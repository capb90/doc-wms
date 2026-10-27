# Plan cerrado — Staging limpio con los datos del legacy y convenios por cliente

> **Fecha:** 27 de octubre de 2026. **Estado:** Aprobado por el usuario el 2026-10-27. Prompt del ejecutor, por fase: `prompt-staging-limpio-legacy-2026-10-27.md`.
> **Origen:** pedido del usuario del 2026-10-27, antes de la fase 13 del plan P1: «que el ambiente de staging quede limpio. Solo migrar los datos del legacy… y el sistema configurado para que los operarios puedan hacer las pruebas. También que queden configurados los acuerdos para clientes». Sus respuestas están en `DEC-043`.
> **Relación con la fase 13 del plan P1:** la fase 13 despliega el build y hace la QA sobre el staging de hoy, tal como está escrita. Este plan **reinicia staging después de esa QA**:
> - las fases 1 a 3 son locales y pueden correr en paralelo con la fase 13;
> - la fase 4 empieza cuando la fase 13 esté cerrada y la fase 3 haya salido OK;
> - la fase 4b (convenios y apertura de la facturación en staging) va cuando Facturación devuelva la hoja validada (S11).
>
> **R = 2026-10-27** (hoy): el usuario pidió hacer el reinicio hoy. El corte simulado queda en el 2026-10-26.
>
> **Build:** el que deje desplegado la fase 13: BE `911399c` y FE `33fbeba`, o sus descendientes. **Sin cambios de código.** Si la herramienta falla, se abre una ficha `DEF-MIG-NNN` y se corrige aparte, como en el plan de migración (§1).
> **Rutas:** relativas a `code_workspace/`. Prefijos: `B/` = `Backend/wms-api/`; `D/` = `docs/`; `T/` = `db_legacy/trabajo/` (fuera de git).

---

## 0. Instrucciones para el ejecutor

1. **Lee:**
   - `DEC-043` y, de `D/contexto/decisiones.md`, `DEC-006`, `DEC-007`, `DEC-029`, `DEC-040`, `DEC-041` y `DEC-042`;
   - del plan de migración (`D/planes/migracion-staging/plan-migracion-legacy-staging.md`), §2, §3 y §4;
   - `D/planes/migracion-staging/resultados/mapeo-tarifas-propuesto.md`;
   - `D/planes/migracion-staging/resultados/informe-fase-5.md` §4 y §5;
   - `D/analisis/analisis-fob-cif-legacy-v2-2026-10-24.md` §5;
   - el runbook `B/deploy/staging/README.md`.
2. **Git:** se trabaja en `develop` (BE) y en `main` de docs, sin ramas ni commits (`DEC-003`). Al cerrar cada fase te detienes con el resumen y el mensaje de commit de docs.
3. **Datos reales** (`DEC-007`):
   - las fases 1 a 3 trabajan en `T/` y con la MariaDB local `legacy-mariadb`;
   - del resto de `db_legacy/` solo se usa `backupBodegas.sql`, y únicamente para recargar la MariaDB si no está;
   - en git van conteos, ids del legacy, números de depósito y códigos de V2, sin nombres, documentos ni datos de contacto.
4. **Sin SQL de escritura** en ninguna base V2: todo entra por el API de importación y los endpoints del producto (§3.3 del plan de migración). El SQL de lectura es libre en local. En staging solo va como `BEGIN TRANSACTION READ ONLY … ROLLBACK` y con aprobación.
5. **Staging, paso por paso** (`DEC-006`): antes de cada acción sobre staging, una línea con lo que harás y el «sí» explícito del usuario. Borrar `pgdata` lleva su propio «sí», después de mostrar lo que se pierde.
6. **Credenciales:**
   - el agente no escribe contraseñas en el navegador ni las imprime;
   - en local, los scripts leen la credencial del Admin local de su archivo en `T/`;
   - en staging, los scripts los corre el usuario, como el de cuentas de la fase 5 de la migración, y el agente lee solo sus salidas en `T/evidencias/v4/`.
7. **Si el plan choca con una decisión `Sn` en un caso borde, gana la decisión** (`DEC-002`). Si falta una decisión, te detienes y preguntas.

---

## 1. Decisiones

