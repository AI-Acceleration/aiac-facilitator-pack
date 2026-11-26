---
title: "Brief de Próximos Pasos (Participante) — Kit de Co-Facilitación Fase 0 AIAC (ES)"
created: 2026-07-14
category: reference
tags: [aiac, phase0, co-facilitator, next-steps, spanish]
lang: es
translated_from: "04 — Next Steps Brief (Participant).md"
---

*Se le entrega al participante al cierre de la sesión (Bloque 5) como su hoja de ruta de tareas, junto con el Doc 06 — Kit de Supervivencia del Plan Pro.*

# Brief de Próximos Pasos — Dominio de Claude Code

> **Qué es esto:** tu hoja de ruta desde la configuración hasta el uso diario productivo, en orden de prioridad. **Primero la Parte 0** (cerrar bien la Fase 0, esta semana), después la Semana 1, después lo demás. Cada sección trae prompts listos.

## Cómo se Usa Este Brief

- **Prompts cortos** (los bloques de este documento): cópialos y pégalos en Claude Code. En Windows se pega con clic derecho (o `Shift+Insert`), no con Ctrl+V.
- **Prompts largos o archivos enteros:** no los pegues; la terminal puede cortar lo que pegas si es largo. En Obsidian, clic derecho sobre el archivo → **Copiar ruta** (la ruta completa del sistema), y en Claude Code escribe `Lee el archivo <ruta> y sigue sus instrucciones.` Es la misma vía con la que cargaste los prompts de configuración.
- **Donde Claude pueda correr algo por ti, recibes un prompt**, no una lista de comandos. Los comandos de terminal aparecen sólo donde Claude de verdad no puede hacer el paso (un inicio de sesión interactivo, un clic en una app).
- **Junto a este brief** tienes el **Doc 06 — Kit de Supervivencia del Plan Pro** (léelo si estás en Pro) y el **Doc 07 — Vocabulario** (todos los términos en una página).

