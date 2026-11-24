# Plan cerrado — Fase 2 · F01 Núcleo de dominio

> **Fecha:** 21 de noviembre de 2026. **Estado:** Aprobado por el usuario el 2026-11-21 («Aprobar»). En ejecución desde que se lanzan sus prompts (§11).
> **Origen:**
> - `DEC-080` y el análisis funcional `levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md` (AF-01 a AF-137), con sus wireframes;
> - el plan maestro `planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md` (M1 a M24, `DEC-081`);
> - AF dueñas (42, plan maestro §3.1): AF-08, AF-09, AF-12, AF-14, AF-17, AF-18, AF-20, AF-21, AF-22, AF-26, AF-27, AF-28, AF-29, AF-30, AF-31, AF-32, AF-33, AF-34, AF-35, AF-36, AF-37, AF-39, AF-41, AF-42, AF-43, AF-44, AF-46, AF-47, AF-66, AF-68, AF-70, AF-79, AF-84, AF-85, AF-86, AF-88, AF-90, AF-94, AF-95, AF-101, AF-113, AF-136;
> - las respuestas del usuario a la ronda de preguntas de F01 y F02 (2026-11-21), registradas en D1 a D8.
>
> **Base:** BE `fase-2` `529bda7` · FE `fase-2` `3aa6e3c` · docs `main` `91f0632`. Rama: `f2/f01-nucleo` (BE; en I-01 también FE `f2/f02-base`).
> **Partes:** 0 (contrato, §2) · 1 (backend, seis fases) · 3 (I-01, con F02, §13).
> **Migraciones (4):** `AddCatalogSortAndPrefixes` (fase 1), `RemoveUnitMeasure` (fase 2), `EntryPerDocument` (fase 3) y `ReplaceLoadingOrderWithGoodsExit` (fase 5); las fases 4 y 6 no cambian el esquema (§4).
> **Plan hermano:** `planes/sprint-11/f02-base/plan-cerrado-f2-f02-base-2026-11-21.md` (F02, maquetación). Este plan trae el contrato que F02 maqueta y la integración I-01.
> **Rutas:** relativas a `code_workspace/`. Prefijos: `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`; `A/` = el análisis (`D/levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md`); `PM/` = el plan maestro.

---

## 0. Instrucciones para el ejecutor

1. **Lecturas mínimas:** `D/README.md`, `B/AGENTS.md`, `D/procesos/flujo-de-trabajo-agentes.md`, `D/contexto/convenciones-tecnicas.md`, `PM/` §1, §5 y §6, y este plan completo. Las secciones de `A/` que cita cada decisión, cuando la decisión no baste.
2. **Rama y git** (`PM/` §5.3): `git fetch`; si `develop` avanzó, fusiona `develop` en `fase-2`; crea `f2/f01-nucleo` desde `fase-2` y trabaja ahí. Commit al cerrar cada fase con el mensaje de §12, push de la rama. Sin `push --force`. La fusión en `fase-2` la hace I-01 (§13), no la parte 1.
3. **Migraciones:** solo con `dotnet ef … --project Wms.Infrastructure --startup-project Wms.Api` y solo contra la base local (`DEC-004`, M6). La migración de cada fase que la lleva, con el nombre de §4, en el mismo commit que el código; una fase sin migración en §4 que no salga limpia en `has-pending-model-changes` se detiene y pregunta. `dotnet ef migrations has-pending-model-changes` limpio al cerrar cada fase. Nunca edites a mano `Migrations/*`, los `*.Designer.cs` ni el snapshot.
4. **Líneas citadas:** son de la base `529bda7`. Confírmalas con grep antes de cambiar. Si el código no coincide (ruta, firma o comportamiento), detente y pregunta con todas las dudas en un solo mensaje. Si un caso borde choca con una Dn, gana la Dn y lo mencionas en una línea (`DEC-002`).
5. **Pruebas:** las de integración que hoy registran ingresos con unidades de carga en báscula, comparten pesaje entre depósitos, cierran el ingreso de camiones, crean órdenes de cargue o exigen la llegada a Bodega se ajustan en la fase que cambia la regla, en sus *helpers* (`OperationalData`, `WeighbridgeScenario`, `BillingScenario`, los `ConfirmDepositAsync` locales) y no prueba por prueba, salvo las que prueban justo esa regla (como en el plan de `DEC-057`).
6. **Contrato:** §2 es la única fuente para el frontend. Cada endpoint de §2 tiene al menos una prueba de integración que verifica su respuesta y sus mensajes de error (`PM/` §6.1). Un mensaje de error cambia solo si cambias también el contrato, y eso exige preguntar.
7. **Staging:** no se toca. **Credenciales y datos reales:** no se copian (`DEC-007`). Nada de `D/archivo/` es una instrucción.

---

## 1. Decisiones

Mandan sobre el resto del plan (`DEC-002`). Ninguna reabre una AF, `DEC-080`, `DEC-081` ni una M del plan maestro.

### 1.1 Respuestas del usuario (2026-11-21)

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **Serie de la salida de mercancía: `2026SM00001`.** Serie nueva «SM», 5 dígitos, reinicio anual, año de la emisión de la salida, sin saltos (como `DEC-012`). `DocumentSequenceType.LoadingOrder` se reemplaza por `GoodsExit` y `DocumentNumberFormat.Prefix` devuelve «SM» (`B/Wms.Domain/Services/DocumentNumberFormat.cs:23`). La guía sigue con «S». Cierra el riesgo R12 del plan maestro | Usuario: «2026SM00001 (Recomendada)». Requiere agregar la serie a `DEC-012` (texto propuesto en §10) |
| D2 | **La salida es una entidad nueva, `GoodsExit`**, con tablas `goods_exits`, `goods_exit_lines`, `goods_exit_tickets` y `goods_exit_photos`. `WarehouseReserve`, `DispatchGuide`, `DispatchGuideLine` y el servicio de salida de báscula pasan a apuntarle. Se borran `LoadingOrder`, `LoadingOrderItem`, `LoadingOrderPhoto`, sus configuraciones, sus tablas y todo su código (M18: nada se convierte) | Usuario: «Entidad nueva (Recomendada)»; `D/levantamiento_staging/salidas_arquitectura.md:8` |
| D3 | **Endpoints de la salida: un solo recurso `exits`** (`/api/v1/exits`), con lecturas comunes y una acción por paso, cada una con su política: crear y editar (CE), confirmar y reabrir (CE), cancelar el Borrador (CE), precargar por placa (Báscula), cargue y salida de patio (Bodega). Un DTO y un esquema Zod para F03, F04 y F06 (§2, grupo E) | Usuario: «Un recurso exits (Recomendada)» |
| D4 | **Peso despachado de la consolidada, prorrateado por peso documental.** El neto del pesaje de salida se reparte entre sus depósitos en proporción al peso documental de sus líneas: cantidad que sale × peso de mercancía del producto ÷ cantidad ingresada del producto. Con peso documental total 0, se reparte por cantidad. Redondeo a 2 decimales; la diferencia de redondeo va a la línea de mayor peso | Usuario: «Prorrateo por peso (Recomendada)»; AF-42 |
| D5 | **Un ciclo de báscula por entrada.** Un camión (`EntryLog`) puede tener varios ciclos de almacenamiento, uno por documento; cada ciclo tiene exactamente una `WarehouseStorageEntry`, con su depósito, sus pesajes, su repesaje, su tiquete y su factura. El ciclo que se guarda primero en el camión es el original y cobra; los demás se marcan `IsDuplicateEntry` y cobran $0 (la regla R5 de `B/Wms.Domain/Entities/Weighbridge/WeighbridgeCycle.cs:206-230` pasa del depósito adicional a la entrada duplicada). El índice único servicio+camión (`B/Wms.Infrastructure/Persistence/Configurations/Weighbridge/WeighbridgeCycleConfiguration.cs:48-53`) se conserva: dos entradas del mismo camión no van al mismo depósito | Usuario: «Un ciclo por entrada (Recomendada)»; AF-44, AF-46, AF-47 |
| D6 | **Seis fases** (§8): 1 base y catálogos; 2 unidad de medida fuera, con `PER_UOM`; 3 entradas y pesos; 4 edición del ingreso; 5 salidas, con la cantidad facturable por guía; 6 efectos restantes en facturación (peso de mercancía y tasa de la semana en la factura). Cada fase compila, migra y cierra sola | Usuario: «Seis fases (Recomendada)»; riesgo R1 del plan maestro |
| D7 | **Un depósito con tasa propia la conserva.** Los migrados traen la `trm_ingreso` del legacy como tasa fija (`B/Wms.Application/Administration/LegacyImport/Common/LegacyDepositRowParser.cs:101`; `B/Wms.Domain/Entities/Warehouse/WarehouseStorage.cs:173-175`) y la factura del período la usa. La tasa semanal aplica a los depósitos sin tasa propia, que son todos los nuevos (D38) | Usuario: «Conservan la del legacy (Recomendada)»; `PM/` §7.2 |
| D8 | **Prefijos y tasas en tablas propias:** `field_prefixes` (una fila por campo, sembrada sin valor) y `weekly_exchange_rates` (auditada), cada una con su endpoint y su política (AF-128). Los parámetros del sistema no cambian | Usuario: «Tablas propias (Recomendada)» |

### 1.2 Base, catálogos y permisos (fase 1)

| # | Decisión | Fuente |
| --- | --- | --- |
| D9 | **Orden y filtros por columna en el servidor**, una vez para todos (convención C-F01-00, §2.0): `QueryParametersBase` (`B/Wms.Common/Wrappers/QueryParametersBase.cs:3-33`) gana `SortField` y `SortOrder`; cada consulta declara su lista blanca de columnas y su orden por defecto con un ayudante puro (`ListSorting`, en `B/Wms.Common/Wrappers/`). Un `sortField` fuera de la lista blanca responde 400. Filtros de texto: contiene, sin distinguir mayúsculas ni tildes, con la extensión `unaccent` de PostgreSQL (`EF.Functions.ILike(EF.Functions.Unaccent(col), …)`; si el proveedor no expone `Unaccent`, se mapea la función con `HasDbFunction`). Fechas: `<campo>From` y `<campo>To` (`DateOnly`, día de Colombia). Enums: uno o varios separados por coma | `PM/` §5.1; AF-99, AF-129 |
| D10 | **Qué listas ordenan y filtran en el servidor:** las paginadas (Terceros, Productos, Servicios, Conductores, Vehículos, Motivos de ingreso, Ciudades, Cuadrillas, Parámetros, Tasas de cambio, Usuarios y Auditoría). Las de catálogo corto que se traen completas (Tipos de embalaje, Tipos de unidad de carga, Ubicaciones y Prefijos) no cambian: ordenan y filtran en el navegador | AF-129 («orden en el backend si es paginado») |
| D11 | **Permisos de Configuración** (AF-127, AF-128, `A/` §3.1): política nueva `ConfigurationAccess` = Admin, ForeignTrade, Billing, para escribir en los catálogos de Configuración. Donde un rol operativo ya escribe hoy (altas rápidas), la política del endpoint pasa a la unión, para no quitarle nada (`DEC-005`): `DriverConfigurationAccess` = `DriverCatalogAccess` + Billing; `VehicleConfigurationAccess` = `TransportCatalogAccess` + Billing; `StakeholderConfigurationAccess` = `StakeholderAccess` + Billing (el tercero, sus roles, cuentas y contactos); `PackagingConfigurationAccess` = `OperationalAccess` + ForeignTrade + Billing (solo el alta; editar y borrar, `ConfigurationAccess`). Prefijos: `PrefixAccess` = Admin, ForeignTrade. Tasas: `ExchangeRateAccess` = Admin, ForeignTrade, Billing. Parámetros, Usuarios y Auditoría siguen `AdminOnly`. Las lecturas de catálogo siguen como hoy (`ActiveUser` o autenticado); la de ubicaciones se abre a `ConfigurationAccess` + Warehouse con un controlador propio (`WarehouseLocationsController`, ruta `warehouse/locations`), porque `WarehouseController` exige `WarehouseAccess` en la clase (`B/Wms.Api/Controllers/v1/WarehouseController.cs:59`). La matriz completa está en cada ficha de §2 | `PM/` §5.6; `DEC-005`; `DEC-031`; trampa de los `[Authorize]` que se suman (`D/contexto/convenciones-tecnicas.md` §4) |
| D12 | **Motivos con categoría** (AF-08, M22): `EntryReason.Category` (`EntryReasonCategory?`: `Entry`, `Exit`, `WeighingOnly`), obligatoria si `RequiresWeighing` (400 «Elija la categoría del motivo: Ingreso, Salida o Solo báscula.») y nula si no. La semilla (`B/Wms.Infrastructure/Persistence/SeedDataExtensions.cs:290-308`) asigna: los dos «Descargue» → `Entry`, los dos «Cargue» → `Exit`, «Solo Bascula» → `WeighingOnly`; «Solo bodega» y «Otro», nula. La categoría decide el formulario de Báscula (lo construye F03) | AF-08; M22 |
| D13 | **Báscula corrige los datos de Vigilancia** (AF-08): `PUT entry-logs/{id}/correction` (`B/Wms.Api/Controllers/v1/EntryLogCorrectionController.cs:30`) pasa a `EntryCorrectionAccess` + Scale. Si el camión ya tiene un ciclo guardado, el motivo nuevo debe tener la misma categoría: si no, 409 «El camión {placa} ya tiene un registro de {categoría actual}: para cambiarlo a {categoría nueva}, anule el pesaje y regístrelo de nuevo.» Con un depósito confirmado, Báscula ya no corrige la fecha ni la placa: 409 «El depósito {N} ya está confirmado: la corrección la hace Comercio Exterior.» La fecha conserva los límites de `DEC-012` y `DEC-051` | AF-08, AF-26; `A/` §2.1 f («Quién corrige y hasta cuándo») |
| D14 | **Prefijos** (AF-79, D8): `FieldPrefix` con `Field` (`PrefixedField`: `ReleaseNumber`, `AcceptanceNumber`, `DianManifestNumber`) único y `Prefix` (texto de 0 a 20 letras o dígitos, nulo = sin prefijo). Tres filas sembradas con prefijo nulo; los valores los carga el cliente antes del despliegue final (`PM/` §7.3). El backend no aplica el prefijo: el formulario llega con él y el operario lo completa o lo cambia (F05) | AF-79; D8 |
| D15 | **Tasas semanales** (AF-85, AF-86, AF-136, D8): `WeeklyExchangeRate` (`FromDate` y `ToDate` `DateOnly`, `Rate` COP por USD > 0 con 2 decimales, `CreatedById`), `IAuditable`. Reglas: `FromDate ≤ ToDate`, de 1 a 7 días, sin superponerse con otra (409 «Las fechas se cruzan con la tasa del {desde} al {hasta}.»). Se corrige; no se borra. **Consulta de una fecha:** la tasa cuyo rango la contiene; si no hay, la última con `ToDate` anterior a la fecha, marcada `isFallback` (AF-136); si no hay ninguna, nada. **Sin DIAN:** se retiran `IDianTrmService`, `DianTrmService`, `DianTrmOptions`, `GET system/dian-trm/today` y `TrmSource.Dian`; el levante recibe la tasa en la petición (precargada por el formulario con C-F01-13) y la guarda; corregir una tasa no cambia los levantes ya registrados (`A/` §3.5) | AF-85, AF-86, AF-136; `DEC-023` reemplazada |
| D16 | **Conductores con el mismo documento** (AF-18): sale el índice único `idx_driver_id` (`B/Wms.Infrastructure/Persistence/Configurations/Logistics/DriverConfiguration.cs:24`) y queda uno no único. Crear o editar con el mismo tipo y número de otro conductor se permite si el nombre completo normalizado (sin tildes, mayúsculas ni espacios repetidos) es distinto; si es igual, 409 «Ya existe el conductor {nombre} con {tipo} {número}.» `GET weighbridge/drivers/by-document` devuelve la lista de coincidencias, no uno solo (C-F01-20). Los conductores migrados no cambian | AF-18; `DEC-017` reemplazada en ese punto |
| D17 | **Detalle del conductor:** `GET drivers/{id}/recent-entries?take=5` devuelve sus últimos ingresos (fecha, placa, tiquete), para el drawer de P-TR-03 | Wireframe `transversales.html#P-TR-03` |

### 1.3 Unidad de medida (fase 2)

| # | Decisión | Fuente |
| --- | --- | --- |
| D18 | **La unidad de medida sale** (M21, AF-22): se borran `Product.UnitMeasureId`, la entidad y la tabla `unit_measures`, su semilla, sus comandos, consultas, DTO y endpoints (C-F01-73 a C-F01-76), y la unidad de los DTO de productos, del depósito, de la guía, del PDF del depósito y de cualquier impreso o reporte. El embalaje (`Packaging`, `PackagingTypeId`) se queda. El importador del legacy deja de resolver la unidad (`B/Wms.Application/Administration/LegacyImport/Importers/ProductsImporter.cs:89`; `DepositsImporter.cs:199-221`) | M21; AF-22 |
| D19 | **`PER_UOM` por embalaje** (M21): el esquema sembrado pierde el parámetro `uom` (`B/Wms.Infrastructure/Persistence/SeedDataExtensions.cs:424-431`) y su rótulo pasa a «Por cantidad (embalaje)»; `PerUomFormulaCalculator` deja de validarlo (`B/Wms.Application/Billing/Calculators/PerUomFormulaCalculator.cs:37-43`) y cobra tarifa × cantidad. Un `uom` que llegue en un parámetro guardado se ignora. Se cotejan esquema y calculador (trampa 2 de `D/contexto/convenciones-tecnicas.md` §10) | M21; AF-22, AF-117 |

### 1.4 Entradas y pesos (fase 3)

| # | Decisión | Fuente |
| --- | --- | --- |
| D20 | **Entrada por documento** (AF-20, AF-43, AF-44, AF-46, AF-47; D5). `storage/initiate` y `storage/register` aceptan un `entryLogId` que ya tiene ciclos de almacenamiento: crean otro ciclo con su entrada, marcado duplicado. Desaparecen el depósito adicional dentro de un ciclo, el pesaje compartido y los pesajes intermedios entre depósitos (`B/Wms.Application/Weighbridge/Commands/Storage/Initiate/InitiateStorageWeighingHandler.cs:962-968`; `TypeWeight.Intermediate` deja de usarse en almacenamiento). La elección del depósito sigue `DEC-057` D1 (`targetWarehouseStorageId`), también un depósito abierto del mismo número (AF-20). Dos entradas del mismo camión al mismo depósito: 409 «El camión {placa} ya tiene una entrada en el depósito {N}.» La primera cobra; las duplicadas pasan por el cobro en $0 con su tiquete (AF-47). Si se anula la entrada que cobró, las demás siguen en $0: se anulan y se repiten, y Facturación ajusta (`DEC-013`: un error de facturación no bloquea báscula) | AF-20, AF-43, AF-44, AF-46, AF-47; D5 |
| D21 | **Pesos como el legacy** (AF-09, AF-39, AF-41): la entrada guarda `MerchandiseWeight` (kg, opcional) y su origen `MerchandiseWeightSource` (`Declared`, `Reweigh`, `Correction`). Báscula la envía al registrar (el formulario la precarga con el manifiesto). Tara = indicador − mercancía, calculada, mientras no haya repesaje; con repesaje, mercancía = indicador − tara real y origen `Reweigh`. Una corrección posterior (Báscula hasta confirmar, CE siempre) la reemplaza con origen `Correction`. La mercancía no supera el indicador (400 «El peso de la mercancía no puede ser mayor que el peso del indicador.»). El peso de mercancía del depósito es la suma de sus entradas no anuladas; lo usan el levante (F05) y las fórmulas por peso (D40). `ManifestDeducedWeights` y `WeighingTotals` se adaptan a este campo | AF-09, AF-39, AF-41; `DEC-057` H3 precisada |
| D22 | **Manifiesto solo con carta porte** (AF-12): número y peso del manifiesto obligatorios solo si el tipo de documento es `CARTA-PORTE` (`B/Wms.Infrastructure/Persistence/SeedDataExtensions.cs:328`); con otro tipo no se piden, y si vienen se guardan. La confirmación exige el manifiesto solo en los camiones con carta porte (`B/Wms.Application/ForeignTrade/Common/Services/DepositConfirmationRequirements.cs:66-128`). El manifiesto DIAN de la importación sigue exigido (`DEC-057`) | AF-12; `DEC-057` H2 reemplazada |
| D23 | **Inspección flexible** (AF-17): en inspección, tipo y número de documento y productos son opcionales y `inspectionDescription` (10 a 500 caracteres) es obligatoria; se guarda en `WarehouseStorage.InspectionDescription`. Sin documento, cada camión crea su propio depósito; con documento, se asocia como en D20. La recepción directa de Bodega aplica las mismas reglas (la construye F04, AF-69) | AF-17 |
| D24 | **Sin tipo de vehículo en Báscula** (AF-21): `storage/initiate`, `storage/register` y `output/initiate` dejan de exigirlo; `Vehicle.VehicleType` (ya existe, opcional) lo guarda. La recepción lo registra (F04, AF-62) y el montacargas lo precarga (F04, AF-63) | AF-21; `DEC-057` (nota H1) reemplazada |
| D25 | **Sin bloqueos de Bodega** (AF-14, AF-31): se borran `ReceptionArrivalRules` (`B/Wms.Application/Weighbridge/Common/Services/ReceptionArrivalRules.cs:12-19`) y `ExitLoadingRules` (`ExitLoadingRules.cs:25-40`) con sus llamadas y pruebas. El atraso lo vigilan las alertas de F04 | AF-14, AF-31; CHG-36 y `DEC-019` (R-EXP) reemplazados |
| D26 | **Transportadora por entrada** (AF-101): `WarehouseStorageEntry.CarrierCompanyId` (tercero `TRANSPORT_COMPANY`, obligatorio en las entradas nuevas), tomado de la sección «Camión» del registro. El depósito deja de guardar transportadora propia: `PUT foreign-trade/warehouse-storages/{id}/stakeholders` ya no acepta `TRANSPORT_COMPANY` (400 «La empresa de transporte va en cada entrada, no en el depósito.»), y las lecturas (detalle, búsqueda, guía) usan las de las entradas no anuladas (`B/Wms.Application/ForeignTrade/Common/Services/GuideCarrierText.cs`, `DepositSearchQueryExtensions.cs:87`) | AF-101 |
| D27 | **Sin cierre del ingreso de camiones** (AF-95) **y camión tardío con aviso** (AF-84): se borran `ServiceRecord.TruckEntriesClosedAt`, `TruckEntriesClosedById` y `CloseTruckEntries` (`B/Wms.Domain/Entities/Services/ServiceRecord.cs:71-74`, `:319-339`), el endpoint C-F01-82, los filtros de cierre de `B/Wms.Application/Weighbridge/Common/Services/StorageDocumentLookup.cs:35` y `:85-91` y los datos de cierre de los candidatos (`:125-126`, `:151-152`). Un camión que entra a un depósito confirmado suma stock como hoy (`DeclaredEntry`), recalcula la factura del período (`DEC-022`) y avisa a Comercio Exterior con «Camión tardío en depósito confirmado» (D45). El servicio de entrada queda abierto mientras el depósito no esté cerrado ni anulado | AF-84, AF-95; `DEC-013` reemplazada en el cierre |
| D28 | **Precio por camión y valor CPI** (AF-94): `WarehouseStorageEntry.MerchandiseValue` (en la moneda del depósito, opcional) y `WarehouseStorage.CargoValueIsManual`. Mientras no sea manual, `CargoValue` (el valor CPI) es la suma de los precios de las entradas no anuladas, o nulo si ninguna lo tiene; cuando CE lo digita en «Datos principales» (`PATCH foreign-trade/warehouse-storages/{id}/draft`, que F05 abre al estado Confirmado), queda manual y deja de recalcularse. El cobro usa el CPI (`DEC-029` §7.1). Báscula deja de enviar valor y moneda (`InitiateStorageWeighingHandler.cs:410`); la moneda la pone CE | AF-94; M19 |

### 1.5 Edición del ingreso (fase 4)

| # | Decisión | Fuente |
| --- | --- | --- |
| D29 | **Dos endpoints, un servicio** (AF-26): `PUT weighbridge/entries/{entryId}` (Báscula) y `PUT foreign-trade/entries/{entryId}` (CE) usan el mismo `EntryCorrectionService`; la lectura es `GET weighbridge/entries/{entryId}` con la política `EntryEditAccess` (Admin, Scale, ForeignTrade). Corrigen: camión y conductor (transportadora, país, conductor), documento (tipo, número y depósito, que repite la elección de `DEC-057` D1), mercancía (productos, cantidades y embalaje) y los cuatro pesos (indicador, tara si hay repesaje, manifiesto y mercancía). La modalidad no viaja: no cambia | AF-26 |
| D30 | **Hasta cuándo:** Báscula, mientras el depósito esté en Borrador (409 «El depósito {N} ya está confirmado: la corrección la hace Comercio Exterior.»); CE, en Borrador, Confirmado o Cerrado; nadie en Anulado (409). Una cantidad no queda por debajo de lo levantado ni de lo despachado en guías vigentes, y un producto con levante o salida no se quita (409 con el producto y la cantidad). Báscula con el ciclo completo pide motivo de 10 a 500 caracteres y avisa con el tipo de hoy de «Modificación de peso» | AF-26; `A/` §3.6 |
| D31 | **Lo que solo corrige CE** (`PUT foreign-trade/entries/{entryId}`): el switch «Unidad de carga» y sus unidades (agregar, quitar, tipo y placa), mientras ningún producto del depósito tenga levante o salida (409 «El depósito {N} ya tiene levantes o salidas: las unidades de carga ya no se cambian.»); el precio por camión (D28); y la fecha del manifiesto. Báscula ya no registra unidades de carga: `cargoUnits` sale de `storage/initiate` | AF-27, AF-94; `A/` §3.6; AF-102 (rótulo del switch, F05) |
| D32 | **Recálculo y auditoría:** cambiar cantidades, unidades de carga, pesos (si el depósito cobra por peso), precio (si cambia el CPI automático) o fecha de ingreso recalcula la factura del período con el mecanismo único (`DEC-022`, `StorageRecalculationTrigger`). Toda corrección queda en `audit_logs` con su motivo (`IAuditContext`). Se retira `PATCH foreign-trade/warehouse-storages/{id}/entries/{entryId}/manifest` (C-F01-91): lo absorbe C-F01-90 | `A/` §3.6; `DEC-022` |

### 1.6 Salidas (fase 5)

| # | Decisión | Fuente |
| --- | --- | --- |
| D33 | **Modelo de `GoodsExit`** (D2): número (D1), `Type` (`EntryTicket`, `Global`, `Deposit`, `Consolidated`), `Status` (`Draft`, `Confirmed`, `Completed`, `Cancelled`), modalidad (la de sus depósitos; mezclar modalidades da 400 «Los depósitos de una salida deben ser de la misma modalidad.»), vehículo, conductor, transportadora, ciudad de destino (catálogo, con copia del nombre) y dirección, orden del cliente (número, emisor, fecha y soporte, opcional), observaciones, origen (`ForeignTrade` o `Weighbridge`), confirmación, cargue (fecha, usuario, cuadrilla, firma, observación y fotos), salida de patio (fecha, usuario y observación), ciclo de pesaje de salida, peso despachado y anulación (fecha, usuario y motivo). **Líneas:** producto del depósito, unidad de carga opcional, cantidad, cantidad cargada y peso asignado (D4). **Tiquetes:** las entradas del depósito en `EntryTicket` (una) y `Global` (varias), de un solo depósito (`A/` §2.3 g, P-CE-11). `Deposit` o `Consolidated` lo fija el sistema por el número de depósitos (AF-32); CE elige entre «tiquete», «global» y «por depósito». **Lo que falta** (calculado): en `Deposit` y `Consolidated`, `Loading` sin cargue y `Weighing` sin pesaje de salida completo; en `EntryTicket` y `Global`, `YardExit` | AF-28, AF-29, AF-32, AF-35; D2 |
| D34 | **Estados** (AF-30, AF-35, AF-36, AF-66, AF-68, AF-90): `Draft → Confirmed` (confirmar); `Confirmed → Draft` (reabrir: anula la guía con motivo, devuelve el stock y reactiva las reservas, mientras no esté completada, también si ya se cargó: el cargue registrado se conserva); `Draft → Cancelled` (cancelar con motivo; 409 si tiene un pesaje de salida sin anular); `Confirmed → Completed` cuando no le falta nada. Completada no se edita ni se reabre (409 «La salida {N} está completada: ya no se modifica.»). Anular el pesaje de una completada la devuelve a Confirmada, con «falta pesaje» | AF-30, AF-35, AF-36, AF-66, AF-68, AF-90; `DEC-052` |
| D35 | **Reserva en Borrador** (M24): cada línea de una salida en Borrador reserva su cantidad (`WarehouseReserve` reapuntada a `GoodsExit` y `GoodsExitLine`). **Disponible** de un producto = stock − reservas activas de otras salidas. En importación la línea tampoco supera lo nacionalizado disponible = Σ levantado − Σ despachado en guías vigentes − reservas activas de otras salidas. Pasarse responde 409 «{producto} del depósito {N}: disponible {d}, pidió {q}.» Confirmar consume la reserva; reabrir la reactiva; cancelar la libera. La salida que crea Báscula nace sin líneas y no reserva | M24; AF-30 |
| D36 | **Confirmar emite la guía y descuenta el stock** (AF-36, AF-68, AF-88; `DEC-056`): en importación y exportación, la guía (`DispatchGuide.GoodsExitId`, que reemplaza a `LoadingOrderId`) se emite con su cobro (`BillingRecipientInput`, un cobro por guía, AF-33), sus líneas congeladas como hoy (WMS-19) y su firmante: `Global` → importador; las demás → conductor (`bodegas-legacy/modulos/mod_salidas/verguia.php:785-795`). El vencimiento sale de los días de tránsito de la ciudad. La guía pierde el sello (AF-70). En inspección no hay guía ni cobro de guía: confirmar solo descuenta. El stock baja con un movimiento `Out` de origen `GoodsExit`; reabrir lo devuelve con un `In` de origen `GoodsExitReversal`. Sin stock, el depósito pasa a Cerrado; al reabrir vuelve a Confirmado | AF-36, AF-68, AF-88; `DEC-056` |
| D37 | **Báscula y la salida** (AF-30, AF-33, AF-34, AF-37): `GET exits/by-plate/{placa}` devuelve las salidas `Deposit` o `Consolidated` en Borrador o Confirmadas sin pesaje de la placa. `output/initiate` recibe `exitId`; sin él crea una salida en Borrador con placa (la del camión), conductor y transportadora, sin modalidad ni líneas. Una salida, un ciclo de salida. Una salida `EntryTicket` o `Global` no se pesa (400 «La salida {N} es por tiquete o global: no pasa por báscula.»). Báscula cobra en `Deposit` y `Consolidated`, como hoy. Si Báscula cambia el conductor o la placa: en Borrador pasa a la salida; con guía emitida, la salida no cambia y se avisa a CE con «Cambio de conductor o placa en salida con guía» (D45). Se retiran el pesaje compartido entre órdenes, la salida con el tiquete de ingreso (`ServiceRecord.AnchorWeighbridgeCycleId`, `SourceEntryCycleId`) y sus endpoints (§2.1, grupo E) | AF-29, AF-30, AF-33, AF-34, AF-37 |
| D38 | **Cargue y salida de patio** (AF-66, AF-70; `DEC-052`, `DEC-056`): `POST exits/{id}/loading` solo en `Deposit` y `Consolidated` confirmadas (con guía vigente, salvo inspección): cantidad cargada por línea, de 0 a la cantidad de la guía (400 si la supera), cuadrilla, firma del conductor, observación de hasta 250 caracteres y fotos. Libera las ubicaciones de lo cargado con `PlacementPlanner.PlanLifoRelease` (de la más reciente a la más antigua, `B/Wms.Application/Warehouse/Common/Services/PlacementPlanner.cs:36-55`), sin pedirlas; no pide sello. Si lo cargado difiere de la guía, avisa a CE para reabrir y reemitir (`DEC-052`). Confirmar no toca las ubicaciones. `POST exits/{id}/yard-exit` solo en `EntryTicket` y `Global` confirmadas: fecha y hora del servidor y observación opcional; libera el exceso ubicado con `TrimToStockAsync`. Las dos completan la salida si no le falta nada más | AF-66, AF-67, AF-70; `DEC-052`, `DEC-056` |
| D39 | **Peso despachado** (AF-42, D4): al completarse el pesaje de salida, `DispatchedWeight` = neto del ciclo (bruto − tara, en valor absoluto) y cada línea recibe su peso asignado (D4). El depósito expone `dispatchedWeight` (suma de los pesos asignados de sus líneas en salidas con pesaje) y `weightBalance` = peso de mercancía − despachado | AF-42; D4 |
| D40 | **Cantidad facturable por guía** (M15; `DEC-028` precisada por `DEC-081`): `StorageBillableQuantity` (`B/Wms.Application/Billing/Common/Services/StorageBillableQuantity.cs:93-96`) suma los `Out` de origen `GoodsExit` y resta los `In` de origen `GoodsExitReversal`. `SourceTypeMovements.LoadingOrder` y `LoadingOrderReversal` se reemplazan por esos dos (las bases se recrean; el importador solo produce `MigrationOpening`). Las salidas de inspección cuentan al confirmar, que es cuando bajan el stock | M15; `DEC-028`, `DEC-053` BR-06-005, `DEC-055` |

