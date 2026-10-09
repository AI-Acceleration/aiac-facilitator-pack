---
title: "Edición ES — Tabla de Diferencias (Solo Facilitador)"
created: 2026-08-28
category: reference
status: active
tags: [aiac, phase0, co-facilitator-kit, spanish, facilitator, diff]
related: ["[[README — Kit Index & How to Use]]", "[[00W — Windows Edition Diff Tables (FACILITATOR ONLY)]]", "[[00V — Voseo (Argentina) Diff Table (FACILITATOR ONLY)]]"]
lang: es
---

> # 🚨 NO SE LO ENVÍES A UN PARTICIPANTE
>
> Mismo motivo que `00W` y `00V`.

# Edición ES — en qué se aparta del Kit EN, y por qué

**Principio: variante, no bifurcación** — el mismo de `00W`. La edición ES es el Kit EN traducido más una
lista **corta y auditable** de desviaciones deliberadas. Este archivo es esa lista. Si no está aquí, no se
cambió a propósito.

## Invariante que se mantiene

| Comprobación | Resultado (2026-08-28) |
|---|---|
| Bloques de código byte por byte idénticos al EN | **157 de 159** — las 2 excepciones están abajo |
| Paridad de conteo de bloques y de encabezados, archivo por archivo | ✅ exacta en los 11 documentos |
| Comillas tipográficas en documentos del participante | ✅ 0 |
| Voseo en documentos del participante | ✅ 0 (el registro por defecto es tuteo venezolano) |
| Lista de permisos de 8 entradas en el Documento 02 | ✅ intacta, byte por byte |
| `tools/aiac-status-check.sh` | ✅ idéntico al EN — **compartido a propósito, no bifurcado** |

## Las desviaciones — 2 en total

| # | Dónde | El Kit EN dice | La edición ES dice | Por qué |
|---|---|---|---|---|
| 1 | `03 — Skills & Config Setup Prompt`, bloque de la *skill* `session-close` (índice 18) | `- Respond in English.` | `- Respond in Spanish.` | El bloque se escribe **literalmente** dentro del archivo de la *skill* del participante. Sin este cambio, un participante hispanohablante instala una *skill* que le responde en inglés — lo cual anula la premisa de "una superficie completa por idioma". |
| 2 | `03W — Skills & Config Setup Prompt (Windows)`, mismo bloque (índice 18) | `- Respond in English.` | `- Respond in Spanish.` | Idéntico al #1. Se aplica a los dos para que `03W` siga siendo variante de `03` y no adquiera una desviación propia no listada. |

> [!note] **Por qué esto vale una excepción a la regla de "no toques los bloques de código".**
> La regla existe porque los Documentos 02 y 03 se pegan en una terminal viva y un comando mal traducido
> falla en vivo. Esta línea **no es un comando**: es una instrucción en markdown que termina dentro de un
> archivo de configuración. No se ejecuta, no se parsea, y traducirla no puede romper un pegado. Es la única
> clase de contenido dentro de un *fence* donde el idioma sí importa para el participante.
>
> Detectada por el agente que tradujo `03`, que **la reportó en vez de arreglarla por su cuenta** — que es
> exactamente el comportamiento correcto: la excepción la decide el mantenedor y queda registrada aquí.

## Decisión de alcance registrada — el cuerpo del prompt SÍ se traduce

Los Documentos 02 / 02W / 03 / 03W traducen **todo el cuerpo pegable**, no sólo la envoltura dirigida al
participante. Los cuatro usan `PASO`, no `STEP` (18 / 18 / 13 / 13 — verificado).

Esto se registra porque hay un precedente en contra: las plantillas semilla de `aiac-pipeline`
(`main-setup-prompt-template.md`, `skills-config-prompt-template.md`) dejan ese cuerpo **en inglés**
(`STEP` ×17 y ×13, `PASO` ×0). La decisión de apartarse de ellas fue deliberada:

- La spec aprobada dice, textualmente, traducir **el Kit completo** — *"una superficie completa por idioma"*.
- Las semillas son plantillas **del mantenedor del programa**, para que él las rellene por participante; están en inglés
  porque él trabaja en inglés. El Kit es el artefacto **del participante**. Audiencias distintas.
- La semilla de `03` no tiene prosa en español **en absoluto**, así que "precedente de la semilla" en
  realidad significa *"las semillas nunca se tradujeron"*, no *"se decidió dejar el cuerpo en inglés"*.
- El riesgo que la spec nombra es el **comando** mal traducido — y los comandos viven en bloques de código,
  que quedan byte por byte idénticos. La prosa en español alrededor de ellos no rompe ningún pegado.

## Requisito de convergencia (pendiente)

Ahora que existe la edición ES, **ella** — no las plantillas ES de `aiac-pipeline` — es la fuente de verdad
en español. Mientras eso no se refleje, hay dos superficies en español y el próximo parche hay que aplicarlo
dos veces, que es exactamente el defecto que el parche del 2026-08-19 ya pagó una vez.
