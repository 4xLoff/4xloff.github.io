---
layout: post
title: "Write Up Responder."
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Linux,HTB,WinRM,Web,Network,Custom-Applications,Directory-traversal,Protocols,XAMPP,SMB,Responder,PHP,Reconnaissance,Password-Cracking,Hash-Capture,RFI,RCE,eJPTv2]
image:
  path: /assets/img/responder/respon.png
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
nmap --open -p- -Pn -n -T4 -vvv -n 10.129.221.126 -oN allports
```

![list](/assets/img/responder/nmap.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions

```bash
nmap -sVC -Pn -n -p80,5985,7680 10.129.221.126 -oN target
```

![list](/assets/img/responder/service.png){:.lead width="800" height="100" loading="lazy"}

***

## Vulnerability Analysis 

### HTTP TCP-80

En el puerto 80 se encuentra una página web. Al revisar más a fondo, no encontramos contenido relevante exepto un dominio **unika.htb** que meteremos al.


![list](/assets/img/responder/hosts.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Agregamos el dominio **unika.htb** al **/etc/hosts**.


![list](/assets/img/responder/web.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Se carga la pagina normalmente.


#### LFI

Cuando cambiamos de idioma en la página, vemos que hay un parámetro en la URL llamado **page**, lo cual es un poco curioso. Por lo general, esto puede ser vulnerable a LFI. Haciendo unas pequeñas pruebas, confirmamos que es vulnerable y probamos la ruta **C:\Windows\System32\drivers\etc\hosts** que es el /etc/hosts de windows.


![list](/assets/img/responder/etc.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Vemos la ruta donde se guarda los nombres de hosts de windows.


#### RFI and RCE

Ademas de eso la maquina es vulnerables a RFI y RCE porque haciendo pruebas y creando script con una reverse-shell pero esto no nos sirve de nada porque solo nos convertimos wn el usuario www-data pero podemos explotar el RFI ya que con **Responder** o **SMBServer**, podemos ponernos a la escucha e intencertar el hash **NTLMv2-SSP**.


![list](/assets/img/responder/url.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Esplotamos el RFI.


![list](/assets/img/responder/responder.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
A la escucha con responder.


***

## Exploitation

Para explotar esta vulnerabilidad debemos desde la la web incluir la IP desde donde se esta ala escucha con el responder.

![list](/assets/img/responder/hash.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Hash NTLMv2-SSP.


Esto tambien lo podemos hacer com smbserver.

![list](/assets/img/responder/hash2.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Hash NTLMv2-SSP.

Con el hash lo que podemos hacer es tratar de crackearlo con hascat o john the ripper.


![list](/assets/img/responder/john.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Una vez con el hash, lo crackeamos con **Hashcat** o **John the Ripper**, y la clave resultante es `badminton`.


Ahora con las credenciales vamos al puerto **5985** que eta abierto y este es del servicio WinRM de windows esto lo hacemos con **EvilWinrm**.

### WINRM TCP-5985

Con las credenciales adecuadas y el puerto de WinRM abierto, podemos conectarnos al servicio de WinRM.


```bash
evil-winrm -i 10.129.221.126 -u 'Administrator' -p 'badminton'
```


![list](/assets/img/responder/evil.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La flag esta en el escritorio de **mike**.


![list](/assets/img/responder/flag.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Vemos la flag.


{:.note title="Attention"}
En el siguiente enlace te dejo el [LFI.py](https://github.com/4xLoff/Python-Scripting/blob/main/lfiResponder.py) un scripto python que es capaz de hacer el LFI de forma automática para no perder mucho timpo y busca archivos con informacion interesante.


***

```bash
🎉 Felicitaciones ya has comprometido Resporder de HackTheBox 🎉
```
{:.centered}

***

Back to [Starting-Point](2023-02-02-Starting-Point.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}