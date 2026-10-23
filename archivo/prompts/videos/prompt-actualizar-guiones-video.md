Eres el redactor técnico que **actualiza los guiones de los video tutoriales** del WMS de Bodegas Asociadas para que el usuario los grabe. Modelo recomendado: **Opus 5.5**: hay que leer mucho código y documentación para saber cómo funciona hoy cada pantalla.

## Punto de partida
- **Guiones actuales:** `docs/videos/Guiones_Video_Tutoriales_WMS.pdf`, versión 1.0 de julio de 2026, 31 páginas.
  - **No hay archivo fuente editable:** solo existe el PDF, generado con pypdf.
  - Tiene 8 series: 0 Introducción, 1 Administración, 2 Acuerdos, 3 Facturación, 4 Vigilancia, 5 Báscula, 6 Bodega y 7 Comercio Exterior.
  - Son unos 50 guiones con el mismo formato: **número y título, duración y rol, OBJETIVO, REQUISITOS, una tabla `# | En pantalla (lo que haces) | Narración sugerida (lo que dices)` y Cierre.**
  - La sección A explica cómo leer un guion y da recomendaciones de producción.
- **Están desactualizados:** se escribieron antes de las Olas 1 a 3, la paridad con el legacy, la corrección de los defectos del QA (CHG-01 a CHG-90 y DEF-F11-001 a 022) y la migración. Muchas pantallas, botones y flujos cambiaron.
- **El manual de usuario** (`docs/manuales/Manual_Usuario_WMS.pdf`, también de julio) puede servir de contexto, pero **no lo actualices**: está fuera de alcance.

## Lee primero
1. `Backend/wms-api/AGENTS.md` y **el documento de contexto** que indica, entero: negocio, glosario, flujos y facturación.
2. **El PDF actual:** extrae el texto con `pdftotext -layout` en tu carpeta temporal y léelo completo.
3. **Cómo funciona hoy el sistema.** El código manda; los documentos explican el porqué.
   - **Menú por rol y nombres de las entradas:** `Frontend/wms/app/components/layout/AppMenu.vue`.
   - **Pantallas:** `Frontend/wms/app/pages/` y `app/features/*/components/`. Toma los títulos, botones, pasos de los asistentes y mensajes de ahí, **con su texto exacto**.
   - **Decisiones y cambios:**
     - `docs/qa/plan-correccion-defectos.md`: las tarjetas CHG con su «Dado/Cuando/Entonces» y las decisiones D-1 y D-2;
     - `docs/qa/00-plan-maestro.md` §10, con las reglas de negocio confirmadas;
     - `docs/qa/resultados/informe-final.md` y las fichas en `docs/qa/resultados/defectos/`;
     - los planes de las Olas en `code_workspace/ajustes/` (`plan_implementacion_ola2.md`, `plan_implementacion_ola3.md` y el de la Ola 1);
     - `docs/planes/paridad-legacy/plan-backend-paridad-legacy.md` y `docs/planes/paridad-legacy/plan-frontend-paridad-legacy.md`.
   - **Lo que verán los operarios:** `docs/planes/migracion-staging/resultados/guia-pruebas-operarios.md`, con los pasos ya probados por rol.

## Qué hacer

### 1. Inventario de cambios (antes de reescribir)
Arma una tabla **guion por guion**, con estas columnas:
- número, título, rol y estado;
- qué cambió, con su fuente: CHG, DEF, decisión o archivo de código.

Los estados posibles:

| Estado | Cuándo |
|---|---|
| **Vigente** | Sin cambios. |
| **Actualizar** | El flujo cambió. |
| **Reemplazar** | La función se rehízo. |
| **Retirar** | La función ya no existe. |
| **Nuevo** | Una función que no tiene guion. |

**Ejemplos de lo que debes revisar,** verificando cada uno en el código:
- **Báscula:**
  - la pantalla única con la cola y sus filtros;
  - el registro único con el cobro;
  - el multidepósito con el depósito adicional y la factura en cero;
  - Solo báscula;
  - la reanudación de una operación;
  - la corrección de pesos y el autor de la modificación;
  - el reporte diario por tiquete;
  - se retiró el efectivo y el cambio a devolver;
  - se retiró «Cambiar modo de pago» del historial (D-2).
- **Vigilancia:** el formato de placa, un ingreso abierto por placa, la corrección de placa, motivo y fecha, y la salida con sus validaciones.
- **Bodega:** la recepción directa, la recepción con unidades de carga, el montacargas con «Aplicar IVA» y las tarifas por tipo de vehículo, el cargue con firma y las ubicaciones no disponibles.
- **Comercio Exterior:**
  - confirmar el depósito y sus requisitos;
  - validación y manifiesto;
  - levantes y nacionalización;
  - Kanban;
  - orden de cargue y guía de salida con saldos;
  - abandono;
  - anulado en solo lectura;
  - corrección de productos y CE-7.
- **Facturación:**
  - la factura en cero sin número;
  - el N.º SIIGO y la aprobación;
  - el vencimiento solo al aprobar;
  - mora y bloqueo del cliente;
  - pagos con comprobante de hasta 5 MB;
  - la TRM de la DIAN y la manual;
  - el recálculo del almacenamiento;
  - el reporte por CPI con la anulada.
- **Administración:**
  - usuarios con cambio de contraseña obligatorio;
  - la recuperación por correo solo para el Admin (CHG-51);
  - terceros con contactos y cuentas;
  - tarifas base y reglas por modalidad;
  - mínimos con o sin IVA;
  - catálogos y ubicaciones;
  - auditoría.
- **El menú:** «Estadísticas» está oculto por decisión del usuario, así que **no hay guion de Estadísticas**. Los respaldos y la migración del legacy no tienen pantalla: **no llevan guion**, porque son tareas técnicas.

