# AIAC Facilitator Pack

[English](README.md) · **Español**

Este es un kit gratuito para que la gente de tu empresa empiece a usar
**Claude Code**, un asistente de IA que trabaja sobre los archivos de tu
computadora en vez de solo conversar contigo. En una sesión en vivo, cada
persona pasa de no haberlo usado nunca a hacer una tarea real de su propio
trabajo. No escribe código: le da a Claude instrucciones (*prompts*) que ya
vienen escritas. Además sale con su propio «segundo cerebro», una carpeta de
notas en texto simple, en su computadora, que la IA lee y mantiene al día.

- **Para quién es:** el dueño de un negocio, o alguien de tu equipo que
  elijas para dirigirlo (el *facilitador*), y las personas a las que
  incorpora (los *participantes*). Nadie necesita formación técnica.
- **Cuánto cuesta:** el kit es gratis. Cada participante necesita su propio
  plan de Claude. **Claude Pro** (unos 20 USD al mes; revisa
  [claude.com/pricing](https://claude.com/pricing)) alcanza para empezar, y
  solo subes de plan si chocas seguido con sus límites.
- **Cuánto tiempo toma:** los participantes hacen las instalaciones por su
  cuenta antes de la sesión, y después tienen una sesión en vivo, solos o en
  un grupo pequeño. Si todo sale bien, la sesión dura unos 90 minutos.
  Calcula 2–3 horas para tus primeras sesiones, y más si es un grupo.
- **Ediciones:** inglés y español, Mac y Windows.

**Empieza aquí:**

- **Voy a dirigir una sesión** → [Manual del facilitador (Doc 05)](Co-Facilitator%20Kit%20(ES)/05%20%E2%80%94%20Facilitator%20Manual%20%E2%80%94%20How%20to%20Run%20a%20Phase%200%20Session.md)
- **Soy participante** → [Antes de tu sesión (Doc 01)](Co-Facilitator%20Kit%20(ES)/01%20%E2%80%94%20Pre-Session%20Setup%20Instructions%20(Participant).md)
- **Quiero ver todo** → [Índice completo del kit](Co-Facilitator%20Kit%20(ES)/README%20%E2%80%94%20Kit%20Index%20%26%20How%20to%20Use.md)

---

## Qué hay en este repositorio

| Carpeta | Qué es |
|---|---|
| [`Co-Facilitator Kit (ES)/`](Co-Facilitator%20Kit%20(ES)/) · [`(EN)/`](Co-Facilitator%20Kit%20(EN)/) | Los materiales de la sesión. El manual del facilitador (Doc 05) es el núcleo; léelo primero. El índice del kit lista cada documento y a quién se le envía. |
| `Co-Facilitator Kit (…)/tools/` | `aiac-status-check.sh`, un chequeo de solo lectura que el participante corre antes de la sesión. Termina con un bloque corto de líneas `DONE` (hecho) / `NOT DONE` (no hecho) que se puede compartir sin riesgo; el participante envía **solo ese bloque**. El script imprime en inglés a propósito: es el mismo archivo para las dos ediciones. |
| `bin/` · `.githooks/` · `tests/` | La compuerta de datos privados que mantiene los datos de participantes fuera de este repositorio (ver Contribuir). |

Es el método que usa el AI Acceleration Club para su propio onboarding,
publicado gratis y como código abierto para que cualquiera lo use con su
equipo.

## No depende de una sola herramienta de IA

El método son archivos de texto simple (notas en Markdown, unos pocos
archivos de instrucciones) más herramientas estándar como Git y GitHub. Tus
notas y proyectos se pueden leer con cualquier editor y son tuyos. **Hoy
recomendamos Claude Code**, y todos los prompts del kit están escritos para
él, pero el *vault*, los *briefs* de proyecto y los hábitos te sirven igual si
algún día cambias a otra herramienta de IA.

## Qué edición enviar

Se decide **por participante**, nunca por facilitador. La edición en español
usa español latinoamericano neutro con **tuteo**. `00V` recoge las
diferencias del voseo argentino como tabla de diferencias, no como
bifurcación. Los participantes en Windows reciben las ediciones `W` de los
Docs 02 y 03. El [índice del kit](Co-Facilitator%20Kit%20(ES)/README%20%E2%80%94%20Kit%20Index%20%26%20How%20to%20Use.md)
tiene la lista completa de qué enviar.

## Reglas de entrega

- Envía **Markdown**, nunca Word ni PDF: una comilla tipográfica dentro de un
  bloque JSON o de un comando rompe en vivo, a mitad de sesión.
- Los prompts largos **se cargan por archivo, no se pegan**: el participante
  guarda el documento y le dice a Claude «Lee el archivo <ruta> y sigue sus
  instrucciones». Las terminales, sobre todo la de Windows, pueden cortar un
  texto largo pegado.
- Envía `tools/aiac-status-check.sh.txt`, no el `.sh`, porque WhatsApp y
  Gmail bloquean los adjuntos `.sh`. Los dos archivos son idénticos byte a
  byte, a propósito. El participante corre el nombre exacto que recibió, por
  ejemplo `bash ~/Downloads/aiac-status-check.sh.txt`, y comparte solo el
  bloque entre `----- AIAC STATUS (safe to share) -----` y `----- END -----`.
  Cuando Claude lo corre por él, agrega `--share`, que imprime solo ese
  bloque, así el detalle nunca llega al contexto de Claude.

## Contribuir

Las correcciones que salen de sesiones reales son lo más valioso: un comando
que falló en la máquina de alguien, un paso que confundió a un participante,
una traducción que suena mal. Lee [`CONTRIBUTING.md`](CONTRIBUTING.md). Lo
primero después de clonar:

```bash
bash bin/install-hooks.sh
```

`git clone` no copia `.git/hooks`, así que este comando activa la compuerta de
datos privados en tus commits. CI corre la misma compuerta en cada PR.

**Qué detecta la compuerta y qué no:** bloquea las direcciones de correo que
no están en la lista permitida y los archivos internos que se dejan fuera del
kit público a propósito. **No** detecta automáticamente nombres, teléfonos ni
secretos. Eso lo atrapa la revisión humana, así que nunca pongas datos de un
participante en un *issue* ni en un PR.

## Seguridad

Para reportar un problema de seguridad o privacidad (por ejemplo, que el
chequeo de estado muestre algo que no debería, un hueco en la compuerta o un
prompt de configuración que dé más permisos de los que dice), revisa
[`SECURITY.md`](SECURITY.md). Repórtalo en privado; no abras un *issue*
público.

## Créditos

Creado por el AI Acceleration Club. Probado en campo y ampliado por
**Mangan** ([@dibkorma](https://github.com/dibkorma)), que corrió el kit por su
cuenta con diez estudiantes. Las ediciones Windows, el sandbox opcional
(`02-S`), el chequeo de pre-sesión y las reglas de entrega salieron de su
reporte de campo.

## Licencia

- **Contenido** (todo lo de las carpetas del Kit salvo `tools/`):
  [Creative Commons Atribución 4.0](LICENSE). Úsalo, tradúcelo, adáptalo,
  republícalo, úsalo comercialmente; da crédito a "AIAC Facilitator Pack, AI
  Acceleration Club".
- **Código** (`tools/`, `bin/`, `.githooks/`, `tests/`): [MIT](LICENSE-CODE).

Ninguna de las dos licencias cubre el nombre **AI Acceleration Club**. Puedes
decir que tu sesión usa el AIAC Facilitator Pack, pero por favor no te
presentes como facilitador certificado por AIAC si no lo eres.
