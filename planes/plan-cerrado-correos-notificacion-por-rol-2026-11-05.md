# Plan cerrado — Correos de notificación al correo de los usuarios del rol

> **Fecha:** 5 de noviembre de 2026. **Estado:** Aprobado por el usuario el 2026-11-05 (con N2 como está: la lista queda de respaldo). Pendiente de ejecución. Prompt del ejecutor: `planes/prompt-correos-notificacion-por-rol-2026-11-05.md`.
> **Origen:** pedido del usuario del 2026-11-05. En staging, al modificar un pesaje en báscula, el aviso por correo llegó a `capb.dev@gmail.com`, y el usuario esperaba que llegara al correo del administrador que tiene configurado en la aplicación.
> **Problema:**
> - Los avisos por correo no usan el correo de los usuarios. `NotificationOrchestrator.NotifyRoleAsync` (`B/Wms.Api/Services/NotificationOrchestrator.cs:69`) crea la notificación dentro de la aplicación para los usuarios activos del rol, pero para el correo solo pasa el nombre del rol a `NotificationService.NotifyRoleAsync`.
> - `NotificationService.NotifyRoleAsync` (`B/Wms.Infrastructure/Services/NotificationService.cs:517`) ignora el rol para elegir destinatarios y llama a `SendToAdminsAsync` (`:619`), que envía siempre a `Notifications:AdminEmails` (`:30`). En staging esa lista sale de `NOTIFICATIONS_ADMIN_EMAILS` en `deploy/staging/.env.staging` y se dejó en `capb.dev@gmail.com` (`planes/migracion-staging/resultados/informe-fase-2.md`, D4).
> - Cambiar el correo del usuario Admin en la aplicación no tiene efecto sobre estos avisos. Solo lo tiene sobre la recuperación de contraseña y el aviso de respaldo fallido (`BackupFailureMailer`).
>
> **Base:** BE `develop` `aa69633`; docs `main`.
> **Alcance:**
> - 2 fases: código, pruebas y documentación en local; despliegue y verificación en staging;
> - sin migración, sin cambios de permisos y sin cambios de frontend.
>
> **Rutas:** relativas a `code_workspace/`. Prefijos: `B/` = `Backend/wms-api/`; `D/` = `docs/`.

---

## 0. Instrucciones para el ejecutor

1. **Lee:** `B/AGENTS.md`, `D/contexto/convenciones-tecnicas.md`, de `D/contexto/decisiones.md` las `DEC-003`, `DEC-005` y `DEC-006`, y este plan completo.
2. **Git:** se trabaja en `develop` (BE) y en `main` de docs, sin ramas ni commits (`DEC-003`). Al cerrar cada fase te detienes con el resumen y los mensajes de commit.
3. **Antes de editar,** confirma con grep las rutas y las líneas citadas. Si el código no coincide, detente y pregunta con todas las dudas en un solo mensaje. Si un caso borde choca con una decisión de este plan, gana la decisión (`DEC-002`).
4. **Sin retrocesos** (`DEC-005`). Se conservan:
   - la notificación dentro de la aplicación (campana) para los usuarios del rol, que no cambia;
   - el aviso de respaldo fallido, con su regla propia (N4);
   - que un fallo del correo no rompe la operación que lo originó (los `try/catch` actuales).
5. **Credenciales:** no abras `.env*`, `deploy/staging/.env.*` ni `infra/terraform.tfvars`. No imprimas contraseñas ni tokens.
6. **Staging (fase 2):** antes de cada acción, una línea con lo que harás y el «sí» explícito del usuario (`DEC-006`).

---

## 1. Decisiones

