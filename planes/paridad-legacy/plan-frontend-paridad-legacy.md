# Plan cerrado de frontend — paridad con Bodegas legacy (wms)

**Fecha:** 2026-10-01. **Repositorio:** `code_workspace/Frontend/wms`. **Rama de trabajo:** `develop` (`26aed68`), la única: no se crean ramas ni PR. **Los commits los hace el usuario;** el implementador se detiene al terminar cada ítem (§E).
**Backend:** `code_workspace/Backend/wms-api`, rama `develop` en `bf64de1`: las seis fases de backend del plan de paridad ya están implementadas (§D).
**Contrato de API:** `code_workspace/docs/planes/paridad-legacy/contrato-api-paridad.md` (identificadores `C-Fx-yy`). Este plan copia de ahí todo lo que el implementador necesita: no hace falta abrirlo, salvo para auditar.
**Decisiones:** cerradas con el usuario el 2026-10-01 (§A.4). No hay supuestos abiertos.

---

## A. Resumen ejecutivo

### A.1 Qué se construye

La empresa reemplaza el sistema legacy «Bodegas» (PHP) por el WMS v2. El análisis comparó ambos sistemas tarea por tarea del operario, el negocio decidió qué construir y el backend ya está hecho. Este plan es la parte de interfaz: lo que el operario ve y toca.

| Fase | Tema | Qué gana el operario | Dificultad | Estado |
|---|---|---|---|---|
| 1 | Báscula al ritmo del legacy | Registra un camión de importación solo con lo que tiene a mano. La mercancía se digita en línea, con descripción libre. El cobro, con efectivo y cambio, y el peso quedan en la misma ficha, sin modales y con el teclado. Comercio Exterior completa y confirma lo que báscula dejó pendiente. | **Muy alta** | ✅ Completada en código (2026-10-01; commit `12c79c8`). Pendiente F1-09. |
| 2 | Control aduanero | No puede despachar más de lo nacionalizado. Retira levantes y registra su FOB. Ve los depósitos que se acercan al abandono, registra la prórroga y saca los reportes. Elige la ciudad de destino de un catálogo, y el vencimiento de la guía se calcula solo. | Alta | ✅ Completada en código (2026-10-01; commit `5c7ecba`). Lint 306 (tope 310). |
| 3 | Correcciones y facturación | Anula un pesaje completo, modifica, cancela o revierte una salida, anula una guía o un depósito con motivo, refactura una factura anulada y configura los ciclos legacy (15, 30, 90, 180 y 360 días). | Alta | ✅ Completada en código (2026-10-01; commit `57f3371`). Lint 301 (tope 306). |
| 4 | Bodega y mercancía | Ubica, mueve y libera mercancía por cantidades. Registra novedades con desglose y las imprime. Carga listas de empaque. Usa cuadrillas. En báscula, saca otras órdenes con el mismo pesaje o una salida con el tiquete de ingreso. | **Muy alta** | ✅ Completada en código (2026-10-02; commit `aed2ab1`). Lint 300 (tope 301). |
| 5 | Reportes y consultas | Saca en Excel los mismos informes del legacy: kardex con levantes, inventario general, pólizas, ingresos por producto, facturación anual y por CPI, báscula por modalidad y agencias de aduana. Ve las columnas de saldo y busca por placa y por levante. | Media | ✅ Completada en código (2026-10-02; commit `e7c8400`). Lint 296 (tope 300). |
| 6 | Migración y corte | Sin desarrollo de frontend (decisión DF3). Solo una verificación de la interfaz con los datos migrados. | — | ✅ Sin código (DF3), revisada 2026-10-02. Pendiente: verificación con datos migrados por el usuario. |
| 7 | Comodidad (P3, opcional) | Conteo de impresiones de etiquetas, «Terceros» en lugar de «Stakeholders» con accesos por rol, y atajos de teclado globales. | Media | ✅ Completada en código (2026-10-02; sin commit). Lint 296 (igual al tope de la fase 6). |

**La fase 1 es la prioridad del proyecto.** El formulario de báscula es la puerta de entrada y el punto de congestión: los camiones hacen fila. Su criterio de salida es una medición con el operario (F1-09).

### A.2 Orden

1 → 2 → 3 → 4 → 5 → (6 sin código) → 7 opcional, todo en `develop`. Dentro de cada fase, un ítem a la vez, en el orden de §E: el implementador termina el ítem, se detiene y entrega su resumen (§E.2); el usuario hace el commit con el mensaje sugerido y solo entonces sigue el ítem siguiente. Una fase empieza cuando la anterior tiene todos sus ítems con commit (§F).

### A.3 Qué queda fuera y por qué

- **Colmotores** (cliente/importador 70): VIN, seriales, voltajes, patio externo, lecturas y averías de vehículo. Está inhabilitado y no se migra. Ejemplo: el radio «¿Vehículos Colmotores?» del formulario legacy no se replica.
- **Acceso, autenticación y roles.** Son funcionalidad nueva de la v2. Ningún ítem cambia `requiredRoles` de páginas existentes ni las políticas del backend. Las páginas nuevas usan los roles de la política de su endpoint.
- **Ítems retirados por decisión del negocio (2026-09-29):**
  - precarga de cliente y tarifa por placa;
  - salida en portería por número de guía;
  - soportes documentales por depósito, levante y salida;
  - captura automática del peso (el peso se digita en ambos sistemas);
  - administración de los catálogos hoy fijos (documentos comerciales, modalidades, naturaleza, tipos de bodega, tipos de identificación);
  - datos de maestros del legacy: representantes con porcentaje, marca, línea, clase y carrocería del vehículo, fotos.
- **Fase 6 sin pantallas** (DF3): la carga de datos legacy, la conciliación, la apertura de facturación de migrados y los respaldos se operan por API.
- **UI-22** (cobros pendientes visibles para báscula): exige que el rol `Scale` lea facturas, que es un cambio de política. Queda fuera por la regla de acceso.
- **Pantallas congeladas:** `pages/billing/invoices/create.vue`, `BillingPreviewPanel.vue` y la consulta `GetStorageInvoiceDraft` no se reviven. La refacturación (F3-08) usa su propio endpoint.
- **Endpoint `GET weighbridge/lookup`** (precarga por placa, `useWeighbridgeLookup.ts`): existe y no se usa. No se conecta, porque precargaría cliente y tarifa, que es un ítem retirado.

### A.4 Decisiones cerradas

Del usuario, el 2026-10-01:

| # | Tema | Decisión |
|---|---|---|
| DF1 | Dónde se implementa y se prueba | En local, sobre `develop`, sin ramas ni PR. El usuario levanta el backend local y hace los commits; el implementador no ejecuta `git add`, `commit`, `push`, `merge` ni crea ramas. |
| DF2 | Fin del cronómetro de la fase 1 | En el **primer peso registrado con el camión liberado**. El repesaje con la impresión del tiquete se cronometra aparte, sin meta frente al legacy (F1-09). |
| DF3 | Pantallas de la fase 6 | No se hacen. El corte se opera por API. |
| DF4 | FOB de un levante con varios productos | Se digita **una vez por levante**: en el primer producto. Al registrar otro producto con el mismo levante, el FOB arranca vacío con aviso (F2-06). |

Del arquitecto. Cada una se justifica en su ítem:

| # | Decisión | Ítem |
|---|---|---|
| DF5 | El cobro y el peso son **pasos en línea de la misma ficha**: registro → cobro → peso, cada uno con Enter. El modal de cobro desaparece. El modal de peso (F2) queda como alternativa. Es la cadencia del legacy («Insertar registro» → efectivo → imprimir), cada paso se recupera solo si falla y reutiliza `BillingCollectForm` y `WeightCapture`. | F1-05 |
| DF6 | Se retira el modal «Confirmar creación de depósito». Lo reemplaza un aviso en línea, visible antes de guardar: «Documento nuevo: al guardar se crea un depósito» o «Se asociará al depósito 2026BA00012». | F1-06 |
| DF7 | Se retira el botón «Validar documento». El documento se busca al salir del campo «Nro. documento». | F1-01 |
| DF8 | El tipo de operación y la modalidad se preseleccionan por el **motivo de ingreso** que registró Vigilancia (IDs sembrados). El operario puede cambiarlos. | F1-06 |
| DF9 | Destinatario del cobro por defecto: el cliente, si la operación lo tiene; si no, el conductor del vehículo. Es lo que hacía el legacy (`registrarentradabascula.php:151-160`). | F1-05 |
| DF10 | La moneda solo se envía desde báscula si se digitó el valor de la mercancía. Así no se envía «COP» por defecto en un depósito en dólares. | F1-01 |
| DF11 | En báscula, los datos que completa Comercio Exterior van en un panel plegado: fecha del documento, cliente, importador, agencia de aduanas, exportador, valor y moneda. El número y el peso del manifiesto quedan visibles y opcionales, como en el legacy. | F1-01 |
| DF12 | El Excel lo arma el frontend con `exceljs`, cargado con `import()` dinámico, desde una utilidad común. Siempre con `all=true`. | F5-01 |
| DF13 | Fases e ítems en secuencia sobre `develop`: un ítem empieza cuando el anterior tiene commit y una fase cuando la anterior está completa. Todas tocan los mismos servicios y las páginas de detalle del depósito, así que no se trabajan en paralelo. | §F |
| DF14 | **GAP-011** (anular depósito) entra en la fase 3, aunque no está en la tabla UI-xx. El contrato volvió obligatorio el motivo y la pantalla actual lo envía vacío. | F3-06 |
| DF15 | El selector «Tipo de carga» (mercancía suelta o unidades de carga) se agrega en báscula. Su lógica existe pero nunca se pintó, y BAS-07 lo necesita. | F1-03 |
| DF16 | En una línea de mercancía con descripción libre, la unidad de medida es obligatoria. En una línea del catálogo, la unidad viene del producto (regla WMS-18 vigente). | F1-02 |
| DF17 | El «Camión» de una novedad se elige entre las recepciones del depósito: es la lista de camiones a la que Bodega tiene acceso. | F4-03 |
| DF18 | Comercio Exterior hace la «salida con tiquete de ingreso» desde el historial de pesaje del detalle del depósito, eligiendo la orden del mismo vehículo. | F4-06 |

### A.5 Lo que la v2 ya hace mejor y no se puede perder

El implementador verifica cada punto en la prueba manual de cada ítem que lo toca. Si un cambio rompe uno, el ítem no está terminado.

| Ganancia de la v2 | Dónde vive | Ítems que la tocan | Cómo se protege |
|---|---|---|---|---|
| Cola de camiones con estado y filtro `?cola=` | `TruckQueue.vue`, `useWeighbridgeQueue.ts` (refresco cada 15 s) | F1-05, F1-06, F4-05, F4-06 | No se cambia la consulta ni el filtro. Toda mutación de báscula invalida `['weighbridge']`. |
| Una sola pantalla sin «Continuar» | `pages/operations/weighbridge/index.vue` | F1-01 a F1-06 | Se eliminan modales: no se agregan pasos ni pantallas. |
| Memoria del turno | `useEntryFormMemory.ts`: modalidad, tipo de documento, moneda, perecedero, transportadora y países | F1-01, F1-06 | Se conservan las mismas claves y la regla de llenar solo campos vacíos. El motivo de ingreso tiene prioridad sobre la memoria solo en la modalidad. |
| Borradores por camión | `index.vue:178-247` (`drafts`, `KeepAlive`) y aviso al salir (`:827-840`) | F1-05 | Los pasos en línea se guardan en el borrador del camión. |
| Panel de camiones previos | `PreviousEntriesPanel.vue` | F1-02 | Se muestra encima de las líneas de mercancía cuando el documento ya existe. |
| Neto calculado en el servidor | `RecordWeighing` | F1-05 | El frontend no calcula pesos. |
| Validación de mora antes de cobrar | Backend, en el `process-payment` | F1-04, F1-05 | El cobro muestra el error del backend y la ficha se queda en el paso de cobro. |
| Recuperar operaciones a medias | `pages/operations/weighbridge/recover.vue` y `index.vue:842-890` | F1-05 | Retomar abre la ficha en el paso pendiente (cobro o peso), sin modal. |
| Atajos F2, Enter y Esc | `index.vue:799-824` | F1-05, F1-06 | F2 sigue abriendo el peso en ventana. Enter ejecuta la acción del paso actual. Esc cierra la ventana de peso. |
| Alta rápida de tercero y transportadora | `QuickCreateStakeholderDialog.vue`, `CompleteEntryInfo.vue` | F1-01 | Se conserva el botón «+» en importador, agencia y exportador. |
| Fecha de ingreso editable (WMS-33) | `StorageServiceForm.vue:246-259,1126-1144` y `WeightCapture.vue:143-161` | F1-01, F1-05 | Se conserva: fecha propuesta = la de Vigilancia, con mínimo y máximo. |
| Depósito adicional en el mismo camión y flujo perecedero | `index.vue:693-761`, `WeightCapture.vue` | F1-05 | El paso de cobro del depósito adicional es la confirmación en $0, en línea. |
| Pendiente por facturar y conductor como destinatario | `BillingCollectForm.vue`, `PaymentModeSelector.vue` | F1-04, F1-05 | Se conservan. El efectivo y el cambio solo aparecen con pago inmediato en efectivo. |

---

## B. Contexto mínimo para el implementador

### B.1 El negocio en media página

Bodegas Asociadas opera un **depósito público aduanero** en Ipiales, junto al paso de Rumichaca con Ecuador. La mercancía que cruza la frontera se queda ahí mientras la DIAN la nacionaliza, la exporta o la inspecciona. La bodega cobra **báscula**, **montacargas** y **guía de salida** de contado (o pendientes de facturar) y el **almacenamiento** a crédito, por períodos. La factura legal se emite en SIIGO: el WMS calcula el valor y Facturación copia el número.

Flujo de una importación en la v2:

1. **Vigilancia** registra el ingreso del camión: placa, motivo y conductor. El camión entra a la **cola de báscula**.
2. **Báscula** toma el camión de la cola, registra el documento (carta porte) y la mercancía que trae, **cobra** y **pesa**. El primer camión de un documento crea el **depósito** en Borrador. Los siguientes camiones del mismo documento se asocian a ese depósito.
3. **Comercio Exterior** completa el depósito (fecha del documento, importador, agencia de aduanas, valor, moneda, manifiesto de cada camión), lo **confirma**, imprime la etiqueta y registra los **levantes**.
4. **Bodega** recibe la mercancía, la ubica y registra novedades.
5. Para sacarla, Comercio Exterior crea una **orden de cargue**. Bodega la carga, Comercio Exterior emite la **guía de salida** y báscula pesa la salida. Vigilancia registra la salida del camión.

### B.2 Glosario

| Término | Qué es | En el código |
|---|---|---|
| Depósito | Lote de mercancía amparado por un documento y una modalidad (importación, exportación o inspección). Es la unidad de inventario, de etiqueta y de cobro de almacenamiento. Número `2026BA00012`. | `WarehouseStorage` |
| Carta porte | Documento de transporte internacional que ampara la carga. Con su tipo y su modalidad identifica el depósito. En pantalla: «Nro. documento». | `cargoManifestNumber` (el nombre engaña: es la carta porte) |
| Manifiesto del camión | Número y peso bruto que declara el manifiesto de carga de cada camión. | `manifestNumber`, `manifestWeight` |
| Manifiesto DIAN | Número y fecha del manifiesto aduanero del depósito de importación. Lo registra Comercio Exterior. | `ImportWarehouseStorage.manifestNumber` |
| Levante | Autorización de la DIAN para disponer de la mercancía importada. En la v2 se registra por producto: un levante con tres productos son tres registros con el mismo número. | `ImportRelease` |
| Nacionalización | La mercancía con levante está nacionalizada. Solo lo nacionalizado se puede despachar. | suma de levantes por producto |
| Orden de cargue (OC) | Autorización de Comercio Exterior para sacar mercancía de uno o varios depósitos. Reserva stock. | `LoadingOrder` |
| Guía de salida | Documento que acompaña la salida; congela los saldos y se cobra. | `DispatchGuide` |
| Tiquete | Comprobante del pesaje que se entrega al conductor. En ingresos con depósito el número se asigna al completar el ciclo (segundo peso). | `WeighbridgeCycle`, `ticketNumber` |
| Ciclo de báscula | Pesajes de un camión: primer peso (bruto o tara), segundo peso y neto. | `WeighbridgeCycle` |
| Prórroga | Extensión del plazo aduanero. Sin prórroga el depósito cae en abandono a los 30 días; con prórroga, a los 60. Es irreversible. | `extensionRegisteredAt` |
| Abandono | Mercancía sin nacionalizar que venció su plazo. Alerta: de 20 a 30 días sin prórroga, o de 50 a 60 con prórroga. | `foreign-trade/abandonment` |
| Unidad de carga | Contenedor, tanquero o remolque que entra con el camión, con su placa. | `WarehouseStorageCargoUnit` |
| Agencia de aduanas = SIA = intermediario | Un solo rol de negocio, código `CUSTOMS_AGENCY`. En pantalla: «Agencia de aduanas (SIA)». | `CUSTOMS_AGENCY` |
| Modalidad | Importación (`IMP`), Exportación (`EXP`), Dep. Inspección (`INSP`). «Solo báscula» no crea depósito. | `OperationModality` |
| Cuadrilla | Grupo de coteros que descarga o carga. | `Crew` |
| FOB | Valor de la mercancía del levante en dólares, convertido a pesos con la TRM del día. | `fobUsd`, `fobCop` |

### B.3 Roles de operario

| Código | Nombre en la UI | Qué hace | Módulo |
|---|---|---|---|---|
| `Receiving` | Operario vigilancia | Registra ingreso y salida de vehículos. | `/operations/entries` |
| `Scale` | Operario báscula | Toma el camión de la cola, registra documento y mercancía, cobra, pesa e imprime el tiquete. Por decisión del 2026-09-29 también tiene el rol de Vigilancia. | `/operations/weighbridge` |
| `Warehouse` | Operario bodega | Recepción, ubicaciones, novedades, montacargas, cargue e inventario. | `/warehouse` |
| `ForeignTrade` | Comercio exterior | Dueño del depósito: lo completa y confirma, registra levantes y prórrogas, crea órdenes y guías, saca reportes. | `/foreign-trade`, `/reports` |
| `Billing` | Facturación | Facturas, N.º SIIGO, pagos, ciclos de facturación, refacturación. | `/billing` |
| `Admin` | Administrador | Todo, más los catálogos. | `/admin` |

Cada página declara `definePageMeta({ requiredRoles: [...] })`. El menú está en `app/components/layout/AppMenu.vue` y se filtra por `roles`.

### B.4 Arquitectura y convenciones obligatorias

**Stack.** Nuxt 4 como SPA (`ssr: false`), Vue 3.5 con `<script setup lang="ts">`, PrimeVue 4 (componentes auto-importados), `@primevue/forms` con `zod`, Pinia 3, TanStack Vue Query 5, VueUse, Tailwind 3. Las rutas están en `app/pages`; la lógica por dominio, en `app/features/<dominio>/{components,composables,services,types,utils}`.

**Patrones existentes que se copian:**

| Necesidad | Copiar de |
|---|---|
| Servicio HTTP | `features/foreign-trade/services/foreign-trade-service.ts`: `const api = useApi()`, `api.get<Q,R>(ruta, query)` devuelve `{ data, pagination }`; `api.getBlob(ruta)` para PDF. |
| Consulta | `features/billing/composables/useStoragePeriods.ts`: `useApiQuery({ queryKey: computed(() => ['billing', 'storage-periods', params.value]), queryFn })`. |
| Mutación con invalidación | `features/weighbridge/composables/useRegisterStorageEntry.ts`: `useApiMutation({ mutationFn, onSuccess: () => queryClient.invalidateQueries({ queryKey: ['weighbridge'] }) })`. |
| Catálogo administrable (tabla + diálogo de crear y editar) | `pages/admin/packaging-types/index.vue` y `features/administration/composables/useMutationsPackagingTypes.ts`. |
| Reporte con filtros y PDF | `pages/reports/warehouse-movements.vue`. |
| Formulario con validación | `features/weighbridge/components/WeightCapture.vue` (`Form` + `zodResolver`). |
| Confirmación | `useAppConfirm().request({ summary, message, acceptText, accept })`. |
| Avisos | `useWmsToast()`: `showSuccess(título, detalle)`, `showError`, `showWarning`. |
| Fechas en hora de Colombia | `app/utils/colombia-date.ts`: `formatColombiaDateTime`, `toColombiaOffsetIso`, `toColombiaPickerDate`, `nowColombiaPickerDate`. |
| Placas | `app/utils/plate.ts`: `normalizePlate`, `isValidPlate`. |

**Convenciones** (se repiten en cada ítem donde aplican):

1. **Todo el texto visible en español** y con el vocabulario del negocio («depósito», «carta porte», «agencia de aduanas», «levante»). Nunca nombres del modelo de datos frente al operario (`warehouseStorage`, `CUSTOMS_AGENCY`, `Draft`). Los estados se traducen: Borrador, Confirmado, Cerrado, Anulado.
2. **`usePermissions` se importa de forma explícita:** `import { usePermissions, ROLES } from '~/composables/usePermissions'`. No por auto-import.
3. **Tras cada mutación se invalida el prefijo de la consulta.** Las claves nuevas empiezan siempre por uno de estos prefijos: `['weighbridge', …]`, `['foreign-trade', …]`, `['warehouse', …]`, `['billing', …]`, `['administration', …]`, `['reports', …]`. Hay claves heredadas que no siguen la regla (`'weighbridgeHistory'`, `'weighbridge-history'`, `'weighbridge-pending'`, `'warehouse-loading-orders'`, `'warehouse-inventory-movements'`…): cada ítem dice cuáles invalida además del prefijo.
4. **Búsquedas con `watchDebounced`** de VueUse (300 ms), o `refDebounced` como término reactivo de la consulta. Nunca una consulta por tecla.
5. **Paginación:** el backend recorta `pageSize` a 50. Para traer todo (selects, Excel) se envía `all=true`. **Nunca** se sube `pageSize` para esquivar el tope: es el origen del defecto de la exportación de importaciones (`useExportImportsToExcel.ts:17`, `pageSize: 10000`).
6. **Errores del API.** El interceptor (`plugins/api-client.ts:84-150`) ya muestra un aviso global con el mensaje del backend (`app.vue:53-70`) y **rechaza la promesa con el cuerpo del error** (`IApiError`: `status`, `description`, `errors[]`), no con un error de axios. En un `catch`:
   - lea `(e as IApiError).status` y `(e as IApiError).description`;
   - **no** lea `error.response.data` (siempre es `undefined`; varias pantallas lo hacen y muestran un texto genérico);
   - no muestre un segundo aviso con el mismo texto: el global ya salió. Muestre el error en línea (debajo del campo o en un `Message`) solo cuando el ítem lo pide.
7. **Antes de rehacer una pantalla**, compruebe que una ronda anterior no la haya retirado a propósito. Ejemplo real: `pages/billing/invoices/create.vue` está congelada y no se revive.
8. **Verifique el componente y también quién lo instancia:** las props declaradas no dicen qué le pasa el padre. Cada ítem dice qué padre cambia.
9. **Reutilice antes de crear.** Ejemplo: la lógica de efectivo y cambio ya está en `features/weighbridge/components/PaymentForm.vue:178-185,263-266` y ninguna pantalla usa ese componente (F1-04 la extrae).
10. **Motivos:** donde el contrato pide `reason`, el campo es un `Textarea` de 3 filas con contador «{n} / 500 (mínimo 10)», y el botón de enviar queda deshabilitado mientras el texto recortado tenga menos de 10 caracteres. Mensaje bajo el campo: «El motivo debe tener entre 10 y 500 caracteres.»
11. **Dinero** en pesos con `toLocaleString('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 })`; cantidades con `useQuantityFormatter()`; fechas con `formatColombiaDateTime` o `dd/MM/yyyy`.
12. **Abrir en el navegador** lo que cambió, con el backend corriendo, antes de dar un ítem por terminado (§B.5).

### B.5 Cómo se prueba (DF1)

- **Backend local:** el usuario lo levanta desde `Backend/wms-api` en `develop` (`bf64de1` o posterior), con las migraciones de paridad aplicadas (§D.2). API en `http://localhost:5281/api/v1`.
- **Frontend:** `.env` con `NUXT_PUBLIC_API_BASE=http://localhost:5281/api/v1` y `yarn dev`.
- **Usuarios de prueba por rol:** los del `README.md` del frontend. No se copian contraseñas a otros documentos.
- **Navegador:** cada prueba manual se hace en el navegador con el rol indicado. Si una prueba necesita datos (un depósito confirmado, un levante), el paso 0 de la prueba dice cómo crearlos desde la interfaz.
- **El implementador no da un ítem por terminado sin haber visto la pantalla funcionando contra el backend.** Si el endpoint responde distinto al contrato, se detiene y lo reporta. No simula la respuesta.

### B.6 Compilación y lint: cada fase se valida sola

La línea base de `develop` (`26aed68`) compila y tiene **322 errores y 394 advertencias de lint** que ya existían. No se arreglan en este plan, salvo en las líneas que un ítem reescribe. Al cerrar cada fase:

1. `yarn build` termina con código 0.
2. `npx eslint app --format json -o /tmp/eslint-fase.json` y luego `node -e "const r=require('/tmp/eslint-fase.json');console.log(r.reduce((a,f)=>a+f.errorCount,0))"`: el total de errores **no supera** el de `develop` al empezar la fase. Para la fase 1 es 322; el implementador anota en el resumen de cierre de cada fase (§E.2) el número con que cierra, y la fase siguiente lo usa como tope.
3. `npx eslint <archivos nuevos de la fase>`: **cero** errores en los archivos nuevos.

No hay `vue-tsc` instalado: no se exige `nuxi typecheck`.

### B.7 Escala de dificultad

| Nivel | Cuándo | Perfil de agente |
|---|---|---|
| **Baja** | Cambios de texto, etiquetas, columnas o filtros en una pantalla existente. Sin cambios de contrato ni de flujo. | Agente económico, sin supervisión |
| **Media** | Pantalla nueva o formulario nuevo con un contrato ya definido, varios componentes y su composable y servicio. | Agente estándar |
| **Alta** | Rediseño de un formulario existente con muchos campos y validaciones, cambios en el orden del flujo, o una pantalla con estados y efectos encadenados. | Agente capaz, con revisión humana del diff y prueba en el navegador |
| **Muy alta** | El banco de trabajo de báscula y cualquier cambio que pueda romper la cola, la memoria del turno o el cobro. Se mide con el operario antes de darlo por bueno. | Agente capaz, revisión humana y medición con el operario |

### B.8 Cómo leer cada ítem

Cada ítem trae, en este orden: **identificador** (`Fx-yy` del plan y `UI-xx`, `BAS-xx`, `GAP-xxx` del análisis), **dificultad**, **tarea del operario** y **cómo la hacía en el legacy**, **evidencia** (PHP legacy y v2 con líneas, solo para auditar), **pantallas y componentes** (`(nuevo)` o `(modifica)`), **diseño de la interacción** (campos con etiqueta, control, obligatoriedad, validación y mensaje; tabulación y foco; estados; qué pasa al guardar), **endpoints** (del contrato, con su forma), **roles y menú**, **invalidación**, **pruebas manuales**, **terminado cuando** y **riesgo**.

En las tablas de campos, «Obligatorio = Sí» quiere decir que el frontend no deja enviar sin el dato y muestra el mensaje bajo el campo. Los mensajes van tal cual.

---
## C. Fases

### C.1 Fase 1 — Báscula al ritmo del legacy

> **Estado: ✅ COMPLETADA en código (2026-10-01).** F1-01 a F1-08 implementados en `develop` (sin commit: lo hace el usuario). `npm run build` OK. Lint al cerrar la fase: **310 errores** (tope 322) y 0 errores en los archivos nuevos; la fase 2 usa 310 como tope. Pendiente fuera del código: pruebas manuales en el navegador contra el backend local y **F1-09** (medición con el operario), que habilita la fase 2 (§E.1, regla 5).

- **Objetivo:** el operario de báscula registra un camión de importación solo con lo que tiene a mano, de arriba a abajo con el teclado, sin modales, y Comercio Exterior completa y confirma lo que quedó pendiente.
- **Criterio de salida (verificable, desde el operario):**
  1. Con el operario presente y el guion de F1-09, la **mediana** de tres registros de un camión de importación nuevo, desde que lo toma de la cola hasta el primer peso registrado con el camión liberado, es **igual o menor** que la mediana del legacy, de «Nueva Entrada» a tiquete impreso.
  2. Lo mismo para el segundo camión de un mismo documento.
  3. El operario no digita en báscula ningún dato que no tenga a mano: fecha del documento, importador, agencia de aduanas, exportador, valor y moneda quedan opcionales y plegados.
  4. Comercio Exterior ve en el detalle del depósito qué falta para confirmar, lo completa y confirma.
  5. Siguen funcionando la cola, la memoria del turno, el panel de camiones previos, la validación de mora, recuperar operaciones y los atajos (§A.5).
- **Rama:** `develop` (DF1). **Empieza** tras el paso 0 de §E.3 (migraciones aplicadas y backend local corriendo).
- **Backend que debe estar corriendo:** `develop` con el commit `1898052` (fase 1 de backend) y `7c83b77`, con las migraciones `ParidadF1_02_IndiceDocumento`, `ParidadF1_06_ProductoDesdeBascula` y `ParidadF1_09_EfectivoYCambio` aplicadas (§D).
- **Dificultad:** **Muy alta.** Rediseña el banco de trabajo de báscula: el formulario de ingreso, la cola de pasos (registro, cobro y peso) y el cobro. Un error deja camiones en fila.
- **Perfil de agente:** agente capaz, revisión humana del diff, prueba en el navegador y medición con el operario (F1-09).
- **Archivos que toca la fase (resumen):** `pages/operations/weighbridge/index.vue`, `features/weighbridge/components/{StorageServiceForm,CargoUnitsEditor,WeightCapture,PaymentForm}.vue`, `features/billing/components/BillingCollectForm.vue`, tipos y servicio de báscula, páginas de detalle de importación, exportación e inspección, componentes de detalle del depósito, `pages/admin/products/index.vue`. Componentes nuevos listados en cada ítem.

---

#### F1-01 · Báscula registra el camión solo con lo que tiene a mano (BAS-01, UI-01)

- **Dificultad:** Alta.
- **Tarea del operario:** registrar el documento del camión que está en la romana, sin datos que solo llegan después con la documentación que revisa Comercio Exterior.
- **Cómo lo hacía en el legacy** (`registrarentradabascula.php`, una pantalla, botón «Insertar registro»), en este orden:
  1. Fecha y hora, prellenada y editable (`:735`).
  2. Lectura de la báscula y botón «Capturar» (`:741-742`), sin uso en la operación: el peso se digita.
  3. **Vehículo:** Placa (obligatoria, autocompleta y carga país, conductor y transportadora del último pesaje, `:750-755`, `:322-363`); País (`:757-763`); Conductor (diálogo de búsqueda, obligatorio, `:766-772`); Emp. Transporte (diálogo, `:775-778`).
  4. **Modalidad:** radio Importación (marcada por defecto), Exportación u Otra (`:789-799`); Doc. Comercial (select obligatorio, `:802-819`); Nro. Documento (obligatorio, autocompleta con los ingresos existentes de ese tipo y número y, al elegir uno, salta al manifiesto, `:822-829`, `:520-557`); Manifiesto PreImp. (opcional, `:832-834`).
  5. **Pesaje (Kg):** P. Indicador (peso bruto, obligatorio); T. vehículo (calculado = bruto − mercancía); P. manifiesto (opcional, se copia a P. mercancía); P. mercancía (`:840-862`, `:643-651`, `:855`).
  6. **Mercancía:** descripción del producto (texto libre en mayúsculas, máx. 200, obligatorio), embalaje (texto, máx. 100, obligatorio) y cantidad (obligatoria), **una sola línea** (`:884-900`).
  7. Panel derecho: convenio, tarifa, «Facturar a» y otros servicios, que se cargan solos desde la placa (`:913-919`). Fuera de alcance por decisión.
  8. «Insertar registro» (`:906`) crea el ingreso en estado `incompleto` con solo modalidad, fecha, documento, número y transportadora (`:76-77`), y abre el cobro (`:196`).
  9. Comercio Exterior completaba **después**, en `modulos/mod_ingresos/modificaringreso.php:88-106,311-494`: fecha del documento, manifiesto DIAN y su fecha, agencia de aduanas (SIA), importador, exportador, pesos, precio de la mercancía y su moneda.
- **Lo que hace hoy la v2** y hay que cambiar:
  - el esquema exige fecha del documento, importador y agencia en importación, número y peso del manifiesto, valor y moneda (`features/weighbridge/components/StorageServiceForm.vue:369-409`);
  - el botón «Validar documento» exige la fecha antes de buscar (`:952-967`, `:1147-1172`), y los demás campos solo aparecen después de validar (`:1183-1245`);
  - la búsqueda del documento no maneja errores (`pages/operations/weighbridge/index.vue:524-590`, sin `try/catch`);
  - el aviso al guardar no dice el número del depósito (`index.vue:405-409`);
  - los tipos exigen `manifestWeight: number` (`features/weighbridge/types/requests.ts:95`) y la respuesta no tiene `warehouseStorageNumber` ni `createdProducts` (`types/weighbridge-cycle.ts:230-247`).
- **Evidencia legacy:** citada arriba. **Evidencia v2:** citada arriba.
- **Pantallas y componentes:**
  - `app/features/weighbridge/components/StorageServiceForm.vue` (modifica): esquema, sección «Documento», panel de datos opcionales, búsqueda automática, mapeo del envío.
  - `app/features/weighbridge/components/DocumentMatchBanner.vue` (nuevo): aviso del resultado de la búsqueda del documento.
  - `app/pages/operations/weighbridge/index.vue` (modifica): `handleSearchCargoManifest` con manejo de 409 y error, `handleStorageSubmit` con número del depósito.
  - `app/features/weighbridge/types/requests.ts` y `types/weighbridge-cycle.ts` (modifica).
  - `app/features/weighbridge/composables/useStorageWeighing.ts` (modifica: invalida `['weighbridge']` al terminar).
