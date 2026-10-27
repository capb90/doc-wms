# Nota para los operarios: respuesta al informe de hallazgos

> **Para:** operarios de Vigilancia, Báscula y Comercio Exterior de Bodegas Asociadas.
> **Fecha:** 26 de octubre de 2026.
> **Sobre:** el «Informe de hallazgos y ajustes requeridos en el nuevo sistema».

Gracias por el informe. Revisamos cada punto. Algunas cosas **ya se pueden hacer hoy** y se explican abajo. Las demás **cambian en la próxima versión**, que se instala en el ambiente de pruebas cuando estén listas.

---

## 1. Lo que ya se puede hacer hoy

### Tipo de vehículo

El tipo de vehículo **ya es obligatorio en Báscula**. En la tarjeta «Camión y conductor», el campo «Tipo de Vehículo» está marcado como obligatorio, y el sistema no deja guardar el ingreso sin él.

En Vigilancia es opcional a propósito, para que la entrada del camión sea rápida. Si Vigilancia no lo diligencia, Báscula lo pide.

Los vehículos que vienen del sistema anterior no traen el tipo: el primer pesaje de cada uno lo pide una vez.

### Fecha de ingreso de un camión que llegó la noche anterior

Se corrige en dos pasos, en este orden:

1. **Vigilancia** corrige su ingreso. En el historial de Vigilancia, el botón «Corregir ingreso» cambia la «Fecha y hora de ingreso» y pide un motivo. Lo pueden hacer Vigilancia y el administrador.
2. **Báscula o Comercio Exterior** corrigen la fecha del depósito:
   - al registrar, en «Fecha de ingreso del depósito», con «Cambiar»;
   - después, con «Editar fecha de ingreso», en el detalle del ciclo de Báscula o en el detalle del depósito de Comercio Exterior.

   Si el depósito ya tiene factura de almacenamiento, el sistema la recalcula con la fecha corregida.

La fecha del depósito no puede quedar antes de la entrada que registró Vigilancia. Por eso primero se corrige en Vigilancia.

### Eliminar un tiquete con error

- **Antes del cobro:** en Báscula, «Recuperar» → «Descartar operación».
- **Después de guardado:** «Anular pesaje», en Báscula › Historial o en el «Detalle del ciclo». Pide un motivo de al menos 10 caracteres.
  - El sistema devuelve la mercancía de ese camión y libera el ingreso.
  - Si la factura de báscula sigue en Borrador, la anula. Si ya tiene pagos, la manda a Facturación para revisión.
  - No deja anular si la mercancía ya está reservada o despachada.
- **Si solo está mal un peso:** «Editar» → «Modificar pesaje», con motivo. No hace falta anular.

Cambiar el **cobro** de un tiquete ya guardado (facturar o no, o cambiar el valor) no se hace en Báscula: se anula el pesaje y se repite, o lo ajusta Facturación mientras la factura esté en Borrador.

### Aparecen importadores y no el cliente

Los selectores de «Cliente» muestran **todos los terceros que tienen el rol Cliente**. Al pasar los datos del sistema anterior, cada cliente quedó también como importador, porque así funcionaba allá. Las agencias de aduana y otros terceros que pagan quedaron sin el rol Cliente.

Si el cliente que hace el trámite no aparece, se le agrega el rol:
1. En Comercio Exterior, en el menú «Terceros», se abre el tercero.
2. En sus roles se agrega **Cliente** y se guarda.

Desde ese momento aparece en Báscula y en «Asignar cliente» del detalle del depósito. El cliente de un depósito en Borrador se cambia con «Cambiar cliente». Si ya hay factura de almacenamiento en Borrador, el sistema la pasa al cliente nuevo.

---

## 2. Lo que cambia en la próxima versión

