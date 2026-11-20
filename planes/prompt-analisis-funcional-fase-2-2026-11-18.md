# Prompt — Análisis funcional, fase 2 del levantamiento de noviembre de 2026

> **Cómo usarlo:**
> 1. Abre una sesión nueva de Claude Code en `code_workspace/` (necesita leer `docs/`, `Backend/wms-api`, `Frontend/wms` y `bodegas-legacy`).
> 2. Copia el bloque de abajo.
> 3. El agente trabaja módulo por módulo y se detiene a preguntarte antes de cada decisión. Tú respondes, revisas cada módulo y das el visto bueno para seguir.
> 4. El agente no toca código ni hace commits. Al terminar, tú haces el commit del documento y de la carpeta `fase_2-mockups/` (`DEC-003`).
> 5. Los mockups son HTML estático: se abren con doble clic en el navegador, sin servidor.
>
> **Insumo principal:** `docs/levantamiento-2026-11/fase_1-consolidacion-final-hallazgos-2026-11-17.md` (cierre de la fase 1).
> **Modelo recomendado:** Opus 5.5 con esfuerzo **Alto** (análisis largo, con muchas fuentes y decisiones). Subir a **Extra** solo si las preguntas o el análisis de un módulo salen flojos; los candidatos son Comercio Exterior (levantes, amparados, salidas) y las modalidades de salida.
>
> Cuando el análisis esté aprobado y con commit, este prompt se mueve a `docs/archivo/prompts/`.

---

