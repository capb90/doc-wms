Eres el ejecutor de la **Fase 3 — Migración del legacy en staging** del plan `docs/planes/migracion-staging/plan-migracion-legacy-staging.md` del WMS de Bodegas Asociadas. Modelo recomendado: **Sonnet 5.5**. Cargas en staging **el mismo conjunto de CSV v3** que salió OK en local, por el API, con las mismas tarifas, y demuestras que el resultado es **idéntico al de local**. No haces operaciones nuevas: las pruebas de flujo son de la Fase 4.

**Tu trabajo es ejecutar y verificar, no corregir código.** Un defecto nuevo va como `DEF-MIG-009` en adelante.

## Lee primero
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. **El plan:** §2 (D1 a D6), §3 (reglas comunes) y **§6 (esta fase)**.
3. **La referencia local:**
   - `resultados/informe-actualizacion-fases-1-2.md`, la parte A: conteos por entidad, errores por fila clasificados, conciliación, 128 «Opened» y el total del primer período;
   - `resultados/informe-fase-1-repeticion.md`, para el detalle de la clasificación de errores y las tarifas;
   - `resultados/registro-csv-fase-1.md`, el conjunto v3 con sus hashes.
4. **Las tarifas aprobadas:** `resultados/mapeo-tarifas-propuesto.md` (T1 a T4) y las peticiones exactas que usó la repetición (`informe-fase-1-repeticion.md` §7).
5. **Los contratos:**
   - `Wms.Api/Controllers/v1/LegacyImportController.cs`;
   - `CitiesController.cs` (`cities/import`);
   - `deploy/staging/README.md` (sección Respaldos);
   - la colección `deploy/postman/` si te sirve.

## Situación de partida
- **Staging:** `https://api.100-60-89-139.sslip.io/api/v1`, con BE `b31ddb6` / FE `508b91b`.
  - Hay 11 migraciones, **sin datos migrados**, sin ubicaciones y solo con «Contenedor Vacío» como producto.
  - Están activos los respaldos (destino Local en `/opt/wms/backups`) y las llaves persistentes.
  - El FE oculta «Estadísticas» del menú, por decisión del usuario.
- **Admin de staging:** la contraseña está en `code_workspace/db_legacy/trabajo/.admin-staging.local`. **Léela sin imprimirla**; el token se usa en memoria y no se escribe en ningún archivo.
- **CSV:** el conjunto **v3** en `code_workspace/db_legacy/trabajo/csv/`, con `sha256-csv-fase-1-v3.txt`.
- **Local de referencia:** `wms_migracion`, el API en 5291 y `legacy-mariadb` siguen arriba **para leer y comparar**. No los cambies.

## Pasos

### 1. Verificaciones previas
- **Hashes:** los 12 CSV coinciden con `sha256-csv-fase-1-v3.txt`. **Si alguno no coincide, detente.**
- **Staging en el estado esperado:**
  - login del Admin con 200;
  - 0 depósitos;
  - 0 lotes de importación (`GET administration/legacy-import/batches`);
  - 0 ubicaciones;
  - el catálogo sembrado.
- **Respaldo manual «antes de migrar»** (`POST administration/backups/run`) con resultado `Succeeded`. Anota el nombre del `.dump`: es el punto para volver a una base sin datos si la carga sale mal.

### 2. Carga, en el orden del §3.4
- **Cada entidad, primero en simulación y luego en firme:**
  - ciudades por `cities/import`;
  - embalajes, cuadrillas, ubicaciones, clientes, agencias, transportadoras, vehículos, conductores, productos, depósitos y levantes por `legacy-import/{entity}`.
- **Antes de pasar a la siguiente entidad, compara su resultado con el de local:** filas, creados, asociados a un equivalente, omitidos y rechazados.
  - **Cada número debe ser idéntico** al de la parte A del informe de actualización.
  - **Los errores por fila** deben ser los mismos, con la misma causa.
  - **Si hay cualquier diferencia, detente**, investiga y repórtala antes de seguir.
- **Mide el tiempo de cada carga.** Ahora el archivo viaja por internet; compáralo con local.

### 3. Conciliación
`POST administration/legacy-import/reconciliation` con el CSV de depósitos: **133 «Ok», 0 «Difference» y 0 «NotMigrated»**.

### 4. Tarifas T1 a T4
- **Cárgalas por el API** con exactamente las mismas peticiones de la repetición: regla `PERCENTAGE_OF_VALUE` de almacenamiento para `IMP001`, mínimo IMP, IVA y precio de báscula, y precio de la guía, todos desde el 2026-10-01.
- **No crees convenios:** el legacy no tenía convenios vigentes.
- **Comprueba que quedaron igual que en local**, leyendo los dos por el API.

