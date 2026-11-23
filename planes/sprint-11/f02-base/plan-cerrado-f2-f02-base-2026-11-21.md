# Plan cerrado — Fase 2 · F02 Base transversal

> **Fecha:** 21 de noviembre de 2026. **Estado:** Aprobado por el usuario el 2026-11-21 («Aprobar»). En ejecución desde que se lanzan sus prompts (§11).
> **Origen:**
> - `DEC-080` y el análisis funcional `levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md` §3.1 a §3.3, con los wireframes de `fase_2-mockups/transversales.html` (P-TR-01 a P-TR-06 y P-TR-09 a P-TR-11);
> - el plan maestro `planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md` (M1 a M24, `DEC-081`);
> - AF dueñas (10, plan maestro §3.1): AF-38, AF-54, AF-99, AF-127, AF-128, AF-129, AF-130, AF-131, AF-132, AF-134;
> - las respuestas del usuario a la ronda de preguntas de F01 y F02 (2026-11-21), registradas en D1 a D4.
>
> **Base:** BE `fase-2` `529bda7` · FE `fase-2` `3aa6e3c` · docs `main` `91f0632`. Rama: `f2/f02-base` (FE).
> **Partes:** 2 (maquetación, cinco fases). El contrato (parte 0) y la integración (parte 3, I-01) están en el plan de F01: `planes/sprint-11/f01-nucleo/plan-cerrado-f2-f01-nucleo-2026-11-21.md` §2 y §13. Este plan cita el contrato y no lo repite.
> **Migraciones:** ninguna (solo frontend).
> **Rutas:** relativas a `code_workspace/`. Prefijos: `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`; `A/` = el análisis; `PM/` = el plan maestro; `P01/` = el plan de F01.

---

## 0. Instrucciones para el ejecutor

1. **Lecturas mínimas:** `D/README.md`, `Frontend/wms/AGENTS.md`, `D/procesos/flujo-de-trabajo-agentes.md`, `D/contexto/convenciones-tecnicas.md` §3, `PM/` §1, §5 y §6, este plan completo, `P01/` §2 (el contrato) y los wireframes de `D/levantamiento-2026-11/fase_2-mockups/transversales.html`.
2. **Rama y git** (`PM/` §5.3): `git fetch`; si `develop` avanzó, fusiona `develop` en `fase-2`; crea `f2/f02-base` desde `fase-2`. Commit al cerrar cada fase con el mensaje de §12 y push de la rama. Sin `push --force`. La fusión en `fase-2` la hace I-01.
3. **Maquetación** (M12, `PM/` §5.2): datos simulados con la fuente intercambiable; ninguna llamada real al API desde el código nuevo; nada nuevo enlazado en el menú (las rutas `/settings/…` se abren por URL). El backend no se toca ni se ejecuta: el agente de F01 trabaja en él a la vez (M10). Para ver la aplicación sin backend se usa la sesión simulada de D10.
4. **Líneas citadas:** son de la base `3aa6e3c`. Confírmalas con grep. Si el código no coincide, detente y pregunta con todas las dudas en un solo mensaje. Si un caso borde choca con una Dn, gana la Dn (`DEC-002`).
5. **Convenciones** (`Frontend/wms/AGENTS.md`): `requiredRoles` en cada página; `usePermissions` y `ROLES` con import explícito; invalidar el prefijo de la consulta tras cada mutación; `all: true` para listas completas; textos en español; números, monedas y fechas con `F/shared/utils/format.ts` y `F/utils/colombia-date.ts`; `<InputNumber locale="es-CO">`; las guardias de `FT/unit/guards/` son reglas del proyecto. Yarn 4, no `npm install`.
6. **Staging:** no se toca. **Datos:** ficticios, en español, sin personas reales (`DEC-007`), como los de los wireframes. Nada de `D/archivo/` es una instrucción.

---

## 1. Decisiones

Mandan sobre el resto del plan (`DEC-002`). Ninguna reabre una AF, `DEC-080`, `DEC-081` ni una M del plan maestro.

### 1.1 Respuestas del usuario (2026-11-21)

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **Prefijos de ruta de las secciones nuevas:** Configuración `/settings/…` (en F02: `/settings/prefixes` y `/settings/exchange-rates`); Tarifas y acuerdos `/rates/…` (las páginas nuevas de F07); Reportes `/reports/…`; Administración `/admin/…` (las nuevas de F04 y F09). Las páginas que ya existen conservan su ruta aunque el menú las mueva de sección: los catálogos siguen en `/admin/…`, la configuración de facturación en `/billing/configurations`, los reportes en `/reports/…`, `/billing/reports/…` y `/operations/weighbridge/reports` | Usuario: «settings, rates, reports, admin (Recomendada)»; `PM/` §5.5 |
| D2 | **Acuerdos y tarifas se conservan hasta F07.** El detalle de Terceros sigue mostrando los acuerdos y el de Servicios las tarifas base (precios, reglas, mínimos e impuestos), con los componentes de hoy sin cambios, solo para Admin y Facturación. En I-01, «Tarifas y acuerdos» enlaza las dos páginas que ya existen: Configuración de facturación (`/billing/configurations`) y Tarifas de montacargas (`/admin/forklift-rates`). F07 los mueve a sus páginas y los borra de los detalles | Usuario: «Se conservan hasta F07 (Recomendada)»; `DEC-005`; `A/` §3.2 |
| D3 | **Listados del menú que ninguna feature rediseña van a la feature de su módulo:** Vigilancia › Historial (`/operations/entries/history`) a F03; Bodega › Inventario (`/warehouse/inventory`) y Novedades (`/warehouse/novelties`) a F04; CE › Abandono y prórrogas (`/foreign-trade/abandonment`) y Listas de empaque (`/foreign-trade/packing-lists`) a F05; Notificaciones (`/notifications`) a F09. La guardia nueva (D14) los lista como pendientes con esa feature, y cada integración los saca. El texto para el plan maestro está en §10 | Usuario: «La feature de su módulo (Recomendada)»; AF-99, AF-129 |
| D4 | **Componentes compartidos nuevos, con prefijo `App`**, en `F/components/app/`: `AppDataTable`, `AppSearchSelect`, `AppDetailDrawer`, `AppCrudDialog` y `AppChargeForm` (§2). No llaman al API: reciben funciones o datos. `AppTable` (`F/components/app/AppTable.vue`, 15 páginas y `AgreementsList`), `AppPageHeader` (60 archivos) y `BillingCollectForm` (`F/features/billing/components/BillingCollectForm.vue`) se quedan para las pantallas que aún no se rediseñan y los borra la feature que migra su último uso | Usuario: «Nuevos con prefijo App (Recomendada)» |

### 1.2 Menú, permisos y páginas

