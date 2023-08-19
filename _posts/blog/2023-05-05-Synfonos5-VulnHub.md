---
layout: post
title: "Write Up Synfonos5. "
subtitle: "eCPPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,VulnHub,LFI,SUDO,GTFOBins,Wrapper,Ldap,PHP,Reconnaissance,Protocols,eCPPTv2]
image:
  path: /assets/img/synfonos5/synfonos5.png
---

***

<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### Nmap


```bash
nmap -p- --open --min-rate 5000 -n -vvv -Pn -sS 10.10.0.129 -oA allports
```


![list](/assets/img/synfonos5/4.png){:.lead width="800" height="100" loading="lazy"}


### Services and Versions


```bash
nmap -sVC -Pn -n -p22,80,389 10.10.0.129 -oN target
```


![list](/assets/img/synfonos5/3.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Expltation


### HTTP TCP-80


Aunque tenemos el puerto 21 y 389 abiertos,primero como el puerto 80 es mas comun  vamos a enumerar ese primero, si nos conectamos solo hay una imagen asi que vamos a fuzzear para ver que encontramos.


![list](/assets/img/synfonos5/2.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/synfonos5/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Encontramos algunos archivos.php pero todos nos rdirigen a admin.php.


![list](/assets/img/synfonos5/7.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Formulario de login.


Para bypasear el login y como tenemos el puerto de ldap podriamos asumir que esta sicronizado con el ldap, ademas que podemos pobrar codigo sql, pero eso no funciona, provamos codigo ldap `*)(&` y de entrada husmeando en la url vemos algo raro asi que probando coasa seacontece un **LFI**.


![list](/assets/img/synfonos5/8.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Bypass autenticacion.


![list](/assets/img/synfonos5/9.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Url curiosa.


![list](/assets/img/synfonos5/10.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Local File Inclusion.


Como la web ejecuta codigo php asi que no podemos ver el contenido de los archivo asi que tenemos que verlos utilizando wrappers php, el cual lo tranforma en base64 y luego lo decodificaremos  y vemos credenciales.


![list](/assets/img/synfonos5/12.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Wrappers php.


![list](/assets/img/synfonos5/11.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Codigo en base64.


![list](/assets/img/synfonos5/13.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Decodificamos la base64 vemos **cn=admin,dc=symfonos,dc=local** y una contraseña **qMDdyZh3cT6eeAWD**.


***

### LDAP TCP-389


Ya con credenciales podemos conectarnos a LDAP y ver que hay en el servicio con una enumeracion de usuarios y credenciales.

```bash
nmap 192.168.0.112 -p 389 --script ldap-search --script-args 'ldap.username="cn=admin,dc=symfonos,dc=local", ldap.password="qMDdyZh3cT6eeAWD"' 
```


o


```bash
ldapsearch -x -H ladp://10.10.0.129 -D "cn=admin,dc=symfonos,dc=local" -w "qMDdyZh3cT6eeAWD"
```


![list](/assets/img/synfonos5/16.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/synfonos5/17.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Encontramos credenciales en base64 para el usuario zeus que es **cetkKf4wCuHC9FET** y nos conectamos por SHH.


***

## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 


Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.


También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


Al hacer **sudo -l**, descubrimos que zeus tiene permiso de sudo para ejecutar **dpkg** como root, por lo que abusamos de los derechos de sudo de zeus para escalar privilegios al explotar la funcionalidad de dpkg que vemos en GTFOBins.


![list](/assets/img/synfonos5/21.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ya podemos buscar la flag en elescritorio de root.

***

```bash
🎉 Felicitaciones ya has comprometido Synfonos5 de VunlHub 🎉
```
{:.centered}

***

Back to [Certification eCPPTv2](2023-07-06-Road-to-eCPPTv2.md){:.heading.flip-title}
{:.read-more}
