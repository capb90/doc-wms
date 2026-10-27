# Fase 3 — Báscula (fase crítica)

> Lee antes `00-plan-maestro.md`. Rol principal: **Operario báscula** (`bascula`). Verificaciones con `c_exterior`, `bodega`, `facturacion` y Admin.
> **Es la puerta de entrada y el punto de congestión del negocio.** Se divide en sub-bloques con **mini-checkpoints**: si un bloque P0 falla con BLOCKER, el ejecutor se detiene ahí.

## 1. Objetivo

Validar el banco de trabajo de báscula de punta a punta: cola, tipos de operación, datos del camión y conductor, registro del ingreso con depósito, cobro, primer y segundo pesaje, neto, tiquete, estados, **persistencia y reingreso** a una operación, varios camiones por documento, unidades de carga, correcciones, salida de mercancía, solo báscula, historial y reportes, y la integración con Vigilancia, Bodega, Comercio Exterior y Facturación.

## 2. Alcance

| Pantalla | Ruta | Bloques |
|---|---|---|
| Banco de trabajo (cola + panel de proceso de 4 pasos) | `/operations/weighbridge[?cola=][?camion=]` | COL, CAM, REG, COB, PES, TIQ, REI, MCA, UCA, SAL, SBA, UX |
| Dashboard | `/operations/weighbridge/dashboard` | DSH |
| Recuperar operaciones | `/operations/weighbridge/recover` | REC |
| Historial (entradas y salidas) | `/operations/weighbridge/history` | HIS, COR |
| Detalle del ciclo | `/operations/weighbridge/cycles/[id]` | CIC, COR |
| Reporte de facturación diaria | `/operations/weighbridge/reports` | RPT |
| `in-process`, `pending-reweigh` | redirigen a `?cola=` | COL |

**Fuera:** confirmación del depósito (fase 5), facturas y su ciclo (fase 6), recepción (fase 4).

## 3. Criterios de entrada

1. Fases 1 y 2 aprobadas.
2. Ingresos abiertos de la fase 2 (§5) disponibles.
3. Tarifa BASCULA configurada (precio base y convenio de `QA Cliente Uno`).
4. `QA Cliente Mora` **bloqueado** para F3-COB-009. Si aún no lo está, el caso queda `BLOQUEADO` y se re-ejecuta en la fase 6 (o se prepara: ver fase 6, «Palancas de tiempo»).
5. Para el bloque SAL: una orden de cargue `Pending` para `QAB205` (ver «Preparación asistida»).

## 4. Modelo de la pantalla (para orientar al ejecutor)

- **Cola (`DEC-058`)** a todo el ancho, como tabla: Placa, Estado, Motivo, Cliente, Conductor, Modalidad, Documento, Primer peso (kg y tipo), Espera (en ámbar desde 60 min) y «Capturar peso» donde aplica. Filtros arriba con su conteo: «Todos», «Sin iniciar», «Por cobrar», «Por pesar», «Por repesar» (`?cola=`); sin paginador; refresco 15 s. La fila de un camión con datos sin guardar dice «En proceso». «Recuperar operaciones», con su contador, va en el encabezado de la página.
- **Panel de proceso (`DEC-058`):** clic o Enter en una fila abre el camión en un panel grande sobre la cola, con el fondo oscurecido y `?camion=` en la URL. No es una ventana que se cierre sola: **Esc no lo cierra**. Se cierra con «Volver a la cola», «Atrás» del navegador o Alt+N, y lo digitado se conserva. Encabezado: placa, motivo, hora de ingreso, la línea de progreso, los chips «Otros camiones en proceso» y, a la derecha, «Soltar camión», «Volver a la cola» y, en el registro, «Guardar». Debajo, los 4 pasos en línea: **Registro → Cobro → Peso → Tiquete**. El paso sale del estado del servidor. Enter ejecuta la acción del paso; F2 abre el peso en una ventana encima del panel; Esc cierra solo esa ventana.
- **Tipos de operación:** «Ingreso con depósito», «Salida de mercancía», «Solo báscula». Se preseleccionan por el motivo de Vigilancia y se pueden cambiar hasta que existe un servicio.
- **Card «Camión y conductor»**: transportadora, país del vehículo, tipo de vehículo, tipo y número de documento del conductor, apellidos y nombres son obligatorios para Guardar.
- **Documento (`DEC-057`):** al salir del número, si el número y el tipo ya tienen depósitos, aparece un selector con una tarjeta por depósito abierto (cliente, importador o exportador, agencia, transportadora, fecha del documento, placas y camiones) y «Es otro documento: crear depósito nuevo». Los cerrados y migrados se ven en gris y no se eligen. Con abiertos, «Guardar» espera la elección. «N.º de manifiesto» y «Peso según manifiesto (kg)» son obligatorios en el ingreso a depósito.
- **Panel plegado «Datos para Comercio Exterior»**: fecha del documento, cliente, importador, exportador (EXP), agencia, valor y moneda (opcionales en báscula).
- **Peso (`DEC-057`):** en el primer pesaje Bruto de un ingreso a depósito se ven P. indicador, P. manifiesto, T. vehículo y P. mercancía.
- **Panel plegado «Pesaje y observaciones»**: fecha de ingreso del depósito (WMS-33), primer pesaje Bruto/Tara, «Requiere segundo pesaje», «Flujo perecederos», observaciones.
- Estados del ciclo: `PendingPayment → ReadyForWeighing → FirstWeightCaptured → InProgress → Complete`; `Canceled` al anular.
- Consecutivos: tiquete `2026T00001`; depósitos `2026BA…` (IMP), `2026EXP…`, `2026INSP…`.

## 5. Preparación asistida

| Dato | Cómo prepararlo | Rol |
|---|---|---|
| Orden de cargue para `QAB205` | Requiere un depósito IMP **confirmado** y **nacionalizado**. Tras el bloque REG: CE asigna cliente y datos, confirma el depósito de `QAA101` (F5-CNF-001), registra un levante (F5-LEV-001) y crea una OC con vehículo `QAB205` (F5-OC-001). Si la fase 5 aún no se ejecutó, seguir esos pasos como preparación; si fallan, el bloque SAL queda `BLOQUEADO` y se re-ejecuta tras la fase 5. | `c_exterior` |
| Cliente bloqueado | Ver fase 6 §«Palancas de tiempo» o usar un cliente marcado `Blocked` por el job. | Admin (local) |

## 6. Casos

