# Plan cerrado — Fase 2 · F06 Salidas de mercancía

> **Fecha:** 26 de noviembre de 2026. **Estado:** Aprobado por el usuario el 2026-11-26 («Aprobar»). Sin ejecutar: el backend y la maquetación ya pueden arrancar en paralelo desde `fase-2` (I-05 y el plan de `AppAlertIcon` ya están fusionados). En D9 se conservan el emisor y la fecha de la orden del cliente, opcionales. **Revisado el 2026-11-27** contra lo que llegó después a `fase-2` (§1.9).
> **Origen:**
> - `DEC-080` y el análisis funcional `levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md` (§3.7 completo; de §2.2 las reglas «f» y las pantallas P-BOD-06 a P-BOD-09; de §2.3 las reglas «f» de las salidas y las pantallas P-CE-08 y P-CE-11; de §2.4 el cobro de la guía), con los wireframes `fase_2-mockups/bodega.html` (P-BOD-06 a P-BOD-09), `comercio-exterior.html` (P-CE-02, P-CE-08 y P-CE-11) y `transversales.html` (P-TR-02, P-TR-03, P-TR-09 y P-TR-11), y las fuentes del usuario `levantamiento_staging/salidas_arquitectura.md`, la parte «Ordenes de cargue (Salidas)» de `levantamiento_staging/bodega_ajustes.md` y el mockup `levantamiento_staging/mockups/orden_de_salida_bodega/` (MK-10);
> - el plan maestro `planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md` (M1 a M25, `DEC-081`; en especial M13, M15, M18 y M24);
> - AF dueñas (4, plan maestro §3.1): AF-67, AF-89, AF-97 y AF-106;
> - lo integrado de F01 (D1 a D47, contrato C-F01 y notas de la fase 5 y de I-01), de F02 (D1 a D21 y los ajustes de su QA), de F03 (D1 a D45, contrato C-F03 y sus ajustes), de F04 (D1 a D47, contrato C-F04 y sus ajustes de UI) y de F05 (D1 a D49, contrato C-F05 y sus ajustes de UI, D1 a D36), y el plan de `AppAlertIcon` en F01 a F04;
> - las respuestas del usuario a la ronda de preguntas de este plan (2026-11-26), en D1 a D9.
>
> **Base:** BE `fase-2` `348ab15` · FE `fase-2` `3531432` (las dos con I-05 fusionada) · docs `main` `6b1f2cf`. **Revisión** (§1.9): BE `fase-2` `996828e` · FE `fase-2` `8884936` · docs `main` `f98bd7b`. Rama: `f2/f06-salidas` en BE y FE.
> **Partes:** 0 (contrato, §2) · 1 (backend, dos fases) · 2 (maquetación, tres fases y la revisión del usuario) · 3 (I-06, dos fases, §13). **Migraciones:** `RemoveExitCustomerOrderNumber` (BE-2); BE-1, ninguna.
> **Rutas:** relativas a `code_workspace/`. Prefijos: `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`; `A/` = el análisis; `PM/` = el plan maestro; `P01/` = `D/planes/sprint-11/f01-nucleo/plan-cerrado-f2-f01-nucleo-2026-11-21.md`; `P02/` = `D/planes/sprint-11/f02-base/plan-cerrado-f2-f02-base-2026-11-21.md`; `P03/` = `D/planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-bascula-2026-11-24.md`; `P04/` = `D/planes/sprint-11/f04-bodega/plan-cerrado-f2-f04-bodega-2026-11-25.md`; `P05/` = `D/planes/sprint-11/f05-comercio-exterior/plan-cerrado-f2-f05-comercio-exterior-2026-11-25.md`; `AUI5/` = `D/planes/sprint-11/f05-comercio-exterior/plan-cerrado-f2-f05-ajustes-ui-2026-11-26.md`; `MK/` = `D/levantamiento_staging/mockups/`.

**Cómo leer este plan.** El ejecutor de cada parte lee §0, §1, §2.1 (índice) y la sección de su fase en §8. Cada fase de §8 nombra sus decisiones, sus endpoints (con la ficha de §2.2 y el esquema de §2.3 que le tocan), sus archivos (§3) y sus casos QA (§6). El resto se lee solo cuando la fase lo cita. Las líneas citadas son de la base (`348ab15` y `3531432`); las de la orden de cargue de hoy, de `develop`, donde se dice.

---

## 0. Instrucciones para el ejecutor

1. **Lecturas mínimas:** `D/README.md`, el `AGENTS.md` de tu repo (su sección «Eficiencia de contexto y cierres por fase» rige tu trabajo), `D/procesos/flujo-de-trabajo-agentes.md`, `PM/` §1.2, §5 y §6, y de este plan §0, §1, §2.1 y tu fase en §8. El frontend lee además `D/contexto/convenciones-tecnicas.md` §3 (drawer de detalle, tablas de listado, aviso junto a un dato y páginas que no son listados).
2. **Rama y git** (`PM/` §5.3): `git fetch`; si `develop` avanzó, fusiona `develop` en `fase-2`; crea `f2/f06-salidas` desde `fase-2` (o retómala si ya existe) y trabaja ahí. El backend sale de `fase-2` con I-05 fusionada (ya lo está: `348ab15`). **El frontend sale de `fase-2` cuando también esté fusionado el plan de `AppAlertIcon` en F01 a F04** (`D/planes/sprint-11/plan-cerrado-f2-alert-icon-f01-f04-2026-11-26.md`, rama `f2/ui-alert-icon`), con lo que haya en `fase-2` en ese momento. Al cerrar cada fase: commit con el mensaje de §12 y push de la rama. Sin `push --force`. La fusión en `fase-2` la hace I-06 (§13), en los dos repos a la vez.
3. **Una fase por turno** (`PM/` §6): cierra la fase con sus compuertas, el commit, el push y el estado en §8 y en la matriz, y te detienes con el reporte.
4. **Migraciones:** solo con `dotnet ef … --project Wms.Infrastructure --startup-project Wms.Api` y solo contra la base local (`DEC-004`, M6). BE-2 lleva la de §4; BE-1 no lleva ninguna, y si `has-pending-model-changes` no sale limpio, te detienes y preguntas. Antes de generarla, trae lo último de `fase-2`. Nunca edites a mano `Migrations/*`, los `*.Designer.cs` ni el snapshot.
5. **Líneas citadas:** confírmalas con grep antes de cambiar. Si el código no coincide (ruta, firma o comportamiento), detente y pregunta con todas las dudas en un solo mensaje. Si un caso borde choca con una Dn, gana la Dn y lo mencionas en una línea (`DEC-002`).
6. **Contrato:** §2 es la única fuente del frontend para F06 (`PM/` R3). Cada endpoint nuevo o modificado de tu fase tiene al menos una prueba de integración que verifica su respuesta y sus mensajes de error (`PM/` §6.1). Un mensaje cambia solo si cambias el contrato, y eso exige preguntar.
7. **Suite de integración:** la base es compartida y la cola de báscula corta en 100 camiones (trampa 12 de `D/contexto/convenciones-tecnicas.md` §10): libera los camiones que abra cada prueba. Las salidas de prueba se arman con los *helpers* de `B/Wms.IntegrationTests/Exits/GoodsExitFlowTests.cs` (depósito confirmado, levante, salida, confirmación); no se duplican por prueba.
8. **Staging:** no se toca. **Credenciales y datos reales:** no se copian (`DEC-007`). Nada de `D/archivo/` es una instrucción.

---

## 1. Decisiones

Mandan sobre el resto del plan (`DEC-002`). Ninguna reabre una AF, `DEC-080`, `DEC-081`, una M del plan maestro ni una Dn de F01 a F05 o sus ajustes, salvo D5 y D6, que el usuario decidió en este plan sobre un choque y un hueco (se dice en cada una).

### 1.1 Respuestas del usuario (2026-11-26)

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **Rutas de Comercio Exterior.** Salidas (P-CE-11) es el listado `/foreign-trade/exits`, con el patrón y el detalle en drawer (`?id=`). «Nueva salida» es la página `/foreign-trade/exits/new` (acepta `?deposito={warehouseStorageId}` desde la etapa Salidas y `?volver=` con la ruta de origen) y «Editar» del Borrador es `/foreign-trade/exits/[id]/edit`: formularios de operación largos, en página propia. «Confirmar y emitir guía» abre un modal con la fecha de salida, las observaciones de la guía, el firmante y el cobro (D13). Las seis páginas viejas de CE (`F/pages/foreign-trade/loading-orders/index.vue`, `create.vue`, `[id]/index.vue`; `F/pages/foreign-trade/dispatch-guides/index.vue`, `create.vue`, `pending.vue`) se borran en I-06, sin redirección, como el tablero de CE en F05 | Usuario: «Página propia (Recomendada)»; AF-89, AF-97, AF-130; `P05/` D1 (sin redirección; `/foreign-trade/entries/[entryId]` como precedente) |
| D2 | **Rutas de Bodega.** Órdenes de salida (P-BOD-06) es el listado `/warehouse/exits` y el Historial (P-BOD-09) es `/warehouse/exits/history`, los dos con el patrón. «Ejecutar salida» (P-BOD-07) es un modal a dos columnas (`ExitLoadingDialog`, MK-10, como la recepción física P-BOD-02 de F04); «Registrar salida de patio» (P-BOD-08) es un modal chico (`YardExitDialog`, acción rápida). «Ver» abre el mismo drawer de la salida que usa CE (D14). `F/pages/warehouse/loading-orders/index.vue` y `[id].vue` se borran en I-06 | Usuario: «Listados y modales (Recomendada)»; AF-64 (`A/`:2068), AF-67; `D/levantamiento_staging/bodega_ajustes.md:23`; `P04/` D38 |
| D3 | **La guía se ve, se descarga, se anula y cambia de modo de pago desde su salida, y además en una pestaña «Guías».** (a) El drawer de la salida (D14) tiene la sección «Guía» y la de «Guías anuladas», y en su menú «Acciones»: Descargar guía, PDF por depósito (ZIP, solo consolidadas, AF-97), Cambiar modo de pago y Anular guía. (b) Las filas de P-CE-11 y de P-CE-08 llevan los mismos atajos. (c) Salidas de CE tiene dos pestañas, «Salidas» y «Guías» (`?vista=salidas\|guias`): la de guías lista las vigentes y las anuladas (C-F06-08), con «Ver salida», «Descargar guía» (también la anulada, con la marca «ANULADA» de hoy, C-F06-09), PDF por depósito, Cambiar modo de pago, Anular guía y «Exportar». Bodega solo descarga la guía vigente | Usuario: «Pestaña «Guías»» (además del drawer y las filas); AF-97; `DEC-019` D-2; hoy `F/pages/foreign-trade/dispatch-guides/index.vue` (Exportar Excel, PDF, ZIP, Anular, Cambiar modo de pago) y la marca de agua de la guía anulada en sus dos formatos (`B/Wms.Application/ForeignTrade/Common/Services/Pdf/LegacyDispatchGuidePdfRenderer.cs:42`, `B/Wms.Application/ForeignTrade/Common/Services/Pdf/V2/V2DispatchGuidePdfRenderer.cs:65`; D37) |
| D4 | **Precio del cobro de la guía: el del cliente de la salida.** El backend sugiere el cobro (C-F06-06): el convenio del cliente de la salida si sus depósitos son de un solo cliente (`IForeignTradeService.GetGuidePriceAsync`, `B/Wms.Application/ForeignTrade/Common/Services/IForeignTradeService.cs:15`), o el precio general de `GUIA_SALIDA` si son de varios clientes o de ninguno; el total lleva el IVA del servicio. La pantalla precarga ese cliente como «Tercero registrado» y pasa el total a `AppChargeForm` con `editableTotal`, como hoy. Cambiar de destinatario no recalcula el total, como en Báscula (`P03/` C-F03-03) | Usuario: «Precio del cliente (Recomendada)»; AF-106; hoy `F/features/billing/components/BillingCollectForm.vue:283-318` (total editable) |
| D5 | **La etapa Salidas se marca también en un depósito Cerrado.** En Cerrado se marca solo la etapa Salidas, si el depósito tiene una salida Confirmada a la que le falta algo; las demás etapas siguen sin marcarse en Cerrado y en Anulado no se marca ninguna. Precisa D22 de F05 («En Cerrado y Anulado no se marca ninguna») para esta etapa: confirmar la salida que se lleva todo el stock cierra el depósito (`P01/` D36) y esa salida aún espera el cargue, el pesaje o la salida de patio | Usuario: «Sí, solo Salidas (Recomendada)»; AF-73 (`A/`:1162); `P05/` D22; `B/Wms.Application/ForeignTrade/Common/Services/DepositStageRules.cs:102-119` |
| D6 | **El Historial de Bodega trae todo lo atendido por Bodega.** Entran las salidas con un registro de Bodega (cargue o salida de patio) que no estén canceladas, aunque aún les falte el pesaje; el estado se ve en su columna («Confirmada · falta pesaje», «Completada»). Orden por la fecha del registro, la más reciente primero. Reemplaza la nota de C-F01-94 («su historial = `status=Completed`», `P01/`:971) | Usuario: «Todo lo atendido (Recomendada)»; AF-64 |
| D7 | **Los endpoints nuevos y cambiados van en el recurso `exits`** (`P01/` D3): `GET exits` y `GET exits/{id}` suman campos y filtros (C-F06-01, C-F06-02); `POST` y `PUT exits` cambian la orden del cliente (C-F06-03, C-F06-04); `POST exits/{id}/confirm` pierde «Clientes» (C-F06-05); nuevos `GET exits/{id}/guide/charge` (C-F06-06), `GET exits/eligible-deposits` (C-F06-07), `GET exits/guides` (C-F06-08) y `GET exits/guides/{guideId}/pdf` (C-F06-09). Un controlador, `B/Wms.Api/Controllers/v1/ExitsController.cs` | Usuario: «Todo en exits (Recomendada)» |
| D8 | **Fases** (§8). Backend: BE-1 lecturas (listado y detalle ampliados, depósitos elegibles, guías y su PDF, regla de la etapa Salidas); BE-2 escrituras y cobro (orden del cliente con su soporte y la migración, confirmar sin «Clientes», cobro sugerido). Maquetación: FE-1 contratos, fuentes, drawer de la salida y Salidas de CE con sus dos pestañas (P-CE-11); FE-2 «Nueva salida» y «Editar» con la confirmación y el cobro, y la etapa Salidas (P-CE-08); FE-3 Bodega (P-BOD-06 a P-BOD-09). Después, la revisión del usuario (§8.6) e I-06 en dos fases (§13) | Usuario: «2 backend y 3 maqueta (Recomendada)» |
| D9 | **La orden del cliente no tiene número; el soporte es opcional.** Sale el número de la orden del cliente: del contrato (`customerOrder.number`), de la entidad (`GoodsExit.CustomerOrderNumber`, `B/Wms.Domain/Entities/Warehouse/GoodsExit.cs:34`, `:131`), de su configuración (`B/Wms.Infrastructure/Persistence/Configurations/Warehouse/GoodsExitConfiguration.cs:21`) y de la tabla (migración `RemoveExitCustomerOrderNumber`, §4), con su 400 «El número de la orden del cliente es obligatorio…» (`B/Wms.Application/Exits/Commands/UpsertExitCommand.cs:294-300`). No hay regla de número repetido. Quedan el emisor (agencia de aduanas o importador) y la fecha, los dos opcionales, y el **soporte escaneado, opcional**, que se sube con la salida como hoy con la orden externa (PDF, JPG o PNG, hasta 10 MB, base64; hoy `develop` `B/Wms.Application/ForeignTrade/Commands/CreateLoadingOrder/CreateLoadingOrderCommandHandler.cs:27-28`, `:442-480`) y se reemplaza o se quita mientras la salida esté en Borrador. Corrige el retroceso de F01, que solo recibe un `fileUrl` sin subida (`UpsertExitCommand.cs:251`) | Usuario: «La orden del cliente que entrega a CE no tienen numero, son correos u documentos que no tienen numero, esto se puede quitar. En cuanto al soporte escaneado que se sube se puede agregar al crear la salida pero opcional.»; AF-89 (P-CE-11: «Como la orden externa de hoy»); `DEC-005` |

### 1.2 Salidas de Comercio Exterior (P-CE-11, «Nueva salida», confirmación y guías)

