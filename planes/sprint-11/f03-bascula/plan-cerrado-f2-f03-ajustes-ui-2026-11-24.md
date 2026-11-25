# Plan cerrado — Fase 2 · F03 Báscula · Ajustes de UI de la maquetación

> **Fecha:** 24 de noviembre de 2026. **Estado:** Aprobado por el usuario el 2026-11-24 («Aprobar y ejecutar F1»). Ejecutado el 2026-11-24: fases 1 y 2 (FE `7eb7cfc` y `ee3d5d9`), en `f2/f03-bascula`, antes de I-03.
> **Origen:** la revisión del usuario sobre la maquetación de F03 (FE-1 a FE-3, datos simulados), antes de I-03: [`../qa-manual/hallazgos-UI-F03.md`](../qa-manual/hallazgos-UI-F03.md), cinco hallazgos y una duda. Las respuestas del usuario del 2026-11-24 están en D1 a D4.
> **Base:** FE `f2/f03-bascula` `ae34783` · docs `main` `2696bb4`. Rama: `f2/f03-bascula` (FE). Se aplica antes de I-03.
> **Alcance:** solo frontend, sobre las pantallas maquetadas con datos simulados. Sin cambios de backend (BE-1 a BE-3 ya cerraron), de contrato ni migraciones. Cambia decisiones del plan de F03 (D19, D23, D24, D25, D26 a D28, D37, D39 y D43): donde chocan, gana este plan.
> **Rutas:** relativas a `code_workspace/`. Prefijos: `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`; `P03/` = `D/planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-bascula-2026-11-24.md`; `PAJ/` = `D/planes/sprint-11/f02-base/plan-cerrado-f2-f02-ajustes-qa-2026-11-24.md`; `H/` = el archivo de hallazgos.

---

## 0. Instrucciones para el ejecutor

1. **Lecturas mínimas:** `Frontend/wms/AGENTS.md`, `D/procesos/flujo-de-trabajo-agentes.md`, `P03/` D19, D23 a D28, D37 a D40 y D43, `PAJ/` D3, D5 y D6, `H/` y este plan completo.
2. **Rama y git:** sigue en `f2/f03-bascula` (FE). Commit al cerrar cada fase con el mensaje de §7 y push. Sin `push --force`. Para borrar, `rm`.
3. **Líneas citadas:** son de `ae34783`. Confírmalas con grep; si el código no coincide, pregunta en un solo mensaje.
4. **Restricciones de la maquetación (`P03/` D38, D40):**
   - las pantallas siguen con las fuentes simuladas y no llaman al API;
   - no se enlaza nada nuevo en el menú (M4);
   - los componentes compartidos de `P03/` D38 no cambian. El menú de acciones de fila es un componente nuevo (D6) y no cambia ninguno de ellos.
5. **Convenciones:** las de `Frontend/wms/AGENTS.md`. Estilos con tokens de PrimeVue (`var(--p-…)`) y utilidades de Tailwind, sin colores fijos, para que funcione en tema claro y oscuro.
6. **Verificación:** `yarn dev` con `NUXT_PUBLIC_MOCK_SESSION=true` y `?roles=Admin,Scale` (Receiving para Vigilancia); cada pantalla en el navegador, con captura, en tema claro y en uno oscuro.

---

## 1. Decisiones

### 1.1 Respuestas del usuario (2026-11-24)

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **«Repesar» siempre lleva al paso «Repesaje» de la página de proceso** (D12): desde la cola, el historial, el drawer del detalle y `cycles/[id]`. El modal de repesaje desaparece | Usuario: «Ir a la página de proceso» |
| D2 | **Sin campo de observación para CE en los ciclos completados** (duda de `H/`). Los completados sí se editan: <br>• en Entradas, con motivo, mientras el depósito esté en Borrador (`P03/` D26, D31); <br>• en Salidas y Solo báscula, siempre con motivo (`P03/` D27, D28 y D35). <br>Con el depósito confirmado corrige Comercio Exterior (P-CE-03, F05). Un aviso nuevo chocaría con `P03/` D36 y reabriría el backend | Usuario: «No agregarlo (Recomendada)» |
| D3 | **La columna «Conductor» filtra por nombre o por documento con un solo campo de texto.** Si el texto es una sola palabra con algún dígito, la página envía `driverIdNumber`; si no, `driverName` (precisado en la fase 1: ver §4). Todo documento lleva dígitos, incluidos los pasaportes. Así no cambia el contrato: C-F03-22 a C-F03-24 ya aceptan los dos filtros. Ordena por `driverName`. Marcador: «nombre o documento» | Usuario: «se puede admitir buscar por nombre o documento (Ambos)»; `DEC-002` (sin cambio de contrato, porque BE-3 cerró) |
| D4 | **Los filtros de estado del panel de la cola van en un `Select` pequeño con contador**, junto al buscador: «Todos (12)», «Sin iniciar (3)», «Por pesar (2)», «Por cobrar (4)» y «Por repesar (3)». Son los cinco estados de la cola (`F/features/weighbridge/utils/queue-display.ts:13-19`), no solo los tres de hoy (`:22-26`) | Usuario: «Selector con contador (Recomendada)» |

