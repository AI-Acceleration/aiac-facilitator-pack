---
title: "Prompt de Configuración Principal (Participante, WINDOWS) — AI Acceleration Club Fase 0"
created: 2026-07-14
category: reference
tags: [aiac, phase0, co-facilitator-kit, participant, setup-prompt, main-setup, windows]
lang: es
translated_from: "02W — Main Setup Prompt (Windows).md"
---

**Apoya:** el Bloque 2 de la sesión. Le das este archivo a Claude Code con su ruta; no lo pegas.

# Prompt de Configuración Principal (WINDOWS) — AI Acceleration Club Fase 0

> ## Tres reglas de Windows — léelas antes de empezar
>
> 1. **Dale a Claude este archivo con su ruta — no lo pegues** (pasos abajo). Para las líneas cortas que
>    sí pegas, usa **clic derecho** en la terminal, no Ctrl+V: Ctrl+V muchas veces falla en las terminales de Windows.
> 2. **Arranca Claude Code desde Git Bash**, no desde PowerShell ni CMD. Los comandos que ejecuta Claude
>    son bash. Git Bash viene con Git for Windows; ábrelo desde el menú Inicio. (Que `where bash` no devuelva nada es normal.)
> 3. **Barras inclinadas `/` en todas las rutas — nunca barras invertidas `\`.** En Git Bash una `\` sin
>    comillas se elimina en silencio y el comando **falla sin ningún error visible**, y el daño se ve
>    exactamente igual que un bug sin relación. Consigue la ruta de tu vault con `pwd -W`, nunca con `pwd` a secas.

Este es el prompt que construye todo tu entorno de trabajo: tu vault de Obsidian, tu configuración de Claude Code y tu primer proyecto real (lo vamos a llamar **el caso**). Es autocontenido: Claude lee este archivo y te lleva paso a paso, empezando por una entrevista corta para conocer tu trabajo y escoger el caso juntos.

> **El método son archivos simples y herramientas estándar** — notas en Markdown dentro de carpetas,
> un repositorio git, unos pocos archivos de configuración. Claude Code es la herramienta recomendada
> hoy para manejarlos, pero nada aquí te amarra: el vault y el repositorio funcionan con cualquier
> editor o herramienta de IA que uses después.

## Cómo darle este archivo a Claude (lee esto primero)

**No copies y pegues este documento.** Es largo, y las terminales cortan los pegados largos (la
terminal de Windows es la peor). Le entregas a Claude el archivo mismo:

1. **Guarda este archivo en tu computadora** — te lo manda tu facilitador, o descárgalo de GitHub
   (abre el archivo → **Download raw file**). Déjalo en un lugar que encuentres, como `Descargas`.
2. **Copia la ruta completa del archivo.**
   En el Explorador de archivos, mantén presionada **Shift**, haz clic derecho sobre el archivo y elige
   **Copiar como ruta de acceso**. (Sale con comillas y barras invertidas — para esta única línea está
   bien; Claude lo maneja.)
3. **Abre la terminal y arranca Claude Code** en la carpeta correcta: haz `cd` a la carpeta de tu
   vault si ya existe (puede que tu pre-vuelo la haya creado); si no, quédate en tu carpeta de
   usuario. La forma fácil: en el Explorador de archivos abre la carpeta del vault, haz clic derecho en
   un espacio vacío → **Open Git Bash here** (en Windows 11 puede estar en **Mostrar más opciones**).
   Escribe `pwd -W` para confirmar la carpeta y luego ejecuta `claude`.
4. Si Claude Code pregunta **"Do you trust the files in this folder?"**, elige **Yes** para tu vault
   o tu carpeta de usuario. **En Windows la opción resaltada por defecto es "No, exit"** — muévete primero a **Yes**.
5. Escribe esto, pega la ruta (clic derecho) donde dice `<ruta>` y presiona Enter:

   ```
   Lee el archivo <ruta> y sigue sus instrucciones, empezando en "PARA CLAUDE — EMPIEZA AQUÍ".
   ```

6. **Si tienes que parar a mitad de camino** (por ejemplo, para cerrar la terminal e instalar algo),
   arranca Claude otra vez en la carpeta de tu vault y escribe:
   `Lee el archivo <ruta> y continúa desde el Paso N.`

> **Si Claude Code te bloquea una edición de `~/.claude/settings.json` y menciona "auto mode":**
> presiona **Shift+Tab** (cada vez que lo presionas cambia el modo que se ve en la barra inferior)
> hasta que muestre el modo normal **default**, sin "auto". En modo auto, algunas ediciones de
> configuración quedan bloqueadas. Cuando termine la edición, puedes presionar Shift+Tab otra vez para volver.

---

## PARA CLAUDE — EMPIEZA AQUÍ

---

**Entorno: Windows.** Ejecuto Claude Code en **Git Bash** (no PowerShell, no CMD). Usa barras
inclinadas `/` en todas las rutas. No me ofrezcas comandos de macOS como `afplay`, `xcode-select`, `brew`
u `open`. Si un paso tiene una rama de macOS y una de Windows, toma la de Windows sin preguntar.

Me estás ayudando a montar desde cero mi entorno de trabajo completo durante una sesión en vivo de Fase 0 del AI Acceleration Club. Antes de construir nada, me vas a entrevistar para entender mi trabajo y ayudarme a escoger mi primer proyecto real (lo vamos a llamar **el caso**). Después me llevas por la configuración paso a paso, construyendo todo alrededor de ese caso.

**Reglas importantes para esta configuración:**
- Llévame por cada paso UNO A LA VEZ. No vuelques todo de golpe.
- Después de cada paso, confirma qué se creó y pregunta "¿Listo para el siguiente paso?" antes de continuar.
- Si algo falla, ayúdame a resolverlo antes de seguir.
- Todos los archivos de configuración e instrucciones de Claude Code deben vivir dentro de este vault de Obsidian (no escondidos) para que yo pueda verlos y editarlos en Obsidian.
- Empezamos con una entrevista corta (Paso 0) para que entiendas mi trabajo y escojamos el caso juntos — luego construyes todo lo demás alrededor de él.
- Cuando un paso diga **PARA**, detente de verdad: muéstrame el mensaje y espera a que yo te diga que sigamos.
- Nunca me agregues un permiso general o permanente. Todo lo que publique algo (un `git push`, crear un repositorio en GitHub) o cambie configuración fuera de este vault, primero me lo explicas y esperas mi OK.
- Nunca abras ni imprimas `~/.claude/settings.json` ni ningún otro archivo que pueda guardar llaves o tokens. El Paso 3 explica cómo fusionar los ajustes sin leerlos.
- Si un archivo que vas a escribir ya existe, **fusiona**: conserva todo lo que yo ya tenía, muéstrame lo que vas a agregar y nunca borres contenido existente.
- Algunas acciones me necesitan en una **segunda ventana de terminal** (inicios de sesión que hacen preguntas en pantalla, instaladores). Cuando pase, dame la línea exacta que debo escribir ahí y espera a que te diga que funcionó.

---

## PASO 0: QUIÉN SOY Y QUÉ VAMOS A CONSTRUIR (ENTREVISTA EN VIVO)

Antes de tocar ningún archivo, conóceme y ayúdame a escoger mi primer proyecto real — **el caso**. Hazlo conversacionalmente, UNA pregunta a la vez. No vuelques todas las preguntas de golpe, y no avances hasta que yo haya respondido.

**1. Mi identidad.** Primero, revisa si mi identidad de Git ya está configurada:

```bash
git config --global user.name
git config --global user.email
```

- Si ambos imprimen un valor, confírmalos conmigo: "Te tengo como `<name>` `<<email>>` — ¿así está bien para tus commits de Git?"
- Si falta alguno, pídeme mi nombre completo y el correo que quiero en mis commits. Menciona que puedo usar mi dirección "no-reply" de GitHub (GitHub → Settings → Emails) si prefiero no poner mi correo real en el historial de commits.

Guarda mi nombre y mi correo — los vas a usar en la configuración de Git (Paso 4), en el CLAUDE.md del vault (Paso 2), en las plantillas y en los briefs.

**2. Mi trabajo.** Pregúntame: ¿a qué me dedico? Mi rol, mi organización o equipo, y el tipo de trabajo del que soy responsable en el día a día. Presta atención a las áreas de mi vida laboral — esas se convierten en las áreas de responsabilidad de mi vault en el Paso 1.

**3. Mis problemas.** Pídeme que describa **1–3 problemas reales de trabajo** en los que me gustaría que Claude ayude — las tareas repetitivas, manuales o lentas que se comen mi tiempo. (Me pidieron traerlos a la sesión.) Para cada uno, profundiza un nivel más: qué datos o herramientas están involucrados, con qué frecuencia ocurre y cómo se vería "resuelto". Recuérdame que para el primer ejercicio de hoy usamos **datos de muestra o no sensibles** — un extracto inventado, una copia anonimizada o un archivo público con la misma forma. Los datos reales del negocio pueden venir después, cuando ya sepa adónde va cada cosa.

**4. Calibración (para fijar el ritmo).** Hazme 1–2 preguntas ligeras para saber cuánto explicar en cada paso — no me examines, mantenlo amable:
- ¿Qué tan cómodo me siento en una terminal / línea de comandos — nunca, un poco, o cómodo?
- ¿He usado Git o GitHub antes?

Usa mis respuestas para calibrar: más explicación y acompañamiento si soy nuevo en la terminal o en Git; un ritmo más rápido si tengo experiencia. Ajusta durante todo el resto de la configuración.

**5. Recomienda el caso.** De mis problemas, recomienda **UNO** como mi primer caso — el mejor proyecto para arrancar la Fase 0. Escoge el que sea (a) suficientemente doloroso para que importe, (b) suficientemente pequeño para mostrar progreso real en la primera semana, y (c) construido sobre datos o archivos a los que de verdad puedo echarle mano. Explica en 2–3 frases por qué ese es el primer proyecto correcto. Después propón:
- un **nombre de proyecto** corto y humano (por ejemplo, "Sales Dashboard", "Invoice Reconciler", "Monthly Report Automation"), y
- un **nombre de repositorio** derivado de él en kebab-case (por ejemplo, `sales-dashboard`, `invoice-reconciler`, `monthly-report`).

**6. Confirma.** Pídeme que confirme el caso, el nombre del proyecto y el nombre del repositorio — o ajústalos conmigo. Una vez que confirme, resúmemelo en una línea: **mi nombre, mi correo, el caso, el nombre del proyecto y el nombre del repositorio.**

En ese punto ya tienes todo lo que necesitas para el resto de la configuración. Lo vas a usar para:
- darle forma a las áreas de responsabilidad de mi vault (Paso 1),
- escribir los CLAUDE.md de mi vault y de mi proyecto (Pasos 2, 8),
- generar el brief de mi proyecto y el MOC de Área (Pasos 10, 11),
- y crear mi repositorio y el primer commit (Pasos 6, 7, 12).

Confirma el resumen conmigo, luego pasa a la verificación de ubicación del vault de abajo y al Paso 1.

---

## VERIFICACIÓN DE LA UBICACIÓN DEL VAULT — antes del Paso 1

El vault es la carpeta donde viven todas mis notas. Claude Code funciona mejor cuando **se arranca
desde dentro de esa carpeta**: la carpeta desde donde lo lanzas es la carpeta de trabajo de Claude.
Revisa dónde estamos:

```bash
pwd -W
ls -a
```

(`pwd -W` imprime la forma `C:/Users/...`, que es la que se usa en todas partes. `pwd` a secas imprime
`/c/Users/...`, que ni las herramientas de Windows ni el router pueden usar.)

**Caso A — ya estamos dentro de mi vault** (lo creó el pre-vuelo, o lo hice yo antes): el
listado muestra una carpeta `.obsidian`, o yo te confirmo que este es mi vault. Sigue con la regla dura de abajo.

**Caso B — todavía no hay vault.** Créalo con estas reglas:

- **Ponle un nombre permanente** — algo como `AIAC-Vault`, mi nombre o mi empresa. No "Prueba",
  "Vault2" ni "Borrador". Lo voy a usar durante años.
- **Ubicación por defecto:** `~/AIAC-Vault` en Git Bash, que es `C:/Users/YOUR-USER/AIAC-Vault` en el
  Explorador de archivos. Una carpeta directamente en mi carpeta de usuario es la opción más segura.
- Créala con `mkdir -p ~/AIAC-Vault` (o el nombre que yo escoja), y luego dime que abra **Obsidian** y
  elija **"Open folder as vault"** (en la pantalla de inicio, o en **Manage vaults**, en el selector de
  vaults de abajo a la izquierda) y escoja **exactamente esa carpeta**. **Nunca "Create new vault"** — eso
  crea una segunda carpeta distinta, y entonces Obsidian y Claude miran dos lugares diferentes.
- Cuando te diga que está abierta, verifica que Obsidian la marcó: `ls -a ~/AIAC-Vault` tiene que
  listar una carpeta `.obsidian`. Si no aparece, Obsidian abrió otra carpeta — **PARA** y ayúdame a
  arreglar eso primero.
- Luego dime que escriba `/exit`, haga `cd` al vault, arranque `claude` otra vez y diga
  `Lee el archivo <ruta> y continúa desde el Paso 1.` Desde ahí, la carpeta de trabajo de Claude es el vault.

**⚠️ REGLA DURA (en los dos casos): el vault NO puede vivir dentro de una carpeta sincronizada con la
nube** — OneDrive, Dropbox, Google Drive (`Google Drive`, `GoogleDrive`, `My Drive`) o iCloud (`iCloud`,
`Mobile Documents`). Los clientes de sincronización pelean con Obsidian y con git y corrompen archivos.
Si la ruta contiene cualquiera de esos nombres, **PARA** y ayúdame a mover el vault a `~/AIAC-Vault`
antes de cualquier otra cosa.

- `Documents` y `Desktop` muchas veces están redirigidas a OneDrive en silencio, aunque la
  ruta no lo diga. Si el vault está bajo `Documents` o `Desktop`, pregúntame si OneDrive respalda esas
  carpetas (ícono de OneDrive → Configuración → Copia de seguridad); si es así o no estoy seguro, usa
  `C:/Users/YOUR-USER/AIAC-Vault`.
- Evita también `Descargas` y cualquier carpeta que se limpie automáticamente.

Cuando la ruta del vault esté resuelta, dime la ruta completa que vas a usar durante toda la configuración (la de `pwd -W`, con barras inclinadas).

---

## PASO 1: ESTRUCTURA DE CARPETAS DEL VAULT

Estamos dentro de la carpeta de mi vault de Obsidian ahora mismo. Crea esta estructura de carpetas PARA. Bajo `02 AREAS/`, crea una subcarpeta por cada área de responsabilidad que conociste en la entrevista del Paso 0 (por ejemplo `Business/`, `Health/`, `Learning/` — y cualquier área específica en la que se centre mi trabajo):

```
00 HUB/00 INBOX/
00 HUB/00 READ_REVIEW/
01 PROJECTS/
02 AREAS/
  [one subfolder per area of my life/work, from the Step 0 interview — always include Learning/]
