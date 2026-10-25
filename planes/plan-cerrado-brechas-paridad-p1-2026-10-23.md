# Plan cerrado — Brechas P1 y decisiones DEC-050…054 de la auditoría de paridad

> **Fecha:** 23 de octubre de 2026. **Estado:** aprobado por el usuario el 2026-10-23. Lo implementa otro agente, una fase por sesión, con el prompt `planes/prompt-plan-brechas-paridad-p1-2026-10-23.md`.
> **Origen:**
> - `analisis/auditoria-paridad-integral-2026-10-23/06-brechas-priorizadas.md`, con las 13 brechas P1 abiertas y las 7 que se construyen por DEC-050…054.
> - Las fichas de cada brecha, en `analisis/auditoria-paridad-integral-2026-10-23/modulos/<NN>-<modulo>/08-brechas.md`.
> - Las respuestas del usuario del 2026-10-23: 13 preguntas al negocio (DEC-050…054) y 15 de diseño (§2).
> - Agregado el 2026-10-23, con el plan ya aprobado: el pedido del cliente de un **código QR de verificación en la guía de salida** (fase 11, D35–D42, `DEC-060`), con 4 respuestas del usuario.
> - Agregado el 2026-10-24, después de ejecutar las fases 1 a 12: la **fase 12c** (§15C, D43–D46), con los tres cambios de `DEC-055` y el ajuste del orden de bloqueo de las guías.
> - Agregado el 2026-10-25, durante la fase 12c: D47 y D48, respuestas del usuario a lo que el código no permitía (el índice de un precio activo por servicio y el precio de la guía).
>
> **Base (según `contexto/estado.md` §2):** backend `wms-api` `develop` `b27c9bf` · frontend `wms` `develop` `31da26c`.
> **Staging (último despliegue registrado):** BE `044be08` / FE `4ca4e0a`, con datos migrados.
> **Ejecutor:** un agente sin historial. Lee este plan completo antes de empezar.
> **Rutas:** relativas a `code_workspace/`. Prefijos: `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`; `T/` = `Frontend/wms/test/`; `L/` = `bodegas-legacy/`; `D/` = `docs/`; `FT/` = `B/Wms.Application/ForeignTrade/`; `WA/` = `B/Wms.Application/Weighbridge/`.

---

## 0. Instrucciones para el agente ejecutor

1. Lee primero:
   - `B/AGENTS.md` y `D/README.md`;
   - `D/contexto/decisiones.md`, en especial §6 (DEC-050…054);
   - `D/contexto/convenciones-tecnicas.md`, sobre todo las trampas de §10;
   - `D/procesos/flujo-de-trabajo-agentes.md`.
2. **Trabaja en `develop` de los dos repositorios.** No crees ramas ni hagas commits (`DEC-003`). Para borrar archivos usa `rm`.
3. **Ejecuta una fase por sesión y detente en su checkpoint** (§17) con un resumen:
   - archivos tocados;
   - pruebas antes y después;
   - errores de lint antes y después;
   - migraciones;
   - desviaciones.
4. **Este plan no deja decisiones abiertas** (§2). Si el código contradice el plan, no improvises: detente y pregunta, con todas las dudas en un solo mensaje. Si el texto choca con una decisión `Dn` en un caso borde, gana la decisión (`DEC-002`): aplícala y menciónala en una línea.
5. **Migraciones:** solo con `dotnet ef … --project Wms.Infrastructure --startup-project Wms.Api` y solo contra la base local (`DEC-004`). Nunca edites a mano los archivos generados. Este plan crea **cinco**, cada una en su fase: `AddStakeholderExitBlock` (3), `FixAgreementActiveStakeholderIndex` (7), `AddWarehouseStorageLegacyYear` (9), `AddGuideCodeTypeParameter` (11) y `RelaxServicePriceActiveIndex` (12c, D47). En las demás fases, `dotnet ef migrations has-pending-model-changes` debe salir limpio.
6. **Staging:** las fases 1 a 12 son locales. La fase 13 despliega a staging solo con la aprobación explícita del usuario, paso por paso. No abras `.env*` ni `deploy/staging/.env.*`.
7. **Reglas de código** (`D/contexto/convenciones-tecnicas.md`):
   - errores de negocio con `BadRequestException`, `ConflictException` o `NotFoundException`, con el mensaje en español;
   - fechas de negocio con `ColombiaTime`;
   - el autor sale del token (`GetRequiredUserId()`);
   - para listas completas, `all=true`;
   - auditoría genérica `IAuditable` → `audit_logs`, sin tablas propias;
   - las reglas van en clases puras, probadas en `Wms.Tests`;
   - lo que depende de EF, índices o transacciones se prueba en `Wms.IntegrationTests`.

---

## 1. Objetivo y alcance

**Objetivo:** cerrar, antes del corte real, las brechas que la auditoría de paridad del 2026-10-23 marcó como P1, construir lo que el usuario decidió en DEC-050…054 y agregar el código QR de verificación en la guía de salida que pidió el cliente.

**Incluye 20 brechas, 5 defectos colaterales y 1 funcionalidad nueva:**

| Grupo | Brechas | Fase |
| --- | --- | --- |
| Superficie de API y leyenda fiscal | BR-03-001, BR-03-002, BR-02-005 | 1 |
| Concurrencia y guardas de la orden | BR-05-002, BR-05-001 | 2 |
| Guía y marca «sin salidas» | BR-05-006, BR-05-004, colateral C3 | 3 |
| Báscula: corrección y «Solo báscula» | BR-02-006, BR-02-002 | 4 |
| Báscula: un pesaje para varios documentos | BR-02-013, colateral C4 | 5 |
| Facturación: tarifa faltante, precio futuro y renovación | BR-06-004, C5 (`Service.SetPrice`), BR-06-005 | 6 |
| Facturación: convenios programados y depósitos pendientes | BR-06-001, colaterales C1 y C2, BR-06-003 | 7 |
| Reportes | BR-07-003, BR-07-002; de paso BR-07-001, BR-07-004 (colateral) y la parte de `footerLines` de BR-07-005 | 8 |
| Migración legacy | BR-08-005, BR-08-003 | 9 |
| Respaldos | BR-08-001 (código y procedimiento) | 10 |
| Guía de salida con código QR (funcionalidad nueva, pedido del cliente) | QR de verificación seleccionable por parámetro; el código de barras se conserva | 11 |
| Documentación y QA | BR-08-004 (procedimiento de corte), casos QA, fichas, estado | 12 |
| Ajustes tras la ejecución (`DEC-055`) | Depósito agotado en la gracia, orden de bloqueo de las guías, precios de servicio programados | 12c |
| Staging | Despliegue y QA en staging, con aprobación | 13 |

**Defectos colaterales incluidos** (D1). Los encontró la investigación del 2026-10-23 y no estaban en el registro:

| ID | Defecto | Evidencia |
| --- | --- | --- |
| C1 | El índice único «un convenio activo por cliente» nunca aplica: filtra `status = 'ACTIVE'` y el estado se guarda `'Active'` | `B/Wms.Infrastructure/Persistence/Configurations/Agreement/AgreementConfiguration.cs:28-30,53-56` (verificado) |
| C2 | Convenio «Programado» aceptado sin fecha; el formulario rotula «(Opcional)» la fecha que exige; las fechas se comparan en UTC | `CreateAgreementValidator.cs`, `Agreement.cs:36,46-67`, `F/features/agreements/components/AgreementForm.vue:174-181` |
| C3 | La guía de un solo cliente con otro destinatario no valida la mora de los dueños | `FT/Commands/CreateDispatchGuide/CreateDispatchGuideCommandHandler.cs:178-181` |
| C4 | La pantalla de báscula no imprime el tiquete de los depósitos adicionales | `F/features/weighbridge/composables/useTicketPdf.ts:81-98` (sin consumidores); `F/pages/operations/weighbridge/index.vue:1287` |
| C5 | `Service.SetPrice` vence el precio vigente al registrar uno futuro y deja días sin tarifa | `B/Wms.Domain/Entities/Service/Service.cs:56-63` |

**Fuera de alcance:**

- Las brechas P2 y P3 del registro, salvo lo que se arregla de paso y se dice en cada fase. Entre ellas, BR-02-007, BR-05-005, BR-05-013, BR-06-013 y BR-08-002. Las fases 2 y 8 tocan los mismos archivos, pero no las resuelven.
- La migración de `cliente.sinsalidas`: la marca se pone a mano después del corte (D9).
- La vigencia final de los convenios (D20).
- El código de barras del PDF del depósito y de la etiqueta: siguen como están (D35).
- La deduplicación de la notificación de fallo del job de facturación.
- La salida de báscula sin orden de cargue y la edición del registro guardado en báscula: se mantienen como están (DEC-050).

---

