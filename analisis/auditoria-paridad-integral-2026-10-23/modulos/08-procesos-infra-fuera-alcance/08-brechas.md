# 08-procesos-infra-fuera-alcance — 08 Brechas

> AG-08 · 2026-10-23 · Estático. **Prefijos:** `L/` = `bodegas-legacy/`; `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`; `D/` = `docs/`.
> **Antes de registrar se revisaron:** `D/qa/resultados/defectos/INDICE.md` (153 fichas; DEF-F3-001 y DEF-F11-020, Verificadas, siguen corregidas en el código: `B/Wms.Infrastructure/Persistence/SeedDataExtensions.cs:99`, `BackupService.cs:55,118,297-310`), `D/planes/migracion-staging/resultados/defectos/DEF-MIG-001…008` (Verificadas), las observaciones O-1, O-2 y O-3 de los informes de migración y `D/contexto/estado.md` §4.
> **No se registran como brecha** porque ya están pendientes: FOB/CIF de la migración (`estado.md` §4 n.º 8), el corte real (n.º 7), vaciar staging (n.º 6), la baja de Azure test (n.º 9) y la publicación de los videos (n.º 10). Tampoco las diferencias con decisión (`DIFERENCIA_INTENCIONAL`), ni las posiciones de bodega no migradas (ya es BR-03-006).

## Resumen

| ID | ID funcional | Título | Categoría | Criticidad |
| --- | --- | --- | --- | --- |
| BR-08-001 | CF-L004, CF-V080, CF-V080.a, CF-V080.d | Respaldos sin copia fuera del servidor y con aviso de fallo solo en la aplicación | VALIDACION_PENDIENTE | ALTA |
| BR-08-002 | CF-L004, CF-V080, CF-V080.b | La copia de los archivos subidos depende de `Storage:Type`; Azure test sin respaldo | PROCESOS_AUTOMATICOS | BAJA |
| BR-08-003 | CF-V081, CF-V081.a, CF-V081.e | La prórroga del legacy no se migra | PERSISTENCIA | MEDIA |
| BR-08-004 | CF-V081, CF-V081.e | Sin procedimiento para las operaciones en curso al corte | VALIDACION_PENDIENTE | MEDIA |
| BR-08-005 | CF-V081, CF-V081.a, CF-V081.c | Dos depósitos vivos con el mismo número legacy no se pueden migrar | PERSISTENCIA | MEDIA |
| BR-08-006 | CF-V081, CF-V081.e | El número legacy del depósito no se ve ni se busca | FRONTEND | BAJA |
| BR-08-007 | CF-V081, CF-V081.c | La conciliación tras operar marca los levantes nuevos y la recarga de depósitos sale como error | BACKEND | BAJA |
| BR-08-008 | CF-L217, CF-L217.b | Las agencias de aduanas pierden la consulta propia de sus ingresos | REGLAS_NEGOCIO | MEDIA |
| BR-08-009 | CF-V087 | Correo de avisos con hora UTC y rol «Users» | BACKEND | BAJA |
| BR-08-010 | CF-V082 | Cliente SignalR sin reintento del arranque; avisos sin enlace | INTEGRACION | BAJA |
| BR-08-011 | CF-V085 | Sin endpoint de salud; `GET system/dian-trm/today` sin consumidor ni decisión | CONTRATOS_API | BAJA |
| BR-08-012 | CF-V086 | Jobs sin interruptor, sin hora fija en facturación y sin bloqueo entre instancias | PROCESOS_AUTOMATICOS | BAJA |
| BR-08-013 | CF-V081 | La importación de ciudades solo lee UTF-8 | BACKEND | BAJA |
| BR-08-014 | CF-V082 | Los avisos se listan del más antiguo al más reciente | BACKEND | MEDIA |

Por criticidad: CRÍTICA 0 · ALTA 1 · MEDIA 5 · BAJA 8 (total 14).

---

## BR-08-001 · Respaldos sin copia fuera del servidor y con aviso de fallo solo en la aplicación

