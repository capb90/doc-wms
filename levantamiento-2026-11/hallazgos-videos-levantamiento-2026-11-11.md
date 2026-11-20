# Hallazgos de los videos del levantamiento en staging (noviembre de 2026)

Corte: 2026-11-11. Videos grabados por el usuario en la visita a Bodegas Asociadas, con la operaria de Comercio Exterior trabajando en el **legacy**. Este documento deja por escrito lo que se ve en ellos para que nadie tenga que volver a procesarlos.

**Cómo se leyeron.** Fotogramas cada 4 s con `ffmpeg` y lectura de cada pantalla. El audio **no** se transcribió (no hay herramienta de transcripción en el equipo). El contexto hablado se tomó de la transcripción de las sesiones (`documentos/Levantamiento staging/Comercio exterior.txt`) y de la revisión del usuario (`documentos/Levantamiento staging/revision_hallazgos.md`, puntos PA-xx). Los tiempos son aproximados (±4 s).

**Datos omitidos a propósito.** Los videos muestran nombres de personas (operaria, conductores, quien llama por WhatsApp), placas, NIT e importadores reales. Aquí se reemplazan por descripciones (DEC-007). Se conservan el número de depósito y los conteos.

## Caso que muestran los dos videos

Un mismo depósito de importación, `BA3066`: 1 producto (fruta fresca en cajas), **930 cajas** y **24 940 kg**, que llegó en **dos camiones** (dos tiquetes de ingreso) y salió completo el mismo día sin descargar. Es el escenario «salida global» de PA-14.

## Video 1 — `levante_y_salida_global.MOV` (1 min 57 s, vertical)

| Tiempo | Pantalla legacy | Qué se ve |
| --- | --- | --- |
| 0:00–0:24 | *Comercio Exterior › Depósitos Import.* — «Listado de depósitos en bodega» | Tabla: fecha, identificador del depósito, detalles (carta porte, importador, transportadora, manifiesto DIAN), producto y una subtabla por vehículo (placa, cantidad, peso). Bajo cada depósito: «Peso Entra», «P.Bruto Ampara», «Saldo Peso» y el botón «Gestionar Amparados». Una ventana de llamada tapa parte de la pantalla. |
| 0:28 | *Levantes Import.* — «Registro de levante» | Nro. depósito, importador, carta porte, fecha y hora de ingreso, manifiesto. Matriz con filas **Ingreso / Nacionalizados / Saldo** y columnas **Cant. / Peso / una columna por producto** (930 · 24 940 kg · 930 cajas). Campos del levante: Tasa cambio (precargada, 3166,91), CIF USD, Peso bruto (kg), Nro. levante, Nro. aceptación, Fecha (solo la del levante), y FOB CO calculado. Botón «Lista de levantes». |
| 0:40 | Registro de levante, digitando | Al escribir el peso bruto (249…) la cantidad del producto se calcula sola en proporción a lo ingresado: 249 × 930 ÷ 24 940 = 9,29 (`registrarlevante.php:246-254`; solo con un producto, `:611`). Con 24 940 kg queda 930. FOB CO = CIF USD × tasa (≈ 10,18 millones con CIF 3216,03). |
| 0:56 | Registro de levante, guardado | El levante aparece en la matriz (número de levante, aceptación, fecha, FOB US). Nacionalizados 930 / 24 940; **Saldo 0**. Iconos de editar y eliminar el levante. |
| 1:12 | *Salidas Import.* — «Registro de salida de mercancía» | Encabezado del depósito y matriz de saldos (sin nacionalizar / nacionalizados / disponibles). Abajo, **un renglón por tiquete de ingreso** (dos tiquetes, cada uno con su peso) con la cantidad que sale; campos de fecha de salida, transportadora, cuadrilla y observaciones; botón «Guardar». |
| 1:20 | Listado de depósitos | Varios depósitos con sus vehículos y el resumen de pesos; la operaria vuelve al listado tras guardar la salida. |
| 1:36 | «Vista previa de la guía de salida de bodega» | Guía con código de barras: importador, NIT, **dos tiquetes**, **dos placas**, conductores, transportadora, agencia (SIA), y una línea por producto con doc/CPI, depósito, manifiesto, levante, aceptación, embalaje, entrada, saldo anterior, cantidad que sale y nuevo saldo («Total en esta salida 930 cajas»). Observación tipo «salida de mercancía completa a disposición del importador», responsable, cuadrilla, destino, vencimiento y firmas (entrega, importador). Botones Imprimir, Guardar y Volver. |
| 1:52 | PDF de la guía | La misma guía impresa a PDF. |

Hallazgos del video 1:

1. **El levante calcula la cantidad desde el peso digitado**, en proporción a lo ingresado (no al saldo), y solo cuando el depósito tiene un producto. Es lo que la operaria pide en PA-12.
2. **La tasa de cambio llega precargada** con la tasa semanal y es editable en el formulario (PA-08, PA-24).
3. **Solo pide la fecha del levante**; no hay fecha de aceptación (PA-11).
4. **Una matriz con una columna por producto** muestra ingreso, nacionalizado y saldo de todos los productos a la vez (PA-09).
5. **Salida global:** una sola guía con los dos tiquetes de ingreso y las dos placas, sin orden de cargue y sin pasar de nuevo por báscula (PA-14). El firmante de la guía es el importador.

