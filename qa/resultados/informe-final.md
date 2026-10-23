# Informe final del QA — WMS Bodegas Asociadas

> Corte: **2026-10-07 01:15** (hora Colombia, re-test en staging posterior a S6, FE `8527144` / BE `84c712f`). Antes: 00:45, sesión S6 en staging · Build candidato **FE `24d742d` / BE `f6f1828`**, desplegado en staging como FE `508b91b` / BE `b31ddb6` (el candidato más DEF-MIG-007, DEF-MIG-008 y «Estadísticas» oculto) · Ejecutor: Claude (agente QA, Opus 5.5).
> El veredicto se basa en el ambiente local (S0–S5) y en **staging con datos migrados (S6, `F11-informe-S6-2026-10-06.md`)**. De lo diferido a staging solo queda PRF-002, que mide un operario (decisión del usuario).

## Resumen ejecutivo

- **Recomendación: GO condicionado solo a PRF-002 (medición con un operario).** S6 ejecutó en staging, con datos migrados, todo el bloque diferido: F0, F11-REG-001 a 013, E2E-01, la DIAN real, las diferencias de staging y el humo. También el Anexo A desde la operación. **Sin FALLA en P0 y sin fichas abiertas:** las dos de S6 quedaron verificadas en staging el 2026-10-07.
- **S6 abrió dos fichas, ya corregidas y verificadas en staging** (§4), en el re-test posterior a S6 (FE `8527144` / BE `84c712f`, redespliegue sin recrear la base):
  - **DEF-F11-021 (MAJOR):** el enlace real del correo de recuperación del Admin abre «Restablecer contraseña» y el cambio funciona; F0-LOG-008 pasa.
  - **DEF-F11-020 (MINOR):** dos respaldos simultáneos dan 202 y 409, y los del mismo minuto quedan en archivos distintos.
  - La observación **O-3** también quedó verificada: el «por facturar» de báscula responde `totalAmount` 20.000.
- Quedan anotados 130 P1 aceptados con cobertura indirecta.
- La campaña ejecutó 955 casos en F0–F10 y abrió 126 fichas. La fase 11 re-testeó 145 fichas: las 126 de la campaña y 19 propias. S6 agregó 2 en staging, re-testeadas allí después del redespliegue. Hoy hay **147 fichas: 147 Verificadas, 0 Reabiertas y 0 abiertas**.
- **S5 (2026-10-06)** verificó las dos fichas que dejaban el NO-GO de S4 sobre BE `00d6ac3`:
  - **DEF-F11-017 (CRITICAL):** el recálculo del almacenamiento ya cobra la cantidad del período: 41 y 40 bultos, no 11 y 10. La factura conserva su N.º y su aprobación, y Facturación recibe el aviso con el total anterior y el nuevo.
  - **DEF-F11-016 (MAJOR):** corregir el motivo ya no saca al camión de la cola de báscula.
- S5 ejecutó además los **117 P1 pendientes de Báscula, Comercio Exterior y Facturación**: 110 PASA, 2 FALLA, 3 no aplica y 2 diferidos a staging.
- Las dos fallas eran de Báscula y no tocaban importes cobrados. Se corrigieron y el **re-test posterior a S5** (FE `24d742d` / BE `f6f1828`) las verificó:
  - **DEF-F11-018 (MAJOR):** el reporte diario del 06/10 da dos filas para el ciclo multidepósito de QAK402, con el cobro del principal en el total. El total, $ 843.980, coincide con la suma de las facturas de báscula del día. Muestra el destinatario de Consumidor final y de persona no registrada, y la hora de Colombia;
  - **DEF-F11-019 (MINOR):** el detalle del ciclo muestra el estado real del depósito («Cerrado») y el filtro «Cerrado» funciona.
- La suite REG está completa (31 de 31) en local. Los **232 P0** de las fases 0 a 10 se re-ejecutaron en la fase 11. Los **P1** se ejecutaron por ID en **209 de 341**.
- **S6 (staging, 2026-10-06/07):** 74 casos. **66 PASA, 3 FALLA (ninguno P0), 1 no aplica, 1 no ejecutado (respaldo de las 02:00, no alcanzado) y 3 pendientes de operario** (PRF-002, F3-REG-024 y F3-PES-015). DEF-MIG-005, DEF-MIG-007 y DEF-MIG-008 quedan verificados en staging.
- Pendiente: **PRF-002**, con el criterio de registro en báscula en 30 s o menos (incluye F3-REG-024 y F3-PES-015). El escenario está preparado (camión QSP001).

## 1. Alcance ejecutado

