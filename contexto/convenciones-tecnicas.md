# Convenciones técnicas — WMS Bodegas Asociadas

> **Para qué sirve:** stack, arquitectura, permisos, migraciones, pruebas, ambientes y trampas conocidas, para desarrollar o corregir defectos sin romper lo que ya funciona.
> **Fecha de corte:** 2026-10-23. Backend `develop` `35a61b2`, frontend `develop` `c924a8b`. Las rutas son relativas a `code_workspace/`.
> **Idioma:** el código, en inglés; el negocio, la UI, los mensajes de error y la documentación, en español.

## 1. Repositorios y stack

| Repo | Rama | Stack |
| --- | --- | --- |
| `Backend/wms-api` | `develop` (y `main`) | .NET 10 (`net10.0` en todos los proyectos), ASP.NET Core, EF Core 10 con Npgsql (PostgreSQL 18, tablas y columnas en snake_case con EFCore.NamingConventions), MediatR 12 (CQRS), FluentValidation 12, Identity con JWT y refresh tokens, SignalR, QuestPDF, Mapperly, AWSSDK.S3 (respaldos), xUnit 2.9 y Testcontainers |
| `Frontend/wms` | `develop` | Nuxt 4 como SPA (`ssr: false`), Vue 3.5, PrimeVue 4 (plantilla Ultima), Pinia 3, TanStack Vue Query 5, SignalR, VueUse, Tailwind 3, Zod 4, ExcelJS, Chart.js, Vitest 4. Gestor: **Yarn 4** (`packageManager`, `nodeLinker: node-modules`). El `package-lock.json` versionado sobra: no lo uses |
| `docs` | `main` | Este hub de documentación |

`Backend/wms-api/README.md` está desactualizado: dice .NET 8 y solo documenta el ambiente de Azure.

## 2. Backend

| Proyecto | Contenido |
| --- | --- |
| `Wms.Api` | Controladores (`Controllers/v1`), jobs (`BackgroundJobs`), identidad (`Common/Identity`), `Program.cs` |
| `Wms.Application` | Comandos, consultas, handlers, validadores, servicios y DTO por feature. Referencia a `Wms.Infrastructure` |
| `Wms.Domain` | Entidades con métodos de dominio, enums, contratos (`IAuditable`, `IAuditContext`) y la matriz de permisos (`Security/WmsPolicyRoles.cs`) |
| `Wms.Infrastructure` | `AppDbContext`, configuraciones EF, migraciones, servicios externos (DIAN, correo, almacenamiento, respaldos) |
| `Wms.Common` | Excepciones, paginación (`Wrappers`), `ColombiaTime` |
| `Wms.Tests` | xUnit sin base de datos: dominio, validadores y clases puras |
| `Wms.IntegrationTests` | El API completo con `WebApplicationFactory` sobre Postgres en Testcontainers (`Infrastructure/WmsApiFactory.cs`). Necesita Docker |

- **Ids:** los genera el dominio (`Guid.NewGuid()`). Ver la trampa de EF en §10.
- **Errores de negocio:** `BadRequestException`, `ConflictException` y `NotFoundException` (`Wms.Common/Exceptions`), con mensaje en español dirigido al operario. Los estados se muestran traducidos.
- **Autor de una operación:** sale del token con `ClaimsPrincipalExtensions.GetRequiredUserId()`. Nunca del cuerpo de la petición.
- **Fechas de negocio:** con `ColombiaTime` (`Wms.Common/Time/ColombiaTime.cs`, America/Bogota). `DateTimeOffset.UtcNow` solo en `CreatedAt` y `UpdatedAt`. Los PDF y reportes imprimen hora de Colombia.
- **Paginación:** `QueryParametersBase` recorta `pageSize` en silencio a 50. Para traer todo (selects, catálogos) se envía `all=true`; con eso `PageSize` vale `int.MaxValue`, así que no lo uses para reservar memoria ni para aritmética.
- **Auditoría genérica:** toda entidad `IAuditable` registra altas, cambios y bajas en `audit_logs`, con usuario, IP y valores anterior y nuevo; el motivo va por `IAuditContext`. Un criterio «queda auditado» se cumple con esto: no crees tablas de auditoría.
- **Cálculo de tarifas:** existe una sola vez (`BillingResolver` y `FormulaPricing.Price`). No lo dupliques en otro servicio.
- **PDF:** QuestPDF. Para comprobar el texto de un PDF en pruebas: `pdftotext -layout`.

