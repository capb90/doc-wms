# Registro de decisiones vigentes

> **Para qué sirve:** las decisiones que el usuario o el negocio ya tomaron y que mandan sobre las descripciones de Linear, los documentos antiguos y lo que un agente deduciría del código. **No las reabras:** aplícalas. Si una tarea choca con una, pregunta antes de contradecirla.
> **Fecha de corte:** 2026-10-23. Muchas se tomaron en chats o en planes que ya no existen (`contexto/mapa-de-fuentes.md` §7). Este registro es hoy su única fuente escrita.
> **Cómo agregar una:** al final de su sección, con el siguiente número libre, la fecha, la decisión, el porqué y la fuente. Si una decisión reemplaza a otra, marca la vieja «Reemplazada por DEC-nnn» y no la borres.

## Índice

| ID | Tema |
| --- | --- |
| DEC-001…007 | Forma de trabajo |
| DEC-010…019 | Operación (báscula, depósito, salida) |
| DEC-020…029 | Facturación |
| DEC-030…034 | Permisos |
| DEC-040…044 | Migración del legacy y staging |
| DEC-050…059 | Respuestas a la auditoría de paridad (2026-10-23) |
| DEC-060…069 | Documentos impresos |

## 1. Forma de trabajo

**DEC-001 — Plan cerrado antes del código** (2026-09-14). Todo cambio que no sea trivial empieza con un plan cerrado y sin ambigüedades en `docs/planes/`: cada duda resuelta con su fuente, archivos, esquema, pruebas y orden. El agente junta las preguntas en un mensaje y espera la aprobación antes de tocar código. *Por qué:* el usuario revisa las decisiones antes de que se escriba código.

**DEC-002 — Las decisiones del plan mandan** (2026-09-15). Si el texto de un plan choca con una de sus decisiones `Dn` en un caso borde, gana la decisión. Se aplica y se menciona en una línea, sin pedir aprobación. Solo se pregunta lo que ninguna decisión resuelve. *Por qué:* reabrir un punto que una decisión cubre cuesta una ronda.

**DEC-003 — `develop`, sin ramas y sin commits del agente** (2026-09-17). Se trabaja en `develop` de los dos repos. El agente no crea ramas ni ejecuta `git add`, `commit`, `push` o `merge`. Se detiene al final de cada fase y el usuario hace el commit. *Por qué:* el usuario revisa fase por fase con sus propios commits; la Ola 1 usó ramas y PR, y no quiere repetirlo.

**DEC-004 — Migraciones con `dotnet ef`, por el agente** (2026-10-04; reemplaza la regla anterior de que las generaba el usuario). El agente genera, aplica, revierte o elimina migraciones y recrea la base **local** solo con comandos `dotnet ef`. Nunca edita a mano los archivos generados ni usa SQL manual. Staging y producción, solo con aprobación del usuario. *Por qué:* el historial anterior acumuló migraciones con nombres engañosos y una migración inválida; el 2026-10-01 se consolidó todo en `InitialParityLegacy`.

**DEC-005 — Sin retrocesos funcionales** (2026-10-03). Ninguna restricción de permisos, aunque la pida un plan, puede quitar a un rol una función que usa en su flujo. Antes de restringir se listan las pantallas y los roles que llaman al endpoint. *Origen:* restringir conductores y vehículos dejaba a Comercio Exterior sin «Agregar nuevo» en la orden de cargue.

**DEC-006 — Bases de prueba recreables, staging no** (2026-10-03 y 2026-10-06). Las bases locales se recrean: no hay backfills ni scripts de corrección de datos históricos. Staging tiene datos migrados y lo usan operarios: no se recrea ni se restaura sin un «sí» explícito, y nunca se escribe con SQL.

**DEC-007 — Datos reales y credenciales** (2026-10-06). Los datos reales del legacy solo viven en `db_legacy/trabajo/`, fuera de git. Los informes en git van sin datos de personas naturales. Las credenciales nunca se copian a documentos. En staging, el usuario inicia sesión y el agente usa esa sesión.

## 2. Operación

