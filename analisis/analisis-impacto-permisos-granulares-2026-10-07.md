# Análisis de impacto: permisos granulares por usuario

> ## ⏸ Estado: REEMPLAZADO y DIFERIDO
>
> - **Reemplazado** por `plan-cerrado-permisos-por-usuario-2026-10-07.md`. Las decisiones del usuario (P01 a P14 del plan) llevaron a un modelo distinto de la opción A que se recomienda aquí: cada usuario se configura desde cero y las reglas del API se calculan a partir de los permisos.
> - **Diferido** el 7 de octubre de 2026: el sistema sale a producción con el modelo de roles actual. No hubo solicitud del cliente.
> - Se conserva como referencia del estado del código a esa fecha. Su §2, «Cómo funciona hoy», sigue describiendo bien el modelo de roles vigente.
> - **Una afirmación ya no aplica:** «los cambios de esquema los genera el usuario» (§4.1). Hoy las migraciones las opera el agente con `dotnet ef`.

> **Fecha:** 7 de octubre de 2026. Backend `wms-api` y frontend `wms`, rama `develop` (frontend en `429be4d`).
> **Pedido:** pasar del acceso por rol a permisos configurables por usuario: qué rutas e ítems del menú ve cada uno. Hoy, por ejemplo, Comercio exterior ve todo el módulo de Comercio exterior y nada más.
> **Alcance de este documento:** solo análisis. No hay cambios de código ni de esquema.

---

## 1. Resumen

1. **El rol está en ocho piezas del frontend y en seis del backend.** En el backend, el rol es un `enum`, viaja como claim del JWT, decide las 15 políticas que protegen 352 acciones, define los grupos de SignalR y elige a quién se notifica. En el frontend, el rol decide 86 páginas, el menú, la página de inicio, los atajos y 22 botones o secciones.
2. **El costo depende de una sola decisión: ¿el permiso por pantalla también protege la API, o solo la oculta?**
   - **Solo visibilidad** (fase 1): cambia el menú, el middleware y la administración de usuarios. Las políticas del backend no se tocan. Costo moderado, riesgo bajo.
   - **Seguridad real por pantalla** (fase 2): hay que reetiquetar las 352 acciones y rehacer las notificaciones y las pruebas de integración. Costo alto.
3. **Recomendación:** usar los roles como **plantillas de permisos** y permitir **excepciones por usuario**.
   - Fase 1: un catálogo de permisos por pantalla. El usuario ve las pantallas de sus roles, menos las que el administrador le quite.
   - Fase 2: aplicar el mismo catálogo en la API, solo si el cliente necesita que la restricción sea de seguridad y no solo de interfaz.
   - Con este orden no se rompen las pruebas actuales: sin excepciones configuradas, cada usuario ve exactamente lo que ve hoy.

---

## 2. Cómo funciona hoy

### 2.1 Backend (`Backend/wms-api`)

