# Evidencias de la fase 2 (FE) — Formato numérico es-CO

> **Plan:** [`plan-cerrado-f2-separadores-numericos-2026-11-26.md`](../plan-cerrado-f2-separadores-numericos-2026-11-26.md), fase 2 (D10 y D11). **Fecha:** 2026-11-27. **Rama:** FE `f2/formato-numerico` (`3b7656a`) sobre `fase-2` `633b470`.

## Cómo se corrió

- `yarn dev` contra el API local (`dotnet run --launch-profile http`, puerto 5281, BE `f2/formato-numerico`), sin sesión simulada.
- **Sesión:** la del pane, de «Usuario Comercio Exterior». Báscula y Administrador no entran: la contraseña temporal del README del frontend responde «Credenciales inválidas» (lo mismo dice la fase 1). Por eso QA-FN-005 se corrió en el peso (kg) de la etapa Levantes y QA-FN-008 en un campo sin decimales de Configuración > Ciudades, los dos `InputNumber` reales de la app. No se guardó nada: la fila del levante se limpió con `Esc` y el diálogo de la ciudad se canceló.
- **Teclas:** con teclas reales del pane, una por una (su acción de escribir texto inserta el texto sin eventos de tecla y no sirve para este caso).
- **Pegado:** el pane no entrega el portapapeles del sistema a la página. Se despachó sobre el campo un `ClipboardEvent("paste")` con un `DataTransfer` de `text/plain`, que es lo que recibe el campo cuando el usuario pega.
- **Teclado numérico:** el pane no emite la tecla decimal del teclado numérico (`KP_Decimal` y `NumpadDecimal` salen sin `key` ni `keypress`). Se despachó en el campo el `keypress` que da esa tecla cuando escribe punto (`key: "."`, `code: "NumpadDecimal"`) y el resto se tecleó.

## Resultados

| Caso | Pasos | Resultado | Estado |
| --- | --- | --- | --- |
| QA-FN-005 | Peso a levantar (kg) de la etapa Levantes del depósito 2026BA00013: teclear `32023.5` | `32.023,5` ([`fn-005-peso-tecla-punto.jpg`](fn-005-peso-tecla-punto.jpg)) | PASA, en el peso de Levantes; en el registro de Báscula falta, sin sesión de Báscula |
| QA-FN-006 | Cantidad a levantar del mismo depósito: teclear `640.13`; luego pegar `640.13` | `640,13` al teclear ([`fn-006-levantes-tecla-punto.jpg`](fn-006-levantes-tecla-punto.jpg)) y al pegar ([`fn-006-levantes-pegar.jpg`](fn-006-levantes-pegar.jpg)). Pegar `1.234` da `1.234` (miles, R2) | PASA |
| QA-FN-007 | Cantidad a levantar: `640`, la tecla decimal del teclado numérico (simulada) y `13` | `640,13` ([`fn-007-tecla-decimal-numpad-simulada.jpg`](fn-007-tecla-decimal-numpad-simulada.jpg)) | PASA simulada; falta confirmarla en un equipo Windows con configuración regional de Colombia |
| QA-FN-008 | Días de tránsito de «Nueva ciudad» (`max-fraction-digits="0"`): teclear `28`, `.` y `5` | `28` tras el punto y `285` al final: el punto no hace nada ([`fn-008-campo-sin-decimales.jpg`](fn-008-campo-sin-decimales.jpg)) | PASA |

## Compuertas

| Compuerta | Antes (`fase-2` `633b470`) | Después (`3b7656a`) |
| --- | --- | --- |
| `yarn build` | — | código 0; el plugin entra en el bundle |
| `yarn test` | 150 archivos, 805 pruebas en verde | 151 archivos, 812 pruebas en verde (+7 del plugin) |
| Error no manejado de Vitest | 1: `localStorage.getItem is not a function` en `WeighbridgeQueuePage.spec.ts` | el mismo, sin cambios (ajeno al plan) |
| `yarn lint` | 355 errores, 530 avisos | 355 errores, 530 avisos; ninguno en archivos nuevos; los 2 de `LoadingOrderForm.vue` (`:388`, `:408`) ya estaban |
| Guardias `test/unit/guards/` | — | 7 archivos, 37 pruebas en verde, sin cambios |

La prueba del plugin (`test/components/plugins/inputnumber-decimal-point.spec.ts`) monta un `InputNumber` es-CO real. Sin el plugin fallan los 3 casos que dependen de él (la tecla, el teclado numérico y pegar `640.5`); los otros 4 cuidan lo que no debe cambiar.

## Notas

- **Quién decide si hay decimales.** El plugin cambia siempre el `.` tecleado por `,` y deja que el campo decida: en uno sin decimales PrimeVue ignora la coma, como hoy el punto (QA-FN-008). Así no depende de leer las props del componente, que no quedan en el DOM.
- **Pegar en un campo sin decimales.** D10 no distingue el campo al pegar: `640.5` pegado en un campo sin decimales ya no da `6405` sino que no se pega nada, porque PrimeVue rechaza la coma decimal ahí. `1.234` se sigue pegando como `1234`.
