import time
import serial
import pybullet as p
import pybullet_data

# ==========================================
# 1. CONFIGURACIÓN DEL PUERTO SERIAL (ESP32)
# ==========================================
# CAMBIA 'COM3' por el puerto serial al que está conectada tu ESP32.
# En Linux/Mac suele ser '/dev/ttyUSB0' o '/dev/ttyACM0'.
PUERTO_SERIAL = 'COM5' 
BAUD_RATE = 115200

try:
    ser = serial.Serial(PUERTO_SERIAL, BAUD_RATE, timeout=0.1)
    print(f"Conectado exitosamente a la ESP32 en {PUERTO_SERIAL}")
except Exception as e:
    print(f"Error abriendo el puerto serial: {e}")
    print("Revisa qué puerto COM asignó Windows a tu ESP32.")
    exit()

# ==========================================
# 2. INICIALIZAR SIMULADOR EN 3D (PyBullet)
# ==========================================
physicsClient = p.connect(p.GUI) # Inicia la interfaz gráfica
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

# Cargar un piso de fondo
p.loadURDF("plane.urdf")

# Cargar tu robot URDF (Asegúrate de que 'brazo.urdf' esté en esta misma carpeta)
robot_id = p.loadURDF("brazo.urdf", [0, 0, 0], useFixedBase=True)

# Obtener número de articulaciones
num_joints = p.getNumJoints(robot_id)
print(f"El robot tiene {num_joints} articulaciones detectadas.")

# Mapeo de nombres de articulaciones según el URDF
# Inicia los motores en modo control de posición
joint_indices = {}
for i in range(num_joints):
    info = p.getJointInfo(robot_id, i)
    joint_name = info[1].decode('utf-8')
    joint_indices[joint_name] = i
    print(f"Articulación {i}: {joint_name}")

# ==========================================
# 3. BUCLE PRINCIPAL DE CONTROL EN TIEMPO REAL
# ==========================================
time.sleep(1) # Espera de inicialización

try:
    while True:
        p.stepSimulation() # Avanza la física de la simulación
        
        if ser.in_waiting > 0:
            try:
                # Leer línea desde el ESP32
                linea = ser.readline().decode('utf-8', errors='ignore').strip()
                if linea:
                    # Separar los 3 valores recibidos por coma: j1, j2, gripper
                    valores = linea.split(',')
                    if len(valores) == 3:
                        j1 = float(valores[0])
                        j2 = float(valores[1])
                        gripper = float(valores[2])

                        # Imprimir en consola para depuración
                        print(f"Valores -> J1: {j1:.2f} rad | J2: {j2:.2f} rad | Gripper: {gripper:.3f} m")

                        # Actualizar posiciones en la ventana 3D de PyBullet
                        if 'joint_1' in joint_indices:
                            p.setJointMotorControl2(robot_id, joint_indices['joint_1'], p.POSITION_CONTROL, targetPosition=j1)
                        
                        if 'joint_2' in joint_indices:
                            p.setJointMotorControl2(robot_id, joint_indices['joint_2'], p.POSITION_CONTROL, targetPosition=j2)

                        # Actualizar la pinza (si hay varios joints de pinza, se aplican a las articulaciones de los dedos)
                        if 'joint_gripper' in joint_indices:
                            p.setJointMotorControl2(robot_id, joint_indices['joint_gripper'], p.POSITION_CONTROL, targetPosition=gripper)

            except ValueError:
                pass # Ignora lecturas incompletas/corruptas

        time.sleep(0.01) # Frecuencia de actualización ~100Hz

except KeyboardInterrupt:
    print("\nSimulación finalizada por el usuario.")
    ser.close()
    p.disconnect()