| Pieza | Dónde | Cómo depende del rol |
| --- | --- | --- |
| **Modelo** | `ApplicationRole : IdentityRole<Guid>`, tabla `system_roles`, `SystemRolesCode` (`Wms.Domain/Enums/SystemRolesCode.cs`) | Son 6 roles fijos sembrados con `HasData` (`SeedDataExtensions.cs:69-130`). No hay endpoints para crearlos ni editarlos. Las tablas `AspNetUserClaims` y `AspNetRoleClaims` existen, pero ningún código las usa. |
| **Token** | `TokenService.cs:61-89` | El JWT lleva un `ClaimTypes.Role` por rol y el claim `sstamp`. No lleva permisos. |
| **Login y `/user/me`** | `LoginResponseDto`, `UserDto` | El login devuelve `user.roles: string[]` (códigos). `/user/me` devuelve `roles: [{id, code, name}]`. |
| **Políticas** | `Wms.Domain/Security/WmsPolicyRoles.cs` y `WmsAuthentication.cs:92-104` | 14 políticas por rol más `ActiveUser` (ver tabla abajo). |
| **Controladores** | `Wms.Api/Controllers/v1` (51 controladores, 352 acciones) | La política va como literal: `[Authorize(Policy = "…")]`. No hay `[Authorize(Roles=…)]`. Hay 8 controladores «partidos» porque los `[Authorize]` se suman (ver §2.3). |
| **Reglas en código** | `StatisticsVisibility.cs` (bloque de facturación solo para Admin), `PasswordResetEligibility.cs` (recuperación de contraseña solo para Admin), `UserAdministrationRules.cs` y `ActiveAdminCounter.cs` (siempre debe quedar un Admin activo) | Comparan el rol directamente. |
| **Notificaciones** | `NotificationOrchestrator.NotifyRoleAsync` (unos 30 puntos), `SignalRNotifier.SendToRoleAsync` (4 puntos y `TraceabilityNotification`, que se llama desde 17 handlers) | Los destinatarios se buscan con `GetUsersInRoleAsync(code)`. Al conectarse, el hub une al usuario a los grupos `role:{code}` (`NotificationHub.cs:26-32`). |
| **Revocación** | `UserSessionGuard` (caché de 15 s) y el claim `sstamp` | Asignar o quitar un rol rota el stamp: el token viejo recibe 401 y el refresh devuelve los roles nuevos. Es un mecanismo reutilizable. |
| **Auditoría** | `AssignRolesToUserHandler`, `RemoveRolesToUserHandler` | `AspNetUserRoles` no es `IAuditable`. Por eso se registra una descripción con `auditContext.Describe(...)`. Los roles asignados al crear el usuario no quedan auditados. |

Políticas vigentes (`WmsPolicyRoles.cs`):

| Política | Roles | Acciones que protege |
| --- | --- | --- |
| `ForeignTradeAccess` | Admin, ForeignTrade | 84 |
| `BillingAccess` | Admin, Billing | 57 |
| `AdminOnly` | Admin | 44 (+3 combinadas con `WarehouseAccess`) |
| `ScaleAccess` | Admin, Scale | 37 |
| `WarehouseAccess` | Admin, Warehouse | 35 |
| `StakeholderAccess` | Admin, ForeignTrade | 10 |
| `GateAccess` | Admin, Receiving | 8 |
| `OperationalAccess` | Admin, Warehouse, Receiving, Scale | 5 |
| `TransportCatalogAccess` | Admin, Receiving, Scale, ForeignTrade | 4 |
| `InventoryReportAccess` | Admin, ForeignTrade, Warehouse, Billing | 4 |
| `NoveltyReadAccess` | Admin, Warehouse, ForeignTrade | 3 |
| `WeighingCorrectionAccess` | Admin, Scale, Billing | 2 |
| `EntryCorrectionAccess` | Admin, Receiving | 1 |
| `DepositEntryDateAccess` | Admin, Scale, ForeignTrade | 1 |
| `ActiveUser` / `[Authorize]` / anónimo | — | 30 / 17 / 9 |

> **El documento de contexto está desactualizado.** §3 de `docs/contexto/contexto-negocio-wms-para-ia.md` lista 8 políticas e incluye `Receiving` en `WarehouseAccess`. El código tiene 15 políticas y `WarehouseAccess` ya no incluye Vigilancia (DEF-F9-002).

### 2.2 Frontend (`Frontend/wms`)

