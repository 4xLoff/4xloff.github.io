---
layout: post
title: "Write Up Ambassador. "
subtitle: "Starting-Point"
category: Blog
tags:  [Medium,Chunin,Linux,HTB,Grafana,Token,SSH,Web,Vulnerability-Assessment,Database,Git,Common-Applications,Outdated-Software,Apache,MySQL,Python,SQL,Reconnaissance,Configuration-Analysis,Arbitrary-File-Read,Clear-Text-Credentials,Directory-Traversal,Web-Site-Structure-Discovery,eWPT,OSCP] 
image:
  path: /assets/img/abassador/Captura%20de%20pantalla%20(185).png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconocimiento


### nmap


```bash
nmap -p- --open --min-rate 5000 -n -vvv -Pn 10.10.11.183 -oA allports
```


![list](/assets/img/abassador/Kali-2022-10-05-19-04-48.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions


```bash
nmap -p22,8080 -sV -sC 10.10.11.183 -oN target
```
![list](/assets/img/abassador/Kali-2022-10-05-19-07-49.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis


### HTTP TCP-80


![list](/assets/img/abassador/Kali-2022-10-05-19-25-14.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
En el 80 no encontramos nada interesante. 


Miramos el puerto 3000 podemos ver lo siguiente.


![list](/assets/img/abassador/Kali-2022-10-05-19-24-21.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con `curl http://10.10.11.183:3000/login | grep "Grafana v"` podemos ver la version. 


Buscando exploits en la web o con searsploit en contramos una vulneravilidad de 


Directory Traversal and Arbitrary File para [Grafana], para leer archivos.


[Grafana]:https://vk9-sec.com/grafana-8-3-0-directory-traversal-and-arbitrary-file-read-cve-2021-43798/


Usamos el exploit que encontramos para enumerar los usuarios de la victima.


![list](/assets/img/abassador/Kali-2022-10-05-19-16-09.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con `cat credential.txt | grep "sh$"` filtramos por los usuarios validos . 


También podemos descargar la db de grafana para inspeccionarla.


![list](/assets/img/abassador/Kali-2022-10-05-19-23-02.png){:.lead width="800" height="100" loading="lazy"}


```bash
curl -s --path-as-is http://10.10.11.183:3000/public/plugins/alertlist/../../../../../../../../var/lib/grafana/grafana.db -o grafana.db
```

{:.note}
Husmenado en la base de datos nos encontramos una credecial `dontStandSoCloseToMe63221!`.


En este punto ya es conectarnos a la base de datos del servidor hya tenemos un nombre de


usuario que es developer y la pass.


![list](/assets/img/abassador/Kali-2022-10-05-19-38-25.png){:.lead width="800" height="100" loading="lazy"}


Volvemos a husmear y encontramos nuevas credenciales que estan en base64 por lo cual debemos decodearlas ya sea via web o terminal como quieras.


![list](/assets/img/abassador/Kali-2022-10-05-19-39-23.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Las nuevas crededenciales son: `developer:YW5FbmdsaXNoTWFuSW5OZXdZb3JrMDI3NDY4Cg==`.


Nos conectamos via ssh a ssh developer@10.10.11.183


![list](/assets/img/abassador/Kali-2022-10-05-19-42-45.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Como siempre la flag de user esta en el escritorio de developer.


***

## Explotacion and Escalation Privileges


Siempre es bueno ejecutar `LimEnum` Y `pspy` para monitorizar y ver los posibles vectores para escalar de privilegios, ademas hasta que se ejecute los anteriores podemos buscar los permisos con el comado find con el siguite comado.


Buscando entre permisos root se encontró una carpeta propiedad de root con acceso de lectura para el desarrollador y contiene un repo .git, en cual miraremos la diferencias entre los commits.


![list](/assets/img/abassador/Kali-2022-10-05-21-25-52.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Encontramos un token `bb03b43b-1d81-d62b-24b5-39540ee469b5`.


En la búsqueda en línea se han encontrado los siguientes recursos relativos a la explotación del consul [API].


[API]: https://www.infosecmatter.com/metasploit-module-library/?mm=exploit/multi/misc/consul_service_exec


Utilizamos mfscosole para conectarnos al servidor como root con payload que inyecta el acl_token.


![list](/assets/img/abassador/Kali-2022-10-05-22-31-29.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Es inportalte que en el msfconsole se agregue el campo ACL_token `bb03b43b-1d81-d62b-24b5-39540ee469b5`.


Ya lo ultimo es buscar la flag de superusuario en el escritorio de root.

***

```shell
🎉 Felicitaciones ya has comprometido Ambassador de HackTheBox 🎉
```
{:.centered}

***
Back to [Certification eWPT](){:.heading.flip-title}
{:.read-more}

***
Back to [Certification OSCP](){:.heading.flip-title}
{:.read-more}