## 2. Decisiones

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | El alcance son las 20 brechas del §1 **más** los colaterales C1–C5 | Usuario, 2026-10-23 (pregunta 15) |
| D2 | **BR-03-001:** se retira `PATCH entry-logs/{id}` con su comando, handler y validador, y `EntryLog.AssignEntryReason` si queda sin llamadores. No se le aplican guardas: sus funciones ya tienen camino propio (`weighbridge/entry-log/{id}/info`, la corrección WMS-5) | Sin consumidores (`F/features/entries/services/entry-service.ts:34-40` no se llama; herramientas de video tampoco); DEC-005 no se afecta |
| D3 | **BR-03-002:** se retira `POST warehouse/loading-orders` con sus requests y el composable de frontend sin uso. **Se conserva** `PATCH warehouse/loading-orders/{id}/cancel`, que Bodega sí usa | Sin consumidores (`F/features/warehouse/composables/useLoadingOrderMutations.ts:25-46`); DEC-005; DEC-016 |
| D4 | **BR-02-005:** la leyenda «Numeración autorizada y/o habilitada por la DIAN» se reemplaza por textos que dicen que el documento no es fiscal:<br>• **Tiquete:** «Documento interno de control de pesaje. No es una factura de venta.»<br>• **PDF interno de la factura:** «Documento interno de control. La factura electrónica de venta es la que expide la empresa en SIIGO.»<br>Los dos textos van en constantes de una clase `DocumentLegends` | Usuario (pregunta 2); DEC-024 |
| D5 | **BR-05-002:** bloqueo pesimista con `SELECT … FOR UPDATE`, con el patrón de `EntryLogLock`. El orden global de bloqueo es fijo: `entry_logs` → `loading_orders` → `warehouse_storage_products` (`ORDER BY id`) → `document_sequences`. En cada handler, primero se abre la transacción, luego se bloquea, después se lee y se valida. **Sin** `xmin`, sin `Serializable` y sin `CHECK` en la base | Patrón del repo (`WA/Common/Services/EntryLogLock.cs:15-36`); `xmin` no detecta el *write skew* de los levantes |
| D6 | **BR-05-001:** cancelar o modificar los ítems de una orden con guía vigente responde 409 «Anule primero la guía {n} de la orden {OC}…», en CE y en Bodega. La cancelación **no** anula la guía sola | Precedente de revertir (`FT/Commands/RevertLoadingOrder/RevertLoadingOrderCommandHandler.cs:44-46`, F5-OC-018); DEC-016; DEC-052 |
| D7 | **BR-05-006:** la diferencia entre la guía y lo cargado se detecta al ejecutar el cargue. Ese es el único punto posible, porque D6 impide cambiar la orden si tiene guía vigente.<br>Si hay diferencia:<br>• se notifica en tiempo real al rol ForeignTrade (`ActionRequired`);<br>• se muestra una marca calculada «No coincide con lo cargado» en el historial de guías y en el detalle de la orden.<br>No hay estado nuevo ni columna, y no bloquea la salida | DEC-052 |
| D8 | **BR-05-004 (roles):** una política nueva, `ExitBlockAccess` (Admin, ForeignTrade, Billing), pone y quita la marca «sin salidas» con `PATCH stakeholder/{id}/exit-block`. Las dos operaciones exigen motivo y quedan auditadas | Usuario (pregunta 3); DEC-031 |
| D9 | **BR-05-004 (efecto):** la marca impide:<br>• crear una orden;<br>• agregar ítems a una orden;<br>• emitir la guía (se valida a todos los dueños);<br>• **ejecutar el cargue** en Bodega.<br>No bloquea ingresos, cobros, báscula ni la guía automática de exportación. La validación vive en un servicio propio, **no** en `ValidateFinancialStatusAsync`. No se migra del legacy | Usuario (preguntas 4 y 5); DEC-052; `ValidateFinancialStatusAsync` se usa en 14 sitios |
| D10 | **C3:** la guía valida la mora de **todos** los dueños de la orden, con cualquier destinatario | D1 |
| D11 | **BR-02-006:** `PATCH weighbridge/{id}/second-weight` acepta un `weighingId` opcional; sin él, corrige la secuencia 1, como hoy. Al corregir se recalcula el neto de las entradas cuyo par de pesajes incluye el corregido, con la clase pura `CycleNetWeights`. Si el ciclo tiene un solo pesaje, el neto queda nulo, como en la captura | Precedente WMS-33 D17 (`ModifyWeighingDateRequest.WeighingId`); `CompleteCycleHandler.cs:210-245` |
| D12 | **BR-02-002:** el cliente es opcional en «Solo báscula». La columna ya admite nulos: **no hay migración**.<br>• Sin cliente ni conductor, el destinatario predeterminado es el consumidor final.<br>• El tiquete muestra al destinatario no registrado.<br>• El historial muestra su nombre, y su filtro por cliente también mira la factura del ciclo (`wc.Invoice`) | DEC-050; `ServiceRecordConfiguration.cs:38` |
| D13 | **BR-02-013 (modo):** el operario elige con el tipo del segundo pesaje.<br>• **Tara:** un solo pesaje para todos los depósitos. Es la opción **predeterminada**.<br>• **Intermedio:** un pesaje por depósito, como hoy.<br>El modo se deduce de los datos; no hay columna. Después de un intermedio no hay modo mixto | DEC-050 |
| D14 | **BR-02-013 (neto):** con un solo pesaje, el neto del camión se reparte **en proporción al peso de manifiesto** de cada depósito: `round2(total × MWᵢ / ΣMW)`, y el último absorbe el residuo.<br>Si falta un manifiesto, el neto del grupo queda nulo y se reparte cuando Comercio Exterior completa el último.<br>Se reparte otra vez al corregir el bruto o la tara, y al completar un manifiesto, aunque el depósito ya esté validado. La observación de la validación conserva el valor de su momento | Usuario (pregunta 1, tras conocer que el legacy copiaba el total en cada documento) |
| D15 | **BR-02-013 (tiquete):** **un tiquete por depósito**. Cada uno lleva su consecutivo `2026T`, el mismo pesaje, su porción y la línea «Pesaje compartido por {N} depósitos · neto del camión {X} kg». Se conserva el índice único por entrada. El cobro no cambia: el primer depósito cobra y los adicionales van en $0 | Legacy, un recibo por documento (`registrarentradavariascp.php:217-258`); DEC-012; sin migración |
| D16 | **C4:** el paso de impresión de báscula imprime el tiquete de **cada** entrada del ciclo | D1 |
| D17 | **BR-06-004:** la resolución del servicio complementario sube a `ResolveStorageChargesAsync`, con el mismo respaldo que el cargo principal. Si su regla falla, la línea sale con el **mínimo del propio servicio complementario** en la modalidad (sin mínimo, en $0), con advertencia en el detalle y aviso a Facturación.<br>El respaldo del cargo principal también atrapa `NotSupportedException` y los importes negativos.<br>Al guardar una regla **no** se bloquea nada. El cálculo sigue existiendo una sola vez | DEC-020 («nunca bloquea»); DEC-027 |
| D18 | **C5:** `Service.SetPrice` vence los precios activos en `max(UtcNow, validFrom) − 1 tick`, no en `UtcNow` | Usuario (pregunta 9) |
| D19 | **BR-06-005:** la renovación, por job o por cierre manual, abre el período con la cantidad facturable **al cierre del día de inicio**. El corte es `ColombiaTime.StartOfDayUtc(S + 1)`: lo que sale el día S no se cobra.<br>La ventana empieza en `Min(último cierre, corte)`, así el cierre manual anticipado sigue igual.<br>`PER_CARGO_UNIT` y las fórmulas por contenedor también reconstruyen las unidades que había al corte, en la renovación y en el recálculo | Usuario (pregunta 10); DEC-053; DEC-028; DEC-025 (convenios reales por contenedor) |
| D20 | **BR-06-001:** el convenio «Programado» rige desde las 00:00 (Colombia) del día de su fecha.<br>• El resolutor ya lo considera vigente ese día, sin cambiar datos.<br>• Un job diario a las 00:00:30 lo deja `Active` y archiva el activo anterior del cliente.<br>• Sin vigencia final.<br>• Al activarse **no** recalcula facturas: avisa a Facturación.<br>• La fecha es de día, sin hora.<br>• Un convenio «Programado» sin fecha se rechaza (C2) | Usuario (preguntas 6, 7 y 8); legacy por fechas (`L/modulos/mod_convenios/registrarconvenio.php:57`) |
| D21 | **C1:** el filtro del índice pasa a `status = 'Active'` (migración `FixAgreementActiveStakeholderIndex`). Todo camino que active un convenio guarda primero el archivo del anterior (dos `SaveChanges` en una transacción). Antes de desplegar, se cuentan en staging, en solo lectura, los clientes con más de un convenio activo (§16.1); si hay alguno, se detiene y se pregunta | D1; el índice no es diferible |
| D22 | **BR-06-003:** «Depósitos pendientes» incluye los depósitos Confirmados o Cerrados con una factura de almacenamiento en Borrador **sin** N.º SIIGO (también las no fiscales) o anulada sin refacturar. Se agregan una columna «Pendiente» («Por numerar» / «Por refacturar») y un interruptor «Solo con facturas por numerar o refacturar». Un Borrador con N.º no cuenta | DEC-053 (literal) |
| D23 | **BR-07-003:** la fecha de ingreso es `WarehouseStorage.EntryDate ?? WarehouseStorage.CreatedAt` en:<br>• el kardex;<br>• el listado y el Excel de importaciones;<br>• de paso, los Excel de exportaciones e inspecciones y la columna «Fecha Ingreso» de los tres listados de Comercio Exterior | DEC-012 |
| D24 | **BR-07-002 (formato):** el diario de ingresos se agrupa por depósito, con agencia, importador, manifiesto DIAN y CPI.<br>• Lleva una fila por camión con manifiesto preimpreso, placa, fecha y hora, tiquete, planilla de envío, transportadora, embalaje, cantidad, **peso de manifiesto y peso neto de báscula**, y mercancía.<br>• Lleva subtotales por depósito, el total de vehículos y las firmas «Jefe de Bodega», «Recibí conforme DIAN» y «Firma Funcionario».<br>• Va en pantalla, PDF y Excel; el Excel es plano.<br>• Se omite «Planilla de recepción», que el legacy no llenaba | DEC-054; DEF-F7-004 (el neto de báscula se conserva) |
| D25 | **BR-07-002 (modalidad y fecha):**<br>• Filtro de modalidad, con Importación por defecto (IMP, EXP, INSP).<br>• El primer camión del depósito entra con la fecha de ingreso del depósito; los siguientes, con su ingreso en Vigilancia.<br>• Estados: Confirmado y Cerrado | Usuario (pregunta 11); DEC-012; DEC-010.4; `D/qa/00-plan-maestro.md:395` |
| D26 | **Equivalencias del diario** (sin pregunta):<br>• **CPI** = `ServiceRecord.CargoManifestNumber`, que es la carta porte;<br>• **manifiesto preimpreso** = `WarehouseStorageEntry.ManifestNumber`, que es el manifiesto del camión;<br>• **manifiesto DIAN** = `ImportWarehouseStorage.ManifestNumber`, nulo fuera de IMP;<br>• **peso** = `WarehouseStorageEntry.ManifestWeight` | `L/bodegas_schema.sql` (`ingreso.nro_manifiestodian`, `pesaje.nro_manifiestoemp`); trampa §10.9 |
| D27 | **BR-07-001:** los diarios de ingreso y de salida tienen botón «Exportar Excel». **BR-07-004 (C):** el kardex y el diario de salidas muestran el manifiesto DIAN (sin tomar como respaldo el del camión), y el kardex suma la agencia. Inventario, pólizas y CPI no cambian. **BR-07-005 (parcial):** `excel-export.ts` copia `footerLines` también en modo de una hoja | D1; la ficha de BR-07-004 confundía el manifiesto del camión con el DIAN |
| D28 | **BR-08-005:** el depósito legacy se identifica por número + año de `fecha_deposito`, en hora de Colombia. Nueva columna `WarehouseStorage.LegacyYear`. El índice único pasa a `(legacy_number, legacy_year)` con `NULLS NOT DISTINCT`. Los ya migrados se reconocen por el año de su `EntryDate`, sin relleno de datos. El CSV de levantes suma una columna opcional, `anio_deposito` | Criterio del legacy (`L/modulos/mod_depositos/listardepositos.php:103,109`); DEC-006 |
| D29 | **BR-08-003:** columna 22, opcional, `prorroga` en el CSV de depósitos. Con `1` en un depósito de importación, el importador llama `RegisterExtension`: plazo de 60 días y una segunda prórroga responde 409. En otra modalidad, se emite una advertencia y se ignora | `L/menus/evaluaabandonos.php:10-12` |
| D30 | **BR-08-004:** el corte congela un día la operación (D31). Se escribe un procedimiento con los conteos C1–C9, el tratamiento de cada tipo y la conciliación en cero | Usuario (pregunta 14) |
| D31 | Desde la hora T0, en el legacy solo se consulta y se cobra cartera. Todo lo abierto se termina antes o se rehace en V2 después de migrar | Usuario (pregunta 14) |
| D32 | **BR-08-001:** un correo de fallo de respaldo llega a los **usuarios Admin activos y a `Notifications:AdminEmails`**, sin repetir. Sale aunque la base esté caída: la lista de configuración no depende de ella | Usuario (pregunta 13) |
| D33 | **BR-08-001 (destino):** un bucket **privado** de Lightsail Object Storage, en otra región, configurado como destino S3 por API (DF3). Las credenciales van en `deploy/staging/.env.staging` (las pone el usuario) y se pasan a `compose.staging.yaml` como `Backups__S3Credentials__s3-externo__*` | Usuario (pregunta 12); `S3BackupTarget.cs:21-46` |
| D34 | Los defectos que salgan en QA siguen la serie `DEF-F11-028…`. Los casos nuevos continúan la numeración de cada bloque, según `D/qa/00-plan-maestro.md` §2.5 | `D/procesos/qa-y-defectos.md` |
| D35 | **QR en la guía:** el PDF de la guía de salida imprime un código QR **o** el código de barras actual, según la configuración. El código de barras (`GenerateCode39Barcode`) **no se borra ni se modifica**. El PDF del depósito no cambia | Pedido del cliente, 2026-10-23; `DEC-060` |
| D36 | **Dónde se elige:** el parámetro del sistema `GUIDE_CODE_TYPE` (`QR` o `BARCODE`), editable por el Admin en `admin/parameters`, sin desplegar y con auditoría. Un valor inactivo, vacío o desconocido equivale a `BARCODE`, y editarlo con otro valor responde 400 | Usuario, 2026-10-23; patrón CHG-84 (`CompanyInfoProvider`) |
| D37 | **Valor inicial: `QR`.** Como el PDF se genera en cada descarga, desde el despliegue las guías nuevas y las reimpresas salen con QR | Usuario, 2026-10-23 |
| D38 | **Contra la adulteración:** el QR lleva un enlace de verificación con un token firmado (HMAC-SHA256 truncado a 16 bytes sobre el Id de la guía), sin columna nueva. La clave sale de la configuración (`DispatchGuides:VerificationKey`). Sin clave en modo QR, el PDF sale con código de barras y se avisa a Admin: nunca se bloquea la impresión de una guía | Usuario, 2026-10-23 («enlace de verificación»); un QR con solo el número no evita la copia |
| D39 | **Generación:** con el paquete NuGet `QRCoder` (MIT, `PngByteQRCode`), versión fijada exacta. No se escribe un codificador propio | Sin librería QR en el repo (`Wms.Application.csproj:10-20`) |
| D40 | **Verificación pública:** endpoint sin sesión `GET api/v1/public/dispatch-guides/verify/{token}`, en un controlador propio, con un limitador de 30 peticiones por minuto y por IP, y una página pública `/verificar/guia/[token]` en el frontend. Un token inválido o alterado responde 404, con el mismo mensaje que una guía inexistente | Usuario, 2026-10-23; convenciones §4 (los `[Authorize]` se suman) |
| D41 | **Datos públicos mínimos:** número, empresa, fecha y hora de emisión y de salida, estado (vigente o anulada, con la fecha de anulación), depósito(s), destino, productos con cantidad y unidad, y la placa parcialmente oculta (3 caracteres y el resto con `•`). **Nunca** conductor, destinatario, cliente, documentos, teléfonos ni valores | Usuario, 2026-10-23; DEC-007 |
| D42 | La clave de verificación se genera por ambiente, la guarda el usuario fuera de git y no se rota salvo compromiso: rotarla invalida los QR ya impresos. `Frontend:BaseUrl` debe ser la URL pública real, porque queda impresa | DEC-007; `compose.staging.yaml:51` |
| D43 | **Depósito agotado en la gracia:** el cierre por agotamiento no cierra un período cuyo fin ya pasó. Lo deja abierto para que el job, o el cierre manual, lo renueve con la cantidad al cierre del día S (D19), y lo cierre por agotamiento en la misma transacción. No se renueva dentro de la transacción del cargue | Usuario, 2026-10-24 (`DEC-055`, precisa `DEC-053`); evita facturar dentro del cargue |
| D44 | **Orden de bloqueo de las guías:** las guías de importación y de exportación bloquean la orden y sus productos **antes** de tomar el consecutivo `S`, como manda D5. La de exportación pasa a bloquear también la orden | Usuario, 2026-10-24; D5 |
| D45 | **Precios programados:** `POST service/{id}/prices` acepta una vigencia futura, normalizada a las 00:00 de Colombia de ese día. El vigente rige hasta la víspera. La lista los muestra «Programado» (`IsScheduled`). Reemplaza la regla ALM-20/D20 del validador | Usuario, 2026-10-24 (`DEC-055`); `Service.SetPrice` (fase 6) |
| D46 | Registrar un precio deja inactivos los precios programados que empiezan después de él: es el comportamiento actual de `SetPrice` y `Expire`, y solo se documenta | Fase 6 (`ServicePrice.Expire`); registro de ejecución |
| D47 | **Índice de precios activos:** el índice único parcial `idx_service_price_one_active_per_service` (`service_id` con `is_active = true`, de `InitialParityLegacy`) impedía D45, porque un precio programado convive activo con el vigente. Pasa a `idx_service_price_one_active_per_start`, único por `(service_id, valid_from)` con `is_active = true`, con la migración `RelaxServicePriceActiveIndex` en la fase 12c. La regla de un solo precio vigente la mantiene `Service.SetPrice` | Usuario, 2026-10-25 (fase 12c); `ServicePriceConfiguration.cs` |
| D48 | **Precio de la guía:** `ForeignTradeService.GetGuidePriceAsync` (guía sin convenio) toma el precio de `GUIA_SALIDA` vigente hoy, con el mismo filtro del resolutor de tarifas (`ValidFrom <= ahora`, `ValidTo` nulo o posterior, el más reciente). Antes tomaba cualquier precio activo y podía cobrar el programado antes de su fecha | Usuario, 2026-10-25 (fase 12c); `BillingResolver.cs` nivel 3 |

---

## 3. Orden de las fases y dependencias

| Fase | Tema | Repos | Migración | Tamaño | Depende de |
| --- | --- | --- | --- | --- | --- |
| 1 | Superficie de API y leyenda fiscal | BE, FE | — | S | — |
| 2 | Concurrencia y guardas de la orden | BE, FE | — | L | 1 (un llamador menos de `CreateLoadingOrderCommand`) |
| 3 | Guía con aviso y marca «sin salidas» | BE, FE | `AddStakeholderExitBlock` | L | 2 (bloqueo de la orden y D6) |
| 4 | Báscula: corrección por pesaje y «Solo báscula» | BE, FE | — | M | 1 (PDF del tiquete) |
| 5 | Báscula: un pesaje para varios documentos | BE, FE | — | L | 4 (`CycleNetWeights`) |
| 6 | Facturación: tarifa faltante, precio futuro y renovación | BE | — | L | — |
| 7 | Facturación: convenios programados, índice y pendientes | BE, FE | `FixAgreementActiveStakeholderIndex` | M | 6 (mismo resolutor) |
| 8 | Reportes | BE, FE | — | L | 5 (neto prorrateado en el diario) |
| 9 | Migración legacy: año y prórroga | BE, docs | `AddWarehouseStorageLegacyYear` | M | — |
| 10 | Respaldos: correo y destino externo | BE, deploy, docs | — | S | — |
| 11 | Guía de salida con código QR de verificación | BE, FE, deploy | `AddGuideCodeTypeParameter` | M | 2 y 3 (mismos handlers de guía) |
| 12 | Documentación: procedimiento de corte, QA y estado | docs | — | M | 1–11 |
| 12c | Ajustes de `DEC-055` y orden de bloqueo de las guías | BE, FE | `RelaxServicePriceActiveIndex` (D47) | M | 12 y 12b |
| 13 | QA local, despliegue y QA en staging | todos | aplica 5 | M | 12c, y aprobación del usuario |

Las fases van en secuencia (DF13 del plan frontend de paridad): varias tocan los mismos handlers y pantallas. Las fases 6, 9, 10 y 11 no dependen de otras fases salvo lo indicado, pero se mantienen en orden para que cada commit parta del anterior.

---

## 4. Fase 1 — Superficie de API y leyenda fiscal (D2, D3, D4)

### 4.1 BR-03-001: retirar `PATCH entry-logs/{id}`

- **Estado:** `B/Wms.Api/Controllers/v1/EntryLogController.cs:63-72` (con la política `GateAccess`) llama a `UpdateEntryLogHandler`. El handler cambia el motivo sin la guarda D07 (`B/Wms.Application/Logistics/EntryLogs/Commands/UpdateEntryLog/UpdateEntryLogHandler.cs:80-83`) y enlaza el ingreso a un servicio cuya existencia no valida (`:65-73,85-96`).
- **Cambio:** borrar la acción `UpdateEntryLog` y su `using`. Borrar con `rm` la carpeta `UpdateEntryLog/` (comando, handler y validador). Borrar `EntryLog.AssignEntryReason` (`B/Wms.Domain/Entities/Logistics/EntryLog.cs:81-85`) si un grep confirma que no tiene otros llamadores. En el frontend, borrar `updateEntryLog` (`F/features/entries/services/entry-service.ts:34-40,93`) e `IUpdateEntryLogRequest` (`F/features/entries/types/entry-log.ts:53`) si no tiene otros usos.
- **Pruebas:**
  - **Nuevo** `B/Wms.Tests/Api/EntryLogControllerSurfaceTests.cs`, con el patrón de `BillingControllerSurfaceTests.cs`: no existe la acción `UpdateEntryLog` ni un `HttpPatch` con la plantilla `"{id}"`.

### 4.2 BR-03-002: retirar `POST warehouse/loading-orders`

- **Estado:** `B/Wms.Api/Controllers/v1/WarehouseController.cs:791-826` (con `WarehouseAccess`). No envía la unidad de carga (`:806`) y no tiene consumidores.
- **Cambio:** borrar la acción `CreateLoadingOrder` y los records `CreateWarehouseLoadingOrderRequest` y `CreateWarehouseLoadingOrderItemRequest` (`:1177-1197`). En el frontend, borrar:
  - `useLoadingOrderCreate` (`F/features/warehouse/composables/useLoadingOrderMutations.ts:25-46`) y su export (`composables/index.ts:57`);
  - `createLoadingOrder` (`F/features/warehouse/services/warehouse-service.ts:414-420,744`);
  - `ICreateLoadingOrderRequest` de warehouse (`types/loading-order.ts:120-121`, `types/index.ts:45`) y el resultado si queda huérfano;
  - las líneas de `composables/README.md:187-191`.

  **No se tocan** `useLoadingOrderCancel` ni `PATCH …/cancel`.
- **Pruebas:**
  - **Nuevo** `B/Wms.Tests/Api/WarehouseControllerSurfaceTests.cs`: no existe la acción `CreateLoadingOrder` ni un `HttpPost` con la plantilla `"loading-orders"`.

### 4.3 BR-02-005: leyenda no fiscal

- **Estado:** la leyenda está en `WA/Common/Services/WeighbridgeTicketPdfService.cs:414` y en `B/Wms.Application/Billing/Common/Services/InvoicePdfService.cs:314` (verificado). Ningún otro PDF la lleva.
- **Cambio:**
  - **Nuevo** `B/Wms.Application/Common/Services/DocumentLegends.cs`, con `WeighbridgeTicket` e `InternalInvoice` (textos exactos de D4).
  - Los dos PDF usan esas constantes.
- **Pruebas:**
  - **Nuevo** `B/Wms.Tests/Common/DocumentLegendsTests.cs`: ninguna constante contiene «DIAN», «autorizada» ni «habilitada».
  - Verificación manual con `pdftotext -layout` del tiquete y de la factura.

### 4.4 Criterio de salida de la fase 1

- Compuertas del §18.
- `grep` sin resultados de `UpdateEntryLog`, de `CreateWarehouseLoadingOrderRequest` y de «Numeración autorizada».

---

## 5. Fase 2 — Concurrencia y guardas de la orden (D5, D6)

### 5.1 BR-05-002: helper de bloqueo y handlers

- **Estado:**
  - `CreateLoadingOrderCommandHandler` carga y valida stock y nacionalizado fuera de la transacción (`FT/Commands/CreateLoadingOrder/CreateLoadingOrderCommandHandler.cs:79-88,155-197`) y la abre después (`:309`).
  - `WarehouseStorageProduct.ReserveStock` escribe valores absolutos (`B/Wms.Domain/Entities/Warehouse/WarehouseStorageProduct.cs:239-249`). Dos órdenes simultáneas se pisan.
  - Los levantes (`UpdateImportRelease`, `WithdrawImportRelease`) leen la reserva y escriben otra tabla: es un *write skew*.
