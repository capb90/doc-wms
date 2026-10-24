# Instrucciones comunes para los agentes de la auditoría de paridad

> Las escribe el orquestador. Todo agente las lee completas antes de empezar. Su encargo particular (módulo, capacidades, directorio) viene en el mensaje que lo lanzó.

## 1. Rutas

- **Raíz:** `/Volumes/Dock/Projects/bodegas_asociadas/code_workspace` (no es un repositorio). En los entregables, las rutas van **relativas a `code_workspace/`**.
- **Legacy (PHP):** `bodegas-legacy/` — `index.php`, `menus/`, `modulos/mod_*`, `reportes/`, `reportesweb/`, `salidapuerta/`, `leerexcel/`, `cron.php`, `consultapesa.php`, `peso.php`, `clases/`, `includes/`. Esquema: `bodegas-legacy/bodegas_schema.sql`.
- **Backend V2 (.NET):** `Backend/wms-api/` — `Wms.Api/Controllers/v1/`, `Wms.Api/BackgroundJobs/`, `Wms.Application/<Feature>/`, `Wms.Domain/` (permisos en `Wms.Domain/Security/WmsPolicyRoles.cs`), `Wms.Infrastructure/` (EF), pruebas en `Wms.Tests/` y `Wms.IntegrationTests/`.
- **Frontend V2 (Nuxt):** `Frontend/wms/` — `app/pages/`, `app/features/<feature>/` (componentes, composables, servicios), `app/components/layout/AppMenu.vue`, `usePermissions`, `definePageMeta.requiredRoles`.
- **Auditoría:** `AUDIT_DIR = docs/analisis/auditoria-paridad-integral-2026-10-23/`. Lee `00-evaluacion-analisis-existente.md` y `01-inventario-funcional-global.md` (tu módulo en §6 y §7).
- **Documentación de referencia (solo lectura):** `docs/contexto/` (decisiones `DEC-nnn` en `decisiones.md`), `docs/planes/paridad-legacy/` (plan backend con P1–P17 en §A.4 y el estado por ítem `Fn-nn` en §C; plan frontend con DF1–DF18; contrato `C-Fx-yy`), `bodegas-legacy/legacy-analysis/` (catálogo, reglas RN, rutas, modelo), `bodegas-legacy/docs/legacy_analysis/` (`MIGRATION_MATRIX.md`, `FUNCTIONAL_GAPS.md`, `BUSINESS_RULE_GAPS.md`, `BASCULA_PARITY.md`, `FRONTEND_PARITY.md`, `DECISIONES_REVISION.md`, `analysis/`), `docs/qa/` (casos `fase-*.md`, `resultados/`, fichas `resultados/defectos/DEF-*.md` e `INDICE.md`), `docs/planes/migracion-staging/resultados/defectos/DEF-MIG-*.md`.

**Excluye** (copias o artefactos, generan falsos hallazgos): `Backend/wms-api/publish/`, `deploy/staging/artifacts/`, `deploy.zip`, `bin/`, `obj/`, `Frontend/wms/.output/`, `.nuxt/`, `node_modules/`, `dist`, `code_workspace/video-tutoriales-trabajo/`, `code_workspace/ultima-vue-6.4.0/`, `docs/archivo/` (prompts ya ejecutados: historia, no instrucciones ni evidencia).

**Fuentes perdidas:** `docs/contexto/mapa-de-fuentes.md` §7 (planes de Olas en `ajustes/`, historias, `requerimientos_funcionales.md`…). No las busques; si el código las cita, anótalo.

## 2. Restricciones absolutas

