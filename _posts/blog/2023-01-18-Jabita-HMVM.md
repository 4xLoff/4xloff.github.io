---
layout: post
title: "Write Up Jabita. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,HMVM,Fuzzing-Web,SSH,Brute-Forcing,SUDO,Directory-traversal,Python-library-hijacking,eJPTv2]
image:
  path: /assets/img/jabita/jabita.jpg
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

![list](/assets/img/jabita/1.png){:.lead width="800" height="100" loading="lazy"}


### Nmap


```bash
nmap --open -p- -Pn -n -T4 -vvv -n 192.168.1.36 -oN allports
```


![list](/assets/img/pwned/2.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions

```bash
nmap -sVC -Pn -n -p22,80 192.168.1.36 -oN target
```

![list](/assets/img/jabita/3.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis 


### HTTP TCP-80


Aunque tenemos dos puerto en el pueto 22 no podemos hace nada de momento, asi que nos vamos a concentrar en el puerto 80, si usamos herramientas como **whatweb** o **wappalizer**, no coseguiremos nada solo vemos un mesale que dice **We're building our future.**, por lo que si haciendo **ctrl+u** vemos una mensaje de un supuesto hacker jejeje.


![list](/assets/img/jabita/4.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Vemos lo que hay en la pagina Web.


En este pundo podemos tratar de fuzzear con **Gobuster** pero vemos algunos directorios que vamos a analizar.


![list](/assets/img/jabita/5.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Directorio a analizar **/building**.


En el contenido de las páginas no encontramos nada de interés, pero si prestamos atención a la URL, parece que podemos intentar una vulnerabilidad llamada **Directory traversal**, hemos tenido éxito, por lo que guardaremos el contenido de **/etc/shadow** y **/etc/passwd** y los guardaremos en shadow.txt hay dos usuarios jack y jaba, y los hash los vamos a crakear con **john**.


![list](/assets/img/jabita/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Contenido del **/etc/shadow**.


![list](/assets/img/jabita/7.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Usuarios **jack** y **jaba**.


![list](/assets/img/jabita/8.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Contenido del **/etc/passwd**.



![list](/assets/img/jabita/9.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La contraseña de jack es **joanninha** que vamos a usar para conectarnos por SSH.


***

## Privilege Escalation


Es muy buena practica cuando estamos enpezando a uasr herramientas como **Limpeas.sh** o/y **pspy64**, etc, para realizar un reconocimiento del servidor para ver algun posible vector para escalar privileguios pero siempre antes de eso vamos hacer un **sudo -l** para ver quien esta ejecutando algun programacon con permisos de sudoers.


![list](/assets/img/jabita/10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Binario AWK.


En este caso la usuario jaba es esta ejecutando el binario **/usr/bin/awk** que vamos a consultar en [Gtfobins] si hay una posible explotacion para hacer lo que se llama como **Pivoting user**.


[Gtfobins](https://gtfobins.github.io/gtfobins/awk/#sudo)


```bash
sudo -u jaba /usr/bin/awk 'BEGIN {system("/bin/sh")}'
```


![list](/assets/img/jabita/11.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Obtenemos shell como el usuario jaba.


Revisando nuevamente los permisos **SUDO** que tiene java nos damos cuenta que esta ejecutando un archivo `/usr/bin/python3 /usr/bin/clean.py`, carga una biblioteca de Python, esto me da ha  pensar en un ataque llamado **Python library hijacking**, es una técnica de ataque en la que un atacante reemplaza o manipula una biblioteca de Python.


![list](/assets/img/jabita/12.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La libreria se llama **wild**.


Ahora debemos buscar la ubicacion de la libreria para editarla esto lo hacemos con `find / -name "wild*" 2>/dev/null`
/usr/lib/python3.10/wild.py


![list](/assets/img/jabita/13.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La ruta es /usr/lib/python3.10/wild.py.



![list](/assets/img/jabita/14.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Introducimos el comado `os.system("chmod u+s /bin/bash")`.


![list](/assets/img/jabita/15.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La flag esta en el escritorio de root.


***

```bash
🎉 Felicitaciones ya has comprometido Jabita de Hack My VM 🎉
```
{:.centered}

***

Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}
