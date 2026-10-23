# Ficha de defecto — DEF-MIG-008

| Campo | Valor |
|---|---|
| ID | DEF-MIG-008 |
| Título | Las ubicaciones de bodega no reflejan el legacy: 20 de ejemplo sembradas, 3 faltantes y estado perdido |
| Severidad | MAJOR |
| Prioridad sugerida | Alta: corregir **antes de la fase 3**, porque cambia el CSV congelado de ubicaciones y el esquema sembrado de staging |
| Módulo | Administración (ubicaciones) / Bodega / migración legacy |
| Caso(s) | OK-1 (carga de ubicaciones), FA-MIG (maestros); revisión de paridad de `/admin/locations` pedida por el usuario el 2026-10-06 |
| Riesgo del plan (§9) | «La herramienta nunca se probó con datos reales (E19)» |
| Ambiente y commits | Staging (base recién creada en la fase 2) y local (`wms_migracion`) · BE `bf2dea6` · FE `4799cc4` |
| Rol / usuario | Admin (`/admin/locations`); Bodega al ubicar mercancía |
| Estado | Verificado |

## Precondiciones y datos
- Legacy `bodegas` (MariaDB `legacy-mariadb`, dump del 2024-06-10).
  - 9 bodegas activas, todas con uso `bodegas` (ids 12-20).
  - **6 de ellas tienen una sección 1×1:** Bodega 1 BA a Bodega 5 BA y Bodega Baja BA.
  - **3 no tienen secciones:** Cobertizo, Patio 1 BA y Patio 2 BA, con `filas = columnas = 0`.
  - La sección de **Bodega 1 BA** (id 4027) tiene `ocupacion = 'deshabilitado'`.
  - Ninguna sección tiene mercancía asignada: `productodetalle_x_seccion` tiene 284 filas, todas `libre`, de 2013.
- Consulta de exportación: la de F6-02 (`docs/planes/paridad-legacy/plan-backend-paridad-legacy.md` ≈ 2847-2849, la misma de `db_legacy/trabajo/consultas/04_ubicaciones.sql`):
  ```sql
  SELECT S.id_seccion, S.nombre, S.fila, S.columna, B.nom_bodega
  FROM seccion S JOIN bodega B ON B.id_bodega = S.id_bodega
  WHERE S.estado <> 'eliminado' AND B.estado <> 'eliminado' AND B.uso <> 'colmotores';
  ```

## Pasos para reproducir
1. Crear una base v2 limpia con las migraciones actuales (`dotnet ef database update` o `staging.sql`).
2. Consultar `warehouse_locations` o abrir `/admin/locations` como Admin.
3. Cargar el CSV de ubicaciones del legacy por `administration/legacy-import` (fase 1).
4. Volver a consultar las ubicaciones y compararlas con `bodega` y `seccion` del legacy.

## Resultado esperado
- **Ubicaciones:** solo las del legacy, sin datos de ejemplo. Las 9 bodegas activas existen, también las que no tienen secciones, porque son espacios físicos reales.
- **Disponibilidad:** igual que en el legacy. Una sección `deshabilitado` llega como **No disponible** (`IsAvailable = false`), como hace `habilitarseccion.php` (RN-046).
- **Sin pérdidas silenciosas:** la conciliación de la migración cuenta todas las bodegas activas.

## Resultado obtenido
1. **20 ubicaciones de ejemplo sembradas.**
   - Una base recién creada ya trae 20: `A01-R01-N01` … `C01-R01-N02`, `PATIO-01`, `PATIO-02`, `RECEPCION-01`, `DESPACHO-01`, `TRANSITO-01` y `CUARENTENA-01`, con capacidades de 4.000 a 7.000.
   - **Verificado en staging el 2026-10-06** (`SELECT count(*) FROM warehouse_locations` → 20, sin datos migrados).
   - Producción las heredaría por la misma migración.
   - En `wms_migracion` quedan 26: 20 de ejemplo y 6 migradas.