| Fase | Fecha | Build FE / BE | Ambiente | Informe |
|---|---|---|---|---|
| F0 Smoke | 2026-10-02 | `a5289ce` / `191d4b1` | Local | `F0-informe-2026-10-02.md` |
| F1 Administración | 2026-10-02 | `a5289ce` / `191d4b1` | Local | `F1-informe-2026-10-02.md` |
| F2 Vigilancia | 2026-10-02 | `a5289ce` / `191d4b1` | Local | `F2-informe-2026-10-02.md` |
| F3 Báscula | 2026-10-02 | `a5289ce` / `191d4b1` | Local | `F3-informe-2026-10-02.md` |
| F4 Bodega | 2026-10-02 | `41c19cd` / `191d4b1` | Local | `F4-informe-2026-10-02.md` |
| F5 Comercio Exterior | 2026-10-02 | `41c19cd` / `191d4b1` | Local | `F5-informe-2026-10-02.md` |
| F6 Facturación | 2026-10-02 | `41c19cd` / `191d4b1` | Local | `F6-informe-2026-10-02.md` |
| F7 Transversal | 2026-10-03 | `1501cd6` / `191d4b1` | Local | `F7-informe-2026-10-03.md` |
| F8 E2E | 2026-10-03 | `1501cd6` / `191d4b1` | Local | `F8-informe-2026-10-03.md` |
| F9 Roles y permisos | 2026-10-03 | `1501cd6` / `191d4b1` | Local | `F9-informe-2026-10-03.md` (+ anexo matriz API) |
| F10 UX, visual y errores | 2026-10-03 | `1501cd6` / `191d4b1` | Local | `F10-informe-2026-10-03.md` |
| Plan de corrección | 2026-10-03 – 05 | CHG-01 a CHG-90 en 12 fases | — | `plan-correccion-defectos.md` |
| F11-S0 Preparación | 2026-10-05 | `4074c63`+ / `09b0baf`+ | Local (base recreada) | `F11-informe-S0-2026-10-05.md` |
| F11-S1 RET CRITICAL + REG | 2026-10-05 | `ae36cb4` / `c56cc86` | Local | `F11-informe-S1-2026-10-05.md` |
| F11-S2 RET MAJOR | 2026-10-05 | `15a5028` / `214f5f6` | Local | `F11-informe-S2-2026-10-05.md` |
| F11-S3 RET MINOR y TRIVIAL | 2026-10-06 | `d9783af` / `44bd80a` | Local | `F11-informe-S3-2026-10-06.md` |
| F11-S4 Cierre | 2026-10-06 | `e41decf` / `ea14548` | Local | `F11-informe-S4-2026-10-06.md` |
| F11-S5 Re-test posterior a S4 y P1 de F3, F5 y F6 | 2026-10-06 | **`bd729e5` / `00d6ac3`** | Local | `F11-informe-S5-2026-10-06.md` · inventario `F11-S5-inventario-P1.md` |
| F11 re-test posterior a S5 (DEF-F11-018 y DEF-F11-019) | 2026-10-06 | **`24d742d` / `f6f1828`** | Local | Fichas y `evidencias/F11/RT-DEF-F11-018-019.txt` |
| **F11-S6 · QA en staging con datos migrados** (Fase 4 del plan de migración) | 2026-10-06/07 | **`508b91b` / `b31ddb6`** | **Staging** | `F11-informe-S6-2026-10-06.md` |
| F11 re-test en staging posterior a S6 (DEF-F11-020, DEF-F11-021 y O-3) | 2026-10-07 | **`8527144` / `84c712f`** | **Staging** | Fichas y `evidencias/F11/RT-S6-redespliegue-retest.txt` |
| PRF-002 (con F3-REG-024 y F3-PES-015) | — | — | Staging | **Pendiente: lo mide un operario** (decisión del usuario) |

**Fuera del alcance ejecutado:**
- Anexo A (migración legacy): **cumplido en local y en staging.** Fases 1 y 3 del plan de migración y S6 (§7).
- Anexo B (respaldos): FB-BAK-003 y FB-BAK-005 en S6. FB-BAK-003 abrió DEF-F11-020, verificado en el re-test posterior a S6. La corrida programada de las 02:00 queda para la Fase 5.
- Pruebas contra producción: ninguna.

## 2. Métricas

### 2.1 Casos de la campaña (F0–F10, primera ejecución)

| Fase | Total | Pasa | Falla | Bloqueado | No ejecutado | No aplica | No verificable | Observación |
|---|---|---|---|---|---|---|---|---|
| F0 | 37 | 32 | 1 | 0 | 1 | 0 | 0 | 3 |
| F1 | 144 | 101 | 12 | 1 | 12 | 2 | 1 | 15 |
| F2 | 49 | 35 | 4 | 0 | 7 | 0 | 0 | 3 |
| F3 | 182 | 101 | 25 | 4 | 45 | 0 | 1 | 6 |
| F4 | 84 | 59 | 20 | 4 | 1 | 0 | 0 | 0 |
| F5 | 131 | 101 | 16 | 5 | 4 | 1 | 1 | 3 |
| F6 | 144 | 98 | 28 | 2 | 9 | 3 | 2 | 2 |
| F7 | 59 | 39 | 14 | 0 | 3 | 0 | 3 | 0 |
| F8 (E2E) | 20 | 7 | 13 | 0 | 0 | 0 | 0 | 0 |
| F9 | 59 | 37 | 19 | 0 | 2 | 0 | 0 | 1 |
| F10 | 46 | 25 | 16 | 0 | 4 | 0 | 0 | 1 |
| **Total** | **955** | **635** | **168** | **16** | **88** | **6** | **8** | **34** |

