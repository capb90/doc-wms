# Inventario de cambios — Guiones de video tutoriales v1.0 → v2.0

> **Fecha:** 7 de octubre de 2026.
> **Código revisado:** Frontend `wms` en `develop` (`429be4d`) y Backend `wms-api` en `develop` (`7be5700`). Solo lectura.
> **Regla:** el código manda. Donde un documento dice otra cosa, el guion describe el código y la diferencia queda anotada en §5.
> **Abreviaturas:** `FE:` = `Frontend/wms/`; `BE:` = `Backend/wms-api/`. CHG-n = tarjeta de `FE:docs/qa/plan-correccion-defectos.md`; DEF-n = ficha de `FE:docs/qa/resultados/defectos/`; §10 = `FE:docs/qa/00-plan-maestro.md` §10; WMS-n = historia de la Ola correspondiente.

## 1. Resumen

| Estado | Guiones v1 | Qué significa |
|---|---:|---|
| Vigente | 0 | Ningún guion v1 se puede grabar tal cual. |
| Actualizar | 32 | La función existe, pero cambiaron nombres, pasos o reglas. |
| Reemplazar | 17 | La función se rehízo; el guion se escribe de nuevo (incluye dos fusiones y una absorción). |
| Retirar | 0 | No se retira ningún guion completo; sí pasos y funciones (§4). |
| **Total v1** | **49** | |
| Nuevo (v2) | 33 | Funciones sin guion en la v1. |
| **Total v2** | **81** | 49 − 1 (fusión de 3.4 y 3.5) + 33 nuevos. |

**Series de la v2:** 0 Introducción (5), 1 Administración (13), 2 Acuerdos (10), 3 Facturación (13), 4 Vigilancia (4), 5 Báscula (12), 6 Bodega (9), 7 Comercio Exterior (15).

## 2. Guion por guion (v1)

### Serie 0 · Introducción

| v1 | Título v1 | Rol | Estado | Qué cambió | Fuente | v2 |
|---|---|---|---|---|---|---|
| 0.1 | Visión general del sistema | Todos | Actualizar | Los seis roles reales («Administrador», «Facturación», «Comercio exterior», «Operario vigilancia», «Operario báscula», «Operario bodega»). Cada rol entra a su propia página de inicio y solo ve su módulo. El WMS no emite la factura electrónica: el N.º viene de SIIGO. Sin «Estadísticas». | CHG-87 (`FE:app/utils/role-routes.ts`), CHG-03, `AppMenu.vue:30` | 0.1 |
| 0.2 | Acceso y primeros pasos | Todos | Reemplazar | Se divide en tres. El botón es «Recuperar contraseña», no «¿Olvidó su contraseña?», y el correo solo le llega al Administrador. «Cambiar Contraseña» tiene política de 8+ caracteres con mayúscula, minúscula, número y carácter especial. Vigilancia no recibe avisos en la campana. Se agregan «Mi cuenta» y «Cerrar sesión». | CHG-51, CHG-16, `FE:app/pages/auth/*.vue`, `NotificationPanel.vue`, `AppRightMenu.vue` | 0.2, 0.3, 0.4 |

### Serie 1 · Administración

| v1 | Título v1 | Rol | Estado | Qué cambió | Fuente | v2 |
|---|---|---|---|---|---|---|
| 1.1 | Cómo crear usuarios y asignar roles | Admin | Actualizar | El botón es «Crear Usuario». Al guardar se abre el **detalle**, con el toast «Usuario creado.». «Repetir Contraseña» debe coincidir y se exige al menos un rol. La contraseña es temporal. El correo solo sirve de recuperación al Admin. La gestión de la cuenta sale a un video propio. | CHG-50, CHG-51, `UserForm.vue`, `useUserCreate.ts` | 1.1 |
| 1.2 | Cómo registrar un tercero (cliente) | Admin | Actualizar | La ruta es «Administración › Terceros › Crear», no «Stakeholders». El rol se llama «Empresa de transporte». Hay casilla «UAP». El NIT es único: «Ya existe un tercero con número de identificación {n}.». El estado financiero **no es un campo**: solo se lee y vale «Activo», «Vencido» o «Bloqueado». La configuración de facturación está en Facturación › Configuraciones. CE también crea terceros. | CHG-03, CHG-49, `StakeholderForm.vue`, `stakeholder-utils.ts` | 1.3 |
| 1.3 | Cómo crear productos y tipos de embalaje | Admin | Actualizar | Hay SKU autogenerado y editable, y «Unidad de medida» obligatoria. SKU y nombre son únicos. No hay toast de éxito. Los embalajes no vienen sembrados. **Falso que el cobro use el código del embalaje:** las fórmulas usan el tipo de unidad de carga o la unidad de medida. | CHG-41, CHG-49, `ProductForm.vue`, `SeedDataExtensions.cs:395-497` | 1.4 |
| 1.4 | Servicios (I): crear un servicio, IVA y precio base | Admin | Actualizar | No hay pestañas: hay paneles «Información del Servicio» (con «Impuestos» y «Agregar») e «Historial de precios» («Nuevo precio», solo «Vigente desde», sin fecha futura). El precio nuevo vence al anterior. MONTACARGAS no admite impuestos y ALMACENAMIENTO no tiene precio base. En una base nueva, BASCULA no trae IVA: se asigna aquí. | WMS-28, §10 «IVA en báscula», `services/[id].vue`, `ServicePricesList.vue` | 1.6 |
| 1.5 | Servicios (II): reglas de tarificación | Admin | Reemplazar | Ahora se llaman «Tarifas base» y solo existen en la ficha de ALMACENAMIENTO. Campos nuevos: «Aplica a» (perecederos), «Servicio complementario (opcional)», «IVA incluido en la tarifa» y «Previsualizar». La tarifa nace activa. El 409 de unicidad sale bajo el producto. | CHG-26, CHG-27, CHG-64, `ServicePricingRuleFormDialog.vue` | 1.7 |
| 1.6 | Servicios (III): valores mínimos por modalidad | Admin | Actualizar | El panel se llama «Valores mínimos por tipo de depósito». Tiene la columna «Base» y el selector «El valor mínimo se digita: Con IVA incluido / Neto (se suma el IVA)». Es el respaldo cuando no hay convenio ni tarifa base. Sembrados en $0. | CHG-24, `ServiceMinimumValuesCard.vue` | 1.8 |
| 1.7 | Cómo configurar las tarifas de montacargas | Admin | Actualizar | Tabla editable con «Guardar» por fila y el toast «Tarifa actualizada». El convenio gana solo si su servicio MONTACARGAS no tiene producto, modalidad ni perecedero. El IVA se decide al cobrar. | CHG-09, WMS-28, `ForkliftRatesGrid.vue` | 1.9 |
| 1.8 | Catálogos de apoyo: vehículos, conductores, motivos y ubicaciones | Admin | Reemplazar | Se divide en dos. Vehículos y Conductores **no muestran «Nuevo»** en Administración (solo consultar y «Editar»; el vehículo no tiene transportadora): nacen en Vigilancia y Báscula. Las ubicaciones **ya no vienen sembradas**, así que crearlas es imprescindible. El motivo tiene «Requiere Pesaje», que decide entre la cola de báscula y la recepción directa. | CHG-05, migración `RemoveSampleSeedData`, `drivers/index.vue`, `vehicles/index.vue`, `locations/index.vue` | 1.10, 1.11 |
| 1.9 | Parámetros del sistema y auditoría | Admin | Actualizar | La auditoría **no tiene filtro de fecha**: filtra por «Usuario», «Acción» y «Tabla». No guarda contraseñas y ahora registra catálogos y roles. Los parámetros se abren desde «Mi cuenta» › «Parámetros del sistema». Son 7: `INVENTORY_ADJUSTMENT_ADMIN_EMAIL` y 6 datos de la empresa para los PDF. | CHG-02, CHG-68, CHG-84, `audit/index.vue`, `AppRightMenu.vue` | 1.13 |

