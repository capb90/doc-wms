# Plan cerrado — Fase 2 · Formato numérico es-CO único en la app y en los PDF

> **Fecha:** 26 de noviembre de 2026. **Estado:** Borrador, pendiente de la aprobación del usuario. **Reabierto el 2026-11-26:** la primera versión (aprobada ese mismo día, commit docs `37e29ba`) cambiaba la app a `1,234.56`; el usuario la reabrió tras revisar el legacy: «El estandar debe ser el es-CO, y separar los decimales con (,). Por constumbre se suele utiliza el (.) como separador decimal pero no es un estandar». Esta versión la reemplaza entera. Tiene preguntas abiertas (§9).
> **Origen:** el segundo hallazgo 7 de la QA manual de F05 integrado ([`qa-manual/hallazgos-int-F05.md`](qa-manual/hallazgos-int-F05.md), `H/` 7b), que pedía `1,234.56`, y el análisis del formato numérico del legacy que hizo el usuario el 2026-11-26 (resumen en D2).
> **Base:** BE `fase-2` `348ab15` · FE `fase-2` `00d15e5` · docs `main` `5521f75`. El plan de ajustes de la QA de F05 (`AJQ/`) va antes y toca los mismos servicios PDF (su fase 2, BE `7733035`): al empezar, el ejecutor mide de nuevo las líneas citadas sobre `fase-2` con ese plan fusionado.
> **Alcance:** backend, frontend y docs, acotado. La app **ya** usa es-CO en pantallas y campos (CHG-88, `D/contexto/convenciones-tecnicas.md` §3) y eso no cambia. El plan arregla lo que se sale de esa regla: los textos del backend que dependen de la cultura del servidor (en staging salen con punto decimal) y los campos numéricos que ignoran el punto que el operario trae del legacy. Sin cambios de contrato ni migraciones. Registra la decisión del usuario en `DEC-082` (D9).
> **Rutas:** relativas a `code_workspace/`. Prefijos: `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`; `AJQ/` = `D/planes/sprint-11/f05-comercio-exterior/plan-cerrado-f2-f05-ajustes-qa-2026-11-26.md`; `H/` = el archivo de hallazgos; `L/` = `bodegas-legacy/`.

---

## 0. Instrucciones para el ejecutor

1. **Lecturas mínimas:** los dos `AGENTS.md` de los repos, `D/procesos/flujo-de-trabajo-agentes.md`, `D/contexto/convenciones-tecnicas.md` §3, `AJQ/` D1, `H/` 7b y este plan completo.
2. **Cuándo:** después de fusionar en `fase-2` el plan de ajustes de la QA de F05 y antes del plan de formatos v2 de PDF (`D/planes/sprint-11/plan-cerrado-f2-formatos-pdf-v2-2026-11-26.md`, su D26), sin correr en paralelo con él: los dos tocan los mismos servicios PDF.
3. **Ramas y git:** `f2/formato-numerico` en BE y en FE, desde `fase-2`. Commit y push al cerrar cada fase, con el mensaje de §7. Al cerrar la fase 3, fusión en `fase-2` con `--no-ff` en los dos repos y push. Sin `push --force`. Para borrar, `rm`. `test/.nuxtrc` está sin seguimiento: no se sube.
4. **Una fase por turno** (`AGENTS.md`): al cerrar cada una, compuertas, commit, estado en este plan (§4) y en la matriz, y reporte.
5. **Líneas citadas:** son de la base. Confírmalas con grep; si el código no coincide, pregunta en un solo mensaje.
6. **Verificación:** `yarn dev` sin sesión simulada contra el API local (`dotnet run --project B/Wms.Api --launch-profile http`, puerto 5281), con Administrador, Báscula, Comercio Exterior y Facturación. Para los textos del backend, el API se arranca además con la cultura invariante (`DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1` o `LANG=C`), como corre en el contenedor de staging. Capturas y PDF en `D/planes/sprint-11/evidencias-formato-numerico/fn-*`.

---

## 1. Decisiones

