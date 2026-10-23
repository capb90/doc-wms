Eres el implementador de la corrección de **DEF-F11-008 (CRITICAL), DEF-F11-009 (MAJOR), DEF-F11-007 (MINOR) y DEF-F11-006 (TRIVIAL)**, y de **dos reglas de negocio que el usuario decidió el 2026-10-05** a partir de las observaciones de la sesión S2 del re-test de QA (fase 11) del WMS de Bodegas Asociadas. Modelo recomendado: **Opus 5.5** (complejidad media-alta: DEF-F11-008 toca la integridad de datos del conductor en tres flujos de báscula y la regla de exportación toca la salida). Todo lo anterior está corregido y con commit. **El re-test de QA sigue en curso sobre la base local: no la toques.**

Implementa en este orden: **DEF-F11-008 → DEF-F11-009 → R-EXP (repesaje de exportación) → R-TRZ (trazabilidad del descartado) → DEF-F11-007 → DEF-F11-006**. Cada punto entrega su código, sus pruebas y, si tiene ficha, la actualización de la ficha.

## Lee primero
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. `docs/qa/plan-correccion-defectos.md`:
   - la sección «4.0 Reglas comunes» (en especial 4.0.2 migraciones, 4.0.4 lint y 4.0.10 «Sin retrocesos funcionales»);
   - las tarjetas **CHG-06, CHG-33, CHG-34, CHG-37, CHG-42, CHG-45, CHG-46 y CHG-47**.
3. `docs/qa/resultados/F11-informe-S2-2026-10-05.md` (§5, incluidas las «Observaciones sin ficha») y las cuatro fichas `docs/qa/resultados/defectos/DEF-F11-006.md` a `DEF-F11-009.md`, con sus evidencias en `docs/qa/resultados/evidencias/F11/`.
4. `docs/qa/00-plan-maestro.md` §10 (Salida de importación, Báscula).

---

## DEF-F11-008 (CRITICAL): Báscula sobrescribe al conductor existente con los datos de otra persona

**Causa (confirmada en el código).**
- En `Wms.Application/Weighbridge/Common/Services/EntryLogInfoUpdater.cs`, cuando el ingreso ya tiene conductor, `UpdateExistingDriver` llama `driver.Update(...)` con lo que digitó el operario, aunque el documento sea de otra persona.
- La búsqueda por tipo y número (`CreateAndAssignDriverAsync`) solo se usa cuando el ingreso no tiene conductor.
- El registro del conductor es compartido, así que el cambio llega a todos sus ingresos, órdenes de cargue, tiquetes y guías, incluidas las reimpresiones.
- Lo usan `UpdateEntryLogInfoHandler` y `RegisterStorageEntryHandler`, y desde CHG-46 también `InitiateWeighingOnlyHandler` e `InitiateOutputWeighingHandler`.

**Decisión del usuario (cerrada).** Báscula decide por documento:
1. **Mismo documento** (tipo y número iguales a los del conductor actual del ingreso, comparando el tipo sin distinguir mayúsculas y el número sin espacios): se corrigen los datos de ese conductor (nombres, apellidos, país, teléfono). Es el mismo conductor con un error de digitación.
2. **Documento distinto**: se busca el conductor con ese tipo y número. Si existe, se asigna al ingreso **sin modificarlo**. Si no existe, se crea con lo digitado y se asigna. **El conductor anterior no cambia.**
3. **Sin documento**, cuando se envían nombres pero no tipo o número y el ingreso ya tiene conductor: no se toca al conductor. Responde 400 con un mensaje que pida el documento para cambiar de conductor. Excepción: si los nombres son exactamente los del conductor actual (la pantalla reenvía lo precargado), no hay cambio y no hay error.

**Cambios.**
- Reescribe la rama «el ingreso ya tiene conductor» de `EntryLogInfoUpdater` con esas tres reglas. Reutiliza la búsqueda y la creación de `CreateAndAssignDriverAsync` en un solo método de «buscar o crear y asignar».
- Unifica el parseo del tipo de documento: hoy `Enum.TryParse` distingue mayúsculas, y en S2 «Passport» no falló. Sigue el patrón de DEF-F11-002: `ignoreCase: true` y rechazo de valores que no son nombres de la lista (no números), con el mensaje de valores permitidos que ya existe.
- Comentario `// DEF-F11-008 — …` en el estilo del archivo y `<summary>` del servicio actualizado.
- **Fuera de alcance:**
  - Que las guías y los tiquetes guarden una copia del conductor con que se emitieron (requeriría migración y otra decisión).
  - La edición de conductores desde Admin (`PATCH drivers/{id}`), que sigue igual.
  - La pantalla de báscula, salvo que hoy no muestre el mensaje del 400 de la regla 3. En ese caso, solo asegúrate de que el aviso global lo muestre.

