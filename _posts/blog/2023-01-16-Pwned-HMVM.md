---
layout: post
title: "Write Up Pwned. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,HMVM,Fuzzing-Web,FTP,SSH,Brute-Forcing,SUDO,Docker,Reverse-Shell,Groups,Leaked-Information,Password-Recycling,eJPTv2]
image:
  path: /assets/img/pwned/pwned.jpg
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

![list](/assets/img/pwned/1.png){:.lead width="800" height="100" loading="lazy"}

### Nmap

Utilizando **nmap**, comprobamos qué puertos están abiertos.

```bash
nmap --open -p- -Pn -n -T4 -vvv -n 192.168.1.2 -oN allports
```

![list](/assets/img/pwned/2.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions

```bash
nmap -sVC -Pn -n -p21,22,80 192.168.1.2 -oN target
```

![list](/assets/img/pwned/3.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis 

### HTTP TCP-80

Aunque tenemos dos puerto en el pueto 22 no podemos hace nada de momento, asi que nos vamos a concentrar en el puerto 80, si usamos herramientas como **whatweb** o **wappalizer**, no coseguiremos nada solo vemos un mensaje que dice **Pwned**, por lo que si haciendo **ctrl+u** vemos una mensaje de un supuesto hacker jejeje.


![list](/assets/img/pwned/4.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Vemos lo que hay en la pagina Web.


![list](/assets/img/pwned/5.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Mensaje del Hacker.


En este pundo podemos tratar de fuzzear con **Gobuster** pero vemos algunos directorios que vamos a analizar.


![list](/assets/img/pwned/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Directorio a analizar **/hidden_text**.


En **hidden_text** encontramos un listado de directorios que incluye un archivo denominado **secret.dic**.


![list](/assets/img/pwned/7.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Directorio a analizar **/hidden_text**.


![list](/assets/img/pwned/8.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
**secret.dic** es un pequeño diccionario de rutas las parece podemos decargarlo o simplemete copiar y pegar.


Lo siguiente es fuzzerar con **Gobuster** otra ves pero ahora con este diccionario.


![list](/assets/img/pwned/10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Hemos logrado encontrar otra ruta llamada **/pwned.vuln**.


El hacker Vanakam Nanba se burla de nosostros dice que tambien a comprometido el login es un **"PRO"**, Ttambien inspeccionamos la paguna con crtl+u y esta leakeado unas crendeciales del usuario ftpuser y coontraseña `B0ss_B!TcH` que vamos a probar en el servivio ftp.


![list](/assets/img/pwned/11.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Login Hacehedo por Vanakam.


![list](/assets/img/pwned/12.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Credenciales .


### FTP TCP-21

Husmenado dentro del servicio hay dos archivos uno de nota de dice **"Wow you are here ariana won't happy about this note sorry ariana"** y una clave **SSH** que nos decargaremos, pero hay veces que se reutilizan las credenciales y estas mismas las vamos a probar a conectarnos a SSH ya que reutiliza las mismas.

![list](/assets/img/pwned/14.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Descargamos los archivos con `get`.


### SSH TCP-22

Parece indicar que el usuario se llama **ariana** esto nos lo dice la nota, por lo tanto, intentaremos establecer una conexión SSH utilizando la clave privada. Sin embargo, antes de hacerlo, es importante asegurarse de que los permisos de la clave estén configurados correctamente de la siguiente forma `chmod 600 id_rsa`, una vez completado esto, procedemos a conectarnos y realizar un breve tratamiento de [TTY].


[TTY]: https://invertebr4do.github.io/tratamiento-de-tty/#


![list](/assets/img/pwned/13.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Notamos que se resusa la contraseña para el servicio de SSH.


SSh con el usuario **ariana** y la **clave privada**.



![list](/assets/img/pwned/16.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Una ves dentro hacemos tratamiento de TTY, ademas la flag esta en el escritorio.


![list](/assets/img/pwned/17.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La flag.


***

## Privilege Escalation


Es muy buena practica cuando estamos enpezando a uasr herramientas como **Limpeas.sh** o/y **pspy64**, etc, para realizar un reconocimiento del servidor para ver algun posible vector para escalar privileguios pero siempre antes de eso vamos hacer un **sudo -l** para ver quien esta ejecutando algun programacon con permisos de sudoers.


En este caso la usuaria ariana es esta ejecutando el archivo **/home/messenger.sh** que es un programa que tal parece que envia mensajes entre ariana y selena y el cual solo puede ejecutar selena,tambie hay otroa archivo que es el diario de ariana.


```bash
sudo -u selena /home/messenger.sh
```

![list](/assets/img/pwned/19.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ejecutamos el programa como selena.


Haciendo pruebas el campo vulnerable es el de mensaje y podemos ver los archivos de selenala y ademas podemos leerlos pero con el comando `cat /home/selena/*`


![list](/assets/img/pwned/20.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Vemos la flag de selena.


La bandera **flag** de Selena no es útil ni funciona como contraseña, parece que el hacker **Vanakam Nanba** nos han engañado en ese aspecto. Por lo tanto, en esta situación, lo mejor es introducir `bash` para poder obtener una shell como Selena y seguir investigando más a fondo.


![list](/assets/img/pwned/21.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Así que ahora que sabemos que Selena pertenece al grupo **docker**.



Nos vamos [Gtfobins] y buscamos una shell por **docker** de la siguiente forma `docker run -v /:/mnt --rm -it alpine chroot /mnt sh` esto nos dara una shell como root.

[Gtfobins]: https://gtfobins.github.io/gtfobins/docker/#sudo

![list](/assets/img/pwned/22.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La flag esta en el escritorio de root.


***

```bash
🎉 Felicitaciones ya has comprometido Pwned de Hack My VM 🎉
```
{:.centered}

***

Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}
