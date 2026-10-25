# Planes — índice y estado

> Cómo escribir y ejecutar un plan nuevo: `procesos/flujo-de-trabajo-agentes.md`. Al crear un plan, agrega su fila aquí. Al cerrar una fase, actualiza la columna «Estado».
> **Estados:** Propuesto · Aprobado · En ejecución · Ejecutado · Diferido · Reemplazado.

| Plan | Fecha | Estado | Notas |
| --- | --- | --- | --- |
| `plan-cerrado-brechas-paridad-p1-2026-10-23.md` | 2026-10-23 | En ejecución | 13 brechas P1 y 7 de DEC-050…054 de la auditoría de paridad, más 5 colaterales y el QR de verificación en la guía de salida (fase 11, DEC-060), y la fase 12c con los ajustes de DEC-055 (agregada el 2026-10-24). 13 fases más 12b y 12c, y 5 migraciones (la 5.ª, `RelaxServicePriceActiveIndex`, la agregó la fase 12c por D47). Prompt del ejecutor: `prompt-plan-brechas-paridad-p1-2026-10-23.md`. Fases 1–12 commiteadas (la 1 por el usuario; desde la 2, por el orquestador); veredicto QA local «continuar con condiciones» (`qa/resultados/P1-informe-2026-10-24.md`; DEF-F11-028 corregido y verificado en local, BE `9e399de`); fase 12c (ajustes de DEC-055) commiteada el 2026-10-25 (BE `57c94dd` / FE `cb2a4f7`); falta la fase 13 (staging), que exige la aprobación del usuario paso a paso. Registro en `registro-ejecucion-brechas-p1-2026-10-24.md`; estado por fase en su §17 |
| `plan-cerrado-organizacion-documentacion-2026-10-23.md` | 2026-10-23 | Ejecutado | Creó este hub. Pendiente fuera de alcance: publicarlo en un remoto |
| `plan-cerrado-selector-conductor-2026-10-08.md` | 2026-10-08 | Ejecutado | Verificado en staging el 2026-10-08 (BE `044be08` / FE `4ca4e0a`). Siguen abiertos DEF-F11-023, 024 y 026 (MINOR) |
| `plan-cerrado-permisos-por-usuario-2026-10-07.md` | 2026-10-07 | **Diferido** | No implementar antes del corte. Su §11 lista correcciones obligatorias antes de retomarlo |
| `migracion-staging/plan-migracion-legacy-staging.md` | 2026-10-06 | Ejecutado | Fases 1–5 completadas el 2026-10-07. Siguen abiertos el corte real con un volcado nuevo y vaciar o anonimizar staging (`contexto/estado.md`) |
| `paridad-legacy/plan-backend-paridad-legacy.md` | 2026-09-29 | Ejecutado | Fases 1–6 completadas. E19 (datos reales) se cumplió el 2026-10-06 en la migración (`migracion-staging/resultados/informe-fase-1-repeticion.md`) |
| `paridad-legacy/plan-frontend-paridad-legacy.md` | 2026-09-30 | Ejecutado | Fases 1–5 y 7 completadas; la 6 no lleva código. Pendiente F1-09, que es la medición PRF-002 con un operario |
| `paridad-legacy/contrato-api-paridad.md` | 2026-09-29 | Referencia | Contrato de los endpoints `C-Fx-yy` de la paridad |
| `../qa/plan-correccion-defectos.md` | 2026-10-03 | Ejecutado | 12 fases y CHG-01…90, completadas el 2026-10-05 |

## Planes que ya no existen

Las Olas 1, 2 y 3 (septiembre de 2026) se implementaron, pero sus planes se perdieron. Sus decisiones están en `contexto/decisiones.md`; la lista completa, en `contexto/mapa-de-fuentes.md` §7.

## Análisis (`analisis/`)

| Documento | Estado |
| --- | --- |
| `../analisis/analisis-motor-acuerdos-facturacion-2026-09-17.md` | Diagnóstico: el motor de acuerdos es adecuado con ajustes. Referencia |
| `../analisis/analisis-impacto-permisos-granulares-2026-10-07.md` | Reemplazado por el plan de permisos por usuario, y diferido |
| `../analisis/revision-fob-cif-migracion-v2-2026-10-08.md` | **Abierto:** la equivalencia FOB/CIF de la migración no está validada; no la des por cerrada |
| `../analisis/analisis-fob-cif-legacy-v2-2026-10-24.md` | **Abierto, con decisiones pendientes.** Los datos del legacy confirman que el ingreso es FOB y el levante CIF (V2 los tiene invertidos). La tarifa base T1, sin acuerdos, facturaría el 205 % del legacy. Con acuerdos por cliente y la fórmula prorrateada, V2 iguala el total del legacy (≈102 %) sin desarrollo. 10 decisiones en su §7 |
