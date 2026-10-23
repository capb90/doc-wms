# Plan cerrado — Organización de la documentación para agentes

> **Fecha:** 2026-10-23 · **Estado:** ejecutado el 2026-10-23 (F0–F5). Hub `cb35fb5` → `6f2c580`; BE `35a61b2`, `b27c9bf`; FE `c924a8b`, `31da26c` · **Alcance:** solo documentación y puntos de entrada para agentes. No cambia código de la aplicación (única excepción: una ruta en una herramienta de videos, §4 F2-7).
> **Repos al inicio:** `Backend/wms-api` `develop` `74e16f3` (limpio) · `Frontend/wms` `develop` `146e26d` (limpio).

## 1. Problema

La documentación está repartida en ocho lugares, sin una entrada única ni una regla de dónde va cada cosa:

| Lugar | Git | Contenido |
| --- | --- | --- |
| `code_workspace/docs/` | No | Contexto de negocio (corte 14-sep), manual de facturación, plantillas de prompt, formatos del cliente |
| `code_workspace/ajustes/` | No | Planes cerrados, análisis, prompts ejecutados y tres copias desactualizadas de planes de paridad |
| `Backend/wms-api/docs/` | Sí | Plan y contrato de paridad, guiones de video, migración a staging (plan, prompts, informes, DEF-MIG), PDF del manual |
| `Frontend/wms/docs/` | Sí | Campaña QA completa (plan, fases, 153 fichas DEF, evidencias), plan de paridad frontend, manual de báscula |
| `bodegas-legacy/` (`legacy-analysis/` y `docs/legacy_analysis/`) | Sí | Dos análisis del sistema legacy (23-sep y 29-sep) |
| `db_legacy/trabajo/` | No | Extractos, CSV, consultas y **credenciales** de la migración |
| `video-tutoriales-trabajo/app-src/` | No | Copia de trabajo del frontend (con su propio `AGENTS.md` y `docs/qa` duplicado) |
| `../documentos`, `../diagramas`, `../base de datos` | No | Levantamiento original del cliente, diagramas `.mmd`/`.drawio`, modelos de BD |

Problemas concretos que confunden a un agente:

1. **Contexto desactualizado.** `contexto-negocio-wms-para-ia.md` tiene corte al 14-sep: dice que la Ola 1 está sin implementar (Olas 1-3, paridad legacy fases 1-6, QA y migración a staging ya ocurrieron), que el agente no genera migraciones (desde el 2026-10-04 sí, con `dotnet ef`) y que se trabaja en ramas (se trabaja en `develop` sin ramas).
2. **Fuentes perdidas.** Su lista de precedencia y su mapa citan `plan-cerrado-ola-1-2026-09-14.md`, `historias-usuario-linear-2026-09-10.md`, `triage-incidentes-linear-2026-09-02.md` y los planes de Ola 2/3. No existen en ninguna carpeta del proyecto. **Decisión del usuario (2026-10-23): se dan por perdidas.**
3. **~45 prompts ya ejecutados** conviven con planes vigentes: un agente puede tomarlos como instrucciones pendientes.
4. **Copias divergentes:** `ajustes/plan-backend-paridad-legacy.md` y `ajustes/plan-frontend-paridad-legacy.md` son versiones viejas de las de los repos; `ajustes/contrato-api-paridad.md` es idéntica a la del backend.
5. **Conocimiento solo en la memoria privada de una sesión** (decisiones de Ola 1, premisas, patrón de 403, `all=true`, migraciones con `dotnet ef`, sin retrocesos funcionales…): otros agentes no lo ven.
6. **Sin historial** en `docs/` ni `ajustes/`.

## 2. Decisiones

