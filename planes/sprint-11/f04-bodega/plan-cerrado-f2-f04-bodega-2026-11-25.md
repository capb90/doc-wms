# Plan cerrado — Fase 2 · F04 Bodega

> **Fecha:** 25 de noviembre de 2026. **Estado:** Aprobado por el usuario el 2026-11-25 («Aprobar con §10»), con los cambios al hub de §10. En ejecución desde que se lanzan sus prompts (§11).
> **Origen:**
> - `DEC-080` y el análisis funcional `levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md` (§2.2 completo, §3.1, §3.3 y §3.4), con los wireframes `fase_2-mockups/bodega.html` (P-BOD-01 a P-BOD-05; P-BOD-06 a P-BOD-09 son de F06) y `transversales.html` (P-TR-02, P-TR-03, P-TR-08, P-TR-09 y P-TR-11), y los ajustes del usuario de `levantamiento_staging/bodega_ajustes.md` (AF-64);
> - el plan maestro `planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md` (M1 a M25, `DEC-081`);
> - AF dueñas (13, plan maestro §3.1): AF-56, AF-57, AF-58, AF-59, AF-60, AF-61, AF-62, AF-63, AF-64, AF-65, AF-69, AF-105 y AF-119;
> - lo integrado de F01 (D1 a D47, contrato C-F01, notas de las fases 3 a 6 y de I-01), de F02 (D1 a D21 y los ajustes de su QA) y de F03 (D1 a D45, contrato C-F03 y los ajustes de UI y de QA);
> - las respuestas del usuario a la ronda de preguntas de este plan (2026-11-25), en D1 a D13.
>
> **Base:** BE `fase-2` `eb4e428` · FE `fase-2` `2c848af` · docs `main` `4677387`. Rama: `f2/f04-bodega` en BE y FE.
> **Partes:** 0 (contrato, §2) · 1 (backend, tres fases) · 2 (maquetación, tres fases y la revisión del usuario) · 3 (I-04, dos fases, §13). **Migraciones:** `AddWarehouseDelayAlerts` (BE-1), `ReceptionPerEntry` (BE-2) y `ForkliftRequiresInvoice` (BE-3).
> **Rutas:** relativas a `code_workspace/`. Prefijos: `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`; `A/` = el análisis; `PM/` = el plan maestro; `P01/` = `D/planes/sprint-11/f01-nucleo/plan-cerrado-f2-f01-nucleo-2026-11-21.md`; `P02/` = `D/planes/sprint-11/f02-base/plan-cerrado-f2-f02-base-2026-11-21.md`; `PAJ/` = `D/planes/sprint-11/f02-base/plan-cerrado-f2-f02-ajustes-qa-2026-11-24.md`; `P03/` = `D/planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-bascula-2026-11-24.md`; `AUI/` = `D/planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-ajustes-ui-2026-11-24.md`; `AQ3/` = `D/planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md`.

**Cómo leer este plan.** El ejecutor de cada parte lee §0, §1, §2.1 (índice) y la sección de su fase en §8. Cada fase de §8 nombra sus decisiones, sus endpoints (con la ficha de §2.2 y el esquema de §2.3 que le tocan), sus archivos (§3) y sus casos QA (§6). El resto se lee solo cuando la fase lo cita. Las líneas citadas son de la base (`eb4e428` y `2c848af`).

---

## 0. Instrucciones para el ejecutor

1. **Lecturas mínimas:** `D/README.md`, el `AGENTS.md` de tu repo (su sección «Eficiencia de contexto y cierres por fase» rige tu trabajo), `D/procesos/flujo-de-trabajo-agentes.md`, `PM/` §1.2, §5 y §6, y de este plan §0, §1, §2.1 y tu fase en §8. El frontend lee además `D/contexto/convenciones-tecnicas.md` §3 (drawer de detalle, tablas de listado y páginas que no son listados).
2. **Rama y git** (`PM/` §5.3): `git fetch`; si `develop` avanzó, fusiona `develop` en `fase-2`; crea `f2/f04-bodega` desde `fase-2` (o retómala si ya existe) y trabaja ahí. Al cerrar cada fase: commit con el mensaje de §12 y push de la rama. Sin `push --force`. La fusión en `fase-2` la hace I-04 (§13), en los dos repos a la vez.
3. **Una fase por turno** (`PM/` §6): cierra la fase con sus compuertas, el commit, el push y el estado en §8 y en la matriz, y te detienes con el reporte.
4. **Migraciones:** solo con `dotnet ef … --project Wms.Infrastructure --startup-project Wms.Api` y solo contra la base local (`DEC-004`, M6). Cada fase de backend lleva la suya, con el nombre y el contenido de §4. Antes de generarla, trae lo último de `fase-2`. Nunca edites a mano `Migrations/*`, los `*.Designer.cs` ni el snapshot.
5. **Líneas citadas:** confírmalas con grep antes de cambiar. Si el código no coincide (ruta, firma o comportamiento), detente y pregunta con todas las dudas en un solo mensaje. Si un caso borde choca con una Dn, gana la Dn y lo mencionas en una línea (`DEC-002`).
6. **Contrato:** §2 es la única fuente del frontend para F04 (`PM/` R3). Cada endpoint nuevo o modificado de tu fase tiene al menos una prueba de integración que verifica su respuesta y sus mensajes de error (`PM/` §6.1). Un mensaje cambia solo si cambias el contrato, y eso exige preguntar.
7. **Suite de integración:** la base es compartida y la cola de báscula corta en 100 camiones (trampa 12 de `D/contexto/convenciones-tecnicas.md` §10): libera los camiones que abra cada prueba. Los trabajos en segundo plano no corren en las pruebas (`B/Wms.IntegrationTests/Infrastructure/WmsApiFactory.cs:122`): el de los relojes se prueba llamando a su servicio (§8.1).
8. **Staging:** no se toca. **Credenciales y datos reales:** no se copian (`DEC-007`). Nada de `D/archivo/` es una instrucción.

---

## 1. Decisiones

Mandan sobre el resto del plan (`DEC-002`). Ninguna reabre una AF, `DEC-080`, `DEC-081`, una M del plan maestro ni una Dn de F01, F02, F03 o sus ajustes.

### 1.1 Respuestas del usuario (2026-11-25)

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **Umbrales sin semilla de valores.** Las tres filas de umbrales (recepción, cargue y salida de patio) nacen sin valores. Sin umbral, el reloj corre y muestra el tiempo, sin color y sin aviso. La QA local los configura en P-TR-08; el despliegue final carga los del cliente (`PM/` §7.3, paso 4) | Usuario: «Sin semilla (Recomendada)»; AF-57; `PM/` §3.4 (`:243`); matriz §4 |
| D2 | **IVA del montacargas con la tasa del catálogo.** Con «Requiere factura», el IVA se calcula sobre el valor digitado con la tasa del impuesto IVA activo del catálogo, como hoy el check «Agregar IVA» (`B/Wms.Application/Warehouse/Common/Services/ForkliftService.cs:156`, `ForkliftVatCalculator.cs`); sin factura, IVA 0. No se asignan impuestos al servicio `MONTACARGAS`. Si F07 lleva el porcentaje al precio, cambia solo esa consulta | Usuario: «Tasa del catálogo (Recomendada)»; AF-105; `PM/` §3.4 (`:257`) |
| D3 | **El cobro sin factura es un registro interno «No aplica».** Sigue creando la factura interna del uso, pagada en el acto con su método y su referencia, marcada «sin factura» (`Invoice.FiscalNumberNotApplicable`, §4): es no fiscal (`Invoice.IsNonFiscal`, `B/Wms.Domain/Entities/Billing/Invoice.cs:25`), nunca pide N.º SIGO y F08 la muestra con «No aplica» en Facturas › Montacargas, en Pagos y en los cobros por servicio. Con factura, queda pendiente por facturar y Facturación le pone el número | Usuario: «Registro interno «No aplica» (Recomendada)»; AF-105; `A/` `:1402`, `:1577-1578` |
| D4 | **«Queda sobre el vehículo»: marca y ubicación sembrada.** La recepción guarda la marca (`ReceptionLog.StaysOnVehicle`) y ubica todos sus productos en la ubicación sembrada `SOBRE-VEHICULO` («Sobre vehículo»), protegida (`WarehouseLocation.IsSystem`: no se edita, no se desactiva ni se borra). Así se cumple AF-61, el inventario y la disponibilidad la muestran y el cargue de F01 la libera solo (`P01/` D38). F07 lee la marca por entrada (AF-120) | Usuario: «Marca y ubicación sembrada (Recomendada)»; AF-119, AF-61 |
| D5 | **Ruta de la recepción directa: `/warehouse/receptions/direct/[entryLogId]`.** «Nueva recepción directa» (P-BOD-01) abre un modal chico con los ingresos de Vigilancia elegibles (placa, conductor, motivo y hora; C-F01-152) y lleva a la página. Recargar no pierde el camión. No usa `/warehouse/receptions/create` (guardia `FT/unit/guards/receptions-create-route.spec.ts`, CHG-85) | Usuario: «/receptions/direct/[entryLogId] (Recomendada)»; AF-64, AF-69; como `P03/` D5 |
| D6 | **Ruta de Umbrales de alertas: `/admin/alert-thresholds`.** Página de configuración (`OUTSIDE`, «Formulario de configuración» en la guardia): sin tarjeta de título, con `<h1 class="sr-only">`, la tabla de tres filas editable y «Guardar» en una barra arriba a la derecha. API: `GET` y `PUT administration/alert-thresholds` | Usuario: «/admin/alert-thresholds (Recomendada)»; `P02/` D1; AF-128 |
| D7 | **Montacargas: un ítem y un listado.** «Montacargas» lleva a `/warehouse/forklift`, que pasa a listado con el patrón (P-BOD-05): pestañas «En curso» y «Finalizados» con su contador, «Finalizar» en la fila en curso, «+ Registrar uso» en la barra y «Ver» en drawer. I-04 borra `/warehouse/forklift/history` | Usuario: «Un ítem, un listado (Recomendada)»; P-TR-01 (AF-127); AF-59, AF-64 |
| D8 | **El detalle de una recepción va en drawer y `receptions/[id].vue` se borra.** El historial abre el detalle en `AppDetailDrawer` (con `?id=` para enlazarlo); I-04 borra `F/pages/warehouse/receptions/[id].vue`, que solo enlaza el historial de hoy | Usuario: «Drawer y se borra (Recomendada)»; AF-130 |
| D9 | **Los endpoints de la recepción se modifican, no se reemplazan.** `GET warehouse/pending-from-weighbridge` pasa a ser la lista de P-BOD-01 (C-F04-06); `POST warehouse/receptions` recibe la entrada sin llegada (C-F04-07); `POST warehouse/receptions/without-weighbridge` toma los campos de MK-09 (C-F04-08); se retiran `register-arrival` y `{id}/complete` (C-F04-11 y C-F04-12) | Usuario: «Modificar los de hoy (Recomendada)»; `B/Wms.Api/Controllers/v1/WarehouseController.cs:224-395` |
| D10 | **Los relojes que muestran F05 y F06 van en sus lecturas de hoy.** F04 modifica `GET exits` y `GET exits/{id}` (C-F04-03 y C-F04-04: `warehouseClock`) y `GET foreign-trade/warehouse-storages/{id}/entries` (C-F04-05: `reception`, con su reloj). Un solo esquema (`warehouseClockSchema`); F05 y F06 los maquetan | Usuario: «En las lecturas de hoy (Recomendada)»; `PM/` §2, regla de pertenencia |
| D11 | **Dos tablas y un trabajo cada minuto.** `warehouse_alert_thresholds` (tres filas sembradas sin valores, auditada) y `warehouse_delay_alerts` (un registro por aviso enviado, con índice único); el trabajo corre cada minuto y solo avisa si logra registrar el aviso (D35) | Usuario: «Dos tablas y job por minuto (Recomendada)»; AF-57 |
| D12 | **Bodega crea posiciones con `POST warehouse/locations`.** Política nueva `LocationCreateAccess` (Admin, ForeignTrade, Billing, Warehouse) solo en ese endpoint (C-F04-15); editar y borrar siguen en Configuración. La recepción la llama desde un modal chico («+ Nueva posición»). Corrige la nota de C-F01-44, que cita un endpoint de `WarehousePlacementsController` que no existe | Usuario: «Aflojar POST locations (Recomendada)»; `A/` §3.1 (`:1733`); `B/Wms.Api/Controllers/v1/WarehouseLocationsController.cs:68-69` |
| D13 | **Tres fases por parte** (§8). Backend: BE-1 umbrales, relojes y avisos; BE-2 recepción; BE-3 montacargas, inventario y novedades. Maquetación: FE-1 Recepción, modal y recepción directa (P-BOD-01 a P-BOD-03); FE-2 Montacargas, Umbrales e historial de recepciones (P-BOD-04, P-BOD-05, P-TR-08); FE-3 Inventario y Novedades. Después de FE-3, la revisión del usuario con la sesión simulada (§8.7). I-04 en dos fases (§13) | Usuario: «Tres y tres (Recomendada)» |

### 1.2 Recepción

| # | Decisión | Fuente |
| --- | --- | --- |
| D14 | **Qué entrada está en Recepción.** Una fila por entrada (`WarehouseStorageEntry`) que tiene su primer peso, esté o no el ciclo (el primer peso vive en el vínculo camión–servicio hasta el cobro: `B/Wms.Domain/Entities/Logistics/ServiceRecordEntryLog.cs:31-33`, `P03/` D2; o en el primer pesaje del ciclo), no está anulada, su depósito no está cerrado ni anulado y no tiene una recepción activa. Su reloj arranca en la hora del primer peso. Una entrada registrada sin peso no aparece. Reemplaza `PendingReceptionFilters.IsPendingReception` (`B/Wms.Application/Warehouse/Queries/GetPendingFromWeighbridge/PendingReceptionFilters.cs`), que exige ciclo | AF-58, AF-65 («la entrada pesada aparece en Recepción»); `P03/` D2 |
| D15 | **Sin llegada.** Se retiran el registro de la llegada (C-F04-11) y el completar una recepción en curso (C-F04-12), con `ReceptionLog.RegisterArrival` (`B/Wms.Domain/Entities/Warehouse/ReceptionLog.cs:41`) y su comando, validador y pruebas. La columna `reception_logs.arrival_at` y el estado `InProgress` se conservan sin uso nuevo: los leen el detalle del depósito de CE (`B/Wms.Application/ForeignTrade/Common/Services/DepositWarehouseReceptionBuilder.cs:27`, `:94-100`) y las estadísticas (`B/Wms.Application/Reports/Queries/GetOperationalStatistics/GetOperationalStatisticsHandler.cs:114`), y las bases se recrean (M18) | AF-64, AF-65; M18 |
| D16 | **Recepción por entrada** (C-F04-07). Recibe una entrada de D14 y la deja «Recibida» en un paso. Reglas: solo productos con cantidad mayor que cero; la cantidad no supera lo declarado para ese camión (400); cada producto descargado lleva su ubicación (AF-61; 400), salvo «Queda sobre el vehículo» (D19); con unidades de carga, se confirman todas «Recibida completa», sin productos, como hoy (`ReceptionCargoUnits.cs`); si lo contado es menor que lo declarado se avisa a CE como hoy (`ReceptionDeclaredDifference.cs`). La recepción sigue siendo informativa: no mueve stock ni fechas y ubica lo descargado hasta lo pendiente (`WarehousePlacementService.PlaceUpToPendingAsync`, `B/Wms.Application/Warehouse/Common/Services/WarehousePlacementService.cs:47`). Una entrada ya recibida: 409; anulada: 409 | AF-58, AF-61, AF-65; `DEC-010` (2) y (3) |
| D17 | **Tipo de vehículo en la recepción** (AF-62): selector opcional con el catálogo de vehículos (`GET weighbridge/vehicle-types`, `B/Wms.Application/Weighbridge/Common/Dtos/VehicleTypeCatalog.cs`), precargado con el del vehículo. Lo que se elige lo guarda el comando de la recepción en `Vehicle.VehicleType` (`B/Wms.Domain/Entities/Logistics/Vehicle.cs:14`). Bodega no llama a `PATCH vehicles/{id}` (C-F01-24, `VehicleConfigurationAccess`, sin Bodega) | AF-21, AF-62; `P01/` D24 |
| D18 | **Cuadrilla por recepción** (AF-60): `ReceptionLog.CrewId`, opcional. Como un depósito puede tener varios camiones (`P01/` D20), la cuadrilla deja de vivir solo en el depósito; `WarehouseStorage.CrewId` (`B/Wms.Domain/Entities/Warehouse/WarehouseStorage.cs:43`, `:461`) sigue tomando la de la última recepción, porque la leen los detalles de CE (`B/Wms.Application/ForeignTrade/Queries/GetImportDepositDetail/GetImportDepositDetailHandler.cs:248`) hasta que F05 decida | AF-60 («una por recepción, como hoy»); `P01/` D20 |
| D19 | **«Queda sobre el vehículo» en detalle** (D4): con el interruptor encendido, el modal oculta las ubicaciones y el comando ubica cada producto descargado en `SOBRE-VEHICULO`. La ubicación se siembra con un Id fijo (§4); `GET warehouse/locations` la devuelve con `isSystem: true` (C-F04-14); `PATCH` y `DELETE` responden 409 (C-F04-16); Configuración › Ubicaciones no muestra sus acciones. El importador del legacy no crea una ubicación con ese código (§7) | AF-119; D4 |
| D20 | **Recepción directa** (C-F04-08; AF-64, AF-69, `P01/` D23). Siempre crea un depósito de inspección nuevo en Borrador, como hoy y como dice el análisis (`A/` `:657`, `:810`): Bodega no elige depósito (la asociación por documento de AF-17 es de Báscula). Modalidad fija «Inspección»; descripción de la inspección obligatoria (10 a 500); tipo de documento (Carta porte o Guía de transporte, C-F03-44) y número, opcionales y juntos; productos opcionales; por producto declarado, cantidad descargada y ubicación (o «Queda sobre el vehículo»). Camión y conductor: el conductor por Id (alta y elección con `DriverQuickDialog`, C-F01-17), la transportadora obligatoria (`P01/` D26; alta rápida con C-F01-141), el país y el tipo del vehículo se guardan en el vehículo. Cuadrilla, firma, fotos y observaciones como en la recepción. Ya no pide cliente, terceros, documentos adicionales, valor, moneda ni motivo. Los ingresos elegibles no cambian (`DirectReceptionEntryRules.cs`, C-F01-152) | AF-17, AF-64, AF-69; MK-09; `A/` §2.2 f |
| D21 | **«+ Nueva posición»** (D12): modal chico con código, nombre y capacidad (pasillo, estante y nivel opcionales), que llama a C-F04-15 y deja la ubicación nueva elegida en esa fila | `A/` §3.1; P-BOD-02 |
| D22 | **Historial de recepciones** (`/warehouse/receptions/history`) con el patrón: paginado con orden y filtros por columna en el servidor (C-F04-09), «Ver» de solo icono que abre el drawer (D8) | AF-129, AF-130; `A/` §2.2 g («se conserva como hoy») |
| D23 | **Recepción (P-BOD-01):** columnas del wireframe (hora del pesaje, vehículo, depósito, cliente, mercancía, cantidad declarada, tiempo desde el pesaje); filtros por columna (rango de fechas, placa, número, cliente, producto y color); orden por defecto `weighedAt asc` (la más atrasada arriba); el reloj se refresca cada minuto en la pantalla con la regla pura (§2.3). Acciones de fila: «Completar recepción» y «Montacargas» (dos: botones de solo icono con tooltip, `AppRowActions`). «Nueva recepción directa» en la barra de la tabla | P-BOD-01; AF-99, AF-129 |
| D24 | **Montacargas desde la fila** (AF-59): abre «Iniciar uso» con la placa, el cliente y el depósito de la fila y el tipo de vehículo precargado. Si el servicio de la entrada ya tiene un uso en curso (`forkliftInProgress`), el botón queda deshabilitado con el tooltip «Montacargas en curso» | AF-59; `StartForkliftUseCommandHandler.cs:91` |

### 1.3 Montacargas

| # | Decisión | Fuente |
| --- | --- | --- |
| D25 | **«Requiere factura»** (AF-105; D2, D3): interruptor en el cobro, apagado por defecto, como el check de `DEC-018`. Encendido: IVA con la tasa del catálogo, modo «Pendiente por facturar», factura interna sin pago y «Pendiente de número». Apagado: sin IVA, «Pago inmediato», factura interna pagada y marcada «sin factura». `ForkliftUse.ApplyVat` (`B/Wms.Domain/Entities/Warehouse/ForkliftUse.cs:35`) pasa a `RequiresInvoice`. El servidor exige que `billing.paymentMode` coincida: 400 si no | AF-105 (reemplaza `DEC-018`); D2, D3 |
| D26 | **Tipo de vehículo del montacargas** (AF-63): el selector es el de las tarifas (`ForkliftVehicleType`: Tractomula, Doble troque, Sencillo, Turbo, Guacal / estiba; C-F04-25), precargado si el tipo del vehículo tiene el mismo nombre. Si el vehículo no tiene tipo y el elegido existe en el catálogo de vehículos (los cuatro comunes), se guarda en el vehículo. «Guacal / estiba» no se guarda y un vehículo con tipo (también «Veh. particular» u «Otro») no se sobrescribe. Resuelve el choque entre los dos catálogos (`VehicleTypeCatalog.cs` y `B/Wms.Domain/Enums/ForkliftVehicleType.cs`) con la letra de AF-63, «si falta» | AF-63; `DEC-002` |
| D27 | **Inicio del uso** (C-F04-20): ya no recibe el modo de pago (lo fija el cobro, D25). Recibe el servicio y la entrada del camión: desde la fila de Recepción (D24) o, con «+ Registrar uso», desde la búsqueda por placa (C-F04-13) | AF-59, AF-105 |
| D28 | **Listado de Montacargas** (D7): «En curso» muestra inicio, placa, tipo de vehículo, cliente, depósito y horómetro inicial, con «Finalizar» y «Ver»; «Finalizados» muestra las columnas de P-BOD-05 (inicio, fin, placa, tipo, cliente, horas, «Pagado» y «Facturado»), con «Ver». «Pagado» es lo pagado de la factura del uso; «Facturado» dice si la factura ya tiene N.º SIGO (sin factura: «No»). Paginado con orden y filtros en el servidor (C-F04-18) | AF-64 («solo lo pagado y si se facturó»); P-BOD-05 |
| D29 | **Se retiran** `GET warehouse/forklift-uses/active` (C-F04-22; lo reemplaza el filtro de estado de C-F04-18) y `PATCH warehouse/forklift-uses/{id}/payment-mode` (C-F04-23; el modo lo fija «Requiere factura» y el cambio solo valía para usos sin factura, que ya no se crean: `ForkliftUse.cs:186`). Solo los llamaban pantallas de Bodega (`useActiveForkliftUses`, `useChangeForkliftUsePaymentMode`); nadie pierde una función (`DEC-005`) | AF-105; `DEC-005` |
| D30 | **El cobro usa `AppChargeForm`** (P-TR-09; `P02/` D13; `P03/` D42 lo deja para F04). El diálogo del cobro muestra el valor del servicio (base editable, precargada con la tarifa de C-F04-24), el IVA y el total; pasa a `AppChargeForm` el total sin editar y `paymentModes` con el modo de D25; el «+» del tercero usa C-F01-141. Envía `billing.totalAmount` = la base (como hoy, `EndForkliftUseCommand.cs`). **Único cambio a un compartido** (`PM/` R4): `AppChargeForm` sigue los cambios de `paymentModes` (hoy toma el primero al montar, `F/components/app/AppChargeForm.vue:94`), con su prueba | AF-54, AF-132; `PM/` R4 |

