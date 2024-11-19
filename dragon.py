import tkinter as tk
import math
import numpy as np

points = 40
length = 50

class Chain:
    def __init__(self, canvas, length, points):
        self.canvas = canvas
        self.length = length
        self.points = points
        self.joints = []  
        self.circles = []  
        self.lines = []  
        self.perpendicular_lines = []  
        self.sum_lines = []  
        self.create_chain()

    def create_chain(self):
        start = (300, 300)  
        for i in range(self.points):
            x = start[0] + i * self.length
            y = start[1]
            self.joints.append([x, y])  
            ball = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="white")
            self.circles.append(ball)
            
    def update_chain(self, x, y):
        self.joints[0] = [x, y]  

        for i in range(1, self.points):
            dynamic_length = self.length * (1 - i / self.points)  
            
            dx = self.joints[i-1][0] - self.joints[i][0]
            dy = self.joints[i-1][1] - self.joints[i][1]
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > dynamic_length:
                angle = math.atan2(dy, dx)
                self.joints[i][0] = self.joints[i-1][0] - dynamic_length * math.cos(angle)
                self.joints[i][1] = self.joints[i-1][1] - dynamic_length * math.sin(angle)
        
        for line in self.lines:
            self.canvas.delete(line)
        self.lines.clear()  

        for line in self.perpendicular_lines:
            self.canvas.delete(line)
        self.perpendicular_lines.clear()  

        for line in self.sum_lines:
            self.canvas.delete(line)
        self.sum_lines.clear()  
        j=self.points
        for i, (px, py) in enumerate(self.joints):
            self.canvas.coords(self.circles[i], px - 5, py - 5, px + 5, py + 5)

            if i > 0:
                line = self.canvas.create_line(self.joints[i-1][0], self.joints[i-1][1], px, py, width=2, fill="white")
                self.lines.append(line)  

                dx = self.joints[i][0] - self.joints[i-1][0]
                dy = self.joints[i][1] - self.joints[i-1][1]
                length = math.sqrt(dx**2 + dy**2)
                
                normal_dx = -dy / (length*40)-j
                normal_dy = dx / (length*40)-j

                if i < self.points - 5 and i >2: 
                    sum_dx = dx + normal_dx
                    sum_dy = dy + normal_dy
                    sum_dx_2 = dx - normal_dx
                    sum_dy_2 = dy - normal_dy
                    
                    sum_x_1 = px + sum_dx
                    sum_y_1 = py + sum_dy
                    sum_x_2 = px + sum_dx_2
                    sum_y_2 = py + sum_dy_2

                    sum_line1 = self.canvas.create_line(px, py, sum_x_1, sum_y_1, width=2, fill="white")
                    sum_line2 = self.canvas.create_line(px, py, sum_x_2, sum_y_2, width=2, fill="white")
                    self.sum_lines.append(sum_line1)  
                    self.sum_lines.append(sum_line2)  
            j-=1
root = tk.Tk()
root.title("Chain with Tkinter")
canvas = tk.Canvas(root, width=1200, height=600, bg="black")
canvas.pack()
chain = Chain(canvas, length, points)
def on_mouse_move(event):
    x, y = event.x, event.y
    chain.update_chain(x, y)

canvas.bind("<Motion>", on_mouse_move)
root.mainloop()
