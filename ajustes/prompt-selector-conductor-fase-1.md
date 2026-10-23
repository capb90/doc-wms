Eres el implementador de la **Fase 1 (backend)** del selector de conductor del WMS de Bodegas Asociadas. Modelo recomendado: **Sonnet 5.5**.

- Agregas la búsqueda paginada de conductores por nombre o documento.
- Abres a Bodega el alta y la edición de conductores.
- Cubres los dos cambios con pruebas.

**Solo backend.** El frontend es la Fase 2 y no se toca.

## Lee primero
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que cita (`code_workspace/docs/contexto-negocio-wms-para-ia.md`).
2. **El plan cerrado:** `code_workspace/ajustes/plan-cerrado-selector-conductor-2026-10-08.md`, aprobado por el usuario el 2026-10-08. Léelo entero. Tu alcance es **§4**, más las decisiones D3, D4, D5 y D13 de §2. El resto es contexto.
3. **El código que vas a tocar:**
   - `Wms.Application/Logistics/Drivers/Queries/GetAllDrivers/` (consulta y handler);
   - `Wms.Domain/Security/WmsPolicyRoles.cs`;
   - `Wms.Api/Controllers/v1/DriverController.cs`;
   - como patrón de búsqueda y orden, `Wms.Application/Administration/Crews/Queries/GetCrewsQuery.cs`;
   - como patrón de normalización del documento, `Wms.Application/Weighbridge/Common/Services/EntryDriverRules.cs` (`NormalizeIdNumber`).

## Situación de partida
- **Repositorio:** `Backend/wms-api`, rama `develop`. El plan se escribió sobre `b7c656e`. Anota el hash con que empiezas: `git rev-parse --short HEAD`.
- **Sin migraciones:** el cambio no toca el esquema.
- **Datos del entorno:** staging tiene 4.361 conductores migrados. Por eso el selector de la Fase 2 buscará en el servidor y no traerá todo con `all=true`.

## Reglas
1. Trabaja en `develop`. **No crees ramas ni hagas commits**: el usuario commitea al revisar.
2. **Migraciones.** No generes migraciones ni toques `Wms.Infrastructure/Migrations/`. Al final, `dotnet ef migrations has-pending-model-changes --project Wms.Infrastructure --startup-project Wms.Api` debe quedar limpio. Si no queda limpio, detente.
3. **Si el código contradice el plan, no improvises.** Detente y pregunta, con todas las dudas en un solo mensaje. Un caso concreto: si EF no traduce a SQL el `Unaccent` sobre la concatenación `FirstName + " " + LastName`, no lo resuelvas evaluando en memoria; repórtalo.
4. **No cambies lo que el plan deja fuera:**
   - el orden por defecto (`CreatedAt`, `Id`), del que depende Administración → Conductores;
   - los filtros `name`, `idNumber`, `idType` e `isActive`;
   - `VehicleController` y `TransportCatalogAccess`;
   - `EntryDriverRules` y `EntryLogInfoUpdater`;
   - `CreateReceptionWithoutWeighbridgeCommandHandler`.
5. **Mensajes y comentarios** en español, con la densidad de comentarios del código vecino.

## Pasos
1. **Línea base.** Antes de cambiar nada, compila y corre las suites:

   ```bash
   dotnet build
   ```

   ```bash
   dotnet test Wms.Tests
   ```

   ```bash
   dotnet test Wms.IntegrationTests
   ```

   Las pruebas de integración usan Testcontainers: Docker debe estar arriba. Anota los conteos. Si algo ya falla en la línea base, anótalo y sigue sin arreglarlo.
2. **B-1. Búsqueda (plan §4.1):**
   - `Search` y `OrderByName` en `GetAllDriversQuery`, con los comentarios del plan;
   - el filtro D4 en `GetAllDriversHandler`;
   - el orden D5 aplicado sobre la entidad antes de proyectar al DTO.
3. **B-2. Política (plan §4.2):**
   - `DriverCatalogAccess` en `WmsPolicyRoles`, con Admin, Receiving, Scale, ForeignTrade y Warehouse, y su comentario;
   - en `DriverController`, `CreateDriver` y `UpdateDriver` con esa política.
4. **B-3. Pruebas (plan §4.3):**
   - `WmsPolicyRolesTests` y `ControllerAuthorizationTests` actualizadas;
   - `Wms.IntegrationTests/Logistics/DriverSearchTests.cs` con los 7 casos;
   - los 4 casos nuevos en `CatalogWriteAuthorizationTests`.

   **La base de las pruebas de integración es compartida.** Cada prueba siembra sus propios conductores por API, como Admin, con un sufijo único por ejecución. Las aserciones filtran por ese sufijo y nunca dependen de conteos globales.
5. **Verificación (plan §4.4):** build, las dos suites y `has-pending-model-changes`. Todo verde.
6. **Prueba manual corta contra la API local** (puerto 5281; `dotnet run --project Wms.Api` si no está arriba), con un token de Admin de la base local:
   - `GET /api/v1/drivers?search=<término>&isActive=true&orderByName=true&pageSize=20`;
   - el mismo término sin tildes;
   - un fragmento de documento.

   Anota el `totalCount` y el tiempo (`curl -w '%{time_total}'`). No escribas contraseñas en la salida ni en archivos.

## Trampas conocidas
- **Compilación:** si `dotnet build` falla por rutas `bin/Debug/net10.0/bin/...` anidadas, borra `bin/` y `obj/` de los proyectos y compila en modo incremental. No uses `--no-incremental` en paralelo.
- **zsh:**
  - un patrón `--include=*.cs` sin comillas falla con «no matches found»: usa `'*.cs'`;
  - un `grep $(...)` con la sustitución vacía lee stdin y se cuelga: pasa `</dev/null`.
- **Permisos de ASP.NET:** los `[Authorize]` se suman (AND). El controlador ya tiene `ActiveUser` a nivel de clase. La política del método se agrega a esa, no la reemplaza: así debe quedar.

## Entrega y detención
Al terminar, **detente** y entrega un resumen con:

1. el hash inicial y la lista de archivos tocados (`git status --short`);
2. los conteos de `Wms.Tests` e `IntegrationTests`, antes y después, y los nombres de las pruebas nuevas;
3. el resultado de `has-pending-model-changes`;
4. el resultado de la prueba manual: términos, `totalCount` y tiempos;
5. las desviaciones del plan, con su motivo, o «ninguna»;
6. un mensaje de commit propuesto, por ejemplo `feat(conductores): búsqueda paginada por nombre o documento y alta desde Bodega`, que termine con la línea de coautoría de tu modelo.

**No empieces la Fase 2.** Empieza solo cuando el usuario commitee esta fase y la autorice.
