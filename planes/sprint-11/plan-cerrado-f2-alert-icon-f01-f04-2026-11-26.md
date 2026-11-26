# Plan cerrado — Fase 2 · Aviso junto a un dato (`AppAlertIcon`) en F01 a F04

> **Fecha:** 26 de noviembre de 2026. **Estado:** Aprobado por el usuario el 2026-11-26 («Apruebo el plan con las recomendaciones de P1 a P4»; §1.4). Sin ejecutar: arranca cuando `AppAlertIcon` llegue a `fase-2` con la fusión de F05 (D3, P4).
> **Origen:** la regla del usuario en la revisión de F05 ([`qa-manual/hallazgos-UI-F05.md`](qa-manual/hallazgos-UI-F05.md), punto 10): «Si se necesita agregar un mensaje en una columna al lado de un dato como el de "Datos pendientes", usar un icono de alerta pequeño y con tooltip. Esto aplica para toda la app». El plan de ajustes de UI de F05 (`AUI/`) creó `AppAlertIcon` y la convención «Aviso junto a un dato» (D4), la extendió a lo anulado (D34) y a la fila anulada en rojo tenue (D36), y dejó F01 a F04 «en un plan aparte» (`AUI/` §4). Este es ese plan.
> **Base:** FE `fase-2` `12f6656` (inventario hecho sobre `f2/f05-comercio-exterior` `17694dc`, que tiene las mismas pantallas de F01 a F04) · docs `main` `e8deb14`. Rama: `f2/ui-alert-icon`, desde `fase-2` cuando tenga `AppAlertIcon` (D3).
> **Alcance:** solo frontend. Cambia la forma de seis avisos en cinco archivos de Báscula y Bodega, suma una guardia y ajusta la convención. Sin cambios de backend, de contrato, de datos ni de reglas.
> **Rutas:** relativas a `code_workspace/`. Prefijos: `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`; `AUI/` = `D/planes/sprint-11/f05-comercio-exterior/plan-cerrado-f2-f05-ajustes-ui-2026-11-26.md`; `AUI3/` = `D/planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-ajustes-ui-2026-11-24.md`; `PAJ/` = `D/planes/sprint-11/f02-base/plan-cerrado-f2-f02-ajustes-qa-2026-11-24.md`; `P04/` = `D/planes/sprint-11/f04-bodega/plan-cerrado-f2-f04-bodega-2026-11-25.md`.

---

## 0. Instrucciones para el ejecutor

1. **Lecturas mínimas:** `Frontend/wms/AGENTS.md` (sección «Eficiencia de contexto y cierres por fase»), `D/contexto/convenciones-tecnicas.md` §3 («Aviso junto a un dato»), `AUI/` D4, D34 y D36, y este plan completo.
2. **Rama y git:** empieza solo cuando `fase-2` tenga `F/components/app/AppAlertIcon.vue` (D3). `git fetch`; crea `f2/ui-alert-icon` desde `fase-2` y anota su hash en la cabecera. Commit al cerrar la fase con el mensaje de §7 y push de la rama. Al pasar las compuertas, fusiona en `fase-2` con `--no-ff` y push. Sin `push --force`.
3. **Líneas citadas:** son de `f2/f05-comercio-exterior` `17694dc`. Confírmalas con grep. Si el código no coincide con lo que dice este plan, pregunta en un solo mensaje.
4. **Componentes compartidos:** `AppAlertIcon` no cambia. `AppDataTable`, `AppTable`, `AppDetailDrawer`, `AppDetailSection`, `VehiclePlateTag` y el resto, tampoco. Si un cambio pide tocar otro, detente y pregunta.
5. **Convenciones:** las de `Frontend/wms/AGENTS.md`. Fechas con `formatColombiaDateTime`; estilos con utilidades de Tailwind y tokens de PrimeVue, sin colores fijos.
6. **Verificación:** backend local y `yarn dev`, con Admin y con un usuario de cada rol que use la pantalla (Báscula, Bodega). Cada caso, con captura en ancho normal y angosto (768 px).

---

