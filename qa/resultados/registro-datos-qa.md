# Registro de datos QA

> Lo actualiza cada fase. Sirve para que la fase siguiente reutilice datos sin adivinarlos. **Sin contraseñas.**
> Ambiente: Local (`localhost:3000` / `localhost:5281`) · Base recreada el: 2026-10-02 (antes de F0)

## Usuarios
| Usuario | Roles | Activo | Creado en fase | Nota |
|---|---|---|---|---|
| admin | Admin | Sí | (bootstrap) | Contraseña definida por el usuario |
| capb90 | Admin | Sí | F0 (prep.) | Administrador de trabajo del QA |
| vigilancia | Receiving | Sí | F0 (prep.) | |
| bascula | Scale | Sí | F0 (prep.) | |
| facturacion | Billing | Sí | F0 (prep.) | |
| bodega | Warehouse | Sí | F0 (prep.) | |
| c_exterior | ForeignTrade | Sí | F0 (prep.) | |
| v_montenegro | Billing + Admin | Sí | F0 (prep.) | |
| j_coral | Billing + ForeignTrade | Sí | F0 (prep.) | |
| f_chosi | Scale + ForeignTrade | Sí | F0 (prep.) | |
| qa_cambio | Warehouse | Sí | F0 | Prueba del flujo de cambio de contraseña. Su contraseña actual es la de 101 caracteres de F1-AUT-011: resetear antes de usarla. |
| qa_bascula2 | Scale | Sí | F1 | Creada por formulario (F1-USR-002) |
| qa_inactivo | Warehouse | **No** | F1 | Desactivado con fecha de bloqueo 2026-10-03 |
| qa_admin2 | Admin + Billing | Sí | F1 | Pruebas de auto-quitarse rol / auto-desactivarse (restaurado) |
| qa_email_rep | Scale | Sí | F1 | Prueba de correo repetido (F1-USR-007) |

> Contraseñas: no se registran aquí. Las 10 cuentas creadas por el QA ya pasaron por el cambio obligatorio de contraseña. Correo `<usuario>@bodegas-qa.test`, teléfono `+570000000000`, identificaciones 100000001–100000010.

## Estado inicial de catálogos (F0)

| Catálogo | Estado |
|---|---|
| Productos | 5 sembrados: Contenedor Vacío (UNIDAD), Manteca (TONELADA), Granos (TONELADA), Enlatados (BULTO), Plátano Seco (BULTO) |
| Servicios | 5; BASCULA sin precio ni impuestos |
| Tarifas de montacargas | 5 tipos sin monto |
| Parámetro `INVENTORY_ADJUSTMENT_ADMIN_EMAIL` | vacío |
| Terceros, vehículos, conductores, ciudades, cuadrillas, embalajes | 0 |
| Ubicaciones | 20 · Unidades de medida 10 · Tipos de unidad de carga 3 · Motivos 7 |

## Terceros
| Nombre | Identificación | Roles de negocio | Config. facturación | Estado financiero | Nota |
|---|---|---|---|---|---|
| QA Cliente Uno SAS | NIT 900100001 | CUSTOMER | Pendiente F6 (plan: Mensual, 30 días, sin límite) | Active | contacto Ana QA; cuenta Bancolombia Ahorros; convenio QA-CONV-001 |
| QA Cliente Mora SAS | NIT 900100002 | CUSTOMER | Pendiente F6 (límite 1.000) | Active | |
| QA Cliente Consolidado SAS | NIT 900100003 | CUSTOMER | Pendiente F6 (Quincenal, Consolidated) | Active | |
| QA Importación Andina Ltda | NIT 900100004 | IMPORTER | — | Active | antes «QA Importador Ltda» (renombrado en F1-TER-009) |
| QA Exportador SAS | NIT 900100005 | EXPORTER | — | Active | |
| QA Agencia SIA Aduanas | NIT 900100006 | CUSTOMS_AGENCY | — | Active | |
| QA Transportes SAS | NIT 900100007 | TRANSPORT_COMPANY | — | Active | |
| QA Importadora Quito Cía | RUC 1790000000001 | IMPORTER, CUSTOMER | — | Active | contacto en Ecuador |
| QA Multirol Comercial | NIT 900100008 | CUSTOMER, IMPORTER | — | Active | |
| QA Mismo Numero CC | CC 900100001 | CUSTOMER | — | Active | prueba de unicidad por tipo |
| QA <b>Negrita</b> Compañía Ñandú | NIT 900100092 | TRANSPORT_COMPANY | — | Active | para F9-INP-001 (HTML) y F7-PDF-008 (ñ) |

