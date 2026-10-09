---
title: "Instrucciones de Configuración Pre-Sesión (Participante) — AI Acceleration Club Fase 0"
created: 2026-07-14
category: reference
status: draft
tags: [aiac, phase0, co-facilitator-kit, participant, pre-session, setup]
lang: es
translated_from: "01 — Pre-Session Setup Instructions (Participant).md"
---

**Aplica a:** Antes de la sesión — lee esto unos días antes de tu sesión en vivo de Fase 0, y completa cada paso antes de llegar.

# Configuración Pre-Sesión — AI Acceleration Club Fase 0

Bienvenido a la Fase 0 del AI Acceleration Club. Antes de tu sesión en vivo, vas a necesitar instalar unas cuantas herramientas. Cada una cumple un rol específico en el sistema que vamos a construir juntos — para cada punto de abajo vas a encontrar una explicación de una línea de *por qué* la necesitas, más un prompt listo para pegar que le puedes entregar a Claude (en claude.ai) y que te va a guiar por la instalación y a resolver cualquier cosa que salga mal.

Vas a instalar 6 cosas si estás en Mac, o 5 si estás en Windows (en Windows te saltas la aplicación de terminal dedicada — la terminal que ya trae funciona bien).

> **Cuando estés ejecutando comandos en una terminal:** si te trancas en cualquier punto — un comando no funciona, ves un error, no sabes qué responder — copia **todo** lo que está en tu terminal (el comando que escribiste, la respuesta, el error completo) y pégalo de vuelta en la misma conversación de Claude. Claude lee la salida de tu terminal y te guía hasta el siguiente comando hasta que el paso funcione. Así es como avanzas sin quedarte trancado: tú eres los ojos y las manos, Claude es el cerebro.

> **Otra cosa que es normal:** cuando instales Granola, Obsidian o una aplicación de terminal, tu sistema operativo o tu navegador te puede advertir que la descarga viene de un "desarrollador no verificado" o marcarla como posible riesgo de seguridad. Esto es completamente normal y esperado con estas aplicaciones — no te alarmes. Simplemente sigue adelante: en Mac, clic derecho → Abrir sobre la aplicación, o permítela en Configuración del Sistema → Privacidad y Seguridad. Si tienes dudas, pega el mensaje de advertencia en Claude y él te confirma qué hacer.

## ¿Tu Computadora de Trabajo la Administra tu Empresa?

Si tu laptop de trabajo la administra el departamento de IT de tu empresa, por favor confirma con IT **antes de la sesión** que:

1. **Se puede instalar el CLI de Claude Code** — que `npm i -g @anthropic-ai/claude-code` no esté bloqueado.
2. **Se permite `git push` a github.com** — algunos firewalls corporativos bloquean el push por HTTPS a github.com.
3. **No hay bloqueo de DLP saliente** — que ninguna política de prevención de pérdida de datos esté bloqueando el HTTPS saliente hacia `api.anthropic.com`.

Si algo de esto está bloqueado, usa tu laptop personal para la Fase 0. Tu *vault* y tus proyectos son personales de todos modos — no es buena idea construir tu segundo cerebro en una computadora corporativa que IT puede borrar o a la que te puede revocar el acceso sin avisar.

## Solo Windows — Antes de Empezar

Si estás en Mac, salta al Paso 1. Si estás en Windows, trabaja **todos** estos puntos primero —
cada uno le ha costado tiempo real a un participante real.

> **Esta sección es prosa, no comandos.** Léela; no la pegues en una terminal. (Pegar prosa
> en PowerShell produce un `ParserError` y te puede dejar trancado en un prompt de continuación `>>` —
> un apóstrofe en una palabra abre una comilla que nunca cierra. Si eso pasa, presiona
> **Ctrl+C** y sigue adelante.)

