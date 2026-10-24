# 02 — Progreso de la auditoría

> **Fecha:** 2026-10-23. Se actualiza al cerrar cada tanda.

## 1. Estado

| Fase | Estado |
| --- | --- |
| 1. Inventario documental (`00-evaluacion-analisis-existente.md`) | Completa (la clasificación de conclusiones se consolida en `08-auditoria-del-analisis-inicial.md`) |
| 2. Inventario funcional global (`01-inventario-funcional-global.md` y `.csv`) | Completa: 263 capacidades legacy, 49 candidatas V2 |
| 3. Plan de agentes | Completa (§2) |
| 4–7. Auditoría por módulo | Completa: 8 de 8 módulos |
| 8. Control de calidad | Completa (§4) |
| 9–10. Consolidación y recomendaciones QA | Completa: `03`…`09` |
| Decisiones del negocio (posterior) | 2026-10-23: el usuario respondió las 13 preguntas. Quedaron registradas en `docs/contexto/decisiones.md` (DEC-050…054; DEC-012 precisada) y aplicadas a `03`, `04`, `05`, `06`, `07`, `08` y `09`. Las matrices de módulo no se reescriben: sus `08-brechas.md` llevan una nota final |

## 2. Plan de agentes

**Mecanismo:** subagentes de la herramienta `Agent` de Claude Code, lanzados en paralelo, 4 por tanda. Cada uno lee `_instrucciones-agentes.md` (restricciones §3 completas del encargo, estados, entregables, formato de matriz y de brechas) y su encargo particular. Cada agente audita el recorrido completo de su módulo (legacy, frontend, backend, integración, reglas); ningún módulo se reparte por capas.

| Agente | Tanda | Módulo / directorio exclusivo | Capacidades | Rango de IDs nuevos | Referencias documentales principales | Dependencias conocidas |
| --- | --- | --- | --- | --- | --- | --- |
| AG-01 | 1 | `modulos/01-administracion-catalogos/` | 98 legacy (`CF-L001…016`, `021…064`, `073…101`, selectores `241…248`, `253`, `256`) + `CF-V001…011` | `CF-LX01-nn`, `CF-V012…019`, `BR-01-nnn` | `MIGRATION_MATRIX.md`, `FUNCTIONAL_GAPS.md` (GAP-022, 023, 025, 026), plan backend F2-06, F4-10, F6-02; `DEC-011`, `DEC-015`, `DEC-017`, `DEC-030`, `DEC-031`; QA F1, F9 | Ciudades alimentan 05 (destino de la orden); cuadrillas, 05 (guía); tarifas y convenios van en 06 |
| AG-02 | 1 | `modulos/02-bascula/` | 22 legacy (`CF-L102…121`, `235`, `255`) + `CF-V020…025` | `CF-LX02-nn`, `CF-V026…029`, `BR-02-nnn` | `BASCULA_PARITY.md`, plan backend F1-01…09, F3-09, F4-07, F4-08, F5-09; plan frontend fase 1, DF2, DF5–DF11, DF15–DF16; `DEC-010`, `012`, `013`, `016`, `017`, `019`; QA F3, PRF-002 | Crea o asocia depósitos (04); cobros de báscula y tarifas (06); salida con tiquete de ingreso (05) |
| AG-03 | 1 | `modulos/03-vigilancia-bodega/` | 16 legacy (`CF-L168…180`, `230`, `236`, `254`) + `CF-V030…035` | `CF-LX03-nn`, `CF-V036…039`, `BR-03-nnn` | plan backend F4-01…04; `FUNCTIONAL_GAPS.md` GAP-004, 014, 015; `DEC-010`, `014`, `018`, `019`; QA F2, F4 | Recepción depende de báscula (02); cargue de la orden (05); montacargas factura (06) |
| AG-04 | 1 | `modulos/04-ce-ingresos-depositos/` | 24 legacy (`CF-L122…142`, `237`, `259`, `260`) + `CF-V040…045`, `CF-V084` | `CF-LX04-nn`, `CF-V046…049`, `BR-04-nnn` | plan backend F1-04…08, F2-08…10, F3-08, F4-05, F4-06, F4-09; `GAP-003`, `011`, `012`, `013`; `DEC-012…016`, `DEC-020`; QA F5; `revision-fob-cif…` | Depósitos que nacen en báscula (02); levantes y salidas (05); facturación del período (06); reportes de abandono (07) |
| AG-05 | 2 | `modulos/05-ce-levantes-salidas/` | 28 legacy (`CF-L143…167`, `238`, `239`, `261`) + `CF-V050…053` | `CF-LX05-nn`, `CF-V054…059`, `BR-05-nnn` | plan backend F2-01…05, F2-07, F3-01…04, F3-07, F4-07, F4-08, F4-10; `GAP-002`, `006`, `009`, `019`, `025`; P16; `DEC-012`, `016`, `019`; QA F5 | Depósitos (04); cargue en Bodega (03); pesaje de salida (02); cobro de guía (06) |
| AG-06 | 2 | `modulos/06-facturacion/` | 22 legacy (`CF-L017…020`, `065…072`, `201…207`, `234`, `249`, `251`) + `CF-V060…067` | `CF-LX06-nn`, `CF-V068…069`, `BR-06-nnn` | plan backend F3-05, F3-06, F3-10, F5-08; `GAP-007`, `008`, `020`; `DEC-020…028`, `DEC-041`; `analisis-motor-acuerdos…`; `manual-modulo-facturacion.md`; QA F6 | Todos los módulos que generan cargos |
| AG-07 | 2 | `modulos/07-reportes-exportaciones/` | 15 legacy (`CF-L208…216`, `229`, `231…233`, `252`, `258`) + `CF-V070…071` | `CF-LX07-nn`, `CF-V072…079`, `BR-07-nnn` | plan backend §C.5 (C.5.0 mapa de informes, F5-01…10); `GAP-010`, `016`, `017`; DF12; QA F7 | Datos de 02, 04, 05, 06 |
| AG-08 | 2 | `modulos/08-procesos-infra-fuera-alcance/` | 38 legacy (`CF-L004`, `181…200`, `217…228`, `240`, `250`, `257`, `262`, `263`) + `CF-V080…083`, `CF-V085` | `CF-LX08-nn`, `CF-V086…099`, `BR-08-nnn` | plan backend §C.6 (F6-01…05); `GAP-001`, `021`; P13, P14; DF3; `DEC-040…042`; `docs/planes/migracion-staging/`; `deploy/ayuda/README.md` | Verifica que las exclusiones (Colmotores, portal) no dejaron dependencias en los demás módulos |