- **Diseño de la interacción.** La ficha de «Ingresos» deja de tener secciones numeradas que aparecen tras validar. Todo está visible desde el principio, en este orden:

  **Sección «Documento»**

  | # | Etiqueta | Control | Obligatorio | Validación y mensaje |
  |---|---|---|---|---|
  | 1 | Modalidad | Tres `RadioButton`: «Importación», «Exportación», «Dep. Inspección» | Sí (siempre tiene valor) | — Se precarga por motivo de ingreso (F1-06) o por memoria. Bloqueada si el documento ya existe o en depósito adicional. |
  | 2 | Doc. comercial | `Select` con los tipos `CARTA-PORTE`, `FACTURA-COMERCIAL`, `REMISION` (regla actual `:351-355`) | Sí | «Seleccione el tipo de documento.» Se precarga por memoria. |
  | 3 | Nro. documento | `InputText`, mayúsculas al escribir, máx. 50 | Sí | Vacío: «Digite el número del documento.» Más de 50: «El número del documento no puede exceder 50 caracteres.» |
  | 4 | Nro. de manifiesto | `InputText`, máx. 100 | No | Más de 100: «El número de manifiesto no puede exceder 100 caracteres.» |
  | 5 | Peso según manifiesto (kg) | `InputNumber`, 2 decimales, sufijo « kg» | No | Si viene y es ≤ 0: «El peso bruto según manifiesto debe ser mayor que cero.» Texto de ayuda: «Opcional. Si no lo tiene, Comercio Exterior lo completa.» |

  Debajo del campo 3 va `DocumentMatchBanner` con el resultado de la búsqueda.

  **Panel plegado «Datos del documento (opcionales)»** (`Panel toggleable`, plegado por defecto). Encabezado: «Datos del documento — opcionales: Comercio Exterior los exige al confirmar ({n} de 7 diligenciados)».

  | # | Etiqueta | Control | Obligatorio | Validación y mensaje |
  |---|---|---|---|---|
  | 6 | Fecha del documento | `DatePicker` `dd/mm/yy`, máximo hoy | No; **Sí** tras una ambigüedad (409) | Futura: «La fecha del documento no puede ser futura.» Requerida tras 409: «Indique la fecha del documento para elegir el depósito.» |
  | 7 | Cliente | `Select` filtrable (terceros con rol cliente), `show-clear` | No | — |
  | 8 | Importador | `Select` filtrable y botón «+» (alta rápida, se conserva) | No | — |
  | 9 | Agencia de aduanas (SIA) | `Select` filtrable y botón «+» | No | — |
  | 10 | Exportador | `Select` filtrable y botón «+». Solo con modalidad Exportación. | No | — |
  | 11 | Valor de la mercancía | `InputNumber`, 2 decimales | No | ≤ 0: «El valor de la mercancía debe ser mayor que cero.» Más de 2 decimales: «El valor acepta máximo 2 decimales.» |
  | 12 | Moneda | `Select` COP / USD | No; **Sí** si hay valor | Con valor y sin moneda: «Seleccione la moneda del valor.» Se precarga por memoria. |

  Al final del panel, la línea «Fecha de ingreso: {dd/MM/yyyy HH:mm} (registrada por Vigilancia)» y un botón de texto «Cambiar» que muestra el `DatePicker` actual de la fecha de ingreso, con sus mismos límites (`:1126-1144`). Es la ganancia WMS-33: se conserva.

  Con un **documento existente**, el panel muestra en solo lectura lo que ya tiene el depósito (terceros de `existingServiceRecord.stakeholders`; valor y moneda de `existingWarehouseStorage`), con la nota «Estos datos son del depósito. Si están mal, los corrige Comercio Exterior.», y esos campos **no se envían**.

  **Búsqueda del documento (DF7):**
  - Se dispara al salir del campo «Nro. documento» (`blur`), al pulsar Enter en ese campo y al cambiar «Doc. comercial» con número escrito. No se repite si tipo, número y fecha no cambiaron.
  - Llama a `GET weighbridge/service-records/by-document` y, si hay dato, a `GET weighbridge/warehouse-storage/by-document`, con la fecha solo si el operario la digitó.
  - Estados de `DocumentMatchBanner`:

    | Estado | Aviso | Efecto |
    |---|---|---|
    | Buscando | «Buscando el documento…» con `ProgressSpinner` pequeño | — |
    | Nuevo (`data: null`) | `Message info`: «Documento nuevo: al guardar se crea un depósito.» | Formulario de depósito nuevo. |
    | Existente | `Message success`: «Se asociará al depósito {warehouseStorageNumber} ({Borrador / Confirmado}) · Camiones ingresados: {truckCount}» | Precarga modalidad y líneas del depósito (F1-02). Bloquea modalidad y tipo de carga. |
    | Cerrado (`truckEntriesClosedAt` lleno) | `Message error`: «El ingreso de camiones de este documento fue cerrado por {nombre} el {dd/MM/yyyy HH:mm}.» (texto actual `:746-750`) | Bloquea Guardar. |
    | Ambiguo (409) | `Message warn` con la `description` del backend: «Hay {n} depósitos abiertos con el documento {número}: {depósitos}. Indique la fecha del documento para elegir el depósito.» | Abre el panel, marca la fecha como obligatoria y le pasa el foco. Al elegir la fecha, se repite la búsqueda. |
    | Error de red o 5xx | `Message error`: «No se pudo consultar el documento.» y botón «Reintentar» | No bloquea: al guardar, el backend decide. |

  - En depósito adicional se conserva la regla actual: si el documento existe, error «El documento «{número}» ya corresponde a un depósito existente. Cada depósito adicional debe tener un número de documento único.» (`index.vue:564-571`).
  - Si el operario cambia el número después de encontrar un depósito, el estado vuelve a «sin buscar» y se limpian las líneas precargadas.

  **Qué se envía al guardar** (`onSubmit`, `:865-948`):
  - `documentDate`: la fecha o `null`.
  - `importerId` e `importerRoleId`, `importAgencyId` e `importAgencyRoleId`, `exporterId` y `exporterRoleId`: cada par solo si se eligió el tercero; si no, `null`. Con documento existente, `null`.
  - `manifestNumber`: texto recortado o `null`. `manifestWeight`: número o `null`.
  - `cargoValue`: número o `null`. `currency`: solo si hay `cargoValue` (DF10); si no, `null`.
  - El resto, como hoy.
  - La memoria del turno guarda moneda solo cuando se envió; modalidad, tipo de documento y perecedero, como hoy (`:842-851`).

  **Al guardar** (`handleStorageSubmit`):
  - Éxito con `isFirstTruck`: aviso «Depósito {warehouseStorageNumber} creado» y detalle «Documento {cargoManifestNumber}».
  - Éxito sin `isFirstTruck`: aviso «Camión asociado al depósito {warehouseStorageNumber}».
  - 409 de ambigüedad: mismo efecto que en la búsqueda.
  - 409 de documento cerrado o de modalidad distinta: el aviso global ya muestra el mensaje; la ficha marca el banner en error con ese texto.
  - Se elimina la contingencia «Producto no existe en catálogo» (`index.vue:411-430` y `openProductContingency`, `:73-75`): con la descripción libre de F1-02 ya no aplica.
- **Endpoints:**
  - **C-F1-03** `GET weighbridge/service-records/by-document` y `GET weighbridge/warehouse-storage/by-document`, query `cargoManifestNumber`, `primaryDocumentTypeId` y `documentDate` (opcional). 200 con `data` = el único depósito abierto (Borrador o Confirmado, ingreso sin cerrar) o `data: null`. 409 con el mensaje de ambigüedad.
  - **C-F1-02** `POST weighbridge/storage/register` y **C-F1-01** `POST weighbridge/storage/initiate` (depósito adicional). Cambian: `documentDate`, importador, agencia, `exporterId`/`exporterRoleId`, `manifestNumber`, `manifestWeight` y `currency` pasan a opcionales. Respuesta: `warehouseStorageNumber` siempre lleno y `createdProducts: [{ productId, name, sku }]`. Errores nuevos: «La fecha del documento no puede ser futura.», «El peso bruto según manifiesto debe ser mayor que cero.», «El número de manifiesto no puede exceder 100 caracteres.», «La moneda debe ser COP o USD.», el 409 de ambigüedad, el 409 de documento cerrado («El ingreso de camiones del documento '{número}' fue cerrado por {nombre} el {dd/MM/yyyy HH:mm}. No se pueden asociar más camiones. Si es un documento nuevo, indique su fecha.») y el 409 de modalidad distinta.
  - **Tipos que cambian:** en `IInitiateStorageWeighingRequest`, `manifestWeight?: number | null`; en `IInitiateStorageResponse`, agregar `warehouseStorageNumber: string | null` y `createdProducts: { productId: string; name: string; sku: string }[]`.
- **Roles y menú:** sin cambios (`requiredRoles: ["Admin", "Scale"]`).
- **Invalidación:** `useRegisterStorageEntry` ya invalida `['weighbridge']`; `useInitiateStorageWeighing` pasa a invalidarlo también.
- **Pruebas manuales** (rol Operario báscula):
  0. Datos: en Vigilancia, registrar el ingreso de la placa `TST101` con motivo «Descargue mercancia importacion».
  1. Abrir Báscula › Proceso de Pesaje y tomar `TST101`. → La sección «Documento» está visible, sin botón «Validar documento». El panel «Datos del documento» está plegado.
  2. Digitar un número de documento nuevo `CP-PAR-001` y pulsar Tab. → «Documento nuevo: al guardar se crea un depósito.»
  3. Sin abrir el panel, digitar una línea de mercancía y guardar (con F1-02 hecho; antes, con el modal actual). → Se crea el depósito y el aviso dice «Depósito 2026BA…».
  4. Registrar el ingreso de `TST102`, tomarlo y digitar `CP-PAR-001`. → «Se asociará al depósito 2026BA… (Borrador) · Camiones ingresados: 1».
  5. Crear con fechas distintas dos depósitos abiertos con el número `CP-PAR-002`; en un tercer camión digitar `CP-PAR-002` sin fecha. → Banner amarillo con el mensaje del backend, el panel se abre y el foco queda en «Fecha del documento». Elegir la fecha de uno de ellos. → «Se asociará al depósito …».
  6. En Comercio Exterior, cerrar el ingreso de camiones de `CP-PAR-001`; en báscula, digitar `CP-PAR-001` en otro camión. → Banner rojo y Guardar deshabilitado.
  7. Digitar un valor de la mercancía sin moneda e intentar guardar. → «Seleccione la moneda del valor.»
  8. Con el backend detenido, salir del campo del número. → «No se pudo consultar el documento.» con «Reintentar».
- **Terminado cuando:** un camión de importación se registra sin fecha, importador, agencia, valor, moneda ni manifiesto; el segundo camión del mismo documento se asocia sin fecha y el aviso muestra el número del depósito; la ambigüedad pide la fecha; nada se registra con «Validar documento».
- **Riesgo:** asociar un camión al depósito equivocado. Se mitiga mostrando el número y el estado del depósito antes de guardar (banner) y después (aviso). La regla de asociación vive en el backend.

---

#### F1-02 · Mercancía en línea y producto por descripción libre (BAS-02, BAS-03, UI-01)

- **Dificultad:** Alta.
- **Tarea del operario:** digitar qué trae el camión: producto, embalaje y cantidad, sin abrir un modal por producto y sin frenar el pesaje porque el producto no está en el catálogo.
- **Cómo lo hacía en el legacy:** tres campos en la misma pantalla, una línea: descripción del producto (texto libre que se pasa a mayúsculas, máx. 200, obligatorio), embalaje (texto, máx. 100, obligatorio) y cantidad (obligatoria) (`registrarentradabascula.php:884-900`). Al digitar la cantidad mostraba «Total: {n}» (`:676-690`). No tenía unidad de medida ni catálogo en báscula.
- **Lo que hace hoy la v2:** una tabla de solo lectura (`StorageServiceForm.vue:1285-1318`) y el botón «Agregar producto» (`:1333-1342`) que abre un modal por línea (`:1481-1574`), con producto obligatorio del catálogo y, si no existe, un segundo modal de «Crear producto (contingencia)» (`:1576-1592`) que crea el producto en el catálogo. La validación exige producto del catálogo y cantidad > 0 en cada línea (`:674-727`).
- **Pantallas y componentes:**
  - `app/features/weighbridge/components/TruckGoodsLines.vue` (nuevo): editor de líneas en línea.
  - `app/features/weighbridge/composables/useProductSuggestions.ts` (nuevo): sugerencias del catálogo con término diferido.
  - `app/features/weighbridge/components/StorageServiceForm.vue` (modifica): usa `TruckGoodsLines`; elimina el modal de producto, el de contingencia, `modalProductsQueryParams`, `createProductMutation` y sus funciones (`:320-337`, `:549-672`); reescribe `validateProductLines` y el mapeo de `products`.
  - `app/features/weighbridge/types/requests.ts` (modifica): `IStorageProductItemInput.productId: string | null`.
- **Modelo de una línea** (en `TruckGoodsLines`):

  ```ts
  interface ITruckGoodsLine {
    uid: string
    catalogProduct: { id: string; name: string; sku: string; description: string | null;
                      unitMeasureId: string | null; unitMeasureName: string | null;
                      packagingTypeId: string | null } | null  // null = descripción libre
    description: string            // lo digitado, o el nombre del producto elegido
    packagingTypeId: string | null
    unitMeasureId: string | null
    quantity: number | null
    fromDeposit: boolean           // línea precargada de un depósito existente: producto fijo
  }
  ```

- **Diseño de la interacción.** Bajo el título «Mercancía de este camión» (y, si el documento existe, el `PreviousEntriesPanel` que ya existe, encima), una fila por producto:

  | Columna | Etiqueta | Control | Obligatorio | Validación y mensaje |
  |---|---|---|---|---|
  | 1 | Producto | `AutoComplete` con sugerencias del catálogo; `option-label="name"`; plantilla de opción «{sku} — {name}»; acepta texto libre | Sí | Texto libre de menos de 3 letras: «Escriba al menos 3 letras o elija un producto del catálogo.» Más de 200: «La descripción no puede exceder 200 caracteres.» |
  | 2 | Embalaje | `Select` de tipos de embalaje activos (`usePackagingTypes`), `show-clear` | No | — |
  | 3 | Unidad | Producto del catálogo **con** unidad: texto de solo lectura con su unidad. Texto libre, o producto sin unidad: `Select` de unidades activas (`features/administration/composables/useUnitMeasures.ts`). | Sí | «Seleccione la unidad de medida.» |
  | 4 | Cantidad de este camión | `InputNumber`, hasta 2 decimales | Sí en depósito nuevo; en un depósito existente la línea precargada puede quedar vacía | ≤ 0: «La cantidad debe ser mayor que cero.» |
  | 5 | — | Botón icono papelera, `aria-label="Quitar producto"`, `tabindex="-1"` | — | Las líneas precargadas del depósito no se quitan: se dejan vacías. |

  - Debajo, el botón «Agregar otro producto» (`severity="secondary" outlined`) agrega una línea vacía y le pasa el foco a su «Producto». Con documento existente dice «Agregar producto que no está en el depósito».
  - Debajo, «Total de este camión: {suma}» cuando hay cantidades (como el legacy).
  - Mensaje global bajo la tabla si ninguna línea tiene cantidad: «Ingrese la cantidad de al menos un producto para este camión.» (mismo texto del backend).
  - **Depósito nuevo:** arranca con una línea vacía.
  - **Documento existente:** una línea por producto del depósito, con producto, unidad y embalaje fijos (`fromDeposit = true`) y la cantidad vacía (comportamiento WMS-25 actual, `:482-513`).
  - **Sugerencias:** el término digitado se difiere 300 ms con `refDebounced` y consulta `GET product` con `{ searchTerm, isActive: true, productType: 'Producto', pageIndex: 1, pageSize: 20 }` (`useProducts`). Clave de consulta `['products', 'weighbridge-suggestions', término]`. No consulta con menos de 2 caracteres.
  - **Elegir una sugerencia:** `catalogProduct` = el producto; `description` = su nombre; unidad y embalaje del producto.
  - **Texto libre:** al salir del campo, si el texto normalizado (sin tildes, mayúsculas, espacios colapsados) coincide con el nombre de una sugerencia cargada, se elige esa sugerencia. Si no, la línea queda libre: el texto pasa a mayúsculas y aparece una `Tag` «Nuevo en el catálogo» bajo el campo, y la unidad se vuelve obligatoria y editable (DF16).
  - **Tabulación de la fila:** Producto → Embalaje → Unidad (solo si es editable) → Cantidad. Tab desde la Cantidad de la última fila va a «Agregar otro producto».
  - **Enter:** con la lista de sugerencias abierta, Enter elige la sugerencia (comportamiento de PrimeVue); con la lista cerrada, Enter es el guardado de la ficha (F1-06).
- **Qué se envía** (`products`), solo las líneas con producto o cantidad (una fila totalmente vacía se ignora):

  | Campo | Línea del catálogo | Línea libre |
  |---|---|---|
  | `productId` | id del producto | `null` |
  | `productDescription` | `description` del producto o su nombre (regla actual) | el texto en mayúsculas, recortado |
  | `unitMeasureId` | unidad del producto, o la elegida si el producto no tiene | la elegida |
  | `packagingTypeId` | el elegido o `null` | el elegido o `null` |
  | `entryDeclaredQuantity` | la cantidad o `null` | la cantidad |

- **Al guardar:** si la respuesta trae `createdProducts` no vacío, aviso informativo: «Se creó en el catálogo: {name} (SKU {sku}). Comercio Exterior lo revisará.», uno por producto. Al reabrir el formulario para otro camión, la memoria **no** recuerda unidad ni embalaje (regla O2-D20 vigente).
- **Endpoints:**
  - **C-F1-09** `GET product`: sugerencias. Query `searchTerm`, `isActive`, `productType`, `pageIndex`, `pageSize`.
  - **C-F1-01 / C-F1-02**: `products[].productId` opcional si viene `productDescription`. Con `productId` nulo, la descripción es obligatoria (3 a 200 caracteres): el backend busca el producto por nombre sin tildes ni mayúsculas y, si no existe, lo crea. Errores: «La descripción del producto debe tener entre 3 y 200 caracteres.», «La unidad de medida del producto es requerida.», «Ingrese la cantidad de al menos un producto para este camión.», 404 «El producto con Id '{id}' no existe.», 409 «No se pudo generar un SKU único para el producto; intente de nuevo.»
- **Roles y menú:** sin cambios.
- **Invalidación:** la de F1-01. Además, `['products']` si `createdProducts` no está vacío.
- **Pruebas manuales** (Operario báscula):
  1. Camión nuevo, documento nuevo. → Aparece una línea vacía con el foco en «Producto» después del documento.
  2. Escribir «ceb» y elegir «CEBOLLA» de las sugerencias. → La unidad aparece en solo lectura y el embalaje precargado.
  3. Pulsar «Agregar otro producto», escribir «papa criolla roja» y salir del campo. → Queda «PAPA CRIOLLA ROJA» con la etiqueta «Nuevo en el catálogo» y la unidad obligatoria.
  4. Guardar sin unidad en la línea libre. → «Seleccione la unidad de medida.» en esa línea.
  5. Elegir la unidad, digitar cantidades y guardar. → Se crea el depósito y aparece «Se creó en el catálogo: PAPA CRIOLLA ROJA (SKU BAS-…)».
  6. Segundo camión del mismo documento. → Dos líneas precargadas con la cantidad vacía; digitar solo una y guardar. → Se asocia sin error.
  7. Escribir « Papa  criolla roja » en otro camión. → Al salir del campo se elige el producto existente, sin etiqueta «Nuevo».
  8. Revisar que ya no exista el modal «Agregar producto» ni «Crear producto (contingencia)».
- **Terminado cuando:** se digitan varias líneas sin abrir ningún modal; una descripción que no está en el catálogo se guarda y el backend crea el producto; el segundo camión precarga las líneas del depósito.
- **Riesgo:** el catálogo se llena de variantes del mismo producto. Se mitiga eligiendo la coincidencia exacta al salir del campo, con la marca «Creado desde báscula» y con la normalización de Comercio Exterior (F1-08).

---

#### F1-03 · Tipo de carga y unidades de carga sin desglose en báscula (BAS-07, UI-01)

- **Dificultad:** Media.
- **Tarea del operario:** registrar un camión que trae contenedores, tanqueros o remolques, anotando su placa, sin frenar el pesaje para repartir la mercancía entre las unidades.
- **Cómo lo hacía en el legacy:** el selector de unidad de carga está comentado en el formulario (`registrarentradabascula.php:873-878`): en la práctica no la capturaba en báscula.
- **Lo que hace hoy la v2:**
  - El tipo de carga (`cargoHandling`) existe en el formulario y en el envío (`StorageServiceForm.vue:198-221,932-942`), pero **el selector nunca se pintó**: `cargoHandlingOptions` y `cargoHandlingLocked` no se usan en la plantilla. En un depósito nuevo siempre se envía «Mercancía suelta» (DF15).
  - `CargoUnitsEditor.vue:97-140` exige, por unidad, al menos una línea de mercancía con producto y cantidad.
- **Pantallas y componentes:**
  - `app/features/weighbridge/components/StorageServiceForm.vue` (modifica): selector de tipo de carga y reglas de las unidades.
  - `app/features/weighbridge/components/CargoUnitsEditor.vue` (modifica): mercancía por unidad opcional, con interruptor.
  - `app/features/weighbridge/types/requests.ts` (modifica): `cargoUnits[].products` opcional; cada línea con `productId: string | null` y `productDescription?: string | null`.
- **Diseño de la interacción.** En «Mercancía de este camión», **antes** de las líneas:

  | Etiqueta | Control | Obligatorio | Validación y mensaje |
  |---|---|---|---|
  | Tipo de carga | `SelectButton` «Mercancía suelta» / «Unidades de carga» (`CARGO_HANDLING_LABELS`) | Sí, por defecto «Mercancía suelta» | Bloqueado cuando el documento ya existe: hereda el del depósito (`cargoHandlingLocked`). |

  Con «Unidades de carga», debajo de las líneas del camión, el editor de unidades:

  | Etiqueta | Control | Obligatorio | Validación y mensaje |
  |---|---|---|---|
  | Tipo de unidad | `Select` de tipos activos | Sí | «Seleccione el tipo de unidad de carga.» |
  | Placa | `InputText` con `normalizePlate` | Sí | «La placa debe tener de 3 a 20 letras, números o guiones.» Repetida: «Esta placa ya está registrada en el depósito» |
  | Detallar mercancía por unidad | `ToggleSwitch`, uno para todo el camión, **apagado** por defecto | — | — |
  | (con el interruptor encendido, por unidad) Producto | `Select` con las líneas del camión | Sí | «Seleccione el producto de cada línea de mercancía.» |
  | (por unidad) Cantidad | `InputNumber` | Sí | «La cantidad declarada debe ser mayor que cero.» |

  - Botón «Agregar unidad de carga». Sin unidades: «Agregue al menos una unidad de carga.»
  - **Interruptor apagado** (caso normal): las cantidades se digitan en las líneas del camión, como en mercancía suelta. Aviso informativo:
    - con una unidad: «La mercancía del camión queda en la unidad {placa}.»;
    - con dos o más: «Comercio Exterior repartirá la mercancía entre las unidades antes de confirmar el depósito.»
  - **Interruptor encendido:** regla actual. Las cantidades de las líneas del camión se calculan como la suma de las unidades y quedan en solo lectura. Cada línea del camión debe estar en alguna unidad: «El producto {nombre} no está en ninguna unidad de carga».
  - **Depósito existente confirmado con dos o más unidades:** el interruptor queda encendido y bloqueado, con el aviso «El depósito {número} ya está confirmado: declare la mercancía de cada unidad de carga de este camión.» (mismo texto del backend).
- **Qué se envía:** `cargoHandling`; `cargoUnits: [{ cargoUnitTypeId, plateNumber, products }]`, con `products: null` si el interruptor está apagado. Si está encendido, cada línea lleva `{ productId, productDescription, declaredQuantity }`: `productId` si la línea del camión es del catálogo; si es libre, `productId: null` y `productDescription` = su texto.
- **Endpoints:** **C-F1-01 / C-F1-02**. `cargoUnits[].products` opcional: todas las unidades con mercancía o ninguna. Errores: 400 «Declare la mercancía en todas las unidades de carga del camión o en ninguna.» y 400 «El depósito {número} ya está confirmado: declare la mercancía de cada unidad de carga de este camión.»
- **Roles y menú:** sin cambios. **Invalidación:** la de F1-01.
- **Pruebas manuales** (Operario báscula):
  1. Documento nuevo, «Unidades de carga», una unidad CONTENEDOR `CONT001`, interruptor apagado, una línea con cantidad 10. → Se guarda. En Comercio Exterior, la unidad `CONT001` tiene 10 del producto.
  2. Documento nuevo con dos unidades e interruptor apagado. → Se guarda. En Comercio Exterior las unidades están vacías y «Confirmar» pide el reparto (F1-07/F1-08).
  3. Con el depósito del paso 2 confirmado (después de F1-08), segundo camión con dos unidades. → El interruptor está encendido y bloqueado.
  4. Interruptor encendido, línea libre «AJO MORADO» en una unidad. → Se guarda y el reparto aparece en Comercio Exterior.
- **Terminado cuando:** un camión con contenedor se registra solo con tipo y placa de la unidad, y el selector «Tipo de carga» es visible en documentos nuevos.
- **Riesgo:** despachar por unidad sin reparto. El backend lo impide: confirmar exige el reparto.

---

#### F1-04 · Efectivo recibido y cambio en el cobro (BAS-05, GAP-024 b, UI-01)

- **Dificultad:** Media.
- **Tarea del operario:** al cobrar en efectivo, saber cuánto cambio devolver sin hacer la cuenta de memoria.
- **Cómo lo hacía en el legacy:** el recibo mostraba «Total a Pagar», «Efectivo» (con el foco al abrir) y «Cambio», calculado al teclear (`modulos/mod_bascula/facturar.php:152-157`, `:232`, `:787-800`), y guardaba ambos (`:71-72`, `:100`).
- **Lo que hace hoy la v2:** `BillingCollectForm.vue` registra método, modo, total, referencia y notas, sin efectivo ni cambio (`:463-530`). `PaymentForm.vue` sí los calcula (`:178-185,263-266,525-548`) pero ninguna pantalla lo usa.
- **Pantallas y componentes:**
  - `app/features/billing/utils/cash-change.ts` (nuevo): `calculateCashChange(total: number, cash: number | null): { change: number; insufficient: boolean }`. Es la lógica de `PaymentForm.vue:180-185,263-266`.
  - `app/features/weighbridge/components/PaymentForm.vue` (modifica): usa la utilidad. Sin cambio visible.
  - `app/features/billing/components/BillingCollectForm.vue` (modifica): prop nueva `showCashChange?: boolean` (por defecto `false`), campos, validación y `cashReceived` en el `emit`.
  - `app/features/billing/types/billing-collect.ts` (modifica): `IBillingCollectData.cashReceived?: number | null`.
  - `app/features/weighbridge/types/requests.ts` (modifica): `cashReceived?: number | null` en `IProcessWeighingOnlyPaymentRequest`, `IProcessStoragePaymentRequest` e `IProcessOutputPaymentRequest`.
  - `app/features/weighbridge/types/weighbridge-cycle.ts` (modifica): `IProcessPaymentResponse.cashReceived: number | null`; los pagos del detalle del ciclo agregan `cashReceived` y `changeGiven`.
  - `app/pages/operations/weighbridge/index.vue` (modifica): pasa `:show-cash-change="true"` y envía `cashReceived`.
  - `app/pages/operations/weighbridge/history.vue` (modifica): en «Pagos» del detalle (`:653-662`) muestra «Efectivo {valor} · Cambio {valor}» cuando vienen.
  - **No cambian** el cobro de montacargas (`features/warehouse/components/ForkliftUseDialog.vue:483`) ni el de guías (`features/foreign-trade/components/DispatchGuideForm.vue:279`): no pasan la prop y sus endpoints no aceptan efectivo.
- **Diseño de la interacción** (solo con `showCashChange`, método «Efectivo», modo «Pago inmediato» y destinatario distinto de «Clientes»), justo después de «Total a pagar»:

  | Etiqueta | Control | Obligatorio | Validación y mensaje |
  |---|---|---|---|
  | Efectivo recibido | `InputNumber` moneda COP, 0 decimales, mínimo 0 | No | Menor que el total: «El efectivo recibido es menor que el total a pagar.» |
  | Cambio a devolver | Texto grande en verde, solo lectura: `formatCurrency(change)` | — | Se muestra cuando el efectivo ≥ total. |

  - Si el operario cambia el método o el modo, el efectivo se borra.
  - Foco: lo maneja F1-05 (el paso de cobro empieza en «Efectivo recibido» cuando aplica).
- **Al cobrar:** el cuerpo agrega `cashReceived` (solo con efectivo; si no, `null`). Aviso de éxito: «Pago registrado» con el detalle «Cambio: {changeAmount}» cuando `changeAmount` > 0.
- **Endpoints:** **C-F1-12** `POST weighbridge/{storage|weighing-only|output}/process-payment`. Agrega `cashReceived` (decimal | null), solo con `paymentMethod = "Cash"`. Respuesta: `changeAmount` = `cashReceived − totalAmount`, y `cashReceived`. Errores: «El efectivo recibido solo aplica a pagos en efectivo.», «El efectivo recibido no puede ser negativo.», «El efectivo recibido ({x:N0}) es menor que el total a pagar ({y:N0}).» El detalle del ciclo (`GET weighbridge/cycles/{id}`) agrega `cashReceived` y `changeGiven` en cada pago.
- **Roles y menú:** sin cambios.
- **Invalidación:** `useProcessPayment.ts` (las tres mutaciones) invalida `['weighbridge']`, `['weighbridgeHistory']` y `['weighbridge-history']` al terminar.
- **Pruebas manuales:**
  1. Báscula: cobrar 23.000 en efectivo, digitar 50.000. → «Cambio a devolver $27.000». Cobrar. → «Cambio: $27.000» en el aviso.
  2. Digitar 20.000. → «El efectivo recibido es menor que el total a pagar.» y no deja cobrar.
  3. Cambiar a «Transferencia Bancaria». → Desaparece el efectivo.
  4. Elegir «Pendiente por facturar». → No aparece el efectivo.
  5. Historial: abrir el detalle del ciclo. → «Efectivo $50.000 · Cambio $27.000».
  6. Montacargas y guía de salida: el formulario de cobro no muestra el efectivo.
- **Terminado cuando:** el cambio se ve al digitar, viaja al backend y queda en el detalle; montacargas y guías no cambian.
- **Riesgo:** romper los otros dos cobros. Se mitiga con la prop opcional apagada por defecto y la prueba 6.

---

#### F1-05 · Cobro y peso en la misma ficha, sin modales (BAS-04, UI-01, DF5, DF9)

- **Dificultad:** **Muy alta.** Cambia el flujo del banco de trabajo, la cola y el cobro.
- **Tarea del operario:** tras registrar el documento y la mercancía, cobrar y digitar el peso sin abrir ventanas ni usar el mouse.
- **Cómo lo hacía en el legacy:** el peso bruto se digitaba en el mismo formulario (`registrarentradabascula.php:840-862`). Tras «Insertar registro», la pantalla del listado abría sola el cobro (`listarentradasbascula.php:301,310`), con el foco en «Efectivo» (`facturar.php:232`); en importación elegía sola el tiquete «entrada y tara» (`facturar.php:213-219`). «Guardar» preguntaba «¿Desea Imprimir Ahora?» e imprimía (`facturar.php:158-185`).
- **Lo que hace hoy la v2:** «Guardar» (`index.vue:320-340`) abre el modal «Facturación y cobro» (`:1084-1127`). Al cobrar, se cierra y abre el modal «Captura de peso» (`:679-684`, `:1129-1207`), que muestra la impresión del tiquete al completar el ciclo (`:1138-1182`).
- **Pantallas y componentes:**
  - `app/pages/operations/weighbridge/index.vue` (modifica): modelo de pasos, secciones en línea, elimina el modal de cobro, el modal de peso queda solo para F2, nuevo recorrido de retomar.
  - `app/features/weighbridge/components/WeightCapture.vue` (modifica): prop `embedded` (oculta el título «Captura de Peso» y la tarjeta «Información del Vehículo», `:280-313`, y conserva la lista de pesajes previos), `defineExpose({ focusWeight })` y atributo `data-enter-scope="weight"` en la raíz.
  - `app/features/billing/components/BillingCollectForm.vue` (modifica): `defineExpose({ submit, focusFirst })`; `initialRecipientMode` acepta `"driver"`.
  - `app/features/weighbridge/components/WeighbridgeStepSection.vue` (nuevo): contenedor de un paso, con número, título, estado (pendiente, actual, hecho) y resumen cuando está hecho.
- **Diseño de la interacción.** La ficha tiene cuatro bloques, uno debajo de otro:

  | Paso | Cuándo está activo | Contenido | Resumen cuando está hecho |
  |---|---|---|---|
  | 1. Registro | Sin `serviceRecordId` | Formulario de la operación (Ingresos, Solo báscula o Salida), como hoy. | «Registrado: depósito {número} · Documento {número}» (Ingresos); «Registrado: orden {número}» (Salida); «Registrado» (Solo báscula). El formulario queda en solo lectura. |
  | 2. Cobro | Con `serviceRecordId` y sin ciclo (`activeCycleId` nulo) | `BillingCollectForm` en línea, con `:title="null"`, `submit-label="Cobrar"`, `:show-cash-change="true"`. En depósito adicional, el `Message` actual «Depósito adicional — factura en cero…» y el botón «Confirmar y continuar» (`index.vue:1093-1108`). | «Cobrado: {total} · {método}» y «Cambio: {cambio}» si hubo; o «Pendiente por facturar». |
  | 3. Peso | Con ciclo y sin completar | `WeightCapture` con `embedded` | Cada pesaje registrado, como hoy. |
  | 4. Tiquete | Ciclo completo (`showPrintTicketSection`) | El bloque verde actual «Pesaje completado» con «Observación para el ticket (opcional)», «Imprimir Ticket» y «Finalizar» (`index.vue:1138-1182`), en línea. | — |

  - Los pasos aún no alcanzados se muestran con su título en gris y la leyenda «Se habilita al {registrar / cobrar}». No ocupan tabulación.
  - **Destinatario por defecto del cobro (DF9):**
    - `"registered"` con el cliente preseleccionado si la operación lo tiene (`billingPreselectedCustomerId`);
    - si no, `"driver"` si el ingreso tiene conductor (`billingDriver` no nulo);
    - si no, `"registered"` vacío.
  - **Errores del cobro:** cliente en mora, efectivo insuficiente o tarifa: el aviso global muestra el mensaje del backend y la ficha se queda en el paso 2 con los datos digitados. **Se conserva la validación de mora**: no se agrega ningún atajo que la salte.
  - **Pendiente por facturar:** igual que hoy (`index.vue:624-638`), y pasa al paso 3.
  - **Peso:** `WeightCapture` conserva su lógica:
    - tipo permitido según el estado;
    - «Fecha y hora del pesaje» propuesta = ingreso del camión (WMS-33);
    - «Peso (kg)» obligatorio: «Debe ingresar el peso» / «El peso debe ser mayor a cero»;
    - tras un peso que no cierra el ciclo, «Continuar pesaje», «Agregar otro depósito» (solo multidepósito) y «Salir y atender otro camión».
  - **F2:** abre el modal «Captura de peso» actual con el mismo `WeightCapture` (sin `embedded`). Mientras el modal está abierto, el paso 3 en línea no se monta, para no tener dos formularios del mismo ciclo.
  - **Botón «Capturar peso» de la cola** (`TruckQueue`, evento `capture-weight`): selecciona el camión y pone el foco en el peso en línea; ya no abre el modal.
  - **Retomar desde «Recuperar operaciones»** (`index.vue:842-890`): con ciclo, hidrata el ciclo y enfoca el paso 3; sin ciclo, enfoca el paso 2. Ya no abre modales.
  - **Barra inferior:** se quitan los botones «Cobrar» y «Capturar peso» (`:1054-1069`); queda «Guardar» (solo en el paso 1) y el texto de ayuda de F1-06.
  - **Borradores (AC):** el paso actual de cada camión se guarda en `drafts`. Al volver a un camión de la cola, la ficha abre en su paso.
  - **«Soltar camión»:** igual que hoy (`releaseTruck`). Un camión soltado en el paso 2 queda en la cola como «Por cobrar», como al cerrar hoy el modal sin pagar.
- **Endpoints** (sin cambios de ruta; los mismos de hoy):
  - `POST weighbridge/{storage|weighing-only|output}/process-payment` (C-F1-12) y `POST weighbridge/{…}/start-pending-billing`;
  - `POST weighbridge/cycles/{cycleId}/weighings` (`useRecordWeighing`);
  - `GET weighbridge/cycles/{id}` (`hydrateCycle`);
  - `GET weighbridge/{id}/ticket/pdf` (`useTicketPdf`).
- **Roles y menú:** sin cambios.
- **Invalidación:**
  - cobro: la de F1-04;
  - pendiente por facturar (`useStartWeighingPendingBilling.ts`): agregar `['weighbridge']`;
  - peso: la actual de `useRecordWeighing.ts` más `['weighbridge']`;
  - se conserva el `refetchQueue()` actual.
- **Pruebas manuales** (Operario báscula):
  1. Registrar un camión de importación. → La ficha baja al paso 2 «Cobro» sin abrir ventana; el destinatario es «Conductor del vehículo» si no se eligió cliente.
  2. Cobrar en efectivo. → Resumen «Cobrado…» y el foco en «Peso (kg)».
  3. Digitar el peso y Enter. → «Peso registrado — Ciclo en progreso» con «Salir y atender otro camión». Pulsarlo. → La ficha se suelta y el camión aparece en la cola como «Por repesar».
  4. Tomar el camión de «Por repesar». → La ficha abre en el paso 3 con el primer peso listado; registrar la tara. → Paso 4: «Imprimir Ticket» descarga el PDF; «Finalizar» suelta el camión.
  5. Pulsar F2 en el paso 3. → Se abre el modal de peso y desaparece el paso 3 en línea; Esc lo cierra y el paso 3 vuelve.
  6. Cliente bloqueado por mora: elegirlo como destinatario y cobrar. → Mensaje del backend y la ficha sigue en el paso 2.
  7. Soltar un camión en el paso 2, ir a «Recuperar operaciones» y retomarlo. → Abre la ficha en el paso 2, sin modal.
  8. Depósito adicional (multidepósito): tras el primer peso, «Agregar otro depósito», registrar el segundo documento. → El paso 2 muestra la confirmación en $0 y luego vuelve al paso 3.
  9. Saltar entre dos camiones con datos a medio digitar. → Cada uno conserva lo digitado y su paso (KeepAlive y borradores).
  10. Solo báscula y Salida de mercancía. → Registro, cobro y peso funcionan igual, en línea.
- **Terminado cuando:** las tres operaciones se completan de principio a fin sin abrir ningún modal, F2 sigue funcionando y las pruebas 6, 7 y 9 pasan.
- **Riesgo:** perder estado al saltar entre camiones o duplicar un cobro. Se mitiga así:
  - el paso se deriva del estado del servidor (`serviceRecordId`, `activeCycleId`, `cycleResumedStatus`), no de banderas sueltas;
  - el botón «Cobrar» se deshabilita mientras la mutación está pendiente;
  - revisión humana del diff de `index.vue`.