## Catálogos y tarifas
| Tipo | Código / nombre | Valor relevante | ID | Fase |
|---|---|---|---|---|
| Convenio | QA-CONV-001 (QA Cliente Uno) | ALMACENAMIENTO IMP PERCENTAGE_OF_VALUE 0,255 % / mín. 184.000 / umbral 72.156.863; BASCULA FIXED 25.000; MONTACARGAS PER_VEHICLE_TYPE 90/70/50/45/30 mil; GUIA_SALIDA FIXED 30.000. **Desactivados:** ALMACENAMIENTO EXP 150 % (F6-TAR-008) y ALMACENAMIENTO INSP FIXED 50.000 con complementario PAPELERIA (F6-ALM-014) | | F1 |
| Precio base | BASCULA | 24.000 vigente (23.000 cerrado el 2-oct) | | F1 |
| Precio base | GUIA_SALIDA | 35.000 | | F1 |
| Tarifa base | ALMACENAMIENTO IMP | PER_UOM 1.500 por BULTO, producto QA Cebolla | | F1 |
| Tarifa base | ALMACENAMIENTO EXP | FIXED 150.000 (genérica) | | F1 |
| Tarifa base | ALMACENAMIENTO INSP QA Cebolla | FIXED 99.000 **desactivada** (prueba de perecedero, DEF-F1-003) | | F1 |
| Mínimo | ALMACENAMIENTO | IMP 184.000; EXP 0; INSP 0 | | F1 |
| Impuestos | ALMACENAMIENTO IVA; BASCULA IVA 19 % (asignado en F2 por decisión del usuario) | | | F1/F2 |
| Tarifas montacargas | Tractomula 80.000 · DobleTroque 65.000 · Sencillo 45.000 · Turbo 40.000 · GuacalEstiba 25.000 | | | F1 |
| Servicio | QA_SERVICIO | creado | | F1 |
| Producto | QA Cebolla | BULTO, embalaje QA-CAJA, SKU SKU-20261002-153510 | | F1 |
| Producto | QA Aceite | LITRO, SKU QA-SKU-ACEITE | | F1 |
| Producto | QA Repuestos | UNIDAD, SKU QA-SKU-REPUESTOS | | F1 |
| Producto | QA Prueba Emb / SinEmb / EmbNull / PkgTxt | **inactivos** (basura de DEF-F1-001) | | F1 |
| Embalaje | QA-CAJA | QA Caja de cartón | | F1 |
| Unidad de medida | QA_ROLLO | **inactiva** | | F1 |
| Tipo de unidad de carga | QA_ISOTANQUE | | | F1 |
| Ciudad | QA Quito | ECU, PICHINCHA, 3 días | | F1 |
| Ciudad | QA Bogota | COL, DC, 0 días, destino de abandono | | F1 |
| Cuadrilla | QA Cuadrilla 1 | activa | | F1 |
| Motivo | QA Motivo pesaje | requiere pesaje = **No** (para F2-INT-006) | | F1 |
| Ubicación | C01-R01-N01 | **no disponible** (para F4-REC-010) | | F1 |
| Parámetro | INVENTORY_ADJUSTMENT_ADMIN_EMAIL | qa-ajustes@bodegas-qa.test | | F1 |

## Vehículos y conductores
| Placa / documento | Tipo | Transportadora / país | ID | Fase |
|---|---|---|---|---|
| QAA101 | Tractomula | QA Transportes SAS / Colombia | | F1 |
| QAA102 | Sencillo | QA Transportes SAS / Colombia | | F1 |
| QAA103 | Turbo | QA Transportes SAS / Ecuador | | F1 |
| qaa101, QA A-1#, QAZ999 | — | **inactivos** (basura de DEF-F1-005) | | F1 |
| CC 1000000001 | Conductor Pedro QA Conductor Colombia | Colombia | | F1 |
| Pasaporte 1700000001 | Conductor Jorge QA Conductor Ecuador | Ecuador | | F1 |
| Pasaporte 1000000001 | Conductor «Mismo Numero» | prueba de unicidad | | F1 |

