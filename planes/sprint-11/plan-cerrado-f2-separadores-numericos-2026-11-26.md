# Plan cerrado — Fase 2 · Separadores numéricos «1,234.56» en la app y en los PDF

> **Fecha:** 26 de noviembre de 2026. **Estado:** Aprobado por el usuario el 2026-11-26 («Apruebo los dos planes»), con las respuestas de §9 en D12 a D16. Sin ejecutar: va después del plan de ajustes de la QA de F05 y antes del de formatos v2 de PDF (D16).
> **Origen:** el segundo hallazgo 7 de la QA manual de F05 integrado ([`qa-manual/hallazgos-int-F05.md`](qa-manual/hallazgos-int-F05.md), `H/` 7b): «Para toda la APP y PDFs: […] cambiar a "punto (.)" como separador de decimales y "coma (,)" como separador de miles». El usuario decidió el 2026-11-26 tratarlo en un plan propio (`AJQ/` D1).
> **Base:** BE `fase-2` `348ab15` · FE `fase-2` `00d15e5` · docs `main` `9c90a71`. El plan de ajustes de la QA de F05 (`AJQ/`) va antes y toca los mismos servicios PDF: al empezar, el ejecutor mide de nuevo las líneas citadas sobre `fase-2` con ese plan fusionado.
> **Alcance:** backend, frontend y docs. Cambia el formato de los números (cantidades, pesos, montos, porcentajes y tasas) que la app muestra y recibe, y el de los PDF, correos y textos que genera el backend. No cambia contratos ni datos guardados: el API sigue enviando números JSON. Sin migraciones. **Contradice la convención es-CO del hub** (`D/contexto/convenciones-tecnicas.md` §3, que viene de CHG-88, `DEF-F10-006`): propone una decisión nueva, `DEC-082` (D4).
> **Rutas:** relativas a `code_workspace/`. Prefijos: `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `FV/` = `Frontend/wms/tools/video-tutoriales/`; `D/` = `docs/`; `AJQ/` = `D/planes/sprint-11/f05-comercio-exterior/plan-cerrado-f2-f05-ajustes-qa-2026-11-26.md`; `H/` = el archivo de hallazgos.

---

## 0. Instrucciones para el ejecutor

1. **Lecturas mínimas:** los dos `AGENTS.md` de los repos, `D/procesos/flujo-de-trabajo-agentes.md`, `D/contexto/convenciones-tecnicas.md` §3, `AJQ/` D1, `H/` 7b y este plan completo.
2. **Cuándo:** después de fusionar en `fase-2` el plan de ajustes de la QA de F05 (`AJQ/`). No corre en paralelo con el plan de los formatos v2 de PDF (`D/planes/sprint-11/plan-cerrado-f2-formatos-pdf-v2-2026-11-26.md`): los dos tocan los mismos servicios PDF. Este plan va primero (D16).
3. **Ramas y git:** `f2/separadores-numericos` en BE y en FE, desde `fase-2`. Commit y push al cerrar cada fase, con el mensaje de §7. Al cerrar la fase 3, fusión en `fase-2` con `--no-ff` en los dos repos y push. Sin `push --force`. Para borrar, `rm`. `test/.nuxtrc` está sin seguimiento: no se sube.
4. **Una fase por turno** (`AGENTS.md`): al cerrar cada una, compuertas, commit, estado en este plan (§4) y en la matriz, y reporte.
5. **Líneas citadas:** son de la base. Confírmalas con grep; si el código no coincide, pregunta en un solo mensaje.
6. **Verificación:** `yarn dev` sin sesión simulada contra el API local (`dotnet run --project B/Wms.Api --launch-profile http`, puerto 5281), con Administrador, Báscula, Comercio Exterior y Facturación. Los PDF se descargan y se revisan. Capturas en `D/planes/sprint-11/evidencias-separadores/sep-*`.

---

## 1. Decisiones

### 1.1 Del usuario

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **Punto decimal y coma de miles en toda la app y en los PDF:** `1,234.56` en lugar del es-CO de hoy (`1.234,56`) | `H/` 7b |
| D2 | **Plan propio**, fuera del plan de ajustes de la QA de F05, e implementado después de él | Usuario, 2026-11-26 (`AJQ/` D1); el pedido de este plan |
| D12 | **Los Excel siguen como números.** Las celdas exportadas conservan su valor numérico y los formatos `#,##0` y `#,##0.00` (`F/utils/excel-export.ts:39-41`); Excel los muestra según la configuración regional del equipo. Sin cambio de código (P1) | Usuario, 2026-11-26 («acepto las recomendaciones») |
| D13 | **Los textos ya guardados se dejan como están.** Auditoría, observaciones y avisos con cifras generados antes del cambio no se convierten (P2) | Usuario, 2026-11-26 («acepto las recomendaciones») |
| D14 | **Videos tutoriales:** los guiones pasan al formato nuevo (D11) y solo los videos pendientes se graban con él; los publicados no se vuelven a grabar por este plan (P3) | Usuario, 2026-11-26 («acepto las recomendaciones») |
| D15 | **Campos de moneda:** la pantalla con `$ 28,560` y el `InputNumber` con `$28,560`, sin espacio (D6), son aceptables (P4) | Usuario, 2026-11-26 («acepto las recomendaciones») |
| D16 | **Orden:** este plan va antes del de formatos v2 de PDF; los dos, después del plan de ajustes de la QA de F05 y sin correr en paralelo (P5) | Usuario, 2026-11-26 («acepto las recomendaciones») |

