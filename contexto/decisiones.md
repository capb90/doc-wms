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
| DEC-040…049 | Migración del legacy y staging |
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
1. **Báscula rápida:** la meta son ~30 s por camión, como en el legacy. Pantalla única con cola (WMS-31). *Precisada por `DEC-058` (2026-10-26): la cola ocupa la página y el proceso se abre en un panel propio sobre ella; la meta de ~30 s sigue.*
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

**DEC-015 — Unidad de medida y embalaje** (Ola 2, WMS-18). Se imprimen como campos separados. Las unidades de medida son un catálogo que administra el Admin (el enum desapareció). *Precisada por `DEC-057` (2026-10-26): la tarjeta va como el legacy (Ampara · Saldo · Mercancía, embalaje dentro del texto, sin unidad); el PDF del depósito y la guía siguen igual.*

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
- El prorrateo por saldo existe aparte, como `PERCENTAGE_OF_VALUE_PRORATED` (`CIF × CurrentStock / ReceivedQuantity`, base plana, mínimo sin prorratear). **Falta que el cliente confirme cuál aplica**; conviven ambas. *Precisada por `DEC-029` (2026-10-25): la prorrateada es la fórmula por defecto; la de lote completo queda para los convenios que la pidan. La base es el valor de la mercancía (FOB del ingreso), no el CIF.*
- No se prohíbe ninguna fórmula por lo que le falte al modelo de datos: el cliente cobra por vehículo, por contenedor o por tanquero en convenios reales (hoy `PER_VEHICLE` y `PER_CARGO_UNIT`). Solo `PER_VEHICLE_TYPE` es exclusiva del montacargas.

**DEC-026 — Almacenamiento por regla resuelta** (2026-07-09).
- La unidad de trabajo es el depósito: sus productos con stock se agrupan por la regla que les aplica y cada grupo es un cargo, con una línea en la factura del depósito.
- Las magnitudes del depósito (CIF, contenedores, vehículos) se cobran una sola vez. El CIF de un grupo se prorratea por `ReceivedQuantity`.

**DEC-027 — Tarifa base por producto y modalidad** (2026-07). Cuando no hay convenio, la tarifa sale de `ServicePricingRule`, espejo de `AgreementService`. «Tipo de depósito» es `OperationModality`, no un concepto aparte. El cálculo existe una sola vez.

**DEC-028 — Cantidad facturable en el recálculo** (2026-10-06, DEF-F11-017). El recálculo cobra el stock más las salidas netas por cargue desde que el período tomó su stock (`StorageBillableQuantity`), no el stock actual.

