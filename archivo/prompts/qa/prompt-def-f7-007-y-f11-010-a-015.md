Eres el implementador de la corrección de los defectos abiertos tras la sesión S3 del re-test de QA (fase 11) del WMS de Bodegas Asociadas: **DEF-F7-007, DEF-F11-011, DEF-F11-012 y DEF-F11-013 (MINOR)** y **DEF-F11-010, DEF-F11-014 y DEF-F11-015 (TRIVIAL)**. Modelo recomendado: **Sonnet 5.5** (complejidad media: siete cambios acotados; el más delicado es DEF-F7-007, de un reporte de facturación). Todo lo anterior está corregido y con commit. **El re-test de QA sigue sobre la base local: no la toques.**

Implementa en este orden: **DEF-F7-007 → DEF-F11-012 → DEF-F11-011 → DEF-F11-013 → DEF-F11-010 → DEF-F11-014 → DEF-F11-015**. Cada defecto entrega su código, sus pruebas y la actualización de su ficha.

## Lee primero
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. `docs/qa/plan-correccion-defectos.md`:
   - la sección «4.0 Reglas comunes» (en especial 4.0.2 migraciones, 4.0.4 lint y 4.0.10 «Sin retrocesos funcionales»);
   - las tarjetas **CHG-21, CHG-29, CHG-40, CHG-45, CHG-56, CHG-65 y CHG-76**.
3. `docs/qa/resultados/F11-informe-S3-2026-10-06.md` (§5 y §9).
4. Las siete fichas en `docs/qa/resultados/defectos/`, con sus evidencias en `evidencias/F11/`. En particular, la fila «Reabierto» del Historial de `DEF-F7-007.md` y `evidencias/F11/S3-observaciones-S2.txt`.

---

## DEF-F7-007 (MINOR, reabierto): el reporte por CPI pierde la factura anulada al refacturar

**Causa (de la ficha).**
- `DepositInvoiceLinks.Resolve` (CHG-65) encuentra las facturas de un depósito por sus períodos y por las líneas que apuntan a esos períodos.
- Al refacturar, el recálculo del período abierto borra el período original, crea uno nuevo para la factura nueva y deja la línea de la anulada con `StorageBillingPeriodId` en NULL.
- Por eso la unión ya no encuentra la anulada.

**Decisión (cerrada).** Se agrega un tercer vínculo **sin cambiar el esquema ni el recálculo**:
- una factura **anulada cuyo `ReissuedAsInvoiceId` apunta a una factura ya incluida** en el reporte del depósito también se incluye;
- se sigue la cadena completa: la anulada de una anulada también aparece, con un tope de profundidad razonable, por ejemplo 10, para no ciclar.

**Rango de la anulada:**
- su propio `PeriodStartDate`/`PeriodEndDate` si los tiene;
- si no, el de la factura que la reemplazó;
- la fecha límite, igual que la de la que la reemplazó.

La fila de la anulada se marca como hoy marca CHG-65 la refacturación (`isReissued` o el campo que exista). La nueva debe poder identificar a cuál reemplazó, si el DTO ya lo permite. **No agregues campos al DTO salvo que CHG-65 no tenga ninguno para esto**; en ese caso, agrega solo el mínimo y anótalo.

**Cambios.**
- Extiende `DepositInvoiceLinks` (o el handler de `GET reports/deposit-billing`) con ese vínculo, en el estilo del archivo, con un `<summary>` que cite DEF-F7-007.
- Si el reporte por CPI y el de un depósito usan la misma resolución, la corrección debe valer para los dos.
- **Fuera de alcance:** que el recálculo deje de borrar el período original. Es el comportamiento decidido en D10/D11 y lo usan otras pruebas.

**Pruebas.**
- **Unitarias de la resolución:**
  - anulada sin período enlazada por `ReissuedAsInvoiceId` → aparece;
  - cadena de dos refacturaciones → aparecen las tres facturas;
  - anulada sin refacturar → sigue como hoy.