### 1.2 Propuestas (se aprueban con el plan)

| # | Decisión | Fuente |
| --- | --- | --- |
| D3 | **Qué cambia y qué no.** <br>• **Cambia:** todo número que el sistema muestra, imprime o escribe en un texto: cantidades, pesos, montos, porcentajes, TRM y tasas. Pantallas, campos `InputNumber`, PDF (etiquetas, tarjetas, depósito, guía, tiquete de báscula, factura y reportes), correos y los textos que arma el backend (auditoría, observaciones automáticas, avisos y mensajes de error). <br>• **No cambia:** <br>  – las **fechas y horas** (`F/utils/colombia-date.ts` y los `yyyy-MM-dd` / `dd/MM/yyyy` del backend); <br>  – los **identificadores**, que no son números aunque lleven puntos: NIT (`837.000.606-1`, también el del logo), número de depósito, guía, manifiesto, levante, aceptación y placa; <br>  – la **cantidad de decimales** de cada dato (máximo 2 por omisión, como hoy); <br>  – los **símbolos de moneda** de la pantalla (`$` para COP, `US$` para USD); <br>  – los **contratos y datos**: el API envía y recibe números JSON, y el backend sigue leyendo los parámetros de fórmulas y los CSV con `InvariantCulture` (`B/Wms.Application/Billing/Calculators/*`, `B/Wms.Application/Administration/LegacyImport/Common/LegacyValueParsers.cs:37`), que ya usa el punto decimal. <br>• Los Excel y los textos ya guardados: D12 y D13 | D1 |
| D4 | **Decisión nueva del hub: `DEC-082 — Formato numérico 1,234.56`.** Se agrega a `D/contexto/decisiones.md` (§9) en la fase 3: <br>«**DEC-082 — Formato numérico** (2026-11-26, QA manual de F05). Todo número que el sistema muestra, imprime o escribe lleva punto decimal y coma de miles (`1,234.56`). Las fechas, los identificadores (NIT, números de documento) y los símbolos de moneda no cambian. Reemplaza el formato es-CO de números de CHG-88 (`DEF-F10-006`) y la regla `<InputNumber locale="es-CO">` de `convenciones-tecnicas.md` §3. Fuente: el usuario, hallazgo 7 de `planes/sprint-11/qa-manual/hallazgos-int-F05.md`.» <br>`D/contexto/convenciones-tecnicas.md` §3 cambia la línea de números y de `InputNumber` según D5 a D7 | D1; `D/README.md` («Al cerrar un trabajo») |
| D5 | **Frontend: una sola utilidad, con los símbolos de hoy.** <br>• **Hoy:** `F/shared/utils/format.ts:1` fija `LOCALE = 'es-CO'` y formatea con `Intl.NumberFormat` (`:20`, `:49`, `:56`). <br>• **Cambio:** se conserva `es-CO` para el patrón y el símbolo, y se cambian los separadores con `formatToParts` (`group` → `,`, `decimal` → `.`), en un helper privado del mismo archivo. Resultado: `formatNumber(1234567.5)` = `1,234,567.5`; `formatKg(303000)` = `303,000 kg`; `formatCurrency(28560, "COP")` = `$ 28,560`; `formatCurrency(1234.5, "USD")` = `US$ 1,234.50`. <br>• **Por qué no otro locale:** con `es-MX`, `es-419` o `en-US` el COP sale como `COP 28,560` y el USD como `USD` o `$`, con lo que cambiarían los símbolos (D3). <br>• **Comentarios:** los JSDoc de `format.ts:5-7`, `:29`, `:34`, `:40-42` y `F/composables/useQuantityFormatter.ts:5` pasan a `DEC-082`. `F/utils/colombia-date.ts` no cambia | D1, D3 |
| D6 | **Campos `InputNumber`: `locale="en-US"`.** <br>• **Hoy:** 78 etiquetas en 47 archivos con `locale="es-CO"`, exigido por la guardia (`FT/unit/guards/source-guards.spec.ts:73-80`). <br>• **Cambio:** `locale="en-US"` en todas: PrimeVue formatea y lee con el locale, así que el operario escribe `1234.5` y ve `1,234.5`. <br>• **Moneda:** las 11 con `mode="currency"` (todas en COP; p. ej. `F/features/warehouse/components/ForkliftChargeDialog.vue:173-174`, `F/features/services/components/ServiceMinimumValuesCard.vue:83-84`, `F/features/forklift-rates/components/ForkliftRatesGrid.vue:113`) suman `currency-display="narrowSymbol"`, para ver `$28,560` y no `COP 28,560`. El campo no deja el espacio después de `$` que sí deja la pantalla (D5): es como lo pinta `Intl`, y se acepta (D15). <br>• **Marcadores de ejemplo:** `F/features/warehouse/components/ForkliftStartDialog.vue:209` (`1.234,5` → `1,234.5`), `F/features/billing/components/ManualTrmDialog.vue:112` (`Ej: 4.000,00` → `Ej: 4,000.00`) y `F/features/foreign-trade/components/ReleaseEditableRow.vue:300` (`0,00` → `0.00`). `F/features/foreign-trade/components/LoadingOrderForm.vue:868` y `:891` ya dicen `0.00` | D1 |
| D7 | **Guardias del frontend** (`FT/unit/guards/source-guards.spec.ts`). <br>• El bloque «formato único es-CO (CHG-88)» (`:6` y `:50`) pasa a «formato numérico 1,234.56 (DEC-082)». <br>• «todo `<InputNumber>` declara `locale="es-CO"`» (`:73`) pasa a `locale="en-US"`. <br>• Nueva: todo `<InputNumber>` con `mode="currency"` declara `currency-display="narrowSymbol"`. <br>• Se conservan: sin `toLocale*`, sin `es-ES`, sin `new Intl.NumberFormat` ni `DateTimeFormat` fuera de `format.ts` y `colombia-date.ts` (`:11`, `:51-71`). <br>• Las guardias son reglas del proyecto: se cambian solo porque `DEC-082` cambia la regla | D4 |
| D8 | **Backend: una sola cultura numérica.** <br>• **Hoy:** 19 archivos crean su propia `CultureInfo("es-CO")` (lista en §3), entre ellos `B/Wms.Application/Common/Formatting/QuantityDisplay.cs:13`, `B/Wms.Application/Billing/Common/Services/InvoicePdfService.cs:20`, `B/Wms.Application/Weighbridge/Common/Services/WeighbridgeTicketPdfService.cs:246` y tres del dominio (`B/Wms.Domain/Entities/Warehouse/ForkliftUse.cs:50`, `B/Wms.Domain/Entities/Warehouse/NoveltyQuantityRules.cs:12`, `B/Wms.Domain/Services/EntryCorrectionRules.cs:150`). <br>• **Cambio:** `B/Wms.Common/Formatting/WmsCulture.cs` (nuevo; `Wms.Common` lo referencian el dominio y la aplicación) expone `WmsCulture.Instance`: un clon de solo lectura de `es-CO` con `NumberDecimalSeparator`, `CurrencyDecimalSeparator` y `PercentDecimalSeparator` = `.`, y los separadores de grupo = `,`. Conserva el símbolo `$` y los formatos de fecha de es-CO. Los 19 archivos usan `WmsCulture.Instance`; los que también formatean fechas con esa cultura no cambian su salida de fechas | D1, D3 |
| D9 | **Formatos que hoy dependen de la cultura del servidor.** <br>• **Hoy:** estos textos no pasan cultura y salen con la del proceso (la del Mac en local y la invariante en el contenedor de staging, que ya da `1,234.56`): <br>  – `ToString("0.##")` de `B/Wms.Application/ForeignTrade/Common/Services/DepositPdfService.cs:539`, `DispatchGuidePdfService.cs:902` y `B/Wms.Application/Warehouse/Common/Services/WarehouseMovementsPdfService.cs:416`; <br>  – las interpolaciones `:N2` de `B/Wms.Application/Billing/Common/Services/StorageBillingService.cs:264`, `:286` y `:386`, `B/Wms.Application/Billing/EventHandlers/WeeklyExchangeRateChangedHandler.cs:43`, `B/Wms.Application/Warehouse/Commands/AdjustInventory/AdjustInventoryCommandHandler.cs:159` y `:262-266`, `B/Wms.Application/Warehouse/Commands/Reception/ReceptionDeclaredDifference.cs:52` y `:123`, `B/Wms.Application/Weighbridge/Commands/ModifyFirstWeight/ModifyFirstWeightHandler.cs:94`, `ModifySecondWeight/ModifySecondWeightHandler.cs:118` y `B/Wms.Infrastructure/Services/NotificationService.cs:108-116`, `:383-387` y `:482-486`. <br>• **Cambio:** pasan `WmsCulture.Instance` de forma explícita (`ToString(formato, WmsCulture.Instance)` o `string.Create(WmsCulture.Instance, $"…")`). Así el texto es el mismo en local y en staging. <br>• **Sin cambio:** las plantillas de `ILogger` (`B/Wms.Application/Billing/Jobs/BillingJobService.cs:56` y `:90`), que no ve el usuario, y los `Guid.ToString("N")`. <br>• **No se cambia la cultura por omisión del proceso** (`CultureInfo.DefaultThreadCurrentCulture`): alteraría los `Parse` sin cultura que pudiera haber. La guardia de D10 cubre lo nuevo | D1 |
| D10 | **Guardia del backend** (nueva, `B/Wms.Tests/Common/NumberCultureGuardTests.cs`): recorre los `.cs` de `Wms.Domain`, `Wms.Application`, `Wms.Infrastructure` y `Wms.Api` (sin `Migrations`) y falla si aparece `"es-CO"` fuera de `WmsCulture.cs`, o un `ToString("0.##")` / `ToString("#,##0…")` sin segundo argumento. Es la misma idea que las guardias del frontend | D8, D9 |
| D11 | **Guiones de los video tutoriales.** `D/videos/guiones/guiones-video-tutoriales.md` (48 cifras con el formato viejo), `dataset-grabacion.md` (25) y `plan-produccion-videos.md` (6) pasan las cifras que el grabador escribe o la narración lee a `1,234.56` (p. ej. «0,295 %» → «0.295 %», «$16.806,72» → «$16,806.72»). `FV/` lee los valores de esos guiones: se revisa que `FV/siembra/` y `FV/grabador/` no armen cifras con el formato viejo (hoy hay números en `FV/siembra/archivos.mjs`, `datos.mjs` y `piloto.mjs`, y en `FV/grabador/voz-azure.mjs`). Los manuales del hub no tienen cifras afectadas; `D/manuales/nota-operarios-hallazgos-2026-10-26.md` es una nota fechada y no se toca. Los videos ya grabados: D14 | D1 |