## 3. Frontend

- Rutas en `app/pages`. Lógica por dominio en `app/features/<dominio>/` (services, composables, types, components).
- API base: `NUXT_PUBLIC_API_BASE` (local `http://localhost:5281/api/v1`). Centro de ayuda: `NUXT_PUBLIC_AYUDA_BASE_URL`.
- **Permisos:**
  - Cada página declara `definePageMeta({ requiredRoles: [...] })`, que valida `app/middleware/auth.global.ts`.
  - El menú se filtra por roles en `app/components/layout/AppMenu.vue`.
  - Los roles se leen con `usePermissions` y `ROLES` **con import explícito** (`import { usePermissions, ROLES } from "~/composables/usePermissions"`), no con auto-import.
- Tras cada mutación, invalida el prefijo de la consulta (`['billing']`, `['foreign-trade']`…).
- Búsquedas con `watchDebounced`.
- Textos en español. Números y monedas solo con las utilidades de `app/shared/utils/format.ts` (`formatNumber`, `formatKg`, `formatCurrency`), y las fechas con las de `app/utils/colombia-date.ts` (`formatColombiaDate`, `formatColombiaTime`, `formatColombiaDateTime`). `<InputNumber>` siempre con `locale="es-CO"`.
- **Guardias de código fuente** en `test/unit/guards/`: prohíben `toLocale*`, `es-ES`, `new Intl.*` fuera de las utilidades y botones sin `label`, `aria-label` o `title`. Un `yarn test` en rojo por una guardia es un defecto real.
- Errores del API: `app/utils/api-error.ts` y `api-error-notifier.ts`. Envíos dobles: `useSubmitGuard`.
- **Drawer de detalle** (`DEC-080`; plan `planes/sprint-11/f02-base/plan-cerrado-f2-f02-ajustes-qa-2026-11-24.md`, D3, D5 y D6; D3 derogada por `planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md`, D12). Todo detalle de un registro sobre un listado usa `AppDetailDrawer` con secciones `AppDetailSection`; la galería `/dev/components` muestra el patrón:
  - **Encabezado:** `icon` (PrimeIcons), `title`, `status` (`activeStatus()` de `app/types/app-detail.ts`, o la etiqueta que haga de estado) y `subtitle` en una línea, con los datos clave separados por «·». Ampliar y cerrar los pinta el componente.
  - **Acciones del registro** (`actions`): todas van en el menú «Acciones» (⋮) del encabezado, sea una o sean varias, y el drawer no lleva pie. Sin acciones, no hay menú. Nunca un botón de acción suelto en el encabezado ni dentro de una sección para editar el registro.
  - **Secciones:** una `AppDetailSection` por bloque, con `title` e `icon`; `count` para listas; la acción de la sección («Agregar») en el slot `actions`; `flush` para una tabla `DataTable size="small"`; `empty`, `empty-text` y el slot `empty-action` para el estado vacío; los diálogos de la sección en el slot `dialogs`. Los datos van en pares `dt`/`dd` dentro de `.app-detail-grid`.
  - **Botones de solo icono** (acciones de fila, encabezado): siempre con `v-tooltip.top` con el verbo («Ver detalle», «Editar», «Eliminar»…) y su `aria-label`. «Ver» es de solo icono (`pi pi-eye`).
