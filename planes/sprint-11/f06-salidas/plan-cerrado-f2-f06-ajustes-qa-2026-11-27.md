# Plan cerrado — Fase 2 · F06 Salidas de mercancía · Ajustes de la QA manual de la integración

> **Fecha:** 27 de noviembre de 2026. **Estado:** Aprobado por el usuario el 2026-11-27 («Apruebo el plan»), con un cambio posterior del mismo día: solo dos métodos de pago, «Efectivo» y «Transferencia» (D4, D11). Sin ejecutar: AQ-1 (backend) y AQ-2 (frontend) pueden ir en paralelo; AQ-3 va después de las dos.
> **Origen:** la prueba manual del usuario sobre F06 integrada (I-06): [`../qa-manual/hallazgos-int-F06.md`](../qa-manual/hallazgos-int-F06.md), con los mockups [`../qa-manual/modal-confirmar-salida/`](../qa-manual/modal-confirmar-salida/) y [`../qa-manual/formulario-cobro-compartido/`](../qa-manual/formulario-cobro-compartido/). Las respuestas del usuario del 2026-11-27 están en D1 a D4.
> **Base:** BE `fase-2` `335eb25` · FE `fase-2` `3069cb7` · docs `main` `f3f4e0f`.
> **Alcance:** backend y frontend. Backend: el cuerpo de la confirmación (C-F06-05) recibe el firmante y deja de recibir observaciones (la guía toma las de la salida), y el cobro sugerido (C-F06-06) informa el firmante sugerido y si «Importador» es posible. Frontend: el formulario de cobro compartido (`AppChargeForm`) rediseñado en sus tres vistas (Báscula, montacargas y la confirmación de la salida) y en la galería, y el modal de confirmación de la salida rediseñado. Sin migraciones. Cambia decisiones del plan de F06 (D4, D12, D13) y del plan de F02 (D13, AF-132). Donde chocan, gana este plan.
> **Rutas:** relativas a `code_workspace/`. Prefijos: `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`; `P06/` = `D/planes/sprint-11/f06-salidas/plan-cerrado-f2-f06-salidas-2026-11-26.md`; `H/` = el archivo de hallazgos; `MK1/` = el mockup del modal; `MK2/` = el mockup del cobro.

---

## 0. Instrucciones para el ejecutor

1. **Lecturas mínimas:** los dos `AGENTS.md` de los repos, `D/procesos/flujo-de-trabajo-agentes.md`, `P06/` D4, D12, D13 y C-F06-05, C-F06-06 (§2.2), `H/`, los dos mockups (la imagen `@1x.png` y los estilos de su `.dc.html`) y este plan completo.
2. **Ramas y git:** `f2/f06-ajustes-qa` en BE y en FE, desde `fase-2`. Commit y push al cerrar cada fase, con el mensaje de §7. Al cerrar la fase AQ-3, fusión en `fase-2` con `--no-ff` en los dos repos y push. Sin `push --force`. Para borrar, `rm`. `test/.nuxtrc`, `components.d.ts` de la raíz y `.claude/launch.json` del frontend tienen cambios ajenos: no se suben.
3. **Una fase por turno** (`AGENTS.md`): al cerrar cada una, compuertas (§6), commit, estado en este plan (§4) y en la matriz, y reporte.
4. **Líneas citadas:** confírmalas con grep antes de cambiar. Si el código no coincide, detente y pregunta con todas las dudas en un solo mensaje. Si un caso borde choca con una Dn, gana la Dn (`DEC-002`).
5. **Staging:** no se toca. **Credenciales y datos reales:** no se copian (`DEC-007`).

---

## 1. Decisiones

Mandan sobre el resto del plan (`DEC-002`).

