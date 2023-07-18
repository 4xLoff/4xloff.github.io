---
layout: post
title: "Write Up Devzat. "
subtitle: "Starting-Point"
category: Blog
tags: [Medium,Chunin,ScriptKiddie,Linux,Git,CVE,RCE,Web,Vulnerability-Assessment,Injection,Session-Handling,Source-Code-Analysis,Outdated-Software,Authentication,JWT,InfluxDB,Devzat-Chat,Go,Reconnaissance,Password-Reuse,Cookie-Manipulation,Chisel,LFI,Weak-Authentication,Information-Disclosure,
Code-Injection,eWPT,eJPTv2] 
image:
  path: /assets/img/devzat/Captura%20de%20pantalla%20(277).png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
nmap -p- --open --min-rate 5000 -n -vvv -Pn 10.10.11.118 -oA allports
```


![list](/assets/img/devzat/A-2022-12-07-19-25-00.png){:.lead width="800" height="100" loading="lazy"}


### Servicios y versiones


```bash
nmap -p22,80 -sV -sC 10.10.11.118 -oN target
```
![list](/assets/img/devzat/A-2022-12-07-19-30-15.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis


### HTTP TCP-80

Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros.e ispeccionamos la web, ademas de las tecnologias de la ip ataves de la terminal o via  web esto lo hacemos con wapalizzer o whatweb.


![list](/assets/img/devzat/A-2022-12-07-19-12-36.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Nos ecncontramos con un dominio `devzat.htb` el cual vamos agregar al `/etc/host`. 


Aislado a eso tenemos dos puertos SSH que estan abiertos uno el 22 y el otro 8000 en los cuales husmearemosun poco pero solo sirven con credenciales validas.


Por lo que nos vamos al puerto http 80 y procedemos afuzzear la paginaweb para buscar directorios o subdominios.


![list](/assets/img/devzat/A-2022-12-07-20-09-29.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Encontramos un subdominio pets.devzat.htb que vamos a probar `injecciones html` y `XSS`.


Si seguimos fuzzeando por direcctorios nos encontramos el directorio `/.git/`.


![list](/assets/img/devzat/A-2022-12-07-21-32-02.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/devzat/A-2022-12-07-21-34-01.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Este recursos nos vamos a bajar a ala maquina atacnate para revisarloso con lo del **GIT** con el comado `git reset --hard` para recomponer el proyecto y husmear en el mismo,.


Para mejor comodidad abrimos el Burpsuite y nos mandamos un ping a la maquina atacante y nos ponemos a la escucha con **tun0**.


![list](/assets/img/devzat/A-2022-12-07-21-06-03.png){:.lead width="800" height="100" loading="lazy"}


Como vemos que eso funciona nos mandamos una reverse-shell.


![list](/assets/img/devzat/A-2022-12-07-21-08-10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Debemos ponernos ala escucha con netcat ene el puerto 443.


Buscamos por pribileguios elevados haber que encontramos y tambien por capabilities.


![list](/assets/img/devzat/A-2022-12-07-22-02-03.png){:.lead width="800" height="100" loading="lazy"}


Como no encontramos nada a simple vista solo puertos que estan abiertos en el propioservido vamos a jugar con [chisel] para traernos el puerto a la maquina atacante y ver que estan ejecutando.


![list](/assets/img/devzat/A-2022-12-07-22-09-47.png){:.lead width="800" height="100" loading="lazy"}


[chisel]:(https://github.com/jpillora/chisel)



```bash
./chisel server --reverse --port 1234
```


{:.note}
Atacnate


```bash
./chisel client 10.10.14.5:1234 R:SOCKS 
```


{:.note}
Victima para traernos todo los puertos de una vez.


Una ves echo esto nos conectamos a SSH con cuanquier nombre al localhost porque nos trajimos eso puertos para ver que tienen en este caso es el 8443 y es el mismo chat que voimos en el puerto 8000 solo que este tiene algunas funciones habilitadas que el otro no.


```bash
ssh -l test 127.0.0.1 -p 8443
```


{:.note}
Pero aun nopodemos hacer nada por lo que seguimos con los otros puerto y hay uno que llamala atecion el [influxdb].


[influxdb]:(https://github.com/LorenzoTullini/InfluxDB-Exploit-CVE-2019-20933)


Nos decargamos y ejecutamos el exploit y husmeando en la base datos damos con credenciales validad para el usuario catherine y nos vamos a conectar por SSH  y la password es `woBeeYareedahc7Oogeephies7Aiseci`.


![list](/assets/img/devzat/A-2022-12-07-23-05-44.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ya podemos visualizar la flag en su escritorio.


***

## Exploitation and Privilege Escalation


Siempre es bueno ejecutar `LimEnum` Y `pspy` para monitorizar y ver los posibles vectores para escalar de privilegios, ademas hasta que se ejecute los anteriores podemos buscar los permisos con el comado find o tareas crond o tareas que esperen ejecucion.


```shell
find / -type f -user catherine 2>/dev/null | grep -vE "proc|sys"
```


![list](/assets/img/devzat/A-2022-12-07-23-12-41.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Y en contramos dos archivoa que vamos a copiar en tmp y los vamos a investigar.


![list](/assets/img/devzat/A-2022-12-07-23-20-49.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Y encontramos una password `CeilingCatStillAThingIn2021?` que es para el puertp 8443 que nos vamos aconectar de la siguiente forma.


```bash
ssh 127.0.0.1 -p 8443
```


{:.note}
No nesesitamos el parametro `-l` porque estamos desde el propio servidor.


![list](/assets/img/devzat/A-2022-12-07-23-26-18.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Listamos el `/etc/passwd`.


![list](/assets/img/devzat/A-2022-12-07-23-27-07.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Listamos la `id_rsa` de root hy le damos permisos 600.


![list](/assets/img/devzat/A-2022-12-07-23-28-50.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ya podemos visualizar la flag de root ensu escritorio.


***

```shell
🎉 Felicitaciones ya has comprometido Devzat de HackTheBox 🎉
```
{:.centered}
***

***
Back to [Certification eJPTv2 ](2023-07-03-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eWPT ](){:.heading.flip-title}
{:.read-more}