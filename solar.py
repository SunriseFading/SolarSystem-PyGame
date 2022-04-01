import sys
import pygame
import math
import random as r


pygame.init()

screenW, screenH = 1920, 1080
screen = pygame.display.set_mode((screenW, screenH))
pygame.display.set_caption('Solar System')
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)


G = 6.7 * math.pow(10, -11)

MERCURY_DISTANCE = 1.1 * math.pow(10, 10)
VENUS_DISTANCE = 7.8 * math.pow(10, 10)
EARTH_DISTANCE = 1.5 * math.pow(10, 11)
MARS_DISTANCE = 2.8 * math.pow(10, 11)
JUPITER_DISTANCE = 7.8 * math.pow(10, 11)
SATURN_DISTANCE = 1.4 * math.pow(10, 12)
URANUS_DISTANCE = 1.8 * math.pow(10, 12)
NEPTUNE_DISTANCE = 4.5 * math.pow(10, 12)

MASS_OF_THE_SUN = 2.0 * math.pow(10, 30)

EMULATION_SPEED = 10000000
FPS = 144

# External ressources Load
font = pygame.font.Font('Quicksand.ttf', 32)
bg = pygame.image.load("space.jpg")
sunImg = pygame.image.load("sun.png")


class solarObject:
    def __init__(self, name, color, distancepx, realdistance, radius, range):
        self.name = name
        self.color = color
        self.distancepx = distancepx
        self.realdistance = realdistance
        self.radius = radius
        self.angle = 0
        self.range = range


sun_x = screenW/2
sun_y = screenH/2


def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def calculate_period(radius, central_mass):
    period = (2 * math.pi * math.pow(radius, 3 / 2)) / \
        math.pow(G * central_mass, 1 / 2)
    accelerated_period = period / EMULATION_SPEED
    return round(accelerated_period, 2)


def radiant_per_frame(period):
    total_frames = period * FPS
    return -1 * (2 * math.pi) / total_frames


def convert_to_display_distance(realdistance):
    return 130 + realdistance/EARTH_DISTANCE*20


def convert_to_real_distance(distancepx):
    return (distancepx-130)*EARTH_DISTANCE/20


def mouse_sun_distance(mouse):
    return math.sqrt(math.pow(sun_x-mouse[0], 2) + math.pow(sun_y-mouse[1], 2))


planet_period = 0
planet_radiant_per_frame = 0


sun = solarObject("Sun", (0, 0, 0), 0, 0, 0, (0, 120))

planets = [
    solarObject("Mercury", (255, 100, 20), convert_to_display_distance(
        MERCURY_DISTANCE), MERCURY_DISTANCE, 7, (120, 130)),
    solarObject("Venus", (255, 0, 0), convert_to_display_distance(
        VENUS_DISTANCE), VENUS_DISTANCE, 7, (130, 150)),
    solarObject("Earth", (0, 100, 255), convert_to_display_distance(
        EARTH_DISTANCE), EARTH_DISTANCE, 14, (130, 200)),
    solarObject("Mars", (255, 170, 10), convert_to_display_distance(
        MARS_DISTANCE), MARS_DISTANCE, 10, (200, 280)),
    solarObject("Jupiter", (100, 100, 100), convert_to_display_distance(
        JUPITER_DISTANCE), JUPITER_DISTANCE, 40, (280, 500)),
    solarObject("Saturn", (150, 150, 150), convert_to_display_distance(
        SATURN_DISTANCE), SATURN_DISTANCE, 30, (500, 600)),
    solarObject("Uranus", (255, 255, 255), convert_to_display_distance(
        URANUS_DISTANCE), URANUS_DISTANCE, 24.6, (600, 700)),
    solarObject("Neptune", (100, 100, 255), convert_to_display_distance(
        NEPTUNE_DISTANCE), NEPTUNE_DISTANCE, 20, (700, 800)),
]


