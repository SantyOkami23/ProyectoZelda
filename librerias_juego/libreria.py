import pygame
import random
import configparser

VERDE = [0, 255, 0]
ROJO = [255, 0, 0]
AZUL = [0, 0, 255]
AMARILLO = [255, 255, 0]
AZUL_2 = [0, 255, 255]
NEGRO = [0, 0, 0]
BLANCO = [255, 255, 255]
GRIS = [180, 180, 180]
GRIS2 = [192, 192, 192]

game_over = False
win_game = False
score_need = 5 # score necesario para obtener la varita
lista_terreno = []
coordenadas_cueva = []
coordenadas_generador = []
coordenadas_hueco = []
coordenadas_puas = []
coordenadas_boss = []

Arbol = pygame.image.load('librerias_juego/Arbol.png')
anciano_skin = pygame.image.load('librerias_juego/old_man.png')
coin_skin = pygame.image.load('librerias_juego/coin_zelda.png')
varita_skin = pygame.image.load('librerias_juego/varita.png')
solo_aviso = pygame.image.load('librerias_juego/Alone.jpg')
zelda_skin = pygame.image.load('librerias_juego/zelda.png')
need_coins = pygame.image.load('librerias_juego/need_coins.jpg')
espada_skin = pygame.image.load('librerias_juego/espada.png')
need_power = pygame.image.load('librerias_juego/need_power.jpg')
corazon = pygame.image.load('librerias_juego/corazon.png')
moneda = pygame.image.load('librerias_juego/coin_zelda.png')
llave_skin = pygame.image.load('librerias_juego/llave.png')
final = pygame.image.load('librerias_juego/final.jpg')
logo = pygame.image.load('librerias_juego/logo.png')
rescate = pygame.image.load('librerias_juego/Rescatar.jpg')
elimine = pygame.image.load('librerias_juego/Eliminar.jpg')
pared_dungeon = pygame.image.load('Texturas_mapa/pared_dungeon.png')  # NUEVO


def recortar_imagen():

    lista_dungeon = recortar_sprite('Texturas_mapa/dungeon.png', 8, 8)
    lista_dungeon[0][0] = pygame.image.load('Texturas_mapa/suelo.png')
    entradas = recortar_sprite('Texturas_mapa/entradas.png', 3, 2)
    bloqueos = recortar_sprite('Texturas_mapa/bloqueos.png', 3, 2)
    lista_cueva = recortar_sprite('Texturas_mapa/dungeon_rocks.png', 13, 2)

    archivo = configparser.ConfigParser()
    archivo.read('info_mapa.txt')
    nombre_imagen = archivo.get('info', 'imagen')
    ancho_imagen = int(archivo.get('info', 'cantidad_ancho'))
    alto_imagen = int(archivo.get('info', 'cantidad_alto'))

    terreno = pygame.image.load(nombre_imagen)
    info = terreno.get_rect()
    ancho_pixeles = info[2]
    alto_pixeles = info[3]

    ancho_patron = ancho_pixeles/ancho_imagen
    alto_patron = alto_pixeles/alto_imagen

    #parametros  subsurface: posicion x, posicion y, ancho corte (ancho patron), alto corte(alto patron)

    for fila in range(alto_imagen):
        lista_terreno.append([])
        for col in range(ancho_imagen):
           cuadro = terreno.subsurface(ancho_patron*col, alto_patron*fila, ancho_patron, alto_patron)
           lista_terreno[fila].append(cuadro)

    lista_terreno[13][31] = lista_cueva[0][0]
    lista_terreno[13][30] = pygame.image.load('Texturas_mapa/Lava.png')

    #NUEVO
    aux = len(lista_terreno)
    for fila in range(8):
        lista_terreno.append([])
        for col in range(8):
           cuadro = lista_dungeon[fila][col]
           lista_terreno[aux].append(cuadro)
        aux += 1
    #sprites de las entradas de la dungeon
    lista_terreno[0][0] = entradas[0][0]
    lista_terreno[0][1] = entradas[0][1]
    lista_terreno[0][2] = entradas[0][2]
    lista_terreno[0][3] = entradas[1][0]

    #sprite de los bloqueos de la dungeon
    lista_terreno[0][4] = bloqueos[0][0]
    lista_terreno[0][5] = bloqueos[0][1]
    lista_terreno[0][6] = bloqueos[0][2]
    lista_terreno[0][7] = bloqueos[1][0]
 


