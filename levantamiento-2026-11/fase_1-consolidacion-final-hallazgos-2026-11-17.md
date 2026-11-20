# Consolidación final de hallazgos – Proyecto WMS

Corte: 2026-11-17. Cierre documental de la fase 1 (levantamiento en staging de noviembre de 2026). Las referencias al código de la v2 provienen del material de este levantamiento (Backend `develop` `aa69633` · Frontend `develop` `8c7f20e`); este documento no analiza código.

> **Alcance.** Documento exclusivamente documental. Organiza, integra y clasifica lo recopilado. No define requerimientos, no diseña soluciones, no prioriza ni estima. Las propuestas de cambio aparecen como **propuestas no aprobadas**.

## 1. Contexto y alcance

**Visita.** Visita presencial al cliente (bodega que opera como depósito aduanero en Ipiales) el **6 de noviembre de 2026**, durante las pruebas de la nueva versión del WMS (v2) en staging. Se grabaron audios con Báscula, Comercio Exterior y Facturación (con temas de Bodega y Vigilancia), se tomaron notas y se grabaron dos videos de la operaria de Comercio Exterior trabajando en el legacy. La revisión del usuario fecha su análisis de interfaz el «2025-11-06»; en la consulta C-10 el usuario confirmó que la fecha correcta es 2026-11-06.

**Qué consolida este documento.**

1. Los 78 hallazgos y los 25 puntos pendientes de aclaración de la primera consolidación.
2. Las respuestas del usuario a esos 25 puntos, sus nuevos hallazgos y observaciones, y sus propuestas de flujo y diseño, con los mockups asociados.
3. Lo observado en los dos videos del legacy.
4. Las respuestas del usuario a las consultas de esta consolidación (C-01 a C-19).

**Tipos de información.** Cada elemento se clasifica con uno de estos tipos (criterio aprobado en C-02):

| Tipo | Qué es | Identificador |
|---|---|---|
| Hallazgo reportado por operarios | Situación expresada por los operarios en la visita | `H-xxx` |
| Aclaración | Información que precisa un hallazgo: hechos, lo que dijo o pidió el operario | `PA-xx` (respuestas de la revisión) y `C-xx` (consultas) |
| Observación de revisión | Situación que identificó el usuario al revisar la v2 o el legacy, o que se ve en los videos | `H-xxx` (nuevos) y `OV-xx` (videos) |
| Diferencia entre versiones | Comportamiento distinto entre el legacy y la v2, tal como lo describen las fuentes | `D-xx` |
| Propuesta de cambio | Modificación de flujo, comportamiento o interfaz planteada por el usuario o en la visita. **No es una decisión aprobada** | `PR-xx` |
| Referencia visual | Mockup o imagen relacionada | `MK-xx` (mockups) y `RV-xx` (imágenes y videos) |

Regla de clasificación (C-02): lo que en la revisión describe un hecho o lo que dijo o pidió el operario es **Aclaración**; lo prescriptivo («se debe…», «es mejor…») sin atribución a un operario es **Propuesta de cambio** con origen en la revisión del usuario; la sección 2 de la revisión es **Observación de revisión**, salvo donde dice que lo comentan los operarios.

**Estados documentales.**

| Estado | Significado |
|---|---|
| Consolidado | Sin cambios respecto de la primera consolidación |
| Consolidado con aclaración | Incorpora aclaraciones, observaciones o propuestas posteriores |
| Cerrado sin cambio | La aclaración indica que no hace falta un cambio (capacitación o funcionamiento correcto) |
| Corregido | La revisión corrigió un dato del contexto original; se conservan ambas versiones |
| Pendiente de aclaración | Falta información para cerrarlo |
| Propuesta no aprobada | Propuesta documentada, sujeta al análisis funcional |
| Documentado | Observación, diferencia o referencia registrada sin estado de avance |

**Nombres de personas.** Por indicación del usuario (C-19) se conservan los nombres que aparecen en la primera consolidación. Las credenciales del legacy local no se copian aquí.

## 2. Fuentes de información

| Código | Fuente | Ubicación | Qué aporta |
|---|---|---|---|
| F1 | Consolidación de hallazgos – Visita a cliente WMS (v1) | [`docs/levantamiento_staging/consolidacion_v1.txt`](../levantamiento_staging/consolidacion_v1.txt) | H-001 a H-078 y PA-01 a PA-25, con su trazabilidad a `bascula.txt`, `Comercio exterior.txt`, `facturacion.txt`, `Hallazgos.docx` y `CONVENIO 23-24-25-26.xlsx` |
| F2 | Revisión de hallazgos del usuario | [`docs/levantamiento_staging/revision_hallazgos.md`](../levantamiento_staging/revision_hallazgos.md) | §1 respuestas a PA-01–PA-25 · §2 comentarios extra por módulo · §3 recursos para el análisis funcional · §4 análisis de interfaz y propuestas |
| F3 | Hallazgos de los videos del levantamiento | [`docs/levantamiento-2026-11/hallazgos-videos-levantamiento-2026-11-11.md`](./hallazgos-videos-levantamiento-2026-11-11.md) | Lectura por fotogramas de los dos videos del legacy (OV-01 a OV-11) |
| F4 | Consultas de esta consolidación (2026-11-17) | Sección 2.1 de este documento | Respuestas del usuario a contradicciones y ambigüedades (C-01 a C-19) |
| Ref. | Análisis de paridad del flujo de depósitos | [`docs/levantamiento-2026-11/analisis-paridad-flujo-depositos-2026-11-11.md`](./analisis-paridad-flujo-depositos-2026-11-11.md) | **Solo referencia** (C-03). Se usa como evidencia para cerrar PA-04 (C-17) y se cita como insumo de la fase 2. Sus brechas no se incorporan como hallazgos |

La carpeta `docs/levantamiento_staging/` está excluida de git (`.gitignore`); los enlaces a ella funcionan solo en una copia local que la tenga. Los videos originales están fuera del repo (`documentos/Levantamiento staging/`, ver `docs/levantamiento-2026-11/README.md`).

### 2.1. Consultas resueltas durante la consolidación (F4)

| ID | Tema | Respuesta del usuario | Elementos afectados |
|---|---|---|---|
| C-01 | Entregables | Un solo documento con la matriz de trazabilidad incluida, en `docs/levantamiento-2026-11/` con el prefijo `fase_1` | Este documento |
| C-02 | Criterio de clasificación | Hecho o lo dicho por el operario = Aclaración; «se debe…» sin atribución = Propuesta; §2 de F2 = Observación de revisión salvo atribución a operarios | Todo el documento |
| C-03 | Uso del análisis de paridad | Solo como referencia; insumo para la fase 2 | Secciones 2 y 12 |
| C-04 | Unidad de medida (PA-05 vs F2 §4) | Lo que usan Facturación y Comercio Exterior (PA-05) es el **embalaje**. La unidad de medida se propone quitar de toda la app | H-018, H-033, PR-12 |
| C-05 | Tipo de vehículo (PA-23 vs v1) | PA-23 reemplaza lo anterior: se quita de báscula y en bodega es **opcional**. «Obligatorio en bodega» queda como antecedente | H-076, PR-10 |
| C-06 | Interfaz de levantes (PA-09 vs mockup) | El mockup de `mockups/levantes/` es la propuesta. Las dos opciones de PA-09 quedan como contexto de lo que dijo la operaria | H-036, H-040, PR-19 |
| C-07 | Vista 2 del mockup de levantes | Forma parte de la propuesta, como vista aparte | PR-19, MK-05 |
| C-08 | Orden de cargue (PA-14 vs H-072) | Es el mismo escenario: un camión puede entrar a cargar sin orden previa; pasa primero por báscula, donde no existe la orden, y por eso se propone crearla ahí en borrador. Luego el camión carga; cuando el cliente ya sabe qué va a cargar, le pasa la orden de cargue a Comercio Exterior. Esto debe tener en cuenta los tres tipos de salida y tiene como referencia el legacy | H-042, H-072, PR-21 |
| C-09 | Etapa Bodega del detalle del depósito | El descargue lo registra el **operario de bodega** (en F2 §4 dice «operario de báscula» por error de redacción) | PR-17 |
| C-10 | Fecha de la visita | 2026-11-06 | Sección 1 |
| C-11 | Sección «Datos para Comercio exterior» | Son dos secciones distintas. La de báscula se quita: el operario no la va a utilizar. En Comercio Exterior sí va, con Unidades de carga, Fecha de manifiesto, Precio de la mercancía y Moneda | PR-01, PR-17 |
| C-12 | Horómetro (PA-18) | El input ya acepta decimales | H-053 |
| C-13 | Selección de la modalidad en báscula | Radio buttons, como el mockup: una sola modalidad por registro (en F2 §4 dice «checkbox» por error) | PR-01 |
| C-14 | Depósito de inspección (PA-01) | Se maneja igual que importación; el usuario ya lo confirmó con los operarios | H-001, PR-07 |
| C-15 | Tasa de cambio (PA-24) | Una sola tasa semanal compartida por Comercio Exterior y Facturación | H-034, H-077, PR-23 |
| C-16 | Subpuntos sin respuesta | Se cierran: cifras del audio de PA-02, columna «IVA Sí/No» de PA-16 (reemplazada por el switch y los estados de PR-24) y numeración del reporte de PA-17. **Sigue pendiente:** mercancía y embalaje de PA-19. Además, el usuario agrega que la vista `/foreign-trade/loading-orders/create` se debe rediseñar y que la propuesta de diseño depende del análisis funcional | H-008, H-051, H-052, H-055, PR-22 |
| C-17 | PA-04: qué muestra hoy la v2 | Se cierra con la evidencia del análisis de paridad: las coincidencias muestran depósitos abiertos, en borrador **o** confirmado | H-011 |
| C-18 | PA-15: formato del inventario | Pasa a la fase 2 | H-043 |
| C-19 | Nombres de personas | Se mantienen como en la v1 | Todo el documento |

## 3. Resumen general de la consolidación

| Concepto | Cantidad |
|---|---:|
| **Hallazgos (`H-xxx`)** | **86** |
| · de la primera consolidación (H-001 a H-078) | 78 |
| · nuevos (H-079 a H-086) | 8 |
| Hallazgos de Báscula | 25 |
| Hallazgos de Bodega | 2 |
| Hallazgos de Comercio Exterior | 20 |
| Hallazgos de Facturación | 25 |
| Hallazgos transversales | 14 |
| Hallazgos pendientes de clasificación | 0 (H-078 pasó a transversales con PA-25) |
| Por tipo: hallazgos reportados por operarios | 79 (H-001 a H-078 y H-084) |
| Por tipo: observaciones de revisión del usuario | 7 (H-079 a H-083, H-085, H-086) |
| **Aclaraciones a pendientes (`PA-xx`)** | **25** |
| **Observaciones de los videos (`OV-xx`)** | **11** |
| **Diferencias entre versiones (`D-xx`)** | **27** |
| **Propuestas de cambio (`PR-xx`)** | **32** |
| **Mockups (`MK-xx`)** | **6** |
| **Referencias visuales (`RV-xx`)** | **8** |
| **Filas de la matriz de trazabilidad** | **195** |
| Consultas resueltas en esta consolidación (`C-xx`) | 19 |
| Pendientes de aclaración abiertos | 1 (PA-19, parcial) |

**Resultado del cruce de los 25 pendientes con la revisión (antes de las consultas):** aclaración explícita en 13 (PA-03, 06, 07, 08, 11, 12, 13, 16, 20, 21, 22, 24, 25); parcial en 8 (PA-01, 02, 04, 09, 10, 14, 15, 17); ambigua en 1 (PA-18); contradictoria en 2 (PA-05 con F2 §4 y PA-23 con F1); sin resolver en 1 (PA-19, remite a PA-14). Tras las consultas quedan 24 cerrados y 1 abierto (sección 10).

**Hallazgos de la v1 corregidos o reclasificados:** H-032 (contexto corregido), H-078 (de «pendiente de clasificación» a transversal), H-076 («obligatorio en bodega» reemplazado, C-05).

## 4. Hallazgos por módulo

Formato de cada hallazgo: módulo, tipo y estado; descripción y contexto de la v1; aclaraciones y observaciones posteriores; vínculos con diferencias (D), propuestas (PR) y referencias visuales (MK, RV); y fuentes. En **Fuente**, el detalle entre paréntesis de F1 es el «Origen» de la primera consolidación.

### 4.1. Báscula

