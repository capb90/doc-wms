Eres el ejecutor de la **Fase 4** del selector de conductor del WMS de Bodegas Asociadas: **redespliegue de staging y QA en staging**. Modelo recomendado: **Sonnet 5.5**.

Redespliegas staging **sin recrear la base**, verificas el selector con las cuentas `qa.*` y re-pruebas en staging las correcciones que entran con este build. Cierras el informe de la funcionalidad.

**Tu trabajo es desplegar, ejecutar y documentar. No corriges código.**

## Lee primero
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que cita (`code_workspace/docs/contexto-negocio-wms-para-ia.md`).
2. **Plan cerrado:** `code_workspace/ajustes/plan-cerrado-selector-conductor-2026-10-08.md`. Tu alcance es **§8**. Los casos están en §7.1 y las decisiones (§2) dan el resultado esperado.
3. **Informe de la Fase 3:** `Frontend/wms/docs/qa/resultados/SEL-informe-2026-10-08.md`, con su anexo de re-test y la sección «Staging» que vas a completar. Fichas:
   - `DEF-F11-022`, `025` y `027`, en «Corregido»: se verifican aquí;
   - `DEF-F11-023`, `024` y `026`, MINOR «Nuevo»: siguen abiertos.
4. **Reglas de staging:** `Backend/wms-api/docs/migracion-staging/prompt-fase-2.md` y `prompt-fase-4.md`. Como modelo de redespliegue con re-test, `prompt-redespliegue-retest-s6.md`. En resumen:
   - sin secretos;
   - sin SQL de escritura;
   - no se borran volúmenes ni se recrea la base.
5. **Procedimiento de despliegue:** `Backend/wms-api/deploy/staging/README.md` y `scripts/deploy-staging.sh`.
6. **Contexto de staging:** `docs/migracion-staging/resultados/guia-pruebas-operarios.md`. Staging ya está en manos de operarios, con cuentas `operario.*` y datos de práctica P1-P6.

## Situación de partida
- **Staging hoy:** BE `84c712f` / FE `8527144`, con 11 migraciones. Tiene:
  - los datos migrados: 4.361 conductores reales;
  - las operaciones de ejemplo QA-S6;
  - las cuentas `qa.*` y `operario.*`;
  - los datos de práctica P1-P6.
- **Build a desplegar:** el `HEAD` de `develop` de los dos repositorios. Al escribir este prompt eran:
  - **BE `044be08`**: el código es el de `3748ec6`; después solo hay documentos;
  - **FE `4ca4e0a`**: incluye la corrección de DEF-F11-025 y DEF-F11-027.

  Anota los hashes reales (`git rev-parse --short HEAD`). Si `HEAD` es posterior, lista qué agrega.
- **Lo que entra además del selector.** El salto desde `8527144` también trae estos cambios del frontend:

  | Commit | Cambio | Qué haces en esta fase |
  |---|---|---|
  | `ec192cd` | Resaltado del menú (DEF-F11-022) | Se verifica aquí |
  | `1db3448` | El precio base admite centavos | Solo se observa, sin guardar |
  | `944ce53` | Solo báscula preselecciona BRUTO en el primer pesaje | Solo se observa, sin guardar |

  Los commits `tools/video-tutoriales/*` no forman parte de la app generada.
- **Sin migraciones nuevas.** La comprobación del autor del prompt salió vacía:

  ```bash
  git diff --stat 84c712f..HEAD -- Wms.Infrastructure/Migrations
  ```

  Repítela.
- **MINOR abiertos (decisión del usuario: se despliega con ellos).** Anótalos en el informe como conocidos; no son motivo de «Reabierto» ni de detenerte:
  - DEF-F11-023: Esc desde «Tipo de Documento»;
  - DEF-F11-024: foco y texto perdidos al salir del documento en el modal;
  - DEF-F11-026: Enter antes de que llegue la búsqueda.

  Si los ves de nuevo, agrega una línea «visto en staging» a su ficha.

## Reglas
1. **Credenciales.** No escribes contraseñas en el navegador ni las muestras en la salida.
   - **Navegador integrado:** el usuario inicia sesión y tú usas su sesión.
   - **API:**
     - Admin: `db_legacy/trabajo/.admin-staging.local` (solo la contraseña, en una línea);
     - cuentas de QA: `db_legacy/trabajo/credenciales-qa-staging.local.md` (columna 5).

     Léelos sin imprimirlos.
