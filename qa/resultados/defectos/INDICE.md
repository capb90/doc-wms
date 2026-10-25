# Índice de defectos QA — WMS Bodegas Asociadas

Generado el 2026-10-03 a partir de las fichas de esta carpeta (build FE `1501cd6` / BE `191d4b1`). La ficha es la fuente de verdad; este índice es solo un inventario.

**Total: 154 fichas** · CRITICAL 16 · MAJOR 53 · MINOR 77 · TRIVIAL 7 · Duplicado 1 (126 de la campaña + 28 de la fase 11)

> Actualizado en F11-S1 (2026-10-05, FE `ae36cb4` / BE `c56cc86`): los 13 CRITICAL pasan a «Verificado»; se agregan DEF-F11-001 (S0) a DEF-F11-005 (S1).
> Actualizado en F11-S2 (2026-10-05, FE `15a5028` / BE `214f5f6`): re-test de los 46 MAJOR (44 Verificados, DEF-F3-008 Reabierto, DEF-F5-003 parcial) y de DEF-F11-001 a DEF-F11-005 (Verificados); se agregan DEF-F11-006 a DEF-F11-009.
> Actualizado en F11-S3 (2026-10-06, FE `d9783af` / BE `44bd80a`): re-test de los 67 MINOR y TRIVIAL (66 Verificados, DEF-F7-007 Reabierto), DEF-F5-003 (parte SMTP) y DEF-F3-008 Verificados, DEF-F11-006 a DEF-F11-009 Verificados; se agregan DEF-F11-010 a DEF-F11-015.
> Actualizado en F11-S4 (2026-10-06, FE `e41decf` / BE `ea14548`): DEF-F7-007 y DEF-F11-010 a DEF-F11-015 pasan a «Verificado»; se agregan DEF-F11-016 (MAJOR) y DEF-F11-017 (CRITICAL), detectados en la regresión dirigida (DIR).
> Actualizado en F11-S5 (2026-10-06, FE `bd729e5` / BE `00d6ac3`): DEF-F11-016 y DEF-F11-017 pasan a «Verificado» (Parte A); se agregan DEF-F11-018 (MAJOR) y DEF-F11-019 (MINOR), detectados en los P1 de Báscula (Parte B).
> Actualizado en el re-test posterior a S5 (2026-10-06, FE `24d742d` / BE `f6f1828`): DEF-F11-018 y DEF-F11-019 pasan a «Verificado». Quedan 145 de 145 fichas verificadas.
> Actualizado en F11-S6 (2026-10-07, staging, FE `508b91b` / BE `b31ddb6`): se agregan DEF-F11-020 (MINOR, respaldos simultáneos) y DEF-F11-021 (MAJOR, enlace de recuperación en staging). Quedan 145 Verificadas y 2 Nuevas.
> Actualizado en el re-test de staging posterior a S6 (2026-10-07, FE `8527144` / BE `84c712f`): DEF-F11-020 y DEF-F11-021 pasan a «Verificado». Quedan 147 de 147 fichas verificadas.
> Actualizado el 2026-10-07 (FE `59d9b08`, sin commit de la corrección): se agrega DEF-F11-022 (MINOR, menú lateral), reportado por el usuario y ya en «Corregido». Quedan 147 Verificadas y 1 Corregida.
> Actualizado el 2026-10-08 en la Fase 3 del selector de conductor (local `wms_migracion`, FE `7d7516a` / BE `3748ec6`): se agregan DEF-F11-023 a DEF-F11-026 (MINOR, selector y modal del conductor). Quedan 147 Verificadas, 1 Corregida y 4 Nuevas.
> Actualizado el 2026-10-08 (FE `7d7516a` con cambios sin commit): DEF-F11-025 se reclasifica a CRITICAL (decisión del usuario) y pasa a «Corregido»; se agrega DEF-F11-027 (MAJOR, filtro por nombre de Administración → Conductores), ya «Corregido». Quedan 147 Verificadas, 3 Corregidas y 3 Nuevas.
> Actualizado el 2026-10-08 en la Fase 4 del selector de conductor (staging, FE `4ca4e0a` / BE `044be08`, sin recrear la base): DEF-F11-022, DEF-F11-025 y DEF-F11-027 pasan a «Verificado»; DEF-F11-023 y DEF-F11-024 vistos en staging, siguen «Nuevo» con DEF-F11-026 (MINOR conocidos, desplegados por decisión del usuario). Sin fichas nuevas. Quedan 150 Verificadas y 3 Nuevas.
> Actualizado el 2026-10-24 en la fase 12 del plan de brechas P1 (local, FE `e2e11e6` / BE `560f558`): se agrega DEF-F11-028 (MAJOR, «Depósitos pendientes» omite el depósito agotado con factura por numerar), estado «Nuevo». Informe: `P1-informe-2026-10-24.md`.
> Actualizado el 2026-10-24, antes de la fase 13 del plan de brechas P1 (local, BE `9e399de`): DEF-F11-028 corregido y verificado en re-test local (F6-ALM-018, F6-REF-005 y F6-REF-006 PASA). Quedan 151 Verificadas y 3 Nuevas (DEF-F11-023, 024 y 026).
> Actualizado en la ronda QA de preproducción (2026-10-25, FE `cb2a4f7` / BE `57c94dd`, base `wms_qa_preprod`): se agregan los defectos desde DEF-F11-029. Informe: `../PRE-informe-2026-10-25.md`.
> Actualizado el 2026-10-25 en el plan de corrección de DEF-F11-030 y DEF-F11-034 (local): DEF-F11-030 corregido (BE `b8c600e` y `6f49710`); DEF-F11-034 corregido en backend (fase 2, sin commit; falta el diálogo de Bodega). Re-test QA en la fase 4 del plan.

