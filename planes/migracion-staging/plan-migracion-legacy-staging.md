# Plan: migración de datos legacy, despliegue y pruebas en staging

> **Fecha:** 2026-10-06.
> **Build de partida:** FE `24d742d` / BE `f6f1828`. Es el candidato con «GO condicionado» del informe final del QA (`docs/qa/resultados/informe-final.md`).
> **Objetivo:** cumplir las dos condiciones que faltan para el GO:
> - la migración de datos (Anexo A del QA, más E19 «datos reales» de la Fase 6 de paridad);
> - el bloque de staging (§8 del informe final, con PRF-002).
>
> Al final, staging queda listo para que los operarios prueben con datos reales migrados.

## 1. Fases y seguimiento

| Fase | Qué se hace | Dónde | Modelo | Estado |
|---|---|---|---|---|
| **1** | Migrar el legacy a una base local limpia y validarla | Local | Opus 5.5 | Ejecutada el 2026-10-06: **No OK** por DEF-MIG-005 (`resultados/informe-fase-1.md`). Repetida el mismo día con las consultas corregidas: **OK**, con DEF-MIG-001 a 006 verificados y DEF-MIG-007 abierto, que no bloquea la fase 2 (`resultados/informe-fase-1-repeticion.md`) |
| **2** | Preparar y hacer el despliegue a staging | Staging | Sonnet 5.5 | Ejecutada el 2026-10-06 con BE `bf2dea6` / FE `4799cc4`: base recreada con 10 migraciones, respaldos activos y Gmail. Falta que el usuario cambie la contraseña del `admin` y cree el destino Local (`resultados/informe-fase-2.md`) |
| **3** | Migrar el mismo legacy a staging | Staging | Sonnet 5.5 | Ejecutada el 2026-10-06 con BE `b31ddb6` / FE `508b91b`: **idéntica a local** (12 entidades, 133 «Ok», 128 «Opened», primer período $91.257.475,39). Sin defectos nuevos; respaldo «staging migrado» `wms_20261006_2302.dump` (`resultados/informe-fase-3.md`) |
| **4** | QA en staging (sesión S6) | Staging | Opus 5.5 | Ejecutada el 2026-10-06/07 con BE `b31ddb6` / FE `508b91b`: **sin FALLA en P0**. F0, REG-001 a 013, E2E-01, la DIAN real (361 ms), el humo, FA-MIG-009 por rol y FB-BAK-005 en PASA. DEF-MIG-005/007/008 verificados en staging. Fichas nuevas: DEF-F11-021 (MAJOR, enlace de recuperación) y DEF-F11-020 (MINOR, respaldos simultáneos). PRF-002 queda para un operario (camión QSP001 preparado). Tarifas de montacargas de prueba configuradas con autorización. Veredicto: **GO condicionado solo a PRF-002** (`docs/qa/resultados/F11-informe-S6-2026-10-06.md`). **Redespliegue del 2026-10-07** con BE `84c712f` / FE `8527144`, sin recrear la base (11 migraciones, sin nuevas; `pgdata` intacto; Caddy recargado): DEF-F11-021 (incluido el enlace real del correo del Admin y F0-LOG-008), DEF-F11-020 y O-3 **verificados en staging**, sin fichas abiertas. Respaldos `wms_20261007_0103.dump` antes y `wms_20261007_011429_5fa2939e.dump` después (`docs/qa/resultados/evidencias/F11/RT-S6-redespliegue-retest.txt`) |
| **5** | Dejar staging listo para los operarios | Staging | Sonnet 5.5 | **Completada** el 2026-10-07 con BE `84c712f` / FE `8527144`:<br>• **Sin restaurar:** el usuario revocó F5-1 en el checkpoint, y los datos QA-S6 quedan como ejemplo.<br>• Tarifas reales de montacargas.<br>• 5 cuentas `operario.*` con cambio obligatorio de contraseña.<br>• Datos de práctica P1 a P6 creados con las cuentas de cada rol.<br>• Guía por rol (`resultados/guia-pruebas-operarios.md`).<br>• Respaldo «listo para operarios» y corrida de las 02:00 verificada.<br>• Pendientes: PRF-002 con un operario y la decisión de vaciar o anonimizar staging (`resultados/informe-fase-5.md`).<br>• **Redespliegue del 2026-10-08 (selector de conductor):** BE `044be08` / FE `4ca4e0a`, sin recrear la base y **sin migraciones** (siguen 11; `pgdata` y `caddy_data` intactos). Respaldos `wms_20261008_151727_77114401.dump` antes y `wms_20261008_154700_53e8fdc1.dump` después. QA S1-S9 en PASA; DEF-F11-022, 025 y 027 verificados; 3 MINOR conocidos abiertos (023, 024 y 026). Veredicto: **Verificado en staging**. PRF-002 debe medirse con este build (`docs/qa/resultados/SEL-informe-2026-10-08.md`, sección «Staging») |

