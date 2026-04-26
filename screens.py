from fltk import *
from data import *


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

        cree_fenetre(self.width, self.height)

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

    def init_window(self):

        cree_fenetre(self.width, self.height)

        x, y = 500, 400

        image(x, y, 'assets/' + self.img, largeur=self.width, hauteur=self.height, ancrage='center')

    def init_level(self):

        for coord in self.blocs["spawn_player"]:
            rectangle(*coord, couleur = "red")

    def launch_level(self):

        self.init_window()
        self.init_level()

        running = True

        while running:

            event = donne_ev()
            type_event = type_ev(event)

            if type_event == "Quitte":
                running = False

            mise_a_jour()

        ferme_fenetre()


class Level1(Level):
    def __init__(self, blocs, img) -> None:
        super().__init__(blocs, img)


blocs_level_1 = {
    "murs": [(0, 0, 1, 800), (0, 800, 999, 800), (1000, 800, 998, 0), (0, 0, 999, 0)],
    "platforms": [(0, 715, 1000, 800), (0, 600, 125, 715), (0, 485, 225, 600), (875, 600, 1000, 715),
                  (825, 485, 1000, 600), (440, 485, 590, 595)],
    "spawn_player" : [(850, 435, 900, 485)]}

image_level_1 = "img_level_1.png"

test = HomeScreen()
test.launch()

carte = Map()
niveau = carte.choose_level()

levels = [Level1(blocs_level_1, image_level_1)]

if carte.launch_level:
    levels[niveau].launch_level()
