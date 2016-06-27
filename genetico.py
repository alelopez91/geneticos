import os
import random
import pygame
import algoritmos
import myconstants
from obstaculo import Obstaculo
from pasto import Pasto


# Iniciazlizar pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Configurar pantalla
pygame.display.set_caption("Cortadora de Cesped Inteligente!")
pantalla = pygame.display.set_mode((640, 480))

fps = pygame.time.Clock()
obstaculos = [] # Contenedor de obstaculos
pastos = []     # Contenedor de pasto
mapa = []


aux = 0
x = y = 0

for row in myconstants.ENTORNO6:
  mapa.append([])
  for col in row:
    if col == "W":
      mapa[aux].append(Obstaculo((x, y)))
      obstaculos.append(Obstaculo((x, y)))
    if col == "P":
      mapa[aux].append(Pasto((x, y)))
      pastos.append(Pasto((x, y)))
    x += 32

  y += 32
  x = 0
  aux +=1

running = True

while running:
  fps.tick(60)
  
  for e in pygame.event.get():
    if e.type == pygame.QUIT:
      running = False
    if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
      running = False
  
  population = algoritmos.crearPoblacion()#Inicializar una poblacion
  print("Poblacion Inicial:\n%s"%(population)) #Se muestra la poblacion inicial
    
    
  #Se evoluciona la poblacion
  for i in range(100):
      population = selection_and_reproduction(population)
    
  print("\nPoblacion Final:\n%s"%(population)) #Se muestra la poblacion evolucionada
  print("\n\n")

  # Dibujar pantalla
  pantalla.fill((0, 0, 0))

  for obs in obstaculos:
    # if cortadora.rect.colliderect(obs.rect) and cortadora.motor == True:
    #   obs.tocado = True

    if obs.tocado == True:
      pygame.draw.rect(pantalla, (200, 100, 100), obs.rect)
    else:
      pygame.draw.rect(pantalla, (255, 255, 255), obs.rect)

  for pasto in pastos:
    # if pasto.rect.colliderect(cortadora.rect) and pasto.tocado == False  and cortadora.motor == True:
    #   pasto.tocado = True

    if pasto.tocado == True:
      pygame.draw.rect(pantalla, (000, 255, 000), pasto.rect)
    else:
      pygame.draw.rect(pantalla, (000, 128, 000), pasto.rect)

  # pygame.draw.rect(pantalla, (0, 96, 96), cortadora.rect)
  pygame.display.flip()
