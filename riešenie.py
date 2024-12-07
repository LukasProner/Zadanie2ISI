import tkinter as tk
from tkinter import messagebox
import json
from collections import deque
import time
import heapq

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

button_frame = tk.Frame(window)
button_frame.pack(side="top")
# Draw grid
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        canvas.create_rectangle(
            j * CELL_SIZE, i * CELL_SIZE,
            (j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE,
            fill="white", outline="black"
        )

# Draw players and goal
player_ovals = []
for player in players:
    x, y = player["position"]
    oval = canvas.create_oval(
        y * CELL_SIZE, x * CELL_SIZE,
        (y + 1) * CELL_SIZE, (x + 1) * CELL_SIZE,
        fill=player["color"]
    )
    player_ovals.append(oval)

goal_oval = canvas.create_oval(
    goal_position[1] * CELL_SIZE, goal_position[0] * CELL_SIZE,
    (goal_position[1] + 1) * CELL_SIZE, (goal_position[0] + 1) * CELL_SIZE,
    fill="gold"
)

from collections import deque

def find_shortest_path(players, goal, search_type='bfs'):
    if search_type == 'bfs':
        queue = deque([(tuple(tuple(player["position"]) for player in players), [])])
        visited = set()
        visited.add(tuple(tuple(player["position"]) for player in players))
        all_paths = []  # Zoznam na ukladanie všetkých ciest

        while queue:
            current_positions, path = queue.popleft()

            all_paths.append(path)
            # Skontroluj, či červený hráč (hráč 1) dosiahol cieľ
            if current_positions[0] == goal:
                return path, all_paths  # Vráti optimálnu cestu a všetky prejdené cesty

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

                    if (new_row <= 0 and direction == "up") or (new_row >= GRID_SIZE-1 and direction == "down") or (new_col <= 0 and direction == "left") or (new_col >= GRID_SIZE-1 and direction == "right"):
                        new_row, new_col = -1, -1

                    # Aktualizuj pozíciu hráča
                    new_positions[i] = (new_row, new_col)

                    # Skontroluj, či sme tento stav už navštívili
                    new_positions_tuple = tuple(new_positions)
                    if new_positions_tuple not in visited:
                        visited.add(new_positions_tuple)
                        queue.append((new_positions_tuple, path + [(i, direction)]))

        return None, all_paths  # Ak červený hráč nedosiahne cieľ
    if search_type == 'dfs':
        stack = [(tuple(tuple(player["position"]) for player in players), [])]
        visited = set()
        visited.add(tuple(tuple(player["position"]) for player in players))
        all_paths = []  # Zoznam na ukladanie všetkých ciest

        while stack:
            current_positions, path = stack.pop()  # Použi pop pre DFS (LIFO)

            all_paths.append(path)
            # Skontroluj, či červený hráč (hráč 1) dosiahol cieľ
            if current_positions[0] == goal:
                return path, all_paths  # Vráti optimálnu cestu a všetky prejdené cesty

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

                    if (new_row <= 0 and direction == "up") or (
                            new_row >= GRID_SIZE - 1 and direction == "down") or (
                            new_col <= 0 and direction == "left") or (
                            new_col >= GRID_SIZE - 1 and direction == "right"):
                        new_row, new_col = -1, -1

                    new_positions[i] = (new_row, new_col)

                    new_positions_tuple = tuple(new_positions)
                    if new_positions_tuple not in visited:
                        visited.add(new_positions_tuple)
                        stack.append((new_positions_tuple, path + [(i, direction)]))

        return None, all_paths  # Ak červený hráč nedosiahne cieľ


def obstacles():
    return {player["position"] for player in players}

def update_canvas(positions):
    for i, (x, y) in enumerate(positions):
        canvas.coords(
            player_ovals[i],
            y * CELL_SIZE, x * CELL_SIZE,
            (y + 1) * CELL_SIZE, (x + 1) * CELL_SIZE
        )
    window.update()


def move_players_by_path(players, path):
    players = [{"position": tuple(player["position"]), "color": player["color"]} for player in data["players"]]
    if path is None:
        messagebox.showerror("Chyba", "Žiadna cesta neexistuje!")
        return

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

        players[player_index]["position"] = (row, col)

        update_canvas([player["position"] for player in players])

        time.sleep(0.1)

# Funkcia na vykonanie BFS a zobrazenie všetkých prejdených ciest
def execute_bfs_solution(start, goal, search_type='bfs'):
    if search_type == 'bfs':
        optimal_path, all_paths = find_shortest_path(data["players"], goal, search_type='bfs')
    elif search_type == 'dfs':
        optimal_path, all_paths = find_shortest_path(data["players"], goal, search_type='dfs')
    elif search_type == 'greedy':
        optimal_path, all_paths = greedy_search(data["players"], goal)

    print("Optimálna cesta:", optimal_path)
    print("Všetky prejdené cesty:")
    for i, p in enumerate(all_paths):
        print(f"Cesta {i + 1}: {p}")
        move_players_by_path(data["players"], p)


def greedy_search(players, goal):
    # Inicializácia prioritného radu
    priority_queue = []
    start_positions = tuple(tuple(player["position"]) for player in players)
    heapq.heappush(priority_queue, (heuristic(start_positions[0], goal), start_positions, []))

    visited = set()
    visited.add(start_positions)
    all_paths = []  # Zoznam na ukladanie všetkých ciest

    while priority_queue:
        _, current_positions, path = heapq.heappop(priority_queue)

        all_paths.append(path)
        # Skontroluj, či červený hráč (hráč 1) dosiahol cieľ
        if current_positions[0] == goal:
            return path, all_paths  # Vráti optimálnu cestu a všetky prejdené cesty

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

                if (new_row <= 0 and direction == "up") or (new_row >= GRID_SIZE - 1 and direction == "down") or (
                        new_col <= 0 and direction == "left") or (new_col >= GRID_SIZE - 1 and direction == "right"):
                    new_row, new_col = -1, -1

                # Aktualizuj pozíciu hráča
                new_positions[i] = (new_row, new_col)

                # Skontroluj, či sme tento stav už navštívili
                new_positions_tuple = tuple(new_positions)
                if new_positions_tuple not in visited:
                    visited.add(new_positions_tuple)
                    # Pridaj do prioritného radu s ohodnotením podľa heuristiky
                    heapq.heappush(priority_queue, (
                        heuristic(new_positions_tuple[0], goal),
                        new_positions_tuple,
                        path + [(i, direction)]
                    ))

    return None, all_paths  # Ak červený hráč nedosiahne cieľ


def heuristic(position, goal):
    """
    Manhattanova vzdialenosť ako heuristika.
    """
    if position == (-1, -1):  # Ak hráč už vypadol, vráti vysokú hodnotu
        return float('inf')
    return abs(position[0] - goal[0]) + abs(position[1] - goal[1])


def bfs_search():
    execute_bfs_solution(players[0]["position"], goal_position, search_type='bfs')

def dfs_search():
    execute_bfs_solution(players[0]["position"], goal_position, search_type='dfs')

def greedy():
    execute_bfs_solution(players[0]["position"], goal_position, search_type='greedy')

bfs_button = tk.Button(window, text="BFS", command=bfs_search)
bfs_button.pack(side=tk.LEFT)

dfs_button = tk.Button(window, text="DFS", command=dfs_search)
dfs_button.pack(side=tk.LEFT)

dfs_button = tk.Button(window, text="Greedy", command=greedy)
dfs_button.pack(side=tk.LEFT)

#execute_bfs_solution(players[0]["position"], goal_position, search_type='bfs')

window.mainloop()



#bfs_button = tk.Button(button_frame, text="Spustiť BFS", command=bfs_button_click)

