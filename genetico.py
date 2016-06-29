import os
import random
import time
import pygame
import myconstants
from cuadrante_mapa import Cuadrante_mapa
from cuadrante_individuo import Cuadrante_individuo
from obstaculo import Obstaculo
from pasto import Pasto


# Iniciazlizar pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Configurar pantalla
pygame.display.set_caption("Cortadora de Cesped Inteligente!")
pantalla = pygame.display.set_mode((256, 192))

fps = pygame.time.Clock()
obstaculos = [] # Contenedor de obstaculos
pastos = []     # Contenedor de pasto

filas_mapa = 6 #La longitud del material genetico de cada individuo
col_mapa = 8
num = 3 #La cantidad de individuos que habra en la poblacion
pressure = 3 #Cuantos individuos se seleccionan para reproduccion. Necesariamente mayor que 2
mutation_chance = 0.2 #La probabilidad de que un individuo mute

mapa = []

def individual(): #funcionando
  ind = []
  x = 0
  y = 0
  # Crea un individuo
  for i in range(filas_mapa):
    ind.append([])
    x = 0
    for j in range(col_mapa):
      if i==0 or j==0 or i==filas_mapa-1 or j==col_mapa-1:
        ind[i].append(Cuadrante_individuo(False,x,y))
      else:
        ind[i].append(Cuadrante_individuo(random.choice([True, False]),x,y))
      x+=32
    y+=32
  return ind

def crear_poblacion(): #funcionando
  # Crea una poblacion nueva de individuos
    return [individual() for i in range(num)]

def calcular_fitness(individuo, x_base, y_base, x_inicial, y_inicial):
  fitness = 100
  tiene_base = False
  tiene_inicio = False
  distancia = 0
  revisados = []
  caminos_pendientes = []
  solucion = []


  #Regla 1: Se genero la base y la posicion inicial. Se suma 5 al fitness por cada uno
  #Regla 2: Menor distancia recorrida. Por cada cuadrante pisado se resta uno al fitness
  #Regla 3: Conectividad de los cuadrantes. Se suma por cada cuadrante conectado. Si existe un
  # segmento desde la pos inicial a la base se suma un bonus de 10 al fitness
  
  for cuads in individuo:
    for c in cuads:
      if c.pertenece == True:
        fitness -= 1
        if c.x == x_base and c.y == y_base:
          fitness += 6
          tiene_base = True
        if c.x == x_inicial and c.y == y_inicial:
          fitness += 6
          tiene_inicio = True

  return fitness

def selection_and_reproduction(population): #falta hacer
    """
        Puntua todos los elementos de la poblacion (population) y se queda con los mejores
        guardandolos dentro de 'selected'.
        Despues mezcla el material genetico de los elegidos para crear nuevos individuos y
        llenar la poblacion (guardando tambien una copia de los individuos seleccionados sin
        modificar).
  # 
        Por ultimo muta a los individuos.
  # 
    """
    puntuados = [ (calcular_fitness(i), i) for i in population] #Calcula el fitness de cada individuo, y lo guarda en pares ordenados de la forma (5 , [1,2,1,1,4,1,8,9,4,1])
    puntuados = [i[1] for i in sorted(puntuados)] #Ordena los pares ordenados y se queda solo con el array de valores
    population = puntuados
  # 
    selected =  puntuados[(len(puntuados)-pressure):] #Esta linea selecciona los 'n' individuos del final, donde n viene dado por 'pressure'
  # 
  # 
  # 
    #Se mezcla el material genetico para crear nuevos individuos
    for i in range(len(population)-pressure):
        punto = random.randint(1,largo-1) #Se elige un punto para hacer el intercambio
        padre = random.sample(selected, 2) #Se eligen dos padres
          # 
        population[i][:punto] = padre[0][:punto] #Se mezcla el material genetico de los padres en cada nuevo individuo
        population[i][punto:] = padre[1][punto:]
  # 
    return population #El array 'population' tiene ahora una nueva poblacion de individuos, que se devuelven

def dibujar_mapa():
  for obs in obstaculos:
    if obs.tocado == True:
      pygame.draw.rect(pantalla, (200, 100, 100), obs.rect)
    else:
      pygame.draw.rect(pantalla, (255, 255, 255), obs.rect)
 
  for pasto in pastos: 
    if pasto.tocado == True:
      pygame.draw.rect(pantalla, (000, 255, 000), pasto.rect)
    else:
      pygame.draw.rect(pantalla, (000, 128, 000), pasto.rect)

def dibujar_population(population):
  for pops in population:
    for cuads in pops:
      for c in cuads:
        rectangulo = pygame.Rect(c.x, c.y, 32, 32)
        if c.pertenece == True:
          pygame.draw.rect(pantalla, (255, 0, 0), rectangulo)
        else:
          pygame.draw.rect(pantalla, (000, 128, 000), rectangulo)
      # time.sleep(1)

def imprimir_population(population):
  for pops in population:
    for cuads in pops:
      for c in cuads:
        print(c.pertenece, c.x, c.y)

def imprimir_individuo(individuo):
  for cuads in individuo:
    for c in cuads:
      print(c.pertenece, c.x, c.y)

#Comienza programa
aux = 0
x = y = 0

for row in myconstants.ENTORNO7:
  mapa.append([])
  for col in row:
    if col == "W":
      mapa[aux].append(Cuadrante_mapa(x,y,(x,y-32),(x,y+32),(x-32,y),(x+32,y),'o'))
      obstaculos.append(Obstaculo((x, y)))
    if col == "P":
      mapa[aux].append(Cuadrante_mapa(x,y,(x,y-32),(x,y+32),(x-32,y),(x+32,y),'p'))
      pastos.append(Pasto((x, y)))
    x += 32

  y += 32
  x = 0
  aux +=1

running = True
population = crear_poblacion()#Inicializar una poblacion
imprimir_population(population)


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
  dibujar_population(population);
  pygame.display.flip()


