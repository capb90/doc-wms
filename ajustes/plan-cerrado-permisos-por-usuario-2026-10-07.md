# Plan cerrado: permisos por usuario

> ## ⏸ Estado: DIFERIDO — no implementar todavía
>
> **Decisión del usuario (7 de octubre de 2026):** el sistema sale a producción con el **modelo de roles actual**. Este plan queda en el backlog para una versión posterior al corte (2.1 o siguiente).
>
> **Motivos:**
> - **No hubo solicitud del cliente.**
> - El cambio toca la autenticación de punta a punta, y obligaría a repetir buena parte del QA, que hoy está cerrado: 147 de 147 fichas verificadas, con el GO pendiente solo de PRF-002.
> - Invalidaría los videos, las guías y los scripts recién terminados.
> - Los operarios están probando en staging con el modelo de roles.
>
> **Antes de retomarlo,** aplica primero la sección **«§11. Correcciones pendientes antes de retomar»**, al final del documento. Este plan **no es ejecutable tal como está**.
>
> **Si mientras tanto aparece una necesidad puntual** (por ejemplo, que Facturación cree clientes), se resuelve con un ajuste chico a las reglas actuales de `WmsPolicyRoles`, sin este modelo. Ese ajuste respeta la regla de «sin retrocesos funcionales».

> **Fecha:** 7 de octubre de 2026.
> **Repositorios:** `Backend/wms-api` y `Frontend/wms`, ambos desde `develop`.
> **Análisis previo:** `code_workspace/ajustes/analisis-impacto-permisos-granulares-2026-10-07.md`.
> **Para quién:** el agente que lo implemente. Todo lo que hace falta decidir ya está decidido aquí. Si algo del código no coincide con este plan, detente y pregunta; no improvises.

---

## 0. Reglas para el agente

1. Lee primero `code_workspace/docs/contexto-negocio-wms-para-ia.md`. Sus §3 y §11 están desactualizados en cuanto a políticas; lo que diga este plan prevalece.
2. **Migraciones y base de datos: las opera el agente, solo con `dotnet ef`.** No se editan los archivos que genera `dotnet ef` (la migración, su `.Designer.cs` y `AppDbContextModelSnapshot.cs`). Solo se trabaja en la base **local**, nunca en staging ni en Azure. El procedimiento está en §7.2.
3. **Ramas y commits:** todo el trabajo va en una rama de git nueva, `feature/permisos-por-usuario`, creada desde `develop` en **cada** repositorio (backend y frontend). Nunca se trabaja en `develop` ni en `main`. **Los commits los hace el usuario:** el agente entrega el mensaje al cerrar cada fase y espera. El procedimiento está en §7.0.
4. **Textos:**
   - En español: la UI, los mensajes de error (con `BadRequestException`) y los comentarios de negocio.
   - En inglés: el código.
5. **Despliegue:** backend y frontend salen juntos. El contrato del login y de `/user/me` cambia y no hay compatibilidad hacia atrás.
6. **Pruebas:** al terminar cada fase deben pasar las del backend (`dotnet test`) y las del frontend (`npx vitest run`).

---

## 1. Decisiones

| N.º | Decisión | Fuente |
| --- | --- | --- |
| P01 | El permiso controla qué pantallas e ítems del menú ve el usuario. La API se protege con las reglas de acceso actuales, que ahora se deducen de los permisos. **No** se etiqueta cada operación de la API con su pantalla. | Usuario (7-oct, resp. 1) y confirmación del enfoque |
| P02 | Un usuario puede recibir pantallas de cualquier módulo. Ejemplo: Facturación con «Convenios» y «Crear y editar clientes». | Usuario (resp. 2) |
| P03 | Cada usuario se configura desde cero. Los roles dejan de decidir el acceso. Sirven una sola vez, para convertir a los usuarios que ya existen (P07). | Usuario (resp. 3 y 4) |
| P04 | El permiso es por pantalla. Las acciones que hoy dependen del rol dentro de una pantalla pasan a ser permisos aparte. Todo lo demás de una pantalla queda permitido a quien la ve. | Usuario (resp. 2 y 4) |
| P05 | Terceros se separa: ver por tipo (clientes, transportadoras, agencias de aduanas, todos) y crear o editar por tipo. Los convenios son un permiso aparte. | Usuario (resp. 3 y 4) |
| P06 | Las notificaciones las recibe quien tenga el permiso de la pantalla relacionada (tabla §5.8). | Usuario (resp. 5) |
| P07 | Al desplegar, cada usuario existente recibe, una sola vez, los permisos equivalentes a sus roles actuales (§3). Después se edita a mano. | Usuario (resp. 4) |
| P08 | El editor de permisos tiene un botón «Copiar permisos de otro usuario». | Usuario (resp. 4) |
| P09 | **Acceso total:** un indicador por usuario (`has_full_access`) que concede todos los permisos, incluidos los que se agreguen en el futuro. Reemplaza al rol Administrador: lo tienen el administrador inicial y quienes hoy son Admin. Las reglas de «último administrador» y de recuperación de contraseña pasan a depender de él. | Decisión del plan: sin él, cada permiso nuevo exigiría actualizar a mano a los administradores. |
| P10 | «Ver factura desde el ciclo» **no** es un permiso aparte: usa `billing.invoices`. El enlace lleva a esa pantalla; con un permiso propio el enlace podría terminar en «Acceso denegado». | Decisión del plan (ajusta la lista aceptada en la resp. 2) |
| P11 | Se agrega `stakeholders.all.manage` («Crear y editar todos los terceros»). Sin él, nadie podría crear importadores ni exportadores, que no son clientes, transportadoras ni agencias. | Decisión del plan (completa P05) |
| P12 | **Se reorganiza el menú.** Terceros y Reportes pasan a ser grupos de primer nivel, y cada pantalla aparece **una sola vez** (hoy terceros, inventario general y movimientos se repiten en varios grupos). | Decisión del plan: sin roles, los duplicados mostrarían la misma pantalla varias veces. |
| P13 | La regla `AdminOnly` se divide en una regla por área, y se crean reglas propias para las acciones que se pueden conceder fuera de su módulo (§5.4). Así, conceder una pantalla de Administración no abre la administración de usuarios ni los respaldos. | Decisión del plan |
| P14 | Las tablas `system_roles` y `AspNetUserRoles` y el enum `SystemRolesCode` **se conservan**. Solo los usan la conversión (P07) y los ayudantes de pruebas. Quitarlos queda fuera de alcance. | Decisión del plan |

**Fuera de alcance:**
- Proteger la API operación por operación con el permiso de cada pantalla.
- Editar roles.
- Borrar las tablas de roles.
- Cambiar el destino de los correos (siguen yendo a `Notifications:AdminEmails`).

---

## 2. Catálogo de permisos

**Tipos de permiso:**
- **Pantalla:** habilita uno o más ítems del menú y sus páginas.
- **Acción:** habilita un control dentro de una pantalla.

**«Implica»:** quien tenga el permiso de la izquierda recibe también el de la derecha. El backend lo agrega solo al guardar y el editor lo marca solo.

| Módulo (orden) | Código | Nombre en la UI | Tipo | Implica | Páginas o controles que habilita |
| --- | --- | --- | --- | --- | --- |
| General (1) | `dashboard.traceability` | Trazabilidad | Pantalla | — | `/`, búsqueda de placa en la barra superior, `/reports/statistics` (que sigue redirigiendo a `/`) |
| General | `dashboard.billing-summary` | Ver datos de facturación en trazabilidad y estadísticas | Acción | `dashboard.traceability` | Bloque de facturación en `TraceabilityStats` y en las estadísticas |
| Administración (2) | `admin.users` | Usuarios | Pantalla | — | `/admin/users`, `/admin/users/create`, `/admin/users/[id]`, `/admin/users/edit/[id]` |
| Administración | `admin.products` | Productos | Pantalla | — | `/admin/products`, `create`, `[id]`, `edit/[id]` |
| Administración | `admin.packaging-types` | Tipos de embalaje | Pantalla | — | `/admin/packaging-types` |
| Administración | `admin.unit-measures` | Unidades de medida | Pantalla | — | `/admin/unit-measures` |
| Administración | `admin.cargo-unit-types` | Tipos de unidad de carga | Pantalla | — | `/admin/cargo-unit-types` |
| Administración | `admin.services` | Servicios y tarifas base | Pantalla | — | `/admin/services`, `create`, `[id]`, `edit/[id]` |
| Administración | `admin.forklift-rates` | Tarifas de montacargas | Pantalla | — | `/admin/forklift-rates` |
| Administración | `admin.drivers` | Conductores | Pantalla | — | `/admin/drivers` |
| Administración | `admin.vehicles` | Vehículos | Pantalla | — | `/admin/vehicles` |
| Administración | `admin.entry-reasons` | Motivos de entrada | Pantalla | — | `/admin/entry-reasons` |
| Administración | `admin.locations` | Ubicaciones | Pantalla | — | `/admin/locations` |
| Administración | `admin.cities` | Ciudades | Pantalla | — | `/admin/cities` |
| Administración | `admin.crews` | Cuadrillas | Pantalla | — | `/admin/crews` |
| Administración | `admin.audit` | Auditoría | Pantalla | — | `/admin/audit`; enlace de auditoría en `DepositProductsTable` |
| Administración | `admin.parameters` | Parámetros del sistema | Pantalla | — | `/admin/parameters` (menú derecho) |
| Terceros (3) | `stakeholders.all.view` | Ver todos los terceros | Pantalla | — | `/admin/stakeholders` sin filtro y detalle de cualquier tercero |
| Terceros | `stakeholders.customers.view` | Ver clientes | Pantalla | — | `/admin/stakeholders?rol=CUSTOMER` y detalle de clientes |
| Terceros | `stakeholders.transport.view` | Ver transportadoras | Pantalla | — | `?rol=TRANSPORT_COMPANY` y detalle |
| Terceros | `stakeholders.customs.view` | Ver agencias de aduanas | Pantalla | — | `?rol=CUSTOMS_AGENCY` y detalle |
| Terceros | `stakeholders.all.manage` | Crear y editar todos los terceros | Pantalla | `stakeholders.all.view` | `/admin/stakeholders/create` y edición, con cualquier rol de negocio |
| Terceros | `stakeholders.customers.manage` | Crear y editar clientes | Pantalla | `stakeholders.customers.view` | Crear y editar con el rol `CUSTOMER` |
| Terceros | `stakeholders.transport.manage` | Crear y editar transportadoras | Pantalla | `stakeholders.transport.view` | Ídem con `TRANSPORT_COMPANY` |
| Terceros | `stakeholders.customs.manage` | Crear y editar agencias de aduanas | Pantalla | `stakeholders.customs.view` | Ídem con `CUSTOMS_AGENCY` |
| Terceros | `stakeholders.agreements` | Convenios (acuerdos) de clientes | Acción | `stakeholders.customers.view` | Sección de convenios en `/admin/stakeholders/[id]` |
| Vigilancia (4) | `gate.entry` | Ingreso | Pantalla | — | `/operations/entries` |
| Vigilancia | `gate.exit` | Salida | Pantalla | — | `/operations/entries/exits` |
| Vigilancia | `gate.history` | Historial de vigilancia | Pantalla | — | `/operations/entries/history`, incluida la corrección de ingresos |
| Báscula (5) | `weighbridge.dashboard` | Dashboard de báscula | Pantalla | — | `/operations/weighbridge/dashboard` |
| Báscula | `weighbridge.process` | Proceso de pesaje | Pantalla | — | `/operations/weighbridge`, `in-process`, `pending-reweigh`, `recover`; «Cerrar ciclo» en `cycles/[id]` |
| Báscula | `weighbridge.history` | Historial de báscula | Pantalla | — | `/operations/weighbridge/history` |
| Báscula | `weighbridge.reports` | Reportes de báscula | Pantalla | — | `/operations/weighbridge/reports` |
| Báscula | `weighbridge.correct-weights` | Corregir pesos | Acción | — | «Modificar» pesos en el historial y en `cycles/[id]` |
| Báscula | `weighbridge.change-date` | Cambiar fecha de pesaje | Acción | — | Cambiar fecha en el historial |
| Báscula | `weighbridge.void` | Anular pesaje | Acción | — | «Anular pesaje» en el historial y en `cycles/[id]` |
| Bodega (6) | `warehouse.dashboard` | Dashboard de bodega | Pantalla | — | `/warehouse` |
| Bodega | `warehouse.receptions.entry` | Ingresos a recepción | Pantalla | — | `/warehouse/receptions/entry` |
| Bodega | `warehouse.receptions` | Recepción | Pantalla | — | `/warehouse/receptions`, `receptions/[id]` |
| Bodega | `warehouse.receptions.history` | Historial de recepciones | Pantalla | — | `/warehouse/receptions/history`, `receptions/[id]` |
| Bodega | `warehouse.forklift` | Registrar uso de montacargas | Pantalla | — | `/warehouse/forklift` |
| Bodega | `warehouse.forklift.history` | Historial de montacargas | Pantalla | — | `/warehouse/forklift/history` |
| Bodega | `warehouse.loading-orders` | Órdenes de cargue (bodega) | Pantalla | — | `/warehouse/loading-orders`, `[id]` |
| Bodega | `warehouse.inventory` | Inventario | Pantalla | — | `/warehouse/inventory` |
| Bodega | `warehouse.novelties` | Novedades | Pantalla | — | `/warehouse/novelties` |
| Comercio exterior (7) | `foreign-trade.dashboard` | Dashboard de comercio exterior | Pantalla | — | `/foreign-trade` |
| Comercio exterior | `foreign-trade.deposits` | Depósitos | Pantalla | — | `/foreign-trade/deposits`; `imports`, `exports` e `inspections` (listados y `[id]`) |
| Comercio exterior | `foreign-trade.abandonment` | Abandono y prórrogas | Pantalla | — | `/foreign-trade/abandonment` |
| Comercio exterior | `foreign-trade.packing-lists` | Listas de empaque | Pantalla | — | `/foreign-trade/packing-lists` |
| Comercio exterior | `foreign-trade.releases` | Levantes | Pantalla | — | `/foreign-trade/releases` |
| Comercio exterior | `foreign-trade.loading-orders.create` | Crear orden de cargue | Pantalla | — | `/foreign-trade/loading-orders/create`, `[id]` |
| Comercio exterior | `foreign-trade.loading-orders` | Órdenes de cargue | Pantalla | — | `/foreign-trade/loading-orders`, `[id]` |
| Comercio exterior | `foreign-trade.dispatch-guides.create` | Generar guía de salida | Pantalla | — | `/foreign-trade/dispatch-guides/create` |
| Comercio exterior | `foreign-trade.dispatch-guides` | Historial de guías de salida | Pantalla | — | `/foreign-trade/dispatch-guides` |
| Comercio exterior | `foreign-trade.dispatch-guides.pending` | Guías pendientes | Pantalla | — | `/foreign-trade/dispatch-guides/pending` |
| Comercio exterior | `foreign-trade.inventory-adjustment` | Ajuste de inventario | Acción | `foreign-trade.deposits` | «Ajustar cantidad» en el detalle del depósito |
| Comercio exterior | `foreign-trade.deposit-entry-date` | Cambiar fecha de ingreso del depósito | Acción | — | «Editar fecha de ingreso» en el detalle del depósito y en `cycles/[id]` |
| Facturación (8) | `billing.dashboard` | Dashboard de facturación | Pantalla | — | `/billing` |
| Facturación | `billing.invoices` | Facturas | Pantalla | — | `/billing/invoices`, `[id]`; enlace «Ver factura» del ciclo |
| Facturación | `billing.pending-deposits` | Depósitos pendientes | Pantalla | — | `/billing/pending-deposits` |
| Facturación | `billing.payments` | Pagos | Pantalla | — | `/billing/payments` |
| Facturación | `billing.configurations` | Configuraciones de facturación | Pantalla | — | `/billing/configurations` |
| Facturación | `billing.reports.annual` | Facturación anual | Pantalla | — | `/billing/reports/annual` |
| Facturación | `billing.reports.deposit-billing` | Facturación por CPI | Pantalla | — | `/billing/reports/deposit-billing` |
| Reportes (9) | `reports.warehouse-movements` | Movimientos por depósito | Pantalla | — | `/reports/warehouse-movements` |
| Reportes | `reports.daily-incoming` | Mercancías ingresadas (diario) | Pantalla | — | `/reports/daily-incoming-goods` |
| Reportes | `reports.daily-outgoing` | Salida de mercancía (diario) | Pantalla | — | `/reports/daily-outgoing-goods` |
| Reportes | `reports.abandonment-candidates` | Mercancía en abandono | Pantalla | — | `/reports/abandonment-candidates` |
| Reportes | `reports.abandonment-exits` | Salidas a destino de abandono | Pantalla | — | `/reports/abandonment-exits` |
| Reportes | `reports.general-inventory` | Inventario general | Pantalla | — | `/reports/general-inventory` |
| Reportes | `reports.policies` | Informe de póliza | Pantalla | — | `/reports/policies` |
| Reportes | `reports.incoming-by-product` | Ingresos por producto | Pantalla | — | `/reports/incoming-by-product` |
| Reportes | `reports.customs-agency-entries` | Ingresos por agencia de aduanas | Pantalla | — | `/reports/customs-agency-entries` |

