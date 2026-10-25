# Informe QA — Ronda de preproducción (regresión integral antes de la fase 13)

> **Plan:** `qa/plan-ronda-qa-preproduccion-2026-10-25.md` (R1–R10). **Registro de datos:** `qa/resultados/registro-datos-qa-preproduccion.md`.
> **Veredicto:** **GO con condiciones** para la fase 13 (§9): ningún BLOCKER, ensayo de migraciones sin errores, un CRITICAL (DEF-F11-030) y un MAJOR (DEF-F11-034) abiertos, y los pendientes de staging del §8.
> **Conteo:** 178 casos · 162 pasan · 3 fallan · 8 observaciones · 4 no ejecutados · 1 no aplica. Defectos nuevos: 1 CRITICAL, 1 MAJOR, 3 MINOR, 1 TRIVIAL (DEF-F11-029 a 034).

## 1. Entorno

| Campo | Valor |
| --- | --- |
| Fecha (hora Colombia) | 2026-10-25, desde las 10:46 |
| Ejecutor | Agente QA sin historial, solo; sin cambios de código |
| Commits | BE `develop` `57c94dd` · FE `develop` `cb2a4f7` · árboles limpios (`git status`) |
| Base | `wms_qa_preprod`, creada con `CREATE DATABASE wms_qa_preprod TEMPLATE wms_migracion;` a las 10:46 en `wms-postgres-db` (5433, `postgres:18.0`). `wms_migracion`, `wmsdb` y las bases de grabación no se tocaron (solo se leyó el historial de migraciones de `wms_migracion`) |
| Datos de la copia | 130 depósitos (128 `Confirmed`, 1 `Draft`, 1 `Cancelled`), 1.389 terceros, 1.640 productos, 4.365 conductores, 10.398 vehículos, 1.774 ciudades, 131 facturas, 128 períodos, 107 levantes, 1 orden y 1 guía; 6 usuarios (`admin` y `mig.*`); 0 convenios y 0 tarifas de montacargas |
| API | `dotnet run --project Wms.Api`, `http://localhost:5281`, Development, con variables de sesión: cadena a `wms_qa_preprod`, SMTP al sumidero local, `Notifications:AdminEmails` de prueba, `Frontend:BaseUrl = http://localhost:3000`, clave de verificación del QR generada para la ronda, `Backups:TempPath` y `Backups:PgDumpPath` locales (envoltorio de `pg_dump` dentro del contenedor), `Storage:Local:BasePath` en el scratchpad y `Bootstrap` con un usuario de arranque nuevo |
| Frontend | `yarn dev` en el puerto 3000 con `NUXT_PUBLIC_API_BASE=http://localhost:5281/api/v1` |
| Correo | `axllent/mailpit` (SMTP 1025, UI 8025). Nada salió del equipo |
| S3 | `adobe/s3mock` en el puerto 9100, bucket `wms-qa-pre` |
| TRM | API pública de la DIAN (`datos.gov.co`), solo lectura |
| Navegador | Integrado de la app; zona horaria del equipo America/Bogotá (UTC-5); celular emulado a 375 × 812 |
| Cuentas | La copia no trae un Admin utilizable para el ejecutor (`admin` con clave desconocida). Se creó `qa.pre.boot` con `Bootstrap:AdminPassword` (R8) y, con él, por `POST user`: `qa.pre.admin`, `qa.pre.comext`, `qa.pre.vigilancia`, `qa.pre.bascula`, `qa.pre.bodega`, `qa.pre.facturacion`, `qa.pre.multi1` (Facturación + CE) y `qa.pre.multi2` (Báscula + CE). Todas cambiaron la clave inicial (`mustChangePassword` → `false`). Las claves viven solo en el scratchpad del ejecutor |

## 2. Ensayo de las migraciones (R3)

- **Historial de `wms_migracion`:** 11 migraciones, hasta `20261007030137_RemoveSampleSeedData`.
- **Comando:** `dotnet ef database update --project Wms.Infrastructure --startup-project Wms.Api --no-build --connection "<cadena a wms_qa_preprod>"`, de 10:47:26 a 10:47:28.
- **Resultado:** `exit 0`, «Done.», sin errores. Seis migraciones aplicadas, en este orden:

| Migración | Resultado |
| --- | --- |
| `20261008230241_AddForkliftUseEntryLog` | Aplicada |
| `20261024144232_AddStakeholderExitBlock` | Aplicada |
| `20261024155558_FixAgreementActiveStakeholderIndex` | Aplicada |
| `20261024163412_AddWarehouseStorageLegacyYear` | Aplicada |
| `20261024170332_AddGuideCodeTypeParameter` | Aplicada |
| `20261025152149_RelaxServicePriceActiveIndex` | Aplicada |

- **Tiempo:** unos 2 s en total, incluido el arranque de la herramienta; 31 comandos SQL, el más lento de 7 ms.
- **Después:** `__EFMigrationsHistory` termina en `20261025152149_RelaxServicePriceActiveIndex`; `dotnet ef migrations has-pending-model-changes` → «No changes have been made to the model since the last migration.».
- **Aviso no bloqueante:** EF advierte (`10620`) que `FormulaType.ParameterSchema` no tiene `ValueComparer`. Es del modelo, no de la migración.
- **`GUIDE_CODE_TYPE`** quedó sembrado en `QR` por la migración; `INVENTORY_ADJUSTMENT_ADMIN_EMAIL` existe vacío.

## 3. Palancas de tiempo (R4)

Todas en `wms_qa_preprod`, con `psql` dentro del contenedor. Horas de Colombia.

| Hora | SQL | Para |
| --- | --- | --- |
| 11:27 | `update service_prices set valid_from = ((date '2026-10-25')::timestamp + interval '6 hours') at time zone 'America/Bogota' where id='87f23324-…'` (el precio de $18.000 programado para el 26/10; las 00:00 chocan con el índice `idx_service_price_one_active_per_start`, por eso las 06:00) | F1-SRV-021 |
| 11:28:19 | `update storage_billing_periods set period_start = period_start - (date '2026-11-25' - date '2026-10-21') * interval '1 day', period_end = (date '2026-10-21')::timestamp at time zone 'America/Bogota', limit_date = date '2026-10-24' where warehouse_storage_id = <2026BA00014 / 2026BA00021> and status='Open'` | F6-ALM-009, F6-ALM-017 |
| 11:28:19 | Lo mismo con fin `2026-10-23` y `limit_date` `2026-10-26` para `2026BA00022` y `2026BA00023` | F6-ALM-019 |
| 11:28:19 | `update inventory_movements … set created_at = timestamptz '2026-10-22 15:00:00-05'` (salida por cargue de `2026BA00014`, día S) y `'2026-10-23 10:00:00-05'` (de `2026BA00021`, día de gracia) | F6-ALM-009, F6-ALM-017 |
| 11:28:43 | `update storage_billing_periods set limit_date = date '2026-10-24'` para `2026BA00022` y `2026BA00023` (después del cargue total) | F6-ALM-019 |
| 11:28:43 | `update inventory_movements … set created_at = timestamptz '2026-10-24 10:00:00-05'` (salida de `2026BA00023`, día S) | F6-ALM-019 (variante «salió el día S») |
| 11:28:43 | `update invoices set due_date = now() - interval '2 days' where id = <QA-PRE-FE-MORA1>` | E2E-12, F5-OC-007 |
| 11:28:43 | `update storage_billing_periods set period_end = (date '2026-10-21')::timestamp at time zone 'America/Bogota', limit_date = date '2026-10-24' where id = <período abierto de 2022BA00001>` | B5 (renovación de un migrado) |

**Reinicios del API:**

| Hora | Motivo |
| --- | --- |
| 10:47 | Arranque inicial (renovó 92 períodos vencidos de los migrados) |
| 11:28:57 | Con `DianTrm__BaseUrl=http://127.0.0.1:9` (DIAN inaccesible): jobs de la palanca y E2E-14 |
| 11:30:47 | Con la DIAN disponible: E2E-14 (la TRM manual se conserva) y comprobación de que no hay renovaciones de más |
| 11:42:03 | Con credenciales ficticias de AWS para `s3mock` (FB-BAK-002/003) |
| 11:53:37 → 11:54 | API detenido y vuelto a arrancar (B7, «API caída») |

## 4. Resultados por bloque

### B0. Ensayo y humo (P0)

Cómo: `curl`/cliente HTTP con el token de cada cuenta, el navegador integrado y el log del API.