### 1.1 Del usuario

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **El estándar es es-CO:** coma decimal y punto de miles (`1.234,56`) en toda la app, los PDF, los correos y los textos del sistema. El hallazgo `H/` 7b (`1,234.56`) se resuelve **sin cambiar** el formato: el punto decimal es una costumbre, no el estándar | Usuario, 2026-11-26 («El estandar debe ser el es-CO, y separar los decimales con (,)…») |
| D2 | **Lo que hace el legacy** (análisis del usuario, 2026-11-26): <br>• guarda los números como `DECIMAL`/`INT` con punto decimal; el operario escribe con punto (p. ej. `L/modulos/mod_levantes/registrarlevante.php:252`, `toFixed(2)`); <br>• no configura un locale numérico; formatea a mano con `number_format()` en unos 41 puntos, siempre con punto de miles y coma decimal (COP sin decimales; USD, CIF y tarifas con 2; kardex y totales de levantes con espacio de miles); <br>• unos 139 `echo` muestran el valor crudo de MySQL (p. ej. `12500.00` en los pesos de báscula, `L/modulos/mod_bascula/listarentradas.php:450`). <br>**No se copian sus inconsistencias:** el mismo dato con 0 o 2 decimales según la pantalla, el espacio como separador de miles, las unidades pegadas como texto libre y los valores sin formato. En la v2 todo número sale con la regla de D5 | Usuario, 2026-11-26 |
| D3 | **Los Excel siguen como números.** Las celdas conservan su valor y los formatos `#,##0` y `#,##0.00` (`F/utils/excel-export.ts:39-41`); Excel los muestra según la configuración regional del equipo | Usuario, 2026-11-26 (P1 de la primera versión) |
| D4 | **Orden:** este plan va después del plan de ajustes de la QA de F05 y antes del de formatos v2 de PDF, sin correr en paralelo | Usuario, 2026-11-26 (P5 de la primera versión; D26 del plan de formatos v2) |

### 1.2 Propuestas (se aprueban con el plan)