En total son **73 permisos**: 66 de pantalla y 7 de acción.

**Sin permiso, para cualquier usuario autenticado:** `/notifications`, `/access-denied`, `/auth/change-password`.

**Para mostrar las acciones debajo de su pantalla en el editor:** cada acción tiene un padre. Es solo visual, no implica nada salvo lo indicado en la columna «Implica».

| Acción | Se muestra debajo de |
| --- | --- |
| `dashboard.billing-summary` | `dashboard.traceability` |
| `stakeholders.agreements` | `stakeholders.customers.view` |
| `weighbridge.correct-weights`, `weighbridge.change-date`, `weighbridge.void` | `weighbridge.history` |
| `foreign-trade.inventory-adjustment` | `foreign-trade.deposits` |
| `foreign-trade.deposit-entry-date` | `foreign-trade.deposits` |

---

## 3. Conversión de los usuarios existentes

Esta tabla vale para la conversión inicial (P07) y para los ayudantes de pruebas (§5.10). Reproduce el acceso de hoy: las páginas por `requiredRoles` y los controles internos por rol.

Si un usuario tiene varios roles, recibe la unión de sus permisos.

| Rol | Resultado |
| --- | --- |
| `Admin` | `has_full_access = true`, sin filas en `user_permissions` |
| `Receiving` | `gate.entry`, `gate.exit`, `gate.history` |
| `Scale` | `weighbridge.dashboard`, `weighbridge.process`, `weighbridge.history`, `weighbridge.reports`, `weighbridge.correct-weights`, `weighbridge.change-date`, `weighbridge.void`, `foreign-trade.deposit-entry-date` |
| `Warehouse` | Las 9 de Bodega, `reports.general-inventory`, `reports.warehouse-movements` |
| `ForeignTrade` | `dashboard.traceability`; las 10 pantallas de Comercio exterior; `foreign-trade.inventory-adjustment`; `foreign-trade.deposit-entry-date`; las 9 de Reportes; los 8 permisos de Terceros **excepto** `stakeholders.agreements` |
| `Billing` | Las 7 de Facturación, `reports.general-inventory`, `reports.warehouse-movements`, `stakeholders.all.view`, `stakeholders.customers.view`, `stakeholders.agreements`, `weighbridge.correct-weights` |

En `Billing`, `stakeholders.all.view` está porque hoy Facturación entra al listado completo de terceros.

---

## 4. Cambios de comportamiento intencionales

Se listan para que nadie los tome por regresiones. Cada uno tiene su prueba.

1. **Acceso total recibe todas las notificaciones guardadas.** Antes, el Admin solo recibía las dirigidas a Admin. Es consecuencia de P06 y P09.
2. **Las notificaciones que antes iban a Admin van a quien tenga `admin.audit`.** La de respaldo fallido va a quien tenga `admin.parameters`.
3. **Facturación pierde en la API la edición de servicios y de tarifas de montacargas.** Hoy no tenía pantalla para eso; ahora requiere `admin.services` o `admin.forklift-rates`.
4. **Cambia el menú (P12):**
   - Facturación ve «Terceros › Listado» y «Reportes › Movimientos por depósito», a los que ya tenía acceso por URL.
   - Bodega ve «Reportes › Movimientos por depósito».
   - Desaparecen los duplicados.
5. **«Editar fecha de ingreso» en el detalle del depósito** se muestra solo con `foreign-trade.deposit-entry-date`. Hoy no tiene control en la UI.
6. **El correo de recuperación de contraseña** se envía solo a usuarios activos con acceso total. Hoy se envía a los Admin.
7. **Los grupos `role:{code}` de SignalR desaparecen.** Los avisos en tiempo real van a `user:{id}`.

**Limitaciones aceptadas** (P01). Documéntalas en el `README` del frontend (F7):
- Una pantalla de un módulo habilita en la API todo lo que cubre la regla de ese módulo. Por ejemplo, `foreign-trade.releases` habilita las 84 operaciones de `ForeignTradeAccess`.
- El filtro de terceros por tipo es solo de interfaz: `GET /stakeholder` sigue abierta a cualquier usuario autenticado.
- Un cambio de permisos tarda hasta 15 s en aplicarse en otra instancia de la API. La caché es por proceso, igual que la de `UserSessionGuard`.

---

## 5. Backend (`Backend/wms-api`)

### 5.1 Cambios de esquema

Los genera el agente en la fase B1 con `dotnet ef migrations add AddUserPermissions` (§7.2).

| Tabla | Columna | Tipo | Notas |
| --- | --- | --- | --- |
| `permissions` (nueva) | `id` | uuid PK | Fijos, en `PermissionIds` (como `RoleIds`) |
| | `code` | varchar(100), único | p. ej. `billing.invoices` |
| | `module` | varchar(50) | `general`, `admin`, `stakeholders`, `gate`, `weighbridge`, `warehouse`, `foreign-trade`, `billing`, `reports` |
| | `name` | varchar(150) | Nombre en español (§2) |
| | `kind` | varchar(20) | `Screen` o `Action` (enum `PermissionKind`, guardado como texto) |
| | `parent_code` | varchar(100) null | Solo para la vista (§2) |
| | `implies_code` | varchar(100) null | §2 |
| | `sort_order` | int | Orden dentro del módulo, el de la tabla §2 |
| | `is_active` | bool, default true | |
| `user_permissions` (nueva) | `user_id` | uuid FK → `users`, cascade | PK compuesta (`user_id`, `permission_id`) |
| | `permission_id` | uuid FK → `permissions`, restrict | Índice por `permission_id` |
| | `granted_at` | timestamptz | `DateTimeOffset.UtcNow` |
| | `granted_by_id` | uuid null FK → `users`, set null | |
| `users` | `has_full_access` | bool not null default false | P09 |
| | `permissions_initialized_at` | timestamptz null | Marca la conversión (§5.9) |

El `HasData` siembra las 73 filas de `permissions`.

### 5.2 Dominio (`Wms.Domain`)

| Archivo | Contenido |
| --- | --- |
| `Entities/Users/Permission.cs` (nuevo) | Entidad: `Id`, `Code`, `Module`, `Name`, `Kind`, `ParentCode`, `ImpliesCode`, `SortOrder`, `IsActive` |
| `Entities/Users/UserPermission.cs` (nuevo) | Entidad: `UserId`, `PermissionId`, `GrantedAt`, `GrantedById`; navegaciones `User` y `Permission` |
| `Enums/PermissionKind.cs` (nuevo) | `Screen`, `Action` |
| `Entities/Users/ApplicationUser.cs` | Agregar `HasFullAccess` (bool), `PermissionsInitializedAt` (`DateTimeOffset?`) y la colección `Permissions` (`ICollection<UserPermission>`). Métodos `GrantFullAccess()`, `RevokeFullAccess()` y `MarkPermissionsInitialized(DateTimeOffset)`. |
| `Security/WmsPermissions.cs` (nuevo) | Fuente única del catálogo: constantes de código (`public const string BillingInvoices = "billing.invoices";` …), `Modules` (código, nombre, orden) y `Catalog` (lista de `PermissionDefinition(Code, Module, Name, Kind, ParentCode, ImpliesCode, SortOrder)`) con las 73 filas de §2. |
| `Security/PermissionImplications.cs` (nuevo) | `Normalize(IEnumerable<string> codes) → IReadOnlySet<string>`: agrega los implicados en cascada. Pura y probada. |
| `Security/WmsPolicyRoles.cs` | **Se renombra a `WmsPolicies.cs`** (clase `WmsPolicies`). Contiene las constantes de las 33 reglas por permiso y de `ActiveUser`, y el diccionario `Permissions: IReadOnlyDictionary<string, IReadOnlyList<string>>` con la tabla §5.4. `ActiveUser` sigue fuera del diccionario. |
| `Security/RolePermissionPresets.cs` (nuevo) | `For(SystemRolesCode role) → (bool FullAccess, IReadOnlyList<string> Permissions)` con la tabla §3, y `ForRoles(IEnumerable<SystemRolesCode>)` (unión). |
| `Services/IUserPermissionStore.cs` (nuevo) | Ver §5.3 |
| `Contracts/WmsClaimTypes.cs` | Sin cambios |

### 5.3 Infraestructura (`Wms.Infrastructure`)

**Configuraciones** en `Persistence/Configurations/Users/`:
- `PermissionConfiguration.cs`: tabla `permissions`, índice único por `code`, `kind` como texto.
- `UserPermissionConfiguration.cs`: tabla `user_permissions`, PK compuesta y las FK de §5.1.
- `ApplicationUserConfiguration.cs`: las dos columnas nuevas.

**Datos sembrados:**
- `Persistence/SeedDataExtensions.cs`: agregar `SeedPermissions(modelBuilder)`, que recorre `WmsPermissions.Catalog` con `PermissionIds` fijos. Escribe los 73 GUID como constantes una sola vez; no los generes en tiempo de ejecución.
- Llamarlo desde `AppDbContext.OnModelCreating`, junto a `SeedApplicationRoles`.

**`AppDbContext`:** agregar `DbSet<Permission> Permissions` y `DbSet<UserPermission> UserPermissions`.

**`Services/UserPermissionStore.cs`** (nuevo), que implementa `IUserPermissionStore`:
```csharp
public sealed record EffectivePermissions(bool HasFullAccess, IReadOnlySet<string> Codes);

public interface IUserPermissionStore
{
    Task<EffectivePermissions> GetAsync(Guid userId, CancellationToken ct = default);   // con caché
    Task<IReadOnlyList<Guid>> GetActiveUserIdsWithPermissionAsync(string code, CancellationToken ct = default); // sin caché
    void Invalidate(Guid userId);
}
```
- **`GetAsync`:**
  - Caché `IMemoryCache` de 15 s con la clave `user-permissions:{userId}`, igual que `UserSessionGuard`.
  - Con `HasFullAccess`, `Codes` son todos los códigos activos del catálogo.
  - Si el usuario no existe, devuelve `(false, vacío)`.
- **`GetActiveUserIdsWithPermissionAsync`:** usuarios con `IsActive` y que cumplen `has_full_access` **o** tienen una fila del código pedido.
- **Registro:** como scoped en `DependencyInjection` de Infrastructure, junto a `UserSessionGuard`.

