# 00 — Evaluación del análisis existente

> **Fecha de la auditoría:** 2026-10-23. Auditoría estática: no se ejecutaron pruebas, builds ni llamadas a APIs, ni se consultó Git.
> **Referencia de código (según documentación):** BE `develop` `35a61b2` y FE `develop` `c924a8b` (`docs/contexto/estado.md`). El código auditado es el que estaba en disco ese día.
> **Qué es este documento:** el inventario de la documentación previa, con su alcance, su método y su vigencia, escrito **antes** de delegar (Fase 1). El contraste de sus conclusiones con el código lo hacen los agentes por módulo. El dictamen consolidado está en `08-auditoria-del-analisis-inicial.md`.

## 1. Cadena documental de la paridad

La paridad tiene cuatro capas. Cada una se apoya en la anterior y tiene una fecha de código distinta:

| # | Capa | Documentos | Corte de código | Qué afirma |
| --- | --- | --- | --- | --- |
| 1 | Análisis del legacy | `bodegas-legacy/docs/legacy_analysis/analysis/01–06` y su auditoría `bodegas-legacy/legacy-analysis/` | Checkout legacy (sin versión) — 2026-09-23 | 263 funcionalidades, 448 rutas, 77 reglas (RN-001…077), 81 tablas, 24 riesgos |
| 2 | Comparación legacy ↔ V2 | `LEGACY_VS_NEW.md`, `MIGRATION_MATRIX.md`, `FUNCTIONAL_GAPS.md`, `BUSINESS_RULE_GAPS.md`, `FRONTEND_PARITY.md`, `BASCULA_PARITY.md`, `ROADMAP.md`, `DECISIONES_REVISION.md` | BE `b089d2b` / FE `26aed68` (2026-09-24); decisiones del 2026-09-29 | 202 evaluables: 59 CUBIERTA, 45 PARCIAL, 46 NO ENCONTRADA, 14 COMPORTAMIENTO DIFERENTE, 37 REEMPLAZADA, 1 REQUIERE VALIDACIÓN; 26 brechas GAP-001…026 (20 se construyen, 6 se aceptan) |
| 3 | Planes de cierre | `docs/planes/paridad-legacy/plan-backend-paridad-legacy.md` (P1–P17), `plan-frontend-paridad-legacy.md` (DF1–DF18), `contrato-api-paridad.md` (`C-Fx-yy`) | Implementados entre 2026-09-29 y 2026-10-02 (BE `bf64de1` + `83d784f`, FE `d690f25`) | Las 6 fases del backend y las 7 del frontend están completas |
| 4 | Validación | `docs/qa/` (F0–F11, 153 fichas `DEF-F*`), `docs/planes/migracion-staging/` (8 fichas `DEF-MIG-*`), `docs/analisis/revision-fob-cif-migracion-v2-2026-10-08.md` | Hasta BE `84c712f` / FE `8527144` (staging 2026-10-07) y `044be08` / `4ca4e0a` (2026-10-08) | GO condicionado solo a PRF-002; FOB/CIF de la migración sin validar |

**Consecuencia para esta auditoría:** la matriz de la capa 2 es **anterior** a la implementación de la capa 3. Sus estados `NO ENCONTRADA` y `PARCIAL` describen el código del 2026-09-24, no el actual. Lo esperable es que muchos queden `OBSOLETA`; lo que interesa es encontrar los que no se cerraron, los que se cerraron a medias y los que cambiaron después (QA, Olas, fixes del 2026-10-08).

Nadie volvió a medir la paridad contra el código después de los planes de la capa 3: la capa 4 valida flujos con casos de QA, no recorre el catálogo legacy. **Ese es el vacío principal que cubre esta auditoría.**

## 2. Ficha por documento

