Eres el implementador de la corrección de **DEF-MIG-008** (ubicaciones de bodega que no reflejan el legacy y datos de ejemplo sembrados) y de una mejora de configuración de staging (las llaves de DataProtection), dentro del plan `docs/planes/migracion-staging/plan-migracion-legacy-staging.md` del WMS de Bodegas Asociadas. Modelo recomendado: **Opus 5.5**: hay que quitar semillas con una migración sin romper pruebas ni ambientes, y cambiar el importador. **Tu trabajo es el código, la migración y el plan de exportación.** La recarga en local y el redespliegue de staging los hace otro agente con `prompt-actualizacion-fases-1-2.md`.

## Lee primero
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. **El plan:** §2 (D1 a D6) y §3 (reglas comunes).
3. **La ficha** `docs/planes/migracion-staging/resultados/defectos/DEF-MIG-008.md` completa, con la pista técnica y la lista de verificación, y `resultados/informe-fase-2.md` §5 (advertencia de DataProtection).
4. **El código:**
   - `Wms.Infrastructure/Persistence/SeedDataExtensions.cs` (todas las semillas) y `AppDbContext.cs` (≈ líneas 260-275, donde se llaman);
   - `Wms.Application/Administration/LegacyImport/Importers/LocationsImporter.cs`, `LegacyIdMapService` y `MasterRowParser` (o el parser de ubicaciones);
   - la entidad de ubicación (`SetAvailability`);
   - `Wms.Api/Program.cs` y la configuración de servicios (para DataProtection).
5. `docs/planes/paridad-legacy/plan-backend-paridad-legacy.md`: F6-02, la consulta de ubicaciones (≈ líneas 2847-2849) y su regla de capacidad 1 (≈ 2679).
6. `deploy/staging/compose.staging.yaml`, `scripts/deploy-staging.sh` (`bootstrap`) y `deploy/staging/README.md`.

Implementa en este orden: **1 → 2 → 3 → 4**.

---

## 1. Quitar las semillas de ejemplo (decisión cerrada)

**Regla:** se quita lo que es **dato de ejemplo** y se conserva lo que es **catálogo del sistema**.

| Semilla | Decisión |
|---|---|
| `SeedWarehouseLocations`: las 20 ubicaciones `A01-R01-N01`, `PATIO-01`, `RECEPCION-01`… | **Se quita.** Las ubicaciones reales llegan por la migración o las crea el Admin. |
| `SeedStandardProducts`: Manteca (Importaciones), Granos, Enlatados, Plátano Seco | **Se quitan.** Los productos reales llegan por la migración. |
| `SeedStandardProducts`: **Contenedor Vacío** (`58557c15-…`) | **Se conserva.** Es funcional: la decisión D2 lo usa para facturar el contenedor vacío con convenio `PER_UOM`. Si quitar el resto obliga a mover este producto a otro método, hazlo sin cambiar su Id ni sus datos. |
| Roles, roles de negocio, impuestos, modalidades, tipos de unidad de carga, unidades de medida, parámetros (incluidos `COMPANY_*`), motivos de ingreso, tipos de documento, tipos de fórmula, servicios, impuestos por servicio y mínimos por modalidad | **Se conservan.** Son catálogo del sistema. |

**Antes de quitar**, busca en todo el código cualquier referencia a los Id o códigos que se van: backend, frontend, pruebas, `ServiceIds`/`ProductIds` y constantes.
- Si el **código de producción** depende de alguno, **detente y repórtalo**.
- Si **solo las pruebas** dependen de alguno (por ejemplo, `CatalogWriteAuthorizationTests.cs:89` con `A01-R01-N01` y `CatalogPatchTests.cs`), cambia esas pruebas para que **creen sus propios datos**. No se reescribe lo que verifican.
- Revisa con el mismo criterio si alguna otra semilla es dato de ejemplo y no catálogo. **Si encuentras otra, no la quites: repórtala** para que decida el usuario.

