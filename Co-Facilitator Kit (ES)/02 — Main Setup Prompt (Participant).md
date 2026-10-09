---
title: "Prompt de Configuración Principal (Participante) — AI Acceleration Club Fase 0"
created: 2026-07-14
category: reference
status: draft
tags: [aiac, phase0, co-facilitator-kit, participant, setup-prompt, main-setup]
lang: es
translated_from: "02 — Main Setup Prompt (Participant).md"
---

**Apoya:** Pégalo en Claude Code durante el Bloque 2 de la sesión.

# Prompt de Configuración Principal — AI Acceleration Club Fase 0

Este es el prompt que construye todo tu entorno de trabajo: tu vault de Obsidian, tu configuración de Claude Code y tu primer proyecto real (lo vamos a llamar **el caso**). Es autocontenido — todo lo que está debajo de la línea de pegado entra en Claude Code, y Claude te lleva paso a paso, empezando por una entrevista corta para conocer tu trabajo y escoger el caso juntos.

Para ejecutarlo: abre tu terminal, haz `cd` a la carpeta de tu vault de Obsidian, ejecuta `claude` y pega todo lo que está debajo de la línea.

---

> **⚠️ NOTA PARA USUARIOS DE WINDOWS — leer antes de pegar:**
> En PowerShell y Windows Terminal, **Ctrl+V no siempre funciona para pegar bloques largos**.
> Si el prompt no aparece al pegar, usa el **clic del scroll del mouse** (clic medio) o
> **clic derecho** dentro de la terminal. Guarda este tip — lo vas a necesitar en cada paso.
>
> **Si Claude Code te bloquea al editar `~/.claude/settings.json` y menciona "auto mode":**
> Escribe `/model` o cambia el modo a **default** antes de continuar (en la barra inferior
> de Claude Code, cambia de "auto" a "default"). En modo auto, algunas ediciones de
> configuración quedan bloqueadas. Una vez editado el archivo, puedes volver a auto.

---

## PEGA TODO LO QUE ESTÁ DEBAJO EN CLAUDE CODE

---

Me estás ayudando a montar desde cero mi entorno de trabajo completo durante una sesión en vivo de Fase 0 del AI Acceleration Club. Antes de construir nada, me vas a entrevistar para entender mi trabajo y ayudarme a escoger mi primer proyecto real (lo vamos a llamar **el caso**). Después me llevas por la configuración paso a paso, construyendo todo alrededor de ese caso.

**Reglas importantes para esta configuración:**
- Llévame por cada paso UNO A LA VEZ. No vuelques todo de golpe.
- Después de cada paso, confirma qué se creó y pregunta "¿Listo para el siguiente paso?" antes de continuar.
- Si algo falla, ayúdame a resolverlo antes de seguir.
- Todos los archivos de configuración e instrucciones de Claude Code deben vivir dentro de este vault de Obsidian (no escondidos) para que yo pueda verlos y editarlos en Obsidian.
- Empezamos con una entrevista corta (Paso 0) para que entiendas mi trabajo y escojamos el caso juntos — luego construyes todo lo demás alrededor de él.

---

## PASO 0: QUIÉN SOY Y QUÉ VAMOS A CONSTRUIR (ENTREVISTA EN VIVO)

Antes de tocar ningún archivo, conóceme y ayúdame a escoger mi primer proyecto real — **el caso**. Hazlo conversacionalmente, UNA pregunta a la vez. No vuelques todas las preguntas de golpe, y no avances hasta que yo haya respondido.

**1. Mi identidad.** Primero, revisa si mi identidad de Git ya está configurada:

```bash
git config --global user.name
git config --global user.email
```

- Si ambos imprimen un valor, confírmalos conmigo: "Te tengo como `<name>` `<<email>>` — ¿así está bien para tus commits de Git?"
- Si falta alguno, pídeme mi nombre completo y el correo que quiero en mis commits.

Guarda mi nombre y mi correo — los vas a usar en la configuración de Git (Paso 4), en el CLAUDE.md del vault (Paso 2), en las plantillas y en los briefs.

