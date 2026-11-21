# Seguimiento — Implementación de la fase 2

> **Para qué sirve:** la matriz de la implementación de la fase 2 (`DEC-080`, `DEC-081`): en qué orden se ejecuta cada paso, dónde están su plan y sus prompts, y en qué estado va cada parte.
> **Fecha de corte:** 2026-11-21. Backend `develop` `42738e1` y frontend `develop` `3aa6e3c`, con la regla de ramas de `DEC-081` en su `AGENTS.md`; docs `main` `e39db3a`, reorganizado en `planes/sprint-11/` el 2026-11-21. Todavía no existen las ramas `fase-2`.
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
| Grupo | Pendiente · En QA del usuario · En `develop` · En staging |

---

## 2. Matriz de ejecución

### 2.1 Orden, ramas, planes y prompts

Los pasos con el mismo número corren a la vez, uno en cada repo (M10). Un paso arranca cuando su repo está libre y su plan está aprobado; los planes se escriben en `docs` mientras corre el paso anterior.

| # | ID | Paso | Repo y rama | Corre a la vez con | Depende de | Plan | Prompts | Estado del plan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | MAESTRO | Plan maestro de la fase 2 | docs `main` | — | `DEC-080` | [plan-maestro-implementacion-fase-2-2026-11-20.md](plan-maestro-implementacion-fase-2-2026-11-20.md) | [prompt-plan-maestro-implementacion-fase-2-2026-11-20.md](../../archivo/prompts/sprint-11/prompt-plan-maestro-implementacion-fase-2-2026-11-20.md) (archivado) | Aprobado el 2026-11-20 (docs `40acd3d`) |
| 1 | P0 | Correos al rol: código y pruebas (fase 1 de su plan) | BE `p0/correos-por-rol`, desde `develop` | Planes de F01 y F02; maquetación de F02 cuando su plan esté aprobado | — | [plan-cerrado-correos-notificacion-por-rol-2026-11-05.md](plan-cerrado-correos-notificacion-por-rol-2026-11-05.md) | Fase 1: [prompt-correos-notificacion-por-rol-2026-11-05.md](prompt-correos-notificacion-por-rol-2026-11-05.md) | Aprobado el 2026-11-05 |
| 2 | P0 | Correos al rol: QA del usuario, fusión en `develop` y staging (fase 2 de su plan) | BE `develop` y staging | Maquetación de F02 | Paso 1 | El mismo | Fase 2: se pide aparte, con el «sí» del usuario en cada acción | Aprobado |
| 3 | RAMAS | Crear `fase-2` en BE y FE | BE y FE, desde `develop` | — | P0 en `develop`; commit de los `AGENTS.md` | Plan maestro §5.3 | — | — |
| 4 | F01 | Núcleo de dominio (partes 0 y 1) | BE `f2/f01-nucleo` | F02 | Paso 3 | `f01-nucleo/plan-cerrado-f2-f01-nucleo-AAAA-MM-DD.md`, por escribir junto con F02 | `f01-nucleo/`: planificador (F01 y F02) y backend, por escribir | Por escribir |
| 4 | F02 | Base transversal (parte 2) | FE `f2/f02-base` | F01 (y P0, si aún corre) | Paso 3 en FE | `f02-base/plan-cerrado-f2-f02-base-AAAA-MM-DD.md`, por escribir junto con F01 | `f02-base/`: maquetación, por escribir | Por escribir |
| 5 | I-01 | Integración de F01 y F02 (parte 3) | BE `f2/f01-nucleo` y FE `f2/f02-base` | — | F01 y F02 | Los de F01 y F02 | `f01-nucleo/`: integración, por escribir | — |
| 6 | F03 | Báscula | BE y FE `f2/f03-bascula` | Back y front de F03 | I-01 | `f03-bascula/plan-cerrado-f2-f03-bascula-AAAA-MM-DD.md` | `f03-bascula/`: planificador, backend, maquetación e integración, por escribir | Por escribir |
| 7 | F04 | Bodega | BE y FE `f2/f04-bodega` | Back y front de F04 | I-03 | `f04-bodega/plan-cerrado-f2-f04-bodega-AAAA-MM-DD.md` | `f04-bodega/`, igual | Por escribir |
| 8 | F05 | Comercio Exterior | BE y FE `f2/f05-comercio-exterior` | Back y front de F05 | I-04 | `f05-comercio-exterior/plan-cerrado-f2-f05-comercio-exterior-AAAA-MM-DD.md` | `f05-comercio-exterior/`, igual | Por escribir |
| 9 | F06 | Salidas de mercancía | BE y FE `f2/f06-salidas` | Back y front de F06 | I-05 | `f06-salidas/plan-cerrado-f2-f06-salidas-AAAA-MM-DD.md` | `f06-salidas/`, igual | Por escribir |
| 10 | G1 | QA del usuario sobre `fase-2`, fusión en `develop` y despliegue de G1 (staging recreado y cargado desde el legacy, PRF-002) | `fase-2` → `develop` → staging | Back y front de F07 | I-06 | `g1-despliegue/plan-cerrado-despliegue-g1-fase-2-AAAA-MM-DD.md`, por escribir mientras corre F06 (plan maestro §7.3) | `g1-despliegue/`, por escribir | Por escribir |
| 10 | F07 | Tarifas y acuerdos | BE y FE `f2/f07-tarifas-acuerdos` | G1 | I-06 | `f07-tarifas-acuerdos/plan-cerrado-f2-f07-tarifas-acuerdos-AAAA-MM-DD.md` | `f07-tarifas-acuerdos/`, igual que F03 | Por escribir |
| 11 | G2 | QA del usuario y despliegue de F07 | `fase-2` → `develop` → staging | Back y front de F08 | G1 e I-07 | En el plan de F07 | En el plan de F07 | — |
| 11 | F08 | Operación de facturas | BE y FE `f2/f08-operacion-facturas` | G2 | I-07 | `f08-operacion-facturas/plan-cerrado-f2-f08-operacion-facturas-AAAA-MM-DD.md` | `f08-operacion-facturas/`, igual que F03 | Por escribir |
| 12 | G3 | QA del usuario y despliegue de F08 | `fase-2` → `develop` → staging | Back y front de F09 | G2 e I-08 | En el plan de F08 | En el plan de F08 | — |
| 12 | F09 | Notificaciones configurables | BE y FE `f2/f09-notificaciones` | G3 | P0 e I-08 | `f09-notificaciones/plan-cerrado-f2-f09-notificaciones-AAAA-MM-DD.md` | `f09-notificaciones/`, igual que F03 | Por escribir |
| 13 | G4 | QA del usuario y despliegue de F09 | `fase-2` → `develop` → staging | — | G3 e I-09 | En el plan de F09 | En el plan de F09 | — |