| # | Decisión | Fuente |
| --- | --- | --- |
| D5 | **Menú de P-TR-01** (`F/components/layout/AppMenu.vue:9-520`), ítems de un solo nivel, sin «Listado» ni «Crear» (AF-127). F02 deja en su rama estas secciones, con rutas que ya existen; I-01 agrega Prefijos y Tasas de cambio. Las secciones de módulo (Vigilancia, Báscula, Bodega, CE y Facturación) conservan sus ítems de hoy hasta que su feature los rediseñe (`PM/` §2.2), salvo lo que P-TR-01 mueve a otra sección. Tabla completa en §1.5 | AF-127; `PM/` §2.2 (fila `AppMenu.vue`), M4 |
| D6 | **Roles de las páginas** (`requiredRoles`, AF-127, AF-128): Configuración, Admin, ForeignTrade y Billing, salvo Prefijos (Admin, ForeignTrade) y Parámetros (Admin); Tarifas y acuerdos, Admin y Billing; Administración (Usuarios y Auditoría), Admin. Las páginas de Configuración cambian hoy de `["Admin"]` (por ejemplo `F/pages/admin/drivers/index.vue:19`) a la tabla de §1.5; Terceros ya tiene Admin, ForeignTrade y Billing (`F/pages/admin/stakeholders/index.vue:22`). Dentro de una página, cada acción se muestra solo si la política de su endpoint la permite (`P01/` §2.0): por ejemplo, Facturación ve los servicios y sus tarifas, CE ve los servicios sin tarifas | AF-127, AF-128; `DEC-005` |
| D7 | **Sin retrocesos:** Vigilancia, Báscula y Bodega no entran a Configuración, pero sus formularios de hoy conservan su «+» de alta rápida, que no cambia en F02 (`DEC-005`; `A/` §3.1). Bodega sigue creando posiciones desde la recepción | `DEC-005`; AF-127 |

### 1.3 Patrones de interfaz

| # | Decisión | Fuente |
| --- | --- | --- |
| D8 | **Patrón de listado** (AF-129, AF-99, P-TR-02): sin `AppPageHeader` ni tarjeta de título; la tabla es el elemento principal, con su barra («+ Nuevo …» primario y «Exportar»); filtros por columna en una fila bajo los encabezados; orden en las columnas principales, en el servidor si la lista es paginada (C-F01-00) y en el navegador si se trae completa (`P01/` D10); filtros globales en una tarjeta tipo barra encima, solo si la página los necesita (Estado, rango de fechas); acciones solo con botones con borde o relleno, nunca de solo texto (AF-99) y nunca con clic en la fila (H-004). La raíz de la página conserva la clase `wms-page` | AF-129, AF-99; P-TR-02 |
| D9 | **Modal, drawer y página** (AF-130, P-TR-03): el CRUD de un catálogo va en `AppCrudDialog`, de una columna o de dos si pasa de 6 campos; el detalle va en `AppDetailDrawer` sobre el listado, abierto desde «Ver» y por enlace con `?id={id}` (así llegan los enlaces de otras pantallas); los formularios de operación largos siguen en página. Las páginas `create.vue`, `edit/[id].vue` y `[id].vue` de Usuarios, Terceros, Productos y Servicios se reemplazan por modal y drawer; I-01 las borra. El modal de Ubicaciones pasa a dos columnas con los campos de hoy (los del ejemplo que no existen, «Bodega», «Tipo» y «Observaciones», no se construyen: el wireframe dibuja el patrón, `A/` §3.3) | AF-130; P-TR-03 |
| D10 | **Datos simulados y sesión simulada** (M12, `PM/` §5.2): cada servicio nuevo tiene `contracts/<recurso>.ts` (los esquemas de `P01/` §2.3), `services/<recurso>.source.ts`, `mocks/<recurso>.mock.ts` y `mocks/data/<recurso>.ts`. F02 deja en `F/shared/mocks/`: `paginate`, `sortBy` y `filterBy` en memoria con las reglas de C-F01-00 (tope de 50, `all`, contiene sin tildes ni mayúsculas, rangos de fecha, enums con coma); `mockDelay` (150 a 300 ms); `mockProblem(status, description, errors?)`, que lanza `ApiError` (`F/utils/api-error.ts:9`); y la **sesión simulada**: con `NUXT_PUBLIC_MOCK_SESSION=true` y solo en `yarn dev`, un plugin inicia sesión con un usuario ficticio y los roles que se elijan (`?roles=Admin,ForeignTrade`), y apaga lo que el marco llama al API (conexión, SignalR, conteo de notificaciones, `user/me`). En `yarn build` la bandera no tiene efecto (`import.meta.dev`). `F/shared/mocks/` se queda después de I-01 para F03 a F09 | M12; `PM/` §5.2 y §6.2; M10. Ver §9, R1 |
| D11 | **Lo que no se maqueta:** las secciones de los detalles que usan endpoints de hoy sin contrato nuevo se muestran como un marcador con su nombre («Acuerdos del cliente · se conecta en I-01»): en Terceros, roles, cuentas, contactos, marca «sin salidas» y acuerdos; en Servicios, precios, reglas, mínimos e impuestos. I-01 monta ahí los componentes de hoy (`P01/` §13.1). Las acciones de Usuarios (roles, contraseña, activación) sí se maquetan, porque están en el contrato (C-F01-63 a C-F01-66) | M12 («ni tráfico HTTP»); D2 |
| D12 | **Selector con búsqueda** (AF-134, PR-27, P-TR-11): `AppSearchSelect` pagina y busca en el servidor (o en la fuente simulada) con espera de 300 ms y 20 por página, carga más al desplazarse («Mostrando 3 de 27 · desplace para cargar más»), muestra una línea secundaria (NIT, documento, embalaje) y, con `quickCreate`, un botón «+» al lado que emite `create` (AF-54, AF-92). Etiqueta encima (AF-131). Lo usan en F02 los selectores de transportadora (Vehículos) y de tercero (Cobro) | AF-54, AF-92, AF-131, AF-134 |
| D13 | **Formulario de cobro** (AF-132, AF-54, P-TR-09): `AppChargeForm` conserva los destinatarios de hoy (tercero registrado, conductor del vehículo, persona no registrada, consumidor final; `F/features/billing/components/BillingCollectForm.vue:500-548`), con «+» en «Tercero registrado» (C-F01-141); método precargado en «Efectivo»; «Referencia» solo con otro método; sin «Nota». Emite un `BillingRecipientInput` (`P01/` §2.3). No calcula tarifas: recibe el total. «Clientes» (`multiClient`) no se ofrece (`allowMultiClient` en falso por defecto); quitarlo de la guía es de F06 (AF-106). Los cobros de hoy siguen con `BillingCollectForm` hasta F03, F04 y F06 | AF-132, AF-54; `A/` §3.3 |
| D14 | **Guardia del patrón de AF-129** (reemplaza a `FT/unit/guards/page-header.spec.ts:45-53`, `DEC-058`): `FT/unit/guards/list-pattern.spec.ts` (nueva) clasifica cada ruta del menú en una sola lista: `PATTERN` (usa `AppDataTable` y no `AppPageHeader`), `PENDING` (con la feature F03 a F09 que la rediseña, incluidas las de D3) u `OUTSIDE` (con su motivo: tablero, formulario, reporte, ayuda). Verifica que toda ruta resuelve a una página, que está en una sola lista, que las de `PATTERN` cumplen, que las de `PENDING` nombran una feature y que ninguna entrada sobra. `page-header.spec.ts` se borra con `rm` (su primera prueba, rutas que resuelven a una página, pasa a la nueva) | AF-129; `PM/` §2.2, R5 |
| D15 | **Guardia «sin llamadas reales»** (`PM/` §6.2): `FT/unit/guards/mock-sources.spec.ts` (nueva) verifica que ningún archivo de `F/shared/contracts/`, `F/shared/mocks/`, `F/features/*/contracts/`, `F/features/*/mocks/`, los `*.source.ts` y los cinco componentes de D4 importa `useApi`, `$api`, `useApiQuery`, `useApiMutation` ni un servicio `*-service.ts`; los `*.source.ts` solo pueden importar su `*.http.ts`, que en la maquetación no existe; y que las páginas de la lista `MAQUETACION_PAGES` (las de F02 mientras no se integran) tampoco los importan. I-01 vacía la lista; F03 a F09 la vuelven a usar con sus páginas | `PM/` §6.2 |
| D16 | **Esquemas de los datos simulados:** una prueba Vitest por dominio (`FT/unit/<dominio>/mocks.spec.ts`) valida cada dato simulado con su esquema Zod | `PM/` §5.2 |
| D17 | **Etiquetas encima** (AF-131, AF-38): sin `FloatLabel` ni `IftaLabel` (hoy no hay ninguno); la guardia `FT/unit/guards/source-guards.spec.ts` suma la regla. **Botones** (AF-99): en las páginas `PATTERN` y en los cinco componentes nuevos, ningún `<Button>` con `text` o `variant="text"`; la misma guardia lo verifica | AF-38, AF-131, AF-99 |
| D18 | **Correcciones de AF-134:** el switch de tema responde al clic sobre él (H-080, `F/components/layout/AppConfig.vue:112`); el encabezado de los modales no tapa las alertas del contenido (H-081, regla global de `Dialog` en el tema); el detalle del usuario en el sidebar pone los roles en otra línea y el avatar no se corta (H-079, `F/components/layout/AppMenuProfile.vue:14-16`); el login tiene «ver contraseña» (PR-31, `toggle-mask` en `F/pages/auth/login.vue:90`). La tabla de pendientes en tema oscuro (H-082) es de F08 (AF-111) | AF-134; P-TR-10 |
| D19 | **Unidad de medida** (M21): F02 borra la página `F/pages/admin/unit-measures/index.vue`, su ítem del menú y lo que solo ella usa (`F/features/administration/composables/useMutationsUnitMeasures.ts`, tras comprobarlo con grep), y el rótulo de `F/features/audit/utils/entity-labels.ts`. `useUnitMeasures.ts`, `types/unit-measure.ts` y sus métodos de servicio se quedan, porque los usan pantallas de F03, F04, F05 y F07 (`TruckGoodsLines.vue`, `ReceptionStepManualInfo.vue`, `DepositProductDialog.vue`, `ReleaseForm.vue`); el último que los usa los borra. Productos se maqueta sin unidad (C-F01-69) | M21; `PM/` §2.2 |
| D20 | **Galería de componentes:** `F/pages/dev/components.vue`, solo en `yarn dev` (fuera de él responde 404) y para Admin, muestra P-TR-03 (modal y drawer), P-TR-09 (cobro con efectivo y con otro método) y P-TR-11 (selector con «+»), con datos simulados. No va en el menú (`OUTSIDE` no aplica: la guardia solo mira el menú). Sirve de referencia a F03 a F09 y se queda después de I-01 | `PM/` §6.2 (captura de cada pantalla) |
| D21 | **P-TR-02 es un ejemplo del patrón:** Conductores lleva las columnas del conductor de hoy (`P01/` C-F01-15). «Empresa de transporte» no existe en el conductor (`B/Wms.Application/Logistics/Common/Dtos/DriverDto.cs`; la empresa es del vehículo y de la entrada) y no se inventa: en su lugar va «País». El resto del wireframe (barra, filtros por columna, orden, acciones con botones) se cumple completo | `A/` §0.3 (los wireframes muestran qué va dónde con datos ficticios); P-TR-02 («ejemplo: Configuración › Conductores») |

