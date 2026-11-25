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

| Comprobación | Resultado (2026-11-25) |
|---|---|
| Bloques de código byte por byte idénticos al EN | **161 de 169** — las 8 excepciones están abajo |
| Paridad de conteo de bloques y de encabezados, archivo por archivo | ✅ exacta en los documentos con gemelo EN |
| Comillas tipográficas en documentos del participante | ✅ 0 |
| Voseo en documentos del participante | ✅ 0 (el registro por defecto es español latinoamericano neutro con tuteo) |
| Lista de permisos de 12 entradas (`allow` estrecho) en los Documentos 02 / 02W / 02-S | ✅ idéntica al EN, byte por byte (la verifica `tests/test_setup_permissions.py`) |
| `tools/aiac-status-check.sh` | ✅ idéntico al EN — **compartido a propósito, no bifurcado** |

## Las desviaciones — 8 en total

| # | Dónde | El Kit EN dice | La edición ES dice | Por qué |
|---|---|---|---|---|
| 1–4 | `02`, `02W`, `03`, `03W` — la línea que el participante escribe para entregarle el archivo a Claude (bloque 0) | `Read the file <path> and follow its instructions, starting at "FOR CLAUDE — START HERE".` | `Lee el archivo <ruta> y sigue sus instrucciones, empezando en "PARA CLAUDE — EMPIEZA AQUÍ".` | La línea nombra el encabezado donde Claude empieza, y en la edición ES ese encabezado está en español. No es un comando de terminal: es lo que el participante le escribe a Claude. |
| 5–6 | `02` y `02W` — router global `~/.claude/CLAUDE.md`, sección `## Defaults` | `- Language: English. English for code comments and variable names.` | `- Language: Spanish. English for code comments and variable names.` | El bloque se escribe **literalmente** en el archivo de configuración del participante. Sin este cambio, un participante hispanohablante queda con un router que le pide a Claude responder en inglés en cada sesión. |
| 7–8 | `02` y `02W` — `CLAUDE.md` del repo, sección `## Rules` | `- Language: English (comments, variable names, and output).` | `- Language: Spanish for output and documentation; English for code comments and variable names.` | Igual que 5–6, para las sesiones abiertas dentro del repo. |

> [!note] **Por qué esto vale una excepción a la regla de "no toques los bloques de código".**
> La regla existe porque Claude ejecuta los comandos de los Documentos 02 y 03 tal cual están escritos, y
> un comando mal traducido falla en vivo. Estas líneas **no son comandos**: una es lo que el participante le
> escribe a Claude, y las otras son instrucciones en markdown que terminan dentro de un archivo de
> configuración. No se ejecutan ni se parsean. Es la única clase de contenido dentro de un *fence* donde el
> idioma sí importa para el participante.
>
> La desviación anterior (la línea `Respond in Spanish.` de la *skill* `session-close` escrita a mano en
> `03`/`03W`) ya no existe: desde v0.2 esa *skill* se instala desde el paquete público
> `AI-Acceleration/cc-starter-pack` `v1.0.0`, que no fija un idioma y responde en el del participante.

## Decisión de alcance registrada — el cuerpo del prompt SÍ se traduce

Los Documentos 02 / 02W / 03 / 03W traducen **todo el cuerpo** que Claude lee, no sólo la envoltura
dirigida al participante. Los cuatro usan `PASO`, no `STEP` (18 / 18 / 11 / 11 — verificado el 2026-11-25).

La decisión fue deliberada:

- La regla del kit es **una superficie completa por idioma**: el participante hispanohablante lee y
  revisa lo que Claude va a hacer, en su idioma.
- El riesgo real es el **comando** mal traducido — y los comandos viven en bloques de código, que quedan
  byte por byte idénticos salvo las 8 excepciones de arriba. La prosa en español alrededor de ellos no
  rompe nada.