### 1.4 Relojes, umbrales y avisos

| # | Decisión | Fuente |
| --- | --- | --- |
| D31 | **Tres relojes** (AF-56, AF-65, AF-66; `A/` §3.4): **Recepción**, por entrada, desde el primer peso hasta la recepción (D14); **Cargue**, por salida `Deposit` o `Consolidated` confirmada, desde la confirmación hasta el cargue (`GoodsExit.ConfirmedAt` y `LoadedAt`, `B/Wms.Domain/Entities/Warehouse/GoodsExit.cs:41`, `:45`); **Salida de patio**, por salida `EntryTicket` o `Global` confirmada, desde la confirmación hasta la salida de patio (`YardExitAt`, `:52`). «Desde la guía» es la confirmación, que emite la guía (`P01/` D36); en inspección, sin guía, también. Reabrir y volver a confirmar arranca otro reloj; un cargue conservado al reabrir (`P01/` D34) lo deja detenido | AF-56, AF-65, AF-66; `P01/` D34, D36 |
| D32 | **Regla pura `WarehouseClockRules`** (`B/Wms.Application/Warehouse/Alerts/`): minutos transcurridos (enteros, hacia abajo) hasta ahora o hasta el fin; nivel: sin umbrales, `None`; desde el rojo, `Red`; desde el amarillo, `Yellow`; si no, `None`. Un reloj detenido conserva el nivel con que se detuvo. El frontend usa la misma regla (`F/features/warehouse/utils/warehouse-clock.ts`) para refrescar el tiempo y el color cada minuto | AF-57 |
| D33 | **Umbrales** (D1, D6, D11): una fila por registro vigilado (`Reception`, `Loading`, `YardExit`), con amarillo y rojo en minutos enteros: los dos o ninguno, de 1 a 10.080 (siete días), amarillo menor que rojo. Solo Admin los lee y los cambia (AF-128); la tabla es auditable (`IAuditable`). Las pantallas no los piden aparte: cada reloj trae los suyos | AF-57, AF-128 |
| D34 | **El reloj en el contrato** (`warehouseClockSchema`, §2.3): registro vigilado, inicio, fin (nulo si corre), minutos, nivel y los dos umbrales vigentes. Lo traen la lista de Recepción (C-F04-06), el historial (minutos de la recepción, C-F04-09), las salidas (C-F04-03 y C-F04-04) y las entradas del depósito (C-F04-05) | D10 |
| D35 | **Trabajo en segundo plano** `WarehouseDelayAlertBackgroundService` (`B/Wms.Api/BackgroundJobs/`): arranca a los 30 s y corre cada 60 s (`WarehouseAlerts:IntervalSeconds`); en cada vuelta llama a `WarehouseDelayAlertService.RunOnceAsync(ahora)`. Para cada reloj abierto con umbrales calcula el nivel; por cada nivel alcanzado sin aviso registrado, inserta la fila en `warehouse_delay_alerts` (índice único por registro vigilado, Id, inicio del reloj y nivel) y, solo si la inserción entra, avisa. Si al correr ya cruzó amarillo y rojo sin avisos (el servicio estuvo caído o el umbral es nuevo), registra los dos y avisa solo el rojo. Bajar un umbral puede avisar registros abiertos que ahora lo cruzan; subirlo no borra lo avisado. Un error se registra en el log y la vuelta siguiente reintenta. Sin auditoría propia (`DEC-055`) | AF-57; D11 |
| D36 | **Aviso «Atraso de Bodega»** (`A/` §3.4, `:1877`): por `NotificationOrchestrator.NotifyRoleAsync` (`B/Wms.Api/Services/NotificationOrchestrator.cs:79`) a los roles fijos ForeignTrade y Warehouse, en la aplicación y por correo, como los avisos nuevos de F01 (`P01/` D45); F09 lo pasa a su tipo (M23). Nivel `Warning` en amarillo y `Error` en rojo. Textos: «Recepción de {placa} · depósito {N}: {tiempo} desde el pesaje (umbral {amarillo\|rojo}: {m} min).», «Cargue de la salida {N} ({placas}): {tiempo} desde la guía {G} (umbral …).» y «Salida de patio de la salida {N} ({placas}): {tiempo} desde la guía {G} (umbral …).» (sin guía: «desde la confirmación»). `RelatedEntityType`: `WarehouseStorageEntry` o `GoodsExit` | AF-57; `PM/` §2.2; `DEC-070` |
| D37 | **Qué queda para F05 y F06** (D10): F04 construye y prueba por API `warehouseClock` en las salidas (C-F04-03, C-F04-04) y `reception` en las entradas del depósito (C-F04-05) en BE-1, y en FE-1 extiende sus esquemas Zod y deja `WarehouseClockTag`. No los maqueta: F06 los muestra en Órdenes de salida (P-BOD-06; también puede usarlos en P-BOD-09 y P-CE-11) y F05 en la etapa Bodega del detalle de CE (PR-17) | `PM/` §2 (regla de pertenencia) |

### 1.5 Pantallas, componentes y transversales

| # | Decisión | Fuente |
| --- | --- | --- |
| D38 | **Patrones** (`D/contexto/convenciones-tecnicas.md` §3): Recepción, Historial de recepciones, Montacargas, Inventario y Novedades son listados (`PATTERN`): `AppDataTable` en la página, sin tarjeta de título, filtros en la columna, orden en el servidor si paginan, acciones con `AppRowActions` (botones `small`, `outlined`; más de tres posibles, todas al menú), detalle en `AppDetailDrawer` con las acciones en el menú del encabezado y sin pie. La recepción directa (P-BOD-03, fuera del menú) y Umbrales (P-TR-08, en `OUTSIDE`) son formularios, sin tarjeta de título, con `<h1 class="sr-only">` y su acción principal en una barra arriba a la derecha. La recepción física (P-BOD-02) es un modal a dos columnas (MK-08, AF-130) y el montacargas (P-BOD-04), dos modales | AF-99, AF-129, AF-130; `PAJ/`, `AUI/`, `AQ3/` |
| D39 | **Compartidos sin cambios, salvo `AppChargeForm` (D30):** `AppDataTable`, `AppRowActions`, `AppDetailDrawer`, `AppDetailSection`, `AppSearchSelect`, `AppCrudDialog`, `ReasonDialog`; de otros dominios, `DriverQuickDialog` (`F/features/entries/components/`), `StakeholderQuickDialog` (`F/features/stakeholders/components/`) y `VehiclePlateTag` (`F/features/weighbridge/components/`, sin la «D»); de Bodega, `SignaturePad`, `PhotoUploader`, `ProductPlacementsDialog`, `LocationContentPanel` y `WarehouseDepositSelect`. Si una pantalla necesita cambiar otro compartido, el ejecutor se detiene y pregunta | `PM/` R4; `P03/` D38 |
| D40 | **Componentes de Bodega nuevos** (`F/features/warehouse/components/`): `WarehouseClockTag` (tiempo y color; lo reusan F05 y F06), `ReceptionDialog` (P-BOD-02), `ReceptionProductRows` (cantidad, ubicación y «Copiar» por producto; P-BOD-02 y P-BOD-03), `LocationQuickDialog` (D21), `DirectReceptionEntryPicker` (D5), `DirectReceptionTruckSection` y `DirectReceptionGoodsSection` (P-BOD-03), `ForkliftStartDialog` y `ForkliftChargeDialog` (P-BOD-04), `ForkliftUseDetail` y `ReceptionDetail` (contenido de los drawers). `NoveltyFormDialog` se rehace a dos columnas (D43). §3.3 dice qué usa cada pantalla | `PM/` §5.5; como `P03/` D39 |
| D41 | **Fuentes intercambiables** (M12, `PM/` §5.2): contratos en `F/features/warehouse/contracts/` (`clock.ts`, `reception.ts`, `forklift.ts`, `inventory.ts`, `novelty.ts`) y `F/features/administration/contracts/alert-threshold.ts`, más las extensiones de `F/features/exits/contracts/exit.ts` y `F/features/foreign-trade/contracts/deposit-entry.ts`; fuentes `reception`, `forklift`, `inventory` y `novelty` en `F/features/warehouse/services/` y `alert-threshold` en `F/features/administration/services/`. Lo integrado de F01 y F03 que las pantallas usan (ubicaciones con su alta, cuadrillas, conductores con su alta, terceros con su alta rápida, productos, embalajes, tipos de documento y tipos de vehículo) se simula con la fachada `F/features/warehouse/services/catalog.source.ts`, como `P03/` D40: las pantallas nuevas no importan fuentes de `INTEGRATED_SOURCES` (`FT/unit/guards/mock-sources.spec.ts:22`) ni componentes de hoy que llaman al API. I-04 la borra | M12; `P03/` D40 |
| D42 | **Inventario con el patrón** (`P02/` D3): tres pestañas (`Tabs`), cada una con su `AppDataTable`. **Existencias:** tarjeta de filtro global con el depósito (`WarehouseDepositSelect`) y la tabla de sus productos, completa y con orden y filtros en el navegador (C-F01-148), con «Ubicaciones» (`ProductPlacementsDialog`) y «Registrar novedad» (`NoveltyFormDialog`). **Movimientos:** paginado con orden y filtros por columna en el servidor (C-F04-26) y «Exportar» (todo, `all=true`). **Ubicaciones:** las ubicaciones (C-F04-14) con su contenido en drawer (`LocationContentPanel`, C-F04-29). Salen las tarjetas de estadísticas y el aviso de alertas de stock, que nunca cargan (`F/features/warehouse/composables/useInventoryStatistics.ts`: `enabled: false`) | AF-129; `P02/` D3 |
| D43 | **Novedades con el patrón:** paginado con orden y filtros por columna en el servidor (C-F04-30: depósito, producto, camión, tipo, rango de fechas; «Incluir anuladas» en la tarjeta de filtros); acciones «Editar», «Imprimir» y «Anular» (rojo, al final); «+ Nueva novedad» y «Exportar» en la barra; el paso de elegir depósito se conserva. `NoveltyFormDialog` pasa a dos columnas con sus campos de hoy (`A/` §3.3, tabla de modales grandes) | AF-129, AF-130; `P02/` D3 |
| D44 | **Tablero de Bodega** (`/warehouse`, `OUTSIDE`): I-04 cambia sus tarjetas (`F/pages/warehouse/index.vue:13-55`): sale «Ingresos»; «Recepción» e «Historial de recepciones» apuntan a Entradas; «Registrar uso» e «Historial» de montacargas pasan a una tarjeta «Montacargas»; «Órdenes de cargue» se queda hasta F06 | AF-64 |
| D45 | **Menú** (I-04; `F/components/layout/menu-model.ts:60-88` y `:201-208`): Bodega queda Dashboard · Entradas ▸ Recepción, Historial · Montacargas · Órdenes de cargue (hasta que F06 la reemplace por «Salidas») · Inventario · Novedades; Administración queda Usuarios · Auditoría · Umbrales de alertas. «Entradas» es un grupo, como P-TR-01 y AF-64 | AF-64, AF-127; P-TR-01 |
| D46 | **Lo que se borra en I-04** (§13.3), después de comprobar con grep quién importa cada archivo. `BillingCollectForm` y `useUnitMeasures` **no** se borran: F04 no es su último uso (los usan `F/features/foreign-trade/components/DispatchGuideForm.vue`, de F06, y `F/features/foreign-trade/components/DepositProductDialog.vue`, de F05) | `P03/` D42; trampa 7 |
| D47 | **Permisos** (`B/Wms.Domain/Security/WmsPolicyRoles.cs`): una política nueva, `LocationCreateAccess` (D12). Todo lo demás conserva su política (§2.1). Las páginas de Bodega siguen con Admin y Warehouse; Umbrales, solo Admin. Ninguna política pierde un rol (`DEC-005`) | `DEC-005`; `PM/` §5.6 |

### 1.6 Destino de las 13 AF dueñas

| AF | Decisiones | Fase |
| --- | --- | --- |
| AF-56 | D31, D35 | BE-1; FE-1 (reloj de Recepción) |
| AF-57 | D1, D6, D11, D32, D33, D35, D36 | BE-1; FE-1 (colores), FE-2 (P-TR-08) |
| AF-58 | D14, D16 (AF-65 la reduce a «recepción por entrada») | BE-2; FE-1 |
| AF-59 | D24, D38 (P-BOD-02 a dos columnas) | BE-2, BE-3; FE-1, FE-2 |
| AF-60 | D18 | BE-2; FE-1 |
| AF-61 | D16, D21 | BE-2; FE-1 |
| AF-62 | D17 | BE-2; FE-1 |
| AF-63 | D26 | BE-3; FE-2 |
| AF-64 | D5, D7, D8, D9, D20, D22, D28, D44, D45 (lo de las salidas es de F06: «Órdenes de salida», «Salidas» y P-BOD-06 a P-BOD-09) | BE-2, BE-3; FE-1, FE-2; I-04 |
| AF-65 | D14, D15, D31 | BE-1, BE-2; FE-1 |
| AF-69 | D20 | BE-2; FE-1 |
| AF-105 | D2, D3, D25, D29, D30 | BE-3; FE-2 |
| AF-119 | D4, D19 | BE-2; FE-1 |

Las 13 tienen decisión y fase (verificado con un script contra la lista de `PM/` §3.1). La fórmula que usa «Queda sobre el vehículo» es de F07 (AF-116, AF-120) y las columnas de «Requiere factura» en Facturación son de F08 (P-FAC-02).

### 1.7 AF de otras features que F04 muestra o aplica

| AF | Feature dueña | Qué muestra o aplica F04 | Pantalla |
| --- | --- | --- | --- |
| AF-14, AF-31 | F01 | Bodega no frena a Báscula: la entrada aparece en Recepción desde el primer peso y el repesaje no la espera | P-BOD-01 |
| AF-17 | F01 | Inspección con documento y productos opcionales y descripción obligatoria | P-BOD-03 |
| AF-18 | F01 | Conductores con el mismo documento: el selector muestra nombre y documento (`DriverQuickDialog`) | P-BOD-03 |
| AF-21 | F01 | El tipo de vehículo sale de Báscula; Bodega lo registra | P-BOD-02, P-BOD-03, P-BOD-04 |
| AF-22 | F01 | Mercancía sin unidad de medida (embalaje en el texto) | P-BOD-01 a P-BOD-03, Inventario |
| AF-36, AF-68 | F01 | La guía nace al confirmar la salida: arranca el reloj del cargue y de la salida de patio | Relojes (para F06) |
| AF-44 | F01 | La entrada como unidad de recepción: una fila por entrada | P-BOD-01 |
| AF-66, AF-70 | F01 | Cargue y salida de patio: detienen sus relojes | Relojes (para F06) |
| AF-101 | F01 | Transportadora por entrada | P-BOD-02 (lectura), P-BOD-03 (obligatoria) |
| AF-54 | F02 | «+» de alta rápida: conductor y transportadora en P-BOD-03, tercero en el cobro | P-BOD-03, P-BOD-04 |
| AF-99, AF-129, AF-130 | F02 | Filtros por columna, orden, botones con borde, patrón de listado y detalle en drawer | P-BOD-01, P-BOD-05, Historial, Inventario, Novedades |
| AF-127, AF-128 | F02 | Menú de P-TR-01 y roles; Umbrales solo para Admin | Menú, P-TR-08 |
| AF-131, AF-132 | F02 | Etiquetas encima; cobro con método y referencia, sin nota | Todas; P-BOD-04 |

---

## 2. Contrato (parte 0)

Es la única fuente del frontend para lo que F04 crea, cambia o retira (`PM/` R3). Los endpoints de F01 y F03 que F04 consume sin cambios se citan por su ID (`P01/` §2.2 y §2.3; `P03/` §2.2 y §2.3). Los endpoints de hoy que no estaban en ningún contrato y que las pantallas de F04 usan llevan aquí su ID, marcados «sin cambios».

### 2.0 Convenciones

- Rige `P01/` §2.0: base `/api/v1`, JWT, camelCase, enums como texto, fechas ISO 8601 con zona, `{ data, pagination }`, `pageSize` de 1 a 50 con `all=true`, *ProblemDetails* con `description` y `errors[]`, motivos de 10 a 500 caracteres y **C-F01-00** (orden y filtros por columna, con su lista blanca y sus mensajes) en los listados marcados «orden y filtros».
- **Registro vigilado** (`WatchedRecord`): `Reception` | `Loading` | `YardExit`; rótulos «Recepción», «Cargue» y «Salida de patio». **Nivel del reloj** (`ClockLevel`): `None` | `Yellow` | `Red`.
- **Tipo de vehículo:** el del vehículo es `VehicleType` (`Tractomula`, `DobleTroque`, `Sencillo`, `Turbo`, `VehParticular`, `Otro`; `B/Wms.Domain/Enums/VehicleType.cs`); el de la tarifa del montacargas es `ForkliftVehicleType` (`Tractomula`, `DobleTroque`, `Sencillo`, `Turbo`, `GuacalEstiba`; `B/Wms.Domain/Enums/ForkliftVehicleType.cs`). D26 los relaciona.
- **Identificadores:** `C-F04-mm` y `QA2-F04-nnn` (`PM/` §5.1).
- **Política nueva:** `LocationCreateAccess` (Admin, ForeignTrade, Billing, Warehouse), solo en C-F04-15 (D12). Las demás son las de hoy (`B/Wms.Domain/Security/WmsPolicyRoles.cs`): `WarehouseAccess` (Admin, Warehouse) en `WarehouseController` (`B/Wms.Api/Controllers/v1/WarehouseController.cs:54`), `AdminOnly`, `ExitAccess`, `ForeignTradeAccess`, `LocationReadAccess`, `ConfigurationAccess`, `NoveltyReadAccess` y `ActiveUser`.
- **Verificado contra `fase-2`:** las fichas de F01 y F03 que F04 consume se cotejaron con el código (política, DTO y mensajes). Diferencias, que gana lo integrado: C-F01-44 dice que Bodega crea posiciones con un endpoint de `WarehousePlacementsController` que no existe (D12 lo resuelve con C-F04-15); C-F01-24 lista a F04 como consumidor, pero `PATCH vehicles/{id}` no admite a Bodega (`VehicleConfigurationAccess`): el tipo de vehículo lo guardan los comandos de F04 (D17, D20, D26).

### 2.1 Índice

**Grupo A — Umbrales y relojes** (backend, fase BE-1).

| ID | Endpoint | Cambio | Política | Pantalla |
| --- | --- | --- | --- | --- |
| C-F04-01 | `GET administration/alert-thresholds` | nuevo | `AdminOnly` | P-TR-08 |
| C-F04-02 | `PUT administration/alert-thresholds` | nuevo | `AdminOnly` | P-TR-08 |
| C-F04-03 | `GET exits` | modificado (sobre C-F01-94): `warehouseClock` y filtro `warehouseLevel` | `ExitAccess` | F06 (P-BOD-06, P-BOD-09) |
| C-F04-04 | `GET exits/{id}` | modificado (sobre C-F01-95): `warehouseClock` | `ExitAccess` | F06 (P-BOD-07, P-BOD-08) |
| C-F04-05 | `GET foreign-trade/warehouse-storages/{warehouseStorageId}/entries` | modificado (sobre C-F01-85): `reception` con su reloj | `ForeignTradeAccess` | F05 (etapa Bodega) |

**Grupo B — Recepción** (backend, fase BE-2).

| ID | Endpoint | Cambio | Política | Pantalla |
| --- | --- | --- | --- | --- |
| C-F04-06 | `GET warehouse/pending-from-weighbridge` | modificado (sobre C-F01-149): una fila por entrada con primer peso, reloj, orden y filtros | `WarehouseAccess` | P-BOD-01, P-BOD-02 |
| C-F04-07 | `POST warehouse/receptions` | modificado: recibe la entrada sin llegada; tipo de vehículo, «sobre el vehículo», ubicación obligatoria, cuadrilla en la recepción | `WarehouseAccess` | P-BOD-02 |
| C-F04-08 | `POST warehouse/receptions/without-weighbridge` | modificado: campos de MK-09, siempre inspección | `WarehouseAccess` | P-BOD-03 |
| C-F04-09 | `GET warehouse/receptions` | modificado (sobre C-F01-151): historial, orden y filtros | `WarehouseAccess` | Historial de recepciones |
| C-F04-10 | `GET warehouse/receptions/{id}` | modificado: cuadrilla, tipo de vehículo, «sobre el vehículo» y tiempo | `WarehouseAccess` | Drawer del historial |
| C-F04-11 | `POST warehouse/receptions/register-arrival` | retirado (AF-65) | — | — |
| C-F04-12 | `POST warehouse/receptions/{id}/complete` | retirado (AF-65) | — | — |
| C-F04-13 | `GET warehouse/search/plate/{plate}` | modificado (sobre C-F01-150): sin llegada; tipo de vehículo y servicio por depósito | `WarehouseAccess` | P-BOD-04 («+ Registrar uso») |
| C-F04-14 | `GET warehouse/locations` | modificado (sobre C-F01-43): `isSystem` | `LocationReadAccess` | P-BOD-02, P-BOD-03, Inventario, Configuración › Ubicaciones |
| C-F04-15 | `POST warehouse/locations` | modificado (sobre C-F01-44): política `LocationCreateAccess` | `LocationCreateAccess` | P-BOD-02, P-BOD-03 (D21) |
| C-F04-16 | `PATCH` y `DELETE warehouse/locations/{id}` | modificado (sobre C-F01-45 y C-F01-46): 409 con la ubicación del sistema | `ConfigurationAccess` | Configuración › Ubicaciones |
| C-F04-17 | `GET weighbridge/vehicle-types` | sin cambios | `ActiveUser` | P-BOD-02, P-BOD-03 |

**Grupo C — Montacargas** (backend, fase BE-3).

| ID | Endpoint | Cambio | Política | Pantalla |
| --- | --- | --- | --- | --- |
| C-F04-18 | `GET warehouse/forklift-uses` | modificado: orden y filtros; «Requiere factura», «Pagado» y «Facturado» | `WarehouseAccess` | Montacargas (P-BOD-05) |
| C-F04-19 | `GET warehouse/forklift-uses/{id}` | modificado: la misma forma de C-F04-18 | `WarehouseAccess` | Drawer de Montacargas |
| C-F04-20 | `POST warehouse/forklift-uses/start` | modificado: sin modo de pago; tipo al vehículo (D26) | `WarehouseAccess` | P-BOD-04 |
| C-F04-21 | `POST warehouse/forklift-uses/{id}/end` | modificado: `requiresInvoice` (D25) | `WarehouseAccess` | P-BOD-04 |
| C-F04-22 | `GET warehouse/forklift-uses/active` | retirado (D29) | — | — |
| C-F04-23 | `PATCH warehouse/forklift-uses/{id}/payment-mode` | retirado (D29) | — | — |
| C-F04-24 | `GET warehouse/forklift-rate` | sin cambios | `WarehouseAccess` | P-BOD-04 |
| C-F04-25 | `GET forklift-rates/vehicle-types` | sin cambios | autenticado | P-BOD-04 |