### Serie 2 · Acuerdos (Convenios)

| v1 | Título v1 | Rol | Estado | Qué cambió | Fuente | v2 |
|---|---|---|---|---|---|---|
| 2.1 | Qué es un acuerdo y su ciclo de vida | Admin | Actualizar | Se llega por «Administración › Terceros › Clientes» o «Facturación › Clientes» → «Ver detalle» → sección «Gestión de Acuerdos». No es pestaña ni hay ítem «Convenios». La sección solo aparece si el tercero es «Cliente». Un acuerdo «Programado» no se activa solo. Un cliente tiene un solo acuerdo activo. | §10 «Menú», CHG-03, MAF-08, `stakeholders/[id].vue:20` | 2.1 |
| 2.2 | Cómo crear un acuerdo y agregar un servicio | Admin | Actualizar | «Crear Acuerdo» pide «Estado» (Borrador por defecto). Servicios: «Ver detalle» › «Agregar servicio al acuerdo». Campos nuevos: «Aplica a», «Servicio complementario (opcional)» (antes «servicio vinculado»), «Activo» e «IVA incluido en la tarifa». La unicidad incluye el tipo de carga. | CHG-26, `AgreementForm.vue`, `AgreementServiceFormDialog.vue` | 2.2 |
| 2.3 | Las fórmulas de tarifa | Admin | Reemplazar | Nombres reales: «Fijo», «Por unidad de medida», «Por vehículo», «Por tipo de vehículo (montacargas)». **«Por unidad de embalaje» ya no existe:** la reemplaza «Por unidad de carga». Se suman «Mínimo por unidad de carga ($)» y el check «El mínimo incluye IVA…». | WMS-18, WMS-30, CHG-24, CHG-25, `SeedDataExtensions.cs:395-497` | 2.3 |
| 2.4 | Las fórmulas de porcentaje del valor | Admin | Actualizar | Nombres: «Porcentaje del valor declarado (sin prorrateo)» y «… (prorrateado por saldo)». El mínimo ya no es siempre con IVA: lo decide un check, marcado por defecto. Con porcentaje no aparece «IVA incluido en la tarifa». El rango 0–100 lo valida el API. | CHG-24, CHG-27 | 2.4 |
| 2.5 | Parámetros y la regla de especificidad | Admin | Actualizar | Se mantiene el orden producto+modalidad › producto › modalidad › general. Precisiones: una regla de otra modalidad nunca aplica, y «Solo perecederos» va antes que todo. Se agregan los niveles acuerdo › tarifa base › precio base › mínimo. | CHG-09, DEF-F6-001, `RuleSpecificity.cs` | 2.7 |
| 2.6 | Activar, programar y archivar un acuerdo | Admin | Reemplazar | No hay «Archivar»: «Desactivar» deja el acuerdo «Archivado». «Activar» pide confirmar y archiva el activo anterior. Solo se programa al crear, y **nada lo activa en la fecha**. Un archivado se puede reactivar. Se suma editar y quitar servicios. | MAF-08, `AgreementDetailDialog.vue`, `Stakeholder.cs:231-256` | 2.8 |
| 2.7 | Ejemplo completo: convenio de almacenamiento | Admin | Actualizar | El mismo ejemplo con los nombres nuevos, «Tipo de depósito» explícito (una regla IMP no cubre EXP), el check del IVA del mínimo y «Previsualizar». | Todo lo anterior | 2.9 |

### Serie 3 · Facturación

