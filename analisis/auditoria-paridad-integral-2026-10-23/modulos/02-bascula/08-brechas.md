# 02-bascula — 08 Brechas

> AG-02 · 2026-10-23 · Estático. Antes de cada brecha se buscó ficha en `docs/qa/resultados/defectos/` (`INDICE.md`, 153 fichas; las de báscula son DEF-F3-001…019, DEF-F4-003, DEF-F8-003/008/009, DEF-F11-004/007…011/016/018/019/023…026), en `docs/planes/migracion-staging/resultados/defectos/DEF-MIG-*` y en `docs/contexto/estado.md` §4. Ninguna de las brechas siguientes tiene ficha propia; donde hay un riesgo del plan de QA o un caso sin ejecutar se cita.
> **PRF-002** (cronometraje ≤ 30 s, `estado.md` §4 n.º 1) sigue pendiente: no se registra como brecha nueva, se cita en la matriz (CF-L103) y no se da por validado.

## Resumen

| ID | Capacidad | Título | Categoría | Criticidad |
| --- | --- | --- | --- | --- |
| BR-02-001 | CF-L107 | La salida de báscula exige una orden de cargue previa | REGLAS_NEGOCIO | MEDIA |
| BR-02-002 | CF-L111 | Solo báscula exige un cliente registrado | REGLAS_NEGOCIO | MEDIA |
| BR-02-003 | CF-L116.e, CF-L103 | Sin tarifa configurada no se registra ni se cobra | REGLAS_NEGOCIO | BAJA |
| BR-02-004 | CF-L116.d, CF-L235 | No hay «otros servicios» en el cobro de báscula | FRONTEND / BACKEND | BAJA |
| BR-02-005 | CF-L115 | El tiquete dice «Numeración autorizada y/o habilitada por la DIAN» sobre un consecutivo interno | REGLAS_NEGOCIO | MEDIA |
| BR-02-006 | CF-L104, CF-L108, CF-V024 | Corregir un pesaje ≥ 2 en un ciclo con 3 o más pesajes modifica siempre el segundo | BACKEND / FRONTEND | ALTA |
| BR-02-007 | CF-L104, CF-L108, CF-L112 | El API permite corregir pesos, fecha y observación de un pesaje anulado | SEGURIDAD | BAJA |
| BR-02-008 | CF-L102 | Contratos del historial y del cobro desalineados (filtro «ID Ciclo» ignorado, campos inexistentes, nulos) | CONTRATOS_API | BAJA |
| BR-02-009 | CF-L115, CF-L121.a | Del contador de impresiones solo queda la primera, y la marca cualquier descarga | REGLAS_NEGOCIO | BAJA |
| BR-02-010 | CF-L104, CF-L108, CF-L112 | Báscula no puede editar el registro guardado (documento, mercancía, cantidad, destinatario, valor) | REGLAS_NEGOCIO | MEDIA |
| BR-02-011 | CF-L235 | Falta el aviso «el vehículo ya ingresó con este documento» | REGLAS_NEGOCIO | BAJA |
| BR-02-012 | CF-L105 | La anulación del pesaje agrega guardas que el legacy no tenía | REGLAS_NEGOCIO | BAJA |
| BR-02-013 | CF-L103.c | Un camión con varios documentos exige un pesaje intermedio por depósito | REGLAS_NEGOCIO | MEDIA |
| BR-02-014 | CF-L121.b | El reporte por documento (CPI) no tiene equivalente completo | FRONTEND | BAJA |
| BR-02-015 | CF-L114 | No hay repesajes adicionales después de cerrar el ciclo | REGLAS_NEGOCIO | BAJA |
| BR-02-016 | CF-LX02-01 | Alt+K ya no abre la salida | FRONTEND | BAJA |
| BR-02-017 | CF-L116.c | Quedan columnas de efectivo y cambio sin uso tras retirarlos | PERSISTENCIA | BAJA |
| BR-02-018 | CF-L235, CF-V022 | Endpoints, composables y una acción de báscula sin uso real | CONTRATOS_API | BAJA |