03 REFERENCE/
04 ARCHIVES/
05 AI/
  CLAUDE CODE/
    workspace/
    resources/
Templates/
```

**Para qué sirve cada carpeta:**
- `00 HUB/00 INBOX/` — Todo lo nuevo aterriza aquí. Se procesa después.
- `00 HUB/00 READ_REVIEW/` — Artículos, videos y enlaces que guardaste pero todavía no has procesado. Léelos y clasifícalos desde aquí, y luego enruta lo que valga la pena conservar.
- `01 PROJECTS/` — Proyectos activos con resultados claros y línea de meta.
- `02 AREAS/` — Responsabilidades continuas (tus áreas de trabajo, salud, aprendizaje).
- `03 REFERENCE/` — Información útil organizada por tema.
- `04 ARCHIVES/` — Proyectos terminados y material inactivo.
- `05 AI/CLAUDE CODE/workspace/` — Archivos de trabajo de Claude (borradores, análisis intermedios).
- `05 AI/CLAUDE CODE/resources/` — Guías, checklists y material de referencia de Claude Code.
- `Templates/` — Plantillas de notas reutilizables.

Confirma qué se creó. Luego pasa al Paso 1.5.

---

## PASO 1.5: AJUSTES DE OBSIDIAN (FILES AND LINKS)

Antes de tocar ningún CLAUDE.md, configura Obsidian mismo para que las notas nuevas caigan en el
lugar correcto y los enlaces nunca se rompan cuando los archivos se muevan. Estos cuatro ajustes son
los que sostienen todo — cada regla y cada *skill* del vault, aguas abajo, los asume.

No puedo hacer clic en la interfaz de ajustes de Obsidian por ti, así que llévame paso a paso. En Obsidian:

**Abre** Settings (ícono de engranaje, abajo a la izquierda, o `Cmd/Ctrl + ,`) → en la barra lateral
izquierda, bajo "Options", haz clic en **Files and links** (las versiones viejas lo llaman "Files & Links").

Configura esto:

| Ajuste | Ponlo en | Por qué |
|---------|--------|-----|
| **Default location for new notes** | "In the folder specified below" | Las notas nuevas van a un lugar conocido, no regadas en la raíz del vault |
| → **Folder to create new notes in** | `00 HUB/00 INBOX` | Coincide con la regla de captura GTD — todo aterriza primero en el INBOX |
| **Use [[Wikilinks]]** | **ON** | Los enlaces usan el formato `[[Note Name]]` — la convención de enlaces del vault; sobrevive a los cambios de nombre y se dibuja en el grafo |
| **Detect all file extensions** (también llamado "show all file types") | **ON** | Los PDF, imágenes, `.json`, `.csv`, etc. se ven en el explorador de archivos en vez de quedar ocultos |
| **Automatically update internal links** | **ON** | Cuando mueves o renombras una nota, cada `[[link]]` hacia ella se actualiza solo — sin enlaces rotos |

Después de que yo los configure, confírmame cuáles cuatro quedaron en ON / configurados, y dime qué
ves bajo "Folder to create new notes in".

> **¿Quieres más?** Los plugins de potencia (Dataview, Tasks, Templater, Calendar, Periodic
> Notes) y los ajustes más profundos son **opcionales** — viven en la sección "Level Up Your
> Obsidian" de tu Brief de Próximos Pasos, cada uno con para qué sirve y cómo configurarlo.
> Sáltatelos por ahora; los cuatro de arriba son todo lo que la Fase 0 necesita.

Confirma. Pasa al Paso 2.

---

## PASO 2: CLAUDE.md DEL VAULT

Crea un archivo llamado `CLAUDE.md` en la raíz del vault (el directorio actual). Este es el archivo más importante — le dice a Claude Code cómo comportarse cada vez que abras una sesión en este vault.

Usa mi nombre de pila (del Paso 0) en el título. Contenido:

```markdown
# CLAUDE.md — My Vault

## Identity

You are an AI assistant helping manage a personal knowledge vault and code projects. The vault uses PARA (Projects, Areas, Reference, Archives) + GTD (Getting Things Done) principles. Your job: help capture, organize, connect, and review notes — and help build real things.

## Vault Root

**Working directory:** This vault folder.

## Folder Structure

```
00 HUB/00 INBOX/       — GTD capture. All new files land here first.
00 HUB/00 READ_REVIEW/ — Saved articles/videos/links awaiting reading + triage
01 PROJECTS/      — Active projects with defined outcomes and finish lines
02 AREAS/         — Ongoing areas of responsibility
03 REFERENCE/     — Useful reference material organized by topic
04 ARCHIVES/      — Completed/inactive projects and notes (cold storage)
05 AI/            — Claude Code workspace and resources
Templates/        — Reusable note templates
```

