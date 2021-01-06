import pygame
from collections import deque
import heapq


vec = pygame.math.Vector2

TILE = 20
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
PATH_COLOR = (90, 245, 7)
WALL_COLOR = (252, 250, 254)
VISITED_COLOR = (204, 51, 255)
CURRENT_COLOR = (8, 243, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (211, 211, 211)
DARK_GRAY = (28, 8, 44)
START_COLOR = (211, 171, 237)
fps = 30
goal_node = None

start_node = None
pygame.init()
win = pygame.display.set_mode((WIDTH + 350, HEIGHT))
clock = pygame.time.Clock()



class block:
    def __init__(self, tile, width, height):
        self.width = width
        self.height = height
        self.tilesize = tile
        self.wall = []
        self.connections = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1)]
        self.weights = {}

    def drow_wall(self):
        for i in self.wall:
            pygame.draw.rect(win, (GRAY), (i.x * TILE + 2, i.y * TILE + 2, TILE - 3, TILE - 3), 0)

    def drow_block(self, node, color):
        pygame.draw.rect(win, (color), (node.x * TILE + 2, node.y * TILE + 2, TILE - 3, TILE - 3), 0)

    def in_bounds(self, node):
        return 0 <= node.x < WIDTH / TILE and 0 <= node.y < HEIGHT / TILE

    def possible(self, node):
        return node not in self.wall

    def check_neighbors(self, node):
        neighbors = [node + connection for connection in self.connections]
        #if (node.x + node.y) % 2:
        #   neighbors.reverse()
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.possible, neighbors)
        return neighbors

    def cost(self, from_node, to_node):
        if (vec(to_node) - vec(from_node)).length_squared() == 1:
            return self.weights.get(to_node, 0) + 10
        else:
            return self.weights.get(to_node, 0) + 14


class PriorityQueue:
    def __init__(self):
        self.nodes = []

    def put(self, node, cost):
        heapq.heappush(self.nodes, (cost, node))

    def get(self):
        return heapq.heappop(self.nodes)[1]

    def empty(self):
        return len(self.nodes) == 0


def vec2int(node):
    return (int(node.x), int(node.y))


def heuristic(node1, node2):
    return (abs(node1.x - node2.x) + abs(node1.y - node2.y)) * 10


def drow_grid(win):
    for i in range(0, WIDTH, TILE):
        pygame.draw.line(win, (220, 220, 220), (i, 0), (i, HEIGHT), 1)
        for j in range(0, HEIGHT, TILE):
            pygame.draw.line(win, (220, 220, 220), (0, j), (WIDTH, j), 1)


def text_object(text, font):
    textSurface = font.render(text,True, BLACK)
    return textSurface, textSurface.get_rect()