| v1 | Título v1 | Rol | Estado | Qué cambió | Fuente | v2 |
|---|---|---|---|---|---|---|
| 3.1 | Configuración de facturación del cliente | Facturación | Actualizar | Hay ocho ciclos con días explícitos y «Bajo demanda» se retiró. «Consolidada» tiene texto nuevo: solo depósitos y guías a crédito; báscula y montacargas siguen individuales. El límite vacío significa «Sin límite» y desbloquea al instante. Se entra por «Nueva Configuración» o «Editar». No hay control «Activa». | CHG-60, CHG-61, CHG-63, D-1, `BillingConfigForm.vue` | 3.1 |
| 3.2 | Tablero y panorama del módulo | Facturación | Actualizar | Cinco indicadores: «Facturado este mes», «Cartera pendiente», «Facturas vencidas», «Borradores» y «Total facturas». Además «Acciones Rápidas», «Últimas Facturas» y «Clientes con Mora». El menú tiene 10 entradas. | `billing/index.vue`, `AppMenu.vue:445-503` | 3.2 |
| 3.3 | Cómo el sistema calcula una factura | Facturación | Actualizar | La jerarquía se ve en la columna «Método cálculo»: «Acuerdo (nivel 1)» › «Tarifa base (nivel 2)» › «Precio base (nivel 3)» › «Valor mínimo». El mínimo es solo de almacenamiento y se configura con IVA o neto. El almacenamiento cobra por cargo. Se elimina la remisión al «manual, capítulo 7». | CHG-09, CHG-24, `invoices/[id].vue:163-184` | 3.3 |
| 3.4 | Facturación de báscula | Facturación | Reemplazar | Pestaña «Báscula» en lugar de filtro. La factura de contado nace «Pagada» sin N.º y con pago «Recibido»: se verifica el pago y se asigna el N.º una vez. La de «Por facturar» nace en Borrador. Se fusiona con 3.5 y se suma la factura en cero del depósito adicional. | CHG-12, CHG-22, CHG-23, FAC-9, DEF-F11-003 | 3.4 |
| 3.5 | Facturación de montacargas | Facturación | Reemplazar | Se fusiona en 3.4. El detalle **no muestra el origen de la tarifa** («Método cálculo» = «—»); el paso 2 v1 era falso. El «Impuesto %» de la línea es 0 o 19 según «Agregar IVA (19%)». | `EndForkliftUseCommandHandler.cs:143-150`, WMS-28 | 3.4 |
| 3.6 | Facturación de almacenamiento y depósitos pendientes | Facturación | Actualizar | Depósitos Pendientes lista depósitos **ya facturados con período abierto**. Columnas «Días», «Valor mercancía» («TRM pendiente») y «Por refacturar». El resumen no muestra cargos por producto. El valor mínimo se ve con la etiqueta «Valor mínimo» y el aviso «Sin acuerdo ni precio establecido». Corrección con «Sobrescribir total de la línea» (video propio). El cierre manual de período **no tiene pantalla**. | CHG-10, CHG-11, CHG-66, UI-07 | 3.5 |
| 3.7 | Ciclo de vida de la factura | Facturación | Actualizar | Todo en el diálogo «Acciones de la factura». El N.º SIIGO es único, solo en Borrador, y queda fijo al aprobar. **Aprobar fija el vencimiento.** Enviar solo marca «Enviada». La factura en $0 no lleva número. Anular pide motivo ≥ 10 y no se permite con dinero. «Pendiente de aprobación» no se alcanza. | WMS-20, CHG-12, CHG-22, `InvoiceActionsDialog.vue`, `invoice-action-rules.ts` | 3.7 |
| 3.8 | Pagos, ajustes y destinatarios | Facturación | Reemplazar | Pagos solo en facturas emitidas, con comprobante JPG, PNG, WEBP o PDF de hasta 5 MB. Nacen «Verificado». Verificar o rechazar solo aplica a los «Recibido» de contado. El override pasa a video propio y ahora fija el **total con IVA incluido**. **El cambio de destinatario se retiró** de la pantalla. | CHG-11, CHG-18, CHG-22, CHG-29, FAC-9, commit FE `5f237f7` | 3.8, 3.6 |

### Serie 4 · Vigilancia

| v1 | Título v1 | Rol | Estado | Qué cambió | Fuente | v2 |
|---|---|---|---|---|---|---|
| 4.1 | Cómo registrar el ingreso de un vehículo | Vigilancia | Actualizar | Captura mínima: «Placa», «Motivo de ingreso», «Observaciones». **Sin conductor, transportadora ni fecha** (se capturan en Báscula; la hora la pone el sistema). Con Enter se ve «Vehículo encontrado.» o «No existe, se creará al registrar.». Formato de placa con el mensaje «Placa no válida…». Doble ingreso: «Ingreso duplicado». Botón «Registrar ingreso». | CHG-05, CHG-52, `entries/index.vue` | 4.1 |
| 4.2 | Cómo controlar la salida de un vehículo | Vigilancia | Reemplazar | No hay autorización de salida ni manifiesto. Tarjetas «Camiones en planta» → «Registrar salida» → confirmación. Bloqueos: pesaje sin terminar (CHG-30) y orden de importación sin guía (CHG-33). | CHG-15, CHG-30, CHG-33, CHG-52, `exits.vue` | 4.2 |
| 4.3 | Historial y búsqueda por placa | Vigilancia | Actualizar | Filtros «Placa» (parcial) y «Motivo de ingreso»; **sin fecha**. Columnas nuevas «Salida» («Abierto») y «Corrección». «Completado» no significa que salió. | CHG-05, DEF-F11-016, `history.vue` | 4.3 |

### Serie 5 · Báscula

