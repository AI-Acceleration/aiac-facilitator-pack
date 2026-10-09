---
title: "Manual del Facilitador — Cómo dictar una sesión de Fase 0"
created: 2026-07-14
category: reference
status: draft
tags: [aiac, phase0, co-facilitator, facilitator-manual, spanish, mangan]
related: ["[[AIAC Phase 0 Co-Facilitator Kit (EN) — Design Spec]]", "[[AI Acceleration Club - Phase 0 Playbook]]"]
lang: es
translated_from: "05 — Facilitator Manual — How to Run a Phase 0 Session.md"
---

# Manual del Facilitador — Cómo dictar una sesión de Fase 0

> **Esta es la pieza central del Kit de Co-Facilitación AIAC Fase 0.** Está escrito para **ti, el facilitador** — la persona que dicta la sesión — no para el participante. Léelo de principio a fin antes de tu primera sesión, y después mantenlo abierto a tu lado (segundo monitor, segunda pestaña, o impreso) mientras dictas una. Es tu partitura de director.

## Qué es este kit

Este kit empaqueta el onboarding de **Fase 0** del AI Acceleration Club para que puedas dictarlo con cualquier persona, **uno-a-uno**, en unos **90 minutos** — una sesión en vivo y práctica en la que el participante sale con un segundo cerebro funcionando, un repositorio de código real, su primer proyecto, y una configuración de Claude Code que amarra todo junto.

Dos cosas hacen distinto a este kit del pipeline interno del que se deriva:

- **Solo documentos.** No hay plugin que instalar ni nada que pre-generar. Tú conduces la sesión manualmente; el participante pega prompts en Markdown plano dentro de Claude Code. Todo lo que ambos necesitan son los cinco documentos de esta carpeta.
- **Autoconfiguración en vivo.** El participante **no** llena un formulario de admisión de antemano y **no** recibe archivos preconstruidos para su caso. En vez de eso, durante la sesión, Claude lo entrevista sobre su trabajo, lo ayuda a escoger su primer proyecto real, y genera sus archivos de proyecto en el acto. El participante también crea **su propio** repositorio de GitHub bajo **su propia** cuenta — no hay repositorio central ni invitación de colaborador que perseguir.

### Los cinco documentos

| Doc | Para quién | Cuándo se usa |
|---|---|---|
| **01 — Pre-Session Setup Instructions** | Participante | Se envía unos días antes de la sesión; instala y verifica prerrequisitos, y viene con 1–3 problemas de trabajo. |
| **02 — Main Setup Prompt** | Participante | Se pega en Claude Code durante el **Bloque 2**. Construye el *vault*, el repositorio y — vía una entrevista en vivo — su primer caso. |
| **03 — Skills & Config Setup Prompt** | Participante | Se pega en Claude Code durante el **Bloque 3**. Instala el enrutador global, los plugins y las *skills* núcleo. |
| **04 — Next Steps Brief** | Participante | Se entrega como tarea en el **Bloque 5**; es su hoja de ruta para las semanas siguientes. |
| **05 — Facilitator Manual** (este doc) | Tú | Tu guion de la sesión completa. |

Los Docs 02 y 03 están **listos para pegar**: su cuerpo *es* el prompt que el participante pega. Presérvalos exactamente — un comando o bloque JSON cambiado rompe el entorno del participante.

---

## FILOSOFÍA — lee esto antes de tu primera sesión

### Qué logra la Fase 0

Al final de una sesión de Fase 0 el participante tiene, y ha *probado*, cuatro cosas funcionando juntas:

1. **Un segundo cerebro** — un *vault* de Obsidian con una estructura PARA (Projects / Areas / Resources / Archives).
2. **Un repositorio real** — un repositorio Git + GitHub en `~/dev` para su primer caso: bajo su propia cuenta por defecto, o uno del facilitador al que se le invitó y aceptó (ver Bloque 6).
3. **Su primer caso** — un problema de trabajo real, escogido en vivo, con un brief de proyecto y un `CLAUDE.md` de proyecto que le da a Claude el contexto del dominio.
4. **El enrutador** — un `~/.claude/CLAUDE.md` global que apunta a Claude hacia su *vault* desde *cualquier* directorio, para que nunca tenga que explicar dónde viven las cosas.

Ese es el entregable completo: no un trabajo terminado, sino un *sistema funcionando que el participante puede retomar mañana.*

### "Arranque, no cierre"

Este es el principio más importante para el ritmo de la sesión, y el que los facilitadores nuevos rompen más a menudo.

**El Bloque 4 arranca el primer ejercicio. No lo termina.** El trabajo de la sesión es poner al participante *corriendo* sobre su problema real con Claude Code — no producir un entregable pulido en vivo. Completar el primer flujo de trabajo es **tarea de la Semana 1** (Doc 04).

Por qué contenerse:

- Terminarlo en vivo empuja la sesión más allá de dos horas, agota la atención del participante, y quema su límite de uso de Claude.
- Le roba el momento constructor de agencia de "yo hice esto solo" en la Semana 1 — que es el punto de todo el programa.

Así que cuando el primer ejercicio empiece a producir salida, tu instinto va a ser seguir hasta que esté "listo". Resístelo. Produce un resultado parcial, deja una miga de pan clara de dónde continuar, y sigue. Dilo en voz alta para que el participante no se confunda: *"No vamos a terminar esto ahorita — eso es la tarea, y es la parte buena."*

### La demo entre pares

Tu demo de apertura (Bloque 1) no es un pitch de producto. Eres tú mostrando **tu propio** sistema funcionando haciendo algo real — idealmente algo que refleje el mundo del participante. El mensaje que estás transmitiendo es *"esta es una manera normal de trabajar para una persona como tú"*, no *"mira lo que puede hacer la herramienta"*. Mantenlo entre pares: archivos reales, correcciones reales, un cierre real. Tres o cuatro minutos son suficientes.

---

## PRE-SESIÓN

Haz esto en los días previos a la sesión.

### 1. Envía el Doc 01 unos días antes

Envíale el **Doc 01 — Pre-Session Setup Instructions** al participante varios días antes de que se reúnan — con suficiente pista para que instale todo y te escriba si algo falla. El Doc 01 es autoservicio: cada prerrequisito viene con un prompt listo para pegar que él corre en claude.ai, así que rara vez te necesita. El Doc 01 también le pide que **venga con 1–3 problemas de trabajo reales** con los que quisiera la ayuda de Claude — esto reemplaza al viejo formulario de admisión y es lo que alimenta la entrevista en vivo del Bloque 2.

