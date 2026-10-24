# Plan cerrado de backend — paridad con Bodegas legacy (wms-api)

**Fecha:** 2026-09-29. **Repositorio:** `code_workspace/Backend/wms-api`. **Rama de trabajo:** `develop` (`b089d2b`), la única: no se crean ramas ni PR. **Los commits los hace el usuario;** el implementador se detiene al terminar cada ítem (§E).
**Documento hermano (obligatorio):** `code_workspace/docs/planes/paridad-legacy/contrato-api-paridad.md`. Contiene el contrato exacto de cada endpoint nuevo o modificado, con el identificador `C-Fx-yy` que cita este plan. Es parte del plan: el implementador lo sigue al pie de la letra.
**Decisiones:** todas las preguntas se cerraron con el usuario el 2026-09-29 (§A.4). No hay supuestos abiertos.

---

## A. Resumen ejecutivo

### A.1 Qué se construye

La empresa reemplaza el sistema legacy «Bodegas» (PHP) por el WMS v2. El análisis comparó ambos sistemas y el negocio decidió qué construir. Este plan convierte esas decisiones en trabajo de backend, en seis fases que se hacen en secuencia sobre `develop`:

| Fase | Tema | Qué deja lista | Dificultad |
|---|---|---|---|
| 1 ✅ | Báscula al ritmo del legacy (completada el 2026-09-30, §C.1) | Los siete datos que el legacy pedía en Comercio Exterior dejan de ser obligatorios en báscula y se exigen al confirmar el depósito. Producto por descripción libre, unidades de carga sin desglose, efectivo y cambio. | Alta |
| 2 ✅ | Control aduanero (completada el 2026-09-30, §C.2) | No se despacha más de lo nacionalizado por producto. Levantes sin duplicados, retirables y con FOB y tasa congelados. Prórroga, abandono y su alerta. Catálogo de ciudades con días de tránsito y vencimiento de la guía calculado. | Alta |
| 3 ✅ | Correcciones y facturación (completada el 2026-09-30, §C.3) | Anular pesajes, modificar y revertir salidas, anular guías y depósitos con todos sus efectos, anular y refacturar almacenamiento, ciclos de facturación legacy y períodos con la regla legacy. | Muy alta |
| 4 ✅ | Bodega y mercancía (completada el 2026-09-30, §C.4) | Ubicación por cantidades (ubicar, mover, liberar), novedades con desglose e impresión, listas de empaque, pesaje compartido de salida, salida con el tiquete de ingreso, conteo de impresiones de etiquetas y cuadrillas. | Alta |
| 5 ✅ | Reportes y consultas (completada el 2026-09-30, §C.5) | Los reportes que el legacy exportaba a Excel, con sus columnas: kardex con levantes, inventario general, pólizas, ingresos por producto, facturación anual, informe por CPI, báscula por modalidad y reporte para agencias de aduana. Columnas de saldo y búsquedas nuevas. | Media |
| 6 ✅ | Migración y corte (implementada el 2026-10-01, §C.6; E19 con datos reales cumplida el 2026-10-06) | Importación por CSV de maestros y depósitos vivos, con simulación y conciliación. Respaldos diarios con destinos configurables (disco local o S3). | Muy alta |

La **fase 1 es la prioridad del proyecto**. Báscula es la puerta de entrada y el punto de congestión: el criterio es que un camión de importación quede registrado en un tiempo igual o menor al del legacy. La fase 7 del roadmap (comodidad) no tiene trabajo de backend (§C.7).

### A.2 Orden

1 → 2 → 3 → 4 → 5 → 6, en secuencia y todo en `develop`. Dentro de cada fase, un ítem a la vez: el implementador termina el ítem, se detiene y el usuario hace su commit antes del siguiente. Una fase empieza cuando la anterior tiene todos sus ítems con commit (§E).

### A.3 Qué queda fuera y por qué

- **Colmotores** (importador 70): VIN, seriales, voltajes, patio externo, lecturas y averías de vehículo. Está inhabilitado y no se migra.
- **Acceso, autenticación, autorización y roles.** Son funcionalidad nueva de la v2. Los endpoints nuevos usan las políticas que ya existen y no se crean ni cambian políticas (§G).
- **Decisiones aceptadas que no se construyen:**
  - Portería sin pedir la guía (GAP-004).
  - Báscula sin precargar cliente ni tarifa por placa (GAP-018).
  - Soportes documentales (GAP-012).
  - Catálogos fijos en código (GAP-022).
  - Datos de maestros del legacy como representantes con porcentaje o marca y carrocería del vehículo (GAP-023).
  - La numeración actual de la v2.
  - Solo dos monedas: COP y USD (GAP-020).
- **Frontend.** Otro agente lo planifica contra `contrato-api-paridad.md`. Los ítems de báscula que solo son de interfaz (BAS-02 mercancía en línea, BAS-04 peso en la misma pantalla, BAS-06 tabulación y el cronometraje 1.8) no tienen backend.
- **«Pesajes globales»** (LEGACY-FUNC-166), que son la selección de tiquetes de la «Salida Global» del legacy: no se construye la salida en lote. Se cubre con F4-08 camión por camión (P16).
- **Anomalías del legacy.** No se copian. Cada ítem dice cuál corrige.

### A.4 Decisiones cerradas en esta ronda (2026-09-29)

| # | Tema | Decisión |
|---|---|---|
| P1 | Documento sin fecha en báscula | Se busca por número y tipo solo entre depósitos abiertos. Si hay uno, se asocia; si hay varios, 409 pidiendo la fecha. Si el depósito no tenía fecha y el camión la trae, se guarda. |
| P2 | Qué se exige al confirmar | Todas las modalidades: fecha del documento, moneda, valor > 0, número y peso del manifiesto en cada camión. IMP: además importador y agencia de aduanas. EXP: además exportador. INSP: nada más. Comercio Exterior completa el manifiesto por camión en Borrador o Confirmado. |
| P3 | Producto libre | Si la descripción no existe en el catálogo, báscula crea el producto en el mismo registro. Comercio Exterior puede cambiar el producto de la línea en Borrador. |
| P4 | Efectivo y cambio | Se guardan en el pago. |
| P5 | Unidades de carga sin desglose | Con una unidad, automático. Con dos o más, Comercio Exterior reparte en Borrador y confirmar lo exige. Un camión tardío a un depósito confirmado trae el desglose. |
| P6 | Abandono | Tres correcciones: el reporte incluye los depósitos con prórroga desde 60 días; los días se cuentan desde la fecha de ingreso; una marca «Destino de abandono» en ciudades reemplaza el ID fijo −9. |
| P7 | Regla legacy de períodos | Aplica a todos los ciclos. |
| P8 | Vencimiento de la factura de almacenamiento | Sigue siendo emisión + días de plazo del cliente. La fecha límite legacy (fin + 3 días) se guarda y se muestra en el período. |
| P9 | Refacturar | Acción explícita sobre la factura anulada. |
| P10 | BAS-08 y BAS-09 | Se construye la lectura del código: pesaje compartido de salida en $0 y salida con el tiquete de ingreso. |
| P11 | Listas de empaque | Formato legacy corregido. Comercio Exterior carga y asocia en Borrador. |
| P12 | Reportes | Marca UAP en el tercero. Informe anual: almacenamiento por defecto, con filtro por servicio. |
| P13 | Migración | Saldos vivos por CSV, endpoints de Admin con simulación y conciliación. Tarifas a mano. El histórico se consulta en el legacy. |
| P14 | Respaldo | Diario, con retención de 30 diarios y 12 mensuales. **Los destinos se configuran desde la aplicación: disco local o S3, ambos soportados.** |
| P15 | Decisiones por defecto | Confirmadas (§B.4). |
| P16 | «Pesajes globales» / «Salida Global» (LEGACY-FUNC-166) | Se cubre con F4-08: cada camión sale con su tiquete de ingreso, con una orden y una guía por camión (se cobra una guía por camión). No se construye la selección de varios tiquetes en lote. F4-08 queda disponible para báscula y para Comercio Exterior, como el permiso `salidas:registrar` del legacy. |
| P17 | Rama y commits | Todo se trabaja en `develop`, sin ramas ni PR. El usuario hace los commits. El implementador se detiene al terminar cada ítem y espera el commit antes de seguir. |

---

## B. Contexto mínimo para el implementador

### B.1 El negocio en media página

Bodegas Asociadas opera un **depósito público aduanero** en Ipiales (frontera con Ecuador). La mercancía que cruza la frontera se queda ahí mientras la DIAN la nacionaliza, la exporta o la inspecciona. Los servicios que se cobran son báscula, montacargas, guía de salida y almacenamiento. La factura legal se emite en SIIGO: el WMS calcula los valores y Facturación copia el número SIIGO.

**Flujo de importación en la v2:**

1. **Vigilancia** registra el ingreso del camión (placa, motivo). La placa queda en `EntryLog`.
2. **Báscula** toma el camión de la cola y registra el documento y la mercancía. Con el primer camión de una carta porte se crean el `ServiceRecord`, el depósito (`WarehouseStorage`, en `Draft`) y su parte de importación (`ImportWarehouseStorage`). La cantidad declarada de cada camión entra al stock (`WarehouseStorageEntry` por camión). Báscula cobra y pesa.
3. **Comercio Exterior (CE)** completa el depósito, lo **confirma** (`Draft → Confirmed`), imprime la etiqueta y registra los **levantes**. Confirmar abre el primer período de almacenamiento con su factura.
4. **CE** crea la **orden de cargue** (reserva stock). **Bodega** la ejecuta: descuenta el stock y deja un movimiento `Out`. **CE** emite la **guía de salida** (se cobra). Báscula pesa la salida y Vigilancia registra la salida del camión.
5. Cuando todo el stock llega a 0, el depósito pasa a `Closed`.

### B.2 Glosario

| Término | Significado | En el código |
|---|---|---|
| Depósito | Lote de mercancía amparado por un documento y una modalidad (IMP, EXP, INSP). Es la unidad de inventario, de etiqueta y de cobro de almacenamiento. | `WarehouseStorage` |
| Carta porte (CPI) | Documento de transporte internacional. Número + tipo + fecha + modalidad identifican el depósito. | `ServiceRecord.CargoManifestNumber` (el nombre engaña: es la carta porte) |
| Manifiesto del camión | Número y peso bruto según el manifiesto de carga de cada camión. | `WarehouseStorageEntry.ManifestNumber/ManifestWeight` y `Manifest` (por `EntryLog`) |
| Manifiesto DIAN | Número y fecha del manifiesto aduanero del depósito de importación. | `ImportWarehouseStorage.ManifestNumber/ManifestDate` |
| Levante | Autorización de la DIAN para disponer de la mercancía. En la v2 se registra por producto: un levante con tres productos son tres filas con el mismo número. | `ImportRelease` |
| Nacionalización | La mercancía con levante está nacionalizada. Solo lo nacionalizado se puede despachar. | suma de `ImportRelease.ReleasedQuantity` por producto |
| Orden de cargue (OC) | Autorización de CE para sacar mercancía de uno o varios depósitos. Reserva stock. | `LoadingOrder`, `LoadingOrderItem`, `WarehouseReserve` |
| Guía de salida | Documento que acompaña la salida. Congela los saldos por línea y se cobra (servicio `GUIA_SALIDA`). | `DispatchGuide`, `DispatchGuideLine` |
| Tiquete | Comprobante del pesaje. El ciclo tiene el peso de entrada, el de salida y el neto. | `WeighbridgeCycle`, `WeighbridgeWeighing` |
| Prórroga | Extensión del plazo aduanero: sin prórroga el depósito cae en abandono a los 30 días; con prórroga, a los 60. | nuevo en F2-08 |
| Abandono | Mercancía sin nacionalizar que venció su plazo. | nuevo en F2-09 |
| Unidad de carga | Contenedor, tanquero o remolque que entra con el camión, con su propia mercancía. | `WarehouseStorageCargoUnit`, `WarehouseStorageCargoUnitProduct` |
| Período de almacenamiento | Tramo de tiempo que se cobra por adelantado, uno por cargo. | `StorageBillingPeriod` |
| Stock | `ReceivedQuantity` = cantidad del depósito (declarada + ajustes CE-7). `CurrentStock` = lo que hay. `ReservedStock` = reservado por órdenes. `AvailableStock = CurrentStock − ReservedStock`. | `WarehouseStorageProduct` |
| Despachado | `ReceivedQuantity − CurrentStock` (solo el cargue baja el stock sin bajar la cantidad del depósito). | calculado |

### B.3 Arquitectura y convenciones obligatorias

| Capa | Contenido | Ejemplo |
|---|---|---|
| `Wms.Domain` | Entidades con métodos que validan sus transiciones y lanzan excepciones; enums. | `Wms.Domain/Entities/Warehouse/WarehouseStorage.cs` |
| `Wms.Application` | CQRS con MediatR: un comando o consulta por caso de uso, con su validador FluentValidation y su handler, en `Feature/Commands/Nombre/` o `Feature/Queries/Nombre/`. Servicios en `Feature/Common/Services`. Registro de servicios en `Wms.Application/DependencyInjection.cs`. | `Wms.Application/ForeignTrade/Commands/ConfirmStorageDeposit/` |
| `Wms.Infrastructure` | `AppDbContext` (`Persistence/AppDbContext.cs`), configuraciones EF en `Persistence/Configurations/<Área>/<Entidad>Configuration.cs` (se aplican solas con `ApplyConfigurationsFromAssembly`), datos sembrados en `Persistence/SeedDataExtensions.cs`, servicios externos. | `ImportReleaseConfiguration.cs` |
| `Wms.Api` | Controladores en `Controllers/v1`, jobs en `BackgroundJobs` (registrados en `Program.cs` con `AddHostedService`), records de request en `Controllers/v1/Requests/`. | `ForeignTradeController.cs` |
| `Wms.Common` | Excepciones, paginación (`QueryParametersBase`), `ColombiaTime`, normalizadores de texto (`Wms.Common/Text`). | |
| `Wms.Tests` | xUnit. Solo pruebas de dominio, validadores y calculadoras puras: **el proyecto no tiene proveedor de base de datos y no se le agrega**. Cada regla de este plan se escribe como método de dominio o clase pura para poder probarla. | `Wms.Tests/ForeignTrade/DispatchGuideBalanceCalculatorTests.cs` |

**Convenciones que este plan exige en todos los ítems:**

1. **Migraciones EF: no se generan.**
   - El implementador deja la entidad, su configuración y el `HasData` si aplica.
   - No toca `Wms.Infrastructure/Migrations` ni `Wms.Infrastructure/Persistence/Migrations`.
   - Cada cambio de esquema está listado en el ítem y en §F. El usuario genera la migración de cada ítem que cambia el esquema antes de hacer su commit (§E.3).
2. **Idioma.**
   - Español en mensajes de error, textos, notificaciones, comentarios de negocio y documentación.
   - Inglés en nombres de clases, propiedades, métodos y rutas.
3. **Errores de negocio.**
   - `BadRequestException` (400), `NotFoundException` (404) y `ConflictException` (409), de `Wms.Common.Exceptions`, con el **mensaje exacto** que da el ítem.
   - El cuerpo de error ya lo arma `GlobalExceptionHandler`: `{ title, status, description, errors: [{ code, description }] }`.
   - Los errores de FluentValidation salen como 400 con `description: "Error de validación de datos"` y la lista `errors`.
4. **Fechas.**
   - Las fechas de negocio se calculan con `Wms.Common.Time.ColombiaTime`: `Now`, `Today`, `DateOf(instante)`, `ToColombia`. Nunca con `DateTimeOffset.UtcNow`.
   - `UtcNow` solo se usa en `CreatedAt`, `UpdatedAt` y en marcas técnicas (`...At` de auditoría de la acción).
   - «Día calendario» siempre quiere decir el día en Colombia.
5. **Paginación.**
   - Las consultas de listado heredan de `QueryParametersBase`: `pageSize` se recorta a 50 y `all=true` devuelve todo.
   - Nunca se sube el tope. Los reportes pensados para Excel aceptan `all=true` y el Excel se arma en el frontend.
6. **Transacciones.**
   - Toda operación que escribe en más de una tabla usa una transacción: `await using var tx = await context.Database.BeginTransactionAsync(ct); … await tx.CommitAsync(ct);`.
   - Las notificaciones y los recálculos de facturación van **después** del commit. Si fallan, se registran en el log y nunca revierten la operación: es el patrón de `StorageRecalculationTrigger`.
7. **Auditoría.**
   - Toda entidad `IAuditable` ya deja altas, cambios y bajas en `audit_logs`, con usuario e IP. No se crean tablas de auditoría.
   - Cuando un ítem pide «motivo en la auditoría», el `SaveChangesAsync` se envuelve en `using (auditContext.Describe("texto")) { … }` (`Wms.Domain/Contracts/IAuditContext.cs`).
   - Las entidades nuevas implementan `IAuditable`, salvo que el ítem diga lo contrario.
8. **Notificaciones.**
   - Se envían con `INotificationOrchestrator.NotifyRoleAsync(SystemRolesCode.<Rol>.ToString(), new CreateNotificationParams(Guid.Empty, título, mensaje, NotificationLevel.<Nivel>, "<TipoEntidad>", idEntidad), sendEmail: false, ct)`.
   - Los roles son `ForeignTrade`, `Billing`, `Warehouse`, `Scale` y `Admin`.
9. **Enums.**
   - Todos los enums de estado se guardan como texto (`HasConversion<string>()`) y viajan en JSON como texto (`JsonStringEnumConverter`).
   - Agregar un valor a un enum persistido como texto **no** cambia el esquema.
10. **Controladores.**
    - Para evitar conflictos entre fases, los endpoints nuevos van en **controladores nuevos por tema**, con el prefijo de ruta y la política del módulo. Por ejemplo, `[Route("foreign-trade")] [Authorize(Policy = "ForeignTradeAccess")]`.
    - Sus records de request van en `Wms.Api/Controllers/v1/Requests/<Tema>Requests.cs`.
    - Solo se tocan los controladores existentes cuando el ítem modifica un endpoint que ya está en ellos.
    - La respuesta se envuelve siempre en `ApiResponse.Success(dato)`, o `ApiResponse.Success(items, pagination)` en los listados.
11. **Motivos.**
    - Donde un ítem pide «motivo», se valida `motivo.Trim()` entre 10 y 500 caracteres, con el mensaje que da el ítem.
12. **Rama y commits** (P17).
    - Todo el trabajo se hace en `develop`. No se crean ramas ni PR.
    - El implementador **no hace** `git add`, `commit`, `push` ni `merge`.
    - Al terminar cada ítem se detiene y entrega lo que pide §E.2. El usuario hace el commit, con el mensaje sugerido de §D.3, y solo entonces sigue el ítem siguiente.

### B.4 Decisiones por defecto confirmadas (P15)

1. **Levante repetido.** Se rechaza si el número o la aceptación ya existen en otro depósito. En el mismo depósito se permite para productos distintos del mismo levante, con el mismo par número–aceptación (F2-03).
2. **FOB del levante.** Se valoriza con la TRM de la DIAN del día del registro, como el legacy. Si la DIAN no responde, CE digita la tasa (F2-05).
3. **Ubicaciones por cantidades.** Se puede ubicar, mover y liberar. La posición se libera al ejecutar el cargue y una cantidad negativa se rechaza (F4-01, F4-02).
4. **Anular una guía cuya factura está aprobada o pagada.** Se anula la guía y se avisa a Facturación; la factura no se toca (F3-04).
5. **Anular un depósito.** Sus ítems salen de las órdenes de cargue pendientes y se liberan las reservas; si una orden queda vacía, se cancela (F3-08).
6. **Cancelar una orden.** Solo antes del cargue. Después se usa «Revertir salida», que exige anular antes la guía (F3-02, F3-04, F3-07).
7. **Ciudad de destino.** Un solo destino por orden. El vencimiento de la guía es la fecha de salida + los días de la ciudad; si la ciudad no tiene días, se digita (F2-07).
8. **Novedades.** Sin fotos y sin regla de suma entre buena, dañada, faltante y sobrante, como el legacy (F4-03).

### B.5 Cómo leer cada ítem

Cada ítem trae, en este orden:

- **Dificultad** (§B.6).
- **Regla** completa: condición → efecto, con números y mensajes exactos.
- **Evidencia**: el PHP legacy y el archivo actual de la v2 con sus líneas. Sirve para auditar el plan; no hace falta abrirla.
- **Archivos**, con `(nuevo)` o `(modifica)`.
- **Contrato**: el identificador del endpoint en `contrato-api-paridad.md`.
- **Esquema**.
- **Efectos secundarios**.
- **Pruebas**, con su caso, sus datos y el resultado esperado.
- **Terminado cuando**.
- **Riesgo** y cómo se mitiga.

### B.6 Escala de dificultad

| Nivel | Cuándo | Perfil de agente |
|---|---|---|
| **Baja** | Cambios locales en una o dos capas, sin esquema ni efectos en otras entidades. | Agente económico, sin supervisión |
| **Media** | Tres o más capas, esquema simple, efectos acotados. | Agente estándar |
| **Alta** | Transacciones multitabla, cascadas de estado, efectos en inventario o facturación, reversiones, esquema sobre datos existentes. | Agente capaz, con revisión humana del diff |
| **Muy alta** | Inventario y facturación a la vez, casos de borde históricos, conciliación o migración de datos. | Agente capaz, revisión humana y prueba con datos reales antes de cerrar la fase |

---

## C. Fases

### C.1 Fase 1 — Báscula al ritmo del legacy

> **Estado: ✅ COMPLETADA el 2026-09-30** (F1-01 a F1-09, implementados en `develop` en una sola pasada por indicación del usuario). `dotnet build Wms.sln` sin errores y `dotnet test Wms.Tests` en verde (440 pruebas; 323 antes de la fase).
> **Pendiente del usuario:** revisar el diff, generar las tres migraciones de la fase (`ParidadF1_02_IndiceDocumento`, `ParidadF1_06_ProductoDesdeBascula`, `ParidadF1_09_EfectivoYCambio`, §F.1) y hacer el commit.
> **Desviaciones respecto al texto de los ítems** (ninguna cambia una decisión de §A.4):
> 1. **F1-06 — nombre de más de 150 caracteres.** `products.name` mide 150 y la descripción admite 200: el nombre del producto creado se recorta a 150 y la clave de comparación se calcula sobre el nombre recortado, así la misma descripción reutiliza el producto. La línea del depósito guarda la descripción completa. Sin cambio de esquema.
> 2. **F1-06 — dos líneas del camión con el mismo producto.** El depósito tiene un índice único (depósito, producto): dos líneas del mismo registro que resuelven al mismo producto responden 400 «El producto «{nombre}» está repetido en la lista de productos del camión.» en lugar de un error de base de datos. Una línea de producto y una línea de unidad de carga con la misma descripción sí comparten el producto.
> 3. **F1-06 — la mercancía de las unidades no crea productos.** Una descripción en `cargoUnits[].products[]` se casa con las líneas del camión o con el catálogo; si no existe, responde el 400 actual «La mercancía de la unidad {placa} usa un producto que no está en la lista de productos del depósito.»
> 4. **F1-06 — comparación del nombre.** Se compara `upper(unaccent(name))` contra `upper(unaccent(N))`, equivalente a lo pedido y estable ante la configuración regional de la base.
> 5. **F1-07 — bloqueo D22.** `FindBlockReasonAsync` cuenta como atadura cualquier movimiento de inventario, y toda línea que entra por báscula tiene su movimiento `DeclaredEntry`: tal cual, P3 nunca se podría usar. El cambio de producto ignora ese movimiento (parámetro `ignoreDeclaredEntries`); recepción, levante, reserva, orden de cargue y los demás movimientos siguen bloqueando.
> 6. **F1-03 — exportador sin duplicar.** La comprobación es por (servicio, tercero, rol), que es el índice único de la tabla: un tercero que ya es cliente del depósito también puede quedar como exportador.
> 7. **F1-02 — documento cerrado.** El 409 de ingreso de camiones cerrado se evalúa cuando el buscador no encuentra un depósito abierto compatible (resultado «nuevo»), no solo cuando no hay ningún candidato abierto.
> 8. **F1-05 — reparto.** Un camión con alguna unidad sin mercancía ya queda señalado con `CARGO_UNIT_PRODUCTS`; su `CARGO_UNIT_BREAKDOWN` no se repite.
> 9. **Camión adicional con producto nuevo** (`InitiateStorageWeighingHandler`, paso 9): la línea nueva se agrega al contexto de forma explícita para que EF la inserte.
>
> **Hallazgo fuera de alcance, corregido el 2026-09-30 a pedido del usuario:** las líneas nuevas de una factura ya rastreada (recálculo del período abierto y consolidada existente) quedaban como `Modified` y el guardado fallaba con `DbUpdateConcurrencyException`. Se corrigió con `ValueGeneratedNever()` en `InvoiceItem.Id`, sin cambio de esquema. Ver §G.16.

- **Objetivo:** báscula registra un camión de importación solo con lo que tiene a mano (placa, documento, modalidad, mercancía y pesos), y Comercio Exterior completa y valida el resto al confirmar.
- **Criterio de salida (verificable):**
  1. `POST /api/v1/weighbridge/storage/register` crea el depósito (201) con solo: `entryLogId`, carta porte, modalidad `IMP`, una línea con descripción libre y cantidad del camión, y `configuredFirstWeightType`.
  2. Un segundo camión con la misma carta porte y **sin** fecha se asocia al mismo depósito (`isFirstTruck = false`).
  3. `POST .../warehouse-storages/{id}/confirm` responde 400 con la lista de lo que falta. Tras completar fecha, importador, agencia, moneda, valor y manifiesto de cada camión, confirma.
  4. `dotnet build` y `dotnet test` pasan en `develop`.
  5. Operativo, con el frontend: el cronometraje del roadmap 1.8 (no es backend).
- **Rama:** `develop` (§E).
- **Dificultad:** **Alta**. Cambia la validación y la asociación de camiones en el flujo más usado, mueve reglas a la confirmación y toca unidades de carga, que despachan por unidad.
- **Perfil de agente:** agente capaz, con revisión humana del diff.
- **Depende de:** nada. Es la primera fase.
- **Ítems sin backend:** BAS-02 (mercancía en línea), BAS-04 (peso en la misma pantalla), BAS-06 (tabulación) y 1.8 (cronometraje) son del frontend.

---

#### F1-01 · Campos de Comercio Exterior opcionales en báscula (BAS-01)

- **Dificultad:** Media.
- **Regla:**
  1. En `InitiateStorageWeighing` y `RegisterStorageEntry` **dejan de ser obligatorios**: fecha del documento, importador, agencia de aduanas (SIA), valor de la carga, moneda, número de manifiesto y peso del manifiesto. El exportador llega en F1-03 y también es opcional.
  2. **Siguen obligatorios** (reglas actuales, sin cambio):
     - carta porte (1 a 50 caracteres);
     - modalidad `IMP`, `EXP`, `INSP` o `INSP001`;
     - al menos una línea de producto, y al menos una con cantidad del camión mayor que 0 (WMS-25);
     - unidad de medida en cada línea;
     - cliente y rol juntos o ninguno;
     - tipo del primer peso cuando hay dos pesajes;
     - coherencia de depósito adicional y ciclo;
     - tipo de carga `LooseGoods` o `CargoUnits`.
  3. **Si vienen, se validan** (FluentValidation):

     | Campo | Condición | Mensaje |
     |---|---|---|
     | `documentDate` | ≤ ahora + 1 día (regla actual) | "La fecha del documento no puede ser futura." |
     | `manifestWeight` | > 0 | "El peso bruto según manifiesto debe ser mayor que cero." |
     | `manifestNumber` | ≤ 100 caracteres | "El número de manifiesto no puede exceder 100 caracteres." |
     | `cargoValue` | > 0 (regla actual) | "El valor de la carga debe ser mayor a cero." |
     | `currency` | COP o USD, sin distinguir mayúsculas; se guarda en mayúsculas | "La moneda debe ser COP o USD." |
     | pares id/rol de importador, agencia e intermediario | reglas actuales | mensajes actuales |

  4. El handler deja de lanzar "La fecha del documento comercial es requerida. Permite distinguir depósitos con el mismo número de documento en fechas distintas." (primer camión) y "La fecha del documento comercial es requerida." (depósito adicional).
  5. La entrada del camión guarda número y peso de manifiesto si vienen, como hoy. El `Manifest` del `EntryLog` solo se crea si viene el número (regla actual).
- **Evidencia:**
  - Legacy: `modulos/mod_bascula/registrarentradabascula.php:76-77` (el ingreso se crea `incompleto` con solo modalidad, fecha, documento, número, transportadora e importador nulo); `:118-141` (el pesaje guarda manifiesto y peso, que no son obligatorios: sin validador Spry, `:940-950`); `modulos/mod_ingresos/modificaringreso.php:84-106` (Comercio Exterior completa fecha del documento, manifiesto DIAN, SIA, importador, exportador, pesos, precio y moneda).
  - v2: `Wms.Application/Weighbridge/Commands/Storage/Initiate/InitiateStorageWeighingValidator.cs:52-62` (importador y agencia obligatorios en IMP), `:94-98` (peso obligatorio); `InitiateStorageWeighingHandler.cs:194-198` y `:808-810` (exige la fecha); `Register/RegisterStorageEntryValidator.cs:32-35`.
  - **Contradicción con el análisis:** `BASCULA_PARITY.md` dice que el legacy pedía el manifiesto en Comercio Exterior. El código muestra que báscula sí capturaba el manifiesto de la empresa y su peso, **como opcionales**, y que Comercio Exterior capturaba el manifiesto DIAN. El plan sigue al código: opcionales en báscula y exigidos al confirmar (F1-05).
- **Archivos:**
  - `Wms.Application/Weighbridge/Commands/Storage/Initiate/InitiateStorageWeighingValidator.cs` (modifica)
  - `Wms.Application/Weighbridge/Commands/Storage/Initiate/InitiateStorageWeighingHandler.cs` (modifica: quita las dos exigencias de fecha y normaliza la moneda)
  - `Wms.Application/Weighbridge/Commands/Storage/Register/RegisterStorageEntryValidator.cs` (modifica)
  - `Wms.Application/Weighbridge/Commands/Storage/Initiate/InitiateStorageWeighingCommand.cs` y `Wms.Application/Weighbridge/Common/Dtos/Requests/InitiateStorageWeighingRequest.cs` (modifica solo los comentarios XML que dicen «obligatorio»)
  - `Wms.Tests/Weighbridge/InitiateStorageWeighingValidatorTests.cs` y `Wms.Tests/Weighbridge/RegisterStorageEntryValidatorTests.cs` (modifica: `ManifestWeight_Null_IsRequired` pasa a comprobar que es opcional)
- **Contrato:** C-F1-01 y C-F1-02.
- **Esquema:** ninguno.
- **Efectos secundarios:** ninguno nuevo. Pueden nacer depósitos sin esos datos; F1-05 impide confirmarlos incompletos.
- **Pruebas** (`Wms.Tests/Weighbridge/`):

  | Caso | Datos | Resultado |
  |---|---|---|
  | IMP sin importador ni agencia | `OperationModalityCode = "IMP"`, sin `ImporterId` ni `ImportAgencyId` | sin errores en esas propiedades |
  | Peso nulo | `ManifestWeight = null` | válido |
  | Peso en el límite | `ManifestWeight = 0` y `ManifestWeight = -1` | error "El peso bruto según manifiesto debe ser mayor que cero." |
  | Peso mínimo | `ManifestWeight = 0.01` | válido |
  | Moneda | `"EUR"` → error "La moneda debe ser COP o USD."; `"usd"` → válido; `null` → válido | |
  | Fecha | `null` → válido; hoy + 2 días → error "La fecha del documento no puede ser futura." | |
  | Manifiesto largo | 101 caracteres → error; 100 → válido | |
  | Registro | `RegisterStorageEntryValidator` con `ManifestWeight = null` | válido |

- **Terminado cuando:** las pruebas pasan y una petición IMP sin fecha, importador, agencia, valor, moneda ni manifiesto crea el depósito en `Draft`.
- **Riesgo:** depósitos incompletos. Se mitiga con F1-04 (Comercio Exterior completa) y F1-05 (confirmar exige).

---

#### F1-02 · Identificación del documento sin fecha (BAS-01, decisión P1)

- **Dificultad:** Alta.
- **Regla:**
  1. **Clave del documento:**
     - número de carta porte normalizado (`Trim()` + mayúsculas);
     - `PrimaryDocumentTypeId` (un tipo nulo solo casa con otro nulo);
     - `ServiceType = Input`.
  2. **Candidatos:** los `ServiceRecord` con esa clave, `Status != Discarded`, `TruckEntriesClosedAt == null` y cuyo depósito (`WarehouseStorage` del servicio) está en `Draft` o `Confirmed`.
     - Un depósito `Cancelled` o `Closed` nunca es candidato.
     - Esto corrige un defecto: hoy un camión nuevo se puede pegar a un depósito anulado.
  3. **Selección** (función pura `StorageDocumentMatcher.Select(candidates, requestDate)`). Las fechas se comparan por **día calendario en Colombia** (`ColombiaTime.DateOf`).
     - **Sin fecha en la petición:**
       - 0 candidatos → depósito nuevo.
       - 1 candidato → el camión se asocia a él.
       - 2 o más → 409 "Hay {n} depósitos abiertos con el documento {número}: {números de depósito separados por coma}. Indique la fecha del documento para elegir el depósito."
     - **Con fecha:** se quedan los candidatos cuya fecha es la pedida **o es nula**.
       - 0 → depósito nuevo.
       - 1 → se asocia. Si ese candidato no tenía fecha, se le guarda la pedida con `ServiceRecord.UpdateDocumentDate` (nuevo, ver F1-04).
       - 2 o más → si exactamente uno tiene la fecha exacta, se asocia a ese; si no, 409 con el mensaje anterior.
  4. **Documento cerrado:** si no hay candidatos abiertos pero existe un servicio con la clave, fecha compatible (igual, nula en el servicio o no enviada) e ingreso de camiones cerrado, con su depósito sin anular, se responde 409:
     > "El ingreso de camiones del documento '{número}' fue cerrado por {nombre} el {dd/MM/yyyy HH:mm}. No se pueden asociar más camiones. Si es un documento nuevo, indique su fecha."

     La hora va en hora de Colombia. Si el servicio tiene fecha, después del número se agrega " con fecha '{dd/MM/yyyy}'".
  5. **Modalidad distinta:** se conserva el 409 actual. Si falta la fecha, se omite el tramo de fecha:
     > "El documento '{número}' ya tiene un depósito con modalidad '{código}'. No se puede asociar un camión con modalidad '{código}'."
  6. **Consultas de báscula:** `GET weighbridge/service-records/by-document` y `GET weighbridge/warehouse-storage/by-document` usan el mismo buscador.
     - Devuelven el candidato único, o `data: null` (200) si no hay.
     - Si hay varios, 409 con el mensaje del punto 3.
     - Hoy devuelven el primero sin orden (`FirstOrDefault`).
  7. **Respuesta de `storage/initiate` y `storage/register`:** llena `warehouseStorageNumber` también en el camino del primer camión y del camión adicional (hoy solo en el depósito adicional), para que báscula muestre a qué depósito quedó asociado.
  8. **Depósito adicional** (`isAdditionalDeposit = true`): no cambia. Siempre crea su propio servicio.
- **Evidencia:**
  - Legacy: `modulos/mod_bascula/seleccionardocumercial.php:13-19` (autocompleta por tipo y número, excluye anulados, sin fecha); `registrarentradabascula.php:542-556` (`ponerDocumercial` fija el `id_ingreso` elegido).
  - v2: `InitiateStorageWeighingHandler.cs:275-284` (clave con fecha exacta), `:316-347` (modalidad y WMS-26); `Wms.Application/Weighbridge/Queries/GetServiceRecordByDocument/GetServiceRecordByDocumentHandler.cs` (`FirstOrDefaultAsync` con fecha opcional); no se filtran depósitos anulados.
- **Archivos:**
  - `Wms.Application/Weighbridge/Common/Services/StorageDocumentMatcher.cs` (nuevo): `record DocumentCandidate(Guid ServiceRecordId, Guid WarehouseStorageId, string WarehouseStorageNumber, DateTimeOffset? DocumentDate, Guid OperationModalityId)`, `record DocumentMatch(DocumentMatchKind Kind, DocumentCandidate? Candidate, bool SetDocumentDate, IReadOnlyList<DocumentCandidate> Ambiguous)` y `enum DocumentMatchKind { New, Attach, Ambiguous }`.
  - `Wms.Application/Weighbridge/Common/Services/StorageDocumentLookup.cs` (nuevo, scoped): arma los candidatos con EF (`CargoManifestNumber.ToUpper() == numero`) y aplica el matcher. Registrar en `Wms.Application/DependencyInjection.cs`.
  - `Wms.Domain/Entities/Services/ServiceRecord.cs` (modifica): `UpdateDocumentDate(DateTimeOffset? documentDate)`; rechaza fechas futuras ("La fecha del documento no puede ser futura.").
  - `InitiateStorageWeighingHandler.cs` (modifica: usa `StorageDocumentLookup`).
  - `GetServiceRecordByDocumentHandler.cs` y `Wms.Application/Weighbridge/Queries/GetWarehouseStorageByDocument/GetWarehouseStorageByDocumentHandler.cs` (modifica).
  - `Wms.Application/Weighbridge/Common/Dtos/InitiateStorageResponseDto.cs` (sin cambio de forma; se llena el campo).
  - `Wms.Infrastructure/Persistence/Configurations/Services/ServiceRecordConfiguration.cs` (modifica: índice).
- **Contrato:** C-F1-01, C-F1-02 y C-F1-03.
- **Esquema:** índice no único `idx_service_records_document` sobre (`cargo_manifest_number`, `primary_document_type_id`).
- **Efectos secundarios:** al asociar con fecha a un servicio que no la tenía, se actualiza `service_records.document_date` (auditado).
- **Pruebas** (`Wms.Tests/Weighbridge/StorageDocumentMatcherTests.cs`, nuevo):

  | Caso | Candidatos | Fecha pedida | Resultado |
  |---|---|---|---|
  | a | ninguno | ninguna | `New` |
  | b | 1 (fecha nula) | ninguna | `Attach`, `SetDocumentDate = false` |
  | c | 1 (fecha nula) | 2026-09-20 | `Attach`, `SetDocumentDate = true` |
  | d | 2 (D1, D2) | ninguna | `Ambiguous` con los dos números |
  | e | 2 (uno 2026-09-20, otro nulo) | 2026-09-20 | `Attach` al de fecha exacta |
  | f | 2 (ambos nulos) | 2026-09-20 | `Ambiguous` |
  | g | 1 (2026-09-19) | 2026-09-20 | `New` |
  | h | 1 (`2026-09-29T04:30Z`, que es 28/09 en Colombia) | `2026-09-28T12:00-05:00` | `Attach` (mismo día en Colombia) |

  Además, en `Wms.Tests/Domain/Services/ServiceRecordTruckEntriesTests.cs` (modifica) o un archivo nuevo: `UpdateDocumentDate` con fecha de mañana → error; con fecha de hoy → la guarda.
- **Terminado cuando:**
  1. El segundo camión sin fecha se asocia al depósito abierto.
  2. Dos depósitos abiertos con el mismo número dan 409 con el mensaje exacto.
  3. Un depósito anulado con el mismo número no recibe el camión: se crea uno nuevo.
- **Riesgo:** asociar un camión al depósito equivocado. Se mitiga así: solo se consideran depósitos abiertos, el caso ambiguo da 409, la respuesta devuelve el número del depósito para que báscula lo muestre, y queda la auditoría.

---

#### F1-03 · Exportador en báscula y en Comercio Exterior (BAS-01)

- **Dificultad:** Media.
- **Regla:**
  1. `storage/initiate` y `storage/register` aceptan `exporterId` y `exporterRoleId`.
     - Van juntos o ninguno: "Si proporciona el exportador, debe proporcionar su rol."
     - Deben ser GUID válidos: "El Id del exportador no es válido." / "El rol del exportador no es válido."
     - El tercero debe existir: 404 "El exportador no existe."
     - Se guarda como `ServiceRecordStakeholder` con ese rol, sin duplicar si ya está (mismo patrón del importador).
     - Aplica al primer camión, al camión adicional y al depósito adicional.
  2. `PUT foreign-trade/warehouse-storages/{id}/stakeholders` admite el rol `EXPORTER`, además de `IMPORTER`, `CUSTOMS_AGENCY` y `TRANSPORT_COMPANY`. El mensaje de rol no admitido pasa a: "Rol '{rol}' no admitido. Roles válidos: IMPORTER, EXPORTER, CUSTOMS_AGENCY, TRANSPORT_COMPANY."
  3. **Corrige un defecto:** hoy el frontend envía `exporterId`, el backend lo descarta y Comercio Exterior no puede asignarlo. La etiqueta de exportación, que imprime el exportador, sale vacía.
- **Evidencia:**
  - Legacy: `modulos/mod_ingresos/modificaringreso.php:84-106` (guarda `id_exportador`), `:404-407` (campo del formulario).
  - v2: `InitiateStorageWeighingCommand.cs` (sin exportador); `Wms.Application/ForeignTrade/Commands/UpdateDepositStakeholders/UpdateDepositStakeholdersHandler.cs:24-25` (roles admitidos); `Wms.Application/ForeignTrade/Common/Services/LabelGenerationService.cs:286,490` (la etiqueta usa `EXPORTER`); `Frontend/wms/app/features/weighbridge/components/StorageServiceForm.vue:901-902` (el frontend ya lo envía).
- **Archivos:**
  - `InitiateStorageWeighingCommand.cs`, `InitiateStorageWeighingRequest.cs`, `RegisterStorageEntryCommand.cs`, `Wms.Application/Weighbridge/Common/Dtos/Requests/RegisterStorageEntryRequest.cs` y `RegisterStorageEntryHandler.cs` (el mapeo a Initiate): modifica.
  - `Wms.Api/Controllers/v1/WeighbridgeController.cs` (modifica: mapeo en `storage/initiate` y `storage/register`).
  - `InitiateStorageWeighingValidator.cs` e `InitiateStorageWeighingHandler.cs` (modifica, en los tres caminos).
  - `Wms.Application/ForeignTrade/Common/Services/DepositStakeholderRoles.cs` (nuevo): `public static readonly IReadOnlySet<string> Manageable` y `IsManageable(string code)`.
  - `UpdateDepositStakeholdersHandler.cs` (modifica: usa `DepositStakeholderRoles`).
  - `Wms.Api/Controllers/v1/Requests/UpdateDepositStakeholdersRequest.cs` (modifica solo el comentario).
- **Contrato:** C-F1-01, C-F1-02 y C-F1-04.
- **Esquema:** ninguno. El rol `EXPORTER` ya está sembrado.
- **Efectos secundarios:** la etiqueta de exportación muestra el exportador.
- **Pruebas:**
  - Validador: `ExporterId` sin rol → error; ambos presentes y válidos → sin error; ninguno → sin error.
  - `DepositStakeholderRoles.IsManageable("EXPORTER")` → true; `"exporter"` → true; `"CUSTOMER"` → false.
- **Terminado cuando:** un depósito EXP registrado con exportador lo muestra en su detalle y en su etiqueta, y Comercio Exterior puede cambiarlo en Borrador.
- **Riesgo:** bajo.

---

#### F1-04 · Comercio Exterior completa la fecha del documento y el manifiesto de cada camión (BAS-01, P2)

- **Dificultad:** Media.
- **Regla A — fecha del documento:**
  1. `PATCH foreign-trade/warehouse-storages/{id}/draft` acepta `documentDate` (opcional). Solo en Borrador, como el resto del endpoint.
  2. Si viene:
     - No futura (día en Colombia ≤ hoy): 400 "La fecha del documento no puede ser futura."
     - Si otro depósito abierto con la misma clave (número normalizado + tipo) tiene la misma fecha (día en Colombia): 409 "Ya existe un depósito abierto con el documento {número} y fecha {dd/MM/yyyy}: {número de depósito}."
     - Se guarda con `ServiceRecord.UpdateDocumentDate`.
- **Regla B — manifiesto de cada camión:**
  1. Endpoint nuevo `PATCH foreign-trade/warehouse-storages/{id}/entries/{entryId}/manifest` con `manifestNumber` (1 a 100 caracteres), `manifestWeight` (> 0) y `reason` (opcional, hasta 500).
  2. Estado: Borrador o Confirmado. Si no: 400 "Solo se puede completar el manifiesto de un depósito en Borrador o Confirmado."
  3. El camión debe ser del depósito: 404 "El camión no pertenece a este depósito."
  4. Efecto, en una transacción:
     - `WarehouseStorageEntry.UpdateManifest(number, weight)` (nuevo).
     - El `Manifest` del `EntryLog` del camión: si existe uno con el número anterior o con el nuevo, se actualiza con `Manifest.Update`; si no, se crea con `Manifest.Create`.
     - Auditoría: `Describe("Manifiesto del camión {placa} del depósito {n}: {número anterior o 'sin número'} / {peso anterior o 'sin peso'} kg → {número} / {peso} kg. Motivo: {motivo o 'sin motivo'}")`.
  5. Si el depósito está Confirmado y el peso cambió, después del commit: `StorageRecalculationTrigger.RecalculateAsync(storageId, "corrección del manifiesto del camión {placa}")`. El peso alimenta las tarifas por peso (`StorageBillingService.cs:87-91`).
- **Regla C — aviso del camión tardío:** cuando un camión se asocia a un depósito ya Confirmado sin número o sin peso de manifiesto, el aviso actual a Comercio Exterior («Camión adicional en depósito confirmado») agrega al final: " Falta el número o el peso del manifiesto de este camión: complételo en el detalle del depósito."
- **Evidencia:**
  - Legacy: `modulos/mod_ingresos/modificaringreso.php:84-106` (Comercio Exterior completa la fecha del documento y el manifiesto); `registrarentradabascula.php:118-141` (manifiesto y peso opcionales en báscula).
  - v2: `Wms.Application/ForeignTrade/Commands/UpdateDraftDeposit/UpdateDraftDepositCommand.cs` (sin fecha); `Wms.Domain/Entities/Services/ServiceRecord.cs` (sin método para la fecha); `Wms.Domain/Entities/Warehouse/WarehouseStorageEntry.cs` (sin método para el manifiesto); `Wms.Application/Billing/Common/Services/StorageRecalculationTrigger.cs:41-80` (aviso del camión tardío).
- **Archivos:**
  - `WarehouseStorageEntry.cs` (modifica: `UpdateManifest`).
  - `ServiceRecord.cs` (modifica: `UpdateDocumentDate`, compartido con F1-02).
  - `UpdateDraftDepositCommand.cs`, `UpdateDraftDepositCommandValidator.cs` y `UpdateDraftDepositHandler.cs` (modifica).
  - `Wms.Api/Controllers/v1/ForeignTradeController.cs` (modifica: el record `UpdateDraftDepositRequest` agrega `DocumentDate` y el mapeo).
  - `Wms.Application/ForeignTrade/Commands/UpdateTruckManifest/UpdateTruckManifestCommand.cs`, `UpdateTruckManifestCommandValidator.cs` y `UpdateTruckManifestCommandHandler.cs` (nuevos).
  - `Wms.Api/Controllers/v1/DepositCompletionController.cs` (nuevo; `[Route("foreign-trade")]`, `[Authorize(Policy = "ForeignTradeAccess")]`).
  - `Wms.Api/Controllers/v1/Requests/DepositCompletionRequests.cs` (nuevo).
  - `StorageRecalculationTrigger.cs` (modifica: `HandleLateTruckAsync(..., bool manifestMissing)`).
  - `InitiateStorageWeighingHandler.cs` (modifica: pasa `manifestMissing`).
- **Contrato:** C-F1-05 (draft, modificado) y C-F1-06 (manifiesto, nuevo).
- **Esquema:** ninguno. Las columnas ya existen.
- **Efectos secundarios:** recálculo de la factura del período abierto si cambia el peso de un depósito Confirmado; notificaciones de recálculo actuales a Facturación.
- **Pruebas** (`Wms.Tests/Domain/Warehouse/WarehouseStorageEntryManifestTests.cs`, nuevo):

  | Caso | Resultado |
  |---|---|
  | `UpdateManifest("", 100)` | error "El número de manifiesto es requerido." |
  | número de 101 caracteres | error "El número de manifiesto no puede exceder 100 caracteres." |
  | peso 0 | error "El peso del manifiesto debe ser mayor que cero." |
  | peso 0.01 | válido |
  | `(" MAN-1 ", 12500)` | guarda `"MAN-1"` y 12500; actualiza `UpdatedAt` |

  Validador de `UpdateTruckManifest` con motivo de 501 caracteres → error "El motivo no puede exceder 500 caracteres."
- **Terminado cuando:** Comercio Exterior completa la fecha y el manifiesto de cada camión, y el depósito queda listo para F1-05.
- **Riesgo:** que los dos lugares donde vive el manifiesto (entrada y `Manifest`) diverjan. Se actualizan en la misma transacción.

---

#### F1-05 · Requisitos para confirmar el depósito (BAS-01, P2, P5)

- **Dificultad:** Media.
- **Regla:**
  1. `ConfirmStorageDeposit` evalúa, **antes** de abrir la transacción, todos los requisitos. Si falta alguno, responde 400 con la lista completa, en este orden y separada por "; ":
     > "No se puede confirmar el depósito {número}. Falta: {elemento}; {elemento}; …."

     | # | Condición | Código | Texto en la lista |
     |---|---|---|---|
     | 1 | `CustomerId` nulo | `CUSTOMER` | cliente |
     | 2 | `ServiceRecord.DocumentDate` nula | `DOCUMENT_DATE` | fecha del documento |
     | 3a | Modalidad IMP* sin tercero con rol `IMPORTER` | `IMPORTER` | importador |
     | 3b | Modalidad IMP* sin tercero con rol `CUSTOMS_AGENCY` | `CUSTOMS_AGENCY` | agencia de aduanas |
     | 3c | Modalidad EXP* sin tercero con rol `EXPORTER` | `EXPORTER` | exportador |
     | 4 | `Currency` nula o vacía | `CURRENCY` | moneda |
     | 5 | `CargoValue` nulo o ≤ 0 | `CARGO_VALUE` | valor de la mercancía |
     | 6 | Por cada camión (entrada) del depósito, por orden de llegada, con `ManifestNumber` vacío | `MANIFEST_NUMBER` | número de manifiesto del camión {placa} |
     | 7 | Mismo camión con `ManifestWeight` nulo o ≤ 0 | `MANIFEST_WEIGHT` | peso del manifiesto del camión {placa} |
     | 8 | Depósito `CargoUnits`: unidad sin líneas | `CARGO_UNIT_PRODUCTS` | mercancía de la unidad de carga {placa de la unidad} |
     | 9 | Depósito `CargoUnits`: por camión y producto, la suma de las unidades ≠ lo declarado del camión (tolerancia 0,0001) | `CARGO_UNIT_BREAKDOWN` | reparto de {producto} en las unidades del camión {placa} |

     - INSP* no exige importador, agencia ni exportador.
     - La placa del camión es `VehiclePlate`, o "sin placa".
     - A partir de F3-09 se excluyen los camiones anulados.
     - El mensaje actual "El depósito debe tener un cliente asignado para poder confirmarse." se reemplaza por el mensaje unificado, donde el cliente es el primer elemento.
  2. Consulta nueva `GET foreign-trade/warehouse-storages/{id}/confirmation-requirements`, que usa el mismo evaluador. Devuelve `{ warehouseStorageId, warehouseStorageNumber, canConfirm, missing: [{ code, message }] }`, con los códigos de la tabla. El frontend la usa para mostrar lo que falta antes de confirmar.
  3. El evaluador es puro: `DepositConfirmationRequirements.Evaluate(DepositConfirmationSnapshot)` → `IReadOnlyList<MissingRequirement>`. El handler arma el snapshot con los terceros (y sus roles), las entradas, las unidades y sus líneas.
- **Evidencia:**
  - Legacy: `modificaringreso.php` (Comercio Exterior completa sin validación); la decisión P2 lleva la exigencia a la confirmación.
  - v2: `Wms.Application/ForeignTrade/Commands/ConfirmStorageDeposit/ConfirmStorageDepositHandler.cs:48-51` (solo exige cliente).
- **Archivos:**
  - `Wms.Application/ForeignTrade/Common/Services/DepositConfirmationRequirements.cs` (nuevo; incluye `DepositConfirmationSnapshot`, `TruckSnapshot`, `CargoUnitSnapshot` y `MissingRequirement(string Code, string Message)`).
  - `ConfirmStorageDepositHandler.cs` (modifica).
  - `Wms.Application/ForeignTrade/Queries/GetConfirmationRequirements/GetConfirmationRequirementsQuery.cs` y `GetConfirmationRequirementsHandler.cs` (nuevos).
  - `Wms.Application/ForeignTrade/Common/DTOs/ConfirmationRequirementsDto.cs` (nuevo).
  - `DepositCompletionController.cs` (modifica).
- **Contrato:** C-F1-07 (confirm, errores nuevos) y C-F1-08 (requisitos, nuevo).
- **Esquema:** ninguno.
- **Efectos secundarios:** ninguno nuevo. Si confirma, abre el período y la factura como hoy.
- **Pruebas** (`Wms.Tests/ForeignTrade/DepositConfirmationRequirementsTests.cs`, nuevo):

  | Caso | Resultado |
  |---|---|
  | IMP completo | lista vacía |
  | IMP sin importador ni agencia | `[IMPORTER, CUSTOMS_AGENCY]` en ese orden |
  | EXP sin exportador | `[EXPORTER]` |
  | INSP sin terceros documentales | sin `IMPORTER`, `CUSTOMS_AGENCY` ni `EXPORTER` |
  | Moneda `""` y valor 0 | `[CURRENCY, CARGO_VALUE]` |
  | Camión A completo; camión B (placa ABC123) sin peso | `[MANIFEST_WEIGHT]` con el texto "peso del manifiesto del camión ABC123" |
  | `CargoUnits` con una unidad sin líneas | `CARGO_UNIT_PRODUCTS` |
  | Camión con 10 declarados y unidades que suman 9 | `CARGO_UNIT_BREAKDOWN` |
  | Sin cliente ni fecha | el mensaje unificado empieza por "No se puede confirmar el depósito 2026BA00001. Falta: cliente; fecha del documento" |

- **Terminado cuando:** confirmar falla con la lista exacta y funciona cuando todo está completo; la consulta devuelve lo mismo que el error.
- **Riesgo:** los depósitos en Borrador creados antes del cambio quedan bloqueados hasta completarlos. Es aceptable (base de pruebas recreable) y se resuelve con F1-03 y F1-04.

---

#### F1-06 · Producto por descripción libre en báscula (BAS-03, P3)

- **Dificultad:** Media.
- **Regla:**
  1. Cada línea (`products[]`) trae `productId` (GUID del catálogo) **o** `productDescription`.
     - Con `productId`: debe existir (404 "El producto con Id '{id}' no existe.").
     - Sin `productId`: la descripción es obligatoria y tiene de 3 a 200 caracteres tras recortar: "La descripción del producto debe tener entre 3 y 200 caracteres."
  2. **Resolución de la descripción** (`WeighbridgeProductResolver`, dentro de la transacción del registro, **antes** de validar las unidades de carga):
     1. Nombre normalizado `N = CatalogNameNormalizer.ForComparison(descripción)`: recorta, deja un solo espacio entre palabras, quita tildes y diacríticos (NFD sin marcas `NonSpacingMark`) y pasa a mayúsculas invariantes.
     2. Busca productos cuyo `unaccent(upper(name))` sea igual a N, con `EF.Functions.Unaccent(p.Name.ToUpper()) == N` (la extensión `unaccent` ya está instalada). Si hay varios, se prefiere el activo; entre activos, el de `CreatedAt` más antiguo.
     3. Si no hay ninguno, crea el producto (`Product.CreateFromWeighbridge`, nuevo):
        - `Name` = la descripción recortada, con espacios colapsados y en mayúsculas.
        - `Sku` = "BAS-" + 8 caracteres hexadecimales en mayúsculas de un `Guid` nuevo. Si choca con un SKU existente, genera otro; tras 3 intentos, 409 "No se pudo generar un SKU único para el producto; intente de nuevo."
        - `UnitMeasureId` = la unidad de la línea, que debe estar activa (regla actual `UnitMeasureGuard`).
        - `PackagingTypeId` = el embalaje de la línea; `Description` = null; `CreatedFromWeighbridge = true`.
        - Dos líneas del mismo registro con la misma N usan un solo producto.
     4. La línea del depósito guarda el `ProductId` resuelto y `ProductDescription` = el texto original de la línea.
  3. Las líneas de las unidades de carga (`cargoUnits[].products[]`) identifican el producto por `productId` **o** por `productDescription` (campo nuevo), se resuelven igual y se casan con la línea de producto por el `ProductId` resuelto.
  4. La respuesta incluye `createdProducts: [{ productId, name, sku }]` (vacío si no se creó ninguno).
  5. Si se creó algún producto, después del commit se notifica a `ForeignTrade`:
     - Nivel `Info`, título "Producto creado desde báscula", tipo `WarehouseStorage` con el id del depósito.
     - Mensaje: "Báscula creó el producto «{nombre}» (SKU {sku}) en el depósito {número}. Revíselo y, si ya existía con otro nombre, cambie el producto de la línea."
- **Evidencia:**
  - Legacy: `registrarentradabascula.php:124-141` (`descripcionproducto` en texto libre), `:887` (campo de texto libre que pasa a mayúsculas).
  - v2: `InitiateStorageWeighingHandler.cs:177-192` y `:821-835` (exige GUID y que exista); `Wms.Domain/Entities/Warehouse/WarehouseStorageProduct.cs:57-58`; `InitiateStorageWeighingValidator.cs:122-128` (el validador ya admite la descripción; el handler no).
- **Archivos:**
  - `Wms.Common/Text/CatalogNameNormalizer.cs` (nuevo).
  - `Wms.Domain/Entities/Product/Product.cs` (modifica: `CreatedFromWeighbridge` y `CreateFromWeighbridge(name, sku, unitMeasureId, packagingTypeId)`).
  - `Wms.Infrastructure/Persistence/Configurations/Product/ProductConfiguration.cs` (modifica).
  - `Wms.Application/Products/Common/Dtos/ProductDto.cs` y su mapper (modifica: expone `CreatedFromWeighbridge`).
  - `Wms.Application/Products/Queries/GetAllProducts/GetAllProductsQuery.cs` y su handler (modifica: filtro opcional `CreatedFromWeighbridge`).
  - `Wms.Application/Weighbridge/Common/Dtos/Requests/StorageProductItemDto.cs` (modifica: `ProductId` pasa a `string?`).
  - `Wms.Application/Weighbridge/Common/Dtos/Requests/StorageCargoUnitItemDto.cs` (modifica: en la línea, `ProductId` pasa a `string?` y se agrega `ProductDescription`).
  - `Wms.Application/Weighbridge/Common/Services/WeighbridgeProductResolver.cs` (nuevo, scoped; registrar en DI).
  - `InitiateStorageWeighingHandler.cs` (modifica: resuelve en los tres caminos y después pasa por `CargoUnitDeclaration`).
  - `InitiateStorageWeighingValidator.cs` (modifica: la regla de la descripción).
  - `InitiateStorageResponseDto.cs` (modifica: `CreatedProducts`).
- **Contrato:** C-F1-01, C-F1-02 y C-F1-09 (`GET product`, filtro nuevo).
- **Esquema:** `products.created_from_weighbridge boolean NOT NULL DEFAULT false`.
- **Efectos secundarios:** altas en `products` (auditadas); notificación a Comercio Exterior.
- **Pruebas:**
  - `Wms.Tests/Common/CatalogNameNormalizerTests.cs` (nuevo): `"  cebolla   paiteña "` → `"CEBOLLA PAITENA"`; `"ÁRBOL"` → `"ARBOL"`; `null` → `""`.
  - Formato del SKU: cumple `^BAS-[0-9A-F]{8}$`.
  - `Product.CreateFromWeighbridge` con `unitMeasureId = Guid.Empty` → error "La unidad de medida es requerida."
  - Validador: línea sin id con descripción de 2 caracteres → error; de 3 → válida; de 201 → error.
  - Deduplicación pura del resolvedor: `["Cebolla", " cebolla "]` → una sola clave.
- **Terminado cuando:** una línea "Cebolla roja" que no existe crea el producto "CEBOLLA ROJA" y el depósito, y un segundo camión con "cebolla  roja" reutiliza ese producto.
- **Riesgo:** el catálogo se llena de variantes. Se mitiga con la marca `CreatedFromWeighbridge`, el filtro para revisarlas y F1-07 (cambiar el producto de la línea).

---

#### F1-07 · Comercio Exterior cambia el producto de una línea (BAS-03, P3)

- **Dificultad:** Media.
- **Regla:** `PUT foreign-trade/deposits/{id}/products/{storageProductId}/catalog-product` con `productId` y `reason`.

  | Condición | Respuesta |
  |---|---|
  | Depósito que no está en Borrador | 400 "Solo se pueden editar los productos de un depósito en Borrador." (`EnsureProductsAreEditable`) |
  | La línea no es del depósito | 404 "El producto no existe en este depósito." |
  | Producto nuevo inexistente o inactivo | 404 "El producto del catálogo no existe o está inactivo." |
  | Producto nuevo igual al actual | 400 "La línea ya tiene ese producto." |
  | Otra línea del depósito ya tiene ese producto | 409 "El producto «{nombre}» ya tiene una línea en este depósito; corrija esa línea en lugar de cambiar esta." |
  | La línea está atada a recepción, levante o guía (bloqueo D22 actual, `DepositProductDependencies.FindBlockReasonAsync`) | 400 "No se puede cambiar el producto: la línea {motivo}." |
  | Motivo fuera de rango | 400 "El motivo del cambio debe tener entre 10 y 500 caracteres." |

  - **Efecto:** `WarehouseStorageProduct.ChangeProduct(Guid productId)` (nuevo). Solo cambia `ProductId`: cantidades, descripción, unidad y embalaje se conservan. Las líneas por camión y por unidad apuntan a la línea, no al producto, así que no cambian.
  - **Auditoría:** `Describe("Cambio de producto de la línea «{anterior}» → «{nuevo}» del depósito {n}. Motivo: {motivo}")`.
  - **Después del commit:** `DepositProductEditing.AfterCommitAsync` (recalcula la factura si el depósito tenía un período abierto y fue devuelto a corrección).
- **Evidencia:**
  - v2: `Wms.Application/ForeignTrade/Commands/UpdateDepositProduct/UpdateDepositProductCommand.cs` (no permite cambiar el producto); `Wms.Application/ForeignTrade/Common/Services/DepositProductEditing.cs`.
- **Archivos:**
  - `WarehouseStorageProduct.cs` (modifica).
  - `Wms.Application/ForeignTrade/Commands/ChangeDepositLineProduct/ChangeDepositLineProductCommand.cs`, `ChangeDepositLineProductCommandValidator.cs` y `ChangeDepositLineProductCommandHandler.cs` (nuevos).
  - `DepositCompletionController.cs` (modifica). La ruta tiene un segmento más que las existentes `deposits/{id}/products/{productId}`, así que no choca.
- **Contrato:** C-F1-10.
- **Esquema:** ninguno.
- **Efectos secundarios:** auditoría; recálculo posible.
- **Pruebas:** `ChangeProduct(Guid.Empty)` → error "El producto es requerido."; con el mismo id → error "La línea ya tiene ese producto."; con un id válido distinto → cambia `ProductId` y `UpdatedAt`.
- **Terminado cuando:** Comercio Exterior cambia la línea "CEBOLLA ROJA" por el producto "CEBOLLA" del catálogo, en Borrador.
- **Riesgo:** una tarifa distinta por producto. Se mitiga con el recálculo después del commit.

---

#### F1-08 · Unidades de carga sin desglose en báscula (BAS-07, P5)

- **Dificultad:** Alta.
- **Regla** (tipo de carga `CargoUnits`):
  1. Cada unidad trae tipo y placa (reglas actuales). Su lista `products` pasa a ser opcional.
  2. **Todas o ninguna:** todas las unidades del camión traen mercancía, o ninguna. Mezcla → 400 "Declare la mercancía en todas las unidades de carga del camión o en ninguna."
  3. **Con mercancía en todas:** regla actual. Cada línea > 0, cada producto del camión en alguna unidad, y los totales del camión son la suma de las unidades.
  4. **Sin mercancía en ninguna:** los totales del camión salen de `products[].entryDeclaredQuantity`, como en mercancía suelta (al menos una > 0, regla WMS-25).
     - **Una sola unidad:** se le asigna automáticamente cada producto del camión con cantidad > 0: una línea por producto, con la cantidad del camión.
     - **Dos o más unidades:** las unidades se crean sin mercancía. Solo se permite si el depósito no está Confirmado. Si ya lo está → 400 "El depósito {número} ya está confirmado: declare la mercancía de cada unidad de carga de este camión."
  5. **Comercio Exterior reparte en Borrador** con `PUT foreign-trade/warehouse-storages/{id}/entries/{entryId}/cargo-unit-breakdown`, que recibe `units: [{ warehouseStorageCargoUnitId, products: [{ warehouseStorageProductId, declaredQuantity }] }]` y `reason`.

     | Condición | Respuesta |
     |---|---|
     | Depósito que no está en Borrador | 400 "Solo se pueden editar los productos de un depósito en Borrador." |
     | El camión no es del depósito | 404 "El camión no pertenece a este depósito." |
     | Unidad de otro camión | 400 "La unidad de carga {placa} no pertenece al camión indicado." |
     | No vienen todas las unidades del camión | 400 "Envíe el reparto de todas las unidades de carga del camión." |
     | Unidad sin líneas | 400 "La unidad de carga {placa} no tiene mercancía." |
     | Cantidad ≤ 0 | 400 "La cantidad declarada de la unidad {placa} debe ser mayor a cero." |
     | Producto repetido en una unidad | 400 "El producto está repetido en la unidad {placa}." |
     | Producto que no está en el camión | 400 "«{producto}» no está declarado en este camión." |
     | Por producto, suma de las unidades ≠ declarado del camión (tolerancia 0,0001) | 400 "La suma de «{producto}» en las unidades ({x}) no coincide con lo declarado del camión ({y})." |
     | Motivo fuera de rango | 400 "El motivo debe tener entre 10 y 500 caracteres." |

     - **Efecto:** reemplaza las líneas de las unidades de ese camión con `WarehouseStorageCargoUnit.ReplaceProducts(lines)` (nuevo), que rechaza si alguna línea tiene reservado o despachado > 0: "No se puede cambiar la mercancía de la unidad {placa}: tiene cantidades reservadas o despachadas." En Borrador no puede haber reservas.
     - No cambia las cantidades del camión ni el stock. Auditoría con motivo.
  6. Confirmar exige el reparto completo (F1-05, filas 8 y 9).
- **Evidencia:**
  - Legacy: `registrarentradabascula.php:866,873-878` (el selector de unidad de carga está **comentado**: el legacy no la capturaba en báscula).
  - v2: `Wms.Application/Weighbridge/Common/Services/CargoUnitDeclaration.cs:24-69`; `InitiateStorageWeighingHandler.cs:40-58` y `:1238-1272`; `Wms.Application/ForeignTrade/Commands/AddDepositProduct/AddDepositProductCommandHandler.cs:38-49` (Comercio Exterior agrega a una unidad pero suma al camión: no sirve para repartir).
- **Archivos:**
  - `CargoUnitDeclaration.cs` (modifica): `Validate` devuelve `CargoUnitDeclarationMode { WithProducts, AutoAssignSingleUnit, EmptyUnits }`.
  - `InitiateStorageWeighingHandler.cs` (modifica `AddCargoUnitsAsync`: asigna automáticamente o crea vacías; rechaza vacías en depósitos Confirmados).
  - `Wms.Domain/Entities/Warehouse/WarehouseStorageCargoUnit.cs` (modifica: `ReplaceProducts`).
  - `Wms.Application/ForeignTrade/Commands/SetCargoUnitBreakdown/SetCargoUnitBreakdownCommand.cs`, `SetCargoUnitBreakdownCommandValidator.cs` y `SetCargoUnitBreakdownCommandHandler.cs` (nuevos).
  - `Wms.Application/ForeignTrade/Common/Services/CargoUnitBreakdown.cs` (nuevo, puro).
  - `DepositCompletionController.cs` (modifica).
  - La respuesta reutiliza `Wms.Application/Warehouse/Common/DTOs/CargoUnitDto.cs` y `CargoUnitProjection`.
- **Contrato:** C-F1-01, C-F1-02 y C-F1-11.
- **Esquema:** ninguno.
- **Efectos secundarios:** unidades sin líneas hasta el reparto; auditoría.
- **Pruebas:**
  - `Wms.Tests/Weighbridge/CargoUnitDeclarationTests.cs` (modifica):

    | Caso | Resultado |
    |---|---|
    | Todas con líneas | `WithProducts` (comportamiento actual) |
    | Ninguna con líneas y una unidad | `AutoAssignSingleUnit` |
    | Ninguna con líneas y dos unidades | `EmptyUnits` |
    | Mezcla | error con el mensaje exacto |

  - `Wms.Tests/ForeignTrade/CargoUnitBreakdownTests.cs` (nuevo):

    | Caso | Resultado |
    |---|---|
    | 10 declarados, unidades 5 + 5 | válido |
    | 10 declarados, unidades 5 + 4 | error "La suma de «CEBOLLA» en las unidades (9) no coincide con lo declarado del camión (10)." |
    | Producto extra en una unidad | error |
    | Cantidad 0 | error |
    | 1 declarado, una unidad con 1 | válido |

  - `ReplaceProducts` sobre una línea con reservado 1 → error.
- **Terminado cuando:** un camión con un contenedor y sin desglose queda con la línea automática; con dos contenedores, Comercio Exterior reparte y confirmar se bloquea hasta hacerlo.
- **Riesgo:** el despacho por unidad (D27) necesita las líneas por unidad. Queda garantizado porque confirmar las exige y porque un camión tardío a un depósito confirmado debe traer el desglose.

---

#### F1-09 · Efectivo recibido y cambio en el cobro de báscula (BAS-05, GAP-024 b, P4)

- **Dificultad:** Media.
- **Regla:**
  1. `storage/process-payment`, `weighing-only/process-payment` y `output/process-payment` aceptan `cashReceived` (decimal, opcional).
  2. Solo aplica con el método `Cash`. Con otro método → 400 "El efectivo recibido solo aplica a pagos en efectivo."
  3. Si viene, debe ser ≥ el total a pagar (`amountReceived`, que en estos endpoints es el total). Si no → 400 "El efectivo recibido ({x:N0}) es menor que el total a pagar ({y:N0})."
  4. Cambio = `cashReceived − total`, redondeado a 2 decimales.
  5. Se guardan en el pago (`InvoicePayment.CashReceived` y `InvoicePayment.ChangeGiven`, nuevos, con el método `RegisterCash(decimal cashReceived, decimal total)`). La respuesta llena `changeAmount` (hoy siempre 0) y el campo nuevo `cashReceived`.
  6. Sin `cashReceived`, ambos quedan nulos y `changeAmount = 0`, como hoy.
  7. El depósito adicional en $0 (caso B) ignora el efectivo.
  8. Los DTO de pagos exponen `cashReceived` y `changeGiven`: `InvoicePaymentDto` de facturación y la clase `InvoicePaymentDto` del detalle del ciclo.
- **Evidencia:**
  - Legacy: `modulos/mod_bascula/facturar.php:71-72` (la factura guarda pago y cambio), `:100` (el recibo guarda pago y cambio), `:152-157` (cálculo del cambio).
  - v2: `Wms.Domain/Entities/Billing/InvoicePayment.cs` (sin esos campos); `Wms.Application/Weighbridge/Commands/Storage/ProcessPayment/ProcessStoragePaymentHandler.cs:164-166` (`changeAmount = 0`).
- **Archivos:**
  - `InvoicePayment.cs` (modifica).
  - `Wms.Infrastructure/Persistence/Configurations/Billing/InvoicePaymentConfiguration.cs` (modifica).
  - `Wms.Application/Weighbridge/Commands/{Storage,WeighingOnly,Output}/ProcessPayment/*Command.cs`, `*Validator.cs` y `*Handler.cs` (modifica).
  - `Wms.Application/Weighbridge/Common/Dtos/Requests/Process{Storage,WeighingOnly,Output}PaymentRequest.cs` (modifica).
  - `WeighbridgeController.cs` (modifica: mapeo).
  - `Wms.Application/Weighbridge/Common/Dtos/ProcessPaymentResponseDto.cs` (modifica: `CashReceived`).
  - `Wms.Application/Weighbridge/Common/Services/CashChangeCalculator.cs` (nuevo, puro).
  - `Wms.Application/Billing/Common/DTOs/InvoiceDto.cs` (`InvoicePaymentDto`), `Wms.Application/Weighbridge/Common/Dtos/WeighbridgeCycleDetailDto.cs` (`InvoicePaymentDto`) y sus mappers (modifica).
- **Contrato:** C-F1-12.
- **Esquema:** `invoice_payments.cash_received numeric(18,2) NULL` e `invoice_payments.change_given numeric(18,2) NULL`.
- **Efectos secundarios:** ninguno más.
- **Pruebas** (`Wms.Tests/Weighbridge/CashChangeCalculatorTests.cs`, nuevo):

  | Total | Efectivo | Resultado |
  |---|---|---|
  | 23 000 | 50 000 | cambio 27 000 |
  | 23 000 | 23 000 | cambio 0 |
  | 23 000 | 22 999 | error con el mensaje exacto |
  | 23 000 | −1 | error "El efectivo recibido no puede ser negativo." |

  Validador: método `BankTransfer` con `cashReceived` → error "El efectivo recibido solo aplica a pagos en efectivo."
- **Terminado cuando:** pagar 23 000 con 50 000 devuelve `changeAmount = 27000` y guarda ambos valores.
- **Riesgo:** bajo.

---

### C.2 Fase 2 — Control aduanero

> **Estado: ✅ COMPLETADA el 2026-09-30** (F2-01 a F2-10, implementados en `develop` en una sola pasada por indicación del usuario). `dotnet build Wms.sln` sin errores y `dotnet test Wms.Tests` en verde (540 pruebas; 440 antes de la fase). Los cinco criterios de salida se comprobaron además contra un Postgres temporal.
> **Pendiente del usuario:** revisar el diff, generar las migraciones y hacer el commit. Al cierre de esta fase las tres migraciones de la fase 1 seguían sin generarse: la próxima migración que se genere llevará juntos los cambios de las fases 1 y 2 (§F.1, filas 1 a 8).
> **Rompe al frontend actual hasta su fase 2:** crear una orden de cargue exige `destinationCityId` (C-F2-03 y C-F2-08), así que antes hay que cargar el catálogo de ciudades.
> **Desviaciones respecto al texto de los ítems** (ninguna cambia una decisión de §A.4 ni de §B.4):
> 1. **F2-01 — métodos del dominio.** `NationalizePartial` y `ApplyNationalizedDeltaFromReleaseEdit` se retiraron en lugar de adaptarse: los handlers llaman a `RecalculateTotals` directamente. `RegisterRelease` ya no recibe el stock.
> 2. **F2-01 — guarda al editar.** El 409 «No se puede reducir el levante…» solo se evalúa cuando la cantidad baja: aumentar un levante nunca se bloquea por lo ya despachado.
> 3. **F2-01/F2-02 — `Used`.** Lo despachado se toma como `max(0, recibido − stock)`: un ajuste que deje el stock por encima de lo recibido no aumenta lo nacionalizado disponible.
> 4. **F2-03 y F2-05 — servicios compartidos no listados.** `ReleaseDuplicateLookup` (consulta + reglas) y `ReleaseFobService` (tasa de la DIAN con 3 s, respaldo manual y congelamiento) sirven al alta y a la edición.
> 5. **F2-06 — carga masiva.** Además de los casos del plan se reportan por fila: id del legacy repetido en el archivo, ciudad duplicada (nombre, país y distrito) y fila con menos de tres columnas. El listado pagina sobre la entidad (EF no traduce un orden posterior al DTO posicional). Los requests van en `Requests/CityRequests.cs`.
> 6. **F2-07 — texto del destino.** Se quitó del validador la regla de 100 caracteres de `destinationCity`, porque el campo se ignora. La navegación de la orden a la ciudad se llama `DestinationCityRef`.
> 7. **F2-09 — universo.** «Mercancía sin nacionalizar» es Σ cantidad del depósito − Σ levantes, igual que en F2-08. El listado y el reporte de candidatos calculan los días y paginan en memoria.
> 8. **F2-02 — DTO.** `LoadingOrderDepositProductDto` lleva dos campos que no viajan en el JSON (cantidad del depósito y reservado) para calcular `nationalizedAvailable`.
> 9. **Fechas como parámetro.** Los rangos por día de Colombia se convierten a UTC antes de la consulta: Npgsql rechaza un `timestamptz` con desplazamiento −05:00.
>
> **Defecto previo corregido dentro de la fase** (§G.17): `GET …/loading-orders/{id}` fallaba con `NullReferenceException` porque el handler leía la unidad de medida sin incluirla; es uno de los endpoints de C-F2-09.

- **Objetivo:** no se despacha más de lo nacionalizado por producto. Los levantes son confiables (sin duplicados, retirables, con FOB y tasa congelados). El sistema avisa antes de que un depósito caiga en abandono. El destino de la orden sale de un catálogo que calcula el vencimiento de la guía.
- **Criterio de salida (verificable):**
  1. Una orden de cargue que pide más de lo nacionalizado de un producto responde 400 con el mensaje de F2-02.
  2. En un depósito con dos productos se pueden registrar los levantes de ambos. Tras despachar lo nacionalizado se puede registrar el levante del resto.
  3. Un levante repetido en otro depósito responde 409, y retirar un levante con despachos responde 409.
  4. El listado de abandono muestra los días faltantes y el job envía la alerta del día.
  5. Una orden con destino «IPIALES» (3 días) genera una guía que vence 3 días después de la salida.
  6. `dotnet build` y `dotnet test` pasan.
- **Rama:** `develop` (§E).
- **Dificultad:** **Alta**. Afecta el control aduanero del inventario, corrige dos defectos de topes en código que ya está en uso, y suma un job y consultas nuevas.
- **Perfil de agente:** agente capaz, con revisión humana del diff.
- **Depende de:** no usa código de la fase 1, pero empieza cuando la fase 1 tiene todos sus ítems con commit: en `develop` se trabaja un ítem a la vez.

---

#### F2-01 · Topes de levante por producto y totales del depósito (RN-028; prerrequisito de GAP-002)

- **Dificultad:** Alta.
- **Regla:**
  1. **Pendiente por nacionalizar de un producto** = `ReceivedQuantity` (cantidad del depósito: declarada + ajustes CE-7) − Σ `ReleasedQuantity` de los levantes de ese producto, sin contar el levante que se está editando.
     - No depende del stock actual: despachar no reduce lo pendiente por nacionalizar.
     - Hoy el tope es `min(CurrentStock, ReceivedQuantity)` − levantes. Ejemplo del defecto: recibido 100, levante 50, despacho 50 → hoy el pendiente es `min(50,100) − 50 = 0`; el correcto es `100 − 50 = 50`.
  2. **Registrar:** cantidad ≤ pendiente + 0,0001. Si no → 400 "La cantidad a levantar ({q}) supera lo pendiente por nacionalizar del producto ({p})."
  3. **Editar:**
     - Nueva cantidad ≤ `ReceivedQuantity` − Σ otros levantes del producto. Si no, el mismo mensaje.
     - Además, la suma de levantes del producto tras la edición debe ser ≥ lo ya usado de lo nacionalizado (despachado + reservado, ver F2-02). Si no → 409 "No se puede reducir el levante: ya se despacharon o reservaron {x} unidades nacionalizadas de «{producto}». Revierta o cancele primero la salida."
  4. **Totales del depósito de importación:**
     - `ImportWarehouseStorage.NationalizedQuantity` y `NationalizedWeight` son la suma de **todos** sus levantes. Se recalculan con `RecalculateTotals(IEnumerable<ImportRelease>)` (nuevo) después de cada alta, edición o retiro.
     - El estado sigue la regla ACE-1: `Nacionalizado` si la suma > 0; si no, `SinNacionalizar`.
  5. **Se eliminan dos comprobaciones erróneas:**
     - `IsFullyNationalized` a nivel de depósito, usada en `NationalizePartial`, `RegisterRelease` y `ApplyNationalizedDeltaFromReleaseEdit`. Compara el tope de **un** producto con lo nacionalizado de **todo** el depósito, así que en un depósito con varios productos el levante del segundo falla con "El depósito ya está completamente nacionalizado." Los topes se validan por producto en los handlers.
     - La validación de peso contra el «peso documental» en la edición (`NetDeclaredWeight` del primer producto). Desde WMS-10 ese peso es nulo y el dato no tiene sentido por producto.
  6. Un depósito en Borrador no admite levantes (regla actual).
- **Evidencia:**
  - Legacy: `modulos/mod_levantes/registrarlevante.php:255-262` (`evaluaSaldo`: el saldo por nacionalizar es ingreso − nacionalizado, sin mirar las salidas); `:400-436` (reparte el levante entre las filas del producto en el depósito).
  - v2: `Wms.Application/ForeignTrade/Commands/RegisterImportRelease/RegisterImportReleaseCommandHandler.cs:45-59` (tope con el stock actual) y `:75-79` (`NationalizePartial`); `Wms.Application/ForeignTrade/Commands/UpdateImportRelease/UpdateImportReleaseCommandHandler.cs:35-67`; `Wms.Domain/Entities/ForeignTrade/ImportWarehouseStorage.cs:66,100,119-131,149-185`.
- **Archivos:**
  - `Wms.Application/ForeignTrade/Common/Services/NationalizationBalance.cs` (nuevo, puro): `PendingToNationalize(received, releasedOthers)`, `Used(received, current, reserved) = (received − current) + reserved`, `NationalizedAvailable(released, received, current, reserved) = max(0, released − Used)`.
  - `ImportWarehouseStorage.cs` (modifica: `RecalculateTotals`; retira `IsFullyNationalized` y `NationalizationQuantityCap`; `NationalizePartial` y `ApplyNationalizedDeltaFromReleaseEdit` pasan a llamar a `RecalculateTotals`).
  - `RegisterImportReleaseCommandHandler.cs` y `UpdateImportReleaseCommandHandler.cs` (modifica).
- **Contrato:** C-F2-01 (registrar, mensajes nuevos) y C-F2-02 (editar).
- **Esquema:** ninguno.
- **Efectos secundarios:** los totales del depósito se vuelven exactos (suma de filas); el estado de la etiqueta se recalcula.
- **Pruebas:**
  - `Wms.Tests/ForeignTrade/NationalizationBalanceTests.cs` (nuevo):

    | Caso | Datos | Resultado |
    |---|---|---|
    | Pendiente sin levantes | recibido 100, otros 0 | 100 |
    | Pendiente con levante | recibido 100, otros 60 | 40 |
    | Regresión del defecto | recibido 100, levante 50, despachado 50 | pendiente 50 |
    | Usado | recibido 10, actual 7, reservado 2 | 5 |
    | Disponible | levantes 6 y usado 5 | 1 |
    | Disponible en el límite | levantes 5 y usado 5 | 0 |
    | Disponible negativo | levantes 4 y usado 5 | 0 (nunca negativo) |

  - `Wms.Tests/Domain/ForeignTrade/ImportWarehouseStorageTotalsTests.cs` (nuevo):
    - Depósito con producto A (levantes 100) y producto B (levante 30) → `NationalizedQuantity = 130`, estado `Nacionalizado`.
    - Sin filas → 0 y `SinNacionalizar`.
- **Terminado cuando:** el caso multiproducto y el caso «levante después de despachar» funcionan, y las pruebas pasan.
- **Riesgo:** cambia el tope de un flujo en uso. Se mitiga con las pruebas de regresión y la revisión humana.

---

#### F2-02 · Tope de despacho por cantidad nacionalizada por producto (GAP-002, RN-034)

- **Dificultad:** Alta.
- **Regla:**
  1. Para cada producto de un depósito de **importación** (con `ImportWarehouseStorage`): nacionalizado disponible = `NationalizationBalance.NationalizedAvailable(Σ levantes del producto, ReceivedQuantity, CurrentStock, ReservedStock)`.
  2. **Crear orden de cargue:** por cada producto de importación, la suma de las cantidades pedidas en la orden (sumando sus unidades de carga) debe ser ≤ disponible + 0,0001. Si no → 400:
     > "La cantidad solicitada de «{producto}» en el depósito {número} ({solicitado}) supera lo nacionalizado disponible ({disponible}). Registre el levante antes de despachar."
  3. Se suma a las reglas actuales: depósito confirmado, estado `Nacionalizado`, stock disponible y cliente sin bloqueo. Exportación e inspección no cambian.
  4. La misma regla se aplica cuando se **aumenta** la cantidad de una orden (F3-03).
  5. `GET foreign-trade/loading-orders/deposits` agrega por producto `nationalizedQuantity` (Σ levantes) y `nationalizedAvailable`, ambos `null` en exportación e inspección, para que el frontend limite la cantidad.
  6. El legacy calculaba lo mismo (nacionalizado − despachado por producto) pero solo avisaba en JavaScript, y otra ruta dejaba exceder el stock (RN-036, anomalía que no se replica).
- **Evidencia:**
  - Legacy: `modulos/mod_salidas/registrarsalida.php:235-242` (`evaluaSaldo`: alerta «La cantidad disponible nacionalizada es inferior…»), `:786-816` (nacionalizados por producto), `:979-995` (disponibles = nacionalizados − despachados).
  - v2: `Wms.Application/ForeignTrade/Commands/CreateLoadingOrder/CreateLoadingOrderCommandHandler.cs:137-165` (solo exige el estado y `AvailableStock`); `ImportWarehouseStorage.cs:138-142` (ACE-1: `Nacionalizado` con el primer levante de cualquier producto).
- **Archivos:**
  - `CreateLoadingOrderCommandHandler.cs` (modifica: carga la suma de levantes por producto de los depósitos de importación y valida).
  - `Wms.Application/ForeignTrade/Queries/GetLoadingOrderDeposits/GetLoadingOrderDepositsHandler.cs` (modifica).
  - `Wms.Application/ForeignTrade/Common/DTOs/LoadingOrderDepositDto.cs` (modifica: `LoadingOrderDepositProductDto` agrega `NationalizedQuantity` y `NationalizedAvailable`, ambos `decimal?`).
  - `NationalizationBalance.cs` (modifica: `EnsureWithinNationalized(productName, storageNumber, requested, available)`, que lanza la excepción del punto 2).
- **Contrato:** C-F2-03 (crear orden, error nuevo) y C-F2-04 (depósitos para la orden).
- **Esquema:** ninguno.
- **Efectos secundarios:** ninguno; es una validación.
- **Pruebas** (`NationalizationBalanceTests`):

  | Caso | Resultado |
  |---|---|
  | Pide 21 con disponible 20 | error con el mensaje exacto |
  | Pide 20 con disponible 20 | válido |
  | Pide 1 con disponible 0 | error |
  | Pide 0,00005 por encima del disponible | válido (tolerancia) |

- **Terminado cuando:** con un levante de 1 unidad no se puede despachar más de 1 unidad de ese producto, y los productos sin levante no se pueden despachar.
- **Riesgo:** bloquear salidas legítimas si hay levantes mal cargados. Se mitiga con F2-04 (retirar) y la edición de levantes.

---

#### F2-03 · Levante repetido (GAP-009, RN-026, §B.4.1)

- **Dificultad:** Media.
- **Regla** (al registrar y al editar; los números se comparan con `Trim()` + mayúsculas):
  1. Número de levante que ya existe en un levante de **otro** depósito → 409 "El número de levante {n} ya está registrado en el depósito {m}."
  2. Número de aceptación que ya existe en otro depósito → 409 "El número de aceptación {a} ya está registrado en el depósito {m}."
  3. En el **mismo** depósito:

     | Caso | Respuesta |
     |---|---|
     | Mismo número y mismo producto (otra fila) | 409 "El levante {n} ya está registrado para este producto." |
     | Mismo número con otra aceptación | 409 "El levante {n} ya está registrado en este depósito con la aceptación {a}; use el mismo número de aceptación." |
     | Misma aceptación con otro número de levante | 409 "La aceptación {a} ya está registrada en este depósito con el levante {n}; use el mismo número de levante." |
     | Mismo número y misma aceptación para **otro** producto | permitido: un levante de la DIAN cubre varios productos |

  4. El legacy no insertaba el levante repetido y el aviso quedó comentado. La v2 responde con un 409 explícito.
- **Evidencia:**
  - Legacy: `registrarlevante.php:313-316` (busca `nro_levante LIKE x OR nro_aceptacion LIKE y` en todos los levantes; si existe, no inserta), `:330-340` (aviso comentado).
  - v2: `Wms.Infrastructure/Persistence/Configurations/ForeignTrade/ImportReleaseConfiguration.cs` (sin índice único); los handlers no validan.
- **Archivos:**
  - `Wms.Application/ForeignTrade/Common/Services/ReleaseDuplicateRules.cs` (nuevo, puro): `Check(IReadOnlyList<ExistingRelease> existing, Guid importStorageId, Guid storageProductId, string releaseNumber, string acceptanceNumber, Guid? editingReleaseId)`, que lanza `ConflictException`. `ExistingRelease(Guid Id, Guid ImportStorageId, string StorageNumber, Guid StorageProductId, string ReleaseNumber, string AcceptanceNumber)`.
  - `RegisterImportReleaseCommandHandler.cs` y `UpdateImportReleaseCommandHandler.cs` (modifica: consultan los levantes con ese número o esa aceptación, normalizados).
  - `ImportReleaseConfiguration.cs` (modifica: índice).
- **Contrato:** C-F2-01 y C-F2-02 (errores 409).
- **Esquema:** índice no único `idx_import_releases_acceptance_number` sobre `acceptance_number`. **No** se crea índice único, porque el caso permitido repite el número dentro del depósito.
- **Efectos secundarios:** ninguno.
- **Pruebas** (`Wms.Tests/ForeignTrade/ReleaseDuplicateRulesTests.cs`, nuevo): un caso por cada fila de la regla, más uno de edición del mismo levante (se excluye a sí mismo) y uno sin distinguir mayúsculas (`"lev-1"` contra `"LEV-1"`).
- **Terminado cuando:** las pruebas pasan y registrar un levante repetido en otro depósito responde 409.
- **Riesgo:** bajo.

---

#### F2-04 · Retirar un levante (GAP-009, RN-030)

- **Dificultad:** Media.
- **Regla:** `POST foreign-trade/imports/{id}/releases/{releaseId}/withdraw` con `reason`. `{id}` es el `ImportWarehouseStorage.Id`, como en los endpoints actuales de levantes.

  | Condición | Respuesta |
  |---|---|
  | El levante no es del depósito | 404 "El levante no existe o no pertenece a este depósito." |
  | Depósito anulado | 400 "No se pueden retirar levantes de un depósito anulado." |
  | Motivo fuera de rango | 400 "El motivo del retiro debe tener entre 10 y 500 caracteres." |
  | Lo nacionalizado del producto sin este levante < despachado + reservado | 409 "No se puede retirar el levante: ya se despacharon o reservaron {x} unidades nacionalizadas de «{producto}». Revierta o cancele primero la salida." |

  - **Efecto:** borrado físico de la fila (`context.ImportReleases.Remove`), como el legacy. El `SaveChanges` va con `Describe("Retiro del levante {n} (aceptación {a}) del producto «{p}» del depósito {m}: {cantidad}. Motivo: {motivo}")`, y la baja queda en `audit_logs` con los valores anteriores. Recalcula los totales y el estado (F2-01).
  - Para retirar un levante de varios productos se retira cada fila.
  - Si el depósito vuelve a `SinNacionalizar`: notificación a `ForeignTrade`, nivel Warning, título "Depósito sin nacionalizar", mensaje "El depósito {m} quedó sin nacionalizar tras retirar el levante {n}: reimprima la etiqueta."
  - La respuesta es el detalle del depósito (`ImportDepositDetailDto`).
  - La guarda de despachos es la versión corregida: el legacy podía dejar despachado > nacionalizado.
- **Evidencia:**
  - Legacy: `modulos/mod_levantes/eliminarlevante.php:34-47` (borra el levante y sus productos sin validar despachos); `eliminarproductolevante.php:51-58` (borra la fila de un producto).
  - v2: `Wms.Api/Controllers/v1/ForeignTradeController.cs:179,210` (solo POST y PATCH de levantes).
- **Archivos:**
  - `Wms.Application/ForeignTrade/Commands/WithdrawImportRelease/WithdrawImportReleaseCommand.cs`, `WithdrawImportReleaseCommandValidator.cs` y `WithdrawImportReleaseCommandHandler.cs` (nuevos).
  - `Wms.Api/Controllers/v1/ImportReleaseActionsController.cs` (nuevo; `[Route("foreign-trade")]`, `ForeignTradeAccess`).
  - `Wms.Api/Controllers/v1/Requests/ImportReleaseRequests.cs` (nuevo).
  - `NationalizationBalance.cs` (usa `Used`).
- **Contrato:** C-F2-05.
- **Esquema:** ninguno.
- **Efectos secundarios:** baja auditada, recálculo de totales y estado, notificación condicional.
- **Pruebas:** guarda pura `NationalizationBalance.CanReduceTo(newReleased, used)`: (5, 5) → true; (4, 5) → false; (0, 0) → true.
- **Terminado cuando:** se retira un levante sin despachos y el depósito recalcula sus totales; con despachos responde 409.
- **Riesgo:** borrar un levante bueno por error. Se mitiga con el motivo obligatorio y la auditoría con los valores anteriores (se puede volver a registrar).

---

#### F2-05 · FOB y tasa congelados en el levante (RN-060, §B.4.2)

- **Dificultad:** Media.
- **Regla:**
  1. Registrar un levante acepta `fobUsd` (decimal ≥ 0, hasta 2 decimales, opcional) y `manualExchangeRate` (decimal > 0, opcional).
  2. `fobUsd` nulo o 0 → no se registra FOB: los cinco campos nuevos quedan nulos y no se consulta la tasa. El legacy guardaba `NULL` si el FOB venía vacío o en 0.
  3. `fobUsd` > 0: la tasa es la TRM de la DIAN del **día del registro** en Colombia (`ColombiaTime.Today`), como el legacy, que usaba la tasa vigente del día.
     - Se obtiene con `IDianTrmService.GetTrmAsync(fecha, "USD", ct)` y una espera máxima de 3 s (`CancellationTokenSource` vinculado, el mismo patrón de `StorageBillingService.EnsureTrmAsync`).
     - Si la DIAN responde: `ExchangeRateSource = Dian`, `ExchangeRateDate = hoy`; `manualExchangeRate` se ignora.
     - Si no responde y viene `manualExchangeRate`: `ExchangeRateSource = Manual`, `ExchangeRateDate = hoy`.
     - Si no responde y no viene la manual → 400 "No se pudo consultar la TRM de la DIAN. Digite la tasa de cambio para registrar el FOB."
  4. `FobCop = Math.Round(fobUsd × tasa, 0, MidpointRounding.AwayFromZero)`, como el `Math.round` del legacy.
  5. **Congelado:**
     - Al editar, si cambia `fobUsd`, `FobCop` se recalcula con la **misma** tasa guardada; la tasa no se vuelve a consultar ni se reemplaza.
     - Si el levante no tenía tasa y en la edición llega `fobUsd` > 0, se obtiene como al registrar.
     - Si en la edición `fobUsd` pasa a 0 o nulo, se borran los cinco campos.
  6. `ImportReleaseDto` expone `fobUsd`, `exchangeRate`, `exchangeRateSource`, `exchangeRateDate` y `fobCop`.
  7. El importador del levante del legacy (`levante.id_importador`) no se guarda: es el importador del depósito.
- **Evidencia:**
  - Legacy: `registrarlevante.php:93` (tasa vigente hoy en `tasa_cambio`), `:174-178` (`calculaPesos`: `fob_pesos = Math.round(tasa × fob_dolares)`), `:326-329` (INSERT con tasa, FOB en dólares y en pesos), `:322-324` (FOB vacío → `NULL`).
  - v2: `Wms.Domain/Entities/ForeignTrade/ImportRelease.cs` (sin FOB ni tasa); `Wms.Domain/Services/IDianTrmService.cs`.
- **Archivos:**
  - `ImportRelease.cs` (modifica: `FobUsd`, `ExchangeRate`, `ExchangeRateSource` de tipo `TrmSource?` (enum existente), `ExchangeRateDate` de tipo `DateOnly?`, `FobCop`; métodos `SetFob(decimal fobUsd, decimal rate, TrmSource source, DateOnly date)`, `ChangeFob(decimal? fobUsd)` y `ClearFob()`).
  - `ImportReleaseConfiguration.cs` (modifica).
  - `RegisterImportReleaseCommand.cs` y su validador y handler (modifica).
  - `Wms.Application/ForeignTrade/Commands/UpdateImportRelease/UpdateImportReleaseCommand.cs` y su validador y handler (modifica).
  - `ForeignTradeController.cs` (modifica: `RegisterImportReleaseRequest` y el request de la edición agregan `FobUsd` y `ManualExchangeRate`).
  - `Wms.Application/ForeignTrade/Common/DTOs/ImportReleaseDto.cs` y el handler de `GetImportDepositDetail` (modifica).
  - `Wms.Application/ForeignTrade/Common/Services/FobCalculator.cs` (nuevo, puro).
- **Contrato:** C-F2-01, C-F2-02 y C-F2-06 (detalle del depósito).
- **Esquema** (`import_releases`):
  - `fob_usd numeric(18,2) NULL`
  - `exchange_rate numeric(18,4) NULL`
  - `exchange_rate_source varchar(10) NULL`
  - `exchange_rate_date date NULL`
  - `fob_cop numeric(18,2) NULL`
- **Efectos secundarios:** consulta a la DIAN (con caché de 12 h del servicio actual). No bloquea: hay tasa manual de respaldo.
- **Pruebas:**
  - `Wms.Tests/ForeignTrade/FobCalculatorTests.cs` (nuevo): 1000 × 3900,25 → 3 900 250; 0,5 × 1 → 1 (redondeo hacia arriba en el medio); 1 × 3900,4 → 3 900.
  - `Wms.Tests/Domain/ForeignTrade/ImportReleaseFobTests.cs` (nuevo):
    - `SetFob(100, 0, ...)` → error "La tasa de cambio debe ser mayor que cero."
    - `SetFob(-1, 3900, ...)` → error "El FOB no puede ser negativo."
    - `ChangeFob(200)` conserva la tasa y recalcula `FobCop`.
    - `ClearFob()` deja los cinco en nulo.
- **Terminado cuando:** un levante con FOB 1000 queda con la tasa de la DIAN del día y su FOB en pesos, y editar el FOB no cambia la tasa.
- **Riesgo:** DIAN caída. Se mitiga con la tasa manual.

---

#### F2-06 · Catálogo de ciudades con días de tránsito (GAP-025, LEGACY-FUNC-005 a 008)

- **Dificultad:** Media.
- **Regla:**
  1. Entidad `City` (tabla `cities`), con la estructura de la tabla legacy `ciudad` para la carga masiva:

     | Propiedad | Regla | Columna legacy |
     |---|---|---|
     | `LegacyId` (int?) | único cuando no es nulo | `id_ciudad` |
     | `Name` | 1 a 35 caracteres, recortado | `nom_ciudad` |
     | `CountryCode` | 3 letras, se guarda en mayúsculas | `id_pais` |
     | `District` | 0 a 20 caracteres, opcional | `distrito` |
     | `TransitDays` (int?) | 0 a 99 | `dias` |
     | `IsAbandonmentDestination` (bool, por defecto false) | P6c | — |
     | `IsActive` (bool, por defecto true) | | — |

  2. **Administración** (solo Admin): crear, editar (todos los campos menos `LegacyId`), activar o desactivar y eliminar.
     - Eliminar solo si ninguna orden de cargue la usa; si la usa → 409 "La ciudad está en uso en órdenes de cargue; desactívela en lugar de eliminarla." La baja es física y queda auditada.
     - Duplicado (mismo nombre normalizado con `CatalogNameNormalizer`, mismo país y mismo distrito) → 409 "Ya existe la ciudad {nombre} ({país}, {distrito})."
     - Mensajes de validación:
       - "El nombre de la ciudad es obligatorio y no puede exceder 35 caracteres."
       - "El país debe ser un código de 3 letras."
       - "El distrito no puede exceder 20 caracteres."
       - "Los días de tránsito deben estar entre 0 y 99."
  3. **Carga masiva** `POST administration/cities/import` (multipart: `file`, `headerRows` ≥ 0 con valor por defecto 1, `dryRun` con valor por defecto true):
     - Columnas en este orden: `id_ciudad`, `nom_ciudad`, `id_pais`, `distrito`, `dias`. El separador es `;` o `,` y se detecta en la primera fila de datos. UTF-8.
     - Por fila: si existe una ciudad con ese `LegacyId`, se actualiza; si no, se crea.
     - `dias` vacío → nulo.
     - Los errores de una fila no detienen las demás. Casos: id no entero, y los mensajes del punto 2 con el prefijo "Fila {n}: ".
     - Con `dryRun = true` no guarda nada. Con `false` guarda todo en una transacción, solo las filas válidas.
  4. **Lectura:** `GET administration/cities` con búsqueda, país, activas y `all=true` para el select, disponible para cualquier usuario autenticado.
- **Evidencia:**
  - Legacy: `bodegas_schema.sql:124-132` (tabla `ciudad`); `modulos/mod_ciudades/*` (CRUD).
  - v2: sin entidad; `Wms.Domain/Entities/Warehouse/LoadingOrder.cs` (`DestinationCity` de texto libre).
- **Archivos:**
  - `Wms.Domain/Entities/Administration/City.cs` (nuevo).
  - `Wms.Infrastructure/Persistence/Configurations/Administration/CityConfiguration.cs` (nuevo).
  - `AppDbContext.cs` (modifica: `DbSet<City> Cities`).
  - `Wms.Application/Administration/Cities/Commands/{CreateCity,UpdateCity,DeleteCity,ImportCities}/*` (nuevos: comando, validador y handler de cada uno).
  - `Wms.Application/Administration/Cities/Queries/GetCities/*` (nuevo).
  - `Wms.Application/Administration/Cities/Common/CityDto.cs` y `CityCsvParser.cs` (nuevos; el parser es puro).
  - `Wms.Api/Controllers/v1/CitiesController.cs` (nuevo): `[Route("administration")]`, `[Authorize]`, y `[Authorize(Policy = "AdminOnly")]` en las escrituras.
- **Contrato:** C-F2-07.
- **Esquema:** tabla nueva `cities` (§F).
- **Efectos secundarios:** auditoría de altas, cambios y bajas.
- **Pruebas:**
  - `Wms.Tests/Domain/Administration/CityTests.cs` (nuevo): nombre de 36 caracteres → error; país `"CO"` → error; días 100 → error; días 0 → válido; `CountryCode` en minúsculas → se guarda en mayúsculas.
  - `Wms.Tests/Administration/CityCsvParserTests.cs` (nuevo):
    - `"4956;IPIALES;COL;NARIÑO;3"` → la fila correcta.
    - `dias` vacío → nulo.
    - Separador `,`.
    - Con `headerRows = 1` se salta la primera fila.
    - Fila con id `"abc"` → error "Fila 2: el id de la ciudad no es un número entero."
- **Terminado cuando:** se cargan las ciudades con `dryRun = true` y `false`, y el select las lista.
- **Riesgo:** el archivo legacy trae duplicados. Se mitiga reportándolos como errores de fila sin detener la carga.

---

#### F2-07 · Destino de la orden por catálogo y vencimiento calculado de la guía (GAP-025, §B.4.7)

- **Dificultad:** Media.
- **Regla:**
  1. **Crear orden** (`POST foreign-trade/loading-orders` y `POST warehouse/loading-orders`):
     - `destinationCityId` es obligatorio: "Seleccione la ciudad de destino."
     - Debe existir y estar activa: 404 "La ciudad de destino no existe o está inactiva."
     - Se guardan `LoadingOrder.DestinationCityId` y `DestinationCity` = el nombre de la ciudad (copia para impresión y listados). El campo de texto `destinationCity` del request se ignora.
     - `destinationAddress` sigue siendo libre. Un solo destino por orden (el legacy admitía varios).
  2. **Emitir la guía de importación** (`POST foreign-trade/dispatch-guides`):
     - Si la ciudad de la orden tiene `TransitDays > 0`: `ExpirationDate = DepartureDatetime.AddDays(TransitDays)`, a la misma hora; el `expirationDate` del request se ignora.
     - Si la orden no tiene ciudad (órdenes anteriores) o la ciudad no tiene días (nulo o 0): `expirationDate` es obligatorio y posterior a la salida. Si falta → 400 "Indique la fecha de vencimiento: la ciudad de destino {nombre} no tiene días de tránsito.", o bien "Indique la fecha de vencimiento: la orden no tiene ciudad de destino."
     - El validador deja `ExpirationDate` opcional y la regla pasa al handler, con el cálculo en `GuideExpirationCalculator`.
  3. **Guía de exportación automática:** vence `ahora + TransitDays` si la ciudad tiene días; si no, `ahora + 30 días` (regla actual).
- **Evidencia:**
  - Legacy: `modulos/mod_salidas/registrarsalida.php:436-438` (la salida guarda `id_ciudaddestino`); `modulos/mod_salidas/verguia.php:705-721` (vence = fecha de la guía + el mayor de los días de los destinos; al crear la guía, hoy + días).
  - v2: `LoadingOrder.cs` (`DestinationCity` libre); `Wms.Application/ForeignTrade/Commands/CreateDispatchGuide/CreateDispatchGuideCommandValidator.cs:19-22` (vencimiento digitado); `Wms.Application/ForeignTrade/Commands/CreateExportDispatchGuide/CreateExportDispatchGuideCommandHandler.cs:109` (`now + 30`).
- **Archivos:**
  - `LoadingOrder.cs` (modifica: `DestinationCityId` y `SetDestination(Guid cityId, string cityName, string? address)`).
  - `Wms.Infrastructure/Persistence/Configurations/Warehouse/LoadingOrderConfiguration.cs` (modifica).
  - `CreateLoadingOrderCommand.cs`, `CreateLoadingOrderCommandValidator.cs` y `CreateLoadingOrderCommandHandler.cs` (modifica).
  - `ForeignTradeController.cs` (modifica: `CreateLoadingOrderRequest` agrega `DestinationCityId`).
  - `Wms.Api/Controllers/v1/WarehouseController.cs` (modifica: `CreateWarehouseLoadingOrderRequest` agrega `DestinationCityId` y el mapeo).
  - `CreateDispatchGuideCommandValidator.cs` y `CreateDispatchGuideCommandHandler.cs` (modifica).
  - `CreateExportDispatchGuideCommandHandler.cs` (modifica).
  - `Wms.Application/Warehouse/Common/DTOs/LoadingOrderDto.cs` y `Wms.Application/ForeignTrade/Common/DTOs/LoadingOrderListDto.cs` (modifica: `DestinationCityId`).
  - `Wms.Application/ForeignTrade/Common/Services/GuideExpirationCalculator.cs` (nuevo, puro).
- **Contrato:** C-F2-03 (crear orden), C-F2-08 (crear orden desde Bodega), C-F2-09 (detalle y listados de órdenes: `destinationCityId`) y C-F2-10 (emitir guía).
- **Esquema:** `loading_orders.destination_city_id uuid NULL`, FK a `cities(id)` con `ON DELETE RESTRICT`, e índice.
- **Efectos secundarios:** ninguno más.
- **Pruebas** (`Wms.Tests/ForeignTrade/GuideExpirationCalculatorTests.cs`, nuevo):

  | Salida | Días | Resultado |
  |---|---|---|
  | `2026-09-29T10:00-05:00` | 3 | `2026-10-02T10:00-05:00` |
  | cualquiera | 0 o nulo | requiere fecha manual |
  | manual igual a la salida | — | error "La fecha de vencimiento debe ser posterior a la fecha de salida." (regla actual del dominio) |

- **Terminado cuando:** la orden guarda la ciudad y la guía vence según sus días.
- **Riesgo:** órdenes abiertas sin ciudad. Se mitiga con la fecha manual como respaldo.

---

#### F2-08 · Prórroga (GAP-003, RN-024)

- **Dificultad:** Media.
- **Regla:** `POST foreign-trade/imports/{id}/extension` con `notes` (opcional, hasta 500). `{id}` es el `ImportWarehouseStorage.Id`.

  | Condición | Respuesta |
  |---|---|
  | Depósito que no está en Borrador ni Confirmado | 400 "Solo los depósitos de importación en Borrador o Confirmado admiten prórroga." |
  | Sin mercancía por nacionalizar (Σ `ReceivedQuantity` − Σ levantes ≤ 0) | 400 "El depósito {n} no tiene mercancía sin nacionalizar." |
  | Ya tiene prórroga | 409 "El depósito {n} ya tiene prórroga registrada el {dd/MM/yyyy} por {usuario}." (fecha en Colombia) |

  - **Efecto:** `ImportWarehouseStorage.RegisterExtension(Guid userId, string? notes)` (nuevo) guarda `ExtensionRegisteredAt = UtcNow`, `ExtensionRegisteredById` y `ExtensionNotes`.
  - Es irreversible, como el legacy: no hay endpoint para quitarla y la auditoría la registra.
  - El plazo del depósito pasa de 30 a 60 días (F2-09).
- **Evidencia:**
  - Legacy: `modulos/mod_depositos/registrarprorroga.php:39` (`UPDATE deposito SET prorroga=1`, sin fecha ni motivo).
  - v2: `ImportWarehouseStorage.cs` (sin prórroga).
- **Archivos:**
  - `ImportWarehouseStorage.cs` (modifica).
  - `Wms.Infrastructure/Persistence/Configurations/ForeignTrade/ImportWarehouseStorageConfiguration.cs` (modifica).
  - `Wms.Application/ForeignTrade/Commands/RegisterStorageExtension/*` (nuevo).
  - `Wms.Api/Controllers/v1/AbandonmentController.cs` (nuevo; `[Route("foreign-trade")]`, `ForeignTradeAccess`).
  - `ImportDepositDetailDto` y el handler de `GetImportDepositDetail` (modifica: `extensionRegisteredAt`, `extensionRegisteredByName` y `extensionNotes`).
- **Contrato:** C-F2-11 y C-F2-06 (detalle con la prórroga).
- **Esquema** (`import_warehouse_storages`):
  - `extension_registered_at timestamptz NULL`
  - `extension_registered_by_id uuid NULL`
  - `extension_notes varchar(500) NULL`
- **Efectos secundarios:** auditoría.
- **Pruebas** (`Wms.Tests/Domain/ForeignTrade/ImportWarehouseStorageExtensionTests.cs`, nuevo): la primera vez guarda los datos; la segunda → `ConflictException`; notas de 501 caracteres → error "Las notas de la prórroga no pueden exceder 500 caracteres."
- **Terminado cuando:** se registra la prórroga y el listado de F2-09 pasa el plazo a 60 días.
- **Riesgo:** bajo.

---

#### F2-09 · Listado de abandono, resumen y alerta diaria (GAP-003, RN-059, P6b)

- **Dificultad:** Media.
- **Regla:**
  1. **Cálculo** (puro, `AbandonmentCalculator.Evaluate(DateOnly entryDate, DateOnly today, bool hasExtension)`):
     - Días transcurridos `d = today − entryDate` (días calendario en Colombia). La fecha es siempre la de ingreso del depósito (`WarehouseStorage.EntryDate`; si es nula, `CreatedAt`), según P6b.
     - Plazo `L` = 60 con prórroga, 30 sin ella. Días faltantes = `L − d`.
     - Estado:
       - `EnAlerta`: 20 ≤ d ≤ 30 sin prórroga, o 50 ≤ d ≤ 60 con prórroga.
       - `EnAbandono`: d > L.
       - `EnPlazo`: en cualquier otro caso.
  2. **Universo:** depósitos de importación en Borrador o Confirmado con mercancía sin nacionalizar > 0.
  3. `GET foreign-trade/abandonment`:
     - Lista el universo con d ≥ 20 (como el listado legacy de prórrogas), ordenado por días faltantes ascendente.
     - Filtros: estado, con o sin prórroga, número de depósito, carta porte, importador, agencia de aduanas; paginado con `all=true`. Columnas en C-F2-12.
  4. `GET foreign-trade/abandonment/summary` devuelve `{ inAlert, abandoned }` sobre todo el universo, para el aviso del tablero (equivale a la alerta del panel legacy).
  5. **Alerta diaria:** job `AbandonmentAlertBackgroundService` en `Wms.Api/BackgroundJobs`.
     - Corre una vez al día a las 07:00 de Colombia; al arrancar, espera hasta esa hora o corre si ya pasó y hoy no ha corrido.
     - Si hay depósitos `EnAlerta` o `EnAbandono`, envía **una** notificación al rol `ForeignTrade`: nivel Warning, título "Depósitos en ventana de abandono", mensaje "{a} depósito(s) en alerta y {b} en abandono. Más urgente: {número} (faltan {x} días).", tipo `AbandonmentReport`, `RelatedEntityId = Guid.Empty`. Si el más urgente ya venció, el paréntesis dice "(vencido hace {x} días)".
     - Idempotencia: si ya existe una notificación de tipo `AbandonmentReport` creada hoy (Colombia), no envía otra.
- **Evidencia:**
  - Legacy: `menus/evaluaabandonos.php:6-14` (alerta con los rangos 20 a 30 y 50 a 60 y sin nacionalizar > 0, desde `fecha_deposito`); `modulos/mod_depositos/listardepositosprorroga.php:121-130` (importación, activos, sin nacionalizar > 0, días ≥ 20), `:394-399` (faltan = 30 − d o 60 − d), `:403-409` (resalta si faltan ≤ 10); `reporteprorrogas.php:75` (el reporte cuenta desde `fechahora_ingreso`: la inconsistencia que corrige P6b).
  - v2: sin atributo, alerta, listado ni job (`Wms.Api/BackgroundJobs` solo tiene jobs de facturación).
- **Archivos:**
  - `Wms.Application/ForeignTrade/Common/Services/AbandonmentCalculator.cs` (nuevo).
  - `Wms.Application/ForeignTrade/Queries/GetAbandonmentList/*` y `GetAbandonmentSummary/*` (nuevos).
  - `Wms.Application/ForeignTrade/Common/DTOs/AbandonmentItemDto.cs` (nuevo).
  - `Wms.Application/ForeignTrade/Jobs/AbandonmentAlertService.cs` e `IAbandonmentAlertService.cs` (nuevos; registrar en DI).
  - `Wms.Api/BackgroundJobs/AbandonmentAlertBackgroundService.cs` (nuevo; sigue el patrón de `InvoiceDueNotificationBackgroundService`).
  - `Wms.Api/Program.cs` (modifica: `AddHostedService`).
  - `AbandonmentController.cs` (modifica).
- **Contrato:** C-F2-12 y C-F2-13.
- **Esquema:** ninguno.
- **Efectos secundarios:** una notificación diaria a Comercio Exterior.
- **Pruebas** (`Wms.Tests/ForeignTrade/AbandonmentCalculatorTests.cs`, nuevo):

  | Días | Prórroga | Estado | Faltan |
  |---|---|---|---|
  | 19 | no | `EnPlazo` | 11 |
  | 20 | no | `EnAlerta` | 10 |
  | 30 | no | `EnAlerta` | 0 |
  | 31 | no | `EnAbandono` | −1 |
  | 49 | sí | `EnPlazo` | 11 |
  | 50 | sí | `EnAlerta` | 10 |
  | 60 | sí | `EnAlerta` | 0 |
  | 61 | sí | `EnAbandono` | −1 |

  Más un caso de ingreso a las 20:00 de Colombia del 01/09 (que es 02/09 en UTC): cuenta desde el 01/09.
- **Terminado cuando:** el listado y el resumen coinciden con el cálculo, y el job envía una sola notificación por día.
- **Riesgo:** notificaciones repetidas. Se mitiga con la idempotencia por día.

---

#### F2-10 · Reportes de abandono (GAP-003, LEGACY-FUNC-214, P6a y P6c)

- **Dificultad:** Media.
- **Regla A — «Mercancías que se perfilan para abandono»** (`GET reports/abandonment-candidates`):
  1. Filas por producto del depósito, del universo de F2-09 con d ≥ L: 30 días sin prórroga y **60 con prórroga** (corrección P6a: el legacy excluía los que tienen prórroga). Solo productos con stock actual > 0 y sin nacionalizar > 0.
  2. Columnas: días, prórroga (Sí o No), mercancía, embalaje, unidad, fecha de ingreso, depósito, manifiesto DIAN y su fecha, importador, agencia de aduanas, ingreso (`ReceivedQuantity`), existencias (`CurrentStock`) y sin nacionalizar (`ReceivedQuantity` − Σ levantes del producto).
  3. Totales de ingreso, existencias y sin nacionalizar sobre todo el filtro, en la forma `data: { items, totals }`. El legacy sumaba mal la última columna: sumaba lo nacionalizado.
  4. Filtro por importador y `all=true`.
- **Regla B — «Salida de mercancías en abandono»** (`GET reports/abandonment-exits`, con `fromDate` y `toDate`):
  1. Órdenes de cargue en `Loaded`, `Dispatched` o `Complete` cuya ciudad de destino tiene `IsAbandonmentDestination = true` (P6c, reemplaza el ID fijo −9) y cuya fecha de cargue (`LoadingEndDate`) está en el rango. Por defecto, del 1 de enero del año actual a hoy (Colombia), como el legacy.
  2. Filas por ítem: fecha de cargue, orden, guía (si la hay), placa, conductor, transportadora, cliente, agencia de aduanas, depósito, carta porte, manifiesto DIAN, levantes del producto (números separados por coma), mercancía y cantidad.
  3. La cantidad es la del ítem. En la fase 3, F3-01 la cambia por la cantidad cargada.
- **Evidencia:**
  - Legacy: `modulos/mod_inventario/reporteprorrogas.php:64-80` (consulta, `prorroga=0` y días ≥ 30), `:302-316` (columnas), `:330` (filtro saldo > 0 y sin nacionalizar > 0), `:388` (total mal sumado); `modulos/mod_inventario/reporteabandonos.php:71-87` (salidas con `id_ciudaddestino=-9` y modalidad 4, del 1 de enero a hoy).
  - v2: sin reportes.
- **Archivos:**
  - `Wms.Application/Reports/Queries/GetAbandonmentCandidates/*` y `GetAbandonmentExits/*` (nuevos).
  - `Wms.Application/Reports/Common/DTOs/AbandonmentCandidateDto.cs` y `AbandonmentExitDto.cs` (nuevos).
  - `Wms.Application/Reports/Common/AbandonmentReportTotals.cs` (nuevo, puro).
  - `Wms.Api/Controllers/v1/AbandonmentReportsController.cs` (nuevo; `[Route("reports")]`, `ForeignTradeAccess`).
- **Contrato:** C-F2-14 y C-F2-15.
- **Esquema:** ninguno (la marca de ciudad es de F2-06).
- **Efectos secundarios:** ninguno.
- **Pruebas** (`Wms.Tests/Reports/AbandonmentReportTotalsTests.cs`, nuevo): dos filas (ingreso 10 y 5, existencias 8 y 5, sin nacionalizar 6 y 5) → totales 15, 13 y 11.
- **Terminado cuando:** los dos reportes devuelven las columnas del contrato, con `all=true`.
- **Riesgo:** bajo.

---

### C.3 Fase 3 — Correcciones y facturación

> **Estado: ✅ COMPLETADA el 2026-09-30** (F3-01 a F3-10, implementados en `develop` en una sola pasada por indicación del usuario). `dotnet build Wms.sln` sin errores y `dotnet test Wms.Tests` en verde (642 pruebas; 540 antes de la fase). Los seis criterios de salida funcionales se comprobaron además contra un Postgres temporal (73 comprobaciones de extremo a extremo).
> **Pendiente del usuario:** revisar el diff, generar las migraciones y hacer el commit. Al cierre de la fase no se había generado ninguna migración de paridad: el modelo lleva 50 operaciones pendientes contra el snapshot, 24 de las fases 1 y 2 y 26 de esta (§F.1, filas de F3-01 a F3-10).
> **Rompe al frontend actual hasta su fase 3:** cancelar una orden (C-F3-02) y anular un depósito (C-F3-09) exigen motivo de 10 a 500 caracteres; `inventoryMovementId` del cargue puede ser nulo (C-F3-01).
> **Desviaciones respecto al texto de los ítems** (ninguna cambia una decisión de §A.4 ni de §B.4):
> 1. **F3-06 — prueba `Days360`.** La tabla dice que un período desde el 2027-03-01 termina el 2028-02-25, pero la regla (fin = inicio + 360 días, P7) da el **2028-02-24**. Ganó la regla; la prueba lo documenta.
> 2. **F3-06 — `StoragePeriodStart` se retiró** (archivo y pruebas); sus casos pasaron a `StoragePeriodCalculatorTests`. `CalculatePeriodEnd` salió de `IStorageBillingService`. `StoragePeriodOpenOptions.PeriodStart` ahora es un día (`DateOnly`) y los instantes se guardan en UTC (las 00:00 de Colombia), porque Npgsql no acepta otro desplazamiento. El recálculo del período (D10) conserva su fecha límite. Las líneas de la factura imprimen los días en Colombia.
> 3. **F3-06 — camión tardío.** Se abre contiguo al último período (fin + 1) aunque ese día sea futuro, como dice el ítem; solo el cierre manual cae a hoy.
> 4. **F3-01 — emparejamiento.** `LoadingExecutionMath` también empareja reserva e ítem (`PairActiveReserves`); lo usan la cancelación, la modificación y la anulación del depósito. Un ítem repetido en el cargue responde 400 «El item {id} está repetido en el cargue.»; la lista vacía responde el mensaje de «No se cargó mercancía…». Un ítem cargado en 0 no tiene línea en la guía (la línea exige cantidad > 0) ni se imprime.
> 5. **F3-01 — lo cargado en otras consultas.** Además de lo listado, usan `LoadedQuantity ?? Quantity` el total de la guía (listado y creación), el informe diario de salidas y el resumen del depósito; el informe de salidas en abandono omite los ítems cargados en 0.
> 6. **F3-03 — reglas no escritas.** Un ítem existente no cambia de producto ni de unidad (400 «…retírelo y agregue uno nuevo.»); un id repetido responde 400; un ítem que ya figura en una guía no se retira (409 «El ítem de '{p}' figura en la guía {g}: no se puede retirar. Cancele la orden y cree otra.»), porque las líneas de guía lo referencian. `CreateLoadingOrder` reserva con `LoadingOrderReservationService.ReserveAsync` y conserva sus validaciones agregadas. La liberación completa de la cancelación quedó en el mismo servicio (`ReleaseAll`).
> 7. **F3-04 — piezas compartidas.** `CancelledInvoiceDto` e `InvoiceToReviewDto` viven en `Billing/Common/DTOs`; `InvoiceCancellationPolicy` también aplica la política y avisa a Facturación (lo reusan F3-08 y F3-09). Además de las líneas con `DispatchGuideId`, se revisa la factura de `DispatchGuide.InvoiceItemId`. Las guías anuladas tampoco cuentan en las órdenes pendientes de guía, el informe diario de salidas, los movimientos del depósito, el informe de abandono ni el resumen del depósito. Cambiar el modo de pago de una guía anulada responde 409. No hay endpoint de detalle de guía: los campos van en el listado; el ZIP lleva «_ANULADA» en el nombre y sus PDF la marca de agua.
> 8. **F3-07 — `Reverted`** se agregó a los filtros por estado (búsquedas de báscula, guías pendientes, creación de guía, saldos y reservas del detalle). En órdenes anteriores a F3-01, lo devuelto sale de los movimientos del cargue repartidos por producto en orden de creación. La reapertura del período exige que todos los períodos de la última apertura estén cerrados por agotamiento.
> 9. **F3-08 — alcance.** La orden que solo lleva mercancía del depósito se cancela sin borrar sus ítems; la mixta pierde los del depósito. Las facturas afectadas son las de los períodos abiertos que se cierran. `WarehouseStorage.Cancel` exige motivo y usuario (el descarte de báscula pasa los suyos). El aviso a Bodega usa el título «Depósito anulado».
> 10. **F3-09 — casos de borde.** Anular el pesaje de un depósito ya anulado solo anula el pesaje. Una unidad de carga que figura en una orden no se borra (409 «…la unidad de carga {placa} figura en la orden {o}.»). La respuesta suma las facturas del pesaje y las de los depósitos anulados. El aviso a Facturación usa el título «Pesaje anulado con factura emitida».
> 11. **F3-10 — detalle.** `GetInvoiceById` arma el DTO a mano: se le agregaron los dos campos. `pending-deposits` conserva su criterio (depósitos con período abierto) y cuenta los períodos por refacturar de esas filas.
>
> **Defecto previo corregido dentro de la fase** (§G.18): el peso bruto de facturación no cargaba los camiones del depósito y quedaba en cero fuera de báscula; F3-09 necesitaba ese mismo código.

- **Objetivo:** todo lo que se registra se puede corregir o anular, con sus efectos en inventario y facturación; y el almacenamiento se factura con los ciclos y la regla de períodos del legacy, con importes del motor de acuerdos.
- **Criterio de salida (verificable):**
  1. Un cargue parcial libera la reserva no cargada.
  2. Una orden cargada se revierte tras anular su guía: el stock vuelve y un depósito cerrado se reabre.
  3. Un pesaje completo se anula y el stock de ese camión sale del depósito.
  4. Un depósito confirmado se anula liberando reservas, cerrando períodos y anulando la factura que no se ha aprobado.
  5. Una factura de almacenamiento anulada se refactura.
  6. Un cliente con ciclo de 15 días factura los mismos períodos (inicio, fin y fecha límite) que el legacy.
  7. `dotnet build` y `dotnet test` pasan.
- **Rama:** `develop` (§E). Empieza cuando las fases 1 y 2 tienen todos sus ítems con commit. Usa `NationalizationBalance` (F2-01/F2-02), `LoadingOrder.DestinationCityId` (F2-07) y `DepositConfirmationRequirements` (F1-05).
- **Dificultad:** **Muy alta**. Reversiones y anulaciones en cascada que tocan inventario y facturación a la vez, y reglas de períodos con casos de borde históricos.
- **Perfil de agente:** agente capaz, con revisión humana y prueba con datos reales antes de cerrar la fase.
- **Orden interno:** F3-01 → F3-02 → F3-03 → F3-04 → F3-05 → F3-06 → F3-07 → F3-08 → F3-09 → F3-10.

---

#### F3-01 · Cargue: liberar la reserva no cargada y guardar lo cargado (GAP-006)

- **Dificultad:** Alta.
- **Regla** (en `ExecuteLoadingOrder`):
  1. **Cantidad cargada `q` de cada ítem** de la orden: la de la petición, o 0 si el ítem no viene. Condiciones:
     - `0 ≤ q ≤ Quantity`. Si no → error actual "La cantidad a cargar ({q}) excede la cantidad solicitada ({pedida}) para el producto '{p}'."
     - Si todos los ítems quedan en 0 → 400 "No se cargó mercancía: cancele la orden en lugar de ejecutarla."
  2. Se guarda `LoadingOrderItem.LoadedQuantity = q` con `RegisterLoaded(decimal)`, nuevo.
  3. **Contabilidad por ítem.** Cada ítem tiene su reserva, emparejada por `LoadingOrderItemId` (punto 5):
     - Si `q > 0`: movimiento `Out` de `q`, como hoy, y `ReleaseStock(q)`, que baja stock y reserva en `q`.
     - Si `Quantity − q > 0`: `ReleaseReservedStock(Quantity − q)`.
     - La reserva del ítem se desactiva (`reserve.Release()`), se haya cargado o no.
     - Resultado: `CurrentStock` baja en lo cargado y `ReservedStock` en lo pedido. Hoy la reserva no cargada queda retenida para siempre.
  4. **Unidades de carga:** la unidad despacha `q` y libera `Quantity − q`, como hoy. Un ítem que no viene libera `Quantity` completo.
  5. **Emparejamiento reserva–ítem:** se agrega `WarehouseReserve.LoadingOrderItemId` (nuevo).
     - `CreateLoadingOrder` y F3-03 lo llenan.
     - Las reservas anteriores (nulo) se emparejan por producto en orden de creación.
  6. **La guía congela la cantidad cargada** (`LoadedQuantity`) cuando existe. Si no existe, congela la pedida: órdenes anteriores, o guía emitida antes del cargue (hoy se permite con la orden `Pending`, `InProgress` o `Loaded`, `CreateDispatchGuideCommandHandler.cs:113-119`). Aplica a `DispatchGuideBalanceService.FreezeLinesAsync` y a la guía de exportación automática.
  7. El reporte «Salida de mercancías en abandono» (F2-10) usa `LoadedQuantity` cuando no es nulo.
- **Evidencia:**
  - v2 `Wms.Application/Warehouse/Commands/LoadingOrder/ExecuteLoadingOrderCommandHandler.cs:129-203`: `ReleaseStock(LoadedQuantity)` y `reserve.Release()` sin devolver la diferencia; los ítems no enviados conservan su reserva.
  - v2 `Wms.Domain/Entities/Warehouse/LoadingOrderItem.cs`: sin cantidad cargada.
  - v2 `Wms.Application/ForeignTrade/Common/Services/DispatchGuideBalanceService.cs:43-49`: congela `Quantity`.
  - v2 `ExecuteLoadingOrderCommandHandler.cs:141-142`: la reserva se busca por producto (`FirstOrDefault`), no por ítem; dos ítems del mismo producto (en unidades de carga distintas) toman la misma reserva.
- **Archivos** (todos modifica, salvo el nuevo):
  - `LoadingOrderItem.cs`
  - `WarehouseReserve.cs`: `LoadingOrderItemId`
  - `Wms.Infrastructure/Persistence/Configurations/Warehouse/LoadingOrderItemConfiguration.cs` y `WarehouseReserveConfiguration.cs`
  - `ExecuteLoadingOrderCommandHandler.cs` y `ExecuteLoadingOrderCommandValidator.cs`: `LoadedQuantity ≥ 0`
  - `CreateLoadingOrderCommandHandler.cs`: llena `LoadingOrderItemId`
  - `DispatchGuideBalanceService.cs` y `CreateExportDispatchGuideCommandHandler.cs`
  - `Wms.Application/Warehouse/Common/DTOs/LoadingItemResultDto.cs`: agrega `OrderedQuantity`; `ReservedStockReleased` (existente) pasa a ser la reserva completa liberada del ítem (la cantidad pedida). La respuesta incluye todos los ítems de la orden, también los no enviados (con `LoadedQuantity = 0`); `InventoryMovementId` pasa a `Guid?` (nulo si no se cargó nada)
  - `Wms.Application/Warehouse/Common/DTOs/LoadingOrderDto.cs` (`LoadingOrderItemDto`): `LoadedQuantity`
  - handler de `GetAbandonmentExits`
  - `Wms.Application/Warehouse/Common/Services/LoadingExecutionMath.cs` (nuevo, puro)
- **Contrato:** C-F3-01.
- **Esquema:** `loading_order_items.loaded_quantity numeric(18,4) NULL`; `warehouse_reserves.loading_order_item_id uuid NULL`, con FK a `loading_order_items(id)` `ON DELETE SET NULL` e índice.
- **Efectos secundarios:** `AvailableStock` ya no queda reducido para siempre tras un cargue parcial; movimientos `Out` solo por lo cargado.
- **Pruebas** (`Wms.Tests/Warehouse/LoadingExecutionMathTests.cs`, nuevo):

  | Pedido | Cargado | Salida de stock | Reserva liberada | Disponible después (actual 10, reservado 10) |
  |---|---|---|---|---|
  | 10 | 10 | 10 | 10 | 0 |
  | 10 | 6 | 6 | 10 | 4 |
  | 10 | 0 | 0 | 10 | 10 |
  | 10 | 11 | error | — | — |
  | 1 | 1 | 1 | 1 | — |
  | 2 ítems en 0 | — | error "No se cargó mercancía…" | — | — |

  Además, en dominio: `LoadingOrderItem.RegisterLoaded(-1)` → error "La cantidad cargada no puede ser negativa."
- **Terminado cuando:** tras un cargue parcial, `AvailableStock` = stock − reservas vigentes, y la guía muestra lo cargado.
- **Riesgo:** órdenes anteriores sin `LoadedQuantity`. Se mitiga usando la cantidad pedida como respaldo. Si la guía se emitió antes de un cargue parcial, muestra lo pedido: se corrige anulándola (F3-04) y emitiendo otra.

---

#### F3-02 · Cancelar una orden solo antes del cargue (GAP-006, RN-038, §B.4.6)

- **Dificultad:** Media.
- **Regla:**
  1. `LoadingOrder.Cancel(reason)` solo desde `Pending` o `InProgress`. En otro estado, 409:

     | Estado | Mensaje |
     |---|---|
     | `Loaded`, `Dispatched` o `Complete` | "La orden {n} ya fue cargada: use «Revertir salida»." |
     | `Cancelled` | "La orden {n} ya está cancelada." |
     | `Reverted` | "La orden {n} fue revertida." |

  2. El motivo pasa a ser obligatorio, de 10 a 500 caracteres: "El motivo de la cancelación debe tener entre 10 y 500 caracteres." El legacy exigía motivo al anular la salida.
  3. Libera las reservas activas, como hoy. En unidades de carga libera la reserva de la unidad solo para los ítems cuya reserva sigue activa (hoy la libera siempre).
  4. Si la orden estaba `InProgress`: notificación a `Warehouse`, nivel Warning, título "Orden de cargue cancelada", mensaje "La orden {n} fue cancelada: no la cargue. Motivo: {motivo}".
  5. Aplica a los dos endpoints de cancelación existentes: `PATCH foreign-trade/loading-orders/{id}/cancel` (`ForeignTradeController.cs:1009`) y `PATCH warehouse/loading-orders/{id}/cancel` (`WarehouseController.cs:825`).
- **Evidencia:**
  - Legacy: `modulos/mod_salidas/eliminarsalida.php:110,124`: la salida queda `eliminado` con motivo.
  - v2: `Wms.Domain/Entities/Warehouse/LoadingOrder.cs` (`Cancel` solo rechaza `Complete` y `Cancelled`); `Wms.Application/Warehouse/Commands/LoadingOrder/CancelLoadingOrder/CancelLoadingOrderHandler.cs:27-40` (cancelar una orden cargada no devuelve el stock y libera dos veces la reserva de la unidad).
- **Archivos:**
  - `LoadingOrder.cs` (modifica).
  - `Wms.Domain/Enums/LoadingOrdersStatus.cs` (modifica: agrega `Reverted`, que se usa en F3-07).
  - `CancelLoadingOrderCommand.cs` y `CancelLoadingOrderHandler.cs` (modifica); `CancelLoadingOrderCommandValidator.cs` (nuevo).
  - `ForeignTradeController.cs` (`CancelLoadingOrderFtRequest`) y `WarehouseController.cs` (`CancelLoadingOrderRequest`) (modifica: `Reason` obligatorio).
- **Contrato:** C-F3-02.
- **Esquema:** ninguno. `Reverted` es un valor nuevo de un enum guardado como texto.
- **Efectos secundarios:** notificación a Bodega.
- **Pruebas** (`Wms.Tests/Domain/Warehouse/LoadingOrderTransitionsTests.cs`, nuevo): `Cancel` desde `Pending` y desde `InProgress` → pasa a `Cancelled`; desde `Loaded`, `Dispatched`, `Complete`, `Cancelled` y `Reverted` → `ConflictException` con el mensaje exacto.
- **Terminado cuando:** cancelar una orden cargada responde 409 y cancelar una pendiente libera sus reservas.
- **Riesgo:** el motivo obligatorio rompe al frontend actual. Queda anotado en el contrato para el agente de frontend.

---

#### F3-03 · Modificar la orden antes del cargue (GAP-006, LEGACY-FUNC-158 y 162)

- **Dificultad:** Alta.
- **Regla:** `PUT foreign-trade/loading-orders/{id}/items` recibe `items: [{ loadingOrderItemId?, warehouseStorageProductId, warehouseStorageCargoUnitId?, quantity }]` y `reason`.
  1. **Estado:** la orden debe estar en `Pending` o `InProgress`. Si no → 409 "Solo se pueden modificar órdenes pendientes o en cargue; la orden {n} está {estado}."
  2. **La lista enviada reemplaza a la actual:**

     | Caso | Qué hace |
     |---|---|
     | Ítem existente (por `loadingOrderItemId`) con otra cantidad | Ajusta la reserva por la diferencia: al aumentar valida stock disponible y, en importación, lo nacionalizado disponible (F2-02, mismo mensaje); al disminuir libera la diferencia. Se ajusta también la reserva de la unidad de carga. Se usa `LoadingOrderItem.UpdateQuantity` y `WarehouseReserve.UpdateQuantity`. |
     | Ítem existente que no viene | Se retira y libera toda su reserva. El ítem se borra físicamente (auditado por el `Describe`). |
     | Ítem nuevo (sin `loadingOrderItemId`) | Se valida como en la creación (depósito confirmado, coherencia de unidad de carga, stock, nacionalizado, cliente sin bloqueo) y se reserva con `LoadingOrderItemId`. |

     - Un `loadingOrderItemId` que no es de la orden → 400 "El ítem {id} no pertenece a la orden."
     - Cantidad ≤ 0 → 400 "La cantidad debe ser mayor a cero."
     - Lista vacía → 400 "La orden debe conservar al menos un ítem; si ya no sale mercancía, cancélela."
  3. Motivo de 10 a 500 caracteres: "El motivo de la modificación debe tener entre 10 y 500 caracteres."
  4. Todo en una transacción. Auditoría con `Describe("Modificación de la orden {n}: {k} ítems modificados, {r} retirados, {a} agregados. Motivo: {motivo}")`.
  5. Si la orden está `InProgress`: notificación a `Warehouse` "La orden {n} fue modificada: revise las cantidades antes de cargar."
  6. **Diferencia con el legacy:** `modificarsalida.php` modificaba la salida ya despachada. En la v2, después del cargue se revierte (F3-07) y se crea otra orden.
- **Evidencia:**
  - Legacy: `modulos/mod_salidas/modificarsalida.php:132-138` (borra los productos de la salida y actualiza el encabezado), `:511-516` y `:578-583` (vuelve a insertar con las cantidades nuevas); `modulos/mod_salidas/eliminarproductosalida.php:35` (quita un producto).
  - v2: sin endpoint de edición (`ForeignTradeController.cs:870-1030`).
- **Archivos:**
  - `Wms.Application/ForeignTrade/Commands/UpdateLoadingOrderItems/*` (nuevo).
  - `Wms.Application/ForeignTrade/Common/Services/LoadingOrderReservationService.cs` (nuevo, scoped): `ReserveAsync`, `AdjustAsync` y `RemoveAsync`. También lo usan `CreateLoadingOrder` y F3-08.
  - `LoadingOrder.cs` (modifica: `EnsureItemsEditable()`, `RemoveItem(Guid itemId)`).
  - `Wms.Api/Controllers/v1/LoadingOrderCorrectionsController.cs` (nuevo; `[Route("foreign-trade")]`, `ForeignTradeAccess`).
  - `Wms.Api/Controllers/v1/Requests/LoadingOrderCorrectionRequests.cs` (nuevo).
- **Contrato:** C-F3-03.
- **Esquema:** ninguno más que F3-01.
- **Efectos secundarios:** cambios de `ReservedStock` y `AvailableStock`; notificación a Bodega.
- **Pruebas** (`Wms.Tests/ForeignTrade/LoadingOrderEditPlanTests.cs`, nuevo). La función pura `LoadingOrderEditPlan.Build(actual, enviados)` clasifica en modificar, retirar y agregar:

  | Actual | Enviado | Resultado |
  |---|---|---|
  | A = 5 | A = 8 | modificar A +3 |
  | A = 5 | A = 2 | modificar A −3 |
  | A y B | solo A | retirar B |
  | A | A y C nuevo | agregar C |
  | A | lista vacía | error |
  | A | id desconocido | error |

- **Terminado cuando:** una orden pendiente cambia sus cantidades y las reservas quedan exactas.
- **Riesgo:** reservas descuadradas. Se mitiga con la transacción, el emparejamiento por `LoadingOrderItemId` y las pruebas.

---

#### F3-04 · Anular la guía de salida (GAP-006, LEGACY-FUNC-159, §B.4.4)

- **Dificultad:** Alta.
- **Regla:** `POST foreign-trade/dispatch-guides/{id}/cancel` recibe `reason` (10 a 500 caracteres: "El motivo de la anulación debe tener entre 10 y 500 caracteres.").
  1. **Validación:**
     - Guía inexistente → 404 "La guía no existe."
     - Guía ya anulada → 409 "La guía {n} ya está anulada."
  2. **Efecto** (en una transacción):
     - `DispatchGuide.Cancel(userId, reason)` (nuevo) guarda `CancelledAt`, `CancelledById` y `CancellationReason`. La guía conserva su número, que no se reutiliza.
     - Por cada factura con líneas de la guía (`InvoiceItem.DispatchGuideId`):
       - Si está en `Draft` o `PendingApproval`, sin pagos (`AmountPaid` nulo o 0) y no consolidada → `Invoice.Cancel(userId, "Guía {n} anulada: {motivo}")`.
       - En cualquier otro caso no se toca y queda en `invoicesToReview`.
  3. **Aviso a Facturación:** si hay facturas para revisar, después del commit se notifica a `Billing`, nivel Warning:
     - Título: "Guía anulada con factura emitida".
     - Mensaje: "La guía {n} de la orden {o} fue anulada. Revise la factura {número o 'sin número'} ({estado}, {total:N0}): el WMS no la modificó."
  4. La orden de cargue no cambia de estado: la guía no la despacha (regla ABO-1).
  5. **Efectos en guías posteriores:**
     - `DispatchGuideBalanceService` excluye las líneas de guías anuladas al sumar lo despachado antes.
     - Se puede emitir otra guía para la misma orden si la anterior está anulada. La validación actual "Ya existe una guía de salida para esta orden de cargue." pasa a contar solo guías no anuladas, en importación y en exportación.
  6. **Presentación:** los listados, el detalle y el ZIP por depósito muestran `isCancelled`, `cancelledAt` y `cancellationReason`. El PDF de una guía anulada lleva la marca de agua "ANULADA".
- **Evidencia:**
  - Legacy: `bodegas_schema.sql:510-523` (la guía tiene `estado`); `eliminarsalida.php:87-124` (al anular la salida, la guía queda sin salida vigente).
  - v2: `Wms.Domain/Entities/Warehouse/DispatchGuide.cs` (sin anulación); `CreateDispatchGuideCommandHandler.cs:121-128` y `CreateExportDispatchGuideCommandHandler.cs:76-81` (una guía por orden); `DispatchGuideBalanceService.cs:35-41` (solo excluye órdenes canceladas).
- **Archivos** (todos modifica, salvo el nuevo):
  - `DispatchGuide.cs`
  - `Wms.Infrastructure/Persistence/Configurations/Warehouse/DispatchGuideConfiguration.cs`
  - `Wms.Application/ForeignTrade/Commands/CancelDispatchGuide/*` (nuevo)
  - `DispatchGuideBalanceService.cs`
  - `CreateDispatchGuideCommandHandler.cs` y `CreateExportDispatchGuideCommandHandler.cs`
  - `Wms.Application/ForeignTrade/Common/Services/DispatchGuidePdfService.cs`
  - DTOs y handlers de `GetDispatchGuides` y `GetDispatchGuidePerDepositZip`
  - `Wms.Application/Billing/Common/Services/InvoiceCancellationPolicy.cs` (nuevo, puro): `CanAutoCancel(status, amountPaid, isConsolidated)`
  - `LoadingOrderCorrectionsController.cs`
- **Contrato:** C-F3-04.
- **Esquema:** `dispatch_guides.cancelled_at timestamptz NULL`, `cancelled_by_id uuid NULL`, `cancellation_reason varchar(500) NULL`.
- **Efectos secundarios:** facturas anuladas o para revisar; notificación a Facturación; saldos de guías posteriores.
- **Pruebas:**
  - `Wms.Tests/Billing/InvoiceCancellationPolicyTests.cs` (nuevo):

    | Estado | Pagado | Consolidada | Resultado |
    |---|---|---|---|
    | `Draft` | 0 | no | true |
    | `PendingApproval` | nulo | no | true |
    | `Draft` | 1 | no | false |
    | `Approved` | 0 | no | false |
    | `Paid` | total | no | false |
    | `Draft` | 0 | sí | false |

  - `DispatchGuideCancelTests`: la segunda anulación → `ConflictException`.
- **Terminado cuando:** una guía anulada deja de contar en los saldos y se puede emitir otra para la orden.
- **Riesgo:** una factura pagada sigue vigente. Es la decisión §B.4.4: Facturación la revisa en SIIGO.

---

#### F3-05 · Ciclos de facturación: unión legacy y v2 (GAP-008, RN-013)

- **Dificultad:** Media.
- **Regla:**
  1. `BillingCycle` suma `Days15`, `Days30`, `Days90`, `Days180` y `Days360` a los actuales (`Weekly`, `Biweekly`, `Monthly`, `OnDemand`). La columna es texto: no cambia el esquema.
  2. **Longitudes y etiquetas:**

     | Valor | Longitud | Etiqueta |
     |---|---|---|
     | `Weekly` | 7 días | Semanal (7 días) |
     | `Biweekly` | 14 días | Quincenal (14 días) |
     | `Days15` | 15 días | Quincenal (15 días) |
     | `Monthly` | 1 mes calendario | Mensual (mes calendario) |
     | `Days30` | 30 días | Mensual (30 días) |
     | `Days90` | 90 días | Trimestral (90 días) |
     | `Days180` | 180 días | Semestral (180 días) |
     | `Days360` | 360 días | Anual (360 días) |
     | `OnDemand` | sin períodos automáticos | Bajo demanda |

  3. Endpoint nuevo `GET billing/configurations/cycles` que devuelve `[{ value, label, days }]`, con `days` nulo en `Monthly` y `OnDemand`. El frontend arma el select con él.
  4. **Factura consolidada** (`BillingService.CalculateConsolidationPeriod`):
     - `Days15` usa la ventana quincenal.
     - `Days30`, `Days90`, `Days180` y `Days360` usan la ventana mensual.
     - Los demás no cambian.
  5. **Migración (F6-02):** los días del legacy se mapean así: 15 → `Days15`, 30 → `Days30`, 90 → `Days90`, 180 → `Days180` y 360 → `Days360`.
- **Evidencia:**
  - Legacy: `modulos/mod_clientes/modificarcliente.php:466-471` (opciones 15, 30, 90, 180 y 360; valor por defecto 15 en `bodegas_schema.sql:186`).
  - v2: `Wms.Domain/Enums/BillingCycle.cs`; `StorageBillingService.cs:331-338` (longitudes) y `:375-377` (`OnDemand` no abre período); `Wms.Application/Billing/Common/Services/BillingService.cs:182-190` (ventana consolidada; el valor por defecto ya es la mensual).
- **Archivos:**
  - `BillingCycle.cs` (modifica).
  - `Wms.Application/Billing/Common/Services/BillingCycleCatalog.cs` (nuevo, puro: longitudes y etiquetas).
  - `BillingService.cs` (modifica).
  - `Wms.Application/Billing/Queries/GetBillingCycles/*` (nuevo).
  - `Wms.Api/Controllers/v1/BillingCyclesController.cs` (nuevo; `[Route("billing")]`, `BillingAccess`).
- **Contrato:** C-F3-05 (catálogo) y C-F3-06 (configuración: valores nuevos).
- **Esquema:** ninguno.
- **Efectos secundarios:** ninguno hasta F3-06.
- **Pruebas** (`Wms.Tests/Billing/BillingCycleCatalogTests.cs`, nuevo): cada valor devuelve su longitud y etiqueta; `OnDemand` no tiene longitud; la ventana consolidada de `Days15` es la quincenal y la de `Days90` es la mensual.
- **Terminado cuando:** se puede guardar un cliente con `Days90` y el catálogo lista los nueve ciclos.
- **Riesgo:** bajo.

---

#### F3-06 · Períodos de almacenamiento con la regla legacy (RN-050, RN-051, LEGACY-FUNC-201, 202 y 234; P7 y P8)

- **Dificultad:** Muy alta.
- **Regla** (para todos los ciclos, P7; fechas en días calendario de Colombia). Todo cálculo va en la clase pura `StoragePeriodCalculator`.
  1. **Primer período:**
     - Inicio `S1` = `ColombiaTime.DateOf(EntryDate)`. Si la fecha de ingreso es futura, hoy (regla actual «nunca en el futuro»).
     - Fin `E = S + N días`, o `S.AddMonths(1)` en `Monthly`. Es decir, un período de 15 días que empieza el 01/01 termina el 16/01, como el legacy (`fechafin = fechainicio + período`).
     - Fecha límite `L = E + 3 días`.
  2. **Período siguiente:** `S(k+1) = E(k) + 1 día`, con fin y límite por la misma regla.
  3. **Cómo se guardan:**
     - `PeriodStart` = `S` a las 00:00 de Colombia (−05:00).
     - `PeriodEnd` = `E` a las 00:00 de Colombia (la fecha de fin, inclusiva).
     - `LimitDate` (nuevo, `DateOnly`) = `L`.
     - Las facturas imprimen «período dd/MM/yyyy - dd/MM/yyyy» con `S` y `E`.
  4. **Renovación** (job `StoragePeriodAutoCloseBackgroundService` → `BillingJobService.AutoCloseExpiredStoragePeriodsAsync`):
     - Se procesan los períodos `Open` con `LimitDate < hoy`, es decir hoy ≥ E + 4. Hoy la condición es `PeriodEnd <= now`.
     - Por depósito: se cierran esos períodos y se abre el siguiente con `S = E + 1` si el depósito aún tiene stock (`OpenPeriodWithInvoiceAsync` ya no abre nada si no hay cargos).
     - `GetNextPeriodExpirationAsync` devuelve `LimitDate + 1 día` a las 00:00 de Colombia del período abierto más próximo.
     - Si el siguiente período ya venció (por ejemplo, confirmación tardía), el job lo renueva en su próxima pasada, 5 minutos después, hasta ponerse al día. El legacy generaba todos los faltantes en una sola pasada.
  5. **Gracia de 3 días:** la renovación espera al día siguiente a la fecha límite. Si el stock llega a 0 hasta la fecha límite inclusive, el período abierto se cierra por agotamiento (regla actual `CloseDepletedProductPeriodsAsync`, `StorageBillingService.cs:822-867`, que no cambia) y ya no se renueva. Así, una salida dentro de los 3 días siguientes al fin no genera otro período, como el legacy (`cron.php:69`: solo genera si la fecha de la última salida es mayor que la fecha límite).
  6. **Otras aperturas usan la misma regla:**
     - La confirmación, con `S1`.
     - El camión tardío en un depósito sin período abierto (`HandleLateTruckAsync`): contiguo al último período (`E + 1`); si no hay ninguno, `S1`.
     - El rebase por cambio de fecha de ingreso (`RecalculateCoreAsync` con `newPeriodStart`, `StorageBillingService.cs:497-512`): `S` = nueva fecha y su fin.
     - El cierre manual con renovación (`CloseStoragePeriodsHandler.cs:51,63`): siguiente inicio `E + 1` si no es futuro; si lo es (cierre anticipado), hoy.
     - La devolución de mercancía de F3-07.
  7. **Vencimiento de la factura** (P8): sin cambio. Sigue siendo emisión + días de plazo del cliente (30 por defecto). La fecha límite se muestra en el período.
  8. **Importes:** se calculan con el motor de acuerdos, como hoy (`ResolveStorageChargesAsync`), y se cobran por adelantado. El número SIIGO lo asigna Facturación (RN-051, sin cambio).
  9. `GET billing/storage-periods` y `GET billing/storage-periods/{id}` exponen `limitDate`.
  10. **Inconsistencia del legacy que no se replica:** la rama del cron sin períodos facturados usaba `ceil(días/período)` sin la gracia de 3 días. En la v2 el primer período siempre se factura al confirmar, así que aplica la rama con gracia.
- **Evidencia:**
  - Legacy `cron.php`:
    - `:28-51`: saldo 0 → hasta la última salida; `numperiodos = ceil(días/período)`.
    - `:61-94`: con períodos facturados, solo genera si la fecha pasa la fecha límite del último; `fin = inicio + período`, `límite = fin + 3`, siguiente inicio = `fin + 1`.
    - `:95-120`: primer período desde `fecha_deposito`.
  - Legacy `includes/funciones.php:234-239`: `dias_transcurridos = floor(|Δ|/86400)`.
  - v2:
    - `StorageBillingService.cs:331-338` (fin = inicio + 7, 14 días o 1 mes).
    - `Wms.Application/Billing/Jobs/BillingJobService.cs:168-279` (renueva al vencer `PeriodEnd`, contiguo al fin) y `:336-343` (siguiente despertar = `PeriodEnd` más próximo).
    - `Wms.Application/Billing/Common/Services/StoragePeriodStart.cs`.
- **Archivos:**
  - `Wms.Application/Billing/Common/Services/StoragePeriodCalculator.cs` (nuevo, puro): `First(DateOnly entry, DateOnly today, BillingCycle)`, `Next(DateOnly previousEnd, BillingCycle)`, `ShouldRenew(DateOnly limit, DateOnly today)` y `ToInstant(DateOnly)`.
  - `StorageBillingPeriod.cs` (modifica: `LimitDate`; `Create` recibe el límite).
  - `StorageBillingPeriodConfiguration.cs` (modifica).
  - `StorageBillingService.cs` (modifica: `CalculatePeriodEnd` se reemplaza por el calculador, en `OpenPeriodWithInvoiceAsync` y en `RecalculateCoreAsync` con rebase).
  - `StoragePeriodStart.cs` (modifica o retira: pasa a delegar en el calculador).
  - `BillingJobService.cs` (modifica: selección por `LimitDate` y siguiente vencimiento).
  - `Wms.Application/Billing/Commands/CloseStoragePeriods/CloseStoragePeriodsHandler.cs` (modifica: siguiente inicio con el calculador).
  - `StorageRecalculationTrigger.cs` (modifica: apertura contigua).
  - `ConfirmStorageDepositHandler.cs` (modifica: inicio con `S1`).
  - `Wms.Application/Billing/Common/DTOs/StoragePeriodMapper.cs` y su DTO (modifica: `LimitDate`).
- **Contrato:** C-F3-07.
- **Esquema:** `storage_billing_periods.limit_date date NULL`. Los períodos anteriores quedan nulos; para ellos el job toma `E = ColombiaTime.DateOf(PeriodEnd)` y `L = E + 3 días`. La aritmética actual (fin = inicio + N) es la misma del legacy (`fechafin = fechainicio + período`), así que el siguiente inicio `E + 1` también vale para ellos.
- **Efectos secundarios:** cambia cuándo se generan las facturas de renovación (3 días después del fin) y las fechas de los períodos nuevos.
- **Pruebas** (`Wms.Tests/Billing/StoragePeriodCalculatorTests.cs`, nuevo):

  | Caso | Datos | Resultado |
  |---|---|---|
  | Primer período `Days15` | ingreso 2026-01-01 | inicio 01/01, fin 16/01, límite 19/01 |
  | Siguiente `Days15` | fin anterior 16/01 | inicio 17/01, fin 01/02, límite 04/02 |
  | Renovación | límite 19/01 | hoy 19/01 → false; hoy 20/01 → true |
  | `Monthly` desde fin de mes | inicio 31/01 | fin 28/02 (2026), siguiente inicio 01/03 |
  | `Weekly` | inicio 2026-09-29 | fin 06/10 |
  | `Days360` con año bisiesto | inicio 2027-03-01 | fin 2028-02-25 |
  | Ingreso futuro | ingreso mañana | inicio = hoy |
  | Salida el mismo día | ingreso y salida el 2026-01-01 | un solo período (sin renovación porque se cierra por agotamiento) |
  | Instante | `ToInstant(2026-01-17)` | `2026-01-17T00:00:00-05:00` |

  Además, prueba de cotejo con el legacy: un depósito de 15 días con ingreso el 01/01 y última salida el 18/01 (antes del límite 19/01) → 1 período; con salida el 20/01 → 2 períodos.
- **Terminado cuando:** los períodos nuevos siguen la tabla y el job renueva al pasar la fecha límite.
- **Riesgo:** importes o fechas distintos a los del legacy en casos límite. Se mitiga con las pruebas de cotejo, la revisión humana y la prueba con datos reales (roadmap 6.6).

---

#### F3-07 · Revertir la salida después del cargue (GAP-006, RN-038, LEGACY-FUNC-159)

- **Dificultad:** Muy alta.
- **Regla:** `POST foreign-trade/loading-orders/{id}/revert` recibe `reason` (10 a 500 caracteres: "El motivo de la reversión debe tener entre 10 y 500 caracteres.").
  1. **Validación:**
     - Orden en `Loaded`, `Dispatched` o `Complete`. Si no → 409 "Solo se revierte una orden ya cargada; la orden {n} está {estado}."
     - Sin guía vigente (no anulada). Si la tiene → 409 "Anule primero la guía {g} de la orden {n}."
  2. **Efecto** (en una transacción):
     1. **Cantidad a devolver** de cada ítem: `q = LoadedQuantity`. Para órdenes ejecutadas antes de F3-01 (nulo), la suma de los movimientos `Out` con `SourceType = LoadingOrder`, `SourceId` = la orden y ese producto.
     2. Por cada ítem con `q > 0`:
        - `WarehouseStorageProduct.ReturnDispatchedStock(q)` (nuevo): `CurrentStock += q` y recalcula `AvailableStock`. Exige `q > 0` y que el stock no supere `ReceivedQuantity`: "La devolución dejaría más stock que la cantidad del depósito."
        - Movimiento `In` con `SourceType = LoadingOrderReversal` (valor nuevo de `SourceTypeMovements`), `SourceId` = la orden, motivo "Reversión de la orden {n}: {motivo}".
        - Unidad de carga: `WarehouseStorageCargoUnitProduct.RevertDispatch(q)` (nuevo; `DispatchedQuantity −= q`, nunca negativo) y `RefreshStatus()`.
     3. Cada depósito afectado que estaba `Closed` → `WarehouseStorage.ReopenAfterReversal()` (nuevo): pasa a `Confirmed` e `IsActive = true`.
     4. `LoadingOrder.Revert(userId, reason)` (nuevo): estado `Reverted`, `RevertedAt`, `RevertedById` y `ReversalReason`. Las reservas ya estaban inactivas.
     5. El servicio de salida en báscula y su pesaje no cambian: quedan como registro del camión.
        - **Diferencia con el legacy**, que movía los pesajes a una salida nueva «incompleta»: en la v2 se crea otra orden y otro pesaje, o se usa el pesaje compartido de F4-07.
     6. Las posiciones de bodega las trata F4-02: la mercancía devuelta queda «por ubicar».
  3. **Facturación**, después del commit, por depósito afectado (`StorageRecalculationTrigger.HandleStockReturnedAsync`, nuevo):
     - Si tiene un período abierto → no se toca: ya se cobró por adelantado con el stock de su apertura.
     - Si no tiene y su último período se cerró por agotamiento (`ClosedById` nulo) con fin ≥ hoy → `StorageBillingPeriod.ReopenAfterStockReturn()` (nuevo): vuelve a `Open`, con `ClosedAt` y `ClosedById` nulos. No cambia la factura.
     - Si no → abre el siguiente período contiguo (F3-06) con su factura.
  4. **Notificaciones:** a `Warehouse`, nivel Info, título "Salida revertida", mensaje "La orden {n} fue revertida: la mercancía volvió a los depósitos {lista}. Ubíquela de nuevo." Las advertencias de facturación salen por el notificador actual.
- **Evidencia:**
  - Legacy: `modulos/mod_salidas/eliminarsalida.php:87-124` (borra `producto_salida` y devuelve el saldo, reactiva posiciones, deja la salida `eliminado` con motivo y crea una salida `incompleto` con los pesajes).
  - v2: sin reversión (`LoadingOrder.cs`, `ExecuteLoadingOrderCommandHandler.cs`).
- **Archivos:**
  - `LoadingOrder.cs`, `WarehouseStorageProduct.cs`, `WarehouseStorageCargoUnitProduct.cs`, `WarehouseStorage.cs` y `StorageBillingPeriod.cs` (modifica).
  - `Wms.Domain/Enums/SourceTypeMovements.cs` (modifica: `LoadingOrderReversal`, `WeighingVoid` y `StorageCancellation`; los dos últimos se usan en F3-08 y F3-09).
  - `LoadingOrderConfiguration.cs` (modifica).
  - `Wms.Application/ForeignTrade/Commands/RevertLoadingOrder/*` (nuevo).
  - `StorageRecalculationTrigger.cs` (modifica).
  - `LoadingOrderCorrectionsController.cs` (modifica).
  - DTOs de la orden: estado `Reverted`, `revertedAt` y `reversalReason`.
- **Contrato:** C-F3-08.
- **Esquema:** `loading_orders.reverted_at timestamptz NULL`, `reverted_by_id uuid NULL`, `reversal_reason varchar(500) NULL`.
- **Efectos secundarios:** stock, movimientos `In`, unidades de carga, depósitos reabiertos, períodos reabiertos o nuevos, notificaciones.
- **Pruebas:**
  - `WarehouseStorageProductTests` (modifica):
    - Recibido 10, actual 4 → `ReturnDispatchedStock(6)` deja 10.
    - `ReturnDispatchedStock(7)` → error.
    - `ReturnDispatchedStock(0)` → error.
  - `WarehouseStorageCargoUnitTests` (modifica): despachado 5 → `RevertDispatch(5)` deja 0 y el estado `InWarehouse`; `RevertDispatch(6)` → error.
  - `LoadingOrderTransitionsTests`: `Revert` desde `Loaded`, `Dispatched` y `Complete` → `Reverted`; desde `Pending` → error.
  - `WarehouseStorage.ReopenAfterReversal` desde `Closed` → `Confirmed`; desde `Confirmed` → sin cambio.
  - `StorageBillingPeriod.ReopenAfterStockReturn` desde un período `Closed` con `ClosedById` nulo → `Open`; con `ClosedById` → error "Solo se reabre un período cerrado por agotamiento."
- **Terminado cuando:** revertir una orden cargada devuelve el stock, reabre el depósito cerrado y deja el rastro en movimientos y auditoría.
- **Riesgo:** doble cobro o cobro faltante del almacenamiento. Se mitiga con la regla del punto 3, la revisión humana y la prueba con datos reales.

---

#### F3-08 · Anular un depósito con sus efectos (GAP-011, RN-018, RN-025, §B.4.5)

- **Dificultad:** Muy alta.
- **Regla:** endpoint existente `POST foreign-trade/warehouse-storages/{id}/cancel`.
  1. **Motivo:** pasa a ser obligatorio, de 10 a 500 caracteres: "El motivo de la anulación debe tener entre 10 y 500 caracteres."
  2. **Estados** (errores actuales, que pasan a validarse en `WarehouseStorage.Cancel`): `Closed` → "No se puede anular un depósito cerrado."; `Cancelled` → "El depósito ya está anulado."
  3. **Guardas** (409):
     - Una orden en `Loaded`, `Dispatched` o `Complete` tiene ítems del depósito → "El depósito {n} tiene salidas ejecutadas en la orden {o}. Revierta primero la salida."
     - Una entrada del depósito tiene su ciclo de báscula sin terminar (`Status` distinto de `Complete` y de `Canceled`) → "El camión {placa} del depósito {n} aún está en báscula. Termine o anule el pesaje antes de anular el depósito."
  4. **Efectos**, en una transacción, con el servicio compartido `WarehouseStorageCancellationService.CancelAsync(storage, reason, userId)` (que también usa F3-09):
     1. **Órdenes activas** (`Pending` o `InProgress`) con ítems del depósito: se retiran esos ítems y se liberan sus reservas y las de las unidades (`LoadingOrderReservationService.RemoveAsync`, F3-03). Si la orden queda sin ítems → `LoadingOrder.Cancel("Depósito {n} anulado")`.
     2. **Stock:** por cada producto con `CurrentStock > 0`, movimiento `Out` con `SourceType = StorageCancellation`, cantidad = `CurrentStock` y motivo "Anulación del depósito {n}: {motivo}"; luego `VoidStock()`. Aplica también en Borrador; hoy no se hace.
     3. **Períodos abiertos:** `Close(userId)`.
     4. **Sus facturas** (distintas): se aplica `InvoiceCancellationPolicy` (F3-04). Las que se pueden, se anulan con "Depósito {n} anulado: {motivo}"; el resto va a `invoicesToReview`.
     5. **Servicio del depósito** (relación 1:1; el depósito adicional tiene su propio servicio, `InitiateStorageWeighingHandler.cs:783-790`): `ServiceRecord.VoidService(userId)` (nuevo): pasa a `Discarded` desde cualquier estado, con `DiscardedAt` y `DiscardedById`; si ya está `Discarded` no hace nada. Así báscula no lo ofrece como operación en curso (`GetRecoverableOperationsHandler.cs:87`) ni lo precarga por carta porte (`GetWeighbridgeLookupHandler.cs:81`). Un camión nuevo con el mismo documento crea otro depósito, porque el buscador de F1-02 excluye los anulados; es el equivalente del legacy, que cambiaba el número por «ELIMINADO».
     6. `WarehouseStorage.Cancel(reason, userId)` (modifica): guarda `CancelledAt`, `CancelledById` y `CancellationReason`, y conserva la nota en `Observations`.
     7. Los levantes quedan como historia.
  5. **Notificaciones** después del commit:
     - A `Warehouse`, por cada orden `InProgress` afectada: "La orden {o} perdió los ítems del depósito anulado {n}."
     - A `Billing`, si hay facturas para revisar: título "Depósito anulado con factura emitida", mensaje "El depósito {n} fue anulado. Revise la factura {número} ({estado}, {total:N0}): el WMS no la modificó."
  6. La respuesta resume los efectos (ver contrato).
- **Evidencia:**
  - Legacy:
    - `modulos/mod_ingresos/eliminaringreso.php:62-76`: anula el ingreso con motivo, usuario, IP y fecha, y cambia el número por «ELIMINADO».
    - `modulos/mod_depositos/eliminardeposito.php:56-65`: desvincula la mercancía y borra el depósito.
    - `cron.php:3-9`: solo los ingresos activos generan períodos, así que un ingreso anulado deja de facturarse.
  - v2: `Wms.Application/ForeignTrade/Commands/CancelWarehouseStorage/CancelWarehouseStorageHandler.cs:26-39` (en Borrador no pone el stock en cero, no libera reservas, no cierra períodos ni anula facturas, no deja movimiento).
- **Archivos:**
  - `CancelWarehouseStorageCommand.cs` y `CancelWarehouseStorageHandler.cs` (modifica); `CancelWarehouseStorageCommandValidator.cs` (nuevo).
  - `Wms.Application/ForeignTrade/Common/Services/WarehouseStorageCancellationService.cs` (nuevo, scoped).
  - `WarehouseStorage.cs` (modifica) y `WarehouseStorageConfiguration.cs` (modifica).
  - `Wms.Domain/Entities/Services/ServiceRecord.cs` (modifica: `VoidService`).
  - `ForeignTradeController.cs` (modifica: `CancelWarehouseStorageRequest` obligatorio y el DTO de respuesta).
  - `CancelWarehouseStorageResponseDto` (modifica).
- **Contrato:** C-F3-09.
- **Esquema:** `warehouse_storages.cancelled_at timestamptz NULL`, `cancelled_by_id uuid NULL`, `cancellation_reason varchar(500) NULL`.
- **Efectos secundarios:** órdenes modificadas o canceladas, stock en cero con movimiento, períodos cerrados, facturas anuladas o para revisar, notificaciones.
- **Pruebas:**
  - `WarehouseStorageCancelTests` (nuevo): `Cancel` guarda motivo, usuario y fecha; con motivo vacío → error "El motivo de la anulación es obligatorio."
  - `DepositCancellationPlan` puro: dada una lista de órdenes con ítems de varios depósitos, calcula qué ítems retirar y qué órdenes cancelar:
    - Una orden con ítems solo del depósito → se cancela.
    - Una orden con ítems de dos depósitos → solo se retiran los del depósito.
- **Terminado cuando:** anular un depósito confirmado con una orden pendiente y factura en Borrador deja la orden sin sus ítems (o cancelada), el stock en 0 con movimiento, los períodos cerrados y la factura anulada.
- **Riesgo:** anular un depósito con facturas pagadas. Se avisa a Facturación.

---

#### F3-09 · Anular un pesaje completo (GAP-005, RN-058, RN-074)

- **Dificultad:** Muy alta.
- **Regla:** `POST weighbridge/cycles/{cycleId}/void` recibe `reason` (10 a 500 caracteres: "El motivo de la anulación debe tener entre 10 y 500 caracteres."). Si el ciclo ya está anulado → 409 "El pesaje ya está anulado."
- **A. Ingreso a depósito** (el ciclo tiene entradas de camión, una por depósito, incluidos los adicionales). Por cada entrada no anulada del ciclo y cada línea del camión con cantidad `q > 0`:

  | Guarda | Respuesta |
  |---|---|
  | `q > AvailableStock` del producto (la mercancía ya se reservó o despachó) | 409 "No se puede anular el pesaje: la mercancía del camión {placa} en el depósito {n} tiene {x} unidades reservadas o despachadas de «{producto}». Revierta o cancele primero la orden {orden}." (`x = despachado + reservado`; `{orden}` = las órdenes vigentes con ítems del producto; si no hay, se omite ". Revierta o cancele primero la orden {orden}" y termina en "de «{producto}».") |
  | Importación: Σ levantes del producto > `ReceivedQuantity − q` | 409 "No se puede anular el pesaje: los levantes de «{producto}» ({x}) superarían la cantidad que queda en el depósito {n} ({y}). Retire primero el levante." |
  | Unidades de carga de la entrada con reservado o despachado > 0 | 409 "No se puede anular el pesaje: la unidad de carga {placa} tiene mercancía reservada o despachada." |

  **Efectos**, en una transacción:
  1. Cada línea del camión: `UpdateDeclaredQuantity(0)` y luego `DepositProductEditing.RecalculateTotals` (baja declarado, recibido y stock en `q`). Si `q > 0`, movimiento `Out` con `SourceType = WeighingVoid`, `SourceId` = la entrada, motivo "Anulación del pesaje {tiquete}: {motivo}".
  2. Las unidades de carga de la entrada se borran (primero sus líneas); queda auditado.
  3. `WarehouseStorageEntry.Void(userId, reason)` (nuevo) guarda `VoidedAt`, `VoidedById` y `VoidReason`.
  4. **Las entradas anuladas se excluyen de:**
     - el peso bruto de facturación (`StorageBillingService.cs:87-91`);
     - los requisitos de confirmación (F1-05);
     - el conteo de camiones.
  5. **Vínculo camión–servicio:** se borran los `ServiceRecordEntryLog` entre la entrada de portería del ciclo y cada servicio cuya entrada se anuló. Así:
     - el conteo de camiones para el cobro lo excluye (`ProcessStoragePaymentHandler.cs:122`);
     - la misma entrada de portería vuelve a la cola y puede pesarse de nuevo. Hoy `InitiateStorageWeighingHandler.cs:208-212` rechaza una entrada con servicio: "El entry log ya tiene un servicio asignado."
  6. Si el depósito se queda sin entradas activas → se anula con `WarehouseStorageCancellationService` (F3-08), con el motivo "Pesaje anulado: {motivo}". El servicio también descarta el `ServiceRecord`. La guarda de «camión en báscula» de F3-08 no aplica aquí: el ciclo es el que se anula.
- **B. Salida de mercancía** (servicio de salida con orden). El servicio se descarta con `ServiceRecord.VoidService` (F3-08):
  - Si la orden está `Dispatched` → `LoadingOrder.RevertDispatchToLoaded()` (nuevo; `DepartureDate` nulo).
  - Si está `Complete` → 409 "La orden {n} está completa; revierta la salida antes de anular el pesaje." (Hoy ningún flujo llama a `LoadingOrder.Complete()`; la regla queda por seguridad.)
  - El stock **no** cambia, igual que el legacy: para devolver la mercancía se usa F3-07.
  - El servicio pasa a `Discarded` y se borra su vínculo con el camión, para que pueda pesarse de nuevo.
- **C. Solo báscula** (OTH001): el servicio pasa a `Discarded` y se borra su vínculo con el camión.
- **Común a A, B y C:**
  - `WeighbridgeCycle.Void(userId, reason)` (nuevo): estado `Canceled` desde cualquier estado, con `VoidedAt`, `VoidedById` y `VoidReason`. `Cancel()` sigue rechazando los completos.
  - **Cobro de báscula:** las facturas del ciclo (`WeighbridgeCycle.InvoiceId` o `WarehouseStorageEntry.WeighbridgeInvoiceId`) siguen `InvoiceCancellationPolicy`: se anulan con "Pesaje {tiquete} anulado: {motivo}" o van a `invoicesToReview`.
  - **Notificaciones**, después del commit:
    - A `ForeignTrade` (caso A), nivel Warning, título "Pesaje anulado", mensaje "Báscula anuló el pesaje del camión {placa} en el depósito {n}. Motivo: {motivo}. Reimprima la etiqueta si cambió la cantidad."
    - A `Billing`, si hay facturas para revisar: "El pesaje del camión {placa} ({tiquete}) fue anulado. Revise la factura {número} ({estado}, {total:N0}): el WMS no la modificó."
    - Si un depósito confirmado conserva stock: `StorageRecalculationTrigger.RecalculateAsync(id, "anulación del pesaje del camión {placa}")`.
  - El historial de báscula muestra los anulados (`voidedAt` y `voidReason`).
- **Evidencia:**
  - Legacy:
    - `modulos/mod_bascula/eliminarentrada.php:66-110`: pesaje `eliminado` con motivo, usuario, IP y fecha; mercancía del pesaje `eliminado`; producto amparado `eliminado` si no está en otro pesaje; recibo y detalle `eliminado`.
    - `modulos/mod_bascula/eliminarsalida.php:66-86`: pesaje, recibo y salida `eliminado`, sin devolver la mercancía.
    - `modulos/mod_bascula/eliminarsolopeso.php:66-84`.
  - v2:
    - `Wms.Application/Weighbridge/Commands/DiscardIncompleteOperation/DiscardIncompleteOperationHandler.cs:40-46` y `ServiceRecord.cs:213-222` (solo operaciones `InTransit`, sin ciclo).
    - `Wms.Domain/Entities/Weighbridge/WeighbridgeCycle.cs` (`Cancel` rechaza `Complete` y no tiene llamadores).
- **Archivos:**
  - Dominio (modifica): `WeighbridgeCycle.cs`, `WarehouseStorageEntry.cs` y `LoadingOrder.cs`.
  - Configuraciones (modifica): `WeighbridgeCycleConfiguration.cs` y `WarehouseStorageEntryConfiguration.cs`.
  - `Wms.Application/Weighbridge/Commands/VoidWeighing/*` (nuevo).
  - `Wms.Application/Weighbridge/Common/Services/WeighingVoidGuard.cs` (nuevo, puro).
  - `StorageBillingService.cs` (modifica: filtro de entradas anuladas).
  - `DepositConfirmationRequirements.cs` (modifica: excluye anuladas).
  - `Wms.Application/Weighbridge/Queries/GetWeighbridgeHistory/*` y `WeighbridgeHistoryDto.cs` (modifica).
  - `Wms.Api/Controllers/v1/WeighbridgeVoidController.cs` (nuevo; `[Route("weighbridge")]`, `ScaleAccess`).
- **Contrato:** C-F3-10 (anular) y C-F3-11 (historial, campos nuevos).
- **Esquema:** `weighbridge_cycles.voided_at`, `voided_by_id`, `void_reason`; `warehouse_storage_entries.voided_at`, `voided_by_id`, `void_reason` (`timestamptz NULL`, `uuid NULL`, `varchar(500) NULL`).
- **Efectos secundarios:** stock, movimientos, unidades borradas, depósito posiblemente anulado, facturas, recálculo, notificaciones.
- **Pruebas** (`Wms.Tests/Weighbridge/WeighingVoidGuardTests.cs`, nuevo):

  | Caso | Datos | Resultado |
  |---|---|---|
  | Sin reservas ni despachos | disponible 10, q 10 | válido |
  | Parte reservada | disponible 9, q 10 | error con x = 1 |
  | Todo despachado | actual 0, recibido 10, q 10 | error con x = 10 |
  | Levantes que no caben | levantes 8, recibido 10, q 5 | error (8 > 5) |
  | Levantes que caben | levantes 5, recibido 10, q 5 | válido |
  | Unidad con reserva | reservado 1 | error |
  | Cantidad 0 | q 0 | no genera movimiento |

  En dominio:
  - `WeighbridgeCycle.Void` desde `Complete` → `Canceled`; la segunda vez → error.
  - `WarehouseStorageEntry.Void` guarda los tres campos.
  - `LoadingOrder.RevertDispatchToLoaded` desde `Dispatched` → `Loaded`; desde `Loaded` → error.
- **Terminado cuando:** anular el pesaje de un camión adicional baja el stock del depósito en lo que declaró ese camión y deja su rastro; anular el único camión anula el depósito.
- **Riesgo:** anular pesajes con mercancía ya comprometida. Se mitiga con las guardas y la revisión humana.

---

#### F3-10 · Anular la factura de almacenamiento y refacturar (GAP-007, RN-052, P9)

- **Dificultad:** Alta.
- **Regla:**
  1. **Anular** (endpoint existente `PATCH billing/invoices/{id}/cancel`): la validación no cambia. Si la factura tiene líneas de almacenamiento (`StorageBillingPeriodId`), después del commit se notifica a `Billing`:
     - Título: "Factura de almacenamiento anulada".
     - Mensaje: "La factura {número o 'sin número'} fue anulada. Sus períodos de almacenamiento quedaron por refacturar: use «Refacturar» en la factura anulada."
     - Los períodos siguen apuntando a la factura anulada. «Por refacturar» se deduce: la factura del período está `Cancelled` y no tiene `ReissuedAsInvoiceId`.
  2. **Refacturar** (`POST billing/invoices/{id}/reissue`, `BillingAccess`, sin cuerpo):

     | Condición | Respuesta |
     |---|---|
     | La factura no está anulada | 409 "Solo se puede refacturar una factura anulada; la factura {n} está {estado}." |
     | Ya se refacturó | 409 "La factura {n} ya fue refacturada como {m}." |
     | No tiene líneas de almacenamiento | 400 "La factura {n} no tiene períodos de almacenamiento; genere de nuevo el cobro desde su operación." |

     **Efecto** (en una transacción), con `Invoice.CreateReissueOf(Invoice cancelled, DateTimeOffset dueDate)` (nuevo):
     1. Se crea una factura nueva en `Draft` con:
        - el mismo destinatario (cliente, o una copia del destinatario no registrado), `IsConsolidated`, período, notas y detalle;
        - `InvoiceNumber` nulo (Facturación asigna el SIIGO);
        - vencimiento = ahora + días de plazo del cliente (30 si no tiene configuración).
     2. Cada línea se clona con servicio, descripción, cantidad, precio, tasa de impuesto, producto, origen, período y guía. Las sobrescrituras no se clonan: la línea clonada lleva los valores vigentes de la original.
     3. **Enlaces:**
        - `ReissuedFromInvoiceId` en la nueva y `ReissuedAsInvoiceId` en la anulada.
        - Los `StorageBillingPeriod` de la anulada pasan a la nueva (`LinkInvoice`).
        - Las referencias `DispatchGuide.InvoiceItemId`, `WeighbridgeCycle.InvoiceId` y `WarehouseStorageEntry.WeighbridgeInvoiceId` que apuntaban a la anulada se apuntan a la nueva (o a su línea equivalente).
     4. Después del commit, por cada depósito con un período **abierto** reenlazado: `StorageRecalculationTrigger.RecalculateAsync(id, "refacturación")`, que recalcula con el motor de acuerdos. Los períodos cerrados conservan los importes clonados.
     5. La respuesta es el detalle de la factura nueva (`InvoiceDetailDto`).
  3. `GET billing/pending-deposits` agrega por depósito `periodsPendingReissue` (cantidad de períodos cuya factura está anulada sin refacturar).
- **Evidencia:**
  - Legacy: `modulos/mod_facturacion/eliminarfactura.php:56-65` (el período vuelve a `activo` sin número, fecha, detalle ni observaciones, y Facturación lo factura otra vez desde `facturarciigo.php`).
  - v2: `Wms.Application/Billing/Commands/CancelInvoice/CancelInvoiceHandler.cs`; `Wms.Domain/Entities/Billing/Invoice.cs:325-343`; `StorageBillingService.cs:488-489` (el recálculo omite las anuladas).
- **Archivos:**
  - `Invoice.cs` (modifica: `ReissuedFromInvoiceId`, `ReissuedAsInvoiceId`, `CreateReissueOf`, `MarkReissuedAs`).
  - `InvoiceItem.cs` (modifica: `CloneFor(Guid newInvoiceId)`).
  - `Wms.Infrastructure/Persistence/Configurations/Billing/InvoiceConfiguration.cs` (modifica).
  - `CancelInvoiceHandler.cs` (modifica: notificación).
  - `Wms.Application/Billing/Commands/ReissueInvoice/*` (nuevo).
  - `Wms.Application/Billing/Queries/GetPendingDeposits/*` y su DTO (modifica).
  - `Wms.Api/Controllers/v1/InvoiceReissueController.cs` (nuevo; `[Route("billing")]`, `BillingAccess`).
  - `Wms.Application/Billing/Common/DTOs/InvoiceDto.cs` (modifica `InvoiceDetailDto`, línea 38: `reissuedFromInvoiceId`, `reissuedAsInvoiceId`).
- **Contrato:** C-F3-12 (anular, efecto nuevo), C-F3-13 (refacturar) y C-F3-14 (pendientes).
- **Esquema:** `invoices.reissued_from_invoice_id uuid NULL` y `invoices.reissued_as_invoice_id uuid NULL`, con FK a `invoices(id)` `ON DELETE RESTRICT` e índices.
- **Efectos secundarios:** una factura nueva, enlaces movidos, recálculo del período abierto, notificaciones.
- **Pruebas** (`Wms.Tests/Domain/Billing/InvoiceReissueTests.cs`, nuevo):
  - `CreateReissueOf` de una anulada con 2 líneas → nueva en `Draft` con 2 líneas y el mismo total, número nulo y el mismo destinatario.
  - De una no anulada → error.
  - `MarkReissuedAs` dos veces → error.
  - `CloneFor` copia período y guía.
- **Terminado cuando:** anular y refacturar una factura de almacenamiento deja los períodos ligados a la factura nueva y el período abierto recalculado.
- **Riesgo:** enlaces rotos. Se mitiga con la transacción y las pruebas.

---

### C.4 Fase 4 — Bodega y mercancía

> **Estado: ✅ COMPLETADA el 2026-09-30** (F4-01 a F4-10, implementados en `develop` en una sola pasada por indicación del usuario). `dotnet build Wms.sln` sin errores y `dotnet test Wms.Tests` en verde (695 pruebas; 642 antes de la fase). Los ocho criterios de salida funcionales se comprobaron además contra un Postgres temporal (46 comprobaciones de extremo a extremo), y la prueba de la fase 3 se repitió sin regresiones.
> **Pendiente del usuario:** revisar el diff, generar las migraciones y hacer el commit. Al cierre de la fase no se había generado ninguna migración de paridad: el modelo lleva 88 operaciones pendientes contra el snapshot, 50 de las fases 1 a 3 y 38 de esta (§F.1, filas 16 a 22). Los datos iniciales opcionales de F4-01 (§F.3) se agregan a mano al generar su migración.
> **Desviaciones respecto al texto de los ítems** (ninguna cambia una decisión de §A.4 ni de §B.4):
> 1. **F4-07 y F4-08 — depósito «confirmado».** Se acepta también `Closed`: un cargue que deja el depósito sin stock lo cierra, y entonces ninguna orden cargada podía salir con el pesaje compartido ni con el tiquete. `Draft` y `Cancelled` siguen rechazados.
> 2. **F4-01 — ubicación principal.** Mover la vacía la pasa al destino (como dice el ítem); liberar o cargar la pasa a la ubicación más reciente que aún tiene mercancía y, si no queda ninguna, la conserva como referencia. El estado del depósito se valida al ubicar y al mover, no al liberar. Las cantidades son `numeric(18,4)` (§F.2).
> 3. **F4-02 — alcance del cuadre.** Retirar un producto de Comercio Exterior no necesita cuadre: sus ubicaciones se borran con la línea (`ON DELETE CASCADE`). La liberación al cargar se hace por ítem, equivalente a Σq por producto.
> 4. **F4-03 — mensajes no escritos.** «Orden de» (más de 100) y registro fotográfico (más de 200) tienen su mensaje; el producto inexistente responde 404 «El producto del depósito no existe.». El aviso al editar sale cuando cambia alguna de las tres cantidades y ese valor nuevo es mayor que 0. La validación de depósito anulado aplica al registrar.
> 5. **F4-04 — precinto.** La v2 no guarda precinto por camión: el campo sale en blanco. El PDF se arma con una clase pura (`NoveltyReportData`) para poder probarlo sin base.
> 6. **F4-05 — reglas no escritas.** Nombre de proveedor inválido: «El nombre del proveedor es obligatorio y no puede exceder 200 caracteres.». La unicidad normalizada se valida en la aplicación (el índice de §F.2 no es único). Archivo ausente o de más de 5 MB: 400. Lista inexistente al consultar o borrar: 404.
> 7. **F4-06 — extracción.** Además de `AddToEntryAsync` se extrajo `ResolveCargoUnitForEntry` (la regla de unidades de `AddDepositProduct`, con sus mensajes). Cantidad de artículos fuera de 1 a 200: «Seleccione entre 1 y 200 artículos de la lista de empaque.».
> 8. **F4-08 — tiquete sin número.** Un ciclo de ingreso todavía sin tiquete se identifica por su Id en los mensajes. El tiquete anulado se rechaza antes que el incompleto. Los errores de estado y servicio de la orden usan los textos de C-F4-18.
> 9. **F4-09 — acción.** Solo se acepta por nombre (`Print`/`Download`, sin distinguir mayúsculas); un número responde el 400 del contrato.
> 10. **F4-10 — detalle.** El nombre de la cuadrilla del depósito se lee con una consulta aparte en los tres detalles; la cuadrilla inexistente al editar o borrar responde 404 «La cuadrilla no existe.».
>
> **Defecto previo corregido dentro de la fase** (§G.19): el reintento de la guía de exportación automática recargaba la orden sin su ciudad de destino y el vencimiento caía a 30 días.

- **Objetivo:** reponer las funciones de bodega y báscula que el legacy usaba y la v2 no tiene:
  - ubicaciones por cantidad, con su liberación al cargar;
  - novedades estructuradas con su impresión;
  - listas de empaque;
  - pesaje de salida compartido y salida con el tiquete de ingreso;
  - registro de impresiones de etiquetas;
  - catálogo de cuadrillas.
- **Criterio de salida (verificable):**
  1. Se ubican 6 de 10 unidades en A-01, se mueven 2 a B-02 y el pendiente por ubicar es 4.
  2. Un cargue de 5 libera las posiciones de la más reciente a la más antigua.
  3. Una novedad con 2 dañadas notifica a Comercio Exterior y se imprime en PDF.
  4. Una lista de empaque de 3 artículos se importa en simulación y en firme, y sus artículos se asocian a un camión en Borrador con cantidad = bultos × unidades.
  5. Un segundo cliente sale en el mismo pesaje de salida sin cobro.
  6. Una orden sale con el tiquete de ingreso sin pesar de nuevo.
  7. Cada impresión o descarga de etiqueta queda contada.
  8. La guía imprime la cuadrilla de la orden.
  9. `dotnet build` y `dotnet test` pasan.
- **Rama:** `develop` (§E). Empieza cuando la fase 3 tiene todos sus ítems con commit. Usa `LoadedQuantity` (F3-01), la anulación de pesajes (F3-09) y el servicio de anulación de depósitos (F3-08).
- **Dificultad:** **Alta**. Son funciones nuevas y acotadas, pero tocan el cargue, la recepción y el despacho de báscula.
- **Perfil de agente:** agente capaz con revisión humana del diff.
- **Orden interno:** F4-01 → F4-02 → F4-03 → F4-04 → F4-05 → F4-06 → F4-07 → F4-08 → F4-09 → F4-10.

---

#### F4-01 · Ubicaciones por cantidad: ubicar, mover y liberar (GAP-014, RN-045, RN-046, LEGACY-FUNC-089 a 092 y 168 a 172, §B.4.3)

- **Dificultad:** Media.
- **Regla:**
  1. **Entidad `WarehouseStorageProductPlacement`** (tabla `warehouse_storage_product_placements`, `IAuditable`): cuánto de un producto de depósito hay en una ubicación.
     - Campos: `Id`, `WarehouseStorageProductId`, `WarehouseLocationId`, `Quantity` (> 0), `LastPlacedAt`, `CreatedAt`, `UpdatedAt`.
     - Una fila por par producto–ubicación (índice único). Cuando la cantidad llega a 0 la fila se borra; el borrado queda auditado.
  2. **Pendiente por ubicar** = `CurrentStock − Σ Quantity` de sus ubicaciones. Nunca se deja negativo (ver F4-02).
  3. **Ubicar** (`POST warehouse/storage-products/{id}/placements`, con `warehouseLocationId` y `quantity`):

     | Condición | Respuesta |
     |---|---|
     | `quantity ≤ 0` | 400 "La cantidad a ubicar debe ser mayor que cero." (el legacy volvía positivas las negativas; §B.4.3 las rechaza) |
     | `quantity > pendiente` | 409 "No se puede ubicar {q}: solo quedan {p} por ubicar." (legacy: "Solo resta la cantidad de … Por Ubicar") |
     | Producto inexistente | 404 "El producto del depósito no existe." |
     | Ubicación inexistente | 404 "La ubicación no existe." |
     | Ubicación deshabilitada (`IsAvailable = false`) | 409 "La ubicación {código} está deshabilitada." |
     | Depósito `Cancelled` o `Closed` | 409 "El depósito {n} está {estado}; no se puede ubicar mercancía." |

     - Si ya hay fila para ese par, suma la cantidad; si no, la crea. En ambos casos `LastPlacedAt = ahora`.
     - Si el producto no tiene ubicación principal (`WarehouseStorageProduct.WarehouseLocationId` nulo), toma esta. El campo se conserva por compatibilidad con listados y reportes.
     - No se valida capacidad, igual que hoy y que el legacy (RN-047).
  4. **Mover** (`POST warehouse/storage-products/{id}/placements/move`, con `fromLocationId`, `toLocationId` y `quantity`):

     | Condición | Respuesta |
     |---|---|
     | Origen igual al destino | 400 "La ubicación de destino debe ser distinta de la de origen." |
     | El producto no está en el origen | 404 "El producto no está ubicado en {código}." |
     | `quantity ≤ 0` | 400 "La cantidad a mover debe ser mayor que cero." |
     | `quantity >` lo ubicado en el origen | 409 "En {código} solo hay {x} unidades ubicadas." |

     - Además aplican las condiciones de ubicar sobre el destino (existe y está habilitado).
     - Resta en el origen (borra la fila si queda en 0) y suma en el destino (`LastPlacedAt = ahora`). Si el origen era la ubicación principal y se borró, la principal pasa al destino.
  5. **Liberar** (`POST warehouse/storage-products/{id}/placements/release`, con `warehouseLocationId` y `quantity`): mismas validaciones del origen que mover, con "La cantidad a liberar debe ser mayor que cero.". La cantidad liberada vuelve a «por ubicar».
  6. **Consultas:**
     - `GET warehouse/storage-products/{id}/placements`: producto, stock, ubicado, pendiente y ubicaciones.
     - `GET warehouse/locations/{id}/placements`: lo que hay en una ubicación, que es la ocupación del legacy.
  7. **Recepción:** cuando la recepción asigna ubicación a un producto (hoy `AssignWarehouseLocation`), además ubica la cantidad descargada, hasta el pendiente, con el mismo servicio. Con pendiente 0 no ubica nada. La validación de ubicación deshabilitada aplica también aquí (RN-046: hoy la recepción no la comprueba).
  8. Todas las escrituras van en transacción, con `Describe("Ubicación: {acción} {q} de «{producto}» del depósito {n} en {código}")`.
- **Evidencia:**
  - Legacy:
    - `modulos/mod_bodegas/registrarbodegacantidad.php:52-83`: tope «por ubicar»; negativa → positiva.
    - `modulos/mod_bodegas/guardarcantidadseccion.php:104`: ubica.
    - `modulos/mod_bodegas/liberarcantidadseccion.php:105`: libera.
    - `bodegas_schema.sql:1199-1212` (`productodetalle_x_seccion`) y `:1399-1411` (`seccion`).
  - v2:
    - `Wms.Domain/Entities/Warehouse/WarehouseStorageProduct.cs:18,156-158`: una sola ubicación por producto, sin cantidad.
    - `Wms.Application/Warehouse/Commands/Reception/CreateReceptionCommandHandler.cs:240-243`, `CompleteReceptionCommandHandler.cs:153` y `CreateReceptionWithoutWeighbridgeCommandHandler.cs:265`.
- **Archivos:**
  - `Wms.Domain/Entities/Warehouse/WarehouseStorageProductPlacement.cs` (nuevo): `Create`, `Add(q)`, `Remove(q)` (valida que no quede negativa: "La cantidad a retirar supera lo ubicado.").
  - `WarehouseStorageProduct.cs` (modifica: colección `Placements`, `ClearMainLocationIf(Guid locationId, Guid? replacement)`).
  - `Wms.Infrastructure/Persistence/Configurations/Warehouse/WarehouseStorageProductPlacementConfiguration.cs` (nuevo) y `AppDbContext.cs` (`DbSet<WarehouseStorageProductPlacement>`).
  - `Wms.Application/Warehouse/Common/Services/PlacementPlanner.cs` (nuevo, puro): `PendingToPlace(currentStock, placed)` y `PlanLifoRelease(placements, quantity)`.
  - `Wms.Application/Warehouse/Common/Services/WarehousePlacementService.cs` (nuevo, scoped): `PlaceAsync`, `MoveAsync`, `ReleaseAsync`, `ReleaseLifoAsync` y `TrimToStockAsync`. Se registra en `DependencyInjection.cs`.
  - `Wms.Application/Warehouse/Commands/Placement/{PlaceStock,MovePlacement,ReleasePlacement}/*` (nuevos: comando, validador y handler).
  - `Wms.Application/Warehouse/Queries/{GetProductPlacements,GetLocationPlacements}/*` (nuevos).
  - Los tres handlers de recepción citados (modifica).
  - `Wms.Api/Controllers/v1/WarehousePlacementsController.cs` (nuevo; `[Route("warehouse")]`, `WarehouseAccess`) y `Controllers/v1/Requests/WarehousePlacementRequests.cs` (nuevo).
- **Contrato:** C-F4-01 a C-F4-05, y C-F4-06 (recepción: efecto nuevo, sin cambio de forma).
- **Esquema:** tabla nueva `warehouse_storage_product_placements` (§F).
  - Datos iniciales opcionales, para agregar a la migración: una fila por producto con `warehouse_location_id` no nulo y `current_stock > 0`, con `quantity = current_stock`.
- **Efectos secundarios:** auditoría; ninguna notificación.
- **Pruebas** (`Wms.Tests/Warehouse/PlacementPlannerTests.cs` y `Wms.Tests/Domain/Warehouse/WarehouseStorageProductPlacementTests.cs`, nuevos):

  | Caso | Datos | Resultado |
  |---|---|---|
  | Pendiente | stock 10, ubicado 6 | 4 |
  | Ubicar más que el pendiente | pendiente 4, q 5 | error |
  | Ubicar exacto | pendiente 4, q 4 | pendiente 0 |
  | `Remove` que deja 0 | 2 − 2 | 0 (el servicio borra la fila) |
  | `Remove` mayor | 2 − 3 | error |
  | Pendiente con stock menor que lo ubicado | stock 3, ubicado 5 | 0 (y `TrimToStock` libera 2) |

- **Terminado cuando:** se puede ubicar, mover y liberar con los topes, y la recepción deja ubicado lo descargado.
- **Riesgo:** productos existentes sin filas de ubicación. Se mitiga con los datos iniciales opcionales; sin ellos, aparecen como pendientes por ubicar.

---

#### F4-02 · Liberar la ubicación al cargar y mantenerla cuadrada con el stock (GAP-014, RN-048, §B.4.3)

- **Dificultad:** Media.
- **Regla:**
  1. **Al ejecutar el cargue**, por cada producto con cantidad cargada Σq > 0 (F3-01): `ReleaseLifoAsync(producto, Σq)`.
     - Libera primero la ubicación con `LastPlacedAt` más reciente; si no alcanza, sigue con la siguiente.
     - Si lo ubicado es menor que Σq, libera todo lo ubicado: el resto salió de lo «por ubicar».
     - Es el equivalente del legacy, que liberaba por unidad la posición más reciente (`MAX(id)`) al crear la guía. §B.4.3 lo mueve al cargue, que es cuando la mercancía sale físicamente.
  2. **Cuadre con el stock:** toda operación que baja `CurrentStock` fuera del cargue llama al final a `TrimToStockAsync(productos)`, que libera en el mismo orden el exceso de lo ubicado sobre el stock:
     - anulación de depósito (`WarehouseStorageCancellationService`, F3-08);
     - anulación de pesaje (F3-09);
     - ajuste de inventario (`Wms.Application/Warehouse/Commands/AdjustInventory`);
     - edición y retiro de productos por Comercio Exterior (`UpdateDepositProduct` y `RemoveDepositProduct`).
  3. **Reversión** (F3-07): no crea ubicaciones. La mercancía devuelta queda «por ubicar» y la notificación a Bodega ya lo pide.
  4. La respuesta del cargue agrega por ítem `releasedPlacements: [{ warehouseLocationId, locationCode, quantity }]`, para que el operario sepa de dónde retirar.
- **Evidencia:**
  - Legacy: `modulos/mod_salidas/verguia.php:659-676` (libera la posición más reciente por unidad al crear la guía); `modulos/mod_salidas/eliminarsalida.php:89-106` (la anulación reactiva posiciones: no se replica, ver punto 3).
  - v2: `ExecuteLoadingOrderCommandHandler.cs:184-185` (baja el stock sin tocar ubicaciones).
- **Archivos** (modifica):
  - `ExecuteLoadingOrderCommandHandler.cs`
  - `LoadingItemResultDto.cs` (`ReleasedPlacements`)
  - `WarehouseStorageCancellationService.cs`
  - el handler de `VoidWeighing`
  - los handlers de `AdjustInventory`, `UpdateDepositProduct` y `RemoveDepositProduct`
- **Contrato:** C-F4-07.
- **Esquema:** ninguno.
- **Efectos secundarios:** filas de ubicación reducidas o borradas, con auditoría.
- **Pruebas** (`PlacementPlannerTests`):

  | Ubicaciones (`LastPlacedAt`) | Liberar | Resultado |
  |---|---|---|
  | A = 5 (lunes), B = 3 (martes) | 4 | B −3, A −1 |
  | A = 5, B = 3 | 8 | A −5, B −3 |
  | A = 5, B = 3 | 10 | A −5, B −3 (2 sin ubicar) |
  | ninguna | 3 | nada |
  | A = 5 | 0 | nada |

- **Terminado cuando:** tras un cargue, lo ubicado nunca supera el stock y la respuesta dice qué se liberó.
- **Riesgo:** el operario retira de otra posición distinta a la calculada. Se mitiga con mover y liberar manuales (F4-01).

---

#### F4-03 · Novedades de mercancía (GAP-015, RN-068, LEGACY-FUNC-173 y 174, §B.4.8)

- **Dificultad:** Media.
- **Regla:**
  1. **Entidad `WarehouseNovelty`** (tabla `warehouse_novelties`, `IAuditable`), sobre un producto de depósito y, opcionalmente, un camión:

     | Propiedad | Regla | Campo legacy |
     |---|---|---|
     | `WarehouseStorageProductId` | obligatorio | `id_productoenbodega` |
     | `WarehouseStorageEntryId` (null) | el camión, si aplica; debe ser del mismo depósito | — |
     | `Type` | `Entry`, `Exit`, `Transshipment`, `Routine` o `Inspection` (texto) | `tipo_observacion` (ingreso, salida, trasbordo, rutina, inspeccion) |
     | `StartedAt`, `EndedAt` | obligatorias; fin ≥ inicio | `fechahoraini_observacion`, `fechahorafin_observacion` |
     | `OrderedBy` (null) | hasta 100 caracteres | `orden_de` |
     | `Description` | obligatoria, hasta 4000 caracteres | `desc_observacion` |
     | `TotalQuantity` | ≥ 0; el frontend la precarga con el stock | `total` |
     | `GoodQuantity`, `DamagedQuantity`, `MissingQuantity`, `SurplusQuantity` | ≥ 0, por defecto 0; sin regla de suma (§B.4.8) | `buena`, `danada`, `faltante`, `sobrante` |
     | `IsUnloaded` | booleano; cantidad descargada = `TotalQuantity` si es verdadero, si no 0 | `descargada` |
     | `TarpCondition` (null) | `Good`, `Holed`, `Torn`, `NoTarp` | `carpa` (buena, agujereada, rota, sin carpa) |
     | `TrailerCondition` (null) | `Clean`, `Dirty`, `Rusty`, `Wet`, `Broken` | `remolque` (limpio, sucio, oxidado, mojado, roto) |
     | `PhotoRecord` (null) | hasta 200 caracteres; texto, sin archivos (§B.4.8) | `reg_fotografico` |
     | `CreatedById`, `VoidedAt`, `VoidedById`, `VoidReason` | anulación lógica | `estado` |

  2. **Registrar** (`POST warehouse/novelties`). Mensajes:
     - "Seleccione el tipo de novedad."
     - "La descripción de la novedad es obligatoria."
     - "La descripción no puede exceder 4000 caracteres."
     - "La fecha de fin no puede ser anterior a la de inicio."
     - "Las cantidades no pueden ser negativas."
     - "El camión no pertenece al depósito del producto."
     - Depósito `Cancelled` → 409 "El depósito {n} está anulado."
  3. **Editar** (`PUT warehouse/novelties/{id}`): todos los campos salvo el producto. Si está anulada → 409 "La novedad está anulada." El legacy editaba descripción, cantidades y descargada; aquí se permite todo el formulario.
  4. **Anular** (`POST warehouse/novelties/{id}/void`, con `reason`):
     - Motivo: "El motivo de la anulación debe tener entre 10 y 500 caracteres."
     - Ya anulada → 409 "La novedad ya está anulada."
  5. **Consultar:**
     - `GET warehouse/novelties`, con filtros `warehouseStorageId`, `warehouseStorageProductId`, `type`, `from` y `to` (fecha de inicio, día de Colombia), `includeVoided` (por defecto false), paginado (máximo 50) y `all`.
     - `GET warehouse/novelties/{id}`.
  6. **Notificación**, después del commit, a `ForeignTrade`, nivel Warning:
     - Cuándo: al registrar con dañada, faltante o sobrante > 0, o al editar si alguna de esas tres cambia y queda > 0.
     - Título: "Novedad en mercancía".
     - Mensaje: "Bodega registró una novedad ({tipo}) en «{producto}» del depósito {n}: dañada {d}, faltante {f}, sobrante {s}."
  7. Es distinta de la diferencia contra lo declarado de la recepción (`ReceptionDeclaredDifference`), que no cambia.
  8. Fuera de alcance: la «novedad» por unidad con serial (`registrarnovedad.php`, `tipo_observacion = 'novedad'`). Se llama desde `asignarobservacionescolmotores.php` y la lectura de VIN, así que es de Colmotores.
- **Evidencia:**
  - Legacy:
    - `bodegas_schema.sql:771-797` (`observacionesproducto`).
    - `modulos/mod_bodegas/registrarobservaciones.php:104-125` (alta) y `:293-352` (opciones del formulario).
    - `modificarobservacion.php:40` (edición).
    - `eliminarobservacion.php:44` (baja lógica).
  - v2: `Wms.Application/Warehouse/Commands/Reception/ReceptionDeclaredDifference.cs` y `Wms.Domain/Entities/Warehouse/ReceptionLog.cs:11` (`Comments`), sin desglose.
- **Archivos:**
  - `Wms.Domain/Entities/Warehouse/WarehouseNovelty.cs` (nuevo: `Create`, `Update`, `Void`).
  - `Wms.Domain/Enums/{NoveltyType,TarpCondition,TrailerCondition}.cs` (nuevos).
  - `Wms.Infrastructure/Persistence/Configurations/Warehouse/WarehouseNoveltyConfiguration.cs` (nuevo) y `AppDbContext.cs`.
  - `Wms.Application/Warehouse/Novelties/Commands/{CreateNovelty,UpdateNovelty,VoidNovelty}/*` (nuevos).
  - `Wms.Application/Warehouse/Novelties/Queries/{GetNovelties,GetNoveltyById}/*` (nuevos).
  - `Wms.Application/Warehouse/Novelties/Common/WarehouseNoveltyDto.cs` (nuevo).
  - `Wms.Api/Controllers/v1/WarehouseNoveltiesController.cs` (nuevo; `[Route("warehouse")]`, `[Authorize]` en la clase y `WarehouseAccess` en las escrituras) y `Controllers/v1/Requests/WarehouseNoveltyRequests.cs` (nuevo).
- **Contrato:** C-F4-08 a C-F4-11.
- **Esquema:** tabla nueva `warehouse_novelties` (§F).
- **Efectos secundarios:** notificación a Comercio Exterior; auditoría.
- **Pruebas** (`Wms.Tests/Domain/Warehouse/WarehouseNoveltyTests.cs`, nuevo):
  - Fin anterior al inicio → error.
  - Dañada −1 → error.
  - Descripción vacía → error.
  - `IsUnloaded` con total 10 → cantidad descargada 10; sin marcar → 0.
  - `Void` dos veces → error.
  - `Update` sobre una anulada → error.
- **Terminado cuando:** Bodega registra, edita, anula y lista novedades, y Comercio Exterior recibe el aviso.
- **Riesgo:** bajo.

---

#### F4-04 · Impresión «Reporte de mercancías» (GAP-015, LEGACY-FUNC-177)

- **Dificultad:** Baja.
- **Regla:** `GET warehouse/novelties/{id}/pdf` devuelve un PDF (QuestPDF, carta vertical), con archivo `novedad_{depósito}_{yyyyMMdd}.pdf`. Lo generan también las novedades anuladas, con la marca de agua "ANULADA".
  - **Encabezado:** "REPORTE DE MERCANCÍAS"; día, mes y año de `StartedAt` en Colombia; horas de inicio y fin.
  - **Datos:**
    - "Orden de"; factura o CPI, que es el número del depósito;
    - si hay camión: conductor, manifiesto, placa, empresa de transporte, unidad de carga y precinto;
    - importador, agencia de aduanas y modalidad;
    - depósito y mercancía (producto y embalaje);
    - carpa y remolque; descargar sí/no;
    - total, buena, dañada, faltante y sobrante;
    - observación (descripción) y registro fotográfico.
    - Un dato sin valor se deja en blanco.
  - **Firmas:** conductor, bodega cubierta, jefe de bodega y control interno, con línea «C.C.».
  - **Pie:** "Bodegas Asociadas no se hace responsable de daños, hurtos o cualquier otro incidente causados a la mercancía después de ser entregada."
- **Evidencia:** legacy `modulos/mod_bodegas/imprimirobservacion.php:80-190`.
- **Archivos:** `Wms.Application/Warehouse/Novelties/Services/WarehouseNoveltyPdfService.cs` (nuevo, registrado en `DependencyInjection.cs`); `Wms.Application/Warehouse/Novelties/Queries/GetNoveltyPdf/*` (nuevo); `WarehouseNoveltiesController.cs` (modifica).
- **Contrato:** C-F4-12.
- **Esquema:** ninguno.
- **Efectos secundarios:** ninguno.
- **Pruebas:** `Wms.Tests/Warehouse/WarehouseNoveltyPdfServiceTests.cs` (nuevo): genera bytes no vacíos con y sin camión; con una novedad anulada no lanza error.
- **Terminado cuando:** el PDF descarga con los datos de la novedad.
- **Riesgo:** bajo.

---

#### F4-05 · Listas de empaque: proveedores e importación (GAP-013, RN-016, LEGACY-FUNC-129 a 131, P11)

- **Dificultad:** Media.
- **Regla:**
  1. **Entidades** (todas `IAuditable`):

     | Entidad | Tabla | Campos |
     |---|---|---|
     | `PackingListSupplier` | `packing_list_suppliers` | `Name` (1 a 200, único normalizado con `CatalogNameNormalizer`), `IsActive` |
     | `PackingListFile` | `packing_list_files` | `SupplierId`, `ImporterId` (tercero), `FileName` (hasta 250), `ItemCount`, `CreatedById`, `CreatedAt` |
     | `PackingListItem` | `packing_list_items` | `PackingListFileId`, `Code` (1 a 40), `Description` (1 a 250), `Packages` (> 0), `UnitsPerPackage` (> 0), `NetWeightKg` (≥ 0), `ProductId`, `Status` (`Active` o `Associated`), `WarehouseStorageEntryId` (null), `AssociatedAt`, `AssociatedById` |

     - `Quantity = Packages × UnitsPerPackage` (RN-016) es calculada; no se guarda.
     - El legacy tenía el estado intermedio «seleccionado», que era solo de pantalla (`modificarentrada.php:55-56` lo devuelve a «activo»). Aquí la selección viaja en la petición de F4-06.
  2. **Proveedores:**
     - `GET foreign-trade/packing-list-suppliers` (lista completa).
     - `POST foreign-trade/packing-list-suppliers` con `name`. Duplicado → 409 "Ya existe el proveedor {nombre}."
  3. **Importar** (`POST foreign-trade/packing-lists/import`, multipart: `file`, `supplierId`, `importerId`, `headerRows` ≥ 0 con valor por defecto 1, `dryRun` con valor por defecto true):
     - **Columnas**, en orden: `codigo;NOMBRE;CANT_BULTOS;UNID_X_BULTOS;PSO_TOTAL_NETO`. Separador `;`; si la primera fila de datos no lo tiene, `,`. Con `;` se acepta la coma decimal. UTF-8.
     - **Errores de fila**, sin detener las demás:
       - "Fila {n}: el código es obligatorio y no puede exceder 40 caracteres." (el SKU del catálogo admite 40)
       - "Fila {n}: el nombre es obligatorio y no puede exceder 250 caracteres."
       - "Fila {n}: los bultos deben ser un número mayor que cero."
       - "Fila {n}: las unidades por bulto deben ser un número mayor que cero."
       - "Fila {n}: el peso neto debe ser un número mayor o igual a cero."
     - **Validaciones del archivo:**
       - Proveedor inexistente o inactivo → 404 "El proveedor no existe o está inactivo."
       - Importador inexistente → 404 "El importador no existe."
       - Sin filas válidas → 400 "El archivo no tiene filas válidas."
     - **Producto de cada fila.** Corrige el defecto del legacy, que buscaba con la columna 0 como importador y la 1 como código:
       1. Si ya existe un artículo de una lista **del mismo importador** con el mismo código (sin distinguir mayúsculas), se usa su producto.
       2. Si no, se crea el producto con `Product.CreateFromPackingList(name, sku, unitMeasureId)` (nuevo):
          - nombre: los primeros 150 caracteres del nombre;
          - SKU: el código en mayúsculas; si ya existe, `{código truncado a 35}-{4 hex}`, con 3 intentos; si fallan → 409 "No se pudo generar un SKU único para el código {código}.";
          - unidad: `UnitMeasureIds.Unidad`;
          - sin embalaje (el legacy fijaba `id_embalaje = 1`; no se copia).
     - **Con `dryRun = true`** no guarda: devuelve filas válidas, errores y cuántos productos se crearían.
     - **Con `false`**, en una transacción: archivo, artículos (`Active`) y productos nuevos. Se notifica a `ForeignTrade` "Productos creados desde lista de empaque" si hubo altas.
  4. **Consultar:**
     - `GET foreign-trade/packing-lists`: archivos, con filtros `importerId` y `supplierId`, paginado.
     - `GET foreign-trade/packing-lists/{id}`: archivo y artículos.
     - `GET foreign-trade/packing-list-items`: artículos con filtros `importerId` (obligatorio), `status` (por defecto `Active`) y `search` (código o nombre), paginado y `all`.
  5. **Eliminar archivo** (`DELETE foreign-trade/packing-lists/{id}`):
     - Solo si ningún artículo está `Associated`. Si no → 409 "La lista {archivo} tiene artículos asociados a depósitos; no se puede eliminar."
     - Borra archivo y artículos; los productos creados se conservan. Queda auditado.
- **Evidencia:**
  - Legacy:
    - `modulos/mod_listasempaque/cargarlistasempaque.php:80-125`: lectura, búsqueda defectuosa y alta de producto.
    - `bodegas_schema.sql:644-679` (`listaempaquearchivo`, `listasdeempaque`) y `:1221-1225` (`proveedor_listas`).
    - `eliminarlistaempaque.php:52`.
  - v2: sin entidad.
- **Archivos:**
  - `Wms.Domain/Entities/ForeignTrade/{PackingListSupplier,PackingListFile,PackingListItem}.cs` (nuevos).
  - `Wms.Domain/Enums/PackingListItemStatus.cs` (nuevo).
  - `Wms.Domain/Entities/Product/Product.cs` (modifica: `CreateFromPackingList`).
  - Configuraciones en `Wms.Infrastructure/Persistence/Configurations/ForeignTrade/` (nuevas) y `AppDbContext.cs`.
  - `Wms.Application/ForeignTrade/PackingLists/Commands/{CreateSupplier,ImportPackingList,DeletePackingList}/*` (nuevos).
  - `Wms.Application/ForeignTrade/PackingLists/Queries/{GetSuppliers,GetPackingLists,GetPackingListById,GetPackingListItems}/*` (nuevos).
  - `Wms.Application/ForeignTrade/PackingLists/Common/PackingListCsvParser.cs` (nuevo, puro).
  - `Wms.Api/Controllers/v1/PackingListsController.cs` (nuevo; `[Route("foreign-trade")]`, `ForeignTradeAccess`) y `Controllers/v1/Requests/PackingListRequests.cs` (nuevo).
- **Contrato:** C-F4-13 a C-F4-16.
- **Esquema:** tablas nuevas `packing_list_suppliers`, `packing_list_files` y `packing_list_items` (§F).
- **Efectos secundarios:** productos nuevos en el catálogo; notificación; auditoría.
- **Pruebas** (`Wms.Tests/ForeignTrade/PackingListCsvParserTests.cs`, nuevo):
  - `"A-1;TORNILLO 3/8;10;12;25,5"` → código A-1, 10 bultos, 12 unidades, 25.5 kg, cantidad 120.
  - Separador `,` con punto decimal.
  - `headerRows = 2` salta dos filas.
  - Bultos 0 → error de fila.
  - Código de 41 caracteres → error de fila.
  - Línea vacía → se ignora.
- **Terminado cuando:** una lista se importa en simulación y en firme, y sus artículos quedan activos con su producto.
- **Riesgo:** productos duplicados en el catálogo por nombres casi iguales. Es el comportamiento del legacy (un producto por código e importador); F1-07 permite corregir la línea del depósito.

---

#### F4-06 · Asociar artículos de la lista a un camión del depósito (GAP-013, RN-016, LEGACY-FUNC-132, P11)

- **Dificultad:** Media.
- **Regla:** `POST foreign-trade/deposits/{id}/entries/{entryId}/packing-list-items` recibe `itemIds` (1 a 200), `warehouseStorageCargoUnitId?` y `reason`.
  1. **Validaciones:**
     - El depósito se carga con `DepositProductEditing.LoadEditableStorageAsync`: solo en Borrador (mensaje actual "Solo se pueden editar los productos de un depósito en Borrador.").
     - El camión es del depósito (mensaje actual).
     - Motivo: "El motivo de la corrección debe tener entre 10 y 500 caracteres." (el de `AddDepositProduct`).
     - Cada artículo:
       - existe → si no, 404 "El artículo {id} de la lista de empaque no existe.";
       - está `Active` → si no, 409 "El artículo {código} ya está asociado al depósito {n}.";
       - todos son de listas del mismo importador → si no, 400 "Los artículos deben ser de un mismo importador.".
     - Si el depósito tiene importador y no es el de la lista → 409 "Los artículos son de la lista del importador {x}; el depósito es del importador {y}."
     - Unidades de carga: la regla de `AddDepositProduct`. Si el depósito las usa, `warehouseStorageCargoUnitId` es obligatorio y debe ser de ese camión, con los mensajes actuales.
  2. **Efecto** (en una transacción), por cada artículo:
     - Se agrega el producto al camión con cantidad declarada `Packages × UnitsPerPackage`, la unidad de medida del producto y sin embalaje.
     - Se usa la misma lógica de `AddDepositProduct`, extraída a `DepositProductEditing.AddToEntryAsync(storage, entry, productId, description, unitMeasureId, packagingTypeId, quantity, cargoUnit)`, que también usa `AddDepositProductCommandHandler`. Si el producto ya está en el camión, suma.
     - El artículo pasa a `Associated`, con el camión, la fecha y el usuario.
  3. **Importador:** si el depósito no tiene importador, se le asigna el de la lista con la misma lógica de `UpdateDepositStakeholders` (rol IMPORTER). Es lo que hacía el legacy al asociar desde la lista.
  4. `Describe("Artículos de lista de empaque asociados al camión {placa} del depósito {n}: {k} artículos. Motivo: {motivo}")`; después del commit, `editing.AfterCommitAsync`, como `AddDepositProduct`.
  5. La respuesta devuelve los productos del depósito afectados, con su nueva cantidad.
- **Evidencia:**
  - Legacy `modulos/mod_bascula/modificarentrada.php`:
    - `:1104` (botón «Agregar Lista»);
    - `:279-283` (asocia al pesaje);
    - `:287-289` (importador del ingreso desde la lista).
  - Legacy `modulos/mod_listasempaque/listararticulosactivos.php:233` (unidades × bultos).
  - v2: `Wms.Application/ForeignTrade/Commands/AddDepositProduct/AddDepositProductCommandHandler.cs:20-99`.
- **Archivos:**
  - `DepositProductEditing.cs` (modifica: `AddToEntryAsync`).
  - `AddDepositProductCommandHandler.cs` (modifica: usa `AddToEntryAsync`, sin cambiar su comportamiento).
  - `Wms.Application/ForeignTrade/PackingLists/Commands/AssociatePackingListItems/*` (nuevo).
  - `PackingListItem.cs` (modifica: `Associate(entryId, userId)`).
  - `PackingListsController.cs` (modifica).
- **Contrato:** C-F4-17.
- **Esquema:** ninguno adicional.
- **Efectos secundarios:** productos y cantidades del depósito; importador; auditoría; los recálculos de `AfterCommitAsync`.
- **Pruebas:** `Wms.Tests/Domain/ForeignTrade/PackingListItemTests.cs` (nuevo):
  - `Quantity` de 10 × 12 = 120.
  - `Associate` sobre un artículo asociado → error.
  - `Associate` guarda camión, fecha y usuario.
- **Terminado cuando:** los artículos elegidos aparecen como productos del camión con cantidad bultos × unidades y quedan asociados.
- **Riesgo:** refactor de `AddDepositProduct`. Se mitiga manteniendo sus mensajes y su orden de validaciones; la revisión humana compara el diff.

---

#### F4-07 · Pesaje de salida compartido: otras órdenes del mismo camión sin cobro (GAP-019, BAS-08, LEGACY-FUNC-119, P10)

- **Dificultad:** Alta.
- **Regla:** `POST weighbridge/output/cycles/{cycleId}/additional-orders` recibe `loadingOrderIds` (1 a 10, como el tope del legacy).
  1. **Pesaje ancla:** el ciclo de salida que ya tiene el camión.

     | Condición | Respuesta |
     |---|---|
     | No existe | 404 "El pesaje no existe." |
     | Su servicio no es de salida | 400 "Solo se agregan órdenes a un pesaje de salida." |
     | Anulado o cancelado | 409 "El pesaje está anulado." |

  2. **Cada orden:**

     | Condición | Respuesta |
     |---|---|
     | No existe | 404 "La orden de cargue {id} no existe." |
     | Estado distinto de `Pending`, `InProgress` o `Loaded` | 409 "La orden {n} está {estado}; no se puede agregar al pesaje." |
     | Otro vehículo | 409 "La orden {n} es para el vehículo {placa orden}; el pesaje es del vehículo {placa pesaje}." |
     | Ya tiene un servicio de salida no descartado | 409 "La orden {n} ya tiene un servicio de salida en báscula." |
     | Algún depósito de la orden no está confirmado | 400 "Los depósitos de la orden {n} deben estar confirmados." |

  3. **Efecto** (en una transacción), por orden:
     - `ServiceRecord.CreateAnchoredOutput(modalityId, loadingOrderId, customerId, anchorCycleId)` (nuevo):
       - servicio de salida con `AnchorWeighbridgeCycleId`;
       - estado `Completed`, porque no tiene pasos propios: su pesaje es el del ancla;
       - modalidad del depósito de la orden (el legacy fijaba la modalidad 4; no se copia);
       - cliente = el de la orden.
     - Tercero CUSTOMER y vínculo con la entrada de portería del ancla (pivote), como `InitiateOutputWeighing`. El registro de salida en portería sigue tomando el primer vínculo, por fecha, así que no cambia.
     - **Sin cobro:** no se crea factura ni línea en $0. El legacy creaba recibos en $0 solo para su consecutivo.
     - Si el ancla está `Complete` y la orden `Loaded` → `LoadingOrder.Dispatch()` enseguida.
  4. **Despacho posterior:**
     - Al completar el ancla (`CompleteCycleHandler.cs:222-233` y `RecordWeighingHandler.cs:500-516`) se despachan también las órdenes `Loaded` de los servicios anclados.
     - Al ejecutar el cargue después de completar el ancla, la regla ABO-1 (`ExecuteLoadingOrderCommandHandler.cs:305-319`) también considera completo el ciclo ancla del servicio de la orden.
  5. **Anulación del ancla** (F3-09 B, modifica): los servicios anclados también se descartan (`VoidService`) y sus órdenes `Dispatched` vuelven a `Loaded`.
  6. **Historial de báscula:** la fila del ancla agrega `additionalOrders: [{ serviceRecordId, loadingOrderId, loadingOrderNumber, customerName }]`.
- **Evidencia:**
  - Legacy `modulos/mod_bascula/duplicarrecibo.php`:
    - `:60-72`: N salidas «incompleto» con modalidad fija 4;
    - `:103-110`: copia los pesos del pesaje de salida;
    - `:122-138`: recibo y línea de factura en $0;
    - `:287`: tope de 10.
  - v2:
    - `Wms.Application/Weighbridge/Commands/Output/Initiate/InitiateOutputWeighingHandler.cs:46-51` (una salida por entrada de portería) y `:136-151` (creación del servicio).
    - `CompleteCycleHandler.cs:222-233` y `RecordWeighingHandler.cs:500-516` (despacho de la orden al completar).
- **Archivos:**
  - `ServiceRecord.cs` (modifica: `AnchorWeighbridgeCycleId`, `CreateAnchoredOutput`).
  - `Wms.Infrastructure/Persistence/Configurations/Services/ServiceRecordConfiguration.cs` (modifica).
  - `Wms.Application/Weighbridge/Commands/Output/AddAdditionalOrders/*` (nuevo).
  - `CompleteCycleHandler.cs`, `RecordWeighingHandler.cs`, `ExecuteLoadingOrderCommandHandler.cs` y el handler de `VoidWeighing` (modifica).
  - `GetWeighbridgeHistoryHandler.cs` y `WeighbridgeHistoryDto.cs` (modifica).
  - `Wms.Api/Controllers/v1/WeighbridgeOutputSharingController.cs` (nuevo; `[Route("weighbridge")]`, `ScaleAccess`) y `Controllers/v1/Requests/WeighbridgeOutputSharingRequests.cs` (nuevo).
- **Contrato:** C-F4-18.
- **Esquema:** `service_records.anchor_weighbridge_cycle_id uuid NULL`, FK a `weighbridge_cycles(id)` `ON DELETE RESTRICT`, e índice.
- **Efectos secundarios:** servicios nuevos, órdenes despachadas, historial.
- **Pruebas** (`Wms.Tests/Weighbridge/AdditionalOutputOrderRulesTests.cs`, nuevo; función pura `AdditionalOutputOrderRules.Check(anchor, order)`):
  - Otro vehículo → error.
  - Orden `Dispatched` → error.
  - Ancla `Canceled` → error.
  - Orden `Loaded` con ancla `Complete` → válida y «despachar ahora».
  - Orden `Pending` con ancla `InProgress` → válida y «despachar después».
  - 11 órdenes → error del validador "Se pueden agregar entre 1 y 10 órdenes."
- **Terminado cuando:** dos órdenes del mismo camión salen con un solo pesaje y un solo cobro.
- **Riesgo:** despachar una orden que no se cargó. Se mitiga: solo se despachan órdenes `Loaded`.

---

#### F4-08 · Salida con el tiquete de ingreso, sin pesar de nuevo (GAP-019, BAS-09, LEGACY-FUNC-120 y 166, P10, P16)

- **Dificultad:** Alta.
- **Regla:** dos rutas con el mismo comando (`ExitWithEntryTicketCommand`):
  - `POST weighbridge/output/from-entry-ticket` (`ScaleAccess`), con `entryWeighbridgeCycleId` y `loadingOrderId`;
  - `POST foreign-trade/loading-orders/{id}/exit-with-entry-ticket` (`ForeignTradeAccess`), con `entryWeighbridgeCycleId`; `{id}` es la orden.
  - En el legacy, las tres pantallas que sacan mercancía con un tiquete de ingreso piden el permiso `salidas:registrar`, no uno de báscula: `mod_bascula/usartiquete.php`, `mod_salidas/salidausartiquete.php` y `mod_salidas/salidaglobal.php`. Por eso Comercio Exterior también la usa (P16).
  1. **Tiquete de ingreso:**

     | Condición | Respuesta |
     |---|---|
     | No existe | 404 "El pesaje no existe." |
     | Su servicio no es de ingreso | 400 "El tiquete {t} no es de un ingreso." |
     | No está `Complete` | 409 "El tiquete {t} no está completo." |
     | Anulado (F3-09) | 409 "El tiquete {t} está anulado." |
     | Ya se usó en otra salida cuya orden no está cancelada ni revertida | 409 "El tiquete {t} ya se usó para la salida de la orden {o}." |

  2. **Orden:**
     - Mismas condiciones de estado, servicio activo y depósitos de F4-07.
     - Vehículo igual al del tiquete → si no, 409 "La orden {n} es para el vehículo {placa orden}; el tiquete {t} es del vehículo {placa tiquete}."
     - Cada ítem debe ser de un depósito con entrada no anulada en ese ciclo → si no, 409 "La orden {n} tiene mercancía del depósito {d}, que no llegó en el tiquete {t}."
     - Diferencia con el legacy: el legacy sacaba todo lo nacionalizado del pesaje. Aquí Comercio Exterior crea la orden con los topes de F2-02, y báscula o Comercio Exterior la vinculan al tiquete.
  3. **Efecto** (en una transacción):
     - `ServiceRecord.CreateOutputFromEntryTicket(modalityId, loadingOrderId, customerId, entryCycleId)` (nuevo): servicio de salida con `SourceEntryCycleId`, estado `Completed` y sin ciclo propio.
     - Tercero CUSTOMER y vínculo con la entrada de portería del tiquete.
     - Sin cobro.
     - Si la orden está `Loaded` → `Dispatch()` enseguida. Si no, la regla ABO-1 del cargue la despacha al ejecutar, porque considera completo el servicio con `SourceEntryCycleId`.
  4. **Anulación del tiquete** (F3-09 A, guarda nueva): si el tiquete se usó en una salida cuya orden no está cancelada ni revertida → 409 "El tiquete {t} se usó para la salida de la orden {o}; revierta o cancele primero esa orden."
  5. **Historial:** la fila del tiquete agrega `exitOrder: { serviceRecordId, loadingOrderId, loadingOrderNumber }` o null.
  6. **«Salida Global»** (LEGACY-FUNC-166, P16). En el legacy, Comercio Exterior elegía un depósito, marcaba varios tiquetes de ingreso y creaba una sola salida con una sola guía.
     - En la v2 se hace **camión por camión**: una orden de cargue por camión (su vehículo y su conductor) y este endpoint con el tiquete de ese camión.
     - La cantidad de cada orden la fija Comercio Exterior, con los topes de F2-02. La referencia es lo que trajo ese camión, visible por camión en el detalle del depósito; el legacy la proponía igual.
     - Cada camión lleva su guía y se cobra una guía por camión; el legacy emitía una sola.
     - No se construye la selección de varios tiquetes en lote.
- **Evidencia:**
  - Legacy `modulos/mod_bascula/usartiquete.php:8-9` (permiso `salidas:registrar`) y `:60-115`: crea la salida con el importador y la SIA del ingreso, vincula el mismo pesaje (`UPDATE pesaje SET id_salida`) y saca lo nacionalizado del pesaje con su saldo anterior.
  - Legacy `modulos/mod_salidas/salidausartiquete.php:39-40,116-124` («Usando Tiquete de Entrada» desde Salidas, `tipo = tiquete`).
  - Legacy «Salida Global»:
    - `modulos/mod_salidas/nuevasalida.php:113` (opción del menú);
    - `salidaglobal.php:39-40,151-170` (depósito y selección de tiquetes, `tipo = global`);
    - `listarpesajesglobal.php:54-68` (tiquetes de ingreso del depósito) y `:186`;
    - `registrarsalida.php:509-531` (una salida que reutiliza los pesajes de ingreso), `:676-745` (mercancía por camión) y `:1354-1379` (cantidad propuesta = lo que trajo el camión).
  - v2: sin equivalente. `Wms.Application/Weighbridge/Commands/Storage/GenerateGlobalGuide/GenerateGlobalDispatchGuideHandler.cs` **no lo es**: cierra con un solo peso el ciclo del flujo de perecederos y tiene un TODO (§G).
- **Archivos:**
  - `ServiceRecord.cs` y `ServiceRecordConfiguration.cs` (modifica: `SourceEntryCycleId`, `CreateOutputFromEntryTicket`).
  - `Wms.Application/Weighbridge/Commands/Output/ExitWithEntryTicket/*` (nuevo).
  - `ExecuteLoadingOrderCommandHandler.cs`, el handler de `VoidWeighing` y `GetWeighbridgeHistoryHandler.cs` (modifica).
  - `WeighbridgeOutputSharingController.cs` (modifica: ruta de báscula).
  - `Wms.Api/Controllers/v1/LoadingOrderExitController.cs` (nuevo; `[Route("foreign-trade")]`, `ForeignTradeAccess`): ruta de Comercio Exterior, mismo comando.
- **Contrato:** C-F4-19 (las dos rutas).
- **Esquema:** `service_records.source_entry_cycle_id uuid NULL`, FK a `weighbridge_cycles(id)` `ON DELETE RESTRICT`, e índice.
- **Efectos secundarios:** servicio nuevo, orden despachada, historial.
- **Pruebas** (`Wms.Tests/Weighbridge/EntryTicketExitRulesTests.cs`, nuevo; función pura):
  - Tiquete de salida → error.
  - Tiquete no completo → error.
  - Tiquete usado con orden cancelada → válido.
  - Tiquete usado con orden vigente → error.
  - Ítem de un depósito que no está en el tiquete → error.
  - Todo en regla con la orden `Loaded` → válido y «despachar ahora».
- **Terminado cuando:** una orden de mercancía que llegó en el camión sale con su tiquete de ingreso sin cobro ni pesaje nuevos, desde báscula y desde Comercio Exterior. Dos camiones del mismo depósito salen así, cada uno con su orden y su guía.
- **Riesgo:** usar un tiquete de otro camión. Se mitiga con la comparación de vehículo y de depósitos.

---

#### F4-09 · Registro de impresiones y descargas de etiquetas (GAP-024 a, LEGACY-FUNC-141)

- **Dificultad:** Baja.
- **Regla:**
  1. Los tres endpoints de etiqueta aceptan `action` en la consulta: `Print` o `Download`, con `Download` por defecto. Son `GET foreign-trade/imports/{id}/label`, `exports/{id}/label` e `inspections/{id}/label`.
  2. Después de generar el PDF sin error, se guarda una fila en `warehouse_storage_label_prints` con `WarehouseStorageId`, `Action`, `PrintedById` y `CreatedAt`.
     - En importación, el `{id}` es el `ImportWarehouseStorage` y se guarda su `WarehouseStorageId`.
     - Un `action` inválido → 400 "La acción debe ser Print o Download."
  3. `GET foreign-trade/warehouse-storages/{id}/label-prints` devuelve los conteos por acción, la última impresión y las últimas 50 filas con usuario.
- **Evidencia:**
  - Legacy: `bodegas_schema.sql:25-35` (`adhesivos`: acción, depósito, usuario, IP, fecha); `modulos/mod_depositos/adhesivos.php:541-560` (conteo de impresiones y descargas).
  - v2: `Wms.Api/Controllers/v1/ForeignTradeController.cs:270`, `:709` y `:823` (sin registro).
- **Archivos:**
  - `Wms.Domain/Entities/ForeignTrade/WarehouseStorageLabelPrint.cs` (nuevo). Sigue el patrón de `DispatchGuidePrintLog.cs`, que ya registra la generación de guías por depósito: `IAuditable`, factoría `Create` y relación con `ApplicationUser` (`PrintedById`).
  - `Wms.Domain/Enums/LabelPrintAction.cs` (nuevo).
  - `Wms.Infrastructure/Persistence/Configurations/ForeignTrade/WarehouseStorageLabelPrintConfiguration.cs` (nuevo) y `AppDbContext.cs`.
  - `Wms.Application/ForeignTrade/Common/Services/LabelGenerationService.cs` (modifica: `RecordPrintAsync(warehouseStorageId, action, userId)`).
  - `Wms.Application/ForeignTrade/Queries/GetLabelPrints/*` (nuevo).
  - `ForeignTradeController.cs` (modifica solo los tres endpoints de etiqueta: parámetro `action`).
  - `Wms.Api/Controllers/v1/LabelPrintsController.cs` (nuevo; `[Route("foreign-trade")]`, `ForeignTradeAccess`).
- **Contrato:** C-F4-20 y C-F4-21.
- **Esquema:** tabla nueva `warehouse_storage_label_prints` (§F).
- **Efectos secundarios:** ninguno más.
- **Pruebas:** `Wms.Tests/ForeignTrade/LabelPrintActionTests.cs` (nuevo): `"print"` y `"Print"` se aceptan; `"imprimir"` → error; vacío → `Download`.
- **Terminado cuando:** cada impresión o descarga suma en su conteo.
- **Riesgo:** bajo.

---

#### F4-10 · Catálogo de cuadrillas y cuadrilla en la guía (GAP-026, LEGACY-FUNC-021 a 024)

- **Dificultad:** Media.
- **Regla:**
  1. **Entidad `Crew`** (tabla `crews`, `IAuditable`):
     - `Name`: 1 a 200 caracteres, único normalizado con `CatalogNameNormalizer`.
     - `IsActive`.
     - `LegacyId` (int?, único cuando no es nulo; para F6-02).
  2. **Administración** (solo Admin): crear, editar, activar o desactivar y eliminar.
     - Eliminar solo si no está en uso. Si lo está → 409 "La cuadrilla está en uso; desactívela en lugar de eliminarla."
     - Duplicado → 409 "Ya existe la cuadrilla {nombre}."
     - Nombre inválido → "El nombre de la cuadrilla es obligatorio y no puede exceder 200 caracteres."
     - Lectura: `GET administration/crews` (activas, búsqueda, `all`) para cualquier usuario autenticado.
  3. **Dónde se usa** (`crewId`, siempre opcional; si viene, debe existir y estar activa: 404 "La cuadrilla no existe o está inactiva."):
     - **Recepción:** la cuadrilla que descargó (`WarehouseStorage.CrewId`), en `POST warehouse/receptions`, `POST warehouse/receptions/{id}/complete` y `POST warehouse/receptions/without-weighbridge`. Equivale a `deposito.id_cuadrilla` del legacy.
     - **Orden de cargue:** la cuadrilla que carga (`LoadingOrder.CrewId`). Comercio Exterior la puede indicar al crear la orden (`POST foreign-trade/loading-orders` y `POST warehouse/loading-orders`) y Bodega la confirma o cambia al ejecutar el cargue. Equivale a `salida.id_cuadrilla`.
  4. **La guía** (importación y exportación) toma `Crew = nombre de la cuadrilla de la orden` al crearse. Hoy siempre es nula. El PDF ya imprime "Cuadrilla:".
- **Evidencia:**
  - Legacy:
    - `bodegas_schema.sql:247-255` (`cuadrilla`), `:271` (`deposito.id_cuadrilla`) y `:1321` (`salida.id_cuadrilla`);
    - `modulos/mod_cuadrillas/*` (CRUD);
    - `modulos/mod_salidas/verguia.php:765` (imprime la cuadrilla).
  - v2:
    - `Wms.Domain/Entities/Warehouse/DispatchGuide.cs:22,118-121` (`Crew` y `UpdateCrew` sin llamadores);
    - `CreateDispatchGuideCommandHandler.cs:190` y `CreateExportDispatchGuideCommandHandler.cs:126` (`crew: null`);
    - `DispatchGuidePdfService.cs:522`.
- **Archivos:**
  - `Wms.Domain/Entities/Administration/Crew.cs` (nuevo) y su configuración en `Configurations/Administration/`.
  - `WarehouseStorage.cs` y `LoadingOrder.cs` (modifica: `CrewId` y `AssignCrew(Guid?)`) con sus configuraciones.
  - `Wms.Application/Administration/Crews/{Commands,Queries,Common}/*` (nuevos).
  - Los tres comandos y handlers de recepción, `CreateLoadingOrderCommand`/`Handler`, `ExecuteLoadingOrderCommand`/`Handler` y los dos handlers de guía (modifica).
  - Requests de `WarehouseController.cs` y `ForeignTradeController.cs` (modifica: `CrewId`).
  - DTO de detalle y listado de órdenes (`LoadingOrderDto`, `LoadingOrderListDto`) y de detalle de depósitos de importación, exportación e inspección (modifica: `CrewId`, `CrewName`).
  - `Wms.Api/Controllers/v1/CrewsController.cs` (nuevo; `[Route("administration")]`, `[Authorize]` y `AdminOnly` en las escrituras).
- **Contrato:** C-F4-22 (catálogo) y C-F4-23 (`crewId` en recepción, orden y cargue; guía con cuadrilla). C-F4-06 y C-F4-07 ya incluyen el campo.
- **Esquema:** tabla nueva `crews`; `warehouse_storages.crew_id uuid NULL` y `loading_orders.crew_id uuid NULL`, con FK a `crews(id)` `ON DELETE RESTRICT` e índices.
- **Efectos secundarios:** auditoría.
- **Pruebas:** `Wms.Tests/Domain/Administration/CrewTests.cs` (nuevo): nombre vacío → error; 201 caracteres → error; `Deactivate` y `Activate` cambian `IsActive`.
- **Terminado cuando:** la guía de una orden con cuadrilla la imprime.
- **Riesgo:** bajo.

---

### C.5 Fase 5 — Reportes y consultas

> **Estado: ✅ COMPLETADA el 2026-09-30** (F5-01 a F5-10, implementados en `develop` en una sola pasada por indicación del usuario). `dotnet build Wms.sln` sin errores y `dotnet test Wms.Tests` en verde (735 pruebas; 699 antes de la fase). Los cuatro criterios de salida se comprobaron además contra un Postgres temporal (40 comprobaciones de extremo a extremo, entre ellas el kardex 10/7/3/5/5/2 del criterio 3).
> **Pendiente del usuario:** revisar el diff, generar las migraciones y hacer el commit. Al cierre de la fase no se había generado ninguna migración de paridad: el modelo lleva 90 operaciones pendientes contra el snapshot, 88 de las fases 1 a 4 y 2 de esta (§F.1, filas 23 y 24).
> **Desviaciones respecto al texto de los ítems** (ninguna cambia una decisión de §A.4 ni de §B.4):
> 1. **F5-01.** Solo `GetDispatchGuidesQuery` no heredaba de `QueryParametersBase` (tenía su propio `PageIndex`/`PageSize`); ahora hereda, con 20 por defecto como antes. Las demás consultas de la lista ya cumplían.
> 2. **F5-02 — cálculo.** El listado de importaciones ya cargaba los productos y los levantes de la página: los saldos se calculan sobre esas entidades con `NationalizationBalance.ForDeposit` (función pura, probada), sin consultas extra. Exportación e inspección los calculan en la proyección de EF. Despachado = Σ max(0, recibido − stock).
> 3. **F5-03 — placa.** `PlateNormalizer.Normalize` conserva los guiones (placas extranjeras); el filtro usa `PlateNormalizer.ForSearch` (sin espacios ni guiones) y compara contra la placa guardada sin guiones, como pide C-F5-01. El listado de levantes excluye los depósitos anulados y valida el rango invertido con «La fecha final no puede ser anterior a la inicial.».
> 4. **F5-04 — salidas.** El tiquete de salida es el del ciclo del servicio de la orden o, en salida compartida (F4-07), el del ciclo ancla; los pesajes anulados no cuentan. La lectura de salidas quedó en `DepositDispatchReader`, que también usa el informe por CPI. Las secciones del kardex no dependen del rango de fechas de los movimientos.
> 5. **F5-05 — modalidad.** `IMP`, `EXP` e `INSP` se comparan como prefijo del código (`IMP001`, `EXP001`, `INSP001`); otro valor responde 400 «La modalidad debe ser IMP, EXP o INSP.». El manifiesto es el del depósito de importación o, si no lo tiene, el del primer camión (igual en pólizas y CPI).
> 6. **F5-06 — importador sin UAP.** Sin tercero IMPORTER, el detalle muestra el cliente como importador y toma su marca UAP (regla del ítem).
> 7. **F5-07 — política.** El ítem pone el endpoint en `InventoryReportsController` (`ActiveUser`) y C-F5-08 pide `ForeignTradeAccess`: la acción lleva además `[Authorize(Policy = "ForeignTradeAccess")]`; como los atributos se suman, exige las dos.
> 8. **F5-08 — año.** `billing-annual` valida el año con el mismo rango y mensaje de las pólizas. Solo aparecen los meses y días con facturas. El informe por CPI toma, por factura, el rango de los períodos del depósito en ella y la mayor fecha límite.
> 9. **F5-09 — impresión y totales.** La marca se guarda en `WeighbridgeTicketPdfService` tras armar el PDF, con la descripción de auditoría «Primera impresión del tiquete de báscula». `subtotal` e `taxAmount` salen de la misma factura que ya usaba `invoiceTotal` (0 sin factura). Los totales cargan una fila corta por ciclo y suman en memoria (el neto necesita el primer y último pesaje).
> 10. **F5-10 — salidas del detalle.** Una fila por movimiento de salida de orden ejecutada (producto por producto), con el saldo anterior del movimiento; se agregó `productName`. La salida por portería es la del `EntryLog` del ciclo de salida de la orden. La lista agrega `warehouseStorageNumber`.
>
> **Defectos previos corregidos dentro de la fase** (§G.20 y §G.21): el listado de importaciones y el informe de movimientos por depósito leían `UnitMeasure.Name` sin incluir la navegación y fallaban con `NullReferenceException` en cuanto había productos o movimientos.

- **Objetivo:** quien hoy saca un informe del legacy lo saca de la v2 con las mismas columnas, y lo puede exportar a Excel. El Excel lo genera el frontend con `all=true`.
- **Criterio de salida (verificable):**
  1. El listado de importaciones con `all=true` devuelve más de 50 filas, con las columnas de saldo.
  2. Cada informe de la tabla §C.5.0 responde con sus filtros.
  3. El kardex de un depósito con dos levantes y una salida cuadra ingreso − despachado = existencias y nacionalizado − despachado = nacionalizado disponible.
  4. `dotnet build` y `dotnet test` pasan.
- **Rama:** `develop` (§E). Empieza cuando la fase 4 tiene todos sus ítems con commit. Usa el FOB del levante (F2-05), `NationalizationBalance` (F2-01), las novedades (F4-03), `LoadedQuantity` (F3-01) y los períodos con fecha límite (F3-06).
- **Dificultad:** **Media**. Son consultas de solo lectura sobre datos que ya existen, sin transiciones.
- **Perfil de agente:** agente estándar.
- **Reglas comunes a todos los informes nuevos:**
  - Son consultas MediatR que heredan de `QueryParametersBase`: paginado con máximo 50, y `all=true` para el Excel. Nunca se sube el tope.
  - Las fechas de filtro son días calendario de Colombia (`ColombiaTime`), `desde` y `hasta` inclusivos.
  - Nunca incluyen depósitos `Cancelled`, pesajes anulados (F3-09) ni levantes retirados (F2-04, que ya no existen).
  - Solo leen: ningún informe escribe (a diferencia del legacy, RN-019, RN-023 y RN-037).
  - Los informes nuevos con totales responden `data: { items: [...], totals: {...} }` más la paginación; los totales cubren todo el filtro. Los listados existentes no cambian de forma.

#### C.5.0 Mapa de informes legacy → v2

| Informe legacy | Archivo legacy | Endpoint v2 | Ítem |
|---|---|---|---|
| Listado de depósitos de importación con saldos | `modulos/mod_depositos/*` | `GET foreign-trade/imports` (columnas nuevas) | F5-02 |
| Búsqueda por placa y levante; lista de levantes | `modulos/mod_levantes/*` | `GET foreign-trade/imports` (filtros) y `GET foreign-trade/releases` | F5-03 |
| Kardex / informe de movimiento de depósito | `modulos/mod_inventario/kardex.php` | `GET warehouse/movements-report` (ampliado) y su PDF | F5-04 |
| Reporte general de mercancías | `modulos/mod_inventario/reportegeneral.php` | `GET reports/general-inventory` | F5-05 |
| Informe de póliza y detalle | `modulos/mod_inventario/reportepoliza.php`, `reportepolizadetalle.php` | `GET reports/policies` y `GET reports/policies/detail` | F5-06 |
| Ingresos por producto y cliente | `modulos/mod_inventario/reporteingresoproductocliente.php` | `GET reports/incoming-by-product` | F5-07 |
| Informe de facturación (año) | `modulos/mod_facturacion/informefacturacion.php` | `GET reports/billing-annual` | F5-08 |
| Informe de facturación por CPI | `modulos/mod_facturacion/informecpi.php` | `GET reports/deposit-billing` | F5-08 |
| Reporte de báscula | `modulos/mod_bascula/reporteingresos.php` | `GET weighbridge/history` (filtros y columnas) | F5-09 |
| Reporte SIA (ingresos por agencia) | `reportesweb/reportesias.php`, `reportesiasdetalle.php` | `GET reports/customs-agency-entries` y su detalle | F5-10 |
| Abandono y prórroga | `reporteprorrogas.php`, `reporteabandonos.php` | ya en F2-10 | — |
| Diarios de ingreso y salida | `reportediario.php`, `reportediariosalidas.php` | existentes (`reports/daily-incoming-goods`, `reports/daily-outgoing-goods`) | — |

---

#### F5-01 · Exportación a Excel sin tope de filas (GAP-017, LEGACY-FUNC-232)

- **Dificultad:** Baja.
- **Regla:**
  1. Todo listado o informe que el frontend exporta a Excel se consulta con `all=true`. `QueryParametersBase` ya lo resuelve: `PageIndex = 1` y `PageSize = int.MaxValue`.
  2. Hay que verificar, y corregir si falta, que heredan de `QueryParametersBase` y pasan `PageIndex`/`PageSize` a `PaginatedList.CreateAsync`:
     - `GetImportDepositsQuery`, `GetExportDepositsQuery` y `GetInspectionDepositsQuery`;
     - `GetInventoryMovementsQuery` (`GET warehouse/inventory/movements`, que es la fuente del botón «Exportar Excel» de inventario, hoy roto en el frontend);
     - `GetWeighbridgeHistoryQuery`, `GetLoadingOrdersQuery`, `GetDispatchGuidesQuery` y `GetInvoicesQuery`;
     - todas las consultas nuevas de las fases 2 a 5.
  3. No se agrega un endpoint de exportación en el backend: el frontend arma el Excel.
  4. El contrato publica la tabla de endpoints por exportación (C-F5-14).
- **Evidencia:**
  - v2: `Wms.Common/Wrappers/QueryParametersBase.cs:11,20-32`.
  - Frontend: `Frontend/wms/app/features/foreign-trade/composables/useExportImportsToExcel.ts:14-18` (pide `pageSize: 10000`) y `Frontend/wms/app/features/warehouse/composables/useWarehouseExports.ts:35` (método inexistente).
  - Legacy: `reportes/reporteexcel.php:1-26`.
- **Archivos:** las consultas citadas, solo si alguna no hereda o ignora la paginación (modifica).
- **Contrato:** C-F5-14.
- **Esquema:** ninguno.
- **Efectos secundarios:** ninguno.
- **Pruebas:** `Wms.Tests/Common/QueryParametersBaseTests.cs` (nuevo si no existe):
  - `All = true` → `PageIndex` 1 y `PageSize` `int.MaxValue`.
  - `PageSize = 100` → 50.
  - `PageSize = 0` → 1.
  - `PageIndex = -3` → 1.
- **Terminado cuando:** cada endpoint de la tabla C-F5-14 devuelve todas las filas con `all=true`.
- **Riesgo:** consultas muy pesadas con `all=true`. Se mitiga con los filtros de fecha obligatorios de cada informe (se indican en su ítem).

---

#### F5-02 · Columnas de saldo en el listado de importaciones (UI-17)

- **Dificultad:** Baja.
- **Regla:** `ImportDepositDto` agrega, por depósito, la suma de sus productos:

  | Campo | Rótulo | Cálculo |
  |---|---|---|
  | `ReceivedQuantity` | Ingreso | Σ `ReceivedQuantity` |
  | `NationalizedQuantity` (existe) | Nacionalizado | Σ levantes (F2-01) |
  | `PendingToNationalize` | Por nacionalizar | Σ `NationalizationBalance.PendingToNationalize` |
  | `DispatchedQuantity` | Despachado | Σ (`ReceivedQuantity − CurrentStock`) |
  | `CurrentStock` (existe) | Existencias | Σ `CurrentStock` |

  - Se calculan en la proyección de EF, sin cargar entidades.
  - Se aplica el mismo cambio a `ExportDepositDto` e `InspectionDepositDto` para Ingreso, Despachado y Existencias. En esas modalidades no hay nacionalización.
- **Evidencia:**
  - Legacy: `bodegas_schema.sql` vista `vista_kardexdepositos2` (`ingresan`, `nacionalizados`, `salen`, `saldo`).
  - v2: `Wms.Application/ForeignTrade/Common/DTOs/ImportDepositDto.cs:15,22`.
- **Archivos:**
  - `ImportDepositDto.cs`, `ExportDepositDto.cs` e `InspectionDepositDto.cs` (modifica).
  - Handlers de `GetImportDeposits`, `GetExportDeposits` y `GetInspectionDeposits` (modifica).
- **Contrato:** C-F5-01.
- **Esquema:** ninguno.
- **Efectos secundarios:** ninguno.
- **Pruebas:** en `Wms.Tests/ForeignTrade/NationalizationBalanceTests.cs` (existe desde F2-01), caso de agregado por depósito: dos productos (10 recibidos, 4 levantados, 2 despachados; 5 recibidos, 0 levantados, 0 despachados) → ingreso 15, nacionalizado 4, por nacionalizar 11, despachado 2, existencias 13.
- **Terminado cuando:** el listado muestra las cinco columnas.
- **Riesgo:** bajo.

---

#### F5-03 · Búsqueda por placa y por levante; listado de levantes (UI-18)

- **Dificultad:** Media.
- **Regla:**
  1. **`GET foreign-trade/imports`** agrega dos filtros:
     - `vehiclePlate`: algún camión del depósito tiene esa placa (`WarehouseStorageEntry.VehiclePlate`, `ILIKE` con `%` a ambos lados, normalizada con `PlateNormalizer`);
     - `releaseNumber`: algún levante tiene ese número o esa aceptación (`ILIKE`).
  2. **Listado nuevo** `GET foreign-trade/releases`:
     - Filtros: `releaseNumber` (número o aceptación), `warehouseStorageNumber`, `importerId`, `customsAgencyId`, `fromDate` y `toDate` (fecha del levante), paginado y `all`.
     - Una fila por levante de producto: `releaseId`, `releaseNumber`, `releaseDate`, `acceptanceNumber`, `acceptanceDate`, `warehouseStorageId`, `importWarehouseStorageId`, `warehouseStorageNumber`, `importerName`, `customsAgencyName`, `productName`, `releasedQuantity`, `releasedWeight`, `fobUsd`, `exchangeRate`, `fobCop` y `createdAt`.
     - Orden: fecha del levante descendente.
- **Evidencia:**
  - Legacy: `modulos/mod_levantes/listarlevantes.php` (listado y búsqueda por número); búsqueda por placa en el listado de depósitos.
  - v2: `Wms.Application/ForeignTrade/Queries/GetImportDeposits/GetImportDepositsQuery.cs:15-28` (sin placa ni levante).
- **Archivos:**
  - `GetImportDepositsQuery.cs` y su handler (modifica).
  - `Wms.Application/ForeignTrade/Queries/GetReleases/*` (nuevo) y `Wms.Application/ForeignTrade/Common/DTOs/ReleaseListItemDto.cs` (nuevo).
  - `Wms.Api/Controllers/v1/ReleasesController.cs` (nuevo; `[Route("foreign-trade")]`, `ForeignTradeAccess`).
- **Contrato:** C-F5-01 (filtros) y C-F5-02.
- **Esquema:** ninguno (la búsqueda por aceptación usa el índice de F2-03).
- **Efectos secundarios:** ninguno.
- **Pruebas:** `Wms.Tests/Common/PlateNormalizerTests.cs` (existe): `" abc-123 "` → `"ABC123"` como entrada del filtro. El resto se verifica con el criterio de salida.
- **Terminado cuando:** se encuentra un depósito por placa y por número de levante, y el listado de levantes pagina.
- **Riesgo:** bajo.

---

#### F5-04 · Kardex con levantes y despachos (GAP-016, LEGACY-FUNC-209)

- **Dificultad:** Media.
- **Regla:** el informe de movimientos por depósito (`GET warehouse/movements-report` y `/pdf`) agrega las secciones del kardex legacy.
  1. **Por producto**, en `WarehouseStorageMovementsProductDto`:
     - `ReceivedQuantity`;
     - `NationalizedQuantity`, `PendingToNationalize` y `NationalizedAvailable` (de `NationalizationBalance`; nulos si el depósito no es de importación);
     - `DispatchedQuantity` (`Received − Current`).
  2. **`Releases`** (solo importación): lista de levantes con `releaseNumber`, `acceptanceNumber`, `releaseDate`, `releasedWeight`, `fobUsd` y `lines: [{ warehouseStorageProductId, quantity }]`, agrupada por par número–aceptación y ordenada por fecha.
  3. **`Dispatches`**: órdenes ejecutadas (`Loaded`, `Dispatched` o `Complete`, no revertidas) con ítems del depósito:
     - `loadingOrderNumber`, `departureDate` (o la fecha de fin de cargue si no salió), `vehiclePlate`, `guideNumber` (guía vigente o nulo) y `ticketNumber` (tiquete del pesaje de salida o nulo);
     - `lines: [{ warehouseStorageProductId, quantity }]`, con la cantidad cargada (F3-01) o, para órdenes anteriores, la suma de sus movimientos `Out`.
  4. **Totales del encabezado:** ingreso, nacionalizado, por nacionalizar, despachado, existencias y nacionalizado disponible. Los pesos se omiten: la v2 no guarda peso por producto (WMS-10).
  5. El PDF agrega las secciones INGRESO, NACIONALIZADOS, POR NACIONALIZAR, DESPACHADOS y EXISTENCIAS con esos datos, en el orden del legacy.
- **Evidencia:**
  - Legacy: `modulos/mod_inventario/kardex.php:235-256` (encabezado), `:266-307` (ingreso), `:315-371` (levantes), `:373-407` (por nacionalizar), `:416-491` (salidas) y `:515-547` (existencias y saldo nacionalizado).
  - v2: `Wms.Application/Warehouse/Common/DTOs/WarehouseStorageMovementsReportDto.cs:6-33` (sin levantes ni salidas agrupadas).
- **Archivos:**
  - `WarehouseStorageMovementsReportDto.cs` (modifica).
  - `Wms.Application/Warehouse/Queries/GetWarehouseStorageMovements/GetWarehouseStorageMovementsHandler.cs` (modifica).
  - El servicio del PDF de ese informe (modifica; se localiza por su uso en `WarehouseMovementsReportController.cs:61`).
- **Contrato:** C-F5-03.
- **Esquema:** ninguno.
- **Efectos secundarios:** ninguno.
- **Pruebas:** `Wms.Tests/Warehouse/KardexAggregationTests.cs` (nuevo; función pura `KardexAggregator.Build(products, releases, dispatches)`):
  - Recibido 10, levantes 4 + 3, despachado 5 → por nacionalizar 3, existencias 5, nacionalizado disponible 2.
  - Sin levantes → nacionalizado 0.
  - Dos productos en un mismo levante → una fila de levante con dos líneas.
- **Terminado cuando:** el informe y el PDF muestran las cinco secciones del kardex legacy.
- **Riesgo:** bajo.

---

#### F5-05 · Inventario general filtrable (GAP-016, LEGACY-FUNC-211)

- **Dificultad:** Media.
- **Regla:** `GET reports/general-inventory`. Una fila por producto de depósito.
  1. **Filtros:**
     - `balanceType`: `WithBalance` (por defecto; `CurrentStock > 0`) o `All`;
     - `fromDate` y `toDate` (fecha de ingreso del depósito; opcionales, pero con `balanceType = All` son obligatorios: "Indique el rango de fechas para consultar todo el inventario.");
     - `importerId`, `customsAgencyId`, `transportCompanyId` y `productId`;
     - `operationModalityCode` (`IMP`, `EXP` o `INSP`);
     - `warehouseLocationId`: con ubicación (F4-01) o como ubicación principal;
     - `includeReleases` (bool).
     - No se replican los filtros de Colmotores.
  2. **Columnas**, en el orden del legacy: `warehouseStorageNumber`, `entryDate`, `cargoManifestNumber` (C.P.I.), `manifestNumber`, `productName` y `packagingName`, `importerName`, `customsAgencyName`, `locations` (códigos de ubicación separados por coma), `receivedQuantity` (Entran), `nationalizedQuantity` (Nalzdos., nulo fuera de importación), `dispatchedQuantity` (Salen), `currentStock` (Saldo) y `releaseNumbers` (solo con `includeReleases`).
  3. **Totales:** la respuesta es `data: { items: [...], totals: {...} }` más la paginación. `totals` suma las cuatro cantidades sobre todo el filtro, no solo la página. Es la forma común de los informes nuevos con totales.
  4. Orden: fecha de ingreso ascendente y número de depósito.
- **Evidencia:** legacy `modulos/mod_inventario/reportegeneral.php:85-125` (filtros) y `:600-690` (filas); `:259-262` (`tiposaldo` saldo o todo).
- **Archivos:**
  - `Wms.Application/Reports/Queries/GetGeneralInventory/*` (nuevo) y `Wms.Application/Reports/Common/DTOs/GeneralInventoryRowDto.cs` (nuevo).
  - `Wms.Api/Controllers/v1/InventoryReportsController.cs` (nuevo; `[Route("reports")]`, `ActiveUser`, porque lo usan Bodega y Comercio Exterior).
- **Contrato:** C-F5-04.
- **Esquema:** ninguno.
- **Efectos secundarios:** ninguno.
- **Pruebas:** `Wms.Tests/Reports/GeneralInventoryQueryValidatorTests.cs` (nuevo): `All` sin fechas → error; `All` con fechas → válido; `WithBalance` sin fechas → válido; `toDate` anterior a `fromDate` → error "La fecha final no puede ser anterior a la inicial."
- **Terminado cuando:** el informe filtra por cada criterio y devuelve totales.
- **Riesgo:** rendimiento. Se mitiga con la proyección en SQL y el rango obligatorio para `All`.

---

#### F5-06 · Pólizas por año, mes y UAP (GAP-016, LEGACY-FUNC-215, P12)

- **Dificultad:** Media.
- **Regla:**
  1. **Marca UAP en el tercero:**
     - `Stakeholder.IsUap` (bool, por defecto false). Se edita al crear y actualizar el tercero (`POST stakeholder`, `PATCH stakeholder/{id}`) y se expone en sus DTO.
     - Es la `cliente.uap` del legacy.
  2. **Resumen anual** `GET reports/policies?year=` (obligatorio, 2000 a 2100): 12 filas, una por mes (`month` 1 a 12), con `uapValueUsd`, `nonUapValueUsd` y `totalValueUsd`, más la fila de totales.
     - Cálculo: por mes de la **fecha de ingreso del depósito** (`EntryDate` en Colombia), se suma el `FobUsd` de los levantes (F2-05) de los depósitos de importación de ese mes.
     - UAP o no UAP según `IsUap` del **importador** del depósito (rol IMPORTER; si no tiene, el cliente).
     - Los levantes sin FOB suman 0.
     - El legacy rotula estas columnas «CIF UAP» y «CIF NUAP» pero suma el FOB en dólares del levante. Se conserva el cálculo; el rótulo lo decide el frontend (ver §G).
  3. **Detalle** `GET reports/policies/detail?year=&month=&uap=` (`uap`: `true`, `false` o ausente para ambos). Una fila por levante de producto, con las columnas del legacy:
     - `entryDate`, `warehouseStorageNumber`, `cargoManifestNumber`, `manifestNumber`, `cargoUnitPlates` (contenedor);
     - `importerName`, `customsAgencyName`, `productName`;
     - `receivedQuantity`, `nationalizedQuantity`, `dispatchedQuantity` y `currentStock` (del producto);
     - `releaseNumber`, `acceptanceNumber`, `releaseDate`, `fobUsd` y `isUap`.
     - La respuesta incluye el total de `fobUsd`.
  4. El PDF del resumen no se construye en el backend. Las firmas del legacy («Firma funcionario», «Jefe del depósito», «Recibí conforme») las agrega el frontend si imprime.
- **Evidencia:**
  - Legacy: `modulos/mod_inventario/reportepoliza.php:380-428` (por mes de `fecha_deposito`, `SUM(fob_dolares)` por levante, UAP según `cliente.uap`); `reportepolizadetalle.php` (columnas); `bodegas_schema.sql:187` (`cliente.uap`).
  - v2: `Wms.Domain/Entities/Stakeholder/Stakeholder.cs` (sin UAP).
- **Archivos:**
  - `Stakeholder.cs` (modifica: `IsUap`, en `Create` y en la actualización; `StakeholderManageParams` y `UpdateStakeholderParams`) y `StakeholderConfiguration.cs` (modifica).
  - `CreateStakeholder` y `UpdateStakeholder` (comando, validador y handler), sus DTO y el request del `StakeholderController` (modifica).
  - `Wms.Application/Reports/Queries/{GetPoliciesSummary,GetPoliciesDetail}/*` (nuevos).
  - `Wms.Api/Controllers/v1/PolicyReportsController.cs` (nuevo; `[Route("reports")]`, `ForeignTradeAccess`).
- **Contrato:** C-F5-05, C-F5-06 y C-F5-07 (tercero).
- **Esquema:** `stakeholders.is_uap boolean NOT NULL DEFAULT false`.
- **Efectos secundarios:** auditoría del cambio de UAP (ya la da `IAuditable`).
- **Pruebas:** `Wms.Tests/Reports/PolicySummaryCalculatorTests.cs` (nuevo, puro):
  - Levantes de 100 USD (UAP) y 50 USD (no UAP) en marzo → marzo 100 / 50 / 150, demás meses 0.
  - Levante sin FOB → 0.
  - Depósito ingresado el 31/01 23:30 hora de Colombia → enero (no febrero en UTC).
  - Año 1999 → error de validación "El año debe estar entre 2000 y 2100."
- **Terminado cuando:** el resumen y el detalle cuadran para un mes con levantes UAP y no UAP.
- **Riesgo:** importadores sin marca UAP al arrancar. Se mitiga con la migración de maestros (F6-02, columna `uap`).

---

#### F5-07 · Ingresos por producto y cliente (GAP-016, LEGACY-FUNC-216)

- **Dificultad:** Baja.
- **Regla:** `GET reports/incoming-by-product`.
  - **Filtros:** `fromDate` y `toDate` (obligatorios: "Indique el rango de fechas."), `importerId` (obligatorio, como en el legacy: "Seleccione el importador.") y `productId` (opcional).
  - Agrupa por producto y embalaje la suma de `ReceivedQuantity` de los productos de los depósitos cuyo importador (rol IMPORTER) es el indicado y cuya fecha de ingreso está en el rango.
  - **Columnas:** `productId`, `productName`, `packagingName` y `quantity`, más el total. Orden por nombre de producto.
- **Evidencia:** legacy `modulos/mod_inventario/reporteingresoproductocliente.php:85-95` (vista por `fechahora_ingreso` e importador, agrupado por producto y embalaje).
- **Archivos:** `Wms.Application/Reports/Queries/GetIncomingByProduct/*` (nuevo); `InventoryReportsController.cs` (modifica).
- **Contrato:** C-F5-08.
- **Esquema:** ninguno.
- **Efectos secundarios:** ninguno.
- **Pruebas:** validador (nuevo): sin importador → error; sin fechas → error; rango invertido → error.
- **Terminado cuando:** el informe agrupa por producto y embalaje.
- **Riesgo:** bajo.

---

#### F5-08 · Informe anual de facturación y facturación por CPI (GAP-016, LEGACY-FUNC-206 y 207, P12)

- **Dificultad:** Media.
- **Regla:**
  1. **Anual** `GET reports/billing-annual?year=&serviceCategory=`. `serviceCategory` es un valor de `InvoiceServiceCategory` y por defecto `Almacenamiento`, que era lo único que medía el legacy.
     - Facturas con número fiscal (`InvoiceNumber` no nulo), no anuladas, que tengan al menos una línea del servicio de la categoría (código por `MapCategoryToServiceCode`, que se extrae a un helper compartido).
     - La fecha es `CreatedAt` en Colombia.
     - Por mes y por día: `invoiceCount` y `totalAmount` (Σ `Total` de las líneas de ese servicio).
     - **Respuesta:** `months: [{ month, invoiceCount, totalAmount, days: [{ day, invoiceCount, totalAmount }] }]` y `totals`.
  2. **Por CPI** `GET reports/deposit-billing?warehouseStorageNumber=`:
     - **Encabezado:** depósito, carta porte, importador, fecha y hora de ingreso, agencia, manifiesto y TRM de ingreso (`WarehouseStorage.Trm`).
     - **Cantidades por producto:** ingreso, despachado y existencias.
     - **Despachos:** placa y tiquete de cada salida.
     - **Facturas de almacenamiento del depósito** (vía `StorageBillingPeriod`), incluidas las anuladas con su estado:
       - `invoiceNumber`, `invoiceDate` (`CreatedAt`), `periodStart`, `periodEnd`, `limitDate` (F3-06);
       - `billedTo`, `total`, `status`, `notes`, `reissuedAsInvoiceNumber` (F3-10).
     - El total suma solo las no anuladas.
     - Depósito inexistente → 404 "No se encontró el depósito '{número}'."
- **Evidencia:** legacy `modulos/mod_facturacion/informefacturacion.php` (por año: mes, día, cantidad y total) e `informecpi.php` (encabezado, cantidades y facturas por depósito).
- **Archivos:**
  - `Wms.Application/Billing/Common/Services/InvoiceServiceCategoryCodes.cs` (nuevo: el mapeo que hoy está en `GetInvoicesHandler.cs:140-147`, que pasa a usarlo).
  - `Wms.Application/Reports/Queries/{GetBillingAnnual,GetDepositBilling}/*` (nuevos).
  - `Wms.Api/Controllers/v1/BillingReportsController.cs` (nuevo; `[Route("reports")]`, `BillingAccess`).
- **Contrato:** C-F5-09 y C-F5-10.
- **Esquema:** ninguno.
- **Efectos secundarios:** ninguno.
- **Pruebas:** `Wms.Tests/Reports/BillingAnnualAggregatorTests.cs` (nuevo, puro):
  - Dos facturas el 05/03 y una el 06/03 → marzo 3 facturas con dos días.
  - Factura anulada → no cuenta.
  - Factura sin número → no cuenta.
  - Factura creada el 31/03 a las 23:00 en Colombia → marzo.
- **Terminado cuando:** los totales del año cuadran con el listado de facturas filtrado.
- **Riesgo:** bajo.

---

#### F5-09 · Reporte de báscula con los filtros del legacy (GAP-016, LEGACY-FUNC-121)

- **Dificultad:** Media.
- **Regla:**
  1. **Filtros nuevos** en `GET weighbridge/history`:
     - `operationModalityId`;
     - `transportCompanyId` (tercero TRANSPORT_COMPANY del servicio);
     - `customerId`;
     - `zeroValue` (bool: el ciclo no tiene factura o su total es 0);
     - `pendingPayment` (bool: tiene factura no anulada con saldo pendiente, `Total − AmountPaid > 0`);
     - `notPrinted` (bool: el tiquete nunca se imprimió).
  2. **Columnas nuevas** en `WeighbridgeHistoryDto`:
     - `grossWeightKg`, `tareWeightKg` y `netWeightKg` (del primer y último pesaje del ciclo, con el neto como diferencia absoluta);
     - `reweighed` (bool: más de dos pesajes);
     - `subtotal`, `taxAmount`, `cashReceived` y `changeGiven` (F1-09, nulos si no fue en efectivo);
     - `isVoided`, `voidedAt` y `voidReason` (F3-09);
     - `ticketFirstPrintedAt`.
  3. **Tiquete impreso:** `WeighbridgeCycle.TicketFirstPrintedAt` (nuevo) se llena la primera vez que se genera su PDF (`GET weighbridge/{id}/ticket/pdf` o `GET weighbridge/entries/{entryId}/ticket/pdf`) y no cambia después. Es el «no impresos» del legacy.
  4. **Totales** en un endpoint aparte, para no cambiar la forma del listado: `GET weighbridge/history/totals`, con los mismos filtros, devuelve `{ count, netWeightKg, subtotal, taxAmount, total }` sobre todo el filtro.
- **Evidencia:**
  - Legacy `modulos/mod_bascula/reporteingresos.php`: filtros de fecha, cliente, transportadora, placa, modalidad, en ceros, por cobrar y no impresos; columnas de tiquete, fecha, vehículo, conductor, modalidad, P. bruto, tara, neto, repesa, subtotal, pago, cambio y factura SIIGO.
  - v2: `Wms.Application/Weighbridge/Queries/GetWeighbridgeHistory/GetWeighbridgeHistoryQuery.cs:14-22`; `Wms.Api/Controllers/v1/WeighbridgeCycleReadController.cs:57-90` (PDF del tiquete sin registro).
- **Archivos:**
  - `GetWeighbridgeHistoryQuery.cs` y `GetWeighbridgeHistoryHandler.cs` (modifica).
  - `WeighbridgeHistoryDto.cs` (modifica).
  - `WeighbridgeCycle.cs` (modifica: `TicketFirstPrintedAt`, `MarkTicketPrinted()`) y `WeighbridgeCycleConfiguration.cs`.
  - `WeighbridgeTicketPdfService.cs` o `WeighbridgeCycleReadController.cs` (modifica: marca la impresión y guarda).
- **Contrato:** C-F5-11.
- **Esquema:** `weighbridge_cycles.ticket_first_printed_at timestamptz NULL`.
- **Efectos secundarios:** la primera generación del tiquete escribe una fecha. Es la única escritura de esta fase y ocurre en la descarga del tiquete, no en un listado.
- **Pruebas:**
  - `WeighbridgeCycleTests` (modifica): `MarkTicketPrinted` dos veces conserva la primera fecha.
  - `Wms.Tests/Weighbridge/WeighingTotalsTests.cs` (nuevo, puro): pesajes 30 000 y 12 000 → bruto 30 000, tara 12 000, neto 18 000; tres pesajes → `reweighed` true.
- **Terminado cuando:** el historial filtra por modalidad, transportadora, en ceros, por cobrar y no impresos, y muestra los pesos.
- **Riesgo:** bajo.

---

#### F5-10 · Ingresos por agencia de aduanas (GAP-010, LEGACY-FUNC-229)

- **Dificultad:** Media.
- **Regla:**
  1. **Listado** `GET reports/customs-agency-entries?customsAgencyId=` (obligatorio: "Seleccione la agencia de aduanas."):
     - Depósitos no anulados donde la agencia es el tercero CUSTOMS_AGENCY, ordenados por fecha de ingreso descendente.
     - **Columnas:** `warehouseStorageId`, `cargoManifestNumber` (carta porte), `importerName`, `products` (nombre y embalaje), `receivedQuantity`, `entryDate` y `process` (`Báscula` si está en Borrador, `Depósito` si está confirmado o cerrado).
     - **Visibilidad**, como el legacy: un depósito con existencias ≤ 0 solo se muestra si tuvo una salida (orden ejecutada) en las últimas 13 horas. Los depósitos en Borrador se muestran siempre.
  2. **Detalle** `GET reports/customs-agency-entries/{warehouseStorageId}` (404 si la agencia del depósito no es la indicada en `customsAgencyId`):
     - **Pesajes:** tiquete, placa, fecha, bruto, tara y neto.
     - **Novedades** (F4-03), sin las anuladas.
     - **Salidas:** fecha, placa, cantidad, saldo anterior, hora de salida por portería (`EntryLog.DateTimeDeparture`, si existe) y número de guía.
  3. El acceso externo de las agencias queda fuera: el informe lo consulta el personal interno (`ForeignTradeAccess`).
- **Evidencia:**
  - Legacy: `reportesweb/reportesias.php:44-50` (ingresos activos de la SIA), `:158-200` (proceso Báscula/Depósito y regla de 13 horas) y `reportesiasdetalle.php` (pesajes, observaciones y salidas).
  - Defecto legacy que no se replica: en `reportesias.php` el saldo de una fila «Báscula» arrastra el de la fila anterior.
- **Archivos:**
  - `Wms.Application/Reports/Queries/{GetCustomsAgencyEntries,GetCustomsAgencyEntryDetail}/*` (nuevos).
  - `Wms.Application/Reports/Common/CustomsAgencyVisibility.cs` (nuevo, puro).
  - `Wms.Api/Controllers/v1/CustomsAgencyReportsController.cs` (nuevo; `[Route("reports")]`, `ForeignTradeAccess`).
- **Contrato:** C-F5-12 y C-F5-13.
- **Esquema:** ninguno.
- **Efectos secundarios:** ninguno.
- **Pruebas:** `Wms.Tests/Reports/CustomsAgencyVisibilityTests.cs` (nuevo):
  - Existencias 5 → visible.
  - Existencias 0 y salida hace 12 h → visible.
  - Existencias 0 y salida hace 14 h → oculto.
  - Borrador con existencias 0 → visible.
  - Existencias 0 sin salidas → oculto.
- **Terminado cuando:** el listado y el detalle responden para una agencia con depósitos en los dos procesos.
- **Riesgo:** bajo.

---

### C.6 Fase 6 — Migración de datos, conciliación y respaldos

> **Estado: ✅ COMPLETADA. Implementada el 2026-10-01; la prueba con datos reales (E19) se cumplió el 2026-10-06** en la repetición de la fase 1 de la migración (`docs/planes/migracion-staging/resultados/informe-fase-1-repeticion.md`, criterio OK-6 «Cumple», tras corregir DEF-MIG-001 a 006). Queda abierta, fuera de esta fase, la validación de la equivalencia FOB/CIF del legacy (`docs/analisis/revision-fob-cif-migracion-v2-2026-10-08.md`).
> *Estado original (2026-10-01):* implementada; no se daba por cerrada hasta la prueba con datos reales (E19). F6-01 a F6-05 en `develop`, en una sola pasada por indicación del usuario. `dotnet build Wms.sln` sin errores y `dotnet test Wms.Tests` en verde (803 pruebas; 735 antes de la fase). Los criterios de salida 1 a 4 se comprobaron con CSV de prueba contra un Postgres 18 temporal y un S3 compatible (`adobe/s3mock`; la imagen de MinIO ya no se publica en Docker Hub): 45 comprobaciones de extremo a extremo, entre ellas simulación y firme por entidad, conciliación `Ok`/`Difference`/`NotMigrated`, período del migrado desde el 15/09 tras un último fin facturado el 14/09, y un respaldo manual en un destino local y uno S3 con la retención borrando la diaria y la mensual vencidas.
> **Commiteada** en `bf64de1`. El esquema de las seis fases quedó en la migración inicial única `20261001193201_InitialParityLegacy` (§E.3), que exige recrear las bases con el historial viejo.
> **Pendientes del usuario (cerrados):** recrear la base de desarrollo y la de staging, construir la imagen de staging con el `Dockerfile.staging` nuevo y la prueba E19 con los CSV reales del legacy. Los tres se hicieron en la migración a staging del 2026-10-06 (`docs/planes/migracion-staging/plan-migracion-legacy-staging.md`, fases 1 a 3).
> **Desviaciones respecto al texto de los ítems** (ninguna cambia una decisión de §A.4 ni de §B.4):
> 1. **F6-01 — simulación.** La simulación recorre el mismo camino que la carga en firme (constraints incluidos) dentro de una transacción que se revierte; después se guarda solo el lote. `LegacyImportBatch`, `LegacyIdMap` y `BackupRun` no son `IAuditable`: son bitácoras (los maestros que crean sí se auditan); `BackupDestination` sí lo es. Las cuentas `created`/`updated`/`skipped` son por fila (en depósitos, filas de producto). La carga de ciudades (F2-06) registra su lote con `entity = "Cities"`; el endpoint común responde 400 para `Cities`.
> 2. **F6-02 — equivalentes.** Una fila cuyo id ya tiene correspondencia se omite (`skipped`); una que encuentra un registro equivalente sin correspondencia se asocia (`updated`) y le completa lo vacío: roles, marca UAP, configuración de facturación si no tenía, transportadora del vehículo. A una cuadrilla equivalente por nombre no se le asigna el `LegacyId`.
> 3. **F6-02 — ubicaciones.** «Capacidad 0» choca con el dominio (`WarehouseLocation.Create` exige > 0) y con la restricción `chk_warehouse_location_capacity_positive` de la base. Para no tocar el esquema entran con capacidad 1 (`LocationsImporter.LegacyCapacity`), que Comercio Exterior ajusta; la recepción no valida la capacidad (§G.15).
> 4. **F6-03 — tipo de documento.** El CSV no trae el tipo del documento comercial: el servicio migrado queda con «Carta Porte» (`CARTA-PORTE`), que es lo que compara báscula para el 409 de documento cerrado. Un depósito cuyas filas no coinciden en sus datos de cabecera se rechaza entero.
> 5. **F6-03 — levantes.** El reparto del FOB por par número–aceptación se aplica también al peso bruto (también es del levante: sumarlo por producto lo multiplicaría en el kardex y en `NationalizedWeight`); por eso el peso de las filas siguientes es 0. FOB > 0 sin tasa es error de fila. `fob_pesos` del legacy se conserva si viene; si no, se calcula. Los levantes no registran correspondencia en `legacy_id_map` (no tienen id propio en el CSV): se deduplican por número, aceptación y producto.
> 6. **F6-04.** La conciliación agrega `errors` (filas ilegibles) a la respuesta de C-F6-03. Un depósito pedido por id que ya tiene períodos responde `Skipped`; uno sin cargos o con ciclo a demanda, también `Skipped`.
> 7. **F6-05 — capas.** La orquestación (`BackupService`) y la política pura quedaron en `Wms.Application/Administration/Backups/Common`: avisa con `INotificationOrchestrator`, que es de la aplicación, e infraestructura no puede depender de ella. Los destinos (`LocalBackupTarget`, `S3BackupTarget`), `PgDumpRunner` (que también arma el `tar.gz` con `System.Formats.Tar`) y la fábrica están en `Wms.Infrastructure/Services/Backups`.
> 8. **F6-05 — reglas no escritas.** Una corrida parcial cuenta como exitosa para «no repetir en el día» y para el mensual. Una corrida `Running` de más de 6 horas se considera colgada y no bloquea otra. `Backups:Enabled` es false por defecto (en staging se activa con `Backups__Enabled=true`); `Backups:PgDumpPath` permite otra ruta de `pg_dump`. Dos corridas en el mismo minuto comparten el nombre de archivo del formato del ítem.

- **Objetivo:** la v2 arranca con los maestros y los saldos vivos del legacy (P13), se concilia uno a uno contra el legacy y queda con respaldo diario configurable (P14).
- **Criterio de salida (verificable):**
  1. Cada CSV de la §C.6.1 se importa primero en simulación (`dryRun=true`) sin errores, o con errores explicados, y luego en firme.
  2. La conciliación de los depósitos vivos da 0 diferencias, o solo diferencias explicadas.
  3. La facturación de los depósitos migrados se abre contigua al último período facturado en el legacy.
  4. Un respaldo manual queda en un destino local y en uno S3, y la retención borra los vencidos.
  5. `dotnet build` y `dotnet test` pasan.
- **Rama:** `develop` (§E). Empieza cuando la fase 5 tiene todos sus ítems con commit. Usa ciudades (F2-06), ciclos (F3-05), períodos (F3-06), cuadrillas (F4-10), UAP (F5-06) y FOB (F2-05).
- **Dificultad:** **Muy alta**. Se cargan datos reales que no se pueden repetir sin limpieza, con correspondencias de catálogos y saldos que deben cuadrar.
- **Perfil de agente:** agente capaz, con revisión humana y prueba con datos reales antes de cerrar la fase. La prueba con datos reales del roadmap 6.6 está pendiente por decisión del usuario (E19); esta fase no se da por cerrada sin ella.
- **Orden interno:** F6-01 → F6-02 → F6-03 → F6-04 → F6-05. F6-05 no depende de las anteriores y puede ir primero si el corte se acerca.

#### C.6.1 Orden de carga en el corte

Cada paso primero en simulación y luego en firme:

1. Ciudades (F2-06).
2. Embalajes.
3. Cuadrillas.
4. Ubicaciones.
5. Terceros: clientes, agencias y transportadoras.
6. Vehículos.
7. Conductores.
8. Productos.
9. Depósitos vivos.
10. Levantes de los depósitos vivos.
11. Conciliación.
12. Configurar las tarifas a mano en el motor de acuerdos (P13).
13. Abrir la facturación de los depósitos migrados (F6-04).

---

#### F6-01 · Infraestructura de importación legacy (GAP-001)

- **Dificultad:** Alta.
- **Regla:**
  1. **Entidades:**

     | Entidad | Tabla | Campos |
     |---|---|---|
     | `LegacyImportBatch` | `legacy_import_batches` | `Entity` (texto, valor de `LegacyImportEntity`), `FileName`, `DryRun`, `TotalRows`, `CreatedRows`, `UpdatedRows`, `SkippedRows`, `ErrorRows`, `Errors` (jsonb, lista `{row, message}` de hasta 1000), `CreatedById`, `CreatedAt` |
     | `LegacyIdMap` | `legacy_id_map` | `Entity`, `LegacyId` (texto hasta 50), `TargetId` (uuid), `BatchId`, `CreatedAt`; único por (`Entity`, `LegacyId`) |

     - Se guarda un lote también en simulación: sirve de bitácora.
     - `LegacyImportEntity`: `PackagingTypes`, `Crews`, `Locations`, `Customers`, `CustomsAgencies`, `TransportCompanies`, `Vehicles`, `Drivers`, `Products`, `Deposits` y `Releases`. Las ciudades usan su propia importación (F2-06) y registran también su lote.
  2. **Lector** `LegacyCsvReader` (puro):
     - Codificación: UTF-8, con o sin BOM; si no es UTF-8 válido, Windows-1252, porque MySQL exporta `latin1`.
     - Separador `;`, `,` o tabulador, detectado en la primera fila de datos.
     - Campos entre comillas dobles, con `""` como comilla escapada.
     - `headerRows` ≥ 0; líneas vacías ignoradas; valores recortados.
     - Números con punto decimal; con separador `;` se acepta también la coma decimal.
     - Fechas `yyyy-MM-dd` o `yyyy-MM-dd HH:mm:ss`, interpretadas en hora de Colombia.
     - Cada fila conserva su número de línea.
  3. **Endpoint común** `POST administration/legacy-import/{entity}` (multipart: `file`, `headerRows` con valor por defecto 1, `dryRun` con valor por defecto true; `AdminOnly`):
     - Valida todas las filas.
     - Con `dryRun=false`, guarda **todas las filas válidas** en una transacción, con sus correspondencias en `legacy_id_map`.
     - Una fila cuyo `LegacyId` ya está en el mapa se trata según el ítem: se actualiza o se omite.
     - La respuesta es `LegacyImportResultDto` con hasta 500 errores.
     - Errores del archivo:
       - Entidad desconocida → 400 "La entidad {x} no se puede importar."
       - Archivo vacío → 400 "El archivo no tiene filas."
       - Más de 50 000 filas → 400 "El archivo supera 50 000 filas; divídalo."
  4. **Consultas:** `GET administration/legacy-import/batches` (filtro `entity`, paginado) y `GET administration/legacy-import/batches/{id}`.
  5. **Esquema de apoyo** para F6-03:
     - `warehouse_storages.legacy_number varchar(30) NULL`, único cuando no es nulo;
     - `warehouse_storages.is_migrated boolean NOT NULL DEFAULT false`;
     - `warehouse_storages.billing_start_date date NULL` (inicio de facturación de un migrado).
- **Evidencia:** legacy `bodegas_schema.sql` (81 tablas, `latin1`); roadmap 6.1 a 6.3; v2 sin mecanismo de carga (`Wms.Infrastructure/Persistence/SeedDataExtensions.cs` solo siembra catálogos).
- **Archivos:**
  - `Wms.Domain/Entities/Administration/{LegacyImportBatch,LegacyIdMap}.cs` (nuevos) y `Wms.Domain/Enums/LegacyImportEntity.cs` (nuevo).
  - Configuraciones nuevas en `Configurations/Administration/` y `AppDbContext.cs`.
  - `Wms.Application/Administration/LegacyImport/Common/{LegacyCsvReader,LegacyImportResultDto,LegacyIdMapService,LegacyValueParsers}.cs` (nuevos; el lector y los parsers son puros).
  - `Wms.Application/Administration/LegacyImport/Commands/ImportLegacyFile/*` (nuevo: despacha a un importador por entidad, `ILegacyEntityImporter`).
  - `Wms.Application/Administration/LegacyImport/Queries/{GetImportBatches,GetImportBatchById}/*` (nuevos).
  - `WarehouseStorage.cs` y `WarehouseStorageConfiguration.cs` (modifica: `LegacyNumber`, `IsMigrated`, `BillingStartDate`).
  - `Wms.Api/Controllers/v1/LegacyImportController.cs` (nuevo; `[Route("administration")]`, `AdminOnly`).
- **Contrato:** C-F6-01 y C-F6-02.
- **Esquema:** tablas `legacy_import_batches` y `legacy_id_map`; columnas nuevas de `warehouse_storages` (§F).
- **Efectos secundarios:** ninguno fuera de los lotes.
- **Pruebas** (`Wms.Tests/Administration/LegacyCsvReaderTests.cs`, nuevo):
  - UTF-8 con BOM → la primera celda sin el BOM.
  - Bytes `latin1` de «NARIÑO» → «NARIÑO».
  - `"a;""b"";c"` → tres campos con `"b"` en el segundo.
  - Tabulador detectado.
  - `headerRows=2`.
  - Línea vacía ignorada.
  - `"1.234,5"` con `;` → 1234.5.
  - `"2026-01-31 23:30:00"` → `2026-01-31T23:30:00-05:00`.
- **Terminado cuando:** un CSV de prueba pasa por simulación y firme, y deja su lote y sus correspondencias.
- **Riesgo:** caracteres mal codificados. Se mitiga con la detección de codificación y la simulación obligatoria antes de cada carga en firme.

---

#### F6-02 · Maestros desde el legacy (GAP-001, GAP-023, GAP-025, GAP-026, P13)

- **Dificultad:** Alta.
- **Regla común:**
  - Una fila legacy con `estado = 'eliminado'` no se exporta.
  - Si ya existe en la v2 un registro equivalente (clave indicada por entidad), no se duplica: se registra la correspondencia y, si aplica, se completan roles o datos vacíos.
  - Los datos que la v2 no guarda (fotos, marca, línea, clase o carrocería de vehículos, representantes con porcentaje) se descartan (GAP-023).
  - Colmotores queda fuera: se excluye el cliente de Colmotores (id 70 en el legacy; el operador confirma el id antes de exportar) y las bodegas con `uso = 'colmotores'`.
- **Por entidad:**

  | Entidad (`{entity}`) | Columnas del CSV, en orden | Destino y reglas | Clave de equivalencia |
  |---|---|---|---|
  | `PackagingTypes` | `id_embalaje;nom_embalaje` | `PackagingType.Create(code = "LEG" + id, name)` | nombre normalizado (`CatalogNameNormalizer`) |
  | `Crews` | `id_cuadrilla;nom_cuadrilla` | `Crew` con `LegacyId` (F4-10) | `LegacyId`, luego nombre normalizado |
  | `Locations` | `id_seccion;nombre;fila;columna;nom_bodega` | `WarehouseLocation.Create(code = "{nom_bodega}-{nombre}"` truncado al largo de la columna, `name = nombre`, `capacity = 0`, `aisle = nom_bodega`, `rack = fila`, `level = columna)` | código |
  | `Customers` | `id_cliente;nom_tipodocumento;nro_documento;digitoverificacion;id_paisdocumento;nom_cliente;dias_facturacion;uap;es_exportador` | `Stakeholder` con roles CUSTOMER e IMPORTER (y EXPORTER si `es_exportador = 1`); `IsUap = (uap = 1)` (F5-06); configuración de facturación con `BillingCycle` por días: 15→`Days15`, 30→`Days30`, 90→`Days90`, 180→`Days180`, 360→`Days360`, otro valor → error de fila (F3-05); plazo de pago 30 | tipo y número de documento normalizados (sin puntos, guiones ni espacios; sin el dígito de verificación) |
  | `CustomsAgencies` | `id_sia;nom_tipodocumento;nro_documento;digitoverificacion;id_paisdocumento;nombre_sia` | `Stakeholder` con rol CUSTOMS_AGENCY | igual |
  | `TransportCompanies` | `id_empresatransporte;nom_tipodocumento;nro_documento;id_paisdocumento;nom_empresatransporte` | `Stakeholder` con rol TRANSPORT_COMPANY | igual |
  | `Vehicles` | `id_vehiculo;placa_vehiculo;id_paisplaca;id_empresatransporte` | `Vehicle.Create(LicensePlate = PlateNormalizer(placa), CarrierCompanyId` por mapa de transportadoras o nulo, `Country = id_paisplaca`, `VehicleType = null)` | placa normalizada |
  | `Drivers` | `id_persona;nom_tipodocumento;documento_persona;id_paisdocumento;nombres_persona;apellidos_persona;telefono_persona` | `Driver.Create`; apellidos vacíos → «.» | tipo y número de documento |
  | `Products` | `id_producto;aliasproducto;descripcionproducto;id_embalaje` | `Product`: nombre = primeros 150 caracteres de la descripción; descripción completa (hasta 1000); SKU = alias en mayúsculas si existe y está libre, si no `LEG-{id_producto}`; unidad `UnitMeasureIds.Unidad`; embalaje por mapa | SKU, luego nombre normalizado |

- **Tipo de documento legacy** (por nombre normalizado):

  | Nombre legacy | `IdentificationType` |
  |---|---|
  | NIT | `Nit` |
  | RUT | `Rut` |
  | CEDULA, CEDULA DE CIUDADANIA, CC | `Cc` |
  | PASAPORTE | `Pasaporte` |
  | RUC | `Ruc` |

  - También se acepta el nombre del enum.
  - Otro valor → error de fila "Fila {n}: el tipo de documento «{x}» no tiene equivalente en la v2."
- **Consultas de exportación** (MySQL del legacy; se entregan en el plan y el operador las ejecuta con salida CSV `;` en UTF-8):

  ```sql
  -- Clientes (excluye Colmotores: confirme el id)
  SELECT C.id_cliente, TD.nom_tipodocumento, C.nro_documento, C.digitoverificacion, C.id_paisdocumento,
         C.nom_cliente, C.dias_facturacion, C.uap,
         IF(EXISTS(SELECT 1 FROM ingreso I WHERE I.id_exportador = C.id_cliente AND I.estado <> 'eliminado'), 1, 0) AS es_exportador
  FROM cliente C JOIN tipodocumento TD ON TD.id_tipodocumento = C.id_tipodocumento
  WHERE C.estado <> 'eliminado' AND C.id_cliente NOT IN (0, 70);

  -- Agencias de aduana
  SELECT S.id_sia, TD.nom_tipodocumento, S.nro_documento, S.digitoverificacion, S.id_paisdocumento, S.nombre_sia
  FROM sia S JOIN tipodocumento TD ON TD.id_tipodocumento = S.id_tipodocumento WHERE S.estado <> 'eliminado';

  -- Transportadoras
  SELECT E.id_empresatransporte, TD.nom_tipodocumento, E.nro_documento, E.id_paisdocumento, E.nom_empresatransporte
  FROM empresa_transporte E JOIN tipodocumento TD ON TD.id_tipodocumento = E.id_tipodocumento WHERE E.estado <> 'eliminado';

  -- Vehículos, con la transportadora más reciente
  SELECT V.id_vehiculo, V.placa_vehiculo, V.id_paisplaca,
         (SELECT VE.id_empresatransporte FROM vehiculo_x_empresa VE WHERE VE.id_vehiculo = V.id_vehiculo
          ORDER BY VE.fechahora_registra DESC LIMIT 1) AS id_empresatransporte
  FROM vehiculo V WHERE V.estado <> 'eliminado';

  -- Conductores: solo personas que conducen en algún pesaje
  SELECT P.id_persona, TD.nom_tipodocumento, P.documento_persona, P.id_paisdocumento,
         P.nombres_persona, P.apellidos_persona, P.telefono_persona
  FROM persona P JOIN tipodocumento TD ON TD.id_tipodocumento = P.id_tipodocumento
  WHERE P.estado <> 'eliminado' AND P.id_persona IN (SELECT id_conductor FROM pesaje);

  -- Embalajes, productos, cuadrillas y ubicaciones
  SELECT id_embalaje, nom_embalaje FROM embalaje WHERE estado <> 'eliminado';
  SELECT id_producto, aliasproducto, descripcionproducto, id_embalaje FROM producto WHERE estado <> 'eliminado';
  SELECT id_cuadrilla, nom_cuadrilla FROM cuadrilla WHERE estado <> 'eliminado';
  -- Ubicaciones (DEF-MIG-008): una fila por sección activa y una por bodega activa sin secciones
  -- (id_seccion vacío; entra con id legacy B{id_bodega}). ocupacion = 'deshabilitado' entra No disponible.
  SELECT S.id_seccion, S.nombre, S.fila, S.columna, B.nom_bodega, S.ocupacion, B.id_bodega
  FROM bodega B
  LEFT JOIN seccion S ON S.id_bodega = B.id_bodega AND S.estado <> 'eliminado'
  WHERE B.estado <> 'eliminado' AND B.uso <> 'colmotores'
  ORDER BY B.id_bodega, S.id_seccion;
  ```

- **Mensajes de fila** (con prefijo "Fila {n}: "): documento vacío; placa vacía; nombre vacío; transportadora o embalaje sin correspondencia ("no existe la transportadora legacy {id}; impórtela primero."); ciclo de facturación no soportado ("los días de facturación {d} no tienen ciclo equivalente.").
- **Evidencia:**
  - Legacy `bodegas_schema.sql`: `cliente` :174-200, `sia` :1475-1497, `empresa_transporte` :402-424, `vehiculo` :1709-1733, `persona` :885-910, `producto` :1010-1021, `embalaje` :383-392, `bodega` :81-95, `seccion` :1399-1411, `cuadrilla` :247-255, `tipodocumento` :1590-1598, `vehiculo_x_empresa` :1765-1777.
  - v2: `Stakeholder.cs:309` (`StakeholderManageParams`), `Vehicle.cs:61-65`, `Driver.cs:71-77`, `PackagingType.cs:21`, `WarehouseLocation.cs:28-34`, `ProductConfiguration.cs:14-30` (SKU único de 40, nombre de 150).
- **Archivos:**
  - `Wms.Application/Administration/LegacyImport/Importers/{PackagingTypes,Crews,Locations,Customers,CustomsAgencies,TransportCompanies,Vehicles,Drivers,Products}Importer.cs` (nuevos; cada uno implementa `ILegacyEntityImporter` con su parser puro de fila).
  - `Wms.Application/Administration/LegacyImport/Common/LegacyDocumentTypeMapper.cs` y `LegacyBillingCycleMapper.cs` (nuevos, puros).
- **Contrato:** C-F6-01 (mismo endpoint, un `{entity}` por fila de la tabla).
- **Esquema:** ninguno adicional.
- **Efectos secundarios:** altas en maestros, auditadas por `IAuditable`, y correspondencias.
- **Pruebas:**
  - `Wms.Tests/Administration/LegacyDocumentTypeMapperTests.cs` (nuevo): «Cédula de ciudadanía» → `Cc`; «NIT» → `Nit`; «Cédula de extranjería» → error.
  - `LegacyBillingCycleMapperTests` (nuevo): 15 → `Days15`; 360 → `Days360`; 45 → error.
  - Un parser de fila por entidad (nuevo, en `Wms.Tests/Administration/LegacyImport/`), con una fila válida y una inválida cada uno.
  - Normalización de documento: `"900.123.456-7"` → `"900123456"`.
- **Terminado cuando:** los nueve CSV se importan sin duplicar terceros ni vehículos que ya existían.
- **Riesgo:** terceros duplicados con documentos escritos distinto. Se mitiga con la normalización y la revisión del reporte de simulación.

---

#### F6-03 · Depósitos vivos y sus levantes (GAP-001, RN-035, P13)

- **Dificultad:** Muy alta.
- **Regla:**
  1. **CSV de depósitos** (`{entity} = Deposits`): una fila por producto de depósito con saldo > 0. Columnas:

     ```
     nro_deposito; fecha_deposito; modalidad; id_cliente; id_importador; id_exportador; id_sia;
     nro_doccomercial; fecha_doccomercial; nro_manifiestodian; fecha_manifiestodian;
     id_producto; id_embalaje; ingresan; nacionalizados; salen; saldo;
     ultimo_fin_facturado; trm_ingreso; valor_mercancia; moneda; prorroga
     ```

     - Las tres últimas columnas, `valor_mercancia`, `moneda` y `prorroga`, son **opcionales**: un CSV con las 19 columnas anteriores se sigue aceptando y el depósito queda sin CIF y sin prórroga (DEF-MIG-004, BR-08-003).
     - **Identidad del depósito (BR-08-005).** El legacy reinicia la serie cada año: el depósito es el par (`nro_deposito`, año de `fecha_deposito` en hora de Colombia). Las filas se agrupan por ese par y los mensajes lo muestran como «BA0042 (2023)». Se guarda en `WarehouseStorage.LegacyYear`; los migrados antes de esa columna quedan con el año nulo y se reconocen por el año de su fecha de ingreso.
     - **Prórroga (BR-08-003).** `prorroga` (columna 22) vale `1` o `0`, vacía = `0`; cualquier otro valor → "Fila {n}: La prórroga (prorroga) «x» debe ser 1 o 0." Con `1` en un depósito de importación se registra la prórroga (`RegisterExtension`, nota «Prórroga registrada en el legacy (depósito {clave}); migrada.»): plazo de 60 días y una segunda prórroga responde 409. En otra modalidad se ignora con la advertencia "Fila {n}: advertencia: la prórroga solo aplica a importación; se ignora en el depósito {clave}." Es parte de los datos de cabecera: todas las filas del depósito deben coincidir.
     - `modalidad` acepta, sin distinguir mayúsculas ni tildes (DEF-MIG-001):
       - el código v2: `IMP`, `EXP` o `INSP`;
       - el nombre de `modalidad.nom_modalidad` del legacy: «Entrada por Importación» → `IMP` y «Entrada por Exportación» → `EXP`. El legacy no tiene modalidad de inspección; «Entrada por Otros», las «Salida por …» y «Solo servicio de pesaje» no crean depósito;
       - el nombre de la `OperationModality` de la v2.

       Sin equivalencia → "Fila {n}: la modalidad «{x}» no tiene equivalente en la v2. Use IMP, EXP o INSP."
     - **Valor de la mercancía (CIF) y moneda** (DEF-MIG-004). Son del depósito, no del producto:
       - Los dos vacíos → depósito sin CIF.
       - `valor_mercancia` con valor y `moneda` vacía → "Fila {n}: la columna moneda está vacía y valor_mercancia trae valor."
       - `valor_mercancia` mayor que cero y con máximo 2 decimales, como el registro en báscula.
       - `moneda`: `COP`, `USD` o el código de país del legacy (`ingreso.id_paismonedaprecio`): `ECU` → USD y `COL` → COP. En el dump del 2024-06-10, los 128 depósitos vivos traen `ECU`. No se usa `pais.iso_moneda`, que para `ECU` guarda «USA». Otro valor → "Fila {n}: la moneda «{x}» (columna moneda) no se reconoce. Use COP, USD o el código de país del legacy (ECU o COL)."
       - En un depósito de varias filas, todas deben traer el mismo valor y la misma moneda. Si no, el depósito no se migra y la fila distinta dice "el valor de la mercancía (valor_mercancia) y la moneda deben ser iguales en todas las filas del depósito {nro}…".
     - Validaciones: `saldo = ingresan − salen` (si no → "Fila {n}: el saldo no cuadra con ingresan − salen."), `saldo > 0`, `nacionalizados ≤ ingresan`, y todas las referencias en el mapa (cliente, producto, etc.).
  2. **Creación**, agrupando las filas por `nro_deposito` en una transacción:
     - **Servicio.** `ServiceRecord.CreateMigrated(...)` (nuevo): ingreso, modalidad, documento (`nro_doccomercial` y su fecha), cliente, estado `Completed` e ingreso de camiones cerrado.
       - Terceros CUSTOMER, IMPORTER, EXPORTER y CUSTOMS_AGENCY según las columnas.
       - Un camión nuevo con esa carta porte recibe el 409 de «documento cerrado» de F1-02.
     - **Depósito.** `WarehouseStorage.CreateMigrated(...)` (nuevo):
       - `Confirmed`, `IsMigrated = true`, `LegacyNumber = nro_deposito`;
       - número v2 tomado de la secuencia actual (se conserva la numeración de la v2), `EntryDate = fecha_deposito`, `Trm = trm_ingreso`;
       - `CargoValue = valor_mercancia` y `Currency = moneda` (DEF-MIG-004). Con moneda distinta de COP y sin `trm_ingreso`, el depósito queda con la TRM pendiente (WMS-24): `open-billing` la consulta a la DIAN y, si no llega, Facturación registra la TRM manual antes de numerar la factura. COP no requiere TRM;
       - `BillingStartDate = ultimo_fin_facturado + 1 día`, o `fecha_deposito` si no hay período facturado;
       - `CargoHandling = LooseGoods`.
       - En importación también `ImportWarehouseStorage` con manifiesto y fecha.
     - **Productos.** `WarehouseStorageProduct.CreateMigrated(productId, packagingTypeId, unitMeasureId, received = ingresan, current = saldo)` (nuevo): `DeclaredQuantity = ingresan`, sin camiones (`EntryProducts` vacío).
     - **Movimientos**, con `SourceType = MigrationOpening` (valor nuevo) y `SourceId` = el depósito: uno `In` por `ingresan` («Ingreso legacy {nro}») y uno `Out` por `salen` si es > 0 («Despachado en el legacy»). El kardex cuadra.
     - Correspondencia `Deposits` → `{nro_deposito}@{año}`. Un depósito ya migrado se omite: "Fila {n}: el depósito {nro} ({año}) ya fue migrado." Es «ya migrado» el de la misma clave, el de `LegacyYear` nulo con el mismo número y año de ingreso, o el de una correspondencia anterior por número solo cuando su depósito es de ese año.
  3. **Protección de los migrados**, que no tienen camiones:
     - `ReturnStorageForCorrection` → 409 "El depósito {n} viene del legacy: corrija sus cantidades con un ajuste de inventario."
     - La anulación de pesajes no aplica (no tienen ciclos).
     - La anulación del depósito (F3-08) sí aplica.
  4. **CSV de levantes** (`{entity} = Releases`): una fila por `producto_levante` de los depósitos migrados, tal como está en el legacy. Columnas:

     ```
     nro_deposito; id_producto; id_embalaje; nro_levante; fecha_levante; nro_aceptacion; fecha_aceptacion;
     cantidad_levante; peso_bruto; fob_dolares; tasa_cambio; fob_pesos; anio_deposito
     ```

     - **`anio_deposito` (BR-08-005), columna 13 opcional:** el año de `fecha_deposito` del depósito del levante. Sin ella, el número debe identificar a un solo depósito migrado; si existe en varios años → "Fila {n}: el depósito {nro} existe en varios años; exporte la columna anio_deposito." Con ella, el levante va al depósito de ese número y año. El año es parte de la agrupación.
     - **Agrupación (DEF-MIG-003).** El legacy reparte un levante en una fila de `producto_levante` por cada `producto_en_bodega` (cada camión del depósito). Antes de crear, el importador agrupa las filas del archivo por (depósito, producto, embalaje, número de levante, número de aceptación):
       - suma `cantidad_levante`;
       - el peso bruto, el FOB en dólares y en pesos, la tasa y las fechas son de la tabla `levante`: cada fila los repite completos, así que se toman de la primera fila del grupo y no se suman (decisión del usuario del 2026-10-06);
       - si difieren entre filas del grupo, se conserva la primera y el lote lleva una advertencia "Fila {n}: advertencia: el levante {x} del producto {p} trae fechas, tasa, peso o FOB distintos…", que no rechaza la fila.
     - Crea un `ImportRelease` por grupo; FOB con la tasa del legacy, `ExchangeRateSource = Manual` y `ExchangeRateDate = fecha_levante` (F2-05). El reparto del FOB entre productos (abajo) se aplica después de agrupar.
     - Sin aplicar los topes de F2-01: ya se validaron en el legacy.
     - Al final, `ImportWarehouseStorage.RecalculateTotals` (F2-01) por depósito.
     - El lote informa las filas leídas (`totalRows`), los levantes creados ya agrupados (`created`) y los omitidos (`skipped`).
     - Validaciones (un error del grupo se informa en cada una de sus filas):
       - Σ levantes del producto, con la cantidad agrupada, > `ingresan` → "Fila {n}: los levantes superan lo ingresado del producto."
       - Depósito no migrado → "Fila {n}: el depósito {nro} no está migrado."
       - Levante que ya existía en la base antes de este archivo (mismo número, aceptación y producto) → se omite. Así una segunda carga del mismo archivo no duplica.
  5. **Consultas de exportación** (MySQL). No usan `vista_kardexproductoenbodega`, que tiene la errata `'elimininado'` y no excluye lo eliminado (RISK-006):

     **Depósitos.** Corregida tras la fase 1 de la migración (2026-10-06), sobre la consulta congelada `db_legacy/trabajo/consultas/11_depositos.sql`:
     - `modalidad` sale como el código de la v2 con un `CASE` por `id_modalidad` (DEF-MIG-001);
     - `saldo` y `trm_ingreso` salen calculados;
     - se agregan `valor_mercancia` (`ingreso.preciomercancia`) y `moneda` (`ingreso.id_paismonedaprecio`), solo cuando el valor es mayor que cero (DEF-MIG-004);
     - se agrega `prorroga` (`deposito.prorroga`, 0 o 1), la columna 22 del CSV (BR-08-003). Los depósitos de exportación e inspección la traen en 0 o se ignora con advertencia.

     Con el dump del 2024-06-10 da 133 filas (128 depósitos), con las mismas 19 primeras columnas que el CSV congelado de la fase 1.

     ```sql
     SELECT X.nro_deposito, X.fecha_deposito,
            CASE X.id_modalidad WHEN 1 THEN 'IMP' WHEN 2 THEN 'EXP' ELSE X.modalidad END AS modalidad,
            X.id_cliente, X.id_importador, X.id_exportador, X.id_sia, X.nro_doccomercial, X.fecha_doccomercial,
            X.nro_manifiestodian, X.fecha_manifiestodian, X.id_producto, X.id_embalaje,
            X.ingresan, X.nacionalizados, X.salen, X.ingresan - X.salen AS saldo, X.ultimo_fin_facturado,
            (SELECT T.valor FROM tasa_cambio T WHERE T.fecha_inicio <= DATE(X.fecha_ingreso) AND T.fecha_fin >= DATE(X.fecha_ingreso)
               AND T.estado <> 'eliminado' AND T.valor > 0 ORDER BY (T.id_pais = 'ECU') DESC, T.id_tasacambio DESC LIMIT 1) AS trm_ingreso,
            X.valor_mercancia, X.moneda, X.prorroga
     FROM (
       SELECT D.id_deposito, I.id_modalidad, M.nom_modalidad AS modalidad, D.nro_deposito, D.fecha_deposito,
              I.fechahora_ingreso AS fecha_ingreso, I.id_importador AS id_cliente, I.id_importador, I.id_exportador, I.id_sia,
              I.nro_doccomercial, I.fecha_doccomercial, I.nro_manifiestodian, I.fecha_manifiestodian,
              PB.id_producto, PB.id_embalaje,
              SUM(PB.cantidad) AS ingresan,
              IFNULL((SELECT SUM(PL.cantidad_levante) FROM producto_levante PL JOIN producto_en_bodega PB2 ON PB2.id_productoenbodega = PL.id_productoenbodega
                      WHERE PB2.id_deposito = D.id_deposito AND PB2.id_producto = PB.id_producto AND PB2.id_embalaje = PB.id_embalaje
                      AND PL.estado <> 'eliminado' AND PB2.estado <> 'eliminado'), 0) AS nacionalizados,
              IFNULL((SELECT SUM(PS.cantidad_salida) FROM producto_salida PS JOIN producto_en_bodega PB3 ON PB3.id_productoenbodega = PS.id_productoenbodega
                      WHERE PB3.id_deposito = D.id_deposito AND PB3.id_producto = PB.id_producto AND PB3.id_embalaje = PB.id_embalaje
                      AND PS.estado <> 'eliminado' AND PB3.estado <> 'eliminado'), 0) AS salen,
              (SELECT MAX(F.fechafin_periodo) FROM facturaciigo F WHERE F.id_deposito = D.id_deposito AND F.estado = 'facturada') AS ultimo_fin_facturado,
              CASE WHEN I.preciomercancia > 0 THEN CAST(I.preciomercancia AS DECIMAL(18,2)) END AS valor_mercancia,
              CASE WHEN I.preciomercancia > 0 THEN I.id_paismonedaprecio END AS moneda,
              D.prorroga
       FROM deposito D JOIN ingreso I ON I.id_ingreso = D.id_ingreso JOIN modalidad M ON M.id_modalidad = I.id_modalidad
       JOIN producto_en_bodega PB ON PB.id_deposito = D.id_deposito AND PB.estado <> 'eliminado'
       WHERE D.estado <> 'eliminado' AND I.estado <> 'eliminado' AND I.id_importador <> 70
       GROUP BY D.id_deposito, PB.id_producto, PB.id_embalaje
       HAVING ingresan - salen > 0
     ) X
     ORDER BY X.nro_deposito, X.id_producto, X.id_embalaje, X.id_deposito;
     ```

     - **Orden total (O-1):** `X.id_deposito` desempata dos depósitos vivos con el mismo número de años distintos, para que una reexportación traiga las filas en el mismo orden y el mismo hash. Desde BR-08-005 esos depósitos se migran como depósitos distintos, por (número, año de `fecha_deposito`).
     - `trm_ingreso` es la `tasa_cambio` vigente en la fecha de ingreso, como `kardex.php:227`: solo registros no eliminados y con valor > 0; si hay varias, primero la de `ECU` y luego la más reciente.
     - El legacy factura al importador (`cron.php:21`): por eso `id_cliente = id_importador`.
     - El ajuste de prueba D2 del plan de migración (`ultimo_fin_facturado = 2026-09-30`) se aplica después, sobre el CSV.

     **Levantes.** Corregida (DEF-MIG-002), sobre `db_legacy/trabajo/consultas/12_levantes.sql` sin su agrupación:
     - filtra por `id_deposito` de los depósitos vivos, con la misma condición que la consulta de depósitos;
     - no agrupa: exporta una fila por `producto_levante`, tal como está en el legacy, y el importador agrupa (DEF-MIG-003).

     Con el dump del 2024-06-10 da 170 filas, que el importador agrupa en 118 levantes.

     ```sql
     SELECT D.nro_deposito, PB.id_producto, PB.id_embalaje, L.nro_levante, L.fecha_levante, L.nro_aceptacion,
            L.fecha_aceptacion, PL.cantidad_levante, L.peso_bruto, L.fob_dolares, L.tasa_cambio, L.fob_pesos,
            YEAR(D.fecha_deposito) AS anio_deposito
     FROM producto_levante PL JOIN levante L ON L.id_levante = PL.id_levante
     JOIN producto_en_bodega PB ON PB.id_productoenbodega = PL.id_productoenbodega
     JOIN deposito D ON D.id_deposito = PB.id_deposito
     WHERE PL.estado <> 'eliminado' AND L.estado <> 'eliminado' AND PB.estado <> 'eliminado'
       AND D.id_deposito IN (
         SELECT V.id_deposito FROM (
           SELECT D2.id_deposito
           FROM deposito D2 JOIN ingreso I ON I.id_ingreso = D2.id_ingreso
           JOIN producto_en_bodega PB2 ON PB2.id_deposito = D2.id_deposito AND PB2.estado <> 'eliminado'
           WHERE D2.estado <> 'eliminado' AND I.estado <> 'eliminado' AND I.id_importador <> 70
           GROUP BY D2.id_deposito, PB2.id_producto, PB2.id_embalaje
           HAVING SUM(PB2.cantidad) - IFNULL((SELECT SUM(PS.cantidad_salida) FROM producto_salida PS
                    JOIN producto_en_bodega PB3 ON PB3.id_productoenbodega = PS.id_productoenbodega
                    WHERE PB3.id_deposito = D2.id_deposito AND PB3.id_producto = PB2.id_producto AND PB3.id_embalaje = PB2.id_embalaje
                      AND PS.estado <> 'eliminado' AND PB3.estado <> 'eliminado'), 0) > 0
         ) V
       )
     ORDER BY D.nro_deposito, L.nro_levante, L.nro_aceptacion, PB.id_producto, PL.id_productolevante;
     ```

     - **Orden total (O-1):** `PL.id_productolevante`, la clave de `producto_levante`, desempata las filas que coinciden en lo demás, para que una reexportación traiga el mismo orden y el mismo hash. `anio_deposito` (BR-08-005) separa los levantes de dos depósitos que repiten número; la consulta no cambia su orden.
     - **No se filtra por `nro_deposito`:** el legacy reinicia la serie cada año (`BA0001` existe en varios años; 9.682 depósitos con 4.755 números). Por número, la consulta traía 819 filas en vez de 170 y cargaba levantes de depósitos cerrados en el depósito vivo con el mismo número (DEF-MIG-002).
     - El FOB del legacy está en el levante y no por producto. Si un levante tiene varios productos, el FOB se asigna completo a la primera fila del levante y 0 a las demás, para no multiplicarlo en las pólizas (F5-06). El importador aplica esta regla por par número–aceptación.
- **Evidencia:**
  - Legacy:
    - `bodegas_schema.sql:2431` (errata en `vista_kardexproductoenbodega`);
    - `cron.php:3-9` (solo ingresos activos; excluye el importador 70);
    - `cron.php:59` (último período facturado);
    - `modulos/mod_inventario/kardex.php:227` (TRM de ingreso).
  - v2: `WarehouseStorageProduct.cs:45-70,107-125` (el recibido se recalcula desde los camiones: de ahí la protección del punto 3); `DepositProductEditing.cs:28-32`.
- **Archivos:**
  - `ServiceRecord.cs`, `WarehouseStorage.cs`, `WarehouseStorageProduct.cs` e `ImportRelease.cs` (modifica: factorías `CreateMigrated`).
  - `SourceTypeMovements.cs` (modifica: `MigrationOpening`).
  - `Wms.Application/Administration/LegacyImport/Importers/{Deposits,Releases}Importer.cs` (nuevos).
  - `Wms.Application/ForeignTrade/Commands/ReturnStorageForCorrection/ReturnStorageForCorrectionHandler.cs` (modifica: guarda de migrados).
- **Contrato:** C-F6-01 (entidades `Deposits` y `Releases`).
- **Esquema:** las columnas de F6-01; ninguna adicional.
- **Efectos secundarios:** depósitos confirmados sin períodos (los abre F6-04), movimientos de apertura y levantes.
- **Pruebas:**
  - `Wms.Tests/Administration/LegacyImport/DepositRowParserTests.cs` (nuevo):
    - Saldo que no cuadra → error.
    - Saldo 0 → error.
    - Nacionalizados > ingresan → error.
    - Modalidad «IMPORTACION» → `IMP` si coincide con el nombre de la modalidad.
  - `LegacyReleaseFobSplitterTests` (nuevo): levante de 1000 USD con dos productos → 1000 y 0.
  - Correcciones de la fase 1 de la migración (2026-10-06):
    - `DepositRowCargoAndModalityTests`: nombres de modalidad del legacy, CSV de 19 y de 21 columnas, valor sin moneda, moneda desconocida, valores distintos entre filas (DEF-MIG-001 y 004);
    - `LegacyReleaseGrouperTests`: agrupación de las filas del mismo levante (DEF-MIG-003);
    - integración `LegacyReleasesImportTests` y `MigratedStorageBillingTests` (DEF-MIG-003 y 004), y `MigratedGuideBalanceTests` para la guía de los migrados (DEF-MIG-005).
  - `WarehouseStorageProductTests` (modifica): `CreateMigrated(received 10, current 4)` → disponible 4, despachado 6; `current > received` → error.
- **Terminado cuando:** los depósitos vivos aparecen confirmados con su saldo y sus levantes, y el kardex (F5-04) cuadra con el legacy.
- **Riesgo:** saldos distintos por registros eliminados mal marcados. Se mitiga con la conciliación (F6-04) antes de abrir la facturación.

---

#### F6-04 · Conciliación y apertura de la facturación de los migrados (GAP-001, RN-035, RN-050)

- **Dificultad:** Alta.
- **Regla:**
  1. **Conciliación** `POST administration/legacy-import/reconciliation` (multipart: el mismo CSV de depósitos, exportado de nuevo el día del corte):
     - Por fila compara `saldo` con `CurrentStock` y `nacionalizados` con Σ levantes del producto migrado.
     - Informa también lo que cambió en la v2 desde la migración (movimientos distintos de `MigrationOpening`), para no confundir operación nueva con descuadre.
     - **Respuesta:** `rows: [{ legacyNumber, v2Number, productName, legacyBalance, v2Stock, legacyNationalized, v2Nationalized, v2MovementsSinceMigration, status }]`, con `status` `Ok`, `Difference` o `NotMigrated`; y un resumen.
     - No escribe nada.
  2. **Apertura de la facturación** `POST administration/legacy-import/open-billing` (con `warehouseStorageIds` opcional; si no viene, todos los migrados sin períodos):
     - Por depósito migrado sin períodos: `StorageBillingService.OpenPeriodWithInvoiceAsync(storageId, customerId, new StoragePeriodOpenOptions(true, inicio))`, con `inicio = BillingStartDate` en Colombia (F3-06). Si `BillingStartDate` es futura, se omite: "El depósito {n} empieza a facturar el {fecha}."
     - Si la apertura deja períodos vencidos, el job de F3-06 los renueva en sus pasadas siguientes.
     - Requiere las tarifas configuradas. Si falla la resolución de cargos, el depósito se reporta con el error y los demás siguen: un depósito por transacción, como el job.
     - **Respuesta:** `[{ warehouseStorageId, number, status: Opened | Skipped | Failed, message }]`.
  3. `AdminOnly`.
- **Evidencia:**
  - Legacy `cron.php:58-97`: continúa desde el último período facturado.
  - v2 `BillingJobService.cs:208-276`: un depósito por transacción, con aviso a Facturación si falla.
- **Archivos:**
  - `Wms.Application/Administration/LegacyImport/Commands/{ReconcileDeposits,OpenMigratedBilling}/*` (nuevos).
  - `Wms.Application/Administration/LegacyImport/Common/DepositReconciler.cs` (nuevo, puro).
  - `LegacyImportController.cs` (modifica).
- **Contrato:** C-F6-03 y C-F6-04.
- **Esquema:** ninguno.
- **Efectos secundarios:** la apertura crea períodos y facturas en Borrador, con los avisos de facturación actuales.
- **Pruebas** (`Wms.Tests/Administration/LegacyImport/DepositReconcilerTests.cs`, nuevo):
  - Legacy 10, v2 10 → `Ok`.
  - Legacy 10, v2 8 con un `Out` de 2 posterior → `Ok` e informa el movimiento.
  - Legacy 10, v2 8 sin movimientos → `Difference`.
  - Número no migrado → `NotMigrated`.
- **Terminado cuando:** la conciliación da `Ok` en todas las filas y la facturación queda abierta y contigua para los migrados.
- **Riesgo:** abrir la facturación sin tarifas o con tarifas erradas. Se mitiga: es un paso explícito, con resultado por depósito, que se ejecuta después de configurar las tarifas.

---

#### F6-05 · Respaldo diario con destinos configurables (GAP-021, LEGACY-FUNC-004, P14)

- **Dificultad:** Alta.
- **Regla:**
  1. **Destinos** (`backup_destinations`, `IAuditable`; administración solo Admin):
     - Campos: `Name` (único), `Type` (`Local` o `S3`), `LocalPath` (Local), `Bucket`, `Prefix`, `Region` y `ServiceUrl` (S3; `ServiceUrl` para servicios compatibles), `IsActive`.
     - **Las credenciales nunca se guardan en la base.** Se leen de la configuración `Backups:S3Credentials:{Name}:AccessKeyId` y `:SecretAccessKey` (variables de entorno en el servidor) o, si no están, de la cadena de credenciales por defecto de AWS (rol de la instancia).
     - Validaciones:
       - Local sin ruta → "Indique la carpeta del respaldo."
       - S3 sin bucket → "Indique el bucket del respaldo."
       - Nombre duplicado → 409 "Ya existe el destino {nombre}."
     - `POST administration/backup-destinations/{id}/test` escribe y borra un archivo de prueba y devuelve el resultado.
  2. **Ejecución** (`BackupService.RunAsync(kind, triggeredById)`):
     1. `pg_dump --format=custom` de la base, con la cadena de conexión de la configuración, a una carpeta temporal.
     2. Si `Storage:Type = Local`, un `tar.gz` de `Storage:Local:BasePath` (los archivos subidos).
     3. Copia ambos a **cada destino activo**:
        - Local: `{LocalPath}/{yyyy}/{MM}/wms_{yyyyMMdd_HHmm}.dump` y `uploads_{yyyyMMdd_HHmm}.tar.gz`;
        - S3: `{Prefix}/{yyyy}/{MM}/…`.
     4. Registra el resultado en `backup_runs`: `StartedAt`, `FinishedAt`, `Kind` (`Daily`, `Monthly` o `Manual`), `Status` (`Running` mientras corre; luego `Succeeded`, `PartiallySucceeded` o `Failed`), `SizeBytes`, `Results` (jsonb por destino: `destinationId`, `status`, `location` y `error`), `TriggeredById`.
     5. Borra los temporales.
  3. **Programación:**
     - `DatabaseBackupBackgroundService` corre a diario a la hora `Backups:DailyTime` (por defecto 02:00 de Colombia).
     - Idempotente por día: no corre si ya hay un `Daily` o `Monthly` exitoso del día.
     - La primera corrida del mes es `Monthly`.
  4. **Retención** (P14, «diario 30 + 12»): después de cada corrida, por destino, se conservan los 30 respaldos diarios más recientes y los 12 mensuales más recientes; se borran los demás. Los manuales no cuentan ni se borran.
  5. **Fallo:** notificación al rol `Admin`, nivel Error, título "Falló el respaldo", mensaje "El respaldo del {fecha} falló en {destinos}: {error}."
  6. **Endpoints** (`AdminOnly`):
     - CRUD `administration/backup-destinations`;
     - `POST administration/backups/run` (manual; responde 202 con el id de la corrida y la ejecuta en segundo plano; si hay una en curso → 409 "Ya hay un respaldo en curso.");
     - `GET administration/backups/runs` (paginado).
  7. **Infraestructura:**
     - `deploy/staging/Dockerfile.staging` instala `postgresql-client-18`, la misma versión que la imagen `postgres:18.0` de `compose.staging.yaml`.
     - Paquete NuGet `AWSSDK.S3` en `Wms.Infrastructure`.
     - `deploy/staging/README.md` documenta la restauración (`pg_restore --clean --if-exists -d …`) y reemplaza el cron opcional actual.
- **Evidencia:**
  - Legacy: LEGACY-FUNC-004 (respaldo del legacy).
  - v2:
    - `deploy/staging/README.md:155-158` (cron opcional con `pg_dump`, fuera de la aplicación);
    - `deploy/staging/Dockerfile.staging` (imagen `aspnet:10.0` sin cliente de PostgreSQL);
    - `Wms.Infrastructure/Services/StorageService.cs:25-32` (`Storage:Type` y `Storage:Local:BasePath`).
- **Archivos:**
  - `Wms.Domain/Entities/Administration/{BackupDestination,BackupRun}.cs` y sus enums (nuevos).
  - Configuraciones nuevas y `AppDbContext.cs`.
  - `Wms.Infrastructure/Services/Backups/{IBackupService,BackupService,IBackupTarget,LocalBackupTarget,S3BackupTarget,PgDumpRunner}.cs` (nuevos).
  - `Wms.Application/Administration/Backups/{Commands,Queries}/*` (nuevos).
  - `Wms.Application/Administration/Backups/Common/BackupRetentionPolicy.cs` (nuevo, puro).
  - `Wms.Api/BackgroundJobs/DatabaseBackupBackgroundService.cs` (nuevo; se registra en `Program.cs`).
  - `Wms.Api/Controllers/v1/BackupsController.cs` (nuevo; `[Route("administration")]`, `AdminOnly`).
  - `appsettings.json` (modifica: sección `Backups` con `DailyTime`, `TempPath` y `Enabled`).
  - `deploy/staging/Dockerfile.staging` y `deploy/staging/README.md` (modifica).
- **Contrato:** C-F6-05 a C-F6-07.
- **Esquema:** tablas `backup_destinations` y `backup_runs` (§F).
- **Efectos secundarios:** archivos en los destinos; notificaciones de fallo.
- **Pruebas** (`Wms.Tests/Administration/BackupRetentionPolicyTests.cs`, nuevo):
  - 35 diarios → se borran los 5 más viejos.
  - 14 mensuales → se borran 2.
  - Un manual antiguo → se conserva.
  - Un día con un diario exitoso → «no correr».
  - Primer respaldo del mes → `Monthly`.
  - Además, `BackupDestinationTests`: S3 sin bucket → error; Local sin ruta → error.
- **Terminado cuando:** un respaldo manual queda en dos destinos y la retención borra los vencidos en una prueba con fechas simuladas.
- **Riesgo:**
  - Credenciales de S3 expuestas. Se mitiga: solo configuración y entorno, nunca en la base ni en las respuestas.
  - `pg_dump` ausente en la imagen. Se mitiga con el cambio del Dockerfile y el `test` del destino.

---

### C.7 Fase 7 — Comodidad (sin backend)

Los ítems UI-22, UI-23 y UI-24 del roadmap son del frontend:
- UI-22: cobros pendientes visibles para báscula;
- UI-23: renombrar «Stakeholders» a «Terceros» y agregar accesos directos;
- UI-24: atajos de teclado.

UI-22 necesitaría que el rol `Scale` lea facturas pendientes, lo que es un cambio de política (fuera de alcance, ver §G). Esta fase no tiene trabajo de backend.

---

## D. Orden de ejecución y commits

### D.1 Reglas

- Todo en `develop`, un ítem a la vez, en el orden de §D.2 (P17).
- **El implementador no hace commits.** Al terminar cada ítem se detiene y entrega lo que pide §E.2. El usuario hace el commit con el mensaje sugerido de §D.3, cuyo formato es `tipo(ámbito): descripción (identificadores)`.
- Antes de entregar cada ítem: `dotnet build` sin errores y `dotnet test` en verde. Nunca se entrega un ítem a medias.
- Si un ítem necesita un refactor previo (por ejemplo, extraer `DepositProductEditing.AddToEntryAsync` en F4-06), va dentro del mismo ítem.
- El implementador no toca `Wms.Infrastructure/Migrations` ni `Wms.Infrastructure/Persistence/Migrations`. Las migraciones las genera el usuario (§E.3).

### D.2 Pasos con dependencias

| Paso | Ítem | Depende de | Fase |
|---|---|---|---|
| 1 | F1-01 | — | 1 |
| 2 | F1-02 | F1-01 | 1 |
| 3 | F1-03 | F1-01 | 1 |
| 4 | F1-04 | F1-02 | 1 |
| 5 | F1-05 | F1-01, F1-03, F1-04 | 1 |
| 6 | F1-06 | F1-01 | 1 |
| 7 | F1-07 | F1-06 | 1 |
| 8 | F1-08 | F1-05 | 1 |
| 9 | F1-09 | — | 1 |
| 10 | F2-01 | fase 1 completa | 2 |
| 11 | F2-02 | F2-01 | 2 |
| 12 | F2-03 | F2-01 | 2 |
| 13 | F2-04 | F2-01 | 2 |
| 14 | F2-05 | F2-03 | 2 |
| 15 | F2-06 | — | 2 |
| 16 | F2-07 | F2-06 | 2 |
| 17 | F2-08 | — | 2 |
| 18 | F2-09 | F2-08 | 2 |
| 19 | F2-10 | F2-06, F2-08, F2-09 | 2 |
| 20 | F3-01 | fases 1 y 2 completas | 3 |
| 21 | F3-02 | — | 3 |
| 22 | F3-03 | F3-01, F3-02, F2-02 | 3 |
| 23 | F3-04 | — | 3 |
| 24 | F3-05 | — | 3 |
| 25 | F3-06 | F3-05 | 3 |
| 26 | F3-07 | F3-01, F3-02, F3-04, F3-06 | 3 |
| 27 | F3-08 | F3-03, F3-04, F3-07 | 3 |
| 28 | F3-09 | F3-01, F3-04, F3-08, F1-05 | 3 |
| 29 | F3-10 | F3-06 | 3 |
| 30 | F4-01 | fase 3 completa | 4 |
| 31 | F4-02 | F4-01, F3-01, F3-08, F3-09 | 4 |
| 32 | F4-03 | — | 4 |
| 33 | F4-04 | F4-03 | 4 |
| 34 | F4-05 | F1-06 (`CatalogNameNormalizer`) | 4 |
| 35 | F4-06 | F4-05 | 4 |
| 36 | F4-07 | F3-09 | 4 |
| 37 | F4-08 | F4-07 (P16: cubre la «Salida Global») | 4 |
| 38 | F4-09 | — | 4 |
| 39 | F4-10 | — | 4 |
| 40 | F5-01 | fase 4 completa | 5 |
| 41 | F5-02 | F2-01 | 5 |
| 42 | F5-03 | F2-05 | 5 |
| 43 | F5-04 | F2-01, F3-01, F3-04 | 5 |
| 44 | F5-05 | F4-01 | 5 |
| 45 | F5-06 | F2-05 | 5 |
| 46 | F5-07 | — | 5 |
| 47 | F5-08 | F3-06, F3-10 | 5 |
| 48 | F5-09 | F1-09, F3-09 | 5 |
| 49 | F5-10 | F4-03 | 5 |
| 50 | F6-01 | fase 5 completa | 6 |
| 51 | F6-02 | F6-01, F2-06, F3-05, F4-10, F5-06 | 6 |
| 52 | F6-03 | F6-02, F2-01, F2-05 | 6 |
| 53 | F6-04 | F6-03, F3-06 | 6 |
| 54 | F6-05 | — | 6 |

### D.3 Mensajes de commit sugeridos (el usuario hace los commits), en orden

Si un ítem cambia el esquema, el mismo commit incluye su migración (§E.3, nombres en §F.1).

**Fase 1**

1. `feat(bascula): datos de Comercio Exterior opcionales al iniciar el pesaje (BAS-01)`
2. `feat(bascula): identificar el documento sin fecha entre depósitos abiertos (BAS-01, P1)`
3. `feat(bascula): exportador en báscula y en Comercio Exterior (BAS-01)`
4. `feat(comercio-exterior): completar fecha del documento y manifiesto por camión (BAS-01, P2)`
5. `feat(comercio-exterior): requisitos por modalidad al confirmar el depósito (BAS-01, P2, P5)`
6. `feat(bascula): producto por descripción libre con alta en el catálogo (BAS-03, P3)`
7. `feat(comercio-exterior): cambiar el producto de una línea del depósito (BAS-03, P3)`
8. `feat(bascula): unidades de carga sin desglose y reparto en Comercio Exterior (BAS-07, P5)`
9. `feat(bascula): efectivo recibido y cambio en el cobro (BAS-05, GAP-024)`

**Fase 2**

1. `fix(levantes): topes por producto y totales del depósito (RN-028)`
2. `feat(ordenes-cargue): tope de despacho por cantidad nacionalizada (GAP-002, RN-034)`
3. `feat(levantes): rechazar levantes repetidos (GAP-009, RN-026)`
4. `feat(levantes): retirar un levante (GAP-009, RN-030)`
5. `feat(levantes): FOB y tasa de cambio congelados (RN-060)`
6. `feat(ciudades): catálogo de ciudades con días de tránsito e importación (GAP-025)`
7. `feat(guias): destino por catálogo y vencimiento calculado de la guía (GAP-025)`
8. `feat(abandono): registrar la prórroga (GAP-003, RN-024)`
9. `feat(abandono): listado, resumen y alerta diaria (GAP-003, RN-059)`
10. `feat(reportes): candidatos a abandono y salidas en abandono (GAP-003, LEGACY-FUNC-214)`

**Fase 3**

1. `fix(cargue): liberar la reserva no cargada y guardar lo cargado (GAP-006)`
2. `fix(ordenes-cargue): cancelar solo antes del cargue (GAP-006, RN-038)`
3. `feat(ordenes-cargue): modificar ítems antes del cargue (GAP-006, LEGACY-FUNC-158)`
4. `feat(guias): anular la guía de salida (GAP-006, LEGACY-FUNC-159)`
5. `feat(facturacion): ciclos de facturación del legacy (GAP-008, RN-013)`
6. `feat(facturacion): períodos de almacenamiento con fecha límite legacy (RN-050, RN-051)`
7. `feat(ordenes-cargue): revertir la salida después del cargue (GAP-006, RN-038)`
8. `feat(depositos): anular un depósito con sus efectos (GAP-011, RN-018, RN-025)`
9. `feat(bascula): anular un pesaje completo (GAP-005, RN-058)`
10. `feat(facturacion): refacturar almacenamiento anulado (GAP-007, RN-052)`

**Fase 4**

1. `feat(bodega): ubicaciones por cantidad (GAP-014, RN-045)`
2. `feat(bodega): liberar ubicaciones al cargar (GAP-014, RN-048)`
3. `feat(bodega): novedades de mercancía (GAP-015, RN-068)`
4. `feat(bodega): impresión del reporte de mercancías (GAP-015, LEGACY-FUNC-177)`
5. `feat(listas-empaque): proveedores e importación de listas (GAP-013, RN-016)`
6. `feat(listas-empaque): asociar artículos a un camión del depósito (GAP-013, RN-016)`
7. `feat(bascula): pesaje de salida compartido sin cobro (GAP-019, BAS-08)`
8. `feat(salidas): salida con el tiquete de ingreso desde báscula y Comercio Exterior (GAP-019, BAS-09, LEGACY-FUNC-166)`
9. `feat(etiquetas): registrar impresiones y descargas (GAP-024)`
10. `feat(cuadrillas): catálogo y cuadrilla en la guía (GAP-026)`

**Fase 5**

1. `fix(reportes): exportación a Excel con all=true (GAP-017)`
2. `feat(comercio-exterior): columnas de saldo en los listados (UI-17)`
3. `feat(comercio-exterior): búsqueda por placa y levante, listado de levantes (UI-18)`
4. `feat(reportes): kardex con levantes y despachos (GAP-016, LEGACY-FUNC-209)`
5. `feat(reportes): inventario general filtrable (GAP-016, LEGACY-FUNC-211)`
6. `feat(reportes): pólizas por año, mes y UAP (GAP-016, LEGACY-FUNC-215)`
7. `feat(reportes): ingresos por producto y cliente (GAP-016, LEGACY-FUNC-216)`
8. `feat(reportes): facturación anual y por CPI (GAP-016, LEGACY-FUNC-206, LEGACY-FUNC-207)`
9. `feat(reportes): filtros y pesos del reporte de báscula (GAP-016, LEGACY-FUNC-121)`
10. `feat(reportes): ingresos por agencia de aduanas (GAP-010, LEGACY-FUNC-229)`

**Fase 6**

1. `feat(migracion): infraestructura de importación legacy (GAP-001)`
2. `feat(migracion): importar maestros del legacy (GAP-001, GAP-025, GAP-026)`
3. `feat(migracion): importar depósitos vivos y levantes (GAP-001, RN-035)`
4. `feat(migracion): conciliación y apertura de la facturación (GAP-001, RN-050)`
5. `feat(respaldos): respaldo diario con destinos configurables (GAP-021)`

---

## E. Rama, commits y migraciones

### E.1 Rama

- Todo se trabaja en `develop` (P17). No se crean ramas ni PR, y nadie hace merge.
- Las fases van en secuencia (1 → 6). Dentro de cada fase, los ítems van en el orden de §D.2, uno a la vez, porque comparten el árbol de trabajo.

### E.2 Ciclo de cada ítem

1. **Antes de empezar**, el implementador comprueba que `develop` está limpio (`git status` sin cambios). Si no lo está, no toca nada y avisa al usuario: el ítem anterior no tiene commit.
2. Implementa el ítem con sus pruebas.
3. Corre `dotnet build` y `dotnet test`. Los dos deben pasar.
4. **Se detiene** y entrega al usuario:
   - el identificador del ítem;
   - los archivos creados y modificados;
   - el resultado de la compilación y de las pruebas;
   - el mensaje de commit sugerido (§D.3);
   - si el ítem cambia el esquema, el nombre de la migración que debe generar (§F.1) y los cambios que debe contener.
5. El usuario revisa, genera la migración si aplica y hace el commit. El implementador no hace `git add`, `commit`, `push` ni `merge`.
6. Con el commit hecho (`develop` limpio), el implementador sigue con el ítem siguiente.

### E.3 Migraciones EF (las genera el usuario)

> **Estado (2026-10-01): una sola migración inicial, no una por ítem.** Las seis fases se implementaron y commitearon sin generar migraciones, así que al final el usuario intentó una única migración diferencial (`AddParityLegacy`) y falló al aplicarla: EF emitió cinco `UpdateData` de `products` sin columnas («UPDATE products SET  WHERE id = …», error 42601) porque `products.created_from_weighbridge` se configura con `HasDefaultValue(false)` y los productos sembrados traen ese valor (ver §G.22). Para no editar un archivo generado, el usuario borró las 24 migraciones históricas y generó **`20261001193201_InitialParityLegacy`**, que crea el esquema completo y aplica limpia sobre una base vacía (verificado contra un Postgres 18 temporal).
> **Consecuencia:** toda base que tenga el historial viejo (desarrollo y staging) se recrea; no se puede actualizar en sitio. Al 2026-10-01 no hay producción, y los datos reales entran por la carga legacy de la fase 6.
> **De aquí en adelante** vuelve a aplicar la regla de abajo: una migración por cada cambio de esquema, sobre esta inicial.

- **Carpeta:** la activa es `Wms.Infrastructure/Migrations`, que tiene `AppDbContextModelSnapshot.cs`. `Wms.Infrastructure/Persistence/Migrations` está vacía.
- **Una migración por cada ítem que cambia el esquema** (26 en total, §F.1; en la práctica quedaron consolidadas en la inicial única, ver el estado de arriba). Se genera después de que el implementador entrega el ítem y antes del commit, y va en ese mismo commit. Así cada commit de `develop` queda ejecutable y desplegable (staging usa `dotnet ef migrations script --idempotent`, `scripts/deploy-staging.sh:179`).
- **Comando sugerido:** `dotnet ef migrations add <Nombre> --project Wms.Infrastructure --startup-project Wms.Api`, con el nombre de la columna «Migración» de §F.1.
- **Revisión:** la migración debe contener solo los cambios del ítem en §F.1. Si aparece algo más, es un cambio de modelo no previsto y se revisa con el implementador antes del commit.
- Los datos iniciales opcionales de F4-01 (§F.3) van en la migración de ese ítem, si el usuario los quiere.

### E.4 Fases

| Fase | Ítems | Empieza cuando | Migraciones del usuario |
|---|---|---|---|
| 1 ✅ completada (2026-09-30) | F1-01 a F1-09 | de inmediato | 3 (F1-02, F1-06, F1-09), en la inicial única (§E.3) |
| 2 ✅ completada (2026-09-30) | F2-01 a F2-10 | la fase 1 tiene todos sus commits | 5 (F2-03, F2-05, F2-06, F2-07, F2-08), en la inicial única (§E.3) |
| 3 ✅ completada (2026-09-30) | F3-01 a F3-10 | la fase 2 tiene todos sus commits | 7 (F3-01, F3-04, F3-06, F3-07, F3-08, F3-09, F3-10), en la inicial única (§E.3) |
| 4 ✅ completada (2026-09-30) | F4-01 a F4-10 | la fase 3 tiene todos sus commits | 7 (F4-01, F4-03, F4-05, F4-07, F4-08, F4-09, F4-10), en la inicial única (§E.3) |
| 5 ✅ completada (2026-09-30) | F5-01 a F5-10 | la fase 4 tiene todos sus commits | 2 (F5-06, F5-09), en la inicial única (§E.3) |
| 6 ✅ completada (E19 cumplida el 2026-10-06) | F6-01 a F6-05 | la fase 5 tiene todos sus commits; la fase se cierra solo con la prueba con datos reales (E19) | 2 (F6-01, F6-05), en la inicial única (§E.3) |

### E.5 Confirmación final

El implementador de la fase 6, al terminar, revisa las tablas E.4 y F.1 contra lo que realmente pasó y las corrige en este documento si algo cambió:
- ítems partidos o reordenados;
- nombres de las migraciones que se generaron.

Deja la corrección sin commit, con el mensaje sugerido `docs(plan): confirmar fases y migraciones de la paridad legacy`, para que el usuario la revise.

---

## F. Cambios de esquema consolidados

El implementador no genera migraciones (§B.3). Esta lista es la referencia para revisar cada migración que genere el usuario. Los valores nuevos de enums guardados como texto no cambian el esquema (se listan al final).

### F.1 Por ítem, en orden

Los 26 cambios de esta tabla quedaron todos dentro de `20261001193201_InitialParityLegacy` (§E.3): la columna «Migración» es el nombre que se habría usado por ítem y sirve para rastrear qué cambió cada uno.

| # | Fase | Ítem | Cambio | Migración (la genera el usuario) |
|---|---|---|---|---|
| 1 | 1 | F1-02 | Índice no único `idx_service_records_document` sobre `service_records(cargo_manifest_number, primary_document_type_id)`. | `ParidadF1_02_IndiceDocumento` |
| 2 | 1 | F1-06 | `products.created_from_weighbridge boolean NOT NULL DEFAULT false`. | `ParidadF1_06_ProductoDesdeBascula` |
| 3 | 1 | F1-09 | `invoice_payments.cash_received numeric(18,2) NULL`, `invoice_payments.change_given numeric(18,2) NULL`. | `ParidadF1_09_EfectivoYCambio` |
| 4 | 2 | F2-03 | Índice no único `idx_import_releases_acceptance_number` sobre `import_releases(acceptance_number)`. | `ParidadF2_03_IndiceAceptacion` |
| 5 | 2 | F2-05 | `import_releases`: `fob_usd numeric(18,2) NULL`, `exchange_rate numeric(18,4) NULL`, `exchange_rate_source varchar(10) NULL`, `exchange_rate_date date NULL`, `fob_cop numeric(18,2) NULL`. | `ParidadF2_05_FobLevante` |
| 6 | 2 | F2-06 | Tabla nueva `cities` (F.2). | `ParidadF2_06_Ciudades` |
| 7 | 2 | F2-07 | `loading_orders.destination_city_id uuid NULL`, FK `cities(id)` `ON DELETE RESTRICT`, índice. | `ParidadF2_07_CiudadDestinoOrden` |
| 8 | 2 | F2-08 | `import_warehouse_storages`: `extension_registered_at timestamptz NULL`, `extension_registered_by_id uuid NULL`, `extension_notes varchar(500) NULL`. | `ParidadF2_08_Prorroga` |
| 9 | 3 | F3-01 | `loading_order_items.loaded_quantity numeric(18,4) NULL`; `warehouse_reserves.loading_order_item_id uuid NULL`, FK `loading_order_items(id)` `ON DELETE SET NULL`, índice. | `ParidadF3_01_CantidadCargada` |
| 10 | 3 | F3-04 | `dispatch_guides`: `cancelled_at timestamptz NULL`, `cancelled_by_id uuid NULL`, `cancellation_reason varchar(500) NULL`. | `ParidadF3_04_AnulacionGuia` |
| 11 | 3 | F3-06 | `storage_billing_periods.limit_date date NULL`. | `ParidadF3_06_FechaLimitePeriodo` |
| 12 | 3 | F3-07 | `loading_orders`: `reverted_at timestamptz NULL`, `reverted_by_id uuid NULL`, `reversal_reason varchar(500) NULL`. | `ParidadF3_07_ReversionOrden` |
| 13 | 3 | F3-08 | `warehouse_storages`: `cancelled_at timestamptz NULL`, `cancelled_by_id uuid NULL`, `cancellation_reason varchar(500) NULL`. | `ParidadF3_08_AnulacionDeposito` |
| 14 | 3 | F3-09 | `weighbridge_cycles` y `warehouse_storage_entries`: `voided_at timestamptz NULL`, `voided_by_id uuid NULL`, `void_reason varchar(500) NULL`. | `ParidadF3_09_AnulacionPesaje` |
| 15 | 3 | F3-10 | `invoices.reissued_from_invoice_id uuid NULL` e `invoices.reissued_as_invoice_id uuid NULL`, FK `invoices(id)` `ON DELETE RESTRICT`, índices. | `ParidadF3_10_Refacturacion` |
| 16 | 4 | F4-01 | Tabla nueva `warehouse_storage_product_placements` (F.2), con datos iniciales opcionales (F.3). | `ParidadF4_01_Ubicaciones` |
| 17 | 4 | F4-03 | Tabla nueva `warehouse_novelties` (F.2). | `ParidadF4_03_Novedades` |
| 18 | 4 | F4-05 | Tablas nuevas `packing_list_suppliers`, `packing_list_files` y `packing_list_items` (F.2). | `ParidadF4_05_ListasEmpaque` |
| 19 | 4 | F4-07 | `service_records.anchor_weighbridge_cycle_id uuid NULL`, FK `weighbridge_cycles(id)` `ON DELETE RESTRICT`, índice. | `ParidadF4_07_PesajeCompartido` |
| 20 | 4 | F4-08 | `service_records.source_entry_cycle_id uuid NULL`, FK `weighbridge_cycles(id)` `ON DELETE RESTRICT`, índice. | `ParidadF4_08_SalidaConTiquete` |
| 21 | 4 | F4-09 | Tabla nueva `warehouse_storage_label_prints` (F.2). | `ParidadF4_09_ImpresionEtiquetas` |
| 22 | 4 | F4-10 | Tabla nueva `crews` (F.2); `warehouse_storages.crew_id uuid NULL` y `loading_orders.crew_id uuid NULL`, FK `crews(id)` `ON DELETE RESTRICT`, índices. | `ParidadF4_10_Cuadrillas` |
| 23 | 5 | F5-06 | `stakeholders.is_uap boolean NOT NULL DEFAULT false`. | `ParidadF5_06_Uap` |
| 24 | 5 | F5-09 | `weighbridge_cycles.ticket_first_printed_at timestamptz NULL`. | `ParidadF5_09_TiqueteImpreso` |
| 25 | 6 | F6-01 | Tablas nuevas `legacy_import_batches` y `legacy_id_map` (F.2); `warehouse_storages`: `legacy_number varchar(30) NULL` (índice único parcial `WHERE legacy_number IS NOT NULL`), `is_migrated boolean NOT NULL DEFAULT false`, `billing_start_date date NULL`. | `ParidadF6_01_ImportacionLegacy` |
| 26 | 6 | F6-05 | Tablas nuevas `backup_destinations` y `backup_runs` (F.2). | `ParidadF6_05_Respaldos` |

### F.2 Tablas nuevas

Todas tienen `id uuid PK`, `created_at timestamptz NOT NULL` y `updated_at timestamptz NULL`, salvo que se indique otra cosa. Nombres en *snake_case*, como el resto del esquema.

| Tabla | Columnas | Índices y FK |
|---|---|---|
| `cities` | `legacy_id int NULL`, `name varchar(35) NOT NULL`, `country_code varchar(3) NOT NULL`, `district varchar(20) NULL`, `transit_days int NULL`, `is_abandonment_destination boolean NOT NULL DEFAULT false`, `is_active boolean NOT NULL DEFAULT true` | único parcial `legacy_id`; índice `name` |
| `warehouse_storage_product_placements` | `warehouse_storage_product_id uuid NOT NULL`, `warehouse_location_id uuid NOT NULL`, `quantity numeric(18,4) NOT NULL`, `last_placed_at timestamptz NOT NULL` | único (`warehouse_storage_product_id`, `warehouse_location_id`); FK a `warehouse_storage_products` `ON DELETE CASCADE`, a `warehouse_locations` `ON DELETE RESTRICT`; *check* `quantity > 0` |
| `warehouse_novelties` | `warehouse_storage_product_id uuid NOT NULL`, `warehouse_storage_entry_id uuid NULL`, `type varchar(20) NOT NULL`, `started_at timestamptz NOT NULL`, `ended_at timestamptz NOT NULL`, `ordered_by varchar(100) NULL`, `description varchar(4000) NOT NULL`, `total_quantity`, `good_quantity`, `damaged_quantity`, `missing_quantity`, `surplus_quantity` (`numeric(18,4) NOT NULL DEFAULT 0`), `is_unloaded boolean NOT NULL DEFAULT false`, `tarp_condition varchar(20) NULL`, `trailer_condition varchar(20) NULL`, `photo_record varchar(200) NULL`, `created_by_id uuid NOT NULL`, `voided_at timestamptz NULL`, `voided_by_id uuid NULL`, `void_reason varchar(500) NULL` | FK a `warehouse_storage_products` y `warehouse_storage_entries` `ON DELETE RESTRICT`; índices por producto y por `started_at` |
| `packing_list_suppliers` | `name varchar(200) NOT NULL`, `is_active boolean NOT NULL DEFAULT true` | índice `name` |
| `packing_list_files` | `supplier_id uuid NOT NULL`, `importer_id uuid NOT NULL`, `file_name varchar(250) NOT NULL`, `item_count int NOT NULL`, `created_by_id uuid NOT NULL` | FK a `packing_list_suppliers` y `stakeholders` `ON DELETE RESTRICT`; índice `importer_id` |
| `packing_list_items` | `packing_list_file_id uuid NOT NULL`, `code varchar(40) NOT NULL`, `description varchar(250) NOT NULL`, `packages numeric(18,4) NOT NULL`, `units_per_package numeric(18,4) NOT NULL`, `net_weight_kg numeric(18,4) NOT NULL`, `product_id uuid NOT NULL`, `status varchar(20) NOT NULL`, `warehouse_storage_entry_id uuid NULL`, `associated_at timestamptz NULL`, `associated_by_id uuid NULL` | FK a `packing_list_files` `ON DELETE CASCADE`, a `products` y `warehouse_storage_entries` `ON DELETE RESTRICT`; índices (`packing_list_file_id`), (`code`), (`status`) |
| `warehouse_storage_label_prints` | `warehouse_storage_id uuid NOT NULL`, `action varchar(10) NOT NULL`, `printed_by_id uuid NOT NULL` (sin `updated_at`) | FK a `warehouse_storages` `ON DELETE CASCADE` y a usuarios; índice `warehouse_storage_id` |
| `crews` | `legacy_id int NULL`, `name varchar(200) NOT NULL`, `is_active boolean NOT NULL DEFAULT true` | único parcial `legacy_id`; índice `name` |
| `legacy_import_batches` | `entity varchar(40) NOT NULL`, `file_name varchar(250) NOT NULL`, `dry_run boolean NOT NULL`, `total_rows`, `created_rows`, `updated_rows`, `skipped_rows`, `error_rows` (`int NOT NULL`), `errors jsonb NULL`, `created_by_id uuid NOT NULL` (sin `updated_at`) | índice (`entity`, `created_at`) |
| `legacy_id_map` | `entity varchar(40) NOT NULL`, `legacy_id varchar(50) NOT NULL`, `target_id uuid NOT NULL`, `batch_id uuid NOT NULL` (sin `updated_at`) | único (`entity`, `legacy_id`); índice (`entity`, `target_id`); FK a `legacy_import_batches` `ON DELETE RESTRICT` |
| `backup_destinations` | `name varchar(100) NOT NULL`, `type varchar(10) NOT NULL`, `local_path varchar(500) NULL`, `bucket varchar(200) NULL`, `prefix varchar(200) NULL`, `region varchar(50) NULL`, `service_url varchar(300) NULL`, `is_active boolean NOT NULL DEFAULT true` | único `name` |
| `backup_runs` | `started_at timestamptz NOT NULL`, `finished_at timestamptz NULL`, `kind varchar(10) NOT NULL`, `status varchar(20) NOT NULL`, `size_bytes bigint NULL`, `results jsonb NULL`, `error text NULL`, `triggered_by_id uuid NULL` (sin `updated_at`) | índice (`kind`, `started_at`) |

### F.3 Datos iniciales opcionales

Para F4-01, se agregan a su migración (`ParidadF4_01_Ubicaciones`) si el usuario lo decide al generarla:

```sql
INSERT INTO warehouse_storage_product_placements (id, warehouse_storage_product_id, warehouse_location_id, quantity, last_placed_at, created_at)
SELECT gen_random_uuid(), p.id, p.warehouse_location_id, p.current_stock, now(), now()
FROM warehouse_storage_products p
WHERE p.warehouse_location_id IS NOT NULL AND p.current_stock > 0;
```

### F.4 Valores nuevos de enums guardados como texto (sin esquema)

| Enum | Valores nuevos | Ítem |
|---|---|---|
| `BillingCycle` | `Days15`, `Days30`, `Days90`, `Days180`, `Days360` | F3-05 |
| `LoadingOrdersStatus` | `Reverted` | F3-02 y F3-07 |
| `SourceTypeMovements` | `LoadingOrderReversal`, `StorageCancellation`, `WeighingVoid` | F3-07 a F3-09 |
| `SourceTypeMovements` | `MigrationOpening` | F6-03 |

Los enums nuevos (`CargoUnitDeclarationMode`, `NoveltyType`, `TarpCondition`, `TrailerCondition`, `PackingListItemStatus`, `LabelPrintAction`, `LegacyImportEntity` y los de respaldo) se guardan como texto en las columnas de F.2.

---

## G. Observaciones: defectos encontrados fuera de alcance

No se corrigen en este plan. Se dejan para que el usuario decida.

1. **Rol de Vigilancia a báscula** (decisión 2026-09-29). Ese rol también abre Bodega completa y la corrección de ingresos (`BASCULA_PARITY.md` §6). Es acceso: fuera de alcance.
2. **Terceros editables por cualquier usuario activo.** `StakeholderController` (`[Authorize(Policy = "ActiveUser")]`, `Wms.Api/Controllers/v1/StakeholderController.cs:44`) permite `POST` y `PATCH` a cualquier usuario activo. F5-06 agrega un campo sin cambiar la política.
3. **`GenerateGlobalDispatchGuide` de la v2** (`Wms.Application/Weighbridge/Commands/Storage/GenerateGlobalGuide/`) cierra con un solo peso el ciclo del flujo de perecederos y tiene un TODO para persistir una «guía global». Su nombre se confunde con la «Salida Global» del legacy, que es otra cosa y se cubre con F4-08 (P16). No se toca.
4. **Dos carpetas de migraciones.** `Wms.Infrastructure/Persistence/Migrations` está vacía y la activa es `Wms.Infrastructure/Migrations`. Conviene borrar la vacía para que nadie genere ahí.
5. **Fecha programada de la orden de cargue.** El dominio tolera 1 hora hacia atrás (`LoadingOrder.cs:96`) y el validador otra tolerancia (`CreateLoadingOrderCommandValidator.cs:33`). Conviene unificarlas.
6. **Dos caminos para crear órdenes de cargue** (`POST foreign-trade/loading-orders` y `POST warehouse/loading-orders`). F2-07 y F4-10 modifican los dos; a futuro conviene uno solo.
7. **`Invoice.Cancel` acepta facturas parcialmente pagadas** (`Invoice.cs:325-343` solo rechaza `Paid`). Las anulaciones automáticas de este plan no las tocan (`InvoiceCancellationPolicy`), pero el endpoint manual sí puede.
8. **Anular una factura consolidada** anula también sus líneas que no son de almacenamiento. F3-10 las clona al refacturar; fuera de ese flujo se pierden.
9. **Líneas sobrescritas.** Al refacturar (F3-10) se clonan con su valor vigente, sin la marca de sobrescritura.
10. **`LoadingOrder.Complete()` no tiene llamadores:** el estado `Complete` no se alcanza. Las reglas de este plan lo tratan igual que `Dispatched` por seguridad.
11. **La guía se puede emitir antes del cargue** (orden `Pending`, `InProgress` o `Loaded`, `CreateDispatchGuideCommandHandler.cs:113-119`). Con un cargue parcial, la guía muestra lo pedido; se corrige anulándola (F3-04).
12. **Frontend:**
    - la exportación de importaciones pide `pageSize: 10000`, que el API recorta a 50: debe usar `all=true` (F5-01);
    - el botón «Exportar Excel» de inventario llama a un método inexistente;
    - falta el método del PDF del recibo de recepción.
13. **UI-22** (cobros pendientes visibles para báscula) exige que el rol `Scale` lea facturas: es un cambio de política.
14. **Anomalías del legacy que no se replican:**
    - el cron generaba períodos sin la gracia de 3 días en su primera rama (`cron.php:98-123`);
    - el total «SIN NAL» del reporte de prórrogas estaba mal (F2-10);
    - `vista_kardexproductoenbodega` filtra `'elimininado'` (errata, `bodegas_schema.sql:2431`);
    - en `reportesias.php` una fila «Báscula» arrastra el saldo de la anterior;
    - `duplicarrecibo.php` fija la modalidad 4 y `cargarlistasempaque.php` fija el embalaje 1;
    - el informe de pólizas rotula «CIF» lo que es la suma del FOB en dólares. F5-06 conserva el cálculo; el rótulo lo decide el usuario en el frontend.
15. **La recepción no valida la capacidad de la ubicación** (RN-047). Se conserva, como el legacy. F4-01 sí valida que la ubicación esté habilitada.
16. **Líneas nuevas en una factura ya rastreada — CORREGIDO el 2026-09-30** (hallado al verificar la fase 1). El `Id` de `InvoiceItem` lo genera el dominio y la clave era `ValueGeneratedOnAdd`: una línea agregada a una factura que EF ya rastreaba quedaba `Modified` en vez de `Added` y el guardado fallaba con `DbUpdateConcurrencyException`. Tenía dos efectos:
    - el recálculo del período abierto (`StorageBillingService.RecalculateCoreAsync`: camión tardío, CE-7, edición de productos, TRM manual, F1-04 y F1-07) no se guardaba; el disparador capturaba el error y avisaba a Facturación «No se pudo facturar el almacenamiento»;
    - con facturación consolidada, confirmar el segundo depósito de un cliente en el mismo período fallaba y el depósito quedaba en Borrador (`OpenPeriodWithInvoiceAsync` sobre la consolidada existente). El mismo patrón está en la guía de salida a crédito consolidada (`CreateDispatchGuideCommandHandler`).

    Corrección: `builder.Property(i => i.Id).ValueGeneratedNever()` en `InvoiceItemConfiguration`, el mismo remedio de `AgreementParameterConfiguration`. No cambia el esquema: no genera operaciones de migración; la próxima migración que se genere solo actualizará esa línea en `AppDbContextModelSnapshot`. Verificado contra un Postgres temporal: el recálculo por camión tardío pasa de 10 a 15 unidades facturadas y la consolidada recibe su segunda línea. La guía consolidada no se probó de forma directa.
17. **Detalle de la orden de cargue — CORREGIDO el 2026-09-30** (hallado al verificar la fase 2). `GetLoadingOrderDetailHandler` leía `wsp.UnitMeasure.Name` sin incluir la navegación (desde WMS-18, 2026-09-17): `GET foreign-trade/loading-orders/{id}` y `GET warehouse/loading-orders/{id}` respondían con `NullReferenceException`. Se agregó el `Include` de la unidad de medida. No se revisaron los demás usos de `UnitMeasure.Name` en memoria.
18. **Peso bruto de facturación sin camiones — CORREGIDO el 2026-09-30** (hallado en F3-09). `StorageBillingService.ResolveStorageChargesAsync` sumaba `storage.Entries.Sum(e => e.ManifestWeight)` sin incluir la navegación: fuera de la misma unidad de trabajo de báscula (confirmación, job de renovación, recálculos posteriores al commit) el peso bruto era 0 y la fórmula por umbral de peso (perecederos, WMS-32) caía al valor mínimo con advertencia. Se agregó el `Include` de los camiones y se excluyen los anulados. Sin cambio de esquema.
19. **Reintento de la guía de exportación — CORREGIDO el 2026-09-30** (hallado en F4-10). `CreateExportDispatchGuideCommandHandler` recarga la orden cuando el guardado choca por número de guía, pero sin `Include` de la ciudad de destino: en ese reintento el vencimiento se calculaba sin días de tránsito (30 días). Se agregaron los `Include` de la ciudad y de la cuadrilla. Sin cambio de esquema.
20. **Listado de importaciones — CORREGIDO el 2026-09-30** (hallado al verificar F5-02). `GetImportDepositsHandler.MapToDto` leía `UnitMeasure.Name` del primer producto sin incluir la navegación (desde WMS-18): `GET foreign-trade/imports` respondía con `NullReferenceException` en cuanto una página tenía un depósito con productos. Se agregó el `Include` de la unidad. Sin cambio de esquema.
21. **Informe de movimientos por depósito — CORREGIDO el 2026-09-30** (hallado al verificar F5-04). `GetWarehouseStorageMovementsHandler` cargaba los movimientos sin la unidad del producto y fallaba igual con cualquier movimiento; lo arrastraban `GET warehouse/movements-report` y su PDF. Se agregó el `Include`. Siguen sin revisarse los demás usos de `UnitMeasure.Name` en memoria (§G.17).
22. **`UpdateData` vacío al sembrar una columna con valor predeterminado — resuelto de raíz al consolidar las migraciones (2026-10-01).** Una columna nueva `NOT NULL` configurada con `HasDefaultValue(...)` en una tabla con `HasData` hace que EF marque las filas sembradas como cambiadas y emita `UpdateData`; al coincidir el valor con el predeterminado de una columna generada por la base, EF le quita la única columna y el SQL queda `UPDATE t SET  WHERE id = …` (error 42601). Pasó con `products.created_from_weighbridge` (`ProductConfiguration.cs:27`) y es un defecto conocido de EF Core. La migración inicial única no lo tiene (siembra con `InsertData`), pero volverá a aparecer si se agrega otra columna así a una tabla sembrada: entonces hay que quitar el `HasDefaultValue` de esa propiedad (el `AddColumn` ya rellena las filas existentes) o borrar a mano las operaciones vacías.
23. **`FormulaType.ParameterSchema` sin comparador de valores.** La colección va a `jsonb` con conversor pero sin `ValueComparer`, así que EF no compara sus elementos y avisa en cada arranque; una mutación en sitio de la lista podría no guardarse. Las dos colecciones `jsonb` de la fase 6 (`LegacyImportBatch.Errors` y `BackupRun.Results`) sí lo tienen desde el 2026-10-01. El arreglo es el mismo patrón y no cambia el esquema.
