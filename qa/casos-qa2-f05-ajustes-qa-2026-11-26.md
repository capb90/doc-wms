# Casos QA — Fase 2 · F05 «Comercio Exterior» · Ajustes de la QA manual de la integración

> **Para qué sirve:** los casos QA-AJQ5-001 a 025 del plan de ajustes de la QA manual de F05 integrado, con su resultado, copiados al cerrar la fase 4.
> **Plan:** [`planes/sprint-11/f05-comercio-exterior/plan-cerrado-f2-f05-ajustes-qa-2026-11-26.md`](../planes/sprint-11/f05-comercio-exterior/plan-cerrado-f2-f05-ajustes-qa-2026-11-26.md) (§5). Hallazgos de origen: [`planes/sprint-11/qa-manual/hallazgos-int-F05.md`](../planes/sprint-11/qa-manual/hallazgos-int-F05.md).
> **Fecha de corte:** 2026-11-26. Rama `f2/f05-ajustes-qa`: BE fase 1 `f076b2c` y fase 2 `7733035`; FE fase 3 `3cae866` y fase 4 `e707ae9`. Fusiones en `fase-2`: BE `dcb7b8f`, FE `4ed9400`.
> **Fuente:** el plan cerrado manda; esta copia no se edita salvo para registrar un re-test.
> **Verificación:** contra el API local de la rama (base `wmsdb`), sin la sesión simulada, con los usuarios de prueba locales por rol (Administrador, Báscula y Comercio Exterior; las contraseñas no se copian). El depósito de la QA es 2026BA00013 (`5f3749d2-6058-4f58-91e9-45d53f832b41`, legacy BA1452), con un solo levante (372024000009520, 640,13 de 1.920). Evidencias en `planes/sprint-11/f05-comercio-exterior/evidencias/ajq-f2-*`, `ajq-f3-*` y `ajq-f4-*`.

## 1. Casos

