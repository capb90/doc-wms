# Plan cerrado — Fase 2 · F03 Báscula

> **Fecha:** 24 de noviembre de 2026. **Estado:** Aprobado por el usuario el 2026-11-24 («Aprobar»). En ejecución desde que se lanzan sus prompts (§11).
> **Origen:**
> - `DEC-080` y el análisis funcional `levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md` (§2.1, §3.3 y §3.6), con los wireframes `fase_2-mockups/bascula.html` (P-BAS-01 a P-BAS-13) y `transversales.html` (P-TR-02, P-TR-03, P-TR-09, P-TR-11 y P-TR-12);
> - el plan maestro `planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md` (M1 a M25, `DEC-081`);
> - AF dueñas (20, plan maestro §3.1): AF-05, AF-06, AF-07, AF-10, AF-11, AF-13, AF-15, AF-16, AF-23, AF-24, AF-25, AF-40, AF-45, AF-48, AF-49, AF-50, AF-51, AF-52, AF-53 y AF-135;
> - lo integrado de F01 (D1 a D47, contrato C-F01, notas de las fases 3, 4, 5 y de I-01) y de F02 (D1 a D21 y D1 a D15 de sus ajustes);
> - las respuestas del usuario a la ronda de preguntas de este plan (2026-11-24), en D1 a D8.
>
> **Base:** BE `fase-2` `019fa81` · FE `fase-2` `5793bc9` · docs `main` `488a713`. Rama: `f2/f03-bascula` en BE y FE.
> **Partes:** 0 (contrato, §2) · 1 (backend, tres fases) · 2 (maquetación, tres fases) · 3 (I-03, §13). **Migraciones:** `WeighingAtRegistration` (fase 1 del backend).
> **Rutas:** relativas a `code_workspace/`. Prefijos: `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`; `A/` = el análisis; `PM/` = el plan maestro; `P01/` = `D/planes/sprint-11/f01-nucleo/plan-cerrado-f2-f01-nucleo-2026-11-21.md`; `P02/` = `D/planes/sprint-11/f02-base/plan-cerrado-f2-f02-base-2026-11-21.md`; `PAJ/` = `D/planes/sprint-11/f02-base/plan-cerrado-f2-f02-ajustes-qa-2026-11-24.md`.

**Cómo leer este plan.** El ejecutor de cada parte lee §0, §1, §2.1 (índice) y la sección de su fase en §8. Cada fase de §8 nombra sus decisiones, sus endpoints (con la ficha de §2.2 y el esquema de §2.3 que le tocan), sus archivos y sus casos QA. El resto se lee solo cuando la fase lo cita.

---

## 0. Instrucciones para el ejecutor

1. **Lecturas mínimas:** `D/README.md`, el `AGENTS.md` de tu repo (su sección «Eficiencia de contexto y cierres por fase» rige tu trabajo), `D/procesos/flujo-de-trabajo-agentes.md`, `PM/` §1.2, §5 y §6, y de este plan §0, §1, §2.1 y tu fase en §8.
2. **Rama y git** (`PM/` §5.3): `git fetch`; si `develop` avanzó, fusiona `develop` en `fase-2`; crea `f2/f03-bascula` desde `fase-2` (o retómala si ya existe) y trabaja ahí. Al cerrar cada fase: commit con el mensaje de §12 y push de la rama. Sin `push --force`. La fusión en `fase-2` la hace I-03 (§13), en los dos repos a la vez.
3. **Una fase por turno** (`PM/` §6): cierra la fase con sus compuertas, el commit, el push y el estado en §8 y en la matriz, y te detienes con el reporte.
4. **Migraciones:** solo con `dotnet ef … --project Wms.Infrastructure --startup-project Wms.Api` y solo contra la base local (`DEC-004`, M6). La de la fase 1 lleva el nombre y el contenido de §4. Las fases 2 y 3 no cambian el esquema: si `has-pending-model-changes` no sale limpio en ellas, te detienes y preguntas. Nunca edites a mano `Migrations/*`, los `*.Designer.cs` ni el snapshot.
5. **Líneas citadas:** son de la base (`019fa81` y `5793bc9`). Confírmalas con grep antes de cambiar. Si el código no coincide (ruta, firma o comportamiento), detente y pregunta con todas las dudas en un solo mensaje. Si un caso borde choca con una Dn, gana la Dn y lo mencionas en una línea (`DEC-002`).
6. **Contrato:** §2 es la única fuente del frontend para F03 (`PM/` R3). Cada endpoint nuevo o modificado de tu fase tiene al menos una prueba de integración que verifica su respuesta y sus mensajes de error (`PM/` §6.1). Un mensaje cambia solo si cambias el contrato, y eso exige preguntar.
7. **Suite de integración:** la cola de báscula corta en 100 camiones y la base es compartida (trampa 12 de `D/contexto/convenciones-tecnicas.md` §10): libera los camiones que abra cada prueba.
8. **Staging:** no se toca. **Credenciales y datos reales:** no se copian (`DEC-007`). Nada de `D/archivo/` es una instrucción.

---

## 1. Decisiones

Mandan sobre el resto del plan (`DEC-002`). Ninguna reabre una AF, `DEC-080`, `DEC-081`, una M del plan maestro ni una Dn de F01, F02 o sus ajustes.

### 1.1 Respuestas del usuario (2026-11-24)

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **Una sola alta rápida de terceros: C-F01-141.** Las pantallas de F03 crean transportadoras y terceros con `POST stakeholder/quick` (C-F01-141) desde el «+» de `AppSearchSelect` y de `AppChargeForm`. La parte 1 retira `POST weighbridge/stakeholders/quick` (`B/Wms.Api/Controllers/v1/WeighbridgeController.cs:980`; hoy solo lo llama `F/features/stakeholders/composables/useQuickCreateStakeholder.ts:28`, desde `QuickCreateStakeholderDialog` en `F/features/weighbridge/components/StorageServiceForm.vue:1354`) y `POST weighbridge/transport-companies/quick` (`B/Wms.Api/Controllers/v1/WeighbridgeSharedController.cs:107`; hoy lo llama `F/features/entries/components/VehicleForm.vue:274`, que montan Vigilancia en `F/pages/operations/entries/index.vue:346`, Báscula en `F/features/weighbridge/components/CompleteEntryInfo.vue:310` y Bodega en `F/features/warehouse/components/ReceptionStepManualInfo.vue:294`). I-03 pasa `VehicleForm` a C-F01-141 con el rol `TRANSPORT_COMPANY`: Vigilancia y Bodega conservan su «+», y ningún rol pierde permiso, porque `QuickStakeholderAccess` (Admin, Receiving, Scale, Warehouse, ForeignTrade, Billing) contiene a `OperationalAccess` (Admin, Warehouse, Receiving, Scale) (`DEC-005`) | Usuario: «Reemplazar las dos (Recomendada)»; `P01/` §10 |
| D2 | **El registro guarda el primer peso y «Req. 2.º pesaje» en el vínculo camión–servicio.** `service_record_entry_logs` (una fila por entrada en ingreso, salida y solo báscula: `B/Wms.Domain/Entities/Logistics/ServiceRecordEntryLog.cs:13-28`, configurada como tabla de unión en `B/Wms.Infrastructure/Persistence/Configurations/Logistics/EntryLogConfiguration.cs:75-91`) suma el primer peso, su fecha y hora, quién lo tomó y el modo de un solo pesaje (migración `WeighingAtRegistration`, §4). El ciclo sigue naciendo en el cobro (nota de la fase 3 de `P01/` §8): al cobrar, el ciclo nace con su primer pesaje tomado del vínculo y, si la entrada es de un solo pesaje, se cierra. Mientras no hay ciclo, la cola, el historial y el detalle leen el peso del vínculo. `ServiceRecord.SingleWeightOnly` (`B/Wms.Domain/Entities/Services/ServiceRecord.cs:31`) deja de decidir: lo comparten los camiones de un depósito (`P01/` D20) y AF-11 lo pide por entrada | Usuario: «En el vínculo camión–servicio (Recomendada)»; AF-06, AF-07, AF-11 |
| D3 | **La corrección de la sección Vigilancia pide motivo a Báscula solo con el ciclo cerrado.** C-F03-17 modifica C-F01-07: un usuario con el rol Báscula (y sin Receiving ni Admin) puede corregir motivo, fecha y placa sin motivo mientras el camión no tenga un ciclo completo; la auditoría guarda «Corrección en el registro de báscula». Vigilancia y Admin lo siguen pidiendo siempre (`B/Wms.Application/Logistics/EntryLogs/Commands/CorrectEntryLog/CorrectEntryLogCommandValidator.cs:12`). Con un ciclo completo, el motivo es obligatorio para todos | Usuario: «Solo con el ciclo cerrado (Recomendada)»; `A/` §3.6; riesgo R6 |
| D4 | **Endpoints por recurso y acción.** Tres listados del historial (C-F03-22 a C-F03-24), un detalle por entrada de ingreso y otro por servicio (C-F03-25 y C-F03-26), anulación por entrada y por servicio con o sin ciclo (C-F03-37 y C-F03-38), `PUT weighbridge/service-records/{id}` para salida y solo báscula (C-F03-16), el interruptor del 2.º pesaje (C-F03-12), el repesaje del ciclo cerrado sobre `cycles/{id}/weighings` (C-F03-11) y la impresión sobre el PDF de hoy con secciones (C-F03-35), con la observación guardada antes por el endpoint de hoy (C-F03-36). Se retiran `history`, `history/totals`, `recoverable`, `incomplete/{id}`, `entries/{entryId}/ticket/pdf`, `pending`, `pending-second-weight`, `cycles/open` y `cycles/open-by-plate` (§2.1) | Usuario: «Por recurso y acción (Recomendada)», con la lista de su vista previa |
| D5 | **Ruta del registro:** `/operations/weighbridge/process/[entryLogId]`, una página por camión con los tres pasos. La consulta lleva la entrada y el paso: `?servicio={serviceRecordId}&paso=registro|cobro|tiquete`; sin `servicio`, el camión aún no tiene entrada (o es la primera); `?duplicar=1` abre una entrada nueva del mismo camión con las secciones 1 y 2 copiadas (D20). Recargar no pierde el paso. La cola P-BAS-01 conserva `/operations/weighbridge` | Usuario: «/operations/weighbridge/process/[entryLogId] (Recomendada)»; `PM/` §5.5 |
| D6 | **Historial en tres páginas:** Entradas conserva `/operations/weighbridge/history` (con las pestañas Importación, Exportación e Inspección), y Salidas y Solo báscula son `/operations/weighbridge/history/exits` y `/operations/weighbridge/history/weighing-only`. Como Nuxt anida `history.vue` sobre `history/`, `history.vue` pasa a `history/index.vue` (misma URL). Menú de Báscula: Dashboard · Proceso de pesaje · Historial de entradas · Historial de salidas · Historial de solo báscula | Usuario: «history, history/exits y history/weighing-only (Recomendada)»; `P02/` §1.5 |
| D7 | **Páginas sin uso:** I-03 borra `F/pages/operations/weighbridge/recover.vue` (AF-51), `in-process.vue` y `pending-reweigh.vue`, y pasa los enlaces del dashboard (`F/pages/operations/weighbridge/dashboard.vue:21`, `:28`, `:43`, `:100`, `:108`, `:116`) y el atajo Alt+K (`F/composables/useGlobalShortcuts.ts:23`) a la cola nueva con `?estado=PendingReweigh` (u otro estado). `F/pages/operations/weighbridge/cycles/[id].vue` conserva su ruta y sus roles (Admin, Scale, Billing, ForeignTrade; `:55`) y muestra a página completa el mismo componente del detalle P-BAS-11 (`WeighbridgeEntryDetail`), así Comercio Exterior y Facturación no pierden el enlace del detalle del depósito (`F/features/foreign-trade/components/DepositDetailWeightsCard.vue:91`; `DEC-005`). Como la página recibe el Id del ciclo, C-F03-34 devuelve el mismo detalle por ciclo (consecuencia de esta respuesta y de D4). F05 decide si cambia ese enlace | Usuario: «Borrar redirecciones; cycles/[id] con el detalle nuevo (Recomendada)» |
| D8 | **Tres fases por parte** (§8). Backend: 1) registro y ciclo; 2) cola, historial y detalle; 3) tiquete, anulación y correcciones. Maquetación: 1) contratos, fuentes simuladas, cola y registro (P-BAS-01 a P-BAS-04); 2) cobro, tiquete, repesaje e impresión (P-BAS-05 a P-BAS-07 y P-BAS-13); 3) historial, detalle, corrección, Vigilancia › Historial y `cycles/[id]` (P-BAS-08 a P-BAS-11 y P-TR-12) | Usuario: «Tres y tres (Recomendada)» |

### 1.2 Registro y ciclo

| # | Decisión | Fuente |
| --- | --- | --- |
| D9 | **Estados de una entrada** (`A/` §2.1 c), calculados por una regla pura `WeighbridgeEntryStateResolver` (`B/Wms.Application/Weighbridge/Common/Services/`, probada en `Wms.Tests`), única fuente de la cola, el historial y el detalle: `Voided` «Anulado» si la entrada, el servicio o el ciclo están anulados o descartados; `NotStarted` «Sin iniciar» si el camión no tiene vínculo con un servicio; sin ciclo, `PendingWeighing` «Por pesar» si el vínculo no tiene primer peso y `PendingPayment` «Por cobrar» si lo tiene; con ciclo, `PendingWeighing` si no tiene pesajes, `Completed` «Completado» si está completo y `PendingReweigh` «Por repesar» si tiene el primer pesaje y requiere el segundo. «En atención» no es estado: marca en el panel de la cola el camión abierto en la página (`A/` §2.1 c) | AF-05, AF-07, AF-11; `A/` §2.1 c |
| D10 | **Tres pasos en una página** (AF-05, AF-06): Registro (con los pesos) → Cobro → Tiquete, en `process/[entryLogId]` (D5). «Guardar» con P. indicador deja la entrada «Por cobrar»; sin él muestra la advertencia del wireframe («No registró los pesos. La entrada quedará «Por pesar» en la cola. ¿Guardar sin pesaje?», con «Volver» y «Guardar sin pesaje») y la deja «Por pesar». Los dos casos llevan al Cobro (`A/` §2.1 g, P-BAS-02). Los botones van en el encabezado, como MK-01 v2 (AF-07, AF-45). «Volver a la cola» pierde lo no guardado: no hay borradores (se retira el de hoy, `F/features/weighbridge/utils/truck-drafts.ts`). La estructura y la ubicación de botones siguen MK-01 v2 con los apartes de `A/` §2.1 g (sin tipo de vehículo, tara calculada, sin «Datos para Comercio Exterior», descripción de la inspección) | AF-05, AF-06, AF-07, AF-45 |
| D11 | **El formulario lo decide la categoría del motivo** (`P01/` D12, C-F01-02): `Entry` → P-BAS-02; `Exit` → P-BAS-03; `WeighingOnly` → P-BAS-04. Cambiar el motivo en la sección 1 antes de guardar cambia el formulario al instante; después de guardar, un cambio de categoría responde el 409 de C-F01-07 (anular y repetir; `P01/` D13). La cola solo trae camiones con motivo que requiere pesaje o con ciclo abierto, como hoy (`B/Wms.Application/Weighbridge/Queries/GetWeighbridgeQueue/GetWeighbridgeQueueHandler.cs:32-34`) | AF-08 (F01); `A/` §2.1 f |
| D12 | **Sección 1, Vigilancia** (AF-08): un resumen con «✎ Editar», que despliega motivo, fecha y hora y placa. Guarda con C-F03-17, con motivo según D3 y los límites de fecha de `DEC-012` y `DEC-051`. «Duplicar entrada» y la sección 1 viven en el encabezado y en la primera tarjeta, como MK-01 v2 | AF-08, AF-45; `DEC-012`, `DEC-051` |
| D13 | **Conductor por Id** (AF-18, `P01/` D16). Hoy el registro busca al conductor por documento y toma el más antiguo (`B/Wms.Application/Weighbridge/Common/Services/EntryLogInfoUpdater.cs:77-87`), así que con dos conductores del mismo documento asigna el equivocado. `EntryLogInfoInput` (`:11-20`) suma `DriverId`: si viene, se asigna ese conductor (activo; si no, 400 «El conductor no existe o está inactivo.») y se ignoran los campos de documento; sin él, sigue la regla de hoy. Lo usan C-F03-01 a C-F03-04 y C-F03-18. En la sección 2, el selector de conductor es `AppSearchSelect` sobre C-F01-15 (`search`), con nombre y documento en cada opción; «+» crea con C-F01-17 y «✎» corrige con C-F01-18, con el documento bloqueado (`DEC-017`) | AF-18 (F01); `DEC-017`; `P01/` D16 |
| D14 | **Transportadora y tercero** (AF-24, AF-54, AF-16): la transportadora de la sección 2 es `AppSearchSelect` sobre C-F01-25 con `businessRolCode=TRANSPORT_COMPANY`, por nombre o NIT, con «+» que crea con C-F01-141 y el rol `TRANSPORT_COMPANY`; se precarga con la del vehículo (`GET weighbridge/entry-logs/{id}`, C-F03-43) o la memoria del turno (`F/features/weighbridge/composables/useEntryFormMemory.ts`, que no llama al API). El tercero de solo báscula (P-BAS-04) es `AppSearchSelect` sobre C-F01-25 sin filtro de rol, opcional, con «+» que crea con el rol `CUSTOMER`. Reemplaza «Cliente» y sale «Peso esperado» (AF-16, PR-06) | AF-16, AF-24, AF-54 |
| D15 | **Primer peso y «Req. 2.º pesaje» en el registro** (D2). C-F03-01 a C-F03-04 aceptan `firstWeight` (kg, > 0, opcional) y `firstWeightCapturedAt` (fecha y hora; por defecto la del servidor; las reglas de fecha del pesaje de hoy, WMS-33), y el modo de un solo pesaje con el nombre de hoy de cada comando (`singleWeightOnly` en almacenamiento y solo báscula; `requiresReweigh` en salida). El switch se precarga como hoy: encendido en ingreso y salida, apagado en solo báscula (`B/Wms.Application/Weighbridge/Commands/Storage/Initiate/InitiateStorageWeighingCommand.cs:57`; `B/Wms.Application/Weighbridge/Commands/Output/Initiate/InitiateOutputWeighingCommand.cs:20`; `B/Wms.Application/Weighbridge/Commands/WeighingOnly/Initiate/InitiateWeighingOnlyCommand.cs:13`). El formulario deja de enviar lo que AF-10 quita (perecederos, «Primer pesaje», fecha de ingreso, observaciones y documentos adicionales): el backend los sigue aceptando con su valor por defecto (sin perecederos; primer pesaje bruto en ingreso y solo báscula, tara en salida; fecha de Vigilancia; sin documentos) | AF-06, AF-07, AF-10, AF-11 |
| D16 | **Pesos del formulario** (AF-09, AF-39, AF-41; `P01/` D21): en ingreso se digita P. indicador; P. manifiesto (solo con carta porte, AF-12) precarga P. mercancía, que se puede cambiar; P. vehículo/tara = indicador − mercancía, calculada y no digitable. En salida hay un solo campo, P. indicador del vehículo vacío. En solo báscula, P. indicador. La regla vive en `F/features/weighbridge/utils/registration-weights.ts` (pura, con prueba) | AF-09, AF-39, AF-41 (F01) |
| D17 | **Cobro** (P-BAS-05; AF-25, AF-47, AF-54, AF-132; `DEC-057` H5b): `AppChargeForm` (`P02/` D13) con los destinatarios de hoy; «Tercero registrado» precargado con el cliente del depósito; «Conductor del vehículo» con el conductor del registro (H-020); método en «Efectivo», «Referencia» solo con otro método. El total sale de la respuesta del registro o de la lectura de la entrada (`charge`, C-F03-01 a C-F03-04, C-F03-13 y C-F03-15); con `isAgreementZero` o en una entrada duplicada, `zeroValue` (solo pide el destinatario). Modo «Inmediato» llama a `process-payment` y «Pendiente por facturar» a `start-pending-billing` de su categoría (C-F03-05 a C-F03-10), que crean el ciclo con el primer peso (D2). Arriba, el resumen del registro con «✎ Editar registro», que vuelve al paso 1 (H-019) | AF-25, AF-47, AF-54 |
| D18 | **«Req. 2.º pesaje» editable hasta cerrar** (AF-11): sin ciclo, viaja con el guardado del registro (C-F03-01 a C-F03-04, C-F03-14 y C-F03-16); con ciclo abierto, C-F03-12. Apagarlo con el primer pesaje tomado cierra el ciclo con ese peso. Con el ciclo cerrado, el switch queda deshabilitado y el repesaje se agrega con «Repesar» (D19) | AF-11 |
| D19 | **Repesaje** (P-BAS-07; AF-13, AF-40): modal sobre `AppCrudDialog` con los datos del registro, P. indicador y P. manifiesto de solo lectura, la tara (o el bruto en salida) digitada, la mercancía calculada con su diferencia con el manifiesto y la fecha y hora precargadas. Se abre desde la cola («Atender» en «Por repesar»), desde el historial y desde el detalle. En un ciclo abierto registra el segundo pesaje con C-F01-80; en un ciclo de un solo pesaje ya cerrado, C-F03-11 lo acepta una vez (aunque el camión haya salido por Vigilancia). Sin cobro. Un repesaje equivocado se corrige con motivo («Editar pesajes», D31) | AF-11, AF-13, AF-40 |
| D20 | **Duplicar entrada** (AF-44, AF-48, AF-49; `P01/` D20): botón en el encabezado, junto a la placa, solo en ingresos y habilitado con las secciones 1 y 2 completas (`A/` §2.1 f, criterio 3 de AF-50). Lleva a `?duplicar=1`: las secciones 1 y 2 copiadas, la 3 y la 4 vacías. Al guardar, C-F03-01 con el mismo `entryLogId` crea la entrada duplicada. Una duplicada sin guardar se pierde al salir (AF-48) | AF-44, AF-48, AF-49 |
| D21 | **Salida en báscula** (P-BAS-03; AF-30, AF-34, AF-37; `P01/` D37): la página pide `GET exits/by-plate/{plate}` (C-F01-101). Con una salida, la precarga (solo lectura: número, tipo, estado, depósitos, mercancía, guía); con varias, el operario elige; sin ninguna, muestra «Se creará una salida en Borrador con la placa, el conductor y la transportadora. Comercio Exterior completa la mercancía y emite la guía.». Guarda con C-F03-03 (`exitId` o nulo). Si la respuesta trae `driverChangeNotified`, avisa que Comercio Exterior debe reemitir la guía (AF-34). Sin «Duplicar entrada» | AF-30, AF-34, AF-37 (F01) |
| D22 | **Mercancía declarada** (P-BAS-02): «+ Agregar producto» en el encabezado de la tarjeta, como MK-01 v2 (AF-45); cada línea con producto (`AppSearchSelect` sobre C-F01-69), embalaje (C-F01-29) y cantidad, sin unidad de medida (AF-22) y sin unidades de carga (AF-27); papelera por línea. El texto libre crea el producto y avisa a Comercio Exterior, como hoy (`productDescription`; `createdProducts` en la respuesta) | AF-22, AF-27 (F01), AF-45 |
| D23 | **Teclado** (riesgo R6, PRF-002): Enter ejecuta la acción principal del paso (Guardar en Registro, Cobrar en Cobro, Finalizar en Tiquete), salvo en un área de texto, un selector abierto o un modal (la regla de hoy, `F/pages/operations/weighbridge/index.vue:1500` y `:1512-1535`); F2 lleva el foco a P. indicador en Registro y, en una entrada «Por repesar», abre el repesaje; Escape cierra solo modales y nunca la página. La regla vive en `F/features/weighbridge/utils/process-keys.ts` (pura, con prueba). PRF-002 se mide en el despliegue final (`PM/` §7.3) | R6; `DEC-010` (1); `DEC-058` (teclas) |
| D44 | **Sugerencias del documento** (AF-24, H-011): al digitar el número (3 caracteres o más, espera de 300 ms) se sugieren los documentos de depósitos abiertos del tipo elegido; al elegir uno, la elección del depósito sigue `DEC-057` D1, como hoy. C-F03-52 suma a C-F01-81 el parámetro `partial`; hoy la búsqueda compara el número exacto (`B/Wms.Application/Weighbridge/Common/Services/StorageDocumentLookup.cs:30-32`). «Carta porte» es el tipo por defecto (AF-25, H-016) | AF-24, AF-25 |

### 1.3 Cola, historial y detalle

