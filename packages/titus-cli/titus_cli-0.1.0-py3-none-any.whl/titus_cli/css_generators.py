import shutil
import os

from .size_blocks_writers import *
from .color_blocks_writers import *
from .other_blocks_writers import *

def css_file_generator(main_color: str, palette_colors: dict, border_radius: int):
  with open('titus-system.css','w') as file:
    file.write(':root {\n\n')
    
    file.write('  /* GENERAL SIZES =================================================  */\n\n')
    absolute_general_sizes(file)
    relative_general_sizes(file)
    
    file.write('  /* FONTS =========================================================  */\n\n')
    absolute_font_sizes(file)
    relative_font_sizes(file)
    font_weights(file)
    
    file.write('  /* COLORS ========================================================  */\n\n')
    complementary = to_hex(complementary_color(main_color))
    color_samples(file, main_color, complementary, palette_colors)
  
    tints_and_shades(file, main_color, 'main color')
    tints_and_shades(file, complementary, 'complementary color', 'cc')

    for i in range(1, len(palette_colors)):
      color = to_hex(tuple(palette_colors[i]))
      variable_code = f'ac{i}'
      tints_and_shades(file, color, f'accent color #{i}', variable_code)
    
    borders(file, border_radius)
    shadows(file)
    breakpoints(file)
    
    file.write('  /* OTHER VARIABLES ===============================================  */\n\n')
    
    file.write('}\n')

def copy_base_css_files():
  script_path = os.path.abspath(os.path.dirname(__file__))
  shutil.copy(f'{script_path}/css_files/reset.css', './reset.css')
