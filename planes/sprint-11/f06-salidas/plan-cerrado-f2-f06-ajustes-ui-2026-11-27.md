# Plan cerrado — Fase 2 · F06 Salidas de mercancía · Ajustes de UI de la maquetación

> **Fecha:** 27 de noviembre de 2026. **Estado:** Aprobado por el usuario el 2026-11-27 («Aprobar»). Sin ejecutar: tres fases en `f2/f06-salidas` del frontend (§5), una por turno, antes de I-06.
> **Origen:** la revisión del usuario sobre la maquetación de F06 (FE-1 a FE-3, datos simulados; plan de F06 §8.6), antes de I-06: [`../qa-manual/hallazgos-UI-F06.md`](../qa-manual/hallazgos-UI-F06.md), con el mockup del formulario [`../qa-manual/rediseño-formulario-salida/`](../qa-manual/rediseño-formulario-salida/) (captura `Nueva salida — rediseño@1x.png`; valores de estilo en `Main.dc.html`), y las respuestas del usuario a la ronda de preguntas de este plan (2026-11-27), en D1 a D4.
> **Base:** FE `f2/f06-salidas` `1a45f7c` · docs `main` (este commit). Rama: `f2/f06-salidas` (FE). Se aplica antes de I-06.
> **Alcance:** solo frontend, sobre las pantallas maquetadas con datos simulados, en tres fases (§5). Sin cambios de backend, de contrato ni de migraciones: el listado de guías (C-F06-08) y el PDF de una guía (C-F06-09) se siguen usando, ahora desde la fila expandible y el Excel. Cambia la forma de P-CE-11, P-CE-08, P-BOD-06, P-BOD-09 y del drawer de la salida descrita en el plan de F06 (D3, D10, D11, D12, D14, D17, D20, D21 y §8.3 a §8.5): **donde chocan, gana este plan**.
> **Rutas:** relativas a `code_workspace/`. Prefijos: `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`; `P06/` = `D/planes/sprint-11/f06-salidas/plan-cerrado-f2-f06-salidas-2026-11-26.md`; `AUI5/` = `D/planes/sprint-11/f05-comercio-exterior/plan-cerrado-f2-f05-ajustes-ui-2026-11-26.md`; `H/` = el archivo de hallazgos, citado por su número (1 a 5); `MK/` = el mockup del formulario.

---

## 0. Instrucciones para el ejecutor

1. Lee `Frontend/wms/AGENTS.md` (sección «Eficiencia de contexto y cierres por fase»), este plan completo y, de `P06/`, §1 (con §1.9), §8.3 a §8.5 (cómo quedó cada pantalla) y §2.3 (esquemas). Las líneas citadas son de `f2/f06-salidas` `1a45f7c`; confírmalas con grep antes de cambiar.
2. Trabaja en `f2/f06-salidas` del frontend: trae antes lo último de `develop` a `fase-2` y de `fase-2` a la rama. Son tres fases (§5) y se ejecuta una por turno. Al cerrar cada una: compuertas de §6, commit con el mensaje de §7, push de la rama, el estado aquí (§5), en `P06/` §8 (fila «Revisión») y en la matriz; después te detienes con el reporte.
3. Sin llamadas reales: las páginas siguen en `MAQUETACION_PAGES`, con la sesión simulada (`NUXT_PUBLIC_MOCK_SESSION=true`; `?roles=Admin,ForeignTrade`, `?roles=ForeignTrade`, `?roles=Admin,Warehouse` y `?roles=Warehouse`) y sin enlaces del menú.
4. Compartidos: no cambian. `AppDataTable` (con `expandable`, `AUI5/` D34 de F05), `AppRowActions`, `AppDetailDrawer`, `AppDetailSection`, `AppSearchSelect`, `AppAlertIcon`, `DepositTableBlock` y `DepositStageCard` se usan como están. Si una pantalla necesita cambiar otro, detente y pregunta.
5. Del mockup se toman la distribución y el estilo (colores, tamaños, espaciados y radios, llevados a los tokens del tema). Los datos, los rótulos que dicen una regla y las reglas siguen siendo los de `P06/` y los de este plan, como en `AUI5/` §0.5.
6. Números con `F/shared/utils/format.ts` y cada `InputNumber` con `locale="es-CO"` (`P06/` D36). Lo cancelado y lo anulado, en su columna «Estado» con la fila en rojo tenue (`P06/` D35).
7. Commits en `docs`: otros agentes trabajan en paralelo y comparten el índice de git. Antes de commitear en docs, `git pull --rebase` (sin tocar cambios ajenos), `git diff --cached` vacío y commit con rutas explícitas (`git commit -- <tus archivos>`).

