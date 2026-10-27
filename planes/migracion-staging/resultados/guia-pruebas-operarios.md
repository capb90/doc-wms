# Guía de pruebas para operarios — WMS Bodegas Asociadas (staging)

> **Fecha:** 27/10/2026. Reemplaza la guía del 07/10/2026: staging se reinició limpio ese día (`DEC-043`).
> **Para quién:** los operarios de Vigilancia, Báscula, Bodega, Comercio Exterior y Facturación, y el administrador que los acompaña.
> **Objetivo:** que cada persona pruebe su trabajo diario en el sistema nuevo, sin ayuda, y anote lo que no funcione o no entienda.

## 1. Cómo entrar

- **Dirección de la aplicación:** <https://app.100-60-89-139.sslip.io>
- **Usuario:** el de su rol, en la tabla de abajo.
- **Contraseña:** la contraseña inicial se la entrega el administrador. No la comparta.
- **Primer ingreso:** el sistema le pide **cambiar la contraseña**. Escoja una nueva y guárdela: es solo suya.

| Rol | Usuario | Pantalla de inicio |
|---|---|---|
| Vigilancia | `operario.vigilancia` | Vigilancia → Ingreso |
| Báscula | `operario.bascula` | Báscula → Proceso de Pesaje |
| Bodega | `operario.bodega` | Bodega → Dashboard |
| Comercio Exterior | `operario.comext` | Comercio Exterior → Dashboard |
| Facturación | `operario.facturacion` | Facturación → Dashboard |

## 2. Avisos importantes (léalos antes de empezar)

1. **El sistema empieza limpio.** Solo tiene los datos del sistema anterior: clientes, agencias, transportadoras, **vehículos y conductores**, productos, y los **128 depósitos vivos** con sus levantes. No hay camiones en planta, ni pesajes, órdenes, guías o facturas. **Todo lo que vea de ahí en adelante lo crearon ustedes.**
2. **Los datos del sistema anterior son de junio de 2024.** Para las pruebas se simuló un corte el **26/10/2026**: la facturación de los depósitos migrados arranca el **27/10/2026**. **No use estos datos para operar de verdad** ni para responder a clientes.
3. **Los depósitos migrados todavía no tienen factura de almacenamiento.** Se generan cuando Facturación valide los convenios por cliente. Los depósitos nuevos que ustedes creen sí la generan al confirmarse, con la tarifa general.
4. **Los 67 depósitos que aparecen «en abandono» son normales** en estas pruebas: es el efecto de la fecha de 2024. Uno de ellos, el **2022BA00002**, tiene prórroga (plazo de 60 días).
5. **No hay datos de práctica preparados.** Cada operario empieza con un camión que registra Vigilancia, usando un **vehículo y un conductor migrados**. Cuando invente un documento (carta porte, manifiesto, orden externa, N.º SIIGO), **use el prefijo `PRAC-`**. Ejemplo: `PRAC-CP-0001`.
6. **Lea la nota de cambios** `manuales/nota-operarios-hallazgos-2026-10-26.md`, que responde a su informe de hallazgos. Ya está instalado lo siguiente:
   - el selector del depósito de la carta porte;
   - el manifiesto obligatorio en Báscula y el manifiesto DIAN al confirmar;
   - los cuatro pesos del sistema anterior;
   - la báscula en $0 por convenio;
   - la tarjeta del depósito y la del camión;
   - la cola de báscula con el panel de proceso, el tablero de depósitos con buscador por columna y el encabezado común de las páginas.
7. **«Estadísticas» no está en el menú.** Es a propósito.
8. **Si olvida su contraseña,** pídale al administrador que se la restablezca. La recuperación por correo («¿Olvidó su contraseña?») es solo para el administrador.

## 3. Cómo reportar un problema

Cada vez que algo falle, se vea raro o no sepa qué hacer, anote:

| Dato | Ejemplo |
|---|---|
| **Pantalla** (el título o el menú) | Báscula → Proceso de Pesaje |
| **Hora** | 10:35 |
| **Usuario** | `operario.bascula` |
| **Qué hizo** | Escogí el camión y di clic en «Guardar» |
| **Qué esperaba** | Que pasara al primer pesaje |
| **Qué pasó** | Salió el mensaje «…» y no avanzó |
| **Captura de pantalla** | Adjúntela si puede |

