# Evidencia SEL — Fase 4: redespliegue de staging y QA en staging

Staging · app `https://app.100-60-89-139.sslip.io` · API `https://api.100-60-89-139.sslip.io/api/v1` · 2026-10-08, 15:16 a 15:47 (hora Colombia).
Tokens con `POST /auth/login`, leyendo las contraseñas de los archivos locales sin imprimirlas. En el navegador integrado, el usuario inició sesión con cada cuenta. Sin contraseñas, tokens ni datos de personas naturales en este archivo.

## 1. Comprobaciones previas

| Comprobación | Resultado |
|---|---|
| `git rev-parse --short HEAD` | BE `044be08` · FE `4ca4e0a` (los dos repositorios limpios, en `develop`) |
| `git log --oneline 84c712f..HEAD` (BE) | `3748ec6` feat(conductores) · `b7c656e`, `e6a1ccd`, `7be5700`, `5bcdbd8`, `4ba968e` y `044be08`: solo documentos |
| `git log --oneline 8527144..HEAD` (FE) | `ec192cd` menú (DEF-F11-022) · `429be4d` ficha · `1db3448` precio base con centavos · `944ce53` Solo báscula preselecciona BRUTO · `ef5d248` y `7d7516a` selector · `9ecd333` docs QA · `4ca4e0a` corrección DEF-F11-025 y 027 · `59d9b08` docs · `f63439c`, `31f2007` y `e01d81d` `tools/video-tutoriales` (fuera de la app generada) |
| `git diff --stat 84c712f..HEAD -- Wms.Infrastructure/Migrations` | Vacío: siguen las 11 migraciones; no se aplicó ninguna |
| `yarn test` (FE `4ca4e0a`) | 78 archivos, 345 pruebas, todas en verde |
| Login previo de `admin` y de las 5 cuentas `qa.*` | 200 |
| Ventana de despliegue | El usuario confirmó que no había operarios usando staging |

## 2. Respaldo previo

`POST administration/backups/run` (Admin) → 202, corrida `77114401…`, `Manual` · `Succeeded` (4.478.225 B), destino `local-staging` → `/opt/wms/backups/2026/10/wms_20261008_151727_77114401.dump`.

## 3. Despliegue (`Backend/wms-api`)

| Paso | Resultado |
|---|---|
| `scripts/deploy-staging.sh backend` | `dotnet publish` linux-x64, imagen `wms-api:staging` (`sha256:639c8a81…`), `Loaded image` en el servidor |
| `scripts/deploy-staging.sh up` | Solo se recreó `wms-api`; `postgres` (healthy) y `caddy` sin cambios. `pgdata` y `caddy_data` intactos |
| `scripts/deploy-staging.sh frontend` | `yarn generate` con `NUXT_PUBLIC_API_BASE=https://api.100-60-89-139.sslip.io/api/v1` y `rsync` a `/opt/wms/site` |
| `scripts/deploy-staging.sh smoke` | frontend 200 · SPA fallback 200 · login inválido 400 · CORS `access-control-allow-origin: https://app.100-60-89-139.sslip.io` |
| `logs wms-api` | `Now listening on: http://[::]:8080` · `Application started`. Solo avisos previos y benignos (`ParameterSchema` sin value comparer; `HTTP_PORTS` sobrescrito por `URLS`) y el `BadRequestException` del login inválido del `smoke`. Esta vez no apareció el aviso de `libgssapi_krb5.so.2` |

## 4. S1 — búsqueda (`qa.bascula`)

`GET /drivers?search={t}&isActive=true&orderByName=true&pageIndex=1&pageSize=20`, `curl -w '%{time_total}'` desde el Mac (incluye la latencia de internet y TLS), 3 corridas por término. «Esperado» = conteo con la regla D4 sobre `GET /drivers?all=true&isActive=true` (4.364 activos al empezar). «Pertinentes» = ítems que cumplen D4.

| # | Término (descripción genérica) | Ítems | pageSize | totalCount (esperado) | Pertinentes | Orden por nombre | t1 / t2 / t3 (s) |
|---|---|---|---|---|---|---|---|
| T1 | Apellido frecuente de 5 letras, en minúsculas | 20 | 20 | 76 (76) | 20/20 | Sí | 0,364 / 0,290 / 0,298 |
| T2 | Fragmento de 4 dígitos de una cédula | 12 | 20 | 12 (12) | 12/12 | Sí | 0,354 / 0,307 / 0,326 |
| T3 | Apellido con tilde escrito sin tilde | 20 | 20 | 35 (35) | 20/20 | Sí | 0,348 / 0,313 / 0,296 |
| T4 | «apellido nombre» (orden invertido) | 1 | 20 | 1 (1) | 1/1 | Sí | 0,294 / 0,306 / 0,308 |
| T5 | Prefijo de 3 letras del nombre más frecuente | 20 | 20 | 238 (238) | 20/20 | Sí | 0,286 / 0,325 / 0,301 |

Máximo 0,364 s: cumple el criterio de < 1 s en las 15 corridas.

