# 05 · Trazabilidad legacy: capacidad → rutas → scripts → tablas

> Auditoría estática del 2026-10-23 (AG-05). **Prefijos:** `LL/` = `bodegas-legacy/modulos/mod_levantes/`, `LS/` = `bodegas-legacy/modulos/mod_salidas/`, `SCH` = `bodegas-legacy/bodegas_schema.sql`.
> L = lectura, E = escritura. Esquema: `levante` (`SCH:597-619`), `producto_levante` (`SCH:1061`), `salida` (`SCH:1309-1338`), `producto_salida` (`SCH:1084`), `guiadesalida` (`SCH:510-523`, `UNIQUE id_salida`), `ordencargue` (`SCH:821-833`), `pesaje` (`SCH:920`), `ciudad` (`SCH:124`), `cuadrilla` (`SCH:247`), `cliente.sinsalidas` (`SCH:194`).

| Capacidad | Ruta (menú) | Scripts | Tablas y campos |
| --- | --- | --- | --- |
| CF-L143 | Levantes › Listar | `LL/listarlevantes.php` | L: `ingreso`, `documentocomercial`, `deposito`, `levante` (`nro_levante`, `nro_aceptacion`, `fecha_levante`), `producto_levante.cantidad_levante`, `producto_en_bodega.cantidad`, `productoamparado`, `tasa_cambio.valor`, `pesaje.peso_manifiesto` |
| CF-L144 | Levantes › Nuevo | `LL/registrarlevante.php`, `LL/seleccionardeposito.php` | L: `tasa_cambio`, `levante` (duplicado); E: `levante` (`id_importador`, `tasa_cambio`, `fob_dolares`, `fob_pesos`, `nro_aceptacion`, `fecha_aceptacion`, `nro_levante`, `fecha_levante`, `peso_bruto`, auditoría usuario/IP/fecha), `producto_levante` (`id_productoenbodega`, `cantidad_levante`, `id_levante`), `productodetalle.id_productolevante` |
| CF-L145 | Levantes › Editar | `LL/modificarlevante.php` | E: `levante` (además `nro_manifiestodian`, `fecha_manifiestodian`, `estado`), `producto_levante` (DELETE + INSERT) |
| CF-L146 | Levantes › Eliminar | `LL/eliminarlevante.php` | E: `productodetalle.id_productolevante = NULL`; DELETE `producto_levante`, `levante` |
| CF-L147 | Levantes › Asignar productos | `LL/asignarproductos.php`, `LL/listarproductos.php`, `LL/listarproductosajax.php` | E: `producto_levante`, `productodetalle` |
| CF-L149 | Levantes › Quitar producto | `LL/eliminarproductolevante.php` (VIN: `LL/eliminarvinlevante.php`) | E: DELETE `producto_levante` |
| CF-L150 | Levantes › Soportes | `LL/subirsoportes.php`, `LL/procesa.php` | Archivos `documentos/<nro_levante>/` |
| CF-L151 | Salidas › Listar (IMP) | `LS/listarsalidas.php` | L: `salida`, `cliente`, `empresa_transporte`, `producto_salida`, `guiadesalida`, `ordencargue.estado`, `pesaje`; E: `salida.estado='incompleto'` |
| CF-L152 | Salidas › Listar (EXP) | `LS/listarsalidasexp.php` | Ídem |
| CF-L153 | Salidas › Nueva | `LS/nuevasalida.php`, `LS/nuevasalidaexp.php`, `LS/salidausartiquete*.php`, `LS/salidanrodeposito*.php`, `LS/salidaglobal.php`, `LS/salidaconsolidada*.php` | — |
| CF-L154 | Salidas › Registrar IMP | `LS/registrarsalida.php` | L: `deposito`, `ingreso`, `cliente.sinsalidas`, `levante`, `producto_levante`, `producto_salida`; E: `salida` (`id_modalidad`, `fecha_salida`, `nro_salida`, `tipo_salida`, `id_cliente`, `id_empresatransporte`, `id_sia`, `id_ciudaddestino` —lista separada por comas—, `id_cuadrilla`, `observaciones`), `pesaje.id_salida`, `producto_salida` (`cantidad_salida`, `saldo_anterior`, `id_pesaje`), `productodetalle.id_productosalida` |
| CF-L155 | Salidas › Registrar EXP | `LS/registrarsalidaexp.php` | Ídem (modalidad 5) |
| CF-L156 | Salidas › Consolidada | `LS/registrarsalidaconsolidada.php`, `LS/registrarsalidaconsolidadaexp.php` | E: `salida` (`tipo_salida='consolidada'`), `vehiculo_x_empresa`, `producto_salida` |
| CF-L158 | Salidas › Editar | `LS/modificarsalida.php`, `LS/modificarsalidaexp.php`, `LS/modificarorden.php` | E: `salida` (cabecera), `producto_salida` (DELETE + INSERT), `productodetalle`, `ordencargue.fechahora_inicio` |
| CF-L159 | Salidas › Eliminar | `LS/eliminarsalida.php` | E: `productodetalle.id_productosalida`, `productodetalle_x_seccion.estado='activo'`, DELETE `producto_salida`, `salida.estado='eliminado'`, `salida.motivo`, INSERT `salida` (`incompleto`), `pesaje.id_salida` |
| CF-L160 | Salidas › Asignar productos | `LS/asignarproductos.php`, `LS/listarproductoslevante.php`, `LS/listarproductosajax.php` | E: `producto_salida`, `productodetalle` |
| CF-L162 | Salidas › Quitar producto | `LS/eliminarproductosalida.php` (VIN: `LS/eliminarvinasignado.php`) | E: DELETE `producto_salida` |
| CF-L163 | Salidas › Crear/Ver guía | `LS/verguia.php`, `LS/contarimpresiones.php`; PDF por `reportes/crearpdf.php` desde `reportes/salidas/salida_u{usuario}.html` | E: `guiadesalida` (`fecha_guiadesalida`, `nro_guiadesalida`, `impresiones`, `estado`), `salida.num_guias`, `productodetalle_x_seccion.estado='libre'`; L: `ciudad.dias`, `cuadrilla.nom_cuadrilla` |
| CF-L164 | Salidas › Aut. Cargue | `LS/autorizarcargue.php`, `LS/modificarorden.php`; PDF desde `reportes/ordenes/orden_u{usuario}.html` | E: `ordencargue` (`id_salida`, `fechahora_inicio`, `id_usuarioautoriza`, `ip_autoriza`, `estado`) |
| CF-L165 | (embebido) | `LS/vertiquete.php` | L: `recibo`, `detallerecibo`, `pesaje`, `factura`, `resolucion_numeracion` |
| CF-L166 | Salidas › Global | `LS/listarpesajesglobal.php`, `LS/salidaglobal.php` | L: `pesaje`, `ingreso`; E (por `registrarsalida.php`): `salida` (`tipo_salida='global'`), `pesaje.id_salida` de cada tiquete |
| CF-L167 | Salidas › Soportes | `LS/subirsoportes.php`, `LS/procesa.php`, `LS/asignarimagenes.php`, `LS/imprimirsoportes.php` | Archivos `documentos/<nro_salida>/` |
| CF-L238 | (AJAX) | `LL/seleccionardeposito.php`, `LL/seleccionardeposito_ante.php`, `LL/seleccionarvin.php` | L: `deposito`, `producto_en_bodega`, `producto_levante` |
| CF-L239 | (AJAX) | `LS/seleccionarciudad.php`, `LS/seleccionardepositosaldo.php`, `LS/seldepositoexp.php`, `LS/seleccionartiqueteingreso*.php`, `LS/seleccionartiquetesalida*.php`, `LS/seleccionartiquetecolmotores.php`, `LS/listarproductosajax.php` | L: `ciudad`, `vista_kardexdepositos`, `pesaje`, `factura`, `vehiculo`, `producto_levante`, `producto_salida` |
| CF-L261 | Salidas › Listar | `LS/listarsalidas.php:629-643` | E: `salida.estado` |
| CF-LX05-01 | Clientes › Editar; Salidas › Registrar | `mod_clientes/modificarcliente.php`, `LS/registrarsalida.php` | L/E: `cliente.sinsalidas` |
| CF-LX05-02 | Salidas › Listar | `LS/listarsalidas.php:688-705`, `LS/autorizarcargue.php:39-46` | L: `permisos` (`crearguiasinautorizacion`), `ordencargue.estado` |

