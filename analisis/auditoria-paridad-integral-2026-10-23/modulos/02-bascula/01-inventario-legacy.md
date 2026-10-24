# 02-bascula — 01 Inventario legacy

> AG-02 · 2026-10-23 · Auditoría estática. Rutas relativas a `code_workspace/`. Sin Git, sin ejecución.
> Fuente del universo: `01-inventario-funcional-global.md` §6 «02-bascula» (CF-L102…121, CF-L235, CF-L255) contrastado con `bodegas-legacy/modulos/mod_bascula/` (42 archivos `.php` + `index.html` + `_notes/`, 18 687 líneas medidas con `wc -l`), `bodegas-legacy/peso.php`, `bodegas-legacy/consultapesa.php`, `bodegas-legacy/entrada.php`, `bodegas-legacy/menus/menuizquierda.php:193-208` y `bodegas-legacy/reportes/bascula/` (solo salidas generadas, ver §4).

## 1. Puntos de entrada

| Entrada | Destino | Evidencia |
| --- | --- | --- |
| Menú «Báscula › Entradas» | `listarentradasbascula.php` | `bodegas-legacy/menus/menuizquierda.php:195` |
| «Nueva Entrada» | `registrarentradabascula.php` | `menuizquierda.php:196` |
| «Salidas» / «Nueva Salida» | `listarsalidas.php` / `registrarsalida.php` | `menuizquierda.php:197-198` |
| «Solo Pesaje» | `listarsolopesajes.php` | `menuizquierda.php:199` |
| «Reportes» | `inicioreportes.php` (→ `reportecpi.php`, `reporteingresos.php`) | `menuizquierda.php:200`; `inicioreportes.php:94,100` |
| «Cobros Pendientes» | `cobrarcartera.php` | `menuizquierda.php:201` |
| Comercio Exterior › «Tickets Ingresos» | `listarentradas.php` | `menuizquierda.php:208` |
| Atajos Alt+N / Alt+K | `registrarentrada.php` / `registrarsalida.php` | `bodegas-legacy/entrada.php:17-21`; `inicial.php:92,98` |
| «Vehículo con varios Doc.» | `registrarentradavariascp.php` | `listarentradasbascula.php` (bloque HTML, botón `nvoentrada2`, línea 323 del archivo) |

## 2. Permisos (`verificapermisos.php::evaluaPermiso(modulo, accion)`, tabla `permisos` × `modulo`)

`bodegas-legacy/verificapermisos.php:31-44` consulta `permisos` por usuario, módulo y acción (RN-004). Pares observados (los archivos tienen fin de línea CRLF):

| Acción | Scripts |
| --- | --- |
| `bascula:consultar` | `listarentradasbascula.php:6-7`, `listarentradas.php:6-7`, `listarsalidas.php:6-7`, `listarsolopesajes.php:6-7`, `inicioreportes.php:39-40`, `reporteingresos.php:8-9`, `reportecpi.php:39-40`, `cobrarcartera.php:8-9`, `factusiigoticket.php:8-9` |
| `bascula:registrar` | `registrarentradabascula.php:8-9`, `registrarentrada.php:8-9`, `registrarentradavariascp.php:8-9`, `registrarsalida.php:39-40`, `registrarsolopeso.php:8-9`, `repesarsalida.php:8-9`, `facturar.php:7-8`, `facturar1.php:7-8`, `duplicarrecibo.php:7-8`, `vertiquete.php:7-8`, `verrepesa.php:7-8` |
| `bascula:editar` | `modificarentrada.php:39-40`, `modificarentradabascula.php:39-40`, `modificarsalida.php:39-40`, `modificarsolopeso.php:39-40`, `repesarentrada.php:8-9`, `repesarsolopeso.php:8-9` |
| `bascula:eliminar` | `eliminarentrada.php:8-9`, `eliminarsalida.php:8-9`, `eliminarsolopeso.php:8-9` |
| `salidas:registrar` | `usartiquete.php:8-9`; botón «Usar Tiquete» condicionado en `registrarsalida.php:935-939` |
| Sin control de permiso | Selectores AJAX (`consulta*.php`, `seleccionardocumercial.php`, `contarimpresiones.php`) y **`registracobrocartera.php`** (marca facturas como pagadas sin `aut_verifica` ni `evaluaPermiso`, archivo completo de 17 líneas) |

## 3. Capacidades