| # | Decisión | Fuente |
| --- | --- | --- |
| S1 | **Se migra de nuevo.**<br>• La base de staging se recrea vacía, con las migraciones del repo: 19 en `911399c`.<br>• Los datos entran por el API de importación, con simulación (`dryRun=true`) antes de cada firme, en el orden del §3.4 del plan de migración.<br>• Antes se ensaya en local, en `wms_migracion`, recreada.<br>• No se restaura `wms_20261006_2302.dump`: lo cargó la herramienta del 6/10, sin el año del depósito ni la prórroga (`f37f353`) y con el levante anterior a `DEC-029` | `DEC-043` |
| S2 | **Conjunto v4.** Es el v3 con dos archivos regenerados:<br>• `11_depositos.csv`, con la consulta F6-03 actual de `D/planes/paridad-legacy/plan-backend-paridad-legacy.md`, que trae `prorroga` en la columna 22;<br>• `12_levantes.csv`, con la consulta actual, que trae `anio_deposito` en la columna 13.<br>Las consultas se extraen sin editar con `T/consultas/extraer_del_plan.py` a `T/consultas/v4/`. Los otros 10 CSV son los mismos archivos del v3: se verifica su SHA-256 contra `T/csv/sha256-csv-fase-1-v3.txt`. Los hashes del v4 van a `T/csv/sha256-csv-v4.txt` y al registro de CSV | `DEC-043`; plan P1 D28 y D29 |
| S3 | **Corte simulado en R − 1.**<br>• `R` es el día del reinicio de staging (fase 4): **2026-10-27**, fijado por el usuario. Se anota en el §6.<br>• `aplicar_d2.py` recibe la fecha: pone `ultimo_fin_facturado = R − 1` en todas las filas de `11_depositos.csv`, como hizo D2 con el 30/09. El ajuste va solo en el CSV; el dump no se toca.<br>• La facturación de cada depósito vivo arranca en `R`.<br>• Si `R` cambia después de la fase 3, se regenera solo `11_depositos.csv` y se repite el ensayo local con los scripts, que es corto | `DEC-043`; precisa `DEC-040` |
| S4 | **Tarifas:**<br>• T2, T3 y T4 y las cinco tarifas de montacargas, como `DEC-041`;<br>• **almacenamiento para clientes sin convenio:** la tarifa base que fije Facturación en el checkpoint de la fase 2. Es `PERCENTAGE_OF_VALUE_PRORATED`, `IMP001`, con su porcentaje y un mínimo de $50.000 con IVA (`DEC-029` §7.7);<br>• si Facturación no la fija, queda T1 como hoy: `PERCENTAGE_OF_VALUE` al 0,295 % con el mismo mínimo (`DEC-029` §7.10) | `DEC-029`, `DEC-041` |
| S5 | **Propuesta de convenios.** Se calcula con el método del análisis FOB/CIF (§5.2):<br>• fórmula prorrateada;<br>• base: FOB × TRM del día de ingreso;<br>• el porcentaje por cliente es el que iguala lo facturado, neto de IVA, con su base;<br>• mínimo de $50.000 con IVA.<br>Antes de consultar el volcado se pide la aprobación del usuario (`DEC-029` §7.6).<br>**Universo:** los clientes con depósitos vivos en el conjunto v4 y los 29 que concentran el 80 % de las quincenas. Los de ambos grupos van una sola vez.<br>Por cada cliente se marca además si sus recibos de báscula del legacy salieron siempre en $0. Es solo una pista para Facturación: el $0 también lo daban los repesajes | `DEC-029` §7.6; `DEC-043` |
| S6 | **Validación de Facturación:**<br>• la propuesta va como hoja de cálculo en `T/convenios/propuesta-convenios-v1.xlsx`, con los nombres y documentos solo ahí;<br>• Facturación la devuelve con sus columnas llenas: «Validado» (sí o no), «% acordado», «Báscula sin cobro» (sí o no) y «Observaciones»;<br>• **solo se carga lo que diga «Validado = sí»**;<br>• un cliente no validado factura con la tarifa base de S4 | `DEC-029` §7.6 |
| S7 | **Forma del convenio en V2.** Uno por cliente y activo, con un solo activo por cliente (D21). Se crea con `POST stakeholder/{id}/agreement`:<br>• referencia `LEG-{id_cliente}`;<br>• nombre «Convenio calibrado legacy {id_cliente}»;<br>• estado `Active`.<br>Sus servicios se agregan con `POST …/agreement/{id}/services`:<br>• **almacenamiento:** `ALMACENAMIENTO`, `PERCENTAGE_OF_VALUE_PRORATED`, modalidad `IMP001`, sin producto, con el porcentaje acordado y un mínimo de 50.000 con IVA incluido; `TaxIncluded = false`;<br>• **báscula, si dice «Báscula sin cobro = sí»:** `BASCULA`, `FIXED` con monto 0 (`DEC-057` D14 y D15).<br>**El tercero de V2** se busca por el número de identificación del cliente en `05_clientes.csv`, con `GET stakeholder?search=` (en singular), y se cuentan solo los terceros con ese número exacto, normalizado como lo hace el importador: la búsqueda es parcial y mira también el nombre y los contactos. Si no sale exactamente uno, el convenio no se carga y se informa | `DEC-029`; `DEC-057` |
| S8 | **Configuración para los operarios:**<br>• el Admin, que crea `Bootstrap` al arrancar, con la contraseña que maneja el usuario;<br>• las cinco cuentas `operario.*` por rol, con `crear-cuentas-operarios-staging.sh` (corre el usuario), cambio de contraseña al entrar y los correos `capb.dev+operario.<rol>@gmail.com`;<br>• las tarifas de montacargas de `DEC-041`;<br>• los destinos de respaldo `local-staging` (Local, `/opt/wms/backups`) y `s3-externo`.<br>`GUIDE_CODE_TYPE` ya entra en `QR` con la migración, y el correo, `Frontend__BaseUrl` y la clave del QR no cambian: viven en `.env.staging`.<br>**No se crean** cuentas `qa.*`, datos de práctica ni datos de QA | `DEC-043`; `DEC-041`; `DEC-060` |
| S9 | **Lo que queda de antes:**<br>• **los archivos subidos** (`/opt/wms/data/uploads`) se mueven, sin borrarlos, a `/opt/wms/data/uploads-antes-reinicio-AAAAMMDD`;<br>• **los respaldos viejos** se quedan en `/opt/wms/backups` como punto de vuelta;<br>• **`caddy_data`, `caddy_config` y las llaves de DataProtection** no se tocan | `DEC-006` |
| S11 | **La apertura de la facturación espera a los convenios validados.**<br>• Crear o activar un convenio no recalcula las facturas existentes (`AgreementActivationService`): por eso los convenios van **antes** de `open-billing`.<br>• Si Facturación no devuelve la hoja validada antes de la fase 4, la fase 4 deja staging con los datos, las tarifas, las cuentas y los respaldos, **sin convenios y sin `open-billing`**. Los operarios ya pueden operar.<br>• Cuando llegue la hoja, la fase 4b corre en staging los convenios validados y `open-billing`, con el mismo script. Como el corte queda en `R − 1`, el primer período de cada depósito migrado arranca en `R`, aunque `open-billing` corra días después.<br>• Hasta la fase 4b, los depósitos migrados no tienen facturas. Un depósito nuevo de un cliente con convenio, que se cree antes de la 4b, factura con la tarifa base | Respuesta del usuario del 2026-10-27, «Abrir al validar» |
| S10 | **En staging, después del reinicio, la verificación es de solo lectura.** La operación completa ya se prueba en el ensayo local (OK-7). Las únicas escrituras de la verificación son las corridas de respaldo. Así, lo primero que se escribe en staging lo hacen los operarios | `DEC-043` |

