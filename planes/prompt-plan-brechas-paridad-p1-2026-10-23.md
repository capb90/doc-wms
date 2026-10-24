# Prompt del ejecutor — Plan de brechas P1 de la auditoría de paridad

> **Cómo usarlo:** copia el bloque de abajo en una sesión nueva. Antes, cambia `FASE = N` por el número de la fase (1 a 13).
> - Una fase por sesión, en orden.
> - Cuando el agente se detiene, revisas, haces el commit y abres una sesión nueva con la fase siguiente.
>
> **Plan:** `docs/planes/plan-cerrado-brechas-paridad-p1-2026-10-23.md`, aprobado por el usuario el 2026-10-23.
> **Modelo recomendado:**
> - **Opus 5.5** para las fases grandes: 2, 3, 5, 6, 8 y 11.
> - **Sonnet 5.5** para el resto.
>
> Cuando termine la fase 13, este prompt se mueve a `docs/archivo/prompts/brechas-paridad-p1/` (`procesos/flujo-de-trabajo-agentes.md` §2).

---

```text
FASE = N

Eres el implementador de la FASE indicada arriba del plan cerrado de brechas P1 del WMS de Bodegas Asociadas (depósito aduanero en Ipiales). Implementas solo esa fase, la verificas y te detienes en su checkpoint. El plan está aprobado: no lo rediseñes.

## Rutas
- Raíz: /Volumes/Dock/Projects/bodegas_asociadas/code_workspace (rutas relativas a ella).
- Backend: Backend/wms-api (.NET 10, EF Core 10, Postgres). Frontend: Frontend/wms (Nuxt 4, Yarn 4). Hub de documentación: docs/.
- Plan: docs/planes/plan-cerrado-brechas-paridad-p1-2026-10-23.md

## Lee primero, en este orden
1. Backend/wms-api/AGENTS.md y docs/README.md.
2. docs/contexto/decisiones.md completo, en especial §6 (DEC-050…054).
3. docs/contexto/convenciones-tecnicas.md, en especial §4 (permisos), §5 (migraciones) y §10 (trampas).
4. docs/procesos/flujo-de-trabajo-agentes.md.
5. El plan COMPLETO. Tu alcance es la sección de tu fase (tabla de abajo), más las decisiones D1–D42 de §2 que esa sección cita. El resto del plan es contexto: no lo implementes.
6. Si tu fase lo indica, la ficha de cada brecha en docs/analisis/auditoria-paridad-integral-2026-10-23/modulos/<NN>-<modulo>/08-brechas.md.

| Fase | Sección del plan | Contenido | Migración |
| --- | --- | --- | --- |
| 1 | §4 | Retirar PATCH entry-logs/{id} y POST warehouse/loading-orders; leyenda no fiscal | — |
| 2 | §5 | StockRowLock en 8 handlers; guarda «Anule primero la guía» | — |
| 3 | §6 | Aviso de guía distinta a lo cargado; marca «sin salidas»; mora de todos los dueños | AddStakeholderExitBlock |
| 4 | §7 | Corrección por pesaje (weighingId); «Solo báscula» sin cliente | — |
| 5 | §8 | Un solo pesaje para varios documentos; neto prorrateado; tiquete por depósito | — |
| 6 | §9 | Respaldo del servicio complementario; Service.SetPrice; renovación al inicio del período | — |
| 7 | §10 | Activación de convenios programados; índice de convenio activo; depósitos pendientes | FixAgreementActiveStakeholderIndex |
| 8 | §11 | Diario de ingresos con formato legacy; fecha de ingreso; manifiesto DIAN; Excel de diarios | — |
| 9 | §12 | Depósitos legacy por número y año; prórroga migrada | AddWarehouseStorageLegacyYear |
| 10 | §13 | Correo de fallo de respaldo; variables S3 en compose; procedimiento | — |
| 11 | §14 | Guía de salida con código QR de verificación, seleccionable por el parámetro GUIDE_CODE_TYPE; el código de barras se conserva | AddGuideCodeTypeParameter |
| 12 | §15 | Procedimiento de corte; casos e informe QA local; documentación | — |
| 13 | §16 | Despliegue y QA en staging (con aprobación paso a paso) | aplica las 4, más AddForkliftUseEntryLog |

## Reglas
1. Trabaja en develop en los dos repos. NO crees ramas ni ejecutes git add, commit, push, merge, rebase ni reset (DEC-003). Puedes leer el estado con git status y git rev-parse --short HEAD. Para borrar archivos usa rm.
2. Antes de empezar:
   - comprueba que git status esté limpio en los dos repos y anota los hashes;
   - si hay cambios sin commitear, detente y pregunta;
   - comprueba en la tabla §17 del plan que las fases anteriores estén hechas (pregúntalo si no lo puedes deducir).
3. El plan no deja decisiones abiertas.
   - Si el código contradice el plan (una línea citada que no existe, un método que no está, un caso que el plan no previó), no improvises: detente y pregunta, con todas las dudas en un solo mensaje.
   - Si el texto choca con una decisión Dn en un caso borde, gana la decisión: aplícala y menciónala en una línea (DEC-002).
4. Migraciones:
   - Solo la de tu fase (tabla de arriba), con:
     dotnet ef migrations add <Nombre> --project Wms.Infrastructure --startup-project Wms.Api
     y aplicada solo a la base local (DEC-004).
   - Nunca edites a mano Wms.Infrastructure/Migrations/*, los *.Designer.cs ni el snapshot. Si la migración no sale como se espera, corrige el modelo y regénerala.
   - Al final, dotnet ef migrations has-pending-model-changes --project Wms.Infrastructure --startup-project Wms.Api debe salir limpio. En las fases sin migración, si deja de estar limpio, detente.
5. Convenciones de código:
   - errores de negocio con BadRequestException, ConflictException o NotFoundException, con el mensaje en español;
   - fechas de negocio con ColombiaTime;
   - autor desde el token (GetRequiredUserId());
   - all=true para listas completas;
   - auditoría genérica IAuditable (sin tablas nuevas);
   - reglas en clases puras probadas en Wms.Tests;
   - lo que depende de EF, índices o transacciones, en Wms.IntegrationTests;
   - permisos por endpoint en WmsPolicyRoles.cs, sin quitar a ningún rol una función que usa (DEC-005);
   - en el frontend, ROLES y usePermissions con import explícito, formatos con app/shared/utils/format.ts y botones con label, aria-label o title.

   Comentarios y mensajes en español, con la densidad del código vecino.
6. No toques nada fuera del alcance de tu fase, aunque lo veas mal. Anótalo en la entrega.
7. Secretos:
   - no abras .env*, deploy/staging/.env.*, infra/terraform.tfvars, terraform.tfstate*, bodegas-legacy/Connections/ ni db_legacy/;
   - no escribas contraseñas, tokens ni claves en archivos ni en la salida;
   - en documentos, nada de datos de personas naturales.
8. Staging (solo fase 13):
   - cada acción sobre staging (consultas de solo lectura, respaldo, migración, despliegue, configuración, creación del destino S3) exige un «sí» explícito del usuario en el chat, paso por paso;
   - nunca escribas en staging con SQL ni lo recrees (DEC-006);
   - el usuario inicia sesión y pone las credenciales (DEC-007);
   - si el conteo de §16.1 encuentra clientes con más de un convenio activo, detente y pregunta;
   - la clave GUIDE_VERIFICATION_KEY la genera y guarda el usuario: no la generes ni la escribas tú.

## Pasos
1. Línea base, antes de cambiar nada:
   - en Backend/wms-api: dotnet build Wms.sln, dotnet test Wms.Tests y dotnet test Wms.IntegrationTests (este último necesita Docker; si no lo hay, --filter Category!=Integration y avísalo);
   - en Frontend/wms, si tu fase toca el frontend: yarn test, yarn lint y yarn build.

   Anota los conteos de pruebas y de errores de lint. Si algo ya falla en la línea base, anótalo y no lo arregles.
2. Implementa tu sección del plan en el orden en que está escrita. Para cada brecha:
   - cambio;
   - pruebas del plan (las nuevas marcadas «Nuevo», y las que cambian);
   - verificación.
3. Compuertas (§18 del plan):
   - build sin errores;
   - las dos suites en verde;
   - has-pending-model-changes limpio;
   - yarn build con código 0;
   - yarn test en verde (guardias incluidas);
   - yarn lint con igual o menos errores que la línea base y cero en archivos nuevos.
4. Prueba manual corta contra la API local (http://localhost:5281/api/v1), si tu fase cambia endpoints. Usa un usuario de prueba de la base local y no escribas su contraseña.
5. Marca el estado de tu fase en el plan (tabla §17, columna nueva «Estado» o nota bajo la fila) y en docs/planes/README.md («En ejecución», o «Ejecutado» al terminar la fase 13).
   - En la fase 12, además, los documentos de §15.4.
   - En la fase 13, el informe de staging.

## Trampas conocidas
- dotnet build: si falla por rutas bin/Debug/net10.0/bin/... anidadas, borra bin/ y obj/ de los proyectos y compila incremental. No uses --no-incremental en paralelo.
- zsh:
  - patrones sin comillas en --include=*.cs fallan con «no matches found»: usa '*.cs';
  - un grep $(...) con la sustitución vacía lee stdin y se cuelga: pasa </dev/null.
- ASP.NET suma los [Authorize] (AND): para aflojar una acción de un controlador restringido hay que moverla de controlador.
- EF:
  - una entidad nueva descubierta por la navegación de un padre rastreado queda Modified y falla al guardar: usa Set.Add(...);
  - un DTO con AsNoTracking que lee una navegación sin Include revienta;
  - EF no refresca una entidad ya rastreada al volver a consultarla: en la fase 2, bloquea antes de la primera carga.
- La suite de integración comparte base y la cola de báscula corta en 100 camiones: libera los camiones que abra una prueba.
- ServiceRecord.CargoManifestNumber es la carta porte, no el manifiesto.
- Fase 11: agregar un paquete NuGet es un cambio de dependencias permitido solo para QRCoder (D39). Fija la versión exacta y no agregues otros. Si no restaura o no funciona, detente y pregunta.
- El volumen distingue mayúsculas: app/features/Administration y administration conviven.

## Entrega y detención
Al terminar, detente y entrega en el chat:
1. Fase y hashes de partida (BE y FE).
2. Archivos creados, modificados y borrados, por repo.
3. Migración generada (nombre) y resultado de has-pending-model-changes.
4. Pruebas: conteos antes y después (Wms.Tests, Wms.IntegrationTests, Vitest) y errores de lint antes y después.
5. Desviaciones del plan, cada una con la decisión Dn aplicada o la pregunta pendiente.
6. Lo que viste fuera de alcance, sin tocarlo.
7. El mensaje de commit propuesto para cada repo (el del §17 del plan, ajustado).

No sigas con la fase siguiente. El usuario hace el commit y abre otra sesión.
```