## Ingresos (Vigilancia)
| Placa | Motivo | Hora ingreso | Salida | EntryLog ID | Fase | Usado en |
|---|---|---|---|---|---|---|
| QAA101 | Descargue mercancia importacion | 16:00 | — | | F2 | F3 ingreso IMP |
| QAB201 | Descargue mercancia importacion | 16:00 | — | | F2 | F3 segundo camión mismo documento |
| QAB202 | Descargue mercancia importacion | 16:01 | — | | F2 | F3 unidades de carga / tanquero |
| QAA102 | Descargue mercancia exportacion | 16:04 | — | | F2 | F3 ingreso EXP |
| QAA103 | Solo Bascula | 16:04 | — | | F2 | F3 solo báscula |
| QAB203 | Descargue mercancia importacion (observación de 646 car.) | 16:04 | — | | F2 | F3 INSP |
| QAB204 | Solo bodega | 16:04 | — | | F2 | F4 recepción sin báscula |
| QAB205 | Cargue mercancia importacion | 16:04 | — | | F2 | F3/F5 salida |
| QAC303 | Otro (fecha corregida −1 h y +1 min) | — | — | | F2 | pruebas de corrección |
| QAC305 | QA Motivo pesaje (sin pesaje) | 16:04 | — | | F2 | F2-INT-006 |
| QAC392 | Otro (corregido desde QAC302; QAC302 desactivado) | 16:04 | — | | F2 | F2-COR-002 |
| QAC304 | Descargue importación (corregido desde Otro) | 16:04 | 16:07 | | F2 | — |
| QAA102 | Otro (**mal asignado**: se digitó AA102, DEF-F2-001) | 16:00 | 16:03 | | F2 | — |
| AB#12 | Otro (vehículo con placa inválida, DEF-F2-002) | 16:02 | 16:03 | | F2 | — |
| QAZ999 | Otro (vehículo inactivo) | 16:02 | 16:03 | | F2 | — |
| QAC320 | Otro → Solo bodega (ingreso **futuro** 05/10 por API, salida 02/10, DEF-F2-003) | 05/10 16:02 | 02/10 16:02 | | F2 | — |

## Operaciones de báscula
| Tiquete | Placa | Tipo operación | Documento / OC | Estado ciclo | Factura | Fase |
|---|---|---|---|---|---|---|
| 2026T00001 | QAA101 | Ingreso IMP (UI) | QA-CP-0001 | Complete (35.000/15.000, neto 20.000) | Paid $28.560 conductor | F3 |
| 2026T00002 | QAB201 | Ingreso IMP 2.º camión (UI) | QA-CP-0001 | Complete (30.000/12.000) | Draft por facturar $29.750 QA Cliente Uno | F3 |
| 2026T00003 | QAA102 | Ingreso EXP (UI) | QA-CP-0002 | Complete (28.000/13.000) | **2 facturas Paid $29.750 (DEF-F3-002)** + ciclo huérfano 374b7833 | F3 |
| 2026T00004 | QAB203 | INSP (API) | QA-CP-0003 | Complete (21.000, un pesaje) | Paid $29.750 QA Cliente Uno | F3 |
| 2026T00005 | QAA103 | Solo báscula (UI) | — | Complete (18.000 Tara) | Paid $28.560 Consumidor final | F3 |
| 2026T00006 | QAB202 | Ingreso IMP tanquero QAT001 (API) | QA-CP-0005 | **FirstWeightCaptured** (45.000) | Paid transferencia $29.750 | F3 |
| 2026T00007 | QAC406 | Ingreso IMP (API) | QA-CP-0406 | **Anulado** (salida con ciclo abierto, DEF-F3-005) | Paid $28.560 CF | F3 |
| 2026T00008 | QAB205 | Salida OC 2026OC00001 (UI) | 2026OC00001 | **FirstWeightCaptured** (Tara 14.000) — repesar tras cargue F4 | Paid $28.560 CF | F3 |
| — | QAC401/403/404 | Ingresos por API (pruebas de validación) | QA-CP-0401/0403 | Por cobrar | — | F3 |
| — | QAC402 | Descartado → **atascado «Por cobrar» y cobrado (DEF-F3-004)** | QA-CP-0402 | ciclo 23ece56f ReadyForWeighing | Paid CF | F3 |
| — | QAC405 | Camión tardío a 2026EXP00001 | QA-CP-0002 | Por cobrar | — | F3 |
| — | QAC407 | Ingreso (total editable 30.000) | QA-CP-0407 | ReadyForWeighing | Paid $30.000 CF | F3 |
| — | QAC408 | 2.ª salida con la misma OC (descartada → atascado) | — | Por cobrar | — | F3 |
| varios | QAC409 | Solo báscula 2 pesajes (API) | — | Complete neto 15.000 | Paid $29.750 | F3 |
| varios | QAC410 | Ingreso (persona no registrada «QA») tara > bruto | QA-CP-0410 | Complete neto 5.000 tras corregir | Paid $28.560 «QA» | F3 |
| — | QAC415 | Primer pesaje Tara (API) | QA-CP-0415 (2026BA00011) | Complete | Paid CF | F3 |
| — | QAC416 | Solo báscula retomada (DEF-F3-017) | — | ReadyForWeighing, sin factura enlazada | cobrado por ruta de depósito | F3 |
| — | QAC417 | Salida 2026OC00002 | — | Complete (antes del cargue) | Paid $29.750 | F3 |
| — | QAC418 | Salida con OC cancelada | — | Por cobrar | — | F3 |
| — | QAA103 (2.º ingreso) | Ingreso EXP (UI) | QA-CP-0420 (2026BA00012) | ReadyForWeighing | Paid CF | F3 |
| — | QAB203 (2.º ingreso) | Ingreso EXP (API, tiempos) | QA-CP-0421 | FirstWeightCaptured | Paid CF | F3 |
| — | QAC411–414 | Pruebas de producto nuevo y ambigüedad | QA-CP-0401 / QA-CP-AMB | Por cobrar | — | F3 |

