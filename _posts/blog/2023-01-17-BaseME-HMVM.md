---
layout: post
title: "Write Up BaseME. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,HMVM,Base64,id_rsa,eJPTv2]
image:
  path: /assets/img/baseme/baseme.png
---

***

<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance

### Ping Sweep

```bash
sudo arp-scan -I ens33 --localnet
```

![list](/assets/img/baseme/1.png){:.lead width="800" height="100" loading="lazy"}

### Nmap

Utilizando **nmap**, comprobamos qué puertos están abiertos.

```bash
nmap --open -p- -Pn -n -T4 -vvv -n 192.168.1.17 -oN allports
```

![list](/assets/img/baseme/2.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions

```bash
nmap -sVC -Pn -n -p22,80 192.168.1.17 -oN target
```

![list](/assets/img/baseme/3.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis 

### HTTP TCP-80

Aunque tenemos dos puerto en el pueto 22 no podemos hace nada de momento, asi que nos vamos a concentrar en el puerto 80, si usamos herramientas como **whatweb** o **wappalizer**, no coseguiremos nada, pero si haciendo **ctrl+u** vemos una cadena en base64 que vamos a decargarnos o copiar ademas vemos algunas palabras que parecen ser contraseñas. 


![list](/assets/img/jabita/5.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Vemos lo que hay en la pagina Web y las palabras son **iloveyou, youloveyou, shelovesyou, helovesyou, weloveyou, theyhatesme**.


Entonces, aquí tenemos la primera pista **ALL, absolutely ALL that you need is in BASE64.Including the password that you need Remember, BASE64 has the answer to all your questions.-lucas** Parece que el usuario es Lucas y la contraseña podría ser una de las cadenas comentadas en el mismo índice. Vamos a codificarlas en Base64.


![list](/assets/img/baseme/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Decript en base64.


Ya con las las **"credenciales"** y el usuario lucas podemos tataar de con hydra bruteforcear el servicio SSH, pero no tenemos suerte.


![list](/assets/img/baseme/9.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Credenciales en base64.


Por lo que se me ocurre usar Gobuster para fuzzear algun directorio en el servidor para usar esas credenciales, pero nada , ademas probe usar esas credenciales como directorios en el servidor y tampoco tube suerte, por lo que despues de probar algunas cosas probe el encritar todo el diccionaraio **rockyou.txt** pero es mucho asi que mejor el **comom.txt** ,esto por que en nos dijo la nota que todo es en **bsae64** jejeje.


![list](/assets/img/baseme/10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Tenemos dos directorios.


Y tienen dos recurso uno es una nota sin mas y el otro es una cadena en base64.Bien, que bamos a dencriptar en base64.


![list](/assets/img/baseme/13.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Como siempre y ya sabemos esta en base64 porlo que haciendo un `echo 'contenido base64' | base64 -d` nos dara una clave SSH.


![list](/assets/img/baseme/14.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
No olvidarse darle permisos `chmod 600 id_rsa`.


Con credenciales validas i la **id_rsa** nos ya es solo conectarnos pero nos pide la clave de id_rsa y si nos acordamos al pricipio teniamos unas y como todo es en base64 pues eso haremos y la clave es **aWxvdmV5b3UK** la primerita que dificil no? jeje.


![list](/assets/img/baseme/15.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Nos conectamos con  clave SSH al usuario lucas.


![list](/assets/img/baseme/18.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La flag esta en el escritorio del usuario lucas.


***

## Privilege Escalation


Es muy buena practica cuando estamos enpezando a uasr herramientas como **Limpeas.sh** o/y **pspy64**, etc, para realizar un reconocimiento del servidor para ver algun posible vector para escalar privileguios pero siempre antes de eso vamos hacer un **sudo -l** para ver quien esta ejecutando algun programacon con permisos de sudoers, en este caso /usr/bin/base64 .


![list](/assets/img/baseme/16.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Comando **sudo -l**.



![list](/assets/img/baseme/17.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Como cualquiera puede ejecutar el binario y como siempre la flag esta en el escritorio de root.


{:.note title="Attention"}
En el siguiente enlace te dejo el [base64Encriter.py](https://github.com/4xLoff/Python-Scripting/blob/main/baseMeEncript.py) de esta máquina hecho en Python.


***

```bash
🎉 Felicitaciones ya has comprometido BaseME de Hack My VM 🎉
```
{:.centered}

***

Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}