**DEC-029 — FOB, CIF y tarifas del almacenamiento por porcentaje** (2026-10-25). Respuestas del usuario a las 10 decisiones del §7 de `analisis/analisis-fob-cif-legacy-v2-2026-10-24.md`. Precisa `DEC-025` y `DEC-041`. Lo marcado **«Se construye»** necesita plan cerrado (`DEC-001`).
- **Base del cobro: el FOB del ingreso** (§7.1). El porcentaje se cobra sobre el valor que se captura en el depósito, que en los migrados es `ingreso.preciomercancia` (FOB). No se captura el CIF al ingreso. *Por qué:* el historial no distingue las bases (0,7 % de diferencia), el CIF no se conoce al ingreso y los porcentajes se calibran sobre lo que ya está en los datos.
- **El levante es CIF, como en el legacy** (§7.2). **Se construye.** El valor del levante se pide y se rotula «CIF» en el formulario, los listados, el detalle del depósito, el kárdex y la póliza («CIF UAP» y «CIF no UAP»). La póliza se liquida sobre ese CIF. Se corrige la premisa «el legacy rotula CIF pero suma el FOB» de `PolicySummaryCalculator` y `pages/reports/policies.vue`. Los datos migrados no cambian: `levante.fob_dolares` ya es el CIF. Los nombres de columna (`FobUsd`, `FobCop`) se pueden conservar.
- **El depósito guarda un solo valor, con nombre neutro** (§7.3). **Se construye** (solo textos). Se rotula «Valor de la mercancía» en captura, detalle, fórmula, umbral, glosario y textos de facturación. Se documenta que equivale al FOB del ingreso. Desaparecen «Valor Comercial», «Valor declarado», «Umbral CIF» y «CIF» referidos al depósito. Sin campo nuevo ni migración.
- **El valor solo se corrige en Borrador** (§7.4). Se mantiene como hoy: CE devuelve el depósito a Borrador y la factura del período se recalcula (`DEC-056`).
- **Fórmula prorrateada por defecto** (§7.5; cierra la pregunta abierta de `DEC-025`). `PERCENTAGE_OF_VALUE_PRORATED` es la fórmula de la tarifa base de almacenamiento y la de los acuerdos nuevos. `PERCENTAGE_OF_VALUE` (lote completo) sigue disponible para un convenio que lo diga expresamente.
- **Acuerdos por cliente calibrados y validados** (§7.6). Se genera la lista de porcentajes calibrados por cliente, fuera del repo (`DEC-007`), y Facturación la coteja con los convenios reales, empezando por los 29 clientes que concentran el 80 % de las quincenas. Solo lo validado se carga como acuerdo en V2. Regenerar la lista exige consultar el volcado con aprobación del usuario.
- **Tarifa base para clientes sin acuerdo: la define Facturación** (§7.7; precisa T1 de `DEC-041`). Prorrateada y menor que T1, con el 0,141 % neto como referencia y el mismo mínimo de $50.000 con IVA. Facturación fija el porcentaje con su tarifa pública vigente.
- **Valor del levante una sola vez, con bloqueo** (§7.8). **Se construye.** El valor va en el primer producto del levante. Si el número de levante ya tiene valor en otro producto, el siguiente se guarda con valor 0: el aviso DF4 pasa a bloqueo (backend y formulario). La migración ya lo hace así (`LegacyReleaseFobSplitter`).
- **Exportación e inspección** (§7.9). Capturan el mismo «Valor de la mercancía», sin cambios. Facturación confirma si algún convenio de esas modalidades cobra por porcentaje; si ninguno, el valor queda informativo.
- **Antes de facturar en producción** (§7.10). T1 se reemplaza por la tarifa base de §7.7, se cargan los acuerdos validados y se factura **un mes en paralelo** con el sistema actual, comparando por cliente. Mientras tanto, staging sigue facturando con T1 a los clientes sin acuerdo.
- **Fuente:** el usuario, en la sesión del 2026-10-25, opción por opción.
- **Construido** (§7.2, §7.3, §7.5 en el formulario y §7.8) con `planes/plan-cerrado-dec-029-fob-cif-2026-10-25.md`: BE `dafd573` (migración `RenameValueFormulaLabels`), FE `d838535`; docs y verificación local el 2026-10-25. Sin desplegar en staging.

## 4. Permisos

**DEC-030 — Modelo de roles, sin permisos por usuario** (2026-10-07). El sistema sale a producción con los 6 roles y las políticas de `WmsPolicyRoles`. El plan de permisos por usuario queda diferido para una versión posterior (`planes/plan-cerrado-permisos-por-usuario-2026-10-07.md`, con su §11 de correcciones previas). Una necesidad puntual se resuelve con un ajuste chico a `WmsPolicyRoles`, respetando DEC-005. *Por qué:* cambiarlo invalidaría el QA cerrado, los videos, las guías y los scripts, y los operarios están probando con roles.

**DEC-031 — Aflojar por endpoint** (2026-07). Lecturas y catálogos que usan los flujos operativos → `ActiveUser`; escrituras operativas → `OperationalAccess` o la política específica; configuración de tarifas y facturación → restringida. Detalle en `contexto/convenciones-tecnicas.md` §4.

## 5. Migración del legacy y staging

**DEC-040 — Fuente y corte simulado** (2026-10-06).
- La fuente es `db_legacy/backupBodegas.sql`; `db.sql` está truncado.
- Corte simulado: `ultimo_fin_facturado = 2026-09-30`, y la facturación arranca el 2026-10-01.
- El corte real exige un volcado nuevo y repetir las fases 1 y 3 del plan de migración.

**DEC-041 — Tarifas aprobadas para la migración** (2026-10-06/07).
- T1: almacenamiento IMP al 0,295 % con mínimo de $50.000 con IVA. *Precisada por `DEC-029`: antes de facturar en producción, T1 se reemplaza por la tarifa base prorrateada que defina Facturación.*
- T2: mínimo IMP de $50.000.
- T3: báscula $16.806,72 + IVA.
- T4: guía $15.000 (el v2 la cobra aunque el legacy no lo hacía).
- Montacargas: tractomula 220.000, doble troque 150.000, sencillo 140.000, turbo 110.000, guacal/estiba 40.000, con IVA según el check.