## Core Rules

### File Safety — CRITICAL
- **New files go to `00 HUB/00 INBOX/`** unless the user specifies otherwise.
- **Never modify existing files** without explicit permission.
- **Never delete files.** Prefer archiving to `04 ARCHIVES/`.
- When a task produces multiple files, create a descriptively named folder inside `00 HUB/00 INBOX/`.

### AI Workspace
- Claude's working files (reports, drafts, intermediate analysis) go in `05 AI/CLAUDE CODE/workspace/`.
- Deliverables that need user review go to `00 HUB/00 INBOX/`.

### Notes
- One note = one idea. Synthesize, don't copy.
- Use `[[wikilinks]]` to connect related notes — but only for real relationships.
- Capture fast, organize later. The inbox exists so you never lose a thought.

### Projects
- Every active project must have: **Outcome** (what "done" looks like), **Next Actions** (at least one), and a **Log**.
- Keep active projects manageable (aim for 5-7 max).
- If a project has no clear outcome, it's not a project — it's an area or a someday-maybe idea.

### Session Close-Out
When ending a work session:
1. Update relevant project Next Actions — check off completed, add new ones.
2. Add a Log entry with the date and what was accomplished.
3. Tell the user what was updated and where.

### Clarify Before Acting
Before executing any non-trivial task:
1. Ask clarifying questions until scope is clear.
2. Surface tradeoffs or alternatives when relevant.
3. Restate what you plan to do.
4. Get explicit confirmation before proceeding.
No silent assumptions. No action before confirmation.

### Surgical Edits
When modifying notes:
- Don't refactor adjacent content.
- Match existing style and formatting.
- Every change must trace directly to what was asked.
- Flag unrelated issues separately.

### Context Management
- Monitor context window usage. At ~50%, alert the user immediately.
- Save state to the active project brief before context fills up:
  - Add a "Continuation Prompt" section with: date, what we were doing, where to resume, key decisions made.
- Never let context silently degrade.

## What Claude Can Do
- Triage and classify inbox notes
- Turn ideas into project briefs with outcome + next actions
- Analyze data files (CSV, Excel, JSON)
- Write and run code (Python, SQL, scripts)
- Find connections between notes across the vault
- Generate reports on project status
- Help build my case project (the first real project we chose in Step 0)
```

Confirma que el archivo se creó. Luego pasa al Paso 3.

---

## PASO 3: CONFIGURACIÓN GLOBAL DE CLAUDE CODE

Ahora configura los ajustes globales de Claude Code. Viven en `~/.claude/settings.json` (fuera del vault — esta es la única excepción, porque Claude Code los exige ahí).

**Primero, respalda lo que ya exista** (en una máquina nueva estos comandos no hacen nada, y eso está bien):

```bash
mkdir -p ~/.claude
cp -a ~/.claude/settings.json ~/.claude/settings.json.bak 2>/dev/null
cp -a ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.bak 2>/dev/null
```

**Luego fusiona — nunca sobrescribas, y nunca muestres lo que ya hay.** `~/.claude/settings.json`
puede guardar llaves de API y tokens (por ejemplo en su bloque `env`), así que **no abras, no leas ni
imprimas el archivo existente** — ni siquiera para mostrarme qué va a cambiar. La fusión se hace en local,
con un script pequeño que imprime solo las entradas propias del kit y los *nombres* de las claves que
yo ya tenía:

1. Muéstrame el bloque de abajo (solo tiene las entradas del kit) y dime qué línea de `Stop` vas a usar
   (mira la nota después del bloque).
2. Guarda el script de fusión que está más abajo como `~/.claude/aiac-merge-settings.py`, exactamente
   como está escrito.
3. Ejecútalo con el bloque por la entrada estándar (Python pide aprobación cada vez — es intencional; nunca respondas "don't ask again") y
   muéstrame su salida. Su última línea tiene que empezar con `Verified:`. Si empieza con `STOP:`, no se
   cambió nada: muéstrame el mensaje y lo arreglamos juntos (mi respaldo es `~/.claude/settings.json.bak`).

   ```bash
   py ~/.claude/aiac-merge-settings.py - <<'JSON'
   <the JSON block below, with the Stop line for my OS>
   JSON
   ```

**Si no hay Python** (es un prerrequisito del Doc 01, así que no debería pasar): si
`~/.claude/settings.json` **no** existe todavía, créalo con exactamente el bloque de abajo; si **sí**
existe, **PARA** y ayúdame primero a instalar Python. Nunca recurras a leer el archivo.

En Windows el comando de Python es `py` (el lanzador del Doc 01); si no encuentras `py`, usa
`python`. Nunca `python3` — en Windows abre la Microsoft Store.

El bloque del kit:

```json
{
  "permissions": {
    "allow": [
      "Bash(git status)",
      "Bash(git status --short)",
      "Bash(git diff)",
      "Bash(git log --oneline)",
      "Bash(git remote -v)",
      "Bash(ls *)",
      "Bash(wc *)"
    ],
    "ask": [
      "Bash(cat *)",
      "Bash(head *)",
      "Bash(tail *)",
      "Bash(grep *)",
      "Bash(git add *)",
      "Bash(git commit *)",
      "Bash(git push *)",
      "Bash(gh repo create *)"
    ],
    "deny": []
  },
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "powershell.exe -c \"[console]::beep(1000,400)\""
          }
        ]
      }
    ]
  }
}
```

> **El beep de Windows ya viene incorporado en el bloque de arriba** — no lo sustituyas por la línea
> `afplay` de macOS que quizás veas en otras copias de este kit. El *hook* `Stop` se dispara al final de
> **cada turno**, así que un comando de macOS aquí significa un *hook* fallando en cada turno de una sesión de 90 minutos.
>
> **Compruébalo ahora:** termina este paso y escucha un beep al final de la próxima respuesta de Claude.
> **¿No hubo beep?** Borra el bloque `"Stop"` completo y sigue adelante — es una comodidad, nada más
> en la configuración depende de él. No gastes tiempo de sesión depurando un sonido.

**El script de fusión** — guárdalo como `~/.claude/aiac-merge-settings.py`. Agrega cada entrada del kit
que falte, conserva cada clave y cada regla `allow`, `ask` y `deny` que yo ya tenga, se niega a tocar un
archivo que no sea JSON válido, conserva los permisos de acceso del archivo, vuelve a leer el resultado
para verificarlo, y de mis ajustes existentes no imprime nada más que nombres de claves:

```python
# aiac-merge-settings.py - merges the AIAC kit's entries into ~/.claude/settings.json.
# It never prints existing values: only the kit entries it added and the names
# of keys you already had. Usage: python3 aiac-merge-settings.py [--replace KEY] - < block
import json
import os
import shutil
import sys

TARGET = os.path.expanduser("~/.claude/settings.json")
DEEP = ("permissions", "hooks", "env")  # top-level objects merged key by key


def merge(dst, new, path, added, kept):
    for key, val in new.items():
        name = ".".join(path + [key])
        if key not in dst:
            dst[key] = val
            added.append(name)
        elif isinstance(val, list) and isinstance(dst[key], list):
            for item in val:
                if item not in dst[key]:
                    dst[key].append(item)
                    added.append(name + ": " + (item if isinstance(item, str) else "1 entry"))
        elif isinstance(val, dict) and isinstance(dst[key], dict) and (path or key in DEEP):
            merge(dst[key], val, path + [key], added, kept)
        elif dst[key] != val:
            kept.append(name)


def missing(dst, new, path, kept):
    gaps = []
    for key, val in new.items():
        name = ".".join(path + [key])
        if name in kept:
            continue
        if key not in dst:
            gaps.append(name)
        elif isinstance(val, list) and isinstance(dst[key], list):
            gaps += [name for item in val if item not in dst[key]]
        elif isinstance(val, dict) and isinstance(dst[key], dict) and (path or key in DEEP):
            gaps += missing(dst[key], val, path + [key], kept)
    return gaps


def replace(dst, new, dotted):
    keys = dotted.split(".")
    for key in keys[:-1]:
        new = new[key]
        if not isinstance(dst.get(key), dict):
            dst[key] = {}
        dst = dst[key]
    dst[keys[-1]] = new[keys[-1]]


def main():
    args, to_replace = sys.argv[1:], []
    while len(args) >= 2 and args[0] == "--replace":
        to_replace.append(args[1])
        args = args[2:]
    if args and args[0] != "-":
        with open(args[0], encoding="utf-8") as f:
            block = json.load(f)
    else:
        block = json.load(sys.stdin)
    if not isinstance(block, dict):
        sys.exit("STOP: the kit block is not a JSON object. Nothing was changed.")
    current = {}
    if os.path.exists(TARGET):
        try:
            with open(TARGET, encoding="utf-8") as f:
                current = json.load(f)
        except ValueError:
            sys.exit("STOP: ~/.claude/settings.json is not valid JSON. Nothing was changed.")
        if not isinstance(current, dict):
            sys.exit("STOP: ~/.claude/settings.json is not a JSON object. Nothing was changed.")
    added, kept = [], []
    for dotted in to_replace:
        try:
            replace(current, block, dotted)
        except (KeyError, TypeError):
            sys.exit("STOP: " + dotted + " is not in the kit block. Nothing was changed.")
        added.append(dotted + " (replaced, as you asked)")
    merge(current, block, [], added, kept)
    kept = [k for k in kept if not any(r.startswith(k + ".") for r in to_replace)]
    if added:
        tmp = TARGET + ".aiac-tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2, ensure_ascii=False)
            f.write("\n")
        if os.path.exists(TARGET):
            shutil.copymode(TARGET, tmp)
        os.replace(tmp, TARGET)
    for name in added:
        print("added: " + name)
    for name in kept:
        print("kept your existing value (not shown): " + name)
    with open(TARGET, encoding="utf-8") as f:
        gaps = missing(json.load(f), block, [], kept)
    if gaps:
        sys.exit("STOP: still missing after the merge: " + ", ".join(gaps))
    print("Verified: settings.json parses and has every kit entry (%d added)." % len(added))