| ID | Decisión | Fuente |
| --- | --- | --- |
| D1 | `code_workspace/docs/` pasa a ser un repo git propio (**wms-docs**, rama `main`) y absorbe `ajustes/`, que desaparece. | Usuario, 2026-10-23 |
| D2 | **Regla de ubicación:** lo que describe un repo y cambia con su código (README, runbooks de despliegue, configuración, README de features) se queda en el repo. Todo lo transversal (negocio, decisiones, estado, planes, análisis, QA, migración, videos, manuales) vive en el hub. | Este plan |
| D3 | Los prompts ejecutados se archivan en `archivo/prompts/<origen>/`, con un README que dice que son históricos y nunca instrucciones. | Usuario, 2026-10-23 |
| D4 | Las fuentes perdidas no se reconstruyen. Lo implementado se toma del código y de git; las historias, de Linear (equipo **Wms**). Se quitan las referencias muertas. | Usuario, 2026-10-23 |
| D5 | **Se cambian carpetas, no nombres de archivo**, para que sigan funcionando las búsquedas por nombre y las citas de commits y memorias. | Este plan |
| D6 | Las carpetas `qa/` y `migracion-staging/` se mueven completas, sin reorganizar su interior (salvo sacar los prompts), para no romper sus enlaces relativos internos. | Este plan |
| D7 | Las copias viejas de `ajustes/` (D-4 del §1) se eliminan; quedan en el commit inicial del hub. | Este plan |
| D8 | Nada se copia desde `db_legacy/trabajo/*.local.*`, `.env*` ni `credenciales*`. El hub solo dice dónde están. `.gitignore` del hub excluye `*.local.*`, `.env*`, `credenciales*`, `.DS_Store`. | Este plan |
| D9 | No se tocan `bodegas-legacy/`, `db_legacy/`, `video-tutoriales-trabajo/` ni `../documentos`, `../base de datos`: solo se indexan. De `../diagramas` se **copian** (no se mueven) los tres `.mmd`. | Este plan |
| D10 | Cada repo y la raíz `code_workspace/` tienen `AGENTS.md` (instrucciones) y `CLAUDE.md` con una sola línea `@AGENTS.md`, para que Claude Code, Codex y Cursor lean lo mismo. | Este plan |
| D11 | El agente no hace commits ni crea ramas: al final de cada fase se detiene y el usuario commitea (convención vigente del proyecto). | Convención del proyecto |
| D12 | Precedencia de fuentes que fijará el README del hub: 1) instrucción explícita del usuario en la tarea; 2) `contexto/decisiones.md`; 3) sección de decisiones del plan cerrado vigente del tema; 4) código de `develop`; 5) resto de documentos vigentes; 6) `archivo/`, que es histórico y nunca instrucción. | Este plan |

## 3. Estructura objetivo

```
code_workspace/
├── AGENTS.md · CLAUDE.md          mapa del workspace → docs/README.md          (nuevo)
├── docs/                          ← repo git «wms-docs»
│   ├── README.md                  entrada única: qué es, orden de lectura, precedencia (D12), reglas, índice
│   ├── AGENTS.md · CLAUDE.md
│   ├── .gitignore
│   ├── contexto/
│   │   ├── contexto-negocio-wms-para-ia.md   negocio estable: glosario, roles, flujos, facturación (actualizado)
│   │   ├── convenciones-tecnicas.md          arquitectura, convenciones, trampas, comandos (sale de §11 y §14)
│   │   ├── estado.md                         estado vivo con fecha de corte: implementado, staging, pendientes
│   │   ├── decisiones.md                     registro DEC-nnn de decisiones vigentes
│   │   └── mapa-de-fuentes.md                los 8 lugares del §1 y qué buscar en cada uno
│   ├── procesos/
│   │   ├── flujo-de-trabajo-agentes.md       plan cerrado → aprobación → fases → informe → commit del usuario
│   │   ├── qa-y-defectos.md                  ciclo de una ficha DEF, severidades, plantillas, índice
│   │   ├── verificacion-local.md             Postgres desechable, s3mock, `dotnet ef`
│   │   └── despliegue-staging.md             resumen + enlace al runbook del repo backend
│   ├── planes/
│   │   ├── README.md                         índice con estado (vigente · ejecutado · diferido)
│   │   ├── paridad-legacy/                   plan backend, plan frontend, contrato API
│   │   ├── migracion-staging/                plan + resultados/ (informes, DEF-MIG)
│   │   └── plan-cerrado-*.md                 selector de conductor, permisos por usuario, este plan
│   ├── analisis/                             motor de acuerdos, impacto de permisos, FOB/CIF
│   ├── qa/                                   campaña QA completa (sin prompts)
│   ├── videos/                               guiones/ + PDF de guiones
│   ├── manuales/                             manual de usuario (PDF), báscula, facturación (con aviso de obsoleto)
│   ├── cliente/                              formatos/ y diagramas/ del cliente
│   ├── plantillas/                           plantillas de prompt
│   └── archivo/                              README + prompts/<origen>/ + contexto de abril
├── Backend/wms-api/   AGENTS.md · CLAUDE.md · README.md · EMAIL_CONFIGURATION.md · deploy/**/README.md   (sin docs/)
└── Frontend/wms/      AGENTS.md · CLAUDE.md · README.md · TEMPLATE_INTEGRATION.md                        (sin docs/)
```