mouse_position = []
run = True
B = block(TILE, WIDTH, HEIGHT)
front = deque()
visited = []
path = {}
bfs = False
bfs2 = False
done = False
running_algo = False
font = pygame.font.Font('freesansbold.ttf', 40)
small_font = pygame.font.Font('freesansbold.ttf', 20)
text = font.render('Can not find GOAL', True, GREEN, BLACK)
maze1 = [[6, 0],[7, 0],[8, 0],[9, 0],[10, 0],[11, 0],[12, 0],[13, 0],[14, 0],[15, 0],[16, 0],[17, 0],[18, 0],[19, 0],[20, 0],[21, 0],[22, 0],[23, 0],[24, 0],[25, 0],[26, 0],[27, 0],[28, 0],[29, 0],[30, 0],[31, 0],[32, 0],[33, 0],[34, 0],[35, 0],[36, 0],[37, 0],[38, 0],[39, 0],[35, 1],[35, 2],[35, 3],[35, 4],[35, 5],[35, 6],[35, 7],[38, 12],[37, 12],[36, 12],[35, 12],[32, 12],[32, 11],[32, 10],[32, 9],[32, 8],[31, 8],[30, 8],[29, 8],[28, 8],[27, 8],[26, 8],[25, 8],[24, 8],[23, 8],[22, 8],[21, 8],[21, 7],[21, 6],[21, 5],[20, 5],[19, 5],[18, 5],[17, 5],[16, 5],[16, 4],[16, 3],[16, 6],[16, 7],[16, 8],[16, 9],[16, 10],[16, 11],[15, 11],[14, 11],[13, 11],[12, 11],[11, 11],[10, 11],[9, 11],[8, 11],[7, 11],[16, 12],[16, 13],[16, 14],[16, 15],[15, 15],[14, 15],[13, 15],[11, 15],[10, 15],[9, 15],[5, 15],[4, 15],[3, 15],[2, 15],[2, 14],[2, 13],[2, 12],[3, 12],[3, 11],[3, 10],[3, 9],[3, 8],[2, 7],[2, 6],[3, 6],[4, 6],[5, 6],[6, 6],[7, 6],[8, 6],[9, 6],[10, 6],[10, 5],[11, 5],[12, 5],[8, 15],[7, 15],[6, 15],[12, 15],[17, 15],[18, 15],[19, 15],[20, 15],[21, 15],[22, 15],[23, 15],[24, 15],[25, 15],[25, 16],[25, 17],[25, 18],[25, 19],[25, 20],[25, 21],[25, 22],[25, 23],[25, 24],[24, 24],[23, 24],[22, 24],[21, 24],[20, 24],[19, 24],[18, 24],[17, 24],[16, 24],[21, 25],[21, 26],[21, 27],[21, 28],[16, 23],[16, 22],[16, 21],[16, 20],[17, 20],[18, 20],[19, 20],[20, 20],[21, 20],[22, 20],[15, 20],[14, 20],[13, 20],[12, 20],[11, 20],[10, 20],[9, 20],[8, 20],[7, 20],[6, 20],[5, 20],[4, 20],[3, 20],[2, 20],[7, 21],[7, 22],[7, 23],[7, 24],[7, 25],[8, 25],[9, 25],[10, 25],[11, 25],[11, 24],[11, 23],[9, 28],[10, 28],[11, 28],[12, 28],[13, 28],[14, 28],[14, 27],[14, 26],[14, 25],[14, 24],[14, 23],[14, 29],[0, 26],[1, 26],[2, 26],[3, 26],[4, 26],[4, 27],[4, 28],[4, 25],[4, 24],[4, 23],[18, 17],[18, 18],[18, 19],[12, 3],[12, 4],[27, 1],[27, 2],[27, 3],[27, 4],[26, 3],[25, 3],[24, 3],[23, 3],[22, 3],[21, 3],[20, 3],[27, 5],[27, 6],[28, 6],[29, 6],[30, 6],[31, 6],[32, 6],[32, 13],[32, 14],[32, 15],[32, 16],[32, 19],[32, 20],[32, 21],[32, 23],[31, 23],[30, 23],[29, 23],[29, 22],[29, 21],[29, 20],[29, 19],[29, 18],[33, 23],[34, 23],[35, 23],[36, 23],[37, 23],[34, 24],[34, 25],[34, 26],[34, 27],[34, 28],[29, 26],[29, 27],[29, 28],[29, 29],[6, 0],[7, 0],[8, 0],[9, 0],[10, 0],[11, 0],[12, 0],[13, 0],[14, 0],[15, 0],[16, 0],[17, 0],[18, 0],[19, 0],[20, 0],[21, 0],[22, 0],[23, 0],[24, 0],[25, 0],[26, 0],[27, 0],[28, 0],[29, 0],[30, 0],[31, 0],[32, 0],[33, 0],[34, 0],[35, 0],[36, 0],[37, 0],[38, 0],[39, 0],[35, 1],[35, 2],[35, 3],[35, 4],[35, 5],[35, 6],[35, 7],[38, 12],[37, 12],[36, 12],[35, 12],[34, 12],[33, 12],[32, 12],[32, 11],[32, 10],[32, 9],[32, 8],[31, 8],[30, 8],[29, 8],[28, 8],[27, 8],[26, 8],[25, 8],[24, 8],[23, 8],[22, 8],[21, 8],[21, 7],[21, 6],[21, 5],[20, 5],[19, 5],[18, 5],[17, 5],[16, 5],[16, 4],[16, 3],[16, 6],[16, 7],[16, 8],[16, 9],[16, 10],[16, 11],[15, 11],[14, 11],[13, 11],[12, 11],[11, 11],[10, 11],[9, 11],[8, 11],[7, 11],[16, 12],[16, 13],[16, 14],[16, 15],[15, 15],[14, 15],[13, 15],[11, 15],[10, 15],[9, 15],[5, 15],[4, 15],[3, 15],[2, 15],[2, 14],[2, 13],[2, 12],[3, 12],[3, 11],[3, 10],[3, 9],[3, 8],[2, 7],[2, 6],[3, 6],[4, 6],[5, 6],[6, 6],[7, 6],[8, 6],[9, 6],[10, 6],[10, 5],[11, 5],[12, 5],[8, 15],[7, 15],[6, 15],[12, 15],[17, 15],[18, 15],[19, 15],[20, 15],[21, 15],[22, 15],[23, 15],[24, 15],[25, 15],[25, 16],[25, 17],[25, 18],[25, 19],[25, 20],[25, 21],[25, 22],[25, 23],[25, 24],[24, 24],[23, 24],[22, 24],[21, 24],[20, 24],[19, 24],[18, 24],[17, 24],[16, 24],[21, 25],[21, 26],[21, 27],[21, 28],[16, 23],[16, 22],[16, 21],[16, 20],[17, 20],[18, 20],[19, 20],[20, 20],[21, 20],[22, 20],[15, 20],[14, 20],[13, 20],[12, 20],[11, 20],[10, 20],[9, 20],[8, 20],[7, 20],[6, 20],[5, 20],[4, 20],[3, 20],[2, 20],[7, 21],[7, 22],[7, 23],[7, 24],[7, 25],[8, 25],[9, 25],[10, 25],[11, 25],[11, 24],[11, 23],[9, 28],[10, 28],[11, 28],[12, 28],[13, 28],[14, 28],[14, 27],[14, 26],[14, 25],[14, 24],[14, 23],[14, 29],[0, 26],[1, 26],[2, 26],[3, 26],[4, 26],[4, 27],[4, 28],[4, 25],[4, 24],[4, 23],[18, 17],[18, 18],[18, 19],[12, 3],[12, 4],[27, 1],[27, 2],[27, 3],[27, 4],[26, 3],[25, 3],[24, 3],[23, 3],[22, 3],[21, 3],[20, 3],[27, 5],[27, 6],[28, 6],[29, 6],[30, 6],[31, 6],[32, 6],[32, 13],[32, 14],[32, 15],[32, 16],[32, 19],[32, 20],[32, 21],[32, 23],[31, 23],[30, 23],[29, 23],[29, 22],[29, 21],[29, 20],[29, 19],[29, 18],[33, 23],[34, 23],[35, 23],[36, 23],[37, 23],[34, 24],[34, 25],[34, 26],[34, 27],[34, 28],[29, 26],[29, 27],[29, 28],[29, 29],[6, 0],[7, 0],[8, 0],[9, 0],[10, 0],[11, 0],[12, 0],[13, 0],[14, 0],[15, 0],[16, 0],[17, 0],[18, 0],[19, 0],[20, 0],[21, 0],[22, 0],[23, 0],[24, 0],[25, 0],[26, 0],[27, 0],[28, 0],[29, 0],[30, 0],[31, 0],[32, 0],[33, 0],[34, 0],[35, 0],[36, 0],[37, 0],[38, 0],[39, 0],[35, 1],[35, 2],[35, 3],[35, 4],[35, 5],[35, 6],[35, 7],[38, 12],[37, 12],[36, 12],[35, 12],[34, 12],[33, 12],[32, 12],[32, 11],[32, 10],[32, 9],[32, 8],[31, 8],[30, 8],[29, 8],[28, 8],[27, 8],[26, 8],[25, 8],[24, 8],[23, 8],[22, 8],[21, 8],[21, 7],[21, 6],[21, 5],[20, 5],[19, 5],[18, 5],[17, 5],[16, 5],[16, 4],[16, 3],[16, 6],[16, 7],[16, 8],[16, 9],[16, 10],[16, 11],[15, 11],[14, 11],[13, 11],[12, 11],[11, 11],[10, 11],[9, 11],[8, 11],[7, 11],[16, 12],[16, 13],[16, 14],[16, 15],[15, 15],[14, 15],[13, 15],[11, 15],[10, 15],[9, 15],[5, 15],[4, 15],[3, 15],[2, 15],[2, 14],[2, 13],[2, 12],[3, 12],[3, 11],[3, 10],[3, 9],[3, 8],[2, 7],[2, 6],[3, 6],[4, 6],[5, 6],[6, 6],[7, 6],[8, 6],[9, 6],[10, 6],[10, 5],[11, 5],[12, 5],[8, 15],[7, 15],[6, 15],[12, 15],[17, 15],[18, 15],[19, 15],[20, 15],[21, 15],[22, 15],[23, 15],[24, 15],[25, 15],[25, 16],[25, 17],[25, 18],[25, 19],[25, 20],[25, 21],[25, 22],[25, 23],[25, 24],[24, 24],[23, 24],[22, 24],[21, 24],[20, 24],[19, 24],[18, 24],[17, 24],[16, 24],[21, 25],[21, 26],[21, 27],[21, 28],[16, 23],[16, 22],[16, 21],[16, 20],[17, 20],[18, 20],[19, 20],[20, 20],[21, 20],[22, 20],[15, 20],[14, 20],[13, 20],[12, 20],[11, 20],[10, 20],[9, 20],[8, 20],[7, 20],[6, 20],[5, 20],[4, 20],[3, 20],[2, 20],[7, 21],[7, 22],[7, 23],[7, 24],[7, 25],[8, 25],[9, 25],[10, 25],[11, 25],[11, 24],[11, 23],[9, 28],[10, 28],[11, 28],[12, 28],[13, 28],[14, 28],[14, 27],[14, 26],[14, 25],[14, 24],[14, 23],[14, 29],[0, 26],[1, 26],[2, 26],[3, 26],[4, 26],[4, 27],[4, 28],[4, 25],[4, 24],[4, 23],[18, 17],[18, 18],[18, 19],[12, 3],[12, 4],[27, 1],[27, 2],[27, 3],[27, 4],[26, 3],[25, 3],[24, 3],[23, 3],[22, 3],[21, 3],[20, 3],[27, 5],[27, 6],[28, 6],[29, 6],[30, 6],[31, 6],[32, 6],[32, 13],[32, 14],[32, 15],[32, 16],[32, 18],[32, 19],[32, 20],[32, 21],[32, 23],[31, 23],[30, 23],[29, 23],[29, 22],[29, 21],[29, 20],[29, 19],[29, 18],[33, 23],[34, 23],[35, 23],[36, 23],[37, 23],[34, 24],[34, 25],[34, 26],[34, 27],[34, 28],[29, 26],[29, 27],[29, 28],[29, 29],[32, 17],[29, 17],[29, 16],[29, 15],[29, 14],[29, 13],[29, 12],[30, 12]]
textRect = text.get_rect()