| Pieza | Dónde | Cantidad |
| --- | --- | --- |
| **Estado** | `stores/auth.ts`: `roles: string[]` y `hasRole()` | Los roles llegan del login y de `/user/me`, y no se guardan en `localStorage`. **No se recargan tras un refresh de token.** |
| **Composable** | `app/composables/usePermissions.ts`: `ROLES`, `hasRole`, `hasAnyRole` | `canAccessModule` y `MODULE_ROLES` no se usan en ningún sitio. |
| **Páginas** | `definePageMeta({ requiredRoles })` | 86 de 92 páginas. Basta uno de los roles listados. |
| **Middleware** | `app/middleware/auth.global.ts:74-81` | Es el único guardia. Si no hay acceso, `resolveDeniedRedirect` lleva al inicio del rol o a `/access-denied`. |
| **Menú** | `app/components/layout/AppMenu.vue` | Un arreglo estático. Los `roles` van **solo en los 7 grupos raíz**: un ítem hijo no se puede ocultar por separado. Varias rutas aparecen en más de un grupo (terceros, inventario general, movimientos por depósito). |
| **Resaltado del menú** | `app/utils/menu-route.ts`, `AppMenuItem.vue` (DEF-F11-022) | Las claves son posicionales (`padre-índice`) y distinguen el filtro `?rol=`. |
| **Página de inicio** | `app/utils/role-routes.ts` (`ROLE_DEFAULT_ROUTES`) | 6 entradas. El orden hace de prioridad. |
| **Atajos** | `app/composables/useGlobalShortcuts.ts` | 6 atajos con `roles`. |
| **Controles dentro de pantallas** | 15 archivos | Unos 22 controles. Ejemplos: búsqueda de placa en la barra superior, parámetros del sistema, anular, corregir o cambiar la fecha de un pesaje, ajuste de inventario, edición de terceros (Facturación solo lee), convenios, «Ver factura», validar y nacionalizar. |
| **Administración de usuarios** | `UserForm.vue` (selector múltiple `rolIds`), `UserRoles.vue` (asignar y quitar) | `POST /user/{id}/assign-roles` y `/remove-roles`. |
| **Pruebas** | `role-routes.spec`, `auth-middleware.spec`, `AppMenu.spec`, `AppMenuItem.spec`, `AccessDenied.spec`, `ErrorPage.spec`, `weighing-permissions.spec`, `user-create-schema.spec` | 8 archivos. |

### 2.3 Lo que complica el cambio

- **Un rol habilita la pantalla y también su API.** Si un usuario ve una pantalla pero no tiene la política de sus endpoints, recibe 403. Es la trampa 5 del documento de contexto: los servicios compartidos (`app/features/weighbridge`, `app/features/entries`) llaman endpoints de otros módulos.
- **Las políticas cubren módulos enteros.** `ForeignTradeAccess` abre 84 acciones a la vez. Hoy no se puede habilitar «Levantes» en la API sin habilitar todo Comercio exterior.
- **Hay pantallas fuera del menú.** Los detalles (`imports/[id]`, `exports/[id]`, `inspections/[id]`, `weighbridge/cycles/[id]`, `in-process`, `pending-reweigh`, `recover`, `admin/parameters`) necesitan heredar el permiso de una pantalla del menú.
- **Una misma ruta aparece con filtros distintos.** `/admin/stakeholders` sale en el menú como Listado, Clientes, Transportadoras y Agencias (`?rol=`). Un permiso por ruta no distingue entre ellos; uno por ítem del menú sí, pero la URL se puede editar a mano.

---

## 3. Opciones

| | A. Restricción de pantallas sobre el rol | B. Permisos por pantalla de punta a punta | C. Permisos por pantalla y por acción |
| --- | --- | --- | --- |
| **Qué permite** | Quitarle a un usuario pantallas de sus roles (p. ej. un usuario de Comercio exterior que solo ve Levantes y Depósitos). Para dar pantallas de otro módulo, se le agrega el rol y se ocultan las que sobran. | Dar o quitar cualquier pantalla a cualquier usuario. La API respeta lo mismo. | Lo de B, más botones y secciones (anular pesaje, convenios, ajuste de inventario…). |
| **¿Protege la API?** | No: la API sigue protegida por rol. Un usuario técnico podría llamar desde fuera un endpoint de una pantalla oculta. | Sí. | Sí. |
| **Backend** | Catálogo de permisos, asignación por rol y excepciones por usuario; `/me` y el login devuelven los permisos efectivos; endpoints de administración. Las políticas no cambian. | Lo de A, más: un autorizador por permiso que reemplaza a `WmsPolicyRoles`, reetiquetar las 352 acciones, rehacer el destino de las notificaciones y las reglas en código. | Lo de B, más los permisos de acción en los handlers y controladores partidos. |
| **Frontend** | `requiredPermission` en 86 páginas, menú filtrado por ítem, inicio y atajos calculados, pantalla de permisos en la administración de usuarios. | Igual que A. | A, más los 22 controles internos. |
| **Pruebas que se rehacen** | Solo las del frontend (8 archivos) y nuevas pruebas del cálculo de permisos. Las de integración del backend siguen igual. | `WmsPolicyRolesTests`, `ControllerAuthorizationTests` y los ayudantes `CreateClientForRoleAsync` (190 llamadas en 91 archivos), salvo que los roles sigan funcionando como plantillas. | Igual que B. |
| **Orden de magnitud** | 10-13 días-persona | 25-35 días-persona | 30-40 días-persona |
| **Riesgo** | Bajo | Alto (403 por endpoints compartidos, regresiones de seguridad) | Alto |

