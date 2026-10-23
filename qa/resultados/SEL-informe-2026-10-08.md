# Informe de fase — SEL Selector de conductor (Fase 3 del plan: QA local)

> Plan: `code_workspace/docs/planes/plan-cerrado-selector-conductor-2026-10-08.md` §7. Casos registrados en `fase-03-bascula.md` §6.2 (CAM), `fase-04-bodega.md` §5.4 (RSB) y `fase-09-roles-permisos.md` §4.4 (API).
> Resultado esperado: decisiones D1 a D20 (§2) y criterios de teclado (§6) del plan.

## 1. Datos de la ejecución

| Campo | Valor |
|---|---|
| Fase | SEL — Selector de conductor con alta y edición en modal (Báscula y Bodega), Fase 3: QA local |
| Ejecutor | Agente QA (Claude Code) |
| Fecha y hora de inicio / fin (hora Colombia) | 2026-10-08, ~13:55 / ~14:45 |
| Ambiente | Local |
| Base de datos | `wms_migracion` (Postgres Docker `wms-postgres-db`, puerto 5433), con los 4.361 conductores migrados. **No** se usó `wmsdb`. |
| URL frontend / API | `http://localhost:3001` (`nuxt dev`, `NUXT_PUBLIC_API_BASE=http://localhost:5291/api/v1`) / `http://localhost:5291/api/v1` (`Development`, configuración de `db_legacy/trabajo/.env.migracion.local`) |
| Commit frontend / backend | FE `develop` `7d7516a` (Fase 2: `ef5d248` + `7d7516a`) / BE `develop` `3748ec6` (Fase 1). Confirmados con `git rev-parse --short HEAD`; los dos repositorios estaban limpios. |
| Arranque | API: `dotnet publish Wms.Api` de `3748ec6` en el scratchpad de la sesión, ejecutado con las variables de `.env.migracion.local`. Front: `nuxt dev --port 3001`. No se usó `.claude/launch.json` porque está versionado. |
| Navegador y versión, zona horaria | Navegador integrado de Claude Desktop (Chromium, `en-US`); fechas de negocio en hora Colombia (UTC-5). |
| Cuentas usadas (solo usuario) | `mig.vigilancia` (Receiving), `mig.bascula` (Scale), `mig.bodega` (Warehouse), `mig.facturacion` (Billing), `admin` (Admin). En el navegador inició sesión el usuario; por API, tokens de `POST /auth/login` sin imprimir el cuerpo. |

## 2. Criterios de entrada

| Criterio | ¿Cumple? | Evidencia / nota |
|---|---|---|
| Build de las Fases 1 y 2 commiteado | Sí | `HEAD` FE `7d7516a`, BE `3748ec6`. |
| Migraciones de `wms_migracion` al día | Sí | `__EFMigrationsHistory` (solo lectura) con las 11 migraciones del repositorio, de `20261001193201_InitialParityLegacy` a `20261007030137_RemoveSampleSeedData`. No se aplicó nada. |
| API y front levantados contra `wms_migracion` | Sí | API en 5291, front en 3001; login de las 6 cuentas por API → 200. |
| Sin BLOCKER abiertos en Báscula y Bodega | Sí | `INDICE.md`: 147 Verificadas y 1 Corregida (DEF-F11-022, menú) antes de esta fase. |
| Sin datos `QA-SEL` previos | Sí | 0 conductores `900000000%` y 0 placas `QSL%` al empezar. |

## 3. Resumen

Incluye los casos nuevos de §7.1 (21) y la regresión dirigida (4).

| Prioridad | Total | Pasa | Falla | Bloqueado | No aplica | No ejecutado | Observación |
|---|---|---|---|---|---|---|---|
| P0 | 7 | 7 | 0 | 0 | 0 | 0 | 0 |
| P1 | 14 | 11 | 2 | 0 | 0 | 1 | 0 |
| P2 | 4 | 4 | 0 | 0 | 0 | 0 | 0 |
| P3 | 0 | — | — | — | — | — | — |
| **Total** | **25** | **22** | **2** | **0** | **0** | **1** | **0** |

Solo casos nuevos de §7.1: 21 ejecutados de 21 (P0 5/5, P1 12/12, P2 4/4); 19 PASA y 2 FALLA.

## 4. Resultado por caso

Las capturas están en `docs/qa/resultados/evidencias/SEL/`. Las de pantallas con conductores migrados no se guardaron (datos personales).

### 4.1 Báscula — F3-CAM (usuario `mig.bascula`; F3-CAM-022 con `admin`)

