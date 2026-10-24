# Guía de pruebas para operarios — WMS Bodegas Asociadas (staging)

> **Fecha:** 07/10/2026.
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

1. **Los datos son reales del sistema anterior, con fecha de junio de 2024.** Para las pruebas se simuló un corte: la facturación arranca el **01/10/2026**. **No use estos datos para operar de verdad** ni para responder a clientes.
2. **Los 66 depósitos que aparecen «en abandono» son normales** en estas pruebas: es el efecto de la fecha de 2024.
3. **«Estadísticas» no está en el menú.** Es a propósito.
4. **Si olvida su contraseña,** pídale al administrador que se la restablezca. La recuperación por correo («¿Olvidó su contraseña?») es solo para el administrador.
5. **Datos de práctica:** lo que se preparó para usted lleva la palabra **«PRÁCTICA»** en las observaciones, y los documentos nuevos empiezan por **`PRAC-`**. Cuando usted cree documentos (carta porte, orden externa, N.º SIIGO), **use también el prefijo `PRAC-`**. Ejemplo: `PRAC-CP-0001`.
6. **Datos de ejemplo de QA:** también verá camiones, depósitos y facturas con el texto **«QA-S6»** o placas que empiezan por **`QS`** (`QSP001`, `QSB202`, `QSC301`, `QSD401`, `QSE501`, `QSE502`). Son pruebas anteriores del equipo técnico y quedan como ejemplo. **No los modifique**, salvo que su paso lo indique.
7. **El camión `QSP001` está reservado** para la medición de tiempo de báscula del equipo técnico (PRF-002). No lo tome.

## 3. Cómo reportar un problema

Cada vez que algo falle, se vea raro o no sepa qué hacer, anote:

| Dato | Ejemplo |
|---|---|
| **Pantalla** (el título o el menú) | Báscula → Proceso de Pesaje |
| **Hora** | 10:35 |
| **Usuario** | `operario.bascula` |
| **Qué hizo** | Escogí el camión GLS926 y di clic en «Guardar» |
| **Qué esperaba** | Que pasara al primer pesaje |
| **Qué pasó** | Salió el mensaje «…» y no avanzó |
| **Captura de pantalla** | Adjúntela si puede |

Envíe el reporte a **[completar: persona y canal que indique el responsable de las pruebas]**.

## 4. Datos de práctica preparados

| # | Para qué | Dato | Estado inicial |
|---|---|---|---|
| P1 | Importación nueva | Camión **GLS926** (Ecuador), con su conductor migrado, motivo «Descargue mercancía importación» | En la cola de báscula, **sin iniciar** |
| P2 | Solo báscula | Camión **SRC396** (Colombia), con su conductor migrado, motivo «Solo Báscula» | En la cola de báscula, **sin iniciar** |
| P3 | Salida de un depósito | Depósito **2024BA00005** (legacy BA0090), nacionalizado, 2.000 unidades. **Orden de cargue 2026OC00004** (orden externa `PRAC-OC-0001`) por **200 unidades**, destino Pasto. Camión **SVO318** (Colombia), con su conductor migrado, motivo «Cargue mercancía importación» | Orden **pendiente**; 200 reservadas y 1.800 disponibles. Camión en la cola de báscula, **sin iniciar** |
| P4 | Levante pendiente | Depósito **2024BA00006** (legacy BA0118), **sin nacionalizar**, 1.350 unidades | Confirmado, sin levante nuevo. Solo para consultar |
| P5 | Factura de almacenamiento | Facturas de almacenamiento de los depósitos **2024BA00001** (BA0008), por **$558.159,96**, y **2024BA00003** (BA0085), por **$474.566,16**. Período del 01/10/2026 al 16/10/2026 | **Borrador**, sin N.º SIIGO |
| P6 | Medición de tiempo (PRF-002) | Camión **CAH514** (Ecuador), con su conductor migrado, motivo «Descargue mercancía importación» | En la cola de báscula, **sin iniciar** |