### 1.2 Tablas: reglas generales (hallazgos 2 y 5)

| # | Decisión | Fuente |
| --- | --- | --- |
| D5 | **Botones de acción de fila con `size="small"`, como regla de todas las tablas.** Las 17 páginas con `AppDataTable` ya la cumplen (revisado en `ae34783`). Queda escrita en la convención (D16) | `H/` 2 |
| D6 | **Más de tres acciones posibles: todas van a un menú.** Si una tabla puede llegar a tener más de tres acciones por fila, todas pasan a un menú. Lo abre un botón de solo icono `pi pi-ellipsis-v`, pequeño, `text`, con tooltip «Acciones» y `aria-label` «Acciones: {registro}». <br>La regla es por tabla, no por fila: si la tabla puede pasar de tres, toda fila usa el menú, aunque solo tenga «Ver». Con tres o menos, siguen los botones de solo icono con tooltip (`PAJ/` D6). <br>Es la misma regla que el drawer (`PAJ/` D3), pero con umbral de tres. La implementa un componente nuevo, `F/components/app/AppRowActions.vue`: <br>• **props:** `actions` (`{ key, label, icon, severity?, visible }[]`, la lista completa de la tabla) y `subject`; <br>• **evento:** `select(key)`; <br>• **conducta:** decide botones o menú con el largo de `actions`, no con las visibles. <br>Hoy pasan de tres el historial de Báscula (cinco, en sus tres páginas) y Vigilancia › Historial (cuatro: Ver, Corregir, Autorizar salida y Agregar manifiesto). Ninguna otra tabla pasa de tres <br>**Ajustado por `plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md` (D2, D17):** la regla del menú se conserva; el botón «⋮» toma el estilo de Configuración (secundario, con borde y pequeño). | `H/` 5; `PAJ/` D3, D6 |
| D7 | **Placa en etiqueta.** La placa de la cola y de los tres historiales va en un `Tag` con `severity="secondary"`, `font-mono` y negrita. Lo hace un componente nuevo, `F/features/weighbridge/components/VehiclePlateTag.vue` (props `plate` y `duplicate`). En una entrada duplicada se agrega a su lado un `Tag` pequeño «D» (`severity="info"`), con tooltip «Entrada duplicada» y `aria-label` igual. Reemplaza la etiqueta «Duplicada» de la cola (`F/features/weighbridge/components/WeighbridgeQueueTable.vue:73`) y la del tiquete del historial (`F/pages/operations/weighbridge/history/index.vue:157`). El detalle (P-BAS-11) conserva «Duplicada» en «Tickets asociados», que tiene espacio | `H/` 2, 5 |
| D8 | **Pesos en una columna «Pesos (kg)»:** una línea por peso, con la etiqueta en negrita y el valor en texto atenuado y más pequeño. Si todos los pesos están vacíos, muestra «—». Lo hace `F/features/weighbridge/components/WeightLines.vue` (prop `lines: { label, value }[]`). Etiquetas por tabla: <br>• cola y Entradas: «P. bruto», «P. mercancía» y «Tara»; <br>• Salidas: «P. vehículo», «P. al salir» y «P. mercancía»; <br>• Solo báscula: «Pesaje», «Repesaje» y «Tara». <br>Salidas y Solo báscula se agrupan igual por coherencia, aunque el hallazgo nombra solo los pesos de Entradas. La columna no ordena ni filtra; el Excel conserva una columna por peso <br>**Ajustado por `plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md` (D16):** «Pesos (kg)» de Historial › Entradas suma «P. manifiesto»: P. bruto, P. manifiesto, P. mercancía y Tara. | `H/` 2, 5 |

