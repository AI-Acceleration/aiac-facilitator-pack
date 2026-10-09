---
title: "Brief de Próximos Pasos (Participante) — Kit de Co-Facilitación Fase 0 AIAC (ES)"
created: 2026-07-14
category: reference
status: draft
tags: [aiac, phase0, co-facilitator, next-steps, english]
lang: es
translated_from: "04 — Next Steps Brief (Participant).md"
---

*Se le entrega al participante al cierre de la sesión (Bloque 5) como su hoja de ruta de tareas.*

# Brief de Próximos Pasos — Dominio de Claude Code

> **Qué es esto:** Tu hoja de ruta desde la configuración hasta el uso diario productivo. Organizada en orden de prioridad — haz primero la Semana 1, después expande.
> Cada sección tiene prompts exactos que puedes pegar. No hay que pensar — solo copiar, pegar y arrancar.

---

## PARTE 0: INSTALA LOS PLUGINS ESENCIALES (Hazlo Primero)

> **Este brief se maneja con prompts.** Donde Claude pueda ejecutar un comando por ti, recibes un **prompt listo para pegar** en vez de una lista de comandos que tengas que escribir tú — lo pegas en Claude Code, Claude hace el trabajo y tú confirmas. Los comandos crudos quedan como respaldo. (El mismo principio recorre el resto de este brief: cuando veas un bloque de prompt, pégalo; cuando veas un comando de terminal, ese es o el respaldo o un paso que Claude realmente no puede hacer por ti — como hacer clic en la configuración de una aplicación o un OAuth en el navegador.)

**Pega esto en Claude Code:**

```
Install these plugins for me, one by one, then run `claude plugins list` to confirm they
all landed. If one fails, tell me which one and the error, and we'll fix it before moving
on:

- explanatory-output-style  (Claude explains its reasoning while it works)
- commit-commands           (smart git commits via /commit)
- skill-creator             (create your own custom commands)
- claude-md-management      (keep your CLAUDE.md healthy)
- context7                  (up-to-date docs for any library)
- code-review               (code quality review)
- firecrawl                 (web research, scraping, reading documentation)
- playground                (interactive HTML visualizations)
```

Claude instala cada uno (con `claude plugin install <name>@claude-plugins-official`) y reporta el `claude plugin list` final.

<details><summary><b>Respaldo — ejecútalos tú mismo en una terminal</b></summary>

Abre tu terminal normal (no dentro de Claude Code) y ejecuta:

```bash
claude plugin marketplace add anthropics/claude-plugins-official   # only if not already configured
claude plugin install explanatory-output-style@claude-plugins-official
claude plugin install commit-commands@claude-plugins-official
claude plugin install skill-creator@claude-plugins-official
claude plugin install claude-md-management@claude-plugins-official
claude plugin install context7@claude-plugins-official
claude plugin install code-review@claude-plugins-official
claude plugin install firecrawl@claude-plugins-official
claude plugin install playground@claude-plugins-official
```

`claude /install-plugin` y `claude plugins add` no existen — un plugin siempre es `<plugin>@<marketplace>` (corregido el 23-sep-2026).
</details>

**Ya deberías tener, de más temprano en la sesión de hoy:** Compound Engineering, Superpowers (instalados durante tu paso de *Skills* y Configuración, Doc 3).

> **¿Estás en Claude Pro?** Vigila tus límites de uso — espacia las sesiones pesadas a lo largo del día en vez de quemarlas una detrás de otra. En Max puedes ignorar esto.

---

## PARTE 0.7: CONCEPTOS Y STACK INSTALADO — LEE ESTO PRIMERO

> **Por qué existe esta sección:** Durante tu sesión de Fase 0 avanzamos rápido por mucha plomería. Esta es la página de "teoría + inventario" — la referencia a la que vuelves cuando quieres entender *por qué* algo está conectado como está, o *qué exactamente quedó instalado en tu computadora*. Léela una vez completa antes de que empiece la Semana 1. Después revísala por encima cada semana durante el primer mes.

### Los 4 Conceptos Centrales

Solo necesitas entender 4 conceptos para ser productivo con Claude Code. Todo lo demás se desprende de ellos.

#### 1. CLAUDE.md — El Cerebro del Sistema

No hay UN solo `CLAUDE.md`. Hay una **cadena** de ellos que Claude lee automáticamente al iniciar la sesión:

| Ubicación | Propósito | Cuándo lo lee Claude |
|----------|---------|---------------------|
| `~/.claude/CLAUDE.md` | **Router global + tu perfil.** Le dice a Claude dónde está tu *vault*, quién eres y cuáles son tus valores por defecto. | En cada sesión, sin importar el directorio de inicio |
| `[vault]/CLAUDE.md` | **Reglas del *vault*.** Cómo manejar notas, estructura PARA, seguridad, idioma. | En cada sesión iniciada dentro del *vault* |
| `[repo]/CLAUDE.md` | **Reglas del proyecto.** Esquema, principio del dominio, fuentes de datos, stack, reglas de validación. | En cada sesión iniciada dentro de ese repositorio |

**Modelo mental clave:** CLAUDE.md es la manera en que el sistema **mejora con el tiempo**. Cada vez que corrijas a Claude, agrega la regla al CLAUDE.md que corresponda. La siguiente sesión, la corrección se queda. Después de un mes, Claude realmente trabaja mejor para TI porque las reglas se acumulan.

**Regla de ubicación por especificidad:** Agrega una corrección al CLAUDE.md MÁS ESPECÍFICO que aplique. Si la regla es específica del proyecto, va en el CLAUDE.md del repositorio. Si es sobre cómo tomas notas en general, va en el CLAUDE.md del *vault*. Si es sobre tus valores por defecto en TODOS los proyectos (por ejemplo, "usa siempre español"), va en `~/.claude/CLAUDE.md`.

#### 2. Ventana de Contexto — Tu Memoria de Trabajo

La ventana de contexto de Claude es limitada (~200K tokens). A medida que trabajas en una sesión, se va llenando con el historial de la conversación, los archivos que Claude lee, las salidas de herramientas, etc. Cuando se llena más allá de cierto punto, **la calidad se degrada** — a esto se le llama **pudrición de contexto** (*context rot*).

**Los umbrales que importan:**
- **Compactar IDEALMENTE antes del 50%** — mejor calidad, cero degradación, traspaso limpio del estado. Esta es la meta.
- **Compactar SIN FALTA antes del 70%** — pasado el 70%, la calidad de la salida se cae por un barranco. Llegar a este umbral a mitad de una tarea sale caro, porque un compactado forzado y reactivo es mucho más sucio que uno proactivo.
- **Después del 50% empieza a aparecer la pudrición de contexto** — no es catastrófico, pero Claude empieza a olvidar contexto anterior, a hacer referencias inconsistentes y a confundir detalles. La calidad se degrada gradualmente desde el 50% → muro duro cerca del 70%.

**Las opciones de compactado al llegar al umbral:**
- Ejecuta `/session-close` y luego `/clear` para arrancar en limpio (lo más limpio — preserva completamente el estado en el Continuation Prompt del brief del proyecto, y luego reinicia).
- O ejecuta `/compact` para resumir en sitio y seguir en la misma sesión a mitad de tarea (más rápido, pero con pérdida — bota detalle, así que prefiere la opción de arriba en un punto de corte natural).