**DEC-042 — Staging como ambiente de operarios** (2026-10-07). No se restauró el punto previo: los datos de QA (S6) quedan como ejemplo y hay datos de práctica `PRAC-`. Cuentas por rol `operario.*` y `qa.*`. La medición PRF-002 la hace un operario real. *Reemplazada en los datos y las cuentas por `DEC-043` cuando se ejecute su reinicio.*

**DEC-043 — Staging limpio con los datos del legacy para las pruebas de los operarios** (2026-10-27). Respuestas del usuario antes de la fase 13 del plan P1. Reemplaza los datos y las cuentas de `DEC-042`, precisa el corte de `DEC-040` y es la excepción aprobada a `DEC-006` para recrear la base de staging una vez.
- **Staging se recrea vacío y se migra de nuevo** con la herramienta de importación actual, después de la QA de la fase 13. No se restaura el respaldo del 6/10, porque lo cargó la herramienta vieja: sin año del depósito ni prórroga, y con el levante anterior a `DEC-029`. Antes se ensaya en local, en `wms_migracion`.
- **La fuente sigue siendo `backupBodegas.sql`** (junio de 2024). Los CSV de depósitos y levantes se regeneran con las consultas actuales, que traen la prórroga y el año. **El corte simulado pasa al día anterior al reinicio:** la facturación de cada depósito vivo arranca el día del reinicio, sin períodos atrasados.
- **Convenios:** una propuesta calibrada por cliente, con el método de `DEC-029` §7.6. Facturación la valida y solo lo validado se carga.
- **Para los operarios:** el Admin y una cuenta `operario.*` por rol, con cambio de contraseña al entrar, más las tarifas, los parámetros y los respaldos. **Sin datos de práctica ni de QA, y sin cuentas `qa.*`.** Los operarios registran sus propios camiones desde Vigilancia.
- **Plan:** `planes/plan-cerrado-staging-limpio-legacy-2026-10-27.md`.
- **Fuente:** el usuario, en la sesión del 2026-10-27, opción por opción.

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
- **Una etiqueta por depósito** (BR-04-012). No se construye la etiqueta por vehículo del legacy (`adhesivovehiculo.php`). *Reabierto por `DEC-057` (2026-10-26): se construye la tarjeta por vehículo, además de la del depósito.*

**DEC-052 — Salidas** (2026-10-23).
- **Bloqueo manual de salidas por cliente** (BR-05-004). **Se construye.** Una marca «sin salidas» en el tercero, con motivo y auditoría, que impide crear órdenes de cargue y emitir guías, aparte del bloqueo por mora. Es el `cliente.sinsalidas` del legacy. *Lo resuelve el plan:* qué roles la ponen y la quitan (`DEC-005`, `DEC-031`).
- **Guía antes del cargue, con aviso** (BR-05-006). **Se construye.** La guía se sigue pudiendo emitir antes del cargue. Si lo cargado difiere de lo que dice la guía, se avisa a Comercio Exterior para que la anule y la emita de nuevo. *Precisada por `DEC-056`:* en importación la guía es obligatoria antes del cargue.

**DEC-053 — Facturación** (2026-10-23).
- **«Depósitos pendientes» incluye los cerrados con trabajo pendiente** (BR-06-003). **Se construye.** Como en el legacy, un depósito sigue en la lista mientras tenga una factura de almacenamiento en Borrador sin N.º SIIGO o una anulada sin refacturar, aunque ya no tenga un período abierto.
- **La renovación cobra el saldo al inicio del período** (BR-06-005). **Se construye.** El período renovado cobra la cantidad facturable al día de su inicio (fin + 1), aunque el job corra después, con el mismo criterio de `DEC-028`. Afecta a las fórmulas por cantidad; `PERCENTAGE_OF_VALUE` no cambia.

**DEC-054 — Reportes y agencias** (2026-10-23).
- **Diario de ingresos con el formato legacy** (BR-07-002). **Se construye.** Agrupado por depósito, con agencia e importador. Lleva una fila por camión con el manifiesto DIAN y el peso de manifiesto, el total de vehículos y las firmas («Jefe de Bodega», «Recibí conforme DIAN», «Firma Funcionario»), en pantalla, PDF y Excel.
- **Las agencias no consultan por su cuenta** (BR-08-008). No hay acceso externo para las agencias de aduanas: Comercio Exterior genera el reporte de ingresos por agencia y se lo envía.

