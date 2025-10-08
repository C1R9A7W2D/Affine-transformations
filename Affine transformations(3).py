import tkinter as tk
import numpy as np

class PolygonDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("Polygon Drawer")

        self.canvas = tk.Canvas(self.root, bg='white', width=800, height=600)
        self.canvas.pack()

#1
        self.polygons = []
        self.current_polygon = []

        self.temp_point = None  
        self.intersection_points = []  
        self.selected_edge = None  
        self.edge_position_info = "" 

        control_frame = tk.Frame(self.root)
        control_frame.pack()

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_scene)
        clear_button.grid(row=0, column=0, padx=5, pady=5)

        finish_polygon_button = tk.Button(control_frame, text="Завершить полигон", command=self.finish_polygon)
        finish_polygon_button.grid(row=0, column=1, padx=5, pady=5)

        select_edge_button = tk.Button(control_frame, text="Выбрать ребро", command=self.enable_edge_selection)
        select_edge_button.grid(row=0, column=2, padx=5, pady=5)

        transform_frame = tk.Frame(self.root)
        transform_frame.pack()

        tk.Label(transform_frame, text="dx:").grid(row=0, column=0)
        self.dx_entry = tk.Entry(transform_frame, width=5)
        self.dx_entry.grid(row=0, column=1)
        
        tk.Label(transform_frame, text="dy:").grid(row=0, column=2)
        self.dy_entry = tk.Entry(transform_frame, width=5)
        self.dy_entry.grid(row=0, column=3)
        
        offset_button = tk.Button(transform_frame, text="Смещение", command=self.apply_offset)
        offset_button.grid(row=0, column=4, padx=5)

        tk.Label(transform_frame, text="Центр X:").grid(row=1, column=0)
        self.center_x_entry = tk.Entry(transform_frame, width=5)
        self.center_x_entry.grid(row=1, column=1)
        
        tk.Label(transform_frame, text="Центр Y:").grid(row=1, column=2)
        self.center_y_entry = tk.Entry(transform_frame, width=5)
        self.center_y_entry.grid(row=1, column=3)
        
        tk.Label(transform_frame, text="Угол:").grid(row=1, column=4)
        self.degrees_entry = tk.Entry(transform_frame, width=5)
        self.degrees_entry.grid(row=1, column=5)
        
        rotate_button = tk.Button(transform_frame, text="Поворот вокруг точки", command=self.apply_rotation)
        rotate_button.grid(row=1, column=6, padx=5)
        
        rotate_own_center_button = tk.Button(transform_frame, text="Поворот вокруг центра", command=self.apply_rotation_own_center)
        rotate_own_center_button.grid(row=1, column=7, padx=5)

        tk.Label(transform_frame, text="Масштаб:").grid(row=2, column=0)
        self.scale_factor_entry = tk.Entry(transform_frame, width=5)
        self.scale_factor_entry.grid(row=2, column=1)
        
        scale_button = tk.Button(transform_frame, text="Масштабирование от точки", command=self.apply_scaling)
        scale_button.grid(row=2, column=2, padx=5)
        
        scale_own_center_button = tk.Button(transform_frame, text="Масштабирование от центра", command=self.apply_scaling_own_center)
        scale_own_center_button.grid(row=2, column=3, padx=5)

        self.info_label = tk.Label(self.root, text="Создайте полигон: кликните для добавления точек")
        self.info_label.pack()

        self.mode = "draw" 
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<Motion>", self.canvas_motion)

    def enable_edge_selection(self):
        self.mode = "select_edge"
        self.selected_edge = None
        self.info_label.config(text="Выберите ребро: кликните на отрезок")

    def canvas_click(self, event):
        if self.mode == "draw":
            self.add_point(event)
        elif self.mode == "select_edge":
            self.select_edge(event)

    def select_edge(self, event):
        click_point = (event.x, event.y)
        min_distance = float('inf')
        closest_edge = None
        
        for polygon in self.polygons:
            for i in range(len(polygon)):
                if i == len(polygon) - 1:
                    if len(polygon) > 2:
                        edge = (polygon[i], polygon[0])
                    else:
                        continue
                else:
                    edge = (polygon[i], polygon[i+1])
                
                distance = self.point_to_edge_distance(click_point, edge)
                if distance < min_distance and distance < 10:  
                    min_distance = distance
                    closest_edge = edge
        
        if closest_edge:
            self.selected_edge = closest_edge
            self.mode = "draw"
            self.info_label.config(text=f"Выбрано ребро: {closest_edge[0]} - {closest_edge[1]}. Двигайте мышью для анализа.")
        else:
            self.info_label.config(text="Ребро не найдено. Попробуйте еще раз.")

    def point_to_edge_distance(self, point, edge):
        p1, p2 = edge
        x, y = point

        edge_vec = (p2[0] - p1[0], p2[1] - p1[1])
        point_vec = (x - p1[0], y - p1[1])
        
        edge_len_sq = edge_vec[0]**2 + edge_vec[1]**2
        
        if edge_len_sq == 0:
            return np.sqrt(point_vec[0]**2 + point_vec[1]**2)
        
        t = max(0, min(1, (point_vec[0]*edge_vec[0] + point_vec[1]*edge_vec[1]) / edge_len_sq))
        
        closest_point = (
            p1[0] + t * edge_vec[0],
            p1[1] + t * edge_vec[1]
        )
        
        return np.sqrt((x - closest_point[0])**2 + (y - closest_point[1])**2)

    def canvas_motion(self, event):
        self.temp_point = (event.x, event.y)
        self.update_dynamic_info()
        self.draw_scene()
