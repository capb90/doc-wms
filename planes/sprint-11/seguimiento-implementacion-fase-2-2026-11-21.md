# Seguimiento — Implementación de la fase 2

> **Para qué sirve:** la matriz de la implementación de la fase 2 (`DEC-080`, `DEC-081`): en qué orden se ejecuta cada paso, dónde están su plan y sus prompts, y en qué estado va cada parte.
> **Fecha de corte:** 2026-11-24. Backend `fase-2` `019fa81` y frontend `fase-2` `5793bc9`, con F01 y F02 integradas (I-01) y los ajustes de la QA manual de F01 y F02; `develop` sigue en BE `529bda7` y FE `3aa6e3c`. Plan cerrado de F03 aprobado el 2026-11-24, con sus tres prompts; sus partes 1 y 2 están por lanzar.
> **Carpetas:** la raíz de `planes/sprint-11/` guarda el plan maestro, esta matriz y el plan de P0. Cada feature tiene su carpeta `fNN-<tema>/` con su plan cerrado y todos sus prompts, que se quedan ahí aunque ya se hayan ejecutado (plan maestro §5.5).
> **Fuente del orden:** [plan maestro](plan-maestro-implementacion-fase-2-2026-11-20.md), §4 (orden y paralelismo), §5.3 (ramas y fusiones) y §9 (plantilla del plan cerrado).
> **Mantenimiento:** §5 de este documento.

---

## 1. Estados

| Columna | Valores |
| --- | --- |
| Plan | Por escribir · Propuesto · Aprobado · Ejecutado |
| Parte 0 a 3 | — (no la lleva) · Pendiente · En curso · Hecha (commit) · Bloqueada |
| Integración | Pendiente · En curso · Fusionada en `fase-2` |
| Despliegue final | Pendiente · En pruebas del usuario · En `develop` · En staging |

---

## 2. Matriz de ejecución

### 2.1 Orden, ramas, planes y prompts

Los pasos con el mismo número corren a la vez, uno en cada repo (M10). Un paso arranca cuando su repo está libre y su plan está aprobado; los planes se escriben en `docs` mientras corre el paso anterior.

