# 02-bascula — 02 Flujos legacy reconstruidos

> AG-02 · 2026-10-23 · Estático. Rutas relativas a `code_workspace/bodegas-legacy/` salvo indicación. Los archivos PHP usan CRLF; las líneas citadas son las de `grep -n`.

## F-01 · Entrada con depósito (CF-L103.a, el flujo de los ~30 s)

1. **Abrir** «Nueva Entrada» → `modulos/mod_bascula/registrarentradabascula.php`. Al cargar, `onload` inicia el sondeo del peso (`evaluaPesa`, `:560-582`, cada 100 ms contra `consultapesa.php`) y pone el foco en «Capturar» (`:733`). En la operación real el peso **se digita** (DECISIONES_REVISION §2.E.17).
2. **Placa** (`:750-755`): autocompleta (`../mod_selecciones/seleccionarplaca.php`) y `consultaPlaca` (`:322-363`) carga el vehículo; si no existe, alerta y abre el registro de vehículo. En cadena:
   - `consultaConvenios` (`:407-437`) → convenio del vehículo y `consultaTarifas` (`:438-481`): tarifa vigente o, sin tarifa, campos «Valor a Cobrar» / «Valor de Iva» digitados (`:475-476`, `estarifa=0`, «cobro no tarifado» `:162-165`);
   - `consultarConductor` (`:365-378`) y `consultarEmpresaTransporte` (`:379-392`): último conductor y transportadora del vehículo en pesajes anteriores;
   - `cargaCliente` (`:482-…`): «Facturar a» = cliente del convenio o, si no hay, el conductor;
   - `otrosServicios` → `consultaotrosservicios.php`: casillas de servicios con `id_servicio > 1` y tarifa vigente (`:694-718`).
3. **Modalidad** (radio Importación/Exportación/Otra, `:789-799`) → `consultatipodocumento.php` preselecciona el documento comercial; **Nro. documento** autocompleta con `seleccionardocumercial.php` (ingresos no eliminados, sin fecha) y, al elegir, `consultaEntroPlaca` (`:393-406`) avisa «El vehiculo yá ingreso con el documento seleccionado» y limpia el documento; `consultasaldos.php` (`:660`) muestra Entrada/Ampara/Saldo.
4. **Pesos** (`:840-862`): P. Indicador (bruto, obligatorio), P. manifiesto (opcional, copia a P. mercancía), T. vehículo = bruto − mercancía, calculado en el navegador (`calculaTaras`, `:643-649`; RN-054).
5. **Mercancía**: una línea de texto libre en mayúsculas (máx. 200), embalaje (máx. 100) y cantidad (`:884-900`). El selector de unidad de carga está comentado (`:873-878`).
6. **«Insertar registro»** (`:906`) → POST:
   - si no hay `id_ingreso`, `INSERT INTO ingreso … 'incompleto'` (`:66-77`, `MAX()+1`);
   - `vehiculo_x_empresa` si falta la relación (`:80-101`);
   - `INSERT INTO pesaje` con pesos, manifiesto, conductor, tarifa y descripción (`:113-139`);
   - consecutivo de recibo `MAX(num_recibo)+1` del servicio 1 (`:145-148`);
   - recibo a cliente o a persona (conductor) (`:151-160`, `:177`), detalle del servicio 1 y de cada «otro servicio» marcado (`:180-194`);
   - redirige a `listarentradasbascula.php?facturar=1&id_recibo=…` (`:196`), que abre `facturar.php` en diálogo (`listarentradasbascula.php`, `facturaRecibo`).
7. **Cobro / tiquete** (`modulos/mod_bascula/facturar.php`): en importación preselecciona «entrada y tara» (`facturaImportacion`). Dos documentos posibles:
   - **Tiquete** (entrada, tara, entrada y tara): crea `factura` con número del rango de `resolucion_numeracion` vigente (`:356-371`, `:71-72`), su detalle (`:75`), marca el recibo `facturado` (`:78`) y agrega en $0 los pesajes agrupados (`:84-90`, RN-057). Efectivo y cambio están **comentados** en el tiquete (`:521-543`).
   - **Recibo**: guarda `pago`, `cambio` y `estado='cobrado'` (`:100`); en el recibo sí están «Efectivo» y «Cambio» con cálculo al teclear (`calculaCambio`, `:152-157`; campos `:794-799`).
   - «¿Desea Imprimir Ahora?» imprime y suma `factura.impresiones` (`:158-195`, `contarimpresiones.php`).
8. **Comercio Exterior** completa después en `modulos/mod_ingresos/modificaringreso.php` y, para la mercancía del tiquete, en `modulos/mod_bascula/modificarentrada.php` («Tickets Ingresos»).

**Efectos:** `ingreso` incompleto, `pesaje`, `recibo`/`detallerecibo`, `factura`/`detallefactura` si se emitió tiquete. **Sin transacción**; si el `INSERT` del pesaje falla se borra el ingreso nuevo (`:142-143`). **Errores:** `die(mysql_error())`.

## F-02 · Variantes de entrada (CF-L103.b, CF-L103.c)