| ID | P | Estado | Tipo | Observación |
| --- | --- | --- | --- | --- |
| PRE-R3 | P0 | PASA | PER | Seis migraciones aplicadas sobre datos migrados en unos 2 s, sin errores; modelo sin cambios pendientes (§2) |
| F0-DIS-001 | P0 | PASA | FUN | `/billing` sin sesión → `/auth/login`; sin pantalla en blanco |
| F0-DIS-002 | P0 | PASA | API | `POST auth/login` inválido → 400 «Credenciales inválidas» |
| F0-DIS-003 | P0 | PASA | API | El login desde el frontend llega al API, sin error de CORS |
| F0-DIS-004 | P3 | PASA | API | Swagger UI en la raíz del API (301 → `index.html`) |
| F0-DIS-005 | P2 | NO EJECUTADO | UX | No se midió el tiempo de carga |
| F0-LOG-001 | P0 | PASA | FUN | `qa.pre.admin` → `/` (Trazabilidad) |
| F0-LOG-002 | P0 | PASA | FUN | Vigilancia → `/operations/entries`; Báscula → `/operations/weighbridge`; Bodega → `/warehouse`; CE → `/`; Facturación → `/billing`; multirol → `/` |
| F0-LOG-003 | P0 | PASA | ERR | «No se pudo completar la acción · Credenciales inválidas»; se queda en el login |
| F0-LOG-004 | P0 | PASA | PER | Recargar `/operations/weighbridge/history` conserva la sesión y la página |
| F0-LOG-005 | P0 | PASA | FUN | Botón de apagado → «¿Está seguro…?» → Aceptar → `/auth/login`; «Atrás» vuelve al login |
| F0-LOG-006 | P0 | PASA | ROL | Sin sesión, `/billing` → `/auth/login` |
| F0-LOG-007 | P1 | PASA | ROL | Vigilancia en `/billing` → `/access-denied` |
| F0-LOG-008 | P2 | PASA | FUN | Con sesión, `/auth/login` → ruta del rol |
| F0-NAV-001 | P0 | PASA | FUN | Menú Admin completo: Notificaciones, Ayuda, Dashboards, Administración, Vigilancia, Báscula, Bodega, Comercio Exterior, Facturación |
| F0-NAV-002 | P1 | PASA | ROL | Ver B1 |
| F0-NAV-003 | P0 | PASA | FUN | Las 68 rutas del menú de Admin cargan sin 4xx/5xx ni errores de consola (B1) |
| F0-NAV-004 | P3 | PASA | UX | `/no-existe` → «Página no encontrada» |
| F0-NAV-005 | P2 | NO EJECUTADO | UX | Clic en el logo con Báscula no probado |
| F0-API-001…007, 009 | P0 | PASA | API | `user/me`, modalidades (4), motivos (7), cola de báscula, depósitos (130), facturas y servicios (5) responden 200 |
| F0-API-002, 010, 011 | P1 | PASA | API | 6 roles; IVA 19 % y RETE_FUENTE 3 %; 10 unidades de medida y Contenedor/Remolque/Tanquero |
| F0-API-008 | P1 | PASA | API | 9 ubicaciones migradas (`Bodega 1…5`, `Bodega Baja`, `Cobertizo`, `Patio 1/2`); las 20 sembradas no aplican a datos migrados |
| F0-API-012 | P1 | PASA | INT | `POST /hubs/notifications/negotiate` → 200 |
| F0-ENV-001 | P0 | PASA | FUN | 6 usuarios migrados (`admin`, `mig.*`) más las cuentas `qa.pre.*` |
| F0-ENV-002 | P1 | OBSERVACIÓN | FUN | 1.053 clientes/importadores, 77 agencias, 266 transportadoras y **ningún exportador** migrado. Para exportación se creó `QA-PRE Exportador SAS` |
| F0-ENV-003 | P0 | PASA | FUN | Tarifas de `DEC-041` presentes: T1 (regla IMP 0,295 %, mínimo $50.000 con IVA), T2 (mínimo IMP $50.000 con IVA), T3 (báscula $16.806,72 + IVA) y T4 (guía $15.000). Faltaban las de montacargas (§3.7) |
| F0-ENV-004 | P1 | PASA | FUN | `INVENTORY_ADJUSTMENT_ADMIN_EMAIL` vacío en la copia; se configuró por API (§3.7) |
| F0-ENV-005 | P0 | PASA | FUN | Datos migrados del legacy, como se esperaba (R2) |
| F0-ENV-006 | P2 | PASA | FUN | Los 7 jobs arrancan sin excepciones. Al primer arranque `StoragePeriodAutoCloseJob` cerró y renovó **92 períodos vencidos** de depósitos migrados (92 facturas en Borrador, $63.258.314,46); ver B5 |
| F0-ENV-007 | P2 | PASA | FUN | Equipo en America/Bogotá; las horas de pantalla y de los PDF coinciden |

**Configuración agregada (§3.7), por API:** tarifas de montacargas de `DEC-041` (`PUT forklift-rates/{tipo}` con `qa.pre.facturacion`: Tractomula 220.000, DobleTroque 150.000, Sencillo 140.000, Turbo 110.000, GuacalEstiba 40.000); `INVENTORY_ADJUSTMENT_ADMIN_EMAIL` = `qa.pre.ajustes@local.test` (`PATCH administration/system-parameters/{id}` con `qa.pre.admin`); convenios QA en el registro de datos.

### B1. Pantallas por rol (P0)

Cómo: con cada cuenta se entró por la pantalla de login y se recorrieron con el enrutador de la aplicación **todas** las rutas de su menú (`F/app/components/layout/AppMenu.vue`) y una muestra de rutas ajenas, esperando 2,5–3 s por ruta y registrando cada respuesta HTTP, los errores de consola, los avisos emergentes y la redirección a «Acceso denegado».

| ID | P | Estado | Tipo | Observación |
| --- | --- | --- | --- | --- |
| PRE-B1-ADM | P0 | PASA | ROL | `qa.pre.admin`: 68 rutas (Administración 25, Vigilancia 3, Báscula 4, Bodega 10, CE 22, Facturación 7) sin 4xx/5xx ni errores de consola. Listados con los datos migrados: historial de Vigilancia 6, inventario de Bodega paginado (20 por página), levantes paginados, «Mercancía en abandono» 50 por página, depósitos 130 (13 páginas), «Depósitos pendientes» paginado (25), configuraciones de facturación (10) |
| PRE-B1-VIG | P0 | PASA | ROL | Menú: Notificaciones, Ayuda, Vigilancia. Sus 5 rutas cargan; `/` lleva a `/operations/entries`; `/warehouse`, `/warehouse/inventory`, `/billing`, `/foreign-trade/deposits`, `/operations/weighbridge`, `/admin/users` y `/reports/general-inventory` → «Acceso denegado» |
| PRE-B1-BAS | P0 | PASA | ROL | Menú: Notificaciones, Ayuda, Báscula. Sus 6 rutas cargan; `/` → `/operations/weighbridge`; Vigilancia, Bodega, Facturación, CE, `/admin/drivers` e inventario general → «Acceso denegado» |
| PRE-B1-BOD | P0 | PASA | ROL | Menú: Notificaciones, Ayuda, Bodega. Sus 12 rutas cargan (incluido inventario general); `/reports/warehouse-movements` también; Vigilancia, Báscula, Facturación, CE y `/admin/products` → «Acceso denegado» |
| PRE-B1-CE | P0 | PASA | ROL | Menú: Notificaciones, Ayuda, Dashboards, Comercio Exterior. Sus 24 rutas cargan (terceros, reportes); Facturación, Bodega, Báscula, Vigilancia, `/admin/users` y `/admin/drivers` → «Acceso denegado». Durante el recorrido apareció el aviso técnico de cada pesaje: **DEF-F11-029** |
| PRE-B1-FAC | P0 | PASA | ROL | Menú: Notificaciones, Ayuda, Facturación. Sus 12 rutas cargan (incluidos «Clientes», inventario general y movimientos); CE, Bodega, Báscula, `/admin/services`, `/admin/forklift-rates` y `/admin/users` → «Acceso denegado» |
| PRE-B1-M1 | P0 | PASA | ROL | `qa.pre.multi1` (Facturación + CE): menú unión (Dashboards, CE, Facturación); entra a lo de los dos roles y a nada más |
| PRE-B1-M2 | P0 | PASA | ROL | `qa.pre.multi2` (Báscula + CE): menú unión (Dashboards, Báscula, CE); entra a lo de los dos roles y a nada más |
| PRE-B1-OBS1 | P2 | OBSERVACIÓN | ROL | Facturación tiene `BillingAccess` en el API para tarifas base y de montacargas, pero las páginas `/admin/services` y `/admin/forklift-rates` son solo de Admin (`requiredRoles: ["Admin"]`), igual que la matriz de la fase 9 (§2.1). No es un cambio de esta versión |

### B2. Flujos de punta a punta (P0/P1)

Cómo: por API con la cuenta del rol de cada paso (`qa.pre.vigilancia` → `qa.pre.bascula` → `qa.pre.bodega` → `qa.pre.comext` → `qa.pre.facturacion`), datos `QA-PRE` sobre productos, ciudades, ubicaciones y cuadrillas migrados; verificación con SQL de solo lectura y `pdftotext` de los PDF. Detalle de los datos en el registro.