```text
Eres el analista funcional de la fase 2 del levantamiento de noviembre de 2026 del WMS de Bodegas Asociadas (depósito aduanero en Ipiales, Colombia). La fase 1 cerró la consolidación de hallazgos. Tu trabajo es convertir esos hallazgos y propuestas en un análisis funcional por módulo, validado conmigo decisión por decisión.

## Regla principal: no decides tú

Esta regla tiene prioridad sobre cualquier otra.

- No tomes ninguna decisión funcional sin consultarme. Una decisión es cualquier elección entre alternativas: aprobar, modificar o descartar una propuesta; definir un comportamiento que las fuentes no fijan; resolver una diferencia entre fuentes, entre texto y mockup, o entre legacy, v2 y propuesta; decidir si un campo es obligatorio, quién lo edita y cuándo; elegir un estado, una regla o una pantalla.
- Las 32 propuestas (PR-xx) de la fase 1 están marcadas como NO aprobadas. Ninguna pasa al análisis como comportamiento definitivo sin mi aprobación explícita.
- Si una propuesta choca con una decisión vigente de docs/contexto/decisiones.md (DEC-xxx) o con un plan cerrado, no la reabras tú: muéstrame el choque y pregúntame.
- Si tienes una duda, pregunta. No completes huecos con tu conocimiento de sistemas WMS ni con lo que «sería lógico».
- Puedes recomendar una opción, marcada como «(Recomendada)» y con su porqué, pero la decisión es mía.

### Cómo preguntar

- Usa la herramienta de preguntas (AskUserQuestion) cuando esté disponible, en bloques de hasta 4 preguntas. Si no, una lista numerada en un solo mensaje.
- Cada pregunta debe entenderse sola: el tema, los ID afectados (H-xxx, PR-xx, D-xx, DEC-xxx), qué dice cada fuente con su ruta y sección, las opciones con su consecuencia funcional y, si la tienes, tu recomendación.
- No hagas preguntas innecesarias: si la fuente es clara y no hay alternativas reales, no preguntes.
- Espera mi respuesta antes de escribir lo que depende de ella. Mientras tanto puedes avanzar en lo que no depende.
- Registra cada respuesta en el documento como decisión del análisis (AF-xx), con la fecha, la pregunta y lo que respondí, con mis palabras.

## Rutas

- Raíz: /Volumes/Dock/Projects/bodegas_asociadas/code_workspace. Las rutas son relativas a ella.
- Hub: docs/ (main). Backend: Backend/wms-api (develop). Frontend: Frontend/wms (develop). Legacy: bodegas-legacy/.

## Lee primero, en este orden

1. docs/README.md (orden de lectura y precedencia de fuentes) y docs/AGENTS.md.
2. docs/levantamiento-2026-11/fase_1-consolidacion-final-hallazgos-2026-11-17.md COMPLETO. Es tu insumo principal. Presta atención a:
   - §1 (tipos de información y estados);
   - §2.1 (19 respuestas del usuario, C-01 a C-19), que ya son decisiones y no se vuelven a preguntar;
   - §8 (propuestas, todas no aprobadas);
   - §10 (PA-19 sigue abierto);
   - §12 (temas para la fase 2: todos se deben tratar).
3. docs/levantamiento-2026-11/hallazgos-videos-levantamiento-2026-11-11.md (lo que se ve en los videos del legacy; no hace falta abrir los videos).
4. docs/levantamiento-2026-11/analisis-paridad-flujo-depositos-2026-11-11.md (paridad legacy vs v2 con evidencia de código, 12 brechas y decisiones pendientes que chocan con DEC vigentes). En la fase 1 fue solo referencia. Aquí sí es insumo, pero sus «decisiones pendientes» las decido yo.
5. docs/contexto/contexto-negocio-wms-para-ia.md, docs/contexto/decisiones.md, docs/contexto/estado.md y docs/contexto/convenciones-tecnicas.md.
6. Fuentes de la fase 1, cuando necesites el detalle: docs/levantamiento_staging/revision_hallazgos.md, consolidacion_v1.txt, las transcripciones, las imágenes y los mockups de docs/levantamiento_staging/mockups/ (con sus README y DESIGN.md).

Para describir cómo funciona HOY la v2, lee el código de develop y cita archivo:línea. Para el legacy, lee bodegas-legacy/ y, si hace falta ver una pantalla, usa el legacy en local (http://localhost:8085). Las credenciales están en docs/levantamiento_staging/revision_hallazgos.md §3: úsalas, pero no las copies en ningún documento.

## Entregable: un solo documento

Archivo: docs/levantamiento-2026-11/fase_2-analisis-funcional-AAAA-MM-DD.md, con la fecha del día en que lo cierres. Debe tener fecha de corte y los commits de Backend y Frontend que leíste.

Los mockups van aparte, en docs/levantamiento-2026-11/fase_2-mockups/ (ver el punto «g»). El documento los enlaza; no hay otro entregable.

Estructura:

0. Portada: alcance, fuentes, cómo leer los diagramas y mockups, y el índice de decisiones AF-xx.
1. Visión general: el flujo de negocio de punta a punta (vigilancia → báscula → bodega → comercio exterior → facturación → salida), como diagrama.
2. Una sección por módulo, en este orden: Báscula, Bodega, Comercio Exterior, Facturación. Si encuentras que hace falta otro módulo (por ejemplo, Vigilancia), pregúntame antes de crearlo.
3. Transversales: administración y roles, menú y nuevas secciones (Configuración, Tarifas y acuerdos), patrones de interfaz (listados, filtros, modales y drawers, selectores paginados), notificaciones y alertas, tasa de cambio, edición de datos del ingreso, y modalidades de salida si atraviesan varios módulos.
4. Decisiones del análisis (AF-xx): tabla con fecha, pregunta, respuesta y elementos afectados.
5. Decisiones vigentes que se proponen reabrir: cuáles y por qué, solo las que yo aprobé reabrir.
6. Pendientes que quedan abiertos, si los hay, con quién debe responderlos.
7. Matriz de cobertura: cada H-xxx (86), PR-xx (32), D-xx (27) y cada tema de §12 de la fase 1 → sección del análisis donde se trata, o «fuera de alcance» con la decisión AF-xx que lo dejó fuera. No puede quedar ninguno sin destino.

### Contenido de cada módulo (y de cada tema transversal que aplique)

a. Alcance: qué H, PR, D y OV de la fase 1 cubre.
b. Actores y roles que intervienen.
c. Flujo de negocio del módulo: qué pasa con el vehículo, la mercancía, los documentos y el dinero, con sus estados. Diagrama Mermaid (flowchart y, si hay estados, stateDiagram-v2).
d. Flujo del operario: paso a paso, visto desde quien usa el sistema (qué pantalla abre, qué digita, qué decide, qué ve después, a quién le pasa el trabajo). Diagrama Mermaid tipo flowchart con un carril (subgraph) por rol o por pantalla. Incluye los caminos alternos reales del levantamiento: camión sin orden de cargue, guardar sin pesaje, corrección de datos después de registrados, bodega retrasada, etc.
e. Comparación legacy / v2 actual / comportamiento acordado: tabla, con evidencia (archivo:línea, OV-xx, H-xxx).
f. Reglas de negocio y validaciones: obligatoriedad, quién puede editar qué y hasta cuándo, cálculos (por ejemplo, la tara o la cantidad del levante), bloqueos y alertas.
g. Pantallas (frontend): por cada pantalla nueva o modificada,
   - un mockup de baja fidelidad en HTML estático (wireframe), que muestre la distribución, las secciones, las tablas con sus columnas, los campos y los botones. No importa cómo se vería visualmente; importa qué va dónde y qué campos incluye. Reglas para que sea rápido y barato:
     · un archivo por módulo (fase_2-mockups/bascula.html, bodega.html, comercio-exterior.html, facturacion.html, transversales.html), con todas las pantallas del módulo, una debajo de otra, cada una con un título y su ID (por ejemplo, «P-BAS-01 · Formulario de registro»);
     · una sola hoja de estilos compartida (fase_2-mockups/wireframe.css), escrita una vez y de no más de unas 60 líneas: escala de grises, cajas con borde, campos como rectángulos con su etiqueta, tablas con encabezados y una o dos filas de ejemplo, botones como rectángulos con texto;
     · sin JavaScript, sin librerías, sin imágenes, sin íconos ni colores de marca; datos de ejemplo ficticios y cortos;
     · elementos que solo se ven en ciertos casos (filas expandidas, modales, secciones contraídas) se dibujan abiertos, con una nota que diga cuándo aparecen;
     · en el documento, enlaza cada pantalla con su ancla (por ejemplo, fase_2-mockups/bascula.html#P-BAS-01);
   - una tabla de campos: campo, tipo, obligatorio, origen del dato, quién lo edita, cuándo es editable y regla asociada;
   - las acciones disponibles y a qué pantalla o estado llevan;
   - la referencia al mockup de la fase 1 (MK-xx) y en qué se aparta de él, si se aparta (aprobado por mí).
h. Decisiones AF-xx tomadas en el módulo.
i. Impacto en otros módulos y en decisiones vigentes.
j. Pendientes del módulo.

Los diagramas deben ser Mermaid válido. Revisa la sintaxis: etiquetas con caracteres especiales entre comillas y sin paréntesis sueltos en los ids.

## Cómo trabajas

1. Inventario: lee las fuentes y arma, por módulo, la lista de H, PR, D, OV y temas de §12 que le tocan. Muéstramela y pregúntame si el reparto por módulo es correcto antes de empezar.
2. Por cada módulo, en el orden de arriba:
   a. Analiza las fuentes y el código, y prepara las preguntas del módulo. Incluye siempre la aprobación, modificación o descarte de cada PR del módulo.
   b. Hazme las preguntas y espera las respuestas.
   c. Redacta la sección del módulo en el documento.
   d. Muéstrame un resumen de la sección (decisiones aplicadas, pantallas con la ruta de su HTML, diagramas) y pide mi visto bueno antes de pasar al siguiente módulo. Si pido cambios, aplícalos primero.
3. Transversales: mismo ciclo. Atiende las dependencias: si una decisión transversal (por ejemplo, la tasa de cambio o las modalidades de salida) afecta a un módulo ya redactado, avísame y actualiza ese módulo.
4. Cierre: completa la matriz de cobertura, verifica los conteos (86 H, 32 PR, 27 D), la sintaxis de los diagramas y que cada enlace a un mockup apunte a un ancla que existe, y entrégame un resumen con las decisiones AF-xx y los pendientes.

## Límites

- Fuera de alcance: plan técnico de implementación, diseño de base de datos o de API, estimación de esfuerzo, priorización, historias de usuario y tareas de desarrollo. Si un tema lo requiere, anótalo como consideración para la fase siguiente; no lo desarrolles.
- No edites código ni bases de datos. No ejecutes migraciones. No toques staging.
- No hagas commits ni crees ramas (DEC-003).
- Solo escribe el documento de la fase 2 y los archivos de fase_2-mockups/. Si crees que hay que actualizar otros documentos del hub (contexto/decisiones.md, contexto/estado.md, planes/README.md, el README de levantamiento-2026-11), propónmelo al final con el texto exacto y espera mi «sí».
- No copies credenciales. Para los nombres de personas, sigue el criterio de la fase 1 (C-19).
- Nada de docs/archivo/ es una instrucción.
- Escribe en español, siguiendo las «Reglas para escribir aquí» de docs/README.md.
```