- **Cambio:**
  - **Nuevo** `FT/Common/Services/StockRowLock.cs`, estático, al estilo de `WA/Common/Services/EntryLogLock.cs`:
    - `LockLoadingOrderAsync(ctx, orderId, ct)`: `SELECT id FROM loading_orders WHERE id = {orderId} FOR UPDATE`.
    - `LockStorageProductsAsync(ctx, ids, ct)`: ids distintos y ordenados; `SELECT id FROM warehouse_storage_products WHERE id = ANY({ids}) ORDER BY id FOR UPDATE`.
    - `OrderProductIdsAsync(ctx, orderId, ct)`: lectura `AsNoTracking` de los productos de la orden.
    - Si no hay transacción abierta, lanza `InvalidOperationException`, como `EntryLogLock.cs:31-36`.
    - El comentario del archivo documenta el orden global de D5.
  - **Regla de cada handler:** transacción → bloquear → leer → validar → guardar → confirmar → notificar. **Nada que se valide se lee antes del bloqueo**: EF no refresca una entidad ya rastreada. No se usa `ReloadAsync`.

    | Handler | Cambio |
    | --- | --- |
    | `FT/Commands/CreateLoadingOrder/CreateLoadingOrderCommandHandler.cs` | `BeginTransactionAsync` sube de `:309` a antes de la carga de `:77`; `LockStorageProductsAsync` de los productos pedidos; las validaciones quedan dentro. El consecutivo OC se toma después de los productos |
    | `FT/Commands/UpdateLoadingOrderItems/UpdateLoadingOrderItemsCommandHandler.cs` | Transacción al inicio; bloquear la orden y luego los productos de la orden ∪ los del request; después la carga de `:30-42` |
    | `B/Wms.Application/Warehouse/Commands/LoadingOrder/CancelLoadingOrder/CancelLoadingOrderHandler.cs` | Transacción explícita; orden y luego productos; cargar y guardar |
    | `B/Wms.Application/Warehouse/Commands/LoadingOrder/ExecuteLoadingOrderCommandHandler.cs` | El parseo y `PhotoUploadRules.DecodeAll` quedan fuera; la transacción sube antes de `:52`; orden y luego productos |
    | `FT/Commands/RevertLoadingOrder/RevertLoadingOrderCommandHandler.cs` | Orden y luego productos, antes de la carga de `:27` |
    | `FT/Commands/UpdateImportRelease/UpdateImportReleaseCommandHandler.cs`, `FT/Commands/WithdrawImportRelease/WithdrawImportReleaseCommandHandler.cs` | Transacción; leer el `WarehouseStorageProductId` del levante con una consulta escalar; bloquear ese producto; después cargar |
    | `B/Wms.Application/Warehouse/Commands/AdjustInventory/AdjustInventoryCommandHandler.cs` (CE-7) | Transacción y bloqueo del producto antes de cargarlo |
    | `FT/Commands/CreateDispatchGuide/CreateDispatchGuideCommandHandler.cs` | La transacción sube antes de cargar la orden; `LockLoadingOrderAsync` primero; releer «ya existe guía vigente» y el estado después del bloqueo |
    | `FT/Common/Services/DispatchGuideBalanceService.cs:29-30` | Agregar `ORDER BY id` al `FOR UPDATE` |

- **Pruebas:** **Nuevo** `B/Wms.IntegrationTests/ForeignTrade/LoadingOrderConcurrencyTests.cs`. Usa `ImportExitScenario` y el patrón `SimultaneousAsync` de `B/Wms.IntegrationTests/Weighbridge/WeighbridgeIdempotencyTests.cs:51-55`.
  1. Dos `POST foreign-trade/loading-orders` simultáneos por todo lo disponible:
     - uno responde 201 y el otro 400 «Stock disponible insuficiente…»;
     - `ReservedStock == total`;
     - hay una sola reserva activa.
  2. **Determinista:**
     - en un `CreateStandaloneDbContext` se abre una transacción con `FOR UPDATE` del producto;
     - la creación por API no termina en unos 500 ms;
     - la prueba reserva todo y confirma;
     - la creación responde 400.
  3. Reducir el levante (`PATCH`) y crear una orden por lo nacionalizado, en paralelo: una de las dos falla y la reserva final nunca supera los levantes.
  4. Cancelar y emitir la guía de la misma orden, en paralelo:
     - o la orden queda cancelada y sin guía;
     - o la guía queda vigente y la cancelación responde 409 (depende de §5.2).

### 5.2 BR-05-001: guarda «Anule primero la guía»

- **Estado:**
  - `LoadingOrder.Cancel` (`B/Wms.Domain/Entities/Warehouse/LoadingOrder.cs:309-330`) y `EnsureItemsEditable` (`:401-409`) solo miran el estado.
  - La cancelación la exponen CE (`ForeignTradeController.cs:1072-1086`) y Bodega (`WarehouseController.cs:830-844`), las dos con el mismo handler.
- **Cambio:**
  - **Dominio:**
    - `Cancel(string reason, string? activeGuideNumber)`: después de las validaciones de estado de hoy, si hay guía vigente lanza `ConflictException($"Anule primero la guía {n} de la orden {OrderNumber}.")`.
    - `EnsureItemsEditable(string? activeGuideNumber = null)`: «Anule primero la guía {n} de la orden {OC}: la guía tiene las cantidades de la orden.».
    - Los mensajes empiezan por «Anule primero la guía», para que el frontend reutilice la detección de `F/pages/foreign-trade/loading-orders/[id]/index.vue:131`.
  - **Handlers** (`CancelLoadingOrderHandler`, `UpdateLoadingOrderItemsCommandHandler`): después de bloquear la orden, leen `DispatchGuides.Where(g => g.LoadingOrderId == id && g.CancelledAt == null).Select(g => g.GuideNumber).FirstOrDefault()` y lo pasan. La guarda aplica a agregar, retirar y cambiar cantidades. Confirmar con grep que `Cancel(` no tiene otros llamadores.
  - **DTO:** `LoadingOrderDto.ActiveDispatchGuideNumber` (`string?`), que llena `FT/Queries/GetLoadingOrderDetail/GetLoadingOrderDetailHandler.cs`. El detalle de Bodega usa la misma consulta.
  - **Frontend:**
    - **Nuevo** `F/features/foreign-trade/utils/loading-order-guide-lock.ts`, con la función pura `orderActionsWithGuide(status, activeGuideNumber)`.
    - CE, `F/pages/foreign-trade/loading-orders/[id]/index.vue`:
      - mensaje `info`: «Esta orden tiene la guía {n} vigente: para cancelarla o modificarla, anule primero la guía.», con enlace a `/foreign-trade/dispatch-guides`;
      - «Cancelar orden» y «Modificar ítems» quedan deshabilitados, con `title`;
      - el `ReasonDialog` de cancelar recibe `error-action-label` «Ir a guías de salida».
    - Bodega, `F/pages/warehouse/loading-orders/[id].vue`: `canCancel` es falso, con el mensaje «La orden tiene la guía {n} vigente: Comercio Exterior debe anularla antes de cancelar».
    - Tipos: `activeDispatchGuideNumber?: string | null` en `F/features/foreign-trade/types/loading-order.ts` y en `F/features/warehouse/types/loading-order.ts`.
- **Pruebas:**
  - **`B/Wms.Tests/Domain/Warehouse/LoadingOrderTransitionsTests.cs`:**
    - cancelar con guía vigente → 409 con el número;
    - cancelar una orden `Loaded` con guía conserva el mensaje de revertir;
    - `EnsureItemsEditable` con guía → excepción; sin guía → pasa.
  - **Nuevo** `B/Wms.IntegrationTests/ForeignTrade/LoadingOrderWithGuideGuardTests.cs`, con una orden `Pending` y su guía:
    - el `cancel` de CE, el `cancel` de Bodega (rol Warehouse) y `PUT …/items` → 409;
    - después de anular la guía, los tres pasan;
    - el detalle trae `activeDispatchGuideNumber`.
  - **Vitest:** **Nuevo** `T/unit/foreign-trade/loading-order-guide-lock.spec.ts`.

### 5.3 Criterio de salida de la fase 2

- Compuertas del §18.
- Las 4 pruebas de concurrencia y las de la guarda en verde.

---

## 6. Fase 3 — Guía con aviso y marca «sin salidas» (D7, D8, D9, D10)

### 6.1 BR-05-006: aviso de diferencia con lo cargado

- **Estado:**
  - La guía congela `LoadedQuantity ?? Quantity` (`FT/Common/Services/DispatchGuideBalanceService.cs:15-21,97`).
  - `ExecuteLoadingOrderCommandHandler` registra lo cargado (`:219-220`), pero no lo compara con la guía.
- **Cambio:**
  - **Nuevo** `FT/Common/Services/GuideLoadMismatch.cs`, con estas reglas:
    - **Ítems que se comparan:** solo los que tienen `LoadedQuantity`.
    - **Ítem con línea en la guía:** hay diferencia si `|guía − cargado| > NationalizationBalance.Tolerance`.
    - **Ítem cargado sin línea:** cuenta como diferencia contra 0.
    - **Línea cuyo ítem quedó en 0:** cuenta como diferencia.
    - **Mensaje** (`NoticeMessage`): «La guía {g} de la orden {o} no coincide con lo cargado: {producto} guía {x} · cargado {y}; … Anúlela y emítala de nuevo.».
  - **`ExecuteLoadingOrderCommandHandler`:** dentro de la transacción, después de `RegisterLoaded`, calcula las diferencias con la guía vigente. Después del `Commit`:
    - si las hay, envía `NotifyRoleAsync(ForeignTrade, …)` con `ActionRequired`, título «Guía con cantidades distintas a lo cargado», `RelatedEntityType = "DispatchGuide"` y `sendEmail: false`, en un `try/catch` con `LogError`;
    - el mensaje del resultado añade « La guía {g} no coincide con lo cargado: Comercio Exterior fue notificado.».
  - **DTO calculado:**
    - `DispatchGuideDto.DiffersFromLoad` y `LoadDifferences` (`FT/Common/DTOs/DispatchGuideDto.cs`), que se calculan en `FT/Queries/GetDispatchGuides/GetDispatchGuidesHandler.cs` proyectando `LoadingOrderItemId` y `LoadedQuantity`. Solo para guías no anuladas.
    - `LoadingOrderDto.ActiveDispatchGuideDiffersFromLoad`.
  - **Frontend:**
    - `F/pages/foreign-trade/dispatch-guides/index.vue`: `Tag` `warn` «No coincide con lo cargado», con un tooltip que lista las diferencias.
    - Detalle CE de la orden: mensaje `warn` con enlace a guías.
    - Tipos en `F/features/foreign-trade/types/dispatch-guide.ts` y `loading-order.ts`.
- **Pruebas:**
  - **Nuevo** `B/Wms.Tests/ForeignTrade/GuideLoadMismatchTests.cs`:
    - igual, menos, en 0, dentro de la tolerancia y sin `LoadedQuantity`;
    - formato del mensaje.
  - **Nuevo** `B/Wms.IntegrationTests/ForeignTrade/GuideLoadMismatchNoticeTests.cs`:
    - guía por 100 y cargue de 80 → hay notificación y `differsFromLoad = true`;
    - al anular y reemitir, la guía nueva es de 80 y `differsFromLoad = false`;
    - cargar 100 no genera notificación.

### 6.2 BR-05-004: marca «sin salidas»

- **Estado:** `Stakeholder` (`B/Wms.Domain/Entities/Stakeholder/Stakeholder.cs:15-21`) no tiene ninguna marca de salidas. El bloqueo por mora (`B/Wms.Application/Billing/Common/Services/BillingService.cs:106-119`) se usa en 14 sitios y **no** se reutiliza.
- **Dominio:** en `Stakeholder` se agregan:
  - las propiedades `ExitsBlocked`, `ExitsBlockedReason`, `ExitsBlockedAt` y `ExitsBlockedById`;
  - `BlockExits(reason, userId)`: 400 si ya está bloqueado;
  - `UnblockExits(userId)`: 400 si no está bloqueado; limpia los cuatro campos;
  - `EnsureExitsAllowed()`: `BadRequestException("El cliente '{Name}' tiene las salidas bloqueadas: {motivo}. No se puede proceder con la operación.")`.

  El motivo del desbloqueo va a `audit_logs` con `IAuditContext.Describe`.
- **EF y migración:** en `B/Wms.Infrastructure/Persistence/Configurations/Stakeholder/StakeholderConfiguration.cs`, con el precedente de `IsUap`:
  - `exits_blocked` `boolean NOT NULL DEFAULT false`, con `.IsRequired().HasDefaultValue(false)`. La tabla no tiene `HasData`;
  - `exits_blocked_reason` `varchar(500)` nulo;
  - `exits_blocked_at` `timestamptz` nulo;
  - `exits_blocked_by_id` `uuid` nulo y sin FK, como `LoadingOrder.RevertedById`.

  Migración **`AddStakeholderExitBlock`**.
- **Comando:** **Nuevo** `B/Wms.Application/Stakeholders/Commands/SetExitBlock/` (comando, handler y validador). El motivo es obligatorio, de 10 a 500 caracteres, al bloquear y al desbloquear.
- **Endpoint:** `PATCH stakeholder/{id}/exit-block`, con el cuerpo `{ blocked, reason }`. El autor sale del token. Va con la política **nueva** `ExitBlockAccess` (Admin, ForeignTrade, Billing), en `B/Wms.Domain/Security/WmsPolicyRoles.cs`, registrada como las demás. El request nuevo va en `B/Wms.Api/Controllers/v1/Requests/`.
- **Validación:** **Nuevo** `B/Wms.Application/Stakeholders/Common/StakeholderExitRules.cs`, con `EnsureExitsAllowedAsync(ctx, stakeholderIds, ct)`: una consulta `AsNoTracking` que lanza la excepción del primero bloqueado. Se llama en:
  1. `CreateLoadingOrderCommandHandler`, junto a la mora (`:150-152`);
  2. `LoadingOrderReservationService.EnsureNewItemAllowedAsync` (`:63-66`);
  3. `CreateDispatchGuideCommandHandler`, para **todos los dueños** (`owners`, `:150`), con cualquier destinatario;
  4. `ExecuteLoadingOrderCommandHandler`, antes de registrar el cargue, para los dueños de la orden (D9).

  La guía automática de exportación no se valida aparte: con el cargue bloqueado, no se llega a ella.
- **C3, mora de los dueños:** en `CreateDispatchGuideCommandHandler`, `ValidateFinancialStatusAsync` corre para cada dueño (`owners`) en todos los casos, no solo con «Clientes» (`:178-181`).
- **DTO:** `StakeholderDto` (`B/Wms.Application/Stakeholders/Common/Dtos/StakeholderDto.cs`) suma `ExitsBlocked`, `ExitsBlockedReason`, `ExitsBlockedAt` y `ExitsBlockedByName`. Los llenan `GetStakeholdersHandler.cs:81` y la consulta por id. `GetStakeholdersQuery` suma el filtro opcional `exitsBlocked`.
- **Frontend:**
  - `F/features/stakeholders/components/StakeholderProfile.vue`: `Tag` `danger` «Salidas bloqueadas», con motivo, fecha y autor.
  - `F/pages/admin/stakeholders/[id].vue`: botón «Bloquear salidas» o «Desbloquear salidas» que abre `~/components/app/ReasonDialog.vue`. Lo ven Admin, ForeignTrade y Billing.
  - **Nuevo** `F/features/stakeholders/composables/useStakeholderExitBlock.ts`, que invalida `['stakeholders']` y `['foreign-trade']`.
  - Servicio y tipos en `F/features/stakeholders/`.
  - Filtro «Salidas bloqueadas» en `index.vue`.
- **Pruebas:**
  - **Nuevo** `B/Wms.Tests/Domain/Stakeholder/StakeholderExitBlockTests.cs`: bloquear, bloquear dos veces (400), desbloquear, el mensaje y el validador.
  - `B/Wms.Tests/Security/WmsPolicyRolesTests.cs`: la fila de `ExitBlockAccess`.
  - **Nuevo** `B/Wms.IntegrationTests/ForeignTrade/StakeholderExitBlockTests.cs`:
    - con el tercero bloqueado, crear la orden, agregar ítems, emitir la guía (un solo dueño con otro destinatario) y ejecutar el cargue (Bodega) responden 400;
    - al desbloquear, pasan;
    - quedan dos filas en `audit_logs`;
    - Receiving, Scale y Warehouse reciben 403 en el `PATCH` (filas en `B/Wms.IntegrationTests/Security/CatalogWriteAuthorizationTests.cs`);
    - el cobro de báscula y la recepción de un cliente bloqueado **no** se frenan.
  - **C3:** una guía de un solo dueño en mora con otro destinatario → 400.
  - Vitest de la etiqueta y del botón.

### 6.3 Criterio de salida de la fase 3

- Compuertas del §18.
- La migración `AddStakeholderExitBlock` aplicada en la base local.
- `has-pending-model-changes` limpio.

---

## 7. Fase 4 — Báscula: corrección por pesaje y «Solo báscula» (D11, D12)

### 7.1 BR-02-006: corregir el pesaje elegido

- **Estado:**
  - `F/features/weighbridge/components/ModifyWeighingDialog.vue:123-133` manda cualquier pesaje distinto del primero a `second-weight`.
  - `WA/Commands/ModifySecondWeight/ModifySecondWeightHandler.cs:61-63` toma siempre la secuencia 1.
  - `:75-84` actualiza una entrada no determinista (`FirstOrDefaultAsync` sin `OrderBy`) con `|w0 − w1|`.
  - `ModifyFirstWeightHandler.cs:71-82` tiene el mismo patrón.
- **Cambio:**
  - **Nuevo** `WA/Common/Services/CycleNetWeights.cs`:
    - `Recalculate(weighings, entries)` calcula el neto de cada entrada como `|entrada − salida|`;
    - una entrada sin pesaje de salida conserva su valor;
    - `AffectedBy(weighingId, entries)` devuelve las entradas a recalcular.
  - **Request y comando:** `Guid? WeighingId = null` en `ModifySecondWeightRequest` y en el comando.
    - Sin `WeighingId`: se corrige la secuencia 1.
    - Con un pesaje de otro ciclo: 404 «El pesaje no existe en este ciclo.».
    - Con la secuencia 0: 400 «Use la corrección del primer pesaje.».
  - **Los dos handlers:**
    - cargan todas las entradas del ciclo, ordenadas por `CreatedAt`;
    - aplican `UpdatePhysicalNetWeight` a las entradas afectadas;
    - con un solo pesaje, el neto queda nulo (D11).
  - **Respuesta y notificación:**
    - `NewNetWeight` = `|primero − último|`;
    - se agrega `EntryNetWeights`;
    - la notificación a Admin dice «modificó el pesaje #{n} ({tipo})».
  - **`WeighbridgeCorrectionController.cs`:** pasa `WeighingId`.
  - **Frontend:**
    - **Nuevo** `modifyWeightTarget(weighing)` en `F/features/weighbridge/utils/weighing-rules.ts`;
    - el diálogo envía `weighingId` cuando el pesaje no es el primero;
    - el tipo `IModifySecondWeightRequest` suma `weighingId?`.