| ID | P | Estado | Tipo | Puntos de control |
| --- | --- | --- | --- | --- |
| E2E-01 | P0 | PASA | E2E | QPA001 en cola «Sin iniciar» → `2026BA00002` Borrador, stock 100 (`DeclaredEntry`), báscula Pagada $20.000, tiquete `2026T00003`, aviso «Nuevo depósito de importación» a CE → tara sin llegada a Bodega: 409 «…Bodega debe registrar la llegada antes del segundo pesaje»; con llegada: neto 20.000, ciclo `Complete` → recepción 100 sin diferencia, stock 100 → confirmar (faltaban fecha, agencia, moneda y valor) y cerrar ingreso; TRM DIAN 3.158,43; factura Borrador $279.521,06 + IVA = $332.630,06 (30.000 × TRM × 0,295 %); etiqueta «MERCANCIA SIN NACIONALIZAR» → numerar `QA-PRE-FE-0001` y aprobar → levante 100; etiqueta «MERCANCIA NACIONALIZADA» → salida de QPA001, ingreso de QPA002 → `2026OC00002` Pendiente, reservado 100, disponible 0 → salida en báscula con la OC y cobro → cargue: OC Cargada, stock 0, depósito `Closed`, período cerrado, aviso «Guía de salida requerida» → guía `2026S00002` (100/100/100/0), factura de guía $15.000 Pagada → repesaje 34.000: OC Despachada, servicio `Completed` → salida de QPA002 → kárdex IN 100 / OUT 100; facturación por CPI con `QA-PRE-FE-0001` |
| E2E-02 | P0 | PASA | E2E | Dos camiones al mismo documento: un depósito `2026BA00003`, stock 100 → recepción de 58: aviso «Diferencia en recepción… diferencia -2. El stock no cambió…»; stock 100 → CE-7 a 98 (kárdex `Adjustment`, correo «Corrección de Cantidad Recibida» al parámetro), confirmar y cerrar ingreso (2 camiones); factura con «98 UNIDAD» → levante 50, OC, cargue y guía `2026S00003`: 98/98/50/48 → levante 48, segunda OC y guía `2026S00004`: 98/48/48/0; la primera guía no cambia; depósito `Closed`. La etiqueta reimpresa muestra saldo 48 y «Ampara 50,0000»: **DEF-F11-031** (TRIVIAL) |
| E2E-03 | P0 | PASA | E2E | `2026BA00004` confirmado y aprobado (`QA-PRE-FE-0003`) → QPA008 al mismo documento: se asocia, stock 120 → CE: «Camión adicional en depósito confirmado… reimprima la etiqueta»; Facturación: «La factura QA-PRE-FE-0003… se actualizó por camión adicional QPA008. Total anterior $ 110.877, total nuevo $ 110.877» (la tarifa es por valor) y conserva el número → cerrar ingreso; tercer camión: 409 «…fue cerrado por QA PRE comext el 25/10/2026 11:11…» |
| E2E-04 | P0 | PASA | E2E | Descargue de exportación → `2026EXP00001`; confirmar exige fecha, moneda y valor (no importador ni agencia); etiqueta «MERCANCIA PARA EXPORTACION»; factura por el convenio QA-PRE `FIXED` $150.000 + IVA → OC `2026OC00005`, salida en báscula, cargue → **guía de exportación automática `2026S00005` sin cobro** (200/200/200/0) → repesaje; depósito `Closed`, período cerrado |
| E2E-05 | P1 | PASA | E2E | Contenedor `QPCU0001` registrado en báscula (`CargoUnits`) → `2026EXP00002`; Bodega recibe la unidad completa sin contar (`receivedCargoUnitIds`) → CE confirma → OC `2026OC00016` por la unidad → cargue completo → guía automática `2026S00010`; unidad `Dispatched`, depósito `Closed`. `PER_CARGO_UNIT` no se verificó (el convenio del exportador es `FIXED`) |
| E2E-06 | P1 | PASA | E2E | INSP con un solo pesaje (ciclo `Complete` al primer peso) → confirmar exige el manifiesto del camión, no importador ni agencia → etiqueta «INSPECCION ADUANERA» → factura al mínimo de INSP ($0) con advertencia y aviso «Almacenamiento facturado con valor mínimo» (DEC-020) |
| E2E-07 | P0 | PASA | E2E | Solo báscula con cliente y cobro inmediato: ciclo `Complete` con un pesaje, sin depósito → con dos pesajes y «por facturar»: Borrador → `QA-PRE-FE-0007` → aprobada → pago → `Paid` → sin cliente (DEC-050): cobro al conductor como destinatario no registrado; tiquete «Cliente: QA-PRE Conductor 14» y «Documento interno de control de pesaje. No es una factura…» → consumidor final por facturar: tiquete «Cliente: Consumidor Final» |
| E2E-08 | P1 | PASA | E2E | «Solo bodega» no aparece en la cola de báscula → recepción directa crea `2026BA00008` Borrador, stock 12, un solo ingreso abierto → confirmar (exige manifiesto) → factura al mínimo $50.000 (T2) |
| E2E-09 | P1 | PASA | E2E | Montacargas Tractomula iniciado antes de que CE confirme; al finalizar con «Agregar IVA»: $220.000 + $41.800 = $261.800 `Paid` a nombre del cliente del depósito |
| E2E-10 | P1 | PASA | E2E | OC `2026OC00007` con depósitos de C1 y C2 → báscula → cargue parcial (50 de 60) → guía `2026S00007` multicliente: una factura de guía por cliente ($15.000 c/u), firmante forzado al conductor; saldos 120/120/50/70 y 40/40/40/0; ZIP con una guía por depósito; QR en las dos copias |
| E2E-11 | P0 | FALLA | E2E | (1) descartar en «Recuperar»: `2026BA00005` `Cancelled`, stock fuera, el camión vuelve a «Sin iniciar» y se registra de nuevo — PASA. (2) anular pesaje completo: ciclo `Canceled`, `2026BA00006` `Cancelled`, stock 0, la factura de báscula sigue `Paid` y se lista para revisión — PASA. (3) devolver a Borrador, corregir y reconfirmar: sin factura duplicada, pero **corregir solo el valor de la mercancía no recalcula la factura** — FALLA, **DEF-F11-030**; corregir una cantidad sí recalcula. (4) guía `2026S00006` anulada con su factura pagada «para revisión»; revertir antes de anular: 409 «Anule primero la guía…»; después: stock 45 devuelto, depósito `Confirmed` y período `Open` — PASA. (5) anular y refacturar: nueva Borrador enlazada y período re-enlazado — PASA. (6) anular el depósito: stock fuera, período cerrado, factura anulada, avisos a Bodega y Facturación — PASA |
| E2E-12 | P0 | PASA | E2E | Palanca: `due_date` de `QA-PRE-FE-MORA1` −2 días y reinicio → `OverdueDetectionJob`: «1 facturas vencidas, 1 stakeholders actualizados» → `Blocked` en la primera corrida → cobro de báscula, cierre de montacargas, recepción sin báscula, OC y guía: 400 «El cliente 'QA-PRE Cliente Mora SAS' está bloqueado por deuda pendiente…» → pago → `Active` al instante (sin esperar el job) → las cinco operaciones responden 200 |
| E2E-13 | P1 | PASA | E2E | `2026BA00024` (PER_UOM 100): cierre manual → período nuevo desde el 26/11 por 100 → cargue total: período cerrado conservando lo cobrado, depósito `Closed` → tras dos reinicios, ninguna renovación |
| E2E-14 | P1 | PASA | E2E | Con la DIAN inaccesible (palanca): `2026BA00028` USD → factura al mínimo $50.000, aviso «Almacenamiento con TRM pendiente»; numerar y aprobar: 400 «Registre la TRM… antes…»; TRM manual con motivo corto: 400; con 3.950: recalcula a $49.375 + IVA = $58.756,25, numera y aprueba → reinicio con la DIAN disponible: la TRM sigue `Manual` |
| E2E-15 | P1 | PASA | E2E | Ingreso de Vigilancia corregido a ayer 18:00 → pesajes con fecha de ayer (una fecha futura: 400) → `2026BA00030` con fecha de ingreso, TRM y período desde el 24/10; la etiqueta dice «Fecha Ingreso: 2026-10-24 18:00:00» |
| E2E-16 | P2 | PASA | E2E | Con la operación de báscula registrada: cambiar el motivo → 409 «…Descártela primero en Báscula > Operaciones incompletas.»; corregir la placa → 200 y la entrada del depósito y la cola muestran la nueva |
| E2E-17 | P2 | PASA | E2E | QPD005 entra con `2026BA00032`; CE asocia el tiquete de ingreso a la OC `2026OC00017` (`exit-with-entry-ticket`) → cargue → guía `2026S00011` → OC Despachada sin segundo pesaje |
| E2E-18 | P2 | NO APLICA | E2E | Un solo operario de báscula en la operación (plan maestro §10); el doble envío del mismo usuario va en B7 |
| E2E-19 | P1 | PASA | E2E | Del día: tiquetes `2026T00001…00043`, `2026BA00001…00032`, `2026EXP00001…00002`, `2026INSP00001…00002`, `2026OC00001…00017`, `2026S00001…00011`: sin saltos ni repetidos; los depósitos descartados o anulados conservan su número |
| E2E-20 | P1 | PASA | E2E | Reporte diario de báscula $800.000 = suma SQL de las facturas BASCULA del día; cartera del dashboard $160.357.209,55 = pendiente de Borradores + Aprobadas; facturación anual de almacenamiento (4, $514.163) = numeradas del mes sin las de báscula. El inventario general va en B5 |

**Casos de B2 adicionales del plan (§4):**

