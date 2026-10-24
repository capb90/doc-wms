# 06-facturacion — 02 Flujos legacy

> AG-06 · 2026-10-23 · Estático. **Prefijos:** `L/` = `bodegas-legacy/`. Rutas relativas a `code_workspace/`.

## F1. Generación de períodos (CF-L201 y CF-L234)

El mismo algoritmo vive dos veces: en `L/cron.php:15-133` y en `L/modulos/mod_facturacion/listardepositosfacturar.php:311-436`, que **lo ejecuta en cada carga del listado**. En la práctica los períodos se recalculaban cuando Facturación abría «Depósitos x Facturar», aunque el cron no corriera.

Por cada ingreso activo con depósito (`cron.php:3-9`; excluye el importador 70 = Colmotores, `:6`):

1. **Borra los períodos no facturados** del depósito para rehacerlos «porque puede cambiar el período» (`cron.php:29-30`; listado `:326`).
2. **Longitud** `P` = `cliente.dias_facturacion` del importador (`cron.php:21-22,32`).
3. **Hasta qué fecha:** si el saldo es 0, hasta la última salida (`:35-49`); si no, hasta hoy (`:50-56`). `días = floor(|Δ|/86400)` (`L/includes/funciones.php:234-239`); `numperiodos = ceil(días/P)`. Si salió el mismo día del ingreso (`días = 0` con saldo 0) → `saliomismodia`.
4. **Primera rama — ya hay períodos facturados** (`:59-97`): toma el último facturado (ordenado por `fechalimite_periodo`). Solo si la fecha de corte es **mayor que su fecha límite** genera más: desde `fin + 1`, con `fin = inicio + P` y `límite = fin + 3` (`:72-76`). Cada período adicional exige que la fecha límite del anterior sea **anterior a hoy** (`:80-89`).
5. **Segunda rama — sin períodos facturados** (`:98-123`): primer inicio = `fecha_deposito`; mismo cálculo; hasta `numperiodos`, cada uno condicionado a que la fecha límite del anterior ya pasó (`:107-116`). Si `días = 0` el bucle no corre: el primer período aparece al día siguiente.
6. **Salida el mismo día** (`:124-133`): un único período.
7. **Inserción:** `INSERT INTO facturaciigo` con `estado='activo'`, sin número ni valor. El cron graba el usuario 6 en la primera rama (`:92`) y `$_SESSION['usuario_id']` en las otras (`:119,:130`).
8. **Estado del depósito** (`:153-343`): si hay existencias o saldo por despachar, `UPDATE deposito SET estado='activo'` (`:337-340`). Al final reactiva los depósitos `facturado` sin períodos desde 2019 (`:349-350`). El paso a `facturado` está comentado (`:64`).

**Resultado de la regla** (`P = 15`, ingreso 01/01): 01/01–16/01, límite 19/01; el siguiente 17/01–01/02, límite 04/02. Cada período cubre `P + 1` días calendario.

**Incertidumbres:**
- No hay crontab ni documentación del horario del cron en el repositorio. Ejecutado por CLI sin sesión, las ramas que usan `$_SESSION['usuario_id']` producirían SQL inválido (`… '','','',,'…`) y el script moriría con `die()`: el cron solo funcionaría bien en la rama con usuario fijo. Esto no se puede confirmar sin ejecución ni el include de `Connections/`, que no se abrió.
- Anomalía de la segunda rama: con saldo 0, `numperiodos` usa la última salida, pero cada período adicional se condiciona a `fechalimite < hoy` y no a la última salida. Un depósito vaciado dentro de la gracia de 3 días podía generar un segundo período si nunca se había facturado el primero. La primera rama compara con la fecha de corte (`:69`) y no tiene ese efecto. El plan backend lo identifica y decide no replicarlo (F3-06, regla 10).
- La fecha límite es editable al facturar (`facturarciigo.php:299-302`) y la primera rama la usa para decidir si genera el siguiente período (`cron.php:69`): cambiarla movía la generación.

## F2. Depósitos por facturar (CF-L201)

Facturación elige un año de ingreso (`listardepositosfacturar.php:280-294`) → la página regenera los períodos (F1) → por depósito muestra número, fecha, días transcurridos, la tabla de períodos con «Facturar» o «Facturada» (`:445-471`), los datos documentales (documento comercial, NIT del importador, SIA, transportadora, manifiestos, TRM del día de ingreso desde `tasa_cambio`, valor de la mercancía en US y en pesos, `:504-530`) y el resumen: ingresos por producto, levantes con tasa, CIF US y CIF CO (`:633-643`), por nacionalizar, despachos y existencias. **Oculta** el depósito si su último período está facturado (`:478-479`). «Facturar» abre `facturarciigo.php` en un diálogo y, al cerrar, recarga en la misma posición (`:214-218`).