### 2.2 Fase 11 (re-test, regresión y cierre: S0–S5 en local, S6 en staging)

| Sesión | Ejecutados | Pasa | Falla | Bloqueado | No ejecutado | Diferido a staging | Contenido |
|---|---|---|---|---|---|---|---|
| S0 | 7 | 6 | 0 | 0 | 0 | — | Ambiente, usuarios, dataset y cadena operativa (1 observación: DEF-F11-001) |
| S1 | 47 | 42 | 3 | 1 | 0 | — | 13 CRITICAL y REG |
| S2 | 54 | 52 | 1 | 1 (parcial) | 0 | — | 46 MAJOR y DEF-F11-001 a 005 |
| S3 | 79 | 78 | 1 | 0 | 0 | — | 67 MINOR y TRIVIAL, REG-024, SMTP caído, R-EXP y R-TRZ |
| S4 | 146 | 142 | 2 | 0 | 247 (P1 de DIR) | 52 | Re-test posterior a S3, AUT, DIR e informe final |
| S5 | 127 | 122 | 2 | 0 | 0 (3 «no aplica») | 2 | Parte A: re-test de DEF-F11-016 y DEF-F11-017 (12 casos). Parte B: 117 P1 de F3, F5 y F6 |
| Re-test posterior a S5 | 2 | 2 | 0 | 0 | 0 | — | F3-RPT-001 (DEF-F11-018) y F3-CIC-001 (DEF-F11-019) |
| **S6 (staging)** | 71 | 66 | 3 | 0 | 1 (respaldo de las 02:00) | 3 pendientes de operario (PRF-002) | F0 (37), REG-001 a 013, E2E-01, F6-TRM-001, diferencias de staging, humo, FA-MIG-009 por rol, DEF-MIG-005/007, factura de un migrado y FB-BAK-005. 1 «no aplica» (Swagger). FALLA: F0-LOG-008, recuperación de contraseña (DEF-F11-021) y concurrencia de FB-BAK-003 (DEF-F11-020) |
| Re-test en staging posterior a S6 | 5 | 5 | 0 | 0 | 0 | — | DEF-F11-021 (curl, enlace real del correo, sin retrocesos), F0-LOG-008, DEF-F11-020 (FB-BAK-003 concurrente y del mismo minuto), O-3 y el humo del redespliegue |

- **Suite REG:** 31 de 31 ejecutados en local (S1 a S3), ninguno con FALLA final. Las fallas iniciales (REG-002 y REG-028 por DEF-F11-004, REG-022 por DEF-F11-003) se corrigieron y se re-ejecutaron.
- **RET:** 147 fichas re-testeadas (126 de la campaña + DEF-F11-001 a 021). DEF-F8-001 se verificó con DEF-F3-002.
- **DIR:**
  - P0 de F0–F10 re-ejecutados en la fase 11: **232 de 232**.
  - P1: **209 de 341**: 94 en S0–S4 y 115 en S5 (los 117 P1 pendientes de F3, F5 y F6, menos 2 diferidos a staging).
  - Quedan **130 P1** de F0 (8), F1 (52), F2 (21), F4 (16), F7 (12), F9 (14) y F10 (7) sin ejecución por ID: aceptados con cobertura indirecta (§7, nota).
- **AUT** (build de S4, `ea14548`; S5 no lo re-ejecutó: no estaba en su alcance, y el commit `00d6ac3` agrega sus propias pruebas `StorageBillableQuantityTests`, `StorageRecalculationDispatchTests`, `WeighbridgeQueueOpenEntryTests` y `QueueAfterEntryCorrectionTests`):
  - `dotnet test`: 1605 + 269 = **1874 pruebas, 0 fallos**.
  - `yarn build`: código 0.
  - `yarn test`: **266/266**.
  - `yarn lint`: **279** errores (tope 279).

### 2.3 Defectos por severidad y estado (147 fichas)

| Severidad | Total | Verificado | Nuevo (abierto) | Reabierto |
|---|---|---|---|---|
| CRITICAL | 15 | 15 | 0 | 0 |
| MAJOR | 51 (+1 duplicado) | 51 (+1 unificada en DEF-F3-002) | 0 | 0 |
| MINOR | 73 | 73 | 0 | 0 |
| TRIVIAL | 7 | 7 | 0 | 0 |
| **Total** | **147** | **147** | **0** | **0** |

Por origen: 126 de la campaña (F0–F10) y 21 de la fase 11 (DEF-F11-001 a 021; DEF-F11-020 y 021 de S6, en staging).

### 2.4 Defectos por módulo (todas las fichas)