### 1.1 Respuestas del usuario (2026-11-27)

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **Firmante sugerido y bloqueo.** El modal pregunta «¿Quién firma la guía de salida?» con «Importador» y «Conductor» (tarjetas de radio, obligatorio). Se preselecciona «Importador» si los depósitos de la salida tienen un único importador registrado y un único cliente; si no, «Conductor». «Importador» queda deshabilitado, con su motivo en el tooltip, cuando no es posible: depósitos de varios clientes o varios importadores («Con depósitos de varios clientes o importadores firma el conductor.»), o sin importador registrado («Los depósitos no tienen importador registrado.»). Es la regla de hoy de la guía por orden (`B/Wms.Application/ForeignTrade/Common/Services/DispatchGuideSignerRules.cs:15-42`, CHG-34) y reemplaza la del emisor de F06, que decidía solo (`B/Wms.Application/Exits/Common/ExitGuideIssuer.cs:93-104`: conductor, salvo la global con un importador) | Usuario: «Sugerido + bloqueo (Recomendada)»; `H/` 2 |
| D2 | **Total fijo con desglose, en todas las vistas.** El cobro ya no edita el total: muestra el desglose del precio (`MK2/`): «{origen del precio}» con el valor, «IVA ({tasa} %)» y «Total a cobrar» (con «Pago inmediato») o «Total pendiente» (con «Pendiente por facturar»). En la guía sale de C-F06-06 (`unitPrice`, `taxRate`, `taxAmount`, `totalAmount`); en Báscula, del cobro de C-F03 (`weighingPrice`, `taxAmount`, `totalAmount`); en el montacargas, de su cálculo de hoy (base, IVA y total). Cambia D4 de F06 («`editableTotal`»): sale la prop `editableTotal` | Usuario: «Fijo con desglose (Recomendada)»; `MK2/` |
| D3 | **El componente de cobro no trae botón.** Cada vista pone el suyo, con el total: el modal de la salida, en su pie, «Emitir guía y cobrar {total}» (`MK1/`); Báscula, en el pie de su tarjeta de cobro, «Cobrar {total}» (sigue Enter = Cobrar); el montacargas, en el pie de su modal, «Finalizar y cobrar {total}». El componente expone `submit()` (como hoy, `defineExpose`) y emite `submit` con el `BillingRecipientInput`; salen las props `submitLabel` y `submitting` | Usuario: «En cada pantalla (Recomendada)»; `MK1/` |
| D4 | **Lo que se conserva y lo que sale.** Se conserva el conductor editable: al elegir «Conductor del vehículo» los datos se precargan y se pueden corregir (hoy, `F/components/app/AppChargeForm.vue:118-128`). **Salen** la «Referencia» del pago (AF-132 la pedía con otro método; el backend no la exige, `ProcessOutputPaymentValidator.cs:29` solo la valida si viene), el «Teléfono» de la persona no registrada y cuatro métodos de pago: quedan solo «Efectivo» y «Transferencia» (D11; cambio del usuario del 2026-11-27 sobre `MK2/`, que mostraba también «Tarjeta débito / crédito»). El componente envía `referenceNumber: null` (salvo la factura en cero, `ZERO-INVOICE`, como hoy) y la persona no registrada sin teléfono | Usuario: conservar solo «Conductor editable»; `MK2/` |

### 1.2 Observaciones (`H/` 1; fases AQ-1 y AQ-3)

| # | Decisión | Fuente |
| --- | --- | --- |
| D5 | **La guía imprime las observaciones de la salida.** Al emitir la guía, `ExitGuideIssuer.IssueAsync` guarda en la guía `exit.Observations` (`B/Wms.Domain/Entities/Warehouse/GoodsExit.cs:37`), no las del cuerpo de la confirmación. `ExitConfirmRequest.Observations` sale (`B/Wms.Application/Exits/Commands/ConfirmExitCommand.cs:18`, `:42`, `:101`); un cliente viejo que la envíe no rompe (el JSON con campos de más se ignora). Al reabrir y reconfirmar, la guía nueva toma las observaciones vigentes de la salida (se editan en Borrador). La inspección no lleva guía: sin cambio | `H/` 1 |
| D6 | **Texto del paso 8 del formulario** (`F/features/exits/components/ExitForm.vue:465`): «Se imprimen en la guía al confirmarla.» (hoy: «No se imprimen en la guía; las de la guía se escriben al confirmar.») | `H/` 1 |

### 1.3 Firmante (`H/` 2; fases AQ-1 y AQ-3)