| # | Decisión | Fuente |
| --- | --- | --- |
| D10 | **Pestaña «Salidas» de P-CE-11** (`/foreign-trade/exits`, `AppDataTable`). Columnas: Salida (número), Fecha (`createdAt`), Tipo, Estado (la cancelada, «Cancelada» con la fecha y el motivo en el tooltip, y la fila en rojo tenue; sin `AppAlertIcon`, D35), Depósitos, Placas (`VehiclePlateTag`), Guía, Falta y Acciones. «Falta»: una etiqueta por pendiente («Cargue», «Pesaje», «Salida de patio») y, en Confirmada, el reloj de Bodega (`WarehouseClockTag`, `P04/` D37); en el Borrador de Báscula (`origin = Weighbridge`), «Completar (creada en báscula)»; en Completada y Cancelada, «—». Filtros en la columna (C-F06-01): número, rango de fecha, tipo y estado (varios), depósito, placa y guía; orden en el servidor por número, fecha, tipo y estado, por defecto la fecha más reciente. Barra: «+ Nueva salida» (primario) y «Exportar» (todo, `all=true`). Acciones con `AppRowActions` (pasan de tres, así que todas van al menú ⋮): Ver; Editar (Borrador); Descargar guía (con guía vigente); PDF por depósito (ZIP) (consolidada con guía vigente); Cambiar modo de pago (con guía vigente); Anular guía (Confirmada con guía) o Reabrir salida (Confirmada de inspección, sin guía); Cancelar salida (Borrador; `danger`, con `separator`) | P-CE-11; AF-97, AF-99, AF-129; `D/contexto/convenciones-tecnicas.md` §3 (tablas de listado, aviso junto a un dato, fila anulada) |
| D11 | **Pestaña «Guías» de P-CE-11** (D3; `AppDataTable` propio en la misma página, pestañas `Tabs` en la barra como la cola de Báscula, `AUI5/` D5). Columnas: Fecha (`issuedAt`), N.º de guía, Salida (enlace que abre el drawer de su salida), Tipo de salida, Cliente(s), Depósitos, Placas, Conductor, Mercancía («{producto} · {embalaje} · {cantidad}» o «{n} productos» con el detalle en el tooltip), Modo de pago, Estado («Vigente» o «Anulada», esta con la fecha y el motivo en el tooltip y la fila en rojo tenue; sin `AppAlertIcon`, D35) y Acciones. Filtros en la columna (C-F06-08): rango de fecha, número, salida, cliente, depósito, placa, producto, modo de pago y estado («Vigente», «Anulada»); orden por fecha (por defecto, la más reciente) y número. Acciones: Ver salida, Descargar guía (C-F06-09, vigente o anulada), PDF por depósito (ZIP) (vigente de una consolidada), Cambiar modo de pago (vigente) y Anular guía (vigente y salida no completada). «Exportar» (todo) con las columnas de hoy (fecha, guía, cliente, placa, conductor, producto, cantidad, unidades de carga, modo de pago) más la salida y el estado | D3; `DEC-005`; hoy `F/pages/foreign-trade/dispatch-guides/index.vue` |
| D12 | **«Nueva salida» y «Editar»** (`ExitForm` en las dos páginas de D1). Página que no es listado: sin tarjeta de título, `<h1 class="sr-only">`, y en una barra arriba a la derecha «Volver», «Guardar borrador» y «Confirmar y emitir guía» («Confirmar salida» en inspección). Secciones con la tarjeta de registro de Báscula (`registration-card`, `AUI5/` D26): **1 Tipo** (radio «Por tiquete de entrada», «Global», «Por número de depósito»; con dos o más depósitos muestra la etiqueta «Consolidada», AF-32). **2 Depósitos**: `AppSearchSelect` con C-F06-07 (línea secundaria: modalidad · cliente · disponible); después del primero solo ofrece su modalidad (`P01/` D33); uno solo en tiquete y global; cada depósito elegido con «Quitar» y, junto al número, `AppAlertIcon` `warn` «Asigne el cliente del depósito antes de confirmar.» si no tiene cliente (C-F05-21) o `danger` «El cliente tiene las salidas bloqueadas.» (BR-05-004). **3 Tiquetes** (tiquete y global): casillas con los tiquetes del depósito (C-F01-103): tiquete · placa · fecha · mercancía declarada; el que está en otra salida activa va deshabilitado con `AppAlertIcon` «En la salida {N}.»; al marcar, las líneas se precargan con lo declarado (ajustable) y el vehículo con el de la placa del primer tiquete (C-F01-21). **4 Mercancía**: por producto disponible de los depósitos (C-F01-102, con `exceptExitId` al editar): depósito, producto · embalaje, unidad de carga (si el depósito la usa), nacionalizado disponible (solo importación), disponible, saldo anterior (`currentStock`), cantidad que sale (`InputNumber` `es-CO`, máximo el menor entre disponible y nacionalizado disponible) y nuevo saldo, con el total. **5 Transporte**: vehículo (`AppSearchSelect`, C-F01-21, con «+» que abre `VehicleQuickDialog`, C-F01-23), conductor (C-F01-15 con «+» y `DriverQuickDialog`, C-F01-17) y empresa de transporte (opcional; terceros transportadores, C-F01-25, con «+» y `StakeholderQuickDialog`, C-F01-141). **6 Destino**: ciudad (obligatoria; C-F01-47) con «Vence el {fecha}» (días de tránsito de la ciudad; sin ellos, 30 días, nota de la fase 5 de F01) y dirección (opcional, 250). **7 Orden del cliente** (opcional, D9): emisor (agencia o importador, C-F01-25), fecha (no futura) y soporte (PDF, JPG o PNG hasta 10 MB; «Adjuntar», nombre, «Quitar»; al editar, «Ver soporte» del actual). **8 Observaciones** (500). El Borrador de Báscula abre con placa, conductor y transportadora, y le faltan tipo, depósitos y líneas (AF-37). Con `?deposito=` abre con ese depósito y el tipo «Por número de depósito» | P-CE-11; AF-28 a AF-37, AF-54, AF-89; `P01/` C-F01-96, C-F01-102, C-F01-103; D9 |
| D13 | **Confirmar** (`ExitConfirmDialog`). «Confirmar y emitir guía» guarda primero el formulario (C-F06-03 o C-F06-04) y abre el modal. Encabezado en dos líneas: «Confirmar la salida {N}» y, debajo, «Emite la guía y descuenta el stock». Contenido: resumen (tipo, depósitos, placas y total por producto), fecha y hora de salida (por defecto ahora; no antes de ayer), observaciones de la guía (500, se imprimen), firmante en solo lectura («Conductor {nombre}», o «Importador {nombre}» en la global con un importador; nota de la fase 5 de F01), el vencimiento y el cobro: `AppChargeForm` con el total de C-F06-06 (`editableTotal`), `defaultCustomerId`, el conductor de la salida, «Pago inmediato» y «Pendiente por facturar», y `submitLabel` «Confirmar y emitir guía». En inspección no hay guía ni cobro: el modal pide la fecha de salida y las observaciones, y envía `billing: null`. Al confirmar: aviso «Salida {N} confirmada · guía {G}» y vuelve a `?volver=` o abre el drawer en `/foreign-trade/exits?id={id}`. Los errores (cliente sin asignar, salidas bloqueadas, stock que cambió, mora) se muestran en el modal | AF-36, AF-68, AF-88, AF-106, AF-132; `P01/` D36, D47; C-F05-21 |
| D14 | **Drawer de la salida** (`ExitDetailDrawer` con el contenido `ExitDetail`; lo usan P-CE-11, P-CE-08, P-BOD-06 y P-BOD-09; `?id=`). Encabezado: `pi pi-sign-out`, «Salida {N}», el estado como etiqueta y el subtítulo «{tipo} · {placas} · {depósitos}». Secciones (`AppDetailSection`): **Datos** (origen, modalidad, creada, confirmada por y cuándo, vehículo con su tipo, conductor, empresa de transporte, destino y dirección, observaciones; orden del cliente con emisor, fecha y «Ver soporte»); **Mercancía** (`flush`: depósito, producto · embalaje, unidad de carga, cantidad, cargada, peso asignado, saldo anterior y nuevo saldo, con el total); **Tiquetes** (tiquete y global); **Guía** (número, emisión, fecha de salida, vencimiento, firmante, modo de pago y factura; vacía con «Sin guía en Borrador» o «La inspección no lleva guía»); **Guías anuladas** (`count`; número, fecha y motivo); **Bodega** (`WarehouseClockTag`; cargue: fecha, usuario, cuadrilla, observación y fotos; o salida de patio: fecha, usuario y observación; vacía «Pendiente»); **Báscula** (tiquete, estado y neto del pesaje de salida, y peso despachado; en tiquete y global, «No pasa por báscula», AF-33); **Cancelación** (si se canceló). Acciones en el menú ⋮ del encabezado, según el rol (`usePermissions`) y el estado: CE, las de D10; Bodega, «Ejecutar salida» o «Registrar salida de patio» (si le falta) y «Descargar guía» | `D/contexto/convenciones-tecnicas.md` §3 (drawer de detalle); AF-42, AF-97, AF-130 |
| D15 | **Anular guía, reabrir y cancelar** con `ReasonDialog` (motivo de 10 a 500): «Anular guía» y «Reabrir salida» llaman C-F01-99; «Cancelar salida», C-F01-100. Textos: «Anular la guía {G}: la salida {N} vuelve a Borrador, el stock regresa al depósito y la guía queda anulada. El cargue y el pesaje registrados se conservan.»; en inspección, «Reabrir la salida {N}: vuelve a Borrador y el stock regresa al depósito.»; «Cancelar la salida {N}: libera lo reservado. No se puede deshacer.» | AF-90; `P01/` D34 |
| D16 | **Cambiar modo de pago** con `ChangePaymentModeDialog` (`F/features/billing/components/ChangePaymentModeDialog.vue`, que no llama al API y emite el modo y, al pasar a «Pago inmediato», el método) y C-F01-108 | `DEC-019` D-2; `P01/` C-F01-108 |

### 1.3 Bodega (P-BOD-06 a P-BOD-09)

| # | Decisión | Fuente |
| --- | --- | --- |
| D17 | **Órdenes de salida** (P-BOD-06, `/warehouse/exits`): C-F06-01 con `status=Confirmed&missing=Loading,YardExit`, ordenado por `confirmedAt asc` (el reloj más viejo arriba, C-F04-03). Columnas: Salida, Tipo, Placas, Tiquetes (tiquete y global), Depósitos y mercancía («2026BA00010 · Cebolla · Sacos · 300» o «{depósitos} · {n} productos»), Guía («Sin guía · inspección» en inspección), Falta, Tiempo desde la guía (`WarehouseClockTag`) y Acciones. Filtros en la columna: número, tipo, placa, tiquete, depósito o producto, guía, falta y color del reloj (`warehouseLevel`). Acciones (`AppRowActions`; la tabla tiene tres posibles, así que son botones de solo icono con tooltip y la acción del operario queda a un clic): «Ejecutar salida» (depósito y consolidada), «Registrar salida de patio» (tiquete y global) y «Ver»; «Descargar guía» va en el menú del drawer (D14). El reloj se refresca cada minuto (`F/features/warehouse/utils/warehouse-clock.ts`) | P-BOD-06; AF-35, AF-57, AF-64, AF-66, AF-68 |
| D18 | **Ejecutar salida** (P-BOD-07, `ExitLoadingDialog`, MK-10 a dos columnas). Encabezado en dos líneas: «Ejecutar salida» con la etiqueta «Listo para despacho» y «Salida {N} · Complete los datos de la salida». Columna izquierda: el aviso de la guía vigente («Guía de salida {G} vigente. Verifíquela con el conductor antes de iniciar.» con «Verificada»; sin guía vigente, el aviso `danger` y «Ejecutar salida» deshabilitado, `DEC-056`); el aviso de disponibilidad («Todo el stock está disponible para cargar · 100 % ubicado» o «{p} % ubicado: lo que falta no tiene ubicación», con `placedQuantity` de C-F06-02; informa, no bloquea, AF-70); cliente, vehículo (placa y tipo) y conductor en solo lectura; ítems a cargar: por línea, producto · embalaje · depósito, «En la guía: {q} · {u} disp.» (`u` = ubicado), cantidad cargada (`InputNumber`, de 0 a la cantidad de la línea) y «Cargar todo». Columna derecha: cuadrilla que cargó (opcional; C-F01-52), observaciones (opcional, 250), firma del conductor (`SignaturePad`, obligatoria) y fotos (`PhotoUploader`, opcional, 0 / 5). Pie: «Cancelar», «Total a despachar: {n}» y «Ejecutar salida». Llama C-F01-104. Si `differsFromGuide`, aviso «Lo cargado difiere de la guía: se avisó a Comercio Exterior.» (`DEC-052`). Sin «Retirar de», «Stock anterior», «Stock nuevo», «Reserva liberada» ni «Número de sello» (AF-36, AF-70) | P-BOD-07; MK-10 (`MK/orden_de_salida_bodega/`); AF-64, AF-70; `P01/` D38; `DEC-052`, `DEC-056` |
| D19 | **Salida de patio** (P-BOD-08, `YardExitDialog`): «Registrar salida de patio · Salida {N}»; muestra la guía vigente, las placas, los tiquetes, el tipo y el firmante («Firma el importador» o «Firma el conductor»); fecha y hora automáticas (las pone el servidor; la pantalla muestra la hora actual como referencia); observación opcional (250); «Cancelar» y «Registrar salida de patio». Sin firma ni fotos. Llama C-F01-105 y la salida queda Completada | P-BOD-08; AF-66, AF-67 |
| D20 | **Historial** (P-BOD-09, `/warehouse/exits/history`): C-F06-01 con `attendedByWarehouse=true`, ordenado por `warehouseRecordAt desc` (D6). Columnas: Fecha y hora (del registro de Bodega), Salida, Tipo, Placas, Depósitos y mercancía, Guía, Registro de Bodega («Cargado {n}» o «Salida de patio»), Cuadrilla, Estado («Completada» o «Confirmada · falta pesaje») y «Ver». Filtros en la columna: rango de la fecha del registro, número, tipo, placa, depósito o producto, guía, cuadrilla y estado. «Exportar» en la barra | P-BOD-09; AF-64; D6 |

### 1.4 Etapa Salidas del detalle del depósito (P-CE-08)

| # | Decisión | Fuente |
| --- | --- | --- |
| D21 | **Contenido de la etapa** (`F/features/foreign-trade/components/DepositExitsStage.vue`, que F05 dejó vacía, `P05/` D38 y `AUI5/` D25). Dentro de su `DepositStageCard`, un `DepositTableBlock` «Salidas del depósito» con su número, y la tabla de las salidas del depósito (C-F06-01 con `warehouseStorageId` y `all=true`, la más reciente primero) con fila expandible. Fila: fecha, salida, guía, tipo, estado y lo que falta, ciudad de destino, peso despachado y observaciones, y acciones (`AppRowActions`): Ver, Editar (Borrador), Descargar guía, PDF por depósito (consolidada), Anular guía o Reabrir salida. En la consolidada, el peso despachado es la parte de este depósito (suma de `allocatedWeight` de sus líneas, `P01/` D4), con el total del pesaje en el tooltip. Detalle expandido (C-F06-02, al abrirse): por cada línea de este depósito, producto · embalaje, cantidad de entrada, saldo anterior, cantidad que sale y nuevo saldo, con el total de la salida y «Descargar guía». «Nueva salida» va en el encabezado de la tarjeta (`#actions`) y abre `/foreign-trade/exits/new?deposito={id}&volver={ruta del detalle con ?etapa=salidas}`; deshabilitado con tooltip si el depósito no está Confirmado («Confirme el depósito antes de crear una salida.») o, en importación, si no tiene levante («El depósito no tiene mercancía nacionalizada.») | P-CE-08; AF-42, AF-90, AF-96; `P05/` D38, `AUI5/` D15, D16, D25 |
| D22 | **Indicador de la etapa** (D5; `P05/` D22): `DepositStageRules` (`B/Wms.Application/ForeignTrade/Common/Services/DepositStageRules.cs:102-119`) marca `Exits` cuando el depósito tiene una salida Confirmada con algo en `missing`; también en Cerrado (solo esa etapa); nunca en Anulado. El color es el del indicador de etapa, sin nivel de reloj (el nivel sigue siendo solo el de la etapa Bodega). Lo calculan el listado (C-F05-01) y el detalle (C-F05-05 a C-F05-07) por regla (C-F06-10); la pantalla de F05 no cambia: pinta lo que llega | AF-73; `P05/` D22 |

### 1.5 Pantallas, componentes y transversales

| # | Decisión | Fuente |
| --- | --- | --- |
| D23 | **Patrones** (`D/contexto/convenciones-tecnicas.md` §3): Salidas de CE (con sus dos pestañas), Órdenes de salida y el Historial de Bodega son listados (`PATTERN`): `AppDataTable` en la página, sin tarjeta de título, filtros en la columna, orden en el servidor, `AppRowActions` y detalle en `AppDetailDrawer` con las acciones en el menú del encabezado y sin pie. «Nueva salida» y «Editar» son formularios de operación (fuera del menú: la guardia del patrón no los lista), sin tarjeta de título, con `<h1 class="sr-only">` y la barra de acciones arriba a la derecha. Lo cancelado o anulado va como etiqueta en la columna «Estado», con la fecha y el motivo en el tooltip, y la fila en rojo tenue (`AUI5/` D36; D35); `AppAlertIcon` solo junto a un dato (sin cliente, salidas bloqueadas, tiquete en otra salida). Botones de solo icono con `v-tooltip.top` y `aria-label` | AF-99, AF-129, AF-130 |
| D24 | **Compartidos sin cambios**, salvo `AppChargeForm` (D33): `AppDataTable`, `AppRowActions`, `AppDetailDrawer`, `AppDetailSection`, `AppSearchSelect`, `AppCrudDialog`, `AppAlertIcon`, `ReasonDialog`; de otros dominios, `VehiclePlateTag`, `WarehouseClockTag`, `SignaturePad`, `PhotoUploader`, `DriverQuickDialog`, `StakeholderQuickDialog`, `ChangePaymentModeDialog`, `DepositStageCard` y `DepositTableBlock`. Si una pantalla necesita cambiar otro compartido, el ejecutor se detiene y pregunta | `PM/` R4; `P04/` D39 |
| D25 | **Componentes nuevos de salidas** (`F/features/exits/components/`): `ExitListTable` (pestaña «Salidas»), `GuideListTable` (pestaña «Guías»), `ExitDetailDrawer` y `ExitDetail` (D14), `ExitForm` y sus secciones `ExitDepositsSection`, `ExitTicketsSection`, `ExitLinesSection`, `ExitTransportSection` y `ExitCustomerOrderSection` (D12), `ExitConfirmDialog` (D13), `ExitLoadingDialog` (D18), `YardExitDialog` (D19), `ExitMissingTags` (etiquetas de «Falta» con el reloj) y `ExitGoodsCell` (depósitos y mercancía). En `F/features/entries/components/`, `VehicleQuickDialog` (placa, tipo de vehículo y empresa de transporte; no llama al API: recibe las funciones, como `DriverQuickDialog`) | `PM/` §5.5; como `P04/` D40 y `P05/` D35 |
| D26 | **Fuentes intercambiables** (M12, `PM/` §5.2): contratos en `F/features/exits/contracts/exit.ts` (ampliado), `guide.ts` y `exit-charge.ts`; fuentes `F/features/exits/services/exit.source.ts` (C-F06-01 a C-F06-07, C-F01-99 a C-F01-108) y `guide.source.ts` (C-F06-08, C-F06-09), con sus simulados en `F/features/exits/mocks/`. Lo integrado de F01, F03 y F04 que usan las pantallas (vehículos con su alta, conductores con su alta, terceros con su alta rápida, ciudades, cuadrillas y tipos de vehículo) se simula con la fachada `F/features/exits/services/catalog.source.ts`, como `P04/` D41 y `P05/` D36; I-06 la borra. La etapa Salidas usa `exit.source.ts`; el resto del detalle del depósito ya está integrado | M12; `P04/` D41 |
| D27 | **Esquemas de F01 corregidos a lo integrado** (gana el código, `PM/` R3): `guidePaymentModeSchema` suma `paymentMethod` (nulo o un método de pago), porque C-F01-108 lo recibe y pide «Seleccione el método del pago de contado.» al pasar a «Pago inmediato» (`B/Wms.Api/Controllers/v1/ExitsController.cs:181-191`); `exitLoadingResultSchema` (nuevo) agrega a `exitSchema` lo que C-F01-104 ya devuelve (`releasedPlacements`, `differsFromGuide`) | `P01/` C-F01-104, C-F01-108 |
| D28 | **Menú** (I-06; `F/components/layout/menu-model.ts:60-124`): Bodega queda Dashboard · Entradas ▸ Recepción, Historial · Salidas ▸ Órdenes de salida (`/warehouse/exits`), Historial (`/warehouse/exits/history`) · Montacargas · Inventario · Novedades (AF-64: «Salidas» después de «Entradas»; sale «Órdenes de cargue», `P04/` D45). Comercio Exterior queda Dashboard · Depósitos ▸ Importación, Exportación, Inspección · Tickets de ingreso · Levantes · Salidas (`/foreign-trade/exits`) · Abandono y prórrogas · Listas de empaque (P-TR-01; salen «Órdenes de cargue» y «Guías de salida», AF-97, `P05/` D43) | AF-64, AF-97, AF-127; P-TR-01 |
| D29 | **Atajos y tableros** (I-06): Alt+O pasa a «Salidas», `/foreign-trade/exits` (`F/composables/useGlobalShortcuts.ts:25`). El tablero de CE (`F/pages/foreign-trade/index.vue:30-45`, `:100-112`) cambia «Órdenes de Cargue Pendientes» por «Salidas en Borrador» (C-F06-01 con `status=Draft`, `/foreign-trade/exits?estado=borrador`) y «Guías Pendientes» por «Salidas por completar» (`status=Confirmed`, `/foreign-trade/exits?estado=confirmada`), y sus accesos «Nueva orden» y «Nueva guía» por «Nueva salida»; `useForeignTradeDashboard` deja de leer órdenes y guías. El tablero de Bodega (`F/pages/warehouse/index.vue:37-43`) cambia la tarjeta «Órdenes de cargue» por «Salidas» (`/warehouse/exits`) | `DEC-005`; como `P04/` D44 y `P05/` D43 |
| D30 | **Guardias** (I-06): `FT/unit/guards/list-pattern-routes.ts` saca de `PENDING` las cuatro rutas de F06 (`:52-56`) y F06 de `PENDING_FEATURES` (`:113`); entran a `PATTERN` `/foreign-trade/exits`, `/warehouse/exits` y `/warehouse/exits/history`; salen de `OUTSIDE` (`:78-79`) y de `TITLE_RULE_EXEMPT` (`:108-109`) las dos páginas de creación viejas. En la maquetación, las páginas nuevas y la de detalle de CE (por la etapa Salidas) van en `MAQUETACION_PAGES` (`FT/unit/guards/mock-sources.spec.ts:22`); I-06 la deja vacía y suma `exit.source.ts` y `guide.source.ts` a `INTEGRATED_SOURCES` | `P02/` D14, D15 |
| D31 | **Lo que se borra en I-06** (§13.3), después de comprobar con grep quién importa cada archivo (trampas 4 y 7). **Páginas:** las seis de CE (D1) y las dos de Bodega (D2). **Componentes:** `DispatchGuideForm`, `LoadingOrderForm`, `EditLoadingOrderItemsDialog`, `ExitWithEntryTicketDialog` (`F/features/foreign-trade/components/`), `LoadingOrderExecutionDialog` y `LoadingOrderList` (`F/features/warehouse/components/`) y `BillingCollectForm` (`F/features/billing/components/BillingCollectForm.vue`; F06 es su último uso, `P03/` D42, `P04/` D46), con lo que solo ellos usan (`billing-collect.ts`, `useBillingPreview` y sus utilidades, si nadie más los importa). **Composables, servicios, tipos y utilidades de la orden de cargue y la guía por orden:** los de `F/features/foreign-trade/composables/` (`useCancelDispatchGuide`, `useCancelLoadingOrder`, `useChangeDispatchGuidePaymentMode`, `useCreateDispatchGuide`, `useCreateLoadingOrder`, `useDispatchGuidePreview`, `useDispatchGuides`, `useDownloadLoadingOrderPdf`, `useExitWithEntryTicketFt`, `useLoadingOrderDeposits`, `useLoadingOrderDetail`, `useLoadingOrders`, `usePendingImportLoadingOrders`, `useRevertLoadingOrder`, `useUpdateLoadingOrderItems`), de `F/features/warehouse/composables/` (`useLoadingOrderById`, `useLoadingOrderMutations`, `useLoadingOrderStatistics`, `useLoadingOrders`, `usePendingLoadingOrders`), `F/features/weighbridge/composables/useAddAdditionalOrders.ts` y `addAdditionalOrders` de `weighbridge-service.ts` (`P03/` D41: el único que lo importaba era `useExitWithEntryTicketFt`), los tipos `loading-order*.ts` y `dispatch-guide.ts` y los de `F/features/weighbridge/types/weighbridge-cycle.ts` que nadie importe, las utilidades `loading-order-cargo-handling.ts`, `loading-order-guide-lock.ts`, `dispatch-guide-products.ts`, `guide-load-mismatch.ts` y `F/utils/loading-order-status.ts`, los métodos de `foreign-trade-service.ts` y `warehouse-service.ts` que nadie llama, `canCreateLoadingOrders` y `canCreateDispatchGuides` de `F/composables/useAuthForeignTrade.ts` si nadie los usa, y las etiquetas `LoadingOrder` y `LoadingOrderReversal` de `F/features/warehouse/utils/inventory-labels.ts`. Las secciones de los README de `F/features/warehouse/` que describen la orden de cargue se actualizan. **Pruebas** de lo borrado. **Se queda:** `ChangePaymentModeDialog` (D16) y lo que use otra pantalla | `PM/` §5.4; `P03/` D41, D42; `P04/` D46; `P05/` D46 |
| D32 | **Auditoría:** `F/features/audit/utils/entity-labels.ts` suma `GoodsExit: "Salida de mercancía"` y quita `LoadingOrder` (la entidad ya no existe, `P01/` D2, y la base se recrea, M17) | `P01/` D2 |
| D33 | **«Clientes» sale del cobro** (AF-106; `P01/` D47, `P02/` D13): sin ningún uso después de F06, `AppChargeForm` pierde `allowMultiClient` y el modo `multiClient` (`F/components/app/AppChargeForm.vue:29`, `:44`, `:59`, `:129`), y `billingRecipientInputSchema` pierde `"multiClient"` (`F/features/billing/contracts/billing-recipient.ts:10`). En el backend, `ExitGuideIssuer` factura a un solo destinatario aunque haya varios clientes (C-F06-05) y se borran `DispatchGuideBillingPlan` (con `GuideBillingPlanResult`), `DispatchGuideOrderData.PricesAsync`, `BillingRecipientModes.MultiClient` y sus pruebas (`Wms.Tests/ForeignTrade/DispatchGuideBillingPlanTests.cs`, `Wms.IntegrationTests/ForeignTrade/MultiClientGuideTests.cs`), después de comprobar con grep que nada más los usa | AF-106; `B/Wms.Application/Exits/Common/ExitGuideIssuer.cs:30-65`, `:173-177` |
| D34 | **Avisos:** F06 no crea avisos nuevos. Los de las salidas ya existen y van por el orquestador con roles fijos: «Lo cargado difiere de la guía» y «Cambio de conductor o placa en salida con guía» (`P01/` D45) y «Atraso de Bodega» del cargue y de la salida de patio (`P04/` D36). F09 los pasa a tipos (M23) | `PM/` §2.2; `P01/` D45; `P04/` D36 |

