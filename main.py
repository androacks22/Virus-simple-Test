import pygame
import win32api
import win32con
import win32gui
import random
import math
import time

#declaramos algunas variables
winWidth, winHeight = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
mouseX, mouseY = 0, 0
#reemplaza "image.png" con el nombre de tu imagen
image = pygame.image.load("image.png")

#inicializamos pygame :D
from pygame.locals import *
pygame.init()

#configuramos la ventana
window_screen = pygame.display.set_mode((winWidth, winHeight), NOFRAME)
hwnd = pygame.display.get_wm_info()["window"]

#hacemos que la ventana siempre se muestre encima de todo y lo ocultamos de la barra de tareas
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TOOLWINDOW)
#hacemos transparente la ventana
win32gui.SetLayeredWindowAttributes(hwnd, 0, 0, win32con.LWA_COLORKEY)

#----------------------------------------------------------------------------------------------------------------------------------------------------------#

class obj:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.isCollide = False
        self.lastCollide = False
        
    def draw(self):
        window_screen.blit(image, (self.x - 4, self.y - 4))
    
    def moveToMouse(self):
        dx = mouseX - self.x
        dy = mouseY - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        
        if distance > 1 :
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            
    def collision(self):
        return math.dist([self.x, self.y], [mouseX, mouseY]) < 8
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------#

#almacenamos todos los objetos en un array
objects = []
#añadimos el primer objeto, estará cuando se inicie
objects.append(obj(winWidth / 2, winHeight / 2))

#la logica
def update():
    for v in objects:
        v.lastCollide = v.isCollide
        v.draw()
        v.moveToMouse()
        
        #si hay colision con uno de los objetos, se instancia otro en una posicion aleatoria
        if v.collision() :
            v.isCollide = True
            if (v.isCollide == True and v.lastCollide == False):
                objects.append(obj(random.randint(0, int(winWidth)), random.randint(0, int(winHeight))))
        else :
            v.isCollide = False

#bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    #obtenemos la posición del mouse
    mouseX, mouseY = win32api.GetCursorPos()
    
    window_screen.fill((0,0,0))
    update()
    pygame.display.update()
    
    #será mejor que si vamos a ejecutar esto en nuestra computadora...
    #limitemos la frecuencia en el que el bucle se ejecuta
    #de tal forma evitamos usar mucha cpu de forma innecesaria
    time.sleep(1/60)