**Cómo ver tu uso:** Tu % de contexto aparece como una barra en vivo en la línea de estado al fondo de la terminal — configurada durante tu sesión del Prompt de Configuración Principal (Doc 2), el monitor de contexto de cuatro capas. La barra se pone **amarilla ⚠ en 50%** (con un sonido de una sola vez) y **roja 🚨 en 75%**, y la auto-compactación está **frenada en seco en 75%** para que tengas oportunidad de ejecutar `/session-close` (que preserva planes y tareas en el brief de tu proyecto) antes de que se comprima el contexto. Si la barra no se ve, escribe `/context` para ver el estado actual, o pídele a Claude que vuelva a correr la configuración de la línea de estado + el *hook* del Doc 2.

**Por qué existe esto:** Los LLM tienen un límite duro de cuánto texto pueden "pensar" a la vez. A diferencia de la memoria de corto plazo humana, no se degrada de forma pareja hasta el final — empieza gradualmente (~50%) y después choca contra un muro (~70%). La compactación proactiva le gana a chocar contra el tope de forma reactiva, siempre.

#### 3. *Skills* — Procedimientos Reutilizables

Un "*skill*" es un prompt estructurado + flujo de trabajo guardado en `~/.claude/skills/{name}/SKILL.md` que Claude puede invocar con `/{name}`. Ya tienes `/session-close` instalado de más temprano en la sesión de hoy (Doc 3).

**Cómo invocar un *skill*:** Escribe `/` en Claude Code y escoge del autocompletado, O escribe el nombre del *skill* explícitamente (por ejemplo, `/session-close`).

**Cuándo crear un *skill* nuevo:** Si te descubres dándole a Claude las mismas instrucciones 3 veces o más, eso merece un *skill*. Ejecuta `/skill-create` — Claude te guía interactivamente para definirlo.

**Por qué importan los *skills*:** Convierten patrones improvisados en infraestructura duradera. Un *skill* que escribes en la Semana 2 sigue funcionando en el Mes 6 sin que tengas que acordarte de los detalles.

#### 3.5. Flujo Multi-Sesión — El *Vault* y el Repositorio Son Dos Lugares Distintos

Muchas veces vas a tener **dos sesiones de Claude Code abiertas a la vez** — una en tu *vault* (notas, planificación, briefs) y otra en el repositorio de tu proyecto en `~/dev/[your-repo-name]` (código, datos, scripts). Esto es normal, no es un caso raro — así está diseñado el router + la cadena de CLAUDE.md para funcionar.

**Por qué importa la separación:**

1. **Los *skills* solo se cargan en sesiones nuevas.** Cuando se instala un *skill* (como `/session-close` más temprano hoy), no se aplica retroactivamente a la sesión que ya está corriendo. Aparece como "instalado" pero no está "activo" hasta que abres una ventana nueva de Claude Code. Esta noche, por eso mismo vas a usar el Prompt de Cierre Manual (ver APÉNDICE) en vez de `/session-close` — desde tu próxima sesión en adelante, `/session-close` funciona normal.
2. **Cada proyecto tiene su propio CLAUDE.md + su propio estado.** Correr el análisis de tu caso dentro de una sesión de planificación del *vault* mezcla dos bitácoras distintas. Mantén el trabajo del *vault* y el del repositorio en ventanas separadas.
3. **El router te resuelve dentro del proyecto correcto.** Desde cualquier directorio, escribir "vamos a trabajar en mi [nombre del caso]" abre el proyecto de tu caso en una sesión nueva con su Continuation Prompt cargado — sin `cd`, sin preguntas aclaratorias.

**Patrón del día a día:** cuando cambies de proyecto, abre una terminal nueva → `claude` → di "vamos a trabajar en mi [X]". No necesitas cerrar la anterior si vas a volver a ella.

#### 4. MCPs — Conectores a Sistemas Externos

MCP = "Model Context Protocol". Es la forma en que Claude Code habla con sistemas externos (Google Workspace, Granola, GitHub, bases de datos, etc.) más allá de tu sistema de archivos.

**En la sesión de hoy obtuviste:**
- **Conectores de Google Workspace de Claude.ai** (activados durante tu sesión de *Skills* y Configuración, Doc 3) — le permiten a Claude leer tu Drive / Docs / Sheets / borradores de Gmail / Calendario desde la interfaz de chat de Claude.ai
- **MCP de Granola** (activado durante tu sesión de *Skills* y Configuración, Doc 3) — le permite a Claude traer las transcripciones de tus reuniones + los resúmenes de IA

**Cómo agregar más después:** Edita `~/.claude/settings.json` y agrega entradas bajo `mcpServers`. Algunos comunes que vale la pena agregar cuando los necesites: Playwright (automatización de navegador), Supabase/Postgres (consultas a bases de datos), Slack (mensajería de equipo), SQL Server (base de datos corporativa).

**Cuándo agregar un MCP vs. un CLI:** Los MCPs son "conectores estructurados" — Claude recibe herramientas tipadas con entradas/salidas definidas. Los CLIs son "comandos crudos" — Claude escribe comandos de shell. Los MCPs son más limpios para operaciones frecuentes; los CLIs son mejores para tareas puntuales o a nivel de sistema operativo. Para operaciones de Google Workspace por CLI desde Claude Code (no desde la interfaz de chat), instala el CLI `gws` más adelante, cuando un flujo específico lo necesite (ver PARTE 0.9).

### Buenas Prácticas — El Ciclo Central

Estos son los 7 hábitos que separan a los usuarios productivos de Claude Code del resto. Interiorízalos todos para la Semana 4.

1. **Siempre `/session-close` antes de terminar.** Sin excepciones. Este es el hábito que hace que el sistema se acumule.
2. **Planifica antes de construir.** Cualquier tarea que toque 2 o más archivos: `Shift+Tab` dos veces para el Modo Plan. Proyectos grandes o nuevos: `/ce:plan`.
3. **Corrige a Claude en voz alta, y después persiste la corrección.** Cuando Claude haga algo mal, di "eso no está bien porque X. Ahora actualiza el CLAUDE.md para que no vuelva a pasar." ESTE es el ciclo de auto-mejora.
4. **Monitorea la ventana de contexto proactivamente.** Cerca del 50%, compacta o cierra. Nunca dejes que llegue al tope duro a mitad de tarea.
5. **Captura lecciones.** Cualquier comportamiento sorpresivo, truco o rodeo → agrega una línea a una bitácora de lecciones al final de la sesión.
6. **Abre Claude Code todos los días, aunque sean 10 min.** El hábito importa más que el resultado en la Semana 1.
7. **Confía en la cadena de CLAUDE.md.** Si Claude está confundido, normalmente es porque falta un CLAUDE.md o está mal — no porque Claude esté roto. Arregla el CLAUDE.md.

### Qué Quedó Instalado en tu Computadora Hoy

Inventario completo, por si necesitas auditar, replicar o resolver problemas después.

**Archivos globales:**

| Ruta | Qué es | Edítalo cuando... |
|------|-----------|--------------|
| `~/.claude/CLAUDE.md` | Router global + tu perfil | Se mueva tu *vault*, cambie tu rol, o quieras agregar valores por defecto globales |
| `~/.claude/settings.json` | Permisos (comandos pre-aprobados) + *hooks* (sonido de fin de sesión, etc.) | Quieras que Claude pida permiso con menos frecuencia, o disparar eventos en el ciclo de vida de la sesión |
| `~/.claude/skills/session-close/SKILL.md` | El *skill* `/session-close` | Quieras cambiar cómo se cierran las sesiones (raro) |

