# Planes — índice y estado

> Cómo escribir y ejecutar un plan nuevo: `procesos/flujo-de-trabajo-agentes.md`. Al crear un plan, agrega su fila aquí. Al cerrar una fase, actualiza la columna «Estado».
> **Estados:** Propuesto · Aprobado · En ejecución · Ejecutado · Diferido · Reemplazado.

| Plan | Fecha | Estado | Notas |
| --- | --- | --- | --- |
| `plan-cerrado-organizacion-documentacion-2026-10-23.md` | 2026-10-23 | En ejecución | Este hub. F0–F2 hechas; F3–F5 en curso |
| `plan-cerrado-selector-conductor-2026-10-08.md` | 2026-10-08 | Ejecutado | Verificado en staging el 2026-10-08 (BE `044be08` / FE `4ca4e0a`). Siguen abiertos DEF-F11-023, 024 y 026 (MINOR) |
| `plan-cerrado-permisos-por-usuario-2026-10-07.md` | 2026-10-07 | **Diferido** | No implementar antes del corte. Su §11 lista correcciones obligatorias antes de retomarlo |
| `migracion-staging/plan-migracion-legacy-staging.md` | 2026-10-06 | Ejecutado | Fases 1–5 completadas el 2026-10-07. Siguen abiertos el corte real con un volcado nuevo y vaciar o anonimizar staging (`contexto/estado.md`) |
| `paridad-legacy/plan-backend-paridad-legacy.md` | 2026-09-29 | Ejecutado | Fases 1–6 con commit. La tabla del plan aún marca la fase 6 «falta E19», pero la prueba con datos reales se hizo en la migración (`migracion-staging/resultados/informe-fase-1-repeticion.md`) |
| `paridad-legacy/plan-frontend-paridad-legacy.md` | 2026-09-30 | Ejecutado | Fases 1–5 y 7 completadas; la 6 no lleva código. Pendiente F1-09, que es la medición PRF-002 con un operario |
| `paridad-legacy/contrato-api-paridad.md` | 2026-09-29 | Referencia | Contrato de los endpoints `C-Fx-yy` de la paridad |
| `../qa/plan-correccion-defectos.md` | 2026-10-03 | Ejecutado | 12 fases y CHG-01…90, completadas el 2026-10-05. La cabecera aún dice «propuesto» |

## Planes que ya no existen

Las Olas 1, 2 y 3 (septiembre de 2026) se implementaron, pero sus planes se perdieron. Sus decisiones están en `contexto/decisiones.md`; la lista completa, en `contexto/mapa-de-fuentes.md` §7.

## Análisis (`analisis/`)

| Documento | Estado |
| --- | --- |
| `../analisis/analisis-motor-acuerdos-facturacion-2026-09-17.md` | Diagnóstico: el motor de acuerdos es adecuado con ajustes. Referencia |
| `../analisis/analisis-impacto-permisos-granulares-2026-10-07.md` | Reemplazado por el plan de permisos por usuario, y diferido |
| `../analisis/revision-fob-cif-migracion-v2-2026-10-08.md` | **Abierto:** la equivalencia FOB/CIF de la migración no está validada; no la des por cerrada |
