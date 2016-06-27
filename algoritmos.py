import random

filas_mapa = 6 #La longitud del material genetico de cada individuo
col_mapa = 5
num = 10 #La cantidad de individuos que habra en la poblacion
pressure = 3 #Cuantos individuos se seleccionan para reproduccion. Necesariamente mayor que 2
mutation_chance = 0.2 #La probabilidad de que un individuo mute

mapa = [filas_mapa][col_mapa]

def individual(min, max):
  # Crea un individuo
  for i in range(filas_mapa)
    for j in range(col_mapa)
      return[random.randint(min, max)]

def crearPoblacion():
  # Crea una poblacion nueva de individuos
    return [individual(0,2) for i in range(num)]

def calcularFitness(individual):
  # Calcula el fitness de un individuo concreto.
  fitness = 0
  for i in range(len(individual)):
      if individual[i] == modelo[i]:
          fitness += 1

  return fitness

def selection_and_reproduction(population):
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