## 5. S2 — permisos

| Caso | Usuario | Petición | Código |
|---|---|---|---|
| F9-API-022 | `qa.bodega` | `POST /drivers` con `{}` | 400 «Error de validación.» (no 403) |
| F9-API-022 | `qa.bodega` | `PATCH /drivers/{QA-SEL Uno}` con `{"phoneNumber":"3000000801"}` (mismo valor, después de S4) | 200 |
| F9-API-023 | `qa.bodega` | `POST /vehicles` con `{}` | 403 |
| F9-API-024 | `qa.facturacion` | `POST /drivers` con `{}` | 403 |
| F9-API-025 | sin token | `GET /drivers?search=x` | 401 |

## 6. S3 — ingresos (`qa.vigilancia`, API)

| Placa | Vehículo | Ingreso | Motivo | Observación |
|---|---|---|---|---|
| `QSL801` | `97f2f7d5…` (creado) | `0f4f8d03…` 15:20 | Solo Bascula | QA-SEL |
| `QSL802` | `2d8c728c…` (creado) | `b72386aa…` 15:20 | Solo bodega | QA-SEL |
| `QSL803` | `4141f80a…` (creado) | `37f444e3…` 15:20 | Solo Bascula | QA-SEL |

## 7. S4 a S6 — Báscula (`qa.bascula`, navegador integrado)

Peticiones capturadas con un registro de `fetch`/XHR instalado en la página solo para inspección (método, ruta y código).

| Caso | Resultado |
|---|---|
| País del vehículo | `QSL801` → Ecuador |
| 944ce53 | «Solo báscula» queda elegido por el motivo. El tipo del primer pesaje está en la etapa Peso, después del cobro; S6 prohíbe cobrar, así que **no se observó** |
| F3-CAM-004 | «qa-se» → `GET /drivers?search=qa-se…` → «QA-SEL Tres · CC 9000000803»; Enter lo elige; debajo «País: Ecuador (del vehículo)»; lápiz habilitado; sin `PATCH` |
| F3-CAM-013 | «0000 0803» → `search=0000+0803` → `QA-SEL Tres` (API: `totalCount` 1) |
| F3-CAM-014 | «tres qa-sel» → `QA-SEL Tres` (API: `totalCount` 1) |
| F3-CAM-015 | Sin texto: 20 opciones más la elegida y pie «Mostrando 20 de 4365. Escriba nombre o documento para afinar.» |
| F3-CAM-005 | «+» → CC `9000000801`, `Uno` / `QA-SEL` → `POST /drivers` 201 → «Conductor registrado — QA-SEL Uno quedó seleccionado.», modal cerrado, foco en el combobox. `GET /drivers?idNumber=9000000801` → 1 registro (creado 15:32:07), antes de guardar la ficha. Tras la búsqueda por documento, el foco quedó en `BODY` (DEF-F11-024) |
| F3-CAM-016 | «+» → CC `9000000801` → «Este conductor ya está registrado.», datos precargados, «Usar este conductor» → sin `PATCH` ni aviso, `QA-SEL Uno` seleccionado; sigue 1 registro |
| F3-CAM-017 | Lápiz → «Editar conductor», tipo deshabilitado, número `readonly`, foco en «Apellidos» → teléfono `3000000801` → `PATCH /drivers/7d5213c5…` 200 → «Conductor actualizado exitosamente»; el select sigue con `QA-SEL Uno` |
| F3-CAM-021 | Tab desde «Tipo de Vehículo» llega al combobox del conductor; una tecla real abre el filtro con esa letra; texto, Enter elige y no guarda la ficha (sin `POST`). Tab siguiente → «+» (OBS-SEL-01). «+» con Enter abre el modal con el foco en «Tipo de Documento»; Esc no lo cierra (DEF-F11-023) |
| S5 / F3-CAM-020 | Transportadora «QA-S6 Transportadora SAS», tipo Sencillo, cliente «QA-S6 Cliente Uno SAS», observación «QA-SEL» → `POST weighbridge/weighing-only/initiate` 201 → «Operación registrada», ficha «Por cobrar». `GET entry-logs/0f4f8d03…`: `driver` = `QA-SEL Uno` (CC `9000000801`). `QA-SEL Uno` conserva el `updatedAt` de las 15:33 (antes del guardado de las 15:35) y `QA-SEL Tres` sigue sin cambios |
| S6 | «Recuperar operaciones» → `QSL801` «Sin ciclo (abandonada)», única fila con «Descartar» → confirmación → `DELETE weighbridge/incomplete/efcf2b25…` 204 → «Operación descartada». Salida de `QSL801` (`qa.vigilancia`, API) 200. Sin factura: la más reciente de staging es de las 15:15, antes de empezar |

## 8. Re-test DEF-F11-025 (`qa.bascula`)

