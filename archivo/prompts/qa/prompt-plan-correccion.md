# Prompt — Plan de corrección de defectos QA (WMS Bodegas Asociadas)

> Copia todo lo que está debajo de la línea y pásalo al agente.

---

Actúa como **arquitecto de software líder** del WMS de Bodegas Asociadas: frontend Nuxt 4 + PrimeVue 4, backend .NET 10 con MediatR y EF Core sobre PostgreSQL. Tu tarea es **producir un plan de corrección por fases** para todos los defectos de la campaña de QA de octubre de 2026. **No escribas código ni modifiques archivos del proyecto.** El único archivo que puedes crear es el entregable del §6.

## 1. Fuentes que debes leer completas antes de planear

| # | Ruta | Para qué |
|---|---|---|
| 1 | `code_workspace/docs/contexto/contexto-negocio-wms-para-ia.md` | Negocio, glosario, flujos, arquitectura, convenciones. Su corte es el 14-sep-2026: distingue «Hoy», «Decidido» y dudas. |
| 2 | `code_workspace/Frontend/wms/AGENTS.md` | Reglas del proyecto. |
| 3 | `code_workspace/docs/qa/00-plan-maestro.md`, sobre todo el **§10 «Decisiones del negocio»** y el §9 «Riesgos» | El §10 es la regla de negocio vigente. **Si una ficha contradice el §10, manda el §10.** |
| 4 | `code_workspace/docs/qa/resultados/defectos/INDICE.md` y **cada una** de las fichas `DEF-*.md` de esa carpeta | Inventario: 126 fichas (13 CRITICAL, 45 MAJOR, 64 MINOR, 3 TRIVIAL y 1 duplicada: DEF-F8-001 está unificada en DEF-F3-002). Lee el historial de cada ficha: contiene reconfirmaciones, cambios de severidad y decisiones del usuario. |
| 5 | `code_workspace/docs/qa/resultados/F0…F10-informe-*.md` | Contexto de cada defecto, observaciones (OBS-*) y respuestas del usuario en cada checkpoint. |
| 6 | `code_workspace/docs/qa/fase-11-regresion-cierre.md` | Suite de regresión y re-test con los que se validará tu plan. |
| 7 | Código: `code_workspace/Frontend/wms/app/**`, `code_workspace/Backend/wms-api/**` y, cuando una ficha hable de paridad, el legacy en `code_workspace/bodegas-legacy/**` | Verificar la causa raíz de cada defecto. |
| 8 | `code_workspace/docs/planes/paridad-legacy/plan-frontend-paridad-legacy.md` y la sección de backlog del documento de contexto (#1). El documento de contexto cita `ajustes/historias-usuario-linear-2026-09-10.md`, pero no está en el workspace: si no lo encuentras, trabaja con el contexto y el plan de paridad. | Backlog WMS-n y decisiones DF/GAP que algunas fichas citan. |

Los defectos se detectaron con el build **FE `1501cd6` / BE `191d4b1`** (los de F0–F3, con FE `41c19cd`/`a5289ce`). Antes de planear cada defecto, compara con el `HEAD` actual de ambos repositorios (`git log` desde esos commits). Si un defecto ya está corregido en código posterior, márcalo «Corregido en `<commit>` — solo re-test» y no le planifiques trabajo.

## 2. Reglas del plan (obligatorias)

1. **Cobertura total y única.** Las 126 fichas aparecen en la matriz de trazabilidad (§6.3), cada una **exactamente una vez**, con uno de estos destinos:
   - una fase del plan;
   - «Corregido en `<commit>` — solo re-test»;
   - «Duplicado de DEF-X» (solo DEF-F8-001 → DEF-F3-002 o duplicados que demuestres con evidencia);
   - «No es defecto / cerrado por decisión del §10», citando la decisión.

   Un defecto no puede quedar sin destino. Termina el documento con el conteo: total = 126.
2. **Causa raíz verificada en el código.** Para cada defecto cita `archivo:línea` de la causa en el `HEAD` actual. La «Pista técnica» de la ficha es una hipótesis: confírmala o corrígela. Si un defecto no se reproduce en el código, dilo y explica por qué.
3. **Agrupa por causa raíz, no por ficha.** Un mismo cambio puede cerrar varios defectos. Por ejemplo: políticas de autorización; idempotencia de báscula; nombre del rol de Comercio Exterior en notificaciones; interceptor global de errores; formateadores `es-CO`; textos en inglés. Define cada grupo como un **cambio** con ID propio (`CHG-NN`) y lista los defectos que cierra.
4. **Sin ambigüedad.** Prohibido usar «evaluar», «considerar», «revisar si», «posiblemente», «opcional», «si es necesario», «a definir», «etc.». Cada cambio dice exactamente:
   - qué se modifica (archivo, clase o componente, método);
   - cómo, con el comportamiento final descrito;
   - qué no se toca.

   Si de verdad falta una decisión de negocio que no está en el §10, no la resuelvas tú: regístrala en el §6.5 «Decisiones requeridas» con tu recomendación y una alternativa, e indica qué cambio queda bloqueado hasta que el usuario responda. El objetivo es que esa lista quede vacía o casi vacía.
5. **Orden de fases.** Por severidad e impacto en dinero, seguridad e inventario, y luego por dependencias técnicas:
   - Primero, todo CRITICAL, incluidos seguridad (DEF-F7-001 y DEF-F9-001) y facturación (DEF-F6-001…006).
   - Después, los MAJOR que afectan dinero, inventario o salidas sin guía.
   - Al final, MINOR y TRIVIAL.

   Una fase no puede depender de otra posterior. Cada fase debe poder desplegarse y probarse por sí sola, en un tamaño revisable: como guía, no más de 10–12 cambios por fase.
6. **Datos existentes.** Si un defecto dejó datos incorrectos (hashes en la auditoría, depósitos o facturas duplicadas, períodos con fechas repetidas, facturas «por facturar» vencidas), el plan incluye un paso de **saneamiento** con su script o migración descrito. Solo se ejecuta en ambientes de prueba hasta que el usuario lo apruebe para producción.
7. **Pruebas.** Cada cambio define:
   - **(a)** las pruebas automatizadas que se agregan (unitarias o de integración del backend con xUnit, y del frontend con el framework que ya use el repo; verifícalo), con su nombre y lo que afirman;
   - **(b)** los casos QA de re-test: el ID del caso que detectó el defecto (F3-COB-013, E2E-18, F9-API-011…) y los casos REG de la fase 11 que protegen la zona.
8. **Criterios de aceptación** en formato «Dado / Cuando / Entonces», verificables por un tercero sin interpretación, con los valores concretos de la ficha (montos, estados, mensajes exactos en español).
9. **Restricciones de la campaña:**
   - No proponer cambios en producción sin aprobación.
   - No copiar contraseñas ni secretos. El README tiene credenciales: no las transcribas.
   - Los mensajes al usuario van en español.
   - Respetar las convenciones del repositorio y la estructura por features.
   - Las «palancas de tiempo» (SQL para vencer fechas) solo en la base local.
10. **Observaciones (OBS-*)** de los informes: no son defectos. Inclúyelas en el plan solo si una decisión del usuario las convirtió en requisito. Las demás van al anexo §6.6 «Observaciones no incluidas», con una línea de justificación cada una.
11. **Pendientes conocidos** que no son corrección de código: PRF-002 (cronometrar báscula con el operario, pendiente del usuario) y la decisión de recrear la base para la fase 11. Ponlos en el §6.5 o en el §6.7 sin bloquear fases.

## 3. Decisiones del usuario que ya cierran dudas (resumen; la fuente es el §10)

- Vigilancia solo ve y usa Vigilancia; Bodega no opera la portería (DEF-F9-002).
- Permisos de catálogos:
  - terceros: Admin y Comercio Exterior;
  - convenios y tarifas: Admin y Facturación;
  - motivos de ingreso: solo Admin;
  - conductores y vehículos: Vigilancia, Báscula y Admin.
- Se aceptan los catálogos sin autenticación (roles, impuestos, modalidades, embalajes). Cualquier rol puede leer tarifas por API.
- Un solo operario de báscula. DEF-F3-002 es MAJOR (doble envío sin idempotencia).
- Ninguna mercancía de importación sale sin guía (DEF-F5-014, DEF-F8-003).
- La guía de una orden con varios clientes genera **una factura por cada cliente dueño** (en el legacy no se cobraba la guía; es regla nueva).
- La salida con tiquete de ingreso solo admite la mercancía que llegó en ese tiquete.
- La recepción sin báscula deja el depósito **en Borrador** para Comercio Exterior.
- Anular un pesaje ya cobrado deja la factura de báscula pagada (correcto, no se cambia).
- La llegada a Bodega es obligatoria antes del segundo pesaje.
- La hora del pesaje se propone con la hora actual, corregible.
- Báscula lleva IVA 19 %.
- Se eliminan efectivo y cambio del cobro de báscula, también del API.
- Mínimo de almacenamiento configurable con o sin IVA; la aplicación indica si un valor se digita con IVA o neto.
- Facturación puede asignar N.º SIIGO a facturas de contado pagadas.
- Si OnDemand no funciona, se retira de las opciones.
- El reporte de ingresos diarios lista solo Confirmados y Cerrados. Facturación tiene acceso al inventario general.
- Etiqueta «MERCANCIA NACIONALIZADA» con cualquier levante. Una OC puede llevar parte de una unidad de carga.
- El inventario de Bodega muestra los Borradores con mercancía recibida.
- Bodega usa tableta. El modo oscuro funciona y se mantiene.

## 4. Lo que debes investigar por tu cuenta (sin preguntar)

- El estado actual de la «Ola 1» del contexto y de cada WMS-n citado: ¿ya está implementado en `HEAD`?
- El framework de pruebas del frontend y la estructura de pruebas del backend que ya existen.
- Si un cambio de esquema necesita migración de EF Core, y su nombre propuesto.
- Qué defectos comparten archivo, para ordenar los cambios y evitar conflictos de fusión dentro de una fase.

## 5. Antes de escribir el plan

Haz una pasada de verificación y anota los resultados en el §6.2. Por cada ficha:
- ¿Se reproduce en el código de `HEAD`? (sí / no / parcialmente)
- La causa raíz real (`archivo:línea`).
- El grupo de causa (`CHG-NN`) al que pertenece.

No empieces las fases hasta tener esa tabla completa.

## 6. Entregable

Un único archivo **`code_workspace/docs/qa/plan-correccion-defectos.md`**, en español, con esta estructura y en este orden:

1. **Resumen ejecutivo** (máximo 15 líneas): número de fases, cambios y defectos por destino, riesgos principales y orden recomendado.
2. **Verificación en `HEAD`**: tabla `ID | Severidad | ¿Se reproduce? | Causa raíz (archivo:línea) | CHG`.
3. **Matriz de trazabilidad**: `ID | Severidad | Destino (Fase N · CHG-NN / Corregido en … / Duplicado de … / Cerrado por §10) | Casos de re-test`. Exactamente 126 filas, con el conteo final.
4. **Fases**. Por fase:
   - objetivo;
   - criterio de entrada;
   - lista de cambios;
   - orden interno;
   - riesgos y mitigación;
   - saneamiento de datos (si aplica);
   - criterio de salida (pruebas en verde y casos QA que deben pasar);
   - **checkpoint**: qué se entrega al usuario y qué debe aprobar antes de la fase siguiente.

   Por cada cambio, una ficha con:
   - `CHG-NN — título`;
   - defectos que cierra;
   - causa raíz;
   - cambio exacto en backend y frontend (archivo → qué cambia);
   - migración o script;
   - pruebas automatizadas nuevas;
   - criterios de aceptación Dado/Cuando/Entonces;
   - casos QA de re-test;
   - riesgo de regresión;
   - tamaño (S ≤ ½ día, M ≤ 2 días, L ≤ 5 días);
   - dependencias.
5. **Decisiones requeridas**: idealmente vacía. Cada una con su pregunta cerrada, recomendación, alternativa y cambio bloqueado.
6. **Observaciones no incluidas** (OBS-*), con su justificación.
7. **Plan de re-test y cierre**: cómo encaja con la fase 11 (bloques RET y REG), en qué orden se re-testea por fase, y si la base se recrea (pendiente de decisión del usuario).

## 7. Autocontrol antes de entregar

Comprueba y escribe al final del documento una lista de verificación marcada:
- [ ] 126 IDs en la matriz, sin repetidos y sin faltantes (compara contra `INDICE.md`).
- [ ] Todo CRITICAL está en las primeras fases o marcado «Corregido en …» con su commit.
- [ ] Ningún cambio contiene palabras prohibidas (regla 2.4).
- [ ] Ninguna fase depende de una posterior.
- [ ] Todo cambio tiene causa con `archivo:línea`, pruebas automatizadas, criterios Dado/Cuando/Entonces y casos de re-test.
- [ ] Ningún cambio contradice el §10 del plan maestro.
- [ ] No se copió ninguna credencial.

Cuando termines, responde con un resumen breve:
- número de fases y de cambios;
- defectos por destino;
- decisiones requeridas, si las hay;
- ruta del archivo.

Detente ahí: no implementes nada.