- **ID funcional:** CF-L004, CF-V080, CF-V080.a, CF-V080.d.
- **Descripción:** el código permite destinos Local y S3, como manda P14. Pero en staging, y en la plantilla de producción, el único destino es una carpeta del mismo servidor. Si falla un respaldo, solo se avisa dentro de la aplicación.
- **Comportamiento esperado:** una política de producción con al menos una copia fuera del servidor y un aviso de fallo que llegue aunque nadie abra el sistema (`L/docs/legacy_analysis/ROADMAP.md:29`, fase 0.3: «definir la política de respaldo de producción»).
- **Comportamiento actual:**
  - destino `local-staging` en `/opt/wms/backups` (`D/planes/migracion-staging/resultados/informe-fase-5.md:57`), montado desde el mismo host (`B/deploy/staging/compose.staging.yaml:91-92`);
  - la plantilla de producción repite un destino Local en `/opt/wms/backups` con el dominio por definir (`B/deploy/postman/produccion.postman_environment.json`);
  - S3 nunca se configuró fuera de la prueba con `s3mock` de la fase 6;
  - el aviso de fallo usa `sendEmail: false` (`B/Wms.Application/Administration/Backups/Common/BackupService.cs:281`).
- **Capa:** configuración del despliegue (el código cumple P14), más una línea de backend para el correo.
- **Categoría:** VALIDACION_PENDIENTE.
- **Evidencia:** las citadas; `B/deploy/staging/README.md:197-203` (cómo configurar S3); `S3BackupTarget.cs:12,39-40`.
- **Impacto:** si se pierde el disco o la instancia, se pierden a la vez la base, los archivos y todos los respaldos.
- **Criticidad:** ALTA. No impide operar hoy, pero en producción pondría en riesgo todos los datos ante una sola falla. No es CRÍTICA porque staging es un ambiente de pruebas y el código ya soporta la solución.
- **Dependencias:** decisión de infraestructura de producción (`estado.md` §4 n.º 9 sobre Azure; dominio de producción por definir).
- **Acción recomendada:** registrar un destino S3, o de un proveedor compatible, en otra cuenta o región; activar el correo del aviso de fallo, o monitorear `GET administration/backups/runs`; escribir la política de producción.
- **Criterio verificable de resolución:** `GET administration/backups/runs` muestra una corrida diaria con dos destinos `Succeeded`, uno de ellos fuera del servidor, y un fallo provocado llega por correo al administrador.

## BR-08-002 · La copia de los archivos subidos depende de `Storage:Type`; Azure test sin respaldo

- **ID funcional:** CF-L004, CF-V080, CF-V080.b.
- **Descripción:** el `tar.gz` de archivos se arma solo si `Storage:Type = Local` (`B/Wms.Infrastructure/Services/Backups/PgDumpRunner.cs:74-88`). Con almacenamiento en la nube, la aplicación no respalda los archivos y nada documenta quién lo hace. El ambiente Azure test no activa el respaldo (`B/infra/main.tf:112-114`, sin `Backups__*`).
- **Comportamiento esperado:** ROADMAP 0.3 incluye explícitamente «PostgreSQL y `wwwroot/uploads`». El respaldo debe cubrir los archivos sea cual sea el almacenamiento, o el runbook debe decir quién los respalda.
- **Comportamiento actual:** staging (Local) sí los cubre. Con S3 o Azure Blob, ni el código ni la documentación los cubren.
- **Capa:** configuración y documentación.
- **Categoría:** PROCESOS_AUTOMATICOS.
- **Evidencia:** las citadas; `B/Wms.Infrastructure/Services/StorageService.cs:24-25` (tipos `Local`, `AzureBlob`, `AWS-S3`).
- **Impacto:** bajo hoy, porque staging es Local y Azure test se va a dar de baja.
- **Criticidad:** BAJA.
- **Dependencias:** BR-08-001; baja de Azure test.
- **Acción recomendada:** documentar en `B/deploy/staging/README.md` qué cubre el respaldo para cada tipo de almacenamiento, y activar el versionado o la replicación del bucket si se usa uno.
- **Criterio verificable de resolución:** el runbook declara la cobertura de archivos por tipo de almacenamiento, y Azure test está dado de baja o tiene `Backups__Enabled`.

