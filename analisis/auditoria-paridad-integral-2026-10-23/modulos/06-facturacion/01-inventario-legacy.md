# 06-facturacion — 01 Inventario legacy

> AG-06 · 2026-10-23 · Auditoría estática (sin ejecución, sin Git). Referencia de código según `docs/contexto/estado.md`: BE `35a61b2` / FE `c924a8b`; se auditó lo que había en disco ese día.
> **Prefijos de ruta:** `L/` = `bodegas-legacy/`; `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`. Todas las rutas son relativas a `code_workspace/`.
> Los `include` de `Connections/` se citan sin abrir (restricción §2.4).

## 1. Qué es la facturación en el legacy

El legacy **no calcula el valor del almacenamiento**. Genera períodos por depósito (tabla `facturaciigo`) según los días de facturación del cliente (`cliente.dias_facturacion`) y Facturación registra, por cada período, la factura que emitió **fuera del sistema, en SIIGO** («CIIGO» en el código): número, fecha, cliente, **valor digitado**, observaciones y fecha límite (`L/modulos/mod_facturacion/facturarciigo.php:87-96`, `:288-292`). Las tarifas y los convenios del legacy solo valorizan **servicios de báscula y otros servicios** del recibo (`L/modulos/mod_bascula/consultartarifasvehiculo.php:10-17`, `consultaotrosservicios.php:7-14`); no hay tarifa de almacenamiento. La TRM vive en un catálogo semanal manual (`tasa_cambio`) que solo sirve para mostrar el valor de la mercancía en pesos.

## 2. Capacidades

