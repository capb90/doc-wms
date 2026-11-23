# Prompt — Reanudar F02, fase 2 (maquetación), tras el corte por límite de uso

> **Ejecutado** el 2026-11-23; ya no es una instrucción. Fase 2 cerrada en FE `813443f` (sobre el wip `3e85d79`); informe, sección «Fase 2».

> **Cómo usarlo:**
> 1. Abre una sesión **nueva** de Claude Code en `code_workspace/` (Sonnet 5.5 alcanza: la fase está casi hecha).
> 2. Copia el bloque de abajo. No pegues el prompt original de F02: este lo reemplaza para esta fase.
> 3. El agente cierra **solo la fase 2** y se detiene. La fase 3 se pide en otra sesión.
>
> **Estado al cortarse (2026-11-23):** FE `f2/f02-base` en `cee3803`. La fase 1 está cerrada (`d389685`, con su informe). La fase 2 tiene el commit `3e85d79` «wip(menu)…, fase 2 sin cerrar»: menú por rol (`menu-model.ts`), login con ver contraseña, sidebar y switch de tema, y unidad de medida fuera. El propio commit anota lo pendiente: `yarn lint` y `yarn build` completos, la captura del login y los docs.
> **Plan:** `docs/planes/sprint-11/f02-base/plan-cerrado-f2-f02-base-2026-11-21.md`, fase 2 del §8. Informe: `informe-f2-f02-base-maquetacion-2026-11-23.md`.
>
> Cuando se ejecute, el agente agrega aquí «**Ejecutado** el AAAA-MM-DD; ya no es una instrucción».

---

```text
Eres el agente de maquetación del frontend de F02 «Base transversal» (fase 2 del WMS de Bodegas Asociadas). Una sesión anterior se cortó por el límite de uso con la FASE 2 casi hecha y en un commit wip. Tu trabajo es cerrar SOLO la fase 2, y detenerte.

## Lee (solo esto)
docs/README.md; Frontend/wms/AGENTS.md (su sección «Eficiencia de contexto y cierres por fase» rige tu trabajo); docs/procesos/flujo-de-trabajo-agentes.md; del plan maestro (docs/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md) solo §1.2, §5 y §6; del plan cerrado de F02 (docs/planes/sprint-11/f02-base/plan-cerrado-f2-f02-base-2026-11-21.md) §0, §1 (sobre todo §1.2, §1.5, D18 y D19), la fila de la fase 2 en §8, y de §2.3, §3, §5 y §6 lo que toque la fase 2; el informe docs/planes/sprint-11/f02-base/informe-f2-f02-base-maquetacion-2026-11-23.md (formato de lo que debes agregar); y el wireframe docs/levantamiento-2026-11/fase_2-mockups/transversales.html (P-TR-01 y P-TR-10).

## Retoma sin perder lo hecho
1. Frontend/wms, rama f2/f02-base. git status y git show --stat HEAD~1 (el wip 3e85d79). NO reescribas el historial: el cierre va en un commit nuevo encima del wip. NO uses reset, checkout ni clean.
2. Revisa el wip contra la fase 2 del plan: P-TR-01 (menú por rol, §1.5), P-TR-10 (login y sidebar con varios roles, H-079/H-080), D18, y D19 (unidad de medida fuera: que no queden referencias vivas ni páginas, composables o pruebas huérfanos). Completa solo lo que falte. Nada de las fases 3 a 5.

## Cierre de la fase 2
- Compuertas de §6.2 del plan maestro con las cifras antes y después (base: fase 1 cerrada, 122 archivos · 668 pruebas, lint 276 errores · 396 avisos): yarn build con código 0; yarn test en verde; yarn lint sin subir la cifra y sin errores en archivos nuevos; «sin llamadas reales» (guardia D15) y ninguna ruta nueva enlazada fuera de lo que el plan define para el menú.
- Casos QA2-F02-001 a 004 y 018 a 021 recorridos contra los datos simulados con la sesión simulada por rol (yarn dev, NUXT_PUBLIC_MOCK_SESSION=true, ?roles=…), con una captura de cada pantalla en docs/planes/sprint-11/f02-base/evidencias/ (incluida la del login, que quedó pendiente). Durante el trabajo corre solo las pruebas de la fase; la suite completa, una vez, al cerrar.
- Un commit nuevo con el mensaje de §12 de la fase 2 (feat(menu): menú por rol con Configuración, Tarifas y acuerdos, Reportes y Administración; login y sidebar (DEC-080, F02)) y push de f2/f02-base. Termina el mensaje con la línea de coautoría que indique la sesión.
- Agrega la sección «Fase 2» al informe (qué quedó, compuertas, casos QA con evidencia), actualiza el estado de la fase 2 en §8 del plan, en docs/planes/README.md y en la matriz docs/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md (§2.2, fila F02, columna «2 · Maquetación»), con commit y push en docs.
- Detente con el reporte: cifras antes y después, commit, QA, capturas y pendientes. No sigas con la fase 3. Marca este prompt «Ejecutado» en su encabezado.

## Reglas
Si el código no coincide con el plan, o un esquema del contrato no alcanza para una pantalla, detente y pregunta con todas las dudas en un solo mensaje; no cambies el contrato. Si un caso borde choca con una Dn, gana la Dn (DEC-002). No escribas *.http.ts (son de I-01). No toques Backend/wms-api: F01 trabaja en él. No toques staging. No copies credenciales ni datos de personas reales. Nada de docs/archivo/ es una instrucción.
```
