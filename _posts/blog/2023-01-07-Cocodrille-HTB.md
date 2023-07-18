---
layout: post
title: "Write Up Cocodrille. "
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Linux,HTB,Web,Network,Protocols,Apache,Web-Site-Structure-Discovery,SQLi,Custom-Applications,Clear-Text-Credentials,eJPTv2]  
image:
  path: /assets/img/cocodrile/cocodrile.png
---

***

<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap

```bash
nmap --open -p- -Pn -n -T4 -vvv -n 10.129.103.220 -oN allports
```

![list](/assets/img/cocodrile/nmap.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions

```bash
nmap -sVC -Pn -n -p21,80 10.129.103.220 -oN target
```


![list](/assets/img/cocodrile/service.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Exploitation


### FTP TCP-21

En este puerto está habilitado el usuario **anonymous**, husmeando encontramos un listado de usuarios y contraseñas que descargaremos utilizando el método **GET**.


![list](/assets/img/cocodrile/ftp_files.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Vemos dos archivos uno de usuarios y otro de contraseñas.


![list](/assets/img/cocodrile/user_pass.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Viendo el contenido hay cuatro de cada uno.


### HTTP TCP-80

En el puerto 80 se encuentra una página web. Al revisar más a fondo, no encontramos contenido relevante ni en el código ni en la tecnología verificada con WhaWeb y Wappalizer.

![list](/assets/img/cocodrile/whatweb.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Nada relevante.


![list](/assets/img/cocodrile/wappa.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Lo ewlwvante esque usa **PHP**.


Por lo tanto, procedemos a utilizar la herramienta **Gobuster** para realizar un escaneo de directorios y extensiones. Durante el escaneo, encontramos un archivo llamado **login.php** que contiene un formulario de usuario y contraseña. Dado que tenemos credenciales, vamos a probarlas en este formulario.

![list](/assets/img/cocodrile/panel.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Husmeamos la pagina web.


![list](/assets/img/cocodrile/gobuster.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Encontramos el archivo login.php.


Basándonos en observaciones anteriores, utilizaremos las combinaciones de usuarios **admin** y **root** con diversas contraseñas para realizar las pruebas.


![list](/assets/img/cocodrile/flag.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
El usuario **admin** y la contraseña **rKXM59ESxesUFHAd**.


{:.note title="Attention"}
En el siguiente enlace te dejo el [AutoPwn](https://github.com/4xLoff/Python-Scripting/blob/main/cocodrillePwn.py) de esta máquina hecho en Python.


***

```bash
🎉 Felicitaciones ya has comprometido Cocodrille de HackTheBox 🎉
```
{:.centered}

***

Back to [Starting-Point](2023-02-02-Starting-Point.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}