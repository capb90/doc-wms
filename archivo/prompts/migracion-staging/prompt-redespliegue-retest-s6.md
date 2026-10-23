Eres el ejecutor del **redespliegue de staging y el re-test** de las correcciones de **DEF-F11-021, DEF-F11-020 y O-3** del WMS de Bodegas Asociadas. Modelo recomendado: **Sonnet 5.5**. Redespliegas staging **sin recrear la base**, verificas las tres correcciones y cierras las fichas.

**Tu trabajo es ejecutar y verificar, no corregir código.**

## Lee primero
1. `Backend/wms-api/AGENTS.md`.
2. **Las reglas de staging** de `docs/archivo/prompts/migracion-staging/prompt-fase-2.md` y `prompt-fase-4.md`:
   - sin secretos;
   - sin SQL de escritura;
   - datos de QA con la marca QA-S6;
   - no se borran volúmenes ni se recrea la base.
3. **Las fichas** `docs/qa/resultados/defectos/DEF-F11-021.md` y `DEF-F11-020.md`, con su fila «Corregido» y su lista de verificación.
4. **El procedimiento de despliegue:** `deploy/staging/README.md` y `scripts/deploy-staging.sh`.

## Situación de partida
- **Staging:** BE `b31ddb6` / FE `508b91b`. Tiene los datos migrados y las operaciones QA-S6, las cuentas `qa.*` y las tarifas de montacargas de prueba.
- **Credenciales,** que se leen sin imprimirlas:
  - Admin: `db_legacy/trabajo/.admin-staging.local`;
  - cuentas de QA: `credenciales-qa-staging.local.md`.
- **Build nuevo:** los commits de la corrección. Anota los hashes.

## Pasos
1. **Respaldo manual antes de desplegar** (`POST administration/backups/run`), con resultado `Succeeded`. Anota el nombre del archivo.
2. **Artefactos:**
   - genera `staging.sql`, que no debe tener migraciones nuevas: siguen siendo 11;
   - reconstruye la imagen del backend y el frontend (`yarn generate` con la URL del API de staging).
3. **Despliegue:**
   - `config`, que sube el `Caddyfile` nuevo;
   - `backend`, `frontend` y `up`;
   - **recarga Caddy** para que tome el `Caddyfile`, por ejemplo con `docker compose restart caddy`. Sus certificados están en `caddy_data` y se conservan.
   - **No toques `pgdata`.**
4. **Re-test de DEF-F11-021:**
   - **Sin redirecciones:** con `curl` sin sesión, `/auth/login`, `/auth/reset-password?token=abc` y `/auth/request-password-reset` responden **200 sin 308**. Una ruta inexistente sirve el fallback y un recurso `/_nuxt/` responde 200.
   - **F0-LOG-008:** con la sesión de `qa.bodega`, cargar `/auth/login` como página completa redirige a la ruta del rol.
   - **El enlace del correo, de punta a punta, con ayuda del usuario.** La recuperación por correo es solo para el Admin (CHG-51).
     1. Pide la recuperación del `admin` desde la pantalla.
     2. **El usuario abre el enlace del correo, que debe mostrar la pantalla de nueva contraseña, y cambia la contraseña.**
     3. **El usuario guarda la nueva en `.admin-staging.local`** (permisos 600) y te avisa.
     4. Verifica el login del Admin con la contraseña nueva.

     No uses el enlace tú.
5. **Re-test de DEF-F11-020** (FB-BAK-003):
   - dos `POST backups/run` en paralelo → **202 y 409** «Ya hay un respaldo en curso.», y una sola corrida;
   - dos corridas seguidas en el mismo minuto → **dos archivos distintos** en `/opt/wms/backups`, con el nombre nuevo;
   - `GET backups/runs` las lista.
6. **Re-test de O-3:** un cobro «por facturar» de báscula con `qa.bascula`, sobre un camión QA-S6 nuevo, responde **`totalAmount` 20.000** y la factura queda en $20.000. Saca el camión al terminar (salida en Vigilancia).
7. **Humo del redespliegue:**
   - `smoke`;
   - login de cada cuenta `qa.*`;
   - el detalle de BA0042;
   - el total de las facturas de almacenamiento sin cambios, salvo las de las operaciones QA-S6 conocidas.
8. **Respaldo final** después de las pruebas, con resultado `Succeeded`.

## Entrega y detención
1. **Evidencia** en `docs/qa/resultados/evidencias/F11/RT-S6-*`, sin secretos.
2. **Fichas:** en `DEF-F11-021` y `DEF-F11-020`, una fila «Verificado» o «Reabierto». Actualiza `INDICE.md`.
3. **Informe final** (`informe-final.md`): §4 con las dos fichas cerradas y §7 con el veredicto «**GO condicionado solo a PRF-002**», sin fichas abiertas.
4. **El plan de migración:** anota el redespliegue en el estado de la Fase 4.
5. **Los mensajes de commit:**
   - `docs(qa-f11): re-test en staging de DEF-F11-020, DEF-F11-021 y O-3`;
   - si cambió el plan, `docs(migracion): redespliegue de staging con las correcciones de S6`.

   Los dos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí.** La Fase 5 empieza solo con autorización del usuario.
