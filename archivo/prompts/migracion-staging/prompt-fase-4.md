Eres el ejecutor de QA de la **Fase 4 — QA en staging (sesión S6)** del plan `docs/planes/migracion-staging/plan-migracion-legacy-staging.md` del WMS de Bodegas Asociadas. Modelo recomendado: **Opus 5.5**.

Ejecutas en el **ambiente desplegado y con los datos migrados** lo que el informe final del QA dejó «Diferido a staging»: `docs/qa/resultados/informe-final.md` §8. También confirmas en staging las correcciones de la migración. Al terminar actualizas el informe final del QA.

## Lee primero
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. **El marco de QA de la fase 11:** `docs/archivo/prompts/qa/prompt-qa-fase-11-retest.md`. **Sus reglas de registro, fichas y entrega valen aquí.** Lee también `docs/qa/fase-11-regresion-cierre.md`: la suite REG, STG y los anexos.
3. **El informe final del QA:** `docs/qa/resultados/informe-final.md`, en especial §7 y **§8 «Pendiente para staging»**.
4. **Los documentos de las fases del QA** con los casos que vas a ejecutar: `fase-00-smoke.md` (F0 completo) y los casos de origen de F11-REG-001 a 013 y de E2E-01 (`fase-08-e2e.md`).
5. **El plan de migración:** §2 (D4 y D5), §3 y **§7 (esta fase)**. Lee también:
   - `resultados/informe-fase-3.md`, con el estado de staging, los respaldos y las observaciones O-4 y O-5;
   - las fichas `DEF-MIG-005`, `DEF-MIG-007` y `DEF-MIG-008` y sus listas de verificación.

## Situación de partida
- **Staging:**
  - app: `https://app.100-60-89-139.sslip.io`;
  - API: `https://api.100-60-89-139.sslip.io/api/v1`;
  - build: BE `b31ddb6` / FE `508b91b`.
- **Datos migrados:** 128 depósitos «Confirmed», con 128 facturas de almacenamiento en Borrador que suman $91.257.475,39, y las tarifas T1 a T4. Respaldo «staging migrado»: `wms_20261006_2302.dump`.
- **Decisiones del usuario que aplican:**
  - **«Estadísticas» oculto del menú**, a propósito.
  - **El correo es Gmail real** y solo puede llegar a `capb.dev@gmail.com` y sus alias (D4).
  - **PRF-002, el cronometraje del registro en báscula, lo hace después un operario real**, no tú. Lo registras como «Diferido: lo mide un operario» con su criterio: registro en báscula en 30 s o menos. Junto con él quedan F3-REG-024 y F3-PES-015.
- **El Admin:** su contraseña está en `code_workspace/db_legacy/trabajo/.admin-staging.local`. Léela sin imprimirla.

## Paso 0 — Cuentas de QA por rol (con alias del correo del usuario)
Con el Admin, por el API (`POST user`, el mismo contrato que la pantalla de usuarios), crea **una cuenta por rol**:

| Usuario | Rol | Correo |
|---|---|---|
| `qa.vigilancia` | Vigilancia | `capb.dev+qa.vigilancia@gmail.com` |
| `qa.bascula` | Báscula | `capb.dev+qa.bascula@gmail.com` |
| `qa.bodega` | Bodega | `capb.dev+qa.bodega@gmail.com` |
| `qa.comext` | Comercio Exterior | `capb.dev+qa.comext@gmail.com` |
| `qa.facturacion` | Facturación | `capb.dev+qa.facturacion@gmail.com` |

- **Contraseñas:**
  - genera una contraseña fuerte por cuenta, que cumpla la política de CHG-14;
  - guárdalas **solo** en `code_workspace/db_legacy/trabajo/credenciales-qa-staging.local.md`, con permisos 600;
  - **nunca** las escribas en el chat, en los informes ni en git.
- **Cambio obligatorio:** haz el primer cambio de contraseña con `auth/change-password`, para quitarlo, y guarda la contraseña final en el mismo archivo.
- **Correo:** si crear una cuenta envía un correo, debe llegar a su alias. Anota cuáles salieron.
- **Fase 5:** estas cuentas se pueden reutilizar o reemplazar allí; no las borres.

## Alcance

### A. Bloque STG del informe final §8
1. **F0 completo (37):** disponibilidad, CORS con el dominio de staging, login y sesión, menú por rol, API principales, entorno y datos mínimos.
   - El menú sin «Estadísticas» **es lo esperado.**
2. **F11-REG-001 a 013.** Los casos que en local nombraban ubicaciones de ejemplo (`A01-R01-N01`, `B01-R01-N01`: F1-UBI-003, F4-REC-004, F4-UBI-001 y F4-UBI-003) se ejecutan con **las ubicaciones migradas** (DEF-MIG-008).
3. **E2E-01:** una importación completa con un camión y salida total. Pasa por ingreso, báscula, registro del depósito nuevo, recepción, montacargas, confirmación, levante, OC, cargue, guía, repesaje, salida y facturas.
4. **La DIAN real, F6-TRM-001:** confirmar un depósito **nuevo en USD** sin TRM manual. Mide la respuesta, que debe ser de 3 s o menos.
5. **Diferencias propias de staging:**
   - **correo real:** el CE-7 al administrador y la recuperación de contraseña de una cuenta de QA llegan al alias;
   - **Swagger apagado;**
   - **respaldos activos:** FB-BAK-003 manual y la corrida programada de las 02:00, si la sesión la alcanza.