**DEC-055 — Ajustes tras la ejecución del plan de brechas P1** (2026-10-24). Respuestas del usuario a las observaciones del orquestador (`planes/registro-ejecucion-brechas-p1-2026-10-24.md`, «Decisiones para el usuario»). Lo marcado **«Se construye»** necesita plan cerrado (`DEC-001`).
- **Tiquete cobrado a consumidor final.** El tiquete nombra a quien se facturó, aunque el depósito tenga cliente: con un cobro a consumidor final dice «Consumidor Final». Se acepta lo que hace hoy `TicketRecipient` (fase 4, D12), que reemplaza el criterio de CHG-84 para este caso.
- **Depósito agotado en la gracia** (precisa `DEC-053`). **Se construye.** Si un depósito se agota por completo en los días de gracia y tenía mercancía al cierre del día de inicio del período nuevo (S), ese período se abre con esa cantidad, se factura y se cierra por agotamiento. Hoy `CloseDepletedProductPeriodsAsync` cierra el período viejo sin renovarlo. Lo que sale el mismo día S sigue sin cobrarse (D19 del plan).
- **Auditoría de los procesos automáticos.** Los jobs (activación de convenios, renovaciones, mora, conciliación, abandono) **no** dejan `audit_logs`. Bastan las fechas en la entidad, los avisos y los logs del servidor.
- **Precios de servicio programados.** **Se construye.** Se acepta registrar un precio con vigencia futura (día en hora de Colombia). El vigente rige hasta esa fecha y el nuevo entra solo (`Service.SetPrice` ya lo soporta desde la fase 6). La lista de precios lo muestra «Programado». Se relaja `SetServicePriceValidator`.

**DEC-056 — Guía antes del cargue de importación y cambio de cliente con factura** (2026-10-25). Respuestas del usuario a las propuestas P1 y P2 del plan `planes/plan-cerrado-correccion-def-f11-030-034-2026-10-25.md` (DEF-F11-030 y DEF-F11-034).
- **Guía antes del cargue de importación** (precisa `DEC-052`). Bodega no ejecuta el cargue de una orden de importación sin guía de salida vigente: responde 409 y no mueve stock. El conductor pide la guía en Comercio Exterior antes del cargue, y el operario de bodega la valida en la pantalla del cargue, que muestra el número vigente o el aviso y no deja ejecutar. La guía ya no puede emitirse después del cargue. Exportación (guía automática) e inspección (sin guía) no cambian.
- **Vigilancia y Báscula no agregan controles.** Hay una sola salida y un operario que atiende entradas y salidas: su operación sigue siendo rápida. *Riesgo aceptado:* un camión que se salta la báscula sale con guía pero sin pesaje ni cobro de báscula, y la orden queda cargada sin despachar. Las guardas de CHG-33 siguen para las órdenes cargadas sin guía de antes del cambio.
- **Cambio de cliente del depósito con factura de almacenamiento.**
  - Con la factura del período en Borrador y no consolidada, la factura y sus períodos pasan al cliente nuevo y se recalculan con su convenio.
  - Con la factura en otro estado, o consolidada, se rechaza: Facturación debe anularla antes.
  - Con la factura anulada sin refacturar, los períodos pasan al cliente nuevo y la refacturación sale a su nombre.
- **Corrección en Borrador.** Corregir valor, moneda, agencia o fecha de ingreso de un depósito devuelto a Borrador recalcula al momento la factura del período abierto (`DEC-022`); la reconfirmación no recalcula.
- **Fuente:** el usuario, al aprobar el plan (2026-10-25): «la operación en vigilancia y bascula debe ser rapida como esta actualmente. El operario de bodega puede validar la guia de salida.»