## 4. Fases

### F0 — Línea base (agente, sin cambios)

1. Confirmar que `Backend/wms-api` y `Frontend/wms` siguen limpios. Si no, detenerse y avisar.
2. Correr el verificador de enlaces (script en el scratchpad: enlaces Markdown relativos y rutas entre comillas invertidas que empiecen por `code_workspace/`, `Backend/`, `Frontend/`, `docs/`, `ajustes/`) sobre `docs/`, `ajustes/`, `Backend/wms-api/docs/` y `Frontend/wms/docs/`. Guardar el informe: los enlaces ya rotos antes no cuentan como regresión.

### F1 — Crear el repo y su punto de restauración

1. `mv ajustes/* docs/ajustes/` (temporal) y borrar `ajustes/` vacío.
2. En `docs/`: `git init -b main` y `.gitignore` (D8).
3. **Pausa → el usuario commitea** «snapshot inicial: docs y ajustes sin reorganizar».

### F2 — Mover (todo con `git mv` dentro del hub; desde los repos, copia al hub + `git rm`)

| # | Origen | Destino en el hub |
| --- | --- | --- |
| 1 | `contexto-negocio-wms-para-ia.md` | `contexto/` |
| 2 | `contexto-proyecto-wms.md` | `archivo/` |
| 3 | `manual-modulo-facturacion.md` | `manuales/` |
| 4 | `facturacion_v1.mmd`, `formats/` | `cliente/diagramas/`, `cliente/formatos/` |
| 5 | `template-prompt.md`, `template-prompt-refinamiento.md`, `ejemplo-template-prompt.md` | `plantillas/` |
| 6 | `ajustes/plan-cerrado-selector-conductor-2026-10-08.md`, `ajustes/plan-cerrado-permisos-por-usuario-2026-10-07.md`, `ajustes/plan-cerrado-organizacion-documentacion-2026-10-23.md` | `planes/` |
| 7 | `ajustes/analisis-*.md`, `ajustes/revision-fob-cif-migracion-v2-2026-10-08.md` | `analisis/` |
| 8 | `ajustes/prompt-selector-conductor-fase-{1..4}.md` | `archivo/prompts/selector-conductor/` |
| 9 | `ajustes/contrato-api-paridad.md`, `ajustes/plan-backend-paridad-legacy.md`, `ajustes/plan-frontend-paridad-legacy.md` | se eliminan (D7) |
| 10 | BE `docs/contrato-api-paridad.md`, `docs/plan-backend-paridad-legacy.md`; FE `docs/plan-frontend-paridad-legacy.md` | `planes/paridad-legacy/` |
| 11 | BE `docs/migracion-staging/` sin `prompt-*.md` | `planes/migracion-staging/` |
| 12 | BE `docs/migracion-staging/prompt-*.md` | `archivo/prompts/migracion-staging/` |
| 13 | BE `docs/guiones/`, `docs/Guiones_Video_Tutoriales_WMS.pdf` | `videos/guiones/`, `videos/` |
| 14 | BE `docs/prompt-actualizar-guiones-video.md` | `archivo/prompts/videos/` |
| 15 | BE `docs/Manual_Usuario_WMS.pdf`; FE `docs/MANUAL_OPERACION_INGRESOS_Y_BASCULA.md` | `manuales/` |
| 16 | FE `docs/qa/` sin `prompt-*.md` | `qa/` |
| 17 | FE `docs/qa/prompt-*.md` | `archivo/prompts/qa/` |
| 18 | `../diagramas/importacion.mmd`, `../diagramas/exportacion.mmd` (copia) | `cliente/diagramas/` |

