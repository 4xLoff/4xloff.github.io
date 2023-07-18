---
layout: post
title: "Write Up RouterSpace. "
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Linux,APK,RCE,Web,Network,Mobile,Injection,Custom-Applications,Reconnaissance,OS-Command-Injection,eWPT] 
image:
  path: /assets/img/routerspace/Captura%20de%20pantalla%20(307).png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
nmap -p- --open --min-rate 5000-sS -n -vvv -Pn 10.10.11.148 -oA allports
```


![list](/assets/img/routerspace/Arch-2022-06-20-15-53-33.png){:.lead width="800" height="100" loading="lazy"}


### Services and Versions


```bash
nmap -p22,80 -sV -sC 10.10.11.148 -oN target
```


***

## Vulnerability Analysis


### HTTP TCP-80


Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros.e ispeccionamos la web, ademas de las tecnologias de la ip ataves de la terminal o via  web esto lo hacemos con wapalizzer o whatweb. 


![list](/assets/img/routerspace/Parrot-SO3-2022-07-09-18-20-28.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/routerspace/Arch-2022-06-20-15-57-40.png){:.lead width="800" height="100" loading="lazy"}


No encontramos nada interesante pero si podemos decargarnos el APK y ahora con el comado apktool d routerspace.apk te va a desglosar la aplicacion y vamos a utlizar `Ambox` que es un emulador de android y vamos a utilizarlo para ejecutar la `routerspace.apk`.


Para instalarlo hacemos lo siguiente.


![list](/assets/img/routerspace/parrot%20base-2022-07-09-21-12-40.png){:.lead width="800" height="100" loading="lazy"}


```bash
snap install --devmode --beta anbox
```

Lo ejecutamos.

```bash
adb install routerspace.apk
```

![list](/assets/img/routerspace/parrot%20base-2022-07-09-22-07-33.png){:.lead width="800" height="100" loading="lazy"}

Intersectamos todo el trafico con Burpsuite y debemos configurar el proxy con el comado `adb shell settings list global http_proxy 10.10.16.14:8001` y en options en el bursuite en proxy listeners le agregamos el `127.0.0.1:8001` ya estaria configurado.


![list](/assets/img/routerspace/Parrot-SO3-2022-07-10-02-59-19.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/routerspace/Parrot-SO3-2022-07-10-03-13-22.png){:.lead width="800" height="100" loading="lazy"}


Al interceptar tambien vemos que nos esta rediriguiendo a `routerspace.htb` porlo que ese dominio lometeremos al /etc/hosts y probando tenemos capacida de ejecutar comandos remotamente desde aqui ya podemos ver la flag del usuario de bajos privileguios injectandole `"ip":"0.0.0.0; cat /home/paul/user.txt"` pero lo que vamos hacer para entrar a la maquina ya que no nos podemos otorgar una reverse-shell es introducir nuestra clave publica de root como `auhtorized_keys`.


![list](/assets/img/routerspace/Parrot-SO3-2022-07-10-03-38-50.png){:.lead width="800" height="100" loading="lazy"}


Nos conectamos por SSH y ya no nos pedira contraseña y la flag de bajos privileguios en el escritorio del usuario `paul`.


![list](/assets/img/routerspace/Parrot-SO3-2022-07-10-04-01-07.png){:.lead width="800" height="100" loading="lazy"}


***

## Explotacion and Escalation Privileges


Siempre es bueno ejecutar `LimEnum` Y `pspy`, para que podamos enumerar más vulnerabilidades que permitan elevar nuestros privilegios al usuario "root".


Despues de probar y enumerar todos lo posibles vectores y buscando por permisos SUID el binario `/usr/bin/sudo` esta desactualizado y tiene un [exploit] el  cual nos vamos a clonar en la maquina atacante , la vamos a a pasar los tres archivos `Makefile`, `exploit.c`, `shellcode.c` como esta implementado reglas iptable lo haremos de la siguiente forma.


![list](/assets/img/routerspace/Parrot-SO3-2022-07-10-04-18-18.png){:.lead width="800" height="100" loading="lazy"}


```shell
cat Makefile | xclip -sel clip
```


{:.note}
Y lo pegamos en un archivo con el mismo nombre en la maquina victima.


```shell
cat exploit.c | xclip -sel clip
```


{:.note}
Y lo pegamos en un archivo con el mismo nombre en la maquina victima.


```shell
cat shellcode.c | xclip -sel clip
```


{:.note}
Y lo pegamos en un archivo con el mismo nombre en la maquina victima.


Ya solo es cuestion de complilar y ejecutar.


[exploit]:(https://github.com/mohinparamasivam/Sudo-1.8.31-Root-Exploit)


![list](/assets/img/routerspace/Parrot-SO3-2022-07-10-04-18-18.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Y con la contraseña de root esta en el ecritorio del mismo.


***

```shell
🎉 Felicitaciones ya has comprometido Goodgames de HackTheBox 🎉
```
{:.centered}
***

Back to [Certification eWPT](){:.heading.flip-title}
{:.read-more}

