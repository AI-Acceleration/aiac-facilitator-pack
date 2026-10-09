# AIAC Facilitator Pack

Todo lo que necesitas para facilitarle a otra persona una **sesión de
Fase 0**: en pocas horas el participante pasa de cero a trabajar con Claude
Code sobre su propio caso real, dentro de una bóveda de conocimiento personal.
En inglés y en español.

Es el método que usa el AI Acceleration Club para su propio onboarding,
publicado gratis y como código abierto para que cualquiera lo corra con su
equipo.

| Carpeta | Qué es |
|---|---|
| `Co-Facilitator Kit (ES)/` · `(EN)/` | Los materiales de la sesión. `05 — Facilitator Manual` es el núcleo; léelo primero. |
| `Co-Facilitator Kit (…)/tools/` | `aiac-status-check.sh`, un diagnóstico de pre-sesión de solo lectura que reporta HECHO / NO HECHO por documento. |
| `bin/` · `.githooks/` · `tests/` | La compuerta de datos privados que mantiene los datos de participantes fuera de este repo (ver Contribuir). |

**Empieza aquí:** `Co-Facilitator Kit (ES)/README — Kit Index & How to Use.md`,
y luego `05 — Facilitator Manual — How to Run a Phase 0 Session.md`.

## Qué edición enviar

Se decide **por participante**, nunca por facilitador. El español usa **tuteo**
venezolano por defecto; `00V` recoge las diferencias del voseo argentino como
tabla de diferencias, no como bifurcación. Los participantes en Windows reciben
las ediciones `W` de los Docs 02 y 03.

## Reglas de entrega

- Envía **Markdown**, nunca Word ni PDF: una comilla tipográfica dentro de un
  bloque JSON o de un comando rompe en vivo, a mitad de sesión.
- Envía `tools/aiac-status-check.sh.txt`, no el `.sh`: WhatsApp y Gmail bloquean
  los adjuntos `.sh`. Los dos archivos son idénticos byte a byte, a propósito.
- Se ejecuta con `bash aiac-status-check.sh`.

## Contribuir

Las correcciones que salen de sesiones reales son lo más valioso: un comando
que falló en la máquina de alguien, un paso que confundió a un participante,
una traducción que suena mal. Lee `CONTRIBUTING.md`. Lo primero después de
clonar:

```bash
bash bin/install-hooks.sh
```

`git clone` no copia `.git/hooks`; esto activa la compuerta de datos privados
en tus commits. CI corre la misma compuerta en cada PR.

## Créditos

Creado por el AI Acceleration Club. Probado en campo y ampliado por
**Mangan** ([@dibkorma](https://github.com/dibkorma)), que corrió el kit por su
cuenta con diez estudiantes: las ediciones Windows, el sandbox opcional
(`02-S`), el chequeo de pre-sesión y las reglas de entrega salieron de su
reporte de campo.

## Licencia

- **Contenido** (todo lo de las carpetas del Kit salvo `tools/`):
  [Creative Commons Atribución 4.0](LICENSE). Úsalo, tradúcelo, adáptalo,
  úsalo comercialmente; da crédito a "AIAC Facilitator Pack, AI Acceleration Club".
- **Código** (`tools/`, `bin/`, `.githooks/`, `tests/`): [MIT](LICENSE-CODE).

Ninguna de las dos licencias cubre el nombre **AI Acceleration Club**. Puedes
decir que tu sesión usa el AIAC Facilitator Pack; por favor no te presentes
como facilitador certificado por AIAC si no lo eres.
