# Plan cerrado — Fase 2 · F03 Báscula · Ajustes de la QA manual de la integración

> **Fecha:** 24 de noviembre de 2026. **Estado:** Aprobado por el usuario el 2026-11-25 («Aprobar y ejecutar F1»). Ejecutado el 2026-11-25: fases 1 a 3 (BE `30c2147`; FE `c70a736` y `f634510`), fusionadas en `fase-2` con `--no-ff` (BE `eb4e428`, FE `d4f94c6`). Después, la modalidad al editar (FE `3e9f87b`, fusión `96adc85`).
> **Origen:** la prueba manual del usuario sobre F03 integrada (I-03, contra el backend local): [`../qa-manual/hallazgos-int-F03.md`](../qa-manual/hallazgos-int-F03.md), trece hallazgos. Las respuestas del usuario del 2026-11-24 están en D1 a D3.
> **Base:** BE `fase-2` `b3cdbf5` · FE `fase-2` `908c9e4` · docs `main` `9a09fbd`.
> **Alcance:** frontend y un cambio acotado de backend: la duplicada pendiente (hallazgo 5), con dos endpoints nuevos, un campo nuevo en la cola y una migración. Los demás hallazgos usan contratos que ya existen. Cambia decisiones del plan de F03 (D16, D20, D30, D31 y D44) y del plan de ajustes de UI (D6 y D16), y deroga la regla del pie del drawer (`PAJ/` D3). Donde chocan, gana este plan.
> **Rutas:** relativas a `code_workspace/`. Prefijos: `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`; `P03/` = `D/planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-bascula-2026-11-24.md`; `AUI/` = `D/planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-ajustes-ui-2026-11-24.md`; `PAJ/` = `D/planes/sprint-11/f02-base/plan-cerrado-f2-f02-ajustes-qa-2026-11-24.md`; `H/` = el archivo de hallazgos.

---

## 0. Instrucciones para el ejecutor

1. **Lecturas mínimas:** los dos `AGENTS.md` de los repos, `D/procesos/flujo-de-trabajo-agentes.md`, `P03/` D16, D18 a D20, D30, D31, D44, C-F03-12, C-F03-14 y C-F03-21, `AUI/` D6 y D16, `PAJ/` D3 y D5, `H/` y este plan completo.
2. **Ramas y git:** `f2/f03-ajustes-qa` en BE y en FE, desde `fase-2`. Commit y push al cerrar cada fase, con el mensaje de §7. Al cerrar la fase 3, fusión en `fase-2` con `--no-ff` en los dos repos y push. Sin `push --force`. Para borrar, `rm`.
3. **Una fase por turno** (`AGENTS.md`): al cerrar cada una, compuertas, commit, estado en este plan y en la matriz, y reporte.
4. **Líneas citadas:** son de la base. Confírmalas con grep; si el código no coincide, pregunta en un solo mensaje.
5. **Migración:** solo con `dotnet ef … --project Wms.Infrastructure --startup-project Wms.Api`, aplicada solo en la base local, en el mismo commit que el código.
6. **Verificación:** `yarn dev` sin sesión simulada contra el API local (`.claude/launch.json`: `wms-api` y `wms-frontend`), con Administrador y Báscula. Capturas en `D/planes/sprint-11/f03-bascula/evidencias/ajq-*`.

---

## 1. Decisiones

### 1.1 Respuestas del usuario (2026-11-24)

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **La duplicada pendiente se guarda en el backend** (hallazgo 5). Detalle en D8 a D10 | Usuario: «En el backend (Recomendada)» |
| D2 | **Se conserva la regla del menú de acciones de fila** (`AUI/` D6: más de tres acciones posibles, todas al menú). Lo que cambia es el botón «⋮», que toma el estilo de las tablas de Configuración: `severity="secondary"`, `outlined`, `size="small"`, sin `text` ni `rounded` (hoy, `F/components/app/AppRowActions.vue`, el botón del menú) | Usuario: «Se conserva la regla, lo que necesito es que el botón tome el estilo con borde de Configuración» |
| D3 | **Lista de pesajes en el detalle** (hallazgo 7). Detalle en D14 | Usuario: «Lista de pesajes (Recomendada)» |

### 1.2 Registro del camión (hallazgos 2 a 6, 8 y 13)

