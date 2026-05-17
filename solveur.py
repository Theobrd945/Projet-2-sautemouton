from fltk import cercle, donne_ev, efface, mise_a_jour, touche, type_ev
from physique import Couple, MoteurPhysique
from data import Queue


def naive_solver(moteur: MoteurPhysique, essais_max: int = 500000) -> tuple[Queue[Couple], bool]:
    clicks_solution = Queue[Couple]()

    pas = 100
    dist_max = 800
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
    profondeur_max = 20

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
        pos = moteur.personnage.get_position()
        centre = pos + moteur.personnage.get_taille() * 0.5
        click_curr = centre + clicks_possibles[idx_click]
        moteur.onclick(click_curr)

        reussite = False
        for _ in range(30):
            reussite = moteur.update()
            cercle(moteur.personnage.get_position().x, moteur.personnage.get_position().y, 2, 'white', 'white', tag="exploration")
            mise_a_jour()

            ev = donne_ev()
            if type_ev(ev) == 'Touche' and touche(ev) == 'BackSpace':
                efface("exploration")
                mise_a_jour()
                return clicks_solution, reussite

            if reussite or moteur.vitesse == Couple():
                efface("exploration")
                mise_a_jour()
                break

        if reussite:
            for click in chemin + [click_curr]:
                clicks_solution.push(click)
            return clicks_solution, True

        nouvel_etat = get_etat()
        nouvelle_key = position_to_key(nouvel_etat[0])
        # pile.append((nouvel_etat, chemin + [click_curr], nouvelle_key, 0))

        if nouvelle_key not in visites:
            visites.add(nouvelle_key)
            if len(chemin) < profondeur_max:
                pile.append((nouvel_etat, chemin + [click_curr], nouvelle_key, 0))

        essais += 1
        if essais % 5000 == 0:
            print(f"essais: {essais}/{essais_max}, profondeur: {len(pile)}, visites: {len(visites)}")

    return clicks_solution, False