### 1.7 Facturación y transversales (fases 5 y 6)

| # | Decisión | Fuente |
| --- | --- | --- |
| D41 | **Peso de mercancía en las fórmulas por peso** (AF-113): `WeightThresholdFormulaCalculator` (`B/Wms.Application/Billing/Calculators/WeightThresholdFormulaCalculator.cs:29`) y cualquier fórmula que lea peso usan la suma del peso de mercancía de las entradas no anuladas del depósito (D21), haya o no manifiesto. Una entrada sin peso de mercancía cuenta 0 y la factura lleva la advertencia «{n} camiones sin peso de mercancía» (`DEC-020`). El campo del contexto se renombra `MerchandiseWeightKg` | AF-113; `DEC-020` |
| D42 | **Tasa de la semana en la factura** (AF-85, AF-136; D7, D15): `TrmSource` queda con `Weekly`, `WeeklyFallback` y `Manual`. Al facturar un período, un depósito con tasa `Manual` (los migrados) la conserva; uno sin tasa propia toma la de la semana de su fecha de ingreso (`Weekly`) o, si esa semana no tiene, la última anterior (`WeeklyFallback`), con la advertencia «Se usó la tasa del {desde} al {hasta}: la semana de ingreso no tiene tasa.» y el aviso «Semana sin tasa registrada» a CE y Facturación (D45). Sin ninguna tasa registrada, queda pendiente como hoy (`InvoiceTrmGuard`). Registrar o corregir una tasa reasigna la tasa de los depósitos `Weekly` o `WeeklyFallback` cuya fecha de ingreso cae en su rango (o que usaban una anterior como respaldo) y recalcula sus facturas en Borrador (`A/` §3.5) | AF-85, AF-136; D7 |
| D43 | **Se retiran la TRM de la DIAN y la manual por depósito:** `PUT billing/warehouse-storages/{id}/trm` (`B/Wms.Api/Controllers/v1/BillingController.cs:660-687`, C-F01-140), `RegisterManualTrmCommand`, `WarehouseStorage.AssignDianTrm` y `AssignManualTrm`. El levante guarda `ExchangeRateSource` = `Weekly` si la tasa enviada es la de su semana y `Manual` si no | AF-85; `DEC-023` reemplazada |
| D44 | **Importador del legacy** (`PM/` §5.3, fila `LegacyImport`): cada fase adapta lo que cambia — fase 2, productos y depósitos sin unidad (D18); fase 3, depósitos con `CargoValueIsManual = true` y valor CPI = el del legacy, sin precio por camión (M19), y sin transportadora propia (D26); fase 6, la tasa del legacy con origen `Manual` (D7). Las semillas de motivos (D12) y de prefijos (D14) van en la migración de la fase 1. Ver §7 | `PM/` §7.2; M19, M21, M22 |
| D45 | **Avisos nuevos con roles fijos** (`PM/` §2.2, fila de notificaciones; F09 los pasa a tipos): «Camión tardío en depósito confirmado» (ForeignTrade, D27); «Cambio de conductor o placa en salida con guía» (ForeignTrade, D37); «Semana sin tasa registrada» (ForeignTrade y Billing, D42); «Lo cargado difiere de la guía» (ForeignTrade, D38, adapta el aviso de hoy de `DEC-052`). Todos por `NotificationOrchestrator`, con correo según P0 (`DEC-070`) | `PM/` §2.2; AF-84, AF-34, AF-136; `DEC-052`, `DEC-070` |
| D46 | **Guía pública (QR)** (`DEC-060`): `GET public/dispatch-guides/verify/{token}` (C-F01-139) lee la guía desde la salida; su respuesta no cambia de forma | `DEC-060` |
| D47 | **Cobro de la guía:** `exits/{id}/confirm` recibe el `BillingRecipientInput` de hoy (`B/Wms.Application/Billing/Common/DTOs/BillingRecipientInput.cs`), con `multiClient` incluido. Quitar «Clientes» del cobro de la guía es de F06 (AF-106); el campo `notes` se sigue aceptando aunque el formulario compartido ya no lo envía (AF-132, F02) | AF-33; AF-106 y AF-132 (otras features) |

### 1.8 Destino de las 42 AF dueñas

| AF | Decisión | Fase | AF | Decisión | Fase |
| --- | --- | --- | --- | --- | --- |
| AF-08 | D12, D13 | 1 | AF-36 | D34, D36 | 5 |
| AF-09 | D21 | 3 | AF-37 | D37 | 5 |
| AF-12 | D22 | 3 | AF-39 | D21 | 3 |
| AF-14 | D25 | 3 | AF-41 | D21, D29 | 3 y 4 |
| AF-17 | D23 | 3 | AF-42 | D4, D39 | 5 |
| AF-18 | D16 | 1 | AF-43 | D20 | 3 |
| AF-20 | D20 | 3 | AF-44 | D5, D20 | 3 |
| AF-21 | D24 | 3 | AF-46 | D5, D20 | 3 |
| AF-22 | D18, D19 | 2 | AF-47 | D5, D20 | 3 |
| AF-26 | D29, D30, D32 | 4 | AF-66 | D34, D38 | 5 |
| AF-27 | D31 | 4 | AF-68 | D34, D36 | 5 |
| AF-28 | D33 | 5 | AF-70 | D36, D38 | 5 |
| AF-29 | D33, D37 | 5 | AF-79 | D8, D14 | 1 |
| AF-30 | D2, D33, D34, D37 | 5 | AF-84 | D27 | 3 |
| AF-31 | D25, D34 | 3 y 5 | AF-85 | D15, D42, D43 | 1 y 6 |
| AF-32 | D33 | 5 | AF-86 | D15 | 1 |
| AF-33 | D36, D37 | 5 | AF-88 | D36, D40 | 5 |
| AF-34 | D37 | 5 | AF-90 | D34 | 5 |
| AF-35 | D33, D34 | 5 | AF-94 | D28, D31 | 3 y 4 |
| AF-95 | D27 | 3 | AF-101 | D26 | 3 |
| AF-113 | D41 | 6 | AF-136 | D15, D42 | 1 y 6 |

Las 42 tienen decisión y fase. Lo que su regla deja para una pantalla lo construye otra feature, que la cita sin volver a contarla (`PM/` §2, «Regla de pertenencia»): la cola y el formulario de Báscula (F03), la recepción y las órdenes de salida (F04 y F06), el detalle por etapas y los levantes (F05), los acuerdos (F07).

---

## 2. Contrato (parte 0)

Es la única fuente del frontend para lo que F01 cambia (`PM/` R3). F02 lo maqueta con datos simulados (M12) y las features F03 a F08 lo citan en sus planes sin volver a escribirlo: cada una agrega solo los endpoints propios de sus pantallas.

### 2.0 Convenciones

Rige `D/planes/paridad-legacy/contrato-api-paridad.md` §0 (líneas 11-77): base `/api/v1` (las rutas de este contrato son relativas a ella), JWT, JSON en camelCase, enums como texto (`"Draft"`), fechas ISO 8601 con zona y `DateOnly` como `yyyy-MM-dd` en día de Colombia, respuesta `{ data, pagination }`, `pageSize` de 1 a 50 con `all=true` para todo, errores *ProblemDetails* con `description` y `errors[]`, motivos de 10 a 500 caracteres (recortados) y políticas por rol. Regla del frontend: mostrar `errors[].description` si la lista no está vacía; si no, `description`.

**C-F01-00 · Orden y filtros por columna en el servidor** (convención, D9 y D10; fase 1). Aplica a cada listado marcado «orden y filtros (C-F01-00)» en su ficha.

| Parámetro | Tipo | Regla |
| --- | --- | --- |
| `pageIndex`, `pageSize`, `all` | como hoy | `QueryParametersBase` (`B/Wms.Common/Wrappers/QueryParametersBase.cs:3-33`) |
| `sortField` | string | Nombre camelCase de una columna de la **lista blanca** del endpoint. Fuera de la lista: 400 «No se puede ordenar por «{campo}».» Sin él, rige el orden por defecto de la ficha |
| `sortOrder` | `asc` \| `desc` | Por defecto `asc`. Otro valor: 400 «El orden debe ser asc o desc.» |
| `<campo>` (texto) | string | Contiene, sin distinguir mayúsculas ni tildes (`unaccent` + `ILIKE`). Recortado; vacío = sin filtro |
| `<campo>From`, `<campo>To` | `yyyy-MM-dd` | Rango por día de Colombia, inclusivo. `From > To`: 400 «La fecha inicial no puede ser posterior a la final.» |
| `<campo>` (enum) | string | Uno o varios valores separados por coma, sin distinguir mayúsculas. Un valor desconocido: 400 «El valor «{valor}» no es válido para {campo}.» |
| `isActive` | boolean | Como hoy |

- El desempate de todo orden es `id` ascendente, para que la paginación sea estable.
- Los filtros de una ficha son el mínimo: los de los wireframes y los que el endpoint ya tenía. Los filtros que ya existían conservan su nombre (por ejemplo `search`).
- `B/Wms.Common/Wrappers/ListSorting.cs` (nuevo, puro, probado en `Wms.Tests`) aplica la lista blanca y el orden; cada handler le pasa su diccionario campo → expresión.

**Identificadores.** `C-F01-mm` para cada endpoint y `QA2-F01-nnn` para cada caso QA (`PM/` §5.1).

**Políticas nuevas** (`B/Wms.Domain/Security/WmsPolicyRoles.cs`, D11): `ConfigurationAccess` (Admin, ForeignTrade, Billing); `DriverConfigurationAccess` (Admin, Receiving, Scale, ForeignTrade, Warehouse, Billing); `VehicleConfigurationAccess` (Admin, Receiving, Scale, ForeignTrade, Billing); `StakeholderConfigurationAccess` (Admin, ForeignTrade, Billing); `PackagingCreateAccess` (Admin, Warehouse, Receiving, Scale, ForeignTrade, Billing); `QuickStakeholderAccess` (Admin, Receiving, Scale, Warehouse, ForeignTrade, Billing); `LocationReadAccess` (Admin, Warehouse, ForeignTrade, Billing); `PrefixAccess` (Admin, ForeignTrade); `ExchangeRateAccess` (Admin, ForeignTrade, Billing); `EntryEditAccess` (Admin, Scale, ForeignTrade); `ExitAccess` (Admin, ForeignTrade, Warehouse, Scale) para las lecturas de salidas. Cambia: `EntryCorrectionAccess` pasa a Admin, Receiving, Scale (D13). Ninguna política pierde un rol (`DEC-005`).

### 2.1 Índice

**Grupo B — Configuración, Administración y Vigilancia** (fase 1; los maqueta F02, salvo C-F01-07 y C-F01-20).

| ID | Endpoint | Cambio | Consume |
| --- | --- | --- | --- |
| C-F01-01 | `GET entry-reasons` | modificado: categoría, orden y filtros | F02 (P-TR-04) |
| C-F01-02 | `GET entry-reasons/list` | modificado: categoría | Vigilancia, F03 |
| C-F01-03 | `GET entry-reasons/{id}` | modificado: categoría | F02 |
| C-F01-04 | `POST entry-reasons` | modificado: categoría y política | F02 |
| C-F01-05 | `PATCH entry-reasons/{id}` | modificado: categoría y política | F02 |
| C-F01-06 | `DELETE entry-reasons/{id}` | modificado: política | F02 |
| C-F01-07 | `PUT entry-logs/{id}/correction` | modificado: Báscula y categoría | F03 |
| C-F01-08 | `GET settings/prefixes` | nuevo | F02 (P-TR-05), F05 |
| C-F01-09 | `PUT settings/prefixes/{field}` | nuevo | F02 |
| C-F01-10 | `GET settings/exchange-rates` | nuevo | F02 (P-TR-06) |
| C-F01-11 | `POST settings/exchange-rates` | nuevo | F02 |
| C-F01-12 | `PUT settings/exchange-rates/{id}` | nuevo | F02 |
| C-F01-13 | `GET settings/exchange-rates/for-date` | nuevo | F05 (levantes) |
| C-F01-14 | `GET system/dian-trm/today` | retirado | — |
| C-F01-15 | `GET drivers` | modificado: orden y filtros | F02, F03 |
| C-F01-16 | `GET drivers/{id}` | sin cambios | F02 |
| C-F01-17 | `POST drivers` | modificado: documento repetido y política | F02, F03, F04 |
| C-F01-18 | `PATCH drivers/{id}` | modificado: documento repetido y política | F02, F03 |
| C-F01-19 | `GET drivers/{id}/recent-entries` | nuevo | F02 (P-TR-03) |
| C-F01-20 | `GET weighbridge/drivers/by-document` | modificado: devuelve lista | F03 |
| C-F01-21 | `GET vehicles` | modificado: orden y filtros | F02 |
| C-F01-22 | `GET vehicles/{id}` | sin cambios | F02 |
| C-F01-23 | `POST vehicles` | modificado: política | F02, F03 |
| C-F01-24 | `PATCH vehicles/{id}` | modificado: política | F02, F04 |
| C-F01-25 | `GET stakeholder` | modificado: orden y filtros | F02, todos los selectores |
| C-F01-26 | `GET stakeholder/{id}` | sin cambios | F02 |
| C-F01-27 | `POST stakeholder` | modificado: política | F02 |
| C-F01-28 | `PATCH stakeholder/{id}` | modificado: política | F02 |
| C-F01-29 | `GET administration/packaging-types` | sin cambios | F02 |
| C-F01-30 | `POST administration/packaging-types` | modificado: política | F02 |
| C-F01-31 | `PATCH administration/packaging-types/{id}` | modificado: política | F02 |
| C-F01-32 | `DELETE administration/packaging-types/{id}` | modificado: política | F02 |
| C-F01-33 | `GET administration/cargo-unit-types` | sin cambios | F02 |
| C-F01-34 | `POST administration/cargo-unit-types` | modificado: política | F02 |
| C-F01-35 | `PATCH administration/cargo-unit-types/{id}` | modificado: política | F02 |
| C-F01-36 | `DELETE administration/cargo-unit-types/{id}` | modificado: política | F02 |
| C-F01-37 | `GET service` | modificado: orden y filtros | F02 |
| C-F01-38 | `GET service/{id}` | sin cambios | F02 |
| C-F01-39 | `POST service` | modificado: política | F02 |
| C-F01-40 | `PATCH service/{id}` | modificado: política | F02 |
| C-F01-41 | `POST service/{id}/activate` | modificado: política | F02 |
| C-F01-42 | `POST service/{id}/deactivate` | modificado: política | F02 |
| C-F01-43 | `GET warehouse/locations` | modificado: política | F02, F04 |
| C-F01-44 | `POST warehouse/locations` | modificado: política | F02 |
| C-F01-45 | `PATCH warehouse/locations/{id}` | modificado: política | F02 |
| C-F01-46 | `DELETE warehouse/locations/{id}` | modificado: política | F02 |
| C-F01-47 | `GET administration/cities` | modificado: orden y filtros | F02 |
| C-F01-48 | `POST administration/cities` | modificado: política | F02 |
| C-F01-49 | `PUT administration/cities/{id}` | modificado: política | F02 |
| C-F01-50 | `DELETE administration/cities/{id}` | modificado: política | F02 |
| C-F01-51 | `POST administration/cities/import` | modificado: política | F02 |
| C-F01-52 | `GET administration/crews` | modificado: orden y filtros | F02 |
| C-F01-53 | `POST administration/crews` | modificado: política | F02 |
| C-F01-54 | `PUT administration/crews/{id}` | modificado: política | F02 |
| C-F01-55 | `DELETE administration/crews/{id}` | modificado: política | F02 |
| C-F01-56 | `GET administration/system-parameters` | modificado: orden y filtros | F02 |
| C-F01-57 | `GET administration/system-parameters/{id}` | sin cambios | F02 |
| C-F01-58 | `PATCH administration/system-parameters/{id}` | sin cambios | F02 |
| C-F01-59 | `GET user` | modificado: orden y filtros | F02 |
| C-F01-60 | `GET user/{id}` | sin cambios | F02 |
| C-F01-61 | `POST user` | sin cambios | F02 |
| C-F01-62 | `PATCH user/{id}` | sin cambios | F02 |
| C-F01-63 | `POST user/{id}/assign-roles` | sin cambios | F02 |
| C-F01-64 | `POST user/{id}/remove-roles` | sin cambios | F02 |
| C-F01-65 | `POST user/{id}/reset-password` | sin cambios | F02 |
| C-F01-66 | `POST user/{id}/manage-active` | sin cambios | F02 |
| C-F01-67 | `GET administration/system-roles` | sin cambios | F02 |
| C-F01-68 | `GET administration/audit-logs` | modificado: orden y filtros | F02 |
| C-F01-141 | `POST stakeholder/quick` | nuevo: alta rápida de tercero | F02 (P-TR-09, P-TR-11), F03 a F06 |
| C-F01-163 a C-F01-170 | Roles, cuentas y contactos del tercero (8 endpoints) | modificados: política | Secciones de Terceros que monta I-01 |

**Grupo C — Unidad de medida** (fase 2).

| ID | Endpoint | Cambio | Consume |
| --- | --- | --- | --- |
| C-F01-69 | `GET product` | modificado: sin unidad; orden y filtros | F02, selectores |
| C-F01-70 | `GET product/{id}` | modificado: sin unidad | F02 |
| C-F01-71 | `POST product` | modificado: sin unidad; política | F02, F05 |
| C-F01-72 | `PATCH product/{id}` | modificado: sin unidad; política | F02 |
| C-F01-73 | `GET administration/unit-measures` | retirado | — |
| C-F01-74 | `POST administration/unit-measures` | retirado | — |
| C-F01-75 | `PATCH administration/unit-measures/{id}` | retirado | — |
| C-F01-76 | `DELETE administration/unit-measures/{id}` | retirado | — |
| C-F01-77 | `GET FormulaType` | modificado: `PER_UOM` sin `uom` | F07 |

Las demás lecturas que pierden la unidad están en la tabla R-UOM de §2.2.6.

**Grupo D — Entradas y edición del ingreso** (fases 3 y 4).

| ID | Endpoint | Cambio | Consume |
| --- | --- | --- | --- |
| C-F01-78 | `POST weighbridge/storage/initiate` | modificado: entrada por documento | F03 |
| C-F01-79 | `POST weighbridge/storage/register` | modificado: igual que C-F01-78 | F03 |
| C-F01-80 | `POST weighbridge/cycles/{cycleId}/weighings` | modificado: sin bloqueo de Bodega; mercancía con repesaje | F03 |
| C-F01-81 | `GET weighbridge/storage/document-candidates` | modificado: sin cierre de camiones | F03 |
| C-F01-82 | `POST foreign-trade/warehouse-storages/{id}/close-truck-entries` | retirado | — |
| C-F01-83 | `GET foreign-trade/warehouse-storages/{id}/confirmation-requirements` | modificado: manifiesto solo con carta porte | F05 |
| C-F01-84 | `POST foreign-trade/warehouse-storages/{id}/confirm` | modificado: igual | F05 |
| C-F01-85 | `GET foreign-trade/warehouse-storages/{warehouseStorageId}/entries` | modificado: campos de la entrada | F05 |
| C-F01-86 | `GET foreign-trade/imports/{id}` | modificado: campos del depósito | F05 |
| C-F01-87 | `GET foreign-trade/exports/{id}` | modificado: igual | F05 |
| C-F01-88 | `GET foreign-trade/inspections/{id}` | modificado: igual, más la descripción | F05 |
| C-F01-89 | `PUT foreign-trade/warehouse-storages/{id}/stakeholders` | modificado: sin transportadora | F05 |
| C-F01-90 | `PUT foreign-trade/entries/{entryId}` | nuevo: edición del ingreso por CE | F05 (P-CE-03) |
| C-F01-91 | `PATCH foreign-trade/warehouse-storages/{id}/entries/{entryId}/manifest` | retirado (lo absorbe C-F01-90) | — |
| C-F01-92 | `PUT weighbridge/entries/{entryId}` | nuevo: corrección del ingreso por Báscula | F03 |
| C-F01-93 | `GET weighbridge/entries/{entryId}` | nuevo: la entrada para editar | F03, F05 |

**Grupo E — Salidas** (fase 5).

| ID | Endpoint | Cambio | Consume |
| --- | --- | --- | --- |
| C-F01-94 | `GET exits` | nuevo | F06 (P-CE-11, P-BOD-06, P-BOD-09) |
| C-F01-95 | `GET exits/{id}` | nuevo | F03, F05, F06 |
| C-F01-96 | `POST exits` | nuevo | F06 |
| C-F01-97 | `PUT exits/{id}` | nuevo | F06 |
| C-F01-98 | `POST exits/{id}/confirm` | nuevo | F06 |
| C-F01-99 | `POST exits/{id}/reopen` | nuevo | F06 |
| C-F01-100 | `POST exits/{id}/cancel` | nuevo | F06 |
| C-F01-101 | `GET exits/by-plate/{plate}` | nuevo | F03 (P-BAS-03) |
| C-F01-102 | `GET exits/available-stock` | nuevo | F06 |
| C-F01-103 | `GET exits/entry-tickets` | nuevo | F06 |
| C-F01-104 | `POST exits/{id}/loading` | nuevo | F06 (P-BOD-07) |
| C-F01-105 | `POST exits/{id}/yard-exit` | nuevo | F06 (P-BOD-08) |
| C-F01-106 | `GET exits/{id}/guide/pdf` | nuevo (reemplaza C-F01-122) | F06 |
| C-F01-107 | `GET exits/{id}/guide/pdf/per-deposit` | nuevo (reemplaza C-F01-123) | F06 |
| C-F01-108 | `PATCH exits/{id}/guide/payment-mode` | nuevo (reemplaza C-F01-125) | F06, F08 |
| C-F01-109 | `POST weighbridge/output/initiate` | modificado: salida o Borrador nuevo | F03 |
| C-F01-110 | `POST weighbridge/output/process-payment` | modificado: referencia a la salida | F03 |
| C-F01-111 | `POST weighbridge/output/start-pending-billing` | modificado: igual | F03 |
| C-F01-112 a C-F01-138 | órdenes de cargue y guías por orden (27 endpoints) | retirados | — |
| C-F01-139 | `GET public/dispatch-guides/verify/{token}` | modificado: datos desde la salida | Página pública |

Las lecturas que cambian `loadingOrder*` por la salida están en la tabla R-SAL de §2.2.6.

**Grupo F — Facturación** (fase 6).

| ID | Endpoint | Cambio | Consume |
| --- | --- | --- | --- |
| C-F01-140 | `PUT billing/warehouse-storages/{id}/trm` | retirado (tasa semanal, D43) | — |

Los efectos de la fase 6 (peso de mercancía, tasa de la semana) cambian los valores y advertencias de las facturas, no la forma de sus endpoints.

### 2.2 Fichas

Cada ficha dice: política; qué cambia; petición; respuesta (con el esquema de §2.3); filtros, orden y paginación; errores con su mensaje literal; esquema Zod; notas para el frontend. «Sin cambios» quiere decir que la forma y los mensajes son los de hoy, en el archivo citado; la ficha existe porque F02 lo consume con datos simulados (`PM/` §5.2). Las fichas de los endpoints retirados dicen qué los reemplaza; un retirado responde 404 desde su fase.

#### 2.2.1 Grupo B — Configuración, Administración y Vigilancia (fase 1)

##### C-F01-01 · `GET entry-reasons` (modificado)
- **Política:** `ActiveUser` (sin cambios).
- **Qué cambia:** cada motivo trae `category`; orden y filtros (C-F01-00).
- **Petición (query):** `description` (texto), `category` (enum, varios; el valor `None` filtra los que no tienen), `requiresWeighing` (bool), más paginación.
- **Orden:** lista blanca `description`, `category`, `requiresWeighing`; por defecto `description asc`.
- **Respuesta 200:** `pagedSchema(entryReasonSchema)`.
- **Errores:** los de C-F01-00.
- **Zod:** `entryReasonListQuerySchema`, `entryReasonSchema` (`F/features/entries/contracts/entry-reason.ts`).

##### C-F01-02 · `GET entry-reasons/list` (modificado)
- **Política:** `ActiveUser`. **Qué cambia:** cada motivo trae `category` (lista completa, sin paginar, como hoy).
- **Petición:** —. **Respuesta 200:** `dataSchema(z.array(entryReasonSchema))`. **Errores:** ninguno nuevo.
- **Zod:** `entryReasonSchema`. **Notas:** Vigilancia lo usa para su selector; Báscula decide el formulario por `category` (F03).

##### C-F01-03 · `GET entry-reasons/{id}` (modificado)
- **Petición:** el Id en la ruta.
- **Política:** `ActiveUser`. **Qué cambia:** trae `category`.
- **Respuesta 200:** `dataSchema(entryReasonSchema)`. **Errores:** 404 como hoy (`B/Wms.Application/Logistics/EntryReasons/`).
- **Zod:** `entryReasonSchema`.

##### C-F01-04 · `POST entry-reasons` (modificado)
- **Política:** `ConfigurationAccess` (antes `AdminOnly`).
- **Petición:** `entryReasonCreateSchema` — `description` (string, 3 a 100, obligatorio, único sin tildes ni mayúsculas), `requiresWeighing` (bool, obligatorio), `category` (enum `Entry` \| `Exit` \| `WeighingOnly` \| null; obligatoria si `requiresWeighing`).
- **Respuesta 201:** `dataSchema(entryReasonSchema)`.
- **Errores:** 400 «Elija la categoría del motivo: Ingreso, Salida o Solo báscula.» (con `requiresWeighing` y sin categoría); 400 «Un motivo sin pesaje no lleva categoría.» (sin pesaje y con categoría); 409 «Ya existe el motivo {descripción}.»; los de formato de hoy.
- **Zod:** `entryReasonCreateSchema`, `entryReasonSchema`.

##### C-F01-05 · `PATCH entry-reasons/{id}` (modificado)
- **Política:** `ConfigurationAccess`.
- **Petición:** `entryReasonUpdateSchema` — los campos de C-F01-04, todos opcionales; las reglas se validan sobre el resultado.
- **Respuesta 200:** `dataSchema(entryReasonSchema)`. **Errores:** los de C-F01-04 y 404.
- **Zod:** `entryReasonUpdateSchema`, `entryReasonSchema`.
- **Notas:** cambiar la categoría de un motivo en uso solo afecta los registros nuevos (D12).

##### C-F01-06 · `DELETE entry-reasons/{id}` (modificado)
- **Petición:** el Id en la ruta; sin cuerpo.
- **Política:** `ConfigurationAccess`. **Qué cambia:** solo la política.
- **Respuesta 200:** `dataSchema(z.null())`. **Errores:** los de hoy (en uso, 409; no existe, 404). **Zod:** —.

