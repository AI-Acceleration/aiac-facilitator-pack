---
title: "Skills & Config Setup Prompt (Participant, WINDOWS) — AI Acceleration Club Phase 0"
created: 2026-07-14
category: reference
status: draft
tags: [aiac, phase0, co-facilitator-kit, participant, skills, config, setup-prompt, windows]
lang: es
translated_from: "03W — Skills & Config Setup Prompt (Windows).md"
---

**Apoya:** el Bloque 3 de tu sesión en vivo de Fase 0. Pega el bloque de abajo en Claude Code cuando tu facilitador te lo indique.

# Fase 0 — Prompt de Configuración de *Skills* y Config (WINDOWS)

> ## Las mismas tres reglas de Windows del Doc 02
>
> 1. **Clic derecho para pegar**, no Ctrl+V.
> 2. **Git Bash**, no PowerShell y no CMD.
> 3. **Barras normales `/` en todas las rutas.** Una `\` sin comillas se elimina en silencio en Git Bash y
>    el comando falla sin error visible.
>
> **Si abriste una sesión nueva de Claude Code desde el Doc 02, pega esto primero:**
>
> ```
> Environment: Windows, Git Bash. Forward slashes in all paths. Do not offer me macOS commands
> (afplay, xcode-select, brew, open) or macOS paths (~/Library/...). Take the Windows branch
> without asking.
> ```

Este es el **segundo** prompt que vas a pegar en Claude Code durante la sesión. Va justo después de que el Prompt de Configuración Principal (Doc 2) terminó de armar tu *vault* y tu proyecto. Pega todo lo que está debajo de la línea en Claude Code y deja que te guíe paso a paso, uno a la vez.

---

## PEGA TODO LO QUE ESTÁ ABAJO EN CLAUDE CODE

---

Acabamos de terminar de configurar mi *vault* y mi proyecto. Ahora necesito que instales los plugins esenciales, crees las *skills* clave y configures algunas cosas más. Guíame paso a paso, uno a la vez. Confirma cada paso antes de seguir.

---

## PASO 1: VERIFICAR EL ROUTER GLOBAL CLAUDE.md + PRUEBA DE RUTEO

Mi router global `~/.claude/CLAUDE.md` ya fue creado en el **prompt de Configuración Principal (Doc 2)** — el paso "Global Router". Aquí solo confirmamos que está en su sitio y corremos la prueba de ruteo en vivo antes de instalar *skills*.

Verifica el archivo:

```bash
head -25 ~/.claude/CLAUDE.md

# Third check, Windows-specific. This MUST print 0.
# Any other number means a backslash path is in the router, which breaks it silently.
grep -c '\\' ~/.claude/CLAUDE.md
```

Confirma que:
1. La primera sección es `## Default Workspace` (el router imperativo), NO `## Who I Am`.
2. La ruta del *vault* está resuelta (no queda ningún placeholder literal en el archivo).

Luego corre la **prueba de ruteo desde fuera del vault** — clave para detectar el modo de falla "es solo un perfil, no un router":

```bash
cd ~
claude
```

Cuando Claude Code arranque, pregunta: *"¿Qué archivos hay en el INBOX de mi vault?"* Si Claude lee el `00 HUB/00 INBOX/` de mi *vault* sin que yo le dé la ruta, el router está funcionando. Si dice "no sé dónde está tu vault", el router se generó como un documento de perfil, no como router — regresa al paso "Global Router" del prompt de Configuración Principal y vuelve a crear `~/.claude/CLAUDE.md` con el bloque `## Default Workspace` ARRIBA DEL TODO.

Confirma que ambas verificaciones pasan. Pasa al Paso 2.

---

## PASO 2: INSTALAR PLUGINS

Corre estos comandos para instalar los plugins esenciales:

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

Si `superpowers` o `playground` dicen que no conocen el marketplace, corre antes `claude plugin marketplace add anthropics/claude-plugins-official`. (`claude /install-plugin` y `claude plugins add` no existen — corregido el 23-sep-2026.)

Si ninguna funciona, dime qué error te dio y lo resolvemos.

**Después de instalar, explica brevemente qué hace cada plugin:**

