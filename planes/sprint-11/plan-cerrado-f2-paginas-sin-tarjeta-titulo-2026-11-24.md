# Plan cerrado — Fase 2 · Páginas sin tarjeta de título (tableros, formularios y reportes)

> **Fecha:** 24 de noviembre de 2026. **Estado:** Aprobado por el usuario el 2026-11-24 («Aprobar»). Se ejecuta después de I-03 (D4).
> **Origen:** pedido del usuario del 2026-11-24. Varias páginas conservan la tarjeta de título y subtítulo (`AppPageHeader`, `DEC-058`): `/operations/weighbridge/dashboard`, `/operations/entries`, `/operations/entries/exits`, Trazabilidad, Notificaciones y los reportes. AF-129 quitó esa tarjeta solo en los **listados** (`levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md` §3.1, «Listados»). La guardia `FT/unit/guards/list-pattern-routes.ts` deja las demás páginas en `OUTSIDE`, sin regla, y ninguna fase las cambia. Las respuestas del usuario del 2026-11-24 están en D1 a D4.
> **Base:** FE `fase-2` después de fusionar I-03 (el hash se anota al crear la rama). Rama: `f2/ui-paginas-sin-tarjeta`.
> **Alcance:** solo frontend, solo el encabezado de cada página. Sin cambios de backend, de contrato, de datos ni de comportamiento.
> **Rutas:** relativas a `code_workspace/`. Prefijos: `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`; `PAJ/` = `D/planes/sprint-11/f02-base/plan-cerrado-f2-f02-ajustes-qa-2026-11-24.md`.

---

## 0. Instrucciones para el ejecutor

1. **Lecturas mínimas:** `Frontend/wms/AGENTS.md`, `D/procesos/flujo-de-trabajo-agentes.md`, `D/contexto/convenciones-tecnicas.md` §3 (patrón de listado, drawer y tablas) y este plan completo.
2. **Rama y git:** empieza solo cuando I-03 esté fusionada en `fase-2`. `git fetch`; crea `f2/ui-paginas-sin-tarjeta` desde `fase-2` y anota su hash en la cabecera. Commit al cerrar cada fase con el mensaje de §7 y push de la rama. Al cerrar la fase 2 y pasar las compuertas, fusiona en `fase-2` con `--no-ff` y push. Sin `push --force`.
3. **Líneas citadas:** son de `f2/f03-bascula` `ee3d5d9`. I-03 toca `F/pages/operations/weighbridge/dashboard.vue` (sus enlaces) y quizá otras: confírmalas con grep. Si el código no coincide con lo que dice este plan, pregunta en un solo mensaje.
4. **Componentes compartidos:** `AppPageHeader` no se cambia ni se borra. Lo siguen usando los listados `PENDING` (F04 a F09) y los reportes de Facturación (F08). Se borra cuando su último uso desaparezca.
5. **Convenciones:** las de `Frontend/wms/AGENTS.md`. Estilos con utilidades de Tailwind y tokens de PrimeVue, sin colores fijos.
6. **Verificación:** backend local y `yarn dev`, con un usuario Admin (ve todas las páginas). Cada página se revisa en ancho normal y angosto (768 px), con captura.

---

## 1. Decisiones

