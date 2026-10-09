---
title: "Configuración de Sandbox (Participante) — AI Acceleration Club Fase 0"
created: 2026-07-15
category: reference
status: draft
tags: [aiac, phase0, co-facilitator-kit, participant, sandbox, security]
lang: es
translated_from: "02-S — Sandbox Setup (Participant, opt-in).md"
---

**Apoya:** Ejecuta esto ANTES del Doc 02. Reemplaza el bloque de permisos del PASO 3 del Doc 02.

# Configuración de Sandbox — Confinar Claude Code a tu vault

Este documento es para un participante que quiere un límite **verificable** alrededor de Claude Code, no la promesa de uno. Está escrito para alguien técnico. No simplifica, y no sobrevende.

Lee la Parte 1 antes de ejecutar nada. Te dice qué estás obteniendo de verdad — incluyendo lo que **no** estás obteniendo. Si las garantías de la Parte 1 no te resultan suficientes, la Parte 6 te dice qué hacer en su lugar.

---

## Parte 1 — Qué garantiza esto de verdad

Primero la afirmación honesta, porque la versión de marketing de esto es falsa.

**Claude Code no corre "dentro de un sandbox".** No hay un único límite alrededor del proceso. Hay dos mecanismos de aplicación distintos que cubren dos conjuntos distintos de herramientas, y tienen fortalezas muy diferentes:

| Qué se ejecuta | Aplicado por | Fortaleza |
|---|---|---|
| **Comandos de Bash y cada proceso hijo que lanzan** (incluyendo `python`, `node`, `git`, cualquier script) | El kernel del sistema operativo — Seatbelt en macOS, bubblewrap en Linux/WSL2 | **Duro.** Se aplica sobre el proceso en ejecución. Se sostiene sin importar qué decidió ejecutar el modelo, e incluso si un comando permitido hace más de lo que su nombre sugiere. |
| **Las herramientas de archivos integradas de Claude** — Read, Edit, Write, Glob, Grep | El sistema de permisos de Claude Code, en proceso, evaluado *antes* de que la herramienta corra | **A nivel de aplicación.** Las reglas de denegación son absolutas (gana la primera coincidencia, sin excepciones posibles), pero esto es Claude Code aplicándose reglas a sí mismo, no el kernel aplicándoselas a un proceso. |

De la documentación oficial, textualmente:

> "Sandboxing provides OS-level enforcement that restricts what Bash commands can access at the filesystem and network level. **It applies only to Bash commands and their child processes.**"

y

> "**Built-in file tools**: Read, Edit, and Write use the permission system directly rather than running through the sandbox."

Así que la frase precisa es: **todo lo que Claude puede ejecutar queda confinado por el kernel a tu vault; todo lo que Claude lee o escribe directamente queda confinado a tu vault por reglas de permisos que él evalúa antes de actuar.** Ambas capas se configuran abajo. Ninguna es decorativa.

### Por qué la capa de Bash es la que importa

Esta es la parte que vale la pena entender, porque es la razón por la que la configuración estándar de AIAC no te alcanza.

Reglas de permisos como `Read(~/.ssh/**)` en una lista de denegación funcionan sobre las herramientas de archivos propias de Claude y sobre los comandos de archivos que Claude Code reconoce en Bash (`cat`, `head`, `tail`, `sed`). **No** funcionan sobre subprocesos arbitrarios. La documentación, textualmente:

> "They don't apply to arbitrary subprocesses that read or write files indirectly, like a Python or Node script that opens files itself. For OS-level enforcement that blocks all processes from accessing a path, enable the sandbox."

La configuración estándar de Fase 0 pre-aprueba `Bash(python3 *)` y tiene una **lista de denegación vacía**. Esa combinación significa que un script de Python de una línea lee cualquier cosa en la máquina, y ninguna regla de permisos puede detenerlo. Cualquier lista de denegación que le pongas encima es teatro. El sandbox es lo que cierra ese hueco — y lo cierra en el kernel, que es por lo que se sostiene incluso si el modelo está confundido, equivocado o manipulado por algo que leyó.

### Contra qué NO protege esto

Dicho sin rodeos para que decidas tú:

- **La capa de red no inspecciona TLS.** El proxy integrado permite o bloquea según el nombre de host que el cliente declara. La documentación advierte que las listas de permisos amplias "can create paths for data exfiltration" vía *domain fronting*. Nuestra configuración permite un conjunto estrecho.
- **Los *hooks*.** La documentación del sandbox enumera qué queda fuera del sandbox (herramientas de archivos integradas, uso de computadora, variables de entorno, subagentes) y **no menciona los *hooks* ni en un sentido ni en el otro**. No voy a adivinar. Trata los *hooks* como no confinados. Importan aquí porque el Paso 3.5 del Doc 02 instala dos — son comandos de shell que *tú* instalas y puedes leer completos antes de que corran siquiera, así que están dentro de tu límite de confianza por inspección, no por aplicación.
- **Los servidores MCP**, si agregas alguno después (Fase 3). Las reglas de permisos aplican sobre ellos; el sandbox no.
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

Dos archivos. Crea ambos **antes** de pegar el Doc 02 en Claude Code, a mano, para que Claude quede confinado desde su primerísima llamada a una herramienta y no después de haber construido medio vault.

### 3a — Ajustes del proyecto: `<YOUR_VAULT>/.claude/settings.json`

**Este archivo debe vivir en tu vault**, no en `~/.claude/`. Eso sostiene el diseño, no es estético. La ruta `.` resuelve a la raíz del proyecto **solo** cuando la configuración vive en los ajustes del proyecto. La documentación, textualmente:

> "The `.` in `allowRead` resolves to the project root because this configuration lives in project settings. If you placed the same configuration in `~/.claude/settings.json`, `.` would resolve to `~/.claude` instead, and project files would remain blocked by the `denyRead` rule."

