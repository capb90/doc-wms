Eres el implementador de la corrección de **DEF-F11-018 (MAJOR)** y **DEF-F11-019 (MINOR)**, las dos fichas que quedan abiertas en el informe final del QA del WMS de Bodegas Asociadas (`docs/qa/resultados/informe-final.md`, §7, condición 3). Modelo recomendado: **Sonnet 5.5** (complejidad media-baja: un reporte del backend y un componente del frontend). Todo lo anterior está corregido y con commit. **La base local tiene el dataset del QA: no la toques.**

Implementa en este orden: **DEF-F11-018 → DEF-F11-019**.

## Lee primero
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. `docs/qa/plan-correccion-defectos.md`:
   - la sección «4.0 Reglas comunes» (4.0.2 migraciones, 4.0.4 lint, 4.0.10 «Sin retrocesos funcionales»);
   - las tarjetas **CHG-34, CHG-76, CHG-84 y CHG-88**.
3. Las fichas `docs/qa/resultados/defectos/DEF-F11-018.md` y `DEF-F11-019.md`, con sus evidencias en `evidencias/F11/S5-B-*`.
4. `docs/qa/resultados/F11-informe-S5-2026-10-06.md` (casos F3-RPT-001 y F3-CIC-001).

---

## DEF-F11-018 (MAJOR): el reporte diario de báscula omite cobros, imprime la hora en UTC y pone «Cliente N/A»

**Causa (confirmada en el código).**
- `Wms.Application/Weighbridge/Queries/GetDailyBillingReport/GetDailyBillingReportHandler.cs` arma **una fila por ciclo** con `wc.WarehouseStorageEntries.FirstOrDefault(...)`. En un camión multidepósito se queda con una sola entrada (en el caso de QA, la del depósito adicional en $0) y pierde la factura del depósito principal: faltaron 29.750 en el total del día.
- `CustomerName = invoice?.Customer?.Name ?? "N/A"` (y `CustomerIdNumber`) ignoran al destinatario no registrado y al Consumidor final.
- `Wms.Application/Weighbridge/Common/Services/DailyBillingPdfService.cs`:
  - la línea ≈126 imprime `item.CreatedAt.ToString("HH:mm")` sin pasar a la hora de Colombia;
  - la línea ≈45 usa `DateTime.Now` para «Generado».

**Decisión (cerrada).**
1. **Una fila por tiquete.**
   - Un ciclo **con entradas de depósito** da una fila por cada entrada del ciclo (`e.WeighbridgeCycleId == wc.Id`), con su propio tiquete, su factura (`WeighbridgeInvoice`), su peso neto (`PhysicalNetWeight`) y su producto.
   - Un ciclo **sin entradas** (Solo báscula y Salida) da una fila, como hoy, con el tiquete y la factura del ciclo.
   - La placa, el conductor, los pesos y el estado son los del ciclo en cada fila.
   - La factura en cero del depósito adicional aparece como su propia fila, en $0.
2. **Totales.**
   - `TOTAL FACTURADO`, el subtotal y el IVA suman **cada factura una sola vez**, deduplicadas por Id. Así una factura compartida por varias entradas no se cuenta dos veces.
   - El total debe coincidir con la suma de las facturas de báscula de los ciclos del día.
   - Los **conteos por tipo** (Ingreso, Salida, Solo pesaje) y el de completos siguen **por ciclo**, como pide CHG-76: Ingreso + Salida + Solo pesaje = número de ciclos.
   - El peso neto total no cambia: ya suma todas las entradas.
3. **Destinatario.** Cliente y documento salen de la factura con las reglas de destinatario que ya existen en el dominio (`Invoice.ResolveRecipientName()` y su equivalente para el documento): cliente registrado, persona no registrada o «Consumidor final». Sin factura, se conserva el «N/A» de hoy.
4. **Hora de Colombia.**
   - La columna «Hora» y «Generado» del PDF usan `ColombiaTime`, como CHG-84 en los demás PDF.
   - Si la pantalla o un Excel del reporte diario muestran la hora, deben usar las utilidades de CHG-88 (`formatColombiaTime` o equivalente). Revísalo y corrígelo si hace falta.
5. **Fuera de alcance:**
   - el diseño del PDF (columnas, encabezado, pie con los datos de empresa de CHG-84);
   - el filtro de fechas por día de Colombia, que ya está bien;
   - los demás reportes.

**Pruebas.**
- **Unitarias o de integración del handler:**
  - ciclo multidepósito con cobro en el principal y factura en cero en el adicional → dos filas, una por tiquete, y el total incluye el cobro del principal;
  - ciclo de Solo báscula → una fila;
  - una factura compartida por dos entradas → se cuenta una vez;
  - conteos por tipo = ciclos del día;
  - cobro a Consumidor final y a persona no registrada → nombre y documento correctos.
- **PDF:** la hora impresa de un ciclo creado a las 15:56 UTC es 10:56. Usa el método de comparación de PDF que ya se haya usado en el proyecto, por ejemplo una prueba que lo descargue y `pdftotext -layout`, o prueba la función que formatea la hora.
- **Regresión:** las pruebas existentes del reporte diario y de CHG-76 pasan sin editarlas. Si alguna supone una fila por ciclo, **detente y repórtala** antes de cambiarla.

