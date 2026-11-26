# Security policy

**English** · [Español](#política-de-seguridad)

## Reporting a problem

If you find a security or privacy problem in this kit, please report it
**privately** and don't open a public issue or PR.

1. Go to the repo's **Security** tab and choose **Report a vulnerability**
   (GitHub private vulnerability reporting). Only the maintainers can see the
   report.
2. If that button isn't available, open a public issue titled **"Security
   contact request"** with **no details**. A maintainer will reply and set up
   a private channel.

Please include what you ran, on which operating system, what happened, and
what you expected. **Do not include real participant data**, meaning no
names, email addresses, screenshots of someone's machine or excerpts from
their vault. Placeholders such as `YOUR-USER` or `/home/YOUR-USER/...` are
enough.

We aim to acknowledge reports within a week. Fixes land in both language
editions together.

## In scope

- **`tools/aiac-status-check.sh`** (and its `.sh.txt` twin): anything it
  prints that a participant could leak by sharing the "safe to share" block,
  such as names, emails, tokens, full paths or repository URLs; anything it
  writes or changes (it is meant to be read-only).
- **The private-data gate** (`bin/`, `.githooks/`, `.github/workflows/`): a
  way to get an email address or a withheld file past it, or a way for a pull
  request to change what the gate checks.
- **Setup prompts that grant permissions** (Docs 02, 02W, 02-S, 03, 03W): a
  prompt that grants broader or longer-lasting access than it says, overwrites
  a participant's existing settings or restrictions, exposes credentials, or
  publishes something without the participant confirming it first.
- **Third-party installs the kit points to** (for example the pinned starter
  skills): a pinned version that is compromised or does something the kit
  doesn't describe.

## Out of scope

- Bugs in Claude Code, Git, GitHub, Obsidian or other third-party tools
  themselves. Report those to their vendors.
- Typos, unclear wording or steps that fail without a security or privacy
  impact. Open a normal issue or PR for those (see `CONTRIBUTING.md`).

---

# Política de seguridad

[English](#security-policy) · **Español**

## Cómo reportar un problema

Si encuentras un problema de seguridad o de privacidad en este kit,
repórtalo **en privado** y no abras un *issue* ni un PR público.

1. Ve a la pestaña **Security** del repositorio y elige **Report a
   vulnerability** (el reporte privado de vulnerabilidades de GitHub). Solo
   los mantenedores ven el reporte.
2. Si ese botón no aparece, abre un *issue* público titulado **«Security
   contact request»** **sin ningún detalle**. Un mantenedor te responderá y
   abrirá un canal privado.

Incluye qué corriste, en qué sistema operativo, qué pasó y qué esperabas.
**No incluyas datos reales de participantes**: ni nombres, ni correos, ni
capturas de la máquina de alguien, ni fragmentos de su *vault*. Con marcadores
como `YOUR-USER` o `/home/YOUR-USER/...` basta.

Intentamos acusar recibo en menos de una semana. Las correcciones se aplican
en las dos ediciones de idioma a la vez.

## Qué entra

- **`tools/aiac-status-check.sh`** (y su gemelo `.sh.txt`): cualquier cosa que
  imprima y que un participante pueda filtrar al compartir el bloque «safe to
  share», como nombres, correos, *tokens*, rutas completas o URLs de
  repositorios, y cualquier cosa que escriba o modifique (debe ser de solo
  lectura).
- **La compuerta de datos privados** (`bin/`, `.githooks/`,
  `.github/workflows/`): una forma de colar una dirección de correo o un
  archivo retenido, o de que un *pull request* cambie lo que la compuerta
  revisa.
- **Los prompts de configuración que otorgan permisos** (Docs 02, 02W, 02-S,
  03, 03W): un prompt que dé acceso más amplio o más duradero del que dice,
  que sobrescriba la configuración o las restricciones existentes del
  participante, que exponga credenciales o que publique algo sin que el
  participante lo confirme antes.
- **Instalaciones de terceros a las que apunta el kit** (por ejemplo, las
  *skills* iniciales fijadas por versión): una versión fijada que esté
  comprometida o que haga algo que el kit no describe.

## Qué no entra

- Errores de Claude Code, Git, GitHub, Obsidian u otras herramientas de
  terceros en sí mismas. Repórtalos a sus fabricantes.
- Errores de tipeo, redacción poco clara o pasos que fallan sin impacto de
  seguridad o privacidad. Para eso abre un *issue* o un PR normal (ver
  `CONTRIBUTING.md`).
