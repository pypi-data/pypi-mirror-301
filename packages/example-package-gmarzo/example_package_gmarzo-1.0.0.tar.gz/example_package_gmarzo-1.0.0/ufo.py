from src.ezshapes.renderer import *

setup(700, 500)

ufox = 350
speed = 5

while True:

  set_background("skyblue")

  # Draw the ground
  rect(0, 300, get_screen_width(), 200, "lightgreen", 20, "darkgreen")

  # Test Beam
  triangle(ufox, 200, ufox-30, 300, ufox+30, 300, "yellow", 2, "darkyellow")

  # Draw the UFO pieces
  ellipse(ufox, 200, 80, 40, "grey50")
  ellipse(ufox, 190, 40, 30, "lightblue")

  #Draw the sun
  circle(get_screen_width(), 0, 75, "yellow", 1, "orange")

  #Singular sun ray
  line(get_screen_width() - 60, 60, get_screen_width() - 100, 100, "yellow", 3)

  # Have the ufo bounce on hitting a wall
  if ufox > get_screen_width() or ufox < 0:
    speed *= -1
  
  ufox += speed

  update_screen()
