---
layout: post
title: "Write Up Gallery. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,THM,SUDO,GTFOBins,PHP,Reverse-Shell,Leaked-Information,Misconfiguration,Reconnaissance,Fuzzing-Web,eJPTv2,CMS,CVE,SQLi,SQL]
image:
  path: /assets/img/gallery/gallery.png
---

***

<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### Nmap


```bash
nmap --open -p- -Pn -n -T4 -vvv -n 10.10.161.189 -oN allports
```


![list](/assets/img/gallery/1.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions

```bash
nmap -sVC -Pn -n -p80,8080 10.10.161.189  -oN target
```

![list](/assets/img/gallery/2.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Exploitation


### HTTP TCP-8080


El escaneo revela 2 puertos abiertos el puerto 80 y el puerto 8080 de momento con este no vamos hacer nada. El puerto 80 está ejecutando Apache y te redirecciona al 8080 asi que ya nos ahorramos un pueto,asi que procedemos fuzzerar con FFuf y encontramos el directorio /gallery/ pero me acorde que este es un **CMS Simple Image Gallery**, podemos buscar un [exploit] por internet o con searchsploit.


![list](/assets/img/gallery/7.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/gallery/3.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/gallery/4.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Esto es nod da la url vulnerable a injeccion de comandos, aqui ya nos ponemos ala escucha con netcat y listo.


{:.note title="Attention"}
Pero como nos guata aprender vamos hacerlo de la forma manual tambien que en verda hay dos una subiendo una [php-reverse-shell.php] y los mismo ponernos a la escucha con netcat u la otra que la de **Injeccion SQL**, Durante la exploración, al visitar **/gallery/**, nos encontramos con una página de inicio de sesión.

![list](/assets/img/gallery/3.png){:.lead width="800" height="100" loading="lazy"}


Probamos algunas contraseñas predeterminadas, pero no tuvimos éxito. Luego, probamos la sintaxis básica de SQLi y tuvimos éxito. En el campo de nombre de usuario, ingresamos:

```bash
admin'or 1=1 -- -
```


![list](/assets/img/gallery/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Dejamos en blanco el campo de contraseña y entramos en el dashboard.


[php-reverse-shell.php]: https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php


Una ves que somo www-data vemos que podemos entra a un directorio de mike_backups pero es un **rabbithole** que no nos lleva a ningun lado jejej,continuemos, más tarde encontré el archivo **.bash_history**, y aqui esta la contraseña de **mike**, tambie encontre un credenciales en un archivo de configuracionde base de datos.


![list](/assets/img/gallery/8.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
RabbitHole.


![list](/assets/img/gallery/9.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La contraseña de mike es **-lb3stpassw0rdbr0xx** y podemos buscar la flag en el escritorio.


## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 

Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.

También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


Vemos que esta abierto puertos y esta abierto  el pueto de **MySql** asi que nos vamos a conectar a ese servicio y aunque obtenemos un hash del usuario admin es otro **rabbithole**.



![list](/assets/img/gallery/10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Credenciales Backup bases de datos mysql.


![list](/assets/img/gallery/11.png){:.lead width="800" height="100" loading="lazy"}


Al ejecutar **sudo -l**, encontramos lo siguiente, se muestra que el usuario Mike puede ejecutar el archivo /opt/rookit.sh como sudo, cualquiera pensaria que esto nos dara la shell de root pero no qui debemos uar nano y para eso vamos utilizar **GTFObins** y listo.


![list](/assets/img/gallery/12.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Permisos SUDO.


![list](/assets/img/gallery/13.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Esto en el mismo nmap nos da la shell de root ya es ver la flag con **cat /root/root.txt**.

***

```bash
🎉 Felicitaciones ya has comprometido Gallery de Try Hack My 🎉
```
{:.centered}

***

Back to [Certification eJPTv2](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}


