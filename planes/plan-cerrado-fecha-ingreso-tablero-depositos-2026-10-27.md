# Plan cerrado — Fecha de ingreso en el tablero de depósitos

> **Fecha:** 27 de octubre de 2026. **Estado:** Aprobado por el usuario el 2026-10-27. Prompt del ejecutor, por fase: `prompt-fecha-ingreso-tablero-depositos-2026-10-27.md`.
> **Origen:** §8 de `planes/migracion-staging/resultados/informe-staging-limpio-fase-4.md` y la validación de la fase 4 (§6 de `plan-cerrado-staging-limpio-legacy-2026-10-27.md`). Pedido del usuario del 2026-10-27: «que la tarjeta del tablero de depósitos muestre la fecha de ingreso en lugar de la fecha de creación».
> **Problema:**
> - La tarjeta del tablero (`/foreign-trade/deposits`) muestra `createdAt`, la fecha en que se creó el registro (`DepositKanbanColumn.vue:234`).
> - En los 128 depósitos migrados de staging esa fecha es el 27/10/2026, el día de la carga, y no el ingreso del legacy. Por ejemplo, el `2022BA00002` ingresó el 19/12/2022, como muestra «Abandono y prórrogas».
> - El tablero también **ordena y filtra** («Desde», «Hasta») por `CreatedAt` (`GetDepositsHandler.cs`). Si solo cambiara la fecha visible, la columna saldría con las fechas desordenadas y el filtro no encontraría un depósito por la fecha que muestra.
>
> **Base:** BE `develop` `911399c`; FE `develop` `33fbeba`; docs `main` `a1e4b73` (la validación de la fase 4 de `DEC-043`).
> **Alcance:**
> - 2 fases: código y documentación en local; despliegue en staging;
> - sin migración, sin cambios de permisos y sin tocar datos.
>
> **Rutas:** relativas a `code_workspace/`. Prefijos: `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`; `T/` = `db_legacy/trabajo/` (fuera de git).

---

## 0. Instrucciones para el ejecutor

1. **Lee:**
   - `B/AGENTS.md` y `Frontend/wms/AGENTS.md`;
   - `D/contexto/convenciones-tecnicas.md`;
   - de `D/contexto/decisiones.md`, `DEC-058` (K1 a K4), `DEC-005` y `DEC-043`;
   - este plan completo.
2. **Git:** se trabaja en `develop` (BE y FE) y en `main` de docs, sin ramas ni commits (`DEC-003`). Al cerrar cada fase te detienes con el resumen y los mensajes de commit.
3. **Antes de editar,** confirma con grep las rutas y las líneas citadas. Si el código no coincide, detente y pregunta, con todas las dudas en un solo mensaje. Si un caso borde choca con una decisión de este plan, gana la decisión (`DEC-002`).
4. **Sin retrocesos** (`DEC-005`). Se conservan:
   - el buscador por columna (K1);
   - la carga de 20 en 20 sin repetir ni saltar depósitos (K2);
   - el total de cada columna;
   - el tipo de depósito, «Desde», «Hasta» y «Limpiar filtros» (K3);
   - el clic en la tarjeta, que abre el detalle.
5. **`yarn build` reescribe `.nuxt`.** Si el usuario tiene `yarn dev` abierto, compila sobre una copia de `HEAD`:
   1. `git archive HEAD | tar -x -C <scratchpad>`;
   2. un enlace a `node_modules`;
   3. `nuxt prepare` y luego `nuxt build`.
6. **Bases locales:**
   - la verificación de la fase 1 usa `wms_migracion`, que tiene los 128 depósitos migrados del ensayo de `DEC-043`. Solo la lees: no la recreas ni le escribes;
   - tu API local corre en el puerto 5290. El API del usuario corre en el 5281 contra `wms_qa_preprod`: no lo detengas ni lo reconfigures.
