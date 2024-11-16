import RPi.GPIO as GPIO
import time

# Configurações do pino do servo
servo_pin = 11  # GPIO pin 11
angle_increment = 0  # Incremento de ângulo em graus

# Configura o modo de numeração dos pinos
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)  # Desativa os avisos
GPIO.setup(servo_pin, GPIO.OUT)

# Configura o PWM no pino do servo
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz (20 ms de período)
pwm.start(0)  # Inicializa com duty cycle 0%

def set_servo_angle(angle):
    # Calcula o duty cycle baseado no ângulo
    duty = max(min(angle / 18 + 2, 12), 2)  # Limita entre 2% e 12%
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.09)  # Ajusta o tempo se necessário para movimentos mais sutis
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

def get_current_angle():
    try:
        with open('servo_down.txt', 'r') as file:
            angle = float(file.read().strip())
    except (FileNotFoundError, ValueError):
        angle = 0.0  # Default angle if file is not found or has invalid content
    return angle

def save_current_angle(angle):
    with open('servo_down.txt', 'w') as file:
        file.write(f"{angle:.2f}")

try:
    current_angle = get_current_angle()
    new_angle = current_angle + angle_increment
    if new_angle > 180:
        new_angle = 180  # Limita o ângulo a 180 graus
    set_servo_angle(new_angle)
    save_current_angle(new_angle)
    print(f"Movido para {new_angle} graus.")

except KeyboardInterrupt:
    # Para o PWM e limpa as configurações do GPIO
    pwm.stop()
    GPIO.cleanup()