```json
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false,
    "filesystem": {
      "denyRead": ["~/"],
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
- **`allowRead` incluye `~/.claude`** — **esta línea es obligatoria, y se descubrió a las malas.** Con `denyRead: ["~/"]` + `allowRead: ["."]` solos, `~/.claude/` queda bloqueado — y **el Doc 03 vive ahí**. Fallan aproximadamente **12 comandos**: las instalaciones con `curl -o ~/.claude/skills/...`, cinco verificaciones con `head`, la prueba del router, el `ls` de los plugins. Sin esta entrada el sandbox parece funcionar justo hasta el Bloque 3, y ahí rompe toda la instalación de *skills*. Verificado como seguro: Claude Code **auto-deniega las escrituras a `settings.json` en todos los ámbitos**, así que un comando confinado sigue sin poder reescribir su propia política aun con este permiso de lectura.
- **`allowWrite: []`** — las escrituras ya van por defecto al directorio de trabajo + el directorio temporal de la sesión. Vacío significa que no agregamos nada a eso.
- **`failIfUnavailable: true`** — **este es el ajuste del que de verdad depende tu solicitud.** Por defecto, si el sandbox no puede arrancar (dependencia faltante, plataforma no soportada), Claude Code *imprime una advertencia y corre tus comandos sin confinar de todas formas*. Eso es una degradación silenciosa de "confinado" a "no confinado". Esto lo convierte en una falla dura. Sin esta línea, nada de lo anterior es una garantía.
- **`allowUnsandboxedCommands: false`** — el interruptor de "modo sandbox estricto". Por defecto, cuando un comando falla por una restricción del sandbox, Claude puede reintentarlo con `dangerouslyDisableSandbox`, lo que lo corre fuera del límite (sujeto a una solicitud de permiso). Esto hace que ese parámetro sea **completamente ignorado**. Fíjate en el intercambio: algunas herramientas genuinamente no funcionan confinadas (`docker`, `watchman`/`jest`, y los CLI hechos en Go como `gh` pueden fallar la verificación TLS bajo Seatbelt en macOS). Con esto apagado, fallan en vez de escapar. Ese es el trato que estás pidiendo. Si `gh` se rompe, usa HTTPS + un PAT — la Fase 0 ya trata a `gh` como opcional y con alternativas.
- **`network.allowedDomains`** — no hay dominios pre-permitidos por defecto; el primer intento hacia un dominio nuevo te pregunta. Esta lista pre-aprueba solo lo que la Fase 0 necesita (GitHub, npm, PyPI) para que no termines aprobando por fatiga de clics algo que no leíste. Todo lo demás sigue preguntando. Mantenla estrecha — una entrada amplia aquí es la vía de exfiltración de la que advierte la documentación.

Dos cosas que obtienes gratis y vale la pena saber: el sandbox **auto-deniega las escrituras al propio `settings.json` de Claude Code en todos los ámbitos**, así que un comando confinado no puede reescribir su propia política. Y **los subagentes heredan la configuración de sandbox de la sesión padre** — corren en el mismo proceso, así que no hay bypass ahí.

> **`sandbox.credentials` (opcional, necesita Claude Code v2.1.187+).** Verifica con `claude --version`. Este bloque deniega explícitamente los archivos de credenciales y desactiva las variables de entorno secretas para los comandos confinados. Nuestro `denyRead: ["~/"]` ya cubre los archivos bajo `$HOME`, y esto agrega la mitad de las variables de entorno:
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

Esto cubre las herramientas de archivos integradas, que el sandbox no cubre. **Esto reemplaza el bloque de permisos del PASO 3 del Doc 02 — no apliques también aquel.**

> **Nota (2026-08-19):** desde entonces el PASO 3 del Doc 02 se endureció con la misma lista `allow` que
> ves abajo, así que ya no se contradicen en esa mitad. Lo que este bloque sigue agregando encima es la
> **lista `deny` dirigida** (las rutas joya de la corona) — esa parte es exclusiva de la variante con sandbox.

```json
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(ls *)",
      "Bash(mkdir *)",
      "Bash(cat *)",
      "Bash(head *)",
      "Bash(wc *)",
      "Glob",
      "Grep"
    ],
    "deny": [
      "Read(~/.ssh/**)",
      "Read(~/.aws/**)",
      "Read(~/.gnupg/**)",
      "Read(~/.config/gh/**)",
      "Read(~/Library/Keychains/**)",
      "Read(**/.env)",
      "Read(**/*.pem)",
      "Read(**/*.key)"
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

Qué cambió respecto a la configuración estándar de Fase 0, y por qué cada cambio es deliberado:

- **`Bash(python3 *)` y `Bash(pip install *)` eliminados de `allow`.** Esta es la edición más importante de todas. Pre-aprobar Python significa pre-aprobar "leer o escribir cualquier archivo, sin restricción de ninguna regla de permisos". Con el sandbox activo, Python queda confinado por el kernel a tu vault de todos modos — pero no hay razón para *además* entregarle una pre-aprobación en blanco, y si el sandbox alguna vez falla al cargar, tú quieres la solicitud de permiso. (`failIfUnavailable: true` debería hacer eso imposible. Cinturón y tirantes.)
- **`Read`, `Write`, `Edit` a secas eliminados de `allow`.** Un nombre de herramienta a secas en `allow` pre-aprueba esa herramienta para **cualquier** entrada — incluyendo rutas fuera de tu vault. Quitarlos restaura el comportamiento real por defecto: *"By default, Claude has access to files in the directory where you launched it."* Lanza desde el vault, y el vault es el alcance. Este es un caso donde borrar tres líneas compra más que agregar diez.
- **Entradas `deny` dirigidas, no una amplia.** Fíjate en lo que está **ausente** a propósito: no hay `Read(~/Documents/**)` ni `Read(//**)`. Tu vault vive bajo `~/Documents`, y las reglas de denegación de permisos tienen precedencia sobre las de permiso **sin ninguna excepción posible** — una denegación amplia como esa dejaría a Claude fuera, en silencio, del mismísimo vault que estás tratando de darle. Estas entradas son estrechas a propósito. El límite amplio es tarea del sandbox; esta lista es para las joyas de la corona de las herramientas integradas.
- **El *hook* de sonido es solo para macOS.** En Windows Git Bash/WSL usa `powershell.exe -c "[console]::beep(1000,400)"`; en Linux `paplay /usr/share/sounds/freedesktop/stereo/bell.oga`. Si no estás seguro, borra el bloque `"Stop"` completo — es una comodidad, y un comando equivocado aquí falla en cada turno.

**Revisa también `additionalDirectories`.** Si esa clave existe en cualquier archivo de ajustes, lo que liste se suma al alcance de las herramientas integradas de Claude. Debería estar ausente o vacía. Lo mismo para el flag `--add-dir` y el comando `/add-dir` — no los uses.

### 3c — Dónde va el repositorio de código (decídelo antes del Paso 6)

La Fase 0, tal como está diseñada, pone tu repositorio git en **`~/dev/<repo-name>`, fuera del vault**, con el razonamiento de que un `.git` anidado pelea con la sincronización de Obsidian. Eso choca con un límite solo-vault: con `allowRead: ["."]`, Bash no puede ver `~/dev` en absoluto, y `git` no va a funcionar ahí.

Escoge una antes de la sesión:

- **(A) Repositorio dentro del vault** — por ejemplo `<vault>/dev/<repo-name>/`. Un solo límite, nada que ampliar, la configuración de arriba funciona sin cambios. Costo: deberías agregar `dev/` a *Settings → Files and links → Excluded files* de Obsidian para que quede fuera de la búsqueda y la sincronización.
- **(B) Repositorio en `~/dev`, nombrado explícitamente** — conserva la disposición de la Fase 0 y agrega exactamente una ruta al sandbox:
  ```json
  "filesystem": {
    "denyRead": ["~/"],
    "allowRead": [".", "~/dev/<repo-name>"],
    "allowWrite": ["~/dev/<repo-name>"]
  }
  ```
  Dos límites en vez de uno, pero ambos están nombrados, son auditables y siguen excluyendo el resto de la máquina.

Cualquiera de las dos satisface "no toda mi computadora". **(A) es la lectura más estricta de tu solicitud y la que yo tomaría por defecto**; (B) preserva la disposición del kit. Tú decides — dile al facilitador cuál, al inicio de la sesión.

---

## Parte 4 — Verifícalo tú mismo

No tomes la Parte 1 por fe. Estas son las pruebas que distinguen un límite real de un archivo de configuración que se ve tranquilizador. Ejecútalas **antes** de pegar el Doc 02.

**1. Confirma que el sandbox de verdad cargó.** En Claude Code, ejecuta `/sandbox` y abre la pestaña **Config**. Muestra los ajustes *resueltos* — lo que está realmente en efecto después de fusionar todos los ámbitos, no lo que escribiste. Confirma `enabled: true` y que tus reglas de sistema de archivos están ahí. Confirma que el panel no está mostrando una pestaña de Dependencies.

**2. Planta un canario fuera del vault.** En una terminal normal, no a través de Claude:

```bash
mkdir -p ~/canary && echo "CANARY-SHOULD-NEVER-BE-READ" > ~/canary/secret.txt
```

**3. La prueba que importa.** Pídele a Claude, en la sesión del vault:

> Ejecuta este comando exacto y muéstrame la salida cruda, incluyendo cualquier error: `python3 -c "print(open('/Users/YOURNAME/canary/secret.txt').read())"`

**Aquí se juega todo.** Tiene que fallar con un error de sistema de archivos/permisos del sistema operativo. Si imprime `CANARY-SHOULD-NEVER-BE-READ`, tu sandbox no está activo — para y arréglalo antes de continuar. Esta prueba está construida específicamente para saltarse las reglas de permisos (es un subproceso haciendo su propia E/S de archivos), así que **solo** un sandbox de kernel funcionando la detiene. Una configuración que pasa el paso 1 pero falla esta es exactamente el modo de falla que este documento existe para prevenir.

**4. Prueba la capa de herramientas integradas.** Pídele a Claude:

> Lee el archivo ~/canary/secret.txt

No debería leerlo en silencio. Después pídele que lea `~/.ssh/id_rsa` (exista o no) — la regla de denegación debería bloquear eso de plano.

**5. Prueba el límite de red.** Pídele a Claude:

> Ejecuta: `curl -sS -o /dev/null -w "%{http_code}" https://example.com`

No está en `allowedDomains`, así que debería quedar bloqueado o preguntarte — nunca tener éxito en silencio.

**6. Confirma el límite de escritura.** Pídele a Claude:

> Ejecuta: `touch ~/canary/written-by-claude.txt`

Tiene que fallar. Las escrituras están confinadas al directorio de trabajo y al directorio temporal de la sesión.

**7. Limpia.** `rm -rf ~/canary`

Si alguna de las pruebas 3, 5 o 6 tiene éxito, el límite no es lo que crees. Dilo en voz alta en la sesión en vez de seguir — una configuración que en silencio no se aplicó es peor que ninguna configuración, porque estarías confiando en ella.

---

## Parte 4.5 — git bajo el sandbox (lee esto antes del día de la sesión)

**Espéralo, no es un error de configuración:** bajo el sandbox, **Claude no puede ejecutar `git` por ti.**
El *harness* protege por patrón los archivos de estado de `.git/` — `config`, `HEAD`, `refs` — porque los
*hooks* de git y `git config` son un vector de escape documentado (un *hook* no es más que un script que git
va a ejecutar por ti). Esto se verificó con pruebas aisladas en una máquina real durante una sesión en vivo.
Tener `Bash(git *)` en tu lista `allow` no lo cambia: el sandbox es un límite a nivel de kernel, y la lista de
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
la válvula de escape es el ajuste **Excluded Commands** del sandbox para `git`, que devuelve a git a
solicitudes de permiso normales en vez de un bloqueo duro. Eso es un aflojamiento real del límite — que sea
una decisión deliberada de la Semana 1, no un reflejo del día de la sesión.

**Una nota honesta sobre la vía del PAT.** Si te autenticas con un Personal Access Token, termina en
texto plano bajo `~/.claude`. Eso es cierto con o sin sandbox; vale la pena saberlo, y la decisión es
tuya. Si te incomoda, usa Git Credential Manager, que lo guarda en el llavero del sistema operativo.

---

## Parte 5 — Qué cambia en el Doc 02

Ejecuta el Doc 02 normalmente, con estas modificaciones:

| Paso del Doc 02 | Cambio |
|---|---|
| **Antes de pegar** | Haz `cd` a tu vault. Confírmalo con `pwd`. El directorio de trabajo *es* el límite — si lanzas Claude desde cualquier otro lado, el alcance de las herramientas integradas te sigue hasta allá y `.` resuelve a un lugar completamente distinto. |
| **PASO 3 — bloque de permisos** | **Sáltatelo.** Ya está hecho en la Parte 3b, deliberadamente distinto. No dejes que Claude lo sobrescriba. |
| **PASO 3 — router global** | Ejecútalo normalmente. Si escogiste la opción (A) en la Parte 3c, dile a Claude que cambie la regla 3 del router para que apunte a `<vault>/dev/` en vez de `~/dev/`. |
| **PASO 3.5 — hooks** | Ejecútalo normalmente, pero lee ambos comandos de *hook* antes de que se escriban. Son la parte de la configuración que no está restringida por el sandbox. `jq` tiene que estar instalado (Doc 01 Paso 5.5). |
| **PASO 6 — crear el repositorio** | Usa la ubicación que hayas escogido en la Parte 3c. |
| **Si `gh` falla** | Probablemente sea el problema de Seatbelt/TLS con los CLI hechos en Go. Es esperable en modo estricto. Usa HTTPS + un PAT — la Fase 0 trata a `gh` como opcional y con alternativas documentadas. |

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

Cada cita y cada ajuste de arriba vienen de la documentación oficial de Claude Code, consultada el 2026-07-15:

- `https://code.claude.com/docs/en/sandboxing.md` — alcance del sandbox, configuración de sistema de archivos/red, plataformas soportadas, limitaciones
- `https://code.claude.com/docs/en/permissions.md` — precedencia de reglas, patrones de rutas, la salvedad de los subprocesos, el valor por defecto del directorio de trabajo
- `https://code.claude.com/docs/en/settings.md` — referencia completa de ajustes

Donde la documentación no afirma algo (el confinamiento de los *hooks*), este documento lo dice en vez de adivinar.