textRect.center = (WIDTH // 2, HEIGHT // 2)
text_Show = False
astar = False
astar2 = False
dijkstra = False
dijkstra2 = False
done_astar = False
done_dij = False
current_d = None
path_d = {}
front_d_show = []
path_disjksta = {}
start_algo = False
while run:
    win.fill(BLACK)

    #maze
    pygame.draw.rect(win, (220, 220, 220), (900, 40, 150, 70))
    textSurfece, textrect = text_object("Maze", small_font)
    textrect.center = ((900 + (150 / 2)), (40 + (70 / 2)))
    win.blit(textSurfece, textrect)

    #a* button
    pygame.draw.rect(win, (220, 220, 220), (900, 150,150,70 ))
    textSurfece, textrect = text_object("A* search", small_font)
    textrect.center = ((900+(150/2)), (150+(70/2)))
    win.blit(textSurfece,textrect)
    #BFS
    pygame.draw.rect(win, (220, 220, 220), (900, 270, 150, 70))
    textSurfece, textrect = text_object("BFS", small_font)
    textrect.center = ((900 + (150 / 2)), (270 + (70 / 2)))
    win.blit(textSurfece, textrect)
    # Dijkstra
    pygame.draw.rect(win, (220, 220, 220), (900, 390, 150, 70))
    textSurfece, textrect = text_object("Dijkstrea", small_font)
    textrect.center = ((900 + (150 / 2)), (390 + (70 / 2)))
    win.blit(textSurfece, textrect)

    # Dijkstra
    pygame.draw.rect(win, (220, 220, 220), (900, 390, 150, 70))
    textSurfece, textrect = text_object("Dijkstrea", small_font)
    textrect.center = ((900 + (150 / 2)), (390 + (70 / 2)))
    win.blit(textSurfece, textrect)

    #clear button
    pygame.draw.rect(win, (220, 220, 220), (900, 510, 150, 70))
    textSurfece, textrect = text_object("Clear", small_font)
    textrect.center = ((900 + (150 / 2)), (510 + (70 / 2)))
    win.blit(textSurfece, textrect)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x >= WIDTH:
            mouse_position = pygame.mouse.get_pos()
            #print(mouse_position)
            if (900 <= mouse_x <= 900+150 and 40 <= mouse_y <=(40+70)):
                if(pygame.mouse.get_pressed()[0]):
                    for element in maze1:
                        temp = vec(element)
                        B.wall.append(temp)
            # A* button
            if (900 <= mouse_x <= 900+150 and 150 <= mouse_y <=(150+70)):
                if(pygame.mouse.get_pressed()[0] and not running_algo):
                    astar = True
                    running_algo = True
            #bfs button
            if (900 <= mouse_x <= 900+150 and 270 <= mouse_y <=(270+70)):
                if(pygame.mouse.get_pressed()[0] and not running_algo):
                    bfs = True
                    running_algo = True

            #dijkstra
            if (900 <= mouse_x <= 900+150 and 390 <= mouse_y <=(390+70)):
                if(pygame.mouse.get_pressed()[0] and not running_algo):
                    dijkstra = True
                    running_algo = True
            #clear button
            if (900 <= mouse_x <= 900+150 and 510 <= mouse_y <=(510+70)):
                if(pygame.mouse.get_pressed()[0]):
                    visited.clear()
                    front.clear()
                    text_Show = False
                    astar = False
                    astar2 = False
                    dijkstra = False
                    dijkstra2 = False
                    done_astar = False
                    done = False
                    done_dij = False
                    current_d = None
                    path_d.clear()
                    front_d_show.clear()
                    path_disjksta.clear()
                    running_algo = False






        else:
            if pygame.mouse.get_pressed()[0] and not running_algo:
                mouse_position = vec(pygame.mouse.get_pos()) // TILE
                if not start_node and mouse_position != goal_node:
                    start_node = mouse_position
                    # vec2int(start_node)

                elif not goal_node and mouse_position != start_node:
                    goal_node = mouse_position
                elif mouse_position != start_node and mouse_position != goal_node and mouse_position not in B.wall:
                    B.wall.append(mouse_position)

            elif pygame.mouse.get_pressed()[2] and not running_algo:
                mouse_position = vec(pygame.mouse.get_pos()) // TILE
                # print(mouse_position)
                if mouse_position in B.wall:
                    B.wall.remove(mouse_position)
                    # print(mouse_position)
                    # print(B.wall)
                if mouse_position == start_node:
                    start_node = None
                if mouse_position == goal_node:
                    goal_node = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    for element in B.wall:
                        print(element, end=",")
            #    if event.key == pygame.K_SPACE:
            #        bfs = True
            #        running_algo = True
                #elif event.key == pygame.K_d:
                 #   digksta = True
                    # path_disjksta = dijkstra_algo(B, start_node, goal_node)
                    # print(path_disjksta)

    if bfs:
        front.append(start_node)
        visited.append(start_node)
        path[vec2int(start_node)] = None
        bfs2 = True
    if bfs2 and not done:
        bfs = False
        if len(front) > 0:
            current = front.popleft()
            if current == goal_node:
                done = True

            for next_node in B.check_neighbors(current):
                if next_node not in visited:
                    visited.append(next_node)
                    front.append(next_node)
                    path[vec2int(next_node)] = current - next_node
                    # B.drow_block(next_node, VISITED_COLOR)
            if len(front) == 0 and current == goal_node:
                done = True

            if len(front) == 0 and current != 0:
                text_Show = True

    if astar:
        front_astar = PriorityQueue()
        front_d_show.append(start_node)
        front_astar.put(vec2int(start_node), 0)
        path_d = {}
        cost_d = {}
        path_d[vec2int(start_node)] = None
        cost_d[vec2int(start_node)] = 0
        astar2 = True

    if astar2 and not done_astar:
        astar = False
        if front_astar.empty() == False:
            current_d = front_astar.get()
            front_d_show.remove(current_d)

            if current_d == goal_node:
                done_astar = True
            else:
                for next_d in B.check_neighbors(vec(current_d)):
                    next_d = vec2int(next_d)

                    next_cost = cost_d[current_d] + B.cost(current_d, next_d)
                    if next_d not in cost_d or next_cost < cost_d[next_d]:
                        cost_d[next_d] = next_cost
                        # property = next_cost
                        property = heuristic(goal_node, vec(next_d))
                        front_astar.put(next_d, property)
                        front_d_show.append(next_d)
                        path_d[next_d] = vec(current_d) - vec(next_d)

        if front_astar.empty() and current_d == goal_node:
            done_astar = True
            astar2 = False
        if front_astar.empty() and current_d != 0 and current_d != goal_node:
            text_Show = True



    if dijkstra:
        front_dijkstra = PriorityQueue()
        front_d_show.append(start_node)
        front_dijkstra.put(vec2int(start_node), 0)
        path_d = {}
        cost_d = {}
        path_d[vec2int(start_node)] = None
        cost_d[vec2int(start_node)] = 0
        dijkstra2 = True



    if dijkstra2 and not done_dij:
        dijkstra = False
        if front_dijkstra.empty() == False:
            current_d = front_dijkstra.get()
            front_d_show.remove(current_d)

            if current_d == goal_node:
                done_dij = True
            else:
                for next_d in B.check_neighbors(vec(current_d)):
                    next_d = vec2int(next_d)

                    next_cost = cost_d[current_d] + B.cost(current_d, next_d)
                    if next_d not in cost_d or next_cost < cost_d[next_d]:
                        cost_d[next_d] = next_cost
                        property = next_cost
                        front_dijkstra.put(next_d, property)
                        front_d_show.append(next_d)
                        path_d[next_d] = vec(current_d) - vec(next_d)

        if front_dijkstra.empty():
            done_dij = True
            digkstra2 = False


    for i in visited:
        B.drow_block(i, VISITED_COLOR)
    if len(front) > 0:
        for i in front:
            B.drow_block(i, CURRENT_COLOR)

    if len(path_d) > 0:
        for i in path_d:
            B.drow_block(vec(i), VISITED_COLOR)

    if len(front_d_show) > 0:
        for i in front_d_show:
            B.drow_block(vec(i), CURRENT_COLOR)

    if done:
        current = goal_node
        while current != start_node:
            B.drow_block(current, YELLOW)
            current = current + path[vec2int(current)]

    if done_astar:
        current = goal_node
        while current != start_node:
            B.drow_block(current, YELLOW)
            current = current + path_d[vec2int(current)]

    if done_dij:
        current = goal_node
        while current != start_node:
            B.drow_block(current, YELLOW)
            current = current + path_d[vec2int(current)]

    drow_grid(win)
    if start_node != None:
        B.drow_block(start_node, GREEN)
    if goal_node != None:
        B.drow_block(goal_node, RED)

    B.drow_wall()
    if text_Show:
        win.blit(text, textRect)
    pygame.display.update()
    clock.tick(fps)



pygame.quit()

# print(current_d)