| # | Decisión | Fuente |
| --- | --- | --- |
| D7 | **C-F06-05 recibe `signerType`** (`"Importer"` o `"Driver"`), obligatorio cuando la salida emite guía (no en inspección, que lo ignora). El backend lo valida con la regla de D1, extraída a una clase pura junto a `DispatchGuideSignerRules` y probada en `Wms.Tests`: sin `signerType`, 400 «Elija quién firma la guía.»; «Importador» con varios clientes o importadores, 400 «Con depósitos de varios clientes o importadores firma el conductor.»; «Importador» sin importador registrado, 400 «Los depósitos de la salida no tienen importador registrado: elija al conductor como firmante.». El nombre que se imprime sigue como hoy: el importador del depósito o «{nombres} {apellidos} ({cédula})» del conductor | `H/` 2; D1 |
| D8 | **C-F06-06 informa el firmante** con un objeto nuevo `signer`: `suggested` (`"Importer"` o `"Driver"`, D1), `importerName` (nulo si no hay uno solo), `importerAvailable` y `importerUnavailableReason` (nulo o el motivo de D1). El modal lo usa para preseleccionar y deshabilitar; el esquema Zod de §2 lo valida | D1 |

### 1.4 Formulario de cobro compartido (`H/` 3, `MK2/`; fase AQ-2)

| # | Decisión | Fuente |
| --- | --- | --- |
| D9 | **Forma de `AppChargeForm`** (`F/components/app/AppChargeForm.vue`), con los valores del `.dc.html` de `MK2/` llevados a clases y tokens del proyecto (tema claro y oscuro, sin colores fijos): tarjeta con encabezado (icono de tarjeta, título por prop `title` y, si llega, la etiqueta del origen del precio por prop `priceSourceLabel`: «Precio general» o «Convenio»); «¿A quién se le cobra?» con los cuatro destinatarios como tarjetas de radio en dos columnas (la elegida con borde primario y fondo tenue; «Conductor del vehículo» deshabilitada si no hay conductor); según el destinatario: «Tercero» con `AppSearchSelect` y el botón «+» de alta rápida a su derecha (no dentro de la lista); el conductor, con sus datos precargados y editables (D4); la persona no registrada, con «Nombre completo» y «Documento» (tipo y número en una fila); el consumidor final, con el texto «Se cobra a consumidor final (NIT 222222222222). No hace falta registrar datos del comprador.»; separador; «Modo de pago» como control segmentado (solo si hay más de un modo, como hoy); «Método de pago» solo con «Pago inmediato»; con «Pendiente por facturar», el texto «El valor queda pendiente en la cuenta del destinatario y se incluye en la próxima factura.»; y el bloque del desglose de D2. Con `zeroValue` (Báscula: convenio en $0 o entrada duplicada) se queda como hoy: solo el destinatario y el aviso «Factura en $0» | `MK2/`; D2 a D4 |
| D10 | **Props** de `AppChargeForm`: salen `total`, `editableTotal`, `submitLabel` y `submitting`; entran `title` (por defecto «Cobro»), `priceSourceLabel` (opcional) y `breakdown: { baseLabel: string; base: number; taxRate: number; tax: number; total: number }`. El resto sigue (`zeroValue`, `driver`, `defaultCustomerId`, búsquedas, alta rápida, `paymentModes`, `defaultPaymentMethod`, `idPrefix`). Emite `submit`; expone `submit()` y, nuevo, `total` y `paymentMode` de solo lectura para que el botón de la vista diga el total | D2, D3 |
| D11 | **Métodos de pago**: una constante compartida en `F/features/billing/contracts/billing-recipient.ts` con «Efectivo» (`Cash`) y «Transferencia» (`BankTransfer`), que usan `AppChargeForm` y `ChangePaymentModeDialog` (hoy con sus seis métodos propios, `F/features/billing/components/ChangePaymentModeDialog.vue:96-103`), para que el cobro y el cambio de modo ofrezcan lo mismo. El esquema `paymentMethodSchema` no cambia (el backend acepta los seis; las facturas viejas con otros métodos se siguen mostrando) | D4; usuario (2026-11-27): «En método de pago dejar solo dos opciones: "Efectivo" o "Transferencia"» |
| D12 | **Las tres vistas** (`grep -rln AppChargeForm F`): **Báscula** (`F/features/weighbridge/components/WeighbridgeChargeStep.vue:76-99`): título «Cobro de báscula», sin origen de precio, desglose «Tarifa de báscula» con `weighingPrice`, y el botón «Cobrar {total}» en el pie de la tarjeta (sigue `chargeForm.submit()` con Enter). **Montacargas** (`F/features/warehouse/components/ForkliftChargeDialog.vue:150-219`): título «Cobro del montacargas»; la columna izquierda conserva el valor editable y «Requiere factura», y su desglose propio (`:191-195`) sale porque lo muestra el componente («Valor del servicio», IVA y total); el botón «Finalizar y cobrar {total}» pasa al pie del modal. **Salida** (D13 a D15). La **galería** (`F/pages/dev/components.vue`) muestra el componente con un ejemplo de cada vista | D3, D9, D10 |