### 1.3 Proceso de pesaje · cola (hallazgo 2; reemplaza parte de `P03/` D24)

| # | Decisión | Fuente |
| --- | --- | --- |
| D9 | **Cola sin búsqueda global.** <br>• **Filtros en las columnas:** se quita el buscador del slot `globalFilters` (`F/features/weighbridge/components/WeighbridgeQueueTable.vue:62-65`). «Placa» y «Conductor» llevan filtro de texto en la columna (modo `client`). El de «Conductor» conserva lo que hoy hace la búsqueda por conductor. <br>• **Estados en pestañas:** los filtros de estado pasan a `Tabs` de PrimeVue en el slot `toolbar`, como el historial. Cada pestaña lleva su contador en un `Badge`: Todos, Sin iniciar, Por pesar, Por cobrar y Por repesar. Se conserva `?estado=` (`P03/` D7). <br>• **Placa y pesos:** placa en etiqueta y «D» (D7); los tres pesos, en «Pesos (kg)» (D8). <br>• **Acción:** «Atender» sigue siendo la única acción, `small`, con etiqueta | `H/` 2; `P03/` D24 |

### 1.4 Proceso de pesaje · panel de la cola (hallazgo 3; reemplaza `P03/` D25)

| # | Decisión | Fuente |
| --- | --- | --- |
| D10 | **Panel compacto, en un solo contenedor.** <br>• **Contenedor:** sin tarjetas por camión y sin «Cargar a báscula →». La lista va en un contenedor con borde, con divisores de 1px entre filas. <br>• **Filas:** cada fila es un `button` que ocupa todo el ancho, con fondo suave al pasar el mouse. Al hacer clic carga el camión, igual que hoy el botón (`emit('load')`). <br>• **Línea 1:** placa en negrita a la izquierda y, a la derecha, el estado en un `Tag` pequeño («En atención» en el abierto). <br>• **Línea 2:** mercancía resumida (`merchandiseText`) a la izquierda y espera a la derecha, en texto atenuado y pequeño. <br>• **Camión abierto:** fondo `--p-primary-50` (oscuro: `color-mix` del primario) y borde izquierdo de 4px en `--p-primary-color`; sigue arriba de la lista. La entrada duplicada sin guardar sigue mostrándose como hoy, con la nueva forma. <br>• **Encabezado:** título, contador y «Actualizar» como hoy. Debajo, el buscador y el `Select` de D4 | `H/` 3 |
| D11 | **El panel no alarga la página.** El panel no pasa de la altura de la columna del formulario y nunca baja de unas cuatro filas. La lista se desplaza por dentro, con scroll vertical, y el encabezado, el buscador y el filtro quedan fijos. Así la página solo hace scroll por el formulario. <br>El hallazgo dice primero «máximo 4 registros» (frase incompleta) y luego «tal que ocupe la altura del formulario principal»; vale la segunda, que es la propuesta final. <br>Enter sobre una fila enfocada la carga y no guarda el formulario: `process-keys.ts` ya ignora Enter en un `BUTTON` y fuera del formulario (`F/features/weighbridge/utils/process-keys.ts:30-37`) | `H/` 3; `P03/` D23 |

### 1.5 Repesaje como paso de la página (hallazgo 4; reemplaza `P03/` D19 en su forma y ajusta D23 y D24)

