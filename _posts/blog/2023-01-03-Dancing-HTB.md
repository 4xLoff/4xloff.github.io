---
layout: post
title: "Write Up Dancing. "
subtitle: "Starting-Point "
category: Blog
tags: [Easy,Genin,Linux,HTB,SMB,Network,Protocols,Reconnaissance,Anonymous_Guest-Access,Misconfiguration,eJPTv2] 
image:
  path: /assets/img/dancing/dancing-removebg-preview.png
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
nmap 10.129.131.234
```

![list](/assets/img/dancing/nmap.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions

```bash
nmap -sVC 10.129.131.234
```

![list](/assets/img/dancing/nmap_service.png){:.lead width="800" height="100" loading="lazy"}

***

## Vulnerability Analysis

### SMB TCP-445

Están abiertos los puertos 135, 139 y 445, lo que indica que el servicio **SMB** está activo. Dado que los otros puertos no presentaron vulnerabilidades, nos vamos a centrar en este servicio. Sin embargo, como no tenemos credenciales, vamos a utilizar las credenciales por defecto, es decir, el usuario **guest**.

#### Listar Shares

![list](/assets/img/dancing/smb_tools.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Enumerar recursos compartidos utilizando smbclient y smbmap.


***

## Exploitation

Una vez que hemos enumerado los recursos compartidos, verificamos en cuál tenemos permisos de lectura y escritura. Nos conectamos utilizando smbclient y navegamos a través de los directorios hasta encontrar el archivo **flag.txt**. En este caso, se encuentra en el directorio **James.P**. Utilizando el comando **get flag.txt**, lo descargamos del servidor y ya podemos ver su contenido.

![list](/assets/img/dancing/smb_service.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Nos movemos dentro del servicio SMB y encontramos el archivo flag.txt en la carpeta James.P.


![list](/assets/img/dancing/smb_files.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Utilizando get flag.txt, descargamos el archivo.


![list](/assets/img/dancing/flag.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Una vez que descargamos el archivo, podemos ver su contenido utilizando el comando cat flag.txt.



{:.note title="Attention"}
En el siguiente enlace te dejo el [AutoPwn](https://github.com/4xLoff/Python-Scripting/blob/main/dancingPwn.py) de esta máquina hecho en Python.


***

```bash
🎉 Felicitaciones ya has comprometido Dancing de HackTheBox 🎉
```
{:.centered}

***

Back to [Starting-Point](2023-02-02-Starting-Point.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}