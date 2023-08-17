---
layout: post
title: "Write Up Synfonos1. "
subtitle: "eCPPTv2 Track "
category: Blog
tags: [Medium,Chunin,Linux,VulnHub,LFI,Log-Poisoning,SUID,SAMBA,Reconnaissance,Path-Hijacking,Protocols,eCPPTv2]
image:
  path: /assets/img/synfonos1/synfonos1.png
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

![list](/assets/img/synfonos1/1.png){:.lead width="800" height="100" loading="lazy"}


### Nmap


```bash
nmap -p- --open --min-rate 5000 -n -vvv -Pn -sS 192.168.1.53 -oA allports
```


![list](/assets/img/synfonos1/2.png){:.lead width="800" height="100" loading="lazy"}


### Services and Versions


```bash
nmap -sVC -Pn -n -p22,25,80,139,445 198.168.1.53 -oN target
```

![list](/assets/img/synfonos1/3.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Expltation


### SAMBA TCP-445

Aunque tenemos el puerto 22 y 25 abiertos, no tenemos usuarios ni informacion para poder tratar de hacer algo asi que vamos a enumerar en servicio de samba para ver si podemos obtener informacion relevante.

```bash
nmap -p139,445 --script smb-enum-users 192.168.1.53 
```


![list](/assets/img/synfonos1/7.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con este script de nmap encontramos un usuario llamado **helios**.


```bash
nmap -p445 --script smb-security-mode 192.168.1.53
```

![list](/assets/img/synfonos1/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con este script de nmap encontramos un usuario llamado **guest** que es un usuario por defecto con el cual vamos a revisar el servicio de samba y pra ver a que share nos podemos conectary si es asi que informacion podemos obtener.


Con `smbmap -H 192.168.1.53 -u guest` nos conectamos y vemos que podemos leer el share `anonymous`, ademas que el dominio `synfonos.local` del servidor que talvez lo padmos usar mas adelante, esto tambien nos lo dijo nmap y dentro de este hat una archivo `attention.txt` que contiene un mensaje que pone ****Can users please stop using passwords like 'epidioko', 'querty' and 'baseball'!Next person I find using one of these passwords will be fired!-Zeus**** que son contraseñas asi que vamos a porbar esas contraseñas con el usuario **helios** para ver cual concuerda y si es asi si podemos ver algo mas en el share de helios.


![list](/assets/img/synfonos1/8.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
El share anonymous es el unico que tiene permisos de lectura.


![list](/assets/img/synfonos1/9.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Descargamos el archivo `attention.txt`.


![list](/assets/img/synfonos1/10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Abrimos para ver el contenido.


Pobandos las contraseñas con el usuario helios la correctaes qwerty.


![list](/assets/img/synfonos1/11.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con las credenciales**helios:qwerty** podemos leer el contenido del share helios.


Nos descargamos los dos archivo que existen dentro del share helios los cuales para el research.txt pone ****Helios (also Helius) was the god of the sun in Greek mythology. He was thought to ride a golden chariot which brought the sun across the skies each day from the east (Ethiopia) to the west (Hesperides) while at night he did the return journey in leisurely fashion lounging in a golden cup. The god was famously the subject of the Colossus of Rhodes, the giant bronze statue considered one of the SevenWonders of the Ancient World.**** y para todo.txt pone **1. Binge watch Dexter,2. Dance,3. Work on /h3L105** el cual en presumiblemente un directorio para el servicio **http** que vamos a revisdar.


![list](/assets/img/synfonos1/12.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Descargamos el archivo `research.txt` y tambien el archivo `todo.txt`.


![list](/assets/img/synfonos1/13.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Contenido de los archvios dentro del share helios.


### HTTP TCP-80


Al husmear el puerto 80, solo hay una imagen y viendo en el codigo funete no hay nada pero tenemos un subdirectorio `/h3L105`, que nos redirigue a un wordpress que no carga bien, si vemos el codigo fuente  vemos que carga del dominio **synfonos.local** en cual ya sabiamos de antes esto lo agregamos al `/etc/hosts` y recargamos, ahora vemos que estamos frente a un wordpress, cual debemos enumerar.


Primero revisamos la versionde wordpress con **whatweb** y con esa version vemos con searchsploit si hay una verion vulnerable.


![list](/assets/img/synfonos1/14.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
No hubo suerte con ningunio de esos.


Pero hay muchas formas de tratar de explotar un Worpress, primero es ver la version del mismo en este caso es **5.9.3**, tambien los plugins, los temas, el xmlrpc etc, en fin en este caso vamos a ir por los **plugins** pero para lograr esto debemos filtrar por los plugins con el siguiente one-liner.


```bash
curl -s -X GET http://192.168.1.53/h31105/ | grep "plugins" | awk -F'plugins' "(print $2)' | awk -F'/' “(print $2)' | sort —u
```

![list](/assets/img/synfonos1/15.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Tenemos dos plugins.


Despues de buscar los plugin que estan instalado en el worpres y en contrar dos y buscar formas de explotar los mismo encontre que los dos plugin son vulnerables a **LFI** por lo cual podemo ver archivo del sistema en este caso el **/etc/passwd** y vamos intentar acceder a otros archivos privileguiados del sitema.


![list](/assets/img/synfonos1/16.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
PoC de uno de los exploit encontrados con searchsploit.


![list](/assets/img/synfonos1/17.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Contenido del archivo /etc/passwd.


Despues de husmear he investigar por mucho tiempo recordamos que tenemos el pueto 25 abierto y como podemos ver archivos del sitema podemos ver el archivo de los losg de smtp del helios en la ruta `/var/mail/helios`.


![list](/assets/img/synfonos1/18.png){:.lead width="800" height="100" loading="lazy"}


### Log Poisonig smtp

Para generar log en smtp debemos conectarnos al servicio con `telnet 192.168.1.53 25`, como ya tenemos el usuario verificamos el usuario e injectamos un codigo que podemos controlar comandos como es un codigo en php si todo sale correcto esto generar un log que podremos manipular para otorgarnos una reverse-shell como el usuario helios.


![list](/assets/img/synfonos1/19.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Generando log de smtp.


![list](/assets/img/synfonos1/20.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Verificando log dedes la web.


![list](/assets/img/synfonos1/21.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Reverse-shell con el usuario helios debemos estar a la escucha con netcat.


***

## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 


Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.


También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.

Enumerando el sistema y buscando por archivos **SUID** en contramos que el archivo `/opt/statuscheck`, es de el propietario root por lo consigiente vamos aprovecharnos de esto para escalar privilegios, para esto primero debemos saber que hace, pero como es un binario no hay nada legible pero con `string /opt/statuscheck` podemos ver cararteres legibles y ahi esta una referncia a `curl` pero no esta repersentado de forma absoluta, entonces lo que podemos de intertar es un `path hijacking`, consiste en crear en una ruta que controlemos uns archivo que ejecute la supuesta utilidad que ejecuta el original entonces crearemos en tmp el archivo curl pero no sera un binario sino aqui es dode injectaremos el comado que nos proporcione una bash con privilegios de root de la siguiete forma.


![list](/assets/img/synfonos1/22.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Binario SUID.


![list](/assets/img/synfonos1/23.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
El binario hace algo que hace curl.


![list](/assets/img/synfonos1/24.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ruta relativa de **curl**.


Para acontecer el path hijacking debemos crear en tmp un archivo llamado curl al cual le injectaremos el comado **chmod u+x /bin/bash** y para ejecutarlo debemos hacer que el path cambie y que primero se llame desde tmp de la siguiente forma **export PATH=/tmp:$PATH** y luego **/opt/statuscheck** esto nos permite escalar privilegios con **bash -p**, me olvide sacar carpturas.


![list](/assets/img/synfonos1/26.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Comando **bash -p**.


![list](/assets/img/synfonos1/25.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ya podemos buscar la flag en el escritorio de root.


***

```bash
🎉 Felicitaciones ya has comprometido Synfonos1 de VunlHub 🎉
```
{:.centered}

***

Back to [Certification eCPPTv2](2023-07-06-Road-to-eCPPTv2.md){:.heading.flip-title}
{:.read-more}
