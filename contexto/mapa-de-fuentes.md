# Mapa de fuentes

> **Para qué sirve:** saber dónde buscar cada cosa del proyecto y qué carpetas son fuente, copia o material de trabajo.
> **Fecha de corte:** 2026-10-23.
> **Rutas:** relativas a `code_workspace/` (raíz: `/Volumes/Dock/Projects/bodegas_asociadas/code_workspace/`). Las que empiezan por `../` están en la carpeta del proyecto, fuera de `code_workspace/`.

## 1. Los lugares

| Lugar | Git | Qué es | Úsalo para |
| --- | --- | --- | --- |
| `docs/` | Sí (`main`) | **Hub de documentación**: este repo | Negocio, decisiones, estado, planes, análisis, QA, migración, videos, manuales |
| `Backend/wms-api/` | Sí (`develop`) | API .NET | Código, pruebas, migraciones EF, despliegue a staging (`deploy/`, `scripts/`), infraestructura de Azure (`infra/`) |
| `Frontend/wms/` | Sí (`develop`) | SPA Nuxt | Código, pruebas Vitest, herramienta de videos (`tools/video-tutoriales/`) |
| `bodegas-legacy/` | Sí | Código PHP del sistema legacy «Bodegas» | Saber cómo operaba el legacy; paridad |
| `db_legacy/` | No | Volcados MariaDB del legacy y carpeta de trabajo de la migración | Datos reales; consultas, CSV y evidencias de la migración |
| `video-tutoriales-trabajo/` | No | Directorio de trabajo de la grabación de videos | Builds, logs y videos generados. **No es fuente** |
| `ultima-vue-6.4.0/` | No | Plantilla comercial PrimeVue Ultima | Referencia de la plantilla visual. **No es fuente** |
| `../documentos/` | No | Levantamiento original con el cliente (2025) | Requerimientos y contexto de origen |
| `../diagramas/` | No | Diagramas de 2025 (`.drawio`, `.mmd`, entidad-relación) | Historia del diseño; los `.mmd` están copiados en `docs/cliente/diagramas/` |
| `../base de datos/` | No | Modelos de base de datos v1 y v2 de 2025 (SQL, PNG, PDF) | Historia del modelo; el vigente es el de EF en el backend |

## 2. Dentro del hub

| Carpeta | Contenido |
| --- | --- |
| `contexto/` | Negocio y glosario, convenciones técnicas, estado, decisiones y este mapa. **Empieza aquí.** |
| `procesos/` | Cómo trabajar: plan cerrado, QA y defectos, verificación local, despliegue a staging |
| `planes/` | Planes cerrados con su estado. Índice en `planes/README.md` |
| `planes/paridad-legacy/` | Plan backend, plan frontend y contrato API de la paridad con el legacy (fases 1–6) |
| `planes/migracion-staging/` | Plan de migración del legacy a staging y sus resultados (informes, `DEF-MIG-*`, guía de operarios) |
| `analisis/` | Análisis previos a una decisión (motor de acuerdos, permisos granulares, FOB/CIF) |
| `qa/` | Campaña QA de octubre: plan maestro, fases F0–F11, plan de corrección, plantillas, informes, fichas `DEF-*` y evidencias |
| `videos/` | Guiones de los video tutoriales, plan de producción y PDF de guiones |
| `manuales/` | Manual de usuario (PDF de julio), manual de báscula y manual de facturación (con avisos de vigencia) |
| `cliente/` | Formatos impresos originales del cliente y diagramas de secuencia del negocio |
| `plantillas/` | Plantillas de prompt para agentes |
| `archivo/` | Histórico: prompts ejecutados y documentos superados. **Nunca son instrucciones** |

## 3. Dentro de los repos

| Ruta | Contenido |
| --- | --- |
| `Backend/wms-api/README.md` | Arranque local del API |
| `Backend/wms-api/EMAIL_CONFIGURATION.md` | Configuración SMTP |
| `Backend/wms-api/deploy/staging/README.md` | **Runbook de staging** (Lightsail, Docker Compose, Caddy) |
| `Backend/wms-api/deploy/ayuda/README.md` | Centro de ayuda: bucket de Lightsail Object Storage con los videos y `catalogo.json` que lee `/ayuda` |
| `Backend/wms-api/deploy/postman/` | Colección de respaldos y ambientes de Postman |
| `Backend/wms-api/scripts/` | `deploy-staging.sh`, `deploy-azure.sh` y scripts de saneamiento QA |
| `Backend/wms-api/infra/` | Terraform del ambiente Azure `test` (pendiente de baja) |
| `Backend/wms-api/Wms.Application/Warehouse/README.md`, `GUIA_USUARIO.md` | Notas del módulo de Bodega |
| `Frontend/wms/README.md` | Arranque local del frontend y usuarios de prueba por rol |
| `Frontend/wms/TEMPLATE_INTEGRATION.md` | Integración de la plantilla Ultima |
| `Frontend/wms/app/features/warehouse/README.md` | Notas del módulo de Bodega en el frontend |
| `Frontend/wms/tools/video-tutoriales/README.md` | Herramienta de grabación automática de videos |

