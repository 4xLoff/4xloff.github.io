---
layout: post
title: "Write Up Backdoor. "
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Linux,HTB,Wordpress,LFI,CVE,RCE,PHP,Web,Vulnerability-Assessment,Outdated-Software,Backdoor,Reconnaissance,Maintain-Access,Directory-Traversalt,OSCP,eWPT,OSWE,eWPTxv2] 
image:
  path: /assets/img/backdoor/Captura%20de%20pantalla%20(303).png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
nmap -p- --open --min-rate 5000-sS -n -vvv -Pn 10.10.11.125 -oA allports
```

![list](/assets/img/backdoor/Arch-2022-04-29-15-47-31.png){:.lead width="800" height="100" loading="lazy"}


### Services and Versions


```bash
nmap -p22,80,1337 -sV -sC 10.10.11.125 -oN target
```


![list](/assets/img/backdoor/2.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis


### HTTP TCP-80


Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros.e ispeccionamos la web, ademas de las tecnologias de la ip ataves de la terminal o via  web esto lo hacemos con wapalizzer o whatweb. 


![list](/assets/img/backdoor/Arch-2022-04-29-16-05-17.png){:.lead width="800" height="100" loading="lazy"}


Con serachsploit buscamos una vulneravilidad de enumeracion de usuarios  en wordpress pero njo nos resulta.


![list](/assets/img/backdoor/Arch-2022-04-29-16-10-55.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Pero husmenado en la web no esta redirigiendo aun dominio `backdoor.htb` el cual metermos al `/etc/hosts`.


Tratamos de buscar vulnerabilidades del worpress pero no encontramos nada pero eso no quier decri que los plugen esten no esten actualizados por ende son vulnerables, sempres  suelen esta en la ruta `/wp-content/plugins/`.  


![list](/assets/img/backdoor/Arch-2022-04-29-16-18-04.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Buscamos vulnerabilidades relacionadas con ebbok download.


Inspeccionando el exploit vemos  que suseptible a local file inclusion en una ruta dada y eso es lo que haremos en esta prueba me desacrge el `/etc/passdw`.


![list](/assets/img/backdoor/Arch-2022-04-29-16-38-35.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Podemos ver que existe un usuario llamado `user`.


De la misma manera podemo enumerar otras rutas como la .ssh, pero en /proc/net/tcp en contre los puertos que estan abiertos internamente para poder berlos hay que aplicarle un tratamiento `echo "<PORTS>" | sort -u | while read port; do echo "[+] Puerto $port" -> $(0x$port); done`. 


![list](/assets/img/backdoor/Arch-2022-04-29-17-04-15.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Los puertos que encontramos son 3306,53,55610,33060


El puerto 1337 es de `gdbserver` y buscamos vulnerabilidades de aquello con serachsploit y encontramos uno en python y lo ejecutamos .


![list](/assets/img/backdoor/Arch-2022-04-29-18-12-00.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Lo editamos y hacemos todo que nos pide esto nos otorgara una reverse-shell.


{:.note}
La flag de bajos privileguios en el escritorio del usuario user.

***
## Explotacion and Escalation Privileges


Siempre es bueno ejecutar `LimEnum` Y `pspy`, para que podamos enumerar más vulnerabilidades que permitan elevar nuestros privilegios al usuario "root".


Buscamos por privilegios SUID con `find \-perm -4000 2>/dev/null` y encontramos un binario `/usr/bin/screen`.


Ya solo nos sicronisamos a la seccion de root con el siguiente comado.


```shell
screen -x root/
```


{:.note}
Y con la contraseña de root esta en el ecritorio del mismo.


***

```shell
🎉 Felicitaciones ya has comprometido Backdoor de HackTheBox 🎉
```
{:.centered}
***

Back to [Certification eWPT](){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eWPTXv2](){:.heading.flip-title}
{:.read-more}

***
Back to [Certification OSWE](){:.heading.flip-title}
{:.read-more}

***
Back to [Certification OSCP](){:.heading.flip-title}
{:.read-more}