### 5.4 Autorización por permiso (`Wms.Api`)

**Archivos:**
- `Common/Identity/PermissionRequirement.cs` (nuevo): `IAuthorizationRequirement` con `IReadOnlyCollection<string> Permissions`.
- `Common/Identity/PermissionAuthorizationHandler.cs` (nuevo): `AuthorizationHandler<PermissionRequirement>`. Obtiene el `userId` de `ClaimTypes.NameIdentifier` y llama a `IUserPermissionStore.GetAsync`. Da `Succeed` si hay acceso total o si el usuario tiene **alguno** de los permisos. Se registra como scoped.
- `Common/Identity/WmsAuthentication.cs`:
  - Reemplazar el bucle de `WmsPolicyRoles.Roles` por uno sobre `WmsPolicies.Permissions`, que haga `options.AddPolicy(policy, b => b.RequireAuthenticatedUser().AddRequirements(new PermissionRequirement(perms)))`.
  - Conservar `ActiveUser`.
  - Quitar `RoleClaimType`.
  - Actualizar el comentario CHG-03.

**Tabla de reglas → permisos** (`WmsPolicies.Permissions`). Una regla se cumple si el usuario tiene **alguno** de sus permisos, o si tiene acceso total.

| Regla | Permisos que la cumplen | Dónde se usa |
| --- | --- | --- |
| `UserAdministration` | `admin.users` | `UserController`: las 8 acciones que hoy son `AdminOnly` |
| `SystemAdministration` | `admin.parameters` | `BackupsController` (clase), `LegacyImportController` (clase), parámetros del sistema (3 acciones de `AdministrationController`) |
| `AuditLogAccess` | `admin.audit` | `AdministrationController.GetAuditLogs` |
| `PackagingTypeAdministration` | `admin.packaging-types` | `UpdatePackagingType`, `DeletePackagingType` |
| `UnitMeasureAdministration` | `admin.unit-measures` | `Create`, `Update`, `DeleteUnitMeasure` |
| `CargoUnitTypeAdministration` | `admin.cargo-unit-types` | `Create`, `Update`, `DeleteCargoUnitType` |
| `CityAdministration` | `admin.cities` | `CitiesController`: Create, Update, Delete, Import |
| `CrewAdministration` | `admin.crews` | `CrewsController`: Create, Update, Delete |
| `EntryReasonAdministration` | `admin.entry-reasons` | `EntryReasonController`: Create, Update, Delete |
| `ProductAdministration` | `admin.products` | `ProductController`: CreateProduct, UpdateProduct |
| `LocationAdministration` | `admin.locations` | `WarehouseLocationsController` (nuevo): POST, PATCH, DELETE |
| `LocationReadAccess` | `admin.locations` y las 9 de Bodega | `WarehouseLocationsController`: GET `warehouse/locations` |
| `ServiceCatalogAccess` | `admin.services` | `ServiceController`: las 15 escrituras que hoy son `BillingAccess` |
| `ForkliftRateAccess` | `admin.forklift-rates` | `ForkliftRateController`: GetForkliftRates, UpsertForkliftRate |
| `AgreementAccess` | `stakeholders.agreements` | `StakeholderController`: las 9 escrituras de convenios que hoy son `BillingAccess` |
| `StakeholderAccess` | `stakeholders.all.manage`, `stakeholders.customers.manage`, `stakeholders.transport.manage`, `stakeholders.customs.manage` | Sin cambio de atributos |
| `TransportCatalogAccess` | `gate.entry`, `weighbridge.process`, `foreign-trade.loading-orders.create`, `admin.drivers`, `admin.vehicles` | Sin cambio de atributos |
| `OperationalAccess` | `gate.entry`, `weighbridge.process`, `warehouse.receptions`, `admin.packaging-types`, `admin.products` | Sin cambio de atributos |
| `GateAccess` | `gate.entry`, `gate.exit`, `gate.history` | Sin cambio |
| `EntryCorrectionAccess` | `gate.history` | Sin cambio |
| `ScaleAccess` | `weighbridge.dashboard`, `weighbridge.process`, `weighbridge.history`, `weighbridge.reports` | Sin cambio, salvo lo que se mueve a las dos reglas siguientes |
| `WeighingCorrectionAccess` | `weighbridge.correct-weights` | Sin cambio |
| `WeighingDateCorrectionAccess` | `weighbridge.change-date` | `WeighbridgeDateCorrectionController` (nuevo): PATCH `weighbridge/{id}/weighing-date` |
| `WeighingVoidAccess` | `weighbridge.void` | `WeighbridgeVoidController` (cambia la regla de la clase) |
| `DepositEntryDateAccess` | `foreign-trade.deposit-entry-date` | Sin cambio |
| `WarehouseAccess` | las 9 de Bodega | Sin cambio, salvo ubicaciones, que se mueven |
| `NoveltyReadAccess` | `warehouse.novelties`, `foreign-trade.deposits`, `reports.customs-agency-entries` | Sin cambio |
| `InventoryReportAccess` | `reports.general-inventory`, `reports.warehouse-movements` | Sin cambio |
| `ForeignTradeAccess` | las 10 pantallas de Comercio exterior; `reports.daily-incoming`, `reports.daily-outgoing`, `reports.abandonment-candidates`, `reports.abandonment-exits`, `reports.policies`, `reports.incoming-by-product`, `reports.customs-agency-entries` | Sin cambio, salvo trazabilidad y estadísticas, que se mueven |
| `InventoryAdjustmentAccess` | `foreign-trade.inventory-adjustment` | `InventoryAdjustmentController` (cambia la regla de la clase) |
| `TraceabilityAccess` | `dashboard.traceability` | `TraceabilityReportsController` (nuevo): GET `reports/traceability`, GET `reports/statistics` |
| `BillingAccess` | las 7 de Facturación | Sin cambio, salvo el dashboard, que se mueve |
| `BillingSummaryAccess` | `billing.dashboard`, `dashboard.billing-summary` | `BillingDashboardController` (nuevo): GET `billing/dashboard/summary`, GET `billing/dashboard/overdue` |
| `ActiveUser` | cualquier usuario autenticado | Sin cambio |

`AdminOnly` **desaparece**. Cuando termines, ningún controlador debe referenciarlo.

**Controladores nuevos (los «partidos»):**
- Mantienen la **misma ruta y el mismo verbo**, para que el frontend no cambie de URL.
- Llevan un comentario `/// <summary>` que explica el motivo, como los partidos existentes.
- **Mueve** la acción completa (atributos, documentación y respuesta). No dejes copias.

| Controlador nuevo | `[Route]` | Acciones que recibe | Origen |
| --- | --- | --- | --- |
| `WarehouseLocationsController` | `warehouse` | `GetWarehouseLocations` (`LocationReadAccess`), `CreateWarehouseLocation`, `UpdateWarehouseLocation`, `DeleteWarehouseLocation` (`LocationAdministration`) | `WarehouseController.cs:900-950` |
| `WeighbridgeDateCorrectionController` | `weighbridge` | `ModifyWeighingDate` (`WeighingDateCorrectionAccess`) | `WeighbridgeController.cs:885` |
| `TraceabilityReportsController` | `reports` | `GetTraceabilityDashboard`, `GetOperationalStatistics` (`TraceabilityAccess`) | `ReportController.cs:36`, `:157` |
| `BillingDashboardController` | `billing` | `GetDashboardSummary`, `GetOverdueClients` (`BillingSummaryAccess`) | `BillingController.cs:609`, `:623` |

**Atributos que cambian** (el texto de la regla va como literal, igual que hoy):
- `UserController`, `AdministrationController`, `CitiesController`, `CrewsController`, `EntryReasonController` y `ProductController`: cada `AdminOnly` pasa a la regla de su área, según la tabla.
- `BackupsController` y `LegacyImportController`: la clase pasa a `SystemAdministration`.
- `ServiceController`: cada `BillingAccess` de acción pasa a `ServiceCatalogAccess`.
- `ForkliftRateController`: cada `BillingAccess` de acción pasa a `ForkliftRateAccess`.
- `StakeholderController`: cada `BillingAccess` de acción (convenios) pasa a `AgreementAccess`.
- `WeighbridgeVoidController`: la clase pasa a `WeighingVoidAccess`.
- `InventoryAdjustmentController`: la clase pasa a `InventoryAdjustmentAccess`.

**Hub:** en `Hubs/NotificationHub.cs`, borra el bucle de grupos `role:{role}` (líneas 28-32). El grupo `user:{id}` se queda.

### 5.5 Token, login y `/user/me`

| Archivo | Cambio |
| --- | --- |
| `Wms.Domain/Services/ITokenService.cs` y `Wms.Infrastructure/Services/TokenService.cs` | `GenerateJwtToken(ApplicationUser user)`, sin `roleCodes`. Ya no emite `ClaimTypes.Role`. |
| `Wms.Application/Auth/Commands/Login/LoginHandler.cs` | Quitar la búsqueda de roles (líneas 48-55). Obtener `EffectivePermissions` con `IUserPermissionStore.GetAsync`. |
| `Wms.Application/Auth/Commands/RefreshToken/RefreshTokenHandler.cs` | Quitar la búsqueda de roles (líneas 51-58). |
| `Wms.Application/Auth/Common/Dtos/UserInfoDto.cs` | `(Guid Id, string Username, string Email, string Name, IReadOnlyList<string> Permissions, bool HasFullAccess, bool MustChangePassword)`. Ya no tiene `Roles`. `Permissions` son los **efectivos**, ordenados alfabéticamente. |
| `Wms.Application/Users/Common/Dtos/UserDto.cs` y `Mappers/UserMapper.cs` | Reemplazar `Roles` por `HasFullAccess` y `Permissions` (códigos). `GET /user/me` y `GET /user/{id}` llenan `Permissions` con los efectivos. `GET /user` (listado) devuelve `Permissions = []` y llena solo `HasFullAccess`. |
| `Users/Queries/GetUsers/GetUsersHandler.cs` | Quitar el join con `context.UserRoles` (líneas 65-80) y proyectar `HasFullAccess`. |

### 5.6 Administración de usuarios

**Endpoints nuevos:**

| Endpoint | Regla | Comando o consulta (nuevos) |
| --- | --- | --- |
| `GET administration/permissions` | `UserAdministration` | `GetPermissionCatalogQuery`. Devuelve `[{ module, moduleName, order, permissions: [{ code, name, kind, parentCode, impliesCode, sortOrder }] }]`, solo con los activos y ordenado. Va en `AdministrationController`. |
| `GET user/{id}/permissions` | `UserAdministration` | `GetUserPermissionsQuery`. Devuelve `{ hasFullAccess, permissions: string[] }` con los **guardados**, no los efectivos. |
| `PUT user/{id}/permissions` | `UserAdministration` | `SetUserPermissionsCommand(UserId, HasFullAccess, Permissions, ActingUserId)`. `ActingUserId` sale del token. Reemplaza el conjunto completo. |

**Pasos de `SetUserPermissionsCommandHandler`, en orden:**

1. **Normalizar y validar los códigos.**
   - Pasar los códigos por `PermissionImplications.Normalize`.
   - Si un código no existe o está inactivo: `BadRequestException("El permiso «{code}» no existe.")`.
2. **Aplicar las reglas puras** de `UserAdministrationRules` (reescrita, ver abajo):
   - `EnsureHasAccess(hasFullAccess, codes)`: si no hay acceso total y ningún código es de tipo `Screen`, lanza `"Seleccione al menos una pantalla o active el acceso total."`
   - `EnsureCanChangeFullAccess(actorHasFullAccess, actorId, targetId, currentFull, newFull)`:
     - Si el valor cambia y el actor no tiene acceso total: `"Solo un usuario con acceso total puede cambiar el acceso total."`
     - Si `actorId == targetId` y se pasa de `true` a `false`: `"No puede quitarse a sí mismo el acceso total."`
   - `EnsureCanKeepUserAdministration(actorId, targetId, actorHasFullAccess, newCodes)`: si `actorId == targetId`, el actor no tiene acceso total y `admin.users` no está en `newCodes`, lanza `"No puede quitarse a sí mismo el permiso de Usuarios."`
   - Si `currentFull && !newFull`: `EnsureFullAccessRemains(countAfter)`. Si `countAfter < 1`, lanza `"Debe quedar al menos un usuario activo con acceso total."` El conteo lo hace `ActiveFullAccessCounter` (reemplaza a `ActiveAdminCounter`).
3. **Guardar y cerrar la sesión del usuario.**
   - Abrir una transacción.
   - Borrar y volver a crear las filas de `user_permissions` (`granted_by_id` = actor).
   - Actualizar `has_full_access` y `permissions_initialized_at` (si estaba nulo).
   - `userManager.UpdateSecurityStampAsync`.
   - `sessionGuard.Invalidate(userId)` y `permissionStore.Invalidate(userId)`.
4. **Auditar** (patrón CHG-68). Envolver el guardado en:
   ```
   auditContext.Describe($"Permisos actualizados para {userName}: acceso total {Sí|No}; agregados [{códigos}]; retirados [{códigos}]")
   ```

**Endpoints que cambian:**

| Endpoint | Cambio |
| --- | --- |
| `POST user` | `CreateUserWithRolesCommand` pasa a `CreateUserWithPermissionsCommand(Name, Username, IdentificationNumber, Password, Email, Phone, bool HasFullAccess, List<string> Permissions)`. JSON: `hasFullAccess`, `permissions`. Normaliza, valida `EnsureHasAccess` y aplica `EnsureCanChangeFullAccess` con `currentFull=false`. Guarda en la misma transacción y marca `permissions_initialized_at`. Audita con `Describe("Usuario creado con permisos: …")`, lo que cierra el hueco de CHG-68. Renombrar la carpeta `Users/Commands/CreateUserWithRoles` a `CreateUserWithPermissions` y adaptar el validador: lista no nula y sin elementos vacíos. |
| `POST user/{id}/manage-active` | En `ManageUserActivationHandler`, `ActiveAdminCounter` pasa a `ActiveFullAccessCounter`. El mensaje cambia a `"Debe quedar al menos un usuario activo con acceso total."` |
| `POST user/{id}/assign-roles` y `remove-roles` | **Se eliminan**, con sus comandos `AssignRolesToUser` y `RemoveRolesToUser`, DTOs, validadores y pruebas. |

