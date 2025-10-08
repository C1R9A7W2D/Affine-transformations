import matplotlib.pyplot as plt
import numpy as np

class PointClassifier:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.edge_a = None
        self.edge_b = None
        self.points = []
        self.results = []
        self.setup_plot()
        
    def setup_plot(self):
        """Настраивает график"""
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title('Классификация точек относительно ребра', fontsize=14)
        self.ax.axis('equal')
        
    def classify_point_relative_to_edge(self, a, b, p):
        """
        Классифицирует положение точки p относительно ребра ab.
        """
        # Вычисляем векторное произведение
        cross_product = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
        
        if cross_product > 0:
            return "left", cross_product
        elif cross_product < 0:
            return "right", cross_product
        else:
            return "on_line", cross_product
    
    def set_edge(self, a, b):
        """Устанавливает ребро для классификации"""
        self.edge_a = a
        self.edge_b = b
        self.points = []
        self.results = []
        self.draw_edge()
    
    def draw_edge(self):
        """Рисует ребро на графике"""
        self.ax.clear()
        self.setup_plot()
        
        # Рисуем ребро
        self.ax.plot([self.edge_a[0], self.edge_b[0]], [self.edge_a[1], self.edge_b[1]], 
                    'b-', linewidth=3, label='Ребро')
        self.ax.plot([self.edge_a[0], self.edge_b[0]], [self.edge_a[1], self.edge_b[1]], 
                    'bo', markersize=8, label='Концы ребра')
        
        # Добавляем стрелку направления ребра
        dx = self.edge_b[0] - self.edge_a[0]
        dy = self.edge_b[1] - self.edge_a[1]
        self.ax.arrow(self.edge_a[0] + dx*0.1, self.edge_a[1] + dy*0.1, 
                     dx*0.8, dy*0.8, head_width=0.1, head_length=0.1, 
                     fc='blue', ec='blue', alpha=0.7)
        
        # Перерисовываем все точки, если они есть
        for i, (point, result) in enumerate(zip(self.points, self.results)):
            self.draw_point(point, result, i)
        
        self.ax.legend(loc='upper right')
    
    def draw_point(self, point, result, index):
        """Рисует точку на графике с соответствующим цветом"""
        if result[0] == "left":
            color = 'green'
            marker = '^'
            label = 'Слева' if index == 0 else ""
        elif result[0] == "right":
            color = 'red'
            marker = 'v'
            label = 'Справа' if index == 0 else ""
        else:
            color = 'orange'
            marker = 's'
            label = 'На прямой' if index == 0 else ""
        
        self.ax.plot(point[0], point[1], marker, color=color, markersize=10, label=label)
        
        # Добавляем номер точки
        self.ax.text(point[0] + 0.05, point[1] + 0.05, str(index+1), 
                    fontsize=10, color=color, weight='bold')
    
    def add_point(self, point):
        """Добавляет точку и обновляет визуализацию"""
        if self.edge_a is None or self.edge_b is None:
            print("Сначала задайте ребро!")
            return
        
        result = self.classify_point_relative_to_edge(self.edge_a, self.edge_b, point)
        self.points.append(point)
        self.results.append(result)
        
        # Перерисовываем график с новой точкой
        self.draw_edge()
        
        # Выводим информацию о точке
        print(f"Точка {len(self.points)}: {point} → {result[0]} (векторное произведение: {result[1]:.2f})")
    
    def show_statistics(self):
        """Показывает статистику по всем точкам"""
        if not self.points:
            print("Нет точек для анализа")
            return
            
        left_count = sum(1 for r in self.results if r[0] == "left")
        right_count = sum(1 for r in self.results if r[0] == "right")
        online_count = sum(1 for r in self.results if r[0] == "on_line")
        
        print("\n" + "="*50)
        print("СТАТИСТИКА:")
        print(f"Всего точек: {len(self.points)}")
        print(f"Слева от ребра: {left_count}")
        print(f"Справа от ребра: {right_count}")
        print(f"На прямой: {online_count}")
        print("="*50)
    
    def display(self):
        """Отображает график"""
        plt.draw()
        plt.pause(0.01)  # Короткая пауза для обновления графика

def interactive_demo():
    """Интерактивная демонстрация с возможностью добавления точек"""
    print("=== ИНТЕРАКТИВНАЯ КЛАССИФИКАЦИЯ ТОЧЕК ОТНОСИТЕЛЬНО РЕБРА ===")
    
    # Включаем интерактивный режим ДО создания графиков
    plt.ion()
    
    # Создаем классификатор
    classifier = PointClassifier()
    
    # Задаем ребро
    print("\nЗадайте координаты ребра AB:")
    ax = float(input("A_x: "))
    ay = float(input("A_y: "))
    bx = float(input("B_x: "))
    by = float(input("B_y: "))
    
    classifier.set_edge((ax, ay), (bx, by))
    classifier.display()
    
    # Основной цикл добавления точек
    while True:
        print("\n" + "-"*30)
        print("Выберите действие:")
        print("1 - Добавить точку")
        print("2 - Показать статистику")
        print("3 - Задать новое ребро")
        print("0 - Выход")
        
        choice = input("Ваш выбор: ").strip()
        
        if choice == "1":
            print("\nВведите координаты точки:")
            try:
                px = float(input("P_x: "))
                py = float(input("P_y: "))
                classifier.add_point((px, py))
                classifier.display()
            except ValueError:
                print("Ошибка: введите числовые значения!")
                
        elif choice == "2":
            classifier.show_statistics()
            
        elif choice == "3":
            print("\nЗадайте новые координаты ребра AB:")
            ax = float(input("A_x: "))
            ay = float(input("A_y: "))
            bx = float(input("B_x: "))
            by = float(input("B_y: "))
            classifier.set_edge((ax, ay), (bx, by))
            classifier.display()
            
        elif choice == "0":
            print("Выход из программы.")
            plt.close('all')  # Закрываем все графики
            break
            
        else:
            print("Неверный выбор, попробуйте снова.")