| ID | P | Estado | Tipo | Observación |
| --- | --- | --- | --- | --- |
| F3-MUL-005 | P1 | PASA | RN | QPA025 con `2026BA00011` y `2026BA00012`: el adicional se cobra en $0 («AmountReceived debe ser 0»); un solo pesaje de tara para los dos tras las dos llegadas; neto 18.000 repartido 12.000 / 6.000 por peso de manifiesto; tiquete «Pesaje compartido por 2 depósitos · neto del camión 18.000 kg» |
| F3-SBA-001/002 | P0/P1 | PASA | RN | Ver E2E-07 (sin cliente: destinatario no registrado y consumidor final) |
| F5-OC-023 | P0 | PASA | RN | `2026OC00008` con guía `2026S00008` vigente: cancelar (CE y Bodega) y modificar → 409 «Anule primero la guía 2026S00008 de la orden 2026OC00008.» |
| F5-GUI-018 | P1 | PASA | RN | Guía por 10 y cargue de 8: aviso «Guía con cantidades distintas a lo cargado…», `differsFromLoad` con la diferencia y mensaje del cargue |
| F5-GUI-020…022 | P0 | PASA | SEG | QR de `2026S00007` decodificado con CoreImage a 300 dpi → `http://localhost:3000/verificar/guia/{token}`; la API pública responde sin sesión «Vigente», depósitos, destino, productos y placa `QPA•••`; la anulada `2026S00006` → «Anulada» con fecha; token alterado, basura o de 43 caracteres → 404 «La guía no existe o el código no es válido.» |
| PRE-B2-SAL-01 | P0 | FALLA | RN | Salida de importación sin guía (§10, CHG-33): con la báscula de salida iniciada, cargado y sin guía, Vigilancia responde 409 («…pesaje de báscula sin terminar…»); pero si Bodega carga la orden de un camión que **no pasó por báscula**, Vigilancia registra la salida sin guía (200). **DEF-F11-034** (MAJOR). Detectado al cerrar los camiones de la ronda: cinco órdenes de prueba cargadas sin báscula salieron igual |
| F1-TER-019 | P1 | PASA | RN | `QA-PRE Cliente Sin Salidas SAS`: Vigilancia, Báscula y Bodega → 403; motivo corto → 400; bloqueo por CE (fecha, autor, motivo); doble bloqueo → 400; OC, cargue y guía → 400 «…tiene las salidas bloqueadas: …»; filtro `exitsBlocked`; desbloqueo por Facturación; la guía sale después; dos filas de auditoría con el motivo |

### B3. Casos nuevos del plan P1 (P0/P1)

Cómo: por API con la cuenta del rol, SQL de solo lectura, `pdftotext`, el detector de QR de macOS (CoreImage) y el navegador para las pantallas citadas. Varios casos se cumplieron dentro de los flujos de B2; la columna lo dice.

| ID | P | Estado | Tipo | Observación |
| --- | --- | --- | --- | --- |
| F1-TER-019 | P1 | PASA | RN | Ver B2 (bloqueo de salidas) |
| F1-CNV-013 | P1 | PASA | RN | `QA-PRE-CONV-C1-B` programado para hoy: antes del job el resolutor ya cobra su 0,22 % (`2026BA00027`: $69.485,46); al reiniciar, `AgreementActivationJob` «1 activados»: B `Active`, A `Archived`; aviso «Convenio programado activado… Las facturas existentes no se recalcularon.» |
| F1-CNV-014 | P2 | PASA | VAL | Programado sin fecha → 400 |
| F1-CNV-009 | P2 | PASA | VAL | Fecha pasada → 400; la de hoy se acepta |
| F1-SRV-021 | P1 | PASA | RN | Precio de guía $18.000 desde mañana: 201, `isScheduled`, la pantalla lo marca «Programado» (azul) con la ayuda «Una fecha futura programa el precio…»; la guía de hoy cobra $15.000; un precio de hoy ($16.000) deja inactivo al programado (D46); con la palanca de vigencia, la guía cobra $18.000; se restauró T4 ($15.000) |
| F3-COR-001 | P0 | PASA | RN | Camión con dos depósitos en modo intermedio: corregir el bruto (30.000 → 31.000) cambia solo la primera entrada (7.000 → 8.000) |
| F3-COR-003 | P1 | PASA | RN | Sin `weighingId` corrige la secuencia 1 (tara 7.000 → 7.500) y el neto pasa de 11.000 a 10.500 |
| F3-COR-006 | P2 | PASA | RN | Ciclo de 3 pesajes: corregir la tara cambia solo la última entrada |
| F3-COR-010 | P0 | PASA | RN | Tara por `weighingId`: solo la segunda entrada; intermedio: cambian las dos; pesaje de otro ciclo → 404 «El pesaje no existe en este ciclo.»; secuencia 0 → 400 «Use la corrección del primer pesaje.» |
| F3-COR-011 | P1 | PASA | RN | Pesaje compartido de QPA025: tara 12.000 → 13.000, neto 17.000 repartido 11.333,33 / 5.666,67; el tiquete reimpreso dice «neto del camión 17.000 kg» |
| F3-MUL-001…004 | P1 | PASA | RN | QPD006: depósito adicional `2026BA00034` en el mismo ciclo, de otro cliente, cobrado en $0; tara antes de la llegada a Bodega → 409; modo intermedio: netos 7.000 y 13.000 |
| F3-MUL-005 | P1 | PASA | RN | Ver B2 |
| F3-SBA-001/002 | P0/P1 | PASA | RN | Ver B2 (E2E-07) |
| F3-TIQ-002 | P0 | PASA | UI | Tiquetes con cliente, destinatario no registrado o «Consumidor Final» y el pie «Documento interno de control de pesaje. No es una factura de venta.», sin «DIAN» |
| F5-OC-005 | P0 | PASA | RN | 5 unidades con 0 nacionalizadas disponibles → 400 «…supera lo nacionalizado disponible (0). Registre el levante antes de despachar.» |
| F5-OC-014 | P1 | PASA | FUN | Ver E2E-10 |
| F5-OC-015 | P1 | PASA | FUN | Sin guía, 30 → 20 con motivo; la reserva baja a 20 |
| F5-OC-016 | P0 | PASA | RN | Cancelar una orden `Pending` sin guía libera la reserva (0) |
| F5-OC-017 | P0 | PASA | RN | Ver E2E-11 paso 4 (revertir la salida del depósito agotado: stock devuelto, `Confirmed`, período `Open`) |
| F5-OC-022 | P0 | PASA | RN | Dos `POST` simultáneos por 60 con 100 disponibles: uno 201 (`2026OC00019`) y otro 400 «…Disponible: 40,00, Solicitado: 60»; reserva 60 |
| F5-OC-023 | P0 | PASA | RN | Ver B2 |
| F5-GUI-005 | P1 | PASA | RN | Segunda guía de la misma orden → 409 «Ya existe una guía de salida para esta orden de cargue.» |
| F5-GUI-007 | P2 | PASA | FUN | Guía `2026S00008` emitida con la orden `Pending` |
| F5-GUI-018 | P1 | PASA | RN | Ver B2 |
| F5-GUI-019 | P1 | PASA | RN | Dueño con salidas bloqueadas o en mora → 400 (B2 y E2E-12) |
| F5-GUI-020 | P0 | OBSERVACIÓN | SEG | QR decodificado del PDF a 300 dpi y página pública en celular correctos (B2, B7). **Pendiente (fase 13):** imprimir y escanear con Android e iPhone |
| F5-GUI-021/022 | P0 | PASA | SEG | Ver B2 |
| F5-GUI-023 | P1 | PASA | RN | `XYZ` → 400 «El parámetro GUIDE_CODE_TYPE solo admite QR o BARCODE.»; con `BARCODE` la guía trae código de barras (imagen 382 × 60) y sin la leyenda; con `QR`, el QR (450 × 450) y «Escanee para verificar…»; dos filas de auditoría |
| F5-REL-001 | P2 | PASA | FUN | Consulta de levantes: 122, paginada, con sus columnas |
| F6-ALM-001 | P0 | PASA | RN | Al confirmar: período desde el día de ingreso y factura en Borrador (todos los flujos) |
| F6-ALM-008 | P0 | PASA | RN | Cierre manual de `2026BA00024`: cierra 25/10 → 25/11 y abre desde el 26/11 (fin + 1) |
| F6-ALM-014 | P1 | PASA | RN | Convenio de CS con complementario PAPELERIA sin precio: confirma; línea «Papelería… (valor mínimo)» en $0 con origen `MinimumValue`; aviso «Almacenamiento facturado con valor mínimo» |
| F6-ALM-018 | P0 | PASA | RN | `2026BA00003` (`Closed`, factura Borrador sin N.º): aparece con y sin el interruptor como «Por numerar» sin período abierto; al numerar sale; al anular vuelve como «Por refacturar»; los anulados (`2026BA00006`, `2026BA00007`) no aparecen |
| F6-ALM-019 | P0 | PASA | RN | Palanca: `2026BA00022` agotado en la gracia (fin = 23/10, cargue el 25/10): queda `Closed` con el período abierto, en «Depósitos pendientes» con período abierto, log «agotado en la gracia: queda para la renovación (DEC-055)»; el job abre el período del 24/10 por 10, factura en Borrador, aviso «Almacenamiento renovado» y lo cierra por agotamiento. `2026BA00023` (salida fechada el día S): no abre período y el viejo queda cerrado |
| F6-REF-005/006 | P2 | PASA | FUN | Ver F6-ALM-018 |
| F6-TAR-003 | P0 | PASA | RN | Báscula sin convenio: $16.806,72 + IVA = $20.000 (T3) |
| F7-REP-001 | P1 | PASA | RN | Diario de ingresos del día: IMP por defecto, 22 bloques (exactamente los depósitos `Confirmed`/`Closed` del día), 24 vehículos |
| F7-REP-002 | P2 | PASA | VAL | Sin fechas, desde > hasta y modalidad `XX` → 400 |
| F7-REP-012 | P0 | PASA | RN | Kárdex con fecha de ingreso, agencia, manifiesto DIAN y TRM; PDF 200; depósito inexistente → 404 |
| F7-REP-020 | P3 | PASA | FUN | Rango sin datos con INSP: 200 vacío |
| F7-REP-023 | P1 | PASA | RN | `2026BA00030` con ingreso corregido al 24/10: kárdex, listado de importaciones y diario del 24/10 traen la fecha nueva |
| F7-REP-024 | P1 | PASA | RN | En pantalla (fechas con el calendario), PDF y Excel: bloque por depósito con agencia, importador, manifiesto DIAN, camiones y subtotales; «Total vehículos: 24» y las firmas «Jefe de Bodega», «Recibí conforme DIAN», «Firma Funcionario» |
| F9-API-005 | P0 | PASA | ROL | `POST foreign-trade/loading-orders` con Facturación y Báscula → 403 (sonda) |
| F9-API-026 | P0 | PASA | ROL | `exit-block`: Vigilancia, Báscula y Bodega → 403; CE, Facturación y Admin → 200 |
| F9-API-027 | P1 | PASA | API | `PATCH entry-logs/{id}` → 405; `POST warehouse/loading-orders` → 404; `GET billing/storage-invoice-draft` → 404; `POST billing/invoices` → 405 |
| F9-API-028 | P0 | PASA | SEG | Sin sesión: datos mínimos, placa `QPA•••`, sin conductor, destinatario, cliente ni documentos; 404 idéntico para códigos alterados; el limitador responde 429 «Demasiadas consultas de verificación. Intente de nuevo en un minuto.» desde la consulta 31 del minuto |
| F9-API-029 | P1 | PASA | ROL | `GUIDE_CODE_TYPE`: CE, Facturación y Báscula → 403; Admin sí |
| FA-MIG-001 | P1 | PASA | API | `dryRun` de clientes y depósitos: resultado por fila y nada persistido |
| FA-MIG-003 | P1 | PASA | API | Carga real de 2 clientes, 1 producto y 6 depósitos válidos (una fila con error no detiene las demás) |
| FA-MIG-004 | P1 | PASA | API | Recargar clientes: sin duplicados; recargar depósitos: «el depósito N (año) ya fue migrado» en cada fila |
| FA-MIG-007 | P1 | PASA | API | Conciliación: con el CSV original 4 `Ok`, 2 diferencias (los levantes cargados después) y 1 sin migrar (la fila con error); con los nacionalizados al día, 2 `Ok` |
| FA-MIG-011 | P1 | PASA | API | `990001` en 2023 y 2025 → `2023BA00021` y `2025BA00001` con su `legacy_year`; levantes sin `anio_deposito` → «el depósito 990001 existe en varios años; exporte la columna anio_deposito.»; con la columna, cada levante en su depósito |
| FA-MIG-012 | P1 | PASA | API | `prorroga` = 1 en IMP: prórroga registrada, plazo de 60 días en «Abandono y prórrogas» y una segunda → 409; en EXP: advertencia «la prórroga solo aplica a importación; se ignora…»; 0 y vacía: sin prórroga; 2 → «La prórroga (prorroga) «2» debe ser 1 o 0.» |
| FB-BAK-004 | P3 | PASA | FUN | Sin destinos activos: la corrida queda `Failed` «No hay destinos de respaldo activos.» y sale el correo de fallo; CE → 403 |
| FB-BAK-007 | P1 | OBSERVACIÓN | INT | Corrida parcial (S3 sin bucket) y sin destinos: el correo «[WMS] Falló el respaldo del 25/10/2026» llegó a los Admin activos y a `Notifications:AdminEmails`, una vez por corrida. **Pendiente (fase 13):** el bucket externo real y el fallo provocado en staging |

