Eres el ejecutor de la **actualización de las Fases 1 y 2** del plan `docs/planes/migracion-staging/plan-migracion-legacy-staging.md` del WMS de Bodegas Asociadas, después de la corrección de **DEF-MIG-008**: semillas de ejemplo eliminadas, ubicaciones del legacy completas y llaves de DataProtection persistentes. Modelo recomendado: **Sonnet 5.5**. Tienes dos tareas:
- **(A)** repetir la carga en local con la consulta de ubicaciones nueva y volver a congelar el conjunto de CSV;
- **(B)** redesplegar staging con el build nuevo, **sin recrear su base**.

**Tu trabajo es ejecutar y verificar, no corregir código.** Un defecto nuevo va como `DEF-MIG-009` en adelante.

## Lee primero
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. **El plan:** §2 a §5.
3. **Los prompts anteriores**, cuyas reglas valen aquí sin cambios:
   - `prompt-fase-1-repeticion.md`: datos reales fuera de git, sin secretos, en la base v2 no se escribe con SQL, y `wmsdb`, `mysql57` y producción no se tocan;
   - `prompt-fase-2.md`: staging y sus reglas.
4. **Los informes y la ficha:**
   - `resultados/informe-fase-1-repeticion.md`;
   - `resultados/informe-fase-2.md`;
   - `resultados/defectos/DEF-MIG-008.md`, con su fila «Corregido» y su lista de verificación.

## Situación de partida
- **Build:** los commits de la corrección de DEF-MIG-008. Anota los hashes. Incluye la migración `RemoveSampleSeedData`.
- **Local:** `legacy-mariadb` (3308), `wms_migracion` con la carga v2, el API en 5291, el frontend en 3001 y Mailpit.
- **Staging:**
  - desplegado en la Fase 2, **sin datos migrados**;
  - el usuario ya cambió la contraseña del `admin` y creó el destino de respaldo. Si no lo hizo, pídeselo antes de la parte B;
  - la contraseña nueva del Admin de staging está en `db_legacy/trabajo/.admin-staging.local`. Léela sin imprimirla. Si el archivo no existe, pídeselo al usuario.

## A. Recarga en local
1. **Base limpia.**
   - Detén el API local.
   - Borra y recrea **solo** `wms_migracion` con `dotnet ef`. **Verifica dos veces que la cadena apunta a `wms_migracion` y nunca a `wmsdb`.**
   - Arranca el API con el build nuevo.
   - Verifica que la base **no trae** las 20 ubicaciones de ejemplo ni los 4 productos de ejemplo, y **sí** «Contenedor Vacío» y el resto del catálogo.
2. **Conjunto de CSV.**
   - Exporta **solo** las ubicaciones con la consulta nueva del plan. Deben salir **9 filas**: 6 de sección y 3 de bodega, con `ocupacion`.
   - Los otros 11 CSV del conjunto v2 no cambian. Verifica su SHA-256 contra `sha256-csv-fase-1-v2.txt`.
   - Registra el **conjunto v3** en `resultados/registro-csv-fase-1.md`: los 11 iguales y el de ubicaciones nuevo, con su hash. **Ese es el conjunto que se congela para la Fase 3.**
3. **Carga completa**, porque toma menos de 30 s: simulación y firme en el orden del §3.4, idempotencia, conciliación, tarifas T1 a T4 y `open-billing`.
4. **Verificación:**
   - **Ubicaciones:** 9 creadas con 0 rechazos. `Bodega 1 BA-[1][1]` queda No disponible; las demás, Disponibles. Una segunda carga no duplica. `/admin/locations` en la pantalla muestra solo esas 9.
   - **Productos:** el conteo de productos es el de la repetición menos los 4 de ejemplo que ya no existen. Si alguno del legacy se asociaba a uno de ejemplo por nombre, ahora debe crearse: explica la diferencia exacta.
   - **El resto, igual que en la repetición:**
     - la conciliación da 133/133 «Ok»;
     - 128 «Opened»;
     - **el total del primer período es exactamente $91.257.475,39.** Si no, explica por qué.
   - **Una guía sobre un migrado** imprime el manifiesto y los saldos correctos (DEF-MIG-005 y DEF-MIG-007).

