# Fase 7 — Transversal: reportes, documentos impresos, notificaciones, auditoría y trazabilidad

> Lee antes `00-plan-maestro.md`. Roles: Admin, `c_exterior`, `facturacion`, `bodega`, `bascula`.
> Usa los datos acumulados de las fases 2 a 6: cada reporte se verifica contra operaciones conocidas del registro de datos.

## 1. Objetivo

Validar que los reportes cuadran con las operaciones, que los PDF y Excel son correctos y legibles, que las notificaciones llegan al rol correcto en tiempo real y quedan persistidas, que la auditoría registra lo que debe (y no expone secretos), y que el tablero de trazabilidad sigue a cada camión.

## 2. Alcance

| Área | Ruta | Bloque |
|---|---|---|
| Reportes de CE y Bodega | `/reports/*` | REP |
| Reportes de Facturación | `/billing/reports/*` | REP |
| Reporte de báscula | `/operations/weighbridge/reports` | (F3-RPT) |
| Documentos impresos | tiquete, etiqueta, orden de trabajo, guía, factura, novedad, movimientos | PDF |
| Notificaciones | `/notifications`, avisos en tiempo real | NOT |
| Auditoría | `/admin/audit` | AUD |
| Trazabilidad por placa | `/` y búsqueda de la barra superior | TRZ |
| Atajos globales | toda la app | ATJ |

## 3. Criterios de entrada

1. Fases 1 a 6 aprobadas (o con CRITICAL aceptados).
2. Registro de datos con operaciones de al menos dos días distintos (si no, se usan fechas corregidas o se anota la limitación).

## 4. Casos

### 4.1 Reportes (REP)

Para cada reporte: (a) ejecutar con un filtro que incluya datos QA conocidos; (b) comparar cifras con el registro de datos; (c) exportar y abrir el archivo; (d) probar validaciones de filtros.

