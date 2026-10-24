# 08-procesos-infra-fuera-alcance — Resultado del agente (AG-08)

> **Fecha:** 2026-10-23. Auditoría estática: no se ejecutaron builds, pruebas, servidores ni llamadas, no se consultó Git, y no se abrieron `Connections/`, `.env*`, `deploy/staging/.env.*`, `infra/terraform.tfvars`, `terraform.tfstate*` ni `db_legacy/`. Código en disco a esa fecha (según `docs/contexto/estado.md`: BE `35a61b2` / FE `c924a8b`).
> **Prefijos:** `L/` = `bodegas-legacy/`; `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`; `D/` = `docs/`.

## 1. Cobertura

| Concepto | Asignadas | Auditadas |
| --- | ---: | ---: |
| Capacidades legacy (`CF-L004`, `181…200`, `217…228`, `240`, `250`, `257`, `262`, `263`) | 38 | 38 |
| Altas legacy de AG-08 (`CF-LX08-01`) y desgloses (`CF-L217.a/.b`) | — | 3 |
| Candidatas V2 (`CF-V080…083`, `CF-V085`) | 5 | 5 (una con la descripción corregida) |
| V2 nuevas de AG-08 (`CF-V086`, `CF-V087`) y desgloses (`CF-V080.a…e`, `CF-V081.a…e`) | — | 12 |
| **Filas de la matriz** | — | **58** |

## 2. Paridad integral

| Estado | Capacidades legacy asignadas (38) | Todas las filas (58) |
| --- | ---: | ---: |
| `COMPLETO_CODIGO` | 0 | 1 (`CF-LX08-01`) |
| `PARCIAL` | 0 | 0 |
| `NO_IMPLEMENTADO` | 0 | 0 |
| `DIFERENCIA_INTENCIONAL` | 1 (`CF-L004`: P14, DF3, `DECISIONES_REVISION.md` §2.E.16) | 1 |
| `NO_VERIFICADO` | 0 | 0 |
| `NO_APLICA` | 37 (36 de Colmotores; `CF-L217` por acceso) | 56 (39 por exclusión y 17 por origen `SOLO_V2`) |

**Por dimensión (58 filas):**

| Dimensión | Estados |
| --- | --- |
| Frontend | `NO_APLICA` 55 · `COMPLETO_CODIGO` 1 · `PARCIAL` 1 · `NO_IMPLEMENTADO` 1 |
| Backend | `NO_APLICA` 41 · `COMPLETO_CODIGO` 13 · `PARCIAL` 4 |
| Integración | `NO_APLICA` 54 · `CONECTADO_CODIGO` 3 · `SIN_INTEGRACION` 1 |
| Reglas de negocio | `NO_APLICA` 44 · `COMPLETO_CODIGO` 8 · `PARCIAL` 6 |

**Validación por ejecución.** `CF-L004` y `CF-V080` están validados por FB-BAK-003 y 005 y por la corrida de las 02:00. `CF-V081` está validado por OK-1…8 de la migración y la fase 3 en staging. `CF-V082` está validado en parte por F7-NOT. `CF-V083`, `CF-V085`, `CF-V086` y `CF-V087` no tienen ejecución propia. Las 39 filas excluidas no aplican.

## 3. Brechas

| Criticidad | Cantidad | IDs |
| --- | ---: | --- |
| CRÍTICA | 0 | — |
| ALTA | 1 | BR-08-001 |
| MEDIA | 5 | BR-08-003, 004, 005, 008, 014 |
| BAJA | 8 | BR-08-002, 006, 007, 009, 010, 011, 012, 013 |

**Las más graves:**

1. **BR-08-001 (ALTA):** los respaldos van a una sola carpeta del mismo servidor. S3 no está configurado, el aviso de fallo solo se ve dentro de la aplicación y no hay política de producción (`ROADMAP.md` 0.3).
2. **BR-08-014 (MEDIA, defecto nuevo):** los avisos se ordenan del más antiguo al más reciente (`GetNotificationsHandler.cs:35-36`). Con más de 15, el panel no muestra los nuevos.
3. **BR-08-003 (MEDIA):** la prórroga del legacy no se migra. Los migrados con prórroga vencen a los 30 días y admiten una segunda.
4. **BR-08-005 (MEDIA):** dos depósitos vivos con el mismo número de años distintos no se pueden migrar, por la agrupación por número y el índice único de `legacy_number`.
5. **BR-08-004 (MEDIA):** no hay procedimiento para las operaciones en curso el día del corte.

**Citados, sin duplicar:** FOB/CIF (`estado.md` §4 n.º 8), corte real (n.º 7), vaciar staging (n.º 6), baja de Azure test (n.º 9), publicación de videos (n.º 10) y posiciones de bodega no migradas (BR-03-006).

## 4. SOLO_V2 confirmadas

