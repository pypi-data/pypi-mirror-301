import gym
import gym_open_poker
import sys
import logging
from agent import Agent
from gym_open_poker.envs.poker_util.agents import agent_dump, agent_random, agent_p

logger = logging.getLogger("gym_open_poker.envs.poker_util.logging_info.novelty.agent.agent_exchange")


class AgentExchange(gym.Wrapper):
    """
    This novelty modifies one of the player's strategies. It is important to note that this novelty remains inactive and has
    no impact if agents agent_p, agent_random, and agent_dump are not utilized in the tournament. In such cases, a warning
     message will be recorded in the log.

    The rules associated with this novelty are as follows:
        1. agent_p -> agent_random
        2. agent_random -> agent_p
        3. agent_dump -> agent_p
    """

    def __init__(self, env):

        super().__init__(env)

        found_substutued_agent_all = False
        for player_name in env.player_decision_agents:
            found_substutued_agent = False
            if player_name != "player_1":
                original_stratedy = env.player_decision_agents[player_name].strategy_type

                if original_stratedy == "agent_p":
                    replacing_strategy = "agent_dump"
                    found_substutued_agent = True
                elif original_stratedy == "agent_random":
                    replacing_strategy = "agent_p"
                    found_substutued_agent = True
                elif original_stratedy == "agent_dump":
                    replacing_strategy = "agent_p"
                    found_substutued_agent = True

                if found_substutued_agent:
                    substituting_agent = getattr(sys.modules[__name__], replacing_strategy)
                    env.player_decision_agents[player_name] = Agent(**substituting_agent.decision_agent_methods)
                    logger.debug(f"{player_name}'s strategy_type is replaced from {original_stratedy} to {replacing_strategy}")

            found_substutued_agent_all = found_substutued_agent_all or found_substutued_agent

        if not found_substutued_agent_all:
            logger.warn("Cannot find agent_p, agent_random, and agent_dump in the tournament. This novelty has no impact!")
