# Informe — F02 «Base transversal», parte 2 · Maquetación (fase 2, sprint 11)

> **Plan:** [plan-cerrado-f2-f02-base-2026-11-21.md](plan-cerrado-f2-f02-base-2026-11-21.md) (§8). **Prompt:** [prompt-f2-f02-base-maquetacion-2026-11-21.md](prompt-f2-f02-base-maquetacion-2026-11-21.md).
> **Rama:** FE `f2/f02-base`, desde `fase-2` `3aa6e3c` (`develop` no había avanzado: ya estaba en `fase-2`).
> **Cómo se verificó:** `yarn dev` con la sesión simulada (`NUXT_PUBLIC_MOCK_SESSION=true`, `?roles=…`) y `NUXT_PUBLIC_API_BASE` apuntando a un puerto cerrado, para que ninguna pantalla vieja llegue al backend de F01. Los casos QA se recorren contra los datos simulados; se verifican de nuevo en I-01 contra el backend real (plan §6).
> **Datos:** ficticios, como los de los wireframes (`DEC-007`).

Cada fase informa las compuertas de `PM/` §6.2 con las cifras antes y después, los casos QA de la fase y una captura de cada pantalla (carpeta [evidencias/](evidencias/)).

---

## Fase 1 · Base y componentes

**Commit FE:** `d389685` — `feat(base): componentes compartidos, datos simulados y guardias del patrón de listado (DEC-080, F02)`.

### Qué quedó

| Pieza | Archivos (`Frontend/wms/`) |
| --- | --- |
| Contratos | `app/shared/contracts/api.ts`; `app/features/stakeholders/contracts/stakeholder.ts`; `app/features/billing/contracts/billing-recipient.ts` (copiados de `P01/` §2.3; tipos con `z.infer`) |
| Ayudas simuladas (D10) | `app/shared/mocks/list.ts` (`paginate`, `sortBy`, `filterBy`, `listQuery`), `delay.ts`, `problem.ts`, `store.ts`, `session.ts` |
| Sesión simulada (D10) | `app/plugins/mock-session.client.ts`; `runtimeConfig.public.mockSession` en `nuxt.config.ts`; el marco no llama al API con ella activa: `auth-init.client.ts`, `useCurrentUser.ts` (`user/me`), `signalr.client.ts`, `useNotifications.ts` y `api-client.ts` (conexión) |
| Componentes (§2.2) | `AppDataTable.vue`, `AppSearchSelect.vue`, `AppDetailDrawer.vue`, `AppCrudDialog.vue`, `AppChargeForm.vue`, más `AppFormField.vue` (etiqueta encima y error, AF-131); tipos en `app/types/app-table.ts` y `app/types/app-search-select.ts`; mensajes de Zod en español en `app/shared/utils/zod-messages.ts` |
| Fuente de terceros | `app/features/stakeholders/services/stakeholder.source.ts`, `mocks/stakeholder.mock.ts`, `mocks/data/stakeholders.ts` (la usa la galería; la página de Terceros llega en la fase 4) |
| Galería (D20) | `app/pages/dev/components.vue` (solo `yarn dev`, Admin; 404 fuera de desarrollo) |
| Guardias | `test/unit/guards/list-pattern.spec.ts` (D14, reemplaza `page-header.spec.ts`, borrado con `rm`), `mock-sources.spec.ts` (D15), reglas de D17 en `source-guards.spec.ts`; listas en `list-pattern-routes.ts` y `menu-routes.ts` |
| Tema | H-081: el encabezado de `Dialog` no se encoge y el contenido se desplaza bajo él (`app/assets/styles.scss`) |

Decisiones de detalle, sin cambiar ninguna Dn:

- `AppFormField` es un sexto componente pequeño (etiqueta + control + error) para no repetir el marcado en cada modal; lo cubren las guardias D15 y D17 como a los otros cinco.
- Los esquemas del contrato no traen mensajes: `AppCrudDialog` valida con `zodResolver(esquema, { error: zodErrorEs })`, que da los mensajes en español sin cambiar los esquemas.
- `AppSearchSelect` muestra «Mostrando 20 de 27 · desplace para cargar más» con 20 por página (D12); el wireframe dibuja 3 filas como ejemplo. Gana D12 (`DEC-002`).
- `AppChargeForm` acepta `defaultPaymentMethod` (por defecto «Efectivo») solo para que la galería muestre la variante «con otro método» de P-TR-09.
- La guardia D14 admite `F02` como feature de `PENDING` mientras dura la maquetación; la fase 5 la deja sin ninguna.
- Configuración local de `yarn dev` con la sesión simulada en `.claude/launch.json` (`wms-dev-maquetacion`, puerto 3020).

### Compuertas

| Compuerta | Antes (`3aa6e3c`) | Después (`d389685`) |
| --- | --- | --- |
| `yarn build` | código 0 | código 0 |
| `yarn test` | 113 archivos · 608 pruebas, en verde | 122 archivos · 668 pruebas, en verde |
| `yarn lint` | 276 errores · 396 avisos | 276 errores · 396 avisos; 0 en archivos nuevos |
| Sin llamadas reales (D15) | — | `mock-sources.spec.ts` en verde |
| Datos simulados con su esquema (D16) | — | `test/unit/stakeholders/mocks.spec.ts` en verde |
| Rutas nuevas en el menú | — | ninguna |

### Casos QA de la fase (contra los simulados)

| ID | Resultado | Evidencia |
| --- | --- | --- |
| QA2-F02-013 | PASA en la galería: etiquetas encima en el modal a dos columnas, en el alta rápida y en el cobro; sin `FloatLabel` ni `IftaLabel` (guardia D17). Los modales de las páginas se recorren en las fases 3 a 5 | [f1-02](evidencias/f1-02-selector-alta-rapida.jpg), [f1-04](evidencias/f1-04-modal-dos-columnas-error-api.jpg) |
| QA2-F02-014 | PASA: «impor» busca tras la espera, muestra 20 con su NIT y «Mostrando 20 de 27 · desplace para cargar más»; al desplazarse carga los 7 restantes («Mostrando 27 de 27») | [f1-01](evidencias/f1-01-selector-busqueda.jpg) |
| QA2-F02-015 | PASA: «+» › «Importadora Nueva» la crea y queda elegida | [f1-02](evidencias/f1-02-selector-alta-rapida.jpg), [f1-03](evidencias/f1-03-selector-elegido-y-cobro.jpg) |
| QA2-F02-016 | PASA: Efectivo por defecto; con Transferencia aparece «Referencia» y al volver a Efectivo desaparece; nunca hay «Nota» | [f1-03](evidencias/f1-03-selector-elegido-y-cobro.jpg) |
| QA2-F02-017 | PASA: «Tercero registrado» › «+» crea «Cliente Nuevo Ejemplo» y lo deja elegido; «Cobrar» emite un `BillingRecipientInput` válido | [f1-03](evidencias/f1-03-selector-elegido-y-cobro.jpg) |
| QA2-F02-021 | PASA en la galería (adelantado de la fase 2): con el error simulado, la alerta se ve completa bajo el encabezado y el error del campo va en «Código» | [f1-04](evidencias/f1-04-modal-dos-columnas-error-api.jpg) |
| QA2-F02-026 | PASA: guardias `list-pattern` y `mock-sources` en verde | `yarn test` |