**Grupo D — Inventario y novedades** (backend, fase BE-3).

| ID | Endpoint | Cambio | Política | Pantalla |
| --- | --- | --- | --- | --- |
| C-F04-26 | `GET warehouse/inventory/movements` | modificado (sobre C-F01-147): orden y filtros (C-F01-00) | `WarehouseAccess` | Inventario › Movimientos |
| C-F04-27 | `GET warehouse/inventory/deposits` | sin cambios | `WarehouseAccess` | Inventario › Existencias, Novedades |
| C-F04-28 | `GET` y `POST warehouse/storage-products/{id}/placements`, `POST …/placements/move`, `POST …/placements/release` | sin cambios | `WarehouseAccess` | Inventario (`ProductPlacementsDialog`) |
| C-F04-29 | `GET warehouse/locations/{id}/placements` | sin cambios | `WarehouseAccess` | Inventario › Ubicaciones |
| C-F04-30 | `GET warehouse/novelties` | modificado: orden y filtros (C-F01-00) | `NoveltyReadAccess` | Novedades |
| C-F04-31 | `GET warehouse/novelties/{id}`, `GET …/{id}/pdf`, `POST warehouse/novelties`, `PUT …/{id}`, `POST …/{id}/void` | sin cambios | `NoveltyReadAccess` (lecturas), `WarehouseAccess` (escrituras) | Novedades, Inventario |

**Consumidos de F01 y F03 sin cambios:** C-F01-15 y C-F01-17 (conductores y su alta), C-F01-25, C-F01-26 y C-F01-141 (terceros y alta rápida), C-F01-29 (embalajes), C-F01-52 (cuadrillas), C-F01-69 (productos), C-F01-146 (unidades de carga del depósito), C-F01-148 (existencias del depósito), C-F01-152 (ingresos para la recepción directa) y C-F03-44 (tipos de documento). Sus fichas y esquemas están en `P01/` §2.2 y §2.3 y `P03/` §2.2 y §2.3; se verificaron contra `fase-2` (§2.0).

### 2.2 Fichas

#### Grupo A — Umbrales y relojes

##### C-F04-01 · `GET administration/alert-thresholds` (nuevo)
- **Política:** `AdminOnly`. Controlador nuevo `B/Wms.Api/Controllers/v1/AlertThresholdsController.cs` (ruta `administration`).
- **Petición:** sin parámetros.
- **Respuesta 200:** `dataSchema(z.array(alertThresholdSchema))`, siempre las tres filas, en el orden `Reception`, `Loading`, `YardExit`:

```jsonc
{ "data": [
  { "watchedRecord": "Reception", "yellowMinutes": null, "redMinutes": null, "updatedAt": null },
  { "watchedRecord": "Loading",   "yellowMinutes": 45,   "redMinutes": 90,   "updatedAt": "2026-11-26T09:12:00-05:00" },
  { "watchedRecord": "YardExit",  "yellowMinutes": 30,   "redMinutes": 60,   "updatedAt": "2026-11-26T09:12:00-05:00" }
] }
```

- **Errores:** 403 sin el rol Admin. **Zod:** `alertThresholdSchema`.

##### C-F04-02 · `PUT administration/alert-thresholds` (nuevo)
- **Política:** `AdminOnly`.
- **Petición:** `alertThresholdsUpdateSchema`.

| Campo | Tipo | Obligatorio | Regla |
| --- | --- | --- | --- |
| `thresholds` | arreglo de 3 | Sí | Cada registro vigilado una vez |
| `thresholds[].watchedRecord` | `WatchedRecord` | Sí | — |
| `thresholds[].yellowMinutes`, `thresholds[].redMinutes` | entero o nulo | Sí (los dos o ninguno) | De 1 a 10.080; amarillo < rojo (D33) |

- **Efecto:** guarda las tres filas (auditadas). La vuelta siguiente del trabajo usa los valores nuevos (D35).
- **Respuesta 200:** la de C-F04-01.
- **Errores:** 400 «Envíe los tres registros vigilados, cada uno una vez.»; 400 «{registro}: indique los dos umbrales o ninguno.»; 400 «{registro}: el umbral amarillo debe ser menor que el rojo.»; 400 «{registro}: los umbrales van de 1 a 10.080 minutos.» ({registro} = «Recepción», «Cargue» o «Salida de patio»). **Zod:** `alertThresholdsUpdateSchema`, `alertThresholdSchema`.

##### C-F04-03 · `GET exits` (modificado sobre C-F01-94)
- **Política:** `ExitAccess` (hoy, `B/Wms.Api/Controllers/v1/ExitsController.cs:26-27`).
- **Qué cambia:** cada fila suma `warehouseClock` (`warehouseClockSchema` o nulo): nulo en Borrador y Cancelada; en Confirmada corre (`Loading` en `Deposit` y `Consolidated`, `YardExit` en `EntryTicket` y `Global`, D31); en Completada queda detenido con su nivel. Filtro nuevo `warehouseLevel` (enum, uno o varios: solo salidas con el reloj corriendo en ese nivel). El orden y los demás filtros no cambian (`confirmedAt asc` ordena por el reloj).
- **Petición (query):** la de C-F01-94, más `warehouseLevel` (enum, varios).
- **Respuesta 200:** `pagedSchema(exitListItemSchema)`, con el campo de §2.3.
- **Errores:** los de C-F01-00. **Zod:** `exitListItemSchema`, `exitListQuerySchema` (extendidos).
- **Notas:** lo maqueta F06. Órdenes de salida = `status=Confirmed&missing=Loading,YardExit&sortField=confirmedAt&sortOrder=asc` (`P01/` C-F01-94).

##### C-F04-04 · `GET exits/{id}` (modificado sobre C-F01-95)
- **Política:** `ExitAccess`. **Petición:** el Id en la ruta. **Qué cambia:** suma `warehouseClock`, con la regla de C-F04-03. **Respuesta 200:** `dataSchema(exitSchema)`. **Errores:** los de hoy (404 «La salida no existe.»). **Zod:** `exitSchema` (extendido). Lo maqueta F06. `GET exits/by-plate/{plate}` (C-F01-101) devuelve el mismo DTO: también trae el campo, y su esquema lo acepta.

##### C-F04-05 · `GET foreign-trade/warehouse-storages/{warehouseStorageId}/entries` (modificado sobre C-F01-85)
- **Política:** `ForeignTradeAccess` (la de hoy, `B/Wms.Api/Controllers/v1/ForeignTradeController.cs:53`, `:538`).
- **Petición:** la de hoy (el Id del depósito en la ruta). **Respuesta 200:** `dataSchema(z.array(depositEntryWithReceptionSchema))`.
- **Qué cambia:** cada entrada suma `reception`; nulo si la entrada está anulada:

```jsonc
"reception": {
  "status": "Pending",              // Pending | Received
  "receptionLogId": null,
  "receivedAt": null,
  "receivedByName": null,
  "staysOnVehicle": null,           // true o false cuando está recibida
  "clock": {                        // nulo si la entrada aún no tiene su primer peso
    "watchedRecord": "Reception", "startedAt": "2026-11-26T08:10:00-05:00", "stoppedAt": null,
    "elapsedMinutes": 42, "level": "Yellow", "yellowMinutes": 30, "redMinutes": 60
  }
}
```

- **Errores:** los de hoy. **Zod:** `depositEntryWithReceptionSchema` (§2.3). Lo maqueta F05.
- **Notas:** el DTO (`B/Wms.Application/ForeignTrade/Common/DTOs/DepositStorageEntryDto.cs`) es el mismo de C-F03-13 (`GET weighbridge/entries/{entryId}`), que también traerá el campo; `depositEntrySchema` no cambia (Zod descarta las claves que no declara), así que la pantalla de Báscula no se toca.

#### Grupo B — Recepción

##### C-F04-06 · `GET warehouse/pending-from-weighbridge` (modificado sobre C-F01-149)
- **Política:** `WarehouseAccess` (hoy, `B/Wms.Api/Controllers/v1/WarehouseController.cs:376`).
- **Qué cambia:** las entradas de D14 (con o sin ciclo), una fila por entrada, con la forma de `pendingReceptionItemSchema` y su reloj; orden y filtros (C-F01-00). Salen `weighbridgeCycleId`, `entryWeight`, `entryWeightType`, `entryCapturedAt`, `documentQuantity`, `cycleQuantity` y `status` (`B/Wms.Application/Warehouse/Common/DTOs/PendingFromWeighbridgeDto.cs`).
- **Petición (query), orden y filtros (C-F01-00):** `vehiclePlate` (texto; conserva su nombre), `warehouseStorageNumber` (texto), `customerName` (texto), `merchandise` (texto: producto o descripción), `weighedAtFrom`, `weighedAtTo`, `level` (enum, varios), más paginación.
- **Orden:** lista blanca `weighedAt`, `vehiclePlate`, `warehouseStorageNumber`, `customerName`; por defecto `weighedAt asc`.
- **Respuesta 200:** `pagedSchema(pendingReceptionItemSchema)`:

```jsonc
{
  "warehouseStorageEntryId": "guid", "entryLogId": "guid", "serviceRecordId": "guid",
  "warehouseStorageId": "guid", "warehouseStorageNumber": "2026BA00012",
  "weighedAt": "2026-11-10T21:40:00-05:00",
  "vehicleId": "guid", "vehiclePlate": "ABC123", "vehicleType": "Tractomula",
  "driver": { "fullName": "Conductor 1", "idType": "Cc", "idNumber": "1000001" },
  "carrierCompanyName": "Transportes Ejemplo",
  "customerId": "guid", "customerName": "Cliente A",
  "merchandiseText": "Cebolla · Sacos",
  "declaredQuantity": 600,
  "manifestNumber": "M-001", "manifestWeight": 18000, "merchandiseWeight": 18000,
  "usesCargoUnits": false,
  "forkliftInProgress": false,
  "products": [{ "warehouseStorageProductId": "guid", "productName": "Cebolla", "productDescription": null,
                 "packaging": "Sacos", "entryDeclaredQuantity": 600, "currentStock": 600 }],
  "clock": { "watchedRecord": "Reception", "startedAt": "2026-11-10T21:40:00-05:00", "stoppedAt": null,
             "elapsedMinutes": 70, "level": "Red", "yellowMinutes": 30, "redMinutes": 60 }
}
```

- **Errores:** los de C-F01-00 (orden y valores de `level`). **Zod:** `pendingReceptionQuerySchema`, `pendingReceptionItemSchema`.
- **Notas:** P-BOD-02 usa la fila elegida; con `usesCargoUnits`, las unidades vienen de C-F01-146. `merchandiseWeight` es el «Peso físico neto» del modal (`P01/` D21). `customerName` nulo se muestra «Sin cliente».

##### C-F04-07 · `POST warehouse/receptions` (modificado)
- **Política:** `WarehouseAccess`. El receptor sale del token (CHG-72).
- **Qué cambia:** recibe una entrada de D14 en un solo paso (D16), sin llegada. La petición ya no lleva `entryLogId` (lo da la entrada) y suma `vehicleType`, `staysOnVehicle` y la ubicación obligatoria.
- **Petición:** `receptionCreateSchema`.

| Campo | Tipo | Obligatorio | Regla |
| --- | --- | --- | --- |
| `warehouseStorageEntryId` | guid | Sí | Entrada de D14 |
| `vehicleType` | `VehicleType` o nulo | No | Se guarda en el vehículo (D17) |
| `staysOnVehicle` | boolean | Sí | Con `true`, todo va a `SOBRE-VEHICULO` y las ubicaciones enviadas se ignoran (D19) |
| `products[]` | arreglo | Sí, salvo con unidades de carga | Solo cantidades > 0 |
| `products[].warehouseStorageProductId` | guid | Sí | Producto de la entrada |
| `products[].unloadedQuantity` | número > 0 | Sí | No mayor que lo declarado para el camión |
| `products[].warehouseLocationId` | guid o nulo | Sí, salvo `staysOnVehicle` | Ubicación habilitada (AF-61) |
| `receivedCargoUnitIds` | guid[] o nulo | Sí con unidades de carga | Todas las del camión (como hoy) |
| `crewId` | guid o nulo | No | Cuadrilla activa (D18) |
| `comments` | texto ≤ 500 o nulo | No | «Observaciones de la carga» |
| `signatureDriver` | texto (imagen en base64) o nulo | Como hoy | — |
| `photos[]` | `{ base64Data, title, description }` | No | Hasta 5 (`PhotoUploadRules`) |

- **Respuesta 201:** `dataSchema(receptionResultSchema)`.
- **Errores:** 404 «La entrada no existe.»; 409 «La entrada de {placa} en el depósito {N} ya fue recibida.»; 409 «La entrada está anulada: no se recibe.»; 400 «La entrada de {placa} aún no tiene su primer peso.»; 400 «Elija la ubicación de {producto}.»; 400 «{producto}: la cantidad descargada ({q}) supera lo declarado para este camión ({d}).»; 400 «El tipo de vehículo «{valor}» no es válido.»; y los de hoy: depósito cerrado o anulado («No se puede completar la recepción en un depósito en estado {estado}.», `CompleteReceptionCommandHandler.cs:73-78`), productos ajenos al depósito (`ReceptionHelper.ValidateProductsBelongToStorage`), unidades de carga (`ReceptionCargoUnits`), «Debe indicar al menos un producto con cantidad a descargar.», ubicación inexistente (404 «La ubicación de bodega {Id} no existe.»), cuadrilla (`CrewRules`), fotos («Se permiten máximo 5 fotos por recepción.»).
- **Efecto:** `ReceptionLog` completada con sus productos, firma, fotos, cuadrilla y la marca; ubicación de lo descargado (D16, D19); cuadrilla también en el depósito (D18); tipo en el vehículo (D17); aviso de diferencia a CE como hoy. La entrada sale de C-F04-06 y su reloj se detiene.
- **Zod:** `receptionCreateSchema`, `receptionResultSchema`.

##### C-F04-08 · `POST warehouse/receptions/without-weighbridge` (modificado)
- **Política:** `WarehouseAccess`. El autor sale del token (hoy, `WarehouseController.cs:337-338`).
- **Qué cambia:** los campos de MK-09 y P-BOD-03 (D20); salen `driverFirstName` y demás datos sueltos del conductor, `operationModalityCode`, `cargoManifestNumber`, cliente, importador, agencia, `documents`, moneda, valor, `shippingFormNumber`, manifiesto, `warehouseLocationId` general y `manualEntryReason` (`B/Wms.Application/Warehouse/Commands/Reception/CreateReceptionWithoutWeighbridgeCommand.cs`).
- **Petición:** `directReceptionCreateSchema`.

| Campo | Tipo | Obligatorio | Regla |
| --- | --- | --- | --- |
| `entryLogId` | guid | Sí | Ingreso elegible de Vigilancia (C-F01-152; `DirectReceptionEntryRules`) |
| `driverId` | guid | Sí | Conductor existente (alta con C-F01-17); pasa al ingreso |
| `carrierCompanyId` | guid | Sí | Tercero con rol `TRANSPORT_COMPANY` (`P01/` D26) |
| `vehicleCountry` | texto o nulo | No | Se guarda en el vehículo |
| `vehicleType` | `VehicleType` o nulo | No | Se guarda en el vehículo |
| `documentTypeId`, `documentNumber` | guid y texto (1 a 50), o nulos | No; juntos | Tipo «Carta porte» o «Guía de transporte» (C-F03-44) |
| `inspectionDescription` | texto | Sí | 10 a 500 (`P01/` D23) |
| `staysOnVehicle` | boolean | Sí | Como en C-F04-07 |
| `products[]` | arreglo | No | Mercancía declarada |
| `products[].productId`, `packagingTypeId`, `productDescription` | guid, guid o nulo, texto ≤ 500 o nulo | Producto sí | Catálogo (C-F01-69, C-F01-29) |
| `products[].declaredQuantity`, `unloadedQuantity` | números > 0 | Sí | Descargado ≤ declarado |
| `products[].warehouseLocationId` | guid o nulo | Sí, salvo `staysOnVehicle` | AF-61 |
| `crewId`, `comments`, `signatureDriver`, `photos[]` | como C-F04-07 | Como C-F04-07 | — |

- **Respuesta 201:** `dataSchema(receptionResultSchema)` (con el depósito nuevo en `warehouseStorageId` y `warehouseStorageNumber`).
- **Errores:** 404 «El ingreso no existe.»; los de elegibilidad de hoy (`DirectReceptionEntryRules.cs`: 409 ingreso con salida, 400 sin motivo, 400 motivo con pesaje, 409 con recepción); 404 «El conductor no existe.»; 400 «Elija la empresa de transporte.»; 400 «La empresa de transporte no es válida.»; 400 «Indique la descripción de la inspección (10 a 500 caracteres).»; 400 «Indique el tipo y el número del documento, o ninguno.»; 400 «El documento debe ser carta porte o guía de transporte.»; 400 «{producto}: la cantidad descargada ({q}) supera la declarada ({d}).»; 400 «Elija la ubicación de {producto}.»; y los de fotos, cuadrilla y ubicación de C-F04-07.
- **Efecto:** servicio de inspección (modalidad «INSP») y depósito nuevo en Borrador, sin cliente ni valor, con la descripción y el documento; la entrada con su transportadora y el conductor; los productos declarados; la recepción completada con lo descargado; el vehículo con país y tipo. CE lo ve como hoy (`A/` §2.2 i).
- **Zod:** `directReceptionCreateSchema`, `receptionResultSchema`.

##### C-F04-09 · `GET warehouse/receptions` (modificado sobre C-F01-151)
- **Política:** `WarehouseAccess`.
- **Qué cambia:** es el historial: solo recepciones completadas (de báscula y directas); sale el filtro `status`; orden y filtros (C-F01-00); fila de `receptionListItemSchema`.
- **Petición (query):** `receivedAtFrom`, `receivedAtTo`, `vehiclePlate`, `warehouseStorageNumber`, `customerName`, `merchandise` (texto), `kind` (`Weighbridge` | `Direct`, uno o varios), más paginación. **Orden:** lista blanca `receivedAt`, `vehiclePlate`, `warehouseStorageNumber`, `customerName`; por defecto `receivedAt desc`.
- **Respuesta 200:** `pagedSchema(receptionListItemSchema)`. **Errores:** los de C-F01-00. **Zod:** `receptionListQuerySchema`, `receptionListItemSchema`.

##### C-F04-10 · `GET warehouse/receptions/{id}` (modificado)
- **Política:** `WarehouseAccess`. **Petición:** el Id en la ruta. **Qué cambia:** suma `kind`, `vehicleType`, `staysOnVehicle`, `crewName`, `receivedByName`, `weighedAt` y `elapsedMinutes` (del primer peso a la recepción; nulo en las directas); sale `arrivalAt`. **Respuesta 200:** `dataSchema(receptionDetailSchema)`. **Errores:** 404 «La recepción no existe.» (hoy). **Zod:** `receptionDetailSchema`.

##### C-F04-11 y C-F04-12 · `POST warehouse/receptions/register-arrival` y `POST warehouse/receptions/{id}/complete` (retirados)
Responden 404. Los reemplaza C-F04-07 (D9, D15). Solo los llamaban `F/pages/warehouse/receptions/entry.vue` y `index.vue`.

##### C-F04-13 · `GET warehouse/search/plate/{plate}` (modificado sobre C-F01-150)
- **Política:** `WarehouseAccess`. **Petición:** la placa en la ruta (se normaliza como hoy). **Qué cambia:** encuentra el camión en planta con entradas de D14 o ya recibidas; salen `hasInProgressReception`, `inProgressReceptionId` y `arrivalAt` (del camión y de cada depósito, `B/Wms.Application/Warehouse/Common/DTOs/PlateSearchResultDto.cs:28-32`, `:59-61`); suman `vehicleType` y, por depósito, `serviceRecordId` y `forkliftInProgress`. **Respuesta 200:** `dataSchema(plateSearchSchema)`. **Errores:** los de hoy. **Zod:** `plateSearchSchema`. **Notas:** lo usa «+ Registrar uso» para elegir el depósito del camión (D27).

##### C-F04-14 · `GET warehouse/locations` (modificado sobre C-F01-43)
- **Política:** `LocationReadAccess` (hoy). **Petición:** `isAvailable` (opcional), como hoy. **Qué cambia:** cada ubicación suma `isSystem` (verdadero solo en `SOBRE-VEHICULO`, D19). **Respuesta 200:** `dataSchema(z.array(locationSchema))`. **Errores:** ninguno. **Zod:** `locationSchema` (extendido en `F/features/warehouse/contracts/location.ts`). **Notas:** la recepción no ofrece `SOBRE-VEHICULO` en el selector (la usa el interruptor); Configuración › Ubicaciones la muestra sin acciones.

##### C-F04-15 · `POST warehouse/locations` (modificado sobre C-F01-44)
- **Política:** `LocationCreateAccess` (antes `ConfigurationAccess`; suma Warehouse, D12). **Petición:** `locationCreateSchema` (la de C-F01-44: `code`, `name`, `capacity`, `aisle`, `rack`, `level`). **Respuesta 201:** `dataSchema(locationSchema)`. **Errores:** los de C-F01-44 (`B/Wms.Application/Warehouse/Commands/Location/CreateWarehouseLocation/CreateWarehouseLocationValidator.cs`) y 403 sin la política. **Zod:** `locationCreateSchema`, `locationSchema`.

##### C-F04-16 · `PATCH` y `DELETE warehouse/locations/{id}` (modificados sobre C-F01-45 y C-F01-46)
- **Política:** `ConfigurationAccess` (hoy). **Petición:** la de C-F01-45 (`locationUpdateSchema`) y la de C-F01-46 (el Id, sin cuerpo). **Qué cambia:** con `SOBRE-VEHICULO` responden 409 «La ubicación «Sobre vehículo» es del sistema: no se modifica ni se borra.». **Respuesta 200:** `dataSchema(locationSchema)` (PATCH) y `dataSchema(z.null())` (DELETE), como hoy. **Errores:** los de C-F01-45 y C-F01-46 y el 409 de arriba. **Zod:** `locationUpdateSchema`, `locationSchema`.

##### C-F04-17 · `GET weighbridge/vehicle-types` (sin cambios)
- **Política:** `ActiveUser` (`B/Wms.Api/Controllers/v1/WeighbridgeCatalogController.cs:34`). **Petición:** sin parámetros. **Respuesta 200:** `dataSchema(z.array(vehicleTypeItemSchema))` = `[{ "value": "Tractomula", "label": "Tractomula" }, …]`. **Errores:** ninguno. **Zod:** `vehicleTypeItemSchema`.