**DEC-057 — Hallazgos de los operarios en staging** (2026-10-26). Respuestas del usuario a las decisiones de `analisis/hallazgos-operarios-2026-10-26.md`, sobre el informe de hallazgos que Bodegas Asociadas envió tras probar staging (build del 2026-10-08). Lo marcado **«Se construye»** necesita plan cerrado (`DEC-001`).
- **La carta porte la confirma el operario** (H7). **Se construye.** Si el número y tipo de documento ya tienen depósitos abiertos, Báscula los muestra con cliente, importador, transportadora, fecha del documento y placas. El operario elige uno o «Es otro documento: crear depósito nuevo». Nada se asocia solo. Reemplaza la decisión P1 de `planes/paridad-legacy/plan-backend-paridad-legacy.md` (asociación automática por número y tipo). *Por qué:* hoy un camión de otro cliente con el mismo número entra al depósito equivocado, y un depósito sin fecha casa con cualquier fecha.
- **Pesos del legacy en Báscula** (H3). **Se construye.** El formulario de ingreso muestra siempre P. indicador, T. vehículo, P. manifiesto y P. mercancía, y calcula la tara al digitar el manifiesto: mercancía = manifiesto y tara = indicador − mercancía. *Por definir en el plan:* con segundo pesaje, el neto real reemplaza a la mercancía deducida (el neto por diferencia de pesajes no se pierde).
- **Tiquete de báscula en $0 solo por convenio** (H5b). **Se construye.** Si el convenio del cliente fija la báscula en $0, el cobro sale en cero, sin número fiscal (`DEC-024`) y marcado «sin cobro por convenio». El operario no puede digitar 0 a mano.
- **Fecha y tipo del documento en la tarjeta, y mercancía sin duplicar** (H13, H14). **Se construye.**
  - La tarjeta imprime «{tipo de documento}: {número} ({fecha del documento})», con «N/A» si no hay fecha, en lugar de la fecha de ingreso y del rótulo fijo «Carta Porte».
  - La descripción del producto no se imprime si es igual al nombre (sin importar mayúsculas, espacios ni tildes) o si el nombre ya la contiene: tarjeta, PDF del depósito y guía de salida.
- **Manifiesto obligatorio en Báscula** (H2). **Se construye.** El número y el peso del manifiesto del camión son obligatorios al registrar un ingreso a depósito (importación, exportación e inspección). Solo báscula y Salida no lo piden. Reemplaza la decisión P2 / BAS-01 del plan de paridad (opcional en Báscula, exigido al confirmar).
- **Manifiesto DIAN al confirmar la importación.** **Se construye.** Pasa a ser requisito de confirmación del depósito de importación, como en el legacy. Los migrados y los ya confirmados no cambian.
- **El cobro de un tiquete guardado no se edita en Báscula** (H5c). Se mantiene `DEC-050` (anular y repetir; Facturación ajusta en Borrador). **Se construye:** se monta para Facturación el diálogo de cambio de destinatario de la factura (BR-06-007).
- **Sin «Transportadora» en la tarjeta** (H10). **Se construye.** Se quita de las tarjetas de importación, exportación e inspección, como en el legacy. Reemplaza lo pedido en WMS-11; el caso F5-ETI-001 se ajusta.
- **Tarjeta por vehículo** (H12; reabre la etiqueta única de `DEC-051`). **Se construye.** Además de la tarjeta del depósito, una por cada camión: mismo encabezado, la placa y solo la mercancía y cantidades que ingresó ese camión, como `adhesivovehiculo.php`.
- **Columnas de la tarjeta como el legacy** (H15; precisa `DEC-015` para la tarjeta). **Se construye.** Ampara · Saldo · Mercancía, con el embalaje dentro del texto («CEBOLLA FRESCA (SACOS)») y sin unidad. El PDF del depósito y la guía siguen con unidad y embalaje separados. *Riesgo aceptado:* con unidades mixtas en un depósito, la tarjeta no dice la unidad del Ampara.
- **Orden:** un plan cerrado con todo lo anterior se ejecuta **antes** de la fase 13 del plan de brechas P1, y la fase 13 despliega todo junto. Mientras tanto se manda a los operarios una nota de capacitación con lo que ya existe (H1, H4, H5a y H6).
- **Sin cambios** (ya existen o son de datos): el tipo de vehículo ya es obligatorio en Báscula (H1); la fecha de ingreso se corrige en Vigilancia y luego en el depósito (H4); el tiquete con error se anula o se descarta (H5a); el cliente que no aparece se habilita con el rol Cliente en «Terceros» (H6).
- **Fuente:** el usuario, en la sesión del 2026-10-26, opción por opción.
- **Construido** (2026-10-26) con `planes/plan-cerrado-dec-057-hallazgos-operarios-2026-10-26.md`: BE `c2239cd`, `543fe7f` y `a8d06dd` (migración `AddLabelPrintEntry`); FE `0948d62` y `18f79f1`; verificado en local sobre `wms_qa_preprod`. Sin desplegar: va con la fase 13 del plan P1.


