---
layout: post
title: "Write Up Vaccine. "
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Linux,HTB,Web,Network,Vulnerability-Assessment,Database,Injection,Custom-Applications,Protocols,Source-Code-Analysis,Apache,PostgreSQL,FTP,PHP,Reconnaissance,Password-Cracking,SUDO,SQLi,RCE,Clear-Text-Credentials,Anonymous_Guest-Access,eJPTv2]
image:
  path: /assets/img/vaccine/vaccine.png
---

***

<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance

### nmap

Utilizando **nmap**, comprobamos qué puertos están abiertos.

```bash
nmap --open -p- -Pn -n -T4 -vvv -n 10.129.155.40 -oN allports
```

![list](/assets/img/vaccine/nmap.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions

```bash
nmap -sVC -Pn -n -p21,22,80 10.129.155.40 -oN target
```

![list](/assets/img/vaccine/service.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis 

### FTP TCP-21

Tenemos tres puertos abiertos, pero nos centraremos en el puerto FTP que según nmap tiene habilitado el usuario **anonymous**.

![list](/assets/img/vaccine/ftp.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Husmeando en el servicio, encontramos un archivo llamado **backup.zip** que descargaremos con el comando **get backup.zip**.


Una vez que tenemos el archivo en nuestra máquina, al intentar descomprimirlo no podemos hacerlo porque tiene una contraseña y por el momento no tenemos ningún tipo de credenciales. Por lo tanto, nos aprovecharemos de una utilidad llamada **zip2john**.


```bash
zip2john backup.zip > hash
```


![list](/assets/img/vaccine/john.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con ese hash, usaremos **John the Ripper** para obtener la contraseña de backup.zip.


![list](/assets/img/vaccine/pass.png){:.lead width="800" height="100" loading="lazy"})


{:.note}
La clave de backup.zip es **741852963**.


Obtenemos un archivo index.html con el usuario admin y un hash encriptado en formato **MD5**, el cual vamos a descifrar utilizando una herramienta en línea llamada [Crackstation].

[Crackstation]: https://crackstation.net/


![list](/assets/img/vaccine/2023-06-18_21-52.png){:.lead width="800" height="100" loading="lazy"})


{:.note}
Hash encritado.


![list](/assets/img/vaccine/online.png){:.lead width="800" height="100" loading="lazy"})


{:.note}
La contraseña para en usuario admin es **querty789**.


### HTTP TCP-80

De primeras entrando en la web no topamos con un login que probaremos las credenciales  obtenidas, deapues de un reconocimiento a la web vemos un cambo vulnerable a **SQL injection**.


![list](/assets/img/vaccine/web2.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
El campo vulnerable es search poruq al probar alguna queri maliciosa el programa se ve afrctado **any+query' --**.


***

## Exploitation

Aunque podriaamos hacerlo de forma manual la explotacion de esta vulnerabilidad aun no tenemos los habilidades para lograrlo asi que primero vamos a usar una herramienta automatizada llamada sqlmap para ganar una shell de sql y hay mandarnos una reverse-shell estando con netcat a la ecucaha.


![list](/assets/img/vaccine/sqlmap.png){:.lead width="800" height="100" loading="lazy"}


{:.note title="Attention"}
Uso de **SQLMap** y para que funcione debemos de arrastrar la cookie del usuario admin de lo contrario no funcionara.


![list](/assets/img/vaccine/os-shell.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Shell de sql.


![list](/assets/img/vaccine/she%C3%B1%C3%B1.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Shell obtenida del usuario **postgres**, la flag esta en el escritorio del usuario.


***

## Privilege Escalation

Intentaremos encontrar la contraseña en la carpeta **/var/www/html**, ya que la máquina utiliza tanto PHP como SQL, lo que implica que debería haber credenciales en texto claro , pero no conseguimos nada, buenas practica podemos subir el binario de LinEnum,etc, pero en este caso y simpre debemos probar verificar los permisos de sudoers **SUDO**, con el comando **sudo -l**.


![list](/assets/img/vaccine/sudo.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Vemos que todo mundo puede ejecutar el binario de vi y e hala vulnerabilidad.


Hay una pagina llamada [GTFObins] que podemos buscar el binario en hay nos dicen como podemos explotarlo.

[GTFObins]: https://gtfobins.github.io/gtfobins/vi/


Primero abrimos un archivo **vi** cualquiera y com **escape + :** pegamos los comandos esto nos dara shell de root.


```bash
set shell=/bin/sh
```


```bash
shell
```


![list](/assets/img/vaccine/sh.png){:.lead width="800" height="100" loading="lazy"}


{.note}
Ya podemos buscar la flag en el escritorio de **root**.


***

```bash
🎉 Felicitaciones ya has comprometido Vaccine de HackTheBox 🎉
```
{:.centered}

***

Back to [Starting-Point](2023-02-02-Starting-Point.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}