## Depósitos
| Número | Modalidad | Carta porte | Camiones | Estado | Cliente / terceros | Nacionalización | Fase |
|---|---|---|---|---|---|---|---|
| 2026BA00001 | IMP | QA-CP-0001 | QAA101 (100) + QAB201 (60) | **Confirmed**, ingreso de camiones cerrado | QA Cliente Uno · Importador QA Importación Andina · Agencia QA SIA · USD 50.000 | **Nacionalizado** (QA-LEV-001, 100) · reservado 80 (OC) | F3 (prep. CE) |
| 2026EXP00001 | EXP | QA-CP-0002 | QAA102 (50) + QAC405 tardío (5) | **Closed** (F4: OC7 55, stock 0; detalle 404, DEF-F4-006) | QA Cliente Uno · Exportador QA Exportador · COP 50.000.000 | — | F3 (prep. CE) |
| 2026INSP00001 | INSP | QA-CP-0003 | QAB203 (40 QA Repuestos) | Draft (F4: confirmado → OC9 → devuelto a Borrador → cargue 10 ejecutado; stock 30, DEF-F4-004) | QA Cliente Uno | — | F3 |
| 2026BA00005 | IMP | QA-CP-0005 | QAB202 tanquero QAT001 (30.000 L QA Aceite) | Draft | — | — | F3 |
| 2026BA00002 | IMP | QA-CP-0401 | QAC401 (10) + QAC411 (2 + 7 aceite) | Draft | sin transportadora (DEF-F3-009) | — | F3 |
| 2026BA00004 | IMP | QA-CP-0403 | QAC403 + QAC404 | Draft | valor sin moneda | — | F3 |
| 2026BA00007 | IMP | QA-CP-0407 | QAC407 | Draft | — | — | F3 |
| 2026BA00008 | IMP | QA-CP-0410 | QAC410 | Draft | — | — | F3 |
| 2026BA00009 / 00010 | IMP | QA-CP-AMB (fechas distintas) | QAC412 + QAC414 / QAC413 | Draft | — | — | F3 |
| 2026BA00003 | IMP | QA-CP-0402 | — | **Cancelled** (descartado) | — | — | F3 |
| 2026BA00006 | IMP | QA-CP-0406 | — | **Cancelled** (pesaje anulado) | — | — | F3 |
| 2026INSP00002 | INSP | Recepción directa (API) | QAB204 (20 QA Repuestos) | Confirmed | QA Cliente Mora | Factura almacenamiento Borrador $178.500 | F4 |
| 2026INSP00003 | INSP | Recepción directa (API) | QAB204 (20 QA Repuestos) | Confirmed · reservado 7 (OC10) | QA Cliente Uno | Factura almacenamiento Borrador $0 | F4 |