- **Tablas de listado** (`DEC-080`; plan `planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-ajustes-ui-2026-11-24.md`, D5 y D6; `plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md`, D17). Se suman a las del drawer:
  - **Tamaño y estilo:** los botones de acción de una fila llevan siempre `size="small"`, `severity="secondary"` (o el de la acción) y `outlined`, como las tablas de Configuración; el botón «⋮» del menú, también.
  - **Más de tres acciones:** si una tabla puede tener más de tres acciones por fila, todas van al menú «Acciones» (⋮) de `AppRowActions` (`app/components/app/AppRowActions.vue`, tipos en `app/types/app-row-actions.ts`).
    - La regla es por tabla, no por fila: la página pasa todas las acciones posibles, con `visible` según la fila. Así, una fila que solo tiene «Ver» también usa el menú.
    - Con tres o menos, `AppRowActions` pinta botones de solo icono con tooltip.
    - Una acción destructiva lleva `severity="danger"` y `separator` para ir al final, tras un divisor.
  - **Filtros:** en la columna, no en una búsqueda global. Los estados de una cola o de una lista corta pueden ir en pestañas (`Tabs`) con su contador en el slot `toolbar`. **Fila expandible** (F05, D34): un maestro-detalle usa `AppDataTable` con `expandable`, `v-model:expandedRows` y el slot `expansion`; las acciones van solo en la fila principal (AF-99).
  - **Galería:** `/dev/components` muestra `AppRowActions` con tres y con cinco acciones.
- **Aviso junto a un dato** (`DEC-080`; plan `planes/sprint-11/f05-comercio-exterior/plan-cerrado-f2-f05-ajustes-ui-2026-11-26.md`, D4). Un aviso junto a un dato es un `AppAlertIcon` con tooltip, no una etiqueta ni un mensaje.
  - **Componente:** `app/components/app/AppAlertIcon.vue`, con `text` (el tooltip y el `aria-label`) y `severity`: `warn` (ámbar, por omisión), `danger` (rojo) o `info` (azul). Es enfocable y el tooltip también se abre con el teclado.
  - **Dónde va:** a la derecha del dato que acompaña (el N.º de depósito con etapas pendientes, la placa con datos pendientes, el peso con diferencia). Una fila anulada también: `AppAlertIcon` (`danger`) junto a su dato principal, con la fecha de la anulación en el tooltip, sin la etiqueta «Anulada» (D34).
  - **Fila anulada en una tabla:** el fondo de la fila va en rojo tenue (`--p-red-50`; en tema oscuro, rojo al 15 %), como el historial de Báscula (AF-23). La regla de CSS necesita más especificidad que las filas alternas de `app/assets/layout/_wms-datatable.scss` (D36).
  - **Qué no es un aviso** (plan `planes/sprint-11/plan-cerrado-f2-alert-icon-f01-f04-2026-11-26.md`, D2): un estado en su propia columna o en su campo («Estado», «Corregido», «Tipo»; también «Anulada» en la columna «Estado» de los historiales de Báscula, P1); un valor que es el dato («Por ubicar» en lugar de la ubicación, el tiempo en planta, los relojes de Bodega); el estado del registro en el encabezado del drawer o del modal; los mensajes de una sección o de un formulario (validaciones, avisos de un paso, estados vacíos, confirmaciones y el aviso del registro anulado al inicio de un drawer). Esos siguen como etiqueta o mensaje.
  - **Guardia:** `test/unit/guards/source-guards.spec.ts` («guardia: aviso junto a un dato») rechaza un `<i class="pi pi-exclamation-…">` con `v-tooltip` fuera de `AppAlertIcon.vue`.
  - **Adopción:** F05 lo usa desde sus ajustes de UI y F01 a F04 desde el plan `planes/sprint-11/plan-cerrado-f2-alert-icon-f01-f04-2026-11-26.md`. Las fases siguientes (F06 a F09) lo aplican al hacer sus pantallas.