**2. Mi trabajo.** Pregúntame: ¿a qué me dedico? Mi rol, mi organización o equipo, y el tipo de trabajo del que soy responsable en el día a día. Presta atención a las áreas de mi vida laboral — esas se convierten en las áreas de responsabilidad de mi vault en el Paso 1.

**3. Mis problemas.** Pídeme que describa **1–3 problemas reales de trabajo** en los que me gustaría que Claude ayude — las tareas repetitivas, manuales o lentas que se comen mi tiempo. (Me pidieron traerlos a la sesión.) Para cada uno, profundiza un nivel más: qué datos o herramientas están involucrados, con qué frecuencia ocurre y cómo se vería "resuelto".

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

**⚠️ Ubicación y nombre del vault — confírmalo antes de empezar:**
La carpeta de tu vault de Obsidian ya debe existir antes de ejecutar este prompt. Si todavía
no la has creado:
- **Ponle un nombre permanente** (no "Prueba", "Vault2", "Borrador", etc.) — algo como tu
  nombre, tu empresa o "Mi Vault". Vas a usar este nombre durante años.
- **Guárdalo en una ubicación estable:** `Documents/` o tu carpeta de usuario. **NO
  lo guardes en Descargas, el Escritorio, ni en ninguna carpeta que se limpie periódicamente.**
- **macOS:** `~/Documents/Mi Vault/` es el estándar. Abre Obsidian → "Create new vault"
  → ponle nombre → escoge `Documents/` como carpeta madre.
- **Windows:** `C:\Users\[tu nombre]\Documents\Mi Vault\` es el estándar. Evita rutas
  con espacios o caracteres acentuados si puedes.
Dime la ruta completa a la carpeta de tu vault (por ejemplo `C:\Users\Jose\Documents\JRamirez Vault`
o `/Users/jose/Documents/Mi Vault`) antes de empezar — la voy a usar durante toda la configuración.

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

Crea o actualiza `~/.claude/settings.json` con:

```json
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(ls *)",
      "Bash(mkdir *)",
      "Bash(cat *)",
      "Bash(head *)",
      "Bash(wc *)",
      "Glob",
      "Grep"
    ],
    "deny": []
  },
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Blow.aiff"
          }
        ]
      }
    ]
  }
}
```

> **Escoge la línea de sonido del `Stop` según tu sistema operativo — se dispara al final de CADA
> turno, así que un comando equivocado aquí significa un *hook* fallando en cada turno de tu sesión.**
>
> - **macOS:** deja `afplay /System/Library/Sounds/Blow.aiff` tal como está arriba.
> - **Windows (Git Bash / WSL):** `powershell.exe -c "[console]::beep(1000,400)"`
> - **Linux:** `paplay /usr/share/sounds/freedesktop/stereo/bell.oga` (verifica antes con `which paplay`)
> - **No estás seguro / no quieres sonido:** borra el bloque `"Stop"` completo. Es opcional —
>   nada más de la configuración depende de él.

> **Antes de escribir este archivo:** si `~/.claude/settings.json` o `~/.claude/CLAUDE.md`
> ya existen, respáldalos primero — este paso los sobrescribe.
>
> ```bash
> cp -a ~/.claude/settings.json ~/.claude/settings.json.bak 2>/dev/null
> cp -a ~/.claude/CLAUDE.md    ~/.claude/CLAUDE.md.bak    2>/dev/null
> ```
>
> En una máquina nueva ambos comandos no hacen nada, y eso está bien.

> **Por qué esta lista es más corta de lo que esperarías.** Dos cosas se dejaron fuera a propósito:
>
> - **`Bash(python3 *)` y `Bash(pip install *)`.** Python puede leer y escribir cualquier archivo como
>   subproceso, y las reglas de permisos no ven eso. Pre-aprobarlo significaría que cualquier regla
>   `deny` que agregues después es decorativa, a menos que también quites esta línea. Vas a recibir una
>   solicitud de permiso la primera vez que Claude ejecute Python — ese es el resultado correcto el día
>   uno, y puedes aprobarla.
> - **`Read` / `Write` / `Edit` a secas.** Listadas sin una ruta, pre-aprueban esas herramientas para
>   **cualquier lugar de tu disco**, lo que anula el sensato comportamiento por defecto de Claude Code de
>   quedarse en el directorio desde donde lo lanzaste. Dejarlas fuera hace tu configuración **más**
>   acotada, no menos — tu vault se convierte en el límite, gratis.
>
> Todo lo que de verdad hace fluido el día de la sesión (`git`, `ls`, `mkdir`, `cat`, `head`,
> `wc`, `Glob`, `Grep`) sigue estando aquí.

**Qué hace esto:**
- **Permisos:** Pre-aprueba comandos comunes y seguros para que Claude no pida permiso cada vez. Puedes agregar más después.
- **Hook de sonido:** Reproduce un sonido cuando Claude termina una tarea. Esencial cuando te alejas y regresas.

### Router global — `~/.claude/CLAUDE.md`

Ahora crea el **router global** en `~/.claude/CLAUDE.md`. Este es el archivo que hace que Claude Code cargue las reglas de tu vault al inicio de CADA sesión, sin importar desde qué carpeta lo lances. Importan dos partes: ARRIBA va un **router imperativo** (CARGA el CLAUDE.md del vault al arrancar); ABAJO va tu **perfil** (quién eres, qué estás construyendo).

Emite el archivo con esta estructura exacta, llenando `Who I Am`, la ruta del brief del proyecto y la ruta del repositorio a partir de la entrevista del Paso 0 y del caso que escogimos:

```markdown
# CLAUDE.md — Global Router