**`UserAdministrationRules` reescrita:**
- Conserva `EnsureCanDeactivate`.
- Agrega las cuatro reglas de arriba.
- Borra `MustKeepOneRoleMessage`, `CannotRemoveOwnAdminMessage` y `EnsureCanRemoveRoles`.

**`ActiveAdminCounter` pasa a `ActiveFullAccessCounter`:**
- `CountAsync`: usuarios activos con `HasFullAccess`.
- `HasFullAccessAsync(userId)`.

### 5.7 Reglas en código

| Archivo | Cambio |
| --- | --- |
| `Wms.Application/Reports/Common/StatisticsVisibility.cs` | `IncludesBilling(EffectivePermissions p) => p.HasFullAccess \|\| p.Codes.Contains(WmsPermissions.DashboardBillingSummary)` |
| `TraceabilityReportsController.GetOperationalStatistics` | Obtiene los permisos con `IUserPermissionStore`, no con los claims de rol |
| `Wms.Application/Auth/Common/PasswordResetEligibility.cs` | El parámetro `isAdmin` pasa a `hasFullAccess`. El motivo del log dice `"el usuario no tiene acceso total"`. |
| `RequestPasswordResetHandler.cs:25-37` | Lee `user.HasFullAccess` en lugar de buscar el rol Admin |
| `Wms.Api/Common/Identity/BootstrapAdminSeeder.cs` | Al crear, `GrantFullAccess()` y `MarkPermissionsInitialized(UtcNow)`. Si el usuario ya existe, asegura `HasFullAccess = true` en lugar del rol Admin (líneas 51-59). **Sigue** asignando el rol Admin, para que la conversión (§5.9) tenga datos coherentes. |

### 5.8 Notificaciones

**Interfaces:**
- `INotificationOrchestrator.NotifyRoleAsync(string roleCode, …)` pasa a `NotifyPermissionAsync(string permissionCode, …)`.
- `IRealtimeNotifier.SendToRoleAsync` pasa a `SendToPermissionAsync(string permissionCode, NotificationDto, ct)`.
- Las dos implementaciones (`Wms.Api/Services/NotificationOrchestrator.cs` y `SignalRNotifier.cs`) resuelven los destinatarios con `IUserPermissionStore.GetActiveUserIdsWithPermissionAsync` y envían a `user:{id}`.
- **Correo:**
  - `INotificationService.NotifyRoleAsync` (`Wms.Domain/Services/INotificationService.cs:104`) pasa a `NotifyAudienceAsync(string audienceName, …)`.
  - El orquestador le pasa el `name` del permiso.
  - El correo sigue yendo a `Notifications:AdminEmails`. Solo cambia la etiqueta del asunto y del cuerpo.

**Llamada por llamada.** Todos los archivos están bajo `Wms.Application/`.

| Archivo:línea | Aviso | Antes | Ahora |
| --- | --- | --- | --- |
| `Warehouse/Commands/Reception/CreateReceptionWithoutWeighbridgeCommandHandler.cs:323` | Ingreso manual sin báscula | Admin | `admin.audit` |
| `Warehouse/Commands/LoadingOrder/ExecuteLoadingOrderCommandHandler.cs:369` | Cargue completado | Admin | `admin.audit` |
| `ExecuteLoadingOrderCommandHandler.cs:386` | Guía de salida requerida | ForeignTrade | `foreign-trade.dispatch-guides.pending` |
| `Warehouse/Commands/Reception/ReceptionDeclaredDifference.cs:169` | Diferencia de recepción | ForeignTrade | `foreign-trade.deposits` |
| `Warehouse/Commands/LoadingOrder/CancelLoadingOrder/CancelLoadingOrderHandler.cs:57` | Orden de cargue cancelada | Warehouse | `warehouse.loading-orders` |
| `Warehouse/Novelties/Common/WarehouseNoveltyService.cs:52` | Novedad en mercancía | ForeignTrade | `foreign-trade.deposits` |
| `Administration/Backups/Common/BackupService.cs:272` | Falló el respaldo | Admin | `admin.parameters` |
| `Weighbridge/Commands/ModifyFirstWeight/ModifyFirstWeightHandler.cs:86` | Modificación de peso | Admin | `admin.audit` |
| `Weighbridge/Commands/ModifySecondWeight/ModifySecondWeightHandler.cs:90` | Modificación de peso | Admin | `admin.audit` |
| `Weighbridge/Commands/ModifyWeighingDate/ModifyWeighingDateHandler.cs:86` | Modificación de fecha de pesaje | Admin | `admin.audit` |
| `Weighbridge/Commands/Storage/Initiate/InitiateStorageWeighingHandler.cs:714`, `:846`, `:1231` | Nuevo depósito de importación / Producto creado desde báscula / Nuevo depósito adicional | ForeignTrade | `foreign-trade.deposits` |
| `Weighbridge/Commands/VoidWeighing/VoidWeighingCommandHandler.cs:379` | Pesaje anulado | ForeignTrade | `foreign-trade.deposits` |
| `ForeignTrade/PackingLists/Commands/ImportPackingList/ImportPackingListCommandHandler.cs:129` | Productos creados desde lista de empaque | ForeignTrade | `foreign-trade.packing-lists` |
| `ForeignTrade/Common/Services/WarehouseStorageCancellationService.cs:221` | Depósito anulado (orden en cargue) | Warehouse | `warehouse.loading-orders` |
| `WarehouseStorageCancellationService.cs:252` | Avisos de `DepositCancellationNotices` | (rol del aviso) | (permiso del aviso, ver abajo) |
| `ForeignTrade/Commands/UpdateLoadingOrderItems/UpdateLoadingOrderItemsCommandHandler.cs:128` | Orden de cargue modificada | Warehouse | `warehouse.loading-orders` |
| `ForeignTrade/Commands/WithdrawImportRelease/WithdrawImportReleaseCommandHandler.cs:98` | Depósito sin nacionalizar | ForeignTrade | `foreign-trade.releases` |
| `ForeignTrade/Commands/ValidateDeposit/ValidateDepositCommandHandler.cs:79` | Discrepancia en validación | Admin | `admin.audit` |
| `ForeignTrade/Jobs/AbandonmentAlertService.cs:62` | Depósitos en ventana de abandono | ForeignTrade | `foreign-trade.abandonment` |
| `ForeignTrade/Commands/RevertLoadingOrder/RevertLoadingOrderCommandHandler.cs:175` | Salida revertida | Warehouse | `warehouse.loading-orders` |
| `Billing/Common/Services/StorageBillingNotifier.cs:28` | No se pudo facturar el almacenamiento | Billing | `billing.pending-deposits` |
| `StorageBillingNotifier.cs:62` | Almacenamiento facturado con valor mínimo | Billing | `billing.invoices` |
| `StorageBillingNotifier.cs:97` | Almacenamiento renovado | Billing | `billing.pending-deposits` |
| `StorageBillingNotifier.cs:141` | Fecha de ingreso del depósito modificada | Billing | `billing.invoices` |
| `StorageBillingNotifier.cs:209` | Factura actualizada (título variable) | Billing | `billing.invoices` |
| `StorageBillingNotifier.cs:243` | Almacenamiento con TRM pendiente | Billing | `billing.pending-deposits` |
| `Billing/Common/Services/StorageRecalculationTrigger.cs:63` | Camión adicional confirmado | ForeignTrade | `foreign-trade.deposits` |
| `Billing/Common/Services/InvoiceCancellationPolicy.cs:105` | Factura para revisar por anulación | Billing | `billing.invoices` |
| `Billing/Commands/CancelInvoice/CancelInvoiceHandler.cs:70` | Factura anulada | Billing | `billing.invoices` |
| `Billing/Jobs/BillingJobService.cs:316` | Factura próxima a vencer (con correo) | Billing | `billing.invoices` |

**`DepositCancellationNotices.cs`:**
- El campo `SystemRolesCode Role` del record pasa a `string PermissionCode`.
- El aviso a Bodega usa `warehouse.inventory`.
- El de Facturación usa `billing.invoices`.
- Hay que actualizar `DepositCancellationNoticesTests`.

**Avisos solo en tiempo real:**

| Archivo:línea | Antes | Ahora |
| --- | --- | --- |
| `Common/Notifications/TraceabilityNotification.cs` | `Roles = [Admin, ForeignTrade]` | `Permission = WmsPermissions.DashboardTraceability`. `PublishAsync` llama una vez a `SendToPermissionAsync`. |
| `Weighbridge/Commands/Common/RecordWeighing/RecordWeighingHandler.cs:585-586`, `:602-603` | `"Admin"`, `"ForeignTrade"` | Una llamada con `dashboard.traceability` |
| `Weighbridge/Commands/Common/CompleteCycle/CompleteCycleHandler.cs:306-307` | `"Admin"`, `"ForeignTrade"` | Una llamada con `dashboard.traceability` |
| `Weighbridge/Commands/Storage/GenerateGlobalGuide/GenerateGlobalDispatchGuideHandler.cs:112-113` | `"Admin"`, `Scale` | Una llamada con `weighbridge.process` |

Al terminar, ningún archivo de `Wms.Application` debe referenciar `SystemRolesCode`, salvo `RolePermissionPresets` (en Domain) y la conversión.

### 5.9 Conversión al arrancar

**`Wms.Api/Common/Identity/UserPermissionsBootstrapper.cs`** (nuevo):
- Extensión `SeedUserPermissionsAsync(this WebApplication app)`.
- Se llama en `Program.cs` **después** de `SeedBootstrapAdminAsync()` (línea 166).

**Qué hace, para cada usuario con `permissions_initialized_at IS NULL`:**
1. Lee sus roles por `Code`, uniendo `AspNetUserRoles` con `system_roles`. No usa `GetRolesAsync`, que devuelve nombres.
2. Aplica `RolePermissionPresets.ForRoles`. Si el resultado incluye acceso total, llama a `GrantFullAccess()`; además inserta los permisos.
3. Marca `permissions_initialized_at = UtcNow`.
4. Un usuario sin roles queda sin permisos, pero también queda marcado.

**Además:**
- Todo va en una sola transacción.
- Es idempotente: un usuario ya marcado no se toca, aunque después le hayan quitado todos los permisos.
- Escribe en el log cuántos usuarios convirtió.

### 5.10 Pruebas del backend

**Unitarias (`Wms.Tests`):**

| Archivo | Qué prueba |
| --- | --- |
| `Security/WmsPermissionsCatalogTests.cs` (nuevo) | Hay 73 códigos y no se repiten. Cada `ImpliesCode` y `ParentCode` existe. Todo permiso de `WmsPolicies.Permissions` y de `RolePermissionPresets` existe. Cada valor de `SystemRolesCode` tiene plantilla. |
| `Security/WmsPolicyRolesTests.cs` | Se renombra a `WmsPoliciesTests.cs` y fija la tabla §5.4 completa. Comprueba que no hay reglas de más y que `AdminOnly` no existe. |
| `Security/PresetEquivalenceTests.cs` (nuevo) | Copia literal de la tabla política → roles **antigua**, con nombre `LegacyPolicyRoles`. Para cada regla que se conserva (`WarehouseAccess`, `BillingAccess`, `ForeignTradeAccess`, `ScaleAccess`, `WeighingCorrectionAccess`, `OperationalAccess`, `EntryCorrectionAccess`, `DepositEntryDateAccess`, `GateAccess`, `StakeholderAccess`, `TransportCatalogAccess`, `NoveltyReadAccess`, `InventoryReportAccess`) y cada rol R, verifica que la plantilla de R cumple la regla **si y solo si** R estaba en la tabla antigua. Para las reglas nuevas se usa esta matriz explícita. `WeighingDateCorrectionAccess` y `WeighingVoidAccess`: Admin y Scale. `LocationReadAccess`: Admin y Warehouse. `AgreementAccess` y `BillingSummaryAccess`: Admin y Billing. `InventoryAdjustmentAccess` y `TraceabilityAccess`: Admin y ForeignTrade. Todas las demás reglas nuevas: solo Admin. |
| `Security/PermissionImplicationsTests.cs` (nuevo) | Cada implicación de §2, incluidas las cadenas. |
| `Users/UserAdministrationRulesTests.cs` | Se reescribe para las 4 reglas nuevas y `EnsureCanDeactivate`. |
| `Reports/StatisticsVisibilityTests.cs`, `Auth/PasswordResetEligibilityTests.cs`, `Reports/TraceabilityNotificationTests.cs`, `ForeignTrade/DepositCancellationNoticesTests.cs`, `Billing/InvoiceCancellationPolicyTests.cs` | Se adaptan a la API nueva |
| `Security/SeededRolesTests.cs` | Sin cambios: los roles se conservan |

**De integración (`Wms.IntegrationTests`):**

**`Infrastructure/WmsApiFactory.cs`:**
- `CreateUserAsync(params SystemRolesCode[] roles)` **conserva la firma**. Después de asignar los roles, aplica `RolePermissionPresets.ForRoles`: acceso total y permisos.
- Marca `PermissionsInitializedAt`.
- Agregar `CreateUserWithPermissionsAsync(bool fullAccess, params string[] permissions)` y `CreateClientWithPermissionsAsync(...)`.
- Así las 190 llamadas existentes siguen funcionando sin cambios.

**Pruebas nuevas:**

