# Revision del documento de consolidación de hallazgos

# 1. Puntos pendientes de aclaración

## Punto PA-01 (Por confirmar comercio exterior)

El deposito de inspección se debe serguir creando como esta actualmente, cambia la flexibilidad en bascula al momento de registrar el ingreso, documentos y producto opcionales y se debe agregar un campo de descripción obligatorio. facturación cobra estos depositos con un valor fijo por vehiculo (Se maneja igual que importación)

## Punto PA-02

En el caso que se presenta el peso de la tara no es correcto, porque en el repesaje se pesa solo el cabezote, y la mercancia queda en el contenedor cargada, por lo cual el operario de comercio exterior debe ingresar en el legacy Comercio Exterior -> Tickets Ingreso -> "Boton editar" -> Modificar Entrada a Bascula y edita el T.vehiculo [Formulario legacy](./edicion_pesos.png). En general el operario de comercio exterior necesita poder editar cualquier peso que se registra en bascula como lo hace en el sistema legacy.

## Punto PA-03

Es una forma de trabajo, El vehiculo ingreso el día anterior cuando el operario estaba fuera de su horario laboral, al siguiente día el operario llego y realizo el ingreso pero no registro el peso porque el conductor no estaba presente. Cuando el conductor llego el operario registro el peso que faltaba. Se crea el registro de ingreso en bascula, pero el peso queda pendiente. *IMPORTANTE*: Se verifico que el sistema actual si tiene esta funcionalidad, solo es un tema de capacitación al operario.

## Punto PA-04

Lo que el operario necesita esque en el selector al empezar a digitar el carta porte, se vayan mostrando opciones, de esta forma no tiene que digitar todo y puede seleccionar el que desea de forma rapida, despues de seleccionar el comportamiento es el mismo que se presenta actualmente, abajo se muesta el deposito y debe mostrar en el detalle del numero del carta porte. En cuanto al estado borrador o confirmado, falta confirmar que muestra el sistema acutalmente, si muestra solo las coicidencias de depositos en estado borrador o tambien en estado confirmado.

## Punto PA-05

Si se utiliza en facturación y comercio exterior. 

## Punto PA-06

Es mejor rediseñar a vistas separadas, dentro del menu historial, tener 3 submenús: Entradas, Salidas y Solo pesaje. con la tabla de datos correspondiente a cada uno. se debe quitar el panel de filtros y manejarlos por columna en la tabla (Los mas relevantes). Y quitar las cards de resumen (Son innecesarias)

## Punto PA-07

La impresión y la descarga funcionaron correctamente, el operario no reporto ningun inconveniente. Sin embargo observe que en el ticket impreso sobra mucho papel verticalmente, se podria optimizar el espacio. 

## Punto PA-08

El operario configura la tasa que rige semanalmente cada lunes desde la configuración del sistema, al realizar el levante se precarga la tasa configurada para esa semana, pero hay levantes de despositos de semanas anteriores por lo cual en ese momento el operario debe cambiar la tasa a la que correspondia en esa semana.

## Punto PA-09

Con la expresión «el cuadrito… no tan para abajo», el operario se refiere al modal de confirmación de levante, que no se genere scroll vertical. Cuando un deposito tiene mas de un producto, en el sistema legacy para realizar el levante se muestra una tabla y por cada producto una columna, el operario si quiere hacer el levante de un producto "X" ponia en cero la cantidad del otro producto "Y" [formulario legacy](./registro_levante_formulario.png). La otra alternativa es tener un select con los productos, como el sistema nuevo y realizar el levante seleccionando el producto. El operario esta dispuesto al cambio al select del producto, pero la alternativa legacy permite en 1 sola vista tener la percepción de todos los productos y sus cantidades.

## Punto PA-10

El «valor CIF» y «valor en aduanas» se refieren al mismo dato, el operario suguere cambiar el label a «valor en aduanas». Actualmente en el legacy aparece como CIF, pero en los documentos oficiales se usa el término «valor en aduanas».

## Punto PA-11

El operario solicito quitar el campo de fecha de aceptación en el levante, solo se solicita la fecha del levante, se debe conservar el mismo formulario legacy, en el cual solo pide fecha.

## Punto PA-12

El sistema actual no calcula automaticamente las cantidades, el operario efatiza en la importancia de que el sistema calcule automaticamente las cantidades, el comportamiento debe ser igual al legacy, en el video se muestra una operación de levante realizada por el operario [video](./levante_y_salida_global.MOV)

