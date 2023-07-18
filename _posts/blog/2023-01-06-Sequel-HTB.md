---
layout: post
title: "Write Up Sequel. "
subtitle: "Starting-Point"
category: Blog
tags:   [Easy,Genin,Linux,HTB,Vulnerability-Assessment,Database,MySQL,PHP,SQL,Weak-Credentials,Reconnaissance,eJPTv2]  
image:
  path: /assets/img/sequel/sequel.png
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
nmap --open -p- -Pn -n -T4 -vvv -n 10.129.13.151 -oN allports
```

![list](/assets/img/sequel/nmap.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions

```bash
nmap -sCV -n -p80 10.129.13.151 -oN target
```

![list](/assets/img/sequel/version.png){:.lead width="800" height="100" loading="lazy"}

***

## Vulnerability Analysis and Exploitation

### MYSQL TCP-3306

El puerto 3306 está abierto y corresponde al servicio de MySQL. Para ingresar, debemos conocer las credenciales, las cuales no tenemos. Sin embargo, podemos probar los usuarios por defecto, como **root** sin contraseña. 


![list](/assets/img/sequel/mysql.png){:.lead width="800" height="100" loading="lazy"}



```bash
SHOW databases;
```


{:.note}
Muestra las bases de datos disponibles.


```bash
USE htb;
```


{:.note}
Selecciona la base de datos especificada para su uso.


```bash
SHOW tables;
```


{:.note}
Muestra las tablas en la base de datos actual.


```bash
DESCRIBE config; 
```


{:.note}
Muestra la estructura de la tabla especificada.


```bash
SELECT * FROM htb.confi;
```


{:.note}
Realiza una consulta seleccionando todos los registros y columnas de la tabla **confi** en la base de datos **htb**.


![list](/assets/img/sequel/flag.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La flag es la respuesta de la consulta.


{:.note title="Attention"}
En el siguiente enlace te dejo el [AutoPwn](https://github.com/4xLoff/Python-Scripting/blob/main/sequelPwn.py) de esta máquina hecho en Python.

***

```bash
🎉 Felicitaciones ya has comprometido Sequel de HackTheBox 🎉
```
{:.centered}

***

Back to [Starting-Point](2023-02-02-Starting-Point.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}