### 6.1 Cola y selección (COL)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F3-COL-001 | Cola inicial | Abrir el banco de trabajo. | Los ingresos con motivo de pesaje aparecen «Sin iniciar» con placa, motivo y tiempo de espera. | P0 | FUN |
| F3-COL-002 | Filtro por estado | Chips «Por cobrar», «Por pesar», «Por repesar»; abrir `/in-process` y `/pending-reweigh`. | La lista se filtra; las rutas viejas redirigen a `?cola=por-pesar` y `?cola=por-repesar`; los contadores coinciden. | P1 | FUN |
| F3-COL-003 | Refresco | Registrar un ingreso nuevo en Vigilancia (otra ventana). | Aparece en ≤ 15 s sin recargar. | P1 | INT |
| F3-COL-004 | Seleccionar camión | Clic en `QAA101`. | Se abre el panel de proceso con el tipo «Ingreso con depósito» y modalidad IMP preseleccionados (DF8). **Actualizado (`DEC-058`):** antes se abría la ficha a la derecha de la cola. | P0 | FUN |
| F3-COL-005 | Soltar camión | En el panel, «Soltar camión». | **Reescrito (`DEC-058`, B6 y B8):** el panel se cierra, el camión queda sin borrador (su fila ya no dice «En proceso») y el foco va a la primera fila «Sin iniciar» de la cola. | P2 | UX |
| F3-COL-006 | Espera larga | Un camión con > 60 min. | Espera en ámbar. | P3 | UI |
| F3-COL-007 | Atajo de captura | En una fila «Por pesar», botón «Capturar peso». | Abre el panel en el paso de peso. | P2 | UX |
| F3-COL-008 | Cola en tabla | Abrir el banco a 1366×768 y a 1920×1080 con camiones en los cuatro estados. | **Nuevo (`DEC-058`, B1–B3):** la cola ocupa todo el ancho, sin columna lateral; tabla con Placa en negrita, Estado, Motivo, Cliente, Conductor, Modalidad, Documento, Primer peso (kg y tipo), Espera y la columna Acciones con «Capturar peso» solo donde aplica; sin paginador; etiquetas de estado pequeñas y en una línea; sin scroll horizontal. Los filtros con su conteo van arriba de la tabla y conservan `?cola=`. | P1 | UI |
| F3-COL-009 | Abrir el panel | Clic en una fila. Cerrar con «Volver a la cola», recorrer las filas con las flechas y abrir otra con Enter. | **Nuevo (`DEC-058`, B4 y B7):** el camión se abre en un panel grande sobre la cola, con el fondo oscurecido y `?camion=` en la URL; la página de detrás no se desplaza; Tab no sale del panel hacia las filas de la cola. | P0 | FUN |
| F3-COL-010 | «Volver a la cola» conserva lo digitado | En `QAB201`, digitar parte del registro sin guardar → «Volver a la cola». Abrir otro camión; volver a `QAB201` con su chip «Otros camiones en proceso» y, otra vez, desde su fila. | **Nuevo (`DEC-058`, B6):** el panel se cierra sin soltar el camión; el foco queda en su fila, que dice «En proceso»; el chip y la fila lo reabren con lo digitado intacto. Complementa F3-REI-001. | P0 | PER |
| F3-COL-011 | Esc no cierra el panel | Con el panel abierto y ninguna ventana encima, pulsar Esc. | **Nuevo (`DEC-058`, B6):** el panel sigue abierto y no se pierde nada. | P1 | UX |
| F3-COL-012 | «Atrás» del navegador | Con el panel abierto y datos sin guardar, «Atrás» del navegador; después «Adelante». Abrir en otra pestaña la URL con `?camion=` de un camión de la cola y con la de un camión que ya salió. | **Nuevo (`DEC-058`, B7 y B9):** «Atrás» cierra el panel y vuelve a la cola, sin salir del módulo y con lo digitado intacto; «Adelante» lo reabre. Con `?camion=` de un camión de la cola se abre su panel; de uno que ya no está, aviso «Camión fuera de la cola» y la URL se limpia. Si el camión abierto sale de la cola mientras se trabaja, el panel sigue abierto. | P1 | UX |
| F3-COL-013 | F2 sobre el panel | En el paso de peso, F2; después Esc. Con el panel cerrado, F2. | **Nuevo (`DEC-058`, B4 y B8):** «Captura de peso» se abre encima del panel; Esc cierra solo esa ventana y el panel sigue abierto, con la página de detrás sin desplazarse. Con el panel cerrado, F2 no abre nada. | P0 | UX |
| F3-COL-014 | Encabezado mientras carga un camión | Con un camión abierto y datos sin guardar, cambiar a otro con su chip «Otros camiones en proceso» (en una red lenta, o con la herramienta del navegador que la simula). Repetir y, mientras carga, pulsar «Volver a la cola». | **Nuevo (validación `DEC-058`, R1):** mientras carga, el encabezado dice solo «Cargando el camión {placa}…», sin «Soltar camión», «Guardar» ni chips; «Volver a la cola» sigue. Al terminar aparece el camión nuevo con lo suyo, y el anterior conserva lo digitado («En proceso» en su fila). Si se volvió a la cola durante la carga, el panel queda cerrado, el foco en la fila del camión que cargaba y nada se suelta. | P1 | PER |
| F3-COL-015 | Teclas con el foco en una fila | «Volver a la cola» (el foco queda en la fila). Probar ↓ ↑, Inicio y Fin; Enter y Espacio; luego F5, Alt+← (Cmd+[ en Mac), Ctrl+F (Cmd+F) y AvPág. | **Nuevo (validación `DEC-058`, R2):** ↓ ↑ recorren las filas, Inicio y Fin van a la primera y la última, y Enter o Espacio abren el camión. Las teclas del navegador funcionan: F5 recarga, Alt+← vuelve, Ctrl+F abre la búsqueda y AvPág desplaza. Tab entra a la tabla por una sola fila (la del camión elegido o la primera). Enter sobre «Capturar peso» abre el peso, no la fila. | P1 | UX |
| F3-COL-016 | El foco no sale del panel | Con el panel abierto en el registro, Tab repetido desde el último campo; Mayús+Tab repetido desde el primer control del encabezado. Después, F2. | **Nuevo (validación `DEC-058`, R3):** Tab desde el último control vuelve al primero del encabezado, y Mayús+Tab desde el primero va al último; el foco nunca llega a la barra superior, al menú ni a «Recuperar operaciones». F2 sigue abriendo «Captura de peso» encima, con su propio foco. | P1 | UX |
| F3-COL-017 | F5 con el panel abierto | Abrir un camión desde la cola, F5, y después «Atrás» dos veces. Repetir con la dirección `?camion=` de un camión que ya salió de la cola. | **Nuevo (validación `DEC-058`, R4):** F5 reabre el panel del mismo camión. El primer «Atrás» vuelve a la cola y el segundo sale del módulo, sin entradas repetidas de la cola en el historial. Con un camión fuera de la cola: aviso «Camión fuera de la cola», la URL vuelve a la cola y un «Atrás» sale del módulo. | P2 | UX |
| F3-COL-018 | «Atrás» con una ventana abierta | En el registro, abrir «Crear tercero» (el «+» de un selector de tercero) y pulsar «Atrás» del navegador. Cerrar la ventana y pulsar «Atrás» otra vez. Repetir con F2 abierto. | **Nuevo (validación `DEC-058`, R5):** con la ventana abierta, «Atrás» no cierra el panel: el panel y la ventana siguen, y `?camion=` vuelve a la URL. Cerrada la ventana, «Atrás» cierra el panel como siempre. Con F2: primero se cierra F2 (Esc o su botón). Alt+N y Alt+K no actúan con una ventana abierta. | P2 | UX |

### 6.2 Camión y conductor (CAM)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F3-CAM-001 | Precarga del vehículo | Con `QAA101` (tiene tipo y transportadora). | Tipo de vehículo y transportadora precargados; marca «precargado». | P1 | FUN |
| F3-CAM-002 | Vehículo sin datos | Con `QAB201` (creado en Vigilancia sin datos). | Campos vacíos; «Faltan N datos». | P1 | FUN |
| F3-CAM-003 | Obligatorios | Con un camión sin transportadora, país, tipo de vehículo ni conductor (selector vacío) → «Guardar». | No guarda. «Faltan N datos» cuenta el conductor como **un solo** faltante, «conductor» (no cuatro campos), y el foco va al primer faltante; si solo falta el conductor, al select (`#driverId [role='combobox']`). | P0 | VAL |
| F3-CAM-004 | Conductor existente | Tab al select «Conductor» → escribir parte del nombre de un conductor existente (de F1 o un `QA-SEL`) → elegirlo. Repetir con un conductor sin país y un vehículo con país. | La opción se ve como «Nombres Apellidos · CC n» (D7); al elegirla, el select la muestra. Si el conductor no tiene país, debajo del select «País: {país del vehículo} (del vehículo)» (D15). | P1 | FUN |
| F3-CAM-005 | Conductor nuevo con «+» | «+» junto al select → tipo CC, documento nuevo (`9000000001`), nombres `QA-SEL`, apellidos `Uno` → «Registrar conductor». Sin guardar la ficha, abrir Admin → Conductores en otra pestaña. | El modal se cierra con el aviso «Conductor registrado»; el conductor queda seleccionado en el select y **ya existe** en Admin → Conductores antes de guardar la ficha (D9). | P1 | PER |
| F3-CAM-006 | Datos mínimos del conductor | Documento de 3 caracteres; nombre de 1 carácter. | Esperado: rechazo coherente. Riesgo R-BAS-17: la card solo exige no vacío; anotar qué pasa al guardar. | P2 | VAL |
| F3-CAM-007 | Precarga asíncrona | Seleccionar un camión, cambiar rápido a otro y volver. | Los datos precargados corresponden al camión correcto; no se mezclan ni se borran lo digitado (ver memoria `primevue-form-async-prefill`). | P1 | PER |
| F3-CAM-008 | Memoria del turno | Registrar un camión con transportadora X y país Ecuador; abrir el siguiente camión sin datos. | Transportadora y país precargados de la memoria con «limpiar»; solo llena campos vacíos. | P1 | UX |
| F3-CAM-009 | Alta rápida de transportadora | «+» en transportadora → crear `QA Transportes 2`. | Se crea con rol TRANSPORT_COMPANY y queda seleccionada. | P2 | FUN |
| F3-CAM-010 | Persistencia en Solo báscula | En SBA, digitar conductor y tipo de vehículo nuevos; completar la operación; revisar Admin → Vehículos/Conductores y el ingreso. | Esperado: los datos quedan guardados. Riesgo R-BAS-04: se exigen pero no se persisten. | P1 | PER |
| F3-CAM-011 | Persistencia en Salida | Igual en una Salida de mercancía. | Igual que F3-CAM-010. | P1 | PER |
| F3-CAM-012 | Solo lectura tras guardar | Pasar al paso 2. | La card queda en solo lectura. | P2 | UI |
| F3-CAM-013 | Buscar por documento | En el select, escribir un fragmento de 4-6 dígitos del documento de un conductor existente (p. ej. `000000` de los `QA-SEL`). Repetir con espacios intercalados. | Aparece el conductor del documento. Con espacios también (D4: el documento se busca sin espacios). | P0 | FUN |
| F3-CAM-014 | Sin tildes y en otro orden | Escribir el nombre de un conductor con tilde sin la tilde y en minúsculas; luego «apellido nombre». | Lo encuentra en los dos casos (D4) y la opción no la oculta el filtro local (D8). | P1 | FUN |
| F3-CAM-015 | Pie de paginación | Abrir el select sin escribir. | Lista 20 opciones ordenadas por nombre y el pie «Mostrando 20 de N. Escriba nombre o documento para afinar.» (D6). Con un término de pocos resultados, sin pie. | P2 | UI |
| F3-CAM-016 | «+» con documento existente | «+» → CC y el documento de un conductor ya registrado (p. ej. `9000000001` de F3-CAM-005) → salir del campo. | Aviso «Este conductor ya está registrado.»; nombres y apellidos precargados; botón «Usar este conductor». Al pulsarlo queda seleccionado; en Admin → Conductores no hay duplicado (D10). | P1 | RN |
| F3-CAM-017 | Lápiz: corregir el teléfono | Con `QA-SEL Uno` seleccionado → lápiz → cambiar el teléfono → «Guardar cambios». | El tipo y el número de documento están bloqueados; aviso «Conductor actualizado exitosamente»; el cambio se ve en Admin → Conductores y el select sigue con el conductor (D2, D12). | P1 | FUN |
| F3-CAM-018 | Lápiz sin selección | Limpiar el select (×). | El lápiz queda deshabilitado; «+» sigue habilitado. | P2 | UI |
| F3-CAM-019 | Reabrir una operación con conductor | Guardar un registro con conductor; luego retomarlo desde «Recuperar operaciones» (`?resume=`) o reabrir la ficha del camión. | El conductor aparece preseleccionado (D16), con el lápiz habilitado y sin «Faltan» por conductor. | P1 | PER |
| F3-CAM-020 | El ingreso guarda el conductor elegido | Tras guardar el registro de un camión con un conductor elegido en el select, revisar el ingreso (Vigilancia → historial, Trazabilidad o `psql` de solo lectura sobre `entry_logs`). | El ingreso queda con el conductor elegido. Los datos del conductor anterior del camión (si tenía) no cambian (DEF-F11-008). | P0 | PER |
| F3-CAM-021 | Solo teclado | Desde el campo anterior: Tab al select → escribir 3-4 caracteres → Enter → Tab. Luego: «+» con teclado, Esc; y «Guardar» sin conductor. | Se elige el conductor sin ratón y sin clics extra; Enter en el filtro elige la opción y **no** guarda la ficha; el modal abre con el foco en «Tipo de Documento» y Esc lo cierra; «Guardar» sin conductor lleva el foco al select (§6 del plan del selector). | P1 | UX |
| F3-CAM-022 | Conductor inactivo | Admin → Conductores: desactivar `QA-SEL Dos`. En Báscula, buscar `QA-SEL Dos` y su documento. | No aparece en el select (`isActive=true`). | P2 | RN |

> Casos 003-005 reescritos y 013-022 agregados el 2026-10-08 por el selector de conductor (plan `docs/planes/plan-cerrado-selector-conductor-2026-10-08.md`).

### 6.3 Registro del ingreso con depósito (REG)

**Mini-checkpoint REG:** si F3-REG-001 falla, detener la fase (BLOCKER).

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F3-REG-001 | Registro IMP mínimo | `QAA101`: modalidad IMP, Carta porte `QA-CP-0001`, una línea `QA Cebolla` cantidad 100, manifiesto `QA-MAN-0001` con peso 20.000 (obligatorios, `DEC-057` D7); camión y conductor completos → Guardar (Enter). | Aviso en línea «Documento nuevo: al guardar se crea un depósito» antes de guardar. Guarda; la ficha pasa a Cobro. Se crea un depósito `2026BA000nn` en Borrador (ver en CE). | P0 | FUN |
| F3-REG-002 | Stock declarado | CE → detalle del depósito de F3-REG-001; Bodega → Inventario. | Stock del producto = 100 (declarado), con movimiento `DeclaredEntry`. | P0 | INT |
| F3-REG-003 | Notificación a CE | Con `c_exterior`, revisar notificaciones. | «Nuevo depósito de importación» (y aviso por producto creado si aplica). Riesgo R-ADM-01: puede no llegar. | P1 | INT |
| F3-REG-004 | Registro EXP | `QAA102`: EXP, `QA-CP-0002`, `QA Repuestos` 50, exportador `QA Exportador` en el panel. | Depósito `2026EXP…` en Borrador. | P0 | FUN |
| F3-REG-005 | Registro INSP | `QAB203`: cambiar modalidad a INSP, `QA-CP-0003`. | El panel de pesaje fuerza un solo pesaje Bruto y apaga perecedero; depósito `2026INSP…`. | P0 | RN |
| F3-REG-006 | Documento obligatorio | Guardar sin número o sin tipo de documento. | No guarda; mensaje en el campo. | P1 | VAL |
| F3-REG-007 | Longitudes | Número de 51 caracteres; manifiesto de 101. | Rechazados («…no puede exceder 50 caracteres», «…100 caracteres»). | P2 | VAL |
| F3-REG-008 | Mayúsculas | Número `qa-cp-0004`. | Se normaliza a `QA-CP-0004`. | P2 | VAL |
| F3-REG-009 | Sin cantidad | Línea sin cantidad. | «Ingrese la cantidad de al menos un producto para este camión.». | P0 | VAL |
| F3-REG-010 | Producto repetido | Dos líneas `QA Cebolla`. | «El producto «QA Cebolla» está repetido…». | P1 | VAL |
| F3-REG-011 | Línea libre | Descripción libre «QA mercancía varia» sin unidad; luego con unidad. | Sin unidad: rechazo (DF16); con unidad: guarda. Descripción de 2 caracteres o 201: rechazo. | P1 | VAL |
| F3-REG-012 | Peso manifiesto | 0 o negativo. | «El peso bruto según manifiesto debe ser mayor que cero.». Por API, 400 «El peso del manifiesto del camión es obligatorio.» (`DEC-057` D7). | P2 | VAL |
| F3-REG-013 | Datos CE opcionales | Guardar IMP sin importador ni agencia (con el manifiesto del camión). | Guarda (BAS-01); CE los exigirá al confirmar (fase 5). El manifiesto del camión no es opcional: F3-REG-025. | P0 | RN |
| F3-REG-014 | Valor y moneda | Valor 1.500,555 (3 decimales); valor sin moneda; moneda sin valor. | 3 decimales rechazado; valor exige moneda; sin valor la moneda no se envía (DF10). | P1 | VAL |
| F3-REG-015 | Fecha del documento futura | Fecha mañana. | «La fecha del documento no puede ser futura.». | P2 | VAL |
| F3-REG-016 | Alta rápida de importador/agencia/exportador | «+» en cada uno. | Crea el tercero con el rol correcto y lo selecciona. | P2 | FUN |
| F3-REG-017 | Fecha de ingreso del depósito (WMS-33) | «Cambiar» la fecha: anterior al ingreso de Vigilancia; posterior a ahora; dentro del rango. | Fuera de rango: rechazado con «…no puede ser anterior al ingreso del camión en Vigilancia…» / «…no puede ser futura.»; dentro: se guarda y el depósito la muestra. | P1 | RN |
| F3-REG-018 | Primer pesaje Tara | Configurar primer pesaje Tara en un ingreso. | El paso de peso pide Tara primero y Bruto al cerrar. | P1 | RN |
| F3-REG-019 | Un solo pesaje / perecedero | Marcar «Flujo perecederos» con `QA Cebolla`. | Fuerza un solo pesaje. Anotar el flujo de cierre (guía global). | P2 | RN |
| F3-REG-020 | Búsqueda del documento al salir del campo | Escribir `QA-CP-0001` (ya con un depósito abierto) y salir con Tab. | **Reescrito (`DEC-057`, D1 y D4):** «Este documento ya tiene depósitos abiertos: elija a cuál entra el camión o cree uno nuevo.», una tarjeta por depósito abierto (número, estado, camiones, cliente, importador o exportador, agencia, transportadora, fecha del documento y placas) y «Es otro documento: crear depósito nuevo». Ninguna viene elegida y «Guardar» queda deshabilitado hasta elegir. Con un documento sin depósitos: «Documento nuevo: al guardar se crea un depósito.». | P0 | FUN |
| F3-REG-021 | Error de búsqueda | (Local) detener el API un momento y buscar un documento. | Banner de error con «Reintentar»; «Guardar» queda bloqueado hasta reintentar (`DEC-057` D1: sin saber si hay abiertos no se crea un depósito); al reintentar con el API arriba, funciona. | P2 | ERR |
| F3-REG-022 | Observaciones | Escribir en «Observaciones» y pulsar Enter. | Anotar: Enter guarda el formulario (R-BAS-16); ¿es deseado? | P3 | UX |
| F3-REG-023 | Documentos adicionales | Agregar documentos de envío (manifiesto, factura comercial). | Se guardan con el registro (verificar en el detalle). | P2 | PER |
| F3-REG-024 | Tiempo del registro | Cronometrar desde seleccionar el camión hasta guardar un IMP mínimo con datos precargados. | Anotar el tiempo (meta del negocio: el ciclo completo ≈ 30 s del legacy; DF2 mide hasta el primer peso). | P1 | UX |
| F3-REG-025 | Manifiesto obligatorio | Ingreso IMP, EXP e INSP (y un depósito adicional) sin N.º de manifiesto o sin peso → Guardar. Luego Solo báscula y Salida sin manifiesto. | **Nuevo (`DEC-057`, D7):** no guarda; en el campo «El número de manifiesto del camión es obligatorio.» y «El peso del manifiesto del camión es obligatorio.»; el encabezado «Registro» los cuenta en «Faltan N datos». Por API, 400 con los mismos mensajes. Solo báscula y Salida no lo piden. | P0 | VAL |
| F3-REG-026 | Misma carta porte, dos clientes (H7) | Con un depósito abierto de `QA Cliente Uno` para `QA-CP-0101`, llega otro camión de otro cliente con `QA-CP-0101`: elegir «Es otro documento: crear depósito nuevo», cliente `QA Cliente Dos` → Guardar. Después, un tercer camión de `QA Cliente Uno` elige la tarjeta del primer depósito. | **Nuevo (`DEC-057`, D1):** el segundo camión crea un depósito nuevo, con su cliente; el primero no cambia (stock, cliente y fecha). El tercero se asocia al depósito elegido («Camiones ingresados: 2») y precarga sus datos en solo lectura. Nada se asocia solo: sin elección no se guarda. | P0 | RN |
| F3-REG-027 | Depósito cerrado o migrado con el mismo número | Número de un depósito con el ingreso de camiones cerrado (F5-CNF-010) o de uno migrado del legacy → Tab → Guardar. | **Nuevo (`DEC-057`, D3):** el depósito se ve en gris, con candado, «Cerrado por {nombre} el {fecha}» o «Migrado», y no se puede elegir. Si no hay abiertos: «Los depósitos de este documento están cerrados: al guardar se crea un depósito nuevo.». Guarda y crea un depósito nuevo, sin 409. | P0 | RN |
| F3-REG-028 | Depósito elegido que se cierra antes de guardar | Elegir un depósito abierto; en otra pestaña CE cierra su ingreso de camiones; Guardar. | **Nuevo (`DEC-057`, D1):** 409 «El depósito {N} ya no está abierto para el documento {número}. Vuelva a buscar el documento.»; la pantalla repite la búsqueda y el depósito pasa a gris. | P1 | RN |
| F3-REG-029 | Fecha del documento al asociar | Elegir un depósito con fecha del documento; luego uno sin fecha y digitar una. | **Nuevo (`DEC-057`, D2):** con fecha, se muestra en solo lectura y manda la del depósito; sin fecha, se escribe la digitada. | P2 | RN |
| F3-REG-030 | «Guardar» mientras se busca el documento | Escribir `QA-CP-0001` (ya con un depósito abierto) y, sin salir del campo, clic en «Guardar». Repetir con Enter desde un campo posterior y en un depósito adicional. | **Nuevo (revisión de `DEC-057`, C1):** no se guarda. Mientras se busca, el botón dice «Buscando el documento…» y está deshabilitado; al terminar aparece el selector de F3-REG-020 y «Guardar» espera la elección. No se crea un segundo depósito para el documento. | P0 | RN |

### 6.4 Cobro (COB)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F3-COB-001 | Cobro inmediato en efectivo | Tras F3-REG-001: destinatario tercero `QA Cliente Uno`, modo Inmediato, Efectivo, total precargado → Cobrar (Enter). | Factura BASCULA creada y pagada (ver en Facturación); ciclo `ReadyForWeighing`; la ficha pasa a Peso. | P0 | FUN |
| F3-COB-002 | Total precargado por convenio | Comparar el total con el convenio BASCULA de `QA Cliente Uno`; con un tercero sin convenio, comparar con el precio base. | Convenio si hay cliente registrado; si no, precio base. | P0 | RN |
| F3-COB-003 | Destinatario por defecto | Abrir el cobro de una operación que tiene cliente. | Esperado (DF9): el cliente preseleccionado; sin cliente, el conductor. Riesgo R-BAS-05: nunca preselecciona el cliente. | P1 | UX |
| F3-COB-004 | Conductor como destinatario (WMS-23) | «Conductor del vehículo». | Precarga nombre e identificación del conductor como persona no registrada; la factura muestra «No registrado». | P0 | FUN |
| F3-COB-005 | Persona no registrada | Nombre 2 caracteres; ID de 3; ID de 51; datos válidos. | Inválidos rechazados (nombre 3–255, ID alfanumérico 4–50); válidos guardan. | P1 | VAL |
| F3-COB-006 | Consumidor final | Destinatario Consumidor final. | La factura sale a «Consumidor Final» (`222222222222`). | P1 | FUN |
| F3-COB-007 | Por facturar | Modo «Por facturar» con `QA Cliente Uno`. | Factura sin pago y sin número, visible en Facturación; ciclo listo para pesar. | P0 | FUN |
| F3-COB-008 | Total editable | Cambiar el total a 30.000; a 0 (cliente sin convenio de báscula en $0). | 30.000: la factura sale por 30.000 con subtotal + IVA separados según la tasa del servicio; 0: «El total a pagar debe ser mayor a cero.» (el cero solo sale de un convenio: F3-COB-015). | P0 | RN |
| F3-COB-009 | Cliente bloqueado | Destinatario `QA Cliente Mora` (bloqueado). | «El cliente '…' está bloqueado por deuda pendiente. No se puede proceder con la operación.»; la ficha se queda en Cobro. | P0 | RN |
| F3-COB-010 | Sin tarifa | (Local, con un servicio sin precio ni convenio — no tocar BASCULA real.) | Anotar el mensaje «No se encontró tarifa para el servicio de báscula…» y si bloquea o permite digitar el total. | P2 | ERR |
| F3-COB-011 | Otros métodos | Transferencia con referencia; Tarjeta. | Se guardan método y referencia en el pago. | P2 | FUN |
| F3-COB-012 | Efectivo y cambio | Buscar «efectivo recibido» y «cambio». | Anotar: el refactor `a5289ce` los eliminó, contra el plan F1-04 (R-BAS-13). Confirmar con el usuario si es la decisión vigente. | P2 | FUN |
| F3-COB-013 | Doble clic en Cobrar | Pulsar Cobrar dos veces rápido. | Una sola factura y un solo ciclo («Ya existe un ciclo de báscula para este servicio.» si llega la segunda). | P0 | PER |
| F3-COB-014 | Error de cobro recuperable | Provocar un error (cliente bloqueado) y luego cambiar a destinatario válido. | Se cobra sin volver a digitar el registro. | P1 | UX |
| F3-COB-015 | Báscula en $0 por convenio | Cliente con convenio activo de BASCULA `FIXED` con tarifa 0. Cobrar su ingreso a depósito, un Solo báscula y una Salida, en Inmediato y en Por facturar, con destinatario «Tercero registrado». | **Nuevo (`DEC-057`, D14–D16):** el cobro muestra «**Sin cobro por convenio.** El convenio del cliente fija este servicio en $0: se emite una factura en cero, sin número fiscal.», sin total ni modo de pago; el resumen del paso dice «Sin cobro por convenio · factura en $0». La factura sale en cero, sin número, pagada con un pago de $0 «ZERO-INVOICE», con el ítem «Servicio de Báscula — Sin cobro por convenio»; «Por facturar» queda Inmediato. El tiquete imprime «VALOR TOTAL $: 0,00» y debajo «SIN COBRO POR CONVENIO». | P0 | RN |
| F3-COB-016 | $0 que no es de convenio | Por API: con el convenio en $0, pagar 10.000; con precio mayor que 0, pagar 0; con una tarifa base (no convenio) en 0. | **Nuevo (`DEC-057`, D14–D15):** 400 «El convenio del cliente fija la báscula sin cobro: el total a pagar debe ser 0.»; 400 «El total a pagar debe ser mayor a cero.»; la tarifa base en 0 se rechaza como antes («No se encontró tarifa para el servicio de báscula…»). | P1 | VAL |

### 6.5 Pesajes (PES)

**Mini-checkpoint PES:** si F3-PES-001 a 004 fallan, detener la fase (BLOCKER).

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F3-PES-001 | Primer pesaje Bruto | `QAA101` tras cobrar: peso 35.000 kg → registrar (Enter). | Ciclo `FirstWeightCaptured`; se asigna tiquete `2026T000nn`; aparece en la cola como «Por repesar». | P0 | FUN |
| F3-PES-002 | Salir y atender otro | «Salir y atender otro camión». | El ciclo queda abierto «Por repesar»; la ficha se libera. | P0 | FUN |
| F3-PES-003 | Segundo pesaje (tara) | Volver a `QAA101` → peso 15.000 (tipo Tara, único permitido). | Neto en vivo 20.000; al registrar, ciclo `Complete`; paso Tiquete. | P0 | FUN |
| F3-PES-004 | Neto calculado en el servidor | Comparar el neto mostrado y el del tiquete/historial. | Neto = bruto − tara = 20.000 kg en todos los lugares. | P0 | RN |
| F3-PES-005 | Tipo de peso permitido | En el repesaje intentar elegir Bruto otra vez. | Solo se ofrece el opuesto; por API: «Para cerrar el ciclo, el tipo de peso debe ser…». | P1 | RN |
| F3-PES-006 | Peso inválido | 0, negativo, texto, decimales extremos. | Rechazado (> 0). Anotar el manejo de decimales. | P1 | VAL |
| F3-PES-007 | Tara mayor que bruto | Primer 15.000 Bruto, segundo 35.000 Tara. | Anotar el neto resultante (negativo) y si se advierte. Esperado de negocio: advertencia o rechazo. | P1 | RN |
| F3-PES-008 | INSP un solo pesaje | `QAB203` (INSP): pesar una vez. | El ciclo cierra en el primer pesaje; un segundo intento da 409 (mensaje anota «flujo perecedero», R-BAS-16). | P0 | RN |
| F3-PES-009 | Fecha del pesaje | Cambiar fecha/hora del pesaje: antes del ingreso; +10 min futuro; antes del pesaje anterior (en el repesaje). | Rechazados con los mensajes de `OperationalDateRules` (tolerancia 2 min). Dentro del rango se guarda. | P1 | RN |
| F3-PES-010 | F2 peso en ventana | En el paso Peso, F2 → digitar → Enter; Esc cierra. | Funciona igual que el campo en línea. | P2 | UX |
| F3-PES-011 | Observación del pesaje | Observación de 501 caracteres. | Rechazado (máx. 500). | P3 | VAL |
| F3-PES-012 | Doble registro de peso | Enter dos veces seguidas en el peso. | Un solo pesaje («El ciclo ya tiene todos los pesajes requeridos.» o idempotente). | P0 | PER |
| F3-PES-013 | Perecedero | Completar F3-REG-019. | Un pesaje; anotar cómo se cierra el ciclo (guía global); el TODO del backend dice que la guía global no persiste la DispatchGuide. | P2 | RN |
| F3-PES-014 | Notificación de perecederos | Tras F3-PES-013, revisar notificaciones de Admin/CE. | Anotar: el código la envía al rol inexistente «Weighbridge» (R-BAS-16). | P3 | INT |
| F3-PES-015 | Tiempo hasta primer peso | Cronometrar desde seleccionar el camión hasta el primer peso registrado (DF2), con datos precargados. | Anotar el tiempo. Referencia de negocio: ~30 s legacy. | P1 | UX |
| F3-PES-016 | Pesaje tras salida del camión | Ver F2-SAL-005: registrar salida en Vigilancia de un camión «Por repesar» y luego repesar. | «… no puede ser posterior a la salida del camión (…)». Documentar el impacto (R-VIG-03). | P0 | INT |
| F3-PES-017 | Los cuatro pesos del legacy | Ingreso a depósito con manifiesto de 13.700 y primer pesaje Bruto: digitar 21.380 en «P. indicador (kg)» y salir con Tab. Repetir con un manifiesto de 25.000. Probar un primer pesaje Tara. | **Nuevo (`DEC-057`, D9, D10 y D13):** P. indicador 21.380 · P. manifiesto 13.700 · T. vehículo 7.680 · P. mercancía 13.700. Con 25.000: sin tara y «El manifiesto supera el peso del indicador». Con primer pesaje Tara no se muestran. En pesaje compartido, P. manifiesto es la suma de los camiones. Los cálculos se actualizan mientras se digita. | P0 | RN |
| F3-PES-018 | Un solo pesaje con manifiesto | Inspección (o perecedero) con manifiesto 13.700 y Bruto 21.380: completar el ciclo. Revisar el detalle del ciclo, el historial, el tiquete, el diario de ingresos y el detalle del depósito en CE. Repetir con un ingreso de dos pesajes. | **Nuevo (`DEC-057`, D11 y D12):** el neto es 13.700 «según manifiesto» en el detalle del ciclo (sin «Diferencia»), en el historial, en el diario y en CE («Calculado según manifiesto»); el neto real pesado sigue vacío. Con dos pesajes manda el neto real. | P0 | RN |

### 6.6 Tiquete (TIQ)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F3-TIQ-001 | Imprimir tiquete | Paso 4 → Imprimir. | Abre el PDF térmico (80 mm) y el diálogo de impresión. | P0 | FUN |
| F3-TIQ-002 | Contenido | Revisar el PDF. | Empresa, «ORDEN DE PESO No. 2026T…», cliente (o el destinatario no registrado, o «CONSUMIDOR FINAL»), placa, conductor, producto, ENTRADA/SALIDA con hora y tipo, PESO MERCANCÍA (neto), ítems de la factura y VALOR TOTAL. Valores = los registrados. Pie: «Documento interno de control de pesaje. No es una factura de venta.» (sin «DIAN»; BR-02-005). **Actualizado (`DEC-057`, D12):** en un ingreso a depósito con manifiesto, «P. MANIFIESTO»; sin segundo pesaje, «T. VEHÍCULO», y «PESO MERCANCÍA» con el manifiesto y «Kilogramos (según manifiesto)» (F3-PES-018). | P0 | FUN |
| F3-TIQ-003 | Observación en el tiquete | Agregar observación (≤ 1000) y reimprimir. | Aparece en el PDF. | P2 | FUN |
| F3-TIQ-004 | Fecha y hora | Comparar la FECHA del tiquete con la hora Colombia. | Esperado: hora Colombia. Riesgo R-BAS-15: sale en UTC (+5 h). | P1 | RN |
| F3-TIQ-005 | Reimprimir | Reimprimir desde el historial. | Mismo número y datos. | P1 | FUN |
| F3-TIQ-006 | Consecutivo sin saltos | Completar 3 operaciones seguidas. | Tiquetes consecutivos (5 dígitos, prefijo del año del ingreso). Anotar saltos. | P0 | RN |
| F3-TIQ-007 | Finalizar | «Finalizar» tras imprimir. | El camión sale de la cola de báscula. | P1 | FUN |
| F3-TIQ-008 | Filtro «no impresos» | Historial → «no impresos» antes y después de imprimir. | El tiquete deja de aparecer tras la primera impresión. | P2 | FUN |

### 6.7 Persistencia, abandono y reingreso (REI)

Foco pedido explícitamente: registrar → guardar → abandonar → volver → editar → completar. **No debe pedir otra vez lo ya registrado.**

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F3-REI-001 | Borrador sin guardar entre camiones | Digitar parte del registro de `QAB201` sin guardar; seleccionar otro camión; volver. | Lo digitado sigue ahí (borrador por camión). | P0 | PER |
| F3-REI-002 | Aviso al salir con borradores | Con borradores sin guardar, navegar a otra página. | Pide confirmar y lista las placas. | P1 | UX |
| F3-REI-003 | Recarga con borrador sin guardar | Digitar sin guardar y recargar (F5). | Anotar: según el código no hay `beforeunload`; el borrador se pierde sin aviso (R-BAS-14). | P1 | PER |
| F3-REI-004 | Registro guardado, abandono antes de cobrar | Guardar el registro de un camión; ir a otra página; volver y seleccionarlo («Por cobrar»). | Abre en Cobro, no vuelve a pedir el registro; el total se recalcula. | P0 | PER |
| F3-REI-005 | Registro guardado tras recarga | Igual que F3-REI-004 pero recargando el navegador. | Abre en Cobro. Anotar: la sección Registro de solo lectura puede quedar vacía (R-BAS-14). ¿Se ven el documento, productos y cliente? | P0 | PER |
| F3-REI-006 | Abandono tras cobrar | Cobrar y salir sin pesar; volver. | Abre en Peso; el resumen del cobro visible; no vuelve a cobrar. | P0 | PER |
| F3-REI-007 | Abandono tras primer peso | Primer peso, salir, cerrar sesión, entrar con otro usuario Scale (`f_chosi`) y abrir el camión. | Abre en repesaje con el primer peso, el modo y la fecha de ingreso hidratados. | P0 | PER |
| F3-REI-008 | Más de 10 borradores | Abrir 11 camiones con borrador sin guardar (si hay datos) o simular. | Anotar: el más viejo se pierde sin aviso (KeepAlive máx. 10, R-BAS-14). | P3 | PER |
| F3-REI-009 | Editar datos tras guardar | Después de guardar el registro, intentar cambiar cantidad, documento o cliente desde la ficha. | Anotar qué se puede editar (la card queda en solo lectura). Las correcciones van por CE (detalle del depósito) o por anular/descartar. Documentar el camino. | P1 | FUN |
| F3-REI-010 | Solo báscula retomada sin borrador — cobro | Registrar un Solo báscula, recargar antes de cobrar, abrirlo y cobrar. | Esperado: cobro por la ruta de solo báscula, factura vinculada al ciclo. Riesgo R-BAS-03: se trata como depósito (`storage/process-payment`). Verificar en Red y en la factura. | P1 | PER |
| F3-REI-011 | Solo báscula retomada sin borrador — peso | Solo báscula sin tipo configurado, cobrado, recargar y pesar. | Esperado: Tara o Bruto libres. Riesgo R-BAS-03: se pierde la elección libre. | P2 | PER |
| F3-REI-012 | Completar después de reingresar | Terminar las operaciones de F3-REI-004..007. | Ciclos completos con datos correctos; un solo depósito, una sola factura por operación. | P0 | PER |
| F3-REI-013 | Memoria de turno tras cerrar sesión | Cerrar sesión y volver a entrar. | Anotar si la memoria (sessionStorage) se conserva o se limpia. | P3 | UX |

### 6.8 Recuperar operaciones (REC)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F3-REC-001 | Badge y lista | Con operaciones a medias, ver «Recuperar operaciones». | Badge con el número; `/recover` lista las operaciones con filtro por placa. **Actualizado (validación `DEC-058`, R8):** «Recuperar operaciones» es un enlace con su contador: Ctrl+clic (Cmd+clic) o el clic con la rueda abren `/recover` en otra pestaña; el clic simple navega en la misma. | P1 | FUN |
| F3-REC-002 | Retomar | «Retomar» una operación «Por cobrar»; después, «Atrás» del navegador. | **Reescrito (`DEC-058`, B7):** abre el banco con el panel del camión en el paso pendiente (Cobro) y `?camion=` en la URL. «Atrás» cierra el panel y deja la cola, no vuelve a «Recuperar operaciones». | P0 | PER |
| F3-REC-003 | Retomar con primer peso | «Retomar» una con primer peso. | Abre en repesaje. | P1 | PER |
| F3-REC-004 | Descartar operación sin ciclo | Registrar un ingreso IMP de prueba (`QAC401` nuevo documento), no cobrar, «Descartar» → confirmar. | Pide confirmación; servicio `Discarded`; el depósito en Borrador queda `Cancelled` con su stock anulado. | P0 | FUN |
| F3-REC-005 | Descartar con ciclo | Intentar descartar una operación cobrada. | No aparece «Descartar» o «La operación ya tiene un ciclo de báscula; no puede descartarse.». | P1 | RN |
| F3-REC-006 | Camión tras descartar | Tras F3-REC-004, volver a la cola. | Esperado: el camión vuelve a «Sin iniciar» y se puede registrar de nuevo. Riesgo R-BAS-02: sigue «Por cobrar» con el servicio descartado. | P0 | PER |
| F3-REC-007 | Nuevo registro tras descartar | Intentar registrar de nuevo el camión de F3-REC-004. | Esperado: se registra. Riesgo R-BAS-02: «El entry log ya tiene un servicio asignado.». | P0 | PER |
| F3-REC-008 | Cobro sobre servicio descartado | Si el camión sigue «Por cobrar», intentar cobrar. | Esperado: imposible. Si permite cobrar un servicio descartado → CRITICAL. | P0 | RN |
| F3-REC-009 | Descartar depósito confirmado | (Con un depósito confirmado por CE y operación sin ciclo, si se puede preparar.) | «El depósito … ya fue confirmado por Comercio Exterior; no se puede descartar la operación.». | P2 | RN |

### 6.9 Varios camiones por documento — WMS-26 (MCA)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F3-MCA-001 | Segundo camión, mismo documento | `QAB201`: IMP, `QA-CP-0001`, Tab, **elegir la tarjeta del depósito** de `QAA101`, `QA Cebolla` 60 y su manifiesto → Guardar. | **Actualizado (`DEC-057`, D1):** la tarjeta muestra el depósito con «1 camión» y su placa; sin elegirla no se guarda. Al guardar, el depósito suma una entrada. | P0 | FUN |
| F3-MCA-002 | Stock acumulado | CE/Bodega tras F3-MCA-001. | Stock `QA Cebolla` = 160; dos `WarehouseStorageEntry`; «Camiones ingresados: 2». | P0 | INT |
| F3-MCA-003 | Datos de CE en solo lectura | En el segundo camión, panel «Datos para Comercio Exterior». | Se muestran en solo lectura y no se envían. | P1 | RN |
| F3-MCA-004 | Producto nuevo en el segundo camión | Agregar `QA Aceite` 10 en un tercer camión del mismo documento. | Se agrega al depósito. | P1 | RN |
| F3-MCA-005 | Modalidad distinta | Mismo documento con EXP, eligiendo el depósito IMP. | 409 «El documento '…' ya tiene un depósito con modalidad 'IMP'…». | P0 | RN |
| F3-MCA-006 | Dos depósitos abiertos con el mismo documento | Dos depósitos abiertos con el mismo número y tipo; un camión nuevo con ese documento. | **Reescrito (`DEC-057`, D1):** ya no hay 409 de ambigüedad ni se elige por la fecha: el selector muestra las dos tarjetas y el operario elige una o crea un depósito nuevo (F3-REG-026). | P1 | RN |
| F3-MCA-007 | Ingreso cerrado por CE | CE cierra el ingreso de camiones de `QA-CP-0001` (F5-CNF-010); otro camión con ese documento. | **Reescrito (`DEC-057`, D3):** sin 409. El depósito cerrado se ve en gris con «Cerrado por {nombre} el {fecha}» y no se elige; al guardar se crea un depósito nuevo (F3-REG-027). | P0 | INT |
| F3-MCA-008 | Banner con documento cerrado | En F3-MCA-007, mirar el banner al salir del campo. | **Reescrito (`DEC-057`, D3):** «Los depósitos de este documento están cerrados: al guardar se crea un depósito nuevo.» y el depósito en gris. R-BAS-06 queda resuelto. | P2 | UX |
| F3-MCA-009 | Camión tardío en depósito confirmado | Con el depósito confirmado (pero sin cerrar ingreso), registrar otro camión. | Se asocia; stock sube; CE recibe aviso de reimprimir etiqueta (y pedir manifiesto); la factura de almacenamiento se recalcula (verificar en fase 6, F6-REC-001). | P0 | INT |
| F3-MCA-010 | Mismo camión, ciclo activo | Con `QAB201` ya con ciclo activo de ese documento, intentar otro registro. | 409 «Este camión ya tiene un ciclo de báscula activo para este documento.». | P2 | RN |

### 6.10 Unidades de carga y tanqueros — WMS-30 (UCA)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F3-UCA-001 | Depósito con unidades de carga | `QAB202`: IMP, `QA-CP-0005`, tipo de carga «Unidades de carga», un Tanquero placa `QAT001`, `QA Aceite` 30.000 litros. | Guarda; el depósito queda en modo unidades de carga con la unidad `QAT001`. | P0 | FUN |
| F3-UCA-002 | Sin unidades | Tipo «Unidades de carga» sin ninguna. | «Registre al menos una unidad de carga.». | P1 | VAL |
| F3-UCA-003 | Placa repetida | Dos unidades `QAT001`. | «La placa QAT001 está repetida.». | P1 | VAL |
| F3-UCA-004 | Placa ya en el depósito | Segundo camión al mismo documento con `QAT001`. | «La unidad de carga QAT001 ya está registrada en el depósito…». | P1 | RN |
| F3-UCA-005 | Modo distinto en el segundo camión | Segundo camión con «Mercancía suelta». | «El depósito … maneja unidades de carga; el camión debe registrarse como unidades de carga.». | P1 | RN |
| F3-UCA-006 | Desglose en depósito confirmado | Con el depósito confirmado, camión con 2 unidades. | Pide la mercancía por unidad («…declare la mercancía de cada unidad de carga…»); todo o nada. | P2 | RN |
| F3-UCA-007 | Contenedor en el tiquete | Imprimir el tiquete de F3-UCA-001. | Muestra las unidades de carga. | P2 | FUN |
| F3-UCA-008 | Tanquero y contenedor de bodega | Revisar el depósito en CE y Bodega. | La unidad aparece como unidad de carga del depósito (sección de unidades), no como producto. | P1 | INT |

### 6.11 Multidepósito en el mismo camión (MUL)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F3-MUL-001 | Agregar otro depósito | Tras el primer peso de un ingreso, buscar «Agregar otro depósito». | Esperado: disponible para registrar un segundo documento en el mismo camión (cobro en $0, pesaje intermedio). Riesgo R-BAS-01: no aparece (modo Standard). Si no aparece, marcar los casos MUL-002..004 `BLOQUEADO`. | P1 | FUN |
| F3-MUL-002 | Depósito adicional independiente | Registrar el segundo depósito con otro cliente, moneda y valor. | Cada depósito con sus propios terceros y valores; comparten vehículo, ciclo y modalidad. | P1 | RN |
| F3-MUL-003 | Cobro en cero | Paso de cobro del adicional. | «Confirmar y continuar» con factura $0; por API, `AmountReceived` ≠ 0 rechazado. | P1 | RN |
| F3-MUL-004 | Pesaje intermedio | Pesar con 2 depósitos eligiendo «Intermedio — el camión descarga en otro punto». | **Reescrito (DEC-050, D13):** el operario elige. Con «Intermedio»: pesaje `Intermediate`, neto por depósito = \|entrada − salida\| y tiquete propio por depósito; cierre con el opuesto. Después de un intermedio no hay modo mixto: una Tara antes del último depósito responde 400. La Tara antes de la llegada a Bodega del segundo depósito responde 409. | P1 | RN |
| F3-MUL-005 | Un solo pesaje para varios documentos | Camión con 2 depósitos (el segundo, adicional): Bruto → llegada a Bodega de los dos → «Tara — un solo pesaje para todos los depósitos» (predeterminado). Probar con un manifiesto sin peso y completarlo después (desde `DEC-057` D7 el manifiesto es obligatorio en báscula: solo aplica a depósitos registrados antes del cambio, o borrando el peso en CE). | **Nuevo (DEC-050, D13 a D15):** el ciclo cierra con dos pesajes; la Tara asigna la salida a cada entrada. Con un manifiesto sin peso, los netos quedan nulos; al completarlo se reparte el neto del camión **en proporción al peso de manifiesto** (ej. neto 20.000 con 20.000 y 10.000 → 13.333,33 y 6.666,67; el último absorbe el residuo). Hay **un tiquete por depósito** (`2026T…` consecutivos) con «Pesaje compartido por 2 depósitos · neto del camión X kg». El primero cobra y el adicional va en $0. Al repartir de nuevo en un depósito ya validado, la observación de la validación conserva su valor (D14). | P1 | RN |
| F3-MUL-006 | Depósito adicional con un documento abierto | Tras el primer peso, «Agregar otro depósito» con un número y tipo que ya tienen un depósito abierto. | **Nuevo (`DEC-057`, D5):** la pantalla lo rechaza y, por API, 409 «El documento {número} ya tiene un depósito abierto ({N}). Un depósito adicional necesita un documento propio.». Con un documento sin depósitos abiertos se registra como siempre. | P1 | RN |

### 6.12 Salida de mercancía (SAL)

Requiere la preparación del §5.

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F3-SAL-001 | Buscar orden por número | `QAB205` → tipo Salida → número `2026OC…`. | Encuentra la orden; resumen con cliente y depósitos; «Cambiar orden». | P0 | FUN |
| F3-SAL-002 | Buscar por placa | Buscar por `QAB205`. | Encuentra la orden (lista si hay varias). | P1 | FUN |
| F3-SAL-003 | Mínimo de caracteres | Buscar con 3 caracteres. | Esperado: busca (la ayuda dice mínimo 3). Riesgo R-BAS-11: exige más de 3. | P3 | UX |
| F3-SAL-004 | Orden externa | Buscar por número de orden externa (WMS-17). | Encuentra la orden. | P1 | FUN |
| F3-SAL-005 | Cobro y tara | Guardar → cobrar (cliente de la orden) → primer peso Tara 15.000. | Ciclo de salida; factura BASCULA; la OC queda asociada. | P0 | FUN |
| F3-SAL-006 | Repesaje y despacho | Tras el cargue en Bodega (F4-CAR-001), repesar Bruto 30.000. | Ciclo `Complete`; si la orden estaba `Loaded`, pasa a `Dispatched`; el servicio `Completed`. | P0 | INT |
| F3-SAL-007 | Repesaje antes del cargue | Repesar antes de que Bodega cargue. | Anotar: el ciclo cierra y la orden queda sin despachar hasta el cargue (luego Bodega la deja `Dispatched`, F4-CAR-008). | P1 | INT |
| F3-SAL-008 | Orden ya despachada o cancelada | Iniciar salida con una OC `Dispatched` o `Cancelled`. | Esperado: rechazo. Riesgo R-BAS-12: se permite. | P1 | RN |
| F3-SAL-009 | Orden con servicio activo | Otra salida con la misma OC en otro camión. | Esperado: «La orden … ya tiene un servicio de salida en báscula.». Riesgo R-BAS-12. | P1 | RN |
| F3-SAL-010 | Agregar otra orden al pesaje | «Agregar otra orden a este pesaje» con una segunda OC del mismo vehículo. | Se agrega; al cerrar el ciclo ambas se despachan si están cargadas. | P2 | FUN |
| F3-SAL-011 | Salida con tiquete de ingreso | «Con el tiquete de ingreso»: elegir un tiquete completo de la misma placa. | Sin cobro ni peso; pasa a Tiquete; la orden se despacha al cargar. | P1 | FUN |
| F3-SAL-012 | Tiquete inválido | Tiquete anulado, incompleto, ya usado o de otra placa. | Mensajes: «El tiquete … está anulado / no está completo / ya se usó…», «La orden … es para el vehículo …». | P2 | RN |
| F3-SAL-013 | Depósito en Borrador | OC cuyo depósito volvió a Borrador (R-CE-05). | «Los depósitos de la orden … deben estar confirmados.» o «El depósito no está en estado válido para salida…». | P2 | RN |

### 6.13 Solo báscula — OTH001 (SBA)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F3-SBA-001 | Un pesaje | `QAA103`: Solo báscula, cliente `QA Cliente Uno`, sin segundo pesaje → Guardar → Cobrar → Peso 18.000. | Ciclo `Complete` con un pesaje; tiquete en el ciclo; sin depósito. | P0 | FUN |
| F3-SBA-002 | Sin cliente es válido | Con `QAA103`, sin cliente: guardar → cobrar al conductor (destinatario no registrado) → peso. Repetir con «Por facturar» y destinatario «Consumidor final». | **Reescrito (DEC-050, BR-02-002):** se registra sin cliente («Cliente (opcional)»; «Sin cliente, el cobro va al conductor o al consumidor final»). El cobro va al conductor o al consumidor final (por defecto). El tiquete y el historial muestran al destinatario y el filtro por cliente lo encuentra. No se crea depósito. | P1 | RN |
| F3-SBA-003 | Dos pesajes | Otro camión con «Tiene segundo pesaje», primer Tara. | Dos pesajes; neto correcto. | P1 | FUN |
| F3-SBA-004 | Tipo libre | Sin segundo pesaje: elegir Tara o Bruto libremente. | Ambos permitidos (AB-5). | P2 | RN |
| F3-SBA-005 | Peso esperado | Peso esperado 0 o negativo. | Rechazado (> 0). | P3 | VAL |
| F3-SBA-006 | No crea depósito | CE/Bodega. | No hay depósito ni stock nuevo. | P0 | INT |
| F3-SBA-007 | Aparece en historial de entradas | Historial → Entradas. | La operación aparece (incluye Solo báscula). | P2 | FUN |

### 6.14 Historial (HIS)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F3-HIS-001 | Pestañas | Entradas y Salidas. | Entradas incluye depósitos y Solo báscula; Salidas las de mercancía. | P1 | FUN |
| F3-HIS-002 | Filtros | Placa, estado, tiquete, factura, carta porte, tipo, fechas, ID de ciclo, modalidad, transportadora, cliente, «valor cero», «pendiente de pago», «no impresos». | Cada filtro funciona solo y combinado. | P1 | FUN |
| F3-HIS-003 | Totales | Comparar la barra de totales con la suma de filas filtradas. | Coinciden. | P1 | RN |
| F3-HIS-004 | Exportar Excel | Exportar con un filtro aplicado. | Archivo con todas las filas del filtro (no solo la página), columnas legibles, fechas en hora Colombia. | P1 | FUN |
| F3-HIS-005 | Detalle | Abrir el detalle de un ciclo. | Datos completos y acciones según rol. | P1 | FUN |
| F3-HIS-006 | Editar fecha del pesaje | Desde el detalle (Admin/Scale). | Dentro de límites se guarda; fuera, rechazado. | P2 | RN |
| F3-HIS-007 | Imprimir con observaciones | Desde el detalle. | PDF con la observación. | P3 | FUN |
| F3-HIS-008 | Sin «Cambiar modo de pago» | Abrir en el historial el detalle de una operación «por facturar» y de una de pago inmediato. | Esperado (D-2, CHG-47): el modo de pago se muestra solo como etiqueta; el historial no ofrece «Cambiar modo de pago» ni llama a `PATCH weighbridge/{id}/payment-mode`. Un cobro «por facturar» se paga en Facturación → Pagos. | P1 | FUN |
| F3-HIS-009 | Manifiesto y neto según manifiesto | Historial con el ciclo de F3-PES-018 y uno de dos pesajes; ver la barra de totales. | **Nuevo (`DEC-057`, D12 y D13):** columna «Manifiesto (kg)»; con un solo pesaje, el neto es el del manifiesto con «según manifiesto» debajo y la tara es la deducida; los totales suman ese neto. Con dos pesajes, el neto real. El Excel no cambia. | P1 | RN |

### 6.15 Correcciones de pesaje (COR) y detalle del ciclo (CIC)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F3-COR-001 | Modificar primer peso | Detalle del ciclo → «Modificar #1» → nuevo peso, razón ≥ 10. | Se guarda; el neto se recalcula; Admin recibe notificación/correo. | P0 | RN |
| F3-COR-002 | Visibilidad de «Editar» en el historial | Con `bascula` y con `facturacion`, abrir el detalle del historial. | Esperado: ven «Editar» (WeighingCorrectionAccess = Admin, Scale, Billing). Riesgo R-BAS-08: no lo ven. | P1 | ROL |
| F3-COR-003 | Modificar segundo peso | «Modificar #2». | Neto recalculado. | P1 | RN |
| F3-COR-004 | Razón corta | 9 caracteres. | «La razón debe tener al menos 10 caracteres». | P2 | VAL |
| F3-COR-005 | Facturación corrige peso | Con `facturacion`, abrir `cycles/[id]` y modificar. | Permitido. Fecha del pesaje: no permitido para Billing (ScaleAccess). | P2 | ROL |
| F3-COR-006 | Ciclo con 3+ pesajes | (Si F3-MUL funciona) modificar el pesaje #3. | Cambia el #3 y se recalcula el neto de las entradas afectadas. R-BAS-09 corregido en el plan P1 (fase 4, BR-02-006): ver F3-COR-010. | P2 | RN |
| F3-COR-007 | Anular pesaje | Historial → «Anular pesaje» con motivo 10–500 en una operación completa sin salida asociada. | Ciclo `Canceled`; diálogo de resultado; efectos: anotar qué pasa con el depósito, el stock y la factura (recalcula almacenamiento si el depósito está confirmado). | P0 | RN |
| F3-COR-008 | Anular con tiquete usado en salida | Anular un tiquete usado en una salida con tiquete de ingreso. | «El tiquete … se usó para la salida de la orden …; revierta o cancele primero esa orden.». | P2 | RN |
| F3-COR-009 | Anular dos veces | Anular otra vez. | «El pesaje ya está anulado.». | P2 | RN |
| F3-COR-010 | Corregir el pesaje elegido (por `weighingId`) | Ciclo de 3 pesajes con 2 depósitos (Bruto 33.000 → Intermedio 26.000 → Tara 13.000; netos 7.000 y 13.000). Detalle del ciclo → «Modificar» sobre la **Tara** y luego sobre el **Intermedio**, con motivo. Probar un pesaje de otro ciclo y el pesaje #1. | **Nuevo (BR-02-006, D11):** corregir la Tara cambia solo la última entrada; corregir el Intermedio cambia las dos; corregir el Bruto cambia solo la primera. Sin `weighingId` se corrige la secuencia 1 (como antes). Un pesaje de otro ciclo responde 404 «El pesaje no existe en este ciclo.»; el pesaje inicial por esta ruta, 400 «Use la corrección del primer pesaje.». Con un solo pesaje el neto queda nulo. | P0 | RN |
| F3-COR-011 | Corregir la tara de un pesaje compartido | Ciclo de F3-MUL-005 con netos repartidos. Corregir la Tara (13.000 → 14.000) con motivo. | **Nuevo (D14):** el neto del camión pasa a 19.000 y se reparte otra vez (12.666,67 y 6.333,33); los tiquetes reimpresos muestran el neto nuevo. | P1 | RN |
| F3-CIC-001 | Detalle del ciclo | Abrir `cycles/[id]` con Admin, Scale, Billing, CE. | Encabezado, línea de tiempo, tarjetas de depósitos, tiquetes; acciones según rol. | P1 | FUN |
| F3-CIC-002 | Editar fecha de ingreso del depósito | Con Admin/Scale/CE desde la tarjeta del depósito. | Se guarda dentro de límites con motivo; con depósito confirmado recalcula período (fase 6). | P2 | RN |
| F3-CIC-003 | Volver | «Volver» desde el ciclo. | Lleva a `?cola=por-repesar` (o al depósito con `?from=deposit`). | P3 | UX |
| F3-CIC-004 | Cerrar ciclo | «Cerrar ciclo» en un ciclo no terminal (si aparece). | Anotar: el código envía sin peso final y el backend lo rechaza en modo no perecedero (R-BAS-10). | P2 | FUN |
| F3-CIC-005 | Pesos del legacy en el detalle | Abrir el ciclo de F3-PES-018 y uno de dos pesajes. | **Nuevo (`DEC-057`, D12 y D13):** la tarjeta del depósito muestra P. manifiesto, P. indicador, T. vehículo y P. mercancía, y «Peso neto … según manifiesto» sin «Diferencia»; con dos pesajes, el neto pesado y la diferencia ±2 % contra el manifiesto como antes. | P1 | RN |

### 6.16 Dashboard (DSH) y reporte diario (RPT)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F3-DSH-001 | Tarjetas | Abrir el dashboard. | Ciclos hoy, Completados hoy, En proceso, Pendientes de repesaje coherentes con la cola y el historial (anotar que «En proceso» no cuenta `InProgress`). | P1 | FUN |
| F3-DSH-002 | Refresco | Completar una operación con el dashboard abierto. | Se actualiza en ≤ 30 s. | P2 | FUN |
| F3-DSH-003 | Accesos rápidos | Iniciar pesaje, Repesaje, Historial, Recuperar. | Llevan a la ruta correcta. | P3 | UX |
| F3-RPT-001 | Reporte diario | Reportes → fecha de hoy → Descargar PDF. | PDF con cada tiquete del día (placa, destinatario, tipo, subtotal, IVA, total, hora), resumen por tipo y totales. Totales = suma de facturas BASCULA del día. | P1 | RN |
| F3-RPT-002 | Día sin datos | Fecha sin operaciones. | PDF o mensaje «sin datos» sin error. | P3 | ERR |
| F3-RPT-003 | Informe con error | Reportes con el API detenido, o con la consulta del informe fallando (herramientas del navegador). Volver a levantar el API y pulsar «Reintentar». | **Nuevo (validación `DEC-058`, R10):** la tabla muestra el triángulo de alerta, «No se pudo cargar el informe.» y «Reintentar», no «No se encontraron operaciones para esta fecha». «Reintentar» vuelve a consultar y, con el API arriba, muestra el informe. | P2 | ERR |

### 6.17 Integración (INT) y comportamiento visual (UX)

| ID | Caso | Rol | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|---|
| F3-INT-001 | Vigilancia → báscula | Báscula | Tras guardar el registro, revisar el ingreso en el historial de Vigilancia. | Conductor y vehículo actualizados en el ingreso (depósito). | P1 | INT |
| F3-INT-002 | Báscula → Bodega | Bodega | `/warehouse/receptions/entry`. | Las entradas con primer peso (o completas de un solo pesaje) aparecen pendientes de recepción. | P0 | INT |
| F3-INT-003 | Báscula → CE | CE | Lista de importaciones / exportaciones / inspecciones. | Los depósitos creados aparecen en Borrador con sus camiones. | P0 | INT |
| F3-INT-004 | Notificaciones en tiempo real | CE/Admin | Observar mientras se pesa. | `WeighingCaptured` / ciclo completado y «Nuevo depósito…» llegan a Admin y CE (R-ADM-01 para CE). | P1 | INT |
| F3-INT-005 | Báscula → Facturación | Facturación | Facturas → pestaña Báscula. | Una factura por cobro: inmediata Pagada, por facturar sin número, destinatario correcto. | P0 | INT |
| F3-UX-001 | Enter por paso | Báscula | Recorrer un ingreso solo con teclado (Tab, Enter). | Paso 1 Guardar, paso 2 Cobrar, peso con Enter; Enter no actúa en listas desplegadas abiertas ni en modales. | P1 | UX |
| F3-UX-002 | Foco automático | Báscula | Observar el foco en cada paso. | Documento/orden/cliente → total → peso → Imprimir → Finalizar. | P2 | UX |
| F3-UX-003 | Atajos globales | Báscula | Alt+N y Alt+K fuera de un campo de texto, con el panel cerrado y con el panel abierto. | Alt+N → báscula; Alt+K → `?cola=por-repesar`. No actúan dentro de un campo. **Actualizado (`DEC-058`, B8):** con el panel abierto, Alt+N lo cierra como «Volver a la cola», y Alt+K además filtra «Por repesar». | P2 | UX |
| F3-UX-004 | Línea de progreso | Báscula | Recorrer los pasos. | Resumen de cada paso hecho; registro plegable «Ver»; colores coherentes (azul acción, ámbar atención, rojo error, verde completado). | P2 | UI |
| F3-UX-005 | Mensajes de error del backend | Báscula | Provocar 3 errores distintos (sin cantidad, cliente bloqueado, peso inválido). | Se muestra el mensaje en español del backend, sin texto genérico duplicado (riesgo del plan de paridad §G.3). | P1 | ERR |
| F3-UX-006 | Pantalla pequeña | Báscula | Ventana a 1366×768, a 1024 px y a 800 px, con el panel abierto. | **Reescrito (`DEC-058`, B4):** la cola sin scroll horizontal. El panel ocupa casi toda la ventana, su cuerpo se desplaza por dentro y el encabezado deja visibles «Guardar», «Soltar camión» y «Volver a la cola» al bajar. Por debajo de 840 px el panel ocupa toda la pantalla y las acciones bajan a su propia línea. | P2 | UI |

## 7. Mini-checkpoints de la fase

| Tras el bloque | Condición para seguir |
|---|---|
| REG | F3-REG-001, 002, 020 `PASA`. |
| COB | F3-COB-001 y 007 `PASA`. |
| PES | F3-PES-001..004 `PASA`. |
| REI | Ningún CRITICAL de persistencia (datos perdidos o cobro duplicado). Si lo hay, informar antes de seguir. |

## 8. Criterios de salida específicos

- 100 % de P0. Ningún BLOCKER. Los CRITICAL de dinero, peso o persistencia se escalan al usuario antes de la fase 4.
- Depósitos IMP (2 camiones), EXP, INSP, uno con unidades de carga, una operación Solo báscula y una salida (si hubo preparación) anotados en el registro de datos.
- Riesgos verificados: R-BAS-01 a R-BAS-17; R-VIG-03 (F3-PES-016).
- Tiempos medidos (F3-REG-024, F3-PES-015) en el informe.

## 9. Entregables

Informe de fase con los tiempos, defectos, registro de datos. Detenerse.