### 1.6 Destino de las 4 AF dueñas

| AF | Qué pide | Decisión | Fase |
| --- | --- | --- | --- |
| AF-67 | Salida de patio: un clic con verificación (guía vigente, placas y tiquetes), fecha y hora automáticas, observación opcional, sin firma ni fotos | D2, D19 (C-F01-105, sin cambios) | FE-3; I-06 |
| AF-89 | «Crear salida» con el wireframe propuesto (P-CE-11), validado por el usuario | D1, D9, D12, D13; C-F06-03, C-F06-04, C-F06-05, C-F06-06, C-F06-07 | BE-1, BE-2; FE-2; I-06 |
| AF-97 | Un ítem «Salidas» en CE con el listado y «Nueva salida»; la guía se ve, descarga o anula desde su salida; salen «Órdenes de cargue» y «Guías de salida»; el ZIP por depósito solo en consolidadas | D1, D3, D10, D11, D14, D28, D31; C-F06-01, C-F06-08, C-F06-09 | BE-1; FE-1; I-06 |
| AF-106 | El cobro de la guía sin «Clientes»: cuatro destinatarios y un solo destinatario paga | D4, D13, D33; C-F06-05, C-F06-06 | BE-2; FE-2; I-06 |

Las 4 tienen decisión y fase.

### 1.7 AF de otras features que F06 muestra o aplica

La regla vive en otra feature (`PM/` §2, «Regla de pertenencia»); F06 construye la pantalla que la muestra y no la vuelve a contar.

| AF | Dueña | Qué muestra F06 | Pantalla |
| --- | --- | --- | --- |
| AF-28, AF-32 | F01 | Los cuatro tipos; con varios depósitos, «Consolidada» la fija el sistema | P-CE-11 (formulario, listado), P-BOD-06, P-BOD-09, drawer |
| AF-29 | F01 | Tiquete y global: guía directa, sin orden previa | P-CE-11 (formulario) |
| AF-30 | F01 | La salida con su tipo y estado; el Borrador de Báscula se completa en CE | P-CE-11 (listado y formulario) |
| AF-31, AF-35 | F01 | «Falta»: cargue, pesaje o salida de patio, sin orden entre ellos | P-CE-11, P-CE-08, P-BOD-06, P-BOD-09, drawer |
| AF-33 | F01 | Tiquete y global no pasan por báscula; un cobro por guía | Drawer (Báscula), confirmación |
| AF-34 | F01 | El conductor y la placa que trae Báscula a la salida | Formulario (Borrador de Báscula), drawer |
| AF-36 | F01 | Confirmar emite la guía y descuenta el stock; saldos anterior y nuevo | Confirmación, P-CE-08, drawer |
| AF-37 | F01 | El Borrador de Báscula llega con placa, conductor y transportadora | P-CE-11 («Completar (creada en báscula)»), formulario |
| AF-42 | F01 | Peso despachado de la salida y la parte de cada depósito | P-CE-08, drawer |
| AF-68 | F01 | Toda Confirmada tiene guía; Órdenes de salida no tiene «Esperando guía» | P-BOD-06, P-BOD-07 |
| AF-88 | F01 | Inspección sin guía; exportación con guía | Confirmación, P-BOD-06 («Sin guía · inspección»), drawer |
| AF-90 | F01 | Borrador se edita; Confirmada se corrige anulando la guía; Completada no se edita | P-CE-11, P-CE-08, drawer (D15) |
| AF-66, AF-70 | F01 | Salida de patio que completa; cargue sin sello que libera ubicaciones | P-BOD-07, P-BOD-08 |
| AF-56, AF-57 | F04 | Reloj desde la guía y su color | P-BOD-06, P-CE-11, drawer |
| AF-64 | F04 | «Órdenes de salida», «Salidas» con su historial en tabla | P-BOD-06, P-BOD-09, menú |
| AF-73 | F05 | Indicador de la etapa Salidas (D22) | P-CE-01, P-CE-02 (stepper) |
| AF-75 | F05 | La confirmación exige cliente en cada depósito (C-F05-21) | Formulario (aviso), confirmación |
| AF-54 | F02 | «+» de alta rápida en vehículo, conductor, transportadora y tercero del cobro | P-CE-11 (formulario), confirmación |
| AF-99, AF-129, AF-130 | F02 | Filtros por columna y orden; sin botones de texto; listado con el patrón; formulario largo en página; modal a dos columnas | Todas |
| AF-132 | F02 | Cobro con «Efectivo» precargado y «Referencia» solo con otro método, sin «Nota» | Confirmación (`AppChargeForm`) |

### 1.8 Permisos (`B/Wms.Domain/Security/WmsPolicyRoles.cs`; `PM/` §5.6, `DEC-005`)

Sin políticas nuevas y sin quitar roles. C-F06-01, C-F06-02 y la lectura por placa siguen con `ExitAccess` (Admin, ForeignTrade, Warehouse, Scale; `WmsPolicyRoles.cs:162`); C-F06-03 a C-F06-09, con `ForeignTradeAccess` (Admin, ForeignTrade), como las escrituras de CE de hoy y el historial de guías de hoy. Bodega sigue con `WarehouseAccess` en el cargue y la salida de patio (C-F01-104, C-F01-105) y con `ExitAccess` en la guía vigente (C-F01-106). Las páginas: Salidas de CE, «Nueva salida» y «Editar», Admin y ForeignTrade; Órdenes de salida y su historial, Admin y Warehouse. Nadie pierde una función: CE conserva crear, editar, confirmar, anular, cancelar, cambiar el modo de pago y descargar (hoy en órdenes y guías), y Bodega conserva ejecutar e imprimir.

### 1.9 Revisión antes de ejecutar (2026-11-27)

Después de la aprobación llegaron a `fase-2`: en el backend, los ajustes de la QA manual de F05 (`dcb7b8f`), el formato numérico es-CO (`6ccff7b`, `DEC-082`) y los formatos v2 de PDF (`996828e`, con la migración `AddPdfFormatParameters`); en el frontend, el aviso junto a un dato en F01 a F04 (`00d15e5`), los ajustes de la QA de F05 (`4ed9400`, `633b470`) y el formato numérico (`8884936`). Comprobado con `git diff 348ab15 fase-2` y `git diff 3531432 fase-2`: **el código de las salidas no cambió** (`B/Wms.Application/Exits/`, `ExitsController.cs`, `GoodsExit.cs`, `DepositStageRules.cs`, `WmsPolicyRoles.cs`, `ExitGuideIssuer.cs`, `UpsertExitCommand.cs`; en el frontend, `F/features/exits/`, los compartidos, el menú, los atajos, los tableros y la etapa Salidas), y las 80 rutas y líneas citadas siguen en rango. Se corrigieron dos citas que se movieron (la marca «ANULADA», D37; `INTEGRATED_SOURCES`, ahora `FT/unit/guards/mock-sources.spec.ts:31`). Lo demás se aplica así, por `DEC-002`, sin reabrir ninguna Dn:

| # | Decisión | Fuente |
| --- | --- | --- |
| D35 | **Lo cancelado y lo anulado van en la columna «Estado», no con `AppAlertIcon`.** La convención cerrada por el plan de `AppAlertIcon` dice que un estado en su propia columna no es un aviso (D2) y que la etiqueta «Anulada» se queda en la columna «Estado» (P1). Así, en Salidas (D10) la cancelada muestra «Cancelada» en «Estado», con la fecha y el motivo en el tooltip, y la fila va en rojo tenue; la pestaña «Guías» (D11) suma la columna «Estado» («Vigente» o «Anulada», igual) en lugar del icono junto al número, y su filtro de estado queda en esa columna. `AppAlertIcon` se usa solo junto a un dato: depósito sin cliente o con las salidas bloqueadas, tiquete en otra salida (D12). La guardia «aviso junto a un dato» de `FT/unit/guards/source-guards.spec.ts` rige para las pantallas nuevas | `D/contexto/convenciones-tecnicas.md` §3 («Qué no es un aviso»); `D/planes/sprint-11/plan-cerrado-f2-alert-icon-f01-f04-2026-11-26.md`, D2 y P1 |
| D36 | **Formato numérico es-CO** (`DEC-082`). Frontend: todo número que muestra la pantalla (cantidades, saldos, pesos, «{p} % ubicado», «Cargado {n}», «Total a despachar», el total del cobro) sale con `F/shared/utils/format.ts`: COP sin decimales; cantidades, pesos y porcentajes con hasta 2 decimales, sin ceros de relleno. Cada `InputNumber` nuevo solo lleva `locale="es-CO"`: el plugin `F/plugins/inputnumber-decimal-point.client.ts` hace que el punto también sea decimal. Backend: un texto nuevo para el usuario con números usa `WmsCulture.Instance` o `QuantityDisplay.Quantity`; la guardia `Wms.Tests/Common/NumberCultureGuardTests.cs` lo vigila. Los mensajes de C-F06 no tienen números salvo «10 MB», que es texto fijo | `DEC-082`; `D/contexto/convenciones-tecnicas.md` §3 («Formato numérico es-CO») |
| D37 | **El PDF de la guía sale con su parámetro de formato.** C-F01-106, C-F01-107 y C-F06-09 usan el mismo `DispatchGuidePdfService`, que elige LEGACY o V2 con `DISPATCH_GUIDE_FORMAT` (`DEC-060` ampliada); la guía anulada lleva «ANULADA» en los dos (`B/Wms.Application/ForeignTrade/Common/Services/Pdf/LegacyDispatchGuidePdfRenderer.cs:42`, `…/Pdf/V2/V2DispatchGuidePdfRenderer.cs:65`). F06 no cambia el PDF; QA2-F06-010 y QA2-F06-042 se verifican con el valor que tenga el parámetro (hoy LEGACY) | `D/contexto/convenciones-tecnicas.md` §3 («Formatos de los documentos impresos»); plan `D/planes/sprint-11/plan-cerrado-f2-formatos-pdf-v2-2026-11-26.md` |

Sin efecto en F06, revisado: el estado aduanero del depósito («Nacionalizado» con un levante; nota de `DEC-080` del 2026-11-26) coincide con la regla de los depósitos que pueden salir (C-F06-07) y con el botón «Nueva salida» de la etapa (D21); las líneas de la guía guardan ahora todos los levantes del producto (`DispatchGuideLine.ReleaseNumber`), lo que no toca los saldos de C-F06-02; la migración `AddPdfFormatParameters` ya está en `fase-2`, y la de BE-2 se genera después de ella (§0.4).

---

## 2. Contrato (parte 0)

Es la única fuente del frontend para F06 (`PM/` R3). Los endpoints de F01, F03, F04 y F05 que F06 consume sin cambios se citan por su ID, sin copiar la ficha.

### 2.0 Convenciones

Rigen `P01/` §2.0 (base `/api/v1`, JSON en camelCase, enums como texto, fechas ISO 8601 con zona y `DateOnly` en día de Colombia, `{ data, pagination }`, `pageSize` de 1 a 50 con `all=true`, errores *ProblemDetails* con `description` y `errors[]`, motivos de 10 a 500 caracteres) y la convención de orden y filtros por columna **C-F01-00**. Identificadores: `C-F06-mm` y `QA2-F06-nnn` (`PM/` §5.1). Regla del frontend: mostrar `errors[].description` si la lista no está vacía; si no, `description`. Los errores de negocio van con `BadRequestException`, `ConflictException` o `NotFoundException` y su mensaje llega en `description` (nota de BE-1 de `P04/` §8.1).

### 2.1 Índice

| ID | Endpoint | Cambio | Política | Pantallas | Fase |
| --- | --- | --- | --- | --- | --- |
| C-F06-01 | `GET exits` | modificado (sobre C-F04-03): mercancía, origen, modalidad, observaciones y registro de Bodega; filtros de tiquete, depósito o producto, cuadrilla, atendidas por Bodega y fecha del registro; orden por la fecha del registro (D6, D7) | `ExitAccess` | P-CE-11, P-CE-08, P-BOD-06, P-BOD-09, tableros | BE-1 |
| C-F06-02 | `GET exits/{id}` | modificado (sobre C-F04-04): tipo de vehículo, cliente de cada depósito, saldos y ubicado por línea, salida, firmante y observaciones de la guía; en BE-2, la orden del cliente sin número (D9) | `ExitAccess` | Drawer, formulario, P-CE-08, P-BOD-07, P-BOD-08 | BE-1 y BE-2 |
| C-F06-03 | `POST exits` | modificado (sobre C-F01-96): orden del cliente sin número y con el soporte (D9) | `ForeignTradeAccess` | «Nueva salida» | BE-2 |
| C-F06-04 | `PUT exits/{id}` | modificado (sobre C-F01-97): igual, y conservar o quitar el soporte (D9) | `ForeignTradeAccess` | «Editar» | BE-2 |
| C-F06-05 | `POST exits/{id}/confirm` | modificado (sobre C-F05-21 y C-F01-98): sin «Clientes»; un solo destinatario paga la guía (AF-106, D33) | `ForeignTradeAccess` | Confirmación | BE-2 |
| C-F06-06 | `GET exits/{id}/guide/charge` | nuevo: cobro sugerido de la guía (D4) | `ForeignTradeAccess` | Confirmación | BE-2 |
| C-F06-07 | `GET exits/eligible-deposits` | nuevo: depósitos que pueden salir (D12) | `ForeignTradeAccess` | Formulario | BE-1 |
| C-F06-08 | `GET exits/guides` | nuevo: guías vigentes y anuladas (D3, D11) | `ForeignTradeAccess` | P-CE-11 (pestaña «Guías») | BE-1 |
| C-F06-09 | `GET exits/guides/{guideId}/pdf` | nuevo: PDF de una guía, también anulada (D3) | `ForeignTradeAccess` | P-CE-11 (pestaña «Guías») | BE-1 |
| C-F06-10 | `GET foreign-trade/deposits` (C-F05-01) y `GET foreign-trade/{imports\|exports\|inspections}/{id}` (C-F05-05 a C-F05-07) | modificados por regla: `pendingStages` incluye `Exits` (D5, D22); la forma no cambia | las de hoy | P-CE-01, P-CE-02 (stepper) | BE-1 |

Ninguno se retira: la orden de cargue y la guía por orden ya los retiró F01 (C-F01-112 a C-F01-138).

**Consumidos sin cambios.** Comprobados contra el código de `348ab15` (controlador, DTO, validador y mensajes); donde difieren, gana lo integrado y se anota:

| ID | Endpoint | Lo usa | Nota de la comprobación |
| --- | --- | --- | --- |
| C-F01-99 | `POST exits/{id}/reopen` | Anular guía, Reabrir salida (D15) | Coincide (`B/Wms.Application/Exits/Common/ExitStateRules.cs`: «La salida {N} está completada: ya no se modifica.», «La salida {N} no está confirmada.») |
| C-F01-100 | `POST exits/{id}/cancel` | Cancelar salida (D15) | Coincide («Solo se cancela una salida en Borrador.») |
| C-F01-101 | `GET exits/by-plate/{plate}` | P-BAS-03 (F03, sin cambio de pantalla) | Devuelve el DTO de C-F06-02: su esquema (`exitSchema`) cambia y Báscula lo sigue validando (`F/features/weighbridge/services/registration.http.ts:3`); I-06 lo verifica (R4) |
| C-F01-102 | `GET exits/available-stock` | Formulario, sección Mercancía | Coincide |
| C-F01-103 | `GET exits/entry-tickets` | Formulario, sección Tiquetes | Coincide |
| C-F01-104 | `POST exits/{id}/loading` | P-BOD-07 | La respuesta trae además `releasedPlacements` y `differsFromGuide` (ficha de F01) y `warehouseClock` (nota de BE-1 de `P04/`): F06 agrega `exitLoadingResultSchema` (D27). Mensajes de forma de F01 fase 5: «La observación del cargue admite hasta 250 caracteres.», «Una línea está repetida en el cargue.», «Una línea del cargue no pertenece a la salida.» |
| C-F01-105 | `POST exits/{id}/yard-exit` | P-BOD-08 | Coincide; más «La observación de la salida de patio admite hasta 250 caracteres.» |
| C-F01-106 | `GET exits/{id}/guide/pdf` | Descargar guía (vigente) | Coincide |
| C-F01-107 | `GET exits/{id}/guide/pdf/per-deposit` | PDF por depósito (ZIP) | Coincide |
| C-F01-108 | `PATCH exits/{id}/guide/payment-mode` | Cambiar modo de pago (D16) | **Difiere:** la petición también recibe `paymentMethod` (`ChangePaymentModeRequest`, `B/Wms.Api/Controllers/v1/ExitsController.cs:181-191`), obligatorio al pasar a «Pago inmediato» (400 «Seleccione el método del pago de contado.»). Gana el código: `guidePaymentModeSchema` suma `paymentMethod` (D27). Otros mensajes: 404 «La salida no tiene guía.» |
| C-F01-15, C-F01-17 | `GET` y `POST drivers` | Conductor con «+» | — |
| C-F01-21, C-F01-23 | `GET` y `POST vehicles` | Vehículo con «+» (`VehicleQuickDialog`); la placa del tiquete (`licensePlate`) | — |
| C-F04-17 | `GET weighbridge/vehicle-types` | Tipo de vehículo en `VehicleQuickDialog` | — |
| C-F01-25, C-F01-26, C-F01-141 | `GET stakeholder`, `GET stakeholder/{id}`, `POST stakeholder/quick` | Empresa de transporte (`businessRolCode=TRANSPORT_COMPANY`), emisor de la orden (`CUSTOMS_AGENCY` o `IMPORTER`) y tercero del cobro | — |
| C-F01-47 | `GET administration/cities` | Ciudad de destino (`transitDays` para el vencimiento) | — |
| C-F01-52 | `GET administration/crews` | Cuadrilla del cargue (P-BOD-07) | — |
| C-F05-05 a C-F05-07 | detalle del depósito | La etapa Salidas lee el depósito del detalle que ya carga la página | Su `pendingStages` cambia por C-F06-10 |

### 2.2 Fichas

#### Grupo A — Lecturas de las salidas (BE-1)

##### C-F06-01 · `GET exits` (modificado sobre C-F04-03)

- **Política:** `ExitAccess` (`B/Wms.Api/Controllers/v1/ExitsController.cs:26-27`).
- **Qué cambia:** cada fila suma `origin`, `modalityCode`, `observations`, `products[]` (una por línea) y `warehouseRecord` (el registro de Bodega, nulo si no hay). Filtros nuevos: `ticketNumber`, `depositOrProduct`, `crew`, `attendedByWarehouse`, `warehouseRecordAtFrom` y `warehouseRecordAtTo`. Orden nuevo: `warehouseRecordAt`. Los filtros y el orden de hoy no cambian (`B/Wms.Application/Exits/Queries/GetExitsQuery.cs:14-38`).
- **Petición (query):** la de C-F01-94 y C-F04-03, más:

| Campo | Tipo | Regla |
| --- | --- | --- |
| `ticketNumber` | texto | Contiene, en los tiquetes de la salida |
| `depositOrProduct` | texto | Contiene, en el número de depósito o en el nombre del producto de sus líneas |
| `crew` | texto | Contiene, en el nombre de la cuadrilla del cargue |
| `attendedByWarehouse` | boolean | `true`: con cargue o salida de patio registrados y no canceladas (D6) |
| `warehouseRecordAtFrom`, `warehouseRecordAtTo` | `yyyy-MM-dd` | Rango por día de Colombia de la fecha del registro de Bodega (C-F01-00) |

