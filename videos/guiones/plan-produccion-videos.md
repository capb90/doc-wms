# Plan de producción — Videos tutoriales generados por un agente

> **Fecha:** 7 de octubre de 2026. **Estado:** F1 a F6 aprobadas; F7 entregada para revisión: los 81 videos están producidos (ver §4).
> **Antecedente:** el piloto (`plan-piloto-videos.md`) demostró la factibilidad con el video 1.1. El usuario aprobó estas fases y el punto de partida independiente por video el 7-oct-2026.
> **Herramientas:** `Frontend/wms/tools/video-tutoriales/` (README con el uso).

## 1. Método

- **Un punto de partida por video.**
  - Antes de cada video, la base `wms_grabacion` se copia de una plantilla limpia: migraciones, administrador inicial y cuentas C1–C6.
  - El script del video siembra por API lo que necesita encontrar hecho (`preparar`).
  - Así, cualquier video se regraba solo, sin rehacer los anteriores, y las fases se agrupan por módulo.
- **Mismo dataset.** Los datos y sus ID son los de `dataset-grabacion.md`. Solo cambia quién los crea: la siembra, en vez del video anterior. El orden de grabación de su §3 ya no es obligatorio.
- **Sin cambios de producto.** Lo que el video no puede mostrar como dice el guion se corrige en el guion (lo que se ve en pantalla manda) o se reporta como hallazgo.
- **Lo que sigue igual:**
  - voz Azure `es-CO-GonzaloNeural`;
  - franja de subtítulos con el `.srt` aparte;
  - ambiente aislado 5291/3091;
  - nunca staging.

## 2. Fases

| Fase | Videos | Cant. | Lo nuevo o lo difícil |
|---|---|---|---|
| **F1 · Base de producción + Administración** | 1.2 – 1.13 (y el 1.1 regrabado) | 12 | Comando por lote, plantilla, utilidades de PrimeVue y hoja de revisión. |
| **F2 · Acuerdos** | 2.1 – 2.10 y 3.1 | 11 | Fórmulas, previsualización y activación (H4). |
| **F3 · Entrada de mercancía** | 4.1, 5.1–5.8, 5.10, 6.1–6.4 | 14 | Tres roles en un flujo; 5.5 en un solo video; firma; regrabar el 5.2 del piloto. |
| **F4 · Depósito en Comercio Exterior y Bodega** | 6.5, 6.8, 6.9, 7.1–7.9, 7.14 (el 6.7 pasa a F5) | 13 | Incluye el 7.3 del piloto. Archivos y CSV; fechas movidas para abandono; CE-7. |
| **F5 · Salida de mercancía** | 4.2–4.4, 5.9, 5.11, 5.12, 6.6, 6.7, 7.10–7.13, 7.15 | 13 | Orden de cargue, guía y repesaje. Los PDF se muestran en pantalla. |
| **F6 · Facturación** | 3.2 – 3.13 | 12 | Cliente bloqueado por mora (fechas movidas y la tarea programada) y TRM pendiente (DIAN caída solo en el API de grabación). |
| **F7 · Introducción y cierre** | 0.1 – 0.5 | 5 | Bandeja de correo local para 0.3; H1 en 0.5; duraciones reales en los guiones, PDF y paquete final. |

## 3. Ciclo de cada fase

1. **Siembra** del punto de partida de cada video, en `siembra/datos.mjs`.
2. **Script** de cada video, contra el código y el guion. Se prueba con `producir --ensayo`.
3. **Producción** con voz: `producir` y `hoja` para revisar.
4. **Entrega** al usuario: los MP4 y una tabla con duración y observaciones.
5. **Ajustes** según la revisión y mensajes de commit para los dos repositorios. El agente no hace commits.

No se empieza una fase hasta que el usuario apruebe la anterior.

## 4. Avance

### F1 · Base de producción + Administración