##### C-F01-07 · `PUT entry-logs/{id}/correction` (modificado)
- **Política:** `EntryCorrectionAccess`, que pasa a Admin, Receiving y Scale (D13).
- **Qué cambia:** Báscula también corrige placa, motivo y fecha; nuevas reglas de categoría y de depósito confirmado.
- **Petición:** la de hoy (`B/Wms.Api/Controllers/v1/EntryLogCorrectionController.cs:56-60`): `licensePlate`, `entryReasonId`, `dateTimeEntry` (opcionales), `reason` (10 a 500).
- **Respuesta 200:** la de hoy, `entryLogCorrectionResultSchema` (`changes[]` con `field`, `previousValue`, `newValue`).
- **Errores nuevos:** 409 «El camión {placa} ya tiene un registro de {categoría actual}: para cambiarlo a {categoría nueva}, anule el pesaje y regístrelo de nuevo.»; 409 «El depósito {N} ya está confirmado: la corrección la hace Comercio Exterior.» (fecha o placa de un camión con depósito confirmado). Siguen los límites de fecha de hoy (`DEC-012`, `DEC-051`).
- **Zod:** `entryLogCorrectionSchema`, `entryLogCorrectionResultSchema` (`F/features/entries/contracts/entry-log-correction.ts`).

##### C-F01-08 · `GET settings/prefixes` (nuevo)
- **Política:** `ActiveUser` (los formularios de CE la leen).
- **Petición:** —. Lista completa, sin paginar (D10).
- **Respuesta 200:**

```jsonc
{ "data": [
  { "field": "ReleaseNumber", "label": "N.º de levante", "prefix": "4820260", "updatedAt": "2026-11-21T09:00:00-05:00", "updatedByName": "Usuario CE 1" },
  { "field": "AcceptanceNumber", "label": "N.º de aceptación", "prefix": null, "updatedAt": null, "updatedByName": null },
  { "field": "DianManifestNumber", "label": "Manifiesto DIAN", "prefix": null, "updatedAt": null, "updatedByName": null }
] }
```

- **Errores:** ninguno. **Zod:** `fieldPrefixSchema` (`F/features/settings/contracts/prefix.ts`).

##### C-F01-09 · `PUT settings/prefixes/{field}` (nuevo)
- **Política:** `PrefixAccess` (Admin, ForeignTrade).
- **Petición:** `{ "prefix": "4820260" }` — string de 1 a 20 letras o dígitos, o `null` para quitarlo. `field` en la ruta: `ReleaseNumber`, `AcceptanceNumber` o `DianManifestNumber`.
- **Respuesta 200:** `dataSchema(fieldPrefixSchema)`.
- **Errores:** 400 «El prefijo admite solo letras y dígitos, hasta 20.»; 404 «El campo {field} no tiene prefijo configurable.»
- **Zod:** `fieldPrefixUpdateSchema`, `fieldPrefixSchema`.

##### C-F01-10 · `GET settings/exchange-rates` (nuevo)
- **Política:** `ActiveUser`.
- **Petición (query):** `fromDateFrom`, `fromDateTo` (rango sobre «Desde»), más paginación.
- **Orden:** lista blanca `fromDate`, `rate`; por defecto `fromDate desc`.
- **Respuesta 200:** `pagedSchema(exchangeRateSchema)`:

```jsonc
{ "id": "guid", "fromDate": "2026-11-16", "toDate": "2026-11-22", "rate": 4050.00,
  "createdByName": "Usuario CE 1", "createdAt": "2026-11-16T08:10:00-05:00",
  "updatedByName": null, "updatedAt": null }
```

- **Errores:** los de C-F01-00. **Zod:** `exchangeRateListQuerySchema`, `exchangeRateSchema` (`F/features/settings/contracts/exchange-rate.ts`).

##### C-F01-11 · `POST settings/exchange-rates` (nuevo)
- **Política:** `ExchangeRateAccess` (Admin, ForeignTrade, Billing).
- **Petición:** `exchangeRateCreateSchema` — `fromDate`, `toDate` (`yyyy-MM-dd`, obligatorias), `rate` (número > 0, hasta 2 decimales, obligatorio).
- **Efecto:** D42 — reasigna la tasa de los depósitos `Weekly`/`WeeklyFallback` cuya fecha de ingreso cae en el rango (o que usaban una anterior como respaldo) y recalcula sus facturas en Borrador. Hasta la fase 6, la tasa solo se guarda.
- **Respuesta 201:** `dataSchema(exchangeRateSchema)`.
- **Errores:** 400 «La fecha final no puede ser anterior a la inicial.»; 400 «Una tasa semanal cubre de 1 a 7 días.»; 400 «La tasa debe ser mayor que cero.»; 409 «Las fechas se cruzan con la tasa del {dd/MM/yyyy} al {dd/MM/yyyy}.»
- **Zod:** `exchangeRateCreateSchema`, `exchangeRateSchema`.

##### C-F01-12 · `PUT settings/exchange-rates/{id}` (nuevo)
- **Política:** `ExchangeRateAccess`.
- **Petición:** `exchangeRateCreateSchema` (las tres, obligatorias). Queda en la auditoría.
- **Efecto:** D42, sobre el rango anterior y el nuevo. Los levantes ya registrados no cambian (D15).
- **Respuesta 200:** `dataSchema(exchangeRateSchema)`. **Errores:** los de C-F01-11 y 404 «La tasa no existe.»
- **Zod:** `exchangeRateCreateSchema`, `exchangeRateSchema`.

##### C-F01-13 · `GET settings/exchange-rates/for-date` (nuevo)
- **Política:** `ActiveUser`.
- **Petición (query):** `date` (`yyyy-MM-dd`, obligatoria).
- **Respuesta 200:** `dataSchema(exchangeRateForDateSchema)`:

```jsonc
{ "data": { "date": "2026-11-18", "rate": 4050.00, "fromDate": "2026-11-16", "toDate": "2026-11-22",
            "isFallback": false, "warning": null } }
// Sin tasa en esa semana: "isFallback": true, "warning": "La semana del 18/11/2026 no tiene tasa: se precarga la del 09/11/2026 al 15/11/2026."
// Sin ninguna tasa registrada: { "data": null }
```

- **Errores:** 400 «Indique la fecha.» **Zod:** `exchangeRateForDateSchema`.
- **Notas:** el levante (F05) precarga `rate` y muestra `warning` (AF-86, AF-136).

##### C-F01-14 · `GET system/dian-trm/today` (retirado)
- **Política de hoy:** autenticado. **Lo reemplaza:** C-F01-13 (D15). **Petición, respuesta, errores y Zod:** no aplica; responde 404 desde la fase 1.

##### C-F01-15 · `GET drivers` (modificado)
- **Petición (query):** los filtros de «Qué cambia», más paginación y orden (C-F01-00).
- **Política:** `ActiveUser`.
- **Qué cambia:** orden y filtros (C-F01-00); se conservan `name`, `idNumber`, `idType`, `isActive`, `search` y `orderByName` (`B/Wms.Application/Logistics/Drivers/Queries/GetAllDrivers/GetAllDriversQuery.cs:10-17`; con `sortField`, `orderByName` se ignora).
- **Orden:** lista blanca `idNumber`, `firstName`, `lastName`, `country`, `isActive`, `createdAt`; por defecto `createdAt desc`.
- **Respuesta 200:** `pagedSchema(driverSchema)`. **Errores:** los de C-F01-00.
- **Zod:** `driverListQuerySchema`, `driverSchema` (`F/features/entries/contracts/driver.ts`).
- **Notas:** el selector muestra nombre y documento, porque el documento ya no es único (D16).

##### C-F01-16 · `GET drivers/{id}` (sin cambios)
- **Petición:** el Id en la ruta.
- **Política:** `ActiveUser`. **Respuesta 200:** `dataSchema(driverSchema)`. **Errores:** 404 como hoy. **Zod:** `driverSchema`.

##### C-F01-17 · `POST drivers` (modificado)
- **Política:** `DriverConfigurationAccess` (antes `DriverCatalogAccess`; suma Billing).
- **Petición:** `driverCreateSchema` — la de hoy (`CreateDriverCommand`: `firstName`, `lastName`, `idNumber`, `idType`, `country`, `phoneNumber`).
- **Qué cambia:** el mismo tipo y número de otro conductor se acepta si el nombre normalizado es distinto (D16).
- **Respuesta 201:** `dataSchema(driverSchema)`.
- **Errores:** 409 «Ya existe el conductor {nombre} con {tipo} {número}.» (reemplaza el 409 de documento repetido); los de formato de hoy.
- **Zod:** `driverCreateSchema`, `driverSchema`.

##### C-F01-18 · `PATCH drivers/{id}` (modificado)
- **Política:** `DriverConfigurationAccess`. **Petición:** `driverUpdateSchema` (la de hoy, `UpdateDriverRequest`, todos opcionales, más `isActive`).
- **Respuesta 200:** `dataSchema(driverSchema)`. **Errores:** los de C-F01-17 y 404. **Zod:** `driverUpdateSchema`, `driverSchema`.

##### C-F01-19 · `GET drivers/{id}/recent-entries` (nuevo)
- **Política:** `ActiveUser`.
- **Petición (query):** `take` (1 a 20, por defecto 5).
- **Respuesta 200:** `dataSchema(z.array(driverRecentEntrySchema))`: `[{ "entryLogId": "guid", "dateTimeEntry": "…", "licensePlate": "ABC123", "ticketNumber": "2026T00045" }]`, del más reciente al más antiguo; `ticketNumber` nulo si el camión no pasó por báscula.
- **Errores:** 404 «El conductor no existe.» **Zod:** `driverRecentEntrySchema`.

##### C-F01-20 · `GET weighbridge/drivers/by-document` (modificado)
- **Política:** la de hoy (`WeighbridgeCatalogController`).
- **Qué cambia:** devuelve la **lista** de conductores con ese tipo y número (D16), activos primero y por nombre; lista vacía si no hay.
- **Petición:** la de hoy (`idType`, `idNumber`). **Respuesta 200:** `dataSchema(z.array(driverSchema))`.
- **Errores:** los de formato de hoy (antes 404 si no había; ahora lista vacía). **Zod:** `driverSchema`. **Notas:** F03 muestra la lista para elegir.

##### C-F01-21 · `GET vehicles` (modificado)
- **Petición (query):** los filtros de «Qué cambia», más paginación y orden (C-F01-00).
- **Política:** `ActiveUser`.
- **Qué cambia:** orden y filtros; se conservan `licensePlate`, `carrierCompanyId`, `isActive`; nuevos `country` (texto) y `vehicleType` (texto).
- **Orden:** lista blanca `licensePlate`, `country`, `vehicleType`, `isActive`, `createdAt`; por defecto `licensePlate asc`.
- **Respuesta 200:** `pagedSchema(vehicleSchema)`; cada vehículo suma `carrierCompanyName` (nulo si no tiene).
- **Errores:** los de C-F01-00. **Zod:** `vehicleListQuerySchema`, `vehicleSchema` (`F/features/entries/contracts/vehicle.ts`).

##### C-F01-22 · `GET vehicles/{id}` (sin cambios, salvo `carrierCompanyName`)
- **Petición:** el Id en la ruta.
- **Política:** `ActiveUser`. **Respuesta 200:** `dataSchema(vehicleSchema)`. **Errores:** 404 como hoy. **Zod:** `vehicleSchema`.

##### C-F01-23 · `POST vehicles` (modificado)
- **Política:** `VehicleConfigurationAccess` (antes `TransportCatalogAccess`; suma Billing).
- **Petición:** `vehicleCreateSchema` (la de hoy: `licensePlate`, `carrierCompanyId`, `country`, `vehicleType`). **Respuesta 201:** `dataSchema(vehicleSchema)`.
- **Errores:** los de hoy (placa repetida 409). **Zod:** `vehicleCreateSchema`, `vehicleSchema`.

##### C-F01-24 · `PATCH vehicles/{id}` (modificado)
- **Política:** `VehicleConfigurationAccess`. **Petición:** `vehicleUpdateSchema` (la de hoy, opcionales, más `isActive`). **Respuesta 200:** `dataSchema(vehicleSchema)`.
- **Errores:** los de hoy y 404. **Zod:** `vehicleUpdateSchema`, `vehicleSchema`. **Notas:** el tipo de vehículo lo guarda Bodega en la recepción (F04, D24).

##### C-F01-25 · `GET stakeholder` (modificado)
- **Petición (query):** los filtros de «Qué cambia», más paginación y orden (C-F01-00).
- **Política:** `ActiveUser`.
- **Qué cambia:** orden y filtros; se conservan `name`, `idNumber`, `businessRolCode`, `financialStatus`, `isActive`, `search` y `exitsBlocked` (`B/Wms.Application/Stakeholders/Queries/GetStakeholders/GetStakeholdersQuery.cs:10-21`).
- **Orden:** lista blanca `name`, `idNumber`, `financialStatus`, `isActive`, `createdAt`; por defecto `name asc`.
- **Respuesta 200:** `pagedSchema(stakeholderSchema)`. **Errores:** los de C-F01-00.
- **Zod:** `stakeholderListQuerySchema`, `stakeholderSchema` (`F/features/stakeholders/contracts/stakeholder.ts`).
- **Notas:** es la fuente del selector de terceros (P-TR-11): `search` + `businessRolCode`, paginado.

##### C-F01-26 · `GET stakeholder/{id}` (sin cambios)
- **Petición:** el Id en la ruta.
- **Política:** `ActiveUser`. **Respuesta 200:** `dataSchema(stakeholderSchema)` (con `businessRoles`). **Errores:** 404 como hoy. **Zod:** `stakeholderSchema`.

##### C-F01-27 · `POST stakeholder` (modificado)
- **Política:** `StakeholderConfigurationAccess` (antes `StakeholderAccess`; suma Billing).
- **Petición:** `stakeholderCreateSchema` — la de hoy (`CreateStakeholderCommand`: `name`, `idType`, `idNumber`, `commercialStatus`, `chamberOfCommerce`, `businessRoles[]` (códigos), `bankAccounts[]`, `contacts[]`, `isUap`). El modal de F02 envía `bankAccounts` y `contacts` nulos: se agregan después desde el detalle.
- **Respuesta 201:** `dataSchema(stakeholderSchema)`. **Errores:** los de hoy (documento repetido 409). **Zod:** `stakeholderCreateSchema`, `stakeholderSchema`.

##### C-F01-28 · `PATCH stakeholder/{id}` (modificado)
- **Política:** `StakeholderConfigurationAccess`. **Petición:** `stakeholderUpdateSchema` (la de hoy, opcionales). **Respuesta 200:** `dataSchema(stakeholderSchema)`.
- **Errores:** los de hoy y 404. **Zod:** `stakeholderUpdateSchema`, `stakeholderSchema`.

##### C-F01-29 · `GET administration/packaging-types` (sin cambios)
- **Política:** autenticado. **Petición:** `isActive` (opcional). Lista completa: orden y filtro en el navegador (D10).
- **Respuesta 200:** `dataSchema(z.array(packagingTypeSchema))`. **Errores:** ninguno. **Zod:** `packagingTypeSchema` (`F/features/administration/contracts/packaging-type.ts`).

##### C-F01-30 · `POST administration/packaging-types` (modificado)
- **Política:** `PackagingCreateAccess` (antes `OperationalAccess`; suma ForeignTrade y Billing). **Petición:** `packagingTypeCreateSchema` (`code`, `name`). **Respuesta 201:** `dataSchema(packagingTypeSchema)`.
- **Errores:** los de hoy (código o nombre repetido 409). **Zod:** `packagingTypeCreateSchema`, `packagingTypeSchema`.

##### C-F01-31 · `PATCH administration/packaging-types/{id}` (modificado)
- **Política:** `ConfigurationAccess` (antes `AdminOnly`). **Petición:** `packagingTypeUpdateSchema` (`code`, `name`, opcionales). **Respuesta 200:** `dataSchema(packagingTypeSchema)`.
- **Errores:** los de hoy y 404. **Zod:** `packagingTypeUpdateSchema`, `packagingTypeSchema`.

##### C-F01-32 · `DELETE administration/packaging-types/{id}` (modificado)
- **Petición:** el Id en la ruta; sin cuerpo.
- **Política:** `ConfigurationAccess`. **Respuesta 200:** `dataSchema(z.null())`. **Errores:** los de hoy (en uso 409, 404). **Zod:** —.

##### C-F01-33 · `GET administration/cargo-unit-types` (sin cambios)
- **Política:** autenticado. **Petición:** `isActive`. Lista completa (D10). **Respuesta 200:** `dataSchema(z.array(cargoUnitTypeSchema))`. **Errores:** ninguno.
- **Zod:** `cargoUnitTypeSchema` (`F/features/administration/contracts/cargo-unit-type.ts`).

##### C-F01-34 · `POST administration/cargo-unit-types` (modificado)
- **Política:** `ConfigurationAccess` (antes `AdminOnly`). **Petición:** `cargoUnitTypeCreateSchema` (`code`, `name`). **Respuesta 201:** `dataSchema(cargoUnitTypeSchema)`.
- **Errores:** los de hoy. **Zod:** `cargoUnitTypeCreateSchema`, `cargoUnitTypeSchema`.

##### C-F01-35 · `PATCH administration/cargo-unit-types/{id}` (modificado)
- **Política:** `ConfigurationAccess`. **Petición:** `cargoUnitTypeUpdateSchema` (`name`, `isActive`, opcionales). **Respuesta 200:** `dataSchema(cargoUnitTypeSchema)`.
- **Errores:** los de hoy y 404. **Zod:** `cargoUnitTypeUpdateSchema`, `cargoUnitTypeSchema`.

##### C-F01-36 · `DELETE administration/cargo-unit-types/{id}` (modificado)
- **Petición:** el Id en la ruta; sin cuerpo.
- **Política:** `ConfigurationAccess`. **Respuesta 200:** `dataSchema(z.null())`. **Errores:** los de hoy. **Zod:** —.

##### C-F01-37 · `GET service` (modificado)
- **Petición (query):** los filtros de «Qué cambia», más paginación y orden (C-F01-00).
- **Política:** autenticado.
- **Qué cambia:** orden y filtros; se conservan `searchTerm`, `code`, `name`, `isActive`.
- **Orden:** lista blanca `code`, `name`, `isActive`, `createdAt`; por defecto `name asc`.
- **Respuesta 200:** `pagedSchema(serviceSchema)`. **Errores:** los de C-F01-00. **Zod:** `serviceListQuerySchema`, `serviceSchema` (`F/features/services/contracts/service.ts`).

##### C-F01-38 · `GET service/{id}` (sin cambios)
- **Petición:** el Id en la ruta.
- **Política:** autenticado. **Respuesta 200:** `dataSchema(serviceSchema)` (con `currentPrice` y `taxes`). **Errores:** 404 como hoy. **Zod:** `serviceSchema`.

##### C-F01-39 · `POST service` (modificado)
- **Política:** `ConfigurationAccess` (antes `BillingAccess`; suma ForeignTrade). Precios, reglas, mínimos e impuestos siguen en `BillingAccess` (Configuración va «sin precios», AF-127).
- **Petición:** `serviceCreateSchema` (`code`, `name`, `description`). **Respuesta 201:** `dataSchema(serviceSchema)`. **Errores:** los de hoy. **Zod:** `serviceCreateSchema`, `serviceSchema`.

##### C-F01-40 · `PATCH service/{id}` (modificado)
- **Política:** `ConfigurationAccess`. **Petición:** `serviceUpdateSchema` (`name`, `description`). **Respuesta 200:** `dataSchema(serviceSchema)`. **Errores:** los de hoy y 404. **Zod:** `serviceUpdateSchema`, `serviceSchema`.

##### C-F01-41 · `POST service/{id}/activate` (modificado)
- **Petición:** el Id en la ruta; sin cuerpo.
- **Política:** `ConfigurationAccess`. **Respuesta 200:** `dataSchema(serviceSchema)`. **Errores:** los de hoy. **Zod:** `serviceSchema`.

##### C-F01-42 · `POST service/{id}/deactivate` (modificado)
- **Petición:** el Id en la ruta; sin cuerpo.
- **Política:** `ConfigurationAccess`. **Respuesta 200:** `dataSchema(serviceSchema)`. **Errores:** los de hoy. **Zod:** `serviceSchema`.

##### C-F01-43 · `GET warehouse/locations` (modificado)
- **Política:** `LocationReadAccess` (Admin, Warehouse, ForeignTrade, Billing; antes `WarehouseAccess` de la clase). Va en `WarehouseLocationsController` con la misma ruta (D11).
- **Petición:** `isAvailable` (opcional). Lista completa (D10). **Respuesta 200:** `dataSchema(z.array(locationSchema))`. **Errores:** ninguno.
- **Zod:** `locationSchema` (`F/features/warehouse/contracts/location.ts`).

##### C-F01-44 · `POST warehouse/locations` (modificado)
- **Política:** `ConfigurationAccess` (antes `AdminOnly`). **Petición:** `locationCreateSchema` (`code`, `name`, `capacity`, `aisle`, `rack`, `level`). **Respuesta 201:** `dataSchema(locationSchema)`.
- **Errores:** los de hoy. **Zod:** `locationCreateSchema`, `locationSchema`. **Notas:** Bodega sigue creando posiciones desde la recepción con el endpoint de hoy de ubicaciones (`WarehousePlacementsController`), sin cambios (`DEC-005`).

##### C-F01-45 · `PATCH warehouse/locations/{id}` (modificado)
- **Política:** `ConfigurationAccess`. **Petición:** `locationUpdateSchema` (`name`, `capacity`, `aisle`, `rack`, `level` como *PatchField*: ausente = no cambia, `null` = borra; `isAvailable`). **Respuesta 200:** `dataSchema(locationSchema)`.
- **Errores:** los de hoy y 404. **Zod:** `locationUpdateSchema`, `locationSchema`.

##### C-F01-46 · `DELETE warehouse/locations/{id}` (modificado)
- **Petición:** el Id en la ruta; sin cuerpo.
- **Política:** `ConfigurationAccess`. **Respuesta 200:** `dataSchema(z.null())`. **Errores:** los de hoy (con mercancía ubicada, 409). **Zod:** —.

##### C-F01-47 · `GET administration/cities` (modificado)
- **Petición (query):** los filtros de «Qué cambia», más paginación y orden (C-F01-00).
- **Política:** autenticado.
- **Qué cambia:** orden y filtros; se conservan `search`, `countryCode`, `isActive`, `isAbandonmentDestination`; nuevo `district` (texto).
- **Orden:** lista blanca `name`, `countryCode`, `district`, `transitDays`, `isActive`; por defecto `name asc`.
- **Respuesta 200:** `pagedSchema(citySchema)`. **Errores:** los de C-F01-00. **Zod:** `cityListQuerySchema`, `citySchema` (`F/features/administration/contracts/city.ts`).

##### C-F01-48 · `POST administration/cities` (modificado)
- **Política:** `ConfigurationAccess` (antes `AdminOnly`). **Petición:** `cityCreateSchema` (`name`, `countryCode`, `district`, `transitDays`, `isAbandonmentDestination`). **Respuesta 201:** `dataSchema(citySchema)`. `countryCode` lleva 3 letras («COL», «ECU»), como `CreateCityValidator` de hoy: el esquema decía 2 y se corrigió con la respuesta del usuario del 2026-11-23 (maquetación de F02, fase 4).
- **Errores:** los de hoy. **Zod:** `cityCreateSchema`, `citySchema`.

##### C-F01-49 · `PUT administration/cities/{id}` (modificado)
- **Política:** `ConfigurationAccess`. **Petición:** `cityUpdateSchema` (los de C-F01-48, más `isActive`). **Respuesta 200:** `dataSchema(citySchema)`. **Errores:** los de hoy y 404. **Zod:** `cityUpdateSchema`, `citySchema`.

##### C-F01-50 · `DELETE administration/cities/{id}` (modificado)
- **Petición:** el Id en la ruta; sin cuerpo.
- **Política:** `ConfigurationAccess`. **Respuesta 200:** `dataSchema(z.null())`. **Errores:** los de hoy. **Zod:** —.

##### C-F01-51 · `POST administration/cities/import` (modificado)
- **Política:** `ConfigurationAccess`. **Petición:** la de hoy (archivo, `multipart/form-data`). **Respuesta 200:** la de hoy, `cityImportResultSchema`. **Errores:** los de hoy. **Zod:** `cityImportResultSchema`.

##### C-F01-52 · `GET administration/crews` (modificado)
- **Petición (query):** los filtros de «Qué cambia», más paginación y orden (C-F01-00).
- **Política:** autenticado. **Qué cambia:** orden y filtros; se conservan `search` e `isActive`.
- **Orden:** lista blanca `name`, `isActive`, `createdAt`; por defecto `name asc`.
- **Respuesta 200:** `pagedSchema(crewSchema)`. **Errores:** los de C-F01-00. **Zod:** `crewListQuerySchema`, `crewSchema` (`F/features/administration/contracts/crew.ts`).

##### C-F01-53 · `POST administration/crews` (modificado)
- **Política:** `ConfigurationAccess` (antes `AdminOnly`). **Petición:** `crewCreateSchema` (`name`). **Respuesta 201:** `dataSchema(crewSchema)`.
- **Errores:** 409 «Ya existe la cuadrilla {nombre}.» (de hoy). **Zod:** `crewCreateSchema`, `crewSchema`.

##### C-F01-54 · `PUT administration/crews/{id}` (modificado)
- **Política:** `ConfigurationAccess`. **Petición:** `crewUpdateSchema` (`name`, `isActive`). **Respuesta 200:** `dataSchema(crewSchema)`. **Errores:** los de hoy y 404. **Zod:** `crewUpdateSchema`, `crewSchema`.

##### C-F01-55 · `DELETE administration/crews/{id}` (modificado)
- **Petición:** el Id en la ruta; sin cuerpo.
- **Política:** `ConfigurationAccess`. **Respuesta 200:** `dataSchema(z.null())`. **Errores:** los de hoy. **Zod:** —.

##### C-F01-56 · `GET administration/system-parameters` (modificado)
- **Petición (query):** los filtros de «Qué cambia», más paginación y orden (C-F01-00).
- **Política:** `AdminOnly` (sin cambios). **Qué cambia:** orden y filtros; se conservan `code`, `dataType`, `isActive`; nuevo `description` (texto).
- **Orden:** lista blanca `code`, `dataType`, `isActive`, `updatedAt`; por defecto `code asc`.
- **Respuesta 200:** `pagedSchema(systemParameterSchema)`. **Errores:** los de C-F01-00. **Zod:** `systemParameterListQuerySchema`, `systemParameterSchema` (`F/features/administration/contracts/system-parameter.ts`).

##### C-F01-57 · `GET administration/system-parameters/{id}` (sin cambios)
- **Petición:** el Id en la ruta.
- **Política:** `AdminOnly`. **Respuesta 200:** `dataSchema(systemParameterSchema)`. **Errores:** 404 como hoy. **Zod:** `systemParameterSchema`.

##### C-F01-58 · `PATCH administration/system-parameters/{id}` (sin cambios)
- **Política:** `AdminOnly`. **Petición:** `systemParameterUpdateSchema` (`value`, `description` como *PatchField*, `dataType`, `isActive`). **Respuesta 200:** `dataSchema(systemParameterSchema)`.
- **Errores:** los de hoy. **Zod:** `systemParameterUpdateSchema`, `systemParameterSchema`.

##### C-F01-59 · `GET user` (modificado)
- **Petición (query):** los filtros de «Qué cambia», más paginación y orden (C-F01-00).
- **Política:** `AdminOnly`. **Qué cambia:** orden y filtros; se conservan `name`, `userName`, `email`, `identificationNumber`; nuevos `isActive` y `role` (código de rol).
- **Orden:** lista blanca `name`, `username`, `email`, `isActive`, `createdAt`; por defecto `name asc`.
- **Respuesta 200:** `pagedSchema(userSchema)` (con `roles`). **Errores:** los de C-F01-00. **Zod:** `userListQuerySchema`, `userSchema` (`F/features/users/contracts/user.ts`).

##### C-F01-60 · `GET user/{id}` (sin cambios)
- **Petición:** el Id en la ruta.
- **Política:** `AdminOnly`. **Respuesta 200:** `dataSchema(userSchema)`. **Errores:** 404 como hoy. **Zod:** `userSchema`.

##### C-F01-61 · `POST user` (sin cambios)
- **Política:** `AdminOnly`. **Petición:** `userCreateSchema` (`name`, `username`, `identificationNumber`, `password`, `email`, `phone`). **Respuesta 201:** `dataSchema(userSchema)`.
- **Errores:** los de hoy (`B/Wms.Application/Users/Commands/CreateUser/`). **Zod:** `userCreateSchema`, `userSchema`. **Notas:** la contraseña no se muestra ni se guarda en el navegador.

##### C-F01-62 · `PATCH user/{id}` (sin cambios)
- **Política:** `AdminOnly`. **Petición:** `userUpdateSchema` (los de C-F01-61 sin contraseña, opcionales). **Respuesta 200:** `dataSchema(userSchema)`. **Errores:** los de hoy. **Zod:** `userUpdateSchema`, `userSchema`.

##### C-F01-63 · `POST user/{id}/assign-roles` (sin cambios)
- **Política:** `AdminOnly`. **Petición:** `{ "roleIds": ["guid"] }`. **Respuesta 200:** `dataSchema(userSchema)`. **Errores:** los de hoy. **Zod:** `userRolesChangeSchema`, `userSchema`.

##### C-F01-64 · `POST user/{id}/remove-roles` (sin cambios)
- **Política:** `AdminOnly`. **Petición:** `{ "roleIds": ["guid"] }`. **Respuesta 200:** `dataSchema(userSchema)`. **Errores:** los de hoy. **Zod:** `userRolesChangeSchema`, `userSchema`.

##### C-F01-65 · `POST user/{id}/reset-password` (sin cambios)
- **Política:** `AdminOnly`. **Petición:** `{ "newPassword": "…" }`. **Respuesta 200:** `dataSchema(z.null())`. **Errores:** los de hoy (reglas de contraseña). **Zod:** `userResetPasswordSchema`.

##### C-F01-66 · `POST user/{id}/manage-active` (sin cambios)
- **Política:** `AdminOnly`. **Petición:** `{ "isActive": true, "lockoutEndDate": null }`. **Respuesta 200:** `dataSchema(userSchema)`. **Errores:** los de hoy. **Zod:** `userActivationSchema`, `userSchema`.

##### C-F01-67 · `GET administration/system-roles` (sin cambios)
- **Petición:** —.
- **Política:** autenticado. **Respuesta 200:** `dataSchema(z.array(systemRoleSchema))` (`id`, `code`, `name`). **Errores:** ninguno. **Zod:** `systemRoleSchema` (`F/features/users/contracts/user.ts`).

