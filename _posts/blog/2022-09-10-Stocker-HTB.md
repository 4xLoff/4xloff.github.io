---
layout: post
title: "Write Up Stocker. "
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Linux,HTB,IRC,CVE,RCE,SSRF,Steganography,SSH,eJPTv2,eWPT] 
image:
  path: /assets/img/stocker/Captura%20de%20pantalla%20(328).png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
nmap -p- --open --min-rate 5000-sS -n -vvv -Pn 10.10.11.196 -oA allports
```

![list](/assets/img/irked/A-2022-12-22-12-25-19.png){:.lead width="800" height="100" loading="lazy"}


### Services and Versions


```bash
nmap -p22,80,111,6697,8667,38765,65534 -sV -sC 10.10.11.196 -oN target
```


![list](/assets/img/irked/A-2022-12-22-12-30-07.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis


### HTTP TCP-80


Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros.e ispeccionamos la web, ademas de las tecnologias de la ip ataves de la terminal o via  web esto lo hacemos con wapalizzer o whatweb. 


img 3


{:.note}
De aqui sacamos un subdominio stocker.htb el cual vamos agregar al /etc/hosts.


Inspeccionando la web no encontramos nada por lo que vamos a fuzzerar por direcctorio y subdominios.


![list](/assets/img/irked/A-2022-12-22-12-55-30.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
En contramos un subdominio dev.stocker.htb que vamos agregar al /etc/hosts.


Despues de probar SQLinjection y otros typos de ataques llego la conclusion que es NoSQL, ademas nos vamos a poner ala escucha con burpsuite ya que en payloadallthethings nos dice que el content-type debe estar en json.


img


{:.note}
Conseguimos una ruta /stock.


Si nos ponemos agregar cosas al carrito i luego nos metemos a ver nos muestra un ID y si le damos a HERE no lleva a un pdf.


vamos a interceptar todo esto para ver que informacion nos arroja, y al igual que antes es un json que esta mostrando lo que hemos agregado al carrito he investigando por internet llegamos a una vulneravilidad donde el json es susebtible a SSRF.


IMG


{:.note}
En la respuesta vemos un identificado que nos llama la atencion porque es igual al del ppdf asi que lo vamos a usar y encontramos el usuario agoose.


Despues de investigar por mucho tiempo llegamos al archivo index.js que esta en la ruta /var/www/dev/index.js que contiene algunas veces archivos de configuracion y hacemos lo mismo.


img
En contramos unas credenciales que dice que es para la base de datos mongodeb pero vamos a probarlas por ssh y en el login haver que pasa.


Aunque con el usuario dev no funciona conectarse por ssh con el usuario angoose si funciona.

img
la flag esta en el escritorio del usuario angoose.


***
## Exploration and Escalation Privileges


Siempre es bueno ejecutar `LimEnum` Y `pspy`, para que podamos enumerar más vulnerabilidades que permitan elevar nuestros privilegios al usuario "root".


Con sudo -l notamos que podemos ejecutar cualquier archivo js como el usuario root por lo que vamos a buscar por internet como darles permiso SUID  a la bash para hacder bash -p


{:.note}
Ya podemos, buscar la flag en el escritorio del root.


***

```shell
🎉 Felicitaciones ya has comprometido Stocker de HackTheBox 🎉
```
{:.centered}
***

Back to [Certification eJPTv2 ](2023-07-03-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}