`CF-V080` (respaldos, reemplazo ampliado de `CF-L004`), `CF-V081` (importación legacy), `CF-V082` (notificaciones en tiempo real), `CF-V083` (centro de ayuda), `CF-V085` (**corregida**: es la TRM de la DIAN del día, no el estado del sistema, y no tiene consumidor), `CF-V086` (infraestructura de jobs, nueva) y `CF-V087` (avisos por correo, nueva). Son 7.

**Endpoints sin consumidor:** los 6 de respaldos y los 5 de importación son intencionales (DF3, P14). `GET system/dian-trm/today` no tiene decisión (BR-08-011). **Llamadas del frontend sin endpoint:** ninguna.

**Parte B:** no quedan restos de Colmotores ni del portal en V2: sin entidades, enums, tablas EF, endpoints, rutas ni textos de menú. Ningún módulo depende de VIN, serial o voltaje (`05-analisis-v2.md` §8). El único dato no Colmotores del portal era la consulta de ingresos de las agencias de aduanas. V2 la ofrece solo de forma interna (BR-08-008, alcance a confirmar con el negocio).

## 5. Contraste con el análisis anterior

### 5.1 Estados de `MIGRATION_MATRIX.md` (38 capacidades)

| Estado previo | Capacidades | Clasificación | Motivo |
| --- | ---: | --- | --- |
| REQUIERE VALIDACIÓN (`CF-L004`) | 1 | `OBSOLETA` | F6-05 implementado: hay función en la aplicación (`BackupsController`, job). La observación «solo cron opcional» ya no aplica |
| EXCLUIDA, Colmotores inhabilitado (`CF-L181…200`, `218…228`, `240`, `250`, `257`, `262`, `263`) | 36 | `CONFIRMADA_EN_CODIGO` | Sin restos ni dependencias en V2 |
| EXCLUIDA, acceso (`CF-L217`) | 1 | `INCOMPLETA` | El portal es de Colmotores y, además, de agencias de aduanas. La parte de agencias tenía datos no Colmotores que no quedaron cubiertos por la exclusión (BR-08-008) |

**Totales:** `CONFIRMADA_EN_CODIGO` 36 · `INCOMPLETA` 1 · `OBSOLETA` 1 · `CONTRADICHA_POR_CODIGO` 0 · `NO_VERIFICADA` 0.

### 5.2 Afirmaciones de los planes y documentos