7. **Credenciales:** no abras `.env*`, `deploy/staging/.env.*` ni `infra/terraform.tfvars`. No imprimas contraseñas ni tokens. La credencial del Admin local está en `T/.admin-migracion.local`: un script la lee sin mostrarla. No escribes contraseñas en el navegador.
8. **Staging (fase 2):** antes de cada acción, una línea con lo que harás y el «sí» explícito del usuario (`DEC-006`).

---

## 1. Decisiones

| # | Decisión |
| --- | --- |
| F1 | **La fecha de ingreso del tablero es `EntryDate ?? CreatedAt` del depósito.** Es la misma regla que ya usan «Abandono y prórrogas» (`AbandonmentReader`), los movimientos del depósito, la facturación de almacenamiento y las listas de Importaciones, Exportaciones e Inspecciones (`entryDate ?? createdAt`, rotulada «Fecha de ingreso»).<br>• En un depósito creado en la v2, es la entrada de Vigilancia del primer camión (D04).<br>• En un migrado, es la fecha de ingreso del legacy.<br>• `CreatedAt` solo se usa si no hay `EntryDate`: son depósitos anteriores a D04 |
| F2 | **`DepositKanbanDto` agrega `EntryDate`** (`DateTimeOffset`, no nulo), ya resuelta con F1. `CreatedAt` se conserva como está |
| F3 | **La tarjeta muestra la fecha de ingreso,** `formatColombiaDate(deposit.entryDate)`, en el mismo lugar y con el mismo estilo. El `title` y el `aria-label` dicen «Fecha de ingreso: dd/mm/aaaa» |
| F4 | **El tablero ordena por F1, de la más reciente a la más antigua, y luego por `Id` descendente.** El desempate por `Id` mantiene el orden estable de K2. Los depósitos nuevos siguen arriba, y los migrados quedan por su ingreso del legacy |
| F5 | **El filtro «Desde» / «Hasta» del tablero filtra por F1,** con los mismos límites del día en Colombia (CHG-77). Las etiquetas «Desde» y «Hasta» no cambian. Los textos de ayuda pasan de «Fecha desde» / «Fecha hasta» a «Ingreso desde» / «Ingreso hasta» |
| F6 | **Fuera de alcance:**<br>• las listas de Importaciones, Exportaciones e Inspecciones, que ya muestran la fecha de ingreso;<br>• el detalle del depósito, que muestra «Fecha Creación» y «Fecha Ingreso»;<br>• las pantallas donde la fecha de creación es la correcta: órdenes de cargue, guías, listas de empaque;<br>• las tarjetas de conteo de `/foreign-trade` |
| F7 | **Sin migración ni índice nuevo.** El modelo no cambia. El orden por la expresión de F1 recorre los depósitos de comercio exterior, que son unos cientos |
| F8 | **Sin clase pura nueva.** F1 es una sola expresión, la misma que ya usan en línea `AbandonmentReader`, `GetAbandonmentCandidatesHandler`, `GetWarehouseStorageMovementsHandler` y `StorageBillingService`. Se prueba con pruebas de integración del endpoint |

---

## 2. Fase 1 — Backend, frontend y documentación (local)

**Pasos:**

1. **BE, DTO** (`B/Wms.Application/ForeignTrade/Common/DTOs/DepositKanbanDto.cs`): agrega `EntryDate`, con un comentario que cite F1.
2. **BE, consulta** (`B/Wms.Application/ForeignTrade/Queries/GetDeposits/GetDepositsHandler.cs`):
   - el filtro de fechas: `(ws.EntryDate ?? ws.CreatedAt) >= FromDate` y `<= ToDate` (F5);
   - el orden: `.OrderByDescending(ws => ws.EntryDate ?? ws.CreatedAt).ThenByDescending(ws => ws.Id)` (F4). Actualiza el comentario de K2;
   - la proyección y el mapeo de `EntryDate` (F2).
