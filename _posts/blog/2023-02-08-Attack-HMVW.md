---
layout: post
title: "Write Up Superhuman. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Medium,Chunin,Linux,HMVM,SSH,CronJob,Hydra,GTFOBins,Reconnaissance,Brute-Forcing,ssh2john,Protocols,zip2john,Crunch,eJPTv2]
image:
  path: /assets/img/superhuman/superhuman.png
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

![list](/assets/img/superhuman/1.png){:.lead width="800" height="100" loading="lazy"}


### Nmap


```bash
nmap --open -p- -Pn -n -T4 -vvv -n 198.168.100.49 -oN allports
```


![list](/assets/img/superhuman/2.png){:.lead width="800" height="100" loading="lazy"}



### Services and Versions


```bash
nmap -sVC -Pn -n -p22,80 198.168.100.49 -oN target
```

![list](/assets/img/superhuman/3.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Expltation


### HTTP TCP-80


Con el puerto 22 no podemos hacer nada asi que vamosa a husmear el puerto 80,  esta vacia, entonce vamos a fuzzear y encontramos algunos archivos  pero el interesante es **/notes-tips.txt** porque tine una especie de codigo encriptado que pone **** no sabes en que pero vamos a usar [decode.fr] para decodificarlo.


![list](/assets/img/superhuman/7.png){:.lead width="800" height="100" loading="lazy"}


[decode.fr]: https://www.dcode.fr/cipher-identifier


![list](/assets/img/superhuman/4.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
El texto decifrado es  **salome doesn't want me, I'm so sad... i'm sure god is dead...I drank 6 liters of Paulaner.... too drunk lol. I'llwrite her a poem and she'll desire me. I'll name it salome_and_?? I don't know.I must not forget to save it and put a good extension because I don't have much storage**.


![list](/assets/img/superhuman/5.png){:.lead width="800" height="100" loading="lazy"}


Es una nota de desamor lo que dice esque lo va a guardar pero no se acuerda la extencion, ademas pone su nombre **salome an ??** ** que es le la chica por la cual esta bebiendo  y debemos descubri en nombre de el para eso vamos usar crunch o ffuf `crunch 13 13 -t salome_and_@@ > name.txt` entonces vamos afuzzear tambien la extension.


![list](/assets/img/superhuman/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La extension es **.zip**


TratamoS de extraer el **salome_and_me.zip** pero nenesitamos una contraseña asi que vamos a usar **zip2john** para lograrlo.


![list](/assets/img/superhuman/8.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/superhuman/9.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/superhuman/10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La password es **turtle**.


![list](/assets/img/superhuman/11.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
En el interior hay una nota **salome_and_me.txt** que pone **My name is fred, And tonight I'm sad, lonely and scared, Because my love Salome prefers schopenhauer, asshole, I hate him he's stupid, ugly and a peephole, My darling I offered you a great switch, And now you reject my ove, bitch I don't give a fuck, I'll go with another lady, And she'll call me BABY!**.


![list](/assets/img/superhuman/12.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Lo que yo hice aki es crear un filtro para hacer un diccionario la password es **schopenhauer**, pude haberla  deducido ah y el usuario  es fred, por cierto.


![list](/assets/img/superhuman/13.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Nos conectamos como **fred** por ssh y buscamos la  flag en su directorio.


***

## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 


Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.


También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


Buscando por capabilities node tiene este privileguio, asi que vamos GTFOBins.


![list](/assets/img/superhuman/14.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ejecutamos el comado, lo que nos da una shell como root y ya podemos buscar la falag en su escritorio.


***

```bash
🎉 Felicitaciones ya has comprometido Superhuman de Hack My VM 🎉
```
{:.centered}

***

Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}