main()
```

> **Qué hace Claude Code sin preguntar, y qué cambian estas reglas.** Importan dos comportamientos por
> defecto ([permisos de Claude Code](https://code.claude.com/docs/en/permissions)): las herramientas de
> archivos de Claude (Read, Glob, Grep) trabajan sin pedir permiso dentro de la carpeta desde donde lo
> lanzaste — tu vault — y preguntan antes de leer en cualquier otro lugar; y un conjunto integrado de
> comandos de solo lectura — entre ellos `ls`, `cat`, `head`, `tail`, `grep`, `find`, `wc` y los `git` de
> solo lectura — se ejecuta **sin pedir permiso, en cualquier lugar de tu disco**. Ese conjunto no se puede
> apagar; la forma documentada de que uno de ellos pida permiso es una regla `ask` (o `deny`). Por eso:
>
> - **`allow` tiene solo comandos de solo lectura:** cinco comandos de git exactos (`git status`,
>   `git status --short`, `git diff`, `git log --oneline`, `git remote -v`) más `ls` y `wc`. Nada de eso
>   escribe, publica ni ejecuta un programa — ni siquiera `mkdir`: crear una carpeta pregunta cada vez.
> - **`ask` convierte en reglas las confirmaciones prometidas.** `cat`, `head`, `tail` y `grep` imprimen
>   el contenido de archivos, así que preguntan cada vez (dentro del vault Claude lee con su herramienta
>   Read, que ahí no pide permiso). `git add`, `git commit`, `git push` y `gh repo create` también
>   preguntan cada vez. Una regla `ask` le gana a cualquier regla `allow` — incluida una guardada al
>   responder "Yes, and don't ask again" — y sigue preguntando en auto mode.
> - **Fuera a propósito:**
>   - **Cualquier comodín de git en `allow`.** Opciones como `--output`, `--ext-diff` o `--template`
>     pueden escribir archivos, ejecutar programas o plantar *hooks* de git, y una regla allow `git diff *`
>     las aprobaría en silencio. (En `ask`, un comodín solo puede agregar preguntas.)
>   - **Python, Node y otros intérpretes, y `pip install`.** Un script puede leer y escribir cualquier
>     archivo como subproceso, y las reglas de permisos no ven eso. Preaprobar un intérprete dejaría
>     decorativa cualquier regla `deny` que agregues después. Vas a recibir una solicitud de permiso cada
>     vez que Claude ejecute uno — apruébala una vez, nunca con "don't ask again".
>   - **Nombres de herramienta a secas — `Read`, `Write`, `Edit`, `Glob`, `Grep`.** Listado sin una
>     ruta, un nombre de herramienta la preaprueba para **cualquier lugar de tu disco**, lo que anula el
>     comportamiento por defecto de Claude Code de trabajar en la carpeta desde donde lo lanzaste. Glob y
>     Grep ya buscan en el vault sin pedir permiso.
>
> **Qué te da esto y qué no:** tu vault es la carpeta de trabajo de Claude. Las herramientas de archivos
> de Claude preguntan antes de leer o escribir fuera de ella, y las reglas `ask` cubren los comandos que
> imprimen archivos o publican. Pero otros comandos de solo lectura como `ls`, `find` y `wc` todavía
> pueden listar nombres de archivos y contar líneas fuera del vault sin preguntar, y un script que
> apruebes puede abrir cualquier archivo. Estas reglas comparan el comando tal como Claude lo escribe:
> son solicitudes de permiso, no un muro. Si quieres un límite duro y verificable, eso es el
> Documento 02-S (el sandbox opcional).

**Qué hace esto:**
- **Permisos:** Preaprueba unos pocos comandos cotidianos de solo lectura para que Claude no pida permiso cada vez, y hace que los comandos que imprimen archivos, hacen commit o publican pregunten cada vez. Todo lo demás sigue el comportamiento por defecto de Claude Code. Puedes agregar más después, una regla a la vez.
- **Hook de sonido:** Reproduce un sonido cuando Claude termina una tarea. Esencial cuando te alejas y regresas.

### Router global — `~/.claude/CLAUDE.md`

Ahora crea el **router global** en `~/.claude/CLAUDE.md`. Este es el archivo que hace que Claude Code cargue las reglas de tu vault al inicio de CADA sesión, sin importar desde qué carpeta lo lances. Importan dos partes: ARRIBA va un **router imperativo** (CARGA el CLAUDE.md del vault al arrancar); ABAJO va tu **perfil** (quién eres, qué estás construyendo).

Emite el archivo con esta estructura exacta, llenando `Who I Am`, la ruta del brief del proyecto y la ruta del repositorio a partir de la entrevista del Paso 0 y del caso que escogimos. **Si `~/.claude/CLAUDE.md` ya existe** (se respaldó arriba), muéstramelo primero: pon este bloque router arriba y conserva mi contenido existente debajo, a menos que yo te diga otra cosa.

```markdown
# CLAUDE.md — Global Router

## Default Workspace

All Claude Code sessions must load and follow the instructions in:

**`<VAULT_PATH>/CLAUDE.md`**

## Rules

1. At session start, read the vault CLAUDE.md above and follow its routing logic.
2. Default working directory is `<VAULT_PATH>/` unless I explicitly specify another.
3. **Code repositories live in `~/dev/<repo-name>` — never inside the vault.**
   (On Windows, `~/dev` in Git Bash is the same folder as `C:/Users/YOUR-USER/dev` in File Explorer — that is where to look for it later.)
   The test is mechanical: if it has its own `.git/`, it belongs in `~/dev/`.
   A git repo nested inside the vault fights Obsidian sync.
4. Scripts that operate on the vault itself (hooks, helpers, skills, analysis
   one-offs) stay in the vault under `05 AI/`. They're part of the vault, not a
   separate project — no `.git` of their own, no move.
5. Do not create files or folders outside the vault and `~/dev/` unless I ask.

---

## Who I Am

<A 2–4 sentence profile of me from the Step 0 interview: my role, my organization/team, the kind of work I do, and the case I'm building.>

## My Projects

My current project brief is at: <VAULT_PATH>/01 PROJECTS/<Project Name>/<Project Name>.md

## My Code Repos

- <Project Name>: ~/dev/<repo-name>

## Defaults

- Language: Spanish. English for code comments and variable names.
- Database access: READ-ONLY by default. Confirm before any write operation.
- No fake data. If you don't have real data, say so.
- After every correction I give you, update the relevant CLAUDE.md so you don't make the same mistake twice.
- Compaction: never accept Claude Code's default **"Resume from summary"** — always choose **"Resume full session"**, or run `/session-close` first. The auto-summary is lossy and silently drops detail.
```

**Importante:**
- Reemplaza `<VAULT_PATH>` (las dos apariciones) con la ruta absoluta real de mi vault — ejecuta **`pwd -W`** ahora (estamos en el vault) y usa esa ruta. Usa `pwd -W`, no `pwd` a secas: `pwd` imprime `/c/Users/...`, que el router no puede resolver, mientras que `pwd -W` imprime `C:/Users/...`, que sí.
- Llena `## Who I Am` con la entrevista del Paso 0, y define la ruta del brief del proyecto y la ruta del repositorio a partir del nombre del caso y del nombre del repositorio que escogimos.
- El bloque router "Default Workspace" DEBE ir arriba, encima del perfil — Claude usa señales de posición en el archivo y el router va primero.

Verifica antes de seguir: lee de vuelta las primeras 25 líneas de `~/.claude/CLAUDE.md` y luego ejecuta:

```bash
# This MUST print 0. Any other number means a backslash path got written into the router,
# which breaks it silently and looks like an unrelated bug.
grep -c '\\' ~/.claude/CLAUDE.md
```

Confirma: (0) que el `grep` imprimió `0`, (1) que la primera sección es `## Default Workspace` (no `## Who I Am`), y (2) que no queda ningún `<VAULT_PATH>` literal. La prueba completa de ruteo desde fuera del vault viene después, en la compuerta de validación final.

Confirma. Pasa al Paso 3.5.

---

## PASO 3.5: MONITOREO DE CONTEXTO (STATUSLINE + PROTECCIONES DE AUTO-COMPACTACIÓN)

> **Por qué existe este paso.** Claude Code tiene una ventana de contexto limitada. Cuando se llena por encima de su umbral por defecto hace **auto-compactación** — resume y bota detalle, y ahí es donde las sesiones pierden trabajo en silencio. Este paso te da una **barra visible** que muestra qué tan lleno está el contexto, una **alerta audible al 50%** y un **freno duro antes de la auto-compactación** para que TÚ decidas cuándo compactar (con `/session-close`, que preserva planes y tareas en disco antes de que hagas `/clear`) en vez de que te agarre por sorpresa. Cuatro capas pequeñas — instala una a la vez y prueba cada una con el pipe-test antes de seguir.

**Sistema operativo:** Windows, Git Bash (declarado arriba). Las líneas de sonido de abajo ya usan el beep de Windows.

**Luego revisa si está `jq`** (una herramienta pequeña para JSON que usan las Capas 2 y 3): ejecuta `jq --version`.
- Si imprime una versión, sigue.
- Si falta (**no** viene incluido con Git for Windows): la línea de instalación es
  `winget install jqlang.jq`. Dame la línea para ejecutar en una **segunda ventana de terminal**, luego haz que cierre y
  vuelva a abrir la terminal y retome desde el Paso 3.5.
