# Estado del proyecto

> **Para qué sirve:** qué está hecho, qué hay en staging, qué falta y qué decisiones siguen abiertas.
> **Fecha de corte:** 2026-10-27. Backend `develop` `911399c`, frontend `develop` `33fbeba`, desplegados en staging el 2026-10-27 (fase 13 del plan P1). Las secciones §1 a §4 describen el estado del 2026-10-23 más los hitos y commits del plan de brechas P1, de `DEC-029`, de `DEC-057` y de `DEC-058`, el despliegue de la fase 13 (§2 y §3) y el reinicio limpio de staging de `DEC-043` (fase 4, 2026-10-27).
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
| 2026-10-23 | Hub de documentación (`docs/`, repo propio) y `AGENTS.md`/`CLAUDE.md` en cada repo | `b27c9bf` / `31da26c` |
| 2026-10-24 | **Plan de brechas P1** (fases 1 a 12; fase 13 pendiente): 20 brechas de la auditoría de paridad más 5 colaterales y el QR de verificación de la guía (`DEC-060`); 4 migraciones; QA local en `qa/resultados/P1-informe-2026-10-24.md` (GO con condiciones; DEF-F11-028 corregido y verificado en local, BE `9e399de`) | BE `560f558` / FE `e2e11e6` (fases 1 a 11; la 12 es solo de documentación) |
| 2026-10-25 | **DEC-029 construido** (3 fases): levante rotulado CIF, «Valor de la mercancía» en el depósito y las fórmulas (migración `RenameValueFormulaLabels`), valor del levante una sola vez (409) que pasa al siguiente producto al retirar, y fórmula prorrateada preseleccionada en almacenamiento; verificado en local. Sin desplegar en staging; los videos que quedan desactualizados están en `videos/videos-desactualizados-dec-029.md` | `dafd573` / `d838535` |
| 2026-10-26 | **DEC-057 construido** (6 fases): el operario elige el depósito de la carta porte, manifiesto obligatorio en Báscula y DIAN al confirmar la importación, pesos del legacy (tara y mercancía según manifiesto), báscula en $0 por convenio, tarjeta como el legacy y por camión (migración `AddLabelPrintEntry`) y cambio de destinatario de la factura; verificado en local. Sin desplegar en staging; nota para operarios en `manuales/nota-operarios-hallazgos-2026-10-26.md` y videos por regrabar en `videos/videos-desactualizados-dec-057.md` | `a8d06dd` / `18f79f1` |
| 2026-10-27 | **Fase 13 del plan P1: despliegue y QA en staging.** 7 migraciones aplicadas, destino de respaldo externo `s3-externo` y QR de la guía verificados con celular; QA en staging con 21 PASA y 1 no ejecutado, sin defectos (`qa/resultados/PRE-informe-2026-10-25.md` §13). Veredicto: listo para el reinicio limpio de `DEC-043` | `911399c` / `33fbeba` |
| 2026-10-27 | **Staging limpio (`DEC-043`, fase 4):** base recreada con 19 migraciones y el legacy migrado de nuevo con la herramienta actual (conjunto v4, corte en el 2026-10-26), con conteos idénticos al ensayo local; tarifas T1 a T4 y de montacargas; 5 cuentas `operario.*`; respaldos `local-staging` y `s3-externo`; sin datos de QA ni de práctica. Convenios y `open-billing` quedan para la fase 4b (`planes/migracion-staging/resultados/informe-staging-limpio-fase-4.md`) | `911399c` / `33fbeba` (sin cambios de código) |

## 3. Staging

