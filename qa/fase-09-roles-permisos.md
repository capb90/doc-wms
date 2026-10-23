# Fase 9 — Roles, permisos y seguridad básica

> Lee antes `00-plan-maestro.md`. Usa las 9 cuentas del §4 del plan maestro.
> Para los casos `API` se usa el access token de cada cuenta (copiado de la sesión o por `POST auth/login`) y un cliente HTTP. **Solo contra datos QA.** No se intenta escalar privilegios fuera de lo descrito ni se ataca la infraestructura.

## 1. Objetivo

Verificar que cada rol ve y puede hacer exactamente lo que le corresponde, en tres capas: **menú**, **página** (`requiredRoles`) y **API** (políticas del backend). Validar los usuarios con varios roles, el comportamiento ante 401/403 y la sesión.

## 2. Matriz esperada (según el código al 2-oct-2026)

Leyenda: ✔ acceso · ✘ sin acceso (access-denied / 403) · M = aparece en el menú.

### 2.1 Páginas

| Página | Admin | Billing | FT | Receiving | Scale | Warehouse |
|---|---|---|---|---|---|---|
| `/` Trazabilidad | ✔ M | ✘ | ✔ M | ✘ | ✘ | ✘ |
| `/notifications` | ✔ M | ✔ M | ✔ M | ✔ M | ✔ M | ✔ M |
| `/admin/*` | ✔ M | ✘ | ✘ | ✘ | ✘ | ✘ |
| `/operations/entries/*` | ✔ M | ✘ | ✘ | ✔ M | ✘ | ✘ |
| `/operations/weighbridge/*` | ✔ M | ✘ | ✘ | ✘ | ✔ M | ✘ |
| `/operations/weighbridge/cycles/[id]` | ✔ | ✔ | ✔ | ✘ | ✔ | ✘ |
| `/warehouse/**` | ✔ M | ✘ | ✘ | ✘ (decisión 2-oct; hoy entra por URL, R-ADM-09) | ✘ | ✔ M |
| `/foreign-trade/**` | ✔ M | ✘ | ✔ M | ✘ | ✘ | ✘ |
| `/billing/**` | ✔ M | ✔ M | ✘ | ✘ | ✘ | ✘ |
| `/reports/general-inventory` | ✔ | ✘ | ✔ (R-ADM-03) | ✘ | ✘ | ✔ |
| `/reports/warehouse-movements` | ✔ | ✘ | ✔ | ✘ | ✘ | ✔ |
| Otros `/reports/*` | ✔ | ✘ | ✔ | ✘ | ✘ | ✘ |

### 2.2 Políticas del backend

| Política | Roles |
|---|---|
| AdminOnly | Admin |
| BillingAccess | Admin, Billing |
| ForeignTradeAccess | Admin, FT |
| ScaleAccess | Admin, Scale |
| WarehouseAccess | Admin, Warehouse, Receiving (esperado tras la decisión del 2-oct: sin Receiving en lo propio de Bodega) |
| OperationalAccess | Admin, Warehouse, Receiving, Scale |
| WeighingCorrectionAccess | Admin, Scale, Billing |
| EntryCorrectionAccess | Admin, Receiving |
| DepositEntryDateAccess | Admin, Scale, FT |
| ActiveUser | cualquier autenticado |

## 3. Criterios de entrada

1. Fases 1 a 6 aprobadas. Las 9 cuentas activas con sus roles.
2. Datos QA para operar (un depósito Draft, uno Confirmed, una factura Draft, una OC Pending).

## 4. Casos

### 4.1 Menú (MEN)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F9-MEN-001 | Menú por rol | Entrar con cada cuenta de un rol y listar los grupos del menú. | Coincide con las «M» de la matriz §2.1. | P0 | ROL |
| F9-MEN-002 | Multi-rol | `v_montenegro`, `j_coral`, `f_chosi`. | Unión de los menús de sus roles. | P0 | ROL |
| F9-MEN-003 | Parámetros | Perfil con Admin y con otro rol. | «Parámetros» solo para Admin. | P1 | ROL |
| F9-MEN-004 | Bodega para Receiving | Con `vigilancia`: menú y URL `/warehouse`. | Decisión del usuario: Vigilancia solo ve Vigilancia. Esperado: sin menú **y** access-denied en `/warehouse/**`. Hoy entra por URL (R-ADM-09) → defecto. | P1 | ROL |
| F9-MEN-005 | Búsqueda por placa | Barra superior con cada rol. | Solo Admin y FT. | P2 | ROL |

