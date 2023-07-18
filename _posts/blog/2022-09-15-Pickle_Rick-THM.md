---
layout: post
title: "Write Up Pickle Rick."
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Linux,THM,GTFOBins,Reconnaissance,Fuzzing-Web,eJPTv2]
image:
  path: /assets/img//rick/rick2.png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
sudo nmap --open -p- -Pn -n -vvv --min-rate 5000 -sS 10.10.160.208 -oG allports
```


### Services and Versions


```bash
nmap -sCV -p22,80 10.10.160.208 -oN target
```

![list](/assets/img/rick/Kali-2022-09-18-21-40-56.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis


### HTTP TCP 80


Uso de Investigacion web, Google Hacking,Google Dorks y, ecopilación de información gracias a servicios de terceros.


Investigamos el servicio http que corre en el pueto 80, podemos usar **wapalizzer** para ver que tecnologias usa la pagina asi como desde el terminal **whatwe** al hacer `crtl+ u` nos da una pista. 


![list](/assets/img/rick/Kali-2022-09-18-21-45-15.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Hacemos ctrl + u para ispeccionar la pagina, econtrandonos con una pista que es el usuario `R1ckRul3s`y en el robots.txt encontramos la pass `Wubbalubbadubdub`.


Fuzzeamos la direccion IP para enumerar posibles direcctorios y nos encontramos el directorio `/portal/`y`/login/`.


```bash
wfuzz -c -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt -u http://10.10.160.208/FUZZ.php -t 200 -hc=404
```


![list](/assets/img/rick/Kali-2022-09-18-22-04-44.png){:.lead width="800" height="100" loading="lazy"}


Si nos movemos a esa ruta en el navegador nos encontramos con un formulario para loogearnos como ya tenemos credenciales procedemos.


![list](/assets/img/rick/Kali-2022-09-18-22-00-09.png){:.lead width="800" height="100" loading="lazy"}

{:.note}
Nos reedirige a portal.php donde podemos ejecutar comandos.


***

## Exploitation


Ya podemos ejecutar comandos como whoami, ls, pwd execto cat por lo que unaque podemos listar el usuario y vemos las siguientes pistas no las podemos ver pero no hay que preocuparse en ves de cat vamos a usar less a los **superingredient.txt** y visualizamos la primera pista que es`mr.meeseek hair`. 


![list](/assets/img/rick/Kali-2022-09-18-23-28-13.png){:.lead width="800" height="100" loading="lazy"}


Lo mismo acemos con la otra pista de clue.txt


![list](/assets/img/rick/Kali-2022-09-18-23-36-33.png){:.lead width="800" height="100" loading="lazy"}


Podemos listar usuarios del /etc/passwd pero solo son del sitema por lo que ha este punto procedemos ha entablarnos una [reverse-shell], yo la hice en python pero segun que programas tenga intalado la maquina victima se puede usar otras. 


[reverse-shell]: https://www.revshells.com/


![list](/assets/img/rick/Kali-2022-09-18-23-45-08.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Levantamos el listener a la escucha y nos conectamos ya lo unico es buscar la otra pista en este caso es `1 jerry tear`.


***

## Privilege escalation


Siempre es bueno ejecutar `LimEnum` Y `pspy` para monitorizar y ver los posibles vectores para escalar de privilegios.


LimEnum dice que tenemos la capacidad de ejecutar binarios SUID.


LO siguiente es ejecutar el mas que conocido `sudo -l` y ser root y vizualizar la tercera 


flag que es `fleeb juice`.


![list](/assets/img/rick/Kali-2022-09-18-23-46-29.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/rick/Kali-2022-09-18-23-48-00.png){:.lead width="800" height="100" loading="lazy"}


***
```bash
🎉 Felicitaciones ya has comprometido Pickle Rick de Try Hack Me 🎉
```
{:.centered}
***

Back to [Certification eJPTv2 ](2023-07-03-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}


















eWPT OSWE OSCP