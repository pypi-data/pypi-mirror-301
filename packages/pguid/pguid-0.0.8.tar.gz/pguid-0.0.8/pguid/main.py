import pygame, requests
pygame.font.init()

class pgUId:
  def __init__(self) -> None:
    pass

  def docs(self):
    url = 'https://raw.githubusercontent.com/datruememe/pguid/main/documentation.txt'
    response = requests.get(url)

    if response.status_code == 200:
      
      with open('documentation.txt', 'w', encoding='utf-8') as f:
        f.write(response.text)
      print('Documentation download successful')  
    else:
      print(f'Failed to download documentation. Status Code: \n{response.status_code:^46}')

  class UIDisplay:
    def __init__(self, scrollable=False, stacked=False, fill="white", x=0, y=0) -> None:
      self.fill = fill
      self.elements = []
      self.scrollable = scrollable
      self.stacked = stacked

      self.scroll_y = 0
      self.old_scroll_y = 0

      self.scroll_bar_size = 0
      self.scroll_bar_y = 0

      self.scroll_bar_background = "#212121"
      self.scroll_bar_color = "#676767"

      self.x, self.y = x, y

    def config(self, bg="#e2e2e2", color="black"):
      self.scroll_bar_background = bg
      self.scroll_bar_color = color

    def clear_elements(self, tag=None):
      if tag is None:
        self.elements = []
      else:
        for element in self.elements:
          if element.tag == tag:
            self.elements.remove(element)
    
    def render(self, screen, screen_width, screen_height):
      pygame.draw.rect(screen, self.fill, pygame.Rect(self.x, self.y, screen_width, screen_height))

      total_elements_height = sum(element.rect.height for element in self.elements)
      visible_height = screen_height

      if total_elements_height > visible_height:
          scroll_ratio = visible_height / total_elements_height
      else:
          scroll_ratio = 1

      self.scroll_bar_size = max(50, int(scroll_ratio * screen_height))

      y_pos = 0
      for element in self.elements:
          if self.scrollable and total_elements_height > visible_height:
              mouse_buttons = pygame.mouse.get_pressed()

              scroll_bar_background = pygame.draw.rect(screen, self.scroll_bar_background, (screen_width - 15, 0, 15, screen_height))

              self.scroll_bar_y = max(0, min(self.scroll_bar_y, screen_height - self.scroll_bar_size))

              scroll_bar = pygame.draw.rect(screen, self.scroll_bar_color, (screen_width - 10, self.scroll_bar_y, 10, self.scroll_bar_size))

              max_scroll = screen_height - self.scroll_bar_size
              self.scroll_y = -(self.scroll_bar_y / max_scroll) * (total_elements_height - visible_height)

              if scroll_bar.collidepoint(pygame.mouse.get_pos()):
                  if mouse_buttons[0]:
                      self.scroll_bar_y = pygame.mouse.get_pos()[1] - (self.scroll_bar_size // 2)

              if scroll_bar_background.collidepoint(pygame.mouse.get_pos()):
                  if mouse_buttons[0]:
                      self.scroll_bar_y = pygame.mouse.get_pos()[1] - (self.scroll_bar_size // 2)

          if self.stacked:
            element.render(screen, x=element.rect.x, y=y_pos, offset_x=self.x, offset_y=self.scroll_y + self.y)

            y_pos += element.rect.height
          else:
            element.render(screen, offset_x=self.x, offset_y=self.y)

  class element:
    def __init__(self) -> None:
      pass

    class ProgressBar:
      def __init__(self, max_value=100, value=0, background_color="grey", filled_color="red", x=0, y=0, tag=None, width=100, height=20):
          self.max_value = max_value
          self.value = value
          self.x, self.y = x, y
          self.tag = tag

          self.width, self.height = width, height

          self.rect = pygame.Rect(x, y, self.max_value, self.height)
          self.rect.center = (x, y)

          self.filled_rect = pygame.Rect(x, y+self.height/3, self.value, self.height/1.5)
          self.filled_rect.center = (x, y)

          self.background_color = background_color
          self.filled_color = filled_color

      def pack(self, gui_display):
          gui_display.elements.append(self)

      def render(self, screen, x=None, y=None, offset_x=0, offset_y=0):
          if x is not None:
              self.rect.x = x + offset_x
          if y is not None:
              self.rect.y = y + offset_y

          pygame.draw.rect(screen, self.background_color, self.rect)

          pygame.draw.rect(screen, self.filled_color, self.filled_rect)

    class Button:
      def __init__(self, function, texture=None, clicked_texture=None, bg=None, hc=None, x=0, y=0, tag=None, text=None, font="Arial", font_size=24, color="black", width=None, height=None) -> None:
          self.texture = texture
          self.clicked_texture = clicked_texture
          
          if texture is not None:
              self.texture = pygame.image.load(texture)
              self.clicked_texture = pygame.image.load(clicked_texture)

              if width is not None and height is not None:
                  self.texture = pygame.transform.scale(self.texture, (width, height))
                  self.clicked_texture = pygame.transform.scale(self.clicked_texture, (width, height))

              self.rect = self.texture.get_rect()

          self.text = text or "" 
          self.font = font
          self.font_size = font_size
          self.color = color
          self.text_surface = self.render_text() 

          if self.text != "":
              if texture is None:
                self.rect = self.text_surface.get_rect()

          self.background_color = bg
          self.hover_color = hc
          self.rect = self.rect if hasattr(self, 'rect') else pygame.Rect(x, y, 0, 0)
          self.rect.center = (x, y)

          self.x = x
          self.y = y
          self.tag = tag
          self.function = function
          self.clicked = False

          self.current_color = self.background_color

      def render_text(self):
          font = pygame.font.SysFont(self.font, self.font_size)
          return font.render(self.text, True, self.color)

      def pack(self, gui_display):
          gui_display.elements.append(self)

      def config(self, texture=None, clicked_texture=None, bg=None, hc=None, tag=None, x=None, y=None, text=None, font=None, font_size=None, color=None, width=None, height=None):
          if texture is not None:
              self.texture = pygame.image.load(texture)
              self.texture = pygame.transform.scale(self.texture, (self.rect.width, self.rect.height))
              self.rect = self.texture.get_rect()

          if clicked_texture is not None:
              self.clicked_texture = pygame.image.load(clicked_texture)
              self.clicked_texture = pygame.transform.scale(self.clicked_texture, (self.rect.width, self.rect.height))

          if text is not None:
              self.text = text
              self.text_surface = self.render_text()

          if font is not None:
              self.font = font
              self.text_surface = self.render_text()

          if font_size is not None:
              self.font_size = font_size
              self.text_surface = self.render_text()

          if color is not None:
              self.color = color
              self.text_surface = self.render_text()

          if bg is not None:
              self.background_color = bg

          if hc is not None:
             self.hover_color = hc

          if x is not None:
              self.x = x
          if y is not None:
              self.y = y
          
          self.rect.center = (self.x, self.y)

          if tag is not None:
              self.tag = tag

      def update_texture(self, texture):
          self.texture = pygame.image.load(texture)

      def check_click(self, offset_x=0, offset_y=0):
        checks = 0
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint((mouse_pos[0] - offset_x, mouse_pos[1] - offset_y)):
          checks += 1

          if self.hover_color is not None:
            self.current_color = self.hover_color
        else:
          if self.hover_color is not None:
            self.current_color = self.background_color

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
          checks += 1

        if checks == 2:
          if not self.clicked:
            if self.texture is not None:
              self.current_texture = self.clicked_texture
            self.clicked = True
            return True
        else:
          if self.texture is not None:
            self.current_texture = self.texture
          self.clicked = False
          return False

      def render(self, screen, x=None, y=None, offset_x=0, offset_y=0):
          if self.check_click(offset_x=offset_x, offset_y=offset_y):
              self.function()

          if x is not None or y is not None:
              if x is not None:
                  self.rect.x = x
              if y is not None:
                  self.rect.y = y
          
          if self.text_surface is not None:
              text_rect = self.text_surface.get_rect(center=self.rect.center)

          if self.background_color is not None:
              pygame.draw.rect(screen, self.current_color, (self.rect.x + offset_x, self.rect.y + offset_y, self.rect.width, self.rect.height))

          if self.texture is not None:
              screen.blit(self.current_texture, (self.rect.x + offset_x, self.rect.y + offset_y))

          if self.text_surface is not None:
              screen.blit(self.text_surface, (text_rect.x + offset_x, text_rect.y + offset_y))

    class Label:
      def __init__(self, text, x=0, y=0, tag=None, font="Arial", font_size=24, color="black") -> None:
        self.x, self.y = x, y

        self.tag = tag
        
        self.font_size = font_size
        self.color = color
        self.font_name = font
        self.font = pygame.font.SysFont(font, self.font_size)
        self.raw_text = text
        self.text = self.font.render(text, True, self.color)
        self.rect = self.text.get_rect()
        self.rect.center = (self.x, self.y)

      def pack(self, gui_display):
        if self in gui_display.elements:
          gui_display.elements.remove(self)
        
        gui_display.elements.append(self)

      def config(self, text=None, font=None, font_size=None, color=None, tag=None, x=None, y=None):
        
        self.font = pygame.font.SysFont(font if font is not None else self.font_name, font_size if font_size is not None else self.font_size)

        self.text = self.font.render(text if text is not None else self.raw_text, True, color if color is not None else self.color)

        if text is not None:
          self.raw_text = text

        if x is not None and y is not None:
          self.x, self.y = x, y
        self.rect = self.text.get_rect()
        self.rect.center = (self.x, self.y)

        if tag is not None:
          self.tag = tag
      
      def update_text(self, text, font=None, font_size=24, color="black"):
        if font is not None:
          self.font = pygame.font.SysFont(font, font_size)
        self.text = self.font.render(text, True, color)
        self.rect = self.text.get_rect()
        self.rect.center = (self.x, self.y)
      
      def render(self, screen, x=None, y=None, offset_x=0, offset_y=0):
        if x is not None or y is not None:
          if x is not None:
            self.rect.x = x
          if y is not None:
            self.rect.y = y

        screen.blit(self.text, (self.rect.x + offset_x, self.rect.y + offset_y))

pgUId = pgUId()
