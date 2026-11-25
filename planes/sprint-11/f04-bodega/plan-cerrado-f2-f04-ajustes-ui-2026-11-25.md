# Plan cerrado — Fase 2 · F04 Bodega · Ajustes de UI de la maquetación

> **Fecha:** 25 de noviembre de 2026. **Estado:** Aprobado por el usuario el 2026-11-25 («Apruebo el plan»). Ejecutado el 2026-11-25 (FE `f9f4da0` y, con D13, `09c0b87`, en `f2/f04-bodega`); estado en §4.
> **Origen:** la revisión del usuario sobre la maquetación de F04 (FE-1 a FE-3, datos simulados; plan de F04 §8.7), antes de I-04: [`../qa-manual/hallazgos-UI-F04.md`](../qa-manual/hallazgos-UI-F04.md), siete hallazgos y una duda, con el mockup [`../qa-manual/modal-facturacion-montacargas/`](../qa-manual/modal-facturacion-montacargas/). Las respuestas del usuario del 2026-11-25 están en D1 a D4.
> **Base:** FE `f2/f04-bodega` `3ff4603` · docs `main` `e70efef`. Rama: `f2/f04-bodega` (FE). Se aplica antes de I-04.
> **Alcance:** solo frontend, sobre las pantallas maquetadas con datos simulados. Sin cambios de backend, de contrato ni migraciones. Cambia decisiones del plan de F04 (D24, D30 en la forma del diálogo, D39 y D42): donde chocan, gana este plan.
> **Rutas:** relativas a `code_workspace/`. Prefijos: `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`; `P04/` = `D/planes/sprint-11/f04-bodega/plan-cerrado-f2-f04-bodega-2026-11-25.md`; `H/` = el archivo de hallazgos.

---

## 0. Instrucciones para el ejecutor

1. Lee `Frontend/wms/AGENTS.md` (sección «Eficiencia de contexto y cierres por fase»), este plan completo y, de `P04/`, §8.4 a §8.6 (cómo quedó cada pantalla). Las líneas citadas son de la base `3ff4603`; confírmalas con grep antes de cambiar.
2. Trabaja en `f2/f04-bodega`. Una sola fase (§4). Al cerrarla: compuertas de §5, commit con el mensaje de §6, push de la rama, el estado aquí, en `P04/` §8 (fila «Revisión») y en la matriz, y te detienes con el reporte.
3. Sin llamadas reales: las páginas siguen en `MAQUETACION_PAGES` y con la sesión simulada (`NUXT_PUBLIC_MOCK_SESSION=true`, `?roles=Admin,Warehouse`).
4. El único compartido que cambia es `AppDataTable` (D1). Si otra pantalla necesita cambiar otro, detente y pregunta.

---

## 1. Decisiones

Mandan sobre el resto del plan (`DEC-002`).

### 1.1 Respuestas del usuario (2026-11-25)

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **Slot `toolbarEnd` en `AppDataTable`.** La barra de la tabla suma un slot a la derecha, antes de «Limpiar filtros» y «Exportar», para los controles propios de una página. Es aditivo: sin el slot, la barra se ve como hoy. Lo usan Montacargas (D7) y Novedades (D9). Excepción a `P04/` D39, con su prueba | Usuario: «Slot nuevo en AppDataTable (Recommended)»; hallazgos 3 y 7 |
| D2 | **(Reemplazada por D13.)** **Inventario: la tarjeta del depósito se queda arriba.** Las pestañas pasan a la barra de cada tabla (D8). En Existencias, la tarjeta de filtros con el depósito, su estado, cliente y totales sigue encima de la tabla (`P04/` D42); en Movimientos y Ubicaciones no hay tarjeta y la tabla sube | Usuario: «Tarjeta de filtros arriba (Recommended)»; hallazgo 6 |
| D3 | **«Registro fotográfico» sigue siendo texto**, con una ayuda bajo el campo: «Referencia de las fotos: carpeta o números de foto». Rige la decisión del plan de paridad (`D/planes/paridad-legacy/plan-backend-paridad-legacy.md` §B.4.8 y F4-03: `PhotoRecord` texto hasta 200, sin archivos; en el legacy, `reg_fotografico` `varchar(200)`) | Usuario: «Texto con mejor ayuda (Recommended)»; hallazgo 8 |
| D4 | **«Finalizar y cobrar» al final de la sección «Destinatario y pago».** El diálogo del cobro toma las secciones del mockup (D6), pero el botón lo sigue pintando `AppChargeForm`, al final de su formulario; `AppChargeForm` no cambia | Usuario: «Al final de la sección (Recommended)»; hallazgo 5 |