| v1 | Título v1 | Rol | Estado | Qué cambió | Fuente | v2 |
|---|---|---|---|---|---|---|
| 5.1 | El ciclo de pesaje: primer y segundo peso | Báscula | Reemplazar | La báscula es una pantalla única: «Cola de camiones» con filtros «Todos / Sin iniciar / Por cobrar / Por pesar / Por repesar» y ficha con los pasos Registro › Cobro › Peso › Tiquete. Las «tres modalidades» ahora son tipos de operación: «Ingreso con depósito», «Salida de mercancía» y «Solo báscula». El Dashboard cambió. | WMS-31, CHG-76, `TruckQueue.vue`, `OperationTypeSelector.vue` | 5.1 |
| 5.2 | Pesaje solo (sin almacenamiento) y cobro | Báscula | Actualizar | Se llama «Solo báscula». Orden: registro («Cliente» obligatorio, «Tiene segundo pesaje») → «Guardar» → cobro → peso → tiquete. Se cobra **antes** de pesar. Destinatario «Conductor del vehículo». Botón «Cobrar». Sin efectivo ni cambio. | CHG-19, CHG-46, CHG-53, `WeighingOnlyForm.vue` | 5.2 |
| 5.3 | Pesaje para almacenamiento | Báscula | Reemplazar | «Ingreso con depósito» con registro único: «Documento» (modalidad, búsqueda automática, manifiesto), «Mercancía de este camión», panel plegado «Datos para Comercio Exterior» (opcional) y «Pesaje y observaciones». Al guardar crea el depósito en Borrador («Depósito 2026BA… creado»). | WMS-9, WMS-31, BAS-01, `StorageServiceForm.vue` | 5.3 |
| 5.4 | Pesaje de salida | Báscula | Actualizar | «Salida de mercancía»: buscar la orden por número (interno o externo) o placa, y «Cómo sale» (pesar o con el tiquete de ingreso). La orden pasa a «en cargue». El repesaje exige la orden cargada y, en importación, la guía. «Agregar otra orden a este pesaje». | CHG-32, CHG-33, `OutputServiceForm.vue` | 5.9 |
| 5.5 | Pago inmediato vs. facturación diferida | Báscula | Actualizar | Opciones «Inmediato» / «Por facturar». Se propone el cliente de la operación. «Por facturar» crea la factura igual (báscula no consolida, D-1). Mensaje de mora exacto. **«Cambiar modo de pago» se retiró (D-2).** | D-1, D-2, CHG-19, CHG-47 | 5.4 |
| 5.6 | Segundo peso pendiente y cierre de ciclo | Báscula | Reemplazar | No existe «Báscula › En proceso»: se usa el filtro «Por repesar» o «Capturar peso». Nuevo: «Falta llegada a Bodega», hora propuesta y corregible, tara ≤ bruto, F2, «Salir y atender otro camión» y el paso Tiquete. | CHG-36, CHG-37, CHG-44, `WeightCapture.vue` | 5.5 |
| 5.7 | Recuperar incompletos y corregir pesos | Báscula | Reemplazar | Se divide en dos. «Recuperar operaciones» es un botón del encabezado, con «Retomar» y «Descartar» (el camión vuelve a «Sin iniciar»). La corrección de pesos va en Historial › detalle, con «Razón de la Modificación» (≥ 10), autor visible y aviso al Admin. Se suman corregir fecha y «Anular pesaje». | CHG-06, CHG-20, CHG-47, GAP-005, DEF-F11-007 | 5.10, 5.11 |
| 5.8 | Tickets y reporte diario de facturación | Báscula | Actualizar | El tiquete (N.º `2026T…`) se imprime en el paso 4 de la ficha o desde el Historial. Reportes = «Reporte de Facturación Diaria»: un día, una fila por tiquete, solo PDF. El Excel está en Historial. | CHG-76, DEF-F11-018, `reports.vue` | 5.12 |

### Serie 6 · Bodega

| v1 | Título v1 | Rol | Estado | Qué cambió | Fuente | v2 |
|---|---|---|---|---|---|---|
| 6.1 | Cómo recibir mercancía desde báscula | Bodega | Reemplazar | Son dos pantallas: Ingresos › «Ingresar» (llegada, obligatoria antes del segundo pesaje) y Recepción › «Completar recepción». Se cuenta, se ubica, se firma (obligatorio) y se fotografía (máx. 5). **La recepción no mueve stock:** el stock viene de lo declarado en báscula y la diferencia se avisa a CE. | WMS-9, CHG-15, CHG-36, CHG-55, CHG-56, CHG-72 | 6.1, 6.2 |
| 6.2 | Recepción directa (sin báscula) | Bodega | Actualizar | Se llega por Recepciones › **Recepción** › «Recepción Directa». Es para ingresos cuyo motivo no pide pesaje. Formulario largo con modalidad fija «INSP - Inspección», ubicación y firma obligatorias. El depósito queda en **Borrador** para CE. Rechazo por cliente bloqueado. | CHG-08, CHG-85, §10 «Recepción sin báscula» | 6.4 |
| 6.3 | Cómo registrar el uso de montacargas | Bodega | Actualizar | Al iniciar se busca la **placa**; no se elige cliente. El cobro es una tarifa fija por tipo de vehículo, no por hora, precargada y editable. El check es «**Agregar IVA (19%)**», desmarcado. Modos «Pago inmediato» y «Pendiente por facturar». Botón «Finalizar y cobrar». | WMS-28, CHG-58, `ForkliftUseDialog.vue`, `BillingCollectForm.vue` | 6.5 |
| 6.4 | Órdenes de cargue: ejecutar el despacho | Bodega | Actualizar | Pestañas «Pendientes» y «Todas las Órdenes», con botones «Ver» y «Ejecutar». Cargue parcial por ítem, **firma obligatoria**, fotos (máx. 5) y «Confirmar Ejecución». Tabla final con «Retirar de». Exige depósitos confirmados. | CHG-15, CHG-31, CHG-32, CHG-55, GAP-006 | 6.6 |
| 6.5 | Inventario y ajustes | Bodega | Actualizar | Pestañas «Consultar Stock», «Movimientos» (kárdex) y «Ubicaciones». Aparecen los Borradores con mercancía recibida. **El paso del ajuste se retira:** Bodega no ajusta; el CE-7 es de Comercio Exterior y se ve como «Ajuste CE-7». | CHG-39, CHG-74, `InventoryAdjustmentController.cs:21` | 6.7 |

### Serie 7 · Comercio Exterior

