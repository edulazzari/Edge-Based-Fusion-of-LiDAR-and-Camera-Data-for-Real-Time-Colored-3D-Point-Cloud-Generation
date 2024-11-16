import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize
import matplotlib.image as mpimg
import re
import os

# Definição das variáveis de deslocamento
add_coord_x = 0
add_coord_y = 280

def carregar_dados(arquivo):
    with open(arquivo, 'r') as f:
        for _ in range(3):
            next(f)  # Pula cabeçalho
        dados = np.loadtxt(f)
    return dados[:, 0], dados[:, 1]

def plotar_dados():
    angulos, distancias = carregar_dados('/home/edu/Desktop/lidar_scan_data.txt')
    angulo_de_rotacao = 92
    angulos_radianos = np.radians(angulos + angulo_de_rotacao)

    x = distancias * np.cos(angulos_radianos)
    y = distancias * np.sin(angulos_radianos)
    x = -x  # Espelha os dados no eixo X

    fov = 54  # Campo de Visão em graus
    central_angle_deg = 90 + angulo_de_rotacao

    angles_points = (np.degrees(np.arctan2(y, -x)) % 360)  # Normaliza ângulos
    angle_left_boundary = (central_angle_deg - fov / 2) % 360
    angle_right_boundary = (central_angle_deg + fov / 2) % 360

    if angle_left_boundary < angle_right_boundary:
        within_fov = (angles_points >= angle_left_boundary) & (angles_points <= angle_right_boundary)
    else:
        within_fov = (angles_points >= angle_left_boundary) | (angles_points <= angle_right_boundary)

    return np.column_stack((x[within_fov], y[within_fov])), angles_points[within_fov]

def rotacionar_pontos(points):
    def rotate(points, angles):
        angle_x, angle_y, angle_z = np.radians(angles)
       
        # Matriz de rotação em torno do eixo X
        rot_x = np.array([[1, 0, 0],
                          [0, np.cos(angle_x), -np.sin(angle_x)],
                          [0, np.sin(angle_x), np.cos(angle_x)]])
       
        # Matriz de rotação em torno do eixo Y
        rot_y = np.array([[np.cos(angle_y), 0, np.sin(angle_y)],
                          [0, 1, 0],
                          [-np.sin(angle_y), 0, np.cos(angle_y)]])
       
        # Matriz de rotação em torno do eixo Z
        rot_z = np.array([[np.cos(angle_z), -np.sin(angle_z), 0],
                          [np.sin(angle_z), np.cos(angle_z), 0],
                          [0, 0, 1]])
       
        # Rotaciona os pontos
        rotated_points = points @ rot_x.T @ rot_y.T @ rot_z.T
        return rotated_points

    # Adiciona a dimensão Z aos pontos
    points_3d = np.hstack((points, np.zeros((len(points), 1))))
   
    # Define os ângulos de rotação: 0 graus em X, 0 graus em Y e 0 graus em Z
    rotated_points = rotate(points_3d, [0, 0, 0])
   
    return rotated_points[:, :2]  # Retorna apenas as coordenadas x e y

# Carregar e processar os dados
points_within_fov, angles_red_points = plotar_dados()

# Remapeia os ângulos normalizados para coordenadas X (0 a 2592)
x_min = 0
x_max = 2592
y_line = 972  # Valor ajustável para a altura da linha
min_angle = np.min(angles_red_points)
max_angle = np.max(angles_red_points)
shift = -(min_angle + (max_angle - min_angle) / 2)
normalized_angles = angles_red_points + shift

x_coords = np.interp(normalized_angles, (min(normalized_angles), max(normalized_angles)), (x_min, x_max))
new_xy_coordinates = np.column_stack((x_coords, [y_line] * len(x_coords)))

# Carregar e redimensionar a imagem
image_path = '/home/edu/Desktop/testando.jpg'
image = np.rot90(mpimg.imread(image_path), k=0)
resized_image = resize(image, (1944, 2592))

# Filtrar os pontos que estão dentro do intervalo de x = 0 até x = 2592
filtered_xy_coordinates = []
for point in new_xy_coordinates:
    shifted_x = point[0] + add_coord_x
    if 0 <= shifted_x <= 2592:
        shifted_point = (shifted_x, point[1] + add_coord_y)
        filtered_xy_coordinates.append(shifted_point)