## BR-08-003 · La prórroga del legacy no se migra

- **ID funcional:** CF-V081, CF-V081.a, CF-V081.e (efecto en CF-L140 del módulo 04).
- **Descripción:** el legacy marca la prórroga en `deposito.prorroga` (`L/bodegas_schema.sql:272`; `L/modulos/mod_depositos/registrarprorroga.php:39`) y con ella extiende el plazo de abandono a 60 días (RN-024; `L/menus/evaluaabandonos.php:10-12`). El CSV de depósitos no trae esa columna (`D/planes/paridad-legacy/plan-backend-paridad-legacy.md:2884-2887`) y el importador no registra `ExtensionRegisteredAt`.
- **Comportamiento esperado:** un depósito migrado con prórroga en el legacy tiene plazo de 60 días en V2 y no admite otra prórroga.
- **Comportamiento actual:** V2 lo trata como depósito sin prórroga: plazo de 30 días (`B/Wms.Application/ForeignTrade/Common/Services/AbandonmentCalculator.cs:29-44`). Además, `RegisterExtension` deja registrar una segunda (`B/Wms.Domain/Entities/ForeignTrade/ImportWarehouseStorage.cs:34,128-139`).
- **Capa:** backend (importador) y consulta de exportación.
- **Categoría:** PERSISTENCIA.
- **Evidencia:** búsqueda `prorroga` y `Extension` en `B/Wms.Application/Administration/LegacyImport/`: sin resultados. Columnas de `LegacyDepositRowParser` en `Common/LegacyDepositRowParser.cs:52`.
- **Impacto:** alertas y estado de abandono falsos en los depósitos migrados que estén entre el día 30 y el 60 con prórroga, y riesgo de una segunda prórroga sin respaldo aduanero. En el corte simulado no se notó porque los depósitos vivos eran de 2022 a 2024 (67 en abandono, `D/qa/resultados/F11-informe-S6-2026-10-06.md:202`).
- **Criticidad:** MEDIA. Afecta un control aduanero en un escenario específico (migrados recientes con prórroga).
- **Dependencias:** corte real (`estado.md` §4 n.º 7); módulo 04 (abandono).
- **Acción recomendada:** agregar `prorroga` (y su fecha, si existe) a la consulta y al CSV de depósitos, y registrar la prórroga en `ImportWarehouseStorage` al migrar.
- **Criterio verificable de resolución:** una prueba de importación con `prorroga = 1` deja `HasExtension = true`. Ese depósito aparece con plazo de 60 días en `GET foreign-trade/abandonment`, y `RegisterExtension` responde 409.

## BR-08-004 · Sin procedimiento para las operaciones en curso al corte

- **ID funcional:** CF-V081, CF-V081.e.
- **Descripción:** la importación cubre maestros, saldos vivos y levantes (P13). No hay importador ni procedimiento escrito para lo que esté a medias el día del corte: órdenes de cargue o salidas registradas sin despachar, cobros de báscula «por facturar» (`L/modulos/mod_bascula/cobrarcartera.php`, menú «Cobros Pendientes» en `L/menus/menuizquierda.php:201`) y facturas emitidas con saldo.
- **Comportamiento esperado:** `ROADMAP.md:27` (0.1) pide contar «órdenes y guías abiertas» y «períodos sin facturar», y el plan del corte real debe decir qué se hace con cada una: cerrarlas en el legacy antes del corte, recrearlas a mano en V2 o importarlas.
- **Comportamiento actual:** `LegacyImportEntity` no tiene esas entidades (`B/Wms.Domain/Enums/LegacyImportEntity.cs:7-20`). El orden del corte (`D/planes/migracion-staging/plan-migracion-legacy-staging.md` §3.4) no las menciona. Lo despachado parcialmente sí entra, como `salen` en el saldo.
- **Capa:** proceso de migración.
- **Categoría:** VALIDACION_PENDIENTE.
- **Evidencia:** las citadas; búsqueda «abiertas», «en curso», «cartera», «por facturar» en `D/planes/migracion-staging/`: solo la limpieza de operaciones de QA (`plan-migracion-legacy-staging.md:172`).
- **Impacto:** en la ventana del corte, una orden a medio cargar o un cobro pendiente puede perderse o duplicarse.
- **Criticidad:** MEDIA. Afecta escenarios específicos del día del corte, no la operación diaria.
- **Dependencias:** corte real (`estado.md` §4 n.º 7).
- **Acción recomendada:** agregar al plan del corte un paso de «congelamiento»: inventario de operaciones abiertas en el legacy, y para cada tipo la acción (cerrar antes del corte o recrear en V2) con su responsable.
- **Criterio verificable de resolución:** el plan del corte real lista las operaciones abiertas por tipo con su tratamiento, y el informe del corte las concilia en cero.