---

## 2. Fase 1 — Local: conjunto v4 y carga de los datos

**Pasos:**
1. **Preparar.**
   - Comprueba que `legacy-mariadb` (puerto 3308) está arriba con la base `bodegas`. Si no, recárgala desde `backupBodegas.sql` y compara los conteos del §4 del plan de migración.
   - Recrea `wms_migracion`: `dotnet ef database drop`, comprobando antes el destino con `--dry-run`, y `dotnet ef database update`. Deben quedar las 18 migraciones.
   - El API local apunta a esa base por variable de entorno, con `Bootstrap__*`, **en un puerto propio (5290)**. El API del usuario corre en el 5281 sobre `wms_qa_preprod`: no lo detengas ni lo reconfigures.
2. **Exportar el v4** (S2 y S3), con la `R` del §6.
3. **Escribir `T/staging-limpio/cargar-legacy.sh`.** Recibe la URL del API y la ruta del archivo de credencial. Por entidad, en el orden del §3.4 del plan de migración, hace:
   - la simulación;
   - el firme;
   - la conciliación.

   Guarda cada respuesta en `T/evidencias/v4/<ambiente>/`. No imprime la credencial ni el token.
4. **Cargar en local** con el script.
5. **Probar la idempotencia:** recargar `05_clientes.csv` y `11_depositos.csv` no crea duplicados.
6. **Verificar en SQL de lectura**, contra la carga del v3 (`informe-fase-1-repeticion.md` e `informe-actualizacion-fases-1-2.md`):
   - los conteos por entidad;
   - los depósitos vivos y las filas «Ok» de la conciliación;
   - **C7:** los depósitos de importación con prórroga (`prorroga = 1`) quedan con su prórroga y su plazo de 60 días;
   - **C8:** los números de depósito repetidos entre vivos quedan como depósitos distintos, con su `legacy_year`;
   - cada diferencia con el v3 se explica.

**Criterio OK de la fase:**

| # | Criterio |
| --- | --- |
| L1 | Las 12 entidades en firme. Cada rechazo tiene su causa documentada, y la herramienta no causa ninguno |
| L2 | La conciliación queda sin diferencias sin explicar |
| L3 | La segunda carga no duplica |
| L4 | C7 y C8 coinciden con el legacy |
| L5 | Están anotados los tiempos de cada carga |

**Entrega:**
- el informe `D/planes/migracion-staging/resultados/informe-staging-limpio-fase-1.md`, con conteos y sin datos de personas;
- el conjunto v4 en `D/planes/migracion-staging/resultados/registro-csv-fase-1.md`, con archivo, consulta, filas y hash;
- el estado de la fase en el §6.