FA-MIG-013 queda fuera de la ronda: se ejecuta en el ensayo del corte real (plan §4, B4).

### B4. Pendientes del informe P1 (P0/P1)

Los 31 casos `NO EJECUTADO` del informe del 2026-10-24. FA-MIG-013 sigue para el corte real.

| ID | P | Estado | Tipo | Observación |
| --- | --- | --- | --- | --- |
| F6-ALM-009 | P0 | PASA | RN | Palanca: `2026BA00014` (PER_UOM $1.000, 50) con fin 21/10 y salida de 20 el día S (22/10): el job abre el período del 22/10 al 22/11 por **30** (la salida del día S no se cobra) |
| F6-ALM-017 | P0 | PASA | RN | Palanca: `2026BA00021` (40) con salida de 15 en la gracia (23/10): el período renovado cobra **40** (stock 25 + 15 de la gracia) |
| F6-REC-001 | P0 | PASA | RN | E2E-03: camión tardío; la factura aprobada `QA-PRE-FE-0003` dice «120 UNIDAD», conserva el período y el número |
| F6-REC-002 | P0 | PASA | RN | CE-7 30 → 28 sobre `2026BA00018` (PER_UOM): $35.700 → $33.320 |
| F6-REC-003 | P1 | PASA | RN | Factura Borrador de `2026BA00007` recalculada al editar un producto (110.876,69 → 221.753,37), sin aviso a Facturación |
| F6-REC-004 | P0 | PASA | RN | `QA-PRE-FE-0106` aprobada con N.º: misma factura, conserva número y aprobación; aviso «Total anterior $ 35.700, total nuevo $ 33.320» |
| F6-REC-005 | P1 | PASA | RN | Pagada en parte ($20.000): a $33.320 queda `PartiallyPaid`; CE-7 a 10 → $11.900 < pagado → `Paid` y el aviso «Saldo a favor del cliente: $ 8.100» |
| F6-REC-006 | P1 | PASA | RN | Factura anulada de `2026BA00019`: el CE-7 no la toca; aviso «Cambio de depósito sin facturar» |
| F6-REC-007 | P1 | PASA | INT | `2026BA00020` con dos camiones: anular el pesaje de QPB009 → 35.700 → 23.800; corregir el manifiesto y la fecha de ingreso → recalcula (log «período recalculado por …»); la fecha antes del ingreso de Vigilancia o futura → 400 |
| F6-TAR-001 | P0 | PASA | RN | Convenio de C2 `PERCENTAGE_OF_VALUE` 0,25 %: `2026BA00013` USD 10.000 × 3.158,43 × 0,25 % = $78.960,75, origen `Agreement` |
| F6-TAR-002 | P0 | PASA | RN | Tarifa base nivel 2 (T1 `PERCENTAGE_OF_VALUE` 0,295 %, origen `ServiceRule`) en los depósitos de C1 sin convenio (E2E-01). La copia no tiene una regla base `PER_UOM`; no se creó para no tocar la configuración global |
| F6-TAR-004 | P0 | PASA | RN | E2E-06: INSP sin regla → línea «valor mínimo» $0 con advertencia y aviso |
| F6-TAR-005 | P1 | PASA | RN | Tarifa sugerida de montacargas de C2: $100.000 (convenio); con el servicio del convenio desactivado, $220.000 (base); reactivado, $100.000 |
| F6-TAR-006 | P1 | PASA | RN | Regla específica P3 + IMP (PER_UOM $1.000) gana a la genérica: `2026BA00014` 50 × $1.000 |
| F6-TAR-007 | P1 | PASA | RN | Convenio del exportador solo EXP; un depósito IMP del mismo cliente usa la tarifa base (`ServiceRule`), no la de EXP |
| F6-TAR-008 | P2 | PASA | VAL | Porcentaje 150 → 400 «'percentage' debe ser un decimal en el rango 0–100.» |
| F6-TAR-009 | P2 | PASA | RN | Regla perecedera de P1 ($2.000): `2026BA00015` perecedero 30 × $2.000; el P1 no perecedero usa la genérica |
| F6-TAR-010 | P3 | NO EJECUTADO | RN | Desempate por fecha no probado (opcional) |
| F5-OC-007 | P0 | PASA | RN | E2E-12: crear la orden con el cliente en mora → 400 «…bloqueado por deuda pendiente…» |
| F5-OC-013 | P1 | PASA | FUN | `2026OC00018` con dos depósitos de C2: reservas en ambos (30 y 10) |
| F5-OC-018 | P1 | PASA | RN | E2E-11: revertir con guía vigente → 409 «Anule primero la guía 2026S00006 de la orden 2026OC00006.» |
| F3-SBA-003 | P1 | PASA | FUN | Solo báscula con primer pesaje Tara: tara 5.000, bruto 12.500; el historial trae neto 7.500 (el tiquete muestra tara y bruto, sin neto) |
| F7-REP-003 | P1 | PASA | RN | Diario de salidas del día: 6 filas (las órdenes despachadas), filtro por cliente (1) y mercancía «LLAN» (1); 1 carácter → 400; PDF |
| F7-REP-018 | P1 | PASA | FUN | «Mercancía en abandono»: la pantalla pagina 50 y el Excel trae las 74 filas (77 con título y encabezados) |
| F7-REP-019 | P2 | PASA | UI | Excel: encabezados en español, fecha como número de Excel en hora de Colombia (11:07), cantidades numéricas |
| F7-REP-025 | P2 | PASA | FUN | Excel del diario de salidas con las columnas de la pantalla, «Totales (6 filas)» = 710 y el manifiesto DIAN del depósito |
| F11-REG-021 | P0 | PASA | REG | F6-ALM-001 y F6-TAR-001…004 |
| FB-BAK-001 | P2 | PASA | FUN | Destinos Local y S3 creados y editados; nombre duplicado → 409 |
| FB-BAK-002 | P2 | PASA | FUN | Prueba de conexión: Local escribe y borra; S3 sin credenciales, sin bucket y luego con éxito en `s3://wms-qa-pre/qa-pre/_prueba/…`; los errores son claros (el de credenciales trae el texto del SDK en inglés) |
| FB-BAK-003 | P2 | PASA | FUN | `backups/run` → 202; uno simultáneo → 409 «Ya hay un respaldo en curso.»; `backups/runs` lista la corrida `Succeeded` con `.dump` y `.tar.gz` en el destino local y en `s3mock` |
| FA-MIG-013 | P1 | NO EJECUTADO | — | Para el ensayo del corte real (plan §4) |