| Módulo | CRITICAL | MAJOR | MINOR | TRIVIAL | Total | Abiertos |
|---|---|---|---|---|---|---|
| Administración / Autenticación | 0 | 6 | 10 | 0 | 16 | 0 |
| Vigilancia | 1 | 2 | 2 | 0 | 5 | 0 |
| Báscula | 2 | 16 | 9 | 1 | 28 | 0 |
| Bodega | 2 | 4 | 13 | 1 | 20 | 0 |
| Comercio Exterior | 0 | 9 | 11 | 2 | 22 | 0 |
| Facturación | 7 | 9 | 8 | 3 | 27 | 0 |
| Reportes | 0 | 0 | 7 | 0 | 7 | 0 |
| Transversal (seguridad, permisos, frontend, documentos, trazabilidad) | 3 | 6 | 13 | 0 | 22 | 0 |
| **Total** | **15** | **52** | **73** | **7** | **147** | **0** |

El módulo es el primero de la columna «Módulo» del índice. El total de MAJOR incluye la ficha unificada DEF-F8-001.

### 2.5 Tasa de reapertura

- **Fichas de la campaña:** 2 reabiertas de 125 re-testeadas (**1,6 %**). Las dos se corrigieron y se verificaron después.
  - DEF-F3-008 (S2): el conductor de báscula se reescribía; corregido con DEF-F11-008.
  - DEF-F7-007 (S3): el reporte por CPI perdía la anulada al refacturar; verificado en S4.
  - DEF-F5-003 quedó verificado en parte en S2 (faltaba el SMTP caído) y por completo en S3.
- **Fichas de la fase 11:** 0 reabiertas de 21 re-testeadas (DEF-F11-016 y 017 en S5; DEF-F11-018 y 019 en el re-test posterior a S5; DEF-F11-020 y 021 en staging, en el re-test posterior a S6).

## 3. Riesgos del plan maestro (§9): tabla final

★ = podía ser BLOCKER o CRITICAL. «Corregido y verificado» significa: confirmado en la campaña, corregido por el plan y verificado en la fase 11.