Tarifas vigentes en staging:
- **Báscula:** $20.000 con IVA ($16.806,72 + IVA).
- **Guía de salida:** $15.000.
- **Montacargas** (valor base; el IVA se suma solo si se marca «Aplicar IVA»): Tractomula $220.000, Doble Troque $150.000, Sencillo $140.000, Turbo $110.000 y Guacal o Estiba $40.000.
- **Almacenamiento de importación:** 0,295 % del valor CIF, con mínimo de $50.000.

---

## 5. Vigilancia (`operario.vigilancia`)

**Su trabajo:** registrar la entrada y la salida de los camiones.

### Paso a paso

1. **Revise los camiones en planta.** Entre a **Vigilancia → Salida**.
   - **Debería ver:** los camiones que están dentro: GLS926, SRC396, SVO318 y CAH514 (los de práctica), más los de ejemplo `QS…`.
2. **Registre un ingreso nuevo.** En **Vigilancia → Ingreso**, escriba una placa migrada que no esté en planta, por ejemplo **TGV158**.
   - Escoja el conductor (búsquelo por documento o nombre), el motivo **«Solo Báscula»** y escriba en observaciones **«PRÁCTICA vigilancia»**.
   - Guarde.
   - **Debería ver:** el mensaje de ingreso registrado. El camión aparece en **Vigilancia → Salida** y en la cola de Báscula.
3. **Pruebe el bloqueo de doble ingreso.** Intente registrar otra vez la placa **TGV158**.
   - **Debería ver:** un aviso de que el vehículo ya tiene un ingreso abierto.
4. **Registre un vehículo nuevo.** En **Ingreso**, escriba una placa inventada que empiece por `PRAC`, por ejemplo **PRAC01**.
   - **Debería ver:** que el sistema le permite crearlo y registrar el ingreso.
5. **Registre la salida.** Cuando Báscula termine con el camión de **P2 (SRC396)**, búsquelo en **Vigilancia → Salida** y registre la salida.
   - **Debería ver:** que el camión sale de la lista y aparece en **Vigilancia → Historial**.

### Para explorar por su cuenta
- **Historial:** filtre por fecha y por placa.
- **Corrección de un ingreso** (placa, conductor o motivo) mientras el camión no tenga servicio en báscula.
- **Ingreso con motivo «Solo bodega»**, que no pasa por báscula.

---

## 6. Báscula (`operario.bascula`)

**Su trabajo:** tomar el camión de la cola, registrar los documentos y las cantidades declaradas, cobrar y pesar.

### Paso a paso

**A. Solo báscula (P2, camión SRC396)**
1. Entre a **Báscula → Proceso de Pesaje**.
   - **Debería ver:** la cola con GLS926, SRC396, SVO318 y CAH514, «sin iniciar».
2. Tome **SRC396**. La operación es **solo báscula**.
3. **Cobro:** escoja el destinatario (puede ser el conductor) y el pago de contado.
   - **Debería ver:** $20.000 ($16.806,72 + $3.193,28 de IVA).
4. **Registre el peso** e imprima el **tiquete**.
   - **Debería ver:** un tiquete con número `2026T…`. El camión queda listo para salir por Vigilancia.

**B. Importación nueva (P1, camión GLS926)**
1. Tome **GLS926** de la cola y escoja **ingreso con depósito**, modalidad **Importación**.
2. **Registre los datos:**
   - carta porte **`PRAC-CP-0001`** con la fecha de hoy;
   - cliente, importador, agencia de aduanas y transportadora, escogidos entre los terceros migrados;
   - el producto con su **cantidad, peso neto y peso bruto declarados**, el embalaje, la unidad, el valor de la carga y la moneda.
3. **Cobre** la báscula y registre el **primer peso** (bruto).
   - **Debería ver:** un depósito nuevo `2026BA…` en Borrador, y que Comercio Exterior recibe un aviso.
4. **Segundo peso:** cuando el camión vuelva vacío, registre el **segundo peso** (tara).
   - **Debería ver:** el neto calculado y el tiquete.

**C. Salida con orden de cargue (P3, camión SVO318)**
1. Tome **SVO318** y escoja **«Salida de mercancía»** con la orden **2026OC00004**.
2. Cobre y registre el **peso del camión vacío**.
   - **Debería ver:** que Bodega puede cargar la orden.
3. Cuando Bodega cargue, registre el **repesaje** del camión cargado.