- **Orden:** lista blanca `number`, `createdAt`, `type`, `status`, `confirmedAt` y `warehouseRecordAt` (= fecha del cargue o, si no hay, de la salida de patio; sin registro va al final); por defecto `createdAt desc`.
- **Respuesta 200:** `pagedSchema(exitListItemSchema)` (§2.3):

```jsonc
{
  // …campos de C-F01-94 y warehouseClock de C-F04-03…
  "origin": "Weighbridge",                  // ForeignTrade | Weighbridge
  "modalityCode": "IMP001",                 // nulo en el Borrador de Báscula sin líneas
  "observations": null,
  "products": [
    { "warehouseStorageId": "guid", "warehouseStorageNumber": "2026BA00010", "productName": "Cebolla",
      "packaging": "Sacos", "quantity": 300, "loadedQuantity": 300, "allocatedWeight": 14850.5 }
  ],
  "warehouseRecord": {                      // nulo sin cargue ni salida de patio
    "kind": "Loading",                      // Loading | YardExit
    "at": "2026-11-11T09:30:00-05:00", "byName": "Usuario Bodega 1",
    "crewName": "Cuadrilla 2",              // nulo en YardExit o sin cuadrilla
    "loadedQuantity": 300                   // suma de lo cargado; nulo en YardExit
  }
}
```

- **Errores:** los de C-F01-00 (orden fuera de la lista, enum desconocido, rango de fechas al revés).
- **Zod:** `exitListQuerySchema`, `exitListItemSchema`.
- **Notas:** Salidas de CE (D10) = sin filtros fijos, `createdAt desc`. Órdenes de salida (D17) = `status=Confirmed&missing=Loading,YardExit&sortField=confirmedAt&sortOrder=asc`. Historial de Bodega (D20) = `attendedByWarehouse=true&sortField=warehouseRecordAt&sortOrder=desc`. Etapa Salidas (D21) = `warehouseStorageId={id}&all=true`. Tableros (D29) = `status=Draft&pageSize=1` y `status=Confirmed&pageSize=1` (se lee `pagination.totalCount`).

##### C-F06-02 · `GET exits/{id}` (modificado sobre C-F04-04)

- **Política:** `ExitAccess`. **Petición:** el Id en la ruta.
- **Qué cambia** (BE-1): `vehicle.vehicleTypeName`; `deposits[].customerId`; por línea, `receivedQuantity`, `previousBalance`, `newBalance` y `placedQuantity`; en la guía, `departureAt`, `signerName` y `observations`. **En BE-2** (D9): `customerOrder` pierde `number` y sus otros campos pasan a nulables. `GET exits/by-plate/{plate}` (C-F01-101) y las respuestas de C-F01-96 a C-F01-105 devuelven el mismo DTO, así que también los traen.
- **Reglas de los campos nuevos:**
  - `receivedQuantity`: cantidad ingresada del producto en el depósito.
  - `previousBalance` y `newBalance`: en una salida Confirmada o Completada con guía, los congelados en la línea de la guía vigente (`B/Wms.Domain/Entities/Warehouse/DispatchGuideLine.cs:22-26`, enlazada por `GoodsExitLineId`); en la de inspección, los del movimiento `Out` de origen `GoodsExit` de su confirmación (`InventoryMovement.PreviousStock` y `NewStock`, `SourceId` = la salida; con dos líneas del mismo producto, en el orden de las líneas); en Borrador y Cancelada, el stock actual del producto (o de su unidad de carga) y ese stock menos la cantidad.
  - `placedQuantity`: lo ubicado del producto (o de su unidad de carga) en el depósito, incluida la ubicación `SOBRE-VEHICULO` (`P04/` D4), con tope la cantidad de la línea. Es lo que el cargue libera (`P01/` D38); solo informa.
  - `guide.departureAt`, `guide.signerName`, `guide.observations`: los de `DispatchGuide` (`B/Wms.Domain/Entities/Warehouse/DispatchGuide.cs:18-24`).
- **Respuesta 200:** `dataSchema(exitSchema)` (§2.3):

```jsonc
{
  // …campos de C-F01-95 y warehouseClock de C-F04-04…
  "vehicle": { "id": "guid", "licensePlate": "GHI321", "vehicleTypeName": "Sencillo" },
  "deposits": [ { "warehouseStorageId": "guid", "number": "2026BA00010", "customerId": "guid", "customerName": "Cliente A" } ],
  "customerOrder": { "issuerId": "guid", "issuerName": "Agencia A", "date": "2026-11-11", "fileUrl": "/uploads/exit-customer-orders/…" },
                                            // BE-2: sin number; nulo si la salida no tiene orden del cliente
  "lines": [
    { /* …campos de hoy… */ "receivedQuantity": 760, "previousBalance": 760, "newBalance": 460, "placedQuantity": 300 }
  ],
  "guide": { /* …campos de hoy… */ "departureAt": "2026-11-12T10:00:00-05:00", "signerName": "Conductor 5", "observations": null }
}
```

- **Errores:** los de hoy (404 «La salida no existe.»). **Zod:** `exitSchema`.

##### C-F06-07 · `GET exits/eligible-deposits` (nuevo)

- **Política:** `ForeignTradeAccess`.
- **Petición (query):**

| Campo | Tipo | Obligatorio | Regla |
| --- | --- | --- | --- |
| `search` | texto | No | Contiene, en el número de depósito, el documento comercial, el cliente o el importador |
| `modality` | `Import` \| `Export` \| `Inspection` | No | Solo esa modalidad (la del primer depósito elegido, `P01/` D33); por prefijo del código, como `DepositStageRules.ModalityOf` |
| `exceptExitId` | guid | No | Al editar: las reservas de esa salida cuentan como disponibles |
| `pageIndex`, `pageSize`, `all`, `sortField`, `sortOrder` | — | No | C-F01-00; lista blanca `number`, `entryDate`; por defecto `entryDate desc` |

- **Regla:** depósitos Confirmados, con algo disponible: stock menos lo reservado por otras salidas (`P01/` D35) mayor que cero y, en importación, también lo nacionalizado disponible mayor que cero (con al menos un levante). No salen los Borrador, Cerrado ni Anulado.
- **Respuesta 200:** `pagedSchema(eligibleDepositSchema)`:

```jsonc
{
  "warehouseStorageId": "guid", "number": "2026BA00003", "modality": "Import", "modalityCode": "IMP001",
  "documentLabel": "Carta porte 123456",
  "entryDate": "2026-11-02T09:40:00-05:00",
  "customerId": "guid", "customerName": "Cliente A",      // nulos si el depósito no tiene cliente
  "importerName": "Importador A",
  "exitsBlocked": false, "exitsBlockedReason": null,      // marca «sin salidas» del cliente (BR-05-004)
  "productCount": 1,
  "availableQuantity": 300                               // en importación, el menor entre disponible y nacionalizado disponible
}
```

- **Errores:** los de C-F01-00 (incluido 400 «El valor «{valor}» no es válido para modality.»).
- **Zod:** `eligibleDepositQuerySchema`, `eligibleDepositSchema`.
- **Notas:** es la fuente del selector de depósitos (P-TR-11) de D12. El cliente faltante y el bloqueo no excluyen al depósito: el Borrador se arma igual y lo que se detiene es la confirmación (nota de la fase 5 de F01; C-F05-21).

##### C-F06-08 · `GET exits/guides` (nuevo)

- **Política:** `ForeignTradeAccess` (la del historial de guías de hoy, C-F01-119).
- **Petición (query), orden y filtros (C-F01-00):**

| Campo | Tipo | Regla |
| --- | --- | --- |
| `number` | texto | Contiene, en el número de la guía |
| `exitNumber` | texto | Contiene, en el número de la salida |
| `exitId` | guid | Solo las guías de esa salida |
| `issuedAtFrom`, `issuedAtTo` | `yyyy-MM-dd` | Rango de la emisión |
| `status` | `Active`, `Cancelled` (varios) | Vigente o anulada |
| `customer` | texto | Contiene, en el nombre de un cliente de sus depósitos |
| `depositNumber` | texto | Contiene |
| `licensePlate` | texto | Contiene, en la placa del vehículo o de los tiquetes |
| `product` | texto | Contiene, en el producto de sus líneas |
| `paymentMode` | `Immediate`, `PendingBilling` (varios) | — |

- **Orden:** lista blanca `number`, `issuedAt`, `exitNumber`; por defecto `issuedAt desc`.
- **Respuesta 200:** `pagedSchema(guideListItemSchema)`:

```jsonc
{
  "id": "guid", "number": "2026S00034", "issuedAt": "…", "departureAt": "…", "expirationDate": "…",
  "status": "Cancelled", "cancelledAt": "…", "cancellationReason": "Cambio de placa",
  "paymentMode": "Immediate", "signerType": "Driver", "signerName": "Conductor 5", "invoiceId": "guid",
  "exitId": "guid", "exitNumber": "2026SM00041", "exitType": "Consolidated", "exitStatus": "Draft",
  "depositNumbers": ["2026BA00011", "2026BA00015"], "customerNames": ["Cliente A"],
  "licensePlates": ["PQR555"], "driverName": "Conductor 5",
  "products": [ { "productName": "Cebolla", "packaging": "Sacos", "quantity": 120, "cargoUnitIdentifier": null } ]
                                            // de las líneas congeladas de la guía (DispatchedQuantity)
}
```

- **Errores:** los de C-F01-00. **Zod:** `guideListQuerySchema`, `guideListItemSchema` (`F/features/exits/contracts/guide.ts`).

##### C-F06-09 · `GET exits/guides/{guideId}/pdf` (nuevo)

- **Política:** `ForeignTradeAccess`. **Petición:** el Id de la guía en la ruta.
- **Respuesta 200:** `application/pdf`, nombre `guia-{número}.pdf`, con el mismo `DispatchGuidePdfService` de C-F01-106; sale con el formato que fija `DISPATCH_GUIDE_FORMAT` (LEGACY o V2, D37) y la anulada lleva la marca de agua «ANULADA» en los dos (`B/Wms.Application/ForeignTrade/Common/Services/Pdf/LegacyDispatchGuidePdfRenderer.cs:42`, `B/Wms.Application/ForeignTrade/Common/Services/Pdf/V2/V2DispatchGuidePdfRenderer.cs:65`). El servicio ya genera por Id de guía (`IDispatchGuidePdfService.GenerateDispatchGuidePdfAsync`, `B/Wms.Application/ForeignTrade/Common/Services/IDispatchGuidePdfService.cs:14`).
- **Errores:** 404 «La guía no existe.». **Zod:** no aplica (archivo).

##### C-F06-10 · Lecturas del depósito con la etapa Salidas (modificadas por regla)

- **Endpoints:** `GET foreign-trade/deposits` (C-F05-01) y `GET foreign-trade/{imports|exports|inspections}/{id}` (C-F05-05 a C-F05-07). **Política:** las de hoy.
- **Qué cambia:** `pendingStages` incluye `Exits` cuando el depósito tiene una salida Confirmada (no Completada ni Cancelada) con alguna línea suya y algo en `missing`; también si el depósito está Cerrado, donde es la única etapa que se marca (D5, D22). En Anulado, ninguna. `warehouseLevel` no cambia (solo la etapa Bodega). `DepositStageInput` suma el dato (`B/Wms.Application/ForeignTrade/Common/Services/DepositStageRules.cs:30`) y `DepositOverviewReader` lo llena (`…/DepositOverviewReader.cs:209`).
- **Petición:** la de hoy. **Respuesta 200:** la de hoy, con el valor nuevo de `pendingStages`.
- **Errores:** los de hoy.
- **Zod:** los de F05, sin cambios: `depositStageSchema` ya acepta `Exits` (`F/features/foreign-trade/contracts/deposit.ts:12`).

#### Grupo B — Escrituras y cobro (BE-2)

##### C-F06-03 · `POST exits` (modificado sobre C-F01-96)

- **Política:** `ForeignTradeAccess`.
- **Qué cambia:** solo `customerOrder` (D9). Lo demás de C-F01-96 no cambia.
- **Petición:** `exitUpsertSchema` (§2.3); `customerOrder`:

| Campo | Tipo | Obligatorio | Regla |
| --- | --- | --- | --- |
| `customerOrder` | objeto \| null | No | Con los tres campos vacíos se guarda como sin orden |
| `customerOrder.issuerId` | guid \| null | No | Agencia de aduanas o importador activo |
| `customerOrder.date` | `yyyy-MM-dd` \| null | No | No futura |
| `customerOrder.file` | `{ fileName, contentType, base64 }` \| null | No | PDF, JPG o PNG, hasta 10 MB, como la orden externa de hoy; se guarda con el almacenamiento de archivos del sistema, en su carpeta |
| `customerOrder.keepCurrentFile` | boolean | No | Solo en `PUT` (C-F06-04); en `POST` se ignora |

- **Sale:** `customerOrder.number` y su 400 «El número de la orden del cliente es obligatorio (hasta 50 caracteres).»; `customerOrder.fileUrl` deja de recibirse (lo devuelve la lectura).
- **Respuesta 201:** `dataSchema(exitSchema)`, con `customerOrder.fileUrl`.
- **Errores:** los de C-F01-96 y:

| Status | Mensaje |
| --- | --- |
| 400 | «El emisor de la orden del cliente debe ser una agencia de aduanas o un importador registrado.» (de hoy) |
| 400 | «La fecha de la orden del cliente no puede ser futura.» (de hoy) |
| 400 | «El soporte de la orden del cliente debe ser PDF, JPG o PNG.» |
| 400 | «El soporte de la orden del cliente no es un archivo válido.» |
| 400 | «El soporte de la orden del cliente supera los 10 MB.» |

- **Zod:** `exitUpsertSchema`, `exitSchema`.

##### C-F06-04 · `PUT exits/{id}` (modificado sobre C-F01-97)

- **Política:** `ForeignTradeAccess`. **Qué cambia:** lo de C-F06-03. Con `customerOrder.file` nulo, `keepCurrentFile: true` conserva el soporte que ya tenía la salida y `false` lo quita; un archivo nuevo reemplaza al anterior.
- **Respuesta 200:** `dataSchema(exitSchema)`. **Errores:** los de C-F06-03 y los de C-F01-97. **Zod:** `exitUpsertSchema`, `exitSchema`.

##### C-F06-05 · `POST exits/{id}/confirm` (modificado sobre C-F05-21 y C-F01-98)

- **Política:** `ForeignTradeAccess` (`B/Wms.Api/Controllers/v1/ExitsController.cs:69-70`).
- **Qué cambia** (AF-106, D33): `billing.recipientMode` es `registered`, `unregistered` o `finalConsumer`. Un solo destinatario paga la guía aunque los depósitos sean de varios clientes: sale la exigencia de «Clientes» (`B/Wms.Application/Exits/Common/ExitGuideIssuer.cs:40-44`) y la factura por cliente (`:53-58`, `:124-170`). Con `registered` sin `customerId`, el tercero es el primer cliente de la salida, como hoy (`:173-177`). La mora de cada cliente se sigue validando (`:46-47`) y la marca «sin salidas» y el cliente obligatorio (C-F05-21) siguen.
- **Petición:** `exitConfirmSchema` (§2.3). **Respuesta 200:** la de C-F01-98.
- **Errores:** los de C-F01-98 y C-F05-21, menos 400 «La salida {N} tiene depósitos de {n} clientes: la guía se factura a cada cliente dueño. Use el destinatario «Clientes».»; con `multiClient`, 400 de hoy del cobro: «El destinatario de facturación 'multiClient' no es válido para este servicio.» (`B/Wms.Application/Billing/Common/Services/BillingRecipientFactory.cs:95-96`).
- **Zod:** `exitConfirmSchema`, `billingRecipientInputSchema` (sin `multiClient`, D33), `exitSchema`.

##### C-F06-06 · `GET exits/{id}/guide/charge` (nuevo)

- **Política:** `ForeignTradeAccess`. **Petición:** el Id de la salida en la ruta.
- **Regla** (D4): salida en Borrador de importación o exportación. Si las líneas son de depósitos de un solo cliente, el precio es el de `GetGuidePriceAsync(cliente)` (su convenio o el precio general); si son de varios clientes, o aún no tiene líneas, el precio general de `GUIA_SALIDA`. El IVA, con la tasa del servicio (`billingService.GetTotalTaxRate`, como `ExitGuideIssuer.cs:49-51`).
- **Respuesta 200:** `dataSchema(exitGuideChargeSchema)`:

```jsonc
{
  "customerId": "guid", "customerName": "Cliente A",   // nulos con varios clientes o sin líneas
  "priceSource": "Agreement",                         // Agreement | General
  "unitPrice": 40000, "taxRate": 19, "taxAmount": 7600, "totalAmount": 47600
}
```

- **Errores:**

| Status | Mensaje |
| --- | --- |
| 404 | «La salida no existe.» |
| 409 | «La salida {N} no está en Borrador.» |
| 409 | «La salida {N} es de inspección: no lleva guía ni cobro.» |
| 409 | «El servicio de la guía de salida no está configurado.» |

- **Zod:** `exitGuideChargeSchema` (`F/features/exits/contracts/exit-charge.ts`). **Notas:** la pantalla precarga `customerId` en `defaultCustomerId` y `totalAmount` en `total` de `AppChargeForm` (`editableTotal`); el texto bajo el total dice «Precio del convenio de {cliente}» o «Precio general».

### 2.3 Esquemas Zod y tipos

API de Zod 4 (`Frontend/wms/package.json`: `zod` `^4.1.13`), con las ayudas de `F/shared/contracts/api.ts` (`guidSchema` = `z.guid()`, `dateTimeSchema` = `z.iso.datetime({ offset: true })`, `dateOnlySchema` = `z.iso.date()`). Las refinaciones nuevas usan el parámetro `error` de Zod 4.

**`F/features/exits/contracts/exit.ts`** (completo después de F06; lo escribe FE-1, salvo `customerOrder` de la lectura y la escritura, que FE-1 ya deja en su forma de BE-2):