## Default Workspace

All Claude Code sessions must load and follow the instructions in:

**`<VAULT_PATH>/CLAUDE.md`**

## Rules

1. At session start, read the vault CLAUDE.md above and follow its routing logic.
2. Default working directory is `<VAULT_PATH>/` unless I explicitly specify another.
3. **Code repositories live in `~/dev/<repo-name>` — never inside the vault.**
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

- Language: English. English for code comments and variable names.
- Database access: READ-ONLY by default. Confirm before any write operation.
- No fake data. If you don't have real data, say so.
- After every correction I give you, update the relevant CLAUDE.md so you don't make the same mistake twice.
- Compaction: never accept Claude Code's default **"Resume from summary"** — always choose **"Resume full session"**, or run `/session-close` first. The auto-summary is lossy and silently drops detail.
```

**Importante:**
- Reemplaza `<VAULT_PATH>` (las dos apariciones) con la ruta absoluta real de mi vault — ejecuta `pwd` ahora (estamos en el vault) y usa esa ruta.
- Llena `## Who I Am` con la entrevista del Paso 0, y define la ruta del brief del proyecto y la ruta del repositorio a partir del nombre del caso y del nombre del repositorio que escogimos.
- El bloque router "Default Workspace" DEBE ir arriba, encima del perfil — Claude usa señales de posición en el archivo y el router va primero.

Verifica antes de seguir:

```bash
head -20 ~/.claude/CLAUDE.md
```

Confirma: (1) que la primera sección es `## Default Workspace` (no `## Who I Am`), y (2) que no queda ningún `<VAULT_PATH>` literal. La prueba completa de ruteo desde fuera del vault viene después, en la compuerta de validación final.

Confirma. Pasa al Paso 3.5.

---

## PASO 3.5: MONITOREO DE CONTEXTO (STATUSLINE + PROTECCIONES DE AUTO-COMPACTACIÓN)

> **Por qué existe este paso.** Claude Code tiene una ventana de contexto limitada. Cuando se llena por encima de su umbral por defecto hace **auto-compactación** — resume y bota detalle, y ahí es donde las sesiones pierden trabajo en silencio. Este paso te da una **barra visible** que muestra qué tan lleno está el contexto, una **alerta audible al 50%** y un **freno duro antes de la auto-compactación** para que TÚ decidas cuándo compactar (con `/session-close`, que preserva planes y tareas en disco antes de que hagas `/clear`) en vez de que te agarre por sorpresa. Cuatro capas pequeñas — instala una a la vez y prueba cada una con el pipe-test antes de seguir.

