import sys
import subprocess
import argparse

from main_loop import main, NAME_PROJECT

def new_console_run():
    # Reconstruimos la lista de argumentos excluyendo el -nc/--new-console
    new_args = [arg for arg in sys.argv[1:] if arg not in ('-nc', '--new-console')]

    # Ejecutamos el script en una nueva consola
    if sys.platform == "win32":
        # Comando para ejecutar en una nueva consola en Windows
        subprocess.Popen(['start', 'cmd', '/k', 'python', sys.argv[0]] + new_args, shell=True)
    else:
        # Comando para ejecutar en una nueva consola en Unix
        subprocess.Popen(['x-terminal-emulator', '-e', 'python3'] + [sys.argv[0]] + new_args)

### --- EJECUCIÓN PARAMETRIZADA --- ###
if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False,
                                     argument_default=argparse.SUPPRESS,
                                     description=f"Ejecución parametrica de {NAME_PROJECT}")
    
    parser.add_argument('-h', '--help',
                        default=False, action='help',
                        help='Muestra en consola información de los parametros de ejecución (No ejecuta el programa)')
    
    parser.add_argument('-ve','--verb-events',
                        default=False, action='store_true',
                        help='Muestra en consola los eventos manejados por el modulo PyGame')
    
    parser.add_argument('-vi','--verb-info',
                        default=False, action='store_true',
                        help='Muestra en consola información respecto a la ejecución')
    
    parser.add_argument('-nc','--new-console',
                        default=False, action='store_true',
                        help='Ejecuta sobre una nueva consola')

    args = parser.parse_args()

    ### Ejecuta bajo los parametros entregados
    if args.new_console: new_console_run()
    else: main(args)