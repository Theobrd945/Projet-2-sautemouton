from physique import MoteurPhysique, Couple, strategies_resistance, tuple_merge
from data import Personnage
from fltk import *

class Multi :

    def __init__(self, config, img):

        self.mp_1 = MoteurPhysique(config, vmax=Couple(10, 20), gravite=7,resistance=strategies_resistance["quatre_vingt"])

        self.mp_2 = MoteurPhysique(config, vmax=Couple(10, 20), gravite=7,resistance=strategies_resistance["quatre_vingt"])

        self.img = img


    def init_window(self):

        cree_fenetre(1000, 800)

        x, y = 500, 400

        image(x, y, 'assets/' + self.img, largeur=1000, hauteur=800, ancrage='center')

    def draw_players_1(self, cords_player_1):
        efface("player_1")
        rectangle(cords_player_1[0], cords_player_1[1], cords_player_1[0] + 25, cords_player_1[1] + 25, couleur='red', remplissage='red', tag='player_1')

    def draw_players_2(self, cords_player_2):
        efface("player_2")
        rectangle(cords_player_2[0], cords_player_2[1], cords_player_2[0] + 25, cords_player_2[1] + 25, couleur='blue', remplissage='blue', tag='player_2')

    def players(self):

        self.init_window()

        self.mp_1.personnage.set_position((300, 435))
        self.mp_2.personnage.set_position((700, 435))

        tour = 0

        running = True

        while running :

            event = donne_ev()
            type_event = type_ev(event)

            if type_event == "Quitte" :

                running = False

            if type_event == "ClicGauche":

                click_coords = abscisse(event), ordonnee(event)

                if tour % 2 == 0:
                    self.mp_1.onclick(tuple_merge(click_coords))
                else:
                    self.mp_2.onclick(tuple_merge(click_coords))

                tour += 1

            objectif_atteint_1 = self.mp_1.update()
            objectif_atteint_2 = self.mp_2.update()

            if objectif_atteint_1:
                print("gagné!")
                running = False

            self.draw_players_1(self.mp_1.personnage.get_position())
            self.draw_players_2(self.mp_2.personnage.get_position())

            mise_a_jour()


        ferme_fenetre()