- **Cada fase tiene su prompt en esta carpeta** (`prompt-fase-N.md`) y la ejecuta un agente nuevo.
- **Cada fase termina en un checkpoint:** el agente se detiene y el usuario decide si sigue.
- **La fase 2 solo empieza si la fase 1 sale OK** (§4).
- **Si una fase encuentra defectos de código,** el ejecutor no corrige. Abre fichas `DEF-MIG-NNN` y un implementador aparte las corrige con su propio prompt, como en el plan de corrección del QA. Después, la fase se re-ejecuta en lo que corresponda.

## 2. Decisiones del usuario (2026-10-06)

| # | Decisión |
|---|---|
| D1 | **v2 arranca con datos migrados del legacy.** Fuente de prueba: `code_workspace/db_legacy/backupBodegas.sql` (MariaDB 10.1.38, 4,4 GB, completo, «Dump completed on 2024-06-10»). **`db.sql` no se usa:** está truncado, termina en bytes basura y difiere de `backupBodegas.sql` a partir de los 3,7 GB. |
| D2 | **Corte simulado.** El backup es de junio de 2024. Para no generar unos 28 meses de períodos atrasados por depósito, en los CSV de depósitos el «último fin facturado» de cada depósito se lleva a la **fecha de corte de prueba `2026-09-30`**, de modo que la facturación arranca el `2026-10-01`. Se documenta como ajuste de prueba: los datos originales del dump no se modifican y el ajuste se hace solo en el CSV. |
| D3 | **Tarifas y convenios los carga el agente** desde el legacy, por el API, con informe de lo que no pudo mapear. En el esquema, las tablas `tarifa` y `convenio` tienen contadores de 2 y 3 registros, así que es probable que las tarifas reales estén en otro lado: las facturas (`facturaciigo`/`detallefactura`), `cliente.dias_facturacion` o el código PHP de `bodegas-legacy`. **El agente propone el mapeo y lo aprueba el usuario antes de cargarlo** (checkpoint de la fase 1). |
| D4 | **El correo de staging es Gmail real.** Condición: los correos solo pueden llegar a direcciones que controle el usuario. Las cuentas de prueba y `NOTIFICATIONS_ADMIN_EMAILS` usan las direcciones que el usuario indique. Los terceros migrados no traen correo (el importador de clientes no tiene esa columna); si algún flujo enviara correo a un tercero, se reporta antes de seguir. |
| D5 | **Una cuenta por rol** para los operarios: Vigilancia, Báscula, Bodega, Comercio Exterior, Facturación y un Admin. Cada una con contraseña temporal que exige cambiarla al primer ingreso. Las contraseñas quedan **solo** en un archivo local fuera de los repositorios (`code_workspace/db_legacy/trabajo/credenciales-staging.local.md`), nunca en el chat, los informes ni git. |
| D6 | **La base local de la migración es nueva** (`wms_migracion`, en el contenedor `wms-postgres-db`). **La base `wmsdb` del QA no se toca**, porque es la evidencia del cierre de la fase 11. |

## 3. Reglas comunes (todas las fases)

1. **Datos reales fuera de git.**
   - El dump, la base MariaDB, los CSV exportados y cualquier extracto con datos de terceros viven solo en `code_workspace/db_legacy/trabajo/`, que no es repositorio.
   - Los informes en git (`docs/planes/migracion-staging/resultados/`) llevan **conteos, números de depósito y códigos**. No llevan nombres, documentos, teléfonos ni direcciones de personas naturales. Las razones sociales de empresas solo se usan cuando hagan falta para explicar una diferencia.
2. **Sin secretos.** No se imprimen ni se copian los valores de `.env.staging`, `.env.deploy`, la contraseña del administrador inicial ni las contraseñas temporales. Para revisar una configuración, se nombran las claves sin mostrar sus valores.
3. **La migración se hace solo con la herramienta del producto:** los endpoints `administration/legacy-import/*` y `administration/cities/import`, con el usuario Admin y siempre simulación (`dryRun=true`) antes del firme.
   - **En la base v2 no se escribe con SQL.**
   - El SQL de lectura se permite en local para verificar.
   - En staging no hay SQL directo; todo va por el API y la pantalla. La única excepción es el script `migrate` de despliegue, que aplica las migraciones de EF.
