---
title: "Configuración de Sandbox (Participante) — AI Acceleration Club Fase 0"
created: 2026-07-15
category: reference
tags: [aiac, phase0, co-facilitator-kit, participant, sandbox, security]
lang: es
translated_from: "02-S — Sandbox Setup (Participant, opt-in).md"
---

**Apoya:** Ejecuta esto ANTES del Doc 02. Agrega un sandbox de kernel y una lista `deny` encima del bloque de permisos del PASO 3 del Doc 02.

# Configuración de Sandbox — Confinar Claude Code a tu vault

Este documento es para un participante que quiere un límite **verificable** alrededor de Claude Code, no la promesa de uno. Está escrito para alguien técnico. No simplifica, y no sobrevende.

Lee la Parte 1 antes de ejecutar nada. Te dice qué estás obteniendo de verdad — incluyendo lo que **no** estás obteniendo. Si las garantías de la Parte 1 no te resultan suficientes, la Parte 6 te dice qué hacer en su lugar.

> **En cada pregunta de permiso, elige el "Yes" simple (o "No") — nunca "Yes, and don't ask again".**
> La opción "don't ask again" guarda una regla duradera en tus ajustes que deja correr ese comando sin
> preguntar desde entonces, y el chequeo de estado reporta la mayoría de esas reglas, no todas.

---

## Parte 1 — Qué garantiza esto de verdad

Primero la afirmación honesta, porque la versión de marketing de esto es falsa.

**Claude Code no corre "dentro de un sandbox".** No hay un único límite alrededor del proceso. Hay dos mecanismos de aplicación distintos que cubren dos conjuntos distintos de herramientas, y tienen fortalezas muy diferentes:

| Qué se ejecuta | Aplicado por | Fortaleza |
|---|---|---|
| **Comandos de Bash y cada proceso hijo que lanzan** (incluyendo `python`, `node`, `git`, cualquier script) | El kernel del sistema operativo — Seatbelt en macOS, bubblewrap en Linux/WSL2 | **Duro.** Se aplica sobre el proceso en ejecución. Se sostiene sin importar qué decidió ejecutar el modelo, e incluso si un comando permitido hace más de lo que su nombre sugiere. |
| **Las herramientas de archivos integradas de Claude** — Read, Edit, Write, Glob, Grep | El sistema de permisos de Claude Code, en proceso, evaluado *antes* de que la herramienta corra | **A nivel de aplicación.** Las reglas de denegación son absolutas (gana la primera coincidencia, sin excepciones posibles), pero esto es Claude Code aplicándose reglas a sí mismo, no el kernel aplicándoselas a un proceso. |

De la documentación oficial (citada de las páginas vigentes al 2026-11-25):

> "The sandbox covers shell commands only. Claude's file tools, MCP servers, and hooks run outside it."

y

> "**Built-in file and web tools**: tools such as Read, Edit, Write, WebFetch, and WebSearch follow permission rules instead. A `denyRead` entry doesn't stop the Read tool, and `allowedDomains` doesn't limit WebFetch"

Así que la frase precisa, para la configuración de abajo, es:

- **Todo lo que Claude ejecuta a través de Bash** (y cada proceso hijo) queda confinado por el kernel:
  puede **escribir** solo en la carpeta de trabajo (tu vault), en la carpeta temporal de la sesión y en el
  único repositorio de código que nombres en la Parte 3c; puede **leer** tu vault, ese repositorio y
  `~/.claude` (la configuración, las *skills* y los plugins de Claude Code), pero **nada más dentro de tu
  carpeta de usuario** — y tampoco el archivo de inicio de sesión de Claude
  Code, `~/.claude/.credentials.json` (donde Linux y WSL2 guardan tu token de acceso), que la Parte 3a
  vuelve a denegar para que ningún comando pueda leerlo y enviarlo a un dominio permitido como `github.com`. Las rutas fuera de tu carpeta de usuario (carpetas
  del sistema como `/usr` o `/etc`) siguen siendo legibles — la regla de denegación cubre `~/`, no todo el disco.
- **Todo lo que Claude lee o escribe con sus herramientas de archivos integradas** se rige por reglas de
  permisos que Claude Code evalúa antes de actuar: el vault por defecto, una solicitud de permiso para
  cualquier otra cosa, y un bloqueo duro para la lista `deny`.
- **Fuera de las dos capas:** los *hooks* y los servidores MCP (detalles abajo).

Ambas capas se configuran abajo. Ninguna es decorativa, y ninguna es una máquina virtual.

### Por qué la capa de Bash es la que importa

Esta es la parte que vale la pena entender, porque es la razón por la que la configuración estándar de AIAC no te alcanza.

Reglas de permisos como `Read(~/.ssh/**)` en una lista de denegación funcionan sobre las herramientas de archivos propias de Claude y sobre los comandos de archivos que Claude Code reconoce en Bash (`cat`, `head`, `tail`, `sed`). **No** funcionan sobre subprocesos arbitrarios. La documentación (página vigente al 2026-11-25):

> "They also don't apply to arbitrary subprocesses that read or write files indirectly, like a Python or Node script that opens files itself. For OS-level enforcement on sandboxed shell commands, enable the sandbox and turn off the unsandboxed retry."

Versiones anteriores de la configuración de Fase 0 preaprobaban la ejecución de Python sin restricciones y tenían una **lista de denegación vacía**. Con esa combinación, un script de Python de una línea lee cualquier cosa en la máquina, y ninguna regla de permisos puede detenerlo. El Doc 02 ya no preaprueba ningún intérprete, así que fuera del sandbox Claude tiene que preguntar antes de ejecutar uno — pero una vez que apruebas un script, las reglas de permisos siguen sin ver qué abre. Una lista de denegación por sí sola es teatro frente a un subproceso. El sandbox es lo que cierra ese hueco — y lo cierra en el kernel, que es por lo que se sostiene incluso si el modelo está confundido, equivocado o manipulado por algo que leyó.

### Contra qué NO protege esto

Dicho sin rodeos para que decidas tú:

- **La capa de red no inspecciona TLS.** El proxy integrado permite o bloquea según el nombre de host que el cliente declara. La documentación advierte que las listas de permisos amplias "can create paths for data exfiltration" vía *domain fronting*. Nuestra configuración permite un conjunto estrecho.
- **Los *hooks* no están confinados.** Trata cada *hook* como si corriera con todos tus permisos de usuario. Importan aquí porque el Paso 3.5 del Doc 02 instala tres (el script de la statusline y dos *hooks*) — comandos de shell que *tú* instalas y puedes leer completos antes de que corran siquiera, así que están dentro de tu límite de confianza por inspección, no por aplicación.
- **Los servidores MCP y los conectores no están confinados.** Las reglas de permisos aplican sobre sus herramientas; el sandbox no confina el proceso del servidor.
- **Las variables de entorno.** Los comandos confinados heredan el entorno de tu shell, incluyendo cualquier secreto que haya en él. La Parte 3 se encarga de esto.
- **Esto no es una máquina virtual.** La documentación: "Sandboxing reduces risk but is not a complete isolation boundary." Si tu modelo de amenaza necesita un único límite de kernel alrededor de todo el proceso de Claude Code, ve a la Parte 6.

---

## Parte 2 — Compuerta de disponibilidad (haz esto primero)

**El sandbox corre en macOS, Linux y WSL2. Windows nativo no está soportado.**

- **macOS** — no hay nada que instalar. Usa el framework Seatbelt integrado. Estás listo.
- **Windows** — tienes que correr Claude Code **dentro de una distribución WSL2**. WSL1 no funciona (bubblewrap necesita características del kernel que solo tiene WSL2). Verifica con `wsl -l -v` en PowerShell. Dentro de la distro: `sudo apt-get install bubblewrap socat`.
- **Linux** — `sudo apt-get install bubblewrap socat` (o `sudo dnf install bubblewrap socat`).

> **En Ubuntu 24.04+ (incluyendo bajo WSL2):** ejecuta `sysctl kernel.apparmor_restrict_unprivileged_userns`. Si devuelve `1`, AppArmor le impide a bubblewrap crear *user namespaces* y necesitas un perfil de AppArmor para `bwrap` — la documentación de sandboxing trae el perfil exacto. Si la clave no existe o devuelve `0`, sáltate esto.

**Si estás en Windows nativo sin WSL2, para aquí.** No hay sandbox, y el resto de este documento no puede darte lo que estás pidiendo. Avísale al facilitador antes de la sesión — las opciones son WSL2, un contenedor/máquina virtual, o correr la Fase 0 sin la garantía.

Verifica la disponibilidad antes de confiar en nada: inicia Claude Code y ejecuta `/sandbox`. Si el panel muestra **solo una pestaña de Dependencies**, falta algo — instálalo, reinicia Claude Code (la verificación de dependencias corre al arrancar) y vuelve a ejecutarlo.

---

## Parte 3 — La configuración

Dos archivos. Crea ambos **antes** de entregarle el Doc 02 a Claude Code, a mano, para que Claude quede confinado desde su primerísima llamada a una herramienta y no después de haber construido medio vault.

### 3a — Ajustes del proyecto: `<YOUR_VAULT>/.claude/settings.json`

**Este archivo debe vivir en tu vault**, no en `~/.claude/`. Eso sostiene el diseño, no es estético. La ruta `.` resuelve a la raíz del proyecto **solo** cuando la configuración vive en los ajustes del proyecto. La documentación (página vigente al 2026-11-25):

> "Place it in your project's `.claude/settings.json`, because the relative path `.` resolves to the project root when the configuration lives in project settings" … "If you placed the same configuration in `~/.claude/settings.json`, `.` would resolve to `~/.claude` instead, and project files would remain blocked by the `denyRead` rule."

```json
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false,
    "filesystem": {
      "denyRead": ["~/", "~/.claude/.credentials.json"],
      "allowRead": [".", "~/.claude"],
      "allowWrite": []
    },
    "network": {
      "allowedDomains": [
        "github.com",
        "api.github.com",
        "codeload.github.com",
        "registry.npmjs.org",
        "pypi.org",
        "files.pythonhosted.org"
      ]
    }
  }
}
```

Línea por línea, porque no deberías aceptar ninguna de estas bajo mi palabra:

- **`denyRead: ["~/"]` + `allowRead: ["."]`** — la política de lectura por defecto del sandbox es **acceso de lectura a toda tu computadora**. Habilitar el sandbox por sí solo *no* restringe las lecturas. Este par es el patrón documentado para invertir eso a denegar-por-defecto: bloquea todo `$HOME`, luego vuelve a permitir la raíz del proyecto. Fíjate en la asimetría con las reglas de permisos — el `allowRead` del sandbox **sí puede** volver a permitir dentro de una región de `denyRead`; las reglas de denegación de permisos **no pueden** llevar excepciones. Sistemas distintos, semánticas distintas.
- **`allowRead` incluye `~/.claude`** — sin esto, los comandos confinados ni siquiera pueden leer la configuración propia de Claude Code (`claude plugin list`, la verificación de *skills* del Paso 2.7c del Doc 03 y la verificación del router fallan). Ten claro lo que significa: **cualquier cosa que ejecute Bash puede leer `~/.claude`** — tu `CLAUDE.md` global, los ajustes, las *skills*, los archivos de plugins y las transcripciones de sesión (todo menos el archivo de inicio de sesión, siguiente punto). Y es **solo lectura**: **no** hace que `~/.claude` sea escribible, así que las instalaciones dentro de `~/.claude` siguen fallando bajo el sandbox (Parte 3d). Claude Code además **auto-deniega las escrituras a `settings.json` en todos los ámbitos**, así que un comando confinado no puede reescribir su propia política.
- **`denyRead` también lista `~/.claude/.credentials.json`** — en Linux y WSL2, Claude Code guarda tu token de acceso en ese archivo (en macOS vive en el Llavero, así que ahí la entrada simplemente no coincide con nada). `allowRead` vuelve a abrir todo `~/.claude`, y `github.com` es un dominio permitido; la documentación advierte: "Allowing broad domains such as `github.com` can create paths for data exfiltration." Cuando las reglas de lectura se superponen, gana la ruta más estrecha — la documentación: "The deny holds inside a wider allow, so a broad allow can't silently re-expose a secret." Así, esta sola entrada mantiene el token lejos de todo comando confinado, mientras el resto de `~/.claude` sigue siendo legible.
- **`allowWrite: []`** — las escrituras ya van por defecto al directorio de trabajo + el directorio temporal de la sesión. Vacío significa que no agregamos nada a eso.
- **`failIfUnavailable: true`** — **este es el ajuste del que de verdad depende tu solicitud.** Por defecto, si el sandbox no puede arrancar (dependencia faltante, plataforma no soportada), Claude Code *imprime una advertencia y corre tus comandos sin confinar de todas formas*. Eso es una degradación silenciosa de "confinado" a "no confinado". Esto lo convierte en una falla dura. Sin esta línea, nada de lo anterior es una garantía.
- **`allowUnsandboxedCommands: false`** — el interruptor de "modo sandbox estricto". Por defecto, cuando un comando falla por una restricción del sandbox, Claude puede reintentarlo con `dangerouslyDisableSandbox`, lo que lo corre fuera del límite (sujeto a una solicitud de permiso). Esto hace que ese parámetro sea **completamente ignorado**. Fíjate en el intercambio: algunas herramientas genuinamente no funcionan confinadas (`docker`, `watchman`/`jest`, y los CLI hechos en Go como `gh` pueden fallar la verificación TLS bajo Seatbelt en macOS). Con esto apagado, fallan en vez de escapar. Ese es el trato que estás pidiendo. Si `gh` se rompe, ejecuta tú los pasos de `gh` en una terminal normal (Parte 5) — nunca recurras a un *personal access token* clásico.
- **`network.allowedDomains`** — no hay dominios pre-permitidos por defecto; el primer intento hacia un dominio nuevo te pregunta. Esta lista pre-aprueba solo lo que la Fase 0 necesita (GitHub, npm, PyPI) para que no termines aprobando por fatiga de clics algo que no leíste. Todo lo demás sigue preguntando. Mantenla estrecha — una entrada amplia aquí es la vía de exfiltración de la que advierte la documentación.

**Déjalo exactamente así — en todos los archivos de ajustes.** Claude Code combina las listas de rutas y
dominios del sandbox de todos los archivos de ajustes que carga (el `.claude/settings.json` y el
`.claude/settings.local.json` de tu vault, donde `/sandbox` guarda lo que eliges, tu `~/.claude/settings.json`
global y cualquier política que instale tu organización), y un archivo posterior puede apagar un ajuste. Así
que el límite es tan estrecho como todos ellos juntos. El chequeo de estado (`--sandbox`) lee cada uno de esos
archivos y reporta esta parte `NOT DONE` — nunca `DONE` — cuando, juntos:

- permiten un dominio que no es uno de los seis de arriba (una aprobación guardada `WebFetch(domain:…)`
  también cuenta), o dejan alguno fuera;
- hacen legible o escribible algo más allá del vault, `~/.claude` y el único repositorio de la Parte 3c —
  incluidas reglas `allow` de `Read`/`Edit`/`Write` y `additionalDirectories`, cuyas rutas se suman al sandbox;
