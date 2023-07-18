---
layout: post
title: "Write Up BackendTwo. "
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Linux,HTB,JWT,API,RCE,API-Enumeration,Abusing-API,Information-Leakage,eWPT,eWPTxv2,OSWE] 
image:
  path: /assets/img/backend%20two/Arch-2022-05-08-14-43-22.png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
nmap -p- --open --min-rate 5000-sS -n -vvv -Pn 10.10.11.162 -oA allports
```

![list](/assets/img/backend%20two/Arch-2022-05-08-14-53-08.png){:.lead width="800" height="100" loading="lazy"}


### Services and Versions


```bash
nmap -p22,80 -sV -sC 10.10.11.162 -oN target
```


![list](/assets/img/backend%20two/Arch-2022-05-08-15-05-38.png){:.lead width="800" height="100" loading="lazy"}



***

## Vulnerability Analysis


### HTTP TCP-80


Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros.e ispeccionamos la web, ademas de las tecnologias de la ip ataves de la terminal o via  web esto lo hacemos con wapalizzer o whatweb pero no encontramos nada por lo que vamos a inspeccionar la web ademas vamos a fuzzear.


![list](/assets/img/backend%20two/Arch-2022-05-08-15-08-46.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/backend%20two/Arch-2022-05-08-15-16-18.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Encontramos los directorios `/api/` y `/docs`.


Si vemos`/api` en dentro hay `/v1`.


![list](/assets/img/backend%20two/Arch-2022-05-08-15-16-18.png){:.lead width="800" height="100" loading="lazy"}


Dento de admin ay un error de autorizacion.


![list](/assets/img/backend%20two/Arch-2022-05-08-15-17-22.png){:.lead width="800" height="100" loading="lazy"}


Dentro de users no hay nada lo que hace sospechar que es una carpeta asi que vamos hacer un `/users/1`.


![list](/assets/img/backend%20two/Arch-2022-05-08-15-17-46.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/backend%20two/Arch-2022-05-08-15-17-52.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Si provamos con `/users/2`.


![list](/assets/img/backend%20two/Arch-2022-05-08-15-18-35.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
O `/users/12`.


![list](/assets/img/backend%20two/Arch-2022-05-08-15-28-44.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Como hay 12 usuarios vamos hacer un comando que nos estraiga los correos de los doce usuarioa y nos los muestre por pantalla.


Dea ahi tambien notamos un dominio `backendtwo.htb` que vamos a meter en `/etc/hosts`, y vamos a volver a fuzzear en la ruta `/api/v1/users/FUZZ` porque talves no solo exiatan numero tambien archivos o carpetas.


![list](/assets/img/backend%20two/Arch-2022-05-08-15-48-01.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ademas encontramos uno archivos `login` y `singup` con el metodo `POST`.


![list](/assets/img/backend%20two/Arch-2022-05-08-15-49-23.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Lo ispeccionamos con curl.


Ahora vamos a registrarno y a loogearnos esto nos devuleve un JWT que vamos a copiar para en [JWT].io recomponerlo para que crear el de root.


![list](/assets/img/backend%20two/Arch-2022-05-08-16-11-34.png){:.lead width="800" height="100" loading="lazy"}


[JWT.io]:(https://jwt.io/)


![list](/assets/img/backend%20two/Arch-2022-05-08-16-02-08.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Lo ejaremos de momento ya que no tenemos el secreto.


Nos vamosa autenticar con burpsuite.


![list](/assets/img/backend%20two/Arch-2022-05-08-16-11-29.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Debemos agregar la cabecera `Authorization Beader:<JWT>`.


Ahora ya podemos meternos a la ruta `/docs`.


![list](/assets/img/backend%20two/Arch-2022-05-08-16-17-43.png){:.lead width="800" height="100" loading="lazy"}


Despues de hacer muchas pruebas y Husmear por todos lados conseguimos la flag pero no acceso a la maquina todo desde la web.


![list](/assets/img/backend%20two/Arch-2022-05-08-16-32-32.png){:.lead width="800" height="100" loading="lazy"}


Hay una vulnerabilidad que se llama mass asignament attack con el cual vamos a cambiar el `is_superuser: false` a  `is_superuser: true`, esto se hace en `Edit profile`, una ves cambiado debemos reelogearnoS en la pestaña de `autorized`.


![list](/assets/img/backend%20two/Arch-2022-05-08-16-41-25.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Esta en false.


![list](/assets/img/backend%20two/Arch-2022-05-08-16-48-28.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ahora esta en true.


![list](/assets/img/backend%20two/Arch-2022-05-08-16-48-48.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Conseguimos la flag del usuario de bajos privilegios.


Ya como somo superusuario podemos ver archivos del sistema.


![list](/assets/img/backend%20two/Arch-2022-05-08-18-00-53.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Vemos el usuario `htb`.


de la misma forma vamo a curiosear las rutas `/proc/net/tcp` que nos muestra los puerto que estan abiertos luego de pasarlos de hexadeimal a decimal.


![list](/assets/img/backend%20two/Arch-2022-05-08-18-15-47.png){:.lead width="800" height="100" loading="lazy"}


```bash
echo "<PORTS>" | sort -u | while read port; do echo "[+] Puerto $port" -> $(0x$port); done
```


{:.note}
Encontramos el `22,53,80,39560,43888,43890,43896,43898`.



De la misma forma que antes pero ahora atraves de la terminal vemos el proceso que esta corriendo la `API_KEY` con curl.


![list](/assets/img/backend%20two/Arch-2022-05-08-18-15-47.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La `API_KEY=68b329da9893e34099c7d8ad5cb9c940`.


De lo anterio no dice que en la ruta `/home/htb/app/main.py` esta el secreto.


![list](/assets/img/backend%20two/Arch-2022-05-08-19-00-34.png){:.lead width="800" height="100" loading="lazy"}


Ahora vamos a reconstruir el jwt ya que el api_key es el secreto y esto vamos hacer con python.


![list](/assets/img/backend%20two/Arch-2022-05-08-19-09-34.png){:.lead width="800" height="100" loading="lazy"}


Cambimaos la JWT en el coamdo que estabamos utilizando hasta ahora tambien le agregamos `-d` para agregarle el campo file pero tambien podemos agrgarle el campo `debug a true`.


![list](/assets/img/backend%20two/Arch-2022-05-08-20-06-20.png){:.lead width="800" height="100" loading="lazy"}


Ahora como podemos ver archivos de site ma vamos a ver y decargarnos el script en pyto que esta en la ruta /home/htb/app/api/v1/endpoints/user.py, ispeccionando el codigo y vamos a usar [cyberchef] para no tener problemas con comillas ni eso.


[cyberchef]:(https://gchq.github.io/CyberChef/)


![list](/assets/img/backend%20two/Arch-2022-05-08-20-34-24.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Remplazamos las doble comillas.


![list](/assets/img/backend%20two/Arch-2022-05-08-20-34-29.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Remplazamos los saltos de linea.


![list](/assets/img/backend%20two/Arch-2022-05-08-20-34-32.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Reemplazamos als comillas simples.


![list](/assets/img/backend%20two/Arch-2022-05-08-20-43-10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Y eso pegamos en file  y debemos esatr a la escucha en el puerto 443.


{:.note}
La flag del usuari de bajos privileguios se encuentra en el escritorio del usuario `htb`.


***

## Explotation


Siempre es bueno ejecutar `LimEnum` Y `pspy`, para que podamos enumerar más vulnerabilidades que permitan elevar nuestros privilegios al usuario "root".


Si hacemos un `cat auth.log` vemos la contraseña de `htb`.


![list](/assets/img/backend%20two/Arch-2022-05-08-21-01-55.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La contraseña es **1qaz2wsx_htb!**.


Haciendo `sudo -l` se ejecuta un juego del ahorcado que solo tenemos seis oprtunidades para acertar y buscando por PAM nos damos cuenta que hay una ruta archivo `pam_wordle.so` que con string tiene una ruta oculta `/opt/.words` y la palabra clave es `ippsec`, entonde hacemos sudo su ya podemos, buscar la flag en el escritorio del root.


***

```shell
🎉 Felicitaciones ya has comprometido BackendTwo de HackTheBox 🎉
```
{:.centered}
***

Back to [Certification eWPT](){:.heading.flip-title}
{:.read-more}

***
Back to [Certification OSCP](){:.heading.flip-title}
{:.read-more}

***
Back to [Certification OSWE](){:.heading.flip-title}
{:.read-more}



