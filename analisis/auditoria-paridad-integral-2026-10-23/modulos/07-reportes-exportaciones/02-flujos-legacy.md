# 07-reportes-exportaciones — 02 Flujos legacy

> AG-07 · 2026-10-23 · Auditoría estática. Rutas relativas a `code_workspace/`.
> **Prefijos:** `L:` = `bodegas-legacy/`; `INV:` = `bodegas-legacy/modulos/mod_inventario/`; `REP:` = `bodegas-legacy/reportes/`.

## F-07-01 Consultar un informe y exportarlo (patrón común)

1. El usuario abre Comercio Exterior › «Reportes Import.» (`L:menus/menuizquierda.php:215`) → `INV:inicioreportes.php`. La página exige `reportes/consultar` (`INV:inicioreportes.php:38-47`); sin permiso redirige con `error_login=5` (RN-004). La redirección no termina con `exit` (RN-004, «la redirección no siempre termina con exit»).
2. Elige un informe; el formulario hace POST a sí mismo con los filtros.
3. El script arma el SQL concatenando los valores del POST (`INV:reportegeneral.php:81-131`) y pinta la tabla.
4. **Efecto lateral (CF-LX07-01):** al terminar, borra y reescribe `REP:{kardex|diario|general}/informe_u{usuario}.html` con el HTML del informe (`INV:kardex.php:557-562`, `INV:reportediario.php:439-444`).
5. Los iconos de la barra llaman:
   - Excel → `REP:reporteexcel.php?f=…`: lee `{f}.html`, toma lo que sigue a `<!-- TABLA -->`, antepone un logo de un dominio externo y lo devuelve como `.xls` (`REP:reporteexcel.php:2-23`). El `<h2>` con el resumen de filtros queda antes del marcador y no se exporta.
   - PDF / Imprimir → `REP:crearpdf.php?imprimir=0|1&f=…&o=1|2&estilo=…&oficio=…`: dompdf con el encabezado de `REP:encabezado.php` (pie con la dirección y «Pagina X de Y»), guarda `{f}.pdf` y redirige a él; con `imprimir=1` agrega `this.print()`.
6. Ni `reporteexcel.php` ni `crearpdf.php` incluyen `aut_verifica.inc.php`: cualquiera que conozca la ruta puede descargar el último informe de un usuario (incertidumbre: no se probó; depende de la configuración del servidor web).

**Persistencia:** solo archivos; no hay escritura en la base. **Errores:** `or die(mysql_error())` en cada consulta.

## F-07-02 Kardex de un depósito (CF-L209)

1. `INV:kardex.php`: el usuario digita el número; `seleccionardeposito.php` (CF-L241) sugiere depósitos no Colmotores (`INV:kardex.php:133`) y al elegir uno envía `id_deposito`.
2. Encabezado (`:200-260`): depósito, documento comercial, importador, fecha y hora de ingreso, SIA, manifiesto DIAN y la TRM vigente en la fecha de ingreso (`tasa_cambio`, `:227`).
3. Matriz por producto/embalaje (`:266-547`): INGRESO (cantidad y Σ `peso_manifiesto` de los pesajes), un renglón por levante (oculto hasta «Mostrar levantes»), NACIONALIZADOS con «Total CIF» (= Σ `fob_dolares`), POR NACIONALIZAR, un renglón por pesaje de salida sin `pesaje_origen` (oculto hasta «Mostrar salidas»), DESPACHADOS y EXISTENCIAS.
4. Anomalías: la celda «EXISTENCIAS / CANT.» total es `nacionalizados − despachados` (`:546`) mientras la de cada producto es `ingreso − despachado`; el HTML no tiene el marcador `<!-- TABLA -->` (`grep -c` = 0), así que el Excel del kardex sale sin tabla; para Colmotores la cantidad de salida cuenta VIN.

## F-07-03 Diario de ingresos (CF-L210)

1. `INV:reportediario.php`: fechas (hoy por defecto) y tipo de importador (todos / Colmotores / no Colmotores).
2. SQL (`:71-88`): pesajes no eliminados de importación (`PS.id_modalidad=1`) con factura, por `fechahora_inicio` en el rango, ordenados por `fecha_deposito`.
3. Agrupa por depósito: encabezado Depósito / Intermediario / Importador (`:342-346`) y una fila **por pesaje (camión)**: manifiesto DIAN, CPI, manifiesto preimpreso, placa, fecha y hora, tiquete, planilla de envío (vacía), transportadora, embalajes, cantidad, peso de manifiesto, mercancías (`:348-392`). Totales por depósito (con `colspan` desalineado), «Total Vehículos» y tres firmas (`:416-431`).
4. Exportación: Excel, PDF horizontal tamaño oficio, imprimir (`:198-200`).
5. `reportediarioexp.php`: igual para exportación (`I.id_modalidad=2`, exportador). `diario.php` es una copia anterior con el mismo SQL.

## F-07-04 Diario de salidas (CF-L210)

1. `INV:reportediariosalidas.php`: fechas, tipo de importador, cliente (documento o nombre, `LIKE`) y mercancía (`LIKE`) (`:55-78`).
2. SQL (`:83-103`): salidas de importación (`S.id_modalidad=4`) con guía, pesaje de salida sin repesaje, por `fecha_salida`. Solo se muestran las guías que empiezan por «S» (salvo Colmotores).
3. Una fila por pesaje de salida, con las mercancías, embalajes, cantidades, depósitos, CPI, manifiestos, levantes y aceptaciones de sus productos en celdas multilínea; totales por salida y «Total Vehículos» (`:354-600`), firmas (`:605-615`).
4. `reportediariosalidasexp.php`: exportación (`S.id_modalidad=5`).