## 1. Decisiones

Mandan sobre el resto del plan (`DEC-002`).

### 1.1 Alcance y criterio

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **Pantallas de F01 a F04:** las de `F/pages` y `F/features` que no son de Comercio Exterior (F05), Salidas (F06; incluye las órdenes de cargue, que F06 retira, AF-97), Tarifas y acuerdos (F07), Facturación (F08), Notificaciones (F09), Ayuda, Autenticación, la verificación pública de guías ni la galería `/dev/components`. Los reportes de `F/pages/reports` entran al recorrido; ninguno tiene un aviso junto a un dato (§2.2) | Pedido de esta tarea; plan maestro de la fase 2 §3 (alcance de F01 a F09) |
| D2 | **Qué cambia y qué no.** Cambia a `AppAlertIcon` una etiqueta (`Tag`), un mensaje (`Message`) o un icono suelto (`<i class="pi pi-exclamation-…">` con tooltip) que **agrega un aviso** a un dato de la misma celda, de la misma línea o de la misma tarjeta de dato. No cambian: <br>• un **estado en su propia columna o en su campo** (la columna «Estado», «Corregido», «Tipo»): la etiqueta es el dato (P1 decide el caso «Anulada»); <br>• un **valor que es el dato** («Por ubicar» en lugar de la ubicación, el tiempo en planta, los relojes de Bodega); <br>• el **estado del registro** en el encabezado del drawer o del modal (`PAJ/` D5); <br>• los **mensajes de una sección o de un formulario**: validaciones, avisos de un paso, estados vacíos, confirmaciones y el aviso del registro anulado al inicio de un drawer; <br>• lo que una ronda anterior decidió con el usuario: la «D» de la entrada duplicada (`AUI3/` D7; P2) y el aviso de salidas bloqueadas del tercero (`PAJ/` D8) | `AUI/` D4 y su convención; hallazgo 10 de F05 («al lado de un dato») |
| D3 | **Después de que `AppAlertIcon` llegue a `fase-2`.** Hoy solo está en `f2/f05-comercio-exterior` (`b0695f5`). El plan arranca cuando F05 se fusione en `fase-2` (con I-05, plan maestro §5.3), en la rama `f2/ui-alert-icon`, y se fusiona en `fase-2` con `--no-ff` al pasar las compuertas. No se mezcla con I-05 (P4) | Plan maestro §5.3; mismo esquema que `plan-cerrado-f2-paginas-sin-tarjeta-titulo-2026-11-24.md` D4 |

### 1.2 Cambios por pantalla

