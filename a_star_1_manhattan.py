from tkinter import *
from tkinter import ttk
import time
from data_input import maze, start, end


class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        
        self.g = 0
        self.h = 0
        self.f = 0

    @property
    def x(self):
        return self.position[1]
    
    @property
    def y(self):
        return self.position[0]

    def __eq__(self, other):
        return self.position == other.position

    def __str__(self):
        return f"({self.position})"

class AStarGUI(Frame):
    def __init__(self, master, maze, start, end):
        Frame.__init__(self, master)
        master.title("Path Mapping A*")
        self.boardsize = 600
        self.maze = maze
        self.start = start
        self.end = end
        self.sqsize = self.boardsize//len(maze)
        self.rect = []
        self.draw_initial_map()
        self.grid(row=0,column=0)
        self.master.update()
        self.path = self.a_star()
        print(self.path)
        self.draw_line_from_path(self.path)
        self.master.mainloop()

    def draw_initial_map(self):
        mainframe = ttk.Frame(self, padding=(5,5,5,5))
        mainframe.pack()

        self.board = Canvas(mainframe, width=self.boardsize, height=self.boardsize,bg='white')
        self.board.pack()

        for row in range(len(maze)):
            row_rect = []
            for col in range(len(maze[row])):
                if maze[row][col] == 1 : # wall
                    color_fill = 'black'
                elif row == self.start[0] and col == self.start[1]: # start point
                    color_fill = '#00dd00' 
                elif row == self.end[0] and col == self.end[1]: # end point
                    color_fill = 'red'
                else :
                    color_fill = 'white'

                top = row * self.sqsize
                left = col * self.sqsize
                bottom = row * self.sqsize + self.sqsize
                right = col * self.sqsize + self.sqsize
                
                rect = self.board.create_rectangle(left,top,right,bottom,outline='black',fill=color_fill)
                row_rect.append(rect)
            self.rect.append(row_rect)

    def draw_line_from_path(self, path):
        x_start = path[0][1]*self.sqsize + (self.sqsize/2)
        y_start = path[0][0]*self.sqsize + (self.sqsize/2)
        for y,x in path[1:]:
            x_end = x*self.sqsize + (self.sqsize/2)
            y_end = y*self.sqsize + (self.sqsize/2)
            self.board.create_line(x_start, y_start, x_end, y_end, width=3, fill="yellow")
            self.update_gui()
            x_start = x_end
            y_start = y_end

    def set_color(self, y, x , color):
        self.board.itemconfig(self.rect[y][x], fill=color)

    # Helper method
    def node_in_list(self, node, node_list):
        for child in node_list:
            if child == node:
                return child
        return False

    def update_gui(self):
        self.master.update()
        time.sleep(0.01)

    def a_star(self):
        calculate_time = 0.0
        total_operation = 0
        node_searched = 0
        open_list = []
        closed_list = []
        start_node = Node(None, self.start)
        end_node = Node(None, self.end)
        open_list.append(start_node)

        while len(open_list) > 0:
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Color choosen node
            if current_node != start_node :
                self.set_color(current_node.y, current_node.x, '#afeeee')
            self.update_gui()

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
                # Make sure within range and walkable terrain
                if node_position[0] > len(maze)-1 or node_position[0] < 0 or node_position[1] > len(maze[-1])-1 or node_position[1] < 0:
                    continue
                if maze[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node and append to list
                new_node = Node(current_node, node_position)
                children.append(new_node)

                # Check if children node is end point
                if new_node == end_node:
                    path = []
                    current = new_node
                    while current is not None:
                        path.append(current.position)
                        current = current.parent
                    print(f"Calculation time : {calculate_time}")
                    print(f"Node searched : {node_searched}")
                    print(f"Total operation : {total_operation}")
                    print(f"Path length : {len(path)}")
                    return path[::-1]

            for child in children:
                # Child already in closed list
                if self.node_in_list(child, closed_list):
                    continue

                # Create the f, g, and h values
                start_time = time.time()
                child.g = current_node.g + 1
                child.h = abs(child.y - end_node.y)  + abs(child.x - end_node.x) 
                child.f = child.g + child.h
                calculate_time += time.time() - start_time
                total_operation += 1

                # Do not add larger cost path to open list
                node_in_open_node = self.node_in_list(child, open_list)
                if node_in_open_node and child.g >= node_in_open_node.g:
                    continue

                open_list.append(child)
                node_searched += 1

                # Update open path color
                self.set_color(child.y, child.x, 'lightgreen')
            self.update_gui()


if __name__ == '__main__':
    tk = Tk()
    tk.update_idletasks()
    gui = AStarGUI(tk, maze, start, end)
    