| # | Decisión | Fuente |
| --- | --- | --- |
| D4 | **El número de documento nunca toma el texto del depósito** (hallazgo 2). <br>• **Causa:** `AutoComplete` muestra en el campo el `option-label` de la opción elegida, que hoy arma «número · depósito · cliente» (`F/features/weighbridge/components/RegistrationEntrySection.vue:103` y `:164`). Si el número elegido es igual al que ya estaba escrito, el modelo no cambia y el campo se queda con ese texto. <br>• **Cambio:** `option-label="documentNumber"`. La lista sigue con su plantilla de dos líneas (`:174-181`) | `H/` 2 |
| D5 | **El depósito vuelve a las tarjetas de antes, con placas** (hallazgo 3; `P03/` D44 y `DEC-057` D1). <br>• **Tarjetas:** el selector `Select` (`RegistrationEntrySection.vue:197-216`) se cambia por un grupo de tarjetas con `role="radiogroup"`, como el `DocumentMatchBanner.vue` retirado en I-03 (su última versión está en FE `cd0c2b5^`). Cada depósito abierto muestra número, estado, camiones, cliente, importador o exportador, agencia, transportadoras, fecha del documento y **placas** (`plates` de C-F03-52, que ya viene en el contrato). <br>• **Otros casos:** al final, la tarjeta «Es otro documento: crear depósito nuevo». Los depósitos cerrados o migrados, si llegan, salen en gris y no se eligen. <br>• **Sin preselección:** hoy se elige solo el primero (`:88-90`), lo que choca con `P03/` D44 («la elección del depósito sigue `DEC-057` D1»). Gana la `Dn` (`DEC-002`): con depósitos abiertos, el operario elige, y Guardar muestra el error «Elija el depósito del camión o «Es otro documento».» hasta que lo haga. <br>• **Error de «Es otro documento»:** la elección se guarda en el modelo con un valor propio (`NEW_DEPOSIT = "new"`), no con `null`, que el formulario no distingue de «sin elegir». Al armar C-F03-01 y C-F03-14, `"new"` viaja como `targetWarehouseStorageId: null`. La causa exacta del regreso al valor anterior se confirma en el navegador al ejecutar; el cambio la cubre en los dos casos posibles (el `null` del `Select` y la preselección) | `H/` 3; `P03/` D44; `DEC-057` D1 |
| D6 | **Manifiesto siempre visible en el ingreso; obligatorio solo con carta porte** (hallazgo 4; ajusta `P03/` D16). <br>• **Campos:** «N.º de manifiesto» (`RegistrationEntrySection.vue:184`) y «P. manifiesto» (`F/features/weighbridge/utils/registration-weights.ts:49-50`, `weightFields`) se muestran con cualquier tipo de documento. Llevan el asterisco y la validación de hoy solo con carta porte (`F/features/weighbridge/utils/registration-form.ts`, `errors.manifestWeight`). <br>• **Datos:** `buildStorageRegister` y `buildEntryCorrection` envían número y peso siempre, o `null` si están vacíos (hoy, solo con carta porte). El P. manifiesto precarga P. mercancía con cualquier tipo. <br>• **Backend sin cambios:** ya guarda el manifiesto con otro tipo si viene (`B/Wms.Application/Weighbridge/Commands/Storage/Initiate/InitiateStorageWeighingHandler.cs:112`, `F01` D22) | `H/` 4; `F01` D22 |
| D7 | **«Duplicar entrada» crea la duplicada pendiente y deja al operario en el registro** (hallazgo 5; reemplaza `P03/` D20 en su forma). <br>• **Botón:** sigue en el encabezado, solo en ingresos y habilitado con las secciones 1 y 2 completas. Al pulsarlo, llama a C-F03-53, avisa «Se agregó una entrada duplicada de {placa} a la cola.» y **no navega**. Lo que el operario llenó no se pierde. <br>• **Cola y panel:** la duplicada pendiente es una fila «Sin iniciar» con la «D» (D9). «Atender» abre `process/{entryLogId}?duplicar=1`, que copia las secciones 1 y 2 como hoy. <br>• **Al guardar** la duplicada (C-F03-01), el backend descuenta una pendiente (D10). <br>• **«Descartar duplicada»:** en `?duplicar=1`, un botón secundario en el encabezado llama a C-F03-54 y vuelve a la cola. <br>• **Deja de valer:** «Una duplicada sin guardar se pierde al salir» (AF-48 en `P03/` D20). La duplicada abierta y sin guardar sigue sin dejar rastro, pero la pendiente sigue en la cola hasta que se guarde o se descarte | `H/` 5; D1 |
| D8 | **Cerrar sin repesaje desde el paso Repesaje** (hallazgos 6 y 13; `P03/` D18). <br>• **Botón:** en `?paso=repesaje`, «Cerrar sin repesaje» (secundario, con borde, `small`) en el encabezado, junto a «Volver a la cola». Va en ingresos, salidas y solo báscula, siempre que la entrada esté «Por repesar» con ciclo. <br>• **Confirmación:** «El ciclo se cierra con el primer pesaje ({peso} kg) y sale de la cola. Si después llega el repesaje, se registra con «Repesar» desde el historial.» <br>• **Guardado:** C-F03-12 con `required: false` (ya existe y lo usa el interruptor del encabezado). Cierra el ciclo con el primer peso (`B/Wms.Application/Weighbridge/Common/Services/SecondWeighingSwitch.cs`). Invalida `weighbridgeKeys.all` y pasa al paso Tiquete, como tras un repesaje. <br>• **Error:** se muestra el 400 del backend, por ejemplo el de la guía de importación de una salida. <br>• **Regla pura:** `canCloseWithoutReweigh(state, weighbridgeCycleId)` en `F/features/weighbridge/utils/entry-detail.ts`: estado `PendingReweigh` y ciclo presente | `H/` 6, 13; `P03/` D18 |
| D9 | **Editar un ciclo con repesaje no pide la tara** (hallazgo 8). <br>• **Causa:** C-F03-14 exige `tareWeight` cuando el ciclo tiene el pesaje de tara (`B/Wms.Application/Weighbridge/Common/Services/EntryCorrectionService.cs:351-354`), y el frontend siempre envía `null` (`F/features/weighbridge/utils/registration-form.ts:184`). <br>• **Datos:** con `tareIsReal` en la lectura de la entrada (C-F03-13, `F/features/foreign-trade/contracts/deposit-entry.ts:26-27`), el formulario guarda la tara real y la envía en `tareWeight`. <br>• **Formulario:** «P. Vehículo / Tara» muestra esa tara real, de solo lectura, con la leyenda «Repesaje», en lugar de la calculada. Se corrige con «Modificar pesaje» de `cycles/[id]`. <br>• **Mercancía:** al cambiar el indicador, P. mercancía se recalcula como indicador − tara real, y se puede cambiar. Sin repesaje, todo sigue como `P03/` D16 | `H/` 8; `P03/` D16, D31 |

