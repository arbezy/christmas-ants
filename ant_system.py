from typing import List
import random
import numpy as np

PRINT_INTERVAL = 10


class AntSystem:
    def __init__(
        self, area, num_of_ants: int, elites: int, alpha=1.0, beta=1.0, evaporation=0.05
    ):
        self._validate_init_values(alpha, beta, evaporation, num_of_ants, elites)
        self.pher_mat = np.zeros_like(area, dtype=float)
        self.attractiveness = np.array(area)
        self.elites = elites
        self.ant_num = num_of_ants
        self.alpha = alpha
        self.beta = beta
        self.evaporation = evaporation

    def _validate_init_values(self, alpha, beta, evaporation, num_of_ants, elites):
        if alpha < 0:
            raise ValueError("Alpha must be greater than or equal to 0")
        if beta < 1:
            raise ValueError("Beta must be greater than or equal to 1")
        if not 0 <= evaporation <= 1:
            raise ValueError("Evaporation must be between 0 and 1")
        if elites > num_of_ants:
            raise ValueError("Number of elites cannot exceed number of ants")

    def _pheromone_update(self, ants: List["Ant"]) -> None:
        """Update pheromone matrix based on ant tours."""
        # evaporate existing pheromones
        self.pher_mat *= 1.0 - self.evaporation

        # add new pheromones from each ant
        for ant in ants:
            pheromone_delta = 1.0 / ant.tour_score
            for i, j in ant.tour:
                self.pher_mat[i][j] += pheromone_delta

    def run(self, generations: int) -> "Ant":
        ants = [
            Ant(len(self.attractiveness) - 1, self.alpha, self.beta)
            for _ in range(self.ant_num)
        ]
        for g in range(generations):
            # if g < PRINT_INTERVAL or g % PRINT_INTERVAL == 0:
            #   print(f"generation: {g}/{generations}")

            # create ants and complete a tour for each one
            ants = self._get_solutions(ants)
            ants.sort(key=lambda a: a.tour_score)

            # update pheromone matrix
            elite_ants = ants[: self.elites]
            self._pheromone_update(elite_ants)

        # return ant with the best score at the end of all generations
        """ NOTE: doing it this way kind of assumes that the ants have converged / stopped improving.
        It may be more wise to store the best ant seen across all generations and returning that instead.
        In ACO this ant is already stored for global pheromone updates... """
        ants.sort(key=lambda a: a.tour_score)
        return ants[0]

    def _get_solutions(self, ants: List["Ant"]) -> List["Ant"]:
        # create ant population
        ants = [
            Ant(len(self.attractiveness) - 1, self.alpha, self.beta)
            for _ in range(self.ant_num)
        ]

        # generate solution for each ant
        for a in ants:
            a.generate_solution(self.pher_mat, self.attractiveness)

        return ants


class ElitistAntSystem(AntSystem):
    def run(self, generations: int) -> "Ant":
        bounds = len(self.attractiveness) - 1
        ants = [
            Ant(len(self.attractiveness) - 1, self.alpha, self.beta)
            for _ in range(self.ant_num)
        ]

        best_ant = Ant(bounds, self.alpha, self.beta)
        best_ant.tour_score = float("inf")

        for g in range(generations):
            # create tours for each ant
            ants = self._get_solutions(ants)
            ants.sort(key=lambda a: a.tour_score)

            # check for new best ant
            if ants[0].tour_score < best_ant.tour_score:
                best_ant = ants[0]

            # update pheromone matrix
            elite_ants = ants[: self.elites] + [best_ant]
            self._pheromone_update(elite_ants)

        # return ant with the best score at the end of all generations
        ants.sort(key=lambda a: a.tour_score)
        return ants[0]
        # NOTE: could also just return 'best_ant' here, but I feel as though it is more fair between
        # systems to use the best from the final generation


