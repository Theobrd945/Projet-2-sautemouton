from data import Personnage

class Position:
    """
    (x, y)
    """

    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

ORIGIN = Position(0, 0)

from math import sqrt
class Vecteur:
    """
    (x1, y1) -> (x2, y2)
    """
    def __init__(self, a: Position = ORIGIN, b: Position = ORIGIN) -> None:
        self.a = a
        self.b = b
        self.norme = self.calc_norme()

    def calc_norme(self) -> float:
        return sqrt(
            (self.a.x - self.b.x) ** 2 + (self.a.y - self.b.y) ** 2
        )



class MoteurPhysique:
    def __init__(self, personnage: Personnage, gravite: Vecteur = None, vmax: Vecteur = None) -> None:
        self.personnage = personnage
        self.gravite = gravite
        self.vmax = vmax


    def update(self) -> None:
        ...

    def onclick(self, position: tuple[int, int] = (0, 0)) -> None:
        position = self.personnage.get_vitesse()

        force = min(position.norme(), self.vmax)
        

