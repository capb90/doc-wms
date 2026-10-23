# Evidencia SEL — API: permisos (F9-API-022 a 025) y medición de la búsqueda

Local · API `http://localhost:5291/api/v1` (BE `3748ec6`) · base `wms_migracion` · 2026-10-08 ~14:05 (hora Colombia).
Tokens obtenidos con `POST /auth/login` por usuario (cuerpo de la petición no impreso). Sin contraseñas ni tokens en este archivo.

## Permisos

| Caso | Usuario (rol) | Petición | Código | Respuesta (resumen) |
|---|---|---|---|---|
| F9-API-022 | `mig.bodega` (Warehouse) | `POST /drivers` con `QA-SEL Tres`, CC `9000000003` | 201 | `data.id = 1be8af80-…19ac`, `isActive: true`, país y teléfono `null` |
| F9-API-022 | `mig.bodega` (Warehouse) | `PATCH /drivers/1be8af80-…19ac` (nombres, apellidos, país `Colombia`, teléfono `3000000003`) | 200 | país y teléfono actualizados, `updatedAt` con valor |
| (contraste) | `mig.bodega` (Warehouse) | `POST /drivers` con cuerpo `{}` | 400 | «Error de validación.»: nombre, apellido y número requeridos (no 403) |
| F9-API-023 | `mig.bodega` (Warehouse) | `POST /vehicles` con cuerpo `{}` | 403 | sin cuerpo |
| F9-API-024 | `mig.facturacion` (Billing) | `POST /drivers` con cuerpo `{}` | 403 | sin cuerpo |
| F9-API-024 (extra) | `mig.facturacion` (Billing) | `PATCH /drivers/1be8af80-…19ac` con cuerpo `{}` | 403 | sin cuerpo |
| F9-API-025 | sin token | `GET /drivers?search=qa&isActive=true&orderByName=true&pageSize=20` | 401 | sin cuerpo |

Con `{}` en los casos que deben dar 403, la autorización se evalúa antes que la validación del modelo: un 403 confirma la política sin crear datos.

## Medición — `GET /drivers?search={t}&isActive=true&orderByName=true&pageIndex=1&pageSize=20`

Usuario `mig.bascula` (Scale). `curl -w '%{time_total}'`, 3 corridas por término. Los términos se describen de forma genérica (datos de personas naturales).

| # | Término (descripción genérica) | totalCount | Ítems | t1 (s) | t2 (s) | t3 (s) | SQL equivalente |
|---|---|---|---|---|---|---|---|
| T1 | Apellido más frecuente de 5 letras, en minúsculas | 76 | 20 | 0,080 | 0,030 | 0,027 | 76 |
| T2 | Fragmento de 4 dígitos de una cédula | 16 | 16 | 0,026 | 0,021 | 0,024 | 16 |
| T3 | Apellido con tilde escrito sin tilde, en minúsculas | 35 | 20 | 0,023 | 0,023 | 0,024 | 35 |
| T4 | «apellido nombre» (orden invertido) de un conductor | 1 | 1 | 0,029 | 0,027 | 0,024 | 1 |
| T5 | Prefijo de 3 letras del nombre más frecuente | 237 | 20 | 0,020 | 0,023 | 0,023 | 237 |
| — | Sin `search` | 4.362 | 20 | 0,014 | 0,003 | 0,002 | 4.361 migrados + `QA-SEL Tres` |

«SQL equivalente»: `count(*)` de solo lectura sobre `drivers` activos con `unaccent(...) ILIKE unaccent('%t%')` en nombres, apellidos y sus dos concatenaciones, más el documento sin espacios (D4). Coincide en los 5 términos.
Criterio < 1 s: cumple en las 15 corridas (máximo 0,080 s, la primera, con la caché fría).