| Riesgo | Resultado final | Defecto(s) |
|---|---|---|
| R-ADM-01 ★ | Confirmado · corregido y verificado | DEF-F3-001 |
| R-ADM-02 | Confirmado · corregido y verificado | DEF-F10-005 |
| R-ADM-03 | Confirmado · corregido y verificado | DEF-F7-005, DEF-F9-004 |
| R-ADM-04 | Confirmado · corregido y verificado | DEF-F1-006 |
| R-ADM-05 | Confirmado (parcial) · corregido y verificado | DEF-F1-009 |
| R-ADM-06 | Confirmado · corregido y verificado | DEF-F1-007 |
| R-ADM-07 ★ | Confirmado (CRITICAL) · corregido y verificado | DEF-F9-001, DEF-F9-002 |
| R-ADM-08 | Confirmado · corregido y verificado | DEF-F0-003 |
| R-ADM-09 | Confirmado · corregido y verificado (Vigilancia solo ve Vigilancia; S4 F9-MEN-001) | DEF-F9-002 |
| R-ADM-10 | Confirmado en F0 · corregido (parámetros `COMPANY_*` sembrados) y verificado | DEF-F7-011 |
| R-ADM-11 | Confirmado · corregido y verificado | DEF-F7-010 |
| R-ADM-12 ★ | Confirmado (CRITICAL de seguridad) · corregido y verificado | DEF-F7-001 |
| R-ADM-13 | Confirmado · corregido y verificado | DEF-F1-011 |
| R-ADM-14 | Confirmado · observación sin ficha (OBS-F1-007): no hay pantalla de cambio voluntario de contraseña | — |
| R-ADM-15 | Confirmado · corregido y verificado | DEF-F7-008 |
| R-ADM-16 | Confirmado (vehículos); descartado (ubicaciones) · corregido y verificado | DEF-F1-005 |
| R-VIG-01 | Confirmado y agravado · corregido y verificado | DEF-F2-001 |
| R-VIG-02 | Confirmado en F11-S4 · corregido y verificado en S5 | DEF-F11-016 |
| R-VIG-03 ★ | Confirmado · corregido y verificado | DEF-F3-005 |
| R-VIG-04 | Confirmado · corregido y verificado (con R-TRZ) | DEF-F2-004, DEF-F7-002 |
| R-VIG-05 | Confirmado · corregido y verificado (el API valida las fechas) | DEF-F2-003 |
| R-BAS-01 ★ | Confirmado · corregido y verificado (también sin cliente). Efecto nuevo en S5 (el reporte diario omitía el cobro del principal), corregido y verificado en el re-test posterior a S5 | DEF-F3-011, DEF-F11-009, DEF-F11-010 · **DEF-F11-018** |
| R-BAS-02 ★ | Confirmado y agravado · corregido y verificado | DEF-F3-004 |
| R-BAS-03 ★ | Confirmado · corregido y verificado | DEF-F3-017 |
| R-BAS-04 | Confirmado · corregido y verificado | DEF-F3-008, DEF-F11-008 |
| R-BAS-05 | Confirmado · corregido y verificado | DEF-F3-007 |
| R-BAS-06 | Confirmado · corregido y verificado | DEF-F3-010 |
| R-BAS-07 | Confirmado · resuelto por la decisión D-2 (acción retirada) y verificado | DEF-F3-013 |
| R-BAS-08 | Confirmado · corregido y verificado | DEF-F3-013, DEF-F11-007 |
| R-BAS-09 | No verificable en la campaña · corrección de primer y segundo peso (CHG-37) verificada en S2 y S3, sin ficha | — |
| R-BAS-10 | No verificable (la acción «Cerrar ciclo» no está visible) | — |
| R-BAS-11 | No aplica (la búsqueda funciona) | — |
| R-BAS-12 ★ | Confirmado · corregido y verificado; descartado en el build corregido | DEF-F3-012 |
| R-BAS-13 | Resuelto por decisión (efectivo y cambio retirados de la UI y del API) y verificado | DEF-F3-019 |
| R-BAS-14 | Confirmado · corregido y verificado | DEF-F3-006 |
| R-BAS-15 | No verificable en F3 · fechas impresas en hora de Colombia (CHG-84) verificadas en S3, S4 y S5 (tiquete y Excel del historial). Confirmado en S5 en el reporte diario de báscula (columna «Hora» en UTC) · corregido y verificado en el re-test posterior a S5 | **DEF-F11-018** |
| R-BAS-16 | Parcial en F3 · **descartado** en S4: el mensaje de pesaje único de INSP es claro | — |
| R-BAS-17 | Parcial (no probado en la UI con datos cortos) · validaciones de CHG-53 verificadas en S3 | DEF-F3-009 |
| R-BOD-01 ★ | Confirmado · corregido y verificado (recepción directa en S1, S2 y S4) | DEF-F4-002 |
| R-BOD-02 ★ | Confirmado · corregido y verificado | DEF-F4-001 |
| R-BOD-04 | Confirmado · corregido y verificado | DEF-F4-005 |
| R-BOD-05 | Confirmado · corregido y verificado (recepción y corrección de CE) | DEF-F4-010, DEF-F11-014 |
| R-BOD-06 | Confirmado · corregido y verificado | DEF-F4-013, DEF-F4-017 |
| R-BOD-07 | Confirmado · corregido y verificado (advertencia) | DEF-F4-011 |
| R-BOD-08 | Confirmado · corregido y verificado | DEF-F4-012 |
| R-BOD-09 | Confirmado (límite) · corregido y verificado; las fotos huérfanas no son verificables sin forzar un rollback | DEF-F4-009 |
| R-CE-01 ★ | Confirmado · corregido y verificado (también con el SMTP caído) | DEF-F5-003, DEF-F5-004 |
| R-CE-02 | Confirmado · corregido y verificado | DEF-F5-008 |
| R-CE-03 ★ | Confirmado · corregido y verificado por completo (S4: manifiesto de un anulado) | DEF-F5-005, DEF-F11-012 |
| R-CE-04 | Confirmado · corregido y verificado | DEF-F5-006 |
| R-CE-05 ★ | Confirmado · corregido y verificado | DEF-F4-004 |
| R-CE-06 | Confirmado · **aceptado por decisión** (2-oct): «NACIONALIZADA» con cualquier levante | — |
| R-CE-07 | Confirmado · corregido y verificado | DEF-F5-013 |
| R-CE-08 | Confirmado · corregido y verificado (una factura por cliente; firma del conductor) | DEF-F8-002 |
| R-CE-09 | No verificable (el backend recalcula el vencimiento; S4: la guía vence a 3 días de tránsito) | — |
| R-CE-10 | Confirmado · observación sin ficha (GUI-014) | — |
| R-FAC-01 ★ | Confirmado · corregido y verificado | DEF-F6-003, DEF-F6-004 |
| R-FAC-02 ★ | Confirmado y agravado · corregido y verificado | DEF-F6-006 |
| R-FAC-03 ★ | Confirmado · corregido y verificado | DEF-F6-005 |
| R-FAC-04 ★ | Confirmado · corregido y verificado (comprobante hasta 5 MB, S4) | DEF-F6-010, DEF-F11-015 |
| R-FAC-05 | Confirmado · corregido y verificado | DEF-F6-014 |
| R-FAC-06 | Confirmado · corregido y verificado | DEF-F6-009 |
| R-FAC-07 | Confirmado · resuelto por la decisión D-1 y verificado | DEF-F6-017 |
| R-FAC-08 ★ | **Descartado** | — |
| R-FAC-09 | Confirmado · corregido y verificado | DEF-F6-016 |
| R-FAC-10 | Confirmado · corregido y verificado en sus dos partes (S4) | DEF-F7-007 |
| R-FAC-11 | Confirmado · corregido y verificado | DEF-F7-006 |
| R-FAC-12 | **Descartado** | — |
| R-FAC-13 | Confirmado · corregido y verificado | DEF-F6-011 |
| R-FAC-14 | Confirmado · resuelto por decisión (mínimo configurable) y verificado | DEF-F6-021 |
| R-FAC-15 | Confirmado · corregido y verificado | DEF-F1-004, DEF-F6-001 |
| R-FAC-16 | Confirmado · corregido y verificado | DEF-F6-013, DEF-F10-002 |
| Nuevo (recálculo de almacenamiento) | Confirmado en F11-S4 · corregido y verificado en S5 · descartado en staging (S6, F6-REC-002) | DEF-F11-017 |
| Nuevo (S6): recuperación de contraseña con el despliegue estático | Confirmado en staging (S6) · corregido y verificado en staging | DEF-F11-021 |
| Nuevo (S6): respaldos concurrentes | Confirmado en staging (S6) · corregido y verificado en staging | DEF-F11-020 |