---

## 2. Contrato

Ningún contrato cambia: el API envía y recibe números JSON, sin formato. Los PDF cambian solo en su texto.

---

## 3. Archivos que se tocan

**Backend**

- `B/Wms.Common/Formatting/WmsCulture.cs` (nuevo, D8).
- Los 19 con `"es-CO"` (D8): `B/Wms.Application/Billing/Common/Services/InvoiceCancellationPolicy.cs:19`, `InvoicePdfService.cs:20`, `StorageInvoiceDetailFormatter.cs:8`, `StorageMinimumCharge.cs:13`; `B/Wms.Application/Billing/Jobs/DueNoticeMessage.cs:13`; `B/Wms.Application/Billing/Queries/PreviewFormula/PreviewFormulaHandler.cs:124`, `:162` y `:165`; `B/Wms.Application/Common/Formatting/QuantityDisplay.cs:13`; `B/Wms.Application/ForeignTrade/Common/Services/DepositCancellationNotices.cs:21`; `B/Wms.Application/Reports/NationalizedInventory/NationalizedInventoryPdfService.cs:27`; `B/Wms.Application/Warehouse/Common/Services/DailyIncomingGoodsPdfService.cs:14`, `DailyOutgoingGoodsPdfService.cs:16`, `WarehouseMovementsPdfService.cs:24`; `B/Wms.Application/Weighbridge/Common/Services/DailyBillingPdfService.cs:18`, `SharedNetSplit.cs:13`, `TicketSections.cs:90`, `WeighbridgeTicketPdfService.cs:246`; y los tres del dominio de D8.
- Los de D9.
- Pruebas: `B/Wms.Tests/Common/NumberCultureGuardTests.cs` (nueva) y las 21 que esperan textos es-CO: en `Wms.Tests`, `Administration/LegacyCsvReaderTests.cs` (revisar: lee con invariante, puede no cambiar), `Billing/Calculators/PerCargoUnitFormulaCalculatorTests.cs`, `Billing/Services/StorageFallbackWarningTests.cs`, `Billing/Services/StorageMissingCargoValueWarningTests.cs`, `Billing/StorageMinimumChargeTests.cs`, `Common/AuditContextTests.cs`, `Common/QuantityDisplayTests.cs`, `Domain/Warehouse/NoveltyQuantityRulesTests.cs`, `Exits/ExitAvailabilityTests.cs`, `ForeignTrade/GuideLoadMismatchTests.cs`, `Notifications/NotificationEmailFormatTests.cs`, `Warehouse/ReceptionDifferenceNoticeTests.cs`, `Weighbridge/TicketSectionsTests.cs`, `Weighbridge/WeighingPairRulesTests.cs`, `Weighbridge/WeighingProposedTotalTests.cs`; en `Wms.IntegrationTests`, `Billing/MigratedStorageBillingTests.cs`, `Billing/OverdueJobTests.cs`, `Billing/OverrideLineTotalTests.cs`, `Billing/StorageLinkedServiceFallbackTests.cs`, `Billing/StorageMinimumVatTests.cs` y `Weighbridge/PendingBillingRoundedTotalTests.cs`.

