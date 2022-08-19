# Instrucciones de instalación

¡Bienvenido a las instrucciones de instalación de pajbot!

Abajo encuentras el índice para una lista completa de instrucciones de instalación para pajbot.

Estas instrucciones instalarán pajbot de forma que te permita ejecutarlo para varios streamers a la vez sin necesidad de un duplicado. Por esta razón, estas instrucciones de instalación están divididas en dos grandes partes: La instalación de pajbot, y la creación de una instancia de pajbot para un solo canal (que puedes repetir según sea necesario, si quieres ejecutar pajbot en múltiples canales, para diferentes streamers por ejemplo).

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

**Tabla de Contenido** _generada con [DocToc](https://github.com/thlorenz/doctoc)_

- [Instalación de servicios](#instalación-de-servicios)
  - [Instalar dependencias del sistema](#instalar-dependencias-del-sistema)
  - [Configurar un usuario del sistema](#configurar-un-usuario-del-sistema)
  - [Instalar pajbot](#instalar-pajbot)
  - [Instalar y configurar base de datos](#instalar-y-configurar-base-de-datos)
  - [Instalar Redis](#instalar-redis)
  - [Instalar nginx](#instalar-nginx)
  - [Instalar servicios del sistema](#instalar-servicios-del-sistema)
- [Configuración de un bot](#configuración-de-un-bot)
  - [Crear una aplicación con Twitch](#crear-una-aplicación-con-twitch)
  - [Crear un esquema de base de datos](#crear-un-esquema-de-base-de-datos)
  - [Crear un archivo de configuración](#crear-un-archivo-de-configuración)
  - [Configurar el sitio web con nginx](#configurar-el-sitio-web-con-nginx)
  - [Habilitar e iniciar el servicio](#habilitar-e-iniciar-el-servicio)
  - [Autenticar el bot](#autenticar-el-bot)
  - [Otros pasos](#otros-pasos)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Instalación de servicios

Por favor, tenga en cuenta que actualmente sólo documentamos cómo ejecutar pajbot en sistemas GNU/Linux. Las siguientes instrucciones deberían funcionar sin ningún problema en Debian y Ubuntu. Si está ejecutando otra distribución de GNU/Linux, es posible que tenga que hacer algunos cambios en los comandos, ubicaciones de archivos, etc. a continuación.

## Instalar dependencias del sistema

Pajbot está escrito en python, así que necesitamos instalar algunos paquetes básicos de python:

```bash
sudo apt update
sudo apt install python3 python3-dev python3-pip python3-venv
```

También necesitamos las siguientes bibliotecas y herramientas de compilación:

```bash
sudo apt install libssl-dev libpq-dev build-essential git
```

Ahora, comprueba que tienes Python 3.9 o más reciente instalado:

```bash
python3 --version
```

Si la versión de Python de su sistema no es 3.9 o superior, debe instalar [pyenv](https://github.com/pyenv/pyenv) siguiendo las instrucciones que se indican a continuación.

### Instalación de pyenv

Instale las dependencias necesarias para compilar Python (instrucciones de [aquí](https://github.com/pyenv/pyenv/wiki#suggested-build-environment))

```bash
sudo apt update
sudo apt install build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

Instala pyenv en tu sistema (instrucciones desde [aquí](https://github.com/pyenv/pyenv#automatic-installer), hay otros métodos alternativos de instalación disponibles si lo deseas)

```bash
curl https://pyenv.run | bash
```

Configure su entorno de shell bash para Pyenv (instrucciones de [aquí](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv))

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
```

A continuación, reinicie su shell.

## Configurar un usuario del sistema

Por razones de seguridad, no deberías ejecutar pajbot como usuario `root` en tu servidor. Puedes crear un usuario de "sistema" con pocos privilegios para pajbot de la siguiente manera:

```bash
sudo adduser --system --group pajbot --home /opt/pajbot
```

## Instalar pajbot

Descarga la última versión de pajbot mediante una branch dependiendo de tus necesidades:
<p align="center">
<kbd>master</kbd>: Rama base | <kbd>dark-mode</kbd>: Modo oscuro
</p>

```bash
sudo -u pajbot git clone https://github.com/SpanixTeam/pajbot.git /opt/pajbot --branch dark-mode
```

Instala las dependencias de pajbot así:

```bash
cd /opt/pajbot
sudo -H -u pajbot ./scripts/venvinstall.sh
```

Si desea utilizar la versión de Python de su sistema, ejecute el comando de la siguiente manera:

```bash
cd /opt/pajbot
sudo -H -u pajbot SKIP_PYENV=1 ./scripts/venvinstall.sh
```

## Instalar y configurar base de datos

pajbot utiliza PostgreSQL como servidor de bases de datos. Si aún no tienes PostgreSQL corriendo en tu servidor, puedes instalarlo con:

```bash
sudo apt install postgresql
```

Ahora que tienes PostgreSQL instalado, crearemos un usuario para que pajbot pueda utilizar la bases de datos PostgreSQL:

```bash
sudo -u postgres createuser pajbot
```

> Nota: No hemos establecido una contraseña para pajbot, y esto es intencional. Debido a que hemos creado un usuario del sistema con el nombre `pajbot` antes, las aplicaciones que se ejecutan bajo el usuario del sistema `pajbot` serán capaces de iniciar sesión en el servidor de base de datos como el usuario de base de datos `pajbot` automáticamente, sin tener que introducir una contraseña.
>
> Hemos ejecutado `createuser` como `postgres` por la misma razón: `postgres` es un superusuario predefinido de la base de datos PostgreSQL, y al usar `sudo`, estamos ejecutando `createuser pajbot` como el usuario del sistema (y de la base de datos) `postgres`.
>
> Esta es una configuración por defecto presente en los sistemas tipo Debian, y se define a través del fichero de configuración [`pg_hba.conf`](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html).

Ahora crearemos una base de datos llamada `pajbot`, propiedad del usuario de base de datos `pajbot`:

```bash
sudo -u postgres createdb --owner=pajbot pajbot
```

## Instalar Redis

Pajbot también necesita una instancia de [Redis](https://redis.io/) para funcionar. El servidor de base de datos redis no necesita ninguna configuración manual - todo lo que tienes que hacer es instalar redis:

```bash
sudo apt install redis-server
```

El servidor de redis se inicia automáticamente después de la instalación. Puedes comprobar que la instalación funciona así:

```bash
redis-cli PING
```

Deberías obtener `PONG` como respuesta. Eso significa que tu servidor de redis está funcionando bien.

## Instalar nginx

Nginx es un proxy inverso - acepta todas las peticiones HTTP entrantes a su servidor, y reenvía la petición al servicio backend correcto. También aplica encriptación para HTTPS, puede establecer cabeceras, reescribir URLs, etc.

Todo lo que necesitas hacer para este paso es instalar nginx:

```bash
sudo apt install nginx
```

Configuraremos nginx más tarde.

> Nota: Puedes encontrar una configuración básica de nginx que incluye la redirección HTTP -> HTTPS, los parámetros de configuración SSL recomendados, etc. [aquí](./full-nginx-setup/README.md). Si aún no tienes una configuración básica de nginx, te recomendamos encarecidamente que sigas la directriz enlazada ahora.

## Instalar servicios del sistema

Te recomendamos que ejecutes pajbot con la ayuda de systemd. Systemd se encargará de:

- iniciar y detener pajbot,
- capturar y almacenar la salida del servicio como registros,
- iniciar pajbot automáticamente al arrancar el sistema (y arrancarlo en el orden correcto, después de otros servicios que necesita),
- reiniciar pajbot en caso de fallo,
- y ejecutar múltiples instancias si ejecutas pajbot para varios streamers

Para empezar a usar systemd para pajbot, instala los archivos de unidad preempaquetados así:

```bash
sudo cp /opt/pajbot/install-docs/*.service /etc/systemd/system/
```

A continuación, dile a systemd que recargue los cambios:

```bash
sudo systemctl daemon-reload
```

# Configuración de un bot

Ahora que tienes lo básico instalado, necesitamos decirle a pajbot que (y cómo) se ejecute en un canal determinado. Pajbot corriendo en un solo canal, y con su sitio web para ese canal, se llamará una **instancia** de pajbot a partir de ahora.

## Crear una aplicación con Twitch

Lo primero que tienes que hacer es crear una aplicación para la instancia del bot. Registrar una aplicación te da tres datos importantes que el bot necesita para poder acceder a la API de Twitch y permitir a los usuarios iniciar sesión en el sitio web utilizando su cuenta de Twitch: Un ID de cliente, el secreto de cliente y el URL de redireccionamiento.

Para crear una aplicación con Twitch, visita https://dev.twitch.tv/console/apps/create.

- En _Nombre_, introduce el nombre que quieres que los usuarios vean cuando se conecten al sitio web y tengan que confirmar que quieren concederte acceso a su cuenta.
- En _URL de redireccionamiento de OAuth_, introduce la URL completa a la que los usuarios deben ser redirigidos después de completar el procedimiento de inicio de sesión con Twitch. Debería ser `https://tu-dominio.com/login/authorized` (ajustando el nombre del dominio, por supuesto).
- En _Categoría_, deberías elegir _Chat Bot_, ya que es la opción más apropiada para pajbot.

Después de hacer clic en "Crear", se le da acceso a la **ID de cliente**. Después de hacer clic en **Nuevo secreto**, también puedes acceder a tu **Secreto del cliente**. Necesitará estos valores en el siguiente paso - cuando cree el archivo de configuración para su instancia.

## Crear un esquema de base de datos

Los datos de cada instancia viven en la misma base de datos (`pajbot`, la hemos creado antes), pero separamos los datos poniendo cada instancia en su propio **esquema**. Para crear un nuevo esquema para tu instancia, ejecuta:

```bash
sudo -u pajbot psql pajbot -c "CREATE SCHEMA pajbot1_nombrestreamer"
```

Recuerda el nombre del esquema que has creado. Tendrás que introducirlo en el archivo de configuración, que crearás y editarás en el siguiente paso:

## Crear un archivo de configuración

Hay un [archivo de configuración de ejemplo](../configs/example.ini) disponible para que lo copies:

```bash
sudo -u pajbot cp /opt/pajbot/configs/example.ini /opt/pajbot/configs/nombre_streamer.ini
```

El ejemplo de configuración contiene comentarios sobre los valores que debes introducir en cada lugar. Edite la configuración con un editor de texto para ajustar los valores.

```bash
sudo -u pajbot editor /opt/pajbot/configs/nombre_streamer.ini
```

## Configurar el sitio web con nginx

Pajbot viene con archivos de configuración de nginx preconfigurados, sólo tienes que copiarlos y editarlos ligeramente para que reflejen tu instalación.

```bash
sudo cp /opt/pajbot/install-docs/nginx-example.conf /etc/nginx/sites-available/nombre_streamer.tu-dominio.com.conf
sudo ln -s /etc/nginx/sites-available/nombre_streamer.tu-dominio.com.conf /etc/nginx/sites-enabled/
```

A continuación, tienes que editar el archivo, como mínimo tendrás que insertar el nombre correcto del streamer en lugar del nombre del streamer de ejemplo.

La configuración de ejemplo establece su sitio web a través de HTTPS, para lo cual necesita un certificado (`ssl_certificate` y `ssl_certificate_key`). Hay muchas maneras posibles de obtener un certificado, por lo que no podemos ofrecer una guía definitiva que funcione para la configuración de todo el mundo. Sin embargo, si necesitas ayuda para este paso, puedes [encontrar una guía aquí](./certbot-with-cloudflare/README.md) si has configurado tu dominio con **CloudFlare DNS**.

Una vez que hayas terminado con tus cambios, prueba que la configuración no tiene errores:

```bash
sudo nginx -t
```

Si esta comprobación es correcta, ahora puedes recargar nginx:

```bash
sudo systemctl reload nginx
```

## Habilitar e iniciar el servicio

Para iniciar y habilitar (es decir, ejecutarlo en el arranque) pajbot, ejecuta:

```bash
sudo systemctl enable --now pajbot@nombre_streamer pajbot-web@nombre_streamer
```

## Autenticar el bot

Un último paso: Tienes que dar acceso a tu instancia de pajbot para usar tu cuenta de bot. Para ello, visita la URL `https://nombre_streamer.tu-dominio.com/bot_login` y completa el procedimiento de inicio de sesión para autorizar el bot.

El bot se conectará automáticamente al chat en unos 2-3 segundos después de que hayas completado el proceso de inicio de sesión.

## Otros pasos

¡Enhorabuena! Tu bot ya debería estar funcionando, pero hay algunos pasos adicionales que quizás quieras completar:

- Pídele al streamer que se conecte una vez yendo a `https://nombre_streamer.tu-dominio.com/streamer_login` - Si el streamer hace esto, el bot será capaz de buscar quién es un suscriptor y mantener la base de datos actualizada regularmente. El bot también podrá cambiar el juego y el título con los comandos `!settitle` y `!setgame`. Alternativamente, el streamer podría dar al bot el [permiso de editor](https://help.twitch.tv/s/article/Managing-Roles-for-your-Channel?language=es#manage), esto también permitirá al bot cambiar el juego y el título desde el chat.
- Añade algunos comandos básicos:

  Aquí hay algunas ideas:

  ```
  !add command ping --reply FeelsDankMan 🏓 $(tb:bot_name) $(tb:version_brief) || Online durante $(tb:bot_uptime)
  !add command commands|help --reply Comandos disponibles en: https://$(tb:bot_domain)/commands
  !add command ecount --reply $(1) ha sido usado $(ecount;1) veces
  !add command epm --reply $(1) está siendo usado $(epm;1) veces por minutos
  !add command uptime|downtime --reply $(broadcaster:name) ha estado $(tb:stream_status) durante $(tb:status_length)
  !add command points|p --reply $(usersource;1:name) tiene $(usersource;1:points|number_format) puntos
  !add command lastseen --reply $(user;1:name) fue visto por última vez hace $(user;1:last_seen|time_since_dt), y estuvo activo hace $(user;1:last_active|time_since_dt)
  !add command epmrecord --reply $(1) tiene un récord por minuto de $(epmrecord;1)
  !add command profile --reply https://$(tb:bot_domain)/user/$(usersource;1:login)
  !add command overlay|clr --reply https://$(tb:bot_domain)/clr/overlay/12345
  !add command playsounds --reply Los sonidos disponibles están enlistados en: https://$(tb:bot_domain)/playsounds
  !add command title --reply El título actual es: $(stream:title)
  !add command game --reply La categoría actual es: $(stream:game)
  !add command timeonline|watchtime --reply $(usersource;1:name) ha estado $(usersource;1:minutes_in_chat_online|time_since_minutes) en el chat online
  !add command timeoffline --reply $(usersource;1:name) ha estado $(usersource;1:minutes_in_chat_offline|time_since_minutes) en el chat offline
  ```

- Los argumentos avanzados para comandos se pueden encontrar [aquí.](https://github.com/pajbot/pajbot/blob/1ed503003c7363ebc592d0945d6c31ab1107db30/pajbot/managers/command.py#L450-L464)