**Pruebas.**
- **Unitarias o de integración del servicio**, una por regla:
  - mismo documento → se corrige el nombre y el ingreso conserva el `DriverId`;
  - documento distinto existente → `DriverId` del existente y ninguno de los dos conductores cambia;
  - documento distinto nuevo → un conductor más y el anterior intacto;
  - sin documento con nombres distintos → 400 y nada cambia;
  - sin documento con los mismos nombres → sin cambios ni error;
  - tipo en otra combinación de mayúsculas → aceptado;
  - tipo inexistente → 400.
- **Integración de punta a punta** con los tres flujos, registro con depósito, Solo báscula (`weighing-only/initiate`) y Salida (`output/initiate`):
  - ingreso con el conductor A;
  - báscula digita el conductor B;
  - el ingreso queda con B y A conserva su nombre y documento;
  - una orden de cargue o una guía emitida antes con A sigue mostrando a A.

  Reutiliza los escenarios de `Wms.IntegrationTests`.

---

## DEF-F11-009 (MAJOR): el depósito adicional sin cliente bloquea el camión en báscula

**Causa.**
- En `app/pages/operations/weighbridge/index.vue`, `handleAdditionalDepositConfirm` envía `recipientMode: "registered"` sin cliente.
- Si el depósito adicional se registró sin cliente, `BillingRecipientFactory` responde «Debe seleccionar el cliente registrado a facturar.».
- La ficha queda en el paso de cobro sin ningún control para elegirlo, y el camión no avanza hasta que Comercio Exterior asigne el cliente.

**Decisión del usuario (cerrada).**
- El paso de confirmar el depósito adicional **muestra el selector de destinatario** que ya usa el cobro (`BillingCollectForm.vue`): registrado, no registrado o consumidor final, según cómo esté hecho hoy.
- Lo **prellena con el cliente del depósito adicional** si lo tiene. Si no lo tiene, no lo prellena con el del depósito principal.
- El monto sigue en 0 y el cobro sigue sin método de pago visible: es una factura en cero.
- La confirmación envía el destinatario elegido al mismo endpoint de hoy.

**Cambios.**
- Reutiliza el componente o la sección de destinatario de `BillingCollectForm.vue` sin duplicarla. Si para eso hay que extraer un subcomponente, hazlo sin cambiar el cobro normal.
- El backend ya acepta los tres modos en `ProcessStoragePaymentHandler` para el depósito adicional (`BillingRecipientFactory.CreateInvoice` con `isZeroValue: true`). Confírmalo con una prueba y no lo cambies, salvo que algún modo falle. En ese caso, detente y repórtalo.
- Enter (`collect`) sigue confirmando el paso. Si falta el destinatario, se marca el campo y no se envía.

**Pruebas.**
- **Vitest** del paso:
  - con cliente en el depósito, prellenado y envío con ese cliente;
  - sin cliente, el envío queda bloqueado hasta elegir;
  - consumidor final enviado.
- **Integración**: un depósito adicional sin cliente confirmado con consumidor final y con cliente registrado → 200, factura en cero, ficha al pesaje intermedio.

---

## R-EXP (decisión del usuario): repesaje de salida de exportación sin cargue

**Observación de S2.** Con 2026OC00005 «En progreso» y sin cargar, báscula cerró el repesaje de salida, y el cargue posterior despachó la orden. Para importación, CHG-33 lo impide; para exportación no había regla.

**Decisión (cerrada).** Igual que en importación: **el repesaje de salida responde 409 mientras alguna orden de cargue del pesaje no esté «Cargada»**. Aplica a exportación y a cualquier tipo de orden. Mensaje en español que diga qué orden falta y que primero se registre el cargue en Bodega, en el estilo de los mensajes de CHG-33.

**Cambios.**
- Ubica dónde se cierra el pesaje de salida (`Weighbridge/Commands/Output/…` y los servicios comunes `EntryTicketExitRules`, `AdditionalOutputOrderRules` y `SharedOutputDispatch`) y dónde CHG-33 valida la importación.
- Pon la regla en un solo lugar compartido, de modo que valga para la orden principal y para las adicionales.
- La pantalla de báscula muestra el 409 con el aviso global. Si existe la cola o el estado «Falta cargue» (CHG-36 hace algo parecido con «Falta llegada a Bodega»), úsalo para que el operario lo vea antes de intentar. Si no existe, no lo crees.

**Sin retrocesos.**
- El flujo normal sigue igual: Bodega carga, la orden queda «Cargada», báscula repesa y la orden se despacha (o espera guía si es de importación, CHG-33).
- Lo mismo vale para la salida con tiquete de ingreso (CHG-33/DEF-F8-003) y para la salida de un camión sin orden de cargue.
- Revisa las pruebas existentes de salida: si alguna repesa una orden sin cargar a propósito, **detente y repórtala** antes de cambiarla.