**Primero, detecta mi sistema operativo.** Ejecuta `uname` (macOS/Linux). En Windows, pregúntame si estoy en **PowerShell**, **Git Bash** o **WSL** — la línea de sonido y la ejecución de scripts dependen de eso (notas más abajo).

### Capa 1 — Sube el umbral de auto-compactación a 75% (todos los sistemas; hazlo aunque te saltes el resto)

Fusiona esto dentro del objeto `env` de nivel superior de `~/.claude/settings.json` (el archivo del Paso 3 — **fusiona, no reemplaces el objeto completo**):

```json
"env": { "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "75" }
```

Valida: `jq -e '.env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE' ~/.claude/settings.json` imprime `"75"`. Esta capa es independiente del sistema operativo y es la configuración de seguridad más importante de todas.

### Capa 2 — Barra visible en la statusline con alerta al 50%

La statusline es el ÚNICO lugar que puede ver el % de contexto. Fusiona dentro de `~/.claude/settings.json`:

```json
"statusLine": { "type": "command", "command": "~/.claude/statusline.sh", "padding": 2 }
```

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
    afplay /System/Library/Sounds/Sosumi.aiff >/dev/null 2>&1 &
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

`chmod +x ~/.claude/statusline.sh`.

**Línea de sonido — escoge la mía según el sistema operativo:** macOS deja `afplay /System/Library/Sounds/Sosumi.aiff`. **Linux:** cámbiala por `paplay /usr/share/sounds/freedesktop/stereo/bell.oga` (verifica antes con `which paplay`). **Windows (Git Bash / WSL):** cámbiala por `powershell.exe -c "[console]::beep(1000,400)"`, o borra la línea de `afplay` por completo y quédate solo con la barra visual (el color y el ícono son la señal real; el sonido es opcional).

> **⚠️ Nota para Windows:** `statusline.sh` es un script de bash. Corre tal cual bajo **WSL** o **Git Bash** (instalas Git en el Paso 4 — Git for Windows trae `bash`). Si estás en **PowerShell nativo solamente**, dímelo ahora y te doy una variante de statusline en PowerShell en vez de esta.

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

**Fusiona** (no reemplaces) dentro del objeto `hooks` de nivel superior de `~/.claude/settings.json`:

```json
"UserPromptSubmit": [
  { "hooks": [ { "type": "command", "command": "bash ~/.claude/hooks/context-warn-prompt.sh", "timeout": 3 } ] }
],
"PreCompact": [
  { "matcher": "auto", "hooks": [ { "type": "command", "command": "bash ~/.claude/hooks/context-warn-precompact.sh", "timeout": 3 } ] }
]
```

Valida (los tres deben salir con código 0): `jq -e '.env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE' ~/.claude/settings.json`, `jq -e '.hooks.UserPromptSubmit[0].hooks[0].command' ~/.claude/settings.json`, `jq -e '.hooks.PreCompact[] | select(.matcher=="auto")' ~/.claude/settings.json`. Confirma que `jq . ~/.claude/settings.json` sale con código 0 (sin JSON corrupto).

Dime: qué archivos se crearon/modificaron, si hubo que fusionar *hooks*/`env` existentes, cualquier cambio de sonido por sistema operativo, y que quizá tenga que abrir `/hooks` una vez (o reiniciar Claude Code) para que las nuevas entradas de *hooks* se registren. Termina con: "El monitoreo de contexto está activo. La próxima sesión, cuando el contexto pase de 50%, vas a ver un ⚠ amarillo en la barra de estado, escuchar una alerta y recibir un recordatorio en cada turno hasta que compactes."

Confirma. Pasa al Paso 4.

---

## PASO 4: CONFIGURACIÓN DE GIT

Revisa si Git está instalado:

