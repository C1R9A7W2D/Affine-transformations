import tkinter as tk
import numpy as np

class PolygonDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("Polygon Drawer")

        self.canvas = tk.Canvas(self.root, bg='white', width=800, height=600)
        self.canvas.pack()

        self.points = []
        
        clear_button = tk.Button(self.root, text="Очистить", command=self.clear_scene)
        clear_button.pack()
        
        self.dx_entry = tk.Entry(self.root)
        self.dy_entry = tk.Entry(self.root)
        offset_button = tk.Button(self.root, text="Смещение", command=self.apply_offset)
        
        offset_button.pack()
        self.dx_entry.pack()
        self.dy_entry.pack()

        self.center_x_entry = tk.Entry(self.root)
        self.center_y_entry = tk.Entry(self.root)
        self.degrees_entry = tk.Entry(self.root)
        rotate_button = tk.Button(self.root, text="Поворот вокруг точки", command=self.apply_rotation)

        rotate_button.pack()
        self.center_x_entry.pack()
        self.center_y_entry.pack()
        self.degrees_entry.pack()

        self.scale_factor_entry = tk.Entry(self.root)
        scale_button = tk.Button(self.root, text="Масштабирование", command=self.apply_scaling)

        scale_button.pack()
        self.scale_factor_entry.pack()
        
        scale_own_center_button = tk.Button(self.root, text="Масштабирование относительно своего центра", command=self.apply_scaling_own_center)

        scale_own_center_button.pack()

        self.canvas.bind("<Button-1>", self.add_point)

    def add_point(self, event):
        self.points.append((event.x, event.y))
        self.draw_polygons()

    def draw_polygons(self):
        self.canvas.delete("all")

        if len(self.points) > 1:
            self.canvas.create_line(self.points[-2], self.points[-1], fill='black')

        for point in self.points:
            x, y = point
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='red')

        if len(self.points) > 2:
            self.canvas.create_polygon(self.points, outline='black', fill='', width=2)

    def clear_scene(self):
        self.points.clear()
        self.canvas.delete("all")

    def apply_offset(self):
        dx = int(self.dx_entry.get())
        dy = int(self.dy_entry.get())
        self.points = self.affine_transform(np.array(self.points), self.get_translation_matrix(dx, dy))
        self.draw_polygons()

    def apply_rotation(self):
        center_x = int(self.center_x_entry.get())
        center_y = int(self.center_y_entry.get())
        degrees = int(self.degrees_entry.get())
        self.points = self.affine_transform(np.array(self.points), self.get_rotation_matrix(center_x, center_y, degrees))
        self.draw_polygons()

    def apply_scaling(self):
        scale_factor = float(self.scale_factor_entry.get())
        center_x = int(self.center_x_entry.get())
        center_y = int(self.center_y_entry.get())
        self.points = self.affine_transform(np.array(self.points), self.get_scaling_matrix(center_x, center_y, scale_factor))
        self.draw_polygons()

    def apply_scaling_own_center(self):
        scale_factor = float(self.scale_factor_entry.get())
        avgs = np.average(self.points, 0)
        center_x = int(avgs[0])
        center_y = int(avgs[1])
        self.points = self.affine_transform(np.array(self.points), self.get_scaling_matrix(center_x, center_y, scale_factor))
        self.draw_polygons()

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

if __name__ == "__main__":
    root = tk.Tk()
    app = PolygonDrawer(root)
    root.mainloop()