**0. Claude Code no corre en el plan gratuito de Claude.** Esta es la compuerta cero y bloquea todo
lo demás. La documentación de Anthropic es explícita: *"El plan gratuito de Claude.ai no incluye acceso a Claude Code."*
Haz el Paso 1 (Pro o Max) **antes** de intentar instalar cualquier cosa. Se resuelve solo — si `claude` abre
y estás con sesión iniciada, la mejora del plan funcionó. Un participante de otra cohorte estuvo trancado semanas por
exactamente esto.

**0.5. Ten claro en cuál ventana estás escribiendo — esta es la confusión #1 en Windows.** Windows te da
tres, y no son intercambiables:

| Ventana | Para qué la usas |
|---|---|
| **PowerShell** | Instalar Claude Code (el comando `irm ... \| iex`) |
| **Git Bash** | **Todo lo demás en este kit.** Todos los bloques `bash` de los Docs 02/03 la necesitan. Viene con Git for Windows (Paso 3). |
| **CMD** (la caja negra `C:\>`) | Nada de aquí. Si tus mensajes de error empiezan con `C:\>`, estás en la ventana equivocada. |

También es normal y **no** es una instalación fallida: que `where bash` no devuelva nada. Git for Windows instala
Git Bash pero no pone `bash.exe` en tu PATH. Abre Git Bash desde el menú Inicio.

**1. GitHub CLI (`gh`) — opcional, no es requisito para la Fase 0.** `gh` es solo una comodidad para autenticarte con GitHub. Intenta instalarlo desde https://cli.github.com y verifícalo con `gh --version`. **Si la instalación falla** (Windows corporativo, sin permisos de administrador, DLP), eso no te bloquea — usa la vía de abajo, que no necesita permisos de administrador:
   - **Personal Access Token (PAT), 5 min:** github.com → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token (classic) → alcances `repo` + `workflow` → Generate. **Guarda el token** — no se muestra de nuevo.
   - **Git Credential Manager** (viene con Git for Windows): tu primer `git push` abre una ventana del navegador para iniciar sesión en GitHub y autorizar. Alternativa manual: cuando git te pida usuario/contraseña, usa tu nombre de usuario de GitHub y pega el PAT como contraseña.
   Si `gh` instala bien, perfecto. Si no, el PAT + el Credential Manager cubren todo — de cualquier forma no quedas bloqueado para la sesión.

**2. Permisos de administrador.** Asegúrate de que tu cuenta de Windows tenga permisos de administrador — los vas a necesitar para instalar Git, Claude Code y otros paquetes. Si no estás seguro, haz clic derecho en PowerShell → "Ejecutar como administrador". Si te pide una contraseña de administrador que no tienes, avísalo antes de la sesión.

**3. VPN — desactívala para estas URLs durante la instalación:**
   - claude.ai
   - github.com
   - obsidian.md

   Muchas VPNs corporativas bloquean estas URLs durante los inicios de sesión OAuth y las descargas de paquetes. Si tienes una VPN activa por defecto, desactívala temporalmente para los Pasos 2–5 de abajo, o pídele a IT que agregue estos tres dominios a la lista de permisos.

**4. Cómo pegar texto en la terminal de Windows.** En PowerShell y en Windows Terminal, Ctrl+V
muchas veces no funciona con bloques largos. Usa **clic derecho** (o el clic de la rueda del mouse).
Vas a necesitar esto en cada paso de abajo.

