import pygame, sys, random, math
from pygame.locals import *
from collections import OrderedDict
from copy import deepcopy

pygame.init()
fps_clock = pygame.time.Clock()
random.seed()

window = pygame.display.set_mode((600, 200))
best_window = window.subsurface(pygame.Rect(200, 0, 200, 200))
current_window = window.subsurface(pygame.Rect(400, 0, 200, 200))
pygame.display.set_caption('Your\'e Move Atheists')

#load image
img = pygame.image.load('test.jpg')

solution = []
num_circles = 1024
mutation_probability = 0.0025
mutation_factor = 1
generation = 0
black_and_white = False

class position():
  def __init__(self, x, y):
    self.x = x
    self.y = y

class circle():
  def __init__(self, pos, width, height, colour):
    self.pos = pos
    self.width = width
    self.height = height
    self.colour = colour


  def mutate(self):
    if (random.random() < mutation_probability):
      self.pos.x += random.randint(-200, 200) * mutation_factor
      self.pos.x = int(max(0, min(200, self.pos.x)))

    if (random.random() < mutation_probability):
      self.pos.y += random.randint(-200, 200) * mutation_factor
      self.pos.y = int(max(0, min(200, self.pos.y)))
      
    if (random.random() < mutation_probability):
      self.width += random.randint(-145, 145) * mutation_factor
      self.width = int(max(5, min(150, self.width)))

    if (random.random() < mutation_probability):
      self.height += random.randint(-145, 145) * mutation_factor
      self.height = int(max(5, min(150, self.height)))
    
    if (random.random() < mutation_probability):
      self.colour[0] = int(max(0, min(255, self.colour[0] + random.randint(-255, 255) * mutation_factor)))

    if (random.random() < mutation_probability):
      self.colour[1] = int(max(0, min(255, self.colour[1] +random.randint(-255, 255) * mutation_factor)))

    if (random.random() < mutation_probability):
      self.colour[2] = int(max(0, min(255, self.colour[2] + random.randint(-255, 255) * mutation_factor)))


#initialise
def init():
    for i in xrange(num_circles):
      c = circle(position(random.randint(0, 200), random.randint(0, 200)), random.randint(5, 150), random.randint(5, 150), [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 64])
      solution.append(c)

#fitness as the difference between the images
def get_fitness():
  target = pygame.PixelArray(img)
  current = pygame.PixelArray(current_window)
  error = 0
  #sum the difference of the images
  for i in xrange(len(target)):
    for j in xrange(len(target[0])):
      col_target = Color(target[i, j]) 
      col_current = Color(current[i, j])
      error += abs(col_target.r - col_current.r)
      error += abs(col_target.g - col_current.g)
      error += abs(col_target.b - col_current.b)
  error = (error / ((len(target) * len(target[0])) * 255.0 * 3.0))
  return 1 - error


def render_transparent_circle(color, w, h, width=0):
    temp_surf = pygame.Surface((w, h), SRCALPHA)
    temp_surf.fill(Color(0, 0, 0, 0))
    pygame.draw.ellipse(temp_surf, color, Rect(0, 0, w, h))
    return temp_surf


def mutate_all(sol):
	for s in sol:
		s.mutate()


def draw_current_solution():
  current_window.fill(pygame.Color(0, 0, 0)) #clear the screen
  for s in current_solution:
    if (black_and_white):
      circ = render_transparent_circle(pygame.Color(s.colour[0], s.colour[0], s.colour[0], s.colour[3]), s.width, s.height)
    else:
      circ = render_transparent_circle(pygame.Color(s.colour[0], s.colour[1], s.colour[2], s.colour[3]), s.width, s.height)
    current_window.blit(circ, (s.pos.x, s.pos.y))
  pygame.display.update()


def draw_best_solution():
  best_window.fill(pygame.Color(0, 0, 0)) #clear the screen
  for s in solution:
    if (black_and_white):
      circ = render_transparent_circle(pygame.Color(s.colour[0], s.colour[0], s.colour[0], s.colour[3]), s.width, s.height)
    else:
      circ = render_transparent_circle(pygame.Color(s.colour[0], s.colour[1], s.colour[2], s.colour[3]), s.width, s.height)
    best_window.blit(circ, (s.pos.x, s.pos.y))
  pygame.display.update()

#draw the original image
window.blit(img, (0, 0))

#create an initial random solution
init()
current_solution = solution
draw_best_solution()
draw_current_solution()
fitness = get_fitness()

#rendering loop
while True:
  #draw the original image
  window.blit(img, (0, 0))
  
  #clone solution
  current_solution = deepcopy(solution)

  #mutate
  mutate_all(current_solution)
  draw_current_solution()

  #get child's fitness
  current_fitness = get_fitness()

  #keep the best solution
  if current_fitness > fitness:
    fitness = current_fitness
    solution = deepcopy(current_solution)
    draw_best_solution()

  #print the generation and the current fitness
  generation += 1
  print "Generation: ", generation, " Fitness: ", fitness

  #event handling
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()

    if event.type == KEYDOWN:
      if event.key == K_SPACE:
        pygame.image.save(window, "image.jpg")
      elif event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
