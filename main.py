from a_star import astar
from ant_system import AntSystem, ElitistAntSystem
from area_generator import create_area
from print_utils import pprint_area, pprint_tour

def main():
    area = create_area(10)
    pprint_area(area)

    astar_path = astar(area)
    AS = AntSystem(area, num_of_ants=3, elites=3, alpha=2.0, beta=1.0, evaporation=0.1)
    EAS = ElitistAntSystem(area, num_of_ants=3, elites=3, alpha=2.0, beta=1.0, evaporation=0.1)

    systems = {"AS": AS, "EAS": EAS}
    best_ants = []
    for name, s in systems.items():
        best_ant = s.run(100)
        best_ants.append(tuple((best_ant, name)))
        print(f"SYSTEM={name}, best ant route length = {best_ant.tour_score}")

    if astar_path:
        print(f"A* (optimal) route length = {len(astar_path) - 1}")

    best_ants.sort(key=lambda ant_tuple: ant_tuple[0].get_tour_score())
    best_ant, best_system = best_ants[0][0], best_ants[0][1]

    pprint_tour(area, best_ant)
    if best_system == "AS":
        print("ant system is the best")
    elif best_system == "EAS":
        print("elitist ant system is the best")

if __name__ == "__main__":
    main()