- **Compound Engineering:** te da `/ce:plan` (crear un plan estructurado con investigación) y `/ce:work` (ejecutar un plan paso a paso). La idea central: "a menos que sea un cambio de una línea, siempre hay un plan primero".
- **Superpowers:** te da flujos de trabajo estructurados para depuración (`/systematic-debugging`), lluvia de ideas (`/brainstorm`), revisión de código (`/requesting-code-review`) y desarrollo guiado por pruebas (`/test-driven-development`).

Confirma que ambos están instalados. Pasa al Paso 2.5.

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
2. Ve a **Settings → Connectors → Explore**.
3. Instala estos cuatro connectors uno por uno, aceptando el consentimiento OAuth en cada uno:
   - **Gmail** (leer/enviar/buscar)
   - **Google Drive** (buscar/leer/crear archivos)
   - **Google Calendar** (listar eventos, crear eventos, responder invitaciones)
   - **Granola** (transcripciones de reuniones + resúmenes con IA)
4. En cada connector, el navegador abre una pantalla de consentimiento de Google. **Si la pestaña del navegador no se abre sola, copia la URL que Claude muestra y pégala en tu navegador manualmente** — este es el punto de fricción más común, no una falla.
5. Después de instalarlos, los connectors quedan disponibles en cualquier sesión de Claude Code como herramientas `mcp__claude_ai_<connector>__*` — no hace falta más configuración.

**Verificación:** en esta sesión de Claude Code, pregunta: *"Lista mis 3 mensajes de Gmail más recientes."* y *"Lista mis próximos eventos de calendario para hoy."* Si ambas devuelven datos reales, los connectors están conectados.

### Camino B — Microsoft 365 / Outlook

La integración de correo/calendario queda **diferida a la Fase 1** — todavía no hay un Connector de primera mano para Outlook y las opciones de MCP están en evaluación. **Sáltate por completo los Connectors de Google de arriba** (no tocan un buzón de Outlook). Si necesitas datos de Outlook durante la Fase 0, exporta/importa manualmente; conectaremos una integración apropiada en la Fase 1. *(Granola es independiente — si lo usas para tus reuniones, instala solo ese Connector.)*

### Camino C — Otro stack / desconocido

Sáltate la integración de correo para la Fase 0 y difiérela a la Fase 1. Dime qué usas (Fastmail, Zoho, Proton, etc.) y evaluamos opciones más adelante. Nada de esto bloquea el resto de la configuración.

Una vez verificado (Google) o saltado (Microsoft / otro) según tu camino, pasa al Paso 2.5b.

---

### PASO 2.5b: AVANZADO — gws CLI (OPCIONAL, DIFERIR A FASE 0.5 — solo stack Google)

> **Decide:** instala gws CLI solo si necesitas **editar Google Sheets programáticamente desde Claude Code** (escribir fórmulas, actualizar rangos por lotes, gestionar el esquema de una hoja). Los Connectors de arriba ya cubren la *lectura* de Sheets, además de todas las operaciones de Gmail / Drive / Calendar. Si tu proyecto no escribe en Sheets desde scripts de terminal, sáltate este paso por completo — siempre puedes volver después en la Fase 0.5.

Para los proyectos que sí lo necesitan, `gws` es la herramienta de línea de comandos que envuelve toda la superficie de la API de Google Workspace (escrituras a Sheets incluidas) en un solo binario. **En Windows** consigue el build `windows-amd64`, guárdalo como `~/bin/gws.exe` y agrega `export PATH="$HOME/bin:$PATH"` a `~/.bashrc` — las instrucciones de macOS (`chmod +x ~/bin/gws`, editar un perfil de zsh) no aplican. La instalación agrega ~1.5h (instalar gcloud + configurar el cliente OAuth + otorgar scopes).

Guíame por la instalación paso a paso:

1. Revisa si gcloud CLI está instalado: `gcloud --version`
   - Si no, ve a https://cloud.google.com/sdk/docs/install y guíame por la instalación
   - Después de instalar: `gcloud auth login` (abre el navegador)

2. Descarga el binario de gws desde https://github.com/googleworkspace/cli/releases
   - Escoge el binario para mi sistema operativo/arquitectura
   - Colócalo en `~/bin/gws` (crea `~/bin/` si hace falta)
   - `chmod +x ~/bin/gws`
   - Agrega `~/bin` a mi PATH si aún no está (revisa el perfil de mi shell)
   - Verifica: `~/bin/gws --version`

