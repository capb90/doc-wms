Eres el implementador de **R-TRZ**, una regla de trazabilidad que el usuario decidió el 2026-10-05 a partir de una observación de la sesión S2 del re-test de QA (fase 11) del WMS de Bodegas Asociadas. Modelo recomendado: **Sonnet 5.5** (complejidad baja: una columna, un handler y la consulta del tablero). **El re-test de QA sigue en curso sobre la base local**: solo puedes aplicarle la migración de esta tarea, como se indica abajo.

## Contexto
- **La regla.** En el tablero de trazabilidad, un camión cuyo **último servicio fue descartado en báscula** y que **no tiene un servicio vigente** debe aparecer **«Cancelado»** y no contar en «En portería». Así lo pide el criterio 2 de CHG-42.
  - Si después del descarte se le registra un servicio nuevo (CHG-06 lo permite), manda el estado del servicio nuevo.
  - Si el camión sale sin servicio nuevo, también aparece «Cancelado».
- **Por qué hoy no pasa.** `DiscardIncompleteOperationHandler` (CHG-06) marca el servicio como `Discarded` y además borra sus vínculos con los ingresos (`ServiceRecordEntryLogs.RemoveRange(...)`) para liberar el camión. Después de eso, `GetTraceabilityDashboardHandler` ve el ingreso sin servicio y `TruckStageResolver` lo pone «En portería» (regla 2).
- **Decisión del usuario (cerrada).** El ingreso guarda la fecha del último descarte en una **columna nueva**:
  - el descarte la llena;
  - la limpia el momento en que el ingreso recibe un servicio nuevo;
  - el tablero la usa para mostrar «Cancelado».

## Lee primero
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. `docs/qa/plan-correccion-defectos.md`: la sección «4.0 Reglas comunes» (en especial 4.0.2 migraciones y 4.0.10 «Sin retrocesos funcionales») y las tarjetas **CHG-06 y CHG-42**.
3. `docs/qa/resultados/F11-informe-S2-2026-10-05.md`, §5, observación 2.
4. El código:
   - `DiscardIncompleteOperationHandler`;
   - la entidad `EntryLog` y su configuración EF;
   - los puntos donde se crea un `ServiceRecordEntryLog`, es decir, dónde un ingreso recibe un servicio. Búscalos todos: registro con depósito, Solo báscula, Salida, recepción sin báscula y camión agregado a un documento;
   - `Wms.Application/Reports/Queries/GetTraceabilityDashboard/` (`GetTraceabilityDashboardHandler`, `TruckStageResolver`, `TraceabilitySummaryCalculator`, `TruckStages`).

## Alcance (cerrado)
1. **Dominio.**
   - `EntryLog` recibe `ServiceDiscardedAt` (`DateTimeOffset?`, `private set`) con dos métodos:
     - `MarkServiceDiscarded(DateTimeOffset at)`;
     - `ClearServiceDiscarded()`.
   - Pon un `<summary>` que cite R-TRZ, CHG-06 y CHG-42.
2. **Descarte.** `DiscardIncompleteOperationHandler` llama `MarkServiceDiscarded` en **cada ingreso** cuyo vínculo borra, antes del `RemoveRange`, con la misma hora del `Discard`.
3. **Servicio nuevo.** Un solo punto limpia la marca cuando el ingreso recibe un servicio: el método o la fábrica que crea el vínculo `ServiceRecordEntryLog`, o un paso común si no existe uno. No repartas `ClearServiceDiscarded()` por cada handler si hay un lugar común. Si no lo hay, llámalo en cada uno de los puntos que encontraste y lístalos en la entrega.
4. **Tablero.**
   - `TruckStageResolver.Determine` recibe `bool serviceDiscarded`.
   - Si el ingreso **no tiene servicio** y `serviceDiscarded` es verdadero, la etapa es `TruckStages.Canceled`, con o sin salida. Esta regla se evalúa antes de la regla (2) «En portería» y antes de «Salida registrada».
   - Con servicio, todo sigue como hoy.
   - `GetTraceabilityDashboardHandler` pasa `entry.ServiceDiscardedAt is not null`.
   - Revisa que `TraceabilitySummaryCalculator` cuente ese camión en «Cancelado» y no en «En portería».