---

#### F1-06 · Trabajar con el teclado de arriba a abajo (BAS-06, UI-01, DF6, DF8)

- **Dificultad:** **Muy alta.** Toca los atajos y el foco del banco de trabajo, y quita la confirmación del depósito.
- **Tarea del operario:** registrar el camión sin soltar el teclado, con el foco donde empieza a escribir y Enter para avanzar.
- **Cómo lo hacía en el legacy:**
  - foco inicial en «Capturar» (`registrarentradabascula.php:733`);
  - recorrido de los campos encadenado con `onfocus` que saltaba al siguiente (`:759`, `:771`, `:850`);
  - al elegir el documento, el foco pasaba al manifiesto (`:555`);
  - el cobro abría con el foco en «Efectivo» (`facturar.php:232`);
  - atajos globales Alt+N (entrada) y Alt+K (salida) (`entrada.php:9-35`).
- **Lo que hace hoy la v2:**
  - foco en el primer campo de la ficha (`index.vue:249-256`), que es el panel del camión o la modalidad, no el documento;
  - Enter guarda (`:818-823`) y abre el modal «Confirmar creación de depósito» (`StorageServiceForm.vue:1427-1479`), un clic más por camión;
  - el tipo de operación se elige con el mouse (`index.vue:986-990`).
- **Pantallas y componentes:**
  - `app/pages/operations/weighbridge/index.vue` (modifica): foco por paso, manejador de Enter, preselección por motivo, texto de ayuda.
  - `app/features/weighbridge/utils/entry-reason-operation.ts` (nuevo): mapa de motivo a operación.
  - `app/features/weighbridge/components/StorageServiceForm.vue` (modifica): quita el modal de confirmación y agrupa la configuración del pesaje en un panel plegado.
  - `app/features/weighbridge/components/OperationTypeSelector.vue` (modifica): las tarjetas son botones (`<button type="button">`) que se eligen con Enter o Espacio.
- **Diseño de la interacción.**

  **Preselección por motivo de ingreso (DF8):** al abrir un camión «Sin iniciar» sin borrador, se mira `selectedEntry.entryReasonId`. Los IDs están sembrados en el backend (`Wms.Infrastructure/Persistence/SeedDataExtensions.cs:255-261`):

  | Motivo (ID) | Tipo de operación | Modalidad |
  |---|---|---|
  | Descargue mercancia importacion (`1e7a8f2b-9c4d-4a1e-b3f6-2d8e5c0a1b70`) | Ingresos | Importación |
  | Descargue mercancia exportacion (`7b2d9f4a-3c8e-4f1b-d0a5-9c7e2f6b4d03`) | Ingresos | Exportación |
  | Cargue mercancia importacion (`3f9b0c4e-7a2d-4b8f-e1c5-6a3d9e2b0f81`) | Salida de mercancía | — |
  | Cargue mercancia exportacion (`5a1c8e3f-2b7d-4e0a-c9f4-8b6d1e5a3c92`) | Salida de mercancía | — |
  | Solo Bascula (`9c3e0a5b-4d9f-401c-e1b6-0d8f3a7c5e14`) | Solo báscula | — |
  | Otro motivo | Ninguno: el operario elige | — |

  La modalidad del motivo gana sobre la de la memoria (solo para la modalidad; tipo de documento, moneda y perecedero siguen saliendo de la memoria). Se muestra el `PrefilledHint` actual con el texto «Según el motivo de ingreso».

  **Foco inicial** al abrir un camión:

  | Estado del camión | Foco en |
  |---|---|
  | Sin iniciar, operación preseleccionada «Ingresos» | «Nro. documento» |
  | Sin iniciar, «Salida de mercancía» | el campo de número de orden de `OutputServiceForm` |
  | Sin iniciar, «Solo báscula» | el cliente de `WeighingOnlyForm` |
  | Sin iniciar, sin preselección | la primera tarjeta de «Tipo de operación» |
  | Por cobrar | «Efectivo recibido» si el método es efectivo y el modo inmediato; si no, «Método de Pago» |
  | Por pesar / Por repesar | «Peso (kg)» |

  **Orden de tabulación de «Ingresos»:** Modalidad → Doc. comercial → Nro. documento → Nro. de manifiesto → Peso según manifiesto → [panel «Datos del documento», plegado: no entra] → Tipo de carga → líneas (Producto → Embalaje → Unidad → Cantidad) → «Agregar otro producto» → [panel «Configuración del pesaje», plegado: no entra] → Guardar. El panel «Camión y conductor» queda arriba y plegado cuando está completo (regla actual).

  **Panel plegado «Configuración del pesaje y documentos»** reúne lo que hoy son las secciones 3 y 4 (`StorageServiceForm.vue:1345-1410`): «Primer pesaje» (BRUTO o TARA), «Segundo pesaje», «Flujo perecederos», «Documentos adicionales» y «Observaciones», con sus reglas actuales. Encabezado con el resumen: «Primer peso: BRUTO · Segundo pesaje: Sí · Perecedero: No». La memoria de perecedero se conserva y, si viene de la memoria, el panel abre desplegado para que se vea.

  **Sin modal de confirmación (DF6):** se elimina el diálogo «Confirmar creación de depósito» (`:1427-1479`), con `pendingSummary` y `buildConfirmationSummary`. Lo reemplaza el `DocumentMatchBanner` de F1-01, que ya dice si se crea o se asocia y a qué depósito. Guardar envía directo.

  **Manejador de Enter** (reemplaza `index.vue:818-823`). Enter ejecuta la acción del paso actual. **No actúa** si:
  - el destino es un `textarea`, un `button`, un enlace o un contenido editable;
  - hay un modal abierto;
  - el destino está dentro de un elemento con `aria-expanded="true"` (lista de sugerencias o `Select` abierto);
  - el destino está dentro de `[data-enter-scope="weight"]` (el formulario de peso se envía solo);
  - el evento ya fue atendido (`defaultPrevented`).

  | Paso | Enter hace |
  |---|---|
  | 1 en «Nro. documento» | Busca el documento (F1-01) y pasa el foco a «Nro. de manifiesto». |
  | 1 en otro campo | Guardar. |
  | 2 | Cobrar (`BillingCollectForm.submit()`), o «Confirmar y continuar» en depósito adicional. |
  | 3 | Lo maneja el formulario de `WeightCapture`. |

  **Esc:** cierra el modal de peso si está abierto. **F2:** abre el modal de peso si hay ciclo (regla actual).

  **Después de cada paso:** al registrar, foco en el primer campo del cobro (regla de la tabla); al cobrar, foco en «Peso (kg)»; tras «Salir y atender otro camión» o «Finalizar», foco en el primer camión «Sin iniciar» de la cola.

  **Texto de ayuda de la barra** (reemplaza `:1045-1052`):
  - paso 1: «Enter guarda · Tab avanza · F2 peso en ventana»;
  - paso 2: «Enter cobra»;
  - paso 3: «Enter registra el peso · F2 peso en ventana · Esc cierra la ventana».
- **Endpoints:** ninguno nuevo.
- **Roles y menú:** sin cambios. **Invalidación:** ninguna nueva.
- **Pruebas manuales** (Operario báscula, sin tocar el mouse después de abrir la página):
  1. Vigilancia registra `TST201` con «Descargue mercancia importacion». En báscula, Tab hasta el camión en la cola y Enter. → Operación «Ingresos» e «Importación» preseleccionadas y el foco en «Nro. documento».
  2. Digitar el documento y Enter. → Busca y el foco pasa a «Nro. de manifiesto».
  3. Tab por el manifiesto y su peso hasta «Producto», digitar, Tab a «Cantidad», digitar y Enter. → Guarda sin modal de confirmación y el foco queda en el cobro.
  4. Digitar el efectivo y Enter. → Cobra y el foco queda en «Peso (kg)»; digitar y Enter. → Registra el peso.
  5. Tab a «Salir y atender otro camión» y Enter. → El foco vuelve al primer camión «Sin iniciar» de la cola.
  6. Con un motivo «Otro». → No hay preselección y el foco está en la primera tarjeta de operación; Enter la elige.
  7. Con la lista de sugerencias de producto abierta, Enter elige la sugerencia y **no** guarda.
  8. Enter en «Observaciones» (textarea) hace salto de línea y no guarda.
- **Terminado cuando:** las pruebas 1 a 8 pasan sin mouse y el modal de confirmación ya no existe.
- **Riesgo:** un Enter accidental guarda un camión. Se mitiga así: Guardar exige los campos obligatorios; el banner muestra el depósito antes de guardar; el cobro y el peso son pasos aparte, cada uno con su propio Enter.

---

#### F1-07 · Comercio Exterior completa el depósito y ve qué falta para confirmar (BAS-01, UI-01)

- **Dificultad:** Alta.
- **Tarea del operario (Comercio Exterior):** completar en el depósito lo que báscula ya no pide (fecha del documento, importador, agencia de aduanas, exportador, valor, moneda y manifiesto de cada camión) y confirmar sabiendo qué falta.
- **Cómo lo hacía en el legacy:** «Modificar ingreso» con todos los datos del ingreso en una pantalla (`modulos/mod_ingresos/modificaringreso.php:311-494`): fecha y hora de ingreso, nro. y fecha del manifiesto DIAN, doc. comercial, nro. y fecha del documento, transportadora, SIA, exportador, importador, peso neto, peso bruto, precio de la mercancía, moneda, volumen, condiciones y observaciones. Sin validación al confirmar.
- **Lo que hace hoy la v2:**
  - «Confirmar depósito» solo exige cliente (`pages/foreign-trade/imports/[id]/index.vue:122-125`, igual en `exports/[id]` e `inspections/[id]`);
  - la fecha del documento no se edita;
  - el manifiesto por camión no se edita (`features/foreign-trade/components/DepositExpandedEntriesTable.vue`);
  - los terceros documentales solo admiten importador y agencia (`DepositDetailDocumentStakeholdersSection.vue:25-28`).
- **Pantallas y componentes:**
  - `app/features/foreign-trade/components/DepositConfirmationRequirements.vue` (nuevo): aviso con lo que falta.
  - `app/features/foreign-trade/composables/useConfirmationRequirements.ts` (nuevo).
  - `app/features/foreign-trade/components/TruckManifestDialog.vue` (nuevo).
  - `app/features/foreign-trade/composables/useUpdateTruckManifest.ts` (nuevo).
  - `app/features/foreign-trade/components/DepositDetailGeneralInfoCard.vue` (modifica): fecha del documento en la edición de Borrador.
  - `app/features/foreign-trade/components/DepositExpandedEntriesTable.vue` (modifica): columnas y acción de manifiesto.
  - `app/features/foreign-trade/components/DepositDetailDocumentStakeholdersSection.vue` (modifica): rol Exportador y prop `modalityCode`.
  - `app/pages/foreign-trade/{imports,exports,inspections}/[id]/index.vue` (modifica): requisitos y botón Confirmar.
  - `app/features/foreign-trade/services/foreign-trade-service.ts` y `types/*` (modifica).
- **Diseño de la interacción.**

  **Requisitos para confirmar** (solo en Borrador), debajo del aviso de Borrador:
  - Con `canConfirm = false`: `Message warn` «Para confirmar el depósito {número} falta:» y una lista con cada `missing[].message` (por ejemplo «cliente», «fecha del documento», «peso del manifiesto del camión ABC123»). Cada elemento es un enlace que desplaza la página a su sección:

    | Código | Va a |
    |---|---|
    | `CUSTOMER` | «Cliente» |
    | `DOCUMENT_DATE`, `CURRENCY`, `CARGO_VALUE` | «Información general» |
    | `IMPORTER`, `CUSTOMS_AGENCY`, `EXPORTER` | «Partes del depósito» |
    | `MANIFEST_NUMBER`, `MANIFEST_WEIGHT` | «Entradas al depósito» |
    | `CARGO_UNIT_PRODUCTS`, `CARGO_UNIT_BREAKDOWN` | «Unidades de carga» |

  - Con `canConfirm = true`: `Message success` «El depósito cumple los requisitos para confirmarse.»
  - Botón «Confirmar depósito» del encabezado: deshabilitado mientras `canConfirm` sea `false`; tooltip «Falta: {lista separada por «; »}». Reemplaza `canConfirmDeposit` (`:123`).
  - Si confirmar responde 400 con «No se puede confirmar el depósito {número}. Falta: …», se refrescan los requisitos.

  **Fecha del documento** (en «Información general», con «Editar» en Borrador):

  | Etiqueta | Control | Obligatorio | Validación y mensaje |
  |---|---|---|---|
  | Fecha del documento | `DatePicker` `dd/mm/yy`, máximo hoy | No | Futura: «La fecha del documento no puede ser futura.» 409: el mensaje del backend «Ya existe un depósito abierto con el documento {número} y fecha {dd/MM/yyyy}: {depósito}.» bajo el campo. |

  Se envía junto con moneda, valor y observaciones en el `PATCH …/draft` que ya usa la tarjeta (`useUpdateDraftDeposit`).

  **Manifiesto de cada camión** (tabla «Entradas al depósito», `DepositExpandedEntriesTable`): columnas nuevas «Nro. manifiesto» y «Peso manifiesto (kg)» con «—» si falta, y un ícono de alerta si falta alguno. Acción «Completar manifiesto» (o «Corregir manifiesto» si ya tiene), visible en Borrador y Confirmado. Abre `TruckManifestDialog` con el encabezado «Manifiesto del camión {placa}»:

  | Etiqueta | Control | Obligatorio | Validación y mensaje |
  |---|---|---|---|
  | Nro. de manifiesto | `InputText`, máx. 100 | Sí | «El número de manifiesto es requerido.» / «El número de manifiesto no puede exceder 100 caracteres.» |
  | Peso según manifiesto (kg) | `InputNumber`, 2 decimales | Sí | «El peso del manifiesto debe ser mayor que cero.» |
  | Motivo | `Textarea`, máx. 500 | No | «El motivo no puede exceder 500 caracteres.» |

  Al guardar: aviso «Manifiesto del camión {placa} actualizado». Si `billingRecalculated` es `true`: «Facturación recalculará el período del depósito.» Se cierra el diálogo y se refrescan las entradas y los requisitos.

  **Terceros documentales:** `MANAGED_ROLES` pasa a Importador, Agencia de aduanas (SIA) y Exportador. Al lado de cada rol, la etiqueta «Obligatorio para confirmar» según la modalidad:
  - Importación: importador y agencia;
  - Exportación: exportador;
  - Inspección: ninguno.

  Las páginas pasan `modality-code="IMP" | "EXP" | "INSP"`.
- **Endpoints:**
  - **C-F1-08** `GET foreign-trade/warehouse-storages/{id}/confirmation-requirements` → `{ warehouseStorageId, warehouseStorageNumber, canConfirm, missing: [{ code, message }] }`. Códigos en orden: `CUSTOMER`, `DOCUMENT_DATE`, `IMPORTER`, `CUSTOMS_AGENCY`, `EXPORTER`, `CURRENCY`, `CARGO_VALUE`, `MANIFEST_NUMBER`, `MANIFEST_WEIGHT`, `CARGO_UNIT_PRODUCTS`, `CARGO_UNIT_BREAKDOWN`. 404 «El depósito no existe.»
  - **C-F1-07** `POST foreign-trade/warehouse-storages/{id}/confirm`: sin cambio de forma. 400 nuevo «No se puede confirmar el depósito {número}. Falta: …».
  - **C-F1-05** `PATCH foreign-trade/warehouse-storages/{id}/draft` → `{ customerId, intermediaryId, currency, cargoValue, observations, documentDate }` (`documentDate` nuevo). Errores: «La fecha del documento no puede ser futura.» y 409 de documento duplicado.
  - **C-F1-06** `PATCH foreign-trade/warehouse-storages/{id}/entries/{entryId}/manifest` → `{ manifestNumber, manifestWeight, reason }`. 200 `{ warehouseStorageEntryId, vehiclePlate, manifestNumber, manifestWeight, billingRecalculated }`. Errores: los de la tabla, 400 «Solo se puede completar el manifiesto de un depósito en Borrador o Confirmado.», 404 «El camión no pertenece a este depósito.»
  - **C-F1-04** `PUT foreign-trade/warehouse-storages/{id}/stakeholders` → `{ stakeholders: [{ roleCode: "EXPORTER", stakeholderId }] }`; admite `EXPORTER`.
  - `GET foreign-trade/warehouse-storages/{id}/entries` (existente): cada entrada trae `id`, `vehiclePlate`, `manifestNumber`, `manifestWeight`, `netWeight`, `ticketNumber`, `createdAt` y `entryProducts`. Agregar `manifestNumber` y `manifestWeight` al tipo `IDepositStorageEntryDto` (`features/foreign-trade/types/import-deposit.ts:33-41`).
- **Roles y menú:** sin cambios (`["Admin", "ForeignTrade"]`).
- **Invalidación:** `['foreign-trade']` tras cada mutación (cubre requisitos, detalle y entradas). La consulta de requisitos usa la clave `['foreign-trade', 'confirmation-requirements', warehouseStorageId]`.
- **Pruebas manuales** (Comercio exterior):
  0. Datos: el depósito creado en F1-01 (importación sin fecha, terceros, valor ni manifiesto).
  1. Abrir su detalle. → «Para confirmar el depósito … falta: cliente; fecha del documento; importador; agencia de aduanas; moneda; valor de la mercancía; número de manifiesto del camión TST101; peso del manifiesto del camión TST101». «Confirmar depósito» deshabilitado.
  2. Pulsar «peso del manifiesto del camión TST101». → La página baja a «Entradas al depósito».
  3. Completar el manifiesto. → Desaparecen los dos elementos del camión.
  4. Asignar cliente, importador y agencia, y editar fecha, valor y moneda. → «El depósito cumple los requisitos…» y «Confirmar» habilitado. Confirmar.
  5. Depósito de exportación: falta «exportador»; asignarlo en «Partes del depósito».
  6. Corregir el manifiesto de un camión de un depósito confirmado. → Aviso de recálculo.
  7. Poner una fecha del documento igual a la de otro depósito abierto con el mismo número. → Mensaje 409 bajo el campo.
- **Terminado cuando:** un depósito creado sin los siete datos se completa y se confirma desde el detalle, en las tres modalidades.
- **Riesgo:** un depósito en Borrador bloqueado sin saber por qué. Se mitiga con la lista de requisitos, que es el mismo cálculo del backend.

---

#### F1-08 · Comercio Exterior normaliza productos y reparte unidades de carga (BAS-03, BAS-07, UI-01)

- **Dificultad:** Media.
- **Tarea del operario (Comercio Exterior):** cambiar por el producto correcto del catálogo una línea que báscula digitó como texto libre, y repartir la mercancía de un camión entre sus unidades de carga.
- **Cómo lo hacía en el legacy:** el producto era texto libre en el pesaje (`registrarentradabascula.php:131`) y Comercio Exterior lo asociaba al catálogo al crear el depósito y sus productos en bodega. No capturaba unidades de carga en báscula (`:873-878`).
- **Lo que hace hoy la v2:**
  - la línea del depósito no permite cambiar el producto (`DepositProductsTable.vue`; `UpdateDepositProductCommand` no lo admite);
  - la sección de unidades (`DepositDetailCargoUnitsSection.vue`) corrige unidades pero no reparte;
  - la lista de productos de administración no distingue los creados desde báscula.
- **Pantallas y componentes:**
  - `app/features/foreign-trade/components/ChangeLineProductDialog.vue` (nuevo) y `composables/useChangeLineProduct.ts` (nuevo).
  - `app/features/foreign-trade/components/CargoUnitBreakdownDialog.vue` (nuevo) y `composables/useSetCargoUnitBreakdown.ts` (nuevo).
  - `app/features/foreign-trade/components/DepositProductsTable.vue` (modifica): acción «Cambiar producto».
  - `app/features/foreign-trade/components/DepositDetailCargoUnitsSection.vue` (modifica): acción «Repartir mercancía» por camión.
  - `app/pages/admin/products/index.vue`, `app/features/products/types/product.ts` y su servicio (modifica): filtro y etiqueta.
- **Diseño de la interacción.**

  **Cambiar producto** (acción de la fila de `DepositProductsTable`, solo en Borrador). Diálogo «Cambiar producto de la línea»:
  - Muestra «Producto actual: {nombre}», con la etiqueta «Creado desde báscula» si aplica.

  | Etiqueta | Control | Obligatorio | Validación y mensaje |
  |---|---|---|---|
  | Producto del catálogo | `Select` filtrable con búsqueda diferida (`GET product` con `searchTerm`, `isActive: true`, `pageSize: 20`), opción «{sku} — {name}» | Sí | «Seleccione el producto del catálogo.» |
  | Motivo | `Textarea` | Sí | «El motivo del cambio debe tener entre 10 y 500 caracteres.» |

  Al guardar: aviso «Línea «{previousProductName}» cambiada a «{productName}»». Errores del backend en línea: 409 «El producto «{nombre}» ya tiene una línea en este depósito; corrija esa línea en lugar de cambiar esta.», 400 «La línea ya tiene ese producto.», 400 «No se puede cambiar el producto: la línea {motivo}.»

  **Repartir mercancía** (en «Unidades de carga», solo en Borrador). Por cada camión con dos o más unidades, se agrupan sus unidades (por `warehouseStorageEntryId` de cada unidad) y se agrega el botón «Repartir mercancía del camión {placa}», con un aviso «Sin repartir» si alguna unidad no tiene líneas. El diálogo «Reparto de la mercancía del camión {placa}» muestra:
  - una tabla de solo lectura con lo declarado del camión por producto, tomado de `GET foreign-trade/warehouse-storages/{id}/entries` (`entryProducts`);
  - por cada unidad, una fila por producto del camión con «Cantidad en {placa de la unidad}» (`InputNumber`, ≥ 0);
  - el pie por producto: «Repartido {x} de {y}» en rojo si no cuadra;
  - «Motivo» (`Textarea`).

  Validaciones en el frontend antes de enviar:
  - suma por producto distinta de lo declarado: «La suma de «{producto}» en las unidades ({x}) no coincide con lo declarado del camión ({y}).»;
  - una unidad sin cantidades: «La unidad de carga {placa} no tiene mercancía.»;
  - motivo fuera de rango: «El motivo debe tener entre 10 y 500 caracteres.»

  Se envían solo las cantidades > 0. Al guardar: aviso «Mercancía repartida entre las unidades del camión {placa}.»

  **Administración › Productos:** filtro `Checkbox` «Solo creados desde báscula» (query `createdFromWeighbridge=true`) y columna «Origen» con la etiqueta «Báscula» cuando `createdFromWeighbridge` es `true`.
- **Endpoints:**
  - **C-F1-10** `PUT foreign-trade/deposits/{id}/products/{storageProductId}/catalog-product` → `{ productId, reason }`. 200 `{ warehouseStorageProductId, productId, productName, previousProductName }`. Errores: los citados, más 400 «Solo se pueden editar los productos de un depósito en Borrador.» y 404 «El producto del catálogo no existe o está inactivo.» `{id}` es el `warehouseStorageId` y `{storageProductId}` el id de la línea (`WarehouseStorageProduct`), los mismos que ya usa `updateDepositProduct` (`foreign-trade-service.ts:560-566`).
  - **C-F1-11** `PUT foreign-trade/warehouse-storages/{id}/entries/{entryId}/cargo-unit-breakdown` → `{ units: [{ warehouseStorageCargoUnitId, products: [{ warehouseStorageProductId, declaredQuantity }] }], reason }`. 200: las unidades del camión (`CargoUnitDto`). Errores: los de la validación, más «Envíe el reparto de todas las unidades de carga del camión.», ««{producto}» no está declarado en este camión.», «No se puede cambiar la mercancía de la unidad {placa}: tiene cantidades reservadas o despachadas.»
  - **C-F1-09** `GET product?createdFromWeighbridge=true`; `ProductDto.createdFromWeighbridge: boolean`.
  - `GET foreign-trade/warehouse-storages/{id}/cargo-units` (existente): cada unidad trae `warehouseStorageEntryId`, `arrivalVehiclePlate`, `plateNumber` y `products`.
- **Roles y menú:** detalle del depósito sin cambios. Productos: `["Admin"]`, sin cambios.
- **Invalidación:** `['foreign-trade']` tras ambos cambios; `['products']` no cambia.
- **Pruebas manuales:**
  1. En el depósito con «PAPA CRIOLLA ROJA» (F1-02), «Cambiar producto» por «PAPA» del catálogo con motivo. → La línea muestra «PAPA».
  2. Cambiar a un producto que ya tiene otra línea. → Mensaje 409.
  3. Depósito con dos contenedores sin reparto (F1-03, prueba 2). → «Sin repartir» y el requisito «reparto de …» en F1-07. Repartir 6 y 4 de 10. → Desaparece el requisito.
  4. Repartir 6 y 3. → «La suma … (9) no coincide … (10).» sin llamar al backend.
  5. Administración › Productos › «Solo creados desde báscula». → Aparece «PAPA CRIOLLA ROJA» con la etiqueta «Báscula».
- **Terminado cuando:** Comercio Exterior normaliza una línea libre y reparte un camión con varias unidades, y el depósito confirma.
- **Riesgo:** una tarifa distinta por producto. El backend recalcula; el frontend solo invalida.

---

#### F1-09 · Cronometraje con el operario (ROADMAP 1.8, DF2)

- **Dificultad:** Muy alta (es la medición de la fase). No hay código.
- **Tarea:** comprobar con el operario que la v2 registra un camión de importación en un tiempo igual o menor que el legacy.
- **Preparación:**
  - Backend y frontend de `develop` con los ítems F1-01 a F1-08 con commit, en el equipo de báscula o uno equivalente (mismo monitor, teclado y red).
  - Legacy en su ambiente habitual.
  - Un juego de datos igual para los dos sistemas: placa `MED001` (y `MED002` para el segundo camión), conductor y transportadora ya registrados, documento `CP-MED-{n}` (número nuevo en cada corrida), producto existente «CEBOLLA», embalaje «BULTO», cantidad 300, peso según manifiesto 18.000 kg, peso bruto 30.000 kg y pago en efectivo de un total de 23.000 con un billete de 50.000.
  - En la v2, Vigilancia registra el ingreso de la placa antes de cada corrida, con motivo «Descargue mercancia importacion». Ese tiempo no se cuenta: es otro operario.
  - El operario hace dos corridas de práctica en cada sistema antes de medir.
  - Cronómetro de mano o grabación de pantalla.
- **Guion del escenario 1 — camión nuevo, documento nuevo:**

  | Paso | Legacy (`registrarentradabascula.php`) | v2 (banco de trabajo) |
  |---|---|---|
  | Inicio del cronómetro | Clic en «Nueva Entrada» | Clic (o Enter) en el camión de la cola |
  | 1 | Placa, país (automático), conductor y transportadora (diálogos) | — (los trae Vigilancia) |
  | 2 | Modalidad Importación (por defecto), Doc. comercial, Nro. documento | Modalidad y tipo precargados; Nro. documento |
  | 3 | Manifiesto PreImp. | Nro. de manifiesto |
  | 4 | P. Indicador (30.000), P. manifiesto (18.000) | Peso según manifiesto (18.000) |
  | 5 | Producto, embalaje y cantidad | Producto (sugerencia), embalaje, cantidad |
  | 6 | «Insertar registro» | Enter (Guardar) |
  | 7 | Cobro: efectivo 50.000, «Guardar» | Efectivo 50.000, Enter (Cobrar) |
  | 8 | «¿Desea Imprimir Ahora?» → Aceptar | Peso 30.000, Enter (Registrar peso) |
  | Fin del cronómetro | Tiquete impreso | «Peso registrado» visible y «Salir y atender otro camión» pulsado |

- **Guion del escenario 2 — segundo camión del mismo documento:** igual que el escenario 1, con `MED002` y el mismo documento de la corrida anterior. En el legacy, el documento se elige de la lista del autocompletar; en la v2, se digita y el banner dice «Se asociará al depósito …». Se cronometra solo el segundo camión.
- **Tramo B (sin meta):** en la v2, del camión tomado de «Por repesar» a «Imprimir Ticket». Se anota para saber cuánto agrega el repesaje; no entra en el criterio de salida (DF2).
- **Registro:** tres corridas por escenario y sistema. Tabla con escenario, sistema, corrida, segundos, errores del operario y comentarios. Se usa la **mediana**.
- **Criterio:** v2 ≤ legacy en la mediana de los dos escenarios, y el visto bueno verbal del operario anotado con su nombre y la fecha.
- **Si no se cumple:** se anota en qué paso se pierde el tiempo (con la grabación) y se hace un ítem de ajuste en `develop` (con su commit) antes de cerrar la fase. No se pasa a la fase 2 sin la medición aprobada (riesgo n.º 1 del roadmap).
- **Entregable:** `code_workspace/ajustes/medicion-bascula-fase1.md` con la tabla y la conclusión, que sube el implementador o el usuario. No se publica en otro lugar.
- **Terminado cuando:** el archivo de la medición registra las medianas de los dos escenarios en ambos sistemas, con v2 ≤ legacy, y el visto bueno del operario.
- **Riesgo:** medir en condiciones distintas (equipo, red, datos). Se mitiga con el mismo equipo y el mismo juego de datos, dos corridas de práctica y la mediana de tres.

---
### C.2 Fase 2 — Control aduanero

> **Estado: ✅ COMPLETADA en código (2026-10-01).** F2-01 a F2-08 implementados en `develop` (sin commit: lo hace el usuario). `npm run build` OK. Lint al cerrar la fase: **306 errores** (tope 310) y 0 errores en los archivos nuevos; la fase 3 usa 306 como tope. Pendiente fuera del código: pruebas manuales en el navegador contra el backend local (`afe6e8f` y migraciones de la fase 2) y la medición F1-09 que esta fase exigía antes de empezar (§E.1, regla 5).

- **Objetivo:** Comercio Exterior no puede despachar más de lo nacionalizado por producto, gestiona los levantes como en el legacy y ve a tiempo los depósitos que van a caer en abandono.
- **Criterio de salida (desde el operario):**
  1. Al crear una orden de cargue de importación, cada producto se limita a lo nacionalizado disponible y la ciudad de destino se elige de un catálogo.
  2. La guía calcula sola su vencimiento con los días de tránsito de la ciudad.
  3. Comercio Exterior retira un levante equivocado, registra el FOB una vez por levante y no puede repetir un número de levante en otro depósito.
  4. El tablero de Comercio Exterior avisa cuántos depósitos están en alerta o en abandono; desde ahí se registra la prórroga.
  5. Los dos reportes de abandono se consultan con sus filtros.
- **Rama:** `develop` (DF1). **Empieza cuando la fase 1 tiene todos sus ítems con commit y la medición aprobada** (toca `foreign-trade-service.ts`, los tipos y `pages/foreign-trade/imports/[id]/index.vue`, que la fase 1 modifica).
- **Backend que debe estar corriendo:** commit `afe6e8f` (fase 2) con las migraciones `ParidadF2_03_IndiceAceptacion`, `ParidadF2_05_FobLevante`, `ParidadF2_06_Ciudades`, `ParidadF2_07_CiudadDestinoOrden` y `ParidadF2_08_Prorroga`.
- **Advertencia de compatibilidad:** el backend de `develop` ya exige `destinationCityId` al crear órdenes de cargue (C-F2-03). Hasta que esta fase esté en `develop`, crear una orden de cargue falla contra ese backend. El catálogo de ciudades arranca vacío: F2-01 va primero.
- **Dificultad:** **Alta.** Cambia la orden de cargue (un formulario de 1.024 líneas) y el formulario de levantes, con reglas aduaneras.
- **Perfil de agente:** agente capaz, con revisión humana del diff y prueba en el navegador.

---

#### F2-01 · Catálogo de ciudades con días de tránsito (UI-10, GAP-025)

- **Dificultad:** Media.
- **Tarea del operario (Administrador):** mantener las ciudades de destino con sus días de tránsito y marcar las que son destino de abandono; cargar el catálogo del legacy.
- **Cómo lo hacía en el legacy:** «Configuración › Ciudades». El formulario pedía País, Nombre Ciudad, Departamento y «# días» (`modulos/mod_ciudades/registrarciudad.php:165-215`). El listado mostraba «No., ciudad / destino, DEPTO., pais, dias» (`listarciudades.php:124-130`).
- **Lo que hace hoy la v2:** no existe; el destino es texto libre (`features/foreign-trade/components/LoadingOrderForm.vue:129,946-952`).
- **Pantallas y componentes:**
  - `app/pages/admin/cities/index.vue` (nuevo): copia el patrón de `pages/admin/packaging-types/index.vue`.
  - `app/features/administration/types/city.ts` (nuevo): `ICity`, peticiones y resultado de la importación.
  - `app/features/administration/services/administration-service.ts` (modifica): `getCities`, `createCity`, `updateCity`, `deleteCity`, `importCities`.
  - `app/features/administration/composables/useCities.ts` (nuevo) y `useMutationsCities.ts` (nuevo).
  - `app/features/administration/components/CityImportDialog.vue` (nuevo).
  - `app/composables/useApi.ts` (modifica): método `postForm<R>(ruta, formData)` que llama a `$api.post(ruta, formData, { headers: { 'Content-Type': 'multipart/form-data' } })`. Es necesario: la instancia fija `Content-Type: application/json` (`plugins/api-client.ts:24-26`) y axios convierte un `FormData` en JSON con esa cabecera. Lo usan también F4-04.
  - `app/components/layout/AppMenu.vue` (modifica): entrada «Ciudades» en Administración.
- **Diseño de la interacción.**

  **Listado** («Ciudades»): `AppTable` con buscador («Buscar ciudad», diferido 300 ms, query `search`), filtro «Estado» (Activas, Inactivas, Todas) y filtro «Destino de abandono» (Todos, Sí, No). Columnas: «Ciudad», «Departamento», «País», «Días de tránsito» («—» si es nulo), «Destino de abandono» (Sí/No), «Estado» (`Tag` Activa/Inactiva), «Acciones» (Editar, Eliminar). Paginado de 10, 20 o 50. Vacío: «No hay ciudades. Créelas o impórtelas del legacy.» Botones «Nueva ciudad» e «Importar del legacy».

  **Diálogo «Nueva ciudad» / «Editar ciudad»:**

  | Etiqueta | Control | Obligatorio | Validación y mensaje |
  |---|---|---|---|
  | Nombre | `InputText`, mayúsculas, máx. 35 | Sí | «El nombre de la ciudad es obligatorio y no puede exceder 35 caracteres.» |
  | País | `InputText`, 3 letras en mayúsculas (COL, ECU) | Sí | «El país debe ser un código de 3 letras.» |
  | Departamento | `InputText`, máx. 20 | No | «El distrito no puede exceder 20 caracteres.» |
  | Días de tránsito | `InputNumber` entero, 0 a 99 | No | «Los días de tránsito deben estar entre 0 y 99.» |
  | Destino de abandono | `Checkbox` | — | Ayuda: «Las salidas a esta ciudad aparecen en el reporte de salidas a destino de abandono.» |
  | Activa | `ToggleSwitch` (solo al editar) | — | — |

  Al guardar: aviso «Ciudad guardada». 409 «Ya existe la ciudad {nombre} ({país}, {distrito}).» bajo «Nombre».

  **Eliminar:** confirmación «¿Eliminar la ciudad {nombre}?». 409 «La ciudad está en uso en órdenes de cargue; desactívela en lugar de eliminarla.»: el aviso global la muestra.

  **Importar del legacy** (`CityImportDialog`):

  | Etiqueta | Control | Obligatorio | Validación y mensaje |
  |---|---|---|---|
  | Archivo CSV | `FileUpload` modo básico, `accept=".csv"` | Sí | «Seleccione el archivo CSV de ciudades.» |
  | Filas de encabezado | `InputNumber` entero ≥ 0, por defecto 1 | Sí | — |

  - Ayuda: «Columnas en orden: id_ciudad;nom_ciudad;id_pais;distrito;dias. Separador ; o ,.»
  - Botón «Simular»: `dryRun=true`. Muestra «Filas: {totalRows} · Se crean: {created} · Se actualizan: {updated}» y la tabla de errores «Fila» / «Error» con los `errors[]`.
  - Botón «Importar» (habilitado tras una simulación sin errores, o con errores si el operario marca «Importar aunque haya filas con error»): `dryRun=false`. Aviso «Ciudades importadas: {created} creadas, {updated} actualizadas».
