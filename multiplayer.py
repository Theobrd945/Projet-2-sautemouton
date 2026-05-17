from physique import MoteurPhysique, Couple, strategies_resistance, tuple_merge
from fltk import image, cree_fenetre, efface, rectangle, ligne, fleche, donne_ev, type_ev, ordonnee, abscisse, mise_a_jour, ferme_fenetre

class Multi :

    def __init__(self, config, img):
        self.mp_1 = MoteurPhysique(config, vmax=Couple(5, 10), gravite=3,resistance=strategies_resistance["quatre_vingt"])
        self.mp_2 = MoteurPhysique(config, vmax=Couple(5, 10), gravite=3,resistance=strategies_resistance["quatre_vingt"])
        self.img = img


    def init_window(self):
        cree_fenetre(1000, 800)

        x, y = 500, 400

        image(x, y, 'assets/' + self.img, largeur=1000, hauteur=800, ancrage='center')

    def draw_players_1(self, cords_player_1: Couple):
        efface("player_1")
        image(cords_player_1.x,cords_player_1.y,"assets/img_mouton_2.png",largeur=75,hauteur=75,tag="player")

    def draw_players_2(self, cords_player_2: Couple):
        efface("player_2")
        image(cords_player_2.x,cords_player_2.y,"assets/img_mouton_3.png",largeur=75,hauteur=75,tag="player")

    def draw_direction_jump(self, coords_player: Couple, coords_click: Couple):
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


    def players(self):

        self.init_window()

        self.mp_1.personnage.set_position(Couple(100, 500))
        self.mp_2.personnage.set_position(Couple(900, 500))

        tour = 0

        running = True

        while running :

            event = donne_ev()
            type_event = type_ev(event)

            if type_event == "Quitte" :

                running = False

            if type_event == "ClicGauche":

                click_coords = Couple(abscisse(event), ordonnee(event))

                if tour % 2 == 0:
                    self.draw_direction_jump(self.mp_1.personnage.get_position(), click_coords)
                else:
                    self.draw_direction_jump(self.mp_2.personnage.get_position(), click_coords)

            if type_event == "ClicDroit":

                efface("direction_jump")

                click_coords = Couple(abscisse(event), ordonnee(event))

                if tour % 2 == 0:
                    self.mp_1.onclick(click_coords)
                else:
                    self.mp_2.onclick(click_coords)

                tour += 1

            objectif_atteint_1 = self.mp_1.update()
            objectif_atteint_2 = self.mp_2.update()

            if objectif_atteint_1:
                print("gagné pour le joueur 1!")
                running = False

            if objectif_atteint_2:
                print("gagné pour le joueur 2!")
                running = False

            self.draw_players_1(self.mp_1.personnage.get_position())
            self.draw_players_2(self.mp_2.personnage.get_position())

            mise_a_jour()


        ferme_fenetre()
