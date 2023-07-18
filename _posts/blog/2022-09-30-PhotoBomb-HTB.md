---
layout: post
title: "Write Up PhotoBomb. "
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Linux,HTB,Java,Web,RCE,SUDO,Hijacking,Web,Vulnerability-Assessment,Injection,Custom-Applications,NGINX,Python,Bash,Reconnaissance,SUDO,OS-Command-Injection,eWPT,OSCP]
image:
  path: /assets/img/photobomb/Captura%20de%20pantalla%20(384).png
---

---

<!--more-->

1. this ordered seed list will be replaced by the toc
   {:toc}

---

## Reconnaissance


### nmap


```bash
nmap -p- --open --min-rate 5000-sS -n -vvv -Pn 10.10.11.182 -oA allports
```


### Services and Versions


```bash
nmap -p22,80 -sV -sC 10.10.11.182 -oN target
```

![list](/assets/img/photobomb/Kali-2022-10-11-08-25-35.png){:.lead width="800" height="100" loading="lazy"}


---

## Analisis de vulnerabilidades


### HTTP TCP-80


Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros e ispeccionamos la web, ademas de las tecnologias de la ip ataves de la terminal o via web esto lo hacemos con wapalizzer o whatweb el cual nos redirigue aun subdominio `photobomb.htb` y o guardamos al archivo `/etc/hosts`.


Husmenado la web no encontramos que podemos autenticarnos pero no tenemos credenciales de momento pero si vemos el codigo fuente.


![list](/assets/img/photobomb/Kali-2022-10-11-08-26-37.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
En photobomb.js hay unas credenciales.


![list](/assets/img/photobomb/Kali-2022-10-11-08-29-36.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Las credenciales son `http://pH0t0:b0Mb!@photobomb.htb/printer`.


Una ves auntenticados encontramos multiples fotos y al final podemos descargarnos una imagen, pero vamos a intercetar esa peticion con bursuite para ver logramos obtener y despues de muchas pruevas el campo injectable es el de filetype en el cual vamos a colarle un comado para mandarnos una reverse-shell.


![list](/assets/img/photobomb/Kali-2022-10-11-09-07-25.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Web de rezise de fotos.


![list](/assets/img/photobomb/Kali-2022-10-11-09-14-06.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Debemos estar a la escucha con netcat en el puerto 443 y la flag del usuaripo de bajos privileguios esta en el escritorio de `wizard`.


---

## Explotacion and Escalation Privileges


Siempre es bueno ejecutar `LimEnum` Y `pspy`, para que podamos enumerar más vulnerabilidades que permitan elevar nuestros privilegios al usuario "root", por lo que deberemos convertirnos en el usuario deploy para poder ejecutar ese binario.


Al hacer sudo -l podemos ver que podemos ejecutar un script como elusuario root `/opt/cleanup.sh`.


![list](/assets/img/photobomb/Kali-2022-10-11-09-43-26.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Privileguio sudoer.


![list](/assets/img/photobomb/Kali-2022-10-11-09-53-55.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Husmeando en el script podemos ver que usa find de forma relativa y no la ruta absoluta por lo cual podemos aprovecharnos de la vulnerabilidad `Hijacking`.


Enel direcctorip `/home/wizard/photobomb` crtearemos unarchivo llamado `find` al cual daremos permisos de ejecucion `chmod +x find` y en su interios injectaremos un comado que nos de una shell `echo bash`.


Para luego cambiara las variables como el path de la siguiente forma `sudo PATH=$PWD:$PATH /opt/cleanup.sh` para que nos tome un comando de find personalizado, y bajo el contexto de sudo nuestro find se ejecutará como root.


![list](/assets/img/photobomb/Kali-2022-10-11-09-56-26.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ya podemos, buscar la flag en el escritorio del root.


---

```shell
🎉 Felicitaciones ya has comprometido Photobomb. de HackTheBox 🎉
```

{:.centered}

***
Back to [Certification eWPT](){:.heading.flip-title}
{:.read-more}

***
Back to [Certification OSCP](){:.heading.flip-title}
{:.read-more}