### 4.2 Páginas (PAG)

Para cada rol, abrir por URL directa una página de **cada fila** de la matriz §2.1.

| ID | Caso | Resultado esperado | P | Tipo |
|---|---|---|---|---|
| F9-PAG-001 | Admin: todas las páginas | Todas cargan. | P0 | ROL |
| F9-PAG-002 | Billing | Solo `/notifications`, `/billing/**`, `cycles/[id]`; el resto access-denied. | P0 | ROL |
| F9-PAG-003 | ForeignTrade | `/`, `/notifications`, `/foreign-trade/**`, `/reports/*`, `cycles/[id]`; el resto access-denied. | P0 | ROL |
| F9-PAG-004 | Receiving | Solo `/notifications` y `/operations/entries/*`; el resto (incluido `/warehouse/**`) access-denied. | P0 | ROL |
| F9-PAG-005 | Scale | `/notifications`, `/operations/weighbridge/*` (incluido `cycles/[id]`); el resto access-denied. | P0 | ROL |
| F9-PAG-006 | Warehouse | `/notifications`, `/warehouse/**`, `general-inventory`, `warehouse-movements`; el resto access-denied. | P0 | ROL |
| F9-PAG-007 | Multi-rol | Con `j_coral`: Billing y FT; `/admin` denegado. Con `f_chosi`: báscula y CE; `/billing` denegado. | P0 | ROL |
| F9-PAG-008 | Páginas con datos de otro rol | Con Billing, abrir `cycles/[id]` de un ciclo real. | Carga los datos (lectura con ActiveUser). | P2 | ROL |
| F9-PAG-020 | CE en Inventario general | Ver F7-REP-016. | Sin errores 403 (R-ADM-03). | P1 | ROL |

### 4.3 Acciones dentro de una página (ACC)

| ID | Caso | Rol | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F9-ACC-001 | Corregir ingreso | Receiving ✔; Warehouse (vía URL de historial) | Solo Admin y Receiving ven «Editar». | P1 | ROL |
| F9-ACC-002 | Editar fecha de ingreso del depósito | Scale ✔, FT ✔, Billing ✘ | Botón visible solo para Admin, Scale y FT en `cycles/[id]`. | P2 | ROL |
| F9-ACC-003 | Modificar pesos en `cycles/[id]` | Scale ✔, Billing ✔, FT ✘ | «Modificar #n» para Admin, Scale, Billing. | P1 | ROL |
| F9-ACC-004 | Anular pesaje / cerrar ciclo | Scale ✔, Billing ✘ | Solo Admin y Scale. | P1 | ROL |
| F9-ACC-005 | Ubicaciones (CRUD) | Warehouse ✘ (solo lectura) | Crear/editar/borrar ubicaciones solo Admin. | P2 | ROL |
| F9-ACC-006 | Servicios y tarifas de montacargas | Billing | Anotar: la UI es solo Admin pero el API permite Billing (desalineación). | P2 | ROL |
| F9-ACC-007 | Bloque de facturación en trazabilidad | FT ✘ | Solo Admin. | P3 | ROL |
| F9-ACC-008 | Atajos por rol | Ver F7-ATJ-003. | Solo los del rol. | P3 | ROL |
| F9-ACC-010 | Editar peso desde el historial | Scale, Billing | Ver F3-COR-002 (R-BAS-08). | P1 | ROL |

### 4.4 API (API)

Cada caso: llamar al endpoint con el token del rol indicado y verificar el código. Un 2xx donde se espera 403 es **CRITICAL** si permite escribir.