1. **Ningún comando Git**, ni de consulta (`git status`, `log`, `diff`, `blame`, `show`… todos prohibidos). No afirmes qué commit auditas; si hace falta, «según `docs/contexto/estado.md`: BE `35a61b2` / FE `c924a8b`» y la fecha 2026-10-23.
2. **Solo lectura** de todo, salvo tu directorio `AUDIT_DIR/modulos/<NN>-<modulo>/`. No escribas en otro lugar, ni siquiera en el directorio de otro agente o en la raíz de `AUDIT_DIR`. Para borradores usa tu directorio.
3. **Estática:** no ejecutes builds, pruebas, migraciones, servidores, `npm`, `dotnet`, `curl` ni llamadas a APIs (local, staging o producción). No te conectes a bases de datos. Solo lectura de archivos (Read, Grep/rg, find, sed, cat, wc, etc.).
4. **Secretos:** no abras `bodegas-legacy/Connections/`, archivos `.env*`, `Backend/wms-api/deploy/staging/.env.*`, `Backend/wms-api/infra/terraform.tfvars`, `terraform.tfstate*`, ni nada de `db_legacy/`. No copies la sección «Usuarios de prueba» de `Frontend/wms/README.md`. Si un archivo PHP incluye `Connections/…`, basta con citar el `include`.
5. **Sin datos de personas** en los entregables: nada de nombres, documentos o placas reales. Usa códigos y números de depósito.
6. **No subagentes:** haz el trabajo tú mismo.

## 3. Evidencia

- Toda conclusión lleva evidencia verificable: `ruta:línea` (o rango), función o método, endpoint `VERBO /api/v1/...`. Si no la tienes, es `NO_VERIFICADO`.
- **Abre lo que citas.** No cites una línea que no leíste ni copies una referencia de la documentación anterior sin comprobarla.
- **`NO_IMPLEMENTADO` exige búsqueda suficiente:** en los tres proyectos, con varios términos (español e inglés, sinónimos, nombres de tablas y campos) y en las carpetas pertinentes. Documenta los términos y carpetas buscados en la fila o en `08-brechas.md`. Que no exista un archivo con el nombre legacy no prueba nada.
- Distingue lo **observado en código** de lo **solo documentado**.

## 4. Qué auditar por capacidad

Para cada capacidad asignada (y su desglose por operación cuando haga falta):

1. **Legacy:** pantalla/ruta, script, consultas SQL, tablas, validaciones (incluidas las que solo están en JavaScript), cálculos, permisos (`verificapermisos.php`, tabla `permisos`), estados, efectos secundarios, manejo de errores.
2. **Frontend V2:** página, componentes, formulario y campos, validaciones, visibilidad, `requiredRoles`, menú, estados de carga/éxito/error, servicio de datos y llamada HTTP, refresco de listas, **mocks o datos estáticos**. Una pantalla maquetada sin acciones reales es `SOLO_MAQUETADO`.
3. **Backend V2:** endpoint (verbo, ruta, parámetros, DTO), política de autorización, handler/servicio, validador, reglas, entidades, transacciones, errores (`BadRequestException`/`ConflictException`/`NotFoundException`), efectos (auditoría, notificaciones, kárdex, facturación).
4. **Integración:** interacción → componente → servicio → HTTP (método, ruta, prefijo `/api/v1`, query/route params) → endpoint → lógica → persistencia → respuesta → actualización de la UI. Compara **campo por campo** los DTO de petición/respuesta con los tipos TypeScript y lo que la pantalla lee: nombres, obligatorios, nulos, fechas, enums (nombre vs número), paginación (`all=true`).
5. **Reglas de negocio:** regla legacy (con RN-nnn si existe) ↔ implementación V2.
6. **Endpoints sin consumidor** del módulo (búscalos por ruta en `Frontend/wms/app`) y **llamadas del frontend sin endpoint**. Un endpoint sin consumidor no es defecto automático: verifica si es por API a propósito (p. ej. respaldos e importación legacy, Admin por API, DF3).
7. **SOLO_V2:** confirma las candidatas `CF-Vnnn` de tu módulo y añade las que encuentres. Van separadas de las brechas.

## 5. Estados