4. **Orden de carga del corte** (`docs/planes/paridad-legacy/plan-backend-paridad-legacy.md` §C.6.1):
   1. ciudades
   2. embalajes
   3. cuadrillas
   4. ubicaciones
   5. clientes, agencias y transportadoras
   6. vehículos
   7. conductores
   8. productos
   9. depósitos vivos
   10. levantes
   11. conciliación
   12. tarifas y convenios
   13. apertura de la facturación (`open-billing`)
5. **Consultas de exportación:** las de `plan-backend-paridad-legacy.md`.
   - F6-02 (≈ líneas 2815-2850) para los maestros.
   - F6-03 (≈ 2938-3011) para depósitos y levantes.
   - Desde la corrección de DEF-MIG-001 a 004 (2026-10-06), la consulta de depósitos ya calcula `saldo` y `trm_ingreso` y exporta `valor_mercancia` y `moneda`; la de levantes filtra por `id_deposito` y no agrupa.
   - Desde la corrección de DEF-MIG-008 (2026-10-06), la consulta de ubicaciones parte de `bodega` con `LEFT JOIN seccion`: salen las 9 bodegas activas, una fila por sección (6) y una por bodega sin sección (Cobertizo, Patio 1 BA y Patio 2 BA). Exporta además `ocupacion` (6.ª columna; `deshabilitado` entra No disponible) e `id_bodega` (7.ª; la bodega sin sección entra con id legacy `B{id_bodega}`), con `ORDER BY B.id_bodega, S.id_seccion`. El importador sigue aceptando el CSV de 5 columnas.
   - **Por eso el CSV de ubicaciones del conjunto v2 deja de estar congelado** (regla 7) hasta la recarga: se regenera con la consulta nueva, se le saca el hash nuevo y se anota en `resultados/registro-csv-fase-1.md`. Los demás CSV del conjunto v2 siguen congelados.
   - Se excluyen `estado='eliminado'` y Colmotores (cliente 70 y bodegas con `uso='colmotores'`).
   - Si el agente cambia una consulta, guarda la versión usada y la diferencia en `db_legacy/trabajo/consultas/` y la explica en el informe.
6. **Límites de la herramienta.** Hasta 50.000 filas por archivo; si un archivo se pasa, se parte. Separador `;`, codificación UTF-8 o Windows-1252.
7. **Los mismos CSV en local y en staging.** El conjunto que sale OK en la fase 1 se congela (con su hash SHA-256) y es el que se carga en la fase 3.
8. **Producción no se toca.** Cada acción destructiva en staging necesita la aprobación explícita del usuario en el chat en ese momento: recrear la base, borrar volúmenes o sobrescribir datos.
9. **Trabajo en `develop`, sin ramas.** Los agentes no hacen commits: entregan los mensajes y el usuario hace los commits.
10. **Textos en español.**

## 4. Fase 1 — Migración en local (criterio «OK» para seguir)

**Preparar la fuente.**
- Contenedor MariaDB 10.x nuevo, solo para esto: `legacy-mariadb`, puerto 3308. Se carga `backupBodegas.sql` en la base `bodegas`.
- Se verifican los conteos de las tablas clave contra los `AUTO_INCREMENT` y los `INSERT` del dump.
- No se usa el contenedor `mysql57`, que es de otro proyecto.

**Base v2 limpia.**
- `wms_migracion`: `dotnet ef database update` contra esa base. El API local se corre apuntando a ella con `ConnectionStrings__DefaultConnection` por variable de entorno, sin tocar `appsettings`.
- El administrador inicial se crea con `Bootstrap__*` por variables de entorno.

**Exportación.**
- CSV por entidad con las consultas del §3.5, más el ajuste D2 en los depósitos.
- Se registra cada CSV con su consulta, filas y hash.

**Carga.**
- Simulación de cada entidad en orden; luego firme en orden.
- Prueba de idempotencia: recargar un maestro y los depósitos no duplica.
- Conciliación contra los CSV.
- Tarifas y convenios (D3, con checkpoint de aprobación del mapeo).
- `open-billing`.

**Verificación.**
- Anexo A del QA, FA-MIG-001 a 010 (`docs/qa/fase-11-regresion-cierre.md` §Anexo A).
- E19 «datos reales» (`bodegas-legacy/docs/legacy_analysis/ROADMAP.md` 6.6):
  - saldos antes y después de un levante, un despacho, una anulación y un cargue;
  - períodos con fechas límite;
  - recorrido por rol.