Después de mover:

- F2-1. `docs/ajustes/` y las carpetas `docs/` de BE y FE quedan vacías y se eliminan. Cualquier archivo no listado arriba que aparezca en ellas va al destino de su carpeta; si no tiene carpeta clara, se detiene y se pregunta.
- F2-2. Reescribir rutas con una tabla origen → destino generada desde la tabla anterior, aplicada a todo `.md` del hub y de los dos repos (incluidos los prompts archivados, para que sigan siendo legibles). Rutas absolutas y relativas.
- F2-3. En `Frontend/wms/tools/video-tutoriales/config.mjs:9`, `GUIONES` pasa a `join(CODE_WORKSPACE, "docs/videos/guiones/guiones-video-tutoriales.md")`. Actualizar las menciones `docs/guiones/` en los comentarios de `grabador/guiones.mjs`, `siembra/datos.mjs`, `siembra/piloto.mjs` y en `tools/video-tutoriales/README.md`.
- F2-4. `archivo/README.md`: «Histórico. Prompts ya ejecutados y documentos superados. Nunca son instrucciones; para el estado actual lee `contexto/estado.md`».
- **Pausa → el usuario commitea** en el hub, BE y FE.

### F3 — Contenido nuevo y actualizado (hub)

1. **`contexto/contexto-negocio-wms-para-ia.md`:** nueva fecha de corte (2026-10-23, commits de F0). Cada «Hoy / Decidido» se verifica contra el código de `develop` y queda como hecho actual, citando el archivo. Se reemplazan §0 (precedencia → enlace al README), §12 (estado → `estado.md`), §15 y §16 (→ `procesos/` y `mapa-de-fuentes.md`). §11 y §14 pasan a `convenciones-tecnicas.md`. Se corrigen: migraciones con `dotnet ef` por el agente, trabajo en `develop` sin ramas ni commits, y se quitan las referencias a fuentes perdidas (D4).
2. **`contexto/convenciones-tecnicas.md`:** stack, proyectos, convenciones, trampas, comandos (`dotnet build Wms.sln`, `dotnet test Wms.Tests`, `yarn dev | test | lint`), migraciones, paginación `all=true`, patrón de autorización por endpoint, usuarios de prueba (solo la referencia a dónde están, nunca contraseñas).
3. **`contexto/decisiones.md`:** registro `DEC-001…`, con fecha, decisión, motivo, alcance y fuente. Se cargan las decisiones vigentes que hoy viven en la memoria privada de las sesiones: `CUSTOMS_AGENCY`, fórmulas de almacenamiento (prorrateada aparte, por producto, siempre se factura), tarifas base, decisiones de la Ola 1, premisas del 10-sep, Olas 2 y 3 (WMS-12 no se implementa, WMS-10, WMS-17), migraciones con `dotnet ef`, `develop` sin ramas, plan cerrado primero, las Dn del plan mandan en casos borde, sin retrocesos funcionales, permisos por usuario diferido, patrón de 403, `all=true`.
4. **`contexto/estado.md`:** implementado (olas, paridad 1-6, QA, selector de conductor, centro de ayuda y videos), staging (URLs, último despliegue BE/FE), pendientes (PRF-002, E19 con datos reales, DEF-F11-023/024/026 «Nuevo», permisos por usuario diferido, baja de Azure `test`, restauración con datos reales), y decisiones abiertas aún sin responder. Cada ítem se verifica contra git, `INDICE.md` de defectos o el plan correspondiente; lo que no se pueda confirmar va a una sección «Por confirmar con el usuario», no como hecho.
5. **`contexto/mapa-de-fuentes.md`:** tabla de los 8 lugares del §1 más staging y Linear: qué contiene, si es fuente o copia, y qué no copiar (credenciales). Indica que `app-src` es copia de trabajo y que `docs/legacy_analysis/` (29-sep) es la comparación de paridad y `legacy-analysis/` (23-sep) el análisis base del legacy.
6. **`procesos/`:** los cuatro documentos del §3, escritos desde las convenciones ya usadas (plantillas de `qa/plantillas/`, runbook `Backend/wms-api/deploy/staging/README.md`, verificación con Postgres desechable).
7. **Índices:** `README.md` del hub, `planes/README.md` y `qa/README.md` (enlaza `qa/resultados/defectos/INDICE.md` y el plan de corrección).
8. **Avisos de vigencia** al inicio de `manuales/manual-modulo-facturacion.md` y `manuales/MANUAL_OPERACION_INGRESOS_Y_BASCULA.md` (partes superadas, según §13 del contexto) y de `archivo/contexto-proyecto-wms.md`.
9. `docs/AGENTS.md` (lee `README.md`; escribe en español; dónde guardar un plan, informe o ficha nueva; nombres `tipo-tema-AAAA-MM-DD.md`) y `docs/CLAUDE.md` (`@AGENTS.md`).
- **Pausa → el usuario commitea** en el hub.