| # | Decisión | Fuente |
| --- | --- | --- |
| D4 | **Novedades: la novedad anulada con icono y la fila en rojo tenue** (`F/pages/warehouse/novelties/index.vue:216-227`). La etiqueta «Anulada» junto al producto (`:219`) pasa a `AppAlertIcon` (`danger`), a la derecha del producto, con el tooltip «Novedad anulada el {fecha y hora}: {motivo}.» (sin «: {motivo}» si no hay motivo; `voidedAt` y `voidReason` ya vienen en C-F04-30, `F/features/warehouse/contracts/novelty.ts:19`) y `data-testid="novelty-voided"`. El producto deja de ir tachado y atenuado (`:218`), y la fila lleva el fondo rojo tenue de la convención (`AUI/` D36): una marca en la celda (`<span class="novelty-row-voided">`) y la regla `tr:has(.novelty-row-voided):nth-child(n) > td` con `--p-red-50` (rojo al 15 % en tema oscuro), como los historiales de Báscula (`F/pages/operations/weighbridge/history/exits.vue:184`). Con anulada no se muestra el aviso de cantidades (como hoy, `v-else-if`) | `AUI/` D34, D36; convención «Aviso junto a un dato» |
| D5 | **Novedades: el aviso de cantidades sin cuadrar** (`:220-226`). El icono suelto (`pi pi-exclamation-triangle text-orange-500` con `v-tooltip`) pasa a `AppAlertIcon` (`warn`) con `text` = `row.quantityWarning` y `data-testid="novelty-quantity-warning"`. El `aria-label` deja de ser «Cantidades sin cuadrar» y pasa a ser el texto completo del aviso | Convención (D2: icono suelto) |
| D6 | **Historial de recepciones: la diferencia con icono** (`F/pages/warehouse/receptions/history.vue:116-120`). La etiqueta «Diferencia» (`:119`) pasa a `AppAlertIcon` (`warn`), a la derecha de la mercancía, con el tooltip de hoy, «Lo contado difiere de lo declarado», y `data-testid="reception-discrepancy"`. «Sobre vehículo» (`:118`) sigue como etiqueta: dice dónde quedó la mercancía (la ubicación sembrada `SOBRE-VEHICULO`, `P04/` D4), no es un aviso | Convención; `P04/` D4 y QA2-F04-033 |
| D7 | **Registrar uso de montacargas: el depósito con uso en curso** (`F/features/warehouse/components/ForkliftStartDialog.vue:188-193`). La etiqueta «Montacargas en curso» (`:191`) pasa a `AppAlertIcon` (`warn`), a la derecha del N.º de depósito, con el tooltip «Este depósito ya tiene un uso de montacargas en curso.» y `data-testid="forklift-in-progress"`. La etiqueta de estado «Recibido» o «Pendiente de recepción» (`:192`) se muestra siempre, también con el uso en curso, porque es el estado del depósito. La opción sigue deshabilitada (`:185`) | Convención; `D/planes/sprint-11/f04-bodega/plan-cerrado-f2-f04-ajustes-ui-2026-11-25.md` D5 («Finalizar montacargas» desde la fila de Recepción) |
| D8 | **Detalle de báscula: el manifiesto que supera la diferencia de pesajes** (`F/features/weighbridge/components/WeighbridgeEntryDetail.vue:89-98`). El mensaje bajo las tarjetas de peso (`:98`) pasa a `AppAlertIcon` (`warn`), a la derecha del valor de la tarjeta «P. manifiesto» (`card.key === "manifest"`, `F/features/weighbridge/utils/entry-detail.ts:102`), con el texto de hoy (`manifestExceedsText`, `:121-125`) y `data-testid="manifest-warning"`. `manifestExceedsText` no cambia | Convención («el peso con diferencia»); P-BAS-11 (`D/planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-bascula-2026-11-24.md` D30) pide el aviso, no su forma |
| D9 | **Registro de báscula: el producto nuevo** (`F/features/weighbridge/components/RegistrationGoodsLines.vue:79-81`). La etiqueta «Nuevo» (`:81`) junto al producto escrito a mano pasa a `AppAlertIcon` (`warn`), a la derecha del campo, con el tooltip «Producto nuevo: se crea al guardar y se avisa a Comercio Exterior.» (lo que hace hoy, según el comentario del componente, `:3-6`) y `data-testid="goods-line-new"` | Convención; D22 del plan de F03 (`D/planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-bascula-2026-11-24.md`; texto libre con «+») |

### 1.3 Convención y guardia

| # | Decisión | Fuente |
| --- | --- | --- |
| D10 | **La convención queda completa.** En `D/contexto/convenciones-tecnicas.md` §3, «Aviso junto a un dato»: <br>• «Adopción» pasa a: «F05 lo usa desde sus ajustes de UI y F01 a F04 desde el plan `planes/sprint-11/plan-cerrado-f2-alert-icon-f01-f04-2026-11-26.md`. Las fases siguientes (F06 a F09) lo aplican al hacer sus pantallas». <br>• Un punto nuevo, «Qué no es un aviso», con la lista de D2 (estado en su columna, valor que es el dato, estado del registro en el encabezado, mensajes de sección), con el estado «Anulada» en su propia columna entre los ejemplos (P1). <br>• La línea de lo anulado (D34) y la de la fila en rojo tenue (D36) ya están (docs `d40d4db`): no cambian | `AUI/` D4, D34, D36 |
| D11 | **Guardia: ningún icono de aviso suelto.** `FT/unit/guards/source-guards.spec.ts` suma un `describe` «guardia: aviso junto a un dato (DEC-080)» que falla si un `.vue` de `app/`, salvo `F/components/app/AppAlertIcon.vue`, tiene una etiqueta `<i` cuya clase incluye `pi-exclamation-` y que lleva `v-tooltip` (usa `openingTag` del mismo archivo), y un caso que comprueba que la regla detecta un icono suelto y deja pasar `AppAlertIcon`. Los `Tag` y `Message` no se pueden distinguir por texto de un estado o de un mensaje de sección: la guardia no los mira | `FT/unit/guards/source-guards.spec.ts` (`findMatches`, `openingTag`, `:15-40`) |