### 1.1 Respuestas del usuario (2026-11-24)

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **Sin tarjeta de título y sin nada visible en su lugar.** El breadcrumb ya nombra la página. Cada página conserva un `<h1 class="sr-only">` con su título para los lectores de pantalla, y las acciones de la tarjeta se mueven según D5 a D7 | Usuario: «Nada visible (Recomendada)» |
| D2 | **Los subtítulos se eliminan, salvo los que explican una regla del reporte.** Esos pasan a una línea de texto pequeño y atenuado (`text-sm text-muted-color`) al pie de la tarjeta de filtros. Son tres: <br>• Mercancía en abandono: «Productos de depósitos de importación con 30 días o más sin prórroga, o 60 o más con prórroga.» <br>• Salidas a destino de abandono: «Salidas cargadas hacia ciudades marcadas como destino de abandono en Administración › Ciudades.» <br>• Informe de póliza: «Valor CIF de los levantes (USD), por mes, para UAP y no UAP.» <br>Los demás subtítulos solo describen la página y salen | Usuario: «Texto atenuado en filtros (Recomendada)» |
| D3 | **Alcance: todas las páginas que no son listados, menos las que otra fase rehace** (§2). Quedan fuera: <br>• Facturación anual y Facturación por CPI (`/billing/reports/annual`, `/billing/reports/deposit-billing`): F08 las rehace (P-FAC-09 y P-FAC-10); <br>• Notificaciones (`/notifications`): es un listado `PENDING` de F09; <br>• los formularios de creación de órdenes de cargue y guías, que F06 retira (AF-97) y que no usan `AppPageHeader`; <br>• el centro de ayuda (`/ayuda`), que tiene su propio layout. <br>F08 y F09 aplican la convención de D8 al rehacer sus páginas | Usuario: «Todo menos lo que se rehace (Recomendada)» |
| D4 | **Después de I-03**, en la rama `f2/ui-paginas-sin-tarjeta` desde `fase-2`, fusionada en `fase-2` con `--no-ff` al pasar las compuertas. No se mezcla con la integración de Báscula | Usuario: «Después de I-03 (Recomendada)» |

### 1.2 Dónde quedan las acciones

| # | Decisión | Fuente |
| --- | --- | --- |
| D5 | **Reportes:** las acciones de la tarjeta («Exportar Excel», «Descargar PDF») pasan a la fila de botones de la tarjeta de filtros, a la derecha (`ml-auto`), después de «Consultar» o «Generar». Conservan su tamaño, su `severity`, su `loading` y su `disabled` de hoy | D1 |
| D6 | **Páginas sin tarjeta propia donde poner las acciones:** las acciones van en una barra sin tarjeta, alineada a la derecha, arriba del contenido (`flex flex-wrap items-center justify-end gap-2`). Son tres páginas: <br>• Trazabilidad: «Actualizado hace …» y el selector de fechas (`DateFilterSelector`); <br>• Camiones en planta: el contador y «Actualizar»; <br>• Montacargas: «Iniciar uso» | D1 |
| D7 | **Páginas sin acciones en la tarjeta:** solo se quita la tarjeta. Son los tableros de Báscula, Bodega, Comercio Exterior y Facturación, Registro de ingreso e Informe de movimientos por depósito | D1 |
| D8 | **La convención y la guardia quedan escritas.** <br>• **Convención:** un apartado «Páginas que no son listados» en `D/contexto/convenciones-tecnicas.md` §3, con D1, D2, D5 y D6. <br>• **Guardia:** `FT/unit/guards/list-pattern.spec.ts` suma dos reglas: <br>  – ninguna ruta de `OUTSIDE` usa `AppPageHeader`, salvo las de una lista nueva `TITLE_CARD_PENDING` (en `list-pattern-routes.ts`), cada una con la fase que la rehace: los dos reportes de Facturación (F08); <br>  – las páginas de §2 tienen un `<h1`. <br>Una página nueva que no sea listado entra a `OUTSIDE` y cumple la regla desde el principio | `PAJ/` D15 (convención escrita) |

---

## 2. Páginas

