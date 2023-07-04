from constants import width, height, square_size, blue2, rows, cols
from node import Node
import pygame


class Window:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Pathfinding Visualizer")
        self.font = pygame.font.SysFont("calibri", 15)
        self.win = pygame.display.set_mode((width, height))
        self.selected_algorithm = None
        self.speed = "Slow"
        self.paused = False
        self.previous_results = []

    def make_grid(self):
        # Made a 2D grid with rows=rows and columns-cols
        grid = []
        for i in range(rows):
            grid.append([])
            for j in range(cols):
                grid[i].append(Node(i, j))
        
        return grid

    def draw_grid(self):
        for i in range(rows + 1):
            pygame.draw.line(self.win, (0, 0, 0), (i * square_size, 0), (i * square_size, width), 1)
            pygame.draw.line(self.win, (0, 0, 0), (0, i * square_size), (width, i * square_size), 1)
    
    def draw_buttons(self):

        # A* Algorithm
        pygame.draw.rect(self.win, (0, 0, 0), (15, square_size * rows + 10, 15 * 8, 15 * 2))
        if self.selected_algorithm == "a_star":
            pygame.draw.rect(self.win, blue2, (15 + 1, square_size * rows + 11, 15 * 8 - 2, 15 * 2 - 2))
        else:
            pygame.draw.rect(self.win, (255, 255, 255), (15 + 1, square_size * rows + 11, 15 * 8 - 2, 15 * 2 - 2))
        text = self.font.render("A* Search", True, (0, 0, 0))
        self.win.blit(text, (15 * 3, square_size * (rows +1 )+ 2))

        # Greedy BFS Algorithm
        pygame.draw.rect(self.win, (0, 0, 0), (15, square_size * (rows+3), 15 * 8, 15 * 2))
        if self.selected_algorithm == "greedy_best_first_search":
            pygame.draw.rect(self.win, blue2, (15 + 1, square_size * (rows+3) + 1, 15 * 8 - 2, 15 * 2 - 2))
        else:
            pygame.draw.rect(self.win, (255, 255, 255), (15 + 1, square_size * (rows+3) + 1, 15 * 8 - 2, 15 * 2 - 2))
        text = self.font.render("Greedy Best First", True, (0, 0, 0))
        self.win.blit(text, (15 + 9, square_size * (rows+3) + 7))

        # BFS Algorithm
        pygame.draw.rect(self.win, (0, 0, 0), (15 * 19, square_size * (rows+3), 15 * 8, 15 * 2))
        if self.selected_algorithm == "breadth_first_search":
            pygame.draw.rect(self.win, blue2, (15 * 19 + 1, square_size *  (rows+3)+ 1, 15 * 8 - 2, 15 * 2 - 2))
        else:
            pygame.draw.rect(self.win, (255, 255, 255), (15 * 19 + 1, square_size * (rows+3) + 1, 15 * 8 - 2, 15 * 2 - 2))
        text = self.font.render("Breadth First", True, (0, 0, 0))
        self.win.blit(text, (15 * 20 + 6, square_size * (rows+3) + 7))

        # Dijkstra's Algorithm
        pygame.draw.rect(self.win, (0, 0, 0), (15 * 10, square_size * (rows) + 10, 15 * 8, 15 * 2))
        if self.selected_algorithm == "dijkstras":
            pygame.draw.rect(self.win, blue2, (15 * 10 + 1, square_size * rows + 11, 15 * 8 - 2, 15 * 2 - 2))
        else:
            pygame.draw.rect(self.win, (255, 255, 255), (15 * 10 + 1, square_size * rows + 11, 15 * 8 - 2, 15 * 2 - 2))
        text = self.font.render("Dijkstra's Algorithm", True, (0, 0, 0))
        self.win.blit(text, (15 * 10 + 2, square_size * (rows+1) + 2))

        # DFS Algorithm
        pygame.draw.rect(self.win, (0, 0, 0), (15 * 19, square_size * rows + 10, 15 * 8, 15 * 2))
        if self.selected_algorithm == "depth_first_search":
            pygame.draw.rect(self.win, blue2, (15 * 19 + 1, square_size * rows + 11, 15 * 8 - 2, 15 * 2 - 2))
        else:
            pygame.draw.rect(self.win, (255, 255, 255), (15 * 19 + 1, square_size * rows + 11, 15 * 8 - 2, 15 * 2 - 2))
        text = self.font.render("Depth First", True, (0, 0, 0))
        self.win.blit(text, (15 * 20 + 12, square_size * (rows+1) + 2))

        # Change Speed Button
        pygame.draw.rect(self.win, (0, 0, 0), (15 * 10, square_size * (rows+3), 15 * 8, 15 * 2))
        pygame.draw.rect(self.win, (255, 255, 255), (15 * 10 + 1, square_size * (rows+3) + 1, 15 * 8 - 2, 15 * 2 - 2))
        text = self.font.render(self.speed, True, (0, 0, 0))
        if self.speed in ("Fast", "Slow"):
            self.win.blit(text, (15 * 13 + 3, square_size * (rows+3) + 7))
        else:
            self.win.blit(text, (15 * 12 + 6, square_size * (rows+3) + 7))
    
    def draw_results(self):
        if self.previous_results:
            for i in range(len(self.previous_results)):
                text = self.font.render(self.previous_results[i], True, (0, 0, 0))
                self.win.blit(text, (15 * 27 + 10, square_size * (rows + i) + 12))

    def draw_solution(self, start, end, path, draw):
        # Total cost (sum of the weights of all nodes from start to end) of path found
        cost = 0
        end.place_end()

        # Backtracking from end node to start node and draw the path found
        current = end
        while current in path:
            if current not in (start, end):
                cost += current.weight
            current = path[current]
            current.draw_path()
            draw()

        start.place_start()
        return cost
        
    def draw(self, grid):
        self.win.fill((128, 138, 135))
        
        for row in grid:
            for node in row:
                node.draw(self.win)
                if node.weight != 1:
                    text = self.font.render("9", True, (0, 0, 0))
                    self.win.blit(text, (node.row * square_size + 4 , node.col * square_size))
        
        self.draw_grid()
        self.draw_buttons()
        self.draw_results()

        pygame.display.update()

    def get_mouse_position(self, pos):
        row = pos[0] // square_size
        col = pos[1] // square_size
        return row, col