### 1.4 Preguntas al usuario

Respuesta del usuario (2026-11-26): las cuatro recomendaciones. Así, P1: los historiales de Báscula conservan «Anulada» en su columna «Estado» y la convención lo dice en «Qué no es un aviso» (D10); P2: la «D» se queda; P3: el icono de F05 cambia en este plan (§3); P4: se espera a la fusión de F05 en `fase-2` (D3).

| # | Pregunta | Recomendación |
| --- | --- | --- |
| P1 | La convención dice que una fila anulada lleva `AppAlertIcon` «sin la etiqueta "Anulada"» (D34). Los tres historiales de Báscula muestran «Anulada» en su columna «Estado», junto a los otros estados, con el motivo en el tooltip (`F/pages/operations/weighbridge/history/index.vue:163-171`, `exits.vue:138-146`, `weighing-only.vue:131-139`), y la fila ya va en rojo tenue. ¿Se quedan así? | Que se queden: la etiqueta es el dato de la columna «Estado», no un aviso junto a otro dato. La convención lo dirá (D10). Si no, el icono va junto a la placa y la columna muestra «—» en la fila anulada; además, las filas de C-F03-22 traen `voidReason` pero no la fecha de la anulación (`F/features/weighbridge/contracts/history.ts:53`, `:84`, `:109`), así que el tooltip con la fecha que pide la convención necesitaría un campo nuevo en el backend, fuera del alcance de este plan |
| P2 | La «D» de la entrada duplicada es un `Tag` pequeño junto a la placa, con tooltip (`F/features/weighbridge/components/VehiclePlateTag.vue:12-20` y el panel de la cola, `WeighbridgeQueuePanel.vue:112` y `:129`). Lo pidió usted en la revisión de F03 (`AUI3/` D7). ¿Se queda? | Que se quede: es una marca del registro, no un aviso, y fue una decisión suya |
| P3 | La guardia de D11 también encuentra un icono suelto en F05: «Falta el manifiesto del camión» en la fila expandida de las listas de depósitos (`F/features/foreign-trade/components/DepositExpandedEntriesTable.vue:184-189`). ¿Lo cambio a `AppAlertIcon` en este plan? | Sí: es una línea, y así la guardia no necesita excepciones |
| P4 | `AppAlertIcon` llega a `fase-2` con la fusión de F05 (después de I-05). ¿Se espera a eso? | Sí (D3). Hacerlo antes pide sacar la rama de `f2/f05-comercio-exterior`, y F01 a F04 quedarían atados a la fusión de F05 |

---

## 2. Inventario

Recorrido con grep de `<Tag`, `<Message` y `pi-exclamation` en `F/pages`, `F/features` y `F/components`, sin las áreas que D1 excluye (`<Tag` y `<Message` aparecen 250 veces en 164 archivos; 176 apariciones, con los iconos `pi-exclamation`, quedan en el alcance).

### 2.1 Cambian