- **Endpoints (C-F2-07):**
  - `GET administration/cities` (query `search`, `countryCode`, `isActive`, `isAbandonmentDestination`, `pageIndex`, `pageSize`, `all`) → `CityDto[]`: `{ id, legacyId, name, countryCode, district, transitDays, isAbandonmentDestination, isActive, createdAt, updatedAt }`.
  - `POST administration/cities` → `{ name, countryCode, district?, transitDays?, isAbandonmentDestination }`; 201 `CityDto`.
  - `PUT administration/cities/{id}` → lo mismo más `isActive`; 200 `CityDto`.
  - `DELETE administration/cities/{id}` → 204.
  - `POST administration/cities/import` (multipart: `file`, `headerRows`, `dryRun`) → `{ dryRun, totalRows, created, updated, errors: [{ row, message }] }`.
  - Lectura para cualquier usuario autenticado; escritura `AdminOnly`.
- **Roles y menú:** `requiredRoles: ["Admin"]`. Menú: Administración › «Ciudades», ícono `fa-city`, `to: "/admin/cities"`.
- **Invalidación:** `['administration', 'cities']` tras crear, editar, eliminar o importar. Clave de la consulta: `['administration', 'cities', params]`.
- **Pruebas manuales** (Administrador):
  1. Crear «PASTO», COL, NARIÑO, 1 día. → Aparece en el listado.
  2. Crear otra vez «PASTO» con los mismos datos. → Mensaje 409.
  3. Importar un CSV de tres filas con una fila sin nombre. → Simular muestra 1 error «Fila n: …»; importar crea las otras dos.
  4. Marcar «TULCAN» como destino de abandono. → La columna dice «Sí».
  5. Entrar con Comercio exterior a `/admin/cities`. → Acceso denegado (regla actual de `requiredRoles`).
- **Terminado cuando:** el administrador crea, edita, desactiva, elimina e importa ciudades, y el select de F2-02 las muestra.
- **Riesgo:** catálogo vacío el día del corte. Se mitiga con la importación del CSV de la fase 0.4 del roadmap.

---

#### F2-02 · Ciudad de destino de la orden de cargue (UI-10, GAP-025)

- **Dificultad:** Media.
- **Tarea del operario (Comercio Exterior):** elegir la ciudad de destino de la salida de una lista, sin variantes del mismo lugar.
- **Cómo lo hacía en el legacy:** la salida elegía la ciudad del catálogo (`modulos/mod_salidas/registrarsalida.php`, `id_ciudaddestino`).
- **Lo que hace hoy la v2:** texto libre «Ciudad de Destino» (`LoadingOrderForm.vue:946-952`), enviado como `destinationCity` (`:410`).
- **Pantallas y componentes:**
  - `app/features/foreign-trade/components/LoadingOrderForm.vue` (modifica).
  - `app/features/foreign-trade/types/loading-order.ts` (modifica): `ICreateLoadingOrderRequest.destinationCityId: string`; quitar `destinationCity` del envío; `destinationCityId: string | null` en la lectura.
  - Usa `useCities` (F2-01).
- **Diseño de la interacción:** en «Destino y Programación», el campo pasa a ser:

  | Etiqueta | Control | Obligatorio | Validación y mensaje |
  |---|---|---|---|
  | Ciudad de destino | `Select` filtrable; opciones de `GET administration/cities?isActive=true&all=true`; etiqueta «{name} ({district}, {countryCode})» | Sí | «Seleccione la ciudad de destino.» |

  - Debajo, la ayuda «Tránsito: {transitDays} días» o «Sin días de tránsito: el vencimiento de la guía se digitará.»
  - Catálogo vacío: `Message warn` «No hay ciudades activas. Pida al administrador cargarlas en Administración › Ciudades.» y el botón de crear la orden deshabilitado.
  - El campo entra en `isValid` del formulario. Errores del backend: 400 «Seleccione la ciudad de destino.», 404 «La ciudad de destino no existe o está inactiva.»
- **Endpoints:**
  - **C-F2-03** `POST foreign-trade/loading-orders`: `destinationCityId` obligatorio; el texto `destinationCity` se ignora.
  - **C-F2-09** lectura de órdenes: `destinationCityId` nuevo; `destinationCity` sigue siendo el nombre.
  - **C-F2-07** `GET administration/cities`.
  - `POST warehouse/loading-orders` (C-F2-08) no tiene pantalla: `useLoadingOrderCreate` (`features/warehouse/composables/useLoadingOrderMutations.ts:25-46`) no se usa. No se toca (§G).
- **Roles y menú:** sin cambios. **Invalidación:** la actual de `useCreateLoadingOrder` (`['foreign-trade']`).
- **Pruebas manuales** (Comercio exterior):
  1. Crear una orden sin ciudad. → «Seleccione la ciudad de destino.» y no envía.
  2. Elegir «PASTO (NARIÑO, COL)». → «Tránsito: 1 días»; la orden se crea y su detalle dice «PASTO».
  3. Con el catálogo sin ciudades activas. → Aviso y botón deshabilitado.
- **Terminado cuando:** toda orden nueva lleva una ciudad del catálogo.
- **Riesgo:** bajo.

---

#### F2-03 · Tope de despacho por lo nacionalizado de cada producto (UI-04, GAP-002)

- **Dificultad:** Media.
- **Tarea del operario (Comercio Exterior):** que la orden no deje sacar más de lo que tiene levante, producto por producto.
- **Cómo lo hacía en el legacy:** la salida comparaba la cantidad con el disponible nacionalizado de cada producto (`modulos/mod_salidas/registrarsalida.php:231-243,582-735`; `listarproductosajax.php:9-18`).
- **Lo que hace hoy la v2:** limita por el disponible de stock (`LoadingOrderForm.vue:452,461,794-803`), y el depósito quedaba «Nacionalizado» con el primer levante de cualquier producto.
- **Pantallas y componentes:**
  - `app/features/foreign-trade/components/LoadingOrderForm.vue` (modifica).
  - `app/features/foreign-trade/types/loading-order-deposit.ts` (modifica): `ILoadingOrderDepositProductDto` agrega `nationalizedQuantity: number | null` y `nationalizedAvailable: number | null`.
- **Diseño de la interacción.**
  - En la lista de productos del depósito, cada opción muestra, además de «Disponible: {availableStock}», la línea «Nacionalizado disponible: {nationalizedAvailable}» cuando no es nulo (importación).
  - Una opción con `nationalizedAvailable = 0` queda deshabilitada, con la etiqueta «Sin levante».
  - El máximo del campo «Cantidad» es el menor entre el disponible (o el disponible de la unidad de carga) y `nationalizedAvailable` (si no es nulo). Ayuda: «Máximo: {tope} {unidad} (lo nacionalizado disponible)» cuando el tope es el nacionalizado.
  - La suma de un mismo producto en varias líneas (por ejemplo, de varias unidades de carga) no puede pasar `nationalizedAvailable`: «La cantidad supera lo nacionalizado disponible ({tope} {unidad}). Registre el levante antes de despachar.»
  - Error del backend: 400 «La cantidad solicitada de «{producto}» en el depósito {número} ({solicitado}) supera lo nacionalizado disponible ({disponible}). Registre el levante antes de despachar.»
  - Exportación e inspección: sin cambios (los dos campos llegan nulos).
- **Endpoints:**
  - **C-F2-04** `GET foreign-trade/loading-orders/deposits`: cada producto agrega `nationalizedQuantity` y `nationalizedAvailable` (nulos fuera de importación).
  - **C-F2-03**: el error de tope.
- **Roles y menú:** sin cambios. **Invalidación:** sin cambios.
- **Pruebas manuales** (Comercio exterior):
  0. Datos: depósito de importación confirmado con dos productos de 100 cada uno; levante de 30 solo para el primero.
  1. Crear una orden. → El primero muestra «Nacionalizado disponible: 30» y el segundo está deshabilitado con «Sin levante».
  2. Pedir 31 del primero. → Mensaje del tope y no se agrega.
  3. Pedir 30. → Se crea la orden.
  4. Depósito de exportación. → Sin líneas de nacionalizado y el tope es el disponible.
- **Terminado cuando:** no se puede armar una orden de importación que supere lo nacionalizado de un producto.
- **Riesgo:** bajo. El backend repite la regla.

---

#### F2-04 · Vencimiento de la guía calculado por la ciudad (UI-10, GAP-025)

- **Dificultad:** Baja.
- **Tarea del operario (Comercio Exterior):** emitir la guía sin calcular a mano su vencimiento.
- **Cómo lo hacía en el legacy:** vencimiento = fecha de la guía + los días de la ciudad de destino (`modulos/mod_salidas/verguia.php:705-721`; también `autorizarcargue.php:579-583`).
- **Lo que hace hoy la v2:** «Fecha de Vencimiento *» se digita siempre (`features/foreign-trade/components/DispatchGuideForm.vue:57,78,94,198-200`).
- **Pantallas y componentes:** `DispatchGuideForm.vue` (modifica); `features/foreign-trade/types/dispatch-guide.ts` (modifica: `expirationDate?: string | null`); usa `useCities`.
- **Diseño de la interacción:**
  - Con la orden elegida, se busca su `destinationCityId` en el catálogo de ciudades (`all=true`, activas e inactivas).
  - **Ciudad con `transitDays` > 0:** el campo de vencimiento se reemplaza por el texto de solo lectura «Vence el {dd/MM/yyyy HH:mm}: {transitDays} días de tránsito a {ciudad}», con la fecha = salida + días, a la misma hora. Se recalcula al cambiar la fecha de salida. Se envía `expirationDate: null`.
  - **Ciudad sin días, u orden sin ciudad:** el campo «Fecha de vencimiento» es obligatorio, con la ayuda «La ciudad {nombre} no tiene días de tránsito: digite el vencimiento.» o «La orden no tiene ciudad de destino: digite el vencimiento.» Validación: «La fecha de vencimiento debe ser posterior a la fecha de salida.»
- **Endpoints:** **C-F2-10** `POST foreign-trade/dispatch-guides`: `expirationDate` opcional. Errores: «Indique la fecha de vencimiento: la ciudad de destino {nombre} no tiene días de tránsito.», «Indique la fecha de vencimiento: la orden no tiene ciudad de destino.», «La fecha de vencimiento debe ser posterior a la fecha de salida.» **C-F2-09:** la orden trae `destinationCityId`.
- **Roles y menú:** sin cambios. **Invalidación:** sin cambios (`['foreign-trade']`).
- **Pruebas manuales:**
  1. Guía de una orden a «PASTO» (1 día), con salida hoy a las 10:00. → «Vence el {mañana} 10:00…»; se emite y el PDF muestra ese vencimiento.
  2. Orden creada antes de F2-02 (sin ciudad). → Pide la fecha.
- **Terminado cuando:** con ciudad y días, la guía no pide el vencimiento.
- **Riesgo:** bajo.

---

#### F2-05 · Retirar un levante (UI-06, GAP-009)

- **Dificultad:** Media.
- **Tarea del operario (Comercio Exterior):** quitar un levante registrado por error.
- **Cómo lo hacía en el legacy:** ícono «Eliminar» en cada levante del depósito (`modulos/mod_levantes/registrarlevante.php:540-545`), con eliminación por producto (`eliminarproductolevante.php:51-58`) y del levante (`eliminarlevante.php`).
- **Lo que hace hoy la v2:** solo «Editar levante» (`pages/foreign-trade/imports/[id]/index.vue:535-539`).
- **Pantallas y componentes:**
  - `app/features/foreign-trade/components/WithdrawReleaseDialog.vue` (nuevo).
  - `app/features/foreign-trade/composables/useWithdrawRelease.ts` (nuevo).
  - `app/pages/foreign-trade/imports/[id]/index.vue` (modifica): acción por fila.
  - `foreign-trade-service.ts` (modifica).
- **Diseño de la interacción:** en la tabla «Levantes», ícono «Retirar levante» (`pi pi-trash`, `severity="danger"`, tooltip «Retirar levante»), visible si el depósito no está anulado. Diálogo «Retirar levante {releaseNumber} de «{producto}»»:
  - Texto: «El levante deja de nacionalizar esta mercancía. Si el depósito queda sin nacionalizar, reimprima la etiqueta.»
  - Campo «Motivo»: `Textarea`, obligatorio. «El motivo del retiro debe tener entre 10 y 500 caracteres.»
  - Botones «Cancelar» y «Retirar levante» (`severity="danger"`).
  - Al retirar: aviso «Levante retirado» y se muestra el aviso actual de reimprimir la etiqueta (`showLabelHint = true`).
  - 409 «No se puede retirar el levante: ya se despacharon o reservaron {x} unidades nacionalizadas de «{producto}». Revierta o cancele primero la salida.»: bajo el motivo.
- **Endpoints:** **C-F2-05** `POST foreign-trade/imports/{importWarehouseStorageId}/releases/{releaseId}/withdraw` → `{ reason }`. 200: el detalle del depósito de importación. Errores: 400 «No se pueden retirar levantes de un depósito anulado.», 400 del motivo, 404 «El levante no existe o no pertenece a este depósito.» y el 409 citado. `{importWarehouseStorageId}` es el `id` de la ruta de la página (`depositId`).
- **Roles y menú:** sin cambios. **Invalidación:** `['foreign-trade']`.
- **Pruebas manuales:**
  1. Retirar un levante sin salidas. → Desaparece de la tabla, baja «Nacionalizado» y aparece el aviso de la etiqueta.
  2. Retirar un levante cuya mercancía tiene una orden pendiente. → Mensaje 409.
  3. Motivo de 5 caracteres. → Botón deshabilitado y el mensaje.
- **Terminado cuando:** un levante se retira con motivo y la nacionalización del depósito se actualiza.
- **Riesgo:** retirar el levante equivocado. Se mitiga con el diálogo que nombra número y producto.

---

#### F2-06 · FOB y tasa del levante, varios productos por levante y levante repetido (UI-19, GAP-009, RN-060, DF4)

- **Dificultad:** Alta.
- **Tarea del operario (Comercio Exterior):** registrar el levante de la DIAN con su FOB en dólares, para un depósito con varios productos, sin repetir números de otro depósito.
- **Cómo lo hacía en el legacy:** un formulario por levante (`registrarlevante.php:592-645`):
  - Tasa Cambio (prellenada con la del día);
  - «CIF USD» (es el FOB en dólares, `fob_dolares`);
  - Peso Bruto (Kg); Fecha (hoy); Nro. Levante; Nro. Aceptación;
  - FOB CO calculado (tasa × FOB);
  - una columna de cantidad por cada producto con saldo, prellenada con el saldo;
  - un solo envío.

  Rechazaba un número de levante o de aceptación ya registrado (`:301`).
- **Lo que hace hoy la v2:** `ReleaseForm.vue` registra un producto por envío, sin FOB ni tasa. El tope es el mínimo entre stock y recibido (`:49-55`).
- **Pantallas y componentes:**
  - `app/features/foreign-trade/components/ReleaseForm.vue` (modifica).
  - `app/pages/foreign-trade/imports/[id]/index.vue` (modifica): columnas FOB y acción «Registrar otro producto con este levante».
  - `app/features/foreign-trade/types/import-deposit.ts` (modifica): `IImportReleaseDto` agrega `fobUsd`, `exchangeRate`, `exchangeRateSource`, `exchangeRateDate` y `fobCop`; `IRegisterReleaseRequest` agrega `fobUsd?: number | null` y `manualExchangeRate?: number | null`. El detalle agrega `extensionRegisteredAt`, `extensionRegisteredByName` y `extensionNotes` (lo usa F2-07).
- **Diseño de la interacción.** Campos del formulario, en este orden:

  | Etiqueta | Control | Obligatorio | Validación y mensaje |
  |---|---|---|---|
  | Producto del depósito | `Select` (actual) | Sí | — |
  | Número de levante | `InputText` (actual) | Sí | 409 bajo el campo: «El número de levante {n} ya está registrado en el depósito {m}.» o «El levante {n} ya está registrado para este producto.» |
  | Fecha de levante | `DatePicker` (actual) | Sí | — |
  | Número de aceptación | `InputText` (actual) | Sí | 409 bajo el campo: «El número de aceptación {a} ya está registrado en el depósito {m}.», o los de par número–aceptación del contrato. |
  | Fecha de aceptación | `DatePicker` (actual) | Sí | — |
  | Levante total del saldo disponible | `Checkbox` (actual) | — | — |
  | Peso (kg) | `InputNumber` (actual) | Sí | — |
  | Cantidad ({unidad}) | `InputNumber`. **Máximo = recibido del producto − otros levantes del producto** (ya no el stock). | Sí | «La cantidad a levantar ({q}) supera lo pendiente por nacionalizar del producto ({p}).» |
  | FOB del levante (USD) | `InputNumber`, 2 decimales, mínimo 0 | No | Negativo: «El FOB no puede ser negativo.» Ayuda: «Valor FOB en dólares; la tasa es la TRM de la DIAN del día y queda fija.» |
  | Tasa de cambio (COP por USD) | `InputNumber` > 0, 2 decimales. **Solo aparece** cuando el backend respondió «No se pudo consultar la TRM de la DIAN. Digite la tasa de cambio para registrar el FOB.» | Sí cuando aparece | «Digite la tasa de cambio.» Ayuda: «La DIAN no respondió: digite la TRM del día.» |
  | Observaciones | `Textarea` (actual) | No | — |

  - **Edición:** el FOB es editable. Si el levante ya tiene tasa, se muestra en solo lectura: «Tasa: {exchangeRate} ({DIAN o Manual}, {dd/MM/yyyy}). No cambia al editar el FOB.» FOB en 0 o vacío borra el FOB.
  - **Levante de varios productos (DF4):** tras registrar, en vez de cerrar, el diálogo muestra «Levante {n} registrado para «{producto}»» y dos botones: «Registrar otro producto con este levante» y «Terminar».
    - El primero reinicia el formulario con número, fechas y aceptación copiados, el siguiente producto con saldo preseleccionado y el FOB vacío.
    - Si ya existe un registro de ese número de levante con `fobUsd` > 0, bajo el FOB aparece: «El FOB del levante {n} ya se registró con «{producto}» ({fobUsd} USD). Déjelo vacío para no sumarlo dos veces en el informe de pólizas.»
  - **Tabla «Levantes»** del detalle: columnas nuevas «FOB (USD)», «Tasa» y «FOB (COP)», con «—» si no hay FOB.
  - **Visibilidad del botón «Registrar Levante»** (`canRegisterRelease`, `imports/[id]/index.vue:289-311`): usa el nuevo tope (recibido − levantes), no el stock.
- **Endpoints:**
  - **C-F2-01** `POST foreign-trade/imports/{id}/releases` → `{ warehouseStorageProductId, releaseNumber, releaseDate, acceptanceNumber, acceptanceDate, releasedQuantity, releasedWeight, observations, fobUsd, manualExchangeRate }`. Errores: los de la tabla. Se elimina «El depósito ya está completamente nacionalizado.» Se permite el mismo número y aceptación para **otro producto** del mismo depósito.
  - **C-F2-02** `PATCH foreign-trade/imports/{id}/releases/{releaseId}`: lo mismo, más 409 «No se puede reducir el levante: ya se despacharon o reservaron {x} unidades nacionalizadas de «{producto}». Revierta o cancele primero la salida.»
  - **C-F2-06** `GET foreign-trade/imports/{id}`: cada levante trae `fobUsd`, `exchangeRate`, `exchangeRateSource` (`Dian` o `Manual`), `exchangeRateDate` y `fobCop`.
- **Roles y menú:** sin cambios. **Invalidación:** `['foreign-trade']` (la actual de `useRegisterRelease` y `useUpdateImportRelease`).
- **Pruebas manuales:**
  1. Registrar el levante `LEV-1` con FOB 1.000 para el producto A. → La fila muestra FOB 1.000, la tasa del día y FOB en pesos.
  2. «Registrar otro producto con este levante». → Número, fechas y aceptación copiados, el producto B preseleccionado, el FOB vacío y el aviso de FOB ya registrado. Registrar.
  3. En otro depósito, registrar `LEV-1`. → «El número de levante LEV-1 ya está registrado en el depósito …» bajo el campo.
  4. Con la DIAN sin respuesta (pedir al usuario que desconecte la red del backend o use un ambiente sin acceso), registrar con FOB. → Aparece «Tasa de cambio»; digitarla y registrar. → Tasa «Manual».
  5. Editar el FOB de `LEV-1` a 2.000. → La tasa no cambia y el FOB en pesos se recalcula.
  6. Producto con 100 recibidos, 80 en stock (20 despachados) y 0 levantes. → El máximo es 100, no 80.
- **Terminado cuando:** el levante registra el FOB una vez, admite varios productos con el mismo número y rechaza el repetido en otro depósito.
- **Riesgo:** doble conteo del FOB en pólizas. Se mitiga con el aviso de DF4.

---

#### F2-07 · Prórroga y abandono: pantalla, aviso y registro (UI-05, GAP-003)

- **Dificultad:** Media.
- **Tarea del operario (Comercio Exterior):** saber qué depósitos con mercancía sin nacionalizar se acercan al plazo de abandono (30 días, o 60 con prórroga) y registrar la prórroga.
- **Cómo lo hacía en el legacy:**
  - el panel inicial mostraba una alerta clicable cuando había depósitos entre 20 y 30 días sin prórroga o entre 50 y 60 con prórroga (`menus/evaluaabandonos.php:4-18`);
  - la pantalla «Prorrogas» (`modulos/mod_depositos/listardepositosprorroga.php`) listaba con las columnas Fecha (días transcurridos), FALTAN, prórroga, depósito, Detalles, Relación de Mercancía (Ingreso, Nacionalizados, Por nacionalizar, Despachados, Existencias) y PRORROGA (`:346-355`), en rojo cuando faltaba poco (`:390-400`);
  - el botón «Solicitar» (`:751-754`) pedía confirmación: «Está seguro de solicitar prorroga para el depósito #{n}. Al Aceptar no se puede deshacer la solicitud» (`:271`) y marcaba la prórroga (`registrarprorroga.php:34-41`).
- **Lo que hace hoy la v2:** nada.
- **Pantallas y componentes:**
  - `app/pages/foreign-trade/abandonment/index.vue` (nuevo): «Abandono y prórrogas».
  - `app/features/foreign-trade/components/RegisterExtensionDialog.vue` (nuevo).
  - `app/features/foreign-trade/components/AbandonmentSummaryAlert.vue` (nuevo): aviso del tablero.
  - `app/features/foreign-trade/composables/useAbandonment.ts` (nuevo: listado y resumen) y `useRegisterExtension.ts` (nuevo).
  - `app/features/foreign-trade/types/abandonment.ts` (nuevo).
  - `app/pages/foreign-trade/index.vue` (modifica): aviso arriba del tablero.
  - `app/pages/foreign-trade/imports/[id]/index.vue` (modifica): tarjeta «Plazo aduanero».
  - `foreign-trade-service.ts` y `AppMenu.vue` (modifica).
- **Diseño de la interacción.**

  **Pantalla «Abandono y prórrogas».** Filtros, con las búsquedas de texto diferidas 300 ms:

  | Etiqueta | Control | Query |
  |---|---|---|
  | Estado | `Select`: «En alerta» (por defecto), «En abandono», «En plazo», «Todos» | `status` (vacío con «Todos») |
  | Prórroga | `Select`: «Todos», «Con prórroga», «Sin prórroga» | `hasExtension` |
  | Depósito | `InputText` | `warehouseStorageNumber` |
  | Carta porte | `InputText` | `cargoManifestNumber` |
  | Importador | `Select` filtrable (terceros con rol importador, `all=true`) | `importerId` |
  | Agencia de aduanas | `Select` filtrable (rol agencia) | `customsAgencyId` |

  Columnas, en el orden del backend (días faltantes ascendente):

  | Columna | Dato |
  |---|---|
  | Depósito | `warehouseStorageNumber`, enlace a `/foreign-trade/imports/{importWarehouseStorageId}` |
  | Carta porte | `cargoManifestNumber` |
  | Fecha de ingreso | `entryDate` (`dd/MM/yyyy`) |
  | Días | `daysElapsed` |
  | Plazo | `deadlineDays` días |
  | Faltan | `daysRemaining`; en rojo y negrita si ≤ 10 (como el legacy); si es negativo, «Vencido hace {n} días» |
  | Estado | `Tag`: «En alerta» (warn), «En abandono» (danger), «En plazo» (secondary) |
  | Prórroga | «Sí, {dd/MM/yyyy}» o «No» |
  | Importador, Agencia de aduanas, Cliente | nombres |
  | Por nacionalizar | `pendingToNationalize` |
  | Existencias | `currentStock` |
  | Acción | «Registrar prórroga» (solo si `hasExtension` es `false`) |

  Estados: cargando (esqueleto de la tabla); vacío «No hay depósitos de importación en este estado.»; error: el aviso global.

  **Diálogo «Registrar prórroga del depósito {número}»:**
  - Texto: «La prórroga amplía el plazo de abandono de 30 a 60 días. **No se puede deshacer.**»
  - Campo «Notas»: `Textarea`, opcional, máx. 500. «Las notas de la prórroga no pueden exceder 500 caracteres.»
  - Botones «Cancelar» y «Registrar prórroga».
  - Al registrar: aviso «Prórroga registrada: nuevo plazo de {deadlineDays} días».
  - Errores del backend: 400 «Solo los depósitos de importación en Borrador o Confirmado admiten prórroga.», 400 «El depósito {n} no tiene mercancía sin nacionalizar.», 409 «El depósito {n} ya tiene prórroga registrada el {dd/MM/yyyy} por {usuario}.»

  **Aviso del tablero** (`pages/foreign-trade/index.vue`, arriba de las tarjetas): si `inAlert + abandoned > 0`, `Message warn` «Abandono: {inAlert} depósitos en alerta y {abandoned} en abandono.» con el botón «Ver depósitos» a `/foreign-trade/abandonment?estado=en-alerta`. Sin depósitos, no se muestra. La página lee `?estado=` (`en-alerta`, `en-abandono`, `en-plazo`, `todos`) para su filtro inicial.

  **Tarjeta «Plazo aduanero»** en el detalle de importación (debajo del resumen), solo si el depósito está en Borrador o Confirmado y tiene mercancía sin nacionalizar:
  - con prórroga: «Prórroga registrada el {extensionRegisteredAt} por {extensionRegisteredByName}» y las notas;
  - sin prórroga: «Sin prórroga: plazo de 30 días desde el ingreso» y el botón «Registrar prórroga» (mismo diálogo).
  - El detalle de los días está en la pantalla de abandono: la tarjeta no los calcula.
- **Endpoints:**
  - **C-F2-12** `GET foreign-trade/abandonment` (query `status`, `hasExtension`, `warehouseStorageNumber`, `cargoManifestNumber`, `importerId`, `customsAgencyId`, paginado, `all`). Fila: `{ importWarehouseStorageId, warehouseStorageId, warehouseStorageNumber, cargoManifestNumber, entryDate, daysElapsed, deadlineDays, daysRemaining, status, hasExtension, extensionRegisteredAt, importerName, customsAgencyName, customerName, pendingToNationalize, currentStock }`. Universo: depósitos de importación en Borrador o Confirmado, con mercancía sin nacionalizar y 20 o más días desde el ingreso.
  - **C-F2-13** `GET foreign-trade/abandonment/summary` → `{ inAlert, abandoned }`. Además, un job envía cada día a las 07:00 la notificación «Depósitos en ventana de abandono» a Comercio Exterior; la campana actual la muestra sin desarrollo.
  - **C-F2-11** `POST foreign-trade/imports/{importWarehouseStorageId}/extension` → `{ notes }`. 200 `{ importWarehouseStorageId, warehouseStorageNumber, extensionRegisteredAt, extensionRegisteredByName, extensionNotes, deadlineDays }`.
  - **C-F2-06**: el detalle de importación trae `extensionRegisteredAt`, `extensionRegisteredByName` y `extensionNotes`.
- **Roles y menú:** `requiredRoles: ["Admin", "ForeignTrade"]`. Menú: Comercio Exterior › «Abandono y prórrogas», ícono `fa-hourglass-half`, `to: "/foreign-trade/abandonment"`, debajo de «Depósitos».
- **Invalidación:** `['foreign-trade']` tras registrar la prórroga. Claves: `['foreign-trade', 'abandonment', params]` y `['foreign-trade', 'abandonment', 'summary']`.
- **Pruebas manuales** (Comercio exterior):
  0. Datos: depósito de importación con fecha de ingreso de hace 25 días (con «Editar fecha de ingreso», WMS-33) y sin levantes.
  1. Tablero de Comercio Exterior. → «Abandono: 1 depósitos en alerta…».
  2. «Ver depósitos». → El depósito con «Faltan 5» en rojo y el estado «En alerta».
  3. «Registrar prórroga» con notas. → Aviso «nuevo plazo de 60 días»; con «Estado: Todos», la fila dice «Prórroga: Sí» y el estado «En plazo».
  4. Intentar registrarla otra vez desde el detalle (con la pestaña abierta antes). → Mensaje 409.
  5. Depósito con 35 días sin prórroga. → «En abandono» y «Vencido hace 5 días».
- **Terminado cuando:** Comercio Exterior ve el aviso, la lista con los días faltantes y registra la prórroga.
- **Riesgo:** registrar una prórroga por error. Se mitiga con el texto «No se puede deshacer» en el diálogo.

---

#### F2-08 · Reportes de abandono (UI-05, GAP-003, LEGACY-FUNC-214)

- **Dificultad:** Media.
- **Tarea del operario (Comercio Exterior):** sacar el reporte de mercancía en abandono y el de salidas hacia destinos de abandono.
- **Cómo lo hacía en el legacy:** `modulos/mod_inventario/reporteabandonos.php`, con las columnas Fecha y hora, No. Guía, Depósito, Placa, Emp. Transporte y Mercancía (`:328-337`), y el reporte de prórrogas.
- **Lo que hace hoy la v2:** no existe.
- **Pantallas y componentes:**
  - `app/pages/reports/abandonment-candidates.vue` (nuevo) y `app/pages/reports/abandonment-exits.vue` (nuevo): copian el patrón de `pages/reports/daily-incoming-goods.vue`.
  - `app/features/reports/services/reports-service.ts` (modifica): `getAbandonmentCandidates`, `getAbandonmentExits`.
  - `app/features/reports/types/abandonment-reports.ts` (nuevo) y su exportación en `types/index.ts` (modifica).
  - `app/features/reports/composables/useAbandonmentReports.ts` (nuevo).
  - `AppMenu.vue` (modifica).
- **Diseño de la interacción.**

  **«Mercancía en abandono»** (C-F2-14):
  - Filtro «Importador» (`Select` filtrable, opcional) y botón «Consultar».
  - Columnas: «Días», «Prórroga» (Sí/No), «Producto», «Embalaje», «Unidad», «Fecha de ingreso», «Depósito», «Manifiesto», «Fecha del manifiesto», «Importador», «Agencia de aduanas», «Ingreso», «Existencias», «Por nacionalizar».
  - Fila de totales con `totals` (ingreso, existencias, por nacionalizar), que cubren todo el filtro.
  - Vacío: «No hay mercancía en abandono.»

  **«Salidas a destino de abandono»** (C-F2-15):
  - Filtros «Desde» y «Hasta» (`DatePicker`, por defecto del 1 de enero del año actual a hoy). «La fecha final no puede ser anterior a la inicial.»
  - Columnas: «Fecha de cargue», «Orden», «Guía», «Placa», «Conductor», «Transportadora», «Cliente», «Agencia de aduanas», «Depósito», «Carta porte», «Manifiesto», «Levantes», «Producto», «Cantidad».
  - Vacío: «No hay salidas a ciudades marcadas como destino de abandono en el rango.»

  La exportación a Excel de los dos reportes llega en F5-11.
- **Endpoints:**
  - **C-F2-14** `GET reports/abandonment-candidates` (query `importerId`, paginado, `all`) → `{ items: [{ days, hasExtension, productName, packagingName, unitMeasure, entryDate, warehouseStorageNumber, manifestNumber, manifestDate, importerName, customsAgencyName, receivedQuantity, currentStock, pendingToNationalize }], totals: { receivedQuantity, currentStock, pendingToNationalize } }` + `pagination`. Incluye productos de depósitos con 30 días o más sin prórroga, o 60 o más con prórroga.
  - **C-F2-15** `GET reports/abandonment-exits` (query `fromDate`, `toDate` en `yyyy-MM-dd`, paginado, `all`). Fila: `{ loadingDate, loadingOrderNumber, guideNumber, vehiclePlate, driverName, transportCompanyName, customerName, customsAgencyName, warehouseStorageNumber, cargoManifestNumber, manifestNumber, releaseNumbers, productName, quantity }`.
- **Roles y menú:** `requiredRoles: ["Admin", "ForeignTrade"]`. Menú: Comercio Exterior › Reportes › «Mercancía en abandono» y «Salidas a destino de abandono».
- **Invalidación:** no hay mutaciones. Claves `['reports', 'abandonment-candidates', params]` y `['reports', 'abandonment-exits', params]`.
- **Pruebas manuales:**
  1. Con el depósito de 35 días de F2-07. → Aparece en «Mercancía en abandono» con sus totales.
  2. Marcar «TULCAN» como destino de abandono, cargar y despachar una orden a esa ciudad. → Aparece en «Salidas a destino de abandono».
  3. «Hasta» anterior a «Desde». → Mensaje de rango.
- **Terminado cuando:** ambos reportes muestran los datos del backend con sus filtros y totales.
- **Riesgo:** bajo.

---
### C.3 Fase 3 — Correcciones y facturación

> **Estado: ✅ COMPLETADA en código (2026-10-01).** F3-01 a F3-08 implementados en `develop` (sin commit: lo hace el usuario). `npm run build` OK. Lint al cerrar la fase: **301 errores** (tope 306) y 0 errores en los archivos nuevos; la fase 4 usa 301 como tope. Pendiente fuera del código: pruebas manuales en el navegador contra el backend local (`5b6dbe2` y migraciones de la fase 3), en el orden de §E (F3-05 después de F3-04).

- **Objetivo:** todo lo que el operario registra se puede corregir o anular con motivo, como en el legacy, y Facturación puede refacturar y usar los ciclos del legacy.
- **Criterio de salida (desde el operario):**
  1. Báscula anula un pesaje completo con motivo y ve qué se deshizo (depósitos, órdenes, facturas).
  2. Comercio Exterior:
     - modifica o cancela una orden antes del cargue;
     - revierte una salida ya cargada;
     - anula una guía y un depósito, siempre con motivo.
  3. Bodega registra un cargue parcial, incluso con un ítem en 0.
  4. Facturación:
     - refactura una factura de almacenamiento anulada;
     - configura un cliente con ciclo de 15, 30, 90, 180 o 360 días;
     - ve la fecha límite de cada período.
- **Rama:** `develop` (DF1). **Empieza cuando la fase 2 tiene todos sus ítems con commit** (toca el detalle de la orden de cargue y el de importación, que la fase 2 modifica).
- **Backend que debe estar corriendo:** commit `5b6dbe2` (fase 3) con las migraciones `ParidadF3_01_CantidadCargada`, `ParidadF3_04_AnulacionGuia`, `ParidadF3_06_FechaLimitePeriodo`, `ParidadF3_07_ReversionOrden`, `ParidadF3_08_AnulacionDeposito`, `ParidadF3_09_AnulacionPesaje` y `ParidadF3_10_Refacturacion`.
- **Advertencia de compatibilidad:** el backend ya exige motivo al anular un depósito (C-F3-09) y la pantalla actual lo envía vacío (`pages/foreign-trade/imports/[id]/index.vue:173`, «Motivo (opcional)», `:652`): falla hasta F3-06.
- **Dificultad:** **Alta.** Anulaciones y reversiones con efectos en inventario y facturación, cada una con su diálogo de resultado.
- **Perfil de agente:** agente capaz, con revisión humana del diff y prueba en el navegador.
- **Componentes comunes nuevos** (se crean en F3-01 y los reutilizan F3-02 a F3-06 y F4-03):
  - `app/components/app/ReasonDialog.vue`: diálogo genérico con título, texto, campo «Motivo» (convención 10), botón «Cancelar» y botón de acción con su etiqueta y su `severity`. Emite `confirm(reason)` y recibe `loading` y `error` (texto que muestra bajo el motivo).
  - `app/components/app/CorrectionResultDialog.vue`: muestra el resultado de una anulación o reversión: un título, listas con etiqueta y un bloque «Para revisión de Facturación» con facturas (`invoiceNumber` o «Sin número», estado traducido, total). Los estados de factura se traducen con el mapa de `features/billing/components/InvoiceStatusBadge.vue`.

---

#### F3-01 · Anular un pesaje completo (UI-02, GAP-005)