### 1.3 Backend de la duplicada pendiente (D1, D7)

| # | Decisión | Fuente |
| --- | --- | --- |
| D10 | **Contador de duplicadas pendientes en la entrada del camión.** <br>• **Modelo:** `EntryLog.PendingDuplicateEntries` (`int`, no nulo, `0` por defecto), con los métodos `AddPendingDuplicate()`, `RemovePendingDuplicate()` y `ConsumePendingDuplicate()`. La migración `AddEntryLogPendingDuplicateEntries` sale con `dotnet ef`. `EntryLog` ya es `IAuditable`: el cambio queda en `audit_logs` sin más. <br>• **Reglas puras** (`PendingDuplicateRules`, probadas en `Wms.Tests`): <br>  – se agrega solo con el camión en planta (sin salida) y un motivo de categoría ingreso; <br>  – se quita solo si hay alguna; <br>  – al registrar una entrada que resulta duplicada (`DuplicateEntryLookup.HasEarlierEntryAsync`, `InitiateStorageWeighingHandler.cs:196`), se consume una si hay, y nunca baja de cero. <br>Así la cuenta cuadra aunque la entrada original se guarde después de una duplicada. <br>• **Endpoints:** <br>  – C-F03-53 `POST weighbridge/entry-logs/{entryLogId}/pending-duplicates` agrega una; <br>  – C-F03-54 `DELETE weighbridge/entry-logs/{entryLogId}/pending-duplicates` quita una. <br>  Los dos con `ScaleAccess` y respuesta `{ entryLogId, pendingDuplicateEntries }`. Errores: 404 «La entrada del camión no existe.»; 400 «Solo se duplican las entradas de ingreso.»; 400 «El camión ya salió de la planta.»; 400 «La entrada no tiene duplicadas pendientes.». <br>• **Cola (C-F03-21, modificado):** el ítem suma `isPendingDuplicate` (`bool`). Por cada pendiente, el camión suma una fila `NotStarted` con `isDuplicateEntry` e `isPendingDuplicate` en `true`, con placa, conductor, motivo y espera del camión, después de sus entradas. `WeighbridgeQueueFilters.IsPendingInWeighbridge` (`B/Wms.Application/Weighbridge/Queries/GetWeighbridgeQueue/WeighbridgeQueueFilters.cs:25-30`) también deja pasar un camión con pendientes, aunque sus entradas estén completas. <br>• **Salida del camión:** la cola solo lee camiones en planta (`IsOpenEntry`), así que las pendientes de un camión que salió no se ven. El contador no se limpia | D1; `H/` 5 |
| D11 | **Frontend de la cola** (C-F03-21). `queueItemSchema` suma `isPendingDuplicate`. `queueRowKey` agrega el orden de la pendiente, para que dos pendientes del mismo camión tengan claves distintas. `attendQuery` lleva una pendiente a `duplicar=1`. La placa lleva la «D» (`VehiclePlateTag`) y la fila cuenta en «Sin iniciar». En el panel de la cola, la pendiente se ve como cualquier fila, con la «D» | D7 |

### 1.4 Historial, detalle y drawers (hallazgos 7, 9 a 12)