### B5. Datos migrados (P0/P1)

| ID | P | Estado | Tipo | Observación |
| --- | --- | --- | --- | --- |
| PRE-B5-01 | P0 | PASA | PER | Inventario general: 164 filas y 137.286 unidades, igual a la suma SQL de los productos con saldo (159 depósitos); de ellos, 134 migrados con 136.609 |
| PRE-B5-02 | P0 | PASA | PER | Saldos migrados coherentes: ningún saldo negativo; kárdex (entradas − salidas) = stock en todos; disponible = stock − reservado; nacionalizado ≤ recibido; fechas de ingreso entre 2022-07-04 y 2025-07-10 |
| PRE-B5-03 | P0 | PASA | RN | Kárdex de 3 migrados al azar (`2024BA00005`, `2024BA00088`, `2024BA00014`): movimientos `MigrationOpening`, entradas, salidas y saldo cuadran; fecha, agencia, manifiesto y TRM presentes; PDF 200 |
| PRE-B5-04 | P1 | OBSERVACIÓN | RN | El diario de ingresos y el de salidas de fechas migradas salen vacíos (mayo de 2024: 36 depósitos migrados, 0 en el reporte) porque la migración no carga camiones ni salidas; el histórico sigue en el legacy |
| PRE-B5-05 | P1 | PASA | RN | Informe de póliza: FOB de los levantes por mes (2024 con valores; 2026: USD 44.000 = levantes QA-PRE) |
| PRE-B5-06 | P1 | PASA | RN | «Abandono y prórrogas»: 72 en abandono (67 migrados + los migrados QA-PRE), 0 en alerta; el resumen cuadra |
| PRE-B5-07 | P1 | PASA | RN | «Depósitos pendientes»: 153 (128 migrados con factura por numerar); con el interruptor, 150 |
| PRE-B5-08 | P0 | PASA | RN | Renovación con palanca de `2022BA00001` (ciclo de 15 días, USD 239.075, TRM manual 4.151,21): período del 22/10 al 06/11 por $2.927.729,07 + IVA. Además, el primer arranque renovó **92 períodos vencidos** de migrados (la copia es del 2026-10-07) |
| PRE-B5-09 | P0 | PASA | E2E | Orden `2026OC00020`, cargue y guía `2026S00013` sobre `2024BA00005`: entrada 3.211, saldo anterior 2.000 (descuenta las salidas del legacy), sale 10, nuevo 1.990; kárdex `MigrationOpening` + `LoadingOrder` |
| PRE-B5-10 | P2 | OBSERVACIÓN | PER | 1 de 1.640 productos migrados con el nombre mal codificado («LA MUÃ…ECA»); terceros y ciudades sin ese problema |

### B6. Permisos y API (P0)

| ID | P | Estado | Tipo | Observación |
| --- | --- | --- | --- | --- |
| PRE-B6-01 | P0 | PASA | ROL | Sonda de las 348 operaciones del swagger con las 8 cuentas y sin token (3.132 peticiones; GUID inexistente y cuerpo incompleto, sin efectos; `open-billing` con un Id ficticio). Multirol = unión exacta de sus roles en todas. Sin token solo responden los 5 catálogos aceptados y la verificación pública. Frente a la matriz del 2026-10-03: 4 operaciones retiradas, 7 nuevas (`exit-block`: Admin+Billing+FT; `dispatch-guide-preview`: Admin+FT; `weighbridge/dashboard` y `…/registration`: Admin+Scale; `reports/general-inventory/locations`: Admin+Billing+FT+Warehouse; `billing/payments/vouchers`: Admin+Billing) y 74 cambios de roles, todos de las correcciones de octubre (Vigilancia fuera de Bodega; terceros Admin+CE; convenios Admin+Facturación; motivos y productos solo Admin; conductores y vehículos según `WmsPolicyRoles`). En B1 y B2 ningún rol recibió un 403 en sus pantallas ni en sus flujos. Evidencia: `evidencias/PRE/pre-api-matriz.json` y `pre-api-matriz-comparacion.txt` |
| PRE-B6-02 | P0 | PASA | SEG | Verificación pública: ver F9-API-028 |
| PRE-B6-03 | P2 | FALLA | ERR | La única respuesta 5xx de la sonda: `POST warehouse/locations` con `{}` → 500 con el texto de la excepción. **DEF-F11-033** (ya se veía en la sonda del 2026-10-03, sin ficha) |

### B7. Errores y UX (P1)

| ID | P | Estado | Tipo | Observación |
| --- | --- | --- | --- | --- |
| PRE-B7-01 | P1 | OBSERVACIÓN | ERR | Mensajes de negocio en español en todas las respuestas de la ronda. Excepciones: el aviso emergente de cada pesaje (**DEF-F11-029**), el asunto de los correos a Admin (**DEF-F11-032**) y el error del SDK de AWS en la prueba de un destino S3 |
| PRE-B7-02 | P1 | PASA | ERR | Doble envío del mismo usuario: dos cobros simultáneos de báscula → uno 200 y otro 409 «Ya existe un ciclo de báscula para este servicio.», una sola factura; dos guías simultáneas de la misma orden → 201 y 409, consecutivo +1 (`2026S00014`) |
| PRE-B7-03 | P1 | PASA | ERR | Con el API detenido: una sola franja «Sin conexión con el servidor. Reintentando… · Reintentar ahora», sin avisos apilados (DEF-F10-004 sigue corregido); la tabla de facturas dice «No se encontraron facturas» mientras tanto. Al volver el API la página se recupera sola |
| PRE-B7-04 | P1 | OBSERVACIÓN | UI | Montos «$ 20.000», «$ 16.806,72» y fechas «25/10/2026 11:19» en pantalla y PDF. Desvíos: «Ampara 50,0000» en la etiqueta (**DEF-F11-031**), horas UTC en los correos (**DEF-F11-032**) y centavos del mínimo con IVA ($40.000,01; aceptados para el corte en F11-S5) |
| PRE-B7-05 | P1 | PASA | UX | Página pública del QR en 375 × 812 sin desborde horizontal: «GUÍA VIGENTE», «GUÍA ANULADA el 25/10/2026» y «Esta guía no existe en el sistema o el código fue alterado.»; con el limitador activo dice «No se pudo consultar la guía en este momento. Intente de nuevo.» con «Reintentar». Captura: `evidencias/PRE/pre-b7-qr-vigente-movil.jpg` |

## 5. Resumen

### 5.1 Por prioridad

| Prioridad | Total | Pasa | Falla | Bloqueado | No aplica | No ejecutado | Observación |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P0 | 76 | 73 | 2 | 0 | 0 | 0 | 1 |
| P1 | 71 | 65 | 0 | 0 | 0 | 1 | 5 |
| P2 | 26 | 20 | 1 | 0 | 1 | 2 | 2 |
| P3 | 5 | 4 | 0 | 0 | 0 | 1 | 0 |
| **Total** | **178** | **162** | **3** | **0** | **1** | **4** | **8** |

- P0: 100 % ejecutado. P1: 70 de 71 (98,6 %); el que falta es FA-MIG-013, que el plan deja para el corte real.
- Los casos que se cumplen dentro de otro flujo («Ver B2») cuentan una sola vez, en el bloque de su ID.

### 5.2 Por bloque

| Bloque | Casos | Pasa | Falla | No aplica | No ejecutado | Observación |
| --- | --- | --- | --- | --- | --- | --- |
| B0 Ensayo y humo | 38 | 35 | 0 | 0 | 2 | 1 |
| B1 Pantallas por rol | 9 | 8 | 0 | 0 | 0 | 1 |
| B2 Flujos de punta a punta | 21 | 18 | 2 | 1 | 0 | 0 |
| B3 Casos nuevos del plan P1 | 61 | 59 | 0 | 0 | 0 | 2 |
| B4 Pendientes del informe P1 | 31 | 29 | 0 | 0 | 2 | 0 |
| B5 Datos migrados | 10 | 8 | 0 | 0 | 0 | 2 |
| B6 Permisos y API | 3 | 2 | 1 | 0 | 0 | 0 |
| B7 Errores y UX | 5 | 3 | 0 | 0 | 0 | 2 |

## 6. Defectos nuevos

| ID | Severidad | Título | Caso | Módulo |
| --- | --- | --- | --- | --- |
| [DEF-F11-030](defectos/DEF-F11-030.md) | CRITICAL | Reconfirmar tras corregir valor, moneda o fecha deja la factura Borrador con el importe anterior | E2E-11 paso 3, F5-COR-002 | CE / Facturación |
| [DEF-F11-034](defectos/DEF-F11-034.md) | MAJOR | Vigilancia deja salir sin guía un camión cuya orden de importación se cargó sin báscula de salida | PRE-B2-SAL-01 | Vigilancia / Bodega |
| [DEF-F11-029](defectos/DEF-F11-029.md) | MINOR | Cada pesaje muestra a Admin y CE un aviso técnico «WeighingCaptured» con el GUID del ciclo | B1, B7 | Báscula / Transversal |
| [DEF-F11-032](defectos/DEF-F11-032.md) | MINOR | Los correos de aviso a Admin cortan el asunto en el primer punto y fechan en UTC | FB-BAK-007, B7 | Transversal |
| [DEF-F11-033](defectos/DEF-F11-033.md) | MINOR | Crear una ubicación sin código responde 500 en lugar de 400 | PRE-B6-03 | Administración / API |
| [DEF-F11-031](defectos/DEF-F11-031.md) | TRIVIAL | La etiqueta con levante muestra «Ampara» con cuatro decimales | E2E-02, B7 | CE (etiqueta) |