3. Configuración OAuth: `~/bin/gws auth setup` — crea un cliente OAuth y habilita las APIs de Google necesarias.

4. Autentica: `~/bin/gws auth login` — consentimiento OAuth en el navegador, otorga todos los scopes.

5. Prueba: `~/bin/gws drive files list --params '{"pageSize": 3}'` y `~/bin/gws calendar events list --params '{"calendarId": "primary", "maxResults": 3}'`.

6. Agrega `"Bash(~/bin/gws *)"` al arreglo `allow` en `~/.claude/settings.json` para que Claude Code no pregunte cada vez.

7. Agrega una sección "Google Workspace Tools" al CLAUDE.md del *vault* con estas reglas:
   - Herramienta principal: el CLI `gws` en `~/bin/gws`
   - Sintaxis: `gws <service> <resource> [sub-resource] <method> --params <JSON>`
   - Dos flags: `--params` = parámetros de URL/consulta, `--json` = cuerpo de la petición
   - Importante: el carácter `!` en los rangos de Sheets (por ejemplo, `Sheet1!A1:Z10`) se corrompe en bash. Cuando trabajes con rangos, usa siempre `subprocess.run()` de Python para llamar a gws — nunca bash directo.

Si algún paso falla, ayúdame a resolverlo antes de seguir.

Confirma que los Connectors funcionan (y opcionalmente gws si lo instalaste). Pasa al Paso 2.6.

---

## PASO 2.6: TRANSCRIPCIONES DE REUNIONES + SKILL /meeting-minutes

Mi herramienta de transcripción de reuniones es **[HERRAMIENTA]** *(el facilitador la llena antes de la sesión: `Granola` (por defecto) · `SpeakUp` · `Otter` · `Plaud` · `ninguna / transcripción pegada`)*. Instala la *skill* `/meeting-minutes` contra **esa** fuente — no asumas Granola.

**Según la herramienta:**
- **Granola** → en el Paso 2.5 ya instalé el **Connector de Granola** vía claude.ai. Verifícalo: pregunta *"Lista mis 3 reuniones de Granola más recientes."* Si devuelve reuniones reales, funciona; si no, reinstala el connector y **si la pestaña del navegador no se abrió durante el OAuth, copia la URL y pégala manualmente**. La *skill* lee vía las herramientas `mcp__claude_ai_Granola__*`.
- **SpeakUp / Otter / Plaud / otra** → si la herramienta publica un servidor MCP o connector, instálalo ahora (SpeakUp tiene uno — 2026-09-10) y verifica listando grabaciones recientes. Si no tiene, la entrada de la *skill* es **una transcripción que yo pego o exporto a un archivo**; no intentes conectar Granola.
- **Ninguna** → la *skill* acepta una transcripción pegada; sáltate cualquier connector.

**Prerrequisito:** la app de la herramienta está instalada y tengo al menos una grabación de prueba. Si no, hazlo primero (ver las Instrucciones de Configuración Pre-Sesión, Doc 1) y regresa.

Guíame por esto:

1. **Verifica la fuente de transcripciones** según la rama de arriba.

2. **Instala la *skill* `/meeting-minutes`** — crea `~/.claude/skills/meeting-minutes/SKILL.md` que:
   - Reciba un ID de reunión de [HERRAMIENTA] (o pregunte por la última), **o** una transcripción pegada / en archivo cuando no hay connector
   - Traiga la transcripción + el resumen con IA vía el MCP/connector de la herramienta cuando exista (Granola: `mcp__claude_ai_Granola__*`)
   - Genere una nota estructurada de Minuta de Reunión en `03 REFERENCE/<area>/`. Si `Templates/Meeting Minutes Template.md` todavía no existe, créala primero (asistentes, fecha, agenda, decisiones, ítems de acción con responsables, próximos pasos) — el Doc 02 solo entrega una plantilla de Brief de Proyecto
   - Extraiga Decisiones, Ítems de Acción y Próximas Acciones como wikilinks