#### Grupo C — Montacargas

##### C-F04-18 · `GET warehouse/forklift-uses` (modificado)
- **Política:** `WarehouseAccess` (hoy, `WarehouseController.cs:430`).
- **Qué cambia:** orden y filtros (C-F01-00); `fromDate` y `toDate` pasan a `dateInitFrom` y `dateInitTo`; `status` admite varios; la fila es `forkliftUseSchema`, que deja de traer el detalle de la factura (`subTotal`, `taxAmount`, `total`, `invoiceId`, `invoiceNumber`, `paymentMode`, `applyVat`) y suma `requiresInvoice`, `paidAmount` e `invoiced` (D28).
- **Petición (query):** `status` (`InProgress`, `Ended`, `Complete`; varios), `vehiclePlate`, `customerName`, `vehicleType` (varios), `dateInitFrom`, `dateInitTo`, `stakeholderId` (se conserva), más paginación. **Orden:** lista blanca `dateInit`, `dateEnd`, `vehiclePlate`, `customerName`; por defecto `dateInit desc`.
- **Respuesta 200:** `pagedSchema(forkliftUseSchema)`:

```jsonc
{
  "id": "guid", "serviceRecordId": "guid", "entryLogId": "guid", "warehouseStorageNumber": "2026BA00012",
  "vehiclePlate": "ABC123", "vehicleType": "Tractomula", "vehicleTypeLabel": "Tractomula",
  "customerId": "guid", "customerName": "Cliente A", "driverName": "Conductor 1",
  "initHourmeter": 1234.5, "endHourmeter": 1236.0, "dateInit": "…", "dateEnd": "…", "hoursUsed": 1.5,
  "status": "Complete", "comments": null,
  "requiresInvoice": false,   // nulo mientras está en curso
  "paidAmount": 220000,       // lo pagado de la factura del uso; nulo en curso
  "invoiced": false           // la factura ya tiene N.º SIGO; nulo en curso
}
```

- **Errores:** los de C-F01-00. **Zod:** `forkliftUseListQuerySchema`, `forkliftUseSchema`. **Notas:** «En curso» = `status=InProgress`; «Finalizados» = `status=Ended,Complete`.

##### C-F04-19 · `GET warehouse/forklift-uses/{id}` (modificado)
- **Política:** `WarehouseAccess`. **Petición:** el Id en la ruta. **Respuesta 200:** `dataSchema(forkliftUseSchema)` (la forma de C-F04-18, en lugar de `ForkliftUseDetailDto`). **Errores:** los de hoy (404). **Zod:** `forkliftUseSchema`.

##### C-F04-20 · `POST warehouse/forklift-uses/start` (modificado)
- **Política:** `WarehouseAccess`. **Qué cambia:** salen `paymentMode` y `stakeholderId` (el cliente sale del servicio, como hoy cuando no viene); `entryLogId` pasa a obligatorio; el tipo se guarda en el vehículo con D26.
- **Petición:** `forkliftStartSchema`: `serviceRecordId` (guid), `entryLogId` (guid, del servicio), `initHourmeter` (número ≥ 0, con decimales), `vehicleType` (`ForkliftVehicleType`), `comments` (≤ 500 o nulo).
- **Respuesta 201:** `dataSchema(forkliftUseSchema)`.
- **Errores:** los de hoy (`B/Wms.Application/Warehouse/Commands/Forklift/ForkliftMessages.cs`): entrada que no es del servicio (400), tipo de vehículo inválido (400), uso en curso del mismo servicio (409, `StartForkliftUseCommandHandler.cs:91-97`). **Zod:** `forkliftStartSchema`, `forkliftUseSchema`.

##### C-F04-21 · `POST warehouse/forklift-uses/{id}/end` (modificado)
- **Política:** `WarehouseAccess`. **Qué cambia:** `applyVat` pasa a `requiresInvoice` y decide IVA y modo (D25).
- **Petición:** `forkliftEndSchema`: `endHourmeter` (> inicial), `comments` (≤ 500 o nulo), `requiresInvoice` (boolean), `billing` (`billingRecipientInputSchema` de `P01/` §2.3: `totalAmount` = valor del servicio sin IVA, > 0; `paymentMode` = `PendingBilling` con factura e `Immediate` sin ella).
- **Efecto:** con factura: IVA con la tasa del catálogo (D2), factura interna sin pago, pendiente de número; sin factura: IVA 0, factura interna pagada con su método y referencia, `fiscalNumberNotApplicable` (D3). El uso queda `Complete` y guarda `RequiresInvoice`.
- **Respuesta 200:** `dataSchema(forkliftUseSchema)`.
- **Errores:** 400 «Con factura, el cobro queda pendiente por facturar; sin factura, es de pago inmediato.»; y los de hoy (`EndForkliftUseCommandHandler.cs`): «El impuesto IVA no está activo en el catálogo; no se puede agregar IVA.» (con factura), «El valor del servicio debe ser mayor a cero.», horómetro final no mayor que el inicial, uso que no está en curso, estado financiero del cliente (`ValidateFinancialStatusAsync`). **Zod:** `forkliftEndSchema`, `forkliftUseSchema`.

##### C-F04-22 y C-F04-23 · `GET warehouse/forklift-uses/active` y `PATCH warehouse/forklift-uses/{id}/payment-mode` (retirados)
Responden 404 (D29).

##### C-F04-24 · `GET warehouse/forklift-rate` (sin cambios)
- **Política:** `WarehouseAccess`. **Petición (query):** `stakeholderId` (guid, opcional), `vehicleType` (`ForkliftVehicleType`, obligatorio). **Respuesta 200:** `dataSchema(forkliftRateSchema)` = `{ "ratePerHour": 220000, "taxRatePercent": 0, "vatRatePercent": 19 }` (`B/Wms.Application/Warehouse/Common/DTOs/ForkliftRateDto.cs`). **Errores:** 400 «El tipo de vehículo es requerido.» (`WarehouseController.cs:467-470`) y los de la tarifa sin configurar (hoy). **Notas:** `ratePerHour` precarga el valor del servicio y `vatRatePercent` es la tasa del IVA de D2. **Zod:** `forkliftRateSchema`.

##### C-F04-25 · `GET forklift-rates/vehicle-types` (sin cambios)
- **Política:** autenticado (`B/Wms.Api/Controllers/v1/ForkliftRateController.cs:19`, `:27`). **Petición:** sin parámetros. **Respuesta 200:** `dataSchema(z.array(forkliftVehicleTypeItemSchema))` = `[{ "value": "GuacalEstiba", "label": "Guacal / estiba" }, …]`. **Errores:** ninguno. **Zod:** `forkliftVehicleTypeItemSchema`.

#### Grupo D — Inventario y novedades

##### C-F04-26 · `GET warehouse/inventory/movements` (modificado sobre C-F01-147)
- **Política:** `WarehouseAccess`. **Qué cambia:** orden y filtros (C-F01-00): `fromDate` y `toDate` pasan a `createdAtFrom` y `createdAtTo` (`DateOnly`); `movementType` y `sourceType` admiten varios; suman `productName` (texto) y `authorizedByUser` (texto); se conservan `warehouseStorageId`, `warehouseStorageProductId` y `warehouseStorageNumber` (texto). La fila no cambia (`B/Wms.Application/Warehouse/Common/DTOs/InventoryMovementDto.cs`). **Petición (query):** los filtros de «Qué cambia», más paginación y orden. **Orden:** lista blanca `createdAt`, `warehouseStorageNumber`, `productName`, `movementType`, `sourceType`; por defecto `createdAt desc`.
- **Respuesta 200:** `pagedSchema(inventoryMovementSchema)`. **Errores:** los de C-F01-00 (reemplazan el 400 de filtros de hoy, `WarehouseController.cs:695-700`). **Zod:** `inventoryMovementQuerySchema`, `inventoryMovementSchema`.

##### C-F04-27 · `GET warehouse/inventory/deposits` (sin cambios)
- **Política:** `WarehouseAccess` (`WarehouseController.cs:780`). **Petición:** la de hoy (`GetInventoryDepositsQuery.cs`: `searchTerm`, `stakeholderId`, `searchField`, `searchValue`, `includeZeroStock`, `includeReceivedDrafts`, paginación). **Respuesta 200:** `pagedSchema(inventoryDepositSchema)`. **Errores:** los de hoy. Lo usa `WarehouseDepositSelect`. **Zod:** `inventoryDepositSchema`.

##### C-F04-28 · ubicación de lo almacenado (sin cambios)
- **Petición:** el Id del producto del depósito en la ruta; `POST …/placements` y `POST …/placements/release` con `{ warehouseLocationId, quantity }` (`placementInputSchema`) y `POST …/placements/move` con `{ fromLocationId, toLocationId, quantity }` (`placementMoveSchema`) (`B/Wms.Api/Controllers/v1/Requests/WarehousePlacementRequests.cs`). **Respuesta 200:** `dataSchema(productPlacementsSchema)` en las cuatro. **Zod:** `productPlacementsSchema`, `placementInputSchema`, `placementMoveSchema`. **Política:** `WarehouseAccess` (`B/Wms.Api/Controllers/v1/WarehousePlacementsController.cs:22`). **Errores:** los de hoy (`PlacementPlanner`). Lo usa `ProductPlacementsDialog`, sin cambios.

##### C-F04-29 · `GET warehouse/locations/{id}/placements` (sin cambios)
- **Política:** `WarehouseAccess` (`WarehousePlacementsController.cs:100`). **Petición:** el Id de la ubicación en la ruta. **Respuesta 200:** `dataSchema(locationPlacementsSchema)`. **Errores:** 404 de hoy. **Zod:** `locationPlacementsSchema`. Lo usa `LocationContentPanel`.

##### C-F04-30 · `GET warehouse/novelties` (modificado)
- **Política:** `NoveltyReadAccess` (hoy, `B/Wms.Api/Controllers/v1/WarehouseNoveltiesController.cs:28-29`). **Qué cambia:** orden y filtros (C-F01-00): `from` y `to` pasan a `startedAtFrom` y `startedAtTo`; `type` admite varios; suman `warehouseStorageNumber`, `productName` y `vehiclePlate` (texto); se conservan `warehouseStorageId`, `warehouseStorageProductId` e `includeVoided`. **Petición (query):** los filtros de «Qué cambia», más paginación y orden. **Orden:** lista blanca `startedAt`, `warehouseStorageNumber`, `productName`, `type`; por defecto `startedAt desc`.
- **Respuesta 200:** `pagedSchema(noveltySchema)` (la fila de hoy, `B/Wms.Application/Warehouse/Novelties/Common/WarehouseNoveltyDto.cs`). **Errores:** los de C-F01-00. **Zod:** `noveltyListQuerySchema`, `noveltySchema`.

##### C-F04-31 · el resto de novedades (sin cambios)
- **Política:** `NoveltyReadAccess` en `GET warehouse/novelties/{id}` y `GET …/{id}/pdf`; `WarehouseAccess` en `POST warehouse/novelties`, `PUT …/{id}` y `POST …/{id}/void` (`WarehouseNoveltiesController.cs:41-129`).
- **Petición:** el Id en la ruta; `POST` con `noveltyCreateSchema` (`{ warehouseStorageProductId, …noveltyInput }`); `PUT` con `noveltyInputSchema`; `void` con `{ reason }` (`reasonBodySchema`, 10 a 500).
- **Respuesta 200:** `dataSchema(noveltySchema)`; el PDF, binario (`application/pdf`).
- **Errores:** los de hoy (`NoveltyInputValidator.cs`, `NoveltyQuantityRules`). **Zod:** `noveltyCreateSchema`, `noveltyInputSchema`, `noveltySchema`, `reasonBodySchema`.

### 2.3 Esquemas Zod y tipos

Zod 4 (`Frontend/wms/package.json`: `zod ^4.1.13`), con las ayudas comunes de `F/shared/contracts/api.ts` (`guidSchema`, `dateTimeSchema`, `dateOnlySchema`, `identificationTypeSchema`, `dataSchema`, `pagedSchema`, `listQueryBaseSchema`, `reasonSchema`). Los tipos se derivan con `z.infer` (`export type X = z.infer<typeof xSchema>`). Los filtros con varios valores se declaran como arreglo y la fuente http los une con coma (C-F01-00).

**`F/features/warehouse/contracts/clock.ts`** (FE-1; C-F04-03 a C-F04-06, C-F04-09):

```ts
import { z } from "zod";
import { dateTimeSchema } from "~/shared/contracts/api";

export const watchedRecordSchema = z.enum(["Reception", "Loading", "YardExit"]);
export const clockLevelSchema = z.enum(["None", "Yellow", "Red"]);
export const warehouseClockSchema = z.object({
  watchedRecord: watchedRecordSchema,
  startedAt: dateTimeSchema,
  stoppedAt: dateTimeSchema.nullable(),          // nulo mientras corre
  elapsedMinutes: z.int().min(0),                // a la hora del servidor o hasta el fin
  level: clockLevelSchema,
  yellowMinutes: z.int().min(1).nullable(),      // umbrales vigentes (D33)
  redMinutes: z.int().min(1).nullable(),
});
export type WatchedRecord = z.infer<typeof watchedRecordSchema>;
export type ClockLevel = z.infer<typeof clockLevelSchema>;
export type WarehouseClock = z.infer<typeof warehouseClockSchema>;
```

**`F/features/administration/contracts/alert-threshold.ts`** (FE-2; C-F04-01, C-F04-02):

```ts
import { z } from "zod";
import { dateTimeSchema } from "~/shared/contracts/api";
import { watchedRecordSchema } from "~/features/warehouse/contracts/clock";

const minutesSchema = z.int().min(1).max(10080).nullable();
export const alertThresholdSchema = z.object({
  watchedRecord: watchedRecordSchema,
  yellowMinutes: minutesSchema,
  redMinutes: minutesSchema,
  updatedAt: dateTimeSchema.nullable(),
});
export const alertThresholdInputSchema = z
  .object({ watchedRecord: watchedRecordSchema, yellowMinutes: minutesSchema, redMinutes: minutesSchema })
  .refine((t) => (t.yellowMinutes === null) === (t.redMinutes === null), { message: "Indique los dos umbrales o ninguno." })
  .refine((t) => t.yellowMinutes === null || t.redMinutes === null || t.yellowMinutes < t.redMinutes, {
    message: "El umbral amarillo debe ser menor que el rojo.",
  });
export const alertThresholdsUpdateSchema = z.object({ thresholds: z.array(alertThresholdInputSchema).length(3) });
```

**Extensiones de contratos de F01** (FE-1; los maquetan F05 y F06):

```ts
// F/features/exits/contracts/exit.ts — C-F04-03 y C-F04-04: se agrega a los dos objetos.
import { warehouseClockSchema, clockLevelSchema } from "~/features/warehouse/contracts/clock";
//   exitSchema         = z.object({ …campos de hoy…, warehouseClock: warehouseClockSchema.nullable() })
//   exitListItemSchema = z.object({ …campos de hoy…, warehouseClock: warehouseClockSchema.nullable() })
//   exitListQuerySchema = listQueryBaseSchema.extend({ …filtros de hoy…, warehouseLevel: z.array(clockLevelSchema).optional() })

// F/features/foreign-trade/contracts/deposit-entry.ts — C-F04-05: esquema nuevo; depositEntrySchema no cambia.
export const depositEntryReceptionSchema = z.object({
  status: z.enum(["Pending", "Received"]),
  receptionLogId: guidSchema.nullable(),
  receivedAt: dateTimeSchema.nullable(),
  receivedByName: z.string().nullable(),
  staysOnVehicle: z.boolean().nullable(),
  clock: warehouseClockSchema.nullable(),
});
export const depositEntryWithReceptionSchema = depositEntrySchema.extend({
  reception: depositEntryReceptionSchema.nullable(),   // nulo si la entrada está anulada
});

// F/features/warehouse/contracts/location.ts — C-F04-14: locationSchema suma `isSystem: z.boolean()`.
```

**`F/features/warehouse/contracts/reception.ts`** (FE-1; C-F04-06 a C-F04-10, C-F04-13, C-F04-17):

```ts
import { z } from "zod";
import {
  dataSchema, dateOnlySchema, dateTimeSchema, guidSchema, identificationTypeSchema, listQueryBaseSchema,
} from "~/shared/contracts/api";
import { clockLevelSchema, warehouseClockSchema } from "./clock";

export const vehicleTypeSchema = z.enum(["Tractomula", "DobleTroque", "Sencillo", "Turbo", "VehParticular", "Otro"]);
export const vehicleTypeItemSchema = z.object({ value: vehicleTypeSchema, label: z.string() });
export const receptionKindSchema = z.enum(["Weighbridge", "Direct"]);

export const pendingReceptionProductSchema = z.object({
  warehouseStorageProductId: guidSchema,
  productName: z.string(),
  productDescription: z.string().nullable(),
  packaging: z.string().nullable(),
  entryDeclaredQuantity: z.number().nullable(),
  currentStock: z.number(),
});
export const pendingReceptionItemSchema = z.object({
  warehouseStorageEntryId: guidSchema,
  entryLogId: guidSchema,
  serviceRecordId: guidSchema,
  warehouseStorageId: guidSchema,
  warehouseStorageNumber: z.string(),
  weighedAt: dateTimeSchema,
  vehicleId: guidSchema,
  vehiclePlate: z.string(),
  vehicleType: vehicleTypeSchema.nullable(),
  driver: z.object({ fullName: z.string(), idType: identificationTypeSchema, idNumber: z.string() }).nullable(),
  carrierCompanyName: z.string().nullable(),
  customerId: guidSchema.nullable(),
  customerName: z.string().nullable(),
  merchandiseText: z.string(),
  declaredQuantity: z.number().nullable(),
  manifestNumber: z.string().nullable(),
  manifestWeight: z.number().nullable(),
  merchandiseWeight: z.number().nullable(),
  usesCargoUnits: z.boolean(),
  forkliftInProgress: z.boolean(),
  products: z.array(pendingReceptionProductSchema),
  clock: warehouseClockSchema,
});
export const pendingReceptionQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["weighedAt", "vehiclePlate", "warehouseStorageNumber", "customerName"]).optional(),
  vehiclePlate: z.string().optional(),
  warehouseStorageNumber: z.string().optional(),
  customerName: z.string().optional(),
  merchandise: z.string().optional(),
  weighedAtFrom: dateOnlySchema.optional(),
  weighedAtTo: dateOnlySchema.optional(),
  level: z.array(clockLevelSchema).optional(),
});

export const receptionPhotoInputSchema = z.object({
  base64Data: z.string().min(1),
  title: z.string().max(200).nullable().optional(),
  description: z.string().max(500).nullable().optional(),
});
export const receptionProductInputSchema = z.object({
  warehouseStorageProductId: guidSchema,
  unloadedQuantity: z.number().positive(),
  warehouseLocationId: guidSchema.nullable(),
});
export const receptionCreateSchema = z.object({
  warehouseStorageEntryId: guidSchema,
  vehicleType: vehicleTypeSchema.nullable(),
  staysOnVehicle: z.boolean(),
  products: z.array(receptionProductInputSchema),
  receivedCargoUnitIds: z.array(guidSchema).nullable(),
  crewId: guidSchema.nullable(),
  comments: z.string().max(500).nullable(),
  signatureDriver: z.string().nullable(),
  photos: z.array(receptionPhotoInputSchema).max(5),
});
export const receptionResultSchema = z.object({
  receptionLogId: guidSchema,
  warehouseStorageId: guidSchema,
  warehouseStorageNumber: z.string(),
  totalUnloadedQuantity: z.number(),
  quantityDiscrepancy: z.number().nullable(),
  discrepancyPercentage: z.number().nullable(),
  hasDiscrepancy: z.boolean(),
  status: z.string(),                     // «Completed»
  createdAt: dateTimeSchema,
  unloadCompletedAt: dateTimeSchema.nullable(),
});

export const directReceptionProductInputSchema = z.object({
  productId: guidSchema,
  packagingTypeId: guidSchema.nullable(),
  productDescription: z.string().trim().max(500).nullable(),
  declaredQuantity: z.number().positive(),
  unloadedQuantity: z.number().positive(),
  warehouseLocationId: guidSchema.nullable(),
});
export const directReceptionCreateSchema = z
  .object({
    entryLogId: guidSchema,
    driverId: guidSchema,
    carrierCompanyId: guidSchema,
    vehicleCountry: z.string().trim().min(1).max(100).nullable(),
    vehicleType: vehicleTypeSchema.nullable(),
    documentTypeId: guidSchema.nullable(),
    documentNumber: z.string().trim().min(1).max(50).nullable(),
    inspectionDescription: z.string().trim().min(10).max(500),
    staysOnVehicle: z.boolean(),
    products: z.array(directReceptionProductInputSchema),
    crewId: guidSchema.nullable(),
    comments: z.string().max(500).nullable(),
    signatureDriver: z.string().nullable(),
    photos: z.array(receptionPhotoInputSchema).max(5),
  })
  .refine((r) => (r.documentTypeId === null) === (r.documentNumber === null), {
    message: "Indique el tipo y el número del documento, o ninguno.",
  });

export const receptionListItemSchema = z.object({
  id: guidSchema,
  kind: receptionKindSchema,
  warehouseStorageEntryId: guidSchema,
  warehouseStorageId: guidSchema,
  warehouseStorageNumber: z.string(),
  vehiclePlate: z.string(),
  driverName: z.string().nullable(),
  customerName: z.string().nullable(),
  merchandiseText: z.string(),
  totalUnloadedQuantity: z.number(),
  hasDiscrepancy: z.boolean(),
  staysOnVehicle: z.boolean(),
  crewName: z.string().nullable(),
  receivedByName: z.string().nullable(),
  weighedAt: dateTimeSchema.nullable(),     // nulo en las directas
  receivedAt: dateTimeSchema,
  elapsedMinutes: z.int().min(0).nullable(),
});
export const receptionListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["receivedAt", "vehiclePlate", "warehouseStorageNumber", "customerName"]).optional(),
  receivedAtFrom: dateOnlySchema.optional(),
  receivedAtTo: dateOnlySchema.optional(),
  vehiclePlate: z.string().optional(),
  warehouseStorageNumber: z.string().optional(),
  customerName: z.string().optional(),
  merchandise: z.string().optional(),
  kind: z.array(receptionKindSchema).optional(),
});
export const receptionProductLineSchema = z.object({
  warehouseStorageProductId: guidSchema,
  productName: z.string(),
  productDescription: z.string().nullable(),
  packagingType: z.string().nullable(),
  entryDeclaredQuantity: z.number().nullable(),
  countedQuantity: z.number().nullable(),
  difference: z.number().nullable(),
  warehouseLocationCode: z.string().nullable(),
});
export const receptionDetailSchema = z.object({
  id: guidSchema,
  kind: receptionKindSchema,
  warehouseStorageEntryId: guidSchema,
  warehouseStorageId: guidSchema,
  warehouseStorageNumber: z.string(),
  entryLogId: guidSchema,
  vehiclePlate: z.string(),
  vehicleType: vehicleTypeSchema.nullable(),
  driverName: z.string().nullable(),
  driverIdType: z.string().nullable(),
  driverIdNumber: z.string().nullable(),
  importerName: z.string().nullable(),
  exporterName: z.string().nullable(),
  customerName: z.string().nullable(),
  customsAgencyName: z.string().nullable(),
  carrierName: z.string().nullable(),
  carrierIdNumber: z.string().nullable(),
  cargoHandling: z.enum(["LooseGoods", "CargoUnits"]),
  entryPhysicalNetWeight: z.number().nullable(),
  staysOnVehicle: z.boolean(),
  crewName: z.string().nullable(),
  receivedByName: z.string().nullable(),
  weighedAt: dateTimeSchema.nullable(),
  unloadCompletedAt: dateTimeSchema.nullable(),
  elapsedMinutes: z.int().min(0).nullable(),
  comments: z.string().nullable(),
  signatureDriver: z.string().nullable(),
  photos: z.array(z.object({ id: guidSchema, url: z.string(), title: z.string().nullable(), createdAt: dateTimeSchema })),
  productLines: z.array(receptionProductLineSchema),
  cargoUnits: z.array(z.object({ id: guidSchema, cargoUnitTypeName: z.string(), plateNumber: z.string() }).loose()),
});

export const plateSearchDepositSchema = z.object({
  warehouseStorageEntryId: guidSchema,
  warehouseStorageId: guidSchema,
  warehouseStorageNumber: z.string().nullable(),
  serviceRecordId: guidSchema,
  stakeholderId: guidSchema.nullable(),
  stakeholderName: z.string().nullable(),
  productDescription: z.string().nullable(),
  hasCompletedReception: z.boolean(),
  forkliftInProgress: z.boolean(),
});
export const plateSearchSchema = z.object({
  message: z.string(),
  entryLogId: guidSchema.nullable(),       // nulo: la placa no está en planta
  vehiclePlate: z.string().nullable(),
  vehicleType: vehicleTypeSchema.nullable(),
  driverName: z.string().nullable(),
  deposits: z.array(plateSearchDepositSchema),
});
export const vehicleTypesResponseSchema = dataSchema(z.array(vehicleTypeItemSchema));
```

