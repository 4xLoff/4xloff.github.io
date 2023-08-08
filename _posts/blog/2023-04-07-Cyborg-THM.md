---
layout: post
title: "Write Up Cyborg. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,THM,SSH,SUDO,Fuzzing-Web,Reconnaissance,Brute-Forcing,John,Misconfiguration,Weak-Credentials,eJPTv2]
image:
  path: /assets/img/cybord/cyborg.jpg
---

***

<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### Nmap


```bash
nmap --open -p- -Pn -n -T4 -vvv -n 10.10.237.236 -oN allports
```


![list](/assets/img/cybord/1.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions

```bash 
nmap -sVC -Pn -n -p22,80 10.10.237.236 -oN target
```

![list](/assets/img/cybord/2.1.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Exploitation


### HTTP TCP-80


En el pueto 80 solo esta la paguina por de fecto de apache asi que vamos a fuzzear con FFUF.


![list](/assets/img/cybord/3.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
tenemos dos directorios el **admin** y el **etc**.


![list](/assets/img/cybord/2.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Fuzzeando dentro de /etc/ encontramos un directorio /squid/ que vamoa a fuzzear por supuesto.


![list](/assets/img/cybord/4.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Dentro de /squid/ encontramos un archivo **passwd** que contiene un un usuario y un has que vamos a crackear con jhon la contraseña es **squidward**.

### Borg

Tratamos de conectarnos a ssh pero no es asi que volvemos a /admin/ no nos olvidemos es el otro directorio que fuzzeamos y hay nos decargamos un archive.tar que vamos a descomprimir.


![list](/assets/img/cybord/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Archive.tar.


Contiene algunos archivos pero la mayoria son binarios un config y una nota , ademas un directorio data de primeras pense que era un proyecto git pero no en la nota pone que es algo que tiene que ver con [Borg] y eso lo vamos a averigurar en internet.

[Borg]: https://borgbackup.readthedocs.io/en/stable/


![list](/assets/img/cybord/7.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Vemos la documentacion oficial para instalacion y uso.


Para montar el proyecto se neseita contraseña la cual tenemos  que es squidward, procedemos a listar el proyecto.


![list](/assets/img/cybord/9.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Listamos has proyecto solo hay uno.


![list](/assets/img/cybord/10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Extraemos el proyecto.


![list](/assets/img/cybord/2023-07-01_22-51.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Consegumos crenciales que son alex:S3cretP@s3 y nos conectamos por ssh.


![list](/assets/img/cybord/12.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Nos conectamos con esas credenciales a SSH, la carperta de alex esta la flag.


***

## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 


Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.


También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


Con **sudo -l**, puedes ver que el usuario root puede ejecutar **(ALL : ALL) NOPASSWD: /etc/mp3backups/backup.sh** asi que solo lo editamos con nano y obtenrmos una shell como root.



![list](/assets/img/cybord/14.png){:.lead width="800" height="100" loading="lazy"}



***

```bash
🎉 Felicitaciones ya has comprometido Cyborg de Try Hack My 🎉
```
{:.centered}

***

Back to [Certification eJPTv2](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}


