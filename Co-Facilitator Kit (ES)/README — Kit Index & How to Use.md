# Kit de Co-Facilitación AIAC Fase 0 (ES)

[← Volver a la portada del repositorio](../LEEME.md) · [Kit in English](../Co-Facilitator%20Kit%20(EN)/README%20%E2%80%94%20Kit%20Index%20%26%20How%20to%20Use.md)

Este es un kit autocontenido en español, **solo de documentos**, para dirigir
una **sesión de onboarding de Fase 0** con cualquier persona. No hay
formulario de admisión, y lo único que se prepara de antemano son dos
marcadores que llenas una sola vez (ver abajo). El
participante **construye su propio proyecto en vivo durante la sesión** a
través de una entrevista guiada. Está pensado para sesiones uno a uno; con un
grupo pequeño también funciona, pero toma más tiempo.

## Cómo funciona en un párrafo

Tú (el facilitador) le envías al participante los **Docs 01, 02, 03 y 07** (el
Doc 07 es el vocabulario) más o menos una semana antes. El participante
instala todo por su cuenta y termina con un pre-vuelo corto cuyo resultado, en
una línea (`PREFLIGHT: READY · ACCOUNT: personal|team`), te envía.
El día de la sesión corres el flujo de 8 bloques del **Doc 05 (el manual)**.
El participante le da el **Doc 02** a Claude Code **por archivo**: lo guarda y
le dice a Claude «Lee el archivo <ruta> y sigue sus instrucciones». Claude lo
entrevista, escoge su primer caso real y le arma su propio *vault* y su
proyecto. Luego carga el **Doc 03** de la misma forma para instalar *skills*
y configuración. Al final le entregas el **Doc 04** (su hoja de ruta de
tareas) y el **Doc 06** (cómo hacer rendir el plan Pro). La sesión *arranca*
su primer proyecto, y la tarea de la Semana 1 lo termina. Duración: unos 90
minutos si todo sale bien. Calcula 2–3 horas para tus primeras sesiones.

## Los documentos (léelos en este orden)

| # | Documento | Audiencia | Cuándo |
|---|----------|----------|------|
| **05** | [**Manual del facilitador — Cómo dictar una sesión de Fase 0**](05%20%E2%80%94%20Facilitator%20Manual%20%E2%80%94%20How%20to%20Run%20a%20Phase%200%20Session.md) | Tú (facilitador) | **Lee esto primero.** Guion de la sesión, puntos de enseñanza, compuertas. |
| 01 | [Configuración pre-sesión](01%20%E2%80%94%20Pre-Session%20Setup%20Instructions%20(Participant).md) | Participante | Se envía más o menos una semana antes de la sesión. |
| 07 | [Vocabulario](07%20%E2%80%94%20Vocabulario%20(Participante).md) | Participante | Se envía junto con el Doc 01. Los términos principales, cinco minutos de lectura, más o menos un día antes de la sesión. |
| 02 | [Prompt de configuración principal](02%20%E2%80%94%20Main%20Setup%20Prompt%20(Participant).md) | Participante | Se envía con el Doc 01 (el pre-vuelo lo mueve al *vault*). Se carga en Claude Code por archivo durante el **Bloque 2** (contiene la entrevista en vivo). |
| 03 | [Prompt de configuración de *skills* y config](03%20%E2%80%94%20Skills%20%26%20Config%20Setup%20Prompt%20(Participant).md) | Participante | Se envía con el Doc 01. Se carga en Claude Code por archivo durante el **Bloque 3**. |
| 04 | [Brief de próximos pasos](04%20%E2%80%94%20Next%20Steps%20Brief%20(Participant).md) | Participante | Se entrega en el **Bloque 5** como hoja de ruta de tareas. |
| 06 | [Kit de supervivencia del plan Pro](06%20%E2%80%94%20Kit%20de%20Supervivencia%20del%20Plan%20Pro%20(Participante).md) | Participante | Se entrega con el Doc 04, para leerlo antes de empezar el trabajo real. Cómo funcionan los límites de uso y cómo hacer rendir el plan Pro. |
| **02-S** | [**Configuración de sandbox**](02-S%20%E2%80%94%20Sandbox%20Setup%20(Participant,%20opt-in).md) *(opcional)* | Participante | **Solo para participantes que piden que Claude quede confinado a su *vault*.** Se corre después del Doc 01 y **antes** del Doc 02, y reemplaza el bloque de permisos del PASO 3 del Doc 02. No es parte del flujo por defecto. macOS, Linux, o Windows con Claude Code dentro de WSL2 (no Windows nativo). |
| **02W** | [**Prompt de configuración principal (Windows)**](02W%20%E2%80%94%20Main%20Setup%20Prompt%20(Windows).md) | Participante | **Envíalo en lugar del Doc 02 a un participante en Windows.** |
| **03W** | [**Prompt de *skills* y config (Windows)**](03W%20%E2%80%94%20Skills%20%26%20Config%20Setup%20Prompt%20(Windows).md) | Participante | **Envíalo en lugar del Doc 03 a un participante en Windows.** |
| **00W** | [**Tablas de diferencias de la edición Windows**](00W%20%E2%80%94%20Windows%20Edition%20Diff%20Tables%20(FACILITATOR%20ONLY).md) | Mantenedor | 🚨 **Solo para el facilitador, nunca lo envíes.** El registro auditable de cada desviación de Windows. |
| **00V** | [**Tabla de diferencias del voseo (Argentina)**](00V%20%E2%80%94%20Voseo%20(Argentina)%20Diff%20Table%20(FACILITATOR%20ONLY).md) | Mantenedor | 🚨 **Solo para el facilitador, nunca lo envíes a un participante.** La variante rioplatense como tabla de sustituciones: es una variante, no una bifurcación (el Kit ES en tuteo más esta lista). El registro se elige por participante, no por facilitador. |
| **00E** | [**Tabla de diferencias de la edición ES**](00E%20%E2%80%94%20ES%20Edition%20Diff%20Table%20(FACILITATOR%20ONLY).md) | Mantenedor | 🚨 **Solo para el facilitador, nunca lo envíes a un participante.** El registro auditable de cada desviación de esta edición frente al Kit EN, más la decisión de alcance de traducir el cuerpo de los prompts. |