| v1 | Título v1 | Rol | Estado | Qué cambió | Fuente | v2 |
|---|---|---|---|---|---|---|
| 7.1 | Gestión del depósito: confirmar, corregir, cancelar | Comercio Exterior | Actualizar | «Confirmar depósito» está deshabilitado mientras falten requisitos, y la lista «Para confirmar el depósito … falta:» tiene enlaces. Confirmar no espera a Bodega. El primer período cuenta desde la **fecha de ingreso**. Hay «Cerrar ingreso de camiones». «Devolver para corrección» solo existe en Confirmado y dentro de «Productos del Depósito». «Cancelar» se llama «Anular depósito» (video propio). | WMS-9, WMS-26, WMS-33, CHG-21, CHG-31, `DepositConfirmationRequirements.cs` | 7.3 |
| 7.2 | Cliente, terceros y contenedores del depósito | Comercio Exterior | Actualizar | Los terceros asignables son «Importador», «Agencia de aduanas (SIA)» y «Exportador», con la etiqueta «Obligatorio para confirmar». **La transportadora ya no se asigna aquí.** Las unidades de carga nacen en báscula: CE solo «Corregir» y «Repartir mercancía del camión». Se suman la «Información General» editable y el manifiesto por camión. | WMS-30, CHG-21, `DepositDetailDocumentStakeholdersSection.vue` | 7.2 |
| 7.3 | Importaciones: validación y liberaciones | Comercio Exterior | Reemplazar | **«Validar depósito» no tiene botón** (§4). Las «liberaciones» son **levantes**: «Registrar Levante» en Confirmado, con FOB y tasa, y opciones para registrar otro producto, editar y retirar. Un levante, aunque sea parcial, deja el depósito «Nacionalizado». El Manifiesto DIAN del depósito no es requisito; el de cada camión sí. | CHG-40, CHG-70, UI-18, §10 «Etiqueta con levante parcial» | 7.7 |
| 7.4 | Rótulos y documentos PDF | Comercio Exterior | Actualizar | La etiqueta se imprime **desde Borrador**. «Documentos» tiene «Descargar etiqueta» y «PDF consolidado». Contador de impresiones con historial. Textos «MERCANCIA SIN NACIONALIZAR» / «MERCANCIA NACIONALIZADA». | WMS-15, CHG-69, CHG-73, `LabelGenerationService.cs` | 7.4 |
| 7.5 | Exportaciones e inspecciones | Comercio Exterior | Reemplazar | Ya no están en el menú: se llega por el Kanban de «Depósitos» con el tipo «Exportación» o «Inspección». Se absorbe en el video del Kanban. | `AppMenu.vue:299-446`, `deposits/index.vue` | 7.1 |
| 7.6 | Cómo crear una orden de cargue | Comercio Exterior | Reemplazar | Formulario único en 4 bloques: «Orden de cargue externa» (el WMS ya no emite la orden), «Depósitos de la Orden» (multi-cliente, solo lo nacionalizado), «Vehículo y Conductor» y «Destino y Programación» (ciudad obligatoria). Estado financiero por cliente. No descarga PDF. | WMS-17, CE-12, GAP-002, GAP-025 | 7.10 |
| 7.7 | Guías de salida: generar, pendientes e historial | Comercio Exterior | Actualizar | «Continuar al cobro» abre «Facturación y Cobro — Guía de Salida», con una fila por cliente dueño y «Total a cobrar» **antes** de crear. Firmante, vencimiento por días de tránsito y saldos congelados en el PDF. Sin guía vigente no hay repesaje ni salida. Historial con ZIP y «Anular guía». Se divide en dos. | CHG-33, CHG-34, CHG-35, CHG-43, WMS-19 | 7.12, 7.13 |

## 3. Guiones nuevos (33)

| v2 | Título | Rol | Por qué | Fuente |
|---|---|---|---|---|
| 0.3 | Recuperar o restablecer la contraseña | Admin y todos | Recuperación por correo solo para el Admin; los demás piden «Resetear Contraseña». | CHG-51 |
| 0.4 | Notificaciones, Mi cuenta y cerrar sesión | Comercio Exterior | Campana, página de notificaciones, «Mi cuenta», tema, atajos y cierre de sesión. | `NotificationPanel.vue`, `AppRightMenu.vue`, CHG-16 |
| 0.5 | Trazabilidad: seguir un camión por etapas | Comercio Exterior o Admin | Página de inicio de Admin y CE; 13 etapas; búsqueda por placa en la barra superior. | CHG-42, CHG-81, `features/traceability` |
| 1.2 | Gestionar la cuenta de un usuario | Admin | «Resetear Contraseña», «Asignar Roles» / «Remover Roles», inactivar; reglas de un Admin activo. | CHG-16, CHG-50 |
| 1.5 | Unidades de medida y tipos de unidad de carga | Admin | Catálogos nuevos cuyos códigos usan las fórmulas. | WMS-18, WMS-30 |
| 1.11 | Motivos de entrada, conductores y vehículos | Admin | Sale del v1 1.8: motivos con «Requiere Pesaje», consulta y corrección de conductores y vehículos. | CHG-05, `entry-reasons/index.vue` |
| 1.12 | Ciudades y cuadrillas | Admin | Pantallas nuevas: días de tránsito para el vencimiento de la guía y destino de abandono; cuadrillas. | GAP-025, GAP-026 |
| 2.5 | Previsualizar una tarifa | Admin o Facturación | Calcula con valores de ejemplo, igual que el cobro real. | D36, CHG-64 |
| 2.6 | Tarifas para carga perecedera | Admin o Facturación | «Aplica a: Solo perecederos» y la fórmula «Por umbral de peso (perecederos)». | WMS-32, CHG-26 |
| 2.10 | Convenio de montacargas y servicio complementario | Admin o Facturación | «Por tipo de vehículo (montacargas)» en el acuerdo y «Servicio complementario». | CHG-09, MAF-07 |
| 3.6 | Sobrescribir el total de una línea | Facturación | El override fija el total con IVA incluido, con desglose en vivo; una vez por línea y solo en Borrador. | CHG-11 |
| 3.9 | TRM pendiente y TRM manual | Facturación | La TRM salió de báscula; Facturación la registra si la DIAN no responde. | WMS-24 |
| 3.10 | Anular y refacturar una factura de almacenamiento | Facturación | «Refacturar» crea una factura nueva en Borrador; el reporte por CPI conserva la anulada. | UI-07, CHG-22, CHG-65 |
| 3.11 | Factura recalculada después de emitida | Facturación | Camión tardío, TRM manual o CE-7 actualizan la misma factura y avisan. | D10/D11, DEF-F11-017 |
| 3.12 | Cartera, mora y bloqueo del cliente | Facturación | Estados «Activo / Vencido / Bloqueado», desbloqueo inmediato al pagar o quitar el límite. | CHG-13, CHG-61, CHG-62 |
| 3.13 | Reportes de Facturación: anual y por CPI | Facturación | Reportes nuevos del menú. | GAP-016, CHG-65 |
| 4.4 | Corregir un ingreso | Vigilancia | Placa, motivo y fecha con motivo de corrección y confirmación. | WMS-5 |
| 5.6 | Ingreso con unidades de carga e inspección | Báscula | «Tipo de carga: Unidades de carga» y la modalidad «Inspección» (un solo pesaje). | WMS-30, `CargoUnitsEditor.vue` |
| 5.7 | Varios camiones con el mismo documento | Báscula | «Camiones ingresados: N», «Ver camiones» y documento con ingreso cerrado. | WMS-26, CHG-54 |
| 5.8 | Multidepósito: agregar otro depósito | Báscula | Depósito adicional, factura en cero y pesaje intermedio. | CHG-45, DEF-F11-003 |
| 5.11 | Historial de báscula: corregir, anular y reimprimir | Báscula | Sale del v1 5.7 y 5.8: corregir peso y fecha, «Anular pesaje», «Imprimir Ticket», Excel. | CHG-47, GAP-005 |
| 6.1 | Registrar la llegada del camión | Bodega | Sale del v1 6.1: «Ingresar» es obligatorio antes del segundo pesaje. | CHG-36 |
| 6.3 | Recibir unidades de carga | Bodega | «Recibida completa» por unidad, sin contar productos. | CHG-07, WMS-30 |
| 6.8 | Novedades de mercancía | Bodega | Registrar, desglose que no cuadra, «REPORTE DE MERCANCÍAS», anular. | GAP-015, CHG-57 |
| 6.9 | Inventario general e historiales de Bodega | Bodega | Reporte de inventario general, historial de recepciones y de montacargas. | GAP-016, CHG-58 |
| 7.5 | Corregir los productos del depósito | Comercio Exterior | Agregar, editar, cambiar y eliminar productos en Borrador; «Devolver para corrección». | WMS-29, CHG-31 |
| 7.6 | Ajustar la cantidad del depósito (CE-7) | Comercio Exterior | Movimiento «Ajuste CE-7», correo al Admin, recálculo de la factura. | CHG-38, CHG-39 |
| 7.8 | Abandono y prórrogas | Comercio Exterior | Plazo de 30 o 60 días y «Registrar prórroga». | GAP-003 |
| 7.9 | Listas de empaque | Comercio Exterior | Cargar el CSV del proveedor y asociar artículos al camión. | GAP-013 |
| 7.11 | Modificar, cancelar y revertir una orden de cargue | Comercio Exterior | «Modificar ítems», «Cancelar Orden», «Revertir salida». | GAP-006, CHG-31 |
| 7.13 | Guías pendientes e historial de guías | Comercio Exterior | Sale del v1 7.7: pendientes, PDF, ZIP por depósito, «Anular guía». | CHG-33, CHG-43 |
| 7.14 | Anular un depósito | Comercio Exterior | Motivo, resultado y solo lectura. | CHG-67, DEF-F11-012 |
| 7.15 | Reportes de Comercio Exterior | Comercio Exterior | Nueve reportes del menú. | GAP-003, GAP-010, GAP-016, CHG-79, CHG-82 |