**Archivos creados en el *vault*:**

| Ruta | Qué es |
|------|-----------|
| `[vault]/CLAUDE.md` | Reglas a nivel de *vault* (PARA, idioma, seguridad) |
| `[vault]/Templates/Project Brief Template.md` | Plantilla reutilizable para proyectos nuevos |
| `[vault]/01 PROJECTS/[project name]/[project name].md` | El brief del proyecto de tu caso |
| `[vault]/01 PROJECTS/AI Acceleration Club — [your name].md` | Lleva el registro de tu progreso en el programa |
| Una bitácora de lecciones en tu *vault* | Donde anotas lecciones de una línea después de cada sesión |
| `[vault]/00 HUB/00 INBOX/AIAC Cheat Sheet.md` | Tarjeta de referencia rápida |

**Archivos del repositorio:**

| Ruta | Qué es |
|------|-----------|
| `~/dev/[your-repo-name]/CLAUDE.md` | Reglas a nivel de proyecto (esquema, principios, fuentes de datos, stack) + puntero al brief del *vault* |
| `~/dev/[your-repo-name]/README.md` | Introducción al proyecto para humanos |
| `~/dev/[your-repo-name]/.gitignore` | Evita subir datos/secretos a GitHub |
| `~/dev/[your-repo-name]/data/{raw,working,processed}/` | Zonas de datos (raw = ignorada por git, processed = versionada) |

**Plugins instalados hoy (Doc 3 + Parte 0 de arriba):**

| Plugin | Comandos principales | Qué hace |
|--------|--------------|--------------|
| Compound Engineering | `/ce:plan`, `/ce:work`, `/ce:brainstorm`, `/ce:review` | Flujo planificar → investigar → construir |
| Superpowers | `/brainstorm`, `/systematic-debugging`, `/test-driven-development`, `/verification-before-completion` | Pensamiento estructurado + depuración |
| Explanatory Output Style | (automático) | Claude explica su razonamiento mientras trabaja |
| Commit Commands | `/commit`, `/commit-push-pr` | Commits de git inteligentes con mensajes automáticos |
| Skill Creator | `/skill-create` | Creación interactiva de *skills* |
| Claude MD Management | `/claude-md-improver` | Audita y mejora los archivos CLAUDE.md |
| Context7 | (automático) | Documentación actualizada de librerías cuando las mencionas |
| Code Review | `/code-review` | Revisión de errores / seguridad / calidad |
| Firecrawl | (reemplaza la búsqueda web) | Investigación web + scraping |
| Playground | `/playground` | Visualizaciones HTML interactivas |

**Conectores MCP:**

| Conector | Qué expone |
|-----------|-----------------|
| Google Workspace de Claude.ai | Drive, Docs, Sheets (lectura + escritura), Gmail (solo borradores), Calendario (CRUD completo) — desde el chat de Claude.ai |
| Granola | Transcripciones de reuniones + resúmenes de IA |

> **Si un conector de claude.ai (Gmail / Drive / Calendario / Granola) no terminó de autorizarse durante la sesión:**
>
> Vuelve a claude.ai → Settings → Connectors, busca el conector y completa el flujo de OAuth. Verifica que funcionó con un prompt de prueba rápido en Claude Code, por ejemplo *"Lista mis 3 correos más recientes."* Si aun así no autoriza, avísale a tu facilitador con el error exacto que ves en la pantalla de OAuth.

***Hooks*:**

| Evento | *Hook* | Qué pasa |
|-------|------|--------------|
| `Stop` (fin de sesión) | Pitido | Notificación audible cuando Claude termina una tarea |

### Cómo Resolver Problemas Cuando Algo se Siente Raro

Árbol de decisión rápido:

- **Claude no sabe nada de mi proyecto** → puede que el router `~/.claude/CLAUDE.md` esté roto. Vuelve a correr la prueba de ventana nueva del Bloque 7 de la Fase 0.
- **Claude repite el mismo error una y otra vez** → la corrección no quedó persistida. Abre el CLAUDE.md correspondiente y verifica que la regla esté ahí.
- **La sesión se siente lenta o Claude está olvidando cosas** → la ventana de contexto está llena. Ejecuta `/session-close` y luego `/clear`.
- **No se encuentra un comando de un plugin** → puede que el plugin no esté instalado. Ejecuta `claude plugins list` para ver qué está cargado.
- **No se encuentra el comando de un *skill*** → puede que el *skill* esté en un plugin y no global. Revisa `~/.claude/skills/` vs `~/.claude/plugins/*/skills/`.
- **Algo da error en la terminal** → copia el error, pégalo de vuelta en Claude y pregunta "qué es este error?" (este es el respaldo universal).

---

## PARTE 0.8: OPCIONAL — SUBE DE NIVEL TU OBSIDIAN

> **Opcional, no obligatorio.** La Fase 0 ya dejó puestas las cuatro configuraciones de Obsidian que sostienen todo
> (notas nuevas → `00 HUB/00 INBOX`, wikilinks, mostrar todos los tipos de archivo, actualizar enlaces automáticamente). Todo
> lo de abajo es *amplificación* — plugins de la comunidad y configuraciones más profundas que hacen tu *vault*
> más potente. Agrégalos cuando quieras la capacidad, no porque toque. Cada entrada
> dice **para qué sirve** y **cómo configurarlo**.

### Plugins de la comunidad que vale la pena instalar

La ruta de instalación es la misma para todos: **Settings → Community plugins → Turn on
community plugins → Browse → busca el nombre → Install → Enable (interruptor en ON)**. Instala uno,
pruébalo, y después vuelve por el siguiente — no instales de golpe cinco plugins que no vas a tocar.

| Plugin | Para qué es útil | Cómo configurarlo |
|--------|----------------------|------------------|
| **Dataview** | Consultas en vivo sobre el frontmatter de tus notas — el motor detrás de cualquier tablero compilado o vista de "muéstrame todos los proyectos activos". El plugin de mayor palanca para un *vault* PARA. | Instalar + habilitar. Después, en su configuración pon en **ON**: "Enable inline queries", "Enable JavaScript queries", "Enable inline JavaScript queries". Pruébalo en una nota: un bloque cercado ```` ```dataview LIST FROM "" LIMIT 5 ``` ```` debería mostrar una lista de archivos. |
| **Tasks** | Gestión real de tareas encima de las casillas `- [ ]` — fechas de entrega, prioridades, recurrencia y consultas como "todo lo que vence esta semana en todo el *vault*". | Instalar + habilitar. En su configuración pon en ON "Set done date on every completed task". Prueba: escribe `- [ ] Test 📅 2026-12-31` — le sale una píldora de fecha. |
| **Templater** | Sustitución de marcadores en plantillas (`{{title}}`, `{{date}}`, fragmentos dinámicos) — convierte tu Project Brief Template en un andamio que se llena solo. | Instalar + habilitar. Apunta su "Template folder location" a `Templates/`. |
| **Calendar** | Un mini-calendario en la barra lateral atado a las notas diarias — haces clic en un día y abres/creas la nota de ese día. Se lleva bien con Periodic Notes. | Instalar + habilitar. No necesita configuración para empezar. |
| **Periodic Notes** | Creación de notas diarias / semanales / mensuales con plantillas — la columna vertebral de un hábito de diario o bitácora. | Instalar + habilitar. Activa "Daily Notes" y define su plantilla + carpeta. |

