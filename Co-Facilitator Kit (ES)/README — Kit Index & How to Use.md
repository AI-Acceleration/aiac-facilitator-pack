---
title: "Kit de Co-Facilitación AIAC Fase 0 (ES) — README e Índice"
created: 2026-07-14
category: reference
status: draft
tags: [aiac, phase0, co-facilitator, kit, spanish, readme]
related: ["[[AI Acceleration Club - Phase 0 Playbook]]"]
lang: es
translated_from: "README — Kit Index & How to Use.md"
---

# Kit de Co-Facilitación AIAC Fase 0 (ES)

Un kit autocontenido, en español, **solo-documentos**, que le permite a un co-facilitador dictar una **sesión de onboarding de Fase 0 uno-a-uno** con cualquier persona — sin archivos preconfigurados y sin formulario de admisión. El participante **construye su propio proyecto en vivo durante la sesión** a través de una entrevista guiada.

## Cómo funciona en un párrafo

Tú (el facilitador) le envías al participante el **Doc 01** unos días antes. El día de la sesión corres el flujo de ~90 minutos y 8 bloques del **Doc 05 (el manual)**: el participante pega el **Doc 02** en Claude Code — que lo entrevista, escoge su primer caso real y genera su propio *vault* + proyecto — y luego pega el **Doc 03** para instalar *skills* y configuración. Al final le entregas el **Doc 04** como su hoja de ruta de tareas. La sesión *arranca* su primer proyecto; la tarea de la Semana 1 lo termina.

## Los documentos (léelos en este orden)

| # | Documento | Audiencia | Cuándo |
|---|----------|----------|------|
| **05** | **Facilitator Manual — How to Run a Phase 0 Session** | Tú (facilitador) | **Lee esto primero.** Guion de la sesión, puntos de enseñanza, compuertas. |
| 01 | Pre-Session Setup Instructions | Participante | Se envía unos días antes de la sesión. |
| 02 | Main Setup Prompt | Participante | Se pega en Claude Code durante el **Bloque 2** (contiene la entrevista en vivo). |
| 03 | Skills & Config Setup Prompt | Participante | Se pega en Claude Code durante el **Bloque 3**. |
| 04 | Next Steps Brief | Participante | Se entrega en el **Bloque 5** como hoja de ruta de tareas. |
| **02-S** | **Sandbox Setup** *(opcional)* | Participante | **Solo para participantes que piden que Claude quede confinado a su *vault*.** Se corre después del Doc 01 y **antes** del Doc 02, y reemplaza el bloque de permisos del PASO 3 del Doc 02. No es parte del flujo por defecto. Solo Mac/Linux. |
| **02W** | **Main Setup Prompt (Windows)** | Participante | **Envíalo en lugar del Doc 02 a un participante en Windows.** |
| **03W** | **Skills & Config Setup Prompt (Windows)** | Participante | **Envíalo en lugar del Doc 03 a un participante en Windows.** |
| **00W** | **Windows Edition Diff Tables** | Mantenedor | 🚨 **Solo para el facilitador — nunca lo envíes.** El registro auditable de cada desviación de Windows. |
| **00V** | **Voseo (Argentina) Diff Table** | Mantenedor | 🚨 **Solo para el facilitador — nunca lo envíes a un participante.** La variante rioplatense como tabla de sustituciones: variante, no bifurcación — el Kit ES en tuteo venezolano más esta lista. El registro se elige por participante, no por facilitador. |
| **00E** | **ES Edition Diff Table** | Mantenedor | 🚨 **Solo para el facilitador — nunca lo envíes a un participante.** El registro auditable de cada desviación de esta edición frente al Kit EN (hoy: **2**), más la decisión de alcance de traducir el cuerpo pegable. |
| 00 | Design Spec | Mantenedor | Procedencia / cómo se derivó el kit. No es parte de la sesión ni del repo público. |

## Cuál edición enviar

| Participante | Envía |
|---|---|
| **Mac** | 01 · 02 · 03 · 04 |
| **Windows** | 01 · **02W** · **03W** · 04 — el Doc 01 y el Doc 04 son compartidos y no necesitan variante |
| **Quiere que Claude quede confinado a su *vault*** (Mac/Linux) | 01 · **02-S** · 02 · 03 · 04, en ese orden |

Windows es una **variante, no un *fork***: `02W`/`03W` son los documentos base más un conjunto listado de
cambios, registrado en `00W — Windows Edition Diff Tables`. Cuando cambies el Doc 02 o el 03, revisa si el
cambio también corresponde a la variante W — y actualiza la tabla de diferencias en cualquier caso.

