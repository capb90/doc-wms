# QA — Campaña de octubre de 2026

> Cómo se registra y verifica un defecto: `procesos/qa-y-defectos.md`. Estado general del proyecto: `contexto/estado.md`.

| Documento | Para qué |
| --- | --- |
| `00-plan-maestro.md` | Alcance, ambientes, riesgos (§9) y **decisiones del negocio (§10)**, que mandan sobre las fichas |
| `fase-00-smoke.md` … `fase-11-regresion-cierre.md` | Casos de prueba por fase. La fase 11 tiene el Anexo A (datos migrados) |
| `plan-ronda-qa-preproduccion-2026-10-25.md` | Ronda QA de preproducción (regresión integral sobre una copia de los datos migrados, antes de la fase 13 del plan P1). Prompt: `prompt-ronda-qa-preproduccion-2026-10-25.md` |
| `plan-correccion-defectos.md` | Plan de corrección: CHG-01…CHG-90 en 12 fases, todas completadas. Su §4.0 contiene las reglas comunes de implementación |
| `plantillas/` | Plantillas de ficha de defecto, informe de fase y registro de datos |
| `resultados/informe-final.md` | Veredicto de la campaña (GO / NO-GO) y sus condiciones |
| `resultados/defectos/INDICE.md` | Inventario de fichas con severidad y estado. La ficha es la fuente de verdad |
| `resultados/F*-informe-*.md` | Informes por fase y sesión (F11: S0…S6) |
| `resultados/SEL-informe-2026-10-08.md` | QA del selector de conductor |
| `resultados/P1-informe-2026-10-24.md` | QA local del plan de brechas P1 (fases 1 a 11): casos nuevos y de regresión, DEF-F11-028 y condiciones para la fase 13 |
| `resultados/PRE-informe-2026-10-25.md` | Ronda QA de preproducción (2026-10-25, BE `57c94dd` / FE `cb2a4f7`) sobre `wms_qa_preprod`, copia de los datos migrados: ensayo de las 6 migraciones, B0–B7 (178 casos) y veredicto **GO con condiciones** (DEF-F11-030 CRITICAL y DEF-F11-034 MAJOR). Anexo §11: re-test del 2026-10-25 (BE `b3de3cc` / FE `83a0af0`), los dos «Verificado» y **GO** para la fase 13. Datos: `resultados/registro-datos-qa-preproduccion.md` |
| `resultados/evidencias/`, `resultados/muestras-f*/` | Evidencias y muestras (capturas, PDF, respuestas del API) |
| `resultados/registro-datos-qa*.md` | Datos de prueba creados en cada fase |
| `resultados/*.sql` | Consultas de «palanca» usadas en pruebas locales (solo base local) |

Los prompts que guiaron cada fase y cada corrección están en `archivo/prompts/qa/`. Son históricos.