Drawer de P-TR-03 en la galería: [f1-05](evidencias/f1-05-drawer-detalle.jpg).

---

## Fase 2 · Menú y marco

**Commits FE:** `3e85d79` (wip de la sesión cortada por el límite de uso) y `813443f` — `feat(menu): menú por rol con Configuración, Tarifas y acuerdos, Reportes y Administración; login y sidebar (DEC-080, F02)`, encima del wip, sin reescribir el historial.

### Qué quedó

| Pieza | Archivos (`Frontend/wms/`) |
| --- | --- |
| P-TR-01, menú por rol (D5, D6; §1.5) | `app/components/layout/menu-model.ts` (secciones en el orden de P-TR-01, roles por sección o por ítem, `filterMenuByRoles` y `menuRoutesOf`); `AppMenu.vue` solo filtra el modelo. Salen de su sección «Terceros» (CE), «Configuraciones», «Clientes» y los reportes (Facturación); `MENU_FILTER_PARAMS` queda vacío (`app/utils/menu-route.ts`) |
| P-TR-10 · H-079, sidebar | `AppMenuProfile.vue`: roles en otra línea, una etiqueta por rol con su nombre en español (`ROLE_LABELS` y `roleLabel` en `usePermissions.ts`); el avatar no se encoge. `AppRightMenu.vue` usa los mismos nombres |
| P-TR-10 · H-080, switch de tema | `AppRightMenu.vue`: el clic sobre el switch cambiaba el tema dos veces (el del switch y el de la fila). El switch vive en el menú derecho, no en `AppConfig.vue:112`, que cita el plan |
| P-TR-10 · PR-31, ver contraseña | `app/pages/auth/login.vue`: `toggle-mask` con rótulos accesibles. **Corregido al cerrar:** dentro del `InputGroup`, el campo enfocado sube a `z-index: 1` y tapaba el ojo, que no se veía ni recibía el clic; el ojo queda por encima (estilo con alcance de la página) |
| H-081, encabezado del modal | Hecho en la fase 1 (`app/assets/styles.scss`); se recorre aquí su caso |
| D6, Tarifas y acuerdos | `app/pages/admin/forklift-rates/index.vue` pasa de `["Admin"]` a `["Admin", "Billing"]`: el menú se la muestra a Facturación y el API ya pide `BillingAccess` (`ForkliftRateController`). Sin este cambio, Facturación llegaba a «acceso denegado» desde su menú |
| D19, unidad de medida fuera | Borrados con `rm`: `app/pages/admin/unit-measures/index.vue` y `useMutationsUnitMeasures.ts` (solo los usaba esa página); sale el rótulo de `entity-labels.ts`. Se quedan `useUnitMeasures.ts`, `types/unit-measure.ts` y sus métodos de servicio (los usan pantallas de F03, F04, F05 y F07). El campo de unidad de `ProductForm.vue` lo retira la fase 4 (Productos) y sus páginas viejas, I-01 |
| Pruebas | `test/unit/layout/app-menu.spec.ts` (nueva: cada rol, sin «Unidades de medida», ninguna ruta `/settings/…`); ajustadas `AppMenu.spec.ts`, `AppMenuItem.spec.ts`, `entity-labels.spec.ts`, `menu-route.spec.ts` y las listas de las guardias |

Notas, sin cambiar ninguna Dn:

- Las páginas de Configuración (salvo Terceros) siguen con `["Admin"]` hasta las fases 3 y 4, que les ponen los roles de §1.5 (plan §3.3). Mientras tanto, CE y Facturación las ven en el menú y reciben «acceso denegado» al abrirlas: es lo esperado en la rama de la maquetación (`PM/` §5.4).
- Vigilancia no tiene reportes propios en §1.5, así que su menú no muestra «Reportes».

### Compuertas

| Compuerta | Antes (fase 1, `d389685`) | Después (`813443f`) |
| --- | --- | --- |
| `yarn build` | código 0 | código 0 |
| `yarn test` | 122 archivos · 668 pruebas, en verde | 123 archivos · 675 pruebas, en verde |
| `yarn lint` | 276 errores · 396 avisos | 276 errores · 396 avisos; 0 errores en archivos nuevos (`menu-model.ts`, `app-menu.spec.ts`) |
| Sin llamadas reales (D15) | `mock-sources.spec.ts` en verde | en verde |
| Rutas nuevas en el menú | ninguna | ninguna: solo rutas de hoy; ninguna `/settings/…` (`app-menu.spec.ts`) |

### Casos QA de la fase (contra los simulados, sesión simulada por rol)

| ID | Resultado | Evidencia |
| --- | --- | --- |
| QA2-F02-001 | PASA (`?roles=ForeignTrade`): Notificaciones, Dashboards, Comercio Exterior (sin «Terceros»), Reportes (los seis de CE, Movimientos, Inventario general y Póliza), Configuración sin Parámetros, Ayuda | [f2-01](evidencias/f2-01-menu-comercio-exterior.jpg) |
| QA2-F02-002 | PASA (`?roles=Billing`): Facturación sin «Configuraciones» ni «Clientes»; Reportes con Movimientos, Inventario general, Facturación por CPI y anual; Tarifas y acuerdos (las dos páginas abren); Configuración sin Prefijos ni Parámetros | [f2-02](evidencias/f2-02-menu-facturacion.jpg) |
| QA2-F02-003 | PASA (`?roles=Admin`): las doce secciones en el orden de P-TR-01; Administración con Usuarios y Auditoría; sin «Unidades de medida» | [f2-03](evidencias/f2-03-menu-admin.jpg) |
| QA2-F02-004 | PASA: Vigilancia ve Notificaciones, Vigilancia y Ayuda; Báscula, además, Reportes › Reporte de báscula; Bodega, Reportes › Inventario general. `/admin/drivers` lleva a «Acceso denegado» con los tres | [f2-04a](evidencias/f2-04a-menu-vigilancia.jpg), [f2-04b](evidencias/f2-04b-menu-bascula.jpg), [f2-04c](evidencias/f2-04c-menu-bodega.jpg), [f2-04d](evidencias/f2-04d-conductores-acceso-denegado.jpg) |
| QA2-F02-018 | PASA tras la corrección del ojo (antes no se veía): con la sesión cerrada, el ojo muestra la contraseña (`type="text"`) y la vuelve a ocultar | [f2-06a](evidencias/f2-06a-login-oculta.jpg), [f2-06b](evidencias/f2-06b-login-visible.jpg) |
| QA2-F02-019 | PASA (`?roles=Admin,ForeignTrade,Billing`): «Administrador», «Comercio Exterior» y «Facturación» en otra línea, bajo el nombre; avatar de 35 × 35 px sin cortar | [f2-05](evidencias/f2-05-sidebar-tres-roles.jpg) |
| QA2-F02-020 | PASA: un clic sobre el switch pasa a oscuro y otro vuelve a claro | [f2-07](evidencias/f2-07-switch-tema-oscuro.jpg) |
| QA2-F02-021 | PASA (galería, error simulado del API): la alerta empieza bajo el encabezado del modal y se ve completa; el error del campo va en «Código» | [f2-08](evidencias/f2-08-modal-error-api.jpg) |