## BR-08-005 · Dos depósitos vivos con el mismo número legacy no se pueden migrar

- **ID funcional:** CF-V081, CF-V081.a, CF-V081.c.
- **Descripción:** el legacy reinicia la numeración cada año (DEF-MIG-002: 9.682 depósitos con 4.755 números). El plan admite que puede haber «dos depósitos vivos con el mismo número de años distintos» (`D/planes/paridad-legacy/plan-backend-paridad-legacy.md:2983`), pero solo lo resuelve en el orden de la consulta. El importador agrupa las filas por `nro_deposito` (`B/Wms.Application/Administration/LegacyImport/Importers/DepositsImporter.cs:73`) y `legacy_number` es único (`B/Wms.Infrastructure/Persistence/Configurations/Warehouse/WarehouseStorageConfiguration.cs:54-57`).
- **Comportamiento esperado:** los dos depósitos se migran como distintos y se concilian cada uno con el suyo.
- **Comportamiento actual:** las filas de los dos se mezclan en un grupo y se rechazan juntas («los datos del depósito … no coinciden», `:93-96`, o «producto repetido», `:154-157`). La conciliación y los levantes también buscan por número (`Commands/ReconcileDeposits/ReconcileDepositsCommand.cs:78-83`; `Importers/ReleasesImporter.cs:96`).
- **Capa:** backend y esquema.
- **Categoría:** PERSISTENCIA.
- **Evidencia:** las citadas. En el volcado de junio de 2024 no ocurrió: 128 de 128 migrados (`D/planes/migracion-staging/resultados/informe-fase-3.md:99`).
- **Impacto:** con un volcado nuevo, un depósito vivo de un año anterior con el mismo número que uno del año en curso quedaría sin migrar. La simulación lo mostraría, pero sin camino para cargarlo.
- **Criticidad:** MEDIA. Es un caso específico, detectable, que bloquea la migración de esos depósitos.
- **Dependencias:** corte real.
- **Acción recomendada:** antes del corte, contar en el volcado nuevo los números repetidos entre vivos. Si hay, identificar el depósito por número y año (por ejemplo, `legacy_number = AAAA-BA0042`) en la consulta, el importador, la conciliación y los levantes.
- **Criterio verificable de resolución:** una prueba con dos depósitos vivos `BA0042` de años distintos migra los dos, con sus levantes, y la conciliación da `Ok` para cada uno.

## BR-08-006 · El número legacy del depósito no se ve ni se busca