| # | Decisión | Fuente |
| --- | --- | --- |
| D12 | **Acciones del drawer: siempre en el menú del encabezado** (hallazgo 9; deroga `PAJ/` D3 y ajusta `PAJ/` D5 y `P03/` D30). <br>• **Regla:** con una o más acciones, todas van al menú «Acciones» (⋮) del encabezado, y el drawer no lleva pie. Sin acciones, no hay botón de menú. Vale para todos los drawers de la app. <br>• **Dónde cambia:** todos usan `F/components/app/AppDetailDrawer.vue` (`MAX_FOOTER_ACTIONS` y `footerActions`, `:49-50` y `:150-166`), así que el cambio es uno solo. `TruckDetailSidebar` (trazabilidad) no tiene acciones. <br>• **Afectados:** Terceros, Servicios, Conductores y la Báscula, que hoy usan el pie. Usuarios ya usa el menú y Auditoría no tiene acciones. La galería `F/pages/dev/components.vue` muestra el drawer con una y con tres acciones | `H/` 9 |
| D13 | **Acciones del drawer de Báscula** (hallazgos 10 y 11). <br>• **«Editar pesajes» sale de la sección** «2. Pesaje en báscula» (`F/features/weighbridge/components/WeighbridgeEntryDetail.vue:87-97`), y con él su prop `canEditWeights` y el evento `edit-weights`. <br>• **Menú del encabezado,** en este orden: «Editar», «Repesar», «Cerrar sin repesaje», «Imprimir tiquete» y «Anular pesaje» (en rojo). <br>• **«Editar»** se ve con `canEdit` o con `canEditWeights`. Abre lo de hoy: en un ingreso, el registro (`processEditRoute`, con `editWeights` si solo hay `canEditWeights`); en salida y solo báscula, P-TR-12. <br>• **«Cerrar sin repesaje»** se ve con `canCloseWithoutReweigh` (D8). Confirma como en D8, llama a C-F03-12 e invalida `weighbridgeKeys.all`. <br>• **Dónde va:** `detailRecordActions` y `DETAIL_ACTION_META` (`F/features/weighbridge/utils/entry-detail.ts:31-47`) suman `edit` y `closeWithoutReweigh`, y `WeighbridgeEntryDialogs` suma la acción `closeWithoutReweigh`. <br>• **`cycles/[id]`** conserva su tarjeta «Correcciones» | `H/` 10, 11 |
| D14 | **«Pesajes del ciclo» en el detalle** (hallazgo 7; D3). En la sección 2, debajo de los cuatro pesos, una tabla pequeña (`DataTable` `size="small"`, `PAJ/` D5) con los `weighings[]` del contrato: <br>• «Pesaje» para la secuencia 0 y «Repesaje» para la 1; <br>• tipo (Bruto o Tara), peso y fecha y hora; <br>• si se corrigió, el peso original tachado y el motivo en un tooltip. <br>Sin pesajes, la tabla no se muestra. La arma una regla pura, `detailWeighingRows`, en `entry-detail.ts`. Se ve en el drawer y en `cycles/[id]` | `H/` 7; D3 |
| D15 | **«Cerrar sin repesaje» en las tablas del historial** (hallazgo 10). `WeighbridgeHistoryActions.vue` suma la acción después de «Repesar» (icono `pi pi-check-square`), visible con `canCloseWithoutReweigh(row.state, row.weighbridgeCycleId)`. Las tres páginas del historial la atienden como el drawer (D13). La tabla pasa a seis acciones posibles y sigue en el menú (D2) | `H/` 10 |
| D16 | **«P. manifiesto» en «Pesos (kg)» de Historial › Entradas** (hallazgo 12; ajusta `AUI/` D8). Las líneas quedan en este orden: «P. bruto», «P. manifiesto», «P. mercancía» y «Tara». El dato es `manifestWeight` de C-F03-22, que ya viene. Salidas y Solo báscula no tienen manifiesto. El Excel no cambia | `H/` 12 |
| D17 | **Botón del menú de fila con borde** (hallazgo 12; D2). El cambio es en `AppRowActions.vue` y alcanza a los historiales de Báscula y a Vigilancia › Historial, que son las tablas que hoy usan el menú. Las demás tablas con `AppDataTable` ya usan botones de solo icono con borde (revisado en la base: las 16 de Configuración y Ajustes). <br>«Atender» de la cola conserva su etiqueta y su estilo (`AUI/` D9): es la única acción de la tabla y no es un botón de solo icono. Las tablas viejas que no usan `AppDataTable` toman la regla cuando su feature las rediseñe (`PAJ/` D6) | `H/` 12; D2 |

### 1.5 Menú (hallazgo 1)

| # | Decisión | Fuente |
| --- | --- | --- |
| D18 | **Báscula sin el grupo «Historial»** (ajusta `AUI/` D16 y `P03/` D43). `F/components/layout/menu-model.ts` queda así: <br>• Dashboard; <br>• Proceso de pesaje; <br>• Entradas (`/operations/weighbridge/history`); <br>• Salidas (`/operations/weighbridge/history/exits`); <br>• Solo báscula (`/operations/weighbridge/history/weighing-only`). <br>Las migas de pan de las tres páginas pasan a «Báscula › Entradas», «Báscula › Salidas» y «Báscula › Solo báscula» | `H/` 1 |

---

## 2. Contrato

| Id | Endpoint | Cambio | Permiso | Pantalla |
| --- | --- | --- | --- | --- |
| C-F03-21 | `GET weighbridge/queue` | modificado: `isPendingDuplicate` y las filas de las duplicadas pendientes (D10) | `ScaleAccess` | P-BAS-01 y panel |
| C-F03-53 | `POST weighbridge/entry-logs/{entryLogId}/pending-duplicates` | nuevo (D10) | `ScaleAccess` | P-BAS-02 |
| C-F03-54 | `DELETE weighbridge/entry-logs/{entryLogId}/pending-duplicates` | nuevo (D10) | `ScaleAccess` | P-BAS-02 (`?duplicar=1`) |

Esquema del frontend (`F/features/weighbridge/contracts/`):

