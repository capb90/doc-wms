# Prompt — Planificación de F04 «Bodega» (fase 2, sprint 11)

> **Cómo usarlo:**
> 1. Abre una sesión nueva de Claude Code en `code_workspace/`. Necesita leer `docs/`, `Backend/wms-api` y `Frontend/wms`, los dos en su rama `fase-2`.
> 2. Copia el bloque de abajo.
> 3. El agente lee, te hace **una sola ronda de preguntas**, escribe el plan cerrado y los tres prompts de ejecución, y espera tu aprobación. No toca código.
> 4. Con tu aprobación, marca todo «Aprobado», hace commit y push en `docs` (`DEC-081`) y te dice cómo lanzar el backend y la maquetación de F04 en paralelo.
>
> **Insumos:** el plan maestro (`docs/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md`), el análisis (`docs/levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md`, `DEC-080`) y lo ya integrado de F01, F02 y F03, con sus ajustes.
> **Base:** BE `fase-2` `eb4e428` (F01 y F03 integradas, con los ajustes de la QA de F03) · FE `fase-2` `2c848af` (F02 y F03 integradas, con sus ajustes y las páginas sin tarjeta de título) · `develop` sin cambios (BE `529bda7`, FE `3aa6e3c`).
> **Modelo recomendado:** Opus 5.5 con esfuerzo **Alto**.
>
> Cuando lo ejecutes, el agente agrega aquí «**Ejecutado** el AAAA-MM-DD; ya no es una instrucción» (plan maestro §5.5). Este prompt no se mueve a `archivo/`.

---

