---
layout: post
title: "Write Up Agent-Sudo. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,THM,FTP,SSH,SUDO,GTFOBins,Steganography,Weak-Credentials,Brute-Forcing,Reconnaissance,Misconfiguration,zip2john,Fuzzing-Web,eJPTv2,eWPT]
image:
  path: /assets/img/agent-sudo/agent.jpg
---

***

<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### Nmap


```bash
nmap --open -p- -Pn -n -T4 -vvv -n 10.10.253.135 -oN allports
```


![list](/assets/img/agent-sudo/1.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions

```bash
nmap -sVC -Pn -n -p21,22,80 10.10.253.135 -oN target
```

![list](/assets/img/agent-sudo/2.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Exploitation


### HTTP TCP-80


Aunque tenemos tres puertos, en el puerto 21 y 22 no podemos hace nada de momento, asi que nos vamos a concentrar en el puerto 80,pero solo tiene un mensaje un mensaje del agente R que dice **que uses tu codigo para acceder ala web** si agente R es el code name de otro agente es posible pensar que otra letra sea el code name  para ingresar y calaro la otra pista es el nombre de la amaquina y el los nombres de los agentes por lo que vamos a fuzzerar el campo del **User-Agent** esto lo podemos hacer con con **Curl** o **Burpsuite**.


![list](/assets/img/agent-sudo/3.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Mensaje de agente R.

```bash
curl -A "C" -L http://IP-SERVIDOR/
```


{:.note}
Yo lo hice con Curl y aqui en esta pagina vemos el mensaje **Attention chris, Do you still remember our deal? Please tell agent J about the stuff ASAP. Also, change your god damn password, is weak!**, de aqui sacamos el user chris.


Ya con esto vamos a usar Hydra para bruteforcear el servicio ssh pero eso no sirvio asi que lo mismo para el servicio ftp.


![list](/assets/img/agent-sudo/4.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La contraseña para chris es **crystal**.


Dentro del servicio nos encontramos tres archivos u nota y imagenes. que las decargamos a nuestra maquina para husmearlas y ver algunposible vector, el el archivo To_agenteJ.txt pone **Dear agent J,All these alien like photos are fake! Agent R stored the real picture inside your directory. Your login password is somehow stored in the fake picture. It shouldn't be a problem for you. From,Agent C**, por lo que vamos a probar a investigar las imagenes por pesos de las mismas me hac pensar que continem informacion por eso vamos a usar exiftool, stegeek, binkwak, steghide, para taratar de estraer toda la inforcion posible. 


![list](/assets/img/agent-sudo/5.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Descargamos los tres archivos.


![list](/assets/img/agent-sudo/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con stegeek a cute_alient.jpg obtenemos una contraseña **Area51**.


![list](/assets/img/agent-sudo/2023-07-03_15-20.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con binkwalk obtenemos un archivo.zip que vamosa de despaquetar y nos pide una contraseña probamos Area51 pero no es , asi que probamos usar  zip2john para obtener la contraseña.


![list](/assets/img/agent-sudo/7.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La contraseña del archivo.zip es alien.


En el interio hay dos archivo una imagen y una nota que pone **Agent C,We need to send the picture to 'QXJlYTUx' as soon as possible!.By,Agent R**, eso esta en base64, y si desencriptamos pone Area51 asi que ya nos ahorramos esto, por otra parte la imagen.


![list](/assets/img/agent-sudo/8.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La contraseña es Area51.


![list](/assets/img/agent-sudo/9.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con steguide  a cutie_alient.jpg obtenemos la contraseña para ssh que es **hackerrules!**.


![list](/assets/img/agent-sudo/10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Obtenemos shell como james que es un nombre recurente en las notas, la flag esta en su escritorio.


***

## Escalation Privileges

Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 

Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.

También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


![list](/assets/img/agent-sudo/11.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con **sudo -l** vemos que root vemos que que cualquier usuario puede ejecutar `(ALL, !root) /bin/bash` pero no sabemos que es eso asi qye investigamnos en internet y encontramos un [exploit].

[exploit]: https://blog.aquasec.com/cve-2019-14287-sudo-linux-vulnerability


{:.note title="Attention"}
En esta situación, sudo no realiza una verificación de la existencia de la identificación de usuario especificada y se ejecuta con una identificación de usuario aleatoria. Por lo tanto, al utilizar **sudo -u#-1 /bin/bash**, se obtiene un resultado de 0, que corresponde a la identificación de usuario root, ya solo buscamos la flag en el escritorio del mismo.


Hay una ultima imagen el el directorio de user trate de aplicarle la alguinas de las tecnicas vista pero no escontre nada solo es la imagen de un alien y tiene que ver con la pregunta del cuestionario Caso Roswell.


***

```bash
🎉 Felicitaciones ya has comprometido Agent-Sudo de Try Hack My 🎉
```
{:.centered}

***

Back to [Certification eJPTv2](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}

***

Back to [Certification eWPT](){:.heading.flip-title}
{:.read-more}
