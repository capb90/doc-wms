Eres el implementador de la corrección de **DEF-F11-021 (MAJOR)**, **DEF-F11-020 (MINOR)** y del **resto de O-3**, encontrados en la sesión S6 de QA en staging del WMS de Bodegas Asociadas. Modelo recomendado: **Sonnet 5.5**: son tres cambios acotados en el frontend, el servicio de respaldos y báscula, más la configuración del servidor web de staging. **Tu trabajo es el código y la configuración.** El redespliegue y el re-test en staging los hace otro agente con `prompt-redespliegue-retest-s6.md`.

## Lee primero
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. Las fichas `docs/qa/resultados/defectos/DEF-F11-021.md` y `DEF-F11-020.md`, y el informe `F11-informe-S6-2026-10-06.md`, §4.10, con la observación del total sin redondear.
3. **El código:**
   - `Frontend/wms/app/middleware/auth.global.ts` y los demás middleware de `app/middleware/`;
   - `app/utils/role-routes.ts` (`resolveDeniedRedirect`);
   - las páginas `app/pages/auth/` (`reset-password` lee el token de la query);
   - `Backend/wms-api/deploy/staging/Caddyfile`;
   - `Wms.Application/Administration/Backups/Common/BackupService.cs`: `StartManualAsync` (≈ línea 53), `IsRunningAsync` (≈ 287) y el nombre del archivo (≈ 116-117), más el job programado que llama al mismo servicio;
   - los handlers `StartStoragePendingBillingHandler`, `StartOutputPendingBillingHandler` y `StartWeighingOnlyPendingBillingHandler`;
   - `WeighbridgeService.CalculateTaxAmount`, que ya redondea por O-3 (commit `ae36ac9`).

---

## 1. DEF-F11-021 (MAJOR): las rutas con «/» final rompen la recuperación de contraseña

**Causa.**
- Caddy sirve el sitio estático con `try_files {path} {path}/ /200.html`. Para las rutas que existen como carpeta generada (`/auth/login`, `/auth/reset-password`, `/auth/request-password-reset`…) responde **308 hacia la ruta con «/» final** y conserva la query.
- El middleware compara `to.path` de forma literal: `PUBLIC_ROUTES.includes(to.path)`, `=== "/auth/change-password"` y `=== "/access-denied"`. No reconoce la ruta y manda al login, sin el token.

**Decisión (cerrada): se corrigen las dos capas.**
1. **Frontend (la corrección de fondo).** Una función `normalizePath` en `app/utils/`: quita las «/» finales y deja «/» para la raíz.
   - El middleware la usa en **todas** sus comparaciones de rutas y al calcular la redirección por rol.
   - Revisa los demás middleware y cualquier comparación literal de `route.path` o `to.path` en el código, por ejemplo el resaltado del menú, y aplícala donde corresponda.
   - **La query y el hash no se pierden:** `reset-password` debe seguir leyendo `?token=`.
   - **Prueba Vitest** del middleware y de la función:
     - `/auth/reset-password/?token=x` sin sesión → se permite, con el token;
     - `/auth/login/` con sesión → redirige a la ruta del rol (F0-LOG-008);
     - `/auth/change-password/` y `/access-denied/` → se comportan como sin la barra;
     - `/` sigue funcionando.
2. **Servidor web de staging.** En el `Caddyfile`, cambia la regla del sitio para **servir el `index.html` de la carpeta sin redirigir**, por ejemplo `try_files {path} {path}/index.html /200.html`. El fallback SPA a `200.html` debe seguir funcionando.
   - Verifica localmente con un Caddy en Docker sobre el `.output/public` generado (`yarn generate`) que:
     - `/auth/login` responde **200 sin 308**;
     - `/auth/reset-password?token=abc` responde 200 y conserva la query;
     - una ruta inexistente sirve el fallback;
     - los recursos estáticos (`/_nuxt/…`) se sirven bien.
   - Documenta el cambio en `deploy/staging/README.md`, con una línea para el futuro despliegue de producción.

**Fuera de alcance:**
- CHG-51: la recuperación por correo sigue siendo solo para el Admin; los operarios los restablece el Admin.
- El contenido de las páginas de autenticación.

---

## 2. DEF-F11-020 (MINOR): dos respaldos simultáneos corren a la vez

**Causa.**
- `StartManualAsync` consulta si hay una corrida `Running` y después inserta la nueva, sin bloqueo entre las dos operaciones. Dos peticiones simultáneas pasan las dos.
- El nombre del archivo tiene resolución de minuto (`wms_{yyyyMMdd_HHmm}.dump`), así que dos corridas del mismo minuto escriben el mismo archivo.