Por criticidad: CRÍTICA 0 · ALTA 1 · MEDIA 5 · BAJA 12.

---

### BR-02-001 · La salida de báscula exige una orden de cargue previa
- **ID funcional:** CF-L107 (R-23).
- **Descripción:** en el legacy, báscula registraba la salida del camión (tara) sin orden y Comercio Exterior la completaba después; en V2 no se puede iniciar la salida sin una orden de cargue existente.
- **Esperado (legacy):** `registrarsalida.php:104-105` crea `salida` «incompleto» sin orden; CE completa en `mod_salidas`.
- **Actual (V2):** `InitiateOutputWeighingValidator.cs:13-15` («El Id de la orden de cargue es requerido.») y `OutputInitiationRules.cs:14-21` (estado Pending/InProgress/Loaded y sin otro servicio de salida).
- **Capa:** backend y frontend (`OutputServiceForm.vue` busca la orden). **Categoría:** REGLAS_NEGOCIO.
- **Impacto:** si el camión llega antes que la orden, espera en la báscula. Afecta el flujo de salida.
- **Criticidad:** MEDIA — el flujo V2 está diseñado con la orden primero (DEC-016 conserva la orden de cargue) y QA lo recorrió sin queja (F3-SAL-001…005 PASA), pero no hay decisión que diga que el orden báscula → CE cambió.
- **Dependencias:** módulo 05 (orden de cargue).
- **Acción:** confirmar con el negocio; si se acepta, registrar la decisión en `docs/contexto/decisiones.md`.
- **Criterio de resolución:** decisión escrita que acepte «la orden antes de la salida», o un flujo V2 que permita pesar la salida y asociar la orden después.

### BR-02-002 · Solo báscula exige un cliente registrado
- **ID funcional:** CF-L111 (R-03).
- **Esperado:** `registrarsolopeso.php:117-125`: sin cliente, el recibo va al conductor.
- **Actual:** `Commands/WeighingOnly/Initiate/InitiateWeighingOnlyValidator.cs:13-15` («El Id del cliente es requerido.»); `WeighingOnlyForm.vue:73-74` cuenta el cliente como dato faltante. El cobro sí permite conductor o consumidor final como destinatario, pero el registro ya exigió un tercero.
- **Capa:** backend y frontend. **Categoría:** REGLAS_NEGOCIO.
- **Impacto:** un camión ocasional obliga a crear un tercero antes de pesar (tiempo en la báscula y terceros de relleno).
- **Criticidad:** MEDIA — servicio frecuente en la báscula, con alternativa (alta rápida de tercero, CF-V028).
- **Dependencias:** ninguna. QA: F3-SBA-002 PASA con la regla actual (`F3-informe-2026-10-02.md` §4), sin decisión del negocio.
- **Acción:** confirmar con el negocio si el cliente es obligatorio; si no, aceptar `customerId` nulo y usar el destinatario del cobro.
- **Criterio:** decisión escrita, o `POST weighbridge/weighing-only/initiate` sin `customerId` responde 200 y el cobro factura al conductor.

### BR-02-003 · Sin tarifa configurada no se registra ni se cobra
- **ID funcional:** CF-L116.e, CF-L103 (R-09).
- **Esperado:** sin tarifa, el operario digitaba valor e IVA («cobro no tarifado», `registrarentradabascula.php:162-167,470-480`).
- **Actual:** 400 «No se encontró tarifa para el servicio de báscula…» en `InitiateStorageWeighingHandler.cs:697-701` y en `ProcessStoragePaymentHandler.cs:167-172` (y equivalentes de salida y solo báscula), aunque el total es editable cuando hay tarifa (`:175-182`).
- **Capa:** backend. **Categoría:** REGLAS_NEGOCIO.
- **Impacto:** un error de configuración de BASCULA detiene todos los camiones. Hoy hay tarifa T3 aprobada (DEC-041), por eso el riesgo es bajo.
- **Criticidad:** BAJA — solo ocurre sin configuración; F3-COB-010 no ejecutado.
- **Acción:** confirmar con el negocio; opción: permitir total digitado > 0 cuando no hay tarifa, con aviso a Facturación.
- **Criterio:** decisión escrita, o un cobro con el servicio sin precio acepta un total digitado y deja aviso.

