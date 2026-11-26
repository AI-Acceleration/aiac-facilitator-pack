---
title: "Instrucciones de Configuración Pre-Sesión (Participante) — AI Acceleration Club Fase 0"
created: 2026-07-14
category: reference
tags: [aiac, phase0, co-facilitator-kit, participant, pre-session, setup]
lang: es
translated_from: "01 — Pre-Session Setup Instructions (Participant).md"
---

**Aplica a:** Antes de la sesión. Lo recibes más o menos una semana antes: empieza lo antes que puedas, no la noche anterior, y termina cada paso, incluido el **pre-vuelo** del final, antes de la fecha límite que te dé tu facilitador.

# Configuración Pre-Sesión — AI Acceleration Club Fase 0

Bienvenido a la Fase 0 del AI Acceleration Club. Antes de tu sesión en vivo vas a instalar unas cuantas herramientas. Cada una cumple un papel en el sistema que vamos a montar juntos. En cada paso tienes una explicación de una línea de *para qué* la necesitas y un prompt listo para pegar en Claude (claude.ai), que te guía en la instalación y te ayuda si algo falla.

El último paso es el **pre-vuelo**. Claude Code crea tu vault, comprueba cada herramienta y termina con una línea que le mandas a tu facilitador. Esa línea es la forma en que tu facilitador sabe que estás listo. **El pre-vuelo es obligatorio.**

**Dónde mandar las cosas:** [SET: your support channel]

**¿Palabras nuevas?** Tu facilitador te manda el **Doc 07 — Vocabulario** junto con este documento: todos los términos del kit (vault, skill, plugin, brief, router…) en una página. Tenlo a mano.

> **Si te trabas en un comando:** copia el comando que escribiste y el mensaje de error, y pégalos en la misma conversación de Claude. Claude los lee y te da el siguiente paso hasta que funcione. Tú eres los ojos y las manos; Claude es el cerebro.
> **Antes de pegar, échale un vistazo.** Nunca pegues en un chat una contraseña, un token (cadenas largas al azar, que muchas veces empiezan con `ghp_`, `gho_` o `sk-`), una llave privada o un código de recuperación. Si un mensaje de error trae uno, bórralo primero.

> **Descarga sólo de los sitios oficiales que nombra cada paso.** Con esas descargas oficiales es normal y esperado un aviso como «desarrollador no identificado» (Gatekeeper en macOS) o «Windows protegió tu PC» (SmartScreen). En Mac: clic derecho sobre la app → **Abrir**, o permítela en **Ajustes del Sistema → Privacidad y seguridad**. En Windows: **Más información → Ejecutar de todas formas**. Si el aviso sale con algo que **no** bajaste del sitio oficial, o menciona un virus, detente y pregúntale a tu facilitador.

## Antes de Empezar — Tu Computadora

**Usa un equipo que tengas permitido usar para este trabajo.** Si es una laptop de la empresa, pídele a IT **antes de la sesión**:

1. **Permiso y derechos de administrador.** Instalar Git, Claude Code y las demás herramientas necesita permisos de administrador. Casi todos los equipos de IT pueden darlos por un rato para instalar. Pídelos ya, no el día de la sesión.
2. **Que Claude Code esté permitido.** Los instaladores oficiales (`claude.ai/install.sh` en Mac/Linux, `claude.ai/install.ps1` en Windows) no pueden estar bloqueados, y nada (un firewall o una política de prevención de pérdida de datos) puede bloquear `claude.ai` ni `api.anthropic.com`.
3. **Que GitHub esté permitido.** `github.com`, incluido `git push` por HTTPS, no puede estar bloqueado.

Si tu empresa no permite esto en sus equipos, háblalo con tu facilitador. No pases datos de trabajo a una computadora personal si la política de tu empresa no lo permite. El primer ejercicio se hace con **datos de muestra**, así que una computadora personal sirve, siempre que no le pongas datos confidenciales.

**¿Tu computadora está lista?** Una máquina vieja o muy lenta hace la sesión muy cuesta arriba. Revísalo ahora: un sistema operativo que todavía recibe actualizaciones, al menos 8 GB de memoria y unos cuantos GB libres en disco. Si dudas, pregúntale a tu facilitador. Puede darte una **fecha límite** para tener lista la máquina y el pre-vuelo.

