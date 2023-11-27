---
layout: post
title: "Write Up CozyHosting. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,HTB,Cookie,Cookie-Manipulation,Cookie-Hijacking,Command-Injection,Java,PostgreSQL,John,Hashes,Cracking,SUDO,GTFOBins,Protocols,Reconnaissance,eJPTv2]
image:
  path: /assets/img/cozy/cozy.png
---

---

<!--more-->

1. this ordered seed list will be replaced by the toc
   {:toc}

---

## Reconnaissance


### nmap

```bash
nmap -p- --open --min-rate 5000 -n -vvv -Pn -sS 10.10.11.230 -oA allports
```

![list](/assets/img/cozy/1.ong){:.lead width="800" height="100" loading="lazy"}


### Services and Versions


```bash
nmap -sCV -p11,80 10.10.11.230 -oN target
```

![list](/assets/img/cozy/2.ong){:.lead width="800" height="100" loading="lazy"}


---


## Vulnerability Analysis and Exploitation


### HTTP TCP-80


Aunque buscamos las tecnologuias con whatweb no encontramos nada solo el domidion `cozyhosting.htb` que agregaremos al `/etc/hosts` y como no tenemos nada aun vamos a inspeccionar la pagina web.


![list](/assets/img/cozy/3.ong){:.lead width="800" height="100" loading="lazy"}


Explorando la web no encontramos nada asi que vamos a fuzzear por direcctorios primero y luego por subdomios si no conseguimos nada, esamos con suerte porque fuzzeando encontramos una ruta llamada `/actuator/sessions` que contiene un nombre de usuario y un hash aparentemente, pero son dinamicos aparentemente.


![list](/assets/img/cozy/5.ong){:.lead width="800" height="100" loading="lazy"}


{:.note}
El usuario es `kanderson`.


![list](/assets/img/cozy/6.ong){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/cozy/7.ong){:.lead width="800" height="100" loading="lazy"}


{:.note}
La cookie es dinamica.


Con ese hash lo que podemos hacer es tratar es de editar la cookie y trasformarnos en otro usuario.


![list](/assets/img/cozy/8.ong){:.lead width="800" height="100" loading="lazy"}


{:.note}
Editamos la cookie.


![list](/assets/img/cozy/9.ong){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ahora somos el usuario ´K. Anderson´.


Por lo pronto vamos ha ver que podemos hacer aki para ganar acceso al servidor y vemos que pone **Para que Cozy Scanner se conecte, la clave privada que recibiste al registrarte debe incluirse en el archivo .ssh/authorized_keys de tu host.**, lo que se me ocurre es como pide el hostanme y un usuario probar eso mismo ya que tenemos las dos cosas y para eso vamos usar el proxy de burpsuite.


![list](/assets/img/cozy/10.ong){:.lead width="800" height="100" loading="lazy"}


{:.note}
Lo dicho es la funcion de ssh.


![list](/assets/img/cozy/11.ong){:.lead width="800" height="100" loading="lazy"}


{:.note}
Podemos ejecutar comandos es hora de mandarnos una reverse-shell.


![list](/assets/img/cozy/13.ong){:.lead width="800" height="100" loading="lazy"}


{:.note title="Attention"}
El `${IFS}`, se está utilizando para representar un espacio en blanco.


Creamos un archivo llamado shell.sh donde vamos a mandarnos el codigo para mandarnos una bash desde el servidor con curl vamos obtener la reverse shell.


![list](/assets/img/cozy/12.ong){:.lead width="800" height="100" loading="lazy"}


{:.note}
Archivo shell.sh.


![list](/assets/img/cozy/14.ong){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/cozy/15.ong){:.lead width="800" height="100" loading="lazy"}


{.:note}
Ya somos el usuario `app`.


Enumerando un poco en contramos un `archivo.jar` que vamos a deenpaquetar en el cual hay credenciales.


![list](/assets/img/cozy/16.ong){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/cozy/17.ong){:.lead width="800" height="100" loading="lazy"}


{:.note}
Son credenciales de la base de datsos postgres `Vg&nvzAQ7XxR`.


Econtramos unos hashes detro de la base de datos que vamos a crackear con john the ripper.


![list](/assets/img/cozy/18.ong){:.lead width="800" height="100" loading="lazy"}


{:.note}
Hashes.


![list](/assets/img/cozy/20.ong){:.lead width="800" height="100" loading="lazy"}


{:.note}
Encontramos una contraseña de pero ese usuario no hay asi que reutilisemos con el usuario josh y buscamos la credenciales en su escritorio.


---

## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada.


Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.


También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


Con **sudo -l**, puedes ver que tenemos permisos para el comando ssh como root y despues de buscar en [GTFObins], y con podemos convertirnos en root.


![list](/assets/img/cozy/19.ong){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ya podemos, buscar la flag en el escritorio del root.


---


```shell
🎉 Felicitaciones ya has comprometido CozyHosting de HackTheBox 🎉
```


{:.centered}


---


Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}