> **Sobre el plan.** Claude **Pro** es lo estándar y alcanza para empezar. Todos los planes tienen límites de uso que se reinician cada pocas horas y cada semana. El Doc 06 explica cómo repartir las sesiones pesadas y hacer que Pro rinda. Sube a Max sólo si chocas una y otra vez con los límites ([claude.com/pricing](https://claude.com/pricing)).

---

## PARTE 0: PRIMERO CIERRA LA FASE 0 (ESTA SEMANA)

### 0.1 Revisa lo que dejó la configuración

Abre una sesión en tu *vault* (`cd "<ruta de tu vault>"` y después `claude`) y pega:

```
Revisa lo que dejó armado mi configuración de la Fase 0. No cambies nada: sólo mira, y dame LISTO o FALTA en cada punto.
1. ~/.claude/CLAUDE.md (el enrutador global) y el CLAUDE.md de la raíz de mi vault.
2. ~/.claude/settings.json es JSON válido y tiene CLAUDE_AUTOCOMPACT_PCT_OVERRIDE en 75. Corre exactamente
   esto; imprime solo OK o NOT OK, nunca un valor del archivo (puede guardar llaves):
   jq -e '(.env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE | tostring) == "75"' ~/.claude/settings.json >/dev/null 2>&1 && echo OK || echo "NOT OK"
3. El cheat sheet: 00 HUB/00 INBOX/AIAC Cheat Sheet.md
4. La plantilla: Templates/Project Brief Template.md
5. El mapa de mi área: un archivo <Área>.md dentro de 02 AREAS/<Área>/
6. El brief de mi recorrido: 01 PROJECTS/AI Acceleration/<Mi Nombre>/AI Acceleration Club - <Mi Nombre> Journey.md
7. El brief del proyecto de mi caso: 01 PROJECTS/<Nombre del Proyecto>/<Nombre del Proyecto>.md
8. Mi repo, fuera del vault y en GitHub, privado:
   ls ~/dev/<nombre-del-repo> y gh repo view github.com/<dueño>/<nombre-del-repo> --json nameWithOwner,visibility
   (visibility tiene que ser PRIVATE)
9. La carpeta 05 AI/CLAUDE CODE/resources/ (ahí aparece lessons.md con mi primera lección;
   que todavía no exista no es una FALTA).
10. Mis skills y plugins: lista las carpetas de ~/.claude/skills/ y corre claude plugin list.
Si algo falta, dime qué paso del Main Setup Prompt o del Skills & Config Setup Prompt lo crea.
No lo rehagas por tu cuenta.
```

Si falta algo de la configuración, carga ese archivo de configuración por ruta y pide sólo ese paso: `Lee el archivo <ruta del prompt de configuración> y corre sólo el PASO N.` Si el repo **no** es privado, arregla eso primero (en GitHub: Settings → General → Danger Zone → Change visibility → Private).

### 0.2 El brief de tu caso, con `/project-create` (sólo si falta)

Normalmente el Main Setup Prompt crea el brief de tu caso. **Si la 0.1 dice que existe, sáltate esto**; no crees un segundo brief. Si falta, créalo con la *skill* `/project-create`, que te entrevista. Es el mismo recorrido que vas a seguir cada vez que arranques algo nuevo.

1. **Abre una ventana NUEVA de Claude Code** en tu *vault*. Las *skills* cargan sólo en sesiones nuevas.
2. **Escribe exacto:**

   ```
   /project-create
   ```

   Si al escribir `/` no aparece en la lista, no está instalada: pide ayuda en [SET: your support channel]. Escribir sólo el nombre del proyecto **no** llama a la *skill*.
3. Como nombre del proyecto usa el nombre de tu caso. Responde con lo que conversaron en la sesión.
4. **Si Claude empieza a escribir código o te pide instalar algo, no estás en la *skill*.** Presiona `Esc` y vuelve al punto 2.
5. Cuando termine, revisa dónde quedó el brief. Va en su propia carpeta: `01 PROJECTS/<Nombre del Proyecto>/<Nombre del Proyecto>.md`. Si quedó en otro lado, dile a Claude: `Muévelo a 01 PROJECTS/ en su propia carpeta, con el mismo nombre.`
6. Abre el brief en Obsidian y léelo completo. Si tu repo no aparece en `## Key Resources`, pídele a Claude que agregue `~/dev/<nombre-del-repo>`.

### 0.3 Cierra a mano la sesión de configuración

`/session-close` se instaló **durante** tu sesión de configuración. Las *skills* sólo cargan en sesiones que arrancan después de instalarlas, así que en esa misma sesión todavía no funciona. Ciérrala con el **APÉNDICE: PROMPT DE CIERRE MANUAL** del final de este brief. Desde tu próxima sesión, `/session-close` funciona normal.

Cuando termines la Parte 0, cierra con `/session-close`.

---

## PARTE 0.5: CONCEPTOS E INVENTARIO — LÉELO UNA VEZ

> **Por qué existe esta sección:** en tu sesión de Fase 0 pasamos rápido por mucha plomería. Ésta es la página de «teoría + inventario»: la referencia a la que vuelves cuando quieres entender *por qué* algo está conectado así, o *qué* quedó instalado exactamente. Léela completa una vez antes de la Semana 1. Después repásala cada semana durante el primer mes.

### Los 4 Conceptos Clave

#### 1. CLAUDE.md — El Cerebro del Sistema

No hay UN `CLAUDE.md`. Hay una **cadena** que Claude lee solo al arrancar cada sesión:

| Dónde | Para qué | Cuándo lo lee Claude |
|----------|---------|---------------------|
| `~/.claude/CLAUDE.md` | **Enrutador global + tu perfil.** Le dice a Claude dónde está tu *vault*, quién eres, tus reglas por defecto. | En toda sesión, arranques donde arranques |
| `[vault]/CLAUDE.md` | **Reglas del *vault*.** Cómo manejar las notas, la estructura PARA, la seguridad, el idioma. | En toda sesión que arranca dentro del *vault* |
| `[repo]/CLAUDE.md` | **Reglas del proyecto.** Principios del dominio, fuentes de datos, qué se puede tocar y el puente de vuelta a tu brief. | En toda sesión que arranca dentro de ese repo |

**La idea central:** el `CLAUDE.md` es la forma en que el sistema **mejora con el tiempo**. Cada vez que corriges a Claude, agrega la regla al `CLAUDE.md` que corresponde. En la próxima sesión, la corrección se queda. Al mes, Claude de verdad trabaja mejor para TI porque las reglas se acumulan.

**Regla de especificidad:** la corrección va en el `CLAUDE.md` MÁS específico que aplique. Del proyecto → el `CLAUDE.md` del repo. De cómo tomas notas en general → el del *vault*. Para TODOS los proyectos (por ejemplo «respóndeme siempre en español») → `~/.claude/CLAUDE.md`.

#### 2. La Ventana de Contexto — Tu Memoria de Trabajo

La ventana de contexto de Claude es limitada. Mientras trabajas en una sesión, se llena con el historial de la conversación, los archivos que Claude lee, las salidas de las herramientas, etc. Pasado cierto punto, **la calidad baja**: a eso se le llama **degradación del contexto**.

**Los umbrales que importan:**
- **Compacta IDEALMENTE antes del 50%:** la mejor calidad, el estado se traspasa limpio. Ésa es la meta.
- **Después del 50% empieza la degradación:** no es catastrófico, pero Claude empieza a olvidar lo del principio y a confundir detalles.
- **Compacta SÍ O SÍ antes del 70%:** pasado el 70%, la calidad se desploma. Una compactación forzada a última hora es mucho más desordenada que una a tiempo.

**Las opciones para compactar al llegar al umbral:**
- Corre `/session-close` y después `/clear` para empezar de cero (lo más limpio: el estado queda guardado en el Continuation Prompt del brief de tu proyecto, y después se reinicia).
- O corre `/compact` para resumir en el sitio y seguir a mitad de tarea (más rápido, pero pierde detalle: prefiere la opción de arriba en una pausa natural).

**Cómo ves tu uso:** tu % de contexto aparece como una barra en vivo abajo en la terminal, el monitor de contexto que montó tu Main Setup Prompt. La barra se pone **amarilla ⚠ al 50%** (con un aviso de una sola vez), y la **compactación automática queda apagada**, así que nada se comprime a tus espaldas: al 75% la barra se pone roja y esa es tu señal para correr `/session-close` (o `/compact`). Si ignoras la barra roja, un pedido posterior puede fallar; entonces corre `/compact` tú mismo. Si no ves la barra, abre una sesión nueva; si sigue sin aparecer, escribe `/context` para ver el estado actual y pídele a Claude que vuelva a correr el PASO 3.5 de tu Main Setup Prompt (no uses `/statusline-setup`: reemplaza la barra personalizada y quita el aviso del 50%).

#### 3. Skills — Procedimientos Reutilizables

Una *skill* es un prompt estructurado + un flujo de trabajo guardado en `~/.claude/skills/{nombre}/SKILL.md` (o dentro de un plugin) que Claude corre cuando escribes `/{nombre}`. Ya tienes `/session-close` y las demás *skills* iniciales de tu paso de Skills & Config.

**Cómo se invoca una *skill*:** escribe `/` en Claude Code y elige del autocompletado (basta parte del nombre, por ejemplo `/session`).

**Cuándo crear una *skill* nueva:** si te encuentras dándole a Claude las mismas instrucciones 3 veces o más, merece una *skill*. Corre `/skill-create` y Claude te guía para definirla.

**Por qué importan:** convierten patrones sueltos en infraestructura duradera. Una *skill* que escribes en la Semana 2 sigue funcionando en el Mes 6 sin que te acuerdes de los detalles.

#### 4. MCP y Conectores — Sistemas Externos

MCP («Model Context Protocol») es la forma en que Claude Code habla con sistemas más allá de tus archivos: correo, calendarios, documentos, herramientas de transcripción, bases de datos.

**Lo que conectaste en tu paso de Skills & Config** depende de tu plataforma:
- **Google:** los conectores de claude.ai para Gmail, Google Drive y Google Calendar.
- **Microsoft 365:** el conector de Microsoft 365 de claude.ai (correo y calendario de Outlook, OneDrive, SharePoint), si tu cuenta lo permite.
- **Reuniones:** `/meeting-minutes` lee del conector de tu herramienta de transcripción, o de una transcripción que pegas.
- **Cuenta Team o Enterprise:** el administrador de tu organización decide qué conectores puedes ver.

> **Si un conector de claude.ai no terminó de autorizarse durante la sesión:** entra a claude.ai → Settings → Connectors, ábrelo y completa la autorización. Después, en una sesión **nueva** de Claude Code, pruébalo con un prompt rápido (por ejemplo *«Lista mis 3 correos más recientes.»*). Si sigue sin autorizarse, mándale a tu facilitador el error exacto.

**Para agregar más después:** pídele a Claude que te ayude a agregar un servidor MCP cuando un flujo lo necesite, y consúltalo antes con tu facilitador si toca datos del trabajo. Acceso a bases de datos: sólo lectura por defecto. Los conectores y servidores MCP nuevos aparecen en sesiones **nuevas**.

**MCP vs. CLI:** los MCP son conectores estructurados (Claude recibe herramientas con entradas y salidas definidas). Las CLI son comandos sueltos que Claude escribe en la terminal. Los MCP son más limpios para operaciones frecuentes; las CLI sirven para tareas puntuales o del sistema operativo.

### Dos Lugares, Dos Tipos de Sesión

Muchas veces vas a tener **dos sesiones de Claude Code abiertas a la vez**: una en tu *vault* (notas, planificación, briefs) y otra en el repo de tu proyecto en `~/dev/[nombre-de-tu-repo]` (código, datos, scripts). Es normal; así está diseñado el enrutador + la cadena de `CLAUDE.md`.

1. **Las *skills* y los plugins cargan sólo en sesiones nuevas.** Algo instalado durante una sesión aparece como instalado pero no queda activo hasta que abres una ventana nueva de Claude Code.
2. **Cada proyecto tiene su propio `CLAUDE.md` y su propio estado.** Correr el análisis de tu caso dentro de una sesión de planificación del *vault* mezcla dos registros. Mantén el trabajo del *vault* y el del repo en ventanas separadas.
3. **El enrutador te lleva al proyecto correcto.** Desde cualquier carpeta, en una ventana nueva, di *«trabajemos en mi proyecto [nombre del caso]»*: Claude abre tu proyecto con su Continuation Prompt, sin `cd`.

La regla de dónde vive cada cosa: el **conocimiento** (notas, briefs, gestión de proyectos) en el *vault*; los **repositorios de código** en `~/dev/`. Si una carpeta tiene su propio `.git/`, va en `~/dev/`.

### Trabajar en la App de Escritorio de Claude

Todo lo configuraste en la terminal, y ahí es donde se hacen las instalaciones y los cambios de configuración. La pestaña **Code** de Claude Desktop lee la misma carpeta `~/.claude` (tus *skills*, tu configuración y tus `CLAUDE.md`), así que puedes hacer el trabajo del día a día ahí si prefieres una ventana a una terminal. Comandos como `claude plugin …` y `claude mcp add …` siguen necesitando la terminal.

### Portabilidad — Tu Sistema no Queda Amarrado

Todo lo que armaste son archivos Markdown planos, Git y herramientas estándar. Claude Code es la herramienta recomendada hoy, pero tu *vault*, tus briefs y tus reglas de `CLAUDE.md` son sólo texto: otra herramienta de IA podría leerlos mañana. Nada de tu segundo cerebro depende de un solo proveedor.

### Buenas Prácticas — El Ciclo Central

Éstos son los 7 hábitos que separan a quien usa Claude Code de forma productiva del resto. Interiorízalos todos para la Semana 4.

1. **Cierra siempre con `/session-close`.** Sin excepciones. Es el hábito que hace que el sistema se acumule.
2. **Planifica antes de construir.** Cualquier tarea que toque 2 archivos o más: presiona `Shift+Tab` hasta que la barra de abajo diga *plan*. Proyectos grandes o nuevos: una *skill* de planificación (ver Parte 5).
3. **Corrige a Claude en voz alta y guarda la corrección.** «Eso no está bien porque X. Ahora actualiza el CLAUDE.md para que no vuelva a pasar.» Ése ES el ciclo de automejora.
4. **Vigila la barra de contexto.** Al ~50%, compacta o cierra. Nunca dejes que llegue al límite a mitad de una tarea.
5. **Anota las lecciones.** Cada sorpresa, tropiezo o truco → una línea en `05 AI/CLAUDE CODE/resources/lessons.md`.
6. **Abre Claude Code todos los días, aunque sean 10 min.** En la Semana 1 el hábito importa más que el resultado.
7. **Confía en la cadena de `CLAUDE.md`.** Si Claude está confundido, casi siempre es porque falta o está mal un `CLAUDE.md`, no porque Claude esté roto.

### Qué Quedó Instalado en tu Máquina

El inventario completo, por si necesitas auditar, replicar o resolver problemas después.

**Archivos globales:**

| Ruta | Qué es | Edítalo cuando... |
|------|-----------|--------------|
| `~/.claude/CLAUDE.md` | Enrutador global + tu perfil | Tu *vault* cambia de lugar, cambia tu rol, quieres agregar reglas globales |
| `~/.claude/settings.json` | Permisos (una lista corta de comandos pre-aprobados de solo lectura, más reglas `ask` para imprimir archivos, hacer commit y publicar), hooks (sonido al terminar, avisos de contexto), auto-compactación al 75%, barra de estado | Quieres que Claude pregunte menos por un comando seguro concreto, o cambiar un hook |
| `~/.claude/statusline.sh` y `~/.claude/hooks/` | La barra de contexto y los avisos del 50% y de antes de compactar | Casi nunca |
| `~/.claude/skills/` | Tus *skills* iniciales (`/session-close`, `/project-create`, …) | Agregas o actualizas *skills* |

> **Los permisos son acotados a propósito.** La configuración nunca pre-aprueba comandos generales (todo `git`, Python, …) ni nada que escriba, borre o corra un script, así que Claude normalmente pregunta antes de hacerlo — salvo que ya hayas guardado una aprobación para ese comando ("Yes, and don't ask again"), uses un modo de permisos que se salta las preguntas, o corras el sandbox del 02-S en modo auto-allow, donde los comandos encerrados corren sin preguntar. Las catorce reglas `ask` son lo que siempre pregunta, cada vez, incluso por encima de una aprobación guardada: imprimir archivos con `cat`, `head`, `tail`, `grep`, `diff`, `sed`, `sort` o `git show`; `git add`, `git commit`, `git push` y cualquier forma `git -C …` / `git -c …`; y `gh repo create` — ésa es tu red de seguridad. Otros comandos de sólo lectura (por ejemplo `ls`, `find` o `git log -p`) siguen corriendo sin preguntar. Cuando agregues un permiso, agrega un comando concreto, nunca un comodín, y nunca saques una regla de `ask`. El archivo de ajustes puede guardar llaves: cámbialo tú en un editor de texto en vez de pedirle a Claude que lo imprima.

**Archivos creados en el *vault*:**

| Ruta | Qué es |
|------|-----------|
| `[vault]/CLAUDE.md` | Reglas del *vault* (PARA, idioma, seguridad) |
| `[vault]/Templates/Project Brief Template.md` | Plantilla reutilizable para proyectos nuevos |
| `[vault]/01 PROJECTS/[nombre del proyecto]/[nombre del proyecto].md` | El brief del proyecto de tu caso |
| `[vault]/01 PROJECTS/AI Acceleration/[tu nombre]/AI Acceleration Club - [tu nombre] Journey.md` | Sigue tu avance en el programa |
| `[vault]/02 AREAS/[área]/[área].md` | El mapa de tu área (MOC) |
| `[vault]/05 AI/CLAUDE CODE/resources/` | Carpeta de lecciones; `lessons.md` aparece con tu primera lección |
| `[vault]/00 HUB/00 INBOX/AIAC Cheat Sheet.md` | Tarjeta de referencia rápida |

**Archivos del repo** (en `~/dev/[nombre-de-tu-repo]/`, fuera del *vault*, subido a un repo **privado** de GitHub):

| Ruta | Qué es |
|------|-----------|
| `CLAUDE.md` | Reglas del proyecto + el puente de vuelta al brief de tu *vault* |
| `README.md` | La presentación del proyecto para personas |
| `.gitignore` | Deja los datos crudos y los secretos fuera de GitHub |
| `data/raw/` · `data/working/` · `data/processed/` | Zonas de datos: crudos y de trabajo **nunca** se suben; los resultados procesados sí |

**Plugins:** corre `claude plugin list` en la terminal para ver exactamente qué está instalado y activado (la Parte 6 explica los principales).

**Hooks:**

| Evento | Hook | Qué pasa |
|-------|------|--------------|
| `Stop` | Sonido | Aviso audible cuando Claude termina una tarea |
| `UserPromptSubmit` | Aviso de contexto | Un recordatorio de una sola vez cuando pasas el 50% |
| `PreCompact` | Apaga la compactación automática (el intento se salta y la conversación sigue) | Tú decides cuándo correr `/session-close` o `/compact` |

### Qué Hacer Cuando Algo se Siente Raro

- **Claude no sabe de mi proyecto** → el enrutador de `~/.claude/CLAUDE.md` puede estar roto. En una ventana nueva, desde `cd ~`, pregúntale qué hay en el INBOX de tu *vault*. Si no lo encuentra, pide ayuda.
- **Claude repite el mismo error** → la corrección no quedó guardada. Abre el `CLAUDE.md` que corresponde y revisa que la regla esté.
- **La sesión va lenta o Claude olvida cosas** → el contexto está lleno. `/session-close`, y después `/clear`.
- **No aparece el comando de una *skill* o de un plugin** → primero abre una ventana **nueva** (cargan en sesiones nuevas). Después corre `claude plugin list` en la terminal y revisa `~/.claude/skills/`. En una cuenta Team/Enterprise, un plugin que instalaste a mano con el mismo nombre que uno que da tu organización puede tapar la copia de la organización: quédate con la de la organización.
- **Sale un error en la terminal** → copia el error (revisa que no traiga una contraseña o un token), pégaselo a Claude y pregúntale *«¿qué es este error?»*.

---

## PARTE 0.6: MANTENER LOS PLUGINS AL DÍA

Los plugins vienen de **marketplaces** (catálogos). Para actualizar, en Claude Code:

1. `/plugin marketplace update` (refresca los catálogos)
2. `/plugin update <plugin>@<marketplace>` para el plugin que quieres actualizar
3. **Abre una sesión nueva** para que cargue la versión nueva.

Revisa el resultado con `claude plugin list` en la terminal. En una cuenta **Team o Enterprise**, los plugins que da tu organización los actualiza tu organización; puede que sólo necesites el paso 3.

---

## PARTE 0.7: OPCIONAL — MÁS PLUGINS

Tu paso de Skills & Config instaló los plugins centrales (Compound Engineering, Superpowers y Playground). Éstos valen la pena cuando los quieras. **Pega esto en Claude Code:**

```
Instala estos plugins del marketplace oficial (claude-plugins-official), uno por uno, preguntándome
antes de cada instalación. Si un plugin ya está instalado, sáltalo. Cuando termines, corre
claude plugin list y muéstrame el resultado. Si uno falla, dime cuál y el error.

- explanatory-output-style  (Claude explica su razonamiento mientras trabaja)
- commit-commands           (commits de git con buenos mensajes, con /commit)
- claude-md-management      (mantén sanos tus CLAUDE.md)
- context7                  (documentación al día de cualquier librería)
- code-review               (revisión de calidad del código)
```

Después **abre una sesión nueva** para que carguen.

<details><summary><b>Respaldo — córrelos tú en una terminal</b></summary>

Un plugin siempre es `<plugin>@<marketplace>`:

```bash
claude plugin marketplace add anthropics/claude-plugins-official   # only if not already configured
claude plugin install explanatory-output-style@claude-plugins-official
claude plugin install commit-commands@claude-plugins-official
claude plugin install claude-md-management@claude-plugins-official
claude plugin install context7@claude-plugins-official
claude plugin install code-review@claude-plugins-official
claude plugin list
```

`claude /install-plugin` y `claude plugins add` **no existen**. Si los ves en una guía vieja, ignóralos.
</details>

---

## PARTE 0.8: OPCIONAL — SÁCALE MÁS A OBSIDIAN

> **Opcional, no obligatorio.** La Fase 0 ya dejó los cuatro ajustes de Obsidian que cargan peso
> (notas nuevas → `00 HUB/00 INBOX`, wikilinks, mostrar todos los tipos de archivo, actualizar enlaces
> automáticamente). Todo lo de abajo es *amplificación*. Agrégalo cuando quieras la capacidad, no porque toque.

### Complementos de la comunidad que valen la pena

Todos se instalan igual: **Configuración → Complementos de la comunidad → Activar complementos de la
comunidad → Explorar → busca el nombre → Instalar → Habilitar**. Instala uno, pruébalo y
vuelve por el siguiente.

| Complemento | Para qué sirve | Cómo se configura |
|--------|----------------------|------------------|
| **Dataview** | Consultas en vivo sobre el frontmatter de tus notas: «todos mis proyectos activos» en una tabla. El de mayor impacto para un *vault* PARA. | Instálalo y habilítalo. Prueba en una nota: un bloque ```` ```dataview LIST FROM "" LIMIT 5 ``` ```` tiene que mostrar una lista de archivos. Activa las consultas JavaScript sólo si entiendes qué corren. |
| **Tasks** | Tareas de verdad sobre las casillas `- [ ]`: fechas, prioridades, recurrencia, y consultas como «lo que vence esta semana». | Instálalo y habilítalo. En su configuración activa «Set done date on every completed task». |
| **Templater** | Plantillas que se llenan solas (`{{title}}`, `{{date}}`). | Instálalo y habilítalo. En «Template folder location» pon `Templates/`. |
| **Calendar** + **Periodic Notes** | Notas diarias y semanales con plantilla, desde un calendario en la barra lateral. | Instala y habilita los dos; en Periodic Notes activa «Daily Notes» y fija su plantilla y su carpeta. |

### Ajustes más profundos (opcional)

- **Adjuntos en una sola carpeta.** Configuración → Archivos y enlaces → **Ubicación por defecto
  para nuevos adjuntos** → «En la carpeta especificada abajo» → por ejemplo `assets`.
- **Formato de enlace más corto.** Configuración → Archivos y enlaces → **Formato de nuevos enlaces** →
  «Ruta más corta cuando sea posible».

---

## PARTE 0.9: OPCIONAL — LA CLI gws PARA UNA INTEGRACIÓN MÁS PROFUNDA CON GOOGLE WORKSPACE

> **Opcional, sólo para Google, y no para la Semana 1.** Los conectores de claude.ai cubren casi todo lo que necesitas. Agrega la **CLI gws** más adelante sólo si tu proyecto necesita que Claude **escriba en Google Sheets** o maneje Google Workspace desde scripts. Sáltatela por completo si usas Microsoft 365. Si es una cuenta de Google **del trabajo**, pregúntale antes a tu IT o a tu facilitador.

Reglas básicas: inicia sesión con **sólo los permisos que necesitas** (por ejemplo Sheets, no todo), y **no agregues una regla de permisos que pre-apruebe todos los comandos `gws`**: deja que Claude pregunte cada vez. Calcula una hora y media de punta a punta.

```
Quiero instalar la CLI gws para que Claude Code pueda escribir en Google Sheets. Guíame paso a paso.
Pregúntame qué servicios de Google necesito de verdad y pide sólo esos permisos cuando inicie sesión.
No agregues ninguna regla de permisos que pre-apruebe comandos gws. Prueba un comando de lectura y después
agrega una nota corta «Google Workspace Tools» al CLAUDE.md de mi vault. Si algo falla, lo arreglamos juntos.
```

---

## PARTE 0.10: GENERA TU GUÍA DE USUARIO CONSOLIDADA

> **Hazlo una vez, después de la Parte 0.** Genera un único **`User Guide — [tu nombre].md`** en la raíz de tu *vault*: el mapa de *qué tienes y cómo encaja*. Complementa (no reemplaza) tu **AIAC Cheat Sheet**.

**Pega esto en Claude Code, en tu *vault*:**

```
Genera mi Guía de Usuario consolidada en `User Guide — [tu nombre].md`, en la raíz de mi
vault. Lee lo que REALMENTE está instalado y configurado en mi sistema — no adivines. Tres
secciones cortas y fáciles de navegar:

- Sección A — Mi vault: la estructura PARA, la cadena de CLAUDE.md (global → vault → repo)
  y dónde vive cada cosa (vault = conocimiento, ~/dev/ = repositorios de código).
- Sección B — Claude Code: los plugins y skills que tengo instalados (claude plugin list y
  ~/.claude/skills/), el monitor de contexto (la barra de 50/75%) y el Modo Plan. Para los
  comandos, apunta a mi AIAC Cheat Sheet en vez de copiarlo.
- Sección C — Los flujos de mi caso ([nombre de tu proyecto]): los 2 o 3 flujos concretos
  de mi proyecto y sus prompts de arranque.

Es un mapa, no un manual: mantenlo breve.
```

Vuelve a correrlo cada vez que tu sistema crezca.

---

## PARTE 1: DESPUÉS DE LA SESIÓN — HOY, ESTA SEMANA, CHEAT SHEET, AYUDA

> **Meta:** meter datos reales en el repo, armar tu primer análisis y arrancar el ciclo de automejora.

### 1. Hoy (3 mini-acciones)

- [ ] **Prueba el enrutador.** Abre una terminal nueva, `cd ~`, corre `claude` y pregúntale *«¿Qué archivos hay en el INBOX de mi vault?»*. Si responde sin que le des la ruta, el enrutador funciona. Si no → pide ayuda en [SET: your support channel].
- [ ] **Cierra a mano la sesión de configuración** con el APÉNDICE: PROMPT DE CIERRE MANUAL (Parte 0.3). El hábito de cerrar empieza hoy.
- [ ] **Escribe la intención de mañana** en `## Next Actions` del brief de tu caso, una línea: «Mañana quiero ___».

### 2. Esta Semana (5 cosas para probar, en orden)

Una rampa hacia el uso real. No te saltes pasos: cada uno se apoya en el anterior. (Tu versión de cada paso para tu proyecto vive en la PARTE 3, que llenas al final de la sesión de hoy.)

1. Pon el primer archivo de datos reales (o de muestra) en `data/raw/` de tu repo y pídele a Claude que lo inventaríe: qué tiene, qué le falta, qué preguntas podría responder.
2. Corre tu primer análisis real con un prompt de la PARTE 3.
3. Convierte ese análisis en un resultado guardado (un reporte, un script o una nota en el brief de tu proyecto) para que no quede sólo en el historial del chat.
4. Automatiza el paso manual más molesto de tu flujo: pídele a Claude que lo convierta en un script o una plantilla.
5. Corrige a Claude al menos una vez en voz alta, y después di «actualiza el CLAUDE.md para que esto no vuelva a pasar». Tu primera repetición del ciclo de automejora (PARTE 7).

> **¿Vas a usar datos reales del negocio?** Sólo cuando tu empresa haya aprobado usar Claude con ellos. Los datos crudos quedan en `data/raw/`, que nunca se sube a GitHub.

> **Para tu PRÓXIMO proyecto** (uno nuevo, no el caso de hoy): abre una ventana **nueva** de Claude Code en tu *vault* y corre `/project-create`. **No pidas otro Setup Prompt**: desde aquí el flujo es tuyo.

### 3. Cheat Sheet — Siempre en el Mismo Lugar

Tu cheat sheet vive exactamente en esta ruta:

```
00 HUB/00 INBOX/AIAC Cheat Sheet.md
```

Fíjalo en Obsidian. Lo creó el Main Setup Prompt; si no está, carga ese archivo de configuración por ruta y pide sólo el paso del cheat sheet. Tiene los comandos para arrancar una sesión, el prompt del enrutador, los comandos esenciales, los umbrales de contexto y las anclas de tus archivos.

**Agrégale dos cosas ahora.** Pega esto en Claude Code, en tu *vault*:

```
Agrega dos secciones cortas al final de 00 HUB/00 INBOX/AIAC Cheat Sheet.md, sin cambiar el resto:
1. «Varias sesiones a la vez — claude agents»: los puntos clave de la sección 4 de la PARTE 1 de mi Next Steps Brief.
2. «Pedir algo grande — el contrato de tarea»: la plantilla de cuatro líneas de la sección 5 de la PARTE 1.
Muéstrame el diff antes de guardar.
```

### 4. Varias Sesiones a la Vez — `claude agents`

Muchas veces vas a tener dos o más sesiones abiertas (una en el *vault*, otra en el repo). `claude agents` te las muestra todas y te deja saltar entre ellas:

- Escribe `claude agents` en la terminal: aparece la lista de tus sesiones.
- `↑` `↓` para elegir una; `→` para entrar.
- `←` vuelve a la lista, **sólo con el campo de texto vacío**. Si escribiste algo, bórralo primero.
- ¿No sabes en qué sesión estás? Vuelve con `←` y mira la lista. Para volver otro día: `claude agents`.

¿Prefieres algo más simple? Una pestaña de terminal (en Windows, una ventana de Git Bash) por sesión, con `claude` en cada una. Las dos formas sirven; lo importante es no mezclar el trabajo del *vault* y el del repo en la misma sesión.

### 5. Pedir Algo Grande — El Contrato de Tarea

Para cualquier cosa que pase de una pregunta rápida, dale a Claude un objetivo que pueda verificar. Copia y llena:

```
Objetivo: {qué quieres, en una frase}
Listo cuando: {cómo vamos a saber los dos que funcionó — un archivo que yo abra, un comando que pase, un número que cuadre}
Sólo toca: {los archivos que puede cambiar}
Pregúntame antes si: {va a enviar algo, borrar algo, gastar dinero o tocar datos reales}
```

Las palabras vagas valen *si* agregas: «traduce "profesional" a 3 criterios verificables y confírmalos conmigo antes de empezar».

### 6. ¿Te Trabaste? — Dónde Pedir Ayuda

La ayuda va **por niveles**. Empieza arriba y sube sólo si hace falta:

1. **Primero Claude (casi todo).** Pégale el error, prueba `/systematic-debugging`, revisa la cadena de `CLAUDE.md`. Casi todo se resuelve aquí.
2. **Tu canal de soporte: [SET: your support channel].** Para dudas del día a día, problemas de configuración o un rápido «¿esto es normal?». No te quedes trabado en silencio; una duda compartida se resuelve más rápido.
3. **Tu facilitador, para bloqueos de infraestructura.** Una instalación que falla, un problema para iniciar sesión, un conector que no conecta, una prueba del enrutador que no pasa: escribe de una vez. No quemes un día en plomería.

**Cuando pidas ayuda (en cualquier nivel):** incluye el prompt que usaste, el error exacto (sin contraseñas ni tokens) y lo que ya probaste. «No sirve» no es un mensaje de depuración.

### 7. Al Final de la Semana 1 — Cierra Bien

```
/session-close
```

---

## PARTE 2: SEMANA 2 — ARMA TUS HÁBITOS DIARIOS

### En la Mañana: Arranca el Día

En una ventana nueva, desde cualquier carpeta:

```
Trabajemos en mi proyecto [nombre del proyecto]. ¿Cuáles son mis Next Actions abiertas y qué es lo más importante para hoy?
Si hay un Continuation Prompt, resúmeme dónde me quedé.
```

### Durante el Trabajo: Usa el Modo Plan

Para cualquier tarea que no sea trivial:
- Presiona `Shift+Tab` hasta que la barra de abajo diga *plan*
- Describe lo que quieres
- Revisa el plan
- Apruébalo y ejecútalo

### Antes de Terminar: Cierra Siempre

```
/session-close
```

Actualiza el brief de tu proyecto, registra lo que hiciste y deja un prompt de continuación. **Es el hábito más importante de todos.**

### Cada Semana: Revisa tu Avance

```
Lee el brief de mi proyecto [nombre del proyecto].

Dame un reporte de avance de la semana:
1. ¿Qué hitos se completaron?
2. ¿Qué está en curso?
3. ¿Qué está bloqueado y por quién?
4. ¿En qué me enfoco la semana que viene?
5. ¿Vamos a tiempo con las fechas de los hitos?
```

---

## PARTE 3: LOS PRÓXIMOS FLUJOS DE TU PROYECTO

Tu caso no se escogió por adelantado: lo eligieron tú y tu facilitador en vivo. Por eso esta sección empieza en blanco a propósito. Llénala antes de irte (Bloque 5), mientras la sesión está fresca. Se convierte en tu versión personal de la rampa «Esta Semana» de la PARTE 1 y del mapa de progreso de la PARTE 8.

**Cómo se llena.** Pídeselo a Claude:

```
Con todo lo que armamos y conversamos hoy para [nombre de tu proyecto], ayúdame a redactar
3 a 5 flujos que de verdad voy a volver a correr — reportes, análisis o documentos recurrentes
propios de mi trabajo. Para cada uno, dame:
1. Un nombre corto
2. Cuándo lo usaría
3. Un prompt listo con rutas reales de archivos de mi repo

Guarda esta lista en las Next Actions del brief de mi proyecto, y escríbela también abajo para
tenerla en este brief.
```

### Flujo 1: _______________________________
```
[prompt listo — llénalo durante o después de la sesión de hoy]
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

> **¿Prefieres un plan día por día para la Semana 1 en vez de una lista de flujos?** Pídele a Claude: *«Ayúdame a convertir los flujos de arriba en un calendario día por día para la Semana 1.»*

---

## PARTE 4: PROMPTS GENERALES DE PRODUCTIVIDAD

### Investigar Cualquier Tema

```
/deep-research [tema]
```

### Crear un Proyecto Nuevo

En una ventana **nueva** de Claude Code en tu *vault*:

```
/project-create
```

### Tomar una Decisión

```
Tengo que tomar una decisión sobre: [DESCRIBE LA DECISIÓN]

Ayúdame a pensarlo con orden:
1. ¿Cuáles son las opciones? (al menos 3)
2. ¿Cuáles son los pros y los contras de cada una?
3. ¿Cuál es el riesgo si elijo mal?
4. ¿Qué información me falta?
5. ¿Qué recomiendas y por qué?

Guárdalo como memo de decisión en 00 HUB/00 INBOX/.
```

### Analizar una Hoja de Cálculo

En una sesión de repo (`cd ~/dev/[nombre-de-tu-repo]` y `claude`), con el archivo copiado en `data/raw/`:

```
Lee el archivo [NOMBRE] en data/raw/. No lo modifiques: trabaja sobre una copia. Dime:
1. ¿Qué tienen estos datos? (columnas, cantidad de filas, rango de fechas)
2. Estadísticas de las columnas numéricas
3. Patrones, tendencias o anomalías
4. 3 preguntas que estos datos podrían responder
5. ¿Qué otros datos tendría que cruzar con éstos para tener el panorama completo?
```

### Guardar tu Trabajo en GitHub

En una sesión de repo, al terminar:

```
Haz commit de mis cambios con un mensaje claro y súbelos a GitHub (push). Antes, muéstrame qué
archivos van, confirma que el repositorio sigue siendo privado y que nada de data/raw/ ni
data/working/ se sube.
```

### Crear una Skill Propia

```
/skill-create

Hago una y otra vez [DESCRIBE LA TAREA REPETIDA].
Ayúdame a crear una skill que la automatice.
```

---

## PARTE 5: LAS SKILLS QUE YA TIENES — Y QUÉ CONSTRUIR DESPUÉS

> Para ver todo lo que tienes: escribe `/` en Claude Code y recorre la lista. Los nombres pueden variar un poco entre versiones de los plugins.

### Skills iniciales (instaladas en tu paso de Skills & Config)

Vienen del repositorio público **[AI-Acceleration/cc-starter-pack](https://github.com/AI-Acceleration/cc-starter-pack)**, fijado en la versión **`v1.0.1`** para que todos reciban la misma versión revisada.

| Skill | Qué hace | Cómo se usa |
|-------|-------------|-----------|
| **session-close** | Cierra bien una sesión: actualiza el brief, registra el trabajo y escribe el prompt de continuación | `/session-close` |
| **project-create** | Crea un brief de proyecto con preguntas guiadas | `/project-create` |
| **inbox-clear** | Ordena tu INBOX con el árbol de decisión de GTD; actúa sólo con tu aprobación | `/inbox-clear` |
| **retro** | Una retrospectiva: qué funcionó, qué no y qué cambiar | `/retro` |
| **skill-create** | Crea tus propias *skills* con una conversación guiada | `/skill-create` |
| **deep-research** | Investigación en varias fases: barrido amplio → profundización → síntesis, con fuentes | `/deep-research [tema]` |
| **deep-planning** | Planificación (lluvia de ideas → plan) antes de construir | `/deep-planning` |
| **fermi-decomposition** | Descompone números «imposibles de medir» en factores estimables | `/fermi-decomposition` |
| **load-context** | Una estimación de cuánto contexto llevas usado y un resumen de los temas de la sesión (para la cifra exacta, usa el comando integrado `/context`) | `/load-context` |

Además **`/meeting-minutes`**, configurada para tu herramienta de transcripción (o para transcripciones pegadas).

**Reinstalar o actualizar las *skills* iniciales.** Pídeselo a Claude, fijado al commit revisado de `v1.0.1` (es el mismo bloque del paso de Skills y Configuración). Si tu terminal corta lo que pegas, guarda este documento y dile a Claude: `Lee el archivo <ruta>, busca "Reinstalar o actualizar las skills iniciales" y sigue ese prompt.`

```
Reinstala mis skills iniciales desde AI-Acceleration/cc-starter-pack v1.0.1. Dime qué hace el comando de abajo
y, cuando te apruebe, córrelo exactamente como está, como un solo comando, y muéstrame su salida. Clona en una
carpeta temporal nueva y corre install.sh solo si la clonación salió bien y está en el commit revisado.
Cualquier línea STOP significa que no se instaló nada: muéstramela y no intentes saltártela. Si install.sh
imprime líneas SKIP, muéstrame la lista y pregúntame qué hacer. Si imprime líneas NOTE sobre skills que
quedaron de una versión anterior del paquete, muéstramelas y deja esas carpetas donde están salvo que yo
te diga otra cosa. Nunca corras install.sh desde otra carpeta.

PACK_TMP="$(mktemp -d)" || PACK_TMP=""
if [ -z "$PACK_TMP" ]; then
  echo "STOP: could not create a temporary folder - not installed"
elif ! git clone --depth 1 --branch v1.0.1 https://github.com/AI-Acceleration/cc-starter-pack.git "$PACK_TMP/cc-starter-pack"; then
  echo "STOP: the clone failed - not installed"
elif [ "$(cd "$PACK_TMP/cc-starter-pack" && git rev-parse HEAD)" != "a85d906849f1fbd200d0e44a59b0d1f24b450135" ]; then
  echo "STOP: v1.0.1 is not the reviewed commit a85d906 - not installed"
else
  (cd "$PACK_TMP/cc-starter-pack" && bash ./install.sh)
fi
[ -n "$PACK_TMP" ] && rm -rf "$PACK_TMP"
```

Después abre una sesión **nueva**. Usa una versión más nueva sólo cuando tu facilitador la anuncie — viene con su propio commit revisado.

### Skills de los plugins

| Skill | Qué hace |
|-------|-------------|
| Las *skills* de planificación de **Compound Engineering** (por ejemplo `/ce-plan`, `/ce-work`, `/ce-brainstorm`; las versiones viejas usan `/ce:plan`) | Planificar con investigación previa y ejecutar paso a paso |
| **Superpowers** (por ejemplo `/systematic-debugging`, `/verification-before-completion`, `/brainstorming`) | Depuración, lluvia de ideas y verificación con orden |

### Ideas para construir después (no vienen instaladas — constrúyelas con `/skill-create`)

Son patrones que funcionan bien cuando tienes la base firme. Ninguno viene instalado con el kit; cuando uno te ahorre tiempo, arma tu propia versión con `/skill-create`:

| Idea | Qué haría |
|------|------------------|
| **weekly-review** | Revisión semanal GTD: recorrer tus proyectos, vaciar el INBOX, planificar la semana |
| **startup-day** / **close-day** | Un plan de la mañana con tus tareas y tu calendario; un cierre del día |
| **meeting-agenda** | Armar una agenda con el calendario, tus notas y las minutas anteriores |
| **decision-memo** | Un documento de decisión estructurado: contexto, alternativas, recomendación |
| **followup** | Buscar en tus briefs lo que está en «Waiting For» y redactar seguimientos (tú apruebas cada envío) |

---

## PARTE 6: REFERENCIA DE PLUGINS

**Lo que tienes:** corre `claude plugin list` en la terminal. Tu paso de Skills & Config instaló **Compound Engineering**, **Superpowers** y **Playground**; la Parte 0.7 agrega más.

| Plugin | Qué hace |
|--------|-------------|
| **Compound Engineering** | Flujo de desarrollo que planifica primero, con agentes de investigación |
| **Superpowers** | Flujos con orden para depurar, hacer lluvia de ideas, TDD y verificar |
| **Playground** | Visualizaciones HTML interactivas |
| **Explanatory Output Style** | Claude explica su razonamiento mientras trabaja |
| **Commit Commands** | Commits de git con buenos mensajes |
| **Claude MD Management** | Auditar y mejorar los `CLAUDE.md` |
| **Context7** | Documentación al día de las librerías cuando las mencionas |
| **Code Review** | Revisar el código buscando errores, seguridad y calidad |

### Plugins Opcionales (para Después)

| Plugin | Qué hace | Cuándo instalarlo |
|--------|-------------|----------------|
| **Feature Dev** | Desarrollo guiado de funcionalidades con análisis del código | Cuando construyas funcionalidades más grandes |
| **PR Review Toolkit** | Revisión completa de pull requests | Cuando hagas revisiones de código |
| **Frontend Design** | Generación de interfaces de alta calidad | Cuando construyas interfaces o tableros |
| **Playwright** | Automatización del navegador para pruebas | Cuando pruebes aplicaciones web |
| **Hookify** | Crear hooks que impidan comportamientos no deseados | Cuando quieras automatizar reglas |

---

## PARTE 7: EL CICLO DE AUTOMEJORA

Éste es el concepto más importante. Es lo que separa a quien usa Claude Code de forma productiva de todos los demás.

### El Ciclo

```
1. Trabajas con Claude Code
2. Claude se equivoca -> lo corriges
3. Le dices a Claude: "Actualiza el CLAUDE.md para que esto no vuelva a pasar"
4. La próxima sesión lee el CLAUDE.md actualizado
5. El error no se repite
6. Repites durante semanas -> el CLAUDE.md acumula inteligencia
7. Al mes, Claude de verdad trabaja mejor para TI
```

### Prompt para Arrancar el Ciclo

Cada vez que Claude haga algo mal:

```
Eso no está bien. [Explica qué estuvo mal y cuál es la forma correcta.]
Ahora actualiza el CLAUDE.md para agregar una regla que evite este error en el futuro.
```

### Tus Correcciones

Las correcciones salen de errores reales que Claude comete en **tu** proyecto. Éste es el patrón, más espacio para anotar las tuyas a medida que pasen esta semana:

**Patrón:**
> «[Lo que Claude hizo mal] no está bien — [por qué, y cuál es la forma correcta]. Agrega esta regla al CLAUDE.md para que no vuelva a pasar.»

**Anota las tuyas aquí a medida que pasen:**

1. Corrección — ___________________________:
   > «...»

2. Corrección — ___________________________:
   > «...»

3. Corrección — ___________________________:
   > «...»

---

## PARTE 8: MAPA DE PROGRESO

### Semana 1: Configuración + Primer Uso Real
- [ ] Parte 0 hecha (configuración revisada, sesión de configuración cerrada a mano)
- [ ] Datos reales o de muestra del proyecto en `data/raw/` de tu repo
- [ ] Primer análisis corrido y guardado (no sólo en el chat)
- [ ] Al menos 3 sesiones de Claude Code completadas
- [ ] `/session-close` corrido al final de cada sesión
- [ ] Primer flujo de la PARTE 3 probado de punta a punta

### Semana 2: Hábitos Diarios
- [ ] Revisión diaria de la mañana con el brief de tu proyecto
- [ ] Modo Plan usado al menos dos veces
- [ ] Primer resultado automatizado o repetible (un reporte, un script o una plantilla)
- [ ] Al menos 2 correcciones agregadas a tu `CLAUDE.md` (PARTE 7)
- [ ] Una *skill* `weekly-review` **construida** con `/skill-create` (no viene instalada con el kit; ver Parte 5) y corrida una vez

### Semana 3: Flujos Operativos
- [ ] 2 o 3 de tus flujos de la PARTE 3 probados y afinados
- [ ] Una *skill* propia creada para un flujo que repetiste 3 veces o más (`/skill-create`)
- [ ] Cambios subidos a tu repo privado de GitHub al menos dos veces
- [ ] Los plugins opcionales de la Parte 0.7 instalados, si los quieres

### Semana 4: Autonomía
- [ ] Tu flujo principal corre con un solo prompt listo, sin rehacer nada
- [ ] El `CLAUDE.md` tiene 5 o más reglas acumuladas del ciclo de automejora
- [ ] Usas Claude Code más de 30 minutos reales al día
- [ ] Listo para un segundo proyecto (`/project-create`)

### Mes 2: Expansión
- [ ] Un segundo proyecto arrancado con `/project-create`
- [ ] Al menos un flujo totalmente automatizado de punta a punta

### Mes 3: Dominio
- [ ] Claude Code es parte normal de tu trabajo diario, no una novedad
- [ ] Creaste 2 o más *skills* propias
- [ ] Corriges a Claude y actualizas el `CLAUDE.md` sin que nadie te lo recuerde

---

## ANEXO: TARJETA DE REFERENCIA RÁPIDA

### Empezar a Trabajar

> **Dos lugares, una regla.** El **conocimiento** (notas, briefs, gestión de proyectos) vive en tu *vault*. El **código** vive en `~/dev/[nombre-de-tu-repo]`, **fuera** del *vault*. La prueba es mecánica: si tiene su propio `.git/`, va en `~/dev/`.

```bash
cd "[ruta del vault]" && claude          # notes, projects, thinking
cd ~/dev/[nombre-de-tu-repo] && claude   # code and data
```

En Windows (Git Bash), córrelos en dos líneas (`cd …`, y después `claude`). En el Explorador de archivos, la carpeta del repo es `C:\Users\YOUR-USER\dev\[nombre-de-tu-repo]`.

O, desde cualquier carpeta en una ventana nueva: *«Trabajemos en mi proyecto [nombre del proyecto].»*

### El Flujo de una Sesión
```
1. Arranque: Claude lee los CLAUDE.md solo
2. Retome: "Trabajemos en mi proyecto [nombre del proyecto]. ¿Dónde me quedé?"
3. Plan: Shift+Tab hasta que la barra diga plan -> describe la tarea -> revisa el plan -> apruébalo
4. Trabajo: ejecuta el plan
5. Cierre: /session-close
```

### Varias Sesiones
```
claude agents        (↑ ↓ elegir · → entrar · ← volver a la lista, con el campo de texto vacío)
```

### Pedir Algo Grande
```
Objetivo: … · Listo cuando: … · Sólo toca: … · Pregúntame antes si: …
```

### Cuando te Trabes
```
/systematic-debugging

Estoy trabado en: [describe el problema]
Lo que ya probé: [lo que intentaste]
Lo que esperaba: [lo que debió pasar]
```

### Cuando Necesites Investigar
```
/deep-research [tema]
```

### Al Terminar
```
/session-close
```

---

## APÉNDICE: PROMPT DE CIERRE MANUAL

> **Cuándo se usa:** en la sesión donde corriste la configuración. `/session-close` se instaló en esa MISMA sesión, y las *skills* sólo cargan en sesiones abiertas DESPUÉS de instalarlas, así que esa sesión se cierra a mano. Desde tu próxima sesión, `/session-close` funciona normal. Pega esto **en esa misma sesión**:

```
Cierra esta sesión a mano. No invoques /session-close: está instalada, pero en esta sesión
todavía no carga. Haz los cambios directamente:
1. Al principio de la sección ## Next Actions del brief del proyecto de mi caso, agrega o reemplaza
   el bloque ### Continuation Prompt con:
   - La fecha de hoy
   - Modo: Gestión del vault
   - Resumen del contexto: lo que hicimos en esta sesión de Fase 0 (estructura del vault, brief
     del proyecto creado, repo privado subido a GitHub, skills instaladas, prueba del enrutador pasada)
   - Por dónde sigo: la Parte 0 de mi Next Steps Brief, y después la tarea de la Semana 1
   - Los archivos que tocamos en esta sesión
2. Agrega una entrada al Log: «Sesión de Fase 0 completada — vault armado, brief del caso creado,
   repo privado subido a GitHub, skills instaladas, enrutador validado.»
3. Muéstrame el bloque y la entrada del Log antes de guardar.
```

---

## ÚLTIMO PASO — GUARDA ESTE BRIEF DONDE LO ENCUENTRES

> **Hazlo apenas recibas este documento**, frente a tu facilitador si es una sesión en vivo.

1. Guarda este documento en tu *vault* como `00 HUB/00 INBOX/Next Steps Brief.md`, y el Doc 06 al lado. Si están en tu carpeta de Descargas, pídele a Claude que los mueva ahí.
2. En Obsidian, abre `00 HUB/00 INBOX/` y confirma que ves `Next Steps Brief.md`, el Doc 06 y `AIAC Cheat Sheet.md` en la misma carpeta.
3. Fija el brief y el cheat sheet.

Si el cheat sheet no está, regenéralo con el paso del cheat sheet de tu Main Setup Prompt (carga el archivo por ruta y pide sólo ese paso).

**Por qué importa:** es fácil irse de una sesión con la hoja de ruta flotando en una ventana de chat, en Descargas o en un correo, y perderle la pista en 48 horas. El INBOX es la única carpeta que siempre sabes encontrar.

---

> *Parte del programa de Fase 0 del AI Acceleration Club. Esta hoja de ruta destila patrones refinados durante meses de uso diario de Claude Code en una rampa paso a paso para tu primer mes.*