Las capturas se tomaron con Playwright contra `yarn dev` (`wms-dev-maquetacion`, puerto 3020); los menús y los resultados se comprobaron también por el DOM.

---

## Fase 3 · Configuración I

**Commit FE:** `4e60427` — `feat(configuracion): motivos con categoría, prefijos, tasas de cambio, conductores, vehículos y ubicaciones con el patrón nuevo (DEC-080, F02)`.

### Qué quedó

| Pieza | Archivos (`Frontend/wms/`) |
| --- | --- |
| Contratos (copiados del plan de F01 §2.3, tipos con `z.infer`) | `app/features/entries/contracts/{entry-reason,driver,vehicle}.ts`, `app/features/settings/contracts/{prefix,exchange-rate}.ts`, `app/features/warehouse/contracts/location.ts` |
| Fuentes (`I<Recurso>Source` y la fuente activa, simulada) | `entry-reason.source.ts`, `driver.source.ts`, `vehicle.source.ts` (`entries`); `prefix.source.ts`, `exchange-rate.source.ts` (`settings`, dominio nuevo); `location.source.ts` (`warehouse`) |
| Datos y fuentes simulados | `mocks/data/*.ts` y `mocks/*.mock.ts` de cada dominio: 7 motivos con la categoría de M22, 12 conductores con sus últimos ingresos, 8 vehículos con transportadora de los terceros simulados, los 3 prefijos, 8 tasas semanales (del 28/09 al 22/11/2026) y 9 ubicaciones. Simulan los errores del contrato: categoría obligatoria con pesaje (400), motivo, conductor, placa o código repetidos (409), motivo o ubicación en uso (409), tasa de más de 7 días (400) y fechas que se cruzan (409) |
| Consultas (`*.queries.ts`) | Una por recurso, con prefijo `['entry-reasons']`, `['drivers']`, `['vehicles']`, `['prefixes']`, `['exchange-rates']`, `['locations']` e invalidación tras cada mutación. El segundo nivel (`list`, `detail`) evita chocar con `useDrivers`, `useVehicles` y `useEntryReasons` de hoy, que usan otras pantallas |
| P-TR-04 Motivos (`/admin/entry-reasons`) | Motivo ↕, Categoría ↕ (con «Sin categoría» en el filtro), Requiere pesaje ↕; ✎ y 🗑; «+ Nuevo motivo» y «Exportar». Modal con «Requiere pesaje» y la categoría en botones, que solo aparece con pesaje |
| P-TR-05 Prefijos (`/settings/prefixes`, nueva) | Campo, Prefijo, Ejemplo al digitar (prefijo + «001234»), ✎; sin «Nuevo» ni «Exportar». Modal con el ejemplo en vivo; vacío quita el prefijo. Admin y CE |
| P-TR-06 Tasas (`/settings/exchange-rates`, nueva) | Desde ↕ (filtro de rango), Hasta, Valor (COP por USD) ↕, Registrada por, ✎; «+ Nueva tasa» y «Exportar». Modal con desde, hasta y valor |
| P-TR-02 Conductores (`/admin/drivers`) y drawer | Documento ↕, Nombre ↕, País ↕, Teléfono, Estado; Ver, ✎ y activar o desactivar; drawer con los datos y «Últimos ingresos», sincronizado con `?id=`; «✎ Editar» desde el drawer |
| Vehículos (`/admin/vehicles`) | Placa ↕, Empresa de transporte, País ↕, Tipo ↕, Estado; ✎ y activar o desactivar. Modal con `AppSearchSelect` de transportadora y su «+» (C-F01-141 con `TRANSPORT_COMPANY`) |
| Ubicaciones (`/admin/locations`) | Lista completa con orden y filtros en el navegador; modal a dos columnas con Código, Nombre, Pasillo, Estante, Nivel y Capacidad (al editar, el código no cambia y se suma «Disponible») |
| Roles (D6) | Las cuatro páginas de `/admin` pasan de `["Admin"]` a `["Admin", "ForeignTrade", "Billing"]`; Prefijos, `["Admin", "ForeignTrade"]`; Tasas, `["Admin", "ForeignTrade", "Billing"]`. Ninguna acción se oculta: las políticas de sus endpoints admiten los tres roles |
| `AppDataTable` | Sin fila de filtros cuando ninguna columna filtra (se veía una fila vacía en Prefijos) |
| Guardias | `list-pattern-routes.ts`: las cuatro rutas pasan de `PENDING` a `PATTERN`. `mock-sources.spec.ts`: las seis páginas entran en `MAQUETACION_PAGES` |
| Pruebas | `test/unit/entries/mocks.spec.ts`, `test/unit/settings/mocks.spec.ts` y `test/unit/warehouse/mocks.spec.ts` (D16): cada dato pasa su esquema y la fuente simulada responde con las reglas y los errores del contrato |

Notas, sin cambiar ninguna Dn:

- **Conductores sin filtro de País:** el contrato (C-F01-15, `driverListQuerySchema`) no tiene ese filtro; por respuesta del usuario del 2026-11-23, «País» se ordena pero no se filtra.
- **Tipos de vehículo:** en la maquetación salen de una lista fija con los valores del enum `VehicleType` de hoy (`app/features/entries/utils/vehicle-types.ts`), los mismos del respaldo de la pantalla anterior; la pantalla vieja los leía del catálogo de báscula.
- **Fechas de la tasa:** el selector no admite escritura a mano (`manual-input` en falso, como el filtro de rango): escribir la fecha dejaba un texto que el formulario no reconocía.
- La pantalla vieja de Ubicaciones tenía tarjetas de totales y «Refrescar»; el patrón de AF-129 no las lleva.

### Compuertas

| Compuerta | Antes (fase 2, `813443f`) | Después (`4e60427`) |
| --- | --- | --- |
| `yarn build` | código 0 | código 0 |
| `yarn test` | 123 archivos · 675 pruebas, en verde | 126 archivos · 694 pruebas, en verde |
| `yarn lint` | 276 errores · 396 avisos | 270 errores · 394 avisos (bajan con las páginas reescritas); 0 errores en archivos nuevos o cambiados |
| Sin llamadas reales (D15) | `mock-sources.spec.ts` en verde | en verde, con las seis páginas en `MAQUETACION_PAGES`; en el navegador, ninguna petición a `api/v1` y ninguna línea de error en la consola |
| Datos simulados con sus esquemas (D16) | terceros | terceros, motivos, conductores, ingresos recientes, vehículos, prefijos, tasas y ubicaciones |
| Rutas nuevas en el menú | ninguna | ninguna: `/settings/prefixes` y `/settings/exchange-rates` se abren por URL (`app-menu.spec.ts` en verde) |
| Patrón de listado (D14) | 0 rutas en `PATTERN` | 4 rutas en `PATTERN`, en verde |

### Casos QA de la fase (contra los simulados)

