

class Personnage:

    def __init__(self, position,largeur,hauteur) -> None:
        self.__position = position
        self.__largeur = largeur
        self.__hauteur = hauteur


    def get_position(self) -> tuple:
        return self.__position

    def get_largeur(self) -> float:
        return self.__largeur

    def get_hauteur(self) -> float:
        return self.__hauteur

    def set_position(self,position) -> None:
        self.__position = position

    def move(self, dx, dy):
        x, y = self.__position
        self.__position = (x + dx, y + dy)

    def set_largeur(self,largeur):
        self.__largeur=largeur

    def set_hauteur(self,hauteur):
        self.__hauteur=hauteur




class Bloc:

    def __init__(self, position, typebloc, largeur, hauteur)-> None:
        self.__position = position #(x,y)
        self.__typebloc = typebloc #elastique,glace,bouee,derapage,objectif
        self.__largeur = largeur
        self.__hauteur = hauteur

    def get_typebloc(self) -> str:
        return self.__typebloc

    def get_position(self) -> tuple:
        return self.__position

    def get_largeur(self) -> float:
        return self.__largeur

    def get_hauteur(self) -> float:
        return self.__hauteur




class Configuration:

    def __init__(self,nom_niveaux):
        self.nom_niveaux=nom_niveaux
        self.personnage=None
        self.dico_bloc={}
        self.load(nom_niveaux)#dico avec comme cle le typebloc
        #exemple dico_bloc={ "feu" : objet1bloc,objet2bloc,objet3,}

    def get_objectif(self) -> Bloc:
        return self.dico_bloc["objectif"][0]


    def save(self,nom) -> None:
        with open(nom, "w") as f:
            f.write("[PERSONNAGE]\n")
            x, y = self.personnage.get_position()
            f.write(f"position={x},{y}\n")
            f.write(f"largeur={self.personnage.get_largeur()}\n")
            f.write(f"hauteur={self.personnage.get_hauteur()}\n\n")
            f.write("[BLOCS]\n")
            for liste_blocs in self.dico_bloc.values():
                for bloc in liste_blocs:
                    x, y = bloc.get_position()
                    f.write(f"{bloc.get_typebloc()};{x},{y};{bloc.get_largeur()};{bloc.get_hauteur()}\n")

    def load(self,nom_niveaux) -> None:
        with open(nom_niveaux, "r") as f:
            lignes = f.readlines()

        mode = None
        self.dico_bloc = {}
        self.personnage = None

        for ligne in lignes:
            ligne = ligne.strip()
            if not ligne:
                continue
            if ligne == "[PERSONNAGE]":
                mode = "personnage"
                continue
            elif ligne == "[BLOCS]":
                mode = "blocs"
                continue

            if mode == "personnage":
                cle, valeur = ligne.split("=")

                if cle == "position":
                    x, y = map(int, valeur.split(","))
                    self.personnage = Personnage((x,y),0,0)

                elif cle == "largeur":
                    self.personnage.set_largeur(int(valeur))

                elif cle == "hauteur":
                    self.personnage.set_hauteur(int(valeur))

            elif mode == "blocs":
                typebloc, pos, largeur, hauteur = ligne.split(";")

                x, y = map(int, pos.split(","))
                largeur = int(largeur)
                hauteur = int(hauteur)

                bloc = Bloc((x, y), typebloc, largeur, hauteur)

                if typebloc not in self.dico_bloc:
                    self.dico_bloc[typebloc] = []

                self.dico_bloc[typebloc].append(bloc)



def collision(personnage, dico_bloc):
    px, py = personnage.get_position()
    pl = personnage.get_largeur()
    ph = personnage.get_hauteur()

    for liste_blocs in dico_bloc.values():
        for bloc in liste_blocs:
            bx, by = bloc.get_position()
            bl = bloc.get_largeur()
            bh = bloc.get_hauteur()
            if (px < bx + bl) and (px + pl > bx) and (py < by + bh) and (py + ph > by):
                return bloc

    return None

def victoire(personnage, objectif, dico_bloc) -> bool:
    return objectif==collision(personnage,dico_bloc)






    





    