Un plan o un prompt que aún no existe aparece con su ruta esperada, relativa a esta carpeta y entre comillas invertidas; al escribirlo se reemplaza por el enlace. Los prompts se llaman `prompt-f2-fNN-<tema>-<planificador|backend|maquetacion|integracion>-AAAA-MM-DD.md` y el §11 de cada plan cerrado los enlaza.

### 2.2 Estado de la implementación

| ID | 0 · Contrato | 1 · Backend | 2 · Maquetación | 3 · Integración | Commits (BE / FE) | Grupo | Estado |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P0 | — | Hecho el 2026-11-21; QA del usuario y fusión en `develop` (`529bda7`) | — | — (su fase 2 es la de staging: Pendiente) | `1b2f09f`, fusión `529bda7` / — | Antes de G1 | Fase 1 en `develop`; falta staging |
| F01 | Pendiente (con el plan) | Pendiente | — | Con I-01: Pendiente | — | G1 | Pendiente |
| F02 | En el plan de F01 | — | Pendiente | Con I-01: Pendiente | — | G1 | Pendiente |
| F03 | Pendiente | Pendiente | Pendiente | Pendiente | — | G1 | Pendiente |
| F04 | Pendiente | Pendiente | Pendiente | Pendiente | — | G1 | Pendiente |
| F05 | Pendiente | Pendiente | Pendiente | Pendiente | — | G1 | Pendiente |
| F06 | Pendiente | Pendiente | Pendiente | Pendiente | — | G1 | Pendiente |
| F07 | Pendiente | Pendiente | Pendiente | Pendiente | — | G2 | Pendiente |
| F08 | Pendiente | Pendiente | Pendiente | Pendiente | — | G3 | Pendiente |
| F09 | Pendiente | Pendiente | Pendiente | Pendiente | — | G4 | Pendiente |

