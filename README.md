# pajbot ![Python 4HEad](https://github.com/pajbot/pajbot/workflows/Python%204HEad/badge.svg)

pajbot es un bot para chat de twitch creado por [pajlada](http://twitch.tv/pajlada).  
[Website](https://pajbot.com)

Nota: pajbot está en **modo de mantenimiento**.
Esto significa que nos centramos en mantener el proyecto vivo no permitiendo grandes revisiones de ningún sistema de pajbot ni de ninguna característica importante.
Arreglar errores, actualizar dependencias y asegurar que el código que interactúa con APIs externas siga funcionando será nuestro principal objetivo.
Las peticiones de características no serán aceptadas a menos que alguien esté dispuesto a poseer la característica, e incluso entonces algunas características que cambian demasiado la arquitectura no serán permitidas.
La versión mínima de Python actualmente soportada es **3.9**.

## Versionado de Python

Utilizamos [pyenv](https://github.com/pyenv/pyenv) para gestionar las versiones de Python. Familiarízate con esta herramienta.  
Instalación rápida de pyenv en sistemas Linux: `curl https://pyenv.run | bash`

Si no quieres usar la versión de Python de pyenv en ninguno de nuestros scripts, establece la variable de entorno `SKIP_PYENV` a `1`.

## Instalación rápida

1. Instalar los requisitos de la biblioteca escribiendo `./scripts/venvinstall.sh` en el directorio raíz
2. Copiar `./configs/example.ini` a `./config.ini` y cambiar las líneas relevantes en el archivo.
3. ¡Ejecuta el bot! `./main.py`

## Instalación detallada

Puedes encontrar una guía de instalación detallada para **pajbot** en el [directorio `install-docs`](./install-docs) de este repositorio.

## Opciones de ejecución

Algunos valores pueden ser configurados para aplicarse a tu bot sin modificar el archivo de configuración, estos son principalmente para cosas fuera del bot.  
Se configuran utilizando variables de entorno. Las siguientes opciones están disponibles:

- `PB1_LOG_HIDE_TIMESTAMPS`  
   Si esta opción se establece en `1`, todas las entradas de registro se imprimirán sin un prefijo de marca de tiempo.