| ID | P | Estado | Defecto / Obs. | Evidencia | Nota breve |
|---|---|---|---|---|---|
| F3-CAM-003 | P0 | PASA | — | `F3-CAM-003-faltantes.jpg`; DOM | `QSL101` vacío → «Faltan 4 datos»: transportadora, país, tipo y **un solo** «Conductor» (D17), todos con «Requerido»; el foco va a la transportadora. Con solo el conductor faltante, el foco va a `#driverId [role=combobox]`. No guarda. |
| F3-CAM-004 | P1 | PASA | — | `F3-CAM-005-registrado-seleccionado.jpg`; DOM | «qa-se» lista «QA-SEL Tres · CC 9000000003» y «QA-SEL Uno · CC 9000000001» (D7). Con `QA-SEL Uno` sin país y el vehículo en Ecuador, debajo del select se lee «País: Ecuador (del vehículo)» (D15). |
| F3-CAM-005 | P1 | PASA | DEF-F11-024 (visto aquí) | `F3-CAM-005-registrado-seleccionado.jpg`; SQL | «+» → CC `9000000001`, `QA-SEL` / `Uno` → «Registrar conductor». El modal se cierra con «Conductor registrado — QA-SEL Uno quedó seleccionado.» y el foco vuelve al select. El conductor existe en `drivers` (14:18:00) **antes** de guardar la ficha (D9). Hubo que volver a escribir el apellido, que se perdió por DEF-F11-024. |
| F3-CAM-013 | P0 | PASA | — | DOM | «00000001» trae `QA-SEL Uno`; «9000 0000 03» (con espacios) trae `QA-SEL Tres` (D4). |
| F3-CAM-014 | P1 | PASA | — | DOM; API T3 | «uno qa-sel» («apellido nombre») trae `QA-SEL Uno`. Un apellido migrado con tilde escrito sin tilde trae 20 opciones con tilde, que el filtro local no oculta (D8); pie «Mostrando 20 de 35…», igual que el API y que SQL. |
| F3-CAM-015 | P2 | PASA | — | DOM + API | Sin texto: 20 opciones, pie «Mostrando 20 de 4362. Escriba nombre o documento para afinar.» (D6). Orden por nombres y luego apellidos (D5), igual que `GET /drivers?orderByName=true`. Con pocos resultados, sin pie. |
| F3-CAM-016 | P1 | FALLA | DEF-F11-025 | `F3-CAM-016-ya-registrado.jpg`; SQL | «+» con `9000000001`: «Este conductor ya está registrado.», datos precargados y botón «Usar este conductor» (D10). Queda seleccionado y sin duplicado (1 fila). **Pero** sin cambios del operario envía `PATCH` con el país del vehículo («Ecuador») y avisa «Conductor actualizado exitosamente» (contradice D10 y D15). |
| F3-CAM-017 | P1 | PASA | — | DOM; SQL; `admin-conductores-qa-sel.jpg` | Lápiz → «Editar conductor», tipo deshabilitado y número `readonly`; teléfono `3000000001` → «Guardar cambios» → «Conductor actualizado exitosamente». Persistido; el select sigue con `QA-SEL Uno`. |
| F3-CAM-018 | P2 | PASA | — | DOM | Limpiar (×): lápiz deshabilitado, «+» habilitado, vuelve «Falta 1 dato». |
| F3-CAM-019 | P1 | PASA | — | DOM | Tras guardar `QSL101`, soltar el camión, recargar la página y «Recuperar operaciones» → «Retomar»: «QA-SEL Uno · CC 9000000001» preseleccionado (D16), lápiz habilitado, sin «Faltan». |
| F3-CAM-020 | P0 | PASA | — | SQL | `entry_logs` de `QSL101` → `QA-SEL Uno`; `QSL102` (F3-REG-001) → `QA-SEL Tres`. Los datos del conductor no cambiaron al guardar: `QA-SEL Tres` siguió con país Colombia aunque el vehículo era de Ecuador (DEF-F11-008 sin regresión). |
| F3-CAM-021 | P1 | FALLA | DEF-F11-023, DEF-F11-024, DEF-F11-026; OBS-SEL-01 | DOM; §6 de este informe | Cumple: Tab al select, texto, Enter elige y no guarda la ficha (sin `POST` ni validaciones); el modal abre con el foco en «Tipo de Documento»; «Guardar» sin conductor lleva el foco al select. Falla: Esc no cierra el modal desde «Tipo de Documento» (023); al salir del documento en el modal se pierde el foco y lo tecleado (024); Enter antes de que llegue la búsqueda cierra sin elegir (026). |
| F3-CAM-022 | P2 | PASA | — | `F3-CAM-022-inactivo-no-aparece.jpg` | `admin` desactiva `QA-SEL Dos` en Admin → Conductores. En Báscula (`QSL104`), «dos qa» y «9000000002» → «Sin resultados. Use «+» para registrar el conductor.»; «qa-sel» solo trae Uno y Tres. |

### 4.2 Bodega — F4-RSB (usuario `mig.bodega`, camión `QSL103`)

