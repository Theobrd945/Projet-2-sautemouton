from typing import Callable

from data import Personnage, Configuration, Bloc
from math import sqrt, atan2

class Couple:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    """ couple (couple, y) de réels """

    def __add__(self, other: 'Couple') -> 'Couple':
        return Couple(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Couple') -> 'Couple':
        return Couple(self.x - other.x, self.y - other.y)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


# noinspection PyPep8Naming
def tuple_merge(T: tuple) -> Couple:
    """
    affiche un avertissement à chaque utilisation.
    Utilisé comme remplacement en attendant l'utilisation de la classe couple dans le reste du projet
    """
    print(f"\033[93mWARNING\033[0m: utilisation d'une fonction temporaire tuple_merge")
    return Couple(T[0], T[1])


# noinspection PyPep8Naming
def couple_split(T: Couple) -> tuple:
    """
        affiche un avertissement à chaque utilisation.
        Utilisé comme remplacement en attendant l'utilisation de la classe couple dans le reste du projet
        """
    print(f"\033[93mWARNING\033[0m: utilisation d'une fonction temporaire couple_split")
    return T.x, T.y


def check_collision(personnage, dico_bloc) -> Bloc:
    # par tHéo
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

# a finir
def snap_coords_on_collision(personnage: Personnage, blocs) -> None:
    collision = check_collision(personnage, blocs)
    if not collision: return

    px, py = personnage.get_position()
    pl, ph = personnage.get_largeur(), personnage.get_hauteur()
    
    bx, by = collision.get_position()
    bl, bh = collision.get_largeur(), collision.get_hauteur()



    



class Vecteur:
    """ couple de paire """

    def __init__(self, origin: Couple, destination: Couple):
        self.origin = origin
        self.destination = destination

    def __add__(self, other: 'Vecteur') -> 'Vecteur':
        return Vecteur(self.origin + other.origin, self.destination + other.destination)

    def __str__(self) -> str:
        return f"{self.origin} -> {self.destination} ({self.norme()}u, {self.angle()}rad)"

    def angle(self) -> float:
        dx, dy = abs(self.origin.x - self.destination.x), abs(self.origin.y - self.destination.y)
        return atan2(dx, dy)

    def norme(self) -> float:
        dx, dy = abs(self.origin.x - self.destination.x), abs(self.origin.y - self.destination.y)
        return sqrt(dx ** 2 + dy ** 2)

ORIGIN = Couple(0, 0)
NULVEC = Vecteur(ORIGIN, ORIGIN)

# stratégie par défaut pour le calcul des frottements de l'air
identite = lambda x: x


# TODO: niveaux et collision
class MoteurPhysique:
    def __init__(self, config: Configuration, vmax: float,
                gravite: float = 9.8, resistance: Callable[[Couple], Couple] = identite):
        self.config = config
        self.personnage: Personnage = self.config.personnage
        self.vmax = vmax
        self.vmin = 0.005
        self.gravite = gravite
        self.vitesse: Couple = ORIGIN       # vx, vy
        self.resistance: Callable[[Couple], Couple] = resistance        # resistance de l'air


    def onclick(self, click: Couple) -> None:
        print("click!")
        curr_pos = tuple_merge(self.personnage.get_position())
        self.vitesse += (click - curr_pos)

    def update(self):
        print("update!")
        # refaire
        #self.vitesse += self.resistance(self.vitesse)
        self.vitesse += Couple(0.0, self.gravite)

        # a finir
        if check_collision(self.personnage, self.config.dico_bloc):
            self.vitesse.y = 0.0

        if abs(self.vitesse.x) < self.vmin:      self.vitesse.x = 0.0
        if abs(self.vitesse.y) < self.vmin:      self.vitesse.y = 0.0

        # a finir: si x < 0: ..., x > 0: _ 
        self.vitesse.x = min(self.vmax, self.vitesse.x)
        self.vitesse.y = min(self.vmax, self.vitesse.y)

        print(f"{self.vitesse.x = } {self.vitesse.y = }")

        curr_pos = tuple_merge(self.personnage.get_position())
        curr_pos += self.vitesse
        self.personnage.set_position(couple_split(curr_pos))








demie_vie = (lambda couple: Couple(couple.x / 2, couple.y / 2))
def ssqrt(x: float) -> float:
    # signed square root
    if x < 0: return -sqrt(abs(x))
    return sqrt(x)
racine_signe = (lambda couple: Couple(ssqrt(couple.x), ssqrt(couple.y)))
soixante_dix_pourcent = lambda couple : Couple(couple.x * 0.7, couple.y * 0.7)
full_inverse = lambda couple: Couple(1 / couple.x, 1/ couple.y)
drag = lambda couple : Couple(0.5 * 1.293 * couple.x * (20 * 20) * 1.05, 0.5 * 1.293 * couple.y * (20 * 20) * 1.05)
RESISTANCE = 100
linaire = lambda couple : Couple(couple.x - RESISTANCE, couple.y - RESISTANCE)