### 1.5 Modal de confirmación de la salida (`H/` 3, `MK1/`; fase AQ-3)

| # | Decisión | Fuente |
| --- | --- | --- |
| D13 | **Forma de `ExitConfirmDialog`** (`F/features/exits/components/ExitConfirmDialog.vue`), con los valores de `MK1/`: modal ancho (≈ 1000 px, a una columna en pantallas angostas) con encabezado «Confirmar la salida {N}» y debajo «Al confirmar se emite la guía y se descuenta el stock del depósito.»; dos columnas: a la izquierda, **«Resumen de la salida»** (tarjeta con Tipo, Depósito(s) y Placa(s), y debajo «Mercancía que sale» con cada producto y su cantidad con el embalaje, `totalsByProduct`) y **«Datos de la guía»** (fecha y hora de salida con el calendario, el vencimiento «La guía vence el {fecha} · {n} días después de la salida» y «¿Quién firma la guía de salida?», D1); a la derecha, el **cobro** (`AppChargeForm` con título «Cobro de la guía», origen «Precio general» o «Convenio» de C-F06-06 y el desglose de D2, `baseLabel` igual al origen). Pie: a la izquierda el aviso «Se descontarán {cantidades} del depósito {N}.» (con varios depósitos o productos, «Se descontarán {n} productos de {m} depósitos.»); a la derecha «Cancelar» y «Emitir guía y cobrar {total}». Sale el campo de observaciones (D5) y la fila «Firmante» de solo lectura | `MK1/`; `H/` 2 y 3 |
| D14 | **Texto del pie** (`DEC-002` sobre `MK1/`): el mockup dice «No se puede deshacer.», pero una salida Confirmada sí se corrige: anular la guía devuelve el stock (`P06/` D15). El aviso queda «Se descontarán … Para corregirla después, anule la guía.» | `P06/` D15 |
| D15 | **Inspección** (sin guía ni cobro, `P06/` D13): el mismo modal a una columna con el resumen y la fecha y hora de salida, sin firmante, sin cobro y sin observaciones; botón «Confirmar salida». Los errores de la confirmación (cliente sin asignar, salidas bloqueadas, stock que cambió, mora, firmante no válido) siguen dentro del modal, arriba de las columnas | `P06/` D13 |

---

## 2. Contrato

Cambios sobre `P06/` §2.2 (C-F06-05 y C-F06-06). El resto no cambia.

**C-F06-05 · `POST exits/{id}/confirm`.** Cuerpo:

```json
{ "departureDatetime": "2026-11-27T18:03:00-05:00", "signerType": "Importer", "billing": { "recipientMode": "registered", "customerId": "…", "paymentMethod": "Cash", "paymentMode": "Immediate", "totalAmount": 25000, "referenceNumber": null } }
```

- Sale `observations` (D5): la guía guarda las de la salida.
- Entra `signerType`: `"Importer"` | `"Driver"`; obligatorio si la salida emite guía; ignorado en inspección.
- Errores nuevos (400): «Elija quién firma la guía.»; «Con depósitos de varios clientes o importadores firma el conductor.»; «Los depósitos de la salida no tienen importador registrado: elija al conductor como firmante.». Los demás, como hoy.
- Respuesta: `ExitDto` como hoy; `guide.signerType`, `guide.signerName` y `guide.observations` reflejan D5 y D7.

