# Prompt — Planificación de F01 «Núcleo de dominio» y F02 «Base transversal» (fase 2, sprint 11)

> **Ejecutado** el 2026-11-21; ya no es una instrucción. Resultado: `f01-nucleo/plan-cerrado-f2-f01-nucleo-2026-11-21.md` y `../f02-base/plan-cerrado-f2-f02-base-2026-11-21.md`, con sus tres prompts, aprobados el 2026-11-21.

> **Cómo usarlo:**
> 1. Abre una sesión nueva de Claude Code en `code_workspace/`. Necesita leer `docs/`, `Backend/wms-api` y `Frontend/wms`, los dos en su rama `fase-2`.
> 2. Copia el bloque de abajo.
> 3. El agente lee, te hace **una sola ronda de preguntas**, escribe los dos planes cerrados y los tres prompts de ejecución, y espera tu aprobación. No toca código.
> 4. Con tu aprobación, marca todo «Aprobado», hace commit y push en `docs` (`DEC-081`) y te dice cómo lanzar F01 y F02 en paralelo.
>
> **Insumos:** `docs/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md` (aprobado) y `docs/levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md` (`DEC-080`).
> **Base:** BE `fase-2` `529bda7` (con P0 fusionado) · FE `fase-2` `3aa6e3c`.
> **Modelo recomendado:** Opus 5.5 con esfuerzo **Alto**.
>
> Cuando lo ejecutes, el agente agrega aquí «**Ejecutado** el AAAA-MM-DD; ya no es una instrucción» (plan maestro §5.5). Este prompt no se mueve a `archivo/`.

---

