from fltk import *
from data import *
from time import *
from math import *

class HomeScreen:

    def __init__(self) -> None:
        self.btn_top_left = 425
        self.btn_top_right = 575
        self.btn_bottom_left = 640
        self.btn_bottom_right = 725

        self.width = 1000
        self.height = 800

    def is_click_on_button(self, event_location) -> bool:

        return (self.btn_top_left <= abscisse(event_location) <= self.btn_top_right
                and self.btn_bottom_left <= ordonnee(event_location) <= self.btn_bottom_right)

    def init_window(self):

        cree_fenetre(self.width, self.height, frequence=60)

        x, y = 500, 400
        image(x, y, fichier='assets/img3.jpg', largeur=self.width, hauteur=self.height, ancrage='center', tag='im')

    def launch(self):

        self.init_window()

        running = True

        while running:

            ev = donne_ev()
            tev: str = type_ev(ev)

            if tev == "ClicGauche" and self.is_click_on_button(ev):

                running = False

            elif tev == "Quitte":

                running = False

            mise_a_jour()

        ferme_fenetre()


class Map:

    def __init__(self) -> None:
        self.width = 1000
        self.height = 800

        self.btn_niveau_left = 410
        self.btn_niveau_right = 590

        self.btn_niveau3_top = 165
        self.btn_niveau3_bottom = 230

        self.btn_niveau2_top = 400
        self.btn_niveau2_bottom = 470

        self.btn_niveau1_top = 540
        self.btn_niveau1_bottom = 610

        self.launch_level = True

    def init_window(self):

        cree_fenetre(self.width, self.height)

        x, y = 500, 400

        image(x, y, 'assets/carte2.png', largeur=self.width, hauteur=self.height, ancrage='center', tag='carte')

    def isClick_on_button(self, event_location, btn_top, btn_bot) -> bool:

        return (self.btn_niveau_left <= abscisse(event_location) <= self.btn_niveau_right
                and btn_top <= ordonnee(event_location) <= btn_bot)

    def choose_level(self):

        self.init_window()

        level_is = 0

        running = True

        while running:

            event = donne_ev()
            type_event = type_ev(event)

            if type_event == "ClicGauche":

                if self.isClick_on_button(event, self.btn_niveau3_top, self.btn_niveau3_bottom):

                    level_is = 2

                    running = False

                elif self.isClick_on_button(event, self.btn_niveau2_top, self.btn_niveau2_bottom):

                    level_is = 1

                    running = False

                elif self.isClick_on_button(event, self.btn_niveau1_top, self.btn_niveau1_bottom):

                    level_is = 0

                    running = False

            if type_event == 'Quitte':  # on sort de la boucle
                running = False
                self.launch_level = False

            mise_a_jour()

        ferme_fenetre()

        return level_is


class Level:

    def __init__(self, blocs, img) -> None:

        self.width = 1000
        self.height = 800

        self.blocs = blocs
        self.img = img

        self.dernier_point = 0
        self.points_trajectoire = []

    def init_window(self):

        cree_fenetre(self.width, self.height)

        x, y = 500, 400

        image(x, y, 'assets/' + self.img, largeur=self.width, hauteur=self.height, ancrage='center')

    def launch_level(self):
        self.init_window()

    def draw_blocs(self):
        for typebloc, liste_blocs in self.blocs.items():
            for bloc in liste_blocs:
                x, y = bloc.get_position()
                largeur = bloc.get_largeur()
                hauteur = bloc.get_hauteur()

                if typebloc == "glace":
                    image(x+largeur//2,y+hauteur//2,"assets/glace.png",largeur,hauteur)
                elif typebloc == "objectif":
                    image(x+largeur//2,y+hauteur//2,"assets/objectif.png",largeur,hauteur)
                elif typebloc == "platform":
                    image(x+largeur//2,y+hauteur//2,"assets/terre.png",largeur,hauteur+10)



    def draw_player(self, coords):

        taille_joueur = 25
        efface("player")
        rectangle(coords[0], coords[1], coords[0] + taille_joueur, coords[1] + taille_joueur, couleur='red', remplissage='red', tag="player")

    def draw_jump(self, coords):

        maintenant = time()

        intervalle = 0.006

        if maintenant - self.dernier_point >= intervalle:

            self.points_trajectoire.append(coords)

            self.dernier_point = maintenant

            if len(self.points_trajectoire) > 75:
                self.points_trajectoire.pop(0)

        efface("jump")

        for point in self.points_trajectoire:
            cercle(point[0], point[1], 5, couleur="white", remplissage="white", tag="jump")

    def draw_direction_jump(self, coords_player, coords_click):
        efface("direction_jump")

        x1, y1 = coords_player
        x2, y2 = coords_click

        dx = x2 - x1
        dy = y2 - y1
        distance = sqrt(dx ** 2 + dy ** 2)

        if distance > 300:
            longueur = 150
        else:
            longueur = distance * 0.5

        if distance != 0:
            ux = dx / distance
            uy = dy / distance
        else:
            ux = uy = 0

        end_x = x1 + ux * longueur
        end_y = y1 + uy * longueur

        ligne(x1, y1, end_x, end_y, couleur="white", epaisseur=5,tag="direction_jump")

        fleche(x1, y1, end_x, end_y, couleur="white", epaisseur=5,tag="direction_jump")

class Level1(Level):
    def __init__(self, blocs, img) -> None:
        super().__init__(blocs, img)

class Level2(Level):
    def __init__(self, blocs, img) -> None:
        super().__init__(blocs, img)

class Level3(Level):
    def __init__(self, blocs, img) -> None:
        super().__init__(blocs, img)