| ID | Resultado | Evidencia |
| --- | --- | --- |
| QA2-F02-005 | PASA (`?roles=Admin`): 12 conductores; sin tarjeta de título; barra con «+ Nuevo conductor» y «Exportar»; fila de filtros (documento, nombre, estado); orden en Documento, Nombre y País (probado por País) | [f3-01](evidencias/f3-01-conductores-listado.jpg), [f3-02](evidencias/f3-02-conductores-filtro-orden.jpg) |
| QA2-F02-006 | PASA: en Conductores, Vehículos, Motivos, Ubicaciones, Prefijos y Tasas los botones tienen borde o relleno (la guardia D17 cubre las rutas de `PATTERN`); el clic en una fila no abre nada; las celdas admiten seleccionar texto (`user-select: text`) | [f3-02](evidencias/f3-02-conductores-filtro-orden.jpg), [f3-07](evidencias/f3-07-motivos-listado.jpg), [f3-14](evidencias/f3-14-vehiculos-listado.jpg) |
| QA2-F02-007 | PASA: «Ver» abre el drawer con los datos y «Últimos ingresos»; la URL lleva `?id=`; al recargar, el drawer sigue abierto; «Editar» abre el modal y el cambio se ve en el drawer | [f3-03](evidencias/f3-03-conductor-drawer-tras-recargar.jpg), [f3-04](evidencias/f3-04-conductor-modal-editar.jpg) |
| QA2-F02-008 | PASA: «+ Nueva ubicación» abre el modal a dos columnas con Código, Nombre, Pasillo, Estante, Nivel y Capacidad; un código repetido muestra el 409 en «Código» | [f3-05](evidencias/f3-05-ubicacion-modal-dos-columnas.jpg), [f3-06](evidencias/f3-06-ubicacion-codigo-repetido.jpg) |
| QA2-F02-009 | PASA: con «Requiere pesaje» y sin categoría, el formulario no guarda y pide «Elija la categoría del motivo: Ingreso, Salida o Solo báscula.»; con «Ingreso» se crea | [f3-09](evidencias/f3-09-motivo-pide-categoria.jpg) |
| QA2-F02-010 | PASA: el filtro de categoría «Salida» deja solo los dos motivos de salida | [f3-08](evidencias/f3-08-motivos-filtro-salida.jpg) |
| QA2-F02-011 | PASA (`?roles=ForeignTrade`): ✎ en N.º de levante, «4820260»; el modal muestra 4820260001234 al digitar; se guarda y la tabla lo muestra | [f3-10](evidencias/f3-10-prefijo-ejemplo-al-digitar.jpg), [f3-11](evidencias/f3-11-prefijos-guardado.jpg) |
| QA2-F02-012 | PASA (`?roles=Billing`): «+ Nueva tasa» del 20/11 al 26/11/2026 muestra «Las fechas se cruzan con la tasa del 16/11/2026 al 22/11/2026.» bajo el encabezado del modal | [f3-13](evidencias/f3-13-tasa-fechas-se-cruzan-409.jpg) |

Otras capturas de la fase: Tasas con el filtro de rango de noviembre ([f3-12](evidencias/f3-12-tasas-filtro-rango.jpg)); Vehículos, alta rápida de la transportadora con el «+», queda elegida y el vehículo se crea ([f3-15](evidencias/f3-15-vehiculo-alta-rapida-transportadora.jpg), [f3-16](evidencias/f3-16-vehiculo-transportadora-elegida.jpg), [f3-17](evidencias/f3-17-vehiculo-creado.jpg)). QA2-F02-013 (etiquetas encima) se ve en todos los modales de la fase.

Las capturas se tomaron en el navegador del entorno contra `yarn dev` (`wms-dev-maquetacion`, puerto 3020), con la sesión simulada por rol.

### Pendiente para I-01 (de esta fase)

- Escribir `entry-reason.http.ts`, `driver.http.ts`, `vehicle.http.ts`, `prefix.http.ts`, `exchange-rate.http.ts` y `location.http.ts`, cambiar la línea de cada `*.source.ts`, borrar las carpetas `mocks/` y vaciar `MAQUETACION_PAGES`.
- Enlazar Prefijos y Tasas de cambio en Configuración (D1, §1.5).
- Decidir si los tipos de vehículo vuelven a leerse del catálogo de báscula.
- Al mutar ubicaciones, invalidar también `['warehouse-locations']` de las pantallas de Bodega, si comparten datos con el API real.
- Borrar lo que solo usaban las páginas viejas de esta fase (por ejemplo `useMutations.ts` de `entries` y `useWarehouseLocationMutations.ts`, tras comprobar con grep quién los importa).

---

## Fase 4 · Configuración II

**Commit FE:** `9e738bc` — `feat(configuracion): terceros, productos, embalajes, unidades de carga, servicios, ciudades, cuadrillas y parámetros con el patrón nuevo (DEC-080, F02)`.

### Respuestas del usuario (2026-11-23)

| Duda | Respuesta | Efecto |
| --- | --- | --- |
| El contrato de F01 (§2.3, `cityCreateSchema`) pedía `countryCode` de 2 letras; el backend (`CreateCityValidator`) y los datos usan 3 («COL», «ECU») | «Contrato a 3 letras» | `P01/` §2.3 y C-F01-48 corregidos a `length(3)`, con la nota de la respuesta; el backend de F01 ya valida 3 letras, así que no cambia |
| Terceros: ¿se conservan la búsqueda global (WMS-7) y el filtro «Salidas» (BR-05-004)? | «Nombre, Tipo de identificación, Número de identificación, Roles, Estado Financiero, Salidas, Estado y los filtros solo por columnas; sin búsqueda global» | Siete columnas y solo filtros de fila; sale la búsqueda global; «Salidas» queda como columna con su filtro. Fila de Terceros de §2.3 del plan actualizada |

### Qué quedó