**Riesgos ★ (18):**
- 17 confirmados con defecto, corregidos y verificados.
- R-FAC-08 descartado.
- Ningún ★ queda abierto. El efecto nuevo de R-BAS-01 en el reporte diario de báscula (DEF-F11-018, MAJOR, S5) quedó corregido y verificado.
- R-VIG-02 y el riesgo nuevo del recálculo, abiertos en S4, quedan corregidos y verificados en S5.
- R-BAS-15 y R-BAS-01, abiertos en S5 por el reporte diario de báscula, quedan corregidos y verificados en el re-test posterior a S5.
- Los dos nuevos de S6 (no ★), DEF-F11-021 y DEF-F11-020, quedan corregidos y verificados en staging. No queda ninguno abierto.

## 4. Defectos abiertos: impacto y recomendación

**No queda ninguna ficha abierta.** Las dos que abrió S6 (staging, FE `508b91b` / BE `b31ddb6`) se corrigieron y se verificaron en staging el 2026-10-07, tras redesplegar FE `8527144` / BE `84c712f` sin recrear la base (`evidencias/F11/RT-S6-redespliegue-retest.txt`):

| ID | Severidad | Corrección | Re-test en staging |
|---|---|---|---|
| [DEF-F11-021](defectos/DEF-F11-021.md) | MAJOR | FE `c46c1de`: el middleware normaliza la «/» final. BE `84c712f`: el `Caddyfile` sirve el `index.html` de la carpeta sin el 308 | `curl` sin sesión: `/auth/login`, `/auth/reset-password?token=abc` y `/auth/request-password-reset` → 200 sin redirección; el fallback y `/_nuxt/` responden. El enlace real del correo del Admin, abierto por el usuario en Chrome, mostró «Restablecer contraseña» y el cambio funcionó; el Admin entra con la contraseña nueva. F0-LOG-008: `qa.bodega` con `/auth/login` y `/auth/login/` → `/warehouse`. **Verificado** |
| [DEF-F11-020](defectos/DEF-F11-020.md) | MINOR | BE `57aef56`: candado `pg_advisory_xact_lock` al registrar la corrida y nombre `wms_{aaaammdd_hhmmss}_{id8}.dump` | Dos `POST backups/run` en paralelo → 202 y 409 «Ya hay un respaldo en curso.», una sola corrida. Dos corridas del mismo minuto → `…_010602_f50ba535` y `…_010607_d374a8d6`, cada una con su `.dump` y su `.tar.gz`; `pg_restore --list` 705. **Verificado** |

La observación **O-3** (BE `57aef56`) también quedó verificada: el «por facturar» de báscula de QSR301 con `qa.bascula` responde `totalAmount` 20000.00 (antes 19999.9968) y la factura queda en $20.000.

Las que abrió S5 se corrigieron y se verificaron en el re-test posterior a S5 (FE `24d742d` / BE `f6f1828`, local):

| ID | Severidad | Corrección | Re-test |
|---|---|---|---|
| [DEF-F11-018](defectos/DEF-F11-018.md) | MAJOR | BE `f6f1828`: el reporte diario de báscula da una fila por tiquete, resuelve el destinatario e imprime la hora de Colombia | F3-RPT-001 del 06/10: 30 filas para 29 ciclos. QAK402 sale en dos filas (29.750 del principal y 0 del adicional). «TOTAL FACTURADO» $ 843.980, igual a la suma de las facturas BASCULA del día (30 · 843.980). 2026T00061 sale a nombre de «Consumidor Final» y 2026T00044 a nombre de la persona no registrada. La hora es 10:56 en 2026T00050 y 11:08 en 2026T00061. **Verificado** |
| [DEF-F11-019](defectos/DEF-F11-019.md) | MINOR | FE `24d742d`: la columna «Estado depósito» y el filtro leen `warehouseStorageStatus` | F3-CIC-001: 2026T00050 muestra 2026BA00027 «Cerrado». El filtro «Cerrado» deja la fila y «Abierto» queda vacío. **Verificado** |

DEF-F11-016 y DEF-F11-017, abiertos en S4, quedaron verificados en S5 sobre BE `00d6ac3` (`F11-informe-S5-2026-10-06.md` §4.1 y §4.2).

## 5. Tiempos de báscula frente a la meta