def recortar_sprite(nombre_imagen, ancho_imagen2, alto_imagen2):

    lista_sprites = []
    terreno = pygame.image.load(nombre_imagen)
    info = terreno.get_rect()
    ancho_pixeles = info[2]
    alto_pixeles = info[3]

    ancho_patron = ancho_pixeles/ancho_imagen2
    alto_patron = alto_pixeles/alto_imagen2

    #parametros  subsurface: posicion x, posicion y, ancho corte (ancho patron), alto corte(alto patron)

    for fila in range(alto_imagen2):
        lista_sprites.append([])
        for col in range(ancho_imagen2):
           cuadro = terreno.subsurface(
               ancho_patron*col, alto_patron*fila, ancho_patron, alto_patron)
           lista_sprites[fila].append(cuadro)

    return lista_sprites


def leer_mapa(pantalla,nombre_mapa,nivel):

    archivo = configparser.ConfigParser()
    #NUEVO
    if nivel == 1:
        archivo.read('info_mapa.txt')
    elif nivel == 2:
        archivo.read('info_dungeon.txt')
        pantalla.blit(pared_dungeon, [0, 0])


    #se carga informacion del archivo info_mapa
    mapa = archivo.get('info', nombre_mapa)
    ls_filas = mapa.split('\n')  # divide el mapa por filas

    x = 0
    y = 0
    i = 0
    for j in range(len(ls_filas)):
        i = 0
        for e in ls_filas[j]:
            columna = int(archivo.get(e, 'col'))
            fila = int(archivo.get(e, 'fila'))
            x = i*32
            y = j*32
            if e != 'N' and e != 'K' and e != 'S' and e != 'H' and e != 'B' and e != 'Q':
               pantalla.blit(lista_terreno[fila][columna], [x, y])
            elif e == 'S' or e == 'H' or e == 'B' or e == 'Q':
                pantalla.blit(lista_terreno[fila][columna], [x, y-16])

            i += 1


def obtener_bloques(nombre_mapa):
    archivo = configparser.ConfigParser()
    archivo.read('info_mapa.txt')
    coordenadas_bloques = []
    #se carga informacion del archivo info_mapa
    mapa = archivo.get('info', nombre_mapa)
    ls_filas = mapa.split('\n')  # divide el mapa por filas

    x = 0
    y = 0
    i = 0
    for j in range(len(ls_filas)):
        i = 0
        for e in ls_filas[j]:
            if e != '.' and e != '2' and e != ',' and e != 'n' and  e != 'g':
                x = i*32
                y = j*32
                coordenadas_bloques.append([x,y])
            elif e == '2':
                coordenadas_cueva.append([i*32,j*32])
            elif e == 'g':
                coordenadas_generador.append([i*32, j*32])
                
            i += 1
  
    return coordenadas_bloques


#NUEVO
def obtener_bloques_dungeon(nombre_mapa):
    archivo = configparser.ConfigParser()
    archivo.read('info_dungeon.txt')
    coordenadas_bloques = []
    #se carga informacion del archivo info_mapa
    mapa = archivo.get('info', nombre_mapa)
    ls_filas = mapa.split('\n')  # divide el mapa por filas

    x = 0
    y = 0
    i = 0
    for j in range(len(ls_filas)):
        i = 0
        for e in ls_filas[j]:
            if e != '.' and e != '1' and e != 'K' and e != '7' and e != 'H' and e != '6' and e != 'S' and e != 'P' and e!= 'G' and e != 'Y' and e != 'F':
                x = i*32
                y = j*32
                coordenadas_bloques.append([x, y])
            elif e == 'P':
                coordenadas_hueco.append([i*32, j*32])
            elif e == 'G':
                coordenadas_generador.append([i*32, j*32])
            elif e == 'Y':
                coordenadas_boss.append([i*32, j*32])
            elif e== 'F':
                coordenadas_puas.append([i*32, j*32])


            i += 1

    return coordenadas_bloques


def imprimir_avisos(pantalla,mapa_actual_,L,win_game):

            if mapa_actual_ == 12:
              pantalla.blit(solo_aviso, [160, 64])
              pantalla.blit(anciano_skin, [239, 96])
            if mapa_actual_ == 14:
               if L.score < score_need: 
                   pantalla.blit(need_coins, [180, 64]) 
                   pantalla.blit(anciano_skin, [239, 96])
               else:
                   pantalla.blit(need_power, [180, 64])
                   pantalla.blit(anciano_skin, [239, 96])
            if mapa_actual_ == 21 and win_game:
                pantalla.blit(final,[180, 64])
                pantalla.blit(zelda_skin, [239, 96])
                win_game = True          