## Punto PA-13

Comercio exterior puede editar cualquier peso, lo hace para hacer coicidir la tara o peso de la mercancia con los documentos, en el video se muestra como el operario edita el peso de la mercancia [video](./proceso_levante_edicion_pesos.mov)

## Punto PA-14

La orden de cargue del sistema nuevo se debe modificar para soportar las 3 modalidades de salida que tiene el legacy: 1. Por tiquete de entrada y global, en esta modalidad el camion ingresa cargado, realiza el proceso de pesaje e ingreso, pero el camion no descarga y permanece en la bodega mientras se realiza el proceso de levante, cuando esta listo, se genera la salida mediante el tiquete de ingreso, sin pasar por bascula. La diferencia entre por "tiquete de entrada" y "global" es el firmante de la guia. En el video [video](./levante_y_salida_global.MOV) se explica el proceso de salida global, en el se tiene un deposito que tuvo dos ingresos, es decir la mercancia llego en 2 camiones, por eso en la salida se listan los 2 tickets de entrada que se genero para cada camión y el operario selecciona ambos. 2. por número de depósito, esta modalidad es la que soporta actualmente la ordenes de cargue del sistema nuevo, pero la orden de cargue del sistema nuevo es rigida en el flujo, se debe generar primero la orden de cargue y el camion que llega a cargar debe llegar con ella al pasar por bascual, el problema esque muchas veces, el camion que carga llega sin orden y solo hasta el cargue se sabe que va a cargar el camion y la cantidad, es ahi donde se debe tambien poder generar la orden de cargue. Tener en cuenta como el legacy muestra las cantidades y saldos al generar la guía. En el legacy se genera directamente la guía de salida, en el sistema nuevo se debe generar la orden de cargue para generar la guía de salida, se debe evaluar si en los todos los escenarios sigue siendo util generar primero la orden de cargue y posterior la guía de salida. 

## Punto PA-15 (Confirmar formato de inventario)

El reporte que solicita el operario es de un inventario de mercancia nacionalizada que muestre los levantes y con opciones de filtrar por fecha. El estado del deposito y la etiqueta se mantiene como esta actualmente en el sistema nuevo, se marca como nacionalizado al registrar al menos un levante.

## Punto PA-16

Al registrar el cobro del montacargas en bodega, en el modal de "Facturación y Cobro - Montacargas", se debe cambiar el check de "Agregar IVA (19%)" un switch de "Requiere factura", si requiere factura, se agrega Iva al cobro y el modo de pago es Pendiente por facturar, si no requiere factura, no se incluye el iva y el modo de pago es Inmediato. En la vista de facturación `/billing/invoices` para el servicio de montacargas, cuando el registro es "Requiere factura", en No de factura debe mostrar el estado "Pendiente de número", y el operario puede realizar las acciones de emitir la factura y agregar el numero SIIGO como ahora, si el registro es "No requiere factura", en No de factura debe mostrar el estado "No aplica", en este caso no se genera factura y es solo un registro de la operación.

## Punto PA-17

El reporte de montacargas lo genera el operario de facturación, y es el mismo formato solicitado para los servicios de bascula y guías de salida, separando en 2 columnas los que se facturan y los que no se facturan (Pago Inmediato).

## Punto PA-18

El funcionamiento actual esta correcto, el input debe permitir ingresar decimales. 

## Punto PA-19

Esto se define con las desiciones tomadas en el punto PA-14.

## Punto PA-20

Lo que se solicita esque los pagos queden todos verificados, sin necesidad de verificar manualmente. En almacenamiento funciona de esta manera, al registrar un pago el operario de facturación, queda registrado como verificado, Por eso la expresión «En almacenamiento no» porque ya aplica este comportamiento. 

## Punto PA-21

El simulador de la formula se encuentra en `/admin/stakeholders/{id}` al agregar un servicio al acuerdo, al seleccionar el tipo de formula "Por Umbral de peso", los datos que pide el simulador no corresponde a los datos de la formula, en general el Previsualzar es confuso y no se logra entender como funciona. Con el excel que comparte facturación se debe buscar una mejor alternativa para cargar las formulas de los acuerdos y a que aplica porque el modod e agregar servicios al acuerdo, fue dificil de explicar y entender por parte del operario, ademas de llevar mucho tiempo para configurar a un cliente el acuerdo. 

## Punto PA-22

