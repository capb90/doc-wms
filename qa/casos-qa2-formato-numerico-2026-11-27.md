# Casos QA — Fase 2 · Formato numérico es-CO único

> **Para qué sirve:** los casos QA-FN-001 a 009 del plan de formato numérico es-CO, con su resultado, copiados al cerrar la fase 3.
> **Plan:** [`planes/sprint-11/plan-cerrado-f2-separadores-numericos-2026-11-26.md`](../planes/sprint-11/plan-cerrado-f2-separadores-numericos-2026-11-26.md) (§5). Decisión: `DEC-082`. Hallazgo de origen: el 7b de [`planes/sprint-11/qa-manual/hallazgos-int-F05.md`](../planes/sprint-11/qa-manual/hallazgos-int-F05.md).
> **Fecha de corte:** 2026-11-27. Rama `f2/formato-numerico`: BE fase 1 `08a1f72` (sobre `fase-2` `dcb7b8f`); FE fase 2 `3b7656a` (sobre `fase-2` `633b470`). Fusiones en `fase-2`: BE `6ccff7b`, FE `8884936`.
> **Fuente:** el plan cerrado manda; esta copia no se edita salvo para registrar un re-test.
> **Verificación:**
> - **Backend (001 a 004 y 009):** con el proceso del API en cultura invariante, como el contenedor de staging, por el flujo de las pruebas de integración (nota 1). Antes y después sobre la misma prueba. Resumen: [`fn-textos-fase-1.md`](../planes/sprint-11/evidencias-formato-numerico/fn-textos-fase-1.md).
> - **Frontend (005 a 008):** `yarn dev` contra el API local, sin la sesión simulada, con el usuario de prueba local de Comercio Exterior (las contraseñas no se copian). Depósito 2026BA00013. Resumen: [`fn-campos-fase-2.md`](../planes/sprint-11/evidencias-formato-numerico/fn-campos-fase-2.md).
> - Evidencias en `planes/sprint-11/evidencias-formato-numerico/fn-*`.

## 1. Casos

| ID | Pasos | Resultado esperado | Verificación | Resultado |
| --- | --- | --- | --- | --- |
| QA-FN-001 | API en cultura invariante: PDF del depósito y guía de salida del depósito de la QA de F05 (`5f3749d2-…`) | Cantidades `1.920`, `640,13` y `1.279,87`, como en la pantalla | Prueba de integración, PDF (fase 1) | PASA (BE `08a1f72`), con un depósito sembrado por la prueba con las cifras del de la QA de F05 (1.920 de entrada, un levante y una salida de 640,13; nota 1). Antes `1920 · 640.13 · 1279.87`; después `1.920 · 1.920 · 640,13 · 1.279,87` y «Total en esta salida 640,13» (`fn-001-deposito*.pdf`, `fn-001-guia-salida*`). Las columnas numéricas de la guía pasan a 40 pt (nota 2) |
| QA-FN-002 | Lo mismo: reporte de movimientos por depósito | Cantidades en es-CO | Prueba de integración, PDF (fase 1) | PASA (BE `08a1f72`; `1.920`, `640,13`, `1.279,87`; `fn-002-movimientos*.pdf`) |
| QA-FN-003 | Lo mismo: modificar el primer peso de un ciclo (Báscula) y ver la auditoría | «Peso original: 32.000,00 kg, Nuevo peso: …» | Prueba de integración (fase 1) | PASA (BE `08a1f72`; en el aviso del peso modificado, antes «32,000.00 kg … 32,023.50 kg», después «32.000,00 kg … 32.023,50 kg») |
| QA-FN-004 | Lo mismo: aviso de la TRM semanal y advertencia de «TRM PENDIENTE» de un almacenamiento | Montos en es-CO | Prueba de integración (fase 1) | PASA (BE `08a1f72`; «(4.123,45)» en el recálculo por tasa semanal y «(20.000,00 USD)» en «TRM PENDIENTE») |
| QA-FN-009 | Lo mismo: registrar un levante con una cantidad decimal mayor que lo pendiente del producto (p. ej. pendiente 640,13 y pedir 700,5) | El error dice «La cantidad a levantar (700,5) supera lo pendiente por nacionalizar del producto (640,13).» | Prueba de integración (fase 1) | PASA (BE `08a1f72`; «(1300,5) … (1279,87)»; antes «(1300.5) … (1279.87)»). Lo pendiente era 1.279,87, así que se pidió 1.300,5 y no el 700,5 del ejemplo del plan. Sin punto de miles: es un `0.####` (nota 3) |
| QA-FN-005 | Báscula, registro: en el peso escribir `32023.5` con la tecla `.` | El campo muestra `32.023,5` | Navegador (fase 2) | PASA en el peso a levantar (kg) de la etapa Levantes (FE `3b7656a`; `fn-005-peso-tecla-punto.jpg`). **Pendiente de la QA del usuario en el registro de Báscula:** no hubo sesión de Báscula (nota 4) |
| QA-FN-006 | Etapa Levantes: en la cantidad escribir `640.13`; luego pegar `640.13` | `640,13` en los dos casos | Navegador (fase 2) | PASA (FE `3b7656a`; `fn-006-levantes-tecla-punto.jpg` y `fn-006-levantes-pegar.jpg`). Pegar `1.234` da 1.234 (miles, R2 del plan). El pegado se despachó como evento (nota 5) |
| QA-FN-007 | En un equipo Windows con configuración regional de Colombia, escribir un decimal con la tecla decimal del teclado numérico en un campo de peso | Queda como coma decimal | Navegador, simulada (fase 2) | PASA simulada (FE `3b7656a`; `640`, la tecla decimal despachada como evento y `13` dan `640,13`; `fn-007-tecla-decimal-numpad-simulada.jpg`). **Pendiente de la QA del usuario en un equipo Windows** (nota 5) |
| QA-FN-008 | Un campo sin decimales (p. ej. un monto en COP): escribir `.` | No pasa nada, como hoy | Navegador (fase 2) | PASA (FE `3b7656a`; días de tránsito de «Nueva ciudad», `max-fraction-digits="0"`: `28`, `.` y `5` dan `285`; `fn-008-campo-sin-decimales.jpg`) |