## 4. Funciones y pasos que se retiran de los guiones

| Qué | Dónde estaba | Por qué | Fuente |
|---|---|---|---|
| «Cambiar modo de pago» en báscula | v1 5.5 (implícito) e Historial de báscula | Decisión D-2: un cobro «por facturar» se paga en Facturación › Pagos. | D-2, CHG-47 |
| Efectivo recibido y cambio a devolver | v1 5.2, 5.5 | Decisión del 2-oct-2026; también retirado del API. | §10, CHG-53 |
| Autorización de salida y manifiesto en Vigilancia | v1 4.2 paso 3 | No hay botón; los diálogos de `history.vue` son código muerto. | `history.vue:345-462` |
| Conductor y transportadora en el ingreso de Vigilancia | v1 4.1 paso 3 | Bloque comentado; se capturan en Báscula. | `entries/index.vue:327-362` |
| Cambio de destinatario de una factura | v1 3.8 paso 4 | Se quitó de la pantalla el 8-jul-2026. | FE `5f237f7` |
| «Validar depósito» | v1 7.3 paso 2 | El diálogo existe, pero ningún botón lo abre. | `imports/[id]/index.vue:810` |
| Ajuste de inventario por Bodega | v1 6.5 paso 3 | El CE-7 es de Comercio Exterior. | `InventoryAdjustmentController.cs:21` |
| Agregar o eliminar contenedores desde CE | v1 7.2 paso 3 | Las unidades nacen en báscula; CE solo corrige y reparte. | WMS-30 D29 |
| Páginas «En proceso», «Pendientes de repesaje» y «Recuperar» del menú de báscula | v1 5.6, 5.7 | Son filtros de la cola y un botón del encabezado. | WMS-31 D11 |
| «Archivar» un acuerdo | v1 2.6 | El botón es «Desactivar» y deja «Archivado». | `AgreementDetailDialog.vue` |
| Ciclo «Bajo demanda» | v1 3.1 | Retirado. | CHG-60 |
| Fórmula «Por unidad de embalaje» (`packagingTypeCode`) | v1 2.3 | No existe; la reemplaza «Por unidad de carga». | WMS-30 |
| Estadísticas | Menú Dashboards | Oculta por decisión del usuario (6-oct-2026). Sin guion. | `AppMenu.vue:30` |
| Cierre manual de período de almacenamiento | — | Corregido en el backend (CHG-10), pero sin pantalla. Sin guion. | CHG-10 |
| Respaldos y migración del legacy | — | Tareas técnicas sin pantalla. Sin guion. | Encargo |

## 5. Diferencias entre documentos y código (el guion sigue al código)