| # | ID | Paso | Repo y rama | Corre a la vez con | Depende de | Plan | Prompts | Estado del plan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | MAESTRO | Plan maestro de la fase 2 | docs `main` | — | `DEC-080` | [plan-maestro-implementacion-fase-2-2026-11-20.md](plan-maestro-implementacion-fase-2-2026-11-20.md) | [prompt-plan-maestro-implementacion-fase-2-2026-11-20.md](../../archivo/prompts/sprint-11/prompt-plan-maestro-implementacion-fase-2-2026-11-20.md) (archivado) | Aprobado el 2026-11-20 (docs `40acd3d`) |
| 1 | P0 | Correos al rol: código y pruebas (fase 1 de su plan) | BE `p0/correos-por-rol`, desde `develop` | Planes de F01 y F02; maquetación de F02 cuando su plan esté aprobado | — | [plan-cerrado-correos-notificacion-por-rol-2026-11-05.md](plan-cerrado-correos-notificacion-por-rol-2026-11-05.md) | Fase 1: [prompt-correos-notificacion-por-rol-2026-11-05.md](prompt-correos-notificacion-por-rol-2026-11-05.md) | Aprobado el 2026-11-05 |
| 2 | P0 | Correos al rol: QA del usuario, fusión en `develop` y staging (fase 2 de su plan) | BE `develop` y staging | Maquetación de F02 | Paso 1 | El mismo | Fase 2: se pide aparte, con el «sí» del usuario en cada acción | Fusión hecha (`529bda7`); staging aplazado por el usuario el 2026-11-21 (los operarios no usan la app): va con el próximo despliegue de `develop` |
| 3 | RAMAS | Crear `fase-2` en BE y FE | BE y FE, desde `develop` | — | P0 en `develop`; commit de los `AGENTS.md` | Plan maestro §5.3 | — | Hecho el 2026-11-21, con push: BE `fase-2` en `529bda7`, FE `fase-2` en `3aa6e3c` |
| 4 | F01 | Núcleo de dominio (partes 0 y 1) | BE `f2/f01-nucleo` | F02 | Paso 3 | [plan-cerrado-f2-f01-nucleo-2026-11-21.md](f01-nucleo/plan-cerrado-f2-f01-nucleo-2026-11-21.md) | Planificador (F01 y F02): [prompt-f2-f01-nucleo-planificador-2026-11-21.md](f01-nucleo/prompt-f2-f01-nucleo-planificador-2026-11-21.md) (ejecutado). Backend: [prompt-f2-f01-nucleo-backend-2026-11-21.md](f01-nucleo/prompt-f2-f01-nucleo-backend-2026-11-21.md) (ejecutado). Reanudar fase 1: [prompt-f2-f01-nucleo-backend-fase1-reanudar-2026-11-23.md](f01-nucleo/prompt-f2-f01-nucleo-backend-fase1-reanudar-2026-11-23.md) (ejecutado) | Aprobado el 2026-11-21 |
| 4 | F02 | Base transversal (parte 2) | FE `f2/f02-base` | F01 (y P0, si aún corre) | Paso 3 en FE | [plan-cerrado-f2-f02-base-2026-11-21.md](f02-base/plan-cerrado-f2-f02-base-2026-11-21.md) | Maquetación: [prompt-f2-f02-base-maquetacion-2026-11-21.md](f02-base/prompt-f2-f02-base-maquetacion-2026-11-21.md) (ejecutado). Reanudar fase 2: [prompt-f2-f02-base-maquetacion-fase2-reanudar-2026-11-23.md](f02-base/prompt-f2-f02-base-maquetacion-fase2-reanudar-2026-11-23.md) (ejecutado) | Aprobado el 2026-11-21 |
| 5 | I-01 | Integración de F01 y F02 (parte 3) | BE `f2/f01-nucleo` y FE `f2/f02-base` | — | F01 y F02 | Los de F01 (§13) y F02 | Integración: [prompt-f2-f01-nucleo-integracion-2026-11-21.md](f01-nucleo/prompt-f2-f01-nucleo-integracion-2026-11-21.md) (ejecutado) | Aprobado el 2026-11-21, con los de F01 y F02 |
| 6 | F03 | Báscula | BE y FE `f2/f03-bascula` | Back y front de F03 | I-01 | [plan-cerrado-f2-f03-bascula-2026-11-24.md](f03-bascula/plan-cerrado-f2-f03-bascula-2026-11-24.md) | Planificador: [prompt-f2-f03-bascula-planificador-2026-11-24.md](f03-bascula/prompt-f2-f03-bascula-planificador-2026-11-24.md) (ejecutado). Backend: [prompt-f2-f03-bascula-backend-2026-11-24.md](f03-bascula/prompt-f2-f03-bascula-backend-2026-11-24.md). Maquetación: [prompt-f2-f03-bascula-maquetacion-2026-11-24.md](f03-bascula/prompt-f2-f03-bascula-maquetacion-2026-11-24.md). Integración (I-03): [prompt-f2-f03-bascula-integracion-2026-11-24.md](f03-bascula/prompt-f2-f03-bascula-integracion-2026-11-24.md) | Aprobado el 2026-11-24 |
| 7 | F04 | Bodega | BE y FE `f2/f04-bodega` | Back y front de F04 | I-03 | `f04-bodega/plan-cerrado-f2-f04-bodega-AAAA-MM-DD.md` | `f04-bodega/`, igual | Por escribir |
| 8 | F05 | Comercio Exterior | BE y FE `f2/f05-comercio-exterior` | Back y front de F05 | I-04 | `f05-comercio-exterior/plan-cerrado-f2-f05-comercio-exterior-AAAA-MM-DD.md` | `f05-comercio-exterior/`, igual | Por escribir |
| 9 | F06 | Salidas de mercancía | BE y FE `f2/f06-salidas` | Back y front de F06 | I-05 | `f06-salidas/plan-cerrado-f2-f06-salidas-AAAA-MM-DD.md` | `f06-salidas/`, igual | Por escribir |
| 10 | F07 | Tarifas y acuerdos | BE y FE `f2/f07-tarifas-acuerdos` | — | I-06 | `f07-tarifas-acuerdos/plan-cerrado-f2-f07-tarifas-acuerdos-AAAA-MM-DD.md` | `f07-tarifas-acuerdos/`, igual que F03 | Por escribir |
| 11 | F08 | Operación de facturas | BE y FE `f2/f08-operacion-facturas` | — | I-07 | `f08-operacion-facturas/plan-cerrado-f2-f08-operacion-facturas-AAAA-MM-DD.md` | `f08-operacion-facturas/`, igual que F03 | Por escribir |
| 12 | F09 | Notificaciones configurables | BE y FE `f2/f09-notificaciones` | — | P0 e I-08 | `f09-notificaciones/plan-cerrado-f2-f09-notificaciones-AAAA-MM-DD.md` | `f09-notificaciones/`, igual que F03 | Por escribir |
| 13 | DF | Despliegue final (M25): pruebas del usuario en local sobre `fase-2`, fusión en `develop`, staging recreado y cargado desde el legacy, fase 2 de P0, PRF-002 y apertura a los operarios | `fase-2` → `develop` → staging | — | I-01 a I-09 en `fase-2` | `despliegue-final/plan-cerrado-despliegue-final-fase-2-AAAA-MM-DD.md`, por escribir mientras corre F09 (plan maestro §7.3) | `despliegue-final/`, por escribir | Por escribir |

