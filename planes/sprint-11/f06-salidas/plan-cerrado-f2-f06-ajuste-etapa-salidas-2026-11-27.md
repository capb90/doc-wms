# Plan cerrado — Fase 2 · F06 Salidas de mercancía · Ajuste de la etapa Salidas en el stepper

> **Fecha:** 27 de noviembre de 2026. **Estado:** Ejecutado el 2026-11-27. Aprobado por el usuario el 2026-11-27 («Apruebo, ejecútalo»); fase A-1 hecha (FE `9df8af7`). Las decisiones del usuario del 2026-11-27 están en A1 a A4.
> **Origen:** la nota de cierre de FE-2 de F06 (`P06/` §8.4): el stepper del detalle del depósito y la etiqueta de la tarjeta de la etapa Salidas siguen fijos por F05 («Con la próxima actualización», sin color y fuera del progreso), aunque D22 de F06 dice que la pantalla «pinta lo que llega». El backend ya marca la etapa (BE-1, `DepositStageRules.cs:108-112`, C-F06-10); el frontend la ignora.
> **Base:** FE `f2/f06-salidas` `a2cac51` (FE-2 cerrada) · docs `main` `5bed929`.
> **Alcance:** solo frontend, en `f2/f06-salidas`. Sin contrato nuevo, sin backend, sin migración.
> **Rutas:** relativas a `code_workspace/`. Prefijos: `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`; `P06/` = `D/planes/sprint-11/f06-salidas/plan-cerrado-f2-f06-salidas-2026-11-26.md`; `PM/` = `D/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md`.

---

## 0. Instrucciones para el ejecutor

1. Lee este plan completo, `P06/` §1.4 (D21, D22) y §1.1 (D5), y `F/features/foreign-trade/utils/deposit-stages.ts`. Confirma con grep las líneas citadas; si no coinciden, detente y pregunta.
2. Trabaja en `Frontend/wms`, rama `f2/f06-salidas` (retómala; `git fetch` y, si `develop` o `fase-2` avanzaron, tráelos como dice `PM/` §5.3). No toques `Backend/wms-api`.
3. Una sola fase (§4). Al cerrarla: compuertas de §5, commit con el mensaje de §6 y push de la rama, el estado aquí, en `P06/` §8.4 y en la matriz, y el reporte. No sigas con FE-3.
4. Sin llamadas reales al API, sin menú, con la sesión simulada.

---

## 1. Decisiones

### 1.1 Respuestas del usuario (2026-11-27)

| # | Decisión | Fuente |
| --- | --- | --- |
| A1 | **Tono:** con `Exits` en `pendingStages`, el paso «Salidas» del stepper y la etiqueta de la tarjeta de la etapa van en **amarillo** (`warn`), como las demás etapas pendientes. Sin nivel de reloj (el reloj sigue siendo solo de Bodega, D22) | Usuario: «Amarillo (Recomendada)»; `P06/` D22 |
| A2 | **Texto:** pendiente, «**Salida por completar**»; sin pendiente, «Al día», como las demás | Usuario: «Salida por completar (Recomendada)» |
| A3 | **Progreso:** Salidas **cuenta** en el progreso del encabezado del depósito («{n} de {total} al día»): en importación el total pasa de 5 a 6, en exportación e inspección de 3 a 4 | Usuario: «Sí, cuenta (Recomendada)» |
| A4 | **Cuándo:** ahora, como ajuste de la maquetación en `f2/f06-salidas`, antes de I-06. El color se ve en el detalle real cuando I-06 fusione el backend de F06 (hoy `fase-2` no manda `Exits`) | Usuario: «Ahora, en f2/f06-salidas (Recomendada)» |

### 1.2 Cómo se aplica (sin preguntar, por `P06/` D5 y D22)

| # | Decisión | Fuente |
| --- | --- | --- |
| A5 | **Cerrado y Anulado:** en un depósito Cerrado, Salidas se marca si el backend la manda en `pendingStages` (D5); las demás etapas siguen «Al día». En Anulado el backend no manda ninguna, así que todo queda «Al día». La regla del frontend lee solo `pendingStages` para Salidas, también con `closed` | `P06/` D5; `B/Wms.Application/ForeignTrade/Common/Services/DepositStageRules.cs:108-112` |
| A6 | **Lo que no cambia:** el listado de depósitos ya muestra «Salidas» en «Etapas pendientes» y en su aviso, porque lee `pendingStages` (`F/features/foreign-trade/components/DepositListTable.vue:189`, `:232-233`); el contenido de la etapa (`DepositExitsStage`, FE-2) tampoco cambia | `P06/` D22 |
| A7 | **Galería:** la sección «Etapa Salidas» de `/dev/components` arma el encabezado con `pendingStages` de cada depósito de ejemplo (pendiente si tiene una salida Confirmada a la que le falta algo), para ver el amarillo y «Al día» | `P06/` §8.4 (R6) |

