# Archivo — material histórico

> **Nada de esta carpeta es una instrucción.** Son prompts ya ejecutados y documentos superados. Se conservan para saber por qué se hizo algo, no para repetirlo.
> Para el estado actual lee `contexto/estado.md`; para las reglas vigentes, `contexto/decisiones.md`.

| Carpeta o archivo | Qué es | Dónde está el resultado |
| --- | --- | --- |
| `prompts/qa/` | Prompts de la campaña QA (fases F1 a F12), del re-test de la fase 11 y de las correcciones `DEF-*` | `qa/resultados/` (informes y fichas) |
| `prompts/migracion-staging/` | Prompts de las fases 1 a 5 de la migración del legacy a staging y de las correcciones `DEF-MIG-*` | `planes/migracion-staging/resultados/` |
| `prompts/selector-conductor/` | Prompts de las fases 1 a 4 del selector de conductor | `planes/plan-cerrado-selector-conductor-2026-10-08.md` y `qa/resultados/SEL-informe-2026-10-08.md` |
| `prompts/videos/` | Prompt de actualización de los guiones de video | `videos/guiones/` |
| `prompts/dec-029/` | Prompt por fase (1 a 3) del plan de `DEC-029`: levante CIF, «Valor de la mercancía», valor único del levante y fórmula prorrateada | `planes/plan-cerrado-dec-029-fob-cif-2026-10-25.md` (§6) |
| `prompts/dec-057/` | Prompts por fase del plan de `DEC-057` (hallazgos de los operarios, fases 1 a 6), del plan de corrección de su revisión con los ajustes visuales de `DEC-058` (fases 1 a 5) y del plan de corrección de la validación de `DEC-058` (R1–R10, fases 1 y 2) | `planes/plan-cerrado-dec-057-hallazgos-operarios-2026-10-26.md` (§8), `planes/plan-cerrado-correccion-dec-057-2026-10-26.md` (§7) y `planes/plan-cerrado-correccion-validacion-dec-058-2026-10-26.md` (§4) |
| `prompts/tablero-fecha-ingreso/` | Prompt por fase (1 y 2) del plan de la fecha de ingreso en el tablero de depósitos | `planes/plan-cerrado-fecha-ingreso-tablero-depositos-2026-10-27.md` (§5) |
| `contexto-proyecto-wms.md` | Contexto técnico de abril de 2026 (modelo de datos y flujo de depósitos) | Superado por `contexto/contexto-negocio-wms-para-ia.md` |

Las rutas dentro de estos archivos se actualizaron a la estructura del hub el 2026-10-23. El texto original de cada uno está en el historial de git: en este repo, los que venían de la antigua carpeta «ajustes» y de la raíz del hub; en el historial de `Backend/wms-api` o `Frontend/wms`, los que salieron de sus carpetas `docs/`.