## F-07-05 Inventario general (CF-L211, CF-L172.c)

1. `INV:reportegeneral.php`: filtros de §3 del inventario. Las fechas entran siempre en el SQL (`D.fecha_deposito`), así que sin fechas no hay filas.
2. Por depósito, por producto/embalaje: ENTRAN, NACIONALIZADOS, SALEN; `saldo = entran − salen` (`:600-610`); con «saldo» descarta saldo ≤ 0 (`:612-618`); «Bodega(s)» cuenta unidades por bodega en `productodetalle_x_seccion` activas (`:620-645`); con un filtro de bodega descarta las filas sin unidades en ella; levantes por producto si se pidió (`:686-701`).
3. Totales de entran, nacionalizados, salen y saldo (`:722-735`). Excel / PDF / imprimir.
4. Variante de Bodega (`L:modulos/mod_bodegas/reportegeneral.php`, permiso `bodegas/consultar`): saldo y levantes fijos, sin fechas, todas las modalidades.

## F-07-06 Nacionalizados y sin nacionalizar (CF-L213)

1. `INV:reportenacionalizados.php`: vista `vista_kardexproductoenbodega` agrupada por depósito, producto y embalaje, con `nacionalizados > 0` (`:59-75`); por cada fila, los levantes con su cantidad (`:356-374`).
2. `INV:reportesinnacionalizar.php`: misma vista, filas con `saldo > 0` y `ingresan − nacionalizados > 0` (`:305-307`).
3. Ambos: título con fecha y hora de generación, totales y firmas; Excel / PDF / imprimir. La vista excluye bajas con la cadena errónea `'elimininado'` (RN-035).

## F-07-07 Prórrogas y salidas en abandono (CF-L214)

1. `INV:reporteprorrogas.php` (rotulado «Dep. para Prórrogas»): productos de depósitos con 30 días o más desde `fechahora_ingreso` **y sin prórroga** (`:64-80`); muestra los de saldo > 0 y sin nacionalizar > 0 (cantidad o peso). Total «SIN NAL.» = suma de nacionalizados (`:388`).
2. `INV:reporteabandonos.php` (rotulado «Salidas en Abandono»): salidas a la ciudad fija `-9` (`:82`) del 1 de enero a hoy por defecto.

## F-07-08 Póliza (CF-L215)

1. `INV:reportepoliza.php`: selector de año a partir de los años de `fecha_levante` (`:230-240`).
2. Para cada mes (por `fecha_deposito`), agrupa levantes y suma `fob_dolares` en «CIF UAP» si `cliente.uap = 1` del importador, si no en «CIF NUAP» (`:386-417`). Totales y firmas (`:419-445`).
3. Clic en un mes → `reportepolizadetalle.php?mes=&anio=` con filtro UAP / no UAP / todos (`:84-110`): una fila por depósito (`vista_poliza`) con el valor de la mercancía (FOB), contenedores (`pesaje.unidadcarga`), levantes, fechas, aceptaciones, «CIF» por levante y su total (`:314-332`, `:440-500`).

## F-07-09 Ingresos por producto e importador (CF-L216)

`INV:reporteingresoproductocliente.php`: importador y fechas obligatorios, producto opcional; `SUM(cantidad)` de `vista_ingrsoproductosclientes` por producto y embalaje (`:85-95`).

## F-07-10 Portal de la agencia (CF-L229)

1. El usuario web con `tipo_acceso = 3` entra por `L:reportesweb/entrada.php` (RN-007) → `reportesias.php`.
2. Lista los ingresos activos de su SIA (`:37-50`); una fila sin existencias solo se ve si tuvo una salida en las últimas 13 horas (`:185`); una fila «Báscula» arrastra el saldo de la anterior (anomalía, plan backend §G.14).
3. Detalle `reportesiasdetalle.php?id=`: pesajes, novedades con imágenes y salidas; no verifica que el ingreso sea de la SIA (RN-008).

## F-07-11 Etiquetas, soportes y código de barras (CF-L231, CF-L233, CF-L258)

- Etiqueta: `adhesivos*.php` → `REP:crearpdfetiqueta.php` (sesión): genera el PDF e **inserta** la acción en `adhesivos` (`:55-58`). Detalle en el módulo 04 (CF-L141).
- Soportes documentales: `subirsoportes.php` → `REP:imprimirdocumentos.php?codigo=<html>`: PDF del HTML pasado por URL, sin sesión.
- Historial de adhesivos: `REP:reporteimpresionadhesivos.php` (sin invocador; rutas de `include` inválidas desde `reportes/`).
- Código de barras: `<img src=".../includes/barcode/code128.php?dato=N">` en guía, autorización de cargue, depósito y adhesivos.

## Incertidumbres

- Uso real de cada informe en producción: no consta (el catálogo legacy lo advierte).
- Si el servidor legacy permitía descargar `reportes/*/informe_u*.html` sin sesión: no verificado (no se ejecutó nada).
- `reporteimpresionadhesivos.php` probablemente no funciona (rutas `../../`), pero no se pudo comprobar.