3. **Verificación:** graba una reunión de prueba de 30 segundos en [HERRAMIENTA] (o pega cualquier transcripción corta) y luego corre `/meeting-minutes latest`. Claude debería traer/leer la transcripción, generar un archivo de minuta y mostrarme la ruta.

Confirma que la fuente de transcripciones + la *skill* `/meeting-minutes` funcionan. Pasa al Paso 2.7.

---

### PASO 2.6b: AVANZADO — Granola MCP vía CLI (OPCIONAL, DIFERIR A FASE 0.5)

> **Decide:** instala el MCP de Granola basado en CLI solo si quieres automatización del lado del *vault* que corra **fuera de una sesión de Claude Code** (por ejemplo, un cron que procese las reuniones nuevas cada mañana). El Connector de arriba ya cubre el uso dentro de la sesión — correr `/meeting-minutes` en vivo durante o después de una sesión. Sáltate esto por completo a menos que tengas una necesidad concreta de automatización.

Para los proyectos que sí lo necesitan, Granola expone una API REST que un envoltorio local puede llamar directamente. Si hace falta, guíame por esto:

1. Lee el token de autenticación desde la carpeta de datos de la app de Granola. **En Windows esa carpeta es `%APPDATA%\Granola\`
   (en Git Bash: `~/AppData/Roaming/Granola/`), NO la ruta de macOS `~/Library/Application Support/`.**
   Confirma primero los nombres reales de los archivos en disco (`ls ~/AppData/Roaming/Granola/`) — no asumas que la
   estructura de Mac se traslada igual. Busca el campo anidado `workos_tokens.access_token`.
2. Usa el caché de reuniones en esa misma carpeta para listar IDs/títulos/fechas (de nuevo: confirma el nombre real del archivo en vez de asumir `cache-v6.json`).
3. Construye un pequeño ayudante en Python en `~/bin/granola-fetch` que acepte `--meeting-id` o `--latest` e imprima la transcripción + el resumen con IA como JSON. Endpoints de la API: `https://api.granola.ai/v1/get-document-transcript` y `https://api.granola.ai/v1/get-document-panels`.
4. Conecta el ayudante al **Programador de Tareas de Windows** para procesamiento desatendido (launchd y cron son solo de macOS/Linux).

Confirma que el ayudante de CLI funciona (solo si decidiste instalarlo). Pasa al Paso 2.7.

---

## PASO 2.7: INSTALAR LAS SKILLS CENTRALES DE FASE E

Además de `/session-close` (Paso 4) y `/meeting-minutes` (Paso 2.6), otras cinco *skills* forman parte del set de instalación requerido de Fase E — salieron de fricción repetida en sesiones de Fase 0 donde los miembros tenían que inventar flujos desde cero en vez de usar una *skill* ya probada:

- **`/project-create`** — usada en el flujo de la demo ("siempre empieza con un plan"); crea Briefs de Proyecto / Programa vía preguntas y respuestas guiadas
- **`/inbox-clear`** — procesamiento diario del INBOX; clasifica cada nota, propone acciones, ejecuta tras la aprobación
- **`/retro`** — retrospectivas de sesión; rutea al protocolo correcto según el modo de la sesión
- **`/playground`** — *playgrounds* HTML interactivos para explorar conceptos visualmente
- **`/skill-create`** — construye *skills* nuevas a partir de una conversación guiada; se usa para la *skill* de revisión semanal de la Semana 1 y `/retro` la llama cuando propone codificar un flujo recurrente.

### 2.7a — Instalar `/project-create` (curl de una línea)

La *skill* `/project-create` viene en el repositorio público del starter-pack de AIAC. Instálala con un solo curl:

```bash
mkdir -p ~/.claude/skills/project-create/ && curl -fsSL https://raw.githubusercontent.com/wildbuffaloman/cc-starter-pack/main/project-create/SKILL.md -o ~/.claude/skills/project-create/SKILL.md
```

Verifica:
```bash
head -5 ~/.claude/skills/project-create/SKILL.md
```

Deberías ver el frontmatter YAML (`name: project-create`, `version: ...`, etc.).

### 2.7b — Instalar `/playground` (plugin oficial de Anthropic)

`/playground` es parte del marketplace oficial de plugins de Anthropic — instálalo como plugin, no como *skill* independiente:

```bash
claude plugin install playground@claude-plugins-official
```