- **Integración**, con el escenario de F7-REP-022:
  - una factura en Borrador y otra Aprobada con N.º, anuladas y refacturadas;
  - `GET reports/deposit-billing` del depósito → aparecen la anulada y la nueva, con su marca.

---

## DEF-F11-012 (MINOR): Comercio Exterior puede editar el manifiesto DIAN de un depósito anulado

**Decisión (cerrada).** Un depósito **anulado** es de solo lectura también para el manifiesto, como «Información General» (CHG-21) y los levantes y etiquetas (CHG-40).

**Cambios.**
- **API.** `PATCH imports/{id}/manifest` responde **400 «No se puede modificar el manifiesto de un depósito anulado.»** si el depósito está anulado. La regla va en el dominio o en el handler, en el mismo estilo que CHG-21/CHG-40; reutiliza su guardia si existe.
- **Auditoría.** Revisa los demás `PATCH` de datos documentales del depósito en `ForeignTradeController` (importación, exportación e inspección): documento, carta porte, fechas, cliente, transportadora y similares. Lista cuáles ya rechazan el anulado y aplica la misma regla a los que no.
  - **No toques** las acciones que por diseño operan sobre un anulado.
  - **Solo se bloquea el estado Anulado**; los depósitos Cerrados siguen como hoy.
- **Pantalla.** En `app/pages/foreign-trade/imports/[id]/index.vue` (y en exportación e inspección si tienen la misma tarjeta), la tarjeta del manifiesto no ofrece «Editar» en un depósito anulado. Pásale el estado como ya se hace con «Información General».

**Pruebas.**
- Integración: PATCH del manifiesto en anulado → 400; en Borrador o Confirmado → 200 como hoy; lo mismo para cada endpoint que hayas cubierto.
- Vitest: la tarjeta no muestra «Editar» con el estado anulado.

---

## DEF-F11-011 (MINOR): el filtro por tiquete del historial de báscula no encuentra Solo báscula ni Salida

**Causa.** `Wms.Application/Weighbridge/Queries/GetWeighbridgeHistory/WeighbridgeHistoryFilters.cs` (≈60-66) solo compara `WarehouseStorageEntries.TicketNumber`. Los ciclos sin depósito guardan el tiquete en `WeighbridgeCycle.TicketNumber`.

**Cambio.**
- El filtro por tiquete compara **el tiquete del ciclo o el de cualquiera de sus entradas de depósito**, con el mismo tipo de comparación que usa hoy (exacta o parcial, y con o sin mayúsculas).
- Debe seguir traduciéndose a SQL.
- Si la exportación a Excel del historial usa otro filtro, aplica lo mismo.

**Pruebas.** Integración: filtrar por el tiquete de un depósito, de un Solo báscula y de una Salida → cada uno devuelve su operación; combinado con la placa, también.

---

## DEF-F11-013 (MINOR): el detalle de exportación e inspección no muestra la moneda ni el valor

**Cambios.**
- **API.** Los handlers de detalle de exportación (`GetExportDepositDetailHandler`) y de inspección proyectan `Currency` y `CargoValue`, igual que el de importación. Agrega los campos a sus DTO con los mismos nombres que en importación.
- **Pantalla.**
  - `DepositDetailGeneralInfoCard.vue` ya los recibe por props: pásalos desde las páginas de detalle de exportación e inspección.
  - En un Borrador, «Editar» abre el formulario con la moneda y el valor guardados, como en importación.
  - Si el formulario de edición de exportación o inspección no envía esos campos, revisa que el PATCH los conserve.

**Pruebas.** Integración: el detalle de exportación e inspección trae `currency` y `cargoValue`. Vitest (o la prueba que ya exista de la tarjeta): muestra los valores formateados es-CO.

---

## DEF-F11-010 (TRIVIAL): tras confirmar un depósito adicional, la ficha muestra el documento del depósito principal

**Causa.** `app/pages/operations/weighbridge/index.vue` (≈656-658, `registrationSummary`) toma el número del último depósito del ciclo, pero el documento lo toma de `cycleDocumentNumber`, que es el del servicio ancla.

