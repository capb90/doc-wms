# Plan cerrado — Fase 2 · F03 Báscula · El operario elige el tipo de operación al atender

> **Fecha:** 27 de noviembre de 2026. **Estado:** Propuesto.
> **Origen:** pedido del usuario del 2026-11-27 («Báscula: el operario elige el tipo de operación al atender, sin depender de Vigilancia»), con su diseño de referencia ([canvas «Báscula — Tipo de operación explícito»](https://claude.ai/artifact/D2BcbcEmz3Bf7KrCGYjhSL): artboards «1 · Cola» y «2 · Formulario»). Las respuestas del usuario a la ronda de este plan (2026-11-27) están en D1 a D3.
> **Base:** BE `fase-2` `a81b99c` · FE `fase-2` `efa65ff` · docs `main` `c39ea31`. Rama: `f2/f03-tipo-operacion` en BE y en FE.
> **Alcance:** backend y frontend. Se elimina la categoría del motivo de ingreso (una migración). El tipo de operación lo elige Báscula al atender un camión «Sin iniciar». Los campos de cada variante del formulario no cambian; cambia de dónde sale la variante.
> **Qué reemplaza:** la parte de la categoría de AF-08 y M22 (plan maestro §1.2); D12 de F01 y la regla de «la misma categoría» de su D13; la columna y el campo «Categoría» de P-TR-04 (F02); D11 de F03 («El formulario lo decide la categoría del motivo»); la regla «motivo de categoría ingreso» de D10 del plan de ajustes de la QA de F03; y el filtro de motivos de la edición del ingreso de CE (F05). Donde chocan, gana este plan.
> **Rutas:** relativas a `code_workspace/`. Prefijos: `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`; `P01/` = `D/planes/sprint-11/f01-nucleo/plan-cerrado-f2-f01-nucleo-2026-11-21.md`; `P03/` = `D/planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-bascula-2026-11-24.md`; `AUI/` = `D/planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-ajustes-ui-2026-11-24.md`; `AQ/` = `D/planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md`; `DIS/` = el diseño de referencia.

---

## 0. Instrucciones para el ejecutor

1. **Lecturas mínimas:** los dos `AGENTS.md` de los repos, `D/procesos/flujo-de-trabajo-agentes.md`, `D/contexto/convenciones-tecnicas.md` §3 y §10, este plan completo, y de los planes anteriores solo lo que cita cada decisión: `P01/` D12 y D13, `P03/` D5, D11, D23 y D24, `AUI/` D9 y D14, `AQ/` D7, D10 y D11.
2. **Cuándo:** antes de lanzar F07 (plan maestro §4, regla 5: las correcciones de las pruebas del usuario van antes de la siguiente fase de cualquier feature). Un agente a la vez por repo (M10): si otra sesión trabaja en el backend o en el frontend, espera a que termine.
3. **Ramas y git:** `f2/f03-tipo-operacion` en BE y en FE, desde `fase-2`. Commit y push al cerrar cada fase, con el mensaje de §8. Al cerrar la fase 3, fusión en `fase-2` con `--no-ff` en los dos repos y push. Sin `push --force`. Para borrar, `rm`.
4. **Una fase por turno** (`AGENTS.md`): al cerrar cada una, compuertas, commit, estado en este plan y en la matriz, y reporte.
5. **Líneas citadas:** son de la base. Confírmalas con grep; si el código no coincide, pregunta en un solo mensaje. Si un caso borde choca con una Dn, gana la Dn (`DEC-002`).
6. **Migración:** solo con `dotnet ef … --project Wms.Infrastructure --startup-project Wms.Api`, aplicada solo en la base local, en el mismo commit que el código (`DEC-004`, M6).
7. **Verificación:** `yarn dev` sin sesión simulada contra el API local (`.claude/launch.json`), con Administrador, Vigilancia y Báscula. Capturas en `D/planes/sprint-11/f03-bascula/evidencias/tio-*`.
8. **Docs:** otros agentes usan la misma copia de `docs` y su índice de git. Commitea solo tus archivos (`git commit -m … -- <rutas>`) y revisa `git diff --cached --name-only` antes.

---

## 1. Decisiones

### 1.1 Respuestas del usuario (2026-11-27)

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **Se conserva «Requiere pesaje»** en el motivo de ingreso. Sigue decidiendo si el camión pasa a la cola de Báscula (`B/Wms.Application/Weighbridge/Queries/GetWeighbridgeQueue/GetWeighbridgeQueueHandler.cs:45`). Un motivo como «Solo bodega» sigue sin ir a Báscula. El motivo sigue siendo obligatorio en Vigilancia | Usuario: «"Requiere pesaje" (Recomendada)» (completa la frase «Se conserva …» del pedido) |
| D2 | **«Cambiar tipo» solo antes de guardar.** Mientras el registro no está guardado, cambiar el tipo solo cambia las secciones 3 y 4 (D9). Con el registro guardado, el botón queda deshabilitado con el tooltip «Para cambiar el tipo, anule el registro y atienda el camión de nuevo.». No se convierte nada ya guardado | Usuario: «Solo antes de guardar (Recomendada)». El diseño decía «Solo mientras no haya un pesaje registrado» (`DIS/` Formulario); gana la respuesta |
| D3 | **El tipo se guarda con el registro.** Elegirlo en el menú no guarda nada. Si el operario sale sin guardar, el camión vuelve a «Sin iniciar» con el tipo «Por definir». Un camión iniciado guarda su tipo en su operación de báscula, como hoy | Usuario: «Al guardar el registro (Recomendada)» |

### 1.2 Lo que fija el pedido

| # | Decisión | Fuente |
| --- | --- | --- |
| D4 | **El tipo ya no sale del motivo.** Se elimina `EntryReason.Category` del dominio, del API, de la semilla y de la base. El tipo de un camión iniciado sale de su operación de báscula (`WeighbridgeEntryView.CategoryOf`, `B/Wms.Application/Weighbridge/Common/Services/WeighbridgeEntryView.cs:153-157`), como hoy. El de un camión «Sin iniciar» es nulo («Por definir») hasta que se guarda su registro | Pedido |
| D5 | **«Atender» en un camión «Sin iniciar» abre el menú de tipo** (D6). Al elegir una opción se abre el registro de ese tipo (D11). Un camión iniciado («Por pesar», «Por cobrar», «Por repesar») lleva el botón **«Continuar»**, que abre el registro con su tipo guardado, sin menú. La consulta de hoy (`attendQuery`, `F/features/weighbridge/utils/queue-display.ts:106-112`) no cambia para los iniciados | Pedido; `P03/` D5 |
| D6 | **Menú de tipo idéntico al diseño** (`DIS/` Cola, el `role="menu"` de «Atender»). Componente nuevo `WeighbridgeOperationTypeMenu` (`F/features/weighbridge/components/`): <br>• **Título:** «¿Qué operación vas a registrar?» (13 px, peso 600). <br>• **Opciones** (en este orden), cada una con icono en un cuadro de 34 × 34 px con radio 8 px, nombre (14 px, peso 600), descripción (12 px, `#5B6676`) y atajo en un `<kbd>` monoespaciado: **Entrada** (E), «Descargue al depósito · 1.er pesaje bruto», flecha hacia abajo sobre una línea, fondo `#E6F0FC` y texto `#1557AE`; **Salida** (S), «Retiro del depósito · 1.er pesaje tara», flecha hacia arriba sobre una línea, fondo `#FDF0DC` y texto `#8A4A06`; **Solo pesaje** (P), «Pesaje de tercero, sin documentos», balanza, fondo `#EFE9FB` y texto `#5432A6`. Los iconos son los SVG en línea del diseño. <br>• **Caja:** 340 px de ancho, borde `#D7DEE8`, radio 10 px, sombra `0 12px 32px rgba(20,30,50,.16)`, relleno 6 px; la opción con relleno 10 px, radio 8 px y fondo `#F3F6FA` al pasar el puntero. <br>• **Posición:** alineado a la derecha del botón, debajo; si no cabe debajo (cerca del final de la tabla o de la ventana), se abre hacia arriba. <br>• **Teclado:** al abrir, el foco va a la primera opción; E, S y P eligen; flechas para moverse; Enter elige; Escape cierra y devuelve el foco a «Atender». Los atajos solo valen con el menú abierto (sin manejador global). <br>• **Tema oscuro:** el diseño solo dibuja el claro. Los colores de arriba van como variables CSS del componente; en oscuro se usan las variantes del mismo tono con contraste 4.5:1 (regla del proyecto) | Pedido («el menú … debe quedar idéntico al diseño»); `DIS/` Cola; `P03/` D23 (teclado, R6) |
| D7 | **Lo demás conserva sus estilos.** La cola y el formulario mantienen componentes, colores, tipografía y disposición de hoy. Lo nuevo fuera del menú (la columna de tipo, la etiqueta del encabezado y «Cambiar tipo») usa los componentes de hoy: `Tag` para el tipo y `Button` `size="small"` `severity="secondary"` `outlined` para «Cambiar tipo», como los botones del encabezado (`F/features/weighbridge/components/WeighbridgeProcessHeader.vue:85-135`) | Pedido («No se deben modificar los estilos actuales») |
| D8 | **Etiqueta del tipo** (`WeighbridgeOperationTypeTag`, nuevo): «Entrada», «Salida» o «Solo pesaje» con los colores de su opción del menú (D6); «Por definir» con fondo blanco, texto `#4A5463` y borde punteado `#A9B2BF`, como en `DIS/` Cola. La usan la columna de la cola, el panel de la cola y el encabezado del registro | Pedido («los mismos colores por tipo»); `DIS/` |
| D9 | **«Cambiar tipo» en el encabezado del registro**, junto a la etiqueta del tipo y la placa. Abre `WeighbridgeOperationTypeMenu` con las tres opciones (el mismo menú de «Atender»). <br>• Antes de guardar (D2): cambiar de tipo conserva las secciones 1 (Vigilancia) y 2 (Camión y conductor) y rehace las secciones 3 y 4 para el tipo nuevo. Si las secciones 3 o 4 tienen algo digitado, antes pide confirmación: «Se borrará lo digitado en Registro de operación y Pesaje. ¿Cambiar a {tipo}?». <br>• Con el registro guardado: deshabilitado con el tooltip de D2. <br>• En una duplicada (D13): no se muestra | Pedido; D2 |
| D10 | **Encabezado del registro:** la etiqueta del tipo (D8) va junto a la placa; «Duplicar entrada» sigue donde está y solo en Entrada (`AQ/` D7) | Pedido; `DIS/` Formulario |

### 1.3 Cómo se resuelve el tipo en el registro

| # | Decisión | Fuente |
| --- | --- | --- |
| D11 | **Ruta.** «Atender» con un tipo abre `/operations/weighbridge/process/{entryLogId}?tipo=ingreso|salida|solo-pesaje` (las consultas de la página ya están en español: `paso`, `servicio`, `entrada`, `duplicar`). El tipo de la página sale, en este orden: del servicio guardado (`servicio`), de la entrada (`entrada` → Entrada), de la duplicada (`duplicar=1` → Entrada) y de `tipo`. Si no hay ninguno (por ejemplo, un enlace directo o una recarga sin `tipo`), la página muestra el mismo menú (D6) en lugar de la sección 3, y al elegir actualiza `tipo` en la URL. Reemplaza la resolución por el motivo (`F/pages/operations/weighbridge/process/[entryLogId].vue:143-150`) | D3, D5; `P03/` D5 |
| D12 | **Cambiar el motivo ya no cambia el formulario.** La sección 1 lista los motivos con «Requiere pesaje», sin filtrar por categoría (`F/features/weighbridge/components/RegistrationVigilanceSection.vue:40`); salen la etiqueta de categoría (`:31`, `:42`) y el texto «Cambiar el motivo cambia el formulario según su categoría…» (`:159`). Reemplaza `P03/` D11 | D4 |
| D13 | **La duplicada pendiente es siempre una Entrada.** En la cola muestra «Entrada» (no «Por definir») y «Atender» la abre directo con `?duplicar=1`, sin menú, como hoy (`AQ/` D7). C-F03-53 deja de mirar la categoría del motivo: se agrega con el camión en planta y sin una operación guardada de Salida o de Solo pesaje. Si el camión tiene una, 400 «Solo se duplican las entradas de ingreso.» (el mensaje de hoy, `B/Wms.Application/Weighbridge/Common/Services/PendingDuplicateRules.cs:12`) | `AQ/` D10; D4 (`DEC-002`) |

### 1.4 Vigilancia, catálogo y Comercio Exterior

| # | Decisión | Fuente |
| --- | --- | --- |
| D14 | **Corrección de Vigilancia por Báscula** (C-F01-07 / C-F03-17, `B/Wms.Application/Logistics/EntryLogs/Commands/CorrectEntryLog/EntryLogCorrector.cs:99-115`). Con un registro de báscula guardado, el motivo se puede cambiar por otro que requiera pesaje, sin mirar categoría: el tipo ya no depende de él. Si el motivo nuevo no requiere pesaje, 409 «El camión {placa} ya tiene un registro de báscula: elija un motivo que requiera pesaje.» (mensaje nuevo; reemplaza el de la misma categoría). «Hay registro de báscula» pasa a ser: un ciclo no anulado, o una operación de báscula guardada (`hasRecord` con un motivo que requiere pesaje), en lugar de `Category is not null` (`:106`). La regla de la operación de bodega sin registro de báscula (WMS-5, `:117-118`) no cambia | `P01/` D13; D1, D4 |
| D15 | **Catálogo de motivos** (P-TR-04, `/admin/entry-reasons`): sale la columna, el filtro, el orden y el campo «Categoría» del listado y del modal, con su regla (`F/features/entries/contracts/entry-reason.ts:7-33`) y `F/features/entries/utils/entry-reason-category.ts`, que se borra si nadie más lo usa (trampa 7). En el backend, C-F01-01 a C-F01-05 pierden `category` en la petición, la respuesta, el filtro y `sortField`, y salen los mensajes «Elija la categoría del motivo…» y el de categoría no permitida | D4; `P01/` D12 |
| D16 | **Edición del ingreso por CE** (F05): el selector de motivo lista los motivos con «Requiere pesaje» (`F/features/foreign-trade/components/EntryEditForm.vue:94` filtra hoy por `category === "Entry"`). C-F01-93 / C-F03-13 pierden `entryReasonCategory` (`B/Wms.Application/Weighbridge/Queries/GetEntryForEdit/EntryForEditDto.cs:22`; `F/features/weighbridge/contracts/entry-edit.ts:17`) | D4 (`DEC-002`) |

### 1.5 Cola (P-BAS-01)

| # | Decisión | Fuente |
| --- | --- | --- |
| D17 | **Columnas** (`F/pages/operations/weighbridge/index.vue:61-70`). Salen «Cliente» (`:65`) y «Conductor» (`:66`). «Mercancía» suma un filtro de texto sobre lo que muestra (producto y embalaje; «Duplicada pendiente» en esa fila). «Documento» suma un filtro de texto y muestra el tipo y el número («Carta porte · CP-5678»; solo el número si no hay tipo). Columna nueva **«Tipo de operación»** entre «Placa» y «Estado», con la etiqueta de D8 y orden. Las demás columnas, el filtro de «Placa», las pestañas de estado y los pesos no cambian. La tabla sigue en modo `client` (`AUI/` D9) | Pedido; `P03/` D24 |
| D18 | **Contrato de la cola** (C-F03-21, `B/Wms.Application/Weighbridge/Common/Dtos/WeighbridgeQueueItemDto.cs`): `category` es nula en las filas «Sin iniciar» (hoy sale del motivo, `GetWeighbridgeQueueHandler.cs:80` y `:158-162`) y vale `Entry` en la duplicada pendiente (D13); se agrega `documentType` (texto: el nombre del tipo de documento, o nulo). `customerName` y `driverName` se conservan en la respuesta (los usa el panel de la cola) | D4, D13, D17 |
| D19 | **Acción por fila:** «Atender» (primario, con chevron, `aria-haspopup="menu"`) en «Sin iniciar» que no son duplicadas; «Atender» directo en la duplicada pendiente (D13); «Continuar» (`severity="secondary"` `outlined`) en los iniciados. El panel de la cola de la página del registro (`F/features/weighbridge/components/WeighbridgeQueuePanel.vue:126`) hace lo mismo: el menú en los «Sin iniciar» | D5, D13 (`DEC-002`: es la misma cola) |

### 1.6 Backend

| # | Decisión | Fuente |
| --- | --- | --- |
| D20 | **El enum se queda con su uso real.** `EntryReasonCategory` pasa a llamarse `WeighbridgeCategory` (mismos valores, `Entry`, `Exit` y `WeighingOnly`, y mismo JSON), porque ya no pertenece al motivo (trampa 9, nombres engañosos). `EntryReason.CategoryLabel` pasa a una utilidad de `WeighbridgeCategory`. Salen de `EntryReason` (`B/Wms.Domain/Entities/Logistics/EntryReason.cs`) la propiedad, `EnsureCategory` y sus dos mensajes; de los comandos y validadores de alta y edición, el campo; de `EntryReasonDto`, `GetAllEntryReasons` (columna, filtro y orden) y `GetEntryReasonsList`, el campo; y de `WeighbridgeTruckSnapshot` (`WeighbridgeEntryReader.cs:19`, `:123`), `EntryReasonCategory` | D4 |
| D21 | **Lo que no cambia:** los comandos de inicio y registro (`storage/initiate`, `storage/register`, `output/initiate` y el de solo báscula) no miran la categoría del motivo (comprobado con grep en la base: ninguna referencia); el tipo de los iniciados, el historial, el detalle, el tiquete y los reportes salen del servicio. Si el ejecutor encuentra un comando que sí la mira, se detiene y pregunta | D4 |
| D22 | **Migración `RemoveEntryReasonCategory`:** quita la columna `category` de `entry_reasons` y la propiedad de la configuración (`B/Wms.Infrastructure/Persistence/Configurations/Logistics/EntryReasonConfiguration.cs:17`); la semilla (`B/Wms.Infrastructure/Persistence/SeedDataExtensions.cs:290-296`) deja de llevar `Category`. El importador del legacy no asigna categoría (comprobado: sin referencias en `B/Wms.Application/Administration/LegacyImport/`); la prueba que contaba «5 de los 7 motivos con categoría» se ajusta | D4; `P01/` §8, nota de la fase 6 |

---

## 2. Contrato

Cambios sobre endpoints que ya existen; ninguno nuevo, ninguno retirado.

| ID | Endpoint | Cambio |
| --- | --- | --- |
| C-F01-01 | `GET entry-reasons` | Sin `category` en la respuesta, en los filtros ni en `sortField` (D15) |
| C-F01-02 | `GET entry-reasons/list` | Sin `category` (D15) |
| C-F01-03 | `GET entry-reasons/{id}` | Sin `category` (D15) |
| C-F01-04, C-F01-05 | `POST entry-reasons`, `PATCH entry-reasons/{id}` | Sin `category` en la petición; salen sus dos mensajes de error (D15). Un `category` enviado se ignora |
| C-F01-07 / C-F03-17 | `PUT entry-logs/{id}/correction` | Regla del motivo con registro de báscula y mensaje nuevo (D14) |
| C-F01-93 / C-F03-13 | `GET weighbridge/entries/{entryId}` | Sin `entryReasonCategory` (D16) |
| C-F03-21 | La cola de Báscula (la ruta de hoy) | `category` nula en «Sin iniciar» y `Entry` en la duplicada pendiente; `documentType` nuevo (D18) |
| C-F03-53 | `POST …/pending-duplicates` (la ruta de hoy) | Regla sin categoría (D13); mismo mensaje |

**Esquemas Zod** (Zod 4):

```ts
// F/features/entries/contracts/entry-reason.ts — sale entryReasonCategorySchema y el campo category.
export const entryReasonSchema = z.object({
  id: z.uuid(),
  description: z.string(),
  requiresWeighing: z.boolean(),
  // …los demás campos de hoy, sin category
});
export const entryReasonListParamsSchema = z.object({
  sortField: z.enum(["description", "requiresWeighing"]).optional(),
  // …sin el filtro category
});

// F/features/weighbridge/contracts/queue.ts — category nullable (ya lo es) y documentType nuevo.
documentType: z.string().nullable(),

// F/features/weighbridge/contracts/entry-edit.ts — sale entryReasonCategory.
```

El ejecutor confirma los nombres exactos de los esquemas de hoy con grep y cambia solo lo de arriba.

---

## 3. Archivos que se tocan

**Backend** (`B/`): `Wms.Domain/Entities/Logistics/EntryReason.cs` y el enum (renombrado, D20); `Wms.Application/Logistics/EntryReasons/` (comandos, validadores y consultas); `Wms.Application/Logistics/Common/Dtos/EntryReasonDto.cs`; `Wms.Application/Logistics/EntryLogs/Commands/CorrectEntryLog/EntryLogCorrector.cs` (D14); `Wms.Application/Weighbridge/Common/Services/WeighbridgeEntryReader.cs`, `PendingDuplicateRules.cs` y `WeighbridgeEntryView.cs`; `Wms.Application/Weighbridge/Commands/PendingDuplicates/PendingDuplicatesHandlers.cs`; `Wms.Application/Weighbridge/Queries/GetWeighbridgeQueue/GetWeighbridgeQueueHandler.cs` y `Common/Dtos/WeighbridgeQueueItemDto.cs` (D18); `Wms.Application/Weighbridge/Queries/GetEntryForEdit/` (D16); `Wms.Infrastructure/Persistence/Configurations/Logistics/EntryReasonConfiguration.cs`, `SeedDataExtensions.cs` y la migración nueva; y los usos del enum renombrado (unos 40 archivos, en su mayoría de Báscula). Pruebas: los *helpers* que crean motivos con categoría, las de `EntryReason`, `EntryLogCorrector`, `PendingDuplicateRules`, la cola y la importación de ensayo.

**Frontend** (`F/`): `features/entries/contracts/entry-reason.ts`, `features/entries/utils/entry-reason-category.ts` (se borra), `pages/admin/entry-reasons/index.vue` (D15); `features/weighbridge/contracts/queue.ts` y `entry-edit.ts`; `features/weighbridge/components/WeighbridgeOperationTypeMenu.vue` y `WeighbridgeOperationTypeTag.vue` (nuevos), `WeighbridgeProcessHeader.vue` (D9, D10), `WeighbridgeQueuePanel.vue` (D19), `RegistrationVigilanceSection.vue` (D12); `features/weighbridge/utils/queue-display.ts` (D5, D11); `pages/operations/weighbridge/index.vue` (D17, D19) y `pages/operations/weighbridge/process/[entryLogId].vue` (D11); `features/foreign-trade/components/EntryEditForm.vue` (D16); la galería `pages/dev/components.vue` (el menú y la etiqueta). Pruebas (`FT/`): `fixtures/foreign-trade/catalog.mock.ts`, `fixtures/weighbridge/views.ts` y las de cada componente tocado.

**Docs** (`D/`): este plan, la matriz, `qa/casos-qa2-f03-bascula-2026-11-24.md` (los casos de §6 al final) y los cambios de §10 con el «sí» del usuario.

---

## 4. Esquema y migración

| Migración | Contenido esperado |
| --- | --- |
| `RemoveEntryReasonCategory` | `DropColumn` de `category` en `entry_reasons`; los `UpdateData` de la semilla que EF genere al quitar `Category` de los motivos sembrados. Nada más: si EF genera otro cambio, el ejecutor se detiene y pregunta |

La base local se actualiza con `dotnet ef database update`. Staging no se toca: se recrea en el despliegue final (M25).

---

## 5. Fases

| Fase | Repo | Contenido | Criterio de salida | Estado |
| --- | --- | --- | --- | --- |
| 1 | BE | D4, D13, D14, D15 (backend), D16 (backend), D18, D20 a D22; migración | Compuertas BE de §7; QA-TIO-001 a 006 en PASA (API) | Pendiente |
| 2 | FE | Contratos sin categoría; catálogo de motivos (D15); sección 1 del registro (D12); edición del ingreso de CE (D16); menú y etiqueta nuevos (D6, D8) en la galería; la página del registro con el tipo de D11, la etiqueta y «Cambiar tipo» en el encabezado (D9, D10) | Compuertas FE; QA-TIO-007 a 012 en PASA en el navegador | Pendiente |
| 3 | FE y docs | Cola: columnas (D17), acción por fila y menú que se abre hacia arriba (D19), duplicada pendiente (D13); panel de la cola; casos al archivo de QA; matriz; fusión de `f2/f03-tipo-operacion` en `fase-2` en los dos repos | Compuertas FE; QA-TIO-013 a 020 en PASA; fusiones con push | Pendiente |

---

## 6. Casos QA

| ID | Regla | Precondición | Pasos | Resultado esperado | Verificación |
| --- | --- | --- | --- | --- | --- |
| QA-TIO-001 | D15 | Admin | `GET entry-reasons`, `GET entry-reasons/list` y `GET entry-reasons/{id}` | Sin `category`; `sortField=category` responde como cualquier campo fuera de la lista blanca (C-F01-00) | API |
| QA-TIO-002 | D15 | Admin | `POST entry-reasons` con «Requiere pesaje» y sin categoría | 201; el motivo nace sin categoría (no existe) | API |
| QA-TIO-003 | D18 | Un camión de Vigilancia sin iniciar con motivo «Descargue…» | `GET` de la cola | Su fila con `category` nula y `documentType` nulo | API |
| QA-TIO-004 | D14 | Un camión con una Entrada guardada | Corregir el motivo a «Cargue…» (requiere pesaje); luego a «Solo bodega» | El primero, 200; el segundo, 409 «El camión {placa} ya tiene un registro de báscula: elija un motivo que requiera pesaje.» | API |
| QA-TIO-005 | D13 | Un camión sin iniciar; otro con una Salida guardada | C-F03-53 en cada uno | El primero suma la pendiente y su fila sale con `category` `Entry`; el segundo, 400 «Solo se duplican las entradas de ingreso.» | API |
| QA-TIO-006 | D22 | Base local migrada | `has-pending-model-changes`; consultar `entry_reasons` | Limpio; sin columna `category` | API y base |
| QA-TIO-007 | D15 | Admin, `/admin/entry-reasons` | Ver la tabla y abrir «Nuevo motivo» | Sin columna, filtro ni campo «Categoría»; se crea y se edita sin ella | Pantalla |
| QA-TIO-008 | D11, D6 | Báscula; un camión sin iniciar | Abrir `/operations/weighbridge/process/{id}` sin `tipo` | La página muestra el menú en lugar de la sección 3; al elegir «Salida», se arma la sección 3 de salida y la URL lleva `?tipo=salida` | Pantalla |
| QA-TIO-009 | D9, D2 | Registro abierto como Entrada, sin guardar, con datos en la sección 3 | «Cambiar tipo» → «Solo pesaje» | Pide la confirmación de D9; al aceptar, conserva las secciones 1 y 2 y arma las de solo pesaje | Pantalla |
| QA-TIO-010 | D2 | Registro de Entrada guardado | Ver «Cambiar tipo» | Deshabilitado, con el tooltip de D2 | Pantalla |
| QA-TIO-011 | D12 | Registro de un camión sin iniciar | Editar la sección 1 y cambiar el motivo | Lista solo motivos con «Requiere pesaje»; el formulario no cambia de tipo | Pantalla |
| QA-TIO-012 | D16 | CE, edición del ingreso (P-CE-03) | Abrir el selector de motivo | Lista los motivos con «Requiere pesaje» | Pantalla |
| QA-TIO-013 | D17 | Báscula, `/operations/weighbridge` con camiones de varios estados | Ver la tabla | Sin «Cliente» ni «Conductor»; «Tipo de operación» entre «Placa» y «Estado», con «Por definir» en los sin iniciar; «Documento» con tipo y número | Pantalla |
| QA-TIO-014 | D17 | La misma cola | Filtrar «Mercancía» por un producto y «Documento» por un número | Solo las filas que contienen el texto, sin tildes ni mayúsculas | Pantalla |
| QA-TIO-015 | D6, D19 | Un camión sin iniciar | «Atender» | Se abre el menú igual al diseño (título, tres opciones con icono, nombre, descripción, atajo y colores); al elegir «Entrada» abre el registro de ingreso con `?tipo=ingreso` | Pantalla, con captura junto al diseño |
| QA-TIO-016 | D6 | Un camión sin iniciar en una de las últimas filas | «Atender» | El menú se abre hacia arriba, entero a la vista | Pantalla |
| QA-TIO-017 | D6 | Menú abierto | Pulsar S; abrir otra vez y pulsar Escape | S abre el registro de salida; Escape cierra y el foco vuelve a «Atender» | Pantalla |
| QA-TIO-018 | D5, D3 | Un camión «Por cobrar»; otro sin iniciar que se atendió y se dejó sin guardar | Ver sus filas | El primero con «Continuar» y su tipo, que abre en Cobro sin menú; el segundo vuelve a «Sin iniciar · Por definir» | Pantalla |
| QA-TIO-019 | D13 | «Duplicar entrada» en un registro de ingreso | Ver la fila de la duplicada y «Atender» | «Entrada» con la «D»; abre directo con `?duplicar=1`, sin menú | Pantalla |
| QA-TIO-020 | D19 | Página del registro con el panel de la cola | «Atender» en una fila sin iniciar del panel | Se abre el mismo menú | Pantalla |

---

## 7. Compuertas de cada fase

- **BE (fase 1):** `dotnet build Wms.sln` sin errores; `dotnet test Wms.Tests` (base 2547) y `dotnet test Wms.IntegrationTests` (base 916) en verde, con las cifras antes y después; `dotnet ef migrations has-pending-model-changes` limpio; `git grep -n "EntryReasonCategory"` sin resultados fuera de `Migrations/`.
- **FE (fases 2 y 3):** `yarn build` con código 0; `yarn test` en verde (base 913); `yarn lint` con 118 errores o menos y ninguno en archivos nuevos o tocados; las guardias de `FT/unit/guards/` en verde; `git grep -n "entryReasonCategory\|ENTRY_REASON_CATEGORY"` sin resultados.
- Las cifras de base son las del último cierre (ajustes de la QA de F06); el ejecutor las confirma al empezar y reporta antes y después.
- Capturas de los casos de la fase, y en QA-TIO-015 una junto a `DIS/` Cola.

---

## 8. Commits

| Fase | Repo | Mensaje |
| --- | --- | --- |
| 1 | BE | `feat(bascula): el tipo de operación ya no sale del motivo; se retira la categoría del motivo de ingreso (DEC-080, F03)` |
| 2 | FE | `feat(bascula): tipo de operación elegido en el registro, con «Cambiar tipo» antes de guardar; motivos sin categoría (DEC-080, F03)` |
| 3 | FE | `feat(bascula): «Atender» elige el tipo en la cola; columnas de tipo, mercancía y documento (DEC-080, F03)` |
| Cada fase | docs | `docs(f03): fase N del tipo de operación en Báscula (sprint 11)` |

Fusiones: `f2/f03-tipo-operacion` en `fase-2`, con `--no-ff`, en BE y en FE, al cerrar la fase 3.

---

## 9. Riesgos

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R1 | Un paso más para el operario (PRF-002, meta de 30 s por camión) | El menú se maneja con una tecla (E, S o P) y abre con el foco en la primera opción (D6); PRF-002 se mide en el despliegue final |
| R2 | El renombre del enum toca unos 40 archivos | Renombre mecánico en la fase 1, con la compilación y las dos suites como red; sin cambiar valores ni JSON (D20) |
| R3 | Vigilancia elige un motivo que no requiere pesaje y el camión no llega a la cola | Es la regla de hoy (D1); se corrige desde Vigilancia o desde la sección 1 del registro |
| R4 | Un operario elige un tipo equivocado y guarda | Se anula el registro con motivo y se atiende de nuevo (D2), como cualquier registro equivocado (`P03/` D11, AF-23) |
| R5 | Otra sesión trabaja en el backend o el frontend (por ejemplo, los formatos PDF) | Un agente por repo (M10, §0.2): este plan espera su turno y va antes de F07 |
| R6 | Colores fijos del diseño en el tema oscuro | Variables del componente con variantes oscuras de contraste 4.5:1 (D6) |

---

## 10. Cambios al hub (con el «sí» del usuario)

1. `D/contexto/decisiones.md`, nueva al final: «**DEC-083 — Tipo de operación en Báscula** (2026-11-27). Pedido del usuario: el operario de Báscula elige el tipo de operación (Entrada, Salida o Solo pesaje) al atender un camión «Sin iniciar»; se elimina la categoría del motivo de ingreso. El motivo sigue obligatorio en Vigilancia y conserva «Requiere pesaje», que decide si el camión va a Báscula. El tipo se guarda con el registro y solo se cambia antes de guardarlo; después, se anula el registro y se atiende de nuevo. Reemplaza la parte de la categoría de AF-08 y M22. Plan: `planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-tipo-operacion-2026-11-27.md`.»
2. `D/contexto/decisiones.md`, `DEC-080`, al final: «*La categoría del motivo de AF-08 y M22 la reemplaza `DEC-083` (2026-11-27).*»
3. `D/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md` §1.2, fila M22, al final de la decisión: «**Reemplazada por `DEC-083`** (2026-11-27): el motivo ya no tiene categoría.»

---

## 11. Prompt para ejecutarlo

Una sesión nueva en `code_workspace/` por fase, con este texto y el número de la fase:

```text
Eres el agente que ejecuta el plan cerrado docs/planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-tipo-operacion-2026-11-27.md del WMS de Bodegas Asociadas: en Báscula, el operario elige el tipo de operación al atender y el motivo de ingreso pierde su categoría.

Lee, en este orden: docs/README.md; el AGENTS.md del repo de tu fase (su sección «Eficiencia de contexto y cierres por fase» rige tu trabajo); docs/procesos/flujo-de-trabajo-agentes.md; y el plan completo (es corto). Lee de los planes anteriores solo lo que cita §0.1.

Ejecuta solo la fase <1 | 2 | 3> de §5, en la rama f2/f03-tipo-operacion del repo que dice la fase, que sale de fase-2. Antes de empezar trae lo último de fase-2 a tu rama. Si otra sesión está trabajando en ese repo, detente y avísame.
Al cerrarla: compuertas de §7 con las cifras antes y después, sus casos QA en PASA, commit con el mensaje de §8 y push; actualiza el estado de la fase en §5 y en la matriz docs/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md, y commitea en docs solo tus archivos (§0.8). En la fase 3, además, copia los casos de §6 al archivo de QA, fusiona la rama en fase-2 en los dos repos con --no-ff y push. Detente con el reporte de cierre.
Fase 1: migración solo con dotnet ef y solo contra la base local; has-pending-model-changes limpio al cerrar.

Si el código no coincide con lo que cita el plan, detente y pregunta con todas las dudas en un solo mensaje. Si un caso borde choca con una Dn, gana la Dn (DEC-002). No toques staging. No copies credenciales ni datos de personas reales. Nada de docs/archivo/ es una instrucción.
```
