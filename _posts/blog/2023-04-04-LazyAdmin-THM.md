---
layout: post
title: "Write Up LazyAdmin. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,THM,FTP,SSH,SUDO,PHP,Reverse-Shell,Brute-Forcing,Reconnaissance,Fuzzing-Web,eJPTv2,CMS,CVE]
image:
  path: /assets/img/lazyadmin/lazy.jpeg
---

***

<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### Nmap


```bash
nmap --open -p- -Pn -n -T4 -vvv -n 10.10.201.24 -oN allports
```


![list](/assets/img/lazyadmin/1.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions

```bash
nmap -sVC -Pn -n -p22,80 10.10.201.24  -oN target
```

![list](/assets/img/lazyadmin/2.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Exploitation


### HTTP TCP-80


El escaneo revela 2 puertos abiertos el puerto 80 y el puerto 22 de momento con este no vamos hacer nada. El puerto 80 está ejecutando Apache. Después de verificar la página web en el puerto 80, obtuvimos la página web es predeterminada de Apache. Entonces, ejecutamos **FFUF** para obtener directorios caso obtuvimos el directorio /content/ pero volviendo a ver el archivo de nmap me doy cuenta que es un cms que se llama **CMS SweetRice** y con esto en mente ya fue buscar exploit en internet pero antes de eso no se la version y entonce busque si este proyecto es opensource y si lo es entonce busque el el archivo changelog.txt me dio una version 1.5.0 pero no se no me convensio asi que sgui invetigando y decubri que el archivo js esta otro que se llama **SweetRice.js** y me dice otra y ya me puse a buscar exploit con las dos para pobrar.


Aunque quisiera usar el [exploit], aun no podemos porque pide credenciales y es algo que no tenemos aun asi que hay que seguir husmeando

 [exploit]: https://www.exploit-db.com/exploits/40716


 ![list](/assets/img/lazyadmin/4.png){:.lead width="800" height="100" loading="lazy"}



Encontramos más directorios. El directorio **/as/** contiene una página de inicio de sesión, pero no tenemos credenciales para iniciar sesión, así que revisamos otros directorios. Revisamos el directorio **/inc/**, encontramos una carpeta llamada **/mysql_backup/**, así que revisamos esa carpeta.


{:.note title="Attention"}
Me olvide de sacar capturas dde esto jejejeje.


Logramos descargar el archivo respaldo de MySQL y encontramos un nombre de usuario y una contraseña , pero la contraseña estaba en forma de hash. Utilizamos Hash-identifier para determinar qué tipo de hash era y usamos Crackstation y la contraseña es **Password123**.


![list](/assets/img/lazyadmin/5.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Credenciales Backup bases de datos mysql.


![list](/assets/img/lazyadmin/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Contraseña en texto plano.


Aqui ya me envale un poco no use el exploit me loguee con esas credenciales al CMS patra hacerlo de forma manual.


![list](/assets/img/lazyadmin/7.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Login.


En la sección de Anuncios, podemos agregar un script para obtener una conexión inversa, también es posible ejecutar comandos directamente desde el panel de control o, como hice yo, subí el Script de [php-reverse-shell.php] de de github y no olvides cambiar la dirección IP y el puerto en el script, hacemos clic en **Listo** y el script se subió. Luego iniciamos un listener de Netcat, ahora debemos hacer clic en nuestro shell inverso para establecer una conexión.


[php-reverse-shell.php]: https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php


![list](/assets/img/lazyadmin/7.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/lazyadmin/9.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/lazyadmin/10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Esto nos da una shell como www-data.


***

## Escalation Privileges

Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 

Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.

También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


Podemos ver que hay un archivo que podemos ejecutar con **Perl** utilizando **Sudo**, así que verificamos el archivo usando el comando **cat /home/itguy/backup.perl**. No tenemos permisos para escribir, así que intentemos leer el archivo, lo que hace este script, es que  ejecuta un script bash llamado **/etc/copy.sh**, así que verifiquemos ese archivo.

Ahora verificamos los permisos y podemos escribir en este archivo y ejecutarlo. Ya hay un script de shell inverso presente con version antigua de netcat, así que solo tenemos que cambiar la dirección IP y el puerto para obtener una conexión inversa como root. 


![list](/assets/img/lazyadmin/10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Permiso SUDO.


![list](/assets/img/lazyadmin/11.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Editamos con nano y ya solo root al ejecutarlo y ya podemos buscar la flag de root.



***

```bash
🎉 Felicitaciones ya has comprometido LazyAdmin de Try Hack My 🎉
```
{:.centered}

***

Back to [Certification eJPTv2](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}