### BR-02-004 · No hay «otros servicios» en el cobro de báscula
- **ID funcional:** CF-L116.d, CF-L235 (R-10).
- **Esperado:** casillas con los servicios de tarifa vigente (`id_servicio > 1`) que se suman al recibo del pesaje (`consultaotrosservicios.php`; `registrarentradabascula.php:183-194,694-718`; igual en salida y solo pesaje).
- **Actual:** el cobro factura un solo ítem «Servicio de Báscula» (`ProcessStoragePaymentHandler.cs:205-214`). Búsqueda sin resultados de «otros servicios», «servicio adicional», `additionalService`, `extraService` en `Frontend/wms/app/features/{billing,weighbridge}`, `pages/operations` y `Wms.Application/Weighbridge`.
- **Capa:** frontend y backend. **Categoría:** FRONTEND / BACKEND.
- **Impacto:** un servicio extra cobrado en la báscula del legacy no tiene dónde cobrarse en V2, salvo los que tienen módulo propio (montacargas en Bodega, DEC-018; guía en CE, DEC-041 T4).
- **Criticidad:** BAJA — no se sabe qué servicios se cobraban así (datos en `db_legacy/`, no consultados); el plan frontend F1-01 lo da por fuera de alcance, pero la decisión citada (§A.3) solo retira la precarga de cliente y tarifa.
- **Acción:** confirmar con el negocio qué servicios se cobraban en báscula; si alguno sigue vigente, agregar ítems al cobro o documentar el módulo que lo cobra.
- **Criterio:** decisión escrita con la lista de servicios y dónde se cobra cada uno.

### BR-02-005 · Pie «Numeración autorizada y/o habilitada por la DIAN» en un consecutivo interno
- **ID funcional:** CF-L115 (R-11).
- **Esperado:** el legacy numeraba el tiquete con el rango de una resolución de facturación (`facturar.php:356-371`, tabla `resolucion_numeracion`), así que la leyenda tenía respaldo.
- **Actual:** el tiquete V2 usa el consecutivo interno `2026T00001` (DEC-012; `WeighbridgeService.cs:105-106`) y el número fiscal lo pone Facturación en SIIGO (DEC-024), pero el PDF imprime «Numeración autorizada y/o habilitada por la DIAN» (`Common/Services/WeighbridgeTicketPdfService.cs:414`) junto a «ORDEN DE PESO No.: 2026T…» (`:228`).
- **Capa:** backend (PDF). **Categoría:** REGLAS_NEGOCIO (leyenda legal).
- **Impacto:** el cliente recibe un documento que declara una numeración DIAN que no tiene. Riesgo fiscal o de reclamo.
- **Criticidad:** MEDIA — documento entregado a terceros en cada camión; el contenido del tiquete pasó QA (F3-TIQ-002 PASA) sin evaluar la leyenda.
- **Acción:** confirmar con Facturación o el contador; quitar la leyenda o reemplazarla por el texto que corresponda a un documento no fiscal.
- **Criterio:** el PDF de `GET weighbridge/{id}/ticket/pdf` no contiene la frase, o hay decisión escrita que la respalde.