**`F/features/warehouse/contracts/forklift.ts`** (FE-2; C-F04-18 a C-F04-21, C-F04-24, C-F04-25):

```ts
import { z } from "zod";
import { dateOnlySchema, dateTimeSchema, guidSchema, listQueryBaseSchema } from "~/shared/contracts/api";
import { billingRecipientInputSchema } from "~/features/billing/contracts/billing-recipient";

export const forkliftUseStatusSchema = z.enum(["InProgress", "Ended", "Complete"]);
export const forkliftVehicleTypeSchema = z.enum(["Tractomula", "DobleTroque", "Sencillo", "Turbo", "GuacalEstiba"]);
export const forkliftVehicleTypeItemSchema = z.object({ value: forkliftVehicleTypeSchema, label: z.string() });
export const forkliftUseSchema = z.object({
  id: guidSchema,
  serviceRecordId: guidSchema,
  entryLogId: guidSchema.nullable(),
  warehouseStorageNumber: z.string().nullable(),
  vehiclePlate: z.string(),
  vehicleType: forkliftVehicleTypeSchema,
  vehicleTypeLabel: z.string(),
  customerId: guidSchema.nullable(),
  customerName: z.string().nullable(),
  driverName: z.string().nullable(),
  initHourmeter: z.number(),
  endHourmeter: z.number().nullable(),
  dateInit: dateTimeSchema,
  dateEnd: dateTimeSchema.nullable(),
  hoursUsed: z.number().nullable(),
  status: forkliftUseStatusSchema,
  comments: z.string().nullable(),
  requiresInvoice: z.boolean().nullable(),
  paidAmount: z.number().nullable(),
  invoiced: z.boolean().nullable(),
});
export const forkliftUseListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["dateInit", "dateEnd", "vehiclePlate", "customerName"]).optional(),
  status: z.array(forkliftUseStatusSchema).optional(),
  vehiclePlate: z.string().optional(),
  customerName: z.string().optional(),
  vehicleType: z.array(forkliftVehicleTypeSchema).optional(),
  dateInitFrom: dateOnlySchema.optional(),
  dateInitTo: dateOnlySchema.optional(),
  stakeholderId: guidSchema.optional(),
});
export const forkliftStartSchema = z.object({
  serviceRecordId: guidSchema,
  entryLogId: guidSchema,
  initHourmeter: z.number().min(0),
  vehicleType: forkliftVehicleTypeSchema,
  comments: z.string().max(500).nullable(),
});
export const forkliftEndSchema = z
  .object({
    endHourmeter: z.number().positive(),
    comments: z.string().max(500).nullable(),
    requiresInvoice: z.boolean(),
    billing: billingRecipientInputSchema,
  })
  .refine((e) => e.billing.paymentMode === (e.requiresInvoice ? "PendingBilling" : "Immediate"), {
    message: "Con factura, el cobro queda pendiente por facturar; sin factura, es de pago inmediato.",
  });
export const forkliftRateSchema = z.object({
  ratePerHour: z.number(),
  taxRatePercent: z.number(),
  vatRatePercent: z.number(),
});
```

**`F/features/warehouse/contracts/inventory.ts`** (FE-3; C-F04-26 a C-F04-29; C-F01-148):

```ts
import { z } from "zod";
import { dateOnlySchema, dateTimeSchema, guidSchema, listQueryBaseSchema } from "~/shared/contracts/api";

export const movementTypeSchema = z.enum(["In", "Out", "Adjustment"]);
export const movementSourceSchema = z.enum([
  "ReceptionLog", "GoodsExit", "Adjustment", "Damage", "Return", "DeclaredEntry",
  "GoodsExitReversal", "WeighingVoid", "StorageCancellation", "MigrationOpening", "DepositProductEdit",
]);
export const inventoryMovementSchema = z.object({
  id: guidSchema, warehouseStorageProductId: guidSchema, warehouseStorageId: guidSchema,
  warehouseStorageNumber: z.string(), productName: z.string().nullable(), productDescription: z.string().nullable(),
  movementType: movementTypeSchema, quantity: z.number(), sourceType: movementSourceSchema, sourceId: guidSchema.nullable(),
  previousStock: z.number(), newStock: z.number(), reason: z.string().nullable(), authorizedByUser: z.string().nullable(),
  createdAt: dateTimeSchema, movementDate: dateTimeSchema, truckPlate: z.string().nullable(),
  ticketNumber: z.string().nullable(), dispatchGuideNumber: z.string().nullable(),
});
export const inventoryMovementQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["createdAt", "warehouseStorageNumber", "productName", "movementType", "sourceType"]).optional(),
  warehouseStorageId: guidSchema.optional(),
  warehouseStorageProductId: guidSchema.optional(),
  warehouseStorageNumber: z.string().optional(),
  productName: z.string().optional(),
  authorizedByUser: z.string().optional(),
  movementType: z.array(movementTypeSchema).optional(),
  sourceType: z.array(movementSourceSchema).optional(),
  createdAtFrom: dateOnlySchema.optional(),
  createdAtTo: dateOnlySchema.optional(),
});
export const inventoryDepositSchema = z.object({
  warehouseStorageId: guidSchema, warehouseStorageNumber: z.string(), stakeholderId: guidSchema,
  stakeholderName: z.string(), operationModalityCode: z.string().nullable(), createdAt: dateTimeSchema, status: z.string(),
  products: z.array(z.object({
    warehouseStorageProductId: guidSchema, productName: z.string(), productDescription: z.string(),
    currentStock: z.number(), availableStock: z.number(), cargoHandling: z.string(),
    nationalizedQuantity: z.number().nullable(), nationalizedAvailable: z.number().nullable(),
    receivedQuantity: z.number(), reservedStock: z.number(),
  })),
});
export const depositStockSchema = z.object({          // C-F01-148 (StockDto)
  warehouseStorageId: guidSchema, warehouseStorageNumber: z.string(), status: z.string(),
  entryDate: dateTimeSchema.nullable(), expectedExitDate: dateTimeSchema.nullable(),
  products: z.array(z.object({
    id: guidSchema, productId: guidSchema, productName: z.string().nullable(), productDescription: z.string().nullable(),
    packagingTypeId: guidSchema.nullable(), packagingTypeName: z.string().nullable(), declaredQuantity: z.number().nullable(),
    receivedQuantity: z.number(), currentStock: z.number(), reservedStock: z.number(), availableStock: z.number(),
    warehouseLocationId: guidSchema.nullable(), warehouseLocationCode: z.string().nullable(), warehouseLocationName: z.string().nullable(),
  })),
});
const placementSchema = z.object({
  warehouseLocationId: guidSchema, locationCode: z.string(), locationName: z.string(),
  quantity: z.number(), lastPlacedAt: dateTimeSchema,
});
export const productPlacementsSchema = z.object({
  warehouseStorageProductId: guidSchema, warehouseStorageId: guidSchema, warehouseStorageNumber: z.string(),
  productName: z.string(), currentStock: z.number(), placedQuantity: z.number(), pendingToPlace: z.number(),
  mainLocationId: guidSchema.nullable(), placements: z.array(placementSchema),
});
export const placementInputSchema = z.object({ warehouseLocationId: guidSchema, quantity: z.number().positive() });
export const placementMoveSchema = z.object({ fromLocationId: guidSchema, toLocationId: guidSchema, quantity: z.number().positive() });
export const locationPlacementsSchema = z.object({
  warehouseLocationId: guidSchema, code: z.string(), name: z.string(), isAvailable: z.boolean(), totalQuantity: z.number(),
  items: z.array(z.object({
    warehouseStorageProductId: guidSchema, warehouseStorageNumber: z.string(), productName: z.string(),
    quantity: z.number(), lastPlacedAt: dateTimeSchema,
  })),
});
```

**`F/features/warehouse/contracts/novelty.ts`** (FE-3; C-F04-30, C-F04-31):

```ts
import { z } from "zod";
import { dateOnlySchema, dateTimeSchema, guidSchema, listQueryBaseSchema } from "~/shared/contracts/api";

export const noveltyTypeSchema = z.enum(["Entry", "Exit", "Transshipment", "Routine", "Inspection"]);
export const tarpConditionSchema = z.enum(["Good", "Holed", "Torn", "NoTarp"]);
export const trailerConditionSchema = z.enum(["Clean", "Dirty", "Rusty", "Wet", "Broken"]);
export const noveltySchema = z.object({
  id: guidSchema, warehouseStorageProductId: guidSchema, warehouseStorageId: guidSchema,
  warehouseStorageNumber: z.string(), productName: z.string(), warehouseStorageEntryId: guidSchema.nullable(),
  vehiclePlate: z.string().nullable(), type: noveltyTypeSchema, startedAt: dateTimeSchema, endedAt: dateTimeSchema,
  orderedBy: z.string().nullable(), description: z.string(), totalQuantity: z.number(), goodQuantity: z.number(),
  damagedQuantity: z.number(), missingQuantity: z.number(), surplusQuantity: z.number(), isUnloaded: z.boolean(),
  unloadedQuantity: z.number(), tarpCondition: z.string().nullable(), trailerCondition: z.string().nullable(),
  photoRecord: z.string().nullable(), createdByName: z.string(), createdAt: dateTimeSchema, updatedAt: dateTimeSchema.nullable(),
  isVoided: z.boolean(), voidedAt: dateTimeSchema.nullable(), voidReason: z.string().nullable(), quantityWarning: z.string().nullable(),
});
export const noveltyListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["startedAt", "warehouseStorageNumber", "productName", "type"]).optional(),
  warehouseStorageId: guidSchema.optional(),
  warehouseStorageProductId: guidSchema.optional(),
  warehouseStorageNumber: z.string().optional(),
  productName: z.string().optional(),
  vehiclePlate: z.string().optional(),
  type: z.array(noveltyTypeSchema).optional(),
  startedAtFrom: dateOnlySchema.optional(),
  startedAtTo: dateOnlySchema.optional(),
  includeVoided: z.boolean().optional(),
});
export const noveltyInputSchema = z.object({
  warehouseStorageEntryId: guidSchema.nullable(), type: noveltyTypeSchema, startedAt: dateTimeSchema, endedAt: dateTimeSchema,
  orderedBy: z.string().max(200).nullable(), description: z.string().max(2000).nullable(),
  totalQuantity: z.number().min(0), goodQuantity: z.number().min(0), damagedQuantity: z.number().min(0),
  missingQuantity: z.number().min(0), surplusQuantity: z.number().min(0), isUnloaded: z.boolean(),
  tarpCondition: tarpConditionSchema.nullable(), trailerCondition: trailerConditionSchema.nullable(), photoRecord: z.string().nullable(),
});
export const noveltyCreateSchema = noveltyInputSchema.extend({ warehouseStorageProductId: guidSchema });
```

Los límites de texto de `noveltyInputSchema` (200 y 2000) los confirma el ejecutor de FE-3 contra `B/Wms.Application/Warehouse/Novelties/Common/NoveltyInputValidator.cs` antes de usarlos; si difieren, gana el validador y se anota en §8.6.

### 2.4 Pantallas y sus endpoints

| Pantalla | Ruta | Endpoints |
| --- | --- | --- |
| P-BOD-01 · Entradas › Recepción | `/warehouse/receptions` | C-F04-06; «Montacargas» abre P-BOD-04 (C-F04-25, C-F04-20) |
| P-BOD-02 · Recepción física (modal) | sobre P-BOD-01 | La fila de C-F04-06; C-F01-146 (unidades de carga); C-F04-14 y C-F04-15 (ubicaciones y «+ Nueva posición»); C-F01-52 (cuadrillas); C-F04-17 (tipos de vehículo); C-F04-07 |
| P-BOD-03 · Recepción directa | `/warehouse/receptions/direct/[entryLogId]` | C-F01-152 (elegir el ingreso, desde P-BOD-01); C-F01-15 y C-F01-17 (conductor y su alta); C-F01-25, C-F01-26 y C-F01-141 (transportadora y su alta); C-F04-17; C-F03-44 (tipos de documento); C-F01-69 (productos); C-F01-29 (embalajes); C-F04-14 y C-F04-15; C-F01-52; C-F04-08 |
| P-BOD-04 · Montacargas: inicio y cobro (modales) | sobre P-BOD-01 y Montacargas | C-F04-13 («+ Registrar uso»); C-F04-25; C-F04-20; C-F04-24 (tarifa e IVA); C-F01-25, C-F01-26 y C-F01-141 (tercero del cobro); C-F04-21 |
| P-BOD-05 · Montacargas (listado, D7) | `/warehouse/forklift` | C-F04-18; C-F04-19 (drawer); «Finalizar» abre el cobro de P-BOD-04 |
| Entradas › Historial | `/warehouse/receptions/history` | C-F04-09; C-F04-10 (drawer) |
| P-TR-08 · Administración › Umbrales de alertas | `/admin/alert-thresholds` | C-F04-01, C-F04-02 |
| Inventario | `/warehouse/inventory` | C-F04-27 y C-F01-148 (Existencias); C-F04-28 (`ProductPlacementsDialog`); C-F04-31 (registrar novedad); C-F04-26 (Movimientos); C-F04-14 y C-F04-29 (Ubicaciones) |
| Novedades | `/warehouse/novelties` | C-F04-30; C-F04-31; C-F04-27 y C-F01-148 (elegir depósito y producto) |
| Configuración › Ubicaciones (F02, ajuste) | `/admin/locations` | C-F04-14 y C-F04-16 (la ubicación del sistema sin acciones) |
| Tablero de Bodega | `/warehouse` | Ninguno (enlaces, D44) |
| Para F06 (P-BOD-06 a P-BOD-09) | — | C-F04-03, C-F04-04 (`warehouseClock`) |
| Para F05 (etapa Bodega del detalle de CE) | — | C-F04-05 (`reception`) |

---

## 3. Archivos que se tocan

### 3.1 Pantallas y componentes

| Pantalla | Ruta y archivo | Tipo (guardia) | Componentes |
| --- | --- | --- | --- |
| P-BOD-01 Recepción | `F/pages/warehouse/receptions/index.vue` (se rehace en su ruta, M11) | `PATTERN` | `AppDataTable`, `AppRowActions`, `VehiclePlateTag`, `WarehouseClockTag`, `ReceptionDialog`, `DirectReceptionEntryPicker`, `ForkliftStartDialog` |
| P-BOD-02 Recepción física | modal de P-BOD-01 | — | `ReceptionDialog` con `ReceptionProductRows`, `LocationQuickDialog`, `SignaturePad`, `PhotoUploader` |
| P-BOD-03 Recepción directa | `F/pages/warehouse/receptions/direct/[entryLogId].vue` (nueva) | Formulario fuera del menú (la guardia list-pattern no la lista; sin `AppPageHeader`, con `<h1 class="sr-only">`) | `DirectReceptionTruckSection` (con `DriverQuickDialog`, `StakeholderQuickDialog`, `AppSearchSelect`), `DirectReceptionGoodsSection`, `ReceptionProductRows`, `LocationQuickDialog`, `SignaturePad`, `PhotoUploader` |
| P-BOD-04 Montacargas | modales de P-BOD-01 y de Montacargas | — | `ForkliftStartDialog`, `ForkliftChargeDialog` (con `AppChargeForm`, `StakeholderQuickDialog`) |
| P-BOD-05 Montacargas | `F/pages/warehouse/forklift/index.vue` (se rehace en su ruta) | `PATTERN` (antes `OUTSIDE`) | `AppDataTable` con pestañas, `AppRowActions`, `AppDetailDrawer` con `ForkliftUseDetail`, `ForkliftStartDialog` (con búsqueda por placa), `ForkliftChargeDialog` |
| Entradas › Historial | `F/pages/warehouse/receptions/history.vue` (se rehace) | `PATTERN` | `AppDataTable`, `AppRowActions`, `AppDetailDrawer` con `ReceptionDetail` |
| P-TR-08 Umbrales | `F/pages/admin/alert-thresholds/index.vue` (nueva) | `OUTSIDE` («Formulario de configuración: umbrales de alertas») | Tabla editable propia con `InputNumber locale="es-CO"` |
| Inventario | `F/pages/warehouse/inventory/index.vue` (se rehace) | `PATTERN` | `Tabs`, tres `AppDataTable`, `WarehouseDepositSelect`, `ProductPlacementsDialog`, `NoveltyFormDialog`, `AppDetailDrawer` con `LocationContentPanel` |
| Novedades | `F/pages/warehouse/novelties/index.vue` (se rehace) | `PATTERN` | `AppDataTable`, `AppRowActions`, `NoveltyFormDialog` (dos columnas), `ReasonDialog`, `WarehouseDepositSelect` |
| Configuración › Ubicaciones | `F/pages/admin/locations/index.vue` (ajuste) | `PATTERN` (sin cambio) | Oculta las acciones de la fila con `isSystem` |
| Galería | `F/pages/dev/components.vue` | — | Suma `WarehouseClockTag` con los tres niveles |

### 3.2 Backend

**BE-1 (umbrales, relojes y avisos).**
- Se crean: `B/Wms.Domain/Enums/WatchedRecord.cs`, `B/Wms.Domain/Enums/ClockLevel.cs`; `B/Wms.Domain/Entities/Warehouse/WarehouseAlertThreshold.cs` (`IAuditable`) y `WarehouseDelayAlert.cs`; sus configuraciones en `B/Wms.Infrastructure/Persistence/Configurations/Warehouse/` (la de umbrales con `HasData` de las tres filas) y sus `DbSet` en `AppDbContext`; en `B/Wms.Application/Warehouse/Alerts/`: `WarehouseClockRules.cs`, `AlertThresholdRules.cs` y `DelayAlertPlanner.cs` (puras), `WarehouseClockReader.cs` (arma los relojes de entradas y salidas desde la base, para las lecturas y el trabajo), `WarehouseDelayAlertService.cs` (`RunOnceAsync(DateTimeOffset now, CancellationToken)`), `WarehouseDelayAlertMessages.cs`, `Queries/GetAlertThresholds/` y `Commands/UpdateAlertThresholds/` (con su validador); `B/Wms.Api/Controllers/v1/AlertThresholdsController.cs`; `B/Wms.Api/BackgroundJobs/WarehouseDelayAlertBackgroundService.cs`.
- Cambian: `B/Wms.Api/Program.cs:81-87` (registro del trabajo y del servicio); `appsettings.json` (`WarehouseAlerts:IntervalSeconds`: 60); `B/Wms.Application/Warehouse/Queries/GetPendingFromWeighbridge/PendingReceptionFilters.cs` (regla de D14, que usan el trabajo y C-F04-06; su prueba `B/Wms.Tests/Warehouse/PendingReceptionFiltersTests.cs`); `B/Wms.Application/Exits/Common/ExitDtos.cs` (`ExitDto` `:6`, `ExitListItemDto` `:93`: `WarehouseClock`), `B/Wms.Application/Exits/Common/ExitReader.cs` y `B/Wms.Application/Exits/Queries/GetExitsQuery.cs` (filtro `warehouseLevel`); `B/Wms.Application/ForeignTrade/Common/DTOs/DepositStorageEntryDto.cs` y `B/Wms.Application/ForeignTrade/Common/Services/DepositStorageEntryReader.cs` (`Reception`).

**BE-2 (recepción).**
- Cambian: `B/Wms.Domain/Entities/Warehouse/ReceptionLog.cs` (`CrewId`, `StaysOnVehicle`; se borra `RegisterArrival`, `:41`; `Create` recibe la cuadrilla y la marca); `B/Wms.Domain/Entities/Warehouse/WarehouseLocation.cs` (`IsSystem`, guardas de edición y borrado); sus configuraciones (`ReceptionLogConfiguration`, `WarehouseLocationConfiguration`, con la semilla de `SOBRE-VEHICULO`); `B/Wms.Domain/Security/WmsPolicyRoles.cs` (`LocationCreateAccess`); `B/Wms.Api/Controllers/v1/WarehouseLocationsController.cs:68-69` (política de `POST`); `B/Wms.Api/Controllers/v1/WarehouseController.cs:224-260` (salen `register-arrival` y `{id}/complete`), `:262-270`, `:331-345`, `:376-390`, `:90-130`, `:166-175`; `B/Wms.Application/Warehouse/Commands/Reception/CreateReceptionCommand.cs`, su handler y su validador (C-F04-07), `CreateReceptionWithoutWeighbridgeCommand.cs`, su handler y su validador (C-F04-08), `ReceptionHelper.cs`; `B/Wms.Application/Warehouse/Queries/GetPendingFromWeighbridge/*` (C-F04-06), `Queries/GetReceptions/*` y `Common/Mappers/ReceptionProjection.cs` (C-F04-09, C-F04-10), `Queries/SearchByPlateForReception/*` y `Common/DTOs/PlateSearchResultDto.cs` (C-F04-13), `Common/DTOs/ReceptionDto.cs`, `ReceptionDetailDto.cs`, `PendingFromWeighbridgeDto.cs`, `WarehouseLocationDto.cs`; `B/Wms.Application/Warehouse/Commands/Location/*` (C-F04-15, C-F04-16) y `Queries/GetWarehouseLocations/*` (`isSystem`); `B/Wms.Application/Administration/LegacyImport/` (la carga de ubicaciones salta el código reservado, §7).
- Se borran: `Commands/Reception/RegisterReceptionArrivalCommand.cs`, su handler y su validador; `CompleteReceptionCommand.cs`, su handler y su validador (su lógica de ubicación, fotos, firma y diferencias pasa a C-F04-07); `RegisterReceptionArrivalResultDto` (`ReceptionResultDto.cs`); sus pruebas.