| Archivo | Casos |
| --- | --- |
| `Security/PermissionAuthorizationTests.cs` | (a) Solo `stakeholders.customers.manage`: `POST stakeholder` no da 403; `GET foreign-trade/deposits` da 403. (b) Plantilla Billing más `stakeholders.customers.manage` y `stakeholders.agreements` (el ejemplo del usuario): crea un cliente y un convenio sin 403. (c) Solo `admin.locations`: GET y POST de `warehouse/locations` funcionan; `GET warehouse/inventory/deposits` da 403. (d) Solo `dashboard.traceability`: `GET reports/traceability` funciona; `GET foreign-trade/imports` da 403. (e) Solo `foreign-trade.deposits`: `POST warehouse/inventory/adjustments` da 403. (f) Solo `admin.products`: `POST product` funciona; `GET user` da 403. (g) Acceso total: todo funciona. |
| `Security/UserPermissionsAdministrationTests.cs` | `PUT` normaliza las implicaciones. Rechaza códigos inexistentes, usuarios sin pantallas, quitarse el propio acceso total, cambiar el acceso total sin tenerlo y quedarse sin usuarios con acceso total. Después del `PUT`, el token anterior da 401 y el nuevo login trae los permisos nuevos. Hay fila de auditoría con la descripción. |
| `Security/UserPermissionsBootstrapperTests.cs` | Usuario con roles Billing y ForeignTrade sin marcar: recibe la unión. Ejecutar dos veces no cambia nada. Un usuario marcado y sin permisos no se rellena. |
| `Notifications/PermissionAudienceTests.cs` | Un aviso a `foreign-trade.deposits` llega a quien tiene el permiso y a quien tiene acceso total. No llega a un usuario sin él ni a uno inactivo. |
| `Security/ControllerAuthorizationTests.cs` | Agregar: (1) por reflexión, toda regla en un `[Authorize(Policy = …)]` está registrada en `WmsPolicies`; (2) las acciones movidas tienen la regla nueva (las 4 tablas de §5.4). |

**Pruebas existentes que se adaptan:**

| Archivo | Cambio |
| --- | --- |
| `Security/SessionRevocationTests.cs` | `RemoveRole_OldTokenGets401_NewTokenGets403` pasa a `ChangePermissions_OldTokenGets401_NewTokenGets403`, usando `PUT user/{id}/permissions` |
| `Security/UserAdministrationTests.cs` | Crear usuarios con `permissions`; ya no hay asignar ni quitar roles |
| `Audit/CatalogAuditTests.cs:45` | `AssignRole_WritesAuditLogWithDescription` pasa a `SetPermissions_WritesAuditLogWithDescription` |
| `Notifications/ForeignTradeNotificationTests.cs` | Destinatarios por permiso |
| `Reports/OperationalStatisticsTests.cs` | El bloque de facturación depende de `dashboard.billing-summary` o del acceso total |
| `Smoke/ApiSmokeTests.cs` | Revisar las rutas movidas |

---

## 6. Frontend (`Frontend/wms`)

### 6.1 Estado, tipos y composable

| Archivo | Cambio |
| --- | --- |
| `app/utils/permissions.ts` (nuevo) | `PERMISSION_CODES` (los 73, `as const`) y el tipo `PermissionCode`. `PERMISSION_IMPLIES: Partial<Record<PermissionCode, PermissionCode>>` (§2). `normalizePermissions(codes)`, que agrega los implicados en cascada. `STAKEHOLDER_VIEW_BY_ROLE` y `STAKEHOLDER_MANAGE_BY_ROLE` (§6.6). |
| `stores/auth.ts` | `roles: string[]` pasa a `permissions: string[]` y `hasFullAccess: boolean`. Getters `can: (code) => state.permissions.includes(code)` y `canAny: (codes) => codes.some(...)`. Se borran `userRoles` y `hasRole`. `restoreUserState(username, mustChangePassword, permissions, hasFullAccess, name?)`. `login` lee `payload.user.permissions` y `payload.user.hasFullAccess`. `logoutUser` limpia los campos nuevos. |
| `app/features/auth/types/login.ts` | `user.roles` pasa a `user.permissions: string[]` y `user.hasFullAccess: boolean` |
| `app/features/users/types/user.ts` | `IUser.roles` pasa a `permissions: string[]` y `hasFullAccess: boolean`. Se borra `IUserRole`. |
| `app/composables/usePermissions.ts` | Pasa a ser `export const usePermissions = () => ({ can, canAny })` y delega en el store. Se borran `ROLES`, `RoleCode`, `MODULE_ROLES`, `hasRole`, `hasAnyRole` y `canAccessModule`. Sigue la convención: se importa explícitamente. |
| `app/plugins/auth-init.client.ts`, `app/middleware/auth.global.ts`, `app/features/users/composables/useCurrentUser.ts` | Llaman a `restoreUserState` con `user.permissions` y `user.hasFullAccess` |
| `app/types/page-meta.d.ts` | `requiredRoles` pasa a `requiredPermissions?: PermissionCode[]` |

**Se borran:**
- `app/composables/useAuthForeignTrade.ts`
- `app/utils/weighing-permissions.ts` y `test/unit/utils/weighing-permissions.spec.ts`
- `app/utils/role-routes.ts`, que reemplaza `home-route.ts` (§6.4)
- `app/features/users/components/UserRoles.vue`
- `useAssignRoles.ts`, `useRemoveRoles.ts`
- `assignRoles` y `removeRoles` de `user-service.ts`, con sus tipos de `types/requests.ts`

### 6.2 Middleware y metadatos de página

**`app/middleware/auth.global.ts`:**
- Las líneas 74-81 leen `to.meta.requiredPermissions`.
- Si hay lista y `!authStore.canAny(lista)`, redirige con `resolveDeniedRedirect(path, authStore.permissions)`.
- Se conserva `normalizePath` (DEF-F11-021).
- Una página sin `requiredPermissions` sigue abierta a cualquier usuario autenticado, como hoy.

**`requiredRoles` pasa a `requiredPermissions`.** Basta **alguno** de los permisos de la lista.

| Página (`app/pages/…`) | `requiredPermissions` |
| --- | --- |
| `index.vue` | `['dashboard.traceability']` |
| `reports/statistics.vue` | `['dashboard.traceability']` (mantiene `redirect: "/"`) |
| `admin/audit/index.vue` | `['admin.audit']` |
| `admin/cargo-unit-types/index.vue` | `['admin.cargo-unit-types']` |
| `admin/cities/index.vue` | `['admin.cities']` |
| `admin/crews/index.vue` | `['admin.crews']` |
| `admin/drivers/index.vue` | `['admin.drivers']` |
| `admin/entry-reasons/index.vue` | `['admin.entry-reasons']` |
| `admin/forklift-rates/index.vue` | `['admin.forklift-rates']` |
| `admin/locations/index.vue` | `['admin.locations']` |
| `admin/packaging-types/index.vue` | `['admin.packaging-types']` |
| `admin/parameters/index.vue` | `['admin.parameters']` |
| `admin/unit-measures/index.vue` | `['admin.unit-measures']` |
| `admin/vehicles/index.vue` | `['admin.vehicles']` |
| `admin/products/` (index, create, `[id]`, `edit/[id]`) | `['admin.products']` |
| `admin/services/` (index, create, `[id]`, `edit/[id]`) | `['admin.services']` |
| `admin/users/` (index, create, `[id]`, `edit/[id]`) | `['admin.users']` |
| `admin/stakeholders/index.vue`, `admin/stakeholders/[id].vue` | `['stakeholders.all.view', 'stakeholders.customers.view', 'stakeholders.transport.view', 'stakeholders.customs.view']`, más la regla interna §6.6 |
| `admin/stakeholders/create.vue`, `admin/stakeholders/edit/[id].vue` | `['stakeholders.all.manage', 'stakeholders.customers.manage', 'stakeholders.transport.manage', 'stakeholders.customs.manage']`, más la regla interna §6.6 |
| `operations/entries/index.vue` | `['gate.entry']` |
| `operations/entries/exits.vue` | `['gate.exit']` |
| `operations/entries/history.vue` | `['gate.history']` |
| `operations/weighbridge/index.vue`, `in-process.vue`, `pending-reweigh.vue`, `recover.vue` | `['weighbridge.process']` |
| `operations/weighbridge/dashboard.vue` | `['weighbridge.dashboard']` |
| `operations/weighbridge/history.vue` | `['weighbridge.history']` |
| `operations/weighbridge/reports.vue` | `['weighbridge.reports']` |
| `operations/weighbridge/cycles/[id].vue` | `['weighbridge.process', 'weighbridge.history', 'billing.invoices', 'foreign-trade.deposits']` |
| `warehouse/index.vue` | `['warehouse.dashboard']` |
| `warehouse/receptions/entry.vue` | `['warehouse.receptions.entry']` |
| `warehouse/receptions/index.vue` | `['warehouse.receptions']` |
| `warehouse/receptions/history.vue` | `['warehouse.receptions.history']` |
| `warehouse/receptions/[id].vue` | `['warehouse.receptions', 'warehouse.receptions.history']` |
| `warehouse/forklift/index.vue` | `['warehouse.forklift']` |
| `warehouse/forklift/history.vue` | `['warehouse.forklift.history']` |
| `warehouse/loading-orders/index.vue`, `[id].vue` | `['warehouse.loading-orders']` |
| `warehouse/inventory/index.vue` | `['warehouse.inventory']` |
| `warehouse/novelties/index.vue` | `['warehouse.novelties']` |
| `foreign-trade/index.vue` | `['foreign-trade.dashboard']` |
| `foreign-trade/deposits/index.vue`; `imports`, `exports`, `inspections` (index y `[id]`) | `['foreign-trade.deposits']` |
| `foreign-trade/abandonment/index.vue` | `['foreign-trade.abandonment']` |
| `foreign-trade/packing-lists/index.vue` | `['foreign-trade.packing-lists']` |
| `foreign-trade/releases/index.vue` | `['foreign-trade.releases']` |
| `foreign-trade/loading-orders/create.vue` | `['foreign-trade.loading-orders.create']` |
| `foreign-trade/loading-orders/index.vue` | `['foreign-trade.loading-orders']` |
| `foreign-trade/loading-orders/[id]/index.vue` | `['foreign-trade.loading-orders', 'foreign-trade.loading-orders.create']` (al crear, se redirige al detalle) |
| `foreign-trade/dispatch-guides/create.vue` | `['foreign-trade.dispatch-guides.create']` |
| `foreign-trade/dispatch-guides/index.vue` | `['foreign-trade.dispatch-guides']` |
| `foreign-trade/dispatch-guides/pending.vue` | `['foreign-trade.dispatch-guides.pending']` |
| `billing/index.vue` | `['billing.dashboard']` |
| `billing/invoices/index.vue`, `[id].vue` | `['billing.invoices']` |
| `billing/payments` | `['billing.payments']` |
| `billing/pending-deposits` | `['billing.pending-deposits']` |
| `billing/configurations` | `['billing.configurations']` |
| `billing/reports/annual` | `['billing.reports.annual']` |
| `billing/reports/deposit-billing` | `['billing.reports.deposit-billing']` |
| `reports/warehouse-movements.vue` | `['reports.warehouse-movements']` |
| `reports/daily-incoming-goods.vue` | `['reports.daily-incoming']` |
| `reports/daily-outgoing-goods.vue` | `['reports.daily-outgoing']` |
| `reports/abandonment-candidates.vue` | `['reports.abandonment-candidates']` |
| `reports/abandonment-exits.vue` | `['reports.abandonment-exits']` |
| `reports/general-inventory.vue` | `['reports.general-inventory']` |
| `reports/policies.vue` | `['reports.policies']` |
| `reports/incoming-by-product.vue` | `['reports.incoming-by-product']` |
| `reports/customs-agency-entries.vue` | `['reports.customs-agency-entries']` |

**Sin permiso:** `notifications`, `access-denied`, y las 4 de `auth/`.

**Si encuentras una página que no está en esta tabla, detente y pregunta.**

### 6.3 Menú (`app/components/layout/AppMenu.vue`)

**Estructura:**
- Cada hoja navegable lleva `permissions: PermissionCode[]`. Basta alguno.
- Los grupos **no** llevan permisos: un grupo se muestra si le queda al menos una hija visible.
- El filtro es recursivo y devuelve copias; no muta `allMenuItems`.
- `Notificaciones` no lleva permiso.
- Se borra la propiedad `roles`.

Estructura nueva, en este orden. Las etiquetas y las rutas se conservan tal como están hoy.

1. **Notificaciones**: `/notifications`
2. **Dashboards**: Trazabilidad `/` (`dashboard.traceability`)
3. **Administración**
   - Usuarios: Listado, Crear (`admin.users`)
   - Productos: Listado, Crear (`admin.products`); Tipos de Embalaje (`admin.packaging-types`); Unidades de medida (`admin.unit-measures`); Tipos de unidad de carga (`admin.cargo-unit-types`)
   - Servicios: Tarifas base, Crear (`admin.services`)
   - Tarifas de montacargas (`admin.forklift-rates`), Conductores (`admin.drivers`), Vehículos (`admin.vehicles`), Motivos de Entrada (`admin.entry-reasons`), Ubicaciones (`admin.locations`), Ciudades (`admin.cities`), Cuadrillas (`admin.crews`), Auditoría (`admin.audit`)
4. **Terceros** (grupo nuevo de primer nivel; icono `pi pi-fw pi-users`)
   - Listado `/admin/stakeholders` (`stakeholders.all.view`)
   - Clientes `?rol=CUSTOMER` (`stakeholders.customers.view`)
   - Transportadoras `?rol=TRANSPORT_COMPANY` (`stakeholders.transport.view`)
   - Agencias de aduanas `?rol=CUSTOMS_AGENCY` (`stakeholders.customs.view`)
   - Crear `/admin/stakeholders/create` (los 4 `*.manage`)