def demo_with_example():
    """Демонстрация с заранее заданным примером"""
    plt.ion()  # Включаем интерактивный режим
    
    classifier = PointClassifier()
    
    # Задаем пример ребра
    classifier.set_edge((0, 0), (3, 2))
    classifier.display()
    
    # Добавляем несколько точек для демонстрации
    demo_points = [
        (1, 2),   # слева
        (2, 1),   # справа
        (1.5, 1), # на прямой
        (0, 1),   # слева
        (3, 0),   # справа
    ]
    
    print("Демонстрация: добавляем точки к ребру (0,0)→(3,2)")
    for i, point in enumerate(demo_points):
        print(f"Добавляем точку {i+1}: {point}")
        classifier.add_point(point)
        classifier.display()
        plt.pause(1)  # Пауза для наглядности
    
    classifier.show_statistics()
    
    # Ждем закрытия окна
    print("\nНажмите Enter в консоли для завершения...")
    input()
    plt.close('all')

def simple_interactive():
    """Упрощенная интерактивная версия без сложного управления графиком"""
    print("=== ПРОСТАЯ ИНТЕРАКТИВНАЯ КЛАССИФИКАЦИЯ ===")
    
    # Задаем ребро
    print("\nЗадайте координаты ребра AB:")
    ax = float(input("A_x: "))
    ay = float(input("A_y: "))
    bx = float(input("B_x: "))
    by = float(input("B_y: "))
    
    a = (ax, ay)
    b = (bx, by)
    
    points = []
    results = []
    
    def classify_point(a, b, p):
        cross_product = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
        if cross_product > 0:
            return "left", cross_product
        elif cross_product < 0:
            return "right", cross_product
        else:
            return "on_line", cross_product
    
    def visualize_all(a, b, points, results):
        plt.figure(figsize=(10, 8))
        
        # Рисуем ребро
        plt.plot([a[0], b[0]], [a[1], b[1]], 'b-', linewidth=3, label='Ребро')
        plt.plot([a[0], b[0]], [a[1], b[1]], 'bo', markersize=8, label='Концы ребра')
        
        # Рисуем все точки
        for i, (point, result) in enumerate(zip(points, results)):
            if result[0] == "left":
                color = 'green'
                marker = '^'
            elif result[0] == "right":
                color = 'red'
                marker = 'v'
            else:
                color = 'orange'
                marker = 's'
            
            plt.plot(point[0], point[1], marker, color=color, markersize=10)
            plt.text(point[0] + 0.05, point[1] + 0.05, str(i+1), 
                    fontsize=10, color=color, weight='bold')
        
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Классификация точек относительно ребра', fontsize=14)
        plt.legend()
        plt.show()
    
    while True:
        print("\n" + "-"*30)
        print("Выберите действие:")
        print("1 - Добавить точку")
        print("2 - Показать статистику и визуализацию")
        print("0 - Выход")
        
        choice = input("Ваш выбор: ").strip()
        
        if choice == "1":
            print("\nВведите координаты точки:")
            try:
                px = float(input("P_x: "))
                py = float(input("P_y: "))
                p = (px, py)
                result = classify_point(a, b, p)
                points.append(p)
                results.append(result)
                print(f"Точка {len(points)}: {p} → {result[0]} (векторное произведение: {result[1]:.2f})")
            except ValueError:
                print("Ошибка: введите числовые значения!")
                
        elif choice == "2":
            if not points:
                print("Нет точек для анализа")
            else:
                left_count = sum(1 for r in results if r[0] == "left")
                right_count = sum(1 for r in results if r[0] == "right")
                online_count = sum(1 for r in results if r[0] == "on_line")
                
                print("\n" + "="*50)
                print("СТАТИСТИКА:")
                print(f"Всего точек: {len(points)}")
                print(f"Слева от ребра: {left_count}")
                print(f"Справа от ребра: {right_count}")
                print(f"На прямой: {online_count}")
                print("="*50)
                
                visualize_all(a, b, points, results)
            
        elif choice == "0":
            print("Выход из программы.")
            break
            
        else:
            print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    print("Выберите режим:")
    print("1 - Полная интерактивная демонстрация")
    print("2 - Демонстрационный пример")
    print("3 - Простая интерактивная версия")
    
    choice = input("Ваш выбор (1/2/3): ").strip()
    
    if choice == "1":
        interactive_demo()
    elif choice == "2":
        demo_with_example()
    else:
        simple_interactive()