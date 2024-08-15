import pygame
from Room import Room
from SimulatedAnnealing import SimulatedAnnealing
import numpy as np
from Object import Object


# Create room and objects
room_shape = np.array([522, 347])
room = Room(room_shape)
list_objects = [
    Object(0, "TV", (290, 40), "black", (290, 40)),
    Object(1, "Canapé", (270, 90), "blue", (270, 90)),
    Object(2, "Fauteuil1", (95, 75), "red", (115, 90)),
    Object(3, "Fauteuil2", (95, 75), "red", (115, 90)),
    Object(4, "Table", (115, 90), "yellow", (120, 95)),
    Object(5, "Plante", (105, 100), "green", (135, 120)),
]

# Simulated annealing
sa = SimulatedAnnealing(room=room, objects=list_objects)
solution, min_energy = sa.run()
print("Steps:", sa.steps, "Min Energy:", min_energy)


# Pygame setup
pygame.init()
screen_shape = (640, 360)
screen = pygame.display.set_mode(screen_shape)
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    pygame.draw.rect(
        screen,
        "black",
        pygame.Rect(
            (
                screen_shape[0] / 2 - room_shape[0] / 2,
                screen_shape[1] / 2 - room_shape[1] / 2,
            ),
            room_shape,
        ),
        width=2,
    )

    for obj, s in zip(solution.objects, solution.state):
        rect = obj.get_rect(
            s,
            screen_shape,
            room_shape,
        )
        pygame.draw.rect(screen, obj.color, rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