**Frontend**

- `F/shared/utils/format.ts` (D5) y `F/composables/useQuantityFormatter.ts:5` (comentario).
- Las 78 etiquetas `<InputNumber>` de 47 archivos (D6; lista con `grep -rln 'locale="es-CO"' app`), y los tres marcadores de D6.
- `FT/unit/guards/source-guards.spec.ts` (D7) y `FT/unit/utils/format.spec.ts`.
- Las 21 pruebas que esperan cifras es-CO: `FT/unit/weighbridge/` (`weighing-rules`, `entry-detail`, `charge-step`, `queue-display`, `ticket-print`), `FT/unit/warehouse/` (`forklift-mocks`, `forklift-charge`), `FT/unit/billing/` (`payment-actions`, `payment-invoice-label`), `FT/components/weighbridge/` (`WeighbridgeEntryDetail`, `WeighbridgeTicketStep`, `ServiceCorrectionDialog`, `WeighbridgeReweighStep`, `WeighbridgeQueuePanel`, `WeighbridgeQueuePage`), `FT/components/foreign-trade/` (`EntryEditForm`, `DepositReleasesStage`), `FT/components/services/ServicePricesList`, `FT/components/billing/` (`BillingCollectForm`, `OverrideAmountDialog`) y `FT/unit/utils/format.spec.ts`.
- `FV/` solo si arma cifras con el formato viejo (D11).

