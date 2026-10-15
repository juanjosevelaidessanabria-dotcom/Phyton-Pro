# Instructivo: subir DevDiary a Render

> Escrito para: alguien que nunca ha subido una app a internet. Sigue los pasos en orden y no te saltes ninguno.

---

## Antes de empezar

Necesitas tener esto listo:

- [ ] Una cuenta de **GitHub** (github.com)
- [ ] Una cuenta de **Render** (render.com). Puedes entrar con tu cuenta de GitHub.
- [ ] **Git** instalado. Revisa abriendo PowerShell y escribiendo:
  ```powershell
  git --version
  ```
  Si sale un número de versión, está bien. Si sale un error, descarga Git desde https://git-scm.com/downloads e instálalo.

---

## Parte 1: Subir el proyecto a GitHub

### Paso 1.1: Abrir PowerShell en la carpeta del proyecto

1. Abre la carpeta `devdiary-2.0-solucion` en el Explorador de archivos.
2. Haz clic en la barra de direcciones, escribe `powershell` y presiona **Enter**.
3. Se abre una ventana azul de PowerShell ya ubicada en la carpeta correcta.

### Paso 1.2: Crear el archivo `.gitignore`

Este archivo le dice a Git qué **no** debe subir (la base de datos local y archivos basura).

Copia y pega esto en PowerShell y presiona **Enter**:

```powershell
Set-Content -Path .gitignore -Value "diary.db`n__pycache__/`n.venv/" -Encoding utf8
```

No muestra nada si funcionó. Para confirmar, escribe `dir` y debes ver el archivo `.gitignore` en la lista.

### Paso 1.3: Preparar Git en la carpeta

Copia y pega, una línea a la vez, presionando **Enter** después de cada una:

```powershell
git init
```

```powershell
git add .
```

```powershell
git commit -m "Primer commit: devdiary"
```

```powershell
git branch -M main
```

Si `git commit` te pide que configures tu nombre o correo, escribe:

```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu_correo@gmail.com"
```

y luego repite el `git commit`.

### Paso 1.4: Crear el repositorio vacío en GitHub

1. Entra a https://github.com y haz clic en el botón **+** (arriba a la derecha) → **New repository**.
2. En **Repository name** escribe: `devdiary`
3. Deja todo lo demás **sin marcar**. **No** marques "Add a README", ni .gitignore, ni license.
4. Haz clic en **Create repository**.
5. Copia la dirección que aparece, tipo `https://github.com/TU_USUARIO/devdiary.git`.

### Paso 1.5: Enviar el código a GitHub

En PowerShell, reemplaza `TU_USUARIO` por tu usuario de GitHub y ejecuta:

```powershell
git remote add origin https://github.com/TU_USUARIO/devdiary.git
```

```powershell
git push -u origin main
```

- Si se abre una ventana para iniciar sesión en GitHub, inicia sesión.
- Cuando termine, entra a `https://github.com/TU_USUARIO/devdiary` y verifica que veas **`main.py`**, **`requirements.txt`**, las carpetas **`templates`** y **`static`**.

✅ **Parte 1 terminada.** Tu código ya está en GitHub.

---

## Parte 2: Crear la app en Render

### Paso 2.1: Crear el Web Service

1. Entra a https://render.com e inicia sesión.
2. Arriba a la derecha haz clic en **New +**.
3. Elige **Web Service**.

### Paso 2.2: Conectar tu repositorio de GitHub

1. Verás una lista de repositorios. Busca **devdiary** y haz clic en **Connect**.
2. Si no aparece, haz clic en **Configure account** y dale permiso a Render para leer el repositorio `devdiary`. Luego vuelve a intentar.

### Paso 2.3: Llenar el formulario

Llena **exactamente** estos campos:

| Campo | Qué escribir |
|---|---|
| **Name** | `devdiary` (o el nombre que quieras) |
| **Region** | La que quieras (cualquiera sirve) |
| **Branch** | `main` |
| **Root Directory** | **Déjalo VACÍO** |
| **Language** (o Runtime) | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn main:app` |
| **Instance Type** | `Free` |

> ⚠️ Ignora el ejemplo de `yarn` que aparece en otras guías. Eso es para proyectos de Node.js, no para este.

### Paso 2.4: Crear el servicio

1. Baja hasta el final y haz clic en **Create Web Service**.
2. Render empieza a instalar y arrancar la app. Verás texto corriendo en una pantalla negra (son los **Logs**).
3. Espera entre 2 y 5 minutos. Cuando diga algo como **"Your service is live"**, ya está publicada.

✅ **Parte 2 terminada.** Arriba de la página aparece tu URL, tipo `https://devdiary-xxxx.onrender.com`.

---

## Parte 3: Probar que funciona

1. Haz clic en la URL que aparece arriba en Render, o pégala en tu navegador.
2. Si ves la página de DevDiary, **felicidades**, ya está en internet.

> ℹ️ En el plan Free, si nadie entra en unos 15 minutos la app se "duerme". La primera visita después tarda ~30 segundos en cargar. Es normal.

---

## Si algo sale mal

| Qué ves | Qué hacer |
|---|---|
| `git` no se reconoce como comando | Instala Git (ver "Antes de empezar") y cierra y abre PowerShell. |
| `git push` pide usuario y contraseña | Usa tu usuario de GitHub. Como contraseña, GitHub ya no acepta la normal: usa un **Personal Access Token** (GitHub → Settings → Developer settings → Tokens). O inicia sesión con la ventana que se abre. |
| En Render dice `gunicorn: command not found` o `ModuleNotFoundError: gunicorn` | Revisa que `requirements.txt` tenga la línea `gunicorn`. Luego haz commit y push (ver abajo). |
| En Render dice `No module named flask` | El Build Command debe ser exactamente `pip install -r requirements.txt`. |
| La página sale en error 500 | Mira los **Logs** en Render; el error exacto aparece al final, en rojo. |
| Cambié el Start Command y sigue fallando | Asegúrate de que sea exactamente `gunicorn main:app` (sin comillas). |

---

## Actualizar la app después (cuando cambies código)

Cada vez que modifiques algo y quieras publicarlo:

```powershell
git add .
```

```powershell
git commit -m "Describe el cambio"
```

```powershell
git push
```

Render detecta el cambio en GitHub y **vuelve a publicar la app solo**. No tienes que hacer nada en Render.

---

## Notas importantes

- **Los datos se pierden en cada redeploy.** La base de datos es SQLite (`diary.db`) y en el plan Free se borra cada vez que Render vuelve a publicar. Para guardar datos de verdad, hay que usar una base PostgreSQL de Render (eso es otro instructivo).
- **La clave secreta está en el código** (`main.py`, línea 11). Para publicar algo serio, hay que moverla a una variable de entorno en Render.
