Eres el implementador de la corrección de **DEF-MIG-007** y de dos observaciones menores de la repetición de la Fase 1 del plan de migración del WMS de Bodegas Asociadas (`docs/planes/migracion-staging/plan-migracion-legacy-staging.md`). Modelo recomendado: **Sonnet 5.5**. Es un cambio acotado en el PDF de la guía, una línea del plan de paridad y una revisión de redondeo. **Se corrige antes de la Fase 2**, para que la imagen que se despliega en staging ya lo lleve.

## Lee primero
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. `docs/planes/migracion-staging/resultados/informe-fase-1-repeticion.md`: §8, «Hallazgo nuevo», y §12, «Defectos y observaciones», con O-1 y O-3.
3. `docs/planes/migracion-staging/resultados/defectos/DEF-MIG-007.md`.
4. El código:
   - `Wms.Application/ForeignTrade/Common/Services/DispatchGuidePdfService.cs` (≈ líneas 485-520: la carga del contexto de la guía y la tabla de líneas);
   - `Wms.Domain/Entities/ForeignTrade/ImportWarehouseStorage.cs` (`ManifestNumber`);
   - las pruebas existentes de la guía, en especial `GuideReprintTests` y las de CHG-33, CHG-35 y DEF-MIG-005.

---

## 1. DEF-MIG-007 (MAJOR): la guía de los depósitos migrados sale sin el manifiesto DIAN

**Causa (confirmada).**
- La columna «Manifiesto» de cada línea se toma solo de los manifiestos de los camiones del servicio: `sr.EntryLogs.SelectMany(el => el.Manifests).FirstOrDefault()`.
- Los depósitos migrados no tienen camiones, así que sale vacía.
- El manifiesto sí está en el depósito: `ImportWarehouseStorage.ManifestNumber`, cargado por la migración y visible en el detalle.

**Decisión (cerrada).**
- **Orden de prioridad del manifiesto:**
  1. el de los camiones, si hay alguno, **exactamente como hoy**;
  2. si no hay, el del depósito de importación de esa línea (`ImportWarehouseStorage.ManifestNumber`);
  3. si tampoco, vacío.
- **Depósitos con camiones:** la regla no cambia para ellos, ni siquiera si su manifiesto de depósito difiere del de los camiones.
- **Carga de datos:** si el contexto de la guía no carga `ImportWarehouseStorage`, agrégalo a la consulta de la guía sin cambiar la cantidad de idas a la base de forma notable, o en una sola consulta adicional por guía.
- **Reimpresión:** la guía se genera con los datos de hoy, así que una reimpresión de una guía ya emitida de un migrado mostrará el manifiesto. Es correcto: el manifiesto no cambió.
- **Fuera de alcance:**
  - el encabezado «Tiquetes:» de los migrados, que queda vacío porque los tiquetes del legacy no se migran;
  - el formato del PDF (CHG-84 / formato legacy).

**Pruebas.**
- **Integración:**
  - una guía de un depósito migrado sin camiones imprime el manifiesto del depósito;
  - una guía de un depósito con camiones imprime el manifiesto del camión, como hoy, aun si el depósito tiene otro;
  - un depósito sin manifiesto en ningún lado sale vacío.
- **Cómo leer el PDF:** usa el método que ya existe en el proyecto, por ejemplo el que usan las pruebas de reimpresión, o una prueba sobre la función que arma la línea.

---

## 2. O-1 (documentación): el orden de la consulta de levantes no es estable

- **Problema:** la consulta de levantes del plan (`docs/planes/paridad-legacy/plan-backend-paridad-legacy.md`, ≈ línea 3008) termina en `ORDER BY D.nro_deposito, L.nro_levante, L.nro_aceptacion, PB.id_producto`. Ese orden no es total: una reexportación trae las mismas filas en otro orden y cambia el hash del CSV.
- **Cambio:** agrega al final del `ORDER BY` el identificador único de la fila de `producto_levante` (`PL.id_productolevante` o el nombre real de la columna; verifícalo en `bodegas-legacy/bodegas_schema.sql`).
- **Revisa también** si la consulta de depósitos (≈ línea 2975) tiene un orden total. Si no lo tiene, agrégale una columna de desempate.
- Agrega una nota de una línea con la razón.

---

## 3. O-3 (revisión): el inicio de salida de báscula responde el total sin redondear