---

## 1. Decisiones

Mandan sobre el resto del plan (`DEC-002`).

### 1.1 Respuestas del usuario (2026-11-27)

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **Lo que falta va en el tooltip del estado.** Sin la columna «Falta» (D6, D16), en Salidas de CE y en la etapa Salidas la etiqueta del estado lleva un tooltip: «Confirmada» → «Falta: cargue y pesaje» (o lo que le falte; «Falta: salida de patio» en tiquete y global), y el Borrador creado en Báscula → «Creado en Báscula: complete tipo, depósitos y mercancía». Así se sigue cumpliendo AF-35 («indicar qué falta para completarlo») sin columna. En Órdenes de salida de Bodega no hace falta: la acción de la fila ya dice qué toca | Usuario: «Tooltip del estado (Recomendada)»; AF-35; H/ 1 y 4 |
| D2 | **«Exportar» con dos opciones.** El botón «Exportar» de Salidas pasa a un menú con «Salidas» (el Excel de hoy, C-F06-01 con `all=true`) y «Guías» (todas, vigentes y anuladas, con C-F06-08 y `all=true`, con las columnas del historial de guías de hoy: fecha, guía, cliente, placa, conductor, producto, cantidad, unidades de carga y modo de pago, más la salida y el estado). Conserva el Excel de guías que se perdía con la pestaña (`DEC-005`) | Usuario: «Exportar con dos opciones (Recomendada)»; `P06/` D11 |
| D3 | **«Ver guía» en el aviso de la guía de Bodega.** El aviso «Guía de salida {G} vigente» de «Ejecutar salida» (`ExitLoadingDialog`) y el de «Registrar salida de patio» (`YardExitDialog`) llevan un botón «Ver guía» (`pi pi-file-pdf`, pequeño, con borde) que abre el PDF de la guía vigente (C-F01-106). Sin guía (inspección), no aparece | Usuario: «En el aviso de la guía (Recomendada)»; `DEC-005`; H/ 4 |
| D4 | **El historial de Bodega tiene su versión del detalle.** «Ver» del historial abre el drawer de la salida con solo lo del operario: **Datos** (salida, tipo, placas, vehículo y su tipo, conductor, cliente y depósitos, guía vigente), **Mercancía** (depósito, producto con embalaje, cantidad y cargada, con el total) y **Registro de Bodega** (cargue: fecha, usuario, cuadrilla, observación y fotos; o salida de patio: fecha, usuario y observación). Menú «Acciones»: «Descargar guía». Sin saldos, peso asignado, orden del cliente, tiquetes, pesaje ni cancelación | Usuario: «Versión de Bodega (Recomendada)»; H/ 5 |

### 1.2 Salidas de Comercio Exterior (H/ 1)