| # | Decisión | Fuente |
| --- | --- | --- |
| D24 | **Cola** (P-BAS-01; AF-15, AF-44, AF-51, H-004): una fila por entrada (las duplicadas repiten la placa), con placa, estado, motivo, mercancía (producto, embalaje y peso de mercancía; «+n» si hay más líneas), cliente, conductor, modalidad, documento, P. bruto, P. mercancía, tara y espera. Pesos vacíos en «Sin iniciar» y «Por pesar». Filtros de estado como botones con contador (Todos, Sin iniciar, Por pesar, Por cobrar, Por repesar) y búsqueda por placa o conductor, en el navegador. Única acción: «Atender», que abre `process/[entryLogId]` en el paso que toca (Registro; Cobro si está «Por cobrar»; el repesaje si está «Por repesar»); la fila no abre nada al hacer clic. Sin «Recuperar operaciones». La página usa `AppDataTable` en modo `client`, con los filtros en `globalFilters`, así que pasa al patrón de AF-129 (I-03 la mueve a `PATTERN`). Acepta `?estado=` (D7) | AF-15, AF-44, AF-51; `P02/` D8 |
| D25 | **Panel de la cola en el registro** (AF-05, MK-01 v2): a la derecha de `process/[entryLogId]`, la misma lista en formato compacto (placa, estado, mercancía, espera), con buscador, filtros Todos, Por pesar y Repesar, «Cargar a báscula →» en cada camión y la marca «En atención» en el abierto. Usa la misma fuente que P-BAS-01 | AF-05, AF-44 |
| D26 | **Historial › Entradas** (P-BAS-08; AF-15, AF-23, AF-50, H-007): `AppDataTable` en modo `server` sobre C-F03-22, con las pestañas Importación, Exportación e Inspección (`modality`). Columnas del legacy: fecha y hora, vehículo, conductor, ID del conductor, P. bruto, P. mercancía, tara, cantidad, peso del manifiesto, documento de entrada, repesa, valor, tiquete, estado y acciones; filtro en cada columna y orden en el servidor, por defecto la más reciente primero. Acciones con botones de solo icono y tooltip (`PAJ/` D6, D7): «Ver» (drawer), «Editar» (si `canEdit`: P-BAS-02 hasta que CE confirme, AF-26), «Repesar» (si `canReweigh`), «Imprimir» (si `canPrint`) y «Anular» (si `canVoid`). Una fila por entrada, duplicadas incluidas (AF-50). La fila anulada se resalta en rojo, con el motivo en un tooltip (AF-23). «Exportar» arma el Excel con `useExcelExport` sobre la consulta con `all=true` | AF-15, AF-23, AF-26, AF-50; AF-99, AF-129 (F02) |
| D27 | **Historial › Salidas** (P-BAS-09; AF-135): columnas del legacy (`bodegas-legacy/modulos/mod_bascula/listarsalidas.php`): fecha y hora, vehículo, conductor, ID del conductor, mercancía (producto · embalaje · cantidad), peso del vehículo, peso al salir, peso de la mercancía, repesa y valor, más salida, tiquete y estado. Mismas acciones que Entradas; «Editar» abre P-TR-12 (D35), también con el ciclo cerrado | AF-15, AF-135 |
| D28 | **Historial › Solo báscula** (P-BAS-10; PR-06): fecha y hora, vehículo, conductor, ID del conductor, tercero, pesaje, repesaje, tara, valor, tiquete y estado. «Tara» es la diferencia entre el pesaje y el repesaje, como el legacy (`bodegas-legacy/modulos/mod_bascula/listarsolopesajes.php:299-311`, `peso_mercancia` del repesaje), y queda vacía sin repesaje. Mismas acciones que Salidas | AF-15, AF-16 |
| D29 | **Las filas del historial son entradas guardadas, con o sin ciclo.** Una entrada guardada sin cobrar aparece con su estado (D9) y sin tiquete ni valor, para que se pueda ver, editar y anular (AF-48: «guardada, se anula con motivo»). Clave de cada fila: `warehouseStorageEntryId` en Entradas; `serviceRecordId` en Salidas y Solo báscula | AF-23, AF-48 |
| D30 | **Detalle del ciclo** (P-BAS-11; AF-15, AF-45, AF-50, AF-53; MK-07): `AppDetailDrawer` con la anatomía de `PAJ/` D5: icono `pi pi-truck`, título «Detalle del ciclo de báscula», estado (D9) y subtítulo «Placa · Ingreso: fecha y hora». Secciones `AppDetailSection`: «1. Datos del vehículo y entrada» (conductor, empresa y tipo, motivo y fecha); «2. Pesaje en báscula (kg)» (los cuatro pesos en 2×2 con sus fechas, «✎ Editar pesajes» en las acciones de la sección y el aviso si el manifiesto supera la diferencia de pesajes); «Tickets asociados» (el tiquete de esta entrada, con su peso declarado y su valor; $0 y la etiqueta «Duplicada» en una duplicada); «Factura y cobro», reducida (factura, cliente, total cobrado y estado). Acciones del registro: «Imprimir tiquete», «Repesar» (solo en un ciclo de un solo pesaje cerrado) y «Anular pesaje». La regla de `PAJ/` D3 (que cita MK-07) manda sobre la ubicación del pie de MK-07: con dos acciones van en el pie, con tres pasan al menú «Acciones» (⋮) del encabezado; «Cerrar» es la ✕ del encabezado. Abre desde «Ver» y por enlace con `?id={clave}` (`P02/` D9). El contenido vive en `F/features/weighbridge/components/WeighbridgeEntryDetail.vue`, que también monta `cycles/[id]` (D7) | AF-15, AF-45, AF-50, AF-53; `PAJ/` D3, D5 |
| D31 | **«Editar pesajes»:** en una entrada de ingreso abre la sección 4 del registro y guarda con C-F03-14 mientras el depósito esté en Borrador (Báscula), con motivo si el ciclo está completo (`P01/` D30); confirmado el depósito, corrige CE (P-CE-03, F05). En salida y solo báscula abre P-TR-12 (D35). En `cycles/[id]`, Facturación conserva el diálogo de hoy (D32) | AF-13, AF-26 (F01), AF-135 |
| D32 | **`cycles/[id]` sin retrocesos** (D7; `DEC-005`): además del detalle nuevo, conserva para los roles que hoy las tienen «Modificar pesaje» (Admin, Scale, Billing; `F/pages/operations/weighbridge/cycles/[id].vue:11`, con `ModifyWeighingDialog` y C-F03-45/46) y la fecha de ingreso del depósito (Admin, Scale, ForeignTrade; `:73`, con C-F03-51). `first-weight-modify` y `second-weight` aplican en un ciclo de almacenamiento la regla de mercancía de `P01/` D21 (con repesaje, mercancía = indicador − tara; origen `Correction`) y recalculan la factura del período (`DEC-022`), como C-F01-92: hoy no la aplican (`B/Wms.Application/Weighbridge/Commands/ModifyFirstWeight/ModifyFirstWeightHandler.cs` y `ModifySecondWeight/ModifySecondWeightHandler.cs` no tocan la mercancía) | `DEC-005`; `P01/` D21, D32 (`DEC-002`) |

### 1.4 Tiquete, anulación y corrección

| # | Decisión | Fuente |
| --- | --- | --- |
| D33 | **Impresión** (P-BAS-12 y P-BAS-13; AF-16, AF-24, AF-50, AF-52, AF-53; PR-32): un solo «Imprimir» en el paso Tiquete, en la fila del historial y en el detalle abre el modal: casillas «Entrada (bruto …)», «Tara (calculada o real …)» y «Repesaje», marcadas si existen y la de Repesaje deshabilitada si no existe; switch «Incluir recibo ($ …)»; «Observación (opcional)», precargada con la guardada. «Imprimir» guarda la observación con C-F03-36 y pide el PDF con C-F03-35. Se imprime desde el primer pesaje, también con el repesaje pendiente. El PDF toma el alto de su contenido, lleva una línea por mercancía (producto · embalaje · cantidad, H-006) y conserva la leyenda «Documento interno de control de pesaje. No es factura de venta.» (H-068). Salen «Imprimir sin observaciones» y «Guardar e Imprimir» del historial de hoy | AF-16, AF-24, AF-50, AF-52, AF-53 |
| D34 | **Anulación** (AF-23, AF-48, AF-51): «Anular pesaje» con motivo de 10 a 500 caracteres en `ReasonDialog` (`F/components/app/ReasonDialog.vue`), con o sin ciclo: C-F03-37 para una entrada de ingreso y C-F03-38 para salida y solo báscula. Con ciclo, los efectos y mensajes de hoy de la anulación del ciclo (`B/Wms.Application/Weighbridge/Commands/VoidWeighing/VoidWeighingCommandHandler.cs:40-114` y `:170-313`); sin ciclo, se anula la entrada (su mercancía sale del depósito, el depósito en Borrador sin camiones se anula) o se descarta el servicio, con el motivo en la auditoría, y el camión vuelve a «Sin iniciar». La página `recover` y `DELETE weighbridge/incomplete/{id}` se retiran (AF-51). El resultado se muestra con `CorrectionResultDialog` | AF-23, AF-48, AF-51 |
| D35 | **Corrección de salida y solo báscula** (P-TR-12; AF-135; `A/` §3.6): `AppCrudDialog` a dos columnas con placa, conductor (con «+»), transportadora (con «+»; en solo báscula, «Tercero»), fecha y hora, los pesos (peso del vehículo, peso al salir y peso de la mercancía calculado; en solo báscula, pesaje y repesaje) y «Motivo de la corrección», obligatorio con el ciclo completo. Guarda con C-F03-16. Con el ciclo cerrado avisa con el aviso de hoy «Modificación de Peso en Báscula» (rol Admin, con correo; `B/Wms.Application/Weighbridge/Commands/ModifyFirstWeight/ModifyFirstWeightHandler.cs:80-91`). En una salida con guía, cambiar placa o conductor avisa a CE con el aviso de `P01/` D45 y muestra el texto del wireframe. Antes del cobro, el mismo endpoint guarda el registro de una salida o un solo pesaje sin motivo | AF-135, AF-34 (F01) |
| D36 | **Avisos nuevos: ninguno.** F03 reutiliza «Modificación de Peso en Báscula» (hoy) y «Cambio de conductor o placa en salida con guía» (`P01/` D45), por `NotificationOrchestrator`. F09 los pasa a tipos | `PM/` §2.2 |

### 1.5 Vigilancia › Historial

| # | Decisión | Fuente |
| --- | --- | --- |
| D37 | **`/operations/entries/history` pasa al patrón de AF-129** (`P02/` D3, D8): sin `AppPageHeader` ni `AppTable`; `AppDataTable` en modo `server` sobre C-F03-27, con las columnas de hoy (placa, motivo, estado, ingreso, salida y corrección; `F/pages/operations/entries/history.vue:91-123`), filtro en cada una y orden en el servidor, por defecto el ingreso más reciente primero. Acciones con botones de solo icono y tooltip: «Ver» abre un `AppDetailDrawer` (datos del ingreso, conductor, vehículo, manifiestos, autorizaciones de salida y la última corrección), «Corregir» (C-F01-07, con motivo siempre para Vigilancia, D3), «Autorizar salida» y «Agregar manifiesto» (las de hoy, `:155-220`, con C-F03-49 y C-F03-50). Roles de la página sin cambio (Admin, Receiving; `:26`) | AF-129, AF-130 (F02); `P02/` D3 |

### 1.6 Frontend: componentes, fuentes y lo que se conserva

| # | Decisión | Fuente |
| --- | --- | --- |
| D38 | **Componentes compartidos sin cambios:** `AppDataTable`, `AppSearchSelect`, `AppDetailDrawer`, `AppDetailSection`, `AppCrudDialog`, `AppChargeForm`, `ReasonDialog` y `CorrectionResultDialog` se usan tal como están. Si una pantalla necesitara cambiar uno, el ejecutor se detiene y pregunta (riesgo R4) | R4; `P02/` D4 |
| D39 | **Componentes de Báscula nuevos** (en `F/features/weighbridge/components/`): `WeighbridgeQueueTable`, `WeighbridgeQueuePanel`, `WeighbridgeProcessHeader`, `RegistrationVigilanceSection`, `RegistrationTruckSection`, `RegistrationEntrySection`, `RegistrationGoodsLines`, `RegistrationExitSection`, `RegistrationWeighingOnlySection`, `RegistrationWeights`, `WeighbridgeChargeStep`, `WeighbridgeTicketStep`, `ReweighDialog`, `TicketPrintDialog`, `WeighbridgeEntryDetail`, `WeighbridgeHistoryActions` y `ServiceCorrectionDialog`. En otros dominios: `F/features/stakeholders/components/StakeholderQuickDialog.vue` (alta rápida con C-F01-141 y el rol fijado por prop) y `F/features/entries/components/DriverQuickDialog.vue` (alta y corrección del conductor con C-F01-17 y C-F01-18, documento bloqueado al corregir). §3.1 dice qué usa cada pantalla | `PM/` §5.5 |
| D40 | **Fuentes intercambiables** (M12, `PM/` §5.2): contratos en `F/features/weighbridge/contracts/` (y los de §2.3 en `entries/`, `exits/` y `foreign-trade/`); fuentes `queue`, `registration`, `payment`, `weighing`, `history`, `detail`, `ticket`, `void`, `service-record` y `catalog` en `F/features/weighbridge/services/*.source.ts`, y `entry-log` en `F/features/entries/services/`. **Los catálogos de F01 ya integrados** (motivos, conductores, terceros con su alta rápida, productos, embalajes y tipos de documento) se simulan con la fachada `catalog.source.ts`, porque sus fuentes de F01 ya apuntan al API real (`FT/unit/guards/mock-sources.spec.ts:22-39`) y la maquetación no llama al API: las pantallas nuevas no importan ninguna fuente de `INTEGRATED_SOURCES` ni un componente de hoy que llame al API (`DriverPicker`, `VehicleForm`, `BillingCollectForm`…). En I-03 la fachada se borra y sus usos pasan a las fuentes integradas de F01 | M12; `P02/` D10, D15 |
| D41 | **Lo de `F/features/weighbridge/` que otros módulos importan se conserva** (trampa 4): `services/weighbridge-service.ts` (lo usan Vigilancia y los componentes de `entries/`: `getVehicleTypes`, `getVehicleByPlate`, `getDriverByDocument`, `updateEntryLogInfo`; `quickCreateTransportCompany` sale en I-03 por D1), `composables/useEntryFormMemory.ts`, `components/PrefilledHint.vue`, `types/operation-types.ts`, `types/documents.ts` y `components/ServiceRecordDocumentsManager.vue` (Bodega, `ReceptionStepManualInfo.vue:17-18`), `types/weighbridge-cycle.ts` (`F/features/foreign-trade/services/foreign-trade-service.ts:66`) y `composables/useAddAdditionalOrders.ts` (`F/features/foreign-trade/composables/useExitWithEntryTicketFt.ts:3`, de F06). I-03 borra solo lo que nadie más importa, comprobado con grep (trampa 7) | Trampas 4 y 7; `PM/` §2.2 |
| D42 | **`BillingCollectForm` y `useUnitMeasures` no se borran**: F03 no es su último uso. `BillingCollectForm` lo siguen usando la guía (`F/features/foreign-trade/components/DispatchGuideForm.vue:11`, F06) y el montacargas (`F/features/warehouse/components/ForkliftUseDialog.vue:19`, F04); `useUnitMeasures`, CE (`F/features/foreign-trade/components/DepositProductDialog.vue:11`, F05) y Bodega (`ReceptionStepManualInfo.vue:30`, F04). `AdditionalDepositCollect.vue` solo lo usa Báscula: I-03 lo borra con su prueba | `P02/` D4, D19 |
| D43 | **Menú** (`P02/` §1.5, D5): I-03 deja Báscula con Dashboard · Proceso de pesaje · Historial de entradas · Historial de salidas · Historial de solo báscula (`F/components/layout/menu-model.ts:45-55`), y Vigilancia sin cambios (`:38-44`). Ninguna ruta nueva se enlaza antes de I-03 (M4) | M4; D6 |

### 1.7 Destino de las 20 AF dueñas

| AF | Decisiones | Fase (BE · FE) |
| --- | --- | --- |
| AF-05 | D5, D9, D10, D24, D25 | BE 1 y 2 · FE 1 |
| AF-06 | D2, D10, D17 | BE 1 · FE 1 y 2 |
| AF-07 | D2, D9, D10 | BE 1 · FE 1 |
| AF-10 | D15 | BE 1 · FE 1 |
| AF-11 | D2, D15, D18 | BE 1 · FE 1 y 2 |
| AF-13 | D19, D31 | BE 1 · FE 2 |
| AF-15 | D24, D26, D27, D28, D30 | BE 2 · FE 1 y 3 |
| AF-16 | D14, D28, D33 | BE 1 y 3 · FE 1 y 2 |
| AF-23 | D26, D29, D34 | BE 3 · FE 3 |
| AF-24 | D14, D33, D44 | BE 1 y 3 · FE 1 y 2 |
| AF-25 | D17, D26, D44 | BE 2 · FE 1 y 2 |
| AF-40 | D19 | BE 1 · FE 2 y 3 |
| AF-45 | D10, D12, D22, D30 | — · FE 1 y 3 |
| AF-48 | D20, D29, D34 | BE 3 · FE 1 y 3 |
| AF-49 | D20 | BE 1 · FE 1 |
| AF-50 | D26, D30, D33 | BE 2 y 3 · FE 2 y 3 |
| AF-51 | D7, D24, D34 | BE 3 · FE 1 |
| AF-52 | D33 | BE 3 · FE 2 |
| AF-53 | D30, D33 | BE 3 · FE 2 y 3 |
| AF-135 | D27, D35 | BE 3 · FE 3 |

Las 20 tienen decisión y fase.

### 1.8 AF de otras features que F03 muestra o aplica

| AF | Feature dueña | Qué muestra F03 | Pantalla |
| --- | --- | --- | --- |
| AF-08 | F01 | Formulario por la categoría del motivo; sección Vigilancia editable | P-BAS-02 a P-BAS-04 |
| AF-09, AF-39, AF-41 | F01 | Pesos del legacy: mercancía precargada con el manifiesto, tara calculada, neto real con el repesaje | P-BAS-02, P-BAS-07, P-BAS-11 |
| AF-12 | F01 | Número y peso del manifiesto solo con carta porte | P-BAS-02 |
| AF-14, AF-31 | F01 | Sin esperas por Bodega en el repesaje | P-BAS-07 |
| AF-17 | F01 | Inspección con documento y producto opcionales y descripción obligatoria | P-BAS-02 |
| AF-18 | F01 | Conductores con el mismo documento: el selector muestra nombre y documento (D13) | P-BAS-02 a P-BAS-04, P-TR-12 |
| AF-20, AF-43, AF-44, AF-46, AF-47 | F01 | Una entrada por documento, que puede sumarse al depósito abierto; cada duplicada con sus pesos y su cobro en $0 | P-BAS-01, P-BAS-02, P-BAS-05, P-BAS-08, P-BAS-11 |
| AF-21 | F01 | Sin tipo de vehículo en la sección 2 | P-BAS-02 a P-BAS-04 |
| AF-22 | F01 | Mercancía sin unidad de medida | P-BAS-02, P-BAS-12 |
| AF-26 | F01 | «Editar» desde el historial hasta que CE confirme | P-BAS-08, P-BAS-11 |
| AF-27 | F01 | Sin unidades de carga en Báscula | P-BAS-02 |
| AF-30, AF-34, AF-37 | F01 | Salida precargada por la placa o creada en Borrador; el conductor pasa a la salida | P-BAS-03, P-TR-12 |
| AF-84 | F01 | Camión tardío en un depósito confirmado (`isLateTruck`): aviso al guardar | P-BAS-02 |
| AF-101 | F01 | Transportadora por entrada | P-BAS-02 |
| AF-54 | F02 | «+» de alta rápida junto a transportadora, tercero de solo báscula y tercero registrado del cobro | P-BAS-02, P-BAS-04, P-BAS-05, P-TR-12 |
| AF-99 | F02 | Filtros por columna, orden y botones con borde o relleno | P-BAS-01, P-BAS-08 a P-BAS-10, Vigilancia › Historial |
| AF-129, AF-130 | F02 | Patrón de listado y detalle en drawer | P-BAS-01, P-BAS-08 a P-BAS-11, Vigilancia › Historial |
| AF-131, AF-132 | F02 | Etiquetas encima; cobro con método y referencia | todas; P-BAS-05 |

---

## 2. Contrato (parte 0)

Es la única fuente del frontend para lo que F03 crea, cambia o retira (`PM/` R3). Los endpoints de F01 que F03 consume sin cambios se citan por su ID C-F01-mm (`P01/` §2.2 y §2.3). Lo verificado contra el código de `fase-2` se anota en cada ficha.

### 2.0 Convenciones

- Rige `P01/` §2.0: base `/api/v1`, JWT, camelCase, enums como texto, fechas ISO 8601 con zona, `{ data, pagination }`, `pageSize` de 1 a 50 con `all=true`, *ProblemDetails* con `description` y `errors[]`, motivos de 10 a 500 caracteres y C-F01-00 (orden y filtros por columna) en los listados marcados «orden y filtros».
- **Estado de una entrada** (D9): `WeighbridgeEntryState` = `NotStarted` | `PendingWeighing` | `PendingPayment` | `PendingReweigh` | `Completed` | `Voided`; rótulos «Sin iniciar», «Por pesar», «Por cobrar», «Por repesar», «Completado», «Anulado».
- **Categoría** = `Entry` | `Exit` | `WeighingOnly` (la del motivo, `P01/` D12).
- **Clave de una entrada:** el camión (`entryLogId`) y su servicio (`serviceRecordId`). En ingreso también `warehouseStorageEntryId`, que identifica la entrada en el historial, el detalle y la anulación; en salida y solo báscula, `serviceRecordId`.
- **Identificadores:** `C-F03-mm` y `QA2-F03-nnn` (`PM/` §5.1).
- **Políticas:** F03 no crea políticas. Usa las de hoy (`B/Wms.Domain/Security/WmsPolicyRoles.cs:11-38`): `ScaleAccess` (Admin, Scale) para lo de Báscula; `ActiveUser` para el detalle y el PDF (los abren Facturación y CE desde `cycles/[id]`); `GateAccess` y `EntryCorrectionAccess` para Vigilancia; `WeighingCorrectionAccess` y `DepositEntryDateAccess` para lo que conserva `cycles/[id]`. Ningún rol pierde una función (`DEC-005`): lo retirado solo lo llaman pantallas de Báscula o se reemplaza por C-F01-141 (D1).

### 2.1 Índice

**Grupo A — Registro y ciclo** (backend, fase 1).

| ID | Endpoint | Cambio | Política | Pantalla |
| --- | --- | --- | --- | --- |
| C-F03-01 | `POST weighbridge/storage/register` | modificado (sobre C-F01-79): primer peso, modo por entrada, `driverId`, `state` y `charge` | `ScaleAccess` | P-BAS-02 |
| C-F03-02 | `POST weighbridge/storage/initiate` | modificado (sobre C-F01-78): lo mismo que C-F03-01, sin los datos del camión | `ScaleAccess` | — (comando compartido) |
| C-F03-03 | `POST weighbridge/output/initiate` | modificado (sobre C-F01-109): primer peso, `state` y `charge` | `ScaleAccess` | P-BAS-03 |
| C-F03-04 | `POST weighbridge/weighing-only/initiate` | modificado: primer peso, tercero sin rol fijo, sin peso esperado | `ScaleAccess` | P-BAS-04 |
| C-F03-05 | `POST weighbridge/storage/process-payment` | modificado: el ciclo nace con el primer peso | `ScaleAccess` | P-BAS-05 |
| C-F03-06 | `POST weighbridge/storage/start-pending-billing` | modificado: igual | `ScaleAccess` | P-BAS-05 |
| C-F03-07 | `POST weighbridge/output/process-payment` | modificado (sobre C-F01-110): igual | `ScaleAccess` | P-BAS-05 |
| C-F03-08 | `POST weighbridge/output/start-pending-billing` | modificado (sobre C-F01-111): igual | `ScaleAccess` | P-BAS-05 |
| C-F03-09 | `POST weighbridge/weighing-only/process-payment` | modificado: igual | `ScaleAccess` | P-BAS-05 |
| C-F03-10 | `POST weighbridge/weighing-only/start-pending-billing` | modificado: igual | `ScaleAccess` | P-BAS-05 |
| C-F03-11 | `POST weighbridge/cycles/{cycleId}/weighings` | modificado (sobre C-F01-80): repesaje del ciclo de un solo pesaje cerrado | `ScaleAccess` | P-BAS-02 a P-BAS-04, P-BAS-07 |
| C-F03-12 | `PATCH weighbridge/cycles/{cycleId}/second-weighing` | nuevo | `ScaleAccess` | P-BAS-02 a P-BAS-04 |
| C-F03-13 | `GET weighbridge/entries/{entryId}` | modificado (sobre C-F01-93): estado, primer peso sin ciclo, modo, cobro y embalaje | `EntryEditAccess` | P-BAS-02, P-BAS-05 |
| C-F03-14 | `PUT weighbridge/entries/{entryId}` | modificado (sobre C-F01-92): primer peso sin ciclo y modo | `ScaleAccess` | P-BAS-02, P-BAS-11 |
| C-F03-15 | `GET weighbridge/service-records/{serviceRecordId}/registration` | modificado (sobre C-F01-155): estado, primer peso, modo, conductor, transportadora y cobro | `ScaleAccess` | P-BAS-03 a P-BAS-05 |
| C-F03-17 | `PUT entry-logs/{id}/correction` | modificado (sobre C-F01-07): motivo opcional para Báscula sin ciclo completo | `EntryCorrectionAccess` | P-BAS-02 a P-BAS-04, Vigilancia › Historial |
| C-F03-18 | `PATCH weighbridge/entry-log/{id}/info` | modificado: `driverId` opcional (D13) | `OperationalAccess` | — (Vigilancia hoy) |
| C-F03-19 | `POST weighbridge/stakeholders/quick` | retirado (D1) | — | — |
| C-F03-20 | `POST weighbridge/transport-companies/quick` | retirado (D1) | — | — |
| C-F03-43 | `GET weighbridge/entry-logs/{id}` | sin cambios | `ScaleAccess` | P-BAS-02 a P-BAS-04 |
| C-F03-44 | `GET weighbridge/shipping-document-types` | sin cambios | `ActiveUser` | P-BAS-02 |
| C-F03-52 | `GET weighbridge/storage/document-candidates` | modificado (sobre C-F01-81): `partial` | la de hoy (`ScaleAccess`) | P-BAS-02 |

