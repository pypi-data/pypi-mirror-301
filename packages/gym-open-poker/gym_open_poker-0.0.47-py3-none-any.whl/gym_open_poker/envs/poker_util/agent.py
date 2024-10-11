from flag_config import flag_config_dict

import logging

logger = logging.getLogger("gym_open_poker.envs.poker_util.logging_info.agent")


class Agent:
    def __init__(
        self,
        make_pre_flop_moves,
        make_flop_moves,
        make_turn_moves,
        make_river_moves,
        strategy_type=None,
    ):
        self.make_pre_flop_moves = make_pre_flop_moves
        self.make_flop_moves = make_flop_moves
        self.make_turn_moves = make_turn_moves
        self.make_river_moves = make_river_moves
        self.is_running = False
        self.strategy_type = strategy_type
        # self._agent_memory = dict()

    def startup(self):
        """
        The function need to be run before simulation. If all phases is not None, we will set is_running to be True
        :return: return successful_action code if all functions are properly set up; otherwise, return failure_code
        """
        if not self.make_pre_flop_moves:
            logger.debug("Agent did not initialized properly. Return failure_code.")
            return flag_config_dict["failure_code"]
        if not self.make_flop_moves:
            logger.debug("Agent did not initialized properly. Return failure_code.")
            return flag_config_dict["failure_code"]
        if not self.make_turn_moves:
            logger.debug("Agent did not initialized properly. Return failure_code.")
            return flag_config_dict["failure_code"]
        if not self.make_river_moves:
            logger.debug("Agent did not initialized properly. Return failure_code.")
            return flag_config_dict["failure_code"]

        # now, all functions are set up properly
        self.is_running = True
        return flag_config_dict["successful_action"]

    def shutdown(self):
        """
        The function is called to shutdown a running agent if the game is terminated or if the agent loss
        all of its money during the game
        :return: return successful_action code if shutdown the agent properly; otherwise, return failure code
        """
        if self.is_running:
            self.is_running = False
        else:
            logger.debug(
                "Trying to shutdown an agent has been shutdown before. Return failure code."
            )
            return flag_config_dict["failure_code"]
        return flag_config_dict["successful_action"]
