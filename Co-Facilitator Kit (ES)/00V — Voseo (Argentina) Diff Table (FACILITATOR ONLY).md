---
title: "Voseo rioplatense (Argentina) — Tabla de Diferencias (Solo Facilitador)"
created: 2026-08-28
category: reference
status: active
tags: [aiac, phase0, co-facilitator-kit, voseo, argentina, facilitator, diff, register]
related: ["[[README — Kit Index & How to Use]]", "[[00W — Windows Edition Diff Tables (FACILITATOR ONLY)]]"]
lang: es
---

> # 🚨 NO SE LO ENVÍES A UN PARTICIPANTE
>
> Igual que `00W`: el participante le entrega los documentos de setup a Claude Code por su ruta (*"Lee el
> archivo … y sigue sus instrucciones"*), y Claude lee el archivo **completo**: cualquier cosa añadida a un
> documento la leería como instrucciones. Este archivo existe **por separado** para que la variante
> rioplatense quede auditable sin viajar de contrabando en el setup de alguien.

# Voseo rioplatense — qué cambia y por qué

**Principio: variante, no bifurcación.** Exactamente el mismo patrón que la Edición Windows. **No existe un
"Kit ES-AR".** Existe el Kit ES — en español latinoamericano neutro con tuteo — más esta lista de sustituciones. Cada desviación se
puede revisar, cuestionar o revertir, y la edición nunca se desvía en silencio del kit.

> [!important] **El registro se elige por PARTICIPANTE, nunca por facilitador.**
> Un facilitador rioplatense con alumnos argentinos usará esta tabla casi siempre. Pero un facilitador
> que trabaja en tuteo puede tener su círculo más cercano **en inglés**: un mismo facilitador abarca dos
> registros *y* dos idiomas. Antes de cada sesión, decide el registro mirando
> **a quién tienes enfrente**, no de quién es la cuenta.

## Alcance — dónde aplica y dónde NO

| Superficie | ¿Aplica el voseo? |
|---|---|
| Prosa de los documentos del participante (`01`, `02`, `02W`, `02-S`, `03`, `03W`, `04`, `06`, `07`) | ✅ Sí |
| Texto **dentro de bloques de código** (``` ```), comandos, rutas, JSON, `{{PLACEHOLDERS}}` | ⛔ **NUNCA.** Byte por byte idéntico al Kit ES. Claude ejecuta esos comandos tal cual están escritos. |
| Comentarios dentro de bloques de código | ⛔ No. Van en inglés en las tres ediciones. |
| Manual del Facilitador (`05`) y specs (`00`, `00W`, `00V`) | ➖ Opcional — los lee el facilitador, no el alumno. Si el facilitador es rioplatense, que los lea como están; no vale la pena mantener una segunda copia. |
| Títulos de las preguntas del formulario de admisión | ⛔ **NUNCA.** Son claves de unión del Apps Script. Renombrarlas rompe el manejador en silencio. |

## La regla en una línea

**Cambian dos cosas: el imperativo afirmativo y el presente de indicativo de la 2ª persona.** Casi todo lo
demás — `te`, `tu`, `tus`, `tuyo`, el imperativo **negativo**, y todos los tiempos que no sean presente —
es idéntico en ambos registros. Por eso la sustitución es corta y mecánica.

## Imperativos — las formas que aparecen de verdad en el Kit ES

Conteo medido sobre la prosa de `01`, `02`, `02W`, `02-S`, `03`, `03W` y `04` el 2026-11-25, excluyendo
bloques de código y código en línea. **Los conteos son aproximados:** varias formas también son
sustantivo o 3ª persona (`prueba`, `muestra`, `sigue`, `lee`, `corre`, `usa`, `crea`) — convierte sólo
cuando es imperativo dirigido al lector. En **negrita**, las que no salen de mover el acento.

| # | Tuteo (Kit ES) | Voseo (AR) | Apariciones |
|---|---|---|---|
| 1 | `crea` | `creá` | ~66 |
| 2 | `confirma` | `confirmá` | ~71 |
| 3 | `usa` | `usá` | ~59 |
| 4 | `escribe` | `escribí` | ~46 |
| 5 | `ejecuta` | `ejecutá` | ~44 |
| 6 | `prueba` | **`probá`** | ~44 |
| 7 | `abre` | `abrí` | ~41 |
| 8 | `lee` | `leé` | ~41 |
| 9 | `revisa` | `revisá` | ~41 |
| 10 | `sigue` | **`seguí`** | ~41 |
| 11 | `instala` | `instalá` | ~38 |
| 12 | `haz` | **`hacé`** | ~35 |
| 13 | `dime` | **`decime`** | ~29 |
| 14 | `muéstrame` | **`mostrame`** | ~27 |
| 15 | `copia` | `copiá` | ~26 |
| 16 | `corre` | `corré` | ~26 |
| 17 | `pega` | `pegá` | ~25 |
| 18 | `muestra` | **`mostrá`** | ~24 |
| 19 | `verifica` | `verificá` | ~23 |
| 20 | `ve` (de *ir*) | **`andá`** | ~20 |
| 21 | `agrega` | `agregá` | ~18 |
| 22 | `vuelve` | **`volvé`** | ~18 |
| 23 | `arranca` | `arrancá` | ~14 |
| 24 | `pregúntame` | **`preguntame`** | ~14 |
| 25 | `espera` | `esperá` | ~12 |
| 26 | `guarda` | `guardá` | ~12 |
| 27 | `cierra` | `cerrá` | ~11 |
| 28 | `pide` | **`pedí`** | ~9 |
| 29 | `reemplaza` | `reemplazá` | ~9 |
| 30 | `presiona` | `presioná` | ~8 |
| 31 | `busca` | `buscá` | ~7 |
| 32 | `cambia` | `cambiá` | ~6 |
| 33 | `di` | **`decí`** | ~6 |
| 34 | `mantén` | **`mantené`** | ~6 |
| 35 | `anota` | `anotá` | ~5 |
| 36 | `borra` | `borrá` | ~5 |
| 37 | `dile` | **`decile`** | ~5 |
| 38 | `elige` | **`elegí`** | ~5 |
| 39 | `entra` | `entrá` | ~5 |
| 40 | `marca` | `marcá` | ~5 |
| 41 | `asegúrate` | **`asegurate`** | ~4 |
| 42 | `pon` | **`poné`** | ~4 |
| 43 | `añade` | `añadí` | ~2 |
| 44 | `avísame` | **`avisame`** | ~2 |
| 45 | `quita` | `quitá` | ~2 |
| 46 | `responde` | `respondé` | ~2 |
| 47 | `selecciona` | `seleccioná` | ~2 |
| 48 | `ten` | **`tené`** | ~2 |
| 49 | `ábrelo` | **`abrilo`** | ~1 |
| 50 | `descarga` | `descargá` | ~1 |

### Las irregulares — las que no salen de mover el acento

La regla general del imperativo voseo es *quitar la `-r` del infinitivo y acentuar la última sílaba*
(`pegar → pegá`). Éstas no siguen el patrón visualmente y son donde se cometen los errores:

| Tuteo | Voseo | Trampa |
|---|---|---|
| `haz` | `hacé` | No es `hacé` ← `haz`; sale de `hacer`. `hazlo` → **`hacelo`** (sin tilde: la sílaba tónica ya cae bien). |
| `ve` | `andá` | **Supletiva.** El voseo usa *andar*, no *ir*. `ve a la carpeta` → `andá a la carpeta`. |
| `pon` | `poné` | De `poner`. `ponlo` → **`ponelo`**. |
| `sigue` · `vuelve` · `muestra` · `prueba` · `pide` · `elige` | `seguí` · `volvé` · `mostrá` · `probá` · `pedí` · `elegí` | **Verbos con cambio de raíz:** el voseo usa la raíz del infinitivo, sin diptongo ni cambio de vocal (`seguir`, `volver`, `mostrar`, `probar`, `pedir`, `elegir`). `vuelve a hacer push` → `volvé a hacer push`. |
| `di` · `dime` · `dile` | `decí` · `decime` · `decile` | De `decir`. `dímelo` → **`decímelo`** (aquí la tilde se queda: la palabra queda esdrújula). |
| `ten` · `ven` · `mantén` | `tené` · `vení` · `mantené` | De `tener`, `venir`, `mantener`. `mantén presionada` → `mantené presionada`. |
| `asegúrate` | `asegurate` | ⚠ **La tilde DESAPARECE.** El acento se corre a la última sílaba, que ya no necesita tilde escrita. Escribir `asegurate` con tilde es el error más común. |

> [!caution] **Los enclíticos pierden la tilde, no la ganan.**
> `hazlo → hacelo` · `pégalo → pegalo` · `créalo → crealo` · `revísalo → revisalo` ·
> `muéstrame → mostrame` · `pregúntame → preguntame` · `avísame → avisame` · `ábrelo → abrilo`.
> En tuteo la tilde aparece al pegar el pronombre; en voseo **no**, porque la sílaba tónica ya es la última
> de la raíz. Si tu buscar-y-reemplazar produce `pegálo`, está mal.

## Presente de indicativo — las formas del Kit ES

| Tuteo (Kit ES) | Voseo (AR) | Apariciones | Nota |
|---|---|---|---|
| `puedes` | `podés` | ~20 | |
| `tienes` | `tenés` | ~18 | |
| `necesitas` | `necesitás` | ~14 | |
| `quieres` | `querés` | ~13 | |
| `eres` | **`sos`** | ~4 | Supletiva |
| `haces` | `hacés` | ~3 | |
| `sabes` | `sabés` | ~3 | |
| `debes` | `debés` | ~2 | |
| `sientes` | `sentís` | ~2 | |
| `prefieres` | `preferís` | ~1 | |
| `vuelves` | `volvés` | ~1 | |
| `dices` | `decís` | 0 | Incluida por si aparece al editar |
| `eliges` | `elegís` | 0 | Incluida por si aparece al editar |

### ✅ Idénticas en ambos registros — NO las toques

Éstas son las que un buscar-y-reemplazar descuidado rompe de más:

| Forma | Por qué no cambia |
|---|---|
| `estás` | El presente de *estar* ya es agudo en las dos variantes. |
| `vas` | Igual en tuteo y voseo. |
| `ves` | Igual en tuteo y voseo (`vos ves`). |
| `te`, `tu`, `tus`, `tuyo`, `ti` → `vos` sólo tras preposición | Los clíticos y posesivos son idénticos. Sólo el pronombre sujeto `tú` → `vos`, y `para ti` → `para vos`. |
| Imperativo **negativo** (`no borres`, `no cierres`, `no pegues`) | El subjuntivo negativo es el mismo. **Sólo cambia el afirmativo.** |
| Pasado, futuro, condicional, infinitivos | Sin cambios. |

> [!note] **Por eso la línea de consentimiento del formulario no tiene variante.**
> *"Tus respuestas se comparten con la persona que dirige tu sesión y con el responsable del programa."* — está escrita a
> propósito con `tus`/`tu`, que son idénticos en los dos registros. Una sola cadena sirve a toda la
> audiencia hispana, y no hay que tocar un título de formulario bloqueado.

## Léxico — sustituciones opcionales

Ninguna es obligatoria; el Kit ES se entiende perfectamente en Argentina tal cual. Úsalas sólo si quieres
que el documento suene local.

| Kit ES (neutro) | AR | Comentario |
|---|---|---|
| `computadora` | `computadora` | Igual. **No uses `ordenador`** (España) en ninguna edición. |
| `carpeta` / `archivo` | `carpeta` / `archivo` | Igual. **Nunca `fichero`.** |
| `¿Cómo te va?` | `¿Cómo andás?` | Sólo en la charla del facilitador, no en los documentos. |
| `celular` | `celular` | Igual. |

## Cómo aplicarla — procedimiento

1. **Copia el Kit ES**, no lo edites en su sitio. La versión en tuteo es la fuente de verdad.
2. **Aplica las sustituciones sólo a la prosa.** Antes de nada, extrae y aparta los bloques de código.
3. **Corre las compuertas** de abajo antes de mandarle nada a un participante.
4. **No conviertas** `05`, `00`, `00W` ni este archivo — son del facilitador.

> [!danger] **Un buscar-y-reemplazar global sobre el archivo entero rompe los Documentos 02 y 03.**
> `usa` aparece dentro de comandos y de JSON. Reemplazar a ciegas mete `usá` dentro de un bloque de código
> y el comando falla **en vivo, a mitad de sesión**. Aparta los bloques primero. Esto no es teórico: es la
> misma clase de falla que la mina de la barra invertida de `00W`.

## Compuertas de verificación

Corre las cuatro. Las cuatro deben dar el resultado indicado.

| # | Comprobación | Resultado esperado |
|---|---|---|
| 1 | Paridad de bloques de código contra el Kit ES (conteo Y contenido byte por byte) | Idéntico — **0 diferencias** |
| 2 | Comillas tipográficas (`’ ‘ “ ”`) en todo el archivo | **0** |
| 3 | Tuteo residual en prosa: buscar todas las formas de las tablas de arriba (imperativos y presente) | **0** usos dirigidos al lector |
| 4 | Enclíticos mal acentuados: buscar `pegálo`, `hacélo`, `creálo`, `revisálo`, `asegúrate`, `mostráme`, `preguntáme` | **0** |

## Estado

| Documento | Estado de la variante voseo |
|---|---|
| `01 — Pre-Session Setup Instructions` | ⬜ Pendiente — conversión mecánica según esta tabla |
| `02 — Main Setup Prompt` | ⬜ Pendiente — ⚠ el de mayor riesgo (42 bloques de código) |
| `02-S — Sandbox Setup` | ⬜ Pendiente |
| `02W — Main Setup Prompt (Windows)` | ⬜ Pendiente |
| `03 — Skills & Config Setup Prompt` | ⬜ Pendiente — ⚠ 12 bloques de código |
| `03W — Skills & Config Setup Prompt (Windows)` | ⬜ Pendiente |
| `04 — Next Steps Brief` | ⬜ Pendiente |
| `06` y `07` (plan Pro y vocabulario, nuevos en v0.2) | ⬜ Pendiente |
| `05 — Facilitator Manual` | ➖ No aplica — documento del facilitador |

> [!note] **Por qué se despacha la tabla y no los archivos convertidos.**
> El pilot son cuatro facilitadores y **uno solo** es rioplatense. Mantener ocho archivos duplicados para un
> facilitador es exactamente la bifurcación que `00W` existe para evitar: cada defecto habría que arreglarlo
> dos veces, y la segunda copia se queda atrás en silencio — que es el defecto que el parche del 2026-08-19
> ya pagó una vez. La tabla es la unidad correcta hasta que haya suficientes alumnos rioplatenses para que
> valga la pena mantener los archivos.
