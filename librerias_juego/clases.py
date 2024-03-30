import pygame
import random

#Recomiendo fuertemente copiar toda la clase de enemigos, proyectiles
#y generadores

ANCHO = 512
ALTO = 320 #este alto es del jugador no de la ventana de juego
BLANCO = [255, 255, 255]
NEGRO = [0, 0, 0]

# [izquierda, derecho, arriba, abajo,cueva]
ubicaciones = {0: [-1, 1, 7, -1], 1: [0, 2, 4, -1, 12], 2: [1, 3, 5, -1], 3: [2, -1, 6, -1,14],
               7: [-1, 4, 8, 0, 13], 4: [7, 5, 9, 1], 5: [4, 6, 10, 2], 6: [5, -1, 11, 3],
               8: [-1, 9, -1, 7], 9: [8, 10, -1, 4], 10: [9, 11, -1, 5], 11: [10, -1, 22, 6],
               12: [-1,-1, -1, 1, -1], 13: [-1, -1, -1, 7, -1], 14: [-1, -1, -1, 3, -1],
               17: [-1,16,19,-1], 16:[17,-1,-1,-1], 19: [-1,-1,20,17], 20:[-1,18,-1,19], 
               21: [-1,-1,-1,18], 18:[20,-1,21,-1], 22:[-1, -1, -1, 11]}


#Se fusionó bolas de fuego y flechas para simplicidad
proyectiles_e = pygame.sprite.Group()
class Potenciadores(pygame.sprite.Sprite):

    def __init__(self, pos, sprite):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]

    def efecto(self, Link):
        pass


class Corazon(Potenciadores):

    def __init__(self, pos):
        super().__init__(pos, pygame.image.load('librerias_juego/heart.png'))
        self.sfx = pygame.mixer.Sound("sfx/LOZ_Get_Heart.wav")

    def efecto(self, Link):
        if Link.estado == 0:                    
            self.sfx.play()
            Link.salud += 1
            if Link.salud > 5:
                Link.salud = 5
            self.kill()
            del self