2. **Faltan 3 bodegas.** Cobertizo, Patio 1 BA y Patio 2 BA no llegan. El `JOIN` con `seccion` las descarta y la fase 1 reporta «6 filas, 6 creadas, 0 rechazadas» sin avisarlo (`resultados/registro-csv-fase-1.md`, `informe-fase-1-repeticion.md`).
3. **Estado perdido.** `Bodega 1 BA-[1][1]` llega **Disponible**: la consulta no exporta `ocupacion` y el importador crea todas con `IsAvailable = true`.

## Evidencia
- **Staging:** consulta de solo lectura por SSH del 2026-10-06, 20 códigos, los listados en el punto 1.
- **Legacy (solo SELECT):**
  - `bodega`: 20 filas, 9 activas.
  - `seccion`: 4.032 filas, 6 activas, una de ellas `deshabilitado`.
- **Fase 1:** `resultados/registro-csv-fase-1.md:22,72` e `informe-fase-1-repeticion.md:71,84`.

## Impacto
- **Operación:** en `/admin/locations`, en la recepción y en Inventario › Ubicaciones, Bodega ve 20 posiciones que no existen en la bodega de Ipiales, mezcladas con las 6 reales. Puede ubicar mercancía en ellas y el inventario por ubicación queda falso.
- **Producción:** las 20 llegarían igual. Borrarlas a mano después de operar es difícil, porque la FK de la mercancía ubicada es `Restrict` y responde 409.
- **Paridad:** faltan 3 espacios físicos (los patios y el cobertizo), y una sección deshabilitada queda habilitada.
- **Lo que no afecta:** stock, saldos, levantes ni facturación. Ningún importador asigna ubicación a los depósitos y en el legacy no hay mercancía ubicada.

## Pista técnica (opcional)
1. **Quitar las de ejemplo.**
   - El sembrado está en `Wms.Infrastructure/Persistence/SeedDataExtensions.cs:396-644` (`SeedWarehouseLocations`, `HasData`), y lo llama `AppDbContext.cs:269`.
   - Quitar la llamada y el método genera, con `dotnet ef migrations add`, un `DeleteData` de los 20 Id. No hay que editar los archivos generados.
   - Ese `DeleteData` falla en una base donde alguna esté referenciada (mercancía ubicada o ubicación principal). Es el caso de la base de QA `wmsdb`, que según D6 no se toca. Staging y producción llegan limpias.
   - Revisar si las otras semillas de ejemplo (`SeedDataExtensions`) también tienen que salir de un ambiente real.
2. **Exportar todas las bodegas y su estado.** Cambiar la consulta a un `LEFT JOIN` desde `bodega`, para que salgan las bodegas sin secciones, y exportar `S.ocupacion`.
   - Las filas sin sección no tienen `id_seccion`. El importador necesita otro id legacy, por ejemplo `B{id_bodega}`, para no chocar en `LegacyIdMapService`, y otro código, por ejemplo el nombre de la bodega.
   - Conviene que la columna nueva sea **opcional**, para que el CSV de 5 columnas siga cargando.
3. **Trasladar el estado.** En `LocationsImporter.ApplyAsync` (`Wms.Application/Administration/LegacyImport/Importers/LocationsImporter.cs`):
   - si `ocupacion = 'deshabilitado'`, crear la ubicación y llamar a `SetAvailability(false)`;
   - con una ubicación ya existente (equivalente por código), decidir si se actualiza o se respeta.
4. **Lo que depende de las semillas:**
   - **Pruebas:** `Wms.IntegrationTests/Security/CatalogWriteAuthorizationTests.cs:89` espera `A01-R01-N01`. `Wms.IntegrationTests/Administration/CatalogPatchTests.cs` usa ubicaciones. Ambas tendrían que crear sus propios datos.
   - **Casos de QA:** `F1-UBI-003`, `F4-REC-004` y `F4-UBI-003` (`docs/qa/fase-01-administracion.md:189`, `fase-04-bodega.md:61,105`) nombran `A01-R01-N01` y `B01-R01-N01`. Habría que crearlas como dato QA o cambiar los casos.
5. **Fuera de alcance (anotado):**
   - Las migradas entran con capacidad 1, que la pantalla muestra como «1 kg». Es una decisión de F6-02 (`plan-backend-paridad-legacy.md:2679`).
   - El comentario del importador dice que la ajusta Comercio Exterior, pero editar ubicaciones es `AdminOnly`.
   - Los rótulos «Pasillo / Rack / Nivel» muestran la bodega, la fila y la columna del legacy.

