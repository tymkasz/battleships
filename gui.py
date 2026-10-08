import tkinter as tk
from tkinter import messagebox

GRID_SIZE = 10
LETTERS = "ABCDEFGHIJ"

# Oznaczenia tekstowe
CHAR_EMPTY = " "
CHAR_SHIP = "S"
CHAR_MISS = "o"
CHAR_HIT = "x"
CHAR_SUNK = "#"

FONT_CELL = ("Consolas", 11, "bold")
COLOR_BG = "#f0f0f0"
COLOR_CELL_BG = "#ffffff"


class BattleshipGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gra w Statki")
        self.root.configure(bg=COLOR_BG)

        self.is_player_turn = True
        self.game_over = False

        # Floty graczy
        self.player_ships = [
            {(1, 1), (1, 2), (1, 3)},  # 3-masztowiec
            {(4, 5), (5, 5)},          # 2-masztowiec
            {(8, 8)}                   # 1-masztowiec
        ]
        self.enemy_ships = [
            {(2, 3), (2, 4), (2, 5)},
            {(6, 7), (7, 7)},
            {(0, 0)}
        ]

        # Łączna liczba masztów do zatopienia
        self.total_enemy_ship_cells = sum(len(ship) for ship in self.enemy_ships)
        self.total_player_ship_cells = sum(len(ship) for ship in self.player_ships)

        # Trafienia i pudła
        self.player_hits = set()
        self.player_misses = set()
        self.enemy_hits = set()
        self.enemy_misses = set()

        self.player_cells = {}
        self.enemy_buttons = {}

        self._build_ui()
        self._init_player_board()

    def _build_ui(self):
        self.status_label = tk.Label(
            self.root, 
            text="Wybierz cel na prawej planszy", 
            font=("Arial", 12, "bold"), 
            bg=COLOR_BG,
            pady=10
        )
        self.status_label.pack()

        boards_frame = tk.Frame(self.root, bg=COLOR_BG, padx=15, pady=10)
        boards_frame.pack()

        # Lewa plansza: Flota gracza
        left_box = tk.Frame(boards_frame, bg=COLOR_BG, padx=15)
        left_box.pack(side=tk.LEFT)
        tk.Label(left_box, text="PLANSZA GRACZA", font=("Arial", 11, "bold"), bg=COLOR_BG).pack(pady=5)
        self._create_grid(left_box, is_enemy=False)

        # Prawa plansza: Cel gracza
        right_box = tk.Frame(boards_frame, bg=COLOR_BG, padx=15)
        right_box.pack(side=tk.RIGHT)
        tk.Label(right_box, text="PLANSZA PRZECIWNIKA", font=("Arial", 11, "bold"), bg=COLOR_BG).pack(pady=5)
        self._create_grid(right_box, is_enemy=True)

    def _create_grid(self, parent, is_enemy):
        grid_frame = tk.Frame(parent, bg=COLOR_BG)
        grid_frame.pack()

        for col in range(GRID_SIZE):
            tk.Label(grid_frame, text=LETTERS[col], width=3, bg=COLOR_BG, font=("Arial", 9, "bold")).grid(row=0, column=col + 1)

        for row in range(GRID_SIZE):
            tk.Label(grid_frame, text=str(row + 1), width=3, bg=COLOR_BG, font=("Arial", 9, "bold")).grid(row=row + 1, column=0)

            for col in range(GRID_SIZE):
                coords = (row, col)

                if is_enemy:
                    btn = tk.Button(
                        grid_frame,
                        text=CHAR_EMPTY,
                        font=FONT_CELL,
                        width=3,
                        height=1,
                        bg=COLOR_CELL_BG,
                        relief=tk.RAISED,
                        command=lambda r=row, c=col: self.on_player_fire(r, c)
                    )
                    btn.grid(row=row + 1, column=col + 1, padx=1, pady=1)
                    self.enemy_buttons[coords] = btn
                else:
                    lbl = tk.Label(
                        grid_frame,
                        text=CHAR_EMPTY,
                        font=FONT_CELL,
                        width=3,
                        height=1,
                        bg=COLOR_CELL_BG,
                        relief=tk.SOLID,
                        borderwidth=1
                    )
                    lbl.grid(row=row + 1, column=col + 1, padx=1, pady=1)
                    self.player_cells[coords] = lbl

    def _init_player_board(self):
        for ship in self.player_ships:
            for coords in ship:
                self.player_cells[coords].config(text=CHAR_SHIP)

    def on_player_fire(self, row, col):
        if not self.is_player_turn or self.game_over:
            return

        coords = (row, col)
        if coords in self.player_hits or coords in self.player_misses:
            return

        btn = self.enemy_buttons[coords]
        hit_ship = self._find_ship_at(coords, self.enemy_ships)

        if hit_ship:
            self.player_hits.add(coords)
            btn.config(text=CHAR_HIT, state=tk.DISABLED, relief=tk.SUNKEN)

            # Sprawdzenie zatopienia pojedynczego statku
            if hit_ship.issubset(self.player_hits):
                for segment in hit_ship:
                    self.enemy_buttons[segment].config(text=CHAR_SUNK)
                self.status_label.config(text=f"Trafiony i zatopiony (#{LETTERS[col]}{row+1})!")
            else:
                self.status_label.config(text=f"Trafienie ({CHAR_HIT}) w {LETTERS[col]}{row+1}!")

            # Sprawdzenie wygranej gracza (zatopienie całej floty wroga)
            if len(self.player_hits) == self.total_enemy_ship_cells:
                self._handle_game_over(player_won=True)
                return
        else:
            self.player_misses.add(coords)
            btn.config(text=CHAR_MISS, state=tk.DISABLED, relief=tk.SUNKEN)
            self.status_label.config(text=f"Pudło ({CHAR_MISS}) w {LETTERS[col]}{row+1}. Tura komputera...")
            
            self.is_player_turn = False
            self.root.after(800, self.simulate_enemy_turn)

    def simulate_enemy_turn(self):
        if self.game_over:
            return

        import random
        available = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) 
                     if (r, c) not in self.enemy_hits and (r, c) not in self.enemy_misses]

        if not available:
            return

        target = random.choice(available)
        cell = self.player_cells[target]
        hit_ship = self._find_ship_at(target, self.player_ships)

        if hit_ship:
            self.enemy_hits.add(target)
            cell.config(text=CHAR_HIT)

            if hit_ship.issubset(self.enemy_hits):
                for segment in hit_ship:
                    self.player_cells[segment].config(text=CHAR_SUNK)
                self.status_label.config(text="Komputer zatopił Twój statek (#)!")
            else:
                self.status_label.config(text="Komputer trafił Twój statek (x)!")

            # Sprawdzenie wygranej komputera (zatopienie całej floty gracza)
            if len(self.enemy_hits) == self.total_player_ship_cells:
                self._handle_game_over(player_won=False)
                return

            self.root.after(800, self.simulate_enemy_turn)
        else:
            self.enemy_misses.add(target)
            cell.config(text=CHAR_MISS)
            self.status_label.config(text="Komputer spudłował (o). Twoja tura!")
            self.is_player_turn = True

    def _handle_game_over(self, player_won):
        self.game_over = True
        self.is_player_turn = False

        # Zablokowanie wszystkich pozostałych przycisków na planszy ataku
        for btn in self.enemy_buttons.values():
            btn.config(state=tk.DISABLED)

        if player_won:
            self.status_label.config(text="KONIEC GRY: Wygrałeś!")
            messagebox.showinfo("Koniec gry", "Wygrałeś! Wszystkie statki wroga zostały zniszczone.")
        else:
            self.status_label.config(text="KONIEC GRY: Przegrałeś!")
            messagebox.showinfo("Koniec gry", "Przegrałeś! Twoja flota poszła na dno.")

    def _find_ship_at(self, coords, ships_list):
        for ship in ships_list:
            if coords in ship:
                return ship
        return None


if __name__ == "__main__":
    app_window = tk.Tk()
    gui = BattleshipGUI(app_window)
    app_window.mainloop()