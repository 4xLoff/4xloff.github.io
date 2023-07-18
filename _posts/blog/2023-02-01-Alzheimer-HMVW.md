---
layout: post
title: "Write Up Alzheimer. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,HMVM,Reverse-Shell,PHP,FTP,SUDO,GTFObins,Weak-Credentials,Reconnaissance,Buffer-Overflow,Ghidra,Steganography,Protocols,Fuzzing-Web,Port-Knocking,eJPTv2]
image:
  path: /assets/img/alzheimer/alzheimer.png
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

![list](/assets/img/alzheimer/1.png){:.lead width="800" height="100" loading="lazy"}


### Nmap


```bash
nmap --open -p- -Pn -n -T4 -vvv -n 198.168.1.3 -oN allports
```


![list](/assets/img/alzheimer/2.png){:.lead width="800" height="100" loading="lazy"}



### Services and Versions

```bash
nmap -sVC -Pn -n -p21 198.168.1.3 -oN target
```

![list](/assets/img/alzheimer/3.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Expltation


### FTP TCP-21


Como podemos conectarnos como el usuario **anonymous** sin credenciales ya que es el unico puerto que tenemos y encontramos un archivo oculto **.secretnote.txt**, que pone **I need to knock this ports and one door will be open! 1000 2000 3000 Ihavebeenalwayshere!!!**, nos presenta una técnica completamente llamada **port knocking**, es una técnica de seguridad utilizada para ocultar los servicios expuestos en un servidor o dispositivo detrás de un firewall. En lugar de tener los puertos abiertos de forma permanente, el port knocking requiere que los usuarios realicen una secuencia específica de conexiones a puertos cerrados antes de que se les permita el acceso a un servicio o puerto específico.



![list](/assets/img/alzheimer/5.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Archivo oculto.


![list](/assets/img/alzheimer/8.png){:.lead width="800" height="100" loading="lazy"}



![list](/assets/img/alzheimer/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con `knock -v 192.168.1.3 1000  2000 3000` vamos abrir los puerto, y para comprovarlo volveremos a usar nmap.


### HTTP TCP-80

Con el puerto 80 expuesto  es hora de  husmear en la pagina web y pone **I dont remember where I stored my password :(I only remember thatwas into a .txt file...-medusa<!---. --- - .... .. -. --. -->**, parece ser un codigo morse y el usuario medusa.



![list](/assets/img/alzheimer/7.7.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Aqui me salian la respuesta extraña ya que pase por alto  el comentario en php por eso es que no sale la palabra correcta que en este caso es **NOTHING**, y nada mas asi que vamos a fuzzerar.


Encontramos cuatro directorios en el **/home** pone **Maybe my pass is at home! -medusa**, en el **/admin** no hay nada, en el **/root** hay un archivo llamado **secret** pone **Maybe my password is in this secret folder?**, y por ultimo **/home** pone **Im trying a lot. Im sure that i will recover my pass! -medusa**, nada en concreto solo el usuario medusa pero al principio en contramos la contraseña **Ihavebeenalwayshere!!!**.


![list](/assets/img/alzheimer/7.7.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/alzheimer/9.png){:.lead width="800" height="100" loading="lazy"}



{:.note}
Ya nos podemos conectar por ssh a meduas y buscar la flag en su directorio.


***

## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 


Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.


También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


Sudo -l nos dice  el usuario **medusa** tiene permisos especiales y puede ejecutar el comando **/bin/id** pero buscando no nos podemos aprovecahr de id para escalar privileguos sin proporcionar una contraseña pero no hay nada en internet sobre como escalar privileguios con eso asi que debemos buscar otra forma.


A hora que con `find / -type f -perm -4000 -ls 2>/dev/null` podemos ver un binario que se parece aotro pero es raro que est ahi asi que lo buscamos en GTFOBins y listo lo explotamos.


![list](/assets/img/alzheimer/11.1.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/alzheimer/12.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ya es cuestion de buscar la flag en su directorio, el de root.


***

```bash
🎉 Felicitaciones ya has comprometido Alzheimer de Hack My VM 🎉
```
{:.centered}

***

Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}
