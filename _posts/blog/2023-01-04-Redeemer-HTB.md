---
layout: post
title: "Write Up Redeemer. "
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Linux,HTB,Redis,Database,Network,Protocols,Reconnaissance,Anonymous_Guest-Access,Misconfiguration,eJPTv2]  
image:
  path: /assets/img/redeener/redeemer.png
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
nmap --open -p- -Pn -n -T4 -vvv 10.129.180.205 -oN allports
```

![list](/assets/img/redeener/nmap.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions

```bash
nmap -sVC -p6379 10.129.180.205 -oN target
```

![list](/assets/img/redeener/nmap_service.png){:.lead width="800" height="100" loading="lazy"}

***

## Vulnerability Analysis and Exploitation

### REDIS TCP-6379

El puerto 6379 está abierto, lo que indica que el servicio de **Redis** está en funcionamiento. Dado que los otros puertos no presentaron vulnerabilidades, nos centraremos en este. Sin embargo, como no tenemos credenciales, nos conectaremos sin proporcionar nada.

Utilizamos el comando **info** para ver toda la información del sistema. Al observar que hay cuatro bases de datos, usamos el comando **select 0** para seleccionar la base de datos 0. Para ver todas las claves en esa base de datos, usamos el comando **keys \***. Luego, imprimimos el valor de la clave llamada 'flag' utilizando el comando **get flag**.


![list](/assets/img/redeener/flag.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
View the flag.



{:.note title="Attention"}
En el siguiente enlace te dejo el [AutoPwn](https://github.com/4xLoff/Python-Scripting/blob/main/redeemerPwn.py) de esta máquina hecho en Python.


***

```bash
🎉 Felicitaciones ya has comprometido Redeemer de HackTheBox 🎉
```
{:.centered}

***

Back to [Starting-Point](2023-02-02-Starting-Point.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}