**BE-3 (montacargas, inventario y novedades).**
- Cambian: `B/Wms.Domain/Entities/Warehouse/ForkliftUse.cs` (`ApplyVat` → `RequiresInvoice`, `:35`, `:106`; `ChangePaymentMode`, `:186`, se conserva: lo usa el cobro, `EndForkliftUseCommandHandler.cs:69`); `B/Wms.Domain/Entities/Billing/Invoice.cs` (`FiscalNumberNotApplicable`, que entra en `IsNonFiscal`, `:25`) y `B/Wms.Application/Billing/Common/Services/BillingRecipientFactory.cs` (crear la factura con la marca); `B/Wms.Application/Warehouse/Commands/Forklift/StartForkliftUseCommand.cs`, handler y validador (C-F04-20, D26), `EndForkliftUseCommand.cs`, handler y validador (C-F04-21, D25); `B/Wms.Application/Warehouse/Queries/GetActiveForkliftUses/*` y `GetForkliftUseById/*` (C-F04-18, C-F04-19), `Common/DTOs/ForkliftUseDto.cs` y `ForkliftUseDetailDto.cs`; `WarehouseController.cs:430-660` (montacargas) y `:679-760` (movimientos, C-F04-26) con `Queries/GetInventoryMovements/*`; `B/Wms.Application/Warehouse/Novelties/Queries/GetNovelties/*` (C-F04-30).
- Se borran: `Commands/Forklift/ChangePaymentMode/*` y la acción `forklift-uses/active` (D29), con sus pruebas.

### 3.3 Frontend

- **Contratos** (§2.3): `F/features/warehouse/contracts/clock.ts`, `reception.ts`, `forklift.ts`, `inventory.ts`, `novelty.ts`; `F/features/administration/contracts/alert-threshold.ts`; extensiones de `F/features/exits/contracts/exit.ts`, `F/features/foreign-trade/contracts/deposit-entry.ts` y `F/features/warehouse/contracts/location.ts`.
- **Fuentes** (§5.2 de `PM/`): `F/features/warehouse/services/reception.source.ts`, `forklift.source.ts`, `inventory.source.ts`, `novelty.source.ts`, la fachada `catalog.source.ts` (D41) y `F/features/administration/services/alert-threshold.source.ts`; sus simulados en `F/features/warehouse/mocks/` y `F/features/administration/mocks/` (datos ficticios, como los de los wireframes, sin personas reales).
- **Composables** nuevos por fuente en `F/features/warehouse/composables/` y `F/features/administration/composables/` (TanStack Query; invalidan el prefijo `['warehouse']` o `['alert-thresholds']` tras cada mutación).
- **Reglas puras:** `F/features/warehouse/utils/warehouse-clock.ts` (D32: minutos, nivel y texto «1 h 10» / «20 min»), `reception-form.ts` (validación del modal y de la página), `forklift-charge.ts` (base, IVA y total; modo según «Requiere factura»), `forklift-vehicle-type.ts` (D26: precarga y si se guarda).
- **Componentes** de D40 en `F/features/warehouse/components/`; `NoveltyFormDialog.vue` a dos columnas.
- **Compartido:** `F/components/app/AppChargeForm.vue` (D30) con su prueba.
- **Guardias:** `FT/unit/guards/list-pattern-routes.ts` (las rutas de §13.2) y `FT/unit/guards/mock-sources.spec.ts` (`MAQUETACION_PAGES` con las páginas de F04 mientras se maquetan).

---

## 4. Esquema y migraciones

Las genera el agente de backend con `dotnet ef`, en su fase, después de traer `fase-2` (§0.4). Las bases se recrean (`DEC-006`); no hay datos que convertir (§7).

**`AddWarehouseDelayAlerts` (BE-1):**
1. Tabla `warehouse_alert_thresholds`: `id` (uuid), `watched_record` (texto, único), `yellow_minutes` (int, nulo), `red_minutes` (int, nulo), `created_at`, `updated_at` (nulo). Semilla de tres filas con Id fijo y sin valores: `Reception`, `Loading`, `YardExit` (D1).
2. Tabla `warehouse_delay_alerts`: `id` (uuid), `watched_record` (texto), `record_id` (uuid), `clock_started_at` (timestamptz), `level` (texto: `Yellow` o `Red`), `notified` (bool: el rojo se registró con el amarillo sin avisarlo, D35), `created_at`. Índice único (`watched_record`, `record_id`, `clock_started_at`, `level`) e índice por `record_id`.

**`ReceptionPerEntry` (BE-2):**
1. `reception_logs`: `crew_id` (uuid, nulo, FK a `crews`, índice) y `stays_on_vehicle` (bool, no nulo; `false` en las filas existentes).
2. `warehouse_locations`: `is_system` (bool, no nulo; `false` en las filas existentes) y la semilla de `SOBRE-VEHICULO` («Sobre vehículo», capacidad 0 = sin tope, disponible, `is_system = true`, Id fijo). Si la tabla no tenía `HasData`, la columna nueva no lleva `HasDefaultValue` en el modelo (`D/contexto/convenciones-tecnicas.md` §5).

**`ForkliftRequiresInvoice` (BE-3):**
1. `forklift_uses`: `apply_vat` pasa a `requires_invoice` (renombre; si `dotnet ef` genera borrar y crear, se acepta: las bases se recrean).
2. `invoices`: `fiscal_number_not_applicable` (bool, no nulo; `false` en las filas existentes).

`dotnet ef migrations has-pending-model-changes` limpio al cerrar cada fase.

---

## 5. Pruebas

| Proyecto | Prueba (nueva o ajustada) | Escenario |
| --- | --- | --- |
| `Wms.Tests` | `WarehouseClockRulesTests` (nueva) | Minutos hacia abajo; sin umbrales `None`; justo en amarillo y en rojo; reloj detenido con su nivel; inicio futuro (0) |
| `Wms.Tests` | `AlertThresholdRulesTests` (nueva) | Los dos o ninguno; amarillo < rojo; 1 a 10.080; tres registros sin repetir; mensajes de C-F04-02 |
| `Wms.Tests` | `DelayAlertPlannerTests` (nueva) | Nada registrado y nivel amarillo → registra y avisa amarillo; rojo sin nada → registra los dos y avisa solo rojo; rojo con amarillo previo → solo rojo; nada que hacer |
| `Wms.Tests` | `PendingReceptionFiltersTests` (ajustada) | D14: con primer peso en el vínculo y sin ciclo; con ciclo; sin peso; anulada; recibida; depósito cerrado o anulado |
| `Wms.Tests` | `ReceptionRulesTests` (nueva) | Ubicación obligatoria salvo «sobre el vehículo»; tope por lo declarado; solo cantidades > 0 |
| `Wms.Tests` | `ForkliftVehicleTypeRulesTests` (nueva) | D26: precarga por nombre; se guarda solo si falta y existe; «Guacal / estiba» no se guarda |
| `Wms.Tests` | `ForkliftChargeRulesTests` (nueva; reemplaza las de `ForkliftVatCalculator` si cambian) | Con factura: IVA y `PendingBilling`; sin factura: 0 e `Immediate`; modo que no coincide |
| `Wms.IntegrationTests` | `AlertThresholdsEndpointTests` (nueva) | C-F04-01 y C-F04-02: Admin 200, otros 403, validaciones, auditoría |
| `Wms.IntegrationTests` | `WarehouseClockReadsTests` (nueva) | C-F04-03 a C-F04-05: el reloj y la recepción en las lecturas, con y sin umbrales; filtro `warehouseLevel` |
| `Wms.IntegrationTests` | `WarehouseDelayAlertServiceTests` (nueva) | `RunOnceAsync` con un `now` fijo: amarillo, rojo, sin repetir, sin umbrales, recepción hecha, salida reabierta; notificaciones a los usuarios activos de CE y Bodega |
| `Wms.IntegrationTests` | `ReceptionPerEntryTests` (nueva; absorbe `ReceptionShortageTests`, `ReceptionDateFilterTests` y `CargoUnitReceptionTests` donde registraban la llegada) | C-F04-06, C-F04-07, C-F04-09, C-F04-10, C-F04-11 y C-F04-12 en 404 |
| `Wms.IntegrationTests` | `DirectReceptionTests` (ajustada) | C-F04-08 con los campos nuevos y los errores |
| `Wms.IntegrationTests` | `WarehouseLocationSystemTests` (nueva) y `CatalogWriteAuthorizationTests` (ajustada) | C-F04-14 a C-F04-16; `POST` con Bodega 201 |
| `Wms.IntegrationTests` | `ForkliftUsesListTests`, `ForkliftUseTruckTests` (ajustadas) y `ForkliftRequiresInvoiceTests` (nueva) | C-F04-18 a C-F04-23 |
| `Wms.IntegrationTests` | `InventoryMovementsListTests` y `NoveltiesListTests` (nuevas) | C-F04-26 y C-F04-30: orden, filtros y 400 de C-F01-00 |
| Vitest | `FT/unit/warehouse/warehouse-clock.spec.ts`, `reception-form.spec.ts`, `forklift-charge.spec.ts`, `forklift-vehicle-type.spec.ts` (nuevas) | Las reglas puras del frontend |
| Vitest | `FT/unit/warehouse/mocks.spec.ts` y `FT/unit/administration/mocks.spec.ts` (nuevas o ampliadas) | Cada dato simulado pasa su esquema Zod |
| Vitest | `FT/unit/components/AppChargeForm.spec.ts` (ampliada) | Cambiar `paymentModes` cambia el modo elegido (D30) |
| Vitest | `FT/components/warehouse/*.spec.ts` (nuevas) | `ReceptionDialog` (ubicación obligatoria, «sobre el vehículo», unidades de carga), `ForkliftChargeDialog` (IVA y modo), `WarehouseClockTag` |
| Vitest | `FT/components/warehouse/ReceptionStepManualInfo.spec.ts`, `FT/unit/warehouse/manual-reception.spec.ts`, `pending-weighing.spec.ts`, `forklift-start.spec.ts`, `forklift-history.spec.ts` (se borran en I-04 con lo que prueban, §13.3) | — |

---

## 6. Casos QA

Formato de `PM/` §5.1. Los de la parte 1 se verifican por API (pruebas de integración HTTP contra Postgres) en la fase que los nombra; los de I-04, en el navegador, contra el backend local real y sin la sesión simulada.

### 6.1 Parte 1 (API)

| ID | Regla de origen | Precondición | Pasos | Resultado esperado | Verificación |
| --- | --- | --- | --- | --- | --- |
| QA2-F04-001 | AF-57, AF-128; D1, D33 | Base recién migrada | C-F04-01 con Admin; con un usuario Bodega | Tres filas sin valores; Bodega 403 | API (BE-1) |
| QA2-F04-002 | AF-57; D33 | Admin | C-F04-02 con 30/60, 45/90, 30/60; con 60/30; con solo amarillo; con dos filas | 200 y auditoría; 400 con los mensajes de la ficha | API (BE-1) |
| QA2-F04-003 | AF-56, AF-65; D14, D31 | Umbrales 30/60; entrada con primer peso hace 40 min, sin ciclo | C-F04-05 del depósito | `reception.status: Pending`, `clock.level: Yellow`, `elapsedMinutes: 40` | API (BE-1) |
| QA2-F04-004 | AF-66; D31 | Umbrales de cargue 45/90 y de patio 30/60; salida `Deposit` confirmada hace 100 min; salida `Global` confirmada hace 10 min | C-F04-03 y C-F04-04; después C-F01-104 (cargue) | `Loading` en `Red` y `YardExit` en `None`; tras el cargue, el reloj detenido con `stoppedAt`; en Borrador, `warehouseClock: null` | API (BE-1) |
| QA2-F04-005 | AF-57; D35, D36 | Umbrales 30/60; una entrada a 35 min; usuarios activos de CE y Bodega | `RunOnceAsync(now)` dos veces con el mismo `now` | Una fila `Yellow` y un aviso «Atraso de Bodega» a cada usuario activo de los dos roles; la segunda vuelta no avisa | API (BE-1) |
| QA2-F04-006 | AF-57; D35 | La entrada de 005 | `RunOnceAsync(now + 30 min)`; otra entrada nueva a 70 min sin avisos | Primera: fila y aviso `Red`. Segunda: filas `Yellow` y `Red`, un solo aviso (rojo) | API (BE-1) |
| QA2-F04-007 | D1, D35 | Sin umbrales; o una entrada recibida | `RunOnceAsync` | Ningún aviso ni fila | API (BE-1) |
| QA2-F04-008 | D31, D35 | Salida avisada en amarillo, reabierta y confirmada de nuevo | `RunOnceAsync` al cruzar otra vez | Aviso nuevo (otro inicio de reloj) | API (BE-1) |
| QA2-F04-009 | AF-58, AF-65; D14 | Camión con dos entradas (una con primer peso sin ciclo, otra con ciclo); una tercera entrada sin peso; una anulada | C-F04-06 | Dos filas (una por entrada con peso), con su reloj; ni la sin peso ni la anulada | API (BE-2) |
| QA2-F04-010 | AF-99; D23 | Varias entradas | C-F04-06 con `vehiclePlate`, `level=Red`, `sortField=weighedAt&sortOrder=desc`; con `sortField=foo` | Filtra y ordena; 400 «No se puede ordenar por «foo».» | API (BE-2) |
| QA2-F04-011 | AF-58, AF-61; D16 | Entrada de 009 | C-F04-07 con ubicación por producto; otra vez | 201; sale de C-F04-06; aparece en C-F04-09; la segunda, 409 | API (BE-2) |
| QA2-F04-012 | AF-61; D16 | Entrada pendiente | C-F04-07 sin ubicación; con más de lo declarado; con menos | 400 «Elija la ubicación de {producto}.»; 400 del tope; 201 y aviso de diferencia a CE | API (BE-2) |
| QA2-F04-013 | AF-119; D4, D19 | Entrada pendiente | C-F04-07 con `staysOnVehicle: true` y sin ubicaciones; C-F04-10 | 201; lo descargado queda en `SOBRE-VEHICULO`; el detalle trae `staysOnVehicle: true` | API (BE-2) |
| QA2-F04-014 | AF-60, AF-62; D17, D18 | Vehículo sin tipo; cuadrilla activa | C-F04-07 con `vehicleType: Sencillo` y `crewId` | El vehículo queda `Sencillo`; la recepción y el depósito con la cuadrilla | API (BE-2) |
| QA2-F04-015 | `DEC-010` (3); D16 | Entrada con unidades de carga | C-F04-07 con todas las unidades; con una menos | 201; 400 de hoy | API (BE-2) |
| QA2-F04-016 | AF-17, AF-64, AF-69; D20 | Ingreso «Solo bodega» de Vigilancia | C-F04-08 con documento y un producto; sin descripción; sin productos | 201 y depósito de inspección nuevo en Borrador con la descripción, la transportadora en la entrada y la recepción hecha; 400; 201 | API (BE-2) |
| QA2-F04-017 | D20 | Ingreso con motivo que requiere pesaje; ingreso ya recibido | C-F04-08 | 400 y 409 de hoy | API (BE-2) |
| QA2-F04-018 | AF-65; D15, D22 | — | C-F04-11 y C-F04-12; C-F04-09 con `kind=Direct` y orden; C-F04-13 con la placa de 009 | 404 y 404; el historial filtra y ordena; la búsqueda trae `vehicleType` y no trae llegada | API (BE-2) |
| QA2-F04-019 | D12, D19, D21 | Usuarios Bodega y Admin | C-F04-15 con Bodega; C-F04-16 sobre `SOBRE-VEHICULO` con Admin; C-F04-14 | 201; 409; la lista la trae con `isSystem: true` | API (BE-2) |
| QA2-F04-020 | `DEC-005`; D47 | Usuarios Vigilancia, Báscula y CE | C-F04-06 y C-F04-07 | 403 (como hoy: `WarehouseAccess`) | API (BE-2) |
| QA2-F04-021 | AF-63; D26, D27 | Vehículos sin tipo, con «VehParticular» y sin tipo para «Guacal / estiba» | C-F04-20 con `Tractomula`, con `Turbo` y con `GuacalEstiba` | El primero queda `Tractomula`; el segundo conserva su tipo; el tercero sigue sin tipo; los tres usos en curso | API (BE-3) |
| QA2-F04-022 | AF-105; D2, D25 | Uso en curso; IVA activo al 19 % | C-F04-21 con `requiresInvoice: true`, `PendingBilling` y 220.000 | Factura con IVA, sin pago, sin número; C-F04-18: `requiresInvoice: true`, `paidAmount: 0`, `invoiced: false` | API (BE-3) |
| QA2-F04-023 | AF-105; D3, D25 | Uso en curso | C-F04-21 con `requiresInvoice: false`, `Immediate` y 220.000 | Factura sin IVA, pagada, `fiscalNumberNotApplicable` y no fiscal; `paidAmount: 220000`, `invoiced: false` | API (BE-3) |
| QA2-F04-024 | D25 | Uso en curso | C-F04-21 con `requiresInvoice: true` e `Immediate` | 400 «Con factura, el cobro queda pendiente por facturar; sin factura, es de pago inmediato.» | API (BE-3) |
| QA2-F04-025 | D2 | IVA inactivo en el catálogo | C-F04-21 con factura | 400 de hoy («El impuesto IVA no está activo…») | API (BE-3) |
| QA2-F04-026 | AF-64; D28, D29 | Usos en curso y finalizados | C-F04-18 con `status=InProgress`; con `status=Ended,Complete&sortField=dateInit`; C-F04-22 y C-F04-23 | Filtra y ordena; 404 y 404 | API (BE-3) |
| QA2-F04-027 | D24 | Entrada con un uso en curso de su servicio | C-F04-06 | `forkliftInProgress: true` en su fila | API (BE-3) |
| QA2-F04-028 | AF-129; D42 | Movimientos de varios depósitos | C-F04-26 con `warehouseStorageNumber`, `movementType=In,Out`, `createdAtFrom`, `sortField=productName` | Filtra y ordena; `pageSize` > 50 se recorta | API (BE-3) |
| QA2-F04-029 | AF-129; D43 | Novedades, una anulada | C-F04-30 con `productName`, `type=Entry`, `includeVoided=false`, `sortField=startedAt` | Filtra y ordena; sin la anulada | API (BE-3) |
| QA2-F04-030 | D28 | Uso finalizado sin factura | C-F04-19 | La misma forma de C-F04-18; sin datos de la factura | API (BE-3) |

### 6.2 Integración I-04 (navegador)

| ID | Regla de origen | Precondición | Pasos | Resultado esperado | Verificación |
| --- | --- | --- | --- | --- | --- |
| QA2-F04-031 | AF-56, AF-57, AF-58; D23 | Umbrales 1/2 min en P-TR-08; dos entradas pesadas | Abrir Recepción, filtrar por placa y color, ordenar | Una fila por entrada; el tiempo sube y la fila pasa a amarillo y a rojo sin recargar | Pantalla |
| QA2-F04-032 | AF-59 a AF-62; D16, D17, D18 | Entrada pendiente | «Completar recepción»: cantidades, ubicación, cuadrilla, tipo de vehículo, firma y fotos | Sale de Recepción; aparece en el historial con la cuadrilla; el vehículo guarda el tipo | Pantalla y API |
| QA2-F04-033 | AF-119; D4, D19 | Entrada pendiente | Activar «Queda sobre el vehículo» y completar | Las ubicaciones se ocultan; el historial y el inventario muestran «Sobre vehículo» | Pantalla |
| QA2-F04-034 | `A/` §3.1; D12, D21 | Usuario Bodega | «+ Nueva posición» en el modal | La posición se crea y queda elegida | Pantalla |
| QA2-F04-035 | `DEC-010` (3) | Entrada con unidades de carga | Completar marcando cada unidad «Recibida completa» | Se guarda sin pedir cantidades | Pantalla |
| QA2-F04-036 | AF-64, AF-69; D5, D20 | Ingreso «Solo bodega» de Vigilancia | «Nueva recepción directa» → elegir el ingreso → completar la página → «Guardar» | Depósito de inspección en Borrador que CE ve; recargar la página no pierde el camión | Pantalla |
| QA2-F04-037 | AF-54; D20 | Usuario Bodega | En la recepción directa, «+» de conductor y de transportadora | Los crea y los deja elegidos | Pantalla |
| QA2-F04-038 | AF-59, AF-63; D24, D26 | Entrada pendiente de un vehículo sin tipo | «Montacargas» en la fila; iniciar con «Tractomula» | Placa, cliente y depósito precargados; el uso aparece «En curso»; el botón de la fila queda deshabilitado; el vehículo guarda el tipo | Pantalla |
| QA2-F04-039 | AF-105; D2, D25, D30 | Uso en curso | «Finalizar» con «Requiere factura» | El total suma el IVA; Facturación ve la factura pendiente de número | Pantalla |
| QA2-F04-040 | AF-105; D3, D25 | Uso en curso | «Finalizar» sin factura, con transferencia y referencia | Total sin IVA; «Pagado» con el valor y «Facturado: No» en Finalizados | Pantalla |
| QA2-F04-041 | AF-64; D7, D27, D28 | Usos en curso y finalizados | Montacargas: pestañas, filtros, «+ Registrar uso» por placa, «Ver» | El drawer muestra horas, «Pagado» y «Facturado», sin el detalle de la factura | Pantalla |
| QA2-F04-042 | AF-57, AF-128; D6 | Usuarios Admin y Bodega | Admin guarda umbrales en P-TR-08; Bodega abre `/admin/alert-thresholds` | Se guardan; Bodega no ve el ítem y la página la rechaza | Pantalla |
| QA2-F04-043 | AF-57; D35, D36 | Umbrales 1/2 min; trabajo corriendo en local | Dejar una entrada sin recibir 3 minutos | La campana de CE y de Bodega recibe «Atraso de Bodega» amarillo y luego rojo, una vez cada uno | Pantalla |
| QA2-F04-044 | AF-129, AF-130; D8, D22 | Recepciones hechas | Historial: filtros, orden, «Ver»; abrir `/warehouse/receptions/{id}` | Drawer con el detalle; la ruta vieja da 404 | Pantalla |
| QA2-F04-045 | AF-129; D42 | Depósito con stock y movimientos | Inventario: Existencias por depósito, Movimientos con orden en el servidor y «Exportar», Ubicaciones con su contenido | Cumple el patrón; sin tarjetas de estadísticas | Pantalla |
| QA2-F04-046 | AF-129, AF-130; D43 | Depósito con stock | Novedades: filtrar, crear (modal a dos columnas), editar, imprimir, anular | Cumple el patrón; las acciones de hoy siguen | Pantalla |
| QA2-F04-047 | AF-64, AF-127; D44, D45 | Usuarios Bodega y Admin | Ver el menú y el tablero de Bodega; abrir `/warehouse/receptions/entry` y `/warehouse/forklift/history` | Menú de D45; tablero con sus enlaces nuevos; las dos rutas dan 404 | Pantalla |
| QA2-F04-048 | `PM/` §6.3 | — | `yarn test` | La guardia list-pattern sin rutas de F04 en `PENDING`; `MAQUETACION_PAGES` vacía; ningún import de `mocks/` fuera de las pruebas | Vitest |
| QA2-F04-049 | `DEC-005`; D12, D18, D29 | Usuarios Vigilancia, CE y Facturación | «+» de transportadora en Vigilancia; detalle del depósito en CE (cuadrilla); Facturación › Facturas con los cobros de montacargas | Todo sigue como antes de F04 | Pantalla |
| QA2-F04-050 | AF-14, AF-31; D14 | Camión en Báscula | Registrar con primer peso, sin cobrar; mirar Recepción; cobrar y repesar sin recibir | La entrada aparece en Recepción desde el primer peso; Báscula no espera a Bodega | Pantalla |

