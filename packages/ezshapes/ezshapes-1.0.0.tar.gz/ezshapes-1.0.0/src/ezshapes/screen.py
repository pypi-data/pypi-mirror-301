import pygame

pygame.init()

class Screen:
  """
  A wrapper class for the pygame display.

  Attributes:
    - height (int): height of the screen in pixels.
    - width (int): width of the screen in pixels.
    - display (Surface): Created surface from pygame display.
  """
  def __init__(self, height:int, width:int, name:str)->None:
    """
    Initializes a Screen object.

    Parameters:
      - height (int): height of the screen in pixels
      - width (int): width of the screen in pixels
      - name (str): caption at the top of the screen
    """
    self.height = height
    self.width = width
    self.display = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption(name)
  
  def __get_screen__(self)->pygame.Surface:
    """
    Returns the Surface object.
    """
    return self.display

  def get_width(self)->int:
    """
    Returns the width of the screen.
    """
    return self.width

  def get_height(self)->int:
    """
    Returns the height of the screen.
    """
    return self.height