- **Pruebas:**
  - **Nuevo** `B/Wms.Tests/Weighbridge/CycleNetWeightsTests.cs`, sobre el ciclo Bruto 30.000 → Intermedio 22.000 → Tara 12.000 con dos entradas:
    - corregir la tara cambia solo la entrada 2;
    - corregir el intermedio cambia las dos;
    - corregir el bruto cambia solo la 1;
    - una entrada sin salida no cambia;
    - con dos pesajes, el neto es `|w0 − w1|`.
  - **Nuevo** `B/Wms.IntegrationTests/Weighbridge/MultiDepositWeightCorrectionTests.cs`, con el sembrado de `AdditionalDepositRecipientTests` y `RegisterArrivalAsync`:
    - con el `weighingId` de la secuencia 2, la secuencia 1 queda intacta;
    - sin `weighingId`, se corrige la 1;
    - un pesaje de otro ciclo → 404;
    - la secuencia 0 → 400;
    - `TareAboveGrossTests` y `WeightModificationAuthorTests` siguen en verde.
  - **Vitest:** `modifyWeightTarget` con las secuencias 0, 1 y 2.

### 7.2 BR-02-002: «Solo báscula» sin cliente

- **Estado:**
  - **Backend:**
    - `WA/Commands/WeighingOnly/Initiate/InitiateWeighingOnlyValidator.cs:13-15` exige el cliente;
    - el handler lo parsea a la fuerza (`InitiateWeighingOnlyHandler.cs:37-40,66-73,96-103,129-138,168`);
    - `ServiceRecord.CreateForWeighingOnly(… Guid customerId …)` (`B/Wms.Domain/Entities/Services/ServiceRecord.cs:99-120`).
  - **Ya funciona sin cliente:** la columna admite nulos y el cobro también (`ProcessWeighingOnlyPaymentHandler.cs:64-100`, `StartWeighingOnlyPendingBillingHandler.cs:58-90`).
- **Cambio:**
  - **Backend:**
    - request y comando con `string? CustomerId`;
    - el validador solo exige un Guid válido cuando viene;
    - el handler busca al cliente solo si viene, agrega el stakeholder CUSTOMER solo si hay cliente, pide la tarifa con `customerId ?? Guid.Empty` y responde `CustomerName = customer?.Name ?? "Sin cliente asignado"`;
    - `CreateForWeighingOnly(…, Guid? customerId, …)`.
  - **Tiquete:** **Nuevo** `WA/Common/Services/TicketRecipient.cs`, función pura. El nombre del tiquete es el primero disponible de esta cadena:
    1. `invoice.Customer?.Name`;
    2. `invoice.UnregisteredRecipient?.Name`;
    3. `ServiceRecord.Customer?.Name`;
    4. «CONSUMIDOR FINAL».

    Documento y teléfono siguen la misma precedencia. `WeighbridgeTicketPdfService.cs:176-184` la usa.
  - **Historial:**
    - `WA/Queries/GetWeighbridgeHistory/GetWeighbridgeHistoryHandler.cs:54-59`: el nombre cae a `UnregisteredRecipient.Name` de la factura del ciclo o de sus entradas;
    - `WeighbridgeHistoryFilters.cs:41-48`: el filtro por cliente incluye `wc.Invoice` (cliente y no registrado).
  - **Frontend:**
    - `F/features/weighbridge/components/WeighingOnlyForm.vue` (`:2-13,73-74,81-82,103-105`):
      - rótulo «Cliente (opcional)», con la ayuda «Sin cliente, el cobro va al conductor o al consumidor final»;
      - zod opcional y nulo;
      - `missingCount` en 0;
      - se envía `customerId || null`.
    - `F/features/weighbridge/types/requests.ts:34`: `customerId?: string | null`.
    - `F/features/billing/utils/billing-recipient-default.ts`: parámetro `fallback`, que «Solo báscula» pasa como `"finalConsumer"` desde `F/pages/operations/weighbridge/index.vue:1046`.
- **Pruebas:**
  - **Nuevo** `B/Wms.Tests/Weighbridge/InitiateWeighingOnlyValidatorTests.cs` y **Nuevo** `TicketRecipientTests.cs`.
  - **Nuevo** `B/Wms.IntegrationTests/Weighbridge/WeighingOnlyWithoutCustomerTests.cs`:
    - iniciar sin cliente → 201, sin stakeholder CUSTOMER;
    - cobro al conductor → factura con `UnregisteredRecipient`;
    - `start-pending-billing` con `finalConsumer` → 200;
    - el historial muestra al conductor y el filtro lo encuentra;
    - `InitiateCustomerIdTests` sigue en verde.
  - **Vitest:** `defaultBillingRecipient(null, null, "finalConsumer")`.

### 7.3 Criterio de salida de la fase 4

- Compuertas del §18.
- Sin migración.

---

## 8. Fase 5 — Báscula: un pesaje para varios documentos (D13, D14, D15, D16)

- **Estado:**
  - `WA/Commands/Common/RecordWeighing/RecordWeighingHandler.cs:140-160` exige un intermedio por cada depósito adicional. La interfaz ya ofrece Tara (`F/features/weighbridge/components/WeightCapture.vue:135-141`), pero el backend responde 400.
  - `WA/Commands/Common/CompleteCycle/CompleteCycleHandler.cs:125-129,191-207` exige `pesajes == depósitos` y asigna la salida solo a la última entrada.
  - El mensaje de `RecordWeighingHandler.cs:128-133`, sobre el perecedero «sin pesaje», es inalcanzable.
- **Reglas puras:**
  - **Nuevo** `WA/Common/Services/MultiDepositWeighingRules.cs`, con `Classify(sequence, storageCount, hasIntermediate, requested, oppositeOfFirst)`, que devuelve `FirstWeighing | Intermediate | CloseShared | ClosePerDeposit`:
    - `sequence == 0` → `FirstWeighing`;
    - `storageCount ≤ 1` → `ClosePerDeposit` con el opuesto; con otro tipo, 400 como hoy;
    - sin intermedio en la secuencia 1:
      - el opuesto → `CloseShared`;
      - Intermedio → `Intermediate`;
      - otro → 400 «Con {N} depósitos, el pesaje 2 debe ser {opuesto} (un solo pesaje para todos) o Intermedio (descarga en otro punto).»;
    - con intermedio → las reglas de hoy.
  - **Nuevo** `WA/Common/Services/SharedNetSplit.cs`, con `Split(total, manifestWeights)`, según D14. Si algún peso es nulo o cero, todos los netos del grupo quedan nulos.
  - `CycleNetWeights` (fase 4) se amplía: las entradas con el mismo par (entrada, salida) forman un grupo y reparten el neto del camión con `SharedNetSplit`.
- **`RecordWeighingHandler`:** usa `Classify`. `cycleCompletes = CloseShared || ClosePerDeposit`. Se corrige el mensaje obsoleto.
- **`CompleteCycleHandler`, rama compartida** (no perecedero, un pesaje previo y 2 o más depósitos). Relaja la regla de `:125-129` solo en este caso y, para **cada** entrada:
  - `EntryWeighingId ??= w0.Id` y `AssignExitWeighing(final.Id)`;
  - `ReceptionArrivalGuard.EnsureArrivedAsync` (CHG-36);
  - el tiquete de la entrada que no tenga uno, en orden de `CreatedAt`, con `IWeighbridgeService.GenerateTicketNumberAsync(EntryLog.DateTimeEntry)` dentro de la transacción. Hay que inyectar `IWeighbridgeService`;
  - el neto, con `CycleNetWeights.Recalculate`.
- **Reparto de nuevo** (D14):
  - en `ModifyFirstWeightHandler` y `ModifySecondWeightHandler`, al corregir el bruto o la tara de un grupo compartido;
  - en `FT/Commands/UpdateTruckManifest/UpdateTruckManifestCommandHandler.cs:28-46`: si la entrada pertenece a un grupo compartido de un ciclo completo, se cargan las entradas del ciclo y se reparte de nuevo.
- **DTO:** `IsSharedWeighing`, calculado, en `WA/Common/Dtos/WeighbridgeCycleDetailDto.cs` y en los DTO de detalle de CE.
- **Tiquete PDF:** en el modo compartido, debajo de «PESO MERCANCÍA», la línea de D15.
- **Frontend:**
  - **Nuevo** `F/features/weighbridge/utils/multi-deposit-weighing.ts`, con el orden y los rótulos:
    - con `FirstWeightCaptured` y `MultiDeposit`, el orden es `[opuesto, "Intermediate"]`;
    - rótulos: «{Tara/Bruto} — un solo pesaje para todos los depósitos» e «Intermedio — el camión descarga en otro punto».
  - `WeightCapture.vue` lo usa.
  - `StorageServiceForm.vue:428`: la nota del modo adicional explica las dos opciones.
  - **C4:** en `F/pages/operations/weighbridge/index.vue:1287`, en multidepósito, se imprime el tiquete de cada entrada con `downloadAndPrintEntryTicket` (`useTicketPdf.ts:81-98`).
  - `F/features/foreign-trade/components/DepositDetailWeightsCard.vue`: el rótulo «Neto prorrateado (pesaje compartido)».
- **Pruebas:**
  - **Nuevos** `B/Wms.Tests/Weighbridge/MultiDepositWeighingRulesTests.cs`, con todas las ramas y el mensaje de 400.
  - **Nuevo** `SharedNetSplitTests.cs`:
    - 20.000/10.000 de manifiesto con 27.000 de neto → 18.000/9.000;
    - la suma da exacta con el redondeo;
    - un manifiesto nulo → todos nulos;
    - un solo depósito → el total.
  - `CycleNetWeightsTests` ampliado.
  - **Nuevo** `B/Wms.IntegrationTests/Weighbridge/SharedWeighingMultiDepositTests.cs`:
    - dos depósitos con Bruto y Tara → ciclo `Complete`, los dos pares asignados, tiquetes consecutivos y netos que suman el neto del camión;
    - sin llegada a Bodega del segundo → 409;
    - el modo intermedio sigue como hoy;
    - con un intermedio, una Tara antes de N → 400;
    - corregir la tara reparte de nuevo;
    - completar el manifiesto que faltaba reparte;
    - facturas: la primera con valor y la del adicional en $0.
  - **Vitest:** **Nuevo** `T/unit/weighbridge/multi-deposit-weighing.spec.ts`.
- **Riesgo:** un papel por depósito suma tiempo en la vía. Se mide dentro de PRF-002 (DEC-010).
- **Criterio de salida:** compuertas del §18, sin migración.

---

## 9. Fase 6 — Facturación: tarifa faltante, precio futuro y renovación (D17, D18, D19)

### 9.1 BR-06-004: respaldo del servicio complementario

- **Estado:**
  - `B/Wms.Application/Billing/Common/Services/StorageBillingService.cs:790` llama a `billingResolver.ResolveAsync` del complementario **sin** `try/catch`, dentro de `BuildStorageChargeLinesAsync` (`:711-801`).
  - La excepción revierte la confirmación (`FT/Commands/ConfirmStorageDeposit/ConfirmStorageDepositHandler.cs:68-89`).
  - En el job, la excepción deja el período vencido, que se reintenta cada 5 min (`B/Wms.Api/BackgroundJobs/StoragePeriodAutoCloseBackgroundService.cs:10,88-91`).
  - El cargo principal no atrapa `NotSupportedException` (`:148`, `:228`).
- **Cambio:**
  - **Nuevo** `B/Wms.Application/Billing/Common/Services/StorageRuleFailure.cs`, con `IsRuleFailure(Exception)`: `BadRequest`, `NotFound` o `NotSupported`.
  - **`ResolveStorageChargesAsync`, paso nuevo después de los cargos.** Para cada `LinkedServiceId` distinto:
    1. resuelve con el mismo `FormulaContext` de `:779-788`;
    2. un importe negativo se trata como una falla de la regla;
    3. si la regla falla, toma el `ServiceMinimumValue` del **propio** servicio en la modalidad con `StorageMinimumCharge.NetAmount`, o $0 si no hay;
    4. agrega `StorageFallbackWarning.BuildLinkedService(...)`;
    5. guarda el resultado en `StorageChargeResolution.LinkedCharges`, con el record nuevo `StorageLinkedCharge` en `StorageCharge.cs`.
  - **`BuildStorageChargeLinesAsync`:** usa `resolution.LinkedCharges` y ya no resuelve. La línea de respaldo dice «{Nombre} (valor mínimo) {período}».
  - **Respaldo del cargo principal** (`:148`, `:228`): usa `IsRuleFailure`; un importe negativo también va al respaldo.
  - **`ConfirmStorageDepositHandler.cs:62-65`:** corregir el comentario.
- **Pruebas:**
  - **`Wms.Tests`:**
    - `StorageFallbackWarningTests` (textos con mínimo y sin él);
    - **Nuevo** `StorageRuleFailureTests`.
  - **Nuevo** `B/Wms.IntegrationTests/Billing/StorageLinkedServiceFallbackTests.cs`:
    1. Complementario sin tarifa ni mínimo: confirmar responde 200, la línea sale en $0 con `MinimumValue`, el `Detail` lleva la advertencia y Facturación recibe el aviso.
    2. Con mínimo en IMP: la línea vale ese mínimo.
    3. Con un precio vencido: igual que el caso 1.
    4. Con una regla `PER_VEHICLE`: la línea de respaldo.
    5. Renovación por job, con el período fechado hacia atrás con `ExecuteUpdateAsync`: se renueva sin aviso de fallo, y una segunda corrida no encuentra nada vencido.
    6. CE-7: 200, factura recalculada.

### 9.2 C5: `Service.SetPrice`

- **Cambio:** en `B/Wms.Domain/Entities/Service/Service.cs:56-63`, los precios activos vencen en `max(UtcNow, validFrom) − 1 tick`.
- **Pruebas:** **Nuevo** `B/Wms.Tests/Domain/Service/ServiceSetPriceTests.cs`:
  - un precio futuro no vence el vigente antes de su `validFrom`;
  - un precio inmediato lo vence ya.
- **Riesgo:** afecta a báscula, montacargas y guía; F6-TAR y F3-COB se re-ejecutan en la fase 12.

### 9.3 BR-06-005: saldo al inicio del período

- **Estado:**
  - el job renueva en `fin + 4` con inicio `fin + 1` (`B/Wms.Application/Billing/Jobs/BillingJobService.cs:160-168,225-241`);
  - la apertura cobra `CurrentStock` (`StorageBillingService.cs:112-115,381`);
  - `StorageBillableQuantity.WindowStart` (`B/Wms.Application/Billing/Common/Services/StorageBillableQuantity.cs:40-46`) empieza en el último cierre;
  - dos pruebas codifican el comportamiento que DEC-053 revierte.
- **Cambio:**
  - `StorageBillableQuantity`:
    - `RenewalCutoff(S) = ColombiaTime.StartOfDayUtc(S + 1)`;
    - `WindowStart`: si no hay cierres previos, el inicio del período, como hoy; si los hay, `Min(último cierre, RenewalCutoff(día de inicio))`.
  - **Refactor:** se extrae de `LoadBillableQuantitiesAsync` (`:622-667`) el método `LoadBillableQuantitiesSinceAsync(wsId, since, depletedSet)`.
  - **Opción nueva** `StoragePeriodOpenOptions.BillAtPeriodStart` (`StorageCharge.cs:61`), en `true` solo en:
    - el job (`BillingJobService.cs:237-241`);
    - el cierre manual (`B/Wms.Application/Billing/Commands/CloseStoragePeriods/CloseStoragePeriodsHandler.cs:61-65`).

    En `OpenPeriodWithInvoiceAsync`, si está activa: `since = Min(UtcNow, RenewalCutoff(PeriodStart))`; si `since < UtcNow`, se cargan las cantidades desde `since` y se pasan a `ResolveStorageChargesAsync`.
  - **Unidades de carga (D19):**
    - **Nuevo** `B/Wms.Application/Billing/Common/Services/StorageBillableCargoUnits.cs`, con `Count(units, dispatchesSince)`: una unidad cuenta si hoy no está `Dispatched` o si salió por cargue después de `since`;
    - los datos salen de `LoadingOrderItem.WarehouseStorageCargoUnitId`, unido con `InventoryMovement` (`SourceType = LoadingOrder`, `CreatedAt >= since`);
    - se pasan a `ResolveStorageChargesAsync` como `billableCargoUnitIds` (`:81-87`), en la apertura de la renovación **y** en `RecalculateCoreAsync`.
- **Pruebas:**
  - **`B/Wms.Tests/Billing/StorageBillableQuantityTests.cs`:**
    - cambian `WindowStart_Renewal_IsTheLastClosingOfEarlierWindows` (pasa a `…_IsThePeriodStartCutoff`) y `Renewal_DispatchInGraceDays_IsNotBilledAgain` (pasa a `…_IsBilledAtPeriodStart`, que espera 40);
    - se mantienen las de cierre manual anticipado y primer período;
    - nuevas: una salida el día S no se cobra; cierre manual en la gracia; job atrasado dos períodos.
  - **Nuevo** `StorageBillableCargoUnitsTests.cs`.
  - **Nuevo** `B/Wms.IntegrationTests/Billing/StorageRenewalAtPeriodStartTests.cs`, con fechas hacia atrás vía `ExecuteUpdateAsync`:
    1. `PER_UOM` de 10, salida de 4 en `fin + 2`: la factura nueva cobra 10, `StockAtBilling = 10`, y un CE-7 sin cambio la deja en 10.
    2. La salida en `fin − 1`: cobra 6.
    3. Una salida el día S (`fin + 1`): no se cobra.
    4. `PERCENTAGE_OF_VALUE` sin agotar: el mismo total.
    5. Producto agotado en la gracia dentro de un grupo: entra con su cantidad.
    6. `PER_CARGO_UNIT` con un contenedor despachado en la gracia: cuenta.
    7. `EarlyManualClose_RenewalKeepsLoadingAfterTheClose` y `ManualPeriodCloseTests` siguen en verde.
- **Riesgo en staging:** los períodos renovados que sigan abiertos subirán en su próximo recálculo lo despachado en la gracia. DEC-022 actualiza la factura y notifica. Se avisa en el despliegue (§16.3).

### 9.4 Criterio de salida de la fase 6