**Pruebas.** De integración:
- orden de exportación «En progreso» → repesaje 409 con el mensaje;
- tras el cargue → repesaje 200 y orden despachada;
- orden adicional sin cargar → 409.

---

## R-TRZ (decisión del usuario): servicio descartado sin salida en trazabilidad

**Observación de S2.**
- En el tablero de trazabilidad, un camión cuyo servicio se descartó en báscula y que no ha salido aparece «En portería».
- El criterio 2 de CHG-42 pide «Cancelado».
- La causa probable es que CHG-06 desvincula el servicio del ingreso al descartarlo, y entonces `TruckStageResolver` ve el ingreso «sin servicio» (regla 2).

**Decisión (cerrada).**
- El camión cuyo **último servicio fue descartado y no tiene un servicio vigente** aparece **«Cancelado»** y no cuenta en «En portería».
- Si después del descarte se le registró un servicio nuevo (CHG-06 lo permite), manda el estado del servicio nuevo.
- Al salir, se aplica la regla (1) que ya existe.

**Cambios.**
- En la consulta del tablero (`GetTraceabilityDashboard`), averigua para cada ingreso si su último servicio fue descartado, usando el vínculo que exista hoy: el ciclo de báscula cancelado del ingreso, el registro de servicio descartado o la auditoría del descarte.
- Pásalo a `TruckStageResolver` (por ejemplo, un parámetro `lastServiceDiscarded`) y respétalo antes de la regla (2).
- Ajusta `TraceabilitySummaryCalculator` si el contador depende de la etapa.
- **Si no hay un vínculo fiable sin cambiar el esquema, detente y repórtalo** con la opción que propones. No generes migración sin aprobación.
- **Fuera de alcance:** el camión de recepción directa «En tránsito» sin contador propio (otra observación de S2).

**Pruebas.**
- Unitarias de `TruckStageResolver`: descartado sin salida → Cancelado; descartado con servicio nuevo → etapa del nuevo.
- De integración del tablero: descartar y consultar → Cancelado y no cuenta en «En portería».
- Las pruebas existentes de trazabilidad pasan sin editarlas.

---

## DEF-F11-007 (MINOR): «Modificado por N/A el N/A · Razón: N/A» en el historial de báscula

**Causa.**
- `app/pages/operations/weighbridge/history.vue` (≈647-651) lee `weighing.modifiedBy`, `modifiedAt` y `modificationReason`.
- El API devuelve `weightModifiedAt`, `weightModifiedById` y `weightModificationReason` (`WeighbridgeCycleDetailDto`, con `GetWeighbridgeCycleHandler` y `GetOpenCycleByPlateHandler`), sin el nombre del usuario.

**Cambios.**
- **Backend:** agrega `WeightModifiedByName` al DTO del pesaje y llénalo en los handlers que llenan `WeightModifiedById`, con el nombre visible del usuario, igual que otros DTO que ya muestran autor. Si el historial usa otro endpoint o DTO, aplícalo también ahí.
- **Frontend:**
  - el recuadro lee `weightModifiedByName`, `weightModifiedAt` (con `formatColombiaDateTime`) y `weightModificationReason`;
  - corrige los tipos en `features/weighbridge/types/` (`requests.ts` y `weighbridge-cycle.ts`) para que coincidan con el API y retira los campos que no existen;
  - si el detalle del ciclo (`cycles/[id].vue`) muestra el mismo recuadro, corrígelo igual;
  - sin dato, muestra «—», no «N/A».

**Pruebas.** Integración: modificar un peso y `GET weighbridge/cycles/{id}` trae el nombre. Vitest: el recuadro muestra autor, fecha de Colombia y razón.

---

## DEF-F11-006 (TRIVIAL): el detalle de una factura en cero se titula «pendiente de número»

**Cambio.** En `app/pages/billing/invoices/[id].vue` (≈42), el título usa la misma regla que `InvoiceActionsDialog.vue`:
- con número: «Factura {número}»;
- sin número y `isZeroValue`: «Factura en cero»;
- sin número y no en cero: «Factura pendiente de número».

No cambies nada más de la página.

**Prueba.** Vitest o prueba de la función del título con los tres casos.

---

## Sin retrocesos (regla 4.0.10)
- **DEF-F11-008:**
  - el operario sigue pudiendo completar o corregir los datos del conductor del ingreso, y cambiar de conductor digitando su documento;
  - Vigilancia, la recepción sin báscula y Admin no cambian;
  - el registro con depósito, Solo báscula y Salida siguen funcionando con un ingreso sin conductor.