### Configuraciones más profundas (opcional)

Un par de configuraciones más allá de las cuatro de la Fase 0, para cuando las quieras:

- **Adjuntos en una sola carpeta.** Settings → Files and links → **Default location for new
  attachments** → "In the folder specified below" → por ejemplo `assets`. Mantiene las imágenes pegadas
  y los PDF fuera de tus carpetas de notas.
- **Formato de enlace más corto.** Settings → Files and links → **New link format** → "Shortest
  path when possible". Enlaces `[[Note]]` más limpios en vez de rutas completas.

### Ruta de usuario avanzado: escribir los archivos de configuración directamente

Todo lo de arriba también se puede configurar editando los archivos JSON de la carpeta oculta `.obsidian/`
dentro de tu *vault* (más rápido que hacer clic, y automatizable). Hazlo solo si te sientes
cómodo — y **reinicia Obsidian después**. Pídele a Claude Code:

```
Open the .obsidian/ folder in my vault and show me app.json. I want to set:
attachments → "assets", new link format → shortest, and confirm new notes go to 00 HUB/00 INBOX.
Then walk me through enabling Dataview inline queries via its data.json.
```

---

## PARTE 0.9: OPCIONAL — CLI gws PARA UNA INTEGRACIÓN MÁS PROFUNDA CON GOOGLE WORKSPACE

> **Enriquecimiento opcional, solo para el stack de Google.** La sesión de hoy conectó los **Connectors de claude.ai** (Gmail / Drive / Calendario / Granola) — eso cubre ~90% de lo que vas a necesitar y es el valor por defecto correcto. Agrega el **CLI gws** más adelante, solo cuando se te queden cortos los Connectors y necesites **manejar Google Workspace de forma programática desde scripts** — sobre todo **escribir en Google Sheets** (fórmulas, actualizaciones de rangos por lote, esquema), que los Connectors no hacen. Sáltatelo por completo si estás en Microsoft 365 / Outlook o si no escribes scripts contra Sheets.

**Qué desbloquea más allá de los Connectors:** toda la superficie de la API de Google Workspace en un solo binario — *escrituras* en Sheets, Apps Script, Drive/Calendario avanzados — invocable desde Python/bash para que Claude pueda construir automatizaciones reales (un reporte nocturno que escribe en una hoja, una tubería manejada por un formulario, etc.).

**Cuándo vale la pena:** tu proyecto necesita que Claude *edite* una hoja de cálculo, no solo que la lea; o estás construyendo una automatización con scripts alrededor de Google Workspace.

**Cómo** — la misma ruta de instalación de la sección opcional del CLI gws que se cubrió en tu sesión de *Skills* y Configuración (Doc 3), si la tocaste ahí; si no, calcula ~1,5h de punta a punta (gcloud + el binario `gws` + OAuth). Para configurarlo ahora, pega esto en Claude Code:

```
I want to install the gws CLI so I can write to Google Sheets from Claude Code. Walk me
through it step by step: check whether I have gcloud, install the gws binary to ~/bin,
run the OAuth authentication, test a read command, and add a "Google Workspace Tools"
rule to my vault's CLAUDE.md. If anything fails, we'll troubleshoot it together.
```

Claude corre la instalación contigo. (Un detalle que ya sabe: los rangos de gws que contienen `!` necesitan `subprocess` de Python, no bash crudo.)

---

## PARTE 0.10: OPCIONAL — CURSOS AUTOGUIADOS DESDE TU *VAULT*

> ⚠ **Este kit no lo instala.** `/notebooklm` es un *skill* personalizado, no viene en el paquete de arranque ni en ninguno de los plugins de arriba — el prompt de abajo no tiene nada a qué llamar hasta que lo construyas (`/skill-create`) o tu facilitador comparta el suyo. Toma esta sección como un patrón hacia el cual construir, no como un comando para ejecutar hoy.

> **Enriquecimiento opcional.** Convierte tu propio material del *vault* — un brief de proyecto, un grupo de notas, un wiki, un conjunto de minutas — en un **curso autoguiado**: un cuaderno de NotebookLM con mazos de estudio, una vista general narrada y un Q&A que puedes interrogar. Excelente para profundizar en un tema en el que estás construyendo, o para hacerte onboarding a ti mismo (o a tu equipo) en un cuerpo de conocimiento que has acumulado.

**Qué hace:** `/notebooklm` toma las fuentes del *vault* que le señales y produce un conjunto de estudio estructurado — esquema → mazos → vista general narrada — para que *aprendas* el material en vez de solo almacenarlo. La jugada que compone: tu segundo cerebro no solo guarda conocimiento, también te lo enseña de vuelta.

**Cuándo usarlo:** ya has acumulado suficiente sobre un tema (un proyecto, un MOC de área, un wiki) como para que un recorrido guiado le gane a releer notas crudas.

**Cómo** — pega esto en Claude Code:

```
I want to turn [name your project / folder / wiki] into a self-guided course with
/notebooklm. Build the course outline from those notes and generate the study decks.
Before generating, tell me which sources you'll use.
```

Claude define contigo el alcance de las fuentes, y después ejecuta `/notebooklm` para construir el curso.

---

## PARTE 0.11: GENERA TU GUÍA DE USUARIO CONSOLIDADA

> **Haz esto una vez, después de que el resto de la configuración esté lista.** Ahora tienes un *vault*, un repositorio, plugins, *skills* y un monitor de contexto repartidos en varios lugares. Esto genera un único **`User Guide — [your name].md`** en la raíz de tu *vault* — el único mapa de *qué tienes y cómo encaja todo*. Complementa (no reemplaza) tu **AIAC Cheat Sheet** (referencia rápida de comandos) y las tareas de abajo. (Se genera de una sola pasada a partir de tu configuración real — es robusta sin importar en qué orden hayas instalado las cosas.)

**Pega esto en Claude Code:**

```
Generate my consolidated User Guide at `User Guide — [your name].md` at the root of my
vault. Read what's ACTUALLY installed and configured on my system — don't guess. Three
short, navigable sections:

- Section A — My Vault: the PARA structure, the CLAUDE.md chain (global → vault → repo),
  the 4 Obsidian settings, and where everything lives (vault vs. repo).
- Section B — Claude Code: the plugins and skills I have installed, the context monitor
  (the 50/75% bar), and Plan Mode. For the command quick-ref, point to my AIAC Cheat
  Sheet instead of duplicating it.
- Section C — My case workflows ([your project name]): the 2-3 concrete workflows for
  my project and their starter prompts.

It's a map, not a manual — keep it short.
```

Claude lee tu configuración real y escribe la guía. Vuelve a correrlo cada vez que tu sistema crezca.

---

## PARTE 1: TAREAS POST-SESIÓN — ESTA NOCHE, ESTA SEMANA, CHEAT SHEET, TRANCADO

> **Meta:** Meter datos reales en el repositorio, construir tu primer análisis, arrancar el ciclo de auto-mejora. Estructurado en 4 capas para que no se pierda nada.

### 1. Esta Noche (3 mini-acciones, antes de dormir)

Estas tres son diminutas. Hazlas esta noche mientras la sesión está fresca.

