import os
import random
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
# pantalla = pygame.display.set_mode((256, 192))

fps = pygame.time.Clock()
obstaculos = [] # Contenedor de obstaculos
pastos = []     # Contenedor de pasto

filas_mapa = 10 #La longitud del material genetico de cada individuo
col_mapa = 10
num = 1 #La cantidad de individuos que habra en la poblacion
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
  caminos = 0
  revisados = []
  caminos_pendientes = []
  solucion = []
  izq = False
  arr = False
  aba = False
  der = False


  #Regla 1: Se genero la base y la posicion inicial. Se suma 5 al fitness por cada uno
  for cuads in individuo:
    for c in cuads:
      if c.x == x_base and c.y == y_base:
        fitness += 5
        tiene_base = True
      if c.x == x_inicial and c.y == y_inicial:
        fitness += 5
        tiene_inicio = True


  #Regla 2: Menor distancia recorrida. Por cada cuadrante pisado se resta uno al fitness
  #Regla 3: Conectividad de los cuadrantes. Se suma por cada cuadrante conectado. Si existe un
  # segmento desde la pos inicial a la base se suma un bonus de 10 al fitness
  if tiene_base == True and tiene_inicio == True:
    for cuads in individuo:
      for c in cuads:
        if c.pertenece == True:
          distancia += 1
          fitness -= 1
          if c.x == x_base and c.y == y_base:
            if buscar_der(individuo,c.x,c.y) == True:
              izq = True
              caminos +=1
            else:
              izq = False
            if buscar_aba(individuo,c.x,c.y) == True:
              arr = True
              caminos +=1
            else:
              arr = False
            if buscar_izq(individuo,c.x,c.y) == True:
              der = True
              caminos +=1
            else:
              der = False
            if buscar_arr(individuo,c.x,c.y) == True:
              aba = True
              caminos +=1
            else:
              aba = False
            if caminos > 1:
              caminos_pendientes.append(c)
            if caminos == 1:
              solucion.append(c)
            revisados.append(c)
          else:
            if der == False:
              if buscar_der(individuo,c.x,c.y) == True:
                izq = True
                caminos +=1
              else:
                izq = False
            if aba == False:            
              if buscar_aba(individuo,c.x,c.y) == True:
                arr = True
                caminos +=1
              else:
                arr = False
            if izq == False:
              if buscar_izq(individuo,c.x,c.y) == True:
                der = True
                caminos +=1
              else:
                der = False
            if arr == False:            
              if buscar_arr(individuo,c.x,c.y) == True:
                aba = True
                caminos +=1
              else:
                aba = False
            if caminos > 1:
              caminos_pendientes.append(c)
            if caminos == 1:
              solucion.append(c)
            revisados.append(c)













            
  
        
          fitness += 5
        if c.x == x_inicial and c.y == y_inicial:
          fitness += 5


  a = 0
  b = 0
  c = 0

  for cuadrante in individuo:
    if cuadrante.parte_camino == 1:
      a += 1

    if cuadrante.es_base == 1:
      b += 1

  fitness = (b * c)/a

  return fitness

def buscar_arr(individuo, pos_x, pos_y):
  for cuads in individuo:
    for c in cuads:
      if c.x == pos_x and c.y-32 == pos_y:
        if c.pertenece == True:
          return True
        else:
          return False
def buscar_aba(individuo, pos_x, pos_y):
  for cuads in individuo:
    for c in cuads:
      if c.x == pos_x and c.y+32 == pos_y:
        if c.pertenece == True:
          return True
        else:
          return False
def buscar_izq(individuo, pos_x, pos_y):
  for cuads in individuo:
    for c in cuads:
      if c.x-32 == pos_x and c.y == pos_y:
        if c.pertenece == True:
          return True
        else:
          return False
def buscar_der(individuo, pos_x, pos_y):
  for cuads in individuo:
    for c in cuads:
      if c.x+32 == pos_x and c.y == pos_y:
        if c.pertenece == True:
          return True
        else:
          return False



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

def dibujar_individuo():
  for pops in population:
    for p in pops:
      for tupla in p:
        rectangulo = pygame.Rect(tupla[1], tupla[2], 32, 32)
        if tupla[0] == 1:
          pygame.draw.rect(pantalla, (255, 0, 0), rectangulo)
        else:
          pygame.draw.rect(pantalla, (000, 128, 000), rectangulo)

def imprimir_population(population):
  for pops in population:
    for cuads in pops:
      for c in cuads:
        print(c.pertenece, c.x, c.y, c.es_base)

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
# population = crear_poblacion()#Inicializar una poblacion
# imprimir_population(population)
asd = individual()
imprimir_individuo(asd)


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
  # pantalla.fill((0, 0, 0))




  # pygame.display.flip()