### 1.4 Destino de las 10 AF dueñas

| AF | Decisión | Fase |
| --- | --- | --- |
| AF-38 | D17 (resuelta por AF-131) | 1 |
| AF-54 | D12, D13; C-F01-141 | 1 |
| AF-99 | D8, D14, D17 | 1 y 3 a 5 |
| AF-127 | D5, D6, D7 | 2 |
| AF-128 | D5, D6 | 2 |
| AF-129 | D8, D14 | 1 y 3 a 5 |
| AF-130 | D9 | 1 y 3 a 5 |
| AF-131 | D12, D17 | 1 |
| AF-132 | D13 | 1 |
| AF-134 | D12, D18 | 1 y 2 |

Las 10 tienen decisión y fase. F03 y F05 aplican AF-54 y AF-99 a sus pantallas con estos componentes (`PM/` §3.1, notas).

### 1.5 Menú por sección (D5, D6)

Roles entre paréntesis; «Hoy» = ruta que ya existe. Las filas marcadas **I-01** se enlazan en la integración; las marcadas con una feature llegan con ella.

| Sección | Ítem | Ruta | Roles |
| --- | --- | --- | --- |
| Notificaciones | Notificaciones | `/notifications` (hoy) | Todos |
| Dashboards | Trazabilidad | `/` (hoy) | Admin, ForeignTrade |
| Vigilancia | Ingreso · Salida · Historial | `/operations/entries`, `/operations/entries/exits`, `/operations/entries/history` (hoy) | Admin, Receiving |
| Báscula | Dashboard · Proceso de pesaje · Historial | rutas de hoy; el historial en tres páginas llega con F03 | Admin, Scale |
| Bodega | Dashboard · Recepciones (Ingresos, Recepción, Historial) · Montacargas (Registrar uso, Historial) · Órdenes de Cargue · Inventario · Novedades | rutas de hoy; «Entradas» y «Salidas» llegan con F04 y F06 | Admin, Warehouse |
| Comercio Exterior | Dashboard · Depósitos · Abandono y prórrogas · Listas de empaque · Levantes · Órdenes de Cargue · Guías de Salida | rutas de hoy; «Depósitos» por tipo, «Tickets de ingreso» y «Salidas» llegan con F05 y F06. Sale «Terceros» (lo cubre Configuración) | Admin, ForeignTrade |
| Facturación | Dashboard · Facturas · Depósitos pendientes · Pagos | rutas de hoy. Salen «Configuraciones» (a Tarifas y acuerdos), «Clientes» (a Configuración › Terceros) y los reportes (a Reportes) | Admin, Billing |
| Reportes | Reporte de báscula | `/operations/weighbridge/reports` (hoy) | Admin, Scale |
| Reportes | Diario de ingresos · Diario de salidas · Mercancía en abandono · Salidas a destino de abandono · Ingresos por producto · Ingresos por agencia | `/reports/daily-incoming-goods`, `/reports/daily-outgoing-goods`, `/reports/abandonment-candidates`, `/reports/abandonment-exits`, `/reports/incoming-by-product`, `/reports/customs-agency-entries` (hoy) | Admin, ForeignTrade |
| Reportes | Movimientos por depósito | `/reports/warehouse-movements` (hoy) | Admin, ForeignTrade, Billing |
| Reportes | Inventario general | `/reports/general-inventory` (hoy) | Admin, Warehouse, ForeignTrade, Billing |
| Reportes | Póliza | `/reports/policies` (hoy) | Admin, ForeignTrade (Facturación llega con F08, AF-111) |
| Reportes | Facturación por CPI · Facturación anual | `/billing/reports/deposit-billing`, `/billing/reports/annual` (hoy) | Admin, Billing |
| Reportes | Inventario nacionalizado · Cobros por servicio | llegan con F05 y F08 | — |
| Tarifas y acuerdos | Configuración de facturación · Tarifas de montacargas | `/billing/configurations`, `/admin/forklift-rates` (hoy; D2) | Admin, Billing |
| Configuración | Terceros · Productos · Tipos de embalaje · Tipos de unidad de carga · Servicios · Conductores · Vehículos · Motivos de ingreso · Ubicaciones · Ciudades · Cuadrillas | `/admin/stakeholders`, `/admin/products`, `/admin/packaging-types`, `/admin/cargo-unit-types`, `/admin/services`, `/admin/drivers`, `/admin/vehicles`, `/admin/entry-reasons`, `/admin/locations`, `/admin/cities`, `/admin/crews` (hoy) | Admin, ForeignTrade, Billing |
| Configuración | Prefijos | `/settings/prefixes` (**I-01**) | Admin, ForeignTrade |
| Configuración | Tasas de cambio | `/settings/exchange-rates` (**I-01**) | Admin, ForeignTrade, Billing |
| Configuración | Parámetros | `/admin/parameters` (hoy) | Admin |
| Administración | Usuarios · Auditoría | `/admin/users`, `/admin/audit` (hoy) | Admin |
| Administración | Notificaciones · Umbrales de alertas | llegan con F09 y F04 | — |
| Ayuda | Centro de ayuda | `/ayuda` (hoy) | Todos |

