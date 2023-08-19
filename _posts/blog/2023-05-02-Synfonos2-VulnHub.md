---
layout: post
title: "Write Up Synfonos2. "
subtitle: "eCPPTv2 Track "
category: Blog
tags: [Medium,Chunin,Linux,VulnHub,FTP,LFI,SUDO,Port-Forwarding,Brute-Forcing,Reconnaissance,User-Pivoting,Protocols,Log-Analysis,SAMBA,eCPPTv2]
image:
  path: /assets/img/synfonos2/synfonos2.png
---

***

<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


```bash
sudo arp-scan -I ens33 --localnet
```

![list](/assets/img/synfonos2/1.png){:.lead width="800" height="100" loading="lazy"}


### Nmap


```bash
nmap -p- --open --min-rate 5000 -n -vvv -Pn -sS 192.168.1.57 -oA allports
```


![list](/assets/img/synfonos2/2.png){:.lead width="800" height="100" loading="lazy"}



### Services and Versions


```bash
nmap -sVC -Pn -n -p21,22,25,80,139,445 198.168.1.57 -oN target
```


![list](/assets/img/synfonos2/3.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Expltation


### SAMBA TCP-445


Aunque tenemos el puerto 21 y 80 abiertos, no tenemos usuarios ni informacion para poder tratar de hacer algo asi que vamos a enumerar en servicio de samba para ver si podemos obtener informacion relevante.


```bash
nmap -p445 --script smb-security-mode 192.168.1.53
```


![list](/assets/img/synfonos2/4.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con este script de nmap encontramos un usuario llamado **guest** que es un usuario por defecto con el cual vamos a revisar el servicio de samba y pra ver a que share nos podemos conectary si es asi que informacion podemos obtener.


Con `smbmap -H 192.168.1.53 -u guest` nos conectamos y vemos que podemos leer el share `anonymous`, esto tambien nos lo dijo nmap y dentro de este hay una carpeta llamada `backups` la cual contine un archivo llamado `log.txt`, que por lo que se ve es el log  comando que el usuario a hecho por ejemplo ha echo una copia del `/etc/shadow` y a mirado el contedido del archivo `smb.conf` lo cual es interesante ya que con este en contramos un nombre de usuario ademas que la ruta del samba que es `/home/aeolus/share` lo cual es muy interesante.


![list](/assets/img/synfonos2/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
El share `anonymous` solo es el que se pude ver, ademas dentro ahi un directorio de backups qu contine un archivo de `log.txt` que vamos a descargar.


![list](/assets/img/synfonos2/7.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/synfonos2/8.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Contenido del archivo `log.txt`, de momento no podemos hacer nada pero tenemos otros servicios que podemos explotar o intentarlo.



### FTP TCP-21


Como vimos anteriormente en samba el usuario esta copiando el `/etc/shadow` y lo guarda a una carpeta pero esta versionde **FTP** es la `ProFTP 1.3.5` la cual si buscamos en internet o con serchsploit vemos que es vulnerable a  **mod_copy** por lo cual nos vamos a copiar el `/etc/shadow` igual pero lo vamos a pegar a la ruta `/home/aeolus/share` que se ve que es la que esta sincronizada con el samba segun `smb.conf`.


![list](/assets/img/synfonos2/10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Explotacion del servicio **ProFTP 1.3.5**.


Despues de noc conectamos a FTP, vemos que efectivamente hay una copia del archivo `/etc/shadow.bak` y con `John the Ripper` en contramos que la clave de `aeolus` que  es `sergioteamo` lo cual la usaremos para conectarnos por ssh, pero tambien me olvide de sacar capturas de esto.


![list](/assets/img/synfonos2/9.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Contenido dentro del sevico **FTP**.


![list](/assets/img/synfonos2/12.png){:.lead width="800" height="100" loading="lazy"}


***

## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 


Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.


También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


Enumenrando lo procesos que esta ejecutando el servidor vemos que esta ejecutando skl servicio de apache y con `ss -tuln` vemos que el puerto 8080 ademas que con curl comprobamos que esta un formulario de login en esa web, por lo que ahora vamos hacer un `local port forwarding` para hacer un user pivoting ya que el usuario `cronos` ejecuta el servicio de apache.

![list](/assets/img/synfonos2/13.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Proceso apache que ejecuta cronos.


![list](/assets/img/synfonos2/14.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Puerto 8080 abierto


### User Pivoting

Vamoa hacer el `User Pivoting`, atraves de local port forwarding con el servicio ssh ya que conocemos credenciales validas.

Ya podemos ver que la pagina se trata de `librenms` que hay un exploit del mismo en cual consta en injectar un coamdo que nos conceda una resevse-shell en un formulario vulnerable de la siguiente forma.


![list](/assets/img/synfonos2/15.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Pagina de `librenms`.


![list](/assets/img/synfonos2/16.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Aunque encontramos algunos exploit son inviables asi que lo hcemos de forma manual.


![list](/assets/img/synfonos2/17.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Creamos el payload como dice el script de python.


![list](/assets/img/synfonos2/18.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/synfonos2/19.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/synfonos2/20.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/synfonos2/21.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ejecutamos y nos ponemos a la escucha con netca esto nos debe dar una reverse-shell como el usuario `cronos`.


### User Pivoting


Ya somos el usuario `cronos` y haciendo `sudo -l` nos dice que root puede ejecutar mysql sin proprocionar contraseña.


![list](/assets/img/synfonos2/22.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Buscando en GTFObins en contramos que para escalar privileges con mysql tenemos que ejecutar el siguiente comando `sudo mysql -e '\! /bin/sh'`.


{:.note}
Ya podemos buscar la flag en elescritorio de root.

***

```bash
🎉 Felicitaciones ya has comprometido Synfonos2 de VunlHub 🎉
```
{:.centered}

***

Back to [Certification eCPPTv2](2023-07-06-Road-to-eCPPTv2.md){:.heading.flip-title}
{:.read-more}
