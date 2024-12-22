import numpy as np
import matplotlib
matplotlib.use('Agg')  # Используем бекенд без графического интерфейса
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
import imageio

# Параметры GIF
gif_filename = 'u-speen-me-round.gif'
frames = []
num_frames = 60  # Количество кадров


# Функция для поворота точки в 3D
def rotate(point, angle_x, angle_y, angle_z):
    # Углы поворота в радианах
    ax, ay, az = np.radians(angle_x), np.radians(angle_y), np.radians(angle_z)

    # Матрицы вращения
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(ax), -np.sin(ax)],
                   [0, np.sin(ax), np.cos(ax)]])

    Ry = np.array([[np.cos(ay), 0, np.sin(ay)],
                   [0, 1, 0],
                   [-np.sin(ay), 0, np.cos(ay)]])

    Rz = np.array([[np.cos(az), -np.sin(az), 0],
                   [np.sin(az), np.cos(az), 0],
                   [0, 0, 1]])

    # Применение вращения
    rotated_point = Rz @ Ry @ Rx @ point
    return rotated_point


# Генерация случайных точек и создание выпуклой оболочки
num_points = 50  # Количество случайных точек
points = np.random.uniform(-1, 1, (num_points, 3))

# Создание выпуклой оболочки
hull = ConvexHull(points)

# Создание фигуры
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Генерация случайных цветов для каждой грани
colors = np.random.rand(len(hull.simplices), 3)

# Создание анимации вращения
for i in range(num_frames):
    ax.clear()  # Очищаем оси перед каждым новым кадром
    ax.set_title("Palanes")
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Углы поворота
    angle_x = i * 6
    angle_y = i * 3
    angle_z = i * 2

    # Поворачиваем все точки
    rotated_points = np.array([rotate(p, angle_x, angle_y, angle_z) for p in points])

    # Рисуем грани фигуры
    for idx, simplex in enumerate(hull.simplices):
        triangle = rotated_points[simplex]
        ax.plot_trisurf(triangle[:, 0], triangle[:, 1], triangle[:, 2],
                        color=colors[idx], edgecolor='k', alpha=0.8)

    # Используем buffer_argb вместо tostring_rgb
    fig.canvas.draw()

    # Считываем изображение из буфера в формате ARGB
    image = np.frombuffer(fig.canvas.tostring_argb(), dtype='uint8')

    # Преобразуем в нужный формат: (восстанавливаем размерность)
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (4,))  # Теперь 4 канала (ARGB)

    # Если нам нужен только RGB, убираем альфа-канал (для GIF не требуется альфа-канал)
    image = image[..., 1:]  # Оставляем только RGB каналы (ARGB -> RGB)

    # Добавляем кадр в список
    frames.append(image)

# Запись в GIF
imageio.mimsave(gif_filename, frames, fps=15)
print(f'GIF сохранен в файл: {gif_filename}')