- **ID funcional:** CF-V081, CF-V081.e.
- **Descripción:** el backend guarda `legacy_number`, pero ningún DTO lo expone y ninguna búsqueda lo usa. `ROADMAP.md:113` (6.3) pedía conservarlo «como referencia». El plan frontend lo dejó como hallazgo, no como decisión (`D/planes/paridad-legacy/plan-frontend-paridad-legacy.md:2327,2699`, §G.12).
- **Comportamiento esperado:** durante la transición, el operario puede buscar un depósito migrado por el número que tiene en sus papeles y etiquetas del legacy.
- **Comportamiento actual:** «Buscar BA0042 → No se encontraron depósitos» (FA-MIG-010, `D/planes/migracion-staging/resultados/informe-fase-1.md:165`, «PASA con nota conocida»).
- **Capa:** backend (DTO, filtros) y frontend.
- **Categoría:** FRONTEND.
- **Evidencia:** búsqueda `LegacyNumber` en `B/Wms.Application` fuera de `LegacyImport`: sin resultados. Búsqueda `legacyNumber` en `F/`: sin resultados.
- **Impacto:** el operario tiene que traducir a mano el número legacy al de la v2 (`2024BA00002` para `BA0042`).
- **Criticidad:** BAJA.
- **Dependencias:** ninguna.
- **Acción recomendada:** confirmar con el negocio. Si aplica, mostrar el número legacy en el detalle y aceptarlo en la búsqueda de depósitos.
- **Criterio verificable de resolución:** decisión registrada, o la búsqueda «BA0042» devuelve el depósito migrado y su detalle muestra el número legacy.

## BR-08-007 · La conciliación tras operar marca los levantes nuevos y la recarga de depósitos sale como error

- **ID funcional:** CF-V081, CF-V081.c.
- **Descripción:**
  - (a) `DepositReconciler` exige que lo nacionalizado de V2 sea igual al legacy (`B/Wms.Application/Administration/LegacyImport/Common/DepositReconciler.cs:58-60`) y no descuenta los levantes registrados después de migrar, como sí hace con los movimientos de stock. Es la observación O-2 (`D/planes/migracion-staging/resultados/informe-fase-1-repeticion.md`, §6).
  - (b) La segunda carga de un depósito ya migrado se informa como error de fila, no como omitido (`Importers/DepositsImporter.cs:83-85`; `informe-fase-1.md:122`).
- **Comportamiento esperado:** la conciliación distingue un descuadre de una operación nueva, y la recarga idempotente se informa como «omitido», igual que en las demás entidades.
- **Comportamiento actual:** sale `Difference` con un levante nuevo, y los errores de la recarga se mezclan con los reales.
- **Capa:** backend.
- **Categoría:** BACKEND.
- **Evidencia:** las citadas.
- **Impacto:** bajo, porque la conciliación se usa el día del corte, antes de operar. Puede confundir si se repite después.
- **Criticidad:** BAJA.
- **Dependencias:** ninguna.
- **Acción recomendada:** informar los levantes de V2 posteriores a la migración (como `v2MovementsSinceMigration`) y contar los depósitos ya migrados como `skipped`.
- **Criterio verificable de resolución:** con un levante nuevo, la fila sale `Ok` con el levante informado, y la recarga del CSV de depósitos da `skipped = filas` y `errors = 0`.

## BR-08-008 · Las agencias de aduanas pierden la consulta propia de sus ingresos

- **ID funcional:** CF-L217, CF-L217.b (contenido: CF-L229, módulo 07).
- **Descripción:** el portal `reportesweb` tenía dos tipos de usuario: «Colmotores» e «Intermediarios» (`L/reportesweb/mod_usuarios/registrarusuario.php:237-239`). El segundo, una agencia de aduanas, consultaba por sí mismo los ingresos de su SIA con productos, pesajes, novedades, guías y salidas (`L/reportesweb/entrada.php:5-6`; `reportesias.php:37-53`; `reportesiasdetalle.php:37,310-413`). Es el único dato no Colmotores del portal. La v2 lo da como reporte interno para Admin y Comercio Exterior (`B/Wms.Api/Controllers/v1/CustomsAgencyReportsController.cs:17-18`; `F/pages/reports/customs-agency-entries.vue:18`).
- **Comportamiento esperado:** el negocio decide si las agencias necesitan autoservicio o si basta con que Comercio Exterior les envíe el reporte.
- **Comportamiento actual:** sin acceso externo. La exclusión de CF-L217 se hizo como «acceso, autenticación y roles» (`L/docs/legacy_analysis/MIGRATION_MATRIX.md:265`). `DECISIONES_REVISION.md` §2.A.1 (`:17`) pide «el reporte», no el portal.
- **Capa:** alcance (frontend, backend y modelo de usuarios).
- **Categoría:** REGLAS_NEGOCIO.
- **Evidencia:** las citadas; `L/bodegas_schema.sql:1685-1699` (`usuariocliente` con `id_sia`, sin `id_cliente`); búsqueda `portal`, `usuariocliente`, `CustomerPortal`, `ClientUser` en B/ y F/: solo comentarios.
- **Impacto:** las agencias que usaban el portal dependerán de Comercio Exterior para ver sus ingresos, lo que agrega carga y demora.
- **Criticidad:** MEDIA. Es una función secundaria, para usuarios externos, y hay alternativa interna.
- **Dependencias:** permisos (DEC-030 y DEC-031: hoy no hay rol externo).
- **Acción recomendada:** confirmar con el negocio y registrar la decisión. Si se necesita autoservicio, evaluar un rol de solo lectura filtrado por agencia en una versión posterior.
- **Criterio verificable de resolución:** decisión en `D/contexto/decisiones.md`, o un usuario de agencia que vea solo sus ingresos.

