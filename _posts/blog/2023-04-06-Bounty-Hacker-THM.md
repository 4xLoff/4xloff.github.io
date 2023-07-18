---
layout: post
title: "Write Up Bounty Hacker. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Easy,Genin,Linux,THM,FTP,SSH,SUDO,CronJob,Reconnaissance,Misconfiguration,Weak-Credentials,eJPTv2]
image:
  path: /assets/img/bounty/bounty.jpg
---

***

<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### Nmap


```bash
nmap --open -p- -Pn -n -T4 -vvv -n 10.10.233.119 -oN allports
```


![list](/assets/img/bounty/1.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions

```bash
nmap -sVC -Pn -n -p21,22,80 10.10.233.119  -oN target
```

![list](/assets/img/bounty/4.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Exploitation


### FTP TCP-21


Como el usuario anonymos esta habilitado en el servicio de FTP es lo primero que vamos a revisar hay dos archivos uno es una nota que pone **1.) Protect Vicious.2.) Plan for Red Eye pickup on the moon.-lin** de aqui sacamos el nombre de usuario y el oro parece ser contraseñas pero no sabemos cual es valida asi que vamos ausar hydra para bruteforcear el servicio ssh.


![list](/assets/img/bounty/5.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
tenemos dos archivos que vamos a descarga el **locks.txt** y el **task.txt**.


![list](/assets/img/bounty/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La contraseña es **RedDr4gonSynd1cat3** y nos conectamos al ssh.


![list](/assets/img/bounty/8.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La flag esta en escritoriode lin.



***

## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 


Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.


También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


Con **sudo -l**, puedes ver que tenemos permisos para el comando tar como root y despues de buscar en [GTFObins],  y con linpeas vemos las tareas cron y hat un archivo  **passwd** que esta ejecutando meterse a backups y copiarse el pass y una arvhico.bak.

[GTFObins]: https://gtfobins.github.io/gtfobins/tar/


![list](/assets/img/startup/11.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
.


```bash
sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
```


![list](/assets/img/startup/11.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Obtenemos la shell de root y ya podemos buscar la flag de root.



***

```bash
🎉 Felicitaciones ya has comprometido Bounty Hacker de Try Hack My 🎉
```
{:.centered}

***

Back to [Certification eJPTv2](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}


