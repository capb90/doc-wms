Eres el ejecutor de la **Fase 2 — Preparar y desplegar staging** del plan `docs/planes/migracion-staging/plan-migracion-legacy-staging.md` del WMS de Bodegas Asociadas. Modelo recomendado: **Sonnet 5.5**. Dejas staging con el build candidato, la base recreada con las migraciones actuales, los respaldos activos y el correo funcionando, **sin datos migrados**: la migración es la Fase 3. **Es un ambiente compartido y accesible desde internet:** cada paso destructivo necesita el «sí» del usuario en el chat en ese momento.

## Lee primero
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. **El plan:** §2 (decisiones D4 y D5), §3 (reglas comunes) y **§5 (esta fase)**.
3. `deploy/staging/README.md` completo, en especial la sección **Respaldos** (≈ líneas 153-186), y `scripts/deploy-staging.sh`, con sus subcomandos `bootstrap`, `config`, `backend`, `frontend`, `dbup`, `migrate`, `up`, `smoke` y `logs`.
4. `deploy/staging/compose.staging.yaml`, `Dockerfile.staging`, `Caddyfile` y `.env.staging.example`.
5. `docs/qa/fase-11-regresion-cierre.md`, Anexo B (FB-BAK-001 a 006).

## Situación de partida
- **Build candidato:** BE **`bf2dea6`** / FE **`4799cc4`**. Verifica que `develop` de los dos repos esté en esos commits, o anota los que encuentres.
- **Servidor:** el de AWS Lightsail de julio sigue vigente (confirmado por el usuario). La conexión está en `deploy/staging/.env.deploy` (`STAGING_IP`, `SSH_KEY`), que está en `.gitignore`.
- **Staging hoy:** desplegado en julio con la cadena de migraciones anterior a `InitialParityLegacy`. **Su base no sirve:** hay que recrearla.
- **`deploy/staging/artifacts/staging.sql` está obsoleto** (17 de julio).
- **Decisiones del usuario para esta fase:**
  - **Correo, D4:** Gmail real. La única dirección de destino es **`capb.dev@gmail.com`**: para `NOTIFICATIONS_ADMIN_EMAILS` y `BOOTSTRAP_ADMIN_EMAIL`. Las cuentas por rol de la Fase 5 usarán alias de esa misma dirección (`capb.dev+rol@gmail.com`).
  - **Respaldos activos,** con un destino Local.
  - **Acceso al servidor vigente.**

## Pasos

### 1. Inventario del servidor (solo lectura)
Por SSH, con la llave de `.env.deploy`, registra:
- contenedores y su estado, imágenes y tamaño;
- volúmenes (`pgdata`, `caddy_data`);
- espacio en disco, memoria y swap;
- contenido de `/opt/wms/` (sin abrir `.env`);
- la versión del API desplegada, si se puede saber;
- y si la base actual tiene datos: conteos de tablas principales, sin datos personales.

**No cambies nada.**

### 2. Configuración (sin mostrar valores)
- **`.env.staging`:** revisa que estén **todas** las claves de `.env.staging.example`, sin imprimir sus valores. Comprueba que:
  - `SMTP_HOST` apunta a Gmail;
  - `NOTIFICATIONS_ENABLED` está activo;
  - `NOTIFICATIONS_ADMIN_EMAILS` y `BOOTSTRAP_ADMIN_EMAIL` son `capb.dev@gmail.com`. Estas dos no son secretos: puedes verificar su valor.
- **Valores que solo pone el usuario:** si falta o hay que cambiar un valor secreto (contraseña SMTP, `JWT_KEY`, `POSTGRES_PASSWORD`, `BOOTSTRAP_ADMIN_PASSWORD`), **pídeselo al usuario** para que lo escriba él en el archivo. Nunca lo escribas tú ni lo pidas en el chat.
- **Respaldos.** Agrega a `compose.staging.yaml`, en el servicio `wms-api`:
  - `Backups__Enabled=true`;
  - `Backups__DailyTime=02:00`;
  - `Backups__TempPath=/tmp`;
  - el montaje `/opt/wms/backups:/opt/wms/backups`.

  Incluye en el despliegue la creación de `/opt/wms/backups` en el host con dueño UID 1654: en `bootstrap` o como paso documentado en el README. Actualiza la sección Respaldos del README para que diga que staging ya los trae activos (FB-BAK-006 resuelto).
- **Correo en el README.** Corrige la contradicción que dice «Mailtrap»: staging usa Gmail real, solo hacia direcciones del equipo (D4).

### 3. Artefactos (en el Mac)
- Regenera `deploy/staging/artifacts/staging.sql` con:
  ```
  dotnet ef migrations script --idempotent -p Wms.Infrastructure -s Wms.Api -o deploy/staging/artifacts/staging.sql
  ```
  Comprueba que contiene las **10 migraciones** (de `InitialParityLegacy` a `AddEntryLogServiceDiscardedAt`) y ninguna de la cadena vieja.