| Ruta | Propósito | Alcance | Fecha | Método | Aprovechable | Problemas detectados (iniciales) | Vacíos |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `docs/README.md`, `docs/contexto/*.md` | Hub: negocio, decisiones, estado, convenciones, mapa de fuentes | Todo el proyecto | Corte 2026-10-23 | Síntesis | Decisiones `DEC-001…042` (única fuente escrita de muchas decisiones), pendientes, URL y datos de staging | `estado.md` §1 afirma «toda la funcionalidad planeada está implementada» sin una matriz que lo respalde | No mide paridad funcional |
| `bodegas-legacy/legacy-analysis/LEGACY_FUNCTIONAL_CATALOG.md` | Catálogo de capacidades legacy | 263 funcionalidades | 2026-09-23 | Lectura de código PHP, una ficha por capacidad | **Base del inventario** de esta auditoría (IDs `CF-Lnnn`) | Es inventario del checkout, no de uso real (lo dice el propio documento) | No distingue lo que se usaba en producción |
| `bodegas-legacy/legacy-analysis/LEGACY_BUSINESS_RULES.md`, `analysis/04_BUSINESS_RULES.md` | Reglas RN-001…077 | Todo el legacy | 2026-09-23 | Estático, con evidencia por archivo | Referencia de reglas para §8.5 | Mezcla conducta observada con anomalías (aclarado en el texto) | — |
| `bodegas-legacy/legacy-analysis/LEGACY_MIGRATION_RISKS.md` | Riesgos RISK-001…024 | Comparación funcional | 2026-09-23 | Estático | Lista de puntos que exigen datos reales | — | — |
| `bodegas-legacy/docs/legacy_analysis/analysis/01–06` | Arquitectura, rutas, funcionalidades, reglas, modelo de datos, integraciones | Legacy completo | 2026-09-23 | Estático | Evidencia legacy detallada | Duplica parcialmente `legacy-analysis/`; los IDs coinciden | — |
| `bodegas-legacy/docs/legacy_analysis/LEGACY_VS_NEW.md` | Validación de migración, define `NEW-FUNC-xxx` | 202 evaluables | Código 2026-09-24 | Estático por funcionalidad | IDs `NEW-FUNC` y evidencia V2 de esa fecha | **Corte anterior a la paridad, a las correcciones de QA y a las Olas 2–3 tardías** | — |
| `bodegas-legacy/docs/legacy_analysis/MIGRATION_MATRIX.md` | Matriz de migración con estado por funcionalidad | 202 + 61 excluidas | Código 2026-09-24; decisiones 2026-09-29 | Estático; seis estados propios | Estado previo de cada `CF-Lnnn` (columna de `01-inventario-funcional-global.md`) | Estados no comparables 1:1 con los de esta auditoría (no separa frontend, backend e integración). Corte anterior a la paridad | Sin dimensión de integración ni de contratos |
| `bodegas-legacy/docs/legacy_analysis/FUNCTIONAL_GAPS.md` | Brechas GAP-001…026 con impacto | 202 evaluables | 2026-09-29 | Agrupación de funcionalidades | Mapa GAP → ítems de los planes | Corte anterior a la paridad | — |
| `bodegas-legacy/docs/legacy_analysis/BUSINESS_RULE_GAPS.md` | Estado de cada regla legacy en V2 | RN-001…077 | Código 2026-09-24 | Por regla: entrada → validación → persistencia → efectos | Punto de partida para §8.5 | Corte anterior a la paridad | — |
| `bodegas-legacy/docs/legacy_analysis/BASCULA_PARITY.md` | Paridad del formulario de báscula | Una pantalla | 2026-09-29 | Comparación campo a campo | Insumo del módulo 02 | No mide tiempo real (PRF-002 sigue pendiente) | — |
| `bodegas-legacy/docs/legacy_analysis/FRONTEND_PARITY.md` | Paridad de interfaz | 80 páginas (hoy hay 94) | FE `26aed68` (2026-09-24) | Por pantalla | Mapa de pantallas | Desactualizado: 14 páginas más en V2 | — |
| `bodegas-legacy/docs/legacy_analysis/ROADMAP.md` | Hoja de ruta de sustitución | 26 brechas | 2026-09-29 | Planificación | Orden y principios del corte | Sus fases 1–6 se ejecutaron (capa 3); su fase 0 tiene ítems sin cierre explícito (rol de Vigilancia a báscula, política de respaldo) | — |
| `bodegas-legacy/docs/legacy_analysis/DECISIONES_REVISION.md` | Respuestas del negocio | 19 + 8 + 1 decisiones | 2026-09-29 | Preguntas y respuestas | **Fuente válida de `DIFERENCIA_INTENCIONAL`** | Cita `code_workspace/ajustes/plan-backend-paridad-legacy.md`, ruta que ya no existe (hoy `docs/planes/paridad-legacy/`) | — |
| `docs/planes/paridad-legacy/plan-backend-paridad-legacy.md` | Plan cerrado de backend, fases 1–6, P1–P17 | GAP-001…026 en backend | 2026-09-29 → 10-06 | Plan por ítem `Fn-nn` | Lo que debía construirse, con criterios de aceptación | Declara las 6 fases completas: **no verificado en código** hasta esta auditoría | — |
| `docs/planes/paridad-legacy/plan-frontend-paridad-legacy.md` | Plan cerrado de frontend, fases 1–7, DF1–DF18 | Pantallas | 2026-10-01 → 02 | Plan por ítem | Fuente válida de decisiones `DF*` | Ídem | — |
| `docs/planes/paridad-legacy/contrato-api-paridad.md` | Contrato de cada endpoint nuevo o modificado (`C-Fx-yy`) | Endpoints de paridad | 2026-09-29 | Contrato petición/respuesta/errores | Base para verificar contratos (§8.4) | Puede haber divergido con los fixes de QA | — |
| `docs/qa/00-plan-maestro.md` | Plan de QA por fases; §10 decisiones del negocio | Todo V2 | 2026-10-02 | Casos por fase | Fuente válida de decisiones (§10); casos reutilizables | Su §9 son hipótesis estáticas, no hallazgos | — |
| `docs/qa/fase-00…11-*.md` | Casos de prueba por fase | Todo V2 | 2026-10-02 → 06 | Casos | Casos que se citan en `09-recomendaciones-qa.md` | — | Los casos validan flujos V2, no equivalencia con el legacy |
| `docs/qa/resultados/informe-final.md` | Veredicto QA | Todo V2 | Corte 2026-10-07 | Ejecución local (S0–S5) y staging (S6) | **Única evidencia de validación ejecutada**; cuenta para «paridad validada» | GO condicionado a PRF-002 | No cubre los fixes posteriores al 2026-10-08 (`estado.md` §7) |
| `docs/qa/resultados/defectos/INDICE.md` y fichas | 153 defectos `DEF-F*` | Todo V2 | Hasta 2026-10-08 | Fichas con re-test | Se citan antes de registrar una brecha | 3 fichas «Nuevo» (DEF-F11-023, 024, 026) | — |
| `docs/qa/fase-11-regresion-cierre.md` (Anexo A) | Regresión y datos migrados | Re-test | 2026-10-05 → 07 | Ejecución | Evidencia de datos migrados | — | — |
| `docs/planes/migracion-staging/` y `resultados/` | Migración legacy → staging, 8 `DEF-MIG-*` | Datos vivos | 2026-10-06 → 07 | Ejecución por fases | Evidencia de la importación legacy (CF-V081) | Corte simulado al 2026-09-30 (`DEC-040`): el corte real no se ha hecho | — |
| `docs/analisis/revision-fob-cif-migracion-v2-2026-10-08.md` | Revisión de FOB y CIF | Migración y facturación | 2026-10-08 | Estático + datos | Riesgo abierto de equivalencia de conceptos | Dictamen: «no dar por cerrada» | — |
| `docs/analisis/analisis-motor-acuerdos-facturacion-2026-09-17.md`, `analisis-impacto-permisos-granulares-2026-10-07.md` | Análisis previos a decisiones | Facturación; permisos | 2026-09-17; 2026-10-07 | Análisis | Contexto de los módulos 06 y 01 | El segundo describe un plan diferido (`DEC-030`) | — |
| `docs/manuales/*` | Manuales de usuario | Operación | Julio y posteriores | — | Contexto funcional | El PDF de julio es anterior a las Olas (aviso de vigencia) | — |