- [ ] **Abre tu *vault*.** `cd "[vault path]" && claude` — confirma que la sesión arranca y el router carga. Si `~/.claude/CLAUDE.md` no toma tu *vault* → avísale a tu facilitador.
- [ ] **Ejecuta el Prompt de Cierre Manual (ver APÉNDICE).** `/session-close` todavía no está activo en esta sesión (se instaló hoy — los *skills* solo se activan en una sesión nueva). Esto registra el trabajo de Fase 0 de hoy en el brief de tu proyecto y escribe el Continuation Prompt. El hábito empieza esta noche, no la semana que viene.
- [ ] **Escribe tu intención de proyecto para mañana** en la sección de Next Actions del brief del caso — una línea: "Mañana quiero ___." Esto ancla el Día 1.

### 2. Esta Semana (5 cosas para probar, en orden)

Una rampa secuenciada hacia el uso real. No te saltes pasos — cada uno se apoya en el anterior. (Este es un patrón general — tu versión específica de cada paso vive en la PARTE 3, "Los Próximos Flujos de tu Proyecto", que llenas al final de la sesión de hoy.)

1. Mete en `data/raw/` de tu repositorio el primer archivo de datos real que trajiste a la sesión de hoy y pídele a Claude que lo inventaríe — qué contiene, qué le falta, qué preguntas podría responder.
2. Corre tu primer análisis real usando el prompt que redactaste con tu facilitador en la PARTE 3.
3. Convierte ese primer análisis en una salida guardada — un reporte, un script o una nota en el brief de tu proyecto — para que no se quede tirado en el historial del chat.
4. Automatiza el paso manual más fastidioso de tu flujo — esa cosa que haces a mano todas las semanas. Pídele a Claude que la convierta en script o plantilla.
5. Corrige a Claude por lo menos una vez en voz alta, y después di "actualiza el CLAUDE.md para que esto no vuelva a pasar." Esta es tu primera repetición del ciclo de auto-mejora (PARTE 7).

> **Para tu PRÓXIMO proyecto (NO el caso de hoy — uno completamente nuevo):** ejecuta `/project-create` y deja que el *skill* te guíe con preguntas. **No pidas otro Prompt de Configuración** — de aquí en adelante, el flujo es autoservicio con `/project-create`. El Prompt de Configuración es solo para la Fase 0; después de eso, ya tienes el *skill* instalado.

### 3. Cheat Sheet — Siempre en el Mismo Lugar

Tu cheat sheet vive exactamente en esta ruta:

```
00 HUB/00 INBOX/AIAC Cheat Sheet.md
```

Esa es la ubicación canónica — no regada en `03 REFERENCE/`, ni flotando en otro lado. Fija este archivo en Obsidian.

El cheat sheet se creó durante tu sesión del Prompt de Configuración Principal (Doc 2). Si no lo encuentras: abre Obsidian, navega a `00 HUB/00 INBOX/` y busca `AIAC Cheat Sheet.md`. Si falta → avísale a tu facilitador, o pídele a Claude que vuelva a correr el paso del cheat sheet del Doc 2 para regenerarlo.

El cheat sheet contiene: comandos de inicio de sesión, el prompt del router, comandos esenciales, umbrales de la ventana de contexto, anclas de archivos. Todo lo que necesitas en una pantalla.

### 4. ¿Trancado? — Dónde Pedir Ayuda

No te quedas solo después de la sesión. La ayuda es **por niveles** — empieza arriba y solo escala cuando haga falta:

1. **Claude primero (la mayoría de los casos).** Pega los errores de vuelta en Claude, prueba `/systematic-debugging`, revisa la cadena de CLAUDE.md. Dale ~24h de depuración por tu cuenta antes de escalar — casi todo se resuelve justo aquí.
2. **Tu canal de soporte: [SET: your support channel].** Para dudas del día a día, problemas de instalación/configuración, o un rápido "¿esto es normal?" — pregunta aquí. No te quedes trancado en silencio — una pregunta compartida se resuelve más rápido, y ayudarse entre todos es parte de cómo sube de nivel una cohorte.
3. **Tu facilitador — para bloqueos de infraestructura.** Escríbele de inmediato si estás bloqueado por: una falla al instalar una herramienta, un problema de autenticación/inicio de sesión, una configuración de MCP que no conecta, o una prueba del router que falla. No quemes un día en plomería de infraestructura — eso es justo lo que tu facilitador normalmente desbloquea en minutos.

**Cuando pidas ayuda (en cualquier nivel):** incluye el prompt que ejecutaste, la salida exacta del error, y lo que ya intentaste. "Está roto" no es un mensaje de depuración.

### 5. Fin de la Semana 1 — Cierra Como Se Debe

```
/session-close
```

---

## PARTE 2: SEMANA 2 — CONSTRUYE TUS HÁBITOS DIARIOS

### En la Mañana: Arranca tu Día

```
Read my project brief at 01 PROJECTS/[project name].md.
What are my open next actions? What's the most important thing to work on today?
If there's a Continuation Prompt, summarize where I left off.
```

### Durante el Trabajo: Usa el Modo Plan

Para cualquier tarea no trivial, entra primero al **Modo Plan**:
- Presiona `Shift+Tab` dos veces
- Describe lo que quieres
- Revisa el plan
- Aprueba y ejecuta

### Antes de Terminar: Siempre Cierra

```
/session-close
```

Esto actualiza el brief de tu proyecto, registra lo que hiciste y crea un prompt de continuación. **Este es el hábito más importante de todos.** Cada sesión hace mejor a la siguiente.

### Semanal: Revisa el Avance

```
Read 01 PROJECTS/[project name].md.

Give me a weekly progress report:
1. What milestones have been completed?
2. What's in progress?
3. What's blocked and by whom?
4. What should I focus on next week?
5. Are we on track for the milestone targets?
```

---

## PARTE 3: LOS PRÓXIMOS FLUJOS DE TU PROYECTO

A diferencia de una cohorte pre-configurada, tu caso no se escogió por adelantado — tú y tu facilitador lo escogieron en vivo, durante la sesión de hoy, entre los 1 a 3 problemas que trajiste. Por eso esta sección arranca en blanco a propósito. Llénala antes de irte (Bloque 5), mientras la sesión está fresca — se convierte en tu versión personal de la rampa "Esta Semana" de la PARTE 1 y del mapa de progresión de la PARTE 8.

**Cómo llenarla.** Pídeselo a Claude directamente:

```
Based on everything we built and discussed today for [your project name], help me draft
3-5 workflows I'll actually run again — recurring reports, analyses, or documents specific
to my work. For each one, give me:
1. A short name
2. When I'd use it
3. A paste-ready prompt with real file paths from my repo

Save this list into my project brief's Next Actions, and also write it out below so I
have it in this brief too.
```

Después escribe cada uno aquí, siguiendo la misma forma de los prompts generales de la PARTE 4 — un nombre corto, una descripción de una línea de cuándo lo usarías, y el prompt exacto listo para pegar.

### Flujo 1: _______________________________
```
[paste-ready prompt — fill in during/after today's session]
```

### Flujo 2: _______________________________
```

```

### Flujo 3: _______________________________
```

```

### Flujo 4: _______________________________
```

```

### Flujo 5: _______________________________
```

```

