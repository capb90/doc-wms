# Verificación local

> **Para qué sirve:** cómo comprobar un cambio en el equipo de desarrollo sin tocar las bases del usuario ni staging.
> **Fuentes:** `qa/plan-correccion-defectos.md` §4.0 y la experiencia de las fases de paridad y corrección (sep–oct 2026).

## 1. Bases locales

El contenedor de Postgres de desarrollo es `wms-postgres-db` (puerto 5433, imagen `postgres:18.0`). Tiene varias bases con usos distintos. **No mezcles bases.**

| Base | Uso |
| --- | --- |
| `wmsdb` | Base de QA de la campaña de octubre. Quedó en un esquema anterior a `RemoveSampleSeedData`: no la migres sin pedirlo |
| `wms_migracion` | Ensayo de la migración del legacy (datos reales). Para QA sobre datos migrados |
| `wms_grabacion_plantilla`, `wms_grabacion` | Grabación de videos (`Frontend/wms/tools/video-tutoriales/`) |

La base que usa `Wms.Api` en Development está en `appsettings.Development.json` o en el entorno.

## 2. Pruebas automatizadas

| Proyecto | Qué cubre | Cómo |
| --- | --- | --- |
| `Wms.Tests` | Dominio, validadores y clases puras (sin base) | `dotnet test Wms.Tests` |
| `Wms.IntegrationTests` | API real contra Postgres en Testcontainers: autorización, EF, índices, transacciones | `dotnet test Wms.IntegrationTests` (necesita Docker) |
| Frontend | Vitest (`test/**/*.spec.ts`), incluidas guardias de código fuente | `yarn test` |

- Sin Docker: `dotnet test --filter Category!=Integration`.
- La suite de integración comparte la base entre pruebas. Una prueba que deja un camión abierto rompe otras (la cola de báscula corta en 100 camiones): libéralo al terminar.

## 3. Comprobar un handler contra una base desechable

Cuando hace falta ejecutar un handler o una consulta EF sin usar la base del usuario:

1. Levanta un contenedor desechable: `docker run -d --rm --name <nombre> -e POSTGRES_PASSWORD=<clave> -e POSTGRES_DB=<base> -p 55440:5432 postgres:18.0` (trae `unaccent` y `pg_trgm`). Detenlo al terminar.
2. Crea un proyecto de consola **en el scratchpad**, fuera del repo, con `FrameworkReference Microsoft.AspNetCore.App` y referencias a `Wms.Application` y `Wms.Infrastructure`. Registra `AddApplicationServices()` y `AddInfrastructureServices(config)`, más dobles de `IRealtimeNotifier` e `INotificationOrchestrator`.
3. `EnsureCreatedAsync()` crea el esquema desde el modelo, con los `HasData`. Siembra a mano lo que falte: usuario, vehículos, ingreso, terceros y precio de `BASCULA`.
4. Para activar la auditoría, pon un `DefaultHttpContext` con el claim `NameIdentifier` y usa un scope por «petición».
5. Para ver solo el SQL de una consulta no hace falta base: `ToQueryString()`.
6. Para simular la DIAN, registra un `IDianTrmService` falso después de `AddInfrastructureServices`. Para PDF, fija `QuestPDF.Settings.License`.
7. Para S3 local usa `adobe/s3mock` (`-p 9100:9090`, `ServiceURL` + `ForcePathStyle`). En el Mac no hay `pg_dump`: `Backups:PgDumpPath` puede apuntar a un script que haga `docker exec <contenedor> pg_dump`.

## 4. Migraciones

- Generar: `dotnet ef migrations add <Nombre> --project Wms.Infrastructure --startup-project Wms.Api`
- Aplicar: `dotnet ef database update --project Wms.Infrastructure --startup-project Wms.Api`
- Recrear la base local: `dotnet ef database drop --force …` y luego `database update …`
- Rehacer la propia antes del commit: `dotnet ef migrations remove …`
- Comprobar que no falta ninguna: `dotnet ef migrations has-pending-model-changes --project Wms.Infrastructure --startup-project Wms.Api`
- Probar una migración contra un Postgres temporal: `dotnet ef database update … --connection "<cadena>"`

## 5. Trampas conocidas

- **EF y claves generadas en el dominio.** Una entidad nueva que EF descubre por la navegación de un padre ya rastreado queda `Modified`, no `Added`, y el guardado falla con `DbUpdateConcurrencyException`. Agrégala con `context.Set.Add(...)` o configura `ValueGeneratedNever()`.
- **Columnas nuevas en tablas con `HasData`.** Una columna `NOT NULL` con `HasDefaultValue` en una tabla con `HasData` genera una migración inválida. No uses `HasDefaultValue` ahí.
- **Índices sobre la columna de una FK.** Un `HasIndex` explícito sobre esa columna hace que EF borre el índice de la FK. Declara el de la FK aparte y usa `HasDatabaseName`.
- **Npgsql y fechas.** Rechaza `DateTimeOffset` con desplazamiento ≠ 0 para `timestamptz`: convierte con `ToUniversalTime()`.
- **Navegaciones sin `Include`.** Un DTO armado en memoria con `AsNoTracking` que lee una navegación sin `Include` revienta (varios casos con `UnitMeasure.Name`).
- **Compilación.** Si `dotnet build` falla por rutas `bin/Debug/net10.0/bin/...` anidadas, borra `bin/` y `obj/` y compila de forma incremental.
- **zsh.** `grep $(…)` con sustitución vacía lee stdin y se cuelga: pasa `</dev/null`. `GID` es una variable reservada. `for f in $VAR` no parte la lista: usa `while read`.
- **Mayúsculas en el volumen.** `/Volumes/Dock` distingue mayúsculas: `app/features/Administration` y `administration` conviven.
