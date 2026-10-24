# 05 · Comercio Exterior: levantes, órdenes de cargue, salidas y guías — Inventario legacy

> Auditoría estática del 2026-10-23 (AG-05). No se ejecutó nada ni se consultó Git.
> **Prefijos:** `L/` = `bodegas-legacy/`, `B/` = `Backend/wms-api/`, `F/` = `Frontend/wms/app/`. Rutas relativas a `code_workspace/`.
> **Permisos legacy:** `evaluaPermiso($modulo,$accion)` sobre la tabla `permisos` (`L/verificapermisos.php:33-40`). Se anota el par `módulo:acción` que pide cada script.
> No se abrieron los HTML/PDF generados en `L/reportes/salidas/` ni `L/reportes/ordenes/` (`salida_u{usuario}.html`, `orden_u{usuario}.html`): son copias impresas que pueden tener datos reales. Basta saber que `verguia.php` y `autorizarcargue.php` escriben ahí la guía y la orden para `L/reportes/crearpdf.php`.

## 1. Capacidades asignadas

| ID | Capacidad | Pantallas / scripts | Tablas (L = lectura, E = escritura) | Permiso legacy | Notas |
| --- | --- | --- | --- | --- | --- |
| CF-L143 | Consultar y filtrar levantes | `L/modulos/mod_levantes/listarlevantes.php` (filtros `:95-125`: Cta. porte/factura, depósito con año, importador, fecha, levante, aceptación); `listarlevantes_ante.php` (versión anterior) | L: `ingreso`, `deposito`, `levante`, `producto_levante`, `producto_en_bodega`, `productoamparado`, `tasa_cambio`, `pesaje`, `productodetalle` | `ingresos:consultar` (`listarlevantes.php:39-41`) | Lista depósitos con sus levantes y saldos por producto |
| CF-L144 | Registrar levante | `L/modulos/mod_levantes/registrarlevante.php` (+ `registrarlevante_ante.php`, `registrarlevante-copia.php`, sin enlace) | L: `tasa_cambio` (`:93`), `levante` (duplicado `:313`); E: `levante` (`:326-329`), `producto_levante` (`:424`), `productodetalle` (`:432`) | `levantes:registrar` (`:39-41`) | Un formulario por levante con una columna de cantidad por producto; tasa vigente del día; FOB USD y COP |
| CF-L145 | Modificar levante | `L/modulos/mod_levantes/modificarlevante.php` (+ `modificarlevante_colm.php`, Colmotores) | E: `levante` (`:88`, incluye manifiesto DIAN, tasa, FOB, importador), `producto_levante` (`:135-144`, borra y reinserta) | `levantes:editar` (`:39-41`) | — |
| CF-L146 | Eliminar levante | `L/modulos/mod_levantes/eliminarlevante.php:31-47` | E: `productodetalle` (desvincula), `producto_levante` y `levante` (DELETE físico) | **Ninguno**: el script no incluye `aut_verifica.inc.php` ni `verificapermisos.php` | Lo llama `listarlevantes.php:297` y el ícono «Eliminar» de `registrarlevante.php` |
| CF-L147 | Asignar productos a levante | `L/modulos/mod_levantes/asignarproductos.php:63,77`; `listarproductos.php`, `listarproductosajax.php` | E: `producto_levante`, `productodetalle` | `aut_verifica` + `verificapermisos` (`:5-6`) | Inserta la cantidad del POST sin repetir el tope (RN-028) |
| CF-L148 | Asignar VIN a levante (Colmotores) | `L/modulos/mod_levantes/asignarvines.php:58-84`, `seleccionarvin.php` | E: `producto_levante`, `productodetalle` | — | Excluida (Colmotores) |
| CF-L149 | Quitar producto o VIN de levante | `L/modulos/mod_levantes/eliminarproductolevante.php:52` (DELETE `producto_levante`); `eliminarvinlevante.php:22-33` (VIN) | E: `producto_levante`, `productodetalle` | `levantes:eliminar` (`eliminarproductolevante.php:8-10`) | La parte VIN es Colmotores |
| CF-L150 | Gestionar soportes de levante | `L/modulos/mod_levantes/subirsoportes.php`, `procesa.php:46-83` (`move_uploaded_file`, `unlink`, carpeta `documentos/<nro_levante>`) | Archivos | — | GAP-012: aceptado, no se construye |
| CF-L151 | Consultar salidas de importación | `L/modulos/mod_salidas/listarsalidas.php` (filtros `:327-333`: depósito, guía, fecha de salida, tiquete, transportadora, importador, placa; acciones `:688-752`) | L: `salida`, `producto_salida`, `guiadesalida`, `ordencargue`, `pesaje`; E: `salida.estado` (RN-037, `:638`) | `salidas:consultar` (`:39-41`) | Botones «Aut. Cargue», «Crear Guía», «Ver Guía», editar, eliminar |
| CF-L152 | Consultar salidas de exportación | `L/modulos/mod_salidas/listarsalidasexp.php` (mismos filtros `:317-323`; guía con `modalidad=5`, `:712-718`) | Ídem | `salidas` (`:39`) | — |
| CF-L153 | Elegir modalidad de nueva salida | `L/modulos/mod_salidas/nuevasalida.php:98-129` (usar tiquete, por depósito, global, consolidada, Colmotores); `nuevasalidaexp.php:98-119` | — | `salidas:registrar` (`:39-41`) | `nuevasalidaexp.php:113` enlaza `salidaglobalexp.php`, que no existe en el checkout |
| CF-L154 | Registrar salida de importación | `L/modulos/mod_salidas/registrarsalida.php` (consecutivo `:409-417`; tiquete de entrada `:422-490`; por depósito `:495-505`; global `:509-531`; reparto por lote `:600-680`; nacionalizados y disponibles `:790-830`, `:975-1000`; aviso JS `:231-243`; cliente con salidas bloqueadas `:546-549`, `:1225-1227`) | L: `deposito`, `ingreso`, `cliente.sinsalidas`, `producto_levante`, `levante`; E: `salida`, `pesaje.id_salida`, `producto_salida`, `productodetalle` | `salidas:registrar` (`:39-41`) | La salida de báscula crea antes la salida «incompleto» que Comercio Exterior completa |
| CF-L155 | Registrar salida de exportación | `L/modulos/mod_salidas/registrarsalidaexp.php` (copia de la de importación, `:239`, `:593-705`) | Ídem | `salidas` | — |
| CF-L156 | Registrar salida consolidada | `L/modulos/mod_salidas/registrarsalidaconsolidada.php:99,127-155,710` (+ `salidaconsolidada.php`, `...exp`) | E: `salida` (`tipo_salida='consolidada'`), `vehiculo_x_empresa`, `producto_salida` | `salidas:<accion>` (`:39-45`) | Varios depósitos en un vehículo |
| CF-L157 | Registrar salida Colmotores | `L/modulos/mod_salidas/registrarsalidacolmotores.php`, `salidacolmotores.php` | — | `salidas` | Excluida (Colmotores) |
| CF-L158 | Modificar salida | `L/modulos/mod_salidas/modificarsalida.php:126-140` (desvincula detalles, borra `producto_salida`, actualiza fecha, cliente, transportadora, SIA, destino, cuadrilla, observaciones), `:511-583` (reinserta); `modificarsalidaexp.php`; `modificarsalida_ante.php`; `modificarorden.php` (AJAX: observaciones y hora de inicio, sin sesión) | E: `salida`, `producto_salida`, `productodetalle`, `ordencargue` | `salidas:registrar` (`modificarsalida.php:39-41`) | Se modifica también una salida ya despachada |
| CF-L159 | Anular salida | `L/modulos/mod_salidas/eliminarsalida.php:87-124` (motivo `:206-208`) | E: `productodetalle`, `productodetalle_x_seccion` (reactiva ubicación libre), `producto_salida` (DELETE), `salida` (`eliminado` + motivo), nueva `salida` «incompleto», `pesaje.id_salida` | `salidas:eliminar` (`:39-41`) | No toca la guía ni la factura |
| CF-L160 | Asignar productos a salida | `L/modulos/mod_salidas/asignarproductos.php:87-170`; `listarproductoslevante.php`; `listarproductosajax.php:7-18` | E: `producto_salida`, `productodetalle` | `salidas:registrar` (`:39-41`) | Ramas de tope comentadas (RN-036) |
| CF-L161 | Asignar VIN a salida (Colmotores) | `L/modulos/mod_salidas/asignarvines.php`, `seleccionarvin.php` | — | — | Excluida |
| CF-L162 | Quitar producto o VIN de salida | `L/modulos/mod_salidas/eliminarproductosalida.php:35`; `eliminarvinasignado.php:45-72` (VIN, RN-075) | E: `producto_salida` | — | La parte VIN es Colmotores |
| CF-L163 | Generar y consultar guía de salida | `L/modulos/mod_salidas/verguia.php` (crear `:172-210`; saldos `:434-452`, `:556-643`; libera posiciones `:478-479`, `:673`; vence `:706-721`; cuadrilla `:765`; imprimir `:224-243`); `contarimpresiones.php:40-50` | E: `guiadesalida` (único por salida, `L/bodegas_schema.sql:510-523`), `salida.num_guias`, `productodetalle_x_seccion`; `guiadesalida.impresiones` | `salidas:registrar` (`verguia.php:8-10`) | Serie `S` + 5 dígitos (IMP), `EXP` + 3 (EXP), 6 dígitos (Colmotores), `MAX+1` anual |
| CF-L164 | Autorizar orden de cargue | `L/modulos/mod_salidas/autorizarcargue.php:81-99` (crea `ordencargue` al abrir), `:570-583` (vence); `modificarorden.php` | E: `ordencargue` | Redirige a quien **tiene** `crearguiasinautorizacion:registrar` (`:39-46`) | Para los demás usuarios, «Crear Guía» solo aparece con el cargue `completo` (`listarsalidas.php:688-705`) |
| CF-L165 | Consultar tiquete de salida | `L/modulos/mod_salidas/vertiquete.php:166-330` (embebido en `salidausartiquete*.php`, `salidaconsolidada*.php` por `iframe`) | L: `recibo`, `pesaje`, `factura`, `vehiculo` | `bascula:registrar` (`:7-9`) | Vista del recibo de báscula |
| CF-L166 | Consultar pesajes globales | `L/modulos/mod_salidas/listarpesajesglobal.php` (+ `salidaglobal.php:39-41,151-170`) | L: `pesaje`, `ingreso` | `bascula:consultar` (`listarpesajesglobal.php:6-8`); `salidas:registrar` (`salidaglobal.php`) | Selección de varios tiquetes de ingreso para una salida «global» |
| CF-L167 | Gestionar soportes de salida | `L/modulos/mod_salidas/subirsoportes.php`, `procesa.php:78-115`, `asignarimagenes.php`, `imprimirsoportes.php`; ícono en `listarsalidas.php:680` | Archivos `documentos/<nro_salida>` | — | GAP-012 |
| CF-L238 | Selectores de levantes | `L/modulos/mod_levantes/seleccionardeposito.php:14`, `seleccionardeposito_ante.php`, `seleccionarvin.php`; `listarproductosajax.php:51-82` (saldo por nacionalizar) | L: `deposito`, `producto_en_bodega`, `producto_levante` | Sin `aut_verifica` | AJAX |
| CF-L239 | Selectores de salidas | `L/modulos/mod_salidas/seleccionarciudad.php:10` (LIKE, 10 filas), `seleccionardepositosaldo.php:21` (`vista_kardexdepositos`), `seldepositoexp.php:9`, `seleccionartiqueteingreso.php:9`, `...exp`, `seleccionartiquetesalida*.php`, `listarproductosajax.php:7-18` (nacionalizado y saldo > 0) | L: `ciudad`, `vista_kardexdepositos`, `pesaje`, `factura`, `producto_levante`, `producto_salida` | Sin `aut_verifica` | AJAX |
| CF-L261 | Marcar salida sin mercancía como incompleta | `L/modulos/mod_salidas/listarsalidas.php:629-643` (`UPDATE salida SET estado='incompleto'` al listar) | E: `salida.estado` | `salidas:consultar` | Efecto de escritura dentro de una lectura (RN-037) |