| ID | P | Estado | Defecto / Obs. | Evidencia | Nota breve |
|---|---|---|---|---|---|
| F4-RSB-008 | P0 | PASA | — | Red; SQL; `GET receptions/{id}` | Selector → `QA-SEL Tres`; formulario completo (cliente migrado, producto migrado, 10 sacos, ubicación, firma, motivo «QA-SEL…») → `POST warehouse/receptions/without-weighbridge` → 201. Depósito `2026INSP00001` en Borrador, carta porte `QA-SEL-CP-0002`, stock 0 → 10, sin diferencia. La recepción devuelve `driverName = QA-SEL Tres`, `driverIdNumber = 9000000003`; el ingreso queda con `QA-SEL Tres`. Un solo ingreso. |
| F4-RSB-009 | P0 | PASA | — | Red | «+» → CC `9000000002`, `QA-SEL` / `Dos` → `POST /drivers` → **201** (sin 403, D13). «Conductor registrado — QA-SEL Dos quedó seleccionado.» |
| F4-RSB-010 | P1 | PASA | — | Red; `admin-conductores-qa-sel.jpg` | Lápiz → teléfono `3000000002` → `PATCH /drivers/{id}` → **200**. «Conductor actualizado exitosamente». |
| F4-RSB-011 | P1 | PASA | — | DOM | Formulario completo salvo el conductor → «Completar Recepción Manual» → «Campos incompletos — Conductor requerido: selecciónelo o regístrelo con «+».» (D18). No guarda. El botón se habilita solo con firma: para llegar al mensaje hay que capturarla. |

### 4.3 Permisos — F9-API (curl; detalle en `evidencias/SEL/api-permisos-y-medicion-2026-10-08.md`)

| ID | P | Estado | Defecto / Obs. | Evidencia | Nota breve |
|---|---|---|---|---|---|
| F9-API-022 | P1 | PASA | — | `POST /drivers` → 201; `PATCH /drivers/1be8af80-…` → 200 | Warehouse (`mig.bodega`) crea `QA-SEL Tres` y lo edita. Contraste: `POST /drivers {}` → 400 «Error de validación.», no 403. |
| F9-API-023 | P1 | PASA | — | `POST /vehicles {}` → 403 | Warehouse sigue sin poder crear vehículos (`TransportCatalogAccess`). |
| F9-API-024 | P1 | PASA | — | `POST /drivers {}` → 403; `PATCH /drivers/{id} {}` → 403 | Billing (`mig.facturacion`). |
| F9-API-025 | P2 | PASA | — | `GET /drivers?search=qa&…` sin token → 401 | — |

### 4.4 Regresión dirigida

| ID | P | Estado | Defecto / Obs. | Evidencia | Nota breve |
|---|---|---|---|---|---|
| F3-REG-001 | P0 | PASA | — | Aviso; SQL | `QSL102`, adaptado a `wms_migracion`: Ingreso con depósito, Importación, Carta Porte `QA-SEL-CP-0001` («Documento nuevo: al guardar se crea un depósito.»), producto migrado × 10, cliente migrado (persona jurídica), conductor `QA-SEL Tres` por teclado → Guardar. Aviso «Depósito 2026BA00001 creado — Documento QA-SEL-CP-0001»; la ficha pasa a Cobro. Sin cobro ni peso. Después: «Recuperar operaciones» → «Descartar» → servicio `Discarded`, depósito `Cancelled`, enlace con el ingreso liberado. |
| F3-CAM-010 | P1 | PASA | — | SQL; red | `QSL101` Solo báscula completa: registro (`POST weighbridge/weighing-only/initiate` → 201), cobro inmediato en efectivo a «Consumidor final» ($20.000, `Paid`), peso 12.500 kg, «Ciclo completado», tiquete `2026T00002` (no se imprimió) y «Finalizar». Persisten en el ingreso el conductor (`QA-SEL Uno`) y en el vehículo la transportadora, el país (Ecuador) y el tipo (Sencillo). |
| F3-CAM-011 | P1 | NO EJECUTADO | — | SQL | No hay orden de cargue pendiente en `wms_migracion`: `loading_orders` tiene 1, `Dispatched`. Por instrucción, no se armó una cadena de importación para crearla. |
| F4-RSB-002 | P0 | PASA | — | Ver F4-RSB-008 | Cubierto por F4-RSB-008: el depósito se crea desde la recepción directa, en Borrador y con stock declarado. |

## 5. Defectos nuevos