## 3. Fuentes que ya no existen

`docs/contexto/mapa-de-fuentes.md` §7 lista los planes de las Olas 1–3, las historias de usuario, los análisis de almacenamiento y los requerimientos `FAC-n`/`CE-n`. No se buscaron. Sus decisiones se toman de `docs/contexto/decisiones.md`. Cuando el código las cite en comentarios, el agente lo registra sin darlas por existentes.

## 4. Conclusiones anteriores que se contrastan

Cada agente clasifica, para las capacidades de su módulo, el estado previo de `MIGRATION_MATRIX.md` y las afirmaciones de los planes como `CONFIRMADA_EN_CODIGO`, `CONTRADICHA_POR_CODIGO`, `INCOMPLETA`, `OBSOLETA` o `NO_VERIFICADA` (sección «Contraste con el análisis anterior» de su `resultado-agente.md`). Las afirmaciones de mayor peso que se verifican:

1. Los 46 `NO ENCONTRADA` y 45 `PARCIAL` de la matriz anterior se cerraron con los planes de la capa 3.
2. Las 20 brechas «se construyen» de `FUNCTIONAL_GAPS.md` están implementadas en backend **y** frontend, con integración real.
3. Las 6 brechas aceptadas y P16 se respetan (no se construyó lo que se decidió no construir; no quedó código a medias).
4. Las 61 exclusiones no dejaron dependencias rotas en V2.
5. Los contratos `C-Fx-yy` coinciden con los DTO y las llamadas actuales.
6. `estado.md`: «toda la funcionalidad planeada está implementada».

## 5. Vacíos que cubre esta auditoría

- Contraste por capacidad contra el código **actual** (después de QA y de los fixes del 2026-10-08).
- Dimensión de **integración** frontend ↔ backend y de **contratos** (no existía).
- Endpoints sin consumidor y servicios del frontend sin endpoint.
- Procesos automáticos comparados uno a uno (`cron.php`, alertas del menú, jobs).
- Capacidades `SOLO_V2`, separadas de la paridad.
- Indicadores con denominadores explícitos: cobertura, paridad estática y paridad validada.
