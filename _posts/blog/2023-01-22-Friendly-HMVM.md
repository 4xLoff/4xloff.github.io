---
layout: post
title: "Write Up Frendly. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,HMVM,Reverse-Shell,PHP,FTP,SUDO,GTFOBins,Weak-Credentials,Default-Credentials,Misconfiguration,Reconnaissance,Protocols,eJPTv2]
image:
  path: /assets/img/friendly/friendly.png
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

![list](/assets/img/friendly/1.png){:.lead width="800" height="100" loading="lazy"}


### Nmap


```bash
nmap --open -p- -Pn -n -T4 -vvv -n 198.168.1.38 -oN allports
```


![list](/assets/img/friendly/2.png){:.lead width="800" height="100" loading="lazy"}



### Services and Versions

```bash
nmap -sVC -Pn -n -p22,80 198.168.1.38 -oN target
```

![list](/assets/img/friendly/2.1.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Expltation


### FTP TCP-21

Aunque tenemos algunos puertos en el pueto 21 no podemos hace nada de momento, ni tampoco el puerto 80 porque tiene la pagina de apache por defecto, asi que nos vamos a concentrar en el puerto FTP con el usuario **anonymous**, sin requerir una contraseña, en este caso, el archivo **index.html** que aparece es la página predeterminada de Apache. Aprovecharemos esto para subir una reverse-shell.


![list](/assets/img/friendly/4.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Una vez hecho esto, procederemos a poner en escucha Netcat y ejecutar la reverse shell. Para ello,usatremos el comando `curl http://192.168.1.38/php-reverse-shell.php` (o cargaremos directamente la URL desde el navegador).


Obtenemod una shell como **www-dat** y podemos buscar la flag en su escritorio.


![list](/assets/img/friendly/5.png){:.lead width="800" height="100" loading="lazy"}



***

## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 


Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.


También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


![list](/assets/img/friendly/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Dentro del directorio private hat un archivo llamado targets.txt parece estar codificado en base64.



```bash
echo  'bsase64' | base64 -d; echo
```

![list](/assets/img/friendly/7.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Son nombres de cradores de contenido **ShellDredd**, **xerosec**, **sML** y **boyras200**.


![list](/assets/img/friendly/8.png){:.lead width="800" height="100" loading="lazy"}



Como nos dice **sudo -l** cualquiera puede usar vim, asi que utilizaremos GTFObins para obtener una shell como root.


[GTOFBins]: https://gtfobins.github.io/gtfobins/vim/#sud


![list](/assets/img/friendly/9.png){:.lead width="800" height="100" loading="lazy"}



{:.note}
Las flag esta el escritorio de root, jejje no es cierto es un troleo debemos buscarla y la pista est ahi mismo.


***

```bash
🎉 Felicitaciones ya has comprometido Frendly de Hack My VM 🎉
```
{:.centered}

***

Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}
