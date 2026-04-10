

class Personnage:

    def __init__(self, position) -> None:
        self.vitesse = (0,0)
        self.position = position
        self.pas = 0.0
        self.largeur= 0
        self.hauteur= 0



    def set_pas(self,pas):
        self.pas=pas

    def get_pas(self) -> float:
        return self.pas

    def get_position(self):
        return self.position
        





class Bloc:

    def __init__(self, position, typebloc, largeur, hauteur)-> None:
        self.position = position
        self.typebloc = typebloc
        self.largeur = largeur
        self.hauteur = hauteur

    def get_typebloc():
        return self.typebloc

#type: mur sol arrivé
class Niveau:

    def __init__(self, personnage, liste_bloc):
        self.personnage=personnage
        self.liste_bloc=liste_bloc

    def get_fin(self):
        for e in self.liste_bloc:
            if e.get_typebloc()=="arrivé":
                return e    
        



    def save(self,personnage,liste_bloc):
        fichier=open("niveau.txt","w")
        fichier.write(f"{self.personnage.get_position()}\n")
        fichier.write()



class Vecteur:
    def __init__(self,x,y):
        self.x=x
        self.y=y



    





    