Verifica corriendo `/playground` en esta sesión — Claude debería describir el flujo del constructor de playgrounds.

### 2.7c — Instalar `/inbox-clear` (pegado en línea)

El repositorio de la *skill* `/inbox-clear` es privado por ahora (será público en una cohorte futura). Por lo pronto, crea el archivo con este contenido listo para pegar. Crea `~/.claude/skills/inbox-clear/SKILL.md` con:

```markdown
---
name: inbox-clear
description: GTD-based inbox clearing — classify every note in 00 HUB/00 INBOX/, propose actions in a clearance manifest, execute after user approval.
user-invocable: true
argument-hint: "optional: single note path, or 'batch' to process all"
---

Clear `00 HUB/00 INBOX/` using a GTD-style classify-then-execute flow. Never delete or move silently — always propose first.

## Phase 1: Audit

For each note in `00 HUB/00 INBOX/`:

1. Read the note (full content if <500 chars, otherwise frontmatter + first/last sections).
2. Classify into one of:
   - **PROJECT** — actionable, multi-step → route to `01 PROJECTS/<Brief>/` or create a new project via `/project-create`
   - **REFERENCE** — durable knowledge → route to `03 REFERENCE/<area>/`
   - **READ_REVIEW** — needs deeper read before disposition → route to `03 REFERENCE/READ_REVIEW/`
   - **TASK** — single action → append to the Next Actions section of the relevant project brief, then archive the note. (If you have a task manager wired up, offer to add it there too — don't assume one.)
   - **DAILY_NOTE** — date-tagged daily content → route to `03 REFERENCE/DAILY NOTES/`
   - **ARCHIVE** — historical / completed → route to `04 ARCHIVES/`
   - **DELETE** — duplicate / accidental / no value → propose deletion
   - **KEEP_IN_INBOX** — needs human triage that AI can't make
3. For tasks: propose Eisenhower priority (Q1🔺 / Q2⏫ / Q3🔼 / Q4 none) based on urgency + leverage.

## Phase 2: Clearance Manifest

Write the manifest to `00 HUB/00 INBOX/_inbox-clear-manifest-YYYY-MM-DD.md`:

| Note | Classification | Proposed Action | Target Path | Priority |
|------|----------------|-----------------|-------------|----------|
| ... | PROJECT | Route to existing brief | 01 PROJECTS/Foo/Foo.md | — |

Present the manifest to the user. Wait for approval (or per-row overrides) before Phase 3.

## Phase 3: Execute

Only after user approves:
1. Move each note to its target.
2. Append TASK rows to the Next Actions section of the relevant project brief (and to a task manager only if the user has one set up).
3. Run `/project-create` for any new PROJECT rows.
4. Update the manifest with `✓` per executed row.
5. Surface anything that failed for re-decision.

## Rules

- Never bulk-move without approval.
- Tasks dedup against existing Apple Reminders before creating (search by title).
- Preserve original filename when moving — don't rename silently.
- If a note has wikilinks to others in INBOX, process the cluster together so cross-refs stay valid.
- Surface anything truly ambiguous as KEEP_IN_INBOX — better to leave it than mis-route.
```

Verifica:
```bash
head -5 ~/.claude/skills/inbox-clear/SKILL.md
```

Debería mostrar el frontmatter `name: inbox-clear`.

### 2.7d — Instalar `/retro` (pegado en línea)

El repositorio de la *skill* `/retro` es privado por ahora. Crea `~/.claude/skills/retro/SKILL.md` con esta versión simplificada:

