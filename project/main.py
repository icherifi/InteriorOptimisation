import pygame
from Room import Room
from SimulatedAnnealing import SimulatedAnnealing
import numpy as np


# Create room and objects
room_shape = np.array([522, 347])
room = Room(room_shape)
objects = room.create_objects()

# Simulated annealing
sa = SimulatedAnnealing(room)
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

    for obj in objects:
        rect = obj.get_rect(solution[obj.index], screen_shape, room_shape)
        pygame.draw.rect(screen, obj.color, rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
