from physique import MoteurPhysique, Couple, strategies_resistance
from data import Personnage
from fltk import *

class Multi :

    def __init__(self, config, img):

        self.mp = MoteurPhysique(config, vmax=Couple(10, 20), gravite=7, resistance=strategies_resistance["quatre_vingt"])

        self.personnages = [Personnage((200,100), 25, 25), Personnage((700, 100), 25, 25)]

        self.img = img


    def init_window(self):

        cree_fenetre(1000, 800)

        x, y = 500, 400

        image(x, y, 'assets/' + self.img, largeur=1000, hauteur=800, ancrage='center')

    def draw_players(self, cords_player_1, cords_player_2):
        efface("player_1")
        rectangle(cords_player_1[0], cords_player_1[1], cords_player_1[0] + 25, cords_player_1[1] + 25, couleur='red', remplissage='red', tag='player_1')

        efface("player_2")
        rectangle(cords_player_2[0], cords_player_2[1], cords_player_2[0] + 25, cords_player_2[1] + 25, couleur='blue', remplissage='blue', tag='player_2')

    def players(self):

        self.init_window()

        tour = 0

        running = True

        while running :

            cords_player_1 = self.personnages[0].get_position()
            cords_player_2 = self.personnages[1].get_position()

            self.draw_players(cords_player_1, cords_player_2)

            event = donne_ev()
            type_event = type_ev(event)

            if type_event == "Quitte" :

                running = False

            if tour % 2 == 0 :

                if type_event == "ClicGauche" :
                    click_coords = abscisse(event), ordonnee(event)
                    mp.onclick(tuple_merge(click_coords))

            mise_a_jour()


        ferme_fenetre()