## Cuál edición enviar

| Participante | Envía |
|---|---|
| **Mac** | 01 · 02 · 03 · 07 antes de la sesión (02 y 03 se cargan durante la sesión); 04 · 06 al final |
| **Windows** | 01 · **02W** · **03W** · 07 antes (02W y 03W se cargan durante la sesión); 04 · 06 al final. Los Docs 01, 04, 06 y 07 son compartidos y no necesitan variante |
| **Quiere que Claude quede confinado a su *vault*** (macOS, Linux o WSL2) | 01 · 02 · 03 · 07 antes, más **02-S** después del pre-vuelo y antes del Doc 02; 04 · 06 al final |

Windows es una **variante, no un *fork***: `02W`/`03W` son los documentos base
más un conjunto listado de cambios, registrado en `00W — Windows Edition Diff
Tables`. Cuando cambies el Doc 02 o el 03, revisa si el cambio también
corresponde a la variante W, y actualiza la tabla de diferencias en cualquier
caso.

***Sandbox* en Windows:** el módulo `02-S` funciona solo con Claude Code
corriendo dentro de **WSL2** (Parte 2 del 02-S). Windows nativo no tiene
*sandbox*, así que un participante en Windows que pida acotar el alcance o
trabaja dentro de WSL2 o necesita otra respuesta.

**Prerrequisitos:** todo lo del Doc 01 es obligatorio en el pre-vuelo,
incluidos Python 3 (la fusión de ajustes del Paso 3 del Doc 02 lo usa) y `jq`.
Lo único opcional es lo que el Doc 01 marca como opcional (Ghostty, una
herramienta de transcripción). Si de verdad no se puede instalar `jq` ese día,
el Doc 02 tiene un camino reducido sin la barra de estado.

**Plan:** Claude **Pro** es el plan por defecto y alcanza para empezar. Pasa a
Max solo cuando los límites te frenen seguido. El Doc 06 explica cómo
saberlo.

**Registro:** español latinoamericano neutro con **tuteo**. Para un
participante rioplatense, aplica la tabla `00V`.

## Antes de tu primera sesión: las DOS cosas que debes llenar

Todo lo demás del kit es genérico. Estos dos marcadores son tuyos:

1. **`[SET: your support channel]`** en los **Docs 01 y 04**. Reemplázalo con
   el canal por el que tus participantes te contactan (un grupo de WhatsApp,
   un canal de Slack, tu correo).
2. **`[TOOL]`** en los **Docs 03 y 03W**. Reemplázalo con la herramienta de
   transcripción de reuniones del participante: Granola, otra herramienta de
   transcripción, o `none / pasted transcript` (ninguna, transcripción
   pegada). Grabar es opcional: pregunta siempre antes a todos los presentes;
   una transcripción pegada funciona igual de bien.

## Reglas de entrega: cómo viajan estos documentos (léelas antes de enviar cualquier cosa)

Las aprendimos a golpes en el campo. Cuando rompes una, nada te avisa: el
participante recibe un archivo que *parece* correcto y falla a mitad de
sesión.

