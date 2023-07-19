---
layout: post
title: "Write Up Visions. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,HMVM,SSH,SUDO,Hydra,GTFOBins,Reconnaissance,Brute-Forcing,ssh2john,id_rsa,Protocols,eJPTv2]
image:
  path: /assets/img/visions/visions.jpg
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

![list](/assets/img/visions/1.png){:.lead width="800" height="100" loading="lazy"}


### Nmap


```bash
nmap --open -p- -Pn -n -T4 -vvv -n 198.168.1.40 -oN allports
```


![list](/assets/img/visions/2.png){:.lead width="800" height="100" loading="lazy"}



### Services and Versions


```bash
nmap -sVC -Pn -n -p22,80 198.168.1.40 -oN target
```

![list](/assets/img/visions/3.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Expltation


### HTTP TCP-80


Con el puerto 22 no podemos hacer nada asi que vamosa a husmear el puerto 80,  esta vacia pero vamos a ver el codigo fuente y hay una nota que pone **"Only those who can see the invisible can do the impossible.You have to be able to see what doesn't exist.Only those who see the invisible can see what is not there.-alicia"**. de hay ya tenemos un usuario pero banado hasta el fina de la pagina hay una etciqueta html que esta cargando una imagen.


![list](/assets/img/visions/4.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Usuario **alicia**.


![list](/assets/img/visions/5.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Descargamos la  imagen y tratamos de ver si tiene alguna informacion oculta.


Usando exiftoll vemos que continene unas credenciales **pw:ihaveadream** que vamos a usar para conectarnos como alicia.


![list](/assets/img/visions/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La contraseña es valida para alicia.


![list](/assets/img/visions/7.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Nos conectamos por ssh..


***

## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 


Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.


También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.

### User Pivoting alicia to emma


Sudo -l nos dice que cualquier usuario **emma** tiene privilegios para ejecutar el comando **/usr/bin/nc**, sin requerir una contraseña.

![list](/assets/img/visions/8.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Nos ponemos a la escucha con necat y ya somos emma.


### User Pivoting emma to sophia


Despues de subir  y probar alguna formas de escalar privileguios ya que la nota que esta en el  escritoio pone **I cant help myself**, no nos da pista de nada, pero esta maquina se resuelve con la imagen del principio hay que subirle la **exposision** con [pinetools] para ver las credenciales.

[pinetools]: https://pinetools.com/change-image-exposure

![list](/assets/img/visions/9.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Las credenciales encontradas son **sophia:seemstoimpossible**, y nos conectamos como **sophia** por ssh.


### User Pivoting sophia to isabella


Sudo -l nos dice  todos los usuarios pueden ejecutar el comando **cat** en el archivo **/home/isabella/.invisible** sin necesidad de proporcionar una contraseña.


![list](/assets/img/visions/11.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/visions/12.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Nos conectamos como **isabella** por ssh pero no es tan simple porque nos falta la palabra clave asi que vamos a usar ssh2john e hydra.


![list](/assets/img/visions/13.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/visions/14.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Nos conectamos como **isabella** por ssh con la pass **invisible**.


sudo -l, nos dice que **emma** puede ejecutar el comando **man**. si proporcionar contraseña pero esto no nos sirve de nada por ya fuimos emmas si hacemos eso bajaremos de privileguios debemosmbuscar otra forma.


La primera ves que vi esto me parecio raro porque para crear un link simbolico se debe tener permisos de escritura, asi que esto es un salto de fe , lo que ocurre esque no tenemos porque saber que tenemos este permiso pero la maquina esta configurada asi en tonces hacemos `ln -s /root/.ssh/id_rsa` y, como de antes dabemos que podemo que con el usuario Sophia, leer su contenido. 


![list](/assets/img/visions/16.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/visions/17.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Nos conectamos como **root** y ya podemos buscar la flag en ele escritorio de root.


***

```bash
🎉 Felicitaciones ya has comprometido Visions de Hack My VM 🎉
```
{:.centered}

***

Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}