> **¿Quieres un plan de Semana 1 día por día en vez de solo una lista de flujos?** Pídele a Claude: *"Ayúdame a convertir los flujos de arriba en un cronograma día por día para la Semana 1."*

---

## PARTE 4: PROMPTS GENERALES DE PRODUCTIVIDAD

### Investigar Cualquier Tema

```
/deep-research [topic]

Example:
/deep-research best practices for [relevant topic to your domain]
```

### Crear un Proyecto Nuevo

Abre Claude Code en tu *vault*, y luego:

```
I need to create a new project. Help me fill out a Project Brief.

Project name: [NAME]
What I want to achieve: [DESCRIBE THE OUTCOME]

Use the Project Brief Template in Templates/ and save the brief in 01 PROJECTS/.
```

### Tomar una Decisión

```
I need to make a decision about: [DESCRIBE THE DECISION]

Help me think through this structured:
1. What are the options? (at least 3)
2. What are the pros and cons of each?
3. What's the risk if we pick wrong?
4. What information am I missing?
5. What's your recommendation and why?

Save this as a decision memo in 00 HUB/00 INBOX/.
```

### Analizar una Hoja de Cálculo

```
Read the file [FILENAME] in data/.
Tell me:
1. What's in this data? (columns, row count, date range)
2. Summary statistics for the numerical columns
3. Any patterns, trends, or anomalies
4. 3 questions this data could answer
5. What other data would I need to combine with this for a complete picture?
```

### Crear un *Skill* Personalizado

Cuando te descubras haciendo algo repetidamente:

```
/skill-create

I keep doing [DESCRIBE THE REPEATED TASK].
Help me create a skill that automates this.
```

### Flujo de Git

```
# After finishing work:
/commit

# If you want to push too:
/commit-push-pr
```

---

## PARTE 5: CATÁLOGO DE *SKILLS* — PRIORIZADO