**Commit sugerido (docs):** `docs(migracion): conjunto v4 y carga local con la herramienta actual para el reinicio de staging (DEC-043)`

---

## 3. Fase 2 — Propuesta de convenios y validación de Facturación

**Pasos:**
1. **Pide al usuario la aprobación para consultar el volcado** (`DEC-029` §7.6). Sin ella, no sigues.
2. **Calcula la propuesta** (S5) con consultas de lectura sobre `legacy-mariadb`:
   - las consultas van en `T/consultas/convenios/`;
   - los resultados intermedios, en `T/convenios/`.
3. **Valida la propuesta fuera de la muestra**, como el §5.5 del análisis: calibrar con 2022–2023 y aplicar a 2024. Anota el total, el primer período, las renovaciones y la proporción de facturas a ±10 % y a ±25 %.
4. **Arma la hoja `T/convenios/propuesta-convenios-v1.xlsx`.** Lleva una fila por cliente, con:
   - el id del legacy y el nombre;
   - el número de identificación;
   - si tiene depósitos vivos;
   - si está entre los 29;
   - las quincenas usadas;
   - el porcentaje calibrado;
   - lo facturado en el legacy y lo que daría V2;
   - la pista de báscula en $0;
   - las columnas vacías de Facturación (S6).
5. **Resume la propuesta en git** en `D/planes/migracion-staging/resultados/convenios-propuesta-2026-10-27.md`:
   - cuántos clientes, la cobertura de quincenas y de depósitos vivos;
   - la distribución de los porcentajes y la validación fuera de la muestra;
   - sin nombres ni documentos.
6. **Checkpoint.** El usuario lleva la hoja a Facturación y la devuelve en `T/convenios/propuesta-convenios-v1-validada.xlsx`, con la tarifa base de S4 o la indicación de dejar T1.

**Criterio OK de la fase:** la hoja validada está en `T/convenios/` y la tarifa base está decidida. El resumen en git dice cuántos convenios se validaron, cuántos no y con qué tarifa base quedan los demás.

**Commit sugerido (docs):** `docs(migracion): propuesta de convenios calibrados por cliente y su validación por Facturación (DEC-029, DEC-043)`

---

## 4. Fase 3 — Local: tarifas, convenios y apertura de la facturación

**Pasos:**
1. **Escribir `T/staging-limpio/cargar-tarifas-convenios.sh`**, con los mismos argumentos de `cargar-legacy.sh` y tres opciones que se pueden correr por separado (`--tarifas`, `--convenios`, `--apertura`; sin opciones, las tres). En este orden:
   1. las tarifas de S4: la regla de almacenamiento, el mínimo, la báscula con IVA, la guía y las cinco de montacargas con `PUT forklift-rates/{tipo}`;
   2. los convenios validados (S7), leídos de una exportación CSV de la hoja validada en `T/convenios/`. Antes de crear un convenio, comprueba que el cliente no tiene otro activo;
   3. `open-billing`.

   Guarda cada respuesta en `T/evidencias/v4/<ambiente>/`.
2. **Correrlo en local** sobre la base de la fase 1, primero `--tarifas` y después `--convenios --apertura`, como se correrá en staging. Si todavía no hay hoja validada, el ensayo local usa la propuesta (`propuesta-convenios-v1.xlsx`) para probar el mecanismo; en staging solo se carga la validada.
3. **Verificar:**
   - **tarifas y convenios:** lo cargado coincide con S4 y con la hoja validada;
   - **un solo convenio activo por cliente** (D21);
   - **`open-billing`:** cada depósito vivo queda «Opened», o «Skipped» con su causa, con el primer período desde `R`;
   - **el primer período de cinco depósitos con convenio y dos sin él**, recalculado a mano (valor × saldo / recibido × porcentaje, con el mínimo), coincide al peso con la factura en Borrador;
   - **los totales del primer período**, por cliente con convenio y en total, quedan anotados para compararlos en la fase 4.
4. **Hacer una operación nueva completa sobre un depósito migrado de un cliente con convenio** (OK-7): levante → orden de cargue → cargue → guía → factura. Si algún cliente quedó con «Báscula sin cobro», además, un ingreso de Solo báscula de ese cliente sale en $0, con la marca «SIN COBRO POR CONVENIO».

**Criterio OK de la fase:**

| # | Criterio |
| --- | --- |
| L6 | Tarifas y convenios como S4 a S7, con un solo convenio activo por cliente |
| L7 | `open-billing` sin «Failed», con el primer período desde `R` |
| L8 | Los siete recálculos coinciden al peso |
| L9 | La operación de OK-7 funciona de punta a punta |
| L10 | Los dos scripts corren de punta a punta sobre una base recién recreada, que es como corren en staging |

Con `R` = hoy, el ensayo y el reinicio usan el mismo `11_depositos.csv`. Si la fase 4 se corre otro día, se regenera ese archivo con la fecha nueva (S3) y se repite el ensayo.

