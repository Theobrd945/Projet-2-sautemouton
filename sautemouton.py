from physique import MoteurPhysique, tuple_merge, Couple, strategies_resistance, printwarn
from screens import HomeScreen, Map, Level1, Level2, Level3
from data import Configuration
from fltk import donne_ev, type_ev, abscisse, ordonnee, mise_a_jour, ferme_fenetre, rectangle

printwarn("test1")
printwarn("test2", sev="ERROR")


def debut():

    configs = [Configuration("all_levels/level1.txt"), Configuration("all_levels/level2.txt")]

    images = ["img_level_1.png", "img_level_2_2.png", "img_level_3.png"]

    home_screen = HomeScreen()
    home_screen.launch()

    carte = Map()
    name_level = carte.choose_level()

    mp = MoteurPhysique(configs[name_level], vmax=Couple(8, 18), gravite=0.81, resistance=strategies_resistance["quatre_vingt"])

    levels = [Level1(configs[0].dico_bloc, images[0]), Level2(configs[1].dico_bloc, images[1])]


    if carte.launch_level:

        level = levels[name_level]
        level.launch_level()

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

        level.draw_player(mp.personnage.get_position())

        print(f"position: {mp.personnage.get_position()}")
        print(f"vitesse: {mp.vitesse}")
        print(f"on block: {mp.onblock}")

        mise_a_jour()

    ferme_fenetre()


debut()