**Problema.** El inicio de salida de báscula devuelve `totalAmount = 19.999,9968`, que es 16.806,72 × 1,19 sin redondear. La factura sale bien, en $20.000,00.

**Qué hacer.**
1. Ubica el handler o DTO que arma ese `totalAmount`. Probablemente es la vista previa del cobro de salida o de báscula.
2. Comprueba si la pantalla de báscula lo muestra o lo envía tal cual, por ejemplo como total propuesto del cobro.
3. **Corrige el redondeo a 2 decimales** en el cálculo del total propuesto, con la misma regla que usa la factura. El total que muestra la pantalla y el que se cobra deben ser el mismo valor.
4. **No cambies** cómo se calcula la factura.
5. Si el mismo patrón sin redondear aparece en las vistas previas de cobro de entrada o de Solo báscula, corrígelo igual y lístalo.
6. **Si la pantalla ya redondea y el valor nunca llega sin redondear al cobro,** corrige solo el API para que responda el total redondeado y anótalo.

**Prueba.** Unitaria o de integración: con el precio 16.806,72 + IVA del 19 %, el total propuesto es **20.000,00**.

---

## Sin retrocesos
- Las guías de depósitos con camiones imprimen lo mismo que hoy.
- Los saldos de la guía (DEF-MIG-005) y el levante guardado (CHG-35) no cambian.
- Los cobros de báscula no cambian de importe.
- Las pruebas existentes pasan sin editarlas. Si alguna supone el valor sin redondear, **detente y repórtala**.

## Verificación con datos reales
En `wms_migracion`, que quedó arriba con el API local en el puerto 5291 y el build de la repetición:

1. Detén el API local de la migración y arráncalo con este build: el mismo `.env.migracion.local`, sin tocar `appsettings`.
2. **Reimprime por el API** las guías `2026S00001` a `2026S00004` (`GET dispatch-guides/{id}/pdf`). La columna «Manifiesto» debe traer el manifiesto DIAN de cada depósito, el mismo que muestra su detalle.
3. Guarda los PDF en `db_legacy/trabajo/evidencias/v2/def-mig-007/`, **fuera de git**.
4. **No escribas en la base con SQL.** Las reimpresiones son de solo lectura.
5. No toques `wmsdb`, staging ni producción.

## Restricciones (obligatorias)
- Trabaja en `develop`. **No crees ramas, no hagas `git add`, commit, push ni merge**: entregas los mensajes de commit y el usuario hace los commits.
- No copies secretos ni datos reales a git. En los informes y fichas, cita los manifiestos solo por depósito; no transcribas datos de terceros.
- Sin migraciones: `dotnet ef migrations has-pending-model-changes` sin cambios.
- Textos y comentarios en español. Nada fuera de este alcance.

## Ficha e informe
- En `DEF-MIG-007.md`: **Estado** «Corregido», una fila «Corregido» y una fila «Verificado» con la reimpresión de las 4 guías de `wms_migracion`, más «commits: pendiente».
- En `informe-fase-1-repeticion.md` §12, actualiza el estado de DEF-MIG-007, O-1 y O-3 con una línea cada uno. No cambies el veredicto.

## Verificación antes de terminar
1. `dotnet build` sin errores ni advertencias nuevas.
2. `dotnet test` de `Wms.Tests` y `Wms.IntegrationTests` en verde (1694 y 286 antes de esta corrección). Reporta los totales.
3. `has-pending-model-changes` sin cambios.
4. Si tocaste el frontend por O-3: `yarn test`, `yarn build` y `yarn lint` (no más de 279 errores).
5. `git status`: solo los archivos de este alcance, este prompt y los documentos de `docs/planes/migracion-staging/`.

## Entrega
Responde con:
1. Los archivos modificados, por punto.
2. Dónde estaba el total sin redondear (O-3) y qué otras vistas previas revisaste.
3. El resultado de cada compuerta, con números.
4. La verificación con las 4 guías reimpresas.
5. **Los mensajes de commit**, listos para pegar, cada uno por separado:
   - **Backend:** `fix(migracion): la guía usa el manifiesto del depósito cuando no hay camiones y el total propuesto de báscula se redondea (DEF-MIG-007)`, con una línea por cambio.
   - **Backend (documentación):** `docs(migracion): orden estable de las consultas de exportación y ficha DEF-MIG-007 verificada`.
   - **Frontend**, solo si lo tocaste.
   - Todos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí.** La Fase 2 (despliegue a staging) empieza solo con autorización del usuario.