```markdown
---
name: retro
description: Run a retrospective on the current session or project — surface what worked, what didn't, and what to change so the next session is better.
user-invocable: true
argument-hint: "optional: scope — session, project, weekly, monthly"
---

Run a retrospective and update CLAUDE.md / project briefs with lessons learned.

## When to Run

- After a milestone or significant session
- When something broke or pivoted unexpectedly
- At a regular cadence (weekly = recommended, monthly = strategic)
- When the user says "retro", "let's reflect", "what did we learn"

## Steps

### 1 — Scope

Determine the scope:
- **session** (default) — just this session
- **project** — entire project arc (read its brief, look at Log section)
- **weekly** — last 7 days across all projects
- **monthly** — last 30 days strategic view

If no scope arg, ask: "Retro on this session, the current project, or a longer review?"

### 2 — Surface the Material

Pull the relevant material:
- For session: current conversation
- For project: the brief's Log + last 5 entries in Next Actions + Continuation Prompts history
- For weekly/monthly: scan all project briefs touched in that window

### 3 — The Three Questions

Ask the user (or work through these yourself, then confirm):

1. **What went well?** (2-3 items — celebrate wins, identify what to keep doing)
2. **What went wrong / friction?** (2-3 items — be specific, name the moment)
3. **What to change?** (1-2 concrete actions — these become CLAUDE.md updates or new rules)

### 4 — Codify

For each "change" item:
- If it's a behavior rule → update `~/.claude/CLAUDE.md` or the relevant project CLAUDE.md
- If it's a recurring workflow → propose codifying as a skill via `/skill-create` (don't auto-create — ask first)
- If it's a one-off lesson → append a line to `05 AI/CLAUDE CODE/resources/lessons.md`

### 5 — Log

Append a Retro entry to the relevant Log section (project brief Log, or lessons.md for session-scope retros):

| Date | Type | Description |
|------|------|-------------|
| YYYY-MM-DD | Retro | <one-line summary of the 3 questions> |

## Rules

- Never auto-edit CLAUDE.md without user approval — present the proposed diff first
- Keep it short — 3 wins, 3 frictions, 1-2 changes is the target. Don't write essays
- If the user says "no retro needed", respect that — don't push
- Lessons learned in retro should be **specific** ("when X happens, do Y"), not vague ("be more careful")
```

Verifica:
```bash
head -5 ~/.claude/skills/retro/SKILL.md
```

Debería mostrar el frontmatter `name: retro`.

### 2.7e — Instalar `/skill-create` (curl de una línea)

`/skill-create` construye *skills* nuevas a partir de una conversación guiada — la vas a usar para tu *skill* de revisión semanal de la Semana 1, y `/retro` la llama cuando propone codificar un flujo recurrente. Instálala desde el starter-pack público de AIAC con un solo curl:

```bash
mkdir -p ~/.claude/skills/skill-create/ && curl -fsSL https://raw.githubusercontent.com/wildbuffaloman/cc-starter-pack/main/skill-create/SKILL.md -o ~/.claude/skills/skill-create/SKILL.md
```

Verifica:
```bash
head -5 ~/.claude/skills/skill-create/SKILL.md
```

Deberías ver `name: skill-create` en el frontmatter.

### 2.7f — Verificación Final

Corre todas las *skills* en una sola revisión:

```bash
for skill in meeting-minutes project-create inbox-clear retro skill-create; do
  if [ -f ~/.claude/skills/$skill/SKILL.md ]; then
    echo "✓ $skill"
  else
    echo "✗ $skill MISSING"
  fi
done
```

Para `/playground` (que es un plugin, no una *skill* independiente):
```bash
ls ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/playground 2>/dev/null && echo "✓ playground plugin" || echo "✗ playground plugin MISSING"
```

Si falta algo, arréglalo antes de pasar al Paso 3.

---

## PASO 3: CARPETA DE LECCIONES

Crea un archivo de lecciones en mi *vault* en `05 AI/CLAUDE CODE/resources/lessons.md` para capturar las lecciones aprendidas.

Siémbralo con esta regla de Windows como primera entrada, para que toda sesión futura la vuelva a leer:

> **Usa siempre barras normales `/` en las rutas en esta máquina.** En Git Bash una barra invertida sin comillas se
> elimina en silencio y el comando falla sin error visible — y el síntoma imita un
> bug no relacionado. Obtén las rutas de Windows con `pwd -W`, nunca con `pwd` a secas.

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

## PASO 4: SKILL SESSION-CLOSE

Crea el archivo `~/.claude/skills/session-close/SKILL.md` con este contenido:

```markdown
---
name: session-close
description: Close the current session — update the project brief, log the work done, and leave a Continuation Prompt for the next session.
user-invocable: true
argument-hint: "optional: project name"
---

Close the current session by updating all relevant artifacts.

## When to Run

Run when:
- The user says "close session", "wrap up", "done for today", "save the state", or similar
- Context is running low (~50% used)
- An important task was completed
- The session is ending for any reason

## Step 1 — Identify the Project Brief

Every work session corresponds to a project. Find the matching brief:

1. Look in `01 PROJECTS/` (in the Obsidian vault) for a .md file that matches this session's work.
2. If no brief exists, create a new one in `00 HUB/00 INBOX/` using the Project Brief Template.
3. If the session was purely exploratory with no specific project, still create a minimal brief.

## Step 2 — Update the Project Brief

### Continuation Prompt (THE MOST IMPORTANT PART)

At the top of the `## Next Actions` section, add or REPLACE a `### Continuation Prompt` block. Only the most recent one is kept — it's overwritten each session.

Format:

### Continuation Prompt
> **Date:** YYYY-MM-DD
> **Context:** <1-2 sentences — which project, what we were doing>
>
> **Resume from:** <specific step, file, or location to continue from>
> **Key decisions:** <decisions made that affect the next steps>
> **Blockers/questions:** <anything unresolved>
> **Files touched:** <important files modified this session>

This block is designed to be copied and pasted into a new Claude Code session to resume the work without friction.

### Next Actions

Update the task list:
- Mark completed tasks as done
- Add new tasks discovered during the session

### Log

Add dated entries for the work performed:

| Date | Type | Description |
|------|------|-------------|
| YYYY-MM-DD | Task | Summary of the work |

Log rules:
- One item per row
- Label as "Task" or "Milestone"

### Waiting For

Only items that depend on OTHER people. Never put your own tasks here.

## Step 3 — Code Verification (only if code was written)

If the session involved writing or modifying code:

### 3a. Run and Verify
- Run the scripts that were created/modified
- Verify the output is correct
- If there are tests, run them

### 3b. Quality Review
Review the code for:
- **Security:** SQL injection? Hardcoded credentials?
- **Common errors:** Division by zero? Unclosed connections?
- **Readability:** Clear variable names? Comments where needed?