### Cambios de estado en la fase 5
| Depósito | Estado tras F5 | Datos clave |
|---|---|---|
| 2026BA00002 | Confirmed · **Nacionalizado** · ingreso cerrado · prórroga | Confirmado por la interfaz; USD 50.000, TRM DIAN 3.307,73; QA-LEV-201 (Cebolla 10, FOB 8.000) + QA-LEV-201 Aceite 3 (FOB vacío); manifiesto DIAN QA-DIAN-002; stock Cebolla 2, Aceite 7 |
| 2026BA00004 | Confirmed · Nacionalizado | Confirmado sin recepción; devuelto y reconfirmado; QA-LEV-403 (20) con recibido 15 (pendiente −5, DEF-F5-004); fecha de ingreso corregida |
| 2026BA00005 | Confirmed · Nacionalizado | Tanquero QAT001 → placa **QAT009**; QA-LEV-501 (30.000 L) |
| 2026EXP00002 | Confirmed (cerrado por OC13 y reabierto al revertir) | Exportador QA Exportador SAS; stock 6 |
| 2026INSP00001 | Confirmed | Recibido ajustado 40 → 35 (CE-7, sin movimiento); stock 30 (OC9 revertida, OC17 despachó 5) |
| 2026BA00011 | **Cancelled** | Con levante QA-LEV-1100 aceptado (DEF-F5-005) |
| 2026INSP00002 / 00003 | **Cancelled** | Facturas de almacenamiento anuladas |
| 2026BA00008 | Draft | Cantidad corregida 3 → 4 |
| 2026BA00009 / 00010 | Draft | BA00009 con fecha de documento 30/09/2026 (BA00010 rechazado por duplicado) |

## Recepciones y montacargas
| ID | Depósito / placa | Estado | Diferencia | Factura | Fase |
|---|---|---|---|---|---|
| Recepción 35ecb101 | 2026EXP00002 / QAB203 | Completed (interfaz, 1 foto, firma) | 6 = 6 | — | F4 |
| Recepción 3dcbb9e5 | 2026INSP00001 / QAB203 | Completed (6 fotos) | 35 de 40 (−5) | — | F4 |
| Recepción de63dc66 | 2026BA00002 / QAC411 | Completed (PDF como foto) | Cebolla 2; Aceite 7 sin contar | — | F4 |
| Recepción 7dfeaa1c | 2026BA00001 / QAA101 | Completed (`POST receptions`, un paso) | 100 | — | F4 |
| Recepción 6af9b00b | 2026INSP00002 / QAB204 | Completed (directa por API) | 20 | Almacenamiento $178.500 | F4 |
| Recepción 8d8294db | 2026INSP00003 / QAB204 | Completed (directa por API) | 20 | Almacenamiento $0 | F4 |
| Recepción 58713672 | 2026BA00005 / QAB202 tanquero | **InProgress sin salida** (DEF-F4-001) | — | — | F4 |
| Montacargas f973eec5 | QAB201 · Tractomula · 100→102 h | Complete | — | Pagada 80.000 sin IVA | F4 |
| Montacargas de294a13 | QAB201 · GuacalEstiba · 0→0 h | Complete | — | Pagada 119.001,19 (100.001 + IVA) | F4 |
| Montacargas ea2dce04 | QAB201 · Tractomula · 200→202 h (interfaz) | Complete | — | Borrador 107.100 (pendiente por facturar) | F4 |
| Novedad db75c167 | 2026INSP00001 / QAB203 | Vigente (40/34/4/2) | — | — | F4 |
| Novedad (cuadre 100/90/20) | 2026INSP00001 / QAB203 | Anulada | — | — | F4 |