**Dónde estás importa.** Claude solo está disponible en los [países y regiones admitidos](https://www.anthropic.com/legal/supported-regions), y lo que cuenta es dónde estás físicamente cuando lo usas. Revisa esa lista **antes** de la sesión; si vas a estar en un lugar que no aparece ahí, avísale a tu facilitador y elijan una fecha en la que estés en una región admitida. **Red de la empresa:** si la red o la VPN de tu empresa bloquea `claude.ai`, `github.com` u `obsidian.md`, pídele a IT que habilite esos tres dominios. No apagues una VPN de la empresa en contra de la política.

## Sólo Windows — Léelo Antes de Empezar

Si estás en Mac o Linux, salta a la tabla de abajo. En Windows, lee **todo** esto primero. Cada punto le costó tiempo de verdad a un participante de verdad.

> **Esta sección es prosa, no comandos.** Léela; no la pegues en una terminal. (Pegar prosa en
> PowerShell produce un `ParserError` y te puede dejar atascado en un prompt de continuación `>>`:
> un apóstrofo abre una comilla que nunca se cierra. Si te pasa, presiona **Ctrl+C** y sigue.)

**0. Claude Code no funciona con el plan gratuito de Claude.** Es la compuerta cero y bloquea todo lo demás.
La documentación de Anthropic es explícita: *"The free Claude.ai plan does not include Claude Code access."*
Haz el Paso 1 **antes** de intentar instalar cualquier cosa. Se resuelve solo: si `claude` abre y tienes
la sesión iniciada, el cambio de plan funcionó. Un participante de otra cohorte se quedó semanas trabado justo en esto.

**0.5. Ten claro en qué ventana escribes. Es la confusión número uno en Windows.** Windows te da tres,
y no son intercambiables:

| Ventana | Para qué |
|---|---|
| **PowerShell** | Sólo para instalar Claude Code (el comando `irm ... \| iex` del Paso 4) |
| **Git Bash** | **Todo lo demás de este kit.** Viene con Git para Windows (Paso 2). Ábrela desde el menú Inicio. |
| **CMD** (la ventana negra `C:\>`) | Nada de esto. Si tus mensajes de error empiezan con `C:\>`, estás en la ventana equivocada. |

También es normal y **no** es una instalación fallida: `where bash` no devuelve nada. Git para Windows instala
Git Bash pero no pone `bash.exe` en tu PATH. Abre Git Bash desde el menú Inicio.

**1. Pega con clic derecho.** En Git Bash, PowerShell y Windows Terminal, Ctrl+V muchas veces no funciona. Usa **clic derecho** (o el clic de la rueda del mouse, o `Shift+Insert`).

**2. Los textos largos se cortan al pegarlos.** La terminal de Windows puede recortar en silencio lo que pegas si es largo. Por eso, desde el pre-vuelo en adelante, los prompts largos nunca se pegan: le das a Claude la **ruta** del archivo y le dices que lo lea. El pre-vuelo lo practica contigo.

**3. En las rutas usa siempre barras `/`, nunca barras invertidas `\`.**
Escribe `C:/Users/YOUR-USER/AIAC-Vault`, no `C:\Users\YOUR-USER\AIAC-Vault`. Esto importa más de lo
que parece: en Git Bash una `\` sin comillas desaparece en silencio y **el comando falla sin ningún error
visible**. La falla que resulta se ve idéntica a otro problema que no tiene nada que ver, y te pasas la
sesión depurando lo que no es. Para ver una ruta en la forma correcta, Claude usa `pwd -W` (que
imprime `C:/Users/...`), no `pwd` a secas (que imprime `/c/Users/...`).

**4. El paso del PATH después de instalar Claude Code.** El instalador de Claude Code puede terminar bien y aun así decir, en su propia salida, que **no** agregó `C:\Users\YOUR-USER\.local\bin` a tu PATH. Entonces `claude` «no se reconoce». La solución: Inicio → «Editar las variables de entorno del sistema» → **Variables de entorno** → selecciona **Path** en **Variables del sistema** (o en Variables de usuario si no tienes permisos de administrador) → **Nuevo** → pega esa carpeta → Aceptar, y abre una ventana **nueva**. El prompt del Paso 4 te guía.

**5. «¿Confías en los archivos de esta carpeta?»** La primera vez que corres `claude` en una carpeta, Claude Code te lo pregunta (en inglés: *Do you trust the files in this folder?*). Para tu propia carpeta de usuario y, más adelante, tu vault, elige **Sí** (*Yes*). La respuesta por defecto es No, y No simplemente cierra.

---

## Para Qué Sirve Cada Cosa

| Herramienta | Para qué la necesitas |
|---|---|
| **Claude** (plan de pago) | El asistente de IA. Es el cerebro de todo lo demás. El plan gratuito no incluye Claude Code. |
| **Git** | Registra cada cambio de los archivos de tu proyecto, para que nunca pierdas trabajo y puedas volver atrás. |
| **Cuenta de GitHub** | El respaldo en la nube de ese trabajo. El repositorio de tu proyecto vive ahí, **privado**. |
| **Ghostty** (Mac, opcional) | Una terminal moderna. La Terminal que trae la Mac también sirve. |
| **Claude Code** | Claude en tu terminal: lee tus archivos, escribe código, arma reportes y automatiza tareas. |
| **`gh`** (GitHub CLI) | La herramienta de GitHub para la terminal. Con ella Claude crea tu repositorio privado durante la sesión. Inicias sesión una vez, desde el navegador. |
| **Python 3** | Varias skills lo usan por dentro para procesar archivos. Tú no vas a programar en Python. |
| **`jq`** | Una herramienta chiquita para leer JSON. La barra de contexto que montas en la sesión depende de ella: sin `jq` la barra nunca aparece y no hay mensaje de error. |
| **Obsidian** | Tu «segundo cerebro»: la app donde viven tus notas, tus proyectos y todo lo que generes con IA, conectado entre sí. |
| **Herramienta de transcripción** (opcional) | Convierte reuniones en texto para que Claude arme la minuta. Sirve cualquiera, o ninguna. |

---

## Paso 1 — Tu Plan de Claude (Pro alcanza para empezar)

Claude es el asistente de IA que vas a usar para todo. **Claude Code necesita un plan de pago.** Lo estándar es **Claude Pro** (unos $20 al mes), que incluye Claude Code y alcanza para empezar. Sube a Max sólo si chocas una y otra vez con los límites de uso. Precios y límites actuales: [claude.com/pricing](https://claude.com/pricing). Todos los planes tienen límites de uso que se reinician cada pocas horas y cada semana. El **Doc 06 — Kit de Supervivencia del Plan Pro** explica cómo hacer que Pro te rinda.

Este paso es manual:

1. Entra a claude.ai e inicia sesión (o crea tu cuenta).
2. **Settings → Billing** → elige **Pro**.
3. Completa el pago.

> Si tu empresa te da Claude con una cuenta **Team o Enterprise**, usa esa cuenta y sáltate el pago. Avísale a tu facilitador. El pre-vuelo también lo detecta.

## Paso 2 — Tu Cuenta de GitHub y Git

Dos cosas que van juntas pero no son lo mismo:

- **Git** es un programa en tu computadora. Registra cada cambio de los archivos de tu proyecto.
- **GitHub** es una cuenta gratuita en la nube (github.com). Ahí se respalda tu proyecto, en un repositorio **privado** que sólo tú ves.

**PRIMERO, crea tu cuenta de GitHub** (manual, 2 minutos):

1. Entra a https://github.com
2. Haz clic en **Sign up** y crea tu cuenta (es gratis).
3. Confirma tu correo y anota tu **nombre de usuario** de GitHub. Se lo vas a mandar a tu facilitador.

**DESPUÉS, instala Git.** Pega en claude.ai el prompt de tu sistema.

**Mac:**

```
Necesito instalar Git en mi Mac. Guíame paso a paso:
1. Primero dime cómo verificar si ya lo tengo (git --version en la Terminal).
2. Si no lo tengo, el comando es: xcode-select --install
   (las herramientas de línea de comandos de Apple: traen Git y también Python 3).
3. Verifica con git --version.
Si algo falla, ayúdame a resolverlo.
```

**Windows:**

```
Necesito instalar Git en mi PC con Windows. Guíame paso a paso:
1. Primero dime cómo verificar si ya lo tengo (git --version).
2. Si no lo tengo, el comando es: winget install --id Git.Git -e
   Si winget no funciona, dime cómo usar el instalador de https://git-scm.com/download/win
   Deja las opciones por defecto: instalan Git Bash, que voy a usar para todo.
3. Abre una ventana NUEVA de Git Bash desde el menú Inicio y verifica con git --version.
Si algo falla, ayúdame a resolverlo.
```

**Linux:** instala `git` con tu gestor de paquetes (por ejemplo `sudo apt install git`) y verifica con `git --version`.

## Paso 3 — Tu Terminal

La terminal es la ventana donde vas a trabajar con Claude Code.

- **Mac:** la app **Terminal** que viene con la Mac sirve. Si quieres una más cómoda, instala **Ghostty** (opcional) pegando esto en claude.ai:

  ```
  Quiero instalar Ghostty, una aplicación de terminal, en mi Mac. Guíame:
  1. Descárgala de ghostty.org.
  2. Instálala como cualquier app de Mac.
  3. Ábrela y verifica que funciona.
  Si algo falla, ayúdame a resolverlo.
  ```

  Desde aquí, «terminal» es Terminal o Ghostty, la que hayas elegido.
- **Windows:** tu terminal es **Git Bash** (del Paso 2). PowerShell se usa sólo en el Paso 4.
- **Linux:** tu terminal de siempre.

## Paso 4 — Claude Code

Claude Code es la versión de Claude que corre en tu terminal. Lee tus archivos, escribe código, arma reportes y automatiza tareas. Aquí pasa el trabajo de verdad.

**Mac o Linux:** abre tu terminal y pega esto en claude.ai:

```
Necesito instalar Claude Code (la herramienta de Anthropic para la terminal). Guíame paso a paso:
1. Usa el instalador nativo de Anthropic: curl -fsSL https://claude.ai/install.sh | bash
   (No necesita Homebrew ni sudo, y se actualiza solo.)
2. Verifica con: claude --version
   Si no encuentra el comando, ayúdame a confirmar que ~/.local/bin está en mi PATH.
3. Guíame para iniciar sesión con mi cuenta de Claude.
Si algo falla, ayúdame a diagnosticarlo.
```

> **Por qué el instalador nativo:** es lo que recomienda la documentación de Anthropic, y se
> mantiene al día solo. Una instalación con Homebrew **no** se actualiza sola, así que te quedarías
> sin darte cuenta en una versión vieja.

**Windows:** Claude Code se instala desde **PowerShell** (no desde Git Bash ni desde CMD). Git para Windows (Paso 2) ya tiene que estar instalado. Pega esto en claude.ai:

```
Necesito instalar Claude Code (la herramienta de Anthropic para la terminal) en Windows. Guíame paso a paso:
1. En PowerShell, el comando es: irm https://claude.ai/install.ps1 | iex
2. IMPORTANTE: lee conmigo la salida del instalador antes de cerrar la ventana. Puede terminar
   bien y aun así decir que NO agregó C:\Users\YOUR-USER\.local\bin a mi PATH.
   Si lo dice, guíame para agregar esa carpeta a Path en Variables de entorno
   (Variables del sistema, o Variables de usuario si no tengo permisos de administrador). No uses setx.
   Después abro una ventana NUEVA.
3. Abre una ventana NUEVA de Git Bash y verifica con: claude --version
   Si sale "'claude' no se reconoce", casi seguro es el PATH del punto anterior: arréglalo primero.
4. Guíame para iniciar sesión con mi cuenta de Claude.
Si algo falla, ayúdame a diagnosticarlo.
```

**Verifica con Claude.** Desde ahora Claude Code puede comprobar su propio trabajo. En tu terminal (Git Bash en Windows), escribe `claude`, responde **Sí** si te pregunta si confías en la carpeta, y pega:

```
Corre git --version y claude --version. Dime LISTO o FALTA para cada uno, nada más.
```

> **Desde aquí puedes elegir dónde pegar los prompts de instalación:** en claude.ai (tú corres los
> comandos) o en Claude Code (Claude los corre y te pide permiso antes de cada uno). Una excepción:
> los **inicios de sesión** (`gh auth login`, el de Claude) hacen preguntas en pantalla que Claude no puede
> contestar, así que esos los corres tú, en otra ventana de terminal.

## Paso 5 — `gh` y tu Sesión en GitHub

**Obligatorio.** Durante la sesión Claude usa `gh` para crear tu repositorio **privado** en GitHub. Inicias sesión desde el navegador. No hay ningún token que copiar ni guardar.

**Mac:**

```
Necesito instalar GitHub CLI (gh) en mi Mac e iniciar sesión. Guíame paso a paso:
1. Si tengo Homebrew (brew --version responde), el comando es: brew install gh
   Si no lo tengo, dime cómo usar el instalador para macOS (.pkg) de https://cli.github.com
2. Verifica con: gh --version
3. Inicia sesión con: gh auth login --hostname github.com --git-protocol https --web
   Me muestra un código de un solo uso y abre el navegador: dime dónde pego el código y qué estoy autorizando.
4. Verifica con: gh auth status
   Tiene que decir que tengo sesión iniciada en github.com con mi usuario.
Si algo falla, ayúdame a resolverlo.
```

**Windows:**

```
Necesito instalar GitHub CLI (gh) en Windows e iniciar sesión. Guíame paso a paso:
1. El comando es: winget install --id GitHub.cli -e
   Si winget no funciona, dime cómo usar el instalador .msi de https://cli.github.com
2. Abre una ventana NUEVA de Git Bash y verifica con: gh --version
3. Inicia sesión con: gh auth login --hostname github.com --git-protocol https --web
   Me muestra un código de un solo uso y abre el navegador: dime dónde pego el código y qué estoy autorizando.
4. Verifica con: gh auth status
   Tiene que decir que tengo sesión iniciada en github.com con mi usuario.
Si algo falla, ayúdame a resolverlo.
```

**Linux:** instala `gh` (https://github.com/cli/cli/blob/trunk/docs/install_linux.md), después `gh auth login --hostname github.com --git-protocol https --web` y verifica con `gh auth status`.

Si en tu computadora no se puede instalar `gh` (por ejemplo, una laptop de la empresa bloqueada), avísale a tu facilitador **antes** de la sesión. Hay un camino sólo con el navegador, pero toma más tiempo y tu facilitador tiene que saberlo con anticipación. **No** crees un «personal access token» para salir del paso.

**Verifica con Claude:**

```
Corre gh --version y gh auth status. Dime LISTO si tengo sesión iniciada en github.com, FALTA si no.
No corras tú el inicio de sesión.
```

## Paso 6 — Python 3

**Mac:** casi siempre quedó instalado con el Paso 2. Pega esto en claude.ai (o en Claude Code):

```
Necesito comprobar que tengo Python 3 en mi Mac. Guíame:
1. En la terminal: python3 --version
2. Si responde con una versión 3.x, listo.
3. Si no responde, o me ofrece instalar las herramientas de desarrollo, acepto. Si aun así no aparece,
   instálalo con brew install python (si tengo Homebrew) o con el instalador de https://www.python.org/downloads/
4. Vuelve a verificar con python3 --version
Si algo falla, ayúdame a resolverlo.
```

**Windows:**

```
Necesito instalar Python 3 en Windows. Guíame paso a paso:
1. Primero verifica si ya lo tengo: en Git Bash, py --version
2. Si no lo tengo, el comando es: winget install --id Python.Python.3.12 -e
3. Abre una ventana NUEVA y verifica con: py --version
   En Windows Python se llama con py. Si python3 abre la Microsoft Store, ignóralo: es un atajo de Windows, no Python.
Si algo falla, ayúdame a resolverlo.
```

**Linux:** `sudo apt install python3` (o tu gestor de paquetes), y después `python3 --version`.

**Verifica con Claude:**

```
Corre python3 --version (en Windows: py --version). Dime LISTO si es la versión 3.x, FALTA si no.
```

## Paso 7 — jq (chiquito, pero la sesión depende de él)

macOS 15 y posteriores ya traen `jq`; los macOS más viejos y Windows no, y Git para Windows tampoco lo incluye. Revisa con `jq --version` e instálalo ahora si falta.

**Mac:**

```
Necesito instalar jq (una herramienta chiquita de línea de comandos para JSON) en mi Mac. Guíame paso a paso:
1. Si tengo Homebrew (brew --version responde), el comando es: brew install jq
2. Si no lo tengo: dime qué chip tengo (uname -m: arm64 = Apple Silicon, x86_64 = Intel),
   crea ~/.local/bin si no existe, descarga el archivo que corresponde de
   https://github.com/jqlang/jq/releases/latest (jq-macos-arm64 o jq-macos-amd64) a ~/.local/bin/jq,
   hazlo ejecutable (chmod +x) y asegúrate de que ~/.local/bin quede en mi PATH para siempre.
3. Verifica con: jq --version
Si algo falla, ayúdame a resolverlo.
```

**Windows:**

```
Necesito instalar jq (una herramienta chiquita de línea de comandos para JSON) en Windows. Guíame paso a paso:
1. El comando es: winget install --id jqlang.jq -e
2. Abre una ventana NUEVA de Git Bash para que se actualice el PATH.
3. Verifica con: jq --version
Si algo falla, ayúdame a resolverlo.
```

**Linux:** `sudo apt install jq`, y después `jq --version`.

**Verifica con Claude:**

```
Corre jq --version. Dime LISTO o FALTA.
```

## Paso 8 — Obsidian

Obsidian es una app de notas que se convierte en tu «segundo cerebro»: el lugar donde tus proyectos, tus ideas y todo lo que creas con IA viven y se conectan entre sí.

Pega esto en claude.ai:

```
Necesito instalar Obsidian en mi computadora. Pregúntame qué sistema operativo uso si te hace falta.
Guíame paso a paso:
1. Dime de qué página descargarlo (obsidian.md).
2. Explícame cómo instalarlo en mi sistema.
3. Cuando esté instalado, sólo verifica que abre.
4. NO crees ningún vault: lo crea el pre-vuelo, en el último paso.
Si algo falla, ayúdame a resolverlo.
```

**Verifica:** Obsidian abre. Si te muestra una pantalla de bienvenida que ofrece crear una bóveda, ciérrala. **No crees tú ningún vault.**

## Paso 9 — Transcripción de Reuniones (opcional, cualquier herramienta)

Después de la sesión puedes convertir reuniones en minutas con Claude. Necesitas la reunión en texto, y sirve cualquiera de estas opciones:

- **Granola** (granola.ai), un grabador de reuniones con IA. Sirve cualquier correo. En la pantalla de entrada usa **Continue with Google** (o Microsoft), no el botón de **SSO**, que es sólo para cuentas empresariales.
- **Otra herramienta de transcripción** que ya uses (Zoom, Teams, Meet, Otter y otras).
- **Ninguna herramienta.** Le pegas la transcripción a Claude a mano.

Dile a tu facilitador cuál vas a usar. Nada de esto bloquea la sesión.

> **Grabar necesita consentimiento.** Graba una reunión sólo cuando todos los presentes estén de acuerdo. Tu facilitador te va a preguntar antes de grabar tu sesión, y puedes decir que no.

Si eliges Granola, este prompt te guía (pégalo en claude.ai):

```
Necesito instalar Granola (granola.ai), un grabador de reuniones con IA. Guíame paso a paso:
1. Dime a qué página ir y cómo instalarlo en mi computadora.
2. Ayúdame a crear la cuenta con "Continue with Google" o Microsoft (no con SSO).
3. Conecta mi calendario y verifica que aparecen mis reuniones.
4. Grabemos 30 segundos de mí hablando y confirma que genera una transcripción y un resumen.
Si algo falla, ayúdame a diagnosticarlo.
```

---

## Paso 10 — El Pre-Vuelo (obligatorio)

El pre-vuelo deja tu computadora lista para la sesión en unos 10 minutos. Claude Code:

- crea tu vault en un lugar seguro (nunca dentro de una carpeta sincronizada con la nube como OneDrive, Dropbox, Google Drive o iCloud),
- te pide abrirlo en Obsidian y comprueba que Obsidian abrió **esa misma carpeta**,
- mueve tus archivos del kit al vault y practica cargar un prompt **por archivo**,
- comprueba cada herramienta y tu sesión de GitHub,
- termina con **una línea** que le mandas a tu facilitador.

**Antes de empezar:** terminaste los Pasos 1 a 8. Tu facilitador te mandó estos archivos del kit: este documento, el **Main Setup Prompt** y el **Skills & Config Setup Prompt** (en Windows, sus ediciones para Windows `02W` y `03W`), y el Doc 07 — Vocabulario. Guárdalos todos en tu carpeta de **Descargas** y no les cambies el nombre, no los abras ni los muevas. El pre-vuelo los mueve.

**Cómo se corre.** El prompt largo de abajo no lo pegas. Le dices a Claude que lo lea de este archivo:

1. Abre tu terminal (en Windows: **Git Bash**) y escribe `claude`. Si te pregunta si confías en la carpeta, elige **Sí**.
2. Pega este prompt corto (en Windows: clic derecho para pegar) y presiona Enter:

   ```
   Lee el archivo de mi carpeta de Descargas cuyo nombre contiene "Pre-Session Setup Instructions". Busca la sección "PROMPT DE PRE-VUELO" y sigue sólo las instrucciones de su bloque de código.
   ```

3. Contesta lo que Claude te pregunte. La **última línea** de Claude dice `PREFLIGHT: READY …` o `PREFLIGHT: MISSING …`.

Si Claude no encuentra el archivo (por ejemplo, lo guardaste en otro lado), arrastra el archivo a la ventana de la terminal: eso pega su ruta. Después escribe `Lee este archivo, busca la sección "PROMPT DE PRE-VUELO" y sigue sólo las instrucciones de su bloque de código.` Como último recurso en Mac o Linux, copia el bloque de abajo y pégalo.

> **La última línea va en inglés a propósito** (`PREFLIGHT: READY` = listo, `PREFLIGHT: MISSING` = falta, `ACCOUNT: personal/team` = cuenta personal o de equipo). Así tu facilitador la lee igual en cualquier idioma del kit, como el chequeo de estado.

### PROMPT DE PRE-VUELO

```
PRE-VUELO — AI Acceleration Club Fase 0

Hola, Claude. Me estoy preparando para mi sesión de inicio con Claude Code. Vamos a hacer un pre-vuelo: dejar listo mi vault de Obsidian y comprobar mis herramientas. Háblame en español. Ve en orden, un punto a la vez, y espérame cuando un punto me necesite. No instales nada ni cambies ninguna configuración sin preguntarme antes. Nunca leas, muestres ni me pidas una contraseña, un token o una llave.

0. MI COMPUTADORA
   - Dime qué sistema detectas: macOS, Windows (Git Bash), WSL o Linux.
   - En Windows: corre los comandos en Git Bash, escribe las rutas con barras / (C:/Users/...), nunca con \, y muéstrame las rutas con pwd -W en vez de pwd.

1. MI VAULT (la carpeta que se convierte en mi segundo cerebro)
   - Pregúntame si ya tengo un vault de Obsidian que quiera usar. Si sí, pídeme su ruta completa y usa esa carpeta: no crees otra.
   - Si no, créalo como AIAC-Vault directamente dentro de mi carpeta de usuario: $HOME/AIAC-Vault (en Windows es C:/Users/YOUR-USER/AIAC-Vault). Pregúntame sólo si quiero otro nombre; uno sin espacios es lo más fácil.
   - REGLA DURA: el vault nunca puede vivir dentro de una carpeta sincronizada con la nube. Si la ruta completa contiene OneDrive, Dropbox, Google Drive, GoogleDrive, My Drive, iCloud o Mobile Documents, no la uses: dime por qué y propón $HOME/AIAC-Vault. Tampoco lo pongas en Documentos ni en el Escritorio: en Windows muchas veces están redirigidos a OneDrive, y en Mac pueden estar sincronizados con iCloud.
   - Crea sólo la carpeta del vault y, dentro, "00 HUB/00 INBOX". Nada más: el Main Setup Prompt arma el resto durante la sesión. Si alguna carpeta ya existe, déjala como está.
       mkdir -p "$HOME/AIAC-Vault/00 HUB/00 INBOX" && cd "$HOME/AIAC-Vault" && pwd
     (En Windows usa pwd -W. Si elegí otra ruta u otro nombre, usa ésos.)
   - Muéstrame la ruta completa del vault. La voy a necesitar en la sesión.

2. OBSIDIAN ABRE LA MISMA CARPETA
   - Dime que abra Obsidian y elija «Abrir carpeta como bóveda» (en inglés, «Open folder as vault»), y que seleccione la carpeta del punto 1. Si Obsidian ya tiene una bóveda abierta, se llega por el ícono de bóvedas abajo a la izquierda: «Administrar bóvedas» y después «Abrir carpeta como bóveda». NUNCA «Crear nueva bóveda»: eso hace un segundo vault en otro lugar.
   - Espera a que te diga «listo». Después comprueba que dentro de la carpeta del vault apareció la carpeta oculta .obsidian (ls -a). Si no aparece, Obsidian abrió otra carpeta: repitamos el punto 2.

3. MIS ARCHIVOS DEL KIT Y CARGAR UN PROMPT POR ARCHIVO
   - Busca en mi carpeta de Descargas los archivos del kit que me mandó mi facilitador: los que tienen en el nombre "Pre-Session Setup Instructions", "Main Setup Prompt", "Skills & Config Setup Prompt" o "Vocabulario". Si hay más de una copia de un archivo (por ejemplo con «(1)» en el nombre), toma la más reciente y dime cuál tomaste.
   - Muévelos a "00 HUB/00 INBOX" del vault, quitando cualquier «(1)» del nombre. Si no está el Main Setup Prompt o el Skills & Config Setup Prompt, sigue y anota «archivos del setup» como falta.
   - Muéstrame lo que quedó en "00 HUB/00 INBOX".
   - Ahora practiquemos cómo se cargan los prompts largos en la sesión. Dime que en Obsidian abra "00 HUB/00 INBOX", haga clic derecho sobre el archivo del Main Setup Prompt (o sobre este archivo Pre-Session si falta el del setup), elija «Copiar ruta» y después la ruta completa del sistema (no la «URL de Obsidian»), y que la pegue aquí. Comprueba que esa ruta es la del archivo (test -f). En Windows, cambia las \ por / antes de probarla. NO ejecutes ese archivo ahora: sólo comprobamos que la ruta sirve.

4. MIS HERRAMIENTAS
   Corre esto y muéstrame qué salió en cada línea:
     git --version
     gh --version
     gh auth status
     python3 --version     (en Windows: py --version)
     jq --version
     claude --version
   - gh auth status tiene que decir que tengo sesión iniciada en github.com. Si no lo dice, NO corras tú el inicio de sesión: hace preguntas en pantalla que desde aquí no puedes contestar. Dime que corra esto en OTRA ventana de terminal, que siga lo que pide el navegador y que te avise cuando termine:
       gh auth login --hostname github.com --git-protocol https --web
     Después vuelve a correr gh auth status.
   - Cuando tenga la sesión iniciada, corre gh api user --jq .login y muéstrame mi nombre de usuario de GitHub. Se lo voy a mandar a mi facilitador.
   - En Windows Python se llama con py. Si python3 abre la Microsoft Store, ignóralo: es un atajo de Windows, no Python.
   - Si algo no está instalado, dime qué paso de mis Instrucciones de Configuración Pre-Sesión lo instala y espera. Cuando te diga que terminé, vuelve a comprobarlo; lo recién instalado a veces necesita una ventana de terminal nueva. Si sigue sin aparecer, anótalo como falta.
   - El tipo de mi cuenta de Claude. Corre esto; muestra sólo el tipo de cuenta, nada más:
       grep -o '"organizationType": *"[^"]*"' "$HOME/.claude.json"
     claude_team o claude_enterprise significa una cuenta de equipo: el administrador de mi organización decide qué conectores veo y puede repartir plugins. Cualquier otra cosa, o nada, significa una cuenta personal. Ninguna de las dos es un problema.

5. TRANSCRIPCIÓN DE REUNIONES (nunca es una falta)
   - Pregúntame cómo voy a capturar mis reuniones después de la sesión: Granola, otra herramienta de transcripción, o pegando la transcripción a mano. Cualquier respuesta sirve. Sólo anótala.

6. RESUMEN
   - Dame una tabla con cada punto y LISTO o FALTA: vault (no está en una carpeta sincronizada), Obsidian abrió la misma carpeta (.obsidian encontrada), archivos del setup en el INBOX, «Copiar ruta» funciona, git, gh, gh con sesión iniciada, Python 3, jq, Claude Code. Agrega una fila «cuenta de Claude» (personal o de equipo), una fila «usuario de GitHub» y una fila «transcripción» con mi respuesta.
   - Debajo de la tabla, la línea que voy a usar en la sesión para entrar a mi vault: cd "<ruta completa del vault>"
   - Termina con UNA línea exacta, en inglés, sin nada después:
       PREFLIGHT: READY · ACCOUNT: personal
     si todo está listo, o
       PREFLIGHT: MISSING <lo que falta, separado por comas> · ACCOUNT: personal
     por ejemplo: PREFLIGHT: MISSING jq, gh login · ACCOUNT: team
     Escribe team en vez de personal si la cuenta es Team o Enterprise.
```

### Después del Pre-Vuelo

- **Manda la última línea** (`PREFLIGHT: READY …` o `PREFLIGHT: MISSING …`) y tu **usuario de GitHub** a tu facilitador por [SET: your support channel]. Si dice `MISSING`, pide ayuda de una vez, **antes** de la sesión. Lo que falta se arregla en minutos ahora y en media hora en vivo.
- **Guarda la línea `cd "…"`** que te dio Claude. En la sesión la usas para entrar a tu vault.
- **No crees otro vault.** Si Obsidian no muestra el tuyo, ábrelo otra vez con **Abrir carpeta como bóveda**.
- En la sesión, los prompts largos se **cargan por archivo**, igual que acabas de practicar: en Obsidian, clic derecho sobre el archivo → **Copiar ruta**; en Claude Code, `Lee el archivo <ruta> y sigue sus instrucciones.`

### Si tu Facilitador te Pide el Chequeo de Estado

Tu facilitador también te puede mandar `aiac-status-check.sh` (muchas veces como `aiac-status-check.sh.txt`, porque las apps de chat y el correo bloquean los archivos `.sh`). Es un script chiquito de **sólo lectura**: no instala nada, no cambia nada y no envía nada. Sólo mira e imprime un reporte. Guárdalo en Descargas y dile a Claude, con el **nombre exacto del archivo que recibiste**:

```
Corre `bash ~/Downloads/aiac-status-check.sh.txt --share` y muéstrame su salida tal cual como se imprime.
```

(Si tu archivo se llama `aiac-status-check.sh`, usa ese nombre; los dos funcionan.) **`--share` importa:** con esa opción el script imprime sólo el bloque que empieza con `----- AIAC STATUS (safe to share) -----` y termina con `----- END -----`, así que nada más sobre tu máquina entra en la conversación con Claude. Ese bloque trae nombres de chequeos y `DONE` (hecho) / `NOT DONE` (falta) / `SKIPPED (optional)` (opcional, omitido) más una línea de veredicto, nada personal, y es lo único que compartes. El script imprime en inglés a propósito. El primer `NOT DONE` es donde retomas.

¿Quieres el reporte completo, con el detalle de cada línea? Córrelo **tú en una ventana de terminal** (Git Bash en Windows), no a través de Claude: `bash ~/Downloads/aiac-status-check.sh.txt`. Ese detalle es sólo para tus ojos; nunca se lo pegues a Claude ni a nadie, y nunca compartas la salida de `--details`. Si Claude Code todavía no funciona, corre ese mismo comando en tu terminal y copia sólo el bloque entre las dos líneas `-----`.

---

## Llega con un Proyecto Concreto

No llenas ningún formulario. En cambio, llega a la sesión con **un proyecto concreto de tu trabajo real** en el que quieras que Claude te ayude. Si dudas, trae dos o tres candidatos y elegimos uno juntos.

«Concreto» quiere decir que puedes nombrar tres cosas:

- **La entrada:** un archivo, una exportación o un reporte que ya tienes (una hoja de cálculo, PDFs, una exportación de un sistema).
- **La salida que quieres:** un reporte, un resumen, una tabla limpia, un borrador, un análisis.
- **Por qué importa:** el tiempo que te cuesta hoy, o la decisión que te ayudaría a tomar.

Ejemplos del tipo de cosa que funciona bien:

- «Armo el mismo reporte a mano todos los meses y me toma horas.»
- «Tengo datos en un sistema que no puedo cruzar fácilmente con otro.»
- «Necesito analizar algo pero no tengo las herramientas adecuadas.»
- «Mi equipo coordina un proceso y la información se pierde por el camino.»

«Aprender IA» o «ser más productivo» todavía no es un proyecto. Bájalo a una tarea concreta que de verdad vayas a repetir.

**Trae datos de muestra, no datos confidenciales.** Para el primer ejercicio, usa una copia sin nombres ni montos, un pedacito, o filas inventadas que se parezcan a las reales. Usa datos reales del negocio sólo cuando tu empresa haya aprobado usar Claude con ellos.