Sale «Unidades de medida» (D19). El orden de las secciones es el de la tabla (P-TR-01). Un ítem se ve si el usuario tiene alguno de sus roles; una sección sin ítems visibles no se muestra.

---

## 2. Contrato, componentes y pantallas

### 2.1 Contrato

El contrato es el de `P01/` §2: convenciones y C-F01-00 en §2.0, fichas en §2.2.1 y §2.2.2, esquemas Zod en §2.3. F02 copia los esquemas tal cual a sus archivos (`P01/` §2.3 da la ruta de cada uno) y deriva los tipos con `z.infer`. Si un esquema no alcanza para una pantalla, el agente se detiene y pregunta: no lo cambia por su cuenta (`PM/` R3).

Endpoints que consume F02, todos con ficha en `P01/` §2.2: C-F01-01, C-F01-03 a C-F01-06, C-F01-08 a C-F01-12, C-F01-15 a C-F01-19, C-F01-21 a C-F01-72 y C-F01-141. Las secciones de D11 usan endpoints de hoy (`P01/` §13.5) que no se maquetan. El mapa pantalla → endpoints está en `P01/` §13.2.

### 2.2 Componentes compartidos

En `F/components/app/`, con prueba Vitest cada uno en `FT/unit/components/`. No importan servicios ni `useApi` (D15). Los textos van en español y las etiquetas encima del campo (AF-131).

**`AppDataTable`** — listado con filtros por columna y orden (AF-129, AF-99, P-TR-02).

| Prop / evento | Tipo | Regla |
| --- | --- | --- |
| `rows` | `T[]` | Filas de la página actual |
| `columns` | `AppColumn<T>[]` | `field`, `header`, `sortable`, `filter` (`text` \| `select` \| `dateRange` \| `boolean`, con `options` en `select`), `format` (`number` \| `kg` \| `currency` \| `date` \| `datetime`, con `F/shared/utils/format.ts` y `F/utils/colombia-date.ts`), `width` |
| `totalRecords`, `loading` | `number`, `boolean` | — |
| `mode` | `"server"` \| `"client"` | `server`: emite el estado y no ordena ni filtra; `client`: ordena y filtra en el navegador (`P01/` D10) |
| `v-model:state` | `{ pageIndex, pageSize, sortField?, sortOrder?, filters }` | En `server` es lo que se manda a la fuente, con los nombres de C-F01-00. Filtros de texto con espera de 300 ms |
| `createLabel` | `string` \| `undefined` | Muestra «+ {createLabel}» en la barra y emite `create` |
| `exportable` | `boolean` | Muestra «Exportar» y emite `export` (la página arma el Excel con `useExcelExport`) |
| `globalFilters` | slot | Tarjeta tipo barra encima de la tabla, solo si la página la pasa (RV-06) |
| `actions` | slot por fila | Botones con borde o relleno y `aria-label` (guardia de hoy); la fila no tiene clic |
| `emptyMessage` | `string` | Por defecto «No se encontraron registros.» |

Paginador con `TABLE_ROWS_OPTIONS` de `F/shared/utils/table.ts`. Usan después: F03 (historial, P-BAS-08 a P-BAS-10), F04 (P-BOD-01, P-BOD-05, P-BOD-06, P-BOD-09), F05 (P-CE-01, P-CE-09, P-CE-10), F06 (P-CE-11), F07 (P-FAC-11 a P-FAC-14), F08 (P-FAC-01 a P-FAC-10) y F09 (P-TR-07).

**`AppSearchSelect`** — selector de lista grande con búsqueda y alta rápida (AF-134, AF-54, AF-92, P-TR-11; D12).

| Prop / evento | Tipo | Regla |
| --- | --- | --- |
| `v-model` | `string \| null` (Id) | — |
| `fetchPage` | `(search: string, pageIndex: number) => Promise<{ items: T[]; totalCount: number }>` | La página le pasa la fuente (simulada o http); 20 por página |
| `fetchById` | `(id: string) => Promise<T \| null>` | Para mostrar el valor inicial |
| `optionLabel`, `optionDescription` | `(item: T) => string` | Línea principal y secundaria («Importador X SAS» · «NIT 900000010») |
| `placeholder` | `string` | «Buscar por nombre o NIT…» |
| `quickCreate` | `boolean` | Muestra «+» al lado y emite `create`; la página abre su modal de alta y, al crear, fija el valor |
| `invalid`, `disabled` | `boolean` | Para `@primevue/forms` |

Usan después: F03 (transportadora, conductor, tercero de solo báscula, P-BAS-02 a P-BAS-05), F04 (placa y tercero del montacargas), F05 (terceros y productos de P-CE-03 y P-CE-04), F06 (depósitos, vehículo, conductor y ciudad de P-CE-11) y F07 (cliente e importador de P-FAC-11 y P-FAC-12).

**`AppDetailDrawer`** — detalle de un registro sobre el listado (AF-130, P-TR-03, como MK-07).

| Prop / evento | Tipo | Regla |
| --- | --- | --- |
| `v-model:visible` | `boolean` | Se cierra con ✕ o Escape |
| `title`, `subtitle` | `string` | Encabezado («Conductor 1 · CC 1000001») |
| `width` | `"md"` \| `"lg"` | `lg` para Terceros y Servicios (secciones de D11) |
| `expandable` | `boolean` | Botón ⤢ para pantalla completa (MK-07) |
| `sections` | slot | Bloques con título; el pie lleva las acciones («✎ Editar») |
| `loading` | `boolean` | — |