- Compuertas del §18.
- Sin migración.
- `StorageRecalculationDispatchTests`, `ManualPeriodCloseTests` y `StorageTariffResolutionTests` en verde.

---

## 10. Fase 7 — Facturación: convenios programados, índice y pendientes (D20, D21, D22)

### 10.1 BR-06-001 y C2: activación de convenios programados

- **Estado:**
  - Nada pasa un convenio de `Scheduled` a `Active`: solo leen `ScheduledActivationDate` los DTO, los validadores y la creación y edición.
  - El resolutor filtra `Status == Active` (`B/Wms.Application/Billing/Services/BillingResolver.cs:180-185`).
  - Ya existe el índice `idx_agreement_status_scheduled` (`AgreementConfiguration.cs:50-51`).
- **Cambio:**
  - **Nuevo** `B/Wms.Domain/Entities/Agreement/AgreementEffectivity.cs`, con `EffectiveAgreementId(agreements, now)`:
    - si hay programados vencidos, gana el más reciente;
    - si no, el activo.
  - **`BillingResolver.FindActiveAgreementServiceAsync`** (`:167-196`):
    - carga los convenios `Active` o (`Scheduled` con fecha ≤ ahora);
    - elige con `EffectiveAgreementId`;
    - aplica `RuleSpecificity.Select` solo a los servicios del elegido;
    - no modifica datos.
  - **`Stakeholder.ActivateDueScheduledAgreements(now)`** (`Stakeholder.cs:231-243`, junto a `ActivateAgreement`):
    - activa los vencidos en orden de fecha;
    - cada activación archiva el anterior;
    - es idempotente.
  - **Nuevo** `B/Wms.Application/Agreements/Services/AgreementActivationService.cs`, con `IAgreementActivationService.ActivateDueAsync(ct)`:
    - un cliente por transacción;
    - **archivar y guardar, y después activar y guardar** (D21);
    - `IAuditContext.Describe("Activación programada del convenio …")`;
    - aviso a Billing: «Convenio {X} de {cliente} activado (programado para dd/MM/aaaa)».
  - **Nuevo** `B/Wms.Api/BackgroundJobs/AgreementActivationBackgroundService.cs`:
    - corre a los 30 s del arranque y cada día a las 00:00:30 de Colombia;
    - patrón de `DelayUntilNextRun` de `FT/Jobs/AbandonmentAlertService.cs`;
    - se registra en `B/Wms.Api/Program.cs:77-82` y en `BackgroundServiceTypes` de `B/Wms.IntegrationTests/Infrastructure/WmsApiFactory.cs:38-46`.
  - **Granularidad de día (C2):**
    - `CreateAgreementHandler` y `UpdateAgreementHandler` normalizan a `ColombiaTime.StartOfDayUtc(fecha)`;
    - los validadores comparan con `ColombiaTime.Today`; «hoy» es válido;
    - `Scheduled` sin fecha → 400 «Un convenio programado necesita la fecha de activación.» (validador y `Agreement.Create`).
  - **Frontend:**
    - `F/features/agreements/components/AgreementForm.vue`: sin `show-time`, sin «(Opcional)», con el aviso «Se activará el dd/MM/aaaa y archivará el convenio activo»;
    - **Nuevo** `F/features/agreements/utils/agreement-schedule.ts`, con el esquema;
    - `AgreementProfile.vue`, `AgreementHeader.vue` y `AgreementDetailDialog.vue`: «Se activa el …».

### 10.2 C1: índice único de convenio activo

- **Cambio:**
  - En `AgreementConfiguration.cs:53-56`, `HasFilter("status = 'Active'")`. Migración **`FixAgreementActiveStakeholderIndex`**.
  - Todo camino que activa un convenio guarda el archivo del anterior antes de activar el nuevo, en la misma transacción:
    - `Stakeholder.SetAgreement` con un convenio nuevo `Active` (`:203-218`);
    - `ActivateAgreement` (`:231-243`) y su handler;
    - el servicio del §10.1.

    Buscar todos los caminos con grep de `SetAgreement(`, `ActivateAgreement(` y `.Activate(`.
- **Riesgo:** si staging tiene clientes con dos convenios activos, la migración falla. Se cuentan antes de desplegar (§16.1).

### 10.3 BR-06-003: depósitos pendientes

- **Estado:** `B/Wms.Application/Billing/Queries/GetPendingDeposits/GetPendingDepositsHandler.cs:27-33,139-145,171-173,247-249`: solo depósitos `Confirmed` con un período `Open`.
- **Cambio:**
  - **Nuevo** `PendingDepositCriteria.cs`, en la misma carpeta, con expresiones traducibles. Un período está pendiente si cumple una de estas dos condiciones:
    - **Por numerar:** su factura está en Borrador y sin N.º SIIGO.
    - **Por refacturar:** su factura está anulada y sin reemplazo.

    Un depósito entra en la lista si cumple una de estas dos:
    - es `IsActive`, está `Confirmed` y tiene un período `Open` (lo de hoy);
    - es `IsActive`, está `Confirmed` o `Closed` y tiene algún período por numerar o por refacturar.
  - **Orden:** primero los que tienen período abierto, por su inicio más antiguo; después los cerrados, por el `PeriodEnd` más reciente; desempate por número. El orden es explícito: no se confía en NULLS LAST.
  - **DTO** `DepositPendingBillingRow`:
    - `DaysOpen` pasa a `int?`;
    - se agregan `HasOpenPeriod` y `PeriodsPendingNumber`;
    - `BuildRow` ya no descarta las filas sin período abierto.
  - **Consulta:** `PendingWorkOnly` (bool) en `GetPendingDepositsQuery`.
  - **Frontend:**
    - **Nuevo** `F/features/billing/utils/pending-deposit-status.ts`;
    - `F/pages/billing/pending-deposits/index.vue`: columna «Pendiente» con etiquetas, y «Cerrado» en la columna «Días»;
    - `F/features/billing/components/PendingDepositsFilters.vue`: el interruptor;
    - tipos en `F/features/billing/types/pending-deposit.ts` (`daysOpen: number | null`, `hasOpenPeriod`, `periodsPendingNumber`) y en `requests.ts` (`pendingWorkOnly?`);
    - revisar `getDaysBadgeSeverity`.

### 10.4 Pruebas de la fase 7

- **`Wms.Tests`:**
  - **Nuevos** `B/Wms.Tests/Agreements/AgreementEffectivityTests.cs` y `ScheduledAgreementActivationTests.cs`:
    - vencido contra no vencido;
    - dos vencidos;
    - idempotencia;
    - un programado sin fecha → 400;
    - la próxima corrida a las 00:00:30.
  - **Nuevo** `B/Wms.Tests/Billing/Queries/PendingDepositCriteriaTests.cs`: los seis casos de D22.
- **`Wms.IntegrationTests`:**
  - **Nuevo** `B/Wms.IntegrationTests/Billing/ScheduledAgreementActivationTests.cs`:
    1. Un programado con la fecha llevada hacia atrás: la factura sale con `Source = Agreement` y su tarifa.
    2. `ActivateDueAsync`: el programado queda `Active` y el anterior `Archived`; quedan `audit_logs` y el aviso a Billing; la segunda corrida no hace nada.
    3. Un programado para mañana no rige.
    4. Con el índice corregido, dos activos del mismo cliente por SQL de prueba → violación de unicidad. La activación manual y la programada pasan.
  - **Nuevo** `B/Wms.IntegrationTests/Billing/PendingDepositsListTests.cs`:
    - depósito cerrado con Borrador sin N.º;
    - anulado sin refacturar;
    - depósito `Cancelled`, que no aparece;
    - `pendingWorkOnly`;
    - paginación con `all=true`.
- **Vitest:** **Nuevos** `T/unit/agreements/agreement-schedule.spec.ts` y `T/unit/billing/pending-deposit-status.spec.ts`.

### 10.5 Criterio de salida de la fase 7

- Compuertas del §18.
- La migración `FixAgreementActiveStakeholderIndex` aplicada en la base local.

---

## 11. Fase 8 — Reportes (D23 a D27)

### 11.1 BR-07-003: fecha de ingreso

- **Cambio:**
  - **Kardex:** `EntryDateTime = warehouseStorage.EntryDate ?? warehouseStorage.CreatedAt` (`B/Wms.Application/Warehouse/Queries/GetWarehouseStorageMovements/GetWarehouseStorageMovementsHandler.cs:309`). Hoy usa el `CreatedAt` del servicio.
  - **Importaciones:** se agrega `ImportDepositDto.EntryDate` (`FT/Common/DTOs/ImportDepositDto.cs:31`), con valor `iws.WarehouseStorage.EntryDate` (`FT/Queries/GetImportDeposits/GetImportDepositsHandler.cs:147`).
  - **Frontend:**
    - Excel de importaciones (`F/pages/foreign-trade/imports/index.vue:169`), de exportaciones (`exports/index.vue:114`) y de inspecciones (`inspections/index.vue:85`): `entryDate ?? createdAt`;
    - columna «Fecha Ingreso» de `F/features/foreign-trade/components/ImportDepositList.vue:129`, `ExportDepositList.vue:98` e `InspectionDepositList.vue:118`, con `field="entryDate"` y respaldo `createdAt`;
    - tipo `IImportDepositDto.entryDate?: string | null`.
  - **Diario de ingresos:** lo cubre el §11.2.
- **Fuera:** el filtro `fromDate/toDate` de `GET foreign-trade/deposits` (`GetDepositsHandler.cs:79-88`), que es una búsqueda y no un informe. Se anota en el informe de la fase.

### 11.2 BR-07-002: diario de ingresos con formato legacy

- **Estado:**
  - `B/Wms.Application/Warehouse/Queries/GetDailyIncomingGoodsReport/GetDailyIncomingGoodsReportHandler.cs:39-58` filtra por `CreatedAt`, mezcla todas las modalidades y arma filas por producto (`DailyIncomingGoodsRowBuilder.cs:39-73`).
  - El PDF no muestra el depósito ni las firmas.
  - Legacy de referencia: `L/modulos/mod_inventario/reportediario.php:72-92,340-431`.
- **Consulta:** `GetDailyIncomingGoodsReportQuery(DateOnly? DateFrom, DateOnly? DateTo, string? OperationModalityCode)`.
  - El validador acepta solo `IMP`, `EXP` o `INSP`; si no, 400 «La modalidad debe ser IMP, EXP o INSP.».
  - El handler proyecta con `Select` a registros planos, sin `Include` profundos (trampa §10.11), y usa `ReportDateRange` y `ColombiaTime` en lugar de su `TimeZoneInfo` propio (`:14-15,31-34`).
  - **Candidatos:** depósitos `Confirmed` o `Closed` de la modalidad con `EntryDate` en el rango, **o** con algún `EntryLog.DateTimeEntry` de sus camiones en el rango.
- **Clase pura:** **Nuevo** `B/Wms.Application/Warehouse/Common/Services/DailyIncomingGoodsReportBuilder.cs`. Reemplaza a `DailyIncomingGoodsRowBuilder.cs`, que se borra con `rm`.
  - **Fecha del camión:**
    - el primer camión del depósito (orden por `CreatedAt`, aunque esté anulado) toma `ws.EntryDate ?? EntryLog.DateTimeEntry`;
    - los demás, su `EntryLog.DateTimeEntry`;
    - entra la fila no anulada cuya fecha (`ColombiaTime`) cae en el rango.
  - **Datos por camión:**
    - placa = `VehiclePlate` o la del vehículo del ingreso;
    - tiquete = `TicketNumber`;
    - transportadora = la del vehículo; si falta, el tercero `TRANSPORT_COMPANY`;
    - embalajes y mercancías = los distintos de `EntryProducts`, unidos con «, »;
    - cantidad = Σ `DeclaredQuantity`;
    - pesos `ManifestWeight` y `PhysicalNetWeight`.
  - **Datos por depósito:**
    - agencia `CUSTOMS_AGENCY`;
    - importador según la modalidad: IMP → `IMPORTER` o el cliente; EXP → `EXPORTER` o el cliente; INSP → el cliente;
    - manifiesto DIAN, CPI y `ShippingFormNumber` (D26).
  - **Grupos:** se ordenan por la fecha mínima de sus camiones y luego por número, con subtotales y totales.
- **DTO:** **Nuevos** `DailyIncomingDepositDto.cs` y `DailyIncomingTruckDto.cs`. Se reescribe `DailyIncomingGoodsReportDto.cs` y se borra `DailyIncomingGoodsReportRowDto.cs`.

  ```text
  DailyIncomingGoodsReportDto  { DateFrom, DateTo, OperationModalityCode, GeneratedAt,
                                 TotalVehicles, TotalQuantity, TotalManifestWeightKg, TotalNetWeightKg,
                                 Deposits[] }
  DailyIncomingDepositDto      { WarehouseStorageId, WarehouseStorageNumber, ModalityCode,
                                 CustomsAgencyName, ImporterName, DianManifestNumber,
                                 CommercialDocumentTypeCode, CommercialDocumentNumber, ShippingFormNumber,
                                 TotalVehicles, TotalQuantity, TotalManifestWeightKg, TotalNetWeightKg?,
                                 Trucks[] }
  DailyIncomingTruckDto        { WarehouseStorageEntryId, PreprintedManifestNumber, VehiclePlate,
                                 EntryDateTime, WeighbridgeTicketNumber, CarrierCompanyName,
                                 PackagingTypeNames, Quantity, ManifestWeightKg?, NetWeightKg?, ProductNames }
  ```

- **Endpoints:** en `B/Wms.Api/Controllers/v1/ReportController.cs:56-91`, el JSON y el PDF suman `[FromQuery] string? operationModalityCode`.
- **PDF** (`B/Wms.Application/Warehouse/Common/Services/DailyIncomingGoodsPdfService.cs`), en carta horizontal:
  - un bloque por depósito con el encabezado, la tabla de camiones y su subtotal;
  - al final, «Total vehículos: N», los totales y el bloque de firmas con `ShowEntire()`;
  - rótulo «Importador» en IMP y «Exportador / Cliente» en las demás modalidades.
- **Pantalla** (`F/pages/reports/daily-incoming-goods.vue`):
  - filtro «Modalidad», con IMP por defecto;
  - un panel por depósito con su tabla y el subtotal en `#footer`;
  - un pie con los totales y las tres firmas;
  - botones «Descargar PDF», que pasa la modalidad, y «Exportar Excel».
- **Excel:** **Nuevo** `F/features/reports/utils/daily-incoming-goods-excel.ts`, con `buildDailyIncomingGoodsExcel(report)`.
  - Es plano: Depósito, Agencia e Importador se repiten en cada fila de camión.
  - Lleva la fila de totales.
  - `footerLines = ["Total vehículos: N", "", "______________ Jefe de Bodega", "______________ Recibí conforme DIAN", "______________ Firma Funcionario"]`.
  - Usa el reporte ya cargado: no hace otra llamada.
- **Tipos y servicio:** `F/features/reports/types/daily-incoming-goods.ts`, reescrito, y `F/features/reports/services/reports-service.ts:76-95`, con la modalidad.

### 11.3 De paso (D27)

- **BR-07-005, parcial:** en `F/utils/excel-export.ts:158-167`, el modo de una hoja copia `footerLines`. Arregla también las firmas del resumen de pólizas (`F/pages/reports/policies.vue:105`).
- **BR-07-001:** botón «Exportar Excel» en `F/pages/reports/daily-outgoing-goods.vue`, con las columnas de la pantalla y la fila de totales.
- **BR-07-004:**
  - **Kardex:**
    - `ManifestNumber` = `ImportWarehouseStorage.ManifestNumber`, sin respaldo al manifiesto del camión (`GetWarehouseStorageMovementsHandler.cs:62,308-310`);
    - `CustomsAgencyName` nuevo en `WarehouseStorageMovementsReportDto`, en el PDF (`WarehouseMovementsPdfService.cs`) y en `F/pages/reports/warehouse-movements.vue:370-400`.
  - **Diario de salidas:**
    - `CargoManifestNumber` = el manifiesto DIAN del depósito (`GetDailyOutgoingGoodsReportHandler.cs:180`);
    - la columna «Manifiesto» de `daily-outgoing-goods.vue:340-345`.

### 11.4 Pruebas de la fase 8

- **`Wms.Tests`:** **Nuevo** `B/Wms.Tests/Warehouse/DailyIncomingGoodsReportBuilderTests.cs`, con los ocho casos siguientes. Reemplaza a `DailyIncomingGoodsRowBuilderTests.cs`, que se borra.
  1. Dos depósitos IMP del mismo día.
  2. Un camión tardío en otro día.
  3. Una `EntryDate` corregida.
  4. Un camión anulado.
  5. Cantidad, embalajes y mercancías.
  6. Totales, con neto nulo.
  7. Respaldo del importador y del exportador.
  8. El manifiesto preimpreso distinto del DIAN.
- **`Wms.IntegrationTests`:**
  - **Nuevo** `B/Wms.IntegrationTests/Reports/DailyIncomingGoodsTests.cs`, con `DailyOutgoingGoodsTests.cs` como modelo:
    - dos camiones en días distintos con el manifiesto completado → JSON agrupado;
    - `EXP` excluye los IMP;
    - `XX` → 400;
    - el PDF → `application/pdf`;
    - libera los camiones (trampa §10.12).
  - **Nuevo** `B/Wms.IntegrationTests/Reports/EntryDateReportsTests.cs`: con la fecha corregida, el kardex y las importaciones traen la fecha nueva.
- **Vitest:**
  - **Nuevo** `T/unit/reports/daily-incoming-goods-excel.spec.ts`;
  - `T/unit/utils/excel-export.spec.ts`: el modo de una hoja escribe `footerLines`.

### 11.5 Criterio de salida de la fase 8

- Compuertas del §18.
- Sin migración.

---

## 12. Fase 9 — Migración legacy: año y prórroga (D28, D29)

### 12.1 BR-08-005: número + año

