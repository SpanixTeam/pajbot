# Configuración básica de nginx

Cuando instalas nginx desde los repositorios debian, viene con una configuración básica para mostrar que nginx está funcionando. Sin embargo, la configuración no es recomendada establecerse para un servidor seguro que utiliza HTTPS solamente.

Puedes usar esta configuración básica como una plantilla para tu propia configuración. Contiene un `nginx.conf` ligeramente alterado que establece algunas cabeceras relevantes para la seguridad, configura valores predeterminados seguros para las conexiones HTTPS y también redirige a los usuarios si intentan acceder a sus sitios web utilizando HTTP.

Lo primero que tenemos que hacer: Vamos a necesitar una versión de nginx con algunas características extra:

```bash
sudo apt install nginx-extras
```

A continuación, fusiona nuestra configuración en tu directorio de configuración de nginx y elimina la configuración del sitio por defecto preinstalada:

```bash
sudo cp -RT /opt/pajbot/install-docs/full-nginx-setup/basic-config/ /etc/nginx/
sudo ln -s /etc/nginx/sites-available/https-redirect.conf /etc/nginx/sites-enabled/https-redirect.conf
sudo rm /etc/nginx/sites-{available,enabled}/default
```

También necesitamos generar un archivo criptográfico llamado "parámetros Diffie-Hellman":

```bash
sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 4096
```

Este comando puede tardar bastante (del orden de 1-2 horas si su CPU no es muy reciente).

> Nota: Los parámetros Diffie-Hellman no son secretos en ningún sentido (Su servidor incluso envía estos parámetros a los clientes que se conectan), por lo que no necesita mantener el archivo generado en secreto, ni preocuparse de que se filtre.

Una vez hecho esto, reinicia nginx de la siguiente manera:

```bash
sudo systemctl reload nginx
```