| ID | Severidad | Título | Caso | Módulo |
|---|---|---|---|---|
| [DEF-F11-023](defectos/DEF-F11-023.md) | MINOR | Esc no cierra el modal del conductor cuando el foco está en «Tipo de Documento» | F3-CAM-021 | Báscula / Bodega |
| [DEF-F11-024](defectos/DEF-F11-024.md) | MINOR | En el modal del conductor, al salir del documento se pierde el foco y lo que se teclea después | F3-CAM-005, 016, 021 | Báscula / Bodega |
| [DEF-F11-025](defectos/DEF-F11-025.md) | CRITICAL (reclasificado por el usuario; corregido, ver anexo) | «Usar este conductor» guarda en el conductor el país del vehículo sin que el operario lo cambie | F3-CAM-016 | Báscula / Bodega |
| [DEF-F11-027](defectos/DEF-F11-027.md) | MAJOR (corregido, ver anexo) | El filtro por nombre de Administración → Conductores no filtra | — (antes OBS-SEL-02) | Administración |
| [DEF-F11-026](defectos/DEF-F11-026.md) | MINOR | Enter antes de que llegue la búsqueda cierra el selector sin elegir y borra lo escrito | F3-CAM-021 | Báscula / Bodega |

DEF-F11-024 ya existía en `DriverForm` antes de la Fase 2. Se registra porque ahora afecta al modal de «+», el camino nuevo para registrar.

**Observaciones (sin ficha):**

- **OBS-SEL-01 (UX, F3-CAM-021).** Desde el select del conductor, el Tab siguiente va a «+» y luego al lápiz antes de llegar a «Tipo de operación»: dos Tab más que con el formulario anterior. No son clics, pero cuentan en el criterio «Tab a lo siguiente» de §6.
- **OBS-SEL-02 → DEF-F11-027.** Filtro por nombre de Administración → Conductores (`firstName` en lugar de `name`). El usuario pidió corregirlo antes de staging; ver anexo.

## 6. Mediciones

### 6.1 API — `GET /drivers?search={t}&isActive=true&orderByName=true&pageIndex=1&pageSize=20` (plan §7.2)

Usuario `mig.bascula`. `curl -w '%{time_total}'`, 3 corridas por término. Términos descritos de forma genérica.

| # | Término | totalCount | t1 / t2 / t3 (s) |
|---|---|---|---|
| T1 | Apellido más frecuente de 5 letras, en minúsculas | 76 | 0,080 / 0,030 / 0,027 |
| T2 | Fragmento de 4 dígitos de una cédula | 16 | 0,026 / 0,021 / 0,024 |
| T3 | Apellido con tilde escrito sin tilde | 35 | 0,023 / 0,023 / 0,024 |
| T4 | «apellido nombre» (orden invertido) | 1 | 0,029 / 0,027 / 0,024 |
| T5 | Prefijo de 3 letras del nombre más frecuente | 237 | 0,020 / 0,023 / 0,023 |

- El `totalCount` coincide en los 5 términos con un `count(*)` SQL de solo lectura con la misma regla D4.
- Criterio < 1 s: **cumple** en las 15 corridas (máximo 0,080 s).
- Sin `search`: `totalCount` 4.362, 0,002 a 0,014 s.

### 6.2 Teclado (plan §6, dentro de F3-CAM-021)

| Criterio | Resultado |
|---|---|
| Caso común sin clics extra (Tab, 3-4 caracteres, Enter, Tab) | Cumple, sin ratón. Con OBS-SEL-01 (dos Tab más) y DEF-F11-026 (Enter demasiado rápido). |
| Enter en el filtro elige y no guarda la ficha | Cumple: sin `POST` ni validaciones de la ficha tras Enter. |
| Foco del modal en «Tipo de Documento» | Cumple (alta). En edición, el tipo está bloqueado y el foco va a «Apellidos». |
| Esc cierra el modal | **No** desde «Tipo de Documento» (DEF-F11-023); sí desde los demás campos. |
| «Guardar» sin conductor lleva el foco al select | Cumple. |

**Tramo «Tab al select → conductor elegido»** con `QA-SEL Uno` («uno q»):

| Corrida | Tiempo | Pausa antes de Enter |
|---|---|---|
| 1 | 1.065 ms | 1 s |
| 2 | 557 ms | 0,5 s |
| 3 | 551 ms | 0,5 s |

Medido con `performance.now()` en la página, desde el `keydown` de Tab hasta que el select muestra el conductor, con teclas enviadas por el agente, no con un reloj humano. Es una referencia, **no PRF-002**. Con una pausa de 0,2 s, Enter no elige (DEF-F11-026).

## 7. Datos creados o modificados en `wms_migracion`

