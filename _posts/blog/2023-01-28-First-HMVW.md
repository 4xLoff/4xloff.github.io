---
layout: post
title: "Write Up First. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,HMVM,Reverse-Shell,PHP,FTP,SUDO,GTFObins,Weak-Credentials,Reconnaissance,Buffer-Overflow,Ghidra,Steganography,Protocols,Fuzzing-Web,eJPTv2]
image:
  path: /assets/img/first/first.jpg
---

***

<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### Ping Sweep


```bash
sudo arp-scan -I ens33 --localnet
```

![list](/assets/img/first/1.png){:.lead width="800" height="100" loading="lazy"}


### Nmap


```bash
nmap --open -p- -Pn -n -T4 -vvv -n 198.168.1.30 -oN allports
```


![list](/assets/img/first/2.png){:.lead width="800" height="100" loading="lazy"}



### Services and Versions

```bash
nmap -sVC -Pn -n -p21,22,80 198.168.1.30 -oN target
```

![list](/assets/img/first/3.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Expltation


### FTP TCP-21


Como podemos conectarnos como el usuario **anonymous** sin credenciales vamos a ver los archivos pero sin carpetas y pude haber muchas asi que noas vamos hacer una montura para poder movernos mejor, o podemos hacerlo de forma manual, ademas que el el puerto 80 solo hay nota que pone **I Finnaly got apache working, I am tired so I will do the todo list tomorrow. -first**.

```bash
curlftpfs ftp://anonymous:@192.168.1.30 ~/ftp_mount
```

![list](/assets/img/first/5.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con montura.


![list](/assets/img/first/4.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Sin montura.


Sea como sea que lo hagamos nos vamos a descargar todo lo que encontremos, hay una imagen first_logo.jpg y como es una imagen vamos aplicate tecnicas para ver si contiene informacion oculta con exiftool, steghuide, stegseek, binkwalk lo que sea para conseguirlo.


![list](/assets/img/first/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Imagen en FTP.


![list](/assets/img/first/7.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Nada con exiftool.


![list](/assets/img/first/8.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con stegseek en contramos un secret.txt y la palabra cleve es **firstgurl1**.



![list](/assets/img/first/9.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con steghide no pudo estaer secret.txt y usamos  la palabra cleve es **firstgurl1** asi que esperaremos a encontrar algo mas.


![list](/assets/img/first/10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Contenido del first_Logo.jpg.out que quedo   de stegseek.


![list](/assets/img/first/11.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Esta en base64 asi que lo desencriptamos y pone **Hi I had to change the name of the todo list becouse directory busting is too easy theese days also I encoded this in besa64 becouse it is cool btw your todo list is : 2f 74 30 64 30 5f 6c 31 73 74 5f 66 30 72 5f 66 31 72 35 74 do it quick we are vulnarable do the first first** y aparte nos da una cla en hexadecimal.


![list](/assets/img/first/12.png){:.lead width="800" height="100" loading="lazy"}


Con  `echo "2f 74 30 64 30 5f 6c 31 73 74 5f 66 30 72 5f 66 31 72 35 74" | xxd -ps -r` podemos ver el texto **/t0d0_l1st_f0r_f1r5t**, es un diretorio imposible de fuzzear.


![list](/assets/img/first/13.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Paguina web que pone **hazlo rapido** o algo asi.


![list](/assets/img/first/14.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Dice que hay un archivo secreto, asi que vamos a fuzzear.


![list](/assets/img/first/15.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Encontramos el directorio **/uploads**.


![list](/assets/img/first/16.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Formulario de subida de archivos y subimos una php-reverse-shell.php.


![list](/assets/img/first/17.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Nos ponemos a la ecucha con netcat y obtenemos una shell como **www-data** y la flag esta en su escritorio.


***

## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 


Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.


También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


Sudo -l nos dice que el usuario **first** tiene el privilegio de ejecutar el comando **/bin/neofetch**  sin necesidad de proporcionar una contraseña, por ende debemos de convertirnos primero en **first** y como siempre vamos a ver que nos dice GTFOBins.

En resumen, el código crea un archivo temporal único utilizando mktemp, escribe en él una línea que ejecuta la shell **bash -i** y luego utiliza sudo para ejecutar neofetch utilizando el archivo temporal como configuración. La finalidad de este fragmento de código es ejecutar un shell con privilegios de superusuario utilizando neofetch como medio.


![list](/assets/img/first/18.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ese archivo contiene la instrucion **bash -i** y le daremos permiso **655** qu nos dara una shell como **first** interactiva.


![list](/assets/img/first/19.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ejecutamos **sudo -u first neofetch --config /tmp/tmp.archivo**.


Ahira somos first asi que hacemos de nuevo  sudo -l dice, el usuario **first** tiene el privilegio de ejecutar el comando **/bin/secret** como cualquier usuario sin necesidad de proporcionar una contraseña.


![list](/assets/img/first/21.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Al inicio nos dieron una pista solucionar la vulnerabilidad de desbordamiento de búfer en nuestro archivo secreto, y cuando ejecutamos ese archivo binario, solicita una contraseña que desconocemos. Lo que intentaremos es ingresar varios caracteres y ver si podemos "evadir" la verificación, vamos a usar ghidra para hacer reversing a este binario.


Debemos traer este binario a nuestra maquina para hacer la pruebas.


![list](/assets/img/first/2023-06-23_04-45.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Me olvide de sacra la captura pero como es una maquina facil a simple observacion nos damo cuenta que el expacion qeu an determinado para el  input de cararteres es de 10 a 114  y si poneemos de mas,  se acontecce el desboramiento.




![list](/assets/img/first/23.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La flag esta como r00t.txt en el directorio de root.


***

```bash
🎉 Felicitaciones ya has comprometido First de Hack My VM 🎉
```
{:.centered}

***

Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}