Los datos del ingreso se pueden editar en cualquier momento, como se hace en el sistema legacy, lo que buscan los operarios es poder tener la misma flexibilidad en el sistema nuevo, se debe permitir editar los mismos datos que se pueden editar en el sistema legacy por parte de comercio exterior y que bascula tambien tenga la posibilidad de correguir los datos. El operario de bascula no los pudo editar por que no tiene la opción de hacerlo desde su modulo.

## Punto PA-23

En bascula en el formulario de registro, se debe quitar el Tipo de vehículo del formulario y ponerlo en bodega al registrar la recepción, los campos deben ser opcionales, esto se almacena como información de cada vehiculo y para facturar el montacargas es necesario el tipo de vehiculo. Adicionalmente, al registar el uso del montacargas en `warehouse/forklift` al ingresar la placa del vehiculo si la información del camion ya trae el tipo de vehiculo, se debe precargar en el formulario.

## Punto PA-24

El comercio exterior el operario solicito usar la tasa manual igual que se hace con el legacy, en facturación tambien seguir la misma logica, aplicar la paridad con el legacy.

## Punto PA-25

Permitir al usuario administrador configurar los destinatarios por rol de la notificación que existen en el sistema. 

# 2. Comentarios extra encontrados en la lectura y revisión de la aplicación

## Bascula.

* En el modulo de bascula al registrar un ingreso de tipo "solo bascula" quitar "Peso esperado" y cliente cambio por "tercero" listan do los terceros en un select paginado y con las opciones de buscar por nombre o Nit.
* Quitar el boten de "soltar camión" no es necesario.
* No debe haber bloquantes para el proceso de bascula, Quitar el bloqueo de bodega para el proceso de repesaje.


## Bodega
* El proceso de bodega no debe ser bloquean para el flujo, los operarios comentan que los súpervisores de bodega suelen estar ocupados para registrar el ingreso y recepción inmediatamente, se propuso que se controle el tiempo de los registros y se lance una alerta cuando se supere un limite, la alerta se debe lanzar a comercio exterior y bodega (la configuración de la alerta se relaciona con el punto PA-25).

## comercio exterior

* H-032. lo mencionado en el contexto no es correcto, la creación de productos no se realiza en bodega. 
* Se debe poder confirmar el deposito sin cliente. la facturación se activa desde que se asigna el cliente (Esto va ligado a la configuración de los acuerdos a partir del excel de facturación).
* En la vista de crear orden de cargue esta demasiado lento los selectores de vehículos, conductor, ciudad los consultas esta trayendo todos los resultados (mas de 1000 registros) lo que relectiza el selector y en la bodega el internet y el equipo de computo no esta actualizado, por que difuculta el floujo. Regla general para el sistema todos los selectores que traigan resultados con listas grandes de la base de datos deben estar paginados y contar con el buscador.

# 3. Para el Analisis funcional