### Para explorar por su cuenta
- **Un depósito de exportación o de inspección:** en el sistema anterior no había depósitos vivos de esas modalidades, así que no hay datos migrados.
  - Para probarlo, pídale a Vigilancia un ingreso con motivo **«Descargue mercancía exportación»** y, en báscula, escoja la modalidad **Exportación**.
  - Para inspección, escoja **Depósito por inspección**: lleva un solo pesaje.
  - Use una carta porte `PRAC-…`.
- **Un segundo camión con la misma carta porte** `PRAC-CP-0001`: debería sumarse al mismo depósito.
- **Retomar o descartar una operación a medias:** opción de recuperar en Báscula.
- **El conductor en «Camión y conductor»:** el de los camiones de práctica ya viene escogido. Para cambiarlo, búsquelo en el selector escribiendo parte del nombre o de la cédula; si no existe, regístrelo con **«+»**; para corregir su teléfono, use el **lápiz**. Lo mismo aplica en la **Recepción Directa** de Bodega.
- **Historial** y **Reportes** de báscula.

---

## 7. Bodega (`operario.bodega`)

**Su trabajo:** recibir la mercancía, registrar el montacargas, cargar las órdenes y revisar el inventario.

### Paso a paso

1. **Recepción de P1.** Cuando Báscula registre el primer peso de **GLS926**, entre a **Bodega → Recepciones → Ingresos**.
   - Abra el depósito nuevo (`2026BA…`, carta porte `PRAC-CP-0001`).
   - Registre la **cantidad contada**, una **foto** y la **ubicación**.
   - **Debería ver:** la recepción guardada. Si lo contado difiere de lo declarado, Comercio Exterior recibe un aviso. La cantidad del depósito **no cambia**: es la declarada en báscula.
2. **Montacargas.** En **Bodega → Montacargas → Registrar uso**, inicie un uso para el depósito de P1 con el **horómetro inicial**.
   - Al terminar, escriba el **horómetro final** y abra el cobro.
   - **Debería ver:** la tarifa precargada según el tipo de vehículo; para Tractomula, $220.000.
   - Marque **«Aplicar IVA»**.
   - **Debería ver:** el total con IVA: $261.800 para Tractomula.
3. **Cargue de la orden de P3.** Entre a **Bodega → Órdenes de Cargue** y abra **2026OC00004**.
   - Verifique y cargue las **200 unidades** del depósito **2024BA00005**.
   - **Debería ver:** la orden cargada. El depósito queda con **1.800** unidades.
4. **Inventario.** En **Bodega → Inventario**, busque **2024BA00005**.
   - **Debería ver:** el saldo antes y después del cargue.

### Para explorar por su cuenta
- **Novedades** de bodega.
- **Historial** de recepciones y de montacargas.
- **Inventario general** (reporte).

---

## 8. Comercio Exterior (`operario.comext`)

**Su trabajo:** ser dueño del depósito: confirmarlo, ajustar cantidades, imprimir etiquetas, registrar levantes, crear órdenes de cargue y emitir guías.

### Paso a paso

1. **Depósito nuevo de P1.** Cuando Báscula registre GLS926, entre a **Comercio Exterior → Depósitos** y abra el depósito `2026BA…` (carta porte `PRAC-CP-0001`).
   - Asigne el **cliente**, **confirme** el depósito e imprima la **etiqueta «SIN NACIONALIZAR»**.
   - **Debería ver:** el depósito «Confirmado», y que nace su **factura de almacenamiento** en Facturación.
   - Cuando ya no lleguen más camiones con ese documento, use **«Cerrar ingreso de camiones»**.
2. **Levante pendiente (P4).** Abra el depósito **2024BA00006** (sin nacionalizar, 1.350 unidades).
   - **Solo consulte:** el manifiesto, la cantidad y el estado de nacionalización.
   - Si quiere practicar un levante, hágalo sobre **el depósito nuevo de P1**, no sobre P4.
   - **Debería ver:** al cubrir toda la cantidad con levantes, el depósito pasa a «Nacionalizado» y se puede imprimir la etiqueta «NACIONALIZADO».