**Cambio.**
- El resumen muestra el documento **del depósito que muestra**: usa el del registro del depósito adicional (lo que ve el paso de cobro), o el que traiga el API para ese depósito.
- Si la respuesta del API no trae el documento del depósito adicional, guárdalo en el estado de la ficha al registrar.
- No cambies la ficha del depósito principal.

**Prueba.** Vitest de la función o el computado del resumen: con depósito adicional → número y documento del adicional; sin adicional → igual que hoy.

---

## DEF-F11-014 (TRIVIAL): corregir productos en Comercio Exterior avisa «camión sin placa» y «El stock no cambió»

**Causa.**
- `Wms.Application/ForeignTrade/Common/Services/DepositProductEditing.cs` (≈144) reutiliza el aviso de diferencia de recepción con `vehiclePlate: null`.
- El texto, en `ReceptionDeclaredDifference.cs` (≈109), está pensado para la recepción de Bodega.
- Además, este camino no avisa los productos declarados y no contados, que el de recepción sí avisa (CHG-56).

**Decisión (cerrada).** El aviso de la corrección de Comercio Exterior tiene **su propio texto**:
- **Título:** «Diferencia con lo contado por Bodega».
- **Cuerpo:** «Depósito {N.º}, corrección de Comercio Exterior: {producto}: declarado {x}, contado por Bodega {y} (diferencia {d}). El stock quedó con lo declarado; si corresponde, ajuste la cantidad (CE-7).», con una línea por producto.
- Incluye los productos **declarados y no contados** («contado por Bodega 0»), con la misma regla de CHG-56.
- El aviso de la recepción de Bodega **no cambia**.
- Implementa el texto con un parámetro de contexto o un método aparte en `ReceptionDeclaredDifference`, sin duplicar el cálculo de diferencias.

**Pruebas.** Unitarias del texto en los dos contextos. Integración: corregir un producto contado y uno no contado → un aviso con las dos líneas y sin «camión sin placa».

---

## DEF-F11-015 (TRIVIAL): por API, un comprobante de más de 5,3 MB responde «Adjunte el comprobante del pago.»

**Causa.** `BillingController.cs` (≈315-316) limita la petición a 5.500.000 bytes (`RequestSizeLimit` y `MultipartBodyLengthLimit`). El archivo se descarta antes de que `PaymentVoucherRules` valide el tamaño, y el mensaje que sale es `MissingMessage`.

**Decisión (cerrada).**
- Sube los dos límites de **ese endpoint** a **10 MB** (constante con nombre, junto a la de 5 MB de `PaymentVoucherRules`), para que un archivo de entre 5 y 10 MB llegue a la validación y reciba **«El comprobante no puede superar 5 MB.»**.
- Por encima de 10 MB, la respuesta también debe decir «El comprobante no puede superar 5 MB.» en el formato de error del API, no el 413 genérico. Si el proyecto ya traduce el error de tamaño de Kestrel o del form, reutilízalo. Si no, captura ese caso solo en este endpoint.
- No cambies el límite de 5 MB del comprobante ni el de otros endpoints.

**Pruebas.** Integración: 72 KB → 200; 6 MB → 400 con el mensaje de tamaño; 11 MB → error con el mismo mensaje; sin archivo → «Adjunte el comprobante del pago.».

---

## Sin retrocesos (regla 4.0.10)
- **DEF-F7-007:**
  - el reporte sigue mostrando las facturas que muestra hoy;
  - no cambian los totales del depósito: la anulada no suma, y si hoy suma alguna anulada, se respeta lo que hace CHG-65;
  - el recálculo no cambia.
- **DEF-F11-012:** Borradores, Confirmados y Cerrados se editan como hoy.
- **DEF-F11-011:** los demás filtros del historial no cambian.
- **DEF-F11-013:** la edición de importación no cambia.
- **DEF-F11-014:** el aviso de recepción de Bodega no cambia.
- **DEF-F11-015:** los demás endpoints con archivos no cambian.
- Las pruebas existentes pasan sin editarlas. Si alguna supone el comportamiento viejo, detente y repórtala antes de cambiarla.

