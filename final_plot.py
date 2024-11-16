import numpy as np
import matplotlib.pyplot as plt
import os
from glob import glob

def carregar_dados_arquivos(pasta):
    arquivos = sorted(glob(os.path.join(pasta, 'plot_*.txt')))
    dados = []
    
    for arquivo in arquivos:
        dados_arquivo = np.loadtxt(arquivo)
        dados.append(dados_arquivo)
    
    return np.vstack(dados)  # Empilha os dados em uma única matriz

def plotar_dados(dados):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Separar coordenadas XYZ e valores RGB
    xyz = dados[:, :3]
    rgb = dados[:, 3:] / 255.0  # Normalizar valores RGB para o intervalo [0, 1]
    
    # Plotar todos os pontos
    ax.scatter(0, 0, 0, c='red', marker='o')
    ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2], c=rgb, edgecolors='none', marker='o', s=10)
    
    # Definir limites dos eixos (ajustar conforme necessário)
    x_limits = (0, 2500)
    y_limits = (-1500, 1500)
    z_limits = (1000, -2500)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # Definir limites dos eixos
    ax.set_xlim(x_limits)
    ax.set_ylim(y_limits)
    ax.set_zlim(z_limits)
    
    # Definir elevação e azimute
    ax.view_init(elev=10, azim=168)
    
    plt.show()

# Caminho para a pasta onde os arquivos estão localizados
pasta_dados = '/home/edu/plot_sala_12/'

# Carregar todos os dados dos arquivos .txt
dados_todos = carregar_dados_arquivos(pasta_dados)

# Plotar os dados
plotar_dados(dados_todos)
