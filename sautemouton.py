import data
import physique
import screens

game = screens.HomeScreen()
game.launch()

carte = screens.Map()
level_selected = carte.choose_level()

blocs_level_1 = {
    "murs": [(0, 0, 1, 800), (0, 800, 999, 800), (1000, 800, 998, 0), (0, 0, 999, 0)],
    "platforms": [(0, 715, 1000, 800), (0, 600, 125, 715), (0, 485, 225, 600), (875, 600, 1000, 715),
                  (825, 485, 1000, 600), (440, 485, 590, 595)],
    "spawn_player" : [(850, 435, 900, 485)]}

image_level_1 = "img_level_1.png"

levels = [screens.Level1(blocs_level_1, image_level_1)]

if carte.launch_level:
    levels[level_selected].launch_level()

    player = data.Personnage((900,300),100, 100)

    physique_game = physique.MoteurPhysique(player)




# tache 1: Theo
# tache 2: Adam
# tache 3: Maverick
# tache 4: Adam