| # | Decisión | Fuente |
| --- | --- | --- |
| D5 | **Regla de decimales: la de hoy** (P2). <br>• **Montos en COP:** sin decimales (`$ 28.560`; `F/shared/utils/format.ts:44-53`). <br>• **Montos en otras monedas** (USD, FOB, CIF) y tarifas con centavos: siempre 2 decimales (`US$ 1.234,50`). <br>• **Pesos (kg), cantidades, porcentajes y TRM:** hasta 2 decimales, sin ceros de relleno (`12.000`, `640,13`, `0,295`; `format.ts:16`, `formatNumber` y `formatKg`). <br>• Un dato que pida otra precisión la declara al llamar a la utilidad (`minimumFractionDigits` / `maximumFractionDigits`), como hoy. <br>• **Backend:** este plan no cambia la cantidad de decimales de los textos que ya arma (p. ej. los `:N2` de la auditoría); solo fija la cultura (D6, D7) | P2; D1, D2 |
| D6 | **Backend: una sola cultura numérica es-CO.** <br>• **Hoy:** 19 archivos crean su propia `CultureInfo("es-CO")` (lista en §3), entre ellos `B/Wms.Application/Common/Formatting/QuantityDisplay.cs:13`, `B/Wms.Application/Billing/Common/Services/InvoicePdfService.cs:20`, `B/Wms.Application/Weighbridge/Common/Services/WeighbridgeTicketPdfService.cs:246` y tres del dominio (`B/Wms.Domain/Entities/Warehouse/ForkliftUse.cs:50`, `B/Wms.Domain/Entities/Warehouse/NoveltyQuantityRules.cs:12`, `B/Wms.Domain/Services/EntryCorrectionRules.cs:150`). <br>• **Cambio:** `B/Wms.Common/Formatting/WmsCulture.cs` (nuevo; `Wms.Common` lo referencian el dominio y la aplicación) expone `WmsCulture.Instance` = `CultureInfo.GetCultureInfo("es-CO")`, de solo lectura. Los 19 archivos lo usan. La salida no cambia: es la misma cultura en un solo lugar | D1 |
| D7 | **Backend: ningún texto con la cultura del servidor.** <br>• **Hoy:** estos textos no pasan cultura y salen con la del proceso. En el contenedor de staging (`B/deploy/staging/Dockerfile.staging:17`, `aspnet:10.0` sin cultura configurada) es la invariante: punto decimal y coma de miles, distinto de la pantalla. Es la inconsistencia del legacy que D2 pide no copiar: <br>  – `ToString("0.##")` de `B/Wms.Application/ForeignTrade/Common/Services/DepositPdfService.cs:539` y `DispatchGuidePdfService.cs:902` (cantidades del PDF del depósito y de la guía: `640.13` en staging, `640,13` en pantalla) y de `B/Wms.Application/Warehouse/Common/Services/WarehouseMovementsPdfService.cs:416`; <br>  – las interpolaciones `:N2` de `B/Wms.Application/Billing/Common/Services/StorageBillingService.cs:264`, `:286` y `:386`, `B/Wms.Application/Billing/EventHandlers/WeeklyExchangeRateChangedHandler.cs:43`, `B/Wms.Application/Warehouse/Commands/AdjustInventory/AdjustInventoryCommandHandler.cs:159` y `:262-266`, `B/Wms.Application/Warehouse/Commands/Reception/ReceptionDeclaredDifference.cs:52` y `:123`, `B/Wms.Application/Weighbridge/Commands/ModifyFirstWeight/ModifyFirstWeightHandler.cs:94`, `ModifySecondWeight/ModifySecondWeightHandler.cs:118` y `B/Wms.Infrastructure/Services/NotificationService.cs:108-116`, `:383-387` y `:482-486`. <br>• **Cambio:** pasan `WmsCulture.Instance` de forma explícita (`ToString(formato, WmsCulture.Instance)` o `string.Create(WmsCulture.Instance, $"…")`). Las cantidades de `0.##` pasan a `QuantityDisplay.Quantity` (`#,##0.##`, `QuantityDisplay.cs:15`), que ya usan las etiquetas, para que el PDF del depósito y la guía muestren `1.920` y `640,13` como la pantalla. <br>• **Sin cambio:** las plantillas de `ILogger` (`B/Wms.Application/Billing/Jobs/BillingJobService.cs:56` y `:90`), que no ve el usuario; los `Guid.ToString("N")`; y la lectura de parámetros de fórmulas y CSV con `InvariantCulture` (`B/Wms.Application/Billing/Calculators/*`, `B/Wms.Application/Administration/LegacyImport/Common/LegacyValueParsers.cs:37`), que es dato y no texto para el usuario. <br>• **No se cambia la cultura por omisión del proceso** (`CultureInfo.DefaultThreadCurrentCulture`): haría que un `decimal.Parse` sin cultura leyera `1.5` como 15. <br>• **Textos ya guardados** con punto decimal (auditoría, observaciones de staging): se quedan como están | D1, D2 |
| D8 | **Guardia del backend** (nueva, `B/Wms.Tests/Common/NumberCultureGuardTests.cs`): recorre los `.cs` de `Wms.Domain`, `Wms.Application`, `Wms.Infrastructure` y `Wms.Api` (sin `Migrations`) y falla si aparece `"es-CO"` fuera de `WmsCulture.cs`, o un `ToString("0.##")`, `ToString("N…")` o `ToString("#,##0…")` sin segundo argumento. Una interpolación `{x:N2}` dentro de un texto para el usuario debe ir en `string.Create(WmsCulture.Instance, …)`: la guardia busca `:N` / `:C` / `:#` en interpolaciones fuera de ese patrón y de las plantillas de `ILogger`; si da falsos positivos, se acota con una lista explícita y se documenta | D6, D7 |
| D9 | **Decisión del hub: `DEC-082 — Formato numérico es-CO`.** Se agrega a `D/contexto/decisiones.md` (§9) en la fase 3: <br>«**DEC-082 — Formato numérico es-CO** (2026-11-26, QA manual de F05). Todo número que el sistema muestra, imprime o escribe sale en es-CO: coma decimal y punto de miles (`1.234,56`), con una sola utilidad por repo (`app/shared/utils/format.ts` en el frontend, `WmsCulture` en el backend). COP sin decimales; otras monedas con 2; pesos, cantidades, porcentajes y TRM con hasta 2, sin ceros de relleno. Los campos numéricos aceptan la coma y también el punto como separador decimal. Confirma CHG-88 (`DEF-F10-006`) y responde el hallazgo 7b de `planes/sprint-11/qa-manual/hallazgos-int-F05.md`, que pedía `1,234.56`. El legacy no tenía regla: no se copian sus formatos (plan `planes/sprint-11/plan-cerrado-f2-separadores-numericos-2026-11-26.md`, D2). Fuente: el usuario, 2026-11-26.» <br>`D/contexto/convenciones-tecnicas.md` §3 suma a la línea de números la regla de decimales, el punto en los campos (D10) y `WmsCulture` | D1, D5, D10 |
| D10 | **Los campos numéricos aceptan el punto como decimal** (P1). <br>• **Hoy:** con `locale="es-CO"`, `InputNumber` de PrimeVue solo toma la coma como decimal (`isDecimalSign`, `node_modules/primevue/inputnumber/index.mjs:680-686`) e ignora el punto, que toma por separador de miles. Un operario acostumbrado al legacy que escribe `640.5` obtiene `6405`; al pegar `640.5`, también (`onPaste`, `:650-662`). <br>• **Cambio:** un plugin de cliente, `F/plugins/inputnumber-decimal-point.client.ts` (nuevo), escucha en captura `keypress` y `paste` sobre los `input` de `.p-inputnumber`. <br>  – **Tecla:** si el campo admite decimales y la tecla es `.`, la cambia por `,` (cancela el evento y vuelve a despachar `keypress` con `key: ","`). Cubre la tecla decimal del teclado numérico, que según el sistema escribe `.`. En un campo sin decimales, el punto sigue sin efecto. <br>  – **Pegado:** un texto con un solo `.`, sin `,` y con 1 o 2 dígitos después (p. ej. `640.5`, `1234.50`) se toma como decimal y se pega `640,5`. Con 3 dígitos después (`1.234`) se respeta como miles, que es lo es-CO. <br>• **Por qué un plugin:** cubre los 78 `<InputNumber>` de 47 archivos sin tocarlos, y los que se agreguen después. <br>• Los 78 siguen con `locale="es-CO"` y la guardia de hoy (`FT/unit/guards/source-guards.spec.ts:73-80`) no cambia | D2; P1 |
| D11 | **Detalles del frontend.** El marcador `placeholder="0.00"` de `F/features/foreign-trade/components/LoadingOrderForm.vue:868` y `:891` pasa a `0,00`. Las utilidades (`F/shared/utils/format.ts`, `F/utils/colombia-date.ts`) y los guiones de los video tutoriales no cambian: ya están en es-CO | D1 |