Entregables, restricciones y formato: `_instrucciones-agentes.md` §2–§9.

## 3. Tandas

| Tanda | Agentes | Inicio | Fin | Resultado |
| --- | --- | --- | --- | --- |
| 1 | AG-01, AG-02, AG-03, AG-04 | 2026-10-23 | 2026-10-23 | Los 4 módulos entregados. Control de calidad: AG-02 corrigió estados inválidos en la dimensión reglas (CF-L116.c, CF-L255 y 15 reglas de su `03-reglas-negocio.md`); AG-01 debe citar la decisión en 23 filas `DIFERENCIA_INTENCIONAL` que solo decían «Ídem» |
| 2 | AG-05, AG-06, AG-07, AG-08 | 2026-10-23 | 2026-10-23 | Los 4 módulos entregados. AG-05 y AG-06 se lanzaron al cerrar AG-02/03/04; AG-07 y AG-08 al cerrar AG-01, para no pasar de 4 agentes simultáneos. Sus encargos incluían las lecciones de la tanda 1 y no necesitaron correcciones de formato |

## 4. Estado por módulo

| Módulo | Capacidades asignadas / auditadas | Filas de matriz | Brechas (A/M/B) | Estado | Pendiente |
| --- | --- | ---: | --- | --- | --- |
| 01 Administración y catálogos | 98 + 11 V2 / todas (+2 `CF-LX`, +2 V2) | 113 | 0 / 1 / 7 | Completo | Efecto de desactivar un cliente en la facturación (QA-15) |
| 02 Báscula | 22 + 6 V2 / todas (+1 `CF-LX`, +4 V2) | 43 | 1 / 5 / 12 | Completo | PRF-002 (ejecución) |
| 03 Vigilancia y Bodega | 16 + 6 V2 / todas (+3 `CF-LX`, +4 V2) | 38 (37 en la global) | 0 / 2 / 9 | Completo | `CF-L172.c` cerrada por el módulo 07 |
| 04 CE: ingresos y depósitos | 24 + 7 V2 / todas (+1 `CF-LX`, +3 V2) | 39 | 0 / 3 / 9 | Completo | Uso real de seriales y etiqueta por vehículo (datos) |
| 05 CE: levantes, órdenes y guías | 28 + 4 V2 / todas (+2 `CF-LX`, +5 V2) | 43 | 0 / 7 / 6 | Completo | BR-05-002 y BR-05-007 exigen ejecución |
| 06 Facturación | 22 + 8 V2 / todas (+1 `CF-LX`, +4 V2) | 44 | 2 / 5 / 7 | Completo | BR-06-004 exige ejecución |
| 07 Reportes y exportaciones | 15 + 2 V2 / todas (+2 `CF-LX`) | 33 | 0 / 4 / 9 | Completo | Si los diarios se entregaban firmados (datos) |
| 08 Procesos, infra y excluidas | 38 + 5 V2 / todas (+1 `CF-LX`, +2 V2) | 58 | 1 / 5 / 8 | Completo | Producción sin definir (despliegue) |

