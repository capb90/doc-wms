# Plan cerrado — Corrección de DEF-F11-029, 031, 032 y 033 antes de la fase 13

> **Fecha:** 25 de octubre de 2026. **Estado:** Ejecutado el 2026-10-25 y commiteado (BE `3cbf181`, docs `58dcbd5`); aprobado por el usuario el 2026-10-25. Ejecución y desviaciones en el §6. Prompt del ejecutor: `archivo/prompts/qa/prompt-def-f11-029-031-032-033.md` (archivado tras el commit).
> **Origen:** los 4 defectos menores abiertos de la ronda QA de preproducción (`qa/resultados/PRE-informe-2026-10-25.md` §6). El usuario pidió corregirlos antes de la fase 13 del plan de brechas P1.
> **Base:** BE `develop` `390eb0e` · FE `develop` `83a0af0`.
> **Alcance:** solo backend. Una fase, sin migración y sin cambios de permisos.
> **Rutas:** relativas a `code_workspace/`. Prefijos: `B/` = `Backend/wms-api/`; `D/` = `docs/`.

---

## 0. Instrucciones para el ejecutor

1. Lee `B/AGENTS.md`, `D/contexto/convenciones-tecnicas.md` y las cuatro fichas: `D/qa/resultados/defectos/DEF-F11-029.md`, `031`, `032` y `033`.
2. Trabaja en `develop`, sin ramas ni commits (`DEC-003`). Al terminar, te detienes y entregas el resumen y el mensaje de commit.
3. **Sin migración:** `dotnet ef migrations has-pending-model-changes` debe seguir limpio. Si deja de estarlo, detente.
4. Si el código no coincide con lo que dice el plan, detente y pregunta, con todas las dudas en un solo mensaje.

---

## 1. Decisiones

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **DEF-F11-029:** se dejan de enviar dos avisos en tiempo real: «WeighingCaptured» (cada pesaje) y «WeighbridgeCycleCompleted» (ciclo completado, en `RecordWeighingHandler` y `CompleteCycleHandler`). Llevan el GUID del ciclo, van en inglés y ninguna pantalla los usa para refrescar datos: el frontend solo los muestra como aviso emergente (`Frontend/wms/app/features/users/composables/useNotifications.ts:68-77`), y la trazabilidad escucha solo `TraceabilityUpdated` (`features/traceability/composables/useTraceabilityDashboard.ts:57-58`). El aviso «PerishableFlowClosed», que ya trae un texto en español con la placa, se conserva con el título en español «Flujo de perecederos cerrado» | Ficha DEF-F11-029 («o no mostrar este evento como aviso emergente»); plan maestro QA §10, mensajes en español |
| D2 | **DEF-F11-031:** las cantidades de la tabla Ampara / Saldo de la etiqueta se imprimen con la utilidad común `QuantityDisplay.Quantity` (`#,##0.##`, cultura es-CO), en todas las celdas: Ampara consolidado, Ampara por fila, Saldo y la fila vacía. Así un 50,0000 sale «50», un 48,00 sale «48» y un 12,5 sale «12,5», con un formato único en toda la tabla | `B/Wms.Application/Common/Formatting/QuantityDisplay.cs:15`; la ficha pide el mismo formato en toda la tabla |
| D3 | **DEF-F11-032:**<br>• El asunto de los correos de aviso por rol se arma con la **primera oración completa**: el texto hasta el primer «. » (punto seguido de espacio) o el final, recortado a 100 caracteres con «…». Ya no se corta en el primer punto, que cortaba `operario.bascula` o `12.000,00`.<br>• Las fechas del cuerpo de todos los correos de `NotificationService` van en hora de Colombia (`ColombiaTime.Now`) con el rótulo «(hora Colombia)», en lugar de `UtcNow … UTC` | Ficha DEF-F11-032; convenciones §2 (`ColombiaTime`) |
| D4 | **DEF-F11-033:**<br>• Validador nuevo de FluentValidation para `CreateWarehouseLocationCommand`, con las reglas y los mensajes que ya tiene el dominio (`WarehouseLocation.Create`): código y nombre requeridos y capacidad mayor que cero. Agrega los largos de la columna: código 50, nombre 200 y pasillo, rack y nivel 50.<br>• El handler deja de llamar `Trim()` sobre un código nulo.<br>• Con el cuerpo `{}`, la respuesta es 400 con el mensaje en español, no 500 | `B/Wms.Domain/Entities/Warehouse/WarehouseLocation.cs:37-49`; `B/Wms.Infrastructure/Persistence/Configurations/Warehouse/WarehouseLocationConfiguration.cs:15-20` |
| D5 | Fuera de alcance:<br>• el nombre del rol en inglés del asunto («[Admin]») y del cuerpo, y el «[Users]» de BR-08-009;<br>• los MINOR del selector de conductor (DEF-F11-023, 024 y 026);<br>• las observaciones del §7 del informe de preproducción | Alcance pedido: los 4 defectos |

---

## 2. Cambios

### 2.1 DEF-F11-029: avisos técnicos de báscula (D1)