---

## DEF-F11-019 (MINOR): el detalle del ciclo muestra «Abierto» en todo depósito y su filtro por estado no funciona

**Causa (confirmada en el código).**
- `app/features/weighbridge/components/WeighbridgeCycleTickets.vue` lee `data.status` / `e.status` en `mapStatusToDisplay`, en el filtro (`filteredEntries`), en `entrySeverity` y en la columna de estado.
- El API envía ese campo nulo y el estado está en `warehouseStorageStatus`, que el tipo `weighbridge-cycle.ts` ya declara. Con nulo, la función cae en «Abierto».

**Cambios.**
- El componente usa **`warehouseStorageStatus`** en los cuatro puntos.
- El tipo de la entrada deja de declarar `status` si el API no lo envía nunca. Busca otros usos de `entry.status` en el frontend antes de quitarlo y lista los que encuentres.
- `mapStatusToDisplay` conserva su mapeo: Borrador o Confirmado → «Abierto», Cerrado → «Cerrado», Anulado → «Anulado».
- **Sin estado**, la etiqueta es «—» y el estado no cuenta para ningún filtro salvo «Todos». No uses «Abierto» como valor por defecto.
- **No cambies el API.**

**Pruebas.** Vitest del componente:
- entradas Confirmado, Cerrado y Anulado → etiquetas correctas;
- el filtro «Cerrado» muestra solo la cerrada;
- sin estado → «—».

---

## Sin retrocesos (regla 4.0.10)
- **DEF-F11-018:**
  - un día sin camiones multidepósito da las mismas filas y el mismo total que hoy;
  - los conteos por tipo no cambian;
  - el PDF conserva su formato legacy (CHG-84).
- **DEF-F11-019:** el resto del detalle del ciclo (facturas, pesos, «Modificar pesaje», reimpresión) no cambia.

## Base de datos y entorno
- **No uses la base, el API ni el frontend locales** y no los reinicies. Las pruebas de integración usan su propio PostgreSQL con Testcontainers (Docker activo).
- No se espera migración. Al terminar, `dotnet ef migrations has-pending-model-changes` no debe reportar cambios.

## Restricciones (obligatorias)
- Trabaja en `develop` de los dos repos. **No crees ramas, no hagas `git add`, commit, push ni merge**: entregas los mensajes de commit y el usuario hace los commits.
- No copies contraseñas ni secretos. No toques producción ni `infra/`.
- Textos y comentarios en español. Respeta la estructura por features.
- Nada fuera de estas dos fichas. Las observaciones de backlog del informe final quedan fuera.
- Si el código real contradice este prompt, adapta a lo que hay sin cambiar el comportamiento pedido y anótalo. Si el comportamiento cambia, detente y repórtalo.

## Fichas
- En `DEF-F11-018.md` y `DEF-F11-019.md`:
  - cambia el **Estado** a «Corregido»;
  - agrega una fila «Corregido» al Historial con la fecha, el resumen, las pruebas y «commits: pendiente».
- En `defectos/INDICE.md`, actualiza solo esos dos estados.
- No modifiques el informe final ni los informes de sesión.

## Verificación antes de terminar
1. `dotnet build` sin errores ni advertencias nuevas.
2. `dotnet test` de `Wms.Tests` y `Wms.IntegrationTests` en verde (1634 y 278 antes de la S5). Reporta los totales.
3. `has-pending-model-changes` sin cambios.
4. En `Frontend/wms`:
   - `yarn test` en verde;
   - `yarn build` con código 0;
   - `yarn lint` con **no más de 279 errores** y 0 en archivos nuevos.
5. `git status` en los dos repos: solo los archivos de este alcance, más este prompt y las fichas.

## Entrega
Responde con:
1. Los archivos creados o modificados, por ficha. Para DEF-F11-019, incluye los usos de `entry.status` que encontraste.
2. El resultado de cada compuerta, con números.
3. Para DEF-F11-018, el total del reporte en el escenario de prueba antes y después de la corrección.
4. Las desviaciones y cualquier prueba existente que hayas tenido que reportar.
5. Lo que QA debe re-testear en local:
   - **F3-RPT-001:** reporte del 06/10 con el ciclo multidepósito de QAK402 (2026BA00021 y su adicional), los cobros a Consumidor final (2026T00061) y a persona no registrada (2026T00044), y la hora de 2026T00050 y 2026T00061.
   - **F3-CIC-001:** detalle del ciclo de 2026T00050 y el filtro «Cerrado».
6. **Los mensajes de commit**, listos para pegar, cada uno por separado:
   - **Backend:** `fix(qa-f11): reporte diario de báscula por tiquete, con destinatario y hora de Colombia (DEF-F11-018)`, con una línea por cambio.
   - **Frontend (código):** `fix(qa-f11): estado del depósito en el detalle del ciclo de báscula (DEF-F11-019)`, con una línea por cambio. Si tocaste la pantalla del reporte diario por DEF-F11-018, inclúyela aquí.
   - **Frontend (documentación):** `docs(qa-f11): fichas DEF-F11-018 y DEF-F11-019 corregidas`. Este prompt puede ir en el mismo commit.
   - Todos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí.** El re-test y la actualización del informe final los hace QA, después de que el usuario reinicie el API y el frontend.
