# Plan del piloto — Videos tutoriales generados por un agente

> **Fecha:** 7 de octubre de 2026. **Estado:** **en pausa tras el video 1.1, con la factibilidad demostrada** (decisión del usuario del 7-oct-2026: puede haber ajustes en el manejo de permisos y roles). Voz elegida: Azure `es-CO-GonzaloNeural`. Ver §7.
> **Herramientas:** `Frontend/wms/tools/video-tutoriales/` (README con el uso).
> **Objetivo:** comprobar con 3 videos si un agente puede producir los 81 videos de `guiones-video-tutoriales.md`, con qué calidad y con cuánto esfuerzo, y comparar la voz del usuario con una voz sintética.

## 1. Qué se va a probar

| Video | Por qué entra en el piloto | Rol |
|---|---|---|
| 1.1 Cómo crear un usuario y asignarle roles | Formulario simple, validaciones, mensajes y navegación por menú. Es la base del grabador. | Administrador |
| 5.2 Solo báscula de principio a fin | La pantalla más densa: cola, ficha en pasos, teclado (Enter), tarjeta «Camión y conductor», cobro y tiquete en PDF. | Operario báscula |
| 7.3 Confirmar el depósito y cerrar el ingreso de camiones | Diálogos de confirmación, ayudas emergentes (*hover*), etiquetas de estado y avisos. Necesita un depósito preparado. | Comercio exterior |

Cada video sale en **dos versiones**: (A) con la voz del usuario y (B) con voz sintética. Son 6 videos en total.

**Criterio de éxito del piloto:**

| Criterio | Meta |
|---|---|
| Fidelidad | Cada paso de la tabla del guion se ve en pantalla, con su texto exacto y su resultado. |
| Sincronía | La narración de cada paso empieza cuando empieza su acción (desfase < 0,5 s). |
| Duración | Dentro del rango del guion (1.1: 3 min; 5.2: 4 min; 7.3: 3 min), con un margen de ±30 s. |
| Calidad visual | 1080p, cursor visible, campo o mensaje resaltado en cada paso, sin pantallas de carga largas ni datos reales. |
| Repetibilidad | Volver a generar un video desde cero (base recreada) sin tocar nada a mano. |
| Esfuerzo marginal | El tercer video toma claramente menos trabajo que el primero. Se mide para estimar los 81. |
| Calidad de la voz | El usuario elige entre la versión A y la B (o decide que la B sirve solo para borradores). |

## 2. Cómo funciona

```
guiones-video-tutoriales.md ──► narración por paso ──► audio por paso (usuario o TTS)
                                                              │ duración de cada paso
ambiente local + siembra ──► script Playwright del video ──► grabación .webm + marcas de tiempo por paso
                                                              │
                                     ffmpeg: video + audio + portada/cierre + subtítulos ──► .mp4 1080p
```

**Regla clave: primero el audio y después el video.**
1. Se genera o graba el audio de cada paso.
2. Se mide su duración.
3. El script hace la acción del paso y espera lo que dure su audio (más un margen de 0,6 s).
4. El montaje pone cada audio en la marca de tiempo donde empezó su paso.

Así no hay que sincronizar a mano, y si el audio cambia, se vuelve a grabar el video solo.

### 2.1 Ambiente y datos del piloto

- **Base:** `wms_grabacion`, una base **nueva** en el contenedor local `wms-postgres-db` (puerto 5433), migrada con el build actual de `develop`. No se toca la base de QA ni staging.
- **API y frontend** en `localhost:5281` y `localhost:3000`, como en `dataset-grabacion.md` §1.
- **Siembra del piloto:** un script que llama al API como Admin y crea solo lo que piden los tres videos (subconjunto de `dataset-grabacion.md`):

| Video | Datos previos |
|---|---|
| 1.1 | Cuenta C1 `video.admin`. |
| 5.2 | Cuenta C3; T1 y T4; precio e IVA de BASCULA (S1); ingreso de VID102 con motivo «Solo Bascula». |
| 7.3 | Cuenta C5; T1 (cliente e importador) y T3; P1 y P3; el depósito `DEMO-CP-0001` con los camiones VID101 y VID105, la recepción de Bodega y todos los requisitos para confirmar (es el estado al final de 7.2); la tarifa S4 o el acuerdo A1, para que la confirmación genere su factura. |