| # | Decisión |
| --- | --- |
| N1 | **El correo de un aviso va a los correos de los usuarios activos del rol destino.** Se toman los de los mismos usuarios a los que el orquestador ya crea la notificación en la aplicación (`GetUsersInRoleAsync` + `IsActive`), con correo no vacío, sin repetir y sin distinguir mayúsculas. El rol destino es el `roleCode` que ya reciben los llamadores (`Admin`, `Billing`). |
| N2 | **`Notifications:AdminEmails` pasa a ser respaldo.** Se usa solo cuando el rol tiene usuarios activos pero ninguno con correo. Con usuarios con correo no se envían copias a la lista. *(A confirmar al aprobar el plan: la alternativa es que la lista reciba siempre copia, como complemento. Se descarta porque dejaría llegar a `capb.dev@gmail.com` los avisos que el usuario no espera allí.)* |
| N3 | **Si el rol no tiene usuarios activos, no se envía correo.** Se mantiene el `return` actual del orquestador (`NotificationOrchestrator.cs:83`). El respaldo de N2 no lo reemplaza. |
| N4 | **El aviso de respaldo fallido no cambia.** Sigue enviando a los Admin activos más `Notifications:AdminEmails`, sin repetir, aunque la base esté caída o `Notifications:Enabled` esté apagado (`BackupFailureMailer`, D32 y BR-08-001). |
| N5 | **`Notifications:Enabled=false` sigue apagando los avisos por correo,** igual que hoy (`NotificationService.cs:525`). |
| N6 | **Firma nueva.** `INotificationService.NotifyRoleAsync` recibe `IReadOnlyCollection<string> recipientEmails` además del rol. El orquestador resuelve los correos y se los pasa. `NotificationService` envía a esa lista y, si llega vacía, aplica el respaldo de N2. |
| N7 | **`NotifyUsersAsync` del orquestador** envía el correo a los correos de los usuarios que recibe, con el mismo respaldo. Hoy no tiene llamadores; se ajusta porque comparte la firma de N6. El asunto conserva «Users» como rol destino. |
| N8 | **Los métodos tipados** de `INotificationService` (`NotifyQuantityDiscrepancyAsync`, `NotifyLoadingCompletedAsync`, `NotifyManualEntryAsync`, `NotifyInventoryAdjustmentAsync`, `NotifyLowStockAsync`) no tienen llamadores. No se tocan y siguen enviando a `Notifications:AdminEmails`. |
| N9 | **Clase pura `NotificationRecipients`** en `B/Wms.Infrastructure/Services/`, junto a `NotificationEmailFormat`. `Resolve(roleEmails, configuredList)` devuelve los correos del rol sin repetir; si no queda ninguno, devuelve los de la lista de configuración. La lista admite coma o punto y coma como separador (hoy solo coma). Se prueba en `Wms.Tests`. |
| N10 | **La plantilla `deploy/staging/.env.staging.example` deja de traer un correo personal:** `ACME_EMAIL` y `NOTIFICATIONS_ADMIN_EMAILS` pasan a `CAMBIAR-EMAIL`, como el resto de sus valores. No se toca el `.env.staging` real. |
| N11 | **Sin migración, sin permisos nuevos, sin frontend.** El modelo de datos no cambia. |
| N12 | **Registro:** al cerrar, se agrega la decisión `DEC-070` (bloque nuevo `DEC-070…079`, Notificaciones) con N1 a N4 en `D/contexto/decisiones.md`. |

---

## 2. Qué cambia y dónde

### 2.1 Código (`B/`)

| Archivo | Cambio |
| --- | --- |
| `Wms.Infrastructure/Services/NotificationRecipients.cs` (nuevo) | N9. Clase estática pura, sin dependencias. |
| `Wms.Domain/Services/INotificationService.cs` | N6. `NotifyRoleAsync` agrega `recipientEmails`. |
| `Wms.Infrastructure/Services/NotificationService.cs` | N6. `NotifyRoleAsync` envía a `NotificationRecipients.Resolve(recipientEmails, config)` y no a `_adminEmails`. `SendToAdminsAsync` se conserva para N8. El análisis de `Notifications:AdminEmails` del constructor usa el mismo separador de N9. Si no hay destinatarios, avisa en el log y no envía. |
| `Wms.Api/Services/NotificationOrchestrator.cs` | N1, N6 y N7. En `NotifyRoleAsync` toma `Email` de `usersInRole` activos. En `NotifyUsersAsync` toma los correos de los `userIds` desde `AppDbContext`. |
| `deploy/staging/.env.staging.example` | N10. Líneas 13 y 36. |

Los 7 llamadores con `sendEmail: true` no cambian de código, porque conservan la misma firma de `INotificationOrchestrator`: `ModifyFirstWeightHandler`, `ModifySecondWeightHandler`, `ModifyWeighingDateHandler`, `ValidateDepositCommandHandler`, `ExecuteLoadingOrderCommandHandler`, `CreateReceptionWithoutWeighbridgeCommandHandler` y `BillingJobService` (rol `Billing`).

### 2.2 Pruebas

| Archivo | Casos |
| --- | --- |
| `Wms.Tests/Notifications/NotificationRecipientsTests.cs` (nuevo) | 1) correos del rol repetidos con otra capitalización salen una sola vez; 2) espacios y valores nulos o vacíos se ignoran; 3) con correos del rol, la lista de configuración no se usa; 4) sin correos del rol, se usa la lista; 5) la lista admite coma y punto y coma; 6) todo vacío devuelve lista vacía. |
| `Wms.IntegrationTests/Notifications/RoleEmailRecipientsTests.cs` (nuevo; carpeta por confirmar con grep) | Con `InMemoryEmailService`: 1) con `Notifications:AdminEmails` = otro correo y un Admin activo con correo, modificar el primer peso envía un solo correo, al Admin y no a la lista; 2) con el Admin sin correo, el envío va a la lista; 3) con `Notifications:Enabled=false`, no se envía nada; 4) un Admin inactivo no recibe el correo. |