| ID | Capacidad | Pantalla / script principal | Scripts auxiliares | Tablas (L = lectura, E = escritura) | Permiso |
| --- | --- | --- | --- | --- | --- |
| CF-L102 | Consultar y filtrar entradas | `listarentradasbascula.php` (filtros fecha, tiquete, placa: `:59-71`; acciones por fila: repesar, ver repesas, crear/imprimir tiquete, editar si CE no asignó productos, eliminar si no está eliminado) | `listarentradas.php` (versión de Comercio Exterior) | L: `pesaje`, `vehiculo`, `vehiculo_x_empresa`, `persona`, `recibo`, `detallerecibo`, `ingreso`, `documentocomercial`, `producto_en_bodega`, `factura`, `detallefactura` | `bascula:consultar` |
| CF-L103 | Registrar entrada y pesaje | `registrarentradabascula.php` (formulario único, «Insertar registro» `:906`) | `registrarentrada.php` (variante Alt+N con productos del catálogo y redirección a «Tickets Ingresos»), `registrarentradavariascp.php` (un vehículo con varios documentos, pesajes «agrupados») | E: `ingreso` (estado `incompleto`, `:76`), `vehiculo_x_empresa`, `pesaje` (`:113`), `recibo` (`:177`), `detallerecibo`; en las variantes también `producto_en_bodega`, `productoamparado`, `productodetalle`, `productobodega_x_proceso` | `bascula:registrar` |
| CF-L104 | Modificar entrada y pesaje | `modificarentradabascula.php` (`UPDATE ingreso` `:101`, `UPDATE pesaje` `:120`, reemplazo de `producto_en_bodega` `:159-195`, `UPDATE recibo` `:264-266`) | `modificarentrada.php` (Comercio Exterior completa mercancía, listas de empaque e importador: `:115-325`) | E: `ingreso`, `pesaje`, `producto_en_bodega`, `productodetalle`, `productoamparado`, `recibo`, `detallerecibo`, `listasdeempaque` | `bascula:editar` |
| CF-L105 | Anular entrada | `eliminarentrada.php:61-119` | — | E: `pesaje.estado='eliminado'` + motivo/usuario/IP/fecha en `observacion_estado`, `producto_en_bodega`, `productoamparado` (condicional), `recibo`, `detallerecibo` | `bascula:eliminar` |
| CF-L106 | Consultar y filtrar salidas | `listarsalidas.php` (botón «Usar» → duplicar recibo `:435`; repesas `:417`) | — | L: `salida`, `pesaje`, `producto_en_bodega`, `recibo` | `bascula:consultar` (RN-074: niveles >1 no ven eliminados) |
| CF-L107 | Registrar salida | `registrarsalida.php:69-221` (crea `salida` «incompleto» sin orden previa `:104-105`) | botón «Usar Tiquete» `:935-939` | E: `salida`, `vehiculo_x_empresa`, `pesaje`, `recibo`, `detallerecibo` | `bascula:registrar` |
| CF-L108 | Modificar salida | `modificarsalida.php:99-173` | — | E: `salida`, `pesaje`, `recibo`, `detallerecibo` | `bascula:editar` |
| CF-L109 | Anular salida | `eliminarsalida.php:61-88` (pesaje, recibo y `salida` eliminados; no devuelve mercancía) | — | E: `pesaje`, `recibo`, `detallerecibo`, `salida` | `bascula:eliminar` |
| CF-L110 | Consultar solo pesajes | `listarsolopesajes.php` | — | L: `pesaje`, `vehiculo`, `detallefactura` | `bascula:consultar` |
| CF-L111 | Registrar solo pesaje | `registrarsolopeso.php` (cliente opcional: sin cliente se factura al conductor `:117-125`) | — | E: `vehiculo_x_empresa`, `pesaje`, `recibo`, `detallerecibo` | `bascula:registrar` |
| CF-L112 | Modificar solo pesaje | `modificarsolopeso.php:94-166` | — | E: `pesaje`, `recibo`, `detallerecibo` | `bascula:editar` |
| CF-L113 | Anular solo pesaje | `eliminarsolopeso.php:61-87` | — | E: `pesaje`, `recibo`, `detallerecibo` | `bascula:eliminar` |
| CF-L114 | Registrar repesaje | `repesarentrada.php:61-127` (inserta un `pesaje` nuevo con `pesaje_origen`, sin cobro) | `repesarsalida.php`, `repesarsolopeso.php`; botón «Repesar» siempre visible (`listarentradasbascula.php`, fila, `repesarentrada.php?id=`) | E: `pesaje` | `bascula:editar` / `bascula:registrar` (salida) |
| CF-L115 | Ver tiquete y repesaje | `vertiquete.php` | `verrepesa.php`, `contarimpresiones.php` | L: `recibo`, `pesaje`, `factura`; E: `factura.impresiones` | `bascula:registrar` |
| CF-L116 | Facturar servicios de báscula | `facturar.php` (elige «Tiquete» de entrada / tara / entrada y tara, o «Recibo»; tiquete = `factura` con `resolucion_numeracion` `:356-371`, `:71-90`; recibo = `UPDATE recibo SET pago, cambio, estado='cobrado'` `:100`; agrupados en $0 `:84-90`) | `facturar1.php` (variante anterior, sin llamadores encontrados), `consultaotrosservicios.php` (servicios adicionales con tarifa vigente), `consultartarifasvehiculo.php`, `consultarconveniosvehiculo.php` | E: `factura`, `detallefactura`, `recibo` | `bascula:registrar` |
| CF-L117 | Registrar N.º SIIGO del tiquete | `factusiigoticket.php:61-66` (`UPDATE factura SET fact_siigo`), abierto desde `reporteingresos.php:514` | — | E: `factura.fact_siigo` | `bascula:consultar` |
| CF-L118 | Cobrar cartera pendiente | `cobrarcartera.php:60-71` (facturas con `total_factura>0` y `pago=0`) | `registracobrocartera.php:9` (`UPDATE … SET F.pago=F.total_factura`) | L: `pesaje`, `factura`, `detallefactura`; E: `factura.pago` | `bascula:consultar` (el script de escritura no valida sesión) |
| CF-L119 | Duplicar recibo | `duplicarrecibo.php:58-138` (N salidas «incompleto» con modalidad fija 4, copia pesos, recibos y detalle de factura en $0; tope 10 `:287`) | — | E: `salida`, `vehiculo_x_empresa`, `pesaje`, `recibo`, `detallerecibo`, `detallefactura` | `bascula:registrar` |
| CF-L120 | Usar tiquete existente | `usartiquete.php:56-114` (salida con importador y SIA del ingreso, `UPDATE pesaje SET id_salida`, `producto_salida` con lo nacionalizado) | `vertiquete.php` en marco | E: `salida`, `pesaje`, `producto_salida` | `salidas:registrar` |
| CF-L121 | Reportes de báscula | `inicioreportes.php` → `reporteingresos.php` (filtros cliente, transportadora, placa, modalidad, en ceros, por cobrar, no impresos `:44-90`) y `reportecpi.php` (tiquetes de un documento: fecha, tiquete, placa, cantidad, peso manifiesto y totales `:247-356`; Excel, PDF e impresión) | `reportes/reporteexcel.php`, `reportes/crearpdf.php` | L: `pesaje`, `factura`, `modalidad`, `ingreso` | `bascula:consultar` |
| CF-L235 | Selectores y consultas auxiliares | `consultaentroplaca.php` (vehículo ya ingresó con el documento), `consultarconductor.php` y `consultarempresatransporte.php` (último conductor/transportadora del vehículo), `consultarconveniosvehiculo.php`, `consultartarifasvehiculo.php`, `consultaotrosservicios.php`, `consultasaldos.php` (Entrada/Ampara/Saldo del documento), `seleccionardocumercial.php` (autocompletar documento, excluye eliminados), `consultatipodocumento.php` (tipo por modalidad), `contarimpresiones.php`, `mod_bascula/consultapesa.php` | `../mod_selecciones/seleccionarplaca.php`, `../mod_vehiculos/consultarplaca.php` (fuera del módulo) | L: `pesaje`, `tarifa`, `servicio`, `ingreso`, `productoamparado`, `producto_en_bodega`, `docmercial_x_modalidad`; E: `factura.impresiones` | sin control |
| CF-L255 | Consultar último peso | `peso.php:8-32` (sondeo cada 100 ms) | `consultapesa.php:9` (`SELECT * FROM peso ORDER BY id_peso DESC LIMIT 1`); el formulario de entrada también sondea (`registrarentradabascula.php:560-582`, botón «Capturar» `:741-742`) | L: `peso` | sin control |
| **CF-LX02-01** | Atajos de teclado de báscula (no catalogado) | `bodegas-legacy/entrada.php:14-30` (Alt+N → `registrarentrada.php`, Alt+K → `registrarsalida.php`) | `inicial.php:92,98` (`accesskey`) | — | sesión |