- **El depósito de 7.3** se prepara por API, recorriendo los mismos pasos del negocio: ingreso, registro en báscula, cobro, pesos, llegada y recepción en Bodega, y datos de CE.
  - Su valor se pone en **COP**, para no depender de la DIAN durante el piloto. La TRM se prueba aparte, en el video 3.9.
- **Recrear la base y sembrar de nuevo** toma un solo comando. Así se cumple el criterio de repetibilidad.

### 2.2 Grabador (Node + Playwright)

- **Navegador:** el Chromium de Playwright, ya descargado en la máquina. Ventana de 1920 × 1080, escala 1 y video del contexto a 1080p.
- **Funciones comunes para todos los videos:**
  - `iniciarSesion(rol)`: se hace **fuera de cámara** y la grabación empieza con la pantalla ya cargada. En 0.2 y 0.3 sí se graba el ingreso.
  - **Cursor visible:** Playwright no dibuja el mouse. Se inyecta un cursor que se desplaza con suavidad hasta cada elemento antes del clic.
  - `resaltar(elemento)` y `acercar(zona)`: un contorno de color y un zoom suave, con CSS, sobre el campo o el mensaje del paso.
  - `escribir(texto)` a velocidad humana y `pulsar(tecla)` (Enter, Tab, F2, Esc).
  - `paso(n, accion)`: registra la marca de tiempo del paso n, hace la acción y espera la duración de su audio.
  - `verificar(texto)`: confirma que el texto del guion apareció en pantalla. Si no aparece, el video **falla** en vez de salir mal, y el texto real se anota para corregir el guion.
- **Lo que no se graba:** el código del script maneja los elementos por su texto o su rol accesible (`getByRole`, `getByText`), el mismo texto exacto del guion. No se cambia el código de la aplicación.
- **Salida:** `salida/<video>/video.webm` y `pasos.json`, con el inicio y el fin de cada paso.

### 2.3 Voz

| | Versión A: voz del usuario | Versión B: voz sintética |
|---|---|---|
| Qué produce el agente | Una **guía de locución** por video: la narración partida por paso, numerada, con indicaciones de pronunciación y pausas. | El audio de cada paso, generado por un servicio de voz. |
| Qué hace el usuario | Graba **un archivo por paso** (`1.1-paso-01.wav`, …) con el micrófono, en un lugar silencioso. Alternativa: un solo archivo con 2 s de silencio entre pasos, y el agente lo corta con `ffmpeg silencedetect`. | Elige la voz y escucha el resultado. |
| Voz | La del usuario. | Borrador: voces del Mac (`say`, «Paulina» es_MX). Publicable: una voz neuronal en español de Colombia; recomendada Azure Speech `es-CO-SalomeNeural` o `es-CO-GonzaloNeural`, alternativas ElevenLabs u OpenAI TTS. |
| Costo | Tiempo de grabación del usuario. | Unos centavos de dólar por video en un servicio neuronal. Requiere una cuenta y una clave del usuario. |

- **Pronunciación:** un archivo `pronunciacion.json` reemplaza las siglas al generar la voz sintética. Por ejemplo, «SIIGO» se lee «sigo», «TRM» se lee «te, erre, eme», «CE-7» se lee «ce e siete» e «IVA» se lee «iva».
  - Los números de documento («2026BA00001») no se narran: la narración ya los evita.
- **Privacidad:** la narración solo tiene datos ficticios. Lo único que sale a Internet es ese texto, enviado al servicio de voz.

### 2.4 Montaje (ffmpeg)

1. **Video:** el `.webm` se convierte a `.mp4` H.264, 1080p, 30 fps.
2. **Audio:** se arma con cada paso en su marca de tiempo y se normaliza el volumen (−16 LUFS).
3. **Portada y cierre:** de 3 s, con el número y el título del video y el logo de la aplicación (`Frontend/wms/public`), generados como HTML y grabados igual.
4. **Subtítulos:** un archivo `.srt` desde la narración y las marcas de tiempo. Se entrega aparte, sin quemarlos en el video, salvo que el usuario lo pida.
5. **Salida:** `salida/<video>/<video>-voz-usuario.mp4`, `<video>-voz-sintetica.mp4` y `<video>.srt`.

## 3. Fases