```ts
import { z } from "zod";
import { dateOnlySchema, dateTimeSchema, guidSchema, identificationTypeSchema, listQueryBaseSchema } from "~/shared/contracts/api";
import { billingRecipientInputSchema, paymentMethodSchema, paymentModeSchema } from "~/features/billing/contracts/billing-recipient";
import { clockLevelSchema, warehouseClockSchema } from "~/features/warehouse/contracts/clock";

// DEC-080 — Salida de mercancía: F01 (C-F01-94 a C-F01-108), F04 (warehouseClock, C-F04-03 y C-F04-04) y F06 (C-F06-01 a C-F06-05).

export const exitTypeSchema = z.enum(["EntryTicket", "Global", "Deposit", "Consolidated"]);
export const exitKindSchema = z.enum(["EntryTicket", "Global", "ByDeposit"]);
export const exitStatusSchema = z.enum(["Draft", "Confirmed", "Completed", "Cancelled"]);
export const exitMissingSchema = z.enum(["Loading", "Weighing", "YardExit"]);
export const exitOriginSchema = z.enum(["ForeignTrade", "Weighbridge"]);
export const depositModalitySchema = z.enum(["Import", "Export", "Inspection"]);

export const exitLineSchema = z.object({
  id: guidSchema, warehouseStorageId: guidSchema, warehouseStorageNumber: z.string(),
  warehouseStorageProductId: guidSchema, productName: z.string(), packaging: z.string().nullable(),
  cargoUnitId: guidSchema.nullable(), quantity: z.number().positive(),
  loadedQuantity: z.number().min(0).nullable(), allocatedWeight: z.number().nullable(),
  receivedQuantity: z.number(),               // F06 (C-F06-02)
  previousBalance: z.number(),
  newBalance: z.number(),
  placedQuantity: z.number().min(0),
});
export const exitGuideSchema = z.object({
  id: guidSchema, number: z.string(), issuedAt: dateTimeSchema, expirationDate: dateTimeSchema,
  signerType: z.enum(["Importer", "Driver"]), paymentMode: paymentModeSchema, invoiceId: guidSchema.nullable(),
  isCancelled: z.boolean(),
  departureAt: dateTimeSchema,                // F06 (C-F06-02)
  signerName: z.string().nullable(),
  observations: z.string().nullable(),
});
export const exitCustomerOrderSchema = z.object({ // F06 (D9): sin número
  issuerId: guidSchema.nullable(), issuerName: z.string().nullable(),
  date: dateOnlySchema.nullable(), fileUrl: z.string().nullable(),
});
export const exitSchema = z.object({
  id: guidSchema,
  number: z.string(),
  type: exitTypeSchema,
  status: exitStatusSchema,
  missing: z.array(exitMissingSchema),
  origin: exitOriginSchema,
  modalityCode: z.string().nullable(),
  createdAt: dateTimeSchema,
  vehicle: z.object({ id: guidSchema, licensePlate: z.string(), vehicleTypeName: z.string().nullable() }),
  driver: z.object({ id: guidSchema, fullName: z.string(), idType: identificationTypeSchema, idNumber: z.string() }),
  carrierCompany: z.object({ id: guidSchema, name: z.string() }).nullable(),
  destination: z.object({ cityId: guidSchema.nullable(), cityName: z.string().nullable(), address: z.string().nullable() }),
  customerOrder: exitCustomerOrderSchema.nullable(),
  observations: z.string().nullable(),
  deposits: z.array(z.object({
    warehouseStorageId: guidSchema, number: z.string(), customerId: guidSchema.nullable(), customerName: z.string().nullable(),
  })),
  tickets: z.array(z.object({ warehouseStorageEntryId: guidSchema, ticketNumber: z.string(), licensePlate: z.string() })),
  lines: z.array(exitLineSchema),
  guide: exitGuideSchema.nullable(),
  loading: z
    .object({ loadedAt: dateTimeSchema, loadedByName: z.string(), crewId: guidSchema.nullable(), crewName: z.string().nullable(),
              observations: z.string().nullable(), photoCount: z.int().min(0) })
    .nullable(),
  yardExit: z.object({ exitedAt: dateTimeSchema, exitedByName: z.string(), observations: z.string().nullable() }).nullable(),
  weighing: z.object({ cycleId: guidSchema, ticketNumber: z.string().nullable(), status: z.string(), netWeight: z.number().nullable() }).nullable(),
  dispatchedWeight: z.number().nullable(),
  confirmedAt: dateTimeSchema.nullable(),
  confirmedByName: z.string().nullable(),
  cancelledAt: dateTimeSchema.nullable(),
  cancelledByName: z.string().nullable(),
  cancellationReason: z.string().nullable(),
  guideHistory: z.array(z.object({ number: z.string(), cancelledAt: dateTimeSchema, reason: z.string() })),
  warehouseClock: warehouseClockSchema.nullable(), // F04 (C-F04-04)
});
export const exitLoadingResultSchema = exitSchema.extend({ // C-F01-104 (D27)
  releasedPlacements: z.array(z.object({ locationCode: z.string(), quantity: z.number() })),
  differsFromGuide: z.boolean(),
});

export const exitListProductSchema = z.object({
  warehouseStorageId: guidSchema, warehouseStorageNumber: z.string(), productName: z.string(), packaging: z.string().nullable(),
  quantity: z.number(), loadedQuantity: z.number().nullable(), allocatedWeight: z.number().nullable(),
});
export const exitWarehouseRecordSchema = z.object({
  kind: z.enum(["Loading", "YardExit"]), at: dateTimeSchema, byName: z.string(),
  crewName: z.string().nullable(), loadedQuantity: z.number().nullable(),
});
export const exitListItemSchema = z.object({
  id: guidSchema, number: z.string(), createdAt: dateTimeSchema, type: exitTypeSchema, status: exitStatusSchema,
  missing: z.array(exitMissingSchema), depositNumbers: z.array(z.string()), licensePlates: z.array(z.string()),
  ticketNumbers: z.array(z.string()), guideNumber: z.string().nullable(), confirmedAt: dateTimeSchema.nullable(),
  dispatchedWeight: z.number().nullable(), destinationCityName: z.string().nullable(),
  warehouseClock: warehouseClockSchema.nullable(), // F04 (C-F04-03)
  origin: exitOriginSchema,                        // F06 (C-F06-01)
  modalityCode: z.string().nullable(),
  observations: z.string().nullable(),
  products: z.array(exitListProductSchema),
  warehouseRecord: exitWarehouseRecordSchema.nullable(),
});
export const exitListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["number", "createdAt", "type", "status", "confirmedAt", "warehouseRecordAt"]).optional(),
  number: z.string().optional(), createdAtFrom: dateOnlySchema.optional(), createdAtTo: dateOnlySchema.optional(),
  type: z.array(exitTypeSchema).optional(), status: z.array(exitStatusSchema).optional(), missing: z.array(exitMissingSchema).optional(),
  depositNumber: z.string().optional(), licensePlate: z.string().optional(), guideNumber: z.string().optional(),
  warehouseStorageId: guidSchema.optional(),
  warehouseLevel: z.array(clockLevelSchema).optional(), // F04 (C-F04-03)
  ticketNumber: z.string().optional(),                  // F06 (C-F06-01)
  depositOrProduct: z.string().optional(),
  crew: z.string().optional(),
  attendedByWarehouse: z.boolean().optional(),
  warehouseRecordAtFrom: dateOnlySchema.optional(),
  warehouseRecordAtTo: dateOnlySchema.optional(),
});

const maxFileBytes = 10 * 1024 * 1024;
export const exitCustomerOrderFileSchema = z.object({
  fileName: z.string().trim().min(1),
  contentType: z.enum(["application/pdf", "image/jpeg", "image/png"], { error: "El soporte de la orden del cliente debe ser PDF, JPG o PNG." }),
  base64: z.string().min(1),
}).refine((f) => Math.floor((f.base64.length * 3) / 4) <= maxFileBytes, {
  error: "El soporte de la orden del cliente supera los 10 MB.", path: ["base64"],
});
export const exitCustomerOrderInputSchema = z.object({ // F06 (D9)
  issuerId: guidSchema.nullable(),
  date: dateOnlySchema.nullable(),
  file: exitCustomerOrderFileSchema.nullable(),
  keepCurrentFile: z.boolean(),
});
export const exitUpsertSchema = z
  .object({
    kind: exitKindSchema,
    warehouseStorageIds: z.array(guidSchema).min(1),
    ticketEntryIds: z.array(guidSchema),
    lines: z.array(z.object({ warehouseStorageProductId: guidSchema, cargoUnitId: guidSchema.nullable(), quantity: z.number().positive() })).min(1),
    vehicleId: guidSchema,
    driverId: guidSchema,
    carrierCompanyId: guidSchema.nullable(),
    destinationCityId: guidSchema,
    destinationAddress: z.string().max(250).nullable(),
    customerOrder: exitCustomerOrderInputSchema.nullable(),
    observations: z.string().max(500).nullable(),
  })
  .refine((v) => v.kind === "ByDeposit" || v.warehouseStorageIds.length === 1, {
    error: "Una salida por tiquete o global es de un solo depósito.", path: ["warehouseStorageIds"],
  })
  .refine((v) => v.kind !== "EntryTicket" || v.ticketEntryIds.length === 1, {
    error: "Una salida por tiquete lleva un solo tiquete; la global, dos o más.", path: ["ticketEntryIds"],
  })
  .refine((v) => v.kind !== "Global" || v.ticketEntryIds.length >= 2, {
    error: "Una salida por tiquete lleva un solo tiquete; la global, dos o más.", path: ["ticketEntryIds"],
  });
export const exitConfirmSchema = z.object({
  departureDatetime: dateTimeSchema,
  observations: z.string().max(500).nullable(),
  billing: billingRecipientInputSchema.nullable(), // null solo en inspección
});
export const exitLoadingSchema = z.object({
  lines: z.array(z.object({ lineId: guidSchema, loadedQuantity: z.number().min(0) })).min(1),
  crewId: guidSchema.nullable(),
  signatureDriver: z.string().min(1, { error: "La firma del conductor es obligatoria." }),
  observations: z.string().max(250).nullable(),
  photos: z.array(z.object({ fileName: z.string(), contentType: z.string(), base64: z.string() })),
});
export const exitYardExitSchema = z.object({ observations: z.string().max(250).nullable() });
export const guidePaymentModeSchema = z.object({ // C-F01-108 (D27)
  paymentMode: paymentModeSchema,
  paymentMethod: paymentMethodSchema.nullable(),
});
export const availableStockSchema = z.object({
  warehouseStorageId: guidSchema, warehouseStorageNumber: z.string(), warehouseStorageProductId: guidSchema,
  productName: z.string(), packaging: z.string().nullable(), receivedQuantity: z.number(), currentStock: z.number(),
  reservedByOthers: z.number(), available: z.number(), nationalizedAvailable: z.number().nullable(),
  cargoUnits: z.array(z.object({ id: guidSchema, identifier: z.string(), stock: z.number() })),
});
export const entryTicketSchema = z.object({
  warehouseStorageEntryId: guidSchema, ticketNumber: z.string(), licensePlate: z.string(), entryDate: dateTimeSchema,
  products: z.array(z.object({ warehouseStorageProductId: guidSchema, productName: z.string(), packaging: z.string().nullable(), declaredQuantity: z.number() })),
  activeExitNumber: z.string().nullable(),
});
export const eligibleDepositQuerySchema = listQueryBaseSchema.extend({ // C-F06-07
  sortField: z.enum(["number", "entryDate"]).optional(),
  search: z.string().optional(),
  modality: depositModalitySchema.optional(),
  exceptExitId: guidSchema.optional(),
});
export const eligibleDepositSchema = z.object({
  warehouseStorageId: guidSchema, number: z.string(), modality: depositModalitySchema, modalityCode: z.string(),
  documentLabel: z.string().nullable(), entryDate: dateTimeSchema,
  customerId: guidSchema.nullable(), customerName: z.string().nullable(), importerName: z.string().nullable(),
  exitsBlocked: z.boolean(), exitsBlockedReason: z.string().nullable(),
  productCount: z.int().min(0), availableQuantity: z.number().min(0),
});

export type Exit = z.infer<typeof exitSchema>;
export type ExitListItem = z.infer<typeof exitListItemSchema>;
export type ExitUpsert = z.infer<typeof exitUpsertSchema>;
export type ExitLoadingResult = z.infer<typeof exitLoadingResultSchema>;
export type EligibleDeposit = z.infer<typeof eligibleDepositSchema>;
```

**`F/features/exits/contracts/exit-charge.ts`** (FE-1; C-F06-06):

```ts
import { z } from "zod";
import { guidSchema } from "~/shared/contracts/api";

export const exitGuideChargeSchema = z.object({
  customerId: guidSchema.nullable(),
  customerName: z.string().nullable(),
  priceSource: z.enum(["Agreement", "General"]),
  unitPrice: z.number().min(0),
  taxRate: z.number().min(0),
  taxAmount: z.number().min(0),
  totalAmount: z.number().min(0),
});
export type ExitGuideCharge = z.infer<typeof exitGuideChargeSchema>;
```

**`F/features/exits/contracts/guide.ts`** (FE-1; C-F06-08):

```ts
import { z } from "zod";
import { dateOnlySchema, dateTimeSchema, guidSchema, listQueryBaseSchema } from "~/shared/contracts/api";
import { paymentModeSchema } from "~/features/billing/contracts/billing-recipient";
import { exitStatusSchema, exitTypeSchema } from "./exit";

export const guideStatusSchema = z.enum(["Active", "Cancelled"]);
export const guideListItemSchema = z.object({
  id: guidSchema, number: z.string(), issuedAt: dateTimeSchema, departureAt: dateTimeSchema, expirationDate: dateTimeSchema,
  status: guideStatusSchema, cancelledAt: dateTimeSchema.nullable(), cancellationReason: z.string().nullable(),
  paymentMode: paymentModeSchema, signerType: z.enum(["Importer", "Driver"]), signerName: z.string().nullable(),
  invoiceId: guidSchema.nullable(),
  exitId: guidSchema, exitNumber: z.string(), exitType: exitTypeSchema, exitStatus: exitStatusSchema,
  depositNumbers: z.array(z.string()), customerNames: z.array(z.string()), licensePlates: z.array(z.string()),
  driverName: z.string(),
  products: z.array(z.object({
    productName: z.string(), packaging: z.string().nullable(), quantity: z.number(), cargoUnitIdentifier: z.string().nullable(),
  })),
});
export const guideListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["number", "issuedAt", "exitNumber"]).optional(),
  number: z.string().optional(), exitNumber: z.string().optional(), exitId: guidSchema.optional(),
  issuedAtFrom: dateOnlySchema.optional(), issuedAtTo: dateOnlySchema.optional(),
  status: z.array(guideStatusSchema).optional(), customer: z.string().optional(), depositNumber: z.string().optional(),
  licensePlate: z.string().optional(), product: z.string().optional(), paymentMode: z.array(paymentModeSchema).optional(),
});
export type GuideListItem = z.infer<typeof guideListItemSchema>;
```

**`F/features/billing/contracts/billing-recipient.ts`** (FE-2; D33): `recipientMode` queda `z.enum(["registered", "unregistered", "finalConsumer"])`; el resto no cambia. `AppChargeForm` pierde `allowMultiClient` y el modo `multiClient`; sus pruebas y la galería se ajustan.

**Fixtures de otras features** (FE-1): los que arman una `Exit` (`FT/fixtures/weighbridge/world.ts`, `FT/fixtures/weighbridge/registration.mock.ts`) y la prueba `FT/unit/warehouse/mocks.spec.ts` suman los campos nuevos; Báscula no cambia de pantalla.

### 2.4 Pantallas y sus endpoints

| Pantalla | Ruta o componente | Endpoints |
| --- | --- | --- |
| P-CE-11 · Salidas (pestaña «Salidas») | `/foreign-trade/exits` | C-F06-01; acciones C-F01-99, C-F01-100, C-F01-106, C-F01-107, C-F01-108; drawer C-F06-02 |
| P-CE-11 · Salidas (pestaña «Guías») | `/foreign-trade/exits?vista=guias` | C-F06-08, C-F06-09; acciones C-F01-99, C-F01-107, C-F01-108; drawer C-F06-02 |
| P-CE-11 · Nueva salida y Editar | `/foreign-trade/exits/new`, `/foreign-trade/exits/[id]/edit` | C-F06-02 (al editar), C-F06-03, C-F06-04, C-F06-07, C-F01-102, C-F01-103, C-F01-21, C-F01-23, C-F04-17, C-F01-15, C-F01-17, C-F01-25, C-F01-26, C-F01-141, C-F01-47 |
| P-CE-11 · Confirmación con el cobro de la guía | `ExitConfirmDialog` | C-F06-06, C-F06-05; tercero del cobro C-F01-25, C-F01-26, C-F01-141 |
| P-CE-08 · Etapa Salidas | `DepositExitsStage` en `/foreign-trade/{imports\|exports\|inspections}/[id]?etapa=salidas` | C-F06-01, C-F06-02; acciones C-F01-99, C-F01-106, C-F01-107; el depósito, de C-F05-05 a C-F05-07 (ya los carga la página) |
| P-CE-01 y P-CE-02 · Indicador de la etapa | listas y detalle de F05 | C-F06-10 |
| P-BOD-06 · Órdenes de salida | `/warehouse/exits` | C-F06-01; C-F01-106; drawer C-F06-02 |
| P-BOD-07 · Ejecutar salida | `ExitLoadingDialog` | C-F06-02, C-F01-104, C-F01-52 |
| P-BOD-08 · Salida de patio | `YardExitDialog` | C-F06-02, C-F01-105 |
| P-BOD-09 · Historial | `/warehouse/exits/history` | C-F06-01; drawer C-F06-02; C-F01-106 |
| Drawer de la salida | `ExitDetailDrawer` | C-F06-02 y las acciones de su rol (arriba) |
| Tableros de CE y Bodega | `/foreign-trade`, `/warehouse` | C-F06-01 |
| P-BAS-03 (F03, sin cambio de pantalla) | Báscula | C-F01-101 (forma de C-F06-02) |

Todos los endpoints de las pantallas de F06 están en C-F01, C-F04, C-F05 o C-F06.

---

## 3. Archivos que se tocan

### 3.1 Pantallas y componentes

| Pantalla | Página | Componentes nuevos (D25) | Compartidos (D24) | Fase |
| --- | --- | --- | --- | --- |
| P-CE-11 · Salidas y Guías | `F/pages/foreign-trade/exits/index.vue` (nueva) | `ExitListTable`, `GuideListTable`, `ExitMissingTags`, `ExitGoodsCell`, `ExitDetailDrawer`, `ExitDetail` | `AppDataTable`, `AppRowActions`, `AppAlertIcon`, `AppDetailDrawer`, `AppDetailSection`, `ReasonDialog`, `ChangePaymentModeDialog`, `VehiclePlateTag`, `WarehouseClockTag` | FE-1 |
| P-CE-11 · Nueva salida y Editar | `F/pages/foreign-trade/exits/new.vue` y `F/pages/foreign-trade/exits/[id]/edit.vue` (nuevas) | `ExitForm`, `ExitDepositsSection`, `ExitTicketsSection`, `ExitLinesSection`, `ExitTransportSection`, `ExitCustomerOrderSection`, `ExitConfirmDialog`, `VehicleQuickDialog` | `AppSearchSelect`, `AppAlertIcon`, `AppChargeForm` (D33), `DriverQuickDialog`, `StakeholderQuickDialog` | FE-2 |
| P-CE-08 · Etapa Salidas | la de hoy del detalle (`DepositStageDetail`) | `DepositExitsStage` (se rehace) | `DepositStageCard`, `DepositTableBlock`, `AppRowActions`, `ExitDetailDrawer` | FE-2 |
| P-BOD-06 · Órdenes de salida | `F/pages/warehouse/exits/index.vue` (nueva) | `ExitLoadingDialog`, `YardExitDialog` | `AppDataTable`, `AppRowActions`, `WarehouseClockTag`, `VehiclePlateTag`, `ExitDetailDrawer` | FE-3 |
| P-BOD-07 · Ejecutar salida | modal en P-BOD-06 | `ExitLoadingDialog` | `SignaturePad`, `PhotoUploader` | FE-3 |
| P-BOD-08 · Salida de patio | modal en P-BOD-06 | `YardExitDialog` | — | FE-3 |
| P-BOD-09 · Historial | `F/pages/warehouse/exits/history.vue` (nueva) | — | `AppDataTable`, `AppRowActions`, `ExitDetailDrawer` | FE-3 |

### 3.2 Backend

**BE-1:**
- `B/Wms.Application/Exits/Common/ExitDtos.cs`: `ExitListItemDto` (`:96-113`) suma `Origin`, `ModalityCode`, `Observations`, `Products` y `WarehouseRecord`; `ExitDto` (`:7-38`) suma el tipo del vehículo, el cliente de cada depósito, los saldos y lo ubicado por línea, y los datos de la guía.
- `B/Wms.Application/Exits/Queries/GetExitsQuery.cs`: filtros y orden de C-F06-01 (`:14-38`, `:51-89`) y la proyección (`:91-111`).
- `B/Wms.Application/Exits/Common/ExitReader.cs:96-160`: lo nuevo del detalle.
- Nuevas, puras y probadas: `B/Wms.Application/Exits/Common/ExitLineBalances.cs` (de dónde salen los saldos de una línea, C-F06-02) y `ExitWarehouseRecord.cs` (el registro de Bodega y su fecha).
- Nuevas: `B/Wms.Application/Exits/Queries/GetEligibleDepositsQuery.cs` (C-F06-07) y `GetExitGuidesQuery.cs` (C-F06-08), con sus DTO; `GetGuidePdfQuery` en `B/Wms.Application/Exits/Queries/ExitQueries.cs` (C-F06-09, junto a `GetExitGuidePdfQuery`, `:182-222`).
- `B/Wms.Api/Controllers/v1/ExitsController.cs`: `GET eligible-deposits`, `GET guides` y `GET guides/{guideId:guid}/pdf`.
- `B/Wms.Application/ForeignTrade/Common/Services/DepositStageRules.cs:30`, `:102-119` y `DepositOverviewReader.cs:209`: la etapa Salidas (C-F06-10).

**BE-2:**
- `B/Wms.Domain/Entities/Warehouse/GoodsExit.cs:34`, `:108-138`: sale `CustomerOrderNumber` del modelo y de `UpdateData`; `B/Wms.Infrastructure/Persistence/Configurations/Warehouse/GoodsExitConfiguration.cs:21`, su configuración. Migración de §4.
- `B/Wms.Application/Exits/Commands/UpsertExitCommand.cs`: `ExitCustomerOrderRequest` (`:32`) pasa a emisor, fecha, archivo y `KeepCurrentFile`; las reglas de `:130-140` y `:294-300`; el soporte se guarda con el servicio de almacenamiento como hoy la orden externa (`develop` `B/Wms.Application/ForeignTrade/Commands/CreateLoadingOrder/CreateLoadingOrderCommandHandler.cs:442-480`), en la carpeta `exit-customer-orders`.
- `B/Wms.Application/Exits/Common/ExitReader.cs:117-123`: la orden del cliente sin número.
- `B/Wms.Application/Exits/Common/ExitGuideIssuer.cs:30-65`, `:118-205`: un solo destinatario (D33). Se borran `B/Wms.Application/ForeignTrade/Common/Services/DispatchGuideBillingPlan.cs`, `DispatchGuideOrderData.PricesAsync` (`…/DispatchGuideOrderData.cs:36-46`) y `BillingRecipientModes.MultiClient` (`B/Wms.Application/Billing/Common/DTOs/BillingRecipientInput.cs`, y su comentario), con sus pruebas, después de comprobar con grep que nada más los usa.
- Nueva: `GetExitGuideChargeQuery` (C-F06-06) en `B/Wms.Application/Exits/Queries/`, con una regla pura `ExitGuideChargeRules` (un cliente, varios o ninguno); `IForeignTradeService` (`B/Wms.Application/ForeignTrade/Common/Services/IForeignTradeService.cs:15`) dice además si el precio salió del convenio o del precio general.
- `B/Wms.Api/Controllers/v1/ExitsController.cs`: `GET {id:guid}/guide/charge`.

### 3.3 Frontend

