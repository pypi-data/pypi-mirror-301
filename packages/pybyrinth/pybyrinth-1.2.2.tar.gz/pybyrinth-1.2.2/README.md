
# Maze Solver Documentation

## Descripción

Esta biblioteca permite crear, resolver y visualizar laberintos. Incluye métodos para cargar un laberinto desde un archivo, resolverlo utilizando algoritmos como DFS (Depth-First Search) y BFS (Breadth-First Search), y visualizar tanto el laberinto original como el resuelto.

## Instalación

Para instalar las dependencias necesarias, ejecuta el siguiente comando:

```bash
pip install -r requirements.txt
```

## Uso

### Leer un laberinto desde un archivo

```python
import maze

# Leer el laberinto
maze_instance = maze.read("ruta/al/archivo/maze.txt")
maze_instance.show(title="Maze Original", label=True)
```

### Resolver el laberinto

```python
# Resolver el laberinto usando DFS
solved_maze = maze_instance.solve(method="DFS")

# Mostrar el laberinto resuelto
solved_maze.show(title="Solved Maze (DFS)", label=True)
```

### Obtener información sobre la solución

```python
# Número de pasos
print(solved_maze.info())

# Pasos del camino resuelto
print(solved_maze.steps())
```

## Requisitos

Para utilizar la biblioteca, asegúrate de tener instaladas las siguientes dependencias:

- `numpy==1.23.5`
- `matplotlib==3.6.2`

Estas dependencias se pueden instalar ejecutando:

```bash
pip install -r requirements.txt
```

## Créditos

Desarrollado por: Pablo Álvaro Hidalgo