**Nunca disponible en Windows:** el módulo *sandbox* `02-S`. Windows nativo no tiene *sandbox* (requiere
WSL2), así que un participante en Windows que pida acotar el alcance necesita otra respuesta.

## Antes de tu primera sesión — lo ÚNICO que debes configurar

En el **Doc 04**, reemplaza `[SET: your support channel]` con tu canal de soporte real (por ejemplo, un grupo de WhatsApp, un canal de Slack, tu correo). Es el único valor que llenas; todo lo demás es genérico.

## Reglas de entrega — cómo viajan estos documentos (léelas antes de enviar cualquier cosa)

Aprendidas a golpes en el campo. Romperlas falla en silencio: el participante recibe un archivo que
*parece* correcto y falla al pegarlo.

**1. Los Docs 02 y 03 NUNCA deben viajar por Word ni PDF.**
Su cuerpo *es* el prompt que el participante pega en un terminal. Word encorva las comillas, y una
comilla tipográfica dentro de un JSON o de un comando de shell **falla en vivo, a mitad de sesión**.
Envíalos como `.md` (o en un repositorio privado). **Los Docs 01 y 04 sí se pueden convertir** — sus
bloques se pegan en el chat de claude.ai, que tolera comillas tipográficas.

> Verifica cualquier `.docx` generado antes de enviarlo: revisa que ningún fragmento en `Courier New`
> contenga `' ' " "`, y luego **mira** de verdad el archivo renderizado. Las revisiones de texto no
> detectan errores de diagramación.

**2. WhatsApp y Gmail bloquean los adjuntos `.sh`.**
Envía un gemelo `.sh.txt` byte-idéntico (corre igual). Mantén cualquier script que envíes **100% ASCII**
para que sobreviva el copiar y pegar por aplicaciones de chat.

**3. Los repositorios privados de entrega por estudiante funcionan bien.**
Un repositorio privado por participante (`aiac-phase0-<name>`), con los documentos verificados por hash
contra el kit después del *push*. Privado a propósito: enviarle tu kit a tu propio participante es su uso
previsto; publicarlo abiertamente es republicar el material. Díselos claramente: *no corran Claude Code
dentro del clon* — el Doc 02 construye el *vault* donde sea que Claude Code esté corriendo.

**4. El material del facilitador nunca viaja junto.**
Todo lo que esté escrito *sobre* un participante (notas de seguimiento, tablas de diferencias,
discusiones de defectos) vive fuera de la carpeta compartible. Mantén una sola subcarpeta
`Send to <Name>/` que sea la única superficie desde la que compartes.

## Herramientas

- **`tools/aiac-status-check.sh`** — diagnóstico de pre-sesión de solo lectura que el participante corre en
  su propio Terminal. Reporta DONE / NOT DONE por documento; el primer NOT DONE es el punto de retomada.
  Envía el gemelo `.sh.txt` (WhatsApp y Gmail bloquean `.sh`). Aportado por Mangan, adoptado el 2026-08-19.
- **Nota de la edición ES:** `tools/aiac-status-check.sh` se comparte **intencionalmente** con la edición en
  inglés y **no se traduce** — el script es byte-idéntico al de la edición EN para no bifurcarlo. Su salida
  (`DONE` / `NOT DONE`) sale en inglés a propósito; explícasela al participante en la sesión.

## Alcance

- **Dentro:** español, uno-a-uno, solo-documentos, autoconfiguración del participante en vivo.
- **Fuera (futuro):** formato de grupo/cohorte, *decks* de enseñanza (el manual carga la narrativa de enseñanza en su lugar), un plugin instalable.

## Notas para el mantenedor

- Las *skills* de los Docs 03/04 se instalan desde el repositorio **público** `wildbuffaloman/cc-starter-pack`. Si la visibilidad de ese repositorio alguna vez cambia a privada, las instalaciones del participante se van a romper — mantenlo público (o empaqueta los cuerpos de las *skills*).
- Derivado de las plantillas del pipeline AIAC en español en vivo. **Desde el 2026-08-19 el pipeline ES en
  vivo SÍ se mantiene sincronizado** — el mismo conjunto de defectos se había propagado allá y se parchó en
  la misma pasada. Cuando arregles algo aquí, revisa `05 AI/CLAUDE CODE/plugins/aiac-pipeline/` por el
  gemelo.
- Una instantánea prístina previa al parche vive en `../_kit-snapshots/2026-08-19 pre-mangan-patch (do not edit)/`.
  Compara contra ella para auditar cualquier cambio. Guarda una instantánea fresca antes de la próxima ronda de ediciones.