```bash
git --version
```

- Si está instalado: dime la versión y sigue.
- Si no: dime que abra una ventana de terminal SEPARADA y ejecute `xcode-select --install`, y luego espera a que yo confirme.

Configura mi identidad de Git con el nombre y el correo del Paso 0 (si ya estaba configurada y la confirmé, puedes saltarte esto; si no, configúrala ahora):

```bash
git config --global user.name "<my full name>"
git config --global user.email "<my email>"
```

Confirma. Pasa al Paso 5.

---

## PASO 5: CUENTA DE GITHUB

Pregúntame: **"¿Tienes una cuenta de GitHub? Si sí, ¿cuál es tu nombre de usuario?"**

- Si sí: anota mi nombre de usuario y sigue.
- Si no: llévame a crear una en https://github.com (solo el registro). Después pídeme el nombre de usuario.

**Sobre la autenticación (importa cuando creemos el repositorio y hagamos push, Pasos 6 y 12) — `gh` es OPCIONAL, no es obligatorio para la Fase 0:** Si el CLI `gh` está instalado, `gh auth login` es el camino fácil. Si no lo está (común en Windows corporativo sin derechos de administrador), el primer `git push` abre el navegador vía **Git Credential Manager** (viene con Git for Windows) — o pega un **Personal Access Token** (github.com → Settings → Developer settings → Personal access tokens (classic), *scopes* `repo` + `workflow`) como contraseña cuando git te la pida. Ninguna de las dos vías necesita derechos de administrador. Anota cuál aplica en mi caso para que los Pasos 6 y 12 salgan fluidos.

Pasa al Paso 6.

---

## PASO 6: CREA EL REPOSITORIO — EN `~/dev`

**Crítico:** el repositorio vive en `~/dev/<repo-name>`, NO dentro del vault de Obsidian. Usa el nombre de repositorio que escogimos en el Paso 0.

Dos espacios de trabajo, una sola regla para distinguirlos: **si tiene su propio `.git/`, va en `~/dev/`.** El conocimiento (notas, briefs, gestión de proyectos) vive en el vault. Los repositorios de código viven en `~/dev/`. Un repositorio git anidado dentro del vault pelea con Obsidian — Obsidian reescribe archivos con solo mostrarlos, las tripas de `.git` se agitan en la sincronización y las carpetas de datos inflan el vault.

(Esto NO significa "el código no puede vivir en el vault". Los scripts pequeños que operan sobre el vault mismo — *hooks*, ayudantes, análisis puntuales — se quedan en el vault bajo `05 AI/`. No tienen `.git` propio. La regla es sobre *repositorios*, no sobre *código*.)

> **⚠️ Windows:** `~/dev` funciona tal cual en **Git Bash** y **WSL**. En **PowerShell** nativo la misma carpeta es `$HOME\dev` (o sea `C:\Users\[tu nombre]\dev`). Dime en qué shell estás y uso la forma correcta en todo el proceso.

Como estamos arrancando un proyecto nuevo desde cero, no hay nada que clonar todavía — creamos un repositorio local nuevo. Primero asegúrate de que `~/dev` existe, luego crea e inicializa el repositorio:

```bash
mkdir -p ~/dev
mkdir -p ~/dev/<repo-name>
cd ~/dev/<repo-name> && git init
```

**Verifica que el repositorio quedó en `~/dev` — NO TE SALTES ESTO:**

```bash
cd ~/dev/<repo-name> && test "$(git rev-parse --show-toplevel)" = "$HOME/dev/<repo-name>" \
  && echo "OK — repo is at $HOME/dev/<repo-name>" \
  || echo "WRONG LOCATION: $(git rev-parse --show-toplevel)"
```

Esa sola verificación afirma dos cosas: que el repositorio SÍ está en `~/dev/<repo-name>` y que NO está dentro del vault. Si imprime `WRONG LOCATION`, **PARA** — no sigas con el repositorio en el lugar equivocado. Pégame la ruta que imprimió y lo arreglamos antes del Paso 7.