**Herramientas nuevas:**
- **Plantilla y base por video:** `ambiente/base.mjs`, `ambiente/plantilla.mjs` (`npm run plantilla`, unos 8 s).
- **`npm run producir`:** el ciclo por video (base, API, siembra, voz con caché, grabación y montaje) y `salida/resumen.md`.
  - `--ensayo` prueba un script en unos 30 s.
  - Si algo falla, deja la captura, el árbol de accesibilidad y el paso.
- **Utilidades del grabador:** `menu(ruta)`, `senalar`, `aviso`, `elegir`, `fila`, `accion`, `columna`, `filtrar` y `dialogo`.
- **`npm run hoja`:** un fotograma por paso para revisar.
- **Piezas del dataset:** `usuarioNuevo` (C7), `gestionCuenta`, `transporte` (T4, VID101–VID107 y conductores) y `correoAjustes`.

**Hallazgos de F1:**

| # | Hallazgo | Qué se hizo |
|---|---|---|
| F1-1 | El campo «Precio base» de un servicio (moneda COP) no admite centavos: el navegador formatea el peso sin decimales y $16.806,72 se convierte en $1.680.672. | El 1.6 graba $16.807 (con IVA da los mismos $20.000) y el guion se corrigió. El usuario decidió (7-oct-2026) usar $16.807 en todo el dataset: S1, A.4 y 3.3 corregidos. El IVA de 3.3 ($3.193) se confirma al grabar F6. |
| F1-2 | Las marcas `[verificar en pantalla]` de 1.5 (botón «Nuevo») se confirmaron. | Marcas retiradas del guion. |
| F1-3 | En 1.11, VID107 llega sin tipo ni país (entró por «Solo bodega»): el video completa el tipo «Sencillo», que es lo que el guion llama «corregir». | Sin cambios de guion. |

**Resultado (7-oct-2026):** 13 videos producidos, 14 min 8 s en total. Unos 72 s de máquina por video y 10.096 caracteres de Azure (capa gratuita).

| Video | Duración | Guion decía |
|---|---|---|
| 1.1 | 1:08 | 3 min |
| 1.2 | 1:01 | 3–4 min |
| 1.3 | 1:52 | 4–5 min |
| 1.4 | 1:07 | 3 min |
| 1.5 | 0:48 | 2–3 min |
| 1.6 | 1:11 | 3–4 min |
| 1.7 | 1:17 | 4–5 min |
| 1.8 | 0:45 | 2–3 min |
| 1.9 | 0:54 | 2 min |
| 1.10 | 0:59 | 3 min |
| 1.11 | 0:59 | 3 min |
| 1.12 | 0:58 | 3 min |
| 1.13 | 1:09 | 3 min |

### F2 · Acuerdos

**Herramientas nuevas:**
- **Diapositivas** sobre la app: `diapositiva`, `destacarEnDiapositiva` y `quitarDiapositiva` (2.1 y 2.7).
- **Cambio de cuenta a mitad de video:** `cambiarUsuario` (2.1, paso 5).
- **Confirmaciones:** `confirmacion()`; `dialogo()` busca por el título del diálogo.
- **Piezas del dataset:** `baseAcuerdos` (T1 completo, T2, P1, P3, S1, S3 y S4), `acuerdoA0`, `servicioGeneralA1`, `servicioLlantasA1`, `acuerdoA2` y `configFacturacionT2`.
- **Voz:** los importes con «$» se leen en pesos; Azure decía «dólares».

**Correcciones de guion:**
- 2.5: se confirmaron las explicaciones de la previsualización y se retiraron sus marcas.
- 2.3: el paso 6 vuelve a «Fijo», porque «Por tipo de vehículo (montacargas)» no tiene «Mínimo por unidad de carga».
- 2.10 (revisión del usuario, 8-oct-2026): el paso 2 decía que el convenio de montacargas no aplica si tiene producto, modalidad o restricción de perecederos. Ahora dice que Bodega cobra el montacargas con el convenio del cliente o, sin convenio, con la tarifa general por tipo de vehículo. El código sí exige esos campos vacíos (`ForkliftService`), pero el paso 1 ya los deja así.
- 3.1: la ayuda «¿Qué significa cada opción?» viene abierta. La tabla necesita al menos una configuración para mostrar sus columnas, así que el punto de partida incluye la de T2 (PREP-2).

