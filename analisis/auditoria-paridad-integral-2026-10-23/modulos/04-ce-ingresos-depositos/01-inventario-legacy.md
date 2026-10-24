# 04 — Inventario legacy: Comercio Exterior, ingresos y depósitos

> Auditoría estática del 2026-10-23 (AG-04). Rutas relativas a `code_workspace/`. Código V2 según `docs/contexto/estado.md`: BE `35a61b2` / FE `c924a8b` (no se consultó Git).
> Los permisos legacy salen de `evaluaPermiso($modulo,$accion)` (`bodegas-legacy/verificapermisos.php`, tabla `permisos` por usuario). Los scripts incluyen `Connections/miconexion.php` (no abierto).

## 1. Pantallas del menú legacy de este módulo

`bodegas-legacy/menus/menuizquierda.php:204-220` (grupo «Comercio Exterior»):

| Entrada de menú | Script | Capacidad |
| --- | --- | --- |
| Listas Empaque | `modulos/mod_listasempaque/listarlistas.php` | CF-L129 |
| Ingresos | `modulos/mod_ingresos/listaringresos.php` | CF-L122 |
| Depósitos Import. | `modulos/mod_depositos/listardepositos.php` | CF-L133 |
| Prorrogas (se pinta de rojo con la alerta, `menuizquierda.php:169-180`) | `modulos/mod_depositos/listardepositosprorroga.php` | CF-L140 |
| Depósitos Export. | `modulos/mod_depositos/listardepositosexp.php` | CF-L134 |
| (grupo Colmotores) Etiquetas | `modulos/mod_depositos/adhesivos.php?solocolmotores=1` | CF-L141 (variante Colmotores, excluida) |

Además: alerta de abandono en el panel inicial (`bodegas-legacy/inicial.php:57-73`, solo para `usuario_nivel <= 1`, `inicial.php:78`) y accesos rápidos a ingresos y depósitos (`inicial.php:104-110`, `entrada.php:24,33`).

## 2. Capacidades asignadas