2. **Base de datos:**
   - sin SQL de escritura;
   - no se tocan `pgdata` ni `caddy_data`;
   - no se recrea ni se restaura la base;
   - **no se aplica ninguna migración.** Si la comprobación de migraciones no sale vacía, detente.
3. **Datos de staging:**
   - **Datos personales.** Staging tiene conductores reales. **No edites, desactives ni registres datos sobre conductores migrados.** El lápiz, «Usar este conductor» y cualquier `PATCH` se prueban solo sobre conductores `QA-SEL`.
   - **Informes sin datos de personas naturales.** Los términos de búsqueda sobre migrados se describen de forma genérica. Las capturas con datos reales se recortan o no se guardan.
   - **No toques los datos de práctica P1-P6.** CAH514 está reservado para PRF-002. Tampoco toques las operaciones de los operarios.
4. **Datos de prueba** con la marca `QA-SEL`:
   - placas `QSL801`, `QSL802` y `QSL803`;
   - conductores `QA-SEL Uno` (CC `9000000801`), `QA-SEL Dos` (CC `9000000802`) y `QA-SEL Tres` (CC `9000000803`, sin país);
   - observación «QA-SEL».

   Libera todo camión al terminar. Anota lo que quede creado.
5. **Fallas:**
   - si aparece un BLOCKER o CRITICAL en staging, detente, documenta y pregunta;
   - **no hagas rollback por tu cuenta**: el respaldo previo existe para que el usuario decida.

## Pasos
1. **Ventana de despliegue.** Antes de tocar staging, pregunta al usuario si hay operarios usando staging en este momento y espera su confirmación: el redespliegue reinicia el API y la sesión de quien esté trabajando puede fallar unos segundos.
2. **Comprobaciones previas** (plan §8.1):
   - los hashes;
   - la lista de commits que entran, con `git log --oneline` del último build de staging a `HEAD` en cada repositorio;
   - la comprobación de migraciones vacía;
   - en el frontend, `yarn test` en verde con el `HEAD` a desplegar. Anota el conteo.
3. **Respaldo manual antes de desplegar** (`POST administration/backups/run` como Admin), con resultado `Succeeded` en `GET administration/backups/runs`. Anota el nombre del archivo.
4. **Despliegue** (plan §8.2), desde `Backend/wms-api`:
   1. `scripts/deploy-staging.sh backend` y luego `scripts/deploy-staging.sh up`. No hacen falta `config` ni `migrate`: no cambian el compose, el Caddyfile ni el esquema.
   2. `scripts/deploy-staging.sh frontend`.
   3. `scripts/deploy-staging.sh smoke`.

   Revisa `logs wms-api` por errores de arranque. El aviso de `libgssapi_krb5.so.2` es benigno.
