Eres el ejecutor de la **Fase 5 — Staging listo para los operarios** del plan `docs/planes/migracion-staging/plan-migracion-legacy-staging.md` del WMS de Bodegas Asociadas. Modelo recomendado: **Sonnet 5.5**. Dejas staging con los **datos migrados limpios**, las tarifas reales de montacargas, una cuenta por rol para los operarios, datos de práctica sacados del legacy y una guía de pruebas por rol, para que los operarios prueben todo sin ayuda.

## Lee primero
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. **El plan:** §2 (D1 a D6), §3 y **§8 (esta fase)**.
3. **Los informes:**
   - `resultados/informe-fase-3.md`: el respaldo «staging migrado» y lo que contiene;
   - `docs/qa/resultados/F11-informe-S6-2026-10-06.md` y `evidencias/F11/RT-S6-redespliegue-retest.txt`: el estado actual de staging, las cuentas `qa.*`, las operaciones QA-S6, la recuperación de contraseña que ya funciona y los respaldos con nombre nuevo;
   - `docs/qa/resultados/informe-final.md` §8: PRF-002, que mide un operario.
4. **El despliegue:** `deploy/staging/README.md`, en especial Respaldos y Restauración, y `deploy/staging/compose.staging.yaml`.
5. **Para la guía:** el documento de contexto, el manual de usuario `docs/manuales/Manual_Usuario_WMS.pdf` si sirve, y los flujos de `docs/qa/fase-0*.md`.

## Decisiones del usuario para esta fase (2026-10-07)

| # | Decisión |
|---|---|
| F5-1 | **Partir de los datos migrados limpios:** se restaura el respaldo «staging migrado», **`/opt/wms/backups/2026/10/wms_20261006_2302.dump`**, con sus archivos `uploads_20261006_2302.tar.gz`. Se pierden las operaciones QA-S6, las cuentas `qa.*` y las tarifas de montacargas de prueba. |
| F5-2 | **Tarifas base actuales de montacargas,** por tipo de vehículo:<br>Tractomula **$220.000**<br>Doble Troque **$150.000**<br>Sencillo **$140.000**<br>Turbo **$110.000**<br>Guacal o Estiba **$40.000**<br>Son **valores base**: el IVA se suma en cada uso cuando se marca «Aplicar IVA», según la decisión de la Ola 1 (IVA opcional en montacargas). Si el modelo de `ForkliftRate` interpreta el monto de otra forma, **detente y pregunta**. |
| F5-3 | **Una cuenta por rol para los operarios,** con alias del correo del usuario: `capb.dev+operario.<rol>@gmail.com`. |

## Pasos

### 1. Respaldo y estado antes de restaurar (solo lectura)
- **Respaldo manual «antes de F5»**, con resultado `Succeeded`. Guarda las pruebas de S6 por si hiciera falta volver.
- **Registra el estado actual:** conteos de depósitos, facturas y su total, usuarios, entradas, ciclos, órdenes y guías.
- **Verifica en el host** que existen `wms_20261006_2302.dump` y `uploads_20261006_2302.tar.gz`, con sus tamaños de la Fase 3: 4.065.098 B y 342.517 B.

### 2. Checkpoint de aprobación (obligatorio)
Muestra al usuario:
- **qué se pierde:** las operaciones QA-S6, las cuentas `qa.*`, las tarifas de prueba y la factura de O-3;
- **el aviso de la contraseña del Admin:** con la restauración, **el Admin vuelve a la contraseña que tenía a las 23:02 del 06/10**, anterior al cambio del re-test, que ya no está guardada. Después de restaurar, el usuario la cambia con la recuperación por correo, que ya funciona (paso 4);
- **los comandos exactos** de los pasos 3 y 4.

**Espera el «sí» del usuario en el chat.** Sin él, detente.

### 3. Restauración
1. Detén solo el contenedor del API: `docker compose stop wms-api`.
2. Restaura la base con `pg_restore --clean --if-exists` dentro de `wms-staging-postgres-1`, sobre la base de staging, siguiendo el README.
3. **Archivos subidos:**
   - **verifica primero la carpeta real del host.** `compose.staging.yaml` monta `/opt/wms/data/uploads:/app/wwwroot/uploads`, y el README dice `/opt/wms/uploads`;
   - **corrige el README** si está mal;
   - mueve el contenido actual a `/opt/wms/data/uploads.antes-f5/`, **sin borrarlo**;
   - extrae el `uploads_20261006_2302.tar.gz`, con dueño UID 1654.
