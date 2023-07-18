---
layout: post
title: "Write Up Bashed. "
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Linux,HTB,Mobile,Apache,Web,Common-Applications,Reconnaissance,Web-Site-Structure-Discovery,SUDO,Scheduled-Job-Abuse,OS-Command-Injection,Code-Execution,eJPTv2,eWPT,eCPPTv2] 
image:
  path: /assets/img/bashed/Captura%20de%20pantalla%20(309).png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
nmap -p- --open --min-rate 5000-sS -n -vvv -Pn 10.10.10.68 -oA allports
```


![list](/assets/img/bashed/A-2022-12-22-11-21-27.png){:.lead width="800" height="100" loading="lazy"}


***

### Services and Versions


```bash
nmap -p22,80 -sV -sC 10.10.10.68 -oN target
```
![list](/assets/img/bashed/A-2022-12-22-11-22-23.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis


### HTTP TCP-80


Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros.e ispeccionamos la web, ademas de las tecnologias de la ip ataves de la terminal o via  web esto lo hacemos con wapalizzer o whatweb. 


![list](/assets/img/bashed/A-2022-12-22-11-22-09.png){:.lead width="800" height="100" loading="lazy"}


Si fuzzeamos rapidamente con nmap encontramos algunas rutas.


![list](/assets/img/bashed/A-2022-12-22-11-23-16.png){:.lead width="800" height="100" loading="lazy"}


Claro nos metemos en ruta /dev/y encontramos a un archivo phpbash.php, que lo que hace es que interpreta comados de bash porlo que podemos otorgarnos una reverse-shell.


![list](/assets/img/bashed/A-2022-12-22-11-31-42.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/bashed/A-2022-12-22-11-41-55.png){:.lead width="800" height="100" loading="lazy"}

{:.note}
Debemos estar a la escucha con netcat en el puerto 443 y la flag de bajos privileguios en el la carpeta oculta del usuario `/home/.arrexel`.


***
## Explotation and Escalation Privileges


Siempre es bueno ejecutar `LimEnum` Y `pspy`, para que podamos enumerar más vulnerabilidades que permitan elevar nuestros privilegios al usuario "root".


Hacemos un `sudo -l` y el usuario scriptmanager puede ejecutar cualquier comando.


```shell
sudo -u scriptmanager bash
```


{:.note}
Nos estamos dando una shell con el usuario `scriptmanager`.


En la ruta `/scripts` hay un archivo `test.txt` y `test.py` , lo que hacemos es  borrar todo el contenido de `test.py` y lo remplazamos por lo siguiente:


![list](/assets/img/bashed/A-2022-12-22-11-53-15.png){:.lead width="800" height="100" loading="lazy"}


```shell
import os
os.system("chmod u+s /bin/bash")
```


{:.note}
Y solo esperamos unos segundos ejecutamos el comando `bash -p` y ya somos root y buscamos la flag en su escritorio.


***

```shell
🎉 Felicitaciones ya has comprometido Bashed de HackTheBox 🎉
```
{:.centered}

***
Back to [Certification eJPTv2](2023-07-03-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eWPT](2023-07-04-Road-to-eWPT.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eCPPTv2](2023-07-06-Road-to-eCPPTv2.md){:.heading.flip-title}
{:.read-more}