**DEC-010 — Premisas de pruebas** (2026-09-10, tras las pruebas con operarios). Rigen todos los ajustes:
1. **Báscula rápida:** la meta son ~30 s por camión, como en el legacy. Pantalla única con cola (WMS-31).
2. **Las cantidades del depósito son las declaradas en báscula.** Bodega solo informa y confirma. Comercio Exterior confirma e imprime la etiqueta sin esperar a Bodega (WMS-9).
3. **La unidad de carga es un concepto propio** (contenedor, tanquero, remolque). Bodega la recibe completa, sin contar producto por producto (WMS-30).
4. **Fechas editables:** si el camión entra el sábado y se procesa el lunes, todo lleva la fecha del sábado (WMS-33).

No propongas diseños que hagan esperar a Comercio Exterior por Bodega, ni que cuenten producto por producto dentro de unidades de carga.

**DEC-011 — Agencia de aduanas = SIA = intermediario.** Es un solo rol de negocio, con código canónico `CUSTOMS_AGENCY`. Un `"SIA"` o `"INTERMEDIARY"` en el código es un bug.

**DEC-012 — Fecha de ingreso y consecutivos** (Ola 1, 2026-09-14; Ola 2, 2026-09-17).
- La fecha de ingreso del depósito es la hora de Vigilancia del primer camión; los siguientes no la cambian. Báscula y Comercio Exterior pueden corregirla, sin límite hacia atrás y nunca hacia el futuro. *Precisada por DEC-051 (2026-10-23):* «sin límite hacia atrás» significa dentro de la estadía del primer camión.
- Rige la etiqueta, la fecha de la TRM, el año del consecutivo y el inicio del primer período de almacenamiento.
- Consecutivos de 5 dígitos, con reinicio anual y sin saltos: `2026T00001`, `2026BA00001` (solo importación), `2026EXP00001`, `2026INSP00001`, `2026S00001` (una serie para todas las guías) y `2026OC00001`.
- Tiquetes y depósitos toman el año de la fecha de ingreso; guías y órdenes, el de su emisión.

**DEC-013 — Varios camiones por documento** (Ola 1, WMS-26). Completar el ciclo de un camión no cierra el servicio. Comercio Exterior cierra el ingreso de camiones de forma explícita, sin reapertura. Un camión tardío se registra, entra al stock, se recalcula la factura del período (DEC-022) y se avisa para reimprimir la etiqueta. Un error de facturación nunca bloquea báscula.

**DEC-014 — Unidad de carga** (Ola 2, comentarios de Linear del 2026-09-17).
- La mercancía se declara por unidad de carga, sin mezclar mercancía suelta con unidades en un mismo depósito.
- **Una unidad puede salir parcialmente** (contra el criterio original de que «sale completa»).
- Se cobra por unidad (`PER_CARGO_UNIT`).
- Los tipos de unidad son un catálogo global que amplía el administrador.
- El tanquero es un tipo de unidad, no un embalaje.

**DEC-015 — Unidad de medida y embalaje** (Ola 2, WMS-18). Se imprimen como campos separados. Las unidades de medida son un catálogo que administra el Admin (el enum desapareció).

**DEC-016 — Alcances recortados de la Ola 3** (comentarios de Linear del 2026-09-21):
- **WMS-12 no se implementa.** La etiqueta sigue solo en Comercio Exterior: nada de `LabelAccess` ni de marca «PRELIMINAR».
- **WMS-10 elimina los pesos por producto.** Báscula captura un único peso bruto del manifiesto. Las columnas de peso por producto quedan en `null`, no se borran.
- **WMS-17 conserva la orden de cargue y su flujo.** Solo deja de emitirse su PDF y se registran los datos de la orden externa. No se fusionan las pantallas de orden y guía.

**DEC-017 — Conductor** (QA, 2026-10-05; selector, 2026-10-08).
- En báscula, el conductor se identifica por documento: el mismo documento corrige al conductor, uno distinto busca o crea otro y lo reasigna. Nunca se reescribe al conductor anterior.
- Báscula y Bodega eligen al conductor con un selector paginado. Desde ahí se puede crear o corregir uno en un modal (lápiz con `PATCH /drivers/{id}` y el documento bloqueado).
- No se editan los conductores migrados para probar.