### 2. La compuerta de verificación de prerrequisitos de 24 horas

El día antes (o al menos 24 horas antes), confirma que el participante esté realmente configurado. El Doc 01 termina con un prompt de verificación que revisa el stack; pídele que lo corra y te envíe el resultado. Estás buscando **seis ítems confirmados**:

1. **Suscripción Claude Pro/Max activa** — puede entrar a claude.ai y usarlo.
2. **Obsidian instalado** — abierto al menos una vez. (**No** debería haber creado un *vault* todavía — eso pasa en vivo en el Bloque 2.)
> **El resumen del Paso 7 es la compuerta — y en el campo nunca llegó por sí solo de ningún
> estudiante.** Trata el silencio como "no hecho", nunca como "seguro está bien". Dos arreglos que
> funcionan:
>
> 1. **Pídelo explícitamente** cuando envíes los documentos, y otra vez 24 h antes.
> 2. **Envía `tools/aiac-status-check.sh`** (como gemelo `.sh.txt` — WhatsApp y Gmail bloquean `.sh`).
>    Es de solo lectura y reporta DONE / NOT DONE por documento; el primer NOT DONE es el punto de
>    retomada. Haz que lo corra en su **Terminal, no dentro de Claude Code** — bajo un *sandbox* el
>    Bash de Claude está confinado al *vault*, así que las revisiones de `~/.claude` fallarían por la
>    razón equivocada.
>
> Una tercera opción que funciona aún mejor para participantes no técnicos: **corre la pre-sesión en
> vivo con él** (instalan juntos, compuerta imposible de fallar en silencio).
>
> **Una cuarta opción ya no es opcional: el Bloque 0 de abajo vuelve a correr el mismo script en
> vivo, como lo primero que haces en la sesión** — sin importar si el envío de pre-sesión funcionó.
> Trata una petición de pre-sesión fallida como algo esperado, no como una corredera; el Bloque 0 es
> la red que la atrapa.

> **Si el participante pide que Claude solo toque el *vault* que le da** — envíale también
> **`02-S — Sandbox Setup`**, para correrlo después del Doc 01 y *antes* del Doc 02. Aproximadamente
> uno de cada diez lo pide sin que se lo sugieran, y es la objeción que si no bloquea a cualquiera en
> una máquina del empleador. Tres cosas que saber antes de aceptar correrlo:
>
> - El **bloque de permisos del PASO 3 del Doc 02 se salta** — el 02-S lo reemplaza deliberadamente.
> - **Claude no puede correr `git`** bajo el *sandbox* (bloqueado por diseño, no por mala
>   configuración). El participante corre git él mismo; el *commit* se convierte en su acto de
>   aprobación. Dilo de entrada para que no se lea como una falla a mitad de sesión.
> - **`gh` puede fallar** bajo modo estricto (TLS en CLIs de Go bajo Seatbelt). Usa HTTPS + un PAT
>   **clásico**; el kit ya trata a `gh` como opcional.
>
> Solo Mac y Linux — Windows nativo no tiene *sandbox* (requiere WSL2). Una Fase 0 completa ha corrido
> sobre él de punta a punta, y el Bloque 7 pasó.
>
> **"Me dijeron que está listo" es un reporte, no un estado.** Una sesión arrancó a ciegas; otra se
> agendó sobre un "ya está todo instalado" y luego se atascó dos veces, con una semana de diferencia,
> por una entrada de PATH faltante. Al revés, un estudiante dado por perdido con 19 días de atraso
> resultó estar *terminado* y esperándonos — el script fue lo que lo descubrió.

3. **Git instalado y una cuenta de GitHub que exista** — esa es la compuerta. `gh` en sí NO es requerido (el Doc 01 nunca lo instala en Mac y lo llama opcional en Windows). Corre `gh auth status` solo para saber cuál camino toma el Paso 2: con sesión iniciada -> camino `gh`; no instalado o sin sesión -> Git Credential Manager o un PAT. Cualquiera de las dos respuestas está bien; ninguna bloquea la sesión.
4. **Claude Code instalado y funcionando** — `claude --version` devuelve una versión. (En Mac, un terminal moderno como Ghostty es un plus; el Terminal integrado también sirve.)
5. **Granola instalado** — y con permisos de pantalla/micrófono otorgados para que pueda grabar la sesión.
6. **1–3 problemas de trabajo reales listos** — ya pensó en qué quiere trabajar.

Si falta cualquiera de los seis, resuélvelo **antes** de la sesión, no durante. Una falla de prerrequisito descubierta en vivo es la manera más común de que una sesión de 90 minutos se vuelva de 2+ horas.

### 3. Confirma que Granola vaya a grabar

La grabación de Granola es **obligatoria** — es cómo la sesión queda transcrita para el seguimiento. Confirma que Granola esté instalado y con permisos en la compuerta de arriba, y confirma que esté realmente **grabando** al inicio del Bloque 0.5, justo después de la revisión de estado del Bloque 0, antes de cualquier otra cosa de la sesión propiamente dicha.

### 4. La compuerta de acceso del Bloque 0 (la versión de este kit)

El pipeline interno en español hace que los facilitadores persigan una *invitación de colaborador* a un repositorio central antes de la sesión — porque allá el repositorio se precrea en una organización compartida. **Este kit no funciona así.** Aquí el participante crea **su propio** repositorio bajo **su propia** cuenta de GitHub, en vivo, durante el Bloque 2.

Así que la compuerta de acceso de este kit es más simple. Todo lo que necesitas confirmado es:

> **El participante tiene Claude Code corriendo + una cuenta de GitHub + `gh` autenticado.**

Verifica la autenticación en vivo al inicio de la sesión con:

```
gh auth status
```

Si reporta un usuario de GitHub con sesión iniciada, el paso de creación del repositorio del Bloque 2 va a funcionar. Si da error o muestra "not logged in", pausa y haz que corra `gh auth login` (flujo de navegador) antes de seguir. **No** hay invitación de colaborador que aceptar y **no** hay repositorio central — no salgas a buscar uno.

---

## EL GUION DE LA SESIÓN DE 90 MINUTOS

Nueve bloques, ~90 minutos más un colchón de ~5 minutos para el Bloque 7. Mantén esta barra visible mientras dictas:

