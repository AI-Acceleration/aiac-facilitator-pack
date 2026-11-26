---
title: "Manual del Facilitador — Cómo dictar una sesión de Fase 0"
created: 2026-07-14
category: reference
tags: [aiac, phase0, co-facilitator, facilitator-manual, spanish]
lang: es
translated_from: "05 — Facilitator Manual — How to Run a Phase 0 Session.md"
---

# Manual del Facilitador — Cómo dictar una sesión de Fase 0

> **Esta es la pieza central del Kit de Co-Facilitación AIAC Fase 0.** Está escrito para **ti, el facilitador**, la persona que dicta la sesión, no para el participante. Léelo de principio a fin antes de tu primera sesión, y después mantenlo abierto a tu lado (segundo monitor, segunda pestaña o impreso) mientras dictas una. Es tu partitura de director.

## Qué es este kit

Este kit empaqueta el onboarding de **Fase 0** del AI Acceleration Club para que puedas dictarlo con cualquier persona, **uno-a-uno**: una sesión en vivo y práctica en la que el participante sale con un segundo cerebro funcionando, un repositorio de código real y privado, su primer proyecto y una configuración de Claude Code que amarra todo.

**Cuánto toma de verdad.** Unos **90 minutos es el mejor caso**: una sesión uno-a-uno con los prerrequisitos y el pre-vuelo hechos, un facilitador que ya la dictó antes y un participante cómodo con la terminal. **Para tus primeras sesiones, calcula 2 a 3 horas.** Los grupos necesitan más: para un grupo chico, planifica al menos 3 horas, con un ayudante por cada dos o tres participantes.

Dos cosas hacen distinto a este kit del pipeline interno del que se deriva:

- **Sólo documentos.** No hay plugin que instalar ni nada que pre-generar. Tú conduces la sesión; el participante le da a Claude Code prompts en Markdown plano. Los prompts largos se **cargan por archivo** («Lee el archivo <ruta> y sigue sus instrucciones»), nunca se pegan, porque las terminales (sobre todo en Windows) pueden recortar en silencio lo que se pega si es largo.
- **Autoconfiguración en vivo.** El participante **no** llena un formulario de admisión y **no** recibe archivos preconstruidos para su caso. Durante la sesión, Claude lo entrevista sobre su trabajo, lo ayuda a escoger su primer proyecto real y genera sus archivos de proyecto en el acto. El participante también crea **su propio** repositorio **privado** en GitHub, bajo **su propia** cuenta. No hay repositorio central ni invitación de colaborador que perseguir.

> **Independiente del modelo, por diseño.** El método son archivos Markdown planos, Git y herramientas estándar de línea de comandos. Claude Code es la herramienta recomendada hoy, pero el vault, los briefs y los hábitos se llevan a otra herramienta de IA si algún día cambias.

### Los cinco documentos centrales, más variantes

| Doc | Para quién | Cuándo se usa |
|---|---|---|
| **01 — Pre-Session Setup Instructions** | Participante | Se envía una semana antes. Instala los prerrequisitos, corre el **pre-vuelo** y te manda su resultado de una línea. |
| **02 — Main Setup Prompt** | Participante | Se carga por archivo en Claude Code en el **Bloque 2**. Arma la estructura del *vault*, el repositorio privado y, con una entrevista en vivo, su primer caso. |
| **03 — Skills & Config Setup Prompt** | Participante | Se carga por archivo en el **Bloque 3**. Instala el enrutador global, los plugins y las *skills* núcleo. |
| **04 — Next Steps Brief** | Participante | Se entrega en el **Bloque 5**. Su hoja de ruta para las semanas siguientes. |
| **05 — Facilitator Manual** (este doc) | Tú | Tu guion de la sesión completa. |

**Variantes y acompañantes:**

| Archivo | Qué es |
|---|---|
| **02W / 03W** | Ediciones para Windows de 02 y 03. Mándalas en lugar de 02/03 a quien usa Windows. |
| **02-S** | Configuración opcional de sandbox, para quien quiere a Claude encerrado en su *vault* (Mac/Linux). |
| **06 — Kit de Supervivencia del Plan Pro** | Cómo hacer que Claude Pro rinda. Se entrega con el Doc 04. |
| **07 — Vocabulario** | Todos los términos en una página. Se envía con el Doc 01. |
| **00W / 00E / 00V** | Tablas de diferencias sólo para el facilitador (edición Windows, edición en español, voseo argentino). Nunca se las mandes a un participante. |
| **`tools/aiac-status-check.sh`** (+ su gemelo `.sh.txt`) | Un diagnóstico de sólo lectura que corre el participante; comparte sólo su bloque seguro para compartir. |

Los Docs 02 y 03 **son** los prompts. Presérvalos exactamente: un comando o un bloque JSON cambiado rompe el entorno del participante. **Nunca los adaptes a mano para un participante sin un diff paso por paso contra el original** (ver Pre-Sesión § 1).

### Primero la terminal, no la app de escritorio

Haz la configuración en una **terminal**. La pestaña Code de Claude Desktop lee la misma carpeta `~/.claude` (las mismas *skills*, la misma configuración y los mismos `CLAUDE.md`), así que el participante puede trabajar ahí después. Pero `claude plugin …` y `claude mcp add …` necesitan la terminal, y los prompts de configuración asumen una.

---

## FILOSOFÍA — léela antes de tu primera sesión

### Qué logra la Fase 0

Al final de una sesión de Fase 0 el participante tiene, y ha *probado*, cuatro cosas funcionando juntas:

1. **Un segundo cerebro:** un *vault* de Obsidian con estructura PARA (Proyectos / Áreas / Recursos / Archivo).
2. **Un repositorio real:** un repo de Git en `~/dev`, subido a un repositorio **privado** de GitHub bajo su propia cuenta, para su primer caso.
3. **Su primer caso:** un problema de trabajo real, escogido en vivo, con un brief de proyecto y un `CLAUDE.md` de proyecto que le da a Claude el contexto del dominio.
4. **El enrutador:** un `~/.claude/CLAUDE.md` global que le indica a Claude dónde está su *vault* desde *cualquier* carpeta, para que nunca tenga que explicar dónde vive cada cosa.

Ése es todo el entregable: no un trabajo terminado, sino un *sistema funcionando que el participante puede retomar mañana.*

### «Arrancar, no terminar»

Éste es el principio más importante para el ritmo de la sesión, y el que más rompen los facilitadores nuevos.

**El Bloque 4 arranca el primer ejercicio. No lo termina.** El trabajo de la sesión es dejar al participante *andando* con su problema real en Claude Code, no producir un entregable pulido en vivo. Completar el primer flujo es **tarea de la Semana 1** (Doc 04).

Por qué contenerse:

- Terminar en vivo alarga todavía más la sesión, agota la atención del participante y se come su límite de uso de Claude (en Pro esto importa, ver Doc 06).
- Le quita el momento de «esto lo hice yo» de la Semana 1, que construye autonomía y es el punto de todo el programa.

Así que cuando el primer ejercicio empiece a producir resultados, tu instinto va a ser seguir hasta que esté «listo». Resístelo. Produce un resultado parcial, deja una miga clara de por dónde seguir y pasa al siguiente bloque. Dilo en voz alta para que el participante no se confunda: *«Esto no lo terminamos ahora. Ésa es la tarea, y es la parte buena.»*

### El demo entre pares

Tu demo de apertura (Bloque 1) no es un pitch de producto. Eres tú mostrando **tu propio** sistema haciendo algo real, idealmente algo que refleje el mundo del participante. El mensaje es *«ésta es una forma normal de trabajar para alguien como tú»*, no *«mira lo que hace la herramienta»*. Mantenlo entre pares: archivos reales, correcciones reales, un cierre real. Tres o cuatro minutos bastan.

---

## PRE-SESIÓN

Haz esto en la semana previa a la sesión.

### 1. Ensayo en seco del material (antes de tu primera sesión y después de cada actualización del kit)

Corre tú mismo los Docs 01 → 02 → 03, de principio a fin, en una **máquina limpia o una cuenta de usuario nueva**, exactamente como lo haría un participante. Las herramientas cambian; un prompt que funcionaba el mes pasado puede romperse con una versión nueva de Claude Code. Es en el ensayo donde te enteras, no el participante.

