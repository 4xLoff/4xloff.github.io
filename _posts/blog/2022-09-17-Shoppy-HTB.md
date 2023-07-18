---
layout: post
title: "Write Up Shoppy. "
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Linux,HTB,NoSQL,Cracking,Hashes,Docker,SUDO,Log,CVE,RCE,Steghide,SSH,Web,Vulnerability-Assessment,Injection,Common-Applications,Custom-Applications,Reversing,NGINX,Docker,C,Reconnaissance,Web-Site-Structure-Discovery,Fuzzing-Web,Password-Reuse,Password-Cracking,Brute-Forcing,Docker-Abuse,Decompilation,SQLi,Weak-Credentials,Clear-Text-Credentials,Information-Disclosure,eWPT,OSWE,OSCP] 
image:
  path: /assets/img/shoppy/Captura%20de%20pantalla%20(316).png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
nmap -p- --open --min-rate 5000-sS -n -vvv -Pn 10.10.11.180 -oA allports
```


![list](/assets/img/shoppy/Kali-2022-09-24-17-19-50.png){:.lead width="800" height="100" loading="lazy"}


***

### Services and Versions


```bash
nmap -p22,80,9093 -sV -sC 10.10.11.180 -oN target
```

![list](/assets/img/shoppy/Kali-2022-09-24-17-24-43.png){:.lead width="800" height="100" loading="lazy"}


## Vulnerability Analysis


### HTTP TCP-80


Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros.e ispeccionamos la web, ademas de las tecnologias de la ip ataves de la terminal o via  web esto lo hacemos con wapalizzer o whatweb elcual nos redirigue aun subdominio `shoppy.htb` y o guardamos al archivo `/etc/hosts`.


Husmenado la web no encontramos nada asi que vamos a fuzzear con wfuzz para conseguir los directorios y con gubuster para subdominios.


![list](/assets/img/shoppy/Kali-2022-09-24-18-48-37.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Fuzz directorios.


![list](/assets/img/shoppy/Kali-2022-09-24-18-42-48.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Fuzz subdominios.


Encontramos un login e intentamos todas las querys de inyeccion SQL que nos sabemos sin nigun resultadoasi qeu depues de haber probado muchas cosas sin exito, vamosa probar `NoSQL` y para so nos vamos ayudar de [PayloadsAllTheThings]


[PayloadsAllTheThings]:(https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/NoSQL%20Injection)


![list](/assets/img/shoppy/Kali-2022-09-24-17-38-04.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La query NoSQL que funciona es `admin'||'1==1`.


Una vesingresamos podemos ver un buscador de usuarios.


![list](/assets/img/shoppy/Kali-2022-09-24-17-38-10.png){:.lead width="800" height="100" loading="lazy"}


Despues de husmear encontramos credenciales.


![list](/assets/img/shoppy/Kali-2022-09-24-17-49-59.png){:.lead width="800" height="100" loading="lazy"}


Con john gtratamos de crackear los hashes y logramos obtener una contraseña que es `remembermethisway` del usuario `josh`.


De antes que habimos encontrado un subdominio `mattermost.shoppy.htb` es otro login, para el cual podemos usar las credenciales.


![list](/assets/img/shoppy/Kali-2022-09-24-18-28-00.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Las credeciales son valiadas.


Husmenado entre la conversacion de dos usuario dimos con las contraseñas de jaeger y su contraseña `Sh0ppyBest@pp!` la que usaremos para conectarnos por SSH.


![list](/assets/img/shoppy/Kali-2022-09-24-18-32-16.png){:.lead width="800" height="100" loading="lazy"}


```shell
sshpass -p 'Sh0ppyBest@pp!' ssh jaeger@10.10.11.180
```


{:.note}
La flag del usuaripo de bajos privileguios esta en el escritorio de `jaeger`.


***

## Explotacion and Escalation Privileges


Siempre es bueno ejecutar `LimEnum` Y `pspy`, para que podamos enumerar más vulnerabilidades que permitan elevar nuestros privilegios al usuario "root", por lo que deberemos convertirnos en el usuario deploy para poder ejecutar ese binario.


![list](/assets/img/shoppy/Kali-2022-09-24-18-34-20.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Al ejecutarlo nos pide una contraseña, asi que no tenemos acceso.


Pero si le hacemos un cat al archivo podemos ver nsa credencial que usaremos y que es `Sample`.


![list](/assets/img/shoppy/Kali-2022-09-24-18-42-48.png){:.lead width="800" height="100" loading="lazy"}
Utilizamos las crdeciales para conectarnos por SSH con el usuario `deploy` y las pass `Deploying@pp!`.


```shell
sshpass -p 'Deploying@pp!' ssh deploy@10.10.11.180
```


{:.note}
Y recurimos a [GTObins] para ver como hacernos root con docker.


[GTObins]:(https://gtfobins.github.io/gtfobins/docker/#shell)


```shell
docker run -v /:/mnt --rm -it alpine chroot /mnt sh
```


{:.note}
Ejecutamos.


![list](/assets/img/shoppy/Kali-2022-09-24-18-48-37.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ya podemos, buscar la flag en el escritorio del root.


***

```shell
🎉 Felicitaciones ya has comprometido Shoppy. de HackTheBox 🎉
```
{:.centered}
***
Back to [Certification eWPT](){:.heading.flip-title}
{:.read-more}

***
Back to [Certification OSWE](){:.heading.flip-title}
{:.read-more}

***
Back to [Certification OSCP](){:.heading.flip-title}
{:.read-more}