#### H-001 – Registro de inspecciones: normalmente solo se pesa y los vehículos llegan sin documentos

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Consolidado con aclaración
- **Descripción:** En las inspecciones, por lo regular, solo se registra el peso. Los vehículos suelen llegar sin documentos (por ejemplo, los de Logitrans vienen solo a pesar y envían los documentos después). En el sistema anterior, para inspecciones se registraba únicamente placa, conductor, información necesaria, peso y mercancía, sin crear depósito, porque el documento indica entrega en el lugar de arribo en el puente. El sistema nuevo crea un depósito de inspección. El operario preguntó cómo distinguir un depósito de inspección de otro cuando no trae documento ni producto; en el sistema anterior escribe en la descripción de quién es la inspección. La cantidad le serviría para elaborar la tarjeta. En inspección se manejan tarjetas manuales.
- **Contexto (v1):** En la visita el desarrollador indicó que el depósito de inspección se crearía con documentos opcionales, descripción del producto opcional y un campo para describir la inspección; quedó por confirmar con facturación (Jennifer) si el depósito le sirve. El hallazgo aparece dos veces en el documento inicial (Báscula #1 y #17).
- **Aclaración (PA-01):** El depósito de inspección se sigue creando como está actualmente. Cambia la flexibilidad en báscula al registrar el ingreso: documentos y producto opcionales, y un campo de descripción obligatorio. Facturación cobra estos depósitos con un valor fijo por vehículo («se maneja igual que importación»). El usuario confirmó con los operarios que se maneja igual (C-14).
- **Vínculos:** D-01 · PR-07 · PR-20 · PR-01
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #1 y #17; `bascula.txt` › Inspaccion parte 1, Inspaccion 2 - Conclusion, Bascula) · F2 §1 PA-01, §4 Báscula · F4 C-14

#### H-002 – Cerrar el ciclo de báscula sin segundo pesaje o agregar un segundo pesaje

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado con aclaración
- **Descripción:** Cuando un vehículo se registra con ciclo de dos pesajes y finalmente no descarga, el registro queda en la fila y no aparece en el historial hasta cerrar el ciclo. El operario no encontró cómo cambiar el ciclo después de registrado. Se solicita poder cerrar el ciclo sin segundo pesaje o, en sentido contrario, agregarle un segundo pesaje.
- **Contexto (v1):** Ejemplo: un vehículo que llega con cebollas y no las descarga. El desarrollador indicó que agregaría una opción de cerrar el ciclo.
- **Relación con la revisión:** La propuesta del formulario de registro deja visible en el encabezado el switch «Requiere segundo pesaje» y quita el switch de perecederos (PR-01).
- **Vínculos:** PR-01 · H-084
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #2; `bascula.txt` › Bascula) · F2 §4 Báscula

#### H-003 – Columnas de la vista de báscula iguales a las de entradas del sistema anterior

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado con aclaración
- **Descripción:** En la interfaz de báscula (`/operations/weighbridge`) se requiere ver las mismas columnas que la vista de entradas del sistema anterior: fecha, hora, vehículo (placa), conductor e identificación, peso bruto, peso de la mercancía, tara del vehículo y cantidad. Lo más importante para el operario: peso bruto, peso de la mercancía y tara.
- **Contexto (v1):** En el sistema anterior esta información aparece igual en entradas, salidas y solo pesaje.
- **Relación con la revisión:** La propuesta del historial (PR-05) lleva esas columnas a las páginas de Entradas, Salidas y Solo báscula del historial. El hallazgo original se refería a `/operations/weighbridge`; la propuesta las ubica en el historial. Se documentan ambas sin resolver la diferencia.
- **Vínculos:** D-03 · PR-05 · H-026 · H-047
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #3; `bascula.txt` › Bascula) · F2 §4 Báscula (2)

#### H-004 – El listado abre el registro al hacer clic en cualquier parte de la fila

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado con aclaración
- **Descripción:** En el listado de báscula, al hacer clic en cualquier parte de la fila se abre el registro. Se solicita que se abra solo con el botón, porque los operarios necesitan copiar información de la tabla.
- **Relación con la revisión:** La propuesta general de listados establece que las acciones de una tabla se ejecutan solo con botones, no con clic en la fila (PR-29).
- **Vínculos:** PR-29
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #4; `bascula.txt` › Bascula) · F2 §4 Ajustes generales

#### H-005 – Imprimir ticket sin repesaje: solo tara, solo entrada y recibo

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** En el sistema anterior se puede imprimir el ticket sin hacer el repesaje: ticket de entrada con el peso bruto, ticket con la tara que el sistema toma automáticamente, y un recibo. En el sistema nuevo es necesario hacer el repesaje para imprimir. El recibo muestra la información y el valor del ticket; los conductores lo piden antes del repesaje para demostrar a los dueños del vehículo cuánto pagaron.
- **Contexto (v1):** Son de los tickets que más se usan. Relacionado con la tara de vehículos que no descargan (el ticket con tara se entrega a la DIAN).
- **Vínculos:** D-02 · H-008
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #5; `bascula.txt` › Bascula)

#### H-006 – El ticket de báscula no muestra producto, embalaje ni cantidad

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** En el ticket solo aparece la descripción del producto. Se solicita que aparezcan descripción, embalaje y cantidad (por ejemplo: arroz, sacos y cantidad), en los tickets de entrada y en los que salen al final.
- **Contexto (v1):** Se necesita para saber cuántas unidades se entregaron en bodega. En la conversación sobre órdenes de cargue también se pidió que el ticket muestre productos y cantidades.
- **Vínculos:** H-085
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #6; `bascula.txt` › Bascula, Ordenes de cargue)

#### H-007 – Orden de los tickets: del más reciente al más antiguo

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** Los tickets aparecen del más antiguo al más reciente. Se solicita lo contrario.
- **Vínculos:** PR-29 (orden por columnas)
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #8; `bascula.txt` › Bascula)

#### H-008 – Tara de vehículos que no descargan (oleína, contenedores)

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Consolidado con aclaración
- **Descripción:** En vehículos como los de oleína se desengancha el tanque y se pesa solo el cabezote; en contenedores, el vehículo llega con el contenedor, se pesa y el contenedor se baja. Al registrar la repesa, el peso de la mercancía resulta sobredimensionado. Cuando la DIAN pide el ticket, el operario entrega el ticket con la tara que toma el sistema, porque no se tiene el peso del tanque o del contenedor vacío. El operario indicó que en algunos casos (perecederos) ajusta pesos «desde su módulo» y que necesita que eso se pueda corregir.
- **Contexto (v1):** Cifras del audio: ingreso de unas 30 toneladas, repesa de 9.080, resultado de 37.480 y 27.480, vehículo de 16.560.
- **Aclaración (PA-02):** El peso de la tara no es correcto porque en el repesaje se pesa solo el cabezote y la mercancía queda cargada en el contenedor. Por eso el operario de comercio exterior entra al legacy en *Comercio Exterior › Tickets Ingreso › Editar › Modificar entrada a báscula* y edita la T. vehículo. En general, el operario de comercio exterior necesita poder editar cualquier peso registrado en báscula, como en el legacy. La relación entre las cifras del audio se cierra sin más información (C-16).
- **Observación de video:** OV-06 y OV-07 muestran la edición de pesos en el mismo formulario del legacy.
- **Vínculos:** D-12 · PR-11 · H-041 · RV-01
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #9; `bascula.txt` › Tara de vehiculo sin descargar, Bascula) · F2 §1 PA-02 · F3 Video 2 · F4 C-16

#### H-009 – Vehículo ingresado sin peso y editado posteriormente para agregar el peso

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Cerrado sin cambio
- **Descripción:** «El día de ayer ingresó un vehículo, el operario registra pero sin peso; posteriormente el operario edita e ingresa el peso».
- **Aclaración (PA-03):** Es una forma de trabajo. El vehículo ingresó el día anterior fuera del horario del operario; al día siguiente el operario hizo el ingreso sin registrar el peso porque el conductor no estaba, y lo registró cuando el conductor llegó. Se verificó que el sistema actual sí tiene esta funcionalidad; es un tema de capacitación.
- **Vínculos:** PR-03 (la propuesta «Guardar sin pesaje» toca el mismo caso)
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #10) · F2 §1 PA-03

#### H-010 – Eliminación de tickets

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** Se solicita poder eliminar tickets. En el sistema anterior se muestra la información del ticket, se pide la razón y el registro queda marcado en rojo. Motivos: el sistema a veces duplica tickets, y cuando varios vehículos llegan con la misma carta porte y el arrastre queda en otra carta porte, no se puede editar.
- **Vínculos:** D-04 · H-074
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #11; `bascula.txt` › Eliminación de ticket)

#### H-011 – Búsqueda de coincidencias de la carta porte al digitar

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Consolidado con aclaración
- **Descripción:** En el sistema anterior, al digitar la carta porte aparece un listado de coincidencias en el select; al seleccionar, se muestra el detalle del depósito y se agrega el número en el detalle. Se solicita el mismo comportamiento. Según el documento inicial, al repetir una carta porte solo se cargan los depósitos en estado borrador.
- **Contexto (v1):** Dudas del operario: cómo se verá con más de tres depósitos en borrador, coincidencias parciales con muchos resultados, y que las coincidencias muestran el número de depósito cuando él se guía por la carta porte. El desarrollador explicó en la visita que las coincidencias muestran solo depósitos en borrador.
- **Aclaración (PA-04):** Lo que necesita el operario es que, al empezar a digitar la carta porte, el selector vaya mostrando opciones para no digitar todo y elegir rápido. Después de seleccionar, el comportamiento es el actual: abajo se muestra el depósito y el número de carta porte aparece en el detalle.
- **Aclaración (C-17):** Sobre qué estados muestra hoy la v2, se cierra con el análisis de paridad: las coincidencias incluyen depósitos abiertos, en **borrador o confirmado**. Esto corrige lo dicho en la visita («solo borrador»); se conservan ambas versiones.
- **Vínculos:** D-05 · PR-27
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #12 y #22; `bascula.txt` › Cambios Interfaz) · F2 §1 PA-04 · F4 C-17 · Ref. (etapa 5, «Reutilizar el documento al pesar»)

#### H-012 – Edición de la fecha y hora de ingreso

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado con aclaración
- **Descripción:** El sistema no deja editar la fecha y la hora: la restablece. Se solicita poder editarla libremente y mover la edición de la fecha al encabezado.
- **Contexto (v1):** La fecha de ingreso del depósito se toma por defecto del ingreso en vigilancia.
- **Relación con la revisión:** La propuesta del formulario de registro quita el campo «Fecha de ingreso del depósito» porque ya se registra en la sección Vigilancia, que es editable desde el mismo formulario (PR-01). El operario pidió la fecha en el encabezado; la propuesta la deja en la sección Vigilancia. Se documentan ambas sin resolver la diferencia.
- **Vínculos:** PR-01 · H-028
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #13 y #14; `bascula.txt` › Bascula) · F2 §4 Báscula

#### H-013 – Búsqueda de la empresa de transporte por número de documento

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** Se solicita que la empresa de transporte se pueda buscar por número de documento.
- **Contexto (v1):** El fragmento de la transcripción es poco legible.
- **Vínculos:** PR-27 (selectores con buscador)
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #15; `bascula.txt` › Inspaccion parte 1)

#### H-014 – Conductores distintos con el mismo número de documento

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** En los documentos a veces vienen cédulas repetidas con nombres diferentes. El sistema valida número de documento y país y no permite crear otro conductor con el mismo número. En el sistema anterior se agregaba un punto al final del número para diferenciarlo.
- **Contexto (v1):** El desarrollador indicó que quitaría la validación. No aparece en el documento inicial.
- **Vínculos:** D-06
- **Fuente:** F1 (`bascula.txt` › Inspaccion parte 1)

#### H-015 – Manifiesto obligatorio solo cuando el documento es carta porte

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** El número de manifiesto es obligatorio para cualquier documento comercial. Solo debería serlo con carta porte, porque con factura comercial o remisión solo traen ese documento.
- **Contexto (v1):** Se mencionó en el registro de exportación.
- **Vínculos:** PR-01 (subsección Modalidad: tipo de documento, número y manifiesto en una fila)
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #18; `bascula.txt` › Exportacion)

#### H-016 – Carta porte seleccionada por defecto como documento comercial

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** Se solicita que el documento comercial venga seleccionado por defecto como carta porte.
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #19; `bascula.txt` › Exportacion)

#### H-017 – Salida de mercancía: traer la placa de vigilancia y precargar la orden de cargue

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado con aclaración
- **Descripción:** Para la salida, se solicita que la placa ingresada en vigilancia se cargue en báscula y que con ella se precargue la orden de cargue. El conductor de la orden puede cambiar, por lo que debe poder modificarse en báscula.
- **Contexto (v1):** Comercio exterior crea la orden amarrada a una placa; en báscula se busca por número de orden o por placa. Cambiar el conductor en báscula no modifica la orden; la guía toma los datos de la orden. El desarrollador mencionó una alerta a comercio exterior cuando se cambie el conductor.
- **Relación con la revisión:** Para «Salida de mercancía» se conservan las secciones actuales del formulario con los ajustes de los hallazgos (PR-01). El flujo de salida y la orden de cargue se replantean en PR-21.
- **Vínculos:** PR-01 · PR-21 · H-072
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #20; `bascula.txt` › Salida Mcia) · F2 §4 Báscula

#### H-018 – Unidad no editable al agregar un producto

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Consolidado con aclaración
- **Descripción:** Al agregar un producto existente, el sistema trae la unidad (por ejemplo, kilogramos) y la cantidad, y no permite editar la unidad. Se solicita poder editarla.
- **Contexto (v1):** Se preguntó quién necesita la unidad; se mencionó facturación sin confirmarlo. El arroz se ingresa solo como «Arroz» (en sacos).
- **Aclaración (PA-05 y C-04):** «Sí se utiliza en facturación y comercio exterior». El usuario precisó que se refiere al **embalaje**. Para la **unidad de medida**, la revisión propone eliminarla de los productos y de toda la app porque no se usa (PR-12).
- **Vínculos:** PR-12 · PR-01 · H-033
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #23; `bascula.txt` › Cambios Interfaz) · F2 §1 PA-05, §4 Báscula · F4 C-04

#### H-019 – Paso 2 del registro: mostrar y editar toda la información del paso 1

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado con aclaración
- **Descripción:** En el paso 2 del registro se solicita que el detalle del paso 1 muestre toda la información y que se pueda editar.
- **Relación con la revisión:** La propuesta reorganiza el flujo en tres pasos (Registro, Cobro, Tiquete) en una página, con la sección Vigilancia editable (PR-01).
- **Vínculos:** PR-01
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #24) · F2 §4 Báscula

#### H-020 – Conductor en el paso de cobro

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** Cuando se cambia el conductor en el paso 1, el paso 2 (cobro) no se actualiza. Se solicita en el cobro el select de conductores, preseleccionado con el del paso 1.
- **Relación con la revisión:** En la propuesta, los pasos de cobro y tiquete conservan la distribución y funcionalidad actual con los ajustes de los hallazgos (PR-01).
- **Vínculos:** PR-01
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #25 y #26)

#### H-021 – Camiones con más de una mercancía (pesos intermedios)

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** En el sistema anterior, por cada depósito adicional del mismo camión se ingresaba un nuevo registro. En el nuevo se piden los documentos entre un pesaje y otro. Se solicita llenar toda la documentación al inicio y, después de cada descargue, solo repesar. El operario preguntó a qué producto queda asignado el peso bruto.
- **Contexto (v1):** El desarrollador explicó que el peso bruto queda asignado a todo el camión y que en cada peso intermedio se escoge el producto que se pesa.
- **Vínculos:** D-07 · H-024 · H-073
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #27; `bascula.txt` › Multideposito (Importante))

#### H-022 – Historial único frente a vistas separadas de entradas y salidas

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios + Propuesta · **Estado:** Consolidado con aclaración
- **Descripción:** El sistema anterior tiene vistas separadas de entradas, salidas y solo pesaje. En el nuevo, el historial muestra todo junto. El operario comparó el historial con el reporte que usan.
- **Contexto (v1):** La respuesta final del operario quedó cortada en la transcripción.
- **Respuesta de la revisión (PA-06):** Clasificada como propuesta (C-02): rediseñar en vistas separadas, con tres submenús bajo Historial (Entradas, Salidas y Solo pesaje), filtros por columna en lugar del panel de filtros, y sin las cards de resumen. La opinión del operario sigue sin registrarse.
- **Vínculos:** D-08 · PR-05
- **Fuente:** F1 (`bascula.txt` › Multideposito (Importante)) · F2 §1 PA-06, §4 Báscula (2)

#### H-023 – Impresión del ticket mediante descarga

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Cerrado sin cambio
- **Descripción:** El ticket se descarga para imprimirlo en lugar de imprimirse directamente. El operario comentó revisar la configuración de la impresora y que el formato quede cuadrado en la hoja.
- **Contexto (v1):** Frase no clara: «La opción de guardar sí sería buena, pero en blanco».
- **Aclaración (PA-07):** La impresión y la descarga funcionaron correctamente y el operario no reportó inconvenientes. La observación sobre el espacio sobrante del ticket se registra aparte (H-085).
- **Vínculos:** H-085 · PR-32
- **Fuente:** F1 (`bascula.txt` › Multideposito (Importante)) · F2 §1 PA-07

#### H-084 – Edición de la información de báscula después de terminar el ciclo (nuevo)

- **Módulo:** Báscula · **Tipo:** Hallazgo reportado por operarios (registrado en la revisión) · **Estado:** Consolidado
- **Descripción:** El operario solicita poder editar la información incluso después de terminar el ciclo. En el legacy, en entradas, salidas y solo pesaje, el operario puede seguir editando; se pide lo mismo para la v2.
- **Vínculos:** D-10 · PR-01 · PR-05 (la edición abre otra vez el formulario de registro) · PR-11 · H-074 · H-002
- **Fuente:** F2 §4 Báscula (1)

#### H-085 – Espacio vertical sobrante en el ticket impreso (nuevo)

- **Módulo:** Báscula · **Tipo:** Observación de revisión · **Estado:** Documentado
- **Descripción:** En el ticket impreso sobra mucho papel verticalmente; se podría optimizar el espacio.
- **Vínculos:** PR-32 · H-023 · H-006
- **Fuente:** F2 §1 PA-07

### 4.2. Bodega

#### H-024 – Ingreso duplicado en bodega cuando el camión trae más de un producto

- **Módulo:** Bodega · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** Cuando un camión trae más de un producto, en bodega aparecen dos ingresos del mismo camión. Debería ser un solo ingreso y que el operario escoja el producto que descarga.
- **Contexto (v1):** Observado durante la prueba de pesos intermedios.
- **Vínculos:** H-021 · H-073
- **Fuente:** F1 (`Hallazgos.docx` › Bodegas #1; `bascula.txt` › Multideposito (Importante))

#### H-025 – Selección de la cuadrilla de bodega al ejecutar el cargue

- **Módulo:** Bodega · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** Al ejecutar el cargue (cantidad, cuadrilla, observaciones, firma, fotos), el operario preguntó si es posible indicar qué cuadrilla cargó.
- **Contexto (v1):** Las cuadrillas se administran en el sistema y el campo es opcional.
- **Relación con la revisión:** Las cuadrillas pasan a la sección propuesta «Configuración» (PR-28).
- **Vínculos:** PR-28
- **Fuente:** F1 (`bascula.txt` › Ordenes de cargue) · F2 §4 Ajustes generales

### 4.3. Comercio Exterior

#### H-026 – Vistas de entradas, salidas y solo pesaje con las columnas de báscula del sistema anterior

- **Módulo:** Comercio Exterior · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado con aclaración
- **Descripción:** Se solicita en comercio exterior la vista de entradas, salidas y solo pesaje con las mismas columnas del sistema anterior (peso bruto, tara, entre otras). El operario revisa los pesos de los vehículos y los clientes le piden a él los tickets.
- **Contexto (v1):** Lo que hoy muestra báscula para esta consulta no le sirve.
- **Relación con la revisión:** La revisión propone el ítem de menú «Tickets de ingreso» con las columnas de la tabla de entradas del depósito, más el número de depósito como enlace y la acción de editar (PR-18). OV-06 muestra la lista «Tickets Ingresos» del legacy.
- **Vínculos:** D-03 · D-13 · PR-18 · PR-05 · OV-06
- **Fuente:** F1 (`Hallazgos.docx` › Comercio Exterior #1; `Comercio exterior.txt` › Cambio tablas) · F2 §4 Comercio Exterior · F3 Video 2

#### H-027 – Información del depósito: tarjetas frente a tabla del sistema anterior

- **Módulo:** Comercio Exterior · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado con aclaración
- **Descripción:** En `/foreign-trade/deposits` la información se muestra en tarjetas y no aparece toda; para ver la cantidad hay que abrir el depósito. En el sistema anterior la tabla muestra fecha de ingreso, depósito, carta porte, importador, transportadora, manifiesto, producto, placa, cantidad, peso y número de etiqueta. El operario prefería una tabla.
- **Contexto (v1):** El desarrollador propuso un panel lateral (drawer) con toda la información al hacer clic en cada tarjeta y los operarios respondieron que sí.
- **Relación con la revisión:** La revisión propone otra solución: ocultar `/foreign-trade/deposits`, separar los depósitos por tipo en el menú y usar una tabla con fila expandible (maestro-detalle) más una página de detalle por etapas (PR-15, PR-16, PR-17). Se documentan el drawer aceptado en la visita y la propuesta de la revisión sin resolver la diferencia.
- **Vínculos:** D-14 · PR-15 · PR-16 · PR-17 · MK-02 · MK-03
- **Fuente:** F1 (`Hallazgos.docx` › Comercio Exterior #2; `Comercio exterior.txt` › Tarjetas de deposito) · F2 §4 Comercio Exterior

#### H-028 – Edición de la fecha de llegada de la mercancía y del manifiesto

- **Módulo:** Comercio Exterior · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado con aclaración
- **Descripción:** Se solicita poder editar la fecha de llegada de la mercancía (no la fecha de creación del depósito) y el manifiesto, que agrega el operario.
- **Relación con la revisión y videos:** OV-09 muestra que en el legacy la fecha y hora, el número y las observaciones del depósito se editan en cualquier momento. La etapa «Datos principales» propuesta incluye fecha y hora, número de manifiesto y fecha del manifiesto DIAN (PR-17).
- **Vínculos:** D-15 · PR-17 · OV-09 · H-012 · H-074
- **Fuente:** F1 (`Hallazgos.docx` › Comercio Exterior #3; `Comercio exterior.txt` › Productos) · F2 §4 Comercio Exterior · F3 Video 2

#### H-029 – Creación rápida de terceros, clientes, importadores y agencias desde el depósito

- **Módulo:** Comercio Exterior · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** Se solicita editar y agregar importadores, agencias de aduanas y clientes desde el detalle del depósito, también después de confirmarlo, con botones rápidos de creación. Hoy en borrador se pueden asignar, pero no crear.
- **Contexto (v1):** Normalmente la creación la hace otra persona (Vanessa); el usuario ya tiene la opción en la sección de terceros.
- **Relación con la revisión:** La gestión de terceros pasa a la sección propuesta «Configuración», con acceso de Comercio Exterior (PR-28). La etapa «Datos principales» incluye los terceros relacionados (PR-17).
- **Vínculos:** PR-17 · PR-28
- **Fuente:** F1 (`Hallazgos.docx` › Comercio Exterior #5; `Comercio exterior.txt` › Productos) · F2 §4

#### H-030 – Edición de la sección de transporte

- **Módulo:** Comercio Exterior · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** Se solicita poder editar toda la información de la sección de transporte del depósito.
- **Vínculos:** PR-17 (Datos principales: empresas de transporte)
- **Fuente:** F1 (`Hallazgos.docx` › Comercio Exterior #6; `Comercio exterior.txt` › Productos)

#### H-031 – Edición de productos después de confirmar el depósito

- **Módulo:** Comercio Exterior · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado con aclaración
- **Descripción:** Una vez confirmado el depósito no se pueden cambiar los productos; solo en borrador. Se solicita poder editar, agregar o quitar productos después de confirmar, mientras la mercancía no haya salido.
- **Contexto (v1):** En el sistema anterior sí se podía; cuando la mercancía ya salió, no permite agregar ni quitar.
- **Relación con la revisión y videos:** La etapa «Amparados» propuesta permite ingresar la cantidad amparada de cada producto, y quitar, agregar o editar productos (PR-17). OV-10 muestra que en el legacy los productos amparados se registran aparte.
- **Vínculos:** D-16 · PR-17 · OV-10
- **Fuente:** F1 (`Hallazgos.docx` › Comercio Exterior #7; `Comercio exterior.txt` › Productos) · F2 §4 · F3 Video 2

#### H-032 – Crear productos desde el modal de agregar productos

- **Módulo:** Comercio Exterior · **Tipo:** Hallazgo reportado por operarios · **Estado:** Corregido
- **Descripción:** Siguen llegando productos nuevos y en el modal de agregar productos (ni en borrador) no hay opción para crear uno. Se solicita poder crearlo desde ese modal.
- **Contexto (v1):** «Se mencionó que en bodega sí se puede crear». En la transcripción lo dice el desarrollador durante la sesión.
- **Corrección (F2 §2):** Lo mencionado en el contexto no es correcto: la creación de productos no se realiza en bodega. Se conservan la cita original y la corrección.
- **Vínculos:** PR-28 (Productos en «Configuración») · H-033
- **Fuente:** F1 (`Hallazgos.docx` › Comercio Exterior #8; `Comercio exterior.txt` › Productos) · F2 §2 Comercio Exterior

#### H-033 – Mostrar el embalaje junto al nombre del producto

- **Módulo:** Comercio Exterior · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado con aclaración
- **Descripción:** En el modal de agregar productos aparece solo el nombre y hay varias referencias con el mismo nombre; los operarios tuvieron que adivinar cuáles eran cajas y cuáles bultos. Se solicita mostrar las características junto al nombre: embalaje y unidad.
- **Contexto (v1):** Flores en cajas o envueltas; piña en banastas o cajas; coco rallado en sacos o bultos.
- **Relación con las aclaraciones:** El dato que usan Facturación y Comercio Exterior es el embalaje (C-04); la revisión propone quitar la unidad de medida de toda la app (PR-12).
- **Vínculos:** PR-12 · H-018
- **Fuente:** F1 (`Hallazgos.docx` › Comercio Exterior #9; `Comercio exterior.txt` › Productos) · F4 C-04

#### H-034 – Tasa de cambio ingresada manualmente y visible en los levantes

- **Módulo:** Comercio Exterior · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Consolidado con aclaración
- **Descripción:** La declaración anticipada usa la tasa de cambio anterior; si el sistema toma la actual, el valor queda mal. La tasa la ingresan semanalmente (cada lunes) en la configuración del sistema anterior. Se solicita dejarla manual y que se muestre en los levantes, con posibilidad de cambiarla.
- **Contexto (v1):** El operario prefirió que quede manual. Hay levantes hechos una o dos semanas antes y mercancía del año anterior («toca ir actualizando para cada salida»).
- **Aclaración (PA-08):** El operario configura cada lunes la tasa de la semana. Al registrar el levante se precarga la tasa configurada para esa semana, pero hay levantes de depósitos de semanas anteriores; en ese caso el operario cambia la tasa a la que correspondía.
- **Aclaración (C-15):** Es una sola tasa semanal, compartida por Comercio Exterior y Facturación.
- **Observación de video:** OV-02.
- **Vínculos:** D-22 · PR-23 · H-077 · OV-02
- **Fuente:** F1 (`Hallazgos.docx` › Comercio Exterior #10 y #11; `Comercio exterior.txt` › Levante 1, Levantes 2) · F2 §1 PA-08 · F3 Video 1 · F4 C-15

#### H-035 – Prefijos para números de levante, aceptación y manifiesto

- **Módulo:** Comercio Exterior · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** Hay que digitar números largos (por ejemplo, «37 2026…») y los operarios se equivocan. Se solicita configurar prefijos, como en el sistema anterior, para los formularios de levante, aceptación y manifiesto DIAN, editables por los operarios.
- **Contexto (v1):** El motivo es principalmente el tiempo.
- **Vínculos:** D-17
- **Fuente:** F1 (`Hallazgos.docx` › Comercio Exterior #12; `Comercio exterior.txt` › Levante 1)

#### H-036 – Interfaz de levantes similar al sistema anterior

- **Módulo:** Comercio Exterior · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Consolidado con aclaración
- **Descripción:** Se solicita que la interfaz de los levantes sea similar a la del sistema anterior: allí los productos aparecen en columnas; en el nuevo se escoge el producto. El operario quiere «el cuadrito… no tan para abajo».
- **Aclaración (PA-09):** «El cuadrito… no tan para abajo» se refiere al modal de confirmación del levante: que no genere scroll vertical. Con varios productos, el legacy muestra una columna por producto y el operario ponía en cero la cantidad del producto que no levantaba. La alternativa es el select de producto de la v2. El operario está dispuesto a cambiar al select, pero la opción legacy da en una sola vista la percepción de todos los productos y sus cantidades.
- **Aclaración (C-06):** La propuesta de diseño es la del mockup de levantes (tabla agrupada por mercancía con fila editable, PR-19). Las dos opciones de PA-09 quedan como contexto.
- **Observación de video:** OV-04.
- **Vínculos:** D-18 · PR-19 · OV-04 · RV-02 · MK-04 · MK-05 · MK-06
- **Fuente:** F1 (`Hallazgos.docx` › Comercio Exterior #13; `Comercio exterior.txt` › Levantes calculos) · F2 §1 PA-09, §4 Levantes · F3 Video 1 · F4 C-06

#### H-037 – Valor CIF / valor en aduanas obligatorio en levantes

- **Módulo:** Comercio Exterior · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Consolidado con aclaración
- **Descripción:** En el levante, el campo de valor CIF aparece como opcional, pero el operario indicó que es obligatorio. La etiqueta debería decir «Valor en aduanas».
- **Contexto (v1):** El desarrollador comentó que internamente se guarda como FOB; el operario señaló que FOB es un incoterm.
- **Aclaración (PA-10):** «Valor CIF» y «valor en aduanas» son el mismo dato. El operario sugiere la etiqueta «Valor en aduanas»: en el legacy aparece como CIF, pero los documentos oficiales usan «valor en aduanas».
- **Observación de video (OV-11):** En el legacy el formulario pide «CIF USD» y calcula «FOB CO» = CIF USD × tasa.
- **Nota:** El mockup de levantes (MK-04, MK-05) rotula la columna «CIF (USD)».
- **Vínculos:** OV-11 · PR-19 · MK-04
- **Fuente:** F1 (`Hallazgos.docx` › Comercio Exterior #14; `Comercio exterior.txt` › Levantes 2) · F2 §1 PA-10 · F3 Video 1

#### H-038 – Datos de aceptación en levantes

- **Módulo:** Comercio Exterior · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Consolidado con aclaración
- **Descripción:** El documento inicial indica quitar la fecha de aceptación. En la transcripción: «el número de aceptación, la fecha de aceptación no la necesito, solo la fecha de levante».
- **Aclaración (PA-11):** El operario solicitó quitar la fecha de aceptación; solo se pide la fecha del levante. Se conserva el formulario legacy, que solo pide esa fecha. El formulario legacy (RV-02) y el video (OV-03) muestran que sí se conserva el número de aceptación, coherente con el pedido de prefijos de H-035.
- **Vínculos:** D-20 · OV-03 · RV-02 · H-035
- **Fuente:** F1 (`Hallazgos.docx` › Comercio Exterior #15; `Comercio exterior.txt` › Levantes calcular cantidades automaticamente, Levante 1) · F2 §1 PA-11 · F3 Video 1

#### H-039 – Cálculo automático de la cantidad al hacer el levante

- **Módulo:** Comercio Exterior · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Consolidado con aclaración
- **Descripción:** En el sistema anterior, al hacer el levante se calcula la cantidad a partir del peso. En el nuevo no se calcula, lo que genera inconvenientes cuando hay varias declaraciones.
- **Contexto (v1):** El desarrollador dio posibles motivos (descargue pendiente en bodega, peso documental insuficiente); las transcripciones tenían afirmaciones contradictorias.
- **Aclaración (PA-12):** El sistema actual no calcula automáticamente las cantidades. El operario enfatiza la importancia de que lo haga; el comportamiento debe ser igual al legacy (video RV-07).
- **Observación de video:** OV-01.
- **Vínculos:** D-19 · OV-01 · RV-07 · H-040
- **Fuente:** F1 (`Hallazgos.docx` › Comercio Exterior #16; `Comercio exterior.txt` › Levantes calcular cantidades automaticamente, Levantes calculos) · F2 §1 PA-12 · F3 Video 1

#### H-040 – Levantes sucesivos mostrando pesos y cantidades restantes hasta quedar en cero

- **Módulo:** Comercio Exterior · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado con aclaración
- **Descripción:** Se agrega un levante e inmediatamente otro, mostrando los pesos y cantidades restantes hasta llegar a cero. En el legacy los productos aparecen en columnas y se pone cero en el peso que no corresponde; el depósito se va separando por producto. Al guardar se genera ahí mismo otra declaración; en el nuevo hay que guardar y volver a abrir.
- **Contexto (v1):** Lo más importante son los pesos; al final no debe sobrar peso.
- **Relación con la revisión:** La tabla agrupada del mockup muestra por mercancía el ingreso, cada levante, el nacionalizado y el saldo, con una fila para agregar el siguiente levante y aviso de diferencia de peso (PR-19).
- **Vínculos:** D-21 · PR-19 · OV-01 · OV-04 · H-036 · H-039
- **Fuente:** F1 (`Hallazgos.docx` › Comercio Exterior #17; `Comercio exterior.txt` › Levantes varios productos, Levantes calculos, Levantes calcular cantidades automaticamente) · F2 §4 Levantes

#### H-041 – Edición de pesos y tabla de tickets de ingreso en comercio exterior

- **Módulo:** Comercio Exterior · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Consolidado con aclaración
- **Descripción:** Se solicita dejar en comercio exterior la tabla de tickets de ingreso y la sección de pesajes para editar todos los pesos, como en el sistema anterior. Báscula registra el peso del manifiesto; la mercancía pasa revisión del ICA; se pesan bultos de muestra y se calcula el peso que se usa para la planilla DIAN. El operario edita el peso del manifiesto y a veces el del indicador para que cuadre; ese peso aparece en el depósito y en el levante.
- **Contexto (v1):** El peso calculado no siempre coincide con el neto. Marcado «Importante» en el audio.
- **Aclaración (PA-13):** Comercio exterior puede editar cualquier peso, para hacer coincidir la tara o el peso de la mercancía con los documentos (video RV-08).
- **Observación de video:** OV-06, OV-07 y OV-08: la operaria cambia indicador, manifiesto y mercancía en un solo formulario para cuadrar con la planilla de recepción DIAN; la T. vehículo se recalcula (indicador − mercancía) y el cambio se ve en el depósito y en el levante.
- **Vínculos:** D-12 · D-13 · PR-11 · PR-18 · OV-06 · OV-07 · OV-08 · RV-01 · RV-08 · H-008
- **Fuente:** F1 (`Hallazgos.docx` › Comercio Exterior #18; `Comercio exterior.txt` › Edicion y calculo de pesos (Importante), Levantes 2, cuadrar pesos) · F2 §1 PA-13 · F3 Video 2

#### H-042 – Modalidades de salida: por tiquete de entrada, por número de depósito y global

- **Módulo:** Comercio Exterior · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Consolidado con aclaración
- **Descripción:** Según el documento inicial, en salidas se usan «Usando tiquete de entrada», «Usando Nro. de depósito» y «Salida global»; solo en la de depósito se cobra báscula. Las salidas por tiquete y globales corresponden a vehículos que ingresan y no descargan: la mercancía se nacionaliza y se genera la guía mientras el camión permanece; al generarse la guía, el camión sale sin pasar por báscula.
- **Contexto (v1):** En el legacy, para salidas, se usaba el mismo tiquete varias veces («usar tiquete»), registrando productos en cada duplicado; en la v2 la salida se hace con la orden de cargue.
- **Aclaración (PA-14):** (1) **Por tiquete de entrada y global:** el camión ingresa cargado, se pesa y registra, no descarga y permanece en la bodega durante el levante; cuando está listo, la salida se genera con el tiquete de ingreso, sin pasar por báscula. La diferencia entre «por tiquete de entrada» y «global» es el firmante de la guía. En el video RV-07, un depósito con dos ingresos (dos camiones) lista los dos tickets de entrada y el operario selecciona ambos. (2) **Por número de depósito:** es la que soporta hoy la orden de cargue de la v2, pero el flujo es rígido: la orden debe existir antes de pasar por báscula y muchas veces el camión llega sin orden; solo en el cargue se sabe qué y cuánto carga. En el legacy la guía se genera directamente; en la v2 se genera desde la orden de cargue. Hay que tener en cuenta cómo el legacy muestra cantidades y saldos al generar la guía.
- **Aclaración (C-08):** Ver H-072.
- **Observación de video:** OV-05 (una guía con los dos tiquetes y las dos placas, sin orden de cargue ni báscula; firmante: importador).
- **Pendiente para la fase 2:** evaluar si en todos los escenarios sigue siendo útil generar primero la orden y luego la guía (sección 12).
- **Vínculos:** D-23 · PR-21 · PR-22 · OV-05 · RV-07 · H-072 · H-055
- **Fuente:** F1 (`Hallazgos.docx` › Comercio Exterior #19 y #20; `bascula.txt` › Ordenes de cargue) · F2 §1 PA-14 · F3 Video 1 · F4 C-08

#### H-043 – Registro de levantes e inventario de mercancía nacionalizada

- **Módulo:** Comercio Exterior · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Consolidado con aclaración
- **Descripción:** El inventario de mercancía nacionalizada se lleva a mano y el levante se coloca a mano en la tarjeta. Se necesita registrar el levante, que la mercancía aparezca como nacionalizada en el inventario y en la tarjeta, y poder sacar del sistema el inventario que pide la DIAN (por ejemplo, desde enero de 2025).
- **Contexto (v1):** En la v2, al registrar cualquier levante la mercancía aparece como nacionalizada en la etiqueta. «Amparado» = total de la carta porte; «saldo» = lo que queda en bodega.
- **Aclaración (PA-15):** El reporte que se solicita es un inventario de mercancía nacionalizada que muestre los levantes, con filtro por fecha. El estado del depósito y la etiqueta se mantienen como están en la v2: se marca como nacionalizado al registrar al menos un levante. El formato del reporte pasa a la fase 2 (C-18).
- **Vínculos:** sección 12
- **Fuente:** F1 (`Comercio exterior.txt` › Levante inventario) · F2 §1 PA-15 · F4 C-18

#### H-044 – Pruebas detenidas en levantes con varias declaraciones

- **Módulo:** Comercio Exterior · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** El operario quería probar todo el proceso hasta la salida, pero quedó detenido en el levante de un depósito con varias declaraciones. En facturación se indicó que nunca se ha llegado a una guía de salida en las pruebas.
- **Contexto (v1):** El desarrollador sugirió un levante sencillo para continuar las pruebas.
- **Vínculos:** H-039 · H-040
- **Fuente:** F1 (`Comercio exterior.txt` › Guias de salida; `facturacion.txt` › Facturacion almacenamiento)

#### H-045 – Lentitud de los selectores en la creación de la orden de cargue

- **Módulo:** Comercio Exterior · **Tipo:** Hallazgo reportado por operarios + Observación de revisión · **Estado:** Consolidado con aclaración
- **Descripción (v1):** Durante la demostración de creación de órdenes de cargue, la selección del vehículo fue lenta. El desarrollador lo comentó en dos sesiones («tengo que revisarlo»).
- **Observación de revisión (F2 §2):** En la vista de crear orden de cargue son demasiado lentos los selectores de vehículos, conductor y ciudad: las consultas traen todos los resultados (más de 1.000 registros). En la bodega el internet y los equipos no están actualizados, lo que dificulta el flujo.
- **Vínculos:** PR-27 (regla general de selectores) · PR-22 (rediseño de la vista)
- **Fuente:** F1 (`Comercio exterior.txt` › Guias de salida; `facturacion.txt` › Facturacion almacenamiento) · F2 §2 Comercio Exterior

### 4.4. Facturación

#### H-046 – Editar el número SIGO

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** Una vez asignado el número SIGO a una factura no se puede editar. Se solicita poder editarlo, porque a veces se digita mal.
- **Fuente:** F1 (`Hallazgos.docx` › Facturación #1; `facturacion.txt` › Facturacion Bascula)

#### H-047 – Información de báscula en las facturas (detalle y columnas)

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** En el detalle de las facturas de báscula no aparece la información necesaria. Se solicita mostrar número de ticket, modalidad y placa, y que la tabla de facturas de báscula en `/billing/invoices` tenga las columnas de entradas del sistema anterior (`bodegas/entrada.php`): ticket, fecha y hora, modalidad, vehículo, conductor, pesos y valor. Todo es importante excepto dos columnas que el operario señaló en pantalla.
- **Contexto (v1):** Los clientes piden la factura por placa y fecha de ingreso, o por número de ticket.
- **Vínculos:** D-03 · H-003 · H-026 · PR-29
- **Fuente:** F1 (`Hallazgos.docx` › Facturación #2 y #3; `facturacion.txt` › Facturacion Bascula)

#### H-048 – Filtros de búsqueda en facturas

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** Se solicita ampliar los filtros de `/billing/invoices` para buscar por carta porte, placa, tipo de servicio, ticket, conductor, fecha, número de factura, número SIGO, número de depósito y cliente. Hoy se busca principalmente por NIT.
- **Contexto (v1):** El sistema anterior tiene la vista de facturas emitidas con búsqueda por carta porte, factura, depósito, número SIGO y cliente.
- **Vínculos:** D-24 · PR-29 (filtros por columna)
- **Fuente:** F1 (`Hallazgos.docx` › Facturación #13; `facturacion.txt` › Facturacion Bascula, Facturacion almacenamiento y pagos)

#### H-049 – Reportes de facturación en PDF con suma al final

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** Los reportes solo se exportan en Excel. Se solicita imprimirlos en PDF, para todos los servicios (el operario escoge el servicio), con la suma al final y con las columnas del sistema anterior.
- **Vínculos:** H-050 · H-052
- **Fuente:** F1 (`Hallazgos.docx` › Facturación #4; `facturacion.txt` › Facturacion Bascula)

#### H-050 – Separar lo pagado de contado y lo que queda por cobrar

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** En la exportación (PDF o Excel) se solicita separar lo que está por cobrar (crédito) de lo pagado (contado), con suma independiente de cada uno.
- **Contexto (v1):** Lo pagado en efectivo en báscula es lo que se debe entregar.
- **Vínculos:** H-049 · H-052
- **Fuente:** F1 (`Hallazgos.docx` › Facturación #5; `facturacion.txt` › Facturacion Bascula)

#### H-051 – Montacargas: identificar qué servicios requieren factura

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios + Propuesta · **Estado:** Consolidado con aclaración
- **Descripción:** En montacargas, lo que se paga directamente al operario va sin IVA y no se factura; cuando el cliente pide factura electrónica va con IVA, queda a crédito y se le asigna número SIGO. El documento inicial registra dos solicitudes: una columna «IVA Sí/No» y preguntar al registrar si requiere factura.
- **Contexto (v1):** El operario de facturación prefiere «con factura / sin factura» en lugar de «con IVA / sin IVA». Hoy el operario de montacargas marca en el reporte físico cuáles se facturan.
- **Respuesta de la revisión (PA-16):** Clasificada como propuesta (C-02), coherente con la preferencia del operario: ver PR-24. La columna «IVA Sí/No» se da por reemplazada por el switch y los estados de PR-24 (C-16).
- **Vínculos:** PR-24 · H-052
- **Fuente:** F1 (`Hallazgos.docx` › Facturación #6 y #7; `facturacion.txt` › Facturacion montacargas) · F2 §1 PA-16 · F4 C-16

#### H-052 – Reporte de montacargas en reemplazo de los reportes físicos

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Consolidado con aclaración
- **Descripción:** El operario de montacargas usa reportes físicos numerados, los suma y entrega el dinero. Si deja de usarlos, facturación necesita un reporte del sistema para saber cuánto dinero se recibe, filtrable por días o rangos de fechas.
- **Aclaración (PA-17):** Lo genera el operario de facturación, con el mismo formato solicitado para báscula y guías de salida, separando en dos columnas lo que se factura y lo que no (pago inmediato). La numeración del reporte se cierra sin más información (C-16).
- **Vínculos:** H-049 · H-050 · H-051 · PR-24
- **Fuente:** F1 (`facturacion.txt` › Facturacion montacargas) · F2 §1 PA-17 · F4 C-16

#### H-053 – Registro del horómetro de montacargas

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Cerrado sin cambio
- **Descripción:** Al iniciar y finalizar el uso del montacargas se registra el horómetro inicial y final en horas. Hubo confusión sobre cómo registrar fracciones.
- **Contexto (v1):** Se registra lo que marca el horómetro y el sistema calcula las horas. El registro lo hacen en bodega.
- **Aclaración (PA-18 y C-12):** El funcionamiento actual es correcto y el input ya acepta decimales.
- **Fuente:** F1 (`facturacion.txt` › Facturacion montacargas) · F2 §1 PA-18 · F4 C-12

#### H-054 – Destinatario de las guías de salida sin la opción «cliente»

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** En el cobro de la guía se solicita quitar la opción de destinatario «clientes», porque se confunden, y dejar tercero registrado, conductor del vehículo y consumidor final.
- **Vínculos:** H-069
- **Fuente:** F1 (`Hallazgos.docx` › Facturación #8; `facturacion.txt` › Facturacion almacenamiento)

#### H-055 – Información y búsqueda en las facturas de guías de salida

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios · **Estado:** Pendiente de aclaración (parcial)
- **Descripción:** Se solicita agregar en las guías el número de guía, el depósito, la placa y el ticket (orden de cargue), y filtrar por ellos y por CPI. Hoy el operario busca la placa en el reporte de báscula y luego en el de guías. El reporte de guías del sistema anterior muestra fecha y hora, guía, depósito, placa, mercancía, embalaje, cantidad y CPI.
- **Contexto (v1):** En la v2 el equivalente al ticket es el número de orden de cargue. Se discutió si facturación necesita mercancía y embalaje.
- **Aclaración (PA-19):** «Esto se define con las decisiones tomadas en el punto PA-14». PA-14 no fija el dato, por lo que la relación ticket / orden de cargue pasa a la fase 2 junto con las modalidades de salida. **Sigue pendiente** si deben aparecer mercancía y embalaje (C-16).
- **Vínculos:** D-25 · H-042 · PR-21 · sección 10
- **Fuente:** F1 (`Hallazgos.docx` › Facturación #9; `facturacion.txt` › Facturacion almacenamiento) · F2 §1 PA-19 · F4 C-16

#### H-056 – Ciclo de facturación abierto en la configuración del cliente

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** El ciclo solo permite semanal, quincenal o mensual. Hay convenios con otros plazos (20 días, 120 días). Se solicita dejar el ciclo abierto en días.
- **Contexto (v1):** El sistema anterior tampoco permitía configurarlos.
- **Vínculos:** PR-25 · H-070
- **Fuente:** F1 (`Hallazgos.docx` › Facturación #10; `facturacion.txt` › Facturacion almacenamiento y pagos)

#### H-057 – Conteo de los periodos de facturación

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** El periodo debe contar desde el día de ingreso de la mercancía (si ingresa el 6, desde el 6) y el siguiente empieza el día después de que termina el anterior.
- **Contexto (v1):** Detectado en una factura de prueba.
- **Fuente:** F1 (`Hallazgos.docx` › Facturación #11; `facturacion.txt` › Facturacion almacenamiento y pagos)

#### H-058 – Depósitos pendientes por facturar: mostrar solo los que cumplieron el periodo

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** En `/billing/pending-deposits` aparecen todos los depósitos activos y hay que expandirlos. Se solicita, como en el sistema anterior, que aparezcan solo los pendientes: el depósito aparece al cumplirse el periodo, desaparece al facturarlo y vuelve con el siguiente periodo.
- **Contexto (v1):** El operario mantuvo la solicitud pese a la paginación y los filtros.
- **Vínculos:** D-26 · H-082
- **Fuente:** F1 (`Hallazgos.docx` › Facturación #12; `facturacion.txt` › Facturacion almacenamiento y pagos)

#### H-059 – Facturación por CPI con el valor de la mercancía

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** El informe `/billing/reports/deposit-billing` debe quedar igual al del sistema anterior e incluir el valor de la mercancía. Ya permite PDF o Excel.
- **Fuente:** F1 (`Hallazgos.docx` › Facturación #14; `facturacion.txt` › Facturacion almacenamiento y pagos)

#### H-060 – Estado de los pagos registrados

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Consolidado con aclaración
- **Descripción:** Según el documento inicial, los pagos deben aparecer siempre verificados. En la conversación se acordó que los pagos de contado de báscula y guías aparezcan verificados; para almacenamiento, el operario respondió «en almacenamiento no».
- **Aclaración (PA-20):** Lo que se solicita es que todos los pagos queden verificados, sin verificación manual. En almacenamiento ya funciona así (el pago que registra facturación queda verificado); por eso la expresión «en almacenamiento no».
- **Fuente:** F1 (`Hallazgos.docx` › Facturación #15; `facturacion.txt` › Facturacion almacenamiento y pagos) · F2 §1 PA-20

#### H-061 – Reporte de facturación anual con detalle de facturas

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** `/billing/reports/anual` muestra por mes y día solo la cantidad de facturas. Se solicita el listado de facturas con consecutivo, a quién se facturó y valor, cuya suma coincida con el total.
- **Fuente:** F1 (`Hallazgos.docx` › Facturación #16; `facturacion.txt` › Facturacion almacenamiento y pagos)

#### H-062 – Informe de póliza

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** El informe de póliza debe habilitarse para los usuarios de facturación y generarse con los valores de la mercancía según la declaración (la del levante), no según la carta porte.
- **Fuente:** F1 (`Hallazgos.docx` › Facturación #17 y #18)

#### H-063 – Simulador de previsualización de la fórmula

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Consolidado con aclaración
- **Descripción:** En el simulador de previsualización se solicita que aplique la fórmula seleccionada.
- **Aclaración (PA-21):** El simulador está en `/admin/stakeholders/{id}`, al agregar un servicio al acuerdo. Con la fórmula «Por umbral de peso», los datos que pide no corresponden a la fórmula; en general el «Previsualizar» es confuso. La observación adicional sobre la configuración de acuerdos se registra en H-086 y la propuesta en PR-25.
- **Vínculos:** H-086 · PR-25 · PR-28
- **Fuente:** F1 (`Hallazgos.docx` › Facturación #19) · F2 §1 PA-21

#### H-064 – Destinatario de las facturas de almacenamiento y bloqueo al cliente del depósito

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** Las facturas de almacenamiento deben permitir escoger el destinatario, pero el bloqueo de salida se aplica al cliente del depósito.
- **Vínculos:** H-069 · H-070
- **Fuente:** F1 (`Hallazgos.docx` › Facturación #20; `facturacion.txt` › Facturacion montacargas)

#### H-065 – Registro rápido del pago completo

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** Se solicita una acción rápida para registrar el pago completo sin digitar el valor; los pagos parciales se conservan como están.
- **Contexto (v1):** Ya existen acciones rápidas para registrar pagos sin entrar al detalle.
- **Fuente:** F1 (`Hallazgos.docx` › Facturación #21; `facturacion.txt` › Facturacion almacenamiento y pagos)

#### H-066 – Factura de almacenamiento calculada con un valor incorrecto en la prueba

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** En la prueba, el valor de la factura de almacenamiento no fue correcto («no sé de dónde salió ese valor»).
- **Contexto (v1):** Los convenios no estaban cargados.
- **Vínculos:** H-070 · PR-25
- **Fuente:** F1 (`facturacion.txt` › Facturacion almacenamiento y pagos)

#### H-067 – Comprensión del nuevo flujo de facturas (valor automático, aprobar, registrar pago)

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** En el sistema anterior el valor se ingresaba a mano; en el nuevo se calcula con los convenios y se puede cambiar en borrador. Hubo confusión entre aprobar la factura y registrar el pago.
- **Contexto (v1):** Se explicó el flujo: número SIGO, aprobar y registrar pagos.
- **Vínculos:** D-27
- **Fuente:** F1 (`facturacion.txt` › Facturacion almacenamiento y pagos, Facturacion montacargas)

#### H-068 – El documento entregado en báscula no debe presentarse como factura

- **Módulo:** Facturación · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** El documento que se entrega al conductor en báscula no puede decir en ningún lado que es una factura; la factura se hace en SIGO.
- **Contexto (v1):** Ya dice «documento interno de control de pesaje, no es una factura de venta».
- **Fuente:** F1 (`facturacion.txt` › Facturacion Bascula)

#### H-082 – La tabla interna de `/billing/pending-deposits` no cambia con el tema oscuro (nuevo)

- **Módulo:** Facturación · **Tipo:** Observación de revisión · **Estado:** Documentado
- **Descripción:** En `/billing/pending-deposits`, al cambiar al tema oscuro, la tabla interna que muestra las facturas por periodo no cambia de color.
- **Vínculos:** H-058 · H-080
- **Fuente:** F2 §4 Ajustes generales

#### H-086 – Configurar los acuerdos de un cliente es difícil de explicar y lento (nuevo)

- **Módulo:** Facturación · **Tipo:** Observación de revisión · **Estado:** Documentado
- **Descripción:** La forma de agregar servicios al acuerdo fue difícil de explicar y de entender para el operario, y configurar el acuerdo de un cliente lleva mucho tiempo.
- **Vínculos:** H-063 · H-070 · PR-25 · PR-28
- **Fuente:** F2 §1 PA-21

## 5. Hallazgos transversales

### H-069 – Figura de «cliente» frente a «responsable» y destinatario de la factura de almacenamiento

- **Módulos:** Facturación, Comercio Exterior, Báscula · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado
- **Descripción:** En el negocio no existe la figura de «cliente» sino la de responsable. La mercancía de importación se conoce por el importador; en algún punto del proceso se agrega el responsable. La factura de almacenamiento sale a nombre de la «razón social en factura» del Excel de convenios; el bloqueo de salida se aplica al responsable, que se puede seguir manejando como «cliente».
- **Contexto (v1):** En facturación de guías se pidió quitar la opción «cliente» porque se confunden.
- **Vínculos:** H-054 · H-064 · H-070 · H-071
- **Fuente:** F1 (`Hallazgos.docx` › Transversales #1; `facturacion.txt` › Facturacion montacargas, Facturacion almacenamiento; `CONVENIO_23-24-25-26.xlsx` › columnas RESPONSABLE / RAZON SOCIAL EN FACTURA)

### H-070 – Excel de convenios como fuente de responsables, razón social y fórmulas de tarifa

- **Módulos:** Facturación, Comercio Exterior · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado con aclaración
- **Descripción:** El Excel de facturación establece responsable, importador asociado, razón social en factura, tipo de mercancía y la fórmula de la tarifa de almacenamiento. Es preferible que el sistema quede cargado con los clientes y sus fórmulas, idealmente importando el Excel.
- **Contexto (v1):** Hojas 2022, 2023-2024, 2025 y 2026, más «Bascula» y «EXPO». Tarifas en texto libre. En la prueba los convenios no estaban cargados.
- **Relación con la revisión:** F2 §3 indica que el Excel contiene todos los clientes con sus fórmulas de cobro y, en la hoja «Bascula», los precios base de todos los servicios. Con ese Excel se debe buscar una mejor alternativa para cargar las fórmulas de los acuerdos (PR-25).
- **Vínculos:** PR-25 · RV (Excel, sección 9) · H-063 · H-086
- **Fuente:** F1 (`Hallazgos.docx` › Transversales #2; `CONVENIO_23-24-25-26.xlsx`; `facturacion.txt` › Facturacion almacenamiento y pagos) · F2 §1 PA-21, §3

### H-071 – Mercancía con responsable desconocido o nuevo al momento del ingreso

- **Módulos:** Comercio Exterior, Facturación · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Consolidado con aclaración
- **Descripción:** A veces se conoce el importador pero no el responsable, o el responsable es nuevo y no tiene tarifa. No afecta el ingreso, pero facturación no puede emitir la factura de almacenamiento. Comercio exterior solicita confirmar el depósito sin cliente y que se facture desde que se asigna el cliente.
- **Aclaración (F2 §2):** Se debe poder confirmar el depósito sin cliente; la facturación se activa desde que se asigna el cliente. Va ligado a la configuración de los acuerdos a partir del Excel de facturación.
- **Vínculos:** H-069 · H-070 · PR-25
- **Fuente:** F1 (`Hallazgos.docx` › Transversales #3, Comercio Exterior #4; `facturacion.txt` › Facturacion-acuerdos; `Comercio exterior.txt` › Productos) · F2 §2 Comercio Exterior

### H-072 – Vehículos que llegan a cargar sin orden de cargue

- **Módulos:** Báscula, Comercio Exterior, Bodega · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Consolidado con aclaración
- **Descripción:** En la v2 la salida requiere una orden de cargue creada antes de pesar en báscula. En la operación, la mayoría de vehículos llegan sin orden: algunos clientes cargan antes porque no saben si cabrá toda la mercancía; la orden llega cuando el vehículo ya está cargado y puede cambiar. Otras veces la cantidad es exacta y la orden llega antes. Sin orden, báscula no puede registrar el ingreso, y devolverlo a comercio exterior retrasa la operación.
- **Contexto (v1):** El desarrollador planteó en la visita que, si no existe orden al pesar la salida, se cree en borrador para que comercio exterior la confirme; de la orden confirmada sale la guía, y bodega ejecuta el cargue solo con la guía generada.
- **Aclaración (C-08):** Es el mismo escenario de PA-14: el camión entra sin orden, pasa primero por báscula, donde se crea la orden en borrador; luego carga, y cuando el cliente ya sabe qué va a cargar le pasa la orden a Comercio Exterior. Debe considerar los tres tipos de salida, con el legacy como referencia.
- **Vínculos:** D-23 · PR-21 · PR-22 · H-017 · H-042
- **Fuente:** F1 (`bascula.txt` › Ordenes de cargue; `Comercio exterior.txt` › Guias de salida, Cargues actuales) · F2 §1 PA-14 · F4 C-08

### H-073 – Pesaje intermedio bloqueado hasta que bodega registre la llegada del camión

- **Módulos:** Báscula, Bodega, Comercio Exterior · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Consolidado con aclaración
- **Descripción:** Al registrar un peso intermedio aparece el mensaje de que bodega debe registrar la llegada antes del segundo pesaje. Bodega suele demorarse y esperar detiene la operación. Según el documento inicial, bodega no debe bloquear las operaciones de otros módulos y se debe validar el tiempo de los registros pendientes para emitir una alerta de retraso a comercio exterior.
- **Contexto (v1):** Se diferenció «ingreso» en bodega (confirmar llegada) de «recepción» (descargue terminado). El desarrollador indicó que quitaría el bloqueo para báscula y agregaría una alerta por tiempo.
- **Aclaración (F2 §2, Bodega):** Los operarios comentan que los supervisores de bodega suelen estar ocupados para registrar el ingreso y la recepción de inmediato. La alerta se debe lanzar a **comercio exterior y bodega**, y su configuración se relaciona con PA-25.
- **Vínculos:** PR-09 · PR-14 · PR-17 (etapa Bodega) · PR-26 · H-021 · H-024
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #28, Bodegas #2; `bascula.txt` › Multideposito (Importante)) · F2 §2 Báscula y Bodega, §4 Bodega

### H-074 – Corrección de la carta porte y demás datos del ingreso

- **Módulos:** Báscula, Comercio Exterior · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Consolidado con aclaración
- **Descripción:** Cuando se digita mal la carta porte u otro dato, no se puede corregir; báscula lo intentó desde comercio exterior y no pudo. Báscula solicita editar todo desde báscula (carta porte, documento, placa, conductor, empresa de transporte). Comercio exterior también solicita editar la carta porte. Con varios vehículos con la misma carta porte (arrastre) la edición no es posible.
- **Contexto (v1):** El desarrollador indicó que en borrador todo es editable; el operario no pudo.
- **Aclaración (PA-22):** Los datos del ingreso se pueden editar en cualquier momento en el legacy. Los operarios buscan la misma flexibilidad: comercio exterior debe poder editar los mismos datos que en el legacy, y báscula también debe poder corregirlos. El operario de báscula no pudo editarlos porque no tiene la opción en su módulo.
- **Vínculos:** D-11 · PR-11 · PR-01 · H-084 · H-075 · H-010
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #7, Comercio Exterior #3; `bascula.txt` › Bascula, Eliminación de ticket; `Comercio exterior.txt` › Productos) · F2 §1 PA-22

### H-075 – Edición de la placa desde báscula además de vigilancia

- **Módulos:** Vigilancia, Báscula · **Tipo:** Hallazgo reportado por operarios · **Estado:** Consolidado con aclaración
- **Descripción:** Vigilancia a veces se equivoca en las placas. Báscula solicita editar la placa desde su encabezado (solo la placa; la modalidad se cambiaría desde vigilancia). En una prueba, un registro no permitió editar la modalidad y otros sí.
- **Contexto (v1):** Se explicó que es mejor cambiar la placa desde vigilancia porque se propaga en cascada; el desarrollador indicó que podría habilitarla en báscula.
- **Relación con la revisión:** La propuesta del formulario incluye la sección «Vigilancia» con los datos de vigilancia y opción de editarlos; el motivo de ingreso también se puede corregir ahí (PR-01, PR-02).
- **Vínculos:** PR-01 · PR-02 · H-074
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #21; `bascula.txt` › Editar placa bascula, Salida Mcia) · F2 §4 Báscula

### H-076 – Obligatoriedad del tipo de vehículo

- **Módulos:** Báscula, Bodega, Facturación · **Tipo:** Hallazgo reportado por operarios + Propuesta · **Estado:** Consolidado con aclaración
- **Descripción:** Según el documento inicial, el tipo de vehículo debe ser opcional en báscula y obligatorio en bodega. Báscula no lo necesita; lo podría necesitar facturación (Jennifer).
- **Contexto (v1):** La respuesta de facturación quedó incompleta («Lo requiere. Cuando se captura de almacenamiento…»).
- **Aclaración (PA-23):** El tipo de vehículo es necesario para facturar el montacargas y se almacena como información de cada vehículo. La revisión propone quitarlo de báscula y registrarlo en bodega como opcional (PR-10). Por C-05, «obligatorio en bodega» queda como antecedente reemplazado.
- **Vínculos:** PR-10 · PR-13
- **Fuente:** F1 (`Hallazgos.docx` › Báscula #16; `bascula.txt` › Inspaccion parte 1; `facturacion.txt` › Facturacion montacargas) · F2 §1 PA-23 · F4 C-05

### H-077 – Origen de la tasa de cambio: manual en comercio exterior y consulta a la DIAN en facturación

- **Módulos:** Comercio Exterior, Facturación · **Tipo:** Hallazgo reportado por operarios + Aclaración · **Estado:** Consolidado con aclaración
- **Descripción:** Comercio exterior solicita tasa manual cada lunes y no consultada a la DIAN. En facturación, el desarrollador indicó que la TRM se consulta automáticamente a un servicio de la DIAN.
- **Aclaración (PA-24):** El operario de comercio exterior solicitó usar la tasa manual igual que en el legacy. La revisión propone que facturación siga la misma lógica (paridad con el legacy). Es una sola tasa compartida (C-15).
- **Vínculos:** D-22 · PR-23 · H-034 · OV-02
- **Fuente:** F1 (`Comercio exterior.txt` › Levante 1; `facturacion.txt` › Facturacion almacenamiento y pagos) · F2 §1 PA-24 · F4 C-15

### H-078 – Destinatarios de las notificaciones (repesaje)

- **Módulos:** Administración, Báscula · **Tipo:** Hallazgo reportado por operarios + Propuesta · **Estado:** Consolidado con aclaración (antes «pendiente de clasificación»)
- **Descripción:** Las notificaciones de repesaje llegan solo al usuario de administración. El operario comentó que sería bueno que también le llegaran a él.
- **Contexto (v1):** Se pueden configurar más usuarios para ciertas notificaciones.
- **Respuesta de la revisión (PA-25):** Clasificada como propuesta (C-02): el administrador configura los destinatarios por rol de las notificaciones existentes (PR-26). Con esto el hallazgo pasa a transversal (Administración).
- **Vínculos:** PR-26 · H-073
- **Fuente:** F1 (`bascula.txt` › Ordenes de cargue) · F2 §1 PA-25

### H-079 – Sidebar con varios roles: detalle de usuario apretado y avatar cortado (nuevo)

- **Módulos:** Interfaz general · **Tipo:** Observación de revisión · **Estado:** Documentado
- **Descripción:** Cuando un usuario tiene varios roles, en el sidebar el detalle del usuario y los roles se ven apretados y el avatar aparece cortado.
- **Vínculos:** RV-03 · PR-28
- **Fuente:** F2 §4 Ajustes generales

### H-080 – El switch de tema claro/oscuro no responde al clic sobre el switch (nuevo)

- **Módulos:** Interfaz general (Mi cuenta › Preferencias) · **Tipo:** Observación de revisión · **Estado:** Documentado
- **Descripción:** En las preferencias de «Mi cuenta», el switch para cambiar de tema no funciona si se hace clic sobre él; hay que hacer clic fuera del switch para que se aplique.
- **Vínculos:** H-082
- **Fuente:** F2 §4 Ajustes generales

### H-081 – En los modales con alertas, el header tapa parte de la alerta (nuevo)

- **Módulos:** Interfaz general · **Tipo:** Observación de revisión · **Estado:** Documentado
- **Descripción:** Cuando un modal muestra alertas, el header tapa parte de la alerta. La revisión indica agregar padding al contenido.
- **Fuente:** F2 §4 Ajustes generales

### H-083 – Menú denso y páginas de listado cargadas de cards (nuevo)

- **Módulos:** Interfaz general (todos los módulos) · **Tipo:** Observación de revisión · **Estado:** Documentado
- **Descripción:** El menú es muy denso y dificulta la navegación. Las páginas principales de listados están cargadas de cards innecesarias (título, subtítulo, resúmenes).
- **Vínculos:** PR-28 · PR-29 · PR-30 · H-022
- **Fuente:** F2 §4 Ajustes generales

**Temas recurrentes entre módulos (referencia, no son hallazgos adicionales).**

- *Vistas y columnas equivalentes al legacy:* H-003, H-026, H-047; propuestas PR-05, PR-16, PR-18.
- *Edición de datos después del registro inicial:* H-008, H-012, H-018, H-019, H-028, H-030, H-031, H-041, H-046, H-074, H-075, H-084; propuestas PR-01, PR-11, PR-17.
- *Orden de cargue y guías de salida:* H-017, H-025, H-042, H-045, H-054, H-055, H-072; propuestas PR-21, PR-22.
- *Bodega no bloqueante y alertas:* H-073, H-078; propuestas PR-09, PR-14, PR-26.
- *Convenios y tarifas:* H-063, H-066, H-069, H-070, H-071, H-086; propuestas PR-25, PR-28.

## 6. Observaciones de revisión de V2 y legacy

### 6.1. Observaciones de la revisión del usuario (v2)

Registradas como hallazgos con su módulo:

| ID | Observación | Módulo | Sección |
|---|---|---|---|
| H-045 (parte) | Selectores de la orden de cargue lentos (más de 1.000 registros) | Comercio Exterior | 4.3 |
| H-079 | Sidebar con varios roles apretado, avatar cortado | Interfaz general | 5 |
| H-080 | Switch de tema no responde sobre el switch | Interfaz general | 5 |
| H-081 | Header de modal tapa las alertas | Interfaz general | 5 |
| H-082 | Tabla interna de `/billing/pending-deposits` sin tema oscuro | Facturación | 4.4 |
| H-083 | Menú denso y listados con cards innecesarias | Interfaz general | 5 |
| H-085 | Espacio vertical sobrante en el ticket impreso | Báscula | 4.1 |
| H-086 | Configurar acuerdos es difícil y lento; simulador confuso | Facturación | 4.4 |
| H-032 (corrección) | La creación de productos no se realiza en bodega | Comercio Exterior | 4.3 |

### 6.2. Observaciones de los videos (legacy)

Fuente: F3. Los videos muestran a la operaria de Comercio Exterior en el legacy con el depósito `BA3066` (1 producto, 930 cajas, 24 940 kg, llegó en dos camiones y salió completo sin descargar). Tiempos aproximados.

| ID | Observación | Video y tiempo | Relaciona |
|---|---|---|---|
| OV-01 | El levante calcula la cantidad desde el peso bruto digitado, en proporción a lo ingresado (Σ cantidad ÷ Σ manifiesto), solo si el depósito tiene un producto | RV-07, 0:40 | H-039, PA-12, D-19 |
| OV-02 | La tasa de cambio llega precargada con la tasa semanal y es editable en el formulario de levante | RV-07, 0:28 | H-034, H-077, PA-08, PA-24, D-22 |
| OV-03 | El levante pide número de levante, número de aceptación y solo la fecha del levante (sin fecha de aceptación) | RV-07, 0:28 | H-038, PA-11, D-20 |
| OV-04 | El registro de levante muestra una matriz Ingreso / Nacionalizados / Saldo con columnas Cant., Peso y una columna por producto | RV-07, 0:28–0:56 | H-036, H-040, PA-09, D-18 |
| OV-05 | Salida global: en «Salidas Import.» se elige el depósito y se marcan los dos tiquetes de ingreso; la guía lleva los dos tiquetes y las dos placas, una línea por producto con saldo anterior, cantidad que sale y nuevo saldo. Sin orden de cargue ni báscula. El firmante es el importador | RV-07, 1:12–1:52 | H-042, PA-14, D-23 |
| OV-06 | Desde «Tickets Ingresos» (fecha y hora, vehículo, conductor, ID conductor, peso bruto, peso mercancía, tara, cantidad, peso manifiesto, doc. entrada, repesa, valor, tiquete, estado) se abre «Modificar entrada a báscula» y se cambian indicador, manifiesto y mercancía en un solo formulario para cuadrar con la planilla de recepción DIAN | RV-08, 0:16–2:20 | H-008, H-041, PA-02, PA-13, D-12, D-13 |
| OV-07 | El peso de la mercancía lo digita la operaria y la T. vehículo se recalcula sola (indicador − mercancía) | RV-08, 0:52–1:36 | H-041, PA-13, D-12 |
| OV-08 | Los pesos editados se reflejan de inmediato en el depósito y en el levante | RV-08 | H-041 |
| OV-09 | «Modificar datos del depósito» permite editar fecha y hora, número del depósito y observaciones; el resto se muestra en solo lectura | RV-08, 2:36 | H-028, D-15 |
| OV-10 | Los productos amparados se registran aparte (producto, embalaje y cantidad amparada) | RV-08, 3:08 | H-031, D-16 |
| OV-11 | El formulario de levante pide «CIF USD» y calcula «FOB CO» = CIF USD × tasa | RV-07, 0:40 | H-037, PA-10 |

## 7. Diferencias entre versiones

Se registran tal como las describen las fuentes, sin interpretación. Cuando una fuente no describe el comportamiento de una de las versiones, se indica «sin descripción en las fuentes». Para la comparación en el código, ver el análisis de paridad (Ref.), que es insumo de la fase 2.

| ID | Tema | Legacy | V2 (versión actual) | Fuente | Relaciona |
|---|---|---|---|---|---|
| D-01 | Registro de inspecciones | Registra placa, conductor, peso y mercancía, sin crear depósito | Crea un depósito de inspección | F1 H-001 | H-001, PR-07 |
| D-02 | Ticket sin repesaje | Imprime ticket de entrada (bruto), ticket con tara automática y recibo sin repesar | Hay que hacer el repesaje para imprimir | F1 H-005 | H-005 |
| D-03 | Columnas de entradas, salidas y solo pesaje | Fecha, hora, placa, conductor e ID, peso bruto, peso mercancía, tara y cantidad, iguales en las tres vistas | Columnas distintas; no sirven a Báscula, Comercio Exterior ni Facturación | F1 H-003, H-026, H-047 | PR-05, PR-18 |
| D-04 | Eliminación de tickets | Existe: muestra el ticket, pide la razón y lo marca en rojo | No existe la opción | F1 H-010 | H-010 |
| D-05 | Coincidencias de carta porte | Lista de coincidencias al digitar, desde los caracteres iniciales | Coincidencias de depósitos abiertos (borrador o confirmado), identificadas por número de depósito | F1 H-011; F2 PA-04; F4 C-17 | H-011 |
| D-06 | Conductores con el mismo documento | Se agrega un punto al final del número | Valida número y país; no permite repetir | F1 H-014 | H-014 |
| D-07 | Camión con más de una mercancía | Un registro nuevo por cada depósito adicional | Documentos pedidos entre un pesaje y otro | F1 H-021 | H-021 |
| D-08 | Historial de báscula | Vistas separadas de entradas, salidas y solo pesaje | Historial único | F1 H-022 | PR-05 |
| D-09 | Repesajes | Permite más de un repesaje | Sin descripción en las fuentes | F2 §4 Báscula | PR-04 |
| D-10 | Edición tras terminar el ciclo | Se sigue editando en entradas, salidas y solo pesaje | Se pide para la v2 | F2 §4 Báscula | H-084 |
| D-11 | Edición de los datos del ingreso | Se editan en cualquier momento | Báscula no tiene la opción en su módulo | F2 PA-22 | H-074, PR-11 |
| D-12 | Edición de pesos del tiquete | Comercio Exterior edita indicador, manifiesto y mercancía en un formulario; la tara se recalcula | Comercio Exterior necesita poder editar cualquier peso como en el legacy | F2 PA-02, PA-13; F3 OV-06, OV-07 | H-008, H-041, PR-11 |
| D-13 | Lista de tiquetes de ingreso en Comercio Exterior | «Tickets Ingresos», con «Editar» por tiquete | Se propone crear el ítem «Tickets de ingreso» | F3 OV-06; F2 §4 | H-026, H-041, PR-18 |
| D-14 | Vista de depósitos | Tabla con fecha, depósito, carta porte, importador, transportadora, manifiesto, producto, placa, cantidad, peso y etiqueta | Tarjetas; la cantidad exige abrir el depósito | F1 H-027; F3 Video 1 | PR-15, PR-16 |
| D-15 | Datos del depósito | Fecha y hora, número y observaciones editables en cualquier momento | No permite editar la fecha de llegada ni el manifiesto (según H-028) | F3 OV-09; F1 H-028 | H-028, PR-17 |
| D-16 | Productos tras confirmar | Se agregan o quitan mientras la mercancía no haya salido; amparados registrados aparte | Solo en borrador | F1 H-031; F3 OV-10 | H-031, PR-17 |
| D-17 | Prefijos de números | Prefijos configurables para levante, aceptación y manifiesto | Sin prefijos | F1 H-035 | H-035 |
| D-18 | Productos en el levante | Una columna por producto; se pone cero en el que no corresponde | Se escoge el producto con un select | F1 H-036; F2 PA-09; F3 OV-04 | H-036, PR-19 |
| D-19 | Cantidad del levante | Se calcula desde el peso, en proporción a lo ingresado, solo con un producto (`registrarlevante.php:246-254`, `:611`) | No se calcula | F2 PA-12; F3 OV-01 | H-039 |
| D-20 | Datos de aceptación | Número de levante, número de aceptación y fecha del levante | Pide además la fecha de aceptación | F1 H-038; F2 PA-11; F3 OV-03 | H-038 |
| D-21 | Levantes sucesivos | Al guardar se puede registrar otro de inmediato, viendo lo que queda | Hay que guardar y volver a abrir | F1 H-040 | H-040, PR-19 |
| D-22 | Tasa de cambio | Manual, semanal, precargada y editable en el levante | Consultada automáticamente a la DIAN | F1 H-034, H-077; F2 PA-08, PA-24; F3 OV-02 | PR-23 |
| D-23 | Salidas | Tres modalidades (tiquete de entrada, depósito y global); guía directa; tiquete y global sin báscula | Orden de cargue previa a báscula y guía desde la orden; corresponde a la modalidad por depósito | F1 H-042, H-072; F2 PA-14; F3 OV-05 | PR-21, PR-22 |
| D-24 | Búsqueda de facturas | Facturas emitidas buscables por carta porte, factura, depósito, número SIGO y cliente | Búsqueda principalmente por NIT | F1 H-048 | H-048 |
| D-25 | Reporte de guías | Fecha y hora, guía, depósito, placa, mercancía, embalaje, cantidad y CPI | Sin esos datos en la vista de facturas de guías | F1 H-055 | H-055 |
| D-26 | Depósitos pendientes por facturar | Solo aparecen los que cumplieron el periodo | Aparecen todos los activos | F1 H-058 | H-058 |
| D-27 | Valor de la factura | Se ingresa a mano | Se calcula con los convenios y se puede cambiar en borrador | F1 H-067 | H-067 |

## 8. Propuestas de modificación de flujos

**Todas las propuestas de esta sección son no aprobadas.** Salvo que se indique otra cosa, su origen es la revisión del usuario (F2). La nota de F2 §4 Báscula aplica a todo el bloque: la intención es simular el comportamiento del legacy para que el operario se adapte sin esfuerzo; el agente que haga el análisis funcional debe validar la viabilidad, informar incongruencias y ampliar con los hallazgos. Los mockups hechos con IA son referencia de estructura y contenido; los estilos se adaptan al tema de la aplicación.

### 8.1. Báscula

#### PR-01 – Formulario de registro de báscula como página

- **Origen:** F2 §4 Báscula (1) · F4 C-11, C-13 · **Mockup:** MK-01
- **Comportamiento actual:** El pesaje en `/operations/weighbridge?camion={id}` se hace en un modal.
- **Propuesta:** Migrar el formulario a una página, conservando la distribución y los estilos del modal actual, para ganar espacio y reutilizarlo en Comercio Exterior.
  - **Encabezado:** pasos del mismo tamaño que en el modal y, a la derecha, «Volver a la cola» y «Guardar». El switch «Requiere segundo pesaje» queda visible en el encabezado.
  - **Tres pasos:** Registro, Cobro y Tiquete. El peso se registra en el paso 1, como en el legacy.
  - **Sección «Vigilancia»** (cada sección en su card): datos de vigilancia, compactos, con «Editar» que la abre como hoy «Camión y conductor».
  - **Sección «Registro»:** subsección «Modalidad» con Importación, Exportación o Inspección (**radio buttons, una sola modalidad**, C-13) y, en una fila, tipo de documento, número de documento y número de manifiesto. Subsección «Mercancía» con la tabla de productos y un botón de agregar más pequeño. Sin unidad de medida (PR-12).
  - **Sección «Pesaje (kg)»:** inputs en dos filas y dos columnas: P. Indicador y P. Vehículo; P. Manifiesto y P. Mercancía. La T. vehículo se calcula según lo digitado, como en el legacy.
  - **Sección «Datos para Comercio exterior»:** F2 la planteaba opcional y contraída en báscula; por C-11 **se quita de báscula** porque el operario no la va a usar. La sección de Comercio Exterior va en la edición de entradas (PR-17).
  - **Se elimina la sección «Pesaje y observaciones»:** la fecha de ingreso del depósito (ya está en Vigilancia), el «Primer pesaje» (en un ingreso con depósito siempre es bruto), el switch de perecederos (basta «Requiere segundo pesaje»), y las observaciones y documentos adicionales (no se usan y generan ruido).
  - **Labels flotantes** de PrimeVue (variante `on`) en lugar de labels y placeholders.
  - **Exportación e Inspección:** mismos cambios más los ajustes de los hallazgos (por ejemplo, la descripción obligatoria de inspección, PR-07).
  - **Salida de mercancía y Solo báscula:** conservan sus secciones actuales con los ajustes de los hallazgos.
  - **Cobro y Tiquete:** conservan la distribución y funcionalidad actual dentro de la página.
- **Diferencia con el mockup:** En MK-01 los botones de guardar están al pie y el encabezado tiene «Volver a la cola»; el texto ubica «Guardar» en el encabezado.
- **Relaciona:** H-002, H-012, H-015, H-017, H-018, H-019, H-020, H-075, H-084

#### PR-02 – Motivo de ingreso con categoría en lugar del selector de tipo de operación

- **Origen:** F2 §4 Báscula (1)
- **Propuesta:** Quitar el selector «Tipo de operación». El formulario se filtra por el motivo de ingreso que viene de vigilancia. Los motivos de ingreso tienen una categoría: «Ingreso», «Salida» o «Solo báscula». Si vigilancia registró mal el motivo, báscula lo corrige desde la sección Vigilancia y el formulario se actualiza de inmediato.
- **Relaciona:** H-075, PR-01, PR-28 (Motivos de entrada en Configuración)

#### PR-03 – «Guardar» y «Guardar sin pesaje», con estados en la cola

- **Origen:** F2 §4 Báscula (1) · **Mockup:** MK-01
- **Propuesta:** Dos botones. «Guardar»: los pesajes son obligatorios; guarda el registro y los pesajes, y el camión queda «Por cobrar» en la cola hasta completar el paso 2. «Guardar sin pesaje»: los pesajes no son obligatorios ni se guardan; genera el registro como el paso 1 actual y el camión queda «Por pesar». En ambos casos se redirige al paso 2 (cobro). Los registros «Por cobrar» y «Por pesar» se retoman desde donde quedaron.
- **Relaciona:** H-009, PR-01

#### PR-04 – Repesaje en un modal

- **Origen:** F2 §4 Báscula (1)
- **Propuesta:** Un modal con los cuatro pesos y la información registrada en solo lectura, donde solo se puede modificar el peso del vehículo (tara).
- **Para la fase 2:** investigar por qué el legacy permite más de un repesaje y si hace falta (D-09).
- **Relaciona:** D-09, H-008, PR-09

#### PR-05 – Historial de báscula en tres páginas

- **Origen:** F2 §1 PA-06, §4 Báscula (2)
- **Propuesta:** Dividir `/operations/weighbridge/history` en tres subítems del menú: Entradas, Salidas y Solo báscula (PA-06 lo llama «Solo pesaje»). Entradas con tres pestañas: Importación, Exportación e Inspección. Columnas de Entradas, las del legacy: fecha y hora, vehículo, conductor, ID conductor, P. bruto, P. mercancía, tara vehículo, cantidad, peso manifiesto, doc. entrada (tipo y número), repesa, valor, ticket y estado, más acciones. Salidas y Solo báscula: las columnas del legacy más ticket y estado. La edición abre otra vez el formulario de registro. Filtros por columna (solo filtros globales si se requieren), sin el panel de filtros ni las cards de resumen.
- **Relaciona:** H-003, H-022, H-084, D-03, D-08, PR-29

#### PR-06 – Registro «Solo báscula»: sin peso esperado y con tercero

- **Origen:** F2 §2 Báscula
- **Propuesta:** En el registro de tipo «Solo báscula», quitar «Peso esperado» y cambiar «Cliente» por «Tercero», con un select paginado que busque por nombre o NIT.
- **Relaciona:** PR-27

#### PR-07 – Depósito de inspección con registro flexible en báscula

- **Origen:** F2 §1 PA-01 · F4 C-14
- **Propuesta:** El depósito de inspección se sigue creando como hoy. Al registrar el ingreso en báscula, documentos y producto son opcionales y se agrega un campo de descripción obligatorio. El cobro (valor fijo por vehículo) se maneja igual que importación, confirmado con los operarios.
- **Relaciona:** H-001, D-01, PR-01, PR-20

#### PR-08 – Quitar el botón «Soltar camión»

- **Origen:** F2 §2 Báscula
- **Propuesta:** Quitar el botón «Soltar camión»; no es necesario.

#### PR-09 – Báscula sin bloqueos de bodega

- **Origen:** F2 §2 Báscula
- **Propuesta:** No debe haber bloqueos para el proceso de báscula; quitar el bloqueo de bodega para el repesaje.
- **Relaciona:** H-073, PR-14

#### PR-10 – Tipo de vehículo en bodega, opcional

- **Origen:** F2 §1 PA-23 · F4 C-05
- **Propuesta:** Quitar el tipo de vehículo del formulario de báscula y registrarlo en bodega al registrar la recepción, como opcional. Se guarda como información del vehículo y es necesario para facturar el montacargas. En `/warehouse/forklift`, al digitar la placa, si el camión ya tiene tipo de vehículo, se precarga.
- **Relaciona:** H-076, PR-13

#### PR-11 – Edición de los datos del ingreso y de los pesos como en el legacy

- **Origen:** F2 §1 PA-02, PA-13, PA-22
- **Propuesta:** Comercio exterior puede editar cualquier peso registrado en báscula y los mismos datos del ingreso que edita en el legacy; báscula también puede corregir los datos del ingreso desde su módulo. En Comercio Exterior la edición se hace desde la pantalla de edición de entradas (PR-17).
- **Relaciona:** H-008, H-041, H-074, H-084, D-11, D-12, OV-06, OV-07

#### PR-12 – Quitar la unidad de medida de los productos en toda la app

- **Origen:** F2 §4 Báscula (1) · F4 C-04
- **Propuesta:** Eliminar la unidad de medida de los productos y de toda la app porque no se usa. Se conserva el embalaje, que sí usan Facturación y Comercio Exterior.
- **Relaciona:** H-018, H-033

### 8.2. Bodega

#### PR-13 – Registro rápido de montacargas desde recepciones

- **Origen:** F2 §4 Bodega (1)
- **Propuesta:** En `/warehouse/receptions`, un botón para registrar el uso del montacargas sin cambiar de vista.
- **Relaciona:** PR-10, H-051

#### PR-14 – Bodega no bloqueante: control de tiempo, alertas e indicador visual

- **Origen:** F2 §2 Bodega, §4 Bodega (2) · F1 H-073 (contexto de la visita)
- **Propuesta:** Bodega no bloquea el flujo. Se controla el tiempo de los registros de ingreso y recepción y se lanza una alerta a Comercio Exterior y Bodega al superar un límite (configuración ligada a PR-26). En las tablas de bodega, un indicador visual del estado y del tiempo de retraso (por ejemplo, fila en rojo o amarillo).
- **Relaciona:** H-073, PR-09, PR-17 (etapa Bodega), PR-26

### 8.3. Comercio Exterior

#### PR-15 – Menú «Depósitos» por tipo, con filtros de estado y fecha

- **Origen:** F2 §4 Comercio Exterior (1, 2)
- **Propuesta:** Ocultar `/foreign-trade/deposits`. «Depósitos» se expande en Importación, Exportación e Inspección. Cada opción muestra su tabla y un panel de filtros con el estado (Borrador, Confirmado, Anulado o Cerrado) y fechas desde y hasta; cada cambio filtra la tabla. Por defecto, Borrador. La tabla muestra un solo estado a la vez y los filtros deben ser claros.
- **Diferencia con el mockup:** MK-02 muestra filtros «Todos / Pendientes / Facturados»; el texto define los filtros de estado anteriores.
- **Relaciona:** H-027, D-14, PR-16

#### PR-16 – Tabla de depósitos de importación maestro-detalle

- **Origen:** F2 §4 Comercio Exterior (3.1) · **Mockup:** MK-02
- **Propuesta:** Una tabla con fila expandible (row expansion de PrimeVue) que condensa lo que el legacy muestra en «Tickets ingreso», «Ingresos» y «Depósitos Import.». Columnas del mockup, que sí corresponden a lo que se debe implementar: Fecha, No. Depósito (con placa), Doc. comercial, Tickets, Terceros (cliente e importador), Mercancía (embalaje), Pesos (bruto, mercancía, tara, manifiesto), Estado y Acciones. Fila expandida: Manifiesto DIAN y valor de la mercancía; tabla con Vehículo/Placa, Mercancía (embalaje), Cantidad, Cant. ampara, Peso (kg), Tiquete, MPreimp (en el legacy «Manifiesto PreImp.») y acciones (adhesivo, ticket); totales de cantidad y peso que entra, amparado y saldo; botones «Gestionar amparados» y «Ver depósito». Aplica a todos los estados; algunos datos varían según el estado. Los botones de acción del mockup son referencia.
- **Relaciona:** H-026, H-027, D-14, PR-15, PR-17

#### PR-17 – Detalle del depósito de importación por etapas

- **Origen:** F2 §4 Comercio Exterior (3.2) · F4 C-09, C-11 · **Mockup:** MK-03
- **Propuesta:** Del mockup se toman exactamente: el stepper de etapas (Entradas, Datos principales, Bodega, Amparados, Levantes, Salidas), la disposición de botones del encabezado y las etiquetas, la «Información general» (placas de los camiones ingresados, producto y subpartida, importador y NIT, manifiesto DIAN, fecha y hora del depósito, balance de cantidades y balance de pesos) y el «Progreso». Cada etapa del mockup es solo referencia; al hacer clic en una etapa se muestra solo lo suyo:
  - **Entradas:** tabla con fecha y hora, vehículo/placa, conductor, ticket de báscula, mercancía (embalaje), peso bruto, peso total de la mercancía, tara del vehículo, cantidad, peso manifiesto y acciones (editar). «Editar» abre otra pantalla con las secciones Vigilancia y Báscula; al editar Báscula se muestra el formulario de registro (PR-01) y además la sección de Comercio Exterior con Unidades de carga, Fecha de manifiesto, Precio de la mercancía y Moneda (C-11).
  - **Datos principales:** fecha y hora, número de manifiesto, fecha del manifiesto DIAN, documento comercial (tipo, número y fecha), terceros relacionados (cliente, empresas de transporte, agencia de aduanas e importador; en F2 dice «Importados»), peso neto CPI, peso bruto CPI, precio de la mercancía CPI y moneda del precio.
  - **Bodega:** datos de bodega, inventario y movimientos. El paso se muestra en rojo o amarillo si, cumplido el tiempo límite, **el operario de bodega** aún no registra el descargue (C-09).
  - **Amparados:** tabla consolidada de productos del depósito; se ingresa la cantidad amparada de cada producto y se agregan, quitan o editan productos y cantidades.
  - **Levantes:** ver PR-19.
  - **Salidas:** tabla con fila expandible. Fila principal: fecha, número de guía, modo de salida (de los tres, PR-21), ciudad destino y observaciones. Detalle: Producto, Cant. entrada, Saldo anterior, Cantidad a salir, Nuevo saldo y total de la salida, con enlace para descargar la guía. Opción de editar la salida «hasta cuando sea posible» y botón «Nueva salida».
- **Relaciona:** H-027, H-028, H-029, H-030, H-031, H-073, D-15, D-16, PR-11, PR-14, PR-19, PR-21

#### PR-18 – «Tickets de ingreso» en el menú principal

- **Origen:** F2 §4 Comercio Exterior (3.2, Entradas)
- **Propuesta:** Un ítem de menú «Tickets de ingreso» con la tabla de entradas del depósito más el número de depósito como enlace al detalle, y la acción «Editar» que lleva a la misma pantalla de edición de la entrada. Da acceso rápido al listado de ingresos, muy importante para el operario.
- **Relaciona:** H-026, H-041, D-13, OV-06

#### PR-19 – Levantes: tabla agrupada por mercancía y vista general

- **Origen:** F2 §4 Comercio Exterior (Levantes) · F4 C-06, C-07 · **Mockups:** MK-04, MK-05, MK-06
- **Propuesta (C-06):** El diseño de `mockups/levantes/` es la propuesta; reemplaza como propuesta a las dos opciones de PA-09 (modal con columnas o con select).
  - **Tabla compartida, agrupada por mercancía:** encabezado de ingreso (mercancía, embalaje, estado Sin levante / Parcial / Nacionalizado, cantidad y peso de ingreso), una fila por levante (Nº levante, Nº aceptación, fecha del levante, tasa, CIF (USD), cantidad, peso, acciones: ver documento, editar, eliminar), «Agregar levante» como fila editable que propone el saldo disponible, y filas de Nacionalizado y Saldo con aviso de diferencia de peso.
  - **Vista 1 (pestaña Levantes del detalle):** encabezado con Exportar y Nuevo levante, resumen en cuatro tarjetas (Ingreso, Nacionalizado con avance, Saldo en bodega, Levantes), alerta de diferencia de peso y la tabla agrupada. De esta vista aplica el contenido de la pestaña; el stepper es el de PR-17.
  - **Vista 2 (vista aparte, C-07):** depósitos y levantes en maestro-detalle con búsqueda (depósito, documento, importador, mercancía o Nº de levante), filtro por estado de nacionalización con conteo y botón «Con diferencia de peso». Columnas: depósito y fecha, documento comercial, terceros, mercancía, ingreso, nacionalizado con avance, saldo y estado; la fila expandida muestra la tabla agrupada compacta con opción de agregar levantes.
- **Nota:** La columna «CIF (USD)» del mockup convive con la aclaración de PA-10 (etiqueta «Valor en aduanas»).
- **Relaciona:** H-036, H-037, H-040, D-18, D-21, OV-01, OV-04

#### PR-20 – Depósitos de exportación e inspección

- **Origen:** F2 §4 Comercio Exterior (4)
- **Propuesta:** Estructura y diseño similares a los de importación, ajustando las etapas y campos de cada tipo.
- **Relaciona:** PR-07, PR-15, PR-16, PR-17

#### PR-21 – Tres modalidades de salida y orden de cargue en borrador desde báscula

- **Origen:** F2 §1 PA-14 · F4 C-08 · F1 H-072 (propuesta del desarrollador en la visita)
- **Propuesta:** La orden de cargue debe soportar las tres modalidades de salida del legacy: por tiquete de entrada, global (difieren en el firmante de la guía; la global puede reunir varios tiquetes de ingreso del depósito) y por número de depósito. Para el camión que llega a cargar sin orden: pasa por báscula, donde se crea la orden en borrador; luego carga, y cuando el cliente ya sabe qué carga le pasa la orden a Comercio Exterior. Tener en cuenta cómo el legacy muestra cantidades y saldos al generar la guía.
- **Para la fase 2:** evaluar si en todos los escenarios sigue siendo útil generar primero la orden y después la guía.
- **Relaciona:** H-017, H-042, H-055, H-072, D-23, OV-05, PR-17, PR-22

#### PR-22 – Rediseño de la vista de crear orden de cargue

- **Origen:** F4 C-16
- **Propuesta:** Rediseñar `/foreign-trade/loading-orders/create`. La propuesta de diseño depende del análisis funcional, que determinará cómo se manejan las salidas.
- **Relaciona:** H-045, PR-21, PR-27

#### PR-23 – Tasa de cambio manual, semanal y compartida

- **Origen:** F2 §1 PA-08, PA-24 · F4 C-15
- **Propuesta:** Usar la tasa manual como en el legacy: se configura cada lunes, se precarga en el levante con la de la semana y se puede cambiar por la de la semana que corresponda. Facturación sigue la misma lógica, con la misma tasa.
- **Relaciona:** H-034, H-077, D-22, OV-02

### 8.4. Facturación

#### PR-24 – Montacargas: switch «Requiere factura»

- **Origen:** F2 §1 PA-16
- **Propuesta:** En el modal «Facturación y cobro – Montacargas», cambiar el check «Agregar IVA (19 %)» por un switch «Requiere factura». Si requiere factura, se agrega el IVA y el modo de pago es «Pendiente por facturar»; si no, no hay IVA y el modo de pago es «Inmediato». En `/billing/invoices`, para montacargas, el número de factura muestra «Pendiente de número» (se emite la factura y se agrega el número SIGO como hoy) o «No aplica» (no se genera factura; es solo un registro de la operación).
- **Relaciona:** H-051, H-052

#### PR-25 – Carga de las fórmulas de los acuerdos desde el Excel de convenios

- **Origen:** F2 §1 PA-21
- **Propuesta:** Con el Excel de facturación, buscar una mejor alternativa para cargar las fórmulas de los acuerdos y a qué aplican, en lugar del flujo actual de agregar servicios al acuerdo.
- **Relaciona:** H-063, H-066, H-070, H-071, H-086, PR-28

### 8.5. Transversales e interfaz general

#### PR-26 – Destinatarios de notificaciones por rol

- **Origen:** F2 §1 PA-25, §2 Bodega
- **Propuesta:** El administrador configura los destinatarios por rol de las notificaciones existentes, incluida la alerta de retraso de bodega.
- **Relaciona:** H-073, H-078, PR-14

#### PR-27 – Selectores paginados con buscador

- **Origen:** F2 §2 Comercio Exterior
- **Propuesta:** Regla general: todo selector que traiga listas grandes de la base de datos debe estar paginado y tener buscador.
- **Relaciona:** H-013, H-045, PR-06, PR-22

#### PR-28 – Rediseño del menú y nuevas secciones

- **Origen:** F2 §4 Ajustes generales · **Alcance:** todos los módulos
- **Propuesta:** El control de acceso sigue por roles, con el menú y las páginas rediseñados:
  - El administrador accede a todos los módulos; «Usuarios» y «Auditoría» son exclusivos de administración.
  - Nueva sección «Configuración»: CRUD de terceros, productos, servicios, conductores, vehículos, motivos de entrada, ubicaciones, ciudades y cuadrillas, **sin precios ni tarifas**. Los acuerdos ya no se manejan en el detalle del tercero ni las tarifas base en el detalle del servicio. Acceso: administrador, Comercio Exterior y Facturación.
  - Nueva sección «Tarifas y acuerdos»: acuerdos de los terceros, tarifas de los servicios y todo lo relacionado con tarifas. Acceso: Facturación y administrador.
  - Los ítems con submenú «Listado» y «Crear» (como «Usuarios») quedan en un solo nivel: el ítem lleva al listado y se crea desde el botón del listado. Aplica a todos los ítems con esa configuración.
  - Reorganizar el menú para que sea más legible y fácil de usar.
- **Relaciona:** H-025, H-029, H-032, H-063, H-079, H-083, H-086, PR-02, PR-25

#### PR-29 – Páginas de listado con tabla CRUD y filtros por columna

- **Origen:** F2 §4 Ajustes generales · **Referencias:** RV-04, RV-05, RV-06 · **Alcance:** todos los módulos
- **Propuesta:** Quitar la card de título y subtítulo y dejar la tabla como elemento principal, con la tabla CRUD de PrimeVue (crear y exportar en la parte superior de la misma card). Filtros por columna al estilo PrimeVue y orden en las columnas principales; si el endpoint es paginado, el orden se hace en el backend. Si hacen falta filtros u opciones globales, una card encima de la tabla con el diseño de referencia. Uniforme en toda la aplicación. Las acciones se ejecutan solo con botones, no con clic en la fila.
- **Relaciona:** H-004, H-007, H-047, H-048, H-083, PR-05

#### PR-30 – CRUD y detalle en modales o drawers

- **Origen:** F2 §4 Ajustes generales
- **Propuesta:** Dentro de lo posible, los CRUD básicos y el detalle de un registro se manejan en la página principal con modales o drawers, para no navegar entre páginas.
- **Relaciona:** H-083, PR-28, PR-29

#### PR-31 – Ver contraseña en el login

- **Origen:** F2 §4 Ajustes generales
- **Propuesta:** Agregar el botón de ver contraseña en el input de contraseña del login.

#### PR-32 – Optimizar el espacio vertical del ticket impreso

- **Origen:** F2 §1 PA-07
- **Propuesta:** En el ticket impreso «se podría optimizar el espacio» vertical.
- **Relaciona:** H-023, H-085

## 9. Inventario de mockups y referencias visuales

Rutas relativas a `code_workspace/`. La carpeta `docs/levantamiento_staging/` está excluida de git.

### 9.1. Mockups

Los mockups se hicieron con IA. Los estilos, fuentes y colores son solo referencia y se adaptan al diseño y tema de la aplicación.

| ID | Mockup | Archivos | Qué representa | Qué se toma de él según F2 | Relaciona |
|---|---|---|---|---|---|
| MK-01 | Formulario de registro de báscula | [`docs/levantamiento_staging/mockups/modelo_bascula/`](../levantamiento_staging/mockups/modelo_bascula/) (`screen.png`, `code.html`) | Página de pesaje con pasos Registro/Cobro/Tiquete, secciones Vigilancia, Camión y conductor, Registro de operación, Pesaje en báscula (2×2) y Datos para Comercio Exterior, y botones «Guardar sin pesaje» y «Guardar (Pesar y continuar)» | Idea del formulario; estilos solo de referencia. La sección «Datos para Comercio Exterior» se quita de báscula (C-11) | PR-01, PR-03 |
| MK-02 | Tabla de depósitos de importación | [`docs/levantamiento_staging/mockups/tabla_dep_importacion/`](../levantamiento_staging/mockups/tabla_dep_importacion/) (`screen.png`, `code.html`, `DESIGN.md`) | Tabla maestro-detalle de depósitos con fila expandida de vehículos y totales | Columnas, estructura y patrón maestro-detalle, y la presentación de los datos. Botones de acción y filtros son referencia | PR-16 |
| MK-03 | Detalle del depósito de importación | [`docs/levantamiento_staging/mockups/detalle_deposito/`](../levantamiento_staging/mockups/detalle_deposito/) (`screen.png`, `code.html`, `DESIGN.md`) | Detalle con stepper de seis etapas, información general y progreso | Exactamente: stepper, disposición de botones y etiquetas del encabezado, información general y progreso. El contenido de cada etapa es referencia | PR-17 |
| MK-04 | Levantes en el detalle del depósito (Vista 1) | [`docs/levantamiento_staging/mockups/levantes/levante_detalle_deposito/`](../levantamiento_staging/mockups/levantes/levante_detalle_deposito/) (captura PNG, `Main.dc.html`) | Pestaña de levantes con resumen en tarjetas, alerta de diferencia de peso y tabla agrupada por mercancía con fila editable | Patrones, estructura y columnas de las tablas | PR-19 |
| MK-05 | Depósitos y levantes, maestro-detalle (Vista 2) | [`docs/levantamiento_staging/mockups/levantes/levantes_vista_general/`](../levantamiento_staging/mockups/levantes/levantes_vista_general/) (captura PNG, `Maestro.dc.html`) | Vista general de depósitos con su avance de nacionalización y levantes en la fila expandida | Vista aparte (C-07) | PR-19 |
| MK-06 | Especificación de la vista de levantes | [`docs/levantamiento_staging/mockups/levantes/README.md`](../levantamiento_staging/mockups/levantes/README.md) | Descripción de columnas y bloques de MK-04 y MK-05 | Explicación del diseño | PR-19 |

### 9.2. Imágenes y videos

| ID | Referencia | Archivo | Qué muestra | Relaciona |
|---|---|---|---|---|
| RV-01 | Formulario legacy de edición de pesos | [`docs/levantamiento_staging/edicion_pesos.png`](../levantamiento_staging/edicion_pesos.png) | «Modificar entrada a báscula»: vehículo, unidad de carga, conductor, modalidad, documento, pesaje (P. indicador, T. vehículo, P. manifiesto, P. mercancía), productos, precio y moneda, convenio, valor, IVA y «Facturar a» | H-008, H-041, PA-02, PR-11 |
| RV-02 | Formulario legacy de registro de levante | [`docs/levantamiento_staging/registro_levante_formulario.png`](../levantamiento_staging/registro_levante_formulario.png) | Matriz Ingreso / Nacionalizados / Saldo con columna por producto; tasa de cambio, CIF USD, peso bruto, Nº levante, Nº aceptación, fecha y FOB CO | H-036, H-038, PA-09, PA-11 |
| RV-03 | Sidebar con varios roles | [`docs/levantamiento_staging/detalle_multiroles_usuario.png`](../levantamiento_staging/detalle_multiroles_usuario.png) | Detalle de usuario y roles apretados, avatar cortado | H-079 |
| RV-04 | Tabla CRUD de PrimeVue | [`docs/levantamiento_staging/tabla_crud.png`](../levantamiento_staging/tabla_crud.png) | Tabla con barra superior (New, Delete, Export), búsqueda, orden por columna y acciones por fila | PR-29 |
| RV-05 | Filtros por columna | [`docs/levantamiento_staging/estilo_filtros.png`](../levantamiento_staging/estilo_filtros.png) · [PrimeVue DataTable – Filter](https://primevue.dev/datatable/#filter) | Fila de filtros bajo los encabezados | PR-29 |
| RV-06 | Panel de filtros globales | [`docs/levantamiento_staging/panel_filtros.png`](../levantamiento_staging/panel_filtros.png) | Card tipo toolbar encima de la tabla | PR-29 |
| RV-07 | Video «Levante y salida global» | `levante_y_salida_global.MOV` (fuera del repo); lectura en F3, video 1 | Levante con cálculo automático y salida global con dos tiquetes | OV-01 a OV-05, OV-11, H-039, H-042 |
| RV-08 | Video «Edición de pesos y levante» | `proceso_levante_edicion_pesos.mov` (fuera del repo); lectura en F3, video 2 | Edición de pesos del tiquete, datos del depósito, amparados y levante | OV-06 a OV-10, H-041 |

**Otras referencias citadas por F2:** [PrimeVue FloatLabel](https://primevue.dev/floatlabel/) (variante `on`, PR-01) · [PrimeVue DataTable – Row expansion](https://primevue.dev/datatable/#row-expansion) (PR-16) · Excel de convenios y precios [`docs/levantamiento_staging/CONVENIO 23-24-25-26.xlsx`](<../levantamiento_staging/CONVENIO 23-24-25-26.xlsx>) (H-070, PR-25) · sistema legacy en local (`http://localhost:8085`; las credenciales están en F2 §3 y no se copian aquí).

## 10. Pendientes de aclaración

### 10.1. Resultado de los 25 puntos de la primera consolidación

| PA | Hallazgo | Cruce inicial con F2 | Resolución | Estado |
|---|---|---|---|---|
| PA-01 | H-001 | Parcial («por confirmar comercio exterior») | Documentos y producto opcionales, descripción obligatoria, cobro fijo por vehículo como importación; confirmado con los operarios (C-14) | Cerrado |
| PA-02 | H-008 | Parcial | Causa de la tara incorrecta y edición de la T. vehículo por Comercio Exterior; cifras del audio cerradas sin más información (C-16) | Cerrado |
| PA-03 | H-009 | Explícita | Forma de trabajo; el sistema ya lo permite; capacitación | Cerrado |
| PA-04 | H-011 | Parcial | Autocompletado al digitar la carta porte; la v2 muestra borrador y confirmado (C-17) | Cerrado |
| PA-05 | H-018 | Contradicción con F2 §4 | Se refiere al embalaje; la unidad de medida se propone quitar (C-04) | Cerrado |
| PA-06 | H-022 | Explícita (propuesta) | Vistas separadas: PR-05 | Cerrado |
| PA-07 | H-023 | Explícita | Funcionó; observación del espacio del ticket (H-085, PR-32) | Cerrado |
| PA-08 | H-034 | Explícita | Tasa semanal precargada y editable por la de la semana correspondiente | Cerrado |
| PA-09 | H-036 | Parcial | «Cuadrito» = modal sin scroll; la propuesta es el mockup de levantes (C-06) | Cerrado |
| PA-10 | H-037 | Parcial | Mismo dato; etiqueta «Valor en aduanas»; FOB CO = CIF USD × tasa (OV-11) | Cerrado |
| PA-11 | H-038 | Explícita | Quitar la fecha de aceptación; se conserva el número de aceptación | Cerrado |
| PA-12 | H-039 | Explícita | La v2 no calcula; debe ser como el legacy | Cerrado |
| PA-13 | H-041 | Explícita | Comercio exterior edita cualquier peso para cuadrar con los documentos | Cerrado |
| PA-14 | H-042 | Parcial | Tres modalidades descritas; orden en borrador desde báscula (C-08); evaluación para la fase 2 | Cerrado (con tema para la fase 2) |
| PA-15 | H-043 | Parcial («confirmar formato») | Contenido del reporte definido; formato a la fase 2 (C-18) | Cerrado (con tema para la fase 2) |
| PA-16 | H-051 | Explícita (propuesta) | PR-24; columna IVA Sí/No reemplazada (C-16) | Cerrado |
| PA-17 | H-052 | Parcial | Lo genera facturación, con dos columnas; numeración cerrada (C-16) | Cerrado |
| PA-18 | H-053 | Ambigua | Funciona bien y ya acepta decimales (C-12) | Cerrado |
| PA-19 | H-055 | Sin resolver (remite a PA-14) | Ticket / orden de cargue pasa a la fase 2 con PR-21 | **Pendiente (parcial)** |
| PA-20 | H-060 | Explícita | Todos los pagos verificados; almacenamiento ya funciona así | Cerrado |
| PA-21 | H-063 | Explícita | Ubicación del simulador y comportamiento; H-086 y PR-25 | Cerrado |
| PA-22 | H-074 | Explícita | Edición como en el legacy, también por báscula; báscula no tenía la opción | Cerrado |
| PA-23 | H-076 | Contradicción con F1 | Opcional en bodega, se quita de báscula (C-05) | Cerrado |
| PA-24 | H-077 | Explícita | Tasa manual como el legacy, compartida con facturación (C-15) | Cerrado |
| PA-25 | H-078 | Explícita (propuesta) | PR-26; H-078 pasa a transversal | Cerrado |

### 10.2. Pendiente abierto

| Punto | Hallazgo | Qué falta | Origen |
|---|---|---|---|
| PA-19 | H-055 – Información y búsqueda en las facturas de guías de salida | Si en las facturas de guías de salida deben aparecer la **mercancía y el embalaje**. Lo demás (si el número de orden de cargue reemplaza al ticket con que los clientes piden la factura) depende de las modalidades de salida (PR-21) y se trata en la fase 2 | F2 §1 PA-19 · F4 C-16 |

No quedan contradicciones abiertas entre las fuentes. Las diferencias entre textos y mockups se documentan en las propuestas (PR-01, PR-15, PR-19) y en la sección 12.

## 11. Matriz general de trazabilidad

Abreviaturas de tipo: **HO** hallazgo reportado por operarios · **AC** aclaración · **OR** observación de revisión · **DV** diferencia entre versiones · **PR** propuesta de cambio · **RV** referencia visual. Estados: **C** consolidado (en las filas PA: punto cerrado) · **CA** consolidado con aclaración · **CSC** cerrado sin cambio · **COR** corregido · **PEN** pendiente de aclaración · **PNA** propuesta no aprobada · **DOC** documentado. Fuentes: F1 a F4 y Ref. según la sección 2.

| ID | Módulo | Tipo de información | Descripción | Fuente | Estado documental | Referencias |
|---|---|---|---|---|---|---|
| H-001 | Báscula | HO + AC | Inspecciones: solo pesaje, sin documentos | F1, F2 PA-01, F4 C-14 | CA | D-01, PR-07, PR-20 |
| H-002 | Báscula | HO | Cerrar ciclo sin segundo pesaje o agregarlo | F1, F2 §4 | CA | PR-01, H-084 |
| H-003 | Báscula | HO | Columnas de báscula iguales a entradas del legacy | F1, F2 §4 | CA | D-03, PR-05 |
| H-004 | Báscula | HO | Clic en la fila abre el registro | F1, F2 §4 | CA | PR-29 |
| H-005 | Báscula | HO | Imprimir ticket sin repesaje | F1 | C | D-02 |
| H-006 | Báscula | HO | Ticket sin producto, embalaje ni cantidad | F1 | C | H-085 |
| H-007 | Báscula | HO | Orden de tickets del más reciente al más antiguo | F1 | C | PR-29 |
| H-008 | Báscula | HO + AC | Tara de vehículos que no descargan | F1, F2 PA-02, F3, F4 C-16 | CA | D-12, PR-11, RV-01 |
| H-009 | Báscula | HO + AC | Ingreso sin peso editado después | F1, F2 PA-03 | CSC | PR-03 |
| H-010 | Báscula | HO | Eliminación de tickets | F1 | C | D-04 |
| H-011 | Báscula | HO + AC | Coincidencias de carta porte al digitar | F1, F2 PA-04, F4 C-17, Ref. | CA | D-05, PR-27 |
| H-012 | Báscula | HO | Edición de fecha y hora de ingreso | F1, F2 §4 | CA | PR-01 |
| H-013 | Báscula | HO | Buscar empresa de transporte por documento | F1 | C | PR-27 |
| H-014 | Báscula | HO | Conductores con el mismo documento | F1 | C | D-06 |
| H-015 | Báscula | HO | Manifiesto obligatorio solo con carta porte | F1 | C | PR-01 |
| H-016 | Báscula | HO | Carta porte por defecto | F1 | C | — |
| H-017 | Báscula | HO | Salida: placa de vigilancia y orden precargada | F1, F2 §4 | CA | PR-01, PR-21 |
| H-018 | Báscula | HO + AC | Unidad no editable al agregar producto | F1, F2 PA-05, F4 C-04 | CA | PR-12 |
| H-019 | Báscula | HO | Paso 2: mostrar y editar el paso 1 | F1, F2 §4 | CA | PR-01 |
| H-020 | Báscula | HO | Conductor en el paso de cobro | F1 | C | PR-01 |
| H-021 | Báscula | HO | Camiones con más de una mercancía | F1 | C | D-07 |
| H-022 | Báscula | HO + PR | Historial único frente a vistas separadas | F1, F2 PA-06 | CA | D-08, PR-05 |
| H-023 | Báscula | HO + AC | Impresión del ticket mediante descarga | F1, F2 PA-07 | CSC | H-085, PR-32 |
| H-024 | Bodega | HO | Ingreso duplicado con más de un producto | F1 | C | H-021 |
| H-025 | Bodega | HO | Cuadrilla al ejecutar el cargue | F1, F2 §4 | C | PR-28 |
| H-026 | Comercio Exterior | HO | Vistas de entradas, salidas y solo pesaje | F1, F2 §4, F3 | CA | D-03, D-13, PR-18 |
| H-027 | Comercio Exterior | HO | Tarjetas frente a tabla de depósitos | F1, F2 §4 | CA | D-14, PR-15, PR-16, PR-17 |
| H-028 | Comercio Exterior | HO | Editar fecha de llegada y manifiesto | F1, F2 §4, F3 | CA | D-15, PR-17, OV-09 |
| H-029 | Comercio Exterior | HO | Crear terceros desde el depósito | F1, F2 §4 | C | PR-17, PR-28 |
| H-030 | Comercio Exterior | HO | Editar la sección de transporte | F1 | C | PR-17 |
| H-031 | Comercio Exterior | HO | Editar productos tras confirmar | F1, F2 §4, F3 | CA | D-16, PR-17, OV-10 |
| H-032 | Comercio Exterior | HO + AC | Crear productos desde el modal | F1, F2 §2 | COR | PR-28 |
| H-033 | Comercio Exterior | HO | Embalaje junto al nombre del producto | F1, F4 C-04 | CA | PR-12 |
| H-034 | Comercio Exterior | HO + AC | Tasa de cambio manual en los levantes | F1, F2 PA-08, F3, F4 C-15 | CA | D-22, PR-23, OV-02 |
| H-035 | Comercio Exterior | HO | Prefijos de levante, aceptación y manifiesto | F1 | C | D-17 |
| H-036 | Comercio Exterior | HO + AC | Interfaz de levantes como el legacy | F1, F2 PA-09, F3, F4 C-06 | CA | D-18, PR-19, RV-02, MK-04 |
| H-037 | Comercio Exterior | HO + AC | Valor CIF / valor en aduanas | F1, F2 PA-10, F3 | CA | OV-11, PR-19 |
| H-038 | Comercio Exterior | HO + AC | Datos de aceptación en levantes | F1, F2 PA-11, F3 | CA | D-20, OV-03, RV-02 |
| H-039 | Comercio Exterior | HO + AC | Cálculo automático de cantidad | F1, F2 PA-12, F3 | CA | D-19, OV-01, RV-07 |
| H-040 | Comercio Exterior | HO | Levantes sucesivos hasta cero | F1, F2 §4 | CA | D-21, PR-19 |
| H-041 | Comercio Exterior | HO + AC | Edición de pesos y tickets de ingreso | F1, F2 PA-13, F3 | CA | D-12, D-13, PR-11, PR-18, RV-08 |
| H-042 | Comercio Exterior | HO + AC | Modalidades de salida | F1, F2 PA-14, F3, F4 C-08 | CA | D-23, PR-21, OV-05 |
| H-043 | Comercio Exterior | HO + AC | Inventario de mercancía nacionalizada | F1, F2 PA-15, F4 C-18 | CA | Secc. 12 |
| H-044 | Comercio Exterior | HO | Pruebas detenidas en levantes | F1 | C | H-039 |
| H-045 | Comercio Exterior | HO + OR | Selectores lentos en la orden de cargue | F1, F2 §2 | CA | PR-22, PR-27 |
| H-046 | Facturación | HO | Editar el número SIGO | F1 | C | — |
| H-047 | Facturación | HO | Información de báscula en facturas | F1 | C | D-03, PR-29 |
| H-048 | Facturación | HO | Filtros de búsqueda en facturas | F1 | C | D-24, PR-29 |
| H-049 | Facturación | HO | Reportes en PDF con suma | F1 | C | H-050 |
| H-050 | Facturación | HO | Separar contado y por cobrar | F1 | C | H-049 |
| H-051 | Facturación | HO + PR | Montacargas: qué requiere factura | F1, F2 PA-16, F4 C-16 | CA | PR-24 |
| H-052 | Facturación | HO + AC | Reporte de montacargas | F1, F2 PA-17, F4 C-16 | CA | PR-24 |
| H-053 | Facturación | HO + AC | Registro del horómetro | F1, F2 PA-18, F4 C-12 | CSC | — |
| H-054 | Facturación | HO | Destinatario de guías sin «cliente» | F1 | C | H-069 |
| H-055 | Facturación | HO + AC | Información y búsqueda en facturas de guías | F1, F2 PA-19, F4 C-16 | PEN | D-25, PR-21 |
| H-056 | Facturación | HO | Ciclo de facturación abierto | F1 | C | PR-25 |
| H-057 | Facturación | HO | Conteo de los periodos | F1 | C | — |
| H-058 | Facturación | HO | Pendientes por facturar: solo cumplidos | F1 | C | D-26 |
| H-059 | Facturación | HO | Facturación por CPI con valor de mercancía | F1 | C | — |
| H-060 | Facturación | HO + AC | Estado de los pagos | F1, F2 PA-20 | CA | — |
| H-061 | Facturación | HO | Reporte anual con detalle | F1 | C | — |
| H-062 | Facturación | HO | Informe de póliza | F1 | C | — |
| H-063 | Facturación | HO + AC | Simulador de fórmula | F1, F2 PA-21 | CA | H-086, PR-25 |
| H-064 | Facturación | HO | Destinatario de facturas y bloqueo | F1 | C | H-069 |
| H-065 | Facturación | HO | Registro rápido del pago completo | F1 | C | — |
| H-066 | Facturación | HO | Factura con valor incorrecto en prueba | F1 | C | H-070 |
| H-067 | Facturación | HO | Comprensión del flujo de facturas | F1 | C | D-27 |
| H-068 | Facturación | HO | El documento de báscula no es factura | F1 | C | — |
| H-069 | Transversal | HO | Cliente frente a responsable | F1 | C | H-070 |
| H-070 | Transversal | HO | Excel de convenios como fuente | F1, F2 PA-21, §3 | CA | PR-25 |
| H-071 | Transversal | HO + AC | Responsable desconocido al ingreso | F1, F2 §2 | CA | PR-25 |
| H-072 | Transversal | HO + AC | Vehículos que llegan sin orden de cargue | F1, F2 PA-14, F4 C-08 | CA | D-23, PR-21 |
| H-073 | Transversal | HO + AC | Bloqueo de báscula por bodega | F1, F2 §2, §4 | CA | PR-09, PR-14, PR-26 |
| H-074 | Transversal | HO + AC | Corrección de datos del ingreso | F1, F2 PA-22 | CA | D-11, PR-11 |
| H-075 | Transversal | HO | Edición de la placa desde báscula | F1, F2 §4 | CA | PR-01, PR-02 |
| H-076 | Transversal | HO + PR | Tipo de vehículo | F1, F2 PA-23, F4 C-05 | CA | PR-10 |
| H-077 | Transversal | HO + AC | Origen de la tasa de cambio | F1, F2 PA-24, F4 C-15 | CA | D-22, PR-23 |
| H-078 | Transversal (Administración) | HO + PR | Destinatarios de notificaciones | F1, F2 PA-25 | CA | PR-26 |
| H-079 | Transversal (Interfaz) | OR | Sidebar con varios roles | F2 §4 | DOC | RV-03 |
| H-080 | Transversal (Interfaz) | OR | Switch de tema | F2 §4 | DOC | — |
| H-081 | Transversal (Interfaz) | OR | Header de modal tapa alertas | F2 §4 | DOC | — |
| H-082 | Facturación | OR | Tabla de pending-deposits sin tema oscuro | F2 §4 | DOC | H-058 |
| H-083 | Transversal (Interfaz) | OR | Menú denso y listados con cards | F2 §4 | DOC | PR-28, PR-29 |
| H-084 | Báscula | HO | Editar tras terminar el ciclo | F2 §4 | C | D-10, PR-11 |
| H-085 | Báscula | OR | Espacio sobrante en el ticket impreso | F2 PA-07 | DOC | PR-32 |
| H-086 | Facturación | OR | Configurar acuerdos es difícil y lento | F2 PA-21 | DOC | PR-25 |
| PA-01 | Báscula | AC | Depósito de inspección | F2 §1, F4 C-14 | C | H-001 |
| PA-02 | Báscula | AC | Tara y edición de T. vehículo | F2 §1, F4 C-16 | C | H-008 |
| PA-03 | Báscula | AC | Ingreso sin peso: forma de trabajo | F2 §1 | C | H-009 |
| PA-04 | Báscula | AC | Autocompletado de carta porte | F2 §1, F4 C-17 | C | H-011 |
| PA-05 | Báscula | AC | Uso del embalaje | F2 §1, F4 C-04 | C | H-018 |
| PA-06 | Báscula | PR | Historial en vistas separadas | F2 §1 | C | H-022, PR-05 |
| PA-07 | Báscula | AC | Impresión funcionó | F2 §1 | C | H-023 |
| PA-08 | Comercio Exterior | AC | Tasa semanal en el levante | F2 §1 | C | H-034 |
| PA-09 | Comercio Exterior | AC | Modal sin scroll; columnas o select | F2 §1, F4 C-06 | C | H-036 |
| PA-10 | Comercio Exterior | AC | CIF = valor en aduanas | F2 §1, F3 | C | H-037 |
| PA-11 | Comercio Exterior | AC | Solo fecha del levante | F2 §1 | C | H-038 |
| PA-12 | Comercio Exterior | AC | La v2 no calcula cantidades | F2 §1 | C | H-039 |
| PA-13 | Comercio Exterior | AC | Comercio exterior edita cualquier peso | F2 §1 | C | H-041 |
| PA-14 | Comercio Exterior | AC | Tres modalidades de salida | F2 §1, F4 C-08 | C | H-042, PR-21 |
| PA-15 | Comercio Exterior | AC | Contenido del inventario nacionalizado | F2 §1, F4 C-18 | C | H-043 |
| PA-16 | Facturación | PR | Switch «Requiere factura» | F2 §1, F4 C-16 | C | H-051, PR-24 |
| PA-17 | Facturación | AC | Reporte de montacargas | F2 §1, F4 C-16 | C | H-052 |
| PA-18 | Facturación | AC | Horómetro con decimales | F2 §1, F4 C-12 | C | H-053 |
| PA-19 | Facturación | AC | Remite a PA-14 | F2 §1, F4 C-16 | PEN | H-055 |
| PA-20 | Facturación | AC | Todos los pagos verificados | F2 §1 | C | H-060 |
| PA-21 | Facturación | AC | Ubicación del simulador | F2 §1 | C | H-063, H-086 |
| PA-22 | Transversal | AC | Edición de datos como el legacy | F2 §1 | C | H-074 |
| PA-23 | Transversal | AC + PR | Tipo de vehículo a bodega | F2 §1, F4 C-05 | C | H-076, PR-10 |
| PA-24 | Transversal | AC | Tasa manual compartida | F2 §1, F4 C-15 | C | H-077, PR-23 |
| PA-25 | Transversal | PR | Destinatarios por rol | F2 §1 | C | H-078, PR-26 |
| OV-01 | Comercio Exterior | OR | Levante calcula cantidad desde el peso | F3 | DOC | H-039, RV-07 |
| OV-02 | Comercio Exterior | OR | Tasa precargada y editable | F3 | DOC | H-034, RV-07 |
| OV-03 | Comercio Exterior | OR | Solo fecha del levante | F3 | DOC | H-038, RV-07 |
| OV-04 | Comercio Exterior | OR | Matriz con columna por producto | F3 | DOC | H-036, RV-07 |
| OV-05 | Comercio Exterior | OR | Salida global con dos tiquetes | F3 | DOC | H-042, RV-07 |
| OV-06 | Comercio Exterior | OR | Edición de pesos desde Tickets Ingresos | F3 | DOC | H-041, RV-08 |
| OV-07 | Comercio Exterior | OR | Mercancía digitada y tara recalculada | F3 | DOC | H-041, RV-08 |
| OV-08 | Comercio Exterior | OR | Cambios visibles en depósito y levante | F3 | DOC | H-041, RV-08 |
| OV-09 | Comercio Exterior | OR | Datos del depósito editables | F3 | DOC | H-028, RV-08 |
| OV-10 | Comercio Exterior | OR | Amparados registrados aparte | F3 | DOC | H-031, RV-08 |
| OV-11 | Comercio Exterior | OR | FOB CO = CIF USD × tasa | F3 | DOC | H-037, RV-07 |
| D-01 | Báscula | DV | Inspecciones sin o con depósito | F1 | DOC | H-001 |
| D-02 | Báscula | DV | Ticket sin repesaje | F1 | DOC | H-005 |
| D-03 | Transversal | DV | Columnas de entradas, salidas y solo pesaje | F1 | DOC | H-003, H-026, H-047 |
| D-04 | Báscula | DV | Eliminación de tickets | F1 | DOC | H-010 |
| D-05 | Báscula | DV | Coincidencias de carta porte | F1, F2, F4 | DOC | H-011 |
| D-06 | Báscula | DV | Conductores con el mismo documento | F1 | DOC | H-014 |
| D-07 | Báscula | DV | Camión con más de una mercancía | F1 | DOC | H-021 |
| D-08 | Báscula | DV | Historial de báscula | F1 | DOC | H-022 |
| D-09 | Báscula | DV | Repesajes múltiples | F2 §4 | DOC | PR-04 |
| D-10 | Báscula | DV | Edición tras terminar el ciclo | F2 §4 | DOC | H-084 |
| D-11 | Transversal | DV | Edición de datos del ingreso | F2 PA-22 | DOC | H-074 |
| D-12 | Comercio Exterior | DV | Edición de pesos del tiquete | F2, F3 | DOC | H-008, H-041 |
| D-13 | Comercio Exterior | DV | Lista de tiquetes de ingreso | F2, F3 | DOC | H-026, PR-18 |
| D-14 | Comercio Exterior | DV | Vista de depósitos | F1, F3 | DOC | H-027 |
| D-15 | Comercio Exterior | DV | Datos del depósito editables | F1, F3 | DOC | H-028 |
| D-16 | Comercio Exterior | DV | Productos tras confirmar | F1, F3 | DOC | H-031 |
| D-17 | Comercio Exterior | DV | Prefijos | F1 | DOC | H-035 |
| D-18 | Comercio Exterior | DV | Productos en el levante | F1, F2, F3 | DOC | H-036 |
| D-19 | Comercio Exterior | DV | Cálculo de cantidad del levante | F2, F3 | DOC | H-039 |
| D-20 | Comercio Exterior | DV | Datos de aceptación | F1, F2, F3 | DOC | H-038 |
| D-21 | Comercio Exterior | DV | Levantes sucesivos | F1 | DOC | H-040 |
| D-22 | Transversal | DV | Tasa de cambio | F1, F2, F3 | DOC | H-034, H-077 |
| D-23 | Transversal | DV | Salidas y orden de cargue | F1, F2, F3 | DOC | H-042, H-072 |
| D-24 | Facturación | DV | Búsqueda de facturas | F1 | DOC | H-048 |
| D-25 | Facturación | DV | Reporte de guías | F1 | DOC | H-055 |
| D-26 | Facturación | DV | Pendientes por facturar | F1 | DOC | H-058 |
| D-27 | Facturación | DV | Valor de la factura | F1 | DOC | H-067 |
| PR-01 | Báscula | PR | Formulario de registro como página | F2 §4, F4 C-11, C-13 | PNA | MK-01 |
| PR-02 | Báscula | PR | Motivo de ingreso con categoría | F2 §4 | PNA | H-075 |
| PR-03 | Báscula | PR | Guardar y Guardar sin pesaje | F2 §4 | PNA | MK-01, H-009 |
| PR-04 | Báscula | PR | Repesaje en modal | F2 §4 | PNA | D-09 |
| PR-05 | Báscula | PR | Historial en tres páginas | F2 PA-06, §4 | PNA | H-003, H-022 |
| PR-06 | Báscula | PR | Solo báscula sin peso esperado, con tercero | F2 §2 | PNA | PR-27 |
| PR-07 | Báscula | PR | Inspección con registro flexible | F2 PA-01, F4 C-14 | PNA | H-001 |
| PR-08 | Báscula | PR | Quitar «Soltar camión» | F2 §2 | PNA | — |
| PR-09 | Báscula | PR | Sin bloqueos de bodega en báscula | F2 §2 | PNA | H-073 |
| PR-10 | Bodega | PR | Tipo de vehículo en bodega, opcional | F2 PA-23, F4 C-05 | PNA | H-076 |
| PR-11 | Transversal | PR | Edición de datos y pesos como el legacy | F2 PA-02, PA-13, PA-22 | PNA | H-008, H-041, H-074 |
| PR-12 | Transversal | PR | Quitar la unidad de medida | F2 §4, F4 C-04 | PNA | H-018, H-033 |
| PR-13 | Bodega | PR | Montacargas desde recepciones | F2 §4 | PNA | PR-10 |
| PR-14 | Bodega | PR | Bodega no bloqueante con alertas | F2 §2, §4 | PNA | H-073 |
| PR-15 | Comercio Exterior | PR | Menú Depósitos por tipo con filtros | F2 §4 | PNA | H-027, MK-02 |
| PR-16 | Comercio Exterior | PR | Tabla de importación maestro-detalle | F2 §4 | PNA | MK-02 |
| PR-17 | Comercio Exterior | PR | Detalle del depósito por etapas | F2 §4, F4 C-09, C-11 | PNA | MK-03 |
| PR-18 | Comercio Exterior | PR | Tickets de ingreso en el menú | F2 §4 | PNA | H-026, H-041 |
| PR-19 | Comercio Exterior | PR | Levantes agrupados y vista general | F2 §4, F4 C-06, C-07 | PNA | MK-04, MK-05, MK-06 |
| PR-20 | Comercio Exterior | PR | Depósitos de exportación e inspección | F2 §4 | PNA | PR-17 |
| PR-21 | Transversal | PR | Tres modalidades de salida y orden en borrador | F2 PA-14, F4 C-08 | PNA | H-042, H-072 |
| PR-22 | Comercio Exterior | PR | Rediseño de crear orden de cargue | F4 C-16 | PNA | H-045, PR-21 |
| PR-23 | Transversal | PR | Tasa manual semanal compartida | F2 PA-08, PA-24, F4 C-15 | PNA | H-034, H-077 |
| PR-24 | Facturación | PR | Montacargas «Requiere factura» | F2 PA-16 | PNA | H-051 |
| PR-25 | Facturación | PR | Fórmulas de acuerdos desde el Excel | F2 PA-21 | PNA | H-063, H-070 |
| PR-26 | Transversal | PR | Notificaciones por rol | F2 PA-25, §2 | PNA | H-078 |
| PR-27 | Transversal | PR | Selectores paginados con buscador | F2 §2 | PNA | H-045 |
| PR-28 | Transversal | PR | Menú y secciones Configuración, Tarifas y acuerdos | F2 §4 | PNA | H-083 |
| PR-29 | Transversal | PR | Listados con tabla CRUD y filtros por columna | F2 §4 | PNA | RV-04, RV-05, RV-06 |
| PR-30 | Transversal | PR | CRUD y detalle en modales o drawers | F2 §4 | PNA | H-083 |
| PR-31 | Transversal | PR | Ver contraseña en el login | F2 §4 | PNA | — |
| PR-32 | Báscula | PR | Optimizar el espacio del ticket | F2 PA-07 | PNA | H-085 |
| MK-01 | Báscula | RV | Mockup del formulario de registro | F2 §4 | DOC | PR-01, PR-03 |
| MK-02 | Comercio Exterior | RV | Mockup de la tabla de importación | F2 §4 | DOC | PR-16 |
| MK-03 | Comercio Exterior | RV | Mockup del detalle del depósito | F2 §4 | DOC | PR-17 |
| MK-04 | Comercio Exterior | RV | Mockup de levantes en el detalle | F2 §4 | DOC | PR-19 |
| MK-05 | Comercio Exterior | RV | Mockup de depósitos y levantes | F2 §4, F4 C-07 | DOC | PR-19 |
| MK-06 | Comercio Exterior | RV | Especificación de la vista de levantes | F2 §4 | DOC | PR-19 |
| RV-01 | Comercio Exterior | RV | Formulario legacy de edición de pesos | F2 §1, §3 | DOC | H-008, H-041 |
| RV-02 | Comercio Exterior | RV | Formulario legacy de registro de levante | F2 §1, §3 | DOC | H-036, H-038 |
| RV-03 | Transversal (Interfaz) | RV | Sidebar con varios roles | F2 §4 | DOC | H-079 |
| RV-04 | Transversal (Interfaz) | RV | Tabla CRUD de PrimeVue | F2 §4 | DOC | PR-29 |
| RV-05 | Transversal (Interfaz) | RV | Filtros por columna | F2 §4 | DOC | PR-29 |
| RV-06 | Transversal (Interfaz) | RV | Panel de filtros globales | F2 §4 | DOC | PR-29 |
| RV-07 | Comercio Exterior | RV | Video de levante y salida global | F2 §3, F3 | DOC | OV-01 a OV-05, OV-11 |
| RV-08 | Comercio Exterior | RV | Video de edición de pesos y levante | F2 §3, F3 | DOC | OV-06 a OV-10 |

**Conteo de la matriz:** 86 hallazgos + 25 aclaraciones + 11 observaciones de video + 27 diferencias + 32 propuestas + 6 mockups + 8 referencias visuales = **195 filas**, igual al resumen de la sección 3.

## 12. Consideraciones para la fase 2

Temas que el análisis funcional deberá abordar. Aquí solo se identifican; no se analizan.

**Validaciones pedidas expresamente por el usuario.**

1. Viabilidad del formulario de registro de báscula (PR-01 a PR-03) y su reutilización en Comercio Exterior; informar incongruencias y ampliar con los hallazgos (nota de F2 §4 Báscula).
2. Por qué el legacy permite más de un repesaje y si hace falta en la v2 (PR-04, D-09).
3. Si en todos los escenarios de salida sigue siendo útil generar primero la orden de cargue y luego la guía, considerando las tres modalidades con el legacy como referencia (PR-21, H-042, H-072, C-08).
4. Diseño de la vista de crear orden de cargue, que depende de cómo se manejen las salidas (PR-22).

**Temas abiertos por las fuentes.**

5. En qué modalidades de salida se cobra báscula: la v1 registra «solo en depósito se cobra báscula» y PA-14 indica que tiquete y global salen sin pasar por báscula (H-042).
6. Relación entre número de ticket y número de orden de cargue en las facturas de guías, y el pendiente de mercancía y embalaje (PA-19, H-055).
7. Formato del inventario de mercancía nacionalizada que pide la DIAN (PA-15, H-043).
8. Límite de «editar la salida hasta cuando sea posible» (PR-17, etapa Salidas).
9. Etapas y campos de los depósitos de exportación e inspección (PR-20).
10. Alternativa para cargar convenios y fórmulas desde el Excel, y su relación con la sección «Tarifas y acuerdos» (PR-25, PR-28, H-070).
11. Tiempo límite y configuración de las alertas de bodega (PR-14, PR-26).
12. Alcance de los ajustes generales en todos los módulos: menú, listados, modales y drawers (PR-28 a PR-30).

**Diferencias entre textos y mockups documentadas sin resolver.**

13. Ubicación de «Guardar» en el formulario de báscula: encabezado (texto) o pie (MK-01) (PR-01).
14. Fecha de ingreso: el operario la pidió en el encabezado (H-012); la propuesta la deja en la sección Vigilancia (PR-01).
15. Filtros de la tabla de importación: «Todos / Pendientes / Facturados» (MK-02) o estados del depósito (texto de PR-15).
16. Etiqueta «CIF (USD)» en MK-04 y MK-05 frente a «Valor en aduanas» (PA-10).
17. Drawer aceptado en la visita frente a la tabla maestro-detalle propuesta (H-027).
18. Columnas pedidas para `/operations/weighbridge` (H-003) frente a las del historial propuesto (PR-05).

**Insumos disponibles.**

19. Lectura de los videos (F3); no hace falta volver a abrirlos.
20. Análisis de paridad del flujo de depósitos (Ref.): 46 diferencias, 12 brechas por impacto y decisiones pendientes que chocan con decisiones ya tomadas (P16, DEC-056, D19, DEC-010, DEC-057 D5). No se incorporó en esta fase (C-03).
21. Sistema legacy en local (F2 §3) y Excel de convenios con la hoja «Bascula» de precios base (F2 §3).