**C-F06-06 · `GET exits/{id}/guide/charge`.** Respuesta, más el objeto `signer`:

```json
{ "customerId": "…", "customerName": "Cliente Ejemplo 1", "priceSource": "General", "unitPrice": 25000, "taxRate": 0, "taxAmount": 0, "totalAmount": 25000,
  "signer": { "suggested": "Importer", "importerName": "Importadora Ejemplo 1", "importerAvailable": true, "importerUnavailableReason": null } }
```

**Esquemas Zod** (`F/features/exits/contracts/`): `exitConfirmSchema` pierde `observations` y suma `signerType: guideSignerTypeSchema.nullable()` (nulo solo en inspección); `exitGuideChargeSchema` suma `signer` (`suggested`, `importerName` nullable, `importerAvailable`, `importerUnavailableReason` nullable).

---

## 3. Archivos que se tocan

| Fase | Archivo | Cambio |
| --- | --- | --- |
| AQ-1 | `B/Wms.Application/Exits/Commands/ConfirmExitCommand.cs` | `SignerType` en el pedido, sin `Observations`; validación (D7) |
| AQ-1 | `B/Wms.Application/Exits/Common/ExitGuideIssuer.cs` | Firmante pedido y validado (D7); observaciones de la salida (D5) |
| AQ-1 | `B/Wms.Application/ForeignTrade/Common/Services/` (clase pura nueva junto a `DispatchGuideSignerRules`) | Firmante sugerido, disponibilidad y motivo (D1, D7, D8) |
| AQ-1 | `B/Wms.Application/Exits/Queries/GetExitGuideChargeQuery.cs` | `signer` en `ExitGuideChargeDto` (D8) |
| AQ-1 | `B/Wms.Tests/…`, `B/Wms.IntegrationTests/Exits/…` | Pruebas de §5 |
| AQ-2 | `F/components/app/AppChargeForm.vue` | Rediseño (D9, D10) |
| AQ-2 | `F/features/billing/contracts/billing-recipient.ts`, `F/features/billing/components/ChangePaymentModeDialog.vue` | Métodos compartidos (D11) |
| AQ-2 | `F/features/weighbridge/components/WeighbridgeChargeStep.vue`, `F/features/weighbridge/utils/charge-step.ts`, `F/features/warehouse/components/ForkliftChargeDialog.vue`, `F/pages/dev/components.vue` | Vistas del cobro (D12) |
| AQ-2 | `FT/unit/components/AppChargeForm.spec.ts` y las pruebas de Báscula, montacargas y galería que montan el cobro | Ajustadas a D9 a D12 |
| AQ-3 | `F/features/exits/components/ExitConfirmDialog.vue`, `F/features/exits/contracts/exit.ts`, `F/features/exits/contracts/exit-charge.ts`, `F/features/exits/utils/exit-form.ts` | Modal (D13 a D15), contrato (§2), firmante sugerido |
| AQ-3 | `F/features/exits/components/ExitForm.vue` | Texto del paso 8 (D6) |
| AQ-3 | `FT/components/exits/ExitConfirmDialog.spec.ts`, `FT/fixtures/exits/` | Ajustadas |

---

## 4. Fases

| Fase | Repo | Contenido | Criterio de salida | Estado |
| --- | --- | --- | --- | --- |
| AQ-1 | BE | Firmante elegido y validado, firmante sugerido en el cobro, observaciones de la salida en la guía (D5, D7, D8; §2) | QA2-F06AQ-001 a 005 en PASA por API | Pendiente |
| AQ-2 | FE | `AppChargeForm` rediseñado y sus tres vistas y la galería (D2 a D4, D9 a D12) | QA2-F06AQ-006 a 009 en PASA en el navegador contra el API local; captura de cada vista | Hecha el 2026-11-27 (FE `d1ddf53` en `f2/f06-ajustes-qa`): QA2-F06AQ-006 a 009 en PASA en el navegador contra el API local (Báscula cobrada con Enter, con el botón, en $0 y por transferencia sin referencia; montacargas sin finalizar, para no gastar el uso en curso de la QA de F04); `yarn test` 905 → 909, lint 118 → 118 errores (sin contar `.claude/worktrees/`, una copia ajena que `yarn lint` también recorre: 331 → 331), `yarn build` con código 0; capturas `evidencias/aq2-*`. El tipo del desglose está en `F/types/app-charge-form.ts`; el componente ofrece un slot `footer` para el botón de la vista dentro de la tarjeta (Báscula). `ExitConfirmDialog` solo se ajustó a las props nuevas, con «Confirmar y emitir guía {total}» en el slot, hasta AQ-3 |
| AQ-3 | FE | Modal de confirmación rediseñado y texto del formulario (D1, D5, D6, D13 a D15); casos en el navegador; fusión en `fase-2` | QA2-F06AQ-010 a 014 en PASA; fusión de los dos repos con push | Pendiente |