**Resultado (7-oct-2026):** 11 videos producidos, 11 min 23 s en total, con 7.842 caracteres de Azure.

| Video | Duración | | Video | Duración |
|---|---|---|---|---|
| 2.1 | 1:13 | | 2.7 | 1:14 |
| 2.2 | 1:04 | | 2.8 | 1:02 |
| 2.3 | 1:08 | | 2.9 | 1:00 |
| 2.4 | 1:09 | | 2.10 | 0:56 |
| 2.5 | 0:47 | | 3.1 | 1:04 |
| 2.6 | 0:46 | | | |

### F3 · Entrada de mercancía

**Herramientas nuevas:**
- **Localizadores:**
  - `campo(etiqueta, ámbito)`: el campo que sigue a una etiqueta visible; sirve en la ficha de báscula y en la recepción directa.
  - `camionCola(placa)`: un camión de la cola de báscula.
- **Acciones físicas:**
  - `firmar(lienzo)`: una rúbrica ficticia con el mouse.
  - `subirArchivos(botón, rutas)`: entrega archivos al selector.
- **Fotos ficticias de mercancía (ARCH-1):** `siembra/archivos.mjs` las dibuja con el navegador.
- **Movimiento del cursor:** centra en pantalla el elemento que queda junto a una barra fija. Antes, el clic caía en la barra de «Guardar» de la báscula y el texto no se escribía.
- **Piezas del dataset:**
  - base: `baseOperacion` (T3, T4, P2, U1, U2, Q1 y configuración de T1) y `terceroT6Bloqueado`;
  - Vigilancia y Báscula: `ingresos`, `registrarDeposito`, `cobrarDeposito`, `pesar` y `registrarSoloBascula`;
  - Bodega: `llegadaBodega`;
  - depósitos ya hechos: `deposito1` (2026BA00001) y `deposito2` (2026BA00002, tanquero).
- **Numeración del guion:** el punto de partida de 5.6, 5.8 y 6.3 incluye los depósitos anteriores, para que los números coincidan con el guion.
- **5.5 en un solo video:** la llegada a Bodega se registra fuera de cámara entre los pasos 2 y 3.

**Hallazgos de F3:**

| # | Hallazgo | Qué se hizo |
|---|---|---|
| F3-1 | Al guardar un depósito adicional (5.8), el aviso dice «Camión asociado al depósito 2026BA00004», no «Depósito 2026BA00004 creado»: el aviso trata el depósito nuevo como un camión más. | El guion muestra el texto real. Si se corrige el aviso, se regraba el 5.8. |
| F3-2 | En Solo báscula con un solo peso, «Tipo de peso» no viene preseleccionado en «BRUTO (Cargado)». Si no se elige, el tiquete sale como «Tara (vacío)». | El 5.2 elige «BRUTO (Cargado)», como dice el guion. Decisión del usuario (8-oct-2026): BRUTO debe venir por defecto; lo corregirá otro agente sin regrabar. |
| F3-3 | El bloqueo por mora (T6) lo pone la tarea de cartera. Para no depender de fechas, la preparación del 5.4 lo fija directo en la base de grabación. | Sin cambios de guion. |

**Correcciones de guion:**
- **5.2:** se confirmó «Total a pagar» $ 20.000.
- **5.8:** el aviso del depósito adicional (F3-1).
- **6.3:** «Completar Recepción» se habilita con la firma, así que se firma en el paso 3 y el aviso de la unidad sin confirmar aparece después.
| F3-4 | Con el precio de báscula en $16.807 (F1-1), el cobro se registra por $ 20.000,33: «Total a pagar» muestra $ 20.000, pero el resumen dice «Cobrado: $ 20.000,33». | Decisión del usuario (8-oct-2026): corregir el campo para que admita centavos; lo hará otro agente. Los videos ya grabados no cambian. Desde F4, la siembra vuelve a $16.806,72 por API y el dataset también. |

