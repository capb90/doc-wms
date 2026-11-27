# Evidencias de la fase 1 (BE) — Formato numérico es-CO

> **Plan:** [`plan-cerrado-f2-separadores-numericos-2026-11-26.md`](../plan-cerrado-f2-separadores-numericos-2026-11-26.md), fase 1 (D6 a D8). **Fecha:** 2026-11-27. **Rama:** BE `f2/formato-numerico` sobre `fase-2` `dcb7b8f`.

## Cómo se corrió

- **Cultura invariante, como en staging.** El contenedor de staging (`aspnet:10.0` sin `LANG`) tiene ICU y la cultura del proceso invariante. En el Mac, .NET toma la cultura del sistema (`en-CO`) e ignora `LANG=C`, y con `DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1` .NET no tiene la cultura es-CO (modo de globalización invariante), que no es lo que corre en staging. Por eso el proceso se arrancó con un *startup hook* (`DOTNET_STARTUP_HOOKS`, fuera del repo) que fija `CultureInfo.DefaultThreadCurrentCulture` y `CurrentCulture` en la invariante antes de `Main`: la muestra `1234.5m.ToString("N2")` del proceso da `1,234.50`.
- **Base desechable.** `wmsdb` no tiene salidas ni guías, y sus usuarios ya no tienen la contraseña temporal del README del frontend. Como en la QA de los ajustes de F05 (`qa/casos-qa2-f05-ajustes-qa-2026-11-26.md`, nota 1), los cinco casos se corrieron con el flujo de las pruebas de integración (Testcontainers) por el API, con una prueba temporal que no se subió. El depósito reproduce las cifras del de la QA de F05 (2026BA00013): 1.920 de entrada, un levante de 640,13 y una salida de 640,13. Ni `wmsdb` ni sus datos se tocaron.
- **Antes y después.** La misma prueba se corrió sobre `fase-2` `dcb7b8f` (antes) y sobre la rama (después), las dos con el *hook*.

## Resultados

| Caso | Antes (`dcb7b8f`, cultura invariante) | Después (rama, cultura invariante) | Estado |
| --- | --- | --- | --- |
| QA-FN-001 — PDF del depósito | Entrada y amparada `1920` ([`fn-001-deposito-antes.pdf`](fn-001-deposito-antes.pdf)) | `1.920` ([`fn-001-deposito.pdf`](fn-001-deposito.pdf)) | PASA |
| QA-FN-001 — Guía de salida | `1920 · 1920 · 640.13 · 1279.87`; «Total en esta salida 640.13» ([`fn-001-guia-salida-antes.pdf`](fn-001-guia-salida-antes.pdf)) | `1.920 · 1.920 · 640,13 · 1.279,87`; «Total en esta salida 640,13» ([`fn-001-guia-salida.pdf`](fn-001-guia-salida.pdf), [`fn-001-guia-salida.jpg`](fn-001-guia-salida.jpg)) | PASA |
| QA-FN-002 — Movimientos por depósito | `1920`, `640.13`, `1279.87` ([`fn-002-movimientos-antes.pdf`](fn-002-movimientos-antes.pdf)) | `1.920`, `640,13`, `1.279,87` ([`fn-002-movimientos.pdf`](fn-002-movimientos.pdf)) | PASA |
| QA-FN-003 — Aviso del primer peso modificado | «Peso original: 32,000.00 kg, Nuevo peso: 32,023.50 kg.» | «Peso original: 32.000,00 kg, Nuevo peso: 32.023,50 kg.» | PASA |
| QA-FN-004 — TRM semanal (auditoría del recálculo) | «… por tasa semanal del 08/03/2097 al 14/03/2097 (4,123.45)» | «… por tasa semanal del 08/03/2097 al 14/03/2097 (4.123,45)» | PASA |
| QA-FN-004 — «TRM PENDIENTE» del almacenamiento | «el valor en pesos de la mercancía (20,000.00 USD)» | «el valor en pesos de la mercancía (20.000,00 USD)» | PASA |
| QA-FN-009 — Levante mayor que lo pendiente | «La cantidad a levantar (1300.5) supera lo pendiente por nacionalizar del producto (1279.87).» | «La cantidad a levantar (1300,5) supera lo pendiente por nacionalizar del producto (1279,87).» | PASA |

- **QA-FN-009:** lo pendiente es 1.279,87 (1.920 − 640,13), así que se pidió 1.300,5 en lugar del 700,5 del ejemplo del plan. El formato `0.####` no lleva punto de miles (D5 y D7: solo gana la cultura).
- **Guía de salida:** con el punto de miles, «1.279,87» ya no cabía en las columnas numéricas de 35 pt y se partía en «1.279,8» / «7». Las cuatro columnas numéricas pasaron a 40 pt (`DispatchGuidePdfService.cs`). El número de levante de la prueba se parte ahora en el guion («LEV-» / «ae9c18b66b»), como ya pasaba con «Aceptación». El plan de formatos v2 de PDF rehace esta tabla.
