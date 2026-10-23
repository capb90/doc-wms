Eres el ejecutor de la **Fase 1 — Migración del legacy en local** del plan `docs/planes/migracion-staging/plan-migracion-legacy-staging.md` del WMS de Bodegas Asociadas. Modelo recomendado: **Opus 5.5**. Es la prueba con datos reales (E19) de la herramienta de importación de la Fase 6 de paridad, que hasta hoy solo se probó con CSV sintéticos.

**Tu trabajo es ejecutar y verificar, no corregir código.** Si la herramienta falla por un defecto, lo documentas como ficha `DEF-MIG-NNN` y sigues con lo que no dependa de él.

## Lee primero (en este orden)
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. **El plan completo:** `docs/planes/migracion-staging/plan-migracion-legacy-staging.md`, en especial §2 (decisiones D1 a D6), §3 (reglas comunes) y §4 (esta fase y su criterio OK).
3. `docs/planes/paridad-legacy/plan-backend-paridad-legacy.md`:
   - §C.6 (≈ líneas 2671-2716);
   - F6-01 a F6-04 (≈ 2718-3015), en especial **las consultas de exportación** de F6-02 (≈ 2815-2850) y F6-03 (≈ 2920-2953) y las tablas de mapeo (≈ 2789-2812).
4. **El código de la herramienta:**
   - `Wms.Api/Controllers/v1/LegacyImportController.cs`;
   - `Wms.Api/Controllers/v1/Requests/LegacyImportRequests.cs`;
   - `Wms.Application/Administration/LegacyImport/`: los importadores, `LegacyCsvReader`, `LegacyDepositRowParser`, `DepositReconciler` y `LegacyBillingCycleMapper`;
   - el importador de ciudades en `CitiesController.cs`.
5. `docs/qa/fase-11-regresion-cierre.md`, **Anexo A** (FA-MIG-001 a 010), y `bodegas-legacy/docs/legacy_analysis/ROADMAP.md` 6.6 (E19).
6. **Para las tarifas (D3):**
   - `bodegas-legacy/` (el código PHP del legacy, `cron.php` y lo que facture);
   - `bodegas-legacy/legacy-analysis/LEGACY_DATA_MODEL.md`;
   - el modelo de tarifas de v2: precios base, reglas por producto y modalidad, convenios (`Agreements`), `FormulaPricing` y los mínimos por modalidad.

## Situación de partida
- **Fuente:** `code_workspace/db_legacy/backupBodegas.sql` (MariaDB 10.1.38, base `bodegas`, completo). **No uses `db.sql`:** está truncado.
- **No hay MariaDB local.** El contenedor `mysql57` es de otro proyecto: no lo uses ni lo detengas.
- **Postgres local:** contenedor `wms-postgres-db` (puerto 5433). La base **`wmsdb` es la del QA cerrado: no la toques.**
- **Build:** BE `f6f1828` / FE `24d742d`. Trabaja en `develop` sin cambiar código.

## Pasos

**1. Fuente legacy.**
- Crea un contenedor **MariaDB 10.x** nuevo, `legacy-mariadb`, puerto 3308, con su volumen. Usa una contraseña local generada; no la escribas en archivos versionados ni en tu respuesta.
- Carga `backupBodegas.sql`. Son 4,4 GB: puede tardar; anota el tiempo.
- Verifica los conteos de las tablas clave: `deposito`, `ingreso`, `cliente`, `producto`, `producto_en_bodega`, `producto_levante`, `producto_salida`, `levante`, `vehiculo`, `persona`, `pesaje`, `facturaciigo`, `detallefactura`, `tarifa`, `convenio` y `servicio`.

**2. Base v2 limpia.**
- Crea la base `wms_migracion` en `wms-postgres-db` y aplica las migraciones con `dotnet ef database update` (cadena de conexión por parámetro o variable de entorno).
- Arranca el API local contra esa base con `ConnectionStrings__DefaultConnection` y `Bootstrap__*` por variables de entorno, en un puerto distinto si el 5281 está ocupado. **No edites `appsettings`.**
- Verifica las 10 migraciones aplicadas, los 6 roles y el login del Admin.

**3. Exportación a CSV.**
- Trabaja en `code_workspace/db_legacy/trabajo/`, que no es repositorio. Crea `consultas/`, `csv/` y `extractos/`.
- Ejecuta las consultas de F6-02 y F6-03 tal como están. Si alguna necesita ajuste para este dump (columnas, codificación o el `saldo` y la `trm_ingreso` que la consulta deja en NULL), guarda la versión usada y explica la diferencia.
- **Ajuste D2:** en el CSV de depósitos, `ultimo_fin_facturado = 2026-09-30` para todos los depósitos vivos. Documenta cuántos tenían otra fecha y su rango original.
- Registra cada CSV con su consulta, filas, codificación y **SHA-256** en `docs/planes/migracion-staging/resultados/registro-csv-fase-1.md`. Ese conjunto es el que se congela para la fase 3.

