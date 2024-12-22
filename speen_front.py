import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull
import imageio

# Параметры GIF
gif_filename = 'u-speen-me-round-front240fps.gif'
frames = []
num_frames = 240  # Количество кадров для 1 секунды анимации

# Функция для поворота точки в 3D
def rotate(point, angle_x, angle_y, angle_z):
    ax, ay, az = np.radians(angle_x), np.radians(angle_y), np.radians(angle_z)
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(ax), -np.sin(ax)],
                   [0, np.sin(ax), np.cos(ax)]])
    Ry = np.array([[np.cos(ay), 0, np.sin(ay)],
                   [0, 1, 0],
                   [-np.sin(ay), 0, np.cos(ay)]])
    Rz = np.array([[np.cos(az), -np.sin(az), 0],
                   [np.sin(az), np.cos(az), 0],
                   [0, 0, 1]])
    return Rz @ Ry @ Rx @ point

# Генерация случайных точек и создание выпуклой оболочки
num_points = 50
points = np.random.uniform(-1, 1, (num_points, 3))
hull = ConvexHull(points)

# Цвета для граней
colors = np.random.rand(len(hull.simplices), 3)

# Создание фигуры
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Генерация анимации вращения
for i in range(num_frames):
    ax.clear()
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.axis('on')

    # Углы поворота
    angle_x = i * 1.5  # Скорость вращения по X
    angle_y = i * 0.75  # Скорость вращения по Y
    angle_z = i * 0.5  # Скорость вращения по Z

    # Поворачиваем точки
    rotated_points = np.array([rotate(p, angle_x, angle_y, angle_z) for p in points])

    # Отрисовка только передних граней без прозрачности
    for idx, simplex in enumerate(hull.simplices):
        triangle = rotated_points[simplex]
        ax.plot_trisurf(triangle[:, 0], triangle[:, 1], triangle[:, 2],
                        color=colors[idx], edgecolor='k', alpha=1.0, shade=True)

    fig.canvas.draw()

    # Используем tostring_argb вместо tostring_rgb
    image = np.frombuffer(fig.canvas.tostring_argb(), dtype='uint8')

    # Преобразуем изображение в формат (высота, ширина, 4), т.к. ARGB включает альфа-канал
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (4,))

    # Убираем альфа-канал, оставляем только RGB
    image = image[:, :, 1:4]

    # Добавляем кадр в список
    frames.append(image)

# Сохранение в GIF с 240 fps
imageio.mimsave(gif_filename, frames, fps=240)
print(f'GIF сохранен в файл: {gif_filename}')