| # | Decisión | Fuente |
| --- | --- | --- |
| D5 | **«+ Nueva salida» arriba a la derecha de la tabla, junto a «Exportar».** Los dos en la barra de la tabla (`#toolbar` de `AppDataTable`), a la derecha: el menú «Exportar» (D2) y «+ Nueva salida» (primario), en ese orden | H/ 1 |
| D6 | **Sin la columna «Falta».** Salidas queda con Salida, Fecha, Tipo, Estado (con el tooltip de D1), Depósitos, Placas, Guía y Acciones (`F/features/exits/components/ExitListTable.vue:57-64`, `:79`, `:135`). El reloj de Bodega deja de verse aquí: sigue en Órdenes de salida y en el drawer. La columna sale también del Excel de Salidas | H/ 1 |
| D7 | **Sin la pestaña «Guías».** Salidas es una sola tabla, sin pestañas (`F/pages/foreign-trade/exits/index.vue:34-44`, `:113-123`; sale `?vista=`). Las guías de cada salida se ven en su fila expandida (D9) y se exportan con D2. Reemplaza `P06/` D3 (c) y D11. Se borra `F/features/exits/components/GuideListTable.vue`, con su prueba | H/ 1 |
| D8 | **Anchos de columna automáticos.** Las tablas de salidas (Salidas, la etapa Salidas, Órdenes de salida y el historial) dejan de fijar anchos: se reparten solas. Solo la columna del botón de expandir y la de acciones llevan ancho, ajustado a su contenido (en Salidas y en la etapa, el botón «⋮» de `AppRowActions`, que agrupa las acciones porque pasan de tres) | H/ 1 |
| D9 | **Fila expandible con dos tablas, con el estilo de la fila expandida de Levantes.** Salidas usa `AppDataTable` con `expandable` (`AUI5/` D34 de F05). Al abrir una fila se leen el detalle (C-F06-02) y sus guías (C-F06-08 con `exitId` y `all=true`) y se muestran, con el marco y la tabla compacta de Levantes (`F/features/foreign-trade/components/ReleaseDepositExpansion.vue`, `DepositReleasesStage.vue:265-350`: `DepositTableBlock`, `release-table` y sus filas de total), dos bloques: **1. Mercancía** («{n} líneas»): Depósito, Producto (con embalaje), Cantidad, Cargada, Peso asignado, Saldo anterior y Nuevo saldo; al pie, la fila de total con el estilo de la fila «NACIONALIZADO» de Levantes (fondo de color, rótulo en mayúsculas pequeñas a la derecha): «TOTAL» con la suma de cantidad, cargada y peso asignado. **2. Guías** («{n} guías»): N.º de guía, Emitida, Fecha de salida, Vence, Firmante, Modo de pago, Estado («Vigente» o «Anulada», esta con la fecha y el motivo en el tooltip y la fila en rojo tenue, `P06/` D35) y las acciones de la guía con botones de solo icono: «Descargar guía» (C-F06-09, también la anulada), «PDF por depósito» (la vigente de una consolidada, C-F01-107) y «Cambiar modo de pago» (la vigente, C-F01-108). Sin guías, el bloque vacío dice «Sin guía en Borrador.» o «La inspección no lleva guía.». Un solo componente nuevo, `ExitExpansion`, lo usan Salidas y la etapa (D12) | H/ 1 y 3 |
| D10 | **El drawer de CE pierde Mercancía, Guía y Guías anuladas.** `F/features/exits/components/ExitDetail.vue` deja de mostrar esas tres secciones para CE (Mercancía `:113-151`, Guía `:169-180` y Guías anuladas `:182-199`; Tiquetes, `:153-167`, se queda): quedan Datos, Tiquetes, Bodega, Báscula y Cancelación. El menú «Acciones» del drawer no cambia (`P06/` D14): Editar, Descargar guía, PDF por depósito, Cambiar modo de pago, Anular guía o Reabrir salida, y Cancelar salida. Las acciones de la fila tampoco cambian (`P06/` D10). Esto aplica también al total de la Mercancía que pedía H/ 1: el total con el estilo de Levantes va en la fila expandida (D9) | H/ 1 |

### 1.3 Etapa Salidas del depósito (H/ 3)

| # | Decisión | Fuente |
| --- | --- | --- |
| D11 | **La etapa usa la misma fila expandida.** `F/features/foreign-trade/components/DepositExitsStage.vue` cambia su detalle expandido por `ExitExpansion` (D9): todas las líneas de la salida, con su depósito (en una consolidada se ven los dos depósitos), y sus guías. Sale el «Descargar guía» suelto del detalle de hoy: está en la tabla de guías. La fila no cambia salvo la columna del estado, que lleva el tooltip de D1 en lugar de «Estado / falta» | H/ 3; `P06/` D21 |