**Entrega:**
- el informe `D/planes/migracion-staging/resultados/informe-staging-limpio-fase-3.md`;
- el estado en el §6.

**Commit sugerido (docs):** `docs(migracion): ensayo local del reinicio de staging con tarifas, convenios validados y apertura de la facturación (DEC-043)`

---

## 5. Fase 4 — Staging: reinicio, carga y configuración

**Empieza cuando:** la fase 13 del plan P1 está cerrada, la fase 3 salió OK y el usuario confirma la ventana del día `R`. Cada paso que toca staging lleva su «sí».

| # | Paso | Detalle |
| --- | --- | --- |
| 1 | Inventario de solo lectura | Contenedores, migraciones, volúmenes, disco y destinos de respaldo |
| 2 | Respaldo «antes del reinicio» | `POST administration/backups/run`, con los dos destinos en `Succeeded`. Se anotan los nombres |
| 3 | Mostrar lo que se pierde | Los conteos de depósitos, facturas, operaciones y usuarios, con las cuentas `qa.*` y `operario.*` y los datos `PRAC-` y QA. **El «sí» de este paso autoriza el 4** |
| 4 | Recrear la base | `docker compose down` sin `-v`, `docker volume rm wms-staging_pgdata` y mover los archivos subidos (S9) |
| 5 | Base y API | `deploy-staging.sh dbup`, `migrate` con el script idempotente (deben ser las 19 migraciones) y `up`. Se verifican `__EFMigrationsHistory`, los 6 roles y que existe el Admin. El usuario inicia la sesión del Admin |
| 6 | Cargar los datos | El usuario corre `cargar-legacy.sh` contra staging, antes verificando los hashes del v4. El agente lee las salidas y compara cada conteo con la fase 1: deben ser **idénticos** |
| 7 | Tarifas | El usuario corre `cargar-tarifas-convenios.sh --tarifas`. Lo cargado debe ser idéntico a la fase 3. **Si ya está la hoja validada**, corre también `--convenios --apertura`, y los conteos, los «Opened» y los totales del primer período, por cliente y en total, deben ser idénticos a la fase 3. **Si no**, ese paso queda para la fase 4b (S11) |
| 8 | Respaldos | Se crean los destinos `local-staging` y `s3-externo` (§13 del plan P1, pasos 1–7) y se prueban |
| 9 | Cuentas | El usuario corre `crear-cuentas-operarios-staging.sh`. Se verifica que existen las 5 cuentas con `mustChangePassword = true` y ninguna `qa.*` |
| 10 | Verificación de solo lectura | • `deploy-staging.sh smoke`.<br>• En SQL de lectura: no hay entradas, ciclos, órdenes, guías ni facturas de báscula o montacargas; las facturas son solo las de `open-billing` (ninguna, si la apertura quedó para la 4b); no hay nada `PRAC-` ni `QA-`.<br>• En pantalla, con la sesión del Admin: diez depósitos migrados, uno con prórroga y un convenio |
| 11 | Respaldo «listo para operarios v2» | Una corrida con los dos destinos en `Succeeded`. Es el punto de vuelta para repetir las pruebas desde cero |

**Entrega:**
- **el informe `D/planes/migracion-staging/resultados/informe-staging-limpio-fase-4.md`:** los respaldos, los conteos y su comparación con local, los convenios cargados y la verificación;
- **`D/planes/migracion-staging/resultados/guia-pruebas-operarios.md`, actualizada:**
  - las cuentas por rol, sin contraseñas;
  - sin escenarios de práctica: cada operario registra su camión desde Vigilancia, con vehículos y conductores migrados;
  - los avisos: datos de junio de 2024 con el corte en `R − 1`; convenios calibrados en N clientes y la tarifa base para los demás, o, si la apertura quedó para la 4b, que los depósitos migrados todavía no tienen factura de almacenamiento; la nota `manuales/nota-operarios-hallazgos-2026-10-26.md`;
  - PRF-002 con un camión que registre el operario;
  - el canal para reportar problemas, que da el usuario. Si no lo da, queda `[completar]`;
- **`D/contexto/estado.md` §3:** los datos, las cuentas y los respaldos;
- **en `D/contexto/estado.md` §4:** se cierran los pendientes 4 (guía), 5 (cuentas `qa.*`) y el 8, en lo que toca a los convenios cargados en staging;
- **`DEC-043`:** su línea de ejecución;
- **el plan de migración** (§1), una fila «Reinicio limpio (2026-10-27)»;
- **`D/planes/README.md`**;
- el estado de la fase en el §6.

**Commit sugerido (docs):** `docs(staging): reinicio limpio con los datos del legacy, convenios validados y cuentas por rol para las pruebas de los operarios (DEC-043)`

### 5.1 Fase 4b — Staging: convenios validados y apertura de la facturación