**Ajustes tras la producción:** el 5.4 confirma la elección del cliente bloqueado, porque la ficha repone al cliente del depósito. El 6.2 usa el campo de ubicación de cada producto.

**Resultado (8-oct-2026):** 14 videos producidos, 15 min 13 s en total, con unos 9.600 caracteres de Azure.

| Video | Duración | | Video | Duración |
|---|---|---|---|---|
| 4.1 | 1:04 | | 5.7 | 1:07 |
| 5.1 | 1:13 | | 5.8 | 1:41 |
| 5.2 | 1:06 | | 5.10 | 0:51 |
| 5.3 | 1:20 | | 6.1 | 0:40 |
| 5.4 | 0:54 | | 6.2 | 1:01 |
| 5.5 | 0:55 | | 6.3 | 0:37 |
| 5.6 | 1:37 | | 6.4 | 1:07 |

**Revisión del usuario (8-oct-2026):**
- **Selector de conductor.** Báscula y Recepción directa cambiaron el formulario del conductor por un selector con alta en modal (commit `044be08` del guion). Se regrabaron 5.1, 5.2, 5.3, 5.6, 5.7, 5.8 y 6.4:
  - 5.2, 5.3 y 6.4 registran al conductor con «+» → «Registrar conductor», como dice el guion;
  - en 5.6, 5.7 y 5.8 los conductores ya existen (pieza `conductores`) y se eligen del listado.
- **Subtítulos duplicados** (5.4, 5.5, 5.10, 6.1 y 6.3, y en general todos). El `.srt` estaba en `entregables/` con el mismo nombre del video, y el reproductor lo cargaba encima de los subtítulos del video. Ahora va en `entregables/subtitulos/`. No hubo que regrabar.
- **Puertos.** El 5291 quedó ocupado por la API de otra sesión, así que esta producción usó API 5292 y app 3092 (variables `VIDEO_PUERTO_API` y `VIDEO_PUERTO_APP`).

### F4 · Depósito en Comercio Exterior y Bodega

**Herramientas nuevas:**
- **Visor de PDF:** `mostrarPdf` y `volverDePdf`. Las etiquetas y los reportes abren otra pestaña, que no queda en la grabación (y el navegador sin interfaz no dibuja PDF). Por eso se convierten en imagen con `pdftoppm` y se muestran sobre la página.
- **Buzón SMTP local:** `ambiente/buzon.mjs`, un proceso aparte que arranca con la API. Los correos de la app (ajuste CE-7 y, en F7, recuperar contraseña) se guardan en `video-tutoriales-trabajo/correo/` y no salen del equipo. Antes el correo apuntaba a un puerto cerrado y el CE-7 decía «no se pudo enviar el correo».
- **Fechas en los selectores:** `escribirFecha` y `hoy`.
- **`elegir`:** si la lista vuelve a abrirse dentro de un diálogo, la cierra.
- **Piezas del dataset:**
  - recorrido de entrada: `recepcion`, `deposito1Completo`, `depositos3y4`, `inspeccion1`, `recepcionDirecta`, `depositosAbandono` (ingresos retrocedidos 25 y 35 días con «Corregir ingreso»), `exportacion1` y `recorridoEntrada`;
  - Comercio Exterior y Facturación: `completarDeposito1`, `confirmarDeposito1`, `acuerdoA1Activo` y `facturaDeposito1Aprobada` (espera a que llegue la TRM de datos.gov.co);
  - montacargas, ubicaciones y archivos: `tarifasMontacargas`, `ubicacionesExtra` y `listaEmpaque` (ARCH-3).
- **El 6.7 pasa a F5.** Su kárdex debe mostrar un movimiento «Orden cargue», que requiere el flujo de salida que se siembra en F5.

**Hallazgos de F4:**

