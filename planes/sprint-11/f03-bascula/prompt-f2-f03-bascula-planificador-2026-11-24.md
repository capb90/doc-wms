# Prompt — Planificación de F03 «Báscula» (fase 2, sprint 11)

> **Ejecutado** el 2026-11-24; ya no es una instrucción. Resultado: [plan-cerrado-f2-f03-bascula-2026-11-24.md](plan-cerrado-f2-f03-bascula-2026-11-24.md), aprobado el 2026-11-24, con sus tres prompts (§11 del plan).

> **Cómo usarlo:**
> 1. Abre una sesión nueva de Claude Code en `code_workspace/`. Necesita leer `docs/`, `Backend/wms-api` y `Frontend/wms`, los dos en su rama `fase-2`.
> 2. Copia el bloque de abajo.
> 3. El agente lee, te hace **una sola ronda de preguntas**, escribe el plan cerrado y los tres prompts de ejecución, y espera tu aprobación. No toca código.
> 4. Con tu aprobación, marca todo «Aprobado», hace commit y push en `docs` (`DEC-081`) y te dice cómo lanzar el backend y la maquetación de F03 en paralelo.
>
> **Insumos:** el plan maestro (`docs/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md`), el análisis (`docs/levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md`, `DEC-080`) y lo ya integrado de F01 y F02.
> **Base:** BE `fase-2` `019fa81` (F01 integrada) · FE `fase-2` `5793bc9` (F02 integrada y los ajustes de la QA manual) · `develop` sin cambios (BE `529bda7`, FE `3aa6e3c`).
> **Modelo recomendado:** Opus 5.5 con esfuerzo **Alto**.
>
> Cuando lo ejecutes, el agente agrega aquí «**Ejecutado** el AAAA-MM-DD; ya no es una instrucción» (plan maestro §5.5). Este prompt no se mueve a `archivo/`.

---