## BR-08-009 · Correo de avisos con hora UTC y rol «Users»

- **ID funcional:** CF-V087.
- **Descripción:** los correos de `NotificationService` escriben la fecha con `DateTimeOffset.UtcNow` y la etiqueta «UTC» (`B/Wms.Infrastructure/Services/NotificationService.cs:124,201,298,403,490,594`). `NotifyUsersAsync` envía el correo como si fuera del rol «Users» (`B/Wms.Api/Services/NotificationOrchestrator.cs:52-60`), y todo correo va a la misma lista `Notifications:AdminEmails` (`NotificationService.cs:30-33,619-635`).
- **Comportamiento esperado:** fechas en hora de Colombia (`D/contexto/convenciones-tecnicas.md:32`: `DateTimeOffset.UtcNow` solo en `CreatedAt` y `UpdatedAt`) y asunto con el rol real o el destinatario.
- **Comportamiento actual:** el administrador recibe «12/10/2026 02:15 UTC» por un evento de las 21:15 del día anterior, y asuntos «[Users]».
- **Capa:** backend.
- **Categoría:** BACKEND.
- **Evidencia:** las citadas.
- **Impacto:** confusión en la lectura de los avisos.
- **Criticidad:** BAJA.
- **Dependencias:** ninguna.
- **Acción recomendada:** usar `ColombiaTime.Now` y pasar el rol o el usuario real al servicio de correo.
- **Criterio verificable de resolución:** un aviso con correo muestra la hora de Colombia y el asunto del rol real.

## BR-08-010 · Cliente SignalR sin reintento del arranque; avisos sin enlace

- **ID funcional:** CF-V082.
- **Descripción:**
  - Si el primer `connection.start()` falla (API caído al iniciar sesión, red), la conexión queda nula y no se reintenta hasta un nuevo inicio de sesión (`F/plugins/signalr.client.ts:58-64,82-92`).
  - La escucha `ReceiveNotification` se intenta adjuntar solo 5 veces en 5 s (`F/features/users/composables/useNotifications.ts:82-96`).
  - No hay sondeo de respaldo.
  - La notificación no enlaza la entidad (§G.13 del plan frontend; F7-NOT-007 OBS).
- **Comportamiento esperado:** la conexión se recupera sola y el aviso lleva a su objeto.
- **Comportamiento actual:** la reconexión automática funciona solo si la conexión llegó a abrirse (F7-NOT-009 PASA). Si nunca abrió, no hay avisos en vivo hasta recargar o volver a iniciar sesión.
- **Capa:** frontend.
- **Categoría:** INTEGRACION.
- **Evidencia:** las citadas; `D/qa/resultados/F7-informe-2026-10-03.md:78,80`.
- **Impacto:** un usuario puede quedarse sin avisos en vivo sin saberlo. Los avisos persisten y se ven en la página.
- **Criticidad:** BAJA.
- **Dependencias:** ninguna.
- **Acción recomendada:** reintentar `startConnection` con espera exponencial y volver a adjuntar la escucha al crear una conexión nueva. Evaluar los enlaces por `relatedEntityType`.
- **Criterio verificable de resolución:** con el API caído al iniciar sesión y levantado después, el usuario recibe el siguiente aviso en vivo sin recargar.