| Pieza | Archivos (`Frontend/wms/`) |
| --- | --- |
| Contratos (copiados de `P01/` §2.3, tipos con `z.infer`) | `app/features/administration/contracts/{packaging-type,cargo-unit-type,city,crew,system-parameter}.ts`, `app/features/services/contracts/service.ts`, `app/features/products/contracts/product.ts` |
| Fuentes (`I<Recurso>Source` y la fuente activa, simulada) | `packaging-type.source.ts`, `cargo-unit-type.source.ts`, `city.source.ts`, `crew.source.ts`, `system-parameter.source.ts` (`administration`); `service.source.ts`; `product.source.ts`. `stakeholder.source.ts` suma `businessRoles()`: simula el endpoint de hoy `GET administration/business-role`, sin cambios (`PM/` §5.2) |
| Datos y fuentes simulados | 9 tipos de embalaje, 7 de unidad de carga, 16 ciudades de Colombia, Ecuador y Perú, 7 cuadrillas, 12 parámetros, 12 servicios sin precios y 15 productos sin unidad. Simulan los errores del contrato: código, nombre, SKU o documento repetidos (409), en uso al eliminar (409), formato del código del servicio (400), activar dos veces (400), valor que no corresponde al tipo del parámetro (400) y la importación del CSV de ciudades con sus filas con error |
| Consultas (`*.queries.ts`) | Prefijos `['packaging-types']`, `['cargo-unit-types']`, `['cities']`, `['crews']`, `['system-parameters']`, `['services']`, `['products']` y `['stakeholders']`, con un segundo nivel (`list`, `detail`) que no choca con los composables de hoy; invalidación tras cada mutación |
| Terceros (`/admin/stakeholders`) | Nombre ↕, Tipo de identificación, Número de identificación ↕, Roles, Estado financiero ↕, Salidas, Estado; filtros de fila; `?rol=` fija el filtro de Roles y el filtro escribe `?rol=` (la miga sigue con el rol). Ver, ✎ y activar o desactivar. Modal a dos columnas (siete campos; roles solo al crear). Drawer con `?id=`: datos, saldo vencido, marca «sin salidas» con su motivo y los marcadores de D11 (roles, cuentas, contactos, «sin salidas»; acuerdos solo para Admin y Facturación, D2) |
| Productos (`/admin/products`) | Nombre ↕, SKU ↕, Embalaje ↕ (filtro por tipo), Estado; ✎ y activar o desactivar. Modal sin unidad de medida (D19) con el tipo de embalaje y su «+» de alta rápida, como hoy (C-F01-30) |
| Tipos de embalaje · Tipos de unidad de carga | Código, Nombre, Estado; lista completa con orden y filtros en el navegador; modal; ✎ y 🗑. En embalajes el estado no se edita (C-F01-31 no lo trae); en unidades de carga, al editar, el código no cambia y se suma «Activo» (C-F01-35) |
| Servicios (`/admin/services`) | Código ↕, Nombre ↕, Estado; Ver, ✎ y activar o desactivar. Modal sin precios (código solo al crear). Drawer con `?id=` y los marcadores de precios, reglas, mínimos e impuestos solo para Admin y Facturación (D2, D6, D11) |
| Ciudades (`/admin/cities`) | Nombre ↕, País ↕, Departamento ↕, Días de tránsito ↕, Destino de abandono, Estado; filtros de fila. «Importar» en la barra: `CityImportDialog.vue` ya no llama al API, recibe `importCities` de la página (fuente activa, C-F01-51). Modal con el país de 3 letras |
| Cuadrillas (`/admin/crews`) | Nombre ↕, Estado; modal; ✎ y 🗑 |
| Parámetros (`/admin/parameters`) | Código ↕, Valor, Tipo ↕, Descripción, Estado; solo edición en modal (sin «Nuevo»), con el valor según su tipo (número con `es-CO`, verdadero o falso, texto); solo Admin |
| Roles (D6) | Las siete páginas de Configuración pasan de `["Admin"]` a `["Admin", "ForeignTrade", "Billing"]`; Parámetros sigue en `["Admin"]`; Terceros ya los tenía. Ninguna acción se oculta salvo las secciones de tarifas y acuerdos (D2): las políticas de sus endpoints admiten los tres roles |
| Componentes compartidos | `AppCrudDialog`: limpia el error del API en cada intento, también si la validación local lo detiene (quedaba «Ya existe la ciudad PASTO» bajo un nombre ya corregido); prueba nueva en `AppCrudDialog.spec.ts`. `AppDataTable`: las acciones de la fila no se parten en varias líneas |
| Guardias | `list-pattern-routes.ts`: ocho rutas pasan de `PENDING` a `PATTERN` (quedan en `PENDING` de F02 solo Usuarios y Auditoría). `mock-sources.spec.ts`: las ocho páginas y `CityImportDialog.vue` entran en `MAQUETACION_PAGES` |
| Pruebas | `test/unit/administration/mocks.spec.ts`, `test/unit/services/mocks.spec.ts`, `test/unit/products/mocks.spec.ts` (nuevas) y `test/unit/stakeholders/mocks.spec.ts` (ampliada): cada dato pasa su esquema y la fuente simulada responde con las reglas y los errores del contrato (D16) |

Notas, sin cambiar ninguna Dn:

- **Campos del contrato fuera del modal:** `bankAccounts` y `contacts` del tercero (el modal no los envía, C-F01-27) y `packaging` del producto (texto libre que el modal de hoy no tiene) se sacan del esquema del formulario y la página los envía en `null`; con el esquema completo, el formulario no se enviaba porque esos campos llegaban sin valor.
- **Productos sin «Origen»:** la columna «Origen» (creado desde báscula) de la pantalla vieja no está en §2.3; queda en el Excel de «Exportar».
- **Velo de carga:** al abrir una página paginada, el velo de la tabla sigue unos cientos de milisegundos después de pintar las filas; pasa igual en Conductores (fase 3). Es cosmético y no se tocó.

### Compuertas

| Compuerta | Antes (fase 3, `4e60427`) | Después (`9e738bc`) |
| --- | --- | --- |
| `yarn build` | código 0 | código 0 |
| `yarn test` | 126 archivos · 694 pruebas, en verde | 129 archivos · 711 pruebas, en verde |
| `yarn lint` | 270 errores · 394 avisos | 262 errores · 390 avisos (bajan con las páginas reescritas); 0 errores en archivos nuevos o cambiados |
| Tipos (`nuxi typecheck`) | — | sin errores en los archivos de la fase (los 71 que reporta son de archivos anteriores) |
| Sin llamadas reales (D15) | `mock-sources.spec.ts` en verde | en verde, con las ocho páginas y `CityImportDialog.vue` en `MAQUETACION_PAGES`; en el navegador, ninguna petición a `api/v1` |
| Datos simulados con sus esquemas (D16) | terceros, motivos, conductores, vehículos, prefijos, tasas y ubicaciones | más roles de negocio, tipos de embalaje y de unidad de carga, ciudades, cuadrillas, parámetros, servicios y productos |
| Rutas nuevas en el menú | ninguna | ninguna |
| Patrón de listado (D14) | 4 rutas en `PATTERN` | 12 rutas en `PATTERN`, en verde |

### Casos QA de la fase (contra los simulados)

| ID | Resultado | Evidencia |
| --- | --- | --- |
| QA2-F02-022 | PASA (`?roles=Billing`): Terceros › Ver un cliente muestra los datos y los marcadores, con «Acuerdos del cliente · se conecta en I-01»; Servicios › Ver muestra «Precios», «Reglas de tarifa», «Valores mínimos» e «Impuestos» como marcadores. Con `?roles=ForeignTrade`, ni acuerdos ni tarifas (D2, D6) | [f4-03](evidencias/f4-03-tercero-drawer-facturacion.jpg), [f4-13](evidencias/f4-13-servicio-drawer-tarifas-facturacion.jpg), [f4-14](evidencias/f4-14-servicio-drawer-sin-tarifas-ce.jpg) |
| QA2-F02-023 | PASA (`?roles=ForeignTrade`): Productos › «+ Nuevo producto» no tiene unidad de medida; el «+» crea el tipo de embalaje «Bolsas», queda elegido y el producto se crea | [f4-08](evidencias/f4-08-producto-modal-sin-unidad.jpg), [f4-09](evidencias/f4-09-producto-embalaje-alta-rapida.jpg) |
| QA2-F02-006 (repaso) | PASA en las ocho páginas: botones con borde o relleno (guardia D17 sobre las rutas de `PATTERN`), sin clic de fila | capturas de los listados |
| QA2-F02-013 (repaso) | PASA: etiquetas encima en todos los modales de la fase | [f4-04](evidencias/f4-04-tercero-modal-validacion.jpg), [f4-17](evidencias/f4-17-ciudad-pais-tres-letras.jpg), [f4-23](evidencias/f4-23-parametro-modal-numero.jpg) |