##### C-F01-68 · `GET administration/audit-logs` (modificado)
- **Petición (query):** los filtros de «Qué cambia», más paginación y orden (C-F01-00).
- **Política:** `AdminOnly`. **Qué cambia:** orden y filtros; se conservan `userName`, `action`, `affectedTable`; `fromDate`/`toDate` (`DateTimeOffset`) pasan a `createdAtFrom`/`createdAtTo` (`yyyy-MM-dd`, C-F01-00); nuevo `registerIdAffected` (texto).
- **Orden:** lista blanca `createdAt`, `userName`, `action`, `affectedTable`; por defecto `createdAt desc`.
- **Respuesta 200:** `pagedSchema(auditLogSchema)`. **Errores:** los de C-F01-00. **Zod:** `auditLogListQuerySchema`, `auditLogSchema` (`F/features/audit/contracts/audit-log.ts`).

##### C-F01-141 · `POST stakeholder/quick` (nuevo)
- **Política:** `QuickStakeholderAccess` (Admin, Receiving, Scale, Warehouse, ForeignTrade, Billing): el «+» de los selectores y del cobro (AF-54, AF-92).
- **Petición:** `stakeholderQuickCreateSchema` — `name` (3 a 200), `idType` (`IdentificationType`), `idNumber` (1 a 30), `roleCode` (`CUSTOMER`, `IMPORTER`, `EXPORTER`, `CUSTOMS_AGENCY` o `TRANSPORT_COMPANY`).
- **Efecto:** como `POST weighbridge/stakeholders/quick` de hoy (`B/Wms.Api/Controllers/v1/WeighbridgeController.cs:1019`): crea el tercero con ese rol, o le agrega el rol si ya existe con ese documento.
- **Respuesta:** 201 creado o 200 rol agregado, `dataSchema(stakeholderQuickResultSchema)` = `{ outcome: "Created" | "RoleAdded", stakeholder }`.
- **Errores:** 409 «El tercero {nombre} ya tiene el rol {rol}.»; los de formato de hoy.
- **Zod:** `stakeholderQuickCreateSchema`, `stakeholderQuickResultSchema`.
- **Notas:** `weighbridge/stakeholders/quick` y `weighbridge/transport-companies/quick` se conservan sin cambios; el plan de F03 decide si sus pantallas pasan a este.

##### C-F01-163 a C-F01-170 · Roles, cuentas y contactos del tercero (modificados: política)

La política de escritura pasa de `StakeholderAccess` (Admin, ForeignTrade) a `StakeholderConfigurationAccess` (Admin, ForeignTrade, Billing), como C-F01-27 y C-F01-28 (AF-127, D11). Petición, respuesta y errores: los de hoy (`B/Wms.Api/Controllers/v1/StakeholderController.cs`). Los consumen los componentes de hoy que I-01 monta en el drawer de Terceros (§13.5); no se simulan en la maquetación, así que su esquema Zod no aplica en F02 (los componentes usan sus tipos de hoy, `F/features/stakeholders/types/`).

| ID | Endpoint |
| --- | --- |
| C-F01-163 | `POST stakeholder/{id}/assign-role` |
| C-F01-164 | `POST stakeholder/{id}/remove-role` |
| C-F01-165 | `POST stakeholder/{id}/bank-account` |
| C-F01-166 | `PATCH stakeholder/{stakeholderId}/bank-account/{bankAccountId}` |
| C-F01-167 | `DELETE stakeholder/{stakeholderId}/bank-account/{bankAccountId}` |
| C-F01-168 | `POST stakeholder/{id}/contact` |
| C-F01-169 | `PATCH stakeholder/{stakeholderId}/contact/{id}` |
| C-F01-170 | `DELETE stakeholder/{stakeholderId}/contact/{bankAccountId}` (el parámetro se llama así hoy; es el Id del contacto) |

#### 2.2.2 Grupo C — Unidad de medida (fase 2)

##### C-F01-69 · `GET product` (modificado)
- **Petición (query):** los filtros de «Qué cambia», más paginación y orden (C-F01-00).
- **Política:** autenticado (sin cambios).
- **Qué cambia:** salen `unitMeasureId`, `unitMeasureCode` y `unitMeasureName` (D18); orden y filtros; se conservan `searchTerm`, `name`, `sku`, `isActive`, `createdFromWeighbridge`; nuevo `packagingTypeId`.
- **Orden:** lista blanca `name`, `sku`, `packagingTypeName`, `isActive`, `createdAt`; por defecto `name asc`.
- **Respuesta 200:** `pagedSchema(productSchema)`. **Errores:** los de C-F01-00.
- **Zod:** `productListQuerySchema`, `productSchema` (`F/features/products/contracts/product.ts`).
- **Notas:** los selectores muestran el embalaje junto al nombre (AF-92, F05): «Cebolla (Sacos)».

##### C-F01-70 · `GET product/{id}` (modificado)
- **Petición:** el Id en la ruta.
- **Política:** autenticado. **Qué cambia:** sin unidad. **Respuesta 200:** `dataSchema(productSchema)`. **Errores:** 404 como hoy. **Zod:** `productSchema`.

##### C-F01-71 · `POST product` (modificado)
- **Política:** `ConfigurationAccess` (antes `AdminOnly`).
- **Petición:** `productCreateSchema` — `name` (obligatorio), `sku` (obligatorio), `description`, `packaging`, `packagingTypeId`. Sale `unitMeasureId`; si llega, se ignora.
- **Respuesta 201:** `dataSchema(productSchema)`. **Errores:** los de hoy (SKU repetido 409) menos los de la unidad. **Zod:** `productCreateSchema`, `productSchema`.

##### C-F01-72 · `PATCH product/{id}` (modificado)
- **Política:** `ConfigurationAccess` (antes `AdminOnly`). **Petición:** `productUpdateSchema` (los de C-F01-71, opcionales, más `isActive`; sin unidad). **Respuesta 200:** `dataSchema(productSchema)`.
- **Errores:** los de hoy y 404. **Zod:** `productUpdateSchema`, `productSchema`.

##### C-F01-73 a C-F01-76 · `administration/unit-measures` (retirados)

| ID | Endpoint | Política de hoy | Lo reemplaza |
| --- | --- | --- | --- |
| C-F01-73 | `GET administration/unit-measures` | autenticado | Nada: la unidad sale de la app (M21) |
| C-F01-74 | `POST administration/unit-measures` | `AdminOnly` | Nada |
| C-F01-75 | `PATCH administration/unit-measures/{id}` | `AdminOnly` | Nada |
| C-F01-76 | `DELETE administration/unit-measures/{id}` | `AdminOnly` | Nada |

Petición, respuesta, errores y Zod: no aplica; responden 404 desde la fase 2. El frontend borra la página y sus servicios en I-01 (plan de F02).

##### C-F01-77 · `GET FormulaType` (modificado)
- **Petición:** la de hoy.
- **Política:** la de hoy. **Qué cambia:** `PER_UOM` llega sin el parámetro `uom` y con el rótulo «Por cantidad (embalaje)» (D19). **Respuesta 200:** la de hoy. **Errores:** ninguno nuevo.
- **Zod:** lo escribe F07 al maquetar las fórmulas (P-FAC-13); este contrato fija solo el cambio.

#### 2.2.3 Grupo D — Entradas (fase 3) y edición del ingreso (fase 4)

##### C-F01-78 · `POST weighbridge/storage/initiate` (modificado)
- **Política:** `ScaleAccess` (sin cambios).
- **Qué cambia:** una entrada por documento (D20), pesos del legacy (D21), manifiesto solo con carta porte (D22), inspección flexible (D23), transportadora por entrada (D26), sin unidades de carga ni valor (D28, D31).
- **Petición** (`InitiateStorageWeighingCommand`, `B/Wms.Application/Weighbridge/Commands/Storage/Initiate/InitiateStorageWeighingCommand.cs`; solo los campos que cambian):

| Campo | Antes | Ahora |
| --- | --- | --- |
| `entryLogId` | un ciclo de almacenamiento por camión | si el camión ya tiene un ciclo de almacenamiento no anulado, la entrada nueva es **duplicada**: ciclo propio, cobro en $0 (D20) |
| `isAdditionalDeposit`, `weighbridgeCycleId` | depósito adicional en el ciclo | **salen**; si llegan, 400 «El depósito adicional ya no existe: use «Duplicar entrada».» |
| `cargoManifestNumber` (número del documento), `primaryDocumentTypeId` | obligatorios | obligatorios en importación y exportación; opcionales en inspección (D23) |
| `products` | obligatoria, al menos uno | obligatoria en importación y exportación; opcional en inspección |
| `inspectionDescription` | — | **nuevo**: string 10 a 500, obligatorio en inspección; se ignora en las demás |
| `manifestNumber`, `manifestWeight` | obligatorios (`DEC-057` H2) | obligatorios solo si el tipo de documento es `CARTA-PORTE`; con otro tipo, opcionales |
| `merchandiseWeight` | — | **nuevo**: decimal > 0, opcional; no supera el indicador cuando este exista (D21) |
| `carrierCompanyId` | opcional, actualiza el vehículo | **obligatorio**: transportadora de la entrada (D26); sigue actualizando la del vehículo |
| `currency`, `cargoValue` | los ponía Báscula | **salen**; se ignoran (D28) |
| `cargoHandling`, `cargoUnits` | Báscula registraba las unidades | **salen**; el depósito nace con mercancía suelta y CE cambia el switch (D31) |
| `targetWarehouseStorageId` | `DEC-057` D1 | igual; sin documento (inspección) se ignora y se crea un depósito nuevo |

- **Respuesta 201** (`InitiateStorageResponseDto`, campos que cambian):

```jsonc
{
  "weighbridgeCycleId": null,              // el ciclo de ESTA entrada: nulo al registrar, nace en el cobro (nota de la fase 3, §8)
  "warehouseStorageEntryId": "guid",       // nuevo
  "isDuplicateEntry": false,               // nuevo: true en las duplicadas
  "warehouseStorageNumber": "2026BA00012",
  "isLateTruck": false                     // nuevo: true si el depósito ya estaba confirmado (D27)
  // …resto sin cambios; salen isAdditionalDeposit y newWarehouseStorageEntryId (D20)
}
```

- **Errores nuevos o cambiados:**

| Status | Mensaje |
| --- | --- |
| 400 | «El número y el peso del manifiesto son obligatorios con carta porte.» |
| 400 | «Describa la inspección (de 10 a 500 caracteres).» |
| 400 | «Indique el tipo y el número del documento.» (importación y exportación) |
| 400 | «Declare al menos un producto.» (importación y exportación) |
| 400 | «El peso de la mercancía debe ser mayor que cero.» |
| 400 | «Elija la empresa de transporte del camión.» |
| 400 | «El depósito adicional ya no existe: use «Duplicar entrada».» |
| 409 | «El camión {placa} ya tiene una entrada en el depósito {N}.» |

  Sale el 409 de ingreso de camiones cerrado (D27).
- **Zod:** `storageEntryInitiateChangesSchema`, `storageEntryInitiateResultChangesSchema` (`F/features/weighbridge/contracts/storage-entry.ts`): el cambio; F03 los une a la petición y la respuesta de hoy al maquetar.
- **Notas:** «Duplicar entrada» (AF-49, F03) es del formulario: copia las secciones 1 y 2 y, al guardar, llama a este endpoint con el mismo `entryLogId`.

##### C-F01-79 · `POST weighbridge/storage/register` (modificado)
- **Política:** `ScaleAccess`. **Qué cambia:** lo mismo que C-F01-78 (mismo comando, más los datos del conductor y del vehículo de hoy). El tipo de vehículo deja de ser obligatorio (D24).
- **Respuesta 201:** la de C-F01-78 más `entryLogUpdated` (de hoy). **Errores:** los de C-F01-78. **Zod:** `storageEntryInitiateChangesSchema` (sobre la petición de hoy de `register`), `storageEntryInitiateResultChangesSchema`; F03 los completa.

##### C-F01-80 · `POST weighbridge/cycles/{cycleId}/weighings` (modificado)
- **Política:** la de hoy. **Petición:** la de hoy (`weight`, `weightType`, `observations`, `capturedAt`).
- **Qué cambia:** sin el 409 de llegada a Bodega ni el de cargue pendiente (D25). En un ciclo de almacenamiento, el pesaje de tara (repesaje) fija la mercancía de su entrada = indicador − tara (D21). `Intermediate` ya no se acepta en almacenamiento: 400 «El pesaje intermedio ya no existe: cada documento tiene su entrada.»
- **Respuesta 200:** la de hoy (`RecordWeighingResponseDto`) más `merchandiseWeight` (decimal \| null).
- **Errores:** salen «El camión {placa} no tiene registrada su llegada a Bodega…» (`ReceptionArrivalRules.cs:17-19`) y «No se puede cerrar el pesaje de salida: la orden…» (`ExitLoadingRules.cs:34-39`). **Zod:** `weighingRecordResultChangesSchema` (`F/features/weighbridge/contracts/weighing.ts`); la petición no cambia y F03 completa la respuesta.

##### C-F01-81 · `GET weighbridge/storage/document-candidates` (modificado)
- **Política:** la de hoy. **Petición:** la de hoy (`number`, `primaryDocumentTypeId`).
- **Qué cambia:** salen `closedAt` y `closedByName`; `isOpen` = estado Borrador o Confirmado (sin cierre de camiones, D27); se conserva `isMigrated`.
- **Respuesta 200:** la lista de hoy (`StorageDocumentCandidateDto`) con el cambio. **Errores:** los de hoy. **Zod:** `documentCandidateChangesSchema` (`F/features/weighbridge/contracts/storage-entry.ts`); F03 lo une al candidato de hoy.

##### C-F01-82 · `POST foreign-trade/warehouse-storages/{id}/close-truck-entries` (retirado)
- **Política de hoy:** `ForeignTradeAccess`. **Lo reemplaza:** nada; el camión tardío entra con aviso (D27, AF-95). Petición, respuesta, errores y Zod: no aplica; 404 desde la fase 3.

##### C-F01-83 · `GET foreign-trade/warehouse-storages/{id}/confirmation-requirements` (modificado)
- **Petición:** la de hoy (Id del depósito en la ruta).
- **Política:** la de hoy. **Qué cambia:** el requisito de manifiesto (número y peso) solo aparece para los camiones con carta porte (D22). El del cliente sigue hasta F05 (AF-75).
- **Respuesta 200:** la de hoy. **Errores:** los de hoy. **Zod:** lo escribe F05 con la respuesta de hoy (`F/features/foreign-trade/contracts/deposit.ts`); este contrato fija solo el cambio de la regla.

##### C-F01-84 · `POST foreign-trade/warehouse-storages/{id}/confirm` (modificado)
- **Petición:** la de hoy (Id del depósito en la ruta).
- **Política:** la de hoy. **Qué cambia:** igual que C-F01-83. **Respuesta y errores:** los de hoy; el 400 de requisitos ya no lista el manifiesto de los camiones sin carta porte. **Zod:** lo escribe F05 con la respuesta de hoy; el cambio es de la regla.

##### C-F01-85 · `GET foreign-trade/warehouse-storages/{warehouseStorageId}/entries` (modificado)
- **Política:** la de hoy. **Petición:** la de hoy (Id del depósito en la ruta). **Respuesta 200:** `dataSchema(z.array(depositEntrySchema))`. **Qué cambia:** cada entrada (`DepositStorageEntryDto`) suma:

```jsonc
{
  "weighbridgeCycleId": "guid",
  "isDuplicateEntry": false,
  "carrierCompanyId": "guid", "carrierCompanyName": "Transportes Ejemplo",
  "documentTypeName": "Carta porte", "documentNumber": "CP-001",
  "indicatorWeight": 30000, "tareWeight": 12000, "tareIsReal": false,
  "merchandiseWeight": 18000, "merchandiseWeightSource": "Declared",
  "manifestDifference": 0,               // mercancía − manifiesto (AF-41)
  "merchandiseValue": 15000.00,          // precio de este camión (D28)
  "manifestDate": null
  // …campos de hoy, sin unidad de medida en los productos
}
```

- **Errores:** los de hoy. **Zod:** `depositEntrySchema` (`F/features/foreign-trade/contracts/deposit-entry.ts`). Lo maqueta F05.

##### C-F01-86 · `GET foreign-trade/imports/{id}` (modificado)
- **Política:** la de hoy. **Qué cambia** en el detalle del depósito: `cargoValue` es el valor CPI y se suma `cargoValueIsManual` y `truckValueSum` (D28); `carriers[]` (nombres, de las entradas no anuladas) reemplaza a la transportadora del depósito (D26); `merchandiseWeight`, `dispatchedWeight` y `weightBalance` (D21, D39); salen `truckEntriesClosedAt` y `truckEntriesClosedByName` (D27); salen los campos de unidad de medida (D18); `trmSource` admite `Weekly`, `WeeklyFallback` y `Manual` (D42).
- **Petición:** la de hoy (Id en la ruta). **Respuesta 200:** el detalle de hoy con los cambios de arriba.
- **Errores:** los de hoy. **Zod:** `depositDetailChangesSchema` (`F/features/foreign-trade/contracts/deposit.ts`); F05 lo une al detalle de hoy.

##### C-F01-87 · `GET foreign-trade/exports/{id}` (modificado)
- Igual que C-F01-86 para exportación. **Política:** la de hoy. **Petición:** la de hoy. **Respuesta 200:** el detalle de hoy con los cambios de C-F01-86. **Errores:** los de hoy. **Zod:** `depositDetailChangesSchema`.

##### C-F01-88 · `GET foreign-trade/inspections/{id}` (modificado)
- Igual que C-F01-86, más `inspectionDescription` (D23); el número de documento puede venir nulo. **Política:** la de hoy. **Petición:** la de hoy. **Respuesta 200:** el detalle de hoy con los cambios. **Errores:** los de hoy. **Zod:** `depositDetailChangesSchema`.

##### C-F01-89 · `PUT foreign-trade/warehouse-storages/{id}/stakeholders` (modificado)
- **Política:** la de hoy. **Petición:** la de hoy. **Qué cambia:** el rol `TRANSPORT_COMPANY` ya no se acepta (D26).
- **Respuesta:** la de hoy. **Errores:** 400 «La empresa de transporte va en cada entrada, no en el depósito.» **Zod:** lo escribe F05 con la petición de hoy (`F/features/foreign-trade/contracts/deposit.ts`); el cambio es la regla del rol.

##### C-F01-90 · `PUT foreign-trade/entries/{entryId}` (nuevo)
- **Política:** `ForeignTradeAccess`.
- **Qué hace:** CE corrige la entrada en Borrador, Confirmado o Cerrado (D29 a D32).
- **Petición:** `entryCorrectionCeSchema`:

| Campo | Tipo | Obligatorio | Regla |
| --- | --- | --- | --- |
| `vehicleCountry` | string | No | Como el registro |
| `carrierCompanyId` | guid | Sí | Tercero con rol `TRANSPORT_COMPANY` (D26) |
| `driverId` | guid | Sí | Conductor activo |
| `primaryDocumentTypeId`, `documentNumber` | guid, string | En importación y exportación | Cambiar el documento exige `targetWarehouseStorageId` (`DEC-057` D1) |
| `targetWarehouseStorageId` | guid \| null | Si cambia el documento | Nulo = depósito nuevo; con valor, las validaciones de `DEC-057` D1 |
| `manifestNumber`, `manifestWeight` | string, decimal | Con carta porte | D22 |
| `manifestDate` | `yyyy-MM-dd` \| null | No | No futura |
| `indicatorWeight` | decimal | Si el ciclo tiene pesaje de entrada | > 0; corrige el pesaje con motivo |
| `tareWeight` | decimal \| null | Solo si hay repesaje | > 0, menor que el indicador |
| `merchandiseWeight` | decimal \| null | No | > 0, ≤ indicador; origen `Correction` (D21) |
| `products[]` | `{ warehouseStorageProductId?, productId, declaredQuantity, packaging, packagingTypeId }` | En importación y exportación | Cantidad ≥ lo levantado y lo despachado (D30) |
| `merchandiseValue` | decimal \| null | No | ≥ 0; recalcula el CPI automático (D28) |
| `usesCargoUnits` | bool | Sí | D31 |
| `cargoUnits[]` | `{ id?, cargoUnitTypeId, identifier }` | Si `usesCargoUnits` | D31 |
| `reason` | string | No | 10 a 500 si viene; va a la auditoría |

- **Respuesta 200:** `dataSchema(depositEntrySchema)`.
- **Errores:**

| Status | Mensaje |
| --- | --- |
| 404 | «La entrada no existe.» |
| 409 | «El depósito {N} está anulado: no se corrige.» |
| 409 | «{producto}: la cantidad no puede quedar en {q}; ya tiene {l} levantado y {d} despachado.» |
| 409 | «{producto} ya tiene levantes o salidas: no se puede quitar.» |
| 409 | «El depósito {N} ya tiene levantes o salidas: las unidades de carga ya no se cambian.» |
| 400 | los de C-F01-78 sobre manifiesto, pesos y documento |

- **Zod:** `entryCorrectionCeSchema`, `depositEntrySchema` (`F/features/foreign-trade/contracts/deposit-entry.ts`). Lo maqueta F05 (P-CE-03).
- **Notas:** el rótulo «Unidad de carga» con switch es de F05 (AF-102).

##### C-F01-91 · `PATCH foreign-trade/warehouse-storages/{id}/entries/{entryId}/manifest` (retirado)
- **Política de hoy:** la de `DepositCompletionController`. **Lo reemplaza:** C-F01-90 (D32). Petición, respuesta, errores y Zod: no aplica; 404 desde la fase 4.

##### C-F01-92 · `PUT weighbridge/entries/{entryId}` (nuevo)
- **Política:** `ScaleAccess`.
- **Qué hace:** Báscula corrige la entrada mientras el depósito esté en Borrador (D29, D30).
- **Petición:** `entryCorrectionScaleSchema` = `entryCorrectionCeSchema` sin `merchandiseValue`, `usesCargoUnits`, `cargoUnits` ni `manifestDate`; `reason` obligatorio (10 a 500) si el ciclo está completo.
- **Respuesta 200:** `dataSchema(depositEntrySchema)`.
- **Errores:** los de C-F01-90, más 409 «El depósito {N} ya está confirmado: la corrección la hace Comercio Exterior.» y 400 «Indique el motivo de la corrección (de 10 a 500 caracteres).»
- **Zod:** `entryCorrectionScaleSchema`, `depositEntrySchema`. Lo maqueta F03 («Editar» del historial, P-BAS-08).

##### C-F01-93 · `GET weighbridge/entries/{entryId}` (nuevo)
- **Petición:** el Id de la entrada en la ruta.
- **Política:** `EntryEditAccess` (Admin, Scale, ForeignTrade).
- **Respuesta 200:** `dataSchema(entryForEditSchema)` = `depositEntrySchema` más los datos de Vigilancia (`entryLogId`, `licensePlate`, `entryReasonId`, `entryReasonCategory`, `dateTimeEntry`), el conductor completo, la modalidad, el depósito (`warehouseStorageId`, número y estado), `usesCargoUnits` y `cargoUnits[]`, y `canScaleEdit` (bool: depósito en Borrador).
- **Errores:** 404 «La entrada no existe.» **Zod:** `entryForEditSchema` (`F/features/weighbridge/contracts/entry-edit.ts`).

#### 2.2.4 Grupo E — Salidas (fase 5)

**Forma de la salida** (`exitSchema`, `F/features/exits/contracts/exit.ts`), que devuelven C-F01-95 a C-F01-105:

```jsonc
{
  "id": "guid",
  "number": "2026SM00041",
  "type": "Consolidated",                 // EntryTicket | Global | Deposit | Consolidated
  "status": "Confirmed",                  // Draft | Confirmed | Completed | Cancelled
  "missing": ["Loading", "Weighing"],     // Loading | Weighing | YardExit; vacío si no le falta nada
  "origin": "ForeignTrade",               // ForeignTrade | Weighbridge
  "modalityCode": "IMP",                  // null en el Borrador de Báscula sin líneas
  "createdAt": "2026-11-12T08:00:00-05:00",
  "vehicle": { "id": "guid", "licensePlate": "PQR555" },
  "driver": { "id": "guid", "fullName": "Conductor 5", "idType": "Cc", "idNumber": "1000005" },
  "carrierCompany": { "id": "guid", "name": "Transportes Ejemplo" },
  "destination": { "cityId": "guid", "cityName": "Pasto", "address": null },
  "customerOrder": { "number": "OC-77", "issuerId": "guid", "issuerName": "Agencia A", "date": "2026-11-11", "fileUrl": null },
  "observations": null,
  "deposits": [ { "warehouseStorageId": "guid", "number": "2026BA00011", "customerName": "Cliente A" } ],
  "tickets": [],                          // en EntryTicket y Global: { "warehouseStorageEntryId", "ticketNumber", "licensePlate" }
  "lines": [
    { "id": "guid", "warehouseStorageId": "guid", "warehouseStorageNumber": "2026BA00011",
      "warehouseStorageProductId": "guid", "productName": "Cebolla", "packaging": "Sacos",
      "cargoUnitId": null, "quantity": 300, "loadedQuantity": null, "allocatedWeight": null }
  ],
  "guide": { "id": "guid", "number": "2026S00034", "issuedAt": "…", "expirationDate": "…",
             "signerType": "Driver", "paymentMode": "Immediate", "invoiceId": "guid", "isCancelled": false },
                                          // null en Borrador y en inspección
  "loading": null,                        // { "loadedAt", "loadedByName", "crewId", "crewName", "observations", "photoCount" }
  "yardExit": null,                       // { "exitedAt", "exitedByName", "observations" }
  "weighing": null,                       // { "cycleId", "ticketNumber", "status", "netWeight" }
  "dispatchedWeight": null,
  "confirmedAt": "…", "confirmedByName": "Usuario CE 1",
  "cancelledAt": null, "cancelledByName": null, "cancellationReason": null,
  "guideHistory": [ { "number": "2026S00030", "cancelledAt": "…", "reason": "…" } ]
}
```

##### C-F01-94 · `GET exits` (nuevo)
- **Política:** `ExitAccess` (Admin, ForeignTrade, Warehouse, Scale).
- **Petición (query), orden y filtros (C-F01-00):** `number` (texto), `createdAtFrom`, `createdAtTo`, `type` (enum, varios), `status` (enum, varios), `missing` (enum, varios: las que les falta alguno de esos), `depositNumber` (texto), `licensePlate` (texto), `guideNumber` (texto), `warehouseStorageId` (guid, para la etapa Salidas del depósito), más paginación.
- **Orden:** lista blanca `number`, `createdAt`, `type`, `status`, `confirmedAt`; por defecto `createdAt desc`.
- **Respuesta 200:** `pagedSchema(exitListItemSchema)` — `id`, `number`, `createdAt`, `type`, `status`, `missing`, `depositNumbers[]`, `licensePlates[]`, `ticketNumbers[]`, `guideNumber`, `confirmedAt`, `dispatchedWeight`, `destinationCityName`.
- **Errores:** los de C-F01-00. **Zod:** `exitListQuerySchema`, `exitListItemSchema`.
- **Notas:** «Órdenes de salida» de Bodega = `status=Confirmed&missing=Loading,YardExit`; su historial = `status=Completed` (F06).

##### C-F01-95 · `GET exits/{id}` (nuevo)
- **Petición:** el Id en la ruta.
- **Política:** `ExitAccess`. **Respuesta 200:** `dataSchema(exitSchema)`. **Errores:** 404 «La salida no existe.» **Zod:** `exitSchema`.

##### C-F01-96 · `POST exits` (nuevo)
- **Política:** `ForeignTradeAccess`.
- **Petición:** `exitUpsertSchema`:

| Campo | Tipo | Obligatorio | Regla |
| --- | --- | --- | --- |
| `kind` | `EntryTicket` \| `Global` \| `ByDeposit` | Sí | Con `ByDeposit`, el sistema fija `Deposit` (un depósito) o `Consolidated` (varios) (AF-32) |
| `warehouseStorageIds` | guid[] | Sí | Confirmados (D33); en importación con levante; uno solo en `EntryTicket` y `Global` |
| `ticketEntryIds` | guid[] | En `EntryTicket` (uno) y `Global` (dos o más) | Entradas no anuladas del depósito y sin otra salida activa |
| `lines[]` | `{ warehouseStorageProductId, cargoUnitId?, quantity }` | Sí, al menos una | `quantity` > 0 y ≤ disponible y, en importación, ≤ nacionalizado disponible (D35). En `EntryTicket` y `Global` se precargan con lo declarado de los tiquetes y se pueden ajustar |
| `vehicleId`, `driverId` | guid | Sí | Activos |
| `carrierCompanyId` | guid \| null | No | Tercero `TRANSPORT_COMPANY` |
| `destinationCityId` | guid | Sí | Ciudad activa del catálogo |
| `destinationAddress` | string \| null | No | Hasta 250 |
| `customerOrder` | `{ number, issuerId, date, fileUrl? }` \| null | No | Si viene: número hasta 50, emisor agencia o importador, fecha no futura |
| `observations` | string \| null | No | Hasta 500 |

- **Efecto:** crea la salida en Borrador con su número (D1) y reserva sus líneas (D35).
- **Respuesta 201:** `dataSchema(exitSchema)`.
- **Errores:**

| Status | Mensaje |
| --- | --- |
| 400 | «Agregue al menos una línea con cantidad mayor que cero.» |
| 400 | «Una salida por tiquete lleva un solo tiquete; la global, dos o más.» |
| 400 | «Una salida por tiquete o global es de un solo depósito.» |
| 400 | «Los depósitos de una salida deben ser de la misma modalidad.» |
| 409 | «El depósito {N} no está confirmado.» |
| 409 | «{producto} del depósito {N}: disponible {d}, pidió {q}.» |
| 409 | «{producto} del depósito {N}: nacionalizado disponible {n}, pidió {q}.» |
| 409 | «El tiquete {T} ya está en la salida {S}.» |
| 404 | «El depósito, el vehículo, el conductor o la ciudad no existe.» (con el que falta) |

- **Zod:** `exitUpsertSchema`, `exitSchema`.