Un plan o un prompt que aún no existe aparece con su ruta esperada, relativa a esta carpeta y entre comillas invertidas; al escribirlo se reemplaza por el enlace. Los prompts se llaman `prompt-f2-fNN-<tema>-<planificador|backend|maquetacion|integracion>-AAAA-MM-DD.md` y el §11 de cada plan cerrado los enlaza.

### 2.2 Estado de la implementación

| ID | 0 · Contrato | 1 · Backend | 2 · Maquetación | 3 · Integración | Commits (BE / FE) | Despliegue | Estado |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P0 | — | Hecho el 2026-11-21; QA del usuario y fusión en `develop` (`529bda7`) | — | — (su fase 2 es la de staging: Pendiente) | `1b2f09f`, fusión `529bda7` / — | DF | Fase 1 en `develop`; staging aplazado |
| F01 | Pendiente (con el plan) | Hecho: fases 1 a 6 cerradas (1 a 4 el 2026-11-23, 5 y 6 el 2026-11-24). Fase 1 hecha el 2026-11-23 (`b089eef`): QA2-F01-001 a 019 en PASA; `Wms.Tests` 2098 → 2150, `Wms.IntegrationTests` 479 → 653 (los 2 fallos heredados). Fase 2 hecha el 2026-11-23 (`9bb205b`): QA2-F01-020 y 021 en PASA; `Wms.Tests` 2150 → 2137, `Wms.IntegrationTests` 653 → 672 (los 2 fallos heredados); agrupaciones por embalaje (plan §2.2.6). Fase 3 hecha el 2026-11-23 (`5a44a71`): QA2-F01-022 a 031 en PASA; `Wms.Tests` 2137 → 2120, `Wms.IntegrationTests` 672 → 661 (los 2 fallos heredados); migración `EntryPerDocument`; el ciclo de báscula nace en el cobro (`weighbridgeCycleId` nulo al registrar; plan §8). Fase 4 hecha el 2026-11-23 (`4f4a78b`): QA2-F01-032 a 035 en PASA; `Wms.Tests` 2120 → 2133, `Wms.IntegrationTests` 661 → 670 (los 2 fallos heredados); sin migración; cambio de documento, unidades de carga y precisiones del contrato para I-01 en la nota de la fase 4 del plan §8. Fase 5 hecha el 2026-11-24 (`202a42d`): QA2-F01-036 a 050 en PASA; `Wms.Tests` 2133 → 2030, `Wms.IntegrationTests` 670 → 673 (los 2 fallos heredados); migración `ReplaceLoadingOrderWithGoodsExit`; la orden de cargue y sus 27 endpoints salen; decisiones aplicadas y el mensaje de salidas bloqueadas pendiente para I-01 en la nota de la fase 5 del plan §8. Fase 6 hecha el 2026-11-24 (`f567f40`): QA2-F01-051 a 054 en PASA; `Wms.Tests` 2030 → 2037, `Wms.IntegrationTests` 673 → 678 (los 2 fallos heredados); sin migración; tasa semanal al facturar con respaldo y aviso, recálculo de las facturas en Borrador al registrar una tasa, peso de mercancía en la fórmula por peso; servicio de la DIAN y C-F01-140 retirados; importación completa de ensayo con conteos iguales (nota de la fase 6 del plan §8) | — | Fusionada en `fase-2` el 2026-11-24 (I-01, BE `019fa81`): QA2-F01-055 a 065 en PASA en el navegador; contrato corregido al backend en C-F01-27, 61, 63, 64, 65, 90, 93 y 98 (plan de F01 §8, nota de I-01); `Wms.Tests` 2037 y `Wms.IntegrationTests` 678 sin cambios (los 2 fallos heredados) | `b089eef`, `9bb205b`, `5a44a71`, `4f4a78b`, `202a42d`, `f567f40`, fusión `019fa81` / — | DF | Integrada en `fase-2` |
| F02 | En el plan de F01 | — | Hecha el 2026-11-23: fases 1 a 5 (`d389685`, `813443f`, `4e60427`, `9e738bc`, `35f1746`); fase 5: QA2-F02-024 y 025 en PASA, `yarn test` 711 → 722, lint 262 → 258 errores; parte: `yarn test` 608 → 722, lint 276 → 258 errores, QA2-F02-001 a 026 contra los simulados | Fusionada en `fase-2` el 2026-11-24 (I-01, FE `50dd86f`, fusión `042c4ce`): QA2-F02-001 a 026 en PASA en el navegador contra el backend local; `yarn test` 722 → 679, lint 258 → 255 errores | — / `d389685`, `813443f`, `4e60427`, `9e738bc`, `35f1746`, `50dd86f`, fusión `042c4ce` | DF | Integrada en `fase-2` |
| F03 | En el plan (§2), aprobado el 2026-11-24 | En curso: fase BE-1 hecha el 2026-11-24 (`ccfa53d`): QA2-F03-001 a 016 en PASA; `Wms.Tests` 2037 → 2072, `Wms.IntegrationTests` 678 → 709 (los 2 fallos heredados); migración `WeighingAtRegistration`; notas para I-03 en el plan §8.1. Faltan BE-2 y BE-3 | Pendiente | Pendiente | `ccfa53d` / — | DF | Parte 1 en curso (BE-1 hecha) |
| F04 | Pendiente | Pendiente | Pendiente | Pendiente | — | DF | Pendiente |
| F05 | Pendiente | Pendiente | Pendiente | Pendiente | — | DF | Pendiente |
| F06 | Pendiente | Pendiente | Pendiente | Pendiente | — | DF | Pendiente |
| F07 | Pendiente | Pendiente | Pendiente | Pendiente | — | DF | Pendiente |
| F08 | Pendiente | Pendiente | Pendiente | Pendiente | — | DF | Pendiente |
| F09 | Pendiente | Pendiente | Pendiente | Pendiente | — | DF | Pendiente |