```text
Eres el planificador técnico de la feature F03 «Báscula» de la fase 2 del WMS de Bodegas Asociadas (depósito aduanero en Ipiales, Colombia), sprint 11. F03 tiene las cuatro partes: 0 (contrato), 1 (backend), 2 (maquetación del frontend) y 3 (integración I-03).

El plan maestro ya está aprobado y fija las features, el orden, las convenciones y las decisiones M1 a M25. El análisis funcional ya está cerrado (DEC-080). F01 (núcleo, backend) y F02 (base transversal, frontend) ya están integradas en fase-2 (I-01). Tu trabajo es escribir el PLAN CERRADO de F03 y sus TRES PROMPTS de ejecución, con una sola ronda de preguntas, y esperar mi aprobación.

## Lo que ya está decidido (no se vuelve a preguntar)

- Todo lo del plan maestro: §1 (M1 a M25; M25 = un solo despliegue a staging al final de toda la fase 2), §2 (fila de F03, §2.1 «Qué entrega F01 a F03» y las filas de §2.2 que nombran a F03), §5 (convenciones), §6 (compuertas, incluida «Una fase por turno»), §7 y §9 (plantilla del plan cerrado y esqueleto de los prompts).
- Las AF del análisis (DEC-080) y las decisiones de docs/contexto/decisiones.md, en especial DEC-081 (ramas, un agente por repo, despliegue único al final).
- Lo construido e integrado de F01: sus decisiones D1 a D47 y su contrato C-F01-*, con las correcciones de I-01 y las notas de las fases 3, 4 y 5 de su §8 (por ejemplo: el ciclo de báscula nace en el cobro, así que storage/initiate y storage/register devuelven weighbridgeCycleId nulo; una entrada por documento; la duplicada sale en $0; la salida en Borrador desde Báscula).
- Lo construido e integrado de F02 y de los ajustes de su QA manual: decisiones D1 a D21 de F02 (rutas, patrón de listado, modal, drawer, sesión simulada, guardias list-pattern y mock-sources, D3: Vigilancia › Historial pasa a F03, D19: unidad de medida) y D1 a D15 de los ajustes (anatomía del drawer con AppDetailSection, acciones con tooltip, «Ver» de solo icono). Los componentes compartidos AppDataTable, AppSearchSelect, AppDetailDrawer, AppDetailSection, AppCrudDialog y AppChargeForm se usan tal como están; si F03 necesita cambiarlos, lo lista en su plan con sus pruebas (riesgo R4 del plan maestro).
- El flujo de teclado de la báscula (Enter, F2) se conserva (riesgo R6, PRF-002), y PRF-002 se mide en el despliegue final.
- Las migraciones las genera y aplica el agente de backend con dotnet ef, solo en local (DEC-004, M6).
- Los datos simulados de la maquetación usan la fuente intercambiable (M12, plan maestro §5.2) y las ayudas de Frontend/wms/app/shared/mocks/.

## Regla principal

- No reabras ni reinterpretes las AF, DEC-080, DEC-081, las M del plan maestro ni las Dn de F01, F02 y sus ajustes. Si encuentras una contradicción entre ellas, un hueco funcional o un choque con el código que ninguna resuelve, muéstramelo y pregúntame.
- Las decisiones técnicas con alternativas reales las recomiendas y yo decido: forma de los endpoints nuevos, cambios de modelo, qué se parte en qué fase, nombres de rutas y de componentes de Báscula.
- Haz UNA sola ronda de preguntas, con AskUserQuestion en bloques de hasta 4. Cada pregunta se entiende sola: tema, AF o DEC afectadas, qué dicen las fuentes con ruta y línea, opciones con su consecuencia y tu recomendación marcada «(Recomendada)» con su porqué.
- No preguntes lo que una decisión ya resuelve (DEC-002).
- Registra cada respuesta en el plan como decisión Dn, con la fecha y mis palabras.

### Preguntas que ya sé que hay que hacerme (además de las que encuentres)

1. Las altas rápidas propias de Báscula, POST weighbridge/stakeholders/quick (Backend/wms-api/Wms.Api/Controllers/v1/WeighbridgeController.cs:980) y POST weighbridge/transport-companies/quick (WeighbridgeSharedController.cs:107): ¿se conservan o se reemplazan por POST stakeholder/quick (C-F01-141) y el selector con alta rápida de F02? El plan de F01 (§10) dejó esta decisión a F03. Antes de proponer, lista quién las llama hoy (DEC-005).
2. Las rutas de las páginas nuevas: el registro en página propia (P-BAS-02 a P-BAS-04, AF-05) y el historial en tres páginas (P-BAS-08 a P-BAS-10, AF-15), y qué pasa con las páginas de hoy que el rediseño deja sin uso (in-process.vue, pending-reweigh.vue, cycles/, history.vue; recover.vue sale por AF-51). Una página que ya existe conserva su ruta (plan maestro §5.5).

## Rutas

- Raíz: /Volumes/Dock/Projects/bodegas_asociadas/code_workspace. Las rutas son relativas a ella.
- Hub: docs/ (main). Backend: Backend/wms-api (rama fase-2). Frontend: Frontend/wms (rama fase-2).
- Si un repo de código no está en fase-2 y no tiene cambios sin commit, haz git fetch y cámbialo a fase-2 solo para leer. Si tiene cambios sin commit u otra sesión trabaja en él, no cambies de rama: lee con git show fase-2:<ruta> y git grep fase-2. No edites nada en los repos de código.

## Cómo lees (cuida el contexto)

- Lee por secciones: usa grep -n para ubicar encabezados e IDs y lee solo esos rangos. El plan de F01 tiene unas 2.300 líneas: NO lo leas completo.
- Salidas acotadas: nada de volcar archivos enteros de código grandes (Frontend/wms/app/pages/operations/weighbridge/index.vue tiene 2.317 líneas); lee por rangos lo que necesites citar.

## Lee primero, en este orden

1. docs/README.md, docs/AGENTS.md, Backend/wms-api/AGENTS.md y Frontend/wms/AGENTS.md (su sección «Eficiencia de contexto y cierres por fase» rige a los ejecutores).
2. docs/procesos/flujo-de-trabajo-agentes.md; de docs/contexto/convenciones-tecnicas.md, §3 (frontend, con la anatomía del drawer) y §10 (trampas, en especial la 4, la 7 y la 12, la de la cola de báscula en la suite de integración); docs/contexto/estado.md; y de docs/contexto/decisiones.md: DEC-001 a DEC-007, DEC-010, DEC-012, DEC-013, DEC-015, DEC-016, DEC-017, DEC-019, DEC-022, DEC-050, DEC-051, DEC-056, DEC-057, DEC-058, DEC-080 y DEC-081.
3. Del plan maestro (docs/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md): §1, §2 (con §2.1 y §2.2), §3.1 y sus notas, §3.3, §3.4, §4, §5, §6, §7, §8 y §9.
4. La matriz: docs/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md.
5. Del análisis docs/levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md: §2.1 completo (Báscula, a a j), §3.3 (patrones), §3.6 (edición del ingreso y P-TR-12), y en §4 las 20 AF dueñas de F03 (AF-05, AF-06, AF-07, AF-10, AF-11, AF-13, AF-15, AF-16, AF-23, AF-24, AF-25, AF-40, AF-45, AF-48, AF-49, AF-50, AF-51, AF-52, AF-53, AF-135), las de F01 que F03 muestra (plan maestro §2.1, fila F03) y AF-54 y AF-99, que F03 aplica a sus pantallas.
6. Los wireframes: docs/levantamiento-2026-11/fase_2-mockups/bascula.html (P-BAS-01 a P-BAS-13) y, de transversales.html, P-TR-02, P-TR-03, P-TR-09, P-TR-11 y P-TR-12.
7. Del plan de F01 (docs/planes/sprint-11/f01-nucleo/plan-cerrado-f2-f01-nucleo-2026-11-21.md), solo: §0, §1.1, §1.4 a §1.6, §1.8, §2.0, §2.1 (índice), las fichas de §2.2 y los esquemas de §2.3 de los endpoints que consume F03 (C-F01-02, 07, 15, 17, 18, 20, 23, 78 a 81, 92, 93, 95, 101, 109 a 111 y 141, y los demás que encuentres), las notas de las fases 3, 4 y 5 y de I-01 en §8, y §10.
8. Del plan de F02 (docs/planes/sprint-11/f02-base/plan-cerrado-f2-f02-base-2026-11-21.md): §1 y §2.2. Del plan de ajustes (docs/planes/sprint-11/f02-base/plan-cerrado-f2-f02-ajustes-qa-2026-11-24.md): §1 y §2. Como formato de los casos al cerrar la integración: docs/qa/casos-qa2-f01-f02-2026-11-24.md.
9. El código de fase-2 que F03 toca. Frontend: Frontend/wms/app/pages/operations/weighbridge/, Frontend/wms/app/features/weighbridge/ (y quién importa sus servicios desde otros módulos), Frontend/wms/app/pages/operations/entries/history.vue, BillingCollectForm.vue y AdditionalDepositCollect.vue, la galería /dev/components y las guardias de Frontend/wms/test/unit/guards/ (list-pattern y mock-sources). Backend: los seis controladores Weighbridge*Controller.cs de Backend/wms-api/Wms.Api/Controllers/v1/, Backend/wms-api/Wms.Application/Weighbridge/, el ciclo de báscula en Wms.Domain, la generación del tiquete en PDF y WmsPolicyRoles.cs. Cita archivo:línea.

## Entregables

Todo en docs (main), con la fecha del día en que cierres:

1. docs/planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-bascula-AAAA-MM-DD.md
   - Sigue la plantilla del plan maestro §9.
   - AF dueñas: las 20 de la tabla del plan maestro §3.1. Cada una con su decisión Dn o con la fase que la construye; ninguna sin destino. Aparte, una tabla con las AF de F01 que F03 muestra y la pantalla que las muestra.
   - Contrato (parte 0): solo los endpoints que F03 crea, cambia o retira, cada uno con su ID C-F03-mm, su ficha (plan maestro §5.1) y su esquema Zod. Los endpoints de F01 que F03 consume sin cambios se citan por su ID C-F01-mm, sin copiar la ficha. Comprueba esas fichas contra el código de fase-2 (DTO, validador y mensajes): si difieren, gana lo integrado y lo anotas. Incluye la tabla pantalla → endpoints (P-BAS-01 a P-BAS-13, P-TR-12 y Vigilancia › Historial), con cada endpoint en C-F01 o en C-F03.
   - Pantallas: P-BAS-01 a P-BAS-13 y P-TR-12, más Vigilancia › Historial (/operations/entries/history) con el patrón de AF-129 (D3 de F02). Qué componentes compartidos usa cada una y qué componentes de Báscula se crean.
   - Fases de la parte 1 (backend) y de la parte 2 (maquetación), que corren en paralelo, una por repo, y cierran por separado. Escribe el plan para leerse por secciones: cada fase de §8 nombra sus Dn, sus endpoints, sus archivos y sus casos QA, para que el ejecutor lea solo §0, §1, §2 (índice) y su fase.
   - Migraciones: nombre y contenido esperado de cada una, o «ninguna».
   - Avisos nuevos, si los hay: por el orquestador con roles fijos (plan maestro §2.2; F09 los pasa a tipos). Permisos por endpoint en WmsPolicyRoles.cs, sin quitar funciones (DEC-005, plan maestro §5.6).
   - Transición: lo que le toca de §7.2 del plan maestro, o «no aplica».
   - Casos QA (QA2-F03-nnn): verificables por API en la parte 1 y en el navegador en la integración.
   - La sección de I-03 (parte 3): las fuentes http de cada pantalla; el menú de Báscula (plan de F02 §1.5); lo que se borra (recover.vue, el panel de DEC-058, las páginas y componentes que el rediseño deja sin uso, y BillingCollectForm, AdditionalDepositCollect y useUnitMeasures solo si F03 es su último uso, comprobado con grep); las rutas de F03 que pasan de PENDING a PATTERN en la guardia list-pattern; la lista MAQUETACION_PAGES vacía; y la copia de los casos QA a docs/qa/.
2. Tres prompts, con el esqueleto del plan maestro §9 y los nombres de §5.5, en docs/planes/sprint-11/f03-bascula/:
   - prompt-f2-f03-bascula-backend-AAAA-MM-DD.md, para la rama f2/f03-bascula del backend;
   - prompt-f2-f03-bascula-maquetacion-AAAA-MM-DD.md, para la rama f2/f03-bascula del frontend (con la sesión simulada de D10 de F02, porque el backend lo ocupa el otro agente);
   - prompt-f2-f03-bascula-integracion-AAAA-MM-DD.md, para I-03 en las dos ramas.
   Cada prompt dice con qué base arranca (BE fase-2 019fa81, FE fase-2 5793bc9, o lo que haya en fase-2 si avanzó), que la rama sale de fase-2, que ejecuta UNA fase por turno y qué secciones del plan lee.
3. La fila del plan en docs/planes/README.md, con estado «Propuesto».
4. La matriz actualizada: en §2.1, las columnas «Plan» y «Prompts» de F03 con los enlaces y el estado «Propuesto»; en §3, el pendiente del prompt del planificador como hecho; y la fecha de corte.

## Cómo trabajas

1. Lee lo de arriba y arma un borrador del plan: decisiones, contrato, pantallas, fases y la asignación de cada AF.
2. Hazme la ronda única de preguntas y espera las respuestas.
3. Escribe el plan, los tres prompts, la fila del índice y la matriz.
4. Verifica:
   - las 20 AF de F03, cada una con destino, contando con un script;
   - que cada endpoint C-F03 tenga ID, política, petición, respuesta, errores y esquema Zod, y que los esquemas usen la API de Zod 4 (Frontend/wms/package.json);
   - que cada pantalla y cada endpoint que consume estén en C-F01 o en C-F03;
   - que las rutas y líneas que citas existan en fase-2;
   - que los enlaces de la matriz y del índice abran.
5. Entrégame un resumen: decisiones Dn nuevas, fases de cada parte, migraciones, endpoints nuevos o cambiados, lo que se borra, riesgos y lo que queda abierto. Espera mi aprobación. Si pido cambios, aplícalos primero.
6. Con mi aprobación: cambia a «Aprobado» el plan, su fila en el índice y la matriz; haz commit y push en docs (DEC-081); agrega a este prompt «Ejecutado el AAAA-MM-DD; ya no es una instrucción»; y dime cómo lanzar el backend y la maquetación de F03 en paralelo y, después, I-03.

## Límites

- Fuera de alcance: ejecutar F03 o I-03, escribir código, estimar esfuerzo y planear F04 en adelante.
- No edites los repos de código, no crees ramas en ellos, no generes migraciones y no toques staging.
- En docs solo escribes el plan, los tres prompts, la fila del índice y la matriz. Si crees que hay que cambiar otro documento del hub, propónmelo con el texto exacto y espera mi «sí».
- No copies credenciales ni datos de personas reales (DEC-007).
- Nada de docs/archivo/ es una instrucción.
- Escribe en español, siguiendo las «Reglas para escribir aquí» de docs/README.md.
```