### 1.4 «Nueva salida» y «Editar» (H/ 2, MK/)

| # | Decisión | Fuente |
| --- | --- | --- |
| D12 | **Encabezado como el mockup.** Migas «Comercio Exterior / Salidas / Nueva salida» (o «Editar»); título visible «Nueva salida de mercancía» o «Editar salida {N}» (`h1`), con una etiqueta de estado al lado: «Sin guardar» o «Borrador · guardado {hora}» (la hora del último guardado de la sesión; al abrir un Borrador, su número). A la derecha, «Volver» y «Guardar borrador». El título visible sigue el precedente de la edición del ingreso (FE `6470ef6`, QA de F05); «Confirmar y emitir guía» deja la barra y va al resumen (D14) | MK/; H/ 2 |
| D13 | **Dos columnas: pasos a la izquierda, resumen a la derecha.** Desde `lg`, los pasos ocupan la columna principal y el resumen (D14) una columna angosta que se queda fija al desplazar; en pantallas pequeñas, el resumen va al final. **Cada paso es una tarjeta** con un círculo a la izquierda del título: el número del paso en gris (opcionales y sin empezar), en ámbar si le falta un dato para confirmar y un check verde si está completo; título y una línea de ayuda; la acción del paso a la derecha («Sacar todo», «+ Agregar orden»). **Pasos:** **1 Tipo de salida**: tres tarjetas de opción (la elegida con borde y fondo azul), con título y descripción según las reglas, no las del mockup: «Por tiquete de entrada · La mercancía de un tiquete de un camión que no descargó.»; «Global · Varios tiquetes de entrada de un depósito en una sola guía.» (el mockup dice «sin atarla a un ingreso puntual», que contradice AF-33); «Por número de depósito · Elija uno o más depósitos. Con dos o más, la salida queda consolidada.». **2 Depósitos**: «Solo aparecen depósitos confirmados con mercancía disponible.»; el buscador (C-F06-07) «Agregar depósito: número, documento o cliente…»; la etiqueta «Salida consolidada · {n} depósitos» con dos o más; cada depósito en una tarjeta (dos por fila): número, «{cliente} · {documento}», «{n} productos · {q} disponibles» y «✕»; los avisos de cliente faltante o bloqueado siguen con `AppAlertIcon` junto al número (`P06/` D12). **3 Tiquetes** (solo tiquete y global): como hoy (`ExitTicketsSection`), con el mismo marco. **4 Mercancía**: «Escriba cuánto sale de cada producto; el nuevo saldo se calcula solo.»; «Sacar todo» (llena cada línea con su tope); tabla Producto (con embalaje), Depósito, Unidad de carga (solo si un depósito las usa), Disponible (el tope: el menor entre disponible y nacionalizado disponible, D35 del plan de F01; si difieren, `AppAlertIcon` `info` con «Stock {s} · Nacionalizado {n}»), Sale (`InputNumber` alineado a la derecha) y Nuevo saldo (stock actual menos lo que sale; en 0, la etiqueta «0 · sale completo»); la línea en 0 va atenuada; al pie, «Total que sale · {k} de {n} productos» y la suma. **5 Transporte**: vehículo («{placa} · {tipo}»), conductor y empresa de transporte (opcional), en una fila, cada uno con su «+» al lado (`P06/` D12); bajo el que falte, «Requerido para emitir la guía». **6 Destino**: ciudad y dirección (opcional) en una fila, y debajo un aviso informativo con icono de calendario: «La guía vence el {fecha} · {d} días de tránsito a {ciudad}» (sin días de tránsito: «La guía vence el {fecha} · 30 días, la ciudad no tiene días de tránsito»). **7 Orden del cliente (opcional)**: «Correo o documento con que el cliente pide la salida.»; plegada con «+ Agregar orden» y, abierta, «Quitar orden», con emisor, fecha y soporte (`P06/` D9). **8 Observaciones**: «No se imprimen en la guía; las de la guía se escriben al confirmar.» (el mockup dice «Solo para la bodega», pero CE también las ve). Los números de paso se renumeran: sin tiquetes (por depósito), Transporte es el 4, como en el mockup | MK/; H/ 2; AF-28, AF-32, AF-33, AF-89; `DEC-002` |
| D14 | **Resumen y requisitos para confirmar.** La tarjeta «Resumen» muestra: Tipo («Por depósito · Consolidada», etc.), Depósitos (sus números), Sale («{q} · {n} productos»), Vehículo, Conductor («Sin asignar» en ámbar si falta), Destino y Vence guía. Debajo, «Para emitir la guía · {k} de {n}» con una barra de avance y la lista de requisitos, cada uno con su check verde o, si falta, el aviso en ámbar con «— ir al campo» (enlace que desplaza y lleva el foco al campo): Tipo de salida, Depósitos, Tiquetes (solo tiquete y global), Cantidades de mercancía, Vehículo, Conductor, Ciudad de destino y **Cliente en cada depósito** (sin cliente o con las salidas bloqueadas no se puede confirmar: C-F05-21 y BR-05-004; el mockup no lo lista). En inspección dice «Para confirmar la salida». Al pie, «Confirmar y emitir guía» («Confirmar salida» en inspección), deshabilitado hasta completar, con la nota «Se habilita cuando todos los requisitos estén completos.». Al pulsarlo guarda y abre `ExitConfirmDialog`, sin cambios (`P06/` D13). La regla de los requisitos va en `F/features/exits/utils/exit-form.ts`, pura y con su prueba | MK/; H/ 2; `P06/` D13; C-F05-21 |