- **Dificultad:** Alta.
- **Tarea del operario (báscula):** anular un pesaje registrado por error, aunque el ciclo esté completo, y volver a pesar el camión.
- **Cómo lo hacía en el legacy:** «Eliminar» en la fila del pesaje de entrada, salida o solo pesaje, con un `textarea` de motivo y el botón «Eliminar registro» (`modulos/mod_bascula/eliminarentrada.php:311-317`). Anulaba en cascada el pesaje, la mercancía, el recibo y su detalle (`:61-119`; `eliminarsalida.php:68-88`; `eliminarsolopeso.php:68-87`).
- **Lo que hace hoy la v2:** solo «Descartar» operaciones incompletas en «Recuperar». Un ciclo completo no se anula.
- **Pantallas y componentes:**
  - `app/components/app/ReasonDialog.vue` y `app/components/app/CorrectionResultDialog.vue` (nuevos, comunes de la fase).
  - `app/features/weighbridge/composables/useVoidWeighing.ts` (nuevo).
  - `app/pages/operations/weighbridge/history.vue` (modifica): botón en el diálogo de detalle (pie, junto a «Cerrar», `:686-694`) y banner de anulado.
  - `app/pages/operations/weighbridge/cycles/[id].vue` (modifica): el mismo botón en el encabezado.
  - `app/features/weighbridge/components/WeighbridgeHistoryTable.vue` (modifica): etiqueta «Anulado» en la columna «Estado» (`:321-328`).
  - `app/features/weighbridge/types/weighbridge-cycle.ts` (modifica): `IWeighbridgeHistory` agrega `isVoided`, `voidedAt` y `voidReason`.
  - `app/features/weighbridge/services/weighbridge-service.ts` (modifica).
- **Diseño de la interacción.**
  - El botón «Anular pesaje» (`severity="danger" outlined`) se ve si el pesaje no está anulado y el usuario tiene rol `Admin` o `Scale` (`hasAnyRole` con `usePermissions` importado). En `cycles/[id].vue`, que también abren Facturación y Comercio Exterior, esos roles no lo ven.
  - `ReasonDialog` «Anular pesaje {ticketNumber o «sin tiquete»} · {placa}»:
    - Texto: «Se anulan el pesaje, la mercancía declarada por este camión y su cobro. El ingreso de portería vuelve a la cola para pesarse de nuevo. Anular un pesaje de salida no devuelve la mercancía al depósito: para eso use «Revertir salida» en la orden de cargue.»
    - Campo «Motivo»: `Textarea`, obligatorio. «El motivo de la anulación debe tener entre 10 y 500 caracteres.»
    - Botones «Cancelar» y «Anular pesaje» (`severity="danger"`).
  - Errores 409 del backend, bajo el motivo, tal cual. Por ejemplo: «No se puede anular el pesaje: la mercancía del camión {placa} en el depósito {n} tiene {x} unidades reservadas o despachadas de «{producto}». Revierta o cancele primero la orden {orden}.»
  - Al anular, `CorrectionResultDialog` con el título «Pesaje anulado» y estas listas, cada una solo si no está vacía:

    | Lista | Dato de la respuesta |
    |---|---|
    | «Camiones retirados de los depósitos» | `voidedEntries`: «{warehouseStorageNumber} · {vehiclePlate}» |
    | «Depósitos anulados por quedar sin camiones» | `cancelledDeposits` |
    | «Órdenes que volvieron a Cargada» | `revertedOrders` |
    | «Facturas anuladas» | `cancelledInvoices` |
    | «Para revisión de Facturación» | `invoicesToReview` |

  - **Pesaje anulado en el historial:** `Tag` «Anulado» (`severity="danger"`) en la columna «Estado», con tooltip «Anulado el {dd/MM/yyyy HH:mm}: {voidReason}». En el detalle, `Message error` «Pesaje anulado el {fecha}. Motivo: {voidReason}», y se ocultan «Editar», «Cambiar modo de pago» e «Imprimir Ticket».
- **Endpoints:**
  - **C-F3-10** `POST weighbridge/cycles/{cycleId}/void` → `{ reason }`. 200 `{ weighbridgeCycleId, ticketNumber, kind, voidedEntries: [{ warehouseStorageNumber, vehiclePlate }], cancelledDeposits: [string], revertedOrders: [string], cancelledInvoices: [{ invoiceId, invoiceNumber }], invoicesToReview: [{ invoiceId, invoiceNumber, status, total }] }`. `kind` es `StorageInput`, `Output` o `WeighingOnly`.
  - Errores: 400 del motivo; 409 «El pesaje ya está anulado.»; los 409 de mercancía reservada o despachada, levantes, unidad de carga y orden completa del contrato; desde la fase 4, 409 «El tiquete {t} se usó para la salida de la orden {o}; revierta o cancele primero esa orden.»
  - **C-F3-11** `GET weighbridge/history`: cada fila agrega `isVoided`, `voidedAt` y `voidReason`.
- **Roles y menú:** historial `["Admin", "Scale"]` (sin cambios). **Política del endpoint:** `ScaleAccess`.
- **Invalidación:** `['weighbridge']`, `['weighbridgeHistory']`, `['weighbridge-history']`, `['weighbridgeCycle']`, `['foreign-trade']` y `['billing']`.
- **Pruebas manuales** (Operario báscula):
  1. Anular un solo báscula completo. → Resultado con la factura anulada; en el historial, «Anulado».
  2. Anular el ingreso del único camión de un depósito en Borrador. → «Depósitos anulados por quedar sin camiones: 2026BA…» y el ingreso vuelve a la cola de báscula.
  3. Anular un ingreso cuya mercancía tiene una orden pendiente. → 409 bajo el motivo.
  4. Con rol Facturación, abrir el detalle del ciclo. → No ve «Anular pesaje».
- **Terminado cuando:** un pesaje completo se anula con motivo, se ve el resultado y el historial lo marca.
- **Riesgo:** anular el pesaje equivocado. Se mitiga con el diálogo, que nombra tiquete y placa, y el motivo obligatorio.

---

#### F3-02 · Cancelar con motivo y modificar la orden antes del cargue (UI-03, GAP-006, LEGACY-FUNC-158 y 162)

- **Dificultad:** Alta.
- **Tarea del operario (Comercio Exterior y Bodega):** corregir cantidades o productos de una orden que aún no se carga, o cancelarla diciendo por qué.
- **Cómo lo hacía en el legacy:**
  - «Modificar» la salida (`modulos/mod_salidas/modificarsalida.php`) y quitar productos (`eliminarproductosalida.php`);
  - «Eliminar» con el campo «Motivo eliminación» (`eliminarsalida.php:206-208,110`).
- **Lo que hace hoy la v2:**
  - «Cancelar Orden» con una confirmación y un motivo fijo «Cancelación manual por usuario», solo en `Pending` (`pages/foreign-trade/loading-orders/[id]/index.vue:29,101-115`), y lo mismo en Bodega (`pages/warehouse/loading-orders/[id].vue:95-116`);
  - la orden no se modifica.
- **Pantallas y componentes:**
  - Usa `ReasonDialog` (creado en F3-01).
  - `app/features/foreign-trade/components/EditLoadingOrderItemsDialog.vue` (nuevo) y `composables/useUpdateLoadingOrderItems.ts` (nuevo).
  - `app/pages/foreign-trade/loading-orders/[id]/index.vue` (modifica).
  - `app/pages/warehouse/loading-orders/[id].vue` (modifica).
  - `features/foreign-trade/composables/useCancelLoadingOrder.ts` y `features/warehouse/composables/useLoadingOrderMutations.ts` (modifica: reciben el motivo).
  - Mapas de estado de ambas páginas (modifica): `Reverted: 'Revertida'`.
- **Diseño de la interacción.**

  **Cancelar** (Comercio Exterior y Bodega): visible con estado `Pending` o `InProgress` (antes solo `Pending` en Comercio Exterior y `Pending`/`Scheduled` en Bodega). Abre `ReasonDialog`:
  - título «Cancelar la orden {orderNumber}»;
  - texto «Se liberan las reservas de stock. Si la orden ya estaba en cargue, Bodega recibe un aviso.»;
  - botón «Cancelar orden».

  Al cancelar: aviso «Orden cancelada». 409 «La orden {n} ya fue cargada: use «Revertir salida».» bajo el motivo.

  **Modificar ítems** (solo Comercio Exterior, estado `Pending` o `InProgress`): botón «Modificar ítems» en el encabezado. Diálogo «Modificar la orden {orderNumber}» con una tabla de los ítems actuales:

  | Columna | Control | Obligatorio | Validación y mensaje |
  |---|---|---|---|
  | Depósito, Producto, Unidad de carga | texto | — | — |
  | Cantidad | `InputNumber`, máximo = `availableStock` + `reservedForThisOrder` del ítem | Sí | «La cantidad debe ser mayor a cero.» Sobre el máximo: «Supera el disponible ({máximo} {unidad}).» |
  | Quitar | botón papelera | — | Si se quitan todos: «La orden debe conservar al menos un ítem; si ya no sale mercancía, cancélela.» |

  - Botón «Agregar producto»: lista los productos de los depósitos que ya están en la orden, con la misma consulta que usa `LoadingOrderForm` (`useLoadingOrderDeposits`), filtrada por esos `warehouseStorageId`, y con el tope de nacionalizado de F2-03.
  - Campo «Motivo» (convención 10) y botón «Guardar cambios».
  - Errores del backend (nacionalizado, stock, estado) bajo la tabla.
  - Al guardar: aviso «Orden modificada» y la vista se actualiza con la respuesta.
- **Endpoints:**
  - **C-F3-02** `PATCH foreign-trade/loading-orders/{id}/cancel` y `PATCH warehouse/loading-orders/{id}/cancel` → `{ reason }`, ahora obligatorio (10 a 500). Errores: 400 «El motivo de la cancelación debe tener entre 10 y 500 caracteres.», 409 «La orden {n} ya fue cargada: use «Revertir salida».», 409 «La orden {n} ya está cancelada.», 409 «La orden {n} fue revertida.»
  - **C-F3-03** `PUT foreign-trade/loading-orders/{id}/items` → `{ items: [{ loadingOrderItemId | null, warehouseStorageProductId, warehouseStorageCargoUnitId | null, quantity }], reason }`; la lista reemplaza a la actual. 200: el detalle de la orden. Errores: los de la tabla, más 400 «El ítem {id} no pertenece a la orden.», «El motivo de la modificación debe tener entre 10 y 500 caracteres.», los de C-F2-03 y 409 «Solo se pueden modificar órdenes pendientes o en cargue; la orden {n} está {estado}.»
- **Roles y menú:** sin cambios.
- **Invalidación:** `['foreign-trade']`, `['warehouse-loading-orders']`, `['warehouse-loading-orders-pending']` y `['warehouse-loading-order']`.
- **Pruebas manuales:**
  1. Comercio Exterior: cancelar una orden pendiente con motivo. → Estado «Cancelada» y el stock disponible vuelve.
  2. Bodega: cancelar una orden en cargue. → Igual, desde `/warehouse/loading-orders/{id}`.
  3. Modificar: bajar de 10 a 8 un ítem y agregar 3 de otro producto del mismo depósito. → La orden queda con 8 y 3.
  4. Quitar todos los ítems. → Mensaje de «al menos un ítem».
  5. Intentar cancelar una orden cargada. → No aparece «Cancelar» (aparece «Revertir salida», F3-05).
- **Terminado cuando:** ninguna cancelación usa el motivo fijo y la orden se modifica antes del cargue.
- **Riesgo:** reservas descuadradas. Las maneja el backend; el frontend solo envía la lista completa.

---

#### F3-03 · Cargue parcial: Bodega registra lo que cargó, incluso 0 (UI-03, GAP-006)

- **Dificultad:** Media.
- **Tarea del operario (Bodega):** ejecutar el cargue con lo que realmente subió al camión; lo no cargado libera su reserva.
- **Cómo lo hacía en el legacy:** «Completar Carga» (`modulos/mod_bodegas/completarcargue.php`).
- **Lo que hace hoy la v2:** `LoadingOrderExecutionDialog.vue` propone la cantidad pedida (`:102`) y envía `loadedQuantity` (`:134`); el backend no admitía 0 y dejaba reservas huérfanas.
- **Pantallas y componentes:**
  - `app/features/warehouse/components/LoadingOrderExecutionDialog.vue` (modifica).
  - `app/features/warehouse/types/loading-order.ts` (modifica): resultado con `orderedQuantity` y `reservedStockReleased`; `inventoryMovementId` nulo.
  - Detalle de la orden en Comercio Exterior y Bodega (modifica): columna «Cargado».
- **Diseño de la interacción.**
  - Por ítem, «Cantidad cargada» es un `InputNumber` de **0** a la cantidad pedida. Sobre la pedida: «La cantidad a cargar ({q}) excede la cantidad solicitada ({pedida}).» Negativa: imposible (mínimo 0).
  - Si todos los ítems quedan en 0: «No se cargó mercancía: cancele la orden en lugar de ejecutarla.» y el botón de ejecutar deshabilitado.
  - Ítem con menos de lo pedido: la ayuda «Se liberan {pedida − cargada} {unidad} de la reserva.»
  - Resultado: tabla «Pedido», «Cargado», «Stock anterior», «Stock nuevo», «Reserva liberada», con todos los ítems de la orden.
  - Detalle de la orden: columna «Cargado» (`loadedQuantity`, «—» si es nulo).
- **Endpoints:** **C-F3-01** `POST warehouse/loading-orders/{id}/execute`: `items[].loadedQuantity` admite 0; un ítem que no se envía cuenta como 0. Respuesta por ítem: `{ loadingOrderItemId, warehouseStorageProductId, warehouseStorageId, warehouseStorageNumber, orderedQuantity, loadedQuantity, previousStock, newStock, reservedStockReleased, inventoryMovementId | null }`. Errores: «No se cargó mercancía: cancele la orden en lugar de ejecutarla.», «La cantidad a cargar ({q}) excede la cantidad solicitada ({pedida}) para el producto '{p}'.», «La cantidad cargada no puede ser negativa.» El detalle (C-F2-09) agrega `loadedQuantity` por ítem.
- **Roles y menú:** sin cambios.
- **Invalidación:** la actual de `useLoadingOrderExecute`, más `['foreign-trade']`.
- **Pruebas manuales** (Operario bodega):
  1. Orden de dos ítems de 10; cargar 6 y 0. → El resultado muestra la reserva liberada de 4 y de 10; el disponible del depósito sube.
  2. Todos en 0. → Mensaje y botón deshabilitado.
  3. Detalle de la orden en Comercio Exterior. → «Cargado: 6» y «0».
- **Terminado cuando:** se ejecuta un cargue parcial y el detalle muestra lo cargado.
- **Riesgo:** bajo.

---

#### F3-04 · Anular una guía de salida (UI-03, GAP-006, LEGACY-FUNC-159)

- **Dificultad:** Media.
- **Tarea del operario (Comercio Exterior):** anular una guía emitida por error, para emitir otra o revertir la salida.
- **Cómo lo hacía en el legacy:** al eliminar la salida se anulaba todo lo asociado (`eliminarsalida.php:87-124`).
- **Lo que hace hoy la v2:** la guía no se anula; el historial solo descarga el PDF, el ZIP o cambia el modo de pago (`pages/foreign-trade/dispatch-guides/index.vue:255-300`).
- **Pantallas y componentes:**
  - `app/pages/foreign-trade/dispatch-guides/index.vue` (modifica): acción «Anular guía», etiqueta «Anulada».
  - `app/features/foreign-trade/composables/useCancelDispatchGuide.ts` (nuevo).
  - `app/features/foreign-trade/types/dispatch-guide.ts` (modifica): `isCancelled`, `cancelledAt` y `cancellationReason`.
- **Diseño de la interacción.**
  - En la fila, ícono «Anular guía» (`pi pi-ban`, `severity="danger"`, tooltip «Anular guía») si no está anulada.
  - `ReasonDialog`:
    - título «Anular la guía {guideNumber}»;
    - texto «Se anula la guía y su cobro sin aprobar. Las facturas aprobadas o pagadas quedan para revisión de Facturación. Después puede emitir otra guía para la orden o revertir la salida.»;
    - botón «Anular guía».
  - Resultado: `CorrectionResultDialog` «Guía anulada» con `cancelledInvoices` e `invoicesToReview`.
  - Guía anulada: el número tachado, la `Tag` «Anulada» (danger) y el tooltip «Anulada el {fecha}: {motivo}». Se ocultan «Cambiar modo de pago» y la anulación. El PDF lleva la marca «ANULADA» (backend).
- **Endpoints:** **C-F3-04** `POST foreign-trade/dispatch-guides/{id}/cancel` → `{ reason }`. 200 `{ dispatchGuideId, guideNumber, cancelledAt, cancelledInvoices: [{ invoiceId, invoiceNumber }], invoicesToReview: [{ invoiceId, invoiceNumber, status, total }] }`. Errores: 400 «El motivo de la anulación debe tener entre 10 y 500 caracteres.», 404 «La guía no existe.», 409 «La guía {n} ya está anulada.» Listados, detalle y ZIP agregan `isCancelled`, `cancelledAt` y `cancellationReason`.
- **Roles y menú:** sin cambios. **Invalidación:** `['foreign-trade']` y `['billing']`.
- **Pruebas manuales:**
  1. Anular una guía con su factura en Borrador. → «Facturas anuladas: …» y la guía «Anulada».
  2. Anular una guía con su factura aprobada. → «Para revisión de Facturación: {número} (Aprobada, $…)».
  3. Ir a «Guías pendientes». → La orden aparece de nuevo para emitir otra guía.
- **Terminado cuando:** la guía se anula con motivo y el listado la marca.
- **Riesgo:** bajo.

---

#### F3-05 · Revertir una salida después del cargue (UI-03, GAP-006, LEGACY-FUNC-159)

- **Dificultad:** Media.
- **Tarea del operario (Comercio Exterior):** deshacer un cargue registrado por error: la mercancía vuelve al depósito.
- **Cómo lo hacía en el legacy:** al anular la salida devolvía la mercancía, reactivaba ubicaciones y reubicaba los pesajes (`eliminarsalida.php:87-124`).
- **Lo que hace hoy la v2:** no existe (la orden cargada solo se corregía con el ajuste CE-7).
- **Pantallas y componentes:**
  - `app/pages/foreign-trade/loading-orders/[id]/index.vue` (modifica): botón «Revertir salida» y banner de revertida.
  - `app/features/foreign-trade/composables/useRevertLoadingOrder.ts` (nuevo).
  - Tipos de la orden (modifica): `revertedAt` y `reversalReason`; estado `Reverted`.
  - `app/pages/foreign-trade/loading-orders/index.vue` (modifica): filtro y etiqueta «Revertida».
- **Diseño de la interacción.**
  - «Revertir salida» (`severity="warn" outlined`) visible con estado `Loaded`, `Dispatched` o `Complete`.
  - `ReasonDialog`:
    - título «Revertir la salida de la orden {orderNumber}»;
    - texto «La mercancía cargada vuelve a su depósito y queda por ubicar. Si la orden tiene una guía vigente, anúlela primero.»;
    - botón «Revertir salida».
  - 409 «Anule primero la guía {g} de la orden {n}.»: bajo el motivo, con el botón «Ir a guías de salida» (`/foreign-trade/dispatch-guides`).
  - Resultado: `CorrectionResultDialog` «Salida revertida» con:
    - «Mercancía devuelta»: `returnedItems`, «{productName} · {quantity} · depósito {warehouseStorageNumber}»;
    - «Depósitos reabiertos»: `reopenedDeposits`.
  - Orden revertida: `Tag` «Revertida» y `Message` «Salida revertida el {revertedAt}. Motivo: {reversalReason}».
- **Endpoints:** **C-F3-08** `POST foreign-trade/loading-orders/{id}/revert` → `{ reason }`. 200 `{ loadingOrderId, orderNumber, status: "Reverted", returnedItems: [{ warehouseStorageProductId, warehouseStorageNumber, productName, quantity }], reopenedDeposits: [string] }`. Errores: 400 del motivo; 409 «Solo se revierte una orden ya cargada; la orden {n} está {estado}.»; 409 de la guía; 400 «La devolución dejaría más stock que la cantidad del depósito.»
- **Roles y menú:** sin cambios. **Invalidación:** `['foreign-trade']`, `['warehouse-loading-orders']`, `['warehouse-inventory-movements']` y `['warehouse']`.
- **Pruebas manuales:**
  1. Orden cargada con guía vigente. → 409 con «Ir a guías de salida». Anular la guía (F3-04) y revertir. → «Mercancía devuelta…» y el estado «Revertida».
  2. Bodega › Inventario. → El stock del depósito subió.
- **Terminado cuando:** una salida cargada se revierte con motivo y el inventario se recupera.
- **Riesgo:** revertir la orden equivocada. Se mitiga con el diálogo que nombra la orden.

---

#### F3-06 · Anular un depósito con motivo y ver sus efectos (GAP-011, DF14)

- **Dificultad:** Media.
- **Tarea del operario (Comercio Exterior):** anular un depósito creado por error, sabiendo qué órdenes, períodos y facturas se afectan.
- **Cómo lo hacía en el legacy:** «Eliminar depósito» e «Eliminar ingreso» con observaciones (`modulos/mod_depositos/eliminardeposito.php:56-65`; `mod_ingresos/eliminaringreso.php:60-79`).
- **Lo que hace hoy la v2:**
  - diálogo «Anular depósito» con «Motivo (opcional)», en las tres páginas de detalle (`pages/foreign-trade/imports/[id]/index.vue:640-660` e iguales en `exports/[id]` e `inspections/[id]`);
  - envía `reason: cancelReason || undefined` (`:173`).
- **Pantallas y componentes:**
  - Las tres páginas de detalle (modifica): usan `ReasonDialog` y `CorrectionResultDialog`, y muestran el banner de anulado.
  - `useCancelWarehouseStorage.ts` (modifica): devuelve la respuesta tipada.
  - Tipos del detalle (modifica): `cancelledAt` y `cancellationReason`.
- **Diseño de la interacción.**
  - `ReasonDialog`:
    - título «Anular el depósito {número}»;
    - texto «Se anulan el depósito, sus ítems en órdenes pendientes (una orden que quede vacía se cancela), sus períodos de almacenamiento y sus facturas sin aprobar. Las facturas aprobadas o pagadas quedan para revisión de Facturación. Un camión nuevo con la misma carta porte creará otro depósito.»;
    - botón «Anular depósito».
  - Errores 409 bajo el motivo: «El depósito {n} tiene salidas ejecutadas en la orden {o}. Revierta primero la salida.» y «El camión {placa} del depósito {n} aún está en báscula. Termine o anule el pesaje antes de anular el depósito.»
  - Resultado: `CorrectionResultDialog` «Depósito anulado» con «Ítems retirados de órdenes: {removedOrderItems}», «Órdenes canceladas», «Períodos cerrados: {closedPeriods}», «Facturas anuladas» y «Para revisión de Facturación». Al cerrar, va a `/foreign-trade/deposits` (comportamiento actual).
  - Depósito anulado: `Message error` «Depósito anulado el {cancelledAt}. Motivo: {cancellationReason}».
- **Endpoints:** **C-F3-09** `POST foreign-trade/warehouse-storages/{id}/cancel` → `{ reason }`, obligatorio (10 a 500). 200 `{ warehouseStorageId, status, removedOrderItems, cancelledOrders: [string], closedPeriods, cancelledInvoices: [{ invoiceId, invoiceNumber }], invoicesToReview: [{ invoiceId, invoiceNumber, status, total }] }`. Errores: 400 del motivo, 400 «No se puede anular un depósito cerrado.», 400 «El depósito ya está anulado.» y los dos 409.
- **Roles y menú:** sin cambios. **Invalidación:** `['foreign-trade']` y `['billing']`.
- **Pruebas manuales:**
  1. Anular un depósito en Borrador con motivo. → Resultado y regreso al listado; su detalle muestra el banner.
  2. Depósito con una orden pendiente de dos depósitos. → «Ítems retirados de órdenes: 1».
  3. Depósito con un camión aún sin pesar. → 409 del camión en báscula.
  4. Motivo vacío. → Botón deshabilitado (antes fallaba en el backend).
- **Terminado cuando:** las tres modalidades anulan con motivo y muestran el resultado.
- **Riesgo:** bajo.

---

#### F3-07 · Ciclos de facturación del legacy y fecha límite del período (UI-08, GAP-008, RN-013)

- **Dificultad:** Baja.
- **Tarea del operario (Facturación):** configurar al cliente con su ciclo del legacy (15, 30, 90, 180 o 360 días) y ver la fecha límite de cada período.
- **Cómo lo hacía en el legacy:** campo «días de facturación» del cliente (`modulos/mod_clientes/modificarcliente.php:466-471`). El período terminaba en inicio + días y vencía en fin + 3 días (`cron.php:20-130`).
- **Lo que hace hoy la v2:** cuatro opciones fijas en el código (`features/billing/components/BillingConfigForm.vue:23-26`; `pages/billing/configurations/index.vue:43-46`; tipo `features/billing/types/billing-config.ts:1`).
- **Pantallas y componentes:**
  - `app/features/billing/composables/useBillingCycles.ts` (nuevo): consulta los ciclos.
  - `BillingConfigForm.vue` y `pages/billing/configurations/index.vue` (modifica): opciones y etiquetas del API.
  - `billing-config.ts` (modifica): `BillingCycle` agrega `Days15`, `Days30`, `Days90`, `Days180` y `Days360`.
  - `app/features/billing/components/DepositSummaryDialog.vue` (modifica): sección «Períodos de almacenamiento» con `useStoragePeriods`, que ya existe y no se usa.
  - `app/features/billing/types/storage-period.ts` (modifica): `limitDate: string | null`.
- **Diseño de la interacción.**
  - «Ciclo de facturación»: `Select` con las nueve opciones de `GET billing/configurations/cycles`, `option-label="label"`, `option-value="value"`. Ayuda bajo el campo con `days`: «Períodos de {days} días» o «Mes calendario» / «Sin períodos automáticos» cuando `days` es nulo.
  - El listado de configuraciones muestra la `label` del API.
  - En el resumen del depósito (Facturación › Depósitos pendientes › resumen), «Períodos de almacenamiento»: columnas «Inicio», «Fin», «Fecha límite» (`dd/MM/yyyy`; «—» si es nulo), «Estado» (Abierto, Cerrado), «Factura» (número o «Sin número»), «Total».
- **Endpoints:**
  - **C-F3-05** `GET billing/configurations/cycles` → `[{ value, label, days }]`.
  - **C-F3-06** `PUT billing/configurations/{stakeholderId}`: `billingCycle` acepta los nueve valores.
  - **C-F3-07** `GET billing/storage-periods?warehouseStorageId={id}&all=true` → `StoragePeriodDto` con `limitDate` (`yyyy-MM-dd` o nulo). `periodStart` y `periodEnd` son las 00:00 de Colombia del día; el fin es inclusivo; se muestran como días.
- **Roles y menú:** sin cambios (`["Admin", "Billing"]`). **Invalidación:** la actual de la configuración (`['billing']`). Claves `['billing', 'cycles']` y `['billing', 'storage-periods', params]` (actual).
- **Pruebas manuales** (Facturación):
  1. Editar un cliente y elegir «Trimestral (90 días)». → Se guarda y el listado lo muestra.
  2. Resumen de un depósito confirmado. → Sus períodos con la fecha límite = fin + 3 días.
- **Terminado cuando:** los nueve ciclos se eligen y se ve la fecha límite.
- **Riesgo:** bajo.

---

#### F3-08 · Refacturar una factura de almacenamiento anulada (UI-07, GAP-007, RN-052)

- **Dificultad:** Media.
- **Tarea del operario (Facturación):** después de anular una factura de almacenamiento, generar la nueva sin perder el período.
- **Cómo lo hacía en el legacy:** anular la factura volvía el período a «activo» y lo dejaba para facturar de nuevo (`modulos/mod_facturacion/eliminarfactura.php:56-65`).
- **Lo que hace hoy la v2:** anular no reabre el período y no hay cómo crear la factura nueva desde la interfaz (`pages/billing/invoices/create.vue` está congelada y **no se revive**).
- **Pantallas y componentes:**
  - `app/features/billing/components/InvoiceActionsDialog.vue` (modifica): acción «Refacturar».
  - `app/features/billing/composables/useReissueInvoice.ts` (nuevo).
  - `app/pages/billing/invoices/[id].vue` (modifica): enlaces entre la anulada y la nueva.
  - `app/pages/billing/pending-deposits/index.vue` (modifica): columna «Por refacturar».
  - Tipos (modifica): `IInvoiceDetailDto.reissuedFromInvoiceId` y `reissuedAsInvoiceId`; fila de depósitos pendientes con `periodsPendingReissue`.
- **Diseño de la interacción.**
  - En el diálogo de acciones, bloque «Refacturar», visible si `status = Cancelled`, `reissuedAsInvoiceId` es nulo y la factura tiene depósitos (`deposits.length > 0`, que solo tienen las de almacenamiento).
    - Texto: «Genera una factura nueva en Borrador, sin número SIIGO, con los mismos períodos de almacenamiento.»
    - Botón «Refacturar».
    - Confirmación con `useAppConfirm`: «¿Refacturar la factura {número}?»
    - Al terminar: aviso «Factura nueva creada en Borrador» y navegación a `/billing/invoices/{id de la nueva}`.
  - En el detalle:
    - si `reissuedFromInvoiceId`: `Message info` «Refacturación de la factura {número de la anulada}», con enlace;
    - si `reissuedAsInvoiceId`: «Refacturada como {número de la nueva o «Borrador»}», con enlace.
  - Depósitos pendientes: columna «Por refacturar» con `periodsPendingReissue` en rojo cuando es > 0.
  - Al anular una factura de almacenamiento (acción existente), el aviso de éxito agrega: «Sus períodos quedaron por refacturar.» (C-F3-12).
- **Endpoints:**
  - **C-F3-13** `POST billing/invoices/{id}/reissue`, sin cuerpo. 201: el detalle de la factura nueva. Errores: 409 «Solo se puede refacturar una factura anulada; la factura {n} está {estado}.», 409 «La factura {n} ya fue refacturada como {m}.», 400 «La factura {n} no tiene períodos de almacenamiento; genere de nuevo el cobro desde su operación.»
  - **C-F3-12** `PATCH billing/invoices/{id}/cancel`: sin cambio de forma.
  - **C-F3-14** `GET billing/pending-deposits`: cada fila agrega `periodsPendingReissue`.
- **Roles y menú:** sin cambios. **Invalidación:** `['billing']`.
- **Pruebas manuales** (Facturación):
  1. Anular una factura de almacenamiento en Borrador. → El aviso dice «Sus períodos quedaron por refacturar»; en depósitos pendientes, «Por refacturar: 1».
  2. «Refacturar». → Navega a la nueva en Borrador con el enlace a la anulada; la anulada dice «Refacturada como…».
  3. Refacturar otra vez la anulada. → No aparece el bloque.
  4. Factura anulada de báscula (sin depósitos). → No aparece «Refacturar».
- **Terminado cuando:** una factura de almacenamiento anulada se refactura desde la interfaz.
- **Riesgo:** revivir la creación manual congelada. Se mitiga usando solo el endpoint de refacturación.

---
### C.4 Fase 4 — Bodega y mercancía

> **Estado: ✅ COMPLETADA en código (2026-10-02; commit `aed2ab1`).** F4-01 a F4-06 implementados en `develop`. `npm run build` OK. Lint al cerrar la fase: **300 errores** (tope 301) y 0 errores en los archivos nuevos; la fase 5 usa 300 como tope. Pendiente fuera del código: pruebas manuales en el navegador contra el backend local (`04bf734` y migraciones de la fase 4) y la validación de F4-05 y F4-06 con el operario de báscula antes de su commit.

- **Objetivo:** Bodega gestiona ubicaciones por cantidad y novedades como en el legacy; Comercio Exterior carga listas de empaque; báscula y Comercio Exterior reponen los atajos «duplicar recibo» y «usar tiquete existente».
- **Criterio de salida (desde el operario):**
  1. Bodega:
     - ubica, mueve y libera mercancía de un producto;
     - ve el contenido de una ubicación;
     - al cargar, el sistema le dice de dónde retirar.
  2. Bodega registra una novedad de un lote que llegó dañado tres días después, con su desglose, y la imprime.
  3. Comercio Exterior carga la lista de empaque de un proveedor real y asocia sus artículos a un camión.
  4. Báscula saca dos órdenes del mismo camión con un solo pesaje y un solo cobro, y saca una orden con el tiquete de ingreso sin volver a pesar.
  5. Las cuadrillas se eligen de un catálogo en la orden, la recepción y el cargue.
- **Rama:** `develop` (DF1). **Empieza cuando la fase 3 tiene todos sus ítems con commit** (toca el diálogo de cargue, el detalle de la orden y el historial de báscula, que la fase 3 modifica).
- **Backend que debe estar corriendo:** commit `04bf734` (fase 4) con las migraciones `ParidadF4_01_Ubicaciones`, `ParidadF4_03_Novedades`, `ParidadF4_05_ListasEmpaque`, `ParidadF4_07_PesajeCompartido`, `ParidadF4_08_SalidaConTiquete`, `ParidadF4_09_ImpresionEtiquetas` y `ParidadF4_10_Cuadrillas`.
- **Dificultad:** **Muy alta.** F4-05 y F4-06 tocan el banco de trabajo de báscula (operación de salida y cobro). El resto es Alta o Media.
- **Perfil de agente:** agente capaz, revisión humana del diff y prueba en el navegador. F4-05 y F4-06 se validan con el operario de báscula antes de su commit (sin cronometraje).

---

#### F4-01 · Catálogo de cuadrillas y su uso en orden, recepción y cargue (UI-15, GAP-026)

- **Dificultad:** Media.
- **Tarea del operario:** elegir la cuadrilla que descarga o carga de una lista, en lugar de escribirla.
- **Cómo lo hacía en el legacy:** catálogo `cuadrilla` (`bodegas_schema.sql`, tabla `cuadrilla`); se elegía al registrar el depósito (`modulos/mod_depositos/registrardeposito.php`) y la salida (`modulos/mod_salidas/registrarsalida.php`, `id_cuadrilla`), y se imprimía en la guía.
- **Lo que hace hoy la v2:** la guía tiene `crew` como texto (`features/foreign-trade/types/dispatch-guide.ts:41`); no hay catálogo ni selección.
- **Pantallas y componentes:**
  - `app/pages/admin/crews/index.vue` (nuevo): patrón de `pages/admin/packaging-types/index.vue`.
  - `app/features/administration/types/crew.ts`, `composables/useCrews.ts` y `useMutationsCrews.ts` (nuevos).
  - `administration-service.ts` (modifica).
  - `app/features/administration/components/CrewSelect.vue` (nuevo): `Select` reutilizable con las cuadrillas activas.
  - Formularios que lo usan (modifica): `features/foreign-trade/components/LoadingOrderForm.vue`, `features/warehouse/components/LoadingOrderExecutionDialog.vue`, `ReceptionStepCompletion.vue` y `ReceptionStepManualInfo.vue`.
  - Lecturas (modifica): detalle de la orden en Comercio Exterior y Bodega; `DepositDetailGeneralInfoCard.vue`.
  - `AppMenu.vue` (modifica).
- **Diseño de la interacción.**

  **Administración › Cuadrillas:** listado con buscador («Buscar cuadrilla», diferido 300 ms) y columnas «Nombre», «Estado», «Acciones». Diálogo con «Nombre» (`InputText`, obligatorio, máx. 200: «El nombre de la cuadrilla es obligatorio y no puede exceder 200 caracteres.») y «Activa» (al editar). 409 «Ya existe la cuadrilla {nombre}.» bajo el nombre. Eliminar: 409 «La cuadrilla está en uso; desactívela en lugar de eliminarla.»

  **Campo «Cuadrilla»** (`CrewSelect`, opcional, `show-clear`, opciones de `GET administration/crews?isActive=true&all=true`):

  | Pantalla | Etiqueta | Dónde va | Valor inicial |
  |---|---|---|---|
  | Crear orden de cargue | «Cuadrilla que carga» | en «Destino y Programación» | vacío |
  | Ejecutar cargue | «Cuadrilla que cargó» | antes de «Número de Sello» | la de la orden |
  | Recepción (con y sin báscula) | «Cuadrilla que descargó» | antes de «Comentarios» | vacío |

  Error 404 «La cuadrilla no existe o está inactiva.»: lo muestra el aviso global.

  **Lecturas:** «Cuadrilla» en el detalle de la orden (`crewName` o «—»); «Cuadrilla que descargó» en «Información general» del depósito.
- **Endpoints:**
  - **C-F4-22** `GET administration/crews` (query `search`, `isActive`, paginado, `all`) → `CrewDto { id, legacyId, name, isActive, createdAt, updatedAt }`; `POST administration/crews` → `{ name }`; `PUT administration/crews/{id}` → `{ name, isActive }`; `DELETE administration/crews/{id}`. Lectura para cualquier usuario; escritura `AdminOnly`.
  - **C-F4-23** `crewId` opcional en:
    - `POST foreign-trade/loading-orders`;
    - `POST warehouse/loading-orders/{id}/execute`;
    - `POST warehouse/receptions`, `POST warehouse/receptions/{id}/complete` y `POST warehouse/receptions/without-weighbridge`.

    Las lecturas de órdenes y depósitos agregan `crewId` y `crewName`; la guía llena `crew` con la cuadrilla de la orden.