| # | Documento | Dice | El código hace | Fuente del código |
|---|---|---|---|---|
| 1 | Contexto §12 y AGENTS.md | La Ola 1 está sin implementar. | Está implementada: stock declarado, «Cerrar ingreso de camiones», TRM fuera de báscula, consecutivos `2026BA…`/`2026T…`, acciones de factura, IVA del montacargas. | `InitiateStorageWeighingHandler.cs:403`, `DocumentNumberFormat.cs` |
| 2 | Encargo | Planes `plan_implementacion_ola2.md`, `plan_implementacion_ola3.md` y el de la Ola 1 en `code_workspace/ajustes/`. | **No existen** en `ajustes/` ni en el resto del proyecto. Se usó el código y los planes de paridad y de corrección. | `ls code_workspace/ajustes` |
| 3 | Encargo y guía de operarios §7 | Check «Aplicar IVA». | El texto es «**Agregar IVA (19%)**». | `BillingCollectForm.vue:234` |
| 4 | Contexto §7.3 | Fórmulas `PER_CONTAINER`, `FIXED_PER_CONTAINER`, `PER_PACKAGING_UNIT`. | No existen. Existen «Por unidad de carga» y «Por umbral de peso (perecederos)». | `SeedDataExtensions.cs:395-497` |
| 5 | Contexto §6 y guía de operarios §8 | «Nacionalizado» cuando los levantes cubren toda la cantidad. | Basta **un** levante, aunque sea parcial. | `ImportWarehouseStorage.cs:114-121`, §10 |
| 6 | Contexto §7.4 | El período cuenta desde la confirmación. | Empieza en la **fecha de ingreso** del depósito. | `ConfirmStorageDepositHandler.cs:74-80` |
| 7 | Contexto §5.1, guía de operarios §6 | Báscula declara cantidad, peso neto y peso bruto por producto. | Solo «Cantidad de este camión» por producto; el único peso declarado es «Peso según manifiesto (kg)» por camión. | `TruckGoodsLines.vue:262-265`, CHG-82 |
| 8 | Contexto §7.9, §10 «Mora» | Un cliente bloqueado no puede pagar báscula. | Solo se valida si el destinatario es «Tercero registrado»; con conductor, persona no registrada o consumidor final se cobra sin aviso. | `BillingRecipientFactory.cs:97-100` |
| 9 | §10 «Permisos de catálogos» | Convenios y tarifas: Admin y Facturación. | El API lo permite, pero las páginas de servicios y de montacargas exigen Admin. Facturación solo gestiona acuerdos. | `admin/services/*.vue`, `admin/forklift-rates/index.vue` |
| 10 | Contexto §7.6 | Borrador → Pendiente de aprobación → Aprobada. | «Pendiente de aprobación» nunca se alcanza: se pasa de Borrador a Aprobada. | `Invoice.cs` |
| 11 | Contexto §7.2 | Cuatro ciclos con `OnDemand`; quincena de 14 días. | Ocho ciclos, sin «Bajo demanda»; quincenas de 14 y de 15 días. | `BillingCycleCatalog.cs:26-33` |
| 12 | Contexto §7.8 | Pagos con N.º de recibo y fecha de consignación. | La pantalla no pide esos campos; los pagos de Facturación nacen «Verificado». | `PaymentDialog.vue`, `RecordPaymentHandler.cs:52-58` |
| 13 | Guion v1 1.2, tarea | «Activo / Aviso por mora / Bloqueado». | La UI dice «Activo / Vencido / Bloqueado»; en la orden de cargue, «Cliente con Mora». | `stakeholder-utils.ts:18-24`, `FinancialStatusAlert.vue` |
| 14 | Guía de operarios §1 | CE inicia en Comercio Exterior → Dashboard. | CE y Admin inician en Dashboards › Trazabilidad. | `role-routes.ts:4-5` |
| 15 | Guía de operarios §2.4, v1 0.2 | «¿Olvidó su contraseña?». | El botón es «Recuperar contraseña». | `login.vue:118` |
| 16 | Contexto §10 | Ubicaciones `A01-R01-N01…` sembradas; embalaje `TANQUERO`; unidad «Tractomula». | Ninguna se siembra en una base nueva: las ubicaciones se borran (`RemoveSampleSeedData`), «Tanquero» es un tipo de unidad de carga y «Tractomula» es un tipo de vehículo. | `SeedDataExtensions.cs`, migración `20261007030137` |
| 17 | Contexto §3 | `WarehouseAccess` incluye Vigilancia. | Vigilancia solo ve Vigilancia. | CHG-03, `WmsPolicyRolesTests.cs` |
| 18 | Guía de operarios §5 | Historial filtra por fecha; la corrección de ingreso cambia el conductor. | Sin filtro de fecha; la corrección cambia placa, motivo y fecha, no el conductor. | `history.vue`, `CorrectEntryLogDialog.vue` |
| 19 | Contexto §5.3 | La orden de cargue genera un PDF. | No lo genera: se registra la orden externa. Bodega descarga la «Orden de trabajo (PDF)». | WMS-17, `useCreateLoadingOrder.ts` |
| 20 | Contexto §7.7 | Tres causas de recálculo. | Nueve motivos (camión adicional, TRM, CE-7, manifiesto, fecha de ingreso, edición de productos, anulación de pesaje, reversión, refacturación). | `StorageRecalculationTrigger.cs` y otros |
| 21 | Guiones v2.0 5.2, 5.3, 5.9 y 6.4 (antes del 2026-10-08) | El conductor se digita campo por campo en «Camión y conductor» y en la Recepción Directa. | Selector con buscador (nombre o documento), «+» para registrar y lápiz para corregir (selector de conductor, 2026-10-08). Los guiones eligen al conductor que ya existe (Jaime en 5.9) y registran con «+» al que no (Mario en 5.2, Luis en 5.3, Hugo en 6.4), según el orden de grabación de `dataset-grabacion.md` §3. | `DriverPicker.vue`, `DriverFormDialog.vue` (FE `7d7516a`) |

## 6. Hallazgos que afectan la grabación (decisión antes de grabar)

| # | Hallazgo | Propuesta para los guiones |
|---|---|---|
| H1 | Trazabilidad muestra valores en inglés sin traducir («Input», «Complete», «Draft», «SinNacionalizar»). | Grabar 0.5 sin acercar esos campos; dejar el texto `[verificar en pantalla]`. |
| H2 | «Validar depósito» no tiene botón. | No grabarlo; queda en §4. |
| H3 | Facturación no puede abrir «Tarifas base» ni «Tarifas de montacargas». | Los videos 1.6 a 1.9 los graba el Admin; la Serie 2 dice «Admin o Facturación» solo para los acuerdos. |
| H4 | Un acuerdo «Programado» nunca se activa solo. | 2.8 dice que hay que activarlo con «Activar». |
| H5 | El diálogo «Agregar servicio al acuerdo» se cierra antes de la respuesta; un error borra lo digitado. | Los guiones no provocan errores en ese diálogo. |
| H6 | La mora en báscula solo bloquea con «Tercero registrado». | La narración dice «si el destinatario es el cliente bloqueado…». |
| H7 | Conductores y Vehículos de Administración no muestran «Nuevo» (por código). | 1.11 los presenta como consulta y corrección; `[verificar en pantalla]`. |
| H8 | El Dashboard de báscula tiene la tarjeta «Acerca del Módulo» con flujos obsoletos; los placeholders de Inventario y Movimientos dicen «DEP-…». | Encuadrar sin esa tarjeta; escribir el número `2026BA…` real. |
| H9 | Varias acciones no tienen toast de éxito (servicios, tarifas base, activar acuerdo, crear producto, override). | El resultado esperado del guion es el cambio en pantalla, no un mensaje. |
| H10 | No se pudo entrar a staging: el uso de contraseñas en un sitio que no es local no está permitido para el agente. | Los textos no confirmados en el código van con `[verificar en pantalla]`. |

