import pygame
from librerias_juego.libreria import *
from librerias_juego.clases import *
import random
import time

ANCHO = 512
ALTO = 352
ALTO_VENTANA = ALTO+64 #este alto se le suma 64 porque es el espacio donde va la informacion del jugador 

def Inicio(music):  
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO, ALTO_VENTANA])
    pygame.display.set_caption("The Legend of Zelda")
    link = Recorte_Link()
    Bola_hielo = Recorte_BolaHielo()
    itemSprite = Recorte_Items()
    recortar_imagen()
    arbustos_f = True
    pausa = False
    archivo = configparser.ConfigParser()
    archivo.read('info_mapa.txt')
    music = Music_manager(music, Listar_canciones())
    tipo_enemigo = 0
    game_over = False
    fuente = pygame.font.Font(None, 25)
    rescatar = True
    eliminar = True
    win_game = False
    

    #sfx
    secret = pygame.mixer.Sound('sfx/LOZ_Secret.wav')
    #---

    #en esta parte se crean todo los grupos de sprites 
    jugadores = pygame.sprite.Group()
    bloques = pygame.sprite.Group()
    arbustos = pygame.sprite.Group()                                
    items = pygame.sprite.Group()
    llamas = pygame.sprite.Group()
    cuevas = pygame.sprite.Group()
    huecos = pygame.sprite.Group()
    generadores_1 = pygame.sprite.Group()
    generadores_2 = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    puas = pygame.sprite.Group()                             
     
    L = Link(link, [ANCHO/2, ALTO/2])
    L.nivel = 1
    L.mapa_actual = 1
    #L.key = True
    jugadores.add(L)
    
   
    mapa_actual_ = L.mapa_actual
    nombre_mapa = archivo.get('infodemapas', str(mapa_actual_))

    # Adicion
    f_input = [False,False,False,False]
    # f_input = [der,izq,arr,abj]
    f_k = False

    reloj = pygame.time.Clock()

    fin = False
    while not fin:
        # Gestion de Eventos
        f_k = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
                music.stop()
            #Cada tecla direccional tiene una bandera que se activa cuando 
            #se pulsa y se desactiva cuando se deja de pulsar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    f_input[0] = True
                if event.key == pygame.K_LEFT:
                    f_input[1] = True
                if event.key == pygame.K_UP:
                    f_input[2] = True
                    rescatar = False
                    if L.nivel == 2:
                       eliminar = False
                if event.key == pygame.K_DOWN:
                    f_input[3] = True
                #Se ataca con espacio
                if event.key == pygame.K_SPACE:
                    if L.estado == 0 and not pausa:
                        L.estado = 1
                        L.velx = 0
                        L.vely = 0
                #Se usa la vara con C
                if event.key == pygame.K_c and not pausa:
                    if L.estado == 0:
                        L.estado = 6
                        L.velx = 0
                        L.vely = 0
                if event.key == pygame.K_x and (pausa or win_game or game_over):
                    fin = True
                    music.stop()
                #Pausa
                if event.key == pygame.K_RETURN and not game_over:
                    pausa = not pausa
                    if pausa:
                        pygame.mixer.pause()
                    else:
                        pygame.mixer.unpause()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    f_input[0] = False
                if event.key == pygame.K_LEFT:
                    f_input[1] = False
                if event.key == pygame.K_UP:
                    f_input[2] = False
                if event.key == pygame.K_DOWN:
                    f_input[3] = False
            
        #Dependiendo de las banderas, se decide la direccion del movimiento
        #En cualquier caso, se activa una bandera especial
        if not pausa:
            if f_input[0]:
                if L.estado == 0:
                    L.dir = 0
                    L.velx = 5
                    L.vely = 0
                    f_k = True
            if f_input[1]:
                if L.estado == 0:
                    L.dir = 1
                    L.velx = -5
                    L.vely = 0
                    f_k = True
            if f_input[2]:
                if L.estado == 0:
                    L.dir = 2
                    L.velx = 0
                    L.vely = -5
                    f_k = True
            if f_input[3]:
                if L.estado == 0:
                    L.dir = 3
                    L.velx = 0
                    L.vely = 5
                    f_k = True
        #Para que no se detenga todo el movimiento al soltar una tecla, se
        #usa la bandera f_k que se activa con cualquier decision de movimiento.
        #Las velocidades seran 0 SOLO SI SE LEVANTAN TODAS LAS TECLAS DIRECCIONALES
        if not f_k:
            L.velx = 0
            L.vely = 0
                
        
        #Aqui se toman los nuevos valores para imprimir el nuevo mapa 
        
        if L.cambio:       
           #Se vacian los grupos de objetos, llamas y enemigos al cambiar mapa
           items.empty()
           llamas.empty()
           cuevas.empty()
           arbustos.empty()
           generadores_1.empty()
           generadores_2.empty()
           enemigos.empty()
           puas.empty()            
           proyectiles_e.empty()

           if len(coordenadas_cueva) != 0:
              coordenadas_cueva.pop(0)
           if len(coordenadas_generador) != 0:
               coordenadas_generador.pop(0)
           if len(coordenadas_boss) != 0:
               coordenadas_boss.pop(0)
           if coordenadas_hueco:
               coordenadas_hueco.clear()
               L.hueco.empty()
           if coordenadas_puas:
                coordenadas_puas.clear()
                
            
            

           mapa_actual_ = L.mapa_actual
           nombre_mapa = archivo.get('infodemapas', str(mapa_actual_))
           #NUEVO
           if L.nivel == 1:
               grupo_bloques = obtener_bloques(nombre_mapa)
           elif L.nivel == 2:
               grupo_bloques = obtener_bloques_dungeon(nombre_mapa)

           
           bloques.empty()
           L.bloques.empty()

           for n in range(len(grupo_bloques)):
                b = Bloque(grupo_bloques[n])
                bloques.add(b)


           if len(coordenadas_cueva) !=0:
                cueva = Cueva(coordenadas_cueva[0])
                cuevas.add(cueva)
                L.cuevas = cuevas

           if len(coordenadas_hueco) != 0:
               for c in range(len(coordenadas_hueco)):
                 hueco = Hueco(coordenadas_hueco[c])
                 huecos.add(hueco)
               L.hueco = huecos
            
           if len(coordenadas_puas) != 0:
                for c in range(len(coordenadas_puas)):
                  pua = Puas(coordenadas_puas[c])
                  puas.add(pua)
              
           
           #TODO: Leer la posicion de las puas por mapa y añadirlas al grupo puas 
           
           if len(coordenadas_boss) !=0:
                boss = Jefe1(Recorte_Jefe1(),Recorte_BolaHielo(),coordenadas_boss[0],L.bloques,L)
                enemigos.add(boss)                
                
           
           #dependiendo de si el mapa tiene un generador y sus coordenadas se han guardado
           #entonces se agrega el generador dependiendo del tipo que tenga el mapa
           if len(coordenadas_generador) != 0:
                if archivo.get('infogeneradores', nombre_mapa) == 'destructible':
                    g = Generador1(coordenadas_generador[0], Arbol)
                    generadores_1.add(g)
                elif archivo.get('infogeneradores', nombre_mapa) == 'indestructible':
                    g2 = Generador2(coordenadas_generador[0])
                    generadores_2.add(g2)
                    tipo_enemigo = 2
                elif archivo.get('infogeneradores', nombre_mapa) == 'invisible':
                    g2 = Generador2(coordenadas_generador[0])
                    generadores_2.add(g2)
                    tipo_enemigo = 3
                else:
                    g2 = Generador2(coordenadas_generador[0])
                    generadores_2.add(g2)
                    tipo_enemigo = 4



           music.set_music(mapa_actual_, L.nivel)

           #Se crean los objetos para testear
           if mapa_actual_ == 12 and L.espada == None:
                items.add(EspadaItem([256,162], itemSprite[0]))
           elif mapa_actual_ == 14 and L.vara == None:
                if L.score < score_need:
                    items.add(VaraItem([264,96], itemSprite[1], itemSprite[3])) 
                else:
                    items.add(VaraItem([256,162], itemSprite[1], itemSprite[3]))
           elif mapa_actual_ == 11 and arbustos_f:
                arbusto = Arbusto(224,0,[itemSprite[4],itemSprite[5],itemSprite[6]])
                arbustos.add(arbusto)
                bloques.add(arbusto.bloque)
           elif mapa_actual_ == 22 and not L.key:
                key = Llave([256,160])
                items.add(key)
           L.bloques = bloques
           L.cambio = False # <==esta variable nos sirve para saber si el personaje 
                        #paso a otro mapa y ahorrarnos procesos 
        

        #aqui es donde se generan los enemigos,todo de pende de si se agrego 
        # generadores al grupo de generadores(generadores_1 es vulnerable,destructible)
        #genrador_2 no lo es y queda invisible en el ambiente
        if len(generadores_1) != 0 and not pausa:
            for g in generadores_1:
                if g.temp <= 0:
                    #Limite de enemigos por mapa
                    if len(enemigos) < 6:
                        r = Enemigo1(Recorte_Enem1(), [g.rect.x, g.rect.y+32], bloques)
                        moneda=random.randrange(100)
                        if moneda < 25:
                            r.velx = 4
                            r.dir = 0
                        elif moneda > 25 and moneda < 50:
                            r.velx = -4
                            r.dir = 1
                        elif moneda > 50 and moneda < 75:
                            r.vely = -4
                            r.dir = 2
                        else:
                            r.vely = 4
                            r.dir=3

                        enemigos.add(r)
                    g.temp = 60

            generadores_1.update()

        elif len(generadores_2) != 0 and not pausa:
            for g in generadores_2:
              if g.temp <= 0:
                    #Limite de enemigos por mapa
                    if tipo_enemigo!= 3 and len(enemigos) < 6:
                        if tipo_enemigo == 2:
                          r = Enemigo2(Recorte_Enem2(), [g.rect.x,g.rect.y], bloques)
                        else:
                          r = Enemigo4(Recorte_Enem4(),[g.rect.x,g.rect.y], bloques)
                        moneda = random.randrange(100)
                        if moneda < 25:
                            r.velx = 4
                            r.dir = 0
                        elif moneda > 25 and moneda < 50:
                            r.velx = -4
                            r.dir = 1
                        elif moneda > 50 and moneda < 75:
                            r.vely = -4
                            r.dir = 2
                        else:
                            r.vely = 4
                            r.dir = 3
                        enemigos.add(r)
                    elif len(enemigos)<3:
                        r = Enemigo3(Recorte_Enem3(), [g.rect.x,g.rect.y], bloques.sprites()+huecos.sprites()+puas.sprites())
                        moneda = random.randrange(100)
                        if moneda < 25:
                            r.velx = 4
                            r.dir = 0
                        elif moneda > 25 and moneda < 50:
                            r.velx = -4
                            r.dir = 1
                        elif moneda > 50 and moneda < 75:
                            r.vely = -4
                            r.dir = 2
                        else:
                            r.vely = 4
                            r.dir = 3
                        enemigos.add(r)

                    if tipo_enemigo == 3:
                        g.temp = 120
                    else:   
                        g.temp = 60
            
            generadores_2.update()

        if not pausa:
            #Chequea si Link disparó fuego
            if L.llama != None:
                llamas.add(L.llama)
            
            #Chequea si Link recoge un objeto
            ls_col = pygame.sprite.spritecollide(L,items, False)
            for i in ls_col:
                i.efecto(L)
            
            #Chequea si los ataques de Link golpean
            if L.hitbox != None:
                for b in enemigos:
                    if L.hitbox.colliderect(b):
                        if b.morir(L):
                            rand = random.randrange(0,15)
                            if rand == 0:
                                items.add(Corazon(b.rect.center))
                for g in generadores_1:
                    if L.hitbox.colliderect(g):
                        g.herir(0)
            for llama in llamas:
                ll_col = pygame.sprite.spritecollide(llama,enemigos,False)
                for b in ll_col:
                    if b.morir_llama(L):
                        rand = random.randrange(0,25)
                        if rand == 0:
                            items.add(Corazon(b.rect.center))
                ll_col = pygame.sprite.spritecollide(llama,generadores_1,False)
                for g in ll_col:
                    g.herir(1)
                    llama.kill()
                ll_col = pygame.sprite.spritecollide(llama,arbustos,False)
                for a in ll_col:
                    a.estado = 1
                    llama.kill()
            #-----
            
            #Chequea si Link es golpeado
            if L.estado != 8: #Solo es golpeado si no está cayendo                                                      
                for b in enemigos:
                    if L.hurtbox.colliderect(b):
                        L.golpe(b)
                for p in puas:
                    if L.hurtbox.colliderect(p):
                        L.golpe(p)
                for g in generadores_1:
                    if L.hurtbox.colliderect(g):
                        L.golpe(g)
                for b in proyectiles_e:
                    if L.hurtbox.colliderect(b):
                        L.golpe(b)
            #-----
    
        #Chequea si Link ha muerto
        if L.salud < 1 and not game_over:
            music.stop()
            enemigos.empty()
            proyectiles_e.empty()
            llamas.empty()
            items.empty()
            generadores_1.empty()
            generadores_2.empty()
            L.morir()
            game_over = True
            background = pygame.image.load("librerias_juego/Game_Over.png")
        
        if win_game: 
            proyectiles_e.empty()
            jugadores.empty()
            music.stop()
        #Si se terminó el juego, ejecuta la secuencia.
        if game_over:
            enemigos.empty()
            proyectiles_e.empty()
            if pygame.mixer.get_busy():
                pantalla.fill(NEGRO)
                jugadores.draw(pantalla)
            else:
                pantalla.blit(background, [0,0])
                volver = fuente.render('Oprima X para volver al inicio', True, BLANCO)
                pantalla.blit(volver, [120, 330])
                

        else:
            pantalla.fill(NEGRO)
            
            #Funcion que se encarga de pintar el mapa en la pantalla
            leer_mapa(pantalla, nombre_mapa,L.nivel)
            #imprime los avistos de la historia de zelda
            imprimir_avisos(pantalla, mapa_actual_, L, win_game)
            #imprime la informazion de link 
            mostrar_informacion(pantalla, L.espada, L.vara,L.salud, L.score, L.key, win_game,L.nivel)
            if rescatar:
                pantalla.blit(rescate, [100,100])
            if eliminar and L.nivel == 2:
                pantalla.blit(elimine,[100,100])
            if mapa_actual_ == 21:
                for e in enemigos:
                    if e.muerto == True:
                      win_game = True
            if not pausa:
                jugadores.update()
                items.update()
                if arbustos_f and arbustos:
                    arbustos.update()
                    if len(arbustos) == 0:
                        secret.play()
                        arbustos_f = False
                llamas.update()
                enemigos.update()
                proyectiles_e.update()
            #La musica sigue sonando aún en pausa                                      
            music.update(L.estado, pausa)
            #draw                       
            arbustos.draw(pantalla)
            items.draw(pantalla)
            puas.draw(pantalla)  
            enemigos.draw(pantalla)                 
            jugadores.draw(pantalla)
            generadores_1.draw(pantalla)
            proyectiles_e.draw(pantalla)
            if pausa:
                pausa_screen = pygame.Surface([ANCHO,ALTO])
                pausa_screen.set_alpha(120)
                pantalla.blit(pausa_screen, [0,0])
            llamas.draw(pantalla)
            #bloques.draw(pantalla)
        pygame.display.flip()
        reloj.tick(20)


def menu():
    pygame.mixer.init(frequency=32000)
    music = pygame.mixer_music
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO, ALTO_VENTANA])
    pygame.display.set_caption("The Legend of Zelda")
    fuente = pygame.font.Font(None, 25)
    texto = fuente.render('Oprima Enter para Continuar', True, NEGRO)
    texto2 = fuente.render('Oprima la E para Salir', True, NEGRO)

    reloj = pygame.time.Clock()
    fin = False
    while not fin:
        #gestion de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    #fin = True
                    Inicio(music)
                if event.key == pygame.K_e:
                    fin = True
                    
                '''if event.key == pygame.K_UP:
                    fin = True '''  

        
        pantalla.fill(GRIS)
        pantalla.blit(logo, [70, 100])
        pantalla.blit(texto, [125, 350])
        pantalla.blit(texto2, [126, 370])
        pygame.display.flip()
        reloj.tick(20)

if __name__ == '__main__':
    menu()
         
quit()