Envíe el reporte a **[completar: persona y canal que indique el responsable de las pruebas]**.

## 4. Tarifas vigentes en staging

- **Báscula:** $20.000 con IVA ($16.806,72 + IVA).
- **Guía de salida:** $15.000.
- **Montacargas** (valor base; el IVA se suma solo si se marca «Aplicar IVA»): Tractomula $220.000, Doble Troque $150.000, Sencillo $140.000, Turbo $110.000 y Guacal o Estiba $40.000.
- **Almacenamiento de importación:** 0,295 % del valor de la mercancía, con un mínimo de $50.000 con IVA. Es la tarifa general mientras Facturación fija la definitiva y valida los convenios.

---

## 5. Vigilancia (`operario.vigilancia`)

**Su trabajo:** registrar la entrada y la salida de los camiones. **Usted abre las pruebas de todos:** cada camión que registre es el que usarán Báscula, Bodega y Comercio Exterior.

### Paso a paso

1. **Registre los camiones de los demás.** En **Vigilancia → Ingreso**, escriba la placa de un **vehículo migrado** y escoja un **conductor migrado** (búsquelo por documento o nombre). Escriba en observaciones **«PRÁCTICA vigilancia»**. Registre al menos:
   - un camión con motivo **«Solo Báscula»**;
   - un camión con motivo **«Descargue mercancía importación»**;
   - un camión con motivo **«Cargue mercancía importación»**, para la salida de un depósito.
   - **Debería ver:** el mensaje de ingreso registrado. El camión aparece en **Vigilancia → Salida** y en la cola de Báscula.
2. **Pruebe el bloqueo de doble ingreso.** Intente registrar otra vez una placa que ya está en planta.
   - **Debería ver:** un aviso de que el vehículo ya tiene un ingreso abierto.
3. **Registre un vehículo nuevo.** En **Ingreso**, escriba una placa inventada que empiece por `PRAC`, por ejemplo **PRAC01**.
   - **Debería ver:** que el sistema le permite crearlo y registrar el ingreso.
4. **Registre la salida.** Cuando Báscula termine con el camión de «Solo Báscula», búsquelo en **Vigilancia → Salida** y registre la salida.
   - **Debería ver:** que el camión sale de la lista y aparece en **Vigilancia → Historial**.

### Para explorar por su cuenta
- **Historial:** filtre por fecha y por placa.
- **Corrección de un ingreso** (placa, conductor o motivo) mientras el camión no tenga servicio en báscula.
- **Ingreso con motivo «Solo bodega»**, que no pasa por báscula.

---

## 6. Báscula (`operario.bascula`)

**Su trabajo:** tomar el camión de la cola, registrar los documentos y las cantidades declaradas, cobrar y pesar.

### Paso a paso

**A. Solo báscula**
1. Entre a **Báscula → Proceso de Pesaje**.
   - **Debería ver:** la cola con los camiones que registró Vigilancia, «sin iniciar».
2. Tome el camión de **«Solo Báscula»**. El cliente es opcional.
3. **Cobro:** escoja el destinatario (puede ser el conductor) y el pago de contado.
   - **Debería ver:** $20.000 ($16.806,72 + $3.193,28 de IVA).
4. **Registre el peso** e imprima el **tiquete**.
   - **Debería ver:** un tiquete con número `2026T…`. El camión queda listo para salir por Vigilancia.

**B. Importación nueva**
1. Tome el camión de **«Descargue mercancía importación»** y escoja **ingreso con depósito**, modalidad **Importación**.
2. **Registre los datos:**
   - la carta porte **`PRAC-CP-0001`** con la fecha de hoy, y el **manifiesto**, que es obligatorio;
   - el cliente, el importador, la agencia de aduanas y la transportadora, escogidos entre los terceros migrados;
   - el producto con su **cantidad, peso neto y peso bruto declarados**, el embalaje, la unidad, el valor de la carga y la moneda.
3. **Cobre** la báscula y registre el **primer peso** (bruto).
   - **Debería ver:** un depósito nuevo `2026BA…` en Borrador, y que Comercio Exterior recibe un aviso.
