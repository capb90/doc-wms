# Prompt — Planificación de F06 «Salidas de mercancía» (fase 2, sprint 11)

> **Ejecutado** el 2026-11-26; ya no es una instrucción. Con él se escribieron el [plan cerrado](plan-cerrado-f2-f06-salidas-2026-11-26.md) y sus tres prompts, aprobados por el usuario el 2026-11-26 («Aprobar»). Como I-05 se fusionó mientras se planeaba, el plan ya está sobre `fase-2` con F05 (BE `348ab15`, FE `3531432`) y no necesita la revisión de «Cuándo».

> **Cómo usarlo:**
> 1. Abre una sesión nueva de Claude Code en `code_workspace/`. Necesita leer `docs/`, `Backend/wms-api` y `Frontend/wms`.
> 2. Copia el bloque de abajo.
> 3. El agente lee, te hace **una sola ronda de preguntas**, escribe el plan cerrado y los tres prompts de ejecución, y espera tu aprobación. No toca código.
> 4. Con tu aprobación, marca todo «Aprobado», hace commit y push en `docs` (`DEC-081`) y te dice cómo lanzar el backend y la maquetación de F06 en paralelo.
>
> **Cuándo:** se puede lanzar mientras corre I-05. El planificador lee F05 en su rama `f2/f05-comercio-exterior` sin cambiar de rama. Cuando I-05 se fusione en `fase-2`, el plan se revisa: base, notas de §13.6 de F05 y cambios al contrato que haya hecho la integración.
> **Insumos:** el plan maestro (`docs/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md`), el análisis (`docs/levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md`, `DEC-080`) y lo integrado o aprobado de F01 a F05.
> **Base al escribir este prompt:** BE `fase-2` `c2ca314` y FE `fase-2` `12f6656` (F01 a F04 integradas); F05 en `f2/f05-comercio-exterior` (BE `9699194`, FE `2e7c76b`), con I-05 en curso. En el frontend, antes de F06 va el plan de `AppAlertIcon` (`planes/sprint-11/plan-cerrado-f2-alert-icon-f01-f04-2026-11-26.md`), que arranca con la fusión de F05.
> **Modelo recomendado:** Opus 5.5 con esfuerzo **Alto**.
>
> Cuando lo ejecutes, el agente agrega aquí «**Ejecutado** el AAAA-MM-DD; ya no es una instrucción» (plan maestro §5.5). Este prompt no se mueve a `archivo/`.

---

