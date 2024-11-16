from rplidar import RPLidar
from collections import defaultdict

PORT_NAME = '/dev/ttyUSB0'
ANGLE_BIN_SIZE = 0.5  # Intervalo de ângulo em graus para agrupar

def run():
    lidar = RPLidar(PORT_NAME)
    full_scan = []

    try:
        for scan in lidar.iter_scans(scan_type='normal'):
            full_scan.extend(scan)
            if len(full_scan) > 5000:  # Limite arbitrário para garantir cobertura de 360 graus
                break
    except ValueError as e:
        print(f"Error: {e}")
    finally:
        lidar.stop()
        lidar.disconnect()

    # Agrupar os dados por bins de ângulos
    bins = defaultdict(list)
    for meas in full_scan:
        angle = round(meas[1] / ANGLE_BIN_SIZE) * ANGLE_BIN_SIZE
        bins[angle].append(meas)

    # Processar os dados e calcular a média
    averaged_data = []
    for angle, measurements in sorted(bins.items()):
        avg_distance = sum(m[2] for m in measurements) / len(measurements)
        avg_quality = sum(m[0] for m in measurements) / len(measurements)
        averaged_data.append((angle, avg_distance, avg_quality))

    # Salvar os dados processados em um arquivo
    with open('lidar_scan_data.txt', 'w') as f:
        f.write('#RPLIDAR SCAN DATA\n')
        f.write(f'#COUNT={len(averaged_data)}\n')
        f.write('#Angle\tDistance\tQuality\n')
        for meas in averaged_data:
            f.write(f'{meas[0]:.4f}\t{meas[1]:.2f}\t{int(meas[2])}\n')

if __name__ == '__main__':
    run()