4. **Segundo peso:** cuando el camión vuelva vacío, registre el **segundo peso** (tara). Bodega debe haber registrado antes la llegada del camión.
   - **Debería ver:** el neto calculado y el tiquete.

**C. Salida de un depósito migrado**
1. Cuando Comercio Exterior tenga la orden de cargue (§8, paso 3), tome el camión de **«Cargue mercancía importación»** y escoja **«Salida de mercancía»** con esa orden.
2. Cobre y registre el **peso del camión vacío**.
3. Cuando Bodega cargue, registre el **repesaje** del camión cargado.

### Para explorar por su cuenta
- **Un segundo camión con la misma carta porte** `PRAC-CP-0001`: el sistema le deja escoger el depósito al que se suma.
- **Un depósito de exportación o de inspección:** pídale a Vigilancia un ingreso con motivo **«Descargue mercancía exportación»** y escoja la modalidad **Exportación**. Para inspección, escoja **Depósito por inspección**, que lleva un solo pesaje. Use una carta porte `PRAC-…`.
- **Retomar o descartar una operación a medias:** opción de recuperar en Báscula.
- **El conductor en «Camión y conductor»:** búsquelo en el selector escribiendo parte del nombre o de la cédula. Si no existe, regístrelo con **«+»**; para corregir su teléfono, use el **lápiz**.
- **Historial** y **Reportes** de báscula.

---

## 7. Bodega (`operario.bodega`)

**Su trabajo:** recibir la mercancía, registrar la llegada y el montacargas, cargar las órdenes y revisar el inventario.

### Paso a paso

1. **Recepción de la importación nueva.** Cuando Báscula registre el primer peso, entre a **Bodega → Recepciones → Ingresos**.
   - Abra el depósito nuevo (`2026BA…`, carta porte `PRAC-CP-0001`).
   - Registre la **llegada**, la **cantidad contada**, una **foto** y la **ubicación**.
   - **Debería ver:** la recepción guardada. Si lo contado difiere de lo declarado, Comercio Exterior recibe un aviso. La cantidad del depósito **no cambia**: es la declarada en báscula.
2. **Montacargas.** En **Bodega → Montacargas → Registrar uso**, inicie un uso para ese depósito con el **horómetro inicial**.
   - Al terminar, escriba el **horómetro final** y abra el cobro.
   - **Debería ver:** la tarifa precargada según el tipo de vehículo; para Tractomula, $220.000.
   - Marque **«Aplicar IVA»**.
   - **Debería ver:** el total con IVA: $261.800 para Tractomula.
3. **Cargue de la orden.** Entre a **Bodega → Órdenes de Cargue** y abra la orden que creó Comercio Exterior.
   - **Una orden de importación no se carga sin guía de salida vigente:** Comercio Exterior emite la guía primero.
   - Verifique y cargue las unidades de la orden.
   - **Debería ver:** la orden cargada y el saldo del depósito reducido.
4. **Inventario.** En **Bodega → Inventario**, busque el depósito de la orden.
   - **Debería ver:** el saldo antes y después del cargue.

### Para explorar por su cuenta
- **Novedades** de bodega.
- **Historial** de recepciones y de montacargas.
- **Inventario general** (reporte).

---

## 8. Comercio Exterior (`operario.comext`)

**Su trabajo:** ser dueño del depósito: confirmarlo, ajustar cantidades, imprimir tarjetas, registrar levantes, crear órdenes de cargue y emitir guías.

### Paso a paso

1. **Depósito nuevo.** Cuando Báscula registre la importación, entre a **Comercio Exterior → Depósitos** y abra el depósito `2026BA…` (carta porte `PRAC-CP-0001`).
   - Asigne el **cliente**, registre el **manifiesto DIAN** (obligatorio para confirmar), **confirme** el depósito e imprima la **tarjeta**.
   - **Debería ver:** el depósito «Confirmado», y que nace su **factura de almacenamiento** en Facturación, con la tarifa general.
   - Cuando ya no lleguen más camiones con ese documento, use **«Cerrar ingreso de camiones»**.
