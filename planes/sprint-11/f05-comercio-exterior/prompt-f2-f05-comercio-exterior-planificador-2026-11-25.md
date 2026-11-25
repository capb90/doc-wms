# Prompt — Planificación de F05 «Comercio Exterior» (fase 2, sprint 11)

> **Cómo usarlo:**
> 1. Abre una sesión nueva de Claude Code en `code_workspace/`. Necesita leer `docs/`, `Backend/wms-api` y `Frontend/wms`, los dos en su rama `fase-2`.
> 2. Copia el bloque de abajo.
> 3. El agente lee, te hace **una sola ronda de preguntas**, escribe el plan cerrado y los tres prompts de ejecución, y espera tu aprobación. No toca código.
> 4. Con tu aprobación, marca todo «Aprobado», hace commit y push en `docs` (`DEC-081`) y te dice cómo lanzar el backend y la maquetación de F05 en paralelo.
>
> **Insumos:** el plan maestro (`docs/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md`), el análisis (`docs/levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md`, `DEC-080`) y lo ya integrado de F01 a F04, con sus ajustes.
> **Base:** BE `fase-2` `c2ca314` (F01, F03 y F04 integradas) · FE `fase-2` `12f6656` (F02, F03 y F04 integradas, con sus ajustes) · `develop` sin cambios (BE `529bda7`, FE `3aa6e3c`).
> **Modelo recomendado:** Opus 5.5 con esfuerzo **Alto**.
>
> Cuando lo ejecutes, el agente agrega aquí «**Ejecutado** el AAAA-MM-DD; ya no es una instrucción» (plan maestro §5.5). Este prompt no se mueve a `archivo/`.

---