##### C-F01-97 · `PUT exits/{id}` (nuevo)
- **Política:** `ForeignTradeAccess`. **Petición:** `exitUpsertSchema` completo; completa también el Borrador que creó Báscula (AF-37).
- **Efecto:** reemplaza las líneas y rehace sus reservas en la misma transacción.
- **Respuesta 200:** `dataSchema(exitSchema)`. **Errores:** los de C-F01-96 y 409 «La salida {N} no está en Borrador: anule la guía para corregirla.» **Zod:** `exitUpsertSchema`, `exitSchema`.

##### C-F01-98 · `POST exits/{id}/confirm` (nuevo)
- **Política:** `ForeignTradeAccess`.
- **Petición:** `exitConfirmSchema` — `departureDatetime` (fecha y hora, obligatoria, no anterior a hoy menos un día), `observations` (string \| null, hasta 500, se imprime en la guía), `billing` (`BillingRecipientInput` de hoy, D47; obligatorio salvo en inspección, donde se ignora).
- **Efecto:** D36 — emite la guía (salvo inspección) con su cobro y su firmante, descuenta el stock (`GoodsExit`), consume las reservas y cierra los depósitos sin stock.
- **Respuesta 200:** `dataSchema(exitSchema)` con `guide`.
- **Errores:**

| Status | Mensaje |
| --- | --- |
| 409 | «La salida {N} no está en Borrador.» |
| 400 | «Complete la salida antes de confirmar: {lo que falta}.» (líneas, vehículo, conductor o ciudad) |
| 409 | «{producto} del depósito {N}: disponible {d}, pidió {q}.» (el stock cambió) |
| 409 | «El tercero {nombre} tiene las salidas bloqueadas.» (marca «sin salidas» de hoy, BR-05-004) |
| 400 | los de formato del cobro de hoy (`BillingRecipientInput`) |

- **Zod:** `exitConfirmSchema`, `billingRecipientInputSchema` (`F/features/billing/contracts/billing-recipient.ts`), `exitSchema`.

##### C-F01-99 · `POST exits/{id}/reopen` (nuevo)
- **Política:** `ForeignTradeAccess`.
- **Petición:** `{ "reason": "…" }` (10 a 500).
- **Efecto:** D34 — anula la guía vigente con el motivo (en inspección no hay guía), devuelve el stock (`GoodsExitReversal`), reactiva las reservas, reabre los depósitos cerrados y deja la salida en Borrador. Conserva el cargue y el pesaje ya registrados.
- **Respuesta 200:** `dataSchema(exitSchema)`.
- **Errores:** 409 «La salida {N} está completada: ya no se modifica.»; 409 «La salida {N} no está confirmada.»; 400 «Indique el motivo (de 10 a 500 caracteres).»; 409 los de la factura de la guía de hoy (`DispatchGuideInvoicedRule`).
- **Zod:** `reasonBodySchema` (`F/shared/contracts/api.ts`), `exitSchema`.

##### C-F01-100 · `POST exits/{id}/cancel` (nuevo)
- **Política:** `ForeignTradeAccess`. **Petición:** `{ "reason": "…" }`.
- **Efecto:** Borrador → Cancelada; libera las reservas.
- **Respuesta 200:** `dataSchema(exitSchema)`.
- **Errores:** 409 «Solo se cancela una salida en Borrador.»; 409 «La salida {N} tiene el pesaje {T} sin anular: anúlelo primero.»; 400 del motivo. **Zod:** `reasonBodySchema`, `exitSchema`.

##### C-F01-101 · `GET exits/by-plate/{plate}` (nuevo)
- **Petición:** la placa en la ruta.
- **Política:** `ScaleAccess`.
- **Respuesta 200:** `dataSchema(z.array(exitSchema))` — las salidas `Deposit` o `Consolidated` en Borrador o Confirmadas, sin pesaje de salida, del vehículo de esa placa (sin distinguir mayúsculas ni espacios); vacía si no hay.
- **Errores:** ninguno. **Zod:** `exitSchema`. **Notas:** con una, Báscula la precarga; con varias, el operario elige; sin ninguna, avisa que se creará una en Borrador (F03, P-BAS-03).

##### C-F01-102 · `GET exits/available-stock` (nuevo)
- **Política:** `ForeignTradeAccess`.
- **Petición (query):** `warehouseStorageIds` (guid, varios separados por coma), `exceptExitId` (guid, opcional: al editar, no cuenta sus propias reservas).
- **Respuesta 200:** `dataSchema(z.array(availableStockSchema))` — por producto del depósito: `warehouseStorageId`, `warehouseStorageNumber`, `warehouseStorageProductId`, `productName`, `packaging`, `receivedQuantity`, `currentStock`, `reservedByOthers`, `available`, `nationalizedAvailable` (nulo fuera de importación), `cargoUnits[]` (`id`, `identifier`, `stock`).
- **Errores:** 400 «Indique al menos un depósito.» **Zod:** `availableStockSchema`.

##### C-F01-103 · `GET exits/entry-tickets` (nuevo)
- **Política:** `ForeignTradeAccess`.
- **Petición (query):** `warehouseStorageId` (obligatorio).
- **Respuesta 200:** `dataSchema(z.array(entryTicketSchema))` — por entrada no anulada: `warehouseStorageEntryId`, `ticketNumber`, `licensePlate`, `entryDate`, `products[]` (`warehouseStorageProductId`, `productName`, `packaging`, `declaredQuantity`), `activeExitNumber` (nulo si no está en otra salida activa).
- **Errores:** 404 «El depósito no existe.» **Zod:** `entryTicketSchema`.

##### C-F01-104 · `POST exits/{id}/loading` (nuevo)
- **Política:** `WarehouseAccess`.
- **Petición:** `exitLoadingSchema` — `lines[]` (`{ lineId, loadedQuantity }`, de 0 a la cantidad de la línea), `crewId` (guid \| null), `signatureDriver` (base64, obligatoria, como hoy), `observations` (hasta 250), `photos[]` (como hoy: `fileName`, `contentType`, `base64`).
- **Efecto:** D38 — registra el cargue, libera ubicaciones LIFO, avisa a CE si lo cargado difiere de la guía y completa la salida si ya tiene el pesaje.
- **Respuesta 200:** `dataSchema(exitSchema)` más `releasedPlacements[]` (`locationCode`, `quantity`) y `differsFromGuide` (bool).
- **Errores:**

| Status | Mensaje |
| --- | --- |
| 409 | «La salida {N} es por tiquete o global: se completa con la salida de patio.» |
| 409 | «La salida {N} no está confirmada.» |
| 409 | «La salida {N} ya tiene registrado el cargue.» |
| 409 | «La salida {N} no tiene guía vigente.» (`DEC-056`) |
| 400 | «{producto}: no se puede cargar más de lo que dice la guía ({q}).» |
| 400 | «La firma del conductor es obligatoria.» |

- **Zod:** `exitLoadingSchema`, `exitSchema`.

##### C-F01-105 · `POST exits/{id}/yard-exit` (nuevo)
- **Política:** `WarehouseAccess`.
- **Petición:** `{ "observations": null }` (hasta 250).
- **Efecto:** D38 — fecha y hora del servidor; la salida queda Completada.
- **Respuesta 200:** `dataSchema(exitSchema)`.
- **Errores:** 409 «La salida {N} es por número de depósito o consolidada: se completa con el cargue y el pesaje.»; 409 «La salida {N} no está confirmada.»; 409 «La salida {N} ya tiene registrada la salida de patio.» **Zod:** `exitYardExitSchema`, `exitSchema`.

##### C-F01-106 · `GET exits/{id}/guide/pdf` (nuevo)
- **Petición:** el Id de la salida en la ruta.
- **Política:** `ExitAccess`. **Respuesta 200:** `application/pdf`, nombre `guia-{número}.pdf`; sin sello ni unidad de medida (D18, D36). **Errores:** 404 «La salida no tiene guía.» **Zod:** no aplica (archivo).

##### C-F01-107 · `GET exits/{id}/guide/pdf/per-deposit` (nuevo)
- **Petición:** el Id de la salida en la ruta.
- **Política:** `ForeignTradeAccess`. **Respuesta 200:** `application/zip` con un PDF por depósito, solo en consolidadas (AF-97). **Errores:** 409 «El ZIP por depósito es solo para salidas consolidadas.»; 404 como C-F01-106. **Zod:** no aplica (archivo).

##### C-F01-108 · `PATCH exits/{id}/guide/payment-mode` (nuevo)
- **Política:** la de hoy de `dispatch-guides/{id}/payment-mode` (`B/Wms.Api/Controllers/v1/ForeignTradeController.cs:1325`). **Petición y regla:** las de hoy (`paymentMode`). **Respuesta 200:** `dataSchema(exitSchema)`. **Errores:** los de hoy. **Zod:** `guidePaymentModeSchema`, `exitSchema`.

##### C-F01-109 · `POST weighbridge/output/initiate` (modificado)
- **Política:** `ScaleAccess`.
- **Petición** (cambios): sale `loadingOrderNumber` y el modo de órdenes adicionales; entra `exitId` (guid \| null). Con `exitId`, la salida debe ser `Deposit` o `Consolidated`, en Borrador o Confirmada y sin pesaje de salida. Sin él, se crea una salida en Borrador con la placa del camión, `driverId` y `carrierCompanyId` del registro (D37). El tipo de vehículo deja de ser obligatorio (D24).
- **Efecto:** si el conductor o el vehículo difieren de los de la salida: en Borrador se actualizan; con guía, no cambian y se avisa a CE (D37, D45).
- **Respuesta 201** (`InitiateOutputResponseDto`): salen `loadingOrderId` y `loadingOrderNumber`; entran `exitId`, `exitNumber`, `exitCreated` (bool) y `driverChangeNotified` (bool).
- **Errores:** 400 «La salida {N} es por tiquete o global: no pasa por báscula.»; 409 «La salida {N} ya tiene el pesaje {T}.»; 409 «La salida {N} está {estado}: no se puede pesar.»; 400 «Elija la empresa de transporte del camión.» (sin `exitId`). Sale «Báscula no pesa la salida sin una orden de cargue…».
- **Zod:** `outputInitiateChangesSchema`, `outputInitiateResultChangesSchema` (`F/features/weighbridge/contracts/output.ts`); F03 los une a la petición y la respuesta de hoy.

##### C-F01-110 · `POST weighbridge/output/process-payment` (modificado)
- **Política:** `ScaleAccess`. **Qué cambia:** la factura de báscula de la salida se asocia al ciclo de la salida, no a la orden. **Petición:** la de hoy. **Respuesta:** la de hoy, con `loadingOrder*` → `exit*` (regla R-SAL). **Errores:** los de hoy. **Zod:** lo escribe F03 con la forma de hoy y R-SAL.

##### C-F01-111 · `POST weighbridge/output/start-pending-billing` (modificado)
- **Política:** `ScaleAccess`. **Qué cambia:** igual que C-F01-110. **Petición:** la de hoy. **Respuesta:** la de hoy con R-SAL. **Errores:** los de hoy. **Zod:** lo escribe F03 con la forma de hoy y R-SAL.

##### C-F01-112 a C-F01-138 · Órdenes de cargue y guías por orden (retirados)

Petición, respuesta, errores y Zod: no aplica; responden 404 desde la fase 5. Las pantallas que los usan (`F/pages/foreign-trade/loading-orders/*`, `F/pages/foreign-trade/dispatch-guides/*`, `F/pages/warehouse/loading-orders/*` y los pasos de salida de báscula) dejan de funcionar en `fase-2` hasta F03 y F06 (`PM/` §5.4, M9).

| ID | Endpoint | Política de hoy | Lo reemplaza |
| --- | --- | --- | --- |
| C-F01-112 | `GET foreign-trade/loading-orders` | `ForeignTradeAccess` | C-F01-94 |
| C-F01-113 | `GET foreign-trade/loading-orders/deposits` | `ForeignTradeAccess` | C-F01-102 |
| C-F01-114 | `GET foreign-trade/loading-orders/{id}` | `ForeignTradeAccess` | C-F01-95 |
| C-F01-115 | `GET foreign-trade/loading-orders/{id}/dispatch-guide-preview` | `ForeignTradeAccess` | C-F01-95 (líneas y saldos) |
| C-F01-116 | `POST foreign-trade/loading-orders` | `ForeignTradeAccess` | C-F01-96 |
| C-F01-117 | `GET foreign-trade/loading-orders/{id}/pdf` | `ForeignTradeAccess` | Nada (`DEC-016`: la orden ya no tenía PDF propio en uso) |
| C-F01-118 | `PATCH foreign-trade/loading-orders/{id}/cancel` | `ForeignTradeAccess` | C-F01-100 |
| C-F01-119 | `GET foreign-trade/dispatch-guides` | `ForeignTradeAccess` | C-F01-94 (`guideNumber`) |
| C-F01-120 | `GET foreign-trade/dispatch-guides/pending-orders` | `ForeignTradeAccess` | C-F01-94 (`status=Draft`) |
| C-F01-121 | `GET foreign-trade/dispatch-guides/pending` | `ForeignTradeAccess` | C-F01-94 |
| C-F01-122 | `GET foreign-trade/dispatch-guides/{id}/pdf` | `ForeignTradeAccess` | C-F01-106 |
| C-F01-123 | `GET foreign-trade/dispatch-guides/{id}/pdf/per-deposit` | `ForeignTradeAccess` | C-F01-107 |
| C-F01-124 | `POST foreign-trade/dispatch-guides` | `ForeignTradeAccess` | C-F01-98 |
| C-F01-125 | `PATCH foreign-trade/dispatch-guides/{id}/payment-mode` | `ForeignTradeAccess` | C-F01-108 |
| C-F01-126 | `PUT foreign-trade/loading-orders/{id}/items` | `ForeignTradeAccess` | C-F01-97 |
| C-F01-127 | `POST foreign-trade/dispatch-guides/{id}/cancel` | `ForeignTradeAccess` | C-F01-99 |
| C-F01-128 | `POST foreign-trade/loading-orders/{id}/revert` | `ForeignTradeAccess` | Nada: una completada no se reabre (AF-90); antes de completar, C-F01-99 |
| C-F01-129 | `POST foreign-trade/loading-orders/{id}/exit-with-entry-ticket` | `ForeignTradeAccess` | C-F01-96 con `kind = EntryTicket` y C-F01-105 |
| C-F01-130 | `GET warehouse/loading-orders/pending` | `WarehouseAccess` | C-F01-94 (`status=Confirmed&missing=Loading,YardExit`) |
| C-F01-131 | `GET warehouse/loading-orders/{id}` | `WarehouseAccess` | C-F01-95 |
| C-F01-132 | `GET warehouse/loading-orders/{id}/pdf` | `WarehouseAccess` | C-F01-106 |
| C-F01-133 | `PATCH warehouse/loading-orders/{id}/cancel` | `WarehouseAccess` | Nada: Bodega no cancela salidas |
| C-F01-134 | `POST warehouse/loading-orders/{id}/execute` | `WarehouseAccess` | C-F01-104 |
| C-F01-135 | `GET weighbridge/loading-orders/by-plate/{plate}` | `ScaleAccess` | C-F01-101 |
| C-F01-136 | `GET weighbridge/loading-orders/{number}` | `ScaleAccess` | C-F01-101 y C-F01-95 |
| C-F01-137 | `POST weighbridge/output/cycles/{cycleId}/additional-orders` | `ScaleAccess` | Nada: una salida consolidada lleva varios depósitos (AF-32) |
| C-F01-138 | `POST weighbridge/output/from-entry-ticket` | `ScaleAccess` | Nada: la salida por tiquete no pasa por báscula (AF-29) |

Las políticas de hoy se confirman en los controladores al retirar (`ForeignTradeController`, `WarehouseController`, `LoadingOrderCorrectionsController`, `LoadingOrderExitController`, `WeighbridgeController`, `WeighbridgeOutputSharingController`).

##### C-F01-139 · `GET public/dispatch-guides/verify/{token}` (modificado)
- **Política:** anónimo, como hoy (`DEC-060`). **Qué cambia:** los datos salen de la guía de la salida; sin unidad de medida (D18). **Petición:** la de hoy (`token` en la ruta). **Respuesta:** `PublicDispatchGuideVerificationDto` sin cambios de forma salvo R-UOM. **Errores:** los de hoy. **Zod:** no aplica (página pública sin cambios de forma).

#### 2.2.5 Grupo F — Facturación (fase 6)

##### C-F01-140 · `PUT billing/warehouse-storages/{id}/trm` (retirado)
- **Política de hoy:** `BillingAccess` (`B/Wms.Api/Controllers/v1/BillingController.cs:660-687`). **Lo reemplaza:** C-F01-11 y C-F01-12 (tasa semanal, D42 y D43). Petición, respuesta, errores y Zod: no aplica; 404 desde la fase 6.

#### 2.2.6 Lecturas que cambian por regla

Dos reglas cambian campos en lecturas que maquetan otras features. La forma nueva la fija la regla; el esquema Zod lo escribe la feature que maqueta la pantalla (columna «Maqueta»), con esta regla.

- **R-UOM** (fase 2, D18): desaparecen `unitMeasureId`, `unitMeasureCode`, `unitMeasureName`, `unitMeasure` y `uom` de toda respuesta.
- **R-SAL** (fase 5, D2): `loadingOrderId`, `loadingOrderNumber` y `loadingOrderStatus` pasan a `exitId`, `exitNumber` y `exitStatus` (valores de `ExitStatus`); lo que hoy cuenta órdenes cuenta salidas; los datos de despacho salen de las salidas con guía.

| ID | Endpoint | Regla | Política | Maqueta |
| --- | --- | --- | --- | --- |
| C-F01-142 | `GET foreign-trade/imports` | R-UOM | la de hoy | F05 |
| C-F01-143 | `GET foreign-trade/exports` | R-UOM | la de hoy | F05 |
| C-F01-144 | `GET foreign-trade/inspections` | R-UOM | la de hoy | F05 |
| C-F01-145 | `GET foreign-trade/warehouse-storages/{id}/cargo-units` | R-UOM | la de hoy | F05 |
| C-F01-146 | `GET warehouse/warehouse-storages/{id}/cargo-units` | R-UOM | la de hoy | F04 |
| C-F01-147 | `GET warehouse/inventory/movements` | R-UOM y R-SAL | la de hoy | F04 |
| C-F01-148 | `GET warehouse/inventory/stock/{warehouseStorageId}` | R-UOM | la de hoy | F04 |
| C-F01-149 | `GET warehouse/pending-from-weighbridge` | R-UOM | la de hoy | F04 |
| C-F01-150 | `GET warehouse/search/plate/{plate}` | R-UOM y R-SAL | la de hoy | F04 |
| C-F01-151 | `GET warehouse/receptions` | R-UOM | la de hoy | F04 |
| C-F01-152 | `GET warehouse/pending-direct-reception` | R-UOM | la de hoy | F04 |
| C-F01-153 | `GET weighbridge/lookup` | R-UOM | la de hoy | F03 |
| C-F01-154 | `GET weighbridge/service-records/by-document` | R-UOM y R-SAL | la de hoy | F03 |
| C-F01-155 | `GET weighbridge/service-records/{serviceRecordId}/registration` | R-UOM y R-SAL | la de hoy | F03 |
| C-F01-156 | `GET weighbridge/history` | R-SAL | la de hoy | F03 |
| C-F01-157 | `GET reports/abandonment-candidates` | R-UOM | la de hoy | F08 |
| C-F01-158 | `GET reports/abandonment-exits` | R-SAL | la de hoy | F08 |
| C-F01-159 | `GET reports/daily-outgoing-goods` (y su `/pdf`) | R-SAL | la de hoy | F08 |
| C-F01-160 | `GET reports/statistics` | R-SAL | la de hoy | F08 |
| C-F01-161 | `GET warehouse/movements-report` (y su `/pdf`) | R-UOM y R-SAL | la de hoy | F08 |
| C-F01-162 | `GET reports/traceability` | R-SAL (solo datos; forma igual) | la de hoy | — |

Para todas: petición sin cambios; respuesta = la de hoy con la regla; errores, los de hoy. Si una lectura no listada lleva alguno de esos campos, se le aplica la regla y se agrega a esta tabla en el commit de su fase.

**R-UOM: el embalaje reemplaza a la unidad en las agrupaciones** (respuesta del usuario del 2026-11-23, «Por embalaje», en la fase 2). Lo que hoy no sumaba unidades distintas (CHG-69, CHG-72) agrupa por el tipo de embalaje de la línea del depósito: resumen de existencias del tablero, saldos del listado de importaciones, total del historial y del PDF de la guía, columna «Ampara» del rótulo y detalle «ALMACENAMIENTO DE» de la factura («40 SACOS CEBOLLA»; sin embalaje, «40 CEBOLLA»). Tres campos cambian de nombre en lugar de desaparecer:

| ID | Endpoint | Antes | Ahora | Maqueta |
| --- | --- | --- | --- | --- |
| C-F01-142 | `GET foreign-trade/imports` | `balances[].unitMeasure` | `balances[].packaging` (texto; «—» sin embalaje) | F05 |
| C-F01-86 | `GET foreign-trade/imports/{id}` | `warehouseReception.lines[].unitMeasure` | `warehouseReception.lines[].packaging` (texto o nulo) | F05 |
| C-F01-171 | `GET foreign-trade/dispatch-guides` (historial de guías) | `products[].unitMeasure` | `products[].packaging` (texto; vacío sin embalaje); `quantity` es nula si la guía mezcla embalajes | F06 |

`GET public/dispatch-guides/verify/{token}` (C-F01-139) pierde `lines[].unitMeasure` por R-UOM: sus líneas quedan con `productName` y `quantity`. La migración `RemoveUnitMeasure` también quita `warehouse_storage_products.unit_measure_id`, que apuntaba a la tabla que D18 borra.

### 2.3 Esquemas Zod y tipos

Zod 4 (`Frontend/wms/package.json`: `"zod": "^4.1.13"`). Reglas:

- Los Id se validan con `z.guid()`, no con `z.uuid()`: las semillas tienen Id que no cumplen la variante RFC 9562 (por ejemplo `3f9b0c4e-7a2d-4b8f-e1c5-6a3d9e2b0f81`, `B/Wms.Infrastructure/Persistence/SeedDataExtensions.cs:293`), y `z.uuid()` los rechaza.
- Fechas con hora: `z.iso.datetime({ offset: true })`; días: `z.iso.date()`.
- Los tipos se derivan con `z.infer` en el mismo archivo (`export type X = z.infer<typeof xSchema>`). No se escriben a mano.
- Los esquemas **completos** son los de los endpoints que maqueta F02 (grupo B, C-F01-69 a C-F01-72 y C-F01-141) y los nuevos de F01 (salidas, edición del ingreso). Para los endpoints de hoy que cambian en pocos campos y maqueta otra feature (C-F01-78 a C-F01-89, C-F01-109 a C-F01-111, R-UOM, R-SAL) este plan da el esquema **del cambio**, y la feature que los maqueta (F03, F04, F05, F08) los completa con los campos de hoy en su plan, con `.extend()` y `.omit()`.

**`F/shared/contracts/api.ts`** (lo crea F02 y lo usan todas las features)

```ts
import { z } from "zod";

export const guidSchema = z.guid();
export const dateTimeSchema = z.iso.datetime({ offset: true });
export const dateOnlySchema = z.iso.date();
export const sortOrderSchema = z.enum(["asc", "desc"]);
export const identificationTypeSchema = z.enum(["Nit", "Rut", "Cc", "Pasaporte", "Ruc"]);
export const systemRoleCodeSchema = z.enum(["Scale", "Receiving", "Warehouse", "ForeignTrade", "Billing", "Admin"]);

export const paginationSchema = z.object({
  pageIndex: z.int().min(1),
  pageSize: z.int().min(1),
  totalCount: z.int().min(0),
  totalPages: z.int().min(0),
});
export const dataSchema = <T extends z.ZodType>(item: T) => z.object({ data: item });
export const pagedSchema = <T extends z.ZodType>(item: T) =>
  z.object({ data: z.array(item), pagination: paginationSchema });

/** Paginación y orden de C-F01-00. `pageSize` hasta 50; `all` para todo. */
export const listQueryBaseSchema = z.object({
  pageIndex: z.int().min(1).optional(),
  pageSize: z.int().min(1).max(50).optional(),
  all: z.boolean().optional(),
  sortField: z.string().optional(),
  sortOrder: sortOrderSchema.optional(),
});

export const reasonSchema = z.string().trim().min(10).max(500);
export const reasonBodySchema = z.object({ reason: reasonSchema });

export const problemSchema = z.object({
  type: z.string().optional(),
  title: z.string().optional(),
  status: z.int(),
  description: z.string().optional(),
  errors: z.array(z.object({ code: z.string(), description: z.string() })).optional(),
});
export type ListQueryBase = z.infer<typeof listQueryBaseSchema>;
```

**`F/features/entries/contracts/entry-reason.ts`**

```ts
import { z } from "zod";
import { guidSchema, listQueryBaseSchema } from "~/shared/contracts/api";

export const entryReasonCategorySchema = z.enum(["Entry", "Exit", "WeighingOnly"]);
export const entryReasonSchema = z.object({
  id: guidSchema,
  description: z.string(),
  requiresWeighing: z.boolean(),
  category: entryReasonCategorySchema.nullable(),
});
export const entryReasonListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["description", "category", "requiresWeighing"]).optional(),
  description: z.string().optional(),
  category: z.array(z.enum(["Entry", "Exit", "WeighingOnly", "None"])).optional(), // se envía separado por comas
  requiresWeighing: z.boolean().optional(),
});
const entryReasonFields = z.object({
  description: z.string().trim().min(3).max(100),
  requiresWeighing: z.boolean(),
  category: entryReasonCategorySchema.nullable(),
});
const categoryRule = (v: { requiresWeighing?: boolean; category?: string | null }) =>
  v.requiresWeighing === undefined || (v.requiresWeighing ? v.category != null : v.category == null);
export const entryReasonCreateSchema = entryReasonFields.refine(categoryRule, {
  message: "Elija la categoría del motivo: Ingreso, Salida o Solo báscula.",
  path: ["category"],
});
export const entryReasonUpdateSchema = entryReasonFields.partial();
export type EntryReason = z.infer<typeof entryReasonSchema>;
```

**`F/features/entries/contracts/entry-log-correction.ts`**

```ts
import { z } from "zod";
import { dateTimeSchema, guidSchema, reasonSchema } from "~/shared/contracts/api";

export const entryLogCorrectionSchema = z.object({
  licensePlate: z.string().trim().min(3).max(15).nullable().optional(),
  entryReasonId: guidSchema.nullable().optional(),
  dateTimeEntry: dateTimeSchema.nullable().optional(),
  reason: reasonSchema,
});
export const entryLogCorrectionResultSchema = z.object({
  entryLog: z.object({ id: guidSchema, licensePlate: z.string(), dateTimeEntry: dateTimeSchema }).loose(),
  changes: z.array(z.object({ field: z.string(), previousValue: z.string().nullable(), newValue: z.string().nullable() })),
  depositsNotUpdated: z.array(z.object({ warehouseStorageNumber: z.string(), entryDate: dateTimeSchema.nullable() })),
  deactivatedVehiclePlate: z.string().nullable(),
});
```

**`F/features/entries/contracts/driver.ts`**

```ts
import { z } from "zod";
import { dateTimeSchema, guidSchema, identificationTypeSchema, listQueryBaseSchema } from "~/shared/contracts/api";

export const driverSchema = z.object({
  id: guidSchema,
  firstName: z.string(),
  lastName: z.string(),
  idNumber: z.string(),
  idType: identificationTypeSchema,
  country: z.string().nullable(),
  phoneNumber: z.string().nullable(),
  isActive: z.boolean(),
  createdAt: dateTimeSchema,
  updatedAt: dateTimeSchema.nullable(),
});
export const driverListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["idNumber", "firstName", "lastName", "country", "isActive", "createdAt"]).optional(),
  name: z.string().optional(),
  idNumber: z.string().optional(),
  idType: identificationTypeSchema.optional(),
  isActive: z.boolean().optional(),
  search: z.string().optional(),
});
export const driverCreateSchema = z.object({
  firstName: z.string().trim().min(1).max(150),
  lastName: z.string().trim().min(1).max(150),
  idNumber: z.string().trim().min(1).max(50),
  idType: identificationTypeSchema,
  country: z.string().max(100).nullable(),
  phoneNumber: z.string().max(20).nullable(),
});
export const driverUpdateSchema = driverCreateSchema.partial().extend({ isActive: z.boolean().optional() });
export const driverRecentEntrySchema = z.object({
  entryLogId: guidSchema,
  dateTimeEntry: dateTimeSchema,
  licensePlate: z.string(),
  ticketNumber: z.string().nullable(),
});
export type Driver = z.infer<typeof driverSchema>;
```

**`F/features/entries/contracts/vehicle.ts`**

```ts
import { z } from "zod";
import { dateTimeSchema, guidSchema, listQueryBaseSchema } from "~/shared/contracts/api";

export const vehicleSchema = z.object({
  id: guidSchema,
  licensePlate: z.string(),
  carrierCompanyId: guidSchema.nullable(),
  carrierCompanyName: z.string().nullable(),
  country: z.string().nullable(),
  vehicleType: z.string().nullable(),
  isActive: z.boolean(),
  createdAt: dateTimeSchema,
  updatedAt: dateTimeSchema.nullable(),
});
export const vehicleListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["licensePlate", "country", "vehicleType", "isActive", "createdAt"]).optional(),
  licensePlate: z.string().optional(),
  carrierCompanyId: guidSchema.optional(),
  country: z.string().optional(),
  vehicleType: z.string().optional(),
  isActive: z.boolean().optional(),
});
export const vehicleCreateSchema = z.object({
  licensePlate: z.string().trim().min(3).max(15),
  carrierCompanyId: guidSchema.nullable(),
  country: z.string().nullable(),
  vehicleType: z.string().nullable(),
});
export const vehicleUpdateSchema = vehicleCreateSchema.partial().extend({ isActive: z.boolean().optional() });
```

**`F/features/settings/contracts/prefix.ts`** y **`exchange-rate.ts`**