2. **Levante.** Practique un levante **sobre el depósito nuevo**, no sobre los migrados.
   - El valor CIF se registra una sola vez por levante, en el primer producto.
   - **Debería ver:** al cubrir toda la cantidad con levantes, el depósito pasa a «Nacionalizado».
3. **Orden de cargue de un depósito migrado.** Busque en el tablero un depósito migrado **nacionalizado** y con saldo. En **Órdenes de Cargue → Crear Orden**, cree una orden por una parte del saldo, con orden externa **`PRAC-OC-0001`**, y el camión de «Cargue mercancía importación».
   - **Debería ver:** la orden pendiente y las unidades reservadas.
4. **Guía de salida.** En **Guías de Salida → Generar Guía**, emita la guía de esa orden **antes del cargue**.
   - **Debería ver:**
     - la guía con la entrada, el saldo anterior, lo despachado y el nuevo saldo;
     - el código QR;
     - su cobro de $15.000.
   - Si Bodega carga una cantidad distinta a la de la guía, le llega un aviso: anule la guía y emítala de nuevo.

### Para explorar por su cuenta
- **Ajuste de cantidad (CE-7)** sobre el depósito nuevo.
- **Abandono y prórrogas** (el `2022BA00002` tiene prórroga), **Levantes**, **Listas de empaque** y **Reportes** (movimientos por depósito, mercancías ingresadas, mercancía en abandono, inventario general).
- **Tablero de depósitos:** el buscador por columna (documento, depósito, tercero y producto).

---

## 9. Facturación (`operario.facturacion`)

**Su trabajo:** revisar las facturas que genera el sistema, digitar el N.º SIIGO, aprobar y registrar pagos.

### Paso a paso

1. **Cobros del día.** En **Facturación → Facturas**, revise las facturas que generen los otros roles al practicar.
   - **Debería ver:** báscula por $20.000, montacargas por $220.000 o $261.800 con IVA, y guía por $15.000.
2. **Factura de almacenamiento del depósito nuevo.** Cuando Comercio Exterior confirme el depósito, busque su factura en **Borrador**.
   - **Debería ver:** el período desde el día de ingreso, el cliente y la línea de almacenamiento con la tarifa general.
3. **N.º SIIGO.** Use **Acciones → Asignar N.º SIIGO** con **`PRAC-FE-0001`**.
   - **Debería ver:** el número en la factura. El sistema no deja repetir un número.
4. **Aprobar.** Apruebe la factura.
   - **Debería ver:** el estado «Aprobada» y que el N.º SIIGO ya no se puede cambiar.
5. **Registrar un pago:** transferencia, con referencia `PRAC-PAGO-0001`, por una parte del valor.
   - **Debería ver:** el estado «Pago parcial» y el saldo pendiente.

### Para explorar por su cuenta
- **Depósitos Pendientes** por facturar.
- **Configuración de facturación** de un cliente (ciclo, plazo y límite de crédito).
- **Cambiar el destinatario** de una factura en Borrador, por ejemplo a la agencia de aduanas.
- **Anular una factura de práctica** (pide un motivo de al menos 10 caracteres).
- Las **facturas de almacenamiento de los depósitos migrados** aparecen cuando se carguen los convenios.

---

## 10. Medición de tiempo en báscula (PRF-002)

**Qué se mide:** cuánto tarda el operario de báscula en registrar un camión. El sistema anterior lo hacía en unos **30 segundos**.

**Criterio:** registro en báscula en **30 s o menos**.

**Quién:** el operario de báscula (`operario.bascula`), con el responsable de las pruebas, que toma el tiempo.

**Escenario:** un camión que **registre Vigilancia** para la medición, con un **vehículo y un conductor migrados** y motivo «Descargue mercancía importación». Los terceros y el producto deben existir en el sistema. Es la báscula nueva, con la cola y el panel de proceso.

**Cómo medir:**
1. **Ensayo:** el operario practica primero con otro camión para conocer la pantalla.
2. **F3-REG-024 · tiempo del registro:** el cronómetro arranca al **seleccionar el camión** en la cola y para al **guardar** el registro de importación mínimo (documento, manifiesto, cliente, terceros y un producto con cantidades declaradas). Use la carta porte `PRAC-CP-PRF1`.
3. **F3-PES-015 · tiempo hasta el primer peso:** misma medición, pero el cronómetro para cuando **queda registrado el primer peso** (incluye el cobro).
4. **Repeticiones:** si se puede, repita con otro camión. Pídale a Vigilancia un ingreso nuevo y use la carta porte `PRAC-CP-PRF2`.

