---
layout: post
title: "Write Up Suidy. "
subtitle: "eJPTv2 Track "
category: Blog
tags: [Medium,Chunin,Linux,HMVM,SSH,SUID,C,Reconnaissance,Protocols,Brute-Forcing,Bash,Fuzzing-Web,Hydra,Compilation,eJPTv2]
image:
  path: /assets/img/suidy/sudo.png
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

![list](/assets/img/suidy/1.png){:.lead width="800" height="100" loading="lazy"}


### Nmap


```bash
nmap --open -p- -Pn -n -T4 -vvv -n 198.168.100.45 -oN allports
```


![list](/assets/img/suidy/2.png){:.lead width="800" height="100" loading="lazy"}



### Services and Versions

```bash
nmap -sVC -Pn -n -p22,80 198.168.100.45 -oN target
```

![list](/assets/img/suidy/3.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Expltation


### HTTP TCP-80

Aunque tenemos algunos puertos en el pueto 22 no podemos hace nada de momento, asi que nos concentraremos en el puerto 80, en contrandonos con un **/hi, /....\..\.-\--.\.-\..\-.** dirctorio al final **/shehatesme**, del apagina que vamosa husmear pero si en contramos nada mas vamos a fuzzear.


![list](/assets/img/suidy/4.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/suidy/5.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Encontramos unas  credenciales **theuser:thepass** , ademas nosdice que en ese directoriohay muchosarchivos .txt asi  que vamos a fuzzear por esos justamente.


Son muchos vamos a verque contine cada uno podemos hacerlo manualmente o crear un script yo hice uno en python lo dejo al final, lo importante esque en uno hay credenciales de este estilo **hidden1/passZZ!,yuijhse/hjupnkk,jhfbvgt/iugbnvh** para usarlo como diccionario con hydra podemos probar una  a una o podemos mediate un one-liner remplazar **/** por **:** y con elparametro -C en hidra usarlo como **user:pass**.


![list](/assets/img/suidy/2023-06-26_18-44.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ataque de fuerza bruta con hydra, nos da  las credenciales correctas que son **theuser:thepass** la misma que ya nos dieron antes.


![list](/assets/img/suidy/6.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La flag de bajos privileguios esta en el directorio.


***

## Escalation Privileges


Primero, ejecutamos el comando **id** en Linux para obtener información sobre la identificación del usuario actual y los grupos a los que pertenece, ademas ejecutaremos **uname -a** y **lsb_release -a** para obtener información del sistema, verificaremossi otro usurio tiene permisos sudores con **sudo -l**, además, buscamos binarios con permisos **SUID** y tareas **Cron** en busca de posibles puntos de entrada. 


Si no encontramos resultados significativos con las acciones anteriores, procedemos a subir los binarios **linpeas** y **pspy** .etc, al sistema. Estos binarios nos ayudarán a realizar un análisis de reconocimiento más exhaustivo, identificando posibles vulnerabilidades o actividades sospechosas en el sistema.


También realizamos un análisis manual del sistema, buscando configuraciones inseguras, archivos sensibles o cualquier otra anomalía que pueda indicar una posible vulnerabilidad o actividad maliciosa.


Husmenado vemos una nota que no podemos leer de momento, y un  binario llmado **suidyyyy** asi que vamos a enterarnod  de que se trata.


![list](/assets/img/suidy/8.png){:.lead width="800" height="100" loading="lazy"}


Después de ejecutarlo, nos hemos transformado en el usuario suidy y ahora tenemos los privilegios necesarios para acceder a esa nota que pone **I love SUID files!,The best file is suidyyyyy because users can use it to feel as I feel.root know itand run an script to be sure that my file has SUID.If you are "theuser" I hate you!-suidy** que nos proporciona otra pista. Por lo tanto, nos dirigimos al directorio de trabajo de suidy y transferimos la herramienta pspy64, que nos facilitará la búsqueda de procesos en el sistema.

El script se ejecuta cada minuto, y de acuerdo con la pista, parece ser el responsable de otorgar permisos **SUID**. No podemos verificar esto debido a la falta de permisos. Además, no tenemos acceso al código fuente del binario suidyyyyy,por lo tanto, vamos a crear uno nuevo y reemplazarlo. Esto significa que perderemos el permiso SUID, pero el proceso que hemos descubierto volverá a otorgarlo, permitiéndonos obtener una shell como root.


![list](/assets/img/suidy/9.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Usamos pspy para ver los proecesos que se estan ejecutando y hay un **root/timer.sh** si lo vemos observamos  que ejecuta a suidyyy yy, pero por la nota sabemos o dedicimos que esto mismo,  por otra parte si vemosnosotros no podemos ejecutar ni escrivir en suidy directorio, entoces nos vamos  a **theuser** a  subirno la el binario que nos otrogara una shell par luego moverlo por theuser no puede ejecutarlos y suidy si.


El binario es el siguiente:


![list](/assets/img/suidy/2023-06-26_18-58.png){:.lead width="800" height="100" loading="lazy"}


```bash
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main(void)
{
    setuid(0);
    setgid(0);
    system("/bin/bash");
    return 0;
}

```


{:.note}
Compilamos el shell.c a shell-root en nuestra maquina y lo  subimos a theuser, y lo copiamos a suidy.


Ahora solo nos  queda esperar o podemos con wath monitorizar al momento que se suidyyy se  vuelva SUID, y lo ejecutamos para así nos convertiremos en root.


![list](/assets/img/suidy/11.png){:.lead width="800" height="100" loading="lazy"}


{:.note title="Attention"}
En el siguiente enlace a la utilidad para extraer las credeciales [suidyPwn](https://github.com/4xLoff/Python-Scripting/blob/main/suidyUserPass.py) de esta máquina hecho en Python.


***

```bash
🎉 Felicitaciones ya has comprometido Suidy de Hack My VM 🎉
```
{:.centered}

***

Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}