4. Arranca el API y revisa el log.

### 4. Verificación de la restauración y del Admin
- **Base:**
  - 11 migraciones;
  - **128 depósitos «Confirmed»**;
  - **128 facturas de almacenamiento en Borrador por $91.257.475,39**;
  - 9 ubicaciones, con `Bodega 1 BA-[1][1]` No disponible;
  - **0** entradas, ciclos, órdenes y guías;
  - **1 usuario (`admin`)**;
  - tarifas T1 a T4;
  - **0 tarifas de montacargas**;
  - el destino de respaldo presente.
- **Contraseña del Admin:**
  1. Pide la recuperación del `admin` desde la pantalla de login.
  2. **El usuario abre el enlace del correo y fija una contraseña nueva.**
  3. **El usuario la guarda en `db_legacy/trabajo/.admin-staging.local`** (permisos 600) y te avisa.
  4. Verifica el login.
- **Respaldos:** un respaldo manual «staging restaurado» con resultado `Succeeded`.

### 5. Tarifas de montacargas (F5-2)
- Cárgalas con el Admin por el API, con el mismo contrato que la pantalla de tarifas de montacargas (`forklift-rates`).
- Verifica que la pantalla las muestra.
- Prueba **una** liquidación en la vista previa, si el API la ofrece sin crear datos.

### 6. Cuentas de los operarios (F5-3)

| Usuario | Rol | Correo |
|---|---|---|
| `operario.vigilancia` | Operario vigilancia | `capb.dev+operario.vigilancia@gmail.com` |
| `operario.bascula` | Operario báscula | `capb.dev+operario.bascula@gmail.com` |
| `operario.bodega` | Operario bodega | `capb.dev+operario.bodega@gmail.com` |
| `operario.comext` | Comercio exterior | `capb.dev+operario.comext@gmail.com` |
| `operario.facturacion` | Facturación | `capb.dev+operario.facturacion@gmail.com` |

- **Cómo crearlas:** reutiliza el patrón del script `db_legacy/trabajo/crear-cuentas-qa-staging.sh` (contraseña fuerte, sin imprimir nada). Haz una copia, `crear-cuentas-operarios-staging.sh`, que guarde las contraseñas en `db_legacy/trabajo/credenciales-operarios-staging.local.md` (600).
- **Esta vez NO quites el cambio obligatorio:** cada operario fija su propia contraseña en el primer ingreso.
- **Contraseñas:** no las escribas en el chat ni en informes. Dile al usuario dónde están.
- **Si el entorno no te deja ejecutar el script,** déjalo listo y pídele al usuario que lo ejecute, como en la Fase 4.

### 7. Datos de práctica (del legacy, por el API, sin SQL)
- **Usa vehículos, conductores y clientes migrados.**
- **Marca los datos de práctica** con «PRÁCTICA» en las observaciones o notas, y los documentos o cartas porte nuevos con el prefijo `PRAC-`.
- **Crea solo lo necesario** para que cada rol tenga algo que hacer desde el primer ingreso. Usa las cuentas `operario.*`, para que la auditoría muestre al autor de cada rol:

| # | Escenario | Qué dejar listo | Para |
|---|---|---|---|
| P1 | Importación nueva | Un ingreso en Vigilancia de un vehículo migrado con su conductor, motivo «Descargue importación», en la cola de báscula «Sin iniciar» | Báscula, Bodega, Comercio Exterior y Facturación |
| P2 | Solo báscula | Un ingreso con motivo de solo pesaje, en la cola | Báscula |
| P3 | Salida de un depósito migrado | Un depósito migrado **nacionalizado con stock**, con una **OC pendiente** creada por Comercio Exterior y un ingreso de cargue en Vigilancia | Báscula, Bodega, Comercio Exterior y Facturación |
| P4 | Levante pendiente | Elegir un depósito migrado **sin nacionalizar** con stock, solo identificarlo, sin operarlo | Comercio Exterior |
| P5 | Factura de almacenamiento | Elegir 2 facturas de almacenamiento en Borrador de depósitos migrados, sin tocarlas | Facturación |
| P6 | PRF-002 | Un ingreso más en la cola, con datos precargados, para el cronometraje | El operario de báscula, con el usuario |