- Cotejo de una muestra de **30 depósitos** contra el legacy: cliente, productos, recibido, despachado, saldo, levantes, modalidad y manifiesto.
- Una operación nueva completa sobre un depósito migrado: levante → OC → cargue → guía → factura.

**Criterio OK** (todos se cumplen):

| # | Criterio |
|---|---|
| OK-1 | Las 12 entidades cargadas en firme. Cada fila rechazada tiene causa documentada y aceptada: dato inválido en el legacy, exclusión por regla o duplicado legítimo. **0 rechazos por defecto de la herramienta.** |
| OK-2 | Conciliación con **0 diferencias sin explicar**: todo depósito vivo del CSV queda «Ok», o con su causa. |
| OK-3 | Idempotencia: la segunda carga no crea duplicados. |
| OK-4 | Muestra de 30 depósitos: 100 % coincide con el legacy en saldo por producto, levantes y cliente. |
| OK-5 | Tarifas: cada depósito con facturación abierta queda «Opened», o «Skipped» con causa. El primer período arranca el 2026-10-01 (D2) y su importe es coherente con la tarifa mapeada. |
| OK-6 | FA-MIG-001 a 010 y E19 sin FALLA, salvo las notas ya conocidas: FA-MIG-002 y FA-MIG-010. |
| OK-7 | La operación nueva sobre un depósito migrado funciona de punta a punta, con saldos correctos. |
| OK-8 | Tiempos anotados: cuánto tarda cada carga. Sirven para planear la ventana del corte real. |

Si un criterio falla por defecto de la herramienta: ficha `DEF-MIG-NNN`, corrección aparte y re-ejecución de la fase 1 desde una base limpia.

## 5. Fase 2 — Preparar y desplegar staging

1. **Inventario del estado actual** del servidor: contenedores, base, volúmenes, versión desplegada y espacio en disco. Todo de solo lectura.
2. **Configuración.** Revisa las claves de `.env.staging` sin mostrar valores:
   - SMTP de Gmail (D4);
   - `NOTIFICATIONS_ADMIN_EMAILS` con las direcciones que indique el usuario;
   - `BOOTSTRAP_ADMIN_*`.

   Los valores los pone el usuario.
3. **Respaldos (recomendado).** Agregar las variables `Backups__*` a `compose.staging.yaml` con un destino Local. Hoy faltan (FB-BAK-006). Es un cambio de configuración versionado: el agente lo deja listo y el usuario lo commitea.
4. **Artefactos.**
   - Regenerar `deploy/staging/artifacts/staging.sql` con `dotnet ef migrations script --idempotent`. El de julio es obsoleto: tiene la cadena de migraciones anterior a `InitialParityLegacy`.
   - Reconstruir la imagen con `Dockerfile.staging` (incluye `postgresql-client-18` para respaldos).
   - Generar el frontend.
5. **Checkpoint de aprobación (obligatorio).** Recrear la base de staging borra lo que haya. El agente muestra qué se pierde y espera el «sí» del usuario.
6. **Despliegue** con `scripts/deploy-staging.sh` (`config`, `backend`, `frontend`, `dbup`, `migrate`, `up`) y `smoke`.
7. **Verificación:**
   - `__EFMigrationsHistory` con las 10 migraciones;
   - 6 roles del sistema;
   - login del Admin;
   - CORS;
   - página de error en español;
   - Swagger apagado;
   - envío de un correo de prueba a una dirección del usuario (recuperación de contraseña del Admin).

## 6. Fase 3 — Migración en staging

- Los **mismos CSV congelados** de la fase 1 (se verifica el hash), por el API de staging (HTTPS), con el Admin y en el mismo orden: simulación y luego firme.
- Las mismas tarifas y convenios aprobados en la fase 1, por el API.
- Conciliación y `open-billing`.
- **Comparación con local:** conteos por entidad, depósitos «Ok» y totales del primer período de facturación. Deben ser **idénticos** a la fase 1; toda diferencia se explica.
- Una muestra de 10 depósitos revisada en pantalla.

## 7. Fase 4 — QA en staging (sesión S6)

- **Alcance:** §8 del informe final del QA.
  - **F0 completo** (37).
  - **F11-REG-001 a 013.**
  - **E2E-01.**
  - **La DIAN real:** F6-TRM-001, con la salida a internet y un tiempo de 3 s o menos.
  - **Las diferencias propias de staging:** correo, Swagger y respaldos.
  - **Humo de las últimas correcciones:** F2-COR-011, F6-REC-002, F3-RPT-001 y F3-CIC-001.