- **URLs:** frontend `https://app.100-60-89-139.sslip.io`, API `https://api.100-60-89-139.sslip.io/api/v1` (AWS Lightsail). Cómo desplegar: `procesos/despliegue-staging.md`.
- **Último despliegue registrado:** 2026-10-27 (fase 13 del plan P1), BE `911399c` / FE `33fbeba`. Migraciones aplicadas: las 7 del plan P1, `DEC-029` y `DEC-057` (`AddStakeholderExitBlock`, `FixAgreementActiveStakeholderIndex`, `AddWarehouseStorageLegacyYear`, `AddGuideCodeTypeParameter`, `RelaxServicePriceActiveIndex`, `RenameValueFormulaLabels` y `AddLabelPrintEntry`), en unos 4,5 s; quedan 19 en el historial. `AddForkliftUseEntryLog` (BE `83de58a`) ya estaba aplicada. Respaldo previo: `wms_20261027_100805_b2d8dade.dump`. Detalle en `qa/resultados/PRE-informe-2026-10-25.md` §13. Antes: 2026-10-08, BE `044be08` / FE `4ca4e0a`.
- **Reinicio limpio (`DEC-043`, fase 4, 2026-10-27):** `pgdata` recreado y migraciones aplicadas desde cero (19), sin desplegar código. Respaldo «antes del reinicio»: `wms_20261027_115925_b88fdf98.dump` (conserva los datos de QA y de práctica anteriores). Los archivos subidos de antes están en `/opt/wms/data/uploads-antes-reinicio-20261027`.
- **Datos:**
  - los maestros y los 128 depósitos vivos del legacy (`backupBodegas.sql`, junio de 2024), cargados con la herramienta actual (conjunto v4, con prórroga y año del depósito); corte simulado en el 2026-10-26, así que la facturación de los migrados arranca el 2026-10-27;
  - tarifas T1 (base: `PERCENTAGE_OF_VALUE` al 0,295 %, porque Facturación no fijó otra), T2 a T4 y las cinco de montacargas;
  - **sin convenios y sin `open-billing`**: los depósitos migrados no tienen factura de almacenamiento hasta la fase 4b (S11);
  - sin operaciones, sin datos de QA (`QA-…`) y sin datos de práctica (`PRAC-…`). Lo que aparezca después lo crean los operarios.
- **Cuentas:** `admin` y las 5 `operario.<rol>`, con cambio obligatorio al primer ingreso. No hay cuentas `qa.*`. Las credenciales están en `db_legacy/trabajo/`; no las copies.
- **Respaldos:** diarios a las 02:00 en dos destinos activos: `local-staging` (`/opt/wms/backups`) y `s3-externo` (bucket privado de Lightsail en `us-east-2`, prefijo `staging`), con correo de fallo a los Admin y a `Notifications:AdminEmails` (verificados de nuevo el 2026-10-27, después del reinicio). Punto «listo para operarios v2»: `wms_20261027_134951_bf7bf952.dump`, que reemplaza al `wms_20261007_020011_a564692e.dump` de `DEC-042`.

**Commits posteriores al último despliegue registrado:** ninguno. BE `911399c` y FE `33fbeba` están en staging desde el 2026-10-27; los commits que se listaban aquí (los fixes del 08-oct, el centro de ayuda, el plan de brechas P1, `DEC-029`, `DEC-057` y `DEC-058`) quedaron desplegados.

## 4. Pendientes