| ID | Hallazgo | Pasos | Resultado esperado | Verificación | Resultado |
| --- | --- | --- | --- | --- | --- |
| QA-AJQ5-001 | 1 | API con Báscula: C-F05AQ-01 con un nombre nuevo | 201; producto con SKU y `createdFromWeighbridge: true` | API (fase 1) | PASA (BE `f076b2c`) |
| QA-AJQ5-002 | 1 | Lo mismo con el nombre en otra capitalización | 200 con el mismo producto | API (fase 1) | PASA (BE `f076b2c`) |
| QA-AJQ5-003 | 1 | API con Comercio Exterior | 403 | API (fase 1) | PASA (BE `f076b2c`; también 403 con Facturación) |
| QA-AJQ5-004 | 6 | Detalle de un depósito con un levante parcial | `nationalizationStatus: "Nationalized"`; el producto sigue `Partial` | API (fase 1) | PASA con el depósito de la QA (BE `f076b2c`) |
| QA-AJQ5-005 | 8 | Tarjeta por vehículo de un camión del depósito de la QA | Manifiesto DIAN con fecha; «DATOS DE NACIONALIZACION» con el levante 372024000009520 y su aceptación | PDF (fase 2) | PASA (BE `7733035`; `ajq-f2-005-006-tarjeta-vehiculo.png`) |
| QA-AJQ5-006 | 8 | Etiqueta y tarjeta de un depósito sin unidades de carga | Sin la línea «Unidad(es) de carga» | PDF (fase 2) | PASA (BE `7733035`; `ajq-f2-006-etiqueta-deposito.png`) |
| QA-AJQ5-007 | 8 | Lo mismo con unidades | La línea con las unidades | PDF (fase 2) | PASA (BE `7733035`; `ajq-f2-007-*`) |
| QA-AJQ5-008 | 8 | PDF del depósito de la QA | Importador con su identificación; «Peso Kg.» con el P. mercancía de cada camión; «TOTAL PESO» 96.050; Entrada, Ampara y Saldo con la regla de D19 | PDF (fase 2) | PASA (BE `7733035`; 1.920, 1.920 y 0; `ajq-f2-008-pdf-deposito.png`) |
| QA-AJQ5-009 | 8 | Guía de salida de una salida (depósito sembrado por la prueba de integración) | Agencia sin el rol repetido; el tiquete de báscula de la salida (D20), no los de ingreso | Prueba de integración (fase 2) | PASA (`GuideExitTicketTests`; nota 1) |
| QA-AJQ5-010 | 8 | La misma guía | QR a la izquierda | Prueba de integración (fase 2) | PASA (`ajq-f2-009-012-guia-salida.png`; nota 1) |
| QA-AJQ5-011 | 8 | La misma guía | Dirección del importador si tiene contacto con dirección (si no, anotado como dato faltante) | Prueba de integración y base local (fase 2) | PASA como dato faltante: el importador del depósito de la QA (LUHOMAR) no tiene contactos; con un contacto activo, la guía imprime su dirección |
| QA-AJQ5-012 | 8 | La misma guía, con un producto de dos levantes | Levante y Aceptación con los dos | Prueba de integración (fase 2) | PASA (`GuideReleaseSnapshotTests`; nota 1) |
| QA-AJQ5-013 | 1 | Báscula, registro: escribir un nombre nuevo y pulsar «+» | Modal con el nombre; al crear, la línea queda con producto y embalaje | Navegador (fase 3) | PASA (FE `3cae866`; Báscula: 201 y la línea con «GARBANZO QA AJQ5» y Sacos; Administrador con el mismo nombre en minúsculas: 200 con el mismo producto) |
| QA-AJQ5-014 | 1 | Abrir la lista de productos | Cada opción con su embalaje | Navegador (fase 3) | PASA (FE `3cae866`) |
| QA-AJQ5-015 | 3 | Edición del ingreso: clic en el texto «Unidad de carga» y fuera del interruptor | No cambia; solo cambia al pulsar el interruptor | Navegador (fase 3) | PASA (FE `3cae866`) |
| QA-AJQ5-016 | 3 | Guardar la edición del ingreso | Sin campo de motivo; guarda y la auditoría muestra el motivo automático | Navegador (fase 3) | PASA (FE `3cae866`; nota 2) |
| QA-AJQ5-017 | 3 | Título de la edición | La placa en una etiqueta | Navegador (fase 3) | PASA (FE `3cae866`) |
| QA-AJQ5-018 | 2 | Comercio Exterior, etapa Entradas: «Ver pesaje» | Drawer con el pesaje, sin acciones; la página no cambia | Navegador (fase 4) | PASA (FE `e707ae9`; drawer «Detalle del ciclo de báscula» de PUB010 sin menú de acciones y la URL igual; `ajq-f4-018-drawer-pesaje-ce.jpg`) |
| QA-AJQ5-019 | 2 | Usuario con roles CE y Báscula (y Administrador): menú ⋮ de la fila | «Repesar» y «Anular pesaje»; «Repesar» abre el paso Repesaje de Báscula, «Anular pesaje» su diálogo, y al volver la etapa está al día | Navegador con Administrador (fase 4) y Vitest con CE + Báscula | PASA (FE `e707ae9`). Administrador en el navegador: el menú con los dos, el diálogo «Anular pesaje · 2026T00019 · PUB010» (cancelado, sin anular), el paso Repesaje de PUB010 (sin registrar) y, al volver, las cuatro consultas del depósito leídas de nuevo (`ajq-f4-019-*`). La combinación CE + Báscula se cubrió con Vitest (`DepositEntriesStage.spec.ts`, roles `ForeignTrade` + `Scale`): en la base local no hay un usuario con esos dos roles y no se creó (decisión del usuario del 2026-11-26) |
| QA-AJQ5-020 | 2 | Usuario solo con el rol CE: menú ⋮ de la fila | Sin «Repesar» ni «Anular pesaje» | Navegador (fase 4) | PASA (FE `e707ae9`; `ajq-f4-020-ce-sin-repesar-ni-anular.jpg`) |
| QA-AJQ5-021 | 4 | Encabezado de un depósito confirmado y de uno cerrado | Confirmado en verde y Cerrado en gris oscuro, también en las listas | Navegador y Vitest (fase 4) | PASA (FE `e707ae9`). Confirmado en verde en el navegador (`ajq-f4-021-022-023-encabezado.jpg`). La base local no tiene depósitos cerrados en ningún tipo: Cerrado (`p-tag-contrast`) se verificó con `DepositDetailHeader.spec.ts`. Las listas de depósitos no pintan el estado del depósito (cada pestaña es un estado; su columna «Estado» es el aduanero); el mismo mapa colorea la etiqueta del estado en la edición del ingreso (nota 3) |
| QA-AJQ5-022 | 4 | Información general | «Documento comercial» con tipo y número | Navegador (fase 4) | PASA (FE `e707ae9`; «Documento comercial: Carta Porte PE000843») |
| QA-AJQ5-023 | 6 | Encabezado del depósito de la QA (un levante) | «Nacionalizado»; nunca «Nacionalización parcial» | Navegador (fase 4) | PASA (FE `e707ae9`; también «Nacionalizado» con 33 % en la vista 2 de Levantes, `ajq-f4-023-vista2-nacionalizado.jpg`) |
| QA-AJQ5-024 | 7a | Etapa Levantes y vista 2 | Sin «Nuevo levante»; la fila editable sigue disponible | Navegador (fase 4) | PASA (FE `e707ae9`; `ajq-f4-024-025-etapa-levantes.jpg` y `ajq-f4-024-vista2-levantes.jpg`) |
| QA-AJQ5-025 | 7a | Fila editable | Botones separados | Navegador (fase 4) | PASA (FE `e707ae9`; `gap-2`, 0,5 rem entre «Guardar» y limpiar; antes `gap-1`) |

## 2. Notas

1. **Guía de salida (009 a 012).** La base local no tiene guías de salida y el depósito de la QA no tiene salidas; un segundo levante en él rompería 023. Por acuerdo con la sesión de integración del 2026-11-26, los cuatro casos se corrieron con la prueba de integración (Testcontainers), con la guía descargada por el API de la prueba y revisada. Ni el depósito de la QA ni la base local se tocaron.
2. **Auditoría del motivo automático (016).** Una corrección sin cambios no escribe fila de auditoría (el motivo es la descripción de las filas cambiadas). Se verificó con la fecha del manifiesto del ingreso ABC125 (2026BA00002), que se puso y se quitó en dos guardados.
3. **Colores del estado (021).** `DEPOSIT_STATUS_SEVERITY` (Borrador `secondary`, Confirmado `success`, Cerrado `contrast`, Anulado `danger`) lo usan el encabezado del depósito y la edición del ingreso.
4. **Datos que quedan.** El producto de prueba «GARBANZO QA AJQ5» (`createdFromWeighbridge`) queda en el catálogo local (fase 3). En la fase 4 no se guardó nada: el diálogo de anular se canceló y el paso Repesaje se abrió sin registrar. El depósito de la QA sigue con un solo levante.
5. **Permisos (D7b).** «Repesar» y «Anular pesaje» se ven con Admin o Báscula. El operario de Comercio Exterior que deba usarlos recibe además el rol Báscula en Usuarios; no cambiaron políticas, páginas ni menú.