### 5. Apertura de la facturación
`POST administration/legacy-import/open-billing`. Debe dar:
- **128 «Opened»**, 0 «Skipped» y 0 «Failed»;
- todos los períodos desde el **2026-10-01**: 92 hasta el 16/10 y 36 hasta el 30/03/2027;
- los 128 con `PERCENTAGE_OF_VALUE`: 124 sobre el mínimo y 4 en el piso;
- **el total del primer período exactamente $91.257.475,39**: $76.686.954,14 de subtotal y $14.570.521,25 de IVA.

### 6. Comparación con local (el criterio de esta fase)
**Tabla por entidad**, local frente a staging, con los conteos en la v2:
- terceros (y por rol), vehículos, conductores, productos y ubicaciones;
- depósitos, productos de depósito, movimientos de apertura y levantes;
- `legacy_id_map` por entidad;
- períodos y facturas de almacenamiento, con su total.

**Cómo leer los conteos:**
- **En staging:** por el API o con **SQL de solo lectura** por SSH (`docker exec … psql`). Nunca SQL de escritura.
- **En local:** con SQL de solo lectura sobre `wms_migracion`.

**Cómo comparar:**
- **Conteos:** todo debe ser **idéntico**, salvo los conteos que en local incluyan operaciones de prueba de la parte A (la OC y la guía de BA0042). Esos se explican aparte.
- **Facturas de almacenamiento:** compara depósito por depósito el número legacy (`legacy_number`), el período y el total. Las 128 deben coincidir; lista cualquier diferencia.
- **Identificadores:** no compares Id de la v2 ni números consecutivos generados, porque pueden variar. Compara por número legacy, códigos y montos.

### 7. Revisión en pantalla (solo lectura)
Entra a `https://app.100-60-89-139.sslip.io` como Admin y revisa:
- **10 depósitos migrados,** elegidos variados: con y sin salidas en el legacy, con varios productos, de los dos ciclos, y los 4 que quedan en el piso del mínimo. Revisa que el detalle muestre cliente, importador, manifiesto, moneda USD, valor comercial, levantes y existencias.
- **El inventario de Bodega** de esos depósitos.
- **La factura de almacenamiento en Borrador** de 3 de ellos.
- **`/admin/locations`** con las 9 ubicaciones, `Bodega 1 BA-[1][1]` No disponible.

**No crees, edites ni apruebes nada:** la Fase 4 hace las operaciones.

### 8. Correo y avisos
- **Correo:** revisa, con el registro de notificaciones del API o los logs, qué correos salieron durante la carga y a quién. **Solo pueden ir a `capb.dev@gmail.com`** (D4).
- **Terceros migrados:** comprueba que ninguno tiene correo; deben ser 0 contactos.
- **Si salió algún correo a otra dirección, detente y repórtalo.**

### 9. Respaldo «staging migrado»
- Lanza un respaldo manual al terminar, con resultado `Succeeded`. Anota el `.dump` y el `.tar.gz` con su tamaño. Es el **punto de restauración** de la base migrada y sin operaciones, que la Fase 5 usa para repetir las pruebas.
- **No restaures nada en esta fase.**

## Reglas (obligatorias)
- **Producción no se toca.**
- **Staging:**
  - los datos solo entran por el API de importación, con simulación antes de cada carga en firme;
  - no hay SQL de escritura ni se borran volúmenes;
  - **no se recrea la base**;
  - si algo sale mal y hace falta volver al respaldo «antes de migrar», **pídele permiso al usuario** y espera su «sí».
- **Datos reales:** los CSV viajan solo por HTTPS al API de staging.
  - No se copian al servidor por SSH ni a ningún otro lugar.
  - No se suben a git ni se pegan en informes.
  - Los informes llevan conteos, números de depósito y códigos; nunca datos de personas.
- **Sin secretos:** ni contraseñas, ni tokens, ni valores de `.env`.
- **Local:** solo lectura para comparar.
- **Sin commits:** entrega el mensaje.
- Textos en español.

## Entrega y detención
1. **Informe** `docs/planes/migracion-staging/resultados/informe-fase-3.md`:
   - las verificaciones previas y el respaldo «antes de migrar»;
   - la carga por entidad con sus tiempos, comparada con local;
   - la conciliación;
   - las tarifas;
   - `open-billing` y el total;
   - **la tabla de comparación local frente a staging**, con las diferencias explicadas;
   - la revisión en pantalla;
   - el correo;
   - el respaldo «staging migrado»;
   - el veredicto: **staging migrado e idéntico a local, listo para la Fase 4**, o lo que falta.
2. **Fichas `DEF-MIG-009` en adelante,** si las hay.
3. **El mensaje de commit:** `docs(migracion): fase 3, migración del legacy en staging idéntica a local`, con la línea de coautoría que corresponde a tu modelo. Incluye solo `docs/planes/migracion-staging/`.

**Detente ahí.** La Fase 4 (QA en staging) empieza solo con autorización del usuario.