## B. Redespliegue de staging (sin recrear la base)
1. **Artefactos:**
   - regenera `deploy/staging/artifacts/staging.sql` (idempotente); debe traer **11 migraciones**, incluida `RemoveSampleSeedData`;
   - reconstruye la imagen del backend y el frontend.
2. **Configuración:**
   - `bootstrap`, que ahora crea `/opt/wms/data/keys` con dueño UID 1654;
   - `config`.
3. **Antes de migrar,** con SQL de solo lectura:
   - comprueba que **ninguna** de las 20 ubicaciones ni de los 4 productos de ejemplo está referenciada en staging (mercancía, ubicación principal o depósitos). Staging no tiene datos, así que deben ser 0;
   - si hay referencias, **detente y repórtalo**.
4. **Despliegue:** `backend`, `frontend`, `migrate` y `up`. **No borres el volumen `pgdata`:** la base conserva el Admin con su contraseña nueva y el destino de respaldo.
5. **Verificación:**
   - **Base:** las 11 migraciones; `warehouse_locations` en 0 (sin ejemplos); los productos de ejemplo eliminados y «Contenedor Vacío» presente.
   - **DataProtection:** hay llaves en `/opt/wms/data/keys`.
   - **Prueba de las llaves:** pide la recuperación de contraseña de una cuenta de prueba, o la del Admin si el usuario lo autoriza. Reinicia el contenedor del API (`docker compose restart wms-api`). **El usuario confirma que el enlace del correo sigue funcionando después del reinicio.** No uses el enlace tú.
   - **`smoke`** en verde.
   - **El login del Admin** con la contraseña de `.admin-staging.local`.
   - **Respaldos:** el destino creado por el usuario está activo y su prueba responde bien. Un respaldo manual deja el `.dump` y el `.tar.gz` en `/opt/wms/backups`.
   - **Lo que la Fase 2 dejó pendiente:**
     - salida a internet hacia la DIAN desde el contenedor del API, en 3 s o menos;
     - si el usuario no lo confirmó antes, la llegada del correo de recuperación a `capb.dev@gmail.com`.

## Reglas (obligatorias)
- **Producción no se toca.**
- **En staging:**
  - no se recrea la base ni se borran volúmenes;
  - no hay SQL de escritura, salvo `migrate`;
  - el SQL de lectura es solo para verificar.
- **Sin secretos:** ni contraseñas, ni tokens, ni valores de `.env`. Las contraseñas se leen de los archivos locales sin imprimirlas.
- **Datos reales fuera de git.** Los informes llevan conteos, códigos y nombres de bodegas, nunca datos de personas.
- **Sin commits:** entrega los mensajes.

## Entrega y detención
1. **Informe** `docs/planes/migracion-staging/resultados/informe-actualizacion-fases-1-2.md`:
   - **A:** conteos comparados con la repetición, ubicaciones, productos, conciliación, el total del primer período, la guía y el conjunto v3 con sus hashes;
   - **B:** artefactos, despliegue, verificación y pendientes cerrados;
   - el veredicto: **listo para la Fase 3** o lo que falta.
2. **Ficha DEF-MIG-008:** una fila «Verificado» o «Reabierto» con la evidencia.
3. **El mensaje de commit:** `docs(migracion): recarga local con las ubicaciones del legacy y redespliegue de staging (DEF-MIG-008)`, con la línea de coautoría que corresponde a tu modelo. Incluye solo `docs/planes/migracion-staging/`.

**Detente ahí.** La Fase 3 (migración en staging) empieza solo con autorización del usuario.