| ID | Funcionalidad | Scripts (todos en `bodegas-legacy/`) | Tablas (L = lectura, E = escritura) | Permiso legacy | Observaciones |
| --- | --- | --- | --- | --- | --- |
| CF-L122 | Consultar y filtrar ingresos | `modulos/mod_ingresos/listaringresos.php` | L: `ingreso`, `documentocomercial`, `deposito`, `cliente`, `empresa_transporte`, `sia`, `productoamparado`, `producto_en_bodega`, `producto`, `embalaje`, `pesaje`, `vehiculo`, `vehiculo_x_empresa`; E: `productodetalle` (VIN, CF-L259) | `ingresos/consultar` (`:39-47`) | Solo ingresos **activos sin depósito** (`:120-124`, `:309-311`). Filtros: doc. comercial, fecha, importador, transportadora, manifiesto DIAN, producto, placa (`:88-117`). Fila roja si falta SIA o peso neto → abre «Modificar ingreso» (`:332-337`). Botón «Crear Depósito» solo si Σ amparada = Σ entrada > 0 (`:515-518`). |
| CF-L123 | Registrar ingreso | `modulos/mod_ingresos/registraringreso.php` (huérfano: ningún enlace lo invoca); el ingreso real nace en báscula (`modulos/mod_bascula/registrarentradabascula.php:76`, `registrarentradavariascp.php:94`) | E: `ingreso` (`registraringreso.php:56-83`) | `ingresos/registrar` | La alta desde Comercio Exterior no está enlazada en el menú; la operación es de báscula (módulo 02). |
| CF-L124 | Modificar ingreso | `modulos/mod_ingresos/modificaringreso.php` | E: `ingreso` (`:87-110`); L: `pesaje` (Σ pesos y precios, `:424`, `:453`) | `ingresos/editar` (`:39-47`) | Campos: fecha/hora de ingreso, manifiesto DIAN (n.º y fecha), doc. comercial (tipo, n.º, fecha), transportadora, SIA, exportador, importador, peso neto, peso bruto, volumen, precio y moneda, condiciones, observaciones (`:305-512`). Sin validación de servidor. SIA 9 por defecto si el importador es 70 (Colmotores, `:397`). **Defecto legacy:** el formulario envía `condiciones2`/`observaciones2` (`:490`, `:494`) pero el `UPDATE` lee `condiciones`/`observaciones` (`:89-110`): cada modificación las borra. Redirige a «Gestionar amparados» (`:113-121`). |
| CF-L125 | Anular ingreso | `modulos/mod_ingresos/eliminaringreso.php` | E: `ingreso` (`:60-79`) | `ingresos/eliminar` | Anulación lógica: `estado='eliminado'`, `nro_doccomercial='ELIMINADO'`, motivo + usuario + IP + fecha en `observaciones` (`:62-76`). No toca pesajes, mercancía ni depósito. RN-018. |
| CF-L126 | Agregar productos amparados | `modulos/mod_ingresos/gestionarproductos.php` | E: `productoamparado` (`:55-76`) | `ingresos/registrar` | Producto + embalaje + cantidad amparada + observaciones. Sin tope ni validación de cantidad. |
| CF-L127 | Modificar producto amparado | `modulos/mod_ingresos/modificargestionarproducto.php` | E: `productoamparado` (`:57`) | `ingresos/editar` | Si la línea vino de un pesaje (`origen` no nulo) bloquea producto y embalaje por JS (`:161-166`). |
| CF-L128 | Eliminar producto amparado | `modulos/mod_ingresos/eliminargestionarproducto.php` | E: `productoamparado.estado` (`:57`) | `ingresos/eliminar` | Baja lógica. Si vino de pesaje solo muestra un `alert` (`:89-93`): el botón no se oculta. |
| CF-L129 | Consultar listas de empaque | `modulos/mod_listasempaque/listarlistas.php`, `verlistaempaque.php` | L: `listaempaquearchivo`, `proveedor_listas`, `listasdeempaque` | `depositos/consultar` (`listarlistas.php:8-9`); `verlistaempaque.php` pide `depositos/registrar` | Pestañas «Vigentes» (con artículos `activo`, `:104-140`) y «Todas» (`:145-170`). |
| CF-L130 | Importar lista de empaque | `modulos/mod_listasempaque/cargarlistasempaque.php`, `evaluaarchivo.php`, `modelo_listaEmpaque.csv` | E: `listaempaquearchivo`, `listasdeempaque`, `producto` (`:52-125`) | `depositos/registrar` (`:8-9`) | CSV con `;`: código, nombre, bultos, unidades por bulto, peso neto. Encabezado sí/no. Aviso de nombre de archivo repetido (`evaluaarchivo.php`). **Defectos legacy:** el filtro MIME asigna en lugar de comparar (`$tipo='text/comma-separated-values'`, `:61`); la búsqueda del producto usa la columna 0 como importador y la 1 como código (`:89-94`); crea producto con `id_embalaje=1` (`:99-113`). |
| CF-L131 | Eliminar lista de empaque | `modulos/mod_listasempaque/eliminarlistaempaque.php` | E: `DELETE listaempaquearchivo` (`:52`) y en cascada `listasdeempaque` (`bodegas_schema.sql:678`) | `depositos/eliminar` | Borra aunque haya artículos ya asociados a pesajes. |
| CF-L132 | Asociar artículos de lista a ingreso | `modulos/mod_listasempaque/listararticulosactivos.php`, `marcarlistaseleccionada.php`; invocado desde `modulos/mod_bascula/modificarentrada.php:1104` | E: `listasdeempaque` (`seleccionado` → `asociado` + `id_pesaje`, `modificarentrada.php:279-283`), `ingreso.id_importador` si estaba vacío (`:287-289`) | `depositos/registrar` | Se hace desde la **modificación del pesaje** en báscula. Cantidad = bultos × unidades (`listararticulosactivos.php:230-238`). RN-016. |
| CF-L133 | Consultar y filtrar depósitos de importación | `modulos/mod_depositos/listardepositos.php`, `verdeposito.php` (ver/imprimir consolidado); `listardepositosanterior.php` y `verdepositanteriro.php` (huérfanos) | L: `ingreso`, `deposito`, `productoamparado`, `producto_en_bodega`, `pesaje`, `factura`; E: `deposito.estado` (CF-L260), `productodetalle` (Colmotores) | `ingresos/consultar` (`:39-40`) | Modalidad 1, estados `activo`/`facturado` (`:140-146`). Filtros como CF-L122 más n.º de depósito con o sin año (`:99-111`). Acciones: Ver depósito, Adhesivo, Editar, Eliminar (`:595-599`). |
| CF-L134 | Consultar depósitos de exportación | `modulos/mod_depositos/listardepositosexp.php` | Igual que CF-L133 | `ingresos/consultar` | Modalidad 2, estado ≠ `eliminado` (`:144-145`). Mismos filtros, incluida placa (`:132-136`). Adhesivo `adhesivoexp.php` (`:573`). |
| CF-L135 | Registrar depósito | `modulos/mod_depositos/registrardeposito.php`, `numerardeposito.php` | E: `deposito`, `producto_en_bodega.id_deposito`, `productodetalle` (`:99-153`) | `depositos/registrar` (`:51-52`) | Exige doc. comercial, transportadora, SIA e importador (`:161-170`, `evaluaIngreso` `:212-218`). Fecha = fecha de ingreso, editable (`:239`). Número propuesto `MAX+1` por año de la fecha de ingreso: `BA0000`, `EXP0000`, `OT0000` (Colmotores aparte) (`:245-297`), editable en pantalla. Crea un detalle (serial de 18 dígitos) por unidad (`:124-145`, RN-021). |
| CF-L136 | Modificar depósito | `modulos/mod_depositos/modificardeposito.php` | E: `deposito` (`:56-76`) | `depositos/editar` | Fecha, **número** y observaciones libres; vuelve el estado a `activo`. |
| CF-L137 | Eliminar depósito | `modulos/mod_depositos/eliminardeposito.php` | E: `producto_en_bodega.id_deposito=NULL`, `DELETE deposito` (`:56-65`) | `depositos/editar` (no `eliminar`, `:8-9`) | Borrado físico sin validar levantes, salidas ni facturas. RN-025. |
| CF-L138 | Consultar detalle y seriales de producto | `modulos/mod_depositos/detalleproducto.php` | L/E: `productodetalle`, `serial` (`:59-130`, `:301`) | `seriales/registrar` (`:8-9`) | Seriales por unidad: automático (código de barras = id con ceros) o manual; casa con `serial` (Colmotores). |
| CF-L139 | Modificar serial de depósito | `modulos/mod_depositos/modificarserial.php` | E: `productodetalle` (`:40-49`) | Sin `evaluaPermiso` | — |
| CF-L140 | Consultar y registrar prórroga | `modulos/mod_depositos/listardepositosprorroga.php`, `registrarprorroga.php` | L: `vista_kardexdepositos2`, `deposito`, `levante`, `salida`…; E: `deposito.prorroga=1` (`registrarprorroga.php:34-41`) | Listado `depositos/registrar` (`:39-40`); `registrarprorroga.php` **sin autenticación** | Universo: importación (mod. 1), ingreso activo, ingresan − nacionalizados > 0 y ≥ 20 días desde `fecha_deposito` (`:121-130`). Faltan = 30 − d o 60 − d; fila roja si faltan ≤ 10 (`:390-409`). Botón «Solicitar» con `confirm` irreversible (`:271-280`, `:751-760`). Enlaza los soportes (`:748`). |
| CF-L141 | Generar y consultar adhesivos (etiquetas) | `modulos/mod_depositos/adhesivos.php`, `adhesivoexp.php`, `adhesivovehiculo.php`, `veradesivo.php`; `adhesivosgm.php` (Colmotores); `reportes/crearpdfetiqueta.php`; `generaradesivo.php` (vacío) | L: depósito, ingreso, amparados, levantes; E: `adhesivos` (acción, depósito, usuario, IP, fecha; `crearpdfetiqueta.php:55-58`) | `depositos/consultar` | Etiqueta «Nacionalizada» o «Sin nacionalizar» a elección (`adhesivos.php:251-254`, `:376-392`), con n.º de depósito con año y Code128, importador, intermediario, cantidades, levantes. Conteo de impresiones y descargas (`:541-560`) y «Impresión # N» impresa en el PDF (`crearpdfetiqueta.php:30-35`). Adhesivo por vehículo (`adhesivovehiculo.php`). El informe `reportes/reporteimpresionadhesivos.php` pertenece a CF-L233 (módulo 07). |
| CF-L142 | Gestionar soportes de depósito | `modulos/mod_depositos/subirsoportes.php`, `procesa.php`, carpeta `documentos/<n.º>` | Archivos (JPG/PNG/GIF, `procesa.php:56-94`) | `procesa.php`: `depositos/registrar`; `subirsoportes.php` sin `evaluaPermiso` | Subir, listar, borrar e imprimir imágenes. |
| CF-L237 | Selector de depósitos (VIN no asociado) | `modulos/mod_depositos/seleccionarvinnoasociado.php` | L: `serial`, `productodetalle` | — | Colmotores: excluida. |
| CF-L259 | Conciliar VIN leídos al listar | `listaringresos.php:384-404`, `listardepositos.php:177-185`, `:442-470` | E: `productodetalle`, `vineslectura` | — | Colmotores: excluida (RN-019). |
| CF-L260 | Reactivar depósito con saldo pendiente | `modulos/mod_depositos/listardepositos.php:507-521`, `:562-576` | E: `deposito.estado='activo'` | (efecto del listado) | Al listar, un depósito `facturado` vuelve a `activo` si queda cantidad o peso amparado por entrar (RN-023). |