## BR-08-011 · Sin endpoint de salud; `GET system/dian-trm/today` sin consumidor ni decisión

- **ID funcional:** CF-V085.
- **Descripción:** no hay endpoint de salud del API (búsqueda `AddHealthChecks`, `MapHealthChecks`, `/health` en `B/`: sin resultados). El contenedor del API no tiene `healthcheck` (`B/deploy/staging/compose.staging.yaml:26-94`; solo Postgres, `:20-24`). La prueba de humo se apoya en el 400 del login (`B/scripts/deploy-staging.sh:209-223`). El único endpoint de `SystemController`, la TRM del día (`B/Wms.Api/Controllers/v1/SystemController.cs:18-44`), no tiene consumidor en `F/` ni una decisión que lo justifique (DF3 no lo cubre).
- **Comportamiento esperado:** un `/health` que compruebe la base y que el orquestador o el monitoreo usen. Cada endpoint, con consumidor o con una decisión de dejarlo por API.
- **Comportamiento actual:** un API colgado, con los jobs detenidos, no lo detecta nada automático.
- **Capa:** backend y despliegue.
- **Categoría:** CONTRATOS_API.
- **Evidencia:** las citadas.
- **Impacto:** detección tardía de caídas; código sin uso.
- **Criticidad:** BAJA.
- **Dependencias:** BR-08-012.
- **Acción recomendada:** agregar `AddHealthChecks` con la base y un `healthcheck` en compose. Decidir si `dian-trm/today` se usa (por ejemplo, en Facturación) o se retira.
- **Criterio verificable de resolución:** `GET /health` responde 200 con la base arriba y 503 sin ella, y la decisión sobre `dian-trm/today` queda escrita o el endpoint tiene consumidor.

## BR-08-012 · Jobs sin interruptor, sin hora fija en facturación y sin bloqueo entre instancias

- **ID funcional:** CF-V086.
- **Descripción:**
  - De los 6 jobs, solo el de respaldo tiene interruptor (`Backups:Enabled`, `B/Wms.Api/BackgroundJobs/DatabaseBackupBackgroundService.cs:22-26`).
  - `OverdueDetection`, `InvoicePaymentReconciliation` e `InvoiceDueNotification` corren 30–60 s después de cada arranque y luego cada 24 h desde ese momento, sin hora de Colombia (`OverdueDetectionBackgroundService.cs:10-25`; `InvoicePaymentReconciliationBackgroundService.cs:14-29`; `InvoiceDueNotificationBackgroundService.cs:10-26`).
  - Ninguno se protege contra varias instancias, salvo el registro de la corrida del respaldo (`BackupService.cs:297-310`).
- **Comportamiento esperado:** cada job se puede apagar por configuración y corre a una hora conocida. Si el API se escala, corre una sola vez.
- **Comportamiento actual:**
  - cada redespliegue mueve la hora de los jobs de facturación;
  - con dos instancias, los avisos de mora, vencimiento y abandono podrían duplicarse; los avisos de vencimiento y abandono tienen marcas de idempotencia, pero dos corridas simultáneas podrían pasar las dos;
  - para apagar un job hay que tocar el código.
- **Capa:** backend.
- **Categoría:** PROCESOS_AUTOMATICOS.
- **Evidencia:** las citadas; `B/Wms.Api/Program.cs:77-82`.
- **Impacto:** bajo con la instancia única de staging; relevante si producción usa App Service con escalado.
- **Criticidad:** BAJA.
- **Dependencias:** decisión de infraestructura de producción; la lógica de cada job es de los módulos 04 y 06.
- **Acción recomendada:** agregar `Jobs:<Nombre>:Enabled`, anclar los jobs diarios a una hora de Colombia, como el de abandono, y usar un `pg_advisory_lock` por job o garantizar una sola instancia.
- **Criterio verificable de resolución:** con `Jobs:OverdueDetection:Enabled = false` el job no corre. Dos instancias simultáneas ejecutan cada job una sola vez por día.