| ID | Endpoint (ejemplo) | Rol que **no** debería poder | Esperado | P | Tipo |
|---|---|---|---|---|---|
| F9-API-001 | `GET billing/invoices` | Scale, Warehouse, Receiving, FT | 403 | P0 | API |
| F9-API-002 | `POST billing/invoices/{id}/approve` (o la acción de aprobar) | FT, Scale | 403 | P0 | API |
| F9-API-003 | `PUT billing/warehouse-storages/{id}/trm` | FT, Scale | 403 | P0 | API |
| F9-API-004 | `POST warehouse-storages/{id}/confirm` | Scale, Billing, Warehouse | 403 | P0 | API |
| F9-API-005 | `POST loading-orders` (CE) | Billing, Scale | 403 | P0 | API |
| F9-API-006 | `POST warehouse/inventory/adjustments` | Warehouse, Scale | 403 | P0 | API |
| F9-API-007 | Registro y cobro de báscula (`weighbridge/...`) | Billing, FT, Warehouse | 403 | P0 | API |
| F9-API-008 | `PUT entry-logs/{id}/correction` | Warehouse, Scale | 403 | P1 | API |
| F9-API-009 | Escrituras de usuarios (`user/...`) | Todos salvo Admin | 403 | P0 | API |
| F9-API-010 | Crear/editar tercero (`stakeholders`) | Scale, Warehouse, Receiving | Esperado de negocio: 403. Riesgo R-ADM-07: 2xx (ActiveUser). | P0 | SEG |
| F9-API-011 | Crear/editar **convenio** y sus servicios (`stakeholders/{id}/agreement…`) | Scale, Warehouse, Receiving, FT | Esperado: 403. Riesgo R-ADM-07 ★: 2xx. Si se confirma: CRITICAL (cualquiera cambia tarifas). | P0 | SEG |
| F9-API-012 | `DELETE entry-reasons/{id}` | Scale, Warehouse, Billing | Esperado: 403. Riesgo R-ADM-07. Probar sobre `QA Motivo pesaje`. | P1 | SEG |
| F9-API-013 | Editar `RequiresWeighing` de un motivo | Scale, Billing | Igual que F9-API-012. | P1 | SEG |
| F9-API-014 | `DELETE`/editar conductores y vehículos | Billing, FT | Anotar resultado (ActiveUser). | P2 | SEG |
| F9-API-015 | Crear productos (`POST products`) | Billing, Receiving | Anotar: cualquier autenticado puede crear. | P2 | SEG |
| F9-API-016 | Lookups anónimos | Sin token: `administration/system-roles`, `business-role`, `taxes`, `operation-modalities`, `packaging-types` | Anotar cuáles responden sin autenticación. | P2 | SEG |
| F9-API-017 | Legacy import y backups | No Admin | 403. | P1 | API |
| F9-API-018 | `user/{otroId}` (me de otro usuario) | Cualquiera | 403 (`Forbid` si no es el propio). | P1 | SEG |
| F9-API-019 | Vigilancia y Bodega cruzados | Warehouse en entradas/salidas; Receiving en recepciones, montacargas, inventario y cargue | Esperado: 403 en ambos sentidos (decisión del 2-oct). Hoy `WarehouseAccess` incluye ambos roles → defecto. | P1 | SEG |
| F9-API-020 | Campos de autoría enviados por el cliente | Cualquier rol con permiso | Enviar `CompletedBy`/`DepartureAuthorizedById`/`AuthorizedByUserId` con el ID de otro usuario. Anotar si el sistema guarda el ID enviado (suplantación en auditoría operativa). | P1 | SEG |
| F9-API-021 | `billing/preview` y `formula-preview` | Scale, Warehouse | Responden (ActiveUser) — anotar si exponen tarifas de convenios a roles operativos. | P2 | SEG |
| F9-API-022 | `POST /drivers` y `PATCH /drivers/{id}` (política `DriverCatalogAccess`) | Warehouse **sí debe poder** | No 403: `POST` válido → 201 (o 400/409 por datos, nunca 403); `PATCH` sobre un conductor `QA-SEL` → 200. | P1 | SEG |
| F9-API-023 | `POST /vehicles` (sigue en `TransportCatalogAccess`) | Warehouse | 403. | P1 | SEG |
| F9-API-024 | `POST /drivers` | Billing | 403. | P1 | SEG |
| F9-API-025 | `GET /drivers?search=…` | Sin sesión (sin token) | 401. | P2 | SEG |