### 2.3 Despliegue final (M25)

| Paso | Contenido | Para cerrarlo | QA del usuario | `fase-2` → `develop` | Staging | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| DF | F01 a F09 | I-01 a I-09 fusionadas en `fase-2` | Pendiente (el usuario puede probar en local cada integración al cerrarse) | Pendiente | Pendiente: recreado y cargado desde el legacy con el «sí» del usuario, datos de arranque, fase 2 de P0, PRF-002 y apertura a los operarios (plan maestro §7.3) | Pendiente |

---

## 3. Pendientes sueltos

| Pendiente | Lo necesita | Estado |
| --- | --- | --- |
| Commit del `AGENTS.md` de `Backend/wms-api` y de `Frontend/wms` (anexo A del plan maestro) | Paso 3 (las ramas salen de `develop`) | Hecho el 2026-11-21: BE `42738e1` y FE `3aa6e3c` en `develop`, publicados |
| Mover el prompt del plan maestro a `archivo/prompts/` | Orden del hub (`README.md`, «Archivos nuevos») | Hecho el 2026-11-21: `archivo/prompts/sprint-11/` |
| Prompt del planificador para los planes cerrados de F01 y F02, en `f01-nucleo/` | Paso 4 | Hecho el 2026-11-21: [prompt-f2-f01-nucleo-planificador-2026-11-21.md](f01-nucleo/prompt-f2-f01-nucleo-planificador-2026-11-21.md) ejecutado; los dos planes y sus tres prompts, aprobados el 2026-11-21 |
| Ajustes de la QA manual de F01 y F02: [plan](f02-base/plan-cerrado-f2-f02-ajustes-qa-2026-11-24.md), aprobado el 2026-11-24; FE `f2/f02-ajustes-qa` | Antes de seguir con F03 sobre `fase-2` | Hecho el 2026-11-24: fases 1 a 3 (FE `5b31280`, `6abd68b`, `877f26b`), fusión en `fase-2` `5793bc9` |
| Prompt del planificador del plan cerrado de F03, en `f03-bascula/` | Paso 6 | Hecho el 2026-11-24: con [prompt-f2-f03-bascula-planificador-2026-11-24.md](f03-bascula/prompt-f2-f03-bascula-planificador-2026-11-24.md) se escribieron el plan cerrado y sus tres prompts, aprobados el 2026-11-24; el prompt, ejecutado |