| Ruta | Archivo | Tarjeta de hoy | Qué cambia | Fase |
| --- | --- | --- | --- | --- |
| `/` | `F/pages/index.vue:76-91` | «Trazabilidad»; indicador de actualización y `DateFilterSelector` | Barra de D6 | 1 |
| `/operations/weighbridge/dashboard` | `F/pages/operations/weighbridge/dashboard.vue:50-53` | «Báscula», sin acciones | D7 | 1 |
| `/warehouse` | `F/pages/warehouse/index.vue:78-81` | Sin acciones | D7 | 1 |
| `/foreign-trade` | `F/pages/foreign-trade/index.vue:52-55` | Sin acciones | D7 | 1 |
| `/billing` | `F/pages/billing/index.vue:59` | Sin acciones | D7 | 1 |
| `/operations/entries` | `F/pages/operations/entries/index.vue:254-257` | «Registro de ingreso», sin acciones | D7 | 1 |
| `/operations/entries/exits` | `F/pages/operations/entries/exits.vue:127-151` | «Camiones en planta»; contador y «Actualizar» | Barra de D6 | 1 |
| `/warehouse/forklift` | `F/pages/warehouse/forklift/index.vue:67-79` | «Registrar Uso de Montacargas»; «Iniciar Uso» | Barra de D6 | 1 |
| `/operations/weighbridge/reports` | `F/pages/operations/weighbridge/reports.vue:77-91` | «Descargar PDF» | D5 (filtros en `:94`) | 2 |
| `/reports/abandonment-candidates` | `F/pages/reports/abandonment-candidates.vue:90-104` | «Exportar Excel»; subtítulo con regla | D5 y D2 | 2 |
| `/reports/abandonment-exits` | `F/pages/reports/abandonment-exits.vue:102-117` | «Exportar Excel»; subtítulo con regla | D5 y D2 | 2 |
| `/reports/customs-agency-entries` | `F/pages/reports/customs-agency-entries.vue:104-119` | «Exportar Excel» | D5 | 2 |
| `/reports/daily-incoming-goods` | `F/pages/reports/daily-incoming-goods.vue:167-191` | «Descargar PDF» y «Exportar Excel» | D5 | 2 |
| `/reports/daily-outgoing-goods` | `F/pages/reports/daily-outgoing-goods.vue:204-228` | «Descargar PDF» y «Exportar Excel» | D5 | 2 |
| `/reports/general-inventory` | `F/pages/reports/general-inventory.vue:150-165` | «Exportar Excel» | D5 | 2 |
| `/reports/incoming-by-product` | `F/pages/reports/incoming-by-product.vue:102-117` | «Exportar Excel» | D5 | 2 |
| `/reports/policies` | `F/pages/reports/policies.vue:148-163` | «Exportar Excel»; subtítulo con regla | D5 y D2 | 2 |
| `/reports/warehouse-movements` | `F/pages/reports/warehouse-movements.vue:255-258` | Sin acciones | D7 | 2 |

Cada página pone el `<h1 class="sr-only">` con el título de su tarjeta de hoy (D1), quita el import de `AppPageHeader` y conserva su raíz `.wms-page`. Ninguna usa `backTo` (revisado en `ee3d5d9`); si I-03 agrega uno, el ejecutor se detiene y pregunta.

---

## 3. Archivos que se tocan

| Archivo | Fase | Cambio |
| --- | --- | --- |
| Las 8 páginas de la fase 1 en §2 | 1 | D1, D6, D7 |
| `FT/unit/guards/list-pattern-routes.ts`; `FT/unit/guards/list-pattern.spec.ts` | 1 | D8: `TITLE_CARD_PENDING` y las dos reglas; en la fase 1 la regla del `<h1` y la de `AppPageHeader` cubren las páginas de la fase 1, y los reportes de la fase 2 van, mientras tanto, en `TITLE_CARD_PENDING` con «fase 2 de este plan» |
| Las 10 páginas de la fase 2 en §2 | 2 | D1, D2, D5, D7 |
| `FT/unit/guards/list-pattern-routes.ts` | 2 | Salen de `TITLE_CARD_PENDING` los reportes de la fase 2; quedan los dos de F08 |
| Pruebas de esas páginas | 1 y 2 | En `ee3d5d9` ninguna prueba mira su tarjeta (`FT/unit/layout/app-menu.spec.ts` cita los nombres del menú, no los encabezados). Si I-03 agrega alguna, se ajusta al `<h1>` oculto |
| `D/contexto/convenciones-tecnicas.md` §3 | 2 | D8 |

---

## 4. Fases