Capturas de cada pantalla:

| Pantalla | Capturas |
| --- | --- |
| Terceros | Listado con Facturación ([f4-01](evidencias/f4-01-terceros-listado-facturacion.jpg)); `?rol=CUSTOMER` con el filtro «Cliente» y la miga «Clientes» ([f4-02](evidencias/f4-02-terceros-filtro-rol-clientes.jpg)); validación del modal ([f4-04](evidencias/f4-04-tercero-modal-validacion.jpg)); NIT repetido, 409 bajo el encabezado ([f4-05](evidencias/f4-05-tercero-documento-repetido-409.jpg)); creado y filtrado por nombre ([f4-06](evidencias/f4-06-tercero-creado-filtro-nombre.jpg)) |
| Productos | [f4-07](evidencias/f4-07-productos-listado.jpg), [f4-08](evidencias/f4-08-producto-modal-sin-unidad.jpg), [f4-09](evidencias/f4-09-producto-embalaje-alta-rapida.jpg) |
| Tipos de embalaje · Tipos de unidad de carga | [f4-10](evidencias/f4-10-tipos-embalaje-listado.jpg) (eliminar «Sacos», en uso, da el aviso del 409); [f4-11](evidencias/f4-11-unidad-carga-modal-editar.jpg) (código fijo y «Activo») |
| Servicios | [f4-12](evidencias/f4-12-servicios-listado.jpg), [f4-13](evidencias/f4-13-servicio-drawer-tarifas-facturacion.jpg), [f4-14](evidencias/f4-14-servicio-drawer-sin-tarifas-ce.jpg) |
| Ciudades | [f4-15](evidencias/f4-15-ciudades-listado.jpg); nombre repetido en el campo ([f4-16](evidencias/f4-16-ciudad-repetida-409.jpg)); país de 2 letras rechazado y sin el error viejo del API ([f4-17](evidencias/f4-17-ciudad-pais-tres-letras.jpg)); creada y filtrada sin tilde ([f4-18](evidencias/f4-18-ciudad-creada-filtro-sin-tilde.jpg)); «Importar» con la simulación del CSV: 3 filas, 1 se crea, 1 se actualiza, 1 con error ([f4-19](evidencias/f4-19-ciudades-importar-simulacion.jpg)) |
| Cuadrillas | [f4-20](evidencias/f4-20-cuadrillas-listado.jpg), [f4-21](evidencias/f4-21-cuadrilla-repetida-409.jpg) |
| Parámetros | [f4-22](evidencias/f4-22-parametros-listado-editado.jpg) (valor guardado), [f4-23](evidencias/f4-23-parametro-modal-numero.jpg); con `?roles=ForeignTrade` lleva a «Acceso denegado» |

Las capturas se tomaron en el navegador del entorno contra `yarn dev` (`wms-dev-maquetacion`, puerto 3020), con la sesión simulada por rol.

### Pendiente para I-01 (de esta fase)

- Escribir `packaging-type.http.ts`, `cargo-unit-type.http.ts`, `city.http.ts`, `crew.http.ts`, `system-parameter.http.ts`, `service.http.ts`, `product.http.ts` y completar `stakeholder.http.ts` con `businessRoles()` (`GET administration/business-role`); cambiar la línea de cada `*.source.ts`, borrar las carpetas `mocks/` y vaciar `MAQUETACION_PAGES` (incluido `CityImportDialog.vue`).
- Montar en los drawers las secciones de D11 con los componentes de hoy (`P01/` §13.5): en Terceros, roles, cuentas, contactos, marca «sin salidas» y acuerdos; en Servicios, precios, reglas, mínimos e impuestos.
- Borrar las páginas `create.vue`, `edit/[id].vue` y `[id].vue` de Terceros, Productos y Servicios, y lo que solo ellas usan (por ejemplo `ProductForm.vue`, con la unidad de medida, y `StakeholderForm.vue`), tras comprobar con grep quién los importa; también `useImportCities` y los composables viejos de los catálogos si ya nadie los usa, y `stakeholderPageTexts` (`page-texts.ts` y su prueba), que la página nueva ya no usa.
- Los enlaces de otras pantallas a `/admin/stakeholders/{id}` (por ejemplo `app/pages/billing/invoices/[id].vue`) pasan a `/admin/stakeholders?id={id}`.
- Comprobar contra el backend real los 409 y 400 que aquí se simulan con mensajes propios (por ejemplo, tipo de embalaje o cuadrilla en uso) y ajustar los textos si difieren.

---

## Fase 5 · Administración

**Commit FE:** `35f1746` — `feat(administracion): usuarios y auditoría con el patrón nuevo (DEC-080, F02)`.

### Qué quedó

| Pieza | Archivos (`Frontend/wms/`) |
| --- | --- |
| Contratos (copiados de `P01/` §2.3, tipos con `z.infer`) | `app/features/users/contracts/user.ts` (C-F01-59 a C-F01-67), `app/features/audit/contracts/audit-log.ts` (C-F01-68) |
| Fuentes (`I<Recurso>Source` y la fuente activa, simulada) | `user.source.ts` (listado, detalle, alta, edición, asignar y quitar roles, restablecer contraseña, activar o desactivar y roles del sistema); `audit-log.source.ts` (solo listado: el contrato no tiene lectura por Id) |
| Datos y fuentes simulados | 6 roles del sistema, 13 usuarios ficticios («Usuario CE 1», `ce.ejemplo1@ejemplo.com`; uno sin roles, dos inactivos, uno bloqueado hasta el 31/12/2026) y 30 registros de auditoría del 02/11 al 22/11/2026 con valores en JSON. Simulan los errores de hoy (`B/Wms.Application/Users/Commands/`): usuario o correo repetidos (400 «Error al guardar el usuario» con su lista), rol que no existe o lista vacía (400), bloqueo con fecha pasada (400), 404 «Usuario no encontrado»; y los de C-F01-00 en la auditoría (rango invertido, acción desconocida, orden fuera de la lista blanca) |
| Consultas (`*.queries.ts`) | Prefijos `['users']` (`list`, `detail`, `system-roles`) y `['audit-logs']` (`list`), con un segundo nivel que no choca con `useUsers` ni `useAuditLogs` de hoy; invalidación de `['users']` tras cada mutación |
| Usuarios (`/admin/users`) | Nombre ↕, Usuario ↕, Correo ↕ (filtros de texto; el de usuario va como `userName`, el orden como `username`), Roles (filtro por rol, `role`), Estado (filtro). «+ Nuevo usuario» y «Exportar». Ver, ✎ y activar o desactivar. Alta en modal a dos columnas (siete campos, D9) con contraseña y confirmación; edición a una columna sin contraseña. Drawer con `?id=`: datos, estado y «Bloqueado hasta», cambio de contraseña pendiente, roles con «Quitar» (con confirmación) y «Asignar roles» (varios a la vez); pie con Editar, «Restablecer contraseña» (modal con confirmación) y Activar o Desactivar (modal con «Bloqueado hasta» opcional) |
| Auditoría (`/admin/audit`) | Fecha ↕ (rango, `createdAtFrom`/`createdAtTo`), Usuario ↕, Acción ↕ (lista), Tabla ↕ (lista de entidades), Registro (texto; Id abreviado, completo en el `title`), Descripción. Orden por defecto: fecha descendente. «Exportar»; sin «Nuevo». Drawer con los datos y el valor anterior y el nuevo, lado a lado. `?affectedTable=` del detalle del depósito (WMS-29) sigue fijando el filtro de Tabla |
| Roles (D6) | Las dos páginas siguen en `["Admin"]`; con `?roles=ForeignTrade,Billing`, «Acceso denegado» |
| Guardias (revisión final, D14 y D15) | `list-pattern-routes.ts`: Usuarios y Auditoría pasan a `PATTERN`, que queda con las **14** rutas del menú que F02 rediseña; `PENDING` queda solo con las de D3 y las de F03 a F09 (29 rutas), y `F02` sale de `PENDING_FEATURES`. `mock-sources.spec.ts`: las dos páginas entran en `MAQUETACION_PAGES` |
| Pruebas | `test/unit/users/mocks.spec.ts` y `test/unit/audit/mocks.spec.ts` (nuevas): cada dato pasa su esquema y la fuente simulada responde con sus reglas y errores (D16) |

