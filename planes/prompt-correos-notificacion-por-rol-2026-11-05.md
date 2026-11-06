# Prompt — Correos de notificación al correo de los usuarios del rol, fase 1

> **Cómo usarlo:**
> 1. Abre una sesión nueva de Claude Code en `code_workspace/Backend/wms-api` y agrega `docs` como directorio adicional.
> 2. Copia el bloque de abajo.
> 3. Al terminar, el agente entrega el resumen y los mensajes de commit. Tú haces los commits (`DEC-003`).
> 4. Este prompt cubre solo la fase 1. La fase 2 (staging) se pide aparte, en una sesión con el plan abierto y con tu «sí» en cada paso (`DEC-006`).
>
> **Plan:** `docs/planes/plan-cerrado-correos-notificacion-por-rol-2026-11-05.md`, aprobado el 2026-11-05.
> **Modelo recomendado:** Sonnet 5.5 para la fase 1; Opus 5.5 si se prefiere más margen en la fase 2.
>
> Cuando se hagan los commits de la fase 2, este prompt se mueve a `docs/archivo/prompts/`.

---

```text
FASE = 1

Eres el ejecutor de la fase indicada arriba del plan cerrado «Correos de notificación al correo de los usuarios del rol» del WMS de Bodegas Asociadas. El plan está aprobado: impleméntalo tal como está, sin rediseñarlo. Ejecutas SOLO esa fase.

## Rutas
- Raíz: /Volumes/Dock/Projects/bodegas_asociadas/code_workspace. Las rutas son relativas a ella.
- Backend: Backend/wms-api (rama develop). Hub de documentación: docs/ (rama main).

## Lee primero
1. docs/README.md y Backend/wms-api/AGENTS.md.
2. docs/planes/plan-cerrado-correos-notificacion-por-rol-2026-11-05.md completo: §0 (instrucciones), §1 (decisiones N1–N12, que mandan sobre el resto), §2 (qué cambia), la sección de tu fase en §3 y §4 (riesgos).
3. docs/contexto/convenciones-tecnicas.md y, de docs/contexto/decisiones.md, DEC-002, DEC-003, DEC-005 y DEC-006.

## Qué haces en la fase 1
Sigue el orden de §3, «Fase 1»:
1. Crear `NotificationRecipients` (N9) y sus pruebas unitarias en Wms.Tests/Notifications.
2. Cambiar la firma de `INotificationService.NotifyRoleAsync` y `NotificationService` (N6).
3. Ajustar `NotificationOrchestrator` en NotifyRoleAsync y NotifyUsersAsync (N1, N7), conservando el `return` cuando el rol no tiene usuarios activos (N3).
4. Cambiar `deploy/staging/.env.staging.example`: ACME_EMAIL y NOTIFICATIONS_ADMIN_EMAILS pasan a CAMBIAR-EMAIL (N10).
5. Escribir las pruebas de integración de §2.2. Confirma con grep la carpeta y cómo `WmsApiFactory` fija `Notifications:AdminEmails` y `Notifications:Enabled`.
6. Actualizar la documentación de §2.3: DEC-070 con su fila de bloque, convenciones-tecnicas, despliegue-staging, estado.md y planes/README.md.

## Reglas
- Antes de editar, confirma con grep las rutas y líneas del plan. Si el código no coincide, detente y pregunta, con todas las dudas en un solo mensaje.
- Si un caso borde choca con una decisión del plan, gana la decisión: aplícala y menciónalo en una línea, sin pedir aprobación (DEC-002).
- No hay migración. No cambies permisos ni frontend. No toques el aviso de respaldo fallido (N4) ni los métodos tipados (N8).
- Errores de negocio y mensajes en español; las reglas se extraen a clases puras y se prueban en Wms.Tests.
- No abras .env*, deploy/staging/.env.* ni infra/terraform.tfvars. No imprimas credenciales.
- Git: trabajas en develop (BE) y main (docs), sin ramas. NO ejecutes git add, commit, push ni merge. Para borrar usa rm.
- Staging y su despliegue NO son de esta fase.

## Criterio de salida
- `dotnet build Wms.sln` sin errores.
- `dotnet test Wms.Tests` y `dotnet test Wms.IntegrationTests` (necesita Docker) en verde. Informa las cifras antes y después. Sin Docker: `dotnet test --filter Category!=Integration`, y dilo.
- `dotnet ef migrations has-pending-model-changes` limpio (no debe haber migración).
- Actualiza el estado de la fase en el plan y en planes/README.md.

## Entrega
Al terminar, detente con:
1. Un resumen de lo hecho y de las cifras de pruebas.
2. Lo que no pudiste verificar.
3. Los mensajes de commit propuestos, uno por repo (BE y docs), tomados de §6 del plan.
4. Recuerda que el efecto en facturación (R1) y el correo de cada Admin de staging se confirman antes de la fase 2.
```