## Consecuencia para el plan de migración
- **CSV congelado:** el CSV v2 de ubicaciones (`db_legacy/trabajo/csv/`, `sha256-csv-fase-1-v2.txt`) cambia. Hay que regenerarlo, volver a sacar su hash y repetir de la fase 1 al menos la carga y la conciliación de ubicaciones, en una base limpia.
- **Staging:** ya tiene las 20 de ejemplo. Con la migración nueva, el `migrate` de la fase 3 (o un redespliegue previo) las borra, siempre que nadie haya ubicado mercancía en ellas. Mientras tanto no se deben usar.

## Corrección (2026-10-06)

### Qué cambió
1. **Sin semillas de ejemplo.** Salen `SeedWarehouseLocations` (las 20 ubicaciones) y, de `SeedStandardProducts`, Manteca (Importaciones), Granos, Enlatados y Plátano Seco. **Contenedor Vacío** (`58557c15-…`, decisión D2) se queda en el mismo método, con su Id y sus datos. El resto de semillas es catálogo del sistema y no cambia.
2. **Migración `RemoveSampleSeedData`**, generada con `dotnet ef migrations add`, sin editar: solo 24 `DeleteData` (20 en `warehouse_locations` y 4 en `products`).
3. **Consulta de ubicaciones** (F6-02, `plan-backend-paridad-legacy.md`): parte de `bodega` con `LEFT JOIN seccion` y exporta `ocupacion` (6.ª columna) e `id_bodega` (7.ª), con `ORDER BY B.id_bodega, S.id_seccion`.
   - **La 7.ª columna no estaba en el prompt.** Hace falta porque una fila sin sección no trae otro dato para armar el id legacy `B{id_bodega}`. Es opcional, como la 6.ª: solo la exige una fila sin `id_seccion`.
   - Contra `legacy-mariadb` da 9 filas: las 6 secciones `[1][1]` (4027 a 4032; la 4027, de Bodega 1 BA, `deshabilitado`) y Cobertizo, Patio 1 BA y Patio 2 BA sin sección (bodegas 18 a 20).
4. **Importador** (`LocationsImporter`):
   - El CSV de 5 columnas carga igual que antes.
   - Una fila sin `id_seccion` y con `id_bodega` es una bodega sin sección: id legacy `B{id_bodega}`, código y nombre = nombre de la bodega, pasillo = bodega, sin estante ni nivel, capacidad 1 (F6-02).
   - `ocupacion = 'deshabilitado'` (sin distinguir mayúsculas) crea la ubicación No disponible con `SetAvailability(false)`; cualquier otro valor, o vacío, la deja disponible.
   - Una ubicación que ya existe (equivalente por código o ya mapeada) **no cambia su disponibilidad**: la recarga es idempotente y no pisa lo que haya decidido el Admin.
   - El lote deja una nota en la fila 0 de `errors`: «Filas leídas: N de sección y M de bodega sin sección.». No cuenta como fila con error.
5. **Llaves de DataProtection** (mejora de staging, informe de la fase 2 §5): con `DataProtection:KeysPath`, `PersistKeysToFileSystem` + `SetApplicationName("wms-api")`. Sin valor, todo queda como antes. En staging se monta `/opt/wms/data/keys` en `/app/keys`; la carpeta la crea `bootstrap` (UID 1654, modo 700). Sin cifrar con certificado: pendiente para producción.

### La migración en cada base
| Base | Qué pasa |
|---|---|
| Base limpia: staging después del redespliegue, producción y `wms_migracion` recreada | Se aplica sin problema; `warehouse_locations` queda vacía y `products` solo con Contenedor Vacío. |
| Base donde alguna ubicación o producto de ejemplo esté referenciado (mercancía ubicada, ubicación principal, línea de depósito, regla o convenio) | El `DeleteData` falla por la FK `Restrict` y la migración no se aplica. |
| **`wmsdb`, la base del QA** | Es el caso anterior y, según D6, no se toca: **no se le aplica la migración**. Se queda con las migraciones que tiene, como evidencia del QA. Si alguien la quisiera actualizar, tendría que recrearla. |

