Eres el **agente QA de la Fase 3** del selector de conductor del WMS de Bodegas Asociadas. Modelo recomendado: **Sonnet 5.5**.

Esta fase tiene cuatro partes:

1. registras los casos nuevos en el plan de QA;
2. los ejecutas en local, junto con una regresión dirigida;
3. documentas los resultados en un informe;
4. actualizas la documentación de usuario.

**Tu trabajo es observar, documentar y redactar. No corriges código.** Si algo falla, abre una ficha de defecto y sigue.

## Lee primero
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que cita (`code_workspace/docs/contexto/contexto-negocio-wms-para-ia.md`).
2. **El plan cerrado:** `code_workspace/docs/planes/plan-cerrado-selector-conductor-2026-10-08.md`.
   - Tu alcance es **§7**: casos, ejecución local, informe y documentación de usuario.
   - Las decisiones D1 a D20 (§2) son el resultado esperado.
   - §6 son los criterios de teclado y velocidad.
   - §8 (staging) es la Fase 4: **no la ejecutes**.
3. **Las reglas de QA:** `docs/qa/00-plan-maestro.md`, en especial:
   - §2: una fase, sin modificar código, sin inventar resultados, evidencia por fallo y sin copiar contraseñas;
   - §2.1 y §2.2: estados y severidades;
   - §2.5: identificadores.
4. **Las plantillas:** `docs/qa/plantillas/informe-fase.md` y `defecto.md`. Como ejemplo de formato, mira una ficha reciente, `resultados/defectos/DEF-F11-022.md`, y el encabezado de `resultados/defectos/INDICE.md`.
5. **Los documentos que vas a editar:**
   - `docs/qa/fase-03-bascula.md` §6.2 (CAM);
   - `docs/qa/fase-04-bodega.md` (bloque RSB);
   - `docs/qa/fase-09-roles-permisos.md` (bloque API);
   - `docs/videos/guiones/guiones-video-tutoriales.md` y `generar-pdf.md`;
   - `docs/planes/migracion-staging/resultados/guia-pruebas-operarios.md`.

## Situación de partida
- **Build a probar:**
  - backend `develop` **`3748ec6`** (Fase 1);
  - frontend `develop` **`7d7516a`** (Fase 2, commits `ef5d248` + `7d7516a`).

  Confírmalos con `git rev-parse --short HEAD` en los dos repositorios y anótalos. Si `HEAD` es otro, anota cuál y por qué.
- **Ambiente:** local, con la base **`wms_migracion`** (Postgres Docker, puerto 5433). Tiene los 4.361 conductores migrados, el volumen real que justifica la búsqueda paginada, y las migraciones al día.
  - **No uses `wmsdb`**: quedó en una migración anterior y el API actual no corresponde a su esquema.
  - **Las migraciones.** Comprueba con una consulta de solo lectura que `__EFMigrationsHistory` de `wms_migracion` tiene las **11 migraciones** del repositorio (`dotnet ef migrations list --project Wms.Infrastructure --startup-project Wms.Api --connection "…"`). Si falta alguna, detente y avisa. No la apliques sin permiso.
- **API y frontend.** Arranca el API con el build `3748ec6` apuntando a `wms_migracion`, y el frontend `7d7516a` apuntando a ese API. Antes se usaron el puerto 5291 para el API y el 3001 para el front, con la configuración de `db_legacy/trabajo/.env.migracion.local`.
  - Léelo sin imprimir secretos.
  - Anota en el informe los puertos y la base.
  - Si no puedes levantarlos, detente y pide ayuda; no recrees ni restaures bases.
- **Cuentas.** Las cuentas `mig.vigilancia`, `mig.bascula`, `mig.bodega`, `mig.comext` y `mig.facturacion` están en `db_legacy/trabajo/credenciales-migracion-local.local.md`. Las del Admin de esa base están en `.env.migracion.local`.
  - Úsalas solo en `localhost`.
  - Léelas sin imprimirlas.
  - No copies contraseñas a informes, fichas, evidencias ni a la salida de comandos.