| # | Decisión | Fuente |
| --- | --- | --- |
| D12 | **Paso «Repesaje» en `process/[entryLogId]`** (`?paso=repesaje`, con `servicio` y, en ingresos, `entrada`). <br>• **Contenido:** ocupa el espacio del formulario de registro, con lo mismo que el modal de hoy (`F/features/weighbridge/components/ReweighDialog.vue`): <br>  – un resumen del registro (modalidad, documento o salida, mercancía y conductor); <br>  – P. indicador y P. manifiesto de solo lectura; <br>  – el repesaje digitado (la tara en ingreso y solo báscula, el bruto al salir en salida); <br>  – la mercancía calculada con su diferencia con el manifiesto; <br>  – la fecha y hora precargadas. <br>  Usa las reglas puras de hoy (`F/features/weighbridge/utils/reweigh.ts`). <br>• **Encabezado:** el avance muestra «Repesaje › Tiquete» en lugar de los tres pasos. El botón principal «Registrar repesaje» va en el encabezado (`P03/` D10), junto a «Volver a la cola». <br>• **Guardado:** registra con C-F03-11, como hoy, y pasa al paso Tiquete. <br>• **Entrada que no se puede repesar** (ni «Por repesar» ni `canReweigh`): el paso muestra un `Message` («Esta entrada no tiene repesaje pendiente.») con el enlace al registro. <br>• **Componente:** `F/features/weighbridge/components/WeighbridgeReweighStep.vue` (nuevo) reemplaza a `ReweighDialog.vue`, que se borra con su prueba | `H/` 4; D1 |
| D13 | **Quién lleva al paso.** <br>• **La cola:** «Atender» en una entrada «Por repesar» lleva a `paso=repesaje` (`attendQuery`, `F/features/weighbridge/utils/queue-display.ts:86-91`), en lugar de abrir el modal sobre el registro. Se retira la apertura automática (`F/pages/operations/weighbridge/process/[entryLogId].vue:531-540`). <br>• **El historial, el drawer y `cycles/[id]`:** «Repesar» navega a la misma ruta (D1), que arma una regla pura nueva, `reweighRoute`, en `F/features/weighbridge/utils/entry-detail.ts`, como `processEditRoute`. <br>• **Ciclo de un solo pesaje ya cerrado:** el paso lo acepta aunque el camión ya haya salido por Vigilancia (`P03/` D19). Si el camión no está en la cola, el panel lo muestra como «En atención» con su placa (`currentPlate`) | `H/` 4; D1; `P03/` D19, D24 |
| D14 | **Teclado** (actualiza `P03/` D23). <br>• **Enter:** en el paso Repesaje registra el repesaje, con las mismas excepciones de hoy. <br>• **F2:** en una entrada «Por repesar», fuera del paso Repesaje, lleva a él; dentro del paso, lleva el foco al campo del repesaje. <br>• **Regla:** vive en `process-keys.ts`, con su prueba: `ProcessStep` suma `"repesaje"` y `openReweigh` pasa a `goToReweigh`. PRF-002 se sigue midiendo en el despliegue final | `P03/` D23; riesgo R6 |

### 1.6 Historial (hallazgo 5; ajusta `P03/` D26 a D28 y D37)

| # | Decisión | Fuente |
| --- | --- | --- |
| D15 | **Columnas de los tres historiales.** <br>• **Placa:** en etiqueta, con «D» en Entradas (D7). <br>• **Conductor:** una sola columna, con el nombre en la primera línea y el documento en la segunda, atenuado y pequeño. Filtra según D3. <br>• **Pesos:** en «Pesos (kg)» (D8). <br>• **Doc. entrada** (solo Entradas): el tipo en la primera línea, atenuado y pequeño, y el número en la segunda, en `font-mono`; mismo filtro (`document`). <br>• **Acciones:** en el menú de D6 (cinco posibles). «Anular» va en rojo (`severity="danger"`), separado de las demás por un divisor. <br>• **Sin cambios:** el Excel (una columna por dato) y la fila anulada en rojo. <br>Vigilancia › Historial (`F/pages/operations/entries/history.vue`) pasa sus cuatro acciones al menú de D6. Sus columnas no cambian: el hallazgo nombra el historial de Báscula | `H/` 5 |

### 1.7 Menú y convención

| # | Decisión | Fuente |
| --- | --- | --- |
| D16 | **Historial con submenú** (hallazgo 1; ajusta `P03/` D43). Las tres páginas ya existen desde FE-3: <br>• `F/pages/operations/weighbridge/history/index.vue` (Entradas); <br>• `history/exits.vue` (Salidas); <br>• `history/weighing-only.vue` (Solo báscula). <br>No se ven en el menú porque la maquetación no enlaza rutas (M4). I-03 deja Báscula como P-TR-01: Dashboard · Proceso de pesaje · Historial ▸ Entradas, Salidas, Solo báscula. «Historial» es un grupo con tres hijos, y `F/components/layout/AppMenuItem.vue:301-302` ya pinta submenús. Este plan solo corrige el texto de `P03/` D43 y §13.2 <br>**Ajustado por `plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md` (D18):** sin el grupo «Historial»: Entradas, Salidas y Solo báscula van al primer nivel del menú de Báscula. | `H/` 1; P-TR-01 (`D/levantamiento-2026-11/fase_2-mockups/transversales.html`) |
| D17 | **La convención queda escrita**: un apartado «Tablas de listado» en `D/contexto/convenciones-tecnicas.md` §3, con D5 y D6 (y el enlace a `PAJ/` D3 y D6). La galería `F/pages/dev/components.vue` muestra `AppRowActions` con tres y con cinco acciones | `H/` 2, 5 |