## Levantes, órdenes de cargue y guías
| Tipo | Número | Depósito(s) | Estado | Factura | Fase |
|---|---|---|---|---|---|
| Levante | QA-LEV-001 (aceptación QA-ACE-001, 100, FOB USD 30.000, tasa manual 4.000) | 2026BA00001 | Vigente | — | F3 (prep.) |
| Levante | QA-LEV-002 (60) | 2026BA00001 | Vigente | — | F3 (2.ª pasada) |
| Orden de cargue | 2026OC00002 (20, QAC417) | 2026BA00001 | **Dispatched** (F4) | — | F3 |
| Orden de cargue | 2026OC00003 (5, QAC418) | 2026BA00001 | **Cancelled** (con salida iniciada, DEF-F3-012) | — | F3 |
| Orden de cargue | 2026OC00004 (5) | 2026BA00001 | **Cancelled** (vehículo inactivo qaa101, DEF-F3-016) | — | F3 |
| Orden de cargue | 2026OC00005 (5, QAA101) | 2026BA00001 | **Dispatched** (F4) | — | F3 |
| Orden de cargue | 2026OC00001 (externa QA-OE-001, emisor QA Agencia SIA, 80 QA Cebolla, QAB205, QA Quito, QA Cuadrilla 1) | 2026BA00001 | **Dispatched** (F4, interfaz) | — | F3 (prep.) |
| Orden de cargue | 2026OC00006 (QA-OE-006, 30, QAB201) | 2026BA00001 | **Loaded** 20 de 30 (10 liberados) | — | F4 |
| Orden de cargue | 2026OC00007 (QA-OE-007, 55, QAA102) | 2026EXP00001 | **Dispatched**; depósito Closed | Sin cargo | F4 |
| Orden de cargue | 2026OC00008 (QA-OE-008, 5) | 2026BA00001 | **Cancelled** desde Bodega | — | F4 |
| Orden de cargue | 2026OC00009 (QA-OE-009, 10, QAB201) | 2026INSP00001 | **Loaded** con el depósito en Borrador (DEF-F4-004) | — | F4 |
| Orden de cargue | 2026OC00010 (QA-OE-010, 7, QAB201) | 2026INSP00003 | Pending | — | F4 |
| Guía de salida | 2026S00001 (Export, vence 2026-10-05) | 2026EXP00001 / OC7 | Vigente, sin factura | — | F4 |
| Orden de cargue | 2026OC00011 (QA-OE-201, 8 Cebolla, QAA103) — creada por la interfaz | 2026BA00002 | Loaded · guía S00002 | GUIA_SALIDA pagada 30.000 | F5 |
| Orden de cargue | 2026OC00012 (QA-OE-308) | 2026INSP00002 | Cancelled | — | F5 |
| Orden de cargue | 2026OC00013 (QA-OE-310, EXP 6) | 2026EXP00002 | **Reverted** (guía S00005 anulada) | — | F5 |
| Orden de cargue | 2026OC00014 (QA-OE-311, BA00001 4 + BA00002 2) | 2 depósitos | Loaded · guía S00004 | GUIA_SALIDA 60.000 en Borrador | F5 |
| Orden de cargue | 2026OC00015 (QA-OE-312, multi-cliente) | 2026BA00001 (3) | Pending (ítem de INSP00002 retirado al anular) | — | F5 |
| Orden de cargue | 2026OC00016 (QA-OE-502, tanquero parcial) | 2026BA00005 | Cancelled | — | F5 |
| Orden de cargue | 2026OC00017 (QA-OE-601, 5 Repuestos, QAB203) | 2026INSP00001 | **Dispatched** (anclada a T00004) | — | F5 |
| Orden de cargue | 2026OC00009 | 2026INSP00001 | **Reverted** | — | F5 |
| Orden de cargue | 2026OC00010 | 2026INSP00003 | Cancelled (por anulación del depósito) | — | F5 |
| Guía de salida | 2026S00002 (IMP) | BA00002 / OC11 | Vigente | Pagada 30.000 | F5 |
| Guía de salida | 2026S00003 (IMP) | OC14 | **Anulada** | Factura anulada | F5 |
| Guía de salida | 2026S00004 (IMP, 2 depósitos) | OC14 | Vigente | 60.000 en Borrador | F5 |
| Guía de salida | 2026S00005 (EXP automática) | OC13 | **Anulada** | Sin cargo | F5 |
| Levante | QA-LEV-201 (BA00002), QA-LEV-401 (retirado), QA-LEV-403, QA-LEV-501, QA-LEV-1100 (anulado) | — | — | — | F5 |
| Lista de empaque | QA Proveedor Empaque · QAPK-01, QAPK-02 (importador QA Importación Andina) | — | Vigente | — | F5 |