**1. Envía los documentos como Markdown (`.md`), nunca por Word ni PDF.**
Los Docs 01 a 04 contienen prompts y comandos. Word encorva las comillas, y
una comilla tipográfica dentro de un JSON o de un comando de shell **falla en
vivo, a mitad de sesión**. Los Docs 06 y 07 son solo lectura y se pueden
convertir si hace falta.

> Si alguna vez generas un `.docx`, verifícalo antes de enviarlo: revisa que
> ningún fragmento en `Courier New` contenga `' ' " "`, y luego **mira** de
> verdad el archivo renderizado. Las revisiones de texto no detectan errores
> de diagramación.

**2. Los prompts largos se cargan por archivo, no se pegan.**
Las terminales, sobre todo la de Windows, pueden cortar un texto largo pegado
sin avisar. El participante guarda el documento, copia su ruta y le dice a
Claude «Lee el archivo <ruta> y sigue sus instrucciones». Solo los prompts
cortos, de pocas líneas, se pegan.

**3. WhatsApp y Gmail bloquean los adjuntos `.sh`.**
Envía el gemelo `.sh.txt` del chequeo de estado, byte-idéntico (corre igual).
El participante corre el **nombre exacto que recibió**, por ejemplo
`bash ~/Downloads/aiac-status-check.sh.txt`, y te envía **solo** el bloque
entre `----- AIAC STATUS (safe to share) -----` y `----- END -----`. Todo lo
que está arriba de ese bloque es solo para sus ojos. Cuando Claude le corre el
chequeo, lo corre con `--share`, que imprime solo el bloque, así el detalle
nunca llega al contexto de Claude. Mantén cualquier script
que envíes **100% ASCII** para que sobreviva el copiar y pegar por
aplicaciones de chat.

**4. Los repositorios privados de entrega por participante funcionan bien.**
Un repositorio privado por participante (`aiac-phase0-<name>`), con los
documentos verificados por hash contra el kit después del *push*. Que sea
privado mantiene fuera de la vista pública el nombre del participante y tus
notas para él. El kit en sí es CC BY 4.0, así que también puedes republicarlo
o adaptarlo abiertamente, siempre que des crédito. Díselo claramente al
participante: *no corras Claude Code dentro del clon*. El Doc 02 construye el
*vault* donde sea que Claude Code esté corriendo.

**5. El material del facilitador nunca viaja junto.**
Todo lo que esté escrito *sobre* un participante (notas de seguimiento,
tablas de diferencias, discusiones de defectos) vive fuera de la carpeta
compartible. Mantén una sola subcarpeta `Send to <Name>/` que sea el único
lugar desde el que compartes.

## Herramientas

- **`tools/aiac-status-check.sh`** (envía el gemelo `.sh.txt`): un chequeo de
  pre-sesión de solo lectura que el participante corre en su propia terminal,
  en macOS, Windows (Git Bash o WSL) o Linux. No escribe nada. Primero
  imprime detalles para el participante y luego un **bloque corto que se
  puede compartir**, solo con nombres de chequeos y su estado, el sistema
  operativo y un veredicto general. El primer `NOT DONE` es el punto donde
  retomar. `--share` imprime solo ese bloque (úsalo siempre que Claude corra
  el chequeo); `--details` muestra más detalle local y advierte que no se
  comparta. Aportado por Mangan.
- **Leyenda: el script imprime en inglés.** Es byte-idéntico al de la edición
  EN, para no bifurcarlo, así que su salida sale en inglés a propósito.
  Explícasela así al participante:

  | El script dice | Significa |
  |---|---|
  | `DONE` | Hecho |
  | `NOT DONE` | No hecho: falta este paso |
  | `SKIPPED (optional)` | Omitido: es opcional y no cuenta para el veredicto |

## De dónde vienen las *skills* iniciales

Los Docs 03/03W y 04 instalan las *skills* iniciales desde el repositorio
público
[`AI-Acceleration/cc-starter-pack`](https://github.com/AI-Acceleration/cc-starter-pack),
**fijado en la etiqueta `v1.0.0`**, para que cada instalación nueva reciba los
mismos archivos revisados (una *skill* que el participante ya tenga con el mismo
nombre se salta y conserva su versión). Una versión nueva implica una etiqueta nueva y
actualizar los documentos.

## No depende de una sola herramienta de IA

El método son archivos de texto simple (notas en Markdown, unos pocos
archivos de instrucciones) más herramientas estándar como Git y GitHub. Hoy
recomendamos Claude Code y todos los prompts están escritos para él, pero el
*vault* y los hábitos te sirven igual con otras herramientas de IA.

## Alcance

- **Dentro:** español, solo documentos, autoconfiguración del participante en
  vivo; uno a uno por diseño, grupos pequeños con tiempo extra.
- **Fuera:** una versión del kit como plugin instalable.