| ID | Severidad | Estado | Módulo | Título |
|---|---|---|---|---|
| [DEF-F0-001](DEF-F0-001.md) | MINOR | Verificado | Transversal (Administración, Comercio Exterior, Bodega, Báscula) | 10 componentes usan `LabelBase` sin importarlo |
| [DEF-F0-002](DEF-F0-002.md) | MINOR | Verificado | Bodega | `receptions/create.vue` usa `ReceptionStepManualInfo` sin importarlo |
| [DEF-F0-003](DEF-F0-003.md) | MINOR | Verificado | Transversal | El logo lleva a «Acceso Denegado» y esa pantalla no permite volver |
| [DEF-F1-001](DEF-F1-001.md) | MAJOR | Verificado | Administración | Productos: `GET`, `POST` y `PATCH product` responden 500 (NullReferenceException) |
| [DEF-F1-002](DEF-F1-002.md) | MAJOR | Verificado | Autenticación | El cambio de contraseña no aplica la política de contraseña fuerte en el backend |
| [DEF-F1-003](DEF-F1-003.md) | MAJOR | Verificado | Administración / Facturación | La dimensión «perecedero» (WMS-32) no se puede configurar: el API descarta `appliesToPerishable` |
| [DEF-F1-004](DEF-F1-004.md) | MAJOR | Verificado | Administración / Facturación | El convenio acepta porcentajes fuera de rango (150 %) |
| [DEF-F1-005](DEF-F1-005.md) | MAJOR | Verificado | Administración / Vigilancia | Vehículos: placa duplicada por mayúsculas, sin validación de formato y transportadora sin rol |
| [DEF-F1-006](DEF-F1-006.md) | MINOR | Verificado | Administración | El alta de usuario no valida que las contraseñas coincidan |
| [DEF-F1-007](DEF-F1-007.md) | MINOR | Verificado | Administración | Editar con identificación o SKU duplicados muestra el error crudo de Postgres; el nombre de producto se puede duplicar |
| [DEF-F1-008](DEF-F1-008.md) | MINOR | Verificado | Administración | Quedan textos «Stakeholder» visibles en el alta de terceros |
| [DEF-F1-009](DEF-F1-009.md) | MAJOR | Verificado | Autenticación / Seguridad | Usuario desactivado, con rol retirado o deslogueado conserva acceso con su token hasta que expira |
| [DEF-F1-010](DEF-F1-010.md) | MINOR | Verificado | Administración | Un Admin puede quitarse su rol o desactivarse a sí mismo, y un usuario puede quedar sin roles |
| [DEF-F1-011](DEF-F1-011.md) | MINOR | Verificado | Autenticación / Seguridad | Enumeración de cuentas por los mensajes de login y de recuperación |
| [DEF-F2-001](DEF-F2-001.md) | CRITICAL | Verificado | Vigilancia | La búsqueda de placa por coincidencia parcial registra el ingreso al vehículo equivocado |
| [DEF-F2-002](DEF-F2-002.md) | MINOR | Verificado | Vigilancia | El ingreso crea vehículos con placa de formato inválido |
| [DEF-F2-003](DEF-F2-003.md) | MINOR | Verificado | Vigilancia | El API acepta fecha de ingreso futura y salida anterior al ingreso |
| [DEF-F2-004](DEF-F2-004.md) | MAJOR | Verificado | Transversal (Trazabilidad) | La trazabilidad muestra «En portería» a camiones que ya salieron |
| [DEF-F3-001](DEF-F3-001.md) | CRITICAL | Verificado | Transversal (notificaciones) | Las notificaciones al rol Comercio Exterior no llegan a nadie |
| [DEF-F3-002](DEF-F3-002.md) | MAJOR | Verificado | Báscula / Facturación | Báscula sin idempotencia: dos envíos del registro o del cobro duplican depósitos, stock, ciclos y facturas |
| [DEF-F3-003](DEF-F3-003.md) | MAJOR | Verificado | Báscula | La hora del pesaje se propone con la del ingreso / pesaje anterior: tiquetes con horas falsas |
| [DEF-F3-004](DEF-F3-004.md) | CRITICAL | Verificado | Báscula | Descartar una operación no libera el camión y permite cobrar el servicio descartado |
| [DEF-F3-005](DEF-F3-005.md) | MAJOR | Verificado | Vigilancia / Báscula | La salida en Vigilancia con ciclo abierto deja el ciclo atascado e invisible |
| [DEF-F3-006](DEF-F3-006.md) | MAJOR | Verificado | Báscula | Tras recargar, el Registro guardado se ve vacío; recargar con borradores no avisa |
| [DEF-F3-007](DEF-F3-007.md) | MAJOR | Verificado | Báscula / Facturación | El cobro no preselecciona al cliente de la operación: propone al conductor y el precio base |
| [DEF-F3-008](DEF-F3-008.md) | MAJOR | Verificado | Báscula | Conductor y vehículo exigidos no se guardan en Solo báscula ni en Salida |
| [DEF-F3-009](DEF-F3-009.md) | MINOR | Verificado | Báscula | El API de registro y cobro acepta datos que la interfaz rechaza |
| [DEF-F3-010](DEF-F3-010.md) | MINOR | Verificado | Báscula | Un documento con ingreso de camiones cerrado se ve como «Documento nuevo» |
| [DEF-F3-011](DEF-F3-011.md) | MAJOR | Verificado | Báscula | «Agregar otro depósito» (multidepósito) es inalcanzable |
| [DEF-F3-012](DEF-F3-012.md) | MAJOR | Verificado | Báscula | Se puede iniciar una segunda salida con una orden de cargue que ya tiene salida activa |
| [DEF-F3-013](DEF-F3-013.md) | MAJOR | Verificado | Báscula | Historial: «Cambiar modo de pago» da 404 y el operario de báscula no ve «Editar peso» |
| [DEF-F3-014](DEF-F3-014.md) | MAJOR | Verificado | Báscula | Se acepta una tara mayor que el bruto (neto negativo) sin advertencia |
| [DEF-F3-015](DEF-F3-015.md) | MINOR | Verificado | Báscula | Historial y dashboard: pesos de operaciones de un pesaje no se muestran y los conteos no cuadran |
| [DEF-F3-016](DEF-F3-016.md) | MAJOR | Verificado | Báscula / Comercio Exterior | La búsqueda de vehículo por placa en báscula devuelve el duplicado inactivo (`qaa101`) |
| [DEF-F3-017](DEF-F3-017.md) | MAJOR | Verificado | Báscula | Solo báscula retomada tras recargar se cobra como depósito y el ciclo queda sin factura |
| [DEF-F3-018](DEF-F3-018.md) | MINOR | Verificado | Báscula | El registro guardado se muestra en campos editables sin forma de guardar los cambios |
| [DEF-F3-019](DEF-F3-019.md) | MINOR | Verificado | Báscula / Facturación | El API de cobro conserva efectivo recibido y cambio, que el negocio decidió eliminar |
| [DEF-F4-001](DEF-F4-001.md) | CRITICAL | Verificado | Bodega | La recepción de depósitos con unidades de carga es imposible |
| [DEF-F4-002](DEF-F4-002.md) | CRITICAL | Verificado | Bodega | La recepción directa sin báscula falla siempre desde la interfaz (500) |
| [DEF-F4-003](DEF-F4-003.md) | MAJOR | Verificado | Bodega / Báscula | Báscula permite el segundo pesaje sin la llegada registrada en Bodega; esas entradas quedan sin recepción |
| [DEF-F4-004](DEF-F4-004.md) | MAJOR | Verificado | Bodega / Comercio Exterior | Se ejecuta un cargue sobre un depósito devuelto a Borrador |
| [DEF-F4-005](DEF-F4-005.md) | MAJOR | Verificado | Bodega / Vigilancia | La recepción directa crea ingresos abiertos duplicados para el mismo vehículo |
| [DEF-F4-006](DEF-F4-006.md) | MAJOR | Verificado | Comercio Exterior | El detalle de un depósito de exportación cerrado da 404 y desaparece de la lista |
| [DEF-F4-007](DEF-F4-007.md) | MINOR | Verificado | Bodega | Historial de recepciones: filtrar un solo día no devuelve nada y el API da 500 con fecha local |
| [DEF-F4-008](DEF-F4-008.md) | MINOR | Verificado | Bodega | Exportar movimientos a Excel solo incluye la primera página |
| [DEF-F4-009](DEF-F4-009.md) | MINOR | Verificado | Bodega | La recepción acepta más de 5 fotos y archivos que no son imagen |
| [DEF-F4-010](DEF-F4-010.md) | MINOR | Verificado | Bodega | Un producto declarado y no contado no genera aviso y el historial dice «Sin diferencia» |
| [DEF-F4-011](DEF-F4-011.md) | MINOR | Verificado | Bodega | Las novedades no validan que las cantidades cuadren con el total |
| [DEF-F4-012](DEF-F4-012.md) | MINOR | Verificado | Bodega / Seguridad | El API ejecuta cargues sin firma y toma el responsable del cliente |
| [DEF-F4-013](DEF-F4-013.md) | MINOR | Verificado | Bodega | Montacargas: el API acepta horómetro inicial 0 y final igual al inicial |
| [DEF-F4-014](DEF-F4-014.md) | MINOR | Verificado | Bodega | Reejecutar una orden ya cargada da un mensaje erróneo (404 de reserva) |
| [DEF-F4-015](DEF-F4-015.md) | MINOR | Verificado | Bodega | Las tarjetas de pendientes de Bodega muestran «kg (Invalid Date)» |
| [DEF-F4-016](DEF-F4-016.md) | MINOR | Verificado | Bodega | El historial de montacargas no muestra horómetros, valor, modo de pago ni factura |
| [DEF-F4-017](DEF-F4-017.md) | TRIVIAL | Verificado | Bodega | Montacargas: mensajes técnicos al iniciar sin servicio |
| [DEF-F4-018](DEF-F4-018.md) | MINOR | Verificado | Bodega | El inventario de Bodega no muestra depósitos en Borrador con mercancía recibida |
| [DEF-F5-001](DEF-F5-001.md) | MAJOR | Verificado | Comercio Exterior | En Borrador no se pueden editar fecha del documento, moneda ni valor: la tarjeta «Información General» queda en blanco |
| [DEF-F5-002](DEF-F5-002.md) | MAJOR | Verificado | Comercio Exterior / Bodega | El ajuste CE-7 y la corrección de productos cambian el stock sin registrar movimiento de inventario |
| [DEF-F5-003](DEF-F5-003.md) | MAJOR | Verificado | Comercio Exterior | El ajuste CE-7 envía el correo antes de validar; si el SMTP falla, responde 500 |
| [DEF-F5-004](DEF-F5-004.md) | MAJOR | Verificado | Comercio Exterior | El ajuste CE-7 permite dejar el recibido por debajo de lo ya levantado (pendiente por nacionalizar negativo) |
| [DEF-F5-005](DEF-F5-005.md) | MAJOR | Verificado | Comercio Exterior | Se aceptan levantes en depósitos anulados, que se ven «Nacionalizado», imprimen etiqueta y muestran «Registrar levante» en Borrador |
| [DEF-F5-006](DEF-F5-006.md) | MINOR | Verificado | Comercio Exterior | El tablero de CE cuenta anulados y «Guías pendientes» abre el historial |
| [DEF-F5-007](DEF-F5-007.md) | MINOR | Verificado | Comercio Exterior | Kanban paginado en conjunto y cantidades que suman unidades distintas |
| [DEF-F5-008](DEF-F5-008.md) | MINOR | Verificado | Comercio Exterior | «Validar depósito» compara solo el peso del último ciclo |
| [DEF-F5-009](DEF-F5-009.md) | MINOR | Verificado | Comercio Exterior | Filtros de órdenes de cargue por documento comercial, importador y manifiesto DIAN no devuelven nada |
| [DEF-F5-010](DEF-F5-010.md) | MINOR | Verificado | Comercio Exterior / Facturación | Datos de terceros y producto incorrectos en guía, factura y etiqueta |
| [DEF-F5-011](DEF-F5-011.md) | MINOR | Verificado | Comercio Exterior | El cobro de la guía no muestra el total y el formulario tiene textos obsoletos |
| [DEF-F5-012](DEF-F5-012.md) | MINOR | Verificado | Comercio Exterior / Bodega | El «Responsable» de la recepción en el detalle de CE es el usuario de Vigilancia |
| [DEF-F5-013](DEF-F5-013.md) | TRIVIAL | Verificado | Comercio Exterior | Mensajes con el estado en inglés y textos equivocados por modalidad |
| [DEF-F5-014](DEF-F5-014.md) | MAJOR | Verificado | Báscula / Bodega / Comercio Exterior | Mercancía de importación despachada sin guía de salida |
| [DEF-F6-001](DEF-F6-001.md) | CRITICAL | Verificado | Facturación | La tarifa de almacenamiento se toma de otra modalidad: el convenio IMP cobra EXP e INSP y la tarifa base EXP cobra INSP |
| [DEF-F6-002](DEF-F6-002.md) | CRITICAL | Verificado | Facturación | El cierre manual de períodos abre el nuevo con la misma fecha de inicio: doble cobro del mismo período |
| [DEF-F6-003](DEF-F6-003.md) | CRITICAL | Verificado | Facturación | El override de una línea con cantidad > 1 multiplica el monto por la cantidad y suma IVA |
| [DEF-F6-004](DEF-F6-004.md) | CRITICAL | Verificado | Facturación | El override muestra el total con IVA como «Monto original» pero aplica el valor digitado como neto + IVA |
| [DEF-F6-005](DEF-F6-005.md) | CRITICAL | Verificado | Facturación | Los cargos «por facturar» vencen el mismo instante en que se crean y quedan atascados en Overdue |
| [DEF-F6-006](DEF-F6-006.md) | CRITICAL | Verificado | Facturación | Mora: las facturas con pago parcial nunca quedan vencidas y el bloqueo tarda 3 corridas diarias |
| [DEF-F6-007](DEF-F6-007.md) | MAJOR | Verificado | Facturación | El piso por unidad de carga provoca una falsa «magnitud facturada dos veces» y cae al mínimo de la modalidad |
| [DEF-F6-008](DEF-F6-008.md) | MINOR | Verificado | Facturación | El ciclo OnDemand se ofrece pero no factura el almacenamiento (retirarlo de las opciones) |
| [DEF-F6-009](DEF-F6-009.md) | MAJOR | Verificado | Facturación | Se registran pagos en borradores y el buscador de pagos lista facturas no pagables con «null» |
| [DEF-F6-010](DEF-F6-010.md) | MAJOR | Verificado | Facturación | El comprobante del pago no se puede guardar (varchar(500)) |
| [DEF-F6-011](DEF-F6-011.md) | MAJOR | Verificado | Facturación | La creación manual de facturas sigue expuesta (pantalla y API) |
| [DEF-F6-012](DEF-F6-012.md) | MAJOR | Verificado | Facturación / Admin | Las reglas para perecederos (WMS-32) no se pueden configurar |
| [DEF-F6-013](DEF-F6-013.md) | MAJOR | Verificado | Facturación | Se puede anular una factura con pagos; el dinero queda en la anulada |
| [DEF-F6-014](DEF-F6-014.md) | MINOR | Verificado | Facturación | No se puede quitar el límite de crédito |
| [DEF-F6-015](DEF-F6-015.md) | MINOR | Verificado | Admin | El PATCH de un servicio de convenio borra los campos omitidos (producto y modalidad) |
| [DEF-F6-016](DEF-F6-016.md) | MINOR | Verificado | Facturación | Las previsualizaciones de fórmula no coinciden con el cobro real |
| [DEF-F6-017](DEF-F6-017.md) | MINOR | Verificado | Facturación | No existe la consolidación diaria de cargos por facturar |
| [DEF-F6-018](DEF-F6-018.md) | MINOR | Verificado | Facturación | Jobs: el aviso de vencimiento se duplica en cada corrida y la renovación manual no avisa |
| [DEF-F6-019](DEF-F6-019.md) | MINOR | Verificado | Facturación | Un método de pago inválido produce 500 NullReference |
| [DEF-F6-020](DEF-F6-020.md) | TRIVIAL | Verificado | Facturación | Mensajes de facturación técnicos o confusos |
| [DEF-F6-021](DEF-F6-021.md) | MAJOR | Verificado | Facturación | El tratamiento del IVA en los mínimos de almacenamiento no es configurable |
| [DEF-F6-022](DEF-F6-022.md) | MAJOR | Verificado | Facturación | No se puede asignar N.º SIIGO a facturas de contado ya pagadas |
| [DEF-F7-001](DEF-F7-001.md) | CRITICAL | Verificado | Seguridad / Admin | La auditoría guarda el PasswordHash y el SecurityStamp de los usuarios |
| [DEF-F7-002](DEF-F7-002.md) | MAJOR | Verificado | Trazabilidad | Trazabilidad: los camiones que salen siguen «En portería» y hay etapas «Desconocido» |
| [DEF-F7-003](DEF-F7-003.md) | MINOR | Verificado | Reportes | El reporte de salidas diarias omite despachos sin guía |
| [DEF-F7-004](DEF-F7-004.md) | MINOR | Verificado | Reportes | Ingresos diarios: peso neto en 0 y placa/tiquete vacíos |
| [DEF-F7-005](DEF-F7-005.md) | MINOR | Verificado | Reportes / Permisos | Inventario general como Comercio Exterior muestra «Error 403 Error interno del servidor» |
| [DEF-F7-006](DEF-F7-006.md) | MINOR | Verificado | Reportes | Las exportaciones a Excel escriben las fechas en UTC |
| [DEF-F7-007](DEF-F7-007.md) | MINOR | Verificado | Reportes / Facturación | Facturación por CPI pierde la factura anulada tras refacturar |
| [DEF-F7-008](DEF-F7-008.md) | MINOR | Verificado | Auditoría | Catálogos sin auditoría |
| [DEF-F7-009](DEF-F7-009.md) | MINOR | Verificado | Reportes | Kárdex: la pantalla y el Excel no muestran las líneas de movimiento |
| [DEF-F7-010](DEF-F7-010.md) | MINOR | Verificado | Trazabilidad | Trazabilidad: «Hoy» en UTC, placa sensible a mayúsculas y aviso con título técnico |
| [DEF-F7-011](DEF-F7-011.md) | MINOR | Verificado | Documentos | Documentos impresos: detalle del depósito ausente, teléfono 0 y datos de empresa inconsistentes |
| [DEF-F7-012](DEF-F7-012.md) | MINOR | Verificado | Permisos | El API de estadísticas entrega el bloque de facturación a Comercio Exterior |
| [DEF-F8-001](DEF-F8-001.md) | MAJOR | Verificado (unificada en DEF-F3-002) | Báscula / Facturación | [UNIFICADO EN DEF-F3-002] Báscula sin idempotencia: dos envíos simultáneos del registro o del cobro duplican depósitos, stock, ciclos y facturas |
| [DEF-F8-002](DEF-F8-002.md) | MAJOR | Verificado | Comercio Exterior / Facturación | La guía de una orden multi-cliente se factura entera al primer cliente |
| [DEF-F8-003](DEF-F8-003.md) | MAJOR | Verificado | Comercio Exterior / Bodega | Tras la salida con el tiquete de ingreso, la OC queda Dispatched al cargar y ya no se puede emitir la guía |
| [DEF-F8-004](DEF-F8-004.md) | MAJOR | Verificado | Comercio Exterior / Documentos | Al reimprimir una guía de salida aparece el levante de otra salida |
| [DEF-F8-005](DEF-F8-005.md) | MAJOR | Verificado | Bodega / Comercio Exterior / Facturación | La recepción sin báscula crea el depósito de inspección ya Confirmado, sin revisión de Comercio Exterior y con factura en $0 |
| [DEF-F8-006](DEF-F8-006.md) | MINOR | Verificado | Facturación | El detalle de la factura de almacenamiento usa la cantidad declarada y no la ajustada |
| [DEF-F8-007](DEF-F8-007.md) | MINOR | Verificado | Comercio Exterior / Notificaciones | Anular un depósito no avisa a Bodega ni a Facturación |
| [DEF-F8-008](DEF-F8-008.md) | MINOR | Verificado | Comercio Exterior / Báscula | La OC sigue Pending durante la salida por báscula (no pasa a «en cargue») |
| [DEF-F8-009](DEF-F8-009.md) | MINOR | Verificado | Báscula / Reportes | Reporte diario de báscula: una inspección de pesaje único se rotula «Solo Pesaje» |
| [DEF-F9-001](DEF-F9-001.md) | CRITICAL | Verificado | Seguridad / Administración | Cualquier usuario autenticado puede crear y editar terceros, convenios y tarifas, motivos de ingreso, conductores, vehículos y productos |
| [DEF-F9-002](DEF-F9-002.md) | MAJOR | Verificado | Seguridad / Vigilancia / Bodega | Vigilancia y Bodega se cruzan: Vigilancia entra a las páginas y al API de Bodega, y Bodega registra ingresos y salidas de Vigilancia |
| [DEF-F9-003](DEF-F9-003.md) | MAJOR | Verificado | Seguridad / Auditoría operativa | El API guarda como autor el usuario que envía el cliente (autorizó la salida, autorizó la recepción, completó el cargue) y la firma del cargue es opcional |
| [DEF-F9-004](DEF-F9-004.md) | MINOR | Verificado | Reportes / Permisos | Facturación no puede abrir el reporte de inventario general en la interfaz |
| [DEF-F9-005](DEF-F9-005.md) | MINOR | Verificado | Seguridad / Permisos | Datos sensibles legibles por roles operativos: tarifas de convenios, simulación de facturas, inventario general y kárdex |
| [DEF-F9-006](DEF-F9-006.md) | MINOR | Verificado | API / Errores | Un cuerpo JSON mal formado devuelve 500 con el texto interno de la excepción |
| [DEF-F10-001](DEF-F10-001.md) | MAJOR | Verificado | Frontend (Bodega, Facturación, CE) | Acciones sin protección contra doble envío (recepción sin báscula, verificar/rechazar pago, crear OC, emitir guía, registrar pago con comprobante, N.º con Enter) y «Rechazar pago» sin confirmación |
| [DEF-F10-002](DEF-F10-002.md) | MINOR | Verificado | Facturación | El formulario de pago borra el monto y la referencia cuando el backend rechaza el pago |
| [DEF-F10-003](DEF-F10-003.md) | MINOR | Verificado | Frontend / Errores | Los errores de negocio se muestran duplicados (aviso global + aviso del componente + texto en línea) |
| [DEF-F10-004](DEF-F10-004.md) | MINOR | Verificado | Frontend / Errores | Con el API caído se apilan avisos «Error 500 / Error de conexión con el servidor» que tapan la pantalla |
| [DEF-F10-005](DEF-F10-005.md) | MINOR | Verificado | Frontend / Navegación | Callejones sin salida: factura inexistente con spinner infinito, ID mal formado como «Error interno», 404 de ruta en inglés |
| [DEF-F10-006](DEF-F10-006.md) | MINOR | Verificado | Frontend / Formatos | Formatos inconsistentes: báscula usa separador de miles estadounidense y hay cuatro formatos de fecha |
| [DEF-F10-007](DEF-F10-007.md) | MINOR | Verificado | Frontend / Backend (textos) | Textos en inglés, técnicos o con errores: «Stakeholder», «role», validación de archivo de PrimeVue, estados en inglés en mensajes del backend |
| [DEF-F10-008](DEF-F10-008.md) | MINOR | Verificado | Frontend / Accesibilidad | Accesibilidad: botones de solo ícono sin tooltip ni etiqueta, campos sin label asociado y el foco no va al primer error |
| [DEF-F11-001](DEF-F11-001.md) | MINOR | Verificado | Autenticación / Seguridad | El token del login hecho justo después de cambiar la contraseña recibe 401 durante 15 s |
| [DEF-F11-002](DEF-F11-002.md) | MINOR | Verificado | Administración / API | El alta de tercero por API responde 500 con un tipo de identificación fuera de la lista |
| [DEF-F11-003](DEF-F11-003.md) | MAJOR | Verificado | Facturación | La factura de almacenamiento en $0 (valor mínimo) exige N.º SIIGO para aprobarse |
| [DEF-F11-004](DEF-F11-004.md) | MAJOR | Verificado | Báscula | El historial de báscula y el detalle del ciclo no cargan («Ocurrió un error inesperado») |
| [DEF-F11-005](DEF-F11-005.md) | MINOR | Verificado | Bodega | Guardar la firma en Bodega lanza «No PrimeVue Toast provided!» y no muestra el aviso |
| [DEF-F11-006](DEF-F11-006.md) | TRIVIAL | Verificado | Facturación | El detalle de una factura en cero se titula «Factura pendiente de número» |
| [DEF-F11-007](DEF-F11-007.md) | MINOR | Verificado | Báscula | El historial de báscula muestra «Modificado por N/A el N/A · Razón: N/A» tras corregir un peso |
| [DEF-F11-008](DEF-F11-008.md) | CRITICAL | Verificado | Báscula / Documentos | Báscula reescribe el conductor existente del ingreso con los datos de otra persona |
| [DEF-F11-009](DEF-F11-009.md) | MAJOR | Verificado | Báscula | El depósito adicional guardado sin cliente no se puede confirmar en báscula |
| [DEF-F11-010](DEF-F11-010.md) | TRIVIAL | Verificado | Báscula | Tras confirmar un depósito adicional, la ficha de báscula muestra el documento del depósito principal |
| [DEF-F11-011](DEF-F11-011.md) | MINOR | Verificado | Báscula | El filtro por tiquete del historial de báscula no encuentra operaciones de Solo báscula ni de Salida |
| [DEF-F11-012](DEF-F11-012.md) | MINOR | Verificado | Comercio Exterior | Comercio Exterior puede editar el manifiesto DIAN de un depósito anulado |
| [DEF-F11-013](DEF-F11-013.md) | MINOR | Verificado | Comercio Exterior | El detalle de exportación e inspección no muestra la moneda ni el valor de la mercancía |
| [DEF-F11-014](DEF-F11-014.md) | TRIVIAL | Verificado | Comercio Exterior | Corregir productos en Comercio Exterior avisa «camión sin placa» y «El stock no cambió» |
| [DEF-F11-015](DEF-F11-015.md) | TRIVIAL | Verificado | Facturación | Por API, un comprobante de pago de más de 5,3 MB responde «Adjunte el comprobante del pago.» |
| [DEF-F11-016](DEF-F11-016.md) | MAJOR | Verificado | Vigilancia / Báscula | Corregir el motivo de un ingreso con conductor lo deja «Completed» y fuera de la cola de báscula |
| [DEF-F11-017](DEF-F11-017.md) | CRITICAL | Verificado | Facturación (almacenamiento) / Comercio Exterior | El recálculo del período de almacenamiento cobra el stock actual y deja de cobrar lo ya despachado |
| [DEF-F11-018](DEF-F11-018.md) | MAJOR | Verificado | Báscula / Reportes | El reporte diario de báscula omite el cobro del depósito principal de un camión multidepósito e imprime la hora en UTC |
| [DEF-F11-019](DEF-F11-019.md) | MINOR | Verificado | Báscula | El detalle del ciclo de báscula muestra «Abierto» como estado de todo depósito y su filtro por estado no funciona |
| [DEF-F11-020](DEF-F11-020.md) | MINOR | Verificado | Administración | Dos respaldos simultáneos corren a la vez y los del mismo minuto escriben el mismo archivo |
| [DEF-F11-021](DEF-F11-021.md) | MAJOR | Verificado | Transversal | En staging, el enlace del correo de recuperación de contraseña lleva al login y pierde el token |
| [DEF-F11-022](DEF-F11-022.md) | MINOR | Verificado | Transversal | El menú lateral salta y resalta la misma opción de otro grupo, y las entradas con filtro no se resaltan |
| [DEF-F11-023](DEF-F11-023.md) | MINOR | Nuevo | Báscula / Bodega | Esc no cierra el modal del conductor cuando el foco está en «Tipo de Documento» |
| [DEF-F11-024](DEF-F11-024.md) | MINOR | Nuevo | Báscula / Bodega | En el modal del conductor, al salir del documento se pierde el foco y lo que se teclea después |
| [DEF-F11-025](DEF-F11-025.md) | CRITICAL | Verificado | Báscula / Bodega | «Usar este conductor» guarda en el conductor el país del vehículo sin que el operario lo cambie |
| [DEF-F11-026](DEF-F11-026.md) | MINOR | Nuevo | Báscula / Bodega | Enter antes de que llegue la búsqueda cierra el selector sin elegir y borra lo escrito |
| [DEF-F11-027](DEF-F11-027.md) | MAJOR | Verificado | Administración | El filtro por nombre de Administración → Conductores no filtra |
| [DEF-F11-028](DEF-F11-028.md) | MAJOR | Verificado | Facturación | «Depósitos pendientes» omite el depósito cerrado por agotamiento aunque tenga factura por numerar |
| [DEF-F11-029](DEF-F11-029.md) | MINOR | Nuevo | Báscula / Transversal | Cada pesaje muestra a Admin y CE un aviso técnico «WeighingCaptured» con el GUID del ciclo |
| [DEF-F11-030](DEF-F11-030.md) | CRITICAL | Corregido | Comercio Exterior / Facturación | Reconfirmar tras corregir valor, moneda o fecha deja la factura Borrador con el importe anterior |
| [DEF-F11-031](DEF-F11-031.md) | TRIVIAL | Nuevo | Comercio Exterior | La etiqueta con levante muestra «Ampara» con cuatro decimales |
| [DEF-F11-032](DEF-F11-032.md) | MINOR | Nuevo | Transversal | Los correos de aviso a Admin cortan el asunto en el primer punto y fechan en UTC |
| [DEF-F11-033](DEF-F11-033.md) | MINOR | Nuevo | Administración / API | Crear una ubicación sin código responde 500 en lugar de 400 |
| [DEF-F11-034](DEF-F11-034.md) | MAJOR | Corregido (backend) | Vigilancia / Bodega | Vigilancia deja salir sin guía un camión cuya orden de importación se cargó sin báscula de salida |