| # | Pendiente | Dónde está documentado | Notas |
| --- | --- | --- | --- |
| 1 | **PRF-002:** cronometrar la báscula con un operario (≤ 30 s), junto con F3-REG-024 y F3-PES-015. Es también el F1-09 del plan frontend de paridad | `qa/resultados/informe-final.md` («Condición para pasar a GO»); `qa/resultados/SEL-informe-2026-10-08.md` | Única condición para el GO. Debe medirse con el build desplegado, que incluya el selector de conductor |
| 2 | ~~Desplegar en staging los commits del §3~~ **Hecho el 2026-10-27** (fase 13 del plan P1): BE `911399c` / FE `33fbeba`, 7 migraciones (la 8.ª, `AddForkliftUseEntryLog`, ya estaba), respaldo externo y QR verificados; QA en staging sin defectos | §3; `qa/resultados/PRE-informe-2026-10-25.md` §13; `planes/registro-ejecucion-brechas-p1-2026-10-24.md` «Fase 13» | Sigue el reinicio de `DEC-043` (pendiente 8c) |
| 3 | DEF-F11-023, 024 y 026 (MINOR, «Nuevo») del selector de conductor | `qa/resultados/defectos/INDICE.md` | Se desplegaron con ellos por decisión del usuario |
| 4 | ~~Guía de operarios~~ **Actualizada el 2026-10-27** con el reinicio (`DEC-043`): cuentas por rol, sin escenarios de práctica, avisos, nota de `DEC-057`/`DEC-058` y PRF-002 con un camión del operario. Canal de reporte: WhatsApp al responsable de las pruebas (2026-10-27) | `planes/migracion-staging/resultados/guia-pruebas-operarios.md`; `informe-fase-5.md`; `SEL-informe` §S.8 | |
| 5 | ~~Decidir si se desactivan las cuentas `qa.*` en staging~~ **Cerrado el 2026-10-27:** el reinicio de `DEC-043` no las creó | `planes/migracion-staging/resultados/informe-fase-5.md` | |
| 6 | Vaciar o anonimizar staging al terminar las pruebas (tiene datos reales) | `planes/migracion-staging/plan-migracion-legacy-staging.md` | |
| 7 | **Corte real:** volcado nuevo del legacy y repetir las fases 1 y 3 de la migración, **con el congelamiento y el conteo de operaciones abiertas (C1 a C9) como paso 0** | `planes/migracion-staging/plan-migracion-legacy-staging.md`; `planes/migracion-staging/procedimiento-corte-operaciones-abiertas.md` (escrito el 2026-10-24, sin ensayar) | El CSV de depósitos trae ahora `prorroga` y el de levantes `anio_deposito` (BR-08-003 y BR-08-005): regenerar las consultas de F6-03 |
| 8 | **Tarifas de almacenamiento (`DEC-029`, 2026-10-25), para Facturación:** validar los acuerdos calibrados por cliente y fijar la tarifa base prorrateada que reemplaza T1; después, un mes de facturación en paralelo antes de producción | `analisis/analisis-fob-cif-legacy-v2-2026-10-24.md` §7; `contexto/decisiones.md` DEC-029 | Staging sigue facturando con T1 a los clientes sin acuerdo. El reinicio del 2026-10-27 no cargó convenios: la hoja validada no ha llegado, y van en la fase 4b de `DEC-043` |
| 8b | **Hallazgos de los operarios (`DEC-057`) y ajustes visuales (`DEC-058`), 2026-10-26:** DEC-057 construido y verificado en local (BE `a8d06dd`, FE `41a17e1`). El plan `planes/plan-cerrado-correccion-dec-057-2026-10-26.md` también está ejecutado y verificado en local: la corrección de la revisión (Guardar durante la búsqueda de la carta porte, camiones anulados y tolerancia mixta; BE `7189676`, FE `543502d`), las páginas uniformes (FE `3d4056b`), el panel de báscula (FE `1fbcc8a`) y el tablero de depósitos (BE `911399c`, FE `e1e871a`); sus docs y casos QA en docs `9bc748c`. La validación del 2026-10-26 dejó 10 hallazgos de frontend (R1–R10 del §7 del plan), corregidos y verificados en local el mismo día con `planes/plan-cerrado-correccion-validacion-dec-058-2026-10-26.md`: FE `345cc44` (báscula, R1–R6) y FE `a0db12b` (páginas, R7, R8 y R10; docs `6e20684`), con sus casos QA; validados sin hallazgos nuevos. Desplegado en staging el 2026-10-27 (fase 13). Falta: enviar la nota a los operarios después del reinicio de `DEC-043` y regrabar los videos (`DEC-057` y `DEC-058`). PRF-002 se mide con la báscula de `DEC-058` (cola y panel) | `planes/plan-cerrado-dec-057-hallazgos-operarios-2026-10-26.md` §8; `planes/plan-cerrado-correccion-dec-057-2026-10-26.md` §7; `manuales/nota-operarios-hallazgos-2026-10-26.md`; `videos/videos-desactualizados-dec-057.md` §5 | Va **antes** de abrir staging a los operarios |
| 8c | **Staging limpio para los operarios (`DEC-043`, 2026-10-27):** después de la QA de la fase 13, staging se recrea y se migra de nuevo el legacy con la herramienta actual, con convenios calibrados que valida Facturación, cuentas `operario.*` por rol y sin datos de QA ni de práctica. **Fase 4 hecha el 2026-10-27:** staging recreado y cargado, con tarifas, cuentas y respaldos, sin convenios ni `open-billing`. Falta la fase 4b, cuando Facturación devuelva la hoja validada | `planes/plan-cerrado-staging-limpio-legacy-2026-10-27.md`; `planes/migracion-staging/resultados/informe-staging-limpio-fase-4.md` | Los operarios ya pueden entrar, con la guía y la nota de `DEC-057`/`DEC-058` |
| 9 | Dar de baja el ambiente Azure `test` cuando el cliente valide staging | `Backend/wms-api/infra/` | |
| 10 | Video tutoriales: F7 entregada para revisión; etiquetas de Trazabilidad en inglés (H1) | `videos/guiones/plan-produccion-videos.md` | |
| 11 | Permisos por usuario | `planes/plan-cerrado-permisos-por-usuario-2026-10-07.md` | **Diferido** después del corte |

