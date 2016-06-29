import pygame

class Cuadrante_mapa(object):
    
  def __init__(self, pos_x, pos_y, vec_arr, vec_aba, vec_izq, vec_der, tipo):
    self.posicion_x = pos_x
    self.posicion_y = pos_y
    self.cuadrante_arriba = vec_arr
    self.cuadrante_abajo = vec_aba
    self.cuadrante_izquierda = vec_izq
    self.cuadrante_derecha = vec_der
    self.tipo = tipo