| ID | Reporte | Pasos y verificación | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F7-REP-001 | Ingresos diarios | Rango con las fechas de la fase 3. | **Actualizado (DEC-054):** formato legacy, con IMP por defecto; ver F7-REP-024. PDF igual a pantalla. | P1 | RN |
| F7-REP-002 | Ingresos diarios — validación | Sin fechas; desde > hasta. | Rechazados. El PDF solo se descarga con el informe vigente. | P2 | VAL |
| F7-REP-003 | Salidas diarias | Rango con las salidas de la fase 5; filtro por cliente y mercancía (≥ 2 caracteres). | Cuadra con las guías/cargues; PDF. | P1 | RN |
| F7-REP-004 | Estadísticas | Semana, mes, año. | Cifras coherentes con las operaciones del período. | P2 | RN |
| F7-REP-005 | Mercancía en abandono | Con datos de F5-ABA. | Depósitos con plazo vencido y stock > 0, totales; Excel con todas las filas. | P2 | RN |
| F7-REP-006 | Salidas a destino de abandono | Rango por defecto (1-ene a hoy) y con una salida a `QA BOGOTA`. | Lista la salida; inicio > fin rechazado. | P2 | RN |
| F7-REP-007 | Inventario general | Tipo de saldo; filtros importador, agencia, transportadora, producto, modalidad, ubicación. | Saldos = inventario de Bodega. | P1 | RN |
| F7-REP-008 | Inventario general — rango | Tipo «All» sin rango. | Rango obligatorio. | P2 | VAL |
| F7-REP-009 | Informe de póliza | Año actual; detalle por mes. | Rotula FOB (no CIF); suma de FOB coherente con los levantes; Excel de resumen y detalle. | P2 | RN |
| F7-REP-010 | Ingresos por producto | Fechas e importador obligatorios. | Cantidades por producto = declaradas. | P2 | RN |
| F7-REP-011 | Ingresos por agencia | Agencia `QA Agencia SIA`. | Sus depósitos; detalle; Excel. | P2 | RN |
| F7-REP-012 | Movimientos por depósito | Número de `QA-CP-0001`; rango que incluya todo. | Kardex: `DeclaredEntry`, ajustes, OUT, reversas; saldo final = stock actual; fecha final inclusiva; Excel 3 hojas y PDF. | P0 | RN |
| F7-REP-013 | Movimientos con levantes | El mismo reporte. | Muestra levantes (kardex con levantes, GAP-010) y columnas de saldo. | P2 | RN |
| F7-REP-014 | Facturación anual | Año actual, cada categoría. | Solo facturas con número y no anuladas; por día de creación en Colombia; suma solo líneas del servicio; excluye $0. Anotar que incluye borradores con número. | P1 | RN |
| F7-REP-015 | Facturación por CPI | Número de depósito; uno inexistente. | Facturas del depósito vía períodos; Excel de 3 hojas; inexistente: «No se encontró el depósito '…'.». | P1 | RN |
| F7-REP-016 | Inventario general como CE puro | Con `c_exterior`, abrir Inventario general. | Esperado: carga completa. Riesgo R-ADM-03: 403 en el filtro de ubicaciones. | P1 | ROL |
| F7-REP-017 | Inventario general como Bodega | Con `bodega`. | Carga (Admin, FT, WH). | P2 | ROL |
| F7-REP-018 | Excel con todas las filas | En cualquier reporte con > 50 filas. | El Excel trae todas (usa `all=true`), no solo la página. Anotar el botón genérico «Exportar» de tablas que solo exporta la página cargada (§G.8 del plan de paridad). | P1 | FUN |
| F7-REP-019 | Formato del Excel | Abrir 3 exportaciones. | Encabezados en español, fechas en hora Colombia, números como número (no texto), tildes correctas. | P2 | UI |
| F7-REP-020 | Reporte vacío | Filtro sin resultados. | Mensaje «sin datos» sin error; exportar no falla. | P3 | ERR |
| F7-REP-021 | Rendimiento | Reporte de rango amplio. | Responde en < 10 s; anotar tiempo. | P3 | UX |
| F7-REP-022 | CPI tras refacturar | Depósito con factura anulada y refacturada (F6-REF-001). | Esperado: muestra ambas (o la trazabilidad). Riesgo R-FAC-10: la anulada desaparece. | P2 | RN |
| F7-REP-023 | Fecha de ingreso corregida en informes | Corregir la fecha de ingreso de un depósito dentro de la estadía de su primer camión (Báscula, Comercio Exterior o Admin) y abrir el kárdex, el listado y el Excel de importaciones, exportaciones e inspecciones, y el diario de ingresos. | **Nuevo (DEC-012, BR-07-003):** todos muestran `EntryDate` (la corregida), no la fecha de creación. En el diario, el primer camión del depósito entra con la fecha de ingreso del depósito y los siguientes con su ingreso en Vigilancia. | P1 | RN |
| F7-REP-024 | Diario con formato legacy | Reportes → Mercancías ingresadas (diario) con un rango y la modalidad (IMP por defecto, EXP, INSP). Pantalla, PDF y Excel. Probar `operationModalityCode=XX`. | **Nuevo (DEC-054, D24 a D26):** un bloque por depósito (solo Confirmado y Cerrado) con agencia, importador (o exportador/cliente), manifiesto DIAN y CPI, y una fila por camión con manifiesto preimpreso, placa, fecha y hora, tiquete, planilla, transportadora, embalaje, cantidad, **peso de manifiesto y neto de báscula** (el neto del pesaje compartido, prorrateado) y mercancía; subtotales por depósito, «Total vehículos: N» y las firmas «Jefe de Bodega», «Recibí conforme DIAN» y «Firma Funcionario». El Excel es plano (Depósito, Agencia e Importador se repiten) con totales y las tres firmas. `XX` responde 400 «La modalidad debe ser IMP, EXP o INSP.». | P1 | RN |
| F7-REP-025 | Diario de salidas a Excel | Reportes → Salida de mercancía (diario) → «Exportar Excel» con resultados. | **Nuevo (BR-07-001, D27):** el archivo trae las columnas de la pantalla y la fila de totales; el manifiesto es el DIAN del depósito (nulo fuera de importación). El kárdex trae la agencia y el manifiesto DIAN (BR-07-004). | P2 | FUN |

### 4.2 Documentos impresos (PDF)