---

## 7. Transición de datos

Le toca de `PM/` §7.2:

- **Llegadas a Bodega:** desaparecen y no se convierten (M18). El estado `InProgress` y la columna `arrival_at` quedan sin uso nuevo (D15).
- **Relojes:** arrancan con los registros nuevos (`PM/` §1.3). En el despliegue final no hay registros abiertos: staging se recrea y la carga del legacy solo trae maestros, depósitos y levantes (`B/Wms.Domain/Enums/LegacyImportEntity.cs:7-20`).
- **Umbrales:** sin valores en la semilla (D1); los del cliente se cargan en P-TR-08 en el paso 4 del despliegue final (`PM/` §7.3). Pendiente 1 de la matriz §4, sin cambio.
- **Importador del legacy:** la carga de ubicaciones (`LegacyImportEntity.Locations`) salta un código igual a `SOBRE-VEHICULO` y lo informa en su resultado (no se espera ninguno). No importa recepciones ni usos de montacargas: nada más cambia.
- **Facturas y usos de montacargas:** las bases locales se recrean; en staging no hay usos que convertir porque se recrea (M17).

---

## 8. Fases por parte

La parte 1 (backend) y la parte 2 (maquetación) corren en paralelo, una por repo (M10), y cierran por separado. Cada fase cierra con las compuertas de `PM/` §6.1 o §6.2, sus casos QA, commit y push de `f2/f04-bodega`, el estado aquí y en la matriz, y el reporte (una fase por turno, `PM/` §6).

| Fase | Parte | Contenido | Criterio de salida | Estado |
| --- | --- | --- | --- | --- |
| BE-1 | 1 | Umbrales, relojes y avisos (§8.1) | QA2-F04-001 a 008 en PASA por API | Hecha el 2026-11-25 (BE `fb707f7`). Estado en §8.1 |
| BE-2 | 1 | Recepción (§8.2) | QA2-F04-009 a 020 en PASA por API | Hecha el 2026-11-25 (BE `b80f8f4`). Estado en §8.2 |
| BE-3 | 1 | Montacargas, inventario y novedades (§8.3) | QA2-F04-021 a 030 en PASA por API | Pendiente |
| FE-1 | 2 | Contratos, fuentes simuladas, Recepción, modal y recepción directa (§8.4) | P-BOD-01 a P-BOD-03 con su lista del wireframe y captura | Hecha el 2026-11-25 (FE `b5c8e78`). Estado en §8.4 |
| FE-2 | 2 | Montacargas, Umbrales e historial de recepciones (§8.5) | P-BOD-04, P-BOD-05, P-TR-08 e historial con su lista y captura | Hecha el 2026-11-25 (FE `5722122`). Estado en §8.5 |
| FE-3 | 2 | Inventario y Novedades (§8.6) | Las dos con el patrón y captura | Pendiente |
| Revisión | — | Revisión del usuario con la sesión simulada (§8.7) | Visto bueno del usuario o plan de ajustes | Pendiente |
| I-04 (1) | 3 | Fuentes http y casos QA en el navegador (§13) | QA2-F04-031 a 046 y 049, 050 en PASA | Pendiente |
| I-04 (2) | 3 | Menú, enlaces, borrados, guardias y fusión (§13) | QA2-F04-047 y 048 en PASA; fusión en `fase-2` | Pendiente |

### 8.1 Backend, fase 1 — Umbrales, relojes y avisos

- **Decisiones:** D1, D10, D11, D14 (la regla de la entrada pendiente, que también usa BE-2), D31 a D37.
- **Endpoints:** C-F04-01 a C-F04-05 (fichas §2.2, grupo A; esquemas `clock.ts`, `alert-threshold.ts` y las extensiones de §2.3).
- **Archivos:** §3.2, «BE-1». **Migración:** `AddWarehouseDelayAlerts` (§4).
- **Trabajo en segundo plano:** `WarehouseDelayAlertBackgroundService` con `WarehouseDelayAlertService.RunOnceAsync(now)` (D35); registro en `B/Wms.Api/Program.cs` junto a los de `:81-87`. Las pruebas de integración llaman al servicio desde un *scope* del `WmsApiFactory` con un `now` fijo (los trabajos no corren en la suite, `WmsApiFactory.cs:122`) y cuentan las notificaciones por usuario.
- **Pruebas:** `WarehouseClockRulesTests`, `AlertThresholdRulesTests`, `DelayAlertPlannerTests`, `PendingReceptionFiltersTests` (ajustada), `AlertThresholdsEndpointTests`, `WarehouseClockReadsTests`, `WarehouseDelayAlertServiceTests` (§5).
- **Casos QA:** QA2-F04-001 a 008.
- **Nota:** el aviso usa el orquestador con roles fijos (D36); no se crea un tipo de notificación (F09).
- **Estado:** hecha el 2026-11-25 (BE `fb707f7`, rama `f2/f04-bodega`). QA2-F04-001 a 008 en PASA por API. `Wms.Tests` 2166 → 2218; `Wms.IntegrationTests` 766 → 776, todas en verde; migración `AddWarehouseDelayAlerts` (el contenido de §4) aplicada en local y `has-pending-model-changes` limpio. Pruebas de integración por endpoint: C-F04-01 y C-F04-02 en `AlertThresholdsEndpointTests`; C-F04-03 a C-F04-05 en `WarehouseClockReadsTests`; el trabajo en `WarehouseDelayAlertServiceTests` (`RunOnceAsync` con un `now` fijo desde un *scope* del `WmsApiFactory`, que excluye `WarehouseDelayAlertBackgroundService`). Unitarias: `WarehouseClockRulesTests`, `AlertThresholdRulesTests`, `DelayAlertPlannerTests`, `WarehouseDelayAlertMessagesTests` y `PendingReceptionFiltersTests` (reescrita con D14).
- **Cómo quedó:** reglas puras en `B/Wms.Application/Warehouse/Alerts/` (`WarehouseClockRules`, `AlertThresholdRules`, `DelayAlertPlanner`, `WarehouseDelayAlertMessages`); `WarehouseClockReader` arma los umbrales, los relojes abiertos y la recepción por entrada; `WarehouseDelayAlertService.RunOnceAsync` inserta la fila de `warehouse_delay_alerts` y solo avisa si entra (índice único); el trabajo corre cada `WarehouseAlerts:IntervalSeconds` (60). `PendingReceptionFilters.IsPendingReception` aplica D14 (primer peso del vínculo sin ciclo o primer pesaje del ciclo vigente; sin anulada, sin recepción activa, depósito abierto).
- **Notas para BE-2, FE-1 e I-04 (aplicadas por `DEC-002`):**
  - C-F04-02 valida en el handler con `BadRequestException`: el mensaje del contrato llega en `description` (no en `errors[]`), como los demás errores de negocio.
  - C-F04-06 (`GET warehouse/pending-from-weighbridge`) sigue listando solo entradas con ciclo hasta que BE-2 la rehaga: su proyección de hoy lee el camión y el peso del ciclo.
  - `reception.staysOnVehicle` sale `false` en las recibidas hasta que BE-2 agregue `ReceptionLog.StaysOnVehicle`; en las pendientes, `null`. «Recibida» = recepción activa en `Completed` (o `Unloaded`, de datos anteriores); una en curso (`InProgress`, que BE-2 retira) cuenta como pendiente.
  - `reception` también llega en las demás respuestas que usan `DepositStorageEntryDto` (C-F03-13 y las correcciones de la entrada), y `warehouseClock` en la respuesta del cargue (C-F01-104); sus esquemas lo aceptan o lo descartan.
  - El aviso sale por `NotifyRoleAsync` una vez por rol (ForeignTrade y Warehouse): un usuario con los dos roles recibe dos. Título «Atraso de Bodega»; el tiempo se escribe «40 min», «1 h», «1 h 5 min».

### 8.2 Backend, fase 2 — Recepción

- **Decisiones:** D4, D9, D12, D14 a D24, D47.
- **Endpoints:** C-F04-06 a C-F04-17 (fichas §2.2, grupo B; esquemas `reception.ts` y la extensión de `location.ts`).
- **Archivos:** §3.2, «BE-2». **Migración:** `ReceptionPerEntry` (§4).
- **Pruebas:** `ReceptionRulesTests`, `ReceptionPerEntryTests`, `DirectReceptionTests` (ajustada), `WarehouseLocationSystemTests`, `CatalogWriteAuthorizationTests` (ajustada) (§5). Las pruebas de hoy que registran la llegada (`ReceptionShortageTests`, `ReceptionDateFilterTests`, `CargoUnitReceptionTests`, `Weighbridge/WeighbridgeFlow.cs`, `ForeignTrade/ProductCorrectionNoticeTests.cs`) pasan a C-F04-07 en sus *helpers*, no prueba por prueba (como `P01/` §0.5).
- **Casos QA:** QA2-F04-009 a 020.
- **Nota:** el reloj de C-F04-06 y del historial sale de `WarehouseClockReader` (BE-1). La cuadrilla sigue también en el depósito (D18).
- **Estado:** hecha el 2026-11-25 (BE `b80f8f4`, rama `f2/f04-bodega`). QA2-F04-009 a 020 en PASA por API (018 con el 405 de C-F04-11, aceptado por el usuario). `Wms.Tests` 2218 → 2242; `Wms.IntegrationTests` 776 → 804, todas en verde; migración `ReceptionPerEntry` (el contenido de §4, más el ajuste del check de capacidad de abajo) aplicada en local y `has-pending-model-changes` limpio. Pruebas de integración por endpoint: C-F04-06, C-F04-07, C-F04-09 a C-F04-13 en `ReceptionPerEntryTests`; C-F04-08 en `DirectReceptionTests` (reescrita); C-F04-14 a C-F04-16 en `WarehouseLocationSystemTests`, `CatalogWriteAuthorizationTests` y `CatalogPoliciesTests`; las unidades de carga (QA2-F04-015) en `CargoUnitReceptionTests`. Unitarias: `ReceptionRulesTests` (nueva) y los validadores de C-F04-07 y C-F04-08.
- **Cómo quedó:** `CreateReceptionCommand` recibe la entrada (`warehouseStorageEntryId`) y aplica D14 a D19 con la regla pura `ReceptionRules` (ubicación obligatoria salvo «sobre el vehículo», tope por lo declarado para el camión, tipo de vehículo del catálogo); `ReceptionLog` suma `CrewId` y `StaysOnVehicle` y pierde `RegisterArrival`; `WarehouseLocation` suma `IsSystem` y la semilla `SOBRE-VEHICULO` (Id `f04b0001-5ab0-4e00-9000-000000000001`), con 409 al editar, desactivar o borrar. La recepción directa crea siempre el servicio `INSP` y el depósito de inspección sin cliente, con el documento en el servicio (número y tipo, como Báscula), la transportadora en la entrada y las cantidades declaradas también en `WarehouseStorageEntryProduct` (antes no se guardaban por camión). `register-arrival`, `{id}/complete` y sus comandos, validadores y pruebas se borraron; los *helpers* de la suite reciben con C-F04-07 (`ReceptionScenario`, `WeighbridgeFlow.ReceiveTruckAsync`); `ModifyWeightMerchandiseTests` recibe después de pesar (D14). El importador del legacy rechaza la fila con código `SOBRE-VEHICULO` y lo informa en el lote. `reception.staysOnVehicle` de C-F04-05 ya sale de la recepción.
- **Notas para BE-3, FE e I-04 (aplicadas por `DEC-002` o por el comportamiento de la plataforma):**
  - **C-F04-11:** `POST warehouse/receptions/register-arrival` responde **405**, no 404: el camino lo cubre `GET receptions/{id:guid}` y ASP.NET responde «método no permitido», como las facturas manuales retiradas (`ManualInvoiceRemovedTests`). C-F04-12 (`{id}/complete`) sí responde 404. Nadie llama ya a ninguno de los dos. **Aceptado por el usuario el 2026-11-25** («Aceptar el 405»): C-F04-11 y QA2-F04-018 quedan con 405; I-04 no lo cambia.
  - **Check de capacidad:** `chk_warehouse_location_capacity_positive` pasa a `capacity > 0 OR is_system`, porque §4 siembra `SOBRE-VEHICULO` con capacidad 0 y la restricción de hoy lo impedía. Crear o editar una ubicación sigue exigiendo capacidad mayor que cero.
  - **Firma:** en C-F04-07 y C-F04-08 es opcional, como en el completar de hoy (`{id}/complete`, el flujo que usaba la pantalla); el `POST receptions` de antes la exigía.
  - **Entrada sin productos:** una inspección registrada en Báscula sin productos (`P01/` D23) se recibe sin contar nada; «Debe indicar al menos un producto…» aplica solo si el depósito tiene productos. El tope por lo declarado aplica solo a los productos que la entrada declara.
  - **Lista de Recepción:** `products` son los declarados para la entrada (si la entrada no declara ninguno, los del depósito, sin cantidad); `merchandiseText` es «Producto · Embalaje» separado por comas; `customerName` y `customerId` son los de la factura de báscula de la entrada o los del servicio; `merchandise` filtra por nombre o descripción del producto. El filtro `level` sigue las franjas de BE-1 (`StartRangeFor`).
  - **Historial:** «Directa» es la recepción cuya entrada no tiene primer peso; `receivedAt` es la hora de la recepción completada. El detalle (C-F04-10) conserva los campos de hoy (estado, desglose por producto, unidades de carga y fotos) y suma los del contrato; su 404 ahora es *ProblemDetails* con «La recepción no existe.».
  - **Búsqueda por placa:** `deposits[]` trae solo las entradas no anuladas que esperan su recepción (D14) o ya recibidas; `message` ya no habla de la llegada.

### 8.3 Backend, fase 3 — Montacargas, inventario y novedades

- **Decisiones:** D2, D3, D7, D25 a D29, D42 y D43 (su parte de API).
- **Endpoints:** C-F04-18 a C-F04-31 (fichas §2.2, grupos C y D; esquemas `forklift.ts`, `inventory.ts` y `novelty.ts`).
- **Archivos:** §3.2, «BE-3». **Migración:** `ForkliftRequiresInvoice` (§4).
- **Pruebas:** `ForkliftVehicleTypeRulesTests`, `ForkliftChargeRulesTests`, `ForkliftUsesListTests` y `ForkliftUseTruckTests` (ajustadas), `ForkliftRequiresInvoiceTests`, `InventoryMovementsListTests`, `NoveltiesListTests` (§5).
- **Casos QA:** QA2-F04-021 a 030.
- **Nota:** Facturación de hoy muestra la factura sin factura como no fiscal (`IsNonFiscal`); el rótulo «No aplica» y las columnas de «Requiere factura» son de F08 (P-FAC-02).

### 8.4 Maquetación, fase 1 — Contratos, fuentes simuladas, Recepción, modal y recepción directa

- **Decisiones:** D4, D5, D14, D16, D17, D19 a D24, D32, D37 a D41.
- **Contratos:** todos los de §2.3 (también los de FE-2 y FE-3, para que una sola fase fije la forma), con sus datos simulados y `FT/unit/warehouse/mocks.spec.ts`.
- **Fuentes:** `reception.source.ts` y la fachada `catalog.source.ts` (D41), con sus simulados.
- **Pantallas:** P-BOD-01 (`F/pages/warehouse/receptions/index.vue`), P-BOD-02 (`ReceptionDialog`) y P-BOD-03 (`F/pages/warehouse/receptions/direct/[entryLogId].vue`), con `DirectReceptionEntryPicker`. Cada una cumple su lista del wireframe (`D/levantamiento-2026-11/fase_2-mockups/bodega.html`, P-BOD-01 a P-BOD-03; `A/` §2.2 g) y se captura en `D/planes/sprint-11/f04-bodega/evidencias/fe1-*`.
- **Componentes:** `WarehouseClockTag` (y su ejemplo en la galería), `ReceptionDialog`, `ReceptionProductRows`, `LocationQuickDialog`, `DirectReceptionEntryPicker`, `DirectReceptionTruckSection`, `DirectReceptionGoodsSection`; reglas `warehouse-clock.ts` y `reception-form.ts` con sus pruebas. Configuración › Ubicaciones oculta las acciones de la ubicación del sistema (C-F04-14).
- **Guardias:** las páginas nuevas y rehechas entran a `MAQUETACION_PAGES`. La recepción directa no está en el menú: la guardia list-pattern no la lista.
- **Sin llamadas reales y sin menú** (`PM/` §6.2): las páginas viejas (`entry.vue`, `[id].vue`) se quedan hasta I-04; `index.vue` se rehace en su ruta (M11). La sesión simulada de `P02/` D10 (`NUXT_PUBLIC_MOCK_SESSION=true`, `?roles=Admin,Warehouse`).
- **Estado:** hecha el 2026-11-25 (FE `b5c8e78`, rama `f2/f04-bodega`). `yarn build` con código 0; `yarn test` 139 → 145 archivos y 711 → 740 pruebas, todas en verde; las guardias de `FT/unit/guards/` en verde (35); `yarn lint` 212 → 210 errores, ninguno en archivos nuevos; los datos simulados pasan sus esquemas (`FT/unit/warehouse/mocks.spec.ts`, `FT/unit/administration/mocks.spec.ts`). `yarn test` sale con código 1 antes y después por un error no controlado heredado de `FT/components/weighbridge/WeighbridgeQueuePage.spec.ts` (`localStorage.getItem is not a function`, de F03), que no hace fallar ninguna prueba. Capturas en `evidencias/fe1-01` a `fe1-07`.
- **Cómo quedó:** contratos de §2.3 en `F/features/warehouse/contracts/` (`clock.ts`, `reception.ts`, `forklift.ts`, `inventory.ts`, `novelty.ts`), `F/features/administration/contracts/alert-threshold.ts` y las extensiones de `exit.ts` (`warehouseClock`, `warehouseLevel`), `deposit-entry.ts` (`depositEntryWithReceptionSchema`) y `location.ts` (`isSystem`); `reception-deps.ts` con C-F01-146 y C-F01-152 (forma de hoy); semillas de FE-2 y FE-3 (`mocks/data/forklift.ts`, `inventory.ts`, `novelty.ts` y `F/features/administration/mocks/data/alert-threshold.ts`), validadas con sus esquemas, para que FE-2 y FE-3 armen sus fuentes. Fuentes `reception.source.ts` y `catalog.source.ts` (simuladas), consultas en `composables/reception.queries.ts` (prefijo `['warehouse']`) y búsquedas en `useWarehouseCatalogSearch.ts`. Reglas `warehouse-clock.ts` y `reception-form.ts` con sus pruebas. Los simulados usan umbrales de recepción de 15 y 60 min para ver los tres colores.
- **Lista del wireframe:**
  - P-BOD-01: las siete columnas y sus filtros (rango, placa, número, nombre, producto y color), orden por defecto `weighedAt asc`, reloj que se refresca cada minuto, «Completar recepción» y «Montacargas» de solo icono con tooltip, «+ Nueva recepción directa» en la barra. Capturas `fe1-01` y `fe1-04`.
  - P-BOD-02: encabezado con «Pendiente», placa, pesaje y depósito (más el reloj); información verificada en báscula (conductor, transportadora, declarado y peso físico neto con el stock); tipo de vehículo precargado; «Queda sobre el vehículo»; por producto, lo declarado, la cantidad con su máximo y «✓ Coincide», la ubicación con «+ Nueva posición»; observaciones, cuadrilla y nota; firma con «Limpiar» y «Capturar»; fotos N / 5; pie con «Cancelar», «Total a recibir · ubicación» y «Completar recepción». Con unidades de carga, una casilla «Recibida completa» por unidad. Capturas `fe1-02` y `fe1-03`.
  - P-BOD-03: sin tarjeta de título (`<h1 class="sr-only">`), «Excepcional», «Volver a Recepciones» y «Guardar» en la barra; 1 camión y conductor (resumen con «Editar», precargado del ingreso y del vehículo; altas rápidas) con el tipo de vehículo; 2 documento (carta porte o guía de transporte y su número), modalidad «INSP · Inspección» y descripción obligatoria con su nota; 3 mercancía declarada con «+ Agregar producto»; 4 «Queda sobre el vehículo», cantidad con «Copiar (N)», ubicación, cuadrilla y observaciones; al lado, firma («Capturada», «Recapturar firma») y fotos. Capturas `fe1-05` y `fe1-06`.
- **Diferencias con el wireframe y casos borde (`DEC-002`):**
  - P-BOD-02 no muestra el NIT de la transportadora ni «Disp.» de la ubicación: C-F04-06 solo trae `carrierCompanyName` y C-F04-14 trae la capacidad, que se muestra como «Capacidad: N kg». Las observaciones van una vez por recepción (C-F04-07 tiene un solo `comments`), no dentro de cada producto.
  - «Montacargas» deshabilitado (D24): `AppRowActions` no tiene acciones deshabilitadas y no se cambia (D39); la fila con uso en curso oculta la acción del menú y muestra al lado un botón deshabilitado con el mismo estilo y el tooltip «Montacargas en curso». En FE-1 la acción habilitada solo avisa que el modal llega en FE-2.
  - La fachada (D41) suma el ingreso de Vigilancia (C-F03-48) y el vehículo (C-F01-23), que P-BOD-03 necesita para precargar conductor, transportadora, país y tipo al recargar la página.
- **Notas para FE-2, FE-3 e I-04:**
  - FE-2 conecta «Montacargas» de la fila a `ForkliftStartDialog` (`F/pages/warehouse/receptions/index.vue`, `onRowAction`) y suma a `reception.source.ts` el historial, el detalle y la búsqueda por placa; las recepciones hechas en la pestaña quedan en `mocks/world.ts` (`receptions`).
  - I-04 escribe `reception.http.ts` con C-F04-06 a C-F04-08, C-F01-146 y C-F01-152, pasa los usos de `catalog.source.ts` y `useWarehouseCatalogSearch.ts` a las fuentes integradas de F01 y F03 y los borra, y saca las dos páginas de `MAQUETACION_PAGES`. El formato del reloj en pantalla sigue el wireframe («1 h 10»); el texto del aviso del backend es «1 h 10 min» (nota de BE-1).