**4. Carga.**
- Usa el Admin y el orden del §3.4 del plan.
- Primero **simulación** (`dryRun=true`) de todas las entidades. Analiza los errores por fila y clasifícalos:
  - dato inválido del legacy;
  - exclusión por regla;
  - duplicado legítimo;
  - **defecto de la herramienta**.
- Luego la **carga en firme**, en orden.
- Prueba la **idempotencia** recargando un maestro y los depósitos.
- Ejecuta la **conciliación** (`legacy-import/reconciliation`).

**5. Tarifas y convenios (D3) — checkpoint intermedio.**
- Determina dónde tarifaba el legacy:
  - las tablas `tarifa`, `convenio` y `servicio`;
  - las facturas de los últimos 6 meses del dump (`facturaciigo`/`detallefactura`), con precios unitarios por cliente, servicio y modalidad;
  - `cliente.dias_facturacion`;
  - el código PHP.
- Propón el mapeo a v2 en `docs/planes/migracion-staging/resultados/mapeo-tarifas-propuesto.md`:
  - precios base por servicio y modalidad;
  - convenios por cliente, con fórmula y parámetros;
  - mínimos;
  - lo que no se puede mapear, con el motivo.

  Usa razones sociales solo de empresas y nada de personas naturales.
- **Detente y pide aprobación al usuario** en el chat con un resumen del mapeo.
- Con el «sí», cárgalo **por el API** (los endpoints de convenios y precios que usa la pantalla). Luego ejecuta `open-billing` y verifica que el primer período arranca el 2026-10-01 con un importe coherente.

**6. Verificación.**
- **Anexo A del QA:** FA-MIG-001 a 010, con la evidencia de cada caso.
- **E19:**
  - saldos antes y después de un levante, un despacho, una anulación y un cargue sobre depósitos migrados;
  - períodos con fecha límite;
  - recorrido por rol en la pantalla, levantando el frontend local contra el API de `wms_migracion`.
- **Muestra de 30 depósitos** cotejada contra el legacy por SQL de lectura en los dos lados: cliente, productos, recibido, despachado, saldo, levantes, modalidad y manifiesto. Elígelos variados: modalidades, con y sin levante, con varios productos y con saldo parcial.
- **Una operación nueva completa** sobre un depósito migrado: levante → OC → cargue → guía → factura.
- **Correo (D4):** verifica que ningún tercero migrado quedó con correo y que ningún aviso de la carga se envió a terceros.

## Reglas (obligatorias)
- **Datos reales fuera de git.**
  - Los CSV, extractos y consultas van en `db_legacy/trabajo/`.
  - Los informes en git llevan conteos, números de depósito y códigos. No llevan nombres, documentos ni datos de contacto de personas naturales.
- **No imprimas secretos:** ni contraseñas, ni tokens, ni valores de `.env`. El token del Admin se usa en memoria y no se escribe en evidencias.
- **En `wms_migracion` no se escribe con SQL.** Todo va por el API; el SQL es solo de lectura para verificar. En MariaDB también solo lectura, salvo la carga del dump.
- **No toques `wmsdb`, el contenedor `mysql57`, staging ni producción.**
- **No cambies código, configuración versionada ni migraciones.** Si la herramienta tiene un defecto, abre `DEF-MIG-NNN` en `docs/planes/migracion-staging/resultados/defectos/` con la plantilla `docs/qa/plantillas/defecto.md`: pasos, CSV de ejemplo **anonimizado**, resultado esperado y obtenido, y la pista técnica.
- Si un defecto bloquea el criterio OK, termina lo que no dependa de él y detente.
- Textos en español.

## Entrega y detención
1. **Informe** `docs/planes/migracion-staging/resultados/informe-fase-1.md`:
   - tiempos de cada paso (OK-8);
   - conteos legacy frente a v2 por entidad;
   - errores por fila clasificados;
   - conciliación;
   - tarifas;
   - Anexo A;
   - E19;
   - la muestra de 30;
   - la operación nueva;
   - **la tabla OK-1 a OK-8 con «Cumple» o «No cumple»**;
   - el veredicto: **OK para pasar a la fase 2**, o **No OK**, con la lista de lo que hay que corregir.
2. Las fichas `DEF-MIG-NNN`, si las hay.
3. El estado del ambiente que dejas: el contenedor `legacy-mariadb` y la base `wms_migracion` quedan **arriba** para revisión; los CSV, congelados.
4. **El mensaje de commit** de la documentación, listo para pegar: `docs(migracion): fase 1, migración del legacy en local y verificación con datos reales (E19)`. Lleva un resumen por línea y la línea de coautoría que corresponde a tu modelo, e incluye **solo** `docs/planes/migracion-staging/`.

**Detente ahí.** La fase 2 (despliegue a staging) empieza solo con autorización del usuario.