### BR-02-006 · Corregir un pesaje ≥ 2 en un ciclo de 3 o más pesajes modifica siempre el segundo
- **ID funcional:** CF-L104, CF-L108, CF-V024.
- **Esperado:** corregir el pesaje elegido y recalcular el neto de cada depósito afectado (en multidepósito, el intermedio cierra un depósito y abre otro).
- **Actual:** la UI manda todo pesaje que no es el primero a `PATCH …/second-weight` (`features/weighbridge/components/ModifyWeighingDialog.vue:123-131`); el handler toma siempre la secuencia 1 (`ModifySecondWeightHandler.cs:62-63`) y recalcula el neto con los pesajes [0] y [1] solo en la primera entrada (`:73-84`). `ModifyFirstWeightHandler.cs:66-81` usa la misma fórmula. Es el riesgo R-BAS-09 del plan de QA (`docs/qa/00-plan-maestro.md:299`), caso F3-COR-006 **no ejecutado**; sin ficha DEF.
- **Capa:** backend y frontend. **Categoría:** BACKEND / FRONTEND.
- **Impacto:** en un camión con dos depósitos, corregir la tara final cambia en silencio el pesaje intermedio y deja netos incorrectos en los dos depósitos y en sus tiquetes.
- **Criticidad:** ALTA — corrompe datos de peso sin aviso en un flujo soportado (multidepósito, CF-L103.c); se limita a correcciones en ese caso.
- **Dependencias:** BR-02-013.
- **Acción:** corregir por `weighingId` (o por secuencia) y recalcular el neto de las entradas cuyo pesaje de entrada o salida cambió; prueba en `Wms.Tests`.
- **Criterio:** en un ciclo Bruto → Intermedio → Tara, corregir la tara cambia solo la secuencia 2 y el neto del segundo depósito; F3-COR-006 pasa.

### BR-02-007 · El API permite corregir un pesaje anulado
- **ID funcional:** CF-L104, CF-L108, CF-L112.
- **Esperado:** un pesaje anulado no se modifica (el legacy ocultaba Editar si `estado='eliminado'`).
- **Actual:** `ModifyFirstWeightHandler.cs`, `ModifySecondWeightHandler.cs:51-63`, `ModifyWeighingDateHandler.cs:50-69` y `UpdateTicketObservationsHandler.cs:17-25` no validan `WeighbridgeCyclesStatus.Canceled` ni `IsVoided`. Solo la UI oculta los botones (`history.vue:607,627`, `cycles/[id].vue:100`).
- **Capa:** backend. **Categoría:** SEGURIDAD (integridad).
- **Impacto:** una llamada directa altera un registro anulado y dispara avisos a Admin.
- **Criticidad:** BAJA — requiere llamada por API de un rol autorizado.
- **Acción:** rechazar con 409 «El pesaje está anulado.» en los cuatro handlers.
- **Criterio:** `PATCH weighbridge/{id}/second-weight` sobre un ciclo anulado responde 409.

### BR-02-008 · Contratos del historial y del cobro desalineados
- **ID funcional:** CF-L102.
- **Actual:**
  1. El filtro «ID Ciclo» (`WeighbridgeHistoryTable.vue:248-253`) envía `weighbridgeCycleId` (`requests.ts:336`); `GetWeighbridgeHistoryQuery.cs` y `WeighbridgeHistoryFilters.cs:9-25` no lo tienen: se ignora sin aviso.
  2. `IWeighbridgeHistory.netWeight` y `mode` (`weighbridge-cycle.ts:194,199`) no existen en `WeighbridgeHistoryDto.cs`; la UI cae a `netWeightKg` (`history.vue:99`, `WeighbridgeHistoryTable.vue:424`).
  3. `ProcessPaymentResponseDto.InvoiceNumber` puede ser nulo (factura sin N.º SIIGO, `ProcessStoragePaymentHandler.cs:188-192,273`) y el TS lo tipa `string` (`weighbridge-cycle.ts:354`).
- **Categoría:** CONTRATOS_API. **Criticidad:** BAJA — el filtro no hace nada; lo demás no rompe la pantalla.
- **Acción:** agregar el filtro al backend o quitarlo de la UI; limpiar los tipos.
- **Criterio:** filtrar por un Id de ciclo devuelve solo ese ciclo; los tipos TS coinciden con los DTO.