## F3. Facturar un período (CF-L202)

1. `facturarciigo.php?id=` carga el período y el depósito (`:98-117`).
2. Arma el **detalle para copiar a SIIGO**: por producto, `entran − salen`, con las salidas hasta el día de inicio del período a las 23:59:59 (`:119-150`); CPI, depósito, período e intermediario (`:250-252`). Botón para copiar al portapapeles (`:223-233`).
3. Propone el N.º = `MAX(nro_facturaciigo) + 1` (`:262-268`), fecha de hoy (`:277`), cliente = importador en mayúsculas (`:284`), valor vacío (`:291`), observaciones y fecha límite (fin + 3) editables (`:299-302`). Validación Spry: todos obligatorios (`:321-325`); el valor solo admite números (`AcceptFloat`).
4. **Guardar** → `UPDATE facturaciigo SET … estado='facturada'` con usuario e IP (`:87-96`). No valida que el número sea único.
5. Cierra el diálogo y recarga el listado (`:239`).

## F4. Facturas emitidas, modificar y anular (CF-L203…205)

- Listado de los períodos con número (`listarfacturas.php:80-85`), filtros por CPI, fecha, depósito, N.º o cliente (`:60-77`), 50 por página.
- **Modificar** (`modificarfactura.php:57-75`): N.º, fecha, fecha límite y observaciones; el detalle se reenvía oculto. El valor y el cliente no se editan.
- **Anular** (`eliminarfactura.php:56-65`): vacía N.º, fecha, detalle y observaciones (el valor y el cliente quedan), vuelve a `activo` y redirige al listado. En la siguiente carga de «Depósitos x Facturar» o del cron, el período se **borra y se regenera** (F1, paso 1) y vuelve a quedar por facturar. No pide motivo ni tiene guardas.

## F5. Informes (CF-L206, CF-L207)

- **Informe de facturación:** año (por defecto el actual) → meses con cantidad y total (`ROUND(SUM(valor))`) de períodos `facturada` por `fecha_facturaciigo` (`informefacturacion.php:92-96`) → clic en el mes → días (`:379-384`). Excel, PDF e impresión por un HTML intermedio (`reportes/facturacion/informe_u{usuario}.html`).
- **Informe por CPI:** autocompletar por N.º de depósito o CPI (`informecpi.php:32-44` → `seleccionardeposito.php`) → encabezado (documento, transportadora, SIA, cliente, cuadrilla, TRM de ingreso), cantidades por producto, despachos con placa y N.º de tiquete de báscula, existencias y facturas con número (`:321-362`). Excel, PDF e impresión.

## F6. Convenios, tarifas y TRM (CF-L017…020, CF-L065…072, CF-L249, CF-LX06-01)

- **Convenio:** cliente + descripción + vigencia (`registrarconvenio.php:57`); se asignan vehículos (CF-L100). En báscula, la placa trae los convenios vigentes hoy (`L/modulos/mod_bascula/consultarconveniosvehiculo.php:10-18`) y el convenio trae sus tarifas del servicio 1 vigentes hoy (`consultartarifasvehiculo.php:10-17`).
- **Tarifa:** servicio + convenio (o ninguno) + vigencia + precio + IVA digitado en % (`registrartarifa.php:57,:255-261`). «Otros servicios» de báscula = tarifas vigentes de servicios distintos del 1 (`consultaotrosservicios.php:7-14`).
- **Tasa de cambio:** una por moneda y semana (`registrartasacambio.php:55,:173-179`), con aviso JavaScript si la semana ya existe (`:128-129` → `consultatasacambio.php`). Se usa para mostrar el valor de la mercancía en pesos (`listardepositosfacturar.php:525-530`; `informecpi.php:111`); la tasa del levante se digita en el levante (módulo 05).
- **Alerta de TRM:** al abrir el panel y el menú, `evaluatasacambio.php` responde «OK» si hay una tasa vigente hoy; si no, aparece «ALERTA! La tasa de cambio está desactualizada» y el clic lleva a la lista de tasas (`inicial.php:37-53`; `menuizquierda.php:149-167`, repetido cada segundo).

## F7. Efectos y errores

- Todo error SQL termina en `die(mysql_error())`: la pantalla muestra el error y no hay transacción.
- Sin auditoría más allá de `id_usuarioregistra`, `ip_registra` y `fechahora_registra` del último cambio.
- Ninguna notificación: Facturación se entera de lo pendiente abriendo el listado.