- **Estado:**
  - `B/Wms.Application/Administration/LegacyImport/Importers/DepositsImporter.cs:58-96,154-157,225` agrupa y marca por número.
  - El índice único `idx_warehouse_storage_legacy_number` (`B/Wms.Infrastructure/Persistence/Configurations/Warehouse/WarehouseStorageConfiguration.cs:54-57`) es solo por número.
  - La conciliación (`Commands/ReconcileDeposits/ReconcileDepositsCommand.cs:54-58,78-83`) y los levantes (`Importers/ReleasesImporter.cs:96,164-175`, `Common/LegacyReleaseGrouper.cs:61-62`) también usan solo el número.
- **Cambio:**
  - **Nuevo** `Common/LegacyDepositKey.cs`, con `record LegacyDepositKey(string Number, int Year)`:
    - `Number` = `Trim().ToUpperInvariant()`;
    - `Year` = `r.EntryDate.Year` (ya en hora local: `Common/LegacyValueParsers.cs:73-82`); **no** usar `ToUniversalTime()`;
    - `ToLegacyId()` = `"{Number}@{Year}"`;
    - `ToString()` = «BA0042 (2023)».
  - **Entidad:** `WarehouseStorage.LegacyYear` (`int?`) y un parámetro más en `CreateMigrated`.
  - **Índice:** `HasIndex(ws => new { ws.LegacyNumber, ws.LegacyYear }).IsUnique().HasFilter("legacy_number IS NOT NULL").AreNullsDistinct(false).HasDatabaseName("idx_warehouse_storage_legacy_number_year")`. Migración **`AddWarehouseStorageLegacyYear`**, sin relleno de datos.
  - **Importador de depósitos:**
    - agrupa por `LegacyDepositKey`;
    - marca los errores por (número, año) si la fecha se pudo leer; si no, por número;
    - considera «ya migrado» un depósito cuando hay:
      - una clave igual;
      - un `LegacyYear` nulo con el mismo número y `ColombiaTime.DateOf(EntryDate).Year == año`;
      - o una correspondencia con `ToLegacyId()` o con el número solo.
  - **Conciliación:**
    - `LegacyDepositRowParser.ParseForReconciliation` (`:158-164`) lee también `row[1]`;
    - `LoadAsync(clave)` aplica la misma búsqueda;
    - si hay más de un candidato, responde con el error «el depósito {clave} corresponde a varios depósitos migrados.».
  - **Levantes:**
    - columna 13, opcional, `anio_deposito`;
    - sin ella y con varios migrados del mismo número: «el depósito {n} existe en varios años; exporte la columna anio_deposito.»;
    - `LegacyReleaseGrouper.KeyOf` suma el año.
  - **Documentación:** en `D/planes/paridad-legacy/plan-backend-paridad-legacy.md` F6-03, agregar `YEAR(D.fecha_deposito) AS anio_deposito` a la consulta de levantes (≈`:2990-3011`) y actualizar O-1. Solo se edita el texto; no se ejecuta.

### 12.2 BR-08-003: prórroga

- **Cambio:**
  - **Parser** (`LegacyDepositRowParser.cs:40-41,49-56,65-125`):
    - columna 22, opcional, `prorroga` (índice 21), leída con `LegacyValueParsers.Bool`;
    - `LegacyDepositRow.HasExtension` en `HeaderKey`.
  - **`DepositsImporter.CreateAsync`, bloque IMP (`:201-206`):**
    - si `head.HasExtension`, llama `import.RegisterExtension(run.UserId, "Prórroga registrada en el legacy (depósito {clave}); migrada.")`;
    - en otra modalidad, emite la advertencia «la prórroga solo aplica a importación; se ignora en el depósito {n}.».
    - **Trampa:** la advertencia se emite **dentro del bucle de grupos**, después de `:58-64`, porque `invalidLines` se arma con `outcome.Errors`, que también incluye las advertencias (`LegacyImportContracts.cs:47-48`).
  - **Documentación:** en F6-03 (`plan-backend-paridad-legacy.md:2877-2967`), `D.prorroga` en la subconsulta, `X.prorroga` después de `X.moneda` y la tabla de columnas (`:2884-2887`).

### 12.3 Pruebas de la fase 9

- **`Wms.Tests`:**
  - **Nuevo** `B/Wms.Tests/Administration/LegacyImport/LegacyDepositKeyTests.cs`: la normalización, `2023-12-31 20:00` → 2023 y `ToLegacyId`.
  - `DepositRowParserTests.cs`:
    - la clave de conciliación con el año;
    - `prorroga` en 1, 0, vacía y ausente, con CSV de 19 y 21 columnas;
    - un 2 → «debe ser 1 o 0»;
    - el campo en `HeaderKey`.
  - `LegacyReleaseGrouperTests.cs`: dos BA0042 de años distintos no se agrupan.
- **`Wms.IntegrationTests`:** **Nuevo** `B/Wms.IntegrationTests/Administration/LegacyDepositsSameNumberTests.cs`, sobre `LegacyMigrationScenario.cs`:
  - dos BA0042 vivos (2023 y 2025) → dos depósitos con `legacy_year`;
  - recargar → «ya fue migrado»;
  - levantes con `anio_deposito` → cada uno en su depósito; sin la columna → el error;
  - conciliación `Ok`;
  - el índice rechaza un `(BA0042, 2023)` repetido;
  - un IMP con `prorroga=1` → `HasExtension`, plazo de 60 en `GET foreign-trade/abandonment` y `POST …/extension` responde 409;
  - un EXP con `prorroga=1` → advertencia, y el depósito se migra.

### 12.4 Criterio de salida de la fase 9

- Compuertas del §18.
- La migración `AddWarehouseStorageLegacyYear` aplicada en la base local.

---

## 13. Fase 10 — Respaldos: correo de fallo y destino externo (D32, D33)

- **Estado:**
  - El aviso de fallo solo se ve en la aplicación (`B/Wms.Application/Administration/Backups/Common/BackupService.cs:262-291`, `sendEmail: false` en `:281`).
  - Con la base caída no sale ningún aviso (`:84-87,173-174`; `B/Wms.Api/BackgroundJobs/DatabaseBackupBackgroundService.cs:69-72`).
  - `compose.staging.yaml` no tiene `env_file`, así que el runbook de credenciales S3 (`B/deploy/staging/README.md:197-203`) no funciona.
- **Código:**
  - **Nuevo** `B/Wms.Application/Administration/Backups/Common/BackupFailureMailer.cs`, con `IBackupFailureMailer.SendAsync(notice, ct)`:
    - `BackupFailureNotice` = `(StartedAt, Kind?, Where, Reason, RunId?)`;
    - destinatarios = `MergeRecipients(admins activos, Notifications:AdminEmails)`, sin repetir y sin distinguir mayúsculas;
    - los Admin se leen con `ActiveAdminCounter.EmailsAsync` (nuevo, junto a `CountAsync`, en `B/Wms.Application/Users/Common/ActiveAdminCounter.cs:10-15`), dentro de un `try`: si la base falla, se sigue con la lista;
    - sin destinatarios, solo `LogWarning`;
    - no depende de `Notifications:Enabled`;
    - nunca lanza.
  - **Nuevo** `BackupFailureEmail.Build(notice)`, puro:
    - asunto «[WMS] Falló el respaldo del {dd/MM/yyyy}»;
    - cuerpo en HTML con la hora de Colombia, el tipo, los destinos, el motivo codificado con `WebUtility.HtmlEncode`, el Id corto y «revise `GET administration/backups/runs`».
  - **Dónde se llama:**
    - `BackupService.NotifyFailureAsync`: primero el correo y después el aviso en la aplicación, cada uno en su `try`;
    - el `catch` de `DatabaseBackupBackgroundService.RunJobAsync`;
    - el `catch` de `BackupService.StartManualAsync` (`:66-69`).
  - **Registro:** en `B/Wms.Application/DependencyInjection.cs`.
- **Despliegue:**
  - `B/deploy/staging/compose.staging.yaml`, servicio `wms-api`, bloque de respaldos:

    ```text
    Backups__S3Credentials__s3-externo__AccessKeyId: "${BACKUP_S3_ACCESS_KEY_ID}"
    Backups__S3Credentials__s3-externo__SecretAccessKey: "${BACKUP_S3_SECRET_ACCESS_KEY}"
    ```

    El nombre `s3-externo` debe coincidir con el `name` del destino.
  - Colección Postman `B/deploy/postman/wms-respaldos.postman_collection.json`: «3b. Crear destino S3», con las variables `bucket`, `region` y `prefix` en los dos ambientes.
- **Procedimiento** (reemplaza `B/deploy/staging/README.md:197-203`; resumen en `D/procesos/despliegue-staging.md`). Los ejecuta el usuario, o el agente con aprobación, en la fase 13:
  1. **El usuario** crea un bucket privado de Lightsail en otra región, por ejemplo `us-east-2`, sin acceso público. El plan del bucket se elige con `sizeBytes` de una corrida × 42.
  2. **El usuario** crea la clave de acceso del bucket y la guarda solo en `deploy/staging/.env.staging` como `BACKUP_S3_ACCESS_KEY_ID` y `BACKUP_S3_SECRET_ACCESS_KEY`.
  3. Con aprobación: `scripts/deploy-staging.sh config`, recrear `wms-api` y redesplegar el backend.
  4. `POST administration/backup-destinations` con `{"name":"s3-externo","type":"S3","bucket":"<n>","prefix":"staging","region":"<r>","serviceUrl":null,"isActive":true}`.
  5. `POST administration/backup-destinations/{id}/test` → `success: true`.
  6. `POST administration/backups/run` → `GET …/runs` con dos destinos `Succeeded`.
  7. Fallo provocado con un destino temporal a un bucket inexistente → `PartiallySucceeded` y llega el correo. Después se borra el destino temporal.
  8. Producción: la misma secuencia. El README deja escrita la política: destino local + externo, retención 30 + 12 y aviso por correo (`ROADMAP.md` 0.3).
- **Pruebas:**
  - **`Wms.Tests`:** **Nuevo** `B/Wms.Tests/Administration/BackupFailureEmailTests.cs`:
    - hora de Colombia, HTML codificado e Id corto;
    - `MergeRecipients` sin repetir.
  - **`Wms.IntegrationTests`:** **Nuevo** `B/Wms.IntegrationTests/Administration/BackupFailureEmailTests.cs`, con `InMemoryEmailService`:
    - sin destinos → `Failed` y un correo a los Admin y a la lista;
    - con un destino que falla → `PartiallySucceeded` y un correo;
    - `BackupConcurrencyTests` sigue en verde.
- **Criterio de salida:** compuertas del §18. La configuración de staging queda para la fase 13.

---

## 14. Fase 11 — Guía de salida con código QR de verificación (D35 a D42)

**Pedido del cliente (2026-10-23):** cambiar el código de barras del PDF de la guía de salida por un código QR, para evitar guías adulteradas. El código de barras **se conserva** y se elige por configuración cuál se imprime.

### 14.1 Estado actual

- `FT/Common/Services/DispatchGuidePdfService.cs`:
  - `:345` genera el código de barras con `GenerateCode39Barcode(displayGuideNumber)`, un Code 39 propio dibujado con SkiaSharp (`:784-877`);
  - `:406-410` lo pinta debajo del número de la guía, con altura 50.
- El PDF se genera **en cada descarga**: `GET foreign-trade/dispatch-guides/{id}/pdf` (`B/Wms.Api/Controllers/v1/ForeignTradeController.cs:1143-1155`), el PDF por depósito (`:1166`) y la emisión (`FT/Commands/CreateDispatchGuide/CreateDispatchGuideCommandHandler.cs:423`). Al cambiar el método, las reimpresiones de guías anteriores salen con el método nuevo.
- No hay librería de QR en el proyecto (`B/Wms.Application/Wms.Application.csproj:10-20`).
- Los parámetros del sistema (`SystemParameter`, `admin/parameters`) se siembran con `HasData` (`B/Wms.Infrastructure/Persistence/SeedDataExtensions.cs:230-262`). El PDF ya los lee en cada documento por `ICompanyInfoProvider` (CHG-84), así que un cambio rige sin desplegar.
- `Frontend:BaseUrl` ya existe en la configuración del API: lo usa el correo de recuperación de contraseña (`B/Wms.Application/Auth/Commands/RequestPasswordReset/RequestPasswordResetHandler.cs:72-74`; `B/deploy/staging/compose.staging.yaml:51`).
- El frontend tiene una lista de rutas públicas en `F/middleware/auth.global.ts:7-9`.
- No hay limitador de peticiones en el API.

### 14.2 Configuración: parámetro `GUIDE_CODE_TYPE` (D35, D36)

- **Nuevo** `B/Wms.Application/ForeignTrade/Common/Services/GuideCodeType.cs`, puro:
  - `enum GuideCodeKind { Barcode, Qr }`;
  - `const string ParameterCode = "GUIDE_CODE_TYPE"`;
  - `Parse(string? value)`: `"QR"` → `Qr`; `"BARCODE"` → `Barcode`; nulo, vacío o desconocido → `Barcode` (respaldo seguro);
  - `IsValid(string value)`: solo `BARCODE` o `QR`, sin distinguir mayúsculas.
- **Siembra:** un `SystemParameter` más en `SeedParameters`, con un Id fijo nuevo, `Code = "GUIDE_CODE_TYPE"`, `Value = "QR"` (D37), `DataType = "string"` y la descripción «Código impreso en la guía de salida: QR (verificación) o BARCODE (código de barras).». Migración **`AddGuideCodeTypeParameter`**.
- **Validación al editar:** `B/Wms.Application/Administration/Commands/UpdateSystemParameter/UpdateSystemParameterHandler.cs` rechaza otro valor para ese código con `BadRequestException("El parámetro GUIDE_CODE_TYPE solo admite QR o BARCODE.")`.
- **Lectura:** **Nuevo** `IGuideCodeSettingsProvider` / `GuideCodeSettingsProvider`, en `B/Wms.Application/Common/Services/`, con el patrón de `CompanyInfoProvider`. Lee el parámetro activo en cada PDF; si está inactivo o no existe, `Barcode`.
- **Pantalla:** `F/pages/admin/parameters/index.vue` no cambia. Si el formulario permite texto libre, el error del backend basta. Opcional: un `Select` con las dos opciones cuando el código es `GUIDE_CODE_TYPE`.

### 14.3 Token de verificación firmado (D38)

- **Nuevo** `B/Wms.Application/ForeignTrade/Common/Services/GuideVerificationToken.cs`, puro:
  - `Create(Guid guideId, byte[] key)` = `Base64Url(guideId.ToByteArray() ‖ HMACSHA256(key, "dispatch-guide:" + guideId)[0..16])`: 32 bytes, 43 caracteres;
  - `TryRead(string token, byte[] key, out Guid guideId)`: valida el largo, decodifica, recalcula la firma y compara con `CryptographicOperations.FixedTimeEquals`;
  - no guarda nada en la base: **sin columna**; cubre también las guías ya emitidas.
- **Clave:** configuración `DispatchGuides:VerificationKey`, en base64 de al menos 32 bytes. Se registra con `IOptions<DispatchGuideVerificationOptions>` (`VerificationKey`, `VerificationPath = "verificar/guia"`).
- **Sin clave en modo QR:** el PDF **no se bloquea**. Usa el código de barras, registra `LogError` y envía una notificación a Admin «Falta la clave de verificación de guías: se imprimió código de barras.». Nunca se impide imprimir una guía.
- **Rotar la clave invalida los QR ya impresos:** el runbook dice que solo se rota si se compromete.
- **URL del QR:** `{Frontend:BaseUrl}/{VerificationPath}/{token}`.

### 14.4 Generación del QR en el PDF (D39)

- **Dependencia nueva:** el paquete NuGet **`QRCoder`** (MIT), en `B/Wms.Application/Wms.Application.csproj`, con la versión estable más reciente fijada exacta (se anota en la entrega). Se usa `PngByteQRCode`, que no depende de `System.Drawing`. Si el paquete no restaura o no funciona en Linux (imagen del contenedor), **detenerse y preguntar**: no escribir un codificador QR propio.
- **Nuevo** `B/Wms.Application/ForeignTrade/Common/Services/GuideQrCode.cs`: `Generate(string url)` → PNG, con corrección de errores nivel M y 10 píxeles por módulo; devuelve un arreglo vacío si falla, con el mismo contrato que `GenerateCode39Barcode`.
- **`DispatchGuidePdfService`:**
  - recibe por constructor `IGuideCodeSettingsProvider` e `IOptions<DispatchGuideVerificationOptions>`, y conserva el constructor de pruebas `(AppDbContext)` con valores por defecto: `Barcode`;
  - `GenerateCode39Barcode` y `Code39Patterns` **no se tocan ni se borran**;
  - en `:345`, según `GuideCodeKind`:
    - `Barcode` → lo de hoy;
    - `Qr` → `GuideQrCode.Generate(url)`;
  - en `:406-410`, con `Qr` se pinta un cuadrado de 70 × 70 junto al número de la guía, con el texto debajo, en 7 pt: «Escanee para verificar esta guía»;
  - se aplica igual a la segunda copia (`isSecondCopy`) y al PDF por depósito (ZIP, CF-V056), porque usan el mismo método;
  - el código de barras del PDF del depósito (`DepositPdfService.cs:546-567`) **no cambia**: fuera de alcance.

### 14.5 Verificación pública (D40, D41)

- **Endpoint sin sesión:** **Nuevo** `B/Wms.Api/Controllers/v1/PublicDispatchGuideVerificationController.cs`, con la ruta `api/v1/public/dispatch-guides/verify/{token}` y `[AllowAnonymous]`. Es un controlador aparte, porque los `[Authorize]` se suman (convenciones §4).
  - Token inválido, firma alterada o guía inexistente → **404** con el mismo mensaje para todos los casos: «La guía no existe o el código no es válido.». No se distingue la causa.
  - **Limitador de peticiones:** ASP.NET Core `AddRateLimiter`, ventana fija de 30 peticiones por minuto y por IP, con la política `public-verification` solo en este endpoint.
    - Detrás de Caddy, la IP real llega en `X-Forwarded-For`. Si `Program.cs` no configura `UseForwardedHeaders`, se agrega solo para los proxies conocidos del compose.
    - Si no se puede determinar la IP, la partición es global.