### BR-02-009 · Contador de impresiones reducido a la primera impresión
- **ID funcional:** CF-L115, CF-L121.a (R-29).
- **Esperado:** `contarimpresiones.php` suma `factura.impresiones` y avisa «La factura se ha impreso en N ocasion(es)» (`facturar.php:185-195`); el reporte muestra «# Impr.».
- **Actual:** solo `TicketFirstPrintedAt`, que se marca en cualquier descarga del PDF por un usuario autenticado (`WeighbridgeTicketPdfService.cs:92,136,144-149`; controlador `ActiveUser`, `WeighbridgeCycleReadController.cs:22-23`); el Excel muestra «# Impr.» como Sí/No (`history.vue:102`).
- **Categoría:** REGLAS_NEGOCIO. **Criticidad:** BAJA — sirve para «no impresos»; se pierde el control de reimpresiones.
- **Acción:** confirmar con el negocio; si hace falta, guardar cada impresión (como se hizo con las etiquetas, DECISIONES_REVISION §3.8).
- **Criterio:** decisión escrita, o el historial muestra el número de impresiones.

### BR-02-010 · Báscula no puede editar el registro guardado
- **ID funcional:** CF-L104, CF-L108, CF-L112 (R-22).
- **Esperado:** `modificarentradabascula.php:101-266` (y `modificarsalida.php`, `modificarsolopeso.php`) reescribía documento, conductor, transportadora, pesos, producto, embalaje, cantidad, fecha y valor del recibo mientras CE no asignaba productos.
- **Actual:** báscula corrige pesos con motivo (`WeighbridgeCorrectionController.cs:36,62`), fecha del pesaje (`WeighbridgeController.cs:885`) y observación del tiquete (`:916`), y datos del conductor/vehículo (`WeighbridgeSharedController.cs:35`). Documento, mercancía y cantidades los edita CE en Borrador (`Wms.Application/ForeignTrade/Commands/UpdateDepositProduct/`, `AddDepositProduct/`, `UpdateDraftDeposit/`); el destinatario o el valor del cobro no se cambian (D-2 retiró «Cambiar modo de pago», DEC-019). Lo demás exige anular y repetir. DEF-F3-018 (Verificado) dejó el registro guardado en solo lectura.
- **Categoría:** REGLAS_NEGOCIO. **Criticidad:** MEDIA — un error de digitación en báscula pasa a CE o a una anulación, con más pasos que en el legacy.
- **Acción:** confirmar con el negocio qué debe poder corregir báscula después de guardar.
- **Criterio:** decisión escrita con la lista de campos corregibles y quién los corrige.

### BR-02-011 · Falta el aviso «el vehículo ya ingresó con este documento»
- **ID funcional:** CF-L235 (R-16).
- **Esperado:** `consultaentroplaca.php` + `registrarentradabascula.php:393-406`: alerta y limpia el documento si el vehículo ya tiene un pesaje con ese ingreso.
- **Actual:** solo 409 cuando el **mismo ingreso de portería** ya tiene servicio o ciclo (`InitiateStorageWeighingHandler.cs:196-204`; `ProcessStoragePaymentHandler.cs:137-147`). Un segundo viaje del mismo vehículo con el mismo documento se asocia sin aviso.
- **Categoría:** REGLAS_NEGOCIO. **Criticidad:** BAJA — en V2 cada viaje es un ingreso distinto y el banner muestra «Camiones ingresados: N».
- **Acción:** confirmar con el negocio si se quiere el aviso.
- **Criterio:** decisión escrita o aviso en `DocumentMatchBanner.vue` cuando la placa ya está en las entradas del depósito.