---

## 2. Archivos que se tocan

| Archivo | Fase | Cambio |
| --- | --- | --- |
| `F/components/app/AppRowActions.vue` (nuevo) | 1 | D6 |
| `F/features/weighbridge/components/VehiclePlateTag.vue`, `WeightLines.vue` (nuevos) | 1 | D7, D8 |
| `F/features/weighbridge/components/WeighbridgeQueueTable.vue`; `F/pages/operations/weighbridge/index.vue` | 1 | D9 (el `v-model:search` sale) |
| `F/features/weighbridge/components/WeighbridgeHistoryActions.vue` | 1 | Arma la lista de cinco acciones y usa `AppRowActions` (D6) |
| `F/pages/operations/weighbridge/history/index.vue`, `exits.vue`, `weighing-only.vue` | 1 | D15, D3 |
| `F/features/weighbridge/utils/history-display.ts` | 1 | `driverFilterQuery` (D3), puro, con prueba |
| `F/pages/operations/entries/history.vue` | 1 | D6 |
| `F/pages/dev/components.vue` | 1 | D17 |
| `F/features/weighbridge/components/WeighbridgeQueuePanel.vue`; `F/features/weighbridge/utils/queue-display.ts` | 2 | D4, D10, D11, D13 (`attendQuery`; `PANEL_FILTERS` sale) |
| `F/pages/operations/weighbridge/process/[entryLogId].vue`; `F/features/weighbridge/components/WeighbridgeProcessHeader.vue` | 2 | D12 a D14 |
| `F/features/weighbridge/components/WeighbridgeReweighStep.vue` (nuevo); `ReweighDialog.vue` (se borra) | 2 | D12 |
| `F/features/weighbridge/components/WeighbridgeEntryDialogs.vue`; `F/features/weighbridge/composables/useHistoryDrawer.ts`; `F/pages/operations/weighbridge/cycles/[id].vue`; `F/features/weighbridge/utils/entry-detail.ts` | 2 | D13 («Repesar» navega; `reweighRoute`) |
| `F/features/weighbridge/utils/process-keys.ts` | 2 | D14 |
| `FT/unit/components/AppRowActions.spec.ts` (nuevo); `FT/components/weighbridge/WeighbridgeHistoryActions.spec.ts`; `FT/unit/weighbridge/history-display.spec.ts` o el que ya prueba `history-display` | 1 | §5 |
| `FT/components/weighbridge/WeighbridgeReweighStep.spec.ts` (nuevo, desde `ReweighDialog.spec.ts`, que se borra); pruebas de `process-keys`, `queue-display` y `entry-detail` | 2 | §5 |
| `D/contexto/convenciones-tecnicas.md` §3; `P03/` D19, D23 a D25, D39, D43 y §13.2 (nota «ajustado por …»); `H/` (decisión por punto); `D/planes/README.md`; `D/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md` §3; la matriz | 2 (cierre) | D16, D17 y estado |

---

## 3. Fuera de alcance

- El campo de observación para CE de los completados (D2).
- Cambios de contrato o de backend: el filtro del conductor se resuelve en la página (D3).
- Enlazar las rutas en el menú: lo hace I-03 (D16, M4).
- Las columnas de Vigilancia › Historial (D15) y las tablas de F01 y F02, que ya cumplen D5 y no pasan de tres acciones (D6).

---

## 4. Fases