| ID | Documento | Verificación | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F7-PDF-001 | Tiquete de báscula | (Ver F3-TIQ-002/004.) Cotejar con `docs/cliente/formatos/TIQUETE BASCULA OK.xlsx`. | Datos completos y correctos; hora Colombia; formato térmico. | P1 | FUN |
| F7-PDF-002 | Etiqueta del depósito | Cotejar con `docs/cliente/formatos/DEPOSITO INGRESO.pdf`. | Texto por modalidad, fecha de ingreso, transportadoras, cantidades/peso, contador. | P1 | FUN |
| F7-PDF-003 | Guía de salida | Cotejar con `GUIA DE SALIDA CEBOLLA.pdf` y `guia_salida.jpg`. | Entrada, saldo anterior, despachado, nuevo saldo por línea; ANULADA si aplica. | P0 | RN |
| F7-PDF-004 | Factura | PDF de 3 facturas (báscula, montacargas con IVA, almacenamiento). | Totales = pantalla; RETE_FUENTE no suma; detalle del depósito. | P1 | RN |
| F7-PDF-005 | Orden de trabajo | Desde Bodega/CE. | Ítems, depósitos, vehículo, cuadrilla, ciudad. | P2 | FUN |
| F7-PDF-006 | Novedad | Desde Bodega. | Desglose y datos del camión. | P3 | FUN |
| F7-PDF-007 | Datos de la empresa | Encabezado de tiquete, informes y facturas. | Anotar si salen valores por defecto (R-ADM-10: `COMPANY_*` sin sembrar). | P2 | FUN |
| F7-PDF-008 | Caracteres especiales | Terceros con tildes y ñ («QA Compañía Ñandú»). | Se imprimen bien. | P2 | UI |

### 4.3 Notificaciones (NOT)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F7-NOT-001 | Conexión en tiempo real | Login; revisar Red. | WebSocket a `/hubs/notifications` abierto. | P1 | INT |
| F7-NOT-002 | Aviso a Facturación | Provocar una TRM pendiente o un cargo al mínimo. | `facturacion` recibe el aviso en vivo y queda en `/notifications`. | P1 | INT |
| F7-NOT-003 | Aviso a Comercio Exterior | Provocar un evento para CE: nuevo depósito IMP, diferencia de recepción, camión tardío, «Guía con cantidades distintas a lo cargado» (desde DEC-056, «Guía de salida requerida» solo sale con órdenes cargadas sin guía antes del cambio). | Esperado: `c_exterior` (y `j_coral`, `f_chosi`) lo reciben. Riesgo R-ADM-01 ★: no llegan a nadie (NormalizedName FOREXTERIOR). Si se confirma: CRITICAL. | P0 | INT |
| F7-NOT-004 | Aviso a Admin | Corrección de peso; validación con discrepancia. | Admin recibe aviso (y correo). | P1 | INT |
| F7-NOT-005 | Aviso a Bodega | CE anula un depósito con OC en cargue. | `bodega` recibe aviso. | P2 | INT |
| F7-NOT-006 | Página de notificaciones | Filtros Todas, No leídas, Leídas; marcar una y todas; paginación. | Funciona; el contador se actualiza. | P1 | FUN |
| F7-NOT-007 | Navegación desde la notificación | Clic en una notificación. | Anotar: no navega a la entidad (§G.13 del plan de paridad). | P3 | UX |
| F7-NOT-008 | Aviso de trazabilidad | Con Admin conectado, registrar un ingreso. | Anotar si aparece un aviso con título «TraceabilityUpdated» (R-ADM-11). | P2 | UI |
| F7-NOT-009 | Reconexión | Detener y reanudar el API con la app abierta. | Se reconecta (0, 2, 5, 10, 30 s); si la conexión se cierra del todo, anotar que hace falta recargar. | P2 | ERR |
| F7-NOT-010 | Usuario multi-rol | Con `j_coral` (Billing + FT). | Recibe avisos de ambos roles (salvo R-ADM-01). | P2 | INT |
| F7-NOT-011 | Persistencia | Generar un aviso con el usuario desconectado; entrar. | Aparece en `/notifications` como no leído. | P1 | PER |

