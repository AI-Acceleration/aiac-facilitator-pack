# Vocabulario

**Para:** participantes, antes de la sesión de Fase 0. Léelo una vez, más o menos un día antes. Toma cinco minutos.

> **Por qué:** en la sesión vamos rápido y vas a oír varias palabras técnicas. Si ya las conoces, todo fluye. No tienes que memorizar nada. Léelas una vez, y lo que todavía no te quede claro lo vemos en vivo.

---

## El mapa primero: cómo encajan las 3 piezas

Antes de los términos sueltos, aquí va la foto completa. Todo lo que vamos a usar se reduce a **3 piezas**, y cada una tiene **un** trabajo. Casi toda la confusión al arrancar no viene de no saber qué significa una palabra. Viene de no ver cómo se conectan las herramientas. Con esta imagen clara, el resto de las palabras cae solo.

```
  +------------------+    +------------------+    +------------------+
  |   CLAUDE CODE    |    |  OBSIDIAN/VAULT  |    |   GIT + GITHUB   |
  |  el que ACTÚA    |    |  donde VIVE tu   |    |  HISTORIAL +     |
  |                  |    |  conocimiento    |    |  RESPALDO        |
  +------------------+    +------------------+    +------------------+
  | La IA en tu      |    | Tus notas,       |    | Guarda cada      |
  | terminal: lee,   |    | proyectos y      |    | versión de tu    |
  | escribe y        |    | briefs. La       |    | código (en       |
  | ejecuta sobre    |    | fuente de la     |    | ~/dev) y lo      |
  | tus archivos.    |    | verdad.          |    | respalda.        |
  +------------------+    +------------------+    +------------------+
     trabajas CON    ->   ...guarda lo que   ->   ...y el CÓDIGO va
     Claude Code...       sabes en el vault       en ~/dev, con Git
```

**En una frase:** trabajas **con** Claude Code. Lo que sabes y decides vive en tu **vault** (Obsidian). El **código** vive aparte, en `~/dev/`, donde **Git** le guarda el historial y **GitHub** lo respalda en la nube. Claude *actúa*, el vault *guarda el conocimiento*, y Git y GitHub son la *red de seguridad* del código.

**Dos lugares, una regla:** si una carpeta tiene su propio `.git/`, es un repo y va en `~/dev/`. El repo de tu primer proyecto va a vivir en `~/dev/<tu-proyecto>`, fuera del vault, con un enlace desde el brief de tu proyecto.

---

## Glosario: los términos principales, uno por uno

### Trabajar con Claude

| Término | Qué es, en una línea |
|---|---|
| **Claude Code** | Claude corriendo en tu terminal, con acceso a tus archivos: lee, escribe, ejecuta comandos y construye cosas, no solo conversa. |
| **Prompt** | Lo que le dices a Claude: una pregunta, una instrucción o todo un documento de instrucciones. En este kit, los prompts largos **se cargan por archivo**: guardas el documento y le dices a Claude «Lee el archivo <ruta> y sigue sus instrucciones». |
| **Harness** (entorno) | El programa que corre el modelo de IA y le da herramientas (leer archivos, ejecutar comandos). Claude Code es un *harness*. El método de este kit son archivos simples, así que también sirve con otros; Claude Code es simplemente el que recomendamos hoy. |
| **Comando con barra** | Lo que escribes dentro de Claude Code con `/` al principio para correr una *skill* o una acción incorporada, como `/session-close` o `/context`. |
| **Modo plan** | Un modo en el que Claude primero te propone un plan y espera tu OK antes de tocar nada. Cambias de modo con **Shift+Tab**. Úsalo para cualquier tarea que no sea trivial. |
| **Ventana de contexto** | La «memoria de trabajo» de Claude en una sesión. Es limitada: cuando se llena, toca guardar y empezar de nuevo. Una barra abajo te muestra el porcentaje. |
| **Límite de uso** | Cuánto de tu plan de Claude has usado, medido en una ventana móvil de 5 horas y por semana. Es distinto de la ventana de contexto. Ver el Doc 06. |

### Tu sistema de conocimiento

