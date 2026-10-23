Eres el ejecutor de la **repetición de la Fase 1 — Migración del legacy en local** del plan `docs/planes/migracion-staging/plan-migracion-legacy-staging.md` del WMS de Bodegas Asociadas. Modelo recomendado: **Opus 5.5**. La primera ejecución dio **No OK** (`resultados/informe-fase-1.md`). Ya están corregidos y con commit **DEF-MIG-001 a DEF-MIG-006**. Tu objetivo es repetir la fase desde una base limpia, con las **consultas del plan corregidas** y sin paliativos, y dar el veredicto OK o No OK para pasar a la Fase 2.

**Tu trabajo es ejecutar y verificar, no corregir código.** Un defecto nuevo va como ficha `DEF-MIG-007` en adelante.

## Lee primero
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. **El plan:** `docs/planes/migracion-staging/plan-migracion-legacy-staging.md`, §2 a §4.
3. **El prompt de la primera ejecución** (`prompt-fase-1.md`). Sus reglas valen aquí sin cambios: datos reales fuera de git, sin secretos, en la base v2 no se escribe con SQL, y `wmsdb`, `mysql57`, staging y producción no se tocan.
4. **El informe de la primera ejecución** y las fichas `DEF-MIG-001` a `006`, con su fila «Corregido» y su lista de verificación.
5. `docs/planes/paridad-legacy/plan-backend-paridad-legacy.md`: las **consultas corregidas** de F6-02 y F6-03 y el formato nuevo del CSV de depósitos, con las columnas opcionales `valor_mercancia` y `moneda`.

## Situación de partida
- **Build:** los commits de la corrección de DEF-MIG-001 a 006. Anota los hashes que encuentres.
- **Lo que dejó la primera ejecución:**
  - `legacy-mariadb` arriba en el puerto 3308;
  - la base `wms_migracion`, con la primera carga y las operaciones de E19;
  - el API local en 5291 y el frontend en 3001;
  - Mailpit;
  - credenciales en `db_legacy/trabajo/`.
- **Mapeo de tarifas aprobado** por el usuario: `resultados/mapeo-tarifas-propuesto.md` (T1 a T4, con T4 en $15.000). **No se vuelve a aprobar.** Se carga igual que en la primera ejecución.

## Pasos
1. **Base limpia.**
   - Detén el API local.
   - Borra y recrea **solo** `wms_migracion` con `dotnet ef database drop` y `dotnet ef database update`, apuntando explícitamente a esa base. **Verifica dos veces la cadena de conexión antes del `drop`: nunca `wmsdb`.**
   - Arranca el API con el build corregido y verifica las migraciones, los 6 roles y el login del Admin.
2. **CSV nuevos.**
   - En `db_legacy/trabajo/`, mueve los CSV de la primera ejecución a `csv/v1/` sin borrarlos.
   - Exporta con **las consultas del plan corregido tal como están**. Guárdalas en `consultas/v2/`.
   - Aplica el ajuste D2 (`ultimo_fin_facturado = 2026-09-30`).
   - El CSV de depósitos debe traer `valor_mercancia` y `moneda`.
   - Registra el conjunto en `resultados/registro-csv-fase-1.md`, sección «Conjunto v2», con filas y SHA-256. **Este es el conjunto que se congela para la Fase 3.**
3. **Carga.**
   - Simulación y firme en el orden del §3.4, idempotencia y conciliación.
   - Tarifas T1 a T4 por el API.
   - `open-billing`.
4. **Verificación de las correcciones,** con la lista de cada ficha:
   - **DEF-MIG-001:** la consulta del plan exporta la modalidad y se acepta; 0 rechazos por modalidad.
   - **DEF-MIG-002:** la consulta de levantes trae solo levantes de los depósitos vivos (≈ 170 filas, no 819). La simulación no crea levantes en depósitos equivocados.
   - **DEF-MIG-003:**
     - el importador agrupa las filas: se crean ≈ 107 levantes sin pérdidas, y el nacionalizado de cada producto es igual a la suma del legacy;
     - la segunda carga los omite;
     - la conciliación da 133/133 «Ok».
   - **DEF-MIG-004:**
     - los depósitos quedan con moneda y valor;
     - `open-billing` liquida T1 sobre el CIF: **0,295 % × CIF en COP + IVA**, con piso de $50.000;
     - informa cuántos períodos quedan sobre el mínimo y cuántos en el mínimo, y por qué;
     - coteja 10 depósitos a mano: CIF × TRM × 0,295 %;
     - los que no tengan TRM con moneda extranjera quedan «TRM pendiente»: anota cuántos;
     - la advertencia del mínimo por CIF faltante tiene el texto nuevo.
   - **DEF-MIG-005:**
     - en BA0042 (recibido 648, salen 200), una OC, un cargue y una guía de 50 imprimen saldo anterior **448** y nuevo **398**;
     - una segunda guía parte de 398;
     - repite en otro depósito con salidas en el legacy y en uno sin salidas.
   - **DEF-MIG-006:** en el detalle de un migrado, el bloque IMPORTADOR muestra el tercero.
5. **Repetir lo esencial de la primera ejecución:**
   - **Muestra de 30 depósitos:** los mismos 30 de la primera ejecución, ahora con el CIF y la moneda en el cotejo.
   - **Operación nueva completa** sobre un migrado con salidas en el legacy: levante → OC → báscula → cargue → guía → repesaje → salida → facturas.
   - **El correo (D4) y el recorrido por rol en la pantalla** que hizo la primera ejecución.

   **No repitas** FA-MIG-005 ni FA-MIG-006 (codificación y límites): no cambiaron. Cítalos con la evidencia de la primera ejecución.

## Entrega y detención
1. **Informe** `docs/planes/migracion-staging/resultados/informe-fase-1-repeticion.md`:
   - tiempos;
   - conteos;
   - errores por fila clasificados, comparados con la primera ejecución;
   - conciliación;
   - facturación con CIF;
   - la verificación de cada DEF-MIG;
   - la muestra de 30;
   - la operación nueva;
   - **la tabla OK-1 a OK-8**;
   - el veredicto: **OK para pasar a la Fase 2**, o **No OK**, con lo que falta.
2. **Fichas.** En cada `DEF-MIG-001` a `006`, una fila «Verificado» o «Reabierto», con la evidencia. Las fichas nuevas van desde `DEF-MIG-007`.
3. **El estado del ambiente que dejas:** `legacy-mariadb`, `wms_migracion` y Mailpit arriba, y los CSV v2 congelados.
4. **El mensaje de commit** de la documentación, listo para pegar: `docs(migracion): repetición de la fase 1 con las consultas corregidas y verificación de DEF-MIG-001 a 006`. Lleva la línea de coautoría que corresponde a tu modelo e incluye **solo** `docs/planes/migracion-staging/`.

**Detente ahí.** La Fase 2 (despliegue a staging) empieza solo con autorización del usuario.