## Facturas y pagos
| N.º interno / SIIGO | Servicio | Cliente / destinatario | Estado | Total | Pagado | Fase |
|---|---|---|---|---|---|---|

## Fase 6 — Facturación
| Dato | Detalle |
|---|---|
| Configuraciones | Uno: Mensual/30/PerService/sin límite · Mora: Mensual/30/límite 1.000 · Consolidado: Biweekly/15/Consolidated/límite 10.000.000 · Multirol: Weekly/10/límite 0 · Importadora Quito: OnDemand · Mismo Numero: Days15/5 |
| Convenios | QA-CONV-CONS (Consolidado): PRORATED Cebolla 0,3 %, PER_VEHICLE Repuestos 40.000, PER_VEHICLE Tornillo 30.000, WEIGHT_THRESHOLD Tuerca (2 productos homónimos), FIXED IVA incl. 100.000 genérico IMP, PER_CARGO_UNIT Aceite · QA-CONV-MN (Mismo Numero): FIXED 50.000 IMP · QA-CONV-001 (Uno): + PER_CARGO_UNIT Aceite **inactivo** |
| Depósitos nuevos | BA00013 Multirol · BA00014–17, BA00019 Consolidado · BA00018 Uno USD (TRM manual 4.100) · BA00020 Mora · BA00021/22 (cobros por facturar Consolidado, Draft) · BA00023 (bloqueo, Draft) · BA00024 Quito OnDemand (sin factura) · BA00025 Mismo Numero |
| OC nuevas | 2026OC00018 (BA00017, 10) y 2026OC00019 (BA00013, 4), despachadas sin guía |
| Facturas con N.º | QA-SIIGO-0001 Paid · 0005 Paid (saldo a favor 16.700) · 0011 PartiallyPaid vencida · 0013 Overdue (Multirol) · 0014 Overdue (Consolidado) · 0018 Draft · 0041 Paid (Mora) |
| Estados financieros | Mora Active · **Multirol Blocked** · Uno y Consolidado OverdueWarning |
| Palancas SQL | `f6_palanca1.sql`, `f6_palanca2.sql` (en esta carpeta) + TRM NULL en BA00018 |
| API | Corriendo en la pestaña del panel «wms-api (QA F6)» (`dotnet run --launch-profile http`), no en Rider |

## Fase 7 — Transversal
| Dato | Detalle |
|---|---|
| Ingresos | QAF701 (motivo Otro) con salida — trazabilidad «En portería» (DEF-F7-002) |
| Cambios de catálogo | Producto QA Tuerca empaque (af8b…) «QA editado F7»; QA Mismo Numero CC cámara «QA-CC-F7»; embalaje y unidad Bulto con descripción «QA F7»; tarifa montacargas Turbo 40.001 → 40.000 |
| Usuarios | `qa_cambio`: contraseña restablecida a la contraseña QA autorizada; rol Bodega quitado y restaurado |
| Depósitos | 2026BA00025 planilla QA-PL-F7 |
| Muestras | `muestras-f7/` (Excel y PDF exportados) |
| API | Pestaña del panel «wms-api (QA)»; frontend preview `wms-dev` |


