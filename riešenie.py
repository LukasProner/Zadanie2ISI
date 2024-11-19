import tkinter as tk
from tkinter import messagebox
import json
from collections import deque

with open("states.json", "r") as file:
    data = json.load(file)

# Konštanty pre veľkosť hracieho poľa a buniek, načítané z JSON súboru
GRID_SIZE = data["grid_size"]
CELL_SIZE = data["cell_size"]

PLAYER_INDEX = 0

# Inicializácia hlavného okna
window = tk.Tk()
window.title("Lunar Lander")

# Nastavenie hracieho plátna
canvas = tk.Canvas(window, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE)
canvas.pack()

# Načítanie hráčov a cieľa z JSON
players = [{"position": tuple(player["position"]), "color": player["color"]} for player in data["players"]]
goal_position = tuple(data["goal_position"])

# Vykreslenie hracej plochy
def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x1 = col * CELL_SIZE
            y1 = row * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            canvas.create_rectangle(x1, y1, x2, y2, outline="black")

# Vykreslenie figúrok a cieľa
def draw_elements():
    canvas.delete("all")
    draw_grid(data["players"])

    # Vykreslenie cieľa
    goal_x1, goal_y1 = goal_position[1] * CELL_SIZE, goal_position[0] * CELL_SIZE
    goal_x2, goal_y2 = goal_x1 + CELL_SIZE, goal_y1 + CELL_SIZE
    canvas.create_rectangle(goal_x1, goal_y1, goal_x2, goal_y2, fill="grey", tags="goal")

    # Vykreslenie hráčov
    for player in players:
        player_x1, player_y1 = player["position"][1] * CELL_SIZE, player["position"][0] * CELL_SIZE
        player_x2, player_y2 = player_x1 + CELL_SIZE, player_y1 + CELL_SIZE
        canvas.create_rectangle(player_x1, player_y1, player_x2, player_y2, fill=player["color"], tags="player")

# Logika pohybu pre konkrétneho hráča
def move_player(player_index, direction):
    row, col = players[player_index]["position"]

    if direction == "up" and row > 0:
        while row > 0 and (row - 1, col) not in obstacles():
            row -= 1
            if (row, col) in obstacles():
                break
            elif row == 0:
                change_player_index(0)
                players.pop(player_index)
                print_player_list()
                return
    elif direction == "down" and row < GRID_SIZE - 1:
        while row < GRID_SIZE - 1 and (row + 1, col) not in obstacles():
            row += 1
            if (row, col) in obstacles():
                break
            elif row == GRID_SIZE - 1 :
                change_player_index(0)
                players.pop(player_index)
                print_player_list()
                return

    elif direction == "left" and col > 0:
        while col > 0 and (row, col - 1) not in obstacles():
            col -= 1
            if (row, col) in obstacles():
                break
            elif col == 0 :
                change_player_index(0)
                players.pop(player_index)
                print_player_list()
                return
    elif direction == "right" and col < GRID_SIZE - 1:
        while col < GRID_SIZE - 1 and (row, col + 1) not in obstacles():
            col += 1
            if (row, col) in obstacles():
                break
            elif col == GRID_SIZE - 1:
                change_player_index(0)
                players.pop(player_index)
                print_player_list()
                return

    # Aktualizácia pozície hráča
    players[player_index]["position"] = (row, col)

    # Ak hlavný hráč dosiahol cieľ, hra končí
    if player_index == 0:
        check_goal()

# Pomocná funkcia na získanie pozícií všetkých hráčov ako prekážok
def obstacles():
    return {player["position"] for player in players}

# Kontrola či hlavný hráč dosiahol cieľ
def check_goal():
    if players[0]["position"] == goal_position:
        messagebox.showinfo("Gratulujeme!", "Hlavný hráč dosiahol cieľ!")
    draw_elements()

# Nastavenie ovládania
def on_key_press(event):
    global PLAYER_INDEX
    if event.keysym == "Up":
        move_player(PLAYER_INDEX, "up")
    elif event.keysym == "Down":
        move_player(PLAYER_INDEX, "down")
    elif event.keysym == "Left":
        move_player(PLAYER_INDEX, "left")
    elif event.keysym == "Right":
        move_player(PLAYER_INDEX, "right")
    draw_elements()

def change_player_index(index):
    global PLAYER_INDEX
    if 0 <= index < len(players):
        PLAYER_INDEX = index
        messagebox.showinfo("Zmena hráča", f"Teraz ovládate hráča {PLAYER_INDEX + 1}")


button_frame = tk.Frame(window)
button_frame.pack(side="top")


from collections import deque