| Fase | Qué se hace | Entregable | Checkpoint con el usuario |
|---|---|---|---|
| F0 | Decisiones de §5. | Respuestas. | Sí: no empieza nada sin ellas. |
| F1 | Base `wms_grabacion`, configuración local del API y del frontend, y siembra del piloto (§2.1). | Comando `recrear-y-sembrar`; las tres pantallas de inicio listas. | No. |
| F2 | Grabador base (§2.2) y video 1.1 **sin voz**, con pausas fijas. | `1.1/video.webm`. | **Sí:** revisión visual del cursor, el resaltado, el ritmo y el encuadre. Se ajusta el estilo antes de seguir. |
| F3 | Voz del 1.1: la guía de locución para el usuario y el audio sintético de borrador. Con la clave del servicio neuronal, también la versión publicable. | `1.1-guia-locucion.md` y los audios. | El usuario graba sus audios del 1.1. |
| F4 | Montaje de las dos versiones del 1.1 (§2.4). | Dos `.mp4` y el `.srt`. | **Sí:** el usuario compara la versión A y la B y elige la voz. |
| F5 | Videos 5.2 y 7.3, con la voz elegida (o las dos si sigue la duda). Se resuelven sus textos `[verificar en pantalla]` y se corrige el guion si hace falta. | Cuatro `.mp4` más sus `.srt`. | El usuario graba los audios de 5.2 y 7.3 si eligió su voz. |
| F6 | Informe del piloto: resultado por criterio (§1), tiempo por video, problemas, cambios a los guiones y propuesta para los 78 restantes (orden, lotes y qué videos necesitan trabajo a mano). | `informe-piloto-videos.md`. | **Sí:** decidir si se producen los 81 y cómo. |

## 4. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| El movimiento se ve mecánico. | Cursor con trayectoria curva y aceleración, pausas de lectura y zoom en los resultados. Se ajusta en el checkpoint de F2. |
| Una pantalla tarda en cargar o cambia de posición. | El script espera elementos concretos, nunca tiempos fijos. Las pausas de carga se recortan en el montaje si pasan de 1 s. |
| Un texto del guion no coincide con la pantalla. | `verificar(texto)` falla y lo reporta. Se corrige el guion: el código manda. |
| La voz sintética pronuncia mal las siglas. | Diccionario de pronunciación y revisión de cada audio en F3. |
| El servicio de voz no está disponible o cuesta más de lo esperado. | La versión con la voz del usuario no depende de él. |
| La preparación del depósito de 7.3 por API falla por reglas del negocio. | Se usa la misma secuencia de la operación real. Si un paso no tiene API, se hace con el grabador sin grabar. |
| Datos reales en cámara. | Base nueva y solo el dataset ficticio. La grabación nunca apunta a staging. |

## 5. Decisiones que necesito antes de empezar

| # | Decisión | Opciones | Propuesta |
|---|---|---|---|
| D1 | Dónde viven los scripts del grabador | (a) `Frontend/wms/tools/video-tutoriales/`, versionado, con su propio `package.json` (no toca las dependencias de la aplicación); (b) una carpeta sin git en `code_workspace/` | **(a):** los scripts son reutilizables y sirven de prueba de los flujos. Los videos generados (`salida/`) van en `.gitignore`. |
| D2 | Instalar `ffmpeg` en la máquina | `brew install ffmpeg` | Instalarlo. Es necesario para el montaje y no existe hoy en el sistema. |
| D3 | Base de grabación | (a) una base `wms_grabacion` nueva en el contenedor `wms-postgres-db`; (b) un contenedor aparte | **(a)**, si el contenedor es solo de desarrollo local. |
| D4 | Servicio de voz neuronal | Azure Speech (es-CO), ElevenLabs, OpenAI TTS, o ninguno (solo `say` como borrador) | **Azure Speech** por sus voces de Colombia. El usuario crea la cuenta y deja la clave en una variable de entorno; el agente no la escribe en ningún archivo. |
| D5 | Formato de entrega | MP4 1080p 30 fps; subtítulos `.srt` aparte o quemados | MP4 con `.srt` aparte. |
| D6 | Portada y cierre | Con el logo de la aplicación o sin logo | Con el logo de `Frontend/wms/public` y el título del video. |

## 6. Qué necesita el usuario hacer