If you find problems, fix them (with the user's confirmation).

### 3c. Commit (if applicable)
If the work is in a git repo:
- Ask: "Do you want to commit the changes?"
- If yes, commit with a descriptive message
- Never push without explicit confirmation

## Step 4 — Lessons Learned

If the session produced reusable learnings:
- Add a line to `05 AI/CLAUDE CODE/resources/lessons.md` (in the vault)

## Step 5 — Report to the User

When finished, show:
- What was updated (and where)
- A summary of the Continuation Prompt
- Recommended next steps

## Step 6 — Retrospective Evaluation

Evaluate whether a quick retro is worthwhile. Indicators (1 point each):

1. **Milestone completed** — a milestone was reached
2. **Failure or pivot** — something broke or the plan changed
3. **New pattern** — a reusable workflow emerged
4. **Rule gap** — a hole in CLAUDE.md
5. **Repeated friction** — permission issues, repeated clarifications

Decision:
- **0-1 points:** No retro.
- **2-3 points:** Suggest a retro.
- **4+ points:** Strongly recommend one.

If the user agrees: **invoke the `/retro` skill** — it runs the retrospective (what went well / what went wrong / what to change) and updates CLAUDE.md / the briefs with the learnings. **Don't run the retro inline here** — `/retro` (installed in Step 2.7d) owns that flow; running it inline would duplicate the logic in two places.

## Rules

- The Continuation Prompt is MANDATORY on every close. No exceptions.
- Never invent data.
- If multiple projects were touched, update all their briefs.
- The Log is historical — only append, never modify previous entries.
- Respond in Spanish.
```

Después de crearlo, verifica que el archivo existe leyéndolo. Luego pasa al Paso 5.

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

## Windows notes (the four things you'll forget by next week)

| Thing | Remember |
|---|---|
| Which window | **Git Bash** for everything in this kit. PowerShell only for installing Claude Code. |
| Paths | Forward slashes `/` always. `pwd -W` gives the `C:/...` form. |
| Paste | Right-click, not Ctrl+V. |
| Something's broken | `claude doctor` — it checks the install and reports what's wrong. |

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
| `Shift+Tab` (x2) | Enter/exit Plan Mode |
| `/project-create` | Create a Project/Program brief via guided Q&A (Phase E skill) |
| `/inbox-clear` | Classify and route 00 HUB/00 INBOX notes (Phase E skill) |
| `/meeting-minutes` | Turn a Granola recording into a structured note (Phase E skill) |
| `/retro` | Run a retrospective on a session, project, or week (Phase E skill) |
| `/playground` | Build an interactive HTML playground (Phase E plugin) |

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
3. Revisa que `~/.claude/settings.json` tenga los permisos que configuramos antes.
4. Revisa que existan las 6 *skills* independientes en `~/.claude/skills/<skill>/SKILL.md`: `meeting-minutes`, `project-create`, `inbox-clear`, `retro`, `skill-create` (el bucle del Paso 2.7f), más `session-close` (creada después, en el Paso 4).
5. Revisa que el plugin `/playground` esté instalado en `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/playground/`.
6. Verifica que los Connectors de claude.ai respondan — pregunta: "Lista mis 3 mensajes de Gmail más recientes" y "Lista mis próximos eventos de calendario para hoy". (Sáltate esta revisión si estás en Microsoft 365 / otro y difeririste la integración de correo a la Fase 1.)
7. **Averigua cuál comando de Python existe en esta máquina antes de usar uno.** En Windows el
   comando suele ser `python` o `py` — **`python3` a secas normalmente NO existe, y escribirlo
   abre la Microsoft Store**, lo que parece un cuelgue. Corre esto primero:

   ```bash
   for c in python py python3; do command -v $c >/dev/null 2>&1 && echo "FOUND: $c"; done
   ```

   - **Si encuentra alguno:** crea un script sencillo en `05 AI/CLAUDE CODE/workspace/hello.py` que
     imprima un saludo personalizado con las rutas del *vault* y del repositorio, córrelo con el comando que
     realmente existe y muéstrame la salida. Agrega ese comando real a mi arreglo `permissions.allow`
     (por ejemplo, `Bash(python *)`), no la forma `python3` de macOS.
   - **Si no encuentra ninguno: eso NO es un bloqueo, y NO instalamos Python ahora.** Nada más en
     la Fase 0 lo necesita. Anótalo como ítem de la Semana 1 y pasa a la siguiente revisión. No dejes que esto detenga
     la sesión — es el último paso de verificación, no un prerrequisito.

8. Valida que el archivo de settings no se haya corrompido con las fusiones del Doc 02:

   ```bash
   jq . ~/.claude/settings.json > /dev/null && echo "settings.json is valid JSON"
   ```

9. Corre `claude doctor` y muéstrame la salida.

Si todo funciona, pasa al Paso 8.

---

## PASO 8: CONFIGURACIÓN COMPLETA

Dame un resumen final de todo lo de esta sesión:

**Qué se configuró:**
1. `~/.claude/CLAUDE.md` — puntero global a mi *vault* (Claude siempre sabe dónde están mis notas)
2. Plugin Compound Engineering — flujo Plan -> Construir
3. Plugin Superpowers — depuración, lluvia de ideas, revisión de código
4. Connectors de claude.ai — Gmail / Drive / Calendar / Granola (ruta de integración por defecto para Google Workspace; diferida a la Fase 1 para Microsoft 365 / otro; gws CLI diferido a la Fase 0.5 si hace falta)
5. *Skills* centrales de Fase E (6) — `/session-close`, `/meeting-minutes`, `/project-create`, `/inbox-clear`, `/retro`, `/playground`
6. Archivo de lecciones — `05 AI/CLAUDE CODE/resources/lessons.md`
7. Modo Plan — aprendiste a planificar antes de construir
8. Hoja de Referencia — referencia rápida en `00 HUB/00 INBOX/`

**Los tres hábitos más importantes:**
1. **Siempre `/session-close` antes de terminar** — esto es lo que te hace más inteligente con el tiempo
2. **Planifica antes de construir** — Shift+Tab dos veces, o `/ce:plan` para tareas grandes
3. **Corrige a Claude y deja que actualice CLAUDE.md** — el bucle de auto-mejora

Termina con: "Tu configuración de Claude Code está completa. Tienes la misma base que los usuarios más productivos de Claude Code. La clave ahora es usarla a diario — aunque sean 10 minutos. Cada sesión hace que la siguiente sea mejor."