El agente que haga el analisis funcional debe tener en cuenta los recursos adjuntos: 

 * [Video levante y salida global](./levante_y_salida_global.MOV): El operario muestra el flujo de realizar un levante y planillar para generar la salida global de la mercancia que se encuentra en bodega, en este caso el manion llego, realizo el ingreso y permanecio en bodega hasta realizar todo el proceso de nacionalización.

 * [Video Edición pesos y levante](./proceso_levante_edicion_pesos.mov): En el video el operario muestra el flujo de ajustar los pesos y editar el deposito para posteriormente realizar el levante.

 * [Formulario edicion pesos](./edicion_pesos.png): Formulario que utiliza el operario en el legacy para ajustar los pesos.

 * [Formulario registro levante](./registro_levante_formulario.png): Formulario que utiliza el operario en el legacy para registrar el levante y muestra las columnas donde se renderizan los productos.

 * [Excel de convenios y precios](./CONVENIO%2023-24-25-26.xlsx): Excel que utiliza facturación para realizar los cobros a los clientes y a quien debe emitir las facturas, en el se encuetra todos los clientes y sus respectivas formulas de cobro. Tambien en la pestaña "Bascula" estan los precios base para todos los servicios.

 * [Sistema legacy local](http://localhost:8085): El sistema legacy levantado en local con el usuario: username: `superadmin` y password: `Local2024`


# 4. Analisis de interfaz

Realice un analisis de la interfaz actual y con lo observado en la visita presencial que realice el 2025-11-06 propongo las siguientes mejoras y cambios:

## Ajustes generales de interfaz

* Cuando un usuario tiene varios roles asignados al ingresar al panel, en el detalle del usuario y roles en el sidebar se muestra apretado y el avatar se ve cortado [Imagen](./detalle_multiroles_usuario.png)

* En preferencias de "Mi cuenta", el switch de cambiar de tema claro a oscuro no funciona si se trata de cambiar sobre el switch, se debe dar click fuera del switch para que se aplique el cambio.

* En login agregar el boton de ver contraseña en el input de contraseña.

* En los modales cuando hay alertas el header del modal tapa parte de la alerta, se debe agregar un padding al contenido para evitar esto.

* En `/billing/pending-deposits` al cambiar al tema oscuro, la tabla interna que muestra las facturas por periodo no cambia de color.

* Se debe rediseñar el menu, el control de usuario se sigue manejando por roles pero se necesita rediseñar el menu y las paginas teniendo en cuenta lo siguiente:
  * El admin debe tener acceso a todas los modulos, los unicos modulos que es exclusivo para administración es el de "Usuarios" y "Auditoria".
  * Se debe crear una nueva sección que se llame configuración, dentro de esta sección debe estar la gestión de terceros, Productos, Servicios, Conductores, Vehiculos, Motivos de entreda, Ubicaciones, ciudades y Cuadrillas. Esta sección debe permitir realizar el CRUD de cada uno de estos elementos, Pero no manejar precios ni tarifas. Ya no se va a manejar los acuerdos dentro del detalle de un tercero, ni tampoco las tarifas base de los servicios en el detalle de un servicio. A este modulo puede tener acceso, ademas de el admin, el rol de "Comercio Exterior" y "Facturación".
  * Se debe crear una nueva sección que se llame "Tarifas y Acuerdos", a esta sección solo va a tener acceso el rol de "Facturación" y el admin. Esta sección debe permitir gestionar los acuerdos de los terceros y las tarifas de los servicios y todo lo relaciona a tarifas.
  * En el item del menu "Usuarios", se expande para indicar "Listado" y "Crear", para estos casos solo dejar 1 nivel, al dar click en "Usuarios" debe ir directamente a "Listado" y para crear el usuario debe ir desde el boton de crear en el listado, como esta actualmente, esto aplica para todos los items que tengan esta configuración
  * Redisañar las paginas principales de listados, estas paginas estan cargadas de cards innecesarias, quitar la card de titulo y subtitulo de cada pagina y solo dejar la tabla como principal, manejando la tabla CRUD de prime [Referencia](./tabla_crud.png) donde los botones de crear o exportar se encuentran en la parte superior de la misma card. Los filtros se deben manejar por columnas en la tabla siguiendo este estilo de prime [Filtros por columna](./estilo_filtros.png), [Doc prime](https://primevue.dev/datatable/#filter) y debe contener tambien la opcion de sort en las columnas principales, si el endpoint es paginado, se debe realizar el sort en el backend. Si se requiere filtros u opciones globales en la pagina se agrega un card arriba de la tabla principal siguiendo este diseño [Filtros globales](./panel_filtros.png) esto debe ser uniforme en todas las paginas de la aplicación, las acciones de una tabla solo se deben ejecutar mediante los botones no dando click en las filas de la tabla.
  * Dentro de lo posible los CRUD basicos se deben manejar en la pagina principal mediante modals u drawers, al igual que el detalle de un registro. Esto le evita al usuario estar navegando entre paginas.
  * El menu actualmente esta muy denso y dificulta la navegación, se debe rediseñar o reorganizar para que sea mas legible y facil de usar, teniendo en cuenta los otros puntos mencionados.
  * El alance de estos ajustes es todos los modulos.

## Ajustes especificos por modulos

### Modulo de bascula

1. En el proceso de pesaje en `/operations/weighbridge?camion={id}` ya no se va a manejar en un modal, por el tamaño del formulario y para la reutilización en comercio exterior, se debe migrar a un pagina. pero se debe conservar la distribución y estilos que se presentan en el modal actual, con los siguientes ajustes:

**Nombre:** Formulario registro
**Mockups:** [Mockup formulario](./mockups/modelo_bascula) Los mockups fueron hechos con IA, bassados en la idea del formulario, los estilos, fuentes, colores, etc, son solo de referencía. Se los debe tomar solo como fuente de referencia, no se deben implementar exactamente, se deben ajustar al diseño y tema de la aplicación. 

* En la cabecera de la pagina debe mostrar los pasos en el mismo tamaño que se muestra ahora en el modal, y en el lado derecho los botones de "Volver a la cola" y "Guardar"
* Ahora los pasos van a ser 3, "Registro", "Cobro" y "tiquete". El peso se va a registrar en el paso 1 de registro para guardar similitud con el legacy.
* La primera sección (Cada sección en un card propio), es "Vigilancia" aqui se muestra la información que ingreso vigilancia, con la opción de editarla si es necesario. Incialmente se muestra compactada y con el boton de editar se abre como en "Camión y conductor".
* El selector de Tipo de operación se debe quitar, ahora se filtra directamente por el motivo de ingreso que viene de vigilancia, los motivos de ingreso ahora deben tener una categoria que indique si es de tipo "Ingreso", "Salida" o "Solo bascula". Si el operario de vigilancia ingreso de manera erronea el motivo, el operario de bascula lo puede modificar desde la sección anterior de este mismo formulario y el cambio se ve reflejado inmediatamente en el formulario.
* La siguiente sección debe ser la de "Registro" y dentro de esta se debe crear 2 subsecciones, la primera subseccion es la de "Modalidad" aqui el operario selecciona la modalidad de la operación (Importación, Exportación, Inspección) mediante un checkbox. Y en una sola fila, Tipo de documento, Numero de documento y el No de manifiesto. La siguiente subsección es "Mercancía" aqui se muestra la tabla para ir agregando los productos, el boton de agregar producto deben ser mas pequeño. Los productos se debe eliminar la unidad de medida, este dato no se utiliza en nuinguna parte, Quitar la unidad de medida de toda la app no es necesario.
* La siguiente sección debe ser la de "Pesaje (kg)" en esta sección el operario registra los pesos, los inputs se deben mostrar en dos filas y dos columnas, la primera fila debe tener "P. Indicador" y "P. Vehiculo", En la segunda fila debe tener "P. Manifiesto" y "P. Mercancía". El comportamiento debe ser similar al legacy donde se va calculando el T.Vehiculo de acuerdo a lo que se va ingresando en los otros inputs. 
* La siguiente sección es opcional, por lo cual se muestra contraida por depecto y solo si el usuario desea la puede completar, es la seccion "Datos para Comercio exterior" aqui se conservan los datos que se solicitan en la versión actual. 
* La Sección de "Pesaje y Observaciones", eliminarla:
  * Fecha de ingreso del depósito: Se Quita, esto ya se hace en la seccion de vigilancia
  * Primer pesaje: Quitar, en un ingreso con depósito el primer pesaje siempre es Bruto.
  * La configuración del ciclo el switch dejarlo visible en el header para que el usuario pueda deshabilitar el segundo pesaje. 
  * El flujo de perecederos: Quitar el switch, con el switch de "Requiere segundo pesaje" es suficiente para el operario.
  * Las observaciones y los documentos adicionales son innutilizados por el operario y genera ruido por eso se quitan.

* Para la modalidad de "Exportación" e "Inspección" se aplican los mismos cambios que se acaban de mencionar pero teniendo en cuenta tambien los ajustes solicitados y registrados en las secciones anteriores de este documento y de los hallazgos, por ejemplo para el caso de inspección se debe agregar un campo de descripción que es obligatorio. 
* Para los tipo de operación de "Salida de mercancía" y "Solo bascula" quedan las secciones actuales con los ajustes que se mencionen en los hallazgos. 
* Para los input de este formulario eliminar los label de los inputs y los placeholders e implementar los label flotantes de prime para ganar espacio [label flotante](https://primevue.dev/floatlabel/) en la variante variant="on"
* van a haber dos botones de guardar, 1. Boton de "Guardar" y el 2. "Guardar sin pesaje". Para el primer caso los pesajes son obligatorios y guarda el registro y los pesjes, por lo cual en la cola del camion quedaria en "Por cobrar" hasta no completar el paso 2. Para el segundo caso los pesajes no son obligatorios y no los guarda, solo genera el registro como el paso 1 actual, en este caso en la cola del camion qudaria en estado "Por pesar". En ambos casos se redirigue al paso 2 que es el cobro. 
* En el paso 2 de cobro y paso 3 de tiquete, se mantiene la distribución y funcionalidad actual pero desde la pagina, solo se aplican los ajustes si hay, de acuerdo a los hallazgos. 
* Para los estados de "Por cobrar" y "Por pesar" que quedan en la cola de camiones se retoma desde donde quedaron en el flujo. 
* Para el repesaje se puede hacer desde un modal que aparescan solo los 4 pesos y la información ingresada en modo lectura, y deje modificar unicamente el peso del vehiculo (Tara). El agente debe investigar por que en el legacy se puede hacer mas de 1 repesaje y si es necesario implementar esa funcionalidad.
* El operario tambien solicita poder editar la información incluso despues de terminar el ciclo, en el legacy tanto en entradas, salidas y solo pesaje el operario puede seguir editando, esto se pide tambien para la version 2. 

**Nota**: La idea con estos ajustes es simular el comportamiento del legacy en la nueva versión, para que el operario de bascula no le cueste adaptarse a los cambios y siga ingresando la información como lo hace actualmente y de manera agil, este formulario se va a reutilizar en comercio exterior con secciones que se renderizan solo para el operario de comerico exterior como agregar unidades de cargue, mas adelante en la sección de comercio exterior se especifica que secciones se agregan. Esta es una propuesta el agente que analise la funcionalidad debe validar la viabilidad y si existen incongruencias informarlas para tomar desiciones o proponer ajustes si lo requiere. Ademas tambien se debe ampliar con los hallazgos encontrados. 

2. Para el historial `/operations/weighbridge/history` se va dividir en 3 paginas. En el menu el historial tendria 3 subitems: Entradas, Salidas y Solo bascula. Y dentro de entradas 3 tabs: Importación, Exportación e Inspección. Para las entradas la tabla debe mostrar todas las columnas que muestra el legacy (Fecha y Hora, Vehiculo, Conductor, ID. Conductor, P. Bruto, P. Mercancía, Tara Vehiculo, Cantidad, Peso Manifiesto, Doc. Entrada (Tipo y Numero), Repesa, Valor, Ticket, Estado) y adicionalmente las acciones. Para la edición se debe abrir nuevamente el Formulario registro. Para salidas y solo pesaje se debe mostrar las mimas columnas del legacy adicionando ticket y estado. Para estas tablas priorizar los filtros por columnas, y solo filtros globales si se requiere.

### Modulo de bodega

1. En `/warehouse/receptions` agregar un boton para registrar el uso de monstacargas de forma rapida sin necesidad de cambiar de vista.
2. Una de las propuestas es que la bodega no sea bloqueante para otras operaciones, y controlar el tiempo de retraso en los registros, para esto agregar un indicador visual del estado y el tiempo que tiene de retraso el registro, puede ser poner la fila en un color rojo o amarillo. 

### Modulo de Comercio Exterior

En el modulo de comercio exterior se va a rediseñar como se muestran los deposito y su detalle, teniendo en cuenta los hallazgos, analisis hechos por el desarrollador y el flujo que deberia quedar:

1. La pagina `/foreign-trade/deposits` ya no se muestra, se debe ocultar, ahora en el menu "Depositos" debe expandir y mostrar las opciones: "Importación", "Exportación" y "Inspección". 

2. Dentro de cada una de estas opciones se debe mostrar la tabla con los depositos correspondientes y un panel de filtro principal con los filtros por estado "Borrador", "Confirmado", "Anulado" o "Cerrado" y filtro de fecha desde y hasta. al Cambiar cada filtro debe filtrar la tabla con los resultados correspondientes. Por defecto al entrar debe estar marcado los filtros de borrador. En la tabla solo se debe ver 1 estado a la vez y los filtros deben ser claros para el usuario. 

3. **Para Depositos de importación**: Esta tabla va a condensar la información que muestra el legacy en "Tickets ingreso", "Ingresos" y "Depósitos Import.". Se va a utilizar una tabla de prime con row expansion [Tabla Prime](https://primevue.dev/datatable/#row-expansion) para implementar el patron maestro detalle, con las siguientes caracteristicas

  3.1. **Vista principal (Listado)**:

   * MockUps: [Referencia](./mockups/tabla_dep_importacion/) Este mockup fue hecho con IA, los estilos y tema son solo de referencia, se debe adaptar al diseño de la aplicacion pero si tomar en cuenta las columnas de las tablas, la estructura y el patron utilizado. Las columnas si corresponden a las que se debe implementar, al igual que la presentación de los datos. Los botones de accion que se muestran son solo referencia, se deben agregar los que consideres y sean de utilizad al operario. Este mockup aplica para todos los estados del deposito, alguna información puede variar dependiendo del estado.

  3.2. **Detalle de un deposito de importación**:

   * MockUps: [Referencia](./mockups/detalle_deposito/) Este mockup fue hecho con IA, los estilos y tema son solo de referencia, se debe adaptar al diseño de la aplicacion. De este mockup se debe tomar exactamente el step donde se muestra las etapas (Entradas, Datos Pric., Bodega, Amparados, Levantes, Salidas), La disposición de bototnes del header y las etiquetas, La información General (Se debe mostrar exactamente lo que muestra el mockup) y el progreso. Cada etapa que muestra el mockup es solo referencia. al dar click en cada etapa debe mostrar solo lo correspondiente. A continuación describo lo que deberia mostrar cada etapa. 

   * **Entradas**: Incialmente muestra el listado de entradas relacionadas al deposito en una tabla con las columnas: Fecha y Hora, Vehiculo/Placa, Conductor, Ticket de bascula, Mercancía (Embalaje), Peso Buto, Peso Total Mercancia, Tara Vehiculo, Cantidad, Peso Manifiesto y acciones. dentro de acciones debe haber la opción de editar. Al dar click en editar lo lleva a otra pantalla donde se muestra la sección de vigilancia y bascula. En vigilancia muestra los datos registrados en vigilancia al ingresar con la opción de editar, en bascula muestra incialmente los datos de bascula con la opción de editar, al editar muestra el formulario de registro de bascula cy adicionalmente la sección de comercio exterior donde ingresa los campos adicionales como: "Unidades de carga", "Fecha de manifiesto", "Precio Mercancia" y "Modenada". El listado de ingresos en muy importante para el operario por esta razon tambien se debe crear en el menu principal de la aplicación un item de "Tickets de ingreso" donde muestre una tabla con las mismas columnas de la tabla en el deposito mas 1 columna con el numero de deposito relacionado, el numero de deposito dede ser tipo link y al dar click lo lleva al detalle del deposito y en acciones el boton de editar que lo lleva a la misma pantalla de editar un ingreso que se muestra en el detalle del deposito, esto le permite un acceso rapido al usuario.

   * **Datos Principales**: En esta sección se muestra y edita los datos principales del deposito como son: "Fecha y hora", "No Manifiesto", "Fecha manifiesto Dian", "Doc. comercial (Tipo, Numero y fecha)", Terceros relaciondos (Cliente, Empresas de transporte, Agencia de aduanas, Importados), Peso Neto CPI, Peso Bruto CPI, Precio Mercancía CPI, Modena precio. 

   * **Bodega**: En esta sección se muestra y edita los datos relacionados de bodega y se consulta el inventario y movimientos. En el step esta sección se debe mostrar en rojo u amarillo para alertar al operario de comercio exterior que aun no se ha registrado el descargue por parte del operario de bascula despues de cumplido el tiempo limite.

   * **Amparados**: En esta sección se muestra y edita el consolidado de prodcutos desde una tabla, todos los productos del deposito, desde aqui el usuario debe ingresar la cantidad amparada de cada producto, asi como quitar, agregar productos o editar cantidades.

   * **Levantes**: Se diseñaron los mockoups con IA, se encuentran en la carpeta [mockups](./mockups/levantes/) y en el README de esa carpeta se encuentra la explicación del diseño, como fueron con IA sin un contexto amplio del proyecto, se deben adaptar a los estilos del proyecto pero tomando los patrones utilizados, la estructura y las columnas de las tablas que se debe utilizar. 
  
   * **Salidas**: En esta sección se lista en una tabla de row expansión las salidas realizadas para el deposito, la tabla principal muestra en las columnas la fecha el numero de guía generado, modo de salida (cual de las 3 formas de salida que se va a implementar), Ciudad destino y Observaciones y en la tabla de detalle que se expande muestre la relacion de mercancia, una tabla con las columnas: Producto, Cant. Entrada, Saldo Anterior, Cantidad a Salir, Nuevo Saldo y al final el total de la salida. y un link para descargar la guía de salida generada. Debe tener tambien la opción de editar la salida hasta cuando sea posible. Y el boton de Nueva salida 

4. **Para Depositos de exportación e Inspección** La estructura y diseño para depositos de exportación e inspección es similar a la de importación, pero ajustando las etapas y campos correspondientes a cada tipo de deposito.
