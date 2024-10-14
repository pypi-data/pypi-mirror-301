import shutil
import platform

flag = """
█
█ █                               ▓███████▓    ▓████████▓    ▓██████▓     ▓██████▓    ▓████████▓
█ █ █                             ▓█▓    ▓█▓   ▓█▓          ▓█▓    ▓█▓   ▓█▓    ▓█▓   ▓█▓       
█ █ █ █                           ▓█▓    ▓█▓   ▓█▓          ▓█▓    ▓█▓   ▓█▓          ▓█▓       
█ █ █ █ █                         ▓███████▓    ▓██████▓     ▓████████▓   ▓█▓          ▓██████▓  
█ █ █ █ █ █                       ▓█▓          ▓█▓          ▓█▓    ▓█▓   ▓█▓          ▓█▓        
█ █ █ █ █ █ █                     ▓█▓          ▓█▓          ▓█▓    ▓█▓   ▓█▓    ▓█▓   ▓█▓       
█ █ █ █ █ █ █ █                   ▓█▓          ▓████████▓   ▓█▓    ▓█▓    ▓██████▓    ▓████████▓
█ █ █ █ █ █ █ █ █               
█ █ █ █ █ █ █ █ █ █         
█ █ █ █ █ █ █ █ █ █ █             ▓████████▓   ▓██████▓    ▓███████▓                             
█ █ █ █ █ █ █ █ █ █ █ █           ▓█▓         ▓█▓    ▓█▓   ▓█▓    ▓█▓                              
█ █ █ █ █ █ █ █ █ █ █ █ █         ▓█▓         ▓█▓    ▓█▓   ▓█▓    ▓█▓                             
█ █ █ █ █ █ █ █ █ █ █ █ █ █       ▓██████▓    ▓█▓    ▓█▓   ▓███████▓                               
█ █ █ █ █ █ █ █ █ █ █ █ █         ▓█▓         ▓█▓    ▓█▓   ▓█▓    ▓█▓                            
█ █ █ █ █ █ █ █ █ █ █ █           ▓█▓         ▓█▓    ▓█▓   ▓█▓    ▓█▓                            
█ █ █ █ █ █ █ █ █ █ █             ▓█▓          ▓██████▓    ▓█▓    ▓█▓                              
█ █ █ █ █ █ █ █ █ █ 
█ █ █ █ █ █ █ █ █               
█ █ █ █ █ █ █ █                    ▓██████▓     ▓██████▓    ▓████████▓    ▓██████▓               
█ █ █ █ █ █ █                     ▓█▓    ▓█▓   ▓█▓    ▓█▓          ▓█▓   ▓█▓    ▓█▓              
█ █ █ █ █ █                       ▓█▓          ▓█▓    ▓█▓        ▓██▓    ▓█▓    ▓█▓                
█ █ █ █ █                         ▓█▓  ▓███▓   ▓████████▓      ▓██▓      ▓████████▓             
█ █ █ █                           ▓█▓    ▓█▓   ▓█▓    ▓█▓    ▓██▓        ▓█▓    ▓█▓                
█ █ █                             ▓█▓    ▓█▓   ▓█▓    ▓█▓   ▓█▓          ▓█▓    ▓█▓                
█ █                                ▓██████▓    ▓█▓    ▓█▓   ▓████████▓   ▓█▓    ▓█▓ 
█
"""  


message = "yLyeyt'ysyymaykyeyysuyryeyynoyyonyeyyfyorygyeytsyytyhyisyygyeynyoycyiydyey."


def peace():
    """
    # PEACE FOR G.A.Z.A

    ## For what?

    - To remember the catastrophic situation in the M.iddle E.ast 
    - To apply international law, for every countries
    - To find a peace solution, sustainable
    - To judge all crimes about innocent people
    - To counter the lack of transparency and neutrality of the Western media
    - To not stigmatise people: people != government

    ## How can you help?

    - Include in python projects, (requirements and optionally import peace function)
    - Create other project like this
    - Communicate about the situation
    """
    return "P.E.A.C.E F.O.R G.A.Z.A".replace('.', '')


class _colors:
    BG_GREEN = "\x1b[0;30;42m"
    BG_WHITE = "\x1b[0;32;47m"
    BG_BLACK = "\x1b[0;37;40m"
    BG_RED = "\x1b[0;31;31m"
    END_COLOR = '\033[0m'


def _draw_illustration():
    """Dirty code, for dirty situation"""

    lines = flag.split("\n")[1:-1]
    width, height = shutil.get_terminal_size()

    # Small message
    if width <= 64:  
        print(peace())
        return

    # Not colored message
    if platform.system() not in ['Linux', 'Darwin'] or width <= 100:
        for line in lines:
            print(line[34:])
        return
    
    # Draw colored flag
    for i_line, line in enumerate(lines):  
        for i_col in range(100):
            c = " "
            try:
                c = line[i_col]
            except Exception:
                pass
            if c != " " and i_col < 30:
                print(f"{_colors.BG_RED}{c}{_colors.END_COLOR}", end='')
            else:
                if  i_line < 9:
                     print(f"{_colors.BG_BLACK}{c}{_colors.END_COLOR}", end='')
                elif i_line < 18:
                     print(f"{_colors.BG_WHITE}{c}{_colors.END_COLOR}", end='')
                elif i_line < 27:
                     print(f"{_colors.BG_GREEN}{c}{_colors.END_COLOR}", end='')
                
        print() 


def _print_message():
    clear_message = message.replace("yy", " ").replace("y", "")
    print(clear_message, end="\n\n")    



def _main():
    _draw_illustration()
    _print_message()


if __name__ == "__main__":
    _main()