| # | Hallazgo | Qué se hizo |
|---|---|---|
| F4-1 | «Imprimir etiqueta» abre la pestaña con `window.open(url, "_blank", "noopener,noreferrer")`. Con `noopener` el navegador siempre devuelve `null`, así que la app cree que la ventana emergente fue bloqueada: muestra «Etiqueta descargada — Permita las ventanas emergentes…» y además descarga el archivo (`useDepositLabelPrint.ts`). | El 7.4 muestra el aviso real. |
| F4-2 | Los productos declarados en báscula no se pueden eliminar: su «Ingreso declarado» ya cuenta como movimiento de inventario («No se puede eliminar: ya tiene movimientos de inventario»). | El 7.5 muestra el botón deshabilitado con su motivo y se ajustó el guion. Decisión del usuario (8-oct-2026): se corrige; lo implementa otro agente. |
| F4-3 | El uso de montacargas iniciado con VID105 aparece en la lista con la placa VID101: la lista toma la placa del primer ingreso del servicio del depósito (`GetActiveForkliftUsesHandler`). | Sin cambios de guion (el paso no cita la placa). Decisión del usuario (8-oct-2026): se corrige; lo implementa otro agente. |
| F4-4 | En «Facturación y Cobro — Montacargas», «Pago inmediato» viene elegido y el selector permite quedar vacío: si se pulsa, se desmarca y «Finalizar y cobrar» no hace nada ni avisa. | El 6.5 no lo pulsa. Decisión del usuario (8-oct-2026): se corrige; lo implementa otro agente. |
| F4-5 | La «Recepción de Bodega (informativa)» del depósito muestra solo la última recepción (VID105). La diferencia de VID101 se ve en «Productos del Depósito». | Se ajustó el paso 5 del 7.2. Decisión del usuario (8-oct-2026): se corrige; lo implementa otro agente. |

**Correcciones de guion:**
- **6.5:** el aviso confirma el total con IVA.
- **7.2:** paso 5 (F4-5).
- **7.5:** paso 4 (F4-2).

**Resultado (8-oct-2026):** 13 videos producidos, 12 min 10 s en total. El 7.2 se regrabó para que se vea la tarjeta «Información General» ya actualizada después de guardar.

| Video | Duración | | Video | Duración |
|---|---|---|---|---|
| 6.5 | 0:59 | | 7.5 | 1:04 |
| 6.8 | 1:00 | | 7.6 | 0:50 |
| 6.9 | 0:47 | | 7.7 | 1:13 |
| 7.1 | 0:54 | | 7.8 | 0:45 |
| 7.2 | 1:11 | | 7.9 | 0:50 |
| 7.3 | 1:00 | | 7.14 | 0:47 |
| 7.4 | 0:50 | | | |

### F5 · Salida de mercancía

**Herramientas nuevas:**
- **`autocompletar`:** campos con búsqueda (AutoComplete), como el emisor de la orden externa.
- **Piezas del dataset:**
  - levantes y depósitos: `levante` (reintenta la TRM de datos.gov.co y, si no responde, usa la tasa manual del formulario), `deposito2Nacionalizado` y `depositosNacionalizados`;
  - catálogos: `catalogosSalida` (K1–K3, Q2 y S2) y `conductorJaime`;
  - órdenes y salida: `ordenCargue`, `orden1`, `orden2`, `salidaBascula1`, `cargue1`, `guia1`, `repesaje1` y `recorridoSalida`;
  - camiones de solo báscula: `vid113PorRepesar` y `vid102Completo`;
  - Vigilancia: `salidaVigilancia`, `ingresoVid109` y `corregirVid109`;
  - archivos: `ordenExternaPdf` (ARCH-4).
- **5.9 en un solo video:** el cargue en Bodega y la guía se hacen fuera de cámara entre los pasos 4 y 5 (`retomarSalida`).

**Hallazgos de F5:**