3. **BE, pruebas** (`B/Wms.IntegrationTests/ForeignTrade/DepositKanbanSearchTests.cs`):
   - **`Paging_SameCreatedAt_NoRepeatsNorGaps` pasa a `Paging_SameEntryDate_NoRepeatsNorGaps`:** el empate es ahora en F1. Iguala `EntryDate` y `CreatedAt` de los depósitos sembrados y conserva lo que verifica: ni repetidos ni saltos;
   - **nueva `EntryDate_DrivesCardDateOrderAndDateFilter`:**
     - un depósito con ingreso antiguo y creado hoy, como un migrado, devuelve su ingreso en `entryDate`;
     - en la columna queda **debajo** de uno con ingreso reciente;
     - `fromDate`/`toDate` del día de su ingreso lo encuentran, y los del día de su creación no;
   - **nueva `EntryDate_FallsBackToCreatedAt`:** sin `EntryDate`, `entryDate` es `createdAt`.

   Los datos de prueba se ajustan con `ExecuteUpdateAsync`, como ya hace la prueba de paginación.
4. **FE, tipo** (`F/features/foreign-trade/types/deposit-kanban.ts`): agrega `entryDate: string` a `IDepositKanbanDto`.
5. **FE, tarjeta** (`F/features/foreign-trade/components/DepositKanbanColumn.vue`, línea 234): muestra F3.
6. **FE, tablero** (`F/pages/foreign-trade/deposits/index.vue`): cambia los textos de ayuda de F5. Las etiquetas no cambian.
7. **FE, pruebas** (`FT/components/foreign-trade/DepositKanbanColumn.spec.ts`):
   - el depósito de ejemplo trae un `entryDate` distinto de `createdAt`;
   - un caso nuevo comprueba que la tarjeta muestra la fecha de ingreso en hora de Colombia, con su `title`.
8. **Compuertas:**
   - BE: `dotnet build Wms.sln`, `dotnet test Wms.Tests` y `dotnet test Wms.IntegrationTests --filter "FullyQualifiedName~ForeignTrade"`, con Docker;
   - FE: `yarn test`, `yarn lint` (sin subir el número de errores) y `yarn build`.
9. **Verificación por API en local, sin navegador:**
   - corre el API de `911399c` más tus cambios en el puerto 5290, contra `wms_migracion`;
   - un script toma el token del Admin con `T/.admin-migracion.local` sin imprimirlo y llama `GET foreign-trade/deposits?depositType=Import&status=Confirmed&pageSize=20`;
   - comprueba:
     - el `2022BA00002` devuelve `entryDate` del 19/12/2022 en hora de Colombia, el mismo día que da `GET foreign-trade/abandonment?all=true`;
     - las fechas de ingreso de la columna van de la más reciente a la más antigua, sin repetidos entre la página 1 y la 2;
     - con `fromDate` y `toDate` del 19/12/2022 (límites del día en Colombia), la respuesta incluye el `2022BA00002`;
     - con los del 27/10/2026, día de la carga, solo salen depósitos con ingreso ese día.
   - Deja las respuestas en `T/evidencias/tablero-fecha-ingreso/` y detén el API al terminar.
10. **Docs:**
    - `D/qa/fase-05-comercio-exterior.md`:
      - caso nuevo **F5-LIS-011 «Fecha de ingreso en la tarjeta»**: un depósito migrado muestra su ingreso del legacy, igual que «Abandono y prórrogas»; uno nuevo muestra la entrada de Vigilancia del primer camión;
      - F5-LIS-001: «Desde» y «Hasta» filtran por la fecha de ingreso;
      - F5-LIS-008: el orden es por la fecha de ingreso;
    - el §5 de este plan, con el estado de la fase.

**Criterio OK:**

| # | Criterio |
| --- | --- |
| A1 | Las compuertas del paso 8 pasan, y las tres pruebas de integración del paso 3 están en verde |
| A2 | La verificación del paso 9 da los cuatro resultados esperados |
| A3 | Nada de lo listado en §0.4 cambió |

