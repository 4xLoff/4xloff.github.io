---
layout: post
title: "Write Up Netmon. "
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Windows,FTP,CVE,RCE,Protocols,Weak-Authentication,Information-Leakage,Lateral-Access,Anonymous_Guest-Access,Reconnaissance,Outdated-Software,Metasploit,Network,Vulnerability-Assessment,Reconnaissance,eJPTv2,eWPT,OSCP]
image:
  path: /assets/img/netmon/Captura de pantalla (142).png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
nmap -p- --open --min-rate 5000 -sS -n -vvv -Pn 10.10.10.152 -oA allports
```


![list](/assets/img/netmon/Kali-2022-09-09-15-00-11.png){:.lead width="800" height="100" loading="lazy"}


### Services and Versions


```bash
nmap -p21,135,139,445,5985,47001,49664,49665,49666,49667,49668,49669 -sV -sC 10.10.10.152 -oN target
```


***

## Vulnerability Analysis


### FTP TCP-21


Aunque tenemos muchos puertos abiertos, ninguno de ellos representa una vulnerabilidad excepto el puerto 21 (FTP) y el puerto 80 (Web).


```bash
ftp 10.10.10.52
```

{:.note}
Husmeando por los direcctorios en el escritorio nos encontramos con la flag de **user.txt**.


Enumeramos las tecnologías que utiliza la web con **WhatWeb** o **Wappalyzer**.


![list](/assets/img/netmon/Kali-2022-09-09-15-18-56.png){:.lead width="800" height="100" loading="lazy"}


También, si nos dirigimos a la web, podemos ver que tenemos la capacidad de iniciar sesión, por lo que podemos probar el uso de contraseñas por defecto buscando en Internet.


Si buscamos en Internet por [path traversal windows pressler] o buscamos manualmente en el **FTP**, encontraremos el archivo de configuración de **PRTG** y también la copia de seguridad. Con el comando `wget`, descargamos ambos archivos a la máquina atacante para analizar dichos documentos.


[path traversal windows pressler]: https://gist.github.com/SleepyLctl/823c4d29f834a71ba995238e80eb15f9


```bash
curlftpfs ftp://10.10.10.152 /mnt/montura
```

{:.note}
Esto es para movilizarnos con fluidez por el **FTP**, pero no es necesario.


Para movilizarnos con rapidez por los directorios de FTP, podíamos crear una montura con **Certutils**.


```bash
diff Configuration.old Configuration.old.bak -y | less
```

{:.note}
El parámetro -y es para que en pantalla aparezcan los dos documentos y sea más fácil su análisis. Encontramos un usuario y contraseña que usaremos en la página web para logearnos."


![list](/assets/img/netmon/Kali-2022-09-09-16-20-57.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La credenciales son `User=prtgadmin` y `pass=PrTg@dmin2018`.


![list](/assets/img/netmon/Kali-2022-09-09-16-21-48.png){:.lead width="800" height="100" loading="lazy"}


Si buscamos en internet algún exploit relacionado con **PRTG** o vemos los archivos de la licencia de PRTG, encontramos una ruta a la cual hacen referencia que es `/myaccount.htm?tabid=2`. Si pegamos esta ruta después de la dirección IP y nos logueamos, seremos redirigidos a una sección donde se pueden crear notificaciones.


![list](/assets/img/netmon/Kali-2022-09-09-16-23-12.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/netmon/Kali-2022-09-09-16-37-44.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
En el FTP hay un **código HTML** que podemos decodificar en la terminal o mediante la web [codebeautify].


[codebeautify]: https://codebeautify.org/html-decode-string


***

## Exploitation and Privilege Escalation


Tenemos varias formas de obtener la flag **root.txt** pero vamos a ver tres.


### Primera forma


Es usar el exploit de GitHub el cual nos dice que necesitamos la cookie de sesión, la cual interceptamos con Burp Suite.


![list](/assets/img/netmon/Kali-2022-09-09-17-33-04.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Interceptar la cookie.


![list](/assets/img/netmon/Kali-2022-09-09-17-34-35.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
El exploit lo que hace es que crea o injecta un usuario y pass para el usuario root.


Luego con crackmaapexec nos loogeamos y obtenemos la flag de root.


```bash
crackmaapexec smb 10.10.10.152 -u "pentest" -p "P3nTest!"
```


### Segunda forma


Nos debemos crear una notificación en la cual podemos inyectar un **usuario** y **contraseña** para usar crackmapexec, SSH o una reverse-shell


![list](/assets/img/netmon/Kali-2022-09-09-16-49-48.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Creamos una notificacion llamada **test**.


En la parte más baja, en la sección de **Remote Execution Code**, existe la posibilidad de insertar líneas de comando para realizar lo antes mencionado de la siguiente manera.


```bash
C:\\User\\Public\\Texter; net user test test123 add/ 
```

{:.note}
Ya creado usamos crackmapexec. 


### Tercera forma


Es lo mismo que el paso anterio pero en ves crear **usuario** y **contraseña** copiamos la flags de root al directio FTP.


![list](/assets/img/netmon/Kali-2022-09-09-17-24-33.png){:.lead width="800" height="100" loading="lazy"}


```bash
tester.txt Copy-Item -Path "C:\Users\Administrator\Desktop\root.txt" -Destination "C:\Users\Public\texter.txt" -Recurse
```


{:.note}
Ya seria diriguirse a la ruta donde guardamos el recurso en el FTP. 


***
```bash
🎉 Felicitaciones ya has comprometido Netmon de HackTheBox 🎉
```
{:.centered}
***

Back to [Beginner-Track](2023-06-29-Beginer-Tack.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eJPTv2 ](2023-07-03-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eWPT ](){:.heading.flip-title}
{:.read-more}

***
Back to [Certification OSCP](){:.heading.flip-title}
{:.read-more}

