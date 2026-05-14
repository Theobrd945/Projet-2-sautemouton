from typing import Callable
from data import Personnage, Configuration, Bloc, BlocObjectif
from math import sqrt
import fltk

class Couple:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    """ couple (couple, y) de réels """
    # distribue l'application sur les membres du couple
    def apply(self, application: Callable[..., float]) -> 'Couple':
        self.x = application(self.x)
        self.y = application(self.y)
        return self

    def copy(self) -> 'Couple':
        return Couple(self.x, self.y)

    def norme(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other: 'Couple') -> 'Couple':
        return Couple(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Couple') -> 'Couple':
        return Couple(self.x - other.x, self.y - other.y)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


def printwarn(s, sev = "warn"):
    return print(f"\033[{"93mWARNING" if sev == "warn" else f"31m{sev}"}\033[0m: {s}")

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


class Direction: ...
HAUT, BAS, DROITE, GAUCHE, NUL_DIREC = (Direction() for _ in range(5))
ORIGIN = Couple(0, 0)
RESISTANCE = 1
EPSILON = 1e-4

# stratégies pour le calcul des frottements de l'air
strategies_resistance = {
    "identite" : lambda x:  x,
    "demie_vie" : lambda couple: Couple(couple.x / 2, couple.y),
    "ssqrt" : lambda couple: couple.apply(ssqrt),
    "quatre_vingt" : lambda couple : couple.apply(lambda v: v * 0.8),
    "lineaire": lambda couple : couple.apply(
        lambda x: x - RESISTANCE
    ),
    "safe_inverse" : lambda couple : couple.apply(
        lambda x: 1/(x + EPSILON)
    ),
    "true_drag" : lambda couple : couple.apply(
        lambda x: 0.5 * 1.293 * x * (20 * 20) * 1.05
    )
}

IDENTITE = strategies_resistance["identite"]


# TODO : collision
class MoteurPhysique:
    def __init__(self, config: Configuration, vmax: Couple,
                gravite: float = 0.02, resistance: Callable[[Couple], Couple] = IDENTITE):
        self.config = config
        self.personnage: Personnage = self.config.personnage if self.config.personnage else Personnage((0, 0), 0, 0)
        self.vmax = vmax
        self.vmin = 0.05
        self.gravite = gravite
        self.vitesse: Couple = ORIGIN       # vx, vy
        self.resistance: Callable[[Couple], Couple] = resistance        # resistance de l'air
        self.onblock: bool = True

    def onclick(self, click: Couple) -> None:
        if not self.onblock:
            return

        self.onblock = False
        curr_pos = tuple_merge(self.personnage.get_position())
        self.vitesse += (click - curr_pos)
        print("click")
        # print(f"{((click - curr_pos).x, (click - curr_pos).y) =}")


    def get_cote_collision(self, position_perso: Couple, taille_perso: Couple,
        position_bloc: Couple, taille_bloc: Couple, vitesse: Couple) -> Direction:
        # on sait déjà qu'il y a collision, on cherche juste de quel coté
        # vérifie que la vitesse vas dans le bon sens -> qu'il y une collision dans cet axe

        collision_droite = (position_perso.x + taille_perso.x) - position_bloc.x
        collision_gauche = (position_bloc.x + taille_bloc.x) - position_perso.x
        collision_haut = (position_perso.y + taille_perso.y) - position_bloc.y
        collision_bas = (position_bloc.y + taille_bloc.y) - position_perso.y

        collision_min = min(collision_droite, collision_gauche, collision_haut, collision_bas)

        if collision_min == collision_droite and vitesse.x < 0:
            return DROITE

        if collision_min == collision_gauche and vitesse.x > 0:
            return GAUCHE

        if collision_min == collision_haut and vitesse.y > 0:
            return HAUT

        if collision_min == collision_bas and vitesse.y < 0:
            return BAS

        # normalement impossible
        return NUL_DIREC

    def check_collision(self, position_perso: Couple, taille_perso: Couple, dico_bloc: dict,
        vitesse: Couple) -> tuple[Bloc | None, Direction]:
        """
        Vérifie si il y a collision à la prochaine update.
        Si oui, renvoie le bloc responsable et la direction du contact
        """

        nouvelle_position_perso = position_perso + vitesse
        for liste_blocs in dico_bloc.values():
            for bloc in liste_blocs:
                position_bloc = tuple_merge(bloc.get_position())
                taille_bloc = Couple(bloc.get_largeur(), bloc.get_hauteur())

                if ((nouvelle_position_perso.x < position_bloc.x + taille_bloc.x)   and
                    (nouvelle_position_perso.x + taille_perso.x > position_bloc.x)  and
                    (nouvelle_position_perso.y < position_bloc.y + taille_bloc.y)   and
                    (nouvelle_position_perso.y + taille_perso.y > position_bloc.y)
                ):
                    return bloc, self.get_cote_collision(nouvelle_position_perso, taille_perso, position_bloc, taille_bloc, vitesse)

        return None, NUL_DIREC



    def update(self) -> bool:
        """ renvoie true si le bloc objectif est atteint """
        printwarn("===== nouvelle frame =====", sev="LOG")

        self.vitesse = self.resistance(self.vitesse)
        if not self.onblock:
            self.vitesse.y += self.gravite

        self.vitesse.apply( lambda v: 0.0 if abs(v) < self.vmin else v )
        capped_speed = self.vitesse.copy()

        capped_speed.x = sign(capped_speed.x) * min(abs(capped_speed.x), self.vmax.x)
        capped_speed.y = sign(capped_speed.y) * min(abs(capped_speed.y), self.vmax.y)

        position_perso = tuple_merge(self.personnage.get_position())
        taille_perso = tuple_merge((self.personnage.get_largeur(), self.personnage.get_hauteur()))

        bloc, direction = self.check_collision(position_perso, taille_perso, self.config.dico_bloc, capped_speed)
        if not bloc:
            self.personnage.set_position(couple_split(position_perso + capped_speed))
            return False

        print(f"capped_speed: {capped_speed}")
        print("collision!")

        if isinstance(bloc, BlocObjectif):
            return True

        position_bloc = tuple_merge(bloc.get_position())
        taille_bloc = Couple(bloc.get_largeur(), bloc.get_hauteur())

        fltk.rectangle(position_bloc.x, position_bloc.y, position_bloc.x + taille_bloc.x, position_bloc.y + taille_bloc.y, "red")

        if direction == GAUCHE:
            self.vitesse.x = capped_speed.x = 0.0
            position_perso.x = position_bloc.x - taille_perso.x - EPSILON

        if direction == DROITE:
            self.vitesse.x = capped_speed.x = 0.0
            position_perso.x = position_bloc.x + taille_bloc.x + EPSILON

        if direction == HAUT:
            self.onblock = True
            self.vitesse.y = capped_speed.y = 0.0
            position_perso.y = position_bloc.y - taille_perso.y - EPSILON

        if direction == BAS:
            self.vitesse.y = capped_speed.y = 0.0
            position_perso.y = position_bloc.y + taille_bloc.y + EPSILON

        if direction == NUL_DIREC:
            print("nul direc!")

        self.personnage.set_position(couple_split(position_perso + capped_speed))
        return False