3. **Orden de cargue de P3.** En **Comercio Exterior → Órdenes de Cargue → Listado**, abra **2026OC00004**.
   - **Debería ver:** 200 unidades del depósito **2024BA00005**, orden externa `PRAC-OC-0001` y estado pendiente.
4. **Guía de salida de P3.** Cuando Bodega cargue la orden, entre a **Guías de Salida → Generar Guía**.
   - **Debería ver:**
     - la guía con la entrada, el saldo anterior (2.000), lo despachado (200) y el nuevo saldo (1.800);
     - su cobro de $15.000.
   - Después **reimprima la etiqueta «NACIONALIZADO»** de 2024BA00005 con la cantidad nueva.

### Para explorar por su cuenta
- **Crear su propia orden de cargue** de otro depósito nacionalizado con saldo, con orden externa `PRAC-OC-…`. **No use** los depósitos BA0042 (2024BA00002) ni BA0558, que tienen pruebas anteriores.
- **Ajuste de cantidad (CE-7)** sobre el depósito de P1.
- **Abandono y prórrogas**, **Levantes**, **Listas de empaque** y **Reportes** (movimientos por depósito, mercancía en abandono, inventario general).

---

## 9. Facturación (`operario.facturacion`)

**Su trabajo:** revisar las facturas que genera el sistema, digitar el N.º SIIGO, aprobar y registrar pagos.

### Paso a paso

1. **Facturas de almacenamiento (P5).** Entre a **Facturación → Facturas** y busque las facturas en **Borrador** de los depósitos **2024BA00001** ($558.159,96) y **2024BA00003** ($474.566,16).
   - **Debería ver:** el detalle con el período del 01/10/2026 al 16/10/2026, el cliente y la línea de almacenamiento.
2. **N.º SIIGO.** En la primera, use **Acciones → Asignar N.º SIIGO** con **`PRAC-FE-0001`**.
   - **Debería ver:** el número en la factura. El sistema no deja repetir un número.
3. **Aprobar.** Apruebe la primera factura.
   - **Debería ver:** el estado «Aprobada» y que el N.º SIIGO ya no se puede cambiar.
4. **Registrar un pago** en la primera: transferencia, con referencia `PRAC-PAGO-0001`, por una parte del valor.
   - **Debería ver:** el estado «Pago parcial» y el saldo pendiente.
5. **Cobros del día.** Revise las facturas de báscula, montacargas y guía que generen los otros roles al practicar.
   - **Debería ver:** báscula por $20.000, montacargas por $220.000 o $261.800 con IVA, y guía por $15.000.

### Para explorar por su cuenta
- **Depósitos Pendientes** por facturar.
- **Configuración de facturación** de un cliente (ciclo, plazo y límite de crédito).
- **Anular una factura de práctica** (pide un motivo de al menos 10 caracteres).
- **La segunda factura de P5 queda en Borrador** para repetir el ejercicio.

---

## 10. Medición de tiempo en báscula (PRF-002)

**Qué se mide:** cuánto tarda el operario de báscula en registrar un camión. El sistema anterior lo hacía en unos **30 segundos**.

**Criterio:** registro en báscula en **30 s o menos**.

**Quién:** el operario de báscula (`operario.bascula`), con el responsable de las pruebas, que toma el tiempo.

**Escenario:**
- **P6:** camión **CAH514**, en la cola sin iniciar, con vehículo, conductor y terceros ya existentes en el sistema.
- **De reserva:** el camión **`QSP001`** del equipo técnico.

**Cómo medir:**
1. **Ensayo:** el operario practica primero con P1 o P2 para conocer la pantalla.
2. **F3-REG-024 · tiempo del registro:** el cronómetro arranca al **seleccionar el camión** en la cola y para al **guardar** el registro de importación mínimo (documento, cliente, terceros y un producto con cantidades declaradas). Use la carta porte `PRAC-CP-PRF1`.
3. **F3-PES-015 · tiempo hasta el primer peso:** misma medición, pero el cronómetro para cuando **queda registrado el primer peso** (incluye el cobro).
4. **Repeticiones:** si se puede, repita con otro camión. Pídale a Vigilancia un ingreso nuevo y use la carta porte `PRAC-CP-PRF2`.