**DEC-018 — Montacargas con IVA opcional** (Ola 1, WMS-28). El servicio `MONTACARGAS` no lleva impuestos configurados. El cobro trae un check «Agregar IVA», desmarcado por defecto, que suma el IVA sobre el valor digitado.

**DEC-019 — Ajustes del plan de corrección** (2026-10-03).
- **D-1:** no se consolidan los cobros «por facturar» de báscula y montacargas.
- **D-2:** se retira «Cambiar modo de pago» del historial de báscula. El modo de pago de una guía sí se puede cambiar (corrección del 2026-10-08).
- CE-7 (ajuste de cantidad) es una operación de Comercio Exterior, no de Bodega, y registra kárdex.
- Repesar la salida responde 409 mientras alguna orden de cargue del camión no esté cargada.
- Un descartado sin salida aparece como «Cancelado» en trazabilidad.

## 3. Facturación

**DEC-020 — La factura de almacenamiento siempre se genera** (2026-07-16). Sin tarifa, o si la regla falla, el cargo usa el valor mínimo de la modalidad; sin mínimo, sale en $0. La advertencia va al detalle de la factura y a una notificación para Facturación, que corrige con un override de línea. Nunca una advertencia sin factura: el operario no tiene cómo regenerarla.

**DEC-021 — No hay creación manual de facturas en el frontend.** El sistema genera las facturas; Facturación asigna el N.º SIIGO, aprueba, envía y registra pagos. La pantalla de creación (`create.vue`), `BillingPreviewPanel.vue` y la consulta `GetStorageInvoiceDraft` se eliminaron; `BillingControllerSurfaceTests` asegura que no vuelvan. No los revivas.

**DEC-022 — Recálculo único de la factura del período** (Ola 1, 2026-09-14). Un solo mecanismo sirve para el camión tardío, la TRM manual y el ajuste CE-7.
- En Borrador o Pendiente de aprobación, la factura se recalcula.
- Aprobada, enviada, vencida o con pagos: se actualiza la misma factura, conserva el N.º SIIGO y se notifica a Facturación con el total anterior y el nuevo. Con pagos queda en Pago parcial si hay saldo, o Pagada con saldo a favor si no.
- Anulada: no se toca.
- Las líneas sobrescritas se reemplazan y la notificación lista el valor descartado.

**DEC-023 — TRM fuera de báscula** (Ola 1, WMS-24).
- Se consulta a la DIAN con la fecha de ingreso al crear la factura del período.
- Si falla, el depósito queda con TRM pendiente y la factura se genera igual. Facturación digita la TRM manual (con motivo) antes de asignar el N.º SIIGO y aprobar.
- Una TRM manual nunca la reemplaza la DIAN, y una de la DIAN no se reemplaza a mano.

**DEC-024 — N.º SIIGO** (Ola 1, WMS-20; QA, 2026-10-05). El número de la factura legal lo asigna Facturación y queda fijo al aprobar. Una factura no fiscal (`IsZeroValue` o total 0) no lleva número fiscal. El diálogo de acciones incluye Enviar y Registrar pago.

**DEC-025 — Fórmulas de almacenamiento** (2026-07-09).
- `PERCENTAGE_OF_VALUE` cobra un % del CIF del lote completo y **no se multiplica por el stock**. Cambiarla alteraría convenios firmados.
- El prorrateo por saldo existe aparte, como `PERCENTAGE_OF_VALUE_PRORATED` (`CIF × CurrentStock / ReceivedQuantity`, base plana, mínimo sin prorratear). **Falta que el cliente confirme cuál aplica**; conviven ambas.
- No se prohíbe ninguna fórmula por lo que le falte al modelo de datos: el cliente cobra por vehículo, por contenedor o por tanquero en convenios reales (hoy `PER_VEHICLE` y `PER_CARGO_UNIT`). Solo `PER_VEHICLE_TYPE` es exclusiva del montacargas.