## BR-08-013 · La importación de ciudades solo lee UTF-8

- **ID funcional:** CF-V081 (paso 1 del corte; la pantalla es del módulo 01).
- **Descripción:** `POST administration/cities/import` lee el archivo con `StreamReader(stream, Encoding.UTF8)` (`B/Wms.Api/Controllers/v1/CitiesController.cs:117`). El importador común detecta UTF-8 o Windows-1252 (`B/Wms.Application/Administration/LegacyImport/Common/LegacyCsvReader.cs:33-46`), porque MySQL exporta `latin1`.
- **Comportamiento esperado:** la misma detección de codificación en todos los CSV del corte.
- **Comportamiento actual:** un CSV de ciudades en Windows-1252 entra con caracteres de reemplazo en «Ñ» y en las tildes, sin error.
- **Capa:** backend.
- **Categoría:** BACKEND.
- **Evidencia:** las citadas. En la migración, el exportador generó UTF-8 y no hubo mojibake (`D/planes/migracion-staging/resultados/informe-fase-1.md:48,57`).
- **Impacto:** bajo, porque el procedimiento ya exporta en UTF-8.
- **Criticidad:** BAJA.
- **Dependencias:** ninguna.
- **Acción recomendada:** leer los bytes y decodificar con `LegacyCsvReader`.
- **Criterio verificable de resolución:** un CSV de ciudades en Windows-1252 con «NARIÑO» se importa como «NARIÑO».

## BR-08-014 · Los avisos se listan del más antiguo al más reciente

- **ID funcional:** CF-V082.
- **Descripción:** `GetNotificationsHandler` ordena por `CreatedAt` y `Id` ascendentes (`B/Wms.Application/Users/Queries/GetNotifications/GetNotificationsHandler.cs:35-36`). El panel pide la página 1 de 15 (`F/features/users/composables/useNotifications.ts:15,35-45`) y la página `/notifications` empieza también en la página 1 (`F/features/users/composables/useNotificationsPage.ts:17`). Ninguno reordena en el cliente (`F/features/users/components/NotificationPanel.vue:116`).
- **Comportamiento esperado:** los avisos más recientes primero, como en cualquier bandeja.
- **Comportamiento actual:** con más de 15 avisos, el panel muestra los 15 más viejos y los nuevos no aparecen. Solo el toast en vivo los anuncia, y la página obliga a ir a la última página.
- **Capa:** backend.
- **Categoría:** BACKEND.
- **Evidencia:** las citadas. F7-NOT-006 se marcó PASA sin comprobar el orden (`D/qa/resultados/F7-informe-2026-10-03.md:77`). Admin tenía 17 avisos en esa prueba (`:75`). No hay ficha DEF que lo registre (búsqueda «orden», «antigu», «reciente» en las fichas de notificaciones).
- **Impacto:** los avisos de acción (TRM pendiente, mínimos, vencimientos, abandono) se pierden de vista en el panel, que es el acceso diario.
- **Criticidad:** MEDIA. Degrada una función transversal de uso diario; hay alternativa (página, toast).
- **Dependencias:** ninguna.
- **Acción recomendada:** `OrderByDescending(n => n.CreatedAt).ThenByDescending(n => n.Id)`, con una prueba.
- **Criterio verificable de resolución:** con 20 avisos, `GET user/{id}/notifications?pageIndex=1&pageSize=15` devuelve primero el más reciente, y el panel lo muestra arriba.


---

## Decisiones posteriores (2026-10-23)

> Nota del orquestador. Después de esta auditoría, el usuario respondió las preguntas al negocio (`docs/contexto/decisiones.md`, DEC-050…054; `06-brechas-priorizadas.md` §3.1). El registro de arriba es la foto previa y no se reescribe. El estado vigente está en `06-brechas-priorizadas.md` y `04-matriz-global.csv`.

| Brecha | Estado | Decisión |
| --- | --- | --- |
| BR-08-008 | Cerrada: se acepta el comportamiento de V2 | DEC-054 |