## 7. Videos que el plan de brechas P1 deja desactualizados (2026-10-24)

> **Origen:** `planes/plan-cerrado-brechas-paridad-p1-2026-10-23.md` §15.4. **Solo se anota; no se graba** (se regraban fuera de ese plan, después del despliegue de la fase 13). Código de referencia: Backend `560f558` / Frontend `e2e11e6`. La numeración es la de `guiones-video-tutoriales.md` (v2).

| Video | Qué cambió en pantalla o en reglas | Plan P1 |
|---|---|---|
| 1.3 Cómo registrar un tercero | El detalle del tercero tiene el botón «Bloquear salidas» / «Desbloquear salidas» (con motivo de 10 a 500 caracteres) y la etiqueta «Salidas bloqueadas» con motivo, fecha y autor. Lo ven Administración, Comercio Exterior y Facturación. La lista tiene el filtro «Salidas bloqueadas» | Fase 3, DEC-052 |
| 1.13 Auditoría y parámetros del sistema | Parámetro nuevo `GUIDE_CODE_TYPE` (`QR` o `BARCODE`, valor inicial `QR`), que solo edita el Admin; cualquier otro valor da error | Fase 11, DEC-060 |
| 2.2 y 2.8 Acuerdos: crear, activar y editar | El convenio «Programado» exige la fecha de activación (sin hora, sin «(Opcional)») y se activa solo a las 00:00 de ese día, archivando al activo del cliente; Facturación recibe el aviso | Fase 7, D20 |
| 2.10 Convenio de montacargas y servicio complementario | Un servicio complementario sin tarifa ya no impide confirmar el depósito: la línea sale en $0 (o con el mínimo del propio servicio) con advertencia en la factura | Fase 6, D17 |
| 3.5 La factura de almacenamiento y los depósitos pendientes | «Depósitos pendientes» tiene la columna «Pendiente» («Por numerar» / «Por refacturar») y el interruptor «Solo con facturas por numerar o refacturar»; las renovaciones cobran el saldo al inicio del período | Fases 6 y 7, DEC-053 |
| 5.2 Solo báscula de principio a fin | El cliente es opcional («Cliente (opcional)»: sin cliente, el cobro va al conductor o al consumidor final); el tiquete y el historial muestran al destinatario | Fase 4, DEC-050 |
| 5.5 Primer peso, llegada a Bodega, segundo peso y tiquete | El pie del tiquete dice «Documento interno de control de pesaje. No es una factura de venta.» (ya no menciona la DIAN) | Fase 1, D4 |
| 5.8 Multidepósito: agregar otro depósito | Con varios documentos el operario elige el segundo pesaje: «Tara — un solo pesaje para todos los depósitos» (predeterminado, neto repartido por el peso de manifiesto) o «Intermedio — el camión descarga en otro punto». Un tiquete por depósito, con «Pesaje compartido por N depósitos». Se imprimen todos los tiquetes | Fase 5, DEC-050 |
| 5.11 Historial de báscula: corregir, anular y reimprimir | La corrección de un pesaje que no es el primero actúa sobre el pesaje elegido y recalcula el neto de las entradas afectadas | Fase 4 |
| 6.6 Cómo ejecutar una orden de cargue | Bodega no puede cargar con un dueño marcado «sin salidas»; si lo cargado difiere de la guía vigente, Comercio Exterior recibe el aviso y el mensaje de resultado lo dice | Fase 3, DEC-052 |
| 7.10 y 7.11 Crear, modificar, cancelar y revertir una orden de cargue | Con una guía vigente, «Cancelar orden» y «Modificar ítems» quedan deshabilitados («anule primero la guía»); también en Bodega. La marca «sin salidas» impide crear la orden | Fases 2 y 3, D6, D9 |
| 7.12 y 7.13 Guía de salida, guías pendientes e historial | El PDF trae un código QR con «Escanee para verificar esta guía» (o el código de barras, según el parámetro) y se verifica en una página pública. El historial marca «No coincide con lo cargado» cuando el cargue difiere de la guía | Fases 3 y 11 |
| 7.15 Reportes de Comercio Exterior | «Mercancías ingresadas (diario)» es nuevo: filtro de modalidad, un bloque por depósito con agencia, importador y manifiesto DIAN, una fila por camión, total de vehículos y firmas; con PDF y «Exportar Excel». «Salida de mercancía (diario)» tiene «Exportar Excel». El kárdex y los listados usan la fecha de ingreso del depósito | Fase 8, DEC-054 |

**Video nuevo sugerido:** «Verificar una guía con el celular» (página pública `/verificar/guia/…`), para Comercio Exterior y para quien recibe la guía en papel.

**Guía de operarios** (`planes/migracion-staging/resultados/guia-pruebas-operarios.md`): se anotan los mismos puntos en su §12, para que rijan desde el despliegue de la fase 13.

## 8. Terminología de `DEC-029` en los guiones (2026-10-25)

> **Origen:** `planes/plan-cerrado-dec-029-fob-cif-2026-10-25.md` (D1–D5, D8), fase 3. Código de referencia: Backend `dafd573` / Frontend `d838535`. Los videos publicados que quedan desactualizados están en `videos/videos-desactualizados-dec-029.md`; se regraban en una tarea aparte.

| Guiones | Qué cambió en el guion | Plan DEC-029 |
|---|---|---|
| 1.7, 2.2, 2.4, 2.5, 2.7, 2.9, 3.3, 3.5, 7.2, 7.7 y 7.15 (y S4 y A1 de `dataset-grabacion.md`) | El levante se rotula CIF («CIF del levante (USD)», «Valor CIF de los levantes (USD)…»). El valor del depósito es «Valor de la mercancía» (antes «Valor Comercial», «Valor mercancía» o «Valor de la mercancía (CIF)»). La fórmula de lote completo es «Porcentaje del valor de la mercancía (lote completo)» y el umbral, «Umbral del valor de la mercancía por encima del cual no se aplica el mínimo ($)». Las narraciones ya no llaman CIF al valor del depósito | D1–D4, D8 |