| Intento | Fecha y hora | Camión | Carta porte | F3-REG-024: hasta guardar (s) | F3-PES-015: hasta el primer peso (s) | ¿≤ 30 s? | Clics o pasos que estorbaron |
|---|---|---|---|---|---|---|---|
| 1 | | CAH514 | PRAC-CP-PRF1 | | | | |
| 2 | | | PRAC-CP-PRF2 | | | | |
| 3 | | | | | | | |

Entregue la tabla al responsable de las pruebas para el informe.

---

## 11. Para el administrador: volver a empezar

El respaldo **«listo para operarios»** es el punto de restauración para repetir las pruebas desde cero:
- base: **`/opt/wms/backups/2026/10/wms_20261007_020011_a564692e.dump`**;
- archivos: **`uploads_20261007_020011_a564692e.tar.gz`**;
- corrida `a564692e` del 07/10/2026 a las 02:00.

 Restaurarlo **borra todo lo que hicieron los operarios después**, incluidas sus contraseñas nuevas: hay que entregarles otra vez la contraseña inicial, que sigue en el archivo local de credenciales del administrador.

Pasos, por SSH en el servidor, siguiendo `deploy/staging/README.md` («Restauración»):

1. **Respaldo previo:** haga un respaldo manual de lo que hay (`POST administration/backups/run`) por si hiciera falta volver.
2. **Detenga el API:** `cd /opt/wms/deploy && docker compose -f compose.staging.yaml stop wms-api`.
3. **Restaure la base:**
   ```bash
   sudo docker cp /opt/wms/backups/2026/10/wms_20261007_020011_a564692e.dump wms-staging-postgres-1:/tmp/
   docker exec wms-staging-postgres-1 pg_restore --clean --if-exists -U wms_staging -d wms_staging /tmp/wms_20261007_020011_a564692e.dump
   ```
4. **Restaure los archivos subidos** (fotos y soportes):
   - mueva el contenido actual de `/opt/wms/data/uploads` a otra carpeta, **sin borrarlo**;
   - extraiga allí `uploads_20261007_020011_a564692e.tar.gz`, con `chown -R 1654:1654`.
5. **Arranque el API:** `docker compose -f compose.staging.yaml start wms-api`. Revise el log.
6. **Contraseña del Admin:** vuelve a la que tenía al momento del respaldo. Si no la tiene, use **«¿Olvidó su contraseña?»** con el usuario `admin`: el enlace llega al correo del administrador.

**Una contraseña olvidada sin restaurar nada:** Administración → Usuarios → el usuario → **restablecer contraseña**. El operario la cambia en su siguiente ingreso.

## 12. Cambios que llegan con el próximo despliegue (plan de brechas P1)

> **Estado:** estos cambios están en el código (backend `560f558` / frontend `e2e11e6`, 2026-10-24) pero **no están en staging** hasta el despliegue de la fase 13 del plan `planes/plan-cerrado-brechas-paridad-p1-2026-10-23.md`. Esta sección no cambia los pasos de arriba: avise a los operarios cuando se despliegue y entréguesela. Los videos afectados se anotan en `videos/guiones/inventario-cambios-guiones.md` §7 (no se graban todavía).

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

**Facturación (`operario.facturacion`)**
- **Depósitos pendientes.** Hay una columna **«Pendiente»** («Por numerar» o «Por refacturar») y el interruptor **«Solo con facturas por numerar o refacturar»**. Un depósito agotado sigue en la lista mientras tenga una factura en Borrador sin N.º SIIGO o una anulada sin refacturar. (Se confirma al desplegar: ver `qa/resultados/defectos/DEF-F11-028.md`.)
- **Convenios programados.** Un convenio «Programado» exige la fecha de activación (sin hora) y se activa solo a las 00:00 de ese día, archivando el convenio activo del cliente. Usted recibe el aviso.
- **Servicio complementario sin tarifa.** Ya no impide confirmar el depósito: la línea sale en $0 (o con el mínimo del propio servicio) y la factura trae la advertencia para que corrija el valor.
- **Renovaciones.** El período renovado cobra la cantidad que había al cierre del día en que empieza. Las facturas abiertas pueden subir en su próximo recálculo (se notifica el total anterior y el nuevo).
