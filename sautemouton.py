from physique import MoteurPhysique, tuple_merge, Couple, strategies_resistance
from screens import HomeScreen, Map, Level1, Level2, Level3
from data import Configuration
from fltk import donne_ev, type_ev, abscisse, ordonnee, mise_a_jour, ferme_fenetre, rectangle, efface, fleche, touche

def multijoueur(config, level):

    running = True

    mp_1 = MoteurPhysique(config, vmax=Couple(10, 20), gravite=7, resistance=strategies_resistance["quatre_vingt"])

    mp_2 = MoteurPhysique(config, vmax=Couple(10, 20), gravite=7, resistance=strategies_resistance["quatre_vingt"])

    click_coords_1 = mp_1.personnage.get_position()

    click_coords_2 = mp_2.personnage.get_position()

    tour = 0

    while running:

        event = donne_ev()
        type_event = type_ev(event)

        if type_event == "Quitte":
            running = False

        if tour % 2 == 0 :

            if type_event == "ClicGauche":
                click_coords_1 = abscisse(event), ordonnee(event)
                level.draw_direction_jump(mp_1.personnage.get_position(), click_coords_1)

            if type_event == "ClicDroit":
                efface("direction_jump")
                mp_1.onclick(tuple_merge(click_coords_1))

            level.draw_jump(mp_1.personnage.get_position())

            objectif_atteint = mp_1.update()

            if objectif_atteint:
                print("gagné pour le joueur 1!")
                running = False

            level.draw_player(mp_1.personnage.get_position())

            tour += 1

        else :

            if type_event == "ClicGauche":
                click_coords_2 = abscisse(event), ordonnee(event)
                level.draw_direction_jump(mp_2.personnage.get_position(), click_coords_2)

            if type_event == "ClicDroit":
                efface("direction_jump")
                mp_2.onclick(tuple_merge(click_coords_2))

            level.draw_jump(mp_2.personnage.get_position())

            objectif_atteint = mp_2.update()

            if objectif_atteint:
                print("gagné pour le joueur 2!")
                running = False

            level.draw_player(mp_2.personnage.get_position())

            tour += 1

        mise_a_jour()

    ferme_fenetre()


def debut():

    configs = [Configuration("all_levels/level1.txt"), Configuration("all_levels/level2.txt"), Configuration("all_levels/level3.txt")]

    images = ["img_level_1.png", "img_level_2_2.png","img_level_3.png"]

    home_screen = HomeScreen()
    home_screen.launch()

    carte = Map()
    name_level = carte.choose_level()

    mp = MoteurPhysique(configs[name_level], vmax=Couple(10, 20), gravite=7, resistance=strategies_resistance["quatre_vingt"])

    levels = [Level1(configs[0].dico_bloc, images[0]), Level2(configs[1].dico_bloc, images[1]), Level3(configs[2].dico_bloc, images[2])]


    if carte.launch_level:

        level = levels[name_level]
        level.launch_level()

    running = True
    click_coords = mp.personnage.get_position()

    initialize_position = mp.personnage.get_position()

    if name_level == 2:

        running = False
        multijoueur(configs[name_level], level)

        return 0

    while running:

        event = donne_ev()
        type_event = type_ev(event)

        if type_event == "Quitte":
            running = False

        if type_event == "ClicGauche":
            click_coords = abscisse(event), ordonnee(event)
            level.draw_direction_jump(mp.personnage.get_position(), click_coords)

        if type_event == "ClicDroit":
            efface("direction_jump")
            mp.onclick(tuple_merge(click_coords))

        if type_event == "Touche" and touche(event) == "m":

            mp.personnage.set_position(initialize_position)

        level.draw_jump(mp.personnage.get_position())

        objectif_atteint = mp.update()

        if objectif_atteint:
            print("gagné!")
            running = False

        level.draw_player(mp.personnage.get_position())

        mise_a_jour()

    ferme_fenetre()


debut()