**Commits sugeridos:**
- BE: `fix(comercio-exterior): el tablero de depósitos devuelve, ordena y filtra por la fecha de ingreso, no por la de creación`
- FE: `fix(comercio-exterior): la tarjeta del tablero de depósitos muestra la fecha de ingreso`
- docs: `docs(planes,qa): fecha de ingreso en el tablero de depósitos, fase 1, y caso F5-LIS-011`

---

## 3. Fase 2 — Despliegue en staging

**Empieza cuando** la fase 1 está commiteada en BE y FE y el usuario confirma la ventana: hay operarios probando. El API se reinicia unos segundos; avísales antes.

| # | Paso | Detalle |
| --- | --- | --- |
| 1 | Respaldo | `POST administration/backups/run`, con los dos destinos (`local-staging` y `s3-externo`) en `Succeeded`. Anota el nombre |
| 2 | Backend | `scripts/deploy-staging.sh backend` y reinicio de `wms-api`. **Sin `migrate`:** el cambio no trae migraciones. Compruébalo antes en local con `dotnet ef migrations list`: deben seguir siendo 19 |
| 3 | Frontend | `scripts/deploy-staging.sh frontend` |
| 4 | Humo | `scripts/deploy-staging.sh smoke` y 0 líneas `fail`/`crit` nuevas en el log de `wms-api` |
| 5 | Verificación de solo lectura | Con la sesión del Admin que abre el usuario, en el tablero (Importación, Confirmado):<br>• el `2022BA00002` muestra 19/12/2022, como «Abandono y prórrogas»;<br>• las fechas van de la más reciente a la más antigua, también al bajar por la columna;<br>• «Desde» = «Hasta» = 19/12/2022 lo encuentra.<br>No se crea ni se edita nada |
| 6 | Registro | `D/contexto/estado.md` §3: último despliegue con los commits, sin migraciones, y el respaldo previo. El §5 de este plan |

**Criterio OK:** B1, los pasos 1 a 4 sin errores; B2, la verificación del paso 5 tal como se describe.

**Commit sugerido (docs):** `docs(staging): despliegue de la fecha de ingreso en el tablero de depósitos`

**Relación con `DEC-043`:** este despliegue no toca datos ni tarifas. La fase 4b puede ir antes o después. El respaldo `bf7bf952` sigue siendo el punto de vuelta del reinicio limpio, pero restaurarlo no revierte el código desplegado.

---

## 4. Riesgos

| Riesgo | Mitigación |
| --- | --- |
| Alguien filtraba el tablero por la fecha de creación | El tablero acaba de cambiar con `DEC-058` y los operarios empiezan hoy con el staging limpio, así que no hay un uso establecido. Las listas por modalidad ya filtran y muestran la fecha de ingreso |
| Un depósito con la fecha de ingreso corregida (`CorrectEntryDate`) cambia de lugar mientras se baja por la columna | Es el mismo caso de cualquier edición durante la carga por páginas. Al recargar, el orden es el correcto |
| El reinicio del API interrumpe a un operario | La ventana la confirma el usuario y los operarios reciben el aviso antes |

---

## 5. Estado de las fases