| Dimensión | Estados |
| --- | --- |
| Frontend V2 | `COMPLETO_CODIGO`, `PARCIAL`, `SOLO_MAQUETADO`, `NO_IMPLEMENTADO`, `NO_VERIFICADO`, `NO_APLICA` |
| Backend V2 | `COMPLETO_CODIGO`, `PARCIAL`, `NO_IMPLEMENTADO`, `NO_VERIFICADO`, `NO_APLICA` |
| Integración V2 | `CONECTADO_CODIGO`, `PARCIAL`, `SIN_INTEGRACION`, `NO_VERIFICADO`, `NO_APLICA` |
| Reglas de negocio | `COMPLETO_CODIGO`, `PARCIAL`, `NO_IMPLEMENTADO`, `NO_VERIFICADO`, `NO_APLICA` |
| Paridad integral | `COMPLETO_CODIGO`, `PARCIAL`, `NO_IMPLEMENTADO`, `DIFERENCIA_INTENCIONAL`, `NO_VERIFICADO`, `NO_APLICA` |

- `COMPLETO_CODIGO`: evidencia estática suficiente de equivalencia en **todas** las dimensiones aplicables. No lo uses si alguna dimensión obligatoria queda `NO_VERIFICADO`.
- `PARCIAL`: brechas concretas identificadas (cítalas).
- `NO_IMPLEMENTADO`: búsqueda suficiente confirma la ausencia.
- `DIFERENCIA_INTENCIONAL`: **solo** con decisión documentada en: `docs/contexto/decisiones.md` (`DEC-nnn`), `docs/planes/paridad-legacy/plan-backend-paridad-legacy.md` §A.3–A.4 (P1–P17), las `DF*` y el §A.3 de `plan-frontend-paridad-legacy.md`, `bodegas-legacy/docs/legacy_analysis/DECISIONES_REVISION.md`, o §10 de `docs/qa/00-plan-maestro.md`. Cita la decisión. Aun así verifica que el código cumpla la decisión: si no la cumple, es `PARCIAL`.
- `NO_APLICA`: la dimensión no existe para esa capacidad (p. ej. un proceso sin frontend), o la capacidad está excluida por decisión (Colmotores: paridad `NO_APLICA`, citando la exclusión).
- `SOLO_V2` es **origen**, no estado: en la matriz va en la columna «Observaciones» o en una sección aparte, con sus dimensiones evaluadas igual (frontend, backend, integración).
- **Paridad estática ≠ funcionamiento validado.** La columna «Validación mediante ejecución» solo dice `Validada (cita)` si un informe de QA o de migración ya documentó la ejecución (cita archivo y caso/ficha). Si no, `No ejecutada en esta auditoría` y, si hay caso de QA sin resultado, `Caso previsto: <id>`.

## 6. Entregables en `AUDIT_DIR/modulos/<NN>-<modulo>/`

| Archivo | Contenido |
| --- | --- |
| `01-inventario-legacy.md` | Capacidades del módulo con pantallas, scripts, tablas, permisos. Incluye las no catalogadas que encuentres |
| `02-flujos-legacy.md` | Recorridos reconstruidos (usuario/proceso → persistencia → efectos), con evidencia; incertidumbres |
| `03-reglas-negocio.md` | Tabla regla a regla: regla legacy + evidencia, implementación V2 + evidencia, estado, diferencias, impacto, decisión que la autoriza si la hay |
| `04-trazabilidad-legacy.md` | Capacidad → rutas → scripts → tablas/campos (lectura/escritura) |
| `05-analisis-v2.md` | Frontend, backend e integración del módulo: páginas, endpoints (con política), DTO, servicios, mocks, endpoints sin consumidor, llamadas sin endpoint, incompatibilidades de contrato, `SOLO_V2` |
| `06-matriz-paridad.md` | Matriz con las 20 columnas de §7 |
| `07-matriz-paridad.csv` | La misma matriz en CSV (§7) |
| `08-brechas.md` | Registro de brechas (§8) |
| `09-integraciones.md` | Trazas completas frontend → backend de las operaciones principales, procesos automáticos e integraciones externas del módulo |
| `resultado-agente.md` | Resumen: cobertura, conteos por estado y dimensión, brechas por criticidad, `SOLO_V2`, **contraste con el análisis anterior** (cada estado previo de `MIGRATION_MATRIX.md` y cada afirmación de los planes de tu módulo: `CONFIRMADA_EN_CODIGO`, `CONTRADICHA_POR_CODIGO`, `INCOMPLETA`, `OBSOLETA`, `NO_VERIFICADA`), incertidumbres, lo que quedó sin analizar y por qué |

