from physique import MoteurPhysique, tuple_merge, Couple, strategies_resistance
from screens import HomeScreen, Map, Level1
from data import Configuration, Queue
from fltk import abscisse_souris, donne_ev, efface, ordonnee_souris, type_ev, abscisse, ordonnee, mise_a_jour, ferme_fenetre, cercle


def affiche_queue(
    positions: Queue, current_ids: Queue, unique_id_count: int, taille_perso: Couple,
    taille_traine = 20, taille_bulles = 5, remplissage=''
    ) -> int:

    unique_id_count += 1
    current_ids.push(unique_id_count)

    if len(positions) > taille_traine and taille_traine > 0:
        positions.pop()
        efface(f"uid:{current_ids.pop()}")
        print(len(positions))

    for position in positions:
        position = position if isinstance(position, Couple) else Couple(position[0], position[1])
        cercle(
            position.x + (taille_perso.x // 2), position.y + (taille_perso.y // 2),
            taille_bulles, 'white', remplissage=remplissage,
            tag=f'uid:{unique_id_count}'
        )

    return unique_id_count


def debut():

    config = Configuration("all_levels/level1.txt")

    images = ["img_level_1.png"]

    mp = MoteurPhysique(config, Couple(10, 20), gravite=7, resistance=strategies_resistance["quatre_vingt"])
    taille_perso = Couple(mp.personnage.get_largeur(), mp.personnage.get_hauteur())

    home_screen = HomeScreen()
    home_screen.launch()

    carte = Map()
    niveau = carte.choose_level()

    levels = [Level1(config.dico_bloc, images[0])]

    queue_positions = Queue()
    ids = Queue()
    predictions_ids = Queue()
    unique_id_count = 0

    if carte.launch_level:
        levels[niveau].launch_level()
        levels[niveau].draw_blocs()

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

        if mp.onblock:
            pos_souris = Couple(abscisse_souris(), ordonnee_souris())

            while not predictions_ids.is_empty():
                efface(f'uid:{predictions_ids.pop()}')

            predictions = Queue(mp.predict(100, pos_souris, True))
            unique_id_count = affiche_queue(
                predictions, predictions_ids, unique_id_count, taille_perso,
                taille_traine=-1, taille_bulles=2, remplissage='white'
            )


        print(f"position: {mp.personnage.get_position()}")
        print(f"vitesse: {mp.vitesse}")
        print(f"on block: {mp.onblock}")

        mise_a_jour()

    ferme_fenetre()




debut()