- Además, **FA-MIG-009 en staging:** el recorrido por rol con los datos migrados.
- **PRF-002:** el agente prepara el escenario (camión y datos precargados) y una hoja para anotar tiempos. **El cronometraje lo hace un operario real** con el usuario; el agente registra los resultados que le dé el usuario. Criterio: 30 s o menos.
- **Datos que crea QA:** solo con prefijo `QA-S6` (placas, documentos, notas), para no mezclarlos con los migrados. Las palancas de SQL no existen en staging: los casos que las necesiten se marcan «No aplica en staging», con la evidencia local.
- **Al cerrar:** se actualiza el informe final.
  - Si no hay FALLA en P0 y PRF-002 cumple, el veredicto pasa a **GO**.
  - Si no, queda en GO condicionado, con las causas.

## 8. Fase 5 — Staging listo para los operarios

1. **Limpieza de QA:** las operaciones `QA-S6` que queden abiertas se cierran o anulan **por la pantalla o el API**: registrar la salida, anular o descartar. No se borra nada con SQL. Lo que no se pueda cerrar se lista.
2. **Cuentas:** una por rol (D5), con el correo que indique el usuario. El archivo local de credenciales queda en `db_legacy/trabajo/` y en el chat solo se informa que está ahí.
3. **Datos de prueba para los operarios**, extraídos del legacy y creados por el API, sin SQL:
   - camiones en planta para practicar cada flujo, usando vehículos y conductores migrados:
     - ingreso → báscula → bodega (importación);
     - exportación;
     - Solo báscula;
     - salida con orden de cargue de un depósito migrado;
   - un depósito migrado de cada modalidad, con levante pendiente;
   - una factura de almacenamiento del período de octubre lista para numerar y aprobar;
   - un cliente con convenio.

   Cada dato queda en la guía.
4. **Guía de pruebas para operarios** (`resultados/guia-pruebas-operarios.md`):
   - una sección por rol con la URL, el usuario (sin contraseña) y qué probar paso a paso, con los datos concretos del punto 3;
   - cómo reportar un problema;
   - **el aviso de que los datos son reales del 2024 con corte simulado y que no se deben usar para operar.**
5. **Respaldo** de la base de staging ya preparada, si se activaron los respaldos en la fase 2: el punto de restauración para repetir las pruebas.
6. **Informe de entrega** con el estado final de staging.

## 9. Riesgos

| Riesgo | Mitigación |
|---|---|
| Staging es accesible desde internet y tendrá datos reales de clientes. | El usuario lo aceptó como ambiente de pruebas. Se mitiga con contraseñas fuertes, cambio obligatorio al primer ingreso, cuentas solo para el equipo, Swagger apagado y ningún dato real en git. Al terminar las pruebas, se evalúa vaciar staging o anonimizarlo. |
| Gmail real puede escribir a personas reales. | Solo direcciones del usuario en las cuentas y en `NOTIFICATIONS_ADMIN_EMAILS`. Antes de cargar, el agente verifica que los terceros migrados no tienen correo y que ningún aviso se envía a terceros. |
| La herramienta de importación nunca se probó con datos reales (E19). | La fase 1 es justo esa prueba. Si hay defectos, se corrigen con fichas `DEF-MIG` antes de staging. |
| Las tarifas del legacy pueden no estar en `tarifa`/`convenio`. | D3: el agente investiga la fuente real y el usuario aprueba el mapeo. |
| Los datos son de junio de 2024, no del corte real. | La fase sirve para validar la herramienta y el proceso. El corte real necesita un dump nuevo y repetir la fase 1 y la fase 3 con él. Los tiempos de OK-8 ayudan a planear esa ventana. |
| La memoria y el disco de staging (Lightsail, 4 GB). | Inventario en la fase 2; el dump y MariaDB **no** van a staging. Solo van los CSV, del orden de MB. |

## 10. Entregables

- `docs/planes/migracion-staging/resultados/`: un informe por fase, el registro de CSV (nombres, filas y hash) y el mapeo de tarifas aprobado.
- **Fichas `DEF-MIG-NNN`,** si las hay. Plantilla: `docs/qa/plantillas/defecto.md`.
- **QA de staging:** `docs/qa/resultados/F11-informe-S6-*.md` y el informe final actualizado.
- `resultados/guia-pruebas-operarios.md`.
- Fuera de git, en `db_legacy/trabajo/`: los CSV, las consultas usadas, los extractos y las credenciales locales.
