import time
import board
import busio
import adafruit_adxl34x
import math

# Inicializar a comunicação I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Inicializar o sensor ADXL345
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# Função para calcular a inclinação em relação ao plano XZ
def calculate_inclination(x, z, calibration_offset):
    inclination = -(math.degrees(math.atan2(x, z)) - calibration_offset)
    return inclination

# Defina o offset de calibração manualmente
calibration_offset = 86.39

# Número de amostras para calcular a média
num_samples = 100

# Intervalo entre leituras em segundos (pode ser ajustado ou removido)
sample_interval = 0.01

# Caminho do arquivo de texto
file_path = "/home/edu/angle.txt"

inclinations = []

# Coletar num_samples amostras
for _ in range(num_samples):
    # Ler os valores de aceleração
    x, y, z = accelerometer.acceleration
    
    # Calcular a inclinação em relação ao plano XZ
    inclination = calculate_inclination(x, z, calibration_offset)
    
    # Adicionar a inclinação à lista
    inclinations.append(inclination)
    
    if sample_interval > 0:
        time.sleep(sample_interval)

# Calcular a média das inclinações
average_inclination = sum(inclinations) / num_samples

# Escrever a média no arquivo txt
with open(file_path, "w") as file:
    file.write(f"Average Inclination: {average_inclination:.2f}°\n")

# O código agora termina a execução após salvar o valor no arquivo.