| Dato | Detalle | Estado final |
|---|---|---|
| Conductor `QA-SEL Uno` | CC `9000000001`; creado por «+» en Báscula (F3-CAM-005) | Activo; país Ecuador (escrito por DEF-F11-025) y teléfono `3000000001` (F3-CAM-017) |
| Conductor `QA-SEL Dos` | CC `9000000002`; creado por «+» en Bodega (F4-RSB-009) | **Inactivo** (F3-CAM-022); país Ecuador, teléfono `3000000002` |
| Conductor `QA-SEL Tres` | CC `9000000003`; creado por API con Warehouse (F9-API-022) | Activo; país Colombia, teléfono `3000000003` |
| Vehículos `QSL101`–`QSL104` | Creados por API con `mig.vigilancia` | `QSL101`: DESCONOCIDA · Ecuador · Sencillo. `QSL102`: tipo Tractomula. `QSL103`: datos de la recepción. `QSL104`: sin datos. |
| Ingresos | `QSL101` y `QSL104` «Solo Bascula», `QSL102` «Descargue mercancia importacion», `QSL103` «Solo bodega»; observación «QA-SEL» | Todos con **salida registrada** (`mig.vigilancia`, API): 3 a las 14:33 y `QSL104` a las 14:37 |
| Operación Solo báscula de `QSL101` | Servicio `34be2ff4-…`, tiquete `2026T00002`, cliente de la operación: persona jurídica migrada | `Completed` |
| Factura de báscula | `65f19b7f-…`, $20.000, destinatario Consumidor final (`222222222222`), sin N.º SIIGO | `Paid` |
| Depósito `2026BA00001` | Carta porte `QA-SEL-CP-0001` (F3-REG-001) | Servicio `Discarded`, depósito `Cancelled` |
| Depósito `2026INSP00001` | Carta porte `QA-SEL-CP-0002`, recepción directa `38d3dfd5-…` (F4-RSB-008), 10 sacos de un producto migrado, cliente persona jurídica migrada | Borrador, stock 10, sin factura ni período de almacenamiento |
| Conductor `QA-SEL Cuatro` | CC `9000000004`, **sin país**; creado por API con Scale para el re-test de DEF-F11-025 | Activo; país `NULL` y teléfono `3000000004` (lápiz) |
| Vehículo e ingreso `QSL105` | «Solo Bascula», «QA-SEL», para el re-test de DEF-F11-025; sin operación de báscula | Salida registrada |

Consumen consecutivos de `wms_migracion`: `2026T00002`, `2026BA00001` y `2026INSP00001`. No se editaron ni desactivaron conductores migrados. No se escribió en la base con SQL.

## 8. Criterios de salida

| Criterio | ¿Cumple? | Nota |
|---|---|---|
| 100 % P0 | Sí | 7/7 ejecutados y PASA. |
| P1 ≥ 95 % ejecutados | Sí en los casos nuevos; no con la regresión | Casos nuevos de §7.1: 12/12 (100 %). Con la regresión dirigida: 13/14 (92,9 %), porque F3-CAM-011 quedó NO EJECUTADO sin datos, como prevé la instrucción de la fase. |
| Cero BLOCKER, CRITICAL y MAJOR abiertos | Sí (tras el anexo) | DEF-F11-025 (CRITICAL) y DEF-F11-027 (MAJOR) quedan «Corregido» y verificados en local; siguen abiertos 3 MINOR (023, 024 y 026). |
| Todos los FALLA con defecto y evidencia | Sí | F3-CAM-016 → DEF-F11-025; F3-CAM-021 → DEF-F11-023, 024 y 026. |
| Medición del API < 1 s | Sí | Máximo 0,080 s. |
| Datos registrados | Sí | §7. |

## 9. Checkpoint

- **Veredicto local: «Listo para staging».**
  - No hay defectos BLOCKER, CRITICAL ni MAJOR. P0 al 100 % y P1 de los casos nuevos al 100 %.
  - Con la regresión incluida, P1 queda en 92,9 %, por F3-CAM-011 sin orden de cargue pendiente. El usuario decide si eso lo condiciona.
  - Por la regla de la fase, la Fase 4 espera la corrección de DEF-F11-023 a 026 y su re-test, o la decisión del usuario de convivir con ellos.
- **Casos a re-ejecutar tras las correcciones:**
  - F3-CAM-016 y F3-CAM-021, con los cuatro criterios de §6;
  - F3-CAM-005, alta por teclado sin reescribir campos;
  - F4-RSB-009, el mismo modal en Bodega;
  - F3-CAM-011, si aparece una orden de cargue pendiente.
- **Preguntas abiertas para el usuario:**
  1. ¿Se corrigen los cuatro MINOR antes de staging o se acepta convivir con ellos?
  2. ¿Se abre ficha para OBS-SEL-02 (filtro por nombre de Admin)?
- **Incidencia de proceso:** durante la preparación, las contraseñas de las cuentas `mig.*` aparecieron una vez en la salida de un comando de la sesión: un filtro no correspondía al formato del archivo de credenciales. No están en este informe, ni en las fichas, ni en las evidencias.
- **Documentación de usuario:**
  - `guiones-video-tutoriales.md`: guiones 5.2, 5.3, 5.9 y 6.4.
  - `inventario-cambios-guiones.md`: fila 21 de §5.
  - `guia-pruebas-operarios.md`: un punto en «Para explorar» de Báscula; ningún paso pedía digitar el conductor.
  - **El PDF de guiones queda por regenerar:** no existe el entorno virtual `~/.venvs/guiones-wms` de `generar-pdf.md` y no se instaló nada.