def Recorte_Link():
    
    #Cada sprite que no sea de objeto tiene su versión invulnerable.
    #Se cicla entre ambas versiones cuando Link es invulnerable.
    Sprite_Link = [[[0,0], [0,0], [0,0], [0,0]], [[0,0], [0,0], [0,0], [0,0]], [[0,0], [0,0], [0,0], [0,0]], [[0,0], [0,0], [0,0], [0,0]], [[0], [0], [0]]]

    # Derecha - Dir 3
    Sprite_Link[0][0][0] = pygame.image.load("librerias_juego/link_right1.png")
    Sprite_Link[0][0][1] = pygame.image.load("librerias_juego/link_right1_I.png")
    Sprite_Link[1][0][0] = pygame.image.load("librerias_juego/link_right2.png")
    Sprite_Link[1][0][1] = pygame.image.load("librerias_juego/link_right2_I.png")
    # Izquierda - Dir 2
    Sprite_Link[0][1][0] = pygame.image.load("librerias_juego/link_left1.png")
    Sprite_Link[0][1][1] = pygame.image.load("librerias_juego/link_left1_I.png")
    Sprite_Link[1][1][0] = pygame.image.load("librerias_juego/link_left2.png")
    Sprite_Link[1][1][1] = pygame.image.load("librerias_juego/link_left2_I.png")
    # Arriba - Dir 1
    Sprite_Link[0][2][0] = pygame.image.load("librerias_juego/link_up1.png")
    Sprite_Link[0][2][1] = pygame.image.load("librerias_juego/link_up1_I.png")
    Sprite_Link[1][2][0] = pygame.image.load("librerias_juego/link_up2.png")
    Sprite_Link[1][2][1] = pygame.image.load("librerias_juego/link_up2_I.png")
    # Abajo - Dir 0
    Sprite_Link[0][3][0] = pygame.image.load("librerias_juego/link_down1.png")
    Sprite_Link[0][3][1] = pygame.image.load("librerias_juego/link_down1_I.png")
    Sprite_Link[1][3][0] = pygame.image.load("librerias_juego/link_down2.png")
    Sprite_Link[1][3][1] = pygame.image.load("librerias_juego/link_down2_I.png")
    # Ataques - Estado 1
    Sprite_Link[2][0][0] = pygame.image.load("librerias_juego/attack_right.png")
    Sprite_Link[2][0][1] = pygame.image.load("librerias_juego/attack_right_I.png")
    Sprite_Link[2][1][0] = pygame.image.load("librerias_juego/attack_left.png")
    Sprite_Link[2][1][1] = pygame.image.load("librerias_juego/attack_left_I.png")
    Sprite_Link[2][2][0] = pygame.image.load("librerias_juego/attack_up.png")
    Sprite_Link[2][2][1] = pygame.image.load("librerias_juego/attack_up_I.png")
    Sprite_Link[2][3][0] = pygame.image.load("librerias_juego/attack_down.png")
    Sprite_Link[2][3][1] = pygame.image.load("librerias_juego/attack_down_I.png")
    # Vara - Estado 6
    Sprite_Link[3][0][0] = pygame.image.load("librerias_juego/wand_right.png")
    Sprite_Link[3][0][1] = pygame.image.load("librerias_juego/wand_right_I.png")
    Sprite_Link[3][1][0] = pygame.image.load("librerias_juego/wand_left.png")
    Sprite_Link[3][1][1] = pygame.image.load("librerias_juego/wand_left_I.png")
    Sprite_Link[3][2][0] = pygame.image.load("librerias_juego/wand_up.png")
    Sprite_Link[3][2][1] = pygame.image.load("librerias_juego/wand_up_I.png")
    Sprite_Link[3][3][0] = pygame.image.load("librerias_juego/wand_down.png")
    Sprite_Link[3][3][1] = pygame.image.load("librerias_juego/wand_down_I.png")
    # Miscelaneos
    Sprite_Link[4][0][0] = pygame.image.load("librerias_juego/item_espada.png")
    Sprite_Link[4][1][0] = pygame.image.load("librerias_juego/item_wand.png")
    Sprite_Link[4][2][0] = pygame.image.load("librerias_juego/item_key.png")

    return Sprite_Link