## Reglas
1. **No modifiques código, configuración ni permisos.** Solo editas los documentos listados y creas datos de prueba en `wms_migracion`.
2. **Escritura en la base.** No escribes en la base con SQL: los datos se crean por la UI o por el API. Las consultas de solo lectura con `psql` sí están permitidas, para verificar persistencia.
3. **Datos de prueba con la marca `QA-SEL`:**
   - conductores `QA-SEL Uno`, `QA-SEL Dos`… con CC `9000000001`, `9000000002`…;
   - placas nuevas `QSL101`, `QSL102`…;
   - carta porte `QA-SEL-CP-0001`…;
   - la observación «QA-SEL» donde se pueda.
4. **No edites ni desactives conductores migrados.** El lápiz, la desactivación y los cambios de datos se prueban solo sobre conductores `QA-SEL`.
5. **Datos personales.** Los informes van a git, así que no llevan datos de personas naturales. Cuando busques sobre los migrados, describe el término de forma genérica («apellido común de 5 letras», «fragmento de 4 dígitos de una cédula», «nombre con tilde escrito sin tilde») y anota el `totalCount` y los tiempos, nunca nombres ni documentos reales. Las capturas de evidencia con datos reales se recortan o no se guardan.
6. **Limpieza.** Libera todo camión que ingreses: registra la salida en Vigilancia y descarta en «Recuperar operaciones» lo que no completes. Anota lo que quede creado: depósitos, facturas, conductores.
7. **Defectos.** Se numeran **DEF-F11-023** en adelante (D20). Cada uno lleva su ficha con la plantilla y una fila en `INDICE.md`, y una nota de actualización en su encabezado con la fecha y los hashes. Un BLOCKER detiene la ejecución (§2 del plan maestro): informe parcial y detenerse.

## Pasos
1. **Registro de casos** (plan §7.1):
   - En `fase-03-bascula.md`, reescribe en su sitio F3-CAM-003, 004 y 005 y agrega F3-CAM-013 a 022.
   - En `fase-04-bodega.md`, agrega F4-RSB-008 a 011.
   - En `fase-09-roles-permisos.md`, agrega F9-API-022 a 025.

   Usa el formato de tabla de cada documento: ID, Caso, Pasos, Resultado esperado, P y Tipo. Los pasos tienen que ser ejecutables por otra persona. Bajo la tabla CAM, agrega una nota: «Casos 003-005 reescritos y 013-022 agregados el 2026-10-XX por el selector de conductor (plan `docs/planes/plan-cerrado-selector-conductor-2026-10-08.md`)». Pon la misma nota en los otros dos documentos.
2. **Preparación de datos** con `mig.vigilancia`: ingresa los camiones que necesites (`QSL101`…).
   - Motivo «Solo Báscula» para las pruebas de báscula.
   - Un motivo de descargue de importación para F3-REG-001.
   - Motivo «Solo bodega» para la recepción directa.

   Anota cada dato en el informe (§7).
3. **Ejecución de los casos nuevos:**
   - F3-CAM-003 a 005 y 013 a 022, con `mig.bascula`. Para F3-CAM-022, desactiva `QA-SEL Dos` con el Admin, en Administración → Conductores.
   - F4-RSB-008 a 011, con `mig.bodega`. F4-RSB-008 sí guarda la recepción, porque crea un depósito `QA-SEL`.
   - F9-API-022 a 025, con `curl` y un token por rol obtenido por `POST /auth/login`, sin imprimir el cuerpo de la petición. Anota método, URL, código y un resumen del cuerpo de la respuesta.

   Para cada caso registra:
   - el estado (PASA, FALLA, BLOQUEADO, NO APLICA, NO EJECUTADO u OBSERVACIÓN);
   - la evidencia: captura en `docs/qa/resultados/evidencias/SEL/`, texto del mensaje, petición y respuesta.
4. **Criterios de §6 del plan,** dentro de F3-CAM-021:
   - el caso común sin clics extra;
   - Enter en el filtro elige la opción y no guarda la ficha;
   - el foco del modal en «Tipo de Documento»;
   - Esc cierra el modal;
   - «Guardar» sin conductor lleva el foco al select.

   Cronometra tres veces, con reloj, el tramo «Tab al select → conductor elegido» con un conductor existente. Anota los tiempos. Es una referencia, no PRF-002.
