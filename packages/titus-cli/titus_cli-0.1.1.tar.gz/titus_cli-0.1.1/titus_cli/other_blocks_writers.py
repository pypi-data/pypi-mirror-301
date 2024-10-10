from .helpers import new_line

WITH_PREFIX = True
PREFIX = 'TITUS' if WITH_PREFIX else ''

BREAKPOINTS = {
  'xs': { 'value': 480,  'comment': 'Extra small devices (e.g., phones)'},
  's': { 'value': 768,  'comment': 'Small devices (e.g., tablets) '},
  'm': { 'value': 1024, 'comment' : 'Medium devices (e.g., small laptops)'},
  'l': { 'value': 1280, 'comment' : 'Large devices (e.g., laptops and desktops)'},
  'xl': { 'value': 1440, 'comment' : 'Extra large devices (e.g., large desktops)'},
  'xxl': { 'value': 1600, 'comment' : 'Ultra-large devices (e.g., large monitors)'}
}

def borders(file: str, border_radius:int , border_width: int=1):
  file.write('  /* BORDERS ======================================================== */\n\n')
  file.write(f'  --{PREFIX}-br: {border_radius}px;\n')
  file.write(f'  --{PREFIX}-bw: {border_width}px;\n')
  new_line(file)
  
def shadows(file: str):
  file.write('  /* SHADOWS ======================================================== */\n\n')
  file.write(f'  --{PREFIX}-sh-light: 0 1px 2px rgba(0, 0, 0, 0.1);\n')
  file.write(f'  --{PREFIX}-sh-medium: 0 4px 8px rgba(0, 0, 0, 0.15);\n')
  file.write(f'  --{PREFIX}-sh-dark: 0 8px 16px rgba(0, 0, 0, 0.25);\n')
  file.write(f'  --{PREFIX}-sh-inner: inset 0 2px 4px rgba(0, 0, 0, 0.1);\n')
  file.write(f'  --{PREFIX}-sh-outline: 0 0 0 3px rgba(66, 153, 225, 0.6);\n')
  new_line(file)
  
def breakpoints(file: str):
  file.write('  /* BREAKPOINTS ==================================================== */\n\n')
  for size, data in BREAKPOINTS.items(): 
    value = data['value']
    comment = data['comment']
    file.write(f'  --{PREFIX}-break-{size}: {value}px; /* {comment} */\n')
  
  new_line(file)