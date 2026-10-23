# Estado del proyecto

> **Para qué sirve:** qué está hecho, qué hay en staging, qué falta y qué decisiones siguen abiertas.
> **Fecha de corte:** 2026-10-23. Backend `develop` `35a61b2`, frontend `develop` `c924a8b`.
> **Mantenimiento:** actualiza este documento al cerrar un trabajo que cambie el estado general (`procesos/flujo-de-trabajo-agentes.md` §7). Cambia la fecha de corte y no borres el historial de hitos.

## 1. Resumen

El WMS está **en pruebas en staging con los operarios**, sobre los datos migrados del sistema legacy.

- La campaña QA terminó en **GO condicionado solo a PRF-002**, la medición con un operario de que la báscula registra un camión en ≤ 30 s (`qa/resultados/informe-final.md`).
- Toda la funcionalidad planeada está implementada: Olas 1–3, paridad con el legacy, correcciones de QA, migración, selector de conductor y video tutoriales.
- Los permisos por usuario quedaron diferidos para después del corte (`DEC-030`).

## 2. Hitos

| Fecha | Hito | Cierre (BE / FE) |
| --- | --- | --- |
| 2026-09-15 | **Ola 1** (R01–R04): stock declarado, varios camiones, TRM fuera de báscula, saldos de guía, consecutivos, destinatario y acciones de factura, IVA del montacargas, búsqueda de terceros | `3332eac` / `0c02d3f` |
| 2026-09-17 → 20 | **Ola 2** (R05–R06): fechas operativas, unidad de carga, unidades de medida y embalaje, datos de recepción | `3bfbd6d` / `e06977d` |
| 2026-09-22 → 23 | **Ola 3** (R07–R11): báscula rápida, etiqueta, orden de cargue simplificada, edición de productos, búsqueda, tarifas mínimas | `b450fba` + `b089d2b` / `26aed68` |
| 2026-09-29 → 10-01 | **Paridad legacy, backend** (fases 1–6) y migración inicial única `InitialParityLegacy` | `bf64de1` + `83d784f` |
| 2026-10-01 → 02 | **Paridad legacy, frontend** (fases 1–7) | `d690f25` |
| 2026-10-02 → 03 | **Campaña QA** F0–F10 | FE `cd121d8` |
| 2026-10-03 → 05 | **Plan de corrección** de defectos: 12 fases, CHG-01…90 | `09b0baf` / `4074c63` |
| 2026-10-05 → 06 | **QA F11** (re-test, S0–S5): GO condicionado | `f6f1828` / `24d742d` |
| 2026-10-06 → 07 | **Migración del legacy a staging** (fases 1–5) y QA S6 en staging | `5bcdbd8`; fixes S6 `84c712f` / `8527144` |
| 2026-10-08 | **Selector de conductor**, verificado en staging | `044be08` / `4ca4e0a` |
| 2026-10-08 → 09 | Fixes tras el despliegue, producción de videos (F1–F7) y centro de ayuda | `74e16f3` / `146e26d` |
| 2026-10-23 | Hub de documentación (`docs/`, repo propio) | `35a61b2` / `c924a8b` |

## 3. Staging

- **URLs:** frontend `https://app.100-60-89-139.sslip.io`, API `https://api.100-60-89-139.sslip.io/api/v1` (AWS Lightsail). Cómo desplegar: `procesos/despliegue-staging.md`.
- **Último despliegue registrado:** 2026-10-08, BE `044be08` / FE `4ca4e0a`, con 11 migraciones aplicadas. Respaldos previos: `wms_20261008_151727_77114401.dump` y `wms_20261008_154700_53e8fdc1.dump`.
- **Datos:**
  - depósitos vivos migrados del legacy (corte simulado al 2026-09-30, `DEC-040`);
  - operaciones de QA S6 sobre BA0042 y BA0558, conservadas como ejemplo;
  - datos de práctica `PRAC-` (P1–P6; el P6 está reservado para PRF-002);
  - conductores `QA-SEL` y vehículos `QSL801`–`803`.
- **Cuentas:** `operario.<rol>` (cambio obligatorio al primer ingreso) y `qa.<rol>`. Las credenciales están en `db_legacy/trabajo/`; no las copies.
- **Respaldos:** diarios a las 02:00 en `/opt/wms/backups`. Punto «listo para operarios»: `wms_20261007_020011_a564692e.dump`.

**Commits posteriores al último despliegue registrado** (según los registros, no están en staging):

| Repo | Commit | Contenido |
| --- | --- | --- |
| BE | `83de58a` | Eliminar productos declarados sin movimientos; camión con el que se inicia el montacargas; recepción informativa con todos los camiones. **Trae la migración `20261008230241_AddForkliftUseEntryLog`** |
| BE | `2eeaaad` | Producto y cantidad en el historial de guías; cambiar el modo de pago de la guía; anular un pesaje por repesar; unidad de carga al crear la orden |
| BE | `74e16f3` | CORS del bucket del centro de ayuda |
| BE | `31b9acc` | Guiones; además cambia `scripts/deploy-staging.sh` (`AYUDA_BASE_URL`) |
| FE | `f686f63`, `7ef72da`, `676ecb2`, `704dcef` | Contraparte de los fixes del 08-oct |
| FE | `0091e53`, `5a063a3`, `146e26d` | Página `/ayuda` y su rediseño |

## 4. Pendientes