## 2. Capacidades legacy no catalogadas

| ID | Capacidad | Evidencia | Por qué se separa |
| --- | --- | --- | --- |
| CF-LX05-01 | Bloquear las salidas de un cliente (`cliente.sinsalidas`) | Marca en la ficha (`L/modulos/mod_clientes/modificarcliente.php:80,94,480`; `L/bodegas_schema.sql:194`). En la salida, aviso «El cliente tiene bloqueadas las salidas» (`registrarsalida.php:546-549`) y el botón «Guardar» se cambia por «Bloqueado» (`:1225-1227`) | Control comercial manual, independiente de la mora; el catálogo lo menciona solo como campo |
| CF-LX05-02 | Crear la guía solo con el cargue completo, salvo permiso `crearguiasinautorizacion` | `listarsalidas.php:688-705`; `autorizarcargue.php:39-46` | Regla de autorización entre cargue y guía que el catálogo no nombra |

## 3. Desglose por operación

| ID | Operación |
| --- | --- |
| CF-L159.a | Anular la salida **antes** del cargue (equivale a cancelar la orden) |
| CF-L159.b | Anular la salida **después** del cargue (devolver la mercancía) |
| CF-L163.a | Generar la guía (número, saldos, vencimiento, cobro en V2) |
| CF-L163.b | Imprimir la guía y contar las impresiones |

