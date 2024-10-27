
import tkinter as tk
from player import Player

class AgeOfEmpireGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Age of Empire - Jeu simple")
        self.canvas = tk.Canvas(self.master, width=600, height=400, bg="light green")
        self.canvas.pack()

        # Création des joueurs
        self.players = [Player("Joueur 1", "blue"), Player("Joueur 2", "red")]
        self.current_player = self.players[0]  # Le joueur 1 commence

        # Affichage des ressources
        self.resource_label = tk.Label(self.master, text=self.update_resource_display())
        self.resource_label.pack()

        # Stocker les objets graphiques des unités et des bâtiments
        self.unit_graphics = {}  
        self.building_graphics = []

        # Boutons de commande
        self.unit_button = tk.Button(self.master, text="Créer Unité", command=self.create_unit)
        self.unit_button.pack(side=tk.LEFT)
        self.build_button = tk.Button(self.master, text="Construire Bâtiment", command=self.prepare_build)
        self.build_button.pack(side=tk.LEFT)
        self.attack_button = tk.Button(self.master, text="Attaquer", command=self.prepare_attack)
        self.attack_button.pack(side=tk.LEFT)
        self.end_turn_button = tk.Button(self.master, text="Fin de tour", command=self.end_turn)
        self.end_turn_button.pack(side=tk.LEFT)

        # Initialisation des zones de ressources
        self.create_resource_areas()

        # Gestion des clics pour la sélection, le déplacement et la construction
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.build_mode = False
        self.attack_mode = False
        self.selected_unit = None  # Unité actuellement sélectionnée
        self.target_unit = None  # Unité cible pendant l'attaque

    def update_resource_display(self):
        """Met à jour l'affichage des ressources du joueur actuel."""
        resources = self.current_player.resources
        return f"Ressources de {self.current_player.name} - Bois: {resources['bois']} | Or: {resources['or']} | Nourriture: {resources['nourriture']}"

    def refresh_resources(self):
        """Actualise l'affichage des ressources."""
        self.resource_label.config(text=self.update_resource_display())

    def prepare_build(self):
        """Active le mode construction pour le joueur actuel."""
        print(f"{self.current_player.name} est en mode construction")
        self.build_mode = True

    def prepare_attack(self):
        """Active le mode attaque pour le joueur actuel."""
        print(f"{self.current_player.name} est en mode attaque")
        self.attack_mode = True

    def create_unit(self):
        """Crée une nouvelle unité pour le joueur actuel."""
        self.current_player.create_unit()
        unit = self.current_player.units[-1]
        unit_graphic = self.canvas.create_oval(unit.x, unit.y, unit.x + 30, unit.y + 30, fill=self.current_player.color)
        unit_vie_text = self.canvas.create_text(unit.x + 15, unit.y + 40, text=f"vie: {unit.vie}", fill="black")
        self.unit_graphics[unit] = (unit_graphic, unit_vie_text)  # Associer l'unité à ses éléments graphiques
        self.refresh_resources()

    def on_canvas_click(self, event):
        """Gestion des clics de souris pour sélectionner, déplacer et attaquer."""
        if self.build_mode:
            # Si le joueur est en mode construction, il peut placer un bâtiment
            self.build_building(event.x, event.y)
            self.build_mode = False  # Désactiver le mode construction après la construction
        else:
            clicked_unit = None
            # Vérifier si l'utilisateur a cliqué sur une unité
            for unit, (graphic, vie_text) in self.unit_graphics.items():
                x1, y1, x2, y2 = self.canvas.coords(graphic)
                if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                    clicked_unit = unit
                    break

            if clicked_unit:
                # Si une unité est cliquée, la sélectionner/désélectionner
                if self.selected_unit:
                    self.selected_unit.toggle_selection()
                self.selected_unit = clicked_unit
                self.selected_unit.toggle_selection()
            elif self.selected_unit:
                # Déplacer l'unité sélectionnée
                if not self.check_collision(event.x, event.y, self.selected_unit):
                    self.selected_unit.move(event.x, event.y)
                    # Mettre à jour les coordonnées du graphique de l'unité
                    self.canvas.coords(self.unit_graphics[self.selected_unit][0], self.selected_unit.x, self.selected_unit.y, self.selected_unit.x + 30, self.selected_unit.y + 30)
                    self.canvas.coords(self.unit_graphics[self.selected_unit][1], self.selected_unit.x + 15, self.selected_unit.y + 40)
                    # Vérifier si l'unité récolte des ressources
                    self.check_resource_zone(event.x, event.y)
                    # Attaquer si une unité ennemie est proche
                    for unit, (graphic, vie_text) in self.unit_graphics.items():
                        if unit.player != self.current_player and self.selected_unit.attack(unit):
                            self.canvas.delete(graphic)  # Supprimer l'unité graphique
                            self.canvas.delete(vie_text)  # Supprimer le texte de vie
                            del self.unit_graphics[unit]
                            break
                        else:
                            self.canvas.itemconfig(vie_text, text=f"vie: {unit.vie}")  # Mettre à jour la vie de la cible

    def build_building(self, x, y):
        """Construit un bâtiment pour le joueur actuel."""
        self.current_player.build(x, y)
        if self.current_player.buildings:
            building = self.current_player.buildings[-1]
            building_graphic = self.canvas.create_rectangle(building.x, building.y, building.x + 50, building.y + 50, fill=self.current_player.color)
            self.building_graphics.append(building_graphic)
            self.refresh_resources()

    def create_resource_areas(self):
        """Crée les zones de ressources sur le canevas."""
        self.resource_zones = [
            {"type": "bois", "x1": 400, "y1": 50, "x2": 450, "y2": 100, "amount": 50, "color": "green"},
            {"type": "or", "x1": 400, "y1": 150, "x2": 450, "y2": 200, "amount": 30, "color": "yellow"},
            {"type": "nourriture", "x1": 400, "y1": 250, "x2": 450, "y2": 300, "amount": 40, "color": "orange"},
        ]
        for zone in self.resource_zones:
            self.canvas.create_rectangle(zone["x1"], zone["y1"], zone["x2"], zone["y2"], fill=zone["color"])
            self.canvas.create_text((zone["x1"] + zone["x2"]) // 2, zone["y2"] + 15, text=f"{zone['type'].capitalize()}")

    def check_resource_zone(self, x, y):
        """Vérifie si l'unité se trouve dans une zone de ressources et récolte."""
        for zone in self.resource_zones:
            if zone["x1"] <= x <= zone["x2"] and zone["y1"] <= y <= zone["y2"]:
                for unit in self.current_player.units:
                    if unit.selected:
                        unit.gather(zone["type"], zone["amount"])
                        self.refresh_resources()

    def check_collision(self, x, y, current_unit):
        """Vérifie si une unité tente de se déplacer dans une position occupée par une autre unité."""
        for unit, (graphic, _) in self.unit_graphics.items():
            if unit != current_unit:  # Ne pas vérifier la collision avec l'unité elle-même
                x1, y1, x2, y2 = self.canvas.coords(graphic)
                if x1 <= x <= x2 and y1 <= y <= y2:
                    print(f"Collision détectée avec l'unité de {unit.player.name} à ({x1}, {y1})")
                    return True
        return False

    def end_turn(self):
        """Passe au joueur suivant."""
        current_index = self.players.index(self.current_player)
        self.current_player = self.players[(current_index + 1) % len(self.players)]
        print(f"C'est au tour de {self.current_player.name}")
        self.refresh_resources()