| Pantalla | Archivo | Hoy | Cambio | Decisión |
| --- | --- | --- | --- | --- |
| Bodega › Novedades | `F/pages/warehouse/novelties/index.vue:219` | `Tag` «Anulada» (`danger`) junto al producto, motivo en el tooltip; producto tachado | `AppAlertIcon` `danger`; fila en rojo tenue | D4 |
| Bodega › Novedades | `F/pages/warehouse/novelties/index.vue:220-226` | Icono suelto naranja con el aviso de cantidades | `AppAlertIcon` `warn` | D5 |
| Bodega › Entradas › Historial | `F/pages/warehouse/receptions/history.vue:119` | `Tag` «Diferencia» (`warn`) junto a la mercancía | `AppAlertIcon` `warn` | D6 |
| Bodega › Montacargas › Registrar uso | `F/features/warehouse/components/ForkliftStartDialog.vue:191` | `Tag` «Montacargas en curso» (`warn`) junto al depósito | `AppAlertIcon` `warn`; el estado, siempre | D7 |
| Báscula › Historial › detalle (P-BAS-11) | `F/features/weighbridge/components/WeighbridgeEntryDetail.vue:98` | `Message` (`warn`) bajo las tarjetas de peso | `AppAlertIcon` `warn` junto a «P. manifiesto» | D8 |
| Báscula › Registro | `F/features/weighbridge/components/RegistrationGoodsLines.vue:81` | `Tag` «Nuevo» (`warn`) junto al producto escrito a mano | `AppAlertIcon` `warn` | D9 |

### 2.2 Se quedan (D2)

| Archivo | Qué es | Por qué |
| --- | --- | --- |
| `F/pages/operations/weighbridge/history/index.vue:165`, `exits.vue:140`, `weighing-only.vue:133` | Estado de la entrada (con «Anulada» y su motivo) | Estado en su columna (P1) |
| `F/features/weighbridge/components/VehiclePlateTag.vue:12`; `WeighbridgeQueuePanel.vue:112`, `:129` | «D» de la entrada duplicada | `AUI3/` D7, pedido del usuario (P2) |
| `F/pages/operations/entries/history.vue:228` | «Corregido» con fecha y usuario en el tooltip | Columna propia «Corregido» |
| `F/pages/operations/entries/exits.vue:208` | Tiempo en planta, ámbar si es largo | Es el dato |
| `F/pages/warehouse/inventory/index.vue:247`, `:270` | Estado del depósito en la barra; «Por ubicar» | Estado (`D/planes/sprint-11/f04-bodega/plan-cerrado-f2-f04-ajustes-ui-2026-11-25.md` D13); valor que reemplaza a la ubicación |
| `F/pages/warehouse/receptions/history.vue:118`; `F/features/warehouse/components/ReceptionDetail.vue:40`, `:94` | «Sobre vehículo» | Ubicación de la mercancía (`P04/` D4) |
| `F/features/warehouse/components/WarehouseClockTag.vue:31` | Reloj de Bodega | Es el dato |
| `F/features/warehouse/components/ReceptionDialog.vue:204` | «Pendiente» en el encabezado del modal | Estado del registro |
| `F/features/warehouse/components/NoveltiesTable.vue:110-116` | «Anulada» o «Vigente» | Columna «Estado»; además, solo la usa F05 (`DepositNoveltiesSection`) |
| `F/pages/admin/locations/index.vue:170` | «Del sistema» en la columna de acciones | Dice por qué la fila no tiene acciones; no acompaña un dato |
| `F/pages/admin/stakeholders/index.vue:363`, `:375`, `:383`, `:387` | Salidas, estado financiero, UAP y el aviso de salidas bloqueadas | `PAJ/` D8 |
| `F/pages/admin/users/index.vue:393`, `:419` | Cambio de contraseña; «Sin roles» | Valor del campo; estado vacío de la sección |
| `F/features/weighbridge/components/WeighbridgeEntryDetail.vue:39`, `:136`, `:150` | Aviso del registro anulado al inicio del drawer; «Duplicada» en «Tickets asociados»; estado del cobro | Aviso del registro, no de un dato; `AUI3/` D7 conserva «Duplicada» en el detalle; estado |
| `F/pages/operations/weighbridge/process/[entryLogId].vue:659-790`; `WeighbridgeReweighStep.vue`, `WeighbridgeChargeStep.vue`, `WeighbridgeTicketStep.vue`, `RegistrationExitSection.vue`, `ServiceCorrectionDialog.vue`, `ModifyWeighingDialog.vue` | Avisos de paso, errores y estados vacíos | Mensajes de sección |
| `F/pages/operations/entries/index.vue:367-377`; `F/features/entries/components/*` | Ingreso abierto, búsqueda del vehículo o del conductor, cambio de fecha | Mensajes del formulario |
| `F/features/warehouse/components/NoveltyFormDialog.vue:428`, `AdjustInventoryDialog.vue:164`, `ForkliftStartDialog.vue:167`, `ForkliftChargeDialog.vue`, `ProductPlacementsDialog.vue`, `DirectReceptionGoodsSection.vue`, `ReceptionProductRows.vue` | Avisos y validaciones de formulario | Mensajes del formulario |
| `F/features/traceability/components/TruckGrid.vue:204`, `TruckDetailSidebar.vue:153`, `:243`, `:255`, `:273`; `TruckStageBadge.vue` | Tipo de servicio, estado del depósito, etapa | Son el dato |
| `F/pages/reports/*.vue` (`warehouse-movements.vue:463`, `customs-agency-entries.vue:180`, mensajes de error) | Tipo de movimiento, proceso; error de la consulta | Son el dato; mensaje de la página |
| Catálogos de Administración y Configuración (`F/pages/admin/*`, `F/pages/settings/*`, `BankAccountsList.vue`, `CityImportDialog.vue`) | Activo o Inactivo, categoría, prefijo, roles, acción de auditoría; avisos de importación y de edición | Estados y valores en su columna (`PAJ/` D14 para el prefijo); mensajes del modal |
| `F/components/app/AppTable.vue:552`, `AppDetailDrawer.vue:87`, `AppFormField.vue:28`, `AppCrudDialog.vue:128`, `AppChargeForm.vue`; `F/components/layout/AppRightMenu.vue:75` | Compartidos | §0.4; estado del encabezado (`PAJ/` D5) y errores de formulario |

