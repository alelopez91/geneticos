import os
import random
import pygame
import myconstants
from cuadrante import Cuadrante
from obstaculo import Obstaculo
from pasto import Pasto


# Iniciazlizar pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Configurar pantalla
pygame.display.set_caption("Cortadora de Cesped Inteligente!")
pantalla = pygame.display.set_mode((256, 192))
# pantalla2 = pygame.display.set_mode((256, 192))

fps = pygame.time.Clock()
obstaculos = [] # Contenedor de obstaculos
pastos = []     # Contenedor de pasto

filas_mapa = 6 #La longitud del material genetico de cada individuo
col_mapa = 8
num = 1 #La cantidad de individuos que habra en la poblacion
pressure = 3 #Cuantos individuos se seleccionan para reproduccion. Necesariamente mayor que 2
mutation_chance = 0.2 #La probabilidad de que un individuo mute

mapa = []

def individual(min, max): #funcionando
  ind = []
  x = 0
  y = 0
  # Crea un individuo
  for i in range(filas_mapa):
    ind.append([])
    x = 0
    for j in range(col_mapa):
      if i==0 or j==0 or i==filas_mapa-1 or j==col_mapa-1:
        ind[i].append((0,x,y))
      else:
        ind[i].append((random.randint(min, max),x,y))
      x+=32
    y+=32
  return ind

def crear_poblacion(): #funcionando
  # Crea una poblacion nueva de individuos
    return [individual(0,1) for i in range(num)]

def calcularFitness(individual): #falta hacer
  # Calcula el fitness de un individuo concreto.
  fitness = 0
  for i in range(len(individual)):
      if individual[i] == modelo[i]:
          fitness += 1

  return fitness

def selection_and_reproduction(population): #falta hacer
    """
        Puntua todos los elementos de la poblacion (population) y se queda con los mejores
        guardandolos dentro de 'selected'.
        Despues mezcla el material genetico de los elegidos para crear nuevos individuos y
        llenar la poblacion (guardando tambien una copia de los individuos seleccionados sin
        modificar).
  
        Por ultimo muta a los individuos.
  
    """
    puntuados = [ (calcularFitness(i), i) for i in population] #Calcula el fitness de cada individuo, y lo guarda en pares ordenados de la forma (5 , [1,2,1,1,4,1,8,9,4,1])
    puntuados = [i[1] for i in sorted(puntuados)] #Ordena los pares ordenados y se queda solo con el array de valores
    population = puntuados
  
    selected =  puntuados[(len(puntuados)-pressure):] #Esta linea selecciona los 'n' individuos del final, donde n viene dado por 'pressure'
  
  
  
    #Se mezcla el material genetico para crear nuevos individuos
    for i in range(len(population)-pressure):
        punto = random.randint(1,largo-1) #Se elige un punto para hacer el intercambio
        padre = random.sample(selected, 2) #Se eligen dos padres
          
        population[i][:punto] = padre[0][:punto] #Se mezcla el material genetico de los padres en cada nuevo individuo
        population[i][punto:] = padre[1][punto:]
  
    return population #El array 'population' tiene ahora una nueva poblacion de individuos, que se devuelven



aux = 0
x = y = 0

for row in myconstants.ENTORNO7:
  mapa.append([])
  for col in row:
    if col == "W":
      mapa[aux].append(Cuadrante(x,y,(x,y-32),(x,y+32),(x-32,y),(x+32,y),'o'))
      obstaculos.append(Obstaculo((x, y)))
    if col == "P":
      mapa[aux].append(Cuadrante(x,y,(x,y-32),(x,y+32),(x-32,y),(x+32,y),'p'))
      pastos.append(Pasto((x, y)))
    x += 32

  y += 32
  x = 0
  aux +=1

running = True
# print(mapa[1][1].cuadrante_arriba)
# population = crear_poblacion()#Inicializar una poblacion
# print("Poblacion Inicial:\n%s"%(population)) #Se muestra la poblacion inicial
# for i in range(len(population)):
  # print(population[i].[0])


while running:
  fps.tick(60)
  
  for e in pygame.event.get():
    if e.type == pygame.QUIT:
      running = False
    if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
      running = False
  
  # population = crear_poblacion() #Inicializar una poblacion
  # print("Poblacion Inicial:\n%s"%(population)) #Se muestra la poblacion inicial
    
    
  # #Se evoluciona la poblacion
  # for i in range(30):
  #     population = selection_and_reproduction(population)
    
  # print("\nPoblacion Final:\n%s"%(population)) #Se muestra la poblacion evolucionada
  # print("\n\n")

  # Dibujar pantalla
  pantalla.fill((0, 0, 0))
  # pantalla2.fill((0, 0, 0))

  for obs in obstaculos:
    # if cortadora.rect.colliderect(obs.rect) and cortadora.motor == True:
      # obs.tocado = True

    if obs.tocado == True:
      pygame.draw.rect(pantalla, (200, 100, 100), obs.rect)
    else:
      pygame.draw.rect(pantalla, (255, 255, 255), obs.rect)
 
  for pasto in pastos:
    # if pasto.rect.colliderect(cortadora.rect) and pasto.tocado == False  and cortadora.motor == True:
      # pasto.tocado = True
 
    if pasto.tocado == True:
      pygame.draw.rect(pantalla, (000, 255, 000), pasto.rect)
    else:
      pygame.draw.rect(pantalla, (000, 128, 000), pasto.rect)

  # for pops in population:
    # if pops[0] == 1:
      # pygame.draw.rect(pantalla2, (255, 0, 0), (pops[1], pops[2], 32, 32))
    # else:
      # pygame.draw.rect(pantalla2, (000, 128, 000), (pops[1], pops[2], 32, 32))

  pygame.display.flip()