```ts
import { z } from "zod";
import { dateOnlySchema, dateTimeSchema, guidSchema, listQueryBaseSchema } from "~/shared/contracts/api";

// prefix.ts
export const prefixedFieldSchema = z.enum(["ReleaseNumber", "AcceptanceNumber", "DianManifestNumber"]);
export const fieldPrefixSchema = z.object({
  field: prefixedFieldSchema,
  label: z.string(),
  prefix: z.string().nullable(),
  updatedAt: dateTimeSchema.nullable(),
  updatedByName: z.string().nullable(),
});
export const fieldPrefixUpdateSchema = z.object({
  prefix: z.string().trim().regex(/^[A-Za-z0-9]{1,20}$/, "El prefijo admite solo letras y dígitos, hasta 20.").nullable(),
});

// exchange-rate.ts
export const exchangeRateSchema = z.object({
  id: guidSchema,
  fromDate: dateOnlySchema,
  toDate: dateOnlySchema,
  rate: z.number().positive(),
  createdByName: z.string(),
  createdAt: dateTimeSchema,
  updatedByName: z.string().nullable(),
  updatedAt: dateTimeSchema.nullable(),
});
export const exchangeRateListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["fromDate", "rate"]).optional(),
  fromDateFrom: dateOnlySchema.optional(),
  fromDateTo: dateOnlySchema.optional(),
});
export const exchangeRateCreateSchema = z
  .object({ fromDate: dateOnlySchema, toDate: dateOnlySchema, rate: z.number().positive().multipleOf(0.01) })
  .refine((v) => v.fromDate <= v.toDate, { message: "La fecha final no puede ser anterior a la inicial.", path: ["toDate"] });
export const exchangeRateForDateSchema = z
  .object({
    date: dateOnlySchema,
    rate: z.number().positive(),
    fromDate: dateOnlySchema,
    toDate: dateOnlySchema,
    isFallback: z.boolean(),
    warning: z.string().nullable(),
  })
  .nullable();
```

**`F/features/stakeholders/contracts/stakeholder.ts`**

```ts
import { z } from "zod";
import { dateTimeSchema, guidSchema, identificationTypeSchema, listQueryBaseSchema } from "~/shared/contracts/api";

export const businessRoleSchema = z.object({ id: guidSchema, code: z.string(), name: z.string() });
export const financialStatusSchema = z.enum(["Active", "OverdueWarning", "Blocked"]);
export const stakeholderSchema = z.object({
  id: guidSchema,
  name: z.string(),
  idType: identificationTypeSchema,
  idNumber: z.string(),
  financialStatus: financialStatusSchema,
  overdueAmount: z.number().nullable(),
  commercialStatus: z.string().nullable(),
  chamberOfCommerce: z.string().nullable(),
  businessRoles: z.array(businessRoleSchema).optional(),
  isActive: z.boolean(),
  isUap: z.boolean(),
  exitsBlocked: z.boolean(),
  exitsBlockedReason: z.string().nullable(),
  exitsBlockedAt: dateTimeSchema.nullable(),
  exitsBlockedByName: z.string().nullable(),
  createdAt: dateTimeSchema,
  updatedAt: dateTimeSchema.nullable(),
});
export const stakeholderListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["name", "idNumber", "financialStatus", "isActive", "createdAt"]).optional(),
  name: z.string().optional(),
  idNumber: z.string().optional(),
  businessRolCode: z.string().optional(),
  financialStatus: financialStatusSchema.optional(),
  isActive: z.boolean().optional(),
  search: z.string().optional(),
  exitsBlocked: z.boolean().optional(),
});
export const stakeholderCreateSchema = z.object({
  name: z.string().trim().min(3).max(200),
  idType: identificationTypeSchema,
  idNumber: z.string().trim().min(1).max(30),
  commercialStatus: z.string().nullable(),
  chamberOfCommerce: z.string().nullable(),
  businessRoles: z.array(z.string()).min(1),
  bankAccounts: z.null(), // el modal no los envía: se agregan desde el detalle
  contacts: z.null(),
  isUap: z.boolean(),
});
export const stakeholderUpdateSchema = stakeholderCreateSchema
  .omit({ businessRoles: true, bankAccounts: true, contacts: true })
  .partial()
  .extend({ isActive: z.boolean().optional() });
export const stakeholderQuickRoleSchema = z.enum(["CUSTOMER", "IMPORTER", "EXPORTER", "CUSTOMS_AGENCY", "TRANSPORT_COMPANY"]);
export const stakeholderQuickCreateSchema = z.object({
  name: z.string().trim().min(3).max(200),
  idType: identificationTypeSchema,
  idNumber: z.string().trim().min(1).max(30),
  roleCode: stakeholderQuickRoleSchema,
});
export const stakeholderQuickResultSchema = z.object({
  outcome: z.enum(["Created", "RoleAdded"]),
  stakeholder: stakeholderSchema,
});
```

**`F/features/administration/contracts/`** (`packaging-type.ts`, `cargo-unit-type.ts`, `city.ts`, `crew.ts`, `system-parameter.ts`)

```ts
import { z } from "zod";
import { dateTimeSchema, guidSchema, listQueryBaseSchema } from "~/shared/contracts/api";

// packaging-type.ts y cargo-unit-type.ts (misma forma)
export const packagingTypeSchema = z.object({
  id: guidSchema, code: z.string(), name: z.string(), isActive: z.boolean(),
  createdAt: dateTimeSchema, updatedAt: dateTimeSchema.nullable(),
});
export const packagingTypeCreateSchema = z.object({ code: z.string().trim().min(1).max(30), name: z.string().trim().min(1).max(100) });
export const packagingTypeUpdateSchema = packagingTypeCreateSchema.partial();
export const cargoUnitTypeSchema = packagingTypeSchema;
export const cargoUnitTypeCreateSchema = packagingTypeCreateSchema;
export const cargoUnitTypeUpdateSchema = z.object({ name: z.string().trim().min(1).max(100).optional(), isActive: z.boolean().optional() });

// city.ts
export const citySchema = z.object({
  id: guidSchema, legacyId: z.int().nullable(), name: z.string(), countryCode: z.string(),
  district: z.string().nullable(), transitDays: z.int().nullable(), isAbandonmentDestination: z.boolean(),
  isActive: z.boolean(), createdAt: dateTimeSchema, updatedAt: dateTimeSchema.nullable(),
});
export const cityListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["name", "countryCode", "district", "transitDays", "isActive"]).optional(),
  search: z.string().optional(), countryCode: z.string().optional(), district: z.string().optional(),
  isActive: z.boolean().optional(), isAbandonmentDestination: z.boolean().optional(),
});
export const cityCreateSchema = z.object({
  name: z.string().trim().min(1).max(100), countryCode: z.string().trim().length(3), // 3 letras («COL», «ECU»), como `CreateCityValidator` (respuesta del usuario del 2026-11-23)
  district: z.string().nullable(), transitDays: z.int().min(0).nullable(), isAbandonmentDestination: z.boolean(),
});
export const cityUpdateSchema = cityCreateSchema.extend({ isActive: z.boolean() });
export const cityImportResultSchema = z.object({
  dryRun: z.boolean(), totalRows: z.int(), created: z.int(), updated: z.int(),
  errors: z.array(z.object({ row: z.int(), message: z.string() })),
});

// crew.ts
export const crewSchema = z.object({
  id: guidSchema, legacyId: z.int().nullable(), name: z.string(), isActive: z.boolean(),
  createdAt: dateTimeSchema, updatedAt: dateTimeSchema.nullable(),
});
export const crewListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["name", "isActive", "createdAt"]).optional(), search: z.string().optional(), isActive: z.boolean().optional(),
});
export const crewCreateSchema = z.object({ name: z.string().trim().min(1).max(100) });
export const crewUpdateSchema = crewCreateSchema.extend({ isActive: z.boolean() });

// system-parameter.ts
export const systemParameterSchema = z.object({
  id: guidSchema, code: z.string(), value: z.string(), description: z.string().nullable(),
  dataType: z.string(), isActive: z.boolean(), createdAt: dateTimeSchema, updatedAt: dateTimeSchema.nullable(),
});
export const systemParameterListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["code", "dataType", "isActive", "updatedAt"]).optional(),
  code: z.string().optional(), dataType: z.string().optional(), description: z.string().optional(), isActive: z.boolean().optional(),
});
export const systemParameterUpdateSchema = z.object({
  value: z.string().optional(),
  description: z.string().nullable().optional(), // PatchField: ausente = no cambia; null = borra
  dataType: z.string().optional(),
  isActive: z.boolean().optional(),
});
```

**`F/features/services/contracts/service.ts`**

```ts
import { z } from "zod";
import { dateTimeSchema, guidSchema, listQueryBaseSchema } from "~/shared/contracts/api";

export const servicePriceSchema = z.object({
  id: guidSchema, basePrice: z.number(), validFrom: dateTimeSchema, validTo: dateTimeSchema.nullable(),
  isActive: z.boolean(), isScheduled: z.boolean(),
});
export const taxSchema = z.object({
  id: guidSchema, code: z.string(), name: z.string(), percent: z.number(), isActive: z.boolean(),
  createdAt: dateTimeSchema, updatedAt: dateTimeSchema.nullable(),
});
export const serviceSchema = z.object({
  id: guidSchema, code: z.string(), name: z.string(), description: z.string().nullable(), isActive: z.boolean(),
  currentPrice: servicePriceSchema.optional(), taxes: z.array(taxSchema).optional(),
  createdAt: dateTimeSchema, updatedAt: dateTimeSchema.nullable(),
});
export const serviceListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["code", "name", "isActive", "createdAt"]).optional(),
  searchTerm: z.string().optional(), code: z.string().optional(), name: z.string().optional(), isActive: z.boolean().optional(),
});
export const serviceCreateSchema = z.object({
  code: z.string().trim().min(1).max(50), name: z.string().trim().min(1).max(150), description: z.string().nullable(),
});
export const serviceUpdateSchema = serviceCreateSchema.omit({ code: true }).partial();
```

**`F/features/warehouse/contracts/location.ts`**

```ts
import { z } from "zod";
import { dateTimeSchema, guidSchema } from "~/shared/contracts/api";

export const locationSchema = z.object({
  id: guidSchema, code: z.string(), name: z.string(), aisle: z.string().nullable(), rack: z.string().nullable(),
  level: z.string().nullable(), capacity: z.number(), isAvailable: z.boolean(), createdAt: dateTimeSchema,
});
export const locationCreateSchema = z.object({
  code: z.string().trim().min(1).max(30), name: z.string().trim().min(1).max(100), capacity: z.number().min(0),
  aisle: z.string().nullable(), rack: z.string().nullable(), level: z.string().nullable(),
});
export const locationUpdateSchema = z.object({
  name: z.string().trim().min(1).max(100), capacity: z.number().min(0),
  aisle: z.string().nullable().optional(), rack: z.string().nullable().optional(), level: z.string().nullable().optional(),
  isAvailable: z.boolean().optional(),
});
```

**`F/features/users/contracts/user.ts`** y **`F/features/audit/contracts/audit-log.ts`**

```ts
import { z } from "zod";
import { dateOnlySchema, dateTimeSchema, guidSchema, listQueryBaseSchema, systemRoleCodeSchema } from "~/shared/contracts/api";

// user.ts
export const systemRoleSchema = z.object({ id: guidSchema, code: systemRoleCodeSchema, name: z.string() });
export const userSchema = z.object({
  id: guidSchema, name: z.string(), username: z.string(), identificationNumber: z.int(), email: z.string(),
  mustChangePassword: z.boolean(), phone: z.string(), isActive: z.boolean(),
  createdAt: dateTimeSchema, updatedAt: dateTimeSchema.nullable(), lockoutEndDate: dateTimeSchema.nullable(),
  roles: z.array(systemRoleSchema).optional(), roleNames: z.array(z.string()).optional(),
});
export const userListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["name", "username", "email", "isActive", "createdAt"]).optional(),
  name: z.string().optional(), userName: z.string().optional(), email: z.string().optional(),
  identificationNumber: z.int().optional(), isActive: z.boolean().optional(), role: systemRoleCodeSchema.optional(),
});
export const userCreateSchema = z.object({
  name: z.string().trim().min(1), username: z.string().trim().min(3), identificationNumber: z.int().positive(),
  password: z.string().min(8), email: z.email(), phone: z.string().trim().min(1),
});
export const userUpdateSchema = userCreateSchema.omit({ password: true }).partial();
export const userRolesChangeSchema = z.object({ roleIds: z.array(guidSchema).min(1) });
export const userResetPasswordSchema = z.object({ newPassword: z.string().min(8) });
export const userActivationSchema = z.object({ isActive: z.boolean(), lockoutEndDate: dateTimeSchema.nullable() });

// audit-log.ts
export const auditActionSchema = z.enum(["Create", "Update", "Delete", "Activate", "Deactivate", "Archive"]);
export const auditLogSchema = z.object({
  id: guidSchema, description: z.string().nullable(), userId: guidSchema, userName: z.string(), action: auditActionSchema,
  affectedTable: z.string(), registerIdAffected: z.string(), previousValue: z.string().nullable(),
  newValue: z.string().nullable(), ipAddress: z.string().nullable(), createdAt: dateTimeSchema,
});
export const auditLogListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["createdAt", "userName", "action", "affectedTable"]).optional(),
  userName: z.string().optional(), action: auditActionSchema.optional(), affectedTable: z.string().optional(),
  registerIdAffected: z.string().optional(), createdAtFrom: dateOnlySchema.optional(), createdAtTo: dateOnlySchema.optional(),
});
```

Las reglas de contraseña del formulario son las de hoy del backend; si el validador de `CreateUserCommand` exige más que 8 caracteres, el esquema se ajusta a él en I-01.

**`F/features/products/contracts/product.ts`**

```ts
import { z } from "zod";
import { dateTimeSchema, guidSchema, listQueryBaseSchema } from "~/shared/contracts/api";

export const productSchema = z.object({
  id: guidSchema, name: z.string(), sku: z.string(), description: z.string().nullable(), packaging: z.string().nullable(),
  packagingTypeId: guidSchema.nullable(), packagingTypeName: z.string().nullable(), isActive: z.boolean(),
  createdFromWeighbridge: z.boolean(), createdAt: dateTimeSchema, updatedAt: dateTimeSchema.nullable(),
});
export const productListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["name", "sku", "packagingTypeName", "isActive", "createdAt"]).optional(),
  searchTerm: z.string().optional(), name: z.string().optional(), sku: z.string().optional(),
  packagingTypeId: guidSchema.optional(), isActive: z.boolean().optional(), createdFromWeighbridge: z.boolean().optional(),
});
export const productCreateSchema = z.object({
  name: z.string().trim().min(1).max(200), sku: z.string().trim().min(1).max(50), description: z.string().nullable(),
  packaging: z.string().nullable(), packagingTypeId: guidSchema.nullable(),
});
export const productUpdateSchema = productCreateSchema.partial().extend({ isActive: z.boolean().optional() });
```

**`F/features/billing/contracts/billing-recipient.ts`** (forma de hoy, `B/Wms.Application/Billing/Common/DTOs/BillingRecipientInput.cs`)

```ts
import { z } from "zod";
import { guidSchema, identificationTypeSchema } from "~/shared/contracts/api";

export const paymentMethodSchema = z.enum(["Cash", "BankTransfer", "Check", "CreditCard", "DebitCard", "Other"]);
export const paymentModeSchema = z.enum(["Immediate", "PendingBilling"]);
export const billingRecipientInputSchema = z.object({
  recipientMode: z.enum(["registered", "unregistered", "finalConsumer", "multiClient"]),
  customerId: guidSchema.nullable().optional(),
  unregisteredRecipient: z
    .object({ name: z.string().trim().min(3), idType: identificationTypeSchema, idNumber: z.string().trim().min(1) })
    .loose()
    .nullable()
    .optional(),
  paymentMethod: paymentMethodSchema,
  paymentMode: paymentModeSchema,
  totalAmount: z.number().min(0),
  referenceNumber: z.string().max(100).nullable().optional(), // AF-132: solo con otro método
  notes: z.string().nullable().optional(),                   // AF-132: el formulario compartido ya no lo envía
});
```

**`F/features/weighbridge/contracts/`** — esquemas del cambio (F03 los completa)

```ts
import { z } from "zod";
import { guidSchema, reasonSchema } from "~/shared/contracts/api";
import { entryReasonCategorySchema } from "~/features/entries/contracts/entry-reason";

// storage-entry.ts — cambios de C-F01-78 y C-F01-79 sobre la petición de hoy
export const storageEntryInitiateChangesSchema = z.object({
  cargoManifestNumber: z.string().trim().max(50).nullable(),
  primaryDocumentTypeId: guidSchema.nullable(),
  manifestNumber: z.string().trim().max(100).nullable(),
  manifestWeight: z.number().positive().nullable(),
  merchandiseWeight: z.number().positive().nullable(),
  inspectionDescription: z.string().trim().min(10).max(500).nullable(),
  carrierCompanyId: guidSchema,
  targetWarehouseStorageId: guidSchema.nullable(),
});
export const storageEntryInitiateResultChangesSchema = z.object({
  weighbridgeCycleId: guidSchema.nullable(), // nulo al registrar: el ciclo nace en el cobro (§8, nota de la fase 3)
  warehouseStorageEntryId: guidSchema,
  isDuplicateEntry: z.boolean(),
  warehouseStorageNumber: z.string(),
  isLateTruck: z.boolean(),
});
export const documentCandidateChangesSchema = z.object({ isOpen: z.boolean(), isMigrated: z.boolean() }); // sin closedAt ni closedByName

// weighing.ts — C-F01-80
export const weighingRecordResultChangesSchema = z.object({ merchandiseWeight: z.number().nullable() });

// output.ts — C-F01-109
export const outputInitiateChangesSchema = z.object({ exitId: guidSchema.nullable(), driverId: guidSchema, carrierCompanyId: guidSchema.nullable() });
export const outputInitiateResultChangesSchema = z.object({
  exitId: guidSchema, exitNumber: z.string(), exitCreated: z.boolean(), driverChangeNotified: z.boolean(),
});

// entry-edit.ts — C-F01-92 y C-F01-93 (completos)
import { depositEntrySchema, entryCorrectionCeSchema } from "~/features/foreign-trade/contracts/deposit-entry";
export const entryCorrectionScaleSchema = entryCorrectionCeSchema
  .omit({ merchandiseValue: true, usesCargoUnits: true, cargoUnits: true, manifestDate: true })
  .extend({ reason: reasonSchema.nullable() });
export const entryForEditSchema = depositEntrySchema.extend({
  entryLogId: guidSchema,
  licensePlate: z.string(),
  entryReasonId: guidSchema,
  entryReasonCategory: entryReasonCategorySchema.nullable(),
  dateTimeEntry: z.iso.datetime({ offset: true }),
  driver: z.object({ id: guidSchema, firstName: z.string(), lastName: z.string(), idType: z.string(), idNumber: z.string() }),
  vehicleCountry: z.string().nullable(),
  modalityCode: z.string(),
  warehouseStorageId: guidSchema,
  warehouseStorageNumber: z.string(),
  warehouseStorageStatus: z.enum(["Draft", "Confirmed", "Closed", "Cancelled"]),
  usesCargoUnits: z.boolean(),
  cargoUnits: z.array(z.object({ id: guidSchema, cargoUnitTypeId: guidSchema, identifier: z.string() })),
  canScaleEdit: z.boolean(),
});
```

**`F/features/foreign-trade/contracts/deposit-entry.ts`** (completo) y **`deposit.ts`** (cambio)

```ts
import { z } from "zod";
import { dateOnlySchema, dateTimeSchema, guidSchema } from "~/shared/contracts/api";

export const merchandiseWeightSourceSchema = z.enum(["Declared", "Reweigh", "Correction"]);
export const depositEntryProductSchema = z.object({
  id: guidSchema, warehouseStorageProductId: guidSchema, productId: guidSchema, productName: z.string().nullable(),
  packaging: z.string().nullable(), declaredQuantity: z.number().nullable(), netWeight: z.number().nullable(),
});
export const depositEntrySchema = z.object({
  id: guidSchema,
  weighbridgeCycleId: guidSchema.nullable(),
  isDuplicateEntry: z.boolean(),
  vehiclePlate: z.string().nullable(),
  ticketNumber: z.string().nullable(),
  carrierCompanyId: guidSchema.nullable(),
  carrierCompanyName: z.string().nullable(),
  documentTypeName: z.string().nullable(),
  documentNumber: z.string().nullable(),
  manifestNumber: z.string().nullable(),
  manifestWeight: z.number().nullable(),
  manifestDate: dateOnlySchema.nullable(),
  indicatorWeight: z.number().nullable(),
  tareWeight: z.number().nullable(),
  tareIsReal: z.boolean(),
  merchandiseWeight: z.number().nullable(),
  merchandiseWeightSource: merchandiseWeightSourceSchema.nullable(),
  manifestDifference: z.number().nullable(),
  merchandiseValue: z.number().nullable(),
  netWeight: z.number().nullable(),
  createdAt: dateTimeSchema,
  voidedAt: dateTimeSchema.nullable(),
  entryProducts: z.array(depositEntryProductSchema),
});
export const entryCorrectionCeSchema = z.object({
  vehicleCountry: z.string().nullable(),
  carrierCompanyId: guidSchema,
  driverId: guidSchema,
  primaryDocumentTypeId: guidSchema.nullable(),
  documentNumber: z.string().trim().max(50).nullable(),
  targetWarehouseStorageId: guidSchema.nullable().optional(),
  manifestNumber: z.string().trim().max(100).nullable(),
  manifestWeight: z.number().positive().nullable(),
  manifestDate: dateOnlySchema.nullable(),
  indicatorWeight: z.number().positive().nullable(),
  tareWeight: z.number().positive().nullable(),
  merchandiseWeight: z.number().positive().nullable(),
  products: z.array(z.object({
    warehouseStorageProductId: guidSchema.nullable(),
    productId: guidSchema,
    declaredQuantity: z.number().positive(),
    packaging: z.string().nullable(),
    packagingTypeId: guidSchema.nullable(),
  })),
  merchandiseValue: z.number().min(0).nullable(),
  usesCargoUnits: z.boolean(),
  cargoUnits: z.array(z.object({ id: guidSchema.nullable(), cargoUnitTypeId: guidSchema, identifier: z.string().trim().min(1).max(50) })),
  reason: z.string().trim().min(10).max(500).nullable(),
});

// deposit.ts — campos nuevos o cambiados del detalle (C-F01-86 a C-F01-88); F05 los une al detalle de hoy
export const trmSourceSchema = z.enum(["Weekly", "WeeklyFallback", "Manual"]);
export const depositDetailChangesSchema = z.object({
  cargoValue: z.number().nullable(),          // valor CPI
  cargoValueIsManual: z.boolean(),
  truckValueSum: z.number().nullable(),
  carriers: z.array(z.string()),
  merchandiseWeight: z.number().nullable(),
  dispatchedWeight: z.number().nullable(),
  weightBalance: z.number().nullable(),
  inspectionDescription: z.string().nullable(),
  trmSource: trmSourceSchema.nullable(),
});
```

**`F/features/exits/contracts/exit.ts`** (completo)

```ts
import { z } from "zod";
import { dateOnlySchema, dateTimeSchema, guidSchema, identificationTypeSchema, listQueryBaseSchema } from "~/shared/contracts/api";
import { billingRecipientInputSchema, paymentModeSchema } from "~/features/billing/contracts/billing-recipient";

export const exitTypeSchema = z.enum(["EntryTicket", "Global", "Deposit", "Consolidated"]);
export const exitKindSchema = z.enum(["EntryTicket", "Global", "ByDeposit"]);
export const exitStatusSchema = z.enum(["Draft", "Confirmed", "Completed", "Cancelled"]);
export const exitMissingSchema = z.enum(["Loading", "Weighing", "YardExit"]);

export const exitLineSchema = z.object({
  id: guidSchema, warehouseStorageId: guidSchema, warehouseStorageNumber: z.string(),
  warehouseStorageProductId: guidSchema, productName: z.string(), packaging: z.string().nullable(),
  cargoUnitId: guidSchema.nullable(), quantity: z.number().positive(),
  loadedQuantity: z.number().min(0).nullable(), allocatedWeight: z.number().nullable(),
});
export const exitGuideSchema = z.object({
  id: guidSchema, number: z.string(), issuedAt: dateTimeSchema, expirationDate: dateTimeSchema,
  signerType: z.enum(["Importer", "Driver"]), paymentMode: paymentModeSchema, invoiceId: guidSchema.nullable(),
  isCancelled: z.boolean(),
});
export const exitSchema = z.object({
  id: guidSchema,
  number: z.string(),
  type: exitTypeSchema,
  status: exitStatusSchema,
  missing: z.array(exitMissingSchema),
  origin: z.enum(["ForeignTrade", "Weighbridge"]),
  modalityCode: z.string().nullable(),
  createdAt: dateTimeSchema,
  vehicle: z.object({ id: guidSchema, licensePlate: z.string() }),
  driver: z.object({ id: guidSchema, fullName: z.string(), idType: identificationTypeSchema, idNumber: z.string() }),
  carrierCompany: z.object({ id: guidSchema, name: z.string() }).nullable(),
  destination: z.object({ cityId: guidSchema.nullable(), cityName: z.string().nullable(), address: z.string().nullable() }),
  customerOrder: z
    .object({ number: z.string(), issuerId: guidSchema, issuerName: z.string(), date: dateOnlySchema, fileUrl: z.string().nullable() })
    .nullable(),
  observations: z.string().nullable(),
  deposits: z.array(z.object({ warehouseStorageId: guidSchema, number: z.string(), customerName: z.string().nullable() })),
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
});
export const exitListItemSchema = z.object({
  id: guidSchema, number: z.string(), createdAt: dateTimeSchema, type: exitTypeSchema, status: exitStatusSchema,
  missing: z.array(exitMissingSchema), depositNumbers: z.array(z.string()), licensePlates: z.array(z.string()),
  ticketNumbers: z.array(z.string()), guideNumber: z.string().nullable(), confirmedAt: dateTimeSchema.nullable(),
  dispatchedWeight: z.number().nullable(), destinationCityName: z.string().nullable(),
});
export const exitListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["number", "createdAt", "type", "status", "confirmedAt"]).optional(),
  number: z.string().optional(), createdAtFrom: dateOnlySchema.optional(), createdAtTo: dateOnlySchema.optional(),
  type: z.array(exitTypeSchema).optional(), status: z.array(exitStatusSchema).optional(), missing: z.array(exitMissingSchema).optional(),
  depositNumber: z.string().optional(), licensePlate: z.string().optional(), guideNumber: z.string().optional(),
  warehouseStorageId: guidSchema.optional(),
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
    customerOrder: z.object({ number: z.string().trim().min(1).max(50), issuerId: guidSchema, date: dateOnlySchema, fileUrl: z.string().nullable() }).nullable(),
    observations: z.string().max(500).nullable(),
  })
  .refine((v) => v.kind === "ByDeposit" || v.warehouseStorageIds.length === 1, {
    message: "Una salida por tiquete o global es de un solo depósito.", path: ["warehouseStorageIds"],
  })
  .refine((v) => v.kind !== "EntryTicket" || v.ticketEntryIds.length === 1, {
    message: "Una salida por tiquete lleva un solo tiquete; la global, dos o más.", path: ["ticketEntryIds"],
  })
  .refine((v) => v.kind !== "Global" || v.ticketEntryIds.length >= 2, {
    message: "Una salida por tiquete lleva un solo tiquete; la global, dos o más.", path: ["ticketEntryIds"],
  });
export const exitConfirmSchema = z.object({
  departureDatetime: dateTimeSchema,
  observations: z.string().max(500).nullable(),
  billing: billingRecipientInputSchema.nullable(), // null solo en inspección
});
export const exitLoadingSchema = z.object({
  lines: z.array(z.object({ lineId: guidSchema, loadedQuantity: z.number().min(0) })).min(1),
  crewId: guidSchema.nullable(),
  signatureDriver: z.string().min(1, "La firma del conductor es obligatoria."),
  observations: z.string().max(250).nullable(),
  photos: z.array(z.object({ fileName: z.string(), contentType: z.string(), base64: z.string() })),
});
export const exitYardExitSchema = z.object({ observations: z.string().max(250).nullable() });
export const guidePaymentModeSchema = z.object({ paymentMode: paymentModeSchema });
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
export type Exit = z.infer<typeof exitSchema>;
```

---

## 3. Archivos que se tocan

Rutas y líneas de la base `529bda7`. El ejecutor confirma con grep (§0.4). «Se borra» va con `rm` y en el mismo commit que el código que deja de usarlo.

### 3.1 Backend