---

## 3. Archivos que se tocan

| Archivo | Cambio | Decisión |
| --- | --- | --- |
| `F/pages/warehouse/novelties/index.vue` | Icono de anulada, marca y estilo de la fila; icono de cantidades | D4, D5 |
| `F/pages/warehouse/receptions/history.vue` | Icono de diferencia | D6 |
| `F/features/warehouse/components/ForkliftStartDialog.vue` | Icono de uso en curso; estado siempre | D7 |
| `F/features/weighbridge/components/WeighbridgeEntryDetail.vue` | Icono junto a «P. manifiesto» | D8 |
| `F/features/weighbridge/components/RegistrationGoodsLines.vue` | Icono de producto nuevo | D9 |
| `F/features/foreign-trade/components/DepositExpandedEntriesTable.vue` | Icono de manifiesto faltante: `AppAlertIcon` (`warn`) con «Falta el manifiesto del camión» | D11, P3 |
| `FT/components/weighbridge/WeighbridgeEntryDetail.spec.ts` | `manifest-warning` es el icono: su `aria-label` tiene el texto (hoy `.text()`, `:33`) | D8 |
| `FT/components/weighbridge/RegistrationGoodsLines.spec.ts` | `goods-line-new` con su `aria-label` en lugar de «Nuevo» en el texto (`:27`) | D9 |
| `FT/components/warehouse/ForkliftStartDialog.spec.ts` (nuevo) | Con uso en curso: el icono, el estado y la opción deshabilitada | D7 |
| `FT/components/warehouse/NoveltiesPage.spec.ts` (nuevo) | Anulada: icono `danger` con fecha y motivo, sin aviso de cantidades, marca de fila; vigente con aviso: icono `warn` | D4, D5 |
| `FT/unit/guards/source-guards.spec.ts` | Guardia del icono suelto | D11 |
| `D/contexto/convenciones-tecnicas.md` §3 | «Adopción» y «Qué no es un aviso» | D10 |

El historial de recepciones (D6) no tiene prueba de página: lo cubre QA-AI-003. Si al montar la página de Novedades la prueba pide más simulación de la que vale, se cubre con QA-AI-001 y 002 y se dice en el cierre.