#1!

#2
    def update_dynamic_info(self):
        if not self.temp_point:
            return
            
        x, y = self.temp_point
        info_text = f"Текущая позиция: ({x}, {y})"
        if self.selected_edge:
            position = self.classify_point_relative_to_edge((x, y), self.selected_edge)
            info_text += f" | Относительно ребра: {position}"
        
        point_check_results = []
        for i, polygon in enumerate(self.polygons):
            if len(polygon) >= 3: 
                is_inside = self.is_point_in_polygon(x, y, polygon)
                polygon_type = "выпуклый" if self.is_convex(polygon) else "невыпуклый"
                status = "внутри" if is_inside else "снаружи"
                point_check_results.append(f"П{i+1}({polygon_type}):{status}")
        
        if point_check_results:
            info_text += " | " + ", ".join(point_check_results)
        
        if len(self.current_polygon) >= 1:
            if len(self.current_polygon) >= 2:
                last_edge = (self.current_polygon[-2], self.current_polygon[-1])
                temp_edge = (self.current_polygon[-1], self.temp_point)
            else:
                temp_edge = (self.current_polygon[-1], self.temp_point)
            
            intersection_info = self.find_intersections_with_edge(temp_edge)
            if intersection_info:
                info_text += f" | Пересечения: {len(intersection_info)}"
        
        self.info_label.config(text=info_text)
#2!

#3
    def classify_point_relative_to_edge(self, point, edge):
        p1, p2 = edge
        x, y = point

        edge_vec = (p2[0] - p1[0], p2[1] - p1[1])
        point_vec = (x - p1[0], y - p1[1])
    
        cross_product = edge_vec[0] * point_vec[1] - edge_vec[1] * point_vec[0]

        if cross_product > 0:
            return "слева"
        else:
            return "справа"
#3!