- **Exportación e inspección:** en el legacy no había depósitos vivos de esas modalidades. **No crees datos de esas modalidades;** la guía explica cómo empezar uno desde báscula.
- **No uses** BA0042 ni BA0558 para P3 y P4: elige otros.
- **Lista en el informe** cada dato creado o elegido, con su número de depósito, placa, OC y factura.

### 8. Guía de pruebas para operarios
**Archivo:** `docs/planes/migracion-staging/resultados/guia-pruebas-operarios.md`, en español, para personas que no son técnicas.

**Contenido general:**
- La URL de la aplicación.
- **Avisos importantes:**
  - **los datos son reales del legacy a junio de 2024, con un corte simulado:** la facturación arranca el 01/10/2026. No se deben usar para operar de verdad;
  - los 66 depósitos que aparecen «en abandono» son esperables;
  - «Estadísticas» no está en el menú, por decisión del usuario;
  - **la recuperación de contraseña por correo es solo para el Admin.** Si un operario olvida la suya, el Admin se la restablece;
  - el primer ingreso pide cambiar la contraseña.
- **Cómo reportar un problema:** qué anotar (pantalla, hora, qué hizo, qué esperaba, captura) y a quién enviarlo: al usuario, por el canal que él indique. Deja ese dato como `[completar]` si no lo sabes.

**Una sección por rol** con:
- el usuario, **sin contraseña**: «la contraseña inicial se la entrega el administrador»;
- su pantalla de inicio;
- **pasos concretos con los datos de práctica del paso 7**;
- qué debería ver al terminar cada paso;
- y otros flujos para explorar por su cuenta.

**Una sección para PRF-002:** cómo medir el registro en báscula con el escenario P6, el criterio (registro en báscula en 30 s o menos) y una tabla para anotar los tiempos. Incluye F3-REG-024 y F3-PES-015.

**Una tabla final** de datos de práctica con su estado inicial.

### 9. Respaldo «listo para operarios» y cierre
- **Respaldo manual** al terminar, con resultado `Succeeded`. Anota su nombre: es el **punto de restauración para repetir las pruebas** de los operarios desde cero. Documenta en la guía, para el administrador, cómo volver a él.
- **Respaldo programado de las 02:00** (pendiente desde la Fase 4):
  - si la sesión pasa por esa hora, verifica que corrió;
  - si no, déjalo anotado para revisar con `GET administration/backups/runs` al día siguiente.
- **Limpieza de imágenes viejas del API** (`docker image prune`): solo con el «sí» del usuario.

## Reglas (obligatorias)
- **Producción no se toca.**
- **Staging:**
  - la única acción destructiva es la restauración, **con el «sí» del paso 2**;
  - no hay SQL de escritura;
  - no se borran volúmenes;
  - los archivos subidos anteriores se mueven, no se borran.
- **Sin secretos:** ni contraseñas, ni tokens, ni valores de `.env`. Las credenciales se leen de los archivos locales sin imprimirlas.
- **Datos reales:** la guía y el informe citan depósitos por número y vehículos por placa, que son datos operativos de prueba. **Nunca** llevan nombres, documentos ni teléfonos de personas naturales: los conductores se citan como «conductor migrado del vehículo X».
- **No cambies código.** Solo puedes tocar `deploy/staging/README.md`, si la ruta de los archivos subidos está mal, y los documentos de `docs/planes/migracion-staging/`.
- **Sin commits:** entrega los mensajes.
- Textos en español.

## Entrega y detención
1. **Informe de entrega** `docs/planes/migracion-staging/resultados/informe-fase-5.md`:
   - respaldos (antes de F5, restaurado y listo para operarios);
   - la aprobación con su hora;
   - la restauración y su verificación;
   - el Admin;
   - las tarifas de montacargas;
   - las cuentas;
   - los datos de práctica;
   - la guía;
   - el respaldo de las 02:00;
   - **el estado final de staging;**
   - los pendientes: PRF-002 con el operario y la decisión sobre vaciar o anonimizar staging al terminar las pruebas (§9 del plan).
2. **La guía** `guia-pruebas-operarios.md`.
3. **El plan:** la Fase 5 «Completada» en la tabla del §1.
4. **Los mensajes de commit:**
   - `docs(migracion): fase 5, staging listo para operarios con datos migrados y guía de pruebas`;
   - si cambió el README, `docs(staging): ruta correcta de los archivos subidos en la restauración`.

   Los dos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí.**
