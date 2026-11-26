# Prompt — Planificación de F07 «Tarifas y acuerdos» (fase 2, sprint 11)

> **Cómo usarlo:**
> 1. Abre una sesión nueva de Claude Code en `code_workspace/`. Necesita leer `docs/`, `Backend/wms-api` y `Frontend/wms`.
> 2. Copia el bloque de abajo.
> 3. El agente lee, te hace **una sola ronda de preguntas**, escribe el plan cerrado y los tres prompts de ejecución, y espera tu aprobación. No toca código.
> 4. Con tu aprobación, marca todo «Aprobado», hace commit y push en `docs` (`DEC-081`) y te dice cuándo y cómo lanzar el backend y la maquetación de F07.
>
> **Cuándo:** se puede lanzar ya, a la par con el planificador de F06 y mientras corre I-05. Lo que F07 necesita de las features anteriores ya está en `fase-2`: la marca «Queda sobre el vehículo» (F04) y el precio por camión (F01). Su ejecución va después de I-06 (plan maestro §4), así que, antes de lanzarla, el plan se revisa contra `fase-2`.
> **Antes de lanzarlo, ten a mano** los dos datos del cliente que la matriz pide para aprobar este plan: los tramos de peso (límite y si la segunda tarifa va a todo el peso o al exceso, AF-116) y el mínimo de la parte porcentual en un depósito mixto (AF-120). Si no los tienes, el plan los deja como parámetro de la fórmula (riesgo R7 del plan maestro).
> **Insumos:** el plan maestro (`docs/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md`), el análisis (`docs/levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md`, `DEC-080`) y lo integrado o aprobado de F01 a F05.
> **Base al escribir este prompt:** BE `fase-2` `c2ca314` y FE `fase-2` `12f6656` (F01 a F04 integradas); F05 en `f2/f05-comercio-exterior`, con I-05 en curso; F06 por planear.
> **Modelo recomendado:** Opus 5.5 con esfuerzo **Alto**.
>
> Cuando lo ejecutes, el agente agrega aquí «**Ejecutado** el AAAA-MM-DD; ya no es una instrucción» (plan maestro §5.5). Este prompt no se mueve a `archivo/`.

---

