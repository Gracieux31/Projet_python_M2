# Pour le lancement du jeu
from tkinter import Tk
from game import AgeOfEmpireGame

if __name__ == "__main__":
    root = Tk()
    game = AgeOfEmpireGame(root)
    root.mainloop()