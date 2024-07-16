import math
import numpy as np
import pygame
import random

# Variables
room_shape =  np.array([522,347])
objects = [
    {
        "name": 'TV',
        "shape": (290,40),
        "color": 'black',
        "noOverlapShape": (290,40),
    },
    {
        "name": 'Canapé',
        "shape": (270,90),
        "color": 'blue',
        "noOverlapShape": (270,90),
    },
    {
        "name": 'Fauteuil1',
        "shape": (95,75),
        "color": 'red',
        "noOverlapShape": (115,90),
    },
    {
        "name": 'Fauteuil2',
        "shape": (95,75),
        "color": 'red',
        "noOverlapShape": (115,90),
    },
    {
        "name": 'Table',
        "shape": (115,90),
        "color": 'yellow',
        "noOverlapShape": (120,95),
    },
    {
        "name": 'Plante',
        "shape": (105,100),
        "color": 'green',
        "noOverlapShape": (135,120),
    },
]
def randomState():
    state = [None]*len(objects)
    for idx,obj in enumerate(objects):
        state[idx] = np.array([
            random.randint(obj['shape'][0]//2,room_shape[0]-obj['shape'][0]//2),
            random.randint(obj['shape'][1]//2,room_shape[1]-obj['shape'][1]//2),
        ])
    return state

def randomNeighbour(state):
    newState = state[:]
    randomIdx = random.randrange(0,len(objects))
    randomVect = random.choice([(0,1),(1,0),(0,-1),(-1,0)])
    newState[randomIdx] = np.add(state[randomIdx],randomVect)
    return newState

def E(s):
    n = len(s)

    # Colisions
    colisions = 0
    for i in range(n):
        for j in range(i+1,n):
            area = max(0, min(s[i][0]+objects[i]['shape'][0]/2,s[j][0]+objects[j]['shape'][0]/2) \
                         -max(s[i][0]-objects[i]['shape'][0]/2, s[j][0]-objects[j]['shape'][0]/2) \
                   ) \
                 * max(0, min(s[i][1]+objects[i]['shape'][1]/2,s[j][1]+objects[j]['shape'][1]/2) \
                         -max(s[i][1]-objects[i]['shape'][1]/2, s[j][1]-objects[j]['shape'][1]/2) \
                   )
            colisions += area
    colisions = math.sqrt(colisions)
    
    # Overlap
    overlap = 0
    for i in range(n):
        for j in range(0,n):
            if i != j:
                # Zone de i avec la taille noOverlapShape qui chevauche j avec la taille shape 
                # moins la zone collision deja prise en compte
                area = (max(0, min(s[i][0]+objects[i]['noOverlapShape'][0]/2,s[j][0]+objects[j]['shape'][0]/2) \
                            -max(s[i][0]-objects[i]['noOverlapShape'][0]/2, s[j][0]-objects[j]['shape'][0]/2) \
                    ) - max(0, min(s[i][0]+objects[i]['shape'][0]/2,s[j][0]+objects[j]['shape'][0]/2) \
                            -max(s[i][0]-objects[i]['shape'][0]/2, s[j][0]-objects[j]['shape'][0]/2) \
                    ))\
                    * (max(0, min(s[i][1]+objects[i]['noOverlapShape'][1]/2,s[j][1]+objects[j]['shape'][1]/2) \
                            -max(s[i][1]-objects[i]['noOverlapShape'][1]/2, s[j][1]-objects[j]['shape'][1]/2) \
                    ) - max(0, min(s[i][1]+objects[i]['shape'][1]/2,s[j][1]+objects[j]['shape'][1]/2) \
                            -max(s[i][1]-objects[i]['shape'][1]/2, s[j][1]-objects[j]['shape'][1]/2) \
                    ))
                overlap += area
    overlap = math.sqrt(overlap)

    # Border
    border = 0
    for i in range(n):
        area = (max(0, -(s[i][0]-objects[i]['shape'][0]/2)) + max(0, s[i][0]+objects[i]['shape'][0]/2 - room_shape[0])) * objects[i]['shape'][1] \
             + (max(0, -(s[i][1]-objects[i]['shape'][1]/2)) + max(0, s[i][1]+objects[i]['shape'][1]/2 - room_shape[1])) * objects[i]['shape'][0]
        border += area
    border = math.sqrt(border)

    # Table between tv and sofa
    tableIdx = [i for i in range(n) if objects[i]["name"] == "Table"][0]
    tvIdx = [i for i in range(n) if objects[i]["name"] == "TV"][0]
    sofaIdx = [i for i in range(n) if objects[i]["name"] == "Canapé"][0]

    tbl_score = 0
    vectSofaTv = np.subtract(s[tvIdx],s[sofaIdx])
    vectSofaTable = np.subtract(s[tableIdx],s[sofaIdx])

    normVectSofaTv = math.sqrt(vectSofaTv[0]**2 + vectSofaTv[1]**2)
    normVectSofaTable = math.sqrt(vectSofaTable[0]**2 + vectSofaTable[1]**2)
    # cos
    tbl_score = (1 - ((vectSofaTv[0]*vectSofaTable[0] + vectSofaTv[1]*vectSofaTable[1]) / (normVectSofaTv*normVectSofaTable)))*room_shape[0]
    # table before tv
    tbl_score += max(0, normVectSofaTable - normVectSofaTv)

    #  # colinear
    # tbl_score = abs(vectSofaTv[0]*vectSofaTable[1] - vectSofaTable[0]*vectSofaTv[1])

    # tbl_score += max(0, s[tvIdx][1] - s[tableIdx][1])
    # tbl_score += max(0, s[tableIdx][1]- s[sofaIdx][1])

    return colisions + border + tbl_score + overlap

# Algo recuit

# Params
kmax = 400
T0 = 2000
l = 0.97
def P(delta_E, T):
    return math.exp(- delta_E / T)


# Loop
s = randomState()
e = E(s)
g,m = s,e
k = 0
T = T0
while k<kmax and e > 4:
    for _ in range(150):
        sp = randomNeighbour(s)
        ep = E(sp)
        if ep < e or random.random() < P(ep-e, T):
            s,e = sp,ep
        if e < m:
            g,m = s,e
    k += 1
    T *= l
print(k,m)

# pygame setup
pygame.init()
screen_shape = (640, 360)
screen = pygame.display.set_mode(screen_shape)
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # Plan
    pygame.draw.rect(screen, "black", pygame.Rect((screen_shape[0]/2-room_shape[0]/2,screen_shape[1]/2-room_shape[1]/2),room_shape), width=2)

    # Objects
    for idx,obj in enumerate(objects):
        pygame.draw.rect(
            screen, 
            obj['color'],
            pygame.Rect(
                (
                    screen_shape[0]/2-room_shape[0]/2+g[idx][0]-obj['shape'][0]/2,
                    screen_shape[1]/2-room_shape[1]/2+g[idx][1]-obj['shape'][1]/2
                ),
                obj['shape']
            )
        )

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()