---
layout: post
title: "Write Up UpDown. "
subtitle: "Starting-Point"
category: Blog
tags: [Medium,Chunin,Linux,HTB,Git,Fuzzing-Web,PHP,SUID,RCE,SUDO,Web,Custom-Applications,Apache,Python,Reconnaissance,LFI,Vulnerability-Assessment,Injection,Web-Site-Structure-Discovery,Source-Code-Analysis,Code-Injection,Misconfiguration,OSWE,eWPT,eWPTxv2,OSCP] 
image:
  path: /assets/img/updown/Captura%20de%20pantalla%20(318).png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
nmap -p- --open --min-rate 5000 -n -vvv -Pn 10.10.11.117 -oA allports
```


![list](/assets/img/updown/Kali-2022-09-16-18-26-06.png){:.lead width="800" height="100" loading="lazy"}


***

### Services and Versions


```bash
nmap -p22,80 -sV -sC 10.10.11.117 -oN target
```
![list](/assets/img/updown/Kali-2022-09-16-18-30-34.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis


### HTTP TCP-80


Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros.e ispeccionamos la web, ademas de las tecnologias de la ip ataves de la terminal o via  web esto lo hacemos con wapalizzer o whatweb.


![list](/assets/img/updown/Kali-2022-09-16-18-32-18.png){:.lead width="800" height="100" loading="lazy"}


Tambien vamos a fuzzear para encontrar subdominios y directorios.


![list](/assets/img/updown/Kali-2022-09-16-18-53-41.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Encontramos un directorio /dev/ entre otros.



![list](/assets/img/updown/Kali-2022-09-16-19-05-00.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Si seguimos fuzseando el directorio /dev/ ahi otro /.git/ que vamos a traerlo a nuestra maquina.


Ademas en la pagina web hay un formulario que lo que esta haciendo es un `curl`, esto lo sabemos si le acemos una peticion a nuestra IP y nos ponemos a la ecucha en el puerto 80 con netcat, ademas hay un subdominio siteup.htb que agregaremos al `/etc/hosts`.


Despues de varia pruebas con el campo para ingresar datos esta sanitisado lo que vamos a continuar es el proyecto `git` que tiene la maquina victima y que vamos a recomponer con `gitdumper`.


![list](/assets/img/updown/Kali-2022-09-16-19-27-43.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Estamos compranado con diff dos commits para ver las diferencias y hay una que habia una cabecera llamada `Special-Dev: only4dev`.


Como de la fuzzeada de antes en contramos el dominio `dev.siteup.htb` que tambien agreagamos al `/etc/hosts` vamos a husmear alli para ver informacion obtenemos.


![list](/assets/img/updown/Kali-2022-09-16-20-06-22.png){:.lead width="800" height="100" loading="lazy"}


Pero para que funcione debemos interceptar con burpsuite y a la pagina `dev.siteup.htb`, le injectamos ala cabecera `Special-Dev: only4dev` y recargamos lo cual nos mostrara un formulario con la capacidad de cargagar archivos el cual tambien intercetaremos apara hacer prueba de que tipo de archivos y de data esta contemplado para la carga.


![list](/assets/img/updown/Kali-2022-09-16-20-14-39.png){:.lead width="800" height="100" loading="lazy"}


Tenemos deshabilitadas funciones como system o shell_exec, afortunadamente proc_open esta habilitado y hay una forma de crear una reverse shell con [proc_open].


[proc_open]:(https://www.php.net/manual/en/function.proc-open.php)


![list](/assets/img/updown/Kali-2022-09-16-20-30-44.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con esto y estando ala escucha en el puerto 443 con netcat ya somo el usuario www-data.


Ahora debemos pivotear al usuario `developer` y para esto primero vamos a buscar permisos SUID con.


```shell
find / -perm -4000 2>/dev/null
```


{:.note}
En contramos el binario `/home/developer/dev/siteisup`.


Si ejecutamos un autilidad que lo que nos permite es ingrsar una URL pero nosotros nos vamos a aprovechar de la vulnerabilidad  de python2 que un `iput()` tambien hace un `eval()` y con eso en mete a lo que ejecutamos  siteup le vamos a agragar lo siguiente `__import__('os').system('cat /home/developer/.ssh/id_rsa')` lo que nos proporcionara la `id_rsa` del usuario `developer` que usaremos para conectarnos por SSH.


![list](/assets/img/updown/Kali-2022-10-11-08-06-52.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ya podemos buscar la flag de bajos privileguios en el escritorip del usuario `developer`. 


***

## Explotation and Escalation Privileges


Siempre es bueno ejecutar `LimEnum` Y `pspy` para monitorizar y ver los posibles vectores para escalar de privilegios, ademas hasta que se ejecute los anteriores podemos buscar los permisos con el comado find o tareas crond o tareas que esperen ejecucion.


Si hacemos un `sudo -l` vemos que podemos ejecutar `easy_install` como root sin contraseña.


![list](/assets/img/updown/Kali-2022-10-11-08-09-54.png){:.lead width="800" height="100" loading="lazy"}


Como siempre buscamos en [GTObins] una forma de convertirnos en root atraves de esate binario.


![list](/assets/img/updown/Kali-2022-10-11-08-12-44.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Lo ultimo es buscar la flag de superusuario en el escritorio de root.

***

```shell
🎉 Felicitaciones ya has comprometido UpDown. de HackTheBox 🎉
```
{:.centered}
***

Back to [Certification eJPTv2](2023-07-03-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eWPT](){:.heading.flip-title}
{:.read-more}

***
Back to [Certification OSCP](){:.heading.flip-title}
{:.read-more}