---

## 2. Contrato

Sin cambios. `pendingStages` ya incluye `Exits` por C-F06-10 (BE-1).

## 3. Archivos que se tocan

| Archivo | Cambio |
| --- | --- |
| `F/features/foreign-trade/utils/deposit-stages.ts` | `stageTone` (`:32-44`): sale `if (stage === "Exits") return "idle"` (`:38`); para `Exits`, `warn` si está en `pendingStages` y `done` si no, también con `closed` (A1, A5). `PENDING_TEXT.Exits` (`:52`) pasa a «Salida por completar» y `stageCaption` (`:56-60`) deja de fijarlo (A2). `stageProgress` (`:71-76`) cuenta todas las etapas (A3). Comentarios de F05 actualizados |
| `F/pages/dev/components.vue` | `exitsStageHeader` (`:284-296`) con `pendingStages` por ejemplo (A7) |
| `FT/unit/foreign-trade/deposit-stages.spec.ts` | `:52-55` y `:59-62`: Salidas en amarillo con pendiente, «Al día» sin él, marcada en Cerrado, nada en Anulado; progreso con Salidas |
| `FT/components/foreign-trade/DepositStageStepper.spec.ts` | `:7`, `:23` y `:29`: el texto y el tono nuevos |
| `FT/components/dev/ComponentsGallery.spec.ts` | La etiqueta de la tarjeta de un ejemplo pendiente dice «Salida por completar» |

## 4. Fase única

| Fase | Contenido | Criterio de salida | Estado |
| --- | --- | --- | --- |
| A-1 | A1 a A3, A5 y A7 en el frontend (§3) | Pruebas de §3 en verde; en la galería, la etapa en amarillo con «Salida por completar» y en un ejemplo sin pendiente «Al día»; captura en `D/planes/sprint-11/f06-salidas/evidencias/aj1-*` | Hecha el 2026-11-27 (FE `9df8af7`) |

**Estado de A-1:** hecha el 2026-11-27 (FE `9df8af7`, rama `f2/f06-salidas` sobre FE-2 `a2cac51`). Cifras: `yarn test` 904 → 906 pruebas en verde (163 archivos; el error no manejado de `WeighbridgeQueuePage.spec.ts` ya estaba en la base), `yarn lint` 142 → 142 errores y cero en los archivos tocados, `yarn build` con código 0 antes y después, guardias de `FT/unit/guards/` en verde (37). Hecho: `stageTone` pinta Salidas en amarillo si llega en `pendingStages`, también en Cerrado, y «Al día» si no; «Salida por completar» como texto; `stageProgress` cuenta todas las etapas; la galería arma el encabezado con los pendientes de cada ejemplo. El tono `idle` queda en el tipo `StageTone` sin uso. Capturas: `aj1-01-etapa-salidas-pendiente.jpg` (2026BA00010, «Salida por completar» en amarillo) y `aj1-02-etapa-salidas-al-dia.jpg` (2026BA00016, «Al día»). El stepper con Salidas pendiente lo cubre `FT/components/foreign-trade/DepositStageStepper.spec.ts`; en el detalle real se verá con I-06 (R1).

## 5. Compuertas

Las de `PM/` §6.2 con cifras antes y después: `yarn build` con código 0, `yarn test` en verde, `yarn lint` sin subir errores y sin errores en archivos tocados, guardias de `FT/unit/guards/` en verde.

## 6. Commits

- FE: `fix(depositos): la etapa Salidas se marca en el stepper y cuenta en el progreso (DEC-080, F06)`.
- Docs: `docs(f06): ajuste de la etapa Salidas en el stepper cerrado (sprint 11)`.

Cada uno termina con la línea de coautoría que indique la sesión.

## 7. Riesgos

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R1 | En `fase-2` (sin el backend de F06) Salidas nunca llega pendiente: el detalle real muestra siempre «Al día» hasta I-06 | Esperado (A4); la galería muestra el amarillo; I-06 lo verifica con QA2-F06-043 |
| R2 | El progreso cambia de base (5 → 6 en importación) y un depósito sin salidas cuenta Salidas como «al día» | Lo decidió el usuario (A3); igual que las demás etapas sin pendiente |
