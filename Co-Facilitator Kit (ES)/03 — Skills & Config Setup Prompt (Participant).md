---
title: "Skills & Config Setup Prompt (Participant) — AI Acceleration Club Phase 0"
created: 2026-07-14
category: reference
tags: [aiac, phase0, co-facilitator-kit, participant, skills, config, setup-prompt]
lang: es
translated_from: "03 — Skills & Config Setup Prompt (Participant).md"
---

**Apoya:** el Bloque 3 de tu sesión en vivo de Fase 0. Le das este archivo a Claude Code por su ruta cuando tu facilitador te lo indique; no lo pegas.

# Fase 0 — Prompt de Configuración de *Skills* y Config

Este es el **segundo** prompt de la sesión. Va justo después de que el Prompt de Configuración Principal (Doc 2) terminó de armar tu *vault* y tu proyecto. Claude lo lee y te guía paso a paso, uno a la vez.

## Cómo darle este archivo a Claude

Igual que con el Doc 02 — **no lo pegues**, dale a Claude el archivo:

1. Guarda este archivo en tu computadora y copia su ruta completa (macOS: Finder → clic derecho, mantén
   **Option** → **Copiar "…" como nombre de ruta** · Windows: Explorador de archivos → **Shift**+clic
   derecho → **Copiar como ruta de acceso** · Linux: **Copiar ruta**, o arrastra el archivo a la terminal).
2. En la terminal, entra con `cd` a tu *vault* y arranca `claude` (o deja abierta la sesión del Doc 02).
3. Escribe esto, pega la ruta donde dice `<ruta>` y presiona Enter:

   ```
   Lee el archivo <ruta> y sigue sus instrucciones, empezando en "PARA CLAUDE — EMPIEZA AQUÍ".
   ```

4. Si tienes que parar a mitad: vuelve a arrancar Claude en tu *vault* y escribe
   `Lee el archivo <ruta> y continúa desde el Paso N.`

> **Dos cosas que debes saber antes de empezar**
>
> - **Los plugins, *skills* y connectors que instalas durante una sesión se cargan en la *siguiente*
>   sesión.** No aparecen en la sesión que los instaló. El Paso 8 termina con una revisión en una sesión nueva.
> - **¿Cuenta de Claude del trabajo o de la escuela (Team / Enterprise)?** El administrador de tu
>   organización controla qué connectors puedes activar, y puede que ya te dé plugins. El Paso 2 revisa esto primero.

---

## PARA CLAUDE — EMPIEZA AQUÍ

---

Acabamos de terminar de configurar mi *vault* y mi proyecto. Ahora necesito que instales los plugins esenciales, instales las *skills* iniciales y configures algunas cosas más. Guíame paso a paso, uno a la vez. Confirma cada paso antes de seguir.

**Reglas para esta parte:** no me agregues permisos amplios ni permanentes; fusiona en los archivos de configuración que ya existen, nunca los sobrescribas; todo lo que necesite un inicio de sesión con preguntas en pantalla va en una **segunda ventana de terminal** (dame la línea exacta y espera); cuando un paso diga **PARA**, detente de verdad y espérame.

---

## PASO 1: VERIFICAR EL ROUTER GLOBAL CLAUDE.md + PRUEBA DE RUTEO

Mi router global `~/.claude/CLAUDE.md` ya fue creado en el **prompt de Configuración Principal (Doc 2)** — el paso "Global Router". Aquí solo confirmamos que está en su sitio y corremos la prueba de ruteo en vivo antes de instalar *skills*.

Verifica el archivo — vuelve a leer sus primeras 20 líneas y confirma que:
1. La primera sección es `## Default Workspace` (el router imperativo), NO `## Who I Am`.
2. La ruta del *vault* está resuelta (no queda ningún placeholder literal en el archivo).

Luego la **prueba de ruteo desde fuera del vault** — clave para detectar el modo de falla "es solo un perfil, no un router". La hago yo, en una **segunda ventana de terminal**, para que esta sesión siga abierta:

```
cd ~/dev
claude
```