class Llave(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('librerias_juego/key.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.sfx = pygame.mixer.Sound("sfx/LOZ_Fanfare.wav")
    
    def efecto(self, Link):
        if Link.estado == 0:                    
            self.sfx.play()
            Link.estado = 4
            Link.con = 2
            Link.key = True
            self.kill()
            del self


class EspadaItem (Potenciadores):
    def __init__(self, pos, sprite):
        super().__init__(pos, sprite)
        self.sfx = pygame.mixer.Sound('sfx\LOZ_Fanfare.wav')

    def efecto(self, Link):
        if Link.estado == 0:            
            Link.espada = Espada()
            self.sfx.play()
            Link.estado = 4
            Link.con = 0
            self.kill()
            del self


class Llama (pygame.sprite.Sprite):

    def __init__(self, sprite):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.centerx = 0
        self.rect.centery = 0
        self.con = 0
        self.vx = 0
        self.vy = 0

    def cast(self, dire, pos):
        self.con = 0
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        if dire == 0:
            self.vx = 3
            self.vy = 0
        elif dire == 1:
            self.vx = -3
            self.vy = 0
        elif dire == 2:
            self.vx = 0
            self.vy = -3
        else:
            self.vx = 0
            self.vy = 3

    def update(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.con += 1
        if self.con < 30:
            self.rect.x += self.vx
            self.rect.y += self.vy
        elif self.con == 60:
            self.kill()


class Vara:
    def __init__(self, sprite_llama):
        self.llama = Llama(sprite_llama)
        self.sfx = pygame.mixer.Sound('sfx\LOZ_MagicalRod.wav')

    def is_alive(self):
        return self.llama.alive()

    def atacar(self, pos, dire):
        self.sfx.play()
        self.llama.cast(dire, pos)
        return self.llama


class VaraItem (Potenciadores):

    def __init__(self, pos, sprite, sprite_llama):
        super().__init__(pos, sprite)
        self.sfx = pygame.mixer.Sound('sfx\LOZ_Fanfare.wav')
        self.sprite_llama = sprite_llama

    def efecto(self, Link):
        if Link.estado == 0:                    
            Link.vara = Vara(self.sprite_llama)
            self.sfx.play()
            Link.estado = 4
            Link.con = 1
            self.kill()
            del self

#Clase de la espada. Se hizo clase por si se quiere modificar sus atributos durante el juego
class Espada:
    def __init__(self):
        #Aquí se ponen stats y atributos
        self.sfx = pygame.mixer.Sound('sfx\LOZ_Sword_Slash.wav')

    def atacar(self, x, y, dire):
        #Las dimensiones del hitbox dependen de la dirección
        if dire == 0:
            hitbox = pygame.Rect(x+34, y, 28, 32)
        elif dire == 1:
            hitbox = pygame.Rect(x-2, y, 28, 32)
        elif dire == 2:
            hitbox = pygame.Rect(x, y-2, 32, 28)
        else:
            hitbox = pygame.Rect(x, y+35, 32, 26)
        return hitbox


class Link(pygame.sprite.Sprite):

    def __init__(self, L, pos):
        pygame.sprite.Sprite.__init__(self)
        self.L = L
        self.dir = 0
        self.con = 0
        self.image = self.L[self.dir][self.con][0]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velx = 0
        self.vely = 0
        self.salud = 5
        self.nivel = 1
        self.bloques = pygame.sprite.Group()
        self.cuevas = []
        self.hueco = pygame.sprite.Group()
        self.encueva = 0
        self.mapa_actual = 1
        self.cambio = True
        self.freeze = False
        self.invulnerable = False
        self.spawn = []               
        #Se implementan índices para facilitar el uso de sprites de invulnerabilidad
        self.sprite_index1 = 0
        self.sprite_index2 = 0
        self.i_sprite = False
        #Contador de invulnerabilidad
        self.i_con = 0
        #Contador de congelacion
        self.f_con = 0
        #Puntaje y llave
        self.score = 0
        self.key = False
        # SFX     
        self.shield_sfx = pygame.mixer.Sound('sfx\LOZ_Shield.wav')
        self.hurt_sfx = pygame.mixer.Sound('sfx\LOZ_Link_Hurt.wav')
        self.dead_sfx = pygame.mixer.Sound('sfx/LOZ_Link_Die.wav')
        self.fall_sfx = pygame.mixer.Sound('sfx/Fall_scream.wav')                                                         

        #Usado para controlar el ataque y animaciones
        self.estado = 0
        #Cubre solo el cuerpo. Usado para que solo se chequee colisión con el cuerpo y no con la espada
        self.hurtbox = self.rect.copy()
        #La espada determina el hitbox. Puede usarse para modificarse luego
        self.espada = None
        #Cubre la espada. Usado para que solo la se chequee colisión con la espada al atacar
        self.hitbox = None
        #La vara para lanzar fuego
        self.vara = None
        #Se guarda una referencia para pasarla al main
        self.llama = None
        #---

    #Si Link fue golpeado
    def golpe(self, e):
        #Reacciona distinto si fueron proyectiles
        if not self.invulnerable and self.estado != 4 and self.estado !=5:
            if isinstance(e, BolaFuego) or isinstance(e, Flecha) or isinstance(e, BolaAzul):
                if self.estado == 0 and ((self.dir==0 and e.direction==1)or(self.dir==1 and e.direction==0)or(self.dir==2 and e.direction==3)or(self.dir==3 and e.direction==2)):
                    self.shield_sfx.play()
                else:
                    self.hurt_sfx.play()
                    self.invulnerable = True
                    self.i_con = 0
                    x = self.rect.x - e.rect.x
                    y = self.rect.y - e.rect.y
                    if abs(x) < abs(y):
                        if y < 0:
                            self.velx = 0
                            self.vely = -15
                        else:
                            self.velx = 0
                            self.vely = 15
                    else:
                        if x < 0:
                            self.velx = -15
                            self.vely = 0
                        else:
                            self.velx = 15
                            self.vely = 0
                    self.estado = 7
                    self.con = 2
                    self.sprite_index1 = 0
                    self.salud -= 1
                    self.hitbox = None
                e.kill()
            elif isinstance(e, BolaHielo):
                self.hurt_sfx.play()
                self.invulnerable = True
                self.i_con = 0
                self.freeze = True
                self.f_con = 0
                self.salud -= 1
                self.hitbox = None
                e.kill()
            else:
                self.hurt_sfx.play()
                self.invulnerable = True
                self.i_con = 0
                x = self.rect.x - e.rect.x
                y = self.rect.y - e.rect.y
                if abs(x) < abs(y):
                    if y < 0:
                        self.velx = 0
                        self.vely = -25
                    else:
                        self.velx = 0
                        self.vely = 25
                else:
                    if x < 0:
                        self.velx = -25
                        self.vy = 0
                    else:
                        self.velx = 25
                        self.vely = 0
                self.estado = 7
                self.con = 0
                self.sprite_index1 = 0
                self.salud -= 1
                self.hitbox = None

    def morir(self):
        self.dead_sfx.play()
    def update(self):
        self.llama = None
        if self.invulnerable:
            if self.i_con <= 30:
                self.i_con += 1
                self.i_sprite = not self.i_sprite
            else:
                self.invulnerable = False
                self.i_sprite = False

        #Congelado
        if self.freeze:
            if self.f_con == 0:
                filtro = pygame.Surface(self.image.get_size()).convert_alpha()
                filtro.fill([0,255,255])
                filtro.blit(self.image, (0,0), special_flags = pygame.BLEND_RGBA_MULT)
                self.image =  filtro
            if self.f_con < 30:
                self.f_con += 1
            else:
                self.freeze = False
                self.f_con = 0
        #Caminando
        elif self.estado == 0 and (self.velx != 0 or self.vely != 0):
            self.rect.x += self.velx
            self.rect.y += self.vely
            self.hurtbox.x = self.rect.x
            self.hurtbox.y = self.rect.y
            #self.image = self.L[self.con][self.dir][self.i_sprite]
            self.sprite_index1 = self.con
            self.sprite_index2 = self.dir
            if self.con < 1:
                self.con += 1
            else:
                self.con = 0
        #Atacando
        elif self.estado == 1:
            if self.espada == None:
                self.estado = 0
            else:
                self.espada.sfx.play()
                #self.image = self.L[2][self.dir][self.i_sprite]
                self.sprite_index1 = 2
                self.sprite_index2 = self.dir
                if self.dir == 0:
                    self.hurtbox.w = 34
                    self.hurtbox.h = 32
                elif self.dir == 1:
                    self.rect.x -= 26
                    self.hurtbox.w = 33
                    self.hurtbox.h = 32
                elif self.dir == 2:
                    self.rect.y -= 29
                    self.hurtbox.y = self.rect.y+29
                    self.hurtbox.w = 32
                    self.hurtbox.h = 35
                else:
                    self.hurtbox.w = 32
                    self.hurtbox.h = 35
                self.hitbox = self.espada.atacar(
                    self.rect.x, self.rect.y, self.dir)
                self.estado = 2
                self.con = 0
        #Cooldown del ataque
        elif self.estado == 2:
            if self.con < 4:
                self.con += 1
            else:
                self.con = 0
                self.estado = 0
                #self.image = self.L[self.con][self.dir][self.i_sprite]
                self.sprite_index1 = self.con
                self.sprite_index2 = self.dir
                if self.dir == 1:
                    self.rect.x += 26
                elif self.dir == 2:
                    self.rect.y += 29
                self.hurtbox.x = self.rect.x
                self.hurtbox.y = self.rect.y
                self.hurtbox.size = self.rect.size
                self.hitbox = None
        #Obtiene item importante
        elif self.estado == 4:
            self.sprite_index1 = 4
            self.sprite_index2 = self.con
            self.rect.y -= 27
            self.estado = 5
            self.con = 0
        elif self.estado == 5:
            if self.con < 31:
                self.con += 1
            else:
                self.con = 0
                self.sprite_index1 = self.con
                self.sprite_index2 = self.dir
                self.rect.y += 27
                self.estado = 0
        # Usando vara
        elif self.estado == 6:
            #La vara solo se puede usar si no hay una llama activa
            if self.vara == None or self.vara.is_alive():
                self.estado = 0
            else:
                #self.image = self.L[3][self.dir][self.i_sprite]
                self.sprite_index1 = 3
                self.sprite_index2 = self.dir
                x = 0
                y = 0
                if self.dir == 0:
                    self.hurtbox.w = 34
                    self.hurtbox.h = 32
                    x = self.rect.x+52
                    y = self.rect.y+16
                elif self.dir == 1:
                    self.rect.x -= 26
                    self.hurtbox.w = 33
                    self.hurtbox.h = 32
                    x = self.rect.x+3
                    y = self.rect.y+16
                elif self.dir == 2:
                    self.rect.y -= 29
                    self.hurtbox.y = self.rect.y+29
                    self.hurtbox.w = 32
                    self.hurtbox.h = 35
                    x = self.rect.x+15
                    y = self.rect.y+3
                else:
                    self.hurtbox.w = 32
                    self.hurtbox.h = 35
                    x = self.rect.x+19
                    y = self.rect.y+54
                self.llama = self.vara.atacar([x, y], self.dir)
                self.estado = 2
                self.con = -9
        # Hitlag (Golpeado)
        elif self.estado == 7:
            if self.con < 5:
                self.rect.x += self.velx
                self.rect.y += self.vely
                self.hurtbox.x = self.rect.x
                self.hurtbox.y = self.rect.y
                self.con += 1
            else:
                self.velx = 0
                self.vely = 0
                self.con = 0
                self.estado = 0
        # Cayendo
        elif self.estado == 8:
            if self.con < 15:
                self.image = pygame.transform.scale(self.image, (self.image.get_width()-2,self.image.get_height()-2))
                self.rect.x += 1
                self.rect.y += 1
                self.con += 1
            elif self.con < 16:
                alpha_img = pygame.Surface(self.image.get_rect().size, pygame.SRCALPHA)
                alpha_img.fill((255, 255, 255, 0))
                alpha_img.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                self.image = alpha_img
                self.con += 1
            elif self.con < 30:
                self.con += 1
            else:
                self.fall_sfx.stop()
                self.hurt_sfx.play()
                self.salud -= 1
                self.rect.x = self.spawn[0]
                self.rect.y = self.spawn[1]
                self.invulnerable = True
                self.i_con = 0
                self.con = 0
                self.estado = 0
        
        if self.estado != 8 and not self.freeze:
            self.image = self.L[self.sprite_index1][self.sprite_index2][self.i_sprite]
        
        #transiciones de un escenario a otro mediante los estremos del jugador
        if self.nivel == 1:
            if self.rect.left >= ANCHO:
                self.mapa_actual = ubicaciones[self.mapa_actual][1]
                self.rect.x = self.rect.x - ANCHO
                self.cambio = True
            if self.rect.right <= 0:
                self.mapa_actual = ubicaciones[self.mapa_actual][0]
                self.rect.x = self.rect.x + ANCHO
                self.cambio = True
            if self.rect.bottom <= 0:
                self.mapa_actual = ubicaciones[self.mapa_actual][2]
                self.rect.y = self.rect.y + ALTO + 32 
                self.cambio = True
            if self.rect.top >= ALTO and self.mapa_actual != 12 and self.mapa_actual != 13 and self.mapa_actual != 14:
                self.mapa_actual = ubicaciones[self.mapa_actual][3]
                self.rect.y = self.rect.y - ALTO
                self.cambio = True
            if self.rect.top >= ALTO and (self.mapa_actual == 12 or self.mapa_actual == 13 or self.mapa_actual == 14) and self.dir == 3:
                if self.mapa_actual == 12:
                 self.rect.y = 32
                 self.rect.x = 128
                elif self.mapa_actual == 13:
                 self.rect.y = 32
                 self.rect.x = 224  
                elif self.mapa_actual == 14:
                    self.rect.y = 32
                    self.rect.x = 320  

                self.cambio = True

                self.mapa_actual = ubicaciones[self.mapa_actual][3]       
        elif self.nivel == 2:
            if self.rect.left >= ANCHO - 58:
                self.mapa_actual = ubicaciones[self.mapa_actual][1]
                self.rect.x = ANCHO - self.rect.x
                self.cambio = True
            if self.rect.right <= 58:
                self.mapa_actual = ubicaciones[self.mapa_actual][0]
                self.rect.x = ANCHO - 64
                self.cambio = True
            if self.rect.bottom <= 58:
                self.mapa_actual = ubicaciones[self.mapa_actual][2]
                self.rect.y = ALTO - 64
                self.cambio = True
            if self.rect.top >= (ALTO - 58) and self.mapa_actual != 12 and self.mapa_actual != 13 and self.mapa_actual != 14:
                self.mapa_actual = ubicaciones[self.mapa_actual][3]
                self.rect.y = ALTO - self.rect.y 
                self.cambio = True

        #Colision con el mapa
        if not self.cambio:
            ls_obj = []
            ls_cuevas = []

            for b in self.bloques:
                if self.hurtbox.colliderect(b):
                    ls_obj.append(b)

            for b in ls_obj:
                if self.hurtbox.right > b.rect.left and self.velx > 0:
                    self.hurtbox.right = b.rect.left
                    self.rect.left = self.hurtbox.left
                    self.velx = 0

                if self.hurtbox.left < b.rect.right and self.velx < 0:
                    self.hurtbox.left = b.rect.right
                    self.rect.right = self.hurtbox.right
                    self.velx = 0

                if self.hurtbox.bottom > b.rect.top and self.vely > 0:
                    self.hurtbox.bottom = b.rect.top
                    self.rect.top = self.hurtbox.top
                    self.vely = 0

                if self.hurtbox.top < b.rect.bottom and self.vely < 0:
                    self.hurtbox.top = b.rect.bottom
                    self.rect.bottom = self.hurtbox.bottom
                    self.vely = 0
            
            if self.estado != 8:
                for h in self.hueco:
                    if self.rect.collidepoint(h.rect.center):
                        self.estado = 8
                        self.sprite_index2 = self.dir
                        self.fall_sfx.play()
            
            #colision con la cueva
            for c in self.cuevas:
                if self.hurtbox.colliderect(c) and (self.mapa_actual!=7 or self.key):
                    ls_cuevas.append(c)

            for c in ls_cuevas:
                if self.hurtbox.bottom <= c.rect.bottom and self.dir == 2:
                    if self.mapa_actual == 7:
                        self.nivel = 2
                        self.mapa_actual = 17
                        self.rect.y = ALTO - 64
                        self.rect.x = 240
                    else:
                        self.mapa_actual = ubicaciones[self.mapa_actual][4]
                        self.rect.y = ALTO
                        self.rect.x = 240
                    self.cambio = True
        else:
            self.spawn = [self.rect.x, self.rect.y]
class Bloque (pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([24, 24])
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Cueva(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([32, 32])
        self.image.fill(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Hueco(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([32, 32])
        self.image.fill(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]



class Music_manager:
    
    def __init__ (self, music, song_list):
        self.music = music
        self.estado = 0
        self.index = -1
        self.songs = song_list
        self.volume = 1
        self.looped = False
        self.pausa = False
    
    def set_music(self, m, n):
        #La música depende del mapa, y chequea si ya se reproduce
        #la canción correspondiente
        if n == 2 and self.index != 1:
            self.music.load(self.songs[1])
            self.music.play(-1)
            self.estado = 1
            self.index = 1
            self.looped = False
        elif m == 12 and n == 1:
            self.volume=0.5
            self.estado = 1
            self.index = 0
        elif n == 1 and self.index != 0:
            self.music.load(self.songs[0])
            self.music.play()
            self.estado = 1
            self.index = 0
            self.looped = False
        if n == 1 and m != 12 and self.music.get_volume() < 1:
            self.volume = 1
    
    def stop(self):
        self.music.stop()
        self.estado = 0
        self.index = -1
    
    def loop(self):
        #Revisa si hay música sonando
        if self.estado != 0:
            #Se obtiene la posición de la reproducción
            pos = self.music.get_pos()
            #Chequea si la música ya loopeó por 1ra vez
            if not self.looped:
                #El punto de loop depende de la canción
                if self.index == 0:
                    if pos >= 45055:
                        self.music.stop()
                        self.music.play(-1, 12.034)
                        self.looped = True
            else:
                #Debido al desplazamiento de inicio al loopear,
                #el punto de loop luego de la primera repeteción
                #cambia
                if self.index == 0:
                    if pos >= 33021:
                        self.music.stop()
                        self.music.play(-1, 12.034)
    
    def update(self, l_estado, pausa):
        #La música se mutea cuando Link obtiene un objeto importante
        if pausa and not self.pausa:
            self.volume = self.volume/2
            self.pausa = True
        if not  pausa and self.pausa:
            self.volume = self.volume*2
            self.pausa = False
        if l_estado == 5 and self.estado == 1:
            self.music.set_volume(0)
            self.estado = 2
        #La música vuelve a sonar cuando termina la animación
        elif self.estado == 2 and l_estado != 5:
            self.music.set_volume(self.volume)
            self.estado = 1
        elif self.estado == 1:
            self.music.set_volume(self.volume)
        self.loop()


class Generador1(pygame.sprite.Sprite):
    def __init__(self, pos, m):
        pygame.sprite.Sprite.__init__(self)
        self.image = m
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.temp = 60
        self.inv = 0
        self.vida = 3
        self.muerto = False
        self.sfx_hurt = pygame.mixer.Sound("sfx/LOZ_Bomb_Blow.wav")
        self.sfx_dead = pygame.mixer.Sound("sfx/LOZ_Boss_Scream2.wav")

    #Tarda unos frames en desaparecer el sprite
    def morir(self):
        if self.inv > 0:
            self.inv -=1
        else:
            self.kill()
    
    #Si es atacado con fuego es instakill
    def herir (self, tipo):
        if self.inv == 0:
            if tipo == 0:
                self.vida -= 1
                self.inv = 5
                self.sfx_hurt.play()
            else:
                self.vida -= 3
    
    def update(self):
        #Solo crea enemigos si tiene vida
        if self.muerto:
            self.morir()
        elif self.vida <= 0:
            self.inv = 5
            self.sfx_dead.play()
            self.muerto = True
        else:
            self.temp -= 1
            if self.inv > 0:
                self.inv -= 1


class Enemigo1(pygame.sprite.Sprite):
    def __init__(self, m, pos, bloques):
        pygame.sprite.Sprite.__init__(self)
        self.m=m
        self.dir=0
        self.con=0
        self.dircon = 0
        self.muerto = False
        self.sfx = pygame.mixer.Sound("sfx/LOZ_Enemy_Hit.wav")
        #Tiempo aleatorio para cambiar de direccion
        self.dirumbral = random.randrange(4, 8)*32
        self.image=self.m[self.con][self.dir]
        self.rect=self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.velx=0
        self.vely=0
        self.Arrow_temp = 20
        self.bloques = bloques
    
    #Cambio de dirección cuando choca con bloque o pasa el tiempo establecido
    def change_dir(self):
        dire = [0,1,2,3]
        #Se elimina la dirección actual de las posibles
        dire.remove(self.dir)
        newdir = random.choice(dire)
        if newdir == 0:
            velx = 4
            vely = 0
        elif newdir == 1:
            velx = -4
            vely = 0
        elif newdir == 2:
            velx = 0
            vely = -4
        else:
            velx = 0
            vely = 4
        #Revisa si se puede ir en la nueva dirección
        self.rect.x += velx*2
        self.rect.y += vely*2
        ls_obj = []
        ls_obj = pygame.sprite.spritecollide(self, self.bloques, False)
        if not ls_obj:
            self.dir = newdir
            self.velx = velx
            self.vely = vely
            self.dircon = 0
            #Se escoge un nuevo tiempo aleatorio
            self.dirumbral = random.randrange(3,8)*32
        self.rect.x -= velx*2
        self.rect.y -= vely*2
    
    def morir(self, Link):
        if not self.muerto:
            self.sfx.play()
            self.muerto = True
            self.image = self.m[2]
            self.con = 0
            Link.score += 1
            return True
        else:
            return False
    
    def morir_llama(self, Link):
        return self.morir(Link)
    
    def update(self):
        #Mantiene el sprite de muerte unos frames
        if self.muerto:
            if self.con < 5:
                self.con += 1
            else:
                self.kill()
        else:
            self.Arrow_temp -= 1

            if self.Arrow_temp == 0:
                arrow = Flecha(self.rect.centerx, self.rect.centery, self.dir, self.bloques)
                proyectiles_e.add(arrow)
                self.Arrow_temp = 50

            if self.dir == 0:
                self.velx = 4
                self.vely = 0
            elif self.dir == 1:
                self.velx = -4
                self.vely = 0
            elif self.dir == 2:
                self.velx = 0
                self.vely = -4
            else:
                self.velx = 0
                self.vely = 4
            
            self.rect.x+=self.velx
            self.rect.y+=self.vely
            
            if self.rect.bottom > ALTO + 32:
                self.dir = 2
                self.dircon = 0
            elif self.rect.y < 0:
                self.dir = 3
                self.dircon = 0
            elif self.rect.right > ANCHO:
                self.dir = 1
                self.dircon = 0
            elif self.rect.left < 0:
                self.dir = 0
                self.dircon = 0

            if self.velx != 0 or self.vely != 0:
                self.image = self.m[self.con][self.dir]
                if self.con < 1:
                    self.con += 1
                else: 
                    self.con = 0
            
            #Controla el choque con bloques
            ls_obj = []
            ls_obj = pygame.sprite.spritecollide(self, self.bloques, False)

            for b in ls_obj:
                if self.rect.right > b.rect.left and self.dir == 0:
                    self.rect.right = b.rect.left
                    self.change_dir()

                elif self.rect.left < b.rect.right and self.dir == 1:
                    self.rect.left = b.rect.right
                    self.change_dir()

                elif self.rect.bottom > b.rect.top and self.dir == 3:
                    self.rect.bottom = b.rect.top
                    self.change_dir()

                elif self.rect.top < b.rect.bottom and self.dir == 2:
                    self.rect.top = b.rect.bottom
                    self.change_dir()
            
            #Cuando pasa el tiempo, cambia de dirección
            if self.dircon == self.dirumbral:
                self.change_dir()
            
            self.dircon += 4

class Enemigo3(pygame.sprite.Sprite):
    def __init__(self, m, pos, bloques):
        pygame.sprite.Sprite.__init__(self)
        self.m=m
        self.dir=0
        self.con=0
        self.dircon = 0
        self.muerto = False
        self.sfx = pygame.mixer.Sound("sfx/LOZ_Enemy_Hit.wav")
        self.hit = pygame.mixer.Sound("sfx/LOZ_Shield.wav")
        #Tiempo aleatorio para cambiar de direccion
        self.dirumbral = random.randrange(4, 8)*32
        self.image=self.m[self.con][self.dir]
        self.rect=self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.velx=0
        self.vely=0
        self.walk_temp = 5
        self.bloques = bloques
    
    #Cambio de dirección cuando choca con bloque o pasa el tiempo establecido
    def change_dir(self):
        dire = [0,1,2,3]
        #Se elimina la dirección actual de las posibles
        dire.remove(self.dir)
        newdir = random.choice(dire)
        if newdir == 0:
            velx = 4
            vely = 0
        elif newdir == 1:
            velx = -4
            vely = 0
        elif newdir == 2:
            velx = 0
            vely = -4
        else:
            velx = 0
            vely = 4
        #Revisa si se puede ir en la nueva dirección
        self.rect.x += velx*2
        self.rect.y += vely*2
        ls_obj = []
        ls_obj = pygame.sprite.spritecollide(self, self.bloques, False)
        if not ls_obj:
            self.dir = newdir
            self.velx = velx
            self.vely = vely
            self.dircon = 0
            #Se escoge un nuevo tiempo aleatorio
            self.dirumbral = random.randrange(3,8)*32
        self.rect.x -= velx*2
        self.rect.y -= vely*2
    
    def morir(self, Link):
        if not self.muerto:
            if Link.dir==self.dir:
                self.sfx.play()
                self.muerto = True
                self.image = self.m[2]
                self.con = 0
                Link.score += 1
                return True
            else:
                self.hit.play()
                return False
        else:
            return False
    
    def morir_llama(self, Link):
        return False
    
    def update(self):
        #Mantiene el sprite de muerte unos frames
        if self.muerto:
            if self.con < 5:
                self.con += 1
            else:
                self.kill()
        else:

            self.walk_temp -= 1

            if self.dir == 0:
                self.velx = 4
                self.vely = 0
            elif self.dir == 1:
                self.velx = -4
                self.vely = 0
            elif self.dir == 2:
                self.velx = 0
                self.vely = -4
            else:
                self.velx = 0
                self.vely = 4
            
            self.rect.x+=self.velx
            self.rect.y+=self.vely
            
            if self.rect.bottom > ALTO + 32:
                self.dir = 2
                self.dircon = 0
            elif self.rect.y < 0:
                self.dir = 3
                self.dircon = 0
            elif self.rect.right > ANCHO:
                self.dir = 1
                self.dircon = 0
            elif self.rect.left < 0:
                self.dir = 0
                self.dircon = 0

            if self.walk_temp <= 0:
                self.walk_temp = 5
                if self.velx != 0 or self.vely != 0:
                    self.image = self.m[self.con][self.dir]
                    if self.con < 1:
                        self.con += 1
                    else: 
                        self.con = 0
            
            #Controla el choque con bloques
            ls_obj = []
            ls_obj = pygame.sprite.spritecollide(self, self.bloques, False)

            for b in ls_obj:
                if self.rect.right > b.rect.left and self.dir == 0:
                    self.rect.right = b.rect.left
                    self.dir = 1

                elif self.rect.left < b.rect.right and self.dir == 1:
                    self.rect.left = b.rect.right
                    self.dir = 0

                elif self.rect.bottom > b.rect.top and self.dir == 3:
                    self.rect.bottom = b.rect.top
                    self.dir = 2

                elif self.rect.top < b.rect.bottom and self.dir == 2:
                    self.rect.top = b.rect.bottom
                    self.dir = 3
            
            #Cuando pasa el tiempo, cambia de dirección
            if self.dircon == self.dirumbral:
                self.change_dir()
            
            self.dircon += 4

# -------------------------- Murcielago ---------------------

class Enemigo4(pygame.sprite.Sprite):
    def __init__(self, m, pos, bloques):
        pygame.sprite.Sprite.__init__(self)
        self.m=m
        self.dir=0
        self.con=0
        self.dircon = 0
        self.muerto = False
        self.sfx = pygame.mixer.Sound("sfx/LOZ_Enemy_Hit.wav")
        #Tiempo aleatorio para cambiar direccion
        self.dirumbral = random.randrange(4,8)*32
        self.image=self.m[self.con]
        self.rect=self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.velx=0
        self.vely=0
        self.alas_temp = 5
        self.bloques = bloques
    
    #Cambio de dirección cuando choca con bloque o pasa el tiempo establecido
    def change_dir(self):
        dire = [0,1,2,3]
        #Se elimina la dirección actual de las posibles
        dire.remove(self.dir)
        newdir = random.choice(dire)
        if newdir == 0:
            velx = 4
            vely = 0
        elif newdir == 1:
            velx = -4
            vely = 0
        elif newdir == 2:
            velx = 0
            vely = -4
        elif newdir == 3:
            velx = 0
            vely = 4
        #Revisa si se puede ir en la nueva dirección
        self.rect.x += velx*1
        self.rect.y += vely*1
        ls_obj = []
        ls_obj = pygame.sprite.spritecollide(self, self.bloques, False)
        if not ls_obj:
            self.dir = newdir
            self.velx = velx
            self.vely = vely
            self.dircon = 0
            #Se escoge un nuevo tiempo aleatorio
            self.dirumbral = random.randrange(5,10)*20
        self.rect.x -= velx
        self.rect.y -= vely
    
    def morir(self, Link):
        if not self.muerto:
            self.sfx.play()
            self.muerto = True
            self.image = self.m[1]
            self.con = 0
            Link.score += 1
            return True
        else:
            return False
    
    def morir_llama(self, Link):
        return self.morir(Link)
    
    def update(self):
        #Mantiene el sprite de muerte unos frames
        if self.muerto:
            if self.con < 5:
                self.con += 1
            else:
                self.kill()
        else:
            
            self.alas_temp -= 1
            
            if self.rect.bottom > ALTO + 32:
                self.dir = 2
                self.velx = 0
                self.vely = -4
                self.dircon -= 15
            elif self.rect.y < 0:
                self.dir = 3
                self.velx = 0
                self.vely = 4
                self.dircon -= 15
            elif self.rect.right > ANCHO:
                self.dir = 1
                self.velx = -4
                self.vely = 0
                self.dircon -= 15
            elif self.rect.left < 0:
                self.dir = 0
                self.velx = 4
                self.vely = 0
                self.dircon -= 15

            self.rect.x+=self.velx
            self.rect.y+=self.vely

            if self.alas_temp <= 0:
                self.alas_temp = 5
                if self.velx != 0 or self.vely != 0:
                    self.image = self.m[self.con]
                    if self.con < 1:
                        self.con += 1
                    else: 
                        self.con = 0
            
            
            #Controla el choque con bloques
            ls_obj = []

            ls_obj = pygame.sprite.spritecollide(self, self.bloques, False)

            for b in ls_obj:
                if self.rect.right > b.rect.left and self.dir == 0:
                    self.rect.right = b.rect.left
                    self.change_dir()

                elif self.rect.left < b.rect.right and self.dir == 1:
                    self.rect.left = b.rect.right
                    self.change_dir()

                elif self.rect.bottom > b.rect.top and self.dir == 3:
                    self.rect.bottom = b.rect.top
                    self.change_dir()

                elif self.rect.top < b.rect.bottom and self.dir == 2:
                    self.rect.top = b.rect.bottom
                    self.change_dir()
            
            #Cuando pasa el tiempo, cambia de dirección
            if self.dircon == self.dirumbral:
                self.change_dir()
                
            self.dircon += 5


class Flecha(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bloques):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        # Derecha
        if self.direction == 0:
            self.image = pygame.image.load("librerias_juego/Arrow_right.png")
        # Izquierda
        elif self.direction == 1:
            self.image = pygame.image.load("librerias_juego/Arrow_left.png")
        # Arriba
        elif self.direction == 2:
            self.image = pygame.image.load("librerias_juego/Arrow_up.png")
        # Abajo
        elif self.direction == 3:
            self.image = pygame.image.load("librerias_juego/Arrow_down.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.bloques = bloques
        if self.direction == 0:
            self.vx = 12
            self.vy = 0
        elif self.direction == 1:
            self.vx = -12
            self.vy = 0
        elif self.direction == 2:
            self.vx = 0
            self.vy = -12
        else:
            self.vx = 0
            self.vy = 12
    
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        ls_obj = []
        ls_obj = pygame.sprite.spritecollide(self, self.bloques, False)
        if ls_obj or self.rect.right < 0 or self.rect.x > ANCHO or self.rect.y > ALTO or self.rect.bottom < 0:
            self.kill()

# ----------------------- Generador 2 (Indestructible) --------------------- #


class Generador2(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([24, 24])
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.temp = 60

    def update(self):
        self.temp -= 1


class Enemigo2(pygame.sprite.Sprite):
    def __init__(self, m, pos, bloques):
        pygame.sprite.Sprite.__init__(self)
        self.m=m
        self.dir=0
        self.con=0
        self.dircon = 0
        self.muerto = False
        self.sfx = pygame.mixer.Sound("sfx/LOZ_Enemy_Hit.wav")
        #Tiempo aleatorio para cambiar direccion
        self.dirumbral = random.randrange(4,8)*32
        self.image=self.m[self.con][self.dir]
        self.rect=self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.velx=0
        self.vely=0
        self.ball_temp = 20
        self.bloques = bloques
    
    #Cambio de dirección cuando choca con bloque o pasa el tiempo establecido
    def change_dir(self):
        dire = [0,1,2,3]
        #Se elimina la dirección actual de las posibles
        dire.remove(self.dir)
        newdir = random.choice(dire)
        if newdir == 0:
            velx = 4
            vely = 0
        elif newdir == 1:
            velx = -4
            vely = 0
        elif newdir == 2:
            velx = 0
            vely = -4
        else:
            velx = 0
            vely = 4
        #Revisa si se puede ir en la nueva dirección
        self.rect.x += velx*1
        self.rect.y += vely*1
        ls_obj = []
        ls_obj = pygame.sprite.spritecollide(self, self.bloques, False)
        if not ls_obj:
            self.dir = newdir
            self.velx = velx
            self.vely = vely
            self.dircon = 0
            #Se escoge un nuevo tiempo aleatorio
            self.dirumbral = random.randrange(4,8)*32
        self.rect.x -= velx
        self.rect.y -= vely
    
    def morir(self, Link):
        if not self.muerto:
            self.sfx.play()
            self.muerto = True
            self.image = self.m[2]
            self.con = 0
            Link.score += 1
            return True
        else:
            return False
    
    def morir_llama(self, Link):
        return self.morir(Link)
    
    def update(self):
        #Mantiene el sprite de muerte unos frames
        if self.muerto:
            if self.con < 5:
                self.con += 1
            else:
                self.kill()
        else:
            self.ball_temp -= 1

            if self.ball_temp == 0:
                arrow = BolaFuego(self.rect.centerx, self.rect.centery, self.dir, self.bloques)
                proyectiles_e.add(arrow)
                self.ball_temp = 50

            if self.dir == 0:
                self.velx = 4
                self.vely = 0
            elif self.dir == 1:
                self.velx = -4
                self.vely = 0
            elif self.dir == 2:
                self.velx = 0
                self.vely = -4
            else:
                self.velx = 0
                self.vely = 4
            
            self.rect.x+=self.velx
            self.rect.y+=self.vely

            if self.velx != 0 or self.vely != 0:
                self.image = self.m[self.con][self.dir]
                if self.con < 1:
                    self.con += 1
                else: 
                    self.con = 0
            
            if self.rect.bottom > ALTO + 32:
                self.dir = 2
                self.dircon -= 15
            elif self.rect.y < 0:
                self.dir = 3
                self.dircon -= 15
            elif self.rect.right > ANCHO:
                self.dir = 1
                self.dircon -= 15
            elif self.rect.left < 0:
                self.dir = 0
                self.dircon -= 15
            
            
            #Controla el choque con bloques
            ls_obj = []

            ls_obj = pygame.sprite.spritecollide(self, self.bloques, False)

            for b in ls_obj:
                if self.rect.right > b.rect.left and self.dir == 0:
                    self.rect.right = b.rect.left
                    self.change_dir()

                elif self.rect.left < b.rect.right and self.dir == 1:
                    self.rect.left = b.rect.right
                    self.change_dir()

                elif self.rect.bottom > b.rect.top and self.dir == 3:
                    self.rect.bottom = b.rect.top
                    self.change_dir()

                elif self.rect.top < b.rect.bottom and self.dir == 2:
                    self.rect.top = b.rect.bottom
                    self.change_dir()
            
            #Cuando pasa el tiempo, cambia de dirección
            if self.dircon == self.dirumbral:
                self.change_dir()
                
            self.dircon += 4


class BolaFuego(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bloques):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        
        self.image = pygame.image.load("librerias_juego/fireball.png")
        if direction == 0 or direction == 1:
            self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.bloques = bloques
        if self.direction == 0:
            self.vx = 10
            self.vy = 0
        elif self.direction == 1:
            self.vx = -10
            self.vy = 0
        elif self.direction == 2:
            self.vx = 0
            self.vy = -10
        else:
            self.vx = 0
            self.vy = 10
        
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        ls_obj = []
        ls_obj = pygame.sprite.spritecollide(self, self.bloques, False)
        if ls_obj or self.rect.right < 0 or self.rect.x > ANCHO or self.rect.y > ALTO or self.rect.bottom < 0:
            self.kill()

class Arbusto(pygame.sprite.Sprite):
    def __init__(self,x,y, sprites):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = sprites
        self.image = sprites[0]
        self.rect = self.image.get_rect()
        self.bloque = Bloque([x,y])
        self.bloque.rect.w = 64
        self.rect.x = x
        self.rect.y = y
        self.con = 0
        self.estado = 0
    
    def update(self):
        if self.estado == 1:
            self.image = self.sprites[self.con%2+1]
            self.con += 1
            if self.con == 40:
                self.estado = 2
        elif self.estado == 2:
            self.kill()
            self.bloque.kill()

class Jefe1(pygame.sprite.Sprite):
    def __init__(self, m, b, pos, bloques, L):
        pygame.sprite.Sprite.__init__(self)
        self.m=m
        self.dir=0
        self.con=0
        self.image=self.m[self.con]
        self.rect=self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.hurtbox = pygame.Rect(0,26, 64, 20)
        self.bloques = bloques
        self.velx=0
        self.vely=0
        self.accx = 0
        self.accy = 0
        self.ball_temp = 40
        self.sball_temp = 180
        self.eye_temp = 10
        self.b = b
        self.salud = 10
        self.i_con = 0
        self.muerto = False
        self.L = L
        #SFX
        self.hit = pygame.mixer.Sound('sfx/LOZFDS_Boss_Hit.wav')
        self.ataque1 = pygame.mixer.Sound('sfx/LOZ_Sword_Shoot.wav')
        self.ataque2 = pygame.mixer.Sound('sfx/LOZFDS_Boss_Scream2.wav')
        self.die = pygame.mixer.Sound('sfx/LOZFDS_Boss_Scream1.wav')

    def morir(self, Link):
        if not self.muerto and self.i_con == 0:
            if Link.dir != 3 and self.hurtbox.colliderect(Link.hitbox):
                self.hit.play()
                self.salud -= 1
                self.i_con = 20
                if self.salud == 0:
                    self.muerto = True
                    self.die.play()
                    self.i_con = 0
        return False
    
    def morir_llama(self, Link):
        return False
    
    def update(self):        

        if self.muerto:
            if self.i_con < 40:
                self.i_con += 1
                if self.i_con%2==0:
                    alpha_img = pygame.Surface(self.image.get_rect().size, pygame.SRCALPHA)
                    alpha_img.fill((255, 255, 255, 0))
                    alpha_img.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                    self.image = alpha_img
                else:
                    self.image = self.m[self.con]
            else:
                self.kill()
                del self
        else:
            self.eye_temp -= 1
            if self.i_con == 0:
                self.ball_temp -= 1
                self.sball_temp -= 1
                
                if self.rect.x < self.L.rect.x:
                    self.accx = 0.5
                elif self.rect.x > self.L.rect.x:
                    self.accx = -0.5
                else:
                    self.accx = 0
                if self.rect.y < self.L.rect.y:
                    self.accy = 0.5
                elif self.rect.y > self.L.rect.y:
                    self.accy = -0.5
                else:
                    self.accy = 0
                
                self.velx+=self.accx
                self.vely+=self.accy
                if self.velx < -1:
                    self.velx = -1
                elif self.velx > 1:
                    self.velx = 1
                if self.vely < -1:
                    self.vely = -1
                elif self.vely > 1:
                    self.vely = 1
                
                if self.ball_temp <= 0:
                    for d in range(4):
                        self.ataque1.play()
                        arrow = BolaAzul(self.rect.x+20, self.rect.y+20, d, self.bloques)
                        proyectiles_e.add(arrow)
                    self.ball_temp = 55
                
                if self.sball_temp <= 0:
                        self.ataque2.play()
                        sball = BolaHielo(self.b, self.rect.x+20, self.rect.y+20, self.bloques, self.L)
                        proyectiles_e.add(sball)
                        self.sball_temp = 150

                

                self.rect.x=round(self.rect.x+self.velx)
                self.rect.y=round(self.rect.y+self.vely)
                self.hurtbox.x=round(self.rect.x+self.velx)
                self.hurtbox.y=round(self.rect.y+self.vely)
            else:
                self.i_con -= 1

            if self.eye_temp <= 0:
                self.image = self.m[self.con]
                self.eye_temp = 5
                if self.con < 7:
                    self.con += 1
                else: 
                    self.con = 0

# --------------- Ataque básico Jefe 1 ---------------------

class BolaAzul(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bloques):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.image = pygame.image.load("librerias_juego/blue_ball.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bloques =  bloques
        
    def update(self):
        if self.direction == 0:
            self.rect.x += 10
        elif self.direction == 1:
            self.rect.x -= 10
        elif self.direction == 2:
            self.rect.y -= 10
        elif self.direction == 3:
            self.rect.y += 10
        ls_obj = []
        ls_obj = pygame.sprite.spritecollide(self, self.bloques, False)
        if ls_obj or self.rect.right < 0 or self.rect.x > ANCHO or self.rect.y > ALTO or self.rect.bottom < 0:
            self.kill()

# ---------------- Esfera de Hielo -------------------

class BolaHielo(pygame.sprite.Sprite):
    def __init__(self, b, x, y, bloques, L):
        pygame.sprite.Sprite.__init__(self)
        self.b = b
        self.con = 0
        self.image = b[self.con]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velx = 0
        self.vely = 0
        self.accx = 0
        self.accy = 0
        self.ball_temp = 10
        self.temp = 0
        self.bloques = bloques
        self.L = L
        self.sfx = pygame.mixer.Sound("sfx/LOZ_Shield.wav")
        
    def update(self):

        self.ball_temp -= 1        
            
        if self.rect.centerx < self.L.rect.centerx:
            self.accx = 0.5
        elif self.rect.centerx > self.L.rect.centerx:
            self.accx = -0.5
        else:
            self.accx = 0
        if self.rect.centery < self.L.rect.centery:
            self.accy = 0.5
        elif self.rect.centery > self.L.rect.centery:
            self.accy = -0.5
        else:
            self.accy = 0

        self.velx+=self.accx
        self.vely+=self.accy
        if self.velx < -3:
            self.velx = -3
        elif self.velx > 3:
            self.velx = 3
        if self.vely < -3:
            self.vely = -3
        elif self.vely > 3:
            self.vely = 3
        self.rect.x=round(self.rect.x+self.velx)
        self.rect.y=round(self.rect.y+self.vely)
        
        ls_obj = []
        ls_obj = pygame.sprite.spritecollide(self, self.bloques, False)
        if ls_obj or self.rect.right < 0 or self.rect.x > ANCHO or self.rect.y > ALTO or self.rect.bottom < 0:
            self.sfx.play()
            self.kill()
        elif self.temp >= 100:
            self.kill()

        self.temp += 1
        if self.ball_temp <= 0:
            self.image = self.b[self.con]
            self.ball_temp = 3
            if self.con < 3:
                self.con += 1
            else: 
                self.con = 0

class Puas(pygame.sprite.Sprite):
    
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('librerias_juego/puas.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]