6. **Humo de las últimas correcciones:** F2-COR-011, F6-REC-002, F3-RPT-001 y F3-CIC-001.
7. **PRF-002, F3-REG-024 y F3-PES-015:** prepara el escenario para el operario y anótalo en el informe. El escenario es un camión QA en la cola, con conductor y transportadora migrados y datos precargados. **No midas tú.**

### B. Migración vista desde la operación
1. **FA-MIG-009 por rol en staging,** con las cuentas `qa.*`:
   - **Comercio Exterior:** los depósitos migrados (detalle, importador, manifiesto, moneda y valor) y su abandono. Los 66 depósitos «en abandono» son esperables, porque ingresaron entre 2022 y 2024.
   - **Bodega:** inventario y ubicaciones.
   - **Facturación:** las facturas de almacenamiento en Borrador.
   - **Báscula y Vigilancia:** un vehículo y un conductor migrados.
2. **DEF-MIG-005 y DEF-MIG-007 en staging:** sobre **un** depósito migrado con salidas en el legacy (BA0042) y **uno** sin salidas (BA0558):
   - levante si hace falta, OC, salida en báscula, cargue, guía, repesaje y salida;
   - la guía imprime **el manifiesto** y los saldos correctos: BA0042 da 448 → 448 − lo que sale.
3. **Facturación de un migrado:** numera y aprueba la factura de almacenamiento de **uno** de esos dos depósitos con un N.º SIIGO de prueba `QA-S6-…`. La factura conserva el período y el total esperados.
4. **El detalle con un Id que no existe** (observación de la Fase 3): abrir un depósito por URL con un Id de otra entidad deja «Cargando…» sin mensaje. Compruébalo contra la regla de CHG-87, «sin callejones sin salida». **Si se confirma, abre ficha.**
5. **O-4,** el orden de los productos en el texto de la factura: solo regístralo como observación conocida. No abras ficha.

### C. FB-BAK-005 (restaurar), opcional y con permiso
Si el usuario lo autoriza en el chat, restaura el respaldo «staging migrado» en una **base aparte** dentro del contenedor de Postgres (por ejemplo `wms_restore_test`), siguiendo el README. Luego:
- comprueba conteos de depósitos, facturas y el total;
- y **borra esa base de prueba**.

**Nunca restaures sobre la base de staging.** Sin el «sí» del usuario, se marca «No ejecutado: sin autorización».

## Reglas (obligatorias)
- **Producción no se toca.**
- **Datos que crea QA:**
  - solo con marca **QA-S6**: placas que empiecen por `QS`, documentos, cartas porte, notas y N.º SIIGO con `QA-S6`;
  - **las operaciones sobre datos migrados se limitan a BA0042 y BA0558** (§B.2 y §B.3), y quedan listadas en el informe.
- **En staging no hay SQL de escritura.**
  - Hay SQL de solo lectura por SSH para verificar.
  - **No existen palancas de tiempo en staging:** los casos que las necesitan (mora, vencimiento, renovación) se marcan «No aplica en staging», citando su evidencia local de la fase 11.
- **Nada se reinicia ni se redespliega sin permiso del usuario.** Si un caso necesita reiniciar el API, pídelo.
- **No se borra ni se restaura sobre la base de staging.** La restauración de prueba va solo en una base aparte y con permiso (§C).
- **Sin secretos:** ni contraseñas, ni tokens, ni valores de `.env`. Las contraseñas se leen de los archivos locales sin imprimirlas.
- **Datos reales:** los informes no llevan datos de personas naturales; los depósitos se citan por su número.
- **Fichas:**
  - un defecto del producto va como `DEF-F11-020` en adelante, en `docs/qa/resultados/defectos/`;
  - un defecto de la migración va como `DEF-MIG-009` en adelante, en `docs/planes/migracion-staging/resultados/defectos/`.
- **No cambies código ni configuración.**
- **Sin commits:** entrega los mensajes.
- Textos en español.

## Entrega y detención
1. **Informe de la sesión** `docs/qa/resultados/F11-informe-S6-<fecha>.md`, con la estructura de los informes S1 a S5:
   - datos de ejecución, con el build y las cuentas usadas (solo el usuario, sin contraseña);
   - resumen por bloque;
   - resultado por caso, con su evidencia en `evidencias/F11/S6-*`;
   - defectos nuevos;
   - riesgos;
   - datos creados, con las operaciones sobre BA0042 y BA0558;
   - criterios de salida;
   - checkpoint.
2. **El informe final** `informe-final.md`:
   - **§1 y §2.2:** agrega la fila S6 en staging.
   - **§7, veredicto:**
     - **sin FALLA en P0 en staging y sin CRITICAL ni BLOCKER abiertos →** «**GO condicionado** solo a PRF-002 (medición con un operario)»;
     - si hay fallas, el veredicto que corresponda, con su causa.
   - **§8:** marca lo ejecutado en S6 y deja solo PRF-002, F3-REG-024 y F3-PES-015 como «Pendiente: lo mide un operario».
   - **Anexo A:** márcalo cumplido en local y staging, citando los informes de la migración.
3. **En el plan de migración,** el estado de la Fase 4 en la tabla del §1.
4. **Los mensajes de commit**, listos para pegar:
   - **Frontend (documentación QA):** `docs(qa-f11): sesión S6 en staging con datos migrados e informe final actualizado`;
   - **Backend (documentación de la migración),** si cambió: `docs(migracion): fase 4, QA en staging`.

   Los dos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí.** La Fase 5 (staging listo para operarios) empieza solo con autorización del usuario.