5. **Migración.**
   - Genérala con `dotnet ef migrations add AddEntryLogServiceDiscardedAt` (proyecto `Wms.Infrastructure`, arranque `Wms.Api`).
   - Revisa que tenga **una sola operación `AddColumn` nullable**, sin `DropColumn`, `AlterColumn`, `RenameColumn` ni `UpdateData`. Si trae otra cosa, detente y repórtalo sin aplicarla.
   - **No edites los archivos generados.**
   - **Base local de QA:** solo con la migración revisada, aplícala con `dotnet ef database update`. Nunca uses `database drop` ni `migrations remove` sobre una migración aplicada, ni SQL manual. La columna nace en NULL, así que los datos del re-test no cambian.
   - **No reinicies el API**: lo hace el usuario antes de la S3.
6. **Fuera de alcance:**
   - el camión de recepción directa que aparece «En tránsito» sin contador propio;
   - las demás observaciones de S2;
   - rellenar la marca en los ingresos descartados antes de esta corrección (son datos de prueba; QA hará un descarte nuevo).

## Pruebas
- **Unitarias de `TruckStageResolver`:**
  - sin servicio y descartado → «Cancelado»;
  - sin servicio, descartado y con salida → «Cancelado»;
  - sin servicio y no descartado → «En portería» (como hoy);
  - con servicio → igual que hoy.
- **Unitarias de `EntryLog`:** marcar y limpiar.
- **Integración** (Testcontainers):
  - registrar y descartar → el tablero muestra el camión «Cancelado» y no lo cuenta en «En portería»;
  - volver a registrarlo → muestra la etapa del servicio nuevo y la marca queda en NULL;
  - un camión que nunca tuvo servicio sigue «En portería».
- Las pruebas existentes de trazabilidad, de descarte (`DiscardOperationTests`) y de la cola de báscula pasan sin editarlas. Recuerda liberar los camiones que dejes abiertos: la cola corta en 100.

## Sin retrocesos (regla 4.0.10)
- El descarte sigue liberando al camión: vuelve a «Sin iniciar» en la cola y se puede registrar de nuevo (CHG-06).
- La recuperación de operaciones no cambia.
- Los demás rótulos y contadores del tablero no cambian.

## Restricciones (obligatorias)
- Trabaja en `develop`. **No crees ramas, no hagas `git add`, commit, push ni merge**: entregas los mensajes de commit y el usuario hace los commits.
- No copies contraseñas ni secretos. No toques producción ni `infra/`.
- Textos y comentarios en español. Respeta la estructura por features.
- Fuera de aplicar esta migración, no uses la base, el API ni el frontend locales.

## Verificación antes de terminar
1. `dotnet build` sin errores ni advertencias nuevas.
2. `dotnet test` de `Wms.Tests` (1574 hoy) y `Wms.IntegrationTests` (251 hoy) en verde. Reporta los totales.
3. `dotnet ef migrations has-pending-model-changes` sin cambios después de generar la migración.
4. `dotnet ef migrations list` muestra la migración nueva aplicada en la base local.
5. El frontend no cambia: el rótulo «Cancelado» ya existe en el tablero. Si no existiera, detente y repórtalo.

## Entrega
Responde con:
1. Los archivos creados o modificados, incluidos los puntos donde se limpia la marca.
2. Las operaciones de la migración (una por línea) y la confirmación de que se aplicó a la base local.
3. El resultado de cada compuerta, con números.
4. Lo que QA debe re-testear en la S3: descartar un registro nuevo sin salida, revisar el tablero, registrarlo de nuevo y revisar otra vez.
5. **Los mensajes de commit**, listos para pegar, cada uno por separado:
   - **Backend (código):** `fix(qa-f11): el camión con el servicio descartado aparece «Cancelado» en trazabilidad (R-TRZ, CHG-42)`, con una línea por cambio.
   - **Backend (migración):** `feat(qa-f11): migración AddEntryLogServiceDiscardedAt`.
   - **Frontend (documentación):** `docs(qa-f11): prompt de R-TRZ`.
   - Todos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí.** La verificación en pantalla la hace QA en la S3, después de que el usuario reinicie el API.