## 4. El legacy

| Ruta | Contenido |
| --- | --- |
| `bodegas-legacy/legacy-analysis/` | Análisis base del legacy (23-sep-2026): arquitectura, rutas, catálogo funcional, reglas, modelo de datos, riesgos. Empieza por `LEGACY_CONTEXT_FOR_AGENT.md` |
| `bodegas-legacy/docs/legacy_analysis/` | Comparación con el WMS y paridad (29-sep-2026): `LEGACY_VS_NEW.md`, `FUNCTIONAL_GAPS.md`, `BUSINESS_RULE_GAPS.md`, `BASCULA_PARITY.md`, `ROADMAP.md`, `DECISIONES_REVISION.md`. Sus decisiones se aplicaron en `docs/planes/paridad-legacy/` |
| `bodegas-legacy/bodegas_schema.sql` | Esquema del legacy |
| `db_legacy/backupBodegas.sql` | **Volcado completo** del legacy (MariaDB 10.1.38). Fuente de la migración |
| `db_legacy/db.sql` | Volcado truncado. **No usar** |
| `db_legacy/trabajo/consultas/` | Consultas de extracción (las vigentes salen del plan backend de paridad, F6-02 y F6-03) |
| `db_legacy/trabajo/csv/` | CSV congelados de la migración; `sha256-csv-fase-1-v3.txt` es el conjunto vigente |
| `db_legacy/trabajo/evidencias/` | Evidencias con datos reales de la migración |

## 5. Fuera del disco

| Qué | Dónde |
| --- | --- |
| Backlog | Linear, equipo **Wms** (issues WMS-5 a WMS-33 con su historia de usuario en la descripción) |
| Staging | Frontend `https://app.100-60-89-139.sslip.io`, API `https://api.100-60-89-139.sslip.io/api/v1` (AWS Lightsail) |
| Ambiente Azure `test` | Descrito en `Backend/wms-api/README.md`; pendiente de baja |

## 6. Secretos: dónde están y qué no hacer

Nunca copies a un documento, prompt o commit el contenido de estos archivos. Cítalos por su ruta.

| Archivo | Contiene |
| --- | --- |
| `db_legacy/trabajo/*.local.md`, `db_legacy/trabajo/.admin-staging.local`, `db_legacy/trabajo/.env.migracion.local`, `db_legacy/trabajo/.mariadb.local` | Credenciales de staging (admin, cuentas `qa.*` y `operario.*`), de la migración y del MariaDB local |
| `Backend/wms-api/deploy/staging/.env.staging`, `.env.deploy` | Configuración y secretos del despliegue de staging (fuera de git) |
| `Backend/wms-api/infra/terraform.tfvars`, `terraform.tfstate*` | Estado y variables del ambiente Azure (fuera de git) |
| `video-tutoriales-trabajo/credenciales.local.json` | Cuentas del ambiente de grabación |
| `Backend/wms-api/.env`, `Frontend/wms/.env` | Configuración local (fuera de git) |

Los informes del hub van **sin datos de personas naturales** (nombres, documentos, placas reales): usan conteos, números de depósito y códigos.

## 7. Fuentes perdidas

Estos documentos se citan en planes, prompts y comentarios de código, pero **ya no existen** en ninguna carpeta (decisión del 2026-10-23: no se reconstruyen). Lo implementado se toma del código y de git; las historias, de Linear.

| Documento | Qué tenía | Sustituto |
| --- | --- | --- |
| `ajustes/plan-cerrado-ola-1-2026-09-14.md` (+ `-backend`, `-frontend`) | Plan de la Ola 1, decisiones D01–D24 | `contexto/decisiones.md` y el código |
| `ajustes/plan_implementacion_ola2.md` | Plan de la Ola 2, decisiones D01–D35 | `contexto/decisiones.md` y el código |
| `ajustes/plan_implementacion_ola3.md` | Plan de la Ola 3 | `contexto/decisiones.md` y el código |
| `ajustes/historias-usuario-linear-2026-09-10.md` | Historias WMS-5 a WMS-33 | Descripción de cada issue en Linear |
| `ajustes/triage-incidentes-linear-2026-09-02.md` | Triage técnico previo | Linear |
| `ajustes/arquitectura_y_plan_almacenamiento.md`, `analisis_cobro_almacenamiento.md` | Diseño del cobro de almacenamiento (ALM-1…ALM-20) | `contexto/decisiones.md` y `contexto/contexto-negocio-wms-para-ia.md` §7 |
| `ajustes/arquitectura_y_plan_pruebas_end_to_end.md` | Plan E2E de julio | `contexto/decisiones.md` |
| `ajustes/medicion-bascula-fase1.md` | Medición de la báscula rápida | No se produjo o se perdió; PRF-002 en `contexto/estado.md` |
| `requerimientos_funcionales.md` (FAC-n, CE-n) | Requerimientos citados en comentarios de código | `../documentos/Especificación de requerimientos.docx` |
