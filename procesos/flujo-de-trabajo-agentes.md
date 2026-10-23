# Flujo de trabajo para agentes

> **Para qué sirve:** cómo se trabaja en este proyecto, desde que llega un pedido hasta el commit. Aplica a desarrollo nuevo y a corrección de defectos.
> **Fuentes:** decisiones `DEC-001` a `DEC-007` de `contexto/decisiones.md` y las reglas comunes §4.0 de `qa/plan-correccion-defectos.md`, que se siguieron en las 12 fases de corrección.

## 1. Antes de empezar

1. Lee `contexto/contexto-negocio-wms-para-ia.md`, `contexto/convenciones-tecnicas.md`, `contexto/decisiones.md` y `contexto/estado.md`.
2. Si la tarea toca un issue de Linear (`WMS-n`), lee su descripción en Linear **y** las decisiones de `contexto/decisiones.md` que lo citan: varias respuestas del usuario cambiaron el alcance que dice el issue.
3. Si existe un plan cerrado del tema en `planes/`, léelo completo. Su sección de decisiones manda sobre el resto del plan.
4. Comprueba `git status` limpio en `Backend/wms-api` y `Frontend/wms`, ambos en `develop`.
5. Antes de mejorar una pantalla, comprueba que una ronda anterior no la retiró (pasó con la creación manual de facturas).

## 2. Plan cerrado antes del código

Todo cambio que no sea trivial empieza con un **plan cerrado y sin ambigüedades**, que el usuario aprueba antes de tocar código (`DEC-001`).

- **Dónde:** `docs/planes/plan-cerrado-<tema>-AAAA-MM-DD.md`, y una fila nueva en `planes/README.md`.
- **Qué lleva:**
  - Cada duda resuelta, citando su fuente: decisión, código con `archivo:línea` o respuesta del usuario.
  - Decisiones numeradas `D1…Dn`. La numeración es propia de cada plan.
  - Archivos que se tocan, cambios de esquema y migraciones con su nombre, pruebas y orden de fases.
  - Riesgos y criterio de salida de cada fase.
- **Preguntas:** júntalas en **un solo mensaje** y espera la respuesta. No preguntes lo que una decisión ya resuelve (`DEC-002`).
- **Prompts por fase:** si el usuario los pide, van en la misma carpeta del plan. Cuando la fase termina, el prompt se mueve a `archivo/prompts/<tema>/`.

## 3. Implementación por fases

- Se trabaja en `develop` de los dos repos, **sin ramas** (`DEC-003`).
- **El agente no ejecuta `git add`, `git commit`, `git push` ni `git merge`.** Al cerrar cada fase se detiene con un resumen y el usuario hace el commit. Para borrar archivos usa `rm`, no `git rm`.
- Una fase a la vez, en el orden del plan. Cada fase parte del código que dejó la anterior.
- Si el texto del plan choca con una de sus decisiones en un caso borde, gana la decisión. Se aplica y se menciona en una línea, sin pedir aprobación (`DEC-002`).
- Los defectos bloqueantes que aparezcan se corrigen antes de pasar a la fase siguiente.
- Ningún cambio de permisos quita a un rol una función que usa (`DEC-005`).

## 4. Migraciones y bases de datos

Regla vigente desde el 2026-10-04 (`DEC-004`); el detalle está en `contexto/convenciones-tecnicas.md` §5.

- El agente genera, aplica, revierte o elimina migraciones **solo con `dotnet ef`** y **solo contra la base local**.
- **Nunca edites a mano** `Wms.Infrastructure/Migrations/*`, los `*.Designer.cs` ni el snapshot. Si la migración no sale como se espera, corrige el modelo y regenérala.
- Nunca SQL manual contra una base.
- Staging y producción solo con aprobación explícita del usuario, con el procedimiento de `procesos/despliegue-staging.md`.
- Al cerrar la fase, `dotnet ef migrations has-pending-model-changes` debe salir limpio, y la migración va en el mismo commit que el código.

## 5. Compuertas de salida de una fase

Toda fase cierra con:

- `dotnet build Wms.sln` sin errores.
- `dotnet test` en verde: `Wms.Tests` y `Wms.IntegrationTests` (este último necesita Docker).
- En el frontend, `yarn build` con código 0 y `yarn test` en verde.
- `yarn lint` con igual o menos errores que al cierre de la fase anterior, y cero errores en archivos nuevos.
- Los casos QA de la fase en PASA, si el plan los define.

Informa las cifras: número de pruebas y errores de lint, antes y después.

## 6. Corrección de defectos

- Un defecto se describe en una ficha `DEF-*` (ver `procesos/qa-y-defectos.md`). Para corregirlo, lee la ficha, el informe de la fase que lo detectó y su evidencia.
- La regla se extrae a una clase pura y se prueba en `Wms.Tests`. Lo que depende de EF, índices o transacciones se prueba en `Wms.IntegrationTests`.
- Al terminar, actualiza la ficha a «Corregido» con el commit base y la lista de verificación. La pasa a «Verificado» quien hace el re-test.

## 7. Al cerrar el trabajo

- Marca el estado en el plan (tabla de fases o bloque «Estado» de la fase) y en `planes/README.md`.
- Actualiza `contexto/estado.md` si cambió algo del estado general. Si tomaste o recibiste una decisión nueva, agrégala a `contexto/decisiones.md`.
- Entrega el mensaje de commit propuesto para cada repo.

## 8. Qué no hacer

- No reconstruyas ni cites como vigentes las fuentes perdidas (`contexto/mapa-de-fuentes.md` §7).
- No tomes como instrucción nada de `archivo/`.
- No copies credenciales ni datos de personas reales a documentos, prompts o commits.
- No conviertas una carencia del modelo de datos en una prohibición de negocio.
- No subas `pageSize` para traer todo: usa `all=true`.