**FE-1:**
- **Contratos** (§2.3): `F/features/exits/contracts/exit.ts` (completo), `exit-charge.ts` y `guide.ts`.
- **Fuentes** (D26): `F/features/exits/services/exit.source.ts`, `guide.source.ts` y la fachada `catalog.source.ts`; simulados en `F/features/exits/mocks/` (`exit.mock.ts`, `guide.mock.ts`, `catalog.mock.ts`, `world.ts` con el estado que cambian las acciones y `data/` con las semillas), con las ayudas de `F/shared/mocks/`. Consultas en `F/features/exits/composables/exits.queries.ts` (prefijo `['exits']`; las mutaciones invalidan `['exits']` y `['foreign-trade']`).
- **Acciones:** `F/features/exits/composables/useExitActions.ts`: qué acciones tiene una salida o una guía según el rol y el estado, para las filas y el drawer (una sola fuente; D10, D11, D14).
- **Componentes:** `ExitListTable`, `GuideListTable`, `ExitMissingTags`, `ExitGoodsCell`, `ExitDetailDrawer`, `ExitDetail` (`F/features/exits/components/`).
- **Página:** `F/pages/foreign-trade/exits/index.vue` (`requiredRoles: [Admin, ForeignTrade]`).
- **Reglas puras:** `F/features/exits/utils/exit-display.ts` (rótulos de tipo, estado, falta y registro; resumen de la mercancía; firmante).
- **Fixtures de otras features:** `FT/fixtures/weighbridge/world.ts`, `FT/fixtures/weighbridge/registration.mock.ts` y `FT/unit/warehouse/mocks.spec.ts` con los campos nuevos de `exitSchema` (§2.3).

**FE-2:**
- **Páginas:** `F/pages/foreign-trade/exits/new.vue` y `F/pages/foreign-trade/exits/[id]/edit.vue` (`requiredRoles: [Admin, ForeignTrade]`).
- **Componentes:** `ExitForm` y sus secciones, `ExitConfirmDialog` (`F/features/exits/components/`); `VehicleQuickDialog` (`F/features/entries/components/`); `F/features/foreign-trade/components/DepositExitsStage.vue` (se rehace, D21) y su paso de datos desde `DepositStageDetail` (el depósito: Id, número, estado, modalidad y si tiene levante).
- **Reglas puras:** `F/features/exits/utils/exit-form.ts` (armar `exitUpsertSchema` desde el formulario, saldos y totales, tope de cada línea, vencimiento de la guía, lectura del archivo a base64).
- **Cobro sin «Clientes»** (D33): `F/components/app/AppChargeForm.vue` y `F/features/billing/contracts/billing-recipient.ts`, con sus pruebas y la galería `F/pages/dev/components.vue`.
- **Galería:** `F/pages/dev/components.vue` suma la sección «Etapa Salidas» con `DepositExitsStage` y datos simulados (R6).

**FE-3:**
- **Páginas:** `F/pages/warehouse/exits/index.vue` y `F/pages/warehouse/exits/history.vue` (`requiredRoles: [Admin, Warehouse]`).
- **Componentes:** `ExitLoadingDialog` y `YardExitDialog` (`F/features/exits/components/`).
- **Reglas puras:** `F/features/exits/utils/exit-loading.ts` («Cargar todo», total a despachar, porcentaje ubicado, si difiere de la guía).

**Guardias** (D30): las tres páginas de CE y las dos de Bodega entran a `MAQUETACION_PAGES` en su fase; I-06 la vacía.

### 3.4 Docs

- Este plan (§8 y §13.6), `D/planes/README.md` y la matriz `D/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md`, en cada cierre.
- Capturas de la maquetación en `D/planes/sprint-11/f06-salidas/evidencias/` (`fe1-*`, `fe2-*`, `fe3-*`).
- Casos QA con su resultado en `D/qa/casos-qa2-f06-salidas-AAAA-MM-DD.md` (I-06) y el hito de I-06 en `D/contexto/estado.md`.

---

## 4. Esquema y migraciones

**BE-1:** sin cambios de esquema. `has-pending-model-changes` debe salir limpio.

**BE-2: `RemoveExitCustomerOrderNumber`** (D9). Contenido esperado, en orden:
1. `goods_exits`: se quita la columna `customer_order_number` (`varchar(50)`, nula; creada por `ReplaceLoadingOrderWithGoodsExit`, `B/Wms.Infrastructure/Migrations/20261124122502_ReplaceLoadingOrderWithGoodsExit.cs:145`).
2. Nada más: `customer_order_issuer_id`, `customer_order_date` y `customer_order_file_url` se quedan (ya eran nulas). Sin índices ni semillas.

La genera y la aplica el agente con `dotnet ef` en la base local, en el mismo commit que el código (M6). El `Down` vuelve a crear la columna nula.

---

## 5. Pruebas

| Proyecto | Prueba (nueva o ajustada) | Escenario | Fase |
| --- | --- | --- | --- |
| `Wms.Tests` | `ExitLineBalancesTests` (nueva) | Saldos de la línea: Borrador (stock actual), Confirmada con guía (los de la guía), inspección (los del movimiento), dos líneas del mismo producto | BE-1 |
| `Wms.Tests` | `ExitWarehouseRecordTests` (nueva) | Registro de Bodega: cargue, salida de patio, ninguno; fecha y suma de lo cargado | BE-1 |
| `Wms.Tests` | `DepositStageRulesTests` (ajustada) | `Exits` en Confirmado con salida pendiente; solo `Exits` en Cerrado; nada en Anulado; sale al completarse | BE-1 |
| `Wms.IntegrationTests` | `ExitListReadsTests` (nueva) | C-F06-01: campos, filtros nuevos, orden por la fecha del registro, consultas de Bodega y errores de C-F01-00 | BE-1 |
| `Wms.IntegrationTests` | `ExitDetailReadsTests` (nueva) | C-F06-02: tipo de vehículo, cliente, saldos, ubicado (con `SOBRE-VEHICULO`) y guía | BE-1 |
| `Wms.IntegrationTests` | `EligibleDepositsTests` (nueva) | C-F06-07: estados, levante, reservas, `exceptExitId`, `modality`, `search`, cliente y bloqueo | BE-1 |
| `Wms.IntegrationTests` | `ExitGuidesEndpointTests` (nueva) | C-F06-08 y C-F06-09: vigente y anulada, filtros, orden, PDF por Id, 404 y 403 | BE-1 |
| `Wms.IntegrationTests` | `DepositExitStageTests` (nueva) | C-F06-10 en la lista y en el detalle | BE-1 |
| `Wms.Tests` | `ExitCustomerOrderRulesTests` (nueva) | Archivo: extensión, base64 inválido, tamaño; los tres vacíos = sin orden; conservar, quitar y reemplazar | BE-2 |
| `Wms.Tests` | `ExitGuideChargeRulesTests` (nueva) | Un cliente, varios, sin líneas | BE-2 |
| `Wms.Tests` | `DispatchGuideBillingPlanTests` | Se borra con la clase (D33) | BE-2 |
| `Wms.IntegrationTests` | `ExitCustomerOrderTests` (nueva) | C-F06-03 y C-F06-04 con soporte | BE-2 |
| `Wms.IntegrationTests` | `SingleRecipientGuideTests` (nueva; reemplaza a `MultiClientGuideTests`, que se borra) | C-F06-05 con dos clientes: un destinatario, mora de los dos, `multiClient` en 400 | BE-2 |
| `Wms.IntegrationTests` | `ExitGuideChargeTests` (nueva) | C-F06-06: convenio, general, varios clientes, errores y 403 | BE-2 |
| `Wms.IntegrationTests` | `GoodsExitFlowTests`, `OutputInitiationTests`, `ExportAndInspectionExitTests` (ajustadas en sus *helpers*) | La orden del cliente sin número; el flujo de F01 sigue en verde | BE-2 |
| Vitest | `FT/unit/exits/mocks.spec.ts` (nueva) | Cada dato simulado pasa su esquema (`PM/` §5.2) | FE-1 |
| Vitest | `FT/unit/exits/exit-display.spec.ts`, `FT/components/exits/ExitListTable.spec.ts`, `GuideListTable.spec.ts`, `ExitDetail.spec.ts`, `FT/unit/exits/useExitActions.spec.ts` (nuevas) | Rótulos, columnas, filtros, acciones por rol y estado, cancelada y anulada en la columna «Estado» con la fila en rojo tenue | FE-1 |
| Vitest | `FT/unit/exits/exit-form.spec.ts`, `FT/components/exits/ExitForm.spec.ts`, `ExitConfirmDialog.spec.ts`, `FT/components/entries/VehicleQuickDialog.spec.ts`, `FT/components/foreign-trade/DepositExitsStage.spec.ts` (nuevas); `AppChargeForm` y su galería (ajustadas) | Formulario por tipo, topes, vencimiento, soporte, confirmación con y sin cobro, etapa | FE-2 |
| Vitest | `FT/unit/exits/exit-loading.spec.ts`, `FT/components/exits/ExitLoadingDialog.spec.ts`, `YardExitDialog.spec.ts` (nuevas) | Cargar todo, topes, firma obligatoria, porcentaje ubicado, salida de patio | FE-3 |
| Vitest | Guardias de `FT/unit/guards/` | `list-pattern` y `mock-sources` con las rutas y fuentes de F06 | FE-1 a FE-3; I-06 |
| Vitest | Las pruebas de lo que se borra (`FT/components/billing/BillingCollectForm.spec.ts`, `FT/components/foreign-trade/LoadingOrderForm.spec.ts` y las demás de D31) | Se borran con su código | I-06 |

---

## 6. Casos QA

### 6.1 Parte 1 (API)

Por prueba de integración HTTP contra Postgres, en la fase que se indica.

| ID | Regla de origen | Precondición | Pasos | Resultado esperado | Verificación |
| --- | --- | --- | --- | --- | --- |
| QA2-F06-001 | AF-97; D7, D10 | Salida por depósito Confirmada, sin cargue ni pesaje | C-F06-01 | La fila trae `origin`, `modalityCode`, `observations`, `products` (una por línea) y `warehouseRecord` nulo | API (BE-1) |
| QA2-F06-002 | AF-64, AF-68; D17 | Salidas: Borrador; Confirmada por depósito sin cargue; Confirmada global sin salida de patio; Confirmada por depósito cargada sin pesaje; Completada | C-F06-01 con `status=Confirmed&missing=Loading,YardExit&sortField=confirmedAt&sortOrder=asc` | Solo las dos que esperan a Bodega, la más vieja primero | API (BE-1) |
| QA2-F06-003 | AF-64; D6, D20 | Las de 002 más una cancelada con cargue conservado | C-F06-01 con `attendedByWarehouse=true&sortField=warehouseRecordAt&sortOrder=desc` | Entran la cargada sin pesaje (`missing: [Weighing]`) y la Completada; no la cancelada ni las que no tienen registro; `warehouseRecord` con `kind`, `at`, `crewName` y `loadedQuantity` | API (BE-1) |
| QA2-F06-004 | AF-99; D7 | Salidas con tiquetes, productos y cuadrillas distintos | C-F06-01 con `ticketNumber`, `depositOrProduct`, `crew` y el rango de `warehouseRecordAt`; con `sortField=placa` y con `warehouseRecordAtFrom` > `To` | Filtran como dice la ficha; 400 con los mensajes de C-F01-00 | API (BE-1) |
| QA2-F06-005 | AF-97; D14 | Salida Confirmada con guía, vehículo con tipo y depósito con cliente | C-F06-02 | `vehicle.vehicleTypeName`, `deposits[].customerId`, `guide.departureAt`, `signerName` y `observations` | API (BE-1) |
| QA2-F06-006 | AF-36; D21 | Depósito con 760; salida A de 300 Confirmada; después salida B de 100 Confirmada; un Borrador C de 50; una de inspección Confirmada | C-F06-02 de A, B, C y la de inspección | A: 760 → 460 (de la guía, no cambia con B); B: 460 → 360; C: 360 → 310; inspección: los de su movimiento | API (BE-1) |
| QA2-F06-007 | AF-70; D18 | Línea de 300 con 200 ubicadas; otra con su producto en `SOBRE-VEHICULO` | C-F06-02 | `placedQuantity` 200 y la cantidad de la línea en la segunda | API (BE-1) |
| QA2-F06-008 | AF-89; D12 | Depósitos: Confirmado con stock; Borrador; Cerrado; importación sin levante; Confirmado con todo reservado por otra salida; uno sin cliente; uno con cliente bloqueado | C-F06-07 sin filtros; con `modality=Export`; con `search`; con `exceptExitId` de la salida que reserva; con `modality=Otra` | Salen el Confirmado, el sin cliente (`customerId` nulo) y el bloqueado (`exitsBlocked`); con `exceptExitId` vuelve el reservado; 400 con `modality` inválida | API (BE-1) |
| QA2-F06-009 | AF-97; D3, D11 | Salida con una guía anulada (reabierta) y otra vigente; otra salida con guía a crédito | C-F06-08 con `status`, `number`, `customer`, `paymentMode`; con un usuario de Bodega | Las dos guías de la salida, la anulada con fecha y motivo; productos de las líneas congeladas; orden por emisión; Bodega 403 | API (BE-1) |
| QA2-F06-010 | AF-97; D3 | Las guías de 009 | C-F06-09 de la vigente y de la anulada; de un Id inexistente; con Bodega | 200 `application/pdf` con `guia-{número}.pdf` (la anulada, con «ANULADA» en el texto del PDF); 404 «La guía no existe.»; 403 | API (BE-1) |
| QA2-F06-011 | AF-73; D5, D22 | Depósito con una salida Confirmada pendiente; el mismo cerrado por esa salida; otro anulado | C-F05-01 y C-F05-05 | `pendingStages` con `Exits` en Confirmado; en Cerrado solo `Exits`; al completar la salida, sin `Exits`; en Anulado, ninguna | API (BE-1) |
| QA2-F06-012 | AF-89; D9 | Agencia y PDF de prueba | C-F06-03 con emisor, fecha y soporte; C-F06-02 | 201; `customerOrder` sin `number`, con `fileUrl`; el archivo existe en el almacenamiento | API (BE-2) |
| QA2-F06-013 | AF-89; D9 | — | C-F06-03 con emisor que no es agencia ni importador; fecha futura; archivo `.txt`; base64 inválido; archivo de 11 MB | 400 con cada mensaje de la ficha | API (BE-2) |
| QA2-F06-014 | AF-89; D9 | Borrador con soporte | C-F06-04 con `keepCurrentFile: true`; con `false`; con un archivo nuevo; sobre una Confirmada | Conserva; quita; reemplaza; 409 «La salida {N} no está en Borrador: anule la guía para corregirla.» | API (BE-2) |
| QA2-F06-015 | AF-106; D33 | Consolidada con depósitos de dos clientes, los dos con cliente | C-F06-05 con `registered` y el `customerId` de uno; con uno de los dos en mora | Una sola factura de la guía, a ese tercero; la guía emitida; con mora, el error de hoy y nada cambia | API (BE-2) |
| QA2-F06-016 | AF-106; D33 | La consolidada de 015 | C-F06-05 con `multiClient` | 400 «El destinatario de facturación 'multiClient' no es válido para este servicio.»; no aparece el mensaje de «Clientes» | API (BE-2) |
| QA2-F06-017 | AF-88, AF-106 | Consolidada de dos clientes; una de inspección | C-F06-05 con `unregistered`; con `finalConsumer`; la de inspección con `billing: null` | 200 las tres; la de inspección sin guía ni cobro | API (BE-2) |
| QA2-F06-018 | AF-106; D4 | Cliente con convenio de guía; otro sin convenio | C-F06-06 de una salida de cada uno, de una de los dos y de un Borrador sin líneas | `Agreement` con el precio del convenio; `General` en los demás; `customerId` nulo con dos clientes o sin líneas; `totalAmount` con el IVA | API (BE-2) |
| QA2-F06-019 | D4 | Salida Confirmada; de inspección; Id inexistente | C-F06-06; con un usuario de Bodega | 409 y 409 con los mensajes de la ficha; 404; 403 | API (BE-2) |
| QA2-F06-020 | `P01/` §2.2.4; R1 | Suite de F01 | `GoodsExitFlowTests`, `OutputInitiationTests` y C-F01-101 | En verde; la búsqueda por placa trae los campos de C-F06-02 | API (BE-2) |

### 6.2 Integración I-06 (navegador)

En el navegador, contra el backend local de `f2/f06-salidas` y sin la sesión simulada, con usuarios de prueba por rol (CE, Bodega, Báscula, Vigilancia y Admin; sus contraseñas no se copian). Para el reloj, umbrales temporales de 1 y 2 minutos que se restauran al terminar.

| ID | Regla de origen | Precondición | Pasos | Resultado esperado | Verificación |
| --- | --- | --- | --- | --- | --- |
| QA2-F06-031 | AF-64, AF-97, AF-127; D28, D29 | Usuarios CE, Bodega y Admin | Abrir el menú con cada uno; Alt+O; los tableros de CE y Bodega | CE: «Salidas»; Bodega: «Salidas ▸ Órdenes de salida, Historial» después de «Entradas»; nadie ve «Órdenes de cargue» ni «Guías de salida»; Alt+O abre Salidas; las tarjetas nuevas llevan a sus listas | Pantalla (I-06 (2)) |
| QA2-F06-032 | AF-97, AF-99; D10 | Salidas en todos los estados, una creada en Báscula y una cancelada | Salidas de CE: filtros, orden, «Falta», exportar | Columnas y filtros de D10; «Completar (creada en báscula)»; reloj en Confirmada; la cancelada con «Cancelada» en la columna «Estado» (fecha y motivo en el tooltip) y la fila en rojo tenue; «Exportar» con todo | Pantalla (I-06 (1)) |
| QA2-F06-033 | AF-89, AF-28, AF-54; D9, D12 | Depósito de importación confirmado con levante y cliente | «+ Nueva salida» por número de depósito: depósito, cantidad, vehículo nuevo con «+», conductor con «+», ciudad, orden del cliente con emisor, fecha y PDF; «Guardar borrador» | Borrador `2026SM…`; vencimiento según la ciudad; soporte visible; otra salida del mismo depósito ve menos disponible (reserva, M24) | Pantalla (I-06 (1)) |
| QA2-F06-034 | AF-32; D12 | Dos depósitos de importación y uno de exportación | Agregar un segundo depósito | Solo ofrece los de importación; aparece «Consolidada»; las líneas de los dos | Pantalla (I-06 (1)) |
| QA2-F06-035 | AF-36, AF-68, AF-106, AF-132; D4, D13 | El Borrador de 033 | «Confirmar y emitir guía»: fecha, observaciones, total sugerido (editarlo), tercero precargado; «Pendiente por facturar»; otra vez con «Pago inmediato» y transferencia | Guía `2026S…` emitida; el stock baja; firmante el conductor; la referencia solo con otro método; si la salida se lleva todo, el depósito queda Cerrado y su etapa Salidas marcada en la lista | Pantalla (I-06 (1)) |
| QA2-F06-036 | AF-75; C-F05-21 | Depósito sin cliente; otro con el cliente bloqueado | Crear la salida (el formulario los marca) y confirmar | El icono junto al depósito; al confirmar, 409 «Asigne el cliente…» y 400 de salidas bloqueadas, en el modal; nada cambia | Pantalla (I-06 (1)) |
| QA2-F06-037 | AF-29, AF-33; D12 | Depósito con dos tiquetes de camiones que no descargaron | Salida global con los dos; otra por tiquete con uno de ellos | Líneas precargadas con lo declarado; el tiquete en otra salida, deshabilitado con su icono; al confirmar, firma el importador (global); el drawer dice «No pasa por báscula» | Pantalla (I-06 (1)) |
| QA2-F06-038 | AF-88; D13 | Depósito de inspección confirmado con cliente | Nueva salida y «Confirmar salida» | Sin cobro ni guía; el stock baja; en Órdenes de salida, «Sin guía · inspección» | Pantalla (I-06 (1)) |
| QA2-F06-039 | AF-37, AF-34; D12 | Borrador creado en Báscula (placa, conductor y transportadora) | «Editar»: tipo, depósito y líneas; reemplazar y luego quitar el soporte | Se completa y conserva la transportadora; el soporte se reemplaza y se quita | Pantalla (I-06 (1)) |
| QA2-F06-040 | AF-97, AF-42; D14 | Salida completada con cargue, pesaje y una guía anulada | Abrir el drawer desde Salidas, desde la etapa y desde Bodega | Secciones de D14 con sus datos; acciones de CE en CE y de Bodega en Bodega; «Ver soporte» | Pantalla (I-06 (1)) |
| QA2-F06-041 | AF-90; D15 | Salida Confirmada con guía; otra de inspección; un Borrador | Anular guía con motivo; volver a confirmar; reabrir la de inspección; cancelar el Borrador | Borrador con el stock devuelto y la guía en «Guías anuladas»; guía nueva al reconfirmar; la de inspección en Borrador; el Borrador, Cancelado | Pantalla (I-06 (1)) |
| QA2-F06-042 | AF-97; D3, D11, D16 | Guías vigentes y anuladas, una consolidada y una a crédito | Pestaña «Guías»: filtros; PDF de una anulada y de una vigente; ZIP; cambiar a «Pago inmediato»; exportar | La anulada con «Anulada» en la columna «Estado» (fecha y motivo en el tooltip) y la fila en rojo tenue; su PDF con «ANULADA»; el ZIP solo en la consolidada; cambiar el modo pide el método; el Excel con las columnas de D11 | Pantalla (I-06 (1)) |
| QA2-F06-043 | AF-42, AF-90, AF-96; D21 | Depósito con una salida por depósito y una consolidada pesadas | Etapa Salidas: expandir, «Descargar guía», «Nueva salida» | Saldos de cada línea; el peso de la consolidada es la parte del depósito; «Nueva salida» abre con el depósito y vuelve a la etapa; en un depósito en Borrador, el botón deshabilitado con su tooltip | Pantalla (I-06 (1)) |
| QA2-F06-044 | AF-57, AF-64, AF-68; D17 | Salidas Confirmadas de los cuatro tipos, umbrales de 1 y 2 minutos | Órdenes de salida con Bodega: columnas, filtros, colores | Solo las Confirmadas pendientes; «Falta»; el reloj cambia de color a los 1 y 2 minutos; acción según el tipo | Pantalla (I-06 (2)) |
| QA2-F06-045 | AF-70, `DEC-052`, `DEC-056`; D18 | Salida por depósito con guía y lo ubicado parcial | «Ejecutar salida»: «Cargar todo», bajar una cantidad, firma y foto | El aviso de la guía y el porcentaje ubicado; sin firma no deja; al ejecutar, aviso de diferencia y la notificación a CE; las ubicaciones liberadas; sale de Órdenes de salida; sin guía vigente no se ejecuta | Pantalla (I-06 (2)) |
| QA2-F06-046 | AF-66, AF-67; D19 | La global de 037 confirmada | «Registrar salida de patio» con observación | La salida queda Completada; sale de Órdenes de salida y entra al Historial | Pantalla (I-06 (2)) |
| QA2-F06-047 | AF-64; D6, D20 | La de 045 (sin pesaje) y la de 046 | Historial de Bodega: filtros y «Ver» | Las dos; la de 045 con «Confirmada · falta pesaje»; el registro, la cuadrilla y la fecha | Pantalla (I-06 (2)) |
| QA2-F06-048 | AF-30, AF-31, AF-34; R1 | La de 045 cargada | Báscula: salida del camión por placa y pesaje | La salida se precarga (C-F01-101 pasa su esquema); al completar el pesaje, la salida queda Completada | Pantalla (I-06 (2)) |
| QA2-F06-049 | D30, D31, D33 | — | Abrir las rutas viejas; buscar en el código | 404 de las páginas viejas; sin `BillingCollectForm` ni «Clientes» en el cobro; guardias en verde | Pantalla y código (I-06 (2)) |
| QA2-F06-050 | Flujo completo (`PM/` §4): AF-30, AF-31, AF-36; `DEC-056` | Base local recreada con los catálogos, tarifas de báscula y de guía, y un cliente | **Por número de depósito:** Vigilancia registra el ingreso → Báscula registra la entrada con su cobro → Bodega recibe → CE confirma el depósito y registra el levante → CE crea la salida y la confirma con su guía y su cobro → Bodega ejecuta el cargue → Báscula pesa la salida y cobra → Vigilancia registra la salida del camión | Cada paso sin errores; la salida queda Completada; el depósito con su saldo, peso despachado y la etapa Salidas al día; las facturas de báscula y de guía en Facturación | Pantalla (I-06 (2)) |
| QA2-F06-051 | Flujo completo: AF-29, AF-33, AF-66, AF-67 | La base de 050 | **Por tiquete:** Vigilancia y Báscula registran un camión que no descarga → CE confirma el depósito (y el levante, en importación) → CE crea la salida por tiquete y la confirma con su guía y su cobro → Bodega registra la salida de patio → Vigilancia registra la salida | La salida queda Completada sin pasar por la báscula de salida; un cobro de guía; el depósito al día | Pantalla (I-06 (2)) |