### BR-02-012 · La anulación del pesaje agrega guardas que el legacy no tenía
- **ID funcional:** CF-L105 (R-06).
- **Esperado:** «Anular un pesaje completo: Sí, igual que el legacy» (DECISIONES_REVISION §2.D.12); el legacy anulaba sin revisar levantes, reservas ni salidas (`eliminarentrada.php:61-119`).
- **Actual:** 409 si la mercancía del camión está reservada o despachada, si los levantes no caben, si una unidad tiene reservas o si el tiquete ya sacó una orden (`VoidWeighingCommandHandler.cs:67-79,213-262`; `WeighingVoidGuard.cs`).
- **Categoría:** REGLAS_NEGOCIO. **Criticidad:** BAJA — es más segura y está en el plan F3-09, pero cambia lo que el negocio pidió «igual».
- **Acción:** confirmar con el negocio y registrar la decisión.
- **Criterio:** decisión escrita que acepte las guardas.

### BR-02-013 · Un camión con varios documentos exige un pesaje intermedio por depósito
- **ID funcional:** CF-L103.c (R-05).
- **Esperado:** `registrarentradavariascp.php:79-133`: varios documentos con **un solo** pesaje físico; cada documento con su peso de manifiesto; un cobro.
- **Actual:** «Agregar otro depósito» exige un pesaje `Intermediate` por cada depósito adicional antes del cierre (`RecordWeighingHandler.cs:133-140`); solo el flujo perecedero agrega depósitos sin pesaje nuevo (`:125-130`). Cobro único con facturas en $0 para los adicionales (`ProcessStoragePaymentHandler.cs:284-363`). DEF-F3-011 (Verificado) hizo alcanzable la acción; F3-MUL-002…004 quedaron bloqueados en la ejecución de F3.
- **Categoría:** REGLAS_NEGOCIO. **Criticidad:** MEDIA — más pesajes en la vía para un caso que el legacy resolvía en un paso (meta DEC-010 ≤ 30 s).
- **Dependencias:** BR-02-006.
- **Acción:** confirmar con el negocio si el camión con varios documentos descarga en un solo punto (sin pesaje intermedio); si es así, permitir varios depósitos sin intermedio fuera del perecedero.
- **Criterio:** decisión escrita, o un ciclo con dos depósitos se cierra con Bruto y Tara.

### BR-02-014 · El reporte por documento (CPI) no tiene equivalente completo
- **ID funcional:** CF-L121.b.
- **Esperado:** `reportecpi.php:247-356`: por documento, fecha, tiquete, placa, cantidad ingresada y peso de manifiesto, con totales, a Excel, PDF o impresora.
- **Actual:** el historial filtra por carta porte (`GetWeighbridgeHistoryQuery.CargoManifestNumber`) y exporta Excel con pesos y valores (`history.vue:91-117`), sin cantidad ni peso de manifiesto por tiquete y sin PDF; CE ve los camiones del depósito en su detalle (`features/foreign-trade/components/DepositDetailWeightsCard.vue`).
- **Categoría:** FRONTEND. **Criticidad:** BAJA — la información existe repartida.
- **Acción:** confirmar con el negocio si se usa; si sí, agregar las dos columnas al historial (o al detalle del depósito) y su exportación.
- **Criterio:** filtrar por un documento muestra por tiquete la cantidad y el peso de manifiesto con totales.

### BR-02-015 · No hay repesajes adicionales después de cerrar el ciclo
- **ID funcional:** CF-L114 (R-18).
- **Esperado:** «Repesar» siempre disponible; cada repesaje es un `pesaje` nuevo («N Reps.») (`repesarentrada.php:61-127`).
- **Actual:** el ciclo cierra con el pesaje opuesto al primero; otro pesaje responde 409 «El ciclo ya tiene todos los pesajes requeridos…» (`RecordWeighingHandler.cs:156-160,380-385`); el error se corrige con motivo (CF-V024).
- **Categoría:** REGLAS_NEGOCIO. **Criticidad:** BAJA — la corrección cubre el caso de error; se pierde el registro de pesajes repetidos reales.
- **Acción:** confirmar con el negocio.
- **Criterio:** decisión escrita.