### 1.5 Bodega (H/ 4 y 5)

| # | Decisión | Fuente |
| --- | --- | --- |
| D15 | **Órdenes de salida sin «Falta» ni «Ver».** Salen la columna «Falta» y su filtro (`F/pages/warehouse/exits/index.vue:42`, `:60`, `:145`) y la acción «Ver» (`:93`): cada fila tiene solo su acción, «Ejecutar salida» (depósito y consolidada) o «Registrar salida de patio» (tiquete y global). La consulta no cambia (`status=Confirmed&missing=Loading,YardExit`, `:47`). La página no abre el drawer | H/ 4 |
| D16 | **El historial abre la versión de Bodega del drawer** (D4). `ExitDetail` recibe la vista (`audience`: `foreignTrade` o `warehouse`) y arma sus secciones según ella; el historial pasa `warehouse`. Columnas y filtros del historial, como hoy (`P06/` D20) | H/ 5 |

### 1.6 Contrato y lo que se borra

- **Sin cambios de contrato ni de backend.** C-F06-08 deja de alimentar una pestaña y pasa a la fila expandida (`exitId`) y al Excel de guías (D2, D9); C-F06-09 se usa en la tabla de guías de la fila expandida. Los esquemas de `P06/` §2.3 no cambian.
- **Se borran** (con `rm`, comprobado con grep): `F/features/exits/components/GuideListTable.vue` (D7) y `ExitMissingTags.vue` si nadie más lo usa después de D1, D6 y D15, con sus pruebas.
- **Para I-06** (`P06/` §13): la fuente de guías (`guide.source.ts`) se integra igual; cambian los casos QA2-F06-032 (sin «Falta», con el tooltip y la fila expandida), 033 a 039 (el formulario de D12 a D14), 040 (el drawer de CE y el de Bodega), 042 (la tabla de guías de la fila expandida y el Excel de guías en lugar de la pestaña), 043 (la etapa con `ExitExpansion`), 044 y 045 (Órdenes de salida sin «Falta» ni «Ver», con «Ver guía» en el aviso) y 047 (el drawer de Bodega). I-06 los pasa con la forma de este plan y lo anota en `P06/` §6.2.

---

## 2. Contrato

Sin cambios (§1.6).

