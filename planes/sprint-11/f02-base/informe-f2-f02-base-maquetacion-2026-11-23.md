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