- **Roles y menú:** Cuadrillas `["Admin"]`; menú Administración › «Cuadrillas», ícono `fa-people-group`, `to: "/admin/crews"`.
- **Invalidación:** `['administration', 'crews']` tras crear, editar o eliminar. Los formularios conservan su invalidación.
- **Pruebas manuales:**
  1. Crear «CUADRILLA 1». → Aparece en los tres formularios.
  2. Crear una orden con cuadrilla y ejecutarla cambiando la cuadrilla. → El detalle muestra la última.
  3. Recepción con cuadrilla. → El detalle del depósito la muestra.
  4. Desactivar la cuadrilla. → Ya no aparece en los selects.
- **Terminado cuando:** la cuadrilla se elige del catálogo en los tres flujos y se ve en las lecturas.
- **Riesgo:** bajo.

---

#### F4-02 · Ubicar, mover y liberar mercancía por cantidades (UI-13, GAP-014, RN-045, RN-048)

- **Dificultad:** Alta.
- **Tarea del operario (Bodega):** repartir la mercancía de un producto entre posiciones, moverla después de recibirla, liberar una posición y, al cargar, saber de dónde retirar.
- **Cómo lo hacía en el legacy:**
  - «Asignar Bodega»: elegía la sección y la cantidad, y podía repartir un lote entre secciones (`modulos/mod_bodegas/registrarbodegacantidad.php`, `guardarcantidadseccion.php:87-118`);
  - «Liberar Bodega» (`liberarcantidadseccion.php:94-105`);
  - liberaba las posiciones al emitir la guía (`modulos/mod_salidas/verguia.php:465-479`).
- **Lo que hace hoy la v2:** una sola ubicación por producto, asignada en la recepción (`features/warehouse/components/ReceptionStepCompletion.vue:461-470`); no se mueve ni se libera.
- **Pantallas y componentes:**
  - `app/features/warehouse/components/ProductPlacementsDialog.vue` (nuevo).
  - `app/features/warehouse/components/LocationContentPanel.vue` (nuevo).
  - `app/features/warehouse/composables/usePlacements.ts` (nuevo: consulta y las tres mutaciones) y `useLocationContent.ts` (nuevo).
  - `app/features/warehouse/types/placements.ts` (nuevo).
  - `features/warehouse/services/warehouse-service.ts` (modifica).
  - `app/pages/warehouse/inventory/index.vue` (modifica): acción «Ubicaciones» en «Consultar Stock» y pestaña nueva «Ubicaciones».
  - `LoadingOrderExecutionDialog.vue` (modifica): posiciones liberadas en el resultado.
  - `ReceptionStepCompletion.vue` y `ReceptionStepManualInfo.vue` (modifica): ayuda del campo de ubicación.
- **Diseño de la interacción.**

  **Diálogo «Ubicaciones de {producto} · depósito {número}»** (acción por fila de «Consultar Stock», `pages/warehouse/inventory/index.vue:386-410`):
  - Resumen: «Existencias {currentStock} · Ubicadas {placedQuantity} · Por ubicar {pendingToPlace}».
  - Tabla: «Ubicación» (`locationCode`), «Cantidad», «Última ubicación» (fecha) y las acciones «Mover» y «Liberar».
  - Vacío: «Este producto no tiene mercancía ubicada.»
  - Botón «Ubicar», habilitado si `pendingToPlace` > 0.

  | Acción | Campos | Validación y mensaje |
  |---|---|---|
  | Ubicar | «Ubicación» (`Select` filtrable de `GET warehouse/locations` disponibles, `all=true`, etiqueta «{code} — {name}»), obligatorio. «Cantidad» (`InputNumber`, máximo `pendingToPlace`), obligatorio. | «Seleccione la ubicación.» / «La cantidad a ubicar debe ser mayor que cero.» / sobre el máximo: «Solo quedan {p} por ubicar.» |
  | Mover | «Desde» (texto: la fila). «Hacia» (`Select`, sin la de origen), obligatorio. «Cantidad» (máximo la de la fila), obligatorio. | «La ubicación de destino debe ser distinta de la de origen.» / «La cantidad a mover debe ser mayor que cero.» / «En {código} solo hay {x} unidades ubicadas.» |
  | Liberar | «Cantidad» (máximo la de la fila), obligatorio. Texto: «Lo liberado vuelve a «por ubicar».» | «La cantidad a liberar debe ser mayor que cero.» |

  Cada acción actualiza el diálogo con la respuesta (`ProductPlacementsDto`) y muestra un aviso: «Mercancía ubicada», «Mercancía movida» o «Posición liberada». Errores 409 bajo el formulario: «La ubicación {código} está deshabilitada.», «El depósito {n} está {estado}; no se puede ubicar mercancía.»

  **Pestaña «Ubicaciones»** en Inventario: un `Select` «Ubicación» (buscador) y, al elegir, `LocationContentPanel` con «Disponible: Sí/No», «Total: {totalQuantity}» y la tabla «Depósito», «Producto», «Cantidad», «Última ubicación». Vacío: «La ubicación está vacía.»

  **Cargue:** en el resultado de `LoadingOrderExecutionDialog`, por ítem: «Retirar de: {locationCode} ({quantity}), …» con `releasedPlacements`, de la más reciente a la más antigua.

  **Recepción:** bajo «Ubicación en bodega», la ayuda «La cantidad descargada queda ubicada en esta posición.» El 409 «La ubicación {código} está deshabilitada.» lo muestra el aviso global.
- **Endpoints:**
  - **C-F4-01** `GET warehouse/storage-products/{id}/placements` → `ProductPlacementsDto { warehouseStorageProductId, warehouseStorageId, warehouseStorageNumber, productName, currentStock, placedQuantity, pendingToPlace, mainLocationId, placements: [{ warehouseLocationId, locationCode, locationName, quantity, lastPlacedAt }] }`. 404 «El producto del depósito no existe.»
  - **C-F4-02** `POST warehouse/storage-products/{id}/placements` → `{ warehouseLocationId, quantity }`. Errores: los de la tabla, más 404 «La ubicación no existe.» y 409 «No se puede ubicar {q}: solo quedan {p} por ubicar.»
  - **C-F4-03** `POST …/placements/move` → `{ fromLocationId, toLocationId, quantity }`. Errores: los de la tabla, más 404 «El producto no está ubicado en {código}.»
  - **C-F4-04** `POST …/placements/release` → `{ warehouseLocationId, quantity }`.
  - **C-F4-05** `GET warehouse/locations/{id}/placements` → `{ warehouseLocationId, code, name, isAvailable, totalQuantity, items: [{ warehouseStorageProductId, warehouseStorageNumber, productName, quantity, lastPlacedAt }] }`.
  - **C-F4-06** recepción: el producto con ubicación queda ubicado; 409 de ubicación deshabilitada.
  - **C-F4-07** cargue: cada ítem del resultado agrega `releasedPlacements: [{ warehouseLocationId, locationCode, quantity }]`.
  - Todos con `WarehouseAccess`. `{id}` de los cuatro primeros es el `id` de la fila de «Consultar Stock» (`IWarehouseStorageStockProduct.id`, que es el `warehouseStorageProductId`).
- **Roles y menú:** Inventario `requiredRoles` actual. Sin menú nuevo.
- **Invalidación:** `['warehouse']`, `['warehouse-storage-stock']` y `['warehouse-locations']` tras ubicar, mover o liberar. Claves: `['warehouse', 'placements', warehouseStorageProductId]` y `['warehouse', 'location-content', warehouseLocationId]`.
- **Pruebas manuales** (Operario bodega):
  1. Producto de 10 sin ubicar: «Ubicar» 6 en A-01 y 4 en B-02. → «Por ubicar 0».
  2. «Mover» 2 de A-01 a C-03. → A-01 4, B-02 4, C-03 2.
  3. «Liberar» 1 de B-02. → «Por ubicar 1».
  4. Pestaña «Ubicaciones», A-01. → Muestra el depósito y la cantidad 4.
  5. Ejecutar una orden de 5 de ese producto. → «Retirar de: …» con las posiciones.
  6. Ubicar en una posición deshabilitada. → 409.
- **Terminado cuando:** las tres acciones funcionan desde Inventario y el cargue indica de dónde retirar.
- **Riesgo:** descuadre entre posiciones y stock. Lo controla el backend; el frontend no calcula cantidades.

---

#### F4-03 · Novedades de mercancía: registro, edición, anulación e impresión (UI-14, GAP-015, RN-068)

- **Dificultad:** Media.
- **Tarea del operario (Bodega):** registrar en cualquier momento una novedad de un producto del depósito (dañada, faltante, sobrante), con el estado de la carpa y del remolque, corregirla, anularla e imprimir el «Reporte de mercancías» para el reclamo del cliente.
- **Cómo lo hacía en el legacy:** «Observaciones» (`modulos/mod_bodegas/registrarobservaciones.php:286-358`), en este orden:
  1. Hora Ingreso y Hora Salida (prellenadas con ahora);
  2. Tipo de Observación (Ingreso, Salida, Trasbordo, **Rutina** por defecto, Inspección y Muestras);
  3. DESCRIPCIÓN (obligatoria);
  4. TOTAL MCIA (prellenado con lo por ubicar); Descargada (casilla); Reg. fotográfico;
  5. Buena, Dañada, Faltante y Sobrante (en 0);
  6. Carpa (Buena, Agujereada, Rota, Sin carpa); Remolque (Limpio, Sucio, Oxidado, Mojado, Roto);
  7. «INSERTAR OBSERVACION».

  Se editaba (`modificarobservacion.php`) e imprimía (`imprimirobservacion.php`).
- **Lo que hace hoy la v2:** solo comentario y fotos durante la recepción. `useReceptionReceiptPdf` llama a un método inexistente (`features/warehouse/composables/useWarehouseExports.ts:79-95`): fuera de alcance (§G).
- **Pantallas y componentes:**
  - `app/pages/warehouse/novelties/index.vue` (nuevo): listado.
  - `app/features/warehouse/components/NoveltyFormDialog.vue` (nuevo): registrar y editar.
  - `app/features/warehouse/composables/useNovelties.ts` (nuevo: listado, detalle, crear, editar, anular, PDF).
  - `app/features/warehouse/types/novelty.ts` (nuevo), con los rótulos de §«Rótulos» abajo.
  - `warehouse-service.ts` (modifica).
  - `app/pages/warehouse/inventory/index.vue` (modifica): acción «Registrar novedad» por fila de «Consultar Stock».
  - `app/features/foreign-trade/components/DepositNoveltiesSection.vue` (nuevo): sección de solo lectura en las tres páginas de detalle del depósito, con «Imprimir».
  - `AppMenu.vue` (modifica).
- **Diseño de la interacción.**

  **Formulario** (diálogo «Registrar novedad · {producto} · depósito {número}» o «Editar novedad»), en el orden del legacy:

  | # | Etiqueta | Control | Obligatorio | Validación y mensaje |
  |---|---|---|---|---|
  | 1 | Inicio | `DatePicker` con hora, 24 h, por defecto ahora | Sí | — |
  | 2 | Fin | `DatePicker` con hora, por defecto ahora | Sí | «La fecha de fin no puede ser anterior a la de inicio.» |
  | 3 | Tipo de novedad | `Select`: Ingreso, Salida, Trasbordo, Rutina (por defecto), Inspección y muestras | Sí | «Seleccione el tipo de novedad.» |
  | 4 | Ordenado por | `InputText`, máx. 100 | No | — |
  | 5 | Camión | `Select` con las recepciones del depósito («{vehiclePlate} · {fecha}», valor `warehouseStorageEntryId`), `show-clear` (DF17) | No | «El camión no pertenece al depósito del producto.» (backend) |
  | 6 | Descripción | `Textarea`, 4 filas, máx. 4.000 | Sí | «La descripción de la novedad es obligatoria.» / «La descripción no puede exceder 4000 caracteres.» |
  | 7 | Total mercancía | `InputNumber`, ≥ 0; al registrar, precargado con las existencias del producto | Sí | «Las cantidades no pueden ser negativas.» |
  | 8 | Descargada | `Checkbox` | — | — |
  | 9 | Registro fotográfico | `InputText`, máx. 200 | No | — |
  | 10 | Buena · Dañada · Faltante · Sobrante | cuatro `InputNumber` ≥ 0, en 0 | No | «Las cantidades no pueden ser negativas.» Sin regla de suma (como el legacy). |
  | 11 | Carpa | `Select`: Buena, Agujereada, Rota, Sin carpa; `show-clear` | No | — |
  | 12 | Remolque | `Select`: Limpio, Sucio, Oxidado, Mojado, Roto; `show-clear` | No | — |

  Botón «Registrar novedad» o «Guardar cambios». Aviso: «Novedad registrada». Con dañada, faltante o sobrante > 0, el aviso agrega «Comercio Exterior recibe el aviso.» 409 «El depósito {n} está anulado.» o «La novedad está anulada.» bajo el formulario.

  **Rótulos** (valor del API → texto):
  - Tipo: `Entry` Ingreso, `Exit` Salida, `Transshipment` Trasbordo, `Routine` Rutina, `Inspection` Inspección y muestras.
  - Carpa: `Good` Buena, `Holed` Agujereada, `Torn` Rota, `NoTarp` Sin carpa.
  - Remolque: `Clean` Limpio, `Dirty` Sucio, `Rusty` Oxidado, `Wet` Mojado, `Broken` Roto.

  **Listado «Novedades»:**
  - Filtros:
    - «Depósito»: `Select` filtrable de `GET warehouse/inventory/deposits` con `all=true`, que da el `warehouseStorageId`;
    - «Tipo»;
    - «Desde» y «Hasta» (fecha de inicio);
    - «Incluir anuladas» (`Checkbox`).
  - Columnas: «Inicio», «Depósito», «Producto», «Camión», «Tipo», «Total», «Buena», «Dañada», «Faltante», «Sobrante», «Registrada por», «Estado» (`Tag` «Anulada» si `isVoided`), «Acciones» («Editar», «Imprimir», «Anular»).
  - Botón «Nueva novedad»: pide «Depósito» y «Producto» (de `GET warehouse/inventory/stock/{warehouseStorageId}`) y abre el formulario.
  - Vacío: «No hay novedades con estos filtros.»

  **Anular:** `ReasonDialog` (F3-02) con el título «Anular la novedad» y el botón «Anular novedad».

  **Imprimir:** abre el PDF en una pestaña nueva, igual que el tiquete (`useTicketPdf.ts`), con el nombre `novedad_{depósito}_{yyyyMMdd}.pdf`.

  **Comercio Exterior** (detalle del depósito): sección «Novedades» con la misma tabla en solo lectura (sin «Editar» ni «Anular») e «Imprimir».
- **Endpoints:**
  - **C-F4-08** `POST warehouse/novelties` → `{ warehouseStorageProductId, warehouseStorageEntryId?, type, startedAt, endedAt, orderedBy?, description, totalQuantity, goodQuantity, damagedQuantity, missingQuantity, surplusQuantity, isUnloaded, tarpCondition?, trailerCondition?, photoRecord? }`. 201 `WarehouseNoveltyDto` (todos esos campos, más `id`, `warehouseStorageId`, `warehouseStorageNumber`, `productName`, `vehiclePlate`, `unloadedQuantity`, `createdByName`, `createdAt`, `updatedAt`, `isVoided`, `voidedAt`, `voidReason`).
  - **C-F4-09** `PUT warehouse/novelties/{id}` (sin `warehouseStorageProductId`); 409 «La novedad está anulada.»
  - **C-F4-10** `POST warehouse/novelties/{id}/void` → `{ reason }`; 409 «La novedad ya está anulada.»
  - **C-F4-11** `GET warehouse/novelties` (query `warehouseStorageId`, `warehouseStorageProductId`, `type`, `from`, `to` en `yyyy-MM-dd`, `includeVoided`, paginado, `all`) y `GET warehouse/novelties/{id}`.
  - **C-F4-12** `GET warehouse/novelties/{id}/pdf` → PDF «REPORTE DE MERCANCÍAS», con la marca «ANULADA» si aplica.
  - `GET warehouse/receptions?warehouseStorageId={id}&all=true` (existente): cada recepción trae `warehouseStorageEntryId` y `vehiclePlate`.
  - Escritura `WarehouseAccess`; lectura y PDF, cualquier usuario autenticado.
- **Roles y menú:** «Novedades» `requiredRoles: ["Admin", "Warehouse", "Receiving"]` (los de las páginas de Bodega). Menú: Bodega › «Novedades», ícono `fa-triangle-exclamation`, `to: "/warehouse/novelties"`.
- **Invalidación:** `['warehouse', 'novelties']` tras crear, editar o anular. Claves `['warehouse', 'novelties', params]`. La sección de Comercio Exterior usa la misma clave.
- **Pruebas manuales:**
  1. Bodega › Inventario › «Registrar novedad» en un producto. → Total precargado con las existencias, tipo «Rutina».
  2. Registrar con dañada 2. → Aviso con «Comercio Exterior recibe el aviso»; aparece en el listado.
  3. Editar la descripción. → Se guarda.
  4. Imprimir. → PDF «REPORTE DE MERCANCÍAS».
  5. Anular con motivo. → «Anulada»; desaparece salvo con «Incluir anuladas»; el PDF dice «ANULADA».
  6. Comercio Exterior › detalle del depósito. → Sección «Novedades» en solo lectura.
- **Terminado cuando:** el ciclo completo de una novedad funciona y Comercio Exterior la ve.
- **Riesgo:** bajo.

---

#### F4-04 · Listas de empaque: carga del archivo del proveedor y asociación al camión (UI-12, GAP-013, RN-016)

- **Dificultad:** Alta.
- **Tarea del operario (Comercio Exterior):** cargar la lista de empaque que envía el proveedor (artículos, bultos y unidades por bulto) y asociar sus artículos al camión del depósito en lugar de digitarlos.
- **Cómo lo hacía en el legacy:**
  - carga del archivo por proveedor (`modulos/mod_listasempaque/cargarlistasempaque.php:59-124`);
  - listado de artículos activos con selección (`listararticulosactivos.php:230-238`);
  - marca de seleccionado (`marcarlistaseleccionada.php`);
  - unidades = bultos × unidades por bulto.
- **Lo que hace hoy la v2:** no existe.
- **Pantallas y componentes:**
  - `app/pages/foreign-trade/packing-lists/index.vue` (nuevo): pestañas «Archivos» y «Artículos».
  - `app/features/foreign-trade/components/PackingListUploadDialog.vue` (nuevo).
  - `app/features/foreign-trade/components/PackingListItemsDialog.vue` (nuevo): artículos de un archivo.
  - `app/features/foreign-trade/components/AssociatePackingListItemsDialog.vue` (nuevo).
  - `app/features/foreign-trade/composables/usePackingLists.ts` (nuevo) y `types/packing-list.ts` (nuevo).
  - `foreign-trade-service.ts` (modifica): usa `useApi().postForm` (F2-01).
  - `DepositExpandedEntriesTable.vue` (modifica): acción por camión.
  - `AppMenu.vue` (modifica).
- **Diseño de la interacción.**

  **Cargar lista** (botón «Cargar lista de empaque»):

  | Etiqueta | Control | Obligatorio | Validación y mensaje |
  |---|---|---|---|
  | Proveedor | `Select` filtrable de proveedores activos, y el botón «Nuevo proveedor» que abre un mini formulario «Nombre» (1 a 200) | Sí | «Seleccione el proveedor.» 409 «Ya existe el proveedor {nombre}.» |
  | Importador | `Select` filtrable de terceros con rol importador | Sí | «Seleccione el importador.» |
  | Archivo CSV | `FileUpload` básico, `.csv` | Sí | «Seleccione el archivo de la lista.» |
  | Filas de encabezado | `InputNumber` ≥ 0, por defecto 1 | Sí | — |

  - Ayuda: «Columnas en orden: codigo;NOMBRE;CANT_BULTOS;UNID_X_BULTOS;PSO_TOTAL_NETO. Separador ; (con coma decimal) o ,. UTF-8.»
  - «Simular»: tabla con «Fila», «Código», «Descripción», «Bultos», «Unid. x bulto», «Cantidad», «Peso neto (kg)», «Producto» y «Nuevo» (Sí si `newProduct`); resumen «Filas válidas {validRows} de {totalRows} · Productos nuevos: {productsToCreate}»; tabla de errores.
  - «Importar» (habilitado tras simular): aviso «Lista cargada: {totalRows} artículos».
  - Errores de archivo: 404 «El proveedor no existe o está inactivo.», 404 «El importador no existe.», 400 «El archivo no tiene filas válidas.», 409 «No se pudo generar un SKU único para el código {código}.»

  **Pestaña «Archivos»:**
  - Filtros «Importador» y «Proveedor».
  - Columnas «Archivo», «Proveedor», «Importador», «Artículos», «Activos», «Asociados», «Cargado por», «Fecha».
  - Acciones «Ver artículos» y «Eliminar» (confirmación; 409 «La lista {archivo} tiene artículos asociados a depósitos; no se puede eliminar.»).

  **Pestaña «Artículos»:**
  - Filtros «Importador» (obligatorio, con el mensaje «Seleccione el importador para ver sus artículos.»), «Estado» («Activos» por defecto, «Asociados») y «Buscar» (código o nombre, diferido).
  - Columnas «Código», «Descripción», «Bultos», «Unid. x bulto», «Cantidad», «Peso neto (kg)», «Archivo», «Proveedor», «Depósito · camión» (si está asociado).

  **Asociar al camión** (detalle del depósito, solo en Borrador): acción «Agregar artículos de lista de empaque» por fila de «Entradas al depósito». Diálogo «Artículos de lista de empaque para el camión {placa}»:
  - Importador: el del depósito; si el depósito no tiene, un `Select` «Importador» con la nota «El depósito tomará el importador de la lista.»
  - Tabla de artículos activos de ese importador (`status=Active`, `all=true`) con selección múltiple (`DataTable selection`, de 1 a 200) y buscador.
  - «Unidad de carga»: `Select` de las unidades de ese camión, **obligatorio si el depósito es de unidades de carga** («Indique la unidad de carga a la que entra el producto.»).
  - «Motivo» (convención 10).
  - Botón «Asociar».
  - Resultado: aviso «Se agregaron {n} productos al camión {placa}»; si `importerAssigned`, otro aviso «El depósito tomó el importador de la lista.»
  - Errores bajo el diálogo: 409 «El artículo {código} ya está asociado al depósito {n}.», 409 «Los artículos son de la lista del importador {x}; el depósito es del importador {y}.», 400 «Los artículos deben ser de un mismo importador.»
- **Endpoints:**
  - **C-F4-13** `GET foreign-trade/packing-list-suppliers` → `[{ id, name, isActive }]`; `POST` → `{ name }`.
  - **C-F4-14** `POST foreign-trade/packing-lists/import` (multipart: `file`, `supplierId`, `importerId`, `headerRows`, `dryRun`) → `{ dryRun, packingListFileId, totalRows, validRows, productsToCreate, items: [{ row, code, description, packages, unitsPerPackage, quantity, netWeightKg, productId, productName, newProduct }], errors: [{ row, message }] }`.
  - **C-F4-15** `GET foreign-trade/packing-lists` (query `importerId`, `supplierId`, paginado), `GET …/{id}` (con `items`) y `DELETE …/{id}`.
  - **C-F4-16** `GET foreign-trade/packing-list-items` (query `importerId` obligatorio, `status`, `search`, paginado, `all`) → `PackingListItemDto`.
  - **C-F4-17** `POST foreign-trade/deposits/{warehouseStorageId}/entries/{entryId}/packing-list-items` → `{ itemIds, warehouseStorageCargoUnitId, reason }`. 200 `{ importerAssigned, products: [{ warehouseStorageProductId, productName, declaredQuantity, entryDeclaredQuantity }] }`.
  - Todos con `ForeignTradeAccess`.
- **Roles y menú:** `requiredRoles: ["Admin", "ForeignTrade"]`. Menú: Comercio Exterior › «Listas de empaque», ícono `fa-list-check`, `to: "/foreign-trade/packing-lists"`.
- **Invalidación:** `['foreign-trade', 'packing-lists']` tras importar o eliminar; `['foreign-trade']` y `['products']` tras asociar o importar (se crean productos).
- **Pruebas manuales** (Comercio exterior):
  1. Crear el proveedor «PROV PRUEBA», cargar un CSV de 3 filas con una fila de bultos 0. → La simulación muestra 1 error; importar deja 2 artículos.
  2. «Artículos» del importador. → 2 activos.
  3. Depósito en Borrador del mismo importador: asociar los 2 al camión. → El depósito suma los productos y los artículos pasan a «Asociados».
  4. Asociarlos otra vez. → 409.
  5. Eliminar la lista. → 409 por tener asociados.
- **Terminado cuando:** se carga la lista real de un proveedor (insumo de la fase 0.5 del roadmap) y se asocia a un camión.
- **Riesgo:** formato de archivo distinto entre proveedores. Se mitiga con la simulación, que muestra fila por fila antes de importar.

---

#### F4-05 · Otras órdenes con el mismo pesaje de salida, sin cobro (UI-11, BAS-08, GAP-019, LEGACY-FUNC-119)

- **Dificultad:** **Muy alta.** Toca la operación de salida del banco de trabajo y su cobro.
- **Tarea del operario (báscula):** un camión carga mercancía de varias órdenes; pesarlo y cobrarlo una sola vez.
- **Cómo lo hacía en el legacy:** «Duplicar recibo» creaba N salidas «incompleto» copiando los pesos de la salida, con recibos en $0, hasta 10 (`modulos/mod_bascula/duplicarrecibo.php:60-72,103-110,122-138,287`).
- **Lo que hace hoy la v2:** una orden por entrada de portería.
- **Pantallas y componentes:**
  - `app/features/weighbridge/components/AdditionalOrdersDialog.vue` (nuevo).
  - `app/features/weighbridge/composables/useAddAdditionalOrders.ts` (nuevo).
  - `app/pages/operations/weighbridge/index.vue` (modifica): botón en el paso 3 de una salida.
  - `WeighbridgeHistoryTable.vue` y `history.vue` (modifica): órdenes adicionales en la fila y en el detalle.
  - Tipos (modifica): `IWeighbridgeHistory.additionalOrders`.
- **Diseño de la interacción.**
  - En el paso 3 (Peso) de una operación «Salida de mercancía» con ciclo, debajo del formulario de peso: botón «Agregar otra orden a este pesaje» (`severity="secondary" outlined`).
  - Diálogo «Otras órdenes del camión {placa}»:
    - tabla de las órdenes de esa placa (`getLoadingOrdersByPlate`, existente), sin la del ciclo, con selección múltiple (1 a 10) y las columnas «Orden», «Cliente», «Producto», «Cantidad» y «Estado»;
    - texto: «Salen con el pesaje de este camión, sin cobro adicional. Las órdenes ya cargadas quedan despachadas al terminar el pesaje.»;
    - botón «Agregar al pesaje».
  - Con más de 10: «Se pueden agregar entre 1 y 10 órdenes.»
  - Resultado: aviso por orden: «{loadingOrderNumber}: despachada» o «{loadingOrderNumber}: se despacha al completar el pesaje».
  - Errores 409 bajo la tabla: otro vehículo, estado, servicio de salida existente, depósitos sin confirmar, pesaje anulado.
  - No cambia el cobro ni el peso del ciclo (§A.5).
  - Historial (salidas): debajo de la orden principal, «También: OC-…, OC-…» (`additionalOrders`).
- **Endpoints:** **C-F4-18** `POST weighbridge/output/cycles/{cycleId}/additional-orders` → `{ loadingOrderIds }`. 200 `[{ serviceRecordId, loadingOrderId, loadingOrderNumber, customerName, dispatched }]`. Errores: 400 «Se pueden agregar entre 1 y 10 órdenes.», 400 «Solo se agregan órdenes a un pesaje de salida.», 400 «Los depósitos de la orden {n} deben estar confirmados.», 404, 409 «El pesaje está anulado.», 409 «La orden {n} está {estado}; no se puede agregar al pesaje.», 409 de vehículo y 409 «La orden {n} ya tiene un servicio de salida en báscula.» El historial agrega `additionalOrders: [{ serviceRecordId, loadingOrderId, loadingOrderNumber, customerName }]`.
- **Roles y menú:** sin cambios. **Invalidación:** `['weighbridge']`, `['weighbridgeHistory']`, `['weighbridge-history']` y `['foreign-trade']`.
- **Pruebas manuales** (Operario báscula):
  1. Dos órdenes cargadas para la placa `TST301`. Tomar el camión, «Salida de mercancía» con la primera, cobrar y registrar la tara.
  2. «Agregar otra orden a este pesaje» y elegir la segunda. → «se despacha al completar el pesaje».
  3. Registrar el bruto. → Ambas órdenes despachadas; una sola factura de báscula.
  4. Elegir una orden de otra placa (forzándola con el número). → 409.
  5. Repetir la prueba 9 de F1-05 (saltar entre camiones). → Sin pérdida de estado.
- **Terminado cuando:** dos órdenes salen con un pesaje y un cobro, y el historial lo muestra.
- **Riesgo:** despachar una orden no cargada. El backend solo despacha órdenes `Loaded`.

---

#### F4-06 · Salida con el tiquete de ingreso, desde báscula y desde Comercio Exterior (UI-11, BAS-09, GAP-019, LEGACY-FUNC-120 y 166, DF18)

- **Dificultad:** **Muy alta.** Agrega una salida sin cobro ni peso al banco de trabajo.
- **Tarea del operario:** sacar la mercancía de un camión que no se descargó (o se descarga y recarga en el momento) usando el tiquete con el que entró, sin pesarlo ni cobrarlo de nuevo. La «Salida Global» del legacy se hace camión por camión: una orden y una guía por camión.
- **Cómo lo hacía en el legacy:**
  - «Usar tiquete existente» desde báscula (`modulos/mod_bascula/usartiquete.php:60-115,185-194`: número del tiquete y «Usar y Continuar»);
  - desde Salidas (`mod_salidas/salidausartiquete.php:116-124`);
  - «Salida Global» con varios tiquetes de un depósito (`salidaglobal.php:151-170`; `listarpesajesglobal.php:54-68`).
- **Lo que hace hoy la v2:** no existe.
- **Pantallas y componentes:**
  - `app/features/weighbridge/components/EntryTicketExitPanel.vue` (nuevo): elección del tiquete en báscula.
  - `app/features/weighbridge/composables/useExitWithEntryTicket.ts` (nuevo).
  - `app/features/weighbridge/components/OutputServiceForm.vue` (modifica): opción «Salir con el tiquete de ingreso».
  - `app/pages/operations/weighbridge/index.vue` (modifica): cierre del flujo sin cobro ni peso.
  - `app/features/foreign-trade/components/ExitWithEntryTicketDialog.vue` (nuevo) y `composables/useExitWithEntryTicketFt.ts` (nuevo).
  - Páginas de detalle del depósito (modifica): acción en «Historial de Pesaje».
  - `WeighbridgeHistoryTable.vue` (modifica): «Salió con la orden {n}» en el tiquete de ingreso.
- **Diseño de la interacción.**

  **En báscula:** con la orden ya encontrada en `OutputServiceForm`, un `SelectButton` «Cómo sale» con «Pesar en báscula» (por defecto, flujo actual) y «Con el tiquete de ingreso (sin pesar ni cobrar)». Con la segunda opción:
  - Se ocultan la configuración de pesaje y el paso de cobro.
  - `EntryTicketExitPanel` lista los tiquetes de ingreso completos de la placa: `GET weighbridge/history` con `vehiclePlate`, `serviceType=Input`, `status=Complete` y `all=true`, sin los anulados (`isVoided`) ni los ya usados (`exitOrder` no nulo).
  - Columnas «Tiquete», «Fecha», «Carta porte», «Neto (kg)».
  - Vacío: «Este camión no tiene tiquetes de ingreso disponibles.»
  - Botón «Registrar salida con este tiquete» (Enter con una fila elegida).
  - Resultado: aviso «La orden {loadingOrderNumber} sale con el tiquete {ticketNumber}» y «Despachada» o «Se despacha al ejecutar el cargue»; la ficha muestra el bloque final con «Finalizar» (suelta el camión).
  - Errores 409 bajo el panel.

  **En Comercio Exterior** (DF18): en «Historial de Pesaje» del detalle del depósito, acción por fila «Salida con este tiquete». Diálogo «Salida con el tiquete {ticketNumber} · {placa}»:
  - órdenes de esa placa: `GET foreign-trade/loading-orders?searchField=LicensePlate&searchValue={placa}&all=true`, filtradas a los estados `Pending`, `InProgress` y `Loaded`;
  - selección de una orden y botón «Registrar salida»;
  - texto: «Cada camión sale con su propia orden y su propia guía. Se cobra una guía por camión.»;
  - vacío: «No hay órdenes pendientes para la placa {placa}. Cree la orden de cargue de este camión.» con el enlace «Crear orden de cargue».

  **Historial de báscula:** el tiquete de ingreso usado muestra «Salió con la orden {loadingOrderNumber}» (`exitOrder`).
- **Endpoints:** **C-F4-19**:
  - `POST weighbridge/output/from-entry-ticket` → `{ entryWeighbridgeCycleId, loadingOrderId }` (`ScaleAccess`);
  - `POST foreign-trade/loading-orders/{id}/exit-with-entry-ticket` → `{ entryWeighbridgeCycleId }` (`ForeignTradeAccess`).

  200 `{ serviceRecordId, loadingOrderId, loadingOrderNumber, ticketNumber, dispatched }`. Errores: 400 «El tiquete {t} no es de un ingreso.», 404 «El pesaje no existe.», 409 «El tiquete {t} no está completo.», «… está anulado.», «… ya se usó para la salida de la orden {o}.», de vehículo, «La orden {n} tiene mercancía del depósito {d}, que no llegó en el tiquete {t}.» y los de estado de C-F4-18. El historial agrega `exitOrder: { serviceRecordId, loadingOrderId, loadingOrderNumber } | null`. El detalle del depósito ya trae `weighbridgeCycles: [{ id, vehiclePlate, ticketNumber, … }]`.
- **Roles y menú:** sin cambios. **Invalidación:** `['weighbridge']`, `['weighbridgeHistory']`, `['weighbridge-history']` y `['foreign-trade']`.
- **Pruebas manuales:**
  1. Báscula: camión `TST401` con tiquete de ingreso completo del depósito D y una orden cargada de D para esa placa. «Salida de mercancía», buscar la orden, «Con el tiquete de ingreso», elegir el tiquete y registrar. → «Despachada», sin cobro ni peso.
  2. Repetir con el mismo tiquete. → No aparece en la lista.
  3. Comercio Exterior: en el detalle de D, «Salida con este tiquete» de otro camión y su orden. → Registrada.
  4. «Salida Global» de dos camiones del mismo depósito: dos órdenes (una por placa) y dos salidas con sus tiquetes. → Dos guías pendientes.
  5. Anular el tiquete usado (F3-01). → 409 «El tiquete {t} se usó para la salida de la orden {o}…».
- **Terminado cuando:** desde báscula y desde Comercio Exterior una orden sale con el tiquete de ingreso, y el historial lo muestra.
- **Riesgo:** usar el tiquete de otro camión. El backend compara vehículo y depósitos; la lista filtra por la placa.

---
### C.5 Fase 5 — Reportes y consultas

> **Estado: ✅ COMPLETADA en código (2026-10-02; commit `e7c8400`).** F5-01 a F5-11 implementados en `develop`. `npm run build` OK. Lint al cerrar la fase: **296 errores** (tope 300) y 0 errores en los archivos nuevos; la fase 6 (sin desarrollo de frontend) no toca este tope. Pendiente fuera del código: pruebas manuales en el navegador contra el backend local (`adb6af4` y migraciones de la fase 5).

- **Objetivo:** quien hoy saca un informe del legacy lo saca de la v2, con las mismas columnas y en Excel.
- **Criterio de salida (desde el operario):**
  1. Los listados de importaciones, exportaciones e inspecciones y los movimientos de inventario se exportan a Excel con **todas** las filas del filtro (más de 50).
  2. Están, con Excel:
     - el kardex con levantes;
     - el inventario general;
     - pólizas por año y mes;
     - ingresos por producto;
     - facturación anual y por CPI;
     - báscula por modalidad;
     - ingresos por agencia de aduanas.
  3. Comercio Exterior ve las columnas Ingreso, Nacionalizado, Por nacionalizar, Despachado y Existencias, busca por placa del camión y por levante, y tiene un listado de levantes.