---

## 4. Fases

| Fase | Contenido | Criterio de salida | Estado |
| --- | --- | --- | --- |
| 1 | D4 a D11 y el icono de F05 (P3), la convención, el cierre y la fusión en `fase-2` | Compuertas de §6; QA-AI-001 a 006 en PASA; fusión hecha y publicada | Pendiente |

Es una sola fase: seis cambios pequeños en cinco archivos, sin dependencias entre ellos.

---

## 5. Pruebas y casos QA

**Vitest:** las de §3 y la guardia (D11). `FT/unit/components/AppAlertIcon.spec.ts` no cambia.

**Casos QA** (navegador, backend local; Bodega para 001 a 004, Báscula para 005 y 006; Admin en todos):

| Caso | Pasos | Resultado esperado |
| --- | --- | --- |
| QA-AI-001 | Novedades con «Incluir anuladas»; pasar el mouse y luego el teclado (Tab) sobre el icono de una anulada | Icono rojo junto al producto, tooltip «Novedad anulada el {fecha y hora}: {motivo}.»; producto sin tachar; la fila en rojo tenue, también en tema oscuro; sin etiqueta «Anulada» |
| QA-AI-002 | Novedades: una vigente con cantidades sin cuadrar | Icono ámbar junto al producto con el aviso de hoy en el tooltip |
| QA-AI-003 | Entradas › Historial: una recepción con diferencia y una «Sobre vehículo» | Icono ámbar «Lo contado difiere de lo declarado» junto a la mercancía; «Sobre vehículo» sigue en etiqueta |
| QA-AI-004 | Montacargas › «+ Registrar uso» con la placa de un camión que tiene un uso en curso | El depósito con el icono ámbar y su tooltip, su estado en etiqueta y la opción deshabilitada |
| QA-AI-005 | Báscula › Historial › Entradas: «Ver detalle» de una entrada cuyo manifiesto supera la diferencia de pesajes | Icono ámbar junto al valor de «P. manifiesto», con el texto de hoy; sin el mensaje bajo las tarjetas |
| QA-AI-006 | Báscula › Registro: una línea con un producto escrito a mano (con el «+») | Icono ámbar junto al campo, con su tooltip; guardar funciona como hoy |

---

## 6. Compuertas de la fase

- `yarn build` con código 0.
- `yarn test` en verde (base: la de `fase-2` al crear la rama; se conoce el error no manejado heredado de `WeighbridgeQueuePage.spec.ts`).
- `yarn lint` sin subir los errores de la base y sin ninguno en archivos tocados.
- Capturas de QA-AI-001 a 006 en `D/planes/sprint-11/evidencias-alert-icon/ai-00N-normal.jpg` y `-angosto.jpg`.

---

## 7. Commits

| Fase | Repo | Mensaje |
| --- | --- | --- |
| 1 | FE | `style(ui): avisos junto a un dato con AppAlertIcon en Báscula y Bodega (DEC-080)`, y la fusión `merge: aviso junto a un dato en F01 a F04, en fase-2` |
| 1 | docs | `docs(convenciones): aviso junto a un dato adoptado en F01 a F04; cierre del plan (sprint 11)` |

Al cerrar: el estado de este plan y su fila en `D/planes/README.md`; una línea en `D/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md` con los commits.

---

## 8. Riesgos

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R1 | Un aviso que hoy se lee sin pasar el mouse queda oculto en un tooltip | Es la regla del usuario; el icono tiene color por severidad y se enfoca con el teclado. QA-AI-001 lo revisa con el teclado |
| R2 | La regla de la fila roja de Novedades pierde contra las filas alternas | La misma especificidad que los historiales de Báscula (`:nth-child(n)`, D4); QA-AI-001 en los dos temas |
| R3 | Se confunde un estado con un aviso en las fases siguientes | D10: «Qué no es un aviso» en la convención |
| R4 | F05 llega a `fase-2` con más cambios a `AppAlertIcon` o a la convención | §0.3: confirmar con grep al empezar; si cambió la interfaz, preguntar |