**Solo si la fase 4 no los cargó** (S11). Empieza cuando la hoja validada está en `T/convenios/propuesta-convenios-v1-validada.xlsx`. Cada paso que toca staging lleva su «sí».

1. **Ensayo local con la hoja validada,** si la fase 3 usó la propuesta. Recrea `wms_migracion` y corre los dos scripts de punta a punta, en el orden de staging: `--tarifas` con T1, como quedó en la fase 4; el cambio de la tarifa base del paso 3, si aplica; y `--convenios --apertura`. Los criterios L6 a L8 deben cumplirse con la hoja validada.
2. **Respaldo** «antes de la apertura» en staging, con los dos destinos en `Succeeded`.
3. **Tarifa base** (S4). Solo si la hoja validada fija un porcentaje en lugar de dejar T1.
   - La fase 4 dejó T1, y `--tarifas` se detiene ante una regla base distinta, así que no sirve para cambiarla.
   - La regla base de `ALMACENAMIENTO` se edita con `PUT service/{id}/pricing-rules/{ruleId}`, que reemplaza la fórmula y los parámetros: `PERCENTAGE_OF_VALUE_PRORATED`, `IMP001`, el porcentaje de Facturación y el mínimo de $50.000 con IVA.
   - Lo hace una opción nueva del script, `--cambiar-base`, que guarda la regla antes y después. La corre el usuario.
   - La fotografía de tarifas de staging debe quedar igual a la del ensayo.
4. **Carga.** El usuario corre `cargar-tarifas-convenios.sh --convenios --apertura` contra staging. Los convenios, los «Opened» y los totales del primer período deben ser idénticos al ensayo local, con el primer período desde `R`.
   - **Excepción:** los depósitos migrados que los operarios movieron desde `R` (levantes, órdenes de cargue, salidas). El ensayo local no tiene esos movimientos, así que su primer período puede no coincidir. Se excluyen de la comparación y se listan con sus movimientos, su saldo y su resultado en la apertura.
5. **Verificación de solo lectura.**
   - Un solo convenio activo por cliente.
   - La fecha límite de cada período abierto es su fin + 3 días (`StoragePeriodCalculator`).
   - Los depósitos que crearon los operarios antes de la 4b se listan con su tarifa y no se tocan (S11).
6. **Respaldo** «listo para operarios v2, con convenios».

**Entrega:** una sección «Fase 4b» en `informe-staging-limpio-fase-4.md`; la guía de los operarios actualizada (los convenios ya cargados); el §6; `DEC-043`.

**Commit sugerido (docs):** `docs(staging): convenios validados y apertura de la facturación de los depósitos migrados en staging (DEC-043)`

---

## 6. Estado de las fases

`R` (día del reinicio, S3): **2026-10-27**. Corte simulado: 2026-10-26.