Los documentos con estado atrasado se pusieron al día el 2026-10-23: la fase 6 del plan backend de paridad (E19 cumplida), la cabecera del plan de corrección, el informe final de QA (153 fichas) y la ficha `DEF-MIG-007` (verificada).

## 5. Defectos

| Origen | Total | Estado |
| --- | --- | --- |
| Campaña QA (`DEF-F*`) | 154 fichas: CRITICAL 16, MAJOR 53, MINOR 77, TRIVIAL 7, 1 duplicada | 151 verificadas, 3 nuevas (DEF-F11-023, 024 y 026) |
| Migración (`DEF-MIG-*`) | 8 | 8 verificadas |

**DEF-F11-028** (MAJOR, «Depósitos pendientes» omite el depósito agotado con factura por numerar) la encontró el QA local del plan P1; se corrigió en BE `9e399de` y quedó verificada en re-test local el 2026-10-24. Los defectos nuevos siguen en `DEF-F11-029` y `DEF-MIG-009` (`procesos/qa-y-defectos.md`).

## 6. Decisiones de negocio abiertas

| Tema | Pregunta | Mientras tanto |
| --- | --- | --- |
| Mínimos de almacenamiento (WMS-32) | ¿El mínimo de importación es $184.000 con 0,255 %? (El umbral de $72.156.863 = $184.000 ÷ 0,255 %.) | Los mínimos son configurables, con o sin IVA (`minimumIncludesVat`). Para la migración se aprobó T1/T2 (`DEC-041`) |
| Tarifas de almacenamiento para producción | ¿Qué porcentaje tiene la tarifa base prorrateada y qué acuerdos por cliente se validan? (`DEC-029`) | Lo define Facturación; staging sigue con T1 (`DEC-041`). Ver pendiente 8 |

Ya resueltas, aunque documentos antiguos las den por abiertas:

- **WMS-30:** la unidad de carga es un concepto propio (`DEC-014`).
- **WMS-18/27:** unidad y embalaje se imprimen por separado (`DEC-015`).
- **WMS-17:** la orden de cargue se conserva y registra la orden externa (`DEC-016`).
- **WMS-33:** el período cuenta desde el ingreso (`DEC-012`).
- **Quincenal de 14 o 15 días:** existen ambos ciclos.

## 7. Por confirmar con el usuario

No se pudieron confirmar desde el código ni los documentos:

- ~~Si hubo despliegues a staging después del 2026-10-08 que no quedaron registrados.~~ *Resuelto el 2026-10-27:* staging ya tenía `AddForkliftUseEntryLog` (BE `83de58a`), así que hubo al menos uno sin registrar; desde la fase 13 staging está en BE `911399c` / FE `33fbeba`, y la pregunta ya no aplica.
- Si los 81 videos ya están publicados en el bucket del centro de ayuda y si el usuario aprobó la serie F7.
- Si los fixes del 2026-10-08 (`83de58a`/`2eeaaad`, `704dcef`…) pasaron por QA.