**Grupo B — Cola, historial y detalle** (backend, fase 2).

| ID | Endpoint | Cambio | Política | Pantalla |
| --- | --- | --- | --- | --- |
| C-F03-21 | `GET weighbridge/queue` | modificado: una fila por entrada, estados nuevos, pesos y mercancía | `ScaleAccess` | P-BAS-01, panel de la cola |
| C-F03-22 | `GET weighbridge/history/entries` | nuevo (orden y filtros) | `ScaleAccess` | P-BAS-08 |
| C-F03-23 | `GET weighbridge/history/exits` | nuevo (orden y filtros) | `ScaleAccess` | P-BAS-09 |
| C-F03-24 | `GET weighbridge/history/weighing-only` | nuevo (orden y filtros) | `ScaleAccess` | P-BAS-10 |
| C-F03-25 | `GET weighbridge/entries/{entryId}/detail` | nuevo | `ActiveUser` | P-BAS-11 |
| C-F03-26 | `GET weighbridge/service-records/{serviceRecordId}/detail` | nuevo | `ActiveUser` | P-BAS-11 |
| C-F03-34 | `GET weighbridge/cycles/{cycleId}/detail` | nuevo (la misma respuesta, para `cycles/[id]`, D7) | `ActiveUser` | `cycles/[id]` |
| C-F03-27 | `GET entry-logs` | modificado: orden y filtros (C-F01-00) | `GateAccess` | Vigilancia › Historial |
| C-F03-48 | `GET entry-logs/{id}` | sin cambios | `GateAccess` | Vigilancia › Historial |
| C-F03-28 | `GET weighbridge/history` | retirado (lo reemplazan C-F03-22 a C-F03-24) | — | — |
| C-F03-29 | `GET weighbridge/history/totals` | retirado | — | — |
| C-F03-30 | `GET weighbridge/pending` | retirado (lo absorbe la cola) | — | — |
| C-F03-31 | `GET weighbridge/pending-second-weight` | retirado | — | — |
| C-F03-32 | `GET weighbridge/cycles/open` | retirado | — | — |
| C-F03-33 | `GET weighbridge/cycles/open-by-plate` | retirado | — | — |

**Grupo C — Tiquete, anulación y correcciones** (backend, fase 3).

| ID | Endpoint | Cambio | Política | Pantalla |
| --- | --- | --- | --- | --- |
| C-F03-35 | `GET weighbridge/{id}/ticket/pdf` | modificado: `sections`, `receipt`, alto según el contenido, una línea por mercancía | `ActiveUser` | P-BAS-12, P-BAS-13 |
| C-F03-36 | `PATCH weighbridge/{id}/ticket-observations` | sin cambios | `ScaleAccess` | P-BAS-13 |
| C-F03-37 | `POST weighbridge/entries/{entryId}/void` | nuevo | `ScaleAccess` | P-BAS-08, P-BAS-11 |
| C-F03-38 | `POST weighbridge/service-records/{serviceRecordId}/void` | nuevo | `ScaleAccess` | P-BAS-09 a P-BAS-11 |
| C-F03-16 | `PUT weighbridge/service-records/{serviceRecordId}` | nuevo: registro de salida o solo báscula antes del cobro y P-TR-12 | `ScaleAccess` | P-BAS-03, P-BAS-04, P-TR-12 |
| C-F03-45 | `PATCH weighbridge/{id}/first-weight-modify` | modificado (efecto, D32): misma forma | `WeighingCorrectionAccess` | `cycles/[id]` |
| C-F03-46 | `PATCH weighbridge/{id}/second-weight` | modificado (efecto, D32): misma forma | `WeighingCorrectionAccess` | `cycles/[id]` |
| C-F03-49 | `POST entry-logs/{id}/departure-authorizations` | sin cambios | `GateAccess` | Vigilancia › Historial |
| C-F03-50 | `POST entry-logs/{id}/manifests` | sin cambios | `GateAccess` | Vigilancia › Historial |
| C-F03-51 | `PATCH warehouse-storages/{id}/entry-date` | sin cambios | `DepositEntryDateAccess` | `cycles/[id]` |
| C-F03-39 | `GET weighbridge/recoverable` | retirado (AF-51) | — | — |
| C-F03-40 | `DELETE weighbridge/incomplete/{serviceRecordId}` | retirado (AF-51; lo reemplazan C-F03-37 y C-F03-38) | — | — |
| C-F03-41 | `GET weighbridge/entries/{entryId}/ticket/pdf` | retirado (una entrada, un ciclo: `P01/` D5) | — | — |

Los números C-F03-42 y C-F03-47 no se usan. `POST weighbridge/cycles/{cycleId}/void` no cambia y no se retira (no estaba en la lista de D4): las pantallas de F03 anulan con C-F03-37 y C-F03-38. Lo anota §10.

**Consumidos de F01 sin cambios** (`P01/` §2.2): C-F01-02 (motivos), C-F01-15, C-F01-17, C-F01-18 y C-F01-20 (conductores), C-F01-25 y C-F01-26 (terceros), C-F01-29 (embalajes), C-F01-69 (productos), C-F01-95 y C-F01-101 (salidas) y C-F01-141 (alta rápida).

### 2.2 Fichas

#### Grupo A — Registro y ciclo

##### C-F03-01 · `POST weighbridge/storage/register` (modificado)
- **Política:** `ScaleAccess` (sin cambios; `B/Wms.Api/Controllers/v1/WeighbridgeController.cs:244`).
- **Qué cambia** (sobre C-F01-79): primer peso y modo por entrada (D2, D15), conductor por Id (D13), estado y cobro en la respuesta.
- **Petición:** la de hoy con los cambios de C-F01-78 (`InitiateStorageWeighingCommand.cs:14-80` más los datos del conductor y del vehículo de `RegisterStorageEntryCommand`), más:

| Campo | Tipo | Obligatorio | Regla |
| --- | --- | --- | --- |
| `driverId` | guid \| null | No | D13: si viene, se asigna ese conductor y se ignoran `driverFirstName`, `driverLastName`, `driverIdNumber` y `driverIdType` |
| `firstWeight` | decimal \| null | No | > 0. Sin él, la entrada queda «Por pesar» |
| `firstWeightCapturedAt` | fecha y hora \| null | No | Por defecto, la del servidor; las reglas de fecha del pesaje de hoy (WMS-33) |
| `singleWeightOnly` | bool | No | Ya existía; ahora se guarda en el vínculo de la entrada (D2) |
| `merchandiseWeight` | decimal \| null | No | `P01/` D21: no supera `firstWeight` cuando este viene |

- **Respuesta 201:** `dataSchema(storageRegisterResultSchema)`: la de hoy (`InitiateStorageResponseDto` más `entryLogUpdated`) más `state` (`PendingWeighing` o `PendingPayment`), `firstWeight` y `charge` (`{ weighingPrice, taxAmount, totalAmount, isAgreementZero, isZeroCharge }`; `isZeroCharge` es verdadero en una duplicada o con convenio en $0).
- **Errores nuevos:** 400 «El peso del indicador debe ser mayor que cero.»; 400 «El peso de la mercancía no puede ser mayor que el peso del indicador.» (`P01/` D21); 400 «El conductor no existe o está inactivo.»; los de C-F01-78 y C-F01-79.
- **Zod:** `storageRegisterSchema`, `storageRegisterResultSchema` (`F/features/weighbridge/contracts/registration.ts`).

##### C-F03-02 · `POST weighbridge/storage/initiate` (modificado)
- **Política:** `ScaleAccess` (`WeighbridgeController.cs:190`). **Qué cambia:** lo mismo que C-F03-01 sin los campos del conductor ni del vehículo (es el mismo comando). **Petición:** `storageRegisterSchema` sin los campos de `entryInfoSchema`. **Respuesta 201:** `dataSchema(storageRegisterResultSchema)` sin `entryLogUpdated`. **Errores:** los de C-F03-01. **Zod:** `storageInitiateSchema`, `storageRegisterResultSchema`. **Notas:** el frontend usa C-F03-01; este lo usan las pruebas (`WeighbridgeScenario`).

##### C-F03-03 · `POST weighbridge/output/initiate` (modificado)
- **Política:** `ScaleAccess` (`WeighbridgeController.cs:373`).
- **Qué cambia** (sobre C-F01-109): `firstWeight`, `firstWeightCapturedAt` (primer pesaje del vehículo vacío, tara) y `driverId` dentro de los datos del camión (D13). `requiresReweigh` (el nombre de hoy, `InitiateOutputWeighingCommand.cs:20`) se guarda en el vínculo.
- **Petición:** `outputInitiateSchema` = `entryLogId`, `exitId` (guid \| null), `driverId`, `observations`, `requiresReweigh`, `firstWeight`, `firstWeightCapturedAt` y los datos del camión (`entryInfoSchema`, con `carrierCompanyId` obligatorio sin `exitId`).
- **Respuesta 201:** `dataSchema(outputInitiateResultSchema)`: `InitiateOutputResponseDto` (con los cambios de C-F01-109) más `state`, `firstWeight` y `charge`.
- **Errores:** los de C-F01-109 y los de peso de C-F03-01. **Zod:** `outputInitiateSchema`, `outputInitiateResultSchema`.

##### C-F03-04 · `POST weighbridge/weighing-only/initiate` (modificado)
- **Política:** `ScaleAccess` (`WeighbridgeController.cs:84`).
- **Qué cambia:** `firstWeight` y `firstWeightCapturedAt`; `customerId` es el «Tercero» (cualquier tercero activo, sin exigir un rol; el servicio lo guarda como hoy, con el rol `CUSTOMER`: `B/Wms.Application/Weighbridge/Commands/WeighingOnly/Initiate/InitiateWeighingOnlyHandler.cs:105-140`); `expectedWeight` se ignora (AF-16); `driverId` en los datos del camión.
- **Petición:** `weighingOnlyInitiateSchema`. **Respuesta 201:** `dataSchema(weighingOnlyInitiateResultSchema)` = `InitiateWeighingResponseDto` más `state`, `firstWeight` y `charge`.
- **Errores:** 404 «El tercero no existe.» y los de peso de C-F03-01. **Zod:** `weighingOnlyInitiateSchema`, `weighingOnlyInitiateResultSchema`.

##### C-F03-05 a C-F03-10 · cobros de báscula (modificados)
- **Endpoints:** `storage/process-payment` (`WeighbridgeController.cs:304`), `storage/start-pending-billing` (`:336`), `output/process-payment` (`:412`), `output/start-pending-billing` (`:444`), `weighing-only/process-payment` (`:122`) y `weighing-only/start-pending-billing` (`:154`). **Política:** `ScaleAccess`.
- **Qué cambia:** al crear el ciclo, si el vínculo de la entrada tiene primer peso, el ciclo nace con ese pesaje (tipo bruto en ingreso y solo báscula, tara en salida; fecha y usuario del vínculo) y, si la entrada es de un solo pesaje, se cierra. Sin primer peso, el ciclo queda listo para pesar, como hoy. La regla de la duplicada en $0 no cambia (`P01/` D20).
- **Petición:** la de hoy (`B/Wms.Application/Weighbridge/Common/Dtos/Requests/ProcessStoragePaymentRequest.cs`: `serviceRecordId`, `entryLogId`, `paymentMethod`, `amountReceived`, `referenceNumber`, `notes`, `unregisteredRecipient`, `invoiceNumber`, `recipientMode`, `customerId`).
- **Respuesta 201:** la de hoy (`ProcessPaymentResponseDto` o `StartPendingBillingResponseDto`) más `state` (`PendingWeighing`, `PendingReweigh` o `Completed`) y `ticketNumber` (texto \| null).
- **Errores:** los de hoy. **Zod:** `weighbridgePaymentSchema`, `processPaymentResultSchema`, `startPendingBillingResultSchema` (`F/features/weighbridge/contracts/payment.ts`).
- **Notas:** el frontend arma la petición desde el `BillingRecipientInput` de `AppChargeForm` (`P02/` D13): `totalAmount` → `amountReceived`; `paymentMode` elige el endpoint.

##### C-F03-11 · `POST weighbridge/cycles/{cycleId}/weighings` (modificado)
- **Política:** `ScaleAccess` (`WeighbridgeController.cs:484`).
- **Qué cambia** (sobre C-F01-80): un ciclo completo, de un solo pesaje y con un pesaje, acepta un segundo pesaje (tara en ingreso y solo báscula; bruto en salida): se reabre, registra el pesaje y se vuelve a cerrar (AF-11, AF-40), aunque el camión haya salido por Vigilancia. En almacenamiento, la mercancía pasa a indicador − tara con origen `Reweigh` (`P01/` D21). Hoy responde 409 «Este ciclo es de un solo pesaje y ya quedó cerrado con el primero.» (`B/Wms.Application/Weighbridge/Commands/Common/RecordWeighing/RecordWeighingHandler.cs:132-136`).
- **Petición:** la de hoy (`weight`, `weightType`, `observations`, `capturedAt`). **Respuesta 200:** la de hoy más `merchandiseWeight` (C-F01-80) y `state`.
- **Errores nuevos:** 409 «El ciclo ya tiene su repesaje: corríjalo con «Editar pesajes».» (un ciclo con dos pesajes); 409 «El pesaje está anulado.»; salen el 409 de `:135` para este caso y los de C-F01-80.
- **Zod:** `recordWeighingSchema`, `recordWeighingResultSchema` (`F/features/weighbridge/contracts/weighing.ts`).

##### C-F03-12 · `PATCH weighbridge/cycles/{cycleId}/second-weighing` (nuevo)
- **Política:** `ScaleAccess`. **Qué hace:** cambia «Req. 2.º pesaje» de un ciclo abierto (AF-11, D18).
- **Petición:** `{ "required": true | false }`.
- **Efecto:** `false` con el primer pesaje tomado cierra el ciclo con ese peso; `false` sin pesajes deja la entrada de un solo pesaje; `true` en un ciclo abierto pide el segundo pesaje.
- **Respuesta 200:** `dataSchema(secondWeighingResultSchema)` = `{ weighbridgeCycleId, singleWeightOnly, state }`.
- **Errores:** 404 «El ciclo de báscula no existe.»; 409 «El ciclo ya está cerrado: para agregar el repesaje use «Repesar».»; 409 «El pesaje está anulado.».
- **Zod:** `secondWeighingSchema`, `secondWeighingResultSchema` (`weighing.ts`).

##### C-F03-13 · `GET weighbridge/entries/{entryId}` (modificado)
- **Política:** `EntryEditAccess` (`B/Wms.Api/Controllers/v1/EntryCorrectionController.cs:29`). **Petición:** el Id de la entrada en la ruta.
- **Qué cambia** (sobre C-F01-93): suma `serviceRecordId`, `state`, `singleWeightOnly`, `firstWeightCapturedAt` y `charge`; `indicatorWeight` también trae el primer peso del vínculo cuando aún no hay ciclo; cada producto suma `packagingTypeId` (hoy la lectura no lo trae: nota de la fase 4 de `P01/` §8).
- **Respuesta 200:** `dataSchema(entryForEditSchema)`. **Errores:** 404 «La entrada no existe.». **Zod:** `entryForEditSchema` (`F/features/weighbridge/contracts/entry-edit.ts`).

##### C-F03-14 · `PUT weighbridge/entries/{entryId}` (modificado)
- **Política:** `ScaleAccess` (`EntryCorrectionController.cs:46`).
- **Qué cambia** (sobre C-F01-92): sin ciclo, `indicatorWeight` fija el primer peso del vínculo (con `indicatorCapturedAt` opcional) y no pide motivo; suma `singleWeightOnly` (solo sin ciclo o con el ciclo abierto; con el ciclo cerrado se ignora). Las demás reglas de C-F01-92 no cambian.
- **Petición:** `entryCorrectionScaleSchema` (con `singleWeightOnly` e `indicatorCapturedAt`). **Respuesta 200:** `dataSchema(depositEntrySchema)`.
- **Errores:** los de C-F01-92. **Zod:** `entryCorrectionScaleSchema`, `depositEntrySchema`.

##### C-F03-15 · `GET weighbridge/service-records/{serviceRecordId}/registration` (modificado)
- **Política:** `ScaleAccess` (`WeighbridgeController.cs:740`).
- **Petición:** el Id en la ruta y `entryLogId` en la consulta (obligatorio: un servicio de ingreso puede tener varios camiones, `P01/` D20). Sin él: 400 «Indique el camión.».
- **Qué cambia** (sobre C-F01-155, con R-UOM y R-SAL): suma `state`, `firstWeight`, `firstWeightCapturedAt`, `singleWeightOnly` (del vínculo), `driver`, `carrierCompany`, `vehicleCountry`, `stakeholder` (solo báscula), `weighbridgeCycleId`, `ticketNumber` y `charge`.
- **Respuesta 200:** `dataSchema(weighbridgeRegistrationSchema)`. **Errores:** 404 «La operación no existe.». **Zod:** `weighbridgeRegistrationSchema` (`registration.ts`).

##### C-F03-17 · `PUT entry-logs/{id}/correction` (modificado)
- **Política:** `EntryCorrectionAccess` (`B/Wms.Api/Controllers/v1/EntryLogCorrectionController.cs:18`, `:31`).
- **Qué cambia** (sobre C-F01-07, D3): `reason` pasa a opcional para un usuario con el rol Báscula y sin Receiving ni Admin, mientras ningún ciclo del camión esté completo; entonces la auditoría guarda «Corrección en el registro de báscula». En los demás casos sigue obligatorio.
- **Petición:** `entryLogCorrectionSchema` con `reason` opcional. **Respuesta 200:** la de C-F01-07.
- **Errores nuevos:** 400 «Indique el motivo de la corrección (de 10 a 500 caracteres).» cuando el motivo es obligatorio y falta; los de C-F01-07.
- **Zod:** `entryLogCorrectionSchema`, `entryLogCorrectionResultSchema` (`F/features/entries/contracts/entry-log-correction.ts`, que crea F03 con el texto de `P01/` §2.3 y este cambio).

##### C-F03-18 · `PATCH weighbridge/entry-log/{id}/info` (modificado)
- **Política:** `OperationalAccess` (`WeighbridgeSharedController.cs:35`). **Qué cambia:** `driverId` opcional (D13). **Petición:** la de hoy (`F/features/weighbridge/types/requests.ts:425`) más `driverId`. **Respuesta:** la de hoy. **Errores:** 400 «El conductor no existe o está inactivo.» y los de hoy. **Zod:** `entryInfoSchema` (`registration.ts`). **Notas:** F03 no lo llama; Vigilancia puede usarlo sin cambio.

##### C-F03-19 y C-F03-20 · altas rápidas de Báscula (retiradas)
- `POST weighbridge/stakeholders/quick` y `POST weighbridge/transport-companies/quick`: 404 desde la fase 1 (D1). Las reemplaza C-F01-141. Petición, respuesta, errores y Zod: no aplica.

##### C-F03-43 · `GET weighbridge/entry-logs/{id}` (sin cambios)
- **Política:** `ScaleAccess` (`WeighbridgeController.cs:828`). **Petición:** el Id del ingreso en la ruta. **Respuesta 200:** `dataSchema(pendingEntryLogSchema)` (forma de hoy, `F/features/weighbridge/types/pending-entry.ts`). **Errores:** 404 de hoy. **Zod:** `pendingEntryLogSchema` (`registration.ts`). **Notas:** precarga las secciones 1 y 2.

##### C-F03-44 · `GET weighbridge/shipping-document-types` (sin cambios)
- **Política:** `ActiveUser` (`B/Wms.Api/Controllers/v1/WeighbridgeCatalogController.cs:92`). **Petición:** —. **Respuesta 200:** `dataSchema(z.array(shippingDocumentTypeSchema))` (`B/Wms.Application/Weighbridge/Common/Dtos/Responses/ShippingDocumentTypeDto.cs`). **Errores:** ninguno. **Zod:** `shippingDocumentTypeSchema` (`registration.ts`).

##### C-F03-52 · `GET weighbridge/storage/document-candidates` (modificado)
- **Política:** la de hoy (`WeighbridgeController.cs:782`).
- **Qué cambia** (sobre C-F01-81): `partial=true` busca los números que contienen el texto (sin distinguir mayúsculas ni espacios), con al menos 3 caracteres, y devuelve hasta 20 depósitos abiertos, del más reciente al más antiguo. Sin `partial`, la comparación exacta de hoy (`StorageDocumentLookup.cs:30-32`).
- **Petición:** `number`, `primaryDocumentTypeId`, `partial` (bool, opcional). **Respuesta 200:** `dataSchema(z.array(documentCandidateSchema))`.
- **Errores nuevos:** 400 «Escriba al menos 3 caracteres del documento.» (con `partial`).
- **Zod:** `documentCandidateQuerySchema`, `documentCandidateSchema` (`registration.ts`; completa el esquema de cambio de `P01/` §2.3).

#### Grupo B — Cola, historial y detalle

##### C-F03-21 · `GET weighbridge/queue` (modificado)
- **Política:** `ScaleAccess` (`WeighbridgeController.cs:534`).
- **Qué cambia:** una fila por entrada (D24) y una por camión «Sin iniciar»; estados de D9; salen `mode`, `entryCount`, `weighingCount`, `awaitingWarehouseArrival`, `firstWeightType` y `operationType` (`B/Wms.Application/Weighbridge/Common/Dtos/WeighbridgeQueueItemDto.cs`); entran categoría, ids de la entrada, mercancía y los tres pesos.
- **Petición (consulta):** `state` (uno o varios, separados por coma; sin él, los cuatro de la cola) y `search` (placa o conductor; contiene, sin tildes ni mayúsculas).
- **Orden:** el de hoy, por ingreso ascendente y `id` (`GetWeighbridgeQueueHandler.cs:37-38`). **Paginación:** no; lista completa, con el tope de hoy.
- **Respuesta 200:** `dataSchema(z.array(queueItemSchema))`:

```jsonc
{
  "entryLogId": "guid", "serviceRecordId": "guid", "warehouseStorageEntryId": "guid", "weighbridgeCycleId": null,
  "category": "Entry", "state": "PendingPayment", "isDuplicateEntry": false,
  "vehiclePlate": "ABC123", "entryReasonName": "Descargue importación", "dateTimeEntry": "2026-11-10T21:35:00-05:00",
  "waitingMinutes": 12, "customerName": "Cliente A", "driverName": "Conductor 1",
  "operationModalityName": "Importación", "documentNumber": "CP-001",
  "merchandise": { "productName": "Cebolla", "packaging": "Sacos", "weight": 18000, "moreLines": 0 },
  "grossWeight": 30000, "merchandiseWeight": 18000, "tareWeight": 12000, "singleWeightOnly": false
}
```

  Pesos: en ingreso, bruto = indicador, mercancía (`P01/` D21) y tara (calculada o real); en salida, tara = primer pesaje, bruto = segundo y mercancía = diferencia; en solo báscula, bruto = pesaje. Nulos sin pesos.
- **Errores:** 400 «El valor «{valor}» no es válido para state.» (C-F01-00). **Zod:** `queueQuerySchema`, `queueItemSchema` (`F/features/weighbridge/contracts/queue.ts`).