### 8.5 Maquetación, fase 2 — Montacargas, Umbrales e historial de recepciones

- **Decisiones:** D6 a D8, D22, D25 a D30, D33.
- **Fuentes:** `forklift.source.ts` y `alert-threshold.source.ts`, con sus simulados; `reception.source.ts` suma el historial y el detalle.
- **Pantallas:** P-BOD-04 (`ForkliftStartDialog`, `ForkliftChargeDialog`, también desde la fila de P-BOD-01), P-BOD-05 (`F/pages/warehouse/forklift/index.vue` como listado, D7, con `ForkliftUseDetail`), P-TR-08 (`F/pages/admin/alert-thresholds/index.vue`) y Entradas › Historial (`F/pages/warehouse/receptions/history.vue` con `ReceptionDetail`). Captura en `evidencias/fe2-*`.
- **Compartido:** el cambio de `AppChargeForm` de D30, con su prueba.
- **Reglas:** `forklift-charge.ts` y `forklift-vehicle-type.ts`, con sus pruebas.
- **Guardias:** `F/pages/warehouse/forklift/index.vue` y `F/pages/admin/alert-thresholds/index.vue` entran a `MAQUETACION_PAGES`; `/warehouse/forklift` pasa de `OUTSIDE` (`list-pattern-routes.ts:75`) a `PENDING` con «F04», porque deja de ser formulario; I-04 la pasa a `PATTERN`. `/admin/alert-thresholds` no está en el menú hasta I-04, que la agrega a `OUTSIDE`.
- **Estado:** hecha el 2026-11-25 (FE `5722122`, rama `f2/f04-bodega`). `yarn build` con código 0; `yarn test` 145 → 149 archivos y 740 → 760 pruebas, todas en verde (sale con código 1 antes y después por el error no controlado heredado de `FT/components/weighbridge/WeighbridgeQueuePage.spec.ts`, que no hace fallar ninguna prueba); las guardias de `FT/unit/guards/` en verde (35); `yarn lint` 210 → 210 errores, ninguno en archivos nuevos; los datos simulados pasan sus esquemas (`FT/unit/warehouse/forklift-mocks.spec.ts`, nueva). Capturas en `evidencias/fe2-01` a `fe2-10`. Verificado en `yarn dev` con la sesión simulada: sin llamadas al API ni errores en consola; Umbrales con `?roles=Warehouse` lleva a «Acceso denegado».
- **Cómo quedó:** fuentes `forklift.source.ts` (C-F04-18 a C-F04-25) y `F/features/administration/services/alert-threshold.source.ts` (C-F04-01, C-F04-02) con sus simulados; `reception.source.ts` suma `history`, `detail` y `searchPlate` (C-F04-09, C-F04-10, C-F04-13). Consultas en `composables/forklift.queries.ts` (prefijo `['warehouse', 'forklift']`; las pestañas cuentan con `pageSize=1`) y `F/features/administration/composables/alert-threshold.queries.ts` (`['alert-thresholds']`). Componentes `ForkliftStartDialog`, `ForkliftChargeDialog`, `ForkliftUseDetail` y `ReceptionDetail`; reglas `forklift-charge.ts`, `forklift-vehicle-type.ts` y `forklift-truck.ts` (el camión con que abre «Iniciar uso»). El mundo simulado (`mocks/world.ts`) suma `history` (cinco recepciones de `mocks/data/reception-history.ts`; las hechas en la pestaña entran arriba con su detalle) y `forkliftUses`; «Montacargas en curso» de la fila de Recepción y su tipo de vehículo salen de esos usos y del vehículo vivo, y el reloj de Recepción toma los umbrales simulados de P-TR-08 (cambiarlos se ve en la lista). `AppChargeForm` sigue los cambios de `paymentModes` (D30), con su prueba en `FT/unit/components/AppChargeForm.spec.ts`. Pruebas nuevas: `forklift-charge.spec.ts`, `forklift-vehicle-type.spec.ts`, `forklift-mocks.spec.ts` y `FT/components/warehouse/ForkliftChargeDialog.spec.ts`.
- **Lista del wireframe:**
  - P-BOD-04 «Iniciar uso»: placa precargada desde Recepción («Precargada desde Recepción») o buscada con «Buscar» y el depósito elegido entre los del camión (con «Montacargas en curso» deshabilitado); «Cliente · Depósito»; horómetro inicial con decimales; tipo de vehículo precargado y la nota de D26 si el vehículo no tiene tipo; observaciones; «Cancelar» e «Iniciar uso». Capturas `fe2-03` y `fe2-06`.
  - P-BOD-04 «Facturación y cobro — Montacargas»: horómetro inicial → final · horas · tipo; observaciones; valor del servicio (base editable, precargada con la tarifa); «Requiere factura» en lugar del check «Agregar IVA» (D25) con valor, IVA y total; destinatario (tercero registrado con «+», conductor, persona no registrada, consumidor final), método y total de `AppChargeForm`; «Finalizar y cobrar». Captura `fe2-04`.
  - P-BOD-05: pestañas «En curso» y «Finalizados» con su contador; En curso: inicio, placa, tipo, cliente, depósito, horómetro inicial, «Finalizar» y «Ver»; Finalizados: inicio, fin, placa, tipo, cliente, horas, «Pagado» y «Facturado» (Sí o No), «Ver»; filtros en la columna; «+ Registrar uso» en la barra; drawer con el camión, el uso y el cobro informativo. Capturas `fe2-01`, `fe2-02` y `fe2-05`.
  - Entradas › Historial: recibida, vehículo, depósito, cliente, mercancía (con «Sobre vehículo» y «Diferencia»), cantidad recibida, tipo (báscula o directa) y tiempo desde el pesaje, con filtros (rango, placa, número, nombre, producto y tipo); «Ver» de solo icono con drawer `?id=` (recepción, camión y depósito, productos con declarado, contado, diferencia y ubicación, unidades de carga, firma y fotos). Capturas `fe2-07` y `fe2-08`.
  - P-TR-08: sin tarjeta de título (`<h1 class="sr-only">`), «Guardar» (y «Descartar cambios») en la barra de arriba a la derecha; registro vigilado, cuenta desde, amarillo a los y rojo a los en minutos (`InputNumber` es-CO), con el resultado y la fecha de la última actualización por fila; los mensajes de C-F04-02; la nota de AF-57. Capturas `fe2-09` y `fe2-10`.
- **Diferencias con el wireframe y casos borde (`DEC-002`):**
  - El cobro no ofrece «Conductor del vehículo»: `forkliftUseSchema` (C-F04-18) solo trae `driverName`, sin el documento que `AppChargeForm` necesita para precargarlo; la opción queda deshabilitada. Si se quiere, I-04 o un ajuste puede sumar el documento al contrato.
  - «Facturado» muestra «Sí» o «No» (D28); en el drawer, un uso con factura y sin N.º SIGO dice «No · pendiente de número». El rótulo «No aplica» es de F08 (D3).
  - La base precargada es `ratePerHour`, que es el valor fijo del servicio por tipo de vehículo (como hoy en `ForkliftUseDialog.vue:211-218`), no una tarifa por hora.
- **Notas para FE-3 e I-04:**
  - I-04 escribe `forklift.http.ts` (C-F04-18 a C-F04-25, con el `status` de las pestañas como `InProgress` o `Ended,Complete`), `alert-threshold.http.ts` (C-F04-01, C-F04-02) y en `reception.http.ts` suma C-F04-09, C-F04-10 y C-F04-13; saca de `MAQUETACION_PAGES` `forklift/index.vue`, `receptions/history.vue` y `admin/alert-thresholds/index.vue`; pasa `/warehouse/forklift` a `PATTERN` y agrega `/admin/alert-thresholds` a `OUTSIDE` con el menú (D45). `searchStakeholders` de `useWarehouseCatalogSearch.ts` (tercero del cobro) pasa a la fuente integrada de terceros.
  - El reloj simulado de Recepción lee los umbrales de `F/features/administration/mocks/alert-threshold.mock.ts`; con el API real cada reloj trae los suyos (D33) y ese enlace desaparece con los `mocks/`.

### 8.6 Maquetación, fase 3 — Inventario y Novedades

- **Decisiones:** D42, D43.
- **Fuentes:** `inventory.source.ts` y `novelty.source.ts`, con sus simulados.
- **Pantallas:** Inventario (`F/pages/warehouse/inventory/index.vue`) y Novedades (`F/pages/warehouse/novelties/index.vue`) con el patrón; `NoveltyFormDialog` a dos columnas. Captura en `evidencias/fe3-*`.
- **Nota:** confirma los límites de texto de `noveltyInputSchema` contra `NoveltyInputValidator.cs` (§2.3).

### 8.7 Revisión del usuario (después de FE-3)

Con FE-1 a FE-3 cerradas y con push, el usuario revisa las pantallas en `yarn dev` con la sesión simulada (`?roles=Admin,Warehouse` y `?roles=Admin`) antes de I-04. Si pide ajustes, van en un plan de ajustes de la maquetación, como `AUI/` en F03, y se ejecutan en `f2/f04-bodega` antes de I-04. El agente de maquetación, al cerrar FE-3, le dice al usuario qué rutas abrir y con qué roles.

---

## 9. Riesgos

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R1 | El trabajo de los relojes envía correos de más (umbrales bajos, muchas entradas abiertas) | Un aviso por nivel y por reloj (índice único, D35); sin umbrales no hace nada (D1); F09 hará el canal configurable. En la QA local se usan umbrales bajos solo en QA2-F04-043 |
| R2 | Dos instancias del API avisan dos veces | El aviso sale solo si la fila entra (índice único, D35) |
| R3 | La lista de Recepción cambia de criterio (sin ciclo) y deja de cuadrar con Báscula | D14 es una regla pura con pruebas de borde; QA2-F04-050 lo verifica en el navegador |
| R4 | Quitar la llegada rompe lectores que la usan (CE, trazabilidad, estadísticas) | Se conservan la columna y el estado (D15); los lectores no cambian; la suite completa en BE-2 |
| R5 | La ubicación del sistema se borra o se edita por Configuración | Guardas del dominio y 409 (C-F04-16); la pantalla oculta las acciones (D19) |
| R6 | El cambio de `AppChargeForm` afecta el cobro de Báscula | Cambio mínimo (seguir `paymentModes`), con prueba; Báscula pasa una lista fija y no cambia de modo |
| R7 | El contrato de las salidas y las entradas del depósito (F05, F06) se escribe antes de sus pantallas | F05 y F06 pueden agregar campos; no cambian `warehouseClock` ni `reception` sin una decisión nueva (`PM/` R3) |
| R8 | `exitSchema` y `locationSchema` ganan un campo obligatorio y fallan contra un backend sin F04 | Los dos repos se fusionan juntos en I-04; I-04 verifica la búsqueda por placa de Báscula (C-F01-101) y Configuración › Ubicaciones |
| R9 | El reloj de la pantalla y el del servidor no coinciden | La misma regla en los dos lados (D32); la pantalla parte de `startedAt` y de los umbrales que trae cada fila |
| R10 | Videos y manuales de Bodega quedan desactualizados | Lista en el despliegue final (`PM/` R13) |

---

## 10. Fuera de alcance

- Las salidas de Bodega (P-BOD-06 a P-BOD-09, «Órdenes de salida» y «Salidas» en el menú) y el retiro de «Órdenes de cargue» (F06); la etapa Bodega del detalle de CE (F05). F04 solo les deja los relojes (D37).
- La fórmula «descargada o sobre vehículo» (F07, AF-116, AF-120) y las columnas de «Requiere factura» y el rótulo «No aplica» en Facturación (F08, P-FAC-02).
- Los tipos de notificación configurables y el canal por tipo (F09).
- Llevar el porcentaje de IVA al precio (F07, `PM/` §3.4).
- Borrar `BillingCollectForm` y `useUnitMeasures` (D46).
- Staging, el despliegue final (`PM/` §7.3) y estimar esfuerzo.

**Cambios al hub** (aprobados por el usuario el 2026-11-25, «Aprobar con §10»; los aplica I-04 al cerrar, §13.4):

1. `D/contexto/convenciones-tecnicas.md` §4, tabla de políticas, después de `InventoryReportAccess`: «| `LocationCreateAccess` | Admin, ForeignTrade, Billing, Warehouse (crear una ubicación desde la recepción de Bodega, `POST warehouse/locations`; editar y borrar siguen en `ConfigurationAccess`) |».
2. `D/contexto/convenciones-tecnicas.md` §6, tabla de trabajos, al final: «| `WarehouseDelayAlertBackgroundService` | Relojes de Bodega: cada minuto (`WarehouseAlerts:IntervalSeconds`) avisa «Atraso de Bodega» a CE y Bodega al cruzar el umbral amarillo o rojo de la recepción, el cargue o la salida de patio; un aviso por nivel y por reloj (`warehouse_delay_alerts`) |».

---

## 11. Prompts por parte

- Parte 1 (backend): [prompt-f2-f04-bodega-backend-2026-11-25.md](prompt-f2-f04-bodega-backend-2026-11-25.md), rama `f2/f04-bodega` del backend.
- Parte 2 (maquetación): [prompt-f2-f04-bodega-maquetacion-2026-11-25.md](prompt-f2-f04-bodega-maquetacion-2026-11-25.md), rama `f2/f04-bodega` del frontend.
- Parte 3 (I-04): [prompt-f2-f04-bodega-integracion-2026-11-25.md](prompt-f2-f04-bodega-integracion-2026-11-25.md), las dos ramas.
- Planificador (ejecutado): [prompt-f2-f04-bodega-planificador-2026-11-25.md](prompt-f2-f04-bodega-planificador-2026-11-25.md).

---

## 12. Mensajes de commit sugeridos

Cada uno termina con la línea de coautoría que indique la sesión.

| Fase | Repo | Mensaje |
| --- | --- | --- |
| BE-1 | BE | `feat(bodega): umbrales de alertas, relojes de recepción, cargue y salida de patio, y aviso de atraso de Bodega (DEC-080, F04)` |
| BE-2 | BE | `feat(bodega): recepción por entrada sin llegada, recepción directa de inspección, «sobre el vehículo» y cuadrilla por recepción (DEC-080, F04)` |
| BE-3 | BE | `feat(bodega): montacargas con «Requiere factura», listado con orden y filtros, e inventario y novedades con el patrón (DEC-080, F04)` |
| FE-1 | FE | `feat(bodega): maquetación de Recepción, la recepción física y la recepción directa con datos simulados (DEC-080, F04)` |
| FE-2 | FE | `feat(bodega): maquetación de Montacargas, Umbrales de alertas y el historial de recepciones (DEC-080, F04)` |
| FE-3 | FE | `feat(bodega): maquetación de Inventario y Novedades con el patrón de listado (DEC-080, F04)` |
| I-04 | BE y FE | `feat(bodega): integración de F04 con el API (DEC-080, F04)` (FE) y `merge: I-04, F04 «Bodega» en fase-2 (DEC-080, DEC-081)` (fusión) |
| Cada fase | docs | `docs(f04): fase N de F04 cerrada (sprint 11)` |

---

## 13. Integración I-04 (parte 3)

Un agente con los dos repos (M1, M10), cuando BE-1 a BE-3 y FE-1 a FE-3 están cerradas y con push, y la revisión de §8.7 tiene el visto bueno del usuario (o su plan de ajustes, ejecutado). Ocupa los dos repos. Va en dos fases: I-04 (1), §13.1 y §13.4; I-04 (2), §13.2, §13.3 y §13.5.

### 13.1 Fuentes http

Por cada `*.source.ts` de F04, escribe su `*.http.ts` con `contractApi` (`F/shared/http/contract-api.ts`) y los esquemas de §2.3 (`.parse` en cada respuesta; un fallo de esquema se registra en consola y se muestra como error del API), cambia la línea activa y la agrega a `INTEGRATED_SOURCES` (`FT/unit/guards/mock-sources.spec.ts:22`):

| Fuente | Endpoints | Pantallas |
| --- | --- | --- |
| `F/features/warehouse/services/reception.source.ts` | C-F04-06 a C-F04-10, C-F04-13, C-F04-17; C-F01-146, C-F01-152 | P-BOD-01 a P-BOD-03, historial |
| `forklift.source.ts` | C-F04-18 a C-F04-21, C-F04-24, C-F04-25 | P-BOD-04, Montacargas |
| `inventory.source.ts` | C-F04-26 a C-F04-29; C-F01-148 | Inventario |
| `novelty.source.ts` | C-F04-30, C-F04-31 | Novedades, Inventario |
| `F/features/administration/services/alert-threshold.source.ts` | C-F04-01, C-F04-02 | P-TR-08 |
| `location.source.ts` (de F01, ya integrada) | C-F04-14, C-F04-15, C-F04-16: actualiza su esquema (`isSystem`) | P-BOD-02, P-BOD-03, Configuración › Ubicaciones |
| `catalog.source.ts` (fachada, D41) | — | Se borra: sus usos pasan a las fuentes integradas de F01 y F03 (`location`, `crew`, `driver`, `stakeholder`, `product`, `packaging-type` y la de tipos de documento; C-F01-15, 17, 25, 26, 29, 52, 69, 141; C-F03-44) |

Verifica además que la búsqueda por placa de Báscula (C-F01-101) y la lectura de la entrada de Báscula (C-F03-13) siguen pasando sus esquemas con los campos nuevos (R8).

### 13.2 Menú, rutas, enlaces y guardias

- `F/components/layout/menu-model.ts:60-88`: Bodega con Dashboard · Entradas ▸ Recepción (`/warehouse/receptions`), Historial (`/warehouse/receptions/history`) · Montacargas (`/warehouse/forklift`) · Órdenes de cargue · Inventario · Novedades (D45). `:201-208`: Administración con Usuarios · Auditoría · Umbrales de alertas (`/admin/alert-thresholds`).
- `F/pages/warehouse/index.vue:13-55`: las tarjetas de D44.
- `FT/unit/guards/list-pattern-routes.ts`: salen de `PENDING` las rutas de F04 (las seis de `:38-44` y `/warehouse/forklift`, que FE-2 agregó); entran a `PATTERN` `/warehouse/receptions`, `/warehouse/receptions/history`, `/warehouse/forklift`, `/warehouse/inventory` y `/warehouse/novelties`; `/warehouse/forklift` sale de `PENDING` (FE-2 la pasó de `OUTSIDE`); entra a `OUTSIDE` `/admin/alert-thresholds` («Formulario de configuración: umbrales de alertas»); la recepción directa no está en el menú y no se lista; salen `/warehouse/receptions/entry` y `/warehouse/forklift/history`.
- `MAQUETACION_PAGES` (`FT/unit/guards/mock-sources.spec.ts:16`) queda vacía.

### 13.3 Se borra

Con `rm`, después de comprobar con grep que nada fuera de lo que se borra los importa (trampas 4 y 7):

- **Páginas:** `F/pages/warehouse/receptions/entry.vue`, `F/pages/warehouse/receptions/[id].vue` (D8) y `F/pages/warehouse/forklift/history.vue` (D7).
- **Componentes de Bodega que solo usaban las pantallas viejas:** `ReceptionStepCompletion`, `ReceptionStepManualInfo`, `PendingFromWeighbridgeList`, `DirectReceptionList`, `ReceptionList`, `ReceptionPartiesInfo`, `ReceptionProductBreakdown`, `ReceptionTransportInfo`, `ForkliftUseDialog`, `ForkliftUseList`, `ForkliftUseDetailDialog`, `NoveltiesTable` (si Novedades ya no la usa); y su registro en `F/features/warehouse/components/index.ts`. `LoadingOrderExecutionDialog` y `LoadingOrderList` se quedan (F06): solo nombran a `ReceptionStepCompletion` en comentarios.
- **Lo que solo usaba la recepción directa vieja:** `F/features/weighbridge/components/ServiceRecordDocumentsManager.vue`, `F/features/weighbridge/types/documents.ts` y `F/features/entries/components/DriverPicker.vue` (hoy los importa solo `ReceptionStepManualInfo.vue`); `F/features/warehouse/utils/manual-reception.ts`.
- **Composables, servicios, tipos y utilidades sin uso:** entre ellos `usePendingFromWeighbridge`, `usePendingDirectReception`, `useReceptions`, `useReceptionById`, `useReceptionDetail`, `useReceptionCreate` (con `useRegisterReceptionArrival` y `useCompleteReception`), `useReceptionStatistics`, `useSearchByPlate`, `useActiveForkliftUses`, `useActiveForkliftStatistics`, `useChangeForkliftUsePaymentMode`, `useForkliftUses`, `useForkliftUseById`, `useForkliftMutations`, `useInventoryMovements`, `useInventoryStatistics` (con `useStockAlerts`), `useNovelties`, `utils/pending-weighing.ts`, `utils/forklift-start.ts`, `utils/forklift-history.ts`, los métodos de `F/features/warehouse/services/warehouse-service.ts` que nadie llama y los tipos de `F/features/warehouse/types/` que nadie importa. Lo que importan otros módulos o F06 (órdenes de cargue) se queda.
- **Pruebas** de lo que se borra (las de §5, última fila).
- **Carpetas `mocks/`** de F04 (`F/features/warehouse/mocks/` y `F/features/administration/mocks/` si solo tiene los de F04) y la fachada `catalog.source.ts`. `F/shared/mocks/` se queda.
- **No se borran** `BillingCollectForm` ni `useUnitMeasures` (D46).

### 13.4 Casos QA y docs

- QA2-F04-031 a QA2-F04-050 en PASA, en el navegador, contra el backend local de `f2/f04-bodega` y sin la sesión simulada; QA2-F04-001 a 030 siguen en verde en la suite. Para QA2-F04-043, el trabajo corre con `yarn dev` y el API local, con umbrales de 1 y 2 minutos que se restauran al terminar.
- Copia los casos con su resultado a `D/qa/casos-qa2-f04-bodega-AAAA-MM-DD.md`, con el formato de `D/qa/casos-qa2-f03-bascula-2026-11-24.md`.
- Actualiza este plan (§8), `D/planes/README.md`, la matriz (`D/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md` §2.2), `D/contexto/estado.md` (hito de I-04) y los cambios al hub de §10 (aprobados); y dile al usuario qué puede probar en local (`PM/` §5.3).

### 13.5 Criterio de salida

- Compuertas de `PM/` §6.1 en BE y §6.2 en FE (salvo «sin llamadas reales»), con las cifras antes y después.
- QA2-F04-031 a QA2-F04-050 en PASA.
- Ningún import de `mocks/` de una feature fuera de las pruebas; las carpetas `mocks/` de F04, borradas.
- Menú con las rutas de F04; páginas, componentes y pruebas viejas, borradas; la guardia list-pattern sin F04 en `PENDING`.
- Fusión con `--no-ff` de `f2/f04-bodega` en `fase-2` en los dos repos, y push.

### 13.6 Estado

Pendiente.