**5. Usa siempre barras hacia adelante `/` en las rutas de archivos — nunca barras invertidas `\`.**
Escribe `C:/Users/tu/Documents/Vault`, no `C:\Users\tu\Documents\Vault`. Esto importa más
de lo que parece: en Git Bash una `\` sin comillas se elimina en silencio y **el comando falla sin ningún
error visible** — y la falla resultante se ve idéntica a un problema que no tiene nada que ver, así que pasarías
la sesión depurando lo que no es. Cuando un documento te pida la ruta de tu *vault*, obténla con `pwd -W` (que
imprime `C:/Users/...`), no con `pwd` a secas (que imprime `/c/Users/...`).

---

## Paso 1 — Claude Pro ($20/mes mínimo; Max recomendado)

Claude es el asistente de IA que vas a usar para todo: piensa, escribe, analiza y te guía paso a paso. **Para qué sirve:** es el cerebro detrás de todo lo demás — cada paso que sigue depende de él, por eso va de primero.

El mínimo para empezar es el **plan Pro ($20/mes)**. Si esperas usarlo intensamente, se recomienda **Max ($100/mes)** — te da límites de uso más altos en el modelo más capaz, para que no te quedes corto a mitad de sesión. Puedes empezar en Pro y pasarte a Max después si lo necesitas.

Este paso es manual:

1. Ve a claude.ai
2. Settings → Billing → escoge "Pro" (mínimo) o "Max" (recomendado)
3. Completa el pago

> Si estás detrás de un firewall corporativo o una VPN que bloquea claude.ai, desactívala temporalmente para este paso, o pídele a tu equipo de IT que agregue el dominio a la lista de permisos.

## Paso 2 — Obsidian

Obsidian es una aplicación de notas que se convierte en tu "segundo cerebro". **Para qué sirve:** es donde tus proyectos, ideas y todo lo que generes con IA va a vivir y conectarse entre sí — todo en un solo lugar, siempre a la mano.

Una vez que tu plan de Claude esté activo, abre claude.ai y pega este prompt:

```
I need to install Obsidian on my computer. Ask me what OS I'm on if you need to.
Walk me through it step by step:
1. Tell me which URL to go to for the download
2. Explain how to install it for my OS
3. Once it's installed, just verify that it opens correctly
4. Don't create any vault yet — I'll do that with my facilitator during the session

If anything fails, help me troubleshoot it.
```

## Paso 3 — Git + Tu Cuenta de GitHub

Son dos cosas que van juntas pero no son lo mismo — vale la pena tener clara la distinción:

- **Git** es un programa que instalas en tu computadora. **Para qué sirve:** lleva el registro de cada cambio que haces en tus archivos, para que nunca pierdas trabajo y puedas devolverte si algo se rompe.
- **GitHub** es una cuenta gratuita en la nube (github.com). **Para qué sirve:** es donde ese trabajo se respalda y vive en línea — el lugar al que Claude Code sube tus proyectos para mantenerlos seguros y poder compartirlos. La vas a necesitar de todas formas, así que créala ahora aunque nunca la hayas usado.

**PRIMERO — crea tu cuenta de GitHub** (manual, 2 minutos):

1. Ve a https://github.com
2. Haz clic en "Sign up" y crea tu cuenta (es gratis)
3. Confirma tu correo y anota tu nombre de usuario de GitHub — se lo vas a compartir a tu facilitador antes de la sesión

**DESPUÉS — instala Git.** Pega este prompt en claude.ai:

```
I need to install Git on my computer.
Walk me through it step by step:
1. First check whether I already have it installed (tell me what command to run in the terminal)
2. If it's not installed, walk me through installing it for my OS
3. Verify the install was successful

If anything fails or you see an error, help me resolve it.
```

*(Los usuarios de Mac siguen al Paso 4. Los usuarios de Windows: salten al Paso 5.)*

## Paso 4 — Ghostty (solo Mac)

La terminal es la ventana donde vas a trabajar con Claude Code: tú escribes, él ejecuta. **Para qué sirve Ghostty:** es una aplicación de terminal moderna, rápida y limpia — mucho mejor que la que viene por defecto con tu Mac, y es donde va a correr todo lo de abajo.

Pega este prompt en claude.ai:

```
I need to install Ghostty on my Mac. It's a modern terminal application.
Walk me through it step by step:
1. Tell me how to download it (ghostty.org)
2. Install it like any other Mac app
3. Open it and verify that it works

