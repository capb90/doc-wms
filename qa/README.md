# QA — Campaña de octubre de 2026

> Cómo se registra y verifica un defecto: `procesos/qa-y-defectos.md`. Estado general del proyecto: `contexto/estado.md`.

| Documento | Para qué |
| --- | --- |
| `00-plan-maestro.md` | Alcance, ambientes, riesgos (§9) y **decisiones del negocio (§10)**, que mandan sobre las fichas |
| `fase-00-smoke.md` … `fase-11-regresion-cierre.md` | Casos de prueba por fase. La fase 11 tiene el Anexo A (datos migrados) |
| `plan-ronda-qa-preproduccion-2026-10-25.md` | Ronda QA de preproducción (regresión integral sobre una copia de los datos migrados, antes de la fase 13 del plan P1). Prompt: `prompt-ronda-qa-preproduccion-2026-10-25.md` |
| `casos-qa2-formatos-pdf-v2-2026-11-27.md` | Casos del plan de formatos v2 de PDF (`DEC-060` §7), con su resultado: QA-PV2-001 a 013 en PASA con pruebas temporales (formato fijo, base local y un escenario de Testcontainers) y el cambio del parámetro por API; la aprobación de los v2 en el frontend, las guías y la exportación con datos reales y QA-PV2-002, 003 y 011 en la pantalla quedan para la QA del usuario (2026-11-27) |
| `casos-qa2-formato-numerico-2026-11-27.md` | Casos del plan de formato numérico es-CO (`DEC-082`), con su resultado: QA-FN-001 a 004 y 009 por la prueba de integración con el API en cultura invariante y QA-FN-005 a 008 en el navegador; 005 (en Báscula) y 007 (en Windows) quedan para la QA del usuario (2026-11-27) |
| `casos-qa2-f04-bodega-2026-11-25.md` | Casos QA2 de la fase 2 de F04 (Bodega), con su resultado: QA2-F04-001 a 030 por API en las fases del backend y QA2-F04-031 a 050 en el navegador, en la integración I-04 (2026-11-25) |
| `casos-qa2-f03-bascula-2026-11-24.md` | Casos QA2 de la fase 2 de F03 (Báscula), con su resultado: QA2-F03-001 a 030 por API en las fases del backend y QA2-F03-031 a 050 en el navegador, en la integración I-03 (2026-11-24) |
| `casos-qa2-f01-f02-2026-11-24.md` | Casos QA2 de la fase 2 de F01 (núcleo de dominio) y F02 (base transversal), con su resultado: QA2-F01-001 a 054 por API en las fases de F01 y QA2-F01-055 a 065 y QA2-F02-001 a 026 en el navegador, en la integración I-01 (2026-11-24) |
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