Las estimaciones solo sirven para comparar opciones. Se afinan con el plan cerrado.

**Recomendación: A ahora, con un modelo de datos que ya sirva para B.** El negocio pide controlar «qué rutas e ítems del menú puede ver un usuario», y A lo cumple. Es una WMS interna con usuarios conocidos, así que ocultar la pantalla resuelve casi todos los casos. Si después hace falta seguridad estricta, B reutiliza el mismo catálogo y las mismas tablas.

---

## 4. Diseño propuesto (opción A, preparada para B)

### 4.1 Modelo de datos

Los cambios de esquema los genera el usuario como migración.

| Tabla | Columnas | Notas |
| --- | --- | --- |
| `permissions` | `id`, `code` (único, p. ej. `foreign-trade.releases`), `module`, `name` (español), `kind` (`Screen` o `Action`), `parent_id`, `sort_order`, `is_active` | Catálogo sembrado con `HasData`. No se edita desde la UI. |
| `role_permissions` | `role_id`, `permission_id` | Plantilla por rol. La semilla reproduce exactamente el acceso actual. |
| `user_permission_overrides` | `user_id`, `permission_id`, `effect` (`Grant` o `Deny`), `created_at`, `created_by_id` | Excepciones por usuario. En la opción A solo se permite `Deny`, o `Grant` dentro de los módulos de sus roles. |

- **Permisos efectivos** = (permisos de sus roles ∪ `Grant`) − `Deny`.
- **Admin** recibe todo siempre. Así nadie bloquea al administrador; las reglas de `UserAdministrationRules` siguen igual.
- **Alternativa:** guardar los permisos en `AspNetUserClaims` y `AspNetRoleClaims`, que ya existen. Se ahorran dos tablas, pero no hay catálogo, ni orden, ni nombres en español, ni integridad referencial. No lo recomiendo.
- **Auditoría:** las tablas nuevas deben implementar `IAuditable`, o seguir el patrón `Describe` de CHG-68. Conviene corregir de paso el hueco de los roles asignados al crear el usuario.

### 4.2 Catálogo de permisos

- **Un permiso por ítem navegable del menú** (unos 55). Los grupos y submenús son nodos padre, sin permiso propio.
- Las páginas de detalle que no están en el menú heredan el permiso de su pantalla:

  | Página de detalle | Permiso que hereda |
  | --- | --- |
  | `foreign-trade/imports/[id]` | `foreign-trade.deposits` |
  | `operations/weighbridge/cycles/[id]` | Varios: báscula, facturación o comercio exterior, como hoy. |
  | `in-process`, `pending-reweigh`, `recover` | `weighbridge.process` |
  | `admin/parameters` | `admin.parameters` (nuevo; hoy depende de `hasRole(Admin)`) |

- Las rutas que se repiten en varios grupos comparten un solo permiso (`reports.general-inventory`, `reports.warehouse-movements`, `admin.stakeholders`).
- Queda por decidir si Clientes, Transportadoras y Agencias son permisos separados o uno solo (ver §6).

### 4.3 Backend (opción A)