La página sincroniza el drawer con `?id={id}` (D9). Usan después: F03 (P-BAS-11), F05 y F06 (detalle de salida), F08 (detalle de factura).

**`AppCrudDialog`** — alta y edición de un catálogo en modal (AF-130, P-TR-03).

| Prop / evento | Tipo | Regla |
| --- | --- | --- |
| `v-model:visible` | `boolean` | No se cierra con clic afuera |
| `title` | `string` | «Nueva ubicación», «Editar motivo» |
| `columns` | `1` \| `2` | 2 si pasa de 6 campos (D9) |
| `schema` | esquema Zod | Valida con `zodResolver` de `@primevue/forms` |
| `initialValues` | objeto | — |
| `submitLabel` | `string` | Por defecto «Guardar» |
| `submitting` | `boolean` | Con `useSubmitGuard` contra el envío doble |
| `@submit` | `(values) => void` | La página llama a la fuente; un `ApiError` muestra `errors[]` en sus campos y `description` arriba del formulario, debajo del encabezado (H-081) |

Usan después: F03 (repesaje, P-BAS-07; P-TR-12), F04 (montacargas), F07 (P-FAC-13) y F09 (P-TR-08).

**`AppChargeForm`** — parte de pago del cobro de báscula, montacargas y guía (AF-132, AF-54, P-TR-09; D13).

| Prop / evento | Tipo | Regla |
| --- | --- | --- |
| `total` | `number` | Lo calcula la pantalla; se muestra con `formatCurrency` |
| `editableTotal` | `boolean` | Como hoy en báscula |
| `zeroValue` | `boolean` | Entrada duplicada o tiquete en $0 por convenio: solo pide el destinatario |
| `driver` | `{ fullName, idType, idNumber } \| null` | Habilita «Conductor del vehículo» |
| `defaultCustomerId` | `string \| null` | Precarga «Tercero registrado» (cliente del depósito) |
| `fetchStakeholders`, `fetchStakeholderById` | funciones de `AppSearchSelect` | Selector del tercero |
| `quickCreateStakeholder` | `(input) => Promise<Stakeholder>` | Alta rápida (C-F01-141) desde el «+» |
| `paymentModes` | `("Immediate" \| "PendingBilling")[]` | Los que ofrece la pantalla |
| `allowMultiClient` | `boolean` | Falso por defecto (D13) |
| `@submit` | `(input: BillingRecipientInput) => void` | Con el esquema `billingRecipientInputSchema` |

Método precargado en «Efectivo»; «Referencia» visible y obligatoria solo con otro método; sin «Nota». Usan después: F03 (P-BAS-05), F04 (P-BOD-04) y F06 (cobro de la guía). El último en migrar borra `BillingCollectForm.vue` y `AdditionalDepositCollect.vue`.

### 2.3 Pantallas

Cada pantalla cumple su wireframe (campos, botones, filtros y su ubicación) con una captura en el informe de su fase (`PM/` §6.2). Los permisos por acción siguen D6.

| Pantalla | Ruta | Fase | Qué lleva |
| --- | --- | --- | --- |
| P-TR-01 Menú por rol | `F/components/layout/AppMenu.vue` | 2 | §1.5. Ítems de un nivel; grupos solo donde el análisis los definió |
| P-TR-10 Login y sidebar | `/auth/login`; `AppMenuProfile.vue`; `AppConfig.vue` | 2 | «Ver contraseña»; roles en otra línea y avatar sin cortar; switch de tema con clic; encabezado del modal sin tapar alertas (D18) |
| P-TR-02 Listado (Conductores) | `/admin/drivers` | 3 | Columnas Documento ↕, Nombre ↕, País ↕, Teléfono, Estado, Acciones (Ver, ✎, activar o desactivar); filtros de fila en documento, nombre, país y estado; «+ Nuevo conductor» y «Exportar». En lugar de «Empresa de transporte» va «País» (D21) |
| P-TR-03 Drawer (Conductor) | `/admin/drivers?id=…` | 3 | Datos del conductor y «Últimos ingresos» (fecha, placa, tiquete; C-F01-19); «✎ Editar» |
| P-TR-03 Modal a dos columnas (Ubicación) | `/admin/locations` | 3 | Código, Nombre, Pasillo, Estante, Nivel, Capacidad; Cancelar y Guardar (D9) |
| P-TR-04 Motivos de ingreso | `/admin/entry-reasons` | 3 | Motivo ↕, Categoría ↕ (Ingreso, Salida, Solo báscula o «—»), Requiere pesaje, Acciones; modal con «Requiere pesaje» y la categoría en botones, obligatoria con pesaje (AF-08) |
| P-TR-05 Prefijos | `/settings/prefixes` | 3 | Campo, Prefijo, Ejemplo al digitar (prefijo + «001234»), Acciones (✎); edición en modal; sin «Nuevo» ni «Exportar» (tres filas fijas) |
| P-TR-06 Tasas de cambio | `/settings/exchange-rates` | 3 | Desde ↕, Hasta, Valor (COP por USD), Registrada por, Acciones (✎); filtro de rango en «Desde»; «+ Nueva tasa» y «Exportar»; modal con desde, hasta y valor |
| Vehículos | `/admin/vehicles` | 3 | Placa ↕, Empresa de transporte, País ↕, Tipo ↕, Estado; modal con `AppSearchSelect` de transportadora y «+» (C-F01-141 con `TRANSPORT_COMPANY`) |
| Ubicaciones | `/admin/locations` | 3 | Lista completa con orden y filtro en el navegador (`P01/` D10) |
| Terceros | `/admin/stakeholders` | 4 | Nombre ↕, Documento ↕, Roles, Estado financiero ↕, Estado; filtros de fila; el filtro de rol de hoy (`?rol=`) se conserva; modal de alta y edición con los datos básicos; drawer con los datos y los marcadores de D11 |
| Productos | `/admin/products` | 4 | Nombre ↕, SKU ↕, Embalaje ↕, Estado; sin unidad (D19); modal con el tipo de embalaje |
| Tipos de embalaje · Tipos de unidad de carga | `/admin/packaging-types`, `/admin/cargo-unit-types` | 4 | Código, Nombre, Estado; lista completa en el navegador; modal |
| Servicios | `/admin/services` | 4 | Código ↕, Nombre ↕, Estado; modal sin precios; drawer con los datos y los marcadores de tarifas (D2, D11) solo para Admin y Facturación |
| Ciudades | `/admin/cities` | 4 | Nombre ↕, País ↕, Departamento ↕, Días de tránsito ↕, Destino de abandono, Estado; modal; «Importar» (C-F01-51) en la barra |
| Cuadrillas | `/admin/crews` | 4 | Nombre ↕, Estado; modal |
| Parámetros | `/admin/parameters` | 4 | Código ↕, Valor, Tipo ↕, Descripción, Estado; edición en modal; sin «Nuevo» |
| Usuarios | `/admin/users` | 5 | Nombre ↕, Usuario ↕, Correo ↕, Roles, Estado; modal de alta (con contraseña) y de edición; drawer con roles (asignar y quitar), «Restablecer contraseña» y activar o desactivar |
| Auditoría | `/admin/audit` | 5 | Fecha ↕, Usuario ↕, Acción ↕, Tabla ↕, Registro, Descripción; filtros de rango de fecha, usuario, acción y tabla; drawer con el valor anterior y el nuevo; sin «Nuevo» |
| P-TR-09 Cobro · P-TR-11 Selector · P-TR-03 (variantes) | `/dev/components` | 1 | La galería de D20 |