Pégame la salida del comando de verificación.

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
data/processed/  — clean, final datasets (committed)
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
*.xlsx.bak
.claude/
node_modules/
data/raw/
data/working/
```

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

- Language: English (comments, variable names, and output).
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
- [[AI Acceleration Club - Phase 0 Playbook]]
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

Ve al repositorio `<repo-name>` (en `~/dev` — ver Paso 6) y haz commit de todo:

```bash
cd ~/dev/<repo-name>
git add -A
git commit -m "Initial project setup: CLAUDE.md, folder structure, README, .gitignore"
```

**Ahora ponlo en GitHub bajo mi propia cuenta.** Crea primero el repositorio en GitHub y luego haz push:

- **Si `gh` está instalado:** `gh repo create <repo-name> --private --source=. --remote=origin --push` crea el repositorio bajo mi cuenta y hace push en un solo paso.
- **Si `gh` no está instalado:** crea un repositorio vacío llamado `<repo-name>` en https://github.com/new (bajo mi cuenta, sin README/gitignore/licencia), luego conéctalo y haz push:

```bash
git remote add origin https://github.com/<my-username>/<repo-name>.git
git branch -M main
git push -u origin main
```

**Si el push pide credenciales o falla la autenticación:** `gh` no es obligatorio. El primer push abre el navegador vía **Git Credential Manager** (viene con Git for Windows) — inicia sesión y autoriza. Alternativa manual: cuando git pida usuario/contraseña, usa mi nombre de usuario de GitHub y pega un **Personal Access Token** (github.com → Settings → Developer settings → Personal access tokens (classic), *scopes* `repo` + `workflow`) como contraseña. Ninguna de las dos vías necesita derechos de administrador. (Ver Paso 5.)

Si no podemos conectarnos a GitHub ahora mismo, un commit solo local está bien — nos conectamos después.

Confirma. Pasa al Paso 12.5.

---

## PASO 12.5: AIAC CHEAT SHEET — UBICACIÓN GARANTIZADA EN EL INBOX

Crea un único archivo de referencia rápida que yo siempre pueda encontrar. **Ruta exacta — no la cambies:**

```
00 HUB/00 INBOX/AIAC Cheat Sheet.md
```

Guárdalo en `00 HUB/00 INBOX/` — la carpeta INBOX del vault, creada en el Paso 1. NO lo mandes a `05 AI/`, `CLAUDE CODE RESOURCES/` ni a ninguna carpeta tipo "Cloud Code Resources" — esas son ubicaciones flotantes que no voy a recordar.

Llena el nombre del repositorio, el nombre del proyecto y mi nombre de pila. Contenido (usa cercas de 4 backticks al pegar esto en Claude Code para que los triples backticks anidados no cierren antes de tiempo):

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
3. Configuración global de Claude Code (permisos + notificación de sonido + **monitoreo de contexto** — barra visible en la statusline, ⚠ amarillo al 50% con sonido, umbral de auto-compactación al 75% y un freno duro antes de la auto-compactación para que puedas hacer `/session-close` primero)
4. Git configurado con mi identidad
5. El repositorio de código de mi caso en `~/dev/<repo-name>` — fuera del vault — con CLAUDE.md (contexto completo del proyecto + un puntero de vuelta al brief del vault)
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

1. **Abre Claude Code todos los días** (aunque sean 10 minutos). En la carpeta `<repo-name>`, mete un archivo de datos y pídele a Claude que lo analice.
2. **Reúne tus datos iniciales** y guárdalos en `<repo-name>/data/` (o en la subcarpeta que corresponda)
3. **Ejecuta este prompt** en la carpeta `<repo-name>`:

```
Read the CLAUDE.md and look at the files in the repo.
Create an inventory document mapping what data we have, what's missing,
and how each piece connects to the project goals.
```

**Termina con:** "Ya estás configurado. Cada vez que abras Claude Code en tu carpeta `<repo-name>`, ya conoce todo tu proyecto. Solo dile lo que necesitas."