## 3. Capacidades no catalogadas encontradas

| ID | Funcionalidad | Scripts | Tablas | Permiso | Nota |
| --- | --- | --- | --- | --- | --- |
| CF-LX04-01 | Alerta de abandono en el panel y en el menú | `menus/evaluaabandonos.php:4-18`; `inicial.php:57-73`; `menus/menuizquierda.php:169-180` | L: `vista_kardexdepositos` | Panel: solo `usuario_nivel <= 1`; menú: todos | Responde `OK` si hay depósitos con ingresan − nacionalizados > 0 entre 20 y 30 días sin prórroga o entre 50 y 60 con prórroga. **No filtra modalidad** (cuenta también exportación). El catálogo la incluye dentro de CF-L003 (módulo 01) y RN-059; aquí se audita por ser parte del flujo de abandono. |

## 4. Scripts del alcance sin capacidad propia

| Script | Estado |
| --- | --- |
| `modulos/mod_depositos/generaradesivo.php` | Página vacía. |
| `modulos/mod_listasempaque/registrarproductolista.php` | Página vacía. |
| `modulos/mod_depositos/listardepositosanterior.php`, `verdepositanteriro.php` | Copias antiguas sin enlace (búsqueda de invocadores sin resultados). |
| `modulos/mod_ingresos/registraringreso.php` | Sin enlace (ver CF-L123). |
| `bodegas-legacy/leerexcel/` | Librería de ejemplo (`example.php`, `.xls` de prueba); ningún script del módulo la usa: la carga de listas lee CSV con `fgets`. |
| `bodegas-legacy/reportes/depositos/` | Salidas HTML/PDF generadas por los adhesivos (`f=depositos/deposito_u<usuario>`); son artefactos con datos, no se abrieron. |