**Guarda el inventario** en `docs/videos/guiones/inventario-cambios-guiones.md`.

### 2. Checkpoint con el usuario
**Antes de reescribir,** muéstrale al usuario en el chat:
- un resumen del inventario: cuántos guiones quedan en cada estado;
- la lista de los **Nuevos** y los **Retirados** que propones;
- el **ambiente de grabación** que propones (ver §4).

**Espera su aprobación o sus cambios.**

### 3. Reescritura
- **Formato:** el mismo del PDF actual (OBJETIVO, REQUISITOS, la tabla «En pantalla / Narración sugerida» y Cierre), con el mismo tono: tuteo, frases claras y la apertura «En este video vas a…».
- **Rutas del menú:** con los nombres **exactos** de `AppMenu.vue`, separados con «›». Para cada guion, indica **con qué rol** se graba.
- **Pasos «En pantalla»:**
  - el botón, la pestaña o el campo con su texto real;
  - y **el resultado esperado**: el mensaje o el estado que debe verse, también con su texto real.
- **Narración:**
  - explica **para qué** sirve cada paso, con los términos del negocio del glosario;
  - incluye **la regla importante cuando aplique**, por ejemplo «la factura en $0 no lleva número», «el vencimiento se fija al aprobar» o «la báscula solo cobra lo de este camión».
- **Duración:** de 2 a 5 minutos. Si un flujo se alarga, divídelo en dos videos (§A.2).
- **Orden de grabación:** el plan maestro de la sección A, en el orden en que tiene sentido grabarlos, para que cada video deje listos los datos del siguiente. Por ejemplo: crear un tercero → crear el acuerdo → registrar el ingreso → pesar → recibir → confirmar → levante → OC → cargue → guía → facturar.
- **REQUISITOS:** los datos que deben existir antes de grabar ese video, citando el dataset de grabación del §4.
- **Versión y fecha:** 2.0, octubre de 2026. Agrega al inicio un **registro de cambios** de una página: qué guiones son nuevos, cuáles se actualizaron y cuáles se retiraron.

### 4. Ambiente y datos de grabación (propuesta para el checkpoint)
**Regla del documento actual (§A.2):** «usa un cliente y productos ficticios; no muestres datos reales». **Staging tiene datos reales del legacy:** clientes, conductores y vehículos. **No propongas grabar en staging.**

**Propón:**
1. **Ambiente:** un ambiente aparte con datos **ficticios**, por ejemplo una base local nueva con el build actual (`dotnet ef database update`).
2. **El dataset de grabación** en `docs/videos/guiones/dataset-grabacion.md`:
   - terceros ficticios: cliente, importador, agencia, transportadora y exportador;
   - productos y embalajes;
   - vehículos y conductores ficticios, con placas de formato válido;
   - tarifas: las de staging son buenas de referencia, porque son las reales (báscula $16.806,72 + IVA, guía $15.000, almacenamiento de importación 0,295 % con mínimo de $50.000, y los montacargas);
   - un acuerdo de ejemplo;
   - las cuentas por rol.

   Para cada dato, indica en qué guion se crea en cámara y cuál debe existir antes.

**No crees los datos ni el ambiente:** solo documéntalos. Si el usuario lo aprueba, se preparan después con otro prompt.

### 5. Entregables
- **Fuente editable:** `docs/videos/guiones/guiones-video-tutoriales.md`, en Markdown, con un archivo único y una sección por serie. Desde ahora esta es la fuente; el PDF se genera desde aquí.
- **El PDF nuevo:** `docs/videos/Guiones_Video_Tutoriales_WMS.pdf`, que **reemplaza** al anterior; la versión 1.0 queda en el historial de git.
  - Genéralo desde el Markdown con HTML y CSS de impresión, en tamaño carta, con un aspecto parecido al actual: portada, encabezado y pie «Guiones de Video Tutoriales · Centro de Ayuda — Sistema WMS · Página N de M», y las tablas de guion.
  - Revisa que las tablas no se corten mal entre páginas.
  - Deja el script o el comando de generación en `docs/videos/guiones/generar-pdf.md`.
- **El inventario** (§1) y **el dataset de grabación** (§4).

## Reglas
- **El código manda.** Si un documento y el código no coinciden, describe lo que hace el código y anota la diferencia en el inventario.
- **No inventes pantallas, botones ni mensajes.** Si no puedes confirmar un texto en el código, márcalo `[verificar en pantalla]`.
- **Puedes mirar staging solo para leer**, con una cuenta `qa.*`, cuyas contraseñas están en `code_workspace/db_legacy/trabajo/credenciales-qa-staging.local.md`; léelas sin imprimirlas. Úsalo para confirmar nombres y pasos. **No crees, edites ni apruebes nada** en staging, y no copies a los guiones ningún dato real que veas allí.
- **Sin datos reales en los guiones:** ni clientes, ni conductores, ni placas, ni números de depósito de la migración. Solo los del dataset ficticio.
- **Sin secretos.**
- **No cambies código** ni el manual de usuario.
- Trabaja en `develop` sin ramas y **sin commits**: entrega el mensaje.
- Textos en español.

## Entrega y detención
1. Después del checkpoint y la reescritura, responde con:
   - el resumen de cambios: cuántos guiones vigentes, actualizados, reemplazados, retirados y nuevos;
   - el número de páginas del PDF;
   - los textos que quedaron `[verificar en pantalla]`.
2. **El mensaje de commit:** `docs(guiones): guiones de video tutoriales v2.0 con fuente editable, inventario de cambios y dataset de grabación`, con la línea de coautoría que corresponde a tu modelo.

**Detente ahí.**