**DEC-026 — Almacenamiento por regla resuelta** (2026-07-09).
- La unidad de trabajo es el depósito: sus productos con stock se agrupan por la regla que les aplica y cada grupo es un cargo, con una línea en la factura del depósito.
- Las magnitudes del depósito (CIF, contenedores, vehículos) se cobran una sola vez. El CIF de un grupo se prorratea por `ReceivedQuantity`.

**DEC-027 — Tarifa base por producto y modalidad** (2026-07). Cuando no hay convenio, la tarifa sale de `ServicePricingRule`, espejo de `AgreementService`. «Tipo de depósito» es `OperationModality`, no un concepto aparte. El cálculo existe una sola vez.

**DEC-028 — Cantidad facturable en el recálculo** (2026-10-06, DEF-F11-017). El recálculo cobra el stock más las salidas netas por cargue desde que el período tomó su stock (`StorageBillableQuantity`), no el stock actual.

## 4. Permisos

**DEC-030 — Modelo de roles, sin permisos por usuario** (2026-10-07). El sistema sale a producción con los 6 roles y las políticas de `WmsPolicyRoles`. El plan de permisos por usuario queda diferido para una versión posterior (`planes/plan-cerrado-permisos-por-usuario-2026-10-07.md`, con su §11 de correcciones previas). Una necesidad puntual se resuelve con un ajuste chico a `WmsPolicyRoles`, respetando DEC-005. *Por qué:* cambiarlo invalidaría el QA cerrado, los videos, las guías y los scripts, y los operarios están probando con roles.

**DEC-031 — Aflojar por endpoint** (2026-07). Lecturas y catálogos que usan los flujos operativos → `ActiveUser`; escrituras operativas → `OperationalAccess` o la política específica; configuración de tarifas y facturación → restringida. Detalle en `contexto/convenciones-tecnicas.md` §4.

## 5. Migración del legacy y staging

**DEC-040 — Fuente y corte simulado** (2026-10-06).
- La fuente es `db_legacy/backupBodegas.sql`; `db.sql` está truncado.
- Corte simulado: `ultimo_fin_facturado = 2026-09-30`, y la facturación arranca el 2026-10-01.
- El corte real exige un volcado nuevo y repetir las fases 1 y 3 del plan de migración.

**DEC-041 — Tarifas aprobadas para la migración** (2026-10-06/07).
- T1: almacenamiento IMP al 0,295 % con mínimo de $50.000 con IVA.
- T2: mínimo IMP de $50.000.
- T3: báscula $16.806,72 + IVA.
- T4: guía $15.000 (el v2 la cobra aunque el legacy no lo hacía).
- Montacargas: tractomula 220.000, doble troque 150.000, sencillo 140.000, turbo 110.000, guacal/estiba 40.000, con IVA según el check.

**DEC-042 — Staging como ambiente de operarios** (2026-10-07). No se restauró el punto previo: los datos de QA (S6) quedan como ejemplo y hay datos de práctica `PRAC-`. Cuentas por rol `operario.*` y `qa.*`. La medición PRF-002 la hace un operario real.

## 6. Respuestas a la auditoría de paridad (2026-10-23)

Respuestas del usuario a las diferencias con el legacy que no tenían decisión, en `analisis/auditoria-paridad-integral-2026-10-23/06-brechas-priorizadas.md` §3.1. Lo marcado **«Se construye»** necesita un plan cerrado antes del código (`DEC-001`). Lo demás confirma el comportamiento actual de V2.

**DEC-050 — Báscula** (2026-10-23).
- **La orden de cargue va antes de la salida** (BR-02-001). Báscula no pesa la salida sin una orden de cargue existente. No se vuelve al flujo legacy de «pesar primero y completar después».
- **«Solo báscula» sin cliente obligatorio** (BR-02-002). **Se construye.** Como en el legacy, se puede pesar sin cliente registrado; el cobro va al conductor o al consumidor final.
- **Qué corrige Báscula después de guardar** (BR-02-010). Solo pesos (con motivo), fecha del pesaje, observación del tiquete y datos del conductor y del vehículo. Comercio Exterior corrige documento, mercancía y cantidades mientras el depósito está en Borrador. Lo demás se anula y se repite. Se mantienen DEF-F3-018 y la D-2 de `DEC-019`.
- **Camión con varios documentos: el operario elige** (BR-02-013). **Se construye.** Por defecto, un solo pesaje (Bruto y Tara) para todos los depósitos del camión, como en el legacy. Si descarga en puntos distintos, un pesaje intermedio por depósito, como hoy. *Lo resuelve el plan:* cómo se reparte el neto entre los depósitos cuando hay un solo pesaje.