**Nunca adaptes los prompts a mano sin un diff paso por paso.** Si ajustas el Doc 02 o el 03 para un participante o una cohorte, compara tu versión contra el original **paso por paso** y asegúrate de que cada paso siga ahí, o lleve una línea explícita «retirado a propósito porque …». En una cohorte, un prompt de configuración adaptado a mano perdió en silencio tres pasos (la plantilla de brief de proyecto, el mapa del área y parte de la estructura del brief). Nadie lo notó en la preparación porque el chequeo comparaba los *nombres* de los documentos, no su contenido. La sesión se alargó una hora.

### 2. Lista de chequeo pre-sesión

- [ ] **Marcadores llenos.** `[SET: your support channel]` aparece en el **Doc 01** y en el **Doc 04**. Reemplázalo por el canal que tus participantes usan para escribirte (un número de WhatsApp, un correo, un canal de Slack). `[TOOL]` aparece en el **Doc 03 / 03W**: reemplázalo por la herramienta de transcripción del participante (`Granola`, otra herramienta, o `none / pasted transcript`). Son los únicos valores que llenas; todo lo demás lo genera el participante en vivo.
- [ ] **Ediciones correctas.** Participante con Windows → **02W / 03W**. Participante argentino → aplica la tabla de voseo `00V` a los documentos del participante.
- [ ] **Compartir pantalla probado** en la herramienta de llamadas que vas a usar.
- [ ] **Ubicación revisada.** El participante va a estar en un [país o región admitidos](https://www.anthropic.com/legal/supported-regions) durante la sesión (depende de dónde esté físicamente). Si no, elige otra fecha; no planees una forma de saltarte la restricción.
- [ ] **Fecha límite fijada** para el pre-vuelo (ver § 4).
- [ ] **Proyecto concreto confirmado** (ver § 6).
- [ ] **Grabación decidida:** opcional, y sólo con consentimiento (ver § 8).

### 3. Manda el material una semana antes

Manda juntos, más o menos una semana antes de la sesión:

- **Doc 01** — Pre-Session Setup Instructions
- **Doc 02 y Doc 03** (Windows: **02W y 03W**). El participante los necesita en su disco: el pre-vuelo los mueve al *vault* y practica cargar uno por archivo.
- **Doc 07** — Vocabulario
- Opcional: `tools/aiac-status-check.sh.txt` (el gemelo `.txt`, porque las apps de chat y el correo bloquean `.sh`).

Dile que guarde todo en **Descargas** sin cambiarle el nombre. El Doc 01 es autoservicio: cada prerrequisito trae un prompt listo para claude.ai, y un chequeo «Verifica con Claude» una vez instalado Claude Code.

### 4. La compuerta del pre-vuelo, con fecha límite

El Doc 01 termina con un **pre-vuelo obligatorio**: un prompt que el participante carga por archivo en Claude Code. Crea el *vault* (nunca en una carpeta sincronizada con la nube), le pide abrirlo en Obsidian con **Abrir carpeta como bóveda**, comprueba que Obsidian abrió esa misma carpeta, mueve los archivos del kit a `00 HUB/00 INBOX/`, practica **Copiar ruta** → cargar por archivo, comprueba cada herramienta y su sesión de GitHub, y termina con exactamente una línea (en inglés a propósito, igual en los dos idiomas del kit):

```
PREFLIGHT: READY · ACCOUNT: personal
PREFLIGHT: MISSING jq, gh login · ACCOUNT: team
```

Pide esa línea **y su usuario de GitHub** para una **fecha límite**, por ejemplo tres días hábiles antes de la sesión, y di la fecha explícitamente cuando mandes los documentos. Usa la misma fecha para que la **máquina esté lista**: una máquina vieja, lenta o bloqueada que se descubre el mismo día le cuesta la sesión.

- **El silencio es «no está hecho».** En la práctica, los autorreportes no llegaron solos. Vuelve a pedirlo 24 horas antes de la fecha límite.
- **`MISSING …`** → se arregla antes de la sesión, por mensaje o en una llamada corta.
- **Sin línea para la fecha límite** → agenda una llamada de preparación (§ 5) o reprograma. No arranques una sesión a ciegas.
- **`ACCOUNT: team`** → una cuenta Team/Enterprise. El administrador de la organización controla qué conectores de claude.ai existen y puede repartir plugins. El Doc 03 lo maneja (primero los plugins de la organización, la instalación manual sólo como respaldo), pero sábelo antes de empezar.

«Me dijo que está listo» es un reporte, no un estado. Una sesión arrancó a ciegas; otra se agendó con «todo está instalado» y después se trabó dos veces, con una semana de diferencia, por una entrada de PATH que faltaba. La línea del pre-vuelo existe para reemplazar el reporte por un chequeo.

### 5. Preparación con un ayudante

Para participantes no técnicos, y en cualquier grupo, **empareja a cada participante con un ayudante antes de la sesión**: tú en una llamada de 20 a 30 minutos, o un colega o un participante anterior que haga de mentor. Juntos recorren el Doc 01 y el pre-vuelo. Así las instalaciones y los inicios de sesión (la parte más frágil) pasan con calma y no en vivo, y la línea del pre-vuelo llega porque había alguien ahí para mandarla.

### 6. Un proyecto concreto y ejecutable (obligatorio)

El participante tiene que llegar con **un proyecto concreto**: una entrada que pueda traer (un archivo, una exportación), una salida que quiera (un reporte, un resumen, una tabla limpia) y una razón por la que importa. «Aprender IA» o «ser más productivo» no es un proyecto. Si lo que recibes es vago, acótalo con él por mensaje antes de la sesión. La entrevista del Bloque 2 llega de «¿a qué te dedicas?» a un caso utilizable mucho más rápido cuando el candidato ya existe.

**Datos de muestra para el primer ejercicio.** Pídele que traiga una copia sin nombres ni montos, un pedacito, o filas inventadas. Los datos reales del negocio vienen después, cuando su empresa haya aprobado usar Claude con ellos, y nunca entran a Git: el repo deja `data/raw/` y `data/working/` fuera del historial.

### 7. El chequeo de estado (respaldo, no la compuerta)

`tools/aiac-status-check.sh` es un script de sólo lectura (no instala, no cambia y no envía nada) que reporta hasta dónde llegó una configuración. Úsalo cuando una línea de pre-vuelo no esté clara o un participante se trabe entre sesiones.

- Dile que corra **el nombre exacto del archivo que recibió**, por ejemplo `bash ~/Downloads/aiac-status-check.sh.txt`. Si Claude se lo corre, corre `bash ~/Downloads/aiac-status-check.sh.txt --share` (el Doc 01 trae el prompt): `--share` imprime sólo el bloque seguro para compartir, así que el detalle nunca entra al contexto de Claude. El reporte completo lo corre el participante en su propia terminal.
- Pídele que comparta **sólo** el bloque entre `----- AIAC STATUS (safe to share) -----` y `----- END -----`. Trae nombres de chequeos, `DONE` / `NOT DONE` / `SKIPPED (optional)`, el sistema operativo y un veredicto general. El script imprime en inglés a propósito. **Nunca pidas los detalles de arriba**, ni la salida de `--details`: esa parte es sólo para los ojos del participante.
- El primer `NOT DONE` es el punto de retome. `SKIPPED (optional)` no es tarea pendiente. Antes de la sesión, una configuración completa dice `VERDICT: PRE-SESSION - homework complete, ready for the session`; después, `VERDICT: PHASE 0 SETUP COMPLETE - …`. El script sólo reporta lo que puede ver en la máquina — por ejemplo `GitHub CLI credentials present`, `Obsidian config found in this folder`, `repo origin points at GitHub` — y su lista `NOT CHECKED HERE` nombra lo que no puede probar: que las credenciales de `gh` sigan funcionando (`gh auth status`), que Obsidian tenga abierta esta carpeta exacta, y que el repo exista en GitHub, sea Private y tenga el commit. Eso lo verificas tú: la carpeta en su pantalla compartida, y el repo del lado del servidor (Compuerta 6).
- Si el participante ya montó el sandbox del 02-S, lo corre en una terminal normal y no dentro de Claude Code: los comandos encerrados sólo pueden leer el vault, `~/.claude` (menos su archivo de inicio de sesión) y el único repo que nombra el 02-S, así que el script en `~/Downloads` y varios de los archivos que revisa (el inicio de sesión de `gh`, las apps instaladas) quedan fuera de su alcance.

### 8. Grabación: opcional, con consentimiento

Grabar la sesión es **opcional**. Si quieres grabar, pregúntale primero al participante y acepta un no. Usa lo que le resulte cómodo: Granola, cualquier otra herramienta de transcripción, o nada (puedes escribir un resumen corto después, o él puede pegarle una transcripción a Claude más tarde). Si grabas, **di los resultados en voz alta** (por ejemplo «prueba del enrutador: PASÓ»), porque la grabación sólo sirve si el resultado está en ella.

### 9. Participantes que quieren el sandbox (02-S)

Si el participante pide que Claude sólo toque la carpeta que él le dé, mándale también **`02-S — Sandbox Setup`**, para correr después del pre-vuelo y *antes* del Doc 02. Más o menos uno de cada diez lo pide sin que se lo ofrezcas, y es la objeción que de otro modo bloquea a cualquiera con una máquina del empleador. Antes de aceptar:

- El **bloque de permisos del PASO 3 del Doc 02 se salta**: el 02-S lo reemplaza a propósito.
- Lee con el participante lo que el propio 02-S dice del límite: el sandbox encierra los comandos de terminal de Claude, pero no es un muro para todo (el 02-S lista lo que queda afuera). No prometas más de lo que dice.
- **Puede que Claude no pueda correr `git` ni `gh`** dentro del sandbox. Esos los corre el participante, y el commit se convierte en su acto de aprobación. Dilo de entrada para que no parezca una falla a mitad de sesión. Si `gh` falla, usa el camino por navegador del § 10 (sin tokens).
- Sólo Mac y Linux. Windows nativo no tiene sandbox (hace falta WSL2).

### 10. Acceso a GitHub (la versión de este kit)

El participante crea **su propio** repo **privado** bajo **su propia** cuenta de GitHub, en vivo, en el Bloque 2. No hay invitación de colaborador ni repo central. Lo que necesitas antes de la sesión:

> **Claude Code funcionando + una cuenta de GitHub + `gh` con sesión iniciada (inicio de sesión por navegador).**

La línea del pre-vuelo ya lo confirma (si no, aparece `gh login` como falta). Antes del **primer push**, el Doc 02 hace que Claude se detenga y confirme tres cosas con el participante: el **dueño** (su cuenta), la visibilidad (**Private**) y la **lista de archivos** que se van a subir. Asegúrate de que ese chequeo ocurra; que nadie lo pase de largo.

**Si `gh` no se puede instalar** (una laptop de empresa bloqueada): el participante crea el repositorio en el navegador en `github.com/new`, con **su cuenta como dueña, visibilidad Private y sin README**, y Git inicia sesión con **Git Credential Manager** (una ventana del navegador en el primer push; viene con Git para Windows). **Nada de personal access tokens clásicos.** La Compuerta 6 (Bloque 6) tiene un chequeo sin `gh` para este camino.

**Repo del facilitador (variante aceptada).** Si por alguna razón tuya el repo vive en tu cuenta, agrega al participante como colaborador con tiempo y confirma que **aceptó** la invitación antes de la sesión. Una invitación pendiente bloquea todo, y las invitaciones vencen a los 7 días.

---

## EL GUION DE LA SESIÓN

Nueve bloques. Los minutos son el **mejor caso nominal** (~90 min). En una primera sesión, espera que cada bloque tome más, y calcula 2 a 3 horas en total. Mantén esta barra a la vista mientras dictas:

```
[ ] Block 0:   Start check: screen share + pre-flight line   5 min  ← before anything else
[ ] Block 0.5: Kickoff + consent to record                   5 min
[ ] Block 1:   Demo (peer-level, 3 key messages)           10 min
[ ] Block 1.5: Obsidian walkthrough                         5 min
[ ] Block 2:   Main Setup Prompt (Doc 02) + interview      30 min  ← capture the VAULT PATH
[ ] Block 3:   Skills & Config (Doc 03) + router test      10 min
[ ] Block 3.5: Status line + context protocol               5 min  ← load-bearing
[ ] Block 4:   First exercise: KICKOFF NOT FINISH          10 min
[ ] Block 5:   Orientation (cheat sheet + Docs 04 and 06) 5–10 min
[ ] Block 6:   Quality gates + Gate 6 (GitHub, server-side) 5 min
[ ] Block 7:   Close-out: fresh-window router test          5 min  ← the real end
```

Para cada bloque: **qué haces tú**, **qué hace el participante**, **puntos de enseñanza**, **errores comunes y cómo arreglarlos**, **Esperado** (lo que tienes que ver antes de seguir) y **tiempo**. Cada bloque enlaza además un deck de Google Slides como **apoyo opcional**: compártelo en pantalla si ayuda, sáltalo si no. La narrativa de este manual alcanza para dictar sin láminas.

---

### Bloque 0 — Chequeo de arranque (5 min)

**Qué haces tú:**
- **Primero, compartir pantalla.** Pídele al participante que comparta su pantalla y confirma que puedes leer su terminal. Todo lo que sigue depende de verla. Que agrande la letra de la terminal si hace falta.
- **Lee la línea del pre-vuelo.** Ya deberías tenerla desde antes de la sesión. Pídele que la muestre (es la última línea del pre-vuelo en su historial de Claude Code) o que te la lea. Mira también su bloque seguro del chequeo de estado si lo pediste. **No corres el script en vivo; lees resultados.**
- **`PREFLIGHT: READY`** → sigue. **`PREFLIGHT: MISSING …`** → arregla ahora sólo lo que aparece, con los mismos arreglos del Doc 01. **No hay línea** → que corra el pre-vuelo ahora (Doc 01, Paso 10). Toma unos 10 minutos y reemplaza las suposiciones.
- **Revisa su línea `cd`.** El pre-vuelo le dio una línea `cd "<ruta del vault>"`. Asegúrate de que la tenga, y **anota tú la ruta del *vault***.

**Qué hace el participante:** comparte pantalla, muestra la línea del pre-vuelo, tiene lista la línea `cd`.

**Errores comunes y arreglos:**
- No encuentra la línea → que abra Claude Code y le pida mostrar el resumen del pre-vuelo de su última sesión, o que vuelva a correr el pre-vuelo.
- La línea dice `ACCOUNT: team` y no lo sabías → no pasa nada; el Doc 03 sigue el camino de organización. Cuenta con que los conectores y los plugins los controla el administrador.
- Obsidian muestra otro *vault* distinto al que creó el pre-vuelo → que use **Abrir carpeta como bóveda** sobre la carpeta del pre-vuelo. Nunca «Crear nueva bóveda».

**Esperado:** pantalla visible, `PREFLIGHT: READY` (o las faltas recién arregladas), ruta del *vault* anotada.

**Tiempo:** 5 min. No te lo saltes porque «me dijo que está listo». Ése es justo el reporte en el que los datos del campo dicen que no hay que confiar.

### Bloque 0.5 — Arranque + consentimiento para grabar (5 min)

**Qué haces tú:**
- Dale una bienvenida cálida al participante. Es su primera experiencia práctica; marca un tono tranquilo de «tenemos tiempo».
- **Pregunta antes de grabar.** Si quieres grabar o transcribir, pregúntalo ahora y acepta un no. Si acepta, arranca la grabación y confirma que de verdad está corriendo.
- Confirma que los datos del primer ejercicio son **datos de muestra**, no datos confidenciales.

**Qué hace el participante:** responde la pregunta de consentimiento; confirma qué datos trajo.

**Puntos de enseñanza** *(el encuadre de «por qué estamos aquí»; apoyo: [Deck 1 — Why AI Acceleration Club](https://docs.google.com/presentation/d/1CP-dpqKJjVbm29mV6h-5IVsqs6FXjivZVeai5gpKjVU/edit), 5 láminas)*:
- **El arco del programa.** «Hoy es la Fase 0, la configuración. Después de esto trabajas por tu cuenta un par de semanas y luego nos volvemos a reunir. La Fase 0 es la base sobre la que se para todo lo demás.»
- **Con qué te vas.** «Hoy vas a tener cuatro cosas, todas conectadas: un segundo cerebro en Obsidian, un repositorio de código privado, tu primer proyecto de verdad y una configuración que le permite a Claude encontrar todo eso solo. Y vamos a *probar* que funciona antes de terminar.»
- **Encuadre entre pares.** «Así trabajo yo todos los días. Nada de esto es exótico. Al final tú también vas a trabajar así.»

**Errores comunes y arreglos:**
- La herramienta de grabación no tiene permiso → en Mac, da permiso de pantalla y micrófono en Ajustes del Sistema y reinicia la herramienta. Si toma más de un minuto, no grabes y toma notas.

**Esperado:** consentimiento respondido (grabando, o sin grabar por decisión); datos de muestra confirmados.

**Tiempo:** 5 min. Que una configuración en verde no te tiente a quedarte. Pasa al demo.

---

### Bloque 1 — Demo (10 min)

**Qué haces tú:**
- Muestra **tu propio** sistema haciendo algo real, idealmente algo que refleje el mundo del participante. Escoge de lo que de verdad usas:
  - *Finanzas / empresa familiar* → un reporte armado a partir de los datos fuente, con el comentario escrito por Claude.
  - *Ejecutivo / gerente general con poco tiempo* → tu centro de mando de la mañana: un comando que reconstruye el día entre tus calendarios, tareas y seguimientos en un plan priorizado.
  - *Operaciones / cadena de suministro* → exportación desordenada → datos limpios y estructurados → una decisión concreta (un punto de reorden, un pronóstico), con Claude atrapando los casos borde de calidad de datos.
  - *Creativo / marca* → construir en vivo una herramienta interactiva chiquita a partir de una idea de una línea.
  - *Trabajador del conocimiento / indeciso* → el ciclo segundo cerebro + corrección: haz una corrección y mira cómo queda escrita en un `CLAUDE.md` para que se quede.
- Mantenlo en 3 a 4 minutos de hacer, y después recapitula. Usa material no confidencial en pantalla.

**Qué hace el participante:** mira. Nada más; éste es tu bloque.

**Puntos de enseñanza** *(los 3 mensajes clave + el mapa mental; apoyo: [Deck 2 — Demo Framing](https://docs.google.com/presentation/d/1asbdnHSlYSfPrtDUjeku292hDy-PlbCYNi0ov_POgkU/edit), 3 láminas, sólo si el demo tarda en arrancar)*:

Abre con el **mapa mental de 30 segundos**. La fricción número uno de quien empieza no es el vocabulario; es no ver cómo encajan las piezas (el vocabulario está en el Doc 07). Di:

> «Hay tres piezas, cada una con un trabajo. **Claude Code** es la IA en tu terminal: *actúa*. Tu ***vault*** en Obsidian es donde vive tu conocimiento: *guarda*. **Git y GitHub** son el historial y el respaldo privado de tu código. Trabajas *con* Claude, *dentro* de tu *vault*; Git protege la parte del código.»

Luego, durante el demo, aterriza los **tres mensajes clave**:

1. **«Claude lee el `CLAUDE.md` solo. Ya conoce el contexto del proyecto.»** (El `CLAUDE.md` es el cerebro del sistema.)
2. **«Cada corrección que hago se guarda, así que mejora con el tiempo.»** (Las correcciones se acumulan en comportamiento permanente.)
3. **«Cierro cada sesión con `/session-close`. Eso es lo que preserva el estado.»** (La disciplina es lo que hace confiable al sistema.)

Cierra con un recuento de **«lo que acabas de ver»**: nombra las tres cosas que Claude hizo solo (leyó el contexto, produjo el artefacto y, si lo mostraste, guardó una corrección).

**Errores comunes y arreglos:**
- El demo cae plano / se siente como una vitrina de la herramienta → tráelo de vuelta a *su* mundo y a *tus* archivos reales. El golpe emocional es «alguien como yo trabaja así».
- Empiezas a improvisar y se alarga → escoge una sola cosa ajustada que puedas hacer en 3 minutos. Más largo es peor.

**Esperado:** el participante puede repetir con sus palabras el mapa de las tres piezas.

**Tiempo:** 10 min incluyendo el recuento.

---

### Bloque 1.5 — Recorrido por Obsidian (5 min)

**Qué haces tú:**
- Antes de correr cualquier configuración, recorre Obsidian con el participante para que la estructura PARA que se va a generar tenga sentido visual. (Hacerlo *primero* evita el acompañamiento a mitad de configuración que antes frenaba el Bloque 2.)
- Que abra Obsidian en **el *vault* que creó el pre-vuelo**. Sólo contiene `00 HUB/00 INBOX/` con sus archivos del kit. Es lo esperado.

**Qué hace el participante** (en Obsidian):
1. **Panel izquierdo, el árbol de archivos.** «Cada carpeta de aquí se vuelve una sección de tu segundo cerebro.»
2. **Crear una nota nueva (Cmd/Ctrl+N).** «Las notas son sólo archivos Markdown: texto plano con formato.»
3. **Wikilinks: escribe `[[Prueba]]` en la nota.** «Así se conectan las notas, como los enlaces internos de Wikipedia.»
4. **Vista de grafo (ícono de la barra lateral izquierda).** «Aquí es donde tu conocimiento se vuelve una red.»
5. **Paleta de comandos (Cmd/Ctrl+P).** «Todo lo que Obsidian puede hacer, lo encuentras aquí.»
6. **Clic derecho sobre un archivo → Copiar ruta.** «Así le vas a pasar los prompts largos a Claude todo el día de hoy.» (Lo practicó en el pre-vuelo.)

Después, que borre la nota de prueba.

**Puntos de enseñanza** *(apoyo: [Deck 3 — Obsidian + PARA + GTD](https://docs.google.com/presentation/d/1M7q-WG6qSRPQjqShRXSwP0khRXTgDWbCzXN7o5poM48/edit), 7 láminas)*:
- **Tu segundo cerebro, tuyo para siempre.** «Es Markdown en texto plano en tu propio disco, sin dependencia de ningún proveedor. Si Obsidian desapareciera mañana, tus notas siguen siendo archivos tuyos.»
- **PARA.** «Cuatro cajones: **Proyectos** (activos, con un final), **Áreas** (responsabilidades continuas), **Recursos** (material de referencia), **Archivo** (lo terminado). Todo tiene un lugar.»
- **GTD en una línea.** «Capturar → Aclarar → Organizar → Ejecutar. Sácalo de tu cabeza, decide qué es, ponlo donde va, y después hazlo.»
- **Dónde encaja Claude Code.** «Los `CLAUDE.md` son las *reglas*; las carpetas son los *datos*. Claude lee las reglas y trabaja sobre los datos.»

Después señala el *vault* casi vacío y deja el gancho:

> «Ahora esto está casi vacío. En la próxima media hora, Claude Code lo va a llenar: la estructura PARA, un brief de proyecto para tu caso, un mapa de área y tu brief del recorrido en el AI Acceleration Club. Mira cómo se llena el panel izquierdo mientras avanzamos.»

**Errores comunes y arreglos:**
- Obsidian abre otro *vault* más viejo → selector de bóvedas (abajo a la izquierda) → **Abrir carpeta como bóveda** → la carpeta del pre-vuelo. Nunca «Crear nueva bóveda»: un segundo *vault* es la forma más común de que la configuración y Obsidian terminen mirando carpetas distintas.
- La vista de grafo está vacía y confunde → es lo esperado en un *vault* vacío; se llena a medida que aparecen notas y enlaces.

**Esperado:** Obsidian muestra el *vault* del pre-vuelo (`00 HUB/00 INBOX/` con los archivos del kit), y el participante sabe hacer Copiar ruta.

**Tiempo:** 5 min. Es orientación, no un tutorial. Mantenlo en movimiento.

---

### Bloque 2 — Main Setup Prompt + entrevista en vivo (30 min)

Es el bloque más grande y el corazón de la configuración. El **Doc 02** (Windows: **02W**) es el prompt.

**Qué haces tú:**
- Que el participante abra una terminal (Windows: Git Bash), corra la línea `cd "<ruta del vault>"` del pre-vuelo y después `claude`. Si Claude pregunta si confía en la carpeta, la respuesta es **Sí**.
- Que **cargue el Doc 02 por archivo**: en Obsidian, clic derecho sobre el Main Setup Prompt en `00 HUB/00 INBOX/` → **Copiar ruta** (la ruta completa del sistema), y en Claude Code: `Lee el archivo <ruta> y sigue sus instrucciones, empezando en "PARA CLAUDE — EMPIEZA AQUÍ".` En Windows, las `\` de la ruta se vuelven `/`.
- Vigila los errores, explica qué hace cada paso mientras pasa, y **confirma que la ruta del *vault*** que usa Claude coincide con la que anotaste en el Bloque 0.
- Durante la **entrevista en vivo**, ayuda al participante a articular su problema de trabajo y orienta hacia un primer caso que encaje bien (ver abajo).
- **Antes del primer push**, asegúrate de que Claude se detenga y confirme con el participante el dueño, la visibilidad **Private** y la lista de archivos a subir.

**Qué hace el participante:**
1. Entra al *vault* y arranca Claude Code.
2. Carga el Doc 02 por archivo y lo recorre de forma interactiva, respondiendo la entrevista.
3. Confirma dueño, Private y la lista de archivos antes del primer push.

**La entrevista en vivo, la diferencia clave de este kit.** Donde el pipeline interno pre-arma los archivos del proyecto a partir de un formulario, el Doc 02 hace que Claude dirija la entrevista *en vivo*. Claude va a:
- Preguntar a qué se dedica y cuál es su rol.
- Preguntar por el proyecto concreto que trajo (el Doc 01 pidió uno, con una entrada y una salida).
- Hacer 1 o 2 preguntas ligeras de calibración (comodidad con la terminal y con Git) para fijar el ritmo.
- Recomendar el **mejor primer caso** y, con la confirmación del participante, generar en el acto su `CLAUDE.md` de proyecto y su brief de proyecto.

Tu trabajo durante la entrevista es ser el copiloto humano: ayúdalo a escoger un caso con **datos de muestra que de verdad pueda traer** y un **primer prototipo que quepa en 10 a 15 minutos** de trabajo de la Semana 1. Si duda entre dos problemas, orienta hacia el más concreto y el que más le duele. Claude deriva el nombre del repo a partir del caso escogido; tú no llenas nada.

**Lo que construye el Main Setup Prompt:**
- La estructura de carpetas PARA + el espacio de trabajo `05 AI/CLAUDE CODE/`.
- El `CLAUDE.md` del *vault* (reglas de comportamiento) y el enrutador global `~/.claude/CLAUDE.md`.
- `~/.claude/settings.json`: permisos acotados, **fusionados** con lo que ya hubiera (nunca sobrescrito, nunca aprobaciones generales), el hook de sonido y el monitor de contexto (barra de estado + resguardos de auto-compactación).
- Git configurado, GitHub conectado y un repo en `~/dev`, subido a un repositorio **privado** de GitHub bajo la propia cuenta del participante.
- El `CLAUDE.md` del repo (contexto del dominio específico del caso, sacado de la entrevista), con un puente de vuelta al brief del *vault*.
- La plantilla de brief de proyecto, el brief de proyecto en `01 PROJECTS/`, el MOC del Área y el brief del recorrido en el AI Acceleration Club.
- El primer commit y el AIAC Cheat Sheet.

**Puntos de enseñanza** *(apoyo: [Deck 5 — Main Setup Prompt](https://docs.google.com/presentation/d/11wEbrjj-TDYecZA2giQBPD9LLTrneKzazWYHzGXeyI4/edit), 3 láminas · [Deck 4 — Git + GitHub 101](https://docs.google.com/presentation/d/19vTq1FY-SIZKNY-yAUWuVKUzD6Ly3C3gUrUKRT7ENHs/edit), 11 láminas; no las pases todas)*:
- **Qué hace el prompt.** «Este único prompt arma todo tu entorno en una sola corrida interactiva. Estás viendo un sistema armarse solo.»
- **La cadena de `CLAUDE.md`.** «Hay tres niveles, de lo general a lo específico: el **enrutador global** (`~/.claude/CLAUDE.md`) apunta a tu *vault* desde cualquier lugar; el **`CLAUDE.md` del *vault*** tiene tus reglas generales de trabajo; el **`CLAUDE.md` del repo** tiene el conocimiento del dominio de este proyecto. Claude lee el más específico que aplique.»
- **Dos briefs, no uno.** «Tienes dos briefs: un **brief del caso** para el proyecto en sí, y un **brief del recorrido** que sigue tu avance en el programa.»
- **Git/GitHub en palabras simples** (dilas mientras corren los pasos de Git):
  - «El control de versiones es una máquina del tiempo para tus archivos.»
  - «Un repositorio es sólo una carpeta que recuerda toda su historia.»
  - «Un commit es un punto de guardado al que siempre puedes volver.»
  - «GitHub es la copia remota: tu respaldo privado y, más adelante, la forma de colaborar.»
  - «`.gitignore` es la lista de lo que *nunca* guardamos en el historial: secretos, archivos de datos grandes o confidenciales.»
- **Privado por defecto.** «Tu repo es privado: sólo tú lo ves. Lo revisamos antes del primer push, siempre.»
- **Conocimiento vs. código.** «Fíjate que el repo vive en `~/dev`, **no** dentro del *vault*. El conocimiento en el *vault*, el código en `~/dev`. Sepáralos.»

**Errores comunes y arreglos:**
- **Lo que pegó salió cortado** → pegó en vez de cargar por archivo. Para, y carga el Doc 02 por ruta.
- **Ruta del *vault* con espacios** → un `cd` sin comillas falla en el espacio. La línea `cd "…"` del pre-vuelo va entre comillas; úsala tal cual. Arrancar `claude` desde dentro del *vault* evita el problema por completo.
- **Git no está instalado** → Doc 01, Paso 2 (`xcode-select --install` en Mac, Git para Windows en Windows).
- **Falla la creación del repo** → `gh auth status` tiene que mostrar un usuario con sesión iniciada; si no, el participante corre `gh auth login --hostname github.com --git-protocol https --web` en **otra ventana de terminal** (Claude no puede contestar sus preguntas). Sin `gh` → el camino por navegador de Pre-Sesión § 10.
- **Venció la sesión de Claude Code** → `/login`, o sal y vuelve a correr `claude`.
- **Claude no está disponible donde está el participante** → Claude solo funciona en los [países y regiones admitidos](https://www.anthropic.com/legal/supported-regions), según dónde está físicamente la persona. No intentes saltarte esa restricción: reprograma para un momento en que esté en una región admitida (pídele que revise la lista antes de agendar). Si una red o VPN *de la empresa* bloquea `claude.ai`, `github.com` u `obsidian.md`, su IT habilita esos dominios.
- **Claude bloquea una edición de configuración y menciona el modo** → presiona **Shift+Tab** para pasar al modo por defecto, haz la edición y vuelve.
- **La entrevista se atasca, el participante no logra nombrar un problema** → vuelve al proyecto que trajo según el Doc 01; si sigue trabado, escoge una tarea concreta y recurrente de su rol y nómbrala tú. Un caso decente le gana a uno perfecto.

**Esperado:** carpetas PARA visibles en Obsidian; el repo en `~/dev/<nombre-del-repo>` (no dentro del *vault*); el primer push hecho después del chequeo de dueño/Private/archivos; la ruta del *vault* confirmada.

**Tiempo:** 30 min nominales, muchas veces más de 45 en una primera sesión. **Confirma la ruta del *vault* antes de salir de este bloque.**

---

### Bloque 3 — Skills & Config + prueba del enrutador (10 min)

El **Doc 03** (Windows: **03W**) es el prompt. El participante sigue en Claude Code, en el *vault*.

**Qué haces tú:**
- Que **cargue el Doc 03 por archivo**, igual que el Doc 02 (Copiar ruta → `Lee el archivo <ruta> y sigue sus instrucciones, empezando en "PARA CLAUDE — EMPIEZA AQUÍ".`).
- Cuando el Doc 03 pregunte qué **plataforma de correo** usa (Google / Microsoft / otra), ayúdalo a responder; el prompt sigue el camino que corresponda en vivo.
- En una **cuenta de equipo** (`ACCOUNT: team`), espera el camino de organización: primero los plugins que reparte la organización, la instalación manual sólo como respaldo.
- Cuando termine, corre la **prueba obligatoria de enrutamiento desde fuera del *vault*** (abajo). No te la saltes.

**Qué hace el participante:** carga el Doc 03 y lo recorre. Instala el `CLAUDE.md` global con el enrutador primero, los plugins, las *skills* iniciales (incluida `/session-close`), `/meeting-minutes` para su herramienta de transcripción, y lo guía por el Modo Plan.

**La prueba obligatoria del enrutador** (una compuerta real, que en sesiones pasadas se detectó demasiado tarde):
1. Escribe `/exit` para salir de Claude Code.
2. `cd ~`
3. Corre `claude`
4. Pregunta: **«¿Qué archivos hay en el INBOX de mi vault?»**

Si Claude lee el INBOX del *vault* **sin que le den la ruta**, el enrutador funciona. Si dice «no sé dónde está tu vault», el `CLAUDE.md` global se generó como documento de *perfil* en vez de *enrutador*. Arréglalo ahora (vuelve a correr el paso del enrutador del Doc 03) y repite la prueba hasta que pase.

**Puntos de enseñanza** *(apoyo: [Deck 6 — Skills + Plugins](https://docs.google.com/presentation/d/1NOddx8buEAwcOZ_8Z_Tubo8aX8i_5LsQIKfjsEEDP_I/edit), 3 láminas)*:
- **Qué es una *skill*.** «Una *skill* es un procedimiento reutilizable que invocas con `/nombre`. Piénsala como un manual guardado que Claude ya sabe correr.»
- **Los plugins.** «Los plugins empaquetan muchos de estos manuales. Hoy te llevas un juego inicial.»
- **Las *skills* y los plugins cargan sólo en sesiones nuevas.** «Lo que instales ahora aparece la *próxima* vez que arranques Claude Code, no en esta sesión. Por eso lo revisamos en una ventana nueva.»
- **Por qué importa el enrutador** (dilo en voz alta): «`~/.claude/CLAUDE.md` es la razón por la que Claude siempre sabe dónde está tu *vault*, desde cualquier carpeta de tu computadora.»
- **El hook de sonido.** «El sonido quiere decir que te puedes ir y volver cuando Claude termine.»
- **El hábito.** «`/session-close` es el hábito más importante. Es lo que hace que el sistema mejore con el tiempo.»

**Errores comunes y arreglos:**
- **Enrutador generado como documento de perfil** (el error clásico) → la prueba desde fuera del *vault* lo atrapa; vuelve a correr el paso del enrutador y repite la prueba.
- **Un plugin o una *skill* «no está»** → revisa en una sesión **nueva**; después, `claude plugin list` en la terminal (la vista de texto) muestra lo instalado y activado. En cuentas de equipo, una copia instalada a mano con el mismo nombre que un plugin de la organización puede taparlo; prefiere la copia de la organización.
- **Confusión con el Modo Plan** → que presione **Shift+Tab** hasta que la barra de abajo diga *plan*, escriba un prompt real, revise el plan y salga. Es sólo práctica.
- **Se escogió mal la rama de correo** → vuelve a correr ese paso con la plataforma correcta.

**Esperado:** la prueba del enrutador pasa desde `cd ~`; `claude plugin list` muestra compound-engineering, superpowers y playground; `/session-close` aparece al escribir `/` en una sesión **nueva**.

**Tiempo:** 10 min nominales, incluyendo la prueba de enrutamiento.

---

### Bloque 3.5 — Barra de estado + protocolo de contexto (5 min)

Es corto pero **carga peso.** La ventana de contexto es uno de los dos modelos mentales más importantes (el otro es el `CLAUDE.md`). Quien lo entiende desde el primer día evita la falla de «mi sesión empeoraba mientras más trabajaba».

**Qué haces tú, parte 1: confirma la barra de estado (2 min).**
- El Doc 02 (PASO 3.5) ya instaló el monitor de contexto: una barra de estado con el % de contexto, un aviso al 50% y un resguardo de auto-compactación al 75%. Que el participante busque el porcentaje de contexto abajo en su terminal. Si no lo ve, que abra una sesión **nueva**: los cambios de la barra aparecen después de reiniciar.
- **No corras `/statusline-setup`.** Reemplaza la barra personalizada del Doc 02 y quita el aviso del 50%. Si la barra sigue sin aparecer después de reiniciar, vuelve a correr sólo el PASO 3.5 del Doc 02 (en Windows, el 02W tiene un respaldo documentado).

**Qué haces tú, parte 2: enseña el protocolo (3 min).** Di estos umbrales en voz alta; *son* el protocolo:

- **Compacta idealmente antes del 50%.** La mejor calidad. Planifica las sesiones para llegar a pausas naturales antes del 50%, y entonces `/session-close` + `/clear`.
- **Después del 50% empieza la degradación del contexto.** No es catastrófico, pero Claude empieza a olvidar el contexto anterior y a hacer referencias inconsistentes. La barra se pone amarilla y avisa una vez.
- **Compacta sí o sí antes del 70%.** Pasado el 70%, la calidad se desploma. La auto-compactación quedó en 75%, con un freno justo antes para que decidas tú y no la herramienta.

Las dos formas de compactar al llegar al umbral:
- **A. `/session-close` + `/clear`**: lo más limpio. El estado queda guardado en el Continuation Prompt del brief, y después se reinicia. Lo mejor para cambiar de tarea.
- **B. `/compact`**: la compactación dentro de la sesión que trae Claude Code; te deja seguir a mitad de tarea. Pierde detalle por diseño, así que A es el mejor hábito.

**Puntos de enseñanza** *(apoyo: [Deck 7 — Context Window + Status Line](https://docs.google.com/presentation/d/1bW0KsaclZ58A4kGoAG530cKXIIrFjkEFIagSKYtwqP8/edit), 4 láminas)*. Di el «por qué» en voz alta:

> «Si te llevas un solo protocolo de hoy, que sea éste. Mirar la barra de contexto es el hábito que separa a quienes mejoran con el tiempo de quienes ven sus sesiones empeorar mientras más trabajan. *Puedes* trabajar pasado el 50%, pero ya estás avisado. Pasado el 70% es donde lo pagas.»

**Qué hace el participante:** encuentra el % de contexto en la barra y te repite los tres umbrales.

**Errores comunes y arreglos:**
- La barra no se ve → primero una sesión nueva; después revisa `jq --version` (la barra depende de `jq`); después vuelve a correr el PASO 3.5 del Doc 02.
- En Windows la barra falla → sigue el respaldo del 02W y para a los 3 minutos; la barra es sólo visual, el resguardo de auto-compactación funciona sin ella.

**Esperado:** un % de contexto visible en la barra (o el respaldo del 02W aplicado); el participante puede decir 50% / 70% / 75%.

**Tiempo:** 5 min. No lo recortes para ganar tiempo; son los 5 minutos de mayor impacto de la sesión.

---

### Bloque 4 — Primer ejercicio: ARRANCAR, NO TERMINAR (10 min)

Vuelve a leer el principio de **«Arrancar, no terminar»** antes de dictar este bloque. Este bloque deja al participante *andando* con su problema real. **No** completa un entregable.

**Qué haces tú:**
- Que abra una ventana **nueva** de terminal y arranque una sesión **en el repo** (no en el *vault*): `cd ~/dev/<nombre-del-repo>` y después `claude`.
- Escoge el camino según si trajo datos de muestra.

  **Camino A — trajo datos de muestra.** Le da a Claude un prompt como:

  > «Copia el archivo <ruta de mi archivo de muestra> a data/raw/ de este repo. No modifiques el original. Después lee el CLAUDE.md y dime, para cada archivo de data/raw/, qué tiene, cuántas filas, qué período cubre y cómo se relaciona con el proyecto del CLAUDE.md. Al final deja una nota de por dónde seguimos en la Semana 1.»

  Tope de 2 o 3 archivos. El punto es mostrar el flujo, no cargarlo todo.

  **Camino B — todavía no tiene datos.**

  > «Lee el CLAUDE.md. Crea una plantilla de inventario de datos en docs/data-inventory.md que yo pueda ir llenando durante la próxima semana.»

**Qué hace el participante:** corre el prompt de arranque y ve a Claude trabajando en *su* problema real.

**Puntos de enseñanza** *(apoyo: [Deck 8 — Primer Ejercicio + Homework](https://docs.google.com/presentation/d/1HWjogJzi_z0IjmAyLEWwbY--ct8RnXNd6Kr95bz3Fm4/edit), 4 láminas)*:
- **Camino A vs Camino B.** «Si trajiste datos, apuntamos a Claude hacia ellos. Si no, armamos la lista para conseguirlos. De cualquier forma te vas con impulso.»
- **Arrancar, no terminar.** Dilo explícitamente: *«Esto no lo terminamos ahora. Vas a seguir esta semana por tu cuenta; ése es todo el punto. Mi trabajo hoy es dejarte en el flujo en el que SABES que puedes retomarlo mañana.»*
- **Los datos crudos quedan fuera de Git.** «`data/raw/` y `data/working/` están en el `.gitignore`. Sólo se hace commit de los resultados procesados.»
- **Si te trabas, vuelve.** «Esta semana, si te trabas, es normal y no da vergüenza. Escríbeme y te destrabo.» (Esto prepara el modelo de soporte del Doc 04.)

**Errores comunes y arreglos:**
- **Te tienta terminarlo** → no lo hagas. Un resultado parcial + una miga es el resultado *correcto*.
- **Trajo datos confidenciales** → no los cargues. Pasa al Camino B, o hagan primero juntos una copia limpia.
- **Sin datos y sin inventario claro** → la plantilla `docs/data-inventory.md` es el entregable; es un punto de partida perfectamente bueno para la Semana 1.

**Esperado:** un prompt real corrido en la sesión del repo; un resultado parcial o la plantilla de inventario; una miga para la Semana 1.

**Tiempo:** 10 min. Para aunque el resultado sea parcial, *sobre todo* si es parcial.

---

### Bloque 5 — Orientación (5–10 min)

**Qué haces tú:**
- Recorre el **AIAC Cheat Sheet** (lo creó el Doc 02, en `00 HUB/00 INBOX/`).
- Entrega el **Doc 04 — Next Steps Brief** (su tarea y su hoja de ruta) y el **Doc 06 — Kit de Supervivencia del Plan Pro** (cómo hacer que Pro rinda). Que guarde los dos ahora en `00 HUB/00 INBOX/`.

**Qué hace el participante:** sigue el cheat sheet; guarda los Docs 04 y 06 en el *vault*.

**Puntos de enseñanza.** Recalca cinco cosas:
1. **Dos espacios de trabajo:** el *vault* (notas, pensar) vs. el repo (código, datos).
2. **El ciclo de automejora:** corriges a Claude → la corrección queda escrita en un `CLAUDE.md` → no repite el error.
3. **Siempre `/session-close`** antes de terminar. Es el mecanismo de aprendizaje acumulado.
4. **Planifica antes de construir:** Shift+Tab al Modo Plan para tareas medianas; una *skill* de planificación para las grandes.
5. **La tarea** (primero la Parte 0 del Doc 04): cerrar bien la Fase 0, abrir Claude Code todos los días (aunque sean 10 minutos), juntar los datos del caso y completar el primer flujo.

**Nota sobre el Doc 04:** el Doc 04 tiene una sección que el participante llena él mismo (Parte 3, «los próximos flujos de tu proyecto»), porque su caso se escogió en vivo. Anímalo a anotar 2 o 3 próximos pasos para su proyecto mientras lo tiene fresco.

**Errores comunes y arreglos:**
- El participante trata la tarea como opcional → enmárcala como la parte en la que de verdad llega el valor; la sesión fue sólo la configuración.

**Esperado:** los Docs 04 y 06 guardados en `00 HUB/00 INBOX/`, junto al Cheat Sheet.

**Tiempo:** 5–10 min.

---

### Bloque 6 — Compuertas de calidad + Compuerta 6 (5 min)

Recórrelas con el participante. **Cada compuerta necesita una evidencia que puedas ver en su pantalla**, no su palabra. Si una compuerta falla, arréglala **ahora**, antes del cierre.

```
QUALITY GATES — Phase 0
━━━━━━━━━━━━━━━━━━━━━━━

- [ ] Obsidian shows the vault Claude built (PARA folders + vault CLAUDE.md),
      and .obsidian/ is inside that same folder
- [ ] Claude Code running: claude --version works
- [ ] ~/.claude/CLAUDE.md is a ROUTER (first section = "Default Workspace"
      with an imperative load instruction, NOT a profile-first doc)
- [ ] Outside-the-vault routing test PASSED (cd ~ && claude, then
      "list my vault INBOX" works without giving the path)
- [ ] ~/.claude/settings.json: narrow permissions merged in (no blanket
      git/cat/interpreter approvals), sound hook, context monitor
- [ ] Status line shows a context % (or the 02W fallback applied)
- [ ] Participant can state the context thresholds (50% / 70% / 75%)
- [ ] Gate 6 PASSED: private GitHub repo verified on the server (below)
- [ ] Project brief in the vault, linked to the repo
- [ ] /session-close shows up in a NEW session
- [ ] claude plugin list shows the plugins Doc 03 installed
      (compound-engineering, superpowers, playground)
- [ ] Ran at least one real prompt on their case (Path A or Path B)
- [ ] Can articulate what they'll work on this week
```

#### Compuerta 6 — GitHub, verificado del lado del servidor (antes de que se vaya)

GitHub es el paso que sigue pasando en la sala y fallando en el disco. `git remote -v` sólo prueba que alguien escribió una URL: la imprime tranquilamente para un repositorio que no existe. Ni la palabra del participante ni el resumen de una grabación lo prueban tampoco. **Pregúntale a GitHub directamente.**

**Con `gh` (lo normal).** En la sesión del repo, el participante le da a Claude este prompt (reemplaza dueño y repo):

> «Corre `gh repo view github.com/<dueño>/<repo> --json nameWithOwner,visibility`, después `gh api --hostname github.com repos/<dueño>/<repo>/commits --jq '.[0].sha[0:7]'` y `git log --oneline -1`. Muéstrame la salida tal cual de los tres.»

**PASA** = `nameWithOwner` es su repo, `visibility` es **`PRIVATE`**, y el SHA del commit que da GitHub coincide con los primeros 7 caracteres de la línea local de `git log`. Un error de `gh`, una respuesta vacía, un repo público o un SHA distinto es **FALLA**, sin importar lo que mostraba la terminal diez minutos antes.

**Sin `gh`.** El participante le pide a Claude que corra `git remote get-url --push --all origin`, luego `git ls-remote <esa dirección> HEAD` y `git rev-parse --short HEAD`. El primero tiene que imprimir exactamente una línea, `https://github.com/<dueño>/<repo>.git` (o la misma dirección en la forma SSH de GitHub), con su dueño y su nombre de repo; el segundo le pregunta a esa dirección exacta (no a `origin`, cuya dirección de lectura puede ser otra) por su último commit, y sus primeros 7 caracteres tienen que coincidir con el tercero. Después abre la página del repo en el navegador mientras comparte pantalla, y tú confirmas la etiqueta **Private** junto al nombre del repositorio.

**Variante con repo del facilitador.** Ser colaborador no prueba nada sobre la privacidad ni sobre el push, así que corres tú las tres comprobaciones en tu máquina:

1. `gh api repos/<dueño>/<repo>/collaborators --jq '.[].login'` — aparece su usuario. Una **invitación pendiente es FALLA**: que la acepte ya en `https://github.com/<dueño>/<repo>/invitations`.
2. `gh repo view github.com/<dueño>/<repo> --json nameWithOwner,visibility` — `visibility` es **`PRIVATE`**.
3. `gh api --hostname github.com repos/<dueño>/<repo>/commits --jq '.[0].sha[0:7]'` — coincide con los primeros 7 caracteres de la línea de `git log --oneline -1` que el Claude del participante muestra en su pantalla.

PASA = las tres. Si falta cualquiera, es **FALLA**.

**Si el repo resulta público**, arréglalo antes que nada: en GitHub, Settings → General → Danger Zone → Change visibility → Private. Después revisa qué se subió.

**Esperado:** cada casilla marcada con evidencia; la Compuerta 6 PASA, dicho en voz alta.

**Tiempo:** normalmente 3 a 5 min si todo aguantó.

---

### Bloque 7 — Cierre: prueba del enrutador en una ventana nueva (5 min) — EL FINAL DE VERDAD

La sesión **no** termina en las compuertas de calidad. Termina cuando el participante tiene **dos ventanas de Claude Code abiertas**: una que sigue trabajando en el repo, y otra recién abierta desde *fuera* del *vault* que prueba que todo el sistema (enrutador + brief del proyecto) funciona de punta a punta. Sin esta última prueba se va «configurado pero sin probar»; con ella se va «listo para trabajar».

**Qué haces tú, parte 1: deja abierta la ventana actual.**
- El participante **no** cierra la sesión de Claude Code que corre en el repo. Nada de `/exit`, nada de cerrar la pestaña.

**Qué haces tú, parte 2: abre una segunda ventana y prueba.**
- Que el participante:
  1. Abra una ventana o pestaña **nueva** de terminal (aparte de la del repo).
  2. `cd ~` (su carpeta de usuario, **no** el *vault*).
  3. `claude` (una sesión nueva).
  4. Escriba exactamente este prompt:

     > **«Abre el brief del proyecto de mi caso y dame un resumen de 3 viñetas de lo que estoy construyendo.»**

**Comportamiento esperado:**
- Claude lee `~/.claude/CLAUDE.md` al arrancar la sesión.
- Encuentra la ruta del *vault* en el bloque del enrutador.
- Abre el brief del proyecto en `01 PROJECTS/…`.
- Devuelve un resumen de 3 viñetas **sin** que el participante le dé ninguna ruta.

**Si pasa:** ya tiene la prueba de que todo el sistema funciona de punta a punta. Di:

> «Listo. Acabamos de probar el ciclo completo. Mañana abres Claude Code, le dices que retome donde lo dejaste, y lo hace.»

**Si falla — modos comunes y arreglos:**
- «No sé dónde está tu vault» → el bloque del enrutador no se generó bien; vuelve a aplicar el paso del enrutador del Doc 03 y repite la prueba.
- Encuentra el *vault* pero no el brief → la ruta del brief está mal o el archivo no se creó; busca en `01 PROJECTS/` el nombre real del archivo y corrige la ruta en el `CLAUDE.md` del *vault*.
- Lee todo pero el resumen sale enredado → probablemente un detalle menor del frontmatter; es raro. Anótalo como arreglo de la Semana 1 y sigue.

**No declares la sesión completa hasta que esta prueba pase.** Éste es el final de verdad, no el Bloque 6.

**Di el resultado en voz alta y anótalo**, *«prueba del enrutador: PASÓ»* o *«prueba del enrutador: FALLÓ por X»*, en tus propias notas. Si grabaste, la grabación sólo sirve cuando el resultado se dice. Una sesión terminó en *«necesito saber si funcionó»* y después nadie pudo confirmarlo.

**Esperado:** «prueba del enrutador: PASÓ», dicho y anotado.

**Tiempo:** 5 min (+ margen si hay que resolver problemas).

---

## POST-SESIÓN

Haz esto el mismo día, mientras está fresco.

### Lista de salida: cada renglón necesita evidencia

No reportes la sesión como completa con un renglón vacío. Para cada punto, escribe al lado la evidencia (una ruta, la salida de un comando, un SHA) o «omitido porque …»:

```
EXIT CHECKLIST — <participant>, <date>
- [ ] Pre-flight line received before the session ............ <the line>
- [ ] Vault path ............................................. <path>
- [ ] Repo + Gate 6 .......................................... <owner/repo, PRIVATE, SHA>
- [ ] Router test (Block 7) .................................. PASSED / FAILED because …
- [ ] Case project brief ..................................... <path under 01 PROJECTS/>
- [ ] Docs 04 + 06 saved in the vault INBOX .................. yes / no
- [ ] Recording .............................................. consented + where it is / not recorded
- [ ] Open issues + who fixes them ........................... <list, or "none">
- [ ] Follow-up date ......................................... <date>
```

Llena la lista con **lo que pasó**, nunca con el plan. Un renglón del plan copiado como resultado («plugins sincronizados») es justo la forma en que un cierre anterior reportó algo que nunca ocurrió.

### Después

- **Confirma que la tarea quedó clara.** En tu nota de seguimiento, repite los primeros pasos del Doc 04: la Parte 0 (cerrar la Fase 0: revisar lo que dejó la configuración, cerrar a mano la sesión de configuración), abrir Claude Code todos los días (aunque sean 10 min), juntar los datos del caso, completar el primer flujo. Recuérdale que el primer ejercicio fue un *arranque*; terminarlo esta semana es el punto.
- **Empieza por cualquier compuerta que falló.** Si falló la Compuerta 6 o la prueba del enrutador, el seguimiento abre con eso, con el arreglo y una fecha.
- **Cómo hacer seguimiento.** Vuelve a contactarlo después de 1 o 2 semanas de trabajo por su cuenta. Si se queda callado, un solo empujón sin presión («¿cómo va el caso? ¿algo trabado?») suele bastar. Mantén un modelo de soporte sin vergüenza: trabarse es lo esperado, no un fracaso.
- **Grabación.** Si grabaste (con consentimiento), la transcripción es tu fuente para las notas de seguimiento. Guárdala con el mismo cuidado que cualquier otra cosa con el trabajo del participante, y bórrala cuando ya no la necesites.
- **Mejora el kit.** Anota cualquier fricción (un paso que falló, un prompt confuso) y arregla el kit, o repórtalo, antes de la próxima sesión.

---

## LA CONFIGURACIÓN ÚNICA DEL FACILITADOR

Haz esto **una vez**, antes de dictar tu primera sesión. No es por participante.

1. **Llena los marcadores.** `[SET: your support channel]` en los **Docs 01 y 04**; `[TOOL]` en los **Docs 03 / 03W** (por participante, si las herramientas de transcripción cambian). Son los únicos valores que llenas.
2. **Haz el ensayo en seco** del kit en una máquina limpia o una cuenta de usuario nueva (Pre-Sesión § 1).
3. **Mantén tu copia al día.** Trabaja desde el kit publicado y revisa si hay una versión nueva antes de cada sesión; los prompts cambian a medida que cambia Claude Code.
4. **Recuerda el formato.** Este kit está escrito para sesiones **uno-a-uno**. La narrativa de este manual es tu guion; **los decks enlazados en cada bloque son apoyo opcional**. Compártelos en pantalla si ayudan, sáltalos si no.

---

## FUERA DE ALCANCE (por ahora)

Anotado para que sepas que son omisiones deliberadas, no huecos:

- **Formato grupal / por cohorte.** Este kit está escrito uno-a-uno. Se puede dictar con grupos chicos, pero calcula al menos 3 horas, dale a cada dos o tres participantes un ayudante que corra con ellos la Compuerta 6 antes de que se vayan, y llena en vivo una grilla compartida de compuertas. Con una docena de personas, un solo facilitador no puede ser además el escribano.
- **Plugin / paquete de skills instalable para facilitadores.** No hay plugin de facilitador en este kit, a propósito. Es sólo documentos, para que funcione con cualquiera sin infraestructura compartida.
