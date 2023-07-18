---
layout: post
title: "Write Up Investigation. "
subtitle: "Starting-Point"
category: Blog
tags: [Medium,Chunin,Linux,HTB,Java,Wordpress,SUDO,eWPT,eJPTv2] 
image:
  path: /assets/img/investigation/Captura%20de%20pantalla%20(327).png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance

F
### nmap


```bash
nmap -p- --open --min-rate 5000 -n -vvv -Pn 10.10.11.119 -oA allports
```


![list](/assets/img/blocky/Parrot-2022-12-20-14-39-23.png){:.lead width="800" height="100" loading="lazy"}


***

### Services and Versions


```bash
nmap -p22,80,443 -sV -sC 10.10.11.119 -oN target
```
![list](/assets/img/blocky/Parrot-2022-12-20-14-42-12.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis


### HTTP TCP-80


Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros.e ispeccionamos la web, ademas de las tecnologias de la ip ataves de la terminal o via  web esto lo hacemos con wapalizzer o whatweb.


aqui


Whatweb nos  esta aplicando un reirerct al dominio `broscience.htb` por lo que lo ingresamos al `/etc/hosts`.


aqui


Tambien podemos fuzzear los directorioso con nmap antes de usar otros fuzzers mas completos para ver que informacion nos entrega.


aqui


Por si cacaso fuzeamos con wfuuzz y nos arrogo lo siguiente.


aqui


En el directorio /includes hay un archivo img.php que se hace un poco raro, tratamos de abrirlo pero nos pide un argumento.


![list](/assets/img/blocky/Parrot-2022-12-20-15-22-10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Logramos opbtener la credenciales para el usuario `notch:8YsqfCTnvxAUeduzjNSXe22`.


Abrimos el burpsuite y probamos LFI y lo urlencode dos veces y podemos ver el /etc/passwd y encontramos los usuarios bill y postgres


![list](/assets/img/blocky/Parrot-2022-12-20-15-37-18.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ya podemos buscar la flag de bajos privileguios en el escritorip del usuario `notch`. 


***

## Explotation and Escalation Privileges


Siempre es bueno ejecutar `LimEnum` Y `pspy` para monitorizar y ver los posibles vectores para escalar de privilegios, ademas hasta que se ejecute los anteriores podemos buscar los permisos con el comado find o tareas crond o tareas que esperen ejecucion.


Para escalar privileguios yo me percate de dos formas y esta cuando hacemos id estamos en dos grupos vulnerables el [lxd] y el grupo sudo este ultimo es que vamos a explotar , como somos sudo lo que resta es hacer sudo su y la clave `8YsqfCTnvxAUeduzjNSXe22` ya nos convertiriamos en root.


![list](/assets/img/blocky/Parrot-2022-12-20-15-39-45.png){:.lead width="800" height="100" loading="lazy"}


[lxd]:(https://www.exploit-db.com/exploits/46978)


{:.note}
Lo ultimo es buscar la flag de superusuario en el escritorio de root.

***

```shell
🎉 Felicitaciones ya has comprometido Investigation de HackTheBox 🎉
```
{:.centered}
***

Back to [Certification eJPTv2](2023-07-03-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eWPT](){:.heading.flip-title}
{:.read-more}