| Medida | Resultado | Meta |
|---|---|---|
| Latencia del sistema registro + cobro + peso (F3-PES-015, automatización) | ≈ 90 ms (F3, 2-oct) | — |
| **PRF-002** · registro en báscula con el operario | **Pendiente: lo mide un operario.** El escenario está listo en staging: camión QSP001 con transportadora y conductor migrados (`F11-informe-S6-2026-10-06.md` §4.7, con la hoja de tiempos) | **Registro en báscula en 30 s o menos** (referencia legacy ≈ 30 s del ciclo) |
| Latencia del sistema en staging (S6, automatización) | Registro IMP 1,15 s; cobro 0,57 s; confirmación con la DIAN 0,65 s | — |
| F3-REG-024 y F3-PES-015 · tiempo del operario | Requieren medición presencial (F1-09) y quedan con PRF-002 | Igual que PRF-002 |

## 6. Decisiones de negocio pendientes que salieron del QA

**Resueltas durante la campaña** (se aplicaron y verificaron):
- Efectivo y cambio en báscula: retirados.
- Mínimo antes o después de IVA: configurable.
- Etiqueta «NACIONALIZADA» con levante parcial: sí.
- Vigilancia en Bodega: no.
- D-1 (consolidación) y D-2 (modo de pago).
- OnDemand: retirado.
- Datos de empresa: los del legacy.
- Ingresos diarios: solo Confirmados y Cerrados.

**Siguen abiertas:**
1. **Ciclo quincenal de 14 frente a 15 días:** el levantamiento dice «cada 15 días» y el código usa 14. Sigue como observación sin confirmar.
2. **Guía de una orden multicliente:** «una factura por cliente; validar contra el legacy» (decisión del 3-oct). Falta el cotejo con un caso real del legacy.
3. **Total de la guía editable por API:** el API acepta un total distinto del que propone la vista previa. Decidir si Comercio Exterior puede cambiarlo, como el total de báscula, o si debe ser fijo.
4. **Observaciones clasificadas como backlog** (detalle en el informe de S4, §4.4 y §4.5):
   - descarte sin movimiento en el kárdex;
   - filtro por carta porte del depósito adicional;
   - PUT de terceros que no permite retirar uno;
   - unidades mezcladas en el resumen de Bodega;
   - «Manifiesto» por «carta porte» en el kárdex;
   - `PerWeighbridgeCycle` en el API;
   - saldo del diálogo tras un pago rechazado;
   - etiqueta de «Buscar por placa»;
   - título «Recurso duplicado.».
5. **Observaciones de S5 clasificadas como backlog** (detalle en el informe de S5, §4.6):
   - el «Detalle» de la factura omite un producto agotado tras un recálculo, aunque la línea lo sigue cobrando;
   - por API: registro de báscula sin tipo de documento y el segundo camión que agrega terceros documentales;
   - el registro con unidades de carga por API ignora la cantidad de la línea;
   - no se puede eliminar en CE una línea que entró por báscula (confirmar con el negocio);
   - el filtro «Manifiesto» de importaciones no busca el manifiesto DIAN;
   - el aviso de anulación de una factura sin número no nombra el depósito;
   - el enlace de «Cartera pendiente» del tablero abre solo las Enviadas;
   - el historial de báscula muestra «Sin cliente asignado» en un cobro a Consumidor final.

## 7. Recomendación go/no-go para el corte del legacy

**Veredicto (local S0–S5 + staging S6 con datos migrados y su re-test): GO condicionado solo a PRF-002 (medición con un operario).** Sin fichas abiertas.
- **Staging (S6 y re-test posterior):** sin FALLA en P0 y **sin fichas abiertas**. DEF-F11-021 (MAJOR) y DEF-F11-020 (MINOR), abiertas en S6, quedaron corregidas y verificadas en staging con FE `8527144` / BE `84c712f` (§4).

**Base del veredicto en local (build FE `24d742d` / BE `f6f1828`):**
- El criterio de salida «cero BLOCKER y cero CRITICAL abiertos» **se cumple**.
- El resto del criterio también se cumple:
  - suite REG completa sin FALLA en P0 (REG-005, 006 y 021 re-ejecutados en S5 sobre `00d6ac3`);
  - 232/232 P0 re-ejecutados;
  - **145 de 145 fichas verificadas** en local, sin reabiertas ni abiertas; con las dos de S6, verificadas en staging, son **147 de 147**;
  - pruebas automatizadas en verde (S4).
- DEF-F11-018 (MAJOR) y DEF-F11-019 (MINOR), abiertos por S5, quedaron corregidos y verificados (§4).

**Condición para pasar a GO:**
1. **PRF-002** con un operario: registro en báscula en 30 s o menos (incluye F3-REG-024 y F3-PES-015).

**Cumplidas en S6:**
- **Bloque de staging sin FALLA en P0:** F0 completo, F11-REG-001 a 013, E2E-01, la DIAN real y el humo (`F11-informe-S6-2026-10-06.md`).
- **Anexo A cumplido en local y en staging:**
  - fases 1 y 3 del plan de migración: `docs/planes/migracion-staging/resultados/informe-fase-1-repeticion.md` e `informe-fase-3.md`;
  - FA-MIG-009 por rol, DEF-MIG-005/007/008 y la factura de un migrado en S6.

**Cumplido después de S6:** DEF-F11-021 corregida, con la recuperación de contraseña y F0-LOG-008 re-ejecutadas en staging, y DEF-F11-020 verificada.

