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
    draw_grid()

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

def print_player_list():
    # Vymazanie existujúcich tlačidiel
    for widget in button_frame.winfo_children():
        widget.destroy()

    # Vytvorenie nových tlačidiel pre každého hráča
    for i in range(len(players)):
        tk.Button(button_frame, text=f"{players[i]['color']}", command=lambda i=i: change_player_index(i)).pack(side="left")

# Zavolajte túto funkciu na začiatku na inicializáciu tlačidiel
print_player_list()

window.bind("<KeyPress>", on_key_press)

draw_elements()
window.mainloop()

def find_path_bfs(start, goal):
    queue = deque([(start, [])])
    visited = set()
    visited.add(start)

    while queue:
        (current, path) = queue.popleft()

        if current == goal:
            return path

        row, col = current
        neighbors = [
            (row - 1, col), (row + 1, col),
            (row, col - 1), (row, col + 1)
        ]

        for neighbor in neighbors:
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE:
                if neighbor not in visited and neighbor not in obstacles():
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

    return None