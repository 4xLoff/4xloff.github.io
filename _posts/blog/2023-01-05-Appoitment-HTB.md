---
layout: post
title: "Write Up Appoitment. "
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Linux,HTB,Web,Database,Injection,Apache,MariaDB,PHP,SQL,SQLi,Reconnaissance,eJPTv2]  
image:
  path: /assets/img/appoitment/appoitment.png
---

***

<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance

### nmap

Utilizando **nmap**, comprobamos qué puertos están abiertos.

```bash
nmap --open -p- -Pn -n -T4 -vvv -n 10.129.85.254 -oN allports
```

![list](/assets/img/appoitment/nmap.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions

```bash
nmap -sCV -n -p80 10.129.85.254 -oN target
```

![list](/assets/img/appoitment/service.png){:.lead width="800" height="100" loading="lazy"}

***

## Vulnerability Analysis and Exploitation

### HTTP TCP-80

Después de ver que hay un servicio HTTP abierto, es decir, que el servidor tiene una página web, abrimos en el buscador de Google con la dirección IP 10.129.85.254 y vemos que nos muestra un login que nos pide usuario y contraseña, pero no las tenemos. Como hemos estado haciendo, vamos a probar contraseñas por defecto como **admin** o **root** y vamos a utilizar una técnica llamada [inyección SQL].


[inyección SQL]: https://portswigger.net/web-security/sql-injection/cheat-sheet


![list](/assets/img/appoitment/exploit.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La injección funciona porque **admin** es un usuario que existe en el sitema , la  comilla **'** es para romper la estructura de la consulta y la almodilla **#** es para cometar la query.


![list](/assets/img/appoitment/flag.png){:.lead width="800" height="100" loading="lazy"}


{:.note title="Attention"}
En el siguiente enlace te dejo el [AutoPwn](https://github.com/4xLoff/Python-Scripting/blob/main/appoitmentPwn.py) de esta máquina hecho en Python.


***

```bash
🎉 Felicitaciones ya has comprometido Appoitment de HackTheBox 🎉
```
{:.centered}

***

Back to [Starting-Point](2023-02-02-Starting-Point.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}