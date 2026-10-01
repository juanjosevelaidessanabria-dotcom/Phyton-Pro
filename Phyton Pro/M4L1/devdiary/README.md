# 🚀 Sprint: DevDiary (Tu propio Diario con Base de Datos)

¡Bienvenido al proyecto DevDiary! Hoy dejaremos de guardar información temporalmente y aprenderemos a usar bases de datos reales.

En este Sprint, el equipo de Frontend ya te ha preparado toda la interfaz de usuario. Tu objetivo como desarrollador Backend es conectar la aplicación web con una base de datos **SQLite** usando **SQLAlchemy** para que la información perdure.

## ⚙️ Antes de empezar

Instala las librerías desde la terminal de tu editor:

```bash
python -m pip install -r requirements.txt
```

> Usamos `python -m pip` y no solo `pip` para asegurarnos de instalar en el mismo Python que ejecuta tu proyecto.

## 📋 Backlog del Sprint (Tus Tareas en main.py)

Busca los comentarios que dicen `TICKET #...` en tu código y resuélvelos en orden:

- [ ] **TICKET #1: Modelado de la Base de Datos**
  - Define las 4 columnas (`id`, `title`, `subtitle`, `text`) de la clase `Card`.
- [ ] **TICKET #2: Crear la Base de Datos (observación)**
  - Ejecuta la app, abre `instance/diary.db` con SQLite Viewer y comprueba que la tabla coincide con tu clase.
- [ ] **TICKET #3: Mostrar todas las entradas**
  - En la ruta `/`, trae todas las tarjetas de la más nueva a la más antigua.
- [ ] **TICKET #4: Vista de detalle por ID**
  - En la ruta `/card/<int:id>`, busca una tarjeta específica.
- [ ] **TICKET #5: Guardar datos (POST)**
  - Crea una nueva `Card` con los datos del formulario, añádela a la sesión y confírmala.

---

## 📖 Chuleta de SQLAlchemy

**Tipos de columna**

| Código | Qué guarda | Ejemplo |
|---|---|---|
| `db.Integer` | Números enteros | un id, una edad |
| `db.String(n)` | Texto corto, máximo `n` caracteres | un título, un nombre |
| `db.Text` | Texto largo, sin límite práctico | el contenido de un post |

**Opciones de columna**

| Opción | Qué hace |
|---|---|
| `primary_key=True` | Identifica cada fila de forma única. SQLite le asigna el número solo (1, 2, 3...) |
| `nullable=False` | El campo es obligatorio: no puede quedar vacío |

**Consultas**

| Código | Qué hace |
|---|---|
| `Card.query` | La "puerta" de entrada a la tabla `card` |
| `.order_by(Card.id)` | Ordena de menor a mayor |
| `.order_by(Card.id.desc())` | Ordena de mayor a menor |
| `.all()` | Trae todos los resultados en una lista |
| `db.get_or_404(Modelo, id)` | Trae UNA fila por su id, o muestra error 404 si no existe |

**Guardar**

| Código | Qué hace |
|---|---|
| `db.session.add(objeto)` | Pone el objeto en el "borrador" (todavía no se guarda) |
| `db.session.commit()` | Confirma el borrador: ahora sí se guarda en `diary.db` |

---

## 🧠 Deep Dive: ¿Qué magia hace `app_context()` bajo el capó?

En el **Ticket #2** viste este código:

```python
with app.app_context():
    db.create_all()
```

¿Por qué no podemos poner `db.create_all()` suelto y ya?

Flask es un framework muy potente que puede ejecutar varias aplicaciones al mismo tiempo. Cuando SQLAlchemy (nuestra base de datos) intenta crear las tablas, necesita saber para qué aplicación en específico está trabajando.

Imagina que tu aplicación Flask es una casa y SQLAlchemy es el electricista. El `with app.app_context():` es como encender el interruptor principal (el "Contexto"). Le dice al electricista: *"Oye, la casa está encendida y activa, entra y haz tu trabajo"*. Adentro de ese bloque, `db.create_all()` revisa tu clase `Card`, la traduce a lenguaje SQL (`CREATE TABLE...`) y construye el archivo `.db` físico. Cuando el bloque termina, el interruptor se apaga de forma segura.

**Ojo:** `create_all()` solo crea las tablas que **no existen**. Si la tabla ya existe, no la toca, aunque hayas cambiado tu clase. Por eso existe `RESET_DB`.

---

## 🆘 Errores comunes

| Si ves... | Significa | Solución |
|---|---|---|
| `could not assemble any primary key columns` | Tu clase `Card` no tiene columnas todavía | Termina el Ticket #1 |
| `no such column: card.subtitle` (u otra columna) | La tabla se creó con una versión vieja de tu clase | Pon `RESET_DB = True`, ejecuta una vez y vuelve a `False`. También puedes borrar la carpeta `instance` |
| `No module named 'flask_sqlalchemy'` | Falta instalar la librería | `python -m pip install -r requirements.txt` |
| Tus entradas desaparecen al reiniciar | Dejaste `RESET_DB = True` | Vuelve a ponerlo en `False` |

---

## 💻 MODO HACKER: Inicializar desde la Terminal

¿Quieres crear la base de datos a mano, como un administrador de sistemas? Borra la carpeta `instance`, abre la Terminal de tu editor y escribe `python` para entrar a la consola interactiva (verás `>>>`):

```python
>>> from main import app, db
>>> app.app_context().push()     # enciende el "interruptor" manualmente
>>> db.drop_all()                # borra todas las tablas
>>> db.create_all()              # vuelve a crearlas
>>> exit()
```

Pregunta para pensar: al hacer `from main import app, db` se ejecuta todo `main.py`... incluido el bloque del Ticket #2. Entonces, ¿en qué momento se creó realmente la tabla?

---

## 🕵️‍♂️ PRO TIP: Inspecciona tu Base de Datos

¿Quieres ver cómo se guarda la información por detrás de la web?

1. Ve a la sección de Extensiones de tu editor, busca **SQLite Viewer** e instálala.
2. En tu explorador de archivos, abre la carpeta `instance` y dale clic a `diary.db`.
3. ¡Verás una tabla real (como un Excel oscuro)! Actualiza esta vista cada vez que crees un post para ver la magia.