| D13 | **El depósito de Existencias en el extremo derecho de la tarjeta de la tabla** (pedido del usuario del 2026-11-25, después de ejecutar D1 a D12; reemplaza D2). Sale la tarjeta de filtros: el selector del depósito (`WarehouseDepositSelect`, 20 rem) va en `toolbarEnd`, a la derecha de las pestañas, con el estado, el cliente, la modalidad y los totales a su izquierda; el aviso del Borrador pasa al tooltip de su estado. Con un filtro de columna activo, «Limpiar filtros» aparece a la derecha del selector (lo pinta `AppDataTable` después de `toolbarEnd`) | Usuario: «en `warehouse/inventory` el filtro de "Depósito" ponerlo en extremo derecho de la card de la tabla» |

### 1.2 Recepción (hallazgos 1 y 2)

| # | Decisión | Fuente |
| --- | --- | --- |
| D5 | **«Finalizar montacargas» desde la fila de Recepción** (reemplaza la segunda frase de `P04/` D24). Una fila con uso en curso (`forkliftInProgress`) muestra la acción «Finalizar montacargas» (`pi pi-stop-circle`) en lugar del botón deshabilitado «Montacargas en curso», y abre el mismo `ForkliftChargeDialog` de Montacargas. Las acciones posibles de la tabla son tres («Completar recepción», «Montacargas» y «Finalizar montacargas», las dos últimas excluyentes): siguen como botones de solo icono con tooltip (`AppRowActions`). El uso se busca sin cambiar el contrato: C-F04-18 con `status=InProgress`, la placa de la fila y `all=true`, y se elige el de su `serviceRecordId`. Si no aparece (otro usuario lo finalizó), un aviso «El uso del montacargas ya no está en curso.» y se refresca la lista. Al cobrar, el prefijo `['warehouse']` se invalida y la fila vuelve a mostrar «Montacargas» | H/ 1; C-F04-18 (`forkliftUseListQuerySchema`); `F/pages/warehouse/receptions/index.vue:62-89`, `:123-135` |
| D6 | **Sin los dos avisos del modal de recepción física.** Salen el texto junto a «Queda sobre el vehículo» (`F/features/warehouse/components/ReceptionDialog.vue:286-288`) y el párrafo bajo la cuadrilla (`:318-321`). Las reglas no cambian: las validaciones siguen diciendo lo que falta | H/ 2 |

### 1.3 Montacargas (hallazgos 3, 4 y 5)

| # | Decisión | Fuente |
| --- | --- | --- |
| D7 | **«+ Registrar uso» a la derecha de la barra.** `F/pages/warehouse/forklift/index.vue` deja de usar `create-label`: las pestañas «En curso» y «Finalizados» quedan solas a la izquierda (slot `toolbar`) y el botón «+ Registrar uso» (`size="small"`, `icon="pi pi-plus"`) va en `toolbarEnd` (D1) | H/ 3 |
| D8 | **Textos del modo de cobro** en `ForkliftChargeDialog` (`:184-188`): sin factura, «Sin IVA · pago inmediato»; con factura, «IVA del {tasa} % · pendiente por facturar». La regla de D25 y D3 de `P04/` no cambia (sin factura sigue siendo el registro interno «No aplica»; lo muestra F08) | H/ 4 |
| D9 | **Diálogo del cobro como el mockup** (`H/` 5; D4). Encabezado de dos líneas: el título «Facturación y cobro — Montacargas» y, debajo, la placa (negrita, monoespaciada) · cliente · depósito · inicio (sale el párrafo que hoy va dentro del contenido). Tres secciones con el mismo marco: **Uso** (horómetro inicial, horómetro final, horas · tipo; observaciones a lo ancho), **Cobro** (valor del servicio con su ayuda a la izquierda; «Requiere factura» y el texto de D8 a la derecha; una línea divisoria y el desglose valor · IVA · total alineado a la derecha) y **Destinatario y pago** (`AppChargeForm` sin cambios, con su total y su botón). El error del cobro sigue arriba. «Conductor del vehículo» sigue deshabilitado (`P04/` §8.5: el contrato no trae el documento) | H/ 5; mockup `../qa-manual/modal-facturacion-montacargas/screen.png` |