- **Actualización del 2026-10-08 (anexo):** el usuario reclasificó DEF-F11-025 a CRITICAL y pidió corregir también DEF-F11-027 antes de staging. Los dos quedan «Corregido» y verificados en local, con cambios de frontend sin commit. El veredicto «Listo para staging» se mantiene sujeto al commit de esas correcciones. Los 3 MINOR restantes no bloquean, salvo que el usuario decida lo contrario.

> El ejecutor se detiene aquí. La Fase 4 (staging) empieza solo con autorización del usuario, después del commit de esta fase.

## Anexo — Re-test (2026-10-08)

Correcciones pedidas por el usuario antes de staging. FE `7d7516a` con cambios sin commit, BE `3748ec6`, local `wms_migracion`.

| Defecto | Caso | Build | Resultado | Nota |
|---|---|---|---|---|
| DEF-F11-025 (CRITICAL) | F3-CAM-016 y lápiz (F3-CAM-017 / F4-RSB-010) | FE `7d7516a` + `driver-option.ts`, `DriverFormDialog.vue` | Verificado | `admin`, camión `QSL105` con Ecuador, conductor `QA-SEL Cuatro` sin país. «+» con `9000000004` → «Usar este conductor»: sin `PATCH` ni aviso, seleccionado, «País: Ecuador (del vehículo)». Lápiz → teléfono `3000000004` → `PATCH` 200 y `country` sigue `NULL`. La misma causa afectaba al lápiz y quedó corregida. |
| DEF-F11-027 (MAJOR) | Admin → Conductores, filtro «Nombre» | FE `7d7516a` + `pages/admin/drivers/index.vue` | Verificado | «QA-SEL» → `GET /drivers?...&name=QA-SEL` → 3 registros. |

- **Pruebas:** `yarn test` → 78 archivos y 345 pruebas en verde, con 11 nuevas (7 unitarias y 4 del modal).
- **Lint:** los archivos tocados quedan igual que la base (2 errores previos en la página de Admin).
- **Tipos:** `vue-tsc` limitado a los archivos tocados no da errores nuevos; el de `isActive` en la línea 281 es previo.

## Staging

Fase 4 del plan (§8), 2026-10-08, 15:16 a 15:47 (hora Colombia). Ejecutor: agente (Claude Code). Detalle y peticiones en `evidencias/SEL/staging-redespliegue-y-qa-2026-10-08.md`; captura de DEF-F11-027 en `evidencias/SEL/staging-admin-filtro-nombre-qa-sel.jpg`.

### S.1 Build desplegado

| Campo | Valor |
|---|---|
| Staging antes | BE `84c712f` / FE `8527144`, 11 migraciones |
| Desplegado | **BE `044be08`** (código de `3748ec6`) / **FE `4ca4e0a`**. Son los `HEAD` de `develop`, los mismos que preveía el prompt |
| Migraciones | `git diff --stat 84c712f..HEAD -- Wms.Infrastructure/Migrations` vacío: siguen 11, no se aplicó ninguna |
| `yarn test` en FE `4ca4e0a` | 78 archivos, 345 pruebas en verde |
| Pasos | `backend` → `up` (solo se recreó `wms-api`) → `frontend` → `smoke` (frontend 200, SPA 200, login inválido 400, CORS correcto). Arranque del API limpio. Sin `config` ni `migrate`; `pgdata` y `caddy_data` intactos; base sin recrear ni restaurar; sin SQL de escritura |
| Ventana | El usuario confirmó que no había operarios en staging antes del despliegue |
| Cuentas | API: `admin`, `qa.vigilancia`, `qa.bascula`, `qa.bodega`, `qa.comext`, `qa.facturacion`. Navegador: `admin`, `qa.bascula`, `qa.bodega`, con la sesión iniciada por el usuario |

**Commits que entraron:**

- **Backend:** `3748ec6` (búsqueda paginada y `DriverCatalogAccess`), más los documentos `4ba968e`, `5bcdbd8`, `7be5700`, `e6a1ccd`, `b7c656e` y `044be08`.
- **Frontend:**
  - el selector: `ef5d248`, `7d7516a` y la corrección `4ca4e0a` (DEF-F11-025 y DEF-F11-027);
  - `ec192cd`, el menú (DEF-F11-022);
  - `1db3448`, el precio base con centavos;
  - `944ce53`, Solo báscula preselecciona BRUTO;
  - los documentos `59d9b08`, `429be4d` y `9ecd333`;
  - `f63439c`, `31f2007` y `e01d81d` (`tools/video-tutoriales`), que no forman parte de la app generada.

### S.2 Respaldos

| Momento | Archivo | Estado |
|---|---|---|
| Antes de desplegar (15:17) | `/opt/wms/backups/2026/10/wms_20261008_151727_77114401.dump` (4.478.225 B) | `Succeeded` |
| Después de las pruebas (15:47) | `/opt/wms/backups/2026/10/wms_20261008_154700_53e8fdc1.dump` (4.482.286 B) | `Succeeded` |

