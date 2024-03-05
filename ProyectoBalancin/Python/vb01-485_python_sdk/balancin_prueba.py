from time import sleep
import RPi.GPIO as GPIO
import pigpio
import device_model
from pynput import keyboard

"""
    WTVB01-485示例 Example
"""

# region Common Register Address Comparison Table
"""

hex    dec      describe        describe en

0x00    0       保存/重启/恢复       SAVE
0x04    4       串口波特率          BAUD

0x1A    26      设备地址            IICADDR

0x3A    58      振动速度x           VX
0x3B    59      振动速度y           VY
0x3C    60      振动速度z           VZ

0x3D    61      振动角度x           ADX
0x3E    62      振动角度y           ADY
0x3F    63      振动角度z           ADZ

0x40    64      温度               TEMP

0x41    65      振动位移x           DX
0x42    66      振动位移y           DY
0x43    67      振动位移z           DZ    

0x44    68      振动频率x           HZX                
0x45    69      振动频率y           HZY
0x46    70      振动频率z           HZZ

0x63    99      截止频率            CUTOFFFREQI
0x64    100     截止频率            CUTOFFFREQF
0x65    101     检测周期            SAMPLEFREQ

"""
# endregion

"""
    Funcion para imprimir los valores del acelerometro
"""
def ImprimirValoresAcelerometro():
    # Impresión de los valores del acelerometro
    if band:
        # v：振动速度 a：振动角度 t：温度 s：振动位移 f：振动频率
        print("vx:{} vy:{} vz:{} ax:{} ay:{} az:{} t:{} sx:{} sy:{} sz:{} fx:{} fy:{} fz:{}".format(device.get("58"),device.get("59"),device.get("60"),device.get("61"),device.get("62"),device.get("63"),device.get("64"),device.get("65"),device.get("66"),device.get("67"),device.get("68"),device.get("69"),device.get("70")))

"""
    Función para cambiar la velocidad del motor cuando se presione la tecla 'a'
"""
def on_press(key):
    global band
    
    if key == keyboard.KeyCode(97):
        band = False
        
        #Control de velocidad del motor
        speed = input("Velocidad: ")
        speed = float(speed)
        pi.set_servo_pulsewidth(ESC_GPIO,speed)
        
        band = True

# Inicializar el listener fuera del bucle
listener = keyboard.Listener(on_press=on_press)
listener.start()

try:
    
    """
        Configuración del acelerometro
    """
    # Get the device model
    device = device_model.DeviceModel("USB-SERIAL CH340", "/dev/ttyUSB0", 9600, 0x50) #Poner el numero de puerto serial que corresponda
    # Turn on the device
    device.openDevice()
    # Enable loop reading
    device.startLoopRead()
    sleep(0.5)

    """
        Configuración del motor
    """
 
    # Configuracion GPIO
    GPIO.setmode(GPIO.BCM)
    pi = pigpio.pi()
    ESC_GPIO = 18 #Pin 12 de la Raspberry
    pi.set_servo_pulsewidth(ESC_GPIO,0)
    sleep(0.1)

    band = True

    while True:

        ImprimirValoresAcelerometro()
            
        sleep(0.2)
    
except KeyboardInterrupt:
    #Terminar Programa
    pi.set_servo_pulsewidth(ESC_GPIO,0)
    print("Programa terminado")
    band = False
    