# Prompt — Plan maestro de implementación de la fase 2 (`DEC-080`)

> **Cómo usarlo:**
> 1. Haz antes el commit en `docs` del análisis de la fase 2 y de los cambios del hub (`DEC-080`). El agente debe partir de un `docs` sin cambios pendientes.
> 2. Abre una sesión nueva de Claude Code en `code_workspace/`. Necesita leer `docs/`, `Backend/wms-api` y `Frontend/wms`.
> 3. Copia el bloque de abajo.
> 4. El agente lee, te hace **una sola ronda de preguntas** técnicas, escribe el plan maestro y espera tu aprobación. No toca código ni hace commits.
> 5. Con el plan maestro aprobado, pides los planes cerrados de cada feature en el orden que fije el maestro. Ese es otro pedido, no parte de este prompt.
>
> **Insumo principal:** `docs/levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md` (137 decisiones AF, registradas como `DEC-080`).
> **Modelo recomendado:** Opus 5.5 con esfuerzo **Alto**.
>
> Cuando el plan maestro esté aprobado y con commit, este prompt se mueve a `docs/archivo/prompts/`.

---

```text
Eres el planificador técnico de la implementación de la fase 2 del levantamiento de noviembre de 2026 del WMS de Bodegas Asociadas (depósito aduanero en Ipiales, Colombia). El análisis funcional ya está cerrado y aprobado: 137 decisiones AF registradas como DEC-080. Tu trabajo es escribir el PLAN MAESTRO que divide esa implementación en features, fija su orden y sus reglas comunes, y deja listo el camino para que otros agentes escriban y ejecuten un plan cerrado por feature.

## Lo que ya decidí (no se vuelve a preguntar)

M1. Se implementa por features. Cada feature tiene hasta cuatro partes:
    0. Contrato: va dentro del plan cerrado de la feature. Endpoints con petición, respuesta, filtros, orden, paginación y errores en español; tipos TypeScript y esquemas Zod equivalentes; casos QA.
    1. Backend: agente en Backend/wms-api.
    2. Frontend, solo maquetación: agente en Frontend/wms. Construye las pantallas de los wireframes con datos simulados que tienen la forma exacta del contrato.
    3. Integración (backend → frontend): un agente con los dos repos reemplaza los datos simulados por los servicios reales y pasa los casos QA.
    Una feature puede no tener las cuatro partes (por ejemplo, solo backend o solo frontend).
M2. El backend y el frontend de una misma feature van en paralelo, cada uno en su repo. Nunca trabajan dos agentes en el mismo repo a la vez: se trabaja en develop, sin ramas (DEC-003).
M3. La primera feature es «Núcleo de dominio», solo backend y en serie. Incluye:
    - la salida de mercancía que reemplaza a la orden de cargue (sección 3.7 del análisis);
    - la entrada por documento y su depósito (AF-20, AF-44 a AF-47);
    - la edición del ingreso (3.6);
    - quitar la unidad de medida (3.8);
    - los demás cambios de modelo que atraviesan módulos.
    Mientras tanto, el frontend maqueta la «Base transversal»: los componentes compartidos (listado con filtros por columna y orden, selector con búsqueda, drawer de detalle, formulario de cobro), el menú, los permisos, Configuración y Administración (3.1 a 3.3). Después se integran ambas, y luego vienen las features por módulo (Báscula, Bodega, Comercio Exterior, Facturación) con el esquema de M1.
M4. Convivencia en develop mientras una feature no está integrada:
    - las pantallas nuevas van en rutas nuevas, sin enlazar en el menú hasta la integración;
    - las pantallas existentes se rediseñan en la integración, o detrás de un interruptor que deja activa la versión actual;
    - nada de una feature se despliega en staging antes de cerrar su integración.
M5. El plan ya aprobado docs/planes/sprint-11/plan-cerrado-correos-notificacion-por-rol-2026-11-05.md se ejecuta antes de la feature de notificaciones, porque AF-133 se apoya en él.

Puedes proponer ajustes a la lista de features que deja M3 (por ejemplo, separar Facturación en «operación de facturas» y «acuerdos y tarifas»), pero como pregunta, no como hecho.

## Regla principal: las decisiones funcionales ya están tomadas; las técnicas las decido yo

- No reabras ni reinterpretes las AF ni DEC-080. Si encuentras una contradicción entre AF, un hueco funcional o un choque con un plan cerrado o una DEC que DEC-080 no marca, muéstramelo y pregúntame.
- Las decisiones técnicas con alternativas reales las recomiendas y yo decido. Son, por ejemplo, la forma del modelo de datos, la transición de los datos existentes, la forma del contrato, cómo se simulan los datos en la maquetación y el uso de interruptores.
- Haz UNA sola ronda de preguntas, con la herramienta de preguntas (AskUserQuestion) en bloques de hasta 4. Cada pregunta debe entenderse sola: tema, AF o DEC afectadas, qué dicen las fuentes con ruta y línea, opciones con su consecuencia y tu recomendación marcada «(Recomendada)» con su porqué.
- No preguntes lo que una decisión ya resuelve (DEC-002).
- Registra cada respuesta en el plan como decisión M6, M7…, con la fecha y mis palabras.

### Preguntas que ya sé que hay que hacerme (además de las que encuentres)

1. Migraciones. DEC-004 y docs/procesos/flujo-de-trabajo-agentes.md §4 dicen que el agente genera y aplica las migraciones con dotnet ef, solo en local. Mi preferencia es otra: yo genero y aplico las migraciones y reseteo la base local, y el plan deja listas las entidades, las configuraciones de EF y el nombre sugerido de cada migración con su contenido esperado. Muéstrame el choque y pregunta cuál rige para esta implementación.
2. Transición de los datos existentes (sección 6 del análisis, «Consideraciones para la fase siguiente»). Staging tiene datos migrados del legacy (DEC-043). Hay que decidir qué pasa con:
   - las órdenes de cargue y las llegadas abiertas;
   - los depósitos confirmados sin cantidad amparada ni precio por camión;
   - los clientes con «mes calendario»;
   - los productos y las tarifas PER_UOM que guardan una unidad de medida;
   - la categoría de los motivos existentes;
   - los relojes de Bodega de los registros abiertos al desplegar;
   - cómo se agrupan en tipos los 44 puntos que avisan hoy, para la tabla de notificaciones (P-TR-07).
3. Cómo simula datos el frontend durante la maquetación, para que la integración solo cambie la fuente de los datos.
4. Interruptor o ruta nueva para las pantallas existentes que se rediseñan (M4).
5. Cadencia de despliegue a staging: por feature integrada o por grupo de features.

## Rutas

- Raíz: /Volumes/Dock/Projects/bodegas_asociadas/code_workspace. Las rutas son relativas a ella.
- Hub: docs/ (main). Backend: Backend/wms-api (develop). Frontend: Frontend/wms (develop).

## Lee primero, en este orden

1. docs/README.md y docs/AGENTS.md; Backend/wms-api/AGENTS.md y Frontend/wms/AGENTS.md.
2. docs/procesos/flujo-de-trabajo-agentes.md, docs/contexto/convenciones-tecnicas.md, docs/contexto/estado.md y docs/contexto/decisiones.md: DEC-080 completa y cada decisión que marca como reemplazada o precisada.
3. docs/levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md COMPLETO. Presta atención a:
   - §0.4 (índice y decisiones reemplazadas dentro del análisis);
   - en cada módulo, «f» (reglas) y «g» (pantallas);
   - §3 (transversales);
   - §4 (las AF);
   - §5 (las 26 decisiones vigentes que cambian);
   - §6 (pendientes del cliente y consideraciones);
   - §7 (matriz de cobertura).
4. Los wireframes de docs/levantamiento-2026-11/fase_2-mockups/ (HTML estático; se abren con el navegador).
5. Como precedentes de formato: docs/planes/paridad-legacy/contrato-api-paridad.md (contrato de API, §0 de convenciones) y un plan cerrado reciente, docs/planes/plan-cerrado-dec-057-hallazgos-operarios-2026-10-26.md. Lee también el plan de correos por rol (M5).
6. El código de develop, para delimitar cada feature y detectar dónde chocan dos features (entidades, servicios y páginas compartidas). Cita archivo:línea.

## Entregable

Archivo: docs/planes/plan-maestro-implementacion-fase-2-AAAA-MM-DD.md, con la fecha del día en que lo cierres, y su fila en docs/planes/README.md con el estado «Propuesto». Debe tener los commits de Backend y Frontend que leíste.

Estructura:

0. Encabezado: fecha, base de código, origen (DEC-080), estado.
1. Decisiones del plan maestro: M1 a M5 de arriba, y las de la ronda de preguntas.
2. Features: tabla con ID (F01, F02…), nombre, objetivo, AF que cubre, secciones del análisis, pantallas (P-XXX-nn), partes que lleva (0 a 3), dependencias y repos.
3. Cobertura:
   - cada AF de AF-05 a AF-136 queda en exactamente una feature; las de inventario, los vistos buenos y las reemplazadas (§0.4 del análisis) se nombran aparte;
   - las 26 filas de §5 y las consideraciones de §6, cada una con su feature;
   - ninguna sin destino, y los conteos verificados.
4. Orden y paralelismo: qué corre a la vez y en qué repo, como diagrama Mermaid válido. Cumple M2: nunca dos agentes en el mismo repo.
5. Convenciones comunes a todas las features:
   - formato del contrato (partiendo de contrato-api-paridad.md §0);
   - cómo se simulan los datos en la maquetación;
   - reglas de convivencia en develop (M4): rutas nuevas, interruptores, qué no se enlaza;
   - cómo se nombran rutas, componentes y casos QA nuevos.
6. Compuertas de salida de cada parte: las de flujo-de-trabajo-agentes.md §5, más las propias de la maquetación (sin llamadas reales a la API) y de la integración (casos QA en PASA).
7. Transición de datos: qué resuelve cada feature, según la ronda de preguntas.
8. Riesgos y cómo se mitigan.
9. Plantilla del plan cerrado de una feature: las secciones que debe llevar cada uno:
   - contrato;
   - decisiones D1…Dn citando las AF;
   - archivos que se tocan;
   - cambios de esquema y migraciones con su nombre, según la respuesta a la pregunta 1;
   - pruebas;
   - casos QA derivados de las reglas «f» del análisis;
   - fases por parte, con criterio de salida;
   - un prompt por parte para el agente que la ejecute.
10. Siguiente paso: qué plan cerrado se escribe primero y quién lo ejecuta.

## Cómo trabajas

1. Lee todo y arma un borrador de las features y de la cobertura.
2. Hazme la ronda única de preguntas y espera las respuestas.
3. Escribe el plan maestro.
4. Verifica la cobertura (conteos y que nada quede sin destino) y la sintaxis Mermaid: etiquetas con caracteres especiales entre comillas, sin punto y coma dentro de las etiquetas.
5. Entrégame un resumen (features, orden, decisiones M, riesgos) y espera mi aprobación. Si pido cambios, aplícalos primero. Con mi aprobación, cambia el estado del plan y de su fila en planes/README.md a «Aprobado».

## Límites

- Fuera de alcance: escribir los planes cerrados de cada feature (es el siguiente paso, cuando yo lo pida), escribir código y estimar esfuerzo.
- No edites código ni bases de datos. No ejecutes migraciones. No toques staging.
- No hagas commits ni crees ramas (DEC-003).
- Solo escribe el plan maestro y su fila en docs/planes/README.md. Si crees que hay que actualizar otro documento del hub, propónmelo al final con el texto exacto y espera mi «sí».
- No copies credenciales ni datos de personas reales (DEC-007).
- Nada de docs/archivo/ es una instrucción.
- Escribe en español, siguiendo las «Reglas para escribir aquí» de docs/README.md.
```