Notas, sin cambiar ninguna Dn:

- **El alta no lleva roles.** La pantalla de hoy pedía roles al crear (`rolIds`), pero el API no los recibe: `CreateUserCommand` no tiene ese campo y C-F01-61 tampoco. Tras crear, el drawer se abre con «Sin roles» y el aviso de asignarlos (QA2-F02-025).
- **Contraseña:** el formulario usa las reglas de hoy (`app/utils/password-schema.ts`, las mismas de `MustBeStrongPassword` del API) y su confirmación; el contrato (`userCreateSchema`, `userResetPasswordSchema`) se copió sin cambios, con su `min(8)` (`P01/` §2.3 deja el ajuste para I-01). La contraseña no se guarda en la fuente simulada.
- **«Bloqueado hasta»** se envía como el final del día elegido en hora de Colombia (`yyyy-MM-ddT23:59:59-05:00`), así que «Hoy» también vale; la pantalla de hoy enviaba la medianoche local.
- **Drawer de Auditoría sin `?id=`:** D9 sincroniza el drawer con `?id=`, pero C-F01-68 no tiene lectura por Id y ninguna pantalla enlaza un registro de auditoría por Id (el depósito enlaza por tabla). El drawer muestra la fila del listado; se cierra con ✕ o Escape.
- **«Exportar»** en las dos páginas, por la barra de D8 (la pantalla de hoy no lo tenía).

### Compuertas

| Compuerta | Antes (fase 4, `9e738bc`) | Después (`35f1746`) |
| --- | --- | --- |
| `yarn build` | código 0 | código 0 |
| `yarn test` | 129 archivos · 711 pruebas, en verde | 131 archivos · 722 pruebas, en verde |
| `yarn lint` | 262 errores · 390 avisos | 258 errores · 390 avisos (bajan con las páginas reescritas); 0 errores y 0 avisos en archivos nuevos o cambiados |
| Tipos (`nuxi typecheck`) | 71 errores, de archivos anteriores | 71, los mismos; ninguno en los archivos de la fase |
| Sin llamadas reales (D15) | `mock-sources.spec.ts` en verde | en verde, con Usuarios y Auditoría en `MAQUETACION_PAGES`; en el navegador, ninguna petición a `api/v1` y la consola sin errores |
| Datos simulados con sus esquemas (D16) | hasta los catálogos de la fase 4 | más roles del sistema, usuarios y registros de auditoría |
| Rutas nuevas en el menú | ninguna | ninguna (Administración enlaza Usuarios y Auditoría, que ya existían; ninguna ruta `/settings/…`) |
| Patrón de listado (D14) | 12 rutas en `PATTERN` | 14 rutas en `PATTERN`; `PENDING` sin rutas de F02 |

### Casos QA de la fase (contra los simulados)

| ID | Resultado | Evidencia |
| --- | --- | --- |
| QA2-F02-024 | PASA (`?roles=Admin`): Auditoría con rango 02/11 a 19/11/2026, usuario «admin» y acción «Actualización» deja 2 registros; el orden por fecha pasa de descendente a ascendente; «Ver» abre el drawer con el valor anterior y el nuevo | [f5-12](evidencias/f5-12-auditoria-listado.jpg), [f5-13](evidencias/f5-13-auditoria-filtros-orden-fecha.jpg), [f5-14](evidencias/f5-14-auditoria-drawer-valores.jpg) |
| QA2-F02-025 | PASA (`?roles=Admin`): «+ Nuevo usuario» abre el modal con contraseña y confirmación (valida reglas y coincidencia; usuario repetido da el aviso del 400 bajo el encabezado); al crear se abre el drawer; ahí se asignan Comercio Exterior y Facturación, se restablece la contraseña y se desactiva con «Bloqueado hasta» | [f5-02](evidencias/f5-02-usuario-modal-alta-validacion.jpg) a [f5-08](evidencias/f5-08-usuario-desactivado-drawer.jpg) |
| QA2-F02-026 | PASA: `yarn test` con `list-pattern` y `mock-sources` en verde, en su revisión final | — (código) |
| QA2-F02-004 (repaso) | PASA: `/admin/users` con `?roles=ForeignTrade,Billing` lleva a «Acceso denegado» (D6) | [f5-16](evidencias/f5-16-usuarios-acceso-denegado-ce-facturacion.jpg) |
| QA2-F02-006 y 013 (repaso) | PASA en las dos páginas y sus cuatro modales: botones con borde o relleno, sin clic de fila, etiquetas encima | capturas de la fase |

Capturas de la fase:

| Pantalla | Capturas |
| --- | --- |
| Usuarios | Listado ([f5-01](evidencias/f5-01-usuarios-listado.jpg)); modal de alta con validación ([f5-02](evidencias/f5-02-usuario-modal-alta-validacion.jpg)); usuario repetido ([f5-03](evidencias/f5-03-usuario-repetido-400.jpg)); creado, drawer sin roles ([f5-04](evidencias/f5-04-usuario-creado-drawer-sin-roles.jpg)); roles asignados ([f5-05](evidencias/f5-05-usuario-roles-asignados.jpg)); restablecer contraseña ([f5-06](evidencias/f5-06-usuario-restablecer-contrasena.jpg)); desactivar con bloqueo ([f5-07](evidencias/f5-07-usuario-desactivar-bloqueo.jpg)) y resultado ([f5-08](evidencias/f5-08-usuario-desactivado-drawer.jpg)); drawer tras recargar con `?id=` ([f5-09](evidencias/f5-09-usuario-drawer-recarga-id.jpg)); quitar rol ([f5-10](evidencias/f5-10-usuario-quitar-rol.jpg)); filtro por rol y orden por correo ([f5-11](evidencias/f5-11-usuarios-filtro-rol-orden-correo.jpg)); acceso denegado ([f5-16](evidencias/f5-16-usuarios-acceso-denegado-ce-facturacion.jpg)) |
| Auditoría | [f5-12](evidencias/f5-12-auditoria-listado.jpg), [f5-13](evidencias/f5-13-auditoria-filtros-orden-fecha.jpg), [f5-14](evidencias/f5-14-auditoria-drawer-valores.jpg); enlace del depósito `?affectedTable=WarehouseStorageProduct` ([f5-15](evidencias/f5-15-auditoria-enlace-tabla-deposito.jpg)) |
| Menú de Admin | Configuración y Administración (Usuarios, Auditoría) ([f5-17](evidencias/f5-17-menu-admin-administracion.jpg)) |

