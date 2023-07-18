---
layout: post
title: "Write Up Arronauth. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,HMVM,Reverse-Shell,PHP,FTP,SUDO,GTFObins,Weak-Credentials,Reconnaissance,Protocols,Brute-Forcing,Directory-Traversalt,Fuzzing-Web,Path-Hijacking,eJPTv2]
image:
  path: \assets\img\arronauth\arronauta.jpg
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

![list](/assets/img/friendly2/1.png){:.lead width="800" height="100" loading="lazy"}


### Nmap


```bash
nmap --open -p- -Pn -n -T4 -vvv -n 198.168.1.39 -oN allports
```


![list](/assets/img/friendly2/2.png){:.lead width="800" height="100" loading="lazy"}



### Services and Versions

```bash
nmap -sVC -Pn -n -p22,80 198.168.1.39 -oN target
```

![list](/assets/img/friendly2/3.1.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Expltation


### HTTP TCP-80

Aunque tenemos algunos puertos en el pueto 22 no podemos hace nada de momento, asi que nos concentraremos en el puerto 80, pero no hay nada asi que vamos a fuzzerar  a ver que encontramos ya que investigando las tecnologuias tampoco obtenemos nada.


![list](/assets/img/friendly2/4.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/friendly2/5.png){:.lead width="800" height="100" loading="lazy"}


{:note}
El directorio **/tools/** es el que me llama la atencion.


Enontramos una web que de primeras no nos dice nada, pero si insapecionamos el codigo vemos una ruta que en suceptible a directory traversal.


![list](/assets/img/friendly2/6.png){:.lead width="800" height="100" loading="lazy"}


{:note}
Web.


![list](/assets/img/friendly2/7.png){:.lead width="800" height="100" loading="lazy"}


{:note}
Ctrl + u, la  ruta es la siguiente `check_if_exist.php?doc=keyboard.html`.


![list](/assets/img/friendly2/8.png){:.lead width="800" height="100" loading="lazy"}


{:note}
Web con la ruta.


![list](/assets/img/friendly2/8.1.png){:.lead width="800" height="100" loading="lazy"}


{:note}
Directory traversal.


Despues de pasr un rato probando algunas rutas en contramos la clave privada del usuario gh0st,esto porque tambien pudimor ver el **/etc/passwd**.


![list](/assets/img/friendly2/9.1.png){:.lead width="800" height="100" loading="lazy"}


{:note}
Contenido de passwd.


![list](/assets/img/friendly2/10.1.png){:.lead width="800" height="100" loading="lazy"}


{:note}
Clave privada de **gh0st**.


Aqui nos encontraremos un perquño obstaculo ya que nos pide una passfrase asi que vamos a usar ssh2john para obtenerla y conectarnos por ssh.


![list](/assets/img/friendly2/12.png){:.lead width="800" height="100" loading="lazy"}


{:note}
Podemos buscar la flag en el escritorio de ghOst.


***

## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 


Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.


También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


![list](/assets/img/friendly2/13.png){:.lead width="800" height="100" loading="lazy"}


Sudo -l nos dice que todo pueden ejecutar el script **/opt/security.sh** sin contraseña, asi que vamos a husmear en el script para ver de que se trata, notamos, el script /opt/security.sh solicita una cadena de texto para codificar y luego realiza algunas validaciones. Si la cadena tiene más de 20 caracteres, muestra un mensaje de error y finaliza. Si la cadena contiene caracteres especiales, también muestra un mensaje de error y finaliza.

Tambien vemos que el script no esta atendiendo a rutas absolutas de grep y por eso nos  aprovecahremos de path hijacking,  y dándole permisos de ejecución.


```bash
sudo PATH=/home/gh0st:$PATH /opt/security.sh
```

![list](/assets/img/friendly2/15.png){:.lead width="800" height="100" loading="lazy"}


{:.note title="Attention"}
Las flag esta el escritorio de root, jejje no es cierto es un troleo otravez como vimos la flag esta codificada no te dire como ya que por lo que sea el creador a dejado asi pero te puedo dar una pista yo utilice linpeas para encontrar la ruta **/...** aunque creo que esta en el directorio pero no le prete atencion utiliza el script **/opt/security.sh**.


***

```bash
🎉 Felicitaciones ya has comprometido Arronauth de Hack My VM 🎉
```
{:.centered}

***

Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}
