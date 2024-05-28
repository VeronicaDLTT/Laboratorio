from time import sleep
import datetime
import RPi.GPIO as GPIO
import pigpio
import device_model
import sys
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

file = None
horaYFechaActual = ''

"""
    Funcion para imprimir los valores del acelerometro
"""
def ImprimirValoresAcelerometro():
    global file
    global horaYFechaActual
    
    # Impresión de los valores del acelerometro
    if band:
        # v：振动速度 a：振动角度 t：温度 s：振动位移 f：振动频率
        # v:Velocidad de vibración a: Ángulo de vibración t: Temperatura s: Desplazamiento de vibración f: Frecuencia de vibración
        print("vx:{} vy:{} vz:{} ax:{} ay:{} az:{} t:{} sx:{} sy:{} sz:{} fx:{} fy:{} fz:{}".format(device.get("58"),device.get("59"),device.get("60"),device.get("61"),device.get("62"),device.get("63"),device.get("64"),device.get("65"),device.get("66"),device.get("67"),device.get("68"),device.get("69"),device.get("70")))
        
    #Guardo los valores en un archivo TXT
    file = open(horaYFechaActual + ".txt", "a+")
    
    infoFile = str(format(device.get("58"))) + "\t\t" + str(format(device.get("59"))) + "\t\t" + str(format(device.get("60"))) + "\t\t"
    infoFile += str(format(device.get("61"))) + "\t\t" + str(format(device.get("62"))) + "\t\t" + str(format(device.get("63"))) + "\t\t"
    infoFile += str(format(device.get("64"))) + "\t\t"
    infoFile += str(format(device.get("65"))) + "\t\t" + str(format(device.get("66"))) + "\t\t" + str(format(device.get("67"))) + "\t\t"
    infoFile += str(format(device.get("68"))) + "\t\t" + str(format(device.get("69"))) + "\t\t" + str(format(device.get("70"))) + "\t\t"
    infoFile += "\r\n"
    
    file.write(infoFile)
    file.close()

"""
    Función para mostrar un MENU cuando se presione la tecla 'a'
"""
def on_press(key):
    global band
    
    if key == keyboard.KeyCode(97):
        #Cuando se presiona la tecla 'a' minuscula se muestre un menú
        band = False
        opc = '0'
        
        while(band==False and opc!='2'):
            
            if(opc!='1'):
        
                print('\nMENU')
                print('1. Cambiar velocidad del motor')
                print('2. Terminar Programa')
                print('3. Salir\n')
                print('Ingrese una opcion: ')
                opc = input()
            
            if opc == '1':
                #Control de velocidad del motor
                print('\nCambiar velocidad del motor')
                print('Ingrese un valor de 1000 a 2000: ')
                speed = input()
                speed = float(speed)
                if speed >= 1000 and speed <= 2000:
                    pi.set_servo_pulsewidth(ESC_GPIO,speed)
                    band = True
                else:
                    print('El valor ingresado no está dentro del rango de 1000 a 2000, intente de nuevo.\n')
                    opc='1'
                    band = False
            elif opc == '2':
                #Terminar Programa
                pi.set_servo_pulsewidth(ESC_GPIO,0)
                band = False
                print("Programa terminado")
                sys.exit(0)
            elif opc == '3':
                #Salir del menu
                print("Usted ha salido del menú\n")
                band = True
            else:
                print("Opción no valida\n")
                band = False

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
    pi.set_servo_pulsewidth(ESC_GPIO,1000)
    sleep(0.1)
    
    #Creamos un nuevo archivo TXT que tendrá como nombre la hora y fecha actual,
    #para guardar los datos del acelerometro
    horaYFechaActual = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) 
    file = open(horaYFechaActual + ".txt", "w")                                                                      
    infoFile = "VelocidadX\tVelocidadY\tVelocidadZ"
    infoFile +=  "\tÁnguloX\tÁnguloY\tÁnguloZ"
    infoFile += "\tTemperatura"
    infoFile += "\tDesplazamientoX\tDesplazamientoY\tDesplazamientoZ"
    infoFile += "\tFrecuenciaX\tFrecuenciaY\tFrecuenciaZ"
    infoFile += "\r\n"
    file.write(infoFile)
    file.close()

    band = True

    while True:

        ImprimirValoresAcelerometro()
            
        sleep(0.2)
    
except KeyboardInterrupt:
    #Terminar Programa
    pi.set_servo_pulsewidth(ESC_GPIO,0)
    print("Programa terminado")
    band = Falsea
    