Eres el ejecutor de QA de la **continuación de la Fase 4 — QA en staging (sesión S6)** del plan `docs/planes/migracion-staging/plan-migracion-legacy-staging.md` del WMS de Bodegas Asociadas. Modelo recomendado: **Opus 5.5**.

Un agente anterior hizo la mayor parte de las pruebas con el Admin, pero **no terminó**:
- no se crearon las cuentas por rol, así que no se probó nada con permisos de rol;
- no se escribieron el informe S6 ni las fichas;
- no se actualizó el informe final.

Tu trabajo es **completar lo que falta sin repetir lo ya hecho** y cerrar la sesión.

## Lee primero
1. **El prompt original de la fase:** `docs/archivo/prompts/migracion-staging/prompt-fase-4.md`. Sus reglas valen aquí sin cambios:
   - los datos que crea QA llevan la marca QA-S6;
   - las operaciones sobre datos migrados se limitan a BA0042 y BA0558;
   - en staging no hay SQL de escritura;
   - no hay secretos ni datos de personas en los informes.
2. **La evidencia de lo ya ejecutado,** en `docs/qa/resultados/evidencias/F11/`:
   - `S6-F0-sin-sesion-y-linea-base.txt`;
   - `S6-A-admin-api.txt`;
   - `S6-A-E2E-REG-operaciones.txt`;
   - `S6-C-FB-BAK-005-restauracion.txt`.

   **Lo que está ahí se da por ejecutado:** lo resumes y lo citas en el informe, sin volver a correrlo.
3. **El marco de QA** (`docs/archivo/prompts/qa/prompt-qa-fase-11-retest.md`) y el informe final (`informe-final.md` §7 y §8).

## Estado que dejó el agente anterior (de la evidencia)
- **Hecho con el Admin:**
  - F0 sin sesión, CORS, Swagger apagado y las lecturas del API;
  - las 66 rutas del menú del Admin;
  - REG-003 y REG-004;
  - E2E-01 completo, con la DIAN real (TRM 3.209,78 en 361 ms);
  - REG-005, 008, 011, 012 y 013;
  - F2-COR-011, F6-REC-002, F3-RPT-001 y F3-CIC-001;
  - DEF-MIG-005 y DEF-MIG-007 en BA0042 y BA0558, más la factura de BA0042 aprobada;
  - FB-BAK-003;
  - FB-BAK-005, autorizado por el usuario y restaurado en una base aparte que después se borró.
- **Hallazgos sin ficha todavía:**
  1. **FB-BAK-003:** dos `POST administration/backups/run` **simultáneos** dan 202 y 202, y las dos corridas escriben el mismo `.dump`. El agente lo nombró «DEF-F11-020», pero la ficha no existe.
  2. **`start-pending-billing` de báscula** responde `totalAmount = 19999.9968`, sin redondear. La corrección O-3 (commit `ae36ac9`) cubrió los inicios de báscula, pero no este camino.
  3. **B.4:** con un Id que no existe, la página muestra el error y el botón «Volver», pero **el subtítulo del encabezado queda en «Cargando…»**.
  4. **Montacargas sin tarifa en staging.** El cierre del uso responde 404 «No hay tarifa de montacargas configurada…», y **el uso del montacargas sobre 2026BA00001 (QA-S6) quedó abierto**. El mapeo de tarifas aprobado (T1 a T4) no incluyó montacargas.
- **Falta:**
  - las cuentas `qa.*`;
  - todo lo que se prueba **por rol**;
  - **F3-REI-007**, porque QSB202 quedó «Por repesar» para hacerlo con `qa.bascula`;
  - las confirmaciones de correo del usuario;
  - el escenario de PRF-002;
  - las fichas;
  - el informe S6, el informe final y el plan.

## Pasos

### 0. Cuentas `qa.*`
- El agente anterior dejó el script `code_workspace/db_legacy/trabajo/crear-cuentas-qa-staging.sh`, para que lo ejecute el usuario. Es idempotente y no imprime contraseñas; las guarda en `credenciales-qa-staging.local.md`, con permisos 600.
- **Si ese archivo de credenciales no existe, pídele al usuario que ejecute el script** y espera. No lo ejecutes tú salvo que el usuario te lo pida.
- Después, verifica con el Admin que existen las 5 cuentas, cada una con su rol y su alias de correo.
- **Revisa los permisos de `code_workspace/db_legacy/trabajo/.admin-staging.local`.** Si no está en 600, pídele al usuario que lo corrija con `chmod 600`.

### 1. Lo que falta del bloque STG, por rol
Con las cuentas `qa.*` (las contraseñas se leen del archivo sin imprimirlas):

