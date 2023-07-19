---
layout: post
title: "Write Up Teacher. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,HMVM,SUDO,Hydra,GTFOBins,Log-Poisoning,Reconnaissance,Brute-Forcing,Log-Analysis,X11,Protocols,eJPTv2]
image:
  path: /assets/img/teacher/teacher.png
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

![list](/assets/img/teacher/1.png){:.lead width="800" height="100" loading="lazy"}


### Nmap


```bash
nmap --open -p- -Pn -n -T4 -vvv -n 198.168.1.14 -oN allports
```


![list](/assets/img/teacher/2.png){:.lead width="800" height="100" loading="lazy"}



### Services and Versions


```bash
nmap -sVC -Pn -n -p22,80 198.168.1.14 -oN target
```


***

## Vulnerability Analysis and Expltation


### HTTP TCP-80


Con el puerto 22 no podemos hacer nada asi que vamosa a husmear el puerto 80, pero analizando con nmap encontramos un direcctorio **/manual/** que vamos a husmear y tambien tenmosun **log.php**.


![list](/assets/img/teacher/3.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/teacher/4.png){:.lead width="800" height="100" loading="lazy"}



{:.note}
Si vemos lapagina inicial hay pone **Hi student, make this server secure please.Our first server got hacked by cool and avijneyam in the first hour, that server was just a test but this server is important becouse this will be used for teaching, if we get hacked you are getting an F**

![list](/assets/img/teacher/5.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/teacher/6.png){:.lead width="800" height="100" loading="lazy"}


La nota pone que han sido  hackeados por **avijneyam**, peroviendo el codigo fuente vemos **Yes mrteacher I will do it**, me meti afondo a fuzzear peroesun rabiithole, porque en el access.php parece estar vacío, pero al inspeccionarla, encontramos una etiqueta `<img src="">`. Esto sugiere que posiblemente se necesite enviar algún parámetro. Por lo tanto, procederé a realizar un fuzzing para explorar y probar diferentes parámetros y ver si podemos obtener más información o funcionalidad oculta.

![list](/assets/img/teacher/7.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/teacher/8.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
El parametro es **id**.


En **access.log**, a través del parámetro **id**, podemos ejecutar código PHP, y el **log.php**, podemos ver los log, que hemos escrito en **access.log**, por ultimo **clearlog.php**, borra todos los registros de **logs**, permitiendo así comenzar de nuevo con el proceso.


![list](/assets/img/teacher/9.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Tratamos de ver informacion haciendo una llamada alsitema para ver informacion delusuario del sitema.


![list](/assets/img/teacher/10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Si vemos elcodigo fuente vemos que seesta interpretando el codigo PHP.


![list](/assets/img/teacher/11.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ahoma metemos **cmd** para ejecutar un comando a discrecion.


![list](/assets/img/teacher/14.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Desde **log.php** es de donde se puede hacer la llamada al codigo php que metimos en **access.log**, para mandarnos la reverse-shell 


![list](/assets/img/teacher/16.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Obtenemos una shell como **www-data**.


***

## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 


Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.


También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


Husmeando vemos un archivo rabbit.jpg en el directorio **/var/www/html/** de www.data, nos vamos a decargar a nuestra maquina para atraves de tecnicas de steganografia buscar informacion, pero no tenemos suerte, ademas, **e14e1598b4271d8449e7fcda302b7975.pdf** quecontiene informacion interesante.


![list](/assets/img/teacher/2023-06-28_18-38.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/teacher/12.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La pass esta chatada.


![list](/assets/img/teacher/13.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Pero como ha escrito muy fuerte en la siguientehoja esta la pass hay que darle la vuelta porque esta al revez.


![list](/assets/img/teacher/15.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/teacher/16.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Nos conectamos a **mrteacher** atravez de ssh y podemosbuscar la flag en su escritorio.


Sudo -l nos dice que todos los usuarios en cualquier host ejecutar los comandos **gedit** y **xauth** sin necesidad de proporcionar una contraseña. 

Pero como gedit es una herramineta con interfaz grafica  debemos usar,-X en la coneccion ssh para habilitar el reenvío de X11. Permite que las aplicaciones gráficas se ejecuten en el servidor remoto, pero sus ventanas se muestren en el sistema local.


![list](/assets/img/teacher/17.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Usamos **gedit** y listamos con **xauth list**.


Ya con esto podemos hacer `sudo gedit /etc/shadow` y ver el  shadow de todo slosusuariospero como va hacer imposible crackear la pass de **root**, vamos a remplazar por la de **mrteacher** y asi nos conectaremos con lamosma credencial.


![list](/assets/img/teacher/18.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/teacher/20.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Reemplazamos hashes.


De esta forma tambien podemos convertirno en root, pero tambien podemos ver la falag de root.


![list](/assets/img/teacher/21.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La flag de **root**


![list](/assets/img/teacher/24.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Shell como **root**.


***

```bash
🎉 Felicitaciones ya has comprometido Visions de Hack My VM 🎉
```
{:.centered}

***

Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}