---

## 3. Archivos que se tocan

Rutas y líneas de la base `3aa6e3c`. «Se borra» va con `rm`, después de comprobar con grep quién importa el archivo (trampa 7 de `D/contexto/convenciones-tecnicas.md` §10).

### 3.1 Se crean

| Archivo | Fase | Contenido |
| --- | --- | --- |
| `F/shared/contracts/api.ts` | 1 | Esquemas comunes (`P01/` §2.3) |
| `F/shared/mocks/list.ts`, `delay.ts`, `problem.ts`, `session.ts`; `F/plugins/mock-session.client.ts` | 1 | Ayudas de D10 y la sesión simulada |
| `F/components/app/AppDataTable.vue`, `AppSearchSelect.vue`, `AppDetailDrawer.vue`, `AppCrudDialog.vue`, `AppChargeForm.vue`; `F/types/app-table.ts` (`AppColumn`) | 1 | §2.2 |
| `F/pages/dev/components.vue` | 1 | Galería (D20) |
| `FT/unit/guards/list-pattern.spec.ts`, `mock-sources.spec.ts`; `FT/unit/components/*.spec.ts` | 1 | D14, D15 y pruebas de los componentes |
| `F/features/<dominio>/contracts/<recurso>.ts` | 3 a 5 | Los esquemas de `P01/` §2.3 de cada recurso de §3.2 |
| `F/features/<dominio>/services/<recurso>.source.ts`, `F/features/<dominio>/mocks/<recurso>.mock.ts`, `F/features/<dominio>/mocks/data/<recurso>.ts` | 3 a 5 | §3.2 |
| `F/features/<dominio>/composables/<recurso>.queries.ts` | 3 a 5 | Consultas y mutaciones de TanStack Query sobre la fuente activa, con su prefijo de clave (`['drivers']`, `['exchange-rates']`…) e invalidación tras cada mutación. Nombres nuevos para no chocar con los composables de hoy que usan otras pantallas (por ejemplo `F/features/entries/composables/useEntryReasons.ts`) |
| `F/features/settings/` (dominio nuevo) y `F/pages/settings/prefixes.vue`, `F/pages/settings/exchange-rates.vue` | 3 | P-TR-05 y P-TR-06 |
| `FT/unit/<dominio>/mocks.spec.ts` | 3 a 5 | D16 |

### 3.2 Fuentes de datos (I-01 escribe su `*.http.ts`)

| Dominio | Fuente | Endpoints (`P01/` §2.2) |
| --- | --- | --- |
| `entries` | `entry-reason.source.ts` | C-F01-01, C-F01-03 a C-F01-06 |
| `entries` | `driver.source.ts` | C-F01-15 a C-F01-19 |
| `entries` | `vehicle.source.ts` | C-F01-21 a C-F01-24 |
| `settings` | `prefix.source.ts` | C-F01-08, C-F01-09 |
| `settings` | `exchange-rate.source.ts` | C-F01-10 a C-F01-12 |
| `stakeholders` | `stakeholder.source.ts` | C-F01-25 a C-F01-28, C-F01-141 |
| `products` | `product.source.ts` | C-F01-69 a C-F01-72 |
| `administration` | `packaging-type.source.ts`, `cargo-unit-type.source.ts`, `city.source.ts`, `crew.source.ts`, `system-parameter.source.ts` | C-F01-29 a C-F01-36, C-F01-47 a C-F01-58 |
| `services` | `service.source.ts` | C-F01-37 a C-F01-42 |
| `warehouse` | `location.source.ts` | C-F01-43 a C-F01-46 |
| `users` | `user.source.ts` | C-F01-59 a C-F01-67 |
| `audit` | `audit-log.source.ts` | C-F01-68 |

Cada fuente exporta la interfaz `I<Recurso>Source` y la fuente activa (`export const driverSource: IDriverSource = driverMockSource;`). Los datos simulados siguen los ejemplos de los wireframes («Conductor 1 · CC 1000001», «Transportes Ejemplo», tasas del 02/11 al 22/11/2026) y simulan los errores del contrato con `mockProblem` (por ejemplo, el 409 de tasas que se cruzan).

### 3.3 Cambian

| Archivo (base) | Fase | Cambio |
| --- | --- | --- |
| `F/components/layout/AppMenu.vue:9-520` | 2 | Menú de §1.5 (D5) |
| `F/components/layout/AppMenuProfile.vue:14-16`; `F/components/layout/AppConfig.vue:112`; tema de `Dialog`; `F/pages/auth/login.vue:90` | 2 | D18 |
| `F/pages/admin/drivers/index.vue`, `vehicles/index.vue`, `entry-reasons/index.vue`, `locations/index.vue` | 3 | Patrón nuevo (D8, D9) con la fuente simulada; `requiredRoles` de §1.5 |
| `F/pages/admin/stakeholders/index.vue`, `products/index.vue`, `packaging-types/index.vue`, `cargo-unit-types/index.vue`, `services/index.vue`, `cities/index.vue`, `crews/index.vue`, `parameters/index.vue` | 4 | Igual |
| `F/pages/admin/users/index.vue`, `audit/index.vue` | 5 | Igual |
| `F/features/audit/utils/entity-labels.ts` | 2 | Sale el rótulo de unidades de medida (D19) |
| `FT/unit/guards/source-guards.spec.ts` | 1 | Reglas de D17 |

### 3.4 Se borran

| Archivo | Cuándo | Por qué |
| --- | --- | --- |
| `FT/unit/guards/page-header.spec.ts` | Fase 1 | Lo reemplaza `list-pattern.spec.ts` (D14) |
| `F/pages/admin/unit-measures/index.vue`; `F/features/administration/composables/useMutationsUnitMeasures.ts` (si solo la usa esa página); sus pruebas | Fase 2 | M21, D19 |
| `F/pages/admin/{users,stakeholders,products,services}/create.vue`, `edit/[id].vue`, `[id].vue`, y los componentes y pruebas que solo ellas usan | I-01 | D9; las borra la integración (`PM/` §5.4) |
| Carpetas `mocks/` de los dominios de §3.2 | I-01 | `PM/` §6.3 |

---

## 4. Esquema y migraciones

No aplica: F02 no toca el backend.

---

## 5. Pruebas

