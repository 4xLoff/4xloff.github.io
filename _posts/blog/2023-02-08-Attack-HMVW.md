---
layout: post
title: "Write Up Attack. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Medium,Chunin,Linux,HMVM,SSH,GTFOBins,WireShark,Reconnaissance,QR,Protocols,eJPTv2]
image:
  path: /assets/img/attack/attack.png
---

***

<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### Nmap


```bash
nmap --open -p- -Pn -n -T4 -vvv -n 198.168.1.42 -oN allports
```


![list](/assets/img/attack/2.png){:.lead width="800" height="100" loading="lazy"}



### Services and Versions


```bash
nmap -sVC -Pn -n -p21,22,80 198.168.1.42 -oN target
```

![list](/assets/img/attack/1.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Expltation


### HTTP TCP-80


Al husmear el puerto 80, solo pone **que hay una rchivo llamado capture y que no se acierda la extesion**, como sabemos por lo general ese nombre por defectova aocmpañado de la  **extension.pcap** por lo que fuzzearemos para ver que encontramos.


![list](/assets/img/attack/4.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Pista.


![list](/assets/img/attack/5.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Efectivamente el archivo se llama **capture.pcap**.


En este punto podemos usar tsark o Wireshark para analizarlo, pero  ami me gusta mas wireshark.


### WireShark


![list](/assets/img/attack/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Buscando por encimaya podemos ver credenciales **teste:simple**, ademas, notamos un archivo llamado **mysecret.png**, y un tercero llamado **filexxx.zip**.


![list](/assets/img/attack/7.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con las  credenciales nos conectamosa al servidor y descargamos el archivo **missecret.png** y **note.txt** que presumimos que son los mismos de la captura lo que nos hace pensar que es una especie captura del sitema que contempla el ftp y otras rutas por el aerchivo filexxx.zip no esta, tambie ya sabemos que hay dos usuarios mas **kratos** y **jackob**.


![list](/assets/img/attack/10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
En teste no podemos hacer nada.


![list](/assets/img/attack/11.png){:.lead width="800" height="100" loading="lazy"}


{:.note}   
Contenido de note.txt pero no nos dice nada.


La nota pone ***i need to find the file**, nada relevante, pero aun nos falta  ver el archivo **filexxx.zip** que podemos estraerlo de wireshark o de la paginaweb, si queremos verlo podemos fuxxearlo pero por el nombre no creo que este en el rockyou.txt asi que lo bajamos de la pagina web, me di cuenta que los tamaños son distintos, el de wireshark es la id_rsa y de la web es **mycode.png.** una imagen que es un codigo QR.


![list](/assets/img/attack/12.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Lo que debemos hacer es  exportar el objeto **filexxx.zip** y guardarlo, al  abrirlo es una clave privada.


![list](/assets/img/attack/13.png){:.lead width="800" height="100" loading="lazy"}



![list](/assets/img/attack/14.png){:.lead width="800" height="100" loading="lazy"}



![list](/assets/img/attack/16.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
QR que desiframos en internet y vemos una ruta **jacobattack.txt**.


![list](/assets/img/attack/2023-06-28_21-47.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/attack/18.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Y nos conectamos con jacob. por ssh, buscamos la flag en su escritorio.


***

## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 


Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.


También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


### User Pivoting

Sudo -l, nos dice que **kratos** puede ejecutar un script bash sin nesesidad de proprocionar contraseñas.


![list](/assets/img/attack/21.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/attack/22.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
El script ejecuta una bash asi que  consegumos una shell como **kratos**.


![list](/assets/img/attack/24.png){:.lead width="800" height="100" loading="lazy"}


sudo -l nos dice que  root pude ejecutar **/usr/sbin/cppw** sin nesesidad de proprcionar contraseñas, pero esto no esta en GTFObins asi que debemos ver  la ayuda, que nos dice que **/usr/sbin/cppw** se utiliza para cambiar la contraseña de un usuario en sistemas UNIX/Linux.


![list](/assets/img/attack/25.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/attack/26.png){:.lead width="800" height="100" loading="lazy"}


Para consegurlo con openssl passwd creamos una contraseña sencilla, copiamos en **/etc/passwd** ya que si lo podemos ver pero lo llevamos a nuestra maquina le  incrustramos la clave que generamos la subimos al servidor y usamos **/usr/sbin/cppw** y ya somos root.

![list](/assets/img/attack/27.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/attack/28.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ya podemos buscar la flag en elescritorio de root.

***

```bash
🎉 Felicitaciones ya has comprometido Attack de Hack My VM 🎉
```
{:.centered}

***

Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}
