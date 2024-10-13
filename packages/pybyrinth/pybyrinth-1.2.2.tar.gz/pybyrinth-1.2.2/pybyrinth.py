# maze.py
__version__ = "1.2.2"
import copy  # Importamos el módulo copy para hacer copias profundas

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return not self.frontier

    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            return self.frontier.pop()

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            return self.frontier.pop(0)

class Maze:
    def __init__(self, filename):
        # Leer el archivo y configurar el laberinto
        with open(filename) as f:
            contents = f.read()

        # Validar punto de inicio y objetivo
        if contents.count("A") != 1:
            raise Exception("El laberinto debe tener exactamente un punto de inicio 'A'")
        if contents.count("B") != 1:
            raise Exception("El laberinto debe tener exactamente un punto objetivo 'B'")

        # Determinar altura y anchura
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Crear la cuadrícula de paredes
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None
        self.steps_count = 0  # Almacena el número de pasos
        self.visited_steps = []  # Almacena las celdas visitadas en la solución

    def __str__(self):
        output = []
        solution = self.solution[1] if self.solution else None
        for i, row in enumerate(self.walls):
            line = ""
            for j, col in enumerate(row):
                if col:
                    line += "█"
                elif (i, j) == self.start:
                    line += "A"
                elif (i, j) == self.goal:
                    line += "B"
                elif solution and (i, j) in solution:
                    line += "*"
                else:
                    line += " "
            output.append(line)
        return "\n".join(output)

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1)),
        ]

        result = []
        for action, (r, c) in candidates:
            if (
                0 <= r < self.height
                and 0 <= c < self.width
                and not self.walls[r][c]
            ):
                result.append((action, (r, c)))
        return result

    def solve(self, method="DFS"):
        """Encuentra una solución al laberinto usando el método especificado ('DFS' o 'BFS')."""
        # Hacer una copia profunda de la instancia actual
        copy_maze = copy.deepcopy(self)

        # Inicializar contadores y conjuntos
        copy_maze.num_explored = 0
        copy_maze.explored = set()

        # Inicializar frontera
        start_node = Node(state=copy_maze.start, parent=None, action=None)
        if method == "DFS":
            frontier = StackFrontier()
        elif method == "BFS":
            frontier = QueueFrontier()
        else:
            raise ValueError("El método debe ser 'DFS' o 'BFS'")
        frontier.add(start_node)

        while True:
            if frontier.empty():
                raise Exception("No hay solución para este laberinto")

            node = frontier.remove()
            copy_maze.num_explored += 1

            if node.state == copy_maze.goal:
                # Se encontró la solución
                actions = []
                cells = []
                while node.parent:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                copy_maze.solution = (actions, cells)
                copy_maze.steps_count = len(cells)  # Número de pasos
                copy_maze.visited_steps = cells  # Celdas visitadas
                return copy_maze  # Devolvemos la copia resuelta

            copy_maze.explored.add(node.state)

            for action, state in copy_maze.neighbors(node.state):
                if not frontier.contains_state(state) and state not in copy_maze.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
    
    def to_img(self, filename, show_solution=True, show_explored=False, label=True):
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 50
        cell_border = 2
        label_height = 100 if label else 0  # Incrementar la altura de la etiqueta
        img_width = self.width * cell_size
        img_height = self.height * cell_size + label_height
        img = Image.new(
            "RGBA", (img_width, img_height), "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution else None
        used_labels = set()  # Track which labels are used

        # Dibujar el laberinto
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    fill = (30, 30, 30)  # Color de las paredes
                    used_labels.add("Wall")
                elif (i, j) == self.start:
                    fill = (0, 171, 28)  # Color del inicio
                    used_labels.add("Start")
                elif (i, j) == self.goal:
                    fill = (255, 0, 0)  # Color del objetivo
                    used_labels.add("Goal")
                elif solution and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)  # Color del camino de la solución
                    used_labels.add("Solution")
                elif show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)  # Color de las celdas exploradas
                    used_labels.add("Explored")
                else:
                    fill = (177, 177, 177)  # Color de las celdas vacías
                    used_labels.add("Empty")

                draw.rectangle(
                    [
                        (
                            j * cell_size + cell_border,
                            i * cell_size + cell_border,
                        ),
                        (
                            (j + 1) * cell_size - cell_border,
                            (i + 1) * cell_size - cell_border,
                        ),
                    ],
                    fill=fill,
                )

        if label:
            # Definir los colores de las etiquetas y sus textos
            label_colors = {
                "Start": (0, 171, 28),
                "Goal": (255, 0, 0),
                "Wall": (177, 177, 177),
                "Solution": (220, 235, 113),
                "Explored": (212, 97, 85),
                "Empty": (30, 30, 30)
            }

            # Tamaño de fuente por defecto
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except IOError:
                font = ImageFont.load_default()

            # Dibujar las etiquetas para los elementos presentes en la imagen
            label_x = 10  # Posición x inicial para las etiquetas en la izquierda
            label_y = self.height * cell_size + 10  # Posición y inicial debajo del laberinto

            for idx, (text, color) in enumerate(label_colors.items()):
                if text in used_labels and text not in ["Solution", "Explored"]:
                    draw.rectangle(
                        [
                            (label_x, label_y + idx * 22),
                            (label_x + 20, label_y + idx * 22 + 20)
                        ],
                        fill=color
                    )
                    draw.text((label_x + 30, label_y + idx * 22), text, fill="white", font=font)

            # Dibujar las etiquetas de "Solution" y "Explored" en el lado derecho de la imagen
            right_label_x = img_width - 180  # Posición más alejada del borde derecho
            right_label_y = self.height * cell_size + 10

            if "Solution" in used_labels:
                draw.text((right_label_x, right_label_y), "Solution", fill="white", font=font)
                draw.rectangle(
                    [
                        (right_label_x + 100, right_label_y),
                        (right_label_x + 120, right_label_y + 20)
                    ],
                    fill=label_colors["Solution"]
                )
                right_label_y += 30  # Mover hacia abajo para la siguiente etiqueta

            if "Explored" in used_labels:
                draw.text((right_label_x, right_label_y), "Explored", fill="white", font=font)
                draw.rectangle(
                    [
                        (right_label_x + 100, right_label_y),
                        (right_label_x + 120, right_label_y + 20)
                    ],
                    fill=label_colors["Explored"]
                )

        img.save(filename)


    def info(self):
        """Devuelve la información sobre el número de pasos en la solución."""
        if self.solution is None:
            return "El laberinto no ha sido resuelto aún."
        return f"Número de pasos para resolver el laberinto: {self.steps_count}"

    def steps(self):
        """Devuelve una lista de las casillas visitadas en la solución."""
        if self.solution is None:
            return "El laberinto no ha sido resuelto aún."
        return self.visited_steps
    
    def show(self, title="Maze", label=False):
        """Visualiza el laberinto utilizando Matplotlib, con la leyenda opcional fuera del gráfico en la esquina superior derecha."""
        import numpy as np
        import matplotlib.pyplot as plt
        from matplotlib.colors import ListedColormap

        rows = self.height
        cols = self.width
        maze_image = np.ones((rows, cols))  # Creamos una matriz para representar el laberinto (1 para paredes)

        # Llenar la matriz con información del laberinto
        for y, row in enumerate(self.walls):
            for x, is_wall in enumerate(row):
                if not is_wall:
                    maze_image[y, x] = 0  # Asignamos 0 a los caminos (negro)

        # Poner el inicio (A) en verde
        start_y, start_x = self.start
        maze_image[start_y, start_x] = 0.5  # Asignamos un valor intermedio para diferenciar

        # Poner el objetivo (B) en rojo
        goal_y, goal_x = self.goal
        maze_image[goal_y, goal_x] = 0.75  # Otro valor intermedio para diferenciar

        # Mostrar la solución si está disponible
        if self.solution:
            solution_path = self.solution[1]  # Obtener la lista de celdas en la solución
            for (y, x) in solution_path:
                maze_image[y, x] = 0.25  # Asignar un valor específico para el camino de la solución

        # Crear un mapa de colores personalizado
        cmap = ListedColormap(['white', 'yellow', 'green', 'red', 'black'])

        # Crear la figura y los ejes para el laberinto
        fig, ax = plt.subplots(figsize=(cols * 0.5, rows * 0.5))  # Ajustar el tamaño de la figura según el laberinto
        ax.imshow(maze_image, cmap=cmap, origin="upper", vmin=0, vmax=1)

        # Añadir marcadores de colores para el inicio y final
        ax.scatter(start_x, start_y, color='green', label='Start (A)', s=100, marker='o')  # Verde para el inicio
        ax.scatter(goal_x, goal_y, color='red', label='Goal (B)', s=100, marker='o')  # Rojo para el objetivo

        # Eliminar marcas de los ejes y poner título
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title)

        if label:
            # Ajustar los márgenes para hacer espacio para la leyenda fuera del gráfico
            plt.subplots_adjust(right=0.75)  # Dejar espacio a la derecha

            # Configurar la leyenda fuera del gráfico en la esquina superior derecha
            ax.legend(
                handles=[
                    plt.Line2D([0], [0], marker='o', color='w', label='Start (A)', markerfacecolor='green', markersize=10),
                    plt.Line2D([0], [0], marker='o', color='w', label='Goal (B)', markerfacecolor='red', markersize=10),
                    plt.Line2D([0], [0], color='white', lw=4, label='Path (white)'),
                    plt.Line2D([0], [0], color='black', lw=4, label='Wall (black)'),
                    plt.Line2D([0], [0], color='yellow', lw=4, label='Solution (yellow)')  # Añadir solución a la leyenda
                ],
                loc='center left',
                bbox_to_anchor=(1.05, 0.5),  # Posicionar la leyenda completamente fuera del área del gráfico
                borderaxespad=0,  # Sin espacio adicional entre el gráfico y la leyenda
                frameon=True  # Mostrar el recuadro alrededor de la leyenda
            )

        plt.show()



    def __repr__(self):
        """Muestra una representación visual del laberinto al evaluar la variable en una celda de Jupyter."""
        self.show(label=True)  # Llamar a show con label=True para mostrar la leyenda
        return ""