## Equivalencia de tablas en V2

| Legacy | V2 (`Backend/wms-api/Wms.Domain/Entities/...`) |
| --- | --- |
| `levante` + `producto_levante` | `ForeignTrade/ImportRelease` (una fila por producto del depósito, con FOB, tasa, fuente y fecha) |
| `salida` (cabecera) | `Warehouse/LoadingOrder` (`OrderNumber`, vehículo, conductor, `DestinationCityId`, `CrewId`, orden externa, estados) |
| `producto_salida` | `Warehouse/LoadingOrderItem` (`Quantity`, `LoadedQuantity`) + `WarehouseReserve` + `InventoryMovement` (`Out` al cargar, `In` al revertir) |
| `ordencargue` | La misma `LoadingOrder` (DEC-016) |
| `guiadesalida` | `Warehouse/DispatchGuide` (+ `Warehouse/DispatchGuideLine` con saldos congelados, `ForeignTrade/DispatchGuidePrintLog`, anulación) |
| `pesaje.id_salida` | `ServiceRecord` de salida (`LoadingOrderId`, `AnchorWeighbridgeCycleId`, `SourceEntryCycleId`) — módulo 02 |
| `ciudad.dias`, `cuadrilla` | `Administration/City.TransitDays`, `Administration/Crew` — módulo 01 |
| `cliente.sinsalidas` | Sin equivalente (BR-05-004) |