##### C-F03-22 · `GET weighbridge/history/entries` (nuevo)
- **Política:** `ScaleAccess`. Orden y filtros (C-F01-00).
- **Petición (consulta):** paginación; `modality` (`Import` \| `Export` \| `Inspection`); `dateTimeEntryFrom`, `dateTimeEntryTo`; `vehiclePlate`, `driverName`, `driverIdNumber`, `document` (tipo o número), `ticketNumber` (texto); `hasReweigh` (bool); `state` (enum, varios).
- **Orden:** lista blanca `dateTimeEntry`, `vehiclePlate`, `driverName`, `ticketNumber`, `state`, `grossWeight`, `merchandiseWeight`; por defecto `dateTimeEntry desc` (H-007).
- **Respuesta 200:** `pagedSchema(historyEntryRowSchema)`: `warehouseStorageEntryId`, `entryLogId`, `serviceRecordId`, `weighbridgeCycleId`, `modality`, `dateTimeEntry`, `vehiclePlate`, `driverName`, `driverIdNumber`, `grossWeight`, `merchandiseWeight`, `tareWeight`, `quantity` (suma de lo declarado), `manifestWeight`, `documentTypeName`, `documentNumber`, `hasReweigh`, `chargedAmount`, `ticketNumber`, `isDuplicateEntry`, `state`, `voidReason`, `warehouseStorageNumber`, `warehouseStorageStatus` y `canEdit`, `canReweigh`, `canPrint`, `canVoid`.
- **Reglas de las acciones:** `canEdit` = no anulada y depósito en Borrador; `canReweigh` = ciclo completo, de un solo pesaje y con un pesaje; `canPrint` = ciclo con al menos un pesaje y tiquete; `canVoid` = no anulada.
- **Errores:** los de C-F01-00. **Zod:** `historyEntriesQuerySchema`, `historyEntryRowSchema` (`F/features/weighbridge/contracts/history.ts`).

##### C-F03-23 · `GET weighbridge/history/exits` (nuevo)
- **Política:** `ScaleAccess`. Orden y filtros (C-F01-00).
- **Petición (consulta):** paginación; `dateTimeEntryFrom`, `dateTimeEntryTo`; `vehiclePlate`, `driverName`, `driverIdNumber`, `product`, `exitNumber`, `ticketNumber` (texto); `hasReweigh`; `state`.
- **Orden:** lista blanca `dateTimeEntry`, `vehiclePlate`, `driverName`, `exitNumber`, `ticketNumber`, `state`; por defecto `dateTimeEntry desc`.
- **Respuesta 200:** `pagedSchema(historyExitRowSchema)`: `serviceRecordId`, `entryLogId`, `weighbridgeCycleId`, `exitId`, `exitNumber`, `dateTimeEntry`, `vehiclePlate`, `driverName`, `driverIdNumber`, `merchandise[]` (`productName`, `packaging`, `quantity`), `vehicleWeight`, `exitWeight`, `merchandiseWeight`, `hasReweigh`, `chargedAmount`, `ticketNumber`, `state`, `voidReason` y las cuatro marcas (`canEdit` = no anulada).
- **Errores:** los de C-F01-00. **Zod:** `historyExitsQuerySchema`, `historyExitRowSchema`.

##### C-F03-24 · `GET weighbridge/history/weighing-only` (nuevo)
- **Política:** `ScaleAccess`. Orden y filtros (C-F01-00).
- **Petición (consulta):** paginación; `dateTimeEntryFrom`, `dateTimeEntryTo`; `vehiclePlate`, `driverName`, `driverIdNumber`, `stakeholder` (nombre o NIT), `ticketNumber`; `state`.
- **Orden:** lista blanca `dateTimeEntry`, `vehiclePlate`, `driverName`, `stakeholderName`, `ticketNumber`, `state`; por defecto `dateTimeEntry desc`.
- **Respuesta 200:** `pagedSchema(historyWeighingOnlyRowSchema)`: `serviceRecordId`, `entryLogId`, `weighbridgeCycleId`, `dateTimeEntry`, `vehiclePlate`, `driverName`, `driverIdNumber`, `stakeholderName`, `stakeholderIdNumber`, `firstWeight` («Pesaje»), `reweighWeight` («Repesaje»), `differenceWeight` («Tara», D28), `chargedAmount`, `ticketNumber`, `state`, `voidReason` y las cuatro marcas.
- **Errores:** los de C-F01-00. **Zod:** `historyWeighingOnlyQuerySchema`, `historyWeighingOnlyRowSchema`.

##### C-F03-25, C-F03-26 y C-F03-34 · detalle (nuevos)
- **Rutas:** `GET weighbridge/entries/{entryId}/detail` (entrada de ingreso), `GET weighbridge/service-records/{serviceRecordId}/detail?entryLogId=` (salida o solo báscula) y `GET weighbridge/cycles/{cycleId}/detail` (cualquier ciclo, para `cycles/[id]`).
- **Política:** `ActiveUser` (en `WeighbridgeCycleReadController`, junto al detalle de hoy).
- **Petición:** el Id en la ruta; C-F03-26 lleva además `entryLogId` en la consulta.
- **Respuesta 200:** `dataSchema(weighbridgeDetailSchema)`: `category`, `state`, `isDuplicateEntry`, `singleWeightOnly`; los ids (`entryLogId`, `serviceRecordId`, `weighbridgeCycleId`, `warehouseStorageEntryId`, `warehouseStorageId`, `warehouseStorageNumber`, `warehouseStorageStatus`, `exitId`, `exitNumber`); `vehicle` (`plate`, `carrierCompanyName`, `country`, `vehicleType`); `driver` (`fullName`, `idType`, `idNumber`) o nulo; `entryReasonName`, `dateTimeEntry`, `stakeholderName`; `documentTypeName`, `documentNumber`, `modalityName`; `merchandise[]`; `weights` (`indicator`, `tare` con `isReal`, `manifest`, `merchandise` con `source`, cada uno con su fecha cuando la tiene, y `manifestExceedsDifference`); `weighings[]` (`id`, `sequence`, `weightType`, `weight`, `capturedAt`, `originalWeight`, `modificationReason`); `ticket` (`ticketNumber`, `chargedAmount`, `declaredWeight`, `isZero`) o nulo; `billing` (`invoiceNumber`, `customerName`, `totalCharged`, `statusLabel`) o nulo; `voided` (`at`, `byName`, `reason`) o nulo; `ticketObservations` (texto \| null: la observación guardada del tiquete, C-F03-36, que precarga el modal de impresión, D33; sumado en FE-2 con la respuesta del usuario del 2026-11-24, «Sumar al detalle»); `actions` (`canEdit`, `canEditWeights`, `canReweigh`, `canPrint`, `canVoid`).
- **Pesos por categoría:** ingreso, como P-BAS-02; salida, `indicator` = peso al salir, `tare` = vehículo vacío, `merchandise` = neto, sin manifiesto; solo báscula, `indicator` = pesaje, `tare` = repesaje, `merchandise` = diferencia.
- **Errores:** 404 «La entrada no existe.», «La operación no existe.» o «El ciclo de báscula no existe.»; 400 «Indique el camión.» (C-F03-26 sin `entryLogId`).
- **Zod:** `weighbridgeDetailSchema` (`F/features/weighbridge/contracts/detail.ts`).

##### C-F03-27 · `GET entry-logs` (modificado)
- **Política:** `GateAccess` (`B/Wms.Api/Controllers/v1/EntryLogController.cs:19`, `:52`). Orden y filtros (C-F01-00).
- **Qué cambia:** se conservan los filtros de hoy (`B/Wms.Application/Logistics/EntryLogs/Queries/GetAllEntryLogs/GetAllEntryLogsQuery.cs`: `vehicleId`, `licensePlate`, `driverId`, `entryReasonId`, `dateFrom`, `dateTo`, `hasDeparture`) y se suman `status` (enum, varios: `Registered`, `Completed`), `dateTimeEntryFrom`, `dateTimeEntryTo`, `dateTimeDepartureFrom`, `dateTimeDepartureTo` e `isCorrected`; `licensePlate` pasa a «contiene».
- **Petición (consulta):** paginación, los filtros de «Qué cambia» y el orden (C-F01-00).
- **Orden:** lista blanca `dateTimeEntry`, `dateTimeDeparture`, `licensePlate`, `status`; por defecto `dateTimeEntry desc`.
- **Respuesta 200:** `pagedSchema(entryLogSchema)` (`EntryLogDto`, `B/Wms.Application/Logistics/Common/Dtos/EntryLogDto.cs`, sin cambios).
- **Errores:** los de C-F01-00. **Zod:** `entryLogListQuerySchema`, `entryLogSchema` (`F/features/entries/contracts/entry-log.ts`).

##### C-F03-48 · `GET entry-logs/{id}` (sin cambios)
- **Política:** `GateAccess` (`EntryLogController.cs:41`). **Petición:** el Id en la ruta. **Respuesta 200:** `dataSchema(entryLogSchema)`. **Errores:** 404 de hoy. **Zod:** `entryLogSchema`.

##### C-F03-28 a C-F03-33 · lecturas retiradas
- `GET weighbridge/history` (`WeighbridgeController.cs:707`), `history/totals` (`:722`), `pending` (`:517`), `pending-second-weight` (`:562`), `cycles/open` (`:600`) y `cycles/open-by-plate` (`:582`): 404 desde la fase 2. Solo los llaman pantallas de Báscula (`F/features/weighbridge/composables/useWeighbridgeHistory.ts`, `useWeighbridgeHistoryTotals.ts`, `useWeighbridgePending.ts`, `usePendingSecondWeight.ts`, `useOpenCycles.ts`, `useOpenCycleByPlate.ts`). Petición, respuesta, errores y Zod: no aplica.

#### Grupo C — Tiquete, anulación y correcciones

##### C-F03-35 · `GET weighbridge/{id}/ticket/pdf` (modificado)
- **Política:** `ActiveUser` (`B/Wms.Api/Controllers/v1/WeighbridgeCycleReadController.cs:57`).
- **Qué cambia:** `sections` (uno o varios de `Entry`, `Tare` y `Reweigh`, separados por coma; sin el parámetro, los que existan) y `receipt` (bool; por defecto falso). El PDF toma el alto de su contenido (hoy fijo en 80 × 200 mm, `B/Wms.Application/Weighbridge/Common/Services/WeighbridgeTicketPdfService.cs:28`), lleva una línea por mercancía (producto · embalaje · cantidad), solo las secciones pedidas, el valor y la factura si `receipt`, la observación guardada (`:511-517`) y la leyenda de documento interno. Marca la primera impresión como hoy.
- **Petición:** el Id del ciclo en la ruta; `sections` y `receipt` en la consulta.
- **Respuesta 200:** `application/pdf`.
- **Errores nuevos:** 400 «Elija al menos una sección del tiquete.»; 400 «El valor «{valor}» no es válido para sections.»; 409 «El pesaje aún no tiene el primer peso: no hay tiquete que imprimir.»; 409 «El repesaje aún no existe: quite «Repesaje» del tiquete.»; 404 «El ciclo de báscula no existe.».
- **Zod:** `ticketPdfQuerySchema` (`F/features/weighbridge/contracts/ticket.ts`); la respuesta es un `Blob`.

##### C-F03-36 · `PATCH weighbridge/{id}/ticket-observations` (sin cambios)
- **Política:** `ScaleAccess` (`WeighbridgeController.cs:900`). **Petición:** `{ "observations": "texto" | null }` (`UpdateTicketObservationsRequest`). **Respuesta:** la de hoy, sin cuerpo útil. **Errores:** los de hoy. **Zod:** `ticketObservationsSchema` (`ticket.ts`).

##### C-F03-37 · `POST weighbridge/entries/{entryId}/void` (nuevo)
- **Política:** `ScaleAccess` (en `WeighbridgeVoidController`).
- **Qué hace:** anula una entrada de ingreso, con o sin ciclo (D34). Con ciclo, lo de hoy de `POST weighbridge/cycles/{cycleId}/void` (`B/Wms.Api/Controllers/v1/WeighbridgeVoidController.cs:33`). Sin ciclo: anula la entrada con su motivo, saca su mercancía del depósito con su movimiento, anula el depósito en Borrador que se queda sin entradas, borra el vínculo y el camión vuelve a «Sin iniciar».
- **Petición:** `{ "reason": "…" }` (10 a 500). **Respuesta 200:** `dataSchema(voidResultSchema)` (forma de hoy, `F/features/weighbridge/types/weighbridge-cycle.ts:284-293`, con `weighbridgeCycleId` nulo sin ciclo).
- **Errores:** 404 «La entrada no existe.»; 409 «La entrada ya está anulada.»; los de hoy de la anulación del ciclo (`VoidWeighingCommandHandler.cs:40-114`).
- **Zod:** `voidRequestSchema`, `voidResultSchema` (`F/features/weighbridge/contracts/void.ts`).

##### C-F03-38 · `POST weighbridge/service-records/{serviceRecordId}/void` (nuevo)
- **Política:** `ScaleAccess`. **Qué hace:** anula una salida o un solo pesaje, con o sin ciclo (D34). Con ciclo, lo de hoy; sin ciclo, descarta el servicio con el motivo en la auditoría, borra el vínculo y el camión vuelve a «Sin iniciar». Una salida en Borrador creada por Báscula queda para que CE la cancele (`P01/` D34).
- **Petición:** `{ "entryLogId": "guid", "reason": "…" }`. **Respuesta 200:** `dataSchema(voidResultSchema)`.
- **Errores:** 404 «La operación no existe.»; 409 «La operación ya está anulada.»; 409 «Es un ingreso: anúlelo por su entrada.»; los de hoy.
- **Zod:** `serviceVoidRequestSchema`, `voidResultSchema`.

##### C-F03-16 · `PUT weighbridge/service-records/{serviceRecordId}` (nuevo)
- **Política:** `ScaleAccess`.
- **Qué hace:** guarda o corrige el registro de una salida o un solo pesaje (D35). Sin ciclo: el registro antes del cobro (primer peso, modo, conductor, transportadora, tercero), sin motivo. Con ciclo abierto: lo mismo, más la corrección del primer pesaje. Con ciclo completo: P-TR-12 (AF-135), con motivo.
- **Petición:** `serviceRecordUpdateSchema`:

| Campo | Tipo | Obligatorio | Regla |
| --- | --- | --- | --- |
| `entryLogId` | guid | Sí | El camión de la entrada |
| `licensePlate` | string \| null | No | Como C-F01-07 |
| `dateTimeEntry` | fecha y hora \| null | No | Límites de `DEC-012` y `DEC-051` |
| `driverId` | guid \| null | No | Conductor activo (D13) |
| `carrierCompanyId` | guid \| null | No | Tercero con rol `TRANSPORT_COMPANY` |
| `stakeholderId` | guid \| null | No | Solo báscula: el tercero (D14) |
| `firstWeight` | decimal \| null | No | > 0 |
| `secondWeight` | decimal \| null | No | > 0; solo si el ciclo tiene segundo pesaje |
| `singleWeightOnly` | bool \| null | No | Solo sin ciclo o con el ciclo abierto |
| `reason` | string \| null | Con el ciclo completo | 10 a 500 |

- **Efectos:** placa y fecha con las reglas de C-F01-07; pesos de un ciclo con el registro del original, como hoy; con el ciclo completo, el aviso «Modificación de Peso en Báscula» (D35); placa o conductor de una salida con guía, el aviso de `P01/` D45; con el conductor o la placa en Borrador, pasan a la salida (`P01/` D37).
- **Respuesta 200:** `dataSchema(weighbridgeRegistrationSchema)` (la de C-F03-15) más `changes[]` (`field`, `previousValue`, `newValue`) y `notifiedForeignTrade` (bool).
- **Errores:** 404 «La operación no existe.»; 409 «La operación está anulada: no se corrige.»; 409 «Es un ingreso: corríjalo por su entrada.»; 400 «Indique el motivo de la corrección (de 10 a 500 caracteres).»; 400 «El ciclo no tiene repesaje.»; 400 «El conductor no existe o está inactivo.»; los de fecha y placa de C-F01-07.
- **Zod:** `serviceRecordUpdateSchema`, `serviceRecordUpdateResultSchema` (`F/features/weighbridge/contracts/service-record.ts`).

##### C-F03-45 y C-F03-46 · corrección de pesos de hoy (modificados en su efecto)
- `PATCH weighbridge/{id}/first-weight-modify` y `PATCH weighbridge/{id}/second-weight` (`B/Wms.Api/Controllers/v1/WeighbridgeCorrectionController.cs:36`, `:63`). **Política:** `WeighingCorrectionAccess` (sin cambios).
- **Qué cambia:** solo el efecto (D32): en un ciclo de almacenamiento recalculan la mercancía de su entrada (`P01/` D21) y la factura del período (`DEC-022`).
- **Petición:** `{ newWeight, reason }` y `{ newWeight, reason, weighingId? }`. **Respuesta:** la de hoy (`F/features/weighbridge/types/requests.ts:441-473`). **Errores:** los de hoy.
- **Zod:** `modifyFirstWeightSchema`, `modifyFirstWeightResultSchema`, `modifySecondWeightSchema`, `modifySecondWeightResultSchema` (`weighing.ts`). **Notas:** las usa `cycles/[id]` con el diálogo de hoy; las pantallas nuevas no.

##### C-F03-49, C-F03-50 y C-F03-51 · acciones de hoy (sin cambios)
- **C-F03-49 · `POST entry-logs/{id}/departure-authorizations`:** **Política:** `GateAccess` (`EntryLogController.cs:19`, `:76`). **Petición:** `{ "observations": "texto" | null }`. **Respuesta:** la de hoy. **Errores:** los de hoy (404 del ingreso y los de su validador). **Zod:** `departureAuthorizationSchema` (`entry-log.ts`).
- **C-F03-50 · `POST entry-logs/{id}/manifests`:** **Política:** `GateAccess` (`:90`). **Petición:** `{ "manifestNumber": "M-123", "manifestWeight": 18000 | null }`. **Respuesta:** la de hoy. **Errores:** los de hoy. **Zod:** `manifestCreateSchema` (`entry-log.ts`).
- **C-F03-51 · `PATCH warehouse-storages/{id}/entry-date`:** **Política:** `DepositEntryDateAccess` (`B/Wms.Api/Controllers/v1/DepositEntryDateController.cs:16`, `:28`). **Petición:** `{ "entryDate": "fecha y hora", "reason": "…" }` (`CorrectDepositEntryDateRequest`). **Respuesta 200:** `CorrectDepositEntryDateResultDto`, la de hoy. **Errores:** 404 y 400 de hoy (límites de `DEC-012` y `DEC-051`). **Zod:** `depositEntryDateSchema` (`entry-log.ts`); la llama el componente de hoy desde `cycles/[id]` (D32), que no se maqueta.

##### C-F03-39, C-F03-40 y C-F03-41 · retirados
- `GET weighbridge/recoverable` (`WeighbridgeController.cs:618`), `DELETE weighbridge/incomplete/{serviceRecordId}` (`:636`) y `GET weighbridge/entries/{entryId}/ticket/pdf` (`WeighbridgeCycleReadController.cs:80`): 404 desde la fase 3. Solo los llaman `recover.vue` y `WeighbridgeCycleTickets.vue`, que se borran. Petición, respuesta, errores y Zod: no aplica.

### 2.3 Esquemas Zod y tipos

Zod 4 (`Frontend/wms/package.json`: `"zod": "^4.1.13"`), con las reglas de `P01/` §2.3: Id con `z.guid()`, fechas con hora con `z.iso.datetime({ offset: true })`, días con `z.iso.date()`, tipos con `z.infer`. Las lecturas de hoy sin cambio de forma usan `.loose()` para no fallar por campos que la pantalla no usa; I-03 valida cada esquema contra el API real, como I-01.

**Archivos que F03 crea copiando el texto de `P01/` §2.3, sin cambios:** `F/features/foreign-trade/contracts/deposit-entry.ts` (bloque de `P01/` §2.3 que empieza en «`F/features/foreign-trade/contracts/deposit-entry.ts`»: `depositEntrySchema`, `depositEntryProductSchema` y `entryCorrectionCeSchema`; F05 lo amplía) y `F/features/exits/contracts/exit.ts` (`exitSchema` completo; F06 lo amplía).

**`F/features/weighbridge/contracts/common.ts`**

```ts
import { z } from "zod";
import { guidSchema } from "~/shared/contracts/api";

export const weighbridgeEntryStateSchema = z.enum([
  "NotStarted", "PendingWeighing", "PendingPayment", "PendingReweigh", "Completed", "Voided",
]);
export const WEIGHBRIDGE_ENTRY_STATE_LABELS: Record<z.infer<typeof weighbridgeEntryStateSchema>, string> = {
  NotStarted: "Sin iniciar", PendingWeighing: "Por pesar", PendingPayment: "Por cobrar",
  PendingReweigh: "Por repesar", Completed: "Completado", Voided: "Anulado",
};
export const weighbridgeCategorySchema = z.enum(["Entry", "Exit", "WeighingOnly"]);
export const weightTypeSchema = z.enum(["Gross", "Tare"]);
export const chargeSchema = z.object({
  weighingPrice: z.number(), taxAmount: z.number(), totalAmount: z.number(),
  isAgreementZero: z.boolean(), isZeroCharge: z.boolean(),
});
export const merchandiseLineSchema = z.object({
  productName: z.string(), packaging: z.string().nullable(), quantity: z.number().nullable(),
});
export const personSummarySchema = z.object({
  id: guidSchema, fullName: z.string(), idType: z.string(), idNumber: z.string(),
});
export type WeighbridgeEntryState = z.infer<typeof weighbridgeEntryStateSchema>;
export type WeighbridgeCategory = z.infer<typeof weighbridgeCategorySchema>;
export type Charge = z.infer<typeof chargeSchema>;
```

**`F/features/weighbridge/contracts/queue.ts`** — C-F03-21

```ts
import { z } from "zod";
import { dateTimeSchema, guidSchema } from "~/shared/contracts/api";
import { weighbridgeCategorySchema, weighbridgeEntryStateSchema } from "./common";

export const queueStateSchema = weighbridgeEntryStateSchema.extract([
  "NotStarted", "PendingWeighing", "PendingPayment", "PendingReweigh",
]);
export const queueQuerySchema = z.object({
  state: z.array(queueStateSchema).optional(), // se envía separado por comas
  search: z.string().trim().optional(),
});
export const queueItemSchema = z.object({
  entryLogId: guidSchema,
  serviceRecordId: guidSchema.nullable(),
  warehouseStorageEntryId: guidSchema.nullable(),
  weighbridgeCycleId: guidSchema.nullable(),
  category: weighbridgeCategorySchema.nullable(),
  state: queueStateSchema,
  isDuplicateEntry: z.boolean(),
  vehiclePlate: z.string(),
  entryReasonName: z.string().nullable(),
  dateTimeEntry: dateTimeSchema,
  waitingMinutes: z.int().min(0),
  customerName: z.string().nullable(),
  driverName: z.string().nullable(),
  operationModalityName: z.string().nullable(),
  documentNumber: z.string().nullable(),
  merchandise: z.object({
    productName: z.string(), packaging: z.string().nullable(),
    weight: z.number().nullable(), moreLines: z.int().min(0),
  }).nullable(),
  grossWeight: z.number().nullable(),
  merchandiseWeight: z.number().nullable(),
  tareWeight: z.number().nullable(),
  singleWeightOnly: z.boolean().nullable(),
});
export type QueueItem = z.infer<typeof queueItemSchema>;
export type QueueQuery = z.infer<typeof queueQuerySchema>;
```

**`F/features/weighbridge/contracts/registration.ts`** — C-F03-01 a C-F03-04, C-F03-15, C-F03-18, C-F03-43, C-F03-44 y C-F03-52