Staging tiene hoy las 20 de ejemplo. Si nadie ubicó mercancía en ellas, el `migrate` del redespliegue las borra; si alguna estuviera referenciada, el `migrate` falla y la base se recrea (con el «sí» del usuario, regla 8). Hasta entonces no se deben usar.

### Casos de QA que nombran datos de ejemplo
No se editan los documentos de QA. En la Fase 4 (QA en staging), estos casos usan ubicaciones migradas (por ejemplo `Bodega 2 BA-[1][1]` y `Patio 1 BA`) o ubicaciones creadas como dato QA desde Administración:
- `F1-UBI-003` (`docs/qa/fase-01-administracion.md:189`): código duplicado, repite `A01-R01-N01`.
- `F4-REC-004` (`fase-04-bodega.md:61`): ubica la recepción en `A01-R01-N01`.
- `F4-UBI-003` (`fase-04-bodega.md:105`): mueve de `A01-R01-N01` a `B01-R01-N01`.
- También `F4-UBI-001` (`fase-04-bodega.md:103`), que ubica en `B01-R01-N01`; no estaba en la ficha.

Ningún caso de QA nombra los productos de ejemplo que salieron.

### Pruebas
- **Unitarias** (`Wms.Tests`):
  - `MasterRowParserTests`: CSV de 5 columnas, 6 columnas con `deshabilitado`, `libre`, `Libre`, `ocupado` y vacío, bodega sin sección y sus errores.
  - `WmsDataProtectionTests`: con `KeysPath` se escriben las llaves y una segunda instancia desprotege lo que protegió la primera; sin `KeysPath` no se registra nada.
- **Integración** (`Wms.IntegrationTests`, `LegacyLocationsImportTests`):
  - 9 filas → 9 ubicaciones, 0 rechazos, la `deshabilitado` No disponible y el patio con id legacy `B{id}`;
  - la segunda carga omite las 9;
  - el CSV de 5 columnas carga;
  - una ubicación existente por código conserva su disponibilidad.
- **Pruebas que dependían de datos de ejemplo**, cambiadas para crear los suyos sin cambiar lo que verifican:
  - `WmsApiFactory` crea al iniciar los productos de prueba Granos, Manteca (Importaciones) y Enlatados, con los mismos Id, nombres y unidades (`OperationalData.TestProducts`). Los usan `OperationalData`, `AdjustmentScenario`, `ReceptionShortageTests`, `ProductCorrectionNoticeTests`, `GetImportDepositDetailHandlerTests` y `StorageRecalculationDispatchTests`.
  - `CatalogWriteAuthorizationTests.Billing_GetReportLocations_Returns200` crea su propia ubicación en vez de esperar `A01-R01-N01`.
  - `CatalogPatchTests` ya creaba su ubicación: sin cambios.

