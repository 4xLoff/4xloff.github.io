---
layout: post
title: "Write Up Hommie. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,HMVM,Reverse-Shell,PHP,FTP,SUDO,GTFObins,Weak-Credentials,Environment-Variable,Reconnaissance,Protocols,SSH,SUID,TFTP,UDP,eJPTv2]
image:
  path: /assets/img/hommie/hommie.png
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

![list](/assets/img/hommie/1.png){:.lead width="800" height="100" loading="lazy"}


### Nmap


```bash
nmap --open -p- -Pn -n -T4 -vvv -n 198.168.1.2 -oN allports
```


![list](/assets/img/hommie/2.png){:.lead width="800" height="100" loading="lazy"}



### Services and Versions

```bash
nmap -sVC -Pn -n -p21,22,80 198.168.1.2 -oN target
```

![list](/assets/img/hommie/3.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Expltation


### FTP TCP-21

Como priordad yo siempre voy de el servicio que tenga mas informacion y en este caso es ftp asi que primero voy a husmear en este ya que tenmos la posibilidad de conectarnos como el usuario **anonymous**, en el directorio oculto llamado **web** encontramos un archivo llamado **index** que podemos visualizar a través del protocolo HTTP. Dentro de ese directorio, tenemos la capacidad de escribir archivos, por lo que intenté subir una php-reverse-shell.php. Sin embargo, el servidor no ejecuta el código PHP y lo sabemos si en un archvivo llamado test-php con el siguiente contenido **<?php phpinfo(); ?>**, lo cual significa que necesitamos explorar otras opciones para lograr nuestro objetivo, pero d espues de mucho tiempo me doy cuenta que esto es un rabithole.


![list](/assets/img/hommie/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Servidor FTP.


### HTTP TCP-80


Vemos la pagina y no tine nada solo pone **alexia, Your id_rsa is exposed, please move it!!!!!Im fighting regarding reverse shells!-nobody** por lo que procederemos a fuzzear.


![list](/assets/img/hommie/4.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Pista.


![list](/assets/img/hommie/5.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Nada.


###  TFTP UDP-69 


Esto debimos hacerlo al principio pero bueno ya estamos aqui, asi que ni modo, primero fuzzeamos todo  el rango de puertos.


![list](/assets/img/hommie/7.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Hay dos puertos abiertos el **68/udp open|filtered dhcpc** y **69/udp open|filtered tftp**. 


![list](/assets/img/hommie/8.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Aqui esta la **id_sra** asi que ya nospodemos conectar por **ssh** presumiblemente.


![list](/assets/img/hommie/9.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Listo obtenemos una shell como alexia y la flag esta en su escritorio.


***

## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 


Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.


También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


Buscando por privileguios **SUID** con `find / -type f -perm -4000 -ls 2>/dev/null` y encontramos **/opt/showMetheKey**, al ejecutar el binario obtenemos otra clave privada.


![list](/assets/img/hommie/10.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/hommie/11.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
En primera  intancia parece que podemos usar esta clave para conectarnos por ssh, pero es la de alicia, asi que viendo los caracteres inprimibles con strings, vemos la toma de **cat $HOME/.ssh/id_rsa** aunque nos conectemos  seriamos alexia y ya solos alexia, entonces que hacemos.


![list](/assets/img/hommie/12.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Despues de tanto estar y estar, podemos midificar la variable de entorno de **export HOME=/root** para cambia de **/alexia** a **/root** para setear la clave root en ves que la de alexia y nos conectamos como ssh y buscamos la flag en sun escritorio.


***

```bash
🎉 Felicitaciones ya has comprometido Hommie de Hack My VM 🎉
```
{:.centered}

***

Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}
