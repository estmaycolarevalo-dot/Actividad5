import time
import serial
import pybullet as p
import pybullet_data
PUERTO_SERIAL = 'COM5' 
BAUD_RATE = 115200
try:
    ser = serial.Serial(PUERTO_SERIAL, BAUD_RATE, timeout=0.1)
    print(f"Conectado exitosamente a la ESP32 en {PUERTO_SERIAL}")
except Exception as e:
    print(f"Error abriendo el puerto serial: {e}")
    print("Revisa qué puerto COM asignó Windows a tu ESP32.")
    exit()
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf")
robot_id = p.loadURDF("brazo.urdf", [0, 0, 0], useFixedBase=True)
num_joints = p.getNumJoints(robot_id)
print(f"El robot tiene {num_joints} articulaciones detectadas.")
joint_indices = {}
for i in range(num_joints):
    info = p.getJointInfo(robot_id, i)
    joint_name = info[1].decode('utf-8')
    joint_indices[joint_name] = i
    print(f"Articulación {i}: {joint_name}")
time.sleep(1)
try:
    while True:
        p.stepSimulation()
        if ser.in_waiting > 0:
            try:
                linea = ser.readline().decode('utf-8', errors='ignore').strip()
                if linea:
                    valores = linea.split(',')
                    if len(valores) == 3:
                        j1 = float(valores[0])
                        j2 = float(valores[1])
                        gripper = float(valores[2])
                        print(f"Valores -> J1: {j1:.2f} rad | J2: {j2:.2f} rad | Gripper: {gripper:.3f} m")
                        if 'joint_1' in joint_indices:
                            p.setJointMotorControl2(robot_id, joint_indices['joint_1'], p.POSITION_CONTROL, targetPosition=j1)
                        if 'joint_2' in joint_indices:
                            p.setJointMotorControl2(robot_id, joint_indices['joint_2'], p.POSITION_CONTROL, targetPosition=j2)
                        if 'joint_gripper' in joint_indices:
                            p.setJointMotorControl2(robot_id, joint_indices['joint_gripper'], p.POSITION_CONTROL, targetPosition=gripper)
            except ValueError:
                pass
        time.sleep(0.01)
except KeyboardInterrupt:
    print("\nSimulación finalizada por el usuario.")
    ser.close()
    p.disconnect()