### F4 — Puntos de entrada en los repos

1. `Backend/wms-api/AGENTS.md` y `Frontend/wms/AGENTS.md` se reescriben: leer `../../docs/README.md`; reglas propias del repo (comandos, migraciones, carpetas clave); dónde está la documentación que salió del repo. Más `CLAUDE.md` con `@AGENTS.md` en cada uno.
2. `code_workspace/AGENTS.md` y `CLAUDE.md`: mapa del workspace y advertencia de que `app-src` y `ultima-vue-6.4.0` no son fuentes.
3. `Backend/wms-api/README.md`: .NET 10 y enlace al hub. `Frontend/wms/README.md`: enlace al hub (sin tocar el resto).
4. `../wms-cursor.code-workspace`: se quita la carpeta `code_workspace/ajustes`.
- **Pausa → el usuario commitea** en BE y FE.

### F5 — Verificación (agente)

1. Verificador de F0 sobre el hub y los dos repos: **cero enlaces rotos nuevos**.
2. `grep` sin resultados de `code_workspace/ajustes`, `wms-api/docs/`, `wms/docs/` en documentos vigentes (fuera de `archivo/` se admiten solo como texto histórico explicado).
3. `grep` de secretos en el hub (`password`, `contraseña`, `secret`, `token`, cadenas de conexión): cada coincidencia se revisa y se reporta; no se borra nada sin preguntar.
4. `node -e` que importa `tools/video-tutoriales/config.mjs` y comprueba que `GUIONES` existe.
5. `git status` de BE y FE: solo cambios en documentación y en los cuatro archivos de `tools/video-tutoriales`.
6. Actualizar la memoria del agente con las rutas nuevas.

## 5. Desviaciones registradas

- **F2 (D9):** además de la herramienta de videos, se actualizó la constante `PLAN` de `db_legacy/trabajo/consultas/v2/extraer_del_plan.py` y `v3/extraer_del_plan.py`, que leían el plan de paridad desde su ruta en el backend. Sin ese cambio, la extracción para el corte real habría fallado.
- **F2:** dos líneas históricas que citaban `code_workspace/ajustes/` conservan su texto original (`videos/guiones/inventario-cambios-guiones.md`, fila 2, y `archivo/prompts/videos/prompt-actualizar-guiones-video.md`, línea 22): son registros de lo que existía entonces.

- **F3:** se encargó a cuatro agentes de solo lectura la verificación del contexto contra el código (roles y stack, flujos, facturación, estado); las afirmaciones que cambian reglas se comprobaron además a mano.
- **F4:** el README del backend, además de .NET 10 y el enlace, perdió la mención a DotNetEnv (ya no se usa) y cerró un bloque de código sin cerrar.

## 6. Fuera de alcance

- Publicar el hub en un remoto (GitHub). Recomendado después, para que las sesiones en la nube lo puedan clonar.
- Reorganizar el repo `bodegas-legacy` o unir sus dos análisis.
- Limpiar `deploy.zip`, `publish/`, `.idea`, `.DS_Store` o los logs de `video-tutoriales-trabajo`.
- Reescribir el contenido de QA, planes o informes más allá de las rutas.