| ID | Capacidad | Pantalla / script | Tablas (L=lee, E=escribe) | Permiso (`verificapermisos.php`, tabla `permisos`) | Menú |
| --- | --- | --- | --- | --- | --- |
| CF-L017 | Consultar convenios | `L/modulos/mod_convenios/listarconvenios.php:48` (no eliminados), `:163-219` (cliente y vehículos asignados, botón «Asignar») | L `convenio`, `cliente`, `vehiculo_x_convenio`, `vehiculo`, `marcavehiculo`, `tipocarroceria` | `convenios:consultar` (`:6-7`) | Administrar Datos → Convenios (`L/menus/menuizquierda.php:272`) |
| CF-L018 | Registrar convenio | `L/modulos/mod_convenios/registrarconvenio.php:57` (INSERT cliente, descripción, fecha inicio, fecha fin), `:166-184` (cliente por diálogo, fechas con calendario) | E `convenio` | `convenios:registrar` (`:8-9`) | — |
| CF-L019 | Modificar convenio | `L/modulos/mod_convenios/modificarconvenio.php:57` | E `convenio` | `convenios:editar` | — |
| CF-L020 | Eliminar convenio | `L/modulos/mod_convenios/eliminarconvenio.php:62` (baja lógica `estado`) | E `convenio` | `convenios:eliminar` | — |
| CF-L065 | Consultar tarifas | `L/modulos/mod_tarifas/listartarifas.php:48-51` (tarifa + servicio + convenio, no eliminadas); columnas tarifa, servicio, precio, IVA, precio+IVA, convenio, vigencia (`:98-106`) | L `tarifa`, `servicio`, `convenio` | `tarifas:consultar` | Administrar Datos → Tarifas (`menuizquierda.php:273`) |
| CF-L066 | Registrar tarifa | `L/modulos/mod_tarifas/registrartarifa.php:57` (INSERT nombre, servicio, convenio o 0, vigencia, precio, IVA en valor, precio+IVA); IVA digitado en % (`:261`) | E `tarifa` | `tarifas:registrar` | — |
| CF-L067 | Modificar tarifa | `L/modulos/mod_tarifas/modificartarifa.php:88`, `:294` (IVA mostrado como % = iva/precio×100) | E `tarifa` | `tarifas:editar` | — |
| CF-L068 | Eliminar tarifa | `L/modulos/mod_tarifas/eliminartarifa.php:58` (**DELETE físico**, aunque el listado filtra `estado<>'eliminado'`) | E `tarifa` | `tarifas:eliminar` | — |
| CF-L069 | Consultar tasas de cambio | `L/modulos/mod_tasascambio/listartasascambio.php:50` (moneda por país, vigencia, valor) | L `tasa_cambio`, `vista_monedas` | `tasascambio:consultar` | Administrar Datos → Tasas de Cambio (`menuizquierda.php:274`) |
| CF-L070 | Registrar tasa de cambio | `L/modulos/mod_tasascambio/registrartasacambio.php:55`; semana por defecto lunes–domingo (`:173-179`); duplicado solo avisado en JavaScript (`:128-129`) | E `tasa_cambio` | `tasascambio:registrar` | — |
| CF-L071 | Modificar tasa de cambio | `L/modulos/mod_tasascambio/modificartasacambio.php:56` | E `tasa_cambio` | `tasascambio:editar` | — |
| CF-L072 | Eliminar tasa de cambio | `L/modulos/mod_tasascambio/eliminartasacambio.php:56` (baja lógica) | E `tasa_cambio` | `tasascambio:eliminar` | — |
| CF-L201 | Depósitos por facturar | `L/modulos/mod_facturacion/listardepositosfacturar.php` (filtro por año `:97-114`, `:280-294`; **regenera los períodos en cada carga** `:321-433`; tabla de períodos con botón «Facturar» `:445-471`; detalle documental, TRM de ingreso y valor US/CO `:504-530`; resumen ingresos/levantes con CIF/despachos/existencias `:560-865`) | L `ingreso`, `documentocomercial`, `vista_kardexdepositos2`, `cliente`, `sia`, `empresa_transporte`, `producto_en_bodega`, `producto_levante`, `levante`, `producto_salida`, `salida`, `pesaje`, `tasa_cambio`; E `facturaciigo` (DELETE + INSERT), `deposito.estado` | `facturacion:consultar` (`:39-47`) | Facturación → Depósitos x Facturar (`menuizquierda.php:259`) |
| CF-L202 | Facturar período en «CIIGO» (SIIGO) | `L/modulos/mod_facturacion/facturarciigo.php` (detalle con saldo por producto al inicio del período `:119-150`, CPI, depósito, período e intermediario `:250-252`; N.º sugerido = MAX+1 `:262-271`; fecha, cliente, valor, observaciones y fecha límite editables `:274-302`; UPDATE a `facturada` `:87-96`) | L `facturaciigo`, `vista_kardexdepositos`, `sia`, `cliente`, `producto_en_bodega`, `producto_levante`, `producto_salida`, `salida`; E `facturaciigo` | `facturacion:registrar` (`:39-47`) | Diálogo desde CF-L201 |
| CF-L203 | Facturas emitidas | `L/modulos/mod_facturacion/listarfacturas.php:60-85` (solo con número; filtros CPI, fecha, depósito, N.º, cliente), `:216-241` (columnas N.º, fecha, límite, detalle, facturado a, valor, observaciones; editar y eliminar) | L `facturaciigo`, `deposito`, `ingreso` | `facturacion:consultar` | Facturación → Facturas Emitidas (`menuizquierda.php:261`) |
| CF-L204 | Modificar factura | `L/modulos/mod_facturacion/modificarfactura.php:57-75` (N.º, fecha, fecha límite, detalle, observaciones; **no** el valor ni el cliente) | E `facturaciigo` | `facturacion:editar` | Desde CF-L203 |
| CF-L205 | Anular factura | `L/modulos/mod_facturacion/eliminarfactura.php:56-65` (vacía N.º, fecha, detalle y observaciones y vuelve a `activo`; el período queda por facturar otra vez) | E `facturaciigo` | `facturacion:eliminar` | Desde CF-L203 |
| CF-L206 | Informe de facturación | `L/modulos/mod_facturacion/informefacturacion.php:92-96` (año → mes: cantidad y total `ROUND(SUM)` de facturadas), `:379-384` (mes → día), `:320-322` y `:392-394` (Excel, PDF, imprimir) | L `facturaciigo` | `facturacion:consultar` (`:39-40`) | Facturación → Informe de Facturación (`menuizquierda.php:262`) |
| CF-L207 | Informe por CPI | `L/modulos/mod_facturacion/informecpi.php:32-44` (autocompletar con `seleccionardeposito.php`), `:84-95` (encabezado del depósito), `:111` (TRM de ingreso), `:150-315` (ingresos, despachos con placa y tiquete, existencias), `:321-362` (facturas con número y total), `:104-106` (Excel, PDF, imprimir) | L `deposito`, `ingreso`, `documentocomercial`, `empresa_transporte`, `sia`, `cliente`, `cuadrilla`, `ciudad`, `producto_en_bodega`, `producto_salida`, `pesaje`, `detallefactura`, `factura`, `vehiculo`, `facturaciigo`, `tasa_cambio` | `facturacion:consultar` (`:8-9`) | Facturación → Informe por CPI (`menuizquierda.php:260`) |
| CF-L234 | Recalcular períodos (cron) | `L/cron.php:3-133` (mismo algoritmo de períodos que CF-L201), `:153-343` (reactiva `deposito.estado='activo'` si hay existencias), `:349-350` (reactiva depósitos `facturado` sin períodos desde 2019) | L `ingreso`, `documentocomercial`, `vista_kardexdepositos2`, `cliente`, `producto_salida`, `producto_en_bodega`, `salida`, `levante`, `producto_levante`, `pesaje`; E `facturaciigo`, `deposito` | Ninguno (script sin `aut_verifica`) | — (no hay crontab en el repositorio) |
| CF-L249 | Consulta de tasa de cambio (AJAX) | `L/modulos/mod_tasascambio/consultatasacambio.php:4-25` (¿existe ya una tasa para ese país y esa semana?) | L `tasa_cambio` | Sin control de sesión | Lo usa CF-L070 |
| CF-L251 | Selector de depósito (AJAX) | `L/modulos/mod_facturacion/seleccionardeposito.php:4-25` (por N.º de depósito **o CPI**, `LIKE`, 10 resultados, no eliminados) | L `deposito`, `ingreso`, `cliente` | Sin control de sesión | Lo usan `informecpi.php:32`, `mod_salidas/*` (8 pantallas) y `mod_depositos/adhesivos*.php` |
| **CF-LX06-01** (no catalogada) | Alerta «La tasa de cambio está desactualizada» | `L/menus/evaluatasacambio.php:4-11` (¿hay una tasa vigente hoy?); `L/inicial.php:37-53` (panel de inicio); `L/menus/menuizquierda.php:149-167` (menú, se repite cada segundo `:166`); clic → lista de tasas | L `tasa_cambio` | Sin control de sesión | Panel y menú |