**Sin cambio:** `F/utils/excel-export.ts` (`:39-41`, formatos `#,##0` y `#,##0.00` de celdas numéricas; D12), `F/utils/colombia-date.ts`, `nuxt.config.ts` (el `locale` de PrimeVue solo tiene textos).

**Docs:** este plan, `D/contexto/decisiones.md` (`DEC-082`), `D/contexto/convenciones-tecnicas.md` §3, `D/contexto/estado.md`, los guiones de D11, `D/planes/README.md`, la matriz y los casos en `D/qa/`.

---

## 4. Fases

| Fase | Repo | Contenido | Cierre | Estado |
| --- | --- | --- | --- | --- |
| 1 | BE | D8 a D10: `WmsCulture`, los 19 archivos, los formatos de D9, la guardia y las pruebas | Compuertas BE; QA-SEP-001 a 006 en PASA (PDF descargados y textos generados) | Pendiente |
| 2 | FE | D5 a D7: utilidad, `InputNumber`, marcadores, guardias y pruebas | Compuertas FE; QA-SEP-007 a 012 en PASA en el navegador | Pendiente |
| 3 | docs (y `FV/` si hace falta) | D4 y D11: `DEC-082`, convenciones, estado, guiones; casos a `D/qa/`; fusión de `f2/separadores-numericos` en `fase-2` en los dos repos | QA-SEP-013 en PASA; fusiones con push | Pendiente |