5. **QA en staging** (plan §8.3). Los casos S1 a S9 del plan, con estas precisiones:
   - **S1:** el API con `qa.bascula`, 5 términos genéricos y 3 corridas por término (`curl -w '%{time_total}'`). Criterio: pertinencia, `pageSize` 20, `totalCount` coherente y cada respuesta en menos de 1 s.
   - **S2:** F9-API-022 a 025.
     - Con `qa.bodega`, `POST /drivers` con cuerpo `{}` debe dar 400 y no 403, y el `PATCH` va sobre `QA-SEL Uno` después de S4.
     - Con `qa.bodega`, `POST /vehicles` con `{}` debe dar 403.
     - Con `qa.facturacion`, `POST /drivers` con `{}` debe dar 403.
     - Sin token, `GET /drivers?search=x` debe dar 401.
   - **S3:** `qa.vigilancia` ingresa `QSL801` y `QSL803` con «Solo Báscula», y `QSL802` con «Solo bodega», todos con la observación «QA-SEL».
   - **S4:** `qa.bascula` toma `QSL801` y pone el país del vehículo «Ecuador». Ejecuta F3-CAM-004, 005 (crea `QA-SEL Uno`), 013, 014, 015, 016 (con `9000000801`), 017 (teléfono de `QA-SEL Uno`) y 021.
     - **Al elegir el tipo de operación «Solo báscula», observa si el primer pesaje propone BRUTO** (`944ce53`).
   - **S5:** guarda el registro de `QSL801`, eligiendo el cliente QA de S6 que use la guía. Verifica F3-CAM-020: el ingreso queda con `QA-SEL Uno` y ningún otro conductor cambia.
   - **S6:** limpieza de `QSL801`: descarta la operación en «Recuperar operaciones», sin cobro ni factura, y registra la salida en Vigilancia.
   - **Re-test de DEF-F11-025 (CRITICAL).**
     1. Crea `QA-SEL Tres` **sin país**, por API con `qa.bascula`: `POST /drivers` con `country: null`.
     2. En báscula, con `QSL803` y su país de vehículo «Ecuador», usa «+», escribe `9000000803` y pulsa «Usar este conductor».
     3. Esperado:
        - no hay `PATCH` ni aviso de actualización;
        - el conductor queda seleccionado con «País: Ecuador (del vehículo)»;
        - `GET /drivers/{id}` sigue con `country: null`.
     4. Luego usa el lápiz, cambia el teléfono y guarda.
     5. Esperado: `PATCH` 200 y `country` sigue `null`.
     6. Suelta el camión sin guardar la ficha y registra la salida de `QSL803`.
   - **S7:** `qa.bodega`, en «Recepción Directa», elige `QSL802` y ejecuta F4-RSB-009 (crea `QA-SEL Dos`), 010 (lápiz sobre `QA-SEL Dos`) y 011. **No guardes la recepción**: crearía un depósito.
   - **S8:** limpieza: registra la salida de `QSL802` en Vigilancia.
   - **Re-test de DEF-F11-027 (MAJOR).** El usuario abre sesión de Admin en el navegador. En Administración → Conductores, filtra por nombre «QA-SEL»: deben aparecer los tres conductores `QA-SEL` y la petición debe llevar `name=QA-SEL`.
   - **Re-test de DEF-F11-022 (MINOR, menú).** Repite los pasos de su ficha con la sesión que tengas abierta: el resaltado del menú respeta la entrada elegida y las entradas con filtro.
   - **Observación de `1db3448`.** Con Admin, abre la edición del precio base de un servicio y comprueba que el campo admite centavos. **No guardes.**
   - **S9: humo.**
     - login de cada cuenta `qa.*`;
     - el detalle de BA0042;
     - la cola de báscula sin camiones `QSL`;
     - Vigilancia → Salida sin camiones `QSL` en planta;
     - los camiones de práctica P1-P6 siguen como los dejó la Fase 5.
6. **Respaldo final** después de las pruebas, con resultado `Succeeded`. Anota el archivo.

## Entrega y detención
1. **Evidencia** en `Frontend/wms/docs/qa/resultados/evidencias/SEL/staging-*`, sin secretos ni datos reales.
2. **Informe** `SEL-informe-2026-10-08.md`: completa la sección «Staging» con:
   - los hashes desplegados y la lista de commits que entraron;
   - los respaldos antes y después;
   - el resultado por caso: S1-S9, los re-test y las observaciones;
   - las mediciones de S1;
   - los MINOR conocidos;
   - los datos `QA-SEL` que quedaron.

   El veredicto es **«Verificado en staging»** si no hay BLOCKER, CRITICAL ni MAJOR abiertos; si no, **«Reabierto»** con el motivo. Agrega la nota: **PRF-002** (cronometraje de báscula con un operario) debe medirse con este build, porque cambió la card del conductor.
3. **Fichas:**
   - en `DEF-F11-022`, `025` y `027`, una fila «Verificado» (staging, fecha y hashes) o «Reabierto»;
   - los defectos nuevos van desde `DEF-F11-028`, con ficha propia;
   - actualiza `INDICE.md`: estados, totales y una nota de actualización en el encabezado.
4. **Plan de migración** (`Backend/wms-api/docs/migracion-staging/plan-migracion-legacy-staging.md`): agrega una línea al estado de la Fase 5 con la fecha, los hashes, «sin migraciones», los respaldos y el veredicto.
5. **Guía de operarios.** Si `guia-pruebas-operarios.md` necesita algo más tras ver el selector en staging, anótalo como pendiente. No la edites en esta fase.
6. **Resumen al usuario y mensajes de commit propuestos.** Cada mensaje termina con la línea de coautoría de tu modelo:
   - frontend: `docs(qa): selector de conductor verificado en staging`;
   - backend: `docs(migracion): redespliegue de staging con el selector de conductor`.

**Detente ahí.** El cierre de PRF-002 y cualquier corrección de los MINOR abiertos son trabajos aparte, con autorización del usuario.