```text
Eres el planificador técnico de dos features de la fase 2 del WMS de Bodegas Asociadas (depósito aduanero en Ipiales, Colombia), sprint 11:
- F01 «Núcleo de dominio»: solo backend (partes 0 y 1).
- F02 «Base transversal»: solo maquetación del frontend (parte 2).
Se planean juntas porque F02 maqueta contra el contrato de F01, y las dos se integran después en I-01 (parte 3).

El plan maestro ya está aprobado y fija las features, el orden, las convenciones y las decisiones M1 a M24. El análisis funcional ya está cerrado (DEC-080). Tu trabajo es escribir los DOS PLANES CERRADOS y los TRES PROMPTS de ejecución, con una sola ronda de preguntas, y esperar mi aprobación.

## Lo que ya está decidido (no se vuelve a preguntar)

- Todo lo de docs/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md: §1 (M1 a M24), §2 (features, AF dueñas, qué entrega F01 a las demás y dónde chocan las features), §5 (convenciones), §6 (compuertas), §7 (transición de datos) y §9 (plantilla del plan cerrado).
- Las 137 AF del análisis (DEC-080) y las decisiones de docs/contexto/decisiones.md, en especial DEC-081 (ramas, un agente por repo, despliegue por grupos, cantidad facturable por guía y reserva de stock de la salida en Borrador).
- Las migraciones las genera y aplica el agente de backend con dotnet ef, solo en local (DEC-004, M6).
- Los datos simulados de la maquetación usan la fuente intercambiable (M12, plan maestro §5.2).

## Regla principal

- No reabras ni reinterpretes las AF, DEC-080, DEC-081 ni las M del plan maestro. Si encuentras una contradicción entre ellas, un hueco funcional o un choque con el código que ninguna resuelve, muéstramelo y pregúntame.
- Las decisiones técnicas con alternativas reales las recomiendas y yo decido: forma del modelo y de las tablas, forma de los endpoints, qué se parte en qué fase, nombres de rutas y de componentes compartidos.
- Haz UNA sola ronda de preguntas para los dos planes, con AskUserQuestion en bloques de hasta 4. Cada pregunta se entiende sola: tema, AF o DEC afectadas, qué dicen las fuentes con ruta y línea, opciones con su consecuencia y tu recomendación marcada «(Recomendada)» con su porqué.
- No preguntes lo que una decisión ya resuelve (DEC-002).
- Registra cada respuesta en el plan que corresponda como decisión Dn, con la fecha y mis palabras.

### Preguntas que ya sé que hay que hacerme (además de las que encuentres)

1. La serie del consecutivo de la salida de mercancía. DEC-012 tiene `2026OC00001` para la orden de cargue, que la salida reemplaza (riesgo R12 del plan maestro).
2. Los prefijos de ruta de las secciones nuevas del menú (Configuración, Tarifas y acuerdos, Reportes y Administración), que el plan maestro §5.5 deja al plan de F02. Una página que ya existe conserva su ruta.

## Rutas

- Raíz: /Volumes/Dock/Projects/bodegas_asociadas/code_workspace. Las rutas son relativas a ella.
- Hub: docs/ (main). Backend: Backend/wms-api (rama fase-2). Frontend: Frontend/wms (rama fase-2).
- Si un repo de código no está en fase-2, haz git fetch y cámbialo a fase-2 solo para leer; no edites nada en los repos de código.

## Lee primero, en este orden

1. docs/README.md, docs/AGENTS.md, Backend/wms-api/AGENTS.md y Frontend/wms/AGENTS.md.
2. docs/procesos/flujo-de-trabajo-agentes.md, docs/contexto/convenciones-tecnicas.md, docs/contexto/estado.md y, de docs/contexto/decisiones.md, DEC-001 a DEC-007, DEC-012, DEC-014, DEC-015, DEC-022, DEC-028, DEC-029, DEC-030, DEC-031, DEC-043, DEC-056, DEC-057, DEC-058, DEC-080 y DEC-081.
3. El plan maestro COMPLETO: docs/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md.
4. La matriz: docs/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md.
5. Del análisis docs/levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md:
   - para F01: §2.1 f, §2.2 f (salidas y salida de patio), §2.3 f (confirmación, edición, valor y amparados), §3.5, §3.6, §3.7, §3.8 y en §4 cada AF dueña de F01;
   - para F02: §3.1, §3.2 y §3.3, y en §4 las AF dueñas de F02.
6. Los wireframes docs/levantamiento-2026-11/fase_2-mockups/transversales.html (P-TR-01 a P-TR-06 y P-TR-09 a P-TR-11) y, para ver cómo se usan los componentes compartidos, bascula.html y comercio-exterior.html.
7. Como precedentes de formato: docs/planes/paridad-legacy/contrato-api-paridad.md (§0 y C-F1-01) y docs/planes/plan-cerrado-dec-057-hallazgos-operarios-2026-10-26.md.
8. El código de fase-2 que cita el plan maestro en §2.2, y todo lo que F01 y F02 tocan. Cita archivo:línea.

## Entregables

Todo en docs (main), con la fecha del día en que cierres:

1. docs/planes/sprint-11/f01-nucleo/plan-cerrado-f2-f01-nucleo-AAAA-MM-DD.md
   - Sigue la plantilla del plan maestro §9.
   - AF dueñas: las 42 de la tabla del plan maestro §3.1. Cada una con su decisión Dn o con la fase que la construye; ninguna sin destino.
   - Contrato (parte 0): todos los endpoints nuevos, cambiados o retirados del núcleo, incluidos los que maqueta F02 (plan maestro §2.1) y la convención de orden y filtros por columna en el servidor sobre QueryParametersBase (plan maestro §5.1). Cada endpoint con su ID C-F01-mm y sus esquemas Zod.
   - Fases de la parte 1, que cierran por separado. El riesgo R1 del plan maestro propone: catálogos y configuración; entradas y pesos; edición del ingreso; salidas; efectos en facturación (cantidad por guía, peso de mercancía, PER_UOM, tasa semanal).
   - Migraciones: nombre y contenido esperado de cada una.
   - Transición: lo que le toca de §7.2 del plan maestro, incluida la adaptación del importador del legacy a las entidades que cambia.
   - Casos QA (QA2-F01-nnn), verificables por API, porque F01 no tiene pantallas.
   - La sección de I-01 (parte 3): qué pantallas de F02 se conectan a qué endpoints, y sus casos QA en el navegador.
2. docs/planes/sprint-11/f02-base/plan-cerrado-f2-f02-base-AAAA-MM-DD.md
   - Sigue la plantilla del plan maestro §9.
   - AF dueñas: las 10 de la tabla del plan maestro §3.1.
   - Pantallas: P-TR-01 a P-TR-06 y P-TR-09 a P-TR-11, más los catálogos de Configuración y Administración (Usuarios, Auditoría) con el patrón nuevo.
   - Componentes compartidos: listado con filtros por columna y orden, selector con búsqueda y alta rápida, drawer de detalle, CRUD en modal y formulario de cobro. Nombres, props y quién los usa después (F03 a F09).
   - Las ayudas de datos simulados en Frontend/wms/app/shared/mocks/ (plan maestro §5.2) y la guardia de «sin llamadas reales» (§6.2).
   - El reemplazo de la guardia FT/unit/guards/page-header.spec.ts:45-53 (DEC-058) por la del patrón de AF-129.
   - Lo que se borra: la página de unidades de medida (M21), lo que el menú nuevo deja sin uso y sus pruebas.
   - El contrato lo cita del plan de F01; no lo duplica.
   - Fases de la parte 2 y casos QA (QA2-F02-nnn), que se verifican en I-01.
3. Tres prompts, con el esqueleto del plan maestro §9 y los nombres de §5.5:
   - docs/planes/sprint-11/f01-nucleo/prompt-f2-f01-nucleo-backend-AAAA-MM-DD.md, para la rama f2/f01-nucleo del backend;
   - docs/planes/sprint-11/f02-base/prompt-f2-f02-base-maquetacion-AAAA-MM-DD.md, para la rama f2/f02-base del frontend;
   - docs/planes/sprint-11/f01-nucleo/prompt-f2-f01-nucleo-integracion-AAAA-MM-DD.md, para I-01 en las dos ramas.
   Cada prompt dice con qué base arranca (BE fase-2 529bda7, FE fase-2 3aa6e3c, o lo que haya en fase-2 si avanzó) y que la rama de la feature sale de fase-2.
4. Las filas de los dos planes en docs/planes/README.md, con estado «Propuesto».
5. La matriz actualizada: en §2.1, las columnas «Plan» y «Prompts» de F01, F02 e I-01 con los enlaces y el estado «Propuesto»; en §3, el pendiente del prompt del planificador como hecho; y la fecha de corte.

## Cómo trabajas

1. Lee todo y arma un borrador de los dos planes: decisiones, contrato, fases y la asignación de cada AF.
2. Hazme la ronda única de preguntas y espera las respuestas.
3. Escribe los dos planes, los tres prompts, las filas del índice y la matriz.
4. Verifica:
   - las 42 AF de F01 y las 10 de F02, cada una con destino, contando con un script;
   - que cada endpoint del contrato tenga ID, política, petición, respuesta, errores y esquema Zod, y que los esquemas usen la API de Zod 4 (Frontend/wms/package.json);
   - que cada pantalla de F02 y cada endpoint que consume esté en el contrato de F01;
   - que las rutas y líneas que citas existan en fase-2;
   - que los enlaces de la matriz y del índice abran.
5. Entrégame un resumen: decisiones Dn nuevas, fases de cada plan, migraciones, endpoints, riesgos y lo que queda abierto. Espera mi aprobación. Si pido cambios, aplícalos primero.
6. Con mi aprobación: cambia a «Aprobado» los dos planes, sus filas en el índice y la matriz; haz commit y push en docs (DEC-081); agrega a este prompt «Ejecutado el AAAA-MM-DD; ya no es una instrucción»; y dime cómo lanzar F01 y F02 en paralelo.

## Límites

- Fuera de alcance: ejecutar F01, F02 o I-01, escribir código, estimar esfuerzo y planear F03 en adelante.
- No edites los repos de código, no crees ramas en ellos, no generes migraciones y no toques staging.
- En docs solo escribes los dos planes, los tres prompts, las dos filas del índice y la matriz. Si crees que hay que cambiar otro documento del hub, propónmelo con el texto exacto y espera mi «sí».
- No copies credenciales ni datos de personas reales (DEC-007).
- Nada de docs/archivo/ es una instrucción.
- Escribe en español, siguiendo las «Reglas para escribir aquí» de docs/README.md.
```