class Ant:
    def __init__(self, area_bounds, alpha, beta, backtrack_limit=10):
        self.position = (0, 0)
        self.area_bounds = area_bounds
        self.alpha = alpha
        self.beta = beta
        # tour score, this will be the sum of the positions visited
        self.tour_score = 0.0
        self.tour_set = set()
        self.tour = list()
        # dead cells are cells where no solution is possible
        self.dead_cells = set()
        self.backtrack_limit = backtrack_limit

    def get_tour_score(self) -> float:
        return self.tour_score

    def _move(self, trail_level: np.ndarray, attractiveness: np.ndarray) -> bool:
        """
        Move ant to the next position in its tour, based in trail pheromone level and maze shape

        Args:
            trail_level: pheromone level matrix, of pheromones deposited by prev generations of ants
            attractivness: how attractive each cell in an area is i.e. if the cell is free vs. blocked

        Returns:
            True if a move was made, False if none made.
            If no move was made then this tour is invalid and will need to be handled !
        """
        directions = self._get_valid_directions()
        moves = self._get_valid_moves(directions, attractiveness)

        if len(moves) == 0:
            # no possible move so not a valid route
            return False

        move_prob = self._calculate_move_probabilities(
            trail_level, attractiveness, moves
        )
        chosen_move = random.choices(moves, move_prob)[0]

        self._update_position(chosen_move)
        return True

    def _get_valid_directions(self) -> dict:
        """Get movement directions that keep ant within bounds."""
        directions = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}

        if self.position[1] <= 0:
            directions.pop("up")
        elif self.position[1] >= self.area_bounds:
            directions.pop("down")
        if self.position[0] <= 0:
            directions.pop("left")
        elif self.position[0] >= self.area_bounds:
            directions.pop("right")

        return directions

    def _get_valid_moves(self, directions: dict, attractiveness: np.ndarray) -> List:
        """
        Get valid ants mvoes from a list of directions.

        Args:
            directions: a map of valid directions for the ant to go in
            attractiveness: a 2d array representing the maze / search space, where 0 means a blocked cell

        Returns:
            a list of x,y moves that are not blocked and have not already been visited, and are not marked
            as 'dead'.
        """
        moves = [
            (self.position[0] + dx, self.position[1] + dy)
            for dx, dy in directions.values()
        ]

        return list(
            filter(
                lambda m: attractiveness[m[0]][m[1]] != 0
                and m not in self.tour_set
                and m not in self.dead_cells,
                moves,
            )
        )

    def _calculate_move_probabilities(
        self, trail_level: np.ndarray, attractiveness: np.ndarray, moves: List
    ) -> List[float]:
        move_prob = [
            (trail_level[x][y] ** self.alpha) * (attractiveness[x][y] ** self.beta)
            for x, y in moves
        ]

        prob_sum = sum(move_prob)
        if prob_sum > 0:
            return [p / prob_sum for p in move_prob]  # type: ignore

        return [1.0 / len(moves)] * len(moves)

    def _update_position(self, new_position: tuple):
        """Update ant position and tour."""
        self.position = new_position
        self.tour.append(self.position)
        self.tour_set.add(self.position)
        # self.tour_score += attractiveness[self.position[0]][self.position[1]] # USE FOR NON BINARY ATTRACTIVENESS
        self.tour_score += 1

    def generate_solution(
        self, trail_level: np.ndarray, attractiveness: np.ndarray
    ) -> "Ant":
        # make ant perform moves from start to the end point
        end = (len(attractiveness) - 1, len(attractiveness) - 1)
        backtrack_count = 0
        while self.position != end:
            valid = self._move(trail_level, attractiveness)
            if not valid:
                # if a valid solution is not created then backtrack until a limit is reached, then full reset
                if backtrack_count < self.backtrack_limit:
                    self._backtrack()
                    backtrack_count += 1
                else:
                    self._reset_ant()
                    backtrack_count = 0

        return self

    """ NOTE: when I first implemented backtracking it wrecked the solutions, I think becuase the ants
    became overcommited to a path and less exploratory of new ones.
    
    Q: how can I make this a bit less aggressive and a bit more exploratory?
    SOL: adding a backtracking limit. """

    def _backtrack(self):
        """
        Remove the last move from the tour and return to previous position.
        This should only be called when ant is stuck, i.e. no valid moves available
        """
        # mark current cell as dead so ant doesnt return there
        self.dead_cells.add(self.position)

        # move back one time
        last_position = self.tour.pop()
        self.tour_set.remove(last_position)
        self.tour_score -= 1
        self.position = self.tour[-1]

    def _reset_ant(self):
        self.position = (0, 0)
        self.tour_score = 0.0
        self.tour_set = set()
        self.tour = list()
        self.dead_cells = set()