```ts
import { z } from "zod";
import { dateTimeSchema, guidSchema, identificationTypeSchema } from "~/shared/contracts/api";
import { chargeSchema, merchandiseLineSchema, personSummarySchema, weighbridgeCategorySchema,
  weighbridgeEntryStateSchema } from "./common";

const weightSchema = z.number().positive();

/** Datos del camión y del conductor (EntryLogInfoInput, con driverId por D13). */
export const entryInfoSchema = z.object({
  driverId: guidSchema.nullable().optional(),
  driverFirstName: z.string().trim().nullable().optional(),
  driverLastName: z.string().trim().nullable().optional(),
  driverIdNumber: z.string().trim().nullable().optional(),
  driverIdType: identificationTypeSchema.nullable().optional(),
  driverCountry: z.string().nullable().optional(),
  driverPhoneNumber: z.string().nullable().optional(),
  carrierCompanyId: guidSchema.nullable().optional(),
  vehicleCountry: z.string().nullable().optional(),
  vehicleType: z.string().nullable().optional(),
});

const firstWeightFields = {
  firstWeight: weightSchema.nullable().optional(),
  firstWeightCapturedAt: dateTimeSchema.nullable().optional(),
};

export const storageProductItemSchema = z.object({
  productId: guidSchema.nullable(),
  productDescription: z.string().trim().max(200).nullable().optional(),
  packagingTypeId: guidSchema.nullable().optional(),
  declaredQuantity: z.number().positive().nullable().optional(),
  entryDeclaredQuantity: z.number().positive().nullable().optional(),
});

/** C-F03-02 (y base de C-F03-01). Los campos que AF-10 quita del formulario no se envían. */
export const storageInitiateSchema = z.object({
  entryLogId: guidSchema,
  operationModalityCode: z.string(),
  cargoManifestNumber: z.string().trim().max(50).nullable(),
  primaryDocumentTypeId: guidSchema.nullable(),
  documentDate: dateTimeSchema.nullable().optional(),
  customerId: guidSchema.nullable().optional(),
  customerRoleId: guidSchema.nullable().optional(),
  importerId: guidSchema.nullable().optional(),
  importerRoleId: guidSchema.nullable().optional(),
  exporterId: guidSchema.nullable().optional(),
  exporterRoleId: guidSchema.nullable().optional(),
  importAgencyId: guidSchema.nullable().optional(),
  importAgencyRoleId: guidSchema.nullable().optional(),
  intermediaryId: guidSchema.nullable().optional(),
  intermediaryRoleId: guidSchema.nullable().optional(),
  manifestNumber: z.string().trim().max(100).nullable(),
  manifestWeight: weightSchema.nullable(),
  merchandiseWeight: weightSchema.nullable(),
  carrierCompanyId: guidSchema,
  products: z.array(storageProductItemSchema).nullable(),
  inspectionDescription: z.string().trim().min(10).max(500).nullable(),
  targetWarehouseStorageId: guidSchema.nullable(),
  singleWeightOnly: z.boolean().optional(),
  ...firstWeightFields,
});
/** C-F03-01: lo mismo, más los datos del camión y del conductor (la transportadora sigue obligatoria). */
export const storageRegisterSchema = entryInfoSchema.extend(storageInitiateSchema.shape);

const registrationResultBase = z.object({
  serviceRecordId: guidSchema,
  entryLogId: guidSchema,
  customerId: guidSchema.nullable(),
  customerName: z.string().nullable(),
  weighingPrice: z.number(),
  taxAmount: z.number(),
  totalAmount: z.number(),
  isAgreementZero: z.boolean(),
  observations: z.string().nullable(),
  singleWeightOnly: z.boolean(),
  configuredFirstWeightType: z.string().nullable(),
  state: weighbridgeEntryStateSchema.extract(["PendingWeighing", "PendingPayment"]),
  firstWeight: z.number().nullable(),
  charge: chargeSchema,
});
export const storageRegisterResultSchema = registrationResultBase.extend({
  cargoManifestNumber: z.string().nullable(),
  warehouseStorageId: guidSchema.nullable(),
  warehouseStorageNumber: z.string().nullable(),
  warehouseStorageEntryId: guidSchema,
  weighbridgeCycleId: guidSchema.nullable(), // nulo: el ciclo nace en el cobro
  isFirstTruck: z.boolean(),
  isDuplicateEntry: z.boolean(),
  isLateTruck: z.boolean(),
  isPerishable: z.boolean(),
  documentDate: dateTimeSchema.nullable(),
  createdProducts: z.array(z.object({ productId: guidSchema, name: z.string(), sku: z.string() })),
  entryLogUpdated: z.boolean().optional(), // solo en C-F03-01
});

/** C-F03-03. */
export const outputInitiateSchema = entryInfoSchema.extend({
  entryLogId: guidSchema,
  exitId: guidSchema.nullable(),
  driverId: guidSchema.nullable(),
  observations: z.string().max(500).nullable().optional(),
  requiresReweigh: z.boolean().optional(),
  ...firstWeightFields,
});
export const outputInitiateResultSchema = registrationResultBase.extend({
  exitId: guidSchema,
  exitNumber: z.string(),
  exitCreated: z.boolean(),
  driverChangeNotified: z.boolean(),
  warehouseStorageId: guidSchema.nullable(),
});

/** C-F03-04: customerId es el «Tercero» (cualquier rol); sin peso esperado. */
export const weighingOnlyInitiateSchema = entryInfoSchema.extend({
  entryLogId: guidSchema,
  customerId: guidSchema.nullable().optional(),
  observations: z.string().max(500).nullable().optional(),
  singleWeightOnly: z.boolean().optional(),
  ...firstWeightFields,
});
export const weighingOnlyInitiateResultSchema = registrationResultBase;

/** C-F03-15: lectura de una salida o un solo pesaje (y la respuesta base de C-F03-16). */
export const weighbridgeRegistrationSchema = z.object({
  serviceRecordId: guidSchema,
  entryLogId: guidSchema,
  category: weighbridgeCategorySchema,
  state: weighbridgeEntryStateSchema,
  operationModalityCode: z.string().nullable(),
  operationModalityName: z.string().nullable(),
  customerId: guidSchema.nullable(),
  customerName: z.string().nullable(),
  stakeholder: z.object({ id: guidSchema, name: z.string(), idNumber: z.string().nullable() }).nullable(),
  driver: personSummarySchema.nullable(),
  carrierCompany: z.object({ id: guidSchema, name: z.string() }).nullable(),
  vehicleCountry: z.string().nullable(),
  exitId: guidSchema.nullable(),
  exitNumber: z.string().nullable(),
  warehouseStorageId: guidSchema.nullable(),
  warehouseStorageNumber: z.string().nullable(),
  lines: z.array(merchandiseLineSchema),
  singleWeightOnly: z.boolean(),
  firstWeight: z.number().nullable(),
  firstWeightCapturedAt: dateTimeSchema.nullable(),
  weighbridgeCycleId: guidSchema.nullable(),
  ticketNumber: z.string().nullable(),
  charge: chargeSchema,
});

/** C-F03-43 (forma de hoy). */
export const pendingEntryLogSchema = z.object({
  id: guidSchema,
  vehicleId: guidSchema,
  vehiclePlate: z.string(),
  vehicleCountry: z.string().nullable().optional(),
  vehicleType: z.string().nullable().optional(),
  carrierCompanyId: guidSchema.nullable().optional(),
  carrierCompanyName: z.string().nullable().optional(),
  driverId: guidSchema.nullable(),
  driverName: z.string().nullable(),
  driverIdType: z.string().nullable(),
  driverIdNumber: z.string().nullable(),
  entryReasonId: guidSchema.nullable(),
  entryReasonName: z.string().nullable(),
  dateTimeEntry: dateTimeSchema,
  status: z.string(),
  observations: z.string().nullable(),
}).loose();

/** C-F03-44 (forma de hoy). */
export const shippingDocumentTypeSchema = z.object({
  id: guidSchema, name: z.string(), code: z.string(),
  description: z.string().nullable().optional(), operationModalityId: guidSchema.nullable().optional(),
}).loose();

/** C-F03-52 (completa documentCandidateChangesSchema de P01/ §2.3). */
export const documentCandidateQuerySchema = z.object({
  number: z.string().trim().min(1),
  primaryDocumentTypeId: guidSchema,
  partial: z.boolean().optional(),
});
export const documentCandidateSchema = z.object({
  warehouseStorageId: guidSchema,
  warehouseStorageNumber: z.string(),
  documentNumber: z.string(),
  status: z.string(),
  isOpen: z.boolean(),
  isMigrated: z.boolean(),
  operationModalityCode: z.string().nullable(),
  operationModalityName: z.string(),
  documentDate: dateTimeSchema.nullable(),
  customerName: z.string().nullable(),
  importerName: z.string().nullable(),
  exporterName: z.string().nullable(),
  customsAgencyName: z.string().nullable(),
  carrierNames: z.array(z.string()),
  plates: z.array(z.string()),
  truckCount: z.int().min(0),
}).loose();
export type StorageRegister = z.infer<typeof storageRegisterSchema>;
export type WeighbridgeRegistration = z.infer<typeof weighbridgeRegistrationSchema>;
export type DocumentCandidate = z.infer<typeof documentCandidateSchema>;
```

`documentNumber` es nuevo en el candidato: con `partial` el operario necesita ver qué número coincidió. El backend lo agrega en C-F03-52.

**`F/features/weighbridge/contracts/payment.ts`** — C-F03-05 a C-F03-10

```ts
import { z } from "zod";
import { dateTimeSchema, guidSchema } from "~/shared/contracts/api";
import { paymentMethodSchema } from "~/features/billing/contracts/billing-recipient";
import { weighbridgeEntryStateSchema } from "./common";

export const weighbridgePaymentSchema = z.object({
  serviceRecordId: guidSchema,
  entryLogId: guidSchema,
  paymentMethod: paymentMethodSchema,
  amountReceived: z.number().min(0),
  referenceNumber: z.string().max(100).nullable().optional(),
  notes: z.string().nullable().optional(),
  unregisteredRecipient: z.object({
    name: z.string().trim().min(3), idType: z.string(), idNumber: z.string().trim().min(1),
  }).loose().nullable().optional(),
  invoiceNumber: z.string().nullable().optional(),
  recipientMode: z.enum(["registered", "unregistered", "finalConsumer"]),
  customerId: guidSchema.nullable().optional(),
});
const paymentResultState = {
  state: weighbridgeEntryStateSchema.extract(["PendingWeighing", "PendingReweigh", "Completed"]),
  ticketNumber: z.string().nullable(),
};
export const processPaymentResultSchema = z.object({
  weighbridgeCycleId: guidSchema,
  invoiceId: guidSchema,
  invoiceNumber: z.string().nullable(),
  totalAmount: z.number(),
  amountReceived: z.number(),
  paymentMethod: z.string(),
  readyForWeighing: z.boolean(),
  paymentDate: dateTimeSchema,
  isZeroInvoice: z.boolean(),
  ...paymentResultState,
});
export const startPendingBillingResultSchema = z.object({
  weighbridgeCycleId: guidSchema,
  readyForWeighing: z.boolean(),
  invoiceId: guidSchema,
  invoiceNumber: z.string().nullable(),
  totalAmount: z.number(),
  isZeroInvoice: z.boolean(),
  ...paymentResultState,
});
export type WeighbridgePayment = z.infer<typeof weighbridgePaymentSchema>;
```

**`F/features/weighbridge/contracts/weighing.ts`** — C-F03-11, C-F03-12, C-F03-45 y C-F03-46

```ts
import { z } from "zod";
import { dateTimeSchema, guidSchema, reasonSchema } from "~/shared/contracts/api";
import { weighbridgeEntryStateSchema, weightTypeSchema } from "./common";

export const recordWeighingSchema = z.object({
  weight: z.number().positive(),
  weightType: weightTypeSchema,
  observations: z.string().max(500).nullable().optional(),
  capturedAt: dateTimeSchema.nullable().optional(),
});
export const recordWeighingResultSchema = z.object({
  weighingId: guidSchema,
  sequence: z.int().min(0),
  cycleStatus: z.string(),
  ticketNumber: z.string().nullable(),
  affectedWarehouseStorageEntryIds: z.array(guidSchema),
  cycleCompleted: z.boolean(),
  merchandiseWeight: z.number().nullable(),
  state: weighbridgeEntryStateSchema,
});
export const secondWeighingSchema = z.object({ required: z.boolean() });
export const secondWeighingResultSchema = z.object({
  weighbridgeCycleId: guidSchema, singleWeightOnly: z.boolean(), state: weighbridgeEntryStateSchema,
});
export const modifyFirstWeightSchema = z.object({ newWeight: z.number().positive(), reason: reasonSchema });
export const modifySecondWeightSchema = modifyFirstWeightSchema.extend({ weighingId: guidSchema.nullable().optional() });
export const modifyFirstWeightResultSchema = z.object({
  weighbridgeCycleId: guidSchema, originalFirstWeight: z.number(), newFirstWeight: z.number(),
  newNetWeight: z.number(), modifiedBy: z.string(), modifiedAt: dateTimeSchema, reason: z.string(),
}).loose();
export const modifySecondWeightResultSchema = z.object({
  weighbridgeCycleId: guidSchema, originalSecondWeight: z.number(), newSecondWeight: z.number(),
  newNetWeight: z.number(), modifiedBy: z.string(), modifiedAt: dateTimeSchema, reason: z.string(),
}).loose();
```

**`F/features/weighbridge/contracts/entry-edit.ts`** — C-F03-13 y C-F03-14

```ts
import { z } from "zod";
import { dateTimeSchema, guidSchema, reasonSchema } from "~/shared/contracts/api";
import { entryReasonCategorySchema } from "~/features/entries/contracts/entry-reason";
import { depositEntryProductSchema, depositEntrySchema, entryCorrectionCeSchema }
  from "~/features/foreign-trade/contracts/deposit-entry";
import { chargeSchema, weighbridgeEntryStateSchema } from "./common";

export const entryForEditSchema = depositEntrySchema.extend({
  entryProducts: z.array(depositEntryProductSchema.extend({ packagingTypeId: guidSchema.nullable() })),
  serviceRecordId: guidSchema,
  entryLogId: guidSchema,
  licensePlate: z.string(),
  entryReasonId: guidSchema.nullable(),
  entryReasonCategory: entryReasonCategorySchema.nullable(),
  dateTimeEntry: dateTimeSchema,
  driver: z.object({ id: guidSchema, firstName: z.string(), lastName: z.string(), idType: z.string(), idNumber: z.string() }).nullable(),
  vehicleCountry: z.string().nullable(),
  modalityCode: z.string(),
  warehouseStorageId: guidSchema,
  warehouseStorageNumber: z.string(),
  warehouseStorageStatus: z.enum(["Draft", "Confirmed", "Closed", "Cancelled"]),
  usesCargoUnits: z.boolean(),
  cargoUnits: z.array(z.object({ id: guidSchema, cargoUnitTypeId: guidSchema, identifier: z.string() })),
  canScaleEdit: z.boolean(),
  state: weighbridgeEntryStateSchema,
  singleWeightOnly: z.boolean(),
  firstWeightCapturedAt: dateTimeSchema.nullable(),
  charge: chargeSchema,
});
export const entryCorrectionScaleSchema = entryCorrectionCeSchema
  .omit({ merchandiseValue: true, usesCargoUnits: true, cargoUnits: true, manifestDate: true })
  .extend({
    reason: reasonSchema.nullable(),
    indicatorCapturedAt: dateTimeSchema.nullable().optional(),
    singleWeightOnly: z.boolean().optional(),
  });
export type EntryForEdit = z.infer<typeof entryForEditSchema>;
export type EntryCorrectionScale = z.infer<typeof entryCorrectionScaleSchema>;
```

**`F/features/weighbridge/contracts/history.ts`** — C-F03-22 a C-F03-24

```ts
import { z } from "zod";
import { dateOnlySchema, dateTimeSchema, guidSchema, listQueryBaseSchema } from "~/shared/contracts/api";
import { merchandiseLineSchema, weighbridgeEntryStateSchema } from "./common";

const historyStateSchema = weighbridgeEntryStateSchema.exclude(["NotStarted"]);
const historyDateFilters = {
  dateTimeEntryFrom: dateOnlySchema.optional(),
  dateTimeEntryTo: dateOnlySchema.optional(),
  vehiclePlate: z.string().optional(),
  driverName: z.string().optional(),
  driverIdNumber: z.string().optional(),
  ticketNumber: z.string().optional(),
  state: z.array(historyStateSchema).optional(), // separado por comas
};
const actionFlags = {
  canEdit: z.boolean(), canReweigh: z.boolean(), canPrint: z.boolean(), canVoid: z.boolean(),
};
export const historyModalitySchema = z.enum(["Import", "Export", "Inspection"]);

export const historyEntriesQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["dateTimeEntry", "vehiclePlate", "driverName", "ticketNumber", "state",
    "grossWeight", "merchandiseWeight"]).optional(),
  modality: historyModalitySchema.optional(),
  document: z.string().optional(),
  hasReweigh: z.boolean().optional(),
  ...historyDateFilters,
});
export const historyEntryRowSchema = z.object({
  warehouseStorageEntryId: guidSchema,
  entryLogId: guidSchema,
  serviceRecordId: guidSchema,
  weighbridgeCycleId: guidSchema.nullable(),
  modality: historyModalitySchema,
  dateTimeEntry: dateTimeSchema,
  vehiclePlate: z.string(),
  driverName: z.string().nullable(),
  driverIdNumber: z.string().nullable(),
  grossWeight: z.number().nullable(),
  merchandiseWeight: z.number().nullable(),
  tareWeight: z.number().nullable(),
  quantity: z.number().nullable(),
  manifestWeight: z.number().nullable(),
  documentTypeName: z.string().nullable(),
  documentNumber: z.string().nullable(),
  hasReweigh: z.boolean(),
  chargedAmount: z.number().nullable(),
  ticketNumber: z.string().nullable(),
  isDuplicateEntry: z.boolean(),
  state: historyStateSchema,
  voidReason: z.string().nullable(),
  warehouseStorageNumber: z.string(),
  warehouseStorageStatus: z.enum(["Draft", "Confirmed", "Closed", "Cancelled"]),
  ...actionFlags,
});

export const historyExitsQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["dateTimeEntry", "vehiclePlate", "driverName", "exitNumber", "ticketNumber", "state"]).optional(),
  product: z.string().optional(),
  exitNumber: z.string().optional(),
  hasReweigh: z.boolean().optional(),
  ...historyDateFilters,
});
export const historyExitRowSchema = z.object({
  serviceRecordId: guidSchema,
  entryLogId: guidSchema,
  weighbridgeCycleId: guidSchema.nullable(),
  exitId: guidSchema.nullable(),
  exitNumber: z.string().nullable(),
  dateTimeEntry: dateTimeSchema,
  vehiclePlate: z.string(),
  driverName: z.string().nullable(),
  driverIdNumber: z.string().nullable(),
  merchandise: z.array(merchandiseLineSchema),
  vehicleWeight: z.number().nullable(),
  exitWeight: z.number().nullable(),
  merchandiseWeight: z.number().nullable(),
  hasReweigh: z.boolean(),
  chargedAmount: z.number().nullable(),
  ticketNumber: z.string().nullable(),
  state: historyStateSchema,
  voidReason: z.string().nullable(),
  ...actionFlags,
});

export const historyWeighingOnlyQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["dateTimeEntry", "vehiclePlate", "driverName", "stakeholderName", "ticketNumber", "state"]).optional(),
  stakeholder: z.string().optional(),
  ...historyDateFilters,
});
export const historyWeighingOnlyRowSchema = z.object({
  serviceRecordId: guidSchema,
  entryLogId: guidSchema,
  weighbridgeCycleId: guidSchema.nullable(),
  dateTimeEntry: dateTimeSchema,
  vehiclePlate: z.string(),
  driverName: z.string().nullable(),
  driverIdNumber: z.string().nullable(),
  stakeholderName: z.string().nullable(),
  stakeholderIdNumber: z.string().nullable(),
  firstWeight: z.number().nullable(),
  reweighWeight: z.number().nullable(),
  differenceWeight: z.number().nullable(), // «Tara» del legacy (D28)
  chargedAmount: z.number().nullable(),
  ticketNumber: z.string().nullable(),
  state: historyStateSchema,
  voidReason: z.string().nullable(),
  ...actionFlags,
});
export type HistoryEntryRow = z.infer<typeof historyEntryRowSchema>;
export type HistoryExitRow = z.infer<typeof historyExitRowSchema>;
export type HistoryWeighingOnlyRow = z.infer<typeof historyWeighingOnlyRowSchema>;
```

**`F/features/weighbridge/contracts/detail.ts`** — C-F03-25, C-F03-26 y C-F03-34

```ts
import { z } from "zod";
import { dateTimeSchema, guidSchema } from "~/shared/contracts/api";
import { merchandiseLineSchema, weighbridgeCategorySchema, weighbridgeEntryStateSchema, weightTypeSchema } from "./common";

const datedWeight = z.object({ weight: z.number(), capturedAt: dateTimeSchema.nullable() });
export const weighbridgeDetailSchema = z.object({
  category: weighbridgeCategorySchema,
  state: weighbridgeEntryStateSchema.exclude(["NotStarted"]),
  isDuplicateEntry: z.boolean(),
  singleWeightOnly: z.boolean(),
  entryLogId: guidSchema,
  serviceRecordId: guidSchema,
  weighbridgeCycleId: guidSchema.nullable(),
  warehouseStorageEntryId: guidSchema.nullable(),
  warehouseStorageId: guidSchema.nullable(),
  warehouseStorageNumber: z.string().nullable(),
  warehouseStorageStatus: z.enum(["Draft", "Confirmed", "Closed", "Cancelled"]).nullable(),
  exitId: guidSchema.nullable(),
  exitNumber: z.string().nullable(),
  vehicle: z.object({
    plate: z.string(), carrierCompanyName: z.string().nullable(),
    country: z.string().nullable(), vehicleType: z.string().nullable(),
  }),
  driver: z.object({ fullName: z.string(), idType: z.string(), idNumber: z.string() }).nullable(),
  entryReasonName: z.string().nullable(),
  dateTimeEntry: dateTimeSchema,
  stakeholderName: z.string().nullable(),
  documentTypeName: z.string().nullable(),
  documentNumber: z.string().nullable(),
  modalityName: z.string().nullable(),
  merchandise: z.array(merchandiseLineSchema),
  weights: z.object({
    indicator: datedWeight.nullable(),
    tare: datedWeight.extend({ isReal: z.boolean() }).nullable(),
    manifest: z.object({ weight: z.number(), documentLabel: z.string() }).nullable(),
    merchandise: datedWeight.extend({ source: z.enum(["Declared", "Reweigh", "Correction", "Calculated"]) }).nullable(),
    manifestExceedsDifference: z.boolean(),
  }),
  weighings: z.array(z.object({
    id: guidSchema, sequence: z.int().min(0), weightType: weightTypeSchema, weight: z.number(),
    capturedAt: dateTimeSchema, originalWeight: z.number().nullable(), modificationReason: z.string().nullable(),
  })),
  ticket: z.object({
    ticketNumber: z.string(), chargedAmount: z.number(), declaredWeight: z.number().nullable(), isZero: z.boolean(),
  }).nullable(),
  billing: z.object({
    invoiceNumber: z.string().nullable(), customerName: z.string().nullable(),
    totalCharged: z.number(), statusLabel: z.string(),
  }).nullable(),
  voided: z.object({ at: dateTimeSchema, byName: z.string(), reason: z.string() }).nullable(),
  ticketObservations: z.string().nullable(), // FE-2 (2026-11-24): la observación guardada (C-F03-36), D33
  actions: z.object({
    canEdit: z.boolean(), canEditWeights: z.boolean(), canReweigh: z.boolean(),
    canPrint: z.boolean(), canVoid: z.boolean(),
  }),
});
export type WeighbridgeDetail = z.infer<typeof weighbridgeDetailSchema>;
```

`Calculated` es el origen de la mercancía en salida y solo báscula (diferencia de pesajes).

**`F/features/weighbridge/contracts/ticket.ts`** — C-F03-35 y C-F03-36

```ts
import { z } from "zod";

export const ticketSectionSchema = z.enum(["Entry", "Tare", "Reweigh"]);
export const ticketPdfQuerySchema = z.object({
  sections: z.array(ticketSectionSchema).min(1), // separado por comas
  receipt: z.boolean().default(false),
});
export const ticketObservationsSchema = z.object({ observations: z.string().max(500).nullable() });
export type TicketSection = z.infer<typeof ticketSectionSchema>;
```

**`F/features/weighbridge/contracts/void.ts`** — C-F03-37 y C-F03-38

```ts
import { z } from "zod";
import { guidSchema, reasonBodySchema, reasonSchema } from "~/shared/contracts/api";

export const voidRequestSchema = reasonBodySchema;
export const serviceVoidRequestSchema = z.object({ entryLogId: guidSchema, reason: reasonSchema });
export const voidResultSchema = z.object({
  weighbridgeCycleId: guidSchema.nullable(),
  ticketNumber: z.string().nullable(),
  kind: z.string(),
  voidedEntries: z.array(z.object({ warehouseStorageNumber: z.string(), vehiclePlate: z.string().nullable() })),
  cancelledDeposits: z.array(z.string()),
  revertedOrders: z.array(z.string()),
  cancelledInvoices: z.array(z.object({ invoiceId: guidSchema, invoiceNumber: z.string().nullable() })),
  invoicesToReview: z.array(z.object({
    invoiceId: guidSchema, invoiceNumber: z.string().nullable(), status: z.string(), total: z.number(),
  })),
}).loose();
export type VoidResult = z.infer<typeof voidResultSchema>;
```

**`F/features/weighbridge/contracts/service-record.ts`** — C-F03-16

```ts
import { z } from "zod";
import { dateTimeSchema, guidSchema } from "~/shared/contracts/api";
import { weighbridgeRegistrationSchema } from "./registration";

export const serviceRecordUpdateSchema = z.object({
  entryLogId: guidSchema,
  licensePlate: z.string().trim().min(3).max(15).nullable().optional(),
  dateTimeEntry: dateTimeSchema.nullable().optional(),
  driverId: guidSchema.nullable().optional(),
  carrierCompanyId: guidSchema.nullable().optional(),
  stakeholderId: guidSchema.nullable().optional(),
  firstWeight: z.number().positive().nullable().optional(),
  secondWeight: z.number().positive().nullable().optional(),
  singleWeightOnly: z.boolean().nullable().optional(),
  reason: z.string().trim().min(10).max(500).nullable().optional(),
});
export const serviceRecordUpdateResultSchema = weighbridgeRegistrationSchema.extend({
  changes: z.array(z.object({ field: z.string(), previousValue: z.string().nullable(), newValue: z.string().nullable() })),
  notifiedForeignTrade: z.boolean(),
});
export type ServiceRecordUpdate = z.infer<typeof serviceRecordUpdateSchema>;
```