paused = False
play = True
clock = pygame.time.Clock()
orbit = True
orbit_width = 1
speed_text = f"X{int(EMULATION_SPEED)} Speed"
LEFT = 1
MIDDLE = 2
RIGHT = 3
planet_name = 1
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.MOUSEMOTION:
            mouse = event.pos
        if event.type == pygame.MOUSEBUTTONUP and paused == False and event.button == RIGHT:
            if(orbit == False):
                orbit = True
            elif(orbit == True):
                orbit = False
        if event.type == pygame.MOUSEBUTTONUP and paused == False and event.button == LEFT:
            mouse = event.pos
            distance_inpx = int(mouse_sun_distance(mouse))
            if(distance_inpx <= 130):
                planets.append(solarObject(str(planet_name), (r.random()*255, r.random()*255, r.random()
                               * 255), 140, convert_to_real_distance(140), r.randrange(7, 50), (130, 150)))
            else:
                planets.append(solarObject(str(planet_name), (r.random()*255, r.random()*255, r.random()*255), int(
                    distance_inpx), convert_to_real_distance(int(distance_inpx)), r.randrange(7, 50), (130, 150)))
            planet_name += 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                if EMULATION_SPEED < 80000000 and paused == False:
                    EMULATION_SPEED = EMULATION_SPEED * 2
                    speed_text = f"X{int(EMULATION_SPEED)} Speed"
            if event.key == pygame.K_DOWN:
                if EMULATION_SPEED > 78125 and paused == False:
                    EMULATION_SPEED = EMULATION_SPEED / 2
                    speed_text = f"X{int(EMULATION_SPEED)} Speed"
            if event.key == pygame.K_ESCAPE and paused == False:
                paused = True
                pause_text = "Paused"
                pause_help1 = "Press c or ESC to Continue"
                pause_help2 = "Press q to Quit"
                font_title = pygame.font.Font('Quicksand.ttf', 115)
                TextSurf, TextRect = text_objects(pause_text, font_title)
                TextSurf1, TextRect1 = text_objects(pause_help1, font)
                TextSurf2, TextRect2 = text_objects(pause_help2, font)
                TextRect.center = ((screenW/2), (screenH/2)-350)
                TextRect1.center = ((screenW/2), (screenH/2)+350)
                TextRect2.center = ((screenW/2), (screenH/2)+400)
                screen.blit(TextSurf, TextRect)
                screen.blit(TextSurf1, TextRect1)
                screen.blit(TextSurf2, TextRect2)
                pygame.display.update()
            elif event.key == pygame.K_c and paused == True:
                paused = False
            elif event.key == pygame.K_ESCAPE and paused == True:
                paused = False
            elif event.key == pygame.K_q and paused == True:
                play = False

    if(not paused):
        screen.blit(bg, (0, 0))
        screen.blit(sunImg, (screenW/2-125, screenH/2-125))
        for planet in planets:
            planet_period = calculate_period(
                planet.realdistance, MASS_OF_THE_SUN)
            planet_radiant_per_frame = radiant_per_frame(planet_period)
            planet.angle = planet.angle + planet_radiant_per_frame
            planet_x = (
                round((planet.distancepx*math.cos(planet.angle)) + sun_x, 2))
            planet_y = (
                round((planet.distancepx*math.sin(planet.angle)) + sun_y, 2))
            sun_orbit_x = sun_x
            sun_orbit_y = sun_y
            if(orbit == True):
                pygame.draw.circle(screen, planet.color, [
                                   sun_orbit_x, sun_orbit_y], planet.distancepx, width=orbit_width)
            pygame.draw.circle(screen, planet.color, [
                               planet_x, planet_y], planet.radius)
            planet_text = planet.name
            PlanetTextSurf, PlanetTextRect = text_objects(planet_text, font)
            PlanetTextRect.center = (planet_x, planet_y-planet.radius-20)
            screen.blit(PlanetTextSurf, PlanetTextRect)
            speedTextSurf, speedTextRect = text_objects(speed_text, font)
            PlanetTextRect.center = (40, 40)
            screen.blit(speedTextSurf, speedTextRect)

    clock.tick(FPS)
    pygame.display.flip()
