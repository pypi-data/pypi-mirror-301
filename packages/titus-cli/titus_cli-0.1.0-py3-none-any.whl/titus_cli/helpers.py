import re

MAX_HEX_VALUE = 255
HEX_FORMAT = r'^\#?[\dabcdef]{6}$'
RGB_FORMAT = r'^\(?\d{1,3},\s?\d{1,3},\s?\d{1,3}\)?$'

def is_valid_color_input(color_input: str) -> bool:
  valid_hex = is_valid_hex(color_input)
  valid_rgb = is_valid_rgb(color_input)

  return valid_hex or valid_rgb

def is_valid_hex(color: str) -> bool:
  return type(color) is str and re.match(HEX_FORMAT, color)

def is_valid_rgb(color) -> bool:
  valid_rgb_format = re.match(RGB_FORMAT, color)
  
  return valid_rgb_format and all(value <= MAX_HEX_VALUE for value in extract_values(color))

def extract_values(color_input: str):
  values = [int(value) for value in re.findall(r'(\d{1,3})', color_input)]
  return values
  
def new_line(file: str):
  file.write('\n')

def increment_letter(letter: str) -> str:
  return chr(ord(letter) + 1)

def to_rgb(color: str) -> tuple:
  if is_valid_rgb(color):
    return tuple(extract_values(color))
    
  code = color.lstrip('#')  
  return tuple(int(code[i: i + 2], 16) for i in (0, 2, 4))

def to_hex(color) -> str:
  if is_valid_hex(color):
    code = color.lstrip('#')
    return f'#{code}'
  
  if type(color) is str:
    color = extract_values(color)
    
  r, g, b = color
  return "#{:02x}{:02x}{:02x}".format(r,g,b)

def calculate_tint(hex_color: str, percentage:float=0.1 ) -> tuple:
  r, g, b = to_rgb(hex_color)
  tint_r = round(min(MAX_HEX_VALUE, r + (MAX_HEX_VALUE - r) * percentage))
  tint_g = round(min(MAX_HEX_VALUE, g + (MAX_HEX_VALUE - g) * percentage))
  tint_b = round(min(MAX_HEX_VALUE, b + (MAX_HEX_VALUE - b) * percentage))

  return to_hex((tint_r, tint_g, tint_b))

def calculate_shade(hex_color: str, percentage:float=0.1 ) -> tuple:
  r, g, b = to_rgb(hex_color)

  tint_r = round(max(0, r - r * percentage))
  tint_g = round(max(0, g - g * percentage))
  tint_b = round(max(0, b - b * percentage))

  return to_hex((tint_r, tint_g, tint_b))