- **Páginas que no son listados** (`DEC-080`; plan `planes/sprint-11/plan-cerrado-f2-paginas-sin-tarjeta-titulo-2026-11-24.md`, D1, D2, D5, D6 y D8). Tableros, formularios de operación y reportes no llevan la tarjeta de título (`AppPageHeader`), como los listados:
  - **Título:** nada visible en su lugar; el breadcrumb nombra la página. La página pone un `<h1 class="sr-only">` con su título para los lectores de pantalla y conserva su raíz `.wms-page`.
  - **Subtítulo:** se elimina, salvo que explique una regla del reporte; esa regla va como texto atenuado (`text-sm text-muted-color`) al pie de la tarjeta de filtros.
  - **Acciones de un reporte** («Exportar Excel», «Descargar PDF»): en la fila de botones de la tarjeta de filtros, a la derecha (`ml-auto`), después de «Consultar» o «Generar», con su `severity`, `loading` y `disabled`.
  - **Acciones de una página sin tarjeta propia donde ponerlas:** en una barra sin tarjeta arriba del contenido, alineada a la derecha (`flex flex-wrap items-center justify-end gap-2`).
  - **Guardia:** `test/unit/guards/list-pattern.spec.ts` exige que ninguna ruta de `OUTSIDE` use `AppPageHeader`, salvo las de `TITLE_CARD_PENDING` (con la fase que la rehace; hoy, los dos reportes de Facturación de F08), y que tengan un `<h1`. Una página nueva que no sea listado entra a `OUTSIDE` y cumple la regla desde el principio. `AppPageHeader` se borra cuando desaparezca su último uso.

## 4. Permisos

**Roles del sistema** (`SystemRolesCode`): `Receiving` (Vigilancia), `Scale` (Báscula), `Warehouse` (Bodega), `ForeignTrade` (Comercio exterior), `Billing` (Facturación) y `Admin`. Un usuario puede tener varios.

**Políticas** (`Wms.Domain/Security/WmsPolicyRoles.cs`; `Wms.Api/Common/Identity/WmsAuthentication.cs` solo las registra):

| Política | Roles |
| --- | --- |
| `AdminOnly` | Admin |
| `WarehouseAccess` | Admin, Warehouse |
| `BillingAccess` | Admin, Billing |
| `ForeignTradeAccess` | Admin, ForeignTrade |
| `ScaleAccess` | Admin, Scale |
| `WeighingCorrectionAccess` | Admin, Scale, Billing |
| `OperationalAccess` | Admin, Warehouse, Receiving, Scale |
| `EntryCorrectionAccess` | Admin, Receiving |
| `DepositEntryDateAccess` | Admin, Scale, ForeignTrade |
| `ExitBlockAccess` | Admin, ForeignTrade, Billing (marca «sin salidas» del tercero, `PATCH stakeholder/{id}/exit-block`) |
| `GateAccess` | Admin, Receiving |
| `EntryLogReadAccess` | Admin, Receiving, Warehouse (leer un ingreso de Vigilancia, `GET entry-logs/{id}` en `EntryLogReadController`; lo usa la recepción directa de Bodega, F04 I-04) |
| `StakeholderAccess` | Admin, ForeignTrade |
| `TransportCatalogAccess` | Admin, Receiving, Scale, ForeignTrade |
| `DriverCatalogAccess` | Admin, Receiving, Scale, ForeignTrade, Warehouse |
| `NoveltyReadAccess` | Admin, Warehouse, ForeignTrade |
| `NoveltyWriteAccess` | Admin, Warehouse, ForeignTrade (registrar, editar y anular novedades; CE lo hace desde la etapa Bodega del depósito, F05 I-05 (1)) |
| `InventoryReportAccess` | Admin, ForeignTrade, Warehouse, Billing |
| `LocationCreateAccess` | Admin, ForeignTrade, Billing, Warehouse (crear una ubicación desde la recepción de Bodega, `POST warehouse/locations`; editar y borrar siguen en `ConfigurationAccess`) |
| `ActiveUser` | Cualquier usuario autenticado y activo |

**Convención:** los permisos se aflojan **por endpoint**, no por controlador.

- Lecturas y catálogos que usan los flujos operativos → `ActiveUser`.
- Escrituras operativas → `OperationalAccess` o la política específica.
- Configuración de tarifas y de facturación → restringida.

Los `[Authorize]` de ASP.NET se suman (AND): para aflojar una acción de un controlador restringido hay que moverla a otro controlador. Así nacieron, entre otros:

- `WeighbridgeCatalogController`, `WeighbridgeSharedController` y `WeighbridgeCycleReadController`.
- `BillingPreviewController`, `WarehouseMovementsReportController`, `InventoryReportsController` y `WarehouseNoveltiesController`.
- `DriverController` y `VehicleController`.
- `EntryLogReadController` (F04, I-04).

