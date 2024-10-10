from .constants import *
from .helpers import *

DEFAULT_1_REM = 16
WITH_PREFIX = True
PREFIX = 'TITUS' if WITH_PREFIX else ''

def absolute_general_sizes(file: str):
    file.write('  /* ===> General Absolute Sizes  */\n\n')
    letter = 'A'
    for size in GENERAL_SIZE_INCREMENTS:
      file.write(f'  --{PREFIX}-s{letter}: calc(var(--base-general-pixel-size) * {size}px);\n')
      letter = increment_letter(letter)
    new_line(file)
      
def relative_general_sizes(file: str):
    file.write('  /* ===> General Relative Sizes  */\n\n')
    letter = 'A'
    for size in GENERAL_SIZE_INCREMENTS:
      file.write(f'  --{PREFIX}-sr{letter}: calc(1rem * {size});\n')
      letter = increment_letter(letter)
    new_line(file)
      
def absolute_font_sizes(file: str):
    file.write('  /* ===> Absolute Font Sizes  */\n\n')
    letter = 'A'
    for size in ABSOLUTE_FONT_SIZES:
      file.write(f'  --{PREFIX}-f{letter}: {size}px;\n')
      letter = increment_letter(letter)
    new_line(file)
      
def relative_font_sizes(file: str):
    file.write('  /* ===> Relative Font Sizes  */\n')
    file.write("""    
  /* General Relative Values for Fonts, equivalent to the previous values,
     assuming 1rem = 16px 
  */\n\n""")
    letter = 'A'
    for size in GENERAL_SIZE_INCREMENTS:
      default_size = int(DEFAULT_1_REM * float(size))
      file.write(f'  --{PREFIX}-fr{letter}: {size}rem; /* Default = {default_size}px*/  \n')
      letter = increment_letter(letter)
    new_line(file)
    
def font_weights(file: str):
    file.write('  /* ===> Font Weights  */\n')
    file.write("""
  /* fwl => [f]ont[w]eight[l]ight == LIGHT */
  /* fwn => [f]ont[w]eight[n]eutral == NEUTRAL*/
  /* fwb => [f]ont[w]eight[b]old == BOLD */
  /* etc... */\n\n""")
    weight = 100
    for weight_code, comment in FONT_WEIGHT_CODES.items():
      file.write(f'  --{PREFIX}-fw{weight_code}: {weight}; /* {comment} */\n')
      weight += 100
    new_line(file)

# Colors

