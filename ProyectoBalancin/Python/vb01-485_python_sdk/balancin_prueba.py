from time import sleep
import datetime
import RPi.GPIO as GPIO
import pigpio
import device_model
from pynput import keyboard
import os

"""
    Variables del Programa
"""
file = None
infoFile = ''
horaYFechaActual = ''

mostrarValores = False
guardarValores = False

opc = '0'
speed = 1000

"""
    Funcion para Crear un Archivo donde se guardaran los valores del Acelerometro
"""
def AbrirArchivo():
    global file
    global horaYFechaActual
    global infoFile

    #Creamos un nuevo archivo TXT que tendrá como nombre la hora y fecha actual,
    horaYFechaActual = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    file = open(horaYFechaActual + ".txt", "w")
    
    #Encabezados del archivo
    infoFile = "VelocidadX\tVelocidadY\tVelocidadZ"
    infoFile +=  "\tÁnguloX\tÁnguloY\tÁnguloZ"
    infoFile += "\tTemperatura"
    infoFile += "\tDesplazamientoX\tDesplazamientoY\tDesplazamientoZ"
    infoFile += "\tFrecuenciaX\tFrecuenciaY\tFrecuenciaZ"
    infoFile += "\r\n"
    file.write(infoFile)

"""
    Función para Cerrar el Archivo
"""
def CerrarArchivo():
    global file

    if file is not None:
        
        file.close()
        file = None
    
"""
    Funcion para imprimir los valores del acelerometro
"""
def ImprimirValoresAcelerometro():
    global file
    global infoFile
    global mostrarValores
    global guardarValores
    
    # Impresión de los valores del acelerometro
    if mostrarValores:
        # v：振动速度 a：振动角度 t：温度 s：振动位移 f：振动频率
        # v:Velocidad de vibración a: Ángulo de vibración t: Temperatura s: Desplazamiento de vibración f: Frecuencia de vibración
        print("vx:{} vy:{} vz:{} ax:{} ay:{} az:{} t:{} sx:{} sy:{} sz:{} fx:{} fy:{} fz:{}".format(device.get("58"),device.get("59"),device.get("60"),device.get("61"),device.get("62"),device.get("63"),device.get("64"),device.get("65"),device.get("66"),device.get("67"),device.get("68"),device.get("69"),device.get("70")))
    
    if guardarValores and file is not None:
        #Guardo los valores en un archivo TXT
        infoFile = str(format(device.get("58"))) + "\t\t" + str(format(device.get("59"))) + "\t\t" + str(format(device.get("60"))) + "\t\t"
        infoFile += str(format(device.get("61"))) + "\t\t" + str(format(device.get("62"))) + "\t\t" + str(format(device.get("63"))) + "\t\t"
        infoFile += str(format(device.get("64"))) + "\t\t"
        infoFile += str(format(device.get("65"))) + "\t\t" + str(format(device.get("66"))) + "\t\t" + str(format(device.get("67"))) + "\t\t"
        infoFile += str(format(device.get("68"))) + "\t\t" + str(format(device.get("69"))) + "\t\t" + str(format(device.get("70"))) + "\t\t"
        infoFile += "\r\n"
        
        file.write(infoFile)
        #file.close()

"""
    Función para mostrar un MENU cuando se presione la tecla 'a'
"""
def on_press(key):
    global mostrarValores
    global guardarValores
    global speed
    global opcS
    
    i=0
    
    if key == keyboard.KeyCode.from_char('a'):
        #Cuando se presiona la tecla 'a' minuscula se muestre un menú
        mostrarValores = False
        opc = '0'
        
        while not mostrarValores and opc!='2':
            
            if(opc!='1'):
        
                print('\nMENU')
                print('1. Cambiar velocidad del motor')
                print('2. Terminar Programa')
                print('3. Salir\n')
                print('Ingrese una opcion: ')
                opc = input()
            
            if opc == '1':
                #Control de velocidad del motor
                print('\nCAMBIAR VELOCIDAD DEL MOTOR')
                print('Ingrese un valor de 1000 a 2000: ')
                speed = int(input())
                
                if speed >= 1000 and speed <= 2000:
                    pi.set_servo_pulsewidth(ESC_GPIO,speed)
                    mostrarValores = True
                else:
                    print('El valor ingresado no está dentro del rango de 1000 a 2000, intente de nuevo.\n')
                    opc='1'
                    mostrarValores = False
            elif opc == '2':
                #Terminar Programa
                i=speed
                for i in range(speed, 995, -5):
                    pi.set_servo_pulsewidth(ESC_GPIO,i)
                    sleep(0.2)
                
                pi.set_servo_pulsewidth(ESC_GPIO,0)
                
                mostrarValores = False
                guardarValores = False
                print("Programa terminado")
                sleep(0.5)
            elif opc == '3':
                #Salir del menu
                print("Usted ha salido del menú\n")
                mostrarValores = True
            else:
                print("Opción no valida\n")
                mostrarValores = False
                
def FuncionPrincipal():
    global mostrarValores
    global guardarValores
    
    mostrarValores = True
    guardarValores = True
     
    AbrirArchivo()
    
    #file.close()
   
    while guardarValores:
        ImprimirValoresAcelerometro()
        sleep(0.2)

    CerrarArchivo()
      
try:
    # Inicializar el listener para detectar eventos del teclado
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

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

    FuncionPrincipal()

    device.stopLoopRead()
    device.closeDevice()
    device = None
    os._exit(0)

        
except KeyboardInterrupt:
    #Terminar Programa
    pi.set_servo_pulsewidth(ESC_GPIO,0)
    mostrarValores = False
    guardarValores = False
    CerrarArchivo()
    print("Programa terminado!")
    os._exit(0)
except Exception as e:
    # Manejar excepciones
    print("Ocurrió un error: ", e)