- **Si hoy no se puede instalar `jq`** (sin derechos de administrador, sin gestor de paquetes): haz solo
  las Capas 1 y 4, sáltate las Capas 2 y 3, y anótalo como pendiente de la Semana 1. Las verificaciones
  de los ajustes de abajo no necesitan `jq`: el script de fusión del Paso 3 verifica el archivo por sí solo.

### Capa 1 — Sube el umbral de auto-compactación a 75% (todos los sistemas; hazlo aunque te saltes el resto)

Fusiónalo en `~/.claude/settings.json` con el script del Paso 3 (la misma regla: nunca abras el archivo):

```bash
py ~/.claude/aiac-merge-settings.py - <<'JSON'
{ "env": { "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "75" } }
JSON
```

Valida: la última línea del script empieza con `Verified:`. Si reporta
`env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` en una línea `kept your existing value`, yo ya tenía otro valor: dímelo, y solo si yo
te lo pido, ejecútalo otra vez con `--replace env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` antes del `-`.
Esta capa es independiente del sistema operativo y es la configuración de seguridad más importante de todas.

### Capa 2 — Barra visible en la statusline con alerta al 50%

La statusline es el ÚNICO lugar que puede ver el % de contexto. Fusiónala con el script del Paso 3:

```bash
py ~/.claude/aiac-merge-settings.py - <<'JSON'
{ "statusLine": { "type": "command", "command": "~/.claude/statusline.sh", "padding": 2 } }
JSON
```

Si reporta `statusLine` en una línea `kept your existing value`, ya tengo una statusline: dímelo y déjame decidir —
reemplazarla (`--replace statusLine` antes del `-`) o quedarme con la mía y saltar el resto de esta capa.

Escribe `~/.claude/statusline.sh` con EXACTAMENTE este contenido:

```bash
#!/bin/bash
input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name // "Claude"')
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
SID=$(echo "$input" | jq -r '.session_id // "default"')
STATE_FILE="/tmp/claude-ctx-warn-${SID}"

FILLED=$((PCT / 10))
EMPTY=$((10 - FILLED))
BAR=$(printf "%${FILLED}s" | tr ' ' '▓')$(printf "%${EMPTY}s" | tr ' ' '░')

RESET=$'\033[0m'
if [ "$PCT" -ge 75 ]; then
  COLOR=$'\033[1;31m'
  ICON="🚨 "
elif [ "$PCT" -ge 50 ]; then
  COLOR=$'\033[1;33m'
  ICON="⚠ "
  if [ ! -f "$STATE_FILE" ]; then
    powershell.exe -c "[console]::beep(1000,400)" >/dev/null 2>&1 &
    touch "$STATE_FILE"
  fi
else
  COLOR=""
  ICON=""
  [ -f "$STATE_FILE" ] && rm -f "$STATE_FILE"
fi

BRANCH=""
if git rev-parse --git-dir > /dev/null 2>&1; then
  BRANCH=" | $(git branch --show-current 2>/dev/null)"
fi

echo "[$MODEL]$BRANCH | $BAR ${COLOR}${ICON}${PCT}%${RESET}"
```

`chmod +x ~/.claude/statusline.sh` (ejecuta esto en **Git Bash**).

**Línea de sonido — ya viene ajustada para Windows.** El bloque de arriba usa `powershell.exe -c "[console]::beep(1000,400)"`. **No** lo reemplaces por la línea `afplay` de macOS que quizás veas en otras copias de este kit — ese comando no existe en Windows y fallaría cada vez que se dispare la advertencia. Si el beep no funciona o te fastidia, borra esa línea y quédate con la barra visual; el color y el ícono son la señal de verdad.

