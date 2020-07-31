from model import Model
import settings
import attr
import tkinter as tk
import numpy as np
import cv2

hex_digits = '0123456789abcdef'


@attr.s(auto_attribs=True)
class App:
    model: Model
    window: tk.Tk
    canvas: tk.Canvas
    cell_size: int = settings.DEFAULT_CELL_SIZE
    delay: float = 0.5
    total_iterations: int = -1
    visualize: bool = True

    @classmethod
    def init(cls, delay=0.005,
             field_width=settings.DEFAULT_FIELD_SIZE, field_height=settings.DEFAULT_FIELD_SIZE,
             cell_size=settings.DEFAULT_CELL_SIZE,
             fire_focus_strength=settings.DEFAULT_FIRE_FOCUS,
             propagation=settings.PROPAGATION, deviation=0.25, drone_number=25, total_iterations=400, visualize=False):
        model = Model.default(field_width, field_height, fire_focus_strength, propagation, deviation,
                              drone_number)
        window = tk.Tk()
        canvas = tk.Canvas(window, width=cell_size * field_width, height=cell_size * field_height)
        canvas.pack()
        self = cls(model, window, canvas, cell_size, delay, total_iterations, visualize)
        return self

    def draw_rectangle(self, x, y, color):
        self.canvas.create_rectangle(
            self.cell_size * x,
            self.cell_size * y,
            (x + 1) * self.cell_size,
            (y + 1) * self.cell_size,
            fill=color
        )

    def tick(self, tick_drones=True):
        self.model.tick(tick_drones)
        if self.visualize:
            mat = self.model.field.get_image()
            mat_resized = cv2.resize(mat, (500, 500))
            scale = len(mat_resized) / len(mat)
            for drone in self.model.drones:
                for i in range(round((drone.x - 1) * scale), round((drone.x + 2) * scale)):
                    for j in range(round((drone.y - 1) * scale), round((drone.y + 2) * scale)):
                        try:
                            mat_resized[i, j] = np.array([256, 0, 0])
                        except IndexError:
                            pass
            cv2.imshow("Fire", mat_resized)
            cv2.waitKey(int(self.delay * 1000))

    def main_loop(self):
        self.model.field.propagation *= 3
        i = 0
        while True:
            if i == 30:
                self.model.field.propagation /= 3
            self.tick(i > 30)
            i += 1
            if i == self.total_iterations or not self.model.field.score():
                print(f'Field log shape: {np.array(self.model.field_log).shape}')
                print(f'Drones log shape: {np.array(self.model.drones_log).shape}')
                np.save('field_log', np.array(self.model.field_log))
                np.save('drones_log', np.array(self.model.drones_log))
                return


if __name__ == '__main__':
    app = App.init()
    app.main_loop()