## Historial
| Fecha | Evento | Build | Por |
|---|---|---|---|
| 2026-10-06 | Detectado al revisar la paridad de `/admin/locations` con el legacy, a pedido del usuario, después del despliegue de la fase 2. Las 20 sembradas se verificaron en staging | BE `bf2dea6` · FE `4799cc4` | Agente ejecutor (Opus 5.5) |
| 2026-10-06 | **Corregido.** Sin semillas de ejemplo: salen las 20 ubicaciones y 4 productos; Contenedor Vacío se queda. Migración `RemoveSampleSeedData`, solo con 24 `DeleteData`. La consulta de ubicaciones parte de `bodega` con `LEFT JOIN` y exporta `ocupacion` e `id_bodega`: 9 filas en el legacy. El importador crea las bodegas sin sección con id `B{id_bodega}`, deja No disponible la sección `deshabilitado`, no cambia la disponibilidad de una ubicación existente y sigue aceptando el CSV de 5 columnas. Llaves de DataProtection persistentes con `DataProtection:KeysPath` (staging: `/opt/wms/data/keys`). Pruebas: `Wms.Tests` 1707 en verde (1696 + 11); `Wms.IntegrationTests` 292 en verde (289 + 3), con la migración nueva aplicada en Testcontainers. Commits: `dd151ed`, `0149648`, `b8bb09e` y `b31ddb6`. | BE `5a72d3b` + cambios sin commit · FE sin cambios | Agente implementador (Opus 5.5) |
| 2026-10-06 | **Verificado.** **Local:** `wms_migracion` recreada con 11 migraciones, sin ubicaciones y con solo Contenedor Vacío; `wmsdb` sin tocar. CSV de ubicaciones con la consulta nueva: 9 filas, 7 columnas, SHA-256 `58e984c2…367d` (conjunto v3). Simulación y firme: 9 creadas, 0 rechazos, «6 de sección y 3 de bodega sin sección». `Bodega 1 BA-[1][1]` No disponible y las otras 8 Disponibles; recarga con 9 omitidas; `/admin/locations` muestra solo las 9. Productos 1.640 (−4 de ejemplo, +1: el legacy 238 «PLATANO SECO», que antes se asociaba al de ejemplo «Plátano Seco» y ahora se crea). Sin cambios en el resto: 133/133 Ok, 128 Opened y primer período de $91.257.475,39. **Staging:** 0 referencias a los 24 Id antes de migrar; `migrate` sin recrear la base (11 migraciones, 0 ubicaciones, solo Contenedor Vacío, Admin y destino de respaldo conservados); `/opt/wms/data/keys` 1654:1654, modo 700, con `key-*.xml`. Un enlace de recuperación emitido antes de reiniciar el API sigue sirviendo después (confirmado por el usuario). Ver `informe-actualizacion-fases-1-2.md` | BE `b31ddb6` (`dd151ed`, `0149648`, `b8bb09e`) · FE `508b91b` | Agente ejecutor (Opus 5.5) |

## Lista de verificación para la re-ejecución
La ejecuta el agente de `prompt-actualizacion-fases-1-2.md`, después de que el usuario haga los commits.
- [x] Base limpia con las migraciones nuevas (incluida `RemoveSampleSeedData`): `warehouse_locations` vacía y `products` solo con Contenedor Vacío.
- [x] `wmsdb` no se toca: no se le aplica la migración (D6).
- [x] La consulta nueva de `plan-backend-paridad-legacy.md` (F6-02) se guarda en `db_legacy/trabajo/consultas/` y exporta 9 filas con 7 columnas: 6 con sección y 3 sin sección.
- [x] La simulación y la carga crean 9 ubicaciones con 0 rechazos, y el lote dice «6 de sección y 3 de bodega sin sección». `Bodega 1 BA-[1][1]` queda No disponible; las demás, incluidos Cobertizo, Patio 1 BA y Patio 2 BA, Disponibles.
- [x] Al recargar el mismo CSV no se duplica nada: 9 omitidas (OK-3).
- [x] El CSV de 5 columnas, el anterior, sigue cargando. (Cubierto por `LegacyLocationsImportTests`; no se repitió con datos reales.)
- [x] Las pruebas de integración pasan sin depender de `A01-R01-N01` ni de los productos de ejemplo. (Hecho por el implementador: 292 en verde.)
- [x] El CSV de ubicaciones queda con hash nuevo y anotado en el registro de CSV; el resto del conjunto v2 sigue congelado.
- [x] Staging redesplegado: 0 ubicaciones antes de la fase 3, `/opt/wms/data/keys` creada por `bootstrap` con UID 1654 y modo 700, y con archivos `key-*.xml` después del arranque. Un enlace de recuperación de contraseña emitido antes de otro redespliegue sigue sirviendo. (Probado con un reinicio del API: el enlace sigue sirviendo, confirmado por el usuario.)
- [x] **Staging, F11-S6 (2026-10-07):** la recepción y la ubicación en «Bodega 1 BA-[1][1]» → 409 «La ubicación Bodega 1 BA-[1][1] está deshabilitada.». Recepción en «Bodega 2 BA» y «Patio 1 BA», ubicar en «Cobertizo» y mover a «Bodega 3 BA» → 200. Inventario › Ubicaciones lista las 9 migradas. Evidencia: `docs/qa/resultados/evidencias/F11/S6-B-roles-qa.txt`.