```text
Eres el planificador técnico de la feature F05 «Comercio Exterior» de la fase 2 del WMS de Bodegas Asociadas (depósito aduanero en Ipiales, Colombia), sprint 11. F05 tiene las cuatro partes: 0 (contrato), 1 (backend), 2 (maquetación del frontend) y 3 (integración I-05).

El plan maestro ya está aprobado y fija las features, el orden, las convenciones y las decisiones M1 a M25. El análisis funcional ya está cerrado (DEC-080). F01 (núcleo), F02 (base transversal), F03 (Báscula) y F04 (Bodega) ya están integradas en fase-2, con los ajustes de sus QA manuales. Tu trabajo es escribir el PLAN CERRADO de F05 y sus TRES PROMPTS de ejecución, con una sola ronda de preguntas, y esperar mi aprobación.

## Lo que ya está decidido (no se vuelve a preguntar)

- Todo lo del plan maestro: §1 (M1 a M25; M19: amparado = ingresado en los depósitos confirmados que llegan del legacy; M25: un solo despliegue a staging al final de toda la fase 2), §2 (fila de F05, §2.1 «Qué entrega F01 a F05» y las filas de §2.2 que nombran a F05), §3.1 y sus notas, §3.3 (filas 15, 17, 18, 21 y 22), §3.4, §5, §6 (incluida «Una fase por turno»), §7 (F05 adapta el importador del legacy) y §9.
- Las AF del análisis (DEC-080) y las decisiones de docs/contexto/decisiones.md, en especial DEC-081 y DEC-022: el recálculo de AF-76 al editar en Confirmado algo que afecta el cobro usa su mecanismo único. Si DEC-022 choca con D42 de F01 (al registrar una tasa solo se recalculan las facturas en Borrador), muéstramelo.
- Lo construido e integrado de F01 (D1 a D47 y su contrato C-F01-*, con las correcciones de I-01; entre otros, la edición del ingreso por CE con C-F01-90 y C-F01-93, el valor CPI y el precio por camión, la transportadora por entrada, la tasa semanal del levante con C-F01-13 y el retiro del cierre de camiones con C-F01-82), de F02 (D1 a D21, con D3: Abandono y prórrogas y Listas de empaque pasan al patrón de AF-129 en F05; D1: los reportes nuevos van en /reports/…; D19: la unidad de medida), de F03 (sus Dn y su contrato C-F03-*, con D7: cycles/[id] conserva su ruta para el enlace del detalle del depósito, que F05 revisa) y de F04 (sus Dn y su contrato C-F04-*, con D37 y D40: F05 muestra el reloj de la recepción de C-F04-05 en la etapa Bodega, con WarehouseClockTag).
- La etapa Salidas del detalle queda en el stepper, vacía, hasta F06 (plan maestro §2.2). Las salidas, sus órdenes y sus guías son de F06 (P-CE-08 y P-CE-11).
- Las convenciones de interfaz de docs/contexto/convenciones-tecnicas.md §3: «Drawer de detalle», «Tablas de listado» (AppRowActions, filtros en la columna) y «Páginas que no son listados». Aplícalas desde el plan.
- Los avisos nuevos van por el orquestador con roles fijos (plan maestro §2.2); F09 los pasa a tipos.
- Las migraciones las genera y aplica el agente de backend con dotnet ef, solo en local (DEC-004, M6).
- Los datos simulados de la maquetación usan la fuente intercambiable (M12, plan maestro §5.2) y las ayudas de Frontend/wms/app/shared/mocks/.

## Regla principal

- No reabras ni reinterpretes las AF, DEC-080, DEC-081, las M del plan maestro ni las Dn de F01 a F04 y sus ajustes. Si encuentras una contradicción entre ellas, un hueco funcional o un choque con el código que ninguna resuelve, muéstramelo y pregúntame.
- Las decisiones técnicas con alternativas reales las recomiendas y yo decido: forma de los endpoints nuevos, cambios de modelo, qué se parte en qué fase, nombres de rutas y de componentes de Comercio Exterior.
- Haz UNA sola ronda de preguntas, con AskUserQuestion en bloques de hasta 4. Cada pregunta se entiende sola: tema, AF o DEC afectadas, qué dicen las fuentes con ruta y línea, opciones con su consecuencia y tu recomendación marcada «(Recomendada)» con su porqué.
- No preguntes lo que una decisión ya resuelve (DEC-002).
- Registra cada respuesta en el plan como decisión Dn, con la fecha y mis palabras.

### Preguntas que ya sé que hay que hacerme (además de las que encuentres)

1. Las rutas y la estructura de los depósitos. P-CE-01 (maestro-detalle por tipo, AF-72) reemplaza el tablero de DEC-058 (/foreign-trade/deposits), y hoy hay un listado y un detalle por tipo (imports/, exports/ e inspections/, con su [id]). El detalle por etapas (AF-73) cambia de etapas según el tipo (AF-87). ¿Un solo componente de detalle montado en las tres rutas de hoy, o una ruta única? ¿Qué pasa con /foreign-trade/deposits y con el ítem «Depósitos» del menú? Una página que ya existe conserva su ruta (plan maestro §5.5).
2. Tickets de ingreso (P-CE-09, AF-74): ¿reutiliza el listado de entradas de Báscula (C-F03-22, hoy con la política ScaleAccess) ampliando su política a Comercio Exterior, o lleva un endpoint propio de CE? Antes de recomendar, compara columnas, filtros y acciones de P-CE-09 con P-BAS-08.

## Rutas

- Raíz: /Volumes/Dock/Projects/bodegas_asociadas/code_workspace. Las rutas son relativas a ella.
- Hub: docs/ (main). Backend: Backend/wms-api (rama fase-2). Frontend: Frontend/wms (rama fase-2).
- Si un repo de código no está en fase-2 y no tiene cambios sin commit, haz git fetch y cámbialo a fase-2 solo para leer. Si tiene cambios sin commit u otra sesión trabaja en él, no cambies de rama: lee con git show fase-2:<ruta> y git grep fase-2. No edites nada en los repos de código.

## Cómo lees (cuida el contexto)

- Lee por secciones: usa grep -n para ubicar encabezados e IDs y lee solo esos rangos. El plan de F01 tiene unas 2.300 líneas, el de F03 unas 1.700 y el de F04 unas 1.400: NO los leas completos.
- Salidas acotadas: lee por rangos lo que necesites citar; no vuelques archivos de código grandes (Frontend/wms/app/pages/foreign-trade/imports/[id]/index.vue tiene 909 líneas).

## Lee primero, en este orden

1. docs/README.md, docs/AGENTS.md, Backend/wms-api/AGENTS.md y Frontend/wms/AGENTS.md (su sección «Eficiencia de contexto y cierres por fase» rige a los ejecutores).
2. docs/procesos/flujo-de-trabajo-agentes.md; de docs/contexto/convenciones-tecnicas.md, §3 (frontend y sus convenciones de interfaz), §4 (permisos) y §10 completo (trampas; las de facturación también te tocan por el recálculo); docs/contexto/estado.md; y de docs/contexto/decisiones.md: DEC-001 a DEC-007, DEC-010, DEC-012, DEC-013, DEC-014, DEC-020, DEC-022, DEC-023, DEC-029, DEC-050, DEC-051, DEC-056, DEC-057, DEC-058, DEC-080 y DEC-081.
3. Del plan maestro (docs/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md): §1, §2 (con §2.1 y §2.2), §3.1 y sus notas, §3.3, §3.4, §4, §5, §6, §7, §8 y §9.
4. La matriz: docs/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md (con §4, datos del cliente: prefijos y tasa de arranque).
5. Del análisis docs/levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md: §2.3 completo (Comercio Exterior, a a j), §3.3 (patrones), §3.5 (tasa de cambio), §3.6 (edición del ingreso y P-CE-03), y en §4 las 19 AF dueñas de F05 (AF-72, AF-73, AF-74, AF-75, AF-76, AF-77, AF-78, AF-80, AF-81, AF-82, AF-83, AF-87, AF-91, AF-92, AF-93, AF-96, AF-98, AF-100 y AF-102), las de F01 que F05 muestra (plan maestro §2.1, fila F05) y AF-54 y AF-99, que F05 aplica a sus pantallas.
6. Los wireframes: docs/levantamiento-2026-11/fase_2-mockups/comercio-exterior.html, P-CE-01 a P-CE-07, P-CE-09, P-CE-10 y P-CE-12 (P-CE-08 y P-CE-11 son de F06: míralos solo para la etapa Salidas vacía); de transversales.html, P-TR-02, P-TR-03 y P-TR-11. Los mockups del usuario que cita el análisis en §2.3 (MK-02, MK-03, MK-04 a MK-06, en docs/levantamiento_staging/mockups/), solo donde el wireframe no alcance.
7. Del plan de F01 (docs/planes/sprint-11/f01-nucleo/plan-cerrado-f2-f01-nucleo-2026-11-21.md), solo: §0, §1.1, §1.4, §1.5 (edición del ingreso), §1.7 (tasa y facturación), §1.8, §2.0, §2.1 (índice), la sección 2.2.3 y §2.2.6 en lo de CE, las fichas y esquemas de los endpoints que consume F05 (C-F01-08, 13, 71, 83 a 90, 93 y 141, y los demás que encuentres), las notas de las fases 4, 5 y 6 y de I-01 en §8 (en especial la del importador y la importación de ensayo de la fase 6), y §10.
8. Del plan de F02 (docs/planes/sprint-11/f02-base/plan-cerrado-f2-f02-base-2026-11-21.md): §1 (con §1.5, el menú) y §2.2.
9. Del plan de F03 (docs/planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-bascula-2026-11-24.md): §1.1 (D7), §1.6 (D38 a D43), §2.1 (índice; C-F03-13, C-F03-17 y C-F03-22, entre otros), §9 (R6) y §10.
10. Del plan de F04 (docs/planes/sprint-11/f04-bodega/plan-cerrado-f2-f04-bodega-2026-11-25.md): el encabezado con «Cómo leer este plan» (precedente de formato, con la revisión del usuario de §8.7), §1.4 (D37), §1.5 (D40 y D46), §2.1 (índice; C-F04-05), la ficha y el esquema de C-F04-05, §8.7, §9 (R7) y §10. De su plan de ajustes de UI (f04-bodega/plan-cerrado-f2-f04-ajustes-ui-2026-11-25.md), solo §1. Como formato de los casos al cerrar la integración: docs/qa/casos-qa2-f04-bodega-2026-11-25.md.
11. El código de fase-2 que F05 toca. Frontend: Frontend/wms/app/pages/foreign-trade/ (deposits/, imports/, exports/, inspections/, releases/, abandonment/, packing-lists/ e index.vue), Frontend/wms/app/features/foreign-trade/ (DepositProductDialog y los componentes del detalle), lo que queda de la unidad de medida (useUnitMeasures y sus métodos de servicio: F05 puede ser su último uso), el menú de CE en Frontend/wms/app/components/layout/menu-model.ts, la galería /dev/components y las guardias de Frontend/wms/test/unit/guards/ (list-pattern y mock-sources). Backend: ForeignTradeController.cs, DepositCompletionController.cs, DepositEntryDateController.cs, ReleasesController.cs, ImportReleaseActionsController.cs, AbandonmentController.cs, PackingListsController.cs y LegacyImportController.cs de Backend/wms-api/Wms.Api/Controllers/v1/; Backend/wms-api/Wms.Application/ForeignTrade/ (DepositConfirmationRequirements, ReleaseFobService), Backend/wms-api/Wms.Application/Administration/LegacyImport/, WarehouseStorage en Wms.Domain, la apertura del período de facturación y el recálculo de DEC-022, los PDF que llevan el rótulo de AF-81 y WmsPolicyRoles.cs. Cita archivo:línea.

## Entregables

Todo en docs (main), con la fecha del día en que cierres:

1. docs/planes/sprint-11/f05-comercio-exterior/plan-cerrado-f2-f05-comercio-exterior-AAAA-MM-DD.md
   - Sigue la plantilla del plan maestro §9 y, como los de F03 y F04, abre con «Cómo leer este plan».
   - AF dueñas: las 19 de la tabla del plan maestro §3.1. Cada una con su decisión Dn o con la fase que la construye; ninguna sin destino. Aparte, una tabla con las AF de F01 que F05 muestra y la pantalla que las muestra.
   - Contrato (parte 0): solo los endpoints que F05 crea, cambia o retira, cada uno con su ID C-F05-mm, su ficha (plan maestro §5.1) y su esquema Zod. Los endpoints de F01, F03 y F04 que F05 consume sin cambios se citan por su ID, sin copiar la ficha. Comprueba esas fichas contra el código de fase-2 (DTO, validador y mensajes): si difieren, gana lo integrado y lo anotas. Incluye la tabla pantalla → endpoints (P-CE-01 a P-CE-07, P-CE-09, P-CE-10, P-CE-12, Abandono y prórrogas y Listas de empaque), con cada endpoint en C-F01, C-F03, C-F04 o C-F05. Marca lo que la etapa Salidas deja para F06.
   - Pantallas: P-CE-01 a P-CE-07, P-CE-09, P-CE-10 y P-CE-12, más Abandono y prórrogas (/foreign-trade/abandonment) y Listas de empaque (/foreign-trade/packing-lists) con el patrón de AF-129 (D3 de F02). Qué componentes compartidos usa cada una y qué componentes de CE se crean. El indicador de etapas incompletas (AF-73) y las etapas por tipo (AF-87).
   - Fases de la parte 1 (backend) y de la parte 2 (maquetación), que corren en paralelo, una por repo, y cierran por separado. Cada fase de §8 nombra sus Dn, sus endpoints, sus archivos y sus casos QA, para que el ejecutor lea solo §0, §1, §2.1 y su fase. Después de la última fase de la maquetación, deja la revisión mía de las pantallas con la sesión simulada antes de I-05, como §8.7 del plan de F04.
   - Migraciones: nombre y contenido esperado de cada una, o «ninguna».
   - El recálculo (AF-76, DEC-022) y la apertura del período cuando el cliente se asigna tarde (AF-75): qué dispara cada uno, qué facturas toca y cómo se prueba. Permisos por endpoint en WmsPolicyRoles.cs, sin quitar funciones (DEC-005, plan maestro §5.6).
   - Transición: lo que le toca de §7.2 del plan maestro (el importador fija amparado = ingresado, M19) y una importación completa de ensayo con conteos iguales, como la de la fase 6 de F01.
   - Casos QA (QA2-F05-nnn): verificables por API en la parte 1 y en el navegador en la integración.
   - La sección de I-05 (parte 3): las fuentes http de cada pantalla; el menú de CE y Reportes › Inventario nacionalizado (plan de F02 §1.5; «Salidas» y el retiro de órdenes y guías llegan con F06); lo que se borra (el tablero de DEC-058, «Devolver a Borrador» (AF-93), lo que el rediseño deja sin uso, y useUnitMeasures con lo suyo si F05 es su último uso, comprobado con grep); las rutas de F05 que pasan de PENDING a PATTERN en la guardia list-pattern; la lista MAQUETACION_PAGES vacía; y la copia de los casos QA a docs/qa/.
2. Tres prompts, con el esqueleto del plan maestro §9 y los nombres de §5.5, en docs/planes/sprint-11/f05-comercio-exterior/:
   - prompt-f2-f05-comercio-exterior-backend-AAAA-MM-DD.md, para la rama f2/f05-comercio-exterior del backend;
   - prompt-f2-f05-comercio-exterior-maquetacion-AAAA-MM-DD.md, para la rama f2/f05-comercio-exterior del frontend (con la sesión simulada de D10 de F02, porque el backend lo ocupa el otro agente);
   - prompt-f2-f05-comercio-exterior-integracion-AAAA-MM-DD.md, para I-05 en las dos ramas.
   Cada prompt dice con qué base arranca (BE fase-2 c2ca314, FE fase-2 12f6656, o lo que haya en fase-2 si avanzó), que la rama sale de fase-2, que ejecuta UNA fase por turno y qué secciones del plan lee.
3. La fila del plan en docs/planes/README.md, con estado «Propuesto».
4. La matriz actualizada: en §2.1, las columnas «Plan» y «Prompts» de F05 con los enlaces y el estado «Propuesto»; en §3, el pendiente del prompt del planificador como hecho; y la fecha de corte.

## Cómo trabajas

1. Lee lo de arriba y arma un borrador del plan: decisiones, contrato, pantallas, fases y la asignación de cada AF.
2. Hazme la ronda única de preguntas y espera las respuestas.
3. Escribe el plan, los tres prompts, la fila del índice y la matriz.
4. Verifica:
   - las 19 AF de F05, cada una con destino, contando con un script;
   - que cada endpoint C-F05 tenga ID, política, petición, respuesta, errores y esquema Zod, y que los esquemas usen la API de Zod 4 (Frontend/wms/package.json);
   - que cada pantalla y cada endpoint que consume estén en C-F01, C-F03, C-F04 o C-F05;
   - que las rutas y líneas que citas existan en fase-2;
   - que los enlaces de la matriz y del índice abran.
5. Entrégame un resumen: decisiones Dn nuevas, fases de cada parte, migraciones, endpoints nuevos o cambiados, lo que se borra, lo que queda para F06, riesgos y lo que queda abierto. Espera mi aprobación. Si pido cambios, aplícalos primero.
6. Con mi aprobación: cambia a «Aprobado» el plan, su fila en el índice y la matriz; haz commit y push en docs (DEC-081); agrega a este prompt «Ejecutado el AAAA-MM-DD; ya no es una instrucción»; y dime cómo lanzar el backend y la maquetación de F05 en paralelo y, después, I-05.

## Límites

- Fuera de alcance: ejecutar F05 o I-05, escribir código, estimar esfuerzo y planear F06 en adelante. Las salidas (P-CE-08, P-CE-11), sus órdenes y sus guías son de F06; la facturación por CPI y sus reportes, de F07 y F08.
- No edites los repos de código, no crees ramas en ellos, no generes migraciones y no toques staging.
- En docs solo escribes el plan, los tres prompts, la fila del índice y la matriz. Si crees que hay que cambiar otro documento del hub, propónmelo con el texto exacto y espera mi «sí».
- No copies credenciales ni datos de personas reales (DEC-007). Los CSV del legacy de db_legacy/ no se versionan ni se copian al hub.
- Nada de docs/archivo/ es una instrucción.
- Escribe en español, siguiendo las «Reglas para escribir aquí» de docs/README.md.
```