**`F/features/entries/contracts/entry-log-correction.ts`** — C-F03-17 (el de `P01/` §2.3 con `reason` opcional)

```ts
import { z } from "zod";
import { dateTimeSchema, guidSchema, reasonSchema } from "~/shared/contracts/api";

export const entryLogCorrectionSchema = z.object({
  licensePlate: z.string().trim().min(3).max(15).nullable().optional(),
  entryReasonId: guidSchema.nullable().optional(),
  dateTimeEntry: dateTimeSchema.nullable().optional(),
  reason: reasonSchema.nullable().optional(), // D3: obligatorio salvo Báscula sin ciclo completo
});
export const entryLogCorrectionResultSchema = z.object({
  entryLog: z.object({ id: guidSchema, licensePlate: z.string(), dateTimeEntry: dateTimeSchema }).loose(),
  changes: z.array(z.object({ field: z.string(), previousValue: z.string().nullable(), newValue: z.string().nullable() })),
  depositsNotUpdated: z.array(z.object({ warehouseStorageNumber: z.string(), entryDate: dateTimeSchema.nullable() })),
  deactivatedVehiclePlate: z.string().nullable(),
});
```

**`F/features/entries/contracts/entry-log.ts`** — C-F03-27, C-F03-48 a C-F03-51

```ts
import { z } from "zod";
import { dateOnlySchema, dateTimeSchema, guidSchema, listQueryBaseSchema } from "~/shared/contracts/api";

export const entryLogStatusSchema = z.enum(["Registered", "Completed"]);
export const entryLogListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["dateTimeEntry", "dateTimeDeparture", "licensePlate", "status"]).optional(),
  licensePlate: z.string().optional(),
  entryReasonId: guidSchema.optional(),
  status: z.array(entryLogStatusSchema).optional(), // separado por comas
  dateTimeEntryFrom: dateOnlySchema.optional(),
  dateTimeEntryTo: dateOnlySchema.optional(),
  dateTimeDepartureFrom: dateOnlySchema.optional(),
  dateTimeDepartureTo: dateOnlySchema.optional(),
  isCorrected: z.boolean().optional(),
});
export const entryLogSchema = z.object({
  id: guidSchema,
  serviceRecordId: guidSchema.nullable(),
  vehicleId: guidSchema,
  driverId: guidSchema.nullable(),
  entryReasonId: guidSchema.nullable(),
  dateTimeEntry: dateTimeSchema,
  status: entryLogStatusSchema,
  dateTimeDeparture: dateTimeSchema.nullable(),
  observations: z.string().nullable(),
  isCorrected: z.boolean(),
  lastCorrectedAt: dateTimeSchema.nullable(),
  lastCorrectedByName: z.string().nullable(),
  hasOperation: z.boolean(),
  hasDeposits: z.boolean(),
  vehicle: z.object({ id: guidSchema, licensePlate: z.string() }).loose().nullable(),
  driver: z.object({ id: guidSchema, firstName: z.string(), lastName: z.string(), idNumber: z.string() }).loose().nullable(),
  entryReason: z.object({ id: guidSchema, description: z.string() }).loose().nullable(),
  manifests: z.array(z.object({ id: guidSchema, manifestNumber: z.string(), manifestWeight: z.number().nullable() }).loose()).nullable(),
  departureAuthorizations: z.array(z.object({ id: guidSchema }).loose()).nullable(),
}).loose();
export const departureAuthorizationSchema = z.object({ observations: z.string().max(500).nullable() });
export const manifestCreateSchema = z.object({
  manifestNumber: z.string().trim().min(1).max(100), manifestWeight: z.number().positive().nullable(),
});
/** C-F03-51 (forma de hoy; lo usa `cycles/[id]`). */
export const depositEntryDateSchema = z.object({ entryDate: dateTimeSchema, reason: z.string().trim().min(10).max(500) });
export type EntryLog = z.infer<typeof entryLogSchema>;
```

### 2.4 Pantallas y sus endpoints

| Pantalla | Ruta | Endpoints |
| --- | --- | --- |
| P-BAS-01 Cola | `/operations/weighbridge` | C-F03-21 |
| P-BAS-02 Registro, ingreso (y panel de la cola) | `/operations/weighbridge/process/[entryLogId]` | C-F03-43, C-F03-17, C-F03-01, C-F03-13, C-F03-14, C-F03-12, C-F03-11, C-F03-44, C-F03-52, C-F03-21; C-F01-02, C-F01-15, C-F01-17, C-F01-18, C-F01-25, C-F01-26, C-F01-29, C-F01-69, C-F01-141 |
| P-BAS-03 Registro, salida | la misma | C-F03-43, C-F03-17, C-F03-03, C-F03-15, C-F03-16, C-F03-12, C-F03-11, C-F03-21; C-F01-02, C-F01-101, C-F01-15, C-F01-17, C-F01-18, C-F01-25, C-F01-141 |
| P-BAS-04 Registro, solo báscula | la misma | C-F03-43, C-F03-17, C-F03-04, C-F03-15, C-F03-16, C-F03-12, C-F03-11, C-F03-21; C-F01-02, C-F01-15, C-F01-17, C-F01-18, C-F01-25, C-F01-141 |
| P-BAS-05 Cobro | la misma (`?paso=cobro`) | C-F03-05 a C-F03-10, C-F03-13, C-F03-15; C-F01-25, C-F01-26, C-F01-141 |
| P-BAS-06 Tiquete | la misma (`?paso=tiquete`) | C-F03-15 (el ciclo) y C-F03-34 (resumen del pesaje por el ciclo: una entrada de ingreso completada sale de la cola y la página pierde su `warehouseStorageEntryId`; respuesta del usuario del 2026-11-24 en FE-2) |
| P-BAS-07 Repesaje | modal en la página, el historial y el detalle | C-F03-11 |
| P-BAS-08 Historial › Entradas | `/operations/weighbridge/history` | C-F03-22, C-F03-37 |
| P-BAS-09 Historial › Salidas | `/operations/weighbridge/history/exits` | C-F03-23, C-F03-38 |
| P-BAS-10 Historial › Solo báscula | `/operations/weighbridge/history/weighing-only` | C-F03-24, C-F03-38 |
| P-BAS-11 Detalle (drawer) | sobre P-BAS-08 a P-BAS-10, con `?id=` | C-F03-25, C-F03-26, C-F03-37, C-F03-38, C-F03-14 |
| P-BAS-12 Tiquete impreso | PDF | C-F03-35 |
| P-BAS-13 Modal de impresión | en P-BAS-06, P-BAS-08 a P-BAS-11 | C-F03-36, C-F03-35 |
| P-TR-12 Corregir salida o solo pesaje | modal en P-BAS-09, P-BAS-10 y P-BAS-11 | C-F03-15, C-F03-16; C-F01-15, C-F01-17, C-F01-25, C-F01-141 |
| Vigilancia › Historial | `/operations/entries/history` | C-F03-27, C-F03-48, C-F03-17, C-F03-49, C-F03-50; C-F01-02 |
| Detalle del ciclo a página completa (D7) | `/operations/weighbridge/cycles/[id]` | C-F03-34, C-F03-37, C-F03-38, C-F03-35, C-F03-36, C-F03-45, C-F03-46, C-F03-51 |

---

## 3. Archivos que se tocan

### 3.1 Pantallas y componentes

| Pantalla | Componentes compartidos | Componentes de Báscula (D39) |
| --- | --- | --- |
| P-BAS-01 | `AppDataTable` (modo `client`, `globalFilters`) | `WeighbridgeQueueTable` |
| P-BAS-02 a P-BAS-04 | `AppSearchSelect`, `AppCrudDialog` (altas) | `WeighbridgeProcessHeader`, `RegistrationVigilanceSection`, `RegistrationTruckSection`, `RegistrationEntrySection`, `RegistrationGoodsLines`, `RegistrationExitSection`, `RegistrationWeighingOnlySection`, `RegistrationWeights`, `WeighbridgeQueuePanel`; `StakeholderQuickDialog`, `DriverQuickDialog` |
| P-BAS-05 | `AppChargeForm` | `WeighbridgeChargeStep` |
| P-BAS-06 | — | `WeighbridgeTicketStep` |
| P-BAS-07 | `AppCrudDialog` | `ReweighDialog` |
| P-BAS-08 a P-BAS-10 | `AppDataTable` (modo `server`), `ReasonDialog`, `CorrectionResultDialog` | `WeighbridgeHistoryActions` |
| P-BAS-11 | `AppDetailDrawer`, `AppDetailSection` | `WeighbridgeEntryDetail` |
| P-BAS-13 | `AppCrudDialog` | `TicketPrintDialog` |
| P-TR-12 | `AppCrudDialog` (dos columnas), `AppSearchSelect` | `ServiceCorrectionDialog` |
| Vigilancia › Historial | `AppDataTable`, `AppDetailDrawer`, `AppDetailSection`, `AppCrudDialog` | — (en `F/features/entries/components/`: `EntryLogDetail`, `EntryLogCorrectionDialog`) |
| `cycles/[id]` | — | `WeighbridgeEntryDetail`; conserva `ModifyWeighingDialog` y el de la fecha de ingreso (D32) |

### 3.2 Backend

| Archivo (base `019fa81`) | Qué cambia | Fase |
| --- | --- | --- |
| `B/Wms.Domain/Entities/Logistics/ServiceRecordEntryLog.cs:13-28`; `B/Wms.Infrastructure/Persistence/Configurations/Logistics/EntryLogConfiguration.cs:75-91` | Primer peso, su fecha y usuario, modo de un solo pesaje (D2) | 1 |
| `B/Wms.Application/Weighbridge/Commands/Storage/Initiate/` (`InitiateStorageWeighingCommand.cs:14-80`, handler `:453`), `Storage/Register/`, `Output/Initiate/` (handler `:153`), `WeighingOnly/Initiate/` (handler `:24`, `:105-140`) | Primer peso, modo en el vínculo, `driverId`, `state` y `charge` (C-F03-01 a C-F03-04) | 1 |
| `B/Wms.Application/Weighbridge/Commands/*/ProcessPayment/`, `*/StartPendingBilling/` | El ciclo nace con el primer peso (C-F03-05 a C-F03-10) | 1 |
| `B/Wms.Application/Weighbridge/Commands/Common/RecordWeighing/RecordWeighingHandler.cs:74-82`, `:132-136`, `:217-221` | Repesaje del ciclo de un solo pesaje cerrado; modo desde el vínculo (C-F03-11) | 1 |
| `B/Wms.Domain/Entities/Weighbridge/WeighbridgeCycle.cs:81-129` | Reabrir un ciclo completo para su único repesaje | 1 |
| `B/Wms.Application/Weighbridge/Common/Services/WeighbridgeEntryStateResolver.cs` (nuevo) | Regla de D9 | 1 |
| `B/Wms.Application/Weighbridge/Common/Services/EntryLogInfoUpdater.cs:11-20`, `:77-87` | `DriverId` (D13) | 1 |
| `B/Wms.Application/Weighbridge/Common/Services/EntryCorrectionService.cs`; `Queries/GetEntryForEdit/` | Primer peso sin ciclo y modo (C-F03-13, C-F03-14) | 1 |
| `B/Wms.Application/Weighbridge/Queries/GetWeighbridgeRegistration/` | C-F03-15 | 1 |
| `B/Wms.Application/Logistics/EntryLogs/Commands/CorrectEntryLog/` (`CorrectEntryLogCommandValidator.cs:12`) | Motivo según D3 (C-F03-17) | 1 |
| `B/Wms.Application/Weighbridge/Common/Services/StorageDocumentLookup.cs:22-36` | `partial` (C-F03-52) | 1 |
| `B/Wms.Api/Controllers/v1/WeighbridgeController.cs:980-1002`; `WeighbridgeSharedController.cs:107-116` | Se borran las altas rápidas (C-F03-19, C-F03-20) | 1 |
| `B/Wms.Application/Weighbridge/Queries/GetWeighbridgeQueue/` (`GetWeighbridgeQueueHandler.cs:32-112`, `:161-168`); `Common/Dtos/WeighbridgeQueueItemDto.cs` | Cola por entrada (C-F03-21) | 2 |
| `B/Wms.Application/Weighbridge/Queries/GetWeighbridgeHistory*` (se borran); `Queries/GetHistoryEntries/`, `GetHistoryExits/`, `GetHistoryWeighingOnly/`, `GetWeighbridgeDetail/` (nuevos) | C-F03-22 a C-F03-26, C-F03-34 | 2 |
| `B/Wms.Application/Weighbridge/Queries/GetPendingEntryLogs/`, `GetPendingSecondWeight/`, `GetOpenCycles/`, `GetOpenCycleByPlate/` | Se borran (C-F03-30 a C-F03-33) | 2 |
| `B/Wms.Application/Logistics/EntryLogs/Queries/GetAllEntryLogs/` | Orden y filtros (C-F03-27) | 2 |
| `B/Wms.Application/Weighbridge/Common/Services/WeighbridgeTicketPdfService.cs:28`, `:42-107`, `:108` (se borra), `:275`, `:511-517` | Secciones, recibo, alto y líneas (C-F03-35) | 3 |
| `B/Wms.Application/Weighbridge/Commands/VoidWeighing/` (`VoidWeighingCommandHandler.cs:40-114`, `:170-313`); `Commands/VoidEntry/`, `Commands/VoidServiceRecord/` (nuevos); `Commands/DiscardIncompleteOperation/` y `Queries/GetRecoverableOperations/` (se borran) | C-F03-37 a C-F03-40 | 3 |
| `B/Wms.Application/Weighbridge/Commands/UpdateServiceRecord/` (nuevo) | C-F03-16 | 3 |
| `B/Wms.Application/Weighbridge/Commands/ModifyFirstWeight/ModifyFirstWeightHandler.cs`, `ModifySecondWeight/ModifySecondWeightHandler.cs` | D32 | 3 |
| `B/Wms.Api/Controllers/v1/WeighbridgeController.cs`, `WeighbridgeCycleReadController.cs`, `WeighbridgeVoidController.cs`, `EntryCorrectionController.cs`, `EntryLogController.cs` | Rutas de §2.1 | 1 a 3 |

`B/Wms.Domain/Security/WmsPolicyRoles.cs` no cambia (§2.0). Pruebas: §5.

### 3.3 Frontend

**Se crean** (maquetación): las páginas `F/pages/operations/weighbridge/process/[entryLogId].vue`, `history/exits.vue` y `history/weighing-only.vue`; los contratos de §2.3; las fuentes de D40 (`*.source.ts`) con sus simulados (`mocks/<recurso>.mock.ts`, `mocks/data/<recurso>.ts`); los componentes de D39; las utilidades `F/features/weighbridge/utils/registration-weights.ts` y `process-keys.ts`.
**Se reescriben en su ruta** (M11): `F/pages/operations/weighbridge/index.vue` (la cola), `history.vue` → `history/index.vue` (D6), `cycles/[id].vue` (D7) y `F/pages/operations/entries/history.vue` (D37).
**Cambian en I-03:** `F/components/layout/menu-model.ts:45-55` (D43), `F/composables/useGlobalShortcuts.ts:23` y `F/pages/operations/weighbridge/dashboard.vue:21`, `:28`, `:43`, `:100`, `:108`, `:116` (D7), `F/features/entries/components/VehicleForm.vue:274` (D1), `FT/unit/guards/list-pattern-routes.ts:32-34` y `:69-72`, `FT/unit/guards/mock-sources.spec.ts:16` y `:22-39`.
**Se borran en I-03** (después del grep de quién los importa; §13.3): lo que sale de la lista de §13.3.

### 3.4 Docs

`D/qa/casos-qa2-f03-bascula-AAAA-MM-DD.md` (I-03), el estado de este plan, `D/planes/README.md`, la matriz y `D/contexto/estado.md` (I-03).

---

## 4. Esquema y migraciones

Una migración, en la fase 1 del backend: **`WeighingAtRegistration`**. La genera y aplica el agente con `dotnet ef` en local (M6).

| Tabla | Cambio | Detalle |
| --- | --- | --- |
| `service_record_entry_logs` | Columnas nuevas | `first_weight` `numeric(18,2)` nula; `first_weight_captured_at` `timestamptz` nula; `first_weight_captured_by_id` `uuid` nula, con clave foránea a `users` (`ON DELETE RESTRICT`, como los demás «por»); `single_weight_only` `boolean` no nula, por defecto `false` |

- La columna `service_records.single_weight_only` se queda (la usan las semillas y lo importado), pero ya no decide: el ciclo lee el modo del vínculo de su entrada (D2). Quitarla no es de F03.
- Sin datos que convertir: las bases locales se recrean (`DEC-006`) y el importador del legacy no crea vínculos de báscula con peso (`PM/` §7.1).
- `dotnet ef migrations has-pending-model-changes` limpio al cerrar las tres fases.

---

## 5. Pruebas

| Proyecto | Prueba (nueva o ajustada) | Escenario |
| --- | --- | --- |
| `Wms.Tests` | `WeighbridgeEntryStateResolverTests` (nueva) | Los seis estados de D9 y sus transiciones de `A/` §2.1 c |
| `Wms.Tests` | `EntryLogInfoUpdaterTests` (nueva) | `DriverId` gana al documento; documento repetido sin `DriverId` (regla de hoy) |
| `Wms.Tests` | `ReweighRulesTests` (nueva) | Repesaje del ciclo de un solo pesaje cerrado: uno sí, el segundo no |
| `Wms.Tests` | `TicketSectionsTests` (nueva) | Secciones válidas según los pesajes del ciclo |
| `Wms.IntegrationTests` | `WeighingAtRegistrationTests` (nueva) | C-F03-01 a C-F03-10: registro con y sin peso, cobro que crea el ciclo con su pesaje, duplicada en $0 |
| `Wms.IntegrationTests` | `CycleSecondWeighingTests` (nueva) | C-F03-11 y C-F03-12 |
| `Wms.IntegrationTests` | `EntryCorrectionTests` (ajustada) | C-F03-13, C-F03-14, C-F03-17 (motivo según el rol y el ciclo) |
| `Wms.IntegrationTests` | `QuickCreateRetiredTests` (nueva) | C-F03-19 y C-F03-20 en 404; C-F01-141 con Vigilancia y Bodega en 201 |
| `Wms.IntegrationTests` | `WeighbridgeQueueTests` (nueva) y `QueueAfterEntryCorrectionTests` (ajustada); `Wms.Tests`: `WeighbridgeQueueFiltersTests` y `WeighbridgeQueueOpenEntryTests` (ajustadas) | C-F03-21: una fila por entrada, estados, pesos, mercancía |
| `Wms.IntegrationTests` | `WeighbridgeHistoryTests` (nueva; reemplaza las del historial de hoy, como `HistoryTicketFilterTests`) | C-F03-22 a C-F03-24: filtros, orden, filas sin ciclo, anuladas; C-F03-28 a C-F03-33 en 404 |
| `Wms.IntegrationTests` | `WeighbridgeDetailTests` (nueva) | C-F03-25, C-F03-26 y C-F03-34 con la misma forma |
| `Wms.IntegrationTests` | `EntryLogListTests` (nueva) | C-F03-27 |
| `Wms.IntegrationTests` | `TicketPdfTests` (nueva) | C-F03-35: secciones, errores, alto de la página según el contenido |
| `Wms.IntegrationTests` | `VoidByEntryTests` (nueva) | C-F03-37 y C-F03-38, con y sin ciclo; C-F03-39 a C-F03-41 en 404 |
| `Wms.IntegrationTests` | `ServiceRecordCorrectionTests` (nueva) | C-F03-16 antes del cobro y con el ciclo cerrado; avisos |
| `Wms.IntegrationTests` | `ModifyWeightMerchandiseTests` (nueva) | C-F03-45 y C-F03-46 recalculan la mercancía y la factura (D32) |
| Vitest | `FT/unit/weighbridge/registration-weights.spec.ts`, `process-keys.spec.ts` (nuevas) | D16 y D23 |
| Vitest | `FT/unit/weighbridge/mocks.spec.ts` (nueva) | Cada dato simulado de F03 pasa su esquema Zod (`P02/` D16) |
| Vitest | `FT/components/weighbridge/*.spec.ts` (nuevas, una por componente de D39) | Lo que pide cada wireframe: campos, botones y su habilitación |
| Vitest | `FT/unit/entries/mocks.spec.ts` (nueva) | Datos simulados de `entry-log` |
| Vitest | `FT/unit/guards/*` | Sin cambios de regla; I-03 actualiza sus listas (§13) |

Las pruebas de integración que hoy usan el historial, las altas rápidas de Báscula, `recoverable`, `incomplete` o `entries/{id}/ticket/pdf` se ajustan en la fase que retira el endpoint, en sus *helpers* (`WeighbridgeScenario`, `OperationalData`), salvo las que prueban justo esa regla.

---

## 6. Casos QA

Verificación: por API en la parte 1 (pruebas de integración HTTP contra Postgres), en el navegador en I-03. Al cerrar I-03 se copian a `D/qa/` con su ID.

### 6.1 Parte 1 (API)

| ID | Regla de origen | Precondición | Pasos | Resultado esperado | Verificación |
| --- | --- | --- | --- | --- | --- |
| QA2-F03-001 | `A/` §2.1 f; AF-07; D2 | Camión con motivo `Entry` | C-F03-01 con `firstWeight: 30000` | 201, `state: PendingPayment`, `firstWeight: 30000`; el vínculo guarda el peso | API |
| QA2-F03-002 | AF-07; D9 | Camión con motivo `Entry` | C-F03-01 sin `firstWeight` | 201, `state: PendingWeighing` | API |
| QA2-F03-003 | AF-06, AF-11; D2 | Entrada de QA2-F03-001 con «Req. 2.º pesaje» | C-F03-05 | El ciclo nace con un pesaje bruto de 30000; `state: PendingReweigh` | API |
| QA2-F03-004 | AF-11; D2 | Igual, de un solo pesaje | C-F03-05 | `state: Completed` | API |
| QA2-F03-005 | `A/` §2.1 c; D9 | Entrada de QA2-F03-002 | C-F03-06; luego C-F01-80 con el bruto | Primero `PendingWeighing`; después `PendingReweigh` | API |
| QA2-F03-006 | AF-44, AF-47; `P01/` D20 | Camión con una entrada guardada | C-F03-01 con otro documento y el mismo `entryLogId`; C-F03-05 con valor > 0 | `isDuplicateEntry: true`, `charge.isZeroCharge: true`; el cobro sale en $0 | API |
| QA2-F03-007 | AF-18; D13 | Dos conductores con CC 1000001 | C-F03-01 con `driverId` del segundo | El camión queda con el segundo conductor | API |
| QA2-F03-008 | AF-11; D18 | Ciclo con el primer pesaje, abierto | C-F03-12 `required: false`; luego otra vez sobre el ciclo cerrado | Primero `Completed`; después 409 «El ciclo ya está cerrado: para agregar el repesaje use «Repesar».» | API |
| QA2-F03-009 | AF-13, AF-40; D19 | Ciclo de un solo pesaje completo, camión ya salido | C-F03-11 con la tara; otra vez | Primero 200 y la mercancía = indicador − tara; después 409 «El ciclo ya tiene su repesaje…» | API |
| QA2-F03-010 | AF-08; D3 | Usuario Báscula; camión sin ciclo completo | C-F03-17 corrige la placa sin `reason`; con un ciclo completo, otra vez sin `reason` | Primero 200 (auditoría «Corrección en el registro de báscula»); después 400 «Indique el motivo…» | API |
| QA2-F03-011 | D3 | Usuario Vigilancia | C-F03-17 sin `reason` | 400 | API |
| QA2-F03-012 | AF-26; D2 | Entrada «Por cobrar» | C-F03-14 con otro `indicatorWeight`, sin motivo | 200; C-F03-13 devuelve el peso nuevo | API |
| QA2-F03-013 | AF-54; D1 | Usuarios Vigilancia y Bodega | C-F03-19 y C-F03-20; C-F01-141 con `TRANSPORT_COMPANY` | Los dos viejos en 404; C-F01-141 en 201 con los dos usuarios | API |
| QA2-F03-014 | AF-16; D14 | Tercero sin rol Cliente | C-F03-04 con ese `customerId` y `firstWeight` | 201, `state: PendingPayment` | API |
| QA2-F03-015 | AF-37; `P01/` D37 | Placa sin salida | C-F03-03 sin `exitId` y con `firstWeight` | 201, `exitCreated: true`, `state: PendingPayment` | API |
| QA2-F03-016 | AF-24; D44 | Depósito abierto con documento «CP-1234» | C-F03-52 `number=1234&partial=true`; `number=12&partial=true` | Primero el candidato con `documentNumber`; después 400 «Escriba al menos 3 caracteres…» | API |
| QA2-F03-017 | AF-15, AF-44; D24 | Un camión con dos entradas (una «Por cobrar» con pesos, otra «Por pesar») y otro «Sin iniciar» | C-F03-21 | Tres filas; la primera con P. bruto, P. mercancía, tara y mercancía; la segunda con pesos nulos | API |
| QA2-F03-018 | AF-15, AF-50, H-007; D26 | Entradas de varios días, una duplicada | C-F03-22 sin orden; con `vehiclePlate=abc` y `state=Completed` | Más reciente primero; la duplicada como fila propia; los filtros aplican | API |
| QA2-F03-019 | AF-23, AF-48; D29 | Una entrada guardada sin cobrar y una anulada | C-F03-22 | La primera sin tiquete ni valor; la anulada con `state: Voided` y su motivo | API |
| QA2-F03-020 | P-BAS-09, P-BAS-10; D27, D28 | Salida y solo pesaje con repesaje | C-F03-23 y C-F03-24 | Columnas del legacy; en solo báscula, `differenceWeight` = pesaje − repesaje | API |
| QA2-F03-021 | P-BAS-11; D30 | Una entrada de ingreso con ciclo | C-F03-25, C-F03-26 (de una salida) y C-F03-34 (del ciclo de la entrada) | C-F03-25 y C-F03-34 devuelven lo mismo; las marcas `actions` según el estado | API |
| QA2-F03-022 | AF-129; D37 | Ingresos de Vigilancia | C-F03-27 con `licensePlate=abc&sortField=dateTimeDeparture&sortOrder=desc`; con `sortField=observations` | Primero la lista filtrada y ordenada; después 400 «No se puede ordenar por «observations».» | API |
| QA2-F03-023 | D4 | — | C-F03-28 a C-F03-33 | 404 | API |
| QA2-F03-024 | AF-52, AF-24; D33 | Ciclo con el primer pesaje, sin repesaje | C-F03-35 `sections=Entry,Tare&receipt=true`; `sections=Reweigh`; `sections=` | 200 PDF; 409 «El repesaje aún no existe…»; 400 «Elija al menos una sección…» | API |
| QA2-F03-025 | PR-32, H-006; D33 | Ciclo con una mercancía y otro con cuatro | C-F03-35 de cada uno | Una página; el alto del primero es menor que el del segundo y menor que 200 mm; una línea por mercancía | API |
| QA2-F03-026 | AF-48; D34 | Entrada «Por pesar» sin ciclo | C-F03-37 con motivo | 200; la entrada anulada con su motivo; C-F03-21 muestra el camión «Sin iniciar» | API |
| QA2-F03-027 | AF-23; D34 | Solo pesaje con ciclo | C-F03-38 con motivo; otra vez | Primero 200 con el resultado de hoy; después 409 «La operación ya está anulada.» | API |
| QA2-F03-028 | AF-135; D35 | Salida completa con guía | C-F03-16 con otro conductor y sin `reason`; con `reason` | Primero 400 «Indique el motivo…»; después 200, `notifiedForeignTrade: true` y el aviso «Modificación de Peso en Báscula» a Admin | API |
| QA2-F03-029 | D32 | Ciclo de almacenamiento con repesaje | C-F03-46 con otra tara | La mercancía de la entrada = indicador − tara nueva, origen `Correction`; la factura en Borrador se recalcula | API |
| QA2-F03-030 | AF-51; D4 | — | C-F03-39 a C-F03-41 | 404 | API |

