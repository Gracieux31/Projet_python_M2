
from entity import Building, Unit

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.resources = {"bois": 200, "or": 200, "nourriture": 200}
        self.units = []
        self.buildings = []

    def create_unit(self):
        if self.resources["nourriture"] >= 50:
            unit = Unit(50 + len(self.units) * 40, 50, self)
            self.units.append(unit)
            self.resources["nourriture"] -= 50
            print(f"{self.name} a créé une unité. Ressources restantes: {self.resources}")
        else:
            print(f"{self.name} n'a pas assez de nourriture pour créer une unité.")

    def gather_resources(self, resource_type, amount):
        self.resources[resource_type] += amount
        print(f"{self.name} a collecté {amount} de {resource_type}. Ressources actuelles: {self.resources}")

    def build(self, x, y):
        if self.resources["bois"] >= 100:
            building = Building(x, y, self)
            self.buildings.append(building)
            self.resources["bois"] -= 100
            print(f"{self.name} a construit un bâtiment. Ressources restantes: {self.resources}")
        else:
            print(f"{self.name} n'a pas assez de bois pour construire un bâtiment.")