> **⚠️ Windows — lee esto antes de invertir tiempo en la barra.**
>
> `statusline.sh` es un script de bash y corre bien bajo Git Bash. Pero existe un **bug conocido de Claude
> Code en Windows + Git Bash donde la línea de estado personalizada sencillamente nunca se renderiza**
> ([claude-code#66455](https://github.com/anthropics/claude-code/issues/66455)). Puede que funcione; puede
> que no haga nada en silencio. Eso no es que tu configuración esté mal.
>
> **Si la barra no aparece, prueba en este orden — y detente a los 3 minutos:**
> 1. Cierra Claude Code por completo y vuelve a abrirlo (la línea de estado se carga al arrancar).
> 2. Confirma que el script corre por su cuenta: pásale el JSON de prueba de abajo por *pipe*. Si eso
>    imprime una barra, el script está bien y el bug está en el renderizado, no en tu archivo.
> 3. Prueba con una ruta absoluta en `statusLine.command`: ejecuta el script de fusión con
>    `--replace statusLine.command` antes del `-`, y el bloque
>    `{ "statusLine": { "command": "/c/Users/YOUR-USER/.claude/statusline.sh" } }`.
>
> **Y después sigue adelante de todas formas.** Este es el replanteamiento más importante en Windows:
> **la barra es solo una pantalla. La protección de verdad es el override de auto-compactación al 75%
> más los dos *hooks*** — y ninguno de ellos depende de que la línea de estado se renderice. Siempre
> puedes escribir `/context` para ver exactamente el mismo número. No dejes que un bug cosmético se
> te coma la sesión.

**Pipe-test** (debe imprimir un ⚠ amarillo al 55%):
```bash
echo '{"model":{"display_name":"Opus"},"context_window":{"used_percentage":55},"session_id":"test"}' | bash ~/.claude/statusline.sh
rm -f /tmp/claude-ctx-warn-test
```

### Capa 3 — Recordatorio al modelo al 50% (hook UserPromptSubmit)

El *hook* no puede ver el % de contexto, así que lee el archivo de estado que escribe la statusline. Crea `~/.claude/hooks/` si hace falta y escribe `~/.claude/hooks/context-warn-prompt.sh`:

```bash
#!/bin/bash
input=$(cat)
SID=$(echo "$input" | jq -r '.session_id // "default"')
STATE_FILE="/tmp/claude-ctx-warn-${SID}"

if [ -f "$STATE_FILE" ]; then
  cat <<'EOF'
{"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": "⚠ CONTEXT ≥50%. Auto-compact fires at 75%. Consider running /session-close then /clear to preserve plans/tasks before compaction strips context."}}
EOF
fi
```

`chmod +x ~/.claude/hooks/context-warn-prompt.sh`. **Pipe-test:**
```bash
touch /tmp/claude-ctx-warn-test
echo '{"session_id":"test"}' | bash ~/.claude/hooks/context-warn-prompt.sh | jq -e .
rm -f /tmp/claude-ctx-warn-test
```

### Capa 4 — Freno duro antes de la auto-compactación (hook PreCompact)

Escribe `~/.claude/hooks/context-warn-precompact.sh`:

```bash
#!/bin/bash
cat <<'EOF'
{"continue": false, "stopReason": "Auto-compact paused at 75%. Run /session-close to preserve plans/tasks to disk (then /clear), or run /compact to proceed with default compaction."}
EOF
```

`chmod +x ~/.claude/hooks/context-warn-precompact.sh`. **Pipe-test:** `echo '{}' | bash ~/.claude/hooks/context-warn-precompact.sh | jq -e .`

### Conecta ambos *hooks* en settings.json + verifica

**Fusiónalos** con el script del Paso 3 — agrega las dos entradas junto a los *hooks* que yo ya tenga:

```bash
py ~/.claude/aiac-merge-settings.py - <<'JSON'
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command", "command": "bash ~/.claude/hooks/context-warn-prompt.sh", "timeout": 3 } ] }
    ],
    "PreCompact": [
      { "matcher": "auto", "hooks": [ { "type": "command", "command": "bash ~/.claude/hooks/context-warn-precompact.sh", "timeout": 3 } ] }
    ]
  }
}
JSON
```

Valida: la última línea del script empieza con `Verified:` — vuelve a leer el archivo, confirma que
parsea y que están todas las entradas de este bloque, sin imprimir nada más del archivo. (Vuelve a
ejecutarlo con los bloques de las Capas 1 y 2 si quieres verificarlas otra vez.)

Dime: qué archivos se crearon/modificaron, si hubo que fusionar *hooks*/`env` existentes, cualquier cambio de sonido por sistema operativo, y que la nueva statusline y los *hooks* entran en efecto en mi **próxima** sesión de Claude Code (o después de abrir `/hooks` una vez). Termina con: "El monitoreo de contexto está activo. La próxima sesión, cuando el contexto pase de 50%, vas a ver un ⚠ amarillo en la barra de estado, escuchar una alerta y recibir un recordatorio en cada turno hasta que compactes."

Confirma. Pasa al Paso 4.

---

## PASO 4: CONFIGURACIÓN DE GIT

Revisa si Git está instalado:

```bash
git --version
```

- Si está instalado: dime la versión y sigue.
- Si no: dime que instale **Git for Windows** — en una segunda ventana de terminal `winget install --id Git.Git -e`, o el instalador de https://git-scm.com/download/win (acepta las opciones por defecto, y asegúrate de que **Git Bash** venga incluido) — luego que cierre y vuelva a abrir la terminal, y espera a que yo confirme. NO sugieras `xcode-select` — eso es solo de macOS.

Configura mi identidad de Git con el nombre y el correo del Paso 0 (si ya estaba configurada y la confirmé, puedes saltarte esto; si no, configúrala ahora):

```bash
git config --global user.name "<my full name>"
git config --global user.email "<my email>"
```

Confirma. Pasa al Paso 5.

---

## PASO 5: CUENTA DE GITHUB Y `gh`

Pregúntame: **"¿Tienes una cuenta de GitHub? Si sí, ¿cuál es tu nombre de usuario?"**

- Si sí: anota mi nombre de usuario y sigue.
- Si no: llévame a crear una en https://github.com (solo el registro). Después pídeme el nombre de usuario.

`gh` es la herramienta de línea de comandos de GitHub. Es parte de los prerrequisitos (Documento 01), y
la usamos en el Paso 12 para crear mi repositorio como **Private** y comprobarlo. Revísala:

```bash
gh --version
gh auth status
```

- **`gh` no está instalado:** dame `winget install --id GitHub.cli -e` para ejecutar en una segunda
  ventana de terminal, luego haz que cierre y vuelva a abrir Git Bash y retome desde el Paso 5.
- **`gh` está instalado pero sin sesión iniciada:** no ejecutes tú el inicio de sesión — hace preguntas
  en pantalla que desde aquí no puedes contestar. Dime que ejecute esto en una **segunda ventana de
  terminal**, que siga lo que le pide el navegador y que te avise cuando termine:

  ```
  gh auth login --hostname github.com --git-protocol https --web
  ```

  Luego ejecuta `gh auth status` otra vez, y conecta git con esa sesión para que los push no pidan contraseña:

  ```bash
  gh auth setup-git
  ```

- **Revisa la cuenta:** `gh api user --jq .login` tiene que imprimir el nombre de usuario que te di. Si
  imprime otra cuenta, dímelo y déjame decidir cuál usar — no decidas por mí.
- **`gh` no está instalado y hoy no se puede instalar** (por ejemplo, una laptop del trabajo sin
  derechos de administrador): anótalo, y usamos el camino del navegador en el Paso 12.
  **Git Credential Manager** (incluido con Git for Windows) abre un inicio de sesión en el navegador en
  el primer push. **Nunca crees un *personal access token* clásico** para esto — el inicio de sesión en
  el navegador es más seguro y es todo lo que necesita la Fase 0.

Pasa al Paso 6.

---

## PASO 6: CREA EL REPOSITORIO — EN `~/dev`

**Crítico:** el repositorio vive en `~/dev/<repo-name>`, NO dentro del vault de Obsidian. Usa el nombre de repositorio que escogimos en el Paso 0.

Dos espacios de trabajo, una sola regla para distinguirlos: **si tiene su propio `.git/`, va en `~/dev/`.** El conocimiento (notas, briefs, gestión de proyectos) vive en el vault. Los repositorios de código viven en `~/dev/`. Un repositorio git anidado dentro del vault pelea con Obsidian — Obsidian reescribe archivos con solo mostrarlos, las tripas de `.git` se agitan en la sincronización y las carpetas de datos inflan el vault.

(Esto NO significa "el código no puede vivir en el vault". Los scripts pequeños que operan sobre el vault mismo — *hooks*, ayudantes, análisis puntuales — se quedan en el vault bajo `05 AI/`. No tienen `.git` propio. La regla es sobre *repositorios*, no sobre *código*.)

> **⚠️ Windows:** `~/dev` funciona tal cual en **Git Bash**. En el Explorador de archivos esa misma carpeta es `C:/Users/YOUR-USER/dev`.

Como estamos arrancando un proyecto nuevo desde cero, no hay nada que clonar todavía — creamos un repositorio local nuevo, en una carpeta que **todavía no puede existir**:

```bash
mkdir -p ~/dev
if [ -e ~/dev/<repo-name> ]; then
  echo "STOP: ~/dev/<repo-name> already exists - not touched"
else
  mkdir ~/dev/<repo-name> && cd ~/dev/<repo-name> && git init -b main
fi
```

**Si imprime `STOP`, para.** Una carpeta que ya existe puede tener su propio historial o un `origin` que
apunta a otro lado, y el Paso 12 haría push desde ahí. No la reutilices por tu cuenta: muéstrame qué hay
(`ls -la ~/dev/<repo-name>` y, si es un repositorio git, `git -C ~/dev/<repo-name> remote -v` y
`git -C ~/dev/<repo-name> log --oneline -5`) y déjame decidir. Lo normal es un nombre de repositorio
nuevo. Solo si yo digo explícitamente que esa carpeta es mía y que hay que reutilizarla, la tratamos como
una recuperación: revisamos juntos sus remotos y su historial, y yo decido sobre cada uno antes del Paso 7.

**Verifica que el repositorio quedó en `~/dev` — NO TE SALTES ESTO:**

```bash
cd ~/dev/<repo-name> && test "$(cd "$(git rev-parse --show-toplevel)" && pwd -P)" = "$(cd ~/dev/<repo-name> && pwd -P)" \
  && echo "OK — repo is at ~/dev/<repo-name>" \
  || echo "WRONG LOCATION: $(git rev-parse --show-toplevel)"
```

En Windows, git escribe las rutas como `C:/Users/…` y Git Bash como `/c/Users/…`, así que la
verificación normaliza los dos lados con `cd … && pwd -P` antes de compararlos. Sin eso, un repositorio
bien ubicado mostraría un `WRONG LOCATION` falso.

Esa sola verificación afirma dos cosas: que el repositorio SÍ está en `~/dev/<repo-name>` y que NO está dentro del vault. Si imprime `WRONG LOCATION`, **PARA** — no sigas con el repositorio en el lugar equivocado. Muéstrame la ruta que imprimió y lo arreglamos antes del Paso 7.

Muéstrame la salida del comando de verificación.

> **⚠️ ALTO — consulta con tu facilitador antes de continuar.**
> Muéstrale al facilitador la salida del comando de verificación de arriba para que confirme que el
> repositorio quedó en el lugar correcto antes de que pases al Paso 7.

Pasa al Paso 7.

---

## PASO 7: CONFIGURACIÓN DEL REPOSITORIO

Dentro de la carpeta `<repo-name>`, crea esta estructura. Estas subcarpetas son valores por defecto sensatos para la mayoría de los proyectos — adáptalas al caso si claramente necesita otras:

**Subcarpetas:**
```
data/raw/        — original untouched inputs (gitignored)
data/working/    — intermediate files you are still shaping (gitignored)
data/processed/  — clean, final datasets (gitignored by default — see below)
scripts/         — Python scripts for extraction and analysis
reports/         — generated reports and output
docs/            — project documentation
```

Crea ya las tres subcarpetas de `data/` — tu tarea de la Semana 1 deja un archivo real en
`data/raw/`, así que tiene que existir antes de que te vayas hoy.

**`.gitignore`:**
```
.env
*.pyc
__pycache__/
.DS_Store
Thumbs.db
desktop.ini
*.xlsx.bak
.claude/
node_modules/
data/raw/
data/working/
data/processed/
```

Las tres carpetas de `data/` quedan en el `.gitignore` a propósito: el repositorio es privado, pero
GitHub sigue siendo un tercero, y el primer ejercicio usa datos de muestra de todos modos. Más adelante,
quita la línea `data/processed/` solo para archivos que estés seguro de que se pueden subir a GitHub.

**`README.md`:** Escribe un README para el caso definido en la entrevista del Paso 0. Incluye:
- una descripción de una línea del proyecto y qué problema resuelve,
- la estructura de carpetas de arriba (con una línea cada una),
- una sección corta de "Data Sources" que liste los sistemas/archivos de donde vienen los datos (según la entrevista), y
- cualquier principio o restricción arquitectónica clave que yo haya mencionado.

Confirma. Pasa al Paso 8.

---

## PASO 8: CLAUDE.md DEL REPOSITORIO

Crea un `CLAUDE.md` en la raíz del repositorio `<repo-name>`. Esto le da a Claude Code contexto completo del proyecto cada vez que abras una sesión en esa carpeta.

Genéralo a partir del caso que definimos en la entrevista del Paso 0. Escribe un CLAUDE.md de proyecto enfocado y preciso — no inventes hechos; usa solo lo que yo te dije, y marca como "TBD" lo que siga sin saberse. Incluye estas secciones:

```markdown
# CLAUDE.md — <Project Name>

## Project

<One or two sentences: what this project is and what problem it solves, from the interview.>

## Key Context

<The domain facts that matter: any architectural principle, constraint, or rule I stated. Skip if none.>

## Data Sources

| System / File | Data | Format |
|---------------|------|--------|
| <source> | <what it holds> | <format or TBD> |

## Milestones

<The rough plan we sketched — the first few concrete milestones toward the outcome.>

## Rules

- Language: Spanish for output and documentation; English for code comments and variable names.
- Data files → `data/`; scripts → `scripts/`; generated reports → `reports/`; documentation → `docs/`.
- Explain what you're doing and why before writing code.
- Ask before complex tasks — don't assume.
- <Any project-specific rule, e.g. currency/units conventions, if I mentioned one.>
```

**Después agrega este bloque puente a ese mismo `CLAUDE.md`.** El repositorio (`~/dev/`) y el brief del proyecto (el vault) ahora viven en árboles distintos, así que el enlace entre ambos tiene que quedar escrito. Sin él, una sesión abierta en `~/dev/<repo-name>` no tiene forma de encontrar el brief. Llena las rutas con la ruta de mi vault, el nombre del proyecto y mi nombre de pila:

```markdown
## Where My Notes Live

- **Vault:** `<VAULT_PATH>/`
- **Project brief:** `<VAULT_PATH>/01 PROJECTS/<Project Name>/<Project Name>.md`
- **AIAC Journey brief:** `<VAULT_PATH>/01 PROJECTS/AI Acceleration/<My Name>/AI Acceleration Club - <My Name> Journey.md`

Read the project brief before any non-trivial work in this repo. At the end of a
session, log what was accomplished back to the brief's Log table.
```

Confirma. Pasa al Paso 9.

---

## PASO 9: PLANTILLA DE BRIEF DE PROYECTO

Regresa al vault. Crea el archivo `Templates/Project Brief Template.md` (usa mi nombre completo del Paso 0 como *owner*):

```markdown
---
category: project
status: active
priority: standard
area: ""
owner: "<My Full Name>"
---

# {{title}}

## Outcome

> What does "done" look like? One clear paragraph.

## Why This Matters

- **If this succeeds:** ...
- **If this fails or stalls:** ...

---

## Next Actions

- [ ] First concrete next step
- [ ] Second step

## Waiting For

| Who | What | Since |
|-----|------|-------|
| | | |

## Dependencies

- Dependency 1
- Dependency 2

---

## Key Resources

- [Resource Name](URL)

## People

- **Name** — Role

---

## Plan (Milestones)

| # | Milestone | Target | Status |
|---|-----------|--------|--------|
| 1 | | | Pending |

---

## Working Notes

(scratch space for ideas, analysis, meeting notes)

---

## Log

| Date | Type | Update |
|------|------|--------|
| {{date}} | Milestone | Project created |
```

Esta es la plantilla para cada proyecto nuevo. Cada vez que arranques un proyecto nuevo, copia esta plantilla y llénala.

Confirma. Pasa al Paso 10.

---

## PASO 10: BRIEF DEL PROYECTO

Crea una carpeta dedicada para el **proyecto del caso** en la raíz del vault — `01 PROJECTS/<Project Name>/` — y coloca el brief del proyecto del caso dentro de ella, exactamente como cualquier otro proyecto real (NO va anidado bajo `01 PROJECTS/AI Acceleration/`). Solo el brief del Journey del AI Acceleration Club (Paso 11.5) vive bajo `01 PROJECTS/AI Acceleration/<My Name>/`, porque ese hace seguimiento a tu recorrido en el programa y no al proyecto de negocio.

Crea el archivo en `01 PROJECTS/<Project Name>/<Project Name>.md`. Genéralo a partir de la Plantilla de Brief de Proyecto (Paso 9), llenada con el caso de la entrevista del Paso 0:
- **Outcome:** un párrafo claro que describa cómo se ve "listo" para el caso.
- **Why This Matters:** el beneficio si sale bien, el costo si se estanca — en mis palabras.
- **Next Actions:** los primeros pasos concretos (conseguir los datos, hacer la primera auditoría/inventario, construir el primer prototipo).
- **Waiting For / Dependencies:** cualquier cosa en la que dije que estoy bloqueado o que necesito de alguien más.
- **Key Resources / People:** enlaces, archivos y personas que mencioné; incluye la ruta del repositorio `~/dev/<repo-name>`.
- **Plan (Milestones):** los hitos que esbozamos.
- **Working Notes:** cualquier número, estructura o contexto que compartí.
- **Log:** una entrada con la fecha de hoy — "Project created. Phase 0 setup complete."

Usa solo lo que yo te dije; marca lo desconocido como TBD en vez de inventar detalles. Ejecuta `date +%Y-%m-%d` para la fecha de hoy.

Confirma. Pasa al Paso 11.

---

## PASO 11: MOC DE ÁREA

Crea un Mapa de Contenido simple para el área de negocio a la que pertenece el caso (según el Paso 0), en `02 AREAS/<Area>/<Area>.md`. Usa esta forma:

```markdown
# <Area Name>

Area of responsibility: <one-line description>.

## Active Projects

- [[<Project Name>]] — <one-line description of the case>

## Key Systems

| System | Function |
|--------|----------|
| <system> | <what it does> |

## Key People

- <Name> — <role>
```

Llénalo con la entrevista. Si el caso no encaja limpiamente en un área de negocio, crea el MOC bajo la carpeta de área más cercana de las que hiciste en el Paso 1.

Confirma. Pasa al Paso 11.5.

---

## PASO 11.5: BRIEF DE JOURNEY DEL AI ACCELERATION CLUB

Soy miembro del AI Acceleration Club — el programa de aprendizaje a través del cual estoy construyendo esta configuración de Claude Code. Crea un brief de Journey para que pueda hacerle seguimiento a mi propia progresión por el programa (onboarding de Fase 0 → sprint de la Semana 1 → sesión de círculo de la Fase 2 → maestría a más largo plazo).

**Dónde vive:** `01 PROJECTS/AI Acceleration/<My Name>/` — la carpeta de seguimiento del programa (el proyecto del caso vive en su PROPIA carpeta en `01 PROJECTS/<Project Name>/`, según el Paso 10). Este brief de Journey hace seguimiento a mi recorrido en el programa, aparte del proyecto de negocio.

Usa mi nombre de pila y mi nombre completo (del Paso 0) y la fecha de hoy (`date +%Y-%m-%d`) en todo el archivo. Créalo en: `01 PROJECTS/AI Acceleration/<My Name>/AI Acceleration Club - <My Name> Journey.md`

```markdown
---
tags:
  - project
  - ai-acceleration-club
  - journey
  - actionable
status: active
priority: standard
category: project
description: "My learning journey through the AI Acceleration Club — from Phase 0 onboarding to daily Claude Code fluency. Separate from case projects; this tracks my skill acquisition and program progress."
AREA:
  - "[[Learning]]"
parent: "[[AI Acceleration Club]]"
owner: "<My Full Name>"
created: <TODAY_DATE>
---

# AI Acceleration Club - <My Name> Journey

## Outcome

Reach an expert level of Claude Code fluency by working through Phase 0 → Phase 2 → Phase 3 on real, personal projects. Success = using Claude Code on real work at least 3x per week, with measurable time savings on my most repetitive tasks.

## Why This Matters

- If this succeeds: I stop doing manual work that Claude can automate; my weekly hours shift from busywork to higher-leverage thinking; I can teach the next member when the time comes.
- If this stalls: The setup sits unused; Claude Code feels like a chore instead of a leverage tool; I fall back to manual workflows.

## Next Actions

- [ ] Open Claude Code at least 10 min per day (habit formation — the single most important step of Week 1)
- [ ] Complete the Week 1 homework in [[Next Steps Brief]]
- [ ] Close every session with `/session-close` — no exceptions
- [ ] Capture at least 3 lessons in `05 AI/CLAUDE CODE/resources/lessons.md` this week
- [ ] Run the first real audit of my case data (stored in my case project brief)
- [ ] Schedule Phase 2 check-in with my facilitator once Week 1 is complete

## Waiting For

| Who | What | Since |
|-----|------|-------|
| My facilitator | Phase 2 scheduling (once Week 1 complete) | <TODAY_DATE> |

## Plan

### Milestones

- [x] **M0: Phase 0 Complete** — vault + repo + CLAUDE.md chain + first Claude Code session. *(Completed <TODAY_DATE>)*
- [ ] **M1: Week 1 Sprint Complete** — audit case data, generate first deliverable, capture 3+ lessons.
- [ ] **M2: Phase 2 Session** — hands-on circle session with my facilitator + other members.
- [ ] **M3: First Real Automation** — at least one workflow running end-to-end saving me time weekly.
- [ ] **M4: Phase 3** — Agent teams, skills, MCP. Building my own tools.

### Sessions Log

| Date | Phase | Session | Notes |
|------|-------|---------|-------|
| <TODAY_DATE> | Phase 0 | 1-on-1 with my facilitator | Setup completed. Case project initialized. |

## Reference

- [[AI Acceleration Club]] — master program brief
- [[Next Steps Brief]] — week-by-week homework
- [[<Project Name>]] — my case project

## Log

| Date | Type | Entry |
|------|------|-------|
| <TODAY_DATE> | Milestone | Phase 0 onboarding session completed with my facilitator. Full vault + Claude Code + repo setup operational. |
```

> Si tu vault le pone otro nombre a tu área de aprendizaje/IA, apunta el campo `AREA:` a esa área en vez de `[[Learning]]`.

Confirma. Pasa al Paso 12.

---

## PASO 12: PRIMER COMMIT

Ve al repositorio `<repo-name>` (en `~/dev` — ver Paso 6) y prepara todo para el commit:

```bash
cd ~/dev/<repo-name>
git add -A
git status --short
```

**Muéstrame la lista de archivos preparados y espera mi OK.** Señala todo lo que parezca que no debería
ir a GitHub — un archivo `.env`, contraseñas o llaves, datos reales de clientes o del negocio,
exportaciones grandes. Si tengo dudas sobre un archivo, sácalo del commit y agrégalo al `.gitignore`.
Antes del primer commit todavía no existe `HEAD`, así que `git restore --staged` no funciona aquí — usa
esto (solo lo saca del área de preparación; el archivo se queda en el disco) y luego muéstrame la lista
revisada:

```bash
git rm --cached -- <file>
git status --short
```

Solo después de que yo confirme la lista, haz el commit:

```bash
git commit -m "Initial project setup: CLAUDE.md, folder structure, README, .gitignore"
```

**Ahora ponlo en GitHub — como repositorio Private y bajo la cuenta correcta.** Antes de crear nada,
confirma tres cosas conmigo y espera mi "sí":

1. **Dueño:** la cuenta bajo la que se va a crear (`gh api user --jq .login`, o mi nombre de usuario del Paso 5).
2. **Visibilidad: Private.**
3. **Nombre:** `<repo-name>`.

**Con `gh`** (el camino por defecto):

```bash
gh repo create <owner>/<repo-name> --private --source . --remote origin
```

**Si imprime cualquier error, PARA.** Puede que el nombre ya esté tomado, que ya exista un `origin` o
que haya fallado el inicio de sesión. En todos los casos: no hagas push, no reintentes con otras
opciones y no ejecutes `git remote add` ni `git remote set-url` por tu cuenta. Muéstrame el error y
déjame decidir.

**Sin `gh`** (camino del navegador): llévame por https://github.com/new — **Owner** = mi cuenta,
**Repository name** = `<repo-name>`, selecciona **Private**, y deja sin marcar README, .gitignore y
licencia. Cuando lo haya creado, haz que confirme que la página del repositorio muestra la etiqueta
**Private**. Luego conéctalo:

```bash
git remote add origin https://github.com/<owner>/<repo-name>.git
```

Si imprime cualquier error (por ejemplo `remote origin already exists`), **PARA** igual: no hagas push,
no cambies el remoto, muéstrame el error.

**Antes del push, revisa adónde iría de verdad — en los dos caminos, NO TE SALTES ESTO:**

```bash
git remote get-url --push --all origin
git log --oneline
```

1. **Destino.** El primer comando imprime la dirección a la que git va a hacer push de verdad, después de
   cualquier regla de reescritura de mi configuración de git. Tiene que imprimir **exactamente una
   línea**, y esa línea tiene que ser `https://github.com/<owner>/<repo-name>.git` (o, si uso
   SSH, la forma SSH de GitHub de esa dirección) con el dueño y el nombre que confirmé. Otro dueño, otro
   nombre, otro servidor o más de una línea significa **PARA** — no hagas push.
2. **Visibilidad.** Con `gh`, ejecuta `gh repo view <owner>/<repo-name> --json nameWithOwner,visibility`:
   tiene que imprimir mi `nameWithOwner` **y `"visibility": "PRIVATE"`**. Sin `gh`, yo confirmo la
   etiqueta **Private** en la página del repositorio. Si no es privado, **PARA** y ayúdame primero a
   arreglarlo (en el repositorio: **Settings → General → Danger Zone → Change visibility**).
3. **Qué se va a enviar.** El primer push envía **todo el historial**, no solo los archivos de hoy.
   `git log --oneline` lista cada commit que va a subir, y tiene que mostrar solo el commit que hicimos
   hoy. Cualquier cosa que yo no reconozca significa **PARA**.

Muéstrame los tres resultados y espera mi "sí". Solo entonces haz push (me pide aprobación cada vez — la
regla `ask` del Paso 3 se asegura de eso):

```bash
git push -u origin main
```

**Si el push pide credenciales o falla la autenticación:** con `gh`, ejecuta `gh auth setup-git` y vuelve
a hacer push. Sin `gh`, Git Credential Manager (incluido con Git for Windows) abre un inicio de sesión en
el navegador — inicia sesión y autoriza ahí. **No crees un *personal access token* clásico.** Si sigue
fallando, **PARA** y muéstrame el error para que se lo pueda pasar a mi facilitador.

**Luego verifica que el push de verdad llegó** — pregúntale a GitHub, no lo des por hecho:

```bash
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

Los dos tienen que mostrar el mismo identificador de commit: el segundo viene del propio GitHub. Con
`gh`, `gh repo view <owner>/<repo-name> --json nameWithOwner,visibility` otra vez confirma que el
repositorio sigue siendo `PRIVATE`.

Si no podemos conectarnos a GitHub ahora mismo, un commit solo local está bien por hoy — dilo claramente
en el resumen, y nos conectamos después.

Confirma. Pasa al Paso 12.5.

---

## PASO 12.5: AIAC CHEAT SHEET — UBICACIÓN GARANTIZADA EN EL INBOX

Crea un único archivo de referencia rápida que yo siempre pueda encontrar. **Ruta exacta — no la cambies:**

```
00 HUB/00 INBOX/AIAC Cheat Sheet.md
```

Guárdalo en `00 HUB/00 INBOX/` — la carpeta INBOX del vault, creada en el Paso 1. NO lo mandes a `05 AI/`, `CLAUDE CODE RESOURCES/` ni a ninguna carpeta tipo "Cloud Code Resources" — esas son ubicaciones flotantes que no voy a recordar.

Llena el nombre del repositorio, el nombre del proyecto y mi nombre de pila. Contenido (la cerca exterior de 4 backticks de abajo solo está para que los bloques anidados de triple backtick se vean bien; escribe el archivo sin ella):

````markdown
# AIAC Cheat Sheet — Quick Reference

> **Location:** `00 HUB/00 INBOX/AIAC Cheat Sheet.md` — this is your one-stop quick-reference. Pin this file in Obsidian.

## Start a session

```bash
cd "[vault path]" && claude       # vault session (notes, projects, thinking)
cd ~/dev/<repo-name> && claude    # repo session (data, code)
```

## Resolve a project from anywhere

In a fresh Claude Code session (any cwd), type:

```
let's work on my <Project Name> project
```

The router (in `~/.claude/CLAUDE.md`) resolves to your **case project** brief in
`01 PROJECTS/<Project Name>/`. No `cd` needed.

To reach your **program journey** brief instead, say *"let's work on my AI Acceleration
journey"* — that one lives at `01 PROJECTS/AI Acceleration/<My Name>/`.

## Essential commands

| Command | What it does |
|---------|-------------|
| `/session-close` | Close session properly — updates brief, logs work, creates continuation prompt. **Never end without this.** |
| `/context` | Show context window usage |
| `/clear` | Reset session (after `/session-close`) |
| `/project-create` | Create a NEW project brief through guided Q&A — use this for project #2 onwards |
| `/help` | List available commands |
| `Shift+Tab Shift+Tab` | Enter Plan Mode (review before executing) |

## Context window thresholds

- ≤50% → keep working
- 50% → ideal compaction point (`/session-close` then `/clear`)
- 70% → quality cliff; do not cross mid-task

## When stuck

24 hours of solo debugging first. Then ping your facilitator with: the prompt, the error, and what you already tried.

If blocked on tool install / auth / MCP config → ping immediately (don't burn a day on infra).

## Where things live

- **Vault** = knowledge (notes, briefs, project management)
- **`~/dev/`** = code repositories. If it has its own `.git/`, it lives here.

## File anchors

- Vault root CLAUDE.md: `[vault]/CLAUDE.md`
- Repo CLAUDE.md: `~/dev/<repo-name>/CLAUDE.md`
- Case project brief: `[vault]/01 PROJECTS/<Project Name>/<Project Name>.md`
- AIAC Journey brief: `[vault]/01 PROJECTS/AI Acceleration/<My Name>/AI Acceleration Club - <My Name> Journey.md`
- Next Steps Brief (homework): `[vault]/00 HUB/00 INBOX/Next Steps Brief.md`
- Lessons log: `[vault]/05 AI/CLAUDE CODE/resources/lessons.md`
````

Confirma. Pasa al Paso 13.

---

## PASO 13: CONFIGURACIÓN COMPLETA — RESUMEN Y PRÓXIMOS PASOS

Dame un resumen final:

**Qué se configuró:**
1. Vault de Obsidian con estructura PARA + espacio de trabajo de IA — más los ajustes centrales de Files and links (notas nuevas → `00 HUB/00 INBOX`, wikilinks ON, todos los tipos de archivo visibles, actualización automática de enlaces internos ON)
2. CLAUDE.md del vault (las reglas de comportamiento de Claude)
3. Configuración global de Claude Code, fusionada con lo que ya había sin mostrarlo (una lista corta de permisos de solo lectura, y reglas `ask` para que imprimir archivos, hacer commit y publicar siempre pregunten — nada que escriba, publique o ejecute scripts queda preaprobado — más notificación de sonido + **monitoreo de contexto** — barra visible en la statusline, ⚠ amarillo al 50% con sonido, umbral de auto-compactación al 75% y un freno duro antes de la auto-compactación para que puedas hacer `/session-close` primero)
4. Git configurado con mi identidad
5. El repositorio de código de mi caso en `~/dev/<repo-name>` — fuera del vault — con CLAUDE.md (contexto completo del proyecto + un puntero de vuelta al brief del vault), subido a GitHub como repositorio **Private** (o solo local por ahora, si no pudimos conectarnos)
6. Plantilla de Brief de Proyecto para proyectos futuros
7. El brief de mi proyecto del caso con todo el detalle (outcome, hitos, contactos) en `01 PROJECTS/<Project Name>/` — la carpeta PROPIA del proyecto del caso (solo el brief de Journey vive bajo `01 PROJECTS/AI Acceleration/<My Name>/`)
8. MOC de Área que enlaza todo
9. Brief de Journey del AI Acceleration Club (hace seguimiento a mi avance en el programa de aprendizaje mismo) — vive en mi carpeta de participante
10. AIAC Cheat Sheet en `00 HUB/00 INBOX/AIAC Cheat Sheet.md` (referencia rápida canónica — siempre vive ahí)

**Dónde vive cada cosa:**
- Vault: [muestra la ruta] — **conocimiento**: notas, briefs, gestión de proyectos
- Repositorio: `~/dev/<repo-name>/` — **código**, fuera del vault. Regla práctica: si tiene su propio `.git/`, vive en `~/dev/`.
- Scripts del lado del vault (*hooks*, ayudantes, *skills*): se quedan en el vault bajo `05 AI/` — no son repositorios, así que no se mueven
- Configuración de Claude Code: ~/.claude/settings.json

**Comandos esenciales:**

| Comando | Qué hace |
|---------|-------------|
| `claude` | Inicia una sesión de Claude Code |
| `/exit` | Termina la sesión |
| `/clear` | Limpia el contexto y arranca de cero |
| `/help` | Ver todos los comandos |
| `Ctrl+C` | Cancela la operación actual |
| `Escape` | Cancela la entrada actual |

**Dos formas de usar Claude Code:**

1. **En el vault** (`cd [vault path] && claude`) — para notas, gestión de proyectos, pensar, investigar
2. **En el repositorio** (`cd ~/dev/<repo-name> && claude`) — para análisis de datos, programar, construir

Claude lee el CLAUDE.md de la carpeta en la que estés. Ya sabe todo sobre tu proyecto.

**La tarea de esta semana (3 tareas):**

1. **Abre Claude Code todos los días** (aunque sean 10 minutos). En la carpeta `<repo-name>`, mete un archivo de datos de muestra (o no sensible) en `data/raw/` y pídele a Claude que lo analice.
2. **Reúne tus datos iniciales** y guárdalos en `<repo-name>/data/raw/` (está en el `.gitignore` — se queda en tu máquina)
3. **Ejecuta este prompt** en la carpeta `<repo-name>`:

```
Read the CLAUDE.md and look at the files in the repo.
Create an inventory document mapping what data we have, what's missing,
and how each piece connects to the project goals.
```

**Termina con:** "Ya estás configurado. Cada vez que abras Claude Code en tu carpeta `<repo-name>`, ya conoce todo tu proyecto. Solo dile lo que necesitas."