```
[ ] Block 0:   Pre-session status check (live re-verify)  3 min  ← NEW, before anything else
[ ] Block 0.5: Kickoff + pre-work check                   5 min
[ ] Block 1:   Demo (peer-level, 3 key messages)        10 min
[ ] Block 1.5: Obsidian walkthrough                      5 min
[ ] Block 2:   Main Setup Prompt (Doc 02) + interview   30 min  ← capture the VAULT PATH
[ ] Block 3:   Skills & Config (Doc 03) + router test   10 min
[ ] Block 3.5: Status line + context protocol            5 min  ← load-bearing
[ ] Block 4:   First exercise — KICKOFF NOT FINISH      10 min
[ ] Block 5:   Orientation (cheat sheet + Doc 04)      5–10 min
[ ] Block 6:   Quality gates checklist                   —
[ ] Block 7:   Close-out — fresh-window router test      5 min  ← the real end
```

Para cada bloque de abajo: **qué haces tú**, **qué hace el participante**, **puntos de enseñanza** (la narrativa; **cada bloque enlaza además su deck de Google Slides como apoyo opcional** — desde 2026-09-10 los 8 decks son material oficial del kit, en ES y EN), **errores comunes + arreglos**, y **tiempos**.

---

### Bloque 0 — Revisión de estado de pre-sesión (3 min — NUEVO)

> **Por qué existe esto (agregado el 2026-08-24).** La § "La compuerta de verificación de prerrequisitos de 24 horas" de arriba ya le pide al participante que corra `tools/aiac-status-check.sh` y te envíe el resultado *antes* de la sesión — pero en el campo ese autorreporte "nunca llegó por sí solo de ningún estudiante". Este bloque convierte la re-corrida en vivo de ese mismo script en lo PRIMERO que haces en la sesión, formal y obligatorio, no en un recurso improvisado al que acudes solo cuando la petición de pre-sesión falló visiblemente. Corre antes de confirmar Granola y antes de la compuerta de acceso del Bloque 0.5 — antes de cualquier otra cosa.

**Qué haces tú:**
- Antes de saludar, antes de confirmar Granola: haz que el participante abra su **Terminal (no Claude Code)** y corra:

  ```
  bash ~/Downloads/aiac-status-check.sh
  ```

  (Ya debería estar en su máquina desde el envío de pre-sesión — `tools/aiac-status-check.sh.txt`. Si no lo tiene, comparte pantalla y pega el contenido de `tools/aiac-status-check.sh` para que él lo guarde y lo corra.)

- Haz que pegue la salida COMPLETA en el chat o que te lea la línea de STAGE 0.
- Los ítems de **STAGE 0** marcados `[ -- ] NOT DONE` (git / Claude Code / jq / Obsidian) son brechas reales — resuélvelas ahora, antes que nada. Esta es la verdadera revisión de prerrequisitos que se suponía que el autorreporte iba a atrapar.
- Los ítems marcados `[sess]` son esperados — se construyen en vivo a partir del Bloque 2, no es algo que el participante se haya saltado. No persigas estos.
- Si el reporte dice "READING: you look PRE-SESSION" y el Stage 0 está limpio, su trabajo previo está genuinamente completo — pasa directo al Bloque 0.5.

**Qué hace el participante:**
- Corre el script en su propio terminal y pega la salida.

**Errores comunes + arreglos:**
- El script reporta una brecha genuina de Stage 0 que el envío de pre-sesión debió haber atrapado → arréglala ahora (los mismos arreglos del Doc 01); este es exactamente el caso de falla silenciosa para el que existe el script.
- El participante nunca recibió el script con antelación → comparte pantalla y pégalo en vivo; anota la brecha de entrega en tu Bitácora de Fricción post-sesión para que el envío de pre-sesión se revise la próxima vez.

**Tiempo:** 3 min. No te saltes esto porque "me dijeron que está listo" — ese es precisamente el reporte que los datos de campo dicen que no hay que creer.

### Bloque 0.5 — Arranque + revisión del trabajo previo (5 min)

**Qué haces tú:**
- Dale la bienvenida cálidamente. Esta es su primera experiencia práctica — pon un tono calmado, de "tenemos tiempo".
- Confirma que **Granola esté grabando**.
- Corre la compuerta de acceso: confirma que Git funciona (`git --version`) y que tiene una cuenta de GitHub. Luego corre `gh auth status` puramente para enrutar: con sesión iniciada -> usa el camino `gh` más adelante; cualquier otra cosa -> planifica con Git Credential Manager o un PAT. NO detengas la sesión para instalar `gh`.
- **Nota sobre el PAT (del campo):** si el repositorio de entrega vive bajo la cuenta del facilitador, un PAT *de grano fino* NO va a alcanzarlo — usa un PAT **clásico** con alcance `repo`. En una máquina del empleador cuyo llavero ya guarda credenciales de trabajo, `git config --global credential.useHttpPath true` acota las credenciales por repositorio sin perturbarlas.
- Reconfirma rápidamente que los seis ítems de prerrequisito sigan en pie (Claude Code abre, Obsidian está instalado, etc.).

**Qué hace el participante:**
- Confirma su configuración, corre `gh auth status`, y (si hace falta) se autentica.