| Su hallazgo | Cómo queda |
| --- | --- |
| **Cartas porte con el mismo número** | Báscula ya no asocia el camión sola. Si el número de carta porte ya tiene depósitos, el sistema los muestra con su cliente, importador, agencia, transportadora, fecha y placas. El operario elige el depósito correcto o «Es otro documento: crear depósito nuevo»; mientras no elija, «Guardar» no se habilita. Los depósitos cerrados se ven en gris, con quién los cerró y cuándo, pero no se pueden elegir. «Agregar otro depósito» no acepta un documento que ya tiene un depósito abierto |
| **Número de manifiesto** | Obligatorio, con su peso, al registrar el ingreso de un camión a un depósito. Solo báscula y Salida no lo piden |
| **Pesos como en el sistema anterior** | Al tomar el primer peso se ven P. indicador, T. vehículo, P. manifiesto y P. mercancía. La tara se calcula sola: indicador menos manifiesto. Si el camión no tiene segundo pesaje, la mercancía según el manifiesto queda como el peso de la mercancía, rotulada «según manifiesto». Si tiene segundo pesaje, manda el peso real |
| **Tiquete en cero** | Si el convenio del cliente dice que la báscula no se cobra, el tiquete sale en $0 con la marca «SIN COBRO POR CONVENIO». El valor cero no se digita a mano: sale del convenio |
| **Manifiesto DIAN** | Comercio Exterior debe diligenciar su número (la fecha no) para confirmar un depósito de importación. La lista «Para confirmar el depósito … falta:» lo indica |
| **Tarjeta: transportadora** | Se quita |
| **Tarjeta: Ampara y Saldo con decimales** | Corregido: «730» en lugar de «730.00». Si la cantidad tiene fracción, como 730,5 toneladas, se muestra la fracción |
| **Tarjeta: fecha de la carta porte** | Muestra el tipo de documento, el número y **la fecha del documento**. Si no se diligenció la fecha, dice «N/A» |
| **Tarjeta: mercancía duplicada** | Corregido: el nombre ya no se repite |
| **Tarjeta: columna Unidad** | Como en el sistema anterior: Ampara · Saldo · Mercancía, con el embalaje dentro del texto, por ejemplo «CEBOLLA FRESCA (SACOS)» |
| **Tarjeta por vehículo** | Además de la tarjeta del depósito, cada camión tiene su tarjeta, con su placa, su manifiesto y lo que trajo ese camión («Cant. ingresa · Mercancía»). Se imprime con «Tarjeta del camión», en la tabla de camiones del detalle del depósito |
| **Pantalla de Báscula y tablero de depósitos** (cambio de aspecto que pidió la revisión) | **Báscula:** la cola de camiones ocupa toda la pantalla, como una tabla con placa, estado, cliente, conductor, documento, primer peso y tiempo de espera. Al elegir un camión, su proceso se abre en un panel grande encima de la cola. «Volver a la cola» (o el botón «Atrás» del navegador) cierra el panel **sin perder lo digitado**; la tecla Esc no lo cierra. Arriba del panel aparecen los otros camiones que tienen datos sin guardar, para cambiar de uno a otro con un clic. Enter y F2 funcionan como antes, y «Guardar» queda arriba, a la derecha. **Comercio Exterior:** en el tablero de depósitos, cada estado es una columna con su propio buscador (documento, número de depósito, tercero o producto) y carga más depósitos al bajar, sin páginas. Arriba quedan solo el tipo de depósito y las fechas. **Todas las pantallas** del menú tienen el mismo encabezado, con el botón «Nuevo …» a la derecha. Algunas acciones de las filas son ahora botones de ícono, como «Acciones» en Facturas, «Registrar prórroga» en Abandono y «Generar Guía» en Pendientes de guía: al pasar el mouse se ve su nombre |
| **Destinatario de la factura** | Facturación puede cambiar a quién va una factura en Borrador con «Cambiar destinatario», junto al destinatario. El sistema propone los terceros de los depósitos de la factura (cliente, importador, agencia y transportadora), por ejemplo la agencia de aduanas, o permite buscar otro cliente |

Cuando la nueva versión esté instalada en el ambiente de pruebas, les avisamos para que la revisen. Los videos de ayuda de Báscula y de Comercio Exterior se actualizarán después.
