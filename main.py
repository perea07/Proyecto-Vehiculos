import cv2
import mysql.connector
import numpy as np
from time import sleep
from constantes import *

lista = []
mi_path = "../Vehicle-Counter/carros-contados.txt"
suma_carros = 0
#Funcion para tomar el centro del objeto (carro)
def centro_carro(x, y, largura, altura):
    """
    :param x: x do objeto
    :param y: y do objeto
    :param largura: largura do objeto
    :param altura: altura do objeto
    :return: tupla que contém as coordenadas do centro de um objeto
    """
    x1 = largura // 2
    y1 = altura // 2
    cx = x + x1
    cy = y + y1
    return cx, cy

def set_info(detec):
    global carros
    for (x, y) in detec:
        if (pos_linha + offset) > y > (pos_linha - offset):
            carros += 1
            lista.append(carros)    
            cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (0, 127, 255), 3)
            detec.remove((x, y))
            #print("Carros detectados hasta el momento " + str(carros))
            #Conexión
            # conexion1=mysql.connector.connect(host="db4free.net", 
            #                       user="dbpruebas78", 
            #                       passwd="E=mc2a+b0929", 
            #                       database="dbpruebas78")
            # cursor1=conexion1.cursor()
            # sql="insert into estacion(n_carro) values (%s)"
            # datos= (carros,)
            # cursor1.execute(sql, datos)
            # conexion1.commit()
            # conexion1.close()
            ######
            
def show_info(frame1, dilatada):
    text = f'Carros: {carros}'
    cv2.putText(frame1, text, (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    cv2.imshow("Contador de Vehiculos", frame1)
    #cv2.imshow("Detectar", dilatada)


carros = camiones = 0
#cap = cv2.VideoCapture('video.mp4')
cap= cv2.VideoCapture("rtsp://admin:admin12345@192.168.0.101:554")
subtracao = cv2.bgsegm.createBackgroundSubtractorMOG() 
#subtracao = cv2.createBackgroundSubtractorMOG2()
while True:
    ret, frame1 = cap.read()  # Toma cada cuadro del video
    tiempo = float(1 / delay) #Tiempo guardado en una variable
    sleep(tiempo)  # Relentizar el video (video de la camara)
    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY) #Toma el marco y conviértalo en blanco y negro
    blur = cv2.GaussianBlur(grey, (3, 3), 5)  # Hace un desenfoque para tratar de eliminar las imperfecciones de la imagen.
    img_sub = subtracao.apply(blur)  # Resta la imagen aplicada en el desenfoque.
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))  # "Espesa" lo que queda de la resta
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (
        5, 5))  # Crea una matriz de 5x5, donde el formato de matriz entre 0 y 1 forme una elipse en el interior
    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)  # Intenta llenar todos los "agujeros" en la imagen.
    dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)

    contorno, img = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (255, 127, 0), 3)
    for (i, c) in enumerate(contorno):
        (x, y, w, h) = cv2.boundingRect(c)
        validar_contorno = (w >= largura_min) and (h >= altura_min)
        if not validar_contorno:
            continue

        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        centro = centro_carro(x, y, w, h)
        detec.append(centro)
        cv2.circle(frame1, centro, 4, (0, 0, 255), -1)
      
    set_info(detec)
    show_info(frame1, dilatada)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
cap.release()

for d in lista:
    suma_carros = 0
    suma_carros += d

file = open(mi_path, 'a+')
file.write(str(suma_carros))
file.close()
print(suma_carros)