```ts
// queue.ts — queueItemSchema suma:
isPendingDuplicate: z.boolean(),
// registration.ts — C-F03-53 y C-F03-54:
export const pendingDuplicatesResultSchema = z.object({
  entryLogId: guidSchema,
  pendingDuplicateEntries: z.int().min(0),
});
```

Al cerrar, la ficha de estos tres contratos se copia a `P03/` §2, con la nota «sumado por el plan de ajustes de la QA manual».

---

## 3. Archivos que se tocan

| Archivo | Fase | Cambio |
| --- | --- | --- |
| `B/Wms.Domain/Entities/Logistics/EntryLog.cs`; su configuración EF; migración nueva | 1 | D10 |
| `B/Wms.Application/Weighbridge/Common/Services/PendingDuplicateRules.cs` (nuevo) | 1 | D10 |
| `B/Wms.Application/Weighbridge/Commands/PendingDuplicates/` (nuevo: agregar y quitar, con sus validadores) y su controlador | 1 | C-F03-53, C-F03-54 |
| `B/Wms.Application/Weighbridge/Commands/Storage/Initiate/InitiateStorageWeighingHandler.cs` | 1 | Consume una pendiente (D10) |
| `B/Wms.Application/Weighbridge/Queries/GetWeighbridgeQueue/` (handler y filtros); `B/Wms.Application/Weighbridge/Common/Dtos/WeighbridgeQueueItemDto.cs` | 1 | C-F03-21 |
| `B/Wms.Tests/…/PendingDuplicateRulesTests.cs` (nuevo); `B/Wms.IntegrationTests/Weighbridge/PendingDuplicatesTests.cs` (nuevo) y la prueba de la cola | 1 | §5 |
| `F/features/weighbridge/components/RegistrationEntrySection.vue`; `F/features/weighbridge/utils/registration-form.ts`; `registration-weights.ts`; `RegistrationWeights.vue` | 2 | D4 a D6, D9 |
| `F/features/weighbridge/components/WeighbridgeProcessHeader.vue`; `F/pages/operations/weighbridge/process/[entryLogId].vue` | 2 | D7, D8 |
| `F/features/weighbridge/contracts/queue.ts`, `registration.ts`; `services/registration.source.ts`, `registration.http.ts`; `composables/weighbridge.queries.ts`; `utils/queue-display.ts`; `WeighbridgeQueuePanel.vue`; `F/pages/operations/weighbridge/index.vue` | 2 | D7, D11 |
| `F/features/weighbridge/utils/entry-detail.ts` | 2 y 3 | `canCloseWithoutReweigh` (fase 2); `detailRecordActions`, `DETAIL_ACTION_META` y `detailWeighingRows` (fase 3) |
| `F/components/app/AppDetailDrawer.vue`; `F/pages/dev/components.vue` | 3 | D12 |
| `F/features/weighbridge/components/WeighbridgeEntryDetail.vue`, `WeighbridgeEntryDialogs.vue`; `composables/useHistoryDrawer.ts`; `F/pages/operations/weighbridge/cycles/[id].vue` | 3 | D13, D14 |
| `F/features/weighbridge/components/WeighbridgeHistoryActions.vue`; `F/pages/operations/weighbridge/history/index.vue`, `exits.vue`, `weighing-only.vue`; `utils/history-display.ts` | 3 | D15, D16, D18 (migas) |
| `F/components/app/AppRowActions.vue` | 3 | D17 |
| `F/components/layout/menu-model.ts` | 3 | D18 |
| Pruebas de `FT/` de cada archivo tocado (§5) | 2 y 3 | §5 |
| `D/contexto/convenciones-tecnicas.md` §3 («Drawer de detalle» y «Tablas de listado»); notas «ajustado por este plan» en `P03/` (D16, D20, D30, D31, D43, D44, §2) y en `AUI/` (D6, D8, D16); `PAJ/` D3 (derogada) y D5; `H/` (decisión por punto); `D/planes/README.md`; seguimiento §3; la matriz | 3 (cierre) | Estado y convención |

---

## 4. Fases