---

## 7. Transición de datos

- **Órdenes de cargue abiertas** (M18, `PM/` §7.2): no aplica en F06. F01 retiró la orden de cargue sin convertir nada, y staging se recrea en el despliegue final (M17, M25).
- **Número de la orden del cliente** (D9): la migración borra la columna; las bases locales se recrean (`DEC-006`) y en staging no hay salidas hasta el despliegue final.
- **Importador del legacy:** no trae salidas ni guías (`B/Wms.Domain/Enums/LegacyImportEntity.cs:7-20`); no cambia.

---

## 8. Fases por parte

La parte 1 (backend) y la parte 2 (maquetación) corren en paralelo, una por repo (M10), y cierran por separado. Cada fase cierra con las compuertas de `PM/` §6.1 o §6.2, sus casos QA, commit y push de `f2/f06-salidas`, el estado aquí y en la matriz, y el reporte (una fase por turno, `PM/` §6). Las cifras de la base las toma cada parte al crear su rama, porque después de I-05 llegaron a `fase-2` los ajustes de la QA de F05, el formato numérico (`DEC-082`), los formatos v2 de PDF y el aviso junto a un dato en F01 a F04 (§1.9); como referencia, I-05 (2) cerró con `Wms.Tests` 2348, `Wms.IntegrationTests` 879, `yarn test` 785 pruebas en 146 archivos y `yarn lint` 142 errores (`P05/` §13.6).

| Fase | Parte | Contenido | Criterio de salida | Estado |
| --- | --- | --- | --- | --- |
| BE-1 | 1 | Lecturas: listado y detalle ampliados, depósitos elegibles, guías y su PDF, etapa Salidas (§8.1) | QA2-F06-001 a 011 en PASA por API | Hecha el 2026-11-27 (BE `8ff47be`) |
| BE-2 | 1 | Escrituras y cobro: orden del cliente con soporte y la migración, confirmar sin «Clientes», cobro sugerido (§8.2) | QA2-F06-012 a 020 en PASA por API | Hecha el 2026-11-27 (BE `f0b9007`) |
| FE-1 | 2 | Contratos, fuentes, drawer y Salidas de CE con sus dos pestañas (§8.3) | P-CE-11 (listado y guías) y el drawer con su lista del wireframe y captura | Hecha el 2026-11-27 (FE `2c5540b`) |
| FE-2 | 2 | «Nueva salida» y «Editar», confirmación con el cobro y la etapa Salidas (§8.4) | P-CE-11 (formulario y confirmación) y P-CE-08 con su lista y captura | Hecha el 2026-11-27 (FE `a2cac51`) |
| FE-3 | 2 | Bodega: Órdenes de salida, Ejecutar salida, Salida de patio e Historial (§8.5) | P-BOD-06 a P-BOD-09 con su lista y captura | Pendiente |
| Revisión | — | Revisión del usuario con la sesión simulada (§8.6) | Visto bueno del usuario o plan de ajustes | Pendiente |
| I-06 (1) | 3 | Fuentes http, Comercio Exterior y sus casos (§13) | QA2-F06-032 a 043 en PASA | Pendiente |
| I-06 (2) | 3 | Bodega, menú, atajos, tableros, borrados, guardias, flujo completo y fusión (§13) | QA2-F06-031 y 044 a 051 en PASA; fusión en `fase-2` | Pendiente |

### 8.1 Backend, fase 1 — Lecturas

- **Decisiones:** D3, D5, D6, D7, D22, D34.
- **Endpoints:** C-F06-01, C-F06-02 (sin la orden del cliente, que es de BE-2), C-F06-07, C-F06-08, C-F06-09 y C-F06-10 (fichas §2.2, grupo A; esquemas de §2.3).
- **Archivos:** §3.2, «BE-1». **Migración:** ninguna.
- **Pruebas:** `ExitLineBalancesTests`, `ExitWarehouseRecordTests`, `DepositStageRulesTests` (ajustada), `ExitListReadsTests`, `ExitDetailReadsTests`, `EligibleDepositsTests`, `ExitGuidesEndpointTests`, `DepositExitStageTests` (§5).
- **Casos QA:** QA2-F06-001 a 011.
- **Notas:** las rutas `exits/eligible-deposits` y `exits/guides` no chocan con `exits/{id:guid}` (restricción de tipo). El orden por `warehouseRecordAt` usa la fecha del cargue o, si no hay, la de la salida de patio, con las salidas sin registro al final. `products` sale de las líneas de la salida, no de la guía. La lectura por placa (C-F01-101) devuelve los campos nuevos sin cambio de código propio.
- **Estado:** hecha el 2026-11-27 (BE `8ff47be`, rama `f2/f06-salidas` desde `fase-2` `996828e`). QA2-F06-001 a 011 en PASA por API (`ExitListReadsTests`, `ExitDetailReadsTests`, `EligibleDepositsTests`, `ExitGuidesEndpointTests`, `DepositExitStageTests`). Compuertas: `dotnet build Wms.sln` sin errores; `Wms.Tests` 2475 → 2501 y `Wms.IntegrationTests` 893 → 901, todas en verde; sin migración y `has-pending-model-changes` limpio. Reglas puras nuevas: `ExitLineBalances` y `ExitWarehouseRecord`; `DepositStageRules` con la etapa Salidas (`DepositStageInput.HasPendingExit`). Contrato sin cambios. Notas para FE e I-06:
  - `vehicle.vehicleTypeName` es el rótulo del catálogo de C-F04-17 (p. ej. «Doble-Troque»; `VehicleTypeCatalog.LabelOf`), o el valor guardado si no es del catálogo.
  - `placedQuantity` sale de lo ubicado del **producto** (con `SOBRE-VEHICULO`): las ubicaciones no distinguen unidad de carga, así que una línea con unidad de carga informa lo ubicado de su producto, con tope su cantidad (lo mismo que libera el cargue, LIFO por producto).
  - Saldos (C-F06-02): en Confirmada o Completada sin línea de guía ni movimiento (no debería pasar) se usa la regla de Borrador. En inspección se toma el último `Out` de la salida por producto (una reapertura anterior queda antes).
  - `attendedByWarehouse=false` devuelve el complemento (sin registro o canceladas); el contrato solo usa `true`.
  - C-F06-07 calcula lo disponible en memoria sobre los depósitos Confirmados de CE antes de paginar; `availableQuantity` es la suma por producto, en importación el menor entre disponible y nacionalizado disponible de cada producto. `documentLabel` = «{tipo de documento} {número}» o, sin número, la descripción de la inspección.
  - Los filtros de texto nuevos ignoran mayúsculas; producto, cuadrilla, cliente e importador también ignoran tildes (`unaccent`).
  - La marca «ANULADA» del PDF (C-F06-09) se verificó con el formato vigente (LEGACY, D37) por la matriz de giro de 30° de la marca en el contenido del PDF, porque el texto va en glifos.
  - *Helpers* nuevos en `B/Wms.IntegrationTests/ForeignTrade/ImportExitScenario.cs` para BE-2 e I-06: `SeedExitDepositAsync` (el antiguo `DepositAsync` de `GoodsExitFlowTests`, que ahora lo llama), `SeedTicketDepositAsync`, `CreateTicketExitAsync`, `SeedTicketExitAsync`; `ConfirmExitAsync` acepta `observations` y `LoadExitAsync`, `crewId`.

### 8.2 Backend, fase 2 — Escrituras y cobro

- **Decisiones:** D4, D9, D33.
- **Endpoints:** C-F06-02 (la orden del cliente), C-F06-03, C-F06-04, C-F06-05 y C-F06-06 (fichas §2.2, grupo B).
- **Archivos:** §3.2, «BE-2». **Migración:** `RemoveExitCustomerOrderNumber` (§4).
- **Pruebas:** `ExitCustomerOrderRulesTests`, `ExitGuideChargeRulesTests`, `ExitCustomerOrderTests`, `SingleRecipientGuideTests`, `ExitGuideChargeTests`; se borran `DispatchGuideBillingPlanTests` y `MultiClientGuideTests`; se ajustan los *helpers* de `GoodsExitFlowTests`, `OutputInitiationTests` y `ExportAndInspectionExitTests` (§5).
- **Casos QA:** QA2-F06-012 a 020.
- **Notas:** el soporte usa el mismo servicio de almacenamiento y las mismas validaciones de archivo que la orden externa de hoy (`develop` `CreateLoadingOrderCommandHandler.cs:442-480`), con los mensajes de C-F06-03. Antes de borrar lo de «Clientes», `grep -rn "MultiClient\|DispatchGuideBillingPlan\|PricesAsync"` fuera de lo que se borra debe salir vacío.
- **Estado:** hecha el 2026-11-27 (BE `f0b9007`, rama `f2/f06-salidas` sobre BE-1 `8ff47be`; `fase-2` sin cambios desde `996828e`). QA2-F06-012 a 020 en PASA por API (`ExitCustomerOrderTests`, `SingleRecipientGuideTests`, `ExitGuideChargeTests`, `GoodsExitFlowTests` con la búsqueda por placa, `OutputInitiationTests`, `ExportAndInspectionExitTests`). Compuertas: `dotnet build Wms.sln` sin errores; `Wms.Tests` 2501 → 2533 y `Wms.IntegrationTests` 901 → 912, todas en verde; migración `RemoveExitCustomerOrderNumber` generada y aplicada en local con `dotnet ef` (solo quita `customer_order_number`, §4) y `has-pending-model-changes` limpio. Reglas puras nuevas: `ExitCustomerOrderRules` y `ExitGuideChargeRules`. Borrados por D33, con el grep limpio: `DispatchGuideBillingPlan` (`GuideOwnerDeposits` pasa a `DispatchGuideOrderData.cs`), `DispatchGuideOrderData.PricesAsync`, `BillingRecipientModes.MultiClient`, `DispatchGuideBillingPlanTests` y `MultiClientGuideTests`. Contrato sin cambios. Notas para FE e I-06:
  - `customerOrder` nulo en `PUT` quita la orden entera (y su soporte). Con los tres campos vacíos (`issuerId`, `date`, `file`) y `keepCurrentFile: true`, el soporte que ya tenía se conserva y la orden queda solo con él; al crear, `keepCurrentFile` se ignora. Un archivo nuevo o «quitar» borra el soporte anterior del almacenamiento después de guardar.
  - El tipo del soporte se valida por la extensión del nombre y por `contentType` (los dos deben ser PDF, JPG o PNG); acepta el prefijo `data:…;base64,`. `fileUrl` es la ruta del almacenamiento (`/uploads/exit-customer-orders/…` en local).
  - C-F06-05 valida el destinatario antes que la mora: con `multiClient` responde el 400 del cobro sin escribir nada. La mora se valida para cada cliente dueño y, con `registered`, también para el tercero elegido.
  - C-F06-06: con un solo cliente sin convenio devuelve ese `customerId` con `priceSource: General` (para precargarlo); `customerId` es nulo con varios clientes, con algún depósito sin cliente o sin líneas. `taxAmount` = tarifa × tasa, redondeado a 2 decimales.
  - Defecto corregido de paso (bloqueante para reemplazar o quitar el soporte): `StorageService.GetFileAsync` y `DeleteFileAsync` fallaban siempre sin `Storage:Local:BaseUrl` (`string.Replace` con un valor vacío). Nadie más los usaba.
  - `GuidePaymentModeChangeTests` creaba sus guías con «Clientes»: ahora con un destinatario (una factura). Su prueba de la factura consolidada se borró, porque la emisión ya no crea líneas de guía en una consolidada; el código de C-F01-108 que mueve esa línea sigue igual (solo lo alcanzarían datos anteriores).

### 8.3 Maquetación, fase 1 — Contratos, fuentes, drawer y Salidas de CE

- **Decisiones:** D1, D3, D10, D11, D14, D15, D16, D23 a D27, D30.
- **Contratos:** todos los de §2.3 (también los de FE-2 y FE-3, para que una sola fase fije la forma; `billing-recipient.ts` cambia en FE-2), con sus datos simulados y `FT/unit/exits/mocks.spec.ts`. Los fixtures de Báscula y Bodega que arman una `Exit` suman los campos nuevos (§2.3).
- **Fuentes:** `exit.source.ts`, `guide.source.ts` y la fachada `catalog.source.ts` (D26), con sus simulados. Semillas, como los wireframes: `2026SM00039` por depósito Completada; `2026SM00040` por depósito Confirmada (falta cargue y pesaje, 20 min); `2026SM00041` consolidada Confirmada (falta cargue, amarillo); `2026SM00042` global Confirmada (falta salida de patio); `2026SM00043` Borrador creado en Báscula; una de inspección Confirmada sin guía; una por depósito cargada que espera el pesaje; una cancelada; y guías vigentes y anuladas (una a crédito y una de una consolidada). Datos ficticios, sin personas reales (`DEC-007`).
- **Pantalla:** P-CE-11 (`F/pages/foreign-trade/exits/index.vue`), pestañas «Salidas» y «Guías», con el drawer. Cumple su lista del wireframe (`D/levantamiento-2026-11/fase_2-mockups/comercio-exterior.html`, P-CE-11; `A/` §2.3 g) y se captura en `D/planes/sprint-11/f06-salidas/evidencias/fe1-*`.
- **Componentes:** `ExitListTable`, `GuideListTable`, `ExitMissingTags`, `ExitGoodsCell`, `ExitDetailDrawer`, `ExitDetail`; `useExitActions`; `exit-display.ts` con sus pruebas.
- **Guardias:** la página entra a `MAQUETACION_PAGES`. **Sin llamadas reales y sin menú** (`PM/` §6.2); la sesión simulada de `P02/` D10 (`NUXT_PUBLIC_MOCK_SESSION=true`, `?roles=Admin,ForeignTrade`).
- **Lista del wireframe:** columnas, filtros y acciones de D10 y D11; «+ Nueva salida» lleva a `/foreign-trade/exits/new` (la página llega en FE-2: hasta entonces, un aviso); el drawer de D14 con sus acciones por rol.
- **Estado:** hecha el 2026-11-27 (FE `2c5540b`, rama `f2/f06-salidas` desde `fase-2` `8884936`).
  - **Cifras:** `yarn test` 812 → 868 pruebas en verde (151 → 157 archivos; el error no manejado de `WeighbridgeQueuePage.spec.ts` ya estaba en la base), `yarn lint` 142 → 142 errores (sin contar el worktree viejo `.claude/worktrees/ui-alert-icon-0ac35c`, que suma 213) y cero en los archivos nuevos, `yarn build` con código 0, guardias de `FT/unit/guards/` en verde. Los simulados pasan sus esquemas (`FT/unit/exits/mocks.spec.ts`).
  - **Hecho:** contratos de §2.3 completos (`exit.ts`, `exit-charge.ts`, `guide.ts`) y `contracts/catalog.ts` con lo integrado que reexporta la fachada; fuentes `exit.source.ts` (todas las operaciones de D26, también las de FE-2 y FE-3), `guide.source.ts` y `catalog.source.ts` con sus simulados y las semillas de esta sección; `exits.queries.ts`, `useExitActions.ts` (acciones por rol, estado y contexto `foreign-trade` o `warehouse`, y su ejecución), `exit-display.ts`; `ExitListTable`, `GuideListTable`, `ExitMissingTags`, `ExitGoodsCell`, `ExitDetailDrawer` y `ExitDetail`; la página `/foreign-trade/exits` en `MAQUETACION_PAGES`, sin menú. Fixtures de Báscula y la prueba de Bodega con los campos nuevos de `exitSchema`.
  - **Lista del wireframe (P-CE-11 y drawer):** columnas, filtros y orden de D10 y D11; la cancelada y la anulada en «Estado» con fecha y motivo en el tooltip y la fila en rojo tenue, también en tema oscuro (D35); acciones en el menú ⋮ por estado; «Salida» de la pestaña «Guías» abre el drawer; drawer con las secciones y el menú de D14; Anular guía, Reabrir y Cancelar con `ReasonDialog` (D15) y Cambiar modo de pago con el método (D16); descargas de la guía, de la guía por Id y del ZIP. Capturas en `D/planes/sprint-11/f06-salidas/evidencias/fe1-01` a `fe1-13`.
  - **Notas para FE-2, FE-3 e I-06:**
    - La fila de C-F06-01 no trae la fecha ni el motivo de la cancelación que piden D10 y D35: el tooltip los lee del detalle (C-F06-02) de las canceladas de la página (`useQueries` en `ExitListTable`), sin cambiar el contrato (`DEC-002`). Si se prefiere sumar `cancelledAt` y `cancellationReason` a la fila, es un cambio de contrato que se pregunta al usuario.
    - «+ Nueva salida» y «Editar» muestran un aviso mientras `FORM_PAGES_READY` sea `false` en la página; FE-2 lo pasa a `true`.
    - Los filtros de tipo, estado, modo de pago y estado de la guía eligen un valor (el `Select` de `AppDataTable`); el contrato admite varios.
    - La sección Guía dice «Emitida» o «Sin factura» y la Mercancía muestra «Asignada» en la unidad de carga: el contrato no trae el número de la factura ni el identificador de la unidad de la línea.
    - Para ver la maquetación: `NUXT_PUBLIC_MOCK_SESSION=true yarn dev` y `/foreign-trade/exits?roles=ForeignTrade` (o `?roles=Admin,ForeignTrade`).