- Construye la imagen del backend con `scripts/deploy-staging.sh backend` y el frontend con `frontend`, como explica el README.
  - El `Dockerfile.staging` debe instalar `postgresql-client-18`, que los respaldos necesitan para `pg_dump`. Verifícalo en la imagen.

### 4. Checkpoint de aprobación (obligatorio)
Antes de tocar el servidor, muestra al usuario:
- qué hay hoy en staging, del inventario del paso 1;
- qué se pierde: la base actual completa y el volumen `pgdata`. `caddy_data` **se conserva**, para no pedir de nuevo los certificados y no chocar con los límites de Let's Encrypt;
- los comandos exactos que vas a ejecutar para recrear la base. Por ejemplo, detener el stack, borrar solo el volumen `pgdata` y levantar Postgres limpio.

**Espera el «sí» del usuario en el chat.** Sin él, detente aquí y entrega lo hecho.

### 5. Despliegue
Con la aprobación:
1. `config`;
2. la carga de la imagen y el frontend;
3. recrear la base (`pgdata` limpio) y `dbup`;
4. `migrate`;
5. `up`.

Después revisa `logs` hasta que el API arranque sin errores. El administrador inicial lo crea `BootstrapAdminSeeder` al arrancar.

### 6. Verificación
1. `scripts/deploy-staging.sh smoke` en verde: frontend, SPA, login inválido y CORS.
2. **Base:** `__EFMigrationsHistory` con las 10 migraciones, los 6 roles del sistema y las tablas de la migración vacías (`legacy_import_batches`, `legacy_id_map` y `warehouse_storages` en 0).
3. **API:**
   - el login del Admin responde 200 y el primer ingreso exige cambiar la contraseña;
   - **Swagger no responde** (`ASPNETCORE_ENVIRONMENT=Production`);
   - una ruta inexistente da la página de error en español;
   - el certificado HTTPS es válido en `app.` y `api.`.
4. **Correo:** pide la recuperación de contraseña del Admin desde la pantalla de login. **Pídele al usuario que confirme** que llegó a `capb.dev@gmail.com`, y anota el tiempo y el remitente. No abras el correo tú.
5. **Respaldos (Anexo B en staging):**
   - con el Admin, crea el destino Local `staging-local` en `/opt/wms/backups` (FB-BAK-001);
   - pruébalo (FB-BAK-002);
   - lanza un respaldo manual (`POST administration/backups/run`, FB-BAK-003) y verifica en el host que quedó el `.dump` y el `.tar.gz` de archivos subidos;
   - FB-BAK-005 (restaurar en una base aparte) **no se ejecuta en staging**: anota que queda para cuando haya datos, en la Fase 5.
6. **DIAN:** desde el contenedor del API, comprueba que hay salida a internet hacia el servicio de la TRM. Mide el tiempo, que debe ser de 3 s o menos. **No confirmes ningún depósito:** la base está vacía.

## Reglas (obligatorias)
- **Producción no se toca.**
- **Staging:**
  - los pasos destructivos solo con el «sí» del paso 4;
  - en la base de staging no hay SQL de escritura, salvo `migrate`;
  - el SQL de lectura es solo para verificar.
- **Sin secretos:** nunca imprimas, copies ni escribas en informes los valores de `.env.staging`, `.env.deploy`, la llave SSH, la contraseña del Admin ni los tokens. La dirección de correo y la IP pública sí pueden aparecer.
- **Datos reales:** en esta fase no se sube ningún dato del legacy. El backup, MariaDB y los CSV **no van a staging**.
- **Cambios versionados:** `compose.staging.yaml`, el README y, si hace falta, `deploy-staging.sh`. Trabaja en `develop` sin ramas y **no hagas commits**: entrega los mensajes. `artifacts/` y los `.env*` siguen fuera de git.
- **No cambies código de la aplicación.** Si el despliegue revela un defecto del producto, abre `DEF-MIG-008` en adelante con la plantilla y detente si bloquea.
- Textos en español.

## Entrega y detención
1. **Informe** `docs/planes/migracion-staging/resultados/informe-fase-2.md`:
   - inventario inicial (sin secretos);
   - cambios de configuración;
   - artefactos: la lista de las 10 migraciones y el tamaño de la imagen;
   - la aprobación recibida, con su hora;
   - cada paso del despliegue con su resultado;
   - la verificación (puntos 1 a 6), con FB-BAK-001 a 003 y la nota de FB-BAK-005;
   - el estado final de staging: URLs, versión, contenedores y espacio en disco;
   - el veredicto: **listo para la Fase 3**, o qué falta.
2. **Los mensajes de commit**, listos para pegar:
   - `chore(staging): respaldos activos con destino local y README actualizado (Gmail, FB-BAK-006)`, con el compose, el README y el script si cambió;
   - `docs(migracion): fase 2, despliegue de staging con el build candidato`, con el informe y este prompt.

   Los dos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí.** La Fase 3 (migración en staging) empieza solo con autorización del usuario.