def Recorte_Items():

    Sprite_items = [0, 0, 0, 0, 0, 0, 0]

    # Espada
    Sprite_items[0] = pygame.image.load("librerias_juego/sword.png")
    # Vara
    Sprite_items[1] = pygame.image.load("librerias_juego/wand.png")
    # Corazón
    Sprite_items[2] = pygame.image.load("librerias_juego/heart.png")
    # Llama
    Sprite_items[3] = pygame.image.load("librerias_juego/fire.png")
    # Arbusto
    Sprite_items[4] = pygame.image.load("librerias_juego/Arbusto.png")
    Sprite_items[5] = pygame.image.load("librerias_juego/Arbusto_llama1.png")
    Sprite_items[6] = pygame.image.load("librerias_juego/Arbusto_llama2.png")
    

    return Sprite_items

def Listar_canciones():
    
    Lista_canciones = []
    
    Lista_canciones.append("music/01 Overworld.ogg")
    Lista_canciones.append("music/02 Labyrinth.ogg")
    
    return Lista_canciones




def Recorte_Enem1():

    Sprite_enem1 = [[0,0,0,0],[0,0,0,0],[0]]
    
    # Derecha - Dir 0
    Sprite_enem1[0][0] = pygame.image.load("librerias_juego/Enem1_right1.png")
    Sprite_enem1[1][0] = pygame.image.load("librerias_juego/Enem1_right2.png")
    # Izquierda - Dir 1
    Sprite_enem1[0][1] = pygame.image.load("librerias_juego/Enem1_left1.png")
    Sprite_enem1[1][1] = pygame.image.load("librerias_juego/Enem1_left2.png")
    # Arriba - Dir 2
    Sprite_enem1[0][2] = pygame.image.load("librerias_juego/Enem1_up1.png")
    Sprite_enem1[1][2] = pygame.image.load("librerias_juego/Enem1_up2.png")
    # Abajo - Dir 3
    Sprite_enem1[0][3] = pygame.image.load("librerias_juego/Enem1_down1.png")
    Sprite_enem1[1][3] = pygame.image.load("librerias_juego/Enem1_down2.png")
    # Muerto
    Sprite_enem1[2] = pygame.image.load("librerias_juego/enemigo_muerto1.png")
    
    return Sprite_enem1

def Recorte_Enem2():

    Sprite_enem2 = [[0,0,0,0],[0,0,0,0],[0]]
    
    # Derecha - Dir 0
    Sprite_enem2[0][0] = pygame.image.load("librerias_juego/Enem2_right1.png")
    Sprite_enem2[1][0] = pygame.image.load("librerias_juego/Enem2_right2.png")
    # Izquierda - Dir 1
    Sprite_enem2[0][1] = pygame.image.load("librerias_juego/Enem2_left1.png")
    Sprite_enem2[1][1] = pygame.image.load("librerias_juego/Enem2_left2.png")
    # Arriba - Dir 2
    Sprite_enem2[0][2] = pygame.image.load("librerias_juego/Enem2_up1.png")
    Sprite_enem2[1][2] = pygame.image.load("librerias_juego/Enem2_up2.png")
    # Abajo - Dir 3
    Sprite_enem2[0][3] = pygame.image.load("librerias_juego/Enem2_down1.png")
    Sprite_enem2[1][3] = pygame.image.load("librerias_juego/Enem2_down2.png")
    # Muerto
    Sprite_enem2[2] = pygame.image.load("librerias_juego/enemigo_muerto2.png")
    
    return Sprite_enem2
    
def Recorte_Enem3():

    Sprite_enem3 = [[0,0,0,0],[0,0,0,0],[0]]
    
    # Derecha - Dir 0
    Sprite_enem3[0][0] = pygame.image.load("librerias_juego/darknut_right1.png")
    Sprite_enem3[1][0] = pygame.image.load("librerias_juego/darknut_right2.png")
    # Izquierda - Dir 1
    Sprite_enem3[0][1] = pygame.image.load("librerias_juego/darknut_left1.png")
    Sprite_enem3[1][1] = pygame.image.load("librerias_juego/darknut_left2.png")
    # Arriba - Dir 2
    Sprite_enem3[0][2] = pygame.image.load("librerias_juego/darknut_up1.png")
    Sprite_enem3[1][2] = pygame.image.load("librerias_juego/darknut_up2.png")
    # Abajo - Dir 3
    Sprite_enem3[0][3] = pygame.image.load("librerias_juego/darknut_down1.png")
    Sprite_enem3[1][3] = pygame.image.load("librerias_juego/darknut_down2.png")
    # Muerto
    Sprite_enem3[2] = pygame.image.load("librerias_juego/enemigo_muerto1.png")
    
    return Sprite_enem3