| Término | Qué es, en una línea |
|---|---|
| **Vault** | Tu carpeta de Obsidian, tu «segundo cerebro»: notas, proyectos, conocimiento. Es la fuente de la verdad de lo que sabes y de lo que estás haciendo. |
| **Obsidian** | La aplicación gratuita con la que lees y navegas tu vault. Las notas son archivos de texto simple, así que siguen siendo tuyas. |
| **PARA** | Cómo se organiza el vault: ***P**rojects* (proyectos, con fecha de cierre), ***A**reas* (responsabilidades continuas), ***R**eference* (material de referencia), ***A**rchives* (archivo: lo terminado o inactivo). |
| **GTD** | *Getting Things Done*: un método para capturar todo en un solo lugar (tu **INBOX**) y luego decidir qué es cada cosa y cuál es la próxima acción. |
| **Brief** | La nota de un proyecto en tu vault: qué quieres lograr, las próximas acciones, lo que esperas de otros y la bitácora. Claude lo lee primero cada vez que retomas ese proyecto. |
| **CLAUDE.md** | El archivo de **instrucciones** que Claude lee solo al arrancar: quién eres, cómo trabajas y las reglas del proyecto. Cada corrección que le haces se guarda aquí, y así mejora con el tiempo. |
| **Router** (enrutador) | El CLAUDE.md de tu carpeta personal (`~/.claude/CLAUDE.md`). Lleva cada sesión nueva a las reglas de tu vault, sin importar desde qué carpeta arranques, para que «trabajemos en mi proyecto» funcione sin más. |

### Ampliar a Claude

| Término | Qué es, en una línea |
|---|---|
| **Skill** / **SKILL.md** | Un procedimiento empaquetado que Claude sigue paso a paso (por ejemplo, cerrar bien una sesión). Su archivo es el `SKILL.md`. CLAUDE.md = reglas; SKILL.md = un procedimiento. |
| **Plugin** | Un paquete de *skills* (y a veces otras herramientas) que instalas de una sola vez. Para ver qué tienes instalado, pídele a Claude que corra `claude plugin list`. |
| **Conector** / **MCP** | El «enchufe» estándar que conecta a Claude con servicios externos, como el correo, el calendario o un grabador de reuniones, para que pueda usarlos. MCP (*Model Context Protocol*) es el nombre técnico. |

### Terminal y código

| Término | Qué es, en una línea |
|---|---|
| **Terminal** (o consola) | La ventana donde escribes comandos en texto, en vez de hacer clic. En Mac, «Terminal»; en Windows, Git Bash o PowerShell. |
| **Shell** | El programa que interpreta lo que escribes en la terminal (bash, zsh y PowerShell son shells). «Terminal» y «shell» se usan casi como sinónimos. |
| **CLI** | *Command-Line Interface*: una herramienta que se usa escribiendo comandos en la terminal. Claude Code es una CLI, y `gh` también. |
| **PATH** | La lista de carpetas donde la terminal busca los programas. Si una herramienta recién instalada da «command not found», casi siempre su carpeta todavía no está en el PATH: cierra y vuelve a abrir la terminal, o sigue el paso de PATH del instalador. |
| **`jq`** | Una herramienta pequeña de terminal para leer archivos JSON. La barra de contexto de tu statusline la usa. Viene incluida en macOS reciente; en Windows y Linux la instalas una vez. |
| **Repo** (repositorio) | Una carpeta de **código** con historial de Git. Vive en `~/dev/`, **fuera** del vault; el brief del proyecto, en el vault, apunta a él. Vault = conocimiento; repo = código. |
| **Git** | El sistema que guarda el historial de cambios de tu código: un «deshacer» infinito. |
| **GitHub** | El servicio en la nube donde se respaldan y se comparten los repos de Git. Tus repos ahí son **privados** (*Private*) salvo que tú decidas otra cosa. |
| **`gh`** | El programa de GitHub para la terminal. Con él Claude crea tu repo en GitHub. |
| **commit** | Guardar una «foto» de tus cambios en el historial de Git, con un mensaje que dice qué cambiaste. |
| **push** | Subir tus commits a GitHub. **pull** es lo contrario: bajar a tu computadora los cambios de la nube. |
| **branch** (rama) / **PR** | Una *branch* es una línea de trabajo paralela, y un *PR* (*pull request*) propone juntar esa rama con la principal. En la Fase 0 casi no los tocamos; están aquí para que las palabras no te suenen raras. |

> Esos son los términos principales, no todas las palabras que vas a encontrar. Si alguno no te quedó claro, no importa: lo vemos en vivo.