| Fase | Repo | Contenido | Criterio de salida | Estado |
| --- | --- | --- | --- | --- |
| 1 | BE | Duplicada pendiente: modelo, migración, reglas, C-F03-53, C-F03-54, C-F03-21 y el consumo al registrar (D10) | Compuertas BE de §6; QA-AJQ3-001 a 004 en PASA (API) | Hecha el 2026-11-25 (BE `30c2147`). QA-AJQ3-001 a 004 en PASA contra el API local, con Báscula: DUP123 llegó a dos pendientes y la cola mostró dos filas «Sin iniciar» con `isPendingDuplicate`; al quitar, bajó a una y luego a cero, con el 400 después; GTY567 (solo báscula) y ABC123 (salida) dieron 400 «Solo se duplican las entradas de ingreso.»; registrar la duplicada de DUP123 salió con `isDuplicateEntry` y cobro en $0, y consumió la pendiente. Esa duplicada quedó en la base local, «Por pesar». <br>• **Migración:** `20261125050208_AddEntryLogPendingDuplicateEntries`, una columna `pending_duplicate_entries` (`integer`, `0` por defecto), aplicada solo en la base local. <br>• **Compuertas:** build sin errores; `Wms.Tests` de 2158 a 2166; `Wms.IntegrationTests` de 762 a 766 pruebas, con 761 en verde y 5 en rojo; `has-pending-model-changes` limpio. <br>• **Las 5 en rojo no son de esta fase:** fallan igual en `fase-2` `b3cdbf5` sin estos cambios, corridas en un worktree aparte. Dependen de la hora: la suite corrió a las 00:10 de Colombia, y sus camiones de prueba entran «hace 30 minutos», o sea, el día anterior. Son `TraceabilityDiscardedServiceTests` (3), `SingleWeighingManifestNetTests.InspectionSingleWeighing_WithManifest_NetIsTheManifest` y `DraftCorrectionRecalculationTests.ReturnedDraft_CurrencyToUsd_AssignsWeeklyRateAndRecalculates`. Una sexta, `WeeklyRateBillingTests.Release_WithTheRateOfItsWeek_IsWeekly_AndWithAnother_IsManual`, falló en la corrida completa y pasó al repetirla. El 2026-11-24, a otra hora, las 762 salieron en verde. |
| 2 | FE | Registro: D4 a D9 y D11 (documento, depósito, manifiesto, duplicar, cerrar sin repesaje en el paso, tara del repesaje al editar, cola) | Compuertas FE; QA-AJQ3-005 a 014 en PASA en el navegador | Hecha el 2026-11-25 (FE `c70a736`). QA-AJQ3-005 a 014 en PASA en el navegador contra el API local, con Báscula: <br>• **005:** ERT3452 elegido, borrado el último carácter y elegido de nuevo; el campo dice solo «ERT3452». <br>• **006:** dos depósitos abiertos en tarjetas, con sus placas y ninguno elegido; Guardar mostró «Elija el depósito del camión o «Es otro documento».». <br>• **007:** «Es otro documento» quedó elegido; guardar creó el depósito 2026BA00010. <br>• **008 y 009:** con Factura Comercial, el manifiesto se ve sin asterisco y se guardó (MAN-FC-008, 6.000 kg); con carta porte sin manifiesto, los dos campos piden su dato. El caso «vacíos, también guarda» lo cubre la prueba de `registration-form`. <br>• **010 y 011:** «Duplicar entrada» avisó, no cambió de página y conservó lo digitado; la cola y el panel mostraron la «D» con «Duplicada pendiente». Atenderla y guardar dio una duplicada en $0 y consumió la pendiente; «Descartar duplicada» pidió confirmar, volvió a la cola y la quitó. <br>• **012 y 013:** «Cerrar sin repesaje» en DUP123 (ingreso) y en GTY567 (solo báscula) confirmó con el primer peso (32.000 kg), cerró el ciclo y pasó al Tiquete; los dos salieron de la cola. <br>• **014:** el ingreso completado `b68db780` mostró la tara real (2.000, «Repesaje»); con P. indicador en 33.000 y motivo, guardó sin el 400 y la mercancía quedó en 31.000. Luego se devolvió a 32.500. <br>• **Compuertas:** `yarn test` de 138 a 138 archivos y de 695 a 701 pruebas; lint de 229 a 229 errores, ninguno en archivos tocados; `yarn build` en 0. <br>• **Casos borde (`DEC-002`):** <br>  – C-F03-54 devuelve el contador, pero el cliente HTTP borra sin leer la respuesta (`contractApi().remove`); la página solo vuelve a la cola. <br>  – Al corregir una entrada ya cobrada, el aviso decía «la entrada queda «Por cobrar»». Ahora dice «Registro corregido.». <br>• **Fuera de esta fase:** al leer una entrada guardada (C-F03-13), el API devuelve `modalityCode` «IMP001» y el formulario espera «IMP». Al editar, ninguna modalidad sale marcada. Viene de I-03. **Resuelto el 2026-11-25** con la respuesta del usuario («Sí, corregirla»), sin cambiar el contrato: `modalityFromCode` traduce por prefijo, como el backend al registrar, y «OTH001» queda sin opción. Rama `f2/f03-modalidad-edicion`: FE `3e9f87b`, fusionada en `fase-2` (`96adc85`). `yarn test` de 703 a 704 pruebas; lint en 229 errores; `yarn build` en 0. En el navegador, `b68db780` abre con «Importación» marcada. En la base local no hay ingresos de exportación ni de inspección; esos casos los cubre la prueba. <br>• **Para la fase 3:** el paso Repesaje dice «se corrige con motivo en «Editar pesajes»», un botón que D13 retira. Ese texto cambia en la fase 3. |
| 3 | FE y docs | Historial, detalle y drawers: D12 a D18; convención y docs; fusión de `f2/f03-ajustes-qa` en `fase-2` en los dos repos | Compuertas FE; QA-AJQ3-015 a 022 en PASA; fusiones con push | Hecha el 2026-11-25 (FE `f634510`; fusiones BE `eb4e428` y FE `d4f94c6`, con push). QA-AJQ3-015 a 022 en PASA en el navegador contra el API local (Báscula; Administrador en 017): <br>• **015:** el menú de Báscula queda Dashboard, Proceso de pesaje, Entradas, Salidas y Solo báscula; las migas dicen «Báscula › Entradas», «› Salidas» y «› Solo báscula». <br>• **016:** el drawer de `b68db780` muestra «Pesajes del ciclo»: Pesaje · Bruto · 32.500 (con el 33.000 de la corrección tachado) y Repesaje · Tara · 2.000, con sus fechas. <br>• **017:** Terceros (Editar, Bloquear salidas), Servicios (Editar), Conductores (Editar) y Usuarios (Editar, Restablecer contraseña, Desactivar) llevan sus acciones en el menú, sin pie; Auditoría, sin menú. <br>• **018:** el drawer no tiene «Editar pesajes»; «Editar» del menú abre el registro de la entrada. <br>• **019 y 020:** «Cerrar sin repesaje» en el menú de la fila y del drawer cerró DUP123 (FC-QA-008, 15.000 kg), ABC123 (salida, 32.000 kg) y S749005 (solo báscula, 18.000 kg); las filas pasaron a «Completado». S749005 es un ingreso de prueba creado para el caso. <br>• **021:** «Pesos (kg)» de Entradas con cuatro líneas, con «P. manifiesto». <br>• **022:** el botón «⋮» de los historiales de Báscula y de Vigilancia › Historial es secundario, con borde y pequeño, en tema claro y en oscuro. <br>• **Compuertas:** `yarn test` de 138 a 138 archivos y de 701 a 703 pruebas; lint de 229 a 229 errores, ninguno en archivos tocados, y de 324 a 319 avisos; `yarn build` en 0. <br>• **Casos borde (`DEC-002`):** <br>  – `cycles/[id]` no tiene drawer. Sus acciones del encabezado salen de la misma regla, así que Báscula conserva «Editar» allí al quitar «Editar pesajes» de la sección (`DEC-005`). <br>  – El texto del paso Repesaje («se corrige con motivo en «Editar pesajes»») pasa a «Modificar pesaje» del detalle del ciclo. <br>  – `WeighbridgeHistoryActions` declara sus eventos uno por uno, con lo que salen 6 avisos de lint. <br>• **Capturas:** `evidencias/ajq2-01` a `ajq2-08` (fase 2) y `ajq3-01` a `ajq3-04` (fase 3). |

