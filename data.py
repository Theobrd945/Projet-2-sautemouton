

class Personnage:

    def __init__(self,position) -> None:
        self.vitesse=(0,0)
        self.position=position
        self.vmax=0
        self.gravite=(0,0)
        self.pas=0.0
        self.largeur=0
        self.hauteur=0



    def set_pas(self,pas):
        self.pas=pas

    def get_pas(self):
        return self.pas
        





class Bloc:

    def __init__(self, position, typebloc, largeur, hauteur)-> None:
        self.position = position
        self.typebloc = typebloc
        self.largeur = largeur
        self.hauteur = hauteur


class Niveau:

    def __init__(self,personnage,liste_bloc):
        pass





    