### Pendiente para I-01 (de esta fase)

- Escribir `user.http.ts` (C-F01-59 a C-F01-67; los roles del sistema con `GET administration/system-roles`) y `audit-log.http.ts` (C-F01-68), cambiar la línea de cada `*.source.ts`, borrar las carpetas `mocks/` de `users` y `audit`.
- Borrar `app/pages/admin/users/create.vue`, `edit/[id].vue` y `[id].vue`, y lo que solo ellas usan (`UserForm.vue`, `UserHeader.vue`, `UserProfile.vue`, `UserRoles.vue`, `UserResetPassword.vue`, `schemas/user-create-schema.ts` y su prueba, `useUserByID`, `useUserCreate`, `useUserUpdate`, `useAssignRoles`, `useRemoveRoles`, `useResetPassword`, `useManageActivation`, `useUsers`), y `useAuditLogs`, `audit-service.ts` y `types/audit-log.ts` si ya nadie los usa, tras comprobar con grep quién los importa.
- Ajustar `userCreateSchema` y `userResetPasswordSchema` a las reglas de `MustBeStrongPassword` (`P01/` §2.3, nota final).
- Comprobar contra el backend real: el código de los errores de usuario o correo repetidos (Identity: `DuplicateUserName`, `DuplicateEmail`; hoy se muestran arriba del formulario) y que «Bloqueado hasta» con `T23:59:59-05:00` pase la validación «La fecha de bloqueo debe ser en el futuro».
- **Filtro de Tabla de la auditoría:** C-F01-00 hace «contiene» en los filtros de texto, así que `WarehouseStorageProduct` también trae `WarehouseStorageProductPlacement` ([f5-15](evidencias/f5-15-auditoria-enlace-tabla-deposito.jpg)). Si se quiere igualdad exacta, es un cambio de contrato y pide decisión del usuario.
- Agregar a `app/features/audit/utils/entity-labels.ts` las entidades nuevas de F01 (por ejemplo `ExchangeRate`, que hoy se ve con su nombre de clase), con los nombres que confirme el backend.

---

## Cierre de la parte 2 (maquetación)

Las cinco fases quedaron hechas el 2026-11-23 en FE `f2/f02-base`: `d389685`, `813443f` (sobre el wip `3e85d79`), `4e60427`, `9e738bc` y `35f1746`, todas con push. La rama no se fusiona en `fase-2`: lo hace I-01 (`PM/` §5.3).

| Cifra | Base (`fase-2` `3aa6e3c`) | Cierre (`35f1746`) |
| --- | --- | --- |
| `yarn test` | 113 archivos · 608 pruebas, en verde | 131 archivos · 722 pruebas, en verde |
| `yarn lint` | 276 errores · 396 avisos | 258 errores · 390 avisos; 0 en archivos nuevos |
| Casos QA2-F02 | — | 001 a 026 recorridos contra los simulados, en PASA; se verifican de nuevo en I-01 contra el backend real (plan §6) |

Capturas de cada pantalla de F02:

| Pantalla | Capturas |
| --- | --- |
| P-TR-01 Menú por rol | [f2-01](evidencias/f2-01-menu-comercio-exterior.jpg), [f2-02](evidencias/f2-02-menu-facturacion.jpg), [f2-03](evidencias/f2-03-menu-admin.jpg), [f2-04a](evidencias/f2-04a-menu-vigilancia.jpg), [f2-04b](evidencias/f2-04b-menu-bascula.jpg), [f2-04c](evidencias/f2-04c-menu-bodega.jpg), [f5-17](evidencias/f5-17-menu-admin-administracion.jpg) |
| P-TR-10 Login, sidebar y tema | [f2-05](evidencias/f2-05-sidebar-tres-roles.jpg), [f2-06a](evidencias/f2-06a-login-oculta.jpg), [f2-06b](evidencias/f2-06b-login-visible.jpg), [f2-07](evidencias/f2-07-switch-tema-oscuro.jpg), [f2-08](evidencias/f2-08-modal-error-api.jpg) |
| P-TR-03, P-TR-09 y P-TR-11 (galería) | [f1-01](evidencias/f1-01-selector-busqueda.jpg) a [f1-05](evidencias/f1-05-drawer-detalle.jpg) |
| P-TR-02 y P-TR-03 Conductores | [f3-01](evidencias/f3-01-conductores-listado.jpg) a [f3-04](evidencias/f3-04-conductor-modal-editar.jpg) |
| Ubicaciones (P-TR-03 modal) | [f3-05](evidencias/f3-05-ubicacion-modal-dos-columnas.jpg), [f3-06](evidencias/f3-06-ubicacion-codigo-repetido.jpg) |
| P-TR-04 Motivos | [f3-07](evidencias/f3-07-motivos-listado.jpg) a [f3-09](evidencias/f3-09-motivo-pide-categoria.jpg) |
| P-TR-05 Prefijos · P-TR-06 Tasas | [f3-10](evidencias/f3-10-prefijo-ejemplo-al-digitar.jpg) a [f3-13](evidencias/f3-13-tasa-fechas-se-cruzan-409.jpg) |
| Vehículos | [f3-14](evidencias/f3-14-vehiculos-listado.jpg) a [f3-17](evidencias/f3-17-vehiculo-creado.jpg) |
| Configuración II (Terceros a Parámetros) | [f4-01](evidencias/f4-01-terceros-listado-facturacion.jpg) a [f4-23](evidencias/f4-23-parametro-modal-numero.jpg) |
| Usuarios · Auditoría | [f5-01](evidencias/f5-01-usuarios-listado.jpg) a [f5-16](evidencias/f5-16-usuarios-acceso-denegado-ce-facturacion.jpg) |

Lo que queda para I-01 está en la sección «Pendiente para I-01» de cada fase (3, 4 y 5) y en `P01/` §13; en resumen: escribir los `*.http.ts` de §3.2 del plan y cambiar la línea de cada `*.source.ts`; borrar las carpetas `mocks/` de los dominios y vaciar `MAQUETACION_PAGES`; enlazar Prefijos y Tasas de cambio en el menú; montar en los drawers de Terceros y Servicios las secciones de D11; borrar las páginas `create.vue`, `edit/[id].vue` y `[id].vue` de Usuarios, Terceros, Productos y Servicios con lo que solo ellas usan; y recorrer QA2-F02-001 a 026 contra el backend real.