- **Rama:** `develop` (DF1). **Empieza cuando la fase 4 tiene todos sus ítems con commit** (toca el historial de báscula y el inventario, que la fase 4 modifica).
- **Backend que debe estar corriendo:** commit `adb6af4` (fase 5) con las migraciones `ParidadF5_06_Uap` y `ParidadF5_09_TiqueteImpreso`.
- **Dificultad:** **Media.** Pantallas nuevas con contrato definido y una utilidad común de Excel.
- **Perfil de agente:** agente estándar.
- **Reglas comunes de los informes de esta fase:**
  - Filtros arriba y botón «Consultar». Los informes no consultan al abrir la página si tienen filtros obligatorios.
  - Las fechas de filtro viajan como `yyyy-MM-dd` (días de Colombia, inclusivos). Si la final es anterior a la inicial: «La fecha final no puede ser anterior a la inicial.»
  - Fila de totales con `totals` del backend, que cubren todo el filtro, no solo la página.
  - Tabla paginada (10, 20 o 50). Vacío: «No hay datos para los filtros elegidos.»
  - Botón «Exportar Excel» (`pi pi-file-excel`) con la utilidad de F5-01. Usa `all=true` y los mismos filtros. **Nunca** sube `pageSize`.
  - Consultas con clave `['reports', '{nombre}', params]` (o `['billing', …]` y `['foreign-trade', …]` según el módulo del endpoint).

---

#### F5-01 · Exportación a Excel sin tope de filas (UI-09, GAP-017, DF12)

- **Dificultad:** Media.
- **Tarea del operario:** bajar a Excel el listado completo que tiene en pantalla, con los filtros aplicados.
- **Cómo lo hacía en el legacy:** cada reporte tenía su exportación: `reportes/reporteexcel.php:1-26` entregaba la tabla del informe como `.xls`, con el logo arriba.
- **Lo que hace hoy la v2:**
  - `useExportImportsToExcel.ts` pide `pageSize: 10000` (`:14-18`), que el API recorta a 50, y usa `XLSX`, que no está instalado ni importado. Ninguna página lo usa.
  - El botón «Exportar Excel» de inventario (`pages/warehouse/inventory/index.vue:162-175,229-234`) llama a `warehouseService.exportInventoryMovementsToExcel`, que no existe (`features/warehouse/composables/useWarehouseExports.ts:35`): falla.
- **Pantallas y componentes:**
  - `package.json` (modifica): dependencia `exceljs` (`yarn add exceljs`).
  - `app/utils/excel-export.ts` (nuevo):
    - `exportRowsToExcel<T>({ fileName, sheetName, title, filtersSummary, columns, rows, totals })`;
    - `columns: { header: string; value: (row: T) => string | number | Date | null; width?: number; format?: 'text' | 'integer' | 'decimal' | 'currency' | 'date' | 'datetime' }[]`;
    - carga `exceljs` con `await import('exceljs')`;
    - fila 1 «BODEGAS ASOCIADAS — {title}»; fila 2 los filtros («Desde: … · Hasta: … · Importador: …»); encabezados en negrita con filtro automático; números como números; fechas en hora de Colombia; fila de totales en negrita;
    - descarga `{fileName}_{yyyyMMdd}.xlsx`.
  - `app/composables/useExcelExport.ts` (nuevo):
    - `useExcelExport()` → `{ exporting, run(fetchAll, options) }`;
    - `fetchAll` pide los datos con `all: true`, sin `pageIndex` ni `pageSize`;
    - avisos «No hay datos para exportar.» y «Excel generado: {n} filas».
  - `app/features/foreign-trade/composables/useExportImportsToExcel.ts` (elimina) y su exportación en `composables/index.ts` (modifica).
  - `app/pages/foreign-trade/{imports,exports,inspections}/index.vue` (modifica): botón «Exportar Excel» junto a «Volver».
  - `app/features/warehouse/composables/useWarehouseExports.ts` (modifica): `useInventoryExport` arma el Excel con `GET warehouse/inventory/movements` y `all=true`.
  - `IGetImportDepositsQuery` e `IGetExportDepositsQuery` (`foreign-trade-service.ts:48-82`), `IGetInspectionDepositsQuery` (`features/foreign-trade/types/inspection-deposit.ts:70`) e `IGetInventoryMovementsQuery` (`features/warehouse/types/inventory.ts:67-77`) (modifica): `all?: boolean`.
- **Columnas de cada Excel:**

  | Exportación | Columnas |
  |---|---|
  | Importaciones | N.º depósito, Cliente, Producto, Unidad, Ingreso, Nacionalizado, Por nacionalizar, Despachado, Existencias, Estado (Nacionalizado / Sin nacionalizar), Levantes, Fecha de ingreso. Las columnas de saldo llegan con F5-02: si F5-02 no está, se exportan las que haya. |
  | Exportaciones e inspecciones | N.º depósito, Cliente, Producto, Unidad, Ingreso, Despachado, Existencias, Estado, Fecha de ingreso. |
  | Movimientos de inventario | Fecha, N.º depósito, Producto, Descripción, Tipo, Cantidad, Stock anterior, Stock nuevo, Origen, Motivo / Observación, Usuario (las de la pestaña «Movimientos», `pages/warehouse/inventory/index.vue:480-540`). |

- **Endpoints:** **C-F5-14**. `GET foreign-trade/imports`, `…/exports`, `…/inspections` y `GET warehouse/inventory/movements`, todos con `all=true` y los filtros de pantalla.
- **Roles y menú:** sin cambios. **Invalidación:** no hay mutaciones.
- **Pruebas manuales:**
  1. Con más de 50 depósitos de importación (crear con báscula o cargar datos), «Exportar Excel» sin filtros. → El archivo trae todas las filas.
  2. Con el filtro «Importador». → Solo las de ese importador y el filtro anotado en la fila 2.
  3. Bodega › Inventario › «Exportar Excel». → Descarga los movimientos sin error.
  4. En la pestaña de red del navegador, ninguna petición lleva `pageSize` mayor que 50.
- **Terminado cuando:** las cuatro exportaciones descargan todas las filas, y `useExportImportsToExcel` y `exportInventoryMovementsToExcel` ya no existen en el código.
- **Riesgo:** listados enormes. Se mitiga con la carga diferida de la librería y el aviso con el número de filas.

---

#### F5-02 · Columnas de saldo en los listados de Comercio Exterior (UI-17)

- **Dificultad:** Baja.
- **Tarea del operario:** ver de un vistazo cuánto entró, cuánto está nacionalizado, cuánto falta y cuánto salió de cada depósito.
- **Cómo lo hacía en el legacy:** listados y kardex con «Ingreso / Nacionalizados / Por nacionalizar / Despachados / Existencias» (`modulos/mod_depositos/listardepositosprorroga.php:477-732`; `mod_inventario/kardex.php`).
- **Lo que hace hoy la v2:** el listado de importaciones solo trae «Stock» y «Estado» (`features/foreign-trade/components/ImportDepositList.vue:83-95`).
- **Pantallas y componentes:**
  - `ImportDepositList.vue`, `ExportDepositList.vue` e `InspectionDepositList.vue` (modifica).
  - `features/foreign-trade/types/import-deposit.ts`, `export-deposit.ts` e `inspection-deposit.ts` (modifica): `receivedQuantity`, `pendingToNationalize` (solo importación) y `dispatchedQuantity`.
- **Diseño:** en importación, la columna «Stock» se reemplaza por cinco columnas numéricas alineadas a la derecha, con la unidad: «Ingreso» (`receivedQuantity`), «Nacionalizado» (`nationalizedQuantity`), «Por nacionalizar» (`pendingToNationalize`, en ámbar si es > 0), «Despachado» (`dispatchedQuantity`) y «Existencias» (`currentStock`). En exportación e inspección: «Ingreso», «Despachado» y «Existencias».
- **Endpoints:** **C-F5-01**: cada fila de `GET foreign-trade/imports` agrega `receivedQuantity`, `pendingToNationalize` y `dispatchedQuantity` (`nationalizedQuantity` y `currentStock` ya existen); exportaciones e inspecciones agregan `receivedQuantity`, `dispatchedQuantity` y `currentStock`.
- **Roles y menú:** sin cambios. **Invalidación:** no aplica.
- **Pruebas manuales:**
  1. Un depósito con 100 de ingreso, 30 nacionalizados y 20 despachados. → 100, 30, 70, 20 y 80.
  2. Exportación. → Tres columnas.
- **Terminado cuando:** las columnas aparecen en los tres listados y en sus Excel.
- **Riesgo:** bajo.

---

#### F5-03 · Búsqueda por placa del camión y por levante; listado de levantes (UI-18)

- **Dificultad:** Media.
- **Tarea del operario (Comercio Exterior):** encontrar un depósito por la placa del camión que lo trajo o por el número de levante o de aceptación, y consultar los levantes de todos los depósitos.
- **Cómo lo hacía en el legacy:**
  - selector «buscar por» con vehículo (`modulos/mod_depositos/listardepositos.php`, filtro `filtro`);
  - «Levantes Import.» con búsqueda por número de levante o aceptación (`modulos/mod_levantes/listarlevantes.php`).
- **Lo que hace hoy la v2:** el panel de filtros tiene «Placa de unidad de carga», pero no la del camión ni el levante (`features/foreign-trade/components/DepositFiltersPanel.vue:137-290`). No hay listado de levantes.
- **Pantallas y componentes:**
  - `DepositFiltersPanel.vue` (modifica): dos campos nuevos.
  - `useDepositFiltersQuery.ts` y `IGetImportDepositsQuery` (modifica): `vehiclePlate` y `releaseNumber`.
  - `app/pages/foreign-trade/releases/index.vue` (nuevo): «Levantes».
  - `app/features/foreign-trade/composables/useReleases.ts` (nuevo) y `types/release-list.ts` (nuevo).
  - `AppMenu.vue` (modifica).
- **Diseño de la interacción.**

  **Filtros nuevos**, después de «Placa de unidad de carga»:
  - «Placa del camión» (`InputText`, mayúsculas, se envía sin guiones ni espacios);
  - «Levante o aceptación» (`InputText`).

  Solo en el listado de importaciones (el backend solo los aplica ahí). Aparecen como chips de filtro, como los demás.

  **Pantalla «Levantes»:**
  - Filtros: «Levante o aceptación», «Depósito», «Importador», «Agencia de aduanas», «Desde» y «Hasta» (fecha del levante).
  - Columnas, por fecha del levante descendente: «Levante», «Fecha», «Aceptación», «Fecha de aceptación», «Depósito» (enlace a `/foreign-trade/imports/{importWarehouseStorageId}`), «Importador», «Agencia de aduanas», «Producto», «Cantidad», «Peso (kg)», «FOB (USD)», «Tasa», «FOB (COP)».
  - «Exportar Excel».
- **Endpoints:**
  - **C-F5-01** `GET foreign-trade/imports` con `vehiclePlate` (algún camión del depósito con esa placa, búsqueda parcial) y `releaseNumber` (levante o aceptación, búsqueda parcial).
  - **C-F5-02** `GET foreign-trade/releases` (query `releaseNumber`, `warehouseStorageNumber`, `importerId`, `customsAgencyId`, `fromDate`, `toDate`, paginado, `all`). Fila: `{ releaseId, releaseNumber, releaseDate, acceptanceNumber, acceptanceDate, warehouseStorageId, importWarehouseStorageId, warehouseStorageNumber, importerName, customsAgencyName, productName, releasedQuantity, releasedWeight, fobUsd, exchangeRate, fobCop, createdAt }`.
- **Roles y menú:** «Levantes» `["Admin", "ForeignTrade"]`; menú Comercio Exterior › «Levantes», ícono `fa-flag-checkered`, `to: "/foreign-trade/releases"`.
- **Invalidación:** no aplica (la clave `['foreign-trade', 'releases', params]` cae bajo el prefijo que invalidan las mutaciones de levantes).
- **Pruebas manuales:**
  1. Filtrar importaciones por «Placa del camión» `TST1`. → Los depósitos con un camión `TST101`.
  2. Filtrar por «Levante o aceptación» `LEV-1`. → El depósito del levante.
  3. «Levantes» con rango de fechas. → Los levantes, con su FOB.
- **Terminado cuando:** las dos búsquedas y el listado funcionan.
- **Riesgo:** bajo.

---

#### F5-04 · Kardex con levantes y despachos (UI-20, GAP-016, LEGACY-FUNC-209)

- **Dificultad:** Media.
- **Tarea del operario:** ver el kardex de un depósito con lo que entró, lo nacionalizado, lo despachado y el saldo, con el detalle de levantes y salidas.
- **Cómo lo hacía en el legacy:** `modulos/mod_inventario/kardex.php`, con ingreso, nacionalizados, por nacionalizar, despachados y existencias por producto, y los levantes y salidas del depósito.
- **Lo que hace hoy la v2:** «Movimientos por Depósito» (`pages/reports/warehouse-movements.vue:317-400`) muestra «Ampara, Entradas, Salidas, Saldo» y los movimientos, sin levantes.
- **Pantallas y componentes:** `pages/reports/warehouse-movements.vue` (modifica); `features/reports/types/*` del informe (modifica); `useWarehouseStorageMovements.ts` (sin cambio de clave).
- **Diseño:**
  - **Tabla por producto:** «Producto», «Unidad», «Ingreso», «Nacionalizado», «Por nacionalizar», «Nacionalizado disponible», «Despachado», «Existencias». Las tres de nacionalización solo en importación. Se conserva el detalle de movimientos que ya se expande por producto.
  - **Totales:** una fila con `totals`.
  - **Sección «Levantes»** (solo importación): «Levante», «Aceptación», «Fecha», «Peso (kg)», «FOB (USD)» y una columna por producto con la cantidad de `lines`.
  - **Sección «Despachos»:** «Orden», «Fecha de salida», «Placa», «Guía», «Tiquete» y una columna por producto con la cantidad.
  - «Exportar PDF» se conserva (el PDF del backend ya trae las secciones).
  - Nuevo «Exportar Excel» con tres hojas: «Productos», «Levantes» y «Despachos». La utilidad de F5-01 recibe varias hojas: agregarlo como `sheets: [...]`.
- **Endpoints:** **C-F5-03** `GET warehouse/movements-report` (`warehouseStorageNumber`, `fromDate`, `toDate`). Cada producto agrega `receivedQuantity`, `dispatchedQuantity`, `nationalizedQuantity`, `pendingToNationalize` y `nationalizedAvailable` (nulos fuera de importación). El informe agrega:
  - `releases: [{ releaseNumber, acceptanceNumber, releaseDate, releasedWeight, fobUsd, lines: [{ warehouseStorageProductId, quantity }] }]`;
  - `dispatches: [{ loadingOrderNumber, departureDate, vehiclePlate, guideNumber, ticketNumber, lines: [{ warehouseStorageProductId, quantity }] }]`;
  - `totals: { receivedQuantity, nationalizedQuantity, pendingToNationalize, dispatchedQuantity, currentStock, nationalizedAvailable }`.

  Ingreso − despachado = existencias.
- **Roles y menú:** sin cambios (`["Admin", "Warehouse", "ForeignTrade"]`).
- **Invalidación:** no aplica.
- **Pruebas manuales:**
  1. Depósito de importación con dos levantes y una salida. → Las tres secciones; la suma cuadra.
  2. Depósito de exportación. → Sin columnas ni sección de levantes.
  3. «Exportar Excel». → Tres hojas.
- **Terminado cuando:** el kardex muestra levantes y despachos y se exporta.
- **Riesgo:** bajo.

---

#### F5-05 · Inventario general filtrable (UI-20, GAP-016, LEGACY-FUNC-211)

- **Dificultad:** Media.
- **Tarea del operario:** sacar el inventario general por importador, agencia, transportadora, producto, modalidad o ubicación, con o sin saldo.
- **Cómo lo hacía en el legacy:** `modulos/mod_inventario/reportegeneral.php`, con los rótulos Depósito, F. Depósito, C.P.I., Manifiesto, Descripción producto, Importador, SIA/Intermediario, Bodega(s), Entran, Nalzdos., Salen, Saldo y Levantes.
- **Lo que hace hoy la v2:** no hay un informe único filtrable.
- **Pantallas y componentes:** `app/pages/reports/general-inventory.vue` (nuevo); `reports-service.ts` (modifica); `features/reports/types/general-inventory.ts` y `composables/useGeneralInventory.ts` (nuevos); `AppMenu.vue` (modifica).
- **Diseño:**
  - Filtros:
    - «Saldo»: `SelectButton` «Con saldo» (por defecto) / «Todos»;
    - «Desde» y «Hasta» (fecha de ingreso), **obligatorios con «Todos»**: «Indique el rango de fechas para consultar todo el inventario.»;
    - «Importador», «Agencia de aduanas», «Transportadora» y «Producto»;
    - «Modalidad»: Importación, Exportación, Inspección;
    - «Ubicación»;
    - «Incluir levantes» (`Checkbox`).
  - Columnas, con los rótulos del legacy: «Depósito», «F. Depósito», «C.P.I.» (carta porte), «Manifiesto», «Descripción producto», «Embalaje», «Importador», «SIA/Intermediario», «Bodega(s)» (`locations`), «Entran», «Nalzdos.» («—» fuera de importación), «Salen», «Saldo», «Levantes» (solo si se pidió).
  - Fila de totales. «Exportar Excel».
- **Endpoints:** **C-F5-04** `GET reports/general-inventory` (query `balanceType` = `WithBalance` | `All`, `fromDate`, `toDate`, `importerId`, `customsAgencyId`, `transportCompanyId`, `productId`, `operationModalityCode` = `IMP` | `EXP` | `INSP`, `warehouseLocationId`, `includeReleases`, paginado, `all`). Fila: `{ warehouseStorageNumber, entryDate, cargoManifestNumber, manifestNumber, productName, packagingName, importerName, customsAgencyName, locations, receivedQuantity, nationalizedQuantity, dispatchedQuantity, currentStock, releaseNumbers }`; `totals: { receivedQuantity, nationalizedQuantity, dispatchedQuantity, currentStock }`. Política `ActiveUser`.
- **Roles y menú:** `requiredRoles: ["Admin", "ForeignTrade", "Warehouse"]`. Menú: Comercio Exterior › Reportes › «Inventario general», y Bodega › «Inventario general».
- **Invalidación:** no aplica.
- **Pruebas manuales:**
  1. «Con saldo» sin filtros. → Solo depósitos con existencias.
  2. «Todos» sin fechas. → Mensaje del rango.
  3. «Incluir levantes». → Aparece la columna «Levantes».
  4. Excel con más de 50 filas. → Completo.
- **Terminado cuando:** el informe filtra como el legacy y se exporta.
- **Riesgo:** bajo.

---

#### F5-06 · Pólizas por año y mes, y marca UAP del tercero (UI-20, GAP-016, LEGACY-FUNC-215, P12)

- **Dificultad:** Media.
- **Tarea del operario:** sacar el «Informe de póliza»: el valor FOB en dólares de lo ingresado, por mes, separado entre usuarios aduaneros permanentes (UAP) y no UAP.
- **Cómo lo hacía en el legacy:** `modulos/mod_inventario/reportepoliza.php:230`: informe por año con las columnas «CIF UAP» y «CIF NUAP» (en realidad suma el FOB en dólares), con firmas «Firma Funcionario», «Jefe del Depósito» y «Recibí conforme». El cliente tenía la marca `uap`.
- **Lo que hace hoy la v2:** no existe; el tercero no tiene marca UAP.
- **Pantallas y componentes:**
  - `app/pages/reports/policies.vue` (nuevo); `reports-service.ts` (modifica); `features/reports/types/policies.ts` y `composables/usePolicies.ts` (nuevos).
  - `features/stakeholders/components/StakeholderForm.vue` (modifica): campo UAP; `features/stakeholders/types/stakeholder.ts` (modifica): `isUap: boolean`.
  - `AppMenu.vue` (modifica).
- **Diseño:**
  - **Tercero** (crear y editar): `Checkbox` «UAP (usuario aduanero permanente)», debajo de «Estado Comercial». Por defecto desmarcado.
  - **«Informe de póliza»:**
    - filtro «Año» (`InputNumber` de 2000 a 2100, por defecto el actual): «El año debe estar entre 2000 y 2100.»;
    - tabla de 12 meses con «Mes» (enero…diciembre), «FOB UAP (USD)», «FOB no UAP (USD)» y «Total (USD)», más la fila de totales. Rótulo del encabezado: «Valor FOB de los levantes (USD)»;
    - clic en un mes abre «Detalle de {mes} {año}» con el filtro «UAP» (Todos, UAP, No UAP) y las columnas «Fecha de ingreso», «Depósito», «Carta porte», «Manifiesto», «Unidades de carga», «Importador», «Agencia de aduanas», «Producto», «Ingreso», «Nacionalizado», «Despachado», «Existencias», «Levante», «Aceptación», «Fecha del levante», «FOB (USD)», «UAP» (Sí/No), y el total del FOB;
    - «Exportar Excel» del resumen (con las tres líneas de firma al pie: «Firma Funcionario», «Jefe del Depósito», «Recibí conforme») y del detalle.
- **Endpoints:**
  - **C-F5-05** `GET reports/policies?year=` → `{ year, months: [{ month, uapValueUsd, nonUapValueUsd, totalValueUsd }] (12), totals: { uapValueUsd, nonUapValueUsd, totalValueUsd } }`.
  - **C-F5-06** `GET reports/policies/detail` (query `year`, `month`, `uap`, paginado, `all`) → `{ items: [{ entryDate, warehouseStorageNumber, cargoManifestNumber, manifestNumber, cargoUnitPlates, importerName, customsAgencyName, productName, receivedQuantity, nationalizedQuantity, dispatchedQuantity, currentStock, releaseNumber, acceptanceNumber, releaseDate, fobUsd, isUap }], totals: { fobUsd } }`. Error «El mes debe estar entre 1 y 12.»
  - **C-F5-07** `POST stakeholder` y `PATCH stakeholder/{id}` aceptan `isUap`; `GET stakeholder` lo devuelve.
  - Cálculo: mes de ingreso del depósito; suma del FOB de sus levantes; UAP según el importador.
- **Roles y menú:** `["Admin", "ForeignTrade"]`; menú Comercio Exterior › Reportes › «Informe de póliza».
- **Invalidación:** el formulario de tercero conserva la suya (`['stakeholder']`).
- **Pruebas manuales:**
  1. Marcar un importador como UAP. → Al reabrirlo, la casilla sigue marcada.
  2. Levantes con FOB de ese importador en marzo. → Marzo suma en «FOB UAP».
  3. Detalle de marzo filtrado «No UAP». → Sin sus levantes.
- **Terminado cuando:** el informe y su detalle cuadran con los FOB registrados (F2-06).
- **Riesgo:** rótulo «CIF» del legacy. Se usa «FOB», que es lo que suma (§G).

---

#### F5-07 · Ingresos por producto y cliente (UI-20, GAP-016, LEGACY-FUNC-216)

- **Dificultad:** Baja.
- **Tarea del operario:** ver cuánto ingresó de cada producto para un importador en un rango.
- **Cómo lo hacía en el legacy:** `modulos/mod_inventario/reporteingresoproductocliente.php:90`.
- **Lo que hace hoy la v2:** el diario de ingresos solo filtra por fechas.
- **Pantallas y componentes:** `app/pages/reports/incoming-by-product.vue` (nuevo); `features/reports/services/reports-service.ts` (modifica: `getIncomingByProduct`); `features/reports/types/incoming-by-product.ts` y `composables/useIncomingByProduct.ts` (nuevos); `AppMenu.vue` (modifica).
- **Diseño:**
  - Filtros obligatorios «Desde», «Hasta» e «Importador»; «Producto» opcional. Mensajes «Indique el rango de fechas.» y «Seleccione el importador.»
  - Columnas «Producto», «Embalaje» y «Cantidad», con la fila de totales.
  - «Exportar Excel».
- **Endpoints:** **C-F5-08** `GET reports/incoming-by-product` (query `fromDate`, `toDate`, `importerId`, `productId`, paginado, `all`) → `{ items: [{ productId, productName, packagingName, quantity }], totals: { quantity } }`.
- **Roles y menú:** `["Admin", "ForeignTrade"]`; menú Comercio Exterior › Reportes › «Ingresos por producto».
- **Invalidación:** no aplica.
- **Pruebas manuales:**
  1. Un importador con dos depósitos de cebolla en el rango. → Una fila con la suma.
  2. Sin importador. → Mensaje.
- **Terminado cuando:** el informe y su Excel funcionan.
- **Riesgo:** bajo.

---

#### F5-08 · Facturación anual e informe por CPI (UI-20, GAP-016, LEGACY-FUNC-206 y 207)

- **Dificultad:** Media.
- **Tarea del operario (Facturación):** sacar la facturación de un año por mes y día, por servicio, y el informe de facturación de un depósito (CPI).
- **Cómo lo hacía en el legacy:**
  - «Informe de Facturación» por año, con PDF y Excel (`modulos/mod_facturacion/informefacturacion.php`);
  - «Informe por CPI» (`informecpi.php`).
- **Lo que hace hoy la v2:** tablero y listado de facturas, sin informe exportable. El resumen del depósito vive en Depósitos pendientes.
- **Pantallas y componentes:**
  - `app/pages/billing/reports/annual.vue` (nuevo) y `app/pages/billing/reports/deposit-billing.vue` (nuevo).
  - `app/features/billing/services/billing-service.ts` (modifica), `types/billing-reports.ts` (nuevo) y `composables/useBillingReports.ts` (nuevo).
  - `AppMenu.vue` (modifica).
- **Diseño.**

  **«Facturación anual»:**
  - Filtros «Año» (obligatorio) y «Servicio»: Almacenamiento (por defecto), Báscula, Montacargas, Guía de salida.
  - Tabla por mes con «Mes», «Facturas» y «Total»; cada mes se expande en sus días («Día», «Facturas», «Total»).
  - Fila de totales y «Exportar Excel» (una fila por día, con el mes).
  - Nota bajo el título: «Facturas con número SIIGO y no anuladas, por fecha de emisión.»

  **«Facturación por CPI»:**
  - Filtro «Depósito» (`InputText`, obligatorio, número `2026BA…`). 404 «No se encontró el depósito '{número}'.»
  - Encabezado: carta porte, importador, fecha de ingreso, agencia de aduanas, manifiesto y TRM de ingreso.
  - Tablas:
    - «Productos»: «Producto», «Ingreso», «Despachado», «Existencias»;
    - «Salidas»: «Placa», «Tiquete», «Fecha»;
    - «Facturas»: «Factura» (número o «Sin número»), «Fecha», «Inicio», «Fin», «Fecha límite», «Facturado a», «Total», «Estado», «Notas», «Refacturada como».
  - «Total facturado» (`invoicesTotal`, sin anuladas). «Exportar Excel» con tres hojas.
- **Endpoints:**
  - **C-F5-09** `GET reports/billing-annual` (query `year`, `serviceCategory` = `Almacenamiento` | `Bascula` | `Montacargas` | `GuiaSalida`) → `{ year, serviceCategory, months: [{ month, invoiceCount, totalAmount, days: [{ day, invoiceCount, totalAmount }] }], totals: { invoiceCount, totalAmount } }`.
  - **C-F5-10** `GET reports/deposit-billing?warehouseStorageNumber=` → `{ warehouseStorageNumber, cargoManifestNumber, importerName, entryDate, customsAgencyName, manifestNumber, entryTrm, products: [{ productName, receivedQuantity, dispatchedQuantity, currentStock }], dispatches: [{ vehiclePlate, ticketNumber, departureDate }], invoices: [{ invoiceId, invoiceNumber, invoiceDate, periodStart, periodEnd, limitDate, billedTo, total, status, notes, reissuedAsInvoiceNumber }], invoicesTotal }`.
  - Política `BillingAccess`.
- **Roles y menú:** `["Admin", "Billing"]`. Menú: Facturación › «Facturación anual» y «Facturación por CPI».
- **Invalidación:** no aplica. Claves `['billing', 'reports', 'annual', params]` y `['billing', 'reports', 'deposit', número]`.
- **Pruebas manuales:**
  1. Año actual, «Almacenamiento». → Los meses con facturas con número SIIGO.
  2. Expandir un mes. → Sus días.
  3. CPI de un depósito refacturado (F3-08). → La anulada con «Refacturada como …» y el total sin la anulada.
- **Terminado cuando:** los dos informes funcionan y se exportan.
- **Riesgo:** bajo.

---

#### F5-09 · Báscula por modalidad: filtros, pesos, totales y Excel (UI-20, GAP-016, LEGACY-FUNC-121)

- **Dificultad:** Media.
- **Tarea del operario (báscula):** sacar el reporte de pesajes del legacy: por fechas, cliente, transportadora, modalidad y placa, con los «en ceros», «por cobrar» y «no impresos», con pesos, pagos y totales.
- **Cómo lo hacía en el legacy:** `modulos/mod_bascula/reporteingresos.php`.
  - Filtros: Desde, Hasta, Otros filtros («en ceros», «por cobrar», «no impresos»), Cliente / Importador, Emp. Transporte, Modalidad y Placa Vehículo.
  - Columnas: #, Ticket #, Fact. Siigo, Fecha, Modalidad, Vehículo, Conductor, P. Bruto, Neto, Tara, Repesa, # Impr., Pago, Cambio y Subtotal, con la fila «TOTALES».
- **Lo que hace hoy la v2:** el historial filtra por placa, cliente, factura, tiquete, carta porte, estado, tipo y fechas (`features/weighbridge/types/requests.ts:300-312`), sin pesos de entrada y salida ni totales.
- **Pantallas y componentes:**
  - `WeighbridgeHistoryTable.vue` (modifica): filtros avanzados y columnas.
  - `pages/operations/weighbridge/history.vue` (modifica): totales y Excel.
  - `useWeighbridgeHistory.ts` (modifica) y `useWeighbridgeHistoryTotals.ts` (nuevo).
  - Tipos (modifica): filtros y campos nuevos.
- **Diseño:**
  - **Filtros avanzados nuevos:**
    - «Modalidad» (`Select` de modalidades, `useOperationModalities`);
    - «Transportadora» y «Cliente» (`Select` filtrables, que reemplazan el texto de cliente por `customerId`);
    - tres casillas: «En ceros», «Por cobrar» y «No impresos».
  - **Columnas nuevas:** «Bruto (kg)», «Tara (kg)», «Neto (kg)», «Repesaje» (Sí/No), «Subtotal», «IVA», «Efectivo», «Cambio» e «Impreso» (fecha de la primera impresión o «No»).
  - **Barra de totales** sobre la tabla (C-F5-11 totals): «Pesajes: {count} · Neto: {netWeightKg} kg · Subtotal: {subtotal} · IVA: {taxAmount} · Total: {total}». Se recalcula con los filtros.
  - **«Exportar Excel»** con las columnas del legacy en su orden, más la fila de totales.
  - Las filas anuladas (F3-01) siguen marcadas.
- **Endpoints:** **C-F5-11**:
  - `GET weighbridge/history` y `GET weighbridge/history/totals`, con los filtros nuevos `operationModalityId`, `transportCompanyId`, `customerId`, `zeroValue`, `pendingPayment` y `notPrinted`;
  - cada fila agrega `grossWeightKg`, `tareWeightKg`, `netWeightKg`, `reweighed`, `subtotal`, `taxAmount`, `cashReceived`, `changeGiven` y `ticketFirstPrintedAt`;
  - totales `{ count, netWeightKg, subtotal, taxAmount, total }`;
  - el tiquete queda «impreso» la primera vez que se genera su PDF.
- **Roles y menú:** sin cambios (`["Admin", "Scale"]`).
- **Invalidación:** las mutaciones de báscula ya invalidan `['weighbridge-history']`. La consulta de totales usa la clave `['weighbridge-history', 'totals', filtros]` para caer bajo esa invalidación.
- **Pruebas manuales:**
  1. Filtrar por modalidad Importación y un mes. → Pesajes y totales de esa modalidad.
  2. «No impresos». → Solo los tiquetes nunca impresos; imprimir uno y recargar. → Sale de la lista.
  3. «Por cobrar». → Los de factura con saldo.
  4. Excel. → Columnas del legacy y totales.
- **Terminado cuando:** el historial reemplaza al reporte de báscula del legacy.
- **Riesgo:** bajo.

---

#### F5-10 · Ingresos por agencia de aduanas (UI-16, GAP-010, LEGACY-FUNC-229)

- **Dificultad:** Media.
- **Tarea del operario (Comercio Exterior):** consultar, para una agencia de aduanas, sus depósitos con pesajes, novedades y salidas.
- **Cómo lo hacía en el legacy:** portal `reportesweb`: listado de ingresos de la SIA (`reportesweb/reportesias.php:36-50`) y detalle (`reportesiasdetalle.php`). El acceso externo de las agencias es del dominio de acceso (fuera de alcance): aquí solo el reporte.
- **Lo que hace hoy la v2:** no existe.
- **Pantallas y componentes:** `app/pages/reports/customs-agency-entries.vue` (nuevo); `features/reports/services/reports-service.ts` (modifica: `getCustomsAgencyEntries`, `getCustomsAgencyEntryDetail`); `features/reports/types/customs-agency-entries.ts` y `composables/useCustomsAgencyEntries.ts` (nuevos); `AppMenu.vue` (modifica).
- **Diseño:**
  - Filtro «Agencia de aduanas» (obligatorio): «Seleccione la agencia de aduanas.»
  - Columnas: «Carta porte», «Importador», «Productos», «Ingreso», «Fecha de ingreso», «Proceso» («Báscula» si el depósito está en Borrador, «Depósito» si no).
  - Clic en la fila: diálogo «Depósito {número}» con tres tablas:
    - «Pesajes»: «Tiquete», «Placa», «Fecha», «Bruto», «Tara», «Neto»;
    - «Novedades»: «Inicio», «Tipo», «Producto», «Buena», «Dañada», «Faltante», «Sobrante», con «Imprimir» (F4-03);
    - «Salidas»: «Fecha», «Placa», «Cantidad», «Saldo anterior», «Salida de portería», «Guía».
  - Nota: «Un depósito sin existencias solo aparece si tuvo una salida en las últimas 13 horas.»
  - «Exportar Excel» del listado.
- **Endpoints:**
  - **C-F5-12** `GET reports/customs-agency-entries` (query `customsAgencyId` obligatorio, paginado, `all`). Fila: `{ warehouseStorageId, cargoManifestNumber, importerName, products, receivedQuantity, entryDate, process }`.
  - **C-F5-13** `GET reports/customs-agency-entries/{warehouseStorageId}?customsAgencyId=` → `{ warehouseStorageNumber, cargoManifestNumber, importerName, weighings: [{ ticketNumber, vehiclePlate, date, grossWeightKg, tareWeightKg, netWeightKg }], novelties: [WarehouseNoveltyDto], exits: [{ date, vehiclePlate, quantity, previousBalance, gateDepartureAt, guideNumber }] }`. 404 «El depósito no existe o no es de esta agencia.»
- **Roles y menú:** `["Admin", "ForeignTrade"]`; menú Comercio Exterior › Reportes › «Ingresos por agencia de aduanas».
- **Invalidación:** no aplica.
- **Pruebas manuales:**
  1. Agencia con dos depósitos, uno en Borrador. → «Báscula» y «Depósito».
  2. Abrir el detalle. → Pesajes, novedades y salidas.
- **Terminado cuando:** el reporte y su detalle funcionan.
- **Riesgo:** bajo.

---

#### F5-11 · Excel en los demás listados del contrato (UI-09, C-F5-14)

- **Dificultad:** Baja.
- **Tarea del operario:** exportar a Excel los listados que el legacy exportaba y que llegaron en fases anteriores.
- **Cómo lo hacía en el legacy:** cada reporte se exportaba con `reportes/reporteexcel.php:1-26`.
- **Pantallas que agregan «Exportar Excel»** (utilidad de F5-01, `all=true`, mismos filtros):

  | Pantalla | Endpoint | Columnas |
  |---|---|---|
  | Abandono y prórrogas (F2-07) | `GET foreign-trade/abandonment` | las de la tabla |
  | Mercancía en abandono (F2-08) | `GET reports/abandonment-candidates` | las de la tabla y los totales |
  | Salidas a destino de abandono (F2-08) | `GET reports/abandonment-exits` | las de la tabla |
  | Órdenes de cargue (`pages/foreign-trade/loading-orders/index.vue`) | `GET foreign-trade/loading-orders` | las de la tabla |
  | Guías de salida (`pages/foreign-trade/dispatch-guides/index.vue`) | `GET foreign-trade/dispatch-guides` | las de la tabla y «Anulada» |
  | Facturas (`pages/billing/invoices/index.vue`) | `GET billing/invoices` | las de la tabla |
  | Novedades (F4-03) | `GET warehouse/novelties` | las de la tabla |

- **Endpoints:** los listados ya existentes, con `all=true` (agregar `all?: boolean` a sus tipos de consulta si falta).
- **Roles y menú:** sin cambios. **Invalidación:** no aplica.
- **Pruebas manuales:**
  1. En cada pantalla, con más de 50 filas, «Exportar Excel». → Todas las filas.
  2. Revisar la pestaña de red. → Sin `pageSize` > 50.