---

## 5. Pruebas y casos QA

**Backend:**

- `WmsCultureTests`: `1234567.5m.ToString("N2", WmsCulture.Instance)` = `1,234,567.50`; `28560m.ToString("C0", …)` = `$ 28,560` (o el patrón de es-CO con esos separadores); una fecha con `dd/MM/yyyy` y `MMMM` sale igual que con es-CO.
- `QuantityDisplayTests`, `TicketSectionsTests` y las demás de §3 con las cifras nuevas.
- `NumberCultureGuardTests` (D10).

**Frontend (Vitest):**

- `format.spec`: `formatNumber`, `formatKg` y `formatCurrency` (COP, USD, moneda desconocida, nulos y `maximumFractionDigits`).
- Guardias de D7.
- Las pruebas de §3 con las cifras nuevas.

**Casos QA** (API local, navegador y PDF descargados):

| Caso | Pasos | Resultado esperado |
| --- | --- | --- |
| QA-SEP-001 | Tiquete de báscula de un ingreso de 32.023 kg | `32,023 kg` en todos los pesos |
| QA-SEP-002 | Etiqueta, tarjeta por vehículo, PDF del depósito y guía de salida del depósito de la QA de F05 (`5f3749d2-…`) | Cantidades con decimales como `640.13`; miles como `1,920`; NIT, números de depósito, manifiesto y levantes sin cambio; fechas sin cambio |
| QA-SEP-003 | PDF de una factura en COP y de una en USD | Montos `28,560` y `1,234.50`; IVA y totales con el mismo formato |
| QA-SEP-004 | Reportes PDF: diario de ingresos, diario de salidas, movimientos, inventario nacionalizado y facturación diaria de báscula | Cifras `1,234.56` |
| QA-SEP-005 | Modificar el primer peso de un ciclo (Báscula) y ver la auditoría | «Peso original: 32,000.00 kg, Nuevo peso: …» |
| QA-SEP-006 | Vista previa de una fórmula de facturación | Montos y kilos con el formato nuevo |
| QA-SEP-007 | Báscula: cola, registro y detalle de un ingreso | Pesos `32,023`; el campo de peso acepta `32023.5` y muestra `32,023.5` |
| QA-SEP-008 | Comercio Exterior: detalle del depósito, etapa Levantes | Ampara `640.13` y saldo `1,279.87`; la fila editable acepta `100.25` |
| QA-SEP-009 | Facturación: cobro y factura en COP; TRM manual | Pantalla `$ 28,560` y `US$ 1,234.50`; el campo de moneda muestra `$28,560`; la TRM acepta `4000.50` |
| QA-SEP-010 | Montacargas: inicio con peso y cobro | Marcador `1,234.5`; el cobro en `$` con coma de miles |
| QA-SEP-011 | Configuración › Parámetros: un parámetro numérico | Valor con el formato nuevo |
| QA-SEP-012 | En un equipo Windows con configuración regional de Colombia, escribir un decimal con la tecla «.» del teclado numérico en un campo de peso | Queda como separador decimal. Si la tecla escribe `,` y el campo la ignora o la toma como miles, es un defecto bloqueante de la fase (R1) |
| QA-SEP-013 | Exportar a Excel una lista con pesos y montos | Celdas numéricas (se pueden sumar); el formato visible lo pone Excel según la configuración regional del equipo (D12) |