def Recorte_Enem4():

    Sprite_enem4 = [0,0]
    
    # Derecha - Dir 0
    Sprite_enem4[0] = pygame.image.load("librerias_juego/Keese1.png")
    Sprite_enem4[1] = pygame.image.load("librerias_juego/Keese2.png")

    return Sprite_enem4

def Recorte_Jefe1():

    Sprite_Jefe1 = [0,0,0,0,0,0,0,0]
    
    # Derecha - Dir 0
    Sprite_Jefe1[0] = pygame.image.load("librerias_juego/Vaati_0.1.png")
    Sprite_Jefe1[1] = pygame.image.load("librerias_juego/Vaati_0.2.png")
    # Izquierda - Dir 1
    Sprite_Jefe1[2] = pygame.image.load("librerias_juego/Vaati_1.1.png")
    Sprite_Jefe1[3] = pygame.image.load("librerias_juego/Vaati_1.2.png")
    # Arriba - Dir 2
    Sprite_Jefe1[4] = pygame.image.load("librerias_juego/Vaati_left1.png")
    Sprite_Jefe1[5] = pygame.image.load("librerias_juego/Vaati_left2.png")
    # Abajo - Dir 3
    Sprite_Jefe1[6] = pygame.image.load("librerias_juego/Vaati_right1.png")
    Sprite_Jefe1[7] = pygame.image.load("librerias_juego/Vaati_right2.png")
    
    return Sprite_Jefe1

def Recorte_BolaHielo():

    Sprite_Sball = [0,0,0,0]
    
    Sprite_Sball[0] = pygame.image.load("librerias_juego/Special_ball1.png")
    Sprite_Sball[1] = pygame.image.load("librerias_juego/Special_ball2.png")
    Sprite_Sball[2] = pygame.image.load("librerias_juego/Special_ball3.png")
    Sprite_Sball[3] = pygame.image.load("librerias_juego/Special_ball4.png")

    return Sprite_Sball

def mostrar_informacion(pantalla, espada, vara,salud,score,key,win_game,nivel):
    
    fuente = pygame.font.Font(None, 25)

    '''pygame.draw.line(pantalla, AZUL, [350, 364], [380, 364], 3)
    pygame.draw.line(pantalla, AZUL, [350, 409], [380, 409], 3)
    pygame.draw.line(pantalla, AZUL, [350, 364], [350, 409], 3)
    pygame.draw.line(pantalla, AZUL, [380, 364], [380, 409], 3)
'''
    pygame.draw.line(pantalla, AZUL, [390, 364], [420, 364], 3)
    pygame.draw.line(pantalla, AZUL, [390, 409], [420, 409], 3)
    pygame.draw.line(pantalla, AZUL, [390, 364], [390, 409], 3)
    pygame.draw.line(pantalla, AZUL, [420, 364], [420, 409], 3) 

    pygame.draw.line(pantalla, AZUL, [430, 364], [460, 364], 3)
    pygame.draw.line(pantalla, AZUL, [430, 409], [460, 409], 3)
    pygame.draw.line(pantalla, AZUL, [430, 364], [430, 409], 3)
    pygame.draw.line(pantalla, AZUL, [460, 364], [460, 409], 3) 

    pygame.draw.line(pantalla, AZUL, [470, 364], [500, 364], 3)
    pygame.draw.line(pantalla, AZUL, [470, 409], [500, 409], 3)
    pygame.draw.line(pantalla, AZUL, [470, 364], [470, 409], 3)
    pygame.draw.line(pantalla, AZUL, [500, 364], [500, 409], 3)


    
    
    #info_salud='Salud: ' + str(j.salud)
    #texto=fuente.render(info_salud,True, BLANCO)
    texto= fuente.render('-LIFE-',True, ROJO)
    pantalla.blit(texto, [15,375])
    i = 5
    for n in range(salud):
      pantalla.blit(corazon, [i,395])  
      i+=15

    puntos = 'x' + str(score)
    s = fuente.render(puntos, True, BLANCO)
    puntaje = fuente.render('-SCORE-',True,VERDE)
    pantalla.blit(puntaje, [268, 375])
    pantalla.blit(moneda, [278, 395])
    pantalla.blit(s, [295, 395])


    if espada: 
        pantalla.blit(espada_skin, [437, 366])
    if vara:
       pantalla.blit(varita_skin, [396, 366])
    if key: 
        pantalla.blit(llave_skin, [477, 366])

    level = '-NIVEL '+ str(nivel) + '-'
    n = fuente.render(level, True, BLANCO)
    pantalla.blit(n, [158, 385])
 