Ningún BLOCKER. Los defectos abiertos de antes (DEF-F11-023, 024 y 026, MINOR del selector de conductor) no se volvieron a probar.

## 7. Observaciones (sin defecto)

- **Primer arranque sobre la copia:** `StoragePeriodAutoCloseJob` renovó 92 períodos vencidos de migrados y creó 92 facturas en Borrador ($63.258.314,46), porque `wms_migracion` es del 2026-10-07. En staging el job corre a diario, así que al desplegar solo renovará lo vencido desde el último arranque.
- **Diarios de fechas migradas vacíos** (PRE-B5-04): la migración no trae camiones ni salidas.
- **Centavos del mínimo con IVA** ($40.000,01 con mínimo de $40.000): ya aceptado para el corte en F11-S5.
- **Cantidad 0 por API:** `PUT foreign-trade/deposits/{id}/products/{productId}` sin `declaredQuantity` la toma como 0 (el validador acepta 0) y la reconfirmación deja el depósito sin cantidad; la facturación avisa «…no tiene cantidades declaradas…». Lo provocó una petición mal armada del ejecutor; la pantalla siempre envía el campo.
- **«Guía de salida requerida»** se envía también cuando la orden ya tiene guía vigente pero distinta de lo cargado (además del aviso de diferencia).
- **Tiquete de solo báscula** con dos pesajes: muestra tara y bruto, no el neto (el historial sí lo trae).
- **Mensaje del montacargas:** «…Factura  generada.» con doble espacio (falta el número cuando no lo hay).
- **Cartera del dashboard:** incluye el pendiente de las facturas en Borrador.
- **Etiqueta y manifiesto:** «Manifiesto No.» de la etiqueta es el manifiesto de importación que registra CE, no el del camión; sin él dice «N/A».
- **`wms_migracion`** tenía 11 migraciones aplicadas; las 6 que faltaban (desde `AddForkliftUseEntryLog`) son las que llevará la fase 13 si staging está en el mismo punto.

## 8. Pendiente para la fase 13

1. Imprimir una guía con QR y escanearla con Android e iPhone (F5-GUI-020).
2. Generar el QR con `QRCoder` en la imagen Linux del contenedor.
3. Respaldo al bucket externo real de Lightsail y fallo provocado con un bucket inexistente (FB-BAK-007).
4. PRF-002 (medición con un operario real).
5. FA-MIG-013 en el ensayo del corte con el volcado nuevo.
6. ~~Re-test de DEF-F11-030 (E2E-11 paso 3, F5-COR-002) y de DEF-F11-034 (PRE-B2-SAL-01)~~: hecho en local el 2026-10-25 (§11). Queda el de los MINOR si se corrigen.

## 9. Criterios de salida y veredicto

| Criterio (plan §6) | ¿Cumple? | Nota |
| --- | --- | --- |
| 100 % de P0 y ≥ 95 % de P1 ejecutados | Sí | P0 100 %; P1 98,6 % (FA-MIG-013 fuera de la ronda) |
| Cada FALLA con su ficha | Sí | DEF-F11-030, DEF-F11-034 y DEF-F11-033 (más tres fichas de observaciones con defecto: 029, 031 y 032) |
| Sin BLOCKER | Sí | — |
| Ensayo de migraciones sin errores | Sí | 6 migraciones en ~2 s sobre datos migrados |
| Ningún flujo P0 roto | Sí, con reparo | E2E-11 falla en un punto de control (paso 3) pero el flujo se completa; los otros 6 flujos E2E P0 pasan. La salida sin guía (PRE-B2-SAL-01) es un control que se puede saltar, no un flujo que no se pueda completar |
| Sin CRITICAL abiertos | **No** | DEF-F11-030 (CRITICAL); además DEF-F11-034 (MAJOR) |

**Veredicto: GO con condiciones para la fase 13.**

- **Condición 1 — DEF-F11-030 (CRITICAL):** corregirlo antes de desplegar, o desplegar aceptándolo con esta instrucción operativa hasta la corrección: cuando CE devuelve un depósito a Borrador y corrige **solo** el valor, la moneda o la fecha del documento, Facturación revisa la factura del período y la anula y refactura (la refacturación toma el valor vigente). Impacto en staging: facturas de almacenamiento en Borrador con el importe del valor anterior, sin aviso. No afecta stock, pesos ni permisos.
- **Condición 2 — DEF-F11-034 (MAJOR):** corregirlo antes de desplegar, o acordar con la operación que todo camión de cargue de importación pase por la báscula de salida antes del cargue y que Vigilancia verifique la guía antes de registrar la salida. Impacto en staging: un camión que se salte la báscula puede salir con mercancía de importación sin guía.
- **Condición 3:** ejecutar en staging lo del §8.
- Los MINOR y el TRIVIAL (029, 031, 032, 033) no impiden el despliegue.

## 10. Limpieza (§8 del plan)

- 12:02: API (5281) y frontend (3000) detenidos; contenedores `qa-pre-mailpit` y `qa-pre-s3mock` detenidos (eran efímeros, `--rm`); `wms-postgres-db` detenido.
- **`wms_qa_preprod` no se borró:** queda en `wms-postgres-db` para el re-test de los defectos. Bases presentes al cerrar: `wms_grabacion`, `wms_grabacion_anular`, `wms_grabacion_plantilla`, `wms_migracion`, `wms_qa_preprod`, `wmsdb`.
- En la copia quedan las cuentas `qa.pre.*` (con `qa.pre.boot`), los datos QA-PRE del registro, los destinos de respaldo QA-PRE inactivos y el camión `QPE001` en planta (DEF-F11-034). Las claves y la clave de prueba del QR viven solo en el scratchpad del ejecutor.
- Sin commits ni cambios de código o configuración versionada. Evidencias en `qa/resultados/evidencias/PRE/`: la matriz del API, su comparación con la del 2026-10-03 y la captura del QR en celular. Los PDF de datos QA-PRE se revisaron con `pdftotext` y quedaron en el scratchpad; no se guardaron capturas con datos de personas.

## 11. Anexo — Re-test de DEF-F11-030 y DEF-F11-034 (2026-10-25)

Fase 4 de `planes/plan-cerrado-correccion-def-f11-030-034-2026-10-25.md`. Local, sobre la copia `wms_qa_preprod` que se conservó (§10).

- **Builds:**
  - BE `b3de3cc`, más la corrección de DEF-F11-035 sin commit;
  - FE `83a0af0`.
- **Cómo se ejecutó:** API en 5281 y frontend de desarrollo en 3000, con las cuentas `qa.pre.*`. El cargue de Bodega se probó en la pantalla, con la sesión Admin de la ronda; lo demás, por API.
- **Datos:** prefijo `QA-PRE-RT-`, camiones `QPR0nn`, depósitos `2026BA00036`–`2026BA00040` y `2026EXP00003`, órdenes `2026OC00024`–`2026OC00028`.
- **Tarifas:** desde la ronda, C1 tiene convenio de almacenamiento al 0,22 % del valor y C2 al 0,25 %. Por eso los importes no coinciden con la tarifa base T1 (0,295 %) del §4.

### 11.1 DEF-F11-030 — Corrección en Borrador y cambio de cliente

| ID | P | Resultado | Evidencia |
|---|---|---|---|
| F5-COR-007 (valor) · F5-COR-002 · E2E-11 paso 3 | P0 | PASA | `2026BA00036` confirmado con USD 10.000: factura Borrador, subtotal $69.485,46 → devolver a Borrador → `PATCH …/draft` con 20.000: **la misma factura** pasa a $138.970,92 (+ IVA = $165.375,39) al guardar → reconfirmar: `Confirmed`, una sola factura, sin otro recálculo. Auditoría: «Recálculo del almacenamiento del depósito 2026BA00036 por corrección de valor de la mercancía…» |
| F5-COR-007 (moneda) | P0 | PASA | `2026BA00037` confirmado en COP 100.000.000: subtotal $220.000 → devolver → pasar a USD 30.000: TRM DIAN 3.158,43 asignada y subtotal $208.456,38 (30.000 × 3.158,43 × 0,22 %) |
| F5-COR-007 (agencia) | P1 | PASA | Mismo depósito, `PUT …/stakeholders` con otra agencia: el detalle de la factura cambia de «AGENCIA:QA-PRE Agencia SIA SAS» a la agencia nueva (una agencia migrada) |
| F5-COR-007 (aprobada) | P0 | PASA | `2026BA00036` con la factura numerada `QA-PRE-FE-RT01` y aprobada → devolver y corregir a USD 15.000: mismo número y estado, total $165.375 → $124.032. Facturación (los 3 usuarios del rol) recibe «Factura de almacenamiento actualizada» con el total anterior y el nuevo |
| F5-COR-008 (Borrador) | P0 | PASA | `2026BA00038` de C1 (subtotal $69.485,46) → devolver → cliente C2: factura y período pasan a C2 y se recalculan con su convenio (subtotal $78.960,75, 0,25 %) |
| F5-COR-008 (aprobada) | P0 | PASA | `2026BA00036` con `QA-PRE-FE-RT01` aprobada: `PATCH …/customer` (Confirmed) y `PATCH …/draft` (Borrador) → 409 «La factura de almacenamiento QA-PRE-FE-RT01 del depósito 2026BA00036 está aprobada: Facturación debe anularla antes de cambiar el cliente.»; el cliente y la factura no cambian |
| F5-COR-008 (anulada) | P0 | PASA | `2026BA00037`: Facturación anula la factura → devolver → cliente C2: el período pasa a C2 → refacturar: factura nueva a C2, subtotal $236.882,25 (USD 30.000 × 3.158,43 × 0,25 %) |

