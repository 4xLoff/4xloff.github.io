---
layout: post
title: "Write Up Blocky. "
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Linux,HTB,SUDO,Web,Vulnerability-Assessment,Common-Applications,Outdated-Software,Authentication,Wordpress,JD-GUI,Java,Site-Structure-Discovery,Password-Reuse,Decompilation,Misconfiguration,Hard-coded-Credentials,eWPT,eJPTv2] 
image:
  path: /assets/img/blocky/Captura%20de%20pantalla%20(287).png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
nmap -p- --open --min-rate 5000 -n -vvv -Pn 10.10.10.37 -oA allports
```


![list](/assets/img/blocky/Parrot-2022-12-20-14-39-23.png){:.lead width="800" height="100" loading="lazy"}


### Services and Versions


```bash
nmap -p80 -sV -sC 10.10.10.37 -oN target
```
![list](/assets/img/blocky/Parrot-2022-12-20-14-42-12.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis   


### HTTP TCP-80


Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros.e ispeccionamos la web, ademas de las tecnologias de la ip ataves de la terminal o via  web esto lo hacemos con **wapalizzer** o **whatweb**, como encontramos version vulnerable del srvicio ftp con serasploit tambien vamos a investigar ese vector.


![list](/assets/img/blocky/Parrot-2022-12-20-14-47-48.png){:.lead width="800" height="100" loading="lazy"}


Whatweb nos  esta aplicando un reirerct al dominio blocky.htb por lo que lo ingresamos al `/etc/hosts`.


![list](/assets/img/blocky/Parrot-2022-12-20-14-44-11.png){:.lead width="800" height="100" loading="lazy"}


Tambien podemos fuzzear los directorioso con nmap antes de usar otros fuzzers mas completos para ver que informacion nos entrega.


![list](/assets/img/blocky/Parrot-2022-12-20-14-52-42.png){:.lead width="800" height="100" loading="lazy"}


Por si cacaso fuzeamos con wfuuzz y nos arrogo lo siguiente.


![list](/assets/img/blocky/Parrot-2022-12-20-15-11-03.png){:.lead width="800" height="100" loading="lazy"}


En el directorio plugins ahi un archivo que se puede descragar que se llama `BlockyCore.jar` el caul nos vamos a decargas y lo investigaremos para ver que tipo de informacion le podemos sacar.


![list](/assets/img/blocky/Parrot-2022-12-20-15-22-10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Logramos opbtener la credenciales para el usuario `notch:8YsqfCTnvxAUeduzjNSXe22`.


Ya solo nos conectamos atraves de SSH.


![list](/assets/img/blocky/Parrot-2022-12-20-15-37-18.png){:.lead width="800" height="100" loading="lazy"}

{:.note}
Ya podemos buscar la flag de bajos privileguios en el escritorip del usuario `notch`. 


***

## Explotation


Siempre es bueno ejecutar `LimEnum` Y `pspy` para monitorizar y ver los posibles vectores para escalar de privilegios, ademas hasta que se ejecute los anteriores podemos buscar los permisos con el comado find o tareas crond o tareas que esperen ejecucion.


Para escalar privileguios yo me percate de dos formas y esta cuando hacemos id estamos en dos grupos vulnerables el [lxd] y el grupo sudo este ultimo es que vamos a explotar , como somos sudo lo que resta es hacer sudo su y la clave `8YsqfCTnvxAUeduzjNSXe22` ya nos convertiriamos en root.


![list](/assets/img/blocky/Parrot-2022-12-20-15-39-45.png){:.lead width="800" height="100" loading="lazy"}


[lxd]:(https://www.exploit-db.com/exploits/46978)


{:.note}
Lo ultimo es buscar la flag de superusuario en el escritorio de root.


***
```shell
🎉 Felicitaciones ya has comprometido Blocky de HackTheBox 🎉
```
{:.centered}
***

Back to [Certification eWPT](2023-07-04-Road-to-eWPT.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eCPTTv2](2023-07-06-Road-to-eCPPTv2.md){:.heading.flip-title}
{:.read-more}