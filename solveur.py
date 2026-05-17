from fltk import cercle
from physique import Couple, MoteurPhysique
from data import Queue


def naive_solver(moteur: MoteurPhysique, essais_max: int = 500000) -> tuple[Queue[Couple], bool]:
    id_cercles = Queue()
    clicks_solution = Queue[Couple]()

    pas = 50
    dist_max = 400
    clicks_possibles = [
        Couple(dx, dy)
        for dx in range(-dist_max, dist_max + 1, pas)
        for dy in range(-dist_max, dist_max + 1, pas)
        if not (dx == 0 and dy == 0)
    ]

    def position_to_key(pos: Couple) -> tuple:
        return (round(pos.x / 5) * 5, round(pos.y / 5) * 5)

    def get_etat():
        pos = moteur.personnage.get_position()
        return (pos, Couple(moteur.vitesse.x, moteur.vitesse.y), moteur.onblock)

    def restore_etat(etat):
        pos, vitesse, onblock = etat
        moteur.personnage.set_position(pos)
        moteur.vitesse = Couple(vitesse.x, vitesse.y)
        moteur.onblock = onblock

    visites = set()
    etat_initial = get_etat()
    key_initial = position_to_key(etat_initial[0])
    visites.add(key_initial)

    # etat_au_moment_d_arriver, chemin_de_clicks, key_de_ce_noeud, index_prochain_click
    pile = [(etat_initial, [], key_initial, 0)]
    essais = 0

    while pile and essais < essais_max:
        etat, chemin, key, idx_click = pile[-1]

        # backtrack si plus rien a essayer
        if idx_click >= len(clicks_possibles):
            pile.pop()
            visites.discard(key)
            continue

        # avance l'index pour la prochaine fois
        pile[-1] = (etat, chemin, key, idx_click + 1)

        # joue le click
        restore_etat(etat)
        click_relatif_stocke = clicks_possibles[idx_click]

        moteur.onclick(click_relatif_stocke)
        reussite = False
        for _ in range(200):
            id = id_cercles.pop() if not id_cercles.is_empty() else "ID_CERCLE1"
            id_cercles.push(
                cercle(moteur.personnage.get_position().x, moteur.personnage.get_position().y, 2, 'gray', 'gray', tag=id)
            )
            reussite = moteur.update()

            if reussite or moteur.onblock:
                break

        if reussite:
            for click in chemin + [click_relatif_stocke]:
                clicks_solution.push(click)
            return clicks_solution, True

        nouvel_etat = get_etat()
        nouvelle_key = position_to_key(nouvel_etat[0])
        pile.append((nouvel_etat, chemin + [click_relatif_stocke], nouvelle_key, 0))

        if nouvelle_key not in visites:
            visites.add(nouvelle_key)
            pile.append((nouvel_etat, chemin + [click_relatif_stocke], nouvelle_key, 0))

        essais += 1
        if essais % 5000 == 0:
            print(f"essais: {essais}/{essais_max}, profondeur: {len(pile)}, visites: {len(visites)}")

    return clicks_solution, False
