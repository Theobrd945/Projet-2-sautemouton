from physique import MoteurPhysique, couple_split, tuple_merge, Couple
from screens import HomeScreen, Map, Level1
from data import Configuration
import pprint
from fltk import *



def debut():

    config = Configuration("all_levels/level1.txt")
    image_level_1 = "img_level_1.png"

    mp = MoteurPhysique(config, vmax=4)

    test = HomeScreen()
    test.launch()

    carte = Map()
    niveau = carte.choose_level()

    levels = [Level1(config.dico_bloc, image_level_1)]

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

        mp.update()
        levels[niveau].draw_player(mp.personnage.get_position())
        print(f"position: {mp.personnage.get_position()}")

        mise_a_jour()

    ferme_fenetre()

    


debut()