| Paso | Resultado |
|---|---|
| `POST /drivers` `QA-SEL Tres`, CC `9000000803`, `country: null` | 201, `e307d3b3…`, `country: null` |
| `QSL803`, país del vehículo Ecuador, «+» → `9000000803` | «Este conductor ya está registrado.»; el modal muestra Ecuador (heredado) |
| «Usar este conductor» | Sin `PATCH` ni aviso; seleccionado con «País: Ecuador (del vehículo)»; `GET /drivers/e307d3b3…` → `country: null`, `updatedAt: null` |
| Lápiz → teléfono `3000000803` → «Guardar cambios» | `PATCH /drivers/e307d3b3…` 200 → `country: null`, teléfono `3000000803` |
| Limpieza | «Soltar camión» sin guardar; ingreso sin operación ni conductor; salida de `QSL803` 200 |

## 9. S7 y S8 — Bodega (`qa.bodega`, navegador integrado)

| Caso | Resultado |
|---|---|
| Recepción Directa | `GET warehouse/pending-direct-reception` → `QSL802` y `QSE501` (S6). «Recibir» en `QSL802`; transportadora y país precargados de la sesión |
| F4-RSB-009 | «+» → CC `9000000802`, `Dos` / `QA-SEL` → `POST /drivers` **201** (sin 403) → «QA-SEL Dos quedó seleccionado.». Foco en `BODY` tras el documento (DEF-F11-024) |
| F4-RSB-010 | Lápiz → «Editar conductor», número `readonly` → teléfono `3000000802` → `PATCH /drivers/77c37cdb…` **200** |
| F4-RSB-011 | Conductor limpiado (lápiz deshabilitado), firma de prueba, «Completar Recepción Manual» → «Campos incompletos — Conductor requerido: selecciónelo o regístrelo con «+».». Sin `POST` de recepción. El resto del formulario se dejó vacío a propósito: la validación corta antes de cualquier envío |
| Cierre | Asistente cerrado sin guardar. Ingreso `QSL802`: sin operación ni depósito |
| S8 | Salida de `QSL802` (`qa.vigilancia`, API) 200 |

## 10. Re-tests y observaciones con Admin (navegador integrado)

| Caso | Resultado |
|---|---|
| DEF-F11-027 | Admin → Conductores, filtro «Nombre» = «QA-SEL» → `GET /drivers?pageIndex=1&pageSize=10&name=QA-SEL` 200 → 3 registros. Captura: `staging-admin-filtro-nombre-qa-sel.jpg` |
| DEF-F11-022 | Comercio Exterior › Reportes › Movimientos por Depósito → resaltado en su grupo. Un clic en Facturación › Movimientos por depósito (misma ruta) → la entrada tocada. Facturación › Clientes → `/admin/stakeholders?rol=CUSTOMER`, resaltado en Facturación. Carga directa de `/reports/general-inventory` → «Bodega › Inventario general». Una sola `active-route` en cada paso |
| 1db3448 | Servicio BASCULA → «Editar precio vigente» muestra «$ 16.806,72»; con `12345,67` → «$ 12.345,67» (`aria-valuenow` 12345.67). «Cancelar», sin guardar: precio vigente $16.806,72 |

## 11. S9 — humo

| Comprobación | Resultado |
|---|---|
| Login de `admin`, `qa.vigilancia`, `qa.bascula`, `qa.bodega`, `qa.comext` y `qa.facturacion` | 200 |
| BA0042 (`2024BA00002`, `qa.comext`) | Listado `Confirmed`, carta porte EC0004054, 398 Unidad, Nacionalizado; `foreign-trade/imports/{id}` 200, USD, 648 nacionalizadas. Igual que en el re-test de S6 |
| Cola de báscula | 10 camiones, ninguno `QSL`: los de ejemplo QA-S6, P1, P2, P3 y P6 (`GLS926`, `SRC396`, `SVO318`, `CAH514`) en `NotStarted`, y dos operaciones de operarios del día |
| Vigilancia → Salida (`entry-logs?hasDeparture=false`) | 12 en planta, ninguno `QSL` |
| P3 | `2024BA00005` `Confirmed`, Nacionalizado, 2.000 Unidad; OC `2026OC00004` (`PRAC-OC-0001`) `Pending`, 200 |
| P4 | `2024BA00006` `Confirmed`, SinNacionalizar, 1.350 Unidad |
| P5 | Facturas de $558.159,96 y $474.566,16 en `Draft`, sin N.º SIIGO, período 01/10 a 16/10/2026 |
| Facturas | 146 (Draft 133, Approved 2, Paid 11); ninguna creada desde las 15:16 |
| Conductores creados o editados desde las 15:17 | Solo `QA-SEL Uno`, `Dos` y `Tres`; ningún migrado |

## 12. Respaldo final

`POST administration/backups/run` → corrida `53e8fdc1…`, `Manual` · `Succeeded` (4.482.286 B) → `/opt/wms/backups/2026/10/wms_20261008_154700_53e8fdc1.dump`.
Servidor: disco 6,9 G de 77 G (9 %); `caddy` Up 39 h, `postgres` Up 45 h (healthy), `wms-api` Up 28 min.
