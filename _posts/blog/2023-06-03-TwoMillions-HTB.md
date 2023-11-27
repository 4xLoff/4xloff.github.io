---
layout: post
title: "Write Up TwoMillions. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,HTB,Web,Command-Execution,JavaScript,PHP,RCE,Lateral-movement,Misconfiguration,Cracking,Protocols,CVE,Kernel,Reconnaissance,Real,eJPTv2,eWPT]
image:
  path: /assets/img/twomillions/twomillions.png
---


---

<!--more-->

1. this ordered seed list will be replaced by the toc
   {:toc}


---

## Reconnaissance


### nmap


```bash
nmap -p- --open --min-rate 5000 -n -vvv -Pn -sS 10.10.11.221 -oA allports
```


![list](/assets/img/twomillions/1.png){:.lead width="800" height="100" loading="lazy"}


### Services and Versions


```bash
nmap -sCV -p22,80 10.10.11.221 -oN target
```


![list](/assets/img/twomillions/2.png){:.lead width="800" height="100" loading="lazy"}


---

## Vulnerability Analysis and Exploitation


### HTTP TCP-80


Con nmap no conseguimos mucha informacion execpto un dominio qu es `2million.htb`, el cual vamos a introducir en el archivo /etc/hosts y vamos a hacer un reconocimiento para ver de que podemos aprovecharnos.


![list](/assets/img/twomillions/3.png){:.lead width="800" height="100" loading="lazy"}


Explorando la web parece ser la verssion antigua de la plataforma asi que esto pude ser muy divertido, husmeando unpoco encontramos que si nos quisieramos unir nos pide un codigo de invitacion y apatrte tambien un formulario de login.