5. **Vigilancia**: Ingreso (`gate.entry`), Salida (`gate.exit`), Historial (`gate.history`)
6. **Báscula**: Dashboard (`weighbridge.dashboard`), Proceso de Pesaje (`weighbridge.process`), Historial (`weighbridge.history`), Reportes (`weighbridge.reports`)
7. **Bodega**
   - Dashboard (`warehouse.dashboard`)
   - Recepciones: Ingresos (`warehouse.receptions.entry`), Recepción (`warehouse.receptions`), Historial (`warehouse.receptions.history`)
   - Montacargas: Registrar uso (`warehouse.forklift`), Historial (`warehouse.forklift.history`)
   - Órdenes de Cargue (`warehouse.loading-orders`), Inventario (`warehouse.inventory`), Novedades (`warehouse.novelties`)
8. **Comercio Exterior**
   - Dashboard, Depósitos, Abandono y prórrogas, Listas de empaque, Levantes (sus permisos)
   - Órdenes de Cargue: Crear Orden (`foreign-trade.loading-orders.create`), Listado (`foreign-trade.loading-orders`)
   - Guías de Salida: Generar Guía (`.dispatch-guides.create`), Historial (`.dispatch-guides`), Pendientes (`.dispatch-guides.pending`)
9. **Facturación**: Dashboard, Facturas, Depósitos Pendientes, Pagos, Configuraciones, Facturación anual, Facturación por CPI (sus permisos)
10. **Reportes** (grupo nuevo de primer nivel; icono `pi pi-fw pi-chart-bar`): Movimientos por Depósito, Mercancías ingresadas (diario), Salida de mercancía (diario), Mercancía en abandono, Salidas a destino de abandono, Inventario general, Informe de póliza, Ingresos por producto, Ingresos por agencia de aduanas (sus permisos)

**Se quitan de su grupo anterior:**
- Terceros, de Administración y de Comercio Exterior.
- Clientes, Inventario general y Movimientos por depósito, de Facturación.
- Inventario general, de Bodega.
- Reportes, de Comercio Exterior.

**Resaltado (DEF-F11-022):**
- `menu-route.ts` y `AppMenuItem.vue` trabajan sobre el modelo **filtrado**. No cambian su lógica.
- Las claves posicionales se calculan sobre lo visible.
- Hay que probar que el resaltado sigue funcionando con grupos parcialmente filtrados (§6.10).

### 6.4 Página de inicio, atajos y barra

**`app/utils/home-route.ts`** (nuevo):
- `LANDING_PRIORITY`:
  1. `['dashboard.traceability', '/']`
  2. `['gate.entry', '/operations/entries']`
  3. `['warehouse.dashboard', '/warehouse']`
  4. `['billing.dashboard', '/billing']`
  5. `['weighbridge.process', '/operations/weighbridge']`
- `getHomeRoute(permissions)`, en orden:
  1. El primero de `LANDING_PRIORITY` que tenga el usuario.
  2. Si no hay ninguno, la primera hoja visible del menú filtrado, en orden y saltando `/notifications`. Para obtenerla, exporta el filtro de `AppMenu.vue` a `app/utils/menu-filter.ts` (`filterMenu(items, can)`) junto con `allMenuItems` (`app/utils/menu-items.ts`).
  3. Si tampoco hay, `/notifications`.
- `resolveDeniedRedirect(path, permissions)`: misma regla que CHG-87. Si `path === '/'` y el inicio no es `/`, va al inicio; si no, a `/access-denied`.

**Llamadas a `getDefaultRouteForRoles(...)`** que pasan a `getHomeRoute(authStore.permissions)`:
- `AppTopbar.vue:17`, `AppSidebar.vue:10`, `AppBreadcrumb.vue:59`
- `useLogin.ts:21`
- `auth/change-password.vue:29,55`
- `access-denied.vue:12`
- `error.vue:24`
- `auth.global.ts:52`

**`app/composables/useGlobalShortcuts.ts`:** `roles` pasa a `permissions` y la comprobación usa `canAny(shortcut.permissions)`.

| Atajo | Permisos |
| --- | --- |
| Alt+N, Alt+K | `['weighbridge.process']` |
| Alt+I, Alt+P | `['foreign-trade.deposits']` |
| Alt+O | `['foreign-trade.loading-orders']` |
| Alt+L | `['foreign-trade.releases']` |

### 6.5 Controles dentro de las pantallas

| Archivo | Hoy | Ahora |
| --- | --- | --- |
| `components/layout/AppTopbar.vue:14,64` | `hasAnyRole([Admin, ForeignTrade])` | `can('dashboard.traceability')` |
| `components/layout/AppRightMenu.vue:14,113` | `hasRole(Admin)` | `can('admin.parameters')` |
| `AppRightMenu.vue:17` | `hasAnyRole(s.roles)` | `canAny(s.permissions)` |
| `AppRightMenu.vue:22-26`, `AppMenuProfile.vue:13-18` | Muestra los nombres de los roles | Muestra «Acceso total» si `hasFullAccess`; si no, «Acceso personalizado» |
| `features/traceability/components/TraceabilityStats.vue:12-15,115` | `isAdmin` | `can('dashboard.billing-summary')`, también para habilitar `useBillingDashboard` |
| `pages/reports/statistics.vue:25-27` | `isAdmin` | `can('dashboard.billing-summary')` |
| `features/foreign-trade/components/DepositProductsTable.vue:59,188` | `hasAnyRole([Admin])` | `can('admin.audit')` |
| `features/weighbridge/components/WeighbridgeCycleTickets.vue:208` | `hasAnyRole([Admin, Billing])` | `can('billing.invoices')` |
| `pages/operations/weighbridge/cycles/[id].vue:67/484` | `hasAnyRole([Admin, Scale, ForeignTrade])` | `can('foreign-trade.deposit-entry-date')` |
| `cycles/[id].vue:87-89` | `canCorrectWeighings` | `can('weighbridge.correct-weights')` |
| `cycles/[id].vue:99-101` | `hasAnyRole([Admin, Scale])` (anular) | `can('weighbridge.void')` |
| `cycles/[id].vue:355` | `hasAnyRole([Admin, Scale])` (cerrar ciclo) | `can('weighbridge.process')` |
| `pages/operations/weighbridge/history.vue:149/806` | anular | `can('weighbridge.void')` |
| `history.vue:205/627` | `canCorrectWeighings` | `can('weighbridge.correct-weights')` |
| `history.vue:206/607` | `canModifyWeighingDate` | `can('weighbridge.change-date')` |
| `pages/operations/entries/history.vue:32/273` | `hasAnyRole([Admin, Receiving])` | Se borra la comprobación; `:enable-edit="true"`, porque la página ya exige `gate.history` |
| `pages/foreign-trade/imports/[id]/index.vue:93-95`, `exports/[id]/index.vue:89-91`, `inspections/[id]/index.vue:93-95` (`canEditInventory`) | `hasAnyRole([Admin, ForeignTrade])` | `can('foreign-trade.inventory-adjustment')` (conserva la condición de estado Draft o Confirmed) |
| El mismo bloque compartido de esos tres detalles: botón «Editar fecha de ingreso» | Sin control | `v-if` con `can('foreign-trade.deposit-entry-date')` (cambio intencional 5) |
| `pages/foreign-trade/imports/index.vue:30,223-224` | `useAuthForeignTrade` | `:can-validate` y `:can-nationalize` = `can('foreign-trade.deposits')` |
| `pages/admin/stakeholders/index.vue`, `[id].vue` | `hasAnyRole` | §6.6 |

### 6.6 Terceros

**`app/utils/stakeholder-permissions.ts`** (nuevo), funciones puras y probadas.

Los dos mapas de `permissions.ts`:
- `STAKEHOLDER_VIEW_BY_ROLE = { CUSTOMER: 'stakeholders.customers.view', TRANSPORT_COMPANY: 'stakeholders.transport.view', CUSTOMS_AGENCY: 'stakeholders.customs.view' }`
- `STAKEHOLDER_MANAGE_BY_ROLE`: igual, con `*.manage`.
- `IMPORTER` y `EXPORTER` no tienen permiso propio: solo los cubren `stakeholders.all.view` y `stakeholders.all.manage`.

**Funciones:**
- `viewableRoleCodes(can)`: devuelve `null` (todos) si `can('stakeholders.all.view')`; si no, los códigos de negocio cuyo `*.view` tiene el usuario.
- `manageableRoleCodes(can)`: devuelve los 5 códigos si `can('stakeholders.all.manage')`; si no, los cuyo `*.manage` tiene el usuario.
- `canViewStakeholder(st, can)`: `all.view`, o algún rol de negocio de `st` está en `viewableRoleCodes`.
- `canManageStakeholder(st, can)`: `all.manage`, o algún rol de `st` está en `manageableRoleCodes`.

**Listado (`pages/admin/stakeholders/index.vue`):**
- **Con `?rol=X`:**
  - Exige `all.view` o el `*.view` de X.
  - Si no lo tiene, redirige a `/access-denied`. Hazlo en el `setup` con `navigateTo`, antes de cargar.
- **Sin `rol`:**
  - Exige `all.view`.
  - Si no lo tiene, `navigateTo` con `replace` a `?rol=` del primer código de `viewableRoleCodes`, en orden CUSTOMER, TRANSPORT_COMPANY, CUSTOMS_AGENCY.
- **Filtro de la columna «Roles»:**
  - Sin `all.view`, se oculta y la lista queda fija al `rol` de la URL.
  - Con `all.view`, igual que hoy.
- **Botones:**
  - `:enable-create`: `manageableRoleCodes(can).length > 0`.
  - `:enable-edit`: por fila, con `canManageStakeholder(row, can)`. Si `StakeholderTable` hoy recibe un booleano global, agrega la prop `canEditRow?: (row) => boolean`.

**Detalle (`[id].vue`):**
- Al cargar, si `!canViewStakeholder`, redirige a `/access-denied`.
- `canManageStakeholder` se calcula con la función. `canManageAgreements` es `can('stakeholders.agreements')`, y se conserva la condición `isCustomer`.
- **`StakeholderBusinessRoles.vue`:**
  - En el diálogo de asignar, las opciones se filtran a `manageableRoleCodes`.
  - El enlace de quitar solo aparece en los roles que el usuario gestiona; se conserva la regla de no quitar el último.

**Crear y editar:**
- **`StakeholderForm.vue`:** las opciones de `businessRoles` (por id) se filtran a los roles de negocio cuyo código está en `manageableRoleCodes`.
- **`edit/[id].vue`:** si `!canManageStakeholder`, redirige a `/access-denied`.

### 6.7 Administración de usuarios

**`app/features/users/components/UserPermissionsEditor.vue`** (nuevo), un `v-model` de `{ hasFullAccess: boolean, permissions: string[] }`:

- **Datos:** el catálogo sale de `GET /administration/permissions`, con el composable `usePermissionCatalog` y la query key `['permissions','catalog']`.
- **Acceso total:**
  - Arriba va un `ToggleSwitch` «Acceso total».
  - Solo es editable si el usuario actual tiene `hasFullAccess`; si no, se muestra deshabilitado con el texto «Solo un usuario con acceso total puede cambiarlo».
  - Con acceso total activado, el árbol se muestra deshabilitado y con todo marcado.
- **Árbol por módulo** (`Panel` o `Fieldset` por módulo, en orden):
  - Casillas para las pantallas.
  - Las acciones van sangradas debajo de su `parentCode`.
  - Por módulo hay «Marcar todo» y «Desmarcar todo».
- **Implicaciones:**
  - Al marcar un permiso con `impliesCode`, se marca el implicado.
  - Al desmarcar un permiso, se desmarcan los que lo implican.
  - Usa `normalizePermissions` y su inversa.
- **Copiar:** el botón «Copiar permisos de otro usuario» abre un diálogo con un `Select` de usuarios (`GET /user?all=true`). Al confirmar, carga `GET /user/{id}/permissions` y **reemplaza** el `v-model`, salvo `hasFullAccess` si el usuario actual no puede cambiarlo. No guarda hasta «Guardar».

**`UserPermissions.vue`** (nuevo, tarjeta «Permisos») reemplaza a `UserRoles.vue` en `pages/admin/users/[id].vue`:
- Contiene el editor y el botón «Guardar permisos».
- «Guardar permisos» llama a `PUT /user/{id}/permissions` (`useSetUserPermissions`).
- Al guardar, invalida `['users']` y `['user', id]`.
- Si el usuario editado es el actual, también invalida `['currentUser']`.
- Muestra un toast «Permisos actualizados».

**`UserForm.vue` (crear):**
- El `MultiSelect` `rolIds` (líneas 95-104) se reemplaza por `UserPermissionsEditor`.
- `ICreateUserRequest` pasa a `{ …, hasFullAccess, permissions }`.
- En el esquema `user-create-schema.ts`, `rolIds` pasa a `hasFullAccess: z.boolean()` y `permissions: z.array(z.string())`. Un `refine` exige acceso total o al menos un permiso de tipo pantalla: «Seleccione al menos una pantalla o active el acceso total.» El tipo de cada código lo da el catálogo; en el esquema basta `permissions.length > 0 || hasFullAccess`, porque el backend valida el tipo.

`pages/admin/users/[id].vue` ya no usa `systemRolesQuery`, `handleAssignRoles` ni `handleRemoveRoles`.

### 6.8 Refresco de permisos

En `app/plugins/api-client.ts`, después de `authStore.updateTokens(...)` (línea ~75):
- Pide `UserService.getCurrentUser()`.
- Llama a `restoreUserState` con los permisos nuevos.
- Si eso falla, no cierra la sesión: el siguiente `/me` lo corrige.