| Cambio | Archivos |
| --- | --- |
| Entidades, configuración y semilla | `Wms.Domain/Entities/Administration/Permission.cs` (nuevo), `RolePermission`, `UserPermissionOverride`; `SeedDataExtensions.cs` |
| Servicio de permisos efectivos (con caché por usuario que se invalida al rotar el stamp, igual que `UserSessionGuard`) | `Wms.Application/Users/Common/EffectivePermissions*` (nuevo) |
| Devolver `permissions: string[]` en el login y en `/user/me` | `UserInfoDto`, `UserDto`, `LoginHandler`, `GetUserByIdHandler` |
| `GET administration/permissions` (catálogo en árbol) | `AdministrationController` |
| `GET/PUT user/{id}/permissions` (AdminOnly; reemplaza las excepciones, valida el catálogo, rota el stamp y audita) | `UserController`, comando y validador nuevos |
| `GET role/{id}/permissions` (solo lectura, para mostrar lo heredado) | `AdministrationController` |
| Pruebas: cálculo efectivo, Admin total, semilla equivalente al acceso actual, que se rote el stamp, auditoría | `Wms.Tests/Security`, `Wms.IntegrationTests/Security` |

**No cambian en la opción A:** `WmsPolicyRoles`, los 51 controladores, las notificaciones, los grupos de SignalR ni las 190 llamadas `CreateClientForRoleAsync`.

**¿Permisos dentro del JWT?** No. Unos 55 códigos inflarían el token, que además viaja en la query string del hub (`/hubs?access_token=`). En la opción A el frontend los lee de `/me`. En la opción B se resolverían en el servidor con caché.

### 4.4 Frontend (opción A)

| Cambio | Archivos |
| --- | --- |
| `permissions: string[]` y `can()` / `canAny()` en el store | `stores/auth.ts`, más los 3 lugares que cargan `/me` (`auth-init.client.ts`, `auth.global.ts`, `useCurrentUser.ts`) |
| `can` y `canAny` en el composable; borrar `MODULE_ROLES` y `canAccessModule` | `app/composables/usePermissions.ts` |
| `requiredPermission` en la meta de cada página, con el tipo en `PageMeta`; el middleware lo valida y conserva `requiredRoles` mientras convivan | `app/types/page-meta.d.ts`, `auth.global.ts`, 86 páginas |
| Menú con `permission` en cada hoja; filtrado recursivo; los grupos vacíos se ocultan | `AppMenu.vue`. Verificar `AppMenuItem.vue` y `menu-route.ts`: al filtrar hijos cambian las claves posicionales, que es justo lo que corrigió DEF-F11-022. |
| La página de inicio pasa a ser la primera pantalla permitida en orden de prioridad (en lugar de `ROLE_DEFAULT_ROUTES`) | `app/utils/role-routes.ts` y quienes lo usan: `AppTopbar`, `AppSidebar`, `AppBreadcrumb`, `useLogin`, `change-password`, `access-denied`, `error.vue` |
| Atajos, búsqueda de placa y parámetros pasan a usar permisos | `useGlobalShortcuts.ts`, `AppTopbar.vue`, `AppRightMenu.vue` |
| Pantalla «Permisos» en el detalle del usuario: árbol por módulo, casillas que muestran lo heredado del rol y lo modificado | `app/features/users/components/UserPermissions.vue` (nuevo), `app/pages/admin/users/[id].vue`, `user-service.ts` |
| Recargar `/me` tras el refresh de un token (hoy no se hace), para que los cambios se vean sin cerrar sesión | `app/plugins/api-client.ts`. Opcional: un evento SignalR `PermissionsChanged` a `user:{id}`. |
| Pruebas: menú, middleware, página de inicio, pantalla de permisos | `test/components/layout/*`, `test/components/app/*`, `test/unit/utils/role-routes.spec.ts` |

**Los 22 controles internos se quedan por rol en la opción A.** Una pantalla visible conserva sus botones según el rol, igual que hoy. Pasan a permisos de acción en la opción C.

### 4.5 Qué se suma en la opción B (si se pide después)

1. **Autorización por permiso:**
   - Un `IAuthorizationPolicyProvider` resuelve `[RequirePermission("…")]`.
   - Un `AuthorizationHandler` consulta el servicio de permisos efectivos.
   - Se retira `WmsPolicyRoles`.
