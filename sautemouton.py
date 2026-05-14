from physique import MoteurPhysique, couple_split, tuple_merge, Couple, strategies_resistance, printwarn
from screens import HomeScreen, Map, Level1
from data import Configuration
import pprint
from fltk import *

printwarn("test1")
printwarn("test2", sev="ERROR")

def debut():

    config = Configuration("all_levels/level1.txt")

    images = ["img_level_1.png"]

    mp = MoteurPhysique(config, vmax=Couple(5, 10), gravite=1, resistance=strategies_resistance["quatre_vingt"])

    home_screen = HomeScreen()
    home_screen.launch()

    carte = Map()
    niveau = carte.choose_level()

    levels = [Level1(config.dico_bloc, images[0])]

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
        print(f"vitesse: {mp.vitesse}")
        print(f"on block: {mp.onblock}")

        mise_a_jour()

    ferme_fenetre()




debut()
