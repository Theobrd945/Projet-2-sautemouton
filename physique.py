from typing import Callable

from data import Personnage
from math import sin, pi, sqrt, cos, atan2

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
    print(f"\033[93mWARNING\033[0m: utilisation d'une fonction temporaire")
    return Couple(T[0], T[1])


# noinspection PyPep8Naming
def couple_split(T: Couple) -> tuple:
    """
        affiche un avertissement à chaque utilisation.
        Utilisé comme remplacement en attendant l'utilisation de la classe couple dans le reste du projet
        """
    print(f"\033[93mWARNING\033[0m: utilisation d'une fonction temporaire")
    return T.x, T.y


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

    def norme(self):
        dx, dy = abs(self.origin.x - self.destination.x), abs(self.origin.y - self.destination.y)
        return sqrt(dx ** 2 + dy ** 2)

ORIGIN = Couple(0, 0)
NULVEC = Vecteur(ORIGIN, ORIGIN)
demie_vie = (lambda couple: Couple(couple.x / 2, couple.y / 2))

def vec_from(r: float, theta: float) -> Vecteur:
    return Vecteur(ORIGIN, Couple(r * -cos(pi - theta), r * sin(pi - theta)))

# TODO: niveaux et collision
class MoteurPhysique:
    def __init__(self, personnage: Personnage, vmax: float, gravite: float = 9.8, resistance: Callable = demie_vie):
        self.personnage = personnage
        self.vmax = vmax
        self.vmin = 0.005
        self.gravite = gravite
        self.vitesse: Couple = ORIGIN       # vx, vy
        self.resistance = resistance        # resistance de l'air

    def onclick(self, click: Couple) -> None:
        curr_pos = tuple_merge(self.personnage.get_position())
        self.vitesse += (click - curr_pos)

    def update(self):
        self.vitesse -= self.resistance(self.vitesse)
        self.vitesse -= Couple(0.0, self.gravite)

        if abs(self.vitesse.x) < self.vmin:      self.vitesse.x = 0.0
        if abs(self.vitesse.y) < self.vmin:      self.vitesse.y = 0.0

        self.vitesse.x = min(self.vmax, self.vitesse.x)
        self.vitesse.y = min(self.vmax, self.vitesse.y)

        curr_pos = tuple_merge(self.personnage.get_position())
        curr_pos += self.vitesse
        self.personnage.set_position(couple_split(curr_pos))


if __name__ == '__main__':
    p = Personnage((0, 0))
    mp = MoteurPhysique(p, 20)
    mp.onclick(Couple(100, 100))

    mp.update()
    counter = 100
    while counter:
        print()
        print(f"{mp.vitesse.__str__() = }")
        print(f"{p.get_position() = }")
        mp.update()
        counter -= 1
