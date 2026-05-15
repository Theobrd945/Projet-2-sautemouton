from physique import MoteurPhysique, tuple_merge, Couple, strategies_resistance
from screens import HomeScreen, Map, Level1
from data import Configuration, Queue
from fltk import donne_ev, efface, type_ev, abscisse, ordonnee, mise_a_jour, ferme_fenetre, cercle

TAILLE_TRAINE = 20
def affiche_queue(positions: Queue, current_ids: Queue, unique_id_count: int, taille_perso: Couple) -> int:
    unique_id_count += 1
    current_ids.push(unique_id_count)
    if len(positions) > TAILLE_TRAINE:
        positions.pop()
        efface(f"uid:{current_ids.pop()}")
        print(len(positions))

    for position in positions:
        cercle(position[0] + (taille_perso.x // 2), position[1] + (taille_perso.y // 2), 10, 'white', tag=f'uid:{unique_id_count}')

    return unique_id_count


def debut():

    config = Configuration("all_levels/level1.txt")

    images = ["img_level_1.png"]

    mp = MoteurPhysique(config, Couple(10, 19), gravite=3, resistance=strategies_resistance["quatre_vingt"])
    taille_perso = Couple(mp.personnage.get_largeur(), mp.personnage.get_hauteur())

    home_screen = HomeScreen()
    home_screen.launch()

    carte = Map()
    niveau = carte.choose_level()

    levels = [Level1(config.dico_bloc, images[0])]

    queue_positions = Queue()
    ids = Queue()
    unique_id_count = 0

    if carte.launch_level:
        levels[niveau].launch_level()

    running = True
    while running:
        event = donne_ev()
        type_event = type_ev(event)

        if type_event == "Quitte":
            running = False

        if type_event == "ClicGauche":
            click_coords = abscisse(event), ordonnee(event)
            mp.onclick(tuple_merge(click_coords))

        objectif_atteint = mp.update()

        if objectif_atteint:
            print("gagné!")
            running = False

        position_perso = mp.personnage.get_position()

        queue_positions.push(position_perso)
        unique_id_count = affiche_queue(queue_positions, ids, unique_id_count, taille_perso)

        levels[niveau].draw_player(position_perso)

        print(f"position: {mp.personnage.get_position()}")
        print(f"vitesse: {mp.vitesse}")
        print(f"on block: {mp.onblock}")

        mise_a_jour()

    ferme_fenetre()




debut()
