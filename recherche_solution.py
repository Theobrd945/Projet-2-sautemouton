from data import *


def algorithme_recherche(niveaux,visites):
    niveau=Configuration(niveaux)
    if niveau.victoire():
        return True
    if niveau.personnage.get_position() in visites:
        return False