| # | Afirmación (fuente) | Clasificación | Evidencia |
| --- | --- | --- | --- |
| 1 | Fase 6 implementada: CSV con simulación y conciliación; respaldos diarios con destinos (`plan-backend-paridad-legacy.md` §A.1, §C.6) | `CONFIRMADA_EN_CODIGO` | `LegacyImportController.cs`, `BackupsController.cs`, `BackupService.cs` |
| 2 | Endpoints `AdminOnly`, `dryRun` verdadero por defecto, 50.000 filas, 500/1.000 errores (F6-01) | `CONFIRMADA_EN_CODIGO` | `LegacyImportController.cs:26,47`; `ImportLegacyFileCommandHandler.cs:20-33,97` |
| 3 | Colmotores excluido en la exportación: cliente 70 y bodegas `uso='colmotores'` (F6-02) | `CONFIRMADA_EN_CODIGO` | Consultas `plan-backend-paridad-legacy.md:2822,2853`; el importador no filtra (R-12) |
| 4 | Depósitos vivos con saldo, levantes y kárdex de apertura (F6-03) | `CONFIRMADA_EN_CODIGO` | `DepositsImporter.cs:170-226`; validado en la fase 3 |
| 5 | La consulta desempata «dos depósitos vivos con el mismo número de años distintos» (F6-03, O-1) | `INCOMPLETA` | Solo el orden; el importador los rechaza (BR-08-005) |
| 6 | La conciliación informa lo que cambió en la v2 «para no confundir operación nueva con descuadre» (F6-04) | `INCOMPLETA` | Movimientos sí; levantes no (BR-08-007) |
| 7 | Apertura de facturación contigua al último período, un depósito por transacción (F6-04) | `CONFIRMADA_EN_CODIGO` | `OpenMigratedBillingCommand.cs:82-129` |
| 8 | Retención 30 + 12, diario a las 02:00, idempotente, primero del mes mensual, aviso a Admin, credenciales fuera de la base (F6-05, P14) | `CONFIRMADA_EN_CODIGO` | `BackupRetentionPolicy.cs`; `DatabaseBackupBackgroundService.cs`; `S3BackupTarget.cs:39-40` |
| 9 | «Los destinos se configuran desde la aplicación: disco local o S3» (P14) | `CONFIRMADA_EN_CODIGO` | Por API (DF3). Solo Local en uso (BR-08-001) |
| 10 | Fase 6 sin pantallas, operada por API (DF3) | `CONFIRMADA_EN_CODIGO` | Búsqueda `legacy-import`, `backup` en `F/`: 0 consumidores |
| 11 | `legacy_number` no viaja en los DTO (plan frontend §C.6 y §G.12) | `CONFIRMADA_EN_CODIGO` | Sigue igual (BR-08-006) |
| 12 | Notificaciones sin enlace a la entidad (plan frontend §G.13) | `CONFIRMADA_EN_CODIGO` | Sigue igual (BR-08-010) |
| 13 | GAP-001 «ninguna herramienta de carga» y GAP-021 «ninguna en la aplicación» (`FUNCTIONAL_GAPS.md`) | `OBSOLETA` | Cerradas por F6-01…05 |
| 14 | ROADMAP 0.3 «definir la política de respaldo de producción» | `INCOMPLETA` | Hay código y staging, sin política de producción (BR-08-001) |
| 15 | ROADMAP 6.3 «conservando el número legacy como referencia» | `INCOMPLETA` | Se guarda, no se ve (BR-08-006) |
| 16 | ROADMAP 0.1 contar órdenes y guías abiertas al corte | `INCOMPLETA` | Sin procedimiento (BR-08-004) |
| 17 | `DECISIONES_REVISION.md` §2.E.16 «política similar a la del legacy» | `CONFIRMADA_EN_CODIGO` | Supera al legacy; queda pendiente el despliegue (BR-08-001) |
| 18 | `estado.md` §3 «Respaldos diarios a las 02:00 en `/opt/wms/backups`» | `CONFIRMADA_EN_CODIGO` | `compose.staging.yaml:78-92`; `informe-fase-5.md:44` |
| 19 | `00-evaluacion` §4.4 «las exclusiones no dejaron dependencias rotas» (para las 37 de este módulo) | `CONFIRMADA_EN_CODIGO` | `05-analisis-v2.md` §8 |
| 20 | Inventario §7: `CF-V085` «Estado del sistema» | `CONTRADICHA_POR_CODIGO` | Solo la TRM de la DIAN (`SystemController.cs:18`) |
| 21 | Runbook: el Id «que muestra la pantalla de respaldos» (`B/deploy/staging/README.md:206`) | `CONTRADICHA_POR_CODIGO` | No hay pantalla (el mismo runbook lo dice en `:160`) |
| 22 | Caso FB-BAK-006: «`Backups__Enabled` no está en `compose.staging.yaml`» (`D/qa/fase-11-regresion-cierre.md:140`) | `OBSOLETA` | Ya está (`compose.staging.yaml:80`) |
| 23 | F7-NOT-006 PASA: página de notificaciones correcta (`F7-informe-2026-10-03.md:77`) | `INCOMPLETA` | El orden quedó sin verificar (BR-08-014) |
| 24 | `estado.md` §1 «toda la funcionalidad planeada está implementada» (alcance de este módulo) | `CONFIRMADA_EN_CODIGO` | Lo planeado existe. Las brechas son de alcance, de despliegue o defectos nuevos |
| 25 | La prueba de la fase 6 dejó «un respaldo manual en un destino local y uno S3» (`plan-backend-paridad-legacy.md` §C.6, estado) | `NO_VERIFICADA` | Prueba local con `s3mock` sin informe de QA; no hay ejecución con S3 real |

**Totales:** `CONFIRMADA_EN_CODIGO` 14 · `INCOMPLETA` 6 · `OBSOLETA` 2 · `CONTRADICHA_POR_CODIGO` 2 · `NO_VERIFICADA` 1 (25 afirmaciones).

## 6. Incertidumbres

- **`cron.php`:** el checkout no tiene `crontab`. Que corra por cron se infiere del nombre.
- **Productos de Colmotores en la migración:** la consulta de productos no filtra a Colmotores (`plan-backend-paridad-legacy.md:2846`). Sin `db_legacy/` no se pudo saber si entraron modelos de vehículo al catálogo.
- **Volcado del corte real:** no se sabe si habrá depósitos vivos con el mismo número de años distintos (BR-08-005) ni cuántas operaciones abiertas habrá (BR-08-004).
- **Producción:** sin definir el almacenamiento (Local o nube), el número de instancias ni el dominio. De eso dependen BR-08-001, 002 y 012.
- **Portal:** no hay datos de uso que digan si las agencias lo usaban.
- **Despliegue:** `estado.md` §3 lista commits posteriores al último despliegue registrado. La auditoría es del código en disco, no de lo desplegado.

## 7. Lo que quedó sin analizar y por qué

- **Lógica de los jobs** de facturación (módulo 06) y de abandono (módulo 04). Aquí solo se revisó la infraestructura. El directorio del módulo 06 no existía al cerrar este informe, así que no hubo contraste. Con el 04 no hay contradicción (`modulos/04-ce-ingresos-depositos/05-analisis-v2.md:114`).
- **Contenido del reporte de agencias** (`CF-L229`, módulo 07) y servicio de TRM de la DIAN (módulo 06).
- **Implementación SMTP de `EmailService`**, **Terraform de Azure** salvo las líneas de almacenamiento, y **herramientas de video** (`Frontend/wms/tools/video-tutoriales`). No hacían falta para la paridad y en parte están cerca de secretos.
- **Datos reales:** `db_legacy/` está prohibido; los conteos se toman de los informes de migración.