If anything fails, help me troubleshoot it.
```

**Usuarios de Windows:** sáltense este paso — Windows Terminal o PowerShell funcionan bien para todo lo de abajo.

## Paso 5 — Claude Code

Claude Code es la versión de Claude que corre en tu terminal. **Para qué sirve:** lee tus archivos, escribe código, genera reportes y automatiza tareas — todo desde texto. Es el motor que hace el trabajo pesado; aquí es donde pasa el trabajo de verdad.

**Si estás en Mac** — abre Ghostty y pega este prompt en claude.ai:

```
I need to install Claude Code (Anthropic's CLI tool for the terminal).

Walk me through it step by step:
1. On Mac, use Anthropic's native installer: curl -fsSL https://claude.ai/install.sh | bash
   (No Homebrew, no sudo, and it auto-updates itself in the background.)
2. If that fails and I already have Homebrew, the fallback is: brew install --cask claude-code
   Tell me first that Homebrew installs do NOT auto-update, so I'd have to run
   `brew upgrade --cask claude-code` myself from time to time.
3. After installing, verify with: claude --version
   If the command isn't found, help me confirm ~/.local/bin is on my PATH.
4. If it asks for authentication, walk me through the login process

If anything fails, help me diagnose and resolve it.
```

> **Por qué el instalador nativo:** es lo que recomienda la propia documentación de configuración de Anthropic. Las
> instalaciones por Homebrew **no** se auto-actualizan, lo que significa que te irías quedando en silencio en una versión vieja.
> La instalación nativa se mantiene al día sola y no requiere Homebrew para nada.

**Si estás en Windows** — abre tu terminal y pega este prompt en claude.ai:

```
I need to install Claude Code (Anthropic's CLI tool for the terminal).

Walk me through it step by step:
1. On Windows the command is: irm https://claude.ai/install.ps1 | iex
   Run it in PowerShell (not CMD, not Git Bash).
2. Walk me through the process in PowerShell
3. IMPORTANT - read the installer's own output before closing the window. It can finish
   successfully and still tell you it did NOT add C:\Users\<me>\.local\bin to my PATH.
   If it says that, walk me through adding it (setx PATH) and then open a NEW window.
4. Open a NEW terminal window and verify with: claude --version
   If I get "'claude' is not recognized", it is almost certainly the PATH step above - fix that
   before anything else.
5. If it asks for authentication, walk me through the login process

If anything fails, help me diagnose and resolve it.
```

## Paso 5.5 — jq (pequeño, pero la sesión depende de él)

`jq` es una herramienta diminuta de línea de comandos para leer JSON. **Para qué sirve:** la barra de
estado del monitor de contexto que vas a construir durante la sesión está montada sobre él. No es opcional —
sin `jq` la barra simplemente nunca aparece, y la falla no te da ningún mensaje de error.
Ni macOS ni Windows lo traen, así que hay que instalarlo ahora.

**Si estás en Mac** — pega este prompt en claude.ai:

```
I need to install jq (a small command-line JSON tool) on my Mac, without Homebrew.

Walk me through it step by step:
1. First tell me which chip I have — Apple Silicon or Intel:
   run `uname -m` (arm64 = Apple Silicon, x86_64 = Intel)
2. Make the folder if it doesn't exist: mkdir -p ~/.local/bin
3. Download the matching binary:
   - Apple Silicon: curl -fsSL -o ~/.local/bin/jq https://github.com/jqlang/jq/releases/latest/download/jq-macos-arm64
   - Intel:         curl -fsSL -o ~/.local/bin/jq https://github.com/jqlang/jq/releases/latest/download/jq-macos-amd64
4. Make it executable: chmod +x ~/.local/bin/jq
5. Make sure ~/.local/bin is on my PATH, and help me add it permanently if it isn't
6. Verify with: jq --version

If anything fails, help me diagnose and resolve it.
```

**Si estás en Windows** — pega este prompt en claude.ai:

```
I need to install jq (a small command-line JSON tool) on Windows.

Walk me through it step by step:
1. The command is: winget install jqlang.jq
2. Open a NEW terminal window afterward so the PATH refreshes
3. Verify with: jq --version

If anything fails, help me diagnose and resolve it.
```

## Paso 6 — Granola

Granola es un grabador de reuniones con IA que se conecta a tu calendario y genera transcripción + resumen automáticamente. **Para qué sirve:** para que tu sesión de Fase 0 — y cada reunión después de esa — quede capturada y lista para procesar con Claude Code, sin que tengas que tomar notas a mano.

**Importante:** instala Granola antes de la sesión y déjalo abierto durante el tiempo que estén juntos para que grabe. Después vas a conectar la integración de Granola con Claude Code y a procesar esa grabación.

Sirve cualquier correo — Gmail personal, Google Workspace o una cuenta de Microsoft. (Había una restricción vieja sobre proveedores de correo gratuitos que ya fue eliminada; si lees lo contrario en algún lado, está desactualizado.) En la pantalla de inicio de sesión usa **"Continue with Google"** — el botón de **SSO** es una vía solo para empresas y termina en callejón sin salida para la mayoría.

Pega este prompt en claude.ai:

```
I need to install Granola.ai on my computer.
It's an AI meeting recorder.
Walk me through it step by step:
1. Tell me which URL to go to (granola.ai)
2. Download and install it for my OS
3. Create an account for me — any email works (personal Gmail, Google Workspace, or Microsoft). Use "Continue with Google", not the SSO button
4. Connect my calendar (Google Workspace or similar)
5. Verify that my calendar meetings show up
6. Test recording 30 seconds of me talking and confirm it generates a transcript and summary automatically

If anything fails, help me diagnose it.
```

## Paso 7 — Verificación Final

Una vez que todo lo de arriba esté instalado, abre tu terminal (Ghostty en Mac, o Windows Terminal / PowerShell en Windows), escribe `claude` y pega este prompt:

```
Verify that I have everything installed correctly for the AI Acceleration Club:
1. Git installed and working (git --version)
2. Obsidian installed
3. Claude Code working (you're already running here)
4. jq installed and working (jq --version)
Tell me what happened with each check, and give me a short summary I can send
to my facilitator listing each item as DONE or NOT DONE.
```

**Envíale ese resumen a tu facilitador.** Esta es la compuerta — sin ella no tenemos forma de saber
hasta dónde llegaste, y ha habido sesiones que empezaron a ciegas porque nunca llegó.

**¿Trancado, con dudas, o simplemente quieres verificar?** Pídele a tu facilitador
`aiac-status-check.sh` — un script pequeño de solo lectura que reporta exactamente hasta dónde llegó tu configuración.
No escribe nada, no instala nada y no envía nada; solo mira archivos que ya existen
e imprime un resumen. Ejecútalo en tu **terminal** (no dentro de Claude Code):

```bash
bash ~/Downloads/aiac-status-check.sh
```

Copia toda la salida de vuelta a tu facilitador. El primer `NOT DONE` es donde retomas.

Si tropiezas en algún paso, guarda la salida de la terminal — puedes retomar la resolución
del problema con Claude, o llevársela a tu facilitador.

---

## Ven Preparado Con Tus Problemas

No necesitas llenar ningún formulario ni enviar nada por adelantado. En vez de eso, ven a tu sesión con **1 a 3 problemas reales de tu trabajo** en los que te gustaría que Claude te ayude — problemas donde mejor automatización, mejor análisis o más velocidad harían una diferencia real.

Ejemplos del tipo de cosa que funciona bien:

- "Armo el mismo reporte a mano todos los meses y me toma horas."
- "Tengo datos en un sistema que no puedo cruzar fácilmente con otro."
- "Necesito analizar algo pero no tengo las herramientas adecuadas."
- "Mi equipo y yo coordinamos un proceso, y la información se sigue perdiendo por el camino."

No hace falta que sea técnico — solo describe el problema y por qué te importa. Durante la sesión, tú y tu facilitador van a escoger el que mejor encaje y lo van a construir juntos, en vivo, como tu primer proyecto real.
