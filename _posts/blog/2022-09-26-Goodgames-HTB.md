---
layout: post
title: "Write Up Goodgames. "
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Linux,HTB,SQLi,SSTI,Hashes,Docker,Web,Network,Vulnerability-Assessment,Injection,Virtualization,Security-Tools,Authentication,Flask,SQLMap,Reconnaissance,Password-Reuse,Password-Cracking,Docker-Abuse,Misconfiguration,OSCP,eWPT,eJPTv2,eCPPTv2] 
image:
  path: /assets/img/goodgames/Captura%20de%20pantalla%20(305).png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
nmap -p- --open --min-rate 5000-sS -n -vvv -Pn 10.10.11.130 -oA allports
```


![list](/assets/img/goodgames/Parrot-2022-12-19-17-04-01.png){:.lead width="800" height="100" loading="lazy"}


***

### Services and Versions


```bash
nmap -p22,80,1337 -sV -sC 10.10.11.130 -oN target
```


![list](/assets/img/goodgames/Parrot-2022-12-19-17-05-22.png).png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis


### HTTP TCP-80


Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros.e ispeccionamos la web, ademas de las tecnologias de la ip ataves de la terminal o via  web esto lo hacemos con wapalizzer o whatweb. 


![list](/assets/img/goodgames/Parrot-2022-12-19-17-06-54.png){:.lead width="800" height="100" loading="lazy"}


Nos encontramos con una pagina delogin y registro pero vamos abrir el burpsuite para intersectar las peticiones y probar algunos ataques e igual nos vamos a registrar para ver que pasa.


![list](/assets/img/goodgames/Parrot-2022-12-19-17-29-20.png){:.lead width="800" height="100" loading="lazy"}


Despues de varias pruebas nos damos cuenta que es susebtible a SQL-injection la pagina web asi que despuer de probar las  Querys mas comunes logramos consegir informacion.


![list](/assets/img/goodgames/Parrot-2022-12-19-17-41-10.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/goodgames/Parrot-2022-12-19-17-41-18.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Nos damos cuenta de aquello porque en numerom del `content-lentgh` cambia de `339490` a `9267` cuando es correcto.


Tambien en las pruebas con burpsuite se setea un cookie y es de el usuario administrado pero no podemos hacer mucho solo que probando en las configuraciones llegamos a la conclusion que se esta aplicando virtualhosting el cual es `goodgames.htb` eh hackthebox siempres es el mismo patron asi que lo agregamos al /etc/host y eso nos lleva a una direccion url `internal-administration.goodgames.htb/login` pero no tenemos credenciales ni nada pero vemos que corre flask podriamos pensar que es suseptible a SSTI lo cual probaremos mas adelante.


Jugando con un secuenciador y aplicado con las injeciones-SQL logramos averiguar los hashes de los usuarios `admin` y del que cree tambien.


![list](/assets/img/goodgames/Parrot-2022-12-19-17-52-26.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/goodgames/Parrot-2022-12-19-18-33-35.png){:.lead width="800" height="100" loading="lazy"}


Lo sigiente es usar `john` para crackear el hash de admin o tambien usar `crackstation` que es usa herramienta online.


![list](/assets/img/goodgames/Parrot-2022-12-19-18-37-59.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La contraseña  del usuario  admin es superadministrator.


Nos loquemos con estas credeciales a panle de login que enumeramos de antes y deberiamos entrar en el panel de administrados de `admin` y husmenado por ahi en contramos un campos suceptible a [SSTI] en cual usaremos para otorgarmos una reverse-shell.


![list](/assets/img/goodgames/Parrot-2022-12-19-19-12-31.png){:.lead width="800" height="100" loading="lazy"}
Debemos estar a la escucha con netcat en el puerto 443.


[SSTI]:(https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection)


{:.note}
La flag de bajos privileguios en el en la carpeta del usuario augustus que es una montura que del directorio `/home` de la maquina real.


***

## Explotacion


Siempre es bueno ejecutar `LimEnum` Y `pspy`, para que podamos enumerar más vulnerabilidades que permitan elevar nuestros privilegios al usuario "root".


Lo que nos queda ver que otras ip y puertos estam abiertos para pivotear de a la maquina real o de usuario esto hacemos con el siguiente one-liner.


```bash
#!/bin/bash
for i in $(seq 1 65535); do
        timeout 1 bash -c "echo '' > /dev/tcp/<IP>/$i" 2>/dev/null && echo "[*]El puerto $i esta -ACTIVE" &
done; wait
tput cnorm
``` 


{:.note}
Solo el puerto `22` y el 80 estan abiertos.


Como tenemos el puerto 22 abierto que es SSH que antes no vimos con nmap porque no estaba visble este abierto internamente vanmos a tratar de conectarnos con las mismas credenciales que usamos en el login de la pagina web porque muchas veces se suelen reutilizar de contraseñas.


![list](/assets/img/goodgames/Parrot-2022-12-19-19-12-31.png){:.lead width="800" height="100" loading="lazy"}


```shell
ssh augustus@172.19.0.1
```


{:.note}
La contraseña es `superadministrator`.


Para este punto probamos lo de siepre, permisos SUID, las capabilities, procesos, etc, pero si recordamos el contenedor es root lo que hacemos copiarno con `cp /bin/bash` a la carpeta de augustus que esta haciendo una montura en el contenedor root por lo que si volvemos a la montura y hacemos. 


```shell
chown root:root bash
```


{:.note}
Le asigunamos perimos de root al grupo del contenedor.


```shell
chmod u+s bash
```


{:.note}
Le damos permiso SUID.


Lo que tenemos  que hacer `bash -p` para obtener la bash de root.



{:.note}
Y con la contraseña de root esta en el ecritorio del mismo.
}

***

```shell
🎉 Felicitaciones ya has comprometido Goodgames de HackTheBox 🎉
```
{:.centered}

***

Back to [Certification eJPTv2](2023-07-03-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}

***

Back to [Certification eWPT](2023-07-04-Road-to-eWPT.md){:.heading.flip-title}
{:.read-more}

***

Back to [Certification eCPPTv2](2023-07-06-Road-to-eCPPTv2.md){:.heading.flip-title}
{:.read-more}

***

Back to [Certification OSCP](2023-07-10-Road-to-OSCP.md){:.heading.flip-title}
{:.read-more}