| Fase | Contenido | Criterio de salida | Estado |
| --- | --- | --- | --- |
| 1 | Trazabilidad, los cuatro tableros, Ingreso y Salida de Vigilancia, Montacargas y la guardia | Compuertas de §6; QA-PST-001 a 005 en PASA | Pendiente |
| 2 | Los diez reportes, la convención y la fusión en `fase-2` | Compuertas; QA-PST-006 a 009 en PASA; fusión hecha y publicada | Pendiente |

---

## 5. Pruebas y casos QA

**Vitest:** la guardia (D8) falla si una página de §2 vuelve a usar `AppPageHeader` o pierde su `<h1>`. `FT/components/app/AppPageHeader.spec.ts` se conserva: el componente sigue en uso (§0.4).

**Casos QA** (navegador, backend local, Admin):

| Caso | Pasos | Resultado esperado |
| --- | --- | --- |
| QA-PST-001 | Trazabilidad: cambiar el rango de fechas y esperar una actualización | Sin tarjeta; la barra muestra «Actualizado hace …» y el selector a la derecha; el filtro funciona como hoy |
| QA-PST-002 | Tableros de Báscula, Bodega, Comercio Exterior y Facturación | Sin tarjeta; los indicadores y enlaces de hoy, sin cambios |
| QA-PST-003 | Vigilancia › Ingreso: registrar un ingreso de prueba (placa `QA-`) | Sin tarjeta; el formulario funciona como hoy |
| QA-PST-004 | Vigilancia › Salida: «Actualizar» y el contador | En la barra, a la derecha; funcionan como hoy |
| QA-PST-005 | Montacargas: «Iniciar uso» | En la barra; abre el diálogo de hoy |
| QA-PST-006 | Reporte de báscula y los dos informes diarios: consultar y descargar PDF y Excel | Botones en la tarjeta de filtros, a la derecha; descargan como hoy |
| QA-PST-007 | Mercancía en abandono, Salidas a destino de abandono e Informe de póliza | La regla del subtítulo, en texto atenuado al pie de los filtros; «Exportar Excel» en los filtros |
| QA-PST-008 | Los otros cuatro reportes: consultar y exportar | Sin tarjeta; exportan como hoy |
| QA-PST-009 | Una página de cada fase con un lector de pantalla o el árbol de accesibilidad | El `<h1>` oculto nombra la página |

---

## 6. Compuertas de cada fase

- `yarn build` con código 0.
- `yarn test` en verde; base: la de `fase-2` al crear la rama.
- `yarn lint` sin subir los errores de la base y sin ninguno en archivos tocados.
- Capturas de los casos de la fase, en ancho normal y angosto.

---

## 7. Commits

| Fase | Repo | Mensaje |
| --- | --- | --- |
| 1 | FE | `style(ui): tableros, Vigilancia y montacargas sin tarjeta de título (DEC-080, AF-129)` |
| 2 | FE | `style(reportes): reportes sin tarjeta de título, con sus acciones en los filtros (DEC-080, AF-129)`, y la fusión `merge: páginas sin tarjeta de título en fase-2` |
| 2 | docs | `docs(convenciones): páginas que no son listados; cierre del plan de páginas sin tarjeta de título` |

Al cerrar: el estado de este plan y su fila en `D/planes/README.md`; una línea en `D/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md` §3 con los commits.

---

## 8. Riesgos

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R1 | Sin título visible, un usuario no sabe en qué reporte está | El breadcrumb lo nombra (D1); QA-PST-009 revisa el `<h1>` oculto |
| R2 | Una acción movida pierde su `disabled` o su `loading` | D5: se conservan tal cual; QA-PST-006 y 008 descargan y exportan |
| R3 | F08 o F09 rehacen sus páginas con la tarjeta | D8: convención y guardia con `TITLE_CARD_PENDING` |
| R4 | I-03 cambia el tablero de Báscula y desplaza las líneas | §0.3: confirmarlas con grep al empezar |