| Proyecto | Prueba | Escenario |
| --- | --- | --- |
| Vitest | `FT/unit/components/AppDataTable.spec.ts` | Modo servidor emite el estado con los nombres de C-F01-00; modo cliente ordena y filtra; barra con «Nuevo» y «Exportar»; sin clic de fila |
| Vitest | `AppSearchSelect.spec.ts` | Busca con espera, carga más al desplazarse, muestra la línea secundaria, «+» emite `create` y fija el valor creado |
| Vitest | `AppDetailDrawer.spec.ts`, `AppCrudDialog.spec.ts` | Abre y cierra; una o dos columnas; muestra `errors[]` del `ApiError` en sus campos |
| Vitest | `AppChargeForm.spec.ts` | «Efectivo» por defecto; «Referencia» solo con otro método; sin «Nota»; `zeroValue`; emite un `BillingRecipientInput` válido |
| Vitest | `FT/unit/shared/mocks.spec.ts` | `paginate`, `sortBy` y `filterBy` con las reglas de C-F01-00 (tope de 50, `all`, tildes, rangos); `mockProblem` lanza `ApiError` |
| Vitest | `FT/unit/shared/mock-session.spec.ts` | La sesión simulada no actúa fuera de `import.meta.dev` ni sin la bandera |
| Vitest | `FT/unit/<dominio>/mocks.spec.ts` | Cada dato simulado pasa su esquema Zod (D16) |
| Vitest | `FT/unit/guards/list-pattern.spec.ts`, `mock-sources.spec.ts`, `source-guards.spec.ts` | D14, D15, D17 |
| Vitest | `FT/unit/layout/app-menu.spec.ts` (nueva) | Para cada rol, las secciones e ítems de §1.5; sin «Unidades de medida»; ninguna ruta `/settings/…` en la maquetación |
| Vitest | Pruebas de las páginas de hoy que cambian | Se ajustan al patrón nuevo; las que prueban `AppPageHeader` en esas páginas se borran |

Cada fase informa el número de pruebas y de errores de lint antes y después (`PM/` §6).

---

## 6. Casos QA

En la maquetación, el agente de F02 los recorre contra los datos simulados y deja la captura en el informe de su fase. **Se verifican en I-01**, en el navegador y contra el backend real (`P01/` §13). Al cerrar I-01 se copian a `D/qa/` con su ID.

| ID | Regla de origen | Precondición | Pasos | Resultado esperado | Verificación |
| --- | --- | --- | --- | --- | --- |
| QA2-F02-001 | AF-127; P-TR-01 | Usuario CE | Ver el menú | Notificaciones, Dashboards, Comercio Exterior, Reportes (los de CE), Configuración (sin Parámetros), Ayuda; sin «Terceros» en CE | Pantalla |
| QA2-F02-002 | AF-127; P-TR-01 | Usuario Facturación | Ver el menú | Facturación sin «Configuraciones» ni «Clientes»; Reportes con Movimientos, Inventario general, Facturación por CPI y anual; Tarifas y acuerdos; Configuración sin Prefijos ni Parámetros | Pantalla |
| QA2-F02-003 | AF-127, AF-128 | Usuario Admin | Ver el menú | Todas las secciones; Administración con Usuarios y Auditoría; sin «Unidades de medida» | Pantalla |
| QA2-F02-004 | `DEC-005`; D7 | Usuarios Vigilancia, Báscula y Bodega | Ver el menú y abrir `/admin/drivers` | Solo su módulo, Notificaciones, Reportes propios y Ayuda; `/admin/drivers` da «acceso denegado» | Pantalla |
| QA2-F02-005 | AF-129; P-TR-02 | 12 conductores | Abrir Configuración › Conductores | Sin tarjeta de título; barra con «+ Nuevo conductor» y «Exportar»; fila de filtros; orden en Documento, Nombre y País | Pantalla |
| QA2-F02-006 | AF-99 | — | Recorrer las páginas de Configuración | Ningún botón de solo texto; la fila no abre nada al hacer clic; se puede seleccionar y copiar texto | Pantalla |
| QA2-F02-007 | AF-130; P-TR-03 | — | Conductores › «Ver» | Drawer con los datos y «Últimos ingresos»; la URL lleva `?id=`; al recargar, el drawer sigue abierto | Pantalla |
| QA2-F02-008 | AF-130; P-TR-03 | — | Ubicaciones › «+ Nueva ubicación» | Modal a dos columnas con Código, Nombre, Pasillo, Estante, Nivel y Capacidad | Pantalla |
| QA2-F02-009 | AF-08; P-TR-04 | — | Motivos › nuevo con «Requiere pesaje» y sin categoría | El formulario no deja guardar y pide la categoría | Pantalla |
| QA2-F02-010 | AF-08; P-TR-04 | — | Filtrar por categoría «Salida» | Solo los motivos de salida | Pantalla |
| QA2-F02-011 | AF-79; P-TR-05 | Usuario CE | Prefijos › ✎ en N.º de levante, «4820260» | Se guarda; «Ejemplo al digitar» muestra 4820260001234 | Pantalla |
| QA2-F02-012 | AF-85, AF-86; P-TR-06 | — | Tasas › «+ Nueva tasa» con fechas que se cruzan | Se muestra el aviso del 409 | Pantalla |
| QA2-F02-013 | AF-131 | — | Recorrer los modales de F02 | Etiquetas encima del campo, sin etiquetas flotantes | Pantalla |
| QA2-F02-014 | AF-134; P-TR-11 | Galería | Selector de importador: digitar «impor» y desplazar | Busca con espera, muestra «Mostrando 3 de 27 · desplace para cargar más» y carga más | Pantalla |
| QA2-F02-015 | AF-54; P-TR-11 | Galería | «+» junto al selector, crear «Importadora Nueva» | Queda elegida en el selector | Pantalla |
| QA2-F02-016 | AF-132; P-TR-09 | Galería | Cobro: cambiar el método a Transferencia y volver a Efectivo | «Referencia» aparece y desaparece; nunca hay «Nota»; Efectivo viene por defecto | Pantalla |
| QA2-F02-017 | AF-54; P-TR-09 | Galería | Cobro: «Tercero registrado» › «+» | Crea el tercero y lo deja elegido | Pantalla |
| QA2-F02-018 | AF-134 (PR-31); P-TR-10 | Sesión cerrada | Login: botón del ojo | Muestra y oculta la contraseña | Pantalla |
| QA2-F02-019 | AF-134 (H-079); P-TR-10 | Usuario con tres roles | Ver el sidebar | Los roles pasan a otra línea; el avatar no se corta | Pantalla |
| QA2-F02-020 | AF-134 (H-080) | — | Clic sobre el switch de tema | Cambia el tema | Pantalla |
| QA2-F02-021 | AF-134 (H-081) | — | Guardar un modal con un error del backend | La alerta se ve completa bajo el encabezado | Pantalla |
| QA2-F02-022 | D2; `DEC-005` | Usuario Facturación | Terceros › Ver un cliente; Servicios › Ver un servicio | Los marcadores de acuerdos y tarifas (en I-01, las secciones de hoy funcionando) | Pantalla |
| QA2-F02-023 | M21; D19 | — | Productos › nuevo | El modal no tiene unidad de medida | Pantalla |
| QA2-F02-024 | AF-129 | Usuario Admin | Auditoría: rango de fechas, usuario y acción; ordenar por fecha | Filtra y ordena; «Ver» abre el drawer con valor anterior y nuevo | Pantalla |
| QA2-F02-025 | AF-130 | Usuario Admin | Usuarios › nuevo; luego «Ver» › asignar un rol y restablecer contraseña | Modal de alta con contraseña; drawer con roles y acciones | Pantalla |
| QA2-F02-026 | `PM/` §6.2 | Rama de F02 | `yarn test` | Guardias `list-pattern` y `mock-sources` en verde | Código |

