---
layout: post
title: "Write Up Archetype."
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Linux,HTB,Network,Protocols,MSSQL,SMB,Impacket,Powershell,Reconnaissance,RCE,Clear-Text-Credentials,Information-Disclosure,Anonymous_Guest-Access,eJPTv2]
image:
  path: /assets/img/archetype/archetype.png
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
nmap --open -p- -Pn -n -T4 -vvv -n 10.129.14.254 -oN allports
```

![list](/assets/img/archetype/nmap.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions

```bash
nmap -sVC -Pn -n -p22,80 10.129.14.254 -oN target
```

![list](/assets/img/archetype/service1.png){:.lead width="800" height="100" loading="lazy"}

![list](/assets/img/archetype/service2.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis 

Tenemos dos puetos que me llaman la atencion uno es el 445 y el otro es el 14433 que es **SQLServer** que es la base de datos de **Microsoft**.


### SMB TCP-443

Con el script de nmap vemos que el usuario anonymous nos vamos a conectar al servicio.


```bash
smbclient -N  10.129.14.254 -L
```


![list](/assets/img/archetype/list.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Tenemos acceso de lectura al sahres **backup**.


![list](/assets/img/archetype/cred.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Husmeando encontramos el archivo **prod.dtsConfig** que contine credenciales `ARCHETYPE/ssql_svc:M3g4c0rp12`.


### MSSQL TCP-1433

Con las credenciales obtenidas nos conectamos al servicio de **SQLServer**.


```bash
mssqlclient.py ARCHETYPE/ssql_svc:M3g4c0rp123@10.129.14.254 -windows-auth
```


![list](/assets/img/archetype/msqlc.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Esto nos da una shell de sqlserver.


***

## Exploitation

Como primer paso, debemos verificar qué rol tenemos en el servidor, utilizaremos el comando que se encuentra en el resumen de comandos anterior  `SELECT is_srvrolemember('sysadmin');`, si el resultado es 1, lo cual se traduce como Verdadero podemos ejecutal comados atraves de **xp_cmdshell**.

Pero tambien hat que habilitar esa funcion eso lo hace,os con el siguiente comando `enable_xp_cmdshell` o `SQL> EXEC xp_cmdshell 'net user';`

![list](/assets/img/archetype/reverse.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Para ejecutar la reverse shell debemos primeramente subir el binario **nc.exe** y a que con **xp_cmdshell** somos capaces de ejecutar comados de **powersehell** para esto levantamos un servidor http con python.


![list](/assets/img/archetype/prove.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con esto debemos tener acceso al servido con el nombre de **archetype\sql_svc**.


[**SeImpersonatePrivilege**]: https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation/roguepotato-and-printspoofer

![list](/assets/img/archetype/juice.png){:.lead width="800" height="100" loading="lazy"}


{:.note title="Attention"}
Para la escalda de privileguios podemos subir el binario **winPEASx64.exe** al servidoe de la misma forma que con **nc64.exe** o tambie desde el servidor con **cerutils** o **IEX**, pero tambien el servido es suceptible a [**SeImpersonatePrivilege**], explotaremos mas adelnate esta vulnerabilidad.


***

## Privilege Escalation

Ejecutamos el **winPEASx64.exe** para ver información que nos podría ayudar en el objetivo de obtener privilegios de **Superusuario**. Al ejecutarlo, nos revela algunas posibilidades de escalar privilegios, información sobre procesos, permisos e información delicada. También nos revela que el archivo del historial contiene datos curiosos `C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt`, así que vamos a ver de qué se trata.


![list](/assets/img/archetype/priv.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Obtuvimos en texto claro la contraseña del usuario **Administrator**, que es **MEGACORP_4dm1n!!**.

Connesta credenciales vamos a usar la herramienta **psexec.py**, que es una herramienta de código abierto utilizada en pentesting y administración de sistemas. Permite la ejecución remota de comandos y programas en máquinas Windows a través del protocolo **SMB (Server Message Block)**.


![list](/assets/img/archetype/root1.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Ya solo el usuario **nt authority/system** osea el **Superusuario**.


![list](/assets/img/archetype/root.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Vemos la flag.


***

```bash
🎉 Felicitaciones ya has comprometido Archetype de HackTheBox 🎉
```
{:.centered}

***

Back to [Starting-Point](2023-02-02-Starting-Point.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}