Así, cuando un administrador cambia los permisos de alguien (rota el sello y el token viejo da 401), el usuario ve el menú nuevo tras el refresh, sin cerrar sesión.

**No hay cambios en SignalR:** los grupos ya son por usuario.

### 6.9 Documentación del frontend

- **`Frontend/wms/README.md`:** en la sección de usuarios de prueba, explicar que los permisos se convirtieron desde sus roles el día del despliegue, y que ahora se editan en Administración › Usuarios › Permisos. Agregar las limitaciones aceptadas de §4.
- **`code_workspace/docs/contexto-negocio-wms-para-ia.md` §3:** reemplazar la tabla de roles y políticas por un resumen de este modelo y un enlace a este plan.

### 6.10 Pruebas del frontend

| Archivo | Casos |
| --- | --- |
| `test/unit/utils/permissions.spec.ts` (nuevo) | `normalizePermissions`, cadenas de implicación |
| `test/unit/utils/home-route.spec.ts` (reemplaza `role-routes.spec.ts`) | Prioridad de inicio. Respaldo a la primera hoja del menú y luego a `/notifications`. `resolveDeniedRedirect`. |
| `test/unit/utils/stakeholder-permissions.spec.ts` (nuevo) | Las 4 funciones. Importador sin `all.*`. Tercero con varios roles. |
| `test/unit/guards/page-permissions.spec.ts` (nuevo) | Lee con `fs` todos los `app/pages/**/*.vue`. Cada página fuera de la lista de libres (§6.2) declara `requiredPermissions`. Todos los códigos usados están en `PERMISSION_CODES`. Ninguna página contiene `requiredRoles`. |
| `test/components/app/auth-middleware.spec.ts` | `signIn(roles)` pasa a `signIn(permissions)`. Mismos casos: barra final, `/` sin `dashboard.traceability` va al inicio, ruta negada va a `/access-denied`. |
| `test/components/app/AccessDenied.spec.ts`, `ErrorPage.spec.ts` | «Ir a mi inicio» con permisos |
| `test/components/layout/AppMenu.spec.ts` | `menuLabelsFor(permissions)`. Grupo sin hijas visibles: oculto. Ninguna etiqueta repetida con acceso total. **Equivalencia:** para cada plantilla de §3, copiada como constante en la prueba, el conjunto de **rutas** visibles es igual al de hoy (rutas por rol, copiadas como constante) más las diferencias de §4.4. |
| `test/components/layout/AppMenuItem.spec.ts` | Fixture con `permissions`. Resaltado DEF-F11-022 con un grupo parcialmente filtrado. |
| `test/unit/users/user-create-schema.spec.ts` | Exige acceso total o algún permiso |
| `test/components/users/UserPermissionsEditor.spec.ts` (nuevo) | Implicaciones al marcar y desmarcar. Acceso total deshabilitado para quien no lo tiene. Copiar reemplaza la selección. |

---

## 7. Fases

### 7.0 Ramas de git

La implementación completa se hace en una rama nueva, creada desde `develop`, en los dos repositorios:

| Repositorio | Ruta | Rama base | Rama de trabajo |
| --- | --- | --- | --- |
| Backend | `code_workspace/Backend/wms-api` | `develop` | `feature/permisos-por-usuario` |
| Frontend | `code_workspace/Frontend/wms` | `develop` | `feature/permisos-por-usuario` |

**Antes de la fase B1, en el backend:**

```bash
git -C /Volumes/Dock/Projects/bodegas_asociadas/code_workspace/Backend/wms-api status
```

```bash
git -C /Volumes/Dock/Projects/bodegas_asociadas/code_workspace/Backend/wms-api checkout develop
```

```bash
git -C /Volumes/Dock/Projects/bodegas_asociadas/code_workspace/Backend/wms-api pull --ff-only
```

```bash
git -C /Volumes/Dock/Projects/bodegas_asociadas/code_workspace/Backend/wms-api checkout -b feature/permisos-por-usuario
```

**Antes de la fase F1, en el frontend:** los mismos cuatro comandos, con la ruta `/Volumes/Dock/Projects/bodegas_asociadas/code_workspace/Frontend/wms`.

**Reglas:**

1. **Árbol limpio antes de crear la rama.** Si `git status` no está limpio, detente y avisa al usuario. No guardes con `stash`, no descartes y no hagas commit de cambios ajenos.
2. **`develop` al día.** Actualízala con `pull --ff-only`. Si no avanza en línea recta, detente y pregunta.
3. **Si la rama ya existe,** local o remota, no la recrees ni la sobrescribas: pregunta al usuario.
4. **Commits: los hace el usuario, no el agente.** El agente no ejecuta `git commit`, `git add`, `git stash`, `git reset` ni nada que cambie el historial o el índice. Al terminar cada fase (B1…B6 en el backend, F1…F7 en el frontend), el agente:
   - Se detiene.
   - Entrega el **mensaje de commit** propuesto, en español, empezando por el código de la fase (p. ej. `feat(permisos): B2 autorización por permiso`), con un cuerpo breve que explique qué cambia y por qué.
   - Entrega la **lista de archivos** de la fase (nuevos, modificados y borrados), que debe coincidir con `git status`, y el repositorio al que pertenecen.
   - **Espera** a que el usuario confirme que hizo el commit antes de seguir con la siguiente fase, para que cada fase quede en su propio commit.

   F6, que es verificación manual, solo lleva mensaje si deja correcciones. Si una fase toca ambos repositorios, se entrega un mensaje por repositorio. En B1, la migración generada forma parte de los archivos de la fase.
5. **Ni `develop` ni `main` se tocan:** no se fusiona, no se rebasa sobre ellas y no se hace `push` a ellas.
6. **`push` de la rama:** solo cuando el usuario lo pida. Las pull requests van de `feature/permisos-por-usuario` hacia `develop`, una por repositorio, y solo si el usuario las pide.
7. **Si `develop` avanza durante el trabajo,** no la fusiones por tu cuenta: avisa al usuario y espera instrucciones.
8. **Los documentos sin git** (`code_workspace/ajustes/` y `code_workspace/docs/`, fase F7) se editan en su sitio. No pertenecen a ninguna rama.

### 7.1 Orden de las fases


| Fase | Repositorio | Contenido | Termina cuando |
| --- | --- | --- | --- |
| **B1** | Backend | §5.1-5.3: entidades, configuraciones, `HasData`, `WmsPermissions`, `PermissionImplications`, `RolePermissionPresets`, `UserPermissionStore`. Pruebas `WmsPermissionsCatalogTests` y `PermissionImplicationsTests`. | Compila y pasan las pruebas unitarias. La migración `AddUserPermissions` está generada y aplicada en la base local con `dotnet ef` (§7.2). `dotnet ef migrations has-pending-model-changes` no informa cambios. |
| **B2** | Backend | §5.4: `PermissionRequirement` y su handler, `WmsPolicies`, los 4 controladores nuevos, los cambios de atributos, el hub. `ControllerAuthorizationTests`, `WmsPoliciesTests`, `PresetEquivalenceTests`. | Compila y pasan las pruebas unitarias. |
| **B3** | Backend | §5.5 y §5.9: token, login, `/me`, `UserDto`, el bootstrapper y el ajuste de `WmsApiFactory`. | Pasan **todas** las pruebas de integración existentes sin cambiar sus llamadas (salvo las de §5.10 «se adaptan»). |
| **B4** | Backend | §5.6: endpoints de permisos, creación de usuarios, activación, reglas; se borran assign y remove de roles. `UserPermissionsAdministrationTests` y las adaptaciones de sesión y auditoría. | Pasan las pruebas. |
| **B5** | Backend | §5.7 y §5.8: estadísticas, recuperación de contraseña, seeder del administrador, notificaciones. `PermissionAudienceTests` y las adaptaciones. | Pasan las pruebas. Cada aparición restante de `grep -rn "SystemRolesCode" Wms.Application Wms.Api` es de `UserPermissionsBootstrapper`, `BootstrapAdminSeeder` o de la consulta de roles del sistema (`GetSystemRoles`), que se conserva. |
| **B6** | Backend | `PermissionAuthorizationTests` y `UserPermissionsBootstrapperTests`. Repaso de `grep -rn "AdminOnly\|ClaimTypes.Role\|NotifyRoleAsync\|SendToRoleAsync"`, que debe quedar en 0 resultados. | Todo en verde. |
| **F1** | Frontend | §6.1: utilidades, store, tipos, composable. | `npx nuxi typecheck` muestra los errores que se resuelven en F2-F5 (es lo esperado). |
| **F2** | Frontend | §6.2: middleware y las páginas. `page-permissions.spec`, `auth-middleware.spec`. | Pasan las pruebas. |
| **F3** | Frontend | §6.3 y §6.4: `menu-items.ts`, `menu-filter.ts`, `AppMenu.vue`, `home-route.ts`, atajos, barra. Sus pruebas. | Pasan las pruebas. |
| **F4** | Frontend | §6.5 y §6.6: controles internos y terceros. `stakeholder-permissions.spec`. | `npx nuxi typecheck` limpio y `grep -rn "hasRole\|hasAnyRole\|ROLES\.\|requiredRoles" app` en 0. |
| **F5** | Frontend | §6.7 y §6.8: editor de permisos, creación de usuarios, refresco tras el refresh. Pruebas del editor y del esquema. | Pasan las pruebas. |
| **F6** | Ambos | Verificación manual en local (§8), con el backend en B6. | Matriz §8 completa. |
| **F7** | Ambos | §6.9: documentación. | Hecho. |

### 7.2 Migraciones y base de datos

Todas las operaciones de esquema y de base de datos las ejecuta el agente, **solo con `dotnet ef`**, desde la raíz del backend (`code_workspace/Backend/wms-api`). Siempre se pasan los proyectos `--project Wms.Infrastructure --startup-project Wms.Api`.

**Reglas:**

1. **No se editan los archivos generados:** la migración `*_AddUserPermissions.cs`, su `.Designer.cs` y `Wms.Infrastructure/Migrations/AppDbContextModelSnapshot.cs`. Si la migración no sale como se espera:
   - Corrige el modelo (entidad, configuración o `HasData`).
   - Si ya estaba aplicada, revierte con `dotnet ef database update <migración anterior>`. La anterior es la última de la carpeta antes de `AddUserPermissions`; hoy, `20261007030137_RemoveSampleSeedData`.
   - Borra la migración con `dotnet ef migrations remove`.
   - Vuelve a generarla.
   - No borres ni muevas los archivos a mano.
2. **Solo base local.** Antes de cada `database update` o `database drop`, ejecuta `dotnet ef dbcontext info --project Wms.Infrastructure --startup-project Wms.Api`. Comprueba que el origen de datos es `localhost` o `127.0.0.1`. Si apunta a otro host, o no puedes confirmarlo, detente y pregunta. Nunca uses una cadena de conexión de staging ni de Azure, y no copies credenciales en ningún archivo ni mensaje.
3. **No se escribe SQL a mano** ni se modifican datos con clientes de base de datos. Los datos sembrados van por `HasData`. La conversión de usuarios la hace `UserPermissionsBootstrapper` al arrancar la API (§5.9).
4. **Borrar la base local** (`dotnet ef database drop --force`) solo con confirmación previa del usuario en el chat. Este plan no lo necesita.
5. **Scripts de staging:** se generan con `dotnet ef migrations script --idempotent` solo si el usuario lo pide. El despliegue lo hace el usuario.

**Comandos de la fase B1, en orden.** Cada uno en su propia línea; deben ejecutarse sin errores.

```bash
dotnet ef migrations add AddUserPermissions --project Wms.Infrastructure --startup-project Wms.Api
```

Revisa que la migración generada contenga exactamente los cambios de §5.1:
- Las tablas `permissions` y `user_permissions`.
- Las columnas `users.has_full_access` y `users.permissions_initialized_at`.
- Las 73 filas sembradas.

Si contiene algo más o le falta algo, aplica la regla 1. Después:

```bash
dotnet ef dbcontext info --project Wms.Infrastructure --startup-project Wms.Api
```

```bash
dotnet ef database update --project Wms.Infrastructure --startup-project Wms.Api
```

```bash
dotnet ef migrations has-pending-model-changes --project Wms.Infrastructure --startup-project Wms.Api
```

**De B2 a B6** no debe cambiar el esquema. Al cerrar cada una de esas fases, `dotnet ef migrations has-pending-model-changes` debe decir que no hay cambios. Si los hay, detente y pregunta: el plan no prevé otra migración.

**Base para la verificación §8:** usa la base local **existente**, sin borrarla, para que conserve los usuarios de prueba con roles.
- La migración de B1 agrega las columnas con `permissions_initialized_at` vacío.
- La primera vez que arranque la API con B3 hecho, `UserPermissionsBootstrapper` convierte a esos usuarios. Eso es lo que verifica el punto 1 de §8.
- Si la base local no tiene usuarios con roles, detente y avisa al usuario antes de seguir. No los inventes con SQL ni recreando la base.

**Despliegue a staging:** lo hace el usuario, desde las ramas `feature/permisos-por-usuario` o después de fusionarlas en `develop`; eso lo decide él.
1. Migración.
2. Backend.
3. Frontend estático.

La conversión corre sola al arrancar la API.

---

## 8. Verificación manual (F6)

Usa local, con la base local existente (§7.2, sin borrarla) y con los usuarios de prueba por rol del `README` del frontend. No copies contraseñas en ningún documento.

1. **Conversión.** Arranca la API con usuarios que tienen roles. En `GET /user/{id}/permissions`, cada uno debe tener su plantilla de §3. El Admin tiene acceso total.
2. **Menú por plantilla.** Entra con cada usuario de prueba:
   - El menú muestra las mismas pantallas que antes, salvo las diferencias de §4.4.
   - La página de inicio es la de antes: Receiving `/operations/entries`, Warehouse `/warehouse`, Billing `/billing`, Scale `/operations/weighbridge`, Admin y ForeignTrade `/`.