(Si Claude Code pregunta si confías en `~/dev`, responde **Yes** — ahí viven mis repositorios.) Cuando arranque, pregunto: *"¿Qué archivos hay en el INBOX de mi vault?"* Si Claude lee el `00 HUB/00 INBOX/` de mi *vault* sin que yo le dé la ruta, el router está funcionando. Si dice "no sé dónde está tu vault", el router se generó como un documento de perfil, no como router — regresa al paso "Global Router" del prompt de Configuración Principal y vuelve a crear `~/.claude/CLAUDE.md` con el bloque `## Default Workspace` ARRIBA DEL TODO. En cualquier caso, escribo `/exit` en esa segunda ventana y vuelvo aquí a contarte el resultado.

Confirma que ambas verificaciones pasan. Pasa al Paso 2.

---

## PASO 2: INSTALAR PLUGINS

**Primero, revisa qué tipo de cuenta de Claude tengo:**

```bash
grep -o '"organizationType": *"[^"]*"' ~/.claude.json
claude plugin list
```

- **Sin salida, o un tipo personal** → cuenta personal (Pro o Max). Instala los plugins de abajo.
- **Un tipo team o enterprise** → cuenta de organización. Su administrador controla los connectors y
  puede que ya me distribuya plugins. **Usa primero los plugins de la organización:** si `claude plugin list`
  ya muestra un plugin de abajo, no lo instales otra vez. Instala a mano **solo como respaldo** uno que la
  organización no dé — y avísame, porque una copia instalada a mano con el mismo nombre puede tapar
  (ocultar) la copia de la organización. (Si ese tapado pasa igual en Windows no está verificado; revisa
  con `claude plugin list` de todos modos.)

Luego instala lo que falte:

```bash
# Compound Engineering — the Plan -> Build workflow
# Creates structured plans before building, uses parallel research agents
claude plugin marketplace add EveryInc/compound-engineering-plugin
claude plugin install compound-engineering@compound-engineering-plugin
```

```bash
# Superpowers — debugging, brainstorming, TDD, code review
claude plugin install superpowers@claude-plugins-official
```

Si `superpowers` o `playground` dicen que no conocen el marketplace, corre antes `claude plugin marketplace add anthropics/claude-plugins-official`.

Si ninguna funciona, dime qué error te dio y lo resolvemos.

**Después de instalar, explica brevemente qué hace cada plugin:**

- **Compound Engineering:** te da `/ce:plan` (crear un plan estructurado con investigación) y `/ce:work` (ejecutar un plan paso a paso). La idea central: "a menos que sea un cambio de una línea, siempre hay un plan primero".
- **Superpowers:** te da flujos de trabajo estructurados para depuración (`/systematic-debugging`), lluvia de ideas (`/brainstorm`), revisión de código (`/requesting-code-review`) y desarrollo guiado por pruebas (`/test-driven-development`).

Confirma que ambos están instalados: corre `claude plugin list` (la vista de texto normal) y muéstrame las líneas de los dos. Se pueden usar en mi **próxima** sesión — no esperes que `/ce:plan` funcione en esta. Pasa al Paso 2.5.

---

## PASO 2.5: INTEGRACIÓN DE CORREO / WORKSPACE (se ramifica según tu stack de correo de trabajo)

Primero, dime qué stack de correo/calendario usas para el trabajo — eso decide qué camino seguimos:

- **Google Workspace / Gmail** → sigue el **Camino A** abajo
- **Microsoft 365 / Outlook** → sigue el **Camino B**
- **Otra cosa** (Fastmail, Zoho, Proton, etc.) → sigue el **Camino C**

Una vez que te diga, guíame **solo** por el camino que corresponde — ignora los otros dos.

### Camino A — Google Workspace / Gmail (Connectors de claude.ai, por defecto)

Para Gmail, Drive, Calendar y Granola, la **ruta de instalación por defecto son los Connectors de claude.ai** — integraciones OAuth de primera mano gestionadas por Anthropic que funcionan desde Claude desktop y Claude Code sin instalar nada por CLI. Esto cubre ~90% de las necesidades de integración y toma unos 5 minutos en total.

Guíame por esto:

1. Abre la app de escritorio de Claude (o https://claude.ai en el navegador).
2. Ve a **Connectors** (dentro de **Settings** o **Customize**, según la versión de la app) → **Browse / Explore**. En una cuenta del trabajo, si un connector no aparece, el administrador de tu organización tiene que habilitarlo primero — anótalo y sigue.
3. Instala estos connectors uno por uno, aceptando el consentimiento OAuth en cada uno:
   - **Gmail** (leer/enviar/buscar)
   - **Google Drive** (buscar/leer/crear archivos)
   - **Google Calendar** (listar eventos, crear eventos, responder invitaciones)
   - **Granola** (transcripciones de reuniones + resúmenes con IA) — solo si Granola es mi herramienta de reuniones (Paso 2.6)
4. En cada connector, el navegador abre una pantalla de consentimiento de Google. **Si la pestaña del navegador no se abre sola, copia la URL que Claude muestra y pégala en tu navegador manualmente** — este es el punto de fricción más común, no una falla.
5. Después de instalarlos, los connectors quedan disponibles en las sesiones de Claude Code como herramientas `mcp__claude_ai_<connector>__*` — no hace falta más configuración. Igual que los plugins, aparecen de forma confiable en una sesión **nueva**.

**Verificación:** al final de esta configuración, en una sesión nueva (Paso 8), pregunta: *"Lista mis 3 mensajes de Gmail más recientes."* y *"Lista mis próximos eventos de calendario para hoy."* Si ambas devuelven datos reales, los connectors están conectados.

### Camino B — Microsoft 365 / Outlook

Existe un **connector de Microsoft 365** de primera mano (correo y calendario de Outlook, OneDrive, SharePoint, Teams). **Sáltate los connectors de Google de arriba** — no tocan un buzón de Outlook.

1. En la app de escritorio de Claude o en https://claude.ai, ve a **Connectors** → busca **Microsoft 365** → **Connect**, e inicia sesión con mi cuenta de Microsoft.
2. **Cuenta de Microsoft del trabajo o de la escuela:** un administrador de Microsoft tiene que aprobar el connector una vez para toda la organización, y en un plan Team/Enterprise de Claude el dueño de la organización de Claude también tiene que habilitarlo. Si el inicio de sesión dice que hace falta aprobación, **no pelees con eso hoy** — anota "pedirle a TI que apruebe el connector de Microsoft 365" como pendiente de la Semana 1 y sigue. Una cuenta personal de Microsoft no necesita administrador.
3. Por defecto el connector es **de solo lectura** (puede leer correos, eventos y archivos, no enviarlos ni cambiarlos). Ese es el ajuste correcto para la Fase 0.
4. Verificación (en una sesión nueva, Paso 8): *"Lista mis 3 correos más recientes"* y *"¿Qué tengo hoy en el calendario?"*

*(Granola es independiente — si lo usas para tus reuniones, instala solo ese connector.)*

### Camino C — Otro stack / desconocido

Sáltate la integración de correo para la Fase 0 y difiérela a la Fase 1. Dime qué usas (Fastmail, Zoho, Proton, etc.) y evaluamos opciones más adelante. Nada de esto bloquea el resto de la configuración.

Una vez conectado (Google o Microsoft) o saltado (otro) según tu camino, pasa al Paso 2.5b.

---

### PASO 2.5b: CLI DE GOOGLE WORKSPACE (`gws`) — HOY NO

Sáltate esto hoy. Los connectors de arriba ya cubren la lectura de Gmail, Drive, Calendar y Sheets. La herramienta de línea de comandos `gws` es solo para **escribir en Google Sheets desde scripts**, y configurarla toma más de una hora (un cliente OAuth de Google Cloud, habilitar APIs, otorgar scopes).

Si un proyecto más adelante la necesita, configúrala en una sesión dedicada con tu facilitador, y mantenla acotada:

- **Inicia sesión solo con los scopes que el proyecto necesita** (por ejemplo, solo Sheets), no "otorgar todos los scopes".
- **Ninguna regla de permiso amplia** para ella en `allow` (ni para `gws` ni para `~/bin/gws` con comodín). Aprueba sus comandos uno a uno, o agrega una regla exacta para un comando específico de solo lectura que corras seguido.

Dime "anotado" y pasa al Paso 2.6.

---

## PASO 2.6: TRANSCRIPCIONES DE REUNIONES + SKILL /meeting-minutes

Mi herramienta de transcripción de reuniones es **[TOOL]** *(MARCADOR DEL FACILITADOR — reemplázalo antes de enviar: `Granola` · otra herramienta de transcripción por su nombre · `ninguna / transcripción pegada`. Si todavía dice [TOOL], pregúntame cuál uso)*. Instala la *skill* `/meeting-minutes` contra **esa** fuente — no asumas Granola. **Grabar es opcional:** una transcripción pegada funciona igual de bien. Sea cual sea la herramienta, **a todas las personas de una reunión se les pide permiso antes de grabarla.**

**Según la herramienta:**
- **Granola** → en el Paso 2.5 ya instalé el **Connector de Granola** vía claude.ai. Verifícalo: pregunta *"Lista mis 3 reuniones de Granola más recientes."* Si devuelve reuniones reales, funciona; si no, reinstala el connector y **si la pestaña del navegador no se abrió durante el OAuth, copia la URL y pégala manualmente**. La *skill* lee vía las herramientas `mcp__claude_ai_Granola__*`.
- **Cualquier otra herramienta (SpeakUp, Otter, Plaud…)** → si la herramienta publica un servidor MCP o connector, instálalo ahora y verifica listando grabaciones recientes. Si no tiene, la entrada de la *skill* es **una transcripción que yo pego o exporto a un archivo**; no intentes conectar Granola.
- **Ninguna** → la *skill* acepta una transcripción pegada; sáltate cualquier connector.

**Para la prueba no hace falta una reunión real:** basta con una grabación de 30 segundos de mí solo, o una transcripción corta inventada y pegada. No uses una reunión real con clientes ni una reunión interna para la primera prueba.

Guíame por esto:

1. **Verifica la fuente de transcripciones** según la rama de arriba.

2. **Instala la *skill* `/meeting-minutes`** — crea `~/.claude/skills/meeting-minutes/SKILL.md` que:
   - Reciba un ID de reunión de [TOOL] (o pregunte por la última), **o** una transcripción pegada / en archivo cuando no hay connector
   - Traiga la transcripción + el resumen con IA vía el MCP/connector de la herramienta cuando exista (Granola: `mcp__claude_ai_Granola__*`)
   - Genere una nota estructurada de Minuta de Reunión en `03 REFERENCE/<area>/`. Si `Templates/Meeting Minutes Template.md` todavía no existe, créala primero (asistentes, fecha, agenda, decisiones, ítems de acción con responsables, próximos pasos) — el Doc 02 solo entrega una plantilla de Brief de Proyecto
   - Extraiga Decisiones, Ítems de Acción y Próximas Acciones como wikilinks

3. **Verificación:** la *skill* queda disponible en mi **próxima** sesión. En la sesión nueva del final (Paso 8), graba una prueba de 30 segundos en [TOOL] (o pega una transcripción corta inventada) y luego corre `/meeting-minutes latest` (o `/meeting-minutes` y pega). Claude debería leer la transcripción, generar un archivo de minuta y mostrarme la ruta.

Confirma la fuente de transcripciones y que existe `~/.claude/skills/meeting-minutes/SKILL.md`. Pasa al Paso 2.7.

---

## PASO 2.7: INSTALAR LAS SKILLS INICIALES (UN PAQUETE, UN CLON)

Las *skills* iniciales vienen de un solo paquete público y revisado: **`AI-Acceleration/cc-starter-pack`, fijado en la etiqueta `v1.0.0`** (una versión fija, para que cada instalación nueva reciba exactamente los mismos archivos; una *skill* que ya tengas con el mismo nombre se salta y conserva tu versión — mira 2.7a). Trae once *skills*, incluidas las que este kit usa todos los días:

- **`/session-close`** — cierra una sesión: actualiza el brief, registra el trabajo, deja un Continuation Prompt (Paso 4)
- **`/project-create`** — crea un Brief de Proyecto / Programa con preguntas y respuestas guiadas
- **`/inbox-clear`** — procesa `00 HUB/00 INBOX/`: clasifica cada nota, propone movimientos, actúa solo tras la aprobación
- **`/retro`** — retrospectivas de sesión que convierten la fricción en reglas de CLAUDE.md
- **`/skill-create`** — construye *skills* nuevas a partir de una conversación guiada (tu *skill* de revisión semanal de la Semana 1)
- además `/context`, `/permissions`, `/extract`, `/deep-research`, `/deep-planning`, `/fermi-decomposition`

Varias *skills* traen archivos de apoyo junto a su `SKILL.md`, así que instala el paquete completo, no archivos sueltos. La copia del paquete va en `~/.aiac/`, **no** en `~/dev/` — es una herramienta del programa, no uno de mis repositorios.

### 2.7a — Clonar el paquete en `v1.0.0` y correr su instalador

El instalador corre **solo** después de una clonación nueva y exitosa — nunca sobre una copia que quedó de antes:

```bash
mkdir -p ~/.aiac
if [ -e ~/.aiac/cc-starter-pack ]; then
  echo "STOP: ~/.aiac/cc-starter-pack already exists - not installed"
else
  git clone --depth 1 --branch v1.0.0 https://github.com/AI-Acceleration/cc-starter-pack.git ~/.aiac/cc-starter-pack \
    && (cd ~/.aiac/cc-starter-pack && bash ./install.sh)
fi
```

(Los paréntesis mantienen la carpeta de trabajo de esta sesión en el *vault*. El `&&` hace que una
clonación fallida nunca ejecute nada.)

- **Si imprime `STOP`** (existe una copia de un intento anterior), dímelo antes de tocarla. O bien, con
  mi OK, la renombras para quitarla del camino (`mv ~/.aiac/cc-starter-pack ~/.aiac/cc-starter-pack.old`)
  y vuelves a correr el bloque, o la verificas primero — esto instala solo si la copia apunta al
  repositorio oficial, está exactamente en el commit `v1.0.0` de GitHub y no tiene archivos cambiados ni
  de más:

  ```bash
  (cd ~/.aiac/cc-starter-pack \
    && test "$(git remote get-url origin)" = "https://github.com/AI-Acceleration/cc-starter-pack.git" \
    && test -z "$(git status --porcelain --untracked-files=all)" \
    && test "$(git rev-parse HEAD)" = "$(git ls-remote origin 'refs/tags/v1.0.0' 'refs/tags/v1.0.0^{}' | tail -n 1 | cut -f1)" \
    && echo "VERIFIED: v1.0.0, clean" && bash ./install.sh)
  ```

  Si no aparece la línea `VERIFIED`, falló una comprobación y no se instaló nada: muéstramelo y usa el
  camino de renombrar.
- `install.sh` copia cada carpeta de *skill* a `~/.claude/skills/<skill>/`. **Se salta** cualquier *skill* que yo ya tenga con el mismo nombre e imprime `SKIP: …` para ella — esa *skill* se queda con mi versión, no con la de `v1.0.0`. Si ves un `SKIP`, muéstrame la lista y pregúntame qué hacer — nunca sobrescribas una de mis *skills* sin mi OK (`bash ./install.sh force` sobrescribe).
- Termina con "Restart Claude Code": **no reinicies ahora.** Las *skills* se cargan en mi próxima sesión.

### 2.7b — Instalar `/playground` (plugin oficial de Anthropic)

`/playground` es un plugin del marketplace oficial, no una *skill* independiente (en una cuenta de organización, revisa primero `claude plugin list`, como en el Paso 2):

```bash
claude plugin install playground@claude-plugins-official
```

### 2.7c — Verificar

```bash
for skill in session-close project-create inbox-clear retro skill-create meeting-minutes; do
  if [ -f ~/.claude/skills/$skill/SKILL.md ]; then echo "OK      $skill"; else echo "MISSING $skill"; fi
done
claude plugin list
```

Las seis *skills* tienen que imprimir `OK`, y `claude plugin list` tiene que listar `playground`, `compound-engineering` y `superpowers`. Si falta algo, **PARA** y arréglalo (muéstrame el error) antes del Paso 3. Usarlas se prueba en una sesión nueva al final (Paso 8).

---

## PASO 3: CARPETA DE LECCIONES

Crea un archivo de lecciones en mi *vault* en `05 AI/CLAUDE CODE/resources/lessons.md` para capturar las lecciones aprendidas.

Contenido:

```markdown
# Lessons Learned — Claude Code

> One line per lesson. Date + what happened + what to do differently.
> This file grows over time. Claude reads it to avoid repeating mistakes.

## Lessons

| Date | Lesson |
|------|--------|
| YYYY-MM-DD | Setup complete. First session. |
```

Usa la fecha de hoy en la primera fila. Confirma. Pasa al Paso 4.

---

## PASO 4: SESSION-CLOSE — EL ÚNICO HÁBITO QUE IMPORTA

`/session-close` se instaló con el paquete inicial en el Paso 2.7 (`~/.claude/skills/session-close/`). No escribas tu propia versión — lee el `SKILL.md` instalado y explícame en palabras sencillas, en cinco líneas o menos:

1. **Cuándo** correrla: cada vez que termino por ahora, cuando el contexto pasa del ~50%, o después de terminar algo importante.
2. **Qué actualiza:** las Next Actions y el Log del brief del proyecto, y un **Continuation Prompt** arriba de las Next Actions — el bloque que la próxima sesión lee para retomar exactamente donde lo dejé.
3. **Qué nunca hace por su cuenta:** subir código (push), borrar notas o inventar datos. Si ofrece hacer commit, pregunta primero.
4. **Retro:** cuando una sesión tuvo un hito, una falla o fricción repetida, sugiere correr `/retro`.

Luego pasa al Paso 5.

---

## PASO 5: ENTRENAMIENTO EN MODO PLAN

Explícame el Modo Plan. Muéstrame:

1. **Qué es:** un modo especial donde Claude Code crea un plan detallado ANTES de hacer cualquier cambio. No se escribe nada de código hasta que el plan esté aprobado.

2. **Cómo activarlo:** escribe `Shift+Tab` dos veces en el área de entrada de la terminal. El prompt cambia para mostrarte que estás en modo plan.

3. **Cuándo usarlo:**
   - Antes de cualquier tarea que toque más de 1-2 archivos
   - Antes de construir algo nuevo
   - Cuando no estás seguro del enfoque
   - Regla práctica: "si no estás seguro, planifica primero".

4. **El flujo:**
   - Entra en modo plan (Shift+Tab dos veces)
   - Describe lo que quieres construir
   - Claude crea un plan estructurado (archivos a tocar, enfoque, riesgos)
   - Revisa el plan, haz preguntas, ajusta
   - Aprueba -> Claude ejecuta el plan paso a paso

5. **Ejemplo:** pídeme que lo pruebe ahora mismo. Haz que entre en modo plan y escriba un prompt sencillo relacionado con mi proyecto para que vea cómo se ve el plan. Luego salgo del modo plan sin ejecutar (esto es solo práctica).

Pasa al Paso 6.

---

## PASO 6: HOJA DE REFERENCIA DE CONCEPTOS CLAVE

Crea un archivo en mi *vault* en `00 HUB/00 INBOX/Claude Code Cheat Sheet.md`:

````markdown
# Claude Code — Cheat Sheet

## Essential Commands

| Command | What it does |
|---------|-------------|
| `claude` | Start a session in current folder |
| `/exit` | End session |
| `/clear` | Clear context, start fresh |
| `/help` | See all commands |
| `/session-close` | Close session properly (updates project brief, logs work, creates continuation prompt) |
| `Ctrl+C` | Cancel current operation |
| `Escape` | Cancel current input |
| `Shift+Tab` | Switch mode (default → accept edits → Plan Mode); press until the bottom bar shows the one you want |
| `/project-create` | Create a Project/Program brief via guided Q&A (starter pack) |
| `/inbox-clear` | Classify and route 00 HUB/00 INBOX notes (starter pack) |
| `/meeting-minutes` | Turn a meeting transcript into a structured note |
| `/retro` | Run a retrospective on a session, project, or week (starter pack) |
| `/skill-create` | Build a new skill from a guided conversation (starter pack) |
| `/playground` | Build an interactive HTML playground (plugin) |

## Plugin Commands

| Command | Plugin | What it does |
|---------|--------|-------------|
| `/ce:plan` | Compound Engineering | Create a structured plan with parallel research |
| `/ce:work` | Compound Engineering | Execute a plan step by step |
| `/brainstorm` | Superpowers | Explore ideas before building |
| `/systematic-debugging` | Superpowers | Debug systematically instead of guessing |

## Key Concepts

### CLAUDE.md = The Brain
Every folder can have a CLAUDE.md. Claude reads it automatically at session start. It tells Claude who you are, what the project is, and how to behave. **Update it after every correction.**

### Context Window = Your Working Memory
Claude has a limited context window (~200K tokens). As you work, it fills up.
- **At ~50%:** Save state and consider starting fresh (`/session-close` then `/clear`)
- **Never work past 70%** — quality degrades
- **Never accept "Resume from summary"** when Claude Code offers to compact — choose **"Resume full session"** or run `/session-close` first. The auto-summary is lossy (it silently drops detail).
- Starting a new session is cheap. Losing context is expensive.

### Plan First, Build Second
Unless it's a one-line change, always plan before building.
- Quick tasks: just describe what you want
- Medium tasks: use Plan Mode (Shift+Tab twice)
- Big tasks: use `/ce:plan` for full research + planning

### Two Workspaces — Vault (Knowledge) + Repo (Code)
The router (`~/.claude/CLAUDE.md`) makes Claude default to your vault no matter which folder you're in. Your notes live in the vault; your code lives in a git repo under `~/dev/`. Repos live OUTSIDE the vault — the mechanical test: if it has its own `.git/`, it belongs in `~/dev/`.
- **Notes / projects / thinking:** `cd [your vault path] && claude` (vault root)
- **Code / data:** `cd ~/dev/[your repo] && claude` (the repo folder)

**How it syncs:** the repo is git-managed — you `git push`/`git pull` to move code, and the GitHub remote works exactly as usual. Obsidian Sync handles only the `.md` knowledge (notes, briefs). The code itself (`.py`, `.sh`, etc.) does NOT sync via Obsidian — Obsidian Sync excludes those files by default. That's expected and fine: the `.md` travels over Obsidian Sync, the code travels over git. Two channels, two workspaces, linked by a pointer in your project brief.

### Session Close = Compound Learning
Always run `/session-close` before ending. It:
1. Updates your project brief with what you did
2. Creates a Continuation Prompt so the next session picks up exactly where you left off
3. Logs lessons learned
4. Reviews code quality
5. Suggests improvements to CLAUDE.md

**This is what makes Claude Code get smarter over time.** The more you close sessions properly, the better the instructions get.

### The Self-Improvement Loop
1. Work with Claude Code
2. When it makes a mistake, correct it
3. Claude updates CLAUDE.md with the new rule
4. Next session, the mistake doesn't happen again
5. After a few weeks, Claude genuinely gets better — not because the model changes, but because the instructions accumulate.

## Starter Prompts

> Tailor these to your own project — the case you set up in the Main Setup session.

**In the vault — morning check-in:**
```
Read my project brief in 01 PROJECTS/. What are my pending next actions?
What's the most important thing today? If there's a Continuation Prompt, summarize where I left off.
```

**In the repo — first automation:**
```
Read the CLAUDE.md, then look at the files and data in this repo.
For each one, tell me what it contains and how it maps to the project.
Then suggest the first automated report or tool we should build.
```
````

Después de crear el archivo, reemplaza los dos prompts iniciales de arriba con 2-3 prompts hechos a la medida de mi proyecto específico (el caso que armamos en la sesión de Configuración Principal), cubriendo tanto el repositorio como el *vault*. Confirma que el archivo fue creado. Pasa al Paso 7.

---

## PASO 7: PRIMERA PRUEBA

Hagamos una prueba rápida para asegurarnos de que todo funciona. Corre este ejercicio sencillo:

1. Revisa que el CLAUDE.md de este *vault* se pueda leer — léelo y dime la primera línea.
2. Revisa que `~/.claude/CLAUDE.md` exista y tenga la ruta correcta del *vault*.
3. Revisa los permisos de `~/.claude/settings.json` **sin abrir ni imprimir el archivo** (puede
   guardar llaves). Corre esta revisión — solo imprime nombres de reglas:

   ```bash
   python3 - <<'PY'
   import json, os, re
   s = json.load(open(os.path.expanduser("~/.claude/settings.json"), encoding="utf-8"))
   p = s.get("permissions") or {}
   allow = [r for r in p.get("allow") or [] if isinstance(r, str)]
   ask = [r for r in p.get("ask") or [] if isinstance(r, str)]
   broad = [r for r in allow if r in ("Bash", "Bash(*)", "Read", "Write", "Edit", "Glob", "Grep")
            or re.match(r"Bash\((git|gh|gws|cat|head|tail|grep|mkdir)\b.*\*", r)
            or re.match(r"Bash\((python3?|py|node|npx|pip3?)\b", r)]
   need = ["Bash(cat *)", "Bash(head *)", "Bash(tail *)", "Bash(grep *)",
           "Bash(git add *)", "Bash(git commit *)", "Bash(git push *)", "Bash(gh repo create *)"]
   print("broad allow rules:", ", ".join(broad) or "none")
   print("missing ask rules:", ", ".join(r for r in need if r not in ask) or "none")
   print("additionalDirectories:", "present" if "additionalDirectories" in p else "absent")
   PY
   ```

   PASA = `broad allow rules: none`, `missing ask rules: none`, `additionalDirectories: absent`. Si
   aparece otra cosa, muéstrame la línea y pregúntame antes de cambiar nada — yo quito una regla en un
   editor de texto, o te pido volver a correr la fusión del Doc 02 si falta una.
4. Revisa que existan las seis *skills* en `~/.claude/skills/<skill>/SKILL.md` (el bucle del Paso 2.7c): `session-close`, `project-create`, `inbox-clear`, `retro`, `skill-create`, `meeting-minutes`.
5. Revisa con `claude plugin list` que `playground`, `compound-engineering` y `superpowers` estén instalados.
6. Crea un script sencillo de Python en `05 AI/CLAUDE CODE/workspace/hello.py` que imprima un saludo personalizado con las rutas del *vault* y del repositorio.
7. Córrelo una vez (yo apruebo la solicitud — **no** agregues Python a `permissions.allow`) y muéstrame la salida. Si no encuentra `python3`, algo anda mal: Python es un prerrequisito (lo revisa el prevuelo del Doc 01, y el Paso 3 del Doc 02 lo usó). Dímelo, dame la línea de instalación del Doc 01 para correr en una **segunda ventana de terminal** y revisa otra vez. Si hoy no se puede instalar, anótalo para mi facilitador y sigue con el resto de esta lista.

Si todo funciona, pasa al Paso 8.

---

## PASO 8: CONFIGURACIÓN COMPLETA

Dame un resumen final de todo lo de esta sesión:

**Qué se configuró:**
1. `~/.claude/CLAUDE.md` — puntero global a mi *vault* (Claude siempre sabe dónde están mis notas)
2. Plugin Compound Engineering — flujo Plan -> Construir
3. Plugin Superpowers — depuración, lluvia de ideas, revisión de código
4. Connectors — Google (Gmail / Drive / Calendar) o Microsoft 365, más Granola si es mi herramienta de reuniones (otros stacks diferidos; CLI `gws`, hoy no)
5. *Skills* iniciales de `AI-Acceleration/cc-starter-pack` `v1.0.0` (`/session-close`, `/project-create`, `/inbox-clear`, `/retro`, `/skill-create` y más), además de `/meeting-minutes` y el plugin `/playground`
6. Archivo de lecciones — `05 AI/CLAUDE CODE/resources/lessons.md`
7. Modo Plan — aprendiste a planificar antes de construir
8. Hoja de Referencia — referencia rápida en `00 HUB/00 INBOX/`

**Los tres hábitos más importantes:**
1. **Siempre `/session-close` antes de terminar** — esto es lo que te hace más inteligente con el tiempo
2. **Planifica antes de construir** — Shift+Tab hasta llegar al Modo Plan, o `/ce:plan` para tareas grandes
3. **Corrige a Claude y deja que actualice CLAUDE.md** — el bucle de auto-mejora

**Última revisión — en una sesión nueva.** Todo lo que se instaló hoy se carga en una sesión nueva, así que dime que: escriba `/exit`, vuelva a arrancar `claude` en mi *vault*, y luego:

- escriba `/` y confirme que veo `/session-close`, `/project-create`, `/inbox-clear`, `/retro`, `/meeting-minutes`;
- pregunte *"¿Qué plugins están activos?"* (o corra `/plugin`) y confirme Compound Engineering, Superpowers y Playground;
- si configuré connectors: corra las preguntas de verificación de Gmail/Calendar (o de Microsoft 365) del Paso 2.5, y la prueba de `/meeting-minutes` del Paso 2.6.

Si ahí falta algo, reinicia Claude Code una vez más; si sigue faltando, anótalo para mi facilitador.

Termina con: "Tu configuración de Claude Code está completa. Tienes la misma base que los usuarios más productivos de Claude Code. La clave ahora es usarla a diario — aunque sean 10 minutos. Cada sesión hace que la siguiente sea mejor."