> Casos 022-025 agregados el 2026-10-08 por el selector de conductor (plan `docs/planes/plan-cerrado-selector-conductor-2026-10-08.md`).

### 4.5 Navegación, 401 y 403 (NAV)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F9-NAV-001 | Access-denied | Con Scale abrir `/billing`. | Página access-denied. | P0 | ROL |
| F9-NAV-002 | Volver desde access-denied | En access-denied. | Esperado: forma de volver a su ruta. Hoy solo «Cerrar sesión» (R-ADM-08). | P2 | UX |
| F9-NAV-003 | 403 del API en una página permitida | Provocar un 403 real (F7-REP-016). | Esperado: mensaje claro de permiso. Riesgo R-ADM-02: «Error 403 / Error interno del servidor». | P1 | ERR |
| F9-NAV-004 | Logo | Con Scale, Warehouse, Billing, Receiving: clic en el logo. | Esperado: su ruta por defecto. Riesgo R-ADM-08: access-denied. | P2 | UX |
| F9-NAV-005 | Ruta por defecto tras login | Cada rol y multi-rol. | Prioridad: Admin/FT → `/`; Receiving → entries; Warehouse → `/warehouse`; Billing → `/billing`; Scale → báscula. `f_chosi` (Scale + FT) → `/`. | P1 | ROL |

### 4.6 Sesión y cambios de rol (SES)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F9-SES-001 | Cambio de rol con sesión abierta | Admin quita Billing a `j_coral` mientras está conectado. | Anotar cuándo pierde el acceso: UI hasta recargar/re-login; API hasta que expire el token. | P1 | SEG |
| F9-SES-002 | Usuario desactivado | Ver F1-USR-015. | Documentado. | P1 | SEG |
| F9-SES-003 | Grupos SignalR tras cambio de rol | Tras F9-SES-001, generar un aviso para Billing. | Anotar si `j_coral` lo sigue recibiendo hasta reconectar. | P2 | SEG |
| F9-SES-004 | Token manipulado | Cambiar un carácter del access token y llamar `user/me`. | 401. | P1 | SEG |
| F9-SES-005 | Token de otro ambiente | (Si aplica) usar un token de staging en local. | 401. | P3 | SEG |
| F9-SES-006 | Tokens en `localStorage` | Revisar almacenamiento. | Anotar: tokens en `localStorage` (riesgo XSS). OBSERVACIÓN. | P3 | SEG |

### 4.7 Seguridad básica de entrada (INP)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F9-INP-001 | HTML en campos de texto | Nombre de tercero `QA <b>negrita</b><img src=x onerror=alert(1)>`; ver listados, detalle, PDF. | Se muestra como texto; no ejecuta script. | P1 | SEG |
| F9-INP-002 | Texto largo | Observaciones con 10.000 caracteres donde no hay límite visible. | Rechazo controlado o truncado; sin 500. | P2 | ERR |
| F9-INP-003 | Caracteres SQL | Filtro de búsqueda `' OR 1=1 --`. | Sin error; sin resultados inesperados. | P2 | SEG |
| F9-INP-004 | Errores crudos de base de datos | Provocar un duplicado al editar (F1-TER-008). | Anotar si el mensaje expone texto de Postgres (R-ADM-06). | P2 | SEG |

## 5. Criterios de salida específicos

- P0 de MEN, PAG y API ejecutados para los 6 roles y 3 multi-rol.
- Cualquier 2xx de escritura donde la matriz dice ✘ → defecto CRITICAL informado.
- Riesgos verificados: R-ADM-02, 03, 05, 07, 08, 09; R-BAS-08; R-BOD-08.
- La matriz §2 actualizada con lo observado (anexo del informe).

## 6. Entregables

Informe con la matriz observada (páginas, menú, API) y diferencias frente a la esperada, defectos. Detenerse.