`InventoryAdjustmentController` (ajuste CE-7) usa `ForeignTradeAccess`: el ajuste es de Comercio Exterior, no de Bodega.

**Sesión:** el token deja de valer en cuanto el usuario se desactiva, cambia de roles o de contraseña, o cierra sesión. Lo controlan `IUserSessionGuard` y el claim `sstamp`, con caché de 15 s. Tras cambiar políticas, reinicia el API: se registran al arrancar.

**Antes de restringir** una política o una página, lista qué pantallas llaman al endpoint y con qué roles. Ningún rol puede perder una función que usa (`DEC-005`).

## 5. Migraciones EF

- Las genera y aplica **el agente**, solo con `dotnet ef`, solo en la base local (`DEC-004`). Comandos en `procesos/verificacion-local.md` §4.
- **Nunca se editan a mano** los archivos generados de `Wms.Infrastructure/Migrations/`. Tampoco hay SQL manual contra ninguna base.
- **El historial se consolidó** el 2026-10-01 en `20261001193201_InitialParityLegacy`: las bases con la cadena anterior se recrean, no se actualizan. Desde entonces hay 15 migraciones más; la última es `20261025152149_RelaxServicePriceActiveIndex` (las cinco del plan de brechas P1: `AddStakeholderExitBlock`, `FixAgreementActiveStakeholderIndex`, `AddWarehouseStorageLegacyYear`, `AddGuideCodeTypeParameter` y esa, de la fase 12c).
- Staging se actualiza con un script idempotente (`dotnet ef migrations script --idempotent`) que aplica `deploy-staging.sh migrate`, con aprobación del usuario.
- `Directory.Build.props` fija `BaseOutputPath` por un fallo de `dotnet ef` en macOS. `dotnet-ef` se instala global.
- Una columna nueva `NOT NULL` en una tabla con `HasData` **no lleva** `HasDefaultValue`.

## 6. Jobs en segundo plano (`Wms.Api/BackgroundJobs`)

| Job | Qué hace |
| --- | --- |
| `OverdueDetectionBackgroundService` | Marca facturas vencidas y recalcula el estado financiero de los clientes (cada 24 h) |
| `InvoicePaymentReconciliationBackgroundService` | Conciliación diaria de pagos. Reemplazó a `DailyChargeConsolidation` |
| `StoragePeriodAutoCloseBackgroundService` | Cierra períodos de almacenamiento vencidos y renueva los de depósitos con stock (programación dinámica) |
| `InvoiceDueNotificationBackgroundService` | Avisa de facturas próximas a vencer |
| `AbandonmentAlertBackgroundService` | Alerta de depósitos próximos al abandono (07:00 Colombia) |
| `DatabaseBackupBackgroundService` | Respaldo diario de base y archivos (02:00 Colombia, si `Backups:Enabled`); el primero exitoso del mes queda como mensual. Si falla, envía el correo de fallo a los Admin activos y a `Notifications:AdminEmails` |
| `AgreementActivationBackgroundService` | Activa los convenios «Programados» cuya fecha llegó (a los 30 s del arranque y cada día a las 00:00:30 Colombia) y archiva el activo anterior |
| `WarehouseDelayAlertBackgroundService` | Relojes de Bodega: cada minuto (`WarehouseAlerts:IntervalSeconds`) avisa «Atraso de Bodega» a CE y Bodega al cruzar el umbral amarillo o rojo de la recepción, el cargue o la salida de patio; un aviso por nivel y por reloj (`warehouse_delay_alerts`) |

`Wms.IntegrationTests` retira los jobs y sustituye por dobles el correo, la TRM y los respaldos.

**Destinatarios de los avisos por correo** (`DEC-070`): `NotificationOrchestrator` envía el correo a los usuarios activos del rol destino con correo, sin repetir (`NotificationRecipients`, en `Wms.Infrastructure/Services/`). `Notifications:AdminEmails` es solo respaldo, para cuando ninguno tiene correo; con el rol sin usuarios activos no se envía nada. Los métodos tipados sin llamadores de `INotificationService` y el correo de fallo del respaldo siguen con su regla propia.

## 7. Pruebas y compuertas