| # | Hallazgo | Qué se hizo |
|---|---|---|
| F5-1 | Crear una orden de cargue con mercancía de una unidad de carga (tanquero de 2026BA00002) es imposible desde la pantalla. El formulario lee `cargoHandling` del depósito y el API lo envía en cada producto (`LoadingOrderForm.vue:239`), así que nunca ofrece la unidad. El API rechaza la orden («…se despacha por unidad de carga: indique la unidad de cada producto») y la pantalla no muestra el error. | El 7.10 queda pendiente de la corrección (tarea propuesta); su script ya está listo. Decisión del usuario (8-oct-2026): se corrige; lo implementa otro agente. |
| F5-2 | En la ficha de báscula, el estado de la orden de cargue sale en inglés («Pending»). | Sin cambios de guion. Decisión del usuario (8-oct-2026): se corrige; lo implementa otro agente. |
| F5-3 | El historial de guías muestra un producto que no está en la orden (el primer producto del depósito del primer ítem) y suma cantidades de unidades distintas (`GetDispatchGuidesHandler.cs:79-86`). En el video, 2026S00001 aparece como «Llantas para camión 5200». | Sin cambios de guion. Decisión del usuario (8-oct-2026): se corrige; lo implementa otro agente. |
| F5-4 | «Cambiar modo de pago» de una guía solo aparece si no tiene factura (`!invoiceItemId`), y la guía genera sus facturas al crearse, así que en el flujo normal no aparece. | Se ajustó el paso 4 del 7.13. Decisión del usuario (8-oct-2026): se corrige; lo implementa otro agente. |
| F5-5 | El historial de báscula solo muestra ciclos cerrados (`WeighbridgeHistoryFilters.cs:80`): un pesaje «Por repesar» no se puede anular desde ahí, aunque el aviso de salida de Vigilancia (4.2) dice «Termínelo o anúlelo en Báscula». | En el 5.11, VID113 se deja con su segundo peso y el video lo anula. Decisión del usuario (8-oct-2026): se corrige; lo implementa otro agente. |

**Correcciones de guion:**
- **4.2:** el título del aviso, «Error al registrar salida».
- **4.3:** el estado de los ingresos es «Registrado».
- **5.9:** el paso 6 es una diapositiva.
- **5.11:** requisitos (F5-5).
- **7.11:** el texto real del diálogo de revertir.
- **7.12:** sin marca.
- **7.13:** paso 4 (F5-4).

**Ajustes tras la producción:**
- **El visor de PDF se cierra al empezar el paso siguiente.** Antes se cerraba a los 4 s, mientras el narrador seguía hablando del documento. Se regrabaron 6.8, 7.7, 5.11, 5.12 y 7.12.
- **5.11:** cierra el detalle de VID102 antes de abrir VID113. Antes se anulaba el pesaje equivocado.
- **7.12:** muestra el PDF de la guía pidiéndolo al API.

**Resultado (8-oct-2026):** 12 videos producidos, 10 min 41 s en total. El 7.10 se grabó después de la corrección F5-1 (1:14). Aprobada por el usuario el 8-oct-2026. El PDF de la guía también suma bultos y litros («Total en esta salida 5200 LITRO»); se le indicó a la tarea de F5-3.

| Video | Duración | | Video | Duración |
|---|---|---|---|---|
| 4.2 | 0:46 | | 6.6 | 0:59 |
| 4.3 | 0:44 | | 6.7 | 0:58 |
| 4.4 | 0:58 | | 7.11 | 0:47 |
| 5.9 | 1:12 | | 7.12 | 0:57 |
| 5.11 | 1:07 | | 7.13 | 0:43 |
| 5.12 | 0:38 | | 7.15 | 0:54 |

### F6 · Facturación