#1
    def add_point(self, event):
        self.current_polygon.append((event.x, event.y))
        self.draw_scene()

    def finish_polygon(self):
        if len(self.current_polygon) > 0:
            self.polygons.append(self.current_polygon.copy())
            self.current_polygon = []
            self.draw_scene()

    def draw_scene(self):
        self.canvas.delete("all")
        
        for i, polygon in enumerate(self.polygons):
            color = 'blue' if self.is_convex(polygon) else 'red'
            if len(polygon) == 1:
                x, y = polygon[0]
                self.canvas.create_oval(x-3, y-3, x+3, y+3, fill=color, outline=color)
            elif len(polygon) == 2:
                self.canvas.create_line(polygon[0], polygon[1], fill=color, width=2)
            else:
                self.canvas.create_polygon(polygon, outline=color, fill='', width=2)

            for point in polygon:
                x, y = point
                self.canvas.create_oval(x-3, y-3, x+3, y+3, fill=color, outline=color)

        if self.selected_edge:
            p1, p2 = self.selected_edge
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], 
                                  fill='orange', width=4, arrow=tk.BOTH)

        if self.current_polygon:
            current_color = 'green'

            if len(self.current_polygon) == 1:
                x, y = self.current_polygon[0]
                self.canvas.create_oval(x-3, y-3, x+3, y+3, fill=current_color, outline=current_color)
            elif len(self.current_polygon) == 2:
                self.canvas.create_line(self.current_polygon[0], self.current_polygon[1], fill=current_color, width=2)
            else:
                self.canvas.create_polygon(self.current_polygon, outline=current_color, fill='', width=2)
            
            for point in self.current_polygon:
                x, y = point
                self.canvas.create_oval(x-3, y-3, x+3, y+3, fill=current_color, outline=current_color)

            if self.current_polygon and self.temp_point:
                last_point = self.current_polygon[-1]
                self.canvas.create_line(last_point[0], last_point[1], 
                                      self.temp_point[0], self.temp_point[1], 
                                      fill=current_color, width=2, dash=(4, 2))

                if len(self.current_polygon) >= 1:
                    temp_edge = (last_point, self.temp_point)
                    intersections = self.find_intersections_with_edge(temp_edge)
                    for x, y in intersections:
                        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill='orange', outline='black')

        for x, y in self.intersection_points:
            self.canvas.create_oval(x-4, y-4, x+4, y+4, fill='purple', outline='black')

        if self.temp_point:
            x, y = self.temp_point
            self.canvas.create_oval(x-2, y-2, x+2, y+2, fill='yellow', outline='black')
#1!
          
#2
    def find_intersections_with_edge(self, edge):
        intersections = []
        p1, p2 = edge

        all_edges = []
        for polygon in self.polygons:
            for i in range(len(polygon)):
                if i == len(polygon) - 1:
                    if len(polygon) > 2:  
                        all_edges.append((polygon[i], polygon[0]))
                else:
                    all_edges.append((polygon[i], polygon[i+1]))
        
        for other_edge in all_edges:
            p3, p4 = other_edge
            intersection = self.find_intersection(p1, p2, p3, p4)
            if intersection:
                intersections.append(intersection)
        
        return intersections
#2!

#1
    def clear_scene(self):
        self.polygons.clear()
        self.current_polygon.clear()
        self.temp_point = None
        self.intersection_points.clear()
        self.selected_edge = None
        self.mode = "draw"
        self.info_label.config(text="Создайте полигон: кликните для добавления точек")
        self.draw_scene()
#1!

#2
    def is_point_in_polygon(self, x, y, polygon):
        if len(polygon) < 3:
            return False
            
        n = len(polygon)
        inside = False
        
        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
            
        return inside

    def is_convex(self, polygon):
        if len(polygon) < 3:
            return True
            
        n = len(polygon)
        if n == 3:
            return True
            
        sign = None
        for i in range(n):
            dx1 = polygon[(i+2)%n][0] - polygon[(i+1)%n][0]
            dy1 = polygon[(i+2)%n][1] - polygon[(i+1)%n][1]
            dx2 = polygon[i][0] - polygon[(i+1)%n][0]
            dy2 = polygon[i][1] - polygon[(i+1)%n][1]
            
            cross = dx1 * dy2 - dy1 * dx2
            
            if cross != 0:
                if sign is None:
                    sign = cross > 0
                elif (cross > 0) != sign:
                    return False
                    
        return True

    def find_intersection(self, p1, p2, p3, p4):
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4
        
        denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
        if abs(denom) < 1e-10:
            return None 
            
        ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
        ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom
        
        if 0 <= ua <= 1 and 0 <= ub <= 1:
            x = x1 + ua * (x2 - x1)
            y = y1 + ua * (y2 - y1)
            return (x, y)
            
        return None