### S.3 Resultado por caso

| Caso | Estado | Nota |
|---|---|---|
| S1 — búsqueda en el API | PASA | 5 términos genéricos × 3 corridas: resultados pertinentes, `pageSize` 20, `totalCount` igual al conteo esperado y orden por nombre (§S.4) |
| S2 — F9-API-022 a 025 | PASA | `qa.bodega`: `POST /drivers {}` → 400 (no 403) y `PATCH` sobre `QA-SEL Uno` → 200; `POST /vehicles {}` → 403. `qa.facturacion`: `POST /drivers {}` → 403. Sin token: `GET /drivers?search=x` → 401 |
| S3 — ingresos | PASA | `qa.vigilancia` (API): `QSL801` y `QSL803` «Solo Bascula», `QSL802` «Solo bodega», con la observación «QA-SEL»; aparecen en la cola de báscula y en la Recepción Directa |
| S4 — F3-CAM-004 | PASA | «qa-se» → «QA-SEL Tres · CC 9000000803»; «País: Ecuador (del vehículo)» |
| S4 — F3-CAM-005 | PASA | «+» crea `QA-SEL Uno` (`POST` 201); queda seleccionado y existe en el API antes de guardar la ficha. Con DEF-F11-024 |
| S4 — F3-CAM-013 | PASA | «0000 0803» (con espacio) → `QA-SEL Tres` |
| S4 — F3-CAM-014 | PASA | «tres qa-sel» → `QA-SEL Tres` |
| S4 — F3-CAM-015 | PASA | Sin texto: «Mostrando 20 de 4365. Escriba nombre o documento para afinar.» |
| S4 — F3-CAM-016 | PASA | Con `9000000801`: «ya está registrado», «Usar este conductor», sin `PATCH` ni duplicado |
| S4 — F3-CAM-017 | PASA | Lápiz: documento bloqueado; teléfono `3000000801` → `PATCH` 200 |
| S4 — F3-CAM-021 | PASA con MINOR conocidos | Tab al select, tecla, texto, Enter elige y no guarda la ficha. Esc no cierra el modal desde «Tipo de Documento» (DEF-F11-023). Tab siguiente → «+» (OBS-SEL-01). DEF-F11-026 no se repitió a propósito |
| S5 — F3-CAM-020 | PASA | `QSL801` guardado como Solo báscula, cliente «QA-S6 Cliente Uno SAS» (`initiate` 201). El ingreso queda con `QA-SEL Uno` y ningún conductor cambió al guardar |
| S6 — limpieza | PASA | Descarte en «Recuperar operaciones» (`DELETE` 204), sin cobro ni factura; salida de `QSL801` |
| Re-test DEF-F11-025 (CRITICAL) | **Verificado** | `QA-SEL Tres` sin país, `QSL803` en Ecuador: «Usar este conductor» sin `PATCH` y con «País: Ecuador (del vehículo)», `country` sigue `null`. El lápiz da `PATCH` 200 y `country` sigue `null`. Camión soltado y salida registrada |
| S7 — F4-RSB-009 | PASA | `qa.bodega`: «+» crea `QA-SEL Dos`, `POST` **201** (sin 403) |
| S7 — F4-RSB-010 | PASA | Lápiz sobre `QA-SEL Dos`, `PATCH` **200** |
| S7 — F4-RSB-011 | PASA | Sin conductor: «Conductor requerido: selecciónelo o regístrelo con «+».». No se guardó la recepción |
| S8 — limpieza | PASA | Salida de `QSL802`; sin operación ni depósito |
| Re-test DEF-F11-027 (MAJOR) | **Verificado** | Filtro «Nombre» = «QA-SEL» → `GET /drivers?…&name=QA-SEL` → 3 conductores |
| Re-test DEF-F11-022 (MINOR) | **Verificado** | La entrada tocada queda resaltada en su grupo; Facturación › Clientes no salta a «Listado»; la carga directa elige siempre la misma entrada |
| Observación `1db3448` | Correcto | El precio vigente de BASCULA se ve «$ 16.806,72» y el campo acepta `12345,67`. Se canceló sin guardar |
| Observación `944ce53` | No observado | El tipo del primer pesaje está en la etapa Peso, después del cobro, y la fase prohíbe cobrar. Queda cubierto por las pruebas de `WeightCapture.spec.ts`; se puede mirar en PRF-002 |
| S9 — humo | PASA | Login de las 6 cuentas → 200. BA0042: `Confirmed`, EC0004054, 398, USD, Nacionalizado. Cola de báscula y Vigilancia → Salida sin camiones `QSL`. P1, P2, P3 y P6 siguen en la cola sin iniciar; P3 con 2.000 unidades y la OC `2026OC00004` `Pending` por 200; P4 con 1.350 sin nacionalizar; P5 en Borrador por $558.159,96 y $474.566,16. 146 facturas, ninguna creada durante la sesión. Solo los tres `QA-SEL` cambiaron entre los conductores |