**Herramientas nuevas:**
- **`s.reiniciarApi(entorno)`:** la siembra puede reiniciar el API de grabación con otra configuración. Se usa para dejar la DIAN sin respuesta (3.9) y para que corra la tarea de cartera, 30 s después de arrancar (3.12).
- **`g.ids`:** `producir` guarda los id de `s.ids` en `salida/<n>/siembra.json` y el script los recibe como `g.ids`. Así abre la factura exacta: el listado de facturas no muestra la placa ni el depósito.
- **`idsFacturas` y `factura`:** ubican las facturas por SQL: el ciclo de báscula, el cobro de cada depósito, el período de almacenamiento, el montacargas, la guía y el número SIIGO.
- **Piezas del dataset:**
  - `recorridoFacturacion` y `almacenamientoBasico`;
  - `montacargas1`, `minimoExportacion` y `minimoImportacion`;
  - `moraT6`: el bloqueo lo pone la tarea de cartera real, no SQL;
  - `deposito7TrmPendiente`, `ajusteCe7`, `sobrescribirExp`, `anularYRefacturarExp`;
  - `numerarFactura` y `pagarFactura`.
- **Archivos:** `comprobantePdf` (ARCH-2).
- **`videos/_facturacion.mjs`:** abrir una factura, el diálogo «Acciones», la campana y las confirmaciones.

**Correcciones de guion:**
- **3.2, 3.9 y 3.11:** la campana lleva a «Ver todas las notificaciones». El panel de la campana se cierra solo a los pocos segundos, antes de terminar la narración.
- **3.4:** la factura en cero del depósito adicional (cobro inmediato) aparece «Pagada», así que no «se aprueba»; ahora la narración dice que no se le asigna número SIIGO.

**Hallazgos:** ninguno nuevo de producto.

**Resultado (9-oct-2026):** 12 videos producidos, 11 min 1 s en total. Aprobada por el usuario el 9-oct-2026.

| Video | Duración | | Video | Duración |
|---|---|---|---|---|
| 3.2 | 0:47 | | 3.8 | 0:58 |
| 3.3 | 1:05 | | 3.9 | 1:04 |
| 3.4 | 1:07 | | 3.10 | 0:52 |
| 3.5 | 0:55 | | 3.11 | 0:58 |
| 3.6 | 0:41 | | 3.12 | 0:57 |
| 3.7 | 0:51 | | 3.13 | 0:46 |

### F7 · Introducción y cierre

**Herramientas nuevas:**
- **Sin sesión:** `usuario = null` en el script abre la app en «Iniciar Sesión» (0.2 y 0.3).
- **`g.escribirClave(campo, nombre)`:** escribe una contraseña de `credenciales.local.json` sin que el valor pase por el script. Se agregaron dos contraseñas de prueba: la definitiva de `video.nuevo` y la restablecida de `video.admin`. `credenciales.mjs` ahora agrega las claves que falten sin tocar las existentes.
- **`g.mostrarCorreo(asunto)`:** lee el último correo del buzón local (`TRABAJO/correo/*.eml`) y lo muestra como una bandeja de pruebas. El botón del correo lleva a la app como en un correo real (0.3).

**Correcciones de guion:**
- **0.2:** el aviso de credenciales es «No se pudo completar la acción» — «Credenciales inválidas».
- **0.4:** Vigilancia registra el ingreso de VID109 fuera de cámara, no en una segunda ventana. «Mi cuenta» tiene el interruptor «Tema claro» y el «Tipo de menú» «Estático / Horizontal».
- **0.5:** el filtro de fecha son botones («Hoy / Esta semana / Este mes / Todo el historial»).

**Hallazgos:** sigue H1. En Trazabilidad, las etiquetas de tipo («Input», «OutputCargo») y los estados del detalle («Complete», «Confirmed») salen en inglés; el 0.5 no los acerca.

**Cierre del paquete:**
- **Duraciones reales en los guiones:** las de los 81 videos grabados; el PDF se regeneró.
- **Índice de videos:** `entregables/indice-videos.csv` y `indice-videos.json` con número, serie, título, título corto, rol, duración, objetivo, video y subtítulos.

**Resultado (9-oct-2026):** 5 videos producidos, 4 min 45 s. **Total de la producción: 81 videos, 1 h 20 min 34 s.**

| Video | Duración |
|---|---|
| 0.1 | 1:16 |
| 0.2 | 1:03 |
| 0.3 | 0:45 |
| 0.4 | 0:47 |
| 0.5 | 0:54 |