## Fase 8 — Flujos E2E (prefijo QAE, 03/10/2026)
| Dato | Detalle |
|---|---|
| Placas | QAE001–QAE029, QAE28X (corregida a QAE028); contenedor QAEC0001 |
| Cartas porte | QAE-CP-001 … QAE-CP-021B |
| Depósitos cerrados | 2026BA00026 (E2E-01) · BA00027 (E2E-02) · BA00028 (E2E-03/12/13) · BA00036 (E2E-15/17) · EXP00003 (E2E-04) · EXP00004 (E2E-05) |
| Depósitos confirmados con stock | BA00035 Uno USD 40 (E2E-14, TRM manual 4.000) · INSP00004 Mora 15 (E2E-06) · INSP00005 Uno 12 (E2E-08) · INSP00006 / INSP00007 Mora 3 + 3 (E2E-12, recepción directa) |
| Depósitos en Borrador (operación abierta) | BA00029 (QAE016, E2E-09, stock 30) · BA00033 (QAE021, sin pesar) · BA00034 (QAE023, solo bruto) · BA00037 (QAE028, E2E-16) · **BA00038 / BA00039 duplicados del mismo camión QAE029 (DEF-F3-002)** |
| Depósitos anulados | BA00030 (descarte) · BA00031 (pesaje anulado) · BA00032 (anulado en E2E-11) · **2025BA00001** (ingreso fechado 31/12/2025, descartado) |
| OC | 2026OC00020–00029 (00021/22/27/28 quedan Loaded con guía; 00026 Reverted; 00029 Dispatched **sin guía**, DEF-F8-003) |
| Guías | 2026S00006–00014 (00012 anulada) |
| Levantes | QAE-LEV-001, 003, 012, 017, 021, 022 |
| Tiquetes | 2026T00015–00033 |
| Facturas con N.º | QAE-SIIGO-001 (298.002,17 Approved) · QAE-SIIGO-003 (214.200 Paid) · QAE-SIIGO-007 (29.750 Paid, solo báscula) · QAE-SIIGO-014 (242.760 Approved, TRM manual) |
| Facturas a revisar | `663899` y `ea0dda` (doble cobro QAE029, 28.560 c/u) · `d058ff` (guía multi-cliente a Uno, 60.000) · `065fd6` (renovación BA00028, 196.350) |
| Estados financieros | QA Cliente Mora: Blocked → pagada → **Active** · Multirol sigue Blocked |
| Ingresos abiertos (camiones en planta) | QAE015 (2 ingresos), QAE021, QAE023, QAE027 (fechado 31/12/2025), QAE028, QAE029 y los vehículos de recepción directa QAE022/QAE024 |
| Palancas y ambiente | `f8_palanca_mora.sql` (vencimiento de QAE-SIIGO-003); 6 reinicios del API; un arranque con `DianTrm__BaseUrl=http://127.0.0.1:9` para simular la DIAN caída (solo variable de entorno, sin tocar código) |
| Usuarios | `f_chosi` usado en E2E-18 (sin cambios) |
| PDF | `muestras-f8/` (guías E2E-01/02/10 y ZIP, etiquetas E2E-02/04/06/15) |

## Fase 9 — Roles y permisos (03/10/2026)
| Dato | Detalle |
|---|---|
| Terceros | «QA F9 Tercero creado por Bascula» (NIT 900999901; convenio QA-F9-BAS con una tarifa, **archivado**) · «QA F9 \<b\>negrita\</b\>\<img…\>» (NIT 900999902, prueba de HTML) |
| Motivos de ingreso | «QA F9 motivo creado por Bascula», creado y borrado por `bascula` |
| Ingresos | QAF901 (motivo Otro) con salida «autorizada por» facturacion y observación de 10.000 caracteres · QAF902 (recepción directa) |
| Depósitos | 2026INSP00008 (QAF902, Confirmed, 1 QA Repuestos) · **2026BA00040 / 2026BA00041** duplicados de QAE030 (QAE-CP-022) con dos facturas Paid de 28.560 |
| Usuarios | `j_coral`: rol Billing quitado y restaurado (queda Billing + ForeignTrade) |
| Sesión del navegador | Quedó con `capb90` |
| Muestras | `muestras-f9/` (matriz del API y resultado de la interfaz por cuenta); anexo `F9-anexo-matriz-api.md` |

## Fase 10 — UX y errores (03/10/2026)
| Dato | Detalle |
|---|---|
| Báscula (UI) | QAF003 → **2026BA00042** (QAF10-CP-001, QA Cebolla 10), cobro inmediato 28.560 al conductor, bruto 30.000; queda «Por repesar» |
| Doble clic | QAE028 (BA00037) cobrado con doble clic → 1 factura `c177b251` Paid y 1 ciclo `eb556df7` |
| Pagos | QAE-SIIGO-001: pago de 100.000 (ref. QAF10-DOBLE) → PartiallyPaid, pendiente 198.002,17. El intento con comprobante (QAF10-COMPROBANTE) fue rechazado (409) y no creó pago |
| Facturas | 065fd6: notas modificadas en ERR-008/009 y restauradas a «Factura de almacenamiento - período 03/10/2026 - 03/11/2026» |
| Ambiente | API detenido unos 30 s y relanzado (pestaña «wms-api (QA)»); navegador con `capb90`, sin emulación |
| Muestras | `muestras-f10/` (capturas a 1366, 1024 y tableta; API caído; factura inexistente) |