- ponen al revés uno de los tres interruptores de arriba;
- listan `excludedCommands` (esos corren **fuera** del sandbox, con todo tu acceso);
- ponen `filesystem.disabled` (apaga el aislamiento de archivos y deja solo el filtro de red — lo pueden poner
  los ajustes de usuario y los administrados, no los del proyecto), o cualquier otro interruptor que afloje:
  aislamiento anidado o de red más débil, Apple Events, espacios de nombres de usuario anidados, sockets Unix,
  búsquedas Mach, escuchar en puertos locales o un proxy propio ([documentación del sandbox](https://code.claude.com/docs/en/sandboxing)).

Si un archivo de ajustes o de política existe pero no se puede leer, el chequeo dice "unverified" (no
verificado) y reporta `NOT DONE`. No puede ver ajustes pasados con `--settings` ni enviados por un perfil MDM:
`/sandbox` → **Config** (Parte 4, paso 1) muestra el resultado resuelto y es la última palabra.

Dos cosas que obtienes gratis y vale la pena saber: el sandbox **auto-deniega las escrituras al propio `settings.json` de Claude Code en todos los ámbitos**, así que un comando confinado no puede reescribir su propia política. Y **los subagentes heredan la configuración de sandbox de la sesión padre** — corren en el mismo proceso, así que no hay bypass ahí.

> **`sandbox.credentials` (opcional; mira la [documentación de sandboxing](https://code.claude.com/docs/en/sandboxing) para los detalles vigentes).** Este bloque deniega explícitamente los archivos de credenciales y desactiva las variables de entorno secretas para los comandos confinados. Nuestro `denyRead: ["~/"]` ya cubre los archivos bajo `$HOME`, y esto agrega la mitad de las variables de entorno:
> ```json
> "credentials": {
>   "files": [
>     { "path": "~/.aws/credentials", "mode": "deny" },
>     { "path": "~/.ssh", "mode": "deny" }
>   ],
>   "envVars": [
>     { "name": "GITHUB_TOKEN", "mode": "deny" },
>     { "name": "AWS_SECRET_ACCESS_KEY", "mode": "deny" }
>   ]
> }
> ```
> No hay una lista de denegación de credenciales integrada — solo se restringe lo que tú listes.

### 3b — Ajustes globales: `~/.claude/settings.json`

Esto cubre las herramientas de archivos integradas, que el sandbox no cubre. Las listas `allow` y `ask` son **las mismas del PASO 3 del Doc 02**; lo que agrega este bloque es la **lista `deny` dirigida** (las rutas joya de la corona, abajo). Úsalo en lugar del bloque del Doc 02 — y, igual que en el Doc 02, **fusiónalo con tu `~/.claude/settings.json` existente sin mostrarlo** (ese archivo puede guardar llaves de API): respalda el archivo, guarda el bloque y ejecuta el script de fusión de esta sección en una **terminal normal**.

```json
{
  "permissions": {
    "allow": [
      "Bash(git status)",
      "Bash(git status --short)",
      "Bash(git diff)",
      "Bash(git log --oneline)",
      "Bash(git remote -v)",
      "Bash(ls *)",
      "Bash(wc *)"
    ],
    "ask": [
      "Bash(cat *)",
      "Bash(head *)",
      "Bash(tail *)",
      "Bash(grep *)",
      "Bash(diff *)",
      "Bash(sed *)",
      "Bash(sort *)",
      "Bash(git show *)",
      "Bash(git -C *)",
      "Bash(git -c *)",
      "Bash(git add *)",
      "Bash(git commit *)",
      "Bash(git push *)",
      "Bash(gh repo create *)"
    ],
    "deny": [
      "Read(~/.ssh/**)",
      "Read(~/.aws/**)",
      "Read(~/.gnupg/**)",
      "Read(~/.config/gh/**)",
      "Read(~/Library/Keychains/**)",
      "Read(~/.claude/.credentials.json)",
      "Read(~/**/.env)",
      "Read(~/**/*.pem)",
      "Read(~/**/*.key)"
    ]
  },
  "hooks": {
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "afplay /System/Library/Sounds/Blow.aiff" }
        ]
      }
    ]
  }
}
```

#### Canonical deny list

Esta es la lista completa. Cada entrada es obligatoria — la comprobación de estado (`--sandbox`) marca
esta parte como `NOT DONE` si falta cualquiera de ellas en `permissions.deny`:

```text
Read(~/.ssh/**)
Read(~/.aws/**)
Read(~/.gnupg/**)
Read(~/.config/gh/**)
Read(~/Library/Keychains/**)
Read(~/.claude/.credentials.json)
Read(~/**/.env)
Read(~/**/*.pem)
Read(~/**/*.key)
```

`Read(~/.claude/.credentials.json)` es la mitad de las herramientas integradas de la protección del
archivo de inicio de sesión de la Parte 3a (la entrada del sandbox cubre Bash; esta cubre la herramienta
Read de Claude).

Cada ruta está anclada en tu carpeta de usuario (`~/`). Es deliberado: en la sintaxis de rutas de Claude
Code, un patrón sin prefijo, como `**/*.key`, es relativo a la carpeta desde donde arrancó Claude, así que
no vería un archivo de llave fuera del vault ([patrones de ruta](https://code.claude.com/docs/en/permissions)).
`~/**/*.key` cubre toda tu carpeta de usuario, vault incluido. Las reglas de denegación bloquean las
herramientas de archivos de Claude y los comandos de archivos que Claude Code reconoce en Bash (`cat`,
`head`, `tail`, `sed`), no scripts arbitrarios — esa parte es tarea del sandbox.

**Fusiónalo sin leer tu archivo existente.** En una terminal normal:

```bash
mkdir -p ~/.claude
```

Luego guarda el bloque JSON de arriba como `~/.claude/aiac-02s-block.json` (antes edita la línea de
`Stop` — mira abajo), guarda el script de abajo como `~/.claude/aiac-merge-settings.py` (es el mismo
script que usa el Paso 3 del Doc 02) y ejecuta
`python3 ~/.claude/aiac-merge-settings.py ~/.claude/aiac-02s-block.json`. Agrega cada entrada que falte,
conserva cada clave y regla que ya tenías, imprime solo las entradas del kit y los *nombres* de las
claves que no tocó, y su última línea tiene que empezar con `Verified:`. Antes de cambiar nada guarda
un respaldo privado de tu archivo actual (del archivo real, si `settings.json` es un enlace simbólico) e
imprime su nombre: `~/.claude/settings.json.bak` la primera vez, el siguiente nombre libre
`settings.json.bak.1`, `.bak.2`, … si ya hay un respaldo anterior (nunca sobrescribe uno anterior). Usa el
archivo de respaldo que nombra el script.

```python
# aiac-merge-settings.py - merges the AIAC kit's entries into ~/.claude/settings.json.
# It never prints existing values: only the kit entries it added and the names
# of keys you already had. Usage: python3 aiac-merge-settings.py [--replace KEY] - < block
import json
import os
import re
import shutil
import sys

TARGET = os.path.expanduser("~/.claude/settings.json")
BACKUP = TARGET + ".bak"
DEEP = ("permissions", "hooks", "env")  # top-level objects merged key by key
HOOK_EVENTS = ("Stop", "UserPromptSubmit", "PreCompact")


def stop(message):
    sys.exit("STOP: " + message + " Nothing was changed.")


def number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0


def hook_groups(v):
    return isinstance(v, list) and all(
        isinstance(g, dict) and set(g) <= {"matcher", "hooks"}
        and isinstance(g.get("matcher", ""), str)
        and isinstance(g.get("hooks"), list) and len(g["hooks"]) > 0
        and all(isinstance(h, dict) and set(h) <= {"type", "command", "timeout"}
                and h.get("type") == "command"
                and isinstance(h.get("command"), str) and h["command"] != ""
                and ("timeout" not in h or number(h["timeout"]))
                for h in g["hooks"])
        for g in v)


# The only shapes a kit block may have. Checked before anything is merged,
# whether or not your settings already have the key.
SCHEMA = {
    "permissions": lambda v: isinstance(v, dict) and set(v) <= {"allow", "ask", "deny"}
    and all(isinstance(x, list) and all(isinstance(r, str) for r in x) for x in v.values()),
    "hooks": lambda v: isinstance(v, dict) and set(v) <= set(HOOK_EVENTS)
    and all(hook_groups(x) for x in v.values()),
    "env": lambda v: isinstance(v, dict) and all(isinstance(x, str) for x in v.values()),
    "statusLine": lambda v: isinstance(v, dict) and set(v) <= {"type", "command", "padding"}
    and v.get("type") == "command" and isinstance(v.get("command"), str) and v["command"] != ""
    and ("padding" not in v or (isinstance(v["padding"], int) and not isinstance(v["padding"], bool))),
}


def check_block(block):
    for key, val in block.items():
        name = key if re.match(r"^[A-Za-z][A-Za-z0-9_]{0,40}$", key) else "a key"
        if key not in SCHEMA:
            stop("the kit block has an entry the kit never uses (" + name + "); check it was copied whole.")
        if not SCHEMA[key](val):
            stop("the kit block's " + name + " entry has the wrong shape; check it was copied whole.")


def merge(dst, new, path, added, kept):
    for key, val in new.items():
        name = ".".join(path + [key])
        deep = isinstance(val, dict) and (path or key in DEEP)
        if key not in dst:
            dst[key] = val
            added.append(name)
        elif (isinstance(val, list) or deep) and type(dst[key]) is not type(val):
            stop(name + " in your settings is not a JSON " +
                 ("list" if isinstance(val, list) else "object") + ", so the kit entries can't be added.")
        elif isinstance(val, list):
            for item in val:
                if item not in dst[key]:
                    dst[key].append(item)
                    added.append(name + ": " + (item if isinstance(item, str) else "1 entry"))
        elif deep:
            merge(dst[key], val, path + [key], added, kept)
        elif dst[key] != val:
            kept.append(name)


def missing(dst, new, path, kept):
    gaps = []
    for key, val in new.items():
        name = ".".join(path + [key])
        if name in kept:
            continue
        if key not in dst:
            gaps.append(name)
        elif isinstance(val, list) and isinstance(dst[key], list):
            gaps += [name for item in val if item not in dst[key]]
        elif isinstance(val, dict) and isinstance(dst[key], dict) and (path or key in DEEP):
            gaps += missing(dst[key], val, path + [key], kept)
    return gaps


def replace(dst, new, dotted):
    keys = dotted.split(".")
    for key in keys[:-1]:
        new = new[key]
        if not isinstance(dst.get(key), dict):
            dst[key] = {}
        dst = dst[key]
    dst[keys[-1]] = new[keys[-1]]


def backup(real):
    """A private copy (0600) of the file's current bytes - the file a symlink
    points at, never the link - made once per run, before the change. An
    earlier backup is never overwritten: the copy goes to the first free name
    (settings.json.bak, then settings.json.bak.1, .bak.2, ...), printed below."""
    name, n = BACKUP, 0
    while os.path.lexists(name):
        n += 1
        name = BACKUP + "." + str(n)
    with open(real, "rb") as f:
        data = f.read()
    fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as f:
        f.write(data)
    return name


def main():
    args, to_replace = sys.argv[1:], []
    while len(args) >= 2 and args[0] == "--replace":
        to_replace.append(args[1])
        args = args[2:]
    try:
        if args and args[0] != "-":
            with open(args[0], encoding="utf-8") as f:
                block = json.load(f)
        else:
            block = json.load(sys.stdin)
    except (OSError, ValueError):
        stop("the kit block could not be read as JSON (check it was copied whole).")
    if not isinstance(block, dict):
        stop("the kit block is not a JSON object.")
    check_block(block)
    # Write through a symlinked settings.json to the file it points at.
    real = os.path.realpath(TARGET)
    current = {}
    if os.path.exists(real):
        try:
            with open(real, encoding="utf-8") as f:
                current = json.load(f)
        except ValueError:
            stop("~/.claude/settings.json is not valid JSON.")
        if not isinstance(current, dict):
            stop("~/.claude/settings.json is not a JSON object.")
    added, kept = [], []
    for dotted in to_replace:
        try:
            replace(current, block, dotted)
        except (KeyError, TypeError):
            stop(dotted + " is not in the kit block.")
        added.append(dotted + " (replaced, as you asked)")
    merge(current, block, [], added, kept)
    kept = [k for k in kept if not any(r.startswith(k + ".") for r in to_replace)]
    saved = None
    if added or not os.path.exists(real):
        os.makedirs(os.path.dirname(real), exist_ok=True)
        if os.path.exists(real):
            try:
                saved = backup(real)
            except OSError:
                stop("could not save a backup of ~/.claude/settings.json first.")
        tmp = real + ".aiac-tmp"
        if os.path.lexists(tmp):
            os.unlink(tmp)
        # Created private (0600) from the start, never briefly readable by others.
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2, ensure_ascii=False)
            f.write("\n")
        if os.path.exists(real):
            shutil.copymode(real, tmp)
        os.replace(tmp, real)
    if saved:
        print("backup of your previous settings (private): ~/.claude/" + os.path.basename(saved))
    for name in added:
        print("added: " + name)
    for name in kept:
        print("kept your existing value (not shown): " + name)
    with open(real, encoding="utf-8") as f:
        gaps = missing(json.load(f), block, [], kept)
    if gaps:
        sys.exit("STOP: still missing after the merge: " + ", ".join(gaps))
    print("Verified: settings.json parses and has every kit entry (%d added)." % len(added))


main()
```

Por qué la lista se ve así, y por qué cada decisión es deliberada:

- **Ningún intérprete (`python`, `node`…) ni `pip install` en `allow`.** Preaprobar un intérprete significa preaprobar "leer o escribir cualquier archivo, sin restricción de ninguna regla de permisos". Con el sandbox activo, los scripts quedan confinados por el kernel de todos modos — y en el modo auto-allow del sandbox corren sin ninguna solicitud de permiso — pero no hay razón para *además* entregarles una preaprobación en blanco: si el sandbox alguna vez falla al cargar, la regla allow que falta es lo que trae de vuelta la solicitud de permiso. (`failIfUnavailable: true` debería hacer eso imposible. Cinturón y tirantes.)
- **Nada de git sin restricciones, ningún permiso de escritura permanente, y reglas `ask` para lo que imprime o publica.** Por las mismas razones que en el Doc 02: solo se preaprueban comandos de git exactos y de solo lectura más `ls` y `wc` (sin comodines, porque opciones como `--output`, `--ext-diff` o `--template` escriben archivos, ejecutan programas o plantan *hooks*). `cat`, `head`, `tail`, `grep`, `diff`, `sed`, `sort` y `git show` pueden imprimir archivos y son comandos integrados de solo lectura que Claude Code ejecuta sin pedir permiso en cualquier lugar del disco salvo que una regla diga otra cosa, así que van en `ask`, junto con `git -C` / `git -c`, `git add`, `git commit`, `git push` y `gh repo create`. Otros comandos de solo lectura (por ejemplo `git log -p`) siguen ejecutándose sin preguntar — el Paso 3 del Doc 02 explica por qué; bajo el sandbox, de todos modos no pueden leer fuera del límite.
- **Nada de `Read`, `Write`, `Edit`, `Glob`, `Grep` a secas en `allow`.** Un nombre de herramienta a secas en `allow` pre-aprueba esa herramienta para **cualquier** entrada — incluyendo rutas fuera de tu vault. Dejarlos fuera mantiene el comportamiento real por defecto: *"By default, Claude has access to files in the directory where you launched it."* Lanza desde el vault, y el vault es el alcance.
- **Entradas `deny` dirigidas, no una amplia.** Fíjate en lo que está **ausente** a propósito: no hay `Read(~/Documents/**)` ni `Read(//**)`. Tu vault vive en tu carpeta de usuario (`~/AIAC-Vault` por defecto), y las reglas de denegación de permisos tienen precedencia sobre las de permiso **sin ninguna excepción posible** — una denegación amplia como esa dejaría a Claude fuera, en silencio, del mismísimo vault que estás tratando de darle. Estas entradas son estrechas a propósito. El límite amplio es tarea del sandbox; esta lista es para las joyas de la corona de las herramientas integradas.
- **El *hook* de sonido es solo para macOS.** En Windows (WSL2) usa `powershell.exe -c "[console]::beep(1000,400)"`; en Linux `paplay /usr/share/sounds/freedesktop/stereo/bell.oga`. Si no estás seguro, borra el bloque `"Stop"` completo — es una comodidad, y un comando equivocado aquí falla en cada turno.

**Revisa también `additionalDirectories`.** Si esa clave existe en cualquier archivo de ajustes, lo que liste se suma al alcance de las herramientas integradas de Claude. Debería estar ausente o vacía. Lo mismo para el flag `--add-dir` y el comando `/add-dir` — no los uses.

### 3c — Nombra el repositorio de código (decídelo antes del Paso 6)

La Fase 0 pone tu repositorio git en **`~/dev/<repo-name>`, fuera del vault** — el Paso 6 del Doc 02 lo crea
ahí y comprueba que quedó ahí, el router lo nombra ahí, y el Doc 04 y el chequeo de estado lo buscan ahí. Eso
choca con un límite solo-vault: con `allowRead: ["."]`, Bash no puede ver `~/dev` en absoluto.

Así que nombra exactamente **un** repositorio — el nombre que vas a usar en el Paso 0 del Doc 02 — y agrégalo al
sandbox. Reemplaza el bloque `"filesystem"` de la 3a por:

```json
"filesystem": {
  "denyRead": ["~/", "~/.claude/.credentials.json"],
  "allowRead": [".", "~/.claude", "~/dev/<repo-name>"],
  "allowWrite": ["~/dev/<repo-name>"]
}
```

Dos límites en vez de uno, pero ambos están nombrados, son auditables y siguen excluyendo el resto de la
máquina, incluido el resto de `~/dev`. Usa el mismo `<repo-name>` en todo lo que sigue: en el Doc 02 (Pasos 0,
6 y el router) y en el Doc 04. Si después eliges otro nombre, cambia esta entrada para que coincida — el
chequeo de estado reporta la Parte 3a `NOT DONE` cuando el sandbox nombra un repositorio distinto del que
nombra tu router, o más de uno.

La carpeta tiene que existir antes de que el sandbox pueda abrirla para escribir (en Linux y WSL2 una entrada
`allowWrite` para una ruta que no existe no tiene efecto), y los comandos confinados no pueden crearla, porque
no pueden escribir en `~/dev`. Así que en el Paso 6 del Doc 02 **tú** corres el bloque de creación en una
terminal normal (Parte 5), y después reinicias Claude Code en tu vault.

### 3d — Las instalaciones en `~/.claude` ocurren fuera del límite (a propósito)

Bajo este sandbox, Bash puede leer `~/.claude` pero **no puede escribir ahí**. Algunos pasos de la configuración escriben ahí con un comando de shell, y **van a fallar** en una sesión confinada:

| Paso | Por qué falla confinado |
|---|---|
| Doc 02 Paso 3.5 — `chmod +x` sobre los scripts de la statusline y de los *hooks* | modifica archivos en `~/.claude` |
| Doc 02 Paso 3.5 — las tres fusiones de ajustes (`aiac-merge-settings.py`) | escribe `~/.claude/settings.json`, que los comandos confinados nunca pueden escribir |
| Doc 03 Paso 2 y 2.7b — `claude plugin install …` | escribe en `~/.claude/plugins/` |
| Doc 03 Paso 2.7a — la instalación del paquete de *skills* | escribe en `~/.claude/skills/` |

Haz esos pasos desde una sesión de Claude Code arrancada **fuera del vault** — por ejemplo desde `~/dev` — donde la configuración de sandbox del vault no aplica. Es un paso corto y deliberado fuera del límite para instalaciones revisadas: lee cada comando antes de aprobarlo y después vuelve a tu sesión del vault. Las *skills* vienen de una versión pública y fija (`AI-Acceleration/cc-starter-pack` `v1.0.1`), así que puedes leer cada archivo antes de instalar.

---

## Parte 4 — Verifícalo tú mismo

No tomes la Parte 1 por fe. Estas son las pruebas que distinguen un límite real de un archivo de configuración que se ve tranquilizador. Ejecútalas **antes** de entregarle el Doc 02 a Claude.

**1. Confirma que el sandbox de verdad cargó.** En Claude Code, ejecuta `/sandbox` y abre la pestaña **Config**. Muestra los ajustes *resueltos* — lo que está realmente en efecto después de fusionar todos los ámbitos, no lo que escribiste. Confirma `enabled: true` y que tus reglas de sistema de archivos están ahí. Confirma que el panel no está mostrando una pestaña de Dependencies.

**2. Planta canarios fuera del vault — solo archivos sintéticos.** En una **terminal normal** (no a través de Claude), crea una carpeta nueva con un nombre único dentro de tu carpeta de usuario, con contenido falso. Nunca uses una llave real ni un secreto real para esta prueba:

```bash
CANARY_DIR="$(mktemp -d "$HOME/aiac-canary.XXXXXX")" &&
printf 'CANARY-SHOULD-NEVER-BE-READ\n' > "$CANARY_DIR/secret.txt" &&
printf 'SYNTHETIC-NOT-A-REAL-KEY\n' > "$CANARY_DIR/test.key" &&
ls -la "$CANARY_DIR" && echo "CANARY_DIR=$CANARY_DIR"
```

- La carpeta se crea **dentro de `$HOME` a propósito**: el sandbox deniega las lecturas bajo `~/`. Una carpeta en el directorio temporal del sistema quedaría fuera de esa regla y no probaría nada.
- `ls -la` tiene que listar `secret.txt` y `test.key`. **Confirma que los dos existen antes de probar nada** — un resultado "denegado" sobre un archivo que no está ahí no prueba nada.
- Deja esta terminal abierta: necesitas la ruta impresa `CANARY_DIR=…` más abajo (escrita `<CANARY_DIR>`) y para la limpieza.

**3. La prueba que importa.** Pídele a Claude, en la sesión del vault (reemplaza `<CANARY_DIR>` por la ruta impresa):

> Ejecuta este comando exacto y muéstrame la salida cruda, incluyendo cualquier error: `python3 -c "print(open('<CANARY_DIR>/secret.txt').read())"`

**Aquí se juega todo.** Tiene que fallar con un error de sistema de archivos/permisos del sistema operativo. Si imprime `CANARY-SHOULD-NEVER-BE-READ`, tu sandbox no está activo — para y arréglalo antes de continuar. Esta prueba está construida específicamente para saltarse las reglas de permisos (es un subproceso haciendo su propia E/S de archivos), así que **solo** un sandbox de kernel funcionando la detiene. Una configuración que pasa el paso 1 pero falla esta es exactamente el modo de falla que este documento existe para prevenir. (Que Claude pregunte antes depende del modo que elegiste en `/sandbox`: en modo auto-allow un comando confinado corre sin solicitud de permiso; en modo de permisos normales lo apruebas una vez. En cualquier caso, la lectura en sí tiene que fallar.)

**4. Prueba la capa de herramientas integradas.** Pídele a Claude:

> Lee el archivo <CANARY_DIR>/secret.txt

No debería leerlo en silencio — está fuera del vault, así que recibes una solicitud de permiso. Recházala. Después pídele:

> Lee el archivo <CANARY_DIR>/test.key

La regla de denegación `Read(~/**/*.key)` tiene que bloquear eso de plano, sin preguntar — la carpeta canario está dentro de tu carpeta de usuario, así que la regla anclada en `~/` la cubre. (Esto usa la llave sintética del paso 2 — nunca apuntes esta prueba a una llave real.)

**5. Prueba el límite de red.** Pídele a Claude:

> Ejecuta: `curl -sS -o /dev/null -w "%{http_code}" https://example.com`

No está en `allowedDomains`, así que debería quedar bloqueado o preguntarte — nunca tener éxito en silencio.

**6. Confirma el límite de escritura.** Pídele a Claude:

> Ejecuta: `touch <CANARY_DIR>/written-by-claude.txt`

Tiene que fallar. Las escrituras están confinadas al directorio de trabajo y al directorio temporal de la sesión.

**7. Limpia solo lo que creó la prueba.** De vuelta en la terminal normal del paso 2:

```bash
rm -f "$CANARY_DIR/secret.txt" "$CANARY_DIR/test.key" && rmdir "$CANARY_DIR"
```

Si `rmdir` se niega porque la carpeta no está vacía, algo más se escribió ahí — revísalo (`ls -la "$CANARY_DIR"`): un `written-by-claude.txt` significa que el paso 6 **no** se sostuvo.

Si alguna de las pruebas 3, 5 o 6 tiene éxito, el límite no es lo que crees. Dilo en voz alta en la sesión en vez de seguir — una configuración que en silencio no se aplicó es peor que ninguna configuración, porque estarías confiando en ella.

---

## Parte 4.5 — git bajo el sandbox (lee esto antes del día de la sesión)

**Espéralo, no es un error de configuración:** bajo el sandbox, **Claude no puede ejecutar `git` por ti.**
El *harness* protege por patrón los archivos de estado de `.git/` — `config`, `HEAD`, `refs` — porque los
*hooks* de git y `git config` son un vector de escape documentado (un *hook* no es más que un script que git
va a ejecutar por ti). Esto se verificó con pruebas aisladas en una máquina real durante una sesión en vivo.
Tener entradas de git en tu lista `allow` no lo cambia: el sandbox es un límite a nivel de kernel, y la lista de
permisos es otro sistema distinto que no puede anularlo.

**Qué hacer al respecto — y por qué la solución es mejor que lo que reemplaza:**

> **Claude crea y edita los archivos. Tú ejecutas git.**
>
> ```bash
> git add -A && git commit -m "..."     # you type this
> ```
>
> Esto salió de una sesión en vivo, y terminó siendo mejor pedagogía que el diseño original:
> **el commit se convierte en tu acto de aprobación.** Nada entra en tu historial sin que lo hayas visto
> y aprobado. Para un participante que pidió un sandbox en primer lugar, eso es justamente el punto,
> no un impuesto.

**Si la fricción supera al beneficio** (estás haciendo commits todo el tiempo y te rompe el flujo),
la válvula de escape es el ajuste `excludedCommands` del sandbox para `git`. Ten claro lo que hace: un
comando excluido corre **fuera del sandbox, con todo tu acceso** — sin límites de archivos ni filtro de red —
y solo quedan las solicitudes de permiso normales ([documentación del sandbox](https://code.claude.com/docs/en/sandboxing)).
Eso es un aflojamiento real del límite, así que el chequeo de estado reporta entonces la Parte 3a `NOT DONE`
— que sea una decisión deliberada de la Semana 1, no un reflejo del día de la sesión.

**Autenticación.** Usa `gh auth login --web` (en una terminal normal) o Git Credential Manager. No crees un
*personal access token* clásico para esto. Ten claro dónde queda la credencial: `gh` guarda su token en el
almacén de credenciales de tu sistema operativo (Llavero de macOS, Administrador de credenciales de Windows,
un llavero de Linux) **cuando hay uno disponible**, y si no, recurre a un archivo de texto plano,
`~/.config/gh/hosts.yml` — algo común en Linux y WSL2 sin llavero. `gh auth status` muestra cuál usó. En los
dos casos, el `denyRead: ["~/"]` del sandbox mantiene a los comandos confinados lejos de `~/.config/gh`, y la
regla `Read(~/.config/gh/**)` de la Parte 3b mantiene lejos a la herramienta Read de Claude. Git Credential
Manager usa el almacén de credenciales del sistema operativo.

---

## Parte 5 — Qué cambia en el Doc 02

Ejecuta el Doc 02 normalmente, con estas modificaciones:

| Paso del Doc 02 | Cambio |
|---|---|
| **Antes de empezar el Doc 02** | Haz `cd` a tu vault. Confírmalo con `pwd`. El directorio de trabajo *es* el límite — si lanzas Claude desde cualquier otro lado, el alcance de las herramientas integradas te sigue hasta allá y `.` resuelve a un lugar completamente distinto. |
| **PASO 3 — bloque de permisos** | **Ya está hecho en la Parte 3b** — las mismas listas `allow` y `ask` más la lista `deny`, fusionadas con el script. Dile a Claude que se salte la fusión del Paso 3: bajo el sandbox el script no puede escribir `~/.claude/settings.json` de todos modos (Claude Code siempre deniega las escrituras confinadas a ese archivo). |
| **PASO 3 — router global** | Ejecútalo normalmente. Nombra `~/dev/<repo-name>`, el mismo repositorio de la Parte 3c. |
| **PASO 3.5 — hooks** | Lee los dos comandos de *hook* y el script de la statusline antes de que se escriban — corren sin confinar. Las líneas `chmod +x` y las tres fusiones de ajustes fallan confinadas (escriben en `~/.claude`): ejecútalas desde una sesión fuera del vault (Parte 3d). `jq` tiene que estar instalado (prerrequisitos del Doc 01). |
| **PASO 6 — crear el repositorio** | Usa el nombre de repositorio de la Parte 3c. Claude te muestra el bloque de creación; **tú** lo corres en una terminal normal (los comandos confinados no pueden escribir en `~/dev` ni ejecutar git — Parte 4.5). Después reinicia Claude Code en tu vault, para que la entrada de la Parte 3c aplique a la carpeta nueva, y corre ahí también tú el comando de verificación. |
| **PASO 12 — primer push** | Bajo el sandbox Claude no puede ejecutar git (Parte 4.5). Claude te muestra la lista de archivos preparados y los comandos; tú revisas dueño, visibilidad **Private** y archivos, y ejecutas tú mismo `gh repo create … --private` y `git push` en una terminal normal. |
| **Si `gh` falla** | Probablemente sea el problema de Seatbelt/TLS con los CLI hechos en Go. Es esperable en modo estricto. Ejecuta `gh` tú mismo en una terminal normal; no crees un *personal access token* clásico. |
| **Doc 03 — plugins y *skills*** | Instálalos desde una sesión fuera del vault (Parte 3d). |

**Sobre "tú metes el contenido":** vale la pena ser preciso sobre qué significa eso y qué no. Copiar un archivo dentro de tu vault lo trae por completo adentro del límite — Claude lo lee, y también lo lee cualquier cosa que corra Bash. El límite es un *perímetro*, no una política por archivo: no existe "Claude puede ver este archivo pero no aquel" dentro del vault. Así que el vault es tu compuerta de revisión. Si algo no debería verse, no va en la carpeta. Ese es todo el modelo, y es un buen modelo *porque* es lo bastante simple como para tenerlo entero en la cabeza.

---

## Parte 6 — Si esto no es suficientemente fuerte

Todo lo de arriba es honesto en cuanto a ser dos mecanismos en vez de uno, y en cuanto a que las herramientas de archivos integradas se aplican a nivel de aplicación y no de kernel. Si esa brecha te importa, el sandbox integrado es la herramienta equivocada y lo que quieres es un límite alrededor de **todo el proceso de Claude Code**:

- **Dev container / contenedor** — Claude Code corre adentro; el contenedor es el límite; toda herramienta, incluidas Read/Edit/Write, queda confinada por él. Ver la documentación oficial de `devcontainer`.
- **Máquina virtual** — la más fuerte, la más pesada.
- **`@anthropic-ai/sandbox-runtime`** — las mismas primitivas del sistema operativo como paquete independiente, usado para envolver el proceso completo.

Para la Fase 0 específicamente, la configuración de la Parte 3 es la proporción correcta: cierra el hueco real (subprocesos arbitrarios leyendo todo tu disco), es verificable en cinco minutos con la Parte 4, y no convierte un onboarding de 90 minutos en un proyecto de infraestructura. Vale la pena saber que la escalera existe, eso sí, y en qué peldaño estás.

---

## Fuentes

Cada ajuste de arriba viene de la documentación oficial de Claude Code (consultada por primera vez el 2026-07-15). Las citas se volvieron a verificar contra las páginas vigentes el 2026-11-25 y llevan esa fecha; las páginas cambian, así que verifícalas de nuevo antes de apoyarte en una cita:

- `https://code.claude.com/docs/en/sandboxing.md` — alcance del sandbox, configuración de sistema de archivos/red, plataformas soportadas, limitaciones
- `https://code.claude.com/docs/en/permissions.md` — precedencia de reglas, patrones de rutas, la salvedad de los subprocesos, el valor por defecto del directorio de trabajo
- `https://code.claude.com/docs/en/settings.md` — referencia completa de ajustes

Donde la documentación no afirma algo (el confinamiento de los *hooks*), este documento lo dice en vez de adivinar.