| Fase | Contenido | Criterio de salida | Estado |
| --- | --- | --- | --- |
| 1 | Reglas de tabla (D5 a D8), cola (D9), historiales de Báscula (D15, D3), acciones de Vigilancia › Historial y galería (D17) | Compuertas de §6; QA-AJ3-001 a 006 en PASA | Hecha el 2026-11-24 (FE `7eb7cfc`). QA-AJ3-001 a 006 en PASA en el navegador con datos simulados (Admin y Báscula; Vigilancia en 006). Capturas `evidencias/aj1-01` a `aj1-07`. <br>• **Compuertas:** `yarn test` de 155 a 157 archivos y de 795 a 802 pruebas; lint de 239 a 239 errores, ninguno en archivos nuevos o tocados; `yarn build` en 0. <br>• **Caso borde de D3 (`DEC-002`):** los nombres de los datos simulados llevan dígitos («Conductor 4»), y con la regla tal cual se buscaban como documento. Ahora es documento si es una sola palabra con algún dígito («1020», «1.000.001», «AB123456»); si no, es nombre. Sigue sin cambiar el contrato. <br>• **Tipos aparte:** `AppRowActions` toma sus tipos de `F/types/app-row-actions.ts`, porque `<script setup>` no exporta constantes. <br>• **`components.d.ts`:** registra `Tabs`, `TabList` y `Tab` |
| 2 | Panel de la cola (D4, D10, D11), repesaje como paso (D12 a D14); docs y convención (D16, D17) | Compuertas; QA-AJ3-007 a 012 en PASA | Hecha el 2026-11-24 (FE `ee3d5d9`). QA-AJ3-007 a 012 en PASA en el navegador con datos simulados (Admin y Báscula). Capturas `evidencias/aj2-01` a `aj2-06`. <br>• **Repesaje:** «Atender» en XYZ987 abre el paso sin modal, con el foco en el peso; Enter registra y pasa al Tiquete con Repesaje › Tiquete. «Repesar» de VWX159 (solo báscula, ciclo cerrado) desde el menú del historial y desde el drawer lleva al paso, y el panel la marca «En atención · Fuera de la cola». F2 desde el registro lleva al paso y, dentro, enfoca el peso. <br>• **Panel:** el selector muestra los cinco estados con su contador y filtra; el clic en una fila carga el camión (PQR741, una salida «Por repesar», abre su repesaje). Con la ventana a 620 px de alto, la lista se desplaza por dentro. Se ve bien en tema oscuro. <br>• **Compuertas:** `yarn test` 157 archivos (sale `ReweighDialog.spec.ts`, entra `WeighbridgeReweighStep.spec.ts`) y de 802 a 804 pruebas; lint de 239 a 239 errores, ninguno en archivos nuevos o tocados; `yarn build` en 0. <br>• **Casos borde (`DEC-002`):** el tiquete que sigue al repesaje lleva `&flujo=repesaje` para conservar los pasos Repesaje › Tiquete. Un camión abierto que no está en la cola dice «Fuera de la cola», y una entrada sin guardar dice «Entrada sin guardar». <br>• **Cierre:** convención «Tablas de listado» en `contexto/convenciones-tecnicas.md` §3; notas «Ajustado por este plan» en el plan de F03 (D19, D23 a D28, D37, D39, D43, §3.1 y §13.2) |

---

## 5. Pruebas y casos QA

**Vitest:**

- `AppRowActions.spec.ts`: con tres acciones, botones de solo icono con tooltip y `aria-label`. Con cinco posibles y solo una visible, un solo botón «Acciones» cuyo menú tiene esa acción; `select` emite la clave.
- `WeighbridgeHistoryActions.spec.ts`: se reescribe sobre el menú. Los elementos del menú y sus eventos siguen las marcas; una fila anulada solo tiene «Ver detalle».
- `history-display`: `driverFilterQuery("Pérez")` → `{ driverName }`; `driverFilterQuery("1020")` → `{ driverIdNumber }`; vacío → `{}`.
- `queue-display`: `attendQuery` con «Por repesar» → `paso: "repesaje"`.
- `process-keys`: Enter en `repesaje` → `submit`; F2 «Por repesar» fuera del paso → `goToReweigh`, y dentro → `focusReweigh`.
- `entry-detail`: `reweighRoute` para una entrada (con `entrada`) y para un servicio.
- `WeighbridgeReweighStep.spec.ts`: los casos de `ReweighDialog.spec.ts` (datos, cálculo, diferencia con el manifiesto, guardado) sobre el paso.

**Casos QA** (navegador, datos simulados, Admin y Báscula; Vigilancia en QA-AJ3-006):

