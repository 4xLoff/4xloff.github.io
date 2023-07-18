---
layout: post
title: "Write Up Haircut. "
subtitle: "Starting-Point"
category: Blog
tags: [Medium,Chunin,ScriptKiddie,Linux,SSRF,eWPT,SSRF,Command-Injection,PHP,NGINX,Web,Vulnerability-Assessment,Injection,Outdated-Software,Reconnaissance,Web-Site-Structure-Discovery,SUID,OS-Command-Injection,eWPT,eC,OSCP] 
---
![list](/assets/img/haircut/Captura%20de%20pantalla%20(289).png){:.lead width="800" height="100" loading="lazy"}

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
nmap -p- --open --min-rate 5000 -n -vvv -Pn 10.10.10.24 -oA allports
```


![list](/assets/img/haircut/Parrot-2022-12-20-11-07-21.png){:.lead width="800" height="100" loading="lazy"}


### Services and Versions


```bash
nmap -p22,80 -sV -sC 10.10.10.24 -oN target
```
![list](/assets/img/haircut/Parrot-2022-12-20-11-09-29.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis


### HTTP TCP-80


Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros.e ispeccionamos la web, ademas de las tecnologias de la ip ataves de la terminal o via  web esto lo hacemos con wapalizzer o whatweb.


![list](/assets/img/haircut/Parrot-2022-12-20-11-18-59.png){:.lead width="800" height="100" loading="lazy"}


Ispeccionando la web no encontramos nada interesante asi que procedemos afuzzear para encontrar direcctorios.


![list](/assets/img/haircut/Parrot-2022-12-20-11-28-01.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Encontramos algunos pero el mas interesante es **exposed.php**.


El archvo exposed esta ejecutando un comandopero si no tenemos experiencia no sabremos que comando es pero si ponesmos nuestra ip y nos ponemos a la escucha en agun puerto con netcat sabremos que comando esta ejecutando.


![list](/assets/img/haircut/Parrot-2022-12-20-11-28-29.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/haircut/Parrot-2022-12-20-11-33-54.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Eta ejecutando curl.


Probando nos damos cuenta que es vulnerable a SSRF por lo que tambien vamos a probar si hay otros puertos abiertos internamente.


![list](/assets/img/haircut/Parrot-2022-12-20-12-03-23.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Esta abierto el 3306  que es de **MySQL**.


Volviendo al **SSRF** lo que vamos hacer con curl que tiene parametros y uno es el `-o` que lo que hace que el output de lo puede "mover a otra ruta"y como vimos que hay una ruta `/var/www/html/uploads` lo que vamos a subir es un cmd.php pafra otogarnos una reverse-shell.


![list](/assets/img/haircut/Parrot-2022-12-20-12-10-46.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La flag del usuaripo de bajos privileguios esta en el escritorio del usuario maria.


***

## Exploitation and Escalation Privileges


Siempre es bueno ejecutar `LimEnum` Y `pspy` para monitorizar y ver los posibles vectores para escalar de privilegios, ademas hasta que se ejecute los anteriores podemos buscar los permisos con el comado find o tareas crond o tareas que esperen ejecucion.


![list](/assets/img/haircut/Parrot-2022-12-20-12-16-53.png){:.lead width="800" height="100" loading="lazy"}


```shell
find \-perm -4000 2>/dev/null
```


{:.note}
Encontramos el binario screen 4.5.6.


Buscamos en searchsploit y encontramos dos una en bash y otra en python vamos a usar el de bash y vamos a segir las intrucciones porque si lo comproamos no va a funcionar.


![list](/assets/img/haircut/Parrot-2022-12-20-12-21-45.png){:.lead width="800" height="100" loading="lazy"}


Al final nos debe de quedar dos archivos un archivo `libhax.so` y un `rootshell.c` los cuales deberemos subir a la mquina victima.


![list](/assets/img/haircut/Parrot-2022-12-20-12-46-21.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Les damos permisos de ejecucion y ejecutamos apartir de `umask 000` de exploit que estamos siguiendo.


![list](/assets/img/haircut/Parrot-2022-12-20-12-49-58.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ya podemos visualizar la flag de root ensu escritorio.


***

```shell
🎉 Felicitaciones ya has comprometido Haircut de HackTheBox 🎉
```
{:.centered}
***

Back to [Certification eWPT](2023-07-04-Road-to-eWPT.md){:.heading.flip-title}
{:.read-more}

***

Back to [Certification eCPPTv2](2023-07-06-Road-to-eCPPTv2.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification OSCP](2023-07-10-Road-to-OSCP.md){:.heading.flip-title}
{:.read-more}