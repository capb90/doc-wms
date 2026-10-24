# 06-facturacion — 04 Trazabilidad legacy

> AG-06 · 2026-10-23 · Estático. **Prefijos:** `L/` = `bodegas-legacy/`. L = lectura, E = escritura.

| Capacidad | Ruta (menú / llamada) | Script | Tablas y campos |
| --- | --- | --- | --- |
| CF-L017 | Administrar Datos → Convenios | `L/modulos/mod_convenios/listarconvenios.php` | L `convenio` (`id_convenio`, `desc_convenio`, `fecha_inicio`, `fecha_fin`, `id_cliente`, `estado`); L `cliente`, `tipodocumento`, `ciudad`, `pais`; L `vehiculo_x_convenio`, `vehiculo`, `marcavehiculo`, `tipocarroceria` |
| CF-L018 | «Nuevo convenio» | `registrarconvenio.php` (+ `L/modulos/mod_clientes/listarclientes.php?dialog=1`) | E `convenio` (`id_cliente`, `desc_convenio`, `fecha_inicio`, `fecha_fin`, `id_usuarioregistra`, `ip_registra`, `fechahora_registra`) |
| CF-L019 | Editar desde el listado | `modificarconvenio.php` | E `convenio` (mismos campos) |
| CF-L020 | Eliminar desde el listado | `eliminarconvenio.php` | E `convenio.estado` (baja lógica) |
| CF-L065 | Administrar Datos → Tarifas | `L/modulos/mod_tarifas/listartarifas.php` | L `tarifa` (`nom_tarifa`, `id_servicio`, `id_convenio`, `fecha_inicio`, `fecha_fin`, `precio`, `iva`, `precio+iva`, `estado`), `servicio`, `convenio` |
| CF-L066 | «Nueva Tarifa» | `registrartarifa.php` (+ `mod_convenios/listarconvenios.php?dialog=1`) | L `servicio`; E `tarifa` |
| CF-L067 | Editar | `modificartarifa.php` | E `tarifa` |
| CF-L068 | Eliminar | `eliminartarifa.php` | E `tarifa` (DELETE físico) |
| CF-L069 | Administrar Datos → Tasas de Cambio | `L/modulos/mod_tasascambio/listartasascambio.php` | L `tasa_cambio` (`fecha_inicio`, `fecha_fin`, `id_pais`, `valor`, `estado`), `vista_monedas` |
| CF-L070 | «Nueva Tasa de Cambio» | `registrartasacambio.php` → AJAX `consultatasacambio.php` | E `tasa_cambio` |
| CF-L071 | Editar | `modificartasacambio.php` | E `tasa_cambio` |
| CF-L072 | Eliminar | `eliminartasacambio.php` | E `tasa_cambio.estado` |
| CF-L201 | Facturación → Depósitos x Facturar (`?anio=`) | `L/modulos/mod_facturacion/listardepositosfacturar.php` | L `ingreso` (`estado`, `id_importador`, `fechahora_ingreso`, `id_sia`, `id_empresatransporte`, `nro_manifiestodian`, `nro_manifiestoemp`, `preciomercancia`, `observaciones`), `documentocomercial`, `vista_kardexdepositos2` (`saldo`, `estado`), `cliente.dias_facturacion`, `sia`, `empresa_transporte`, `productoamparado`, `producto_en_bodega`, `producto_levante`, `levante` (`tasa_cambio`, `fob_dolares`, `fob_pesos`, `peso_bruto`), `producto_salida`, `salida`, `pesaje`, `tasa_cambio`; E `facturaciigo` (DELETE de no facturados, INSERT), `deposito.estado` |
| CF-L202 | Botón «Facturar» del período | `facturarciigo.php?id=` | L `facturaciigo`, `vista_kardexdepositos`, `sia`, `cliente`, `producto_en_bodega`, `producto_levante`, `producto_salida`, `salida`; E `facturaciigo` (`nro_facturaciigo`, `fecha_facturaciigo`, `fechalimite_periodo`, `cliente_facturaciigo`, `valor_facturaciigo`, `detallefactura`, `observaciones`, `estado='facturada'`, usuario, IP, fecha) |
| CF-L203 | Facturación → Facturas Emitidas (`?filtro=&palabrabuscar=`) | `listarfacturas.php` | L `facturaciigo` (con número), `deposito`, `ingreso.nro_doccomercial` |
| CF-L204 | Editar factura | `modificarfactura.php?id=` | E `facturaciigo` (`nro`, `fecha`, `fechalimite`, `detallefactura`, `observaciones`, `estado`) |
| CF-L205 | Eliminar factura | `eliminarfactura.php?id=` | E `facturaciigo` (vacía `nro`, `fecha`, `detallefactura`, `observaciones`; `estado='activo'`) |
| CF-L206 | Facturación → Informe de Facturación (`anio`, `mes`) | `informefacturacion.php` → `reportes/reporteexcel.php`, `reportes/crearpdf.php` | L `facturaciigo` (`fecha_facturaciigo`, `nro`, `valor`, `estado='facturada'`); E archivo `reportes/general/informe_u{usuario}` |
| CF-L207 | Facturación → Informe por CPI | `informecpi.php` → AJAX `seleccionardeposito.php`; exportes | L `deposito`, `ingreso`, `documentocomercial`, `empresa_transporte`, `sia`, `tipodocumento`, `cliente`, `ciudad`, `cuadrilla`, `producto_en_bodega`, `producto_salida`, `productodetalle`, `pesaje`, `detallefactura`, `factura`, `vehiculo_x_empresa`, `vehiculo`, `facturaciigo`, `tasa_cambio`; E archivo `reportes/facturacion/informe_u{usuario}` |
| CF-L234 | Programado (sin crontab en el repositorio) | `L/cron.php` | Igual que CF-L201 (sin HTML); E `facturaciigo`, `deposito.estado` |
| CF-L249 | AJAX desde CF-L070 | `L/modulos/mod_tasascambio/consultatasacambio.php` | L `tasa_cambio` (`id_pais`, `fecha_inicio`, `fecha_fin`) |
| CF-L251 | AJAX desde CF-L207 y `mod_salidas`, `mod_depositos` | `L/modulos/mod_facturacion/seleccionardeposito.php` | L `deposito` (`nro_deposito`, `estado`), `ingreso.nro_doccomercial`, `cliente.nom_cliente` |
| CF-LX06-01 | Carga de `inicial.php` y del menú | `L/menus/evaluatasacambio.php` | L `tasa_cambio` (vigente hoy) |