### BR-02-016 · Alt+K ya no abre la salida
- **ID funcional:** CF-LX02-01.
- **Esperado:** Alt+K → `registrarsalida.php` (`entrada.php:20-21`).
- **Actual:** Alt+K → `/operations/weighbridge?cola=por-repesar` (`composables/useGlobalShortcuts.ts:23`); la salida se elige en la ficha del camión.
- **Categoría:** FRONTEND. **Criticidad:** BAJA — costumbre del operario; Alt+N sí lleva al banco.
- **Acción:** confirmar con el operario en la medición PRF-002.
- **Criterio:** decisión escrita o atajo ajustado.

### BR-02-017 · Columnas de efectivo y cambio sin uso
- **ID funcional:** CF-L116.c.
- **Esperado:** retirados «también del API» (§10 «Efectivo y cambio», 2026-10-02).
- **Actual:** el API ya no los expone (`Wms.Tests/Weighbridge/PaymentContractsTests.cs:10-46`; DEF-F3-019 Verificado), pero `InvoicePayment.CashReceived`/`ChangeGiven` y sus columnas siguen (`Wms.Domain/Entities/Billing/InvoicePayment.cs:29-31`; `InvoicePaymentConfiguration.cs:30-31`) sin escritura en ningún handler (búsqueda de `CashReceived|ChangeGiven` en `Wms.Application`, `Wms.Api`: sin resultados).
- **Categoría:** PERSISTENCIA. **Criticidad:** BAJA — código a medias, sin efecto funcional.
- **Acción:** quitarlas del modelo y generar la migración con `dotnet ef` (DEC-004), o documentar por qué se conservan.
- **Criterio:** `InvoicePayment` sin esas propiedades y `has-pending-model-changes` limpio.

### BR-02-018 · Endpoints, composables y una acción sin uso real
- **ID funcional:** CF-L235, CF-V022.
- **Actual:**
  - Sin consumidor ni decisión: `GET weighbridge/pending` (`WeighbridgeController.cs:518`), `GET pending-second-weight` (`:563`), `GET cycles/open-by-plate` (`:583`), `GET cycles/open` (`:601`), `GET {id}/invoice` (`:690`); composables sin uso `useWeighbridgePending.ts`, `usePendingSecondWeight.ts`, `useOpenCycleByPlate.ts`, `useOpenCycles.ts`, `useInitiateAdditionalDeposit.ts`. (`GET lookup` sin consumidor **a propósito**, plan frontend §A.3.)
  - «Cerrar ciclo» en `cycles/[id].vue:194-252` aparece cuando el último pesaje es el opuesto y envía `{ observations: null }`, que el backend rechaza fuera del perecedero (`CompleteCycleHandler.cs`, «FinalWeight y FinalWeightType son requeridos»). Riesgo R-BAS-10 del plan de QA, F3-CIC-004 no ejecutado.
- **Categoría:** CONTRATOS_API. **Criticidad:** BAJA — superficie muerta y un botón que solo produce un error.
- **Acción:** retirar o documentar los endpoints; quitar el botón o enviar el peso final.
- **Criterio:** `grep` de cada ruta en `Frontend/wms/app` da un consumidor o la ruta ya no existe; el botón no produce 400.


---

## Decisiones posteriores (2026-10-23)

> Nota del orquestador. Después de esta auditoría, el usuario respondió las preguntas al negocio (`docs/contexto/decisiones.md`, DEC-050…054; `06-brechas-priorizadas.md` §3.1). El registro de arriba es la foto previa y no se reescribe. El estado vigente está en `06-brechas-priorizadas.md` y `04-matriz-global.csv`.

| Brecha | Estado | Decisión |
| --- | --- | --- |
| BR-02-001 | Cerrada: se acepta el comportamiento de V2 | DEC-050 |
| BR-02-010 | Cerrada: se acepta el comportamiento de V2 | DEC-050 |
| BR-02-002 | Abierta: se construye (requiere plan cerrado) | DEC-050 |
| BR-02-013 | Abierta: se construye (requiere plan cerrado) | DEC-050 |
