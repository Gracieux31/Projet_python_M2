
class Entity:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player

class Building(Entity):
    def __init__(self, x, y, player):
        super().__init__(x, y, player)  # Appel du constructeur de la classe parente Entity

class Unit(Entity):
    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.selected = False
        self.vie = 100
        self.damage = 20
        self.attack_range = 50

    def move(self, x, y):
        self.x = x
        self.y = y
        print(f"L'unité de {self.player.name} se déplace en position ({x}, {y})")

    def toggle_selection(self):
        self.selected = not self.selected
        print(f"L'unité de {self.player.name} est {'sélectionnée' if self.selected else 'désélectionnée'}")

    def gather(self, resource_type, amount):
        self.player.gather_resources(resource_type, amount)

    def attack(self, target_unit):
        distance = ((self.x - target_unit.x) ** 2 + (self.y - target_unit.y) ** 2) ** 0.5
        if distance <= self.attack_range:
            target_unit.vie -= self.damage
            print(f"L'unité de {self.player.name} attaque {target_unit.player.name}. vie de la cible: {target_unit.vie}")
            if target_unit.vie <= 0:
                print(f"L'unité de {target_unit.player.name} est éliminée.")
                return True
        return False