**DEC-058 — Ajustes visuales antes de la fase 13** (2026-10-26). Pedido del usuario al revisar DEC-057, con sus respuestas a las preguntas del plan `planes/plan-cerrado-correccion-dec-057-2026-10-26.md` (§1.2–§1.4). **Se construye** con ese plan.
- **Páginas uniformes.** Todas las páginas del menú usan el mismo esqueleto:
  - un encabezado común: tarjeta con título `h1`, subtítulo y acciones a la derecha, con el «Nuevo …» primario;
  - los filtros en su propia tarjeta, con etiquetas y búsqueda con espera;
  - la tabla con el mismo estilo y paginador.
  Se crea un componente de encabezado compartido y una prueba que lo exige. `billing/configurations` es la referencia, corregida en sus puntos débiles. Quedan fuera los formularios de creación, los detalles y el centro de ayuda.
- **Báscula: cola a todo el ancho y proceso en un panel propio tipo modal.**
  - La cola es una tabla con placa, estado, motivo, cliente, conductor, modalidad, manifiesto, primer peso y espera.
  - Al elegir un camión, el proceso se abre en un panel grande sobre la cola, con fondo oscurecido.
  - El panel **no es un diálogo de PrimeVue**: no se desmonta, así que lo digitado no se pierde, y Enter y F2 siguen funcionando.
  - Escape no lo cierra; se cierra con «Volver a la cola», que conserva el borrador.
  - Los pasos siguen en línea dentro del panel (DF5 del plan de paridad del frontend no cambia).
  - Reemplaza «pantalla única con cola» de `DEC-010` (1).
- **Tablero de depósitos de CE.**
  - Cada estado es una columna con scroll propio y carga infinita, sin paginación.
  - Cada columna tiene su buscador: documento comercial, número de depósito, tercero y producto.
  - Arriba quedan solo el tipo de depósito y las fechas; se quitan el buscador general de número y el selector de estado.
- **Fuente:** el usuario, en la sesión del 2026-10-26.
- **Construido** (2026-10-26) con `planes/plan-cerrado-correccion-dec-057-2026-10-26.md`: BE `911399c` (búsqueda del tablero); FE `3d4056b` (páginas uniformes), `1fbcc8a` (báscula) y `e1e871a` (tablero); el mismo plan corrigió la revisión de `DEC-057` (BE `7189676`, FE `543502d`). Sin migración; verificado en local sobre `wms_qa_preprod`. *Precisiones del usuario al construir:* la columna «manifiesto» de la cola se rotula «Documento», porque el dato es el número del documento del servicio y no el manifiesto del camión; «Guardar» va en el encabezado del panel, sin pie pegajoso. Sin desplegar: va con la fase 13 del plan P1.
- **Validación corregida** (2026-10-26) con `planes/plan-cerrado-correccion-validacion-dec-058-2026-10-26.md` (R1–R10): FE `345cc44` (báscula: encabezado durante la carga, teclas de la cola, foco del panel, historial, «Atrás» con ventanas y modo oscuro) y FE `a0db12b` (título de Terceros con el filtro de Roles, los botones de navegación vuelven a ser enlaces y el error del informe de báscula). Sin migración; verificado en local.

## 7. Documentos impresos

**DEC-060 — Código QR de verificación en la guía de salida** (2026-10-23, pedido del cliente).
- **Objetivo:** evitar guías adulteradas.
- **Qué imprime la guía:** un **código QR** con un enlace de verificación firmado, o el código de barras de siempre, según el parámetro `GUIDE_CODE_TYPE` (`QR` o `BARCODE`), que edita el Admin. El código de barras se conserva en el código.
- **Valor inicial:** `QR`.
- **Verificación:** al escanear el QR se abre una página pública, sin iniciar sesión. Muestra los datos mínimos de la guía para cotejarlos con el papel: número, fechas, estado vigente o anulada, depósito, destino, productos y cantidades, y la placa parcialmente oculta. Nunca muestra datos de personas (`DEC-007`).
- **Fuente:** el usuario, en el plan `planes/plan-cerrado-brechas-paridad-p1-2026-10-23.md` (fase 11, D35–D42).