Ningún módulo quedó sin analizar. Lo que no se pudo cerrar por ser estático o por depender de datos está en `07-pendientes-no-verificados.md`.

## 5. Control de calidad (Fase 8)

Revisión del orquestador sobre los entregables de cada agente:

| Verificación | Método | Resultado |
| --- | --- | --- |
| CSV válido (UTF-8, 20 campos, encabezados exactos) | `csv.reader` sobre los 8 `07-matriz-paridad.csv` | 8/8 válidos. 410 filas en total; la global tiene 410 tras quitar un duplicado |
| Estados dentro del vocabulario por dimensión | Script de validación por columna | AG-02 tenía `DIFERENCIA_INTENCIONAL` en la dimensión reglas (2 filas de la matriz y 15 reglas de `03-reglas-negocio.md`); lo corrigió |
| `COMPLETO_CODIGO` con alguna dimensión `NO_VERIFICADO` | Script | 0 casos |
| Toda `DIFERENCIA_INTENCIONAL` cita una fuente válida (§8.5) en su propia fila | Búsqueda de `DEC-`, `P`n, `DF`n, `GAP-`, `DECISIONES_REVISION`, §A.3/A.4, §B.4, §10 | AG-01 tenía 23 filas que solo decían «Ídem»; las corrigió. 0 pendientes |
| Cobertura de las capacidades asignadas | Cruce con `01-inventario-funcional-global.csv` | 263/263 capacidades legacy presentes en alguna matriz |
| IDs del CSV presentes en el Markdown | Script | 0 ausentes en los 8 módulos |
| Totales de brechas coherentes entre el registro, la tabla y el resumen | Conteo de las fichas | AG-02 tenía MEDIA 6 / BAJA 11 en el resumen y 5 / 12 en las fichas; lo alineó a las fichas |
| Duplicados entre módulos | Cruce de IDs | `CF-L172.c` en 03 y 07: queda la del 07 (consolidación) |
| Referencias reales | Apertura de una muestra de evidencia por el orquestador | Confirmadas en el código: BR-03-001 (`EntryLogController.cs:63-72`, `UpdateEntryLogHandler.cs:80-83`, `updateEntryLog` sin llamadas); BR-02-006 (`ModifySecondWeightHandler.cs:61-84`, `ModifyWeighingDialog.vue:123-131`); BR-04-002 (`WarehouseStorage.cs:194-219`); BR-06-001 (sin transición `Scheduled → Active`); BR-07-003 (`GetDailyIncomingGoodsReportHandler.cs:51-53`, `GetWarehouseStorageMovementsHandler.cs:309`); BR-05-007 (`releases/index.vue:49-50`, `GetReleasesQuery.cs:19-20`); BR-08-014 (`GetNotificationsHandler.cs:35-36`); BR-01-003 (`CustomsAgencyResolver.cs:16`) |
| Secretos y datos de personas | Búsqueda de claves, contraseñas y placas en `modulos/` | Sin hallazgos. Solo códigos de modalidad (`IMP001`, `EXP001`) y la mención, sin copiar, de credenciales en `menus/backup.php` del legacy |
| Restricciones | Informe de cada agente | Ningún agente informó uso de Git, ejecución, apertura de secretos ni de `db_legacy/`, ni escritura fuera de su directorio |

**Limitación del control:** la muestra abierta por el orquestador son 8 brechas de 103. El resto de la evidencia se aceptó por su consistencia (rutas existentes, estados coherentes, citas de decisión verificables), no por relectura de cada línea.

**Archivos auxiliares de los agentes:** `modulos/05-ce-levantes-salidas/_fuente-matriz.txt` y `modulos/06-facturacion/_fuente-matriz.psv` son las fuentes desde las que esos agentes generaron su `.md` y su `.csv`. Se dejan como están.