![list](/assets/img/twomillions/4.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Web antigua.


![list](/assets/img/twomillions/5.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Formulario invitacion.


![list](/assets/img/twomillions/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Formulario login.


Luego de investigar en interne como hacele ya que otras formas no dieron fruto aprte que fuzzeando por directorios hay uno llamdo `/api`, vamos a ir por este camino,pero no encontramos nada, parece que hay una forma y es con un codigo de invitacion pero no lo tenmos pero viendo el codigo de la pagina podemos ver el cogigo que lo genera y vamos a ver si nos podemos aprovechas de eso de alguna forma.


![list](/assets/img/twomillions/7.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/twomillions/8.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Codigo de forma mas legible.


Aunque el codigo este mas legible el hecho que use la funcion eval, remplace caracteres y minimize la utilizacion de los espacios a mi se me ahace sosopechoso, me da apensar que el codigo esta ofuscado y para eso vamos a usar [js-beauty], para ver si podemos ver que es lo que en verdad esta en este codigo.


[js-beauty]: https://beautifier.io/


![list](/assets/img/twomillions/9.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Vemos el verdadero codigo con una ruta que es `/api/v1/invite/how/to/generate`.


Como vimos hay dos funciones una que verifica el codigo de invitacion y otra que genera un codigo de invitacioy de este ultimo nos vamos a aprovechar.


![list](/assets/img/twomillions/10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Vemos que esta data en cifrada en ROT13.


Con [cyberchef] vamos a decifrar esto **Va beqre gb trarengr gur vaivgr pbqr, znxr n CBFG erdhrfg gb /ncv/i1/vaivgr/trarengr"**que en verdad pone **In order to generate the invite code, make a POST request to /api/v1/invite/generate** y volvemos a ver de que se trata esta ruta.


![list](/assets/img/twomillions/11.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Desifrado de data.


![list](/assets/img/twomillions/12.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Hurra tenemos codigo de invitacion que esta en base pero decifrando queda asi `LLOK5-3853A-91EJ6-VODPH`.


Ya con eso nos podemos regitrar, y nos logueamos y ya estamos dentro del dashboar y ahora tratamos de buscar la forma de ganar una revershell o algo para ejecutar coamdos.


![list](/assets/img/twomillions/12.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Inicio de sesions.


![list](/assets/img/twomillions/13.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Dashboard.


Ahora tratando de buscar alguna forma de ganar un shell o algo y enumerando por bastante tiempo en la fucion de access podemos generar una vpn, y este pueder ser un posible vector asi que vamos a explorar esta idea, lo que se me ocurrio en princio fue la clave privada de la vpn seria para conectarme por ssh pero no porque la vpn es genrada para nuestro usuario, el que creamos nosotros o algo asi pero no, ademas tampoco tenemos usuarios asi que no hay con que usar por loque hay que probar otras cosas, como las cookies, desde que fuzze con ffuf la web ya aprecia un direcctorio api ya lo habiam mecionado porque me llamo la atencion pero igualque antes ahora tambien `curl -v 2million.htb/api` nos muestra que las cabeceras nos estab rechazando `HTTP/1.1 401 Unauthorized` , esa cookie ademas es dinamica cambia cada vez, pero que pasa si hace ruta le metemos la cookie de la peticionde generar la vpn porque aunque la vpn es la que genera para nuestro usuario pero algien genera la peticion y ese es el sitema del servidor asi que haremos eso, con curl o burpsuite lo que mejor se acomode.


![list](/assets/img/twomillions/14.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Unauthorized.


![list](/assets/img/twomillions/15.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Este ya nos da codigo de estado 200 y una ruta `/api/v1` y vamos a seguir asi hasta ver a donde nos lleva.


![list](/assets/img/twomillions/16.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Aqui vemos que podemos hacer varias cosas como check si un usuatrio exites, generar una vpn,y actualizar.


![list](/assets/img/twomillions/17.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Este nos da info que hay data message y es porque admin no existe aun.


![list](/assets/img/twomillions/18.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
No podemos crear vpn admin debemos actualizar primero.


Pero hata ahora solo hemos probado GET para check usuario, que ya no nos lleva a nada pero nos falta POST, para crear admin y put para actualizarlo.


![list](/assets/img/twomillions/19.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ya no nos da errores.


Como es por el metodo PUT debemos agrgarle la cabecera `--header "Content-Type: application/json"` para ver que pone **Missing parameter: email** deberemos agregarlo.


![list](/assets/img/twomillions/21.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Falta el Email y debemos usar el mismo que nos logueamos.


Si quremos agrgarlo nos dice que nos falta un parametro que es `is_admin` asi que lo agregamos, y luego tambien nos dice que debemos agregarle un valor de 0 o 1 vamos a poner 1.


![list](/assets/img/twomillions/22.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Se ha actualizado la informacion.


Ya podemos volver a lo de antes podemos verificat eso se hacia con el metodo GET cuando ponia message false ahora deberia poner true.


![list](/assets/img/twomillions/23.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Admin correctamente check `true`.


Ahora toca ir a generar la vpn, pepro ya digo que igual que hacia flata el email ahora falta el username y debemos hacer lo mismo para username.


![list](/assets/img/twomillions/24.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Esto creara la vpn.


Ahora la vpn es de administradores pero aun no sabemos usuarios asi que las **private_key** no nos serviran de nda por lo que debemos buscar otro vector lo que se ocurre es aprovechanos de que en json se pueden meter parametros ya que no parece que esten bien filtrados.


![list](/assets/img/twomillions/25.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Funciono podemos ejecutar comados e injectaremos codigo para otorgarnos una reverse-shell.


![list](/assets/img/twomillions/26.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Obtenemos una shell como `www-data`.


### Lateral Movement


Ya sea buscando manualmente o subimos **linpeas** podemos encontrar la contraseña `SuperDuperPass123` que vamos a usar para conectarnos por ssh al usuario admin.


![list](/assets/img/twomillions/27.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Contraseña `SuperDuperPass123` en `/var/www/html/.env`.


![list](/assets/img/twomillions/28.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Nos conectamos por ssh.


---

## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada.


Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.


También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


Despues de algun timepo y usar **Linux-Smart-Escalation** vemos que admin tiene mail asi que vamos a ver de que trata.


![list](/assets/img/twomillions/29.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Se trata de un correo con aviso de seguridad sobre una vulnerabilidad **OverlayFS / FUSE**, el cual vamos a explotar y vamos a buscar en internet de que se trata.


Investigando en internet vemos que con el coamdo `uname -r` nos muestra la version del kernel si es 5.15.70-051570-generic podremos ejecutar el ataque, y encontramos una forma de explotar [CVE-2023-0386], solo es cuestion de clonarnos el repositorio comprimirlo y subirlo al servidor.


[CVE-2023-0386]: https://github.com/xkaneiki/CVE-2023-0386


```shell
make all
./fuse ./ovlcap/lower ./gc &
./exp
```


![list](/assets/img/twomillions/30.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ya podemos, buscar la flag en el escritorio del root.


---

```shell
🎉 Felicitaciones ya has comprometido TwoMillions de HackTheBox 🎉
```


{:.centered}


---

Back to [Certification eJPTv2](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}


---

Back to [Certification eWPT](2023-07-04-Road-to-eWPT.md){:.heading.flip-title}
{:.read-more}


---

Back to [Certification OSCP](2023-07-10-Road-to-OSCP.md){:.heading.flip-title}
{:.read-more}
