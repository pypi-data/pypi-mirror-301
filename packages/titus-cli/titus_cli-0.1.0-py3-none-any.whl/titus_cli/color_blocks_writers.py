from .size_blocks_writers import increment_letter
from .helpers import *

WITH_PREFIX = True
PREFIX = 'TITUS' if WITH_PREFIX else ''

def color_samples(file: str, main_color: str, complementary: str, palette_colors: dict):
    file.write('  /* ===> Samples: */\n\n')
    file.write(f'  --TITUS-main-color:          {main_color}; /* Main  Color */\n')
    file.write(f'  --TITUS-complementary-color: {complementary}; /* Complementary  Color */\n')
    for i in range(1, len(palette_colors)):
      accent_color = to_hex(tuple(palette_colors[i]))
      file.write(f'  --TITUS-accent-color-{i}:      {accent_color}; /* Accent Color #{i} */\n')
      
    new_line(file)

def tints_and_shades(file: str, color: str, title: str, variable_code: dict='mc'):
  file.write(f'  /* ===>  {title.capitalize()}  */\n\n')
  
  file.write('  /* Tints  */\n\n')
  generate_tints(file, color, variable_code)
  
  file.write('  /* Base color  */\n\n')
  file.write(f'  --{PREFIX}-{variable_code}base: {color};\n\n')
  
  file.write('  /* Shades  */\n\n')
  generate_shades(file, color, variable_code)

def complementary_color(color: tuple):
    if type(color) is str:
      color = to_rgb(color)

    # Calculate complementary color
    complementary_color = (255 - color[0], 255 - color[1], 255 - color[2])
    return complementary_color

def generate_tints(file: str, hex_color: str, variable_code: str):
  percentage = 0.9
  letter = 'A'
  for _ in range(9):
    tint = calculate_tint(hex_color, percentage)
    file.write(f'  --{PREFIX}-{variable_code}{letter}: {tint};\n')
    letter = increment_letter(letter)
    percentage -= 0.1
    
  new_line(file)
  
def generate_shades(file: str, hex_color: str, variable_code: str):
  percentage = 0.1
  letter = 'F'
  for _ in range(9):
    tint = calculate_shade(hex_color, percentage)
    file.write(f'  --{PREFIX}-{variable_code}{letter}: {tint};\n')
    letter = increment_letter(letter)
    percentage += 0.1
    
  new_line(file)