### 6.2 Integración I-03 (navegador)

| ID | Regla de origen | Precondición | Pasos | Resultado esperado | Verificación |
| --- | --- | --- | --- | --- | --- |
| QA2-F03-031 | P-BAS-01; AF-15, AF-44, AF-51, H-004 | Camiones en varios estados, uno con dos entradas | Abrir Báscula › Proceso de pesaje; filtrar «Por cobrar»; clic en una fila | Una fila por entrada con mercancía y pesos; el contador por estado; la fila no abre nada; sin «Recuperar operaciones» | Pantalla |
| QA2-F03-032 | P-BAS-02; AF-08, AF-12, AF-17, AF-24, AF-25 | Camión «Sin iniciar» con motivo de Ingreso | «Atender»; revisar las secciones; elegir inspección; volver a importación con «Factura comercial» | «Carta porte» por defecto; manifiesto solo con carta porte; en inspección, documento y producto opcionales y descripción obligatoria; sin tipo de vehículo ni unidades de carga | Pantalla |
| QA2-F03-033 | AF-09, AF-41; D16 | El camión anterior | Digitar indicador 30 000 y manifiesto 18 000; cambiar la mercancía a 17 500 | La mercancía se precarga en 18 000; la tara pasa de 12 000 a 12 500 y no se puede digitar | Pantalla |
| QA2-F03-034 | AF-24; D44 | Depósito abierto con «CP-1234» | Digitar «123» en el número | Sugiere CP-1234; al elegirlo aparece el depósito con «Es otro documento» | Pantalla |
| QA2-F03-035 | AF-07; D10 | Registro sin pesos | «Guardar» | La advertencia del wireframe; «Guardar sin pesaje» lleva al Cobro; en la cola, «Por pesar» | Pantalla |
| QA2-F03-036 | AF-08; D11 | Camión con motivo de Ingreso, sin guardar | Cambiar el motivo a uno de Salida en la sección 1 | El formulario pasa a P-BAS-03 al instante | Pantalla |
| QA2-F03-037 | AF-44, AF-48, AF-49; D20 | Registro con las secciones 1 y 2 completas | «Duplicar entrada»; llenar otro documento; guardar; duplicar otra vez y salir sin guardar | El botón se habilita con 1 y 2 completas; la cola muestra dos filas con su mercancía; la tercera no deja rastro | Pantalla |
| QA2-F03-038 | P-BAS-03; AF-30, AF-34, AF-37 | Una placa con salida confirmada y otra sin salida | «Atender» cada una | Caso A: la salida de solo lectura; caso B: el aviso de la salida en Borrador | Pantalla |
| QA2-F03-039 | P-BAS-04; AF-16, AF-54 | Camión de solo báscula | Buscar un tercero; «+» crea uno nuevo | Sin «Peso esperado»; el tercero nuevo queda elegido | Pantalla |
| QA2-F03-040 | P-BAS-05; AF-25, AF-47, AF-54, AF-132 | Entrada «Por cobrar» y su duplicada | Cobrar la primera con Transferencia; cobrar la duplicada | Destinatarios de hoy; tercero precargado; «Referencia» solo con otro método; la duplicada en $0, solo con el destinatario; «Editar registro» vuelve al paso 1 | Pantalla |
| QA2-F03-041 | P-BAS-06, P-BAS-13; AF-24, AF-50, AF-52, AF-53 | Ciclo con el primer pesaje y repesaje pendiente | «Imprimir»; marcar Entrada y Tara, «Incluir recibo» y una observación; imprimir; volver a abrir | Repesaje deshabilitado; el PDF con esas secciones; la observación queda guardada | Pantalla |
| QA2-F03-042 | P-BAS-07; AF-13, AF-40 | Un camión «Por repesar» y un ciclo único cerrado | Repesar desde la cola; «Repesar» desde el historial del otro | El modal con la diferencia con el manifiesto; los dos quedan «Completado» con repesaje | Pantalla |
| QA2-F03-043 | P-BAS-08; AF-15, AF-23, AF-26, AF-50, AF-99 | Historial con entradas de las tres modalidades, una anulada y una duplicada | Cambiar de pestaña; filtrar por placa y estado; ordenar por tiquete; «Exportar» | Columnas del legacy; acciones según el estado; anulada en rojo con su motivo; la duplicada con su tiquete en $0; el Excel con el filtro | Pantalla y red |
| QA2-F03-044 | P-BAS-09, P-BAS-10, P-TR-12; AF-135 | Una salida y un solo pesaje completos | «Editar» en cada uno; cambiar el peso sin motivo; con motivo | Sin motivo, el aviso del backend en el campo; con motivo, se guarda y aparece en el historial | Pantalla |
| QA2-F03-045 | P-BAS-11; AF-15, AF-45, AF-50, AF-53; `PAJ/` D3, D5 | Una entrada completa de un solo pesaje y otra por repesar | «Ver» en cada una | Encabezado, secciones y «Editar pesajes» en la sección 2; con tres acciones, el menú ⋮; con dos, el pie | Pantalla |
| QA2-F03-046 | D7, D32; `DEC-005` | Usuarios CE y Facturación | Abrir el detalle del depósito y su enlace al ciclo; Facturación usa «Modificar pesaje» | Los dos ven el detalle nuevo a página completa; Facturación corrige el peso con motivo | Pantalla |
| QA2-F03-047 | R6; D23 | Camión «Sin iniciar» | Llenar con el teclado; Enter; Enter en el Cobro; F2 en un camión «Por repesar»; Escape | Enter guarda y cobra; F2 abre el repesaje; Escape no cierra la página | Pantalla |
| QA2-F03-048 | D37; AF-129 | Ingresos de Vigilancia | Vigilancia › Historial: filtrar, ordenar por salida, «Ver», «Corregir» sin motivo | La red muestra `sortField` y los filtros; el drawer; la corrección pide motivo | Pantalla y red |
| QA2-F03-049 | D1, D6, D7, D43; `DEC-005` | Usuarios Báscula, Vigilancia y Bodega | Ver el menú de Báscula; abrir `/operations/weighbridge/recover`; Alt+K; «+» de transportadora en Vigilancia y en Bodega | Cinco ítems en Báscula; `recover` da 404; Alt+K abre la cola en «Por repesar»; Vigilancia y Bodega crean la transportadora | Pantalla |
| QA2-F03-050 | `PM/` §6.3 | I-03 cerrada | `grep` de imports de `mocks/` fuera de `F/shared/mocks/` y de las pruebas; `yarn test` de las guardias | Sin resultados; las rutas de F03 en `PATTERN` y `MAQUETACION_PAGES` vacía | Código |

---

## 7. Transición de datos

No aplica: `PM/` §7.2 no le asigna datos a F03. Las columnas nuevas son nulas o con valor por defecto, las bases locales se recrean (`DEC-006`) y el despliegue final recrea staging (M17, M25), así que no hay ciclos abiertos que convertir.

---

## 8. Fases por parte

Cada fase cierra con las compuertas de `PM/` §6 (§6.1 en el backend, §6.2 en la maquetación) con las cifras antes y después, sus casos QA en PASA (por API en la parte 1), commit con el mensaje de §12 y push de `f2/f03-bascula`. Una fase por turno.

| Fase | Parte | Contenido | Criterio de salida | Estado |
| --- | --- | --- | --- | --- |
| BE-1 | 1 | Registro y ciclo | QA2-F03-001 a 016 en PASA; migración `WeighingAtRegistration` aplicada | Hecha el 2026-11-24 (BE `ccfa53d`) |
| BE-2 | 1 | Cola, historial y detalle | QA2-F03-017 a 023 en PASA | Hecha el 2026-11-24 (BE `56d52f8`) |
| BE-3 | 1 | Tiquete, anulación y correcciones | QA2-F03-024 a 030 en PASA | Pendiente |
| FE-1 | 2 | Contratos, fuentes simuladas, cola y registro | P-BAS-01 a P-BAS-04 con su lista del wireframe y captura | Hecha el 2026-11-24 (FE `d49a691`) |
| FE-2 | 2 | Cobro, tiquete, repesaje e impresión | P-BAS-05 a P-BAS-07 y P-BAS-13 con su lista y captura | Hecha el 2026-11-24 (FE `cd58697`) |
| FE-3 | 2 | Historial, detalle, corrección, Vigilancia › Historial y `cycles/[id]` | P-BAS-08 a P-BAS-11, P-TR-12, Vigilancia › Historial y `cycles/[id]` con su lista y captura | Hecha el 2026-11-24 (FE `ae34783`) |
| I-03 | 3 | Integración (§13) | §13.5 | Pendiente |

### 8.1 Backend, fase 1 — Registro y ciclo

- **Decisiones:** D1, D2, D3, D9, D13, D15, D18, D19, D44.
- **Endpoints:** C-F03-01 a C-F03-15, C-F03-17 a C-F03-20, C-F03-43, C-F03-44 y C-F03-52 (fichas de §2.2, grupo A; esquemas de `registration.ts`, `payment.ts`, `weighing.ts`, `entry-edit.ts` y `entry-log-correction.ts` en §2.3).
- **Archivos:** §3.2, filas de la fase 1. Migración `WeighingAtRegistration` (§4).
- **Pruebas:** `WeighbridgeEntryStateResolverTests`, `EntryLogInfoUpdaterTests`, `ReweighRulesTests`, `WeighingAtRegistrationTests`, `CycleSecondWeighingTests`, `EntryCorrectionTests`, `QuickCreateRetiredTests` (§5).
- **Casos QA:** QA2-F03-001 a QA2-F03-016.
- **Cuidado:** el ciclo sigue naciendo en el cobro; la duplicada en $0 no cambia (`P01/` D20); `RecordWeighingHandler` lee el modo del vínculo de la entrada del ciclo, no del servicio.
- **Estado:** hecha el 2026-11-24 (BE `ccfa53d`, rama `f2/f03-bascula`). QA2-F03-001 a 016 en PASA por API. `Wms.Tests` 2037 → 2072; `Wms.IntegrationTests` 678 → 709 (los 2 fallos heredados de la base, `InitiateCustomerIdTests.Queue_PendingService_ReturnsCustomerId` y `DiscardOperationTests.Discard_ReleasesTruckToNotStarted`, que pasan solas y fallan por el orden de la suite); migración `WeighingAtRegistration` aplicada en local y `has-pending-model-changes` limpio. Cada endpoint de la fase tiene su prueba de integración (C-F03-43 y C-F03-44, sin cambios, en `WeighingAtRegistrationTests`; C-F03-52 en `DocumentCandidatesTests`; C-F03-15 en `WeighbridgeRegistrationTests`).
- **Notas para I-03 (aplicadas por `DEC-002`):**
  - D15: el tipo del primer pesaje ya no se exige en ingreso ni en solo báscula; por defecto es bruto, así que `configuredFirstWeightType` de solo báscula sale `Gross` (antes nulo).
  - C-F03-11: el repesaje de un ciclo cerrado no se limita por la salida del camión (D19, «aunque el camión haya salido»); debe ser el opuesto al primer pesaje (400 «El repesaje debe ser Tara (opuesto al primer pesaje).» o «Bruto»).
  - C-F03-07: una salida de un solo pesaje se cierra en el cobro, así que el cobro responde el error de la guía de importación de hoy (CHG-33) si la salida no la tiene.
  - C-F03-17: sin motivo, Vigilancia y Admin reciben el 400 del validador, con el mensaje en `errors[]`; Báscula con un ciclo completo lo recibe en `description`.
  - C-F03-14: la respuesta (`depositEntrySchema`) trae en `indicatorWeight` el primer peso del vínculo cuando no hay ciclo; `packagingTypeId` se suma a cada producto de `depositEntrySchema` en todas sus lecturas (aditivo).
  - C-F03-12: con el ciclo anulado responde 409 «El pesaje está anulado.» aunque la anulación haya retirado el vínculo.
  - D1: se retiraron las dos rutas; los comandos `QuickCreateStakeholderCommand` y `QuickCreateTransportCompanyCommand` quedan sin ruta (los usan pruebas de validación).

### 8.2 Backend, fase 2 — Cola, historial y detalle

- **Decisiones:** D9, D24, D26 a D30, D37.
- **Endpoints:** C-F03-21 a C-F03-34 y C-F03-48 (grupo B; esquemas de `queue.ts`, `history.ts`, `detail.ts` y `entry-log.ts`).
- **Archivos:** §3.2, filas de la fase 2. Sin migración.
- **Pruebas:** `WeighbridgeQueueTests`, `WeighbridgeHistoryTests`, `WeighbridgeDetailTests`, `EntryLogListTests` (§5).
- **Casos QA:** QA2-F03-017 a QA2-F03-023.
- **Cuidado:** los listados usan `ListSorting` de C-F01-00 (`B/Wms.Common/Wrappers/ListSorting.cs`); el estado de cada fila sale de `WeighbridgeEntryStateResolver`; la cola conserva su tope (trampa 12).
- **Cambio de contrato de FE-2 (2026-11-24, respuesta del usuario «Sumar al detalle»):** el detalle (C-F03-25, C-F03-26 y C-F03-34) devuelve también `ticketObservations` (texto \| null), la observación del tiquete que guarda C-F03-36 (la misma que imprime `WeighbridgeTicketPdfService.cs:511-517`). Aditivo; ficha en §2.2 y esquema en §2.3.
- **Estado:** hecha el 2026-11-24 (BE `56d52f8`, rama `f2/f03-bascula`). QA2-F03-017 a 023 en PASA por API. `Wms.Tests` 2072 → 2141; `Wms.IntegrationTests` 709 → 747, todas en verde: los 2 fallos heredados de BE-1 (`InitiateCustomerIdTests.Queue_PendingService_ReturnsCustomerId` y `DiscardOperationTests.Discard_ReleasesTruckToNotStarted`) ya no dependen del orden de la suite, porque buscan su camión en la cola por placa (`F03Scenario.QueueRowAsync`); sin migración y `has-pending-model-changes` limpio. Pruebas de integración por endpoint: C-F03-21 en `WeighbridgeQueueTests`; C-F03-22 a C-F03-24 y C-F03-28 a C-F03-33 en `WeighbridgeHistoryTests` (y `HistoryTicketFilterTests`, pasada a los tres listados); C-F03-25, C-F03-26 y C-F03-34 en `WeighbridgeDetailTests`; C-F03-27 y C-F03-48 en `EntryLogListTests`. `ticketObservations` (nota de FE-2) ya va en el detalle.
- **Cómo quedó:** `WeighbridgeEntryReader` lee las entradas de un grupo de camiones (vínculo, ciclo, entrada del depósito, líneas) y es la única lectura de la cola, la página del historial y el detalle; `WeighbridgeEntryView` (pura, `WeighbridgeEntryViewTests`) da los pesos por categoría y las marcas de las acciones; la regla de D9 pasó a una expresión (`WeighbridgeEntryStateResolver.Rule`) que `Resolve` compila y el historial lleva a SQL para filtrar y ordenar por `state`. Se borraron las consultas retiradas (`GetPendingEntryLogs`, `GetPendingSecondWeight`, `GetOpenCycles`, `GetOpenCycleByPlate`, `GetWeighbridgeHistory`, `GetWeighbridgeHistoryTotals`). `OpenCycleDto` queda para BE-3, que retira `recoverable`.
- **Notas para I-03 (aplicadas por `DEC-002`):**
  - C-F03-28 a C-F03-33: para que `pending`, `history` y `cycles/open` respondan 404 y no caigan en `GET weighbridge/{id}`, ese endpoint y `cycles/{id}` (detalle de hoy, `ActiveUser`) aceptan solo Guid: un Id que no es Guid responde 404 en lugar de 400.
  - Tablero (`GET weighbridge/dashboard`): cuenta con los estados nuevos de la cola; «En proceso» = «Por pesar» + «Por repesar» y «Pendientes repesaje» = «Por repesar», ahora por entrada.
  - C-F03-21: un camión cuyas entradas están todas anuladas (o sin vínculo) es una fila «Sin iniciar» con la categoría de su motivo; uno con todas completas sale de la cola. `documentNumber` es el documento del servicio y, en una salida, el número de la salida. `merchandise.weight` es el peso de la línea o, si es la única, el de la mercancía de la entrada. `customerName` es nulo sin cliente (antes «Sin cliente asignado»).
  - C-F03-22 a C-F03-24: `chargedAmount` es el total de la factura de la entrada (en ingreso, la de la entrada; si no, la del ciclo); nulo sin cobro. `canPrint` sigue el contrato al pie de la letra (pesaje y tiquete), también en una fila anulada; `canEditWeights` del detalle = `canEdit` con algún peso tomado. `modality` fuera de la lista responde 400 «El valor «{valor}» no es válido para modality.». Las diferencias de salida y solo báscula van en valor absoluto. El orden por defecto desempata por Id ascendente (las entradas de un mismo camión comparten la fecha de ingreso).
  - C-F03-25, C-F03-26, C-F03-34: un servicio descartado sin ciclo responde `voided.reason` «Operación descartada.»; `weights.manifest.documentLabel` es el número del manifiesto de la entrada (o, sin él, el tipo y número del documento). C-F03-34 de un ciclo de ingreso devuelve la entrada que tiene ese ciclo asignado; idéntico a C-F03-25.
  - C-F03-27: `licensePlate` ya era «contiene» (sin espacios ni guiones, CHG-05); `status` fuera de la lista responde 400 «El valor «{valor}» no es válido para status.».
  - Pruebas heredadas ajustadas a la cola y al historial nuevos: `InitiateCustomerIdTests.Queue_PendingService_ReturnsCustomerId` (ahora «Por pesar», con `customerName` y `category`), `DepartureGuardTests`, `WeighbridgeDashboardTests`, `SingleWeighingManifestNetTests` (tara = indicador − mercancía) y `WeighingOnlyWithoutCustomerTests` (el destinatario se lee en el detalle).

### 8.3 Backend, fase 3 — Tiquete, anulación y correcciones

- **Decisiones:** D32 a D36.
- **Endpoints:** C-F03-16, C-F03-35 a C-F03-41, C-F03-45, C-F03-46, C-F03-49 a C-F03-51 (grupo C; esquemas de `ticket.ts`, `void.ts`, `service-record.ts` y `weighing.ts`).
- **Archivos:** §3.2, filas de la fase 3. Sin migración.
- **Pruebas:** `TicketSectionsTests`, `TicketPdfTests`, `VoidByEntryTests`, `ServiceRecordCorrectionTests`, `ModifyWeightMerchandiseTests` (§5).
- **Casos QA:** QA2-F03-024 a QA2-F03-030.
- **Cuidado:** la anulación con ciclo reutiliza `VoidWeighingCommandHandler` sin cambiar sus mensajes; el alto del PDF se prueba leyendo el tamaño de la página generada.

### 8.4 Maquetación, fase 1 — Contratos, fuentes simuladas, cola y registro

- **Decisiones:** D5, D9 a D16, D20 a D25, D38 a D40, D44.
- **Contratos:** todos los de §2.3 (también los de las fases 2 y 3, para que las fuentes queden completas desde el inicio).
- **Fuentes:** las de D40, con sus datos simulados en español y sin personas reales (`DEC-007`), siguiendo los ejemplos de los wireframes; las reglas de los simulados usan `F/shared/mocks/` (`listQuery`, `createMockStore`, `mockProblem`, `mockDelay`). Los simulados reproducen los errores de §2.2 que la pantalla muestra (por ejemplo, el de la mercancía mayor que el indicador).
- **Pantallas:** P-BAS-01 (`index.vue` reescrita), P-BAS-02 a P-BAS-04 (`process/[entryLogId].vue`) con el panel de la cola.
- **Lista de cada wireframe:** campos, botones y su ubicación de `A/` §2.1 g y de `bascula.html` (P-BAS-01 a P-BAS-04), con los apartes de D10.
- **Pruebas:** `registration-weights.spec.ts`, `process-keys.spec.ts`, `mocks.spec.ts` y las de los componentes nuevos de la fase.
- **Guardias:** agrega las páginas nuevas y reescritas a `MAQUETACION_PAGES` (`FT/unit/guards/mock-sources.spec.ts:16`); ninguna importa una fuente de `INTEGRATED_SOURCES` (comprobado con grep en el cierre).
- **Sesión simulada** (`P02/` D10): `NUXT_PUBLIC_MOCK_SESSION=true` con `?roles=Admin,Scale` y, para Vigilancia, `Receiving`.
- **Estado:** hecha el 2026-11-24 (FE `d49a691`, rama `f2/f03-bascula`). `yarn test` 124 → 142 archivos y 685 → 744 pruebas, en verde; `yarn lint` 249 → 247 errores (avisos 328, sin cambio), ninguno en archivos nuevos; `yarn build` con código 0. Sin llamadas reales: la guardia de `mock-sources.spec.ts` en verde con las dos páginas en `MAQUETACION_PAGES`, el grep de cierre sin importaciones de `INTEGRATED_SOURCES` ni de componentes de hoy que llamen al API, y ninguna petición al API en el navegador. Los datos simulados pasan sus esquemas (`FT/unit/weighbridge/mocks.spec.ts`, `FT/unit/entries/mocks.spec.ts`). Ninguna ruta nueva en el menú. P-BAS-01 a P-BAS-04 revisadas en el navegador con la sesión simulada (`?roles=Admin,Scale`), con su lista del wireframe; capturas en `evidencias/fe1-01` a `fe1-10`.
- **Hecho:** los contratos de §2.3 (más `deposit-entry.ts` y `exit.ts` copiados de `P01/` §2.3) y las once fuentes de D40, con una Báscula simulada (`F/features/weighbridge/mocks/world.ts`) que comparten todas, así la cola, el registro, el historial y el detalle coinciden; la cola reescrita en `index.vue` (con `?estado=`); el registro en `process/[entryLogId].vue` con los componentes de D39 de la fase y el panel de la cola; las utilidades `registration-weights.ts`, `process-keys.ts`, `registration-form.ts` y `queue-display.ts`, y `F/features/entries/utils/correction-reason.ts` (regla de D3). Pruebas: `registration-weights`, `process-keys`, `registration-form`, `queue-display`, los dos `mocks.spec.ts` y una por componente nuevo de la fase.
- **Notas para FE-2, FE-3 e I-03:**
  - `StakeholderQuickDialog` y `DriverQuickDialog` no llaman a una fuente: la página les pasa `create` (y `update`), hoy la fachada de catálogos. En I-03 reciben las fuentes integradas de F01.
  - La página toma la clave de la entrada de ingreso (`warehouseStorageEntryId`, para C-F03-13) de la fila de la cola (C-F03-21), porque D5 solo lleva `servicio` en la consulta. Una entrada completada no está en la cola: el «Editar» del historial (FE-3) necesita otra forma de pasar esa clave (por ejemplo, en la consulta), que FE-3 debe resolver con el usuario si no la fija el plan.
  - Los pasos Cobro y Tiquete muestran un aviso hasta FE-2; F2 en una entrada «Por repesar» avisa que el repesaje llega en FE-2.
  - El simulado de C-F03-11 ya aplica la nota de BE-1 (§8.1): el repesaje es el opuesto al primer pesaje.