> 🚀 **ATAJO — Instala primero el paquete de arranque.** El programa mantiene un repositorio público curado con los 8 *skills* de Nivel 1 pre-configurados y listos para instalar de una sola vez:
>
> **[wildbuffaloman/cc-starter-pack](https://github.com/wildbuffaloman/cc-starter-pack)** — público
>
> ```bash
> # Clone + install Tier 1 skills with one command:
> git clone https://github.com/wildbuffaloman/cc-starter-pack.git
> cd cc-starter-pack
> ./install.sh                # copies into ~/.claude/skills/ (default)
> ./install.sh symlink        # symlinks instead — keep updated via `git pull`
> ```
>
> Los 8 *skills* vienen con secciones canónicas `## Dependencies` que declaran exactamente qué necesita cada uno. Solo `/session-close` tiene requisitos de CLI externos (`jq` + `git`); el resto funciona de una con las herramientas integradas de Claude Code.
>
> **Después de correr `./install.sh`: reinicia Claude Code y prueba con `/context`** — si corre, ya estás listo.
>
> **¿Por qué un paquete de arranque en vez de construir desde cero?** Los *skills* de abajo tomaron meses de refinamiento. El paquete trae esa experiencia empaquetada para que arranques productivo desde el día 1 en vez de reinventar patrones. Los *skills* de Nivel 2 en adelante (abajo) los vas a construir o pedir individualmente a medida que aparezcan tus necesidades.
>
> Si prefieres copiar un solo *skill* a mano: cada SKILL.md del repositorio es autocontenido — cópialo en `~/.claude/skills/[skill-name]/SKILL.md`. Los *skills* marcados con un prompt en las tablas de abajo se pueden probar de inmediato incluso sin instalarlos — solo pega el prompt.

### NIVEL 1 — ESENCIALES (Instala en la Semana 1 — los 8 están en el paquete de arranque de arriba)

Estos son los *skills* que vas a usar en casi todas las sesiones. Instala los 8 de una con el paquete de arranque, o uno por uno.

| # | *Skill* | Qué hace | Cómo se usa | ¿En el paquete? |
|---|-------|-------------|-----------|------------------|
| 1 | **session-close** | Cierra la sesión como se debe — actualiza el brief, registra el trabajo, crea el prompt de continuación, revisión de código, retro | `/session-close` | ✅ |
| 2 | **context** | Muestra el uso actual de la ventana de contexto y la info de la sesión | `/context` | ✅ |
| 3 | **permissions** | Muestra la configuración actual de permisos | `/permissions` | ✅ |
| 4 | **retro** | Corre una retrospectiva — qué funcionó, qué no, qué cambiar | `/retro` | ✅ |
| 5 | **extract** | Extracción inteligente de contenido desde cualquier nota o URL — salida estructurada de 6 secciones | `/extract [note or URL]` | ✅ |
| 6 | **skill-create** | Crea *skills* personalizados de forma interactiva | `/skill-create` | ✅ |
| 7 | **project-create** | Crea un brief de proyecto con preguntas y respuestas interactivas | `/project-create` | ✅ |
| 8 | **deep-research** | Investigación profunda en dos fases — barrido amplio y luego síntesis en un brief estructurado con fuentes | `/deep-research [topic]` | ✅ |

### NIVEL 2 — PRODUCTIVIDAD DIARIA (Instala en la Semana 2)

Estos son candidatos del Nivel B de la iniciativa del paquete de arranque — van a salir como un segundo paquete después de que el Nivel 1 se pruebe. Por ahora, tu facilitador te puede señalar cada uno, o los puedes reconstruir a partir del patrón.

| # | *Skill* | Qué hace | Cómo se usa |
|---|-------|-------------|-----------|
| 9 | **startup-day** | Centro de mando matutino — agrega tareas, calendario y seguimientos en un plan de acción priorizado | `/startup-day` |
| 10 | **close-day** | Cierre de fin de día — escanea todos los sistemas, actualiza briefs, sincroniza tareas, vista previa de mañana | `/close-day` |
| 11 | **last30days** | Busca en Reddit, X, YouTube, HN, etc. lo que está pasando ahora mismo (⚠ requiere una API key paga de ScrapeCreators + `yt-dlp`) | `/last30days [topic]` |
| 12 | **library** | Crea una nota índice de Biblioteca para un tema, pre-poblada con notas enlazadas del *vault* | `/library [topic]` |

### NIVEL 3 — FLUJOS SEMANALES (Instala en las Semanas 2-3)

| # | *Skill* | Qué hace | Cómo se usa |
|---|-------|-------------|-----------|
| 13 | **weekly-review** | Revisión semanal GTD completa — escaneo del *vault*, calendario, vaciado del inbox, sincronización de tareas, planificación de la próxima semana | `/weekly-review` |
| 14 | **weekly-prep** | Planifica el calendario de la próxima semana — bloques de trabajo profundo, eventos de rutina, agendas de reuniones | `/weekly-prep` |
| 15 | **monthly-review** | Revisión estratégica mensual — recalibración de prioridades, salud de proyectos, finanzas personales, reflexiones | `/monthly-review` |
| 16 | **inbox-clear** | Vaciado del inbox estilo GTD — clasifica cada nota, propone acciones, ejecuta tras aprobación | `/inbox-clear` |
| 17 | **read-review** | Revisa los ítems de READ_REVIEW — resúmenes estructurados, ideas clave, acciones | `/read-review` |
| 18 | **meeting-agenda** | Crea/actualiza agendas de reuniones con contexto de calendario + *vault* + externo | `/meeting-agenda [meeting name]` |
| 19 | **meeting-minutes** | Genera minutas de reuniones a partir de grabaciones de Granola | `/meeting-minutes` |
| 20 | **followup** | Escanea los briefs de proyectos buscando ítems de Waiting For, los clasifica por elegibilidad y envía seguimientos | `/followup` |

### NIVEL 4 — ANÁLISIS DE NEGOCIO (Instala en las Semanas 3-4)

| # | *Skill* | Qué hace | Cómo se usa |
|---|-------|-------------|-----------|
| 21 | **decision-memo** | Documento estructurado de decisión — contexto, 3 o más alternativas, análisis, recomendación | `/decision-memo` |
| 22 | **strategy-brief** | Análisis estratégico para una decisión de negocio, movida de mercado o iniciativa | `/strategy-brief` |
| 23 | **scenario-model** | Construye 3 o más escenarios con resultados ponderados por probabilidad y análisis de sensibilidad | `/scenario-model` |
| 24 | **okr-update** | Actualiza el tablero de OKR — revisa el avance, marca lo que va fuera de curso | `/okr-update` |
| 25 | **okr-cascade** | Revisa la alineación de OKR — cascada de empresa a equipo/individuo, identifica brechas | `/okr-cascade` |
| 26 | **blind-spot-scan** | Análisis socrático de puntos ciegos — saca a la superficie lo que no sabes que no sabes, con preguntas de sondeo | `/blind-spot-scan` |
| 27 | **learning-program** | Crea un programa de aprendizaje estructurado sobre cualquier tema con deconstrucción de habilidades por IA | `/learning-program [topic]` |
| 28 | **contact-card** | Crea una Contact Card rica — combina datos del *vault*, investigación web y contexto de la relación | `/contact-card [name]` |

### NIVEL 5 — NEGOCIACIÓN Y VENTAS (Instala Cuando lo Necesites)

| # | *Skill* | Qué hace | Cómo se usa |
|---|-------|-------------|-----------|
| 29 | **negotiation-prep** | Preparación completa de negociación — investigación de la contraparte, BATNA, mapeo de actores, playbook | `/negotiation-prep` |
| 30 | **negotiation-coach** | Coaching de negociación en vivo — enruta a modo preparación, en vivo o debrief | `/negotiation-coach` |
| 31 | **batna-analysis** | Modelado enfocado de BATNA — identifica, evalúa y ordena alternativas para un trato específico | `/batna-analysis` |
| 32 | **concession-framework** | Diseña una secuencia estructurada de concesiones — ítems negociables, secuenciación, pedidos recíprocos | `/concession-framework` |
| 33 | **objection-tree** | Navega árboles de decisión de objeciones con tácticas de Voss / Cisne Negro / Gap | `/objection-tree` |
| 34 | **stakeholder-map** | Mapea la arquitectura de decisión de la contraparte — 6 tipos de actores con estrategia de acercamiento | `/stakeholder-map` |

### NIVEL 6 — GESTIÓN DEL *VAULT* (Aprende Después)

| # | *Skill* | Qué hace | Cómo se usa |
|---|-------|-------------|-----------|
| 35 | **clean-areas** | Audita `02 AREAS/` — corrige desviaciones de MOC, hace cumplir plantillas, detecta huérfanos | `/clean-areas` |
| 36 | **clean-projects** | Audita `01 PROJECTS/` — cumplimiento de plantilla, detección de contenido estancado | `/clean-projects` |
| 37 | **clean-reference** | Audita `03 REFERENCE/` — detecta archivos mal enrutados, hace cumplir la estructura | `/clean-reference` |
| 38 | **vault-link-scan** | Escaneo de enlaces Zettelkasten — descubre conexiones, inserta wikilinks, repara enlaces rotos | `/vault-link-scan` |

### NIVEL 7 — META / HERRAMENTAL (Avanzado)

| # | *Skill* | Qué hace |
|---|-------|-------------|
| 39 | **bible-sync** | Sincronización mensual de la Claude Code Bible contra la configuración en vivo |
| 40 | **skills-audit** | Escanea los directorios de *skills* y cruza las configuraciones |
| 41 | **skill-health-report** | Genera un reporte de salud de todos los *skills* |
| 42 | **push-skills** | Sube los *skills* actualizados a los repositorios de GitHub |

---

## PARTE 6: REFERENCIA DE PLUGINS

### Instalados (de tu sesión de Fase 0 + la Parte 0 de arriba)

| Plugin | Comandos clave | Qué hace |
|--------|-------------|-------------|
| **Compound Engineering** | `/ce:plan`, `/ce:work`, `/ce:brainstorm`, `/ce:review` | Flujo de desarrollo con planificación primero y agentes de investigación en paralelo |
| **Superpowers** | `/brainstorm`, `/systematic-debugging`, `/test-driven-development`, `/verification-before-completion` | Flujos estructurados para depurar, hacer lluvia de ideas y TDD |
| **Explanatory Output Style** | (automático) | Claude explica su razonamiento mientras trabaja — excelente para aprender cómo piensa |
| **Commit Commands** | `/commit`, `/commit-push-pr` | Commits de git inteligentes con mensajes autogenerados |
| **Skill Creator** | `/skill-create` | Asistente interactivo de creación de *skills* (el *plugin* `skill-creator` de la PARTE 0 hace lo mismo — solo necesitas uno) |
| **Claude MD Management** | `/claude-md-improver` | Audita y mejora los archivos CLAUDE.md |
| **Context7** | (automático) | Trae documentación actualizada de librerías cuando las mencionas |
| **Code Review** | `/code-review` | Revisa el código en busca de errores, seguridad y calidad |
| **Firecrawl** | (reemplaza la búsqueda web) | Investigación web, scraping, lectura de documentación — superior a las herramientas web integradas |
| **Playground** | `/playground` | Crea visualizaciones HTML interactivas para explorar ideas |

### Plugins Opcionales (Instala Después)

| Plugin | Qué hace | Cuándo instalarlo |
|--------|-------------|----------------|
| **Feature Dev** | Desarrollo guiado de funcionalidades con análisis del código base | Cuando construyas funcionalidades más grandes |
| **PR Review Toolkit** | Revisión integral de código en PRs | Cuando hagas revisiones de código |
| **Frontend Design** | Generación de interfaces frontend de alta calidad | Cuando construyas interfaces o tableros |
| **Playwright** | Automatización de navegador para pruebas | Cuando pruebes aplicaciones web |
| **Hookify** | Crea *hooks* para prevenir comportamientos no deseados | Cuando quieras automatizar reglas |
| **GitHub** | Integración con GitHub | Cuando uses GitHub más intensamente |

---

## PARTE 7: EL CICLO DE AUTO-MEJORA

Este es el concepto más importante. Es lo que separa a los usuarios productivos de Claude Code de todos los demás.

### El Ciclo

```
1. Work with Claude Code
2. Claude makes a mistake -> correct it
3. Tell Claude: "Update the CLAUDE.md so this doesn't happen again"
4. Next session reads the updated CLAUDE.md
5. Mistake doesn't happen again
6. Repeat for weeks -> CLAUDE.md accumulates intelligence
7. After a month, Claude genuinely works better for YOU
```

### Prompt para Arrancar el Ciclo

Cada vez que Claude haga algo mal:

```
That's not right. [Explain what was wrong and what the correct approach is.]
Now update the CLAUDE.md to add a rule that prevents this mistake in the future.
```

### Tus Correcciones

Las correcciones son específicas de tu dominio — van a salir de errores reales que Claude cometa en **tu** proyecto, no de una lista genérica. Aquí está el patrón, más espacio para que registres las tuyas a medida que ocurran esta semana:

**Patrón:**
> "[Lo que Claude hizo mal] no está bien — [por qué, y cuál es el enfoque correcto]. Agrega esta regla al CLAUDE.md para que no vuelva a pasar."

**Registra las tuyas aquí a medida que ocurran:**

1. Corrección — ___________________________:
   > "..."

2. Corrección — ___________________________:
   > "..."

3. Corrección — ___________________________:
   > "..."

---

## PARTE 8: MAPA DE PROGRESIÓN

### Semana 1: Configuración + Primer Uso Real
- [ ] Plugins instalados (Parte 0)
- [ ] Datos reales del proyecto metidos en `data/raw/` (o equivalente) en tu repositorio
- [ ] Primera pasada de análisis corrida y guardada (no solo dejada en el chat)
- [ ] Al menos 3 sesiones de Claude Code completadas
- [ ] `/session-close` ejecutado al final de cada sesión
- [ ] Primer flujo de la PARTE 3 probado de punta a punta

### Semana 2: Hábitos Diarios
- [ ] Chequeo matutino diario con el brief de tu proyecto
- [ ] Modo Plan usado al menos dos veces
- [ ] Primera salida automatizada/repetible generada (un reporte, script o plantilla)
- [ ] Al menos 2 correcciones agregadas a tu CLAUDE.md (ciclo de auto-mejora, PARTE 7)
- [ ] Un *skill* `weekly-review` **construido** con `/skill-create` (no está en el paquete de arranque — lo construyes tú; ver Nivel 3) y ejecutado una vez

### Semana 3: Flujos Operativos
- [ ] 2-3 de tus flujos de la PARTE 3 probados y refinados
- [ ] Un *skill* personalizado creado para un flujo que ya has repetido 3 veces o más (`/skill-create`)
- [ ] Repositorio de GitHub actualizado al menos dos veces
- [ ] *Skills* de Nivel 2-3 instalados (ver PARTE 5)

### Semana 4: Autonomía
- [ ] Tu flujo principal corre con un solo prompt listo para pegar, sin retrabajo
- [ ] El CLAUDE.md tiene 5 o más reglas acumuladas del ciclo de auto-mejora
- [ ] Usas Claude Code 30 minutos reales al día o más
- [ ] Listo para tomar un segundo proyecto (`/project-create`)

### Mes 2: Expansión
- [ ] Un segundo proyecto o caso arrancado con `/project-create`
- [ ] *Skills* de Nivel 3-4 instalados y en uso regular
- [ ] Al menos un flujo completamente automatizado de punta a punta

### Mes 3: Dominio
- [ ] Claude Code es parte por defecto de tu trabajo diario, no una novedad
- [ ] Has creado 2 o más *skills* personalizados propios
- [ ] Te sientes cómodo corrigiendo a Claude y actualizando el CLAUDE.md sin que nadie te lo pida

---

## APÉNDICE: TARJETA DE REFERENCIA RÁPIDA

### Empezar a Trabajar

> **Dos lugares, dos propósitos.** Tu *vault* (notas, planificación, briefs) y el repositorio de tu proyecto (`~/dev/[your-repo-name]`, código + datos) son carpetas separadas — el router (`~/.claude/CLAUDE.md`) se asegura de que Claude lea la cadena de CLAUDE.md correcta sin importar en cuál estés.

```bash
# Notes, projects, thinking (vault root):
cd "[vault path]" && claude

# Code and data (your repo, in ~/dev/):
cd ~/dev/[your-repo-name] && claude
```

### Flujo Esencial de una Sesión
```
1. Start: claude reads CLAUDE.md automatically
2. Check continuation: "Read my project brief. Where did I leave off?"
3. Plan: Shift+Tab twice -> describe task -> review plan -> approve
4. Work: Execute the plan
5. Close: /session-close
```

### Cuando Estés Trancado
```
/systematic-debugging

I'm stuck on: [describe the problem]
What I've tried: [what you already tried]
What I expected: [what should have happened]
```

### Cuando Empieces Algo Nuevo
```
/ce:plan [describe what you want to build]
```

### Cuando Necesites Investigar
```
/deep-research [topic]
```

### Cuando Vayas a Terminar
```
/session-close
```

---

## APÉNDICE: PROMPT DE CIERRE MANUAL

> **Cuándo usarlo:** `/session-close` se instaló más temprano en ESTA MISMA sesión — los *skills* solo se activan en sesiones abiertas DESPUÉS de instalarlos. Así que esta noche, justo cuando termine la sesión de hoy, usa este prompt de cierre manual. Desde la sesión de mañana en adelante, `/session-close` funciona normal.

```
Please close this session:
1. At the top of my case project brief's Next Actions section, add or replace the
   ### Continuation Prompt block with:
   - Today's date
   - Mode: Vault Management
   - Context summary: what we did in this Phase 0 session (vault scaffolding, project
     brief created, GitHub repo pushed, case file scaffolded, skills installed, router
     test passed)
   - Resume-from: next actions for Week 1 homework
   - Files touched in this session
2. Append a Log entry: "Phase 0 session completed — vault scaffolded, case brief created,
   GitHub repo pushed, skills installed, router validated."
3. Do not invoke /session-close — it's installed but not yet active in this session
   (skills load on new sessions only). Perform the updates directly via Edit.
```

---

## COMPUERTA 5.5 — GUARDA ESTE BRIEF EN TU *VAULT* (CONFIRMACIÓN FINAL)

> **Haz esto al cierre de la sesión — antes de pararte del escritorio.** Evita la fricción de "¿dónde quedó esa lista de tareas?".

Haz esto AHORA, frente a tu facilitador si es una sesión en vivo:

1. Guarda este documento en tu *vault* en `00 HUB/00 INBOX/Next Steps Brief.md` (copia el contenido que compartió tu facilitador, o pídele a Claude que lo guarde ahí por ti).
2. Abre Obsidian y confirma que lo encuentras en `00 HUB/00 INBOX/`.
3. Confirma que tu `AIAC Cheat Sheet.md` (creado durante tu sesión del Prompt de Configuración Principal, Doc 2) está justo al lado, en la misma carpeta.
4. Di en voz alta: "Encontré los dos archivos en `00 HUB/00 INBOX/`."

Si no encuentras uno o los dos archivos → todavía no han llegado. Vuelve a correr el paso del cheat sheet del Doc 2 para el Cheat Sheet, y guarda manualmente el contenido de este brief en INBOX. NO cierres la sesión hasta que ambos archivos se vean en `00 HUB/00 INBOX/` desde Obsidian.

**Por qué existe esta compuerta:** es fácil salir de una sesión con la hoja de ruta de tareas flotando en una ventana de chat, un enlace de Drive o un correo — y perderle el rastro en 48 horas. INBOX es la única carpeta que todo participante sabe encontrar. Los dos archivos viven ahí, siempre.

---

> *Parte del programa Fase 0 del AI Acceleration Club — esta hoja de ruta destila patrones refinados a lo largo de meses de uso diario de Claude Code en una rampa paso a paso para tu primer mes.*
