import gym
import numpy as np
import sys

from card import Card
from action import Action
import collections
import logging

logger = logging.getLogger("gym_open_poker.envs.poker_util.logging_info.novelty.card.card_dist_suit")


class CardDistSuit(gym.Wrapper):
    """
    This novelty, named 'Card1', alters the card distribution by restricting the deck to only cards of specific suits.
    The rules associated with this novelty are as follows:

    1. In the '_initialize_cards' method, the deck is sorted with both suits and numbers in descending order

    2. In the '_reset_board_each_game' method, only the first x cards of the sorting deck will be used and shuffled, where:
       x = total_number_of_players * 2 + 5 + 3
       - Each player is dealt 2 hole cards.
       - There are 5 community cards.
       - 3 cards are designated as burn cards.
    """

    def __init__(self, env, prohibit_suit="club"):

        super().__init__(env)

        assert prohibit_suit in [
            "spade",
            "heart",
            "diamond",
            "club",
        ], f"prohibit_suit should be in ['spade', 'heart', 'diamond', 'club'], current value is {prohibit_suit}"
        sys.modules["initialize_game_elements"]._initialize_cards = getattr(sys.modules[__name__], "_alter_initialize_cards")
        sys.modules["board"].Board.reset_board_each_game = getattr(sys.modules[__name__], "_alter_reset_board_each_game")
        global PROHIBIT_SUIT
        PROHIBIT_SUIT = prohibit_suit


def _alter_reset_board_each_game(self, current_gameboard):
    """
    original: board.reset_board_each_game



    Args:
        current_gameboard

    Returns:
        None

    """

    # deck
    self.deck_idx = 0
    self.community_cards = list()

    # novelty
    first_x_card = int(current_gameboard["total_number_of_players"] * 2 + 5 + 4)
    first_portion = self.deck[:first_x_card]
    second_portion = self.deck[first_x_card:]
    np.random.shuffle(first_portion)
    np.random.shuffle(second_portion)
    self.deck = first_portion + second_portion
    #

    # pots_attendee_list
    attendee = set()
    for p in current_gameboard["players"]:
        if p.status != "lost":
            attendee.add(p.player_name)
    current_gameboard["board"].pots_attendee_list = [attendee]

    # pots_amount_list
    current_gameboard["board"].pots_amount_list = [0]

    # reset players_last_move_list
    for move_idx in range(len(current_gameboard["players"])):
        if (
            current_gameboard["board"].players_last_move_list[move_idx] != Action.LOST
            and current_gameboard["players"][move_idx].status != "lost"
        ):
            current_gameboard["board"].players_last_move_list[move_idx] = Action.NONE

    # player_pot
    self.player_pot = collections.defaultdict(int)

    # update dealer_position:
    dealer_position = self.dealer_position
    total_number_of_players = current_gameboard["total_number_of_players"]

    while True:
        dealer_position = (dealer_position + 1) % total_number_of_players
        if current_gameboard["players"][dealer_position].status != "lost":
            self.dealer_position = dealer_position
            break

    # update big and small blind:
    counter = 0
    for idx in range(dealer_position + 1, dealer_position + total_number_of_players + 1):
        player = current_gameboard["players"][idx % total_number_of_players]
        if player.status != "lost":
            counter += 1
            if counter == 1:
                current_gameboard["board"].small_blind_postiion_idx = idx % total_number_of_players
            elif counter == 2:
                current_gameboard["board"].big_blind_postiion_idx = idx % total_number_of_players


def _alter_initialize_cards(game_elements):
    """
    original: initialize_game_elements._initialize_cards

    Args:
        None

    Returns:


    Raises:

    """
    # novelty
    # nums = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    nums = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    nums = nums[::-1]
    #
    all_suits = ["spade", "heart", "diamond", "club"]
    all_colors = ["black", "red", "red", "black"]
    suits, colors = [], []
    prohibit_color = None
    for suit, color in zip(all_suits, all_colors):
        if suit != PROHIBIT_SUIT:
            suits.append(suit)
            colors.append(color)
        else:
            prohibit_color = color
    assert prohibit_color is not None
    # append prohibit_color to the last, in case there are more player on the table
    suits.append(PROHIBIT_SUIT)
    colors.append(prohibit_color)

    temp_deck = [(num, suit, color) for suit, color in zip(suits, colors) for num in nums]
    deck = list()
    for num, suit, color in temp_deck:
        if num == "A":
            card = Card(suit=suit, number=1, is_num_card=False, is_face_card=False, is_ace_card=True, active=1, color=color)
        elif num.isdigit():
            card = Card(
                suit=suit, number=int(num), is_num_card=True, is_face_card=False, is_ace_card=False, active=1, color=color
            )
        elif num == "J":
            card = Card(suit=suit, number=11, is_num_card=False, is_face_card=True, is_ace_card=False, active=1, color=color)
        elif num == "Q":
            card = Card(suit=suit, number=12, is_num_card=False, is_face_card=True, is_ace_card=False, active=1, color=color)
        elif num == "K":
            card = Card(suit=suit, number=13, is_num_card=False, is_face_card=True, is_ace_card=False, active=1, color=color)
        deck.append(card)
    game_elements["deck"] = deck