| Intento | Fecha y hora | Camión | Carta porte | F3-REG-024: hasta guardar (s) | F3-PES-015: hasta el primer peso (s) | ¿≤ 30 s? | Clics o pasos que estorbaron |
|---|---|---|---|---|---|---|---|
| 1 | | | PRAC-CP-PRF1 | | | | |
| 2 | | | PRAC-CP-PRF2 | | | | |
| 3 | | | | | | | |

Entregue la tabla al responsable de las pruebas para el informe.

---

## 11. Para el administrador: volver a empezar

El respaldo **«listo para operarios v2»** es el punto de restauración para repetir las pruebas desde cero:
- base: **`/opt/wms/backups/2026/10/wms_20261027_134951_bf7bf952.dump`** (también en `s3://s3-externo/staging/2026/10/`);
- archivos: **`uploads_20261027_134951_bf7bf952.tar.gz`**;
- corrida `bf7bf952` del 27/10/2026 a las 13:49.

Restaurarlo **borra todo lo que hicieron los operarios después**, incluidas sus contraseñas nuevas: hay que entregarles otra vez la contraseña inicial, que sigue en el archivo local de credenciales del administrador. **Si ya se cargaron los convenios (fase 4b),** use el respaldo «listo para operarios v2, con convenios» que deje esa fase. Restaurar requiere la aprobación del responsable de staging.

Pasos, por SSH en el servidor, siguiendo `deploy/staging/README.md` («Restauración»):

1. **Respaldo previo:** haga un respaldo manual de lo que hay (`POST administration/backups/run`) por si hiciera falta volver.
2. **Detenga el API:** `cd /opt/wms/deploy && docker compose -f compose.staging.yaml stop wms-api`.
3. **Restaure la base:**
   ```bash
   sudo docker cp /opt/wms/backups/2026/10/wms_20261027_134951_bf7bf952.dump wms-staging-postgres-1:/tmp/
   docker exec wms-staging-postgres-1 pg_restore --clean --if-exists -U wms_staging -d wms_staging /tmp/wms_20261027_134951_bf7bf952.dump
   ```
4. **Restaure los archivos subidos** (fotos y soportes):
   - mueva el contenido actual de `/opt/wms/data/uploads` a otra carpeta, **sin borrarlo**;
   - extraiga allí `uploads_20261027_134951_bf7bf952.tar.gz`, con `chown -R 1654:1654`.
5. **Arranque el API:** `docker compose -f compose.staging.yaml start wms-api`. Revise el log.
6. **Contraseña del Admin:** vuelve a la que tenía al momento del respaldo. Si no la tiene, use **«¿Olvidó su contraseña?»** con el usuario `admin`: el enlace llega al correo del administrador.

**Una contraseña olvidada sin restaurar nada:** Administración → Usuarios → el usuario → **restablecer contraseña**. El operario la cambia en su siguiente ingreso.

## 12. Cambios del plan de brechas P1 (instalados el 27/10/2026)

> **Estado:** estos cambios están en staging desde el despliegue de la fase 13 del plan `planes/plan-cerrado-brechas-paridad-p1-2026-10-23.md` (backend `911399c` / frontend `33fbeba`). Entréguesela a los operarios junto con la nota de `DEC-057` y `DEC-058`. Los videos afectados se anotan en `videos/guiones/inventario-cambios-guiones.md` §7.