### 8.4 Maquetación, fase 2 — «Nueva salida», «Editar», confirmación y etapa Salidas

- **Decisiones:** D1, D4, D9, D12, D13, D21, D25, D33.
- **Pantallas:** «Nueva salida» y «Editar» (`F/pages/foreign-trade/exits/new.vue`, `[id]/edit.vue`) con `ExitConfirmDialog`; P-CE-08 (`DepositExitsStage`). Cumplen su lista del wireframe (P-CE-11 «Nueva salida» y P-CE-08) y se capturan en `evidencias/fe2-*`.
- **Componentes:** `ExitForm` y sus secciones, `ExitConfirmDialog`, `VehicleQuickDialog`, `DepositExitsStage`; `exit-form.ts` con sus pruebas.
- **Cobro sin «Clientes»** (D33): `AppChargeForm` y `billing-recipient.ts`, con sus pruebas y la galería; Báscula y Montacargas no usan `allowMultiClient`, así que no cambian.
- **Etapa Salidas en la galería** (R6): el detalle del depósito ya usa el API real (I-05), así que P-CE-08 se revisa en `/dev/components` (sección «Etapa Salidas», con un depósito simulado de cada estado). El detalle real pasa a `DepositExitsStage` el depósito que necesita (D21).
- **Guardias:** las dos páginas entran a `MAQUETACION_PAGES`.
- **Lista del wireframe:** las ocho secciones de D12 con sus reglas y avisos; «Guardar borrador» y «Confirmar y emitir guía» en la barra; el modal de D13 con y sin cobro; la etapa de D21 con la fila expandida, el peso por depósito y «Nueva salida».
- **Estado:** hecha el 2026-11-27 (FE `a2cac51`, rama `f2/f06-salidas` sobre FE-1 `2c5540b`; `fase-2` sin cambios desde `8884936`).
  - **Cifras:** `yarn test` 868 → 904 pruebas en verde (157 → 163 archivos; el error no manejado de `WeighbridgeQueuePage.spec.ts` ya estaba en la base), `yarn lint` 142 → 142 errores (sin el worktree viejo `.claude/worktrees/ui-alert-icon-0ac35c`) y cero en los archivos nuevos, `yarn build` con código 0 antes y después, guardias de `FT/unit/guards/` en verde. Los simulados siguen pasando sus esquemas (`FT/unit/exits/mocks.spec.ts`).
  - **Hecho:** páginas `/foreign-trade/exits/new` (`?deposito=`, `?volver=`) y `/foreign-trade/exits/[id]/edit` con `ExitForm` y sus secciones (`ExitDepositsSection`, `ExitTicketsSection`, `ExitLinesSection`, `ExitTransportSection`, `ExitCustomerOrderSection`; Tipo, Destino y Observaciones en `ExitForm`), `ExitConfirmDialog` y `VehicleQuickDialog`; reglas puras `exit-form.ts`; consultas y mutaciones nuevas en `exits.queries.ts` (stock disponible, tiquetes, cobro sugerido, crear, guardar y confirmar). `DepositExitsStage` rehecha (D21) y conectada a `DepositStageDetail` (el depósito: Id, número, estado, modalidad y si tiene levante; tipo `DepositExitsStageDeposit` en `deposit-stages.ts`). D33: `AppChargeForm` sin `allowMultiClient` ni «Clientes» y `billingRecipientInputSchema` sin `multiClient`, con sus pruebas; `F/features/weighbridge/utils/charge-step.ts` pierde la rama muerta `recipientMode === "multiClient"` (el tipo ya no la admite; Báscula no cambia de comportamiento). Galería: nota de D33 y la sección «P-CE-08 · Etapa Salidas del depósito (F06)» con seis depósitos simulados. `MAQUETACION_PAGES` suma las dos páginas y los tres detalles del depósito (D30). En `/foreign-trade/exits` salió `FORM_PAGES_READY`: «+ Nueva salida» y «Editar» navegan. Pruebas nuevas: `FT/unit/exits/exit-form.spec.ts`, `FT/components/exits/ExitForm.spec.ts`, `ExitConfirmDialog.spec.ts`, `FT/components/entries/VehicleQuickDialog.spec.ts`, `FT/components/foreign-trade/DepositExitsStage.spec.ts` y `FT/components/dev/ComponentsGallery.spec.ts`; `FT/unit/components/AppChargeForm.spec.ts` ajustada.
  - **Lista del wireframe:** sin tarjeta de título, `<h1 class="sr-only">` y la barra «Volver», «Guardar borrador» y «Confirmar y emitir guía» («Confirmar salida» en inspección) arriba a la derecha; las ocho secciones de D12 con la tarjeta de registro: tipo con «Consolidada»; depósitos de C-F06-07 con la línea secundaria, la modalidad del primero, uno solo en tiquete y global, «Quitar» y los avisos de cliente sin asignar o salidas bloqueadas; tiquetes con el que está en otra salida deshabilitado y su aviso, precarga de líneas (con tope) y del vehículo de la placa; mercancía con nacionalizado (solo importación), disponible, saldo anterior, cantidad con tope y nuevo saldo, con el total; transporte con los tres «+»; destino con «Vence el»; orden del cliente sin número con emisor, fecha no futura y soporte («Adjuntar», «Quitar», «Ver soporte»); observaciones. El Borrador de Báscula abre con placa, conductor y transportadora y avisa lo que falta. El modal de D13 con el resumen, fecha (no antes de ayer), observaciones, firmante, vencimiento y el cobro de C-F06-06 («Precio del convenio de…» o «Precio general»), y en inspección sin guía ni cobro; los errores en el modal; al confirmar, el aviso y el drawer o `?volver=`. La etapa de D21 con su tabla, la fila expandida, el peso por depósito de la consolidada, las acciones y «Nueva salida» deshabilitado con su motivo. Capturas en `D/planes/sprint-11/f06-salidas/evidencias/fe2-01` a `fe2-14`.
  - **Notas para FE-3, la revisión e I-06:**
    - El stepper y el encabezado de la tarjeta de la etapa Salidas siguen fijos por F05 (`F/features/foreign-trade/utils/deposit-stages.ts`: `stageTone` da `idle` y `stageCaption` «Con la próxima actualización» para `Exits`, y `stageProgress` no la cuenta), aunque D22 dice que la pantalla de F05 «pinta lo que llega». FE-2 no lo cambió (no es de su fase y el texto y el tono no están decididos): queda como pregunta para el usuario antes de I-06.
    - En el detalle real, la etapa lee la fuente simulada con el Id real del depósito: sale vacía hasta I-06 (R6).
    - El emisor de la orden se busca con `businessRolCode=CUSTOMS_AGENCY,IMPORTER` en la fachada simulada; el API compara un solo código (`B/Wms.Application/Stakeholders/Queries/GetStakeholders/GetStakeholdersHandler.cs:63`): I-06 hace dos búsquedas y las une, o se pregunta un cambio de contrato.
    - La fachada no tiene lectura por Id de vehículos, conductores ni ciudades: los selectores la resuelven con `all: true`; I-06 usa las fuentes integradas.
    - «Guardar borrador» vuelve a `?volver=` o a `/foreign-trade/exits?id={id}`; si «Confirmar» guarda y el modal se cierra sin confirmar, el formulario sigue sobre la salida guardada (no crea otra).
    - Ver la maquetación: `NUXT_PUBLIC_MOCK_SESSION=true yarn dev`, `/foreign-trade/exits/new?roles=Admin,ForeignTrade`, `/foreign-trade/exits/new?deposito=e9000000-0000-4000-8000-00000000000a`, `/foreign-trade/exits/e6000000-0000-4000-8000-00000000002b/edit` (Borrador de Báscula) y `/dev/components` (sección «Etapa Salidas»).

### 8.5 Maquetación, fase 3 — Bodega

- **Decisiones:** D2, D17 a D20, D23.
- **Pantallas:** P-BOD-06 (`F/pages/warehouse/exits/index.vue`) con P-BOD-07 (`ExitLoadingDialog`) y P-BOD-08 (`YardExitDialog`); P-BOD-09 (`F/pages/warehouse/exits/history.vue`). Cumplen su lista del wireframe (`D/levantamiento-2026-11/fase_2-mockups/bodega.html`, P-BOD-06 a P-BOD-09; `A/` §2.2 g; MK-10) y se capturan en `evidencias/fe3-*`.
- **Componentes:** `ExitLoadingDialog`, `YardExitDialog`; `exit-loading.ts` con sus pruebas. El reloj, con `WarehouseClockTag` y `warehouse-clock.ts` (F04), refrescado cada minuto.
- **Guardias:** las dos páginas entran a `MAQUETACION_PAGES`. Sesión simulada con `?roles=Admin,Warehouse` y `?roles=Warehouse`.
- **Lista del wireframe:** columnas, filtros y acciones de D17 y D20; el modal de D18 a dos columnas con sus avisos, «Cargar todo», firma y fotos, sin sello ni «Retirar de»; el de D19 sin firma ni fotos.
- **Al cerrar:** dile al usuario qué rutas abrir y con qué roles para su revisión (§8.6), y detente.
- **Estado:** pendiente.

### 8.6 Revisión del usuario (después de FE-3)

Con FE-1 a FE-3 cerradas y con push, el usuario revisa las pantallas en `yarn dev` con la sesión simulada antes de I-06: `/foreign-trade/exits` (las dos pestañas y el drawer), `/foreign-trade/exits/new`, `/foreign-trade/exits/new?deposito={Id simulado}`, `/foreign-trade/exits/{Id del Borrador de Báscula simulado}/edit`, `/dev/components` (sección «Etapa Salidas») con `?roles=Admin,ForeignTrade` y `?roles=ForeignTrade`; `/warehouse/exits` y `/warehouse/exits/history` con `?roles=Admin,Warehouse` y `?roles=Warehouse`. Si pide ajustes, van en un plan de ajustes de la maquetación, como los de F03 a F05, y se ejecutan en `f2/f06-salidas` antes de I-06.

---

## 9. Riesgos

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R1 | `exitSchema` cambia y Báscula lo valida en la búsqueda por placa (C-F01-101) | Campos aditivos que el backend siempre manda; FE-1 ajusta los fixtures de Báscula; QA2-F06-020 por API y QA2-F06-048 en el navegador; los dos repos se fusionan juntos en I-06 (como `P04/` R8) |
| R2 | Saldos de una salida de inspección desde el kárdex, con dos líneas del mismo producto | Regla pura `ExitLineBalances` con pruebas de borde (QA2-F06-006); el orden de las líneas desempata |
| R3 | `placedQuantity` con varias salidas o líneas del mismo producto puede sumar más que lo ubicado | Solo informa (AF-70: el cargue libera solo); tope por línea; no bloquea el cargue |
| R4 | Quitar «Clientes» cambia a quién se factura la guía con varios clientes | Lo decide AF-106; la mora se sigue validando para todos (QA2-F06-015); el aviso al usuario al cerrar I-06 lo dice para Facturación |
| R5 | La pestaña «Guías», las filas y el drawer ofrecen las mismas acciones y pueden divergir | Una sola fuente de acciones (`useExitActions`, D10, D11, D14) con su prueba |
| R6 | P-CE-08 no se puede revisar en el detalle real durante la maquetación: el detalle usa el API real desde I-05 | La galería la muestra con datos simulados (§8.4); I-06 la verifica en el detalle (QA2-F06-043) |
| R7 | Borrar `BillingCollectForm` y lo que solo él usa rompe otra pantalla | Grep de cada archivo antes de borrarlo (trampas 4 y 7); `yarn build` y la suite completa en I-06 (2); QA2-F06-049 |
| R8 | Las rutas viejas se borran sin redirección | Nada está desplegado (M25); el menú, los atajos y los tableros apuntan a las nuevas (D28, D29) |
| R9 | El soporte reemplazado queda en el almacenamiento | Como hoy con la orden externa; limpiar archivos queda fuera de alcance |
| R10 | Videos, manuales y casos QA de la campaña de órdenes de cargue y guías quedan desactualizados | Lista en el despliegue final (`PM/` R13) |
| R11 | La maquetación y el backend se separan del contrato (`PM/` R3) | §2 es la única fuente; Zod valida los simulados; cada endpoint tiene su prueba; I-06 pasa los casos en el navegador |

---

## 10. Fuera de alcance

- La facturación de la guía en Facturación (pestaña «Guía de salida» de P-FAC-02, AF-107) y los reportes que leen salidas con R-SAL (Diario de salidas, salidas a destino de abandono, estadísticas, movimientos por depósito): F08.
- La salida en Báscula (P-BAS-03), su precarga por placa y el Borrador que crea (F03, ya construidos); la salida del camión en Vigilancia (`/operations/entries/exits`) y sus guardas de importación (CHG-33).
- Los tipos de notificación configurables (F09); el texto y los destinatarios de los avisos de las salidas no cambian.
- El cierre de la guía global de Báscula para perecederos (`B/Wms.Application/Weighbridge/Commands/Storage/GenerateGlobalGuide/`), que no es de la salida de mercancía.
- Limpiar del almacenamiento los soportes reemplazados (R9).
- Staging, el despliegue final (`PM/` §7.3) y estimar esfuerzo.

**Cambios al hub:** ninguno. I-06 escribe el hito en `D/contexto/estado.md`, como I-04 e I-05.

---

## 11. Prompts por parte

- Parte 1 (backend): [prompt-f2-f06-salidas-backend-2026-11-26.md](prompt-f2-f06-salidas-backend-2026-11-26.md), rama `f2/f06-salidas` del backend.
- Parte 2 (maquetación): [prompt-f2-f06-salidas-maquetacion-2026-11-26.md](prompt-f2-f06-salidas-maquetacion-2026-11-26.md), rama `f2/f06-salidas` del frontend.
- Parte 3 (I-06): [prompt-f2-f06-salidas-integracion-2026-11-26.md](prompt-f2-f06-salidas-integracion-2026-11-26.md), las dos ramas.
- Planificador: [prompt-f2-f06-salidas-planificador-2026-11-26.md](prompt-f2-f06-salidas-planificador-2026-11-26.md).

---

## 12. Mensajes de commit sugeridos

Cada uno termina con la línea de coautoría que indique la sesión.

| Fase | Repo | Mensaje |
| --- | --- | --- |
| BE-1 | BE | `feat(salidas): listado y detalle de la salida con mercancía, saldos y registro de Bodega; depósitos elegibles, guías y etapa Salidas (DEC-080, F06)` |
| BE-2 | BE | `feat(salidas): orden del cliente sin número y con soporte, guía con un solo destinatario y cobro sugerido (DEC-080, F06)` |
| FE-1 | FE | `feat(salidas): maquetación de Salidas de CE con guías y el detalle de la salida, con datos simulados (DEC-080, F06)` |
| FE-2 | FE | `feat(salidas): maquetación de nueva salida, confirmación con el cobro de la guía y etapa Salidas (DEC-080, F06)` |
| FE-3 | FE | `feat(salidas): maquetación de órdenes de salida, cargue, salida de patio e historial de Bodega (DEC-080, F06)` |
| I-06 (1) | BE y FE | `feat(salidas): integración de Salidas de CE, guías, nueva salida y etapa Salidas con el API (DEC-080, F06)` |
| I-06 (2) | BE y FE | `feat(salidas): integración de Bodega, menú y retiro de órdenes de cargue y guías por orden (DEC-080, F06)` y la fusión `merge: I-06, F06 «Salidas de mercancía» en fase-2 (DEC-080, DEC-081)` |
| Cada fase | docs | `docs(f06): fase N de F06 cerrada (sprint 11)` |

---

## 13. Integración I-06 (parte 3)

Un agente con los dos repos (M1, M10), cuando BE-1, BE-2 y FE-1 a FE-3 están cerradas y con push, y la revisión de §8.6 tiene el visto bueno del usuario (o su plan de ajustes, ejecutado). Ocupa los dos repos. Va en dos fases, una por turno: **I-06 (1)**, §13.1 y los casos de CE (QA2-F06-032 a 043); **I-06 (2)**, §13.2, §13.3, los casos de Bodega y del flujo completo (QA2-F06-031, 044 a 051), §13.4 y la fusión.

### 13.1 Fuentes http

Por cada `*.source.ts` de F06, escribe su `*.http.ts` con `contractApi` (`F/shared/http/contract-api.ts`) y los esquemas de §2.3 (`.parse` en cada respuesta; un fallo de esquema se registra en consola y se muestra como error del API), cambia la línea activa y la agrega a `INTEGRATED_SOURCES` (`FT/unit/guards/mock-sources.spec.ts:31`):

| Fuente | Endpoints | Pantallas |
| --- | --- | --- |
| `F/features/exits/services/exit.source.ts` | C-F06-01 a C-F06-07; C-F01-99 a C-F01-108 | P-CE-11, formulario, confirmación, P-CE-08, P-BOD-06 a P-BOD-09, drawer, tableros |
| `F/features/exits/services/guide.source.ts` | C-F06-08, C-F06-09 | P-CE-11 (pestaña «Guías») |
| `F/features/exits/services/catalog.source.ts` (fachada, D26) | — | Se borra: sus usos pasan a las fuentes integradas de F01, F03 y F04 (`vehicle`, `driver`, `stakeholder`, `city`, `crew` y la de tipos de vehículo de F04; C-F01-15, 17, 21, 23, 25, 26, 47, 52, 141; C-F04-17) |

Verifica además que la búsqueda por placa de Báscula (C-F01-101) sigue pasando su esquema con los campos nuevos (R1). Las páginas salen de `MAQUETACION_PAGES` a medida que se integran; I-06 (2) la deja vacía. `F/features/exits/mocks/` se borra en I-06 (2), y los simulados que usen las pruebas de componentes pasan a `FT/fixtures/exits/` (como I-03 a I-05).

### 13.2 Menú, rutas, enlaces y guardias

- **Menú** (D28): `F/components/layout/menu-model.ts:60-81` (Bodega) y `:83-124` (Comercio Exterior), con sus comentarios al día.
- **Atajos y tableros** (D29): `F/composables/useGlobalShortcuts.ts:25`; `F/pages/foreign-trade/index.vue:30-45` y `:100-112` con `F/features/foreign-trade/composables/useForeignTradeDashboard.ts`; `F/pages/warehouse/index.vue:37-43`.
- **Guardias** (D30): `FT/unit/guards/list-pattern-routes.ts` (`PATTERN` con las tres rutas nuevas; fuera de `PENDING` las cuatro de F06 y F06 de `PENDING_FEATURES`; fuera de `OUTSIDE` y de `TITLE_RULE_EXEMPT` las dos páginas de creación); `MAQUETACION_PAGES` vacía.
- **Auditoría** (D32): `F/features/audit/utils/entity-labels.ts`.
- **Galería:** la sección «Etapa Salidas» de `/dev/components` se queda, con datos de prueba (como las demás secciones de la galería).

### 13.3 Se borra

Con `rm`, después de comprobar con grep que nada fuera de lo que se borra los importa (trampas 4 y 7): lo de D31 y la parte de frontend de D33 que no hizo FE-2. `BillingCollectForm` se borra aquí: F06 es su último uso (`grep -rn "BillingCollectForm" app test` vacío al terminar). `ChangePaymentModeDialog` se queda (D16). Lo que importe otra pantalla, se queda y se anota en §13.6.

### 13.4 Casos QA y docs

- QA2-F06-031 a QA2-F06-051 en PASA, en el navegador, contra el backend local de `f2/f06-salidas` y sin la sesión simulada; QA2-F06-001 a 020 siguen en verde en la suite. Los de flujo completo (050 y 051) se hacen sobre una base local recreada con los catálogos y tarifas de prueba.
- Copia los casos con su resultado a `D/qa/casos-qa2-f06-salidas-AAAA-MM-DD.md`, con el formato de `D/qa/casos-qa2-f04-bodega-2026-11-25.md`.
- Actualiza este plan (§8 y §13.6), `D/planes/README.md`, la matriz (§2.2), `D/contexto/estado.md` (hito de I-06) y marca «Ejecutado» el prompt de integración.
- **Aviso al usuario** (`PM/` §4 y §5.3): con F06 integrada, **el flujo de entrada y salida está completo para probarlo en local**: Vigilancia, Báscula, Bodega (recepción, cargue y salida de patio), Comercio Exterior (depósitos, levantes, salidas y guías) y Báscula de salida, con las rutas y los usuarios por rol. El aviso nombra lo que sigue pendiente (Facturación, F07 y F08; notificaciones configurables, F09) y, para Facturación, que la guía de una salida con varios clientes se factura a un solo destinatario (AF-106, R4).

### 13.5 Criterio de salida

- Compuertas de `PM/` §6.1 en BE y §6.2 en FE (salvo «sin llamadas reales»), con las cifras antes y después.
- QA2-F06-031 a QA2-F06-051 en PASA.
- Ningún import de `mocks/` de una feature fuera de las pruebas; `F/features/exits/mocks/` y la fachada, borradas.
- Menú, atajos y tableros con las rutas de F06; páginas, componentes y pruebas viejas, borradas; la guardia list-pattern sin F06 en `PENDING`; `MAQUETACION_PAGES` vacía.
- Fusión con `--no-ff` de `f2/f06-salidas` en `fase-2` en los dos repos, y push.

### 13.6 Estado

Pendiente.