---

## 5. Pruebas y casos QA

**Backend:**

- `PendingDuplicateRulesTests`: agrega con el camión en planta y motivo de ingreso; rechaza con salida o con otra categoría; quitar con cero falla; consumir con cero se queda en cero.
- `PendingDuplicatesTests` (integración): C-F03-53 dos veces, C-F03-54 una vez y la cola con una fila pendiente; registrar la duplicada la consume; el camión con sus entradas completas y una pendiente sigue en la cola; 403 sin `ScaleAccess`.

**Frontend (Vitest):**

- `registration-form`: el manifiesto viaja con cualquier tipo; obligatorio solo con carta porte; `"new"` viaja como `null`; sin elegir depósito con abiertos, error; `tareWeight` con tara real.
- `registration-weights`: `weightFields` con manifiesto en todo ingreso; mercancía = indicador − tara real.
- `queue-display`: `queueRowKey` distinto para dos pendientes; `attendQuery` de una pendiente → `duplicar=1`.
- `entry-detail`: `canCloseWithoutReweigh`; `detailRecordActions` con `edit` y `closeWithoutReweigh`; `detailWeighingRows` con corrección.
- `AppDetailDrawer`: con una acción, menú y sin pie.
- `AppRowActions`: el botón del menú con borde.
- `RegistrationEntrySection`: elegir «Es otro documento» queda elegido; elegir la sugerencia deja solo el número en el campo.
- `WeighbridgeHistoryActions`: «Cerrar sin repesaje» según el estado.

**Casos QA** (navegador contra el API local, Administrador y Báscula):

