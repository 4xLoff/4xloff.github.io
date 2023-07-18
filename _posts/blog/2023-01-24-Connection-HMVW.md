---
layout: post
title: "Write Up Connection. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,HMVM,Reverses-Shell,PHP,SMB,SUID,GTFObins,Reconnaissance,Protocols,eJPTv2]
image:
  path: /assets/img/connection/connection.png
---

***

<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### Nmap


```bash
nmap --open -p- -Pn -n -T4 -vvv -n 198.168.100.46 -oN allports
```


![list](/assets/img/connection/2.png){:.lead width="800" height="100" loading="lazy"}



### Services and Versions

```bash
nmap -sVC -Pn -n -p22,80,139,445 198.168.100.46 -oN target
```

![list](/assets/img/connection/3.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Expltation


### SMB TCP-445

Aunque tenemos algunos puertos en el pueto 22 no podemos hace nada de momento, ni tampoco el puerto 80 porque tiene la pagina de apache por defecto, asi que nos vamos a concentrar en el puerto smb, sin requerir una contraseña. 


![list](/assets/img/connection/4.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Web.


Nos enfocaremos en el directorio **share** al cual tenemos acceso. Dentro de este directorio encontramos el archivo **index.html** por defecto, que ya habíamos visualizado previamente a través de HTTP es de apache. 


Nuestro objetivo es subir una shell inversa de PHP, Configuraremos la shell con nuestra dirección IP y el puerto deseado, y le daremos permisos de ejecución mediante el comando `chmod +x php-reverse-shell.php`. Luego, procederemos a cargar la shell en el servidor.  



![list](/assets/img/connection/5.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Archivo index y subimos la php-reverse-shell.php.


![list](/assets/img/connection/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Nos ponemos a la escucha con netcat y enecutamos en el navegador `http://198.168.100.46/php-reverse-shell.php`.


Obtenemod una shell como **www-dat** y podemos buscar la flag en su escritorio.


***

## Escalation Privileges

Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 

Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.

También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


```bash
find / -type f -perm -4000 -ls 2>/dev/null
```


![list](/assets/img/connection/7.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Podemos notar la presencia del ejecutable **gdb** en el sistema, el cual podemos utilizar para obtener privilegios de root, aprovechando las técnicas descritas en el sitio web [GTOFBins].

[GTOFBins]: https://gtfobins.github.io/gtfobins/gdb/#suid



![list](/assets/img/connection/8.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Las flag esta el escritorio de root.


***

```bash
🎉 Felicitaciones ya has comprometido Connection de Hack My VM 🎉
```
{:.centered}

***

Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}
