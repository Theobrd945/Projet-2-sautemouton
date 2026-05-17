from typing import Callable
from data import Couple, Personnage, Configuration, Bloc, BlocObjectif, couple_split, printwarn, sign, ssqrt, tuple_merge


class Direction: ...
HAUT, BAS, DROITE, GAUCHE, NUL_DIREC = (Direction() for _ in range(5))
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
        self.personnage = Personnage(self.config.personnage.get_position(), self.config.personnage.get_taille())

        self.vmax = vmax
        self.vmin = 0.05
        self.gravite = gravite
        self.vitesse: Couple = Couple()       # vx, vy
        self.resistance: Callable[[Couple], Couple] = resistance        # resistance de l'air
        self.onblock: bool = True

    def onclick(self, click: Couple) -> None:
        if not self.onblock:
            return

        self.onblock = False
        curr_pos = self.personnage.get_position()
        self.vitesse += click - (curr_pos + self.personnage.get_taille().apply(lambda x : x // 2))


    def get_cote_collision(self, position_perso: Couple, taille_perso: Couple,
        position_bloc: Couple, taille_bloc: Couple, vitesse: Couple) -> Direction:
        # on sait déjà qu'il y a collision, on cherche juste de quel coté
        # vérifie que la vitesse vas dans le bon sens -> qu'il y une collision dans cet axe

        collision_gauche = (position_perso.x + taille_perso.x) - position_bloc.x
        collision_droite = (position_bloc.x + taille_bloc.x) - position_perso.x
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
                position_bloc = bloc.get_position()
                taille_bloc = bloc.get_taille()

                if ((nouvelle_position_perso.x < position_bloc.x + taille_bloc.x)   and
                    (nouvelle_position_perso.x + taille_perso.x > position_bloc.x)  and
                    (nouvelle_position_perso.y < position_bloc.y + taille_bloc.y)   and
                    (nouvelle_position_perso.y + taille_perso.y > position_bloc.y)
                ):
                    return bloc, self.get_cote_collision(nouvelle_position_perso, taille_perso, position_bloc, taille_bloc, vitesse)

        return None, NUL_DIREC



    def update(self) -> bool:
        """ renvoie true si le bloc objectif est atteint """
        # printwarn("===== nouvelle frame =====", sev="LOG")

        self.vitesse = self.resistance(self.vitesse)
        if not self.onblock:
            self.vitesse.y += self.gravite

        self.vitesse.apply( lambda v: 0.0 if abs(v) < self.vmin else v )
        capped_speed = self.vitesse.copy()

        capped_speed.x = sign(capped_speed.x) * min(abs(capped_speed.x), self.vmax.x)
        capped_speed.y = sign(capped_speed.y) * min(abs(capped_speed.y), self.vmax.y)

        position_perso = self.personnage.get_position()
        taille_perso = self.personnage.get_taille()

        if capped_speed.x == 0 and capped_speed.y == 0:
            self.personnage.set_position(position_perso + capped_speed)
            return False

        bloc, direction = self.check_collision(position_perso, taille_perso, self.config.dico_bloc, capped_speed)
        if not bloc:
            # prédicteur
            next_speed = self.resistance(capped_speed.copy())
            next_speed.y += self.gravite
            next_frame_collision, _ = self.check_collision(position_perso + capped_speed, taille_perso, self.config.dico_bloc, next_speed)
            if not next_frame_collision:
                self.onblock = False

            self.personnage.set_position(position_perso + capped_speed)
            return False

        # print(f"capped_speed: {capped_speed}")
        # print("collision!")

        if isinstance(bloc, BlocObjectif):
            return True

        position_bloc = bloc.get_position()
        taille_bloc = bloc.get_taille()

        if direction == GAUCHE:
            self.vitesse.x = capped_speed.x = 0.0
            position_perso.x = position_bloc.x - taille_perso.x

        if direction == DROITE:
            self.vitesse.x = capped_speed.x = 0.0
            position_perso.x = position_bloc.x + taille_bloc.x

        if direction == HAUT:
            self.onblock = True
            self.vitesse.y = capped_speed.y = 0.0
            position_perso.y = position_bloc.y - taille_perso.y

        if direction == BAS:
            self.vitesse.y = capped_speed.y = 0.0
            position_perso.y = position_bloc.y + taille_bloc.y

        if direction == NUL_DIREC:
            printwarn("nul direc!", "ERROR")

        self.personnage.set_position(position_perso + capped_speed)
        return False


    def predict(self, click: Couple, n: int = 100, dx_trim = True, dy_trim = False) -> list[Couple]:
        """
        renvoie la liste des n prochaines coodonées après un clique
        dy_trim stop les prédictions à partir du moment ou le personnage touche le sol
        """

        coord_save = self.personnage.get_position()
        speed_save = self.vitesse.copy()
        onblock_save = self.onblock
        self.onclick(click)

        predictions = []
        for _ in range(n):
            self.update()
            if not (dy_trim and self.vitesse.y == 0) and not (dx_trim and self.vitesse.x == 0):
                predictions.append(self.personnage.get_position())

        self.personnage.set_position(coord_save)
        self.vitesse = speed_save
        self.onblock = onblock_save
        return predictions
