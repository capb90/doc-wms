# Videos publicados que `DEC-029` deja desactualizados

> **Fecha:** 25 de octubre de 2026. **Origen:** `planes/plan-cerrado-dec-029-fob-cif-2026-10-25.md`, D8 y §4.
> **Código de referencia:** Backend `develop` `dafd573` · Frontend `develop` `d838535`.
> **Publicación revisada:** `video-tutoriales-trabajo/salida/publicacion/` (81 subtítulos `.vtt`, sin `.srt`). Solo lectura: no se editan los `.vtt` ni los videos publicados.
> **Regrabar en una tarea aparte (D8).** Los guiones (`videos/guiones/guiones-video-tutoriales.md`) y los scripts de grabación (`Frontend/wms/tools/video-tutoriales/`) ya tienen los textos nuevos.

## 1. Qué cambió en pantalla

| Antes | Ahora | Decisión |
| --- | --- | --- |
| «FOB del levante (USD)», «Valor FOB», «FOB (USD)», «FOB (COP)», «FOB UAP / no UAP», «Total FOB» | «CIF del levante (USD)», «Valor CIF», «CIF (USD)», «CIF (COP)», «CIF UAP / no UAP», «Total CIF» | D1, D2 |
| Segundo producto de un levante: aviso naranja y campo del valor editable | Campo del valor deshabilitado y vacío, con «El CIF de este levante ya se registró con «{producto}» ({USD}). Este producto se registra sin valor.»; el API responde 409 si se fuerza | D6 |
| «Valor Comercial», «Valor de la carga», «Valor de la Carga (Opcional)», «Valor mercancía», «Valor de la mercancía (CIF)» | «Valor de la mercancía» (en la recepción manual, «Valor de la mercancía (opcional)») | D3 |
| «Porcentaje del valor declarado (sin prorrateo)» | «Porcentaje del valor de la mercancía (lote completo)» | D4 |
| «Umbral CIF por encima del cual no se aplica el mínimo ($)» | «Umbral del valor de la mercancía por encima del cual no se aplica el mínimo ($)» | D4 |
| «El porcentaje del valor declarado calcula la base sin IVA…» | «El porcentaje del valor de la mercancía calcula la base sin IVA…» | D3 |
| Al crear una tarifa base o un servicio de acuerdo de ALMACENAMIENTO, la fórmula sale vacía | Sale preseleccionada «Porcentaje del valor de la mercancía (prorrateado por saldo)» | D5 |

## 2. Subtítulos con narración desactualizada

Rutas relativas a `video-tutoriales-trabajo/salida/publicacion/subtitulos/`.

| Archivo | Línea | Dice | Debe decir (guion vigente) |
| --- | ---: | --- | --- |
| `serie-1/1-07-tarifas-base.vtt` | 13 | «… valor de la mercancía, el CIF, convertido a pesos.» | «… valor de la mercancía, convertido a pesos.» |
| `serie-2/2-04-formulas-de-porcentaje.vtt` | 9 | «… valor de la mercancía, el CIF, en pesos.» | «… valor de la mercancía, en pesos.» |
| `serie-2/2-04-formulas-de-porcentaje.vtt` | 29 | «… si el CIF lo supera …» | «… si el valor de la mercancía lo supera …» |
| `serie-2/2-04-formulas-de-porcentaje.vtt` | 37 | «el CIF multiplicado por el saldo …» | «el valor de la mercancía multiplicado por el saldo …» |
| `serie-2/2-04-formulas-de-porcentaje.vtt` | 41 | «La primera, en cambio, cobra el CIF completo …» | «La de lote completo, en cambio, cobra el valor completo …» |
| `serie-7/7-07-levantes.vtt` | 21 | «El FOB se convierte con la TRM …» | «El CIF se convierte con la TRM …» |
| `serie-7/7-15-reportes-de-comercio-exterior.vtt` | 29 | «… suma el FOB de los levantes …» | «… suma el CIF de los levantes …» |

Ningún otro `.vtt` dice «FOB», «valor comercial», «valor declarado», «Umbral CIF» ni «CIF» por el depósito (grep del 2026-10-25; la coincidencia de «especificidad» en `2-07` es falsa).

## 3. Videos con textos de pantalla desactualizados

Los subtítulos de estos videos pueden estar bien, pero la imagen muestra los rótulos viejos del §1. Rutas relativas a `video-tutoriales-trabajo/salida/publicacion/videos/`.

| Video | Qué se ve viejo | Script ajustado (fase 2) |
| --- | --- | --- |
| `serie-1/1-07-tarifas-base.mp4` | «Porcentaje del valor declarado (sin prorrateo)», la nota del IVA, «Valor de la mercancía (CIF)» en la vista previa; la fórmula no sale preseleccionada | `videos/1.7.mjs` |
| `serie-2/2-02-crear-acuerdo-y-servicio.mp4` | «Porcentaje del valor declarado (sin prorrateo)»; la fórmula no sale preseleccionada | `videos/2.2.mjs` |
| `serie-2/2-04-formulas-de-porcentaje.mp4` | Nombre de la fórmula, nota del IVA y «Umbral CIF …» | `videos/2.4.mjs` |
| `serie-2/2-05-previsualizar.mp4` | «Valor de la mercancía (CIF)» en la vista previa | `videos/_acuerdos.mjs` |
| `serie-2/2-06-carga-perecedera.mp4` | Al crear la tarifa de ALMACENAMIENTO, la fórmula no sale preseleccionada (el video elige otra; cambio menor) | — |
| `serie-2/2-07-como-elige-la-tarifa.mp4` | «Porcentaje del valor declarado (sin prorrateo)» | `videos/2.7.mjs` |
| `serie-2/2-09-convenio-completo.mp4` | «Porcentaje del valor declarado (sin prorrateo)» y «Valor de la mercancía (CIF)» en la vista previa | `videos/2.9.mjs`, `videos/_acuerdos.mjs` |
| `serie-3/3-03-como-se-calcula-una-factura.mp4` | «Valor mercancía (USD)» en el detalle de la factura | `videos/3.3.mjs` |
| `serie-3/3-05-almacenamiento-y-depositos-pendientes.mp4` | Columna «Valor mercancía» en Depósitos Pendientes | `videos/3.5.mjs` |
| `serie-7/7-02-completar-un-deposito.mp4` | «Valor Comercial» en «Información General» | `videos/7.2.mjs` |
| `serie-7/7-07-levantes.mp4` | «Valor FOB», «FOB del levante (USD)», «FOB:» en la confirmación y «FOB (USD)»/«FOB (COP)» en la tarjeta de levantes | `videos/7.7.mjs` |
| `serie-7/7-15-reportes-de-comercio-exterior.mp4` | «Valor FOB de los levantes (USD), …» en el informe de póliza | `videos/7.15.mjs` |

## 4. Para la tarea de regrabación

- Regrabar los 12 videos del §3 (incluye los 4 del §2) con los scripts vigentes y republicar sus `.vtt`.
- `pronunciacion.json` no cambia: «CIF» ya existía.
- 2.6 puede quedar como está si se acepta que no muestra la preselección.
