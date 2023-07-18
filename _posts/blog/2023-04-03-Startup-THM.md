---
layout: post
title: "Write Up Startup. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,THM,FTP,SSH,PHP,Reverse-Shell,Brute-Forcing,Weak-Credentials,CronJob,Default-Credentials,Misconfiguration,Reconnaissance,Fuzzing-Web,eJPTv2,Wireshark,eWPT]
image:
  path: /assets/img/startup/startup.png
---

***

<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### Nmap


```bash
nmap --open -p- -Pn -n -T4 -vvv -n 10.10.46.168 -oN allports
```


![list](/assets/img/startup/1.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions

```bash
nmap -sVC -Pn -n -p21,22,80 10.10.46.168 -oN target
```

![list](/assets/img/startup/2.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Exploitation


### FTP TCP-21


Aunque tenemos tres puertos, primero vamos a explorar el puerto FTP ya que este habilitado el usuario anonymous, adentro encontramos tres archivos y un directorio /ftp/ que tiene un index.html, descargamos todo para echar un vistazo.


![list](/assets/img/startup/3.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Archivo en FTP.

![list](/assets/img/startup/4.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La imagen es un meme de Amoung us trate de hacer algo con binkwalk, exiftool y nada.


El otro archivo es una notice.txt que pone **Whoever is leaving these damn Among Us memes in this share, it IS NOT FUNNY. People downloading documents from our website will think we are a joke! Now I dont know who it is, but Maya is looking pretty sus.** de aqui podemos sacar el nombre de usuario **maya**, el ultimo archivo es un vinario de logsque no nos dice nada de monento. 


### HTTP TCP-80


Proseguimos con el puerto 80 para ver que hay en la web pero solo hay un mensaje generico, asi que lo que nos queda es fuzzerar.


![list](/assets/img/startup/5.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Paguina Web.


Con esta tecnica logramos encontrar un directorio /files/ y volviendo a fuzzear dentro de este directorio escontramos el directorio /ftp/ por que me hace pensar que esto esta sicronizado con el servicio FTP por lo que ya encontramos nuestro vector de intrusion asi que vamos aprovar eso, vamos a subir un [php-reverse-shell.php].


[php-reverse-shell.php]: https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php


![list](/assets/img/startup/7.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Fuzzing.



![list](/assets/img/startup/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Subimos la shell al servidor en la carpeta ftpcon put.


Una vez echo todo esto lo que debemos hacer es ponesmos ala escucaha con netca y buscar el archivo que subimos en la web esto nos otrogara una reverse shell como el usuario www-data, una ves aki ya es husmear un poco encontrando el archivo recipe.txt que contiene **Someone asked what our main ingredient to our spice soup is today. I figured I can't keep it a secret forever and told him it was ... spoiler**.


Dentro del directorio de incidentes, encontramos un archivo llamado suspicious.pcapng. Descarguamos este archivo en mi computadora y lo abrimos en con Wireshark, pero tambie antes eso podemos tratar de ver que contien el archivo suspicious.pcapng con cat no veremos nada pero con strings suspicious.pcapng si vemos una contraseña **c4ntg3t3n0ughsp1c3**, pero la forma que me gusto mas la otra para parcticar.


### WIRESHARK


Con el archivo suspicious.pcapng en nuetra maquina lo abrimos y buscamos algo que nos ayude, husmeando por aki y por alla en comtramos un loq de los comandoa que ha usado el usuario **lennie** que se ha autenticado a su usuario y con estas contraseñas ya nos podemos comvertir en el usuario lennie.


![list](/assets/img/startup/2023-07-03_12-37.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Husmeamos suspicious.pcapng.


![list](/assets/img/startup/2023-07-03_13-22.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
En contramos la contraseña para lennie.


![list](/assets/img/startup/2023-07-03_13-22.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
En contramos la contraseña para lennie.


![list](/assets/img/startup/10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Obtenemos sehll como lennie atraves de ssh.


![list](/assets/img/startup/11.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Observamos la flag de user.


***

## Escalation Privileges

Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 

Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.

También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


Con pspy y descubrí que **/home/lennie/scripts/planner.sh** se ejecuta como usuario root cada minuto a través de una tarea programada **cronjob**, perontes husmeando en el archivo lo que hace un echo de una variable de entorno y la mete en el archivo **/home/lennie/scripts/startup_list.txt** pero esto no nos intersesa porque asu ves hay otra ruta llamada **/etc/print.sh**. Verifiqué los permisos de este archivo y sí, tenemos permisos para modificarlo.


![list](/assets/img/startup/11.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Tarea cron.


```bash
ls -la /etc/print.sh
```


```bash
cat > /etc/print.sh << EOF
>#!/bin/bash
>chmod u+s /bin/bash
>EOF
```

Esperamos un minuto hasta que se ejecute la tarea y ya podemos hacer bash -p y esto nos dara una shell como rott y ya podremos buscar la flag en su directorio.


***

```bash
🎉 Felicitaciones ya has comprometido Startup de Try Hack My 🎉
```
{:.centered}

***

Back to [Certification eJPTv2](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}

***

Back to [Certification eWPT](){:.heading.flip-title}
{:.read-more}
