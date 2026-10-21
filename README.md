# PedidoFácil

Aplicación web Django para gestionar productos y pedidos.

## Requisitos

- Python compatible con las versiones indicadas en `requirements.txt`.
- Una base de datos PostgreSQL en Neon.
- Una cuenta de Render para el despliegue.

## Preparación local (Windows / PowerShell)

1. Descomprime el ZIP y abre una terminal en la carpeta que contiene `manage.py`.
2. Crea y activa el entorno virtual:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Copia `.env.example` a `.env`.
4. En Neon, crea una base de datos PostgreSQL y copia su cadena de conexión a `DATABASE_URL` en `.env`. Genera también una `SECRET_KEY` propia. No compartas el archivo `.env`.
5. Para trabajar localmente, puedes dejar `DEBUG=True` y `ALLOWED_HOSTS=localhost,127.0.0.1`.
6. Ejecuta:

   ```powershell
   python manage.py check
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

7. Abre `http://127.0.0.1:8000/`.

## Despliegue en Render

1. Sube el contenido de esta carpeta a un repositorio Git propio, sin `.env`, `.venv`, `.git` de otro repositorio ni archivos temporales.
2. En Render, crea un **Web Service** conectado a ese repositorio.
3. Build Command: `bash build.sh`
4. Start Command: `gunicorn config.wsgi:application`
5. En **Environment**, configura:
   - `SECRET_KEY`: una clave secreta nueva para producción.
   - `DEBUG`: `False`
   - `DATABASE_URL`: cadena de conexión de la base de datos Neon propia.
   - `ALLOWED_HOSTS`: el dominio asignado por Render, sin `https://`.
6. Despliega y revisa los logs. El script `build.sh` instala dependencias, recopila archivos estáticos y ejecuta las migraciones.
7. Crea el usuario administrador desde la Shell de Render con `python manage.py createsuperuser` si aún no existe.

## Seguridad

- No subas ni compartas `.env`.
- No reutilices las credenciales de otra persona.
- La base de datos nueva empieza vacía; `migrate` crea el esquema, no copia datos de la base original.
