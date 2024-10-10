import typer
import os
import requests
from PyInquirer import prompt
from rich import print as rprint

from .css_generators import *
from .color_blocks_writers import to_rgb, to_hex
from .helpers import *

app = typer.Typer()

COLORS_API_URL = 'http://colormind.io/api/'
BORDER_RADIUS = {
  'rounded': 25,
  'standard': 5,
  'square': 0
}
TIMEOUT = 10

@app.command("init")
def init():
    """
    Generates the Titus CSS files in the current folder.
    """
    
    main_color = ''
    while not is_valid_color_input(main_color):
      rprint("[green bold]Enter main color (accepted formats: Hex, RGB):[/green bold]")
      main_color = input()
      
    main_color_rgb = to_rgb(main_color)
    main_color_hex = to_hex(main_color)
    
    # Data for Colormind API
    json_data = {
      "model": "default", # Default model (no special styles of color)
	    "input" : [main_color_rgb,"N","N","N","N"] # Create a palette based on the color provided
    }
    rprint("[green bold]Generating palette...[/green bold]")
    response = requests.post(COLORS_API_URL, json=json_data, timeout=TIMEOUT)
    response_dict = response.json()
    if 'result' in response_dict:
      palette_colors = response_dict['result']
    
    module_list_question  = [
      {
          'type': 'list',
          'name': 'radius',
          'message': 'Select One Border Radius Style: ',
          'choices': [
                      {
                          'name': 'Rounded (Playful, informal, friendly)',
                          'value': BORDER_RADIUS['rounded']
                      },
                      {
                          'name': 'Standard (Neutral, no personality)',
                          'value': BORDER_RADIUS['standard']
                      },
                      {
                          'name': 'Square (Elegant, formal)',
                          'value': BORDER_RADIUS['square']
                      },
                      {
                          'name': 'Other (enter custom border radius)',
                          'value': 'other'
                      }
          ],
      }
    ]
    
    radius_choice = {}
    while 'radius' not in radius_choice:
      radius_choice = prompt(module_list_question)

    radius_input = ''
    if radius_choice['radius'] == 'other':
        while not re.match(r'^[0-9]+$', radius_input):
          rprint("[green bold]Enter your Own Border Radius (in pixels):[/green bold]")
          radius_input = input().strip()
          
        radius = int(radius_input)
    else:
      radius = radius_choice['radius']

    rprint("[green bold]Generating CSS files...[/green bold]")
    
    copy_base_css_files()
    css_file_generator(main_color_hex, palette_colors, radius)
    
    rprint("[green bold]Files generated![/green bold] Enjoy [cyan]Titus![/cyan]")
    
@app.command("help")
def help():
  """
  Displays basic use of the Titus toolkit.
  """
  rprint("[green bold]Enter: [/green bold]")
  rprint("[cyan]titus init[/cyan]")
  rprint("[green bold]to generate the Titus system CSS files[/green bold]")
  rprint("")
  rprint("[green bold]Enter: [/green bold]")
  rprint("[red]titus delete[/red]")
  rprint("[green bold]to delete the Titus system CSS files[/green bold]")
  
@app.command("delete")
def delete():
  """
  Deletes Titus system CSS files
  """
  os.remove('./titus-system.css')
  os.remove('./reset.css')