**Migración.**
- Genera la migración solo con `dotnet ef migrations add RemoveSampleSeedData`. **Nunca edites los archivos generados.**
- Debe contener solo `DeleteData` de las 20 ubicaciones y los 4 productos. Si trae otra cosa, detente y repórtalo.
- Anota en la ficha qué pasa en cada base:
  - en una base limpia (staging después del redespliegue, producción y `wms_migracion` recreada) se aplica sin problema;
  - en una base donde alguna ubicación o producto de ejemplo esté referenciado, el `DeleteData` falla por la FK `Restrict`. Es el caso de **`wmsdb`, la base del QA**: según D6 no se toca, así que **no le apliques la migración**. Queda en la migración anterior como evidencia del QA y, si alguien la quisiera actualizar, tendría que recrearla.

## 2. Ubicaciones del legacy completas y con su estado (decisión cerrada)

**Consulta del plan** (F6-02):
- Cámbiala a un `LEFT JOIN` **desde `bodega`**, para que salgan las **9 bodegas activas**:
  - las 6 con sección: **una fila por sección**, como hoy;
  - las 3 sin sección (Cobertizo, Patio 1 BA y Patio 2 BA): **una fila por bodega**, sin sección.
- Exporta **`S.ocupacion`** como **sexta columna opcional**, `ocupacion`.
- Mantén las exclusiones de hoy (`estado <> 'eliminado'` en las dos tablas y bodegas `colmotores`) y un **orden total**, como en O-1.

**Importador** (`LocationsImporter` y su parser):
- **CSV de 5 columnas:** se sigue aceptando, con el comportamiento de hoy.
- **Fila de bodega sin sección** (`id_seccion` vacío):
  - id legacy **`B{id_bodega}`**, para no chocar con los id de sección en `legacy_id_map`;
  - código = el **nombre de la bodega**;
  - capacidad 1, igual que las demás migradas (decisión de F6-02).
- **`ocupacion = 'deshabilitado'`:** la ubicación se crea y queda **No disponible** con `SetAvailability(false)`. Cualquier otro valor, o vacío, deja la ubicación disponible.
- **Ubicación ya existente** (equivalente por código o ya mapeada): **no se cambia su disponibilidad.** La recarga es idempotente y no pisa lo que haya decidido el Admin en la v2. Anótalo en el resumen de la clase.
- El lote informa cuántas filas fueron de bodega y cuántas de sección.

**Pruebas.**
- Unitarias del parser: 5 y 6 columnas, fila de bodega sin sección y `deshabilitado`.
- Integración:
  - una carga con las 9 filas crea 9 ubicaciones con 0 rechazos, y la `deshabilitado` queda No disponible;
  - la segunda carga no duplica;
  - el CSV de 5 columnas sigue cargando.

## 3. Llaves de DataProtection persistentes (mejora de staging)

**Problema** (informe de la Fase 2 §5): las llaves viven dentro del contenedor y cada redespliegue invalida los enlaces de recuperación de contraseña ya enviados.

**Cambio (cerrado).**
- **Configuración opcional `DataProtection:KeysPath`:**
  - si tiene valor, `AddDataProtection().PersistKeysToFileSystem(...)` en esa carpeta, con un nombre de aplicación fijo (`SetApplicationName("wms-api")`);
  - si no tiene valor, todo queda **como hoy**: local, pruebas y Testcontainers no cambian.
- **En `compose.staging.yaml`:** `DataProtection__KeysPath: "/app/keys"` y el montaje `/opt/wms/data/keys:/app/keys`.
- **En `deploy-staging.sh bootstrap`:** crea `/opt/wms/data/keys` con dueño UID 1654 y modo 700.
- **README:** una línea que explique para qué es la carpeta y que no se borra en los redespliegues.
- **No cifres las llaves con certificado:** queda fuera de alcance para staging. Anótalo en el README como pendiente para producción.

