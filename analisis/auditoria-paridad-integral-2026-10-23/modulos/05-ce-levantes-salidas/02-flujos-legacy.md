# 05 · Flujos legacy reconstruidos

> Auditoría estática del 2026-10-23 (AG-05). **Prefijos:** `L/` = `bodegas-legacy/`, `LS/` = `bodegas-legacy/modulos/mod_salidas/`, `LL/` = `bodegas-legacy/modulos/mod_levantes/`.

## F1 · Levante (nacionalización)

1. Comercio Exterior abre «Nuevo levante» desde `LL/listarlevantes.php:315` y elige el depósito (`LL/seleccionardeposito.php:14`).
2. `LL/registrarlevante.php` carga la tasa de cambio vigente del día (`:93-99`; si no hay, alerta «La Tasa de Cambio esta desactualizada»). El formulario muestra una columna de cantidad por producto con su saldo por nacionalizar; `evaluaSaldo` (JS, `:255-262`) borra la cantidad si supera el saldo (RN-028). El FOB en pesos lo calcula `calculaPesos` (tasa × FOB USD).
3. Al enviar: busca un levante con el mismo número **o** la misma aceptación en toda la tabla (`:313`); si existe, **no inserta** y no avisa (aviso comentado). Si no existe, inserta `levante` con tasa, FOB USD/COP, peso bruto e importador (`:326-329`).
4. Por cada producto con cantidad > 0, reparte entre las filas `producto_en_bodega` del depósito con `min(pendiente, cantidad del lote)` e inserta `producto_levante`; vincula detalles libres (`:400-436`). Sin transacción.
5. **Modificar** (`LL/modificarlevante.php:88,135-144`): actualiza la cabecera (incluido manifiesto DIAN e importador) y reemplaza las filas de producto.
6. **Retirar un producto** (`LL/eliminarproductolevante.php:52`, `levantes:eliminar`) o **el levante entero** (`LL/eliminarlevante.php:31-47`, sin sesión): borrado físico, sin validar lo despachado.
7. **Efecto aguas abajo:** la salida suma lo nacionalizado por producto y resta lo despachado para mostrar «disponibles» (`LS/registrarsalida.php:790-830`, `:975-1000`).

## F2 · Salida de importación (camino «por número de depósito»)

1. **Báscula** pesa el camión de salida y deja una `salida` en estado `incompleto` ligada al pesaje (la crea el flujo de báscula; ver módulo 02). Al listar, toda salida sin mercancía se marca `incompleto` (`LS/listarsalidas.php:629-643`, RN-037).
2. **Comercio Exterior**, desde el listado, entra a la salida (`listarsalidas.php:415-417` → `nuevasalida.php`) y elige la modalidad (`nuevasalida.php:98-129`).
3. `LS/registrarsalida.php`:
   - consecutivo `nro_salida` = `MAX+1` del año, con piso 758 (pensado para el cliente 70; `:409-417`, RN-031);
   - si el cliente tiene `sinsalidas = 1`, aviso rojo y sin botón «Guardar» (`:546-549`, `:1225-1227`);
   - muestra ingresos, nacionalizados, despachados y disponibles por producto; el aviso de exceso es solo JS (`:231-243`, RN-034);
   - al guardar, actualiza la `salida` (fecha, cliente, transportadora, destino, cuadrilla, observaciones; `:500-503`) y reparte la cantidad entre lotes con su saldo anterior (`:600-680`).
4. **Autorizar cargue** (`LS/autorizarcargue.php:81-99`): al abrir la página se crea `ordencargue` (una por salida, RN-039) y se imprime la orden. Quien tiene el permiso `crearguiasinautorizacion` no pasa por aquí (`:39-46`).
5. **Bodega** completa el cargue (`mod_bodegas/completarcargue.php`, módulo 03): `ordencargue.estado = 'completo'`.
6. **Guía** (`LS/verguia.php`): «Crear Guía» aparece si el cargue está completo o si el usuario tiene `crearguiasinautorizacion` (`listarsalidas.php:688-705`). Con `crear=1` inserta `guiadesalida` con `MAX+1` de su serie (`S00001`; `EXP001` en exportación; 6 dígitos en Colmotores) y `salida.num_guias = 1` (`:172-210`). Al generarla libera las posiciones de bodega (`:478-479`, `:673`, RN-048). El vencimiento es la fecha de la guía + el mayor de los días de las ciudades de destino (`:706-721`). Imprime cuadrilla, levante y saldos.
7. **Imprimir:** `contarimpresiones.php:40-50` suma 1 a `guiadesalida.impresiones` y avisa «La guía se ha impreso en N ocasión(es)» (`verguia.php:224-243`).
8. **Portería** entrega por guía (módulo 03, CF-L230).
9. **No hay cobro de guía:** el legacy no factura la guía (`docs/contexto/decisiones.md` DEC-041, T4).

## F3 · Otras modalidades de salida

- **Usar tiquete de entrada** (`LS/salidausartiquete.php`, `registrarsalida.php:422-490`): crea la salida con la modalidad derivada del ingreso (1 → 4, 2 → 5; RN-033), reutiliza el pesaje de entrada y saca **todo lo nacionalizado** que trajo ese pesaje.
- **Global** (`LS/salidaglobal.php:151-170`, `listarpesajesglobal.php`, `registrarsalida.php:509-531`): un depósito, varios tiquetes de ingreso y **una sola** salida y guía.
- **Consolidada** (`LS/registrarsalidaconsolidada.php:127-155`): un vehículo con mercancía de varios depósitos.
- **Exportación** (`LS/registrarsalidaexp.php`, `listarsalidasexp.php`): la misma mecánica con modalidad 5 y serie `EXP` de guía.

## F4 · Corregir y anular

- **Modificar salida** (`LS/modificarsalida.php:126-140`, `:511-583`): borra y reinserta la mercancía y cambia la cabecera, **también después del despacho**. `modificarorden.php` cambia observaciones y hora de inicio de la orden por AJAX.
- **Quitar un producto** (`LS/eliminarproductosalida.php:35`): DELETE de la fila.
- **Anular salida** (`LS/eliminarsalida.php:87-124`, `salidas:eliminar`, con motivo): desvincula detalles, reactiva la primera ubicación libre por unidad, borra `producto_salida`, deja la salida `eliminado` con motivo y crea una salida nueva `incompleto` a la que mueve los pesajes. **No anula la guía ni toca facturas**; sin transacción (RN-038).

## Incertidumbres

- No se pudo confirmar qué rutas de salida usaban los operarios en producción (el catálogo es del checkout, no del uso).
- La salida de exportación (`registrarsalidaexp.php`) copia el aviso de nacionalizados de importación (`:239`); no se determinó si en exportación se exigía levante.
- `autorizarcargue.php` invierte la guarda de permiso (`!= 0` redirige): se interpretó como «quien puede crear la guía sin autorización no autoriza cargues». Confianza media.
