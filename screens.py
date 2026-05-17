from fltk import abscisse, cercle, ordonnee, ligne, fleche, cree_fenetre, image, donne_ev, texte, type_ev, ferme_fenetre, mise_a_jour, efface, rectangle
from data import Couple
from time import time
from math import sqrt

class HomeScreen:

    def __init__(self) -> None:
        self.btn_top_left = 425
        self.btn_top_right = 575
        self.btn_bottom_left = 640
        self.btn_bottom_right = 725

        self.width = 1000
        self.height = 800

    def clicked_button(self, event_location) -> bool:
        abscisse_event, ordonnee_event = abscisse(event_location), ordonnee(event_location)
        if abscisse_event and ordonnee_event:
            return (self.btn_top_left <= abscisse_event <= self.btn_top_right
                    and self.btn_bottom_left <= ordonnee_event <= self.btn_bottom_right)

        return False

    def init_window(self):

        cree_fenetre(self.width, self.height)

        x, y = 500, 400
        image(x, y, fichier='assets/img3.jpg', largeur=self.width, hauteur=self.height, ancrage='center', tag='im')

    def launch(self):

        self.init_window()

        running = True

        while running:

            ev = donne_ev()
            tev: str | None = type_ev(ev)

            if tev == "ClicGauche" and self.clicked_button(ev):

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
        image(500, 400, 'assets/carte2.png', largeur=self.width, hauteur=self.height, ancrage='center', tag='carte')

    def clicked_button(self, event_location, btn_top, btn_bot) -> bool:
        abscisse_event, ordonnee_event = abscisse(event_location), ordonnee(event_location)
        if abscisse_event and ordonnee_event:
            return (self.btn_niveau_left <= abscisse_event <= self.btn_niveau_right
                    and btn_top <= ordonnee_event <= btn_bot)

        return False

    def choose_level(self):
        self.init_window()
        level_is = 0

        running = True
        while running:
            event = donne_ev()
            type_event = type_ev(event)

            if type_event == "ClicGauche":

                if self.clicked_button(event, self.btn_niveau3_top, self.btn_niveau3_bottom):
                    level_is = 2
                    running = False

                elif self.clicked_button(event, self.btn_niveau2_top, self.btn_niveau2_bottom):
                    level_is = 1
                    running = False

                elif self.clicked_button(event, self.btn_niveau1_top, self.btn_niveau1_bottom):
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
        image(500, 400, 'assets/' + self.img, largeur=self.width, hauteur=self.height, ancrage='center')

    def launch_level(self) -> None:
        self.init_window()

    def draw_player(self, coords: Couple, taille_joueur: Couple | None = None):
        taille_joueur = taille_joueur if taille_joueur else Couple(25, 25)
        efface("player")
        rectangle(coords.x, coords.y, coords.x + taille_joueur.x, coords.y + taille_joueur.y, couleur='red', remplissage='red', tag="player")

    def draw_score(self,score,highscore):
        texte(0,0,"score: "+str(score),"white","white","nw",100,tag="score")
        texte(0,100,"meilleur score: " + str(highscore),"white","white","nw",100,tag="score")

    def draw_jump(self, coords: Couple):
        intervalle = 0.006
        maintenant = time()
        if maintenant - self.dernier_point >= intervalle:
            self.points_trajectoire.append(coords)
            self.dernier_point = maintenant

            if len(self.points_trajectoire) > 75:
                self.points_trajectoire.pop(0)

        efface("jump")

        for point in self.points_trajectoire:
            cercle(point.x, point.y, 5, couleur="white", remplissage="white", tag="jump")


    def draw_score(self,score,highscore):
        texte(0,0,"score: "+str(score),"white","white","nw",100,tag="score")
        texte(0,100,"meilleur score: " + str(highscore),"white","white","nw",100,tag="highscore" )


    def draw_direction_jump(self, coords_player, coords_click):
        efface("direction_jump")
        distance = Couple.distance(coords_player, coords_click)

        longueur = 150
        if distance <= 300:
            longueur = distance * 0.5

        u = Couple()        # ??
        if distance != 0:
            u.x = (coords_click.x - coords_player.x) / distance
            u.y = (coords_click.y - coords_player.y) / distance

        end = coords_player + (u * longueur)

        ligne(coords_player.x, coords_player.y, end.x, end.y, couleur="white", epaisseur=5,tag="direction_jump")
        fleche(coords_player.x, coords_player.y, end.x, end.y, couleur="white", epaisseur=5,tag="direction_jump")

class Level1(Level):
    def __init__(self, blocs, img) -> None:
        super().__init__(blocs, img)

class Level2(Level):
    def __init__(self, blocs, img) -> None:
        super().__init__(blocs, img)

class Level3(Level):
    def __init__(self, blocs, img) -> None:
        super().__init__(blocs, img)