---

## 3. Archivos que se tocan

| Archivo | Cambio | Fase |
| --- | --- | --- |
| `F/pages/foreign-trade/exits/index.vue` | Sin pestañas; barra con «Exportar» (menú, D2) y «+ Nueva salida» (D5) | AUI-1 |
| `F/features/exits/components/ExitListTable.vue` | Sin «Falta»; estado con tooltip (D1); anchos automáticos (D8); fila expandible con `ExitExpansion` (D9); Excel sin «Falta» | AUI-1 |
| `F/features/exits/components/ExitExpansion.vue` (nuevo) | Las dos tablas de D9 con el estilo de Levantes | AUI-1 |
| `F/features/exits/components/GuideListTable.vue` | Se borra (D7); su lógica del Excel de guías pasa a una utilidad (`F/features/exits/utils/guide-export.ts`) | AUI-1 |
| `F/features/exits/components/ExitDetail.vue`, `ExitDetailDrawer.vue` | Sin Mercancía, Guía ni Guías anuladas para CE (D10); `audience` y la versión de Bodega (D4, D16) | AUI-1 (CE) y AUI-3 (Bodega) |
| `F/features/foreign-trade/components/DepositExitsStage.vue` | `ExitExpansion` en el detalle expandido; estado con tooltip; anchos (D8, D11) | AUI-1 |
| `F/features/exits/utils/exit-display.ts` | Texto del tooltip del estado (D1) | AUI-1 |
| `F/features/exits/components/ExitForm.vue` y sus secciones (`ExitDepositsSection`, `ExitTicketsSection`, `ExitLinesSection`, `ExitTransportSection`, `ExitCustomerOrderSection`) | Rediseño de D12 a D14; componentes nuevos `ExitFormStep` (la tarjeta del paso con su círculo) y `ExitFormSummary` (el resumen) | AUI-2 |
| `F/features/exits/utils/exit-form.ts` | Requisitos para confirmar, estado de cada paso, «Sacar todo», nuevo saldo y vencimiento (D13, D14) | AUI-2 |
| `F/pages/foreign-trade/exits/new.vue`, `[id]/edit.vue` | Encabezado de D12 | AUI-2 |
| `F/pages/warehouse/exits/index.vue` | Sin «Falta» ni «Ver» (D15); anchos (D8) | AUI-3 |
| `F/pages/warehouse/exits/history.vue` | Drawer de Bodega (D16); anchos (D8) | AUI-3 |
| `F/features/exits/components/ExitLoadingDialog.vue`, `YardExitDialog.vue` | «Ver guía» en el aviso de la guía (D3) | AUI-3 |
| `F/features/exits/composables/useExitActions.ts` | Sin «Ver» en Órdenes de salida; acciones de la tabla de guías | AUI-1 y AUI-3 |
| Pruebas (§6) y `D/planes/sprint-11/f06-salidas/evidencias/aui1-*`, `aui2-*`, `aui3-*` | — | Cada fase |

---

## 4. Fuera de alcance

- El backend y el contrato (§1.6); la integración (I-06).
- Guardar solo («autoguardado»): la etiqueta «guardado {hora}» del mockup informa el último guardado manual.
- Cambiar la convención «Páginas que no son listados» del hub: el título visible de D12 sigue el precedente de la edición del ingreso; si el usuario quiere llevarlo a la convención, va aparte.
- Los relojes de Bodega en Salidas de CE (salen con la columna, D6).

---

## 5. Fases

| Fase | Contenido | Criterio de salida | Estado |
| --- | --- | --- | --- |
| AUI-1 | Salidas de CE, la fila expandida, el Excel de guías, el drawer de CE y la etapa Salidas: D1, D2, D5 a D11 | Capturas `aui1-*` (la tabla, una fila expandida de una consolidada con una guía anulada, el menú «Exportar», el drawer y la etapa en la galería) | Pendiente |
| AUI-2 | «Nueva salida» y «Editar»: D12 a D14 | Capturas `aui2-*` (nueva vacía, por depósito consolidada a medio llenar con el resumen y sus avisos, global con tiquetes, inspección y el Borrador de Báscula) | Pendiente |
| AUI-3 | Bodega: D3, D4, D15, D16 | Capturas `aui3-*` (Órdenes de salida, «Ver guía» en los dos modales y el drawer del historial) | Pendiente |