### 11.2 DEF-F11-034 — Guía antes del cargue de importación

| ID | P | Resultado | Evidencia |
|---|---|---|---|
| F4-CAR-016 | P0 | PASA | Pantalla: `2026OC00024` (importación, sin guía) → aviso «Esta orden es de importación y no tiene guía de salida vigente. El conductor debe solicitarla en Comercio Exterior antes del cargue.» y «Ejecutar Cargue» deshabilitado con firma y stock completos. API: 409 «No se puede cargar la orden 2026OC00024: es de importación y no tiene guía de salida vigente…»; la OC sigue `Pending`, sin movimientos y con la reserva activa |
| F4-CAR-017 | P1 | PASA | Con la guía `2026S00015` emitida: «Guía de salida 2026S00015 vigente. Verifíquela con el conductor.» y el cargue se ejecuta desde la pantalla (OC `Loaded`). La orden de exportación `2026OC00028` no muestra aviso, carga, recibe la guía automática `2026S00019` (Export) y queda `Dispatched` |
| PRE-B2-SAL-01 | P0 | PASA | `QPR010` entra con «Cargue mercancia importacion» y no pasa por báscula: el cargue sin guía responde 409 y la mercancía no sale. Con la guía, carga, y Vigilancia registra la salida (200) con la OC `Loaded`, sin pesaje: es el riesgo aceptado en `DEC-056` |
| F4-CAR-002 | P1 | FALLA → PASA | El primer cargue con guía (`2026OC00024`) avisó a Comercio Exterior «Guía de salida requerida… Generar guía de salida.» aunque la guía ya existía: **DEF-F11-035** (MINOR). Se corrigió en esta fase (el aviso solo sale sin guía vigente, D15). Tras la corrección, E2E-01 y E2E-17 no lo generan |
| E2E-01 | P0 | PASA | `2026BA00039` (100 unidades, USD 30.000) confirmado; factura `QA-PRE-FE-RT20` aprobada; levante 100; salida de `QPR020` → `QPR021` con cargue de importación → `2026OC00025` → salida en báscula con cobro y tara 14.000 (OC `InProgress`) → **guía `2026S00016` antes del cargue** (100/100/100/0) → cargue 100: OC `Loaded`, stock 0, depósito `Closed`, período cerrado, sin aviso de guía → repesaje 34.000: OC `Dispatched`, servicio `Completed` → salida de `QPR021` → kárdex IN 100 / OUT 100 |
| E2E-17 | P2 | PASA | `QPR030` entra con `2026BA00040` (tiquete `2026T00055`) → levante → `2026OC00027` de ese depósito → guía `2026S00018` → salida con el tiquete de ingreso (OC `InProgress`, `awaitingGuide: false`) → cargue → OC `Dispatched` sin segundo pesaje y sin aviso de guía |

En el primer intento, E2E-17 usó otro depósito y la salida respondió 409: «La orden … tiene mercancía del depósito …, que no llegó en el tiquete…». Es una regla vigente, no un defecto. Esa guía (`2026S00017`) se anuló y la OC `2026OC00026` se canceló.

### 11.3 Compuertas tras DEF-F11-035

| Compuerta | Resultado |
|---|---|
| `Wms.Tests` | 2008/2008 |
| `Wms.IntegrationTests` | 431/433; fallan solo las 2 de la línea base |
| `has-pending-model-changes` | Limpio |

`LoadingRequiresGuideTests.ImportOrderWithGuide_Loads` comprueba que no hay aviso y falla con el código anterior.

### 11.4 Veredicto del re-test

- **Fichas:** DEF-F11-030 y DEF-F11-034 pasan a **Verificado**. DEF-F11-035 se detectó, corrigió y verificó en el re-test.
- **Condiciones del §9:** se levantan las condiciones 1 y 2. Ya no hay CRITICAL ni MAJOR abiertos de la ronda. Sigue la condición 3 (§8, puntos 1 a 5) en staging.
- **Veredicto: GO para la fase 13**, con lo del §8 y estos avisos:
  - antes de desplegar, el commit de la corrección de DEF-F11-035;
  - comunicar `DEC-056` a los operarios de Comercio Exterior y Bodega, y a Vigilancia: el conductor pide la guía de importación antes del cargue.
- **Limpieza:** API, frontend y `wms-postgres-db` detenidos. `wms_qa_preprod` conserva los datos `QA-PRE-RT-`.

## 12. Anexo — Re-test de DEF-F11-029, 031, 032 y 033 (2026-10-25)

Plan `planes/plan-cerrado-correccion-def-f11-029-033-2026-10-25.md`. Local, sobre la copia `wms_qa_preprod` que se conservó (§10).

- **Builds:**
  - BE `390eb0e`, más la corrección sin commit;
  - FE `83a0af0`, sin cambios.
- **Cómo se ejecutó:** solo por API, en el puerto 5281, con el sumidero SMTP `axllent/mailpit` (SMTP 1025). `Notifications:AdminEmails` es una dirección de prueba.
  - Para conectarse a la base se creó el rol temporal `qa_rt_029`, con permisos solo en `wms_qa_preprod`, y se eliminó al terminar.
  - Las cuentas `qa.rt.*` son nuevas: `qa.rt.boot` (Admin, por `Bootstrap`), `qa.rt.comext`, `qa.rt.bascula` y `qa.rt.vigilancia`. Las claves viven solo en el scratchpad del ejecutor.
  - Los avisos en tiempo real se leyeron con un cliente SignalR conectado como Admin y como CE. El frontend muestra como aviso emergente cada `ReceiveNotification` que llega por esa conexión.
- **Datos:** camión `QPT313` (motivo «Solo Bascula»), ciclo `a329eccf…`, tiquete `2026T00057`. Evidencia: `evidencias/PRE/pre-retest-def-f11-029-033.txt`.

| ID | Defecto | P | Resultado | Evidencia |
|---|---|---|---|---|
| PRE-B1-CE / PRE-B7-01 | DEF-F11-029 | P0/P1 | PASA | `QPT313` entra, se pesa (tara 12.000, bruto 30.000; el ciclo se completa), se corrige y sale. Admin y CE reciben solo «Trazabilidad» («Camión QPT313 cambió a estado: …») y, el Admin, la «Modificación de Peso en Báscula». Ningún «WeighingCaptured» ni «WeighbridgeCycleCompleted» |
| FB-BAK-007 / F3-COR-011 | DEF-F11-032 | P1 | PASA | `qa.rt.bascula` corrige el bruto (30.000 → 31.000). Asunto: «⚠️ [Admin] El usuario qa.rt.bascula modificó el pesaje #2 (Bruto) del ciclo a329eccf». Cuerpo: «Fecha y Hora 25/10/2026 17:45 (hora Colombia)», enviado a las 17:45 −05. El rol sigue en inglés («[Admin]», «Nivel Warning»), fuera de alcance (D5) |
| PRE-B6-03 | DEF-F11-033 | P2 | FALLA → PASA | `POST warehouse/locations` con `{}` como Admin responde **400** «Error de validación.» con tres mensajes: «El código de ubicación es requerido.», «El nombre de ubicación es requerido.» y «La capacidad debe ser mayor a cero.» |
| E2E-02 paso 4 / PRE-B7-04 | DEF-F11-031 | P0/P1 | PASA | Tabla Ampara / Saldo con `pdftotext -layout`, el mismo formato en todas las celdas: `2026BA00003` 98 / 0 (se despachó entero después de la ronda), `2026BA00040` 10 / 4, `2026BA00021` 15 / 25, `2026BA00004` 120 / 70 y el migrado `2023BA00019` 1.350 / 365. Ya no aparece «50,0000» |

### 12.1 Compuertas

| Compuerta | Resultado |
|---|---|
| `dotnet build Wms.sln` | Sin errores |
| `Wms.Tests` | 2016/2016 |
| `Wms.IntegrationTests` | 433/435. Fallan solo las 2 de la línea base, que pasan al correrlas solas |
| `has-pending-model-changes` | Limpio |

### 12.2 Veredicto

- **Fichas:** DEF-F11-029, 031, 032 y 033 pasan a **Corregido**, con el re-test en PASA. Pasan a «Verificado» cuando se haga el commit del backend.
- **Ronda:** no quedan defectos de la ronda sin corregir. Siguen abiertos los MINOR del selector de conductor (DEF-F11-023, 024 y 026) y la condición 3 del §9 (§8, puntos 1 a 5) en staging.
- **Limpieza:**
  - API, `qa-rt-mailpit` y `wms-postgres-db` detenidos;
  - rol `qa_rt_029` eliminado;
  - `wms_qa_preprod` conserva el camión `QPT313` (salió) y las cuentas `qa.rt.*`.
