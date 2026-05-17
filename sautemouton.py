from copy import deepcopy
from physique import MoteurPhysique, tuple_merge, Couple, strategies_resistance
from screens import HomeScreen, Level, Map, Level1, Level2, Level3
from data import Configuration, couple_split
from fltk import donne_ev, touche, type_ev, abscisse, ordonnee, mise_a_jour, ferme_fenetre, rectangle, efface, fleche
from solveur import naive_solver
from multiplayer import Multi


def main():

    configs = [Configuration("all_levels/level1.txt"), Configuration("all_levels/level2.txt"), Configuration("all_levels/level3.txt")]

    images = ["img_level_1.png", "img_level_2_2.png","img_level_3_1.png"]

    home_screen = HomeScreen()
    home_screen.launch()

    carte = Map()
    name_level = carte.choose_level()

    if name_level == 2:

        running = False

        multi = Multi(configs[name_level], images[name_level])
        multi.players()

        return 0

    mp = MoteurPhysique(configs[name_level], vmax=Couple(10, 20), gravite=7, resistance=strategies_resistance["quatre_vingt"])
    sandbox = deepcopy(mp)
    predictions, gg = naive_solver(sandbox)
    print(f"solution brute: {[(str(c)) for c in predictions.queue]}")
    print(f"{'solution trouvée!' if gg else 'pas de solution trouvée'}")

    levels = [Level1(configs[0].dico_bloc, images[0]), Level2(configs[1].dico_bloc, images[1])]

    level = levels[0]
    if carte.launch_level:

        level: Level = levels[name_level]
        level.launch_level()

    running = True
    click_coords = tuple_merge(mp.personnage.get_position())

    initialize_position = mp.personnage.get_position()

    while running:

        event = donne_ev()
        type_event = type_ev(event)

        if type_event == "Quitte":
            running = False

        if type_event == "Touche" and touche(event) == "m":

            mp.personnage.set_position(initialize_position)

        if type_event == "ClicGauche":
            click_coords = tuple_merge((abscisse(event), ordonnee(event)))
            level.draw_direction_jump(mp.personnage.get_position(), couple_split(click_coords))

        if type_event == "ClicDroit":
            efface("direction_jump")
            mp.onclick(click_coords)

        if type_event == "Touche" and touche(event) == 'space':
            click_coords = predictions.pop()
            mp.onclick(click_coords)
            print(f"{mp.personnage.get_position() = }")


        objectif_atteint = mp.update()

        if objectif_atteint:
            print("gagné!")
            running = False

        level.draw_jump(mp.personnage.get_position())
        level.draw_player(mp.personnage.get_position())

        mise_a_jour()

    ferme_fenetre()


main()