**DEC-051 — Depósitos** (2026-10-23).
- **Límite de la corrección de la fecha de ingreso** (BR-04-002; precisa `DEC-012`). Se corrige solo dentro de la estadía del primer camión: no antes de su ingreso en Vigilancia ni después de su salida. Para ir más atrás se corrige primero el ingreso de Vigilancia (WMS-5). Es lo que hace hoy el código; no hay cambio.
- **Camión tardío a un depósito agotado** (BR-04-001). Un depósito cerrado por agotamiento no recibe más camiones: el camión nuevo con el mismo documento abre otro depósito. `DEC-013` aplica a depósitos en Borrador o Confirmado.
- **Una etiqueta por depósito** (BR-04-012). No se construye la etiqueta por vehículo del legacy (`adhesivovehiculo.php`).

**DEC-052 — Salidas** (2026-10-23).
- **Bloqueo manual de salidas por cliente** (BR-05-004). **Se construye.** Una marca «sin salidas» en el tercero, con motivo y auditoría, que impide crear órdenes de cargue y emitir guías, aparte del bloqueo por mora. Es el `cliente.sinsalidas` del legacy. *Lo resuelve el plan:* qué roles la ponen y la quitan (`DEC-005`, `DEC-031`).
- **Guía antes del cargue, con aviso** (BR-05-006). **Se construye.** La guía se sigue pudiendo emitir antes del cargue. Si lo cargado difiere de lo que dice la guía, se avisa a Comercio Exterior para que la anule y la emita de nuevo.

**DEC-053 — Facturación** (2026-10-23).
- **«Depósitos pendientes» incluye los cerrados con trabajo pendiente** (BR-06-003). **Se construye.** Como en el legacy, un depósito sigue en la lista mientras tenga una factura de almacenamiento en Borrador sin N.º SIIGO o una anulada sin refacturar, aunque ya no tenga un período abierto.
- **La renovación cobra el saldo al inicio del período** (BR-06-005). **Se construye.** El período renovado cobra la cantidad facturable al día de su inicio (fin + 1), aunque el job corra después, con el mismo criterio de `DEC-028`. Afecta a las fórmulas por cantidad; `PERCENTAGE_OF_VALUE` no cambia.

**DEC-054 — Reportes y agencias** (2026-10-23).
- **Diario de ingresos con el formato legacy** (BR-07-002). **Se construye.** Agrupado por depósito, con agencia e importador. Lleva una fila por camión con el manifiesto DIAN y el peso de manifiesto, el total de vehículos y las firmas («Jefe de Bodega», «Recibí conforme DIAN», «Firma Funcionario»), en pantalla, PDF y Excel.
- **Las agencias no consultan por su cuenta** (BR-08-008). No hay acceso externo para las agencias de aduanas: Comercio Exterior genera el reporte de ingresos por agencia y se lo envía.

## 7. Documentos impresos

**DEC-060 — Código QR de verificación en la guía de salida** (2026-10-23, pedido del cliente).
- **Objetivo:** evitar guías adulteradas.
- **Qué imprime la guía:** un **código QR** con un enlace de verificación firmado, o el código de barras de siempre, según el parámetro `GUIDE_CODE_TYPE` (`QR` o `BARCODE`), que edita el Admin. El código de barras se conserva en el código.
- **Valor inicial:** `QR`.
- **Verificación:** al escanear el QR se abre una página pública, sin iniciar sesión. Muestra los datos mínimos de la guía para cotejarlos con el papel: número, fechas, estado vigente o anulada, depósito, destino, productos y cantidades, y la placa parcialmente oculta. Nunca muestra datos de personas (`DEC-007`).
- **Fuente:** el usuario, en el plan `planes/plan-cerrado-brechas-paridad-p1-2026-10-23.md` (fase 11, D35–D42).