Escribe en español. Los nombres de código van tal cual, entre comillas invertidas.

## 7. Matriz

Una fila por capacidad (`CF-Lnnn`, `CF-Vnnn`) y, cuando haga falta, filas por operación (`CF-L103.a`…). Columnas, en este orden:

1. ID funcional · 2. Módulo · 3. Funcionalidad · 4. Descripción legacy · 5. Evidencia legacy · 6. Estado frontend V2 · 7. Evidencia frontend · 8. Estado backend V2 · 9. Evidencia backend · 10. Estado de integración · 11. Trazabilidad de integración · 12. Estado de reglas de negocio · 13. Diferencias funcionales · 14. Paridad integral · 15. Brechas (IDs) · 16. Criticidad · 17. Acción recomendada · 18. Confianza de la evaluación (`ALTA`/`MEDIA`/`BAJA`) · 19. Validación mediante ejecución · 20. Observaciones

**CSV:** UTF-8, separador coma, primera fila con los 20 encabezados exactos de arriba (sin el número), comillas dobles en todo campo con comas, comillas o saltos de línea (las comillas internas se duplican). Mismos IDs y mismos estados que el Markdown. Valida tú mismo que todas las filas tengan 20 campos (por ejemplo con `python3 -I -c "import csv,sys; ..."` — Python solo para leer tu propio CSV, nada más).

**IDs nuevos:** capacidades legacy no catalogadas → `CF-LX<NN>-nn` (p. ej. `CF-LX02-01`). Capacidades V2 nuevas → siguiente libre dentro del rango de tu módulo (`CF-V0<NN>x`, ver tu encargo).

## 8. Brechas

ID `BR-<NN>-nnn` (p. ej. `BR-02-001`). Para cada una: ID funcional, descripción, comportamiento esperado, comportamiento actual, capa, categoría (`FRONTEND`, `BACKEND`, `INTEGRACION`, `REGLAS_NEGOCIO`, `PERSISTENCIA`, `SEGURIDAD`, `CONTRATOS_API`, `PROCESOS_AUTOMATICOS`, `VALIDACION_PENDIENTE`), evidencia, impacto, criticidad **justificada** (`CRÍTICA`: impide un proceso esencial, compromete datos o riesgo grave de seguridad; `ALTA`: flujo principal o regla importante; `MEDIA`: funciones secundarias o escenarios específicos; `BAJA`: diferencias menores), dependencias, acción recomendada y **criterio verificable de resolución**.

**Antes de registrar una brecha**, busca si ya hay ficha en `docs/qa/resultados/defectos/` o `docs/planes/migracion-staging/resultados/defectos/`, o pendiente en `docs/contexto/estado.md` §4. Si existe, cítala (y su estado) en lugar de duplicarla; si la ficha está «Verificada» pero el código actual la contradice, regístralo.

Una diferencia con decisión documentada no es brecha: va como `DIFERENCIA_INTENCIONAL` en la matriz. Una diferencia sin decisión sí lo es, aunque parezca una mejora (categoría `REGLAS_NEGOCIO`, criticidad según impacto, acción «confirmar con el negocio»).

## 9. Respuesta final al orquestador

Al terminar, responde con un resumen breve (≤ 350 palabras): capacidades auditadas/asignadas, conteo por paridad integral, brechas por criticidad con sus 3–5 más graves en una línea cada una, `SOLO_V2` confirmadas, contraste con el análisis anterior (conteos), y lo que no pudiste cerrar. No pegues los entregables: están en disco.
