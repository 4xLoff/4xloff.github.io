---
layout: post
title: "Write Up Hannah. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,HMVM,Hydra,CronJob,Brute-Forcing,Reconnaissance,Weak-Credentials,Path-Hijacking,eJPTv2]
image:
  path: /assets/img/hannah/hannah.png
---

***

<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance

{:.note title="Attention"}
En el siguiente enlace te dejo la [Maquina](https://hackmyvm.eu/machines/machine.php?vm=Hannah) de la plataforma de Hack My VM.

### Ping Sweep


```bash
sudo arp-scan -I ens33 --localnet
```


![list](/assets/img/hannah/1.png){:.lead width="800" height="100" loading="lazy"}


### Nmap


```bash
nmap --open -p- -Pn -n -T4 -vvv -n 192.168.100.43 -oN allports
```


![list](/assets/img/hannah/2.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions

```bash
nmap -sVC -Pn -n -p22,80,113 192.168.100.43 -oN target
```

![list](/assets/img/gift/3.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Exploitation


### HTTP TCP-80


Aunque tenemos dos puertos, en el puerto 22 no podemos hace nada de momento, asi que nos vamos a concentrar en el puerto 80, si usamos herramientas como **whatweb** o **wappalizer**, no coseguiremos nada solo uan ruta, pero nmap no dice que existe el archivo robots.txt que tine una ruta `/enlightenment` de momento no nos dice, nada pero vamos a fuzzer con **Gobuster**.


![list](/assets/img/hannah/5.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/hannah/4.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ruta en robot.txt

### PORT 113


En resumen, el protocolo ident en el puerto 113 tiene como finalidad identificar al usuario que está realizando una conexión TCP. Al realizar un escaneo avanzado con nmap, se puede visualizar un dato inusual denominado "auth-owners" que revela la presencia de un usuario adicional llamado moksha, aparte del usuario root. Esta información nos permite detectar la existencia de dicho usuario en el sistema.


![list](/assets/img/hannah/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Aque nos dice que el usuario de servicio 113 es root de momento no nos sirve.


### SSH TCP-22

Lo unico que nos queda es centrarnos en el puerto 22, y con el usuario mokska procederemos a bruteforcear con hydra


```bash
sudo hydra -l mokska -P /usr/share/seclists/Discovery/Password/Leaked-Databases/rockyou.txt ssh://192.168.100.43 -F
```

![list](/assets/img/hannah/7.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La contraseña es **hannah**.


***

## Escalation Privileges

Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 

Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.

También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


![list](/assets/img/hannah/9.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
En una tarea se esta ejecutando touch de foma relativa por lo que vamos a probar la tecnica de **Path hijacking**.


De acuerdo, para llevar a cabo el path hijacking, podemos aprovechar una vulnerabilidad en la última ruta del PATH. En este caso, podemos escribir en el directorio **/media**. A continuación, vamos a crear un archivo llamado **touch** en ese directorio y le daremos permisos de ejecución `chmod +x /media/touch`.

Una vez hecho esto, modificaremos el archivo bash y le asignaremos el bit SUID asi `echo "chmod +s /bin/bash" > /media/touch`, lo que nos permitirá ejecutarlo con los privilegios de **root**. Este paso es crucial para poder elevar nuestros privilegios y obtener acceso como usuario root.



***

```bash
🎉 Felicitaciones ya has comprometido Hannah de Hack My VM 🎉
```
{:.centered}

***

Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}
