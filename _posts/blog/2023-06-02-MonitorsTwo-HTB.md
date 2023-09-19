---
layout: post
title: "Write Up MonitorsTwo. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,HTB,Web,Vulnerability-Assessment,Common-Applications,Authorization,RCE,Weak-Credentials,Lateral-movement,Weak-Authentication,Misconfiguration,Binary-Exploitation,SUID,Docker,Docker-Abuse,GTFObins,CVE,John,Hashes,Cracking,Protocols,Reconnaissance,Real,eJPTv2,eWPT]
image:
  path: /assets/img/monitors2/monitors2.png
---

---

<!--more-->

1. this ordered seed list will be replaced by the toc
   {:toc}

---

## Reconnaissance


### nmap

```bash
nmap -p- --open --min-rate 5000 -n -vvv -Pn -sS 10.10.11.211 -oA allports
```

![list](/assets/img/monitors2/1.png){:.lead width="800" height="100" loading="lazy"}


### Services and Versions


```bash
nmap -sCV -p22,80 10.10.11.211 -oN target
```


![list](/assets/img/monitors2/2.png){:.lead width="800" height="100" loading="lazy"}


---

## Vulnerability Analysis and Exploitation


### HTTP TCP-80


Con nmap no conseguimos mucha informacion execpto el script http-enum que enumero un direcctorio `/docs/` en el cual vamos a husmear para ver de que se trata pero no conseguimos nada.


![list](/assets/img/monitors2/4.png){:.lead width="800" height="100" loading="lazy"}


Explorando la web y encontramos la version de la aplicacionde cacti con eso vamos a buscar en internet si hay posibles exploits, y efectivamente encontramos uno con wget lo decargamos y lo usamos con esto conseguimos una reverse-shell como `www-data` 


![list](/assets/img/monitors2/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
El usuario es `www-data`.


### Lateral Movement


Luego de buscar vectores para escalar privilegios encontramos que no estamos en la maquina 10.10.11.211 por que exite un archivo `.dockerenv` y ademas no podemos usar algunos comandos como `ip` e `ifconfig` aprte que esto tambien es caracteristico de contenedores de docker `www-data@50bca5e748b0`.


![list](/assets/img/monitors2/8.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Archivo `.dockerenv`.


Seguimos enumerando porque algunas veces cuando estamos en docker hay un binariom que gestiona las capabilities `/sbin/capsh`.


![list](/assets/img/monitors2/8.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Buscamos como explotarlo en GTFObins.


Cuando ejecutamos el comado `capsh --gid=0 --uid=0 --` obtenemos root pero en el mismo contenedor de qui debemos tratar de escapar del este contexto.


![list](/assets/img/monitors2/9.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Contenedor como root.


Luego de enumerar algun tiempo encontramos una archivo de configuracion `/var/www/html/include/config.php` que contine credenciales las cuales son cactiuser:cactiuser que son de la base de datos de MySQL que vamos a meternos a ver que encontramos.


![list](/assets/img/monitors2/13.png){:.lead width="800" height="100" loading="lazy"}


Nos conectamos a la base de datos y buscando encontramos usuarios y credenciales que vamos a tratar de crackear con ***john the ripper**.


![list](/assets/img/monitors2/15.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Encontramos la password de marcos que es `funkymonkey` y que con esas nos vamos a conectar por ssh.


![list](/assets/img/monitors2/18.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/monitors2/16.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Lo logramos ya podemos ver la flag que esta en el escritorio.


---

## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada.


Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.


También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


Despues de algun timepo y usar **Linux-Smart-Escalation** vemos que marcus tiene mail asi que vamos a ver de que trata.


![list](/assets/img/monitors2/20.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Se trata de un correo con aviso de seguridad sobre tres vulnerabilidades y solo una de esas es interesnte para nosotros ya que es la del docker **CVE-2021-41091**, el cual vamos a explotar y vamos a buscar en internet de que se trata.


Investigando en internet vemos que con el coamdo `findmnt` nos muestra cuatro sistemas de archivos relacionados con Docker anidados en el directorio `/var/lib/docker`. Para ejecutar el exploit, necesitamos determinar cuál de estos pertenece al contenedor que ejecuta el servicio Cacti, donde previamente obtuvimos un shell de root. Para lograrlo, regresamos al shell dentro del contenedor y listamos los montajes del contenedor con `mount`.


![list](/assets/img/monitors2/21.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Comando `findmnt`.


![list](/assets/img/monitors2/23.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
De vuelta en el docker ejecutamos el coamdo comando `mount` al final esta rchivo relacionado y volvemos a **marcus**.


El chiste esque cada cosa que hagamos en ele contenedor se va a crear en marcus por lo que nos vamos a copiar la bash `cp /bin/bash /` y le vamos a dar permisos SUID `chmod u+s /bash`.


![list](/assets/img/monitors2/24.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ya podemos, buscar la flag en el escritorio del root.


---


```shell
🎉 Felicitaciones ya has comprometido MonitorsTwo de HackTheBox 🎉
```


{:.centered}


---


Back to [Certification eJPTv2](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}

---

Back to [Certification eWPT](2023-07-04-Road-to-eWPT.md){:.heading.flip-title}
{:.read-more}

---

Back to [Certification OSCP](2023-07-10-Road-to-OSCP.md){:.heading.flip-title}
{:.read-more}