#2!

#1
    def apply_offset(self):
        if not self.polygons:
            return
            
        dx = int(self.dx_entry.get() or 0)
        dy = int(self.dy_entry.get() or 0)
        
        for i in range(len(self.polygons)):
            self.polygons[i] = self.affine_transform(np.array(self.polygons[i]), 
                                                   self.get_translation_matrix(dx, dy))
        self.draw_scene()

    def apply_rotation(self):
        if not self.polygons:
            return
            
        center_x = int(self.center_x_entry.get() or 0)
        center_y = int(self.center_y_entry.get() or 0)
        degrees = int(self.degrees_entry.get() or 0)
        
        for i in range(len(self.polygons)):
            self.polygons[i] = self.affine_transform(np.array(self.polygons[i]), 
                                                   self.get_rotation_matrix(center_x, center_y, degrees))
        self.draw_scene()

    def apply_rotation_own_center(self):
        if not self.polygons:
            return
            
        degrees = int(self.degrees_entry.get() or 0)
        
        for i in range(len(self.polygons)):
            polygon = np.array(self.polygons[i])
            center = np.mean(polygon, axis=0)
            center_x, center_y = center[0], center[1]
            
            self.polygons[i] = self.affine_transform(polygon, 
                                                   self.get_rotation_matrix(center_x, center_y, degrees))
        self.draw_scene()

    def apply_scaling(self):
        if not self.polygons:
            return
            
        scale_factor = float(self.scale_factor_entry.get() or 1.0)
        center_x = int(self.center_x_entry.get() or 0)
        center_y = int(self.center_y_entry.get() or 0)
        
        for i in range(len(self.polygons)):
            self.polygons[i] = self.affine_transform(np.array(self.polygons[i]), 
                                                   self.get_scaling_matrix(center_x, center_y, scale_factor))
        self.draw_scene()
    
    def apply_scaling_own_center(self):
        if not self.polygons:
            return
            
        scale_factor = float(self.scale_factor_entry.get() or 1.0)
        
        for i in range(len(self.polygons)):
            polygon = np.array(self.polygons[i])
            center = np.mean(polygon, axis=0)
            center_x, center_y = center[0], center[1]
            
            self.polygons[i] = self.affine_transform(polygon, 
                                                   self.get_scaling_matrix(center_x, center_y, scale_factor))
        self.draw_scene()

    def affine_transform(self, points, transformation_matrix):     
        points_homogeneous = np.hstack((points, np.ones((points.shape[0], 1))))
        points_transformed = np.dot(transformation_matrix, points_homogeneous.T).T
        return points_transformed[:, :2].astype(int).tolist()

    def get_translation_matrix(self, dx, dy):
        return np.array([[1, 0, dx],
                         [0, 1, dy],
                         [0, 0, 1]])

    def get_rotation_matrix(self, center_x, center_y, angle):
        angle_rad = np.radians(angle)
        cos_a, sin_a = np.cos(angle_rad), np.sin(angle_rad)
        return np.array([[cos_a, -sin_a, center_x - center_x * cos_a + center_y * sin_a],
                         [sin_a, cos_a, center_y - center_x * sin_a - center_y * cos_a],
                         [0, 0, 1]])

    def get_scaling_matrix(self, center_x, center_y, scale_factor):
        return np.array([[scale_factor, 0, center_x * (1 - scale_factor)],
                         [0, scale_factor, center_y * (1 - scale_factor)],
                         [0, 0, 1]])
#1!

if __name__ == "__main__":
    root = tk.Tk()
    app = PolygonDrawer(root)
    root.mainloop()
