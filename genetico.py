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
pantalla = pygame.display.set_mode((640, 480))

fps = pygame.time.Clock()
obstaculos = [] # Contenedor de obstaculos
pastos = []     # Contenedor de pasto

filas_mapa = 15 #La longitud del material genetico de cada individuo
col_mapa = 20
num = 10 #La cantidad de individuos que habra en la poblacion
pressure = 3 #Cuantos individuos se seleccionan para reproduccion. Necesariamente mayor que 2
mutacion_prob = 20 #La probabilidad de que un individuo mute
generaciones = 2 #Cantidad de generaciones que se producen

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
    print("Poblacion inicial: " + str(num))
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
          fitness += 5
          tiene_base = True
        if c.x == x_inicial and c.y == y_inicial:
          fitness += 5
          tiene_inicio = True

  return fitness

def seleccion_and_reproduccion(population): #falta hacer
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
    puntuados = []
    for ind in population:
      puntuados.append((calcular_fitness(ind, 32, 32, 64, 96),ind)) #Calcula el fitness de cada individuo, y lo guarda en pares ordenados de la forma (5 , [1,2,1,1,4,1,8,9,4,1])
    puntuados = [i[1] for i in sorted(puntuados)] #Ordena los pares ordenados y se queda solo con el array de valores
    
    population = puntuados
  # 
    selected =  puntuados[(len(puntuados)-pressure):] #Esta linea selecciona los 'n' individuos del final, donde n viene dado por 'pressure'
  # 
  # 
  # 
    #Se mezcla el material genetico para crear nuevos individuos    
    
    for k in range(len(population)-pressure):
      hijo_1 = []
      hijo_2 = []
      fila_1 = []
      fila_2 = []
      punto_corte = False
  
      punto_i = random.randint(0,filas_mapa-1) #Se elige un punto para hacer el intercambio
      punto_j = random.randint(0,col_mapa-1) #Se elige un punto para hacer el intercambio
      padres = random.sample(selected, 2) #Se eligen dos padres
      for i in range(len(padres)):
        for f in range(filas_mapa):
          for c in range(col_mapa):
            objeto = padres[i][f][c]
            objeto_1 = padres[0][f][c]
            objeto_2 = padres[1][f][c]
            if objeto.x == punto_i*32 and objeto.y == punto_j*32:
              punto_corte = True
            if punto_corte == False:
              fila_1.append(objeto_1)
              fila_2.append(objeto_2)
            else:
              fila_2.append(objeto_1)
              fila_1.append(objeto_2)
          hijo_1.append(fila_1)
          hijo_2.append(fila_2)
          # print(hijo_1)
          # print(hijo_2)
          fila_1 = []
          fila_2 = []
        if buscar_repetidos(population, hijo_1) == False:
          population.append(hijo_1)
          hijo_1 = []
        if buscar_repetidos(population, hijo_1) == False:
          population.append(hijo_2)
          hijo_2 = []
    print("Cantidad de seleccionados: "+str(len(population)))
      
    return population

def mutacion(population):
    """
        Se mutan los individuos al azar. Sin la mutacion de nuevos genes nunca podria
        alcanzarse la solucion.
    """
    elemento = []
    cant_mutaciones = int(filas_mapa * col_mapa * 0.02)
    cant_mutantes = 0
    for inds in population:
      if random.randint(1,100) <= mutacion_prob:
        cant_mutantes += 1
        elemento = inds
        for m in range(cant_mutaciones):
          punto_i = random.randint(0,filas_mapa-1)
          punto_j = random.randint(0,col_mapa-1)
          for cuads in elemento:
            for c in cuads:
              if c.x == punto_i*32 and c.y == punto_j*32:
                if c.pertenece == True:
                  c.pertenece = False
                else:
                  c.pertenece = True
        if buscar_repetidos(population,elemento) == False:
          population.append(elemento)
          elemento = []
    print("Cantidad de mutaciones: " + str(cant_mutantes))

    return population

def buscar_repetidos(population, individuo):
  es_copia = True
  for a in range(len(population)):
    for b in range(filas_mapa):
      for d in range(col_mapa):
        popu = population[a][b][d]
        print(popu.pertenece)
        copia = individuo[b][d]
        print(copia.pertenece)
        if popu.pertenece != copia.pertenece:
          es_copia = False
  return es_copia
              
    
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
  k=1
  pantalla.fill((0, 0, 0))
  time.sleep(1)
  for pops in population:
    print("Individuo " + str(k) + " de " + str(len(population)))
    dibujar_individuo(pops)
    pygame.display.update()
    time.sleep(.5)
    k+=1

def dibujar_individuo(individuo):
  for filas in individuo:
    for c in filas:
      rectangulo = pygame.Rect(c.x, c.y, 32, 32)
      if c.pertenece == True:
        pygame.draw.rect(pantalla, (255, 0, 0), rectangulo)
      else:
        pygame.draw.rect(pantalla, (000, 128, 000), rectangulo)

def imprimir_population(population):
  i=1
  for pops in population:
    print("#######################   Individuo %d  #########################" % i)
    for cuads in pops:
      for c in cuads:
        print(c.pertenece, c.x, c.y)
    i+=1

def imprimir_individuo(individuo):
  for cuads in individuo:
    for c in cuads:
      print(c.pertenece, c.x, c.y)

#Comienza programa
population = crear_poblacion() #Inicializar una poblacion
  #Se evoluciona la poblacion
for g in range(generaciones):
  population = seleccion_and_reproduccion(population)
  population = mutacion(population)

dibujar_population(population)
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

while running:
  fps.tick(60)
  
  for e in pygame.event.get():
    if e.type == pygame.QUIT:
      running = False
    if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
      running = False
  

  # Dibujar pantalla
  pygame.display.flip()