## 2. Pendientes de la QA del usuario

- **QA-FN-005** en el peso del registro de Báscula, con una sesión de Báscula.
- **QA-FN-007** con la tecla decimal real del teclado numérico, en un equipo Windows con configuración regional de Colombia.

## 3. Notas

1. **Backend en cultura invariante.** En el Mac, .NET ignora `LANG=C` y toma la cultura del sistema; con `DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1` no tiene la cultura es-CO, que no es lo que corre en staging. El proceso se arrancó con un *startup hook* (fuera del repo) que fija la cultura invariante antes de `Main`. La base local no tiene salidas ni guías, así que los cinco casos se corrieron con el flujo de las pruebas de integración (Testcontainers) por el API, con una prueba temporal que no se subió, como en `casos-qa2-f05-ajustes-qa-2026-11-26.md` (nota 1). La base local no se tocó.
2. **Ancho de la guía de salida (001).** Con el punto de miles, «1.279,87» ya no cabía en 35 pt y se partía. Las cuatro columnas numéricas pasaron a 40 pt (`DispatchGuidePdfService.cs`). El plan de formatos v2 de PDF rehace esa tabla.
3. **Los `0.####` (009).** Conservan sus hasta 4 decimales y no llevan punto de miles: solo ganan la cultura (`DEC-082`, precisiones).
4. **Sesión de Báscula (005).** La contraseña temporal de los usuarios de prueba locales ya no vale para Báscula ni para Administrador. El caso se corrió en el peso de Levantes, otro `InputNumber` de kg real de la app; el plugin no distingue pantallas.
5. **Teclado y portapapeles (006 y 007).** El navegador de la prueba no entrega el portapapeles del sistema ni emite la tecla decimal del teclado numérico. Se despacharon sobre el campo el `ClipboardEvent("paste")` con `text/plain` y el `keypress` de esa tecla (`key: "."`, `code: "NumpadDecimal"`), que es lo que recibe el campo; el resto se tecleó.
6. **Pegar en un campo sin decimales.** `640.5` no pega nada (antes daba 6.405), porque el campo rechaza la coma decimal. El usuario vio el cambio y siguió sin objetarlo (`DEC-082`, precisiones).
7. **Datos que quedan.** Ninguno: la fila del levante se limpió con `Esc` y el diálogo de la ciudad se canceló.
