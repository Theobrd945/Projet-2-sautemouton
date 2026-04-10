from fltk import * 
import data




class Demarrage :

    def __init__(self) -> None:
        pass

    def ecran_accueil(self):
        
        cree_fenetre(800, 800)

        image(400, 400, 'src/img2.webp',
        largeur=800, hauteur=800, ancrage='center', tag='im')

        rectangle(200, 725, 600, 775)

        texte(365, 735, "Start")

        while True:

            ev = donne_ev()
            tev = type_ev(ev)

            if tev == "ClicGauche":
                print("Clic gauche au point", (abscisse(ev), ordonnee(ev)))

            elif tev == 'Quitte':  # on sort de la boucle
                break

            mise_a_jour()

        ferme_fenetre()

    def carte (self):
        pass

test = Demarrage()
test.ecran_accueil()