---

## 6. Compuertas de cada fase

- **BE (fase 1):** `dotnet build Wms.sln` sin errores; `dotnet test Wms.Tests` y `dotnet test Wms.IntegrationTests` en verde (bases medidas en `fase-2` al empezar, con el plan de ajustes de F05 fusionado); `dotnet ef migrations has-pending-model-changes` limpio.
- **FE (fase 2):** `yarn build` con código 0; `yarn test` en verde (base medida al empezar); `yarn lint` sin subir la base y sin errores en archivos tocados; las guardias de `FT/unit/guards/` en verde; `grep -rn 'locale="es-CO"' app` vacío.
- PDF y capturas de los casos de la fase.

---

## 7. Commits

| Fase | Repo | Mensaje |
| --- | --- | --- |
| 1 | BE | `feat(formato): separadores 1,234.56 en PDF, correos y textos del backend (DEC-082)` |
| 2 | FE | `feat(formato): separadores 1,234.56 en pantallas y campos numéricos (DEC-082)` |
| 3 | docs | `docs(formato): DEC-082, convenciones y guiones con separadores 1,234.56` |

Fusiones: `f2/separadores-numericos` en `fase-2`, con `--no-ff`, en BE y en FE, al cerrar la fase 3.

---

## 8. Riesgos

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R1 | Los operarios están acostumbrados a la coma decimal: escriben `1,5` y el campo lo toma como `15`, o la tecla decimal del teclado numérico (que en Windows con región Colombia escribe `,`) deja de servir | QA-SEP-012 en un equipo Windows real; aviso a los operarios con la salida a staging. Si la tecla no sirve, se corrige en la fase 2 antes de cerrarla |
| R2 | Textos guardados con el formato viejo (auditoría, observaciones, avisos) conviven con los nuevos | D13: son históricos y no se convierten |
| R3 | Queda algún número fuera de las utilidades y sale con el formato viejo | Guardias de D7 y D10; grep de `es-CO` en los dos repos al cerrar |
| R4 | Cambiar 21 + 21 pruebas oculta una regresión real | Solo cambian las cifras esperadas, no la lógica; el diff de pruebas se revisa línea a línea |
| R5 | Los videos ya grabados muestran el formato viejo | D14: los pendientes se graban con el formato nuevo; los publicados no se vuelven a grabar por este plan |
| R6 | El plan de ajustes de F05 o el de formatos v2 mueven líneas de los PDF | Se miden de nuevo al empezar (§0.5); los formatos v2 usan `QuantityDisplay` y `WmsCulture`, así que heredan este cambio sea cual sea el orden |

---

## 9. Preguntas pendientes

Ninguna. P1 a P5 se respondieron el 2026-11-26 con las recomendaciones («acepto las recomendaciones»): D12 a D16 (§1.1).