- **Consulta:** **Nuevo** `FT/Queries/VerifyDispatchGuide/` (consulta y handler), con `AsNoTracking` y `Select` a un DTO plano.
- **Datos mínimos** (D41): **Nuevo** `PublicDispatchGuideVerificationDto`, con:
  - `GuideNumber`;
  - `CompanyName`, de `ICompanyInfoProvider`;
  - `IssuedAt` y `DepartureDate`, en hora de Colombia;
  - `Status`: `"Vigente"` o `"Anulada"`, con `CancelledAt` si aplica;
  - `WarehouseStorageNumbers`;
  - `DestinationCity`;
  - `VehiclePlateMasked`;
  - `Lines[]`, con `ProductName`, `Quantity` y `UnitMeasure`;
  - `VerifiedAt`.

  **Nunca:**
  - conductor, destinatario, cliente, documentos de identidad ni teléfonos;
  - valores ni el Id interno.
- **Placa parcialmente oculta:** **Nuevo** `B/Wms.Application/Common/Services/PlateMask.cs`, puro: los 3 primeros caracteres visibles y el resto con `•` (por ejemplo, «ABC•••»). Si tiene 3 caracteres o menos, todo oculto.
- **Frontend, página pública:**
  - **Nuevo** `F/pages/verificar/guia/[token].vue`, con `layout: "auth"` o un layout público mínimo; la ruta `/verificar/` entra en la lista pública de `F/middleware/auth.global.ts:7-9`.
  - Pensada primero para el celular:
    - una franja grande verde «GUÍA VIGENTE» o roja «GUÍA ANULADA el dd/MM/aaaa»;
    - la tabla de datos;
    - la indicación «Compare estos datos con la guía impresa. Si no coinciden, la guía no es válida.».
  - Si el API responde 404, se muestra «Esta guía no existe en el sistema o el código fue alterado.».
  - **Nuevo** servicio `F/features/foreign-trade/services/public-guide-verification.ts`. Usa `$fetch` sin el interceptor de token: no debe redirigir al login.
  - **Nuevo** `F/features/foreign-trade/utils/guide-verification-status.ts`, puro, con la etiqueta y la severidad.
  - Sin menú ni `requiredRoles`.

### 14.6 Configuración del despliegue (D42)

- **`B/deploy/staging/compose.staging.yaml`**, servicio `wms-api`:

  ```text
  DispatchGuides__VerificationKey: "${GUIDE_VERIFICATION_KEY}"
  ```

- **El usuario** genera la clave (`openssl rand -base64 32`) y la pone en `deploy/staging/.env.staging`. El agente no abre ese archivo.
- **`B/deploy/staging/README.md` y `D/procesos/despliegue-staging.md`:**
  - la variable;
  - que no se rota salvo compromiso;
  - que `Frontend__BaseUrl` debe ser la URL pública real, porque es la que queda impresa en el QR.
- **Producción:** la misma variable, con su propia clave.

### 14.7 Pruebas

- **`Wms.Tests`:**
  - **Nuevo** `B/Wms.Tests/ForeignTrade/GuideVerificationTokenTests.cs`:
    - ida y vuelta;
    - un byte alterado → falso;
    - otra clave → falso;
    - largo o base64 inválidos → falso;
    - el token mide 43 caracteres.
  - **Nuevo** `GuideCodeTypeTests.cs`: `Parse` e `IsValid`.
  - **Nuevo** `B/Wms.Tests/Common/PlateMaskTests.cs`.
  - **Nuevo** `GuideQrCodeTests.cs`: devuelve un PNG (firma `89 50 4E 47`) no vacío para una URL de 80 caracteres.
- **`Wms.IntegrationTests`:** **Nuevo** `B/Wms.IntegrationTests/ForeignTrade/DispatchGuideVerificationTests.cs`:
  1. Guía emitida (`ImportExitScenario`): `GET public/dispatch-guides/verify/{token}` **sin token de sesión** → 200, `Status = "Vigente"`, placa oculta y sin campos de conductor ni de destinatario en el JSON.
  2. Después de anular la guía → `Status = "Anulada"` con fecha.
  3. Token con un carácter cambiado → 404; Guid de otra guía con la firma de la primera → 404.
  4. `PATCH` del parámetro con `"XYZ"` → 400; con `"BARCODE"` y luego `"QR"` → 200.
  5. El PDF de la guía responde `application/pdf` en los dos modos. Sin clave en modo QR → igual 200, con la notificación a Admin.
  6. El limitador responde 429 después de 30 peticiones en un minuto.
  7. La factoría de pruebas (`B/Wms.IntegrationTests/Infrastructure/WmsApiFactory.cs`) configura una `DispatchGuides:VerificationKey` de prueba.
- **Vitest:**
  - **Nuevo** `T/unit/foreign-trade/guide-verification-status.spec.ts`;
  - prueba de que `/verificar/guia/x` está en las rutas públicas del middleware.
- **Prueba manual:**
  - imprimir una guía en papel y escanearla con la cámara de un celular Android y de un iPhone: abre la página pública y muestra «Vigente»;
  - anularla y volver a escanear: «Anulada»;
  - cambiar el parámetro a `BARCODE` y reimprimir: sale el código de barras.

### 14.8 Criterio de salida de la fase 11

- Compuertas del §18.
- La migración `AddGuideCodeTypeParameter` aplicada en la base local.
- El paquete `QRCoder` fijado con su versión exacta.
- La guía impresa se verifica con el celular.

---

## 15. Fase 12 — Documentación: procedimiento de corte, QA y estado

### 15.1 BR-08-004: procedimiento del corte (D30, D31)

**Nuevo** `D/planes/migracion-staging/procedimiento-corte-operaciones-abiertas.md`, con estas secciones:

1. **Ventana y responsables:**
   - T0 al cierre de jornada, sin camiones en planta;
   - quién opera cada paso;
   - desde T0, en el legacy solo se consulta y se cobra cartera.
2. **Conteos en el legacy**, en T−1 y en T0. Solo se describen: los corre el usuario en la MariaDB de trabajo, con los filtros de F6-03 (sin eliminados ni el importador 70):
   - **C1.** Camiones en planta: `pesaje` activo sin peso de salida, por modalidad.
   - **C2.** Ingresos pesados sin depósito.
   - **C3.** Órdenes de cargue abiertas.
   - **C4.** Salidas sin guía y guías sin salida de portería.
   - **C5.** Cobros de báscula pendientes, con el criterio de `L/modulos/mod_bascula/cobrarcartera.php:60-70`.
   - **C6.** Períodos de almacenamiento no facturados de depósitos vivos.
   - **C7.** Depósitos vivos con prórroga (BR-08-003).
   - **C8.** Números de depósito repetidos entre vivos (BR-08-005).
   - **C9.** Depósitos vivos y filas del CSV.
3. **Tratamiento por tipo:**

   | Conteos | Tratamiento | Criterio |
   | --- | --- | --- |
   | C1, C2 | Terminar en el legacy antes de T0 o rehacer en V2 desde Vigilancia | Llegar a 0 |
   | C3, C4 | Terminar en el legacy, o anular allí y crear la orden en V2 sobre el depósito migrado | Llegar a 0 |
   | C5 | Se cobran en el legacy o en SIIGO; se entrega la lista a Facturación. V2 no crea facturas a mano (DEC-021) | Lista entregada |
   | C6 | Facturar o anular en el legacy antes de exportar | Llegar a 0 |
   | Levantes después de T0 | Van en V2 | — |
   | C7, C8 | Se cotejan con el lote | — |

4. **Conciliación** en el informe del corte:
   - una tabla por tipo con el conteo en T−1 y en T0, lo cerrado, lo recreado y la diferencia, que debe ser 0;
   - `reconciliation` todo en `Ok`;
   - `open-billing` en `Opened`.
5. **Reversa:**
   - si un conteo no llega a 0, se posterga el corte;
   - si la excepción se acepta, se documenta.
6. **Plantilla del informe:** sin datos de personas (DEC-007).

**Enlaces:**

- `D/planes/migracion-staging/plan-migracion-legacy-staging.md` §3, regla 4: nuevo paso «0. Congelamiento y conteo».
- `D/contexto/estado.md` §4 n.º 7.

**Advertencia:** los nombres de columnas de los conteos salen de `L/bodegas_schema.sql` y se validan contra el volcado nuevo.

### 15.2 Casos de QA

Se agregan o actualizan en `D/qa/fase-*.md`, siguiendo la numeración de cada bloque (D34):

| Fase QA | Casos |
| --- | --- |
| F1 | **F1-TER-0xx** «Bloquear y desbloquear salidas»; **F1-CNV-013** «Programado se activa en su fecha y archiva el anterior» |
| F3 | Reescribir **F3-SBA-002** (sin cliente es válido) y **F3-MUL-004**; nuevos **F3-COR-010**, **F3-COR-011** y **F3-MUL-005** |
| F5 | **F5-OC-022** «Dos órdenes simultáneas»; **F5-OC-023** «Cancelar o modificar con guía vigente»; **F5-GUI-0xx** «Guía antes de un cargue parcial» y «Cliente con salidas bloqueadas»; actualizar **F5-GUI-007** |
| F6 | **F6-ALM-014**: el resultado esperado pasa a «confirma; línea en $0 o al mínimo con advertencia». **F6-ALM-009**: las fórmulas por cantidad cobran el saldo al inicio. Nuevo «salida en los días de gracia». Nuevo «depósito agotado con Borrador sin N.º» |
| F7 | **F7-REP-023** «Fecha de ingreso corregida en informes»; **F7-REP-024** «Diario con formato legacy»; **F7-REP-025** «Diario de salidas a Excel» |
| F5 (QR) | **F5-GUI-0xx** «Guía con QR: escanear con el celular y verificar vigente»; «Guía anulada: la verificación dice Anulada»; «Código alterado: la página dice que no es válido»; «Parámetro `GUIDE_CODE_TYPE` = `BARCODE`: la guía sale con código de barras» |
| F9 | Filas de `ExitBlockAccess` y de los dos endpoints retirados; **F9-API-0xx** «La verificación pública responde sin sesión y no expone datos personales»; «El parámetro `GUIDE_CODE_TYPE` solo lo edita Admin» |
| F11 | **FA-MIG-011** «Mismo número legacy en dos años»; **FA-MIG-012** «Prórroga migrada»; **FA-MIG-013** «Congelamiento: C1–C6 en cero»; **FB-BAK-007** «Destino externo y correo de fallo»; corregir el texto de **FB-BAK-006** (`D/qa/fase-11-regresion-cierre.md:140`) |

### 15.3 Ejecución QA local

- Se ejecutan en local los casos nuevos y los de regresión de cada fase:
  - **F3:** COR-001/003/006, MUL-001…005, SBA-001/002/003, TIQ-002;
  - **F5:** OC-005/007/013…018, GUI-005/007, REL-001;
  - **F6:** ALM-001/008/009/014, REF-005/006, REC-001…007, TAR-*, CNV-009;
  - **F7:** REP-001/002/003/012/018/019/020;
  - **F9:** API-005;
  - **F11:** REG-021, FA-MIG-001/003/004/007, FB-BAK-001…004;
  - **QR:** los casos F5-GUI-0xx (QR) y F9-API-0xx nuevos, con una guía impresa en papel y escaneada con el celular.
- **Informe:** **Nuevo** `D/qa/resultados/P1-informe-2026-10-XX.md`.
- **Defectos:** desde `DEF-F11-028`, registrados en `INDICE.md`.

### 15.4 Documentos que se actualizan

- **Auditoría** `D/analisis/auditoria-paridad-integral-2026-10-23/06-brechas-priorizadas.md`: la columna «Estado» de las 20 brechas pasa a «Corregida (plan P1)» con la fase.
- **`D/contexto/estado.md`:**
  - hito;
  - pendientes n.º 2 y n.º 7;
  - los commits que no están en staging.
- **`D/planes/README.md`:** estado de este plan.
- **Documentación del repo:**
  - `B/deploy/staging/README.md`, ya cambiado en la fase 10;
  - `B/Wms.Application/Warehouse/README.md:134` y `GUIA_USUARIO.md:224`: corregir «la recepción actualiza el stock» (hallazgo de la auditoría).
- **Guía de operarios** (`D/planes/migracion-staging/resultados/guia-pruebas-operarios.md`) y guiones de video afectados (`D/videos/guiones/`), en estos puntos:
  - pesaje único;
  - «Solo báscula» sin cliente;
  - marca «sin salidas»;
  - el diario nuevo;
  - la guía con QR y cómo verificarla.

  Solo se anota qué video queda desactualizado: no se graba.

### 15.5 Criterio de salida de la fase 12

- Casos e informe local con veredicto.
- Defectos bloqueantes corregidos.
- Documentos actualizados.

---

## 15C. Fase 12c — Ajustes de DEC-055 y orden de bloqueo de las guías (D43 a D46)

> Agregada el 2026-10-24, después de la ejecución de las fases 1 a 12 y de la fase 12b (corrección de DEF-F11-028, `planes/registro-ejecucion-brechas-p1-2026-10-24.md`). Va **antes de la fase 13**, para desplegar todo junto.
>
> **Partida:** BE `9e399de` · FE `e2e11e6`. Sin migración en el plan original; con D47 (2026-10-25) suma `RelaxServicePriceActiveIndex`.

### 15C.1 Depósito agotado en la gracia (D43, `DEC-055`, precisa `DEC-053`)

- **Estado:**
  - Al ejecutar un cargue que deja en cero todos los productos de un período, `ExecuteLoadingOrderCommandHandler` (`B/Wms.Application/Warehouse/Commands/LoadingOrder/ExecuteLoadingOrderCommandHandler.cs:275-293`, dentro de la transacción del cargue) llama a `StorageBillingService.CloseDepletedProductPeriodsAsync` (`B/Wms.Application/Billing/Common/Services/StorageBillingService.cs:1037`).
  - Ese método cierra el período `Open` aunque su fin ya haya pasado, es decir, en los días de gracia. El job (`B/Wms.Application/Billing/Jobs/BillingJobService.cs:154-282`) nunca lo ve vencido y **no lo renueva**: el período que empezaba el día S (`fin + 1`) no se abre ni se cobra.
- **Cambio** (se reutiliza la renovación del job; **no** se renueva dentro de la transacción del cargue):
  1. **`CloseDepletedProductPeriodsAsync`** deja de cerrar un período agotado cuyo `PeriodEnd`, en hora de Colombia, ya pasó (`ColombiaTime.DateOf(PeriodEnd) < ColombiaTime.Today`). Lo deja `Open` para que lo renueve el job, y lo registra con `LogInformation`: «Período {Id} agotado en la gracia: queda para la renovación (DEC-055).». La regla va en una función pura **nueva**, `StorageDepletionRules.ShouldCloseOnDepletion(periodEnd, today)`. Los períodos que todavía están en curso se cierran como hoy.
  2. **`BillingJobService.AutoCloseExpiredStoragePeriodsAsync`:** después del paso 3 (`OpenPeriodWithInvoiceAsync`, `:238-242`) y antes del commit, llama `scopedStorageBilling.CloseDepletedProductPeriodsAsync(deposit.WarehouseStorageId, ct)`. El período renovado, con la cantidad al cierre del día S (D19), queda facturado y cerrado por agotamiento en la misma transacción.
     - Si la cantidad al cierre del día S es cero (todo salió el día S o antes), `ResolveStorageChargesAsync` no devuelve cargos, «no se abre período» (`StorageBillingService.cs:477-480`) y queda solo el cierre del período viejo, como hoy.
  3. **`CloseStoragePeriodsHandler`** (`B/Wms.Application/Billing/Commands/CloseStoragePeriods/CloseStoragePeriodsHandler.cs:61-65`, cierre manual) hace lo mismo después de abrir la renovación.
  4. **Avisos:** la renovación avisa a Facturación con lo que ya existe (`StorageBillingNotifier.NotifyPeriodRenewedAsync` y las advertencias). No hay aviso nuevo.
- **Qué no cambia:**
  - El estado del depósito: sigue `Closed` al agotarse (`ExecuteLoadingOrderCommandHandler.cs:275-281`).
  - El cálculo, que sigue siendo uno solo (DEC-027).
  - Los períodos en curso.
  - Lo que sale el día S, que no se cobra (D19).
- **Efecto visible:** durante los días de gracia, un depósito agotado sigue con su período abierto hasta que corre el job. Aparece en «Depósitos pendientes» con período abierto (D22).
- **Pruebas:**
  - **`Wms.Tests`:** **Nuevo** `B/Wms.Tests/Billing/StorageDepletionRulesTests.cs`:
    - período en curso → se cierra;
    - fin ayer → no se cierra;
    - fin hoy → se cierra.
  - **`Wms.IntegrationTests`:** **Nuevo** `B/Wms.IntegrationTests/Billing/DepletedInGraceRenewalTests.cs`, con fechas hacia atrás vía `ExecuteUpdateAsync`, como en `StorageRenewalAtPeriodStartTests`:
    1. `PER_UOM` de 10 con fin = hoy − 2; se cargan las 10 hoy, es decir `fin + 2`:
       - el período viejo sigue `Open` después del cargue;
       - se fecha el límite hacia atrás y se ejecuta el job;
       - hay una factura nueva por 10, con `StockAtBilling = 10`, y el período renovado queda `Closed`;
       - no hay aviso de fallo.
    2. Lo mismo, pero con el movimiento fechado en el día S: el job no abre período y el viejo queda cerrado.
    3. Agotamiento dentro del período (fin = mañana): se cierra al cargar, como hoy.
    4. Siguen en verde `StorageRenewalAtPeriodStartTests`, `ManualPeriodCloseTests`, `PendingDepositsListTests` y `StorageRecalculationDispatchTests`.
  - **QA:** proponer **F6-ALM-0xx** «Depósito agotado en la gracia: se cobra el período del día S»; re-ejecutar F6-ALM-009 y F6-ALM-018.