**Puntos de enseñanza** *(el encuadre de "por qué estamos aquí" — apoyo: [Deck 1 — Why AI Acceleration Club](https://docs.google.com/presentation/d/1CP-dpqKJjVbm29mV6h-5IVsqs6FXjivZVeai5gpKjVU/edit), 5 láminas)*:
- **El arco del programa.** "Hoy es la Fase 0 — la configuración. Después de esto trabajas por tu cuenta un par de semanas, y luego nos reunimos de nuevo. La Fase 0 es el cimiento sobre el que se para todo lo demás."
- **Con qué vas a salir.** "En unos 90 minutos vas a tener cuatro cosas, todas conectadas entre sí: un segundo cerebro en Obsidian, un repositorio de código real, tu primer proyecto de verdad, y una configuración que le permite a Claude encontrar todo eso automáticamente. Y vamos a *probar* que funciona antes de terminar."
- **Encuadre entre pares.** "Así es como yo trabajo todos los días. Nada de esto es exótico — para el final tú también lo vas a estar haciendo."

**Errores comunes + arreglos:**
- `gh auth status` dice que no hay sesión iniciada → `gh auth login`, escoge GitHub.com + HTTPS + navegador; vuelve a correrlo para confirmar.
- Granola no graba / sin permiso → otorga permiso de pantalla + micrófono en Configuración del Sistema de macOS y reinicia Granola; no sigas hasta que esté en vivo.

**Tiempo:** 5 min. No dejes que una configuración en verde te tiente a demorarte — pasa a la demo.

---

### Bloque 1 — Demo (10 min)

**Qué haces tú:**
- Muestra **tu propio** sistema haciendo algo real, idealmente reflejando el mundo del participante. Escoge de lo que realmente usas:
  - *Finanzas / empresa familiar* → un reporte compilado desde datos fuente, con el comentario escrito por ti.
  - *Ejecutivo / gerente general apurado* → tu centro de comando matutino: un comando que reconstruye el día entre tus calendarios, tareas y seguimientos en un plan priorizado.
  - *Operaciones / cadena de suministro* → exportación desordenada → datos limpios y estructurados → una decisión real (un punto de reorden, un pronóstico), con Claude atrapando los casos borde de calidad de datos.
  - *Creativo / marca* → construir en vivo una herramienta interactiva pequeña a partir de una idea de una línea.
  - *Trabajador del conocimiento / no está seguro* → el segundo cerebro + el ciclo de corrección: haz una corrección y observa cómo queda escrita en un `CLAUDE.md` para que se quede.
- Mantenlo en 3–4 minutos de acción, y luego recapitula.

**Qué hace el participante:**
- Observa. Eso es todo — este es tu bloque.

**Puntos de enseñanza** *(los 3 mensajes clave + el mapa mental — apoyo: [Deck 2 — Demo Framing](https://docs.google.com/presentation/d/1asbdnHSlYSfPrtDUjeku292hDy-PlbCYNi0ov_POgkU/edit), 3 láminas, sólo si el demo tarda en arrancar)*:

Abre con el **mapa mental de 30 segundos** — la fricción #1 para los nuevos no es el vocabulario, es no ver cómo encajan las piezas. Di:

> "Hay tres piezas, cada una con un solo trabajo. **Claude Code** es la IA en tu terminal — ella *actúa*. Tu ***vault*** en Obsidian es donde vive tu conocimiento — él *almacena*. **Git y GitHub** son el historial y el respaldo de tu código. Trabajas *con* Claude, *dentro* de tu *vault*; Git protege la parte del código."

Luego, durante la demo, aterriza los **tres mensajes clave**:

1. **"Claude lee el `CLAUDE.md` automáticamente — ya conoce el contexto del proyecto."** (El `CLAUDE.md` es el cerebro del sistema.)
2. **"Cada corrección que hago queda guardada — así que se vuelve más inteligente con el tiempo."** (Las correcciones se acumulan en comportamiento permanente.)
3. **"Yo cierro cada sesión con `/session-close` — eso es lo que preserva el estado."** (La disciplina es lo que hace confiable al sistema.)

Cierra con una recapitulación de **"lo que acabas de ver"**: nombra las tres cosas que Claude hizo por su cuenta (leyó el contexto, produjo el artefacto, y — si lo mostraste — guardó una corrección).

**Errores comunes + arreglos:**
- La demo cae plana / se siente como una vitrina de herramientas → tráela de vuelta al mundo *de él* y a *tus* archivos reales. El golpe emocional es "una persona como yo trabaja así", no "mira lo que puede hacer".
- Empiezas a improvisar y se alarga → escoge una sola cosa apretada que puedas hacer en 3 minutos. Más largo es peor.

**Tiempo:** 10 min incluyendo la recapitulación.

---

### Bloque 1.5 — Recorrido por Obsidian (5 min)

**Qué haces tú:**
- Antes de correr cualquier configuración, dale al participante un recorrido por Obsidian para que la estructura PARA que está a punto de generarse tenga sentido visual. (Hacer esto *primero* evita el acompañamiento a mitad de configuración que antes hacía lento al Bloque 2.)
- Haz que abra Obsidian (lo instaló en los prerrequisitos pero **no** debería haber creado un *vault* todavía).

**Qué hace el participante:**
- Sigue en Obsidian:
  1. **Panel izquierdo — el árbol de archivos.** "Cada carpeta aquí se convierte en una sección de tu segundo cerebro."
  2. **Crear una nota nueva (Cmd/Ctrl+N).** "Las notas son solo archivos Markdown — texto plano con formato."
  3. **Wikilinks — escribe `[[Test]]` en la nota.** "Así es como se conectan las notas — como los enlaces internos de Wikipedia."
  4. **Vista de grafo (ícono de la barra lateral izquierda).** "Aquí es donde tu conocimiento se vuelve una red."
  5. **Paleta de comandos (Cmd/Ctrl+P).** "Cualquier cosa que Obsidian pueda hacer, la consigues aquí."

**Puntos de enseñanza** *(apoyo: [Deck 3 — Obsidian + PARA + GTD](https://docs.google.com/presentation/d/1M7q-WG6qSRPQjqShRXSwP0khRXTgDWbCzXN7o5poM48/edit), 7 láminas)*:
- **Tu segundo cerebro, tuyo para siempre.** "Es Markdown en texto plano en tu propio disco — sin amarre a un proveedor. Si Obsidian desapareciera mañana, tus notas siguen siendo archivos que tú eres dueño."
- **PARA.** "Cuatro cajones: **Projects** (activos, con un final), **Areas** (responsabilidades continuas), **Resources** (material de referencia), **Archives** (terminado). Todo tiene su lugar."
- **GTD en una línea.** "Capturar → Clarificar → Organizar → Ejecutar. Sácalo de tu cabeza, decide qué es, ponlo donde va, y entonces hazlo."
- **Dónde encaja Claude Code.** "Los archivos `CLAUDE.md` son las *reglas*; las carpetas son los *datos*. Claude lee las reglas y trabaja sobre los datos."

Luego apunta al *vault* vacío y pon el gancho:

> "Ahorita esto está vacío. En los próximos 30 minutos, Claude Code lo va a llenar — la estructura PARA, un brief de proyecto para tu caso, un mapa de área, y tu brief del recorrido por el AI Acceleration Club. Observa cómo se puebla el panel izquierdo mientras avanzamos."

**Errores comunes + arreglos:**
- El participante ya creó un *vault* → está bien, úsalo, pero asegúrate de que esté vacío; si tiene desorden, crea uno nuevo vacío ahora.
- La vista de grafo está vacía y confunde → eso se espera en un *vault* vacío; dile que se llena a medida que aparecen notas y enlaces.

**Tiempo:** 5 min. Esto es orientación, no un tutorial — mantenlo en movimiento.

---

### Bloque 2 — Main Setup Prompt + entrevista en vivo (30 min)

Este es el bloque más grande y el corazón de la configuración. El **Doc 02** es el prompt.

**Qué haces tú:**
- Haz que el participante cree un *vault* nuevo y lance Claude Code dentro de él (ve la nota de Mac sobre rutas con espacios más abajo).
- Haz que pegue el **Doc 02** en Claude Code.
- Vigila los errores, explica qué hace cada paso a medida que ocurre, y — algo crítico — **anota la ruta del *vault*** cuando se cree. La vas a necesitar después, y el participante va a ir rápido.
- Durante la porción de **entrevista en vivo**, ayuda al participante a articular sus problemas de trabajo y dirígelo hacia un primer caso que calce bien (ver abajo).

**Qué hace el participante:**
1. Crea un *vault* nuevo en Obsidian (GUI → "Create new vault").
2. Abre un terminal y lanza Claude Code desde dentro de ese *vault* (o lo lanza directo desde la carpeta del *vault* creada por Obsidian — ve la trampa).
3. Pega el **Doc 02** y avanza por él interactivamente.

**La entrevista en vivo — la diferencia clave de este kit.** Donde el pipeline interno preconstruye los archivos de proyecto del participante a partir de un formulario, el Doc 02 hace que Claude corra la entrevista *en vivo*. Claude va a:
- Preguntar a qué se dedica y su rol.
- Preguntar por sus 1–3 problemas de trabajo (los que el Doc 01 le dijo que trajera).
- Hacer 1–2 preguntas ligeras de calibración (comodidad con terminal / Git) para fijar el ritmo.
- Recomendar el **mejor primer caso** — y, con la confirmación del participante, generar en el acto su `CLAUDE.md` de proyecto y su brief de proyecto.

Tu trabajo durante la entrevista es ser el copiloto humano: ayúdalo a escoger el caso con **datos que realmente pueda traer** y un **primer prototipo que quepa en 10–15 minutos** de trabajo de la Semana 1. Si está dividido entre dos problemas, dirígelo hacia el que sea más concreto y más doloroso para él. Claude también le pide su nombre + correo (o lee `git config`) y deriva el nombre del repositorio del caso escogido — tú no llenas nada.

**Qué construye el Main Setup Prompt:**
- La estructura de carpetas PARA + el espacio de trabajo `05 AI/CLAUDE CODE/`.
- El `CLAUDE.md` del *vault* (reglas de comportamiento) y el enrutador global `~/.claude/CLAUDE.md`.
- El `settings.json` (permisos + *hook* de sonido + el monitor de contexto).
- Git configurado, GitHub conectado, y un repositorio **creado bajo la cuenta propia del participante** en `~/dev`.
- El `CLAUDE.md` del repositorio (contexto de dominio específico del caso, salido de la entrevista).
- El brief de proyecto en `01 PROJECTS/`, el MOC de Área, y el brief del recorrido por el AI Acceleration Club.
- El primer *commit* y la Hoja de Trucos AIAC.

**Puntos de enseñanza** *(apoyo: [Deck 5 — Main Setup Prompt](https://docs.google.com/presentation/d/11wEbrjj-TDYecZA2giQBPD9LLTrneKzazWYHzGXeyI4/edit), 3 láminas · [Deck 4 — Git + GitHub 101](https://docs.google.com/presentation/d/19vTq1FY-SIZKNY-yAUWuVKUzD6Ly3C3gUrUKRT7ENHs/edit), 11 láminas — no las pases todas)*:
- **Qué hace el prompt.** "Este único prompt construye todo tu entorno en una sola corrida interactiva — estás viendo un sistema ensamblarse solo."
- **La cadena de `CLAUDE.md`.** "Hay tres niveles, de general a específico: el **enrutador global** (`~/.claude/CLAUDE.md`) apunta a tu *vault* desde cualquier lado; el **`CLAUDE.md` del *vault*** guarda tus reglas generales de trabajo; el **`CLAUDE.md` del repositorio** guarda el conocimiento de dominio de este proyecto en particular. Claude lee el más específico que aplique."
- **Dos briefs, no uno.** "Recibes dos briefs: un **brief del caso** para el proyecto en sí, y un **brief del recorrido** que rastrea tu progreso por el programa."
- **Git/GitHub en palabras llanas** (di esto mientras corren los pasos de Git):
  - "El control de versiones es una máquina del tiempo para tus archivos."
  - "Un repositorio es simplemente una carpeta que recuerda toda su historia."
  - "Un *commit* es un punto de guardado al que siempre puedes regresar."
  - "GitHub es la copia remota — tu respaldo y, más adelante, cómo colaboras."
  - "`.gitignore` es la lista de las cosas que *nunca* guardamos en la historia — secretos, archivos de datos grandes."
- **Conocimiento vs. código.** "Fíjate que el repositorio vive en `~/dev`, **no** dentro del *vault*. El conocimiento en el *vault*, el código en `~/dev`. Mantenlos separados."

**Errores comunes + arreglos:**
- **Ruta del *vault* con espacios en Mac** — si el nombre de la carpeta del *vault* tiene un espacio (por ejemplo, "My Vault"), un `cd` crudo en el terminal falla en la segunda palabra sin comillas. No pelees con eso: crea/abre el *vault* en Obsidian, luego lanza `claude` y corre la configuración desde dentro de Claude Code — él maneja rutas con espacios nativamente. Pivota a esto de inmediato en vez de quemar minutos en la sintaxis de `cd`.
- **Git no instalado** → `xcode-select --install` (Mac) o descargar de git-scm.com (Windows).
- **La creación del repositorio falla** → confirma que la compuerta `gh auth status` del Bloque 0 realmente pasó; vuelve a autenticar con `gh auth login` si hace falta. (No hay paso de clonado ni invitación en este kit — el repositorio se crea fresco bajo su cuenta.)
- **Autenticación de Claude Code vencida** → vuelve a correr `claude` para re-autenticar.
- **País bloqueado / necesita VPN** → asegúrate de que haya una VPN activa antes de reintentar los pasos de red.
- **La entrevista se atasca — el participante no logra nombrar un problema** → recurre a los 1–3 problemas que trajo según el Doc 01; si sigue trancado, escoge una tarea recurrente concreta y respaldada por datos del rol que describió, y nómbrala tú. No dejes que esto trabe el bloque; un primer caso decente le gana a uno perfecto.

**Tiempo:** 30 min. **Captura la ruta del *vault* antes de salir de este bloque.**

---

### Bloque 3 — Skills & Config + prueba del enrutador (10 min)

El **Doc 03** es el prompt. El participante debería seguir en Claude Code, dentro del *vault*.

**Qué haces tú:**
- Haz que pegue el **Doc 03**.
- Cuando el Doc 03 pregunte cuál **stack de correo** usa (Google / Microsoft / otro), ayúdalo a responder — el prompt sigue el camino correspondiente en vivo.
- Después de que corra, haz la **prueba obligatoria de enrutamiento desde fuera del *vault*** (abajo). No te la saltes.

**Qué hace el participante:**
- Pega el Doc 03 y avanza por él. Instala el `CLAUDE.md` global enrutador-primero, los plugins Compound Engineering y Superpowers, Granola + `/meeting-minutes`, las *skills* núcleo de la Fase E (`project-create`, `playground`, `inbox-clear`, `retro`, `skill-create`), la *skill* `/session-close` en línea, y lo lleva por Plan Mode.

**La prueba obligatoria de enrutamiento del enrutador** (esta es una compuerta de verdad, detectada demasiado tarde en sesiones pasadas):
1. Escribe `/exit` para salir de Claude Code.
2. `cd ~`
3. Corre `claude`
4. Pregunta: **"What files are in my vault INBOX?"**

Si Claude lee el INBOX del *vault* **sin que le den la ruta**, el enrutador funciona. Si dice "I don't know where your vault is", el `CLAUDE.md` global se generó como un documento de *perfil* en vez de un *enrutador*. Arréglalo ahora (vuelve a correr el paso del enrutador del Doc 03 / aplica el arreglo del enrutador), y repite la prueba hasta que pase.

**Puntos de enseñanza** *(apoyo: [Deck 6 — Skills + Plugins](https://docs.google.com/presentation/d/1NOddx8buEAwcOZ_8Z_Tubo8aX8i_5LsQIKfjsEEDP_I/edit), 3 láminas)*:
- **Qué es una *skill*.** "Una *skill* es un procedimiento reutilizable que invocas con `/nombre`. Piénsalo como un manual de jugadas guardado que Claude ya sabe ejecutar."
- **Los plugins.** "**Compound Engineering** y **Superpowers** te dan gratis una biblioteca grande de esos manuales de jugadas."
- **Las *skills* solo se activan en sesiones nuevas.** "Todo lo que instales ahorita aparece la *próxima* vez que arranques Claude Code — no retroactivamente en esta sesión. Por eso probamos en una ventana fresca más adelante."
- **Por qué importa el enrutador** (dilo en voz alta): "`~/.claude/CLAUDE.md` es la razón por la que Claude siempre sabe dónde está tu *vault*, desde cualquier carpeta de tu computadora."
- **El *hook* de sonido.** "El sonido significa que puedes irte y volver cuando Claude haya terminado."
- **El único hábito.** "`/session-close` es el hábito más importante de todos — es lo que te hace más inteligente con el tiempo."

**Errores comunes + arreglos:**
- **El enrutador se generó como documento de perfil** (el bug clásico) → la prueba desde fuera del *vault* lo atrapa; vuelve a correr el paso del enrutador / aplica el arreglo del enrutador, y vuelve a probar.
- **Confusión con Plan Mode** → haz que presione Shift+Tab dos veces, escriba un prompt real, revise el plan, y salga. Es solo práctica — no hace falta ejecutarlo.
- **Rama de stack de correo escogida mal** → vuelve a correr ese paso con el stack correcto.

**Tiempo:** 10 min incluyendo la prueba de enrutamiento.

---

### Bloque 3.5 — Línea de estado + protocolo de contexto (5 min)

Este es corto pero **estructural.** La ventana de contexto es uno de los dos modelos mentales más importantes (el otro es `CLAUDE.md`). Los miembros que lo entienden desde el día uno evitan el modo de falla de "mi sesión empeoró mientras más trabajaba".

**Qué haces tú — Parte 1, montar la línea de estado (2 min):**
- Con Claude Code corriendo, haz que el participante escriba `/statusline-setup` y siga las indicaciones para habilitar un indicador de % de contexto en el terminal.
- Si `/statusline-setup` no está disponible, recurre al prompt: *"Please add a status line to my Claude Code setup that displays my current context window usage as a percentage."*
- Confirma que pueda ver algo como "43% context" en la barra.

**Qué haces tú — Parte 2, enseñar el protocolo (3 min):** Di estos tres umbrales en voz alta — ellos *son* el protocolo:

- **Compacta idealmente antes del 50%.** Mejor calidad. Esta es la meta — planifica tus sesiones para llegar a puntos de corte naturales antes del 50%, y ahí `/session-close` + `/clear`.
- **Después del 50%, empieza la pudrición de contexto.** No es catastrófico, pero Claude empieza a olvidar contexto anterior y a hacer referencias inconsistentes. La calidad se degrada gradualmente de ahí en adelante.
- **Compacta con seguridad antes del 70%.** Pasado el 70%, la calidad de salida se cae por un barranco. Una autocompactación reactiva es mucho más desordenada que una proactiva. Nunca trabajes pasado el 70%.

Las dos maneras de compactar cuando llegas al umbral:
- **A. `/session-close` + `/clear`** — la más limpia. El estado queda guardado en el Continuation Prompt del brief, y luego se reinicia. Mejor para transiciones entre tareas.
- **B. `/compact`** — la compactación integrada de Claude Code dentro de la sesión; te mantiene andando a mitad de tarea sin reiniciar. Con pérdida por diseño, así que A es el mejor hábito.

**Puntos de enseñanza** *(apoyo: [Deck 7 — Context Window + Status Line](https://docs.google.com/presentation/d/1bW0KsaclZ58A4kGoAG530cKXIIrFjkEFIagSKYtwqP8/edit), 4 láminas)* — di el "por qué" en voz alta:

> "Si te llevas un solo protocolo de hoy, es este. Vigilar la barra de contexto es el único hábito que separa a los miembros que mejoran con el tiempo de los miembros cuyas sesiones empeoran mientras más trabajan. *Puedes* trabajar pasado el 50% — pero ya quedaste advertido. Pasado el 70% es donde lo pagas."

**Qué hace el participante:**
- Monta la línea de estado, confirma que el % sea visible, y te puede repetir los tres umbrales.

**Errores comunes + arreglos:**
- `/statusline-setup` no está disponible → usa el prompt de respaldo; Claude edita `~/.claude/settings.json` y reinicia con la barra visible.
- La línea de estado no aparece → confirma que la sesión se haya reiniciado después de la edición.

**Tiempo:** 5 min. No recortes esto para ahorrar tiempo — son los 5 minutos de mayor apalancamiento de la sesión.

---

### Bloque 4 — Primer ejercicio: ARRANQUE, NO CIERRE (10 min)

Vuelve a leer el principio de **"Arranque, no cierre"** de arriba antes de correr esto. Este bloque pone al participante *corriendo* sobre su problema real — **no** completa un entregable.

**Qué haces tú:**
- Fija `REPO` una vez y reúsalo. El repositorio vive en `~/dev`, **no** en el *vault*:

  ```
  REPO="$HOME/dev/<their-repo-name>"
  ```

- Escoge el camino según si el participante trajo datos:

  **Camino A — trajo archivos de datos:**
  ```
  # copy their files in (cap at 2–3 PDFs / files)
  cp <their-file> "$REPO/data/"
  cd "$REPO" && claude
  ```
  Luego corre un prompt de **arranque** apropiado al caso — uno que produzca salida *parcial* y deje una miga de pan clara de "continúa desde aquí en la Semana 1". Por ejemplo: *"Read the CLAUDE.md, then read the files in data/. For each file, tell me what's in it, how many rows, what period it covers, and how it maps to the project structure in the CLAUDE.md."*

  **Camino B — sin datos todavía:**
  ```
  cd "$REPO" && claude
  ```
  Y luego: *"Read the CLAUDE.md. Create a data inventory template at docs/data-inventory.md that I can fill in over the next week."*

**Qué hace el participante:**
- Copia los datos (Camino A) o genera la plantilla de inventario (Camino B), corre el prompt de arranque, y ve a Claude trabajando sobre *su* problema real.

**Puntos de enseñanza** *(apoyo: [Deck 8 — Primer Ejercicio + Homework](https://docs.google.com/presentation/d/1HWjogJzi_z0IjmAyLEWwbY--ct8RnXNd6Kr95bz3Fm4/edit), 4 láminas)*:
- **Camino A vs Camino B.** "Si trajiste datos, apuntamos a Claude hacia ellos. Si no, construimos la lista para recolectarlos. En cualquier caso sales con impulso."
- **Arranque, no cierre.** Dilo explícitamente: *"No vamos a terminar esto ahorita. Vas a seguir esta semana por tu cuenta — ese es todo el punto. Mi trabajo hoy es meterte en el flujo donde SEPAS que puedes retomar esto mañana."*
- **Cuando te trabes, vuelve.** "Esta semana, si te trabas, eso es normal y no hay nada de qué apenarse — escríbeme y te destrabamos." (Esto arma el modelo de soporte del Doc 04.)

**Errores comunes + arreglos:**
- **Te tienta terminarlo** → no. Salida parcial + una miga de pan es el resultado *correcto*.
- **Sin datos y sin un inventario claro** → la plantilla `docs/data-inventory.md` es el entregable; es un punto de partida perfectamente bueno para la Semana 1.
- **Los archivos de datos son enormes / son muchos** → tope de 2–3; el punto es demostrar el flujo, no ingerir todo.

**Tiempo:** 10 min. Detente aunque la salida esté parcial — *sobre todo* si está parcial.

---

### Bloque 5 — Orientación (5–10 min)

**Qué haces tú:**
- Recorre la **Hoja de Trucos AIAC** (creada durante el Bloque 2/3, en el INBOX del *vault*).
- Entrega el **Doc 04 — Next Steps Brief** como la tarea y hoja de ruta del participante.

**Qué hace el participante:**
- Sigue el recorrido en la hoja de trucos; recibe el Doc 04.

**Puntos de enseñanza** — enfatiza cinco cosas:
1. **Dos espacios de trabajo:** el *vault* (notas, pensamiento) vs. el repositorio (código, datos).
2. **El ciclo de automejora:** corriges a Claude → la corrección queda escrita en un `CLAUDE.md` → nunca repite el error.
3. **Siempre `/session-close`** antes de terminar — es el mecanismo de aprendizaje acumulado.
4. **Planifica antes de construir:** Shift+Tab (dos veces) para tareas medianas, `/ce:plan` para las grandes.
5. **Tarea** (en el Doc 04): abrir Claude Code a diario (aunque sean 10 minutos), recolectar los datos del caso, y completar el primer flujo de trabajo.

**Nota sobre el Doc 04:** el Doc 04 contiene una sección que el participante llena él mismo al final de la sesión — la lista de "tus próximos flujos de trabajo" — porque su caso se escogió en vivo en vez de venir preescrito. Apúntalo hacia ella y anímalo a anotar 2–3 próximos pasos para su proyecto mientras está fresco.

**Errores comunes + arreglos:**
- El participante trata la tarea como opcional → encuádrala como la parte donde el valor realmente aterriza; la sesión fue solo la configuración.

**Tiempo:** 5–10 min.

---

### Bloque 6 — Lista de compuertas de calidad

Recórrela con el participante. Si falla cualquier compuerta, resuélvela **ahora**, antes del cierre.

```
QUALITY GATES — Phase 0
━━━━━━━━━━━━━━━━━━━━━━━

- [ ] Obsidian vault operational with a CLAUDE.md
- [ ] Claude Code running: claude --version works
- [ ] ~/.claude/CLAUDE.md is a ROUTER (first section = "Default Workspace"
      with an imperative load instruction — NOT a profile-first doc)
- [ ] Outside-the-vault routing test PASSED (cd ~ && claude, then
      "list my vault INBOX" works without giving the path)
- [ ] ~/.claude/settings.json has permissions + sound hook
- [ ] Status line visible in the terminal with a context % display
- [ ] Participant can state the 3 context thresholds
      (compact ideally <50%, certainly <70%, rot starts after 50%)
- [ ] GitHub repo exists with a first commit, and the participant can push to it
      - preferred: under the PARTICIPANT'S OWN account
      - accepted variant: under the FACILITATOR'S account, with the participant
        added as a collaborator AND the invitation accepted before the clone.
        If you take this path, re-read the PAT note in Block 0.5 - a
        fine-grained PAT cannot reach a facilitator-owned repo; it needs a
        CLASSIC PAT with `repo` scope. An unaccepted invite blocks the clone.
- [ ] Project brief in the vault, linked to the repo
- [ ] /session-close skill installed
- [ ] At least one plugin installed (Compound Engineering or Superpowers)
- [ ] Ran at least one real prompt on their case (Path A or Path B)
- [ ] Can articulate what they'll work on this week
```

**Tiempo:** se pliega dentro del flujo; normalmente 2–3 min si todo se sostuvo.

---

### Bloque 7 — Cierre: prueba del enrutador en ventana nueva (5 min) — EL VERDADERO FINAL

La sesión **no** termina en las compuertas de calidad. Termina cuando el participante tiene **dos ventanas de Claude Code abiertas**: una todavía trabajando en el repositorio, y otra recién abierta desde *fuera* del *vault* que prueba que todo el stack — enrutador + brief de proyecto — funciona de punta a punta. Sin esta última prueba, se va "configurado pero sin probar"; con ella, se va "listo para trabajar".

**Qué haces tú — Parte 1, deja abierta la ventana actual:**
- El participante **no** debe cerrar la sesión de Claude Code que corre en el repositorio. Ese es su cajón de arena para seguir trabajando. Sin `/exit`, sin cerrar la pestaña.

**Qué haces tú — Parte 2, abre una segunda ventana y prueba:**
- Haz que el participante:
  1. Abra una ventana o pestaña **nueva** de terminal (separada de la ventana del repositorio).
  2. `cd ~` (directorio home, **no** el *vault*).
  3. `claude` (una sesión fresca).
  4. Escriba este prompt exacto:

     > **"Open my case project brief and give me a 3-bullet summary of what I'm building."**

**Comportamiento esperado:**
- Claude lee `~/.claude/CLAUDE.md` al arrancar la sesión.
- Encuentra la ruta del *vault* en el bloque del enrutador.
- Abre el brief de proyecto en `01 PROJECTS/…`.
- Devuelve un resumen de 3 viñetas — **sin** que el participante haya dado ninguna ruta.

**Si pasa:** ahora tiene la prueba de que todo el stack funciona de punta a punta. Di:

> "Eso es todo — acabamos de probar el ciclo completo. Mañana abres Claude Code, le dices que retome donde quedaste, y lo hace."

**Si falla — modos comunes + arreglos:**
- "I don't know where your vault is" → el bloque del enrutador no se generó bien; vuelve a aplicar el arreglo del enrutador del paso correspondiente del Doc 03 y repite la prueba.
- Encuentra el *vault* pero no el brief → la ruta del brief está mal o el archivo no se creó; revisa `01 PROJECTS/` por el nombre de archivo real y corrige la ruta en el `CLAUDE.md` del *vault*.
- Lee todo pero el resumen sale enredado → probablemente un problema menor de *frontmatter*; es raro — anótalo como un arreglo de tarea de la Semana 1 y sigue.

**No declares la sesión completa hasta que esta prueba pase.** Este es el verdadero final — no el Bloque 6.

**Di el resultado en voz alta y anótalo** — *"router test: PASÓ"* o *"router test: FALLÓ por X"* — y marca la casilla del Bloque 7 en tu agenda. La grabación es lo único que el cierre (`/aiac-close`) puede leer; si nadie dice el resultado, el cierre no puede confirmar la graduación. Evidencia 2026-09-10: una sesión terminó con *"necesito saber si funcionó"* y el cierre tuvo que marcar el test como no verificado.

**Tiempo:** 5 min (+ colchón si resuelves problemas).

---

## POST-SESIÓN

Haz esto el mismo día, mientras está fresco.

- **Envía los documentos de referencia.** Envíale al participante los **Docs 02, 03 y 04**. Los Docs 02 y 03 son su red de seguridad para reconfigurar (si alguna vez necesita reconstruir el entorno); el **Doc 04** es su hoja de ruta y su tarea para las semanas que vienen.
- **Confirma que la tarea esté clara.** En tu nota de seguimiento, repite los tres ítems de tarea del Doc 04: abrir Claude Code a diario (aunque sean 10 min), recolectar los datos del caso, y completar el primer flujo de trabajo. Recuérdale que el primer ejercicio fue un *arranque* — terminarlo esta semana es el punto.
- **Cómo hacer seguimiento.** Revisa después de 1–2 semanas de su trabajo autodirigido. Si se queda callado, un solo empujoncito sin presión ("¿cómo va el caso — algo trancado?") suele bastar. Mantén el modelo de soporte sin culpa: trabarse es lo esperado, no una falla.
- **Granola.** La grabación de la sesión es tu fuente para una transcripción y cualquier minuta de seguimiento; recupérala si quieres un registro escrito.

---

## LA CONFIGURACIÓN DE UNA SOLA VEZ DEL FACILITADOR

Haz esto **una vez**, antes de dictar tu primera sesión — no es por participante.

1. **Fija tu canal de soporte en el Doc 04.** El Doc 04 tiene un único marcador señalado, `[SET: your support channel]`. Reemplázalo con el canal real que tus participantes deben usar para contactarte (un número de WhatsApp, un correo, un canal de Slack — lo que uses para llevar tu grupo). Este es el **único** valor que llenas en todo el kit; todo lo demás lo genera el participante en vivo.
2. **Ten claro dónde vive el kit.** El mantenedor guarda el kit canónico junto al resto del material de Fase 0 del AI Acceleration Club. Ten tu propia copia de trabajo donde realmente dictes las sesiones, pero revisa si hay una versión actualizada antes de cada sesión.
3. **Recuerda el formato.** Este kit es **uno-a-uno**. La narrativa de este manual es tu guion; **los decks enlazados en cada bloque son apoyo opcional** (comparte pantalla si ayudan, sáltalos si no). No busques un plugin que instalar ni un formulario que enviar — el participante construye en vivo.

---

## EXTENSIONES FUTURAS (fuera de alcance por ahora)

Anotadas para que sepas que son omisiones deliberadas, no brechas:

- **Formato de grupo / cohorte.** Este kit es solo uno-a-uno. Un formato de grupo (varios participantes, un *deck* compartido en vivo, configuración en paralelo) existe en el pipeline interno pero aquí es un proyecto futuro aparte.
- ***Decks* de enseñanza.** Este manual carga la narrativa de enseñanza para que puedas dictar sin láminas. Construir los juegos de láminas es un proyecto futuro aparte.
- **Plugin instalable / paquete de *skills*.** No hay plugin de facilitador en este kit por diseño — es solo documentos para que funcione con cualquiera sin infraestructura compartida.