```text
Eres el planificador técnico de la feature F06 «Salidas de mercancía» de la fase 2 del WMS de Bodegas Asociadas (depósito aduanero en Ipiales, Colombia), sprint 11. F06 tiene las cuatro partes: 0 (contrato), 1 (backend), 2 (maquetación del frontend) y 3 (integración I-06).

El plan maestro ya está aprobado y fija las features, el orden, las convenciones y las decisiones M1 a M25. El análisis funcional ya está cerrado (DEC-080). F01 a F04 ya están integradas en fase-2 y F05 está en su integración (I-05), en la rama f2/f05-comercio-exterior. Tu trabajo es escribir el PLAN CERRADO de F06 y sus TRES PROMPTS de ejecución, con una sola ronda de preguntas, y esperar mi aprobación.

## Lo que ya está decidido (no se vuelve a preguntar)

- Todo lo del plan maestro: §1 (M1 a M25; M13: las pantallas de la salida van en F06 y P-BAS-03 queda en Báscula; M15: la cantidad facturable se cuenta por guía; M24: la salida en Borrador reserva stock), §2 (fila de F06, §2.1 «Qué entrega F01 a F06» y las filas de §2.2 que nombran a F06), §3.1, §4 (con F06 vuelven a funcionar completos los flujos que F01 cambió), §5, §6 (incluida «Una fase por turno»), §7 y §9.
- Las AF del análisis (DEC-080) y las decisiones de docs/contexto/decisiones.md, en especial DEC-081 y DEC-012 (la serie de la salida es 2026SM00001, precisada por F01).
- Lo construido e integrado de F01: la salida de mercancía (GoodsExit, recurso exits) con sus cuatro tipos, sus estados, lo que le falta, la reserva de stock, la guía que se emite al confirmar, la inspección sin guía, la edición y anulación de la guía, y su contrato C-F01-94 a C-F01-139, con las correcciones de I-01 y la nota de la fase 5 de su §8 (salidas bloqueadas con el 400 de hoy, vencimiento de la guía, firmante, guardas de importación).
- Lo de F03: la salida en Borrador desde Báscula y la precarga por placa (P-BAS-03, C-F01-101, C-F01-109 a C-F01-111) ya están construidas; F06 no las rehace. D41 de F03: useAddAdditionalOrders y lo de features/weighbridge/ que importa la salida con tiquete se revisa aquí.
- Lo de F04: D10 y D37, los relojes del cargue y de la salida de patio ya están en GET exits y GET exits/{id} (C-F04-03 y C-F04-04, warehouseClock y el filtro warehouseLevel), con el componente WarehouseClockTag (D40). F06 los muestra en Órdenes de salida (P-BOD-06) y puede usarlos en P-BOD-09 y P-CE-11. D45: «Órdenes de cargue» sigue en el menú de Bodega hasta que F06 la reemplace.
- Lo de F05 (aprobado y en integración): D7, la confirmación de la salida exige cliente en cada depósito (C-F05-21, sobre C-F01-98); D38, la etapa Salidas del detalle está vacía y F06 la llena; D43, «Órdenes de cargue» y «Guías de salida» siguen en el menú de CE hasta F06 (AF-97).
- El cobro de la guía usa AppChargeForm sin «Clientes» (AF-106, D13 de F02). F06 es el último uso de BillingCollectForm (D42 de F03, D46 de F04): la integración lo borra, comprobado con grep.
- Las convenciones de interfaz de docs/contexto/convenciones-tecnicas.md §3: «Drawer de detalle», «Tablas de listado», «Aviso junto a un dato» (AppAlertIcon) y «Páginas que no son listados». Aplícalas desde el plan.
- Los avisos nuevos van por el orquestador con roles fijos (plan maestro §2.2); F09 los pasa a tipos.
- Las migraciones las genera y aplica el agente de backend con dotnet ef, solo en local (DEC-004, M6).
- Los datos simulados de la maquetación usan la fuente intercambiable (M12, plan maestro §5.2) y las ayudas de Frontend/wms/app/shared/mocks/.

## Regla principal

- No reabras ni reinterpretes las AF, DEC-080, DEC-081, las M del plan maestro ni las Dn de F01 a F05 y sus ajustes. Si encuentras una contradicción entre ellas, un hueco funcional o un choque con el código que ninguna resuelve, muéstramelo y pregúntame.
- Las decisiones técnicas con alternativas reales las recomiendas y yo decido: forma de los endpoints nuevos, cambios de modelo, qué se parte en qué fase, nombres de rutas y de componentes de las salidas.
- Haz UNA sola ronda de preguntas, con AskUserQuestion en bloques de hasta 4. Cada pregunta se entiende sola: tema, AF o DEC afectadas, qué dicen las fuentes con ruta y línea, opciones con su consecuencia y tu recomendación marcada «(Recomendada)» con su porqué.
- No preguntes lo que una decisión ya resuelve (DEC-002).
- Registra cada respuesta en el plan como decisión Dn, con la fecha y mis palabras.

### Preguntas que ya sé que hay que hacerme (además de las que encuentres)

1. Las rutas y el contenedor de cada pantalla: el listado y «Nueva salida» de CE (P-CE-11, AF-97), Órdenes de salida (P-BOD-06), Ejecutar salida (P-BOD-07, por número de depósito y consolidada), Salida de patio (P-BOD-08, por tiquete de entrada y global) e Historial de salidas de Bodega (P-BOD-09): ¿página, modal o drawer? Los formularios de operación largos van en página (AF-130). Incluye qué pasa con las páginas de hoy que salen (foreign-trade/loading-orders/, foreign-trade/dispatch-guides/ y warehouse/loading-orders/, AF-97) y con la descarga «PDF por depósito (ZIP)», que se conserva solo para las consolidadas.
2. Dónde se ve, se descarga y se anula la guía, ahora que «Guías de salida» sale del menú (AF-97: «la guía se ve, descarga o anula desde su salida») y que la etapa Salidas de CE (P-CE-08) muestra las salidas de un depósito.

## Rutas

- Raíz: /Volumes/Dock/Projects/bodegas_asociadas/code_workspace. Las rutas son relativas a ella.
- Hub: docs/ (main). Backend: Backend/wms-api. Frontend: Frontend/wms.
- I-05 está en curso: los dos repos de código están en f2/f05-comercio-exterior, y el agente de integración puede tener cambios sin commit. NO cambies de rama ni toques el árbol de trabajo. Lee con git show <rama>:<ruta>, git grep <rama> y git log: fase-2 para lo integrado (F01 a F04) y f2/f05-comercio-exterior para F05. No edites nada en los repos de código.

## Cómo lees (cuida el contexto)

- Lee por secciones: usa grep -n para ubicar encabezados e IDs y lee solo esos rangos. Los planes de F01 a F05 tienen entre 1.400 y 2.300 líneas cada uno: NO los leas completos.
- Salidas acotadas: lee por rangos lo que necesites citar; no vuelques archivos de código grandes.

## Lee primero, en este orden

1. docs/README.md, docs/AGENTS.md, Backend/wms-api/AGENTS.md y Frontend/wms/AGENTS.md (su sección «Eficiencia de contexto y cierres por fase» rige a los ejecutores).
2. docs/procesos/flujo-de-trabajo-agentes.md; de docs/contexto/convenciones-tecnicas.md, §3 (frontend y sus convenciones de interfaz), §4 (permisos) y §10 completo (trampas); docs/contexto/estado.md; y de docs/contexto/decisiones.md: DEC-001 a DEC-007, DEC-012, DEC-015, DEC-016, DEC-019, DEC-050, DEC-052, DEC-056, DEC-057, DEC-058, DEC-080 y DEC-081.
3. Del plan maestro (docs/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md): §1, §2 (con §2.1 y §2.2), §3.1, §4, §5, §6, §7, §8 y §9.
4. La matriz: docs/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md.
5. Del análisis docs/levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md: §3.7 completo (modalidades de salida); en §2.2 y §2.3, lo de las salidas (reglas «f», pantallas «g» de P-BOD-06 a P-BOD-09, P-CE-08 y P-CE-11, e impacto «i»); en §2.4, el cobro de la guía; y en §4 las 4 AF dueñas de F06 (AF-67, AF-89, AF-97 y AF-106), las de F01 que F06 muestra (plan maestro §2.1, fila F06: AF-28 a AF-37, AF-42, AF-36, AF-68, AF-88 y AF-90) y AF-54, AF-99 y AF-132, que F06 aplica a sus pantallas. Las fuentes del usuario que cita: docs/levantamiento_staging/salidas_arquitectura.md, la parte de órdenes de salida de docs/levantamiento_staging/bodega_ajustes.md y el mockup docs/levantamiento_staging/mockups/orden_de_salida_bodega/.
6. Los wireframes: de docs/levantamiento-2026-11/fase_2-mockups/bodega.html, P-BOD-06 a P-BOD-09; de comercio-exterior.html, P-CE-08 y P-CE-11 (y P-CE-02, para ver dónde va la etapa); de transversales.html, P-TR-02, P-TR-03, P-TR-09 y P-TR-11.
7. Del plan de F01 (docs/planes/sprint-11/f01-nucleo/plan-cerrado-f2-f01-nucleo-2026-11-21.md), solo: §0, §1.1, §1.6 (salidas), §1.7, §1.8, §2.0, §2.1 (índice, grupo E), la sección 2.2.4 (fichas del grupo E), §2.2.6 (tabla R-SAL), los esquemas de las salidas en §2.3 (F/features/exits/contracts/exit.ts), las notas de la fase 5 y de I-01 en §8, y §10.
8. Del plan de F02 (docs/planes/sprint-11/f02-base/plan-cerrado-f2-f02-base-2026-11-21.md): §1 (con §1.5, el menú) y §2.2 (en especial AppChargeForm).
9. Del plan de F03 (docs/planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-bascula-2026-11-24.md): §1.6 (D41 y D42), §2.1 (índice; lo de la salida en Báscula) y §10.
10. Del plan de F04 (docs/planes/sprint-11/f04-bodega/plan-cerrado-f2-f04-bodega-2026-11-25.md): el encabezado con «Cómo leer este plan» (precedente de formato), §1.1 (D10), §1.4 (D37), §1.5 (D40, D45 y D46), §1.7 (AF-36, AF-66, AF-68 y AF-70), las fichas y esquemas de C-F04-03 y C-F04-04, §8.7 (la revisión del usuario), §9 (R7) y §10.
11. Del plan de F05 (docs/planes/sprint-11/f05-comercio-exterior/plan-cerrado-f2-f05-comercio-exterior-2026-11-25.md): §1.1 (D7), §1.5 (D38, D43 y D46), §2.1 (índice; C-F05-21 y el párrafo «Para F06»), la ficha de C-F05-21, §9 (R9), §10 y, si ya existe, §13.6 (estado de I-05). De su plan de ajustes de UI (f05-comercio-exterior/plan-cerrado-f2-f05-ajustes-ui-2026-11-26.md), solo §1. Como formato de los casos al cerrar la integración: docs/qa/casos-qa2-f04-bodega-2026-11-25.md.
12. El código que F06 toca, con git show y git grep (no cambies de rama). Frontend (fase-2, y f2/f05-comercio-exterior para el detalle de CE y su etapa Salidas): app/pages/foreign-trade/loading-orders/, app/pages/foreign-trade/dispatch-guides/, app/pages/warehouse/loading-orders/, app/features/exits/, el detalle por etapas de F05, app/features/foreign-trade/components/DispatchGuideForm.vue, app/features/billing/components/BillingCollectForm.vue y ChangePaymentModeDialog.vue, lo de features/weighbridge/ que importa la salida (D41 de F03), el menú en app/components/layout/menu-model.ts, la galería /dev/components y las guardias de test/unit/guards/ (list-pattern y mock-sources). Backend (fase-2): Wms.Api/Controllers/v1/ExitsController.cs y PublicDispatchGuideVerificationController.cs, Wms.Application/Exits/, la salida y la guía en Wms.Domain, la generación de la guía en PDF, el orquestador de avisos y WmsPolicyRoles.cs. Cita rama, archivo y línea.

## Entregables

Todo en docs (main), con la fecha del día en que cierres:

1. docs/planes/sprint-11/f06-salidas/plan-cerrado-f2-f06-salidas-AAAA-MM-DD.md
   - Sigue la plantilla del plan maestro §9 y, como los de F03 a F05, abre con «Cómo leer este plan».
   - AF dueñas: las 4 de la tabla del plan maestro §3.1. Cada una con su decisión Dn o con la fase que la construye; ninguna sin destino. Aparte, una tabla con las AF de F01 que F06 muestra y la pantalla que las muestra.
   - Contrato (parte 0): solo los endpoints que F06 crea, cambia o retira, cada uno con su ID C-F06-mm, su ficha (plan maestro §5.1) y su esquema Zod. Los endpoints de F01, F03, F04 y F05 que F06 consume sin cambios se citan por su ID, sin copiar la ficha. Comprueba esas fichas contra el código (DTO, validador y mensajes): si difieren, gana lo integrado y lo anotas. Incluye la tabla pantalla → endpoints (P-CE-08, P-CE-11 y P-BOD-06 a P-BOD-09), con cada endpoint en C-F01, C-F03, C-F04, C-F05 o C-F06.
   - Pantallas: P-CE-08 (la etapa Salidas que F05 dejó vacía), P-CE-11 y P-BOD-06 a P-BOD-09, con el cobro de la guía. Qué componentes compartidos usa cada una y qué componentes de salidas se crean.
   - Fases de la parte 1 (backend) y de la parte 2 (maquetación), que corren en paralelo, una por repo, y cierran por separado. Cada fase de §8 nombra sus Dn, sus endpoints, sus archivos y sus casos QA, para que el ejecutor lea solo §0, §1, §2.1 y su fase. Después de la última fase de la maquetación, deja la revisión mía de las pantallas con la sesión simulada antes de I-06, como §8.7 del plan de F04.
   - Migraciones: nombre y contenido esperado de cada una, o «ninguna».
   - Avisos nuevos, si los hay, y permisos por endpoint en WmsPolicyRoles.cs, sin quitar funciones (DEC-005, plan maestro §5.6).
   - Transición: lo que le toca de §7.2 del plan maestro (las órdenes de cargue abiertas no se convierten, M18), o «no aplica».
   - Casos QA (QA2-F06-nnn): verificables por API en la parte 1 y en el navegador en la integración. Como F06 cierra el flujo, incluye al menos un caso de punta a punta en el navegador: Vigilancia, Báscula, Bodega, Comercio Exterior (confirmar el depósito y nacionalizar), nueva salida, confirmar con su guía y su cobro, cargue, pesaje de salida y salida de patio.
   - La sección de I-06 (parte 3): las fuentes http de cada pantalla; el menú de CE («Salidas») y de Bodega («Órdenes de salida» y «Salidas»), sin «Órdenes de cargue» ni «Guías de salida»; lo que se borra (las páginas y componentes de la orden de cargue y de la guía por orden, BillingCollectForm y lo que quede sin uso, comprobado con grep); las rutas de F06 que pasan de PENDING a PATTERN en la guardia list-pattern; la lista MAQUETACION_PAGES vacía; la copia de los casos QA a docs/qa/; y el aviso al usuario de que, con F06 integrada, el flujo de entrada y salida está completo para probarlo en local.
2. Tres prompts, con el esqueleto del plan maestro §9 y los nombres de §5.5, en docs/planes/sprint-11/f06-salidas/:
   - prompt-f2-f06-salidas-backend-AAAA-MM-DD.md, para la rama f2/f06-salidas del backend;
   - prompt-f2-f06-salidas-maquetacion-AAAA-MM-DD.md, para la rama f2/f06-salidas del frontend (con la sesión simulada de D10 de F02, porque el backend lo ocupa el otro agente);
   - prompt-f2-f06-salidas-integracion-AAAA-MM-DD.md, para I-06 en las dos ramas.
   Cada prompt dice que la rama sale de fase-2 cuando I-05 esté fusionada (y, en el frontend, también el plan de AppAlertIcon), con lo que haya en fase-2 en ese momento; que ejecuta UNA fase por turno; y qué secciones del plan lee.
3. La fila del plan en docs/planes/README.md, con estado «Propuesto».
4. La matriz actualizada: en §2.1, las columnas «Plan» y «Prompts» de F06 con los enlaces y el estado «Propuesto»; en §3, el pendiente del prompt del planificador como hecho; y la fecha de corte. El agente de I-05 y el planificador de F07 escriben a la vez en la matriz y el índice: antes de cada commit haz git pull --rebase en docs y toca solo tus filas.

## Cómo trabajas

1. Lee lo de arriba y arma un borrador del plan: decisiones, contrato, pantallas, fases y la asignación de cada AF.
2. Hazme la ronda única de preguntas y espera las respuestas.
3. Escribe el plan, los tres prompts, la fila del índice y la matriz.
4. Verifica:
   - las 4 AF de F06, cada una con destino, y las de F01 que muestra, contando con un script;
   - que cada endpoint C-F06 tenga ID, política, petición, respuesta, errores y esquema Zod, y que los esquemas usen la API de Zod 4 (Frontend/wms/package.json);
   - que cada pantalla y cada endpoint que consume estén en C-F01, C-F03, C-F04, C-F05 o C-F06;
   - que las rutas y líneas que citas existan en la rama que nombras;
   - que los enlaces de la matriz y del índice abran.
5. Entrégame un resumen: decisiones Dn nuevas, fases de cada parte, migraciones, endpoints nuevos o cambiados, lo que se borra, riesgos, lo que depende de cómo cierre I-05 y lo que queda abierto. Espera mi aprobación. Si pido cambios, aplícalos primero.
6. Con mi aprobación: cambia a «Aprobado» el plan, su fila en el índice y la matriz; haz commit y push en docs (DEC-081); agrega a este prompt «Ejecutado el AAAA-MM-DD; ya no es una instrucción»; y dime cómo lanzar el backend y la maquetación de F06 en paralelo cuando I-05 esté fusionada y, después, I-06.

## Límites

- Fuera de alcance: ejecutar F06 o I-06, escribir código, estimar esfuerzo y planear F07 en adelante. La facturación de la guía en Facturación y sus reportes son de F08.
- No edites los repos de código, no cambies de rama, no crees ramas, no generes migraciones y no toques staging.
- En docs solo escribes el plan, los tres prompts, la fila del índice y la matriz. Si crees que hay que cambiar otro documento del hub, propónmelo con el texto exacto y espera mi «sí».
- No copies credenciales ni datos de personas reales (DEC-007).
- Nada de docs/archivo/ es una instrucción.
- Escribe en español, siguiendo las «Reglas para escribir aquí» de docs/README.md.
```