### 2.3 Grupos y despliegues

| Grupo | Contenido | Para cerrarlo | QA del usuario | `fase-2` → `develop` | Staging | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | F01 a F06 | I-01, I-03, I-04, I-05 e I-06 fusionadas en `fase-2` | Pendiente | Pendiente | Pendiente: recreado y cargado desde el legacy con el «sí» del usuario, datos de arranque y PRF-002 (plan maestro §7.3) | Pendiente |
| G2 | F07 | I-07 fusionada y G1 en staging | Pendiente | Pendiente | Pendiente | Pendiente |
| G3 | F08 | I-08 fusionada y G2 en staging | Pendiente | Pendiente | Pendiente | Pendiente |
| G4 | F09 | I-09 fusionada y G3 en staging | Pendiente | Pendiente | Pendiente | Pendiente |

---

## 3. Pendientes sueltos

| Pendiente | Lo necesita | Estado |
| --- | --- | --- |
| Commit del `AGENTS.md` de `Backend/wms-api` y de `Frontend/wms` (anexo A del plan maestro) | Paso 3 (las ramas salen de `develop`) | Hecho el 2026-11-21: BE `42738e1` y FE `3aa6e3c` en `develop`, publicados |
| Mover el prompt del plan maestro a `archivo/prompts/` | Orden del hub (`README.md`, «Archivos nuevos») | Hecho el 2026-11-21: `archivo/prompts/sprint-11/` |
| Prompt del planificador para los planes cerrados de F01 y F02, en `f01-nucleo/` | Paso 4 | Por pedir |

---

## 4. Datos del cliente

Ninguno bloquea la construcción; los cuatro primeros se configuran en la aplicación.

| Dato | Lo usa | Hace falta antes de | Estado |
| --- | --- | --- | --- |
| Umbrales amarillo y rojo de recepción, cargue y salida de patio (AF-57) | F04 | El despliegue de G1 | Pendiente del cliente |
| Prefijos de N.º de levante, N.º de aceptación y manifiesto DIAN (AF-79) | F01 y F05 | El despliegue de G1 | Pendiente del cliente |
| Tasa de la semana de arranque (AF-86) | F01 y F05 | El despliegue de G1 | Pendiente del cliente |
| Tramos de peso: límite y si la segunda tarifa va a todo el peso o al exceso (AF-116) | F07 | La aprobación del plan cerrado de F07 (riesgo R7 del plan maestro) | Pendiente del cliente |
| Mínimo de la parte porcentual en un depósito mixto (AF-120) | F07 | Igual | Pendiente del cliente |
| Revisión de la carga inicial de acuerdos (58 textos de tarifa de la hoja 2026, AF-114) | F07 | El despliegue de G2 | Pendiente de Facturación |

---

## 5. Mantenimiento

- **Quién lo actualiza:**
  - el planificador, al escribir o aprobar un plan: columnas «Plan» y «Prompts» de §2.1, con los enlaces a la carpeta de la feature;
  - el agente de cada parte, al cerrarla: su celda de §2.2 y los commits, en el mismo commit de docs de su fase;
  - el agente de integración, al fusionar en `fase-2`: la columna «3 · Integración»;
  - el agente que cierra un grupo: §2.3.
- **Al cambiar algo:** se actualiza la fecha de corte y los commits del encabezado.
- **Al terminar una parte:** su prompt se queda en la carpeta de la feature, con «**Ejecutado** el AAAA-MM-DD; ya no es una instrucción» en su encabezado, y aquí se marca «(ejecutado)» junto a su enlace. No se mueve a `archivo/`.
- **Si el orden cambia:** manda el plan maestro (§4); primero se cambia allí y después aquí.
