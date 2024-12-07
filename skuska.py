import tkinter as tk
import json
import time
from collections import deque

# Load configuration from JSON
with open("states.json", "r") as file:
    data = json.load(file)

GRID_SIZE = data["grid_size"]
CELL_SIZE = data["cell_size"]

# Load players and goal from JSON
players = [{"position": tuple(player["position"]), "color": player["color"]} for player in data["players"]]
goal_position = tuple(data["goal_position"])

# Initialize Tkinter window
window = tk.Tk()
window.title("Search Visualization")

canvas = tk.Canvas(window, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE)
canvas.pack()

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


def update_canvas(positions):
    """Update the canvas to reflect player positions."""
    for i, (x, y) in enumerate(positions):
        canvas.coords(
            player_ovals[i],
            y * CELL_SIZE, x * CELL_SIZE,
            (y + 1) * CELL_SIZE, (x + 1) * CELL_SIZE
        )
    window.update()


def find_path(players, goal, strategy="BFS"):
    """Generic pathfinding function for BFS or DFS."""
    if strategy == "BFS":
        queue = deque([(tuple(player["position"] for player in players), [])])
    else:  # DFS
        queue = [(tuple(player["position"] for player in players), [])]

    visited = set()
    visited.add(tuple(player["position"] for player in players))

    print(f"Starting {strategy} search...")
    print(f"Goal position: {goal}")
    print()

    while queue:
        if strategy == "BFS":
            current_positions, path = queue.popleft()
        else:  # DFS
            current_positions, path = queue.pop()

        # Print current positions
        print(f"Current positions: {current_positions}")

        if current_positions[0] == goal:
            print("\nGoal reached!")
            print(f"Path taken: {path}")
            return path

        for i, (row, col) in enumerate(current_positions):
            if (row, col) == (-1, -1):  # Skip players that are out of bounds
                continue

            directions = ["up", "down", "left", "right"]
            for direction in directions:
                new_positions = list(current_positions)
                new_row, new_col = row, col

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

                new_positions[i] = (new_row, new_col)
                new_positions_tuple = tuple(new_positions)
                if new_positions_tuple not in visited:
                    visited.add(new_positions_tuple)
                    if strategy == "BFS":
                        queue.append((new_positions_tuple, path + [(players[i]["color"], direction)]))
                    else:
                        queue.append((new_positions_tuple, path + [(players[i]["color"], direction)]))
                    print(f"Player {players[i]['color']} moved {direction} to {new_positions[i]}")
                    update_canvas(current_positions)
                    time.sleep(0.05)

    print("\nNo solution found.")
    return None


# Add buttons for searches
def bfs_search():
    path = find_path(players, goal_position, strategy="BFS")
    if path:
        print(f"\nComplete Path: {path}")
    else:
        print("\nBFS could not find a path to the goal.")


def dfs_search():
    path = find_path(players, goal_position, strategy="DFS")
    if path:
        print(f"\nComplete Path: {path}")
    else:
        print("\nDFS could not find a path to the goal.")


bfs_button = tk.Button(window, text="BFS", command=bfs_search)
bfs_button.pack(side=tk.LEFT)

dfs_button = tk.Button(window, text="DFS", command=dfs_search)
dfs_button.pack(side=tk.LEFT)

# Add placeholder buttons for future searches
placeholder_button_1 = tk.Button(window, text="Search 3", command=lambda: None)
placeholder_button_1.pack(side=tk.LEFT)

placeholder_button_2 = tk.Button(window, text="Search 4", command=lambda: None)
placeholder_button_2.pack(side=tk.LEFT)

window.mainloop()