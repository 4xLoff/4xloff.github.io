---
layout: post
title: "Write Up Oopsie. "
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Linux,HTB,PHP,Web,Custom-Applications,Session-Handling,BurpSuite,Apache,Reconnaissance,Web-Site-Structure-Discovery,Cookie-Manipulation,SUID,Authentication-Bypass,Clear-Text-Credentials,Arbitrary-File-Upload,IDOR,Path-Hijacking,eJPTv2]
image:
  path: /assets/img/oopsie/oopsie.png
---

***

<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance

### nmap

Utilizando **nmap**, comprobamos qué puertos están abiertos.

```bash
nmap --open -p- -Pn -n -T4 -vvv -n 10.129.193.120 -oN allports
```

![list](/assets/img/oopsie/nmap.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions

```bash
nmap -sVC -Pn -n -p22,80 10.129.193.120 -oN target
```

![list](/assets/img/oopsie/SERVICE.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis 

### HTTP TCP-80

Tenemos dos puertos, el 22 y el 80. Como no podemos hacer nada con el puerto 22, vamos a examinar la página web. Observamos que se trata de un servidor **HTTP server**. Al principio, no encontramos nada relevante y procedemos a realizar un fuzzing en la web. Sin embargo, hasta el momento no hemos encontrado nada.

Un consejo importante es utilizar siempre **Burp Suite** y cargar la web por primera vez, ya que esto permite realizar un mapeo de la web y guardar el historial. Al examinar el historial, encontramos algunas rutas como **/cdn-cgi/**. Con esta ruta en mente, podemos volver a realizar el fuzzing en esa dirección.


![list](/assets/img/oopsie/WAPPA.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Uso de Wappalizer.


![list](/assets/img/oopsie/burp.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Uso de Burpsuite.


Con **Gobuster** otra ves ya aparece derectorios porque ya añadicmos la rita **/cdn-cgi/** y logaramos decubrir rutas adento como **/login/**, **/uploads/**, etc.


![list](/assets/img/oopsie/login.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
No tenemos credenciales pero como vemos podemos usar el usuario **guest**.


Husmeando la pagima web podemos ver que en la URL hay un parametro **id=2** que si vemos es el usuario guest pero si cambiamos a 1 podemos ver que tenemos el id del usuario administrador y con esto vamos a a manipular la cookie atraves de la id de administradodr  para secuestrar su seccion.


![list](/assets/img/oopsie/id.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Identificador de administrador.


***

## Exploitation

Una vez hecho esto y explorando la web, podemos darnos cuenta de que se habilitó una pestaña para la carga de archivos. En esta pestaña, vamos a subir una web shell para enviar una reverse shell. Para lograr esto, debemos estar atentos y escuchar con netcat en el puerto que hayamos determinado.


![list](/assets/img/oopsie/guest.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/oopsie/upload.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Carga de Web Shell.


![list](/assets/img/oopsie/shellup.png){:.lead width="800" height="100" loading="lazy"}


{.note}
Como encontramos con Gobuster el directorio **/uploads/** para ejecutar la Web-shell.


![list](/assets/img/oopsie/whoami.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/oopsie/rshell.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Obtenemos el reverse-shell.


Somos usuario **www-data** y nesesitamos comvertirno en otro usuario para esto podemos usar el binario LimEnum.sh para enumerar el servidor en cuanto a permisos archivo o permisos,etc. 

Husmenado en el directorio que estamos con `cat * | grep -i passw*` ,y podemos obtener unsa credenciales para el usuario admin que es **MEGACORP_4dm1n!!**.

![list](/assets/img/oopsie/robert.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Tambien podemos ver el archivo **/etc/passwd** ya que tenemos permisos de lectura.


![list](/assets/img/oopsie/passwd.png){:.lead width="800" height="100" loading="lazy"}


Lo que podemos intentar es cambiarno de usuario a **robert** con la credenciales obtenidas.


![list](/assets/img/oopsie/failure.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
No funciona la credenciales asi que probaremos otra cosa.


Seguimos husmeando y en el archivo que reside en **/var/www/html/cdn-cgi/login/** vemors el archivo db.php que contine las credenciales robert y la contraseña **M3g4C0rpUs3r!**, ya podemos ver la flag del ussuario rober que esta en el escritorio.


***

## Privilege Escalation

Para la escala de privileguios podemos ver con id el grupo al que pertenece el usuario robert y este pretenece al grupo **bugtracker** y podemos buscar el ninario con el comado **find / -group bugtracker 2/dev/null**.


![list](/assets/img/oopsie/suid.png){:.lead width="800" height="100" loading="lazy"}


La herramienta acepta la entrada del usuario como el nombre del archivo que se leerá utilizando el comando **cat**, sin embargo, no especifica la ruta completa al archivo cat y, por lo tanto, podríamos aprovechar esto que se llama **path hacking**.
Navegaremos al directorio **/tmp** y crearemos un archivo llamado cat con el siguiente contenido:


```bash
/bin/bash 
```

{:.note}
Le damos periso de ejecuion **chmod +x cat**.


Y para hacer que el sistema lea primero la ruta tmp donde creaste el archivo cat usamos **export PATH=/tmp:$PATH**, y debemos ejecutar otra ves bugtracker y ya podemos buscar la flag en el escritorio de **root**.


***

```bash
🎉 Felicitaciones ya has comprometido Oopsie de HackTheBox 🎉
```
{:.centered}

***

Back to [Starting-Point](2023-02-02-Starting-Point.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}