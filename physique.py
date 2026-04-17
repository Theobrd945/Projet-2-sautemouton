from data import Personnage
from math import sqrt, atan2, cos, sin, pi

ORIGIN = (0, 0)


class Pair:
    def __init__(self, x: float | int, y: float | int) -> None:
        self.x = x
        self.y = y


class Vecteur:
    def __init__(self, origin: Pair, dest: Pair) -> None:
        self.origin = origin
        self.dest = dest
        self.norme = self.get_norme()

    def get_norme(self) -> float:
        dx, dy = self.origin.x - self.dest.x, self.origin.y - self.dest.y
        return sqrt(dx ** 2 + dy ** 2)

    def __add__(self, other: 'Vecteur') -> 'Vecteur': ...


class Vecteur2:
    def __init__(self, norme: float = ORIGIN, angle: float = ORIGIN) -> None:
        self.norme: float = norme
        self.angle: float = angle

    def __str__(self) -> str:
        return f"({self.angle}rad, {self.norme}u)"

    def __add__(self, other: 'Vecteur2') -> 'Vecteur2':
        sXY: tuple[int, int] = self.to_pairXY()
        otherXY: tuple[int, int] = other.to_pairXY()
        dx, dy = sXY[0] + otherXY[0], sXY[1] + otherXY[1]
        res = Vecteur2()
        return res.from_pairXY((dx, dy))

    def from_pairXY(self, pair: tuple[int, int], origin: tuple[int, int] = ORIGIN) -> 'Vecteur2':
        dx, dy = pair[0] - origin[0], pair[1] - origin[1]
        self.norme = sqrt(dx ** 2 + dy ** 2)
        self.angle = atan2(dx, dy)
        return self

    def to_pairXY(self, origin: tuple[float, float] = ORIGIN) -> tuple[float, float]:
        #TODO: ORIGIN
        return self.norme * -cos(pi - self.angle), self.norme * sin(pi - self.angle)

NULVEC = Vecteur2(0, 0)


class MoteurPhysique:
    def __init__(self, personnage: Personnage, gravite: Vecteur2 = None, vmax: float = 100.0) -> None:
        self.personnage = personnage
        self.gravite = gravite
        self.vmax = vmax
        self.vitesse: Vecteur2 = NULVEC

    def update(self) -> None:
        if (self.vitesse.norme < 0.003):
            self.vitesse = NULVEC

        curr_pos = self.personnage.get_position()
        self.personnage.set_position(
            curr_pos + self.vitesse.to_pairXY(curr_pos)
        )

    def onclick(self, clickpos: tuple[int, int]) -> None:
        vec = Vecteur2()
        vec.from_pairXY(clickpos, self.personnage.get_position())
        vec += self.gravite
        vec.norme = min(self.vmax, vec.norme)
        self.vitesse += vec














from pprint import pprint
# battrie de tests
if __name__ == "__main__":
    personnage = Personnage(ORIGIN)
    gravite = Vecteur2(10, 3/2 * pi)     # (0, 10)
    mp = MoteurPhysique(personnage, gravite)
    mp.onclick((10, 10))

    pprint(mp.personnage.get_position())
    mp.update()
    pprint(mp.personnage.get_position())
    mp.update()
    pprint(mp.personnage.get_position())
    mp.update()
    pprint(mp.personnage.get_position())
    mp.update()
    pprint(mp.personnage.get_position())
    mp.update()
    pprint(mp.personnage.get_position())
    mp.update()
    pprint(mp.personnage.get_position())
    mp.update()
    pprint(mp.personnage.get_position())
    mp.update()
    pprint(mp.personnage.get_position())
    mp.update()
    pprint(mp.personnage.get_position())
    mp.update()
    pprint(mp.personnage.get_position())
    mp.update()
    pprint(mp.personnage.get_position())
    mp.update()
    pprint(mp.personnage.get_position())
    mp.update()
    pprint(mp.personnage.get_position())
    mp.update()
    pprint(mp.personnage.get_position())
    mp.update()
    pprint(mp.personnage.get_position())
    mp.update()