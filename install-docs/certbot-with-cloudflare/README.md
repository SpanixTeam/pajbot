# Certbot with CloudFlare DNS

En esta pequeña subguía, obtendremos un certificado de [Let's Encrypt](https://letsencrypt.org/), y utilizaremos la API de CloudFlare para añadir/eliminar registros DNS para validar nuestra propiedad del dominio.

## Generate an API token for CloudFlare

- Vaya a https://dash.cloudflare.com/profile/api-tokens
- En "API Tokens", haga clic en "Crear Token".
- Introduzca un nombre de token descriptivo, por ejemplo "Certbot en mi-nombre-de-servidor".
- En la fila "Permisos", seleccione "Zona", "DNS", "Editar".
- En la fila "Recursos de zona", seleccione "Incluir", "Zona específica" y seleccione el dominio para el que desea obtener el certificado.
- Si desea que su servidor obtenga acceso a más de un dominio, haga clic en "Añadir más" en "Recursos de zona" y repita la operación para otras zonas.
- Haz clic en "Continuar con el resumen" cuando hayas terminado y comprueba que lo que se muestra es lo que deseas.
- Haz clic en "Crear token" para obtener finalmente tu token.
- En la última página, copie el código y guárdelo temporalmente en un lugar seguro, o mantenga la página abierta. Necesitaremos este token en el siguiente paso.

## Instalar Certbot

Certbot es un servicio que se ejecuta en tu servidor y que se encarga automáticamente de solicitar certificados (y mantenerlos actualizados) para tus dominios.

```bash
sudo apt install certbot python3-certbot-dns-cloudflare
```

## Almacenar el token de la API de CloudFlare en el servidor

Crea un archivo para guardar tu clave secreta de la API de la siguiente manera:

```bash
sudo mkdir -p /etc/letsencrypt/secrets
sudo cp /opt/pajbot/install-docs/certbot-with-cloudflare/cloudflare.ini /etc/letsencrypt/secrets/cloudflare.ini
sudo chown root:root /etc/letsencrypt/secrets/cloudflare.ini
sudo chmod 600 /etc/letsencrypt/secrets/cloudflare.ini
```

A continuación, introduzca los datos de su API:

```bash
sudo nano /etc/letsencrypt/secrets/cloudflare.ini
```

Ponga la clave API del paso anterior junto a `dns_cloudflare_api_token`.

## Solicitar certificado con certbot

Repita `-d "nombre-del-dominio.com"` tantas veces como sea necesario para añadir nombres de dominio y comodines a su certificado.

```bash
sudo certbot certonly --dns-cloudflare --dns-cloudflare-credentials /etc/letsencrypt/secrets/cloudflare.ini -d "your-domain.com" -d "*.your-domain.com" --post-hook "systemctl reload nginx"
```

Debería ver un resultado similar a este:

<pre><code>Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator dns-cloudflare, Installer None
Obtaining a new certificate
Performing the following challenges:
dns-01 challenge for example.com
Waiting 10 seconds for DNS changes to propagate
Waiting for verification...
Cleaning up challenges

IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   <b>/etc/letsencrypt/live/your-domain.com/fullchain.pem</b>
   Your key file has been saved at:
   <b>/etc/letsencrypt/live/your-domain.com/privkey.pem</b>
   Your cert will expire on 2020-02-01. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot
   again. To non-interactively renew *all* of your certificates, run
   "certbot renew"
 - If you like Certbot, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le</code></pre>

Fíjate en la parte resaltada: Esto es importante para establecer la configuración de nginx: La primera ruta es la que va con `ssl_certificate`, la segunda ruta va con `ssl_certificate_key`.

Ahora puedes editar el archivo de configuración de nginx y apuntarlo a la ruta correcta del certificado:

```bash
sudo nano /etc/nginx/sites-available/streamer_name.your-domain.com.conf
```

```
ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
```

> ¡Nota! Si has solicitado un certificado comodín (como hemos hecho aquí en el ejemplo), puedes reutilizar el mismo certificado para varios bots. Por ejemplo, si tienes bots que se ejecutan bajo los dos subdominios `streamer_a.tu-dominio.com` y `streamer_b.tu-dominio.com`, y tienes un certificado comodín para `*.tu-dominio.com`, entonces ambas configuraciones del sitio pueden compartir el mismo certificado (`/etc/letsencrypt/live/tu-dominio.com/fullchain.pem` por ejemplo).