### 1.4 Inventario y Novedades (hallazgos 6, 7 y 8)

| # | Decisión | Fuente |
| --- | --- | --- |
| D10 | **Pestañas de Inventario en la tarjeta de la tabla** (ajusta `P04/` D42). Sale la barra de pestañas separada (`F/pages/warehouse/inventory/index.vue`, `<Tabs>` arriba de las tablas); cada una de las tres `AppDataTable` pinta las mismas pestañas en su slot `toolbar`, como Montacargas y el Historial de báscula. El marcado se escribe una vez en la página (un `v-for` sobre `TABS` dentro de cada slot, o un fragmento local) y la pestaña elegida se conserva al cambiar. En Existencias la tarjeta del depósito queda arriba (D2) | H/ 6 |
| D11 | **«Incluir anuladas» en la barra de Novedades.** Sale la tarjeta de filtros (`#globalFilters`); la casilla y su etiqueta van en `toolbarEnd` (D1), a la izquierda de «Limpiar filtros» y «Exportar». «+ Nueva novedad» sigue a la izquierda (`create-label`) | H/ 7 |
| D12 | **Ayuda de «Registro fotográfico»** (D3) en `NoveltyFormDialog` (`:366-369`): `<small class="text-muted-color">Referencia de las fotos: carpeta o números de foto.</small>` bajo el campo y `aria-describedby` en el input | H/ 8 |

---

## 2. Archivos que se tocan

| Archivo | Cambio | Decisión |
| --- | --- | --- |
| `F/components/app/AppDataTable.vue` | Slot `toolbarEnd` en el grupo derecho de la barra, antes de «Limpiar filtros»; en `defineSlots` | D1 |
| `FT/unit/components/AppDataTable.spec.ts` | Caso nuevo: el contenido de `toolbarEnd` se pinta en el grupo derecho, antes de «Exportar»; sin el slot, la barra no cambia | D1 |
| `F/pages/warehouse/receptions/index.vue` | Acción «Finalizar montacargas», búsqueda del uso en curso y `ForkliftChargeDialog`; sale el botón deshabilitado | D5 |
| `F/features/warehouse/composables/forklift.queries.ts` | `findInProgressUse(row)`: C-F04-18 con `status`, `vehiclePlate` y `all`, filtrado por `serviceRecordId` | D5 |
| `F/features/warehouse/components/ReceptionDialog.vue` | Salen los dos avisos | D6 |
| `F/pages/warehouse/forklift/index.vue` | «+ Registrar uso» en `toolbarEnd`; sin `create-label` | D7 |
| `F/features/warehouse/components/ForkliftChargeDialog.vue` | Textos del modo; encabezado de dos líneas; secciones Uso, Cobro y Destinatario y pago | D8, D9 |
| `FT/components/warehouse/ForkliftChargeDialog.spec.ts` | Los textos nuevos del modo | D8 |
| `F/pages/warehouse/inventory/index.vue` | Pestañas en el slot `toolbar` de cada tabla; sale la barra separada | D10 |
| `F/pages/warehouse/novelties/index.vue` | «Incluir anuladas» en `toolbarEnd`; sale `#globalFilters` | D11 |
| `F/features/warehouse/components/NoveltyFormDialog.vue` | Ayuda bajo «Registro fotográfico» | D12 |

---

## 3. Fuera de alcance

- Subir fotos a una novedad (D3): reabre §B.4.8 del plan de paridad y pide cambios de contrato y backend; si se quiere, va en un plan aparte.
- Mover «Finalizar y cobrar» al pie del modal (D4): pediría cambiar `AppChargeForm`.
- Habilitar «Conductor del vehículo» en el cobro: pide el documento del conductor en C-F04-18 (nota de `P04/` §8.5 para I-04).
- Sumar `forkliftUseId` a la fila de C-F04-06: D5 lo resuelve sin cambiar el contrato.

---

## 4. Fase única — Ajustes de UI