# Obter valores RGB dos pixels
pixel_values = []
for point in new_xy_coordinates:
    rounded_x = int(round(point[0] + add_coord_x))
    rounded_y = int(round(point[1] + add_coord_y))
    adjusted_y = resized_image.shape[0] - 1 - rounded_y
    if 0 <= rounded_x < resized_image.shape[1] and 0 <= adjusted_y < resized_image.shape[0]:
        pixel_value = resized_image[adjusted_y, rounded_x] * 255
        pixel_values.append(pixel_value)

# Corrigir a diferença de tamanhos entre arrays
points_within_fov_with_z = np.column_stack((points_within_fov, np.zeros(points_within_fov.shape[0])))
pixel_values = np.array(pixel_values)  # Converta para array numpy

# Certifique-se de que o número de pontos e valores RGB coincide
min_len = min(len(points_within_fov_with_z), len(pixel_values))
points_within_fov_with_z = points_within_fov_with_z[:min_len]
pixel_values = pixel_values[:min_len]

# Converta pixel_values para 2D, se necessário
pixel_values = pixel_values[:, np.newaxis] if pixel_values.ndim == 1 else pixel_values

# Combine os dados
combined_result = np.hstack((points_within_fov_with_z, pixel_values))

# Função para obter o próximo nome de arquivo
def get_next_filename(folder_path, base_name='plot_', extension='.txt'):
    # Listar todos os arquivos no diretório
    files = os.listdir(folder_path)
    
    # Filtrar arquivos que correspondem ao padrão 'plot_x.txt'
    plot_files = [f for f in files if f.startswith(base_name) and f.endswith(extension)]
    
    # Se não houver arquivos existentes, comece com plot_1.txt
    if not plot_files:
        return os.path.join(folder_path, f"{base_name}1{extension}")
    
    # Extrair o número do maior arquivo existente
    numbers = [int(f[len(base_name):-len(extension)]) for f in plot_files]
    max_number = max(numbers)
    
    # Retornar o próximo nome de arquivo
    return os.path.join(folder_path, f"{base_name}{max_number + 1}{extension}")

# Nome do próximo arquivo
file_path = get_next_filename('/home/edu/plot/')

# Caminho para o arquivo de texto do valor de inclinação do ângulo
file_path_angle = '/home/edu/angle.txt'

# Lê o conteúdo do arquivo
with open(file_path_angle, 'r') as file:
    content = file.read()

# Usa expressão regular para extrair o valor numérico da inclinação, incluindo números negativos
angle_match = re.search(r'Average Inclination:\s*([-?\d.]+)°', content)
if angle_match:
    angle_degrees = float(angle_match.group(1))
else:
    raise ValueError("Could not find the angle in the text file.")

# Converte o ângulo para radianos
angle_radians = np.deg2rad(angle_degrees)

# Define a matriz de rotação para uma rotação em torno do eixo y
rotation_matrix_y = np.array([
    [np.cos(angle_radians), 0, np.sin(angle_radians)],
    [0, 1, 0],
    [-np.sin(angle_radians), 0, np.cos(angle_radians)]
])

# Definir xyz
xyz = combined_result[:, :3]

# Rotacionar cada ponto
rotated_xyz = np.dot(xyz, rotation_matrix_y.T)

# Salvar os dados rotacionados em um arquivo .txt
header = 'X Y Z R'
np.savetxt(file_path, np.hstack((rotated_xyz, combined_result[:, 3:])), header=header, fmt='%10.5f')

print(f"Arquivo salvo em: {file_path}")

# Define limites estáticos dos eixos
#x_limits = (0, 4000)
#y_limits = (-2000, 1000)
#z_limits = (2000, -2000)

# Plotar os pontos originais e rotacionados
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.scatter(0, 0, 0, c='red', marker='o')
#ax.scatter(rotated_xyz[:, 0], rotated_xyz[:, 1], rotated_xyz[:, 2], c=combined_result[:, 3:] / 255.0, edgecolors='none')
#ax.set_xlabel('X')
#ax.set_ylabel('Y')
#ax.set_zlabel('Z')

# Definir limites dos eixos
#ax.set_xlim(x_limits)
#ax.set_ylim(y_limits)
#ax.set_zlim(z_limits)

#plt.show()
