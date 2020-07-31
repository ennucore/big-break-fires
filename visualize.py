import cv2
import os
import numpy as np


def get_color_by_rate(rate):
    if rate < 0:
        rate = 0
    return 255 * (1 - rate), (255 - 50 * rate), 255


def visualize(field, drones, height=120, width=120, do_drones=True):
    img = np.zeros((height, width, 3), np.uint8)
    for x in range(width):
        for y in range(height):
            rate = field[x, y]
            img[x, y] = get_color_by_rate(rate)
    if do_drones:
        for drone in drones:
            img = cv2.circle(img, (int(drone[0]), int(drone[1])), 2, (255, 0, 0), -1)
    return img


drones_log = np.load(input('Drones log: ') or 'drones_log.npy')
field_log = np.load(input('Field log: ') or 'field_log.npy')
try:
    os.removedirs('frames')
except Exception:
    pass
os.makedirs('frames')
n = 0
for i in range(30):
    img = visualize(field_log[i], drones_log[i], do_drones=False)
    for _ in range(3):
        cv2.imwrite(f'frames/{n}.jpg', img)
        n += 1
for i in range(30, len(field_log)):
    img = visualize(field_log[i], drones_log[i])
    cv2.imwrite(f'frames/{n}.jpg', img)
    n += 1

cmd = f'ffmpeg -y -start_number 0 -i "frames/%d.jpg" -c:v libx264 -r 24.97 -pix_fmt yuv420p output.mp4'
os.system(cmd)