### S.4 Mediciones de S1

`GET /drivers?search={t}&isActive=true&orderByName=true&pageIndex=1&pageSize=20` con `qa.bascula`, desde el Mac por internet. El tiempo incluye la red y TLS.

| # | Término (descripción genérica) | totalCount | t1 / t2 / t3 (s) |
|---|---|---|---|
| T1 | Apellido frecuente de 5 letras, en minúsculas | 76 | 0,364 / 0,290 / 0,298 |
| T2 | Fragmento de 4 dígitos de una cédula | 12 | 0,354 / 0,307 / 0,326 |
| T3 | Apellido con tilde escrito sin tilde | 35 | 0,348 / 0,313 / 0,296 |
| T4 | «apellido nombre» (orden invertido) | 1 | 0,294 / 0,306 / 0,308 |
| T5 | Prefijo de 3 letras del nombre más frecuente | 238 | 0,286 / 0,325 / 0,301 |

Máximo 0,364 s: **cumple** el criterio de < 1 s. Al empezar había 4.364 conductores activos: los 4.361 migrados y 3 de ejemplo QA-S6.

### S.5 Defectos

- **Sin defectos nuevos** en staging.
- **MINOR conocidos, abiertos por decisión del usuario:**
  - **DEF-F11-023:** Esc desde «Tipo de Documento». Visto en staging.
  - **DEF-F11-024:** foco perdido tras el documento. Visto en staging, en Báscula y en Bodega.
  - **DEF-F11-026:** Enter antes de que llegue la búsqueda. No se repitió.
- **Observación sin ficha (OBS-SEL-01, ya conocida):** desde el select del conductor, Tab pasa por «+» y el lápiz antes de seguir.
- **Nota de ejecución:** la herramienta de escritura del navegador inserta texto sin eventos de tecla. Con el select cerrado, ese texto no abre el filtro; una pulsación real sí lo abre y lo filtra. No es un defecto.

### S.6 Datos `QA-SEL` que quedan en staging

| Dato | Estado final |
|---|---|
| Conductor `QA-SEL Uno` | CC `9000000801`, activo, país Ecuador (lo trajo el modal de alta, heredado del vehículo) y teléfono `3000000801` |
| Conductor `QA-SEL Dos` | CC `9000000802`, activo, país Ecuador (ídem) y teléfono `3000000802` |
| Conductor `QA-SEL Tres` | CC `9000000803`, activo, país `null` y teléfono `3000000803` |
| Vehículos `QSL801`, `QSL802` y `QSL803` | Creados por `qa.vigilancia`. `QSL801` quedó con «QA-S6 Transportadora SAS», Ecuador y Sencillo. `QSL802` y `QSL803` solo con la placa: la Recepción Directa y la ficha de `QSL803` no se guardaron |
| Ingresos de `QSL801`, `QSL802` y `QSL803` | Observación «QA-SEL»; **salida registrada** a las 15:36, 15:42 y 15:38. Ninguno en planta ni en la cola |
| Operación Solo báscula de `QSL801` | Descartada en «Recuperar operaciones»: el ingreso quedó sin operación. Sin cobro, factura, tiquete ni depósito |

No se editaron, desactivaron ni registraron datos sobre conductores migrados. No se tocaron P1-P6, CAH514, QSP001 ni las operaciones de los operarios.

### S.7 Veredicto

**«Verificado en staging».**

- No hay BLOCKER, CRITICAL ni MAJOR abiertos: DEF-F11-025 (CRITICAL) y DEF-F11-027 (MAJOR) quedan verificados en staging, igual que DEF-F11-022.
- Siguen abiertos los 3 MINOR conocidos (023, 024 y 026), por decisión del usuario.

**Nota — PRF-002.** El cronometraje de báscula con un operario (≤ 30 s; con F3-REG-024 y F3-PES-015) **debe medirse con este build** (FE `4ca4e0a` / BE `044be08`), porque cambió la card del conductor. El camión reservado sigue siendo **CAH514** (P6), sin iniciar en la cola.

### S.8 Pendientes para la guía de operarios

No se editó `guia-pruebas-operarios.md` en esta fase. Queda pendiente:

1. En «Avisos importantes» o en «Datos de ejemplo», mencionar los conductores `QA-SEL Uno/Dos/Tres` y las placas `QSL801` a `QSL803` como datos de prueba del equipo técnico que no se deben modificar.
2. En el punto del selector (Báscula, «Para explorar», que ya cubre la Recepción Directa), agregar dos avisos. Al registrar un conductor nuevo, el foco puede saltar tras escribir el documento (DEF-F11-024): hay que hacer clic en «Apellidos» antes de seguir. El modal se cierra con «Cancelar» o la «X» (DEF-F11-023).
3. Para PRF-002, recordarle al responsable que la medición se hace con este build.