| # | Pendiente | Dónde está documentado | Notas |
| --- | --- | --- | --- |
| 1 | **PRF-002:** cronometrar la báscula con un operario (≤ 30 s), junto con F3-REG-024 y F3-PES-015. Es también el F1-09 del plan frontend de paridad | `qa/resultados/informe-final.md` («Condición para pasar a GO»); `qa/resultados/SEL-informe-2026-10-08.md` | Única condición para el GO. Debe medirse con el build desplegado, que incluya el selector de conductor |
| 2 | Desplegar en staging los commits del §3 (incluye una migración y el centro de ayuda) | §3 | Ver «Por confirmar» |
| 3 | DEF-F11-023, 024 y 026 (MINOR, «Nuevo») del selector de conductor | `qa/resultados/defectos/INDICE.md` | Se desplegaron con ellos por decisión del usuario |
| 4 | Guía de operarios: falta el canal de reporte y los avisos del selector (QA-SEL, DEF-F11-023/024) | `planes/migracion-staging/resultados/guia-pruebas-operarios.md`; `informe-fase-5.md`; `SEL-informe` §S.8 | |
| 5 | Decidir si se desactivan las cuentas `qa.*` en staging | `planes/migracion-staging/resultados/informe-fase-5.md` | |
| 6 | Vaciar o anonimizar staging al terminar las pruebas (tiene datos reales) | `planes/migracion-staging/plan-migracion-legacy-staging.md` | |
| 7 | **Corte real:** volcado nuevo del legacy y repetir las fases 1 y 3 de la migración | `planes/migracion-staging/plan-migracion-legacy-staging.md` | |
| 8 | **FOB/CIF de la migración:** la mecánica numérica funciona, pero la equivalencia de conceptos no está validada | `analisis/revision-fob-cif-migracion-v2-2026-10-08.md` | No dar la migración de FOB/CIF por cerrada |
| 9 | Dar de baja el ambiente Azure `test` cuando el cliente valide staging | `Backend/wms-api/infra/` | |
| 10 | Video tutoriales: F7 entregada para revisión; etiquetas de Trazabilidad en inglés (H1) | `videos/guiones/plan-produccion-videos.md` | |
| 11 | Permisos por usuario | `planes/plan-cerrado-permisos-por-usuario-2026-10-07.md` | **Diferido** después del corte |

**Documentos con estado atrasado** (no son trabajo pendiente del sistema, solo de documentación):

- `planes/paridad-legacy/plan-backend-paridad-legacy.md` marca la fase 6 «falta E19». La prueba con datos reales se hizo en la migración (`planes/migracion-staging/resultados/informe-fase-1-repeticion.md`). Además, su mensaje de commit de documentación quedó sin commitear.
- La cabecera de `qa/plan-correccion-defectos.md` dice «propuesto», pero sus 12 fases están completadas.
- `qa/resultados/informe-final.md` dice «147/147»; hoy son 150 fichas verificadas y 3 nuevas.
- La ficha `DEF-MIG-007` sigue en «Corregido», aunque el plan de migración lo da por verificado en staging.

## 5. Defectos

| Origen | Total | Estado |
| --- | --- | --- |
| Campaña QA (`DEF-F*`) | 153 fichas: CRITICAL 16, MAJOR 52, MINOR 77, TRIVIAL 7, 1 duplicada | 150 verificadas, 3 nuevas (DEF-F11-023, 024 y 026) |
| Migración (`DEF-MIG-*`) | 8 | 001–006 y 008 verificadas; 007 verificada según el plan (ficha atrasada) |

Los defectos nuevos siguen en `DEF-F11-028` y `DEF-MIG-009` (`procesos/qa-y-defectos.md`).

## 6. Decisiones de negocio abiertas

| Tema | Pregunta | Mientras tanto |
| --- | --- | --- |
| Prorrateo del almacenamiento | ¿Las renovaciones cobran el CIF completo o el proporcional al saldo? | Conviven `PERCENTAGE_OF_VALUE` y `PERCENTAGE_OF_VALUE_PRORATED`; se elige al configurar (`DEC-025`) |
| Mínimos de almacenamiento (WMS-32) | ¿El mínimo de importación es $184.000 con 0,255 %? (El umbral de $72.156.863 = $184.000 ÷ 0,255 %.) | Los mínimos son configurables, con o sin IVA (`minimumIncludesVat`). Para la migración se aprobó T1/T2 (`DEC-041`) |
| FOB/CIF del legacy | ¿Qué dato del legacy equivale al CIF del v2? | Ver pendiente 8 |

Ya resueltas, aunque documentos antiguos las den por abiertas:

- **WMS-30:** la unidad de carga es un concepto propio (`DEC-014`).
- **WMS-18/27:** unidad y embalaje se imprimen por separado (`DEC-015`).
- **WMS-17:** la orden de cargue se conserva y registra la orden externa (`DEC-016`).
- **WMS-33:** el período cuenta desde el ingreso (`DEC-012`).
- **Quincenal de 14 o 15 días:** existen ambos ciclos.

## 7. Por confirmar con el usuario

No se pudieron confirmar desde el código ni los documentos:

- Si hubo despliegues a staging después del 2026-10-08 que no quedaron registrados (los del §3).
- Si los 81 videos ya están publicados en el bucket del centro de ayuda y si el usuario aprobó la serie F7.
- Si los fixes del 2026-10-08 (`83de58a`/`2eeaaad`, `704dcef`…) pasaron por QA.