---

## 2. Contrato

Ningún contrato cambia: el API envía y recibe números JSON, con punto decimal y sin formato.

---

## 3. Archivos que se tocan

**Backend**

- `B/Wms.Common/Formatting/WmsCulture.cs` (nuevo, D6).
- Los 19 con `"es-CO"` (D6): `B/Wms.Application/Billing/Common/Services/InvoiceCancellationPolicy.cs:19`, `InvoicePdfService.cs:20`, `StorageInvoiceDetailFormatter.cs:8`, `StorageMinimumCharge.cs:13`; `B/Wms.Application/Billing/Jobs/DueNoticeMessage.cs:13`; `B/Wms.Application/Billing/Queries/PreviewFormula/PreviewFormulaHandler.cs:124`, `:162` y `:165`; `B/Wms.Application/Common/Formatting/QuantityDisplay.cs:13`; `B/Wms.Application/ForeignTrade/Common/Services/DepositCancellationNotices.cs:21`; `B/Wms.Application/Reports/NationalizedInventory/NationalizedInventoryPdfService.cs:27`; `B/Wms.Application/Warehouse/Common/Services/DailyIncomingGoodsPdfService.cs:14`, `DailyOutgoingGoodsPdfService.cs:16`, `WarehouseMovementsPdfService.cs:24`; `B/Wms.Application/Weighbridge/Common/Services/DailyBillingPdfService.cs:18`, `SharedNetSplit.cs:13`, `TicketSections.cs:90`, `WeighbridgeTicketPdfService.cs:246`; y los tres del dominio de D6.
- Los de D7.
- Pruebas: `B/Wms.Tests/Common/NumberCultureGuardTests.cs` (nueva) y las que esperen el texto con punto decimal de D7, si alguna corre con la cultura invariante.

**Frontend**

- `F/plugins/inputnumber-decimal-point.client.ts` (nuevo, D10) y su prueba.
- `F/features/foreign-trade/components/LoadingOrderForm.vue` (D11).

**Docs:** este plan, `D/contexto/decisiones.md` (`DEC-082`), `D/contexto/convenciones-tecnicas.md` §3, `D/contexto/estado.md`, `D/planes/README.md`, la matriz y los casos en `D/qa/`.

---

## 4. Fases

| Fase | Repo | Contenido | Cierre | Estado |
| --- | --- | --- | --- | --- |
| 1 | BE | D6 a D8: `WmsCulture`, los 19 archivos, los textos de D7 y la guardia | Compuertas BE; QA-FN-001 a 004 en PASA con el API en cultura invariante | Pendiente |
| 2 | FE | D10 y D11: plugin del punto decimal y marcador | Compuertas FE; QA-FN-005 a 008 en PASA en el navegador | Pendiente |
| 3 | docs | D9: `DEC-082`, convenciones y estado; casos a `D/qa/`; fusión de `f2/formato-numerico` en `fase-2` en los dos repos | Fusiones con push | Pendiente |

---

## 5. Pruebas y casos QA

**Backend:**

- `WmsCultureTests`: `1234567.5m.ToString("N2", WmsCulture.Instance)` = `1.234.567,50`; igual con `CultureInfo.CurrentCulture` invariante en el hilo de la prueba.
- Una prueba por familia de D7 que fije la cultura del hilo en invariante y compruebe el texto es-CO (p. ej. la cantidad del PDF del depósito, el texto de auditoría de `ModifyFirstWeight` y el correo de diferencia de recepción).
- `NumberCultureGuardTests` (D8).

