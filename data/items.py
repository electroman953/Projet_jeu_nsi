import pyxel

class Item:
    # Classe de base pour tous les objets du jeu. Elle regroupe les infos communes :
    # nom, description, position dans la feuille de sprites et attributs de stats.
    def __init__(self, name, description, image_x, image_y):
        self.name = name
        self.description = description
        self.image_x = image_x
        self.image_y = image_y
        self.image_bank = 0
        self.durability = 100
        self.colkey = 0
        self.type = None
        self.liste_attributs = {}

    # Construit et renvoie la liste des stats à afficher dans le tooltip de l'inventaire.
    # Utilise le dictionnaire correspondance_nom de l'app pour afficher des noms lisibles.
    def get_stats(self, app):
        stats = []
        for i, j in self.liste_attributs.items():
            if j != 0:
                stats.append(f"{i if i not in app.correspondance_nom else app.correspondance_nom[i]} : {j}")
        return stats

    # Gère l'état actif d'une arme équipée : active ou désactive le curseur souris,
    # et déclenche une attaque si le joueur clique gauche.
    def etat_arme(self, actif, app):
        pyxel.mouse(actif)
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and actif:
            app.orient_player_to_mouse()
            self.attack(app)


class Potion(Item):
    # Potion consommable. Peut soigner instantanément ou appliquer un effet sur la durée.
    # "attributs" précise le type d'effet (ex: {"heal": True}), "value" la puissance, "duration" la durée en secondes (0 = instantané).
    def __init__(self, name, description, image_x, image_y, attributs, value, duration=0):
        super().__init__(name, description, image_x, image_y)
        self.type = "potion"
        self.image_bank = 1
        self.liste_attributs = attributs
        self.colkey = 3
        self.value = value
        self.duration = duration


class Weapon(Item):
    # Classe parent pour toutes les armes. Stocke les stats de combat dans liste_attributs.
    # "damage" = dégâts de base, les bonus "crit" et "attack_speed" s'ajoutent aux stats du joueur.
    def __init__(self, name, description, image_x, image_y, damage, crit_chance_bonus=0, crit_multiplier_bonus=0, attack_speed_bonus=0):
        super().__init__(name, description, image_x, image_y)
        self.parent_type = "weapon"
        self.liste_attributs["damage"] = damage
        self.liste_attributs["crit_chance_bonus"] = crit_chance_bonus
        self.liste_attributs["crit_multiplier_bonus"] = crit_multiplier_bonus
        self.liste_attributs["attack_speed_bonus"] = attack_speed_bonus

    # Méthode d'attaque à surcharger dans les sous-classes (épée, arc…).
    # Ici elle ne fait rien : c'est un modèle vide que chaque arme spécialise.
    def attack(self, app):
        pass


class Armor(Item):
    # Armure équipable. Réduit les dégâts reçus via "defense" et augmente les PV max via "bonus_health".
    def __init__(self, name, description, image_x, image_y, defense, bonus_health=0):
        super().__init__(name, description, image_x, image_y)
        self.type = "armor"
        self.parent_type = "armor"
        self.liste_attributs["defense"] = defense
        self.liste_attributs["bonus_health"] = bonus_health


class sword(Weapon):
    # Arme de corps-à-corps. Déclenche une animation d'attaque en éventail devant le joueur.
    # Le cooldown (temps entre deux attaques) est réduit par le bonus de vitesse d'attaque.
    def __init__(self, name, description, image_x, image_y, damage, crit_chance_bonus=0.05, crit_multiplier_bonus=0.5, attack_speed_bonus=0.2):
        super().__init__(name, description, image_x, image_y, damage, crit_chance_bonus=0.05, crit_multiplier_bonus=0.5, attack_speed_bonus=0.2)
        self.type = "sword"

    # Lance une attaque de mêlée si le cooldown est écoulé.
    # Déclenche l'animation, recalcule le cooldown et initialise le compteur d'animation.
    def attack(self, app):
        if app.sword_cooldown <= 0:
            app.player_slash()
            app.sword_cooldown = app.SWORD_COOLDOWN - self.liste_attributs.get("attack_speed_bonus", 0)
            app.player.en_attaque = 8
            app.player.next_anim_attaque = 3


class bow(Weapon):
    # Arc : arme à distance qui tire des flèches vers la position de la souris.
    # colkey=7 signifie que la couleur blanche du sprite sera rendue transparente à l'affichage.
    def __init__(self, name, description, image_x, image_y, damage, crit_chance_bonus=0.05, crit_multiplier_bonus=0.5, attack_speed_bonus=0.2):
        super().__init__(name, description, image_x, image_y, damage, crit_chance_bonus=crit_chance_bonus, crit_multiplier_bonus=crit_multiplier_bonus, attack_speed_bonus=attack_speed_bonus)
        self.type = "bow"
        self.colkey = 7

    # Tire une flèche si le cooldown est écoulé. Ajoute le projectile à la liste de l'app.
    def attack(self, app):
        if app.bow_cooldown <= 0:
            app.add_player_projectile("arrow", "basic")
            app.bow_cooldown = app.BOW_COOLDOWN - self.liste_attributs["attack_speed_bonus"]