5. **Regresión dirigida:**
   - **F3-REG-001**, registro de importación mínimo, adaptado a `wms_migracion`: un cliente y un producto migrados existentes, carta porte `QA-SEL-CP-0001` y cantidad 10.
   - **F3-CAM-010**, persistencia en Solo báscula.
   - **F3-CAM-011**, persistencia en Salida. Solo si existe en `wms_migracion` una orden de cargue pendiente que puedas usar sin afectar datos de otros. Si no existe, márcalo NO EJECUTADO con el motivo; no armes una cadena de importación para él.
   - **F4-RSB-002**, crear un depósito desde la recepción directa. Puedes cubrirlo con F4-RSB-008.

   Tras F3-REG-001 no hace falta cobrar ni pesar: verifica el registro y el conductor del ingreso, y descarta la operación al final. Si descartar no es posible después de crear el depósito, anótalo.
6. **Medición del API** (plan §7.2): `GET /drivers?search=…&isActive=true&orderByName=true&pageSize=20` con 5 términos sobre los migrados, cada uno descrito de forma genérica (regla 5). Usa `curl -w '%{time_total}'`, 3 corridas por término, y anota el `totalCount`. Criterio: cada respuesta en menos de 1 s.
7. **Documentación de usuario** (plan §7.4):
   - En `guiones-video-tutoriales.md`, cambia los pasos de Báscula que capturan el conductor campo por campo (cerca de las líneas 654 y 671) y el de la Recepción Directa si lo describe (`grep -n "Recepción Directa"`). Los guiones usan conductores «Demo» con CC `1000000101`–`1000000199`. Con el selector:
     - el conductor que **ya existe** en el dataset se elige escribiendo parte de su nombre o cédula;
     - el que **no existe** se registra con «+».

     Revisa en `dataset-grabacion.md` §2.7 cuáles existen antes de cada video y escribe el paso que corresponda. Agrega una fila al inventario `inventario-cambios-guiones.md` si su formato lo admite.
   - Regenera el PDF siguiendo `generar-pdf.md`. Si WeasyPrint o Pango no están instalados, no instales nada: anota que el PDF queda por regenerar.
   - En `guia-pruebas-operarios.md`, ajusta los pasos de Báscula y Bodega que piden digitar el conductor.

   No cambies otros pasos.
8. **Informe:** crea `docs/qa/resultados/SEL-informe-{fecha}.md` con `plantillas/informe-fase.md`:
   - datos de la ejecución: hashes, base, puertos y cuentas por nombre de usuario;
   - criterios de entrada;
   - resumen por estado;
   - resultado por caso;
   - defectos nuevos;
   - mediciones del API y de teclado;
   - datos creados o modificados;
   - criterios de salida (P0 al 100 %, P1 ≥ 95 %);
   - checkpoint;
   - una sección **«Staging»** vacía, con el texto «Pendiente de la Fase 4».

   **El veredicto local** es «Listo para staging» si no hay defectos BLOCKER, CRITICAL ni MAJOR abiertos y se cumplen los criterios de salida. Si no, es «No listo», con el motivo.

## Trampas conocidas
- **Precarga asíncrona.** La consulta por documento de D16 tarda un poco. Si cambias rápido de camión, comprueba que el conductor precargado sea el del camión correcto (patrón de F3-CAM-007).
- **Navegador integrado.** Para cambiar de cuenta con una sesión pendiente de cambio de contraseña, borra `accessToken` y `refreshToken` de `localStorage`.
- **zsh**
  - Un `grep $(...)` con la sustitución vacía se cuelga: pasa `</dev/null`.
  - `for f in $VAR` no parte la lista: usa `while read`.
- **macOS:** no hay `timeout`.

## Entrega y detención
Al terminar, **detente** y entrega:

1. el veredicto local y el resumen por estado (PASA, FALLA y los demás);
2. los defectos nuevos con su severidad, o «ninguno»;
3. las mediciones del API y de teclado;
4. los archivos tocados en cada repositorio (`git status --short` en `Frontend/wms` y en `Backend/wms-api`);
5. los datos `QA-SEL` que quedaron en `wms_migracion`;
6. los mensajes de commit propuestos, cada uno con la línea de coautoría de tu modelo:
   - frontend: `docs(qa): casos y ejecución local del selector de conductor`;
   - backend: `docs(guiones): selector de conductor en Báscula y Bodega`.

**No empieces la Fase 4 (staging)** hasta que el usuario commitee y la autorice. Si hay defectos, la Fase 4 espera su corrección y el re-test.