- **Contenido:** D1 a D12, en el orden de §2.
- **Verificación en el navegador** (`yarn dev` con la sesión simulada, `?roles=Admin,Warehouse`): en Recepción, iniciar un uso desde la fila, ver «Finalizar montacargas», cobrar y ver que la fila vuelve a «Montacargas»; el modal de recepción sin los dos avisos; Montacargas con las pestañas a la izquierda y «+ Registrar uso» a la derecha; el cobro con las tres secciones y los textos nuevos; Inventario con las pestañas dentro de la tarjeta de la tabla en las tres vistas; Novedades con «Incluir anuladas» junto a «Exportar» y funcionando; la ayuda de «Registro fotográfico». Sin llamadas al API ni errores en consola.
- **Capturas** en `D/planes/sprint-11/f04-bodega/evidencias/aui-*`: `aui-01` Recepción con «Finalizar montacargas»; `aui-02` modal de recepción; `aui-03` Montacargas; `aui-04` cobro; `aui-05` Inventario (Existencias y Movimientos); `aui-06` Novedades; `aui-07` formulario de novedad.
- **Criterio de salida:** los siete hallazgos y la duda resueltos como dicen D1 a D12, con su captura; compuertas de §5 en verde.
- **Estado:** hecha el 2026-11-25 (FE `f9f4da0`). `yarn build` con código 0; `yarn test` 150 archivos y 768 → 769 pruebas, todas en verde (sale con código 1 antes y después por el error no controlado heredado de `FT/components/weighbridge/WeighbridgeQueuePage.spec.ts`); las guardias en verde; `yarn lint` 209 → 209 errores, ninguno en los archivos tocados. Verificado en `yarn dev` con la sesión simulada: «Finalizar montacargas» desde la fila de Recepción cobra el uso y la fila vuelve a «Montacargas»; sin llamadas al API ni errores en consola. Capturas `evidencias/aui-01` a `aui-07` (Inventario en `aui-05a` y `aui-05b`).
- **D13:** hecha el 2026-11-25 (FE `09c0b87`). `yarn build` con código 0; `yarn test` 150 archivos y 769 pruebas en verde, con el mismo error heredado de F03; `yarn lint` 209 → 209 errores. La prueba de `ForkliftChargeDialog` espera el temporizador de 10 ms del aviso de éxito antes de desmontar: en una corrida dejaba un segundo error no controlado («document is not defined», `useWmsToast.ts:22`). Captura `evidencias/aui-08`.
- **Nota para I-04:** `findInProgressUse` (`F/features/warehouse/composables/forklift.queries.ts`) usa la fuente del montacargas; con `forklift.http.ts` llama a C-F04-18 con `status=InProgress`, `vehiclePlate` y `all=true`.

---

## 5. Pruebas y compuertas

- `yarn test` en verde (la base es 150 archivos y 768 pruebas; sale con código 1 por el error no controlado heredado de `FT/components/weighbridge/WeighbridgeQueuePage.spec.ts`, que no hace fallar ninguna prueba), con los casos nuevos de `AppDataTable.spec.ts` y los textos de `ForkliftChargeDialog.spec.ts`; las guardias de `FT/unit/guards/` en verde.
- `yarn lint` con 209 errores o menos y ninguno en los archivos tocados.
- `yarn build` con código 0.

---

## 6. Commits

| Repo | Mensaje |
| --- | --- |
| FE | `style(bodega): ajustes de UI de la maquetación de F04: montacargas desde Recepción, cobro por secciones y barras de las tablas (DEC-080, F04)` |
| docs | `docs(f04): ajustes de UI de la maquetación de F04 (sprint 11)` |

Cada uno termina con la línea de coautoría que indique la sesión.

---

## 7. Riesgos

| Riesgo | Mitigación |
| --- | --- |
| El slot nuevo cambia la barra de todas las tablas que usan `AppDataTable` | Es aditivo: sin contenido no pinta nada; la prueba cubre los dos casos y la guardia list-pattern sigue en verde |
| La búsqueda del uso por placa trae usos de otros servicios del mismo camión | Se filtra por `serviceRecordId` de la fila; si no hay coincidencia, aviso y refresco (D5) |
| Las pestañas repetidas en tres tablas se desalinean | Un solo marcado (D10) y la misma clase de estilo que Montacargas |