**Decisión (cerrada).**
1. **Candado en la base, sin migración.** Dentro de una transacción, toma `pg_advisory_xact_lock` con una clave fija de respaldos. Después:
   - si hay una corrida `Running`, responde lo de hoy: 409 «Ya hay un respaldo en curso.»;
   - si no, inserta la corrida y confirma.

   **El mismo candado** lo usa el job programado de las 02:00: si encuentra una corrida manual en curso, la omite y lo registra en el log, sin fallar.
   - **No uses un índice único** por la corrida: una corrida que quedara `Running` tras un reinicio bloquearía todas las siguientes.
   - Si ya existe una regla para corridas `Running` viejas o huérfanas, respétala. Si no existe, anótalo como observación sin implementarla.
2. **Nombre único.** El nombre del respaldo incluye los segundos y un sufijo corto del Id de la corrida, por ejemplo `wms_{yyyyMMdd_HHmmss}_{id8}.dump`, y lo mismo el `.tar.gz` de los archivos subidos.
   - La retención (30 diarios y 12 mensuales) y la restauración del README deben seguir funcionando con el nombre nuevo. Ajusta el patrón donde se lea el nombre y actualiza el ejemplo del README.
3. **Pruebas de integración** (Testcontainers):
   - dos `POST backups/run` en paralelo → uno 202 y otro 409, y una sola corrida;
   - dos corridas seguidas en el mismo minuto → dos archivos distintos;
   - el job programado con una manual en curso → se omite sin error.

---

## 3. Resto de O-3: el total del cobro «por facturar» sin redondear

**Causa.** La corrección O-3 (`ae36ac9`) redondeó el IVA del total propuesto en los inicios de báscula (`WeighbridgeService.CalculateTaxAmount`). Los handlers `Start*PendingBilling` calculan su `totalAmount` por otro camino, y la respuesta trae 19.999,9968. La factura sí queda en $20.000.

**Cambio.**
- Los tres handlers usan el mismo cálculo redondeado: `WeighbridgeService.CalculateTaxAmount` o la regla de `FormulaPricing`. La respuesta y la factura deben dar el mismo valor.
- **No cambies el importe de las facturas.**
- **Prueba:** 16.806,72 + 19 % en cada uno de los tres caminos responde **20.000,00**.

---

## Sin retrocesos
- **Rutas:** todas siguen funcionando igual, con y sin «/» final. El login, el cambio de contraseña obligatorio, «Acceso Denegado» y la redirección por rol (CHG-87) no cambian.
- **Respaldos:** el respaldo programado y el manual siguen funcionando, con la retención y la notificación de fallo intactas.
- **Báscula:** los cobros no cambian de importe.
- **Pruebas existentes:** pasan sin editarlas. Si alguna supone el nombre de archivo viejo o el total sin redondear, **detente y repórtala**.

## Restricciones
- Trabaja en `develop` de los dos repos. **No crees ramas ni hagas commits**: entrega los mensajes.
- **No toques staging ni producción.** No redespliegues.
- Sin migraciones: `has-pending-model-changes` sin cambios. Si algo exigiera una, detente.
- No copies secretos. Textos y comentarios en español. Nada fuera de este alcance.

## Fichas
- En `DEF-F11-021.md` y `DEF-F11-020.md`: **Estado** «Corregido», una fila «Corregido» con el resumen, las pruebas y «commits: pendiente», y la lista de verificación para el re-test en staging.
- En `INDICE.md`, solo esos dos estados.
- En el informe S6 §4.10, anota que la observación del total sin redondear quedó corregida.

## Verificación antes de terminar
1. `dotnet build` y `dotnet test` de `Wms.Tests` y `Wms.IntegrationTests` en verde. Reporta los totales.
2. `has-pending-model-changes` sin cambios.
3. En `Frontend/wms`:
   - `yarn test` en verde;
   - `yarn build` y `yarn generate` con código 0;
   - `yarn lint` con no más de 279 errores.
4. La prueba del Caddy local (§1.2), con su salida resumida.
5. `git status`: solo los archivos de este alcance.

## Entrega
Responde con:
1. Los archivos por punto.
2. Las comparaciones de ruta que encontraste y cuáles normalizaste.
3. La salida de la prueba de Caddy.
4. Las compuertas, con números.
5. **Los mensajes de commit**, listos para pegar:
   - **Frontend:** `fix(qa-f11): rutas con «/» final reconocidas por el middleware (DEF-F11-021)`;
   - **Backend:** `fix(qa-f11): respaldos sin corridas simultáneas y con nombre único, y total «por facturar» de báscula redondeado (DEF-F11-020, O-3)`;
   - **Backend (staging):** `chore(staging): el sitio sirve index.html sin redirigir a la ruta con «/» (DEF-F11-021)`;
   - **Frontend (documentación):** `docs(qa-f11): fichas DEF-F11-020 y 021 corregidas`.

   Todos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí.**
