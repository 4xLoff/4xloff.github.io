---
layout: post
title: "Write Up Shocker. "
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Linux,cgi,Shellshock,GTFOBins,Apache,WebVulnerability-Assessment,Outdated-Software,Security-Tools,Metasploit,Bash,Perl,Reconnaissance,Web-Site-Structure-Discovery,SUDO,RCE,cgi,eJPTv2,eWPT] 
image:
  path: /assets/img/shocker/Captura%20de%20pantalla%20(275).png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
nmap -p- --open --min-rate 5000-sS -n -vvv -Pn 10.10.10.56 -oA allports
```


![list](/assets/img/shocker/A-2022-12-09-11-57-00.png){:.lead width="800" height="100" loading="lazy"}


***

### Services and Versions


```bash
nmap -p80,2222 -sV -sC 10.10.10.56 -oN target
```


![list](/assets/img/shocker/A-2022-12-09-12-04-14.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis


### HTTP TCP-80


Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros.e ispeccionamos la web, ademas de las tecnologias de la ip ataves de la terminal o via  web esto lo hacemos con wapalizzer o whatweb los cuales nos nos revelan informacion relevante como esta expuesto el puerto 80, ispeccionando la web solo vemos una imagen que no contiene metadatos por lo cual prodecemos a fuzzear con wfuzz o gobuster.


![list](/assets/img/shocker/A-2022-12-09-13-24-13.png){:.lead width="800" height="100" loading="lazy"}


En contramos un direcctorio cgi-bin y el cual volveremos a fuzzerar para ver si tiene mas archivos dentro y encontramos un user.sh.


![list](/assets/img/shocker/A-2022-12-09-13-21-55.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ispeccionandola con curl notamos que es un archivo dinamico los datos camnbian.


![list](/assets/img/shocker/A-2022-12-09-13-28-52.png){:.lead width="800" height="100" loading="lazy"}


Hay un script de nmap que podemos utilizar para verificar si es una vulnerabilidad llamada [Shellshock] de la siguiente forma.



```shell
nmap --script http-shellshock --script-arg uri=/cgi-bin/user.sh -p80 10.10.10.56
```


[Shellshock]:(https://blog.cloudflare.com/inside-shellshock/)


{:.note}
Pero aislado a eso tambien nos damos cunta que se trata de shellshock por la carpeta `cgi-bin` que se encarga de ejecutar scrips como `.sh` `.pl` o `cgi-bin`, en paginas web de ahi que usamos nmap para comprobarlo. 


![list](/assets/img/shocker/A-2022-12-09-13-28-52.png){:.lead width="800" height="100" loading="lazy"}


Lo que procede es que usando burpsuite intercectar la comunicacion e injectar en el `User-Agent` encomado malicioso que de pricipio es un `whoami` para probar pero luego injectaremos un comando que nos otrogue una reverse-shell.


![list](/assets/img/shocker/A-2022-12-09-13-32-17.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/shocker/A-2022-12-10-18-25-03.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/shocker/A-2022-12-10-18-27-28.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Debemos estar a la ecucha con netcat en el puerto 443 y ya podemos buscar la flag del usuario de bajos privileguios en el escritorio de `shelly`.


![list](/assets/img/shocker/A-2022-12-10-18-29-27.png){:.lead width="800" height="100" loading="lazy"}

***

## Explotacion and Exploitation Privileges


Siempre es bueno ejecutar `LimEnum` Y `pspy`, para que podamos enumerar más vulnerabilidades que permitan elevar nuestros privilegios al usuario "root".


Si vemos en que grupo esta nuestro usuario esta en [lxd] y si buscamos en searchsploit encontramos, pero esa no es la manera intencionada de resolvr esta maquina, asi que seguiermos husmeando, haciendo `sudo -l` vemos que podemos ejecutar un binario de perl como el usuario root asi que nos diriguimos a [Gtobins] para ver el coamdo. 


```shell
sudo perl -e 'exec "/bin/sh";'
```


![list](/assets/img/shocker/A-2022-12-10-18-36-41.png){:.lead width="800" height="100" loading="lazy"}


[Gtobins]:(https://gtfobins.github.io/gtfobins/perl/#suid)


[lxd]:(https://www.exploit-db.com/exploits/46978)


Ya podemos, buscar la flag en el escritorio del root.
{:.note}


***

```shell
🎉 Felicitaciones ya has comprometido  Shocker de HackTheBox 🎉
```
{:.centered}

***
Back to [Certification eJPTv2](2023-07-03-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}

***

Back to [Certification eWPT](2023-07-04-Road-to-eWPT.md){:.heading.flip-title}
{:.read-more}