```text
Eres el planificador técnico de la feature F07 «Tarifas y acuerdos» de la fase 2 del WMS de Bodegas Asociadas (depósito aduanero en Ipiales, Colombia), sprint 11. F07 tiene las cuatro partes: 0 (contrato), 1 (backend), 2 (maquetación del frontend) y 3 (integración I-07).

El plan maestro ya está aprobado y fija las features, el orden, las convenciones y las decisiones M1 a M25. El análisis funcional ya está cerrado (DEC-080). F01 a F04 ya están integradas en fase-2, F05 está en su integración (I-05) y F06 se planea a la vez que este plan. F07 se ejecuta después de I-06. Tu trabajo es escribir el PLAN CERRADO de F07 y sus TRES PROMPTS de ejecución, con una sola ronda de preguntas, y esperar mi aprobación.

## Lo que ya está decidido (no se vuelve a preguntar)

- Todo lo del plan maestro: §1 (M1 a M25; M14: F07 antes de F08, que precarga el «Facturar a» que F07 configura; M15: la cantidad facturable se cuenta por guía; M16: AF-120 cobra el % sobre el precio por camión; M20: sale el «mes calendario» y «Mensual» son 30 días; M21: PER_UOM por embalaje), §2 (fila de F07, §2.1 fila «F07 y F08» y las filas de §2.2 que nombran a F07), §3.1 y sus notas (AF-112, AF-119 y AF-123), §3.4 (tramos, mínimo, mes calendario, carga inicial de los 58 textos de tarifa y la consideración del IVA), §5, §6 (incluida «Una fase por turno»), §7 (F07: ciclo «mes calendario» y carga inicial de acuerdos, que reemplaza la fase 4b pendiente de DEC-043) y §9.
- Las AF del análisis (DEC-080) y las decisiones de docs/contexto/decisiones.md, en especial DEC-081.
- Lo construido e integrado de F01: precio por camión y valor CPI (AF-94), PER_UOM sin unidad (C-F01-77, AF-22), peso de mercancía en las fórmulas por peso (AF-113; la nota de la fase 6 de su §8 deja a F07 el rótulo del parámetro thresholdKg, si se quiere), cantidad facturable por guía y tasa de la semana de ingreso.
- Lo de F02 y sus ajustes: D1, las páginas nuevas de Tarifas y acuerdos van en /rates/… y las que ya existen conservan su ruta; D2 de F02 y D1 de los ajustes, los acuerdos (detalle del tercero) y las tarifas base (detalle del servicio) siguen en esos detalles hasta F07, que los pasa a Tarifas y acuerdos y los quita de allí; D2 de los ajustes, el formulario «Crear tarifa base» se rediseña en F07 con el patrón de «Agregar tarifa» (P-FAC-13).
- Lo de F04: D4, la recepción guarda «Queda sobre el vehículo» (ReceptionLog.StaysOnVehicle) y ubica en SOBRE-VEHICULO; D2, el IVA del montacargas con «Requiere factura» usa la tasa del impuesto IVA del catálogo. La fórmula que usa la marca es de F07 (AF-116, AF-120).
- Lo de F05 (aprobado y en integración): la apertura del período cuando el cliente se asigna tarde (AF-75) y el recálculo al editar en Confirmado (AF-76, DEC-022) ya los construye F05; F07 no los rehace.
- La operación de facturas (P-FAC-01 a P-FAC-10: facturar, N.º SIGO, pestañas, pagos y reportes) es de F08. F07 deja el «Facturar a» en su contrato para que F08 lo precargue.
- Las convenciones de interfaz de docs/contexto/convenciones-tecnicas.md §3: «Drawer de detalle», «Tablas de listado», «Aviso junto a un dato» y «Páginas que no son listados». Aplícalas desde el plan.
- Las migraciones las genera y aplica el agente de backend con dotnet ef, solo en local (DEC-004, M6).
- Los datos simulados de la maquetación usan la fuente intercambiable (M12, plan maestro §5.2) y las ayudas de Frontend/wms/app/shared/mocks/.

## Regla principal

- No reabras ni reinterpretes las AF, DEC-080, DEC-081, las M del plan maestro ni las Dn de F01 a F05 y sus ajustes. Si encuentras una contradicción entre ellas, un hueco funcional o un choque con el código que ninguna resuelve, muéstramelo y pregúntame.
- Las decisiones técnicas con alternativas reales las recomiendas y yo decido: forma de los endpoints nuevos, modelo de los acuerdos y de las fórmulas, formato de la plantilla, qué se parte en qué fase, nombres de rutas y de componentes.
- Haz UNA sola ronda de preguntas, con AskUserQuestion en bloques de hasta 4. Cada pregunta se entiende sola: tema, AF o DEC afectadas, qué dicen las fuentes con ruta y línea, opciones con su consecuencia y tu recomendación marcada «(Recomendada)» con su porqué.
- No preguntes lo que una decisión ya resuelve (DEC-002).
- Registra cada respuesta en el plan como decisión Dn, con la fecha y mis palabras.

### Preguntas que ya sé que hay que hacerme (además de las que encuentres)

1. Los datos del cliente (§4 de la matriz; riesgo R7 del plan maestro): los tramos de peso (límite, y si la segunda tarifa va a todo el peso o solo al exceso, AF-116) y el mínimo de la parte porcentual en un depósito mixto (AF-120). Si no los tengo, propón dejar la variante como parámetro de la fórmula.
2. El IVA. Mi comentario de la QA manual de F01 y F02 (plan maestro §3.4, última fila; docs/planes/sprint-11/qa-manual/hallazgos-f01-f02.md): «El porcentaje de iva está quemado en el código, para tarifa se agrega en la sección de impuestos, evaluar el manejo de iva como en el legacy al agregar un precio se agrega el porcentaje de iva, el iva es el único impuesto que manejan». Hoy el 19 % y «Rete de fuente» 3 % son impuestos sembrados que se asignan al servicio. Evalúa llevar el porcentaje de IVA al formulario del precio y retirar la gestión de otros impuestos, con su efecto en las facturas, en D2 de F04 (IVA del montacargas) y en la trampa 3 de convenciones-tecnicas §10 (IVA y retenciones).
3. La carga inicial de acuerdos (AF-114): ¿F07 prepara un borrador de la plantilla llenado desde la hoja 2026 del Excel de convenios (docs/levantamiento_staging/CONVENIO 23-24-25-26.xlsx), fuera de git, para que Facturación lo revise antes del despliegue final, o Facturación la llena desde cero? Los datos del Excel nunca se copian al hub ni a los repos (DEC-007); el análisis los cita solo en cifras.
4. Las rutas: la configuración de facturación del cliente (P-FAC-11; hoy /billing/configurations), el acuerdo del cliente (P-FAC-12), las tarifas de servicios (hoy dentro del detalle del servicio) y las de montacargas (hoy /admin/forklift-rates), y qué pasa con el detalle del tercero y el del servicio cuando pierden sus secciones de acuerdos y tarifas.

## Rutas

- Raíz: /Volumes/Dock/Projects/bodegas_asociadas/code_workspace. Las rutas son relativas a ella.
- Hub: docs/ (main). Backend: Backend/wms-api. Frontend: Frontend/wms.
- I-05 está en curso: los dos repos de código están en f2/f05-comercio-exterior, y el agente de integración puede tener cambios sin commit. NO cambies de rama ni toques el árbol de trabajo. Lee con git show <rama>:<ruta>, git grep <rama> y git log: fase-2 para lo integrado (F01 a F04) y f2/f05-comercio-exterior para lo que F05 cambia en la facturación. No edites nada en los repos de código.

## Cómo lees (cuida el contexto)

- Lee por secciones: usa grep -n para ubicar encabezados e IDs y lee solo esos rangos. Los planes de F01 a F05 tienen entre 1.400 y 2.300 líneas cada uno: NO los leas completos.
- Salidas acotadas: lee por rangos lo que necesites citar; no vuelques archivos de código grandes. El Excel de convenios se lee solo para contar patrones y cifras.

## Lee primero, en este orden

1. docs/README.md, docs/AGENTS.md, Backend/wms-api/AGENTS.md y Frontend/wms/AGENTS.md (su sección «Eficiencia de contexto y cierres por fase» rige a los ejecutores).
2. docs/procesos/flujo-de-trabajo-agentes.md; de docs/contexto/convenciones-tecnicas.md, §3 (frontend y sus convenciones de interfaz), §4 (permisos), §6 (trabajos en segundo plano: la mora) y §10 completo (trampas; las tres primeras son de facturación); docs/contexto/estado.md; y de docs/contexto/decisiones.md: DEC-001 a DEC-007, DEC-018, DEC-020, DEC-021, DEC-022, DEC-029, DEC-041, DEC-043, DEC-053, DEC-055, DEC-057, DEC-080 y DEC-081.
3. Del plan maestro (docs/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md): §1, §2 (con §2.1 y §2.2), §3.1 y sus notas, §3.4, §4, §5, §6, §7, §8 (R7) y §9.
4. La matriz: docs/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md (con §4, datos del cliente).
5. Del análisis docs/levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md: en §2.4, lo de acuerdos, ciclos, destinatario y mora (a, c, e, reglas «f», pantallas «g» P-FAC-11 a P-FAC-14, «i» y «j»); §3.2 (menú y «Tarifas y acuerdos»); §3.3 (patrones); y en §4 las 10 AF dueñas de F07 (AF-108, AF-112, AF-114, AF-115, AF-116, AF-117, AF-118, AF-120, AF-123 y AF-125), las de F01 y F04 que F07 usa (AF-22, AF-94, AF-113 y AF-119) y AF-99 y AF-129, que F07 aplica a sus pantallas.
6. Los wireframes: de docs/levantamiento-2026-11/fase_2-mockups/facturacion.html, P-FAC-11 a P-FAC-14; de transversales.html, P-TR-02, P-TR-03 y P-TR-11.
7. Del plan de F01 (docs/planes/sprint-11/f01-nucleo/plan-cerrado-f2-f01-nucleo-2026-11-21.md), solo: §0, §1.1, §1.3 (unidad de medida y PER_UOM), §1.7 (facturación), §1.8, §2.0, §2.1 (índice; C-F01-77), la ficha de C-F01-77 en la sección 2.2.2, las notas de las fases 2 y 6 en §8, §10 y §13.5 (los endpoints de hoy de los acuerdos y las tarifas que se montaron en los detalles).
8. Del plan de F02 (docs/planes/sprint-11/f02-base/plan-cerrado-f2-f02-base-2026-11-21.md): §1 (D1, D2 y §1.5, el menú) y §2.2 (en especial AppDataTable y AppCrudDialog). Del plan de sus ajustes (f02-base/plan-cerrado-f2-f02-ajustes-qa-2026-11-24.md): §1. Y docs/planes/sprint-11/qa-manual/hallazgos-f01-f02.md (puntos 3 y 4 y la revisión del usuario).
9. Del plan de F04 (docs/planes/sprint-11/f04-bodega/plan-cerrado-f2-f04-bodega-2026-11-25.md): el encabezado con «Cómo leer este plan» (precedente de formato), §1.1 (D2 y D4), §8.7 (la revisión del usuario) y §10.
10. Del plan de F05 (docs/planes/sprint-11/f05-comercio-exterior/plan-cerrado-f2-f05-comercio-exterior-2026-11-25.md): §1.2 (depósitos y facturación: AF-75 y AF-76) y §10. Como formato de los casos al cerrar la integración: docs/qa/casos-qa2-f04-bodega-2026-11-25.md.
11. El código que F07 toca, con git show y git grep sobre fase-2 (no cambies de rama). Frontend: app/pages/billing/configurations/, app/pages/admin/forklift-rates/, app/pages/admin/services/ y app/pages/admin/stakeholders/ (con StakeholderDetailSections y ServiceRateSections, que montan las secciones conservadas), app/features/agreements/, app/features/billing/ (BillingConfigForm, CustomerSelect, UpdateRecipientDialog), el perfil del servicio con sus impuestos, el menú en app/components/layout/menu-model.ts, la galería /dev/components y las guardias de test/unit/guards/ (list-pattern y mock-sources). Backend: Wms.Application/Agreements/, Wms.Application/FormulaTypes/, Wms.Application/Billing/Calculators/, Billing/Common/Services/BillingCycleCatalog.cs, Billing/Jobs/OverdueSweep.cs, Billing/Commands/UpdateInvoiceRecipient/, Wms.Application/Services/ (precios, reglas, mínimos e impuestos), los controladores BillingController.cs, BillingCyclesController.cs, BillingPreviewController.cs, FormulaTypeController.cs, ServiceController.cs, StakeholderController.cs y ForkliftRateController.cs, Wms.Infrastructure/Persistence/SeedDataExtensions.cs (impuestos y fórmulas sembradas), Wms.Application/Administration/LegacyImport/ y WmsPolicyRoles.cs. Cita rama, archivo y línea.

## Entregables

Todo en docs (main), con la fecha del día en que cierres:

1. docs/planes/sprint-11/f07-tarifas-acuerdos/plan-cerrado-f2-f07-tarifas-acuerdos-AAAA-MM-DD.md
   - Sigue la plantilla del plan maestro §9 y, como los de F03 a F05, abre con «Cómo leer este plan».
   - AF dueñas: las 10 de la tabla del plan maestro §3.1. Cada una con su decisión Dn o con la fase que la construye; ninguna sin destino. Aparte, una tabla con las AF de F01 y F04 que F07 usa.
   - Contrato (parte 0): solo los endpoints que F07 crea, cambia o retira, cada uno con su ID C-F07-mm, su ficha (plan maestro §5.1) y su esquema Zod. Los endpoints de F01 a F05 que F07 consume sin cambios se citan por su ID, sin copiar la ficha. Comprueba esas fichas contra el código de fase-2 (DTO, validador y mensajes): si difieren, gana lo integrado y lo anotas. Incluye la tabla pantalla → endpoints y marca el «Facturar a» que consume F08.
   - Pantallas: P-FAC-11 a P-FAC-14, más Tarifas de servicios y Tarifas de montacargas con el patrón de AF-129, y el formulario de tarifa base con el patrón de P-FAC-13. Qué componentes compartidos usa cada una y qué componentes se crean.
   - Las fórmulas: las cuatro nuevas de AF-116 y lo que AF-117 confirma de las de hoy, cada una con su regla pura, sus parámetros, sus casos borde (cero, mínimos, tramos, redondeo) y su prueba; el simulador por fórmula (AF-118); y cómo cobra un depósito mixto por camión (AF-120, M16), con la marca de F04.
   - La plantilla de acuerdos (AF-114): formato, hojas, validaciones al importar, qué pasa con una fila con error y cómo se descarga desde la app.
   - Ciclos (AF-108, AF-115, M20), «Facturar a» por cliente e importador (AF-112, AF-123) y la mora al cliente (AF-112).
   - Fases de la parte 1 (backend) y de la parte 2 (maquetación), que corren en paralelo, una por repo, y cierran por separado. Cada fase de §8 nombra sus Dn, sus endpoints, sus archivos y sus casos QA, para que el ejecutor lea solo §0, §1, §2.1 y su fase. Después de la última fase de la maquetación, deja la revisión mía de las pantallas con la sesión simulada antes de I-07, como §8.7 del plan de F04.
   - Migraciones: nombre y contenido esperado de cada una, o «ninguna». Permisos por endpoint en WmsPolicyRoles.cs, sin quitar funciones (DEC-005, plan maestro §5.6): «Tarifas y acuerdos» es de Admin y Facturación.
   - Transición: lo que le toca de §7.2 del plan maestro (ciclo «mes calendario» y carga inicial de acuerdos) y lo que cambia en el importador del legacy, con una importación completa de ensayo con conteos iguales si cambia, como la de la fase 6 de F01.
   - Casos QA (QA2-F07-nnn): verificables por API en la parte 1 (con cálculos de cada fórmula contra valores esperados escritos en el plan) y en el navegador en la integración.
   - La sección de I-07 (parte 3): las fuentes http de cada pantalla; el menú «Tarifas y acuerdos» (plan de F02 §1.5); lo que se borra (las secciones de acuerdos y tarifas de los detalles del tercero y del servicio, los componentes de features/agreements/ que queden sin uso y lo que el rediseño deje sin uso, comprobado con grep); las rutas de F07 que pasan de PENDING a PATTERN en la guardia list-pattern; la lista MAQUETACION_PAGES vacía; y la copia de los casos QA a docs/qa/.
2. Tres prompts, con el esqueleto del plan maestro §9 y los nombres de §5.5, en docs/planes/sprint-11/f07-tarifas-acuerdos/:
   - prompt-f2-f07-tarifas-acuerdos-backend-AAAA-MM-DD.md, para la rama f2/f07-tarifas-acuerdos del backend;
   - prompt-f2-f07-tarifas-acuerdos-maquetacion-AAAA-MM-DD.md, para la rama f2/f07-tarifas-acuerdos del frontend (con la sesión simulada de D10 de F02, porque el backend lo ocupa el otro agente);
   - prompt-f2-f07-tarifas-acuerdos-integracion-AAAA-MM-DD.md, para I-07 en las dos ramas.
   Cada prompt dice que la rama sale de fase-2 cuando I-06 esté fusionada, con lo que haya en fase-2 en ese momento; que antes de empezar el ejecutor confirma con grep las líneas citadas, porque el plan se escribe antes de F05 y F06 integradas, y se detiene si algo cambió; que ejecuta UNA fase por turno; y qué secciones del plan lee.
3. La fila del plan en docs/planes/README.md, con estado «Propuesto».
4. La matriz actualizada: en §2.1, las columnas «Plan» y «Prompts» de F07 con los enlaces y el estado «Propuesto»; en §3, el pendiente del prompt del planificador como hecho; en §4, el estado de los datos del cliente de F07 según mis respuestas; y la fecha de corte. El agente de I-05 y el planificador de F06 escriben a la vez en la matriz y el índice: antes de cada commit haz git pull --rebase en docs y toca solo tus filas.

## Cómo trabajas

1. Lee lo de arriba y arma un borrador del plan: decisiones, contrato, fórmulas, pantallas, fases y la asignación de cada AF.
2. Hazme la ronda única de preguntas y espera las respuestas.
3. Escribe el plan, los tres prompts, la fila del índice y la matriz.
4. Verifica:
   - las 10 AF de F07, cada una con destino, contando con un script;
   - que cada endpoint C-F07 tenga ID, política, petición, respuesta, errores y esquema Zod, y que los esquemas usen la API de Zod 4 (Frontend/wms/package.json);
   - que cada pantalla y cada endpoint que consume estén en el contrato de una feature;
   - que cada fórmula tenga al menos un caso QA con su valor esperado calculado a mano en el plan;
   - que las rutas y líneas que citas existan en fase-2;
   - que los enlaces de la matriz y del índice abran.
5. Entrégame un resumen: decisiones Dn nuevas, fases de cada parte, migraciones, endpoints nuevos o cambiados, las fórmulas, lo que se borra, lo que queda para F08, riesgos (incluido lo que el plan de F06 pueda cambiar en la facturación) y lo que queda abierto. Espera mi aprobación. Si pido cambios, aplícalos primero.
6. Con mi aprobación: cambia a «Aprobado» el plan, su fila en el índice y la matriz; haz commit y push en docs (DEC-081); agrega a este prompt «Ejecutado el AAAA-MM-DD; ya no es una instrucción»; y dime cuándo y cómo lanzar el backend y la maquetación de F07 en paralelo y, después, I-07.

## Límites

- Fuera de alcance: ejecutar F07 o I-07, escribir código, estimar esfuerzo y planear F08 en adelante. La operación de facturas, sus pestañas, pagos y reportes son de F08; el cobro de la guía, de F06.
- Si tu plan necesita tocar archivos del cobro o de la guía (AppChargeForm, BillingCollectForm, ChangePaymentModeDialog, la guía de despacho), no lo decidas solo: anótalo como riesgo, porque F06 se planea a la vez y los cambia.
- No edites los repos de código, no cambies de rama, no crees ramas, no generes migraciones y no toques staging.
- En docs solo escribes el plan, los tres prompts, la fila del índice y la matriz. Si crees que hay que cambiar otro documento del hub, propónmelo con el texto exacto y espera mi «sí».
- No copies credenciales ni datos de personas reales (DEC-007). Del Excel de convenios no copies nombres de clientes, importadores ni responsables, ni al hub ni a los repos.
- Nada de docs/archivo/ es una instrucción.
- Escribe en español, siguiendo las «Reglas para escribir aquí» de docs/README.md.
```