def read(filepath):
    return Maze(filepath)


import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

def create(x=6, y=6, start='A', end='B', wall='#', empty=' '):
    """
    Create a maze interactively using a graphical interface.
    :param x: Width of the maze
    :param y: Height of the maze
    :param start: Character for the start position
    :param end: Character for the end position
    :param wall: Character for the walls
    :param empty: Character for empty spaces
    :return: Saves the maze as a .txt file
    """

    class MazeCreator:
        def __init__(self, x, y, start_char, end_char, wall_char, empty_char):
            self.root = tk.Tk()
            self.root.title("Maze Creator")
            self.x = x
            self.y = y
            self.start_char = start_char
            self.end_char = end_char
            self.wall_char = wall_char
            self.empty_char = empty_char
            self.start_pos = None
            self.end_pos = None
            self.grid = [[0 for _ in range(x)] for _ in range(y)]
            self.buttons = [[None for _ in range(x)] for _ in range(y)]
            self.current_tool = "wall"  # Default mode is wall
            self.create_widgets()

            # Set window to be on top
            self.root.attributes('-topmost', True)
            self.root.update()

        def create_widgets(self):
            # Frame for the maze grid with padding (margin around the grid)
            maze_frame = tk.Frame(self.root, padx=20, pady=20, bg='#f0f0f0')  # Background to make it modern
            maze_frame.pack()

            for i in range(self.y):
                for j in range(self.x):
                    btn = tk.Button(maze_frame, width=2, height=1, command=lambda i=i, j=j: self.on_cell_click(i, j))
                    btn.grid(row=i, column=j)
                    self.buttons[i][j] = btn

            # Frame for the controls with padding to create some space
            control_frame = tk.Frame(self.root, padx=20, pady=20, bg='#f0f0f0')
            control_frame.pack()

            # Styling for modern buttons (neutral colors, rounded corners)
            button_style = {
                "bg": "#E0E0E0",  # Light gray for a modern neutral look
                "fg": "black",  # Black text color
                "font": ("Segoe UI", 10),  # Font similar to Windows 11
                "bd": 0,  # No border
                "activebackground": "#C0C0C0",  # Slightly darker gray when clicked
                "relief": "flat",  # Flat style for modern look
                "padx": 10,  # Padding inside the button for more space
                "pady": 5
            }

            # Buttons to select start and end points with modern styling
            self.start_button = tk.Button(control_frame, text="Select Start", command=self.set_start_tool, **button_style)
            self.start_button.grid(row=0, column=0, padx=10, pady=10)

            self.end_button = tk.Button(control_frame, text="Select End", command=self.set_end_tool, **button_style)
            self.end_button.grid(row=0, column=1, padx=10, pady=10)

            # Button to save the maze with modern styling
            save_button = tk.Button(self.root, text="Save Maze", command=self.save_maze_as_txt, **button_style)
            save_button.pack(padx=20, pady=5)  # Adjusted padding to 5 to move it up

        def set_start_tool(self):
            self.current_tool = "start"
            self.highlight_button(self.start_button)
            self.unhighlight_button(self.end_button)

        def set_end_tool(self):
            self.current_tool = "end"
            self.highlight_button(self.end_button)
            self.unhighlight_button(self.start_button)

        def highlight_button(self, button):
            button.config(bg="lightgray")  # Highlight the selected button

        def unhighlight_button(self, button):
            button.config(bg="#E0E0E0")  # Reset the button to its neutral color

        def set_wall_tool(self):
            self.current_tool = "wall"
            # Reset button colors when returning to wall mode
            self.unhighlight_button(self.start_button)
            self.unhighlight_button(self.end_button)

        def on_cell_click(self, i, j):
            if self.current_tool == "start":
                if self.start_pos:
                    prev_i, prev_j = self.start_pos
                    self.buttons[prev_i][prev_j].config(bg="SystemButtonFace")
                self.start_pos = (i, j)
                self.buttons[i][j].config(bg="green")
                self.grid[i][j] = 0
                # Automatically return to wall mode
                self.set_wall_tool()
            elif self.current_tool == "end":
                if self.end_pos:
                    prev_i, prev_j = self.end_pos
                    self.buttons[prev_i][prev_j].config(bg="SystemButtonFace")
                self.end_pos = (i, j)
                self.buttons[i][j].config(bg="red")
                self.grid[i][j] = 0
                # Automatically return to wall mode
                self.set_wall_tool()
            elif self.current_tool == "wall":
                if (i, j) != self.start_pos and (i, j) != self.end_pos:
                    current_color = self.buttons[i][j].cget("bg")
                    if current_color == "black":
                        self.buttons[i][j].config(bg="SystemButtonFace")
                        self.grid[i][j] = 0
                    else:
                        self.buttons[i][j].config(bg="black")
                        self.grid[i][j] = 1

        def generate_maze_str(self):
            maze_lines = []
            for i, row in enumerate(self.grid):
                line = ""
                for j, cell in enumerate(row):
                    if (i, j) == self.start_pos:
                        line += self.start_char
                    elif (i, j) == self.end_pos:
                        line += self.end_char
                    elif cell == 1:  # Wall
                        line += self.wall_char
                    else:  # Empty space
                        line += self.empty_char
                maze_lines.append(line)
            return "\n".join(maze_lines)

        def save_maze_as_txt(self):
            if not self.start_pos or not self.end_pos:
                messagebox.showwarning("Warning", "You must select a start and an end position.")
                return
            maze_str = self.generate_maze_str()

            # Get the directory of the current script
            current_directory = os.path.dirname(os.path.abspath(__file__))

            # Open file dialog to save the maze, defaulting to the script's directory
            file_path = filedialog.asksaveasfilename(initialdir=current_directory,
                                                     defaultextension=".txt",
                                                     filetypes=[("Text files", "*.txt")])
            if file_path:
                with open(file_path, "w") as f:
                    f.write(maze_str)
                print(f"Maze saved successfully to {file_path}.")
                self.root.destroy()

        def run(self):
            self.root.mainloop()

    maze_creator = MazeCreator(x, y, start, end, wall, empty)
    maze_creator.run()