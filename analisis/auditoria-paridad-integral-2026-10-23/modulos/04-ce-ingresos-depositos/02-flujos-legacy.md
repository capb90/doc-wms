# 04 — Flujos legacy reconstruidos

> Estático, 2026-10-23. Rutas relativas a `code_workspace/bodegas-legacy/` salvo indicación. Ver el inventario en `01-inventario-legacy.md`.

## F-1. Del camión al depósito (importación)

1. **Báscula crea el ingreso** (módulo 02): `modulos/mod_bascula/registrarentradabascula.php:76` inserta `ingreso` con seis datos (modalidad, fecha, documento comercial, número, transportadora, importador) y el `pesaje` con su `producto_en_bodega` y `productoamparado` (origen pesaje).
2. **Comercio Exterior lista los ingresos pendientes**: `modulos/mod_ingresos/listaringresos.php` muestra solo los ingresos activos **sin depósito** (`:309-311`). Por cada producto amparado compara lo **amparado** (`productoamparado.cantidadamparada`) con lo **entrado** por los camiones (`producto_en_bodega.cantidad`) y el peso bruto amparado con Σ `pesaje.peso_manifiesto` (`:322-505`). La fila se pinta de rojo si falta la SIA o el peso neto (`:332-337`).
3. **Completa el ingreso**: `modificaringreso.php` (manifiesto DIAN, SIA, importador/exportador, pesos, valor y moneda, volumen, condiciones…) sin validación de servidor (`:87-121`) y vuelve a «Gestionar amparados» (`gestionarproductos.php`), donde agrega, modifica o da de baja productos amparados (`:55-76`).
4. **Crea el depósito** cuando Σ amparada = Σ entrada > 0 (`listaringresos.php:515-518`): `modulos/mod_depositos/registrardeposito.php` exige documento, transportadora, SIA e importador (consulta con `JOIN`, `:161-170`; si falta, `alert` y vuelve a modificar el ingreso, `:212-218`). Propone el número `MAX(nro_deposito)+1` del año de la fecha de ingreso (`BA` + 4 dígitos en importación, `EXP` en exportación, `OT` en otras; serie aparte para el importador 70) (`:245-297`), editable. Al guardar: `INSERT deposito` (`:101-117`), `UPDATE producto_en_bodega SET id_deposito` para todo el ingreso (`:121`), un `productodetalle` por unidad con serial automático de 18 dígitos (`:124-145`), y abre «Ver depósito» (`:146-153`).
5. **Etiqueta**: desde el listado de depósitos, «Adhesivo» abre `adhesivos.php` (o `adhesivoexp.php`). El operario elige «Nacionalizada» o «Sin nacionalizar» (`:251-254`); la vista previa arma el HTML con número de depósito con año y Code128, importador, intermediario, ampara/saldo, placas, contenedores y levantes (`:280-535`). «Imprimir»/«Guardar» llaman a `reportes/crearpdfetiqueta.php`, que inserta en `adhesivos` la acción, el usuario, la IP y la fecha (`:55-58`) y escribe «Impresión # N» o «Etiqueta guardada # N» en el PDF (`:30-35`). La pantalla muestra los conteos (`adhesivos.php:541-560`).
6. **Más camiones**: si llegan después, el listado de depósitos recalcula amparado vs entrado; si queda saldo, el depósito vuelve de `facturado` a `activo` (`listardepositos.php:507-521`, `:569-576`, CF-L260).

**Exportación:** mismo recorrido con modalidad 2, listado `listardepositosexp.php` (estado ≠ `eliminado`, `:144-145`) y adhesivo `adhesivoexp.php`.

**Incertidumbres:** no hay registro de qué usuarios usaban `registraringreso.php` (sin enlace). El estado `facturado` lo fija la facturación (módulo 06, `cron.php` / `facturarciigo.php`); aquí solo se ve el retorno a `activo`.

## F-2. Corregir o anular

