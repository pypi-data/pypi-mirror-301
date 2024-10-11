from src.package_name.functions import *

setup(700, 500)

ufox = 350
speed = 5

while True:

  set_background("skyblue")

  # Draw the ground
  rect(0, 300, get_screen_width(), 200, "lightgreen")

  # Test Beam
  triangle(ufox, 200, ufox-30, 300, ufox+30, 300, "yellow")

  # Draw the UFO pieces
  ellipse(ufox, 200, 80, 40, "grey50")
  ellipse(ufox, 190, 40, 30, "lightblue")

  #Draw the sun
  circle(get_screen_width(), 0, 100, "yellow")

  # Have the ufo bounce on hitting a wall
  if ufox > get_screen_width() or ufox < 0:
    speed *= -1
  
  ufox += speed

  update_screen()