- Responder las decisiones D1–D6.
- Si se elige su voz: grabar los audios por paso del 1.1 (en F3) y luego de 5.2 y 7.3 (en F5), siguiendo la guía de locución. Son unos 15 pasos en total.
- Si se elige la voz neuronal: crear la cuenta del servicio y dejar la clave en una variable de entorno (p. ej. `AZURE_SPEECH_KEY` y `AZURE_SPEECH_REGION`).
- Revisar los videos en los checkpoints de F2, F4 y F6.

## 7. Avance

| Fase | Estado | Notas |
|---|---|---|
| F0 | Hecha (7-oct-2026) | D1–D6 aprobadas tal como se propusieron; D4 = Azure Speech. |
| F1 | Hecha | Base `wms_grabacion`, API en 5291 y app compilada en 3091 (desde una copia del código, para no tocar el `.output` del proyecto). La siembra del piloto corre en unos 4 s sobre una base nueva y deja el depósito 2026BA00001 con `canConfirm = true`. |
| F2 | Hecha; pendiente la revisión del usuario | `salida/1.1/1.1-sin-voz.mp4`, de 65 s, con portada, grabación a 1080p y cierre. Se grabó al primer intento; los textos del guion se verificaron en pantalla. |

| F3 | Voz sintética hecha; falta la voz del usuario | Azure Speech `eastus` conectado; la clave está en `Frontend/wms/.env`, ignorado por git. El 1.1 tiene la narración con Salomé (75 s) y con Gonzalo (67,5 s): 874 caracteres por voz, dentro de la capa gratuita. Hay una guía de locución para el usuario y un importador de sus audios. |
| F4 | Parcial | `1.1-voz-salome.mp4` y `1.1-voz-gonzalo.mp4`, con sus `.srt`. Sincronía verificada: cada narración empieza con su paso (detección de silencios) y el volumen es de −16 LUFS. Falta la versión con la voz del usuario. |

| Revisión del usuario | Hecha (7-oct-2026) | La voz sintética Gonzalo es suficiente: no hace falta grabar la voz del usuario. Visualmente, aprobado. Subtítulos: estaban demasiado grandes y tapaban el flujo; ahora van en una franja propia bajo la grabación, en bloques de máximo dos líneas, y el `.srt` queda aparte. |
| F5 y F6 | En pausa | Los videos 5.2 y 7.3 quedan para cuando se definan los ajustes de permisos y roles. La siembra del 7.3 ya está hecha y probada. |

**Entregable de la prueba de factibilidad:** `video-tutoriales-trabajo/salida/1.1/1.1-voz-gonzalo.mp4` (67,5 s) con `subtitulos/1.1-voz-gonzalo.srt`.

**Conclusiones de factibilidad (con el 1.1):**
- **Es factible y repetible.** Con el ambiente arriba, un video sale con cuatro comandos (`voz` → `grabar --voz` → `montar --voz`, más `preparar()` si el video crea datos) en unos 2 minutos de máquina: unos 3 s de voz, la duración del video en grabación y unos 30 s de montaje.
- **El esfuerzo está en el script de cada video.** El 1.1 tiene 5 pasos y unas 50 líneas. Los textos del guion se verifican solos: si la pantalla cambia, el video falla en vez de salir mal.
- **Costo:** $0. Unos 875 caracteres por video; los 81 videos, unos 55.000, dentro de la capa gratuita de Azure.
- **Duración real:** con la voz Gonzalo, unos 67 s para el 1.1, frente a los «3 min» del guion. Las duraciones de los guiones están sobreestimadas cerca de 2,5 veces.
- **Riesgo principal:** los cambios de la interfaz (como el ajuste de permisos y roles) obligan a ajustar el script y a volver a correrlo, no a regrabar a mano.

**Hallazgos de F1–F2:**
- **Escala de la grabación:** Playwright graba en píxeles CSS. Una escala de dispositivo de 1,25 no agrandaba el video: dejaba un borde gris. Se graba a 1536×864 y el montaje escala a 1080p.
- **Lanzador de la vista previa:** no puede ejecutar `bash` sobre el disco externo (`/Volumes`), así que la API se arranca con un script de Node.
- **Duración de los videos:** la narración del 1.1 a un ritmo normal (unos 14 caracteres por segundo) da un video de unos 65 s, frente a los «3 min» del guion. Las duraciones de los guiones están sobreestimadas: se ajustarán con las medidas reales del piloto.
- **Hallazgo H1 confirmado:** Trazabilidad muestra «Input» en inglés. Los videos del Admin arrancan en Notificaciones.
