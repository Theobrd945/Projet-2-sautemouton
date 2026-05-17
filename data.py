from math import sqrt
from typing import Callable


class Queue[T]:
    def __init__(self, queue: list[T] | None = None) -> None:
        self.queue = queue if queue else []

    def pop(self) -> T:
        return self.queue.pop(-1)

    def push(self, item) -> None:
        self.queue.insert(0, item)

    def is_empty(self) -> bool:
        return len(self.queue) == 0

    def __str__(self) -> str:
        s = ""
        for item in self.queue:
            s += f"({item}) -> "
        return s[:-4] if s else "(empty)"

    def __len__(self) -> int:
        return len(self.queue)

    def __iter__(self):
        return iter(self.queue)

class Stack[T]:
    def __init__(self, stack: list[T] | None = None) -> None:
        self.stack = stack if stack else []

    def pop(self) -> T:
        return self.stack.pop(-1)

    def push(self, item: T) -> None:
        self.stack.append(item)

    def is_empty(self) -> bool:
        return len(self.stack) == 0

    def __len__(self) -> int:
        return len(self.stack)

    def __str__(self) -> str:
        s = ""
        for item in reversed(self.stack):
            s += f"{item}, "
        return f"[{s}]" if s else "[empty]"

class Couple[T]:
    def __init__(self, x: float | int | T = 0, y: float | int | T = 0):
        self.x = x
        self.y = y

    """ couple (couple, y) de réels """
    # distribue l'application sur les membres du couple
    def apply(self, application: Callable[..., float | int]) -> 'Couple':
        self.x = application(self.x)
        self.y = application(self.y)
        return self

    def copy(self) -> 'Couple':
        return Couple(self.x, self.y)

    def norme(self) -> float:
        assert (type(self.x) is float or type(self.x) is int) and (type(self.y) is float or type(self.y) is int)
        return sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other: 'Couple') -> 'Couple':
        assert (type(self.x) is float or type(self.x) is int) and (type(self.y) is float or type(self.y) is int)
        return Couple(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Couple') -> 'Couple':
        assert (type(self.x) is float or type(self.x) is int) and (type(self.y) is float or type(self.y) is int)
        return Couple(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float | int) -> 'Couple':
        return self.apply(lambda v: v * other)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    @staticmethod
    def distance(a, b) -> float:
        return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def printwarn(s, sev = "warn"):
    return print(f"\033[{'93mWARNING' if sev == 'warn' else f'31m{sev}'}\033[0m: {s}")

# noinspection PyPep8Naming
def tuple_merge(T: tuple) -> Couple:
    """
    affiche un avertissement à chaque utilisation.
    Utilisé comme remplacement en attendant l'utilisation de la classe couple dans le reste du projet
    """
    # printwarn("utilisation d'une fonction temporaire tuple_merge")
    return Couple(T[0], T[1])


# noinspection PyPep8Naming
def couple_split(T: Couple) -> tuple:
    """
        affiche un avertissement à chaque utilisation.
        Utilisé comme remplacement en attendant l'utilisation de la classe couple dans le reste du projet
        """
    # printwarn("utilisation d'une fonction temporaire couple_split")
    return T.x, T.y


def sign(x: float) -> int: return -1 if x < 0 else 1
def ssqrt(x: float) -> float: return -sqrt(abs(x)) if x < 0 else sqrt(x)


class Personnage:
    def __init__(self, position: Couple, taille: Couple) -> None:
        self.position: Couple = position
        self.taille: Couple = taille

    def get_position(self) -> Couple:
        return self.position.copy()

    def get_taille(self) -> Couple:
        return self.taille.copy()

    def set_position(self, position: Couple) -> None:
        self.position = position


class Bloc:
    def __init__(self, position: Couple, typebloc: str, taille: Couple)-> None:
        self.position = position #(x,y)
        self.type_bloc = typebloc   #objet
        self.taille = taille

    def get_typebloc(self) -> str:
        return self.type_bloc

    def get_position(self) -> Couple:
        return self.position.copy()

    def get_taille(self) -> Couple:
        return self.taille


class BlocObjectif(Bloc):
    def __init__(self, position, taille) -> None:
        super().__init__(position, "objectif", taille)
        self.solide = False
        self.viscosite = 0.0

VISCOSITE_GLACE = 5.0
class BlocGlace(Bloc):
    def __init__(self, position, taille) -> None:
        super().__init__(position, "glace", taille)
        self.solide = True
        self.viscosite = VISCOSITE_GLACE

class BlocPlateforme(Bloc):
    def __init__(self, position, taille) -> None:
        super().__init__(position, "plateform", taille)
        self.solide = True
        self.viscosite = 1.0


class Configuration:

    def __init__(self, nom_niveaux: str):
        self.nom_niveaux = nom_niveaux
        self.personnage = Personnage(Couple(), Couple())
        self.dico_bloc={}
        self.load(nom_niveaux)

    def get_objectif(self) -> Bloc:
        return self.dico_bloc["objectif"][0]

    def save(self, nom,score) -> None:
        position = self.personnage.get_position()
        with open("all_levels/"+nom, "w") as f:
            f.write("[PERSONNAGE]\n")
            f.write(f"position={position.x},{position.y}\n")
            f.write(f"largeur={self.personnage.get_taille().x}\n")
            f.write(f"hauteur={self.personnage.get_taille().y}\n\n")
            f.write("[BLOCS]\n")

            for liste_blocs in self.dico_bloc.values():
                for bloc in liste_blocs:
                    position_bloc= bloc.get_position()
                    f.write(f"{bloc.get_typebloc()};{position_bloc.x},{position_bloc.y};{bloc.get_taille().x};{bloc.get_taille().y}\n")
            f.write("[HIGHSCORE]\n")
            if  self.highscore is None or score<self.highscore:
                self.highscore=score
            f.write(f"highscore={self.highscore}\n")
            print("sauvegarder")


    def load(self,nom_niveaux) -> None:
        with open(nom_niveaux, "r") as f:
            lignes = f.readlines()

        mode = None
        self.dico_bloc = {}
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

            elif ligne == "[HIGHSCORE]":
                mode= "score"
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
                typebloc, pos, taille_x, taille_y = ligne.split(";")
                taille = Couple[int](int(taille_x), int(taille_y))

                x1, y1 = map(int, pos.split(","))

                if typebloc not in self.dico_bloc:
                    self.dico_bloc[typebloc] = []

                if typebloc == "glace":
                    bloc = BlocGlace(Couple[int](x1, y1), taille)

                elif typebloc == "objectif":
                    bloc = BlocObjectif(Couple[int](x1, y1), taille)

                else:
                    bloc = BlocPlateforme(Couple[int](x1, y1), taille)

                self.dico_bloc[typebloc].append(bloc)

            elif mode == "score":
                nom, self.highscore = ligne.split("=")
                self.highscore = int(self.highscore)
        self.personnage = Personnage(Couple(x, y), Couple(largeur1, hauteur1))