---

## 4. Datos del cliente

Ninguno bloquea la construcción; los cuatro primeros se configuran en la aplicación.

| Dato | Lo usa | Hace falta antes de | Estado |
| --- | --- | --- | --- |
| Umbrales amarillo y rojo de recepción, cargue y salida de patio (AF-57) | F04 | El despliegue final | Pendiente del cliente |
| Prefijos de N.º de levante, N.º de aceptación y manifiesto DIAN (AF-79) | F01 y F05 | El despliegue final | Pendiente del cliente |
| Tasa de la semana de arranque (AF-86) | F01 y F05 | El despliegue final | Pendiente del cliente |
| Tramos de peso: límite y si la segunda tarifa va a todo el peso o al exceso (AF-116) | F07 | La aprobación del plan cerrado de F07 (riesgo R7 del plan maestro) | Pendiente del cliente |
| Mínimo de la parte porcentual en un depósito mixto (AF-120) | F07 | Igual | Pendiente del cliente |
| Revisión de la carga inicial de acuerdos (58 textos de tarifa de la hoja 2026, AF-114) | F07 | El despliegue final | Pendiente de Facturación |

---

## 5. Mantenimiento

- **Quién lo actualiza:**
  - el planificador, al escribir o aprobar un plan: columnas «Plan» y «Prompts» de §2.1, con los enlaces a la carpeta de la feature;
  - el agente de cada parte, al cerrarla: su celda de §2.2 y los commits, en el mismo commit de docs de su fase;
  - el agente de integración, al fusionar en `fase-2`: la columna «3 · Integración»;
  - el agente que cierra la implementación: §2.3.
- **Al cambiar algo:** se actualiza la fecha de corte y los commits del encabezado.
- **Al terminar una parte:** su prompt se queda en la carpeta de la feature, con «**Ejecutado** el AAAA-MM-DD; ya no es una instrucción» en su encabezado, y aquí se marca «(ejecutado)» junto a su enlace. No se mueve a `archivo/`.
- **Si el orden cambia:** manda el plan maestro (§4); primero se cambia allí y después aquí.