| Fase | Estado | Notas |
| --- | --- | --- |
| 1 · Local: v4 y carga de datos | Hecha, sin commit (2026-10-27) | **Partida:** BE `911399c`, docs `0836639`. R = 2026-10-27, corte 2026-10-26.<br>**L1 a L5 cumplen** (`informe-staging-limpio-fase-1.md`):<br>• conjunto v4 en `registro-csv-fase-1.md`;<br>• 12 entidades con los conteos y los mensajes de rechazo del v3, 0 por la herramienta;<br>• conciliación 133 Ok;<br>• la recarga no duplica;<br>• C7: BA4575 (2022) → `2022BA00002` con prórroga y 60 días;<br>• C8: 0 números repetidos entre vivos, año en los 128 y levantes por año en 107 de 107;<br>• facturación desde R en los 128.<br>**Tiempos:** exportación de depósitos 14,3 s; `drop` 1,9 s; `update` 3,3 s; carga completa con `cargar-legacy.sh` 12,8 s; idempotencia 1,0 s.<br>**Desviaciones:**<br>1. El repo en `911399c` tiene **19 migraciones**, no 18: el texto no cuenta `AddLabelPrintEntry` (`DEC-057`). Se aplicó S1 («las migraciones del repo»). En la fase 4, el paso 5 debe esperar 19.<br>2. `extraer_del_plan.py` está en `T/consultas/v3/`, no en `T/consultas/`: se copió sin cambios a `T/consultas/v4/`.<br>3. `aplicar_d2.py` no recibía la fecha: se le agregó como tercer argumento (S3), y las estadísticas cuentan por (número, año). La versión anterior está en `T/extractos/aplicar_d2-antes-v4.py`.<br>4. Sin abrir `.env*`, el Admin local usa un archivo nuevo, `T/.admin-migracion.local`, y la conexión se arma con las variables del contenedor.<br>**Para la fase 3:** no hay cuentas por rol en local (S8). Si la operación de OK-7 se hace por rol, hay que crearlas en `wms_migracion` |
| 2 · Propuesta de convenios y validación | Pasos 1–5 hechos, sin commit (2026-10-27); **esperando el checkpoint de Facturación (paso 6)** | **Partida:** BE `911399c`, docs `28eea7e`. Aprobación del usuario para consultar el volcado: 2026-10-27.<br>**Propuesta** (`convenios-propuesta-2026-10-27.md`; hoja `T/convenios/propuesta-convenios-v1.xlsx`):<br>• 43 clientes: 24 con depósitos vivos y los 29 del 80 %, 10 en ambos; 82,4 % de las quincenas;<br>• 40 con porcentaje calibrado (mediana 0,2803 % neto; p25–p75 0,1762–0,3222 %); 3 con 38 depósitos vivos sin quincenas, a la tarifa base;<br>• fuera de la muestra (2021–2023 → 2024): 86,3 % del legacy en el universo, 87,0 % con todos;<br>• referencias para la tarifa base: 0,1363 % neto (todos) y 0,1619 % (los que no están en la hoja);<br>• báscula siempre en $0: 4 clientes (pista).<br>**Tiempos:** extracción 20,8 s; calibración 0,7 s.<br>**Criterio OK:** pendiente: falta `T/convenios/propuesta-convenios-v1-validada.xlsx` con la tarifa base. Si no llega antes de la fase 4, la fase 4 va sin convenios ni `open-billing` (S11).<br>**Desviaciones:** 5, en el §7 del resumen; ninguna choca con una Sn.<br>**Para la fase 3:** el id 925 tiene el documento repetido en otro cliente del legacy (S7); con la propuesta, el ensayo cargaría 40 convenios |
| 3 · Local: tarifas, convenios y apertura | Hecha, sin commit (2026-10-27), **con la propuesta**: la hoja validada no ha llegado | **Partida:** BE `911399c`, docs `47681d2`.<br>**L6 a L10 cumplen** (`informe-staging-limpio-fase-3.md`):<br>• `wms_migracion` recreada (19 migraciones) y `cargar-legacy.sh` con los conteos de la fase 1;<br>• `cargar-tarifas-convenios.sh --tarifas`: T1 (Facturación no fijó la base), T2 a T4 y montacargas como `DEC-041`; repetible sin duplicar;<br>• `--convenios --apertura` con `exportar-hoja-convenios.py --ensayo`: 40 convenios, uno activo por cliente, 4 con báscula en $0;<br>• 128 «Opened» desde R, 0 «Failed»: 90 con convenio y 38 con T1;<br>• los 128 primeros períodos coinciden al centavo con el recálculo a mano. Total $50.938.843,49: $21.752.111,62 con convenio (21 clientes) y $29.186.731,87 con T1 (3 clientes);<br>• OK-7: salida de `2024BA00089` (levante, OC, báscula $20.000, guía $15.000, cargue, repesaje, salida) y Solo báscula del cliente 698 en $0 con «SIN COBRO POR CONVENIO».<br>**Tiempos:** `drop` 3,8 s; `update` 4,4 s; carga 13,6 s; tarifas 1,2 s; convenios 1,2 s; apertura 2,0 s.<br>**Desviaciones:** 6, en el §8 del informe. Entre ellas: la ruta es `GET stakeholder?search=`, en singular, con coincidencia exacta del número; y en OK-7 la guía va antes del cargue.<br>**Para la fase 4 / 4b:** con la hoja validada se repite este ensayo (§5.1, paso 1), y los totales a comparar son los de ese ensayo, no los de este |
| 4 · Staging: reinicio, carga y configuración | Hecha, sin commit (2026-10-27), **sin convenios ni `open-billing`** (S11): la hoja validada no ha llegado | **Partida:** BE `911399c`, docs `7e4c568`; en staging BE `911399c` / FE `33fbeba`. R = 2026-10-27 (hoy), corte 2026-10-26. Fase 13 del plan P1 cerrada.<br>**Resultado** (`informe-staging-limpio-fase-4.md`):<br>• respaldo «antes del reinicio» `b88fdf98` en los dos destinos; se pierden 137 depósitos, 252 facturas, 11 usuarios y los datos `QA-`;<br>• `pgdata` recreado: **19 migraciones**, 6 roles y el Admin de `Bootstrap`; uploads movidos a `uploads-antes-reinicio-20261027`;<br>• `cargar-legacy.sh` (usuario): las 12 entidades con los mismos conteos y mensajes de rechazo que la fase 1, conciliación 133 Ok, conteos de la base iguales tabla por tabla;<br>• `--tarifas` (usuario): fotografía idéntica a la fase 3 (T1, porque Facturación no fijó base);<br>• destinos `local-staging` y `s3-externo` probados, corrida `29433cd2` `Succeeded`, fallo provocado `20dd2306` `PartiallySucceeded` con correo recibido;<br>• 5 cuentas `operario.*` con `must_change_password`, ninguna `qa.*`;<br>• verificación de solo lectura: smoke OK; 0 operaciones, facturas, convenios y datos `PRAC-`/`QA-`; en pantalla 128 depósitos confirmados y `2022BA00002` con 60 días;<br>• respaldo «listo para operarios v2» `bf7bf952` en los dos destinos.<br>**Tiempos:** sin servicio de 12:08 a 12:15; `dbup` 12 s, `migrate` 6 s, `up` 3 s; carga 44,7 s (local 12,8 s); tarifas 7,3 s; cuentas 6 s.<br>**Desviaciones:** 5, en el §7 del informe. Entre ellas: `uploads` se creó de nuevo vacía (dueño 1654) para que el API pueda escribir; los pasos 1 a 3 del §13 del plan P1 no se repitieron porque siguen en el servidor.<br>**Pendiente:** el canal de reporte en la guía de operarios (`[completar]`) y la fase 4b |
| 4b · Staging: convenios y apertura | Pendiente | Cuando Facturación devuelva la hoja validada, si la fase 4 no los cargó (S11) |