## 3. No catalogadas y descartadas

| Elemento | Qué es | Tratamiento |
| --- | --- | --- |
| `L/modulos/mod_facturacion/listardepositosfacturar_nuevo.php` | Variante 2020 del listado (consulta con `LEFT JOIN facturaciigo`, `:94-106`) | No está en el menú (`menuizquierda.php:259` enlaza la versión sin `_nuevo`). Se documenta como variante, sin fila propia |
| Consulta `$consultainformes` (`listardepositosfacturar.php:82-86`) | SELECT de facturas 2021 que no se usa | Código muerto |
| `L/modulos/mod_convenios/vehiculosasignados.php`, `asignarvehiculo.php`, `desasignarvehiculo.php` | Vehículos del convenio | Es **CF-L100** (módulo 01); se cita como contexto de CF-L017…020 |
| `L/modulos/mod_servicios/*` | Catálogo de servicios | Son **CF-L057…060** (módulo 01). Las tarifas por servicio (CF-L065…068) sí son de este módulo |
| Cobros de báscula (`L/modulos/mod_bascula/facturar.php`, `consultartarifasvehiculo.php`, `consultarconveniosvehiculo.php`, `consultaotrosservicios.php`) | Consumo de tarifas y convenios | Módulo 02 (CF-L116…118). Se citan como uso de las tarifas |
| `inicial.php` | Además de la TRM, solo muestra la alerta de abandono (`:57-60`) | El abandono es del módulo 04; la TRM es CF-LX06-01 |

## 4. Modelo de datos legacy (lo que el módulo usa)

- `facturaciigo` (`L/bodegas_schema.sql`, `CREATE TABLE facturaciigo`): `id_deposito`, `nro_facturaciigo` (int, nulo hasta facturar), `fecha_facturaciigo`, `fechainicio_periodo`, `fechafin_periodo`, `fechalimite_periodo`, `cliente_facturaciigo` (texto), `valor_facturaciigo` (double), `detallefactura` (texto), `observaciones`, `estado` (`activo` = por facturar, `facturada`).
- `cliente.dias_facturacion` int(3) por defecto **15** (`L/bodegas_schema.sql:186`); opciones 15/30/90/180/360 (`L/modulos/mod_clientes/registrarcliente.php:466-474`).
- `tarifa`: `nom_tarifa`, `id_servicio`, `id_convenio` (0 = general), `fecha_inicio`/`fecha_fin`, `precio`, `iva` (valor), `precio+iva`, `estado`.
- `convenio`: `id_cliente`, `desc_convenio`, `fecha_inicio`/`fecha_fin`, `estado`. Vehículos en `vehiculo_x_convenio`.
- `tasa_cambio`: `fecha_inicio`/`fecha_fin` (semana), `id_pais` (moneda), `valor`, `estado`.
- Función de días: `dias_transcurridos = floor(|Δ|/86400)` (`L/includes/funciones.php:234-239`).

## 5. Permisos

El legacy controla por módulo y acción (`facturacion`, `convenios`, `tarifas`, `tasascambio` × `consultar/registrar/editar/eliminar`) con `evaluaPermiso` (`L/verificapermisos.php`; p. ej. `facturarciigo.php:39-47`). Los AJAX (`seleccionardeposito.php`, `consultatasacambio.php`, `evaluatasacambio.php`) y `cron.php` no verifican sesión. Qué usuarios tenían cada permiso está en la tabla `permisos` (datos reales, no consultados: `db_legacy/` excluido).