AQ-2 no depende del backend (el cobro de Báscula y del montacargas no cambia de contrato). AQ-3 necesita AQ-1 en `f2/f06-ajustes-qa` del backend para la QA.

---

## 5. Pruebas y casos QA

**Pruebas.** `Wms.Tests`: la regla pura del firmante (un cliente y un importador, sugerido «Importador»; varios clientes, varios importadores o ninguno, sugerido «Conductor» con su motivo; pedido «Importador» no posible, error; sin pedido, error). `Wms.IntegrationTests`: C-F06-05 con `signerType` en sus casos (incluida la inspección, que lo ignora) y la guía con las observaciones de la salida; C-F06-06 con `signer`; las pruebas de salidas que confirman suman `signerType`. Vitest: `AppChargeForm` (destinatarios, conductor editable, sin referencia ni teléfono, dos métodos, texto de pendiente, desglose con «Total a cobrar» y «Total pendiente», factura en cero, `submit()` sin botón propio), las tres vistas con su botón y su total, y `ExitConfirmDialog` (preselección y bloqueo del firmante, cuerpo sin observaciones y con `signerType`, inspección).

| ID | Hallazgo | Precondición | Pasos | Resultado esperado | Verificación |
| --- | --- | --- | --- | --- | --- |
| QA2-F06AQ-001 | `H/` 2; D7 | Salida por depósito de un cliente con un importador | C-F06-05 con `"Importer"`; otra con `"Driver"`; otra sin `signerType` | Guía firmada por el importador; por el conductor; 400 «Elija quién firma la guía.» | API (AQ-1) |
| QA2-F06AQ-002 | `H/` 2; D1, D7 | Consolidada de dos clientes; depósito sin importador (exportación) | C-F06-05 con `"Importer"` en cada una | 400 con los dos mensajes de §2 | API (AQ-1) |
| QA2-F06AQ-003 | D8 | Las salidas de 001 y 002 | C-F06-06 | `signer.suggested` `Importer` con su nombre en la primera; `Driver` con `importerAvailable: false` y su motivo en las otras | API (AQ-1) |
| QA2-F06AQ-004 | `H/` 1; D5 | Salida con observaciones «Carga frágil» | C-F06-05 (con `observations` de un cliente viejo); reabrir, editar las observaciones y reconfirmar | La guía guarda «Carga frágil» e ignora el campo viejo; la guía nueva, las editadas | API (AQ-1) |
| QA2-F06AQ-005 | D15 | Salida de inspección | C-F06-05 sin `signerType` ni `billing` | 200, sin guía | API (AQ-1) |
| QA2-F06AQ-006 | `H/` 3; D9 a D11 | Cualquier vista con cobro | Recorrer los cuatro destinatarios, los dos modos y los métodos | La forma de `MK2/`; conductor editable; sin referencia ni teléfono; dos métodos; texto de pendiente; «Total a cobrar» / «Total pendiente» | Pantalla (AQ-2) |
| QA2-F06AQ-007 | D12 | Camión en Báscula por cobrar; otro con convenio en $0 | Cobrar con Enter y con el botón | «Cobro de báscula» con el desglose; «Cobrar {total}» en el pie; el de $0 solo pide el destinatario | Pantalla (AQ-2) |
| QA2-F06AQ-008 | D12 | Uso de montacargas en curso | «Finalizar»: cambiar el valor y «Requiere factura» | El desglose del componente sigue al valor y al IVA; «Finalizar y cobrar {total}» en el pie | Pantalla (AQ-2) |
| QA2-F06AQ-009 | D11 | Salida con guía | «Cambiar modo de pago» a «Pago inmediato» | Ofrece los mismos dos métodos («Efectivo» y «Transferencia») | Pantalla (AQ-2) |
| QA2-F06AQ-010 | `H/` 3; D13, D14 | Borrador por tiquete de un depósito con importador | «Confirmar y emitir guía» | La forma de `MK1/`: resumen, datos de la guía con el vencimiento, firmante, cobro con origen y desglose, pie con el aviso y «Emitir guía y cobrar {total}»; sin observaciones | Pantalla (AQ-3) |
| QA2-F06AQ-011 | `H/` 2; D1 | La de 010; una consolidada de dos clientes; una de exportación | Abrir el modal en cada una | «Importador» preseleccionado en la primera; en las otras, «Conductor» y «Importador» deshabilitado con su motivo en el tooltip; la guía emitida con el firmante elegido | Pantalla (AQ-3) |
| QA2-F06AQ-012 | `H/` 1; D5, D6 | Borrador con observaciones | Ver el paso 8; confirmar; descargar la guía | El paso 8 dice «Se imprimen en la guía al confirmarla.»; el PDF trae las observaciones de la salida | Pantalla (AQ-3) |
| QA2-F06AQ-013 | D15 | Borrador de inspección | «Confirmar salida» | Modal a una columna con resumen y fecha; sin firmante, cobro ni observaciones | Pantalla (AQ-3) |
| QA2-F06AQ-014 | `P06/` D13 | Depósito sin cliente o bloqueado | Confirmar | El error dentro del modal; nada cambia | Pantalla (AQ-3) |

