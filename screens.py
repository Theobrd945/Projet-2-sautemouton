from fltk import *
from data import Niveau


class HomeScreen:

    def __init__(self) -> None:
        self.btn_top_left = 425
        self.btn_top_right = 575
        self.btn_bottom_left = 640
        self.btn_bottom_right = 725

        self.width = 1000
        self.height = 800

    def is_click_on_button(self,event_location) -> bool:

        return (self.btn_top_left <= abscisse(event_location) <= self.btn_top_right
                and self.btn_bottom_left <= abscisse(event_location) <= self.btn_bottom_right)

    def init_window(self):

        cree_fenetre(self.width, self.height)

        x, y = 500, 400
        image(x, y, fichier='assets/img3.jpg',largeur=self.width, hauteur=self.height, ancrage='center', tag='im')

    def launch(self):

        self.init_window()

        running = True

        while running:

            ev = donne_ev()
            tev : str = type_ev(ev)

            if tev == "ClicGauche" and self.is_click_on_button(ev):

                running = False

            elif tev == "Quitte":

                running = False

            mise_a_jour()

        ferme_fenetre()


class Map:

    def __init__(self) -> None:
        pass

    def choose_level(self):

        cree_fenetre(1000, 800)

        image(500, 400, 'assets/carte.jpg',
              largeur=1000, hauteur=800, ancrage='center', tag='carte')

        while True:

            event = donne_ev()
            type_event = type_ev(event)

            if type_event == "ClicGauche":

                aligne_horizontale = 410 <= abscisse(event) <= 590

                if aligne_horizontale and (165 <= ordonnee(event) <= 230):

                    return "Niveau1"

                elif aligne_horizontale and (400 <= ordonnee(event) <= 470):

                    return "Niveau2"

                elif aligne_horizontale and (540 <= ordonnee(event) <= 610):

                    return "Niveau3"

            if type_event == 'Quitte':  # on sort de la boucle
                break

            mise_a_jour()

        ferme_fenetre()


class Niveau1:

    def __init__(self) -> None:
        pass


test = HomeScreen()
test.launch()

carte = Map()
niveau = carte.choose_level()
print(niveau)