- **`B/Wms.Application/Weighbridge/Commands/Common/RecordWeighing/RecordWeighingHandler.cs`:**
  - se borran `NotifyWeighingCapturedAsync` (`:543-562`) y sus 7 llamadas (`:260`, `:283`, `:298`, `:323`, `:410`, `:427`, `:483`);
  - se borra `NotifyCycleCompletedAsync` (`:564-578`) con sus llamadas.
- **`B/Wms.Application/Weighbridge/Commands/Common/CompleteCycle/CompleteCycleHandler.cs`:** se borra `NotifyCycleCompletedAsync` (`:320-335`) con sus llamadas.
- **`B/Wms.Application/Weighbridge/Commands/Storage/GenerateGlobalGuide/GenerateGlobalDispatchGuideHandler.cs:104`:** `Title = "Flujo de perecederos cerrado"`.
- **Comprobación:** si `realtimeNotifier` queda sin uso en un handler, se quita del constructor y de su registro, sin tocar a los demás. El grep de `"WeighingCaptured"` y `"WeighbridgeCycleCompleted"` en `B/` y en `Frontend/wms/app` debe salir vacío.

### 2.2 DEF-F11-031: cantidades de la etiqueta (D2)

- **`B/Wms.Application/ForeignTrade/Common/Services/LabelGenerationService.cs`,** en `AddProductRows`: `:704`, `:721`, `:732` y `:736` pasan de `$"{valor}"` a `QuantityDisplay.Quantity(valor)`.
- Se revisan con grep las otras tablas Ampara / Saldo del archivo (`:156`, `:382`, `:604`). Si imprimen cantidades sin formato, se usa el mismo cambio.

### 2.3 DEF-F11-032: asunto y hora de los correos (D3)

- **Nuevo** `B/Wms.Infrastructure/Services/NotificationEmailFormat.cs`, puro:
  - `Subject(string icon, string roleCode, string message)` → `"{icon} [{roleCode}] {primeraOración}"`, con la regla de D3;
  - `Timestamp()` → `"{ColombiaTime.Now:dd/MM/yyyy HH:mm} (hora Colombia)"`.
- **`B/Wms.Infrastructure/Services/NotificationService.cs`:**
  - `:547` usa `NotificationEmailFormat.Subject`;
  - `:124`, `:201`, `:298`, `:403`, `:490` y `:594` usan `NotificationEmailFormat.Timestamp()`;
  - un grep de `UTC</` y de `UtcNow:dd` en el archivo debe salir vacío.

### 2.4 DEF-F11-033: validación de la ubicación (D4)

- **Nuevo** `B/Wms.Application/Warehouse/Commands/Location/CreateWarehouseLocation/CreateWarehouseLocationValidator.cs`, con estas reglas y mensajes:

  | Campo | Regla | Mensaje |
  | --- | --- | --- |
  | `Code` | `NotEmpty` | «El código de ubicación es requerido.» |
  | `Code` | `MaximumLength(50)` | «El código no puede superar 50 caracteres.» |
  | `Name` | `NotEmpty` | «El nombre de ubicación es requerido.» |
  | `Name` | `MaximumLength(200)` | — |
  | `Capacity` | `GreaterThan(0)` | «La capacidad debe ser mayor a cero.» |
  | `Aisle`, `Rack`, `Level` | `MaximumLength(50)` cuando vienen | — |

  Lo registra el ensamblado, como los demás validadores (verificarlo en `B/Wms.Application/DependencyInjection.cs`).
- **`CreateWarehouseLocationHandler.cs`:** compara con `request.Code.Trim()` solo después de la validación, sin cambiar su lógica. La normalización la hace ya el dominio en `Create`.

---

## 3. Pruebas

| Proyecto | Prueba | Escenario |
| --- | --- | --- |
| `Wms.Tests` | **Nuevo** `B/Wms.Tests/Notifications/NotificationEmailFormatTests.cs` | `«El usuario operario.bascula modificó el pesaje #2. Peso original: 12.000,00 kg»` → asunto `«… El usuario operario.bascula modificó el pesaje #2»`; un mensaje sin «. » queda completo; uno de más de 100 caracteres termina en «…»; `Timestamp()` termina en «(hora Colombia)» |
| `Wms.Tests` | **Nuevo** `B/Wms.Tests/Warehouse/CreateWarehouseLocationValidatorTests.cs` | `{}` falla con los mensajes de código, nombre y capacidad; un comando válido pasa; un código de 51 caracteres falla |
| `Wms.IntegrationTests` | Prueba de API nueva junto a las de ubicaciones (o **Nuevo** `B/Wms.IntegrationTests/Warehouse/CreateLocationValidationTests.cs`) | `POST warehouse/locations` con `{}` como Admin → 400 con «El código de ubicación es requerido.»; con un cuerpo válido → 201 |
| `Wms.IntegrationTests` | Si la factoría registra un doble del notificador en tiempo real | Registrar un pesaje no envía avisos con el título «WeighingCaptured». Si no hay doble, basta el grep del §2.1 |
| Manual | `pdftotext -layout` de la etiqueta de un depósito con levante parcial | «Ampara 50 · Saldo 48» con el mismo formato |