### 15C.2 Orden de bloqueo de las guías (D44)

- **Estado:**
  - **Importación** (`FT/Commands/CreateDispatchGuide/CreateDispatchGuideCommandHandler.cs`): bloquea la orden (`:60`), toma el consecutivo `S` (`foreignTradeService.GenerateGuideNumberAsync`, `:229`, que bloquea `document_sequences`) y **después** bloquea los productos en `FreezeLinesAsync` (`:249`).
  - **Exportación** (`FT/Commands/CreateExportDispatchGuide/CreateExportDispatchGuideCommandHandler.cs`, que el cargue lanza **después** de su commit, `ExecuteLoadingOrderCommandHandler.cs:408`): abre su propia transacción (`:102`), toma `S` (`:122`) y bloquea los productos en `FreezeLinesAsync` (`:142`). **No** bloquea la orden.
  - Las dos van contra el orden global de D5 (orden → productos → consecutivos).
- **Cambio:**
  - **Importación:** después de `LockLoadingOrderAsync` (`:60`) y antes de tomar el consecutivo, `StockRowLock.LockStorageProductsAsync(context, await StockRowLock.OrderProductIdsAsync(context, loadingOrderId, ct), ct)`.
  - **Exportación:** al abrir la transacción (`:102`), `StockRowLock.LockLoadingOrderAsync`, y luego `LockStorageProductsAsync` con los productos de la orden. Después se vuelve a leer «ya existe guía vigente» bajo el bloqueo, como en la de importación.
  - `FreezeLinesAsync` sigue con su `FOR UPDATE … ORDER BY id` (`FT/Common/Services/DispatchGuideBalanceService.cs:29-30`). Reentrar un bloqueo propio en la misma transacción no espera.
  - El comentario de `StockRowLock` deja escrito que las guías siguen el mismo orden.
  - La numeración sigue sin saltos (DEC-012): el consecutivo se toma dentro de la misma transacción, solo que más tarde.
- **Pruebas:** en `B/Wms.IntegrationTests/ForeignTrade/LoadingOrderConcurrencyTests.cs`:
  - **Nuevo, determinista:** con `FOR UPDATE` de un producto de la orden tomado desde un `CreateStandaloneDbContext`, `POST foreign-trade/dispatch-guides` espera y **no** tiene tomado el consecutivo mientras espera. Comprobación: con la petición bloqueada, otra transacción toma y libera la fila de `document_sequences` de `S` sin esperar.
  - **Nuevo:** dos emisiones de guía de importación simultáneas para la misma orden → una 201 y la otra 409 «ya existe guía vigente»; consecutivos sin saltos.
  - **Nuevo:** guía de exportación automática después de un cargue, sin cambio funcional (regresión de `CreateExportDispatchGuide`).

### 15C.3 Precios de servicio programados (D45, D46, `DEC-055`)

- **Estado:**
  - `B/Wms.Application/Services/Commands/SetServicePrice/SetServicePriceValidator.cs:16-19` rechaza una vigencia futura: «La fecha de inicio de vigencia no puede ser futura.». El comentario cita «ALM-20/D20», de una fuente que ya no existe (`D/contexto/mapa-de-fuentes.md` §7).
  - El dominio ya lo soporta desde la fase 6: `Service.SetPrice` (`B/Wms.Domain/Entities/Service/Service.cs:56-65`) vence los activos en `max(ahora, validFrom) − 1 tick`.
  - El precio vigente ya filtra `ValidFrom <= ahora`, tanto en `Service.CurrentPrice` (`:19`, `IsCurrentlyActive`) como en `GetAllServicesHandler.cs:46-48` y en el resolutor de tarifas.
  - La lista (`F/features/services/components/ServicePricesList.vue:33-35`) marca «Vigente» todo precio con `isActive`, incluido uno futuro.
- **Cambio:**
  - **Backend:**
    - el validador deja de rechazar las fechas futuras; conserva el resto (precio ≥ 0, vencimiento posterior al inicio);
    - el comentario cita `DEC-055`, que reemplaza a ALM-20/D20;
    - el handler de `SetServicePrice` normaliza `ValidFrom` a `ColombiaTime.StartOfDayUtc(ColombiaTime.DateOf(validFrom))` cuando es futura: el precio entra a las 00:00 de Colombia de ese día. Una fecha de hoy o pasada se guarda como hoy (sin cambio).
  - **Regla de reemplazo (D46):** registrar un precio nuevo deja inactivos los precios programados que empiezan después de él. Es lo que ya hace `SetPrice`: los vence en `validFrom − 1` y `Expire` los desactiva si el vencimiento cae antes de su inicio. Solo se documenta en el comentario de `Service.SetPrice`.
  - **DTO:** `ServicePriceDto` suma `IsScheduled`, calculado como `IsActive && ValidFrom > ahora`, en el mapper (`B/Wms.Application/Services/Common/Mappers/ServiceMapper.cs`) y en las proyecciones que listan precios.
  - **Frontend:**
    - `F/features/services/components/ServicePricesList.vue`:
      - `Tag`: «Programado» (`info`) si `isScheduled`, «Vigente» (`success`) si está activo y vigente, «Histórico» (`secondary`) si no;
      - el `DatePicker` «Vigente desde» acepta fechas futuras y muestra la ayuda «Una fecha futura programa el precio: el vigente rige hasta la víspera.»;
      - la fecha se envía como el día elegido en Colombia (`yyyy-MM-ddT00:00:00-05:00`, como los convenios en la fase 7).
    - Tipo `isScheduled?: boolean` en `F/features/services/types/service.ts`.
    - **Nuevo** `F/features/services/utils/service-price-status.ts`, puro, con la etiqueta y la severidad.
- **Permisos:** sin cambio. `POST service/{id}/prices` sigue con su política actual (Admin y Billing, `BillingAccess`); la pantalla, igual.
- **Agregado en la ejecución (2026-10-25, D47 y D48):**
  - el índice único de un precio activo por servicio respondía 409 al programar un precio: pasa a uno por servicio y día de inicio, con la migración `RelaxServicePriceActiveIndex`;
  - el precio de la guía sin convenio (`ForeignTradeService.GetGuidePriceAsync`) filtra por fechas, como el resolutor: con un precio programado, la guía cobra el vigente. Prueba en `ScheduledServicePriceTests` (caso 4).
- **Pruebas:**
  - **`Wms.Tests`:**
    - **Nuevo** `B/Wms.Tests/Services/SetServicePriceValidatorTests.cs`: una fecha futura es válida; un precio negativo y un vencimiento anterior al inicio no lo son;
    - `ServiceSetPriceTests` (fase 6) suma un caso: un precio programado más tarde queda inactivo al registrar uno anterior.
  - **`Wms.IntegrationTests`:** **Nuevo** `B/Wms.IntegrationTests/Services/ScheduledServicePriceTests.cs`:
    1. `POST service/{id}/prices` con un precio para mañana → 201, `isScheduled = true`, y el precio vigente sigue siendo el anterior.
    2. La tarifa de un cobro de hoy usa el anterior. Con `ValidFrom` fechado hacia atrás con `ExecuteUpdateAsync`, el cobro usa el nuevo, sin hueco: el anterior vence la víspera.
    3. Un precio inmediato después de uno programado deja inactivo al programado.
  - **Vitest:** **Nuevo** `T/unit/services/service-price-status.spec.ts`.
  - **QA:** proponer **F1-SRV-0xx** «Programar un precio y verlo entrar en su fecha» y re-ejecutar los casos de tarifas F6-TAR-* y F3-COB.

### 15C.4 Documentación de la fase

- `D/qa/fase-01-administracion.md` y `fase-06-facturacion.md`: los casos nuevos.
- `D/planes/registro-ejecucion-brechas-p1-2026-10-24.md`: la fase 12c.
- §17 de este plan: el estado de la fase 12c.

### 15C.5 Criterio de salida de la fase 12c

- Compuertas del §18.
- Migración `RelaxServicePriceActiveIndex` (D47) y `has-pending-model-changes` limpio.
- Las pruebas nuevas de los tres cambios en verde.

---

## 16. Fase 13 — Despliegue a staging y QA en staging (con aprobación)

Cada paso que toca staging necesita un «sí» explícito del usuario. Runbook: `B/deploy/staging/README.md` y `D/procesos/despliegue-staging.md`.

### 16.1 Antes de desplegar

1. **Conteo de convenios activos duplicados (D21).** Consulta en solo lectura, con aprobación: clientes con más de un convenio `Active`. Si hay alguno, **detenerse y preguntar** qué convenio queda activo. No se corrige con SQL (DEC-006).
2. **Convenios programados vencidos:** listarlos, en solo lectura y con aprobación. Rigen en cuanto se despliega y el job los activa (D20). Se informa al usuario cuántos son.
3. **Respaldo previo:** `deploy-staging.sh backup`.
4. **Migraciones pendientes:**
   - `20261008230241_AddForkliftUseEntryLog`, que trae `83de58a` y ya estaba pendiente;
   - `AddStakeholderExitBlock`;
   - `FixAgreementActiveStakeholderIndex`;
   - `AddWarehouseStorageLegacyYear`;
   - `AddGuideCodeTypeParameter`;
   - `RelaxServicePriceActiveIndex` (fase 12c, D47).

   Se aplican con un script idempotente (`dotnet ef migrations script --idempotent`).

### 16.2 Despliegue

- `deploy-staging.sh` en el orden del runbook: backend con `migrate`, frontend y `config` (fase 10).
- Los pasos 1–7 del procedimiento de respaldos del §13.
- **QR de la guía:** antes de desplegar el backend, el usuario genera la clave (`openssl rand -base64 32`) y la guarda en `deploy/staging/.env.staging` como `GUIDE_VERIFICATION_KEY`. Después, con aprobación, se aplica `config` y se comprueba `Frontend__BaseUrl`. Prueba con un celular: escanear una guía impresa en staging → la página pública dice «Vigente».

### 16.3 QA en staging

- **Humo:** los casos de §15.3 marcados P0 con las cuentas `qa.*`. No se modifican conductores ni terceros migrados reales (DEC-017): se usan los datos `PRAC-` y `QA-SEL`.
- **Respaldo:** FB-BAK-007 con el bucket externo.
- **Aviso a Facturación sobre BR-06-005:** las renovaciones abiertas pueden subir en su próximo recálculo.
- **PRF-002** lo mide un operario real con este build, si el usuario lo programa (DEC-042).
- **Informe:** se agrega una sección de staging en el informe de §15.3.

---

## 17. Orden y checkpoints

| Fase | Repo | Entrega | El agente se detiene y… | Estado |
| --- | --- | --- | --- | --- |
| 1 | BE, FE | §4 | resume; commit sugerido: `refactor(api): retira endpoints sin uso de ingresos y órdenes de Bodega; leyenda no fiscal en tiquete y factura` | Commiteada: BE `267bef6` / FE `7963a4f` (commits del usuario, 2026-10-24) |
| 2 | BE, FE | §5 | `fix(salidas): bloqueo de stock en órdenes, levantes y guías; anular la guía antes de cancelar o modificar la orden` | Commiteada: BE `a7bd8ef` / FE `9c64ca5` / docs (este commit) — 2026-10-24, orquestador |
| 3 | BE, FE | §6 y la migración `AddStakeholderExitBlock` | `feat(salidas): aviso de guía distinta a lo cargado y bloqueo manual de salidas por cliente` | Commiteada: BE `272b785` / FE `b1b27fa` / docs (este commit), con la migración `20261024144232_AddStakeholderExitBlock` — 2026-10-24, orquestador |
| 4 | BE, FE | §7 | `fix(bascula): corrección por pesaje con neto por depósito; Solo báscula sin cliente` | Commiteada: BE `157503b` / FE `8e4deb2` / docs (este commit) — 2026-10-24, orquestador |
| 5 | BE, FE | §8 | `feat(bascula): un solo pesaje para varios documentos con neto prorrateado y tiquete por depósito` | Commiteada: BE `9ba1380` / FE `8dba8a8` / docs (este commit) — 2026-10-24, orquestador |
| 6 | BE | §9 | `fix(facturacion): respaldo del servicio complementario, precio futuro y renovación con el saldo al inicio` | Commiteada: BE `7e3e150` / docs (este commit); sin cambios de FE — 2026-10-24, orquestador |
| 7 | BE, FE | §10 y la migración `FixAgreementActiveStakeholderIndex` | `feat(facturacion): activación de convenios programados, índice de convenio activo y depósitos pendientes cerrados` | Commiteada: BE `cc832b3` / FE `682e1f7` / docs (este commit), con la migración `20261024155558_FixAgreementActiveStakeholderIndex` — 2026-10-24, orquestador |
| 8 | BE, FE | §11 | `feat(reportes): diario de ingresos con formato legacy, fecha de ingreso, manifiesto DIAN y Excel de diarios` | Commiteada: BE `02c0b32` / FE `ae20d54` / docs (este commit) — 2026-10-24, orquestador |
| 9 | BE, docs | §12 y la migración `AddWarehouseStorageLegacyYear` | `feat(migracion): depósitos legacy por número y año; prórroga migrada` | Commiteada: BE `f37f353` / docs (este commit), con la migración `20261024163412_AddWarehouseStorageLegacyYear`; sin cambios de FE — 2026-10-24, orquestador |
| 10 | BE, deploy, docs | §13 | `feat(respaldos): correo de fallo y destino S3 externo` | Commiteada: BE `30df3b0` (código y `deploy/`) / docs (este commit); sin cambios de FE — 2026-10-24, orquestador |
| 11 | BE, FE, deploy | §14 y la migración `AddGuideCodeTypeParameter` | `feat(guias): código QR de verificación en la guía de salida, seleccionable por parámetro` | Commiteada: BE `560f558` / FE `e2e11e6` / docs (este commit), con la migración `20261024170332_AddGuideCodeTypeParameter` y `QRCoder` fijado en `[1.8.1]`; el escaneo con celular y la prueba en la imagen Linux quedan para la fase 13 — 2026-10-24, orquestador |
| 12 | docs | §15 | entrega el veredicto local; commit del hub | Commiteada: BE `2f18fee` (solo documentación) / docs (este commit). Veredicto QA local: continuar con condiciones (DEF-F11-028 MAJOR abierto) — 2026-10-24, orquestador |
| 12b | BE | DEF-F11-028 (fase aparte pedida por el usuario el 2026-10-24, antes de la 13) | `fix(facturacion): «Depósitos pendientes» incluye el depósito agotado (Cerrado e inactivo) con factura por numerar o refacturar (DEF-F11-028)` | Commiteada: BE `9e399de` / docs (este commit); re-test local de F6-ALM-018, F6-REF-005 y F6-REF-006: PASA — 2026-10-24 |
| 12c | BE, FE | §15C y la migración `RelaxServicePriceActiveIndex` (D47) | `fix(facturacion,guias,servicios): renovación del depósito agotado en la gracia, orden de bloqueo de las guías y precios de servicio programados (DEC-055)` | Implementada el 2026-10-25 sobre BE `9e399de` / FE `e2e11e6`, sin commit; con la migración `20261025152149_RelaxServicePriceActiveIndex` y D47–D48. Pendiente del commit del usuario |
| 13 | staging | §16 | entrega el informe de staging y los mensajes de commit pendientes | Pendiente |

Cada fase entrega su resumen y espera el commit del usuario antes de la siguiente (`DEC-003`).

---

## 18. Compuertas de cada fase

- `dotnet build Wms.sln` sin errores.
- `dotnet test Wms.Tests` y `dotnet test Wms.IntegrationTests` en verde. La segunda necesita Docker; sin Docker, `--filter Category!=Integration` y avisarlo.
- `dotnet ef migrations has-pending-model-changes` limpio.
- En `Frontend/wms`:
  - `yarn build` con código 0;
  - `yarn test` en verde, guardias incluidas;
  - `yarn lint` con igual o menos errores que la fase anterior y cero en archivos nuevos.
- Informar las cifras: pruebas antes y después, errores de lint antes y después.

---

## 19. Riesgos conocidos

| Riesgo | Mitigación |
| --- | --- |
| Interbloqueos al agregar `FOR UPDATE` en 8 handlers | Orden global fijo de D5 y `ORDER BY id`; prueba determinista del §5.1 |
| Un bloqueo largo mientras sube el soporte de la orden externa | Aceptado: solo esperan las operaciones sobre los mismos productos |
| La migración del índice de convenios falla con duplicados en staging | Conteo previo (§16.1); detenerse y preguntar |
| Las facturas abiertas de staging suben en su próximo recálculo (BR-06-005) | Es lo que pide DEC-053; DEC-022 notifica; aviso en §16.3 |
| El neto prorrateado cambia en un depósito ya validado | D14: la observación conserva su valor; se documenta en F3-MUL-005 |
| Un papel por depósito alarga la báscula | Medición dentro de PRF-002 |
| El cambio de contrato del diario de ingresos | Backend y frontend en la misma fase (8) |
| Las columnas de los conteos del corte no coinciden con el volcado nuevo | Advertencia en el procedimiento; se validan en el ensayo del corte |
| Correos de fallo a cuentas de prueba (Gmail real en staging) | Verificar los correos de las cuentas Admin antes del paso 7 de §13 |
| Endpoint público nuevo (el primero de negocio sin sesión) | Token firmado sin enumeración, 404 único, limitador por IP y datos mínimos (D40, D41); F9-API-0xx |
| Se pierde o se rota la clave de verificación | Las guías impresas dejan de verificarse: la clave se guarda con los secretos del ambiente y no se rota salvo compromiso (D42) |
| `QRCoder` no funciona en la imagen Linux | Se prueba en el contenedor en la fase 13; si falla, detenerse y preguntar (§14.4) |
| QR ilegible en la impresora de la guía | Prueba manual de escaneo en papel (§14.7); tamaño mínimo de 70 × 70 y corrección de errores M |
| Guiones de video y guía de operarios desactualizados | Se anotan en la fase 12; se regraban fuera de este plan |