## Video 2 — `proceso_levante_edicion_pesos.mov` (3 min 31 s, horizontal)

| Tiempo | Pantalla legacy | Qué se ve |
| --- | --- | --- |
| 0:16 | *Comercio Exterior › Tickets Ingresos* — «Lista de pesajes por entrada de mercancía» | Columnas: fecha y hora, vehículo, conductor, ID conductor, peso bruto, peso mercancía, tara vehículo, cantidad, peso manifiesto, doc. entrada, repesa, valor, tiquete, estado y acciones. Botones «Nuevo pesaje entrada» y «Vehículo con varios doc.». |
| 0:32 | «Modificar entrada a báscula» (`L/mod_bascula/modificarentrada.php`) | Formulario completo del tiquete: vehículo y país, unidad de carga, conductor, modalidad, doc. comercial (carta porte) y número, empresa de transporte, nro. y fecha del manifiesto, **Pesaje (kg): P. indicador, P. manifiesto, T. vehículo, P. mercancía**, naturaleza de la carga, productos transportados (producto, embalaje, cantidad, «Agregar detalles», «Agregar lista»), precio y moneda, y a la derecha convenio, valor a cobrar, IVA y «Facturar a». Botón «Actualizar registro». |
| 0:52–1:36 | Mismo formulario, editando | La operaria cambia **P. indicador 18 560 → 18 660**, **P. manifiesto 11 210 → 11 240** y **P. mercancía 11 300 → 11 240**. La **T. vehículo se recalcula sola: 7 260 → 7 420** (indicador − mercancía). Guarda. |
| 2:04–2:20 | Portal DIAN MUISCA — «Planilla de recepción» | Relación de documentos de la planilla: bultos enviados 420, **peso enviado 11 300 kg**, bultos recibidos 420, **peso recibido 11 240 kg**. Es el dato contra el que cuadra el tiquete. |
| 2:36 | «Modificar datos del depósito» | Fecha y hora del depósito (editable), **número del depósito (editable)**, observaciones, y en solo lectura los datos del ingreso: carta porte, transportadora, manifiesto DIAN, intermediaria, remitente, peso neto y bruto, precio. |
| 3:08 | «Relacione los productos amparados y sus cantidades» | Alta de producto, embalaje y cantidad amparada; tabla con el producto amparado (930 cajas). |
| 3:28 | «Registro de levante» | Mismo formulario del video 1, antes de registrar el levante: saldo 930 / 24 940 kg. |

Hallazgos del video 2:

1. **Comercio Exterior corrige los pesos del tiquete después de creado el depósito** para que coincidan con la planilla de recepción de la DIAN (PA-02, PA-13, PA-22). Cambia indicador, manifiesto y mercancía en **un solo formulario**.
2. **El peso de la mercancía lo digita la operaria** y de él sale la tara (T. vehículo = indicador − mercancía). Según la transcripción («Edición y cálculo de pesos»), muchos camiones no se repesan y ese peso sale de pesar bultos de muestra.
3. **El cambio se ve en vivo en el depósito y en el levante** porque el legacy lee los pesos del tiquete.
4. **Datos del depósito editables en cualquier momento**: fecha, número y observaciones.
5. **Productos amparados** se registran aparte, con su cantidad amparada.

## Contexto de la transcripción que los videos no muestran

De `Comercio exterior.txt` (sin nombres):

- **Tasa de cambio:** la registran a mano cada lunes; las declaraciones anticipadas usan la tasa de una semana anterior, por eso debe poder cambiarse en el levante.
- **Órdenes de cargue:** varios clientes autorizan cargar antes de saber cuánto cabe en el camión y envían la orden después. La orden de la v2 debe poder crearse al cargar (PA-14).
- **Inventario nacionalizado:** piden un reporte de la mercancía nacionalizada con sus levantes, filtrable por fecha (PA-15).
- **Productos:** quieren ver el embalaje junto al nombre del producto y crear productos y terceros desde el formulario.
- **Depósitos:** prefieren ver la información en tabla (vehículos, cantidades, manifiesto) antes que en tarjetas.

## Cómo regenerar los fotogramas

Los fotogramas no se guardan en el repo porque muestran datos de personas. Para volver a sacarlos:

```bash
ffmpeg -i "/Volumes/Dock/Projects/bodegas_asociadas/documentos/Levantamiento staging/levante_y_salida_global.MOV" -vf "fps=1/4" v1_%03d.jpg
```

```bash
ffmpeg -i "/Volumes/Dock/Projects/bodegas_asociadas/documentos/Levantamiento staging/proceso_levante_edicion_pesos.mov" -vf "fps=1/4" v2_%03d.jpg
```

El fotograma `NNN` corresponde al segundo `(NNN − 1) × 4`.