- **`registrarentrada.php`** (Alt+N, `entrada.php:17-18`): mismo patrón, pero guarda la mercancía con producto del catálogo en `producto_en_bodega`, `productoamparado`, `productodetalle` y `productobodega_x_proceso` (`:141-209`), y vuelve a «Tickets Ingresos» (`:256`).
- **`registrarentradavariascp.php`** («Vehículo con varios Doc.»): un vehículo, varios documentos (`cantdetalle`); por cada uno crea/usa el `ingreso` y un `pesaje` con el **mismo peso bruto** y su peso de manifiesto; el primero queda `activo` y cobra, los demás `agrupado` con `pesaje_origen` (`:79-133`); recibos por documento (`:225-258`) y factura única al facturar el origen, con detalles en $0 (`facturar.php:84-90`). **Un solo pesaje físico** para todos los documentos.

## F-03 · Repesaje (CF-L114) y tiquete (CF-L115)

- «Repesar» está en cada fila del listado, siempre visible (`listarentradasbascula.php`, columna Repesa; el `else` que lo ocultaba está comentado). `repesarentrada.php:61-127` inserta un `pesaje` nuevo con `pesaje_origen` = el original, sin cobro; pueden existir varios («N Reps.», `verrepesa.php`).
- `vertiquete.php` reimprime; cada impresión incrementa `factura.impresiones` (`contarimpresiones.php`) y avisa «La factura se ha impreso en N ocasion(es)» (`facturar.php:185-195`).

## F-04 · Modificar (CF-L104, CF-L108, CF-L112)

- Visible solo si Comercio Exterior no asignó productos y el pesaje no está eliminado (`listarentradasbascula.php`, condición `!$asignadoproductos && estado!='eliminado'`).
- `modificarentradabascula.php` reescribe documento e importador del ingreso (`:101`), todos los campos del pesaje —manifiesto, conductor, transportadora, pesos, tarifa, producto, embalaje, cantidad, fecha— (`:120`) y los valores del recibo (`:264-266`). Salida y solo pesaje igual (`modificarsalida.php:99-173`, `modificarsolopeso.php:94-166`). Sin motivo ni auditoría propia (la tabla registra usuario/IP/fecha del último cambio).

## F-05 · Anular (CF-L105, CF-L109, CF-L113, RN-058)

- Formulario con `observacion_estado` (motivo) → `eliminarentrada.php:61-119`: pesaje `eliminado` con motivo, usuario, IP y fecha; `producto_en_bodega` eliminado; `productoamparado` eliminado si el producto no está en otro pesaje activo del ingreso; recibo y detalle eliminados. **Sin guardas** (no revisa levantes, salidas ni reservas) y **no anula la `factura`** del tiquete.
- `eliminarsalida.php:61-88`: además `salida` eliminada; no devuelve mercancía. `eliminarsolopeso.php:61-87`: pesaje y recibo.
- RN-074: los listados ocultan los eliminados a usuarios de nivel > 1 (`listarsalidas.php:4-14,74-91`; `reporteingresos.php:106-120`).

## F-06 · Salida (CF-L107), duplicar recibo (CF-L119) y usar tiquete (CF-L120)

- `registrarsalida.php`: placa, conductor, transportadora, modalidad, peso del vehículo; crea `salida` «incompleto» **sin orden de cargue** (`:104-105`), `pesaje` (`:139`), recibo y otros servicios; Comercio Exterior completa la salida en `mod_salidas`.
- `duplicarrecibo.php:58-138` (botón «Usar» del listado de salidas, `listarsalidas.php:435`): N (1–10) salidas «incompleto» con modalidad fija 4, copia los pesos del pesaje, recibo en $0 y detalle en $0 en la factura de origen.
- `usartiquete.php:56-114` (`salidas:registrar`): elige un tiquete de ingreso, crea la salida con importador y SIA del ingreso, vincula el mismo pesaje (`UPDATE pesaje SET id_salida`) y crea `producto_salida` con lo nacionalizado y su saldo anterior. Redirige a Salidas.

## F-07 · Facturación posterior (CF-L117, CF-L118)

- `reporteingresos.php:514`: si el tiquete no tiene N.º SIIGO, ícono que abre `factusiigoticket.php` → `UPDATE factura SET fact_siigo` (`:61-66`).
- «Cobros Pendientes» (`cobrarcartera.php:60-71`): facturas de báscula con total > 0 y `pago = 0`; el botón llama por AJAX a `registracobrocartera.php:9`, que pone `pago = total_factura` (sin sesión ni permiso).

## F-08 · Reportes (CF-L121)

- `reporteingresos.php`: filtros fecha, cliente/importador (por modalidad < 4 vía `ingreso.id_importador`, ≥ 4 vía `salida.id_cliente`), transportadora, placa+país, modalidad, «en ceros» (`total_factura=0`), «por cobrar» (`total>0 AND pago=0`), «no impresos» (`impresiones=0`) (`:44-90`); columnas tiquete, Fact. Siigo, fecha, modalidad, vehículo, conductor, pesos, repesa, # impresiones, pago, cambio, subtotal y totales.
- `reportecpi.php`: por documento (CPI/Factura/Remesa) — fecha, N.º tiquete, placa, cantidad y peso de manifiesto, con totales (`:247-356`) y salida a Excel, PDF o impresión.

## Incertidumbres

- No se sabe qué variantes se usaban en producción (el catálogo es del checkout, no de uso). El menú apunta a `registrarentradabascula.php`; Alt+N a `registrarentrada.php`.
- Qué servicios eran los «otros servicios» (`servicio.id_servicio > 1` con tarifa vigente) depende de datos de `db_legacy/`, que no se abrió.
- La frecuencia de «Vehículo con varios Doc.» y de los repesajes múltiples no se puede medir estáticamente.