```text
Eres el planificador técnico de la feature F04 «Bodega» de la fase 2 del WMS de Bodegas Asociadas (depósito aduanero en Ipiales, Colombia), sprint 11. F04 tiene las cuatro partes: 0 (contrato), 1 (backend), 2 (maquetación del frontend) y 3 (integración I-04).

El plan maestro ya está aprobado y fija las features, el orden, las convenciones y las decisiones M1 a M25. El análisis funcional ya está cerrado (DEC-080). F01 (núcleo), F02 (base transversal) y F03 (Báscula) ya están integradas en fase-2, con los ajustes de sus QA manuales. Tu trabajo es escribir el PLAN CERRADO de F04 y sus TRES PROMPTS de ejecución, con una sola ronda de preguntas, y esperar mi aprobación.

## Lo que ya está decidido (no se vuelve a preguntar)

- Todo lo del plan maestro: §1 (M1 a M25; M18: llegadas y órdenes de cargue abiertas no se convierten; M25: un solo despliegue a staging al final de toda la fase 2), §2 (fila de F04, §2.1 «Qué entrega F01 a F04» y las filas de §2.2 que nombran a F04), §3.1 y sus notas (AF-105 y AF-119 quedan en F04), §5, §6 (incluida «Una fase por turno»), §7 (los relojes arrancan con los registros nuevos) y §9.
- Las AF del análisis (DEC-080) y las decisiones de docs/contexto/decisiones.md, en especial DEC-081.
- Lo construido e integrado de F01 (D1 a D47 y su contrato C-F01-*, con las correcciones de I-01), de F02 (D1 a D21, con D3: Inventario y Novedades pasan al patrón de AF-129 en F04, y D1: las páginas nuevas de Administración van en /admin/…) y de F03 (sus Dn y su contrato C-F03-*, con D41: lo de features/weighbridge/ que Bodega importa se conserva, y D42: el montacargas sigue con BillingCollectForm hasta F04).
- Las convenciones de interfaz que salieron de las QA manuales y ya están en docs/contexto/convenciones-tecnicas.md §3: «Drawer de detalle» (acciones en el menú del encabezado, sin pie), «Tablas de listado» (AppRowActions, botones pequeños con borde, más de tres acciones en el menú, filtros en la columna) y «Páginas que no son listados» (sin tarjeta de título, con <h1 class="sr-only">). Aplícalas desde el plan: en F03 se aprendieron con dos planes de ajustes.
- Regla de pertenencia (plan maestro §2): F04 construye la regla de los tres relojes y sus umbrales (AF-56, AF-57, AF-65): su cálculo, su configuración (P-TR-08), el trabajo en segundo plano que detecta el cruce y el aviso. Los expone en su contrato. Las pantallas de otras features que los muestran los citan: el reloj del cargue en las salidas de Bodega (F06) y los de Bodega en la etapa Bodega del detalle de CE (F05).
- El dato «Queda sobre el vehículo» (AF-119) lo guarda F04 en la recepción; la fórmula que lo usa es de F07 (AF-116, AF-120). Las columnas de «Requiere factura» (AF-105) en Facturación son de F08 (P-FAC-02).
- Los avisos nuevos van por el orquestador con roles fijos (plan maestro §2.2); F09 los pasa a tipos.
- Las migraciones las genera y aplica el agente de backend con dotnet ef, solo en local (DEC-004, M6).
- Los datos simulados de la maquetación usan la fuente intercambiable (M12, plan maestro §5.2) y las ayudas de Frontend/wms/app/shared/mocks/.

## Regla principal

- No reabras ni reinterpretes las AF, DEC-080, DEC-081, las M del plan maestro ni las Dn de F01, F02, F03 y sus ajustes. Si encuentras una contradicción entre ellas, un hueco funcional o un choque con el código que ninguna resuelve, muéstramelo y pregúntame.
- Las decisiones técnicas con alternativas reales las recomiendas y yo decido: forma de los endpoints nuevos, cambios de modelo, qué se parte en qué fase, nombres de rutas y de componentes de Bodega.
- Haz UNA sola ronda de preguntas, con AskUserQuestion en bloques de hasta 4. Cada pregunta se entiende sola: tema, AF o DEC afectadas, qué dicen las fuentes con ruta y línea, opciones con su consecuencia y tu recomendación marcada «(Recomendada)» con su porqué.
- No preguntes lo que una decisión ya resuelve (DEC-002).
- Registra cada respuesta en el plan como decisión Dn, con la fecha y mis palabras.

### Preguntas que ya sé que hay que hacerme (además de las que encuentres)

1. Los umbrales amarillo y rojo sin los valores del cliente (AF-57; pendiente 1 de §4 de la matriz; plan maestro §3.4: se configuran en P-TR-08 y se cargan antes del despliegue final). Mientras un registro no tenga umbral configurado, ¿el reloj corre sin color ni aviso, o la semilla trae valores provisionales?
2. El IVA del montacargas con «Requiere factura» (AF-105, que reemplaza a DEC-018). Hoy el IVA es un impuesto sembrado que se asigna al servicio, y F07 va a evaluar llevar el porcentaje al precio, como el legacy (plan maestro §3.4, última fila). ¿Cómo calcula F04 el IVA hasta F07 sin adelantarse a ese rediseño?
3. Las rutas: la recepción directa en página (P-BOD-03), Administración › Umbrales de alertas (P-TR-08, bajo /admin/…) y lo que pasa con las páginas de hoy que el rediseño deja sin uso. La página «Ingresos» (/warehouse/receptions/entry) y el registro de la llegada salen (AF-64, AF-65); revisa también receptions/[id].vue, receptions/history.vue, forklift/index.vue y el tablero /warehouse. Una página que ya existe conserva su ruta (plan maestro §5.5).

## Rutas

- Raíz: /Volumes/Dock/Projects/bodegas_asociadas/code_workspace. Las rutas son relativas a ella.
- Hub: docs/ (main). Backend: Backend/wms-api (rama fase-2). Frontend: Frontend/wms (rama fase-2).
- Si un repo de código no está en fase-2 y no tiene cambios sin commit, haz git fetch y cámbialo a fase-2 solo para leer. Si tiene cambios sin commit u otra sesión trabaja en él, no cambies de rama: lee con git show fase-2:<ruta> y git grep fase-2. No edites nada en los repos de código.

## Cómo lees (cuida el contexto)

- Lee por secciones: usa grep -n para ubicar encabezados e IDs y lee solo esos rangos. El plan de F01 tiene unas 2.300 líneas y el de F03 unas 1.700: NO los leas completos.
- Salidas acotadas: lee por rangos lo que necesites citar; no vuelques archivos de código grandes (Frontend/wms/app/pages/warehouse/inventory/index.vue tiene 663 líneas).

## Lee primero, en este orden

1. docs/README.md, docs/AGENTS.md, Backend/wms-api/AGENTS.md y Frontend/wms/AGENTS.md (su sección «Eficiencia de contexto y cierres por fase» rige a los ejecutores).
2. docs/procesos/flujo-de-trabajo-agentes.md; de docs/contexto/convenciones-tecnicas.md, §3 (frontend y sus convenciones de interfaz), §4 (permisos), §6 (trabajos en segundo plano) y §10 (trampas, en especial la 4, la 7 y la 12); docs/contexto/estado.md; y de docs/contexto/decisiones.md: DEC-001 a DEC-007, DEC-010, DEC-018, DEC-041, DEC-052, DEC-056, DEC-057, DEC-058, DEC-080 y DEC-081.
3. Del plan maestro (docs/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md): §1, §2 (con §2.1 y §2.2), §3.1 y sus notas, §3.3, §3.4, §4, §5, §6, §7, §8 y §9.
4. La matriz: docs/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md (con §4, datos del cliente).
5. Del análisis docs/levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md: §2.2 completo (Bodega, a a j), §3.1 (quién configura los umbrales), §3.3 (patrones), §3.4 (notificaciones y alertas), y en §4 las 13 AF dueñas de F04 (AF-56, AF-57, AF-58, AF-59, AF-60, AF-61, AF-62, AF-63, AF-64, AF-65, AF-69, AF-105 y AF-119), las de F01 que F04 muestra (plan maestro §2.1, fila F04) y AF-54, AF-99 y AF-132, que F04 aplica a sus pantallas. AF-64 remite a docs/levantamiento_staging/bodega_ajustes.md: léelo.
6. Los wireframes: docs/levantamiento-2026-11/fase_2-mockups/bodega.html, P-BOD-01 a P-BOD-05 (P-BOD-06 a P-BOD-09 son de F06: míralos solo para ver dónde se muestra el reloj del cargue); de transversales.html, P-TR-02, P-TR-03, P-TR-08, P-TR-09 y P-TR-11.
7. Del plan de F01 (docs/planes/sprint-11/f01-nucleo/plan-cerrado-f2-f01-nucleo-2026-11-21.md), solo: §0, §1.1, §1.4 (en especial D23, D24 y D25), §1.6 (la guía emitida, que arranca el reloj del cargue), §1.8, §2.0, §2.1 (índice), §2.2.6 (las lecturas de Bodega, C-F01-146 a C-F01-152), las fichas y esquemas de los endpoints que consume F04 (C-F01-17, 24, 43 y los demás que encuentres), las notas de las fases 3, 4 y 5 y de I-01 en §8, y §10.
8. Del plan de F02 (docs/planes/sprint-11/f02-base/plan-cerrado-f2-f02-base-2026-11-21.md): §1 (con §1.5, el menú) y §2.2 (en especial AppChargeForm). Del plan de sus ajustes (f02-base/plan-cerrado-f2-f02-ajustes-qa-2026-11-24.md): §1 y §2.
9. Del plan de F03 (docs/planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-bascula-2026-11-24.md): el encabezado con «Cómo leer este plan» (precedente de formato), §1.6 (D38 a D43), §1.8, §2.0, §2.1 (índice; qué C-F03 lee Bodega), §10, §13.3 y §13.6. De sus dos planes de ajustes (f03-bascula/plan-cerrado-f2-f03-ajustes-ui-2026-11-24.md y f03-bascula/plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md), solo §1. Como formato de los casos al cerrar la integración: docs/qa/casos-qa2-f03-bascula-2026-11-24.md.
10. El código de fase-2 que F04 toca. Frontend: Frontend/wms/app/pages/warehouse/ (receptions/, forklift/, inventory/, novelties/ e index.vue), Frontend/wms/app/features/warehouse/ (ReceptionStep*, ForkliftUseDialog, PendingFromWeighbridgeList, DirectReceptionList y lo que importan de features/weighbridge/), el menú de Bodega en Frontend/wms/app/components/layout/menu-model.ts, la galería /dev/components y las guardias de Frontend/wms/test/unit/guards/ (list-pattern y mock-sources). Backend: los controladores de Bodega de Backend/wms-api/Wms.Api/Controllers/v1/ (Warehouse*Controller.cs, InventoryAdjustmentController.cs, ForkliftRateController.cs), Backend/wms-api/Wms.Application/Warehouse/, las entidades de recepción y montacargas en Wms.Domain, Backend/wms-api/Wms.Api/BackgroundJobs/, el orquestador de avisos y WmsPolicyRoles.cs. Cita archivo:línea.

## Entregables

Todo en docs (main), con la fecha del día en que cierres:

1. docs/planes/sprint-11/f04-bodega/plan-cerrado-f2-f04-bodega-AAAA-MM-DD.md
   - Sigue la plantilla del plan maestro §9 y, como el de F03, abre con «Cómo leer este plan».
   - AF dueñas: las 13 de la tabla del plan maestro §3.1. Cada una con su decisión Dn o con la fase que la construye; ninguna sin destino. Aparte, una tabla con las AF de F01 que F04 muestra y la pantalla que las muestra.
   - Contrato (parte 0): solo los endpoints que F04 crea, cambia o retira, cada uno con su ID C-F04-mm, su ficha (plan maestro §5.1) y su esquema Zod. Los endpoints de F01 y F03 que F04 consume sin cambios se citan por su ID, sin copiar la ficha. Comprueba esas fichas contra el código de fase-2 (DTO, validador y mensajes): si difieren, gana lo integrado y lo anotas. Incluye la tabla pantalla → endpoints (P-BOD-01 a P-BOD-05, P-TR-08, Inventario y Novedades), con cada endpoint en C-F01, C-F03 o C-F04. Marca qué campos de los relojes quedan para F05 y F06.
   - Pantallas: P-BOD-01 a P-BOD-05 y P-TR-08, más Inventario (/warehouse/inventory) y Novedades (/warehouse/novelties) con el patrón de AF-129 (D3 de F02). Qué componentes compartidos usa cada una y qué componentes de Bodega se crean. El cobro del montacargas pasa a AppChargeForm (P-TR-09).
   - Fases de la parte 1 (backend) y de la parte 2 (maquetación), que corren en paralelo, una por repo, y cierran por separado. Cada fase de §8 nombra sus Dn, sus endpoints, sus archivos y sus casos QA, para que el ejecutor lea solo §0, §1, §2.1 y su fase. Después de la última fase de la maquetación, deja un punto de revisión mía de las pantallas con la sesión simulada antes de I-04 (en F03 salieron de ahí los ajustes de UI).
   - Migraciones: nombre y contenido esperado de cada una, o «ninguna».
   - El trabajo en segundo plano de los relojes: cada cuánto corre, cómo evita avisar dos veces por el mismo cruce y cómo se prueba. Permisos por endpoint en WmsPolicyRoles.cs, sin quitar funciones (DEC-005, plan maestro §5.6).
   - Transición: lo que le toca de §7.2 del plan maestro (llegadas que desaparecen, relojes desde los registros nuevos) y lo que cambia en el importador del legacy, si algo.
   - Casos QA (QA2-F04-nnn): verificables por API en la parte 1 y en el navegador en la integración.
   - La sección de I-04 (parte 3): las fuentes http de cada pantalla; el menú de Bodega y Administración › Umbrales de alertas (plan de F02 §1.5; «Salidas» y las órdenes llegan con F06); lo que se borra (la página «Ingresos», lo de la llegada, y BillingCollectForm o useUnitMeasures solo si F04 es su último uso, comprobado con grep); las rutas de F04 que pasan de PENDING a PATTERN en la guardia list-pattern; la lista MAQUETACION_PAGES vacía; y la copia de los casos QA a docs/qa/.
2. Tres prompts, con el esqueleto del plan maestro §9 y los nombres de §5.5, en docs/planes/sprint-11/f04-bodega/:
   - prompt-f2-f04-bodega-backend-AAAA-MM-DD.md, para la rama f2/f04-bodega del backend;
   - prompt-f2-f04-bodega-maquetacion-AAAA-MM-DD.md, para la rama f2/f04-bodega del frontend (con la sesión simulada de D10 de F02, porque el backend lo ocupa el otro agente);
   - prompt-f2-f04-bodega-integracion-AAAA-MM-DD.md, para I-04 en las dos ramas.
   Cada prompt dice con qué base arranca (BE fase-2 eb4e428, FE fase-2 2c848af, o lo que haya en fase-2 si avanzó), que la rama sale de fase-2, que ejecuta UNA fase por turno y qué secciones del plan lee.
3. La fila del plan en docs/planes/README.md, con estado «Propuesto».
4. La matriz actualizada: en §2.1, las columnas «Plan» y «Prompts» de F04 con los enlaces y el estado «Propuesto»; en §3, el pendiente del prompt del planificador como hecho; y la fecha de corte.

## Cómo trabajas

1. Lee lo de arriba y arma un borrador del plan: decisiones, contrato, pantallas, fases y la asignación de cada AF.
2. Hazme la ronda única de preguntas y espera las respuestas.
3. Escribe el plan, los tres prompts, la fila del índice y la matriz.
4. Verifica:
   - las 13 AF de F04, cada una con destino, contando con un script;
   - que cada endpoint C-F04 tenga ID, política, petición, respuesta, errores y esquema Zod, y que los esquemas usen la API de Zod 4 (Frontend/wms/package.json);
   - que cada pantalla y cada endpoint que consume estén en C-F01, C-F03 o C-F04;
   - que las rutas y líneas que citas existan en fase-2;
   - que los enlaces de la matriz y del índice abran.
5. Entrégame un resumen: decisiones Dn nuevas, fases de cada parte, migraciones, endpoints nuevos o cambiados, lo que se borra, lo que queda para F05 y F06, riesgos y lo que queda abierto. Espera mi aprobación. Si pido cambios, aplícalos primero.
6. Con mi aprobación: cambia a «Aprobado» el plan, su fila en el índice y la matriz; haz commit y push en docs (DEC-081); agrega a este prompt «Ejecutado el AAAA-MM-DD; ya no es una instrucción»; y dime cómo lanzar el backend y la maquetación de F04 en paralelo y, después, I-04.

## Límites

- Fuera de alcance: ejecutar F04 o I-04, escribir código, estimar esfuerzo y planear F05 en adelante. Las salidas de Bodega (P-BOD-06 a P-BOD-09) son de F06.
- No edites los repos de código, no crees ramas en ellos, no generes migraciones y no toques staging.
- En docs solo escribes el plan, los tres prompts, la fila del índice y la matriz. Si crees que hay que cambiar otro documento del hub, propónmelo con el texto exacto y espera mi «sí».
- No copies credenciales ni datos de personas reales (DEC-007).
- Nada de docs/archivo/ es una instrucción.
- Escribe en español, siguiendo las «Reglas para escribir aquí» de docs/README.md.
```