**Validación de las fases 1 a 3 (2026-10-27).** Revisión de solo lectura sobre los informes, el código en `911399c` y una consulta de fechas en `wms_migracion`. También se revisó la fase 13 del plan P1 (`qa/resultados/PRE-informe-2026-10-25.md` §13).

- **Resultado:** las fases 1 a 3 cumplen L1 a L10, y la fase 13 está cerrada. La fase 4 puede empezar hoy. Sin hoja validada, va sin convenios ni `open-billing` (S11).
- **Correcciones de texto, sin decisión nueva:**
  - S1 y el paso 5 del §5: son 19 migraciones;
  - S7: la ruta es `GET stakeholder?search=` y se cuenta solo el número exacto;
  - el aviso de la guía de operarios cuando la apertura queda para la 4b.
- **§5.1 (fase 4b), completado:**
  - paso 3: cómo se cambia la tarifa base si Facturación fija una (aplica S4);
  - paso 4: los depósitos migrados que los operarios movieron antes de la 4b se excluyen de la comparación con el ensayo;
  - paso 5: verificar la fecha límite.
- **Informe de la fase 3:** la fecha límite es fin + 3 días, no fin + 2. La base da 14/11 y 28/04.
- **Aviso descartado:** el 404 de `GET weighbridge/{id}/invoice` en un ciclo de salida (§9 del informe de la fase 3) no afecta a los operarios: ninguna pantalla llama ese endpoint.
- **Para Facturación, junto con la hoja:**
  - **cliente 464:** 36 de los 128 depósitos vivos. En el legacy factura cada 180 días (`dias_facturacion`), así que la calibración, que solo usa quincenas, no lo cubre. Con T1 su primer período suma $27.999.160,93, el 55 % del total del ensayo. Facturación debe fijar su porcentaje;
  - **el 925** comparte el tercero de V2 con el 926;
  - **porcentajes extremos:** el 773 (2,0048 %), el 842 (0,0524 %) y el 602 (0,0906 %, 43 depósitos vivos);
  - **calibración por debajo del legacy:** con los datos de 2024, los porcentajes calibrados facturan el 86 % de lo que facturó el legacy. Puede haber alzas de tarifa, así que cada porcentaje se compara con lo pactado hoy;
  - **tarifa base:** T1 cobra el 0,295 % sobre el lote completo; la referencia prorrateada está entre el 0,136 % y el 0,162 %.

---

## 7. Riesgos

| Riesgo | Mitigación |
| --- | --- |
| Recrear staging borra la evidencia de la QA de la fase 13 | La fase 13 cierra su informe antes. El respaldo «antes del reinicio» conserva la base, y los archivos subidos se mueven sin borrarlos |
| La herramienta actual da conteos distintos del v3 (año del depósito, prórroga, levante de `DEC-029`) | Se espera y se explica en la fase 1 (C7, C8). Si una diferencia viene de un defecto, ficha `DEF-MIG` antes de seguir |
| Facturación tarda en validar | S11: el reinicio va hoy sin convenios ni apertura, y la fase 4b los carga después. Mientras tanto los depósitos migrados no facturan, y un depósito nuevo de un cliente con convenio factura con la tarifa base |
| El porcentaje calibrado pasa de lo facturado en el legacy a los depósitos de hoy | Es un ensayo: los convenios se calibraron con quincenas de 2022–2024. La validación fuera de la muestra se informa en la fase 2, y el mes en paralelo de `DEC-029` §7.10 sigue antes de producción |
| Staging queda con datos reales de clientes, accesible desde internet | Se mantiene lo aceptado en el plan de migración (§9): contraseñas fuertes, cambio al primer ingreso y Swagger apagado. El pendiente 6 de `estado.md` sigue abierto |
| Al recrear la base se pierden los destinos de respaldo de la fase 13 | El paso 8 de la fase 4 los vuelve a crear y probar. Las claves S3 siguen en `.env.staging` |
