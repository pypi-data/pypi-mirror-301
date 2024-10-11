import pygame, re, sys
from .screen import Screen
from .colordict import THECOLORS

pygame.init()

def setup(width:int, height:int, name:str="Flying a UFO!")->None:
  """
  Creates the pygame display with the given height and width.
  Can optionally include a name to change the window title.

  Parameters:
    - width (int): The width of the screen in pixels
    - height (int): The height of the screen in pixels
    - name (str): The caption of the window
  
  Returns:
    None
  """
  global display
  global clock
  
  display = Screen(height, width, name)
  clock = pygame.time.Clock()

def update_screen()->None:
  """
  Updates the pygame screen to draw all objects previously made.

  Should be called once per frame and after all objects have been drawn.
  """
  clock.tick(24)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
  pygame.display.update()

def set_background(color:str="grey70")->None:
  """
  Sets the color of the background if the given color is valid.

  Parameters:
    - color (str): the color to change the background to
  
  Returns:
    None
  """
  display.__get_screen__().fill(__is_valid_color__(color))

def rect(left:int, top:int, width:int, height:int, color:str="grey70", bordersize:int=-1, bordercolor:str="black")->None:
  """
  Draws a rectangle on screen, with the top-left corner at a
  given coordinate with the specified width and height.

  Parameters:
    - left (int): The x coordinate of the rectangle's top left corner.
    - top (int): The y coordinate of the rectangle's top left corner.
    - width (int): The width of the rectangle, extending right from the top left corner.
    - height (int): The height of the rectangle, extending down from the top left corner.
    - color (str): The fill color of the rectangle.
    - bordersize (int): Optional. Width of the border around the shape.
    - bordercolor (str): Optional. Color of the border if there is one.
  
  Returns:
    None
  """
  pygame.draw.rect(display.__get_screen__(), __is_valid_color__(color), pygame.Rect(left, top, width, height))
  if bordersize > 0:
    pygame.draw.rect(display.__get_screen__(), __is_valid_color__(bordercolor), pygame.Rect(left, top, width, height), width=bordersize)


def ellipse(centerx:int, centery:int, width:int, height:int, color:str="grey70", bordersize:int=-1, bordercolor:str="black")->None:
  """
  Draws an ellipse on screen at the given coordinates and size.

  Parameters:
    - centerx (int): The x coordinate of the ellipse's center.
    - centery (int): The y coordinate of the ellipse's center.
    - width (int): The width of the ellipse.
    - height (int): The height of the ellipse.
    - color (str): The fill color of the ellipse.
    - bordersize (int): Optional. Width of the border around the shape.
    - bordercolor (str): Optional. Color of the border if there is one.
  
  Returns:
    None
  """
  pygame.draw.ellipse(display.__get_screen__(), __is_valid_color__(color), pygame.Rect(centerx-(width/2), centery-(height/2), width, height))
  if bordersize > 0:
      pygame.draw.ellipse(display.__get_screen__(), __is_valid_color__(bordercolor), pygame.Rect(centerx-(width/2), centery-(height/2), width, height), width=bordersize)

def circle(centerx:int, centery:int, radius:int, color:str="grey70", bordersize:int=-1, bordercolor:str="black")->None:
  """
  Draws a circle at the given coordinates.

  Parameters:
    - centerx: The x coordinate of the circle's center.
    - centery: The y coordinate of the circle's center.
    - radius: The size of the circle.
    - color: The fill color of the circle.
    - bordersize (int): Optional. Width of the border around the shape.
    - bordercolor (str): Optional. Color of the border if there is one.
  
  Returns:
    None
  """
  pygame.draw.circle(display.__get_screen__(), __is_valid_color__(color), (centerx, centery), radius)
  if bordersize > 0:
    pygame.draw.circle(display.__get_screen__(), __is_valid_color__(bordercolor), (centerx, centery), radius, width=bordersize)


def triangle(p1x:int, p1y:int, p2x:int, p2y:int, p3x:int, p3y:int, color:str="grey70", bordersize:int=-1, bordercolor:str="black")->None:
  """
  Draws a triangle between 3 given vertices.

  Parameters:
    - p1x (int): The x coordinate of the first vertex.
    - p1y (int): The y coordinate of the first vertex.
    - p2x (int): The x coordinate of the second vertex.
    - p2y (int): The y coordinate of the second vertex.
    - p3x (int): The x coordinate of the third vertex.
    - p3y (int): The y coordinate of the third vertex.
    - color (str): the fill color of the triangle.
    - bordersize (int): Optional. Width of the border around the shape.
    - bordercolor (str): Optional. Color of the border if there is one.

  Returns:
    None 
  """
  pygame.draw.polygon(display.__get_screen__(), __is_valid_color__(color), [(p1x, p1y),(p2x, p2y),(p3x, p3y)])
  if bordersize > 0:
    # pygame.draw.polygon(display.__get_screen__(), __is_valid_color__(bordercolor), [(p1x, p1y),(p2x, p2y),(p3x, p3y)], width=bordersize)
    pygame.draw.lines(display.__get_screen__(), __is_valid_color__(bordercolor), True, [(p1x, p1y),(p2x, p2y),(p3x, p3y)], width=bordersize)

def line(p1x:int, p1y:int, p2x:int, p2y:int, color:str="grey70", width:int=1)->None:
  """
  Draws a line from one point to another.

  Parameters:
    - p1x (int): The x coordinate of the line start
    - p1y (int): The y coordinate of the line start
    - p2x (int): The x coordinate of the line end
    - p2y (int): The y coordinate of the line end
    - color (str): The color of the line
    - width (int): The width of the line
  
  Returns:
    None
  """
  pygame.draw.line(display.__get_screen__(), __is_valid_color__(color), (p1x, p1y), (p2x, p2y), width)

def get_screen_width()->int:
  """
  Returns the width of the screen given at setup.

  Returns:
    int: the width of the screen in pixels
  """
  return display.get_width()

def get_screen_height()->int:
  """
  Returns the height of the screen given at setup.

  Returns:
    int: the height of the screen in pixels
  """
  return display.get_height()

def __is_valid_color__(color)->str:
  """
  Helper func, checks for a valid color string from the user.

  Accepts either a 6-digit hex color string or
  built in color to pygame.

  Returns the given color if valid, or sets the color as grey70 if not.

  Parameters:
    - color (str): Color string to check.
  
  Returns:
    str: The color that will be displayed.
  """
  valid_color = re.compile("^#[0-9|a-f]{6}$")
  match = re.search(valid_color, color)
  if match or color in THECOLORS:
    return color
  else:
    return "grey70"