3. **Ejemplo del usuario.** Al operario de Facturación agrégale «Crear y editar clientes» y «Convenios». Debe pasar esto:
   - Ve «Terceros › Clientes» y «Terceros › Crear».
   - Crea un cliente; el formulario solo ofrece el rol de negocio Cliente.
   - Crea un convenio.
   - No ve «Transportadoras».
   - Al abrir `/admin/stakeholders?rol=TRANSPORT_COMPANY` a mano, va a «Acceso denegado».
4. **Quitar una pantalla.** A un usuario de Comercio exterior quítale «Levantes». Debe pasar esto:
   - Sin cerrar sesión, en la siguiente acción el menú ya no la muestra.
   - Alt+L no hace nada.
   - Al abrir `/foreign-trade/releases`, va a «Acceso denegado».
   - Al retirar un levante desde otra sesión, no recibe la notificación «Depósito sin nacionalizar».
5. **Acciones.** Un usuario con «Historial de báscula» y sin «Anular pesaje» no ve el botón de anular. Con el permiso, lo ve y funciona.
6. **Reglas de administración.**
   - Un usuario con `admin.users` sin acceso total no puede activarse el acceso total.
   - El único usuario con acceso total no puede quitárselo.
   - «Copiar permisos de otro usuario» rellena el editor.
7. **Auditoría.** `/admin/audit` muestra «Permisos actualizados para …».

Comparte con el usuario capturas de los puntos 2 (dos plantillas), 3 y 6.

---

## 9. Resumen de archivos

**Backend: nuevos**
- `Wms.Domain/Entities/Users/Permission.cs`
- `Wms.Domain/Entities/Users/UserPermission.cs`
- `Wms.Domain/Enums/PermissionKind.cs`
- `Wms.Domain/Security/WmsPermissions.cs`
- `Wms.Domain/Security/PermissionImplications.cs`
- `Wms.Domain/Security/RolePermissionPresets.cs`
- `Wms.Domain/Services/IUserPermissionStore.cs`
- `Wms.Infrastructure/Persistence/Configurations/Users/PermissionConfiguration.cs`
- `Wms.Infrastructure/Persistence/Configurations/Users/UserPermissionConfiguration.cs`
- `Wms.Infrastructure/Services/UserPermissionStore.cs`
- `Wms.Api/Common/Identity/PermissionRequirement.cs`
- `Wms.Api/Common/Identity/PermissionAuthorizationHandler.cs`
- `Wms.Api/Common/Identity/UserPermissionsBootstrapper.cs`
- Controladores en `Wms.Api/Controllers/v1/`: `WarehouseLocationsController.cs`, `WeighbridgeDateCorrectionController.cs`, `TraceabilityReportsController.cs`, `BillingDashboardController.cs`
- En `Wms.Application/Users/`:
  - `Queries/GetPermissionCatalog/*`
  - `Queries/GetUserPermissions/*`
  - `Commands/SetUserPermissions/*`
  - `Commands/CreateUserWithPermissions/*` (renombrado)
  - `Common/ActiveFullAccessCounter.cs` (renombrado)

**Backend: modificados**
- **Dominio:** `WmsPolicyRoles.cs` (pasa a `WmsPolicies.cs`), `ApplicationUser.cs`, `ITokenService.cs`, `INotificationService.cs`.
- **Infraestructura:** `TokenService.cs`, `NotificationService.cs`, `AppDbContext.cs`, `SeedDataExtensions.cs`, `ApplicationUserConfiguration.cs`, `DependencyInjection` (Infrastructure).
- **API:**
  - `WmsAuthentication.cs`, `BootstrapAdminSeeder.cs`, `Program.cs`
  - `NotificationHub.cs`, `NotificationOrchestrator.cs`, `SignalRNotifier.cs`
  - Controladores: `UserController`, `AdministrationController`, `CitiesController`, `CrewsController`, `EntryReasonController`, `ProductController`, `BackupsController`, `LegacyImportController`, `ServiceController`, `ForkliftRateController`, `StakeholderController`, `WeighbridgeVoidController`, `InventoryAdjustmentController`, `WarehouseController`, `WeighbridgeController`, `ReportController`, `BillingController`.
- **Aplicación:**
  - `LoginHandler`, `RefreshTokenHandler`, `UserInfoDto`, `UserDto`, `UserMapper`
  - `GetUsersHandler`, `ManageUserActivationHandler`, `UserAdministrationRules`
  - `RequestPasswordResetHandler`, `PasswordResetEligibility`, `StatisticsVisibility`
  - `INotificationOrchestrator`, `IRealtimeNotifier`, `TraceabilityNotification`, `DepositCancellationNotices`
  - Las llamadas de §5.8

**Backend: borrados**
- `Users/Commands/AssignRolesToUser/*`
- `Users/Commands/RemoveRolesToUser/*`
- `ActiveAdminCounter.cs` (renombrado)

**Frontend: nuevos**
- En `app/utils/`: `permissions.ts`, `home-route.ts`, `menu-items.ts`, `menu-filter.ts`, `stakeholder-permissions.ts`
- En `app/features/users/`:
  - `components/UserPermissionsEditor.vue`, `components/UserPermissions.vue`
  - `composables/usePermissionCatalog.ts`, `composables/useUserPermissions.ts`, `composables/useSetUserPermissions.ts`
- Las pruebas nuevas de §6.10

**Frontend: modificados**
- **Estado y tipos:** `stores/auth.ts`, `app/composables/usePermissions.ts`, `app/types/page-meta.d.ts`, `app/features/auth/types/login.ts`, `app/features/users/types/user.ts`, `types/requests.ts`.
- **Arranque y navegación:**
  - `app/middleware/auth.global.ts`
  - `app/plugins/auth-init.client.ts`, `app/plugins/api-client.ts`
  - `useCurrentUser.ts`, `useLogin.ts`
  - `useGlobalShortcuts.ts`
  - Las 86 páginas de §6.2
- **Diseño:** `AppMenu.vue`, `AppTopbar.vue`, `AppSidebar.vue`, `AppBreadcrumb.vue`, `AppRightMenu.vue`, `AppMenuProfile.vue`, `access-denied.vue`, `error.vue`, `change-password.vue`.
- **Pantallas y componentes:** `TraceabilityStats.vue`, `DepositProductsTable.vue`, `WeighbridgeCycleTickets.vue`, el bloque compartido del detalle de depósitos, `StakeholderForm.vue`, `StakeholderBusinessRoles.vue`, la tabla de terceros, `UserForm.vue`, `user-create-schema.ts`, `user-service.ts`, `pages/admin/users/[id].vue`.
- **Documentación:** `README.md`.

**Frontend: borrados**
- `useAuthForeignTrade.ts`, `weighing-permissions.ts` (y su prueba), `role-routes.ts` (y su prueba)
- `UserRoles.vue`, `useAssignRoles.ts`, `useRemoveRoles.ts`

---

## 10. Estimación

Es un orden de magnitud, no un compromiso.

| Bloque | Días-persona |
| --- | --- |
| B1-B6 | 10-12 |
| F1-F5 | 9-11 |
| F6-F7 | 2 |
| **Total** | **21-25** |

---

## 11. Correcciones pendientes antes de retomar

Salen de la revisión del 7 de octubre de 2026, hecha contra el código de `develop` (backend `f6f1828…ae36ac9`+, frontend `f63439c`). El resto del plan quedó verificado:
- las 15 políticas;
- las plantillas de conversión del §3, que reproducen el acceso actual rol por rol;
- el catálogo de 73 permisos (66 pantallas y 7 acciones);
- las ~32 llamadas `NotifyRoleAsync` y las 9 `SendToRoleAsync` del §5.8;
- los usos de roles en el backend y el frontend.

**Al retomar,** vuelve a verificar todo contra el código de ese momento: el sistema habrá cambiado.

### 11.1 Decisiones que el usuario debe tomar (y luego reflejar en §1)

| # | Tema | Problema | Recomendación |
| --- | --- | --- | --- |
| R1 | **Escalada de privilegios** | Un usuario con `admin.users` sin acceso total puede concederse **a sí mismo** los demás permisos. El plan solo le impide activarse el acceso total, así que en la práctica sería administrador. | Que un usuario sin acceso total solo pueda conceder permisos que él mismo tiene, validado en `SetUserPermissionsCommandHandler` y en la creación de usuarios. La alternativa es que la administración de usuarios exija acceso total. |
| R2 | **Respaldos e importación del legacy** | `SystemAdministration` se cumple con `admin.parameters`. Quien reciba «Parámetros del sistema» obtiene también `BackupsController` y `LegacyImportController`, que pueden cargar datos masivos. | Que respaldos e importación exijan **acceso total**, sin un permiso que se pueda conceder. `admin.parameters` queda solo para los parámetros. |
| R3 | **Ramas** | El §0 y el §7.0 exigen la rama `feature/permisos-por-usuario`. La regla vigente del proyecto es trabajar en `develop` sin ramas. | Confirmar con el usuario cuál aplica para este cambio y ajustar el §0 y el §7.0. |
| R4 | **Avisos del acceso total** | El cambio intencional 1 (§4) hace que el acceso total reciba **todas** las notificaciones. Hoy el Admin solo recibe las dirigidas a Admin. | Que el acceso total reciba solo las de `admin.audit` y `admin.parameters`, como hoy, salvo que también tenga marcado el permiso del aviso. Ajustar `GetActiveUserIdsWithPermissionAsync`. |

### 11.2 Fase nueva F8: lo que depende de los roles fuera del código de la aplicación

El plan no lo contempla, y se rompería o quedaría desactualizado:

| Elemento | Dónde | Qué cambiar |
| --- | --- | --- |
| Herramienta del piloto de videos | `Frontend/wms/tools/video-tutoriales/` | `siembra/piloto.mjs` crea usuarios con `rolIds` y lee `administration/system-roles`: debe pasar a `hasFullAccess` y `permissions`. `videos/1.1.mjs` hace clic en «Seleccione uno o varios roles»: debe grabar el editor de permisos. |
| Guiones de los videos | `Backend/wms-api/docs/guiones/` y el PDF v2.0 | El guion 1.1, «Cómo crear un usuario y asignarle roles», pasa a «…y asignarle permisos». Los REQUISITOS escritos por rol pasan a «usuario con los permisos de…». Hay que regenerar el PDF. |
| Scripts de cuentas de staging | `code_workspace/db_legacy/trabajo/crear-cuentas-qa-staging.sh` y `crear-cuentas-operarios-staging.sh` | Usan `rolIds` en `POST user`. Deben pasar a `permissions` con las plantillas del §3. |
| Guía de pruebas para operarios | `Backend/wms-api/docs/migracion-staging/resultados/guia-pruebas-operarios.md` | Las cuentas por rol y los mensajes de «Acceso Denegado» por rol. |
| Guía rápida de entrega al cliente | `db_legacy/trabajo/entrega/` y la versión sin credenciales en `resultados/` | La tabla por puesto sigue valiendo. Revisar los textos que hablen de rol. |
| QA | `Frontend/wms/docs/qa/fase-09-roles-permisos.md` y `resultados/informe-final.md` | Rehacer la matriz de roles como matriz de permisos y plantillas. Ejecutar una ronda de QA del cambio, como mínimo: F0, F9, la suite REG y la administración de usuarios. |
| Documento de contexto | `code_workspace/docs/contexto-negocio-wms-para-ia.md` §3 y §11 | Ya está en F7. Recordar que hoy está desactualizado incluso respecto del modelo de roles: lista 8 políticas cuando hay 15. |

### 11.3 Staging y despliegue

- **Cuándo desplegar:** después de la ventana de pruebas de los operarios y de PRF-002, nunca a mitad de ellas.
- **Conversión:** al arrancar, los usuarios existentes de staging se convierten solos con el §5.9 (`admin`, `qa.*` y `operario.*`).
- **⚠️ Respaldos:** el punto de restauración «listo para operarios» (`wms_20261007_020011_a564692e.dump`) y los anteriores son **previos** a la migración `AddUserPermissions`.
  - Restaurarlos después del despliegue exige volver a aplicar la migración y dejar que la conversión corra otra vez.
  - Saca un respaldo nuevo después del despliegue y actualiza la sección «Volver a empezar» de la guía de operarios.
- **Script de migración:** el despliegue a staging necesita `staging.sql` regenerado con `dotnet ef migrations script --idempotent`. El §7.2 regla 5 lo deja «solo si el usuario lo pide»: inclúyelo en el procedimiento de despliegue.

### 11.4 Compuertas del proyecto

**Reemplaza** las del §0.6 y del §7.1 por las que se usan en este repositorio:
- **Backend:** `dotnet build` sin errores ni advertencias nuevas, `dotnet test` de `Wms.Tests` y `Wms.IntegrationTests`, y `dotnet ef migrations has-pending-model-changes`.
- **Frontend:** `yarn test`, `yarn build` y **`yarn lint` sin pasar del tope vigente**, que hoy es 279 errores, con 0 errores en archivos nuevos.
- **`npx nuxi typecheck`** reporta muchos errores ajenos al cambio. No lo uses como criterio de cierre de fase; si hace falta revisar tipos, usa `vue-tsc` acotado a los archivos tocados.

### 11.5 Otros

- **El análisis** (`analisis-impacto-permisos-granulares-2026-10-07.md`) quedó **reemplazado** por este plan. Recomendaba la opción A, pero las decisiones del usuario llevaron a otro modelo. Además dice que las migraciones las genera el usuario, y hoy las opera el agente con `dotnet ef`.
- **Estimación:** súmale a la del §10 la F8 y la ronda de QA, entre 3 y 5 días-persona más.