- **Modificar depósito** (`modificardeposito.php:56-76`): fecha, número y observaciones libres, sin estado previo; el estado vuelve a `activo`.
- **Eliminar depósito** (`eliminardeposito.php:56-65`, permiso `depositos/editar`): desvincula la mercancía (`id_deposito = NULL`) y borra la fila. No revisa levantes, salidas ni facturas; el ingreso vuelve a aparecer en «Ingresos» (porque ya no tiene depósito) y puede crear otro depósito.
- **Anular ingreso** (`eliminaringreso.php:60-79`): `estado='eliminado'`, número «ELIMINADO» y motivo con usuario, IP y fecha. La facturación deja de generar períodos para ingresos anulados (`cron.php:3-9`, citado por el plan F3-08; módulo 06).

## F-3. Listas de empaque

1. `cargarlistasempaque.php`: proveedor (`proveedor_listas`, sin pantalla de alta), importador, archivo CSV `;` con o sin encabezado. Al elegir el archivo, `evaluaarchivo.php` avisa si el nombre ya existe. Inserta `listaempaquearchivo` y cada línea en `listasdeempaque` (`activo`), creando el producto si no lo encuentra (búsqueda defectuosa, `:89-113`).
2. `listarlistas.php`: pestañas «Vigentes» (con artículos activos) y «Todas»; ver (`verlistaempaque.php`) y eliminar (`eliminarlistaempaque.php`, `DELETE` con cascada).
3. **Asociar**: en la modificación del pesaje de báscula (`modulos/mod_bascula/modificarentrada.php:1104`) el botón «Agregar Lista» abre `listararticulosactivos.php?id_ingreso=…`, que lista los artículos activos del importador del ingreso; al asociar marca `seleccionado` (`marcarlistaseleccionada.php`) y agrega al formulario los productos con cantidad = bultos × unidades (`listararticulosactivos.php:230-238`). Al guardar el pesaje: `estado='asociado'` + `id_pesaje` (`modificarentrada.php:279-283`) y el importador del ingreso si estaba vacío (`:287-289`). Al recargar, los `seleccionado` vuelven a `activo` (`:56`).

## F-4. Prórroga y abandono

1. **Alerta**: `inicial.php:57-73` (solo `usuario_nivel <= 1`, `:78`) y `menuizquierda.php:169-180` llaman a `menus/evaluaabandonos.php`, que responde `OK` si en `vista_kardexdepositos` hay depósitos con ingresan − nacionalizados > 0 en 20–30 días sin prórroga o 50–60 con prórroga (`:6-14`). El panel muestra «Existe mercancía con 10 o menos días para pasar a Abandono» con enlace al listado; el menú pinta «Prorrogas» de rojo. Los días cuentan desde `fecha_deposito`.
2. **Listado de prórrogas** (`listardepositosprorroga.php:121-130`): importación, ingreso activo, saldo sin nacionalizar > 0 y ≥ 20 días; muestra fecha, días transcurridos, «FALTAN n días» (30 − d o 60 − d), prórroga Sí/No, datos del documento, mercancía, levantes y salidas, soportes, y el botón «Solicitar».
3. **Registrar prórroga**: `confirm` irreversible (`:271-280`) → `registrarprorroga.php` hace `UPDATE deposito SET prorroga=1` (`:34-41`), sin fecha, usuario ni autenticación.
4. **Vencido**: no hay cambio de estado ni bloqueo; el depósito sigue en el listado con días negativos. La salida a destino de abandono (ciudad −9, modalidad 4) y su reporte son de los módulos 05 y 07.

**Incertidumbres:** `evaluaabandonos.php` no filtra modalidad (puede alertar por exportaciones, que no tienen levantes); el listado sí filtra importación. Las alertas se recalculan en cada carga de página (no hay job).

## F-5. Seriales y soportes

- `detalleproducto.php`: por cada `producto_en_bodega`, sus `productodetalle` (serial automático o manual, cruce con `serial` de Colmotores); `modificarserial.php` cambia uno.
- `subirsoportes.php` + `procesa.php`: imágenes por depósito en `documentos/<n.º depósito>/`, con miniatura, borrado e impresión.