### 2.3 Documentación (`D/`)

- `contexto/decisiones.md`: `DEC-070` (N12) y la fila del bloque nuevo en la tabla de bloques.
- `contexto/convenciones-tecnicas.md`: en la sección de servicios y jobs, una línea con la regla de destinatarios de los avisos por correo.
- `procesos/despliegue-staging.md`: junto al «Correo de fallo», aclarar que `NOTIFICATIONS_ADMIN_EMAILS` es solo respaldo de los avisos y que el correo que cuenta es el de cada usuario.
- `contexto/estado.md` y `planes/README.md`: estado del plan.

---

## 3. Fases

| Fase | Contenido | Estado |
| --- | --- | --- |
| 1 | Código, pruebas y documentación en local (§2) | Pendiente |
| 2 | Despliegue y verificación en staging, con aprobación explícita | Pendiente |

### Fase 1 — Local

1. Crear `NotificationRecipients` y sus pruebas unitarias.
2. Cambiar la firma de `INotificationService` y `NotificationService`.
3. Ajustar `NotificationOrchestrator` (N1, N7).
4. Cambiar la plantilla `.env.staging.example` (N10).
5. Escribir las pruebas de integración de §2.2.
6. Actualizar la documentación de §2.3.

**Criterio de salida:**
- `dotnet build Wms.sln` sin errores;
- `dotnet test Wms.Tests` y `dotnet test Wms.IntegrationTests` en verde, con las cifras antes y después;
- `dotnet ef migrations has-pending-model-changes` limpio (no hay migración);
- se entrega el resumen y los mensajes de commit. El agente no hace `git add` ni `commit`.

### Fase 2 — Staging

Solo con el «sí» explícito del usuario, paso a paso (`DEC-006`).

1. **Antes de desplegar:** el usuario confirma el correo de cada usuario Admin activo de staging, porque a ese correo llegarán los avisos. Si el Admin tiene `capb.dev@gmail.com` o un alias suyo, el usuario seguirá recibiéndolos, y es lo esperado.
2. Redesplegar el backend con `scripts/deploy-staging.sh` (`deploy/staging/README.md`).
3. **Verificación:** modificar un peso en báscula y comprobar que el correo llega a los Admin activos y no a una dirección que no sea de un Admin.
4. No hace falta cambiar `NOTIFICATIONS_ADMIN_EMAILS` en el servidor. Queda como respaldo.

**Criterio de salida:** el correo del cambio de peso llega solo a los correos de los Admin activos, y el estado queda en `contexto/estado.md`.

---

## 4. Riesgos

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R1 | Los avisos del job de facturación (rol `Billing`) hoy llegan a la lista de configuración. Pasan a los usuarios de Facturación activos con correo. | Es el efecto buscado por N1. Se avisa en el resumen de la fase 1. |
| R2 | Un Admin sin correo no recibe el aviso. | N2 cubre el caso con la lista de respaldo. |
| R3 | Más destinatarios si hay varios Admin activos (`DEC-043`). | Cada Admin recibe un solo correo. Si molesta, se apaga con `Notifications:Enabled=false`, que apaga todos los avisos. |
| R4 | En producción los correos de los usuarios serán reales y los avisos incluyen datos operativos (peso, razón del cambio, ciclo). | Los reciben solo los usuarios del rol que ya ven esos datos en la aplicación. |
| R5 | Un envío fallido no debe afectar la operación. | Se conservan los `try/catch` de `NotificationService` y del orquestador. |

---

## 5. Fuera de alcance

- Preferencias de cada usuario sobre qué avisos recibir por correo.
- Avisos por WhatsApp o dentro de la aplicación para los operarios (aplazados, `contexto/estado.md`).
- Los métodos tipados de N8, mientras no tengan llamadores.
- Cualquier cambio al `.env.staging` real.

---

## 6. Mensajes de commit propuestos

- **BE, fase 1:** `fix(notificaciones): los avisos por correo van a los usuarios activos del rol, y Notifications:AdminEmails queda como respaldo (DEC-070)`
- **Docs, fase 1:** `docs(notificaciones): DEC-070 y plan de correos por rol`
