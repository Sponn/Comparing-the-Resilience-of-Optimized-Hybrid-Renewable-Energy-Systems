from midas.tools.palaestrai.arl_defender_objective import ArlDefenderObjective
from midas.tools.palaestrai.rewards import ExtendedGridHealthReward

from palaestrai.simulation.taking_turns_simulation_controller import TakingTurnsSimulationController

from harl import SACBrain
# objective = ArlDefenderObjective({})

# print(objective._gauss_fc(1))
# print(objective._gauss_fc(0.9))
# print(objective._gauss_fc(1.1))
# print(objective._gauss_fc(0.05))

import palaestrai

if __name__ == "__main__":
    rc = palaestrai.execute("src/classicarl_experiment_run_parallel_test.yml")