Los casos se copian con su resultado a `D/qa/casos-qa2-f06-ajustes-qa-2026-11-27.md` al cerrar AQ-3.

---

## 6. Compuertas de cada fase

- Backend (AQ-1): `dotnet build Wms.sln` sin errores; `Wms.Tests` y `Wms.IntegrationTests` en verde; `has-pending-model-changes` limpio (sin migración).
- Frontend (AQ-2, AQ-3): `yarn build` con código 0; `yarn test` en verde; `yarn lint` con igual o menos errores (base: 118 tras I-06) y ninguno en lo tocado; guardias de `FT/unit/guards/` en verde; capturas de las vistas en `D/planes/sprint-11/f06-salidas/evidencias/aq-*`.
- Cifras antes y después en el reporte de cada fase.

---

## 7. Commits

| Fase | Repo | Mensaje |
| --- | --- | --- |
| AQ-1 | BE | `feat(salidas): firmante de la guía elegido al confirmar y observaciones de la salida en la guía (DEC-080, F06, ajustes de QA)` |
| AQ-2 | FE | `style(cobro): formulario de cobro compartido rediseñado en Báscula, montacargas y salidas (DEC-080, F06, ajustes de QA)` |
| AQ-3 | FE | `style(salidas): modal de confirmación rediseñado con el firmante y sin observaciones (DEC-080, F06, ajustes de QA)` y la fusión `merge: ajustes de la QA de F06 en fase-2 (DEC-080, DEC-081)` |
| Cada fase | docs | `docs(f06): fase AQ-n de los ajustes de la QA de F06 cerrada (sprint 11)` |

---

## 8. Riesgos

| Riesgo | Mitigación |
| --- | --- |
| Quitar la «Referencia» del pago pierde el número de la transferencia en la factura (AF-132) | Decisión del usuario (D4). El backend la acepta nula; las facturas viejas la conservan |
| El rediseño del cobro cambia Báscula y montacargas, ya aprobados | QA2-F06AQ-007 y 008 en el navegador; capturas de cada vista |
| En exportación no hay importador: «Importador» siempre deshabilitado | Es la regla de hoy (D1). Si el exportador debe poder firmar, va en otro ajuste |

---

## 9. Preguntas pendientes

Ninguna: D1 a D4 resueltas por el usuario el 2026-11-27; D5 a D15 se derivan de los hallazgos, los mockups y las decisiones de F06.