**Báscula (`operario.bascula`)**
- **Un solo pesaje para varios documentos.** Si un camión trae dos o más documentos, después del Bruto el segundo pesaje es, por defecto, **«Tara — un solo pesaje para todos los depósitos»**. Si el camión descarga en puntos distintos, elija **«Intermedio — el camión descarga en otro punto»** y pese una vez por depósito, como hasta ahora. Con un solo pesaje, el neto del camión se reparte entre los depósitos **en proporción al peso de manifiesto** de cada uno: si a un depósito le falta el peso de manifiesto, su neto queda en blanco hasta que Comercio Exterior lo complete.
- **Un tiquete por depósito.** Cada depósito del camión imprime su tiquete, con la línea «Pesaje compartido por N depósitos · neto del camión X kg». Al final del proceso se imprimen todos.
- **«Solo báscula» sin cliente.** El cliente es opcional. Sin cliente, el cobro va al **conductor** o al **consumidor final**, y el tiquete muestra a quien se cobró.
- **Corregir un pesaje.** En un ciclo con tres pesajes (Bruto, Intermedio, Tara), la corrección cambia **el pesaje que usted elige** y recalcula el neto de los depósitos afectados. Siempre con motivo.
- **El tiquete ya no menciona a la DIAN.** El pie dice «Documento interno de control de pesaje. No es una factura de venta.».

**Comercio Exterior (`operario.comext`)**
- **Marca «sin salidas» del cliente.** En el detalle del tercero, **«Bloquear salidas»** (con motivo de 10 a 500 caracteres) impide crear órdenes de cargue, agregar ítems, emitir guías y que Bodega cargue. No frena los ingresos, la báscula ni los cobros. **«Desbloquear salidas»** la quita, también con motivo. Es aparte del bloqueo por mora.
- **Orden con guía vigente.** Mientras la orden tenga una guía vigente no se puede cancelar ni modificar: **anule primero la guía**. La pantalla lo dice y enlaza a las guías de salida.
- **Guía distinta a lo cargado.** Si emite la guía antes del cargue y Bodega carga una cantidad distinta, le llega el aviso «Guía con cantidades distintas a lo cargado» y el historial de guías marca **«No coincide con lo cargado»**: anule la guía y emítala de nuevo.
- **Guía con código QR.** La guía impresa trae un **código QR** y la leyenda «Escanee para verificar esta guía». Al escanearlo con la cámara del celular se abre una página pública (sin iniciar sesión) que dice **«GUÍA VIGENTE»** o **«GUÍA ANULADA»** y muestra los datos básicos (número, fechas, depósito, destino, productos y cantidades, y la placa con los últimos caracteres ocultos) para compararlos con el papel. Si la página dice que el código no es válido, la guía no lo es. El administrador puede cambiar el parámetro `GUIDE_CODE_TYPE` a `BARCODE` para volver al código de barras.
- **Diario de mercancías ingresadas.** Reportes → «Mercancías ingresadas (diario)» tiene el formato del sistema anterior: un bloque por depósito (agencia, importador, manifiesto DIAN), una fila por camión, total de vehículos y las firmas. Elija la modalidad (Importación por defecto). Se descarga en PDF y en Excel; el diario de salidas también tiene «Exportar Excel».
- **Fecha de ingreso.** El kárdex, los listados y los Excel de importaciones, exportaciones e inspecciones muestran la **fecha de ingreso** del depósito (la corregida, si se corrigió).

**Bodega (`operario.bodega`)**
- **Orden de importación sin guía.** Bodega no carga una orden de importación sin guía de salida vigente (`DEC-056`).

**Facturación (`operario.facturacion`)**
- **Depósitos pendientes.** Hay una columna **«Pendiente»** («Por numerar» o «Por refacturar») y el interruptor **«Solo con facturas por numerar o refacturar»**. Un depósito agotado sigue en la lista mientras tenga una factura en Borrador sin N.º SIIGO o una anulada sin refacturar.
- **Convenios programados.** Un convenio «Programado» exige la fecha de activación (sin hora) y se activa solo a las 00:00 de ese día, archivando el convenio activo del cliente. Usted recibe el aviso.
- **Servicio complementario sin tarifa.** Ya no impide confirmar el depósito: la línea sale en $0 (o con el mínimo del propio servicio) y la factura trae la advertencia para que corrija el valor.
- **Renovaciones.** El período renovado cobra la cantidad que había al cierre del día en que empieza. Las facturas abiertas pueden subir en su próximo recálculo (se notifica el total anterior y el nuevo).
- **Valor CIF (`DEC-029`).** El levante se rotula CIF y el depósito «Valor de la mercancía». Al crear tarifas de almacenamiento, la fórmula prorrateada sale preseleccionada.