- **DEF-F11-009:** el cobro normal, el de Solo báscula y el de salida no cambian. CHG-34 (una factura por cliente en multicliente) sigue igual.
- **R-EXP:** ver su sección.
- **R-TRZ:** los demás rótulos y contadores del tablero no cambian.
- Las pruebas existentes pasan sin editarlas, salvo las que una sección te manda reportar.

## Base de datos y entorno
- **No uses la base, el API ni el frontend locales**: tienen el dataset del re-test de QA. No los reinicies. Las pruebas de integración usan su propio PostgreSQL con Testcontainers (Docker activo).
- No se espera migración (`WeightModifiedByName` se calcula en la consulta). Al terminar, `dotnet ef migrations has-pending-model-changes` no debe reportar cambios. Si algo exigiera una migración, detente y repórtalo antes de generarla; nunca edites archivos generados ni uses SQL manual.

## Restricciones (obligatorias)
- Trabaja en `develop` de los dos repos. **No crees ramas, no hagas `git add`, commit, push ni merge**: entregas los mensajes de commit y el usuario hace los commits.
- No copies contraseñas ni secretos. No toques producción ni `infra/`.
- Textos y comentarios en español. Respeta la estructura por features.
- Nada fuera del alcance de arriba. En particular, no atiendas las otras observaciones de S2:
  - «Editar» del manifiesto en un depósito anulado;
  - «Moneda» y «Valor Comercial» vacíos en EXP00001;
  - «camión sin placa» en el aviso de diferencia;
  - comprobante de 6 MB;
  - título «Recurso duplicado.» en los 409.

  Quedan para S3.
- Si el código real contradice este prompt, adapta a lo que hay sin cambiar el comportamiento pedido y anótalo. Si el comportamiento cambia, detente y repórtalo.

## Fichas
- En `DEF-F11-006.md` a `DEF-F11-009.md`:
  - **Estado** «Corregido»;
  - fila «Corregido» en el Historial con la fecha, el resumen del cambio, las pruebas y «commits: pendiente».
- En `DEF-F3-008.md` (reabierta por DEF-F11-008), agrega la misma fila «Corregido» que remite a DEF-F11-008.
- En `defectos/INDICE.md`, actualiza solo esos estados.
- R-EXP y R-TRZ no tienen ficha: descríbelos en la entrega para que QA los re-teste.
- No modifiques los informes de S0, S1 y S2 ni otras fichas.

## Verificación antes de terminar
1. `dotnet build` sin errores ni advertencias nuevas.
2. `dotnet test` de `Wms.Tests` (1550 hoy) y `Wms.IntegrationTests` (235 hoy) en verde. Reporta los totales antes y después.
3. `has-pending-model-changes` sin cambios.
4. En `Frontend/wms`:
   - `yarn test` en verde (246 hoy);
   - `yarn build` con código 0;
   - `yarn lint` con **no más de 279 errores** y 0 en archivos nuevos. Reporta la cifra.
5. `git status` en los dos repos: solo los archivos de este alcance, más este prompt y las fichas. Si aparece `components.d.ts` regenerado, indícalo aparte.

## Entrega
Responde con:
1. Los archivos creados o modificados, agrupados por punto (DEF-F11-008, DEF-F11-009, R-EXP, R-TRZ, DEF-F11-007, DEF-F11-006).
2. El resultado de cada compuerta, con números.
3. Las desviaciones del prompt y cualquier prueba existente que hayas tenido que reportar, con lo que propones.
4. Lo que QA debe re-testear en S3 por punto:
   - DEF-F11-008 / DEF-F3-008: F3-CAM-010 y F3-CAM-011, con conductor distinto en los tres flujos, más la reimpresión de 2026S00001;
   - DEF-F11-009: F3-MUL-002 y F3-MUL-003 sin cliente;
   - R-EXP: repesaje con OC de exportación sin cargar;
   - R-TRZ: descartado sin salida en el tablero;
   - DEF-F11-007: F3-COR-002 y F3-COR-003;
   - DEF-F11-006: F6-INV-011.
5. **Los mensajes de commit**, listos para pegar, cada uno por separado:
   - **Backend:** `fix(qa-f11): conductor de báscula por documento, repesaje solo con cargue, descartado como cancelado y autor de la modificación de peso (DEF-F11-008, DEF-F11-007)`, con una línea por cambio. Menciona R-EXP y R-TRZ en el cuerpo.
   - **Frontend (código):** `fix(qa-f11): destinatario del depósito adicional, autor de la modificación de peso y título de la factura en cero (DEF-F11-009, DEF-F11-007, DEF-F11-006)`, con una línea por cambio.
   - **Frontend (documentación):** `docs(qa-f11): fichas DEF-F11-006 a DEF-F11-009 corregidas y DEF-F3-008`. Este prompt puede ir en el mismo commit.
   - Todos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí.** La verificación en pantalla la hace QA en la S3, después de reiniciar el API y el frontend con estos cambios.
