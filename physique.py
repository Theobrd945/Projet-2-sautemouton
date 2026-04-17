from data import Personnage

class Position:
    """
    (x, y)
    """

    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

ORIGIN = Position(0, 0)
class Vecteur: ...

class MoteurPhysique:
    def __init__(self, personnage: Personnage, gravite: Vecteur | None = None, vmax: Vecteur | None = None) -> None:
        self.personnage = personnage
        self.gravite = gravite
        self.vmax = vmax


    def update(self) -> None:
        ...

    def onclick(self, position: tuple[int, int] = (0, 0)) -> None:
        position = self.personnage.get_vitesse()
        force = min(position.norme(), self.vmax)