**Prueba.** Unitaria o de integración: con `KeysPath`, las llaves se escriben en la carpeta y una segunda instancia del protector desprotege lo que protegió la primera.

## 4. Plan de migración y QA
- Actualiza §3.5 del plan de migración: la consulta de ubicaciones cambió y el CSV de ubicaciones del conjunto v2 **deja de estar congelado** hasta la recarga.
- En la ficha, deja anotados los casos de QA que nombran ubicaciones de ejemplo: `F1-UBI-003`, `F4-REC-004` y `F4-UBI-003` (`docs/qa/fase-01-administracion.md` y `fase-04-bodega.md`).
  - **No edites esos documentos de QA.**
  - Anota que en la Fase 4 (QA en staging) esos casos usan ubicaciones migradas o creadas como dato QA.

## Sin retrocesos
- **Una base nueva sigue funcionando completa:** catálogo, roles y Contenedor Vacío.
- **Las ubicaciones** se siguen pudiendo crear y editar desde Administración. La recepción y el inventario por ubicación no cambian.
- **La importación de los demás maestros, de los depósitos y de los levantes** no cambia.
- **Pruebas existentes:** pasan. Solo cambian las que dependían de datos de ejemplo, para crear sus propios datos. Lístalas.

## Restricciones (obligatorias)
- Trabaja en `develop` de los dos repos. **No crees ramas ni hagas commits**: entrega los mensajes.
- **No uses `wmsdb`, `wms_migracion`, staging ni producción** para escribir.
  - Puedes leer `legacy-mariadb` para validar la consulta nueva: conteos y nombres de bodegas, que son de la empresa, no de personas.
  - Las pruebas usan Testcontainers.
- **Migraciones solo con `dotnet ef`**, sin editar archivos generados y sin SQL manual.
- No copies secretos ni datos de terceros. Textos y comentarios en español. Nada fuera de este alcance.

## Ficha
En `DEF-MIG-008.md`: **Estado** «Corregido», una fila «Corregido» con el resumen, las pruebas y «commits: pendiente», y la lista de verificación actualizada para el ejecutor.

## Verificación antes de terminar
1. `dotnet build` sin errores ni advertencias nuevas.
2. `dotnet test` de `Wms.Tests` y `Wms.IntegrationTests` en verde (1696 y 289 antes de esta corrección). Reporta los totales.
3. La migración nueva aplicada en Testcontainers. `has-pending-model-changes` sin cambios después de generarla.
4. Si tocaste el frontend: `yarn test`, `yarn build` y `yarn lint` (no más de 279 errores). Revisa en especial si alguna pantalla o prueba esperaba los productos o ubicaciones de ejemplo.
5. `git status`: solo los archivos de este alcance.

## Entrega
Responde con:
1. Los archivos creados o modificados, por punto, y las operaciones de la migración (una por línea).
2. Las referencias a datos de ejemplo que encontraste y cómo las resolviste, y las otras semillas que reportas sin quitar.
3. La consulta nueva de ubicaciones y su resultado contra `legacy-mariadb`: 9 filas, con la `deshabilitado` marcada.
4. El resultado de cada compuerta, con números.
5. **Los mensajes de commit**, listos para pegar, cada uno por separado:
   - **Backend (código y pruebas):** `fix(migracion): ubicaciones del legacy completas y con su estado, sin semillas de ejemplo, y llaves de DataProtection persistentes (DEF-MIG-008)`;
   - **Backend (migración):** `feat(migracion): migración RemoveSampleSeedData`;
   - **Backend (configuración de staging):** `chore(staging): carpeta persistente para las llaves de DataProtection`;
   - **Backend (documentación):** `docs(migracion): consulta de ubicaciones corregida y ficha DEF-MIG-008`, con el plan de paridad, el plan de migración, la ficha y este prompt;
   - **Frontend**, solo si lo tocaste.

   Todos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí.** La recarga en local y el redespliegue de staging los hace otro agente después de que el usuario haga los commits.