def draw_grid(players):
    """Vykreslí mriežku so zobrazením pozícií hráčov a prekážok."""
    grid = [["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


    # Vykresli pozície hráčov
    for player in players:
        row, col = player["position"]
        grid[row][col] = player.get("color", "P")

    # Vytlač mriežku
    for row in grid:
        print(" ".join(row))
    print("\n" + "-" * (2 * GRID_SIZE - 1))  # Oddelí každú iteráciu


from collections import deque

GRID_SIZE = 5  # Veľkosť mriežky (napr. 5x5)

def move_players_by_path(players, path):
    # Iteruj cez každý krok v ceste
    for player_index, direction in path:
        row, col = players[player_index]["position"]

        # Simuluj pohyb hráča podľa smeru
        if direction == "up" and row > 0:
            while row > 0 and (row - 1, col) not in obstacles() and (row - 1, col) not in [p["position"] for p in players if p != players[player_index]]:
                row -= 1
        elif direction == "down" and row < GRID_SIZE - 1:
            while row < GRID_SIZE - 1 and (row + 1, col) not in obstacles() and (row + 1, col) not in [p["position"] for p in players if p != players[player_index]]:
                row += 1
        elif direction == "left" and col > 0:
            while col > 0 and (row, col - 1) not in obstacles() and (row, col - 1) not in [p["position"] for p in players if p != players[player_index]]:
                col -= 1
        elif direction == "right" and col < GRID_SIZE - 1:
            while col < GRID_SIZE - 1 and (row, col + 1) not in obstacles() and (row, col + 1) not in [p["position"] for p in players if p != players[player_index]]:
                col += 1

        # Ak hráč vypadol, zmeníme jeho pozíciu na (-1, -1)
        if (row <= 0 and direction == "up") or (row >= GRID_SIZE - 1 and direction == "down") or (col <= 0 and direction == "left") or (col >= GRID_SIZE - 1 and direction == "right"):
            row, col = -1, -1
            print(f"Hráč {players[player_index]['color']} vypadol smerom {direction} z pozície ({players[player_index]['position']})")

        # Aktualizácia pozície hráča
        players[player_index]["position"] = (row, col)

        # Ak hlavný hráč (index 0) dosiahol cieľ, hra končí
        if player_index == 0:
            check_goal()

    # Vytlač aktuálnu pozíciu hráčov po vykonaní všetkých krokov
    print_player_list()


def find_shortest_path(players, goal):
    # Inicializácia fronty a navštívených stavov
    queue = deque([(tuple(tuple(player["position"]) for player in players), [])])
    visited = set()
    visited.add(tuple(tuple(player["position"]) for player in players))

    while queue:
        current_positions, path = queue.popleft()
        print("Aktuálne pozície hráčov: ", current_positions)

        # Skontroluj, či červený hráč (hráč 1) dosiahol cieľ
        if current_positions[0] == goal:
            print(players[0]["color"])
            return path

        # Pre každého hráča simuluj pohyb
        for i, (row, col) in enumerate(current_positions):
            if (row, col) == (-1, -1):  # Hráč už vypadol
                continue

            directions = ["up", "down", "left", "right"]
            for direction in directions:
                new_positions = list(current_positions)
                new_row, new_col = row, col

                # Simulácia pohybu
                if direction == "up":
                    while new_row > 0 and (new_row - 1, col) not in current_positions:
                        new_row -= 1
                elif direction == "down":
                    while new_row < GRID_SIZE - 1 and (new_row + 1, col) not in current_positions:
                        new_row += 1
                elif direction == "left":
                    while new_col > 0 and (row, new_col - 1) not in current_positions:
                        new_col -= 1
                elif direction == "right":
                    while new_col < GRID_SIZE - 1 and (row, new_col + 1) not in current_positions:
                        new_col += 1

                if (new_row <= 0 and direction == "up") or (new_row >= GRID_SIZE-1 and direction == "down") or (new_col <= 0 and direction== "left") or (new_col >= GRID_SIZE-1 and direction=="right"):
                    new_row, new_col = -1, -1
                    print(f"vypadol {players[i]["color"]} smerom {direction} z pozicie {row}{col}")

                # Aktualizuj pozíciu hráča
                new_positions[i] = (new_row, new_col)

                # Skontroluj, či sme tento stav už navštívili
                new_positions_tuple = tuple(new_positions)
                if new_positions_tuple not in visited:
                    visited.add(new_positions_tuple)
                    queue.append((new_positions_tuple, path + [(i, direction)]))

    return None  # Ak červený hráč nedosiahne cieľ

def execute_bfs_solution(start, goal):
    path = find_shortest_path(data["players"], goal)
    print(path)
    move_players_by_path(data["players"],path)


def bfs_button_click():
    start = players[0]["position"]
    execute_bfs_solution(start, goal_position)

def print_player_list():
    # Vymazanie existujúcich tlačidiel
    for widget in button_frame.winfo_children():
        widget.destroy()
    bfs_button = tk.Button(button_frame, text="Spustiť BFS", command=bfs_button_click)
    bfs_button.pack(side="left", padx=5)
    # Vytvorenie nových tlačidiel pre každého hráča
    for i in range(len(players)):
        tk.Button(button_frame, text=f"{players[i]['color']}", command=lambda i=i: change_player_index(i)).pack(side="left")

# Zavolajte túto funkciu na začiatku na inicializáciu tlačidiel
print_player_list()

window.bind("<KeyPress>", on_key_press)

draw_elements()
window.mainloop()



#bfs_button = tk.Button(button_frame, text="Spustiť BFS", command=bfs_button_click)