**Frontend (Vitest):**

- Plugin (D10): en un `InputNumber` es-CO con 2 decimales, `.` escribe la coma; en uno sin decimales, `.` no hace nada; pegar `640.5` da 640,5; pegar `1.234` da 1234; pegar `1.234,5` da 1234,5.
- Las guardias de `FT/unit/guards/` siguen en verde sin cambios.

**Casos QA:**

| Caso | Pasos | Resultado esperado |
| --- | --- | --- |
| QA-FN-001 | API en cultura invariante: PDF del depósito y guía de salida del depósito de la QA de F05 (`5f3749d2-…`) | Cantidades `1.920`, `640,13` y `1.279,87`, como en la pantalla |
| QA-FN-002 | Lo mismo: reporte de movimientos por depósito | Cantidades en es-CO |
| QA-FN-003 | Lo mismo: modificar el primer peso de un ciclo (Báscula) y ver la auditoría | «Peso original: 32.000,00 kg, Nuevo peso: …» |
| QA-FN-004 | Lo mismo: aviso de la TRM semanal y advertencia de «TRM PENDIENTE» de un almacenamiento | Montos en es-CO |
| QA-FN-005 | Báscula, registro: en el peso escribir `32023.5` con la tecla `.` | El campo muestra `32.023,5` |
| QA-FN-006 | Etapa Levantes: en la cantidad escribir `640.13`; luego pegar `640.13` | `640,13` en los dos casos |
| QA-FN-007 | En un equipo Windows con configuración regional de Colombia, escribir un decimal con la tecla decimal del teclado numérico en un campo de peso | Queda como coma decimal |
| QA-FN-008 | Un campo sin decimales (p. ej. un monto en COP): escribir `.` | No pasa nada, como hoy |

---

## 6. Compuertas de cada fase

- **BE (fase 1):** `dotnet build Wms.sln` sin errores; `dotnet test Wms.Tests` y `dotnet test Wms.IntegrationTests` en verde (bases medidas en `fase-2` al empezar, con el plan de ajustes de F05 fusionado); `dotnet ef migrations has-pending-model-changes` limpio.
- **FE (fase 2):** `yarn build` con código 0; `yarn test` en verde (base medida al empezar); `yarn lint` sin subir la base y sin errores en archivos nuevos o tocados; las guardias de `FT/unit/guards/` en verde.
- PDF y capturas de los casos de la fase.

---

## 7. Commits

| Fase | Repo | Mensaje |
| --- | --- | --- |
| 1 | BE | `fix(formato): cultura es-CO única en PDF, correos y textos del backend (DEC-082)` |
| 2 | FE | `feat(formato): el punto también es decimal en los campos numéricos (DEC-082)` |
| 3 | docs | `docs(formato): DEC-082, formato numérico es-CO` |

Fusiones: `f2/formato-numerico` en `fase-2`, con `--no-ff`, en BE y en FE, al cerrar la fase 3.

---

## 8. Riesgos

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R1 | El plugin choca con una versión nueva de PrimeVue o despacha un evento que el componente no lee | Prueba del plugin (§5) y QA-FN-005 a 008; si PrimeVue cambia, la prueba falla al actualizar |
| R2 | Un operario pega un número con punto de miles y tres decimales (`1.234`) esperando un decimal | Es la lectura es-CO; los decimales del sistema son como mucho 2, y el caso se muestra en QA-FN-006 |
| R3 | La guardia del backend da falsos positivos con interpolaciones que no son para el usuario | D8: lista explícita y documentada |
| R4 | Textos guardados en staging con punto decimal conviven con los nuevos | Son históricos; staging se recrea en el despliegue final (`DEC-081`) |
| R5 | El plan de ajustes de F05 mueve las líneas de los PDF | Se miden de nuevo al empezar (§0.5) |

---

## 9. Preguntas pendientes

| # | Pregunta | Recomendación |
| --- | --- | --- |
| P1 | **El punto como decimal en los campos** (D10): ¿los campos numéricos aceptan también el punto como separador decimal, para quien escribe como en el legacy? | Sí: evita que `640.5` quede como `6405`, y en es-CO nadie escribe los miles a mano |
| P2 | **Regla de decimales** (D5): ¿se conserva la de hoy (COP sin decimales; otras monedas con 2; pesos, cantidades, porcentajes y TRM con hasta 2, sin ceros de relleno), o pesos y cantidades pasan a mostrar siempre 2 decimales (`12.000,00`), como propone el análisis del legacy? | Conservar la de hoy: es más legible y ya está en toda la app |