Se re-ejecutan en local, sobre `wms_qa_preprod` (que conserva los datos de la ronda), con el sumidero SMTP:

- **B1/B7 de la ronda:** con un pesaje, CE y Admin ya no ven avisos emergentes técnicos;
- **FB-BAK-007:** asunto completo y hora de Colombia en el correo;
- **PRE-B6-03:** la ubicación sin código responde 400;
- **E2E-02, paso 4:** la etiqueta.

Las fichas pasan a «Corregido» con el commit y luego a «Verificado» en el re-test.

---

## 4. Compuertas y entrega

- `dotnet build Wms.sln` sin errores.
- `dotnet test Wms.Tests` y `dotnet test Wms.IntegrationTests` en verde, salvo las 2 fallas conocidas de la línea base (`InitiateCustomerIdTests.Queue_PendingService_ReturnsCustomerId` y `DiscardOperationTests.Discard_ReleasesTruckToNotStarted`).
- `has-pending-model-changes` limpio.
- El frontend no cambia; si se tocara, también `yarn build`, `yarn test` y `yarn lint`.
- **Documentación:**
  - las 4 fichas (historial y estado);
  - `D/qa/resultados/defectos/INDICE.md`;
  - un anexo en `D/qa/resultados/PRE-informe-2026-10-25.md` con el re-test;
  - este plan y `D/planes/README.md`.
- **Commit sugerido (BE):** `fix: avisos técnicos de báscula retirados, cantidades de la etiqueta, asunto y hora de los correos, y validación de ubicaciones (DEF-F11-029, 031, 032 y 033)`.

---

## 5. Riesgos

| Riesgo | Mitigación |
| --- | --- |
| Alguien usaba el aviso del pesaje para enterarse de que un camión pasó por báscula | No hay consumidor en el código. La cola, la trazabilidad y el detalle del depósito siguen mostrando el estado. Si el negocio lo echa de menos, se reintroduce traducido y con la placa |
| Un asunto de correo cambia de forma | Solo el texto: los destinatarios y el canal no cambian |
| Las etiquetas impresas antes muestran otro formato | Es cosmético; las etiquetas nuevas salen con el formato único |

---

## 6. Ejecución (2026-10-25)

- **Base:** BE `390eb0e` · FE `83a0af0`. Cambios sin commit, solo en el backend. Sin migración ni cambios de permisos.
- **Compuertas:**
  - `dotnet build Wms.sln`: sin errores;
  - `Wms.Tests`: 2016/2016;
  - `Wms.IntegrationTests`: 433/435, con solo las 2 fallas de la línea base, que pasan al correrlas solas;
  - `has-pending-model-changes`: limpio.
- **Re-test local** sobre `wms_qa_preprod`: B1/B7, FB-BAK-007, PRE-B6-03 y E2E-02 paso 4 en PASA. Detalle en `qa/resultados/PRE-informe-2026-10-25.md` §12; evidencia en `qa/resultados/evidencias/PRE/pre-retest-def-f11-029-033.txt`.
- **Fichas:** las cuatro quedaron en «Corregido (pendiente de commit)» y pasaron a «Verificado» con el commit del backend (`3cbf181`), como pide el prompt del ejecutor; el §3 decía el orden inverso.

### 6.1 Desviaciones y precisiones

| # | Punto | Qué se hizo | Motivo |
|---|---|---|---|
| X1 | D3, asunto | Además de cortar en el primer «. », se quitan los puntos finales de la oración | El mensaje real de la corrección de peso dice «… del ciclo a329eccf... Peso original…». Con el corte literal, el asunto terminaba en «a329eccf..». Prueba: `Subject_WeighingCorrectionMessage_DropsTrailingEllipsis` |
| X2 | §2.4, mensajes «—» | Los largos de nombre, pasillo, rack y nivel llevan mensaje en español («El nombre no puede superar 200 caracteres.», …) | Sin mensaje propio, FluentValidation responde con el nombre de la propiedad en inglés |
| X3 | §2.4, handler | El handler normaliza el código en una variable (`request.Code?.Trim() ?? ""`) antes de la consulta | Ante un comando sin código que no pase por el validador, el dominio responde el 400 y la consulta ya no revienta. Con el validador, el handler ni se alcanza |
| X4 | §3, doble del notificador | No se escribió la prueba de integración del aviso | `WmsApiFactory` no registra un doble de `IRealtimeNotifier`; el grep del §2.1 sale vacío |
| X5 | §3, re-test | Se hizo por API, con cuentas nuevas `qa.rt.*` y un cliente SignalR. Para la base se usó un rol temporal (`qa_rt_029`), que ya se eliminó | Las claves de las cuentas `qa.pre.*` solo están en el scratchpad de la ronda, y la cadena de conexión local no se lee (`.env` y secretos de usuario) |
| X6 | E2E-02 paso 4 | La etiqueta de `2026BA00003` sale «98 · 0» porque el depósito se despachó entero después de la ronda. El caso con saldo se vio en `2026BA00040`, `2026BA00021`, `2026BA00004` y el migrado `2023BA00019` | No había un estado intermedio que reimprimir |