## 4. Observaciones del inventario

- **No catalogado:** solo CF-LX02-01. Las variantes `registrarentrada.php` y `registrarentradavariascp.php` ya están dentro de CF-L103 (+2); se desglosan en la matriz como CF-L103.b y CF-L103.c.
- **`facturar1.php`** es una versión anterior de `facturar.php` (difieren en la validación de efectivo y en el rótulo «FACTURA» con resolución, `diff` de las líneas 161-242). No se encontró quién la llame (búsqueda de `facturar1.php` en `bodegas-legacy/**/*.php`).
- **`reportes/bascula/`** contiene 44 archivos `informe_uN.html/pdf` y `reporte_uN.html/pdf` generados por usuario: son salidas de `reporteexcel.php`/`crearpdf.php`, no código. **No se abrieron** (pueden contener datos de personas).
- **Tiquete = factura POS:** el «Tiquete No. T{n}» es el `num_factura` tomado del rango de `resolucion_numeracion` vigente (`facturar.php:356-371`), con efectivo y cambio comentados en el tiquete (`facturar.php:521-543`) y activos en el recibo (`:794-799`).
- **Consecutivos con `MAX()+1`** sin transacción (`registrarentradabascula.php:68,106,145`), propensos a colisiones; no se replican en V2 (DEC-012).
- **`registracobrocartera.php`** escribe sin autenticación ni permiso (riesgo de seguridad legacy; no se replica).