## Base de datos y entorno
- **No uses la base, el API ni el frontend locales**: tienen el dataset del re-test de QA. No los reinicies. Las pruebas de integración usan su propio PostgreSQL con Testcontainers (Docker activo).
- No se espera migración. Al terminar, `dotnet ef migrations has-pending-model-changes` no debe reportar cambios. Si algo lo exigiera, detente y repórtalo; nunca edites archivos generados ni uses SQL manual.

## Restricciones (obligatorias)
- Trabaja en `develop` de los dos repos. **No crees ramas, no hagas `git add`, commit, push ni merge**: entregas los mensajes de commit y el usuario hace los commits.
- No copies contraseñas ni secretos. No toques producción ni `infra/`.
- Textos y comentarios en español. Respeta la estructura por features.
- Nada fuera de las siete fichas. Las observaciones sin ficha del §5 del informe de S3 quedan fuera, incluido el título «Recurso duplicado.».
- Si el código real contradice este prompt, adapta a lo que hay sin cambiar el comportamiento pedido y anótalo. Si el comportamiento cambia, detente y repórtalo.

## Fichas
- En cada una de las siete fichas:
  - cambia el **Estado** a «Corregido»;
  - agrega una fila «Corregido» al Historial con la fecha, el resumen del cambio, las pruebas y «commits: pendiente».
- En `defectos/INDICE.md`, actualiza solo esos siete estados.
- No modifiques los informes de sesión ni otras fichas.

## Verificación antes de terminar
1. `dotnet build` sin errores ni advertencias nuevas.
2. `dotnet test` de `Wms.Tests` (1585 hoy) y `Wms.IntegrationTests` (254 hoy) en verde. Reporta los totales.
3. `has-pending-model-changes` sin cambios.
4. En `Frontend/wms`:
   - `yarn test` en verde;
   - `yarn build` con código 0;
   - `yarn lint` con **no más de 279 errores** y 0 en archivos nuevos. Reporta la cifra.
5. `git status` en los dos repos: solo los archivos de este alcance, más este prompt y las fichas. Si aparece `components.d.ts` regenerado, indícalo aparte.

## Entrega
Responde con:
1. Los archivos creados o modificados, agrupados por ficha. Para DEF-F11-012, la lista de endpoints auditados: cuáles ya rechazaban el anulado y cuáles recibieron la regla.
2. El resultado de cada compuerta, con números.
3. Las desviaciones del prompt y cualquier prueba existente que hayas tenido que reportar.
4. Lo que QA debe re-testear en S4 por ficha:
   - DEF-F7-007: F7-REP-022 con 2026BA00002 y 2026BA00016;
   - DEF-F11-011: F3-HIS-002 con 2026T00006, 2026T00034 y 2026T00036;
   - DEF-F11-012: detalle de 2026BA00004 y `PATCH imports/{id}/manifest`;
   - DEF-F11-013: detalle de 2026EXP00001 y 2026INSP00001;
   - DEF-F11-010: F3-MUL-002 en pantalla;
   - DEF-F11-014: corrección de productos en 2026BA00020;
   - DEF-F11-015: `POST billing/payments/vouchers` con 6 MB y con 11 MB.
5. **Los mensajes de commit**, listos para pegar, cada uno por separado:
   - **Backend:** `fix(qa-f11): reporte por CPI con la factura anulada, manifiesto de anulado bloqueado, tiquete en el historial, moneda y valor en exportación e inspección, aviso de corrección de CE y comprobante grande (DEF-F7-007, DEF-F11-011 a DEF-F11-015)`, con una línea por cambio.
   - **Frontend (código):** `fix(qa-f11): manifiesto de anulado sin «Editar», moneda y valor en el detalle y documento del depósito adicional (DEF-F11-012, DEF-F11-013, DEF-F11-010)`, con una línea por cambio.
   - **Frontend (documentación):** `docs(qa-f11): fichas DEF-F7-007 y DEF-F11-010 a DEF-F11-015 corregidas`. Este prompt puede ir en el mismo commit.
   - Todos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí.** La verificación en pantalla la hace QA en la S4, después de que el usuario reinicie el API y el frontend con estos cambios.
