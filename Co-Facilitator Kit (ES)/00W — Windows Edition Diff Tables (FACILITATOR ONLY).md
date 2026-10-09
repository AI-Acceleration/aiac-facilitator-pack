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
> Los documentos del participante le dicen que *"abra el archivo, seleccione todo, copie, pegue"* — cualquier
> cosa añadida a un documento termina pegada dentro de Claude Code junto con él. Este archivo existe
> **por separado** para que las variantes de Windows queden auditables sin viajar de contrabando en el
> portapapeles de alguien.
>
> Patrón tomado de Mangan, que casi pierde sus propias tablas de diferencias dentro del copy-paste de un alumno.

# Edición Windows — qué cambió y por qué

**Principio: variantes, no bifurcaciones.** Cada documento de Windows es el documento EN más un conjunto
listado de cambios. Eso significa que cada desviación se puede revisar, cuestionar o revertir, y la edición
nunca se desvía en silencio del kit.

| Documento | Estado |
|---|---|
| `01 — Pre-Session Setup Instructions` | **Compartido** — sin variante de Windows. Ya estaba ramificado por sistema operativo; la sección de Windows se reforzó en el mismo sitio (5 añadidos abajo). |
| `02W — Main Setup Prompt (Windows)` | Variante — **12 cambios** |
| `03W — Skills & Config Setup Prompt (Windows)` | Variante — **11 cambios** |
| `04 — Next Steps Brief` | **Compartido, sin cambios.** Material de lectura; no se ejecuta nada específico del sistema operativo. |
| `02-S — Sandbox Setup` | **No disponible en Windows.** Windows nativo no tiene sandbox; se requiere WSL2. |

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
   Microsoft Store) — **y el STEP 7 del Documento 03, la verificación final del kit, escribe y ejecuta un
   script de Python.** Tal como se despacha, la última comprobación del kit falla en Windows por una razón
   que no tiene nada que ver con la configuración.

## Documento 01 — reforzado en el mismo sitio (5 añadidos)

| # | Añadido | Por qué |
|---|---|---|
| 1 | **Compuerta 0: el plan gratuito bloquea Claude Code** | Bloquea todo lo demás; un alumno de Mac estuvo trancado semanas por esto |
| 2 | **Compuerta 0.5: en qué ventana estoy** (tabla PowerShell vs Git Bash vs CMD) | Las capturas de error del alumno eran de CMD, sus documentos asumían PowerShell, y los bloques del kit necesitan Git Bash. Además: que `where bash` falle es lo esperado, no una instalación fallida |
| 3 | **Regla de la barra inclinada + `pwd -W`** | Mina #2 |
| 4 | **Verificación del PATH después del instalador** | El instalador oficial terminó y reportó en su propia salida que NO había añadido `.local/bin` al PATH → `'claude' is not recognized`, dos veces, a lo largo de una semana |
| 5 | **Banner "esto es prosa, no comandos"** | Prosa pegada en PowerShell produjo un `ParserError` y un prompt `>>` trancado — una comilla sin cerrar por el apóstrofo de *"you're"* |

## Documento 02W — 12 cambios frente a `02 — Main Setup Prompt (Participant)`

| # | Dónde | El kit dice | 02W dice | Por qué |
|---|---|---|---|---|
| 1 | Frontmatter | genérico | title/tags marcados como Windows | Descubribilidad |
| 2 | Encabezado | (ninguno) | Tres reglas de Windows encima de la línea de pegado | Pegar con clic derecho · Git Bash · barras inclinadas |
| 3 | Preámbulo | (ninguno) | Una declaración de entorno de una línea para pegar primero | Elimina ~6 idas y vueltas de "detecta mi sistema operativo" en una sesión en vivo |
| 4 | Ruta del *vault* | `pwd` | **`pwd -W`** | `pwd` imprime `/c/Users/…`; el router necesita `C:/Users/…` |
| 5 | Verificación del router | `head -20` | `head -25` + **`grep -c '\\'` debe dar 0** | Atrapa una ruta con barra invertida antes de que rompa el router en silencio |
| 6 | *Hook* Stop del STEP 3 | `afplay …` | **beep de Windows ya incorporado** + una comprobación "¿lo escuchaste? / bórralo" | Se dispara en cada turno; una línea equivocada = un error en cada turno durante 90 min |
| 7 | Callout del STEP 3 | lista para elegir según el sistema operativo | Reescrito: no sustituyas por `afplay`; borra el bloque si no hay beep | Elimina la elección que produce la falla |
| 8 | STEP 4 | `xcode-select --install` | git-scm.com/download/win, aceptar Git Bash | Comando de macOS en una sesión de Windows |
| 9 | `.gitignore` del STEP 7 | `.DS_Store` | añade `Thumbs.db`, `desktop.ini` | Equivalentes de Windows |
| 10 | `~/dev` | redacción solo para Mac | añade la traducción `C:\Users\…\dev` | Para que después lo consigan en el Explorador de archivos |
| 11 | Statusline del STEP 3.5 | una nota de Windows | **Bug conocido documentado + plan alterno de 3 pasos + límite de 3 min + el replanteamiento de "la barra es solo pantalla"** | Mina #3 |
| 12 | Sonido del STEP 3.5 | `afplay` en `statusline.sh` | **beep de Windows incorporado dentro del script**; nota reescrita | El único `afplay` genuinamente ejecutable del documento |