2. **Reetiquetar las 352 acciones** con el permiso de la pantalla que las usa.
   - Los endpoints compartidos (catálogos, ciclo de báscula, terceros, vehículos y conductores) necesitan permisos «de lectura transversal» o varios permisos.
   - Los controladores partidos (`WeighbridgeCatalog`, `WeighbridgeShared`, `BillingPreview`, `InventoryAdjustment`, `WarehouseMovementsReport`…) dejan de ser necesarios, pero se pueden quedar donde están.
3. **Notificaciones:** cambiar `NotifyRoleAsync(role)` por `NotifyPermissionAsync(permiso)` en unos 30 puntos.
   - `SendToRoleAsync` y `TraceabilityNotification` envían a `user:{id}` en lugar de a `role:{code}`. Así no hay que volver a unirse a grupos cuando cambian los permisos.
4. **Reglas en código:**

   | Regla | Pasa a |
   | --- | --- |
   | Bloque de facturación en estadísticas | `reports.statistics.billing` |
   | Recuperación de contraseña | Puede seguir por rol |
   | «Último administrador» | Sigue por rol |

5. **Pruebas de integración:** los ayudantes por rol siguen sirviendo si la semilla de `role_permissions` reproduce el acceso actual. Hay que reescribir `WmsPolicyRolesTests` y `ControllerAuthorizationTests`, y agregar una matriz por permiso.

---

## 5. Riesgos

| Riesgo | Mitigación |
| --- | --- |
| La semilla de `role_permissions` no reproduce el acceso actual y alguien pierde una pantalla | Una prueba que compare, rol por rol, el menú visible antes y después (`AppMenu.spec`, matriz por rol). |
| **Opción A:** una pantalla oculta sigue accesible por la API | Documentarlo como restricción de interfaz. Si el cliente exige seguridad, pasar a la opción B. |
| **Opción B:** 403 en pantallas que usan servicios de otro módulo | Inventariar las llamadas de cada pantalla antes de etiquetar. Probar en staging con usuarios de pantallas sueltas. |
| La UI queda desactualizada tras un cambio de permisos | Rotar el stamp, recargar `/me` tras el refresh y, opcionalmente, empujar el cambio por SignalR. |
| Un usuario no puede entrar a ningún sitio porque se le quitaron todas las pantallas | Validar en `PUT user/{id}/permissions` que quede al menos una pantalla, o mandarlo a `/notifications`. |
| Se rompe el resaltado del menú (DEF-F11-022) al filtrar hijos | Repetir los casos de `AppMenuItem.spec` con menús filtrados. |
| Hay que mantener a la par el catálogo, las páginas y el menú | Una prueba que recorra `app/pages` y exija que cada página declare un permiso que exista en el catálogo. |

---

## 6. Decisiones abiertas

1. **¿Basta con ocultar la pantalla (opción A) o la API también debe rechazar el acceso (opción B)?** Esta respuesta es la que más cambia el alcance.
2. **¿Las excepciones solo quitan pantallas, o también pueden dar pantallas de un módulo cuyo rol el usuario no tiene?** En la opción A, dar una pantalla de otro módulo exige asignarle también el rol de ese módulo, porque si no la API responde 403.
3. **¿Los roles siguen existiendo como plantillas, o se configura cada usuario desde cero?** Recomiendo plantillas: menos trabajo para el administrador, y las pruebas actuales siguen sirviendo.
4. **¿Se pueden editar los permisos de un rol desde la UI, o solo las excepciones por usuario?** Recomiendo solo las excepciones en la primera entrega.
5. **¿Qué tan fino es el permiso?**
   - ¿Por pantalla (unos 55) o también por acción (anular pesaje, convenios, ajuste de inventario…, opción C)?
   - ¿Clientes, Transportadoras y Agencias son permisos distintos o uno solo, «Terceros»?
6. **Notificaciones:** si a un usuario de Comercio exterior se le quita «Levantes», ¿deja de recibir los avisos de levantes? En la opción A las notificaciones siguen yendo por rol.
7. **¿El administrador siempre ve todo?** Recomiendo que sí, para no bloquearlo.
