---
layout: post
title: "Write Up Nunchucks. "
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Linux,HTB,PHP,SSTI,RCE,APParmor,Web,Vulnerability-Assessment,Injection,Common-Security-Controls,NodeJS,Web-Site-Structure-Discovery,SUID,Misconfiguration,SSTI,eJPTv2,eWPT] 
image:
  path: /assets/img/nunchucks/Captura%20de%20pantalla%20(273).png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
nmap -p- --open --min-rate 5000-sS -n -vvv -Pn 10.10.11.122 -oA allports
```



![list](/assets/img/nunchucks/A-2022-12-11-11-54-53.png){:.lead width="800" height="100" loading="lazy"}


### Services and Versions


```bash
nmap -p22,80,443 -sV -sC 10.10.11.122 -oN target
```


![list](/assets/img/nunchucks/NUNCHUCKS%20(2).png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis


### HTTP TCP-80


Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros.e ispeccionamos la web, ademas de las tecnologias de la ip ataves de la terminal o via  web esto lo hacemos con wapalizzer o whatweb.


![list](/assets/img/nunchucks/NUNCHUCKS%20(3).png){:.lead width="800" height="100" loading="lazy"}


Nos esta rediriguiendo a un dominio Nunchuks.htb el procedemos a agregarlo al `/etc/hosts` por si acaso se esta haciendo virtual hosting, ademas vemos que el puerto 443 esta abierto y con openssl podemos ver informacion que nos puede dar el certificado autofimado ssl.


![list](/assets/img/nunchucks/A-2022-12-11-12-43-44.png){:.lead width="800" height="100" loading="lazy"}


Como vemos que no encontramos nada en la web lo que podemos es intentar fuzzear por directoriOs o por dominios de la siguiente forma.


```bash
gobuster dir -u http://nunchucks.htb/ -w /usr/share/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 200
```


{:.note}
Enumerar directorios.


```bash
gobuster vhost -u http://nunchucks.htb/b -w /usr/share/SecLists/Discovery/DNS/subdomains-top1million-5000.txt -t 200 
```


{:.note}
Enumerar subdominios.


![list](/assets/img/nunchucks/A-2022-12-11-12-55-58.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
En contramos el subdominio `store.nunchucks.htb` el cual agrgamos al `/etc/host` tambien.


Investigando en internet es un STTI pero de [node.js-stti] que siempre el nombre de la maquina nos puede dar una pista.


[node.js-stti]:(https://disse.cting.org/2016/08/02/2016-08-02-sandbox-break-out-nunjucks-template-engine)


![list](/assets/img/nunchucks/A-2022-12-11-13-40-29.png){:.lead width="800" height="100" loading="lazy"}


Como vemos en la publicacion hay una forma de entablaser una reverse-shell con esa vulnerabilidad, asi que procedemos a levantar un listener a las ecucha en el puerto 443 para conectarnos ala maquina vicima, para esto vamos a usar burpsuite para injectarle el payload en campo vulnerable.


![list](/assets/img/nunchucks/A-2022-12-13-21-36-15.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La flag del usuari de bajos privileguios se encuentra en el escritorio del usuario javi.


***
## Explotation


Siempre es bueno ejecutar `LimEnum` Y `pspy`, para que podamos enumerar más vulnerabilidades que permitan elevar nuestros privilegios al usuario "root", ademas de eso buscando por capabilitis tenemos una que nos permite gestionar el uid y es `/usr/bin/perl`.


Lo primero que se me biene a la mente es usar [Gtobins]para comprobar si el binario de perl permite escalar de privileguios atraves de SUID, pero tiene una capada de seguridad mas ya que esta acoplada a APParmor que esta localizado en `/usr/bin/perl`.


![list](/assets/img/nunchucks/A-2022-12-13-21-40-22.png){:.lead width="800" height="100" loading="lazy"}


[Gtobins]:(https://gtfobins.github.io/gtfobins/knife/#sudo)


Si ispeccionamos el archivos vemos como APParmor nos esta restringuiendo algunos comandos.


![list](/assets/img/nunchucks/A-2022-12-13-21-52-51.png){:.lead width="800" height="100" loading="lazy"}


Hay una vulnerabilidiad [perl-bugs]que lo que permite es editar el shebang que el la primera linea dode se pone la ruta donde reside el lenguaje del script, es debajo de aquello donde vamos a injectar el one-liner que vimos en Gtobins.


![list](/assets/img/nunchucks/A-2022-12-13-22-05-13.png){:.lead width="800" height="100" loading="lazy"}


[perl-bugs]:(https://bugs.launchpad.net/apparmor/+bug/1911431)


Ya podemos, buscar la flag en el escritorio del root.
{:.note}


***

```shell
🎉 Felicitaciones ya has comprometido Nunchucks de HackTheBox 🎉
```
{:.centered}
***

Back to [Certification eJPTv2](2023-07-03-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eWPT](){:.heading.flip-title}
{:.read-more}