## 4. Fuera de alcance por decisión

Colmotores (importador 70): CF-L148, CF-L157, CF-L161 y las ramas VIN de CF-L149 y CF-L162 (`docs/planes/paridad-legacy/plan-backend-paridad-legacy.md` §A.3). Se buscó `vin`, `vines`, `Colmotores` en `B/Wms.Application/ForeignTrade`, `B/Wms.Domain/Entities/ForeignTrade`, `B/Wms.Domain/Entities/Warehouse/LoadingOrder*.cs`, `DispatchGuide*.cs`, `F/features/foreign-trade` y `F/pages/foreign-trade`: sin resultados.

## 5. Anomalías legacy observadas (no se replican)

- `eliminarlevante.php` borra un levante sin sesión ni permiso (`:31-47`).
- `modificarorden.php` actualiza la salida y la orden por AJAX sin sesión.
- Consecutivos de salida, guía y orden con `MAX+1` fuera de transacción (`registrarsalida.php:409-417`, `verguia.php:181-200`, `autorizarcargue.php:89-97`).
- `registrarlevante.php:326-329` guarda la fecha del levante como fecha de aceptación.
- El duplicado de levante usa `LIKE` sin estado (`registrarlevante.php:313`) y el aviso está comentado (`:330-340`).
- `nuevasalidaexp.php:113` enlaza un script inexistente (`salidaglobalexp.php`).