## Documento 03W — 11 cambios frente a `03 — Skills & Config Setup Prompt (Participant)`

| # | Dónde | El kit dice | 03W dice | Por qué |
|---|---|---|---|---|
| 1–2 | Frontmatter + encabezado | genérico | title/tags de Windows; las tres reglas repetidas; declaración de entorno | Una sesión nueva pierde el contexto del Documento 02 |
| 3 | STEP 1 | `head -20`, 2 comprobaciones | `head -25` + **3ra comprobación: cero barras invertidas** | La comprobación que atrapa la mina #2 |
| 4 | Granola del STEP 2.6b | `~/Library/Application Support/Granola/` + launchd/cron | `%APPDATA%\Granola\` (`~/AppData/Roaming/…`) + **Programador de tareas de Windows**, y "confirma los nombres de archivo reales, no asumas la estructura de Mac" | Opcional/diferido, pero las rutas de Mac sencillamente no existen |
| 5 | `gws` del STEP 2.5b | `~/bin/gws`, `chmod +x`, perfil de zsh | `~/bin/gws.exe`, windows-amd64, línea de PATH en `~/.bashrc` | Las instrucciones de Mac eran inejecutables |
| 6 | `lessons.md` del STEP 3 | vacío | sembrado con la regla de la barra inclinada | Pone la regla de Windows donde Claude la vuelve a leer cada sesión |
| 7 | ⭐ **STEP 7** | "Crea un script de Python … y ejecútalo" | **Detectar primero `python`/`py`/`python3`**; que falte Python explícitamente NO es un bloqueo; añadir el comando real a `allow` | ⭐ Mina #4 — de lo contrario la comprobación final del kit falla en Windows por una razón ajena |
| 8 | STEP 7 | 8 comprobaciones | añade la comprobación de validez JSON `jq .` sobre `settings.json` | Barato; atrapa una fusión corrompida del Documento 02 |
| 9 | STEP 7 | (ninguno) | añade `claude doctor` | Lo primero que hay que correr cuando algo se rompa después |
| 10–11 | Chuleta del STEP 6 | neutral respecto a Mac | Bloque de notas de Windows (ventana · rutas · pegado · `claude doctor`) | Las cuatro cosas que van a olvidar para la semana que viene |

## Corrida de verificación (2026-08-19)

| Comprobación | 02W | 03W |
|---|---|---|
| Balance de bloques de código (un "seleccionar todo" no trunca) | ✅ 68, balanceados | ✅ 44, balanceados |
| Comandos de macOS dentro de bloques de código | ✅ 0 ejecutables (1 textual, dentro de la instrucción "no me ofrezcas estos") | ✅ 0 |
| Rutas `~/Library` dentro de bloques de código | ✅ 0 | ✅ 0 |
| `bash -n` sobre cada bloque bash | ✅ 10 limpios / 5 solo con marcadores — **idéntico a la línea base EN**, sin regresiones | ✅ 15 limpios, 0 fallando |
| El bloque `settings.json` parsea, el *hook* Stop desescapa correctamente | ✅ `powershell.exe -c "[console]::beep(1000,400)"` | n/a |
| Comillas tipográficas dentro de bloques de código | ✅ 0 | ✅ 0 |

**Nota sobre el defecto #12:** a diferencia del paquete que Mangan armó para uno de sus participantes — que deliberadamente despachó el
bloque de permisos original — estas variantes heredan el bloque **endurecido** (`Bash(python3 *)`,
`Bash(pip install *)`, `Read`/`Write`/`Edit` a secas eliminados), según la decisión del mantenedor del 2026-08-19.
El cambio del STEP 7 de Windows descrito arriba es lo que hace que ese endurecimiento no cueste nada: hace que
Claude añada el comando *real* de Python a `allow` solo si Python existe de verdad.