| Fase | Archivo (base) | Qué se hace |
| --- | --- | --- |
| 1 | `B/Wms.Common/Wrappers/QueryParametersBase.cs:3-33` | Suma `SortField` y `SortOrder` (D9) |
| 1 | `B/Wms.Common/Wrappers/ListSorting.cs` | **Nuevo**: lista blanca, orden y desempate por `Id` (D9) |
| 1 | `B/Wms.Infrastructure/Persistence/AppDbContext.cs` | `HasPostgresExtension("unaccent")`; `DbSet` de `FieldPrefix` y `WeeklyExchangeRate` |
| 1 | Handlers de los listados de C-F01-01, -10, -15, -21, -25, -37, -47, -52, -56, -59, -68 (por ejemplo `B/Wms.Application/Logistics/Drivers/Queries/GetAllDrivers/GetAllDriversHandler.cs:21-27`) | Filtros con `unaccent` y orden con `ListSorting` |
| 1 | `B/Wms.Domain/Security/WmsPolicyRoles.cs:9-91` | Políticas nuevas y `EntryCorrectionAccess` (§2.0, D11, D13) |
| 1 | `B/Wms.Api/Controllers/v1/EntryReasonController.cs:21-80`, `DriverController.cs:19-58`, `VehicleController.cs`, `StakeholderController.cs`, `ProductController.cs:20-50`, `ServiceController.cs`, `AdministrationController.cs`, `CitiesController.cs`, `CrewsController.cs`, `EntryLogCorrectionController.cs:17` | Políticas por endpoint (§2.2.1) |
| 1 | `B/Wms.Api/Controllers/v1/WarehouseController.cs:860-905` → `WarehouseLocationsController.cs` (**nuevo**) | Las cuatro acciones de ubicaciones, misma ruta, sin la política de la clase (D11) |
| 1 | `B/Wms.Api/Controllers/v1/StakeholderController.cs` | `POST stakeholder/quick` (C-F01-141) con el comando de hoy de `weighbridge/stakeholders/quick`, que pasa a `Wms.Application/Stakeholders/Commands/QuickCreateStakeholder/` |
| 1 | `B/Wms.Domain/Entities/Logistics/EntryReason.cs:5-36`; `B/Wms.Domain/Enums/EntryReasonCategory.cs` (**nuevo**) | `Category` y su regla (D12) |
| 1 | `B/Wms.Infrastructure/Persistence/SeedDataExtensions.cs:290-308` | Categoría de los motivos sembrados (M22) |
| 1 | `B/Wms.Application/Logistics/EntryLogs/Commands/CorrectEntryLog/` | Regla de categoría y de depósito confirmado (D13) |
| 1 | `B/Wms.Domain/Entities/Administration/FieldPrefix.cs`, `B/Wms.Domain/Enums/PrefixedField.cs`, `B/Wms.Domain/Entities/Administration/WeeklyExchangeRate.cs` (**nuevos**), con su configuración EF, semilla de prefijos, comandos, consultas y `SettingsController` (**nuevo**, ruta `settings`) | D14, D15 |
| 1 | `B/Wms.Application/ForeignTrade/Common/Services/ReleaseFobService.cs:56-82` | Sin DIAN: la tasa viene en la petición (D15, D43) |
| 1 | `B/Wms.Domain/Services/IDianTrmService.cs`, `B/Wms.Infrastructure/External/DianTrmService.cs`, `DianTrmOptions.cs`, `B/Wms.Api/Controllers/v1/SystemController.cs:18-21` | **Se borran** (C-F01-14). `SystemController` se borra si queda vacío |
| 1 | `B/Wms.Infrastructure/Persistence/Configurations/Logistics/DriverConfiguration.cs:24` | Índice no único (D16) |
| 1 | `B/Wms.Application/Logistics/Drivers/Commands/` y la consulta de `weighbridge/drivers/by-document` (`WeighbridgeCatalogController.cs:62`) | Regla del nombre; lista (D16, C-F01-20) |
| 1 | `B/Wms.Application/Logistics/Drivers/Queries/GetDriverRecentEntries/` (**nuevo**) | C-F01-19 |
| 2 | `B/Wms.Domain/Entities/Product/Product.cs`; `B/Wms.Domain/Entities/Administration/UnitMeasure.cs`; `B/Wms.Infrastructure/Persistence/Configurations/Administration/UnitMeasureConfiguration.cs`; `B/Wms.Application/Administration/UnitMeasures/` | Sale la unidad; **se borran** la entidad, su configuración y su carpeta (D18) |
| 2 | `B/Wms.Api/Controllers/v1/AdministrationController.cs` (unidades de medida) | **Se borran** las cuatro acciones (C-F01-73 a C-F01-76) |
| 2 | Los 115 archivos de `Wms.Api`, `Wms.Application`, `Wms.Domain` e `Wms.Infrastructure` y los 46 de pruebas que citan `UnitMeasure` (lista con `grep -rl UnitMeasure`) | Sin unidad: DTO (R-UOM), PDF del depósito, guía y reportes |
| 2 | `B/Wms.Application/Billing/Calculators/PerUomFormulaCalculator.cs:37-43`; `B/Wms.Infrastructure/Persistence/SeedDataExtensions.cs:424-431` | `PER_UOM` sin `uom` (D19) |
| 2 | `B/Wms.Application/Administration/LegacyImport/Importers/ProductsImporter.cs:89`, `DepositsImporter.cs:199-221`, `:302` | Sin unidad (D18, D44) |
| 3 | `B/Wms.Application/Weighbridge/Commands/Storage/Initiate/InitiateStorageWeighingCommand.cs`, su validador (`InitiateStorageWeighingValidator.cs:24-26`, `:102-108`, `:133-141`) y su handler (`InitiateStorageWeighingHandler.cs:320-350`, `:410`, `:962-968`); `Register` igual | Entrada por documento, pesos, manifiesto, inspección, transportadora, sin valor ni unidades (D20 a D28) |
| 3 | `B/Wms.Domain/Entities/Weighbridge/WeighbridgeCycle.cs:206-230` | `IsDuplicateEntry`; la regla R5 pasa a la entrada duplicada (D5) |
| 3 | `B/Wms.Domain/Entities/Warehouse/WarehouseStorageEntry.cs:9-180` | `MerchandiseWeight`, `MerchandiseWeightSource`, `CarrierCompanyId`, `MerchandiseValue`, `ManifestDate` (D21, D26, D28) |
| 3 | `B/Wms.Domain/Entities/Warehouse/WarehouseStorage.cs:15`, `:441-459` | `CargoValueIsManual`, `InspectionDescription`; `CargoValue` como CPI automático o manual (D23, D28) |
| 3 | `B/Wms.Application/Weighbridge/Common/Services/ManifestDeducedWeights.cs`, `WeighingTotals.cs:72` | Pesos con `MerchandiseWeight` (D21) |
| 3 | `B/Wms.Application/Weighbridge/Common/Services/ReceptionArrivalRules.cs`, `ExitLoadingRules.cs` | **Se borran** con sus llamadas y pruebas (D25) |
| 3 | `B/Wms.Domain/Entities/Services/ServiceRecord.cs:71-74`, `:319-339`; `B/Wms.Application/Weighbridge/Common/Services/StorageDocumentLookup.cs:35`, `:85-91`, `:125-126`, `:151-152`, `:180`; `B/Wms.Api/Controllers/v1/ForeignTradeController.cs:442` | Sin cierre de camiones (D27) |
| 3 | `B/Wms.Application/ForeignTrade/Common/Services/DepositConfirmationRequirements.cs:66-128` | Manifiesto solo con carta porte (D22) |
| 3 | `B/Wms.Application/ForeignTrade/Common/Services/DepositStakeholderRoles.cs:13`, `GuideCarrierText.cs`, `B/Wms.Application/ForeignTrade/Common/Queries/DepositSearchQueryExtensions.cs:16`, `:87` | Transportadora por entrada (D26) |
| 3 | Notificación «Camión tardío en depósito confirmado» en `B/Wms.Api/Services/NotificationOrchestrator.cs` | D27, D45 |
| 4 | `B/Wms.Application/Weighbridge/Commands/Storage/CorrectEntry/` y `B/Wms.Application/ForeignTrade/Commands/CorrectEntry/` (**nuevos**), con `EntryCorrectionService` (**nuevo**, en `B/Wms.Application/Weighbridge/Common/Services/`) | C-F01-90, C-F01-92, C-F01-93 (D29 a D32) |
| 4 | `B/Wms.Api/Controllers/v1/DepositCompletionController.cs` (`PATCH …/entries/{entryId}/manifest`) | **Se borra** la acción (C-F01-91) |
| 5 | `B/Wms.Domain/Entities/Warehouse/GoodsExit.cs`, `GoodsExitLine.cs`, `GoodsExitTicket.cs`, `GoodsExitPhoto.cs`, `B/Wms.Domain/Enums/ExitType.cs`, `ExitStatus.cs`, `ExitOrigin.cs` (**nuevos**), con sus configuraciones EF | D2, D33 |
| 5 | `B/Wms.Domain/Entities/Warehouse/LoadingOrder.cs`, `LoadingOrderItem.cs`, `LoadingOrderPhoto.cs`, `B/Wms.Domain/Enums/LoadingOrdersStatus.cs`, sus configuraciones y los comandos y consultas de `B/Wms.Application/ForeignTrade/Commands/*LoadingOrder*`, `*DispatchGuide*`, `B/Wms.Application/Warehouse/Commands/LoadingOrder/` | **Se borran** (D2) |
| 5 | `B/Wms.Domain/Entities/Warehouse/WarehouseReserve.cs:10-27`, `DispatchGuide.cs:16`, `:19`, `:39`, `DispatchGuideLine.cs:14` | Apuntan a `GoodsExit` y `GoodsExitLine`; sin sello (D35, D36) |
| 5 | `B/Wms.Domain/Enums/SourceTypeMovements.cs`, `DocumentSequenceType.cs`; `B/Wms.Domain/Services/DocumentNumberFormat.cs:23` | `GoodsExit`, `GoodsExitReversal`; serie «SM» (D1, D36) |
| 5 | `B/Wms.Application/Exits/` (**nueva**: comandos, consultas, `ExitStateRules` puro, `ExitAvailability` puro, `DispatchedWeightAllocator` puro) y `B/Wms.Api/Controllers/v1/ExitsController.cs` (**nuevo**, ruta `exits`) | C-F01-94 a C-F01-108 (D33 a D39) |
| 5 | `B/Wms.Application/Weighbridge/Commands/Output/` (initiate, pagos) y `B/Wms.Api/Controllers/v1/WeighbridgeOutputSharingController.cs`, `LoadingOrderExitController.cs`, `LoadingOrderCorrectionsController.cs` | Salida de báscula con `GoodsExit`; **se borran** los tres controladores (C-F01-109 a C-F01-138) |
| 5 | `B/Wms.Domain/Entities/Services/ServiceRecord.cs:20`, `:25`, `:30` | `LoadingOrderId` → `GoodsExitId`; salen `AnchorWeighbridgeCycleId` y `SourceEntryCycleId` (D37) |
| 5 | `B/Wms.Application/Billing/Common/Services/StorageBillableQuantity.cs:93-96` | Por guía (D40) |
| 5 | `B/Wms.Application/ForeignTrade/Common/Services/DispatchGuidePdfService.cs:432`, la verificación pública y los reportes de R-SAL | Leen la salida (D46, R-SAL) |
| 6 | `B/Wms.Application/Billing/Calculators/WeightThresholdFormulaCalculator.cs:8-10`, `:29` y el contexto de fórmulas | Peso de mercancía (D41) |
| 6 | `B/Wms.Application/Billing/Common/Services/StorageBillingService.cs`, `InvoiceTrmGuard.cs`, `StorageRecalculationTrigger.cs`; `B/Wms.Domain/Entities/Warehouse/WarehouseStorage.cs:39-67`, `:234-283`; `B/Wms.Domain/Enums/TrmSource.cs` | Tasa de la semana (D42, D43) |
| 6 | `B/Wms.Api/Controllers/v1/BillingController.cs:660-687`; `B/Wms.Application/Billing/Commands/RegisterManualTrm/` | **Se borran** (C-F01-140) |
| 6 | `B/Wms.Application/Administration/LegacyImport/Importers/DepositsImporter.cs:258` | Tasa del legacy con origen `Manual` (D7, D44) |

### 3.2 Frontend y docs

La parte 1 no toca el frontend. I-01 lo cubre en §13. En docs, cada fase actualiza su fila de §8, la matriz y `D/planes/README.md`.

---

## 4. Esquema y migraciones

Cuatro migraciones, generadas y aplicadas por el agente con `dotnet ef` en la base local (M6). Antes de generar, `git fetch` y lo último de `fase-2` (`PM/` §5.3). Si una migración no sale como se espera, se corrige el modelo y se regenera.

| Fase | Migración | Contenido esperado, en orden |
| --- | --- | --- |
| 1 | `AddCatalogSortAndPrefixes` | Extensión `unaccent`. `entry_reasons.category` (texto, nulo) y datos de la semilla según M22. Tabla `field_prefixes` (`id`, `field` texto único, `prefix` texto(20) nulo, `created_at`, `updated_at`, `updated_by_id` nulo) con 3 filas sembradas. Tabla `weekly_exchange_rates` (`id`, `from_date` date, `to_date` date, `rate` numeric(18,2), `created_by_id`, `updated_by_id` nulo, `created_at`, `updated_at`), índice por `from_date`. `idx_driver_id` pasa a no único |
| 2 | `RemoveUnitMeasure` | Sale `products.unit_measure_id` con su FK e índice. Sale la tabla `unit_measures` con su semilla. Actualiza el `parameters_schema` sembrado de `PER_UOM` (sin `uom`, rótulo nuevo). Sin `HasDefaultValue` en columnas nuevas de tablas con `HasData` (`D/contexto/convenciones-tecnicas.md` §5) |
| 3 | `EntryPerDocument` | `weighbridge_cycles.is_duplicate_entry` (bool, no nulo). En `warehouse_storage_entries`: `merchandise_weight` numeric nulo, `merchandise_weight_source` texto nulo, `carrier_company_id` uuid nulo con FK a `stakeholders` e índice, `merchandise_value` numeric nulo, `manifest_date` date nulo. En `warehouse_storages`: `cargo_value_is_manual` bool no nulo, `inspection_description` texto(500) nulo. Salen `service_records.truck_entries_closed_at` y `truck_entries_closed_by_id` |
| 4 | Ninguna | La edición del ingreso usa las columnas de la fase 3. Si `has-pending-model-changes` no sale limpio, el ejecutor se detiene y pregunta |
| 5 | `ReplaceLoadingOrderWithGoodsExit` | Tablas `goods_exits`, `goods_exit_lines`, `goods_exit_tickets` y `goods_exit_photos` con sus FK e índices (número único por año; índice por estado; índice por vehículo). `warehouse_reserves.loading_order_id` y `loading_order_item_id` → `goods_exit_id` y `goods_exit_line_id`. `dispatch_guides.loading_order_id` → `goods_exit_id`; sale `dispatch_guides.seal_number`. `dispatch_guide_lines.loading_order_item_id` → `goods_exit_line_id`. `service_records.loading_order_id` → `goods_exit_id`; salen `anchor_weighbridge_cycle_id` y `source_entry_cycle_id`. Salen las tablas `loading_orders`, `loading_order_items` y `loading_order_photos`. Las columnas de texto de enums cambian de valores sin conversión (bases recreadas, M17) |
| 6 | Ninguna | `TrmSource` se guarda como texto: cambiar sus valores no altera el esquema. Igual que la fase 4 si no sale limpio |

Las bases locales se recrean (`DEC-006`): ninguna migración convierte datos. Staging no se toca; lo recrea el despliegue final (M17, M25).

---

## 5. Pruebas

| Proyecto | Prueba (nueva o ajustada) | Escenario |
| --- | --- | --- |
| `Wms.Tests` | `ListSortingTests` (nueva) | Lista blanca, campo desconocido (400), orden por defecto, desempate por Id |
| `Wms.Tests` | `EntryReasonTests` (nueva) | Categoría obligatoria con pesaje y nula sin él |
| `Wms.Tests` | `WeeklyExchangeRateRulesTests` (nueva) | Rango de 1 a 7 días, superposición, consulta por fecha con respaldo y sin tasa |
| `Wms.Tests` | `DriverNameNormalizerTests` (nueva) | Mismo documento y nombre con tildes, mayúsculas o espacios: duplicado |
| `Wms.Tests` | `PerUomFormulaCalculatorTests` (ajustada) | Tarifa × cantidad; un `uom` guardado se ignora |
| `Wms.Tests` | `MerchandiseWeightRulesTests` (nueva) | Declarada, repesaje, corrección; tara calculada; mercancía > indicador |
| `Wms.Tests` | `ConfirmationRequirementsTests` (ajustada) | Manifiesto solo con carta porte |
| `Wms.Tests` | `ExitStateRulesTests` (nueva) | Transiciones de D34, lo que falta por tipo, completada inmutable |
| `Wms.Tests` | `ExitAvailabilityTests` (nueva) | Disponible y nacionalizado con reservas de otras salidas |
| `Wms.Tests` | `DispatchedWeightAllocatorTests` (nueva) | Prorrateo por peso documental, respaldo por cantidad y redondeo (D4) |
| `Wms.Tests` | `StorageBillableQuantityTests` (ajustada) | Salidas `GoodsExit` y reversiones (D40) |
| `Wms.Tests` | `WeightThresholdFormulaCalculatorTests` (ajustada) | Peso de mercancía; entradas sin peso cuentan 0 (D41) |
| `Wms.Tests` | `StorageTrmResolverTests` (nueva) | Tasa propia, semanal, respaldo y pendiente (D42) |
| `Wms.Tests` | `ReceptionArrivalRulesTests`, `ExitLoadingRulesTests`, las de `LoadingOrder` | **Se borran** con su regla |
| `Wms.IntegrationTests` | Una por endpoint del contrato (`PM/` §6.1): respuesta y mensajes de error de C-F01-01 a C-F01-141 (los retirados: 404) | Por fase |
| `Wms.IntegrationTests` | `CatalogPoliciesTests` (nueva) | Cada política de §2.0 con un usuario de cada rol: 200 o 403 según la ficha; ningún rol pierde lo de hoy (`DEC-005`) |
| `Wms.IntegrationTests` | `EntryPerDocumentTests` (nueva) | Dos entradas del mismo camión, cobro $0 de la duplicada, mismo depósito 409, camión tardío con aviso |
| `Wms.IntegrationTests` | `EntryCorrectionTests` (nueva) | Báscula en Borrador y 409 en Confirmado; CE con levante y salida; unidades de carga; recálculo |
| `Wms.IntegrationTests` | `GoodsExitFlowTests` (nueva) | Los cuatro tipos de punta a punta, inspección sin guía, reabrir, cancelar, reservas, cierre y reapertura del depósito |
| `Wms.IntegrationTests` | `WeeklyRateBillingTests` (nueva, fase 6) | Factura con tasa semanal, respaldo con advertencia, recálculo al registrar la tasa, migrado con tasa propia |
| `Wms.IntegrationTests` | *Helpers* `OperationalData`, `WeighbridgeScenario`, `BillingScenario`, `ConfirmDepositAsync` | Sin unidades de carga en báscula, sin cierre de camiones, salidas en lugar de órdenes |

Cada fase informa el número de pruebas antes y después (`PM/` §6).

---

## 6. Casos QA

F01 no tiene pantallas: sus casos se verifican **por API** (Swagger o `curl` con el token de un usuario de prueba de cada rol, en la base local), en la fase que los construye. Los de I-01, en el navegador, están en §13.3. Al cerrar I-01 se copian a `D/qa/` con su ID (`PM/` §5.1). Los usuarios de prueba por rol están en `Frontend/wms/README.md`; sus contraseñas no se copian.

| ID | Regla de origen | Precondición | Pasos | Resultado esperado | Verificación |
| --- | --- | --- | --- | --- | --- |
| QA2-F01-001 | C-F01-00; D9 | Conductores «José Pérez» y «Jose Perez» | `GET drivers?name=jose perez&sortField=lastName&sortOrder=desc` | Los dos, ordenados por apellido descendente | API |
| QA2-F01-002 | C-F01-00 | — | `GET drivers?sortField=password` | 400 «No se puede ordenar por «password».» | API |
| QA2-F01-003 | C-F01-00 | — | `GET administration/audit-logs?createdAtFrom=2026-11-20&createdAtTo=2026-11-19` | 400 «La fecha inicial no puede ser posterior a la final.» | API |
| QA2-F01-004 | AF-08, M22; D12 | Base recién migrada | `GET entry-reasons/list` | Los dos «Descargue» con `Entry`, los dos «Cargue» con `Exit`, «Solo Bascula» con `WeighingOnly`, «Solo bodega» y «Otro» con `null` | API |
| QA2-F01-005 | AF-08; D12 | Usuario CE | `POST entry-reasons` con `requiresWeighing: true` sin categoría | 400 «Elija la categoría del motivo: Ingreso, Salida o Solo báscula.» | API |
| QA2-F01-006 | AF-127; D11 | Usuarios CE y Báscula | `POST entry-reasons` válido con cada uno | CE: 201; Báscula: 403 | API |
| QA2-F01-007 | AF-08; D13 | Camión con ciclo de ingreso guardado; usuario Báscula | `PUT entry-logs/{id}/correction` con un motivo de categoría `Exit` | 409 «El camión {placa} ya tiene un registro de Ingreso: …anule el pesaje y regístrelo de nuevo.» | API |
| QA2-F01-008 | AF-08; D13 | Camión sin depósito confirmado; usuario Báscula | Corregir la placa con motivo | 200 y el cambio en `changes[]` | API |
| QA2-F01-009 | AF-79; D14 | Usuario CE | `PUT settings/prefixes/ReleaseNumber` con `"4820260"`; luego `GET settings/prefixes` | El prefijo guardado, con usuario y fecha | API |
| QA2-F01-010 | AF-128; D11 | Usuario Facturación | `PUT settings/prefixes/ReleaseNumber` | 403 | API |
| QA2-F01-011 | AF-85, AF-86; D15 | Tasa del 16 al 22/11/2026 | `POST settings/exchange-rates` del 20 al 26/11/2026 | 409 «Las fechas se cruzan con la tasa del 16/11/2026 al 22/11/2026.» | API |
| QA2-F01-012 | AF-136; D15 | Solo la tasa del 09 al 15/11/2026 | `GET settings/exchange-rates/for-date?date=2026-11-18` | `isFallback: true`, la tasa del 09 al 15 y el aviso | API |
| QA2-F01-013 | AF-85; D15 | — | `GET system/dian-trm/today` | 404 | API |
| QA2-F01-014 | AF-18; D16 | Conductor «Conductor 1», CC 1000001 | `POST drivers` con CC 1000001 y nombre «Conductor Dos»; luego con «conductor 1» | Primero 201; después 409 «Ya existe el conductor Conductor 1 con Cc 1000001.» | API |
| QA2-F01-015 | AF-18; D16 | Dos conductores con CC 1000001 | `GET weighbridge/drivers/by-document?idType=Cc&idNumber=1000001` | Lista con los dos | API |
| QA2-F01-016 | P-TR-03; D17 | Conductor con tres ingresos | `GET drivers/{id}/recent-entries?take=2` | Los dos más recientes, con placa y tiquete | API |
| QA2-F01-017 | AF-54; C-F01-141 | Usuario Bodega | `POST stakeholder/quick` con rol `CUSTOMER` | 201 `Created`; repetido con otro rol: 200 `RoleAdded`; con el mismo rol: 409 | API |
| QA2-F01-018 | AF-127; D11 | Usuario Facturación | `POST vehicles`, `POST product`, `PATCH administration/crews/{id}` | 201, 201 y 200 | API |
| QA2-F01-019 | `DEC-005`; D11 | Usuarios Vigilancia, Báscula y Bodega | Crear conductor (los tres), vehículo (Vigilancia y Báscula), tipo de embalaje (los tres) | Igual que hoy: ninguno pierde un permiso | API |
| QA2-F01-020 | M21, AF-22; D18 | Fase 2 cerrada | `GET product/{id}`; `GET administration/unit-measures` | Producto sin campos de unidad; 404 | API |
| QA2-F01-021 | M21; D19 | Regla `PER_UOM` con tarifa 100; depósito con 40 sacos | Recalcular la factura del período | Línea de 4.000 (tarifa × cantidad), sin error por `uom` | API |
| QA2-F01-022 | AF-44, AF-47; D20 | Camión ABC123 con motivo de ingreso | `storage/initiate` con CP-001 y luego con CP-002, mismo `entryLogId` | Dos ciclos; el segundo `isDuplicateEntry: true`; su cobro sale en $0 | API |
| QA2-F01-023 | AF-46; D20 | El caso anterior | `storage/initiate` otra vez con CP-001 al mismo depósito | 409 «El camión ABC123 ya tiene una entrada en el depósito {N}.» | API |
| QA2-F01-024 | AF-12; D22 | — | `storage/initiate` con factura comercial sin manifiesto; luego con carta porte sin manifiesto | 201; después 400 «El número y el peso del manifiesto son obligatorios con carta porte.» | API |
| QA2-F01-025 | AF-17; D23 | — | `storage/initiate` de inspección sin documento ni productos y con descripción | 201 y depósito nuevo con la descripción; sin descripción: 400 | API |
| QA2-F01-026 | AF-09, AF-41; D21 | Entrada con indicador 30.000 y mercancía 18.000 | `GET …/entries`; registrar tara real 12.500; leer de nuevo | Tara calculada 12.000; después mercancía 17.500 con origen `Reweigh` | API |
| QA2-F01-027 | AF-14; D25 | Entrada sin recepción en Bodega | Registrar el segundo pesaje | 200, sin el 409 de llegada | API |
| QA2-F01-028 | AF-21; D24 | Vehículo sin tipo | `storage/register` sin tipo de vehículo | 201 | API |
| QA2-F01-029 | AF-101; D26 | — | `PUT foreign-trade/warehouse-storages/{id}/stakeholders` con `TRANSPORT_COMPANY` | 400 «La empresa de transporte va en cada entrada, no en el depósito.» | API |
| QA2-F01-030 | AF-84, AF-95; D27 | Depósito confirmado | `POST …/close-truck-entries`; luego un camión nuevo con su documento | 404; el camión entra, `isLateTruck: true`, aviso «Camión tardío en depósito confirmado» a CE, factura recalculada | API |
| QA2-F01-031 | AF-94; D28 | Depósito con dos entradas de 15.000 y 5.629,20 | Leer el detalle | `cargoValue` 20.629,20, `cargoValueIsManual: false` | API |
| QA2-F01-032 | AF-26; D30 | Depósito confirmado; usuario Báscula | `PUT weighbridge/entries/{id}` | 409 «El depósito {N} ya está confirmado: la corrección la hace Comercio Exterior.» | API |
| QA2-F01-033 | AF-26; D30 | Depósito confirmado con levante de 300 de 760; usuario CE | `PUT foreign-trade/entries/{id}` con 250 | 409 «Cebolla: la cantidad no puede quedar en 250; ya tiene 300 levantado y 0 despachado.» | API |
| QA2-F01-034 | AF-27; D31 | Depósito sin levantes ni salidas | `PUT foreign-trade/entries/{id}` con `usesCargoUnits: true` y dos contenedores | 200 con las unidades; con un levante: 409 | API |
| QA2-F01-035 | AF-26, `DEC-022`; D32 | Depósito confirmado con factura del período en Borrador | Corregir la cantidad por CE | La factura en Borrador cambia; la corrección queda en `audit_logs` | API |
| QA2-F01-036 | AF-28, AF-32; D33 | Dos depósitos de importación nacionalizados | `POST exits` con `kind: ByDeposit` y los dos | 201, número `2026SM00001`, tipo `Consolidated`, estado `Draft` | API |
| QA2-F01-037 | M24; D35 | Producto con stock 760; un Borrador con 500 | `POST exits` con 300 del mismo producto | 409 «Cebolla del depósito {N}: disponible 260, pidió 300.» | API |
| QA2-F01-038 | AF-36, AF-68; D36 | Borrador por depósito completo | `POST exits/{id}/confirm` con el cobro | Guía `2026S…`, stock baja (movimiento `GoodsExit`), `missing: [Loading, Weighing]` | API |
| QA2-F01-039 | AF-88; D36 | Salida de inspección | Confirmar sin cobro | Sin guía; stock baja; `missing` según el tipo | API |
| QA2-F01-040 | AF-90; D34 | Salida confirmada y cargada, sin pesaje | `POST exits/{id}/reopen` con motivo | Borrador, guía anulada en `guideHistory`, stock devuelto, el cargue se conserva | API |
| QA2-F01-041 | AF-90; D34 | Salida completada | `POST exits/{id}/reopen` | 409 «La salida {N} está completada: ya no se modifica.» | API |
| QA2-F01-042 | AF-30, AF-37; D37 | Camión con motivo de salida y sin salida previa | `POST weighbridge/output/initiate` sin `exitId` | Salida en Borrador con placa, conductor y transportadora; `exitCreated: true` | API |
| QA2-F01-043 | AF-34; D37 | Salida confirmada con guía; otro conductor en báscula | `output/initiate` con `exitId` y otro `driverId` | La salida conserva su conductor; aviso a CE; `driverChangeNotified: true` | API |
| QA2-F01-044 | AF-29; D37 | Salida global confirmada | `output/initiate` con su `exitId` | 400 «La salida {N} es por tiquete o global: no pasa por báscula.» | API |
| QA2-F01-045 | AF-31, AF-35; D38 | Salida por depósito confirmada | Cargue primero y pesaje después; y al revés en otra | Las dos quedan `Completed` solo con los dos | API |
| QA2-F01-046 | AF-70; D38 | Producto con 200 en A-14 (más reciente) y 300 en A-15 | Cargue de 250 | Libera 200 de A-14 y 50 de A-15; sin pedir ubicación ni sello | API |
| QA2-F01-047 | AF-66; D38 | Salida por tiquete confirmada | `POST exits/{id}/yard-exit` | `Completed`, con fecha y hora del servidor | API |
| QA2-F01-048 | AF-42; D4, D39 | Consolidada de dos depósitos (peso documental 6.000 y 3.000), neto 8.700 | Completar el pesaje | `dispatchedWeight` 8.700; líneas con 5.800 y 2.900 | API |
| QA2-F01-049 | M15; D40 | Período abierto, salida confirmada de 100 y reabierta | Recalcular la factura | La cantidad facturable no cuenta la salida reabierta | API |
| QA2-F01-050 | — | Fase 5 cerrada | `GET foreign-trade/loading-orders`, `POST warehouse/loading-orders/{id}/execute` | 404 | API |
| QA2-F01-051 | AF-113; D41 | Depósito con dos entradas, una sin peso de mercancía | Recalcular la factura con fórmula por peso | Cobra sobre la suma de mercancía; advertencia «1 camiones sin peso de mercancía» | API |
| QA2-F01-052 | AF-85; D42 | Tasa del 16 al 22/11 = 4.050; depósito USD con ingreso el 18/11 | Abrir el período | Factura con TRM 4.050, `trmSource: Weekly` | API |
| QA2-F01-053 | AF-136; D42 | Sin tasa de la semana del ingreso; la anterior = 4.080 | Abrir el período; luego registrar la tasa de esa semana | Primero 4.080 con advertencia y aviso a CE y Facturación; después la factura en Borrador recalculada | API |
| QA2-F01-054 | D7 | Depósito migrado con `trm_ingreso` 3.900 | Recalcular su factura | Usa 3.900 (`Manual`), sin advertencia | API |

---

## 7. Transición de datos

Lo que le toca a F01 de `PM/` §7.2. Las bases locales se recrean; staging se recrea en el despliegue final (M17, M25); nada se convierte.