| Comando | Desde |
| --- | --- |
| `dotnet build Wms.sln` | `Backend/wms-api` |
| `dotnet test Wms.Tests` | `Backend/wms-api` |
| `dotnet test Wms.IntegrationTests` (Docker) | `Backend/wms-api` |
| `dotnet test --filter Category!=Integration` (sin Docker) | `Backend/wms-api` |
| `yarn test`, `yarn lint`, `yarn build`, `yarn dev` | `Frontend/wms` |

- **Reglas puras:** se extraen a clases puras y se prueban en `Wms.Tests`.
- **Lo que depende de EF, índices o transacciones:** se prueba en `Wms.IntegrationTests`.
- **`yarn lint`:** tiene errores heredados. La regla es no subir la cifra de la fase anterior y no tener ninguno en archivos nuevos.

## 8. Ambientes

- **Local:** API en `http://localhost:5281`; Postgres en el contenedor `wms-postgres-db` (puerto 5433). Las bases locales y sus usos están en `procesos/verificacion-local.md` §1.
- **Staging (AWS Lightsail):** frontend `https://app.100-60-89-139.sslip.io`, API `https://api.100-60-89-139.sslip.io/api/v1`. Runbook: `Backend/wms-api/deploy/staging/README.md`. Resumen: `procesos/despliegue-staging.md`.
- **Azure `test`:** pendiente de baja (`Backend/wms-api/infra/`, Terraform).
- **Usuarios de prueba por rol:** `Frontend/wms/README.md`. Credenciales de staging: `contexto/mapa-de-fuentes.md` §6. **No copies contraseñas a ningún documento.**

## 9. Datos y bases

- Las bases locales de prueba se recrean: nada de backfills ni conversiones de datos históricos.
- Staging tiene **datos migrados del legacy**. No se recrea ni se restaura sin un «sí» explícito del usuario, y no se escribe con SQL.
- Los datos reales del legacy solo viven en `db_legacy/trabajo/`, fuera de git.

## 10. Trampas conocidas

1. **`PERCENTAGE_OF_VALUE` no se multiplica por el stock.** Si marcas la fórmula prorrateada como «por cantidad», reintroduces el doble conteo.
2. **Esquema de parámetros y calculador pueden divergir.** El esquema sembrado de una fórmula y su calculador ya divergieron una vez (`PER_UOM`). Cotéjalos al tocar un calculador.
3. **IVA y retenciones.** Sin `ServiceTax` el IVA no se suma. `RETE_FUENTE` es una retención: no la sumes como IVA.
4. **Un 403 de un rol operativo** suele venir de un servicio compartido que otro módulo importa (`app/features/weighbridge`, `app/features/entries`), no de una llamada directa del módulo.
5. **`all=true`.** `pageSize > 50` se recorta sin avisar.
6. **Pantallas retiradas.** Antes de mejorar una pantalla, comprueba que una ronda anterior no la retiró. Pasó con la creación manual de facturas: su pantalla, `BillingPreviewPanel.vue` y `GetStorageInvoiceDraft` se eliminaron, y `Wms.Tests/Api/BillingControllerSurfaceTests.cs` impide que vuelvan.
7. **Componente y padre.** Verifica el componente y también quién lo instancia: las props declaradas no dicen qué le pasa el padre.
8. **Carencias del modelo.** No conviertas una carencia del modelo de datos en una prohibición de negocio.
9. **Nombres engañosos.** `ServiceRecord.CargoManifestNumber` es la carta porte, no el manifiesto.
10. **EF y Ids del dominio.** Una entidad nueva que EF descubre por la navegación de un padre rastreado queda `Modified` y el guardado falla con `DbUpdateConcurrencyException`. Usa `Set.Add(...)` o `ValueGeneratedNever()`.
11. **Navegaciones sin `Include`.** Un DTO en memoria con `AsNoTracking` que lee una navegación sin `Include` revienta (varios casos con `UnitMeasure.Name`).
12. **Suite de integración y cola de báscula.** La suite comparte base y la cola de báscula corta en 100 camiones: libera los camiones que abra una prueba.
13. **Mayúsculas en `/Volumes/Dock`.** El volumen distingue mayúsculas: `app/features/Administration` y `administration` conviven.