Después de AUI-3, el usuario vuelve a revisar con la sesión simulada (`P06/` §8.6) y con su visto bueno sigue I-06.

---

## 6. Pruebas y compuertas

- Compuertas de `D/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md` §6.2 en cada fase, con las cifras antes y después: `yarn build` con código 0, `yarn test` en verde (guardias incluidas), `yarn lint` sin subir errores y sin errores en archivos nuevos, datos simulados validados con sus esquemas.
- **AUI-1:** `FT/components/exits/ExitListTable.spec.ts` (sin «Falta», tooltip del estado, fila expandida), `ExitExpansion.spec.ts` (nueva: las dos tablas, el total, la guía anulada en rojo tenue y sus acciones, los vacíos), `ExitDetail.spec.ts` (sin las tres secciones para CE), `FT/components/foreign-trade/DepositExitsStage.spec.ts` (con `ExitExpansion`), `FT/unit/exits/guide-export.spec.ts` (nueva: columnas del Excel de guías); se borra la prueba de `GuideListTable`.
- **AUI-2:** `FT/unit/exits/exit-form.spec.ts` (requisitos por tipo, cliente en cada depósito, estado de cada paso, «Sacar todo», nuevo saldo y «sale completo», vencimiento con y sin días de tránsito), `FT/components/exits/ExitForm.spec.ts` (pasos y renumeración, resumen, botón deshabilitado hasta completar, «ir al campo»).
- **AUI-3:** pruebas de `F/pages/warehouse/exits/index.vue` (sin «Falta» ni «Ver»), `ExitLoadingDialog.spec.ts` y `YardExitDialog.spec.ts` («Ver guía» con y sin guía), `ExitDetail.spec.ts` (vista de Bodega).

---

## 7. Commits

Cada uno termina con la línea de coautoría que indique la sesión.

| Fase | Repo | Mensaje |
| --- | --- | --- |
| AUI-1 | FE | `style(salidas): Salidas de CE sin «Falta» ni pestaña de guías, con fila expandible de mercancía y guías; drawer y etapa ajustados (DEC-080, F06, ajustes de UI)` |
| AUI-2 | FE | `style(salidas): formulario de nueva salida por pasos con resumen y requisitos para confirmar (DEC-080, F06, ajustes de UI)` |
| AUI-3 | FE | `style(salidas): órdenes de salida sin «Falta» ni «Ver», «Ver guía» en los modales y detalle de Bodega en el historial (DEC-080, F06, ajustes de UI)` |
| Cada fase | docs | `docs(f06): fase AUI-N de los ajustes de UI de F06 hecha (sprint 11)` |

---

## 8. Riesgos

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R1 | La fila expandida hace dos lecturas por fila abierta | Se leen al abrir, con la caché de TanStack Query por salida; como F05 en Levantes |
| R2 | Las acciones de la guía quedan en tres lugares (fila, drawer y tabla de guías) y divergen | Una sola fuente de acciones (`useExitActions`, `P06/` R5), con su prueba |
| R3 | El resumen de requisitos y el backend no coinciden (el botón se habilita y la confirmación falla) | La regla pura replica las validaciones de C-F01-98 y C-F05-21; si el backend rechaza, el error se muestra en el modal como hoy (`P06/` D13) |
| R4 | El formulario rediseñado pierde una regla de `P06/` D12 (topes, tiquetes en otra salida, avisos de cliente) | §0.5: del mockup solo la distribución y el estilo; las pruebas de `exit-form.ts` de FE-2 siguen en verde y se amplían |
| R5 | Los casos de I-06 quedan desalineados con las pantallas | §1.6 lista los que cambian; I-06 los pasa con esta forma |
