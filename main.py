from ant_system import AntSystem
from area_generator import create_area
from print_utils import pprint_area

def main():
    area = create_area(10)
    pprint_area(area)

    AS = AntSystem(area, num_of_ants=3, elites=3, alpha=2.0, beta=1.0, evaporation=0.1)

    systems = {"AS": AS}
    best_ants = []
    for name, s in systems.items():
        best_ant = s.run(100)
        best_ants.append(tuple((best_ant, name)))
        print(f"SYSTEM={name}, best ant route length = {best_ant.tour_score}")

    best_ants.sort(key=lambda ant_tuple: ant_tuple[0].get_tour_score())
    best_ant, best_system = best_ants[0][0], best_ants[0][1]

    if best_system == "AS":
        print("ant system is the best")


if __name__ == "__main__":
    main()