| Caso | Hallazgo | Pasos | Resultado esperado |
| --- | --- | --- | --- |
| QA-AJ3-001 | 2 | Proceso de pesaje: pestañas de estado, filtro de placa y de conductor en la columna | Sin buscador global; cada pestaña filtra y muestra su contador; `?estado=` se conserva al recargar |
| QA-AJ3-002 | 2 | Cola: una entrada duplicada y una «Por cobrar» | Placa en etiqueta con «D» y su tooltip; «Pesos (kg)» con tres líneas; «—» en «Sin iniciar» |
| QA-AJ3-003 | 5 | Historial › Entradas: columnas y filtro del conductor con «Pérez» y con un documento | Placa en etiqueta y «D»; conductor en dos líneas; doc. entrada en dos líneas; pesos agrupados; el filtro encuentra por nombre y por documento |
| QA-AJ3-004 | 5 | Historial › Entradas: menú de una fila completa y de una anulada | Un solo botón «Acciones»; el menú tiene las acciones según las marcas; la anulada, solo «Ver detalle»; la fila anulada sigue en rojo |
| QA-AJ3-005 | 5 | Historial › Salidas y › Solo báscula | Mismas reglas, con sus etiquetas de pesos |
| QA-AJ3-006 | 5 | Vigilancia › Historial, con Vigilancia | Las cuatro acciones en el menú y funcionando |
| QA-AJ3-007 | 3 | Registro: panel con más camiones de los que caben | Una lista continua con divisores; el abierto con fondo y borde izquierdo; la lista se desplaza por dentro y la página no se alarga |
| QA-AJ3-008 | 3; D4 | Panel: el selector de estado y el buscador; clic en una fila | Los cinco estados con contador; la fila carga el camión |
| QA-AJ3-009 | 4 | Cola: «Atender» en una «Por repesar» | Abre el paso Repesaje en la página, sin modal; Enter registra y pasa al Tiquete |
| QA-AJ3-010 | 4; D1 | Historial y drawer: «Repesar» en un ciclo de un solo pesaje cerrado | Lleva al paso Repesaje de esa entrada; el panel la marca «En atención» |
| QA-AJ3-011 | 4; D14 | Registro de una «Por repesar»: F2 | Lleva al paso Repesaje; dentro, F2 enfoca el campo |
| QA-AJ3-012 | 3, 4 | Panel y paso Repesaje en tema oscuro | Fondos, bordes y textos legibles |

---

## 6. Compuertas de cada fase

- `yarn build` con código 0.
- `yarn test` en verde. Base: 155 archivos y 795 pruebas (FE-3).
- `yarn lint` con 239 errores o menos (base de FE-3) y ninguno en archivos nuevos o tocados.
- La guardia `FT/unit/guards/mock-sources.spec.ts` sigue en verde: ninguna pantalla importa una fuente integrada.
- Capturas de los casos de la fase.

---

## 7. Commits

| Fase | Repo | Mensaje |
| --- | --- | --- |
| 1 | FE | `style(bascula): cola e historiales con placa en etiqueta, pesos agrupados y acciones en menú (DEC-080, F03, QA manual UI)` |
| 2 | FE | `style(bascula): panel de la cola compacto y repesaje como paso de la página de proceso (DEC-080, F03, QA manual UI)` |
| 2 | docs | `docs(f03): ajustes de UI de la maquetación; convención de acciones en tablas` |

Al cerrar: el estado de este plan y su fila en `D/planes/README.md`; las notas «ajustado por este plan» en `P03/`; una línea en el seguimiento §3 con los commits; `H/` marca cada punto con su decisión.

---

## 8. Riesgos

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R1 | Un documento sin dígitos se busca por nombre y no aparece (D3) | Todo documento de identidad lleva dígitos; si en la QA de I-03 aparece uno, se pide `driver` (nombre o documento) al backend en un plan aparte |
| R2 | El paso Repesaje desde el historial abre un camión que ya salió y el panel no lo tiene | D13: el panel lo marca «En atención» con `currentPlate`, como la entrada duplicada sin guardar |
| R3 | El panel con altura limitada se ve cortado en pantallas bajas | D11: mínimo de unas cuatro filas; QA-AJ3-007 en el ancho y alto habituales de la báscula |
| R4 | Mover las acciones al menú esconde «Ver», la más usada | Es la regla pedida (D6); el menú se abre con un clic y con teclado |