### 8.5 Maquetación, fase 2 — Cobro, tiquete, repesaje e impresión

- **Decisiones:** D17 a D19, D23, D33.
- **Pantallas:** P-BAS-05, P-BAS-06, P-BAS-07 y P-BAS-13 (con un PDF de ejemplo en el simulado de C-F03-35).
- **Lista de cada wireframe:** `A/` §2.1 g (P-BAS-05 a P-BAS-07 y P-BAS-13) y `bascula.html`.
- **Pruebas:** las de `WeighbridgeChargeStep`, `WeighbridgeTicketStep`, `ReweighDialog` y `TicketPrintDialog`.
- **Estado:** hecha el 2026-11-24 (FE `cd58697`, rama `f2/f03-bascula`). `yarn test` 142 → 149 archivos y 744 → 770 pruebas, en verde; `yarn lint` 247 → 247 errores (avisos 328, sin cambio), ninguno en archivos nuevos; `yarn build` con código 0. Sin llamadas reales: ninguna página nueva (todo vive en `process/[entryLogId].vue`, ya en `MAQUETACION_PAGES`), el grep de cierre sin `useApi`, `$api`, fuentes de `INTEGRATED_SOURCES` ni componentes de hoy que llamen al API (`useTicketPdf`, `BillingCollectForm`…), y ninguna petición fuera de la app en el navegador. Los simulados pasan sus esquemas (`FT/unit/weighbridge/mocks.spec.ts`, con la observación del detalle). Ninguna ruta nueva en el menú. P-BAS-05, P-BAS-06, P-BAS-07 y P-BAS-13 revisadas en el navegador con la sesión simulada (`?roles=Admin,Scale`), con su lista del wireframe; capturas en `evidencias/fe2-01` a `fe2-09`.
- **Hecho:** el paso Cobro (`WeighbridgeChargeStep`: resumen con «Editar registro», `AppChargeForm` con los destinatarios de hoy, el cliente del depósito precargado, el conductor del registro, «+» de alta rápida, «Inmediato» y «Pendiente por facturar», y $0 con su motivo en la duplicada o por convenio; el error del cobro se muestra en el paso), el paso Tiquete (`WeighbridgeTicketStep`: tiquete, pesos por categoría, lo pendiente y el cobro; «Imprimir» desde el primer pesaje y «Finalizar»), `ReweighDialog` (P-BAS-07, el repesaje opuesto al primer pesaje, la mercancía al instante y su diferencia con el manifiesto) y `TicketPrintDialog` (P-BAS-13); las utilidades puras `charge-step.ts`, `reweigh.ts`, `ticket-print.ts` y `ticket-pdf.ts`, con sus pruebas, y una por componente. El encabezado oculta la acción principal, el switch y «Duplicar entrada» en Cobro y Tiquete, como los wireframes. Teclado (D23, R6): Enter cobra en Cobro y finaliza en Tiquete (el foco queda en el paso), el repesaje se abre solo al atender una entrada «Por repesar» y con F2, con el foco en el peso; Enter en el modal registra; Escape cierra solo el modal. Tras el repesaje la página pasa al Tiquete.
- **Decisiones del usuario (2026-11-24):** (1) el detalle suma `ticketObservations` (§2.2, §2.3 y la nota de §8.2 para BE-2); (2) el paso Tiquete lee el detalle por el ciclo (C-F03-34) que trae C-F03-15 (§2.4).
- **Notas para FE-3 e I-03:**
  - `ReweighDialog` y `TicketPrintDialog` reciben el detalle (`WeighbridgeDetail`) y llaman a sus fuentes (C-F03-11; C-F03-36 y C-F03-35): el historial y el detalle de FE-3 los montan igual. Quien los monte debe fijar el detalle al abrir (como `reweighDetail` en la página): al registrar el repesaje la consulta del detalle puede cambiar y desmontar el modal antes de que avise.
  - `useWeighbridgeDetail` (en `weighbridge.queries.ts`) recibe la clave `entry`, `service` o `cycle` (C-F03-25, C-F03-26 y C-F03-34).
  - El simulado de C-F03-35 responde ya los mensajes del contrato («El pesaje aún no tiene el primer peso…», «El repesaje aún no existe…»).
  - `ticket-pdf.ts` abre el PDF en una pestaña e imprime (si el navegador bloquea la ventana, lo descarga); reemplaza a `useTicketPdf`, que llama al API de hoy y que I-03 borra si nadie más lo importa.
  - En los simulados los errores no pasan por el notificador global (solo el interceptor del API real lo llama): el cobro y los modales muestran el error en su lugar; en I-03, con el API real, el cobro lo reclama con `handlesErrors`.

### 8.6 Maquetación, fase 3 — Historial, detalle, corrección, Vigilancia › Historial y `cycles/[id]`

- **Decisiones:** D6, D7, D26 a D31, D34, D35, D37.
- **Pantallas:** P-BAS-08 (`history/index.vue`), P-BAS-09 (`history/exits.vue`), P-BAS-10 (`history/weighing-only.vue`), P-BAS-11, P-TR-12, Vigilancia › Historial (`F/pages/operations/entries/history.vue`) y `cycles/[id].vue` con el detalle (las acciones de hoy que conserva, D32, se conectan en I-03).
- **Lista de cada wireframe:** `A/` §2.1 g (P-BAS-08 a P-BAS-11), `transversales.html` (P-TR-12) y el patrón de P-TR-02 y P-TR-03 para Vigilancia › Historial.
- **Pruebas:** las de `WeighbridgeEntryDetail`, `WeighbridgeHistoryActions`, `ServiceCorrectionDialog` y las del historial de Vigilancia.
- **Galería:** `F/pages/dev/components.vue` suma el detalle de P-BAS-11 con dos y con tres acciones, como referencia (`P02/` D20; `PAJ/` D15).
- **Estado:** hecha el 2026-11-24 (FE `ae34783`, rama `f2/f03-bascula`). `yarn test` 149 → 155 archivos y 770 → 795 pruebas, en verde; `yarn lint` 247 → 239 errores (avisos 328, sin cambio), ninguno en archivos nuevos; `yarn build` con código 0. Sin llamadas reales: la guardia de `mock-sources.spec.ts` en verde con las cinco páginas nuevas o reescritas en `MAQUETACION_PAGES`, el grep de cierre sin `useApi`, `$api`, fuentes de `INTEGRATED_SOURCES` ni componentes de hoy que llamen al API (`CorrectEntryLogDialog`, `ModifyWeighingDialog`, `useCycleDetail`, `useTicketPdf`…), y ninguna petición al API desde estas páginas en el navegador. Los simulados pasan sus esquemas (`FT/unit/weighbridge/mocks.spec.ts` valida cada fila del historial en las tres modalidades y cada detalle; `FT/unit/entries/mocks.spec.ts`). Ninguna ruta nueva en el menú. P-BAS-08 a P-BAS-11, P-TR-12, Vigilancia › Historial y `cycles/[id]` revisadas en el navegador con la sesión simulada (`?roles=Admin,Scale`; `Admin,Receiving` para Vigilancia; `Billing` para `cycles/[id]`), con su lista del wireframe; capturas en `evidencias/fe3-01` a `fe3-18`.
- **Hecho:** `history.vue` pasó a `history/index.vue` (D6) y se reescribió con `AppDataTable` en modo `server`, las pestañas Importación, Exportación e Inspección, las columnas del legacy con su filtro, el orden en el servidor, la fila anulada en rojo con su motivo en el tooltip y «Exportar»; `history/exits.vue` y `history/weighing-only.vue` con sus columnas (D27, D28); el drawer P-BAS-11 con `WeighbridgeEntryDetail` (dos acciones en el pie, tres en el menú «Acciones», `PAJ/` D3); `WeighbridgeHistoryActions` (Ver, Editar, Repesar, Imprimir y Anular según las marcas); `WeighbridgeEntryDialogs`, que monta para el historial, el drawer y `cycles/[id]` el repesaje, la impresión, la anulación con `ReasonDialog` y `CorrectionResultDialog` (C-F03-37 y C-F03-38) y la corrección P-TR-12 (`ServiceCorrectionDialog`, C-F03-16, solo lo que cambió y el motivo con el ciclo completo); `cycles/[id].vue` a página completa con el detalle por ciclo (C-F03-34), donde Facturación y Comercio Exterior solo imprimen; Vigilancia › Historial (`entries/history.vue`) con el patrón de AF-129, el drawer `EntryLogDetail` y `EntryLogCorrectionDialog` (D3, D37), «Autorizar salida» y «Agregar manifiesto»; la galería con P-BAS-11 de dos y tres acciones. Utilidades puras `entry-detail.ts`, `history-display.ts` y `service-correction.ts`, con sus pruebas, y una prueba por componente nuevo. La Báscula simulada suma cuatro camiones que ya salieron (exportación de un solo pesaje, inspección con el depósito confirmado, salida completada con guía y un solo pesaje anulado).
- **Decisiones del usuario y casos borde (2026-11-24):**
  - **`?entrada=` en el registro** (respuesta del usuario, «?entrada= en la URL»): «Editar» del historial y «Editar pesajes» de un ingreso abren `process/[entryLogId]?servicio=…&paso=registro&entrada={warehouseStorageEntryId}`; la página usa la fila de la cola y, si la entrada ya salió de ella, la de la consulta. Amplía la consulta de D5; sin cambio de contrato. «Editar pesajes» suma `#pesos`, que lleva el foco al P. indicador (D31).
  - **`?camion=` en el drawer de Salidas y Solo báscula** (`DEC-002`): D30 abre el drawer con `?id={clave}` y C-F03-26 pide además `entryLogId`; el drawer usa `?id={serviceRecordId}&camion={entryLogId}`.
  - El componente `WeighbridgeEntryDialogs` y el composable `useHistoryDrawer` no están en la lista de D39: reúnen los modales y el drawer que comparten las tres páginas y `cycles/[id]`, sin cambiar ningún componente compartido (D38).
  - Defecto de FE-1 corregido en la fase: al abrir una entrada desde el historial, sin la caché de la cola, el tipo de documento llegaba después que la entrada y quedaba vacío; ahora se completa cuando llegan los tipos.
  - El simulado de `canEditWeights` sigue la nota de BE-2 (`canEdit` con algún peso tomado).
- **Notas para I-03:**
  - `cycles/[id]`: conectar lo que D32 conserva de hoy y no se maquetó: «Modificar pesaje» (Admin, Scale, Billing; `ModifyWeighingDialog` con C-F03-45 y C-F03-46) y la fecha de ingreso del depósito (Admin, Scale, ForeignTrade; `EditDepositEntryDateDialog` con C-F03-51). «Editar pesajes» del detalle queda para Admin y Báscula.
  - «Imprimir tiquete» en `cycles/[id]` lo ven Facturación y Comercio Exterior (el PDF es `ActiveUser`), pero `TicketPrintDialog` guarda antes la observación con C-F03-36 (`ScaleAccess`): con el API real esos roles recibirían 403. I-03 decide cómo imprimen sin guardar la observación (por ejemplo, saltar el guardado si no cambió) o lo pregunta.
  - El simulado oculta «Imprimir» en una fila anulada; según la nota de BE-2, `canPrint` sigue el contrato también anulada: con el API real puede aparecer.
  - Borrar en I-03, si nadie más los importa: `CorrectEntryLogDialog.vue` (Vigilancia ya no lo usa), `WeighbridgeHistoryTable.vue`, `WeighbridgeHistoryFilters.vue`, `WeighbridgeCycleTimeline.vue`, `WeighbridgeCycleTickets.vue`, `useWeighbridgeHistory.ts`, `useWeighbridgeHistoryTotals.ts`, `useCycleDetail.ts` y `useVoidWeighing.ts` (trampa 7).
  - Menú (D43): Historial de entradas, de salidas y de solo báscula; `list-pattern-routes.ts` pasa las tres rutas y `/operations/entries/history` a `PATTERN`.

---

## 9. Riesgos

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R1 | El registro nuevo vuelve lento el pesaje (PRF-002, riesgo R6 del plan maestro) | D23 conserva Enter y F2; D3 quita el motivo de la corrección en el registro; la medición se hace en el despliegue final |
| R2 | El primer peso vive en el vínculo y el ciclo lo copia en el cobro: dos lugares para el mismo dato | `WeighbridgeEntryStateResolver` y una sola regla de copia en el cobro, con pruebas; con ciclo, el vínculo deja de leerse para el peso |
| R3 | Los simulados se separan del backend (riesgo R3 del plan maestro) | El contrato de §2 es la única fuente; I-03 valida cada respuesta con su esquema, como I-01 |
| R4 | `RecordWeighingHandler` y la anulación tienen muchas reglas de hoy (perecederos, varios pesajes) | La fase 1 solo cambia de dónde sale el modo y el caso del ciclo cerrado; las demás reglas y sus pruebas siguen |
| R5 | Las pantallas nuevas llaman sin querer al API real a través de un componente de hoy | D40: la fachada `catalog.source.ts` y el grep de cierre de la maquetación |
| R6 | `cycles/[id]` mezcla el detalle nuevo con acciones de hoy | D32 las limita a los roles que las usan; F05 revisa el enlace |
| R7 | El historial lista entradas sin ciclo y el operario las confunde con pesajes | Columnas del ciclo vacías y el estado «Por pesar» o «Por cobrar» en la fila |

---

## 10. Fuera de alcance

- La edición del ingreso de CE (P-CE-03), el detalle del depósito y su enlace al ciclo (F05); las salidas de CE y Bodega (F06); los relojes y la recepción de Bodega (F04).
- Quitar `BillingCollectForm`, `useUnitMeasures` y los servicios de `F/features/weighbridge/` que otros módulos importan (D41, D42).
- Retirar `POST weighbridge/cycles/{cycleId}/void` (no estaba en la lista aprobada en D4; queda sin uso en las pantallas de F03) y `service_records.single_weight_only` (§4).
- El reporte de báscula (`/operations/weighbridge/reports`) y el dashboard, salvo sus enlaces (D7).
- Los avisos configurables (F09), staging y el despliegue final (`PM/` §7.3), y estimar esfuerzo.

---

## 11. Prompts por parte

- Parte 1 (backend): [prompt-f2-f03-bascula-backend-2026-11-24.md](prompt-f2-f03-bascula-backend-2026-11-24.md), rama `f2/f03-bascula` del backend.
- Parte 2 (maquetación): [prompt-f2-f03-bascula-maquetacion-2026-11-24.md](prompt-f2-f03-bascula-maquetacion-2026-11-24.md), rama `f2/f03-bascula` del frontend.
- Parte 3 (I-03): [prompt-f2-f03-bascula-integracion-2026-11-24.md](prompt-f2-f03-bascula-integracion-2026-11-24.md), las dos ramas.
- Planificador (ejecutado): [prompt-f2-f03-bascula-planificador-2026-11-24.md](prompt-f2-f03-bascula-planificador-2026-11-24.md).

---

## 12. Mensajes de commit sugeridos

Cada uno termina con la línea de coautoría que indique la sesión.

| Fase | Repo | Mensaje |
| --- | --- | --- |
| BE-1 | BE | `feat(bascula): el registro guarda el primer peso y el ciclo nace con él en el cobro; conductor por Id y una sola alta rápida (DEC-080, F03)` |
| BE-2 | BE | `feat(bascula): cola por entrada, historial en tres listados con orden y filtros, y detalle del ciclo (DEC-080, F03)` |
| BE-3 | BE | `feat(bascula): tiquete con secciones y alto según el contenido, anulación con o sin ciclo y corrección de salidas y solo báscula (DEC-080, F03)` |
| FE-1 | FE | `feat(bascula): maquetación de la cola y del registro en página propia con datos simulados (DEC-080, F03)` |
| FE-2 | FE | `feat(bascula): maquetación del cobro, el tiquete, el repesaje y la impresión (DEC-080, F03)` |
| FE-3 | FE | `feat(bascula): maquetación del historial en tres páginas, el detalle en drawer y Vigilancia › Historial (DEC-080, F03)` |
| I-03 | BE y FE | `merge: I-03, F03 «Báscula» en fase-2 (DEC-080, DEC-081)` (fusión) y `feat(bascula): integración de F03 con el API (DEC-080, F03)` (FE) |
| Cada fase | docs | `docs(f03): fase N de F03 cerrada (sprint 11)` |

---

## 13. Integración I-03 (parte 3)

Un agente con los dos repos (M1, M10), cuando BE-1 a BE-3 y FE-1 a FE-3 están cerradas y con push. Ocupa los dos repos.

### 13.1 Fuentes http

Por cada `*.source.ts` de F03, escribe su `*.http.ts` con `contractApi` (`F/shared/http/contract-api.ts`) y los esquemas de §2.3 (`.parse` en cada respuesta; un fallo de esquema se registra en consola y se muestra como error del API), cambia la línea activa y lo agrega a `INTEGRATED_SOURCES` (`FT/unit/guards/mock-sources.spec.ts:22-39`):

| Fuente | Endpoints | Pantallas |
| --- | --- | --- |
| `F/features/weighbridge/services/queue.source.ts` | C-F03-21 | P-BAS-01, panel de la cola |
| `registration.source.ts` | C-F03-01, C-F03-03, C-F03-04, C-F03-13, C-F03-14, C-F03-15, C-F03-43, C-F03-44, C-F03-52; C-F03-17 | P-BAS-02 a P-BAS-04 |
| `payment.source.ts` | C-F03-05 a C-F03-10 | P-BAS-05 |
| `weighing.source.ts` | C-F03-11, C-F03-12, C-F03-45, C-F03-46 | P-BAS-02 a P-BAS-04, P-BAS-07, `cycles/[id]` |
| `history.source.ts` | C-F03-22 a C-F03-24 | P-BAS-08 a P-BAS-10 |
| `detail.source.ts` | C-F03-25, C-F03-26, C-F03-34 | P-BAS-06, P-BAS-11, `cycles/[id]` |
| `ticket.source.ts` | C-F03-35, C-F03-36 | P-BAS-13 |
| `void.source.ts` | C-F03-37, C-F03-38 | P-BAS-08 a P-BAS-11 |
| `service-record.source.ts` | C-F03-16 | P-BAS-03, P-BAS-04, P-TR-12 |
| `F/features/entries/services/entry-log.source.ts` | C-F03-27, C-F03-48, C-F03-17, C-F03-49, C-F03-50 | Vigilancia › Historial |
| `catalog.source.ts` (fachada, D40) | — | Se borra: sus usos pasan a `driver.source.ts`, `entry-reason.source.ts`, `stakeholder.source.ts`, `product.source.ts` y `packaging-type.source.ts` (C-F01-02, 15, 17, 18, 25, 26, 29, 69, 141) |

`cycles/[id]` conecta además las acciones de hoy de D32 (`ModifyWeighingDialog` y la fecha de ingreso, C-F03-51), con sus componentes de hoy.

### 13.2 Menú, rutas y enlaces

- `F/components/layout/menu-model.ts:45-55`: Báscula con Dashboard · Proceso de pesaje · Historial de entradas · Historial de salidas · Historial de solo báscula (D6, D43).
- `F/composables/useGlobalShortcuts.ts:23` y `F/pages/operations/weighbridge/dashboard.vue:21`, `:28`, `:43`, `:100`, `:108`, `:116`: a la cola con `?estado=…` o al historial nuevo; sin enlaces a `pending-reweigh`, `in-process` ni `recover` (D7).
- `F/features/entries/components/VehicleForm.vue:274`: el «+» de transportadora llama a C-F01-141 con `TRANSPORT_COMPANY` (D1).
- `FT/unit/guards/list-pattern-routes.ts`: `/operations/entries/history` y `/operations/weighbridge/history` pasan de `PENDING` (`:32-34`) a `PATTERN`; se agregan en `PATTERN` `/operations/weighbridge/history/exits` y `/operations/weighbridge/history/weighing-only`; `/operations/weighbridge` pasa de `OUTSIDE` (`:72`) a `PATTERN` (D24).
- `MAQUETACION_PAGES` (`FT/unit/guards/mock-sources.spec.ts:16`) queda vacía.

### 13.3 Se borra

Con `rm`, después de comprobar con grep que nada fuera de lo que se borra los importa (trampa 7; D41):

- **Páginas:** `F/pages/operations/weighbridge/recover.vue`, `in-process.vue`, `pending-reweigh.vue`.
- **Componentes de Báscula que solo usaban las pantallas viejas:** `StorageServiceForm`, `QuickCreateStakeholderDialog`, `CompleteEntryInfo`, `TruckQueue`, `TruckGoodsLines`, `WeightCapture`, `WeighbridgeProcessPanel`, `WeighbridgeProgress`, `OperationTypeSelector`, `OutputServiceForm`, `WeighingOnlyForm`, `RegistrationSummary`, `PendingEntryList`, `PreviousEntriesPanel`, `DocumentMatchBanner`, `CargoUnitsEditor`, `WeighbridgeHistoryTable`, `WeighbridgeHistoryFilters`, `WeighbridgeCycleTickets`, `WeighbridgeCycleTimeline`, `AdditionalOrdersDialog`, `EntryTicketExitPanel`, `AdditionalDepositCollect` (D42), `ModifyWeighingDateDialog`, `WeighingModificationNote`; `ModifyWeighingDialog` solo si `cycles/[id]` ya no lo usa (D32 lo conserva).
- **Composables, utilidades y tipos que quedan sin uso:** entre ellos `useRecoverableOperations`, `useOpenCycles`, `useOpenCycleByPlate`, `usePendingSecondWeight`, `useWeighbridgePending`, `useWeighbridgeHistory`, `useWeighbridgeHistoryTotals`, `useInitiateAdditionalDeposit`, `useExitWithEntryTicket`, `useCycleDetail`, `useTicketPdf` (si su lógica de impresión pasó a `TicketPrintDialog`), `utils/truck-drafts.ts`, `utils/multi-deposit-weighing.ts`, `utils/panel-route.ts`, y los métodos de `weighbridge-service.ts` que nadie llama (`quickCreateTransportCompany` incluido). Lo que importan Vigilancia, Bodega, CE o Facturación se queda (D41).
- **Pruebas** de lo que se borra (`FT/components/weighbridge/*.spec.ts` y `FT/unit/weighbridge/*.spec.ts` de los archivos borrados).
- **La fachada** `catalog.source.ts` y la carpeta `F/features/weighbridge/mocks/` (y `F/features/entries/mocks/` si solo tiene los de F03). `F/shared/mocks/` se queda.
- **No se borran** `BillingCollectForm`, `useUnitMeasures` ni `cycles/[id].vue` (D7, D42).

### 13.4 Casos QA y docs

- QA2-F03-031 a QA2-F03-050 en PASA, en el navegador, contra el backend local de `f2/f03-bascula`, sin la sesión simulada; QA2-F03-001 a 030 siguen en verde en la suite.
- Copia los casos con su resultado a `D/qa/casos-qa2-f03-bascula-AAAA-MM-DD.md`, con el formato de `D/qa/casos-qa2-f01-f02-2026-11-24.md`.
- Actualiza este plan (§8), `D/planes/README.md`, la matriz (`D/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md` §2.2) y `D/contexto/estado.md` (hito de I-03), y dile al usuario qué puede probar en local (`PM/` §5.3).

### 13.5 Criterio de salida

- Compuertas de `PM/` §6.1 en BE y §6.2 en FE (salvo «sin llamadas reales»), con las cifras antes y después.
- QA2-F03-031 a QA2-F03-050 en PASA.
- Ningún import de `mocks/` de una feature fuera de las pruebas; las carpetas `mocks/` de F03, borradas.
- Menú con las rutas de F03; páginas, componentes y pruebas viejas, borradas.
- Fusión con `--no-ff` de `f2/f03-bascula` en `fase-2` en los dos repos, y push.