### 4.4 Auditoría (AUD)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F7-AUD-001 | Registro de cambios | Editar un tercero, un producto y un depósito; abrir `/admin/audit`. | Filas Create/Update con usuario, tabla, fecha y JSON anterior/nuevo. | P1 | FUN |
| F7-AUD-002 | Filtros | Usuario (por nombre), acción, tabla. | Filtran. Anotar que el filtro de fechas no está en la UI. | P2 | FUN |
| F7-AUD-003 | Correcciones con motivo | Corrección de ingreso (WMS-5), fecha de ingreso, retiro de levante. | El motivo queda en la descripción de la auditoría. | P1 | RN |
| F7-AUD-004 | Catálogos auditados | Editar un embalaje, una unidad, una ubicación, un motivo, un conductor, un vehículo, una tarifa de montacargas, un precio y los roles de un usuario. | Anotar cuáles no generan registro (R-ADM-15). | P2 | RN |
| F7-AUD-005 | Jobs | Tras una renovación automática. | Anotar: sin usuario, no queda auditado. | P3 | RN |
| F7-AUD-006 | Secretos en la auditoría | Cambiar la contraseña de un usuario de prueba (reset por Admin) y abrir su registro de auditoría. | Esperado: **no** aparecen `PasswordHash` ni `SecurityStamp`. Riesgo R-ADM-12 ★. Si aparecen: CRITICAL de seguridad. | P0 | SEG |

### 4.5 Trazabilidad (TRZ)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F7-TRZ-001 | Etapas | Dashboard `/` con Hoy. | Cada camión QA en su etapa (13 etapas) coherente con su estado real. | P1 | INT |
| F7-TRZ-002 | Filtros | Hoy / Semana / Mes; placa parcial. | Filtra. Anotar si la placa distingue mayúsculas. | P2 | FUN |
| F7-TRZ-003 | Búsqueda de la barra superior | Con Admin/FT, buscar `QAA101`. | Abre `/?plate=QAA101`. Con otros roles no aparece la búsqueda. | P2 | FUN |
| F7-TRZ-004 | Refresco en vivo | Registrar ingreso y salida con el tablero abierto. | Se actualiza al instante (ingreso, autorización y salida) y cada 5 min en general. | P2 | INT |
| F7-TRZ-005 | Camión que salió sin operación | Ingreso con motivo Otro y salida. | Esperado: etapa «Salió». Riesgo R-VIG-04: «En portería». | P2 | RN |
| F7-TRZ-006 | Bloque de facturación | Con Admin y con CE. | El bloque de facturación de las estadísticas solo para Admin. | P3 | ROL |

### 4.6 Atajos globales — UI-24 (ATJ)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F7-ATJ-001 | Atajos de CE | Con `c_exterior`: Alt+I, Alt+O, Alt+L, Alt+P. | Importaciones, órdenes de cargue, levantes, depósitos. | P2 | UX |
| F7-ATJ-002 | Atajos de báscula | Con `bascula`: Alt+N, Alt+K. | Báscula y `?cola=por-repesar`. | P2 | UX |
| F7-ATJ-003 | Atajos de otro rol | Con `bascula`: Alt+I. | No hace nada. | P2 | ROL |
| F7-ATJ-004 | Dentro de un campo o modal | Pulsar Alt+N escribiendo en un campo y con un modal abierto. | No actúan. Con Ctrl/Cmd/Shift tampoco. | P2 | UX |
| F7-ATJ-005 | Ayuda | Perfil → «Atajos de teclado». | Lista solo los del rol. | P3 | UX |
| F7-ATJ-006 | Teclado no US | (Si es posible) teclado español. | Funcionan (usan la tecla física). Anotar en Mac (Alt = Option). | P3 | UX |

## 5. Criterios de salida específicos

- P0: F7-REP-012, F7-PDF-003, F7-NOT-003, F7-AUD-006 ejecutados.
- Riesgos verificados: R-ADM-01, 03, 10, 11, 12, 15; R-VIG-04; R-FAC-10.

## 6. Entregables

Informe de fase con los archivos exportados de muestra, defectos y registro de datos. Detenerse.
