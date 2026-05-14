

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
        self.__typebloc = typebloc   #objet
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


class BlocObjectif(Bloc):
    def __init__(self, position, largeur, hauteur) -> None:
        super().__init__(position, "objectif", largeur, hauteur)
        self.solide = False
        self.viscosite = 0.0

VISCOSITE_GLACE = 5.0
class BlocGlace(Bloc):
    def __init__(self, position, largeur, hauteur) -> None:
        super().__init__(position, "glace", largeur, hauteur)
        self.solide = True
        self.viscosite = VISCOSITE_GLACE

class BlocPlateforme(Bloc):
    def __init__(self, position, typebloc, largeur, hauteur) -> None:
        super().__init__(position, typebloc, largeur, hauteur)
        self.solide = True
        self.viscosite = 1.0


class Configuration:

    def __init__(self,nom_niveaux):
        self.nom_niveaux=nom_niveaux
        self.personnage=None
        self.dico_bloc={}
        self.load(nom_niveaux)#dico avec comme cle le typebloc
        #exemple dico_bloc={ "feu" : objet1bloc,objet2bloc,objet3,}
        print(self.dico_bloc)

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
        x = 0
        y = 0
        largeur1 = 0
        hauteur1 = 0

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

                elif cle == "largeur":
                    largeur1=int(valeur)

                elif cle == "hauteur":
                    hauteur1=int(valeur)


            elif mode == "blocs":
                typebloc, pos, largeur, hauteur = ligne.split(";")

                x1, y1 = map(int, pos.split(","))
                largeur = int(largeur)
                hauteur = int(hauteur)

                if typebloc not in self.dico_bloc:
                    self.dico_bloc[typebloc] = []

                if typebloc=="glace":
                    bloc = BlocGlace((x1, y1), largeur, hauteur)

                elif typebloc== "objectif":
                    bloc = BlocObjectif((x1, y1), largeur, hauteur)

                else:
                    bloc = BlocPlateforme((x1, y1), typebloc, largeur, hauteur)




                self.dico_bloc[typebloc].append(bloc)
        self.personnage = Personnage((x, y), largeur1, hauteur1)
