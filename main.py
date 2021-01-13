import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

G = 6.67e-3

# class is bascially a C struct
# the less ogj-functions the more functional
class Astro():
    def __init__(self, name, vec, radius, mass):
        self.name = name
        self.vec = np.array(vec, dtype=np.float)
        self.acc = np.array((0.0, 0.0, 0.0) , dtype=np.float)
        self.v_i = 0.0
        self.vel = np.array((0.0, 0.0, 0.0) , dtype=np.float)
        self.vtang = 0
        self.mass, self.radius = mass, radius
        
    def draw(self):
        glTranslatef(self.vec[0], self.vec[1], self.vec[2])
        glColor4f(0.2, 0.2, 0.5, 1)
        gluSphere(sphere, self.radius, 64, 64)


        

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
display = (1200, 720)
scree = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glShadeModel(GL_SMOOTH)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])

sphere = gluNewQuadric() 

glMatrixMode(GL_PROJECTION)
gluPerspective(90, (display[0]/display[1]), 0.1, 50.0)

glMatrixMode(GL_MODELVIEW)
gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
glLoadIdentity()

# init mouse movement and center mouse on screen
displayCenter = [scree.get_size()[i] // 2 for i in range(2)]
mouseMove = [0, 0]
pygame.mouse.set_pos(displayCenter)

up_down_angle = 0.0
paused = False
run = 0
dt = 1e-1


Earth = Astro("Earth", (0.0, 0.0, 0.0), 0.6, 100)
Moon = Astro("Moon", (8.0, 0.0, 0.0), 0.3, 12)


SolarBodies = []
#Sun is stationary

SolarBodies.append(Earth)
SolarBodies.append(Moon)


# THE WHILE LOOP
while (run > -1):
    run += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = -1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                run = -1
            if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                paused = not paused
                pygame.mouse.set_pos(displayCenter) 
        if not paused: 
            if event.type == pygame.MOUSEMOTION:
                mouseMove = [event.pos[i] - displayCenter[i] for i in range(2)]
            pygame.mouse.set_pos(displayCenter)
    if not paused:
        
        keypress = pygame.key.get_pressed()
    
        # init model view matrix
        glLoadIdentity()

        # apply the look up and down
        up_down_angle += mouseMove[1]*0.1
        glRotatef(up_down_angle, 1.0, 0.0, 0.0)

        # init the view matrix
        glPushMatrix()
        glLoadIdentity()

        # apply the movment
        k = 0.1
        if keypress[pygame.K_LSHIFT]:
            k = 1
        if keypress[pygame.K_w]:
            glTranslatef(0,0,k)
        if keypress[pygame.K_s]:
            glTranslatef(0,0,-k)
        if keypress[pygame.K_d]:
            glTranslatef(-k,0,0)
        if keypress[pygame.K_a]:
            glTranslatef(k,0,0)
        if keypress[pygame.K_SPACE]:
            glTranslatef(0,-k,0)
        if keypress[pygame.K_LCTRL]:
            glTranslatef(0,k,0)


        # apply the left and right rotation
        glRotatef(mouseMove[0]*0.1, 0.0, 0.1, 0.0)

        # multiply the current matrix by the get the new view matrix and store the final view matrix 
        glMultMatrixf(viewMatrix)
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        # apply view matrix
        glPopMatrix()
        glMultMatrixf(viewMatrix)

        #glLightfv(GL_LIGHT0, GL_POSITION, [1, -1, 1, 0])

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glPushMatrix()

        # Logic
        for i in SolarBodies:
            i.vec += i.vel*dt 
            for j in SolarBodies:
                if (i != j):
                    r = (i.vec-j.vec)
                    i.acc = -G * j.mass * (r) / np.sum(r**2)**(3./2)
            i.vel += (i.acc * dt)

        if keypress[pygame.K_v]:
            Moon.vel[1] = (G*100/abs(np.sum(r)))**0.5
            Earth.vel[1] = (G*0.1/abs(np.sum(r)))**0.5
        if keypress[pygame.K_UP]:
            Moon.vel[1] += 0.01 
        if keypress[pygame.K_DOWN]:
            Moon.vel[1] -= 0.01

        #print(Moon.vel[1])
        
        textsurface = myfont.render('Some Text', False, (0, 0, 0))
        scree.blit(textsurface,(10,10))

        # Draw
        for i in SolarBodies:
            i.draw()
        glPopMatrix()
        
        pygame.display.flip()
        pygame.time.wait(10)

pygame.quit()
