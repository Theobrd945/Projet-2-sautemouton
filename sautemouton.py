from copy import deepcopy
from physique import MoteurPhysique, tuple_merge, Couple, strategies_resistance
from screens import HomeScreen, Level, Map, Level1, Level2, Level3
from data import Configuration, Queue, couple_split
from fltk import donne_ev, touche, type_ev, abscisse, ordonnee, mise_a_jour, ferme_fenetre, rectangle, efface, fleche
from solveur import naive_solver
from multiplayer import Multi


def main():

    score=0

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
    levels = [
        Level1(configs[0].dico_bloc, images[0]),
        Level2(configs[1].dico_bloc, images[1])
    ]

    level = levels[0]
    if carte.launch_level:

        level: Level = levels[name_level]
        level.launch_level()

    running = True
    click_coords = mp.personnage.get_position()
    initialize_position = mp.personnage.get_position()

    solution = Queue()

    while running:
        event = donne_ev()
        type_event = type_ev(event)

        if type_event == "Quitte":
            running = False

        if type_event == "Touche" and touche(event) == "m":

            mp.personnage.set_position(initialize_position)

        if type_event == "ClicGauche":
            click_coords = tuple_merge((abscisse(event), ordonnee(event)))
            level.draw_direction_jump(mp.personnage.get_position(), click_coords)

        if type_event == "ClicDroit":
            efface("direction_jump")
            mp.onclick(click_coords)
            score+=1
            efface("score")
            efface("highscore")

        if type_event == "Touche" and touche(event) == 'Return':
            curr_pos = mp.personnage.get_position()
            solution, termine = naive_solver(mp)
            mp.personnage.set_position(curr_pos)
            if not termine:
                print("aucune solution n'a pu être trouvée")


        if type_event == "Touche" and touche(event) == 'space' and not solution.is_empty():
            mp.onclick(solution.pop())

        objectif_atteint = mp.update()

        if objectif_atteint:
            configs[name_level].save("level" + str(1+(name_level)) + ".txt",score)
            print("gagné!")
            running = False

        level.draw_jump(mp.personnage.get_position())
        level.draw_player(mp.personnage.get_position())

        mise_a_jour()

    ferme_fenetre()


main()