- **Terminado cuando:** las siete pantallas exportan completo.
- **Riesgo:** bajo.

---

### C.6 Fase 6 — Migración de datos y corte (sin desarrollo de frontend, DF3)

> **Estado: ✅ Revisada (2026-10-02), sin cambios de código (DF3).** El frontend en `e7c8400` ya cubre las pantallas que usa la verificación (F1-01, F2-03, F2-07, F4-02, F5-02 y depósitos pendientes de Facturación). Backend requerido: `bf64de1` con `ParidadF6_01_ImportacionLegacy` y `ParidadF6_05_Respaldos`. Pendiente fuera del código: la carga por API (C-F6-01 a C-F6-07) y la verificación por rol con los datos migrados, que hace el usuario con cada operario.

- **Objetivo:** confirmar que la interfaz muestra bien los datos migrados del legacy.
- **Criterio de salida (desde el operario):** con los maestros, depósitos vivos y levantes cargados por API, cada rol abre sus pantallas con datos reales y los saldos que ve en la v2 son los de la conciliación.
- **Rama:** no aplica: no hay cambios de código ni commits.
- **Backend:** commit `bf64de1` (fase 6) con las migraciones `ParidadF6_01_ImportacionLegacy` y `ParidadF6_05_Respaldos`. La carga se hace con los endpoints C-F6-01 a C-F6-07 desde Swagger o scripts, en el orden del contrato: ciudades, embalajes, cuadrillas, ubicaciones, clientes, agencias, transportadoras, vehículos, conductores, productos, depósitos y levantes. Las ciudades y las cuadrillas también se pueden cargar o corregir desde las pantallas de F2-01 y F4-01.
- **Dificultad:** — (no hay código). La verificación la hace el usuario con cada operario.
- **Verificación con datos migrados** (una sesión por rol, con la base cargada):
  1. **Comercio Exterior:**
     - listado de importaciones con las columnas de saldo (F5-02) de diez depósitos migrados;
     - comparar con el legacy;
     - abrir uno y ver sus levantes con FOB;
     - registrar un levante nuevo;
     - crear una orden con el tope de nacionalizado (F2-03).
  2. **Bodega:** inventario y ubicaciones de un depósito migrado (F4-02).
  3. **Facturación:** depósitos pendientes y períodos de un migrado tras la apertura de facturación (C-F6-04).
  4. **Báscula:** un camión adicional para un documento migrado. → Se asocia al depósito migrado (F1-01).
  5. **Abandono:** la pantalla de F2-07 con los depósitos migrados en ventana.
- **Observación:** el número legacy del depósito (`legacy_number`) no viaja en los DTO de la v2: el operario no lo ve en la interfaz (§G).

---

### C.7 Fase 7 — Comodidad (P3, opcional)

> **Estado: ✅ COMPLETADA en código (2026-10-02; sin commit).** F7-01 a F7-03 implementados en `develop`. `npm run build` OK. Lint al cerrar la fase: **296 errores** (igual al tope de la fase 6; sin regresiones) y 0 errores en los 4 archivos nuevos. Pendiente fuera del código: pruebas manuales en el navegador. Última fase del plan (§A.1): no queda fase siguiente.

- **Objetivo:** cerrar los detalles de comodidad que el operario notó, sin bloquear el corte.
- **Criterio de salida:**
  - la etiqueta lleva la cuenta de impresiones;
  - el menú dice «Terceros» y tiene accesos a Clientes, Transportadoras, Agencias, Tarifas y Convenios;
  - los módulos de uso diario tienen atajos.
- **Rama:** `develop` (DF1). **Empieza cuando la fase 5 tiene todos sus ítems con commit.**
- **Backend:** commit `04bf734` (F4-09 y F4-20/21); nada más.
- **Dificultad:** **Media** (F7-03); el resto, Baja.
- **Perfil de agente:** agente estándar.
- **Fuera:** UI-22 (cobros pendientes para báscula), por exigir un cambio de política (§A.3).

---

#### F7-01 · Conteo de impresiones de etiquetas (UI-21, GAP-024 a, LEGACY-FUNC-141)

- **Dificultad:** Baja.
- **Tarea del operario (Comercio Exterior):** saber cuántas veces se imprimió la etiqueta de un depósito y quién lo hizo por última vez.
- **Cómo lo hacía en el legacy:** cada impresión de adhesivo quedaba en la tabla `adhesivos` y el botón llevaba la cuenta (`bodegas_schema.sql:25-37`).
- **Lo que hace hoy la v2:** «Imprimir etiqueta» y «Descargar» llaman al mismo endpoint sin distinguir la acción (`useDepositLabelPrint.ts`; `foreign-trade-service.ts`: `generateImportLabel`).
- **Pantallas y componentes:**
  - `useDepositLabelPrint.ts` y los servicios de etiqueta (modifica): agregar `?action=Print` al imprimir y `?action=Download` al descargar.
  - `app/features/foreign-trade/components/LabelPrintsBadge.vue` (nuevo).
  - Encabezado del detalle (`DepositDetailPageHeader.vue`) y listados (modifica).
- **Diseño:**
  - Junto a «Imprimir etiqueta», el texto «Impresa {printCount} veces · última: {lastPrintedAt} por {lastPrintedByName}», o «Sin imprimir».
  - Clic: diálogo con las últimas 50 acciones («Acción»: Impresión o Descarga, «Usuario», «Fecha»).
- **Endpoints:**
  - **C-F4-20** `GET foreign-trade/{imports,exports,inspections}/{id}/label?action=Print|Download`; 400 «La acción debe ser Print o Download.»
  - **C-F4-21** `GET foreign-trade/warehouse-storages/{id}/label-prints` → `{ warehouseStorageId, printCount, downloadCount, lastPrintedAt, lastPrintedByName, items: [{ action, printedByName, createdAt }] }`.
- **Roles y menú:** sin cambios. **Invalidación:** `['foreign-trade', 'label-prints', warehouseStorageId]` tras imprimir o descargar.
- **Pruebas manuales:**
  1. Imprimir dos veces y descargar una. → «Impresa 2 veces» y el diálogo con las tres.
- **Terminado cuando:** la cuenta sube al imprimir.
- **Riesgo:** bajo.

---

#### F7-02 · «Terceros» y accesos directos por rol, tarifas y convenios (UI-23)

- **Dificultad:** Baja.
- **Tarea del operario (Administrador):** encontrar clientes, transportadoras y agencias de aduanas como en el legacy, y llegar rápido a tarifas y convenios.
- **Cómo lo hacía en el legacy:** menús «Clientes», «Empresas Transporte», «S.I.A», «Convenios» y «Tarifas» (`menus/menuizquierda.php`).
- **Lo que hace hoy la v2:** un listado «Stakeholders» (`components/layout/AppMenu.vue:59-73`).
- **Pantallas y componentes:**
  - `AppMenu.vue` (modifica): «Stakeholders» pasa a «Terceros», con estos hijos:
    - «Listado»;
    - «Clientes» (`/admin/stakeholders?rol=CUSTOMER`);
    - «Transportadoras» (`?rol=TRANSPORT_COMPANY`);
    - «Agencias de aduanas» (`?rol=CUSTOMS_AGENCY`);
    - «Crear».
  - Bajo Servicios, «Tarifas base» (`/admin/services`).
  - `pages/admin/stakeholders/index.vue` (modifica): lee `?rol=` como filtro inicial de rol de negocio; títulos «Terceros».
  - Textos visibles «Stakeholder» → «Tercero» en `pages/admin/stakeholders/*` y `features/stakeholders/components/*`.
- **Endpoints:** ninguno nuevo.
- **Roles y menú:** sin cambios de roles.
- **Invalidación:** no aplica.
- **Pruebas manuales:**
  1. Menú › Terceros › Agencias de aduanas. → Listado filtrado por ese rol.
- **Terminado cuando:** no queda la palabra «Stakeholder» visible al operario en Administración.
- **Riesgo:** bajo.

---

#### F7-03 · Atajos de teclado globales (UI-24)

- **Dificultad:** Media.
- **Tarea del operario:** saltar a las pantallas de uso diario con el teclado, como en el legacy.
- **Cómo lo hacía en el legacy:** Alt+N nueva entrada, Alt+K nueva salida, Alt+I ingresos, Alt+O salidas, Alt+L levantes, Alt+P depósitos (`entrada.php:9-35`).
- **Lo que hace hoy la v2:** solo F2, Enter y Esc en báscula.
- **Pantallas y componentes:** `app/composables/useGlobalShortcuts.ts` (nuevo), registrado en `app/layouts/default.vue` (modifica); ayuda «Atajos» en el menú del perfil.
- **Diseño:**

  | Atajo | Va a | Solo si el usuario tiene |
  |---|---|---|
  | Alt+N | `/operations/weighbridge` | Admin o Scale |
  | Alt+K | `/operations/weighbridge?cola=por-repesar` | Admin o Scale |
  | Alt+I | `/foreign-trade/imports` | Admin o ForeignTrade |
  | Alt+O | `/foreign-trade/loading-orders` | Admin o ForeignTrade |
  | Alt+L | `/foreign-trade/releases` | Admin o ForeignTrade |
  | Alt+P | `/foreign-trade/deposits` | Admin o ForeignTrade |

  - No actúan dentro de un `input`, `textarea` o un modal abierto.
  - Se usa `usePermissions` importado de forma explícita.
  - No interfieren con F2, Enter ni Esc del banco de trabajo.
- **Endpoints:** ninguno.
- **Roles y menú:** sin cambios de roles; cada atajo respeta los roles de la tabla. **Invalidación:** no aplica.
- **Pruebas manuales:**
  1. Con rol báscula, Alt+N. → Banco de trabajo.
  2. Con rol báscula, Alt+I. → No hace nada.
  3. Alt+N con el foco en un campo. → No navega.
- **Terminado cuando:** los seis atajos funcionan según el rol.
- **Riesgo:** choque con atajos del navegador. Se mitiga usando Alt + letra, como el legacy, y probando en Chrome y Edge.

---
## D. Dependencias del backend

### D.1 Estado del backend al 2026-10-01

- Las seis fases del plan de backend están en `Backend/wms-api`, rama `develop`, en estos commits:

  | Fase | Commit | Mensaje |
  |---|---|---|
  | 1 | `1898052` y `7c83b77` (corrección de facturación) | `feat(bascula): báscula al ritmo del legacy — fase 1 de paridad` |
  | 2 | `afe6e8f` | `feat(comercio-exterior): control aduanero — fase 2 de paridad` |
  | 3 | `5b6dbe2` | `feat(correcciones): correcciones y facturación — fase 3 de paridad` |
  | 4 | `04bf734` | `feat(bodega): bodega y mercancía — fase 4 de paridad` |
  | 5 | `adb6af4` | `feat(reportes): reportes y consultas — fase 5 de paridad` |
  | 6 | `bf64de1` | `feat(migracion): carga legacy, conciliación y respaldos — fase 6 de paridad` |

- El backend no usó ramas ni PR (decisión P17 de su plan): **lo que cada fase del frontend necesita es su commit en `develop` y sus migraciones aplicadas**.
- `develop` local está 8 commits adelante de `origin/develop`: no afecta a esta implementación, que es local (DF1).
- **Las 26 migraciones EF de paridad no están en el repositorio.** La última en `Wms.Infrastructure/Migrations` es `20260923151602_AddUnitMeasure`. Sin ellas, los endpoints que leen o escriben columnas nuevas fallan. **Paso 0 de §E.3:** el usuario las genera y aplica en su base local antes de la fase 1.

### D.2 Migraciones que necesita cada fase

Los nombres son los del plan de backend (§F.1 de ese plan).

| Fase del frontend | Migraciones |
|---|---|
| 1 | `ParidadF1_02_IndiceDocumento`, `ParidadF1_06_ProductoDesdeBascula`, `ParidadF1_09_EfectivoYCambio` |
| 2 | `ParidadF2_03_IndiceAceptacion`, `ParidadF2_05_FobLevante`, `ParidadF2_06_Ciudades`, `ParidadF2_07_CiudadDestinoOrden`, `ParidadF2_08_Prorroga` |
| 3 | `ParidadF3_01_CantidadCargada`, `ParidadF3_04_AnulacionGuia`, `ParidadF3_06_FechaLimitePeriodo`, `ParidadF3_07_ReversionOrden`, `ParidadF3_08_AnulacionDeposito`, `ParidadF3_09_AnulacionPesaje`, `ParidadF3_10_Refacturacion` |
| 4 | `ParidadF4_01_Ubicaciones`, `ParidadF4_03_Novedades`, `ParidadF4_05_ListasEmpaque`, `ParidadF4_07_PesajeCompartido`, `ParidadF4_08_SalidaConTiquete`, `ParidadF4_09_ImpresionEtiquetas`, `ParidadF4_10_Cuadrillas` |
| 5 | `ParidadF5_06_Uap`, `ParidadF5_09_TiqueteImpreso` |
| 6 (verificación) | `ParidadF6_01_ImportacionLegacy`, `ParidadF6_05_Respaldos` |
| 7 | las de la fase 4 |

**Recomendación:** generar y aplicar las 26 de una vez, en el orden de la tabla. El modelo de EF del backend ya tiene todas las entidades.

### D.3 Endpoints que consume el plan

**Estado:** todos los endpoints del contrato existen en `develop` (`bf64de1`). Ningún ítem queda bloqueado. Los endpoints anteriores que usa el plan existen desde antes.

| Contrato | Endpoint | Fase backend (commit) | Ítems |
|---|---|---|---|---|
| C-F1-01, C-F1-02 | `POST weighbridge/storage/initiate`, `…/register` | 1 (`1898052`) | F1-01, F1-02, F1-03 |
| C-F1-03 | `GET weighbridge/service-records/by-document`, `…/warehouse-storage/by-document` | 1 | F1-01 |
| C-F1-04 | `PUT foreign-trade/warehouse-storages/{id}/stakeholders` | 1 | F1-07 |
| C-F1-05 | `PATCH foreign-trade/warehouse-storages/{id}/draft` | 1 | F1-07 |
| C-F1-06 | `PATCH foreign-trade/warehouse-storages/{id}/entries/{entryId}/manifest` | 1 | F1-07 |
| C-F1-07, C-F1-08 | `POST …/confirm`, `GET …/confirmation-requirements` | 1 | F1-07 |
| C-F1-09 | `GET product` (`createdFromWeighbridge`) | 1 | F1-02, F1-08 |
| C-F1-10 | `PUT foreign-trade/deposits/{id}/products/{storageProductId}/catalog-product` | 1 | F1-08 |
| C-F1-11 | `PUT …/entries/{entryId}/cargo-unit-breakdown` | 1 | F1-08 |
| C-F1-12 | `POST weighbridge/{storage,weighing-only,output}/process-payment` | 1 | F1-04, F1-05 |
| C-F2-01, C-F2-02, C-F2-06 | levantes (registrar, editar, detalle con FOB) | 2 (`afe6e8f`) | F2-06 |
| C-F2-03, C-F2-04, C-F2-09 | orden de cargue (destino, nacionalizado, lecturas) | 2 | F2-02, F2-03 |
| C-F2-05 | `POST …/releases/{releaseId}/withdraw` | 2 | F2-05 |
| C-F2-07 | ciudades (CRUD e importación) | 2 | F2-01, F2-02, F2-04 |
| C-F2-10 | `POST foreign-trade/dispatch-guides` | 2 | F2-04 |
| C-F2-11, C-F2-12, C-F2-13 | prórroga, listado y resumen de abandono | 2 | F2-07 |
| C-F2-14, C-F2-15 | reportes de abandono | 2 | F2-08, F5-11 |
| C-F2-08 | `POST warehouse/loading-orders` | 2 | — (sin pantalla, §G) |
| C-F3-01 | `POST warehouse/loading-orders/{id}/execute` | 3 (`5b6dbe2`) | F3-03 |
| C-F3-02, C-F3-03 | cancelar y modificar la orden | 3 | F3-02 |
| C-F3-04 | anular guía | 3 | F3-04 |
| C-F3-05, C-F3-06, C-F3-07 | ciclos y períodos | 3 | F3-07 |
| C-F3-08 | revertir salida | 3 | F3-05 |
| C-F3-09 | anular depósito | 3 | F3-06 |
| C-F3-10, C-F3-11 | anular pesaje e historial | 3 | F3-01 |
| C-F3-12, C-F3-13, C-F3-14 | anular, refacturar, pendientes | 3 | F3-08 |
| C-F4-01 a C-F4-07 | ubicaciones, recepción y cargue | 4 (`04bf734`) | F4-02 |
| C-F4-08 a C-F4-12 | novedades | 4 | F4-03 |
| C-F4-13 a C-F4-17 | listas de empaque | 4 | F4-04 |
| C-F4-18 | órdenes adicionales en el pesaje | 4 | F4-05 |
| C-F4-19 | salida con tiquete de ingreso (dos rutas) | 4 | F4-06 |
| C-F4-20, C-F4-21 | etiquetas y conteo | 4 | F7-01 |
| C-F4-22, C-F4-23 | cuadrillas | 4 | F4-01 |
| C-F5-01, C-F5-02 | importaciones (saldos y búsqueda), levantes | 5 (`adb6af4`) | F5-02, F5-03 |
| C-F5-03 | kardex | 5 | F5-04 |
| C-F5-04 | inventario general | 5 | F5-05 |
| C-F5-05 a C-F5-07 | pólizas y UAP | 5 | F5-06 |
| C-F5-08 | ingresos por producto | 5 | F5-07 |
| C-F5-09, C-F5-10 | facturación anual y por CPI | 5 | F5-08 |
| C-F5-11 | historial de báscula (filtros y totales) | 5 | F5-09 |
| C-F5-12, C-F5-13 | agencias de aduanas | 5 | F5-10 |
| C-F5-14 | exportaciones con `all=true` | 5 | F5-01, F5-11 |
| C-F6-01 a C-F6-07 | carga legacy y respaldos | 6 (`bf64de1`) | — (por API, DF3) |
| existente | `GET weighbridge/history` | anterior | F4-06, F5-09 |
| existente | `GET weighbridge/loading-orders/by-plate/{plate}` | anterior | F4-05 |
| existente | `GET foreign-trade/warehouse-storages/{id}/entries`, `…/cargo-units` | anterior | F1-07, F1-08, F4-04 |
| existente | `GET warehouse/receptions?warehouseStorageId=` | anterior | F4-03 |
| existente | `GET warehouse/inventory/deposits`, `…/inventory/stock/{id}`, `…/inventory/movements`, `warehouse/locations` | anterior | F4-02, F4-03, F5-01 |
| existente | `GET foreign-trade/loading-orders?searchField=LicensePlate` | anterior | F4-06 |

---

## E. Orden de ejecución y commits

### E.1 Reglas

1. **Todo en `develop`.** No se crean ramas ni PR (DF1).
2. **El implementador no hace commits.** No ejecuta `git add`, `git commit`, `git push`, `git merge`, `git stash` ni `git checkout -b`. Los commits los hace el usuario.
3. **Un ítem a la vez**, en el orden de §E.3. Al terminar un ítem, el implementador se detiene y entrega el resumen de §E.2. El usuario revisa el diff, hace el commit con el mensaje sugerido de §E.4 y solo entonces el implementador sigue con el ítem siguiente.
4. **Antes de entregar un ítem:**
   - `yarn build` pasa;
   - el ítem pasó sus pruebas manuales en el navegador contra el backend local (§B.5);
   - el árbol de trabajo solo tiene cambios de ese ítem.
5. **Una fase empieza** cuando la anterior tiene todos sus ítems con commit. La fase 2 exige además la medición de F1-09 aprobada.
6. **Al cerrar una fase**, el implementador aplica §B.6 y escribe en el resumen del último ítem el número de errores de lint con que cierra la fase: «Lint: {n} errores (tope {m}).»
7. Si una prueba descubre que el backend responde distinto al contrato, el implementador se detiene y lo reporta. No simula la respuesta ni cambia el backend.

### E.2 Qué entrega el implementador al terminar cada ítem

Un mensaje con este formato, y nada más hasta que el usuario confirme el commit:

```
Ítem: F1-02 · Mercancía en línea y producto por descripción libre (BAS-02, BAS-03, UI-01)
Archivos nuevos:      app/features/weighbridge/components/TruckGoodsLines.vue, …
Archivos modificados: app/features/weighbridge/components/StorageServiceForm.vue, …
Archivos eliminados:  — (o la lista)
Build:                yarn build OK
Pruebas manuales:     1 OK · 2 OK · … (con la observación si alguna no aplicó)
Ganancias de la v2 (§A.5) verificadas: cola, memoria del turno, …
Mensaje de commit sugerido:
  feat(bascula): mercancía en línea con descripción libre (BAS-02, BAS-03, UI-01)
Lint (solo en el último ítem de la fase): {n} errores (tope {m}).
```

### E.3 Pasos con dependencias

| # | Paso | Depende de | Quién |
|---|---|---|---|---|
| 0 | Generar y aplicar las 26 migraciones de paridad en la base local; levantar el backend `develop` (`bf64de1`); comprobar que hay usuarios de prueba de cada rol. Comprobar que `develop` del frontend está en `26aed68` o posterior y sin cambios pendientes. | — | Usuario |
| 1 | F1-01 | 0 | Implementador; commit del usuario |
| 2 | F1-02 | 1 (usa el formulario reorganizado) | Implementador; commit del usuario |
| 3 | F1-03 | 2 (las unidades usan las líneas libres) | Implementador; commit del usuario |
| 4 | F1-04 | 0 (independiente; va antes de F1-05) | Implementador; commit del usuario |
| 5 | F1-05 | 1 y 4 | Implementador; commit del usuario |
| 6 | F1-06 | 5 (el foco depende de los pasos en línea) | Implementador; commit del usuario |
| 7 | F1-07 | 1 (necesita depósitos incompletos para probar) | Implementador; commit del usuario |
| 8 | F1-08 | 3 y 7 | Implementador; commit del usuario (cierre de lint de la fase si no hay ajustes) |
| 9 | F1-09: medición con el operario. Si no se cumple, ítem de ajuste en `develop` con su commit, y se repite la medición. | 1 a 8 | Usuario, operario e implementador |
| 10 | F2-01 → F2-02 → F2-03 → F2-04 → F2-05 → F2-06 → F2-07 → F2-08, un commit por ítem. F2-02 y F2-04 dependen de F2-01. F2-03 depende de F2-02 (mismo formulario). F2-07 usa los tipos de F2-06. | 9 aprobado | Implementador; commits del usuario |
| 11 | F3-01 (crea `ReasonDialog` y `CorrectionResultDialog`) → F3-02 → F3-03 → F3-04 → F3-05 → F3-06 → F3-07 → F3-08. F3-05 se prueba después de F3-04 (la reversión exige anular la guía). | 10 | Implementador; commits del usuario |
| 12 | F4-01 → F4-02 → F4-03 → F4-04 → F4-05 → F4-06. F4-03 usa `ReasonDialog` (fase 3). F4-04 usa `postForm` (F2-01). F4-05 y F4-06 se validan con el operario de báscula antes de su commit. | 11 | Implementador, operario; commits del usuario |
| 13 | F5-01 (utilidad de Excel) → F5-02 → … → F5-11. Todos los Excel dependen de F5-01. | 12 | Implementador; commits del usuario |
| 14 | Fase 6: carga de datos por API y verificación de C.6 con cada operario. | 13 y migraciones de la fase 6 | Usuario |
| 15 | (Opcional) F7-01 → F7-02 → F7-03. El implementador de la última fase que se ejecute confirma o corrige la tabla §F.2 con el estado real de `develop` (qué ítems tienen commit). | 13 | Implementador; commits del usuario |

### E.4 Mensajes de commit sugeridos (los hace el usuario), en orden

**Fase 1:**

1. `feat(bascula): campos de Comercio Exterior opcionales y documento sin fecha (BAS-01, UI-01)`
2. `feat(bascula): mercancía en línea con descripción libre (BAS-02, BAS-03, UI-01)`
3. `feat(bascula): tipo de carga y unidades de carga sin desglose (BAS-07, UI-01)`
4. `feat(bascula): efectivo recibido y cambio en el cobro (BAS-05, GAP-024, UI-01)`
5. `feat(bascula): cobro y peso en la misma ficha, sin modales (BAS-04, UI-01)`
6. `feat(bascula): ficha de arriba a abajo con el teclado y sin confirmación (BAS-06, UI-01)`
7. `feat(comercio-exterior): requisitos para confirmar, fecha del documento y manifiesto por camión (BAS-01, UI-01)`
8. `feat(comercio-exterior): cambiar producto de la línea y repartir unidades de carga (BAS-03, BAS-07, UI-01)`
9. Solo si la medición pide ajustes: `fix(bascula): ajustes tras la medición con el operario (BAS-06, UI-01)`. F1-09 no tiene commit propio: su resultado va en `code_workspace/ajustes/medicion-bascula-fase1.md`, que no está en git.

**Fase 2:**

1. `feat(administracion): catálogo de ciudades con días de tránsito (UI-10, GAP-025)`
2. `feat(comercio-exterior): ciudad de destino de la orden por catálogo (UI-10, GAP-025)`
3. `feat(comercio-exterior): tope de despacho por lo nacionalizado (UI-04, GAP-002)`
4. `feat(comercio-exterior): vencimiento de la guía por días de tránsito (UI-10, GAP-025)`
5. `feat(comercio-exterior): retirar un levante con motivo (UI-06, GAP-009)`
6. `feat(comercio-exterior): FOB y tasa del levante y levante de varios productos (UI-19, GAP-009)`
7. `feat(comercio-exterior): prórroga y pantalla de abandono con aviso (UI-05, GAP-003)`
8. `feat(reportes): reportes de abandono (UI-05, GAP-003)`

**Fase 3:**

1. `feat(bascula): anular un pesaje completo con motivo (UI-02, GAP-005)`
2. `feat(comercio-exterior): cancelar con motivo y modificar la orden antes del cargue (UI-03, GAP-006)`
3. `feat(bodega): cargue parcial con cantidades en cero (UI-03, GAP-006)`
4. `feat(comercio-exterior): anular una guía de salida (UI-03, GAP-006)`
5. `feat(comercio-exterior): revertir una salida cargada (UI-03, GAP-006)`
6. `feat(comercio-exterior): anular un depósito con motivo y ver sus efectos (GAP-011)`
7. `feat(facturacion): ciclos de facturación legacy y fecha límite del período (UI-08, GAP-008)`
8. `feat(facturacion): refacturar una factura de almacenamiento anulada (UI-07, GAP-007)`

**Fase 4:**

1. `feat(administracion): cuadrillas en orden, recepción y cargue (UI-15, GAP-026)`
2. `feat(bodega): ubicar, mover y liberar mercancía por cantidades (UI-13, GAP-014)`
3. `feat(bodega): novedades de mercancía con desglose e impresión (UI-14, GAP-015)`
4. `feat(comercio-exterior): listas de empaque y asociación al camión (UI-12, GAP-013)`
5. `feat(bascula): otras órdenes con el mismo pesaje de salida (BAS-08, UI-11, GAP-019)`
6. `feat(bascula): salida con el tiquete de ingreso (BAS-09, UI-11, GAP-019)`

**Fase 5:**

1. `feat(reportes): exportación a Excel sin tope de filas (UI-09, GAP-017)`
2. `feat(comercio-exterior): columnas de saldo en los listados (UI-17)`
3. `feat(comercio-exterior): búsqueda por placa y levante, y listado de levantes (UI-18)`
4. `feat(reportes): kardex con levantes y despachos (UI-20, GAP-016)`
5. `feat(reportes): inventario general filtrable (UI-20, GAP-016)`
6. `feat(reportes): informe de póliza y marca UAP del tercero (UI-20, GAP-016)`
7. `feat(reportes): ingresos por producto y cliente (UI-20, GAP-016)`
8. `feat(facturacion): facturación anual y por CPI (UI-20, GAP-016)`
9. `feat(bascula): reporte de báscula con filtros, pesos y totales (UI-20, GAP-016)`
10. `feat(reportes): ingresos por agencia de aduanas (UI-16, GAP-010)`
11. `feat(reportes): Excel en los demás listados (UI-09, GAP-017)`

**Fase 7 (opcional):**

1. `feat(comercio-exterior): conteo de impresiones de etiquetas (UI-21, GAP-024)`
2. `feat(administracion): Terceros y accesos por rol, tarifas y convenios (UI-23)`
3. `feat(general): atajos de teclado globales (UI-24)`

---

## F. Rama, commits y orden de las fases

### F.1 Rama y commits

- **Rama única:** `develop` de `Frontend/wms`. No se crean ramas `feature/*` ni PR (DF1).
- **Commits:** los hace el usuario, uno por ítem, con el mensaje de §E.4. El implementador solo deja los cambios en el árbol de trabajo y entrega el resumen de §E.2.
- **Cada fase compila y pasa el lint por sí sola:** se verifica al cerrar su último ítem (§B.6), antes de empezar la siguiente.
- **Publicación:** cuándo publicar `develop` en `origin` y desplegar lo decide el usuario (ver «Despliegue» en §F.2).

### F.2 Orden de las fases y qué las habilita

Lo confirma o corrige, con el estado real de `develop`, el implementador de la última fase que se ejecute (la 7 o, si no se hace, la 5).

| Orden | Fase | Contiene | Backend requerido (commit en `develop` del backend y migraciones aplicadas) | Fase de frontend que debe estar completa antes | Dificultad | Perfil de agente |
|---|---|---|---|---|---|---|
| 1 | Fase 1 — Báscula | F1-01 a F1-08 (+ ajustes de F1-09) | `1898052` y `7c83b77`; migraciones de la fase 1 | — (paso 0) | Muy alta | Agente capaz, revisión humana y medición con el operario |
| 2 | Fase 2 — Control aduanero | F2-01 a F2-08 | `afe6e8f`; migraciones de la fase 2 | Fase 1 con commits y medición aprobada | Alta | Agente capaz, revisión humana del diff y prueba en el navegador |
| 3 | Fase 3 — Correcciones y facturación | F3-01 a F3-08 | `5b6dbe2`; migraciones de la fase 3 | Fase 2 con commits | Alta | Agente capaz, revisión humana del diff y prueba en el navegador |
| 4 | Fase 4 — Bodega y mercancía | F4-01 a F4-06 | `04bf734`; migraciones de la fase 4 | Fase 3 con commits | Muy alta | Agente capaz, revisión humana y validación con el operario de báscula |
| 5 | Fase 5 — Reportes | F5-01 a F5-11 | `adb6af4`; migraciones de la fase 5 | Fase 4 con commits | Media | Agente estándar |
| — | Fase 6 — Migración | sin código | `bf64de1`; migraciones de la fase 6 | Fase 5 con commits | — | — |
| 6 | Fase 7 — Comodidad (opcional) | F7-01 a F7-03 | `04bf734` | Fase 5 con commits | Media | Agente estándar |

**Por qué en secuencia** (DF13): todas las fases tocan los servicios compartidos (`foreign-trade-service.ts`, `weighbridge-service.ts`), los tipos, `AppMenu.vue` y las páginas de detalle del depósito. En una sola rama, trabajar dos fases a la vez mezclaría sus cambios en el mismo commit y en las mismas pruebas.

**Despliegue:** el backend de `develop` ya exige ciudad de destino al crear órdenes (C-F2-03) y motivo al anular depósitos (C-F3-09). No conviene desplegarlo en un ambiente que use la operación (staging con el cliente, producción) antes de que las fases 2 y 3 del frontend tengan sus commits en `develop` y se desplieguen con él.

---

## G. Observaciones (fuera de alcance, no se planifican)

1. **Backend sin publicar y sin migraciones.** `develop` de `wms-api` está 8 commits adelante de `origin/develop` y no tiene las 26 migraciones de paridad (§D.1).
2. **Frontend y backend de `develop` desalineados hoy.** Contra el backend actual:
   - crear una orden de cargue falla (falta `destinationCityId`);
   - anular un depósito sin motivo falla (`imports/[id]/index.vue:173`, igual en exportación e inspección).

   Se corrige en F2-02 y F3-06.
3. **Manejo de errores.** El interceptor rechaza con el cuerpo `IApiError` (`plugins/api-client.ts:141-147`), pero muchas pantallas leen `error.response.data.description` (siempre `undefined`) y muestran un texto genérico además del aviso global. Ejemplos: `pages/operations/weighbridge/index.vue:284,359,411,444,470,507,675,782`. Solo se corrige en las líneas que tocan los ítems.
4. **Exportaciones rotas hoy:**
   - `features/foreign-trade/composables/useExportImportsToExcel.ts` usa `XLSX`, que no está instalado ni importado, y `pageSize: 10000`. No lo usa ninguna página.
   - `useInventoryExport` llama a un método inexistente.
   - F5-01 los reemplaza.
5. **`useReceptionReceiptPdf`** (`features/warehouse/composables/useWarehouseExports.ts:79-95`) llama a `downloadReceptionReceiptPdf`, que no existe ni en el servicio ni en el API. No está en el contrato.
6. **Código sin uso:**
   - `GET weighbridge/lookup` con `useWeighbridgeLookup.ts`: precarga por placa (ítem retirado);
   - `useLoadingOrderCreate` (`features/warehouse/composables/useLoadingOrderMutations.ts:25-46`): `POST warehouse/loading-orders` no tiene pantalla. El plan de backend ya anota que hay dos caminos para crear órdenes;
   - `PaymentForm.vue`: sin uso; F1-04 solo extrae su lógica.
7. **Selector «Tipo de carga» nunca pintado** en báscula (`StorageServiceForm.vue:198-221`): en un depósito nuevo siempre iba «Mercancía suelta». Se corrige en F1-03 porque BAS-07 lo necesita (DF15).
8. **Exportación de maestros:** el botón «Exportar» de `AppTable` (`components/app/AppTable.vue:260-265`) usa `exportCSV` de PrimeVue y solo exporta las filas cargadas en la página.
9. **Claves de consulta heterogéneas:** `weighbridgeHistory` y `weighbridge-history`, `weighbridgeCycle`, `warehouse-*`, `daily-incoming-goods-report`… Este plan solo agrega claves con prefijo de módulo y nombra las heredadas que invalida.
10. **Lint:** `develop` tiene 322 errores y 394 advertencias de lint previos (§B.6).
11. **Hallazgos del legacy que contradicen el análisis:**
    - `BASCULA_PARITY.md` §2 dice que el legacy pedía el manifiesto en Comercio Exterior. El formulario de báscula sí capturaba «Manifiesto PreImp.» y «P. manifiesto» como opcionales (`registrarentradabascula.php:832-834,855`); Comercio Exterior capturaba el manifiesto DIAN. El plan sigue al código (DF11).
    - La tabla «Entrada / Ampara / Saldo / Nvo. saldo» solo se mostraba para vehículos de Colmotores (`consultaSaldosVehiculos`, `:657-675`, condicionada a `sonvehiculos`). El panel de camiones previos de la v2 la supera para cualquier documento.
    - El atajo Alt+N abre `registrarentrada.php` (formulario anterior, `entrada.php:18`); el menú «Nueva Entrada» abre `registrarentradabascula.php` (`menus/menuizquierda.php:196`), que es el que se comparó.
    - En importación, el legacy imprimía al llegar el tiquete «entrada y tara», con la tara calculada desde el peso del manifiesto (`registrarentradabascula.php:643-651`; `facturar.php:213-219`). La v2 hace dos pesajes reales y numera el tiquete al completar el ciclo. Es un cambio de hábito para capacitación («el conductor recibe el tiquete después del repesaje»). La medición se ajustó con DF2.
    - El informe de pólizas del legacy rotula «CIF» lo que es la suma del FOB en dólares. La v2 rotula «FOB» (F5-06).
12. **Número legacy de los depósitos migrados:** el backend lo guarda (`legacy_number`), pero ningún DTO lo expone; el operario no puede buscar por él en la v2.
13. **Notificaciones sin enlace:** la página de notificaciones no navega por tipo de entidad (por ejemplo, `AbandonmentReport`). El aviso del tablero de F2-07 cubre el caso de abandono.
14. **Acceso** (fuera de alcance por regla):
    - el rol de Vigilancia que se da a báscula también abre Bodega completa y la corrección de ingresos;
    - cualquier usuario activo puede crear y editar terceros (`StakeholderController`).
15. **Gestores de paquetes:** el repositorio tiene `yarn.lock` (con `packageManager: yarn@4.11.0`) y `package-lock.json`. F5-01 agrega `exceljs` con `yarn`, y `package-lock.json` queda desactualizado.
16. **Rama y commits.** Como el backend (P17), el frontend se trabaja todo en `develop`, sin ramas ni PR, y los commits los hace el usuario (DF1).