---

## 7. Transición de datos

No aplica: F02 no tiene datos propios. Los prefijos y la tasa de arranque los carga el cliente antes del despliegue final (`PM/` §7.3; `P01/` §7).

---

## 8. Fases por parte

Una a la vez, en orden. Cada fase cierra con las compuertas de `PM/` §6.2 (`yarn build` con código 0, `yarn test` en verde, `yarn lint` sin subir la cifra y sin errores en archivos nuevos, «sin llamadas reales», datos simulados que pasan sus esquemas, ninguna ruta nueva en el menú, captura de cada pantalla de la fase), commit y push de `f2/f02-base`.

| Fase | Parte | Contenido | Criterio de salida | Estado |
| --- | --- | --- | --- | --- |
| 1 | 2 | Base: `F/shared/contracts`, `F/shared/mocks` y la sesión simulada; los cinco componentes; la galería; las guardias `list-pattern` y `mock-sources` (sale `page-header.spec.ts`); reglas de `source-guards` | Pruebas de §5 de la fase en verde; galería con P-TR-03, P-TR-09 y P-TR-11; QA2-F02-013 a QA2-F02-017 y QA2-F02-026 contra los simulados | Hecha el 2026-11-23 (FE `d389685`); [informe](informe-f2-f02-base-maquetacion-2026-11-23.md) |
| 2 | 2 | Menú y marco: P-TR-01 (§1.5), P-TR-10 y D18; unidad de medida fuera (D19) | `app-menu.spec.ts` en verde; QA2-F02-001 a QA2-F02-004 y QA2-F02-018 a QA2-F02-021 contra los simulados (con la sesión simulada por rol) | Pendiente |
| 3 | 2 | Configuración I: Motivos (P-TR-04), Prefijos (P-TR-05), Tasas (P-TR-06), Conductores (P-TR-02 y drawer), Vehículos, Ubicaciones (modal) | QA2-F02-005 a QA2-F02-012 contra los simulados | Pendiente |
| 4 | 2 | Configuración II: Terceros, Productos, Tipos de embalaje, Tipos de unidad de carga, Servicios, Ciudades, Cuadrillas, Parámetros | QA2-F02-022 y QA2-F02-023 contra los simulados | Pendiente |
| 5 | 2 | Administración: Usuarios y Auditoría; revisión final de la guardia (`PATTERN` con todas las de F02; `PENDING` con las de D3 y las de F03 a F09) | QA2-F02-024 y QA2-F02-025 contra los simulados; capturas de todas las pantallas | Pendiente |
| I-01 | 3 | En el plan de F01 (`P01/` §13) | `P01/` §13.4 | Pendiente |

---

## 9. Riesgos

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R1 | La sesión simulada (D10) toca el marco (plugins de sesión, conexión, SignalR y notificaciones) | Solo actúa con la bandera y en `yarn dev`; prueba que lo verifica; I-01 prueba el inicio de sesión real (QA2-F02-018 y QA2-F01-058). Es la única forma de ver la aplicación sin el backend, que ocupa F01 a la vez (M10) |
| R2 | Las páginas de hoy que F02 no rediseña siguen con `AppTable` y `AppPageHeader` | Esperado (D4): la guardia las lista en `PENDING` con su feature |
| R3 | Una feature necesita cambiar un componente compartido | Se permite en su maquetación, con pruebas y listado en su plan (`PM/` R4). F02 los deja genéricos |
| R4 | El contrato de F01 cambia durante su backend | El contrato del plan es la única fuente; un cambio exige decisión nueva y aviso a F02 (`PM/` R3) |
| R5 | Las secciones de D11 no se ven en la maquetación | Marcadores con su nombre; I-01 las monta y QA2-F02-022 y QA2-F01-063 las verifican |
| R6 | Mayúsculas en `/Volumes/Dock`: `F/features/Administration` y `administration` conviven (trampa 13) | El código nuevo va en `administration` (minúsculas) |

---

## 10. Fuera de alcance

- El backend, el contrato (lo fija `P01/` §2) y la integración (I-01, `P01/` §13).
- Las pantallas de módulo: Báscula (F03), Bodega (F04), Comercio Exterior (F05), Salidas (F06), Tarifas y acuerdos (F07), Facturas y reportes (F08), Notificaciones y Umbrales (F09 y F04).
- Pasar al patrón los listados de D3 (F03, F04, F05 y F09) y la tabla de pendientes en tema oscuro (H-082, F08).
- Migrar los cobros de hoy a `AppChargeForm` (F03, F04 y F06).
- Estimar esfuerzo.

**Cambio al hub de este plan** (aplicado el 2026-11-22 con el «sí» del usuario):

`D/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md` §2.2, fila nueva al final de la tabla:

> | `F/pages/operations/entries/history.vue`, `F/pages/warehouse/inventory/index.vue`, `F/pages/warehouse/novelties/index.vue`, `F/pages/foreign-trade/abandonment/index.vue`, `F/pages/foreign-trade/packing-lists/index.vue`, `F/pages/notifications/index.vue` | Listados del menú sin pantalla propia en los wireframes | F03, F04, F05, F09 | Cada uno pasa al patrón de AF-129 en la feature de su módulo: Vigilancia › Historial en F03; Inventario y Novedades en F04; Abandono y Listas de empaque en F05; Notificaciones en F09 (respuesta del usuario del 2026-11-21, plan de F02 D3) |

---

## 11. Prompts por parte

- Parte 2 (maquetación): [prompt-f2-f02-base-maquetacion-2026-11-21.md](prompt-f2-f02-base-maquetacion-2026-11-21.md), rama `f2/f02-base` del frontend.
- Parte 3 (I-01): en la carpeta de F01, `../f01-nucleo/prompt-f2-f01-nucleo-integracion-2026-11-21.md`.
- Planificador (con F01): `../f01-nucleo/prompt-f2-f01-nucleo-planificador-2026-11-21.md`.

---

## 12. Mensajes de commit sugeridos

Cada uno termina con la línea de coautoría que indique la sesión.

| Fase | Repo | Mensaje |
| --- | --- | --- |
| 1 | FE | `feat(base): componentes compartidos, datos simulados y guardias del patrón de listado (DEC-080, F02)` |
| 2 | FE | `feat(menu): menú por rol con Configuración, Tarifas y acuerdos, Reportes y Administración; login y sidebar (DEC-080, F02)` |
| 3 | FE | `feat(configuracion): motivos con categoría, prefijos, tasas de cambio, conductores, vehículos y ubicaciones con el patrón nuevo (DEC-080, F02)` |
| 4 | FE | `feat(configuracion): terceros, productos, embalajes, unidades de carga, servicios, ciudades, cuadrillas y parámetros con el patrón nuevo (DEC-080, F02)` |
| 5 | FE | `feat(administracion): usuarios y auditoría con el patrón nuevo (DEC-080, F02)` |
| Cada fase | docs | `docs(f02): fase N de F02 cerrada (sprint 11)` |

