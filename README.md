# Documentación del WMS — Bodegas Asociadas

Hub de documentación del WMS de **Bodegas Asociadas**, un depósito público aduanero en Ipiales (Colombia), en la frontera con Ecuador. El sistema reemplaza al legacy «Bodegas» (PHP) y hoy está **en pruebas en staging con los operarios**.

Este repo es la entrada para cualquier agente o persona que vaya a desarrollar, corregir defectos u operar el proyecto. Lo que describe un solo repo de código y cambia con él (README, runbooks, configuración) vive en ese repo; todo lo demás vive aquí.

## Orden de lectura

1. `contexto/contexto-negocio-wms-para-ia.md`: el negocio, el glosario y cómo funciona el sistema hoy.
2. `contexto/decisiones.md`: decisiones vigentes. No las reabras.
3. `contexto/estado.md`: qué está hecho, qué hay en staging y qué falta.
4. `contexto/convenciones-tecnicas.md`: stack, permisos, migraciones, pruebas y trampas.
5. `procesos/flujo-de-trabajo-agentes.md`: cómo se trabaja, del pedido al commit.
6. Según la tarea:
   - un plan de `planes/`;
   - una ficha de `qa/resultados/defectos/`;
   - `procesos/qa-y-defectos.md`, `procesos/verificacion-local.md` o `procesos/despliegue-staging.md`.
7. `contexto/mapa-de-fuentes.md`, para encontrar cualquier otra cosa.

## Precedencia de las fuentes

Cuando dos fuentes dicen cosas distintas, gana la primera de esta lista:

1. Lo que el usuario pide explícitamente en la tarea.
2. `contexto/decisiones.md`.
3. La sección de decisiones del plan cerrado vigente del tema (`planes/`).
4. El código de `develop`, que dice cómo se comporta el sistema hoy.
5. El resto de los documentos vigentes del hub.
6. `archivo/`, que es histórico y **nunca** es una instrucción.

Si el código contradice una decisión, no «corrijas» ninguno de los dos sin preguntar. Las descripciones de los issues de Linear quedan por debajo de las decisiones: varias respuestas del usuario cambiaron su alcance.

## Estructura

| Carpeta | Contenido |
| --- | --- |
| `contexto/` | Negocio, decisiones, estado, convenciones técnicas y mapa de fuentes |
| `procesos/` | Flujo de trabajo, QA y defectos, verificación local, despliegue a staging |
| `planes/` | Planes cerrados con su estado (índice en `planes/README.md`); paridad con el legacy y migración a staging |
| `analisis/` | Análisis previos a decisiones |
| `qa/` | Campaña QA: plan, casos, plan de corrección, informes, fichas de defecto y evidencias (índice en `qa/README.md`) |
| `videos/` | Guiones y plan de producción de los video tutoriales |
| `manuales/` | Manuales de usuario (revisa su aviso de vigencia) |
| `cliente/` | Formatos impresos y diagramas originales del cliente |
| `plantillas/` | Plantillas de prompt para agentes |
| `archivo/` | Prompts ejecutados y documentos superados. Solo como historia |

## Reglas para escribir aquí

- Escribe en español. Los nombres de código van tal cual, entre comillas invertidas.
- Las rutas en los documentos son relativas a `code_workspace/` (p. ej. `Backend/wms-api/…`, `docs/qa/…`) o a la raíz del hub (p. ej. `contexto/estado.md`).
- **Archivos nuevos:** `tipo-tema-AAAA-MM-DD.md`, en kebab-case (`plan-cerrado-…`, `analisis-…`, `informe-…`). Cambia de carpeta un archivo solo si cambia su estado (p. ej. un prompt ejecutado pasa a `archivo/`). No lo renombres: se perderían las referencias.
- Todo documento de estado lleva fecha de corte y los commits BE/FE a los que se refiere.
- **Sin secretos ni datos de personas reales.** Las credenciales se citan por su ruta (`contexto/mapa-de-fuentes.md` §6). Los informes usan códigos, números de depósito y conteos. `.gitignore` excluye `*.local.*`, `.env*` y `credenciales*`.
- Al cerrar un trabajo, actualiza `contexto/estado.md`, `planes/README.md` y, si hubo una decisión nueva, `contexto/decisiones.md`.
- Los commits los hace el usuario (`DEC-003`).

## Repos relacionados

| Repo | Ruta | Rama |
| --- | --- | --- |
| API .NET | `code_workspace/Backend/wms-api` | `develop` |
| SPA Nuxt | `code_workspace/Frontend/wms` | `develop` |
| Legacy PHP | `code_workspace/bodegas-legacy` | — |