| Caso | Hallazgo | Pasos | Resultado esperado |
| --- | --- | --- | --- |
| QA-AJQ3-001 | 5 | API: C-F03-53 sobre un camión de ingreso en planta, dos veces | 200 con `pendingDuplicateEntries` 1 y 2; la cola suma dos filas «Sin iniciar» con `isPendingDuplicate` |
| QA-AJQ3-002 | 5 | API: C-F03-54; otra vez con cero | 200 con 1; luego 400 «La entrada no tiene duplicadas pendientes.» |
| QA-AJQ3-003 | 5 | API: C-F03-53 sobre una salida o un solo báscula | 400 «Solo se duplican las entradas de ingreso.» |
| QA-AJQ3-004 | 5 | API: registrar con C-F03-01 la duplicada de un camión con una pendiente | `isDuplicateEntry: true`; el contador baja a 0 |
| QA-AJQ3-005 | 2 | Escribir un número, elegir la sugerencia, borrar el último carácter, volver a escribirlo y elegirla | El campo muestra solo el número |
| QA-AJQ3-006 | 3 | Número con depósitos abiertos | Tarjetas con placas y demás datos; ninguna elegida; Guardar pide elegir |
| QA-AJQ3-007 | 3 | Elegir «Es otro documento: crear depósito nuevo» y guardar | Queda elegida; se crea un depósito nuevo |
| QA-AJQ3-008 | 4 | Ingreso con un tipo distinto de carta porte; llenar el manifiesto y guardar | Los campos se ven sin asterisco; el manifiesto se guarda; vacíos, también guarda |
| QA-AJQ3-009 | 4 | Ingreso con carta porte sin manifiesto | Error en los dos campos, como hoy |
| QA-AJQ3-010 | 5 | Con el registro a medio llenar, «Duplicar entrada» | Aviso; la página no cambia ni pierde datos; la cola y el panel muestran la fila «D» |
| QA-AJQ3-011 | 5 | Atender la fila «D», guardar; en otra, «Descartar duplicada» | La primera queda como entrada duplicada en $0; la segunda desaparece de la cola |
| QA-AJQ3-012 | 6 | Ingreso «Por repesar»: «Cerrar sin repesaje» en el paso | Confirmación; el ciclo se cierra con el primer peso; pasa al Tiquete; sale de la cola |
| QA-AJQ3-013 | 13 | Solo báscula con «Req. 2 pesaje», en el paso Repesaje | Mismo resultado que el caso 012 |
| QA-AJQ3-014 | 8 | Editar un ingreso completado con repesaje y cambiar P. indicador, con motivo | Guarda sin el 400; la tara se ve como «Repesaje»; la mercancía se recalcula |
| QA-AJQ3-015 | 1 | Menú Báscula | Dashboard, Proceso de pesaje, Entradas, Salidas y Solo báscula, sin «Historial»; las migas coinciden |
| QA-AJQ3-016 | 7 | Drawer del ciclo `b68db780` | «Pesajes del ciclo» con el pesaje de 32.500 kg y el repesaje de 2.000 kg, con sus fechas |
| QA-AJQ3-017 | 9 | Drawers de Terceros, Servicios, Conductores, Usuarios y Báscula | Sin pie; las acciones en el menú del encabezado; Auditoría sin menú |
| QA-AJQ3-018 | 11 | Drawer de un ciclo editable | Sin «Editar pesajes» en la sección; «Editar» en el menú abre el registro |
| QA-AJQ3-019 | 10 | Historial › Entradas: una fila «Por repesar» | «Cerrar sin repesaje» en el menú de la fila y del drawer; al confirmar, la fila pasa a «Completado» |
| QA-AJQ3-020 | 10, 13 | Lo mismo en Salidas y en Solo báscula | Igual |
| QA-AJQ3-021 | 12 | Historial › Entradas: columna «Pesos (kg)» | Cuatro líneas, con «P. manifiesto» |
| QA-AJQ3-022 | 12 | Historiales de Báscula y Vigilancia › Historial | El botón «⋮» con borde, igual que los de Configuración, en tema claro y oscuro |

---

## 6. Compuertas de cada fase

- **BE (fase 1):** `dotnet build Wms.sln` sin errores; `dotnet test Wms.Tests` (base 2158) y `dotnet test Wms.IntegrationTests` (base 762) en verde; `dotnet ef migrations has-pending-model-changes` limpio.
- **FE (fases 2 y 3):** `yarn build` con código 0; `yarn test` en verde (base 138 archivos y 695 pruebas); `yarn lint` con 229 errores o menos y ninguno en archivos nuevos o tocados; las guardias de `FT/unit/guards/` en verde.
- Capturas de los casos de la fase.

---

## 7. Commits

| Fase | Repo | Mensaje |
| --- | --- | --- |
| 1 | BE | `feat(bascula): duplicadas pendientes en la cola (DEC-080, F03, QA manual de integración)` |
| 2 | FE | `fix(bascula): registro del camión: documento, depósito con placas, manifiesto, duplicar sin salir, cerrar sin repesaje y tara del repesaje (DEC-080, F03, QA manual de integración)` |
| 3 | FE | `style(bascula): menú, acciones de drawers y tablas, pesajes del ciclo y cerrar sin repesaje en el historial (DEC-080, F03, QA manual de integración)` |
| 3 | docs | `docs(f03): ajustes de la QA manual de la integración; drawer con acciones en el menú` |

Fusiones: `f2/f03-ajustes-qa` en `fase-2`, con `--no-ff`, en BE y en FE, al cerrar la fase 3.

---

## 8. Riesgos

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R1 | Dos operarios atienden la misma duplicada pendiente y guardan las dos | Las dos se guardan como duplicadas en $0 y el contador no baja de cero. Es el mismo efecto que duplicar dos veces; se anula una con motivo |
| R2 | Un camión sale con duplicadas pendientes | La cola solo muestra camiones en planta (D10); el contador queda en la entrada, sin efecto |
| R3 | Quitar la preselección del depósito agrega un clic al operario | Lo pide `DEC-057` D1 y `P03/` D44: evita sumar un camión al depósito equivocado |
| R4 | Todas las acciones del drawer en el menú esconden «Editar», la más usada | Es la regla pedida (`H/` 9); el menú se abre con un clic y con teclado |
