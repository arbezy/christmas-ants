import random
from typing import List
from ant_system import Ant, AntSystem


class AntColony(AntSystem):
    def __init__(
        self,
        area,
        num_of_ants: int,
        alpha=1.0,
        beta=1.0,
        evaporation=0.05,
        init_pheromone=0.1,
        exploitation_threshold=0.3,
    ):
        # set elites to 1 so we only update using the global best ant
        super().__init__(area, num_of_ants, 1, alpha, beta, evaporation)
        self._validate_ac_values(init_pheromone, exploitation_threshold)
        self.t_0 = init_pheromone
        self.q = exploitation_threshold
        self.pher_mat.fill(init_pheromone)

    def _validate_ac_values(self, t_0, q):
        if not 0 <= q <= 1:
            raise ValueError(f"q must be in range [0, 1], but was {q}")
        if t_0 < 0:
            raise ValueError(f"init pheromone must be 0 or greater, was {t_0}")

    def _get_solutions(self, ants: List["Ant"]) -> List["Ant"]:
        """Generate solutions for all ants in the colony."""
        # create ant population
        ants = [
            ACAnt(self, len(self.attractiveness) - 1, self.alpha, self.beta, self.q)
            for _ in range(self.ant_num)
        ]

        # generate solution for each ant
        for ant in ants:
            ant.generate_solution(self.pher_mat, self.attractiveness)

        return ants


# TODO: now that we are passing the parent system, we don't really need to pass any of the parent's properties as parameters...
# i.e. trail_level and attractiveness could just be fetched when they are needed directly from the parent
# NOTE: when parallelising this (if if do parallelise this) write access to the pheromone matrix will need to be protected / atomic
class ACAnt(Ant):
    def __init__(
        self,
        parent_system: AntColony,
        area_bounds,
        alpha,
        beta,
        q=0.3,
        backtrack_limit=10,
    ):
        super().__init__(area_bounds, alpha, beta, backtrack_limit)
        self.parent_system = parent_system
        self.q_threshold = q

    def _move(self, trail_level, attractiveness) -> bool:
        directions = self._get_valid_directions()
        moves = self._get_valid_moves(directions, attractiveness)

        if len(moves) == 0:
            # no move possible so not a valid route
            return False

        # if q threshold is not met then focus on exploiting the best available move
        if random.random() <= self.q_threshold:
            # pick the move with the best pheromone + attractiveness product
            chosen_move = max(
                moves, key=lambda pos: trail_level[pos] * attractiveness[pos]
            )
        else:
            move_prob = self._calculate_move_probabilities(
                trail_level, attractiveness, moves
            )
            chosen_move = random.choices(moves, move_prob)[0]

        self._update_position(chosen_move)
        # local pheromone update for all ants
        self._update_local_pheromones(chosen_move)

        return True

    # to be called on every construction step i.e. after every move
    # encourages the exploration of other paths by reducing pheromone levels on visited edges
    def _update_local_pheromones(self, move: tuple[int, int]):
        # t_ij = (1 - decay) * t_ij + decay * init_trail_level
        i, j = move
        # NOTE: could make local decay a seperate parameter for finer control
        decay = self.parent_system.evaporation
        pheromone_level = self.parent_system.pher_mat[i, j]
        res = (1 - decay) * pheromone_level + decay * self.parent_system.t_0
        self.parent_system.pher_mat[i, j] = res