| Dato | Qué se hace | Fase | Decisión |
| --- | --- | --- | --- |
| Unidad de medida | La migración quita la columna del producto y el catálogo; las semillas y el esquema de `PER_UOM` pierden `uom`; el importador deja de buscar la unidad | 2 | M21; D18, D19 |
| Motivos de ingreso | La semilla agrega la categoría de M22; con el reinicio del despliegue final no quedan motivos creados a mano | 1 | M22; D12 |
| Órdenes de cargue, guías ligadas a órdenes, cierre de camiones | El modelo nuevo no los tiene; no se convierten | 3 y 5 | M18; D2, D27 |
| Valor del depósito | El importador guarda el valor del legacy como CPI manual (`CargoValueIsManual = true`); el precio por camión queda vacío (los migrados no tienen entradas) | 3 | M19; D28, D44 |
| Transportadora del depósito | El importador no guarda transportadora propia | 3 | D26 |
| Tasa de cambio | La tabla semanal arranca vacía; la de la semana de arranque se carga antes del despliegue final (`PM/` §7.3). Los migrados conservan su `trm_ingreso` con origen `Manual` | 1 y 6 | AF-85, AF-86, AF-136; D7 |
| Prefijos | Se siembran sin valor; los valores del cliente se cargan antes del despliegue final (`PM/` §7.3, pendiente 4 del cliente) | 1 | AF-79; D14 |

**Importador del legacy** (`B/Wms.Application/Administration/LegacyImport/`): se adapta en la fase que cambia cada entidad (D44) y se prueba con su prueba de integración de hoy. Antes de cerrar la fase 6, el ejecutor corre la importación completa en una base local recreada con los CSV de ensayo de hoy (los que usa la suite) y compara los conteos con los de antes de F01: productos, depósitos, levantes y saldos iguales; sin unidades de medida; motivos con categoría. Los CSV con datos reales no se copian a git (`DEC-007`).

---

## 8. Fases por parte

Una a la vez, en orden (`D/procesos/flujo-de-trabajo-agentes.md` §3). Cada fase cierra con las compuertas de `PM/` §6.1 (build, `Wms.Tests`, `Wms.IntegrationTests`, `has-pending-model-changes`, prueba de integración de cada endpoint de la fase), sus casos QA en PASA por API, commit y push de `f2/f01-nucleo`.

| Fase | Parte | Contenido | Criterio de salida | Estado |
| --- | --- | --- | --- | --- |
| 1 | 1 | Base y catálogos: C-F01-00; D9 a D17; C-F01-01 a C-F01-68, C-F01-141 y C-F01-163 a C-F01-170; migración `AddCatalogSortAndPrefixes` | QA2-F01-001 a QA2-F01-019 en PASA | Completada el 2026-11-23 (BE `b089eef`): QA2-F01-001 a 019 en PASA por API (pruebas de integración HTTP contra Postgres); `Wms.Tests` 2098 → 2150; `Wms.IntegrationTests` 479 → 653, con los mismos 2 fallos heredados de la cola de báscula; `has-pending-model-changes` limpio. `IDianTrmService`, `DianTrmService`, `DianTrmOptions` y `TrmSource.Dian` siguen hasta la fase 6 (ver nota) |
| 2 | 1 | Unidad de medida fuera: D18, D19; C-F01-69 a C-F01-77 y R-UOM; migración `RemoveUnitMeasure` | QA2-F01-020 y QA2-F01-021 en PASA; `grep -rl UnitMeasure` sin resultados fuera de `Migrations/` | Completada el 2026-11-23 (BE `9bb205b`): QA2-F01-020 y 021 en PASA por API (pruebas de integración HTTP contra Postgres: `ProductEndpointsTests`, `PerUomByPackagingTests`, `ReadsWithoutUomTests`); `Wms.Tests` 2150 → 2137 (salen las pruebas del catálogo y de la validación de la unidad); `Wms.IntegrationTests` 653 → 672, con los mismos 2 fallos heredados de la cola de báscula (pasan aislados); `has-pending-model-changes` limpio; `grep` sin resultados. Agrupaciones por embalaje y campos renombrados: §2.2.6 |
| 3 | 1 | Entradas y pesos: D20 a D28; C-F01-78 a C-F01-89; migración `EntryPerDocument` | QA2-F01-022 a QA2-F01-031 en PASA | Completada el 2026-11-23 (BE `5a44a71`): QA2-F01-022 a 031 en PASA por API (pruebas de integración HTTP contra Postgres: `EntryPerDocumentTests`, 12 pruebas, una o más por endpoint de C-F01-78 a C-F01-89); `Wms.Tests` 2137 → 2120 (salen las del cierre de camiones y de los bloqueos de Bodega; entran las de la mercancía y de la entrada duplicada); `Wms.IntegrationTests` 672 → 661 (salen 23 del depósito adicional, el pesaje compartido, la llegada a Bodega, el cargue previo al repesaje y el cierre de camiones; entran 12), con los mismos 2 fallos heredados de la cola de báscula (pasan aislados); `has-pending-model-changes` limpio; migración `EntryPerDocument` aplicada en la base local. Ver la nota de la fase 3 |
| 4 | 1 | Edición del ingreso: D29 a D32; C-F01-90 a C-F01-93; sin migración | QA2-F01-032 a QA2-F01-035 en PASA | Completada el 2026-11-23 (BE `4f4a78b`): QA2-F01-032 a 035 en PASA por API (pruebas de integración HTTP contra Postgres: `EntryCorrectionTests`, 9 pruebas, una o más por endpoint de C-F01-90 a C-F01-93); `Wms.Tests` 2120 → 2133 (entran 18 de `EntryCorrectionRulesTests`, salen 5 del validador del manifiesto retirado); `Wms.IntegrationTests` 661 → 670, con los mismos 2 fallos heredados de la cola de báscula (pasan aislados); `has-pending-model-changes` limpio, sin migración. Ver la nota de la fase 4 |
| 5 | 1 | Salidas: D1 a D4, D33 a D40, D45 a D47; C-F01-94 a C-F01-139 y R-SAL; migración `ReplaceLoadingOrderWithGoodsExit` | QA2-F01-036 a QA2-F01-050 en PASA; `grep -rl LoadingOrder` sin resultados fuera de `Migrations/` | Completada el 2026-11-24 (BE `202a42d`): QA2-F01-036 a 050 en PASA por API (pruebas de integración HTTP contra Postgres: `GoodsExitFlowTests`, 25 pruebas, y `OutputInitiationTests`, 7, con una o más por endpoint de C-F01-94 a C-F01-111 y 11 de los retirados en 404; C-F01-139 en `DispatchGuideVerificationTests`); `Wms.Tests` 2133 → 2030 (salen las de la orden de cargue, sus validadores, el pesaje compartido y la salida con tiquete; entran 31 de `ExitStateRulesTests`, `ExitAvailabilityTests` y `DispatchedWeightAllocatorTests`); `Wms.IntegrationTests` 670 → 673, con los mismos 2 fallos heredados de la cola de báscula (pasan aislados); `has-pending-model-changes` limpio; migración `ReplaceLoadingOrderWithGoodsExit` aplicada en la base local; `grep` sin resultados. Ver la nota de la fase 5 |
| 6 | 1 | Facturación: D41 a D43; C-F01-140; importador con la tasa (D44); importación completa de ensayo (§7); sin migración | QA2-F01-051 a QA2-F01-054 en PASA; conteos de la importación iguales; se borran `IDianTrmService`, `DianTrmService`, `DianTrmOptions` y `TrmSource.Dian` | Pendiente |
| I-01 | 3 | Integración con F02 (§13) | §13.4 | Pendiente |

Los avisos de D45 entran en la fase de su regla (3 y 5; el de la tasa, en la 6).

**Servicio de la DIAN (respuesta del usuario del 2026-11-23, «Dejarlo hasta la fase 6»):** la fase 1 retiró `GET system/dian-trm/today` (C-F01-14) y la consulta del levante (D15), pero el servicio de la DIAN lo sigue usando la facturación de almacenamiento (`StorageBillingService.TryAssignDianTrmAsync`, `WarehouseStorage.AssignDianTrm`). Se borra en la fase 6, cuando D42 y D43 lo reemplazan por la tasa semanal.

**Fase 5, salidas (2026-11-24; decisiones aplicadas por `DEC-002` y precisiones para I-01, sin cambiar rutas ni campos del contrato):**

- *Historial de guías.* `GET foreign-trade/dispatch-guides` se retira como dice C-F01-119 (D2, D3): la fila C-F01-171 de §2.2.6 fue el renombre mecánico de la fase 2 sobre ese mismo endpoint. La guía se consulta en la salida (`exitSchema.guide`, `guideHistory`) y se busca con `GET exits?guideNumber=`.
- *Inventario de Bodega.* `GET warehouse/inventory/deposits` no está en la lista de retirados: se conserva con la misma respuesta; su consulta pasa a `GetInventoryDepositsQuery` (antes compartida con la orden de cargue).
- *Salidas bloqueadas (BR-05-004).* La confirmación responde el mensaje y el status de hoy: 400 «El cliente '{nombre}' tiene las salidas bloqueadas: {motivo}.». C-F01-98 lo escribió como 409 «El tercero {nombre} tiene las salidas bloqueadas.»: **pendiente de decidir con el usuario en I-01** (cambiarlo toca la regla compartida del tercero). El Borrador se arma aunque el cliente esté bloqueado: lo que se detiene es la confirmación.
- *Vencimiento de la guía.* La confirmación no trae fecha de vencimiento: con días de tránsito, salida + días; sin ellos, 30 días (la regla de hoy de la guía de exportación).
- *Firmante.* La global la firma el importador del depósito; sin importador registrado (o con varios), el conductor.
- *Exportación.* La guía se emite al confirmar con su cobro (D36), ya no gratis al cargar.
- *Báscula sin `exitId`.* Sin conductor (ni en la petición ni en el ingreso) responde 400 «Elija el conductor del camión.» (mensaje nuevo, de forma). El servicio de báscula del Borrador usa la modalidad «Otros» y no tiene cliente hasta que Comercio Exterior agregue las líneas. Con `exitId` en Borrador, el conductor o la placa del registro pasan a la salida (D37).
- *Pesaje en curso.* Mientras el servicio de salida no tiene tiquete, los 409 de C-F01-100 y C-F01-109 dicen «el pesaje en curso».
- *Guardas de importación de hoy (CHG-33).* Báscula no cierra el pesaje de una salida de importación sin guía vigente y Vigilancia no deja salir el camión: mensajes con «salida» en lugar de «orden».
- *Mensajes de forma nuevos* (no cambian ninguno del contrato): dirección > 250, observaciones > 500 o > 250, orden del cliente (número, emisor agencia o importador, fecha no futura), transportadora no válida, tiquete o producto que no pertenece a la salida, línea repetida o ajena en el cargue, fecha de salida anterior a ayer, «Indique el cobro de la guía.».
- *R-SAL* aplicado en: detalle del servicio (`exitId`), candidatos de documento (`exitId`), registro de báscula (`exitId`, `exitNumber`), historial de báscula (`exitOrder` con `exitId` y `exitNumber`; `additionalOrders` siempre vacío), informe diario (`exitNumber`; salidas confirmadas o completadas, fecha de la guía o de la confirmación), kárdex y movimientos (`exitNumber`), abandono (`exitNumber`), estadísticas (`activeExits`, `pendingExits`). Los campos `removedOrderItems` y `cancelledOrders` de la anulación del depósito conservan el nombre y cuentan líneas y salidas en Borrador.
- *Líneas de guía anulada.* `dispatch_guide_lines.goods_exit_line_id` es nulo si la salida reabierta reemplaza sus líneas: la guía anulada conserva sus cifras por producto.

**Fase 4, edición del ingreso (respuestas del usuario del 2026-11-23, durante la fase):**

- *Cambio de documento (D29).* Si la entrada es la única vigente de su depósito y no se elige otro, se corrige el tipo y el número del documento del mismo depósito, que conserva su número. Si no, la entrada se traslada al depósito elegido (`DEC-057` D1, misma modalidad) o a uno nuevo. Solo lo bloquean el levante o la salida de sus productos (409 «{producto} ya tiene levantes o salidas: no se puede quitar.»); se trasladan con ella las cantidades y el stock (kárdex en los dos depósitos), la recepción de Bodega, las novedades, las unidades de carga, lo ubicado (en las mismas ubicaciones) y el ciclo de báscula con su tiquete y su factura. El depósito nuevo copia del de origen los terceros, la fecha del documento, la moneda, las observaciones y la descripción de la inspección; su fecha de ingreso es la de Vigilancia del camión. Un depósito de origen que queda sin entradas sigue en su estado y Comercio Exterior lo anula.
- *Unidades de carga (D31).* El modo de carga del depósito sale de la suma: unidades de carga si alguna entrada vigente las tiene; si ninguna, mercancía suelta. Se admiten entradas mixtas. `usesCargoUnits` de C-F01-93 es «la entrada tiene unidades»; la mercancía de cada unidad se sigue repartiendo con `PUT …/cargo-unit-breakdown`.
- *Precisiones del contrato para I-01 (sin cambiar rutas, campos ni mensajes):* la lectura (`depositEntrySchema`) no trae el Id del embalaje, así que `products[].packagingTypeId` nulo deja el embalaje como está y `packaging` (el nombre) se ignora; una entrada anulada no se corrige (409 «La entrada está anulada: no se corrige.», mensaje nuevo que falta agregar a C-F01-90); en C-F01-93, `driver` y `entryReasonId` pueden venir nulos si Vigilancia no los registró (el esquema los declara obligatorios); «despachado» es lo de las guías vigentes, hasta que la fase 5 cambie la salida.

**Fase 3, ciclo en el cobro (respuesta del usuario del 2026-11-23, «Ciclo en el cobro»):** el ciclo de báscula de cada entrada sigue naciendo en el cobro (`storage/process-payment` o `storage/start-pending-billing`), uno por entrada; ahí se marca `IsDuplicateEntry` y la duplicada sale en $0 aunque el operario envíe otro valor. Por eso `storage/initiate` y `storage/register` devuelven `weighbridgeCycleId` nulo (el esquema `storageEntryInitiateResultChangesSchema` pasa a `guidSchema.nullable()`) y la pantalla de F03 toma el ciclo de la respuesta del cobro, como hoy. F02 no cambia. Precisiones de la fase, por las decisiones: el detalle del depósito expone `dispatchedWeight` y `weightBalance` en nulo hasta la fase 5 (D39); el formulario debe enviar el peso de la mercancía para que la tara y el neto se deduzcan (D21: el manifiesto solo se informa); una inspección sin documento se reconoce como ingreso con depósito por su depósito; dos registros del mismo camión sin depósito elegido dejan el segundo como entrada duplicada en un depósito nuevo (D20 y `DEC-057` D1).

**Fase 1, nota de D13:** «ciclo guardado» incluye la operación que Báscula ya guardó con `storage/initiate` para un motivo con categoría, aunque el ciclo nazca después, en el cobro. Sin categoría (solo bodega), sigue el bloqueo de hoy (WMS-5).

---

## 9. Riesgos

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R1 | La fase 5 es la más grande: `LoadingOrder` en 158 archivos y 49 de pruebas | Partida por compilación (D6): las fases 1 a 4 dejan el resto estable; la 5 borra la orden y ajusta las pruebas en sus *helpers* (§0.5). Si el borrado no compila en un paso, el ejecutor puede hacer commits intermedios dentro de la fase, pero la cierra completa |
| R2 | Las pantallas viejas de Báscula, Bodega y CE dejan de funcionar en `fase-2` desde las fases 3 y 5 | Esperado (`PM/` §5.4, M9): nada de `fase-2` va a staging antes del despliegue final. I-01 no las arregla; F03 a F06 las reemplazan |
| R3 | `unaccent` no está en la imagen de PostgreSQL de las pruebas | La imagen oficial `postgres:18.0` trae las extensiones de *contrib*; si falla, el ejecutor se detiene y pregunta (no cambia la imagen por su cuenta) |
| R4 | El contrato de los grupos D y E se escribe antes de las pantallas de F03 a F06 | Esos planes pueden agregar endpoints o campos; no cambian los de este contrato sin una decisión nueva (`PM/` R3). La forma de `exitSchema` es la base de F06 |
| R5 | Prorrateo y redondeo del peso despachado (D4) | Clase pura con pruebas de borde (cero, un depósito, redondeo) |
| R6 | La entrada que cobró se anula y las duplicadas quedan en $0 (D20) | Aceptado: se anula y se repite, y Facturación ajusta (`DEC-013`, `DEC-050`). Se anota en la nota para operarios de G1 |
| R7 | Recalcular facturas al registrar una tasa (D42) toca muchos depósitos | Solo los `Weekly`/`WeeklyFallback` del rango y solo facturas en Borrador; prueba de integración con varios depósitos |
| R8 | Cambiar políticas quita una función (`DEC-005`) | Las políticas nuevas son uniones; `CatalogPoliciesTests` y QA2-F01-019 lo verifican |

---

## 10. Fuera de alcance

- Las pantallas: la cola, el formulario de tres pasos, el historial y la impresión de Báscula (F03); la recepción, los relojes y las órdenes de salida de Bodega (F04 y F06); el detalle por etapas, los amparados, la confirmación sin cliente, la edición de «Datos principales» en Confirmado y los levantes en tabla (F05); acuerdos y fórmulas nuevas (F07); facturas y reportes (F08); notificaciones configurables (F09).
- Las AF de otras features aunque toquen las mismas entidades: AF-75, AF-76, AF-77, AF-78, AF-93 (F05); AF-106 (F06); AF-116, AF-119, AF-120 (F07 y F04).
- Quitar `weighbridge/stakeholders/quick` y `weighbridge/transport-companies/quick` (lo decide F03).
- Staging, el despliegue final y su plan (`PM/` §7.3).
- Estimar esfuerzo.

**Cambios al hub de este plan** (aplicados el 2026-11-22 con el «sí» del usuario; en el 2, «Construida» quedó «Se construye», porque F01 aún no se ejecuta):

1. `D/contexto/decisiones.md`, `DEC-012`, al final de la viñeta de consecutivos: «*Precisada por el plan de F01 de la fase 2 (D1, 2026-11-21): la salida de mercancía usa la serie `2026SM00001`, que reemplaza a `2026OC00001` de la orden de cargue.*»
2. `D/contexto/decisiones.md`, `DEC-023`, después de «*Reemplazada por `DEC-080` (AF-85).*»: «*Construida en F01 de la fase 2 con la tasa semanal (D15, D42); los depósitos migrados conservan su TRM del legacy (D7).*»

---

## 11. Prompts por parte

- Parte 1 (backend): [prompt-f2-f01-nucleo-backend-2026-11-21.md](prompt-f2-f01-nucleo-backend-2026-11-21.md), rama `f2/f01-nucleo` del backend.
- Parte 3 (I-01, con F02): [prompt-f2-f01-nucleo-integracion-2026-11-21.md](prompt-f2-f01-nucleo-integracion-2026-11-21.md), ramas `f2/f01-nucleo` (BE) y `f2/f02-base` (FE).
- Parte 2 (F02): en su plan, `../f02-base/plan-cerrado-f2-f02-base-2026-11-21.md` §11.
- Planificador (ejecutado): [prompt-f2-f01-nucleo-planificador-2026-11-21.md](prompt-f2-f01-nucleo-planificador-2026-11-21.md).

---

## 12. Mensajes de commit sugeridos

Cada uno termina con la línea de coautoría que indique la sesión.

| Fase | Repo | Mensaje |
| --- | --- | --- |
| 1 | BE | `feat(catalogos): orden y filtros por columna, motivos con categoría, prefijos, tasa semanal y permisos de Configuración (DEC-080, F01)` |
| 2 | BE | `feat(productos): se retira la unidad de medida y PER_UOM cobra por embalaje (DEC-080, F01)` |
| 3 | BE | `feat(bascula): una entrada por documento con sus pesos, manifiesto solo con carta porte y sin cierre de camiones (DEC-080, F01)` |
| 4 | BE | `feat(ingreso): edición del ingreso por Báscula hasta confirmar y por Comercio Exterior en cualquier estado (DEC-080, F01)` |
| 5 | BE | `feat(salidas): la salida de mercancía reemplaza a la orden de cargue; la guía se emite al confirmar (DEC-080, DEC-081, F01)` |
| 6 | BE | `feat(facturacion): peso de mercancía en las fórmulas por peso y tasa de la semana de ingreso (DEC-080, F01)` |
| Cada fase | docs | `docs(f01): fase N de F01 cerrada (sprint 11)` |

---

## 13. Integración I-01 (parte 3)

Un agente con los dos repos (M1, M10), cuando F01 (fases 1 a 6) y F02 (todas sus fases) están cerradas y con push. Ocupa los dos repos: ningún otro agente trabaja en ellos mientras dura.

### 13.1 Qué hace

**Frontend, en `f2/f02-base`:**

1. Escribe la fuente real `<recurso>.http.ts` de cada `<recurso>.source.ts` que dejó F02 (lista en el plan de F02 §3.2), con `useApi` y los esquemas Zod de §2.3: cada respuesta se valida con su esquema (`.parse`) en la fuente http, y un fallo de esquema se registra en consola y se muestra como error del API.
2. Cambia la línea de cada `<recurso>.source.ts` a la fuente http y borra la carpeta `mocks/` de cada dominio. `F/shared/mocks/` se queda: sus ayudas y la sesión simulada las usan F03 a F09 (plan de F02, D10).
3. Monta en los detalles las secciones que F02 dejó como marcadores (plan de F02, D2 y D11): acuerdos del tercero, cuentas, contactos, roles y marca «sin salidas»; precios, reglas, mínimos e impuestos del servicio. Usa los componentes de hoy sin cambiarlos, salvo una cosa: `F/features/agreements/components/AgreementServiceFormDialog.vue` y `F/features/services/components/ServicePricingRuleFormDialog.vue` dejan de cargar unidades de medida (el esquema de `PER_UOM` ya no tiene `uom`, D19), para que las secciones conservadas no muestren el error del endpoint retirado.
4. Enlaza en el menú las rutas nuevas (`/settings/prefixes`, `/settings/exchange-rates`) y deja el menú de P-TR-01 tal como lo fija el plan de F02 §1 (D5).
5. Ajusta los `requiredRoles` de las páginas de Configuración y Administración a la tabla del plan de F02 (D6); abre `/admin/forklift-rates` a Facturación (su API ya es `BillingAccess`, `B/Wms.Api/Controllers/v1/ForkliftRateController.cs:45`, `:72`).
6. Borra lo viejo (`PM/` §5.4), después de comprobar quién importa cada archivo (trampa 7): `F/pages/admin/unit-measures/index.vue` y sus composables y servicios (M21); las páginas `create.vue`, `edit/[id].vue` y `[id].vue` de usuarios, terceros, productos y servicios, que pasan a modal y drawer; los componentes y pruebas que solo ellas usaban. El enlace de `F/pages/billing/invoices/[id].vue:331` pasa a `/admin/stakeholders?id={id}`.
7. Corre las guardias nuevas de F02 (listado de AF-129 y «sin llamadas reales») y saca de la lista de maquetación las páginas integradas.

**Backend, en `f2/f01-nucleo`:** nada nuevo. Si una pantalla necesita algo que el contrato no tiene, o el backend responde distinto del contrato, el agente se detiene y pregunta (`PM/` R3); no cambia el contrato por su cuenta.

**Cierre:** compuertas de `PM/` §6.3 en los dos repos; casos QA de §13.3 y los QA2-F02 del plan de F02 en PASA, en el navegador, contra el backend local de `f2/f01-nucleo`; fusión de `f2/f01-nucleo` en `fase-2` (BE) y de `f2/f02-base` en `fase-2` (FE) con `--no-ff`, y push de los dos.

### 13.2 Pantallas de F02 y sus endpoints

| Pantalla (plan de F02) | Ruta | Endpoints |
| --- | --- | --- |
| P-TR-01 Menú por rol y P-TR-10 Sidebar | todas | Ninguno nuevo: los roles salen de la sesión de hoy |
| P-TR-10 Login | `/auth/login` | Ninguno nuevo: el de hoy, sin cambios |
| P-TR-02 Listado y P-TR-03 Drawer (Conductores) | `/admin/drivers` | C-F01-15, C-F01-16, C-F01-17, C-F01-18, C-F01-19 |
| P-TR-03 Modal a dos columnas (Ubicaciones) | `/admin/locations` | C-F01-43 a C-F01-46 |
| P-TR-04 Motivos de ingreso | `/admin/entry-reasons` | C-F01-01, C-F01-03 a C-F01-06 |
| P-TR-05 Prefijos | `/settings/prefixes` | C-F01-08, C-F01-09 |
| P-TR-06 Tasas de cambio | `/settings/exchange-rates` | C-F01-10, C-F01-11, C-F01-12 |
| P-TR-09 Formulario de cobro y P-TR-11 Selector (galería) | `/dev/components` | C-F01-25, C-F01-141 |
| Terceros | `/admin/stakeholders` | C-F01-25 a C-F01-28; secciones montadas: los endpoints de hoy de contactos, cuentas, roles, marca «sin salidas» y acuerdos (§13.5) |
| Productos | `/admin/products` | C-F01-69 a C-F01-72; C-F01-29 (selector de embalaje) |
| Tipos de embalaje | `/admin/packaging-types` | C-F01-29 a C-F01-32 |
| Tipos de unidad de carga | `/admin/cargo-unit-types` | C-F01-33 a C-F01-36 |
| Servicios | `/admin/services` | C-F01-37 a C-F01-42; secciones montadas: precios, reglas, mínimos e impuestos de hoy (§13.5) |
| Vehículos | `/admin/vehicles` | C-F01-21 a C-F01-24; C-F01-25 (transportadora) y C-F01-141 («+») |
| Ciudades | `/admin/cities` | C-F01-47 a C-F01-51 |
| Cuadrillas | `/admin/crews` | C-F01-52 a C-F01-55 |
| Parámetros | `/admin/parameters` | C-F01-56 a C-F01-58 |
| Usuarios | `/admin/users` | C-F01-59 a C-F01-67 |
| Auditoría | `/admin/audit` | C-F01-68 |

### 13.3 Casos QA en el navegador

Además de los QA2-F02 del plan de F02, que I-01 repite contra el backend real.

| ID | Regla de origen | Precondición | Pasos | Resultado esperado | Verificación |
| --- | --- | --- | --- | --- | --- |
| QA2-F01-055 | AF-129; C-F01-00 | Más de 50 conductores | Configuración › Conductores: filtrar «jose» en Nombre y ordenar por Documento descendente; pasar de página | La red muestra `name=jose&sortField=idNumber&sortOrder=desc`; el orden se mantiene entre páginas | Pantalla y red |
| QA2-F01-056 | AF-127, AF-128; D11 | Usuario CE | Abrir Configuración; crear un vehículo; abrir Prefijos y guardar uno; abrir Parámetros por URL | Ve Configuración sin Parámetros; crea el vehículo; guarda el prefijo; Parámetros da «acceso denegado» | Pantalla |
| QA2-F01-057 | AF-127; D11 | Usuario Facturación | Abrir Prefijos por URL; registrar una tasa | Prefijos da «acceso denegado»; la tasa se guarda | Pantalla |
| QA2-F01-058 | `DEC-005` | Usuarios Vigilancia, Báscula y Bodega | Iniciar sesión con cada uno | No ven Configuración, Tarifas y acuerdos ni Administración; ven su módulo como hoy | Pantalla |
| QA2-F01-059 | AF-08; D12 | Usuario Admin | Motivos: crear «Pesaje de prueba» con «Requiere pesaje» y sin categoría | El aviso del backend «Elija la categoría del motivo…» se muestra en el campo | Pantalla |
| QA2-F01-060 | AF-85, AF-86; D15 | Tasa del 16 al 22/11 | Tasas: crear una del 20 al 26/11 | Se muestra el 409 «Las fechas se cruzan…» del backend | Pantalla |
| QA2-F01-061 | AF-18; D16 | Conductor CC 1000001 | Conductores: crear otro con CC 1000001 y otro nombre | Se crea; la lista muestra los dos con nombre y documento | Pantalla |
| QA2-F01-062 | AF-54; C-F01-141 | Usuario Bodega | Galería de componentes › Cobro: «+» en Tercero registrado, crear uno | Se crea y queda elegido en el selector | Pantalla |
| QA2-F01-063 | `DEC-005`; plan de F02 D2 | Usuario Facturación | Terceros › detalle de un cliente › Acuerdos; Servicios › detalle › Tarifas base | Las secciones de hoy funcionan dentro del drawer | Pantalla |
| QA2-F01-064 | M21 | — | Abrir `/admin/unit-measures` | 404 de la aplicación; el menú no la tiene | Pantalla |
| QA2-F01-065 | `PM/` §6.3 | I-01 cerrada | `grep` de imports de `mocks/` fuera de `F/shared/mocks/` y de las pruebas | Sin resultados | Código |

### 13.4 Criterio de salida

- Compuertas de `PM/` §6.1 en BE y §6.2 en FE (salvo «sin llamadas reales»), con las cifras antes y después.
- QA2-F01-055 a QA2-F01-065 y los QA2-F02 del plan de F02 en PASA, en el navegador, contra el backend local.
- Ningún import de `mocks/` de una feature fuera de las pruebas; las carpetas `mocks/` de los dominios de F02, borradas.
- Menú con las rutas nuevas; páginas viejas y sus pruebas, borradas.
- Fusión con `--no-ff` de las dos ramas en `fase-2` y push. Matriz y `D/planes/README.md` actualizados; los casos QA copiados a `D/qa/`.

### 13.5 Endpoints de hoy que montan las secciones conservadas

Sin cambios de forma ni de política en F01; los usan los componentes de hoy, que I-01 monta dentro de los drawers (plan de F02, D2 y D11). No se simulan en la maquetación.

| Sección | Endpoints (`B/Wms.Api/Controllers/v1/`) |
| --- | --- |
| Tercero: roles, cuentas, contactos | `StakeholderController.cs`: `{id}/roles`, `{stakeholderId}/bank-account` y `{stakeholderId}/contact` (lecturas, sin cambios); las escrituras son C-F01-163 a C-F01-170 |
| Tercero: marca «sin salidas» | `PATCH stakeholder/{id}/exit-block` (`ExitBlockAccess`) |
| Tercero: acuerdos (hasta F07) | `stakeholder/{stakeholderId}/agreement` y sus servicios (`BillingAccess` para escribir) |
| Servicio: tarifas (hasta F07) | `service/{id}/prices`, `pricing-rules`, `minimum-values`, `assign-tax`, `remove-tax` (`BillingAccess` para escribir); `administration/taxes` |

Facturación edita también roles, cuentas y contactos del tercero (C-F01-163 a C-F01-170, D11); los acuerdos siguen siendo de Admin y Facturación, y la marca «sin salidas», de `ExitBlockAccess`.