1. **F0-LOG y F11-REG-001:** login de cada rol con su ruta de inicio, cierre de sesión y «Atrás».
2. **F0-NAV y F11-REG-002 por rol:** el menú de cada rol, las páginas permitidas que cargan y las demás con «Acceso Denegado». «Estadísticas» oculto es lo esperado.
3. **F11-REG-006 y 007** con Vigilancia, Báscula y Bodega, y **F11-REG-009 y 010** con Báscula. Usa datos QA-S6 nuevos y cita lo que ya cubrió el Admin.
4. **F3-REI-007:** el repesaje de QSB202 con `qa.bascula`.
5. **FA-MIG-009 por rol,** con los datos migrados y solo lectura:
   - **Comercio Exterior:** detalle de 5 depósitos migrados, abandono y kanban;
   - **Bodega:** inventario y las 9 ubicaciones, con `Bodega 1 BA-[1][1]` deshabilitada;
   - **Facturación:** las facturas de almacenamiento en Borrador y la de BA0042 aprobada;
   - **Báscula y Vigilancia:** búsqueda de un vehículo y de un conductor migrados.

### 2. Correo real
Pídele al usuario que confirme en su bandeja de `capb.dev@gmail.com`:
- el correo del CE-7 de F6-REC-002, enviado a la dirección del administrador;
- el de la orden 2026OC00001 cargada;
- y una **recuperación de contraseña de `qa.comext`**, que debe llegar a su alias.

Anota fecha y asunto. **No abras los enlaces.**

### 3. Escenario de PRF-002 (lo mide un operario, no tú)
- Deja **un camión QA-S6 en la cola**, con placa `QS` y un vehículo y conductor migrados o QA-S6 con datos precargados, listo para que el operario registre un ingreso IMP mínimo.
- Escribe en el informe las instrucciones para el operario y la hoja para anotar los tiempos:
  - registro en báscula, que debe ser de **30 s o menos**;
  - tiempo hasta el primer peso;
  - F3-REG-024 y F3-PES-015.

### 4. Fichas
En `docs/qa/resultados/defectos/`, con la plantilla:

| Ficha | Severidad sugerida | Contenido |
|---|---|---|
| **DEF-F11-020** | MAJOR | Respaldos concurrentes. Revisa en el código si el bloqueo «Ya hay un respaldo en curso» solo funciona después de que la primera corrida queda registrada. Pon la pista técnica. |
| **DEF-F11-021** | MINOR | `start-pending-billing` responde el total sin redondear. Es el resto de O-3, con la pista técnica. |

- **El subtítulo «Cargando…»:** ficha **TRIVIAL** solo si confirmas que el encabezado se queda así; si no, va como observación.
- **El montacargas:** **no abras ficha.** Es configuración: falta la tarifa. Regístralo como **decisión pendiente del usuario** en el informe y en el plan: cargar la tarifa de montacargas del legacy o una de prueba, y cerrar o anular el uso abierto de 2026BA00001.

### 5. Informes
1. **El informe S6:** `docs/qa/resultados/F11-informe-S6-2026-10-06.md`, con la estructura de S1 a S5. Incluye:
   - todo lo ejecutado por el agente anterior, citando su evidencia;
   - todo lo tuyo;
   - los datos creados, con las operaciones sobre BA0042 y BA0558;
   - el respaldo «staging migrado» intacto y la restauración de prueba;
   - las decisiones pendientes;
   - el checkpoint.
2. **El informe final** (`informe-final.md`):
   - **§1 y §2.2:** la fila de S6.
   - **§7, veredicto:**
     - sin FALLA en P0 y sin CRITICAL ni BLOCKER abiertos → «**GO condicionado** a PRF-002 (medición con un operario)»;
     - lista también los MAJOR abiertos (DEF-F11-020) como «corregir o aceptar por escrito».
   - **§8:** marca lo ejecutado en S6 y deja solo PRF-002, F3-REG-024 y F3-PES-015.
   - **Anexo A:** cumplido en local y en staging.
3. **El plan de migración:** el estado de la Fase 4 en la tabla del §1 y la decisión pendiente del montacargas.

## Reglas
Las del `prompt-fase-4.md`, más estas:
- **No repitas casos ya ejecutados** salvo que haga falta para un caso por rol, y anótalo.
- **No cierres ni anules el uso abierto del montacargas:** queda para la decisión del usuario.
- **Sin commits:** entrega los mensajes.

## Entrega y detención
1. Los informes y las fichas.
2. **Los mensajes de commit**, listos para pegar:
   - **Frontend:** `docs(qa-f11): sesión S6 en staging con datos migrados, fichas DEF-F11-020 y 021, e informe final actualizado`. Incluye las evidencias `S6-*` del agente anterior y las tuyas.
   - **Backend:** `docs(migracion): fase 4, QA en staging`, con el plan y este prompt más el `prompt-fase-4.md`.

   Los dos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí.** La Fase 5 empieza solo con autorización del usuario.
