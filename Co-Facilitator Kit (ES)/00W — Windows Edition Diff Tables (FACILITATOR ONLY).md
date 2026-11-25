---
title: "Edición Windows — Tablas de Diferencias (Solo Facilitador)"
created: 2026-08-19
category: reference
status: active
tags: [aiac, phase0, co-facilitator-kit, windows, facilitator, diff]
related: ["[[README — Kit Index & How to Use]]"]
lang: es
translated_from: "00W — Windows Edition Diff Tables (FACILITATOR ONLY).md"
---

> # 🚨 NO SE LO ENVÍES A UN PARTICIPANTE
>
> Los participantes le entregan los documentos de configuración a Claude Code por su ruta (*"Lee el
> archivo … y sigue sus instrucciones"*) — Claude lee el archivo **completo**, así que cualquier cosa
> añadida a un documento se leería como instrucciones. Este archivo existe **por separado** para que las
> variantes de Windows queden auditables sin colarse en la configuración de nadie.
>
> Patrón tomado de Mangan, que casi pierde sus propias tablas de diferencias dentro del copy-paste de un alumno.

# Edición Windows — qué cambió y por qué

**Principio: variantes, no bifurcaciones.** Cada documento de Windows es el documento EN más un conjunto
listado de cambios. Eso significa que cada desviación se puede revisar, cuestionar o revertir, y la edición
nunca se desvía en silencio del kit.

| Documento | Estado |
|---|---|
| `01 — Pre-Session Setup Instructions` | **Compartido** — sin variante de Windows. Ya estaba ramificado por sistema operativo; la sección de Windows se reforzó en el mismo sitio (5 añadidos abajo). |
| `02W — Main Setup Prompt (Windows)` | Variante — **18 cambios** |
| `03W — Skills & Config Setup Prompt (Windows)` | Variante — **10 cambios** |
| `04 — Next Steps Brief` | **Compartido, sin cambios.** Material de lectura; no se ejecuta nada específico del sistema operativo. |
| `02-S — Sandbox Setup` | **Compartido; en Windows, solo con WSL2.** Windows nativo no tiene sandbox; funciona con Claude Code corriendo dentro de una distribución WSL2 (Parte 2 del 02-S), donde aplican las instrucciones de Linux. |

## Las cuatro minas que esta edición existe para desactivar

Verificadas contra la documentación viva de Anthropic, y luego contra una máquina Windows real.

1. ⛔ **Claude Code no funciona en el plan gratuito** — la documentación, textual: *"The free Claude.ai plan does
   not include Claude Code access."* Convertido en la compuerta cero del Documento 01. Se resuelve solo: si
   `claude` abre con la sesión iniciada, la mejora de plan ya ocurrió.
2. **Las rutas con barra invertida fallan *en silencio* en Git Bash.** Una `\` sin comillas se elimina y
   *"el comando falla sin error visible"*. Una ruta `C:\` en el router lo rompe **y se ve idéntico al clásico
   bug de perfil-vs-router**, así que estarías depurando lo que no es. Tres defensas: `pwd -W`, una compuerta
   `grep -c '\\'` que debe dar 0 después de escribir el router, y decirle la regla a Claude por adelantado.
3. **La statusline personalizada puede que nunca se renderice** en Windows + Git Bash
   ([claude-code#66455](https://github.com/anthropics/claude-code/issues/66455)). Lleva un plan alterno de
   3 pasos y un **límite de pérdida de 3 minutos**, hecho seguro por el replanteamiento que sí importa:
   **la barra es solo la pantalla — el override de 75% y los dos *hooks* son la protección de verdad**,
   y ninguno depende de ella.
4. **`python3` normalmente no es un comando en Windows** (es `python` o `py`; `python3` a secas abre la
   Microsoft Store) — **y la fusión de ajustes del STEP 3 del Documento 02 y el STEP 7 del Documento 03,
   la verificación final del kit, ejecutan Python.** Escritos con `python3`, los dos fallan en Windows por
   una razón que no tiene nada que ver con la configuración.

## Documento 01 — reforzado en el mismo sitio (5 añadidos)

| # | Añadido | Por qué |
|---|---|---|
| 1 | **Compuerta 0: el plan gratuito bloquea Claude Code** | Bloquea todo lo demás; un alumno de Mac estuvo trancado semanas por esto |
| 2 | **Compuerta 0.5: en qué ventana estoy** (tabla PowerShell vs Git Bash vs CMD) | Las capturas de error del alumno eran de CMD, sus documentos asumían PowerShell, y los bloques del kit necesitan Git Bash. Además: que `where bash` falle es lo esperado, no una instalación fallida |
| 3 | **Regla de la barra inclinada + `pwd -W`** | Mina #2 |
| 4 | **Verificación del PATH después del instalador** | El instalador oficial terminó y reportó en su propia salida que NO había añadido `.local/bin` al PATH → `'claude' is not recognized`, dos veces, a lo largo de una semana |
| 5 | **Banner "esto es prosa, no comandos"** | Prosa pegada en PowerShell produjo un `ParserError` y un prompt `>>` trancado — una comilla sin cerrar por el apóstrofo de *"you're"* |

## Documento 02W — 18 cambios frente a `02 — Main Setup Prompt (Participant)`

| # | Dónde | El kit dice | 02W dice | Por qué |
|---|---|---|---|---|
| 1 | Frontmatter | genérico | title/tags marcados como Windows | Descubribilidad |
| 2 | Encabezado | pasos de carga por archivo para todos los sistemas | **Tres reglas de Windows** (dar el archivo por su ruta, clic derecho para pegar líneas cortas · Git Bash · barras normales) | Las tres cosas que rompen las sesiones en Windows |
| 3 | Encabezado, cómo cargar | Finder / Explorador de archivos / copiar ruta en Linux | Solo **Copiar como ruta de acceso** del Explorador de archivos, más **Open Git Bash here** + `pwd -W` | Arranca Claude en la carpeta correcta desde el shell correcto |
| 4 | Encabezado, pregunta de confianza | "elige Yes" | añade: **en Windows la opción resaltada por defecto es "No, exit"** | La gente presiona Enter y Claude Code se cierra |
| 5 | Inicio de la sección para Claude | (ninguno) | **Declaración de entorno** (Windows, Git Bash, barras normales, nada de comandos de macOS) dentro del archivo | Elimina ~6 idas y vueltas de "detecta mi sistema operativo"; no hace falta un pegado aparte |
| 6 | Revisión de la ubicación del *vault* | `pwd`; ramas de sincronización en la nube para Windows y macOS | **`pwd -W`**; solo la rama de OneDrive de Windows (redirección de `Documents`/`Desktop`), por defecto `C:/Users/YOUR-USER/AIAC-Vault` | La redirección de OneDrive es la trampa de Windows; la rama de iCloud de macOS no aplica |
| 7 | Router, ruta del *vault* | `pwd` | **`pwd -W`** | `pwd` imprime `/c/Users/…`; el router necesita `C:/Users/…` |
| 8 | Verificación del router | releer 20 líneas | 25 líneas + **`grep -c '\\'` debe dar 0** | Atrapa una ruta con barra invertida antes de que rompa el router en silencio |
| 9 | *Hook* Stop del STEP 3 | `afplay …` | **beep de Windows ya incorporado** + una comprobación "¿lo escuchaste? / bórralo" | Se dispara en cada turno; una línea equivocada = un error en cada turno durante 90 min |
| 10 | Callout del STEP 3 | lista para elegir según el sistema operativo | Reescrito: no sustituyas por `afplay`; borra el bloque si no hay beep | Elimina la elección que produce la falla |
| 11 | Detección de SO + `jq` del STEP 3.5 | `uname`, líneas de instalación de `jq` por sistema | SO ya declarado; **`winget install jqlang.jq`** (no viene con Git for Windows) | Que falte `jq` es la falla común de Windows en las Capas 2–3 |
| 12 | Statusline del STEP 3.5 | una nota de Windows | **Bug conocido documentado + plan alterno de 3 pasos + límite de 3 min + el replanteamiento de "la barra es solo pantalla"** | Mina #3 |
| 13 | Sonido del STEP 3.5 | `afplay` en `statusline.sh` | **beep de Windows incorporado dentro del script**; nota reescrita | El único `afplay` genuinamente ejecutable del documento |
| 14 | STEP 4 | `xcode-select --install` | `winget install --id Git.Git -e` o git-scm.com/download/win, conservando Git Bash | Comando de macOS en una sesión de Windows |
| 15 | STEP 5 | revisión de `gh` | añade **`winget install --id GitHub.cli -e`** si falta | La misma vía de instalación que en los prerrequisitos |
| 16 | `~/dev` + revisión de ubicación del STEP 6 | redacción solo para Mac; comparación simple de rutas | añade la traducción `C:/Users/YOUR-USER/dev`; compara normalizando con **`cd … && pwd -P`** | Git imprime `C:/…` y Git Bash `/c/…` — un repo bien ubicado mostraría un falso `WRONG LOCATION` |
| 17 | `.gitignore` del STEP 7 | `.DS_Store` | añade `Thumbs.db`, `desktop.ini` | Equivalentes de Windows |
| 18 | Fusión de ajustes del STEP 3 + 3.5 | `python3 ~/.claude/aiac-merge-settings.py` | **`py`** (alternativa `python`, nunca `python3`); el plan alterno 3 de la statusline fija la ruta absoluta con `--replace statusLine.command` | Mina #4 — el script de fusión en sí es idéntico byte por byte |

## Documento 03W — 10 cambios frente a `03 — Skills & Config Setup Prompt (Participant)`

| # | Dónde | El kit dice | 03W dice | Por qué |
|---|---|---|---|---|
| 1–2 | Frontmatter + encabezado | genérico | title/tags de Windows; las tres reglas repetidas; copiar ruta en el Explorador de archivos + Open Git Bash here; declaración de entorno dentro del archivo | Una sesión nueva pierde el contexto del Documento 02W |
| 3 | Revisión del router del STEP 1 | releer 20 líneas, 2 comprobaciones | 25 líneas + **3ra comprobación: cero barras invertidas** | La comprobación que atrapa la mina #2 |
| 4 | Prueba de ruteo del STEP 1 | segunda ventana, confiar en `~/dev` | segunda ventana **como Git Bash**; la opción por defecto de confianza es "No, exit" | Las mismas dos trampas de Windows que en el Documento 02W |
| 5 | `lessons.md` del STEP 3 | vacío | sembrado con la regla de la barra inclinada | Pone la regla de Windows donde Claude la vuelve a leer cada sesión |
| 6 | ⭐ **STEP 7** | "Crea un script de Python … córrelo una vez" | **Detectar primero `py`/`python`/`python3`**; que falte Python es un hueco de prerrequisitos (línea de instalación del Doc 01, anotarlo para el facilitador), no un motivo para cortar la lista; ejecutar una vez con la aprobación normal, nunca agregarlo a `allow` | ⭐ Mina #4 — de lo contrario la comprobación final del kit falla en Windows por una razón ajena |
| 7 | STEP 7 | (ninguno) | comprobación silenciosa de validez JSON `jq .` sobre `settings.json`; sin `jq`, vale la revisión del punto 3, que ya lo parseó — nunca releer el archivo | Barato; atrapa una fusión corrompida del Documento 02W sin mostrar llaves |
| 8 | STEP 7 | (ninguno) | añade `claude doctor` | Lo primero que hay que correr cuando algo se rompa después |
| 9–10 | Chuleta del STEP 6 | neutral respecto al sistema | Bloque de notas de Windows (ventana · rutas · pegado · `claude doctor`) | Las cuatro cosas que van a olvidar para la semana que viene |

Retirado del kit en v0.2 (por eso ya no son filas de Windows): el ayudante de Granola con el token en caché (antiguo STEP 2.6b) y la instalación del CLI `gws` (antiguo STEP 2.5b, ahora "hoy no").

## Corrida de verificación (2026-11-25)

| Comprobación | 02W | 03W |
|---|---|---|
| Balance de bloques de código | ✅ 94 líneas de *fence*, balanceadas | ✅ 34 líneas de *fence*, balanceadas |
| Comandos de macOS dentro de bloques de código | ✅ 0 | ✅ 0 |
| Rutas `~/Library` dentro de bloques de código | ✅ 0 | ✅ 0 |
| `bash -n` sobre cada bloque bash | ✅ 23 limpios / 5 solo con marcadores (`<repo-name>`, `<file>`) — los mismos 5 que la línea base EN | ✅ 11 limpios, 0 fallando |
| El bloque `settings.json` parsea, el *hook* Stop desescapa correctamente | ✅ `powershell.exe -c "[console]::beep(1000,400)"` | n/a |
| Comillas tipográficas dentro de bloques de código | ✅ 0 | ✅ 0 |

**Nota sobre los permisos:** como el resto del kit, estas variantes usan el bloque de permisos
**acotado**. `allow` tiene solo comandos de solo lectura: comandos de git exactos (`git status`,
`git status --short`, `git diff`, `git log --oneline`, `git remote -v`) más `ls` y `wc` — ningún permiso
de escritura permanente, nada de `mkdir`. `ask` hace que `cat`, `head`, `tail`, `grep`, `git add`,
`git commit`, `git push` y `gh repo create` pregunten cada vez (Claude Code ejecuta comandos integrados de
solo lectura como `cat` sin pedir permiso salvo que una regla `ask` o `deny` los cubra). Ningún comodín de
git en `allow`, ningún intérprete (`python`, `py`, `python3`, `node`), nada de `pip install`, nada de
`Read`/`Write`/`Edit`/`Glob`/`Grep` a secas — y el bloque se fusiona en local con
`aiac-merge-settings.py`, que nunca imprime los valores existentes. El cambio del STEP 7
de Windows descrito arriba mantiene ese endurecimiento: ejecuta el saludo una sola vez con la aprobación
normal usando el comando de Python que existe de verdad, sin agregarlo a `allow`.