| Fase | Estado | Notas |
| --- | --- | --- |
| 1 · Código y documentación (local) | Hecha (2026-10-27): BE `aa69633`, FE `efaabdf`, docs `39e27be` | Base BE `911399c`, FE `33fbeba`, docs `8354a11`. Unas 1 h 15 min.<br>• **Compuertas:** `dotnet build` sin errores; `Wms.Tests` 2092/2092; `Wms.IntegrationTests` (ForeignTrade) 106/106, con las tres pruebas del paso 3; `yarn test` 608/608 (113 archivos); `yarn lint` 276 errores en total; los cuatro archivos tocados tienen 0 antes y después, así que no sube; `yarn build` OK (sin `yarn dev` abierto: se compiló en el árbol).<br>• **Verificación por API** (5290 contra `wms_migracion`, Importación, Confirmado): 128 depósitos; las páginas 1 y 2 (40) van de la fecha de ingreso más reciente a la más antigua (08/06/2024 → 23/05/2024), sin repetidos, y las 40 tienen la creación el 27/10/2026; 32 de ellas salen en «Abandono y prórrogas» y las 32 coinciden en el día; «Desde» = «Hasta» = 19/12/2022 devuelve solo el `2022BA00002`, con ingreso el 19/12/2022, como «Abandono y prórrogas»; con el 27/10/2026 la importación da 0 depósitos en los cuatro estados (ninguno ingresó ese día). Evidencias en `T/evidencias/tablero-fecha-ingreso/`.<br>• **QA:** F5-LIS-011 nuevo; F5-LIS-001 y F5-LIS-008 actualizados.<br>• **Desviaciones:** (1) el `2022BA00002` no está en las dos primeras páginas porque, con F4, queda al fondo de la columna; su `entryDate` se comprobó en la respuesta filtrada por su día. (2) `wms-postgres-db` estaba detenido: se arrancó para la verificación y se detuvo al terminar; la cadena de conexión se armó con las variables del contenedor, sin abrir `.env*` ni mostrarlas. (3) Para no escribir en `wms_migracion`, el API se lanzó sin semilla del Admin (`Bootstrap__AdminPassword` vacío) y se detuvo a los 2 s, antes de que arranquen los jobs (30 s); solo el inicio de sesión del Admin tocó la base. |
| 2 · Despliegue en staging | Hecha, sin commit (2026-10-27) | Desplegado BE `aa69633` / FE `efaabdf`, con un «sí» del usuario en cada paso. Unos 45 min, con las esperas de aprobación.<br>• **Antes:** BE, FE y docs limpios con los commits de la fase 1; `dotnet ef migrations list`: 19, las mismas de staging; el diff de la fase 1 no toca `Migrations/`.<br>• **Paso 1, respaldo:** `wms_20261027_150129_c5d72ef2.dump`, `Succeeded` en `local-staging` y `s3-externo`.<br>• **Paso 2, backend:** imagen cargada y `wms-api` recreado a las 20:09 UTC, sin `migrate`.<br>• **Paso 3, frontend:** `yarn generate` y `rsync` a `/opt/wms/site` sin errores.<br>• **Paso 4, humo:** frontend 200, SPA 200, login inválido 400, CORS presente. El log de `wms-api` desde el reinicio tiene 1 línea `fail` y 0 `crit`; esa línea es «Credenciales inválidas», el login `x`/`y` de la propia prueba de humo. **B1 OK.**<br>• **Paso 5, verificación de solo lectura** (sesión del Admin, Importación, Confirmado): en pantalla, bajando por la columna de 20 en 20, salen 128 tarjetas, sin repetidos y con las fechas de ingreso de la más reciente (08/06/2024) a la más antigua (04/07/2022); el `2022BA00002` muestra 19/12/2022 en la posición 127, igual que «Abandono y prórrogas»; «Desde» = «Hasta» = 19/12/2022 deja solo el `2022BA00002` en Confirmado, y «Limpiar filtros» vuelve a 128. Los textos de ayuda dicen «Ingreso desde» / «Ingreso hasta». Por API (GET) da lo mismo, y los 67 depósitos de «Abandono y prórrogas» coinciden en el día con el tablero. Las 128 tienen la creación el 27/10/2026. No se creó ni se editó nada. **B2 OK.** Resumen en `T/evidencias/tablero-fecha-ingreso/staging-fase2-resumen.md`.<br>• **Desviaciones:** (1) la primera vez, el navegador del panel no tenía sesión; el usuario la abrió ahí antes del respaldo. (2) La carga infinita solo avanza con la columna visible en la ventana, porque usa un centinela; con la columna fuera de vista, mover el scroll por script no carga más. No es un defecto: un usuario siempre baja con la columna a la vista. |