**Nota: 130 P1 aceptados con cobertura indirecta.** Siguen sin ejecución por ID 130 P1 de F0 (8), F1 (52), F2 (21), F4 (16), F7 (12), F9 (14) y F10 (7). Se aceptan con cobertura indirecta:
- el RET de las 145 fichas;
- la suite REG;
- los 232 P0 re-ejecutados;
- las pruebas automatizadas: 1874 + 266 en S4, más las nuevas de `00d6ac3`, `f6f1828` y `24d742d`.

Los P1 de Báscula, Comercio Exterior y Facturación se ejecutaron por ID en S5: 115 de 117, con 2 diferidos a staging.

## 8. Pendiente para staging

**S6 (2026-10-06/07, staging con datos migrados, FE `508b91b` / BE `b31ddb6`) ejecutó el bloque.** Detalle en `F11-informe-S6-2026-10-06.md`. Solo queda lo que mide un operario.

| Bloque | Casos | Estado tras S6 |
|---|---|---|
| **PRF-002** | Cronometraje del registro en báscula con el operario, con **F3-REG-024 y F3-PES-015** | **Pendiente: lo mide un operario.** Criterio: registro en báscula en 30 s o menos, desde seleccionar el camión hasta guardar un IMP mínimo con datos precargados; anotar también el tiempo hasta el primer peso. Escenario listo: camión **QSP001** en la cola, con transportadora y conductor migrados, datos de la ficha y hoja de tiempos en el informe S6 §4.7. |
| F0 completo (37) | F0-DIS, LOG, NAV, API, ENV | **Ejecutado:** 35 PASA, 1 no aplica (Swagger apagado), 1 FALLA P2 (F0-LOG-008, DEF-F11-021), que **pasa en el re-test posterior a S6**. |
| F11-REG-001 a 013 (13) | Camino crítico | **Ejecutado:** 13 PASA. REG-004, con la equivalencia PAPELERIA para no tocar la tarifa T3 de BASCULA. |
| E2E-01 (1) | Importación completa | **Ejecutado: PASA** (2026BA00001). Montacargas tras configurar tarifas de prueba (autorización del usuario). |
| Diferencias propias de staging | Correo real, Swagger, respaldos | **Ejecutado.** El correo sale solo a direcciones del usuario (CE-7, aviso al Admin y recuperación del Admin); la recuperación por correo solo existe para el Admin (CHG-51). Swagger apagado. FB-BAK-003 en serie PASA y en concurrencia FALLA (DEF-F11-020). FB-BAK-005 PASA en una base aparte. El enlace de recuperación falla (DEF-F11-021). **Re-test posterior a S6: DEF-F11-020 y DEF-F11-021 verificados.** La corrida programada de las 02:00 no se alcanzó: queda para la Fase 5 (configuración y job activos). |
| Consulta real a la DIAN | F6-TRM-001 | **Ejecutado: PASA.** DIAN 361 ms, confirmación 650 ms, TRM 3.209,78 `Dian` con la fecha de ingreso. |
| Humo de las últimas correcciones | F2-COR-011, F6-REC-002, F3-RPT-001, F3-CIC-001 | **Ejecutado:** 4 PASA. |
| Migración desde la operación (Anexo A) | FA-MIG-009 por rol, DEF-MIG-005/007/008, factura de un migrado | **Ejecutado:** todo PASA. Abandono 67, la cifra correcta del conjunto v3. |

## Anexo — Fuentes

- Fichas: `docs/qa/resultados/defectos/` (índice en `INDICE.md`).
- Evidencias de la fase 11: `docs/qa/resultados/evidencias/F11/` (S0 a S5 y re-test posterior a S5: `RT-DEF-F11-018-019.txt`, `RT-DEF-F11-018-reporte-diario-2026-10-06.pdf` y `RT-DEF-F11-019-*.jpg`).
- Datos: `docs/qa/resultados/registro-datos-qa-f11.md`.
- Palancas usadas en la fase 11, solo en la base local: `f11_palanca_mora_s0.sql`, `f11_palanca_s1.sql`, `f11_palanca_s3.sql` y `f11_palanca_s5.sql` (abandono y jobs de facturación, restaurada). En S4 y en el re-test posterior a S5 no se usaron palancas.
- Inventario de los P1 de F3, F5 y F6 ejecutados en S5: `F11-S5-inventario-P1.md`.
- **S6 (staging):** `F11-informe-S6-2026-10-06.md` y evidencias `evidencias/F11/S6-*`. En staging no hubo SQL de escritura ni palancas.
- **Re-test en staging posterior a S6** (DEF-F11-020, DEF-F11-021 y O-3, FE `8527144` / BE `84c712f`): `evidencias/F11/RT-S6-redespliegue-retest.txt`. Datos creados: el camión QSR301 («Solo báscula», tiquete 2026T00009, factura de báscula en Borrador por $20.000) y cinco respaldos manuales.
- **Migración:** `docs/planes/migracion-staging/` (plan, informes de las fases 1 a 3 y fichas DEF-MIG).
