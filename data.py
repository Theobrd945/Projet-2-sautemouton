

class Personnage:

    def __init__(self, position) -> None:
        self.__vitesse = (0,0)
        self.__position = position
        self.__pas = 0.0
        self.__largeur = 0
        self.__hauteur = 0



    def set_pas(self,pas):
        self.__pas = pas

    def get_pas(self) -> float:
        return self.__pas

    def get_position(self):
        return self.__position

    def get_vitesse(self):
        return self.__vitesse

    def get_largeur(self):
        return self.__largeur

    def get_hauteur(self):
        return self.__hauteur

    def set_largeur(self, largeur):
        self.__largeur = largeur

    def set_hauteur(self, hauteur):
        self.__hauteur = hauteur





class Bloc:

    def __init__(self, position, typebloc, largeur, hauteur)-> None:
        self.__position = position #(x,y)
        self.__typebloc = typebloc #elastique,glace,bouee,derapage,objectif
        self.__largeur = largeur
        self.__hauteur = hauteur

    def get_typebloc(self):
        return self.__typebloc

    def get_position(self):
        return self.__position

    def get_largeur(self):
        return self.__largeur

    def get_hauteur(self):
        return self.__hauteur


class Niveau:

    def __init__(self, personnage, dico_bloc):
        self.personnage = personnage
        self.dico_bloc=dico_bloc #dico avec comme cle le typebloc
        #exemple dico_bloc={ "feu" : objet1bloc,objet2bloc,objet3,}

    def get_objectif(self):
        return self.dico_bloc["objectif"]


    def save(self):
        with open("niveau.txt", "w") as f:
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

    def load(self):
        with open("niveau.txt", "r") as f:
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
                    self.personnage = Personnage((x, y))

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

def victoire(personnage, objectif, dico_bloc):
    return objectif==collision(personnage,dico_bloc)



class Vecteur:
    def __init__(self):
        self.x = 0
        self.y = 0



    





    


