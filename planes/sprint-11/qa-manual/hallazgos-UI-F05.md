# Hallazgos UI F05

## Listas de depósitos (P-CE-01)

1. En las 3 vistas de listados de depositos: los filtros de estado manejarlos con tabs, como la vista `/operations/weighbridge` y quitar el filtro global de "ingreso desde" y "ingreso hasta", agregar el filtro de columna en la fecha con la opción de seleccionar rangos. De esta forma solo debe quedar la tabla principal y los tabs.

2. En las 3 vistas de listados de depositos: En la columan estados quitar la alerta de las etapas pendientes, es demasiado grande e intrusiva. en su lugar poner un icono de alerta pequeño a lado del numero de deposito y con el tooltip mostrar la descripción.

3. En las 3 vistas de listados de depositos: En la columna de "Estado", mostrar unicamente el estado aduanero que son solo dos: "Sin nacionalizar" o "Nacionalizado" para importación y para expotación e Inspección los estados aduaneros si los tienen o sino ocultar la columna.

4. En las 3 vistas de listados de depositos: La placa de los vehiculos mostrarla en una columna independiente con el filtro por columna correspondiente. 

5. En la vista `/foreign-trade/inspections` para depositos de importación agregar una columna de descripción y poner la descripción a parte del documento.

6. En las 3 vistas de listados de depositos: Quitar la columna de "Pesos (Kg)"

7. En las 3 vistas de listados de depositos: En la columna de "Acciones" Agregar el boton de imprimir la etiqueta del deposito.

## Detalle de importación (Las seis etapas)

1. Las etapas mostrarlas independientes no montadas en una card 

2. Cada etapa montarla en un card principal como la etapa 1 del mockup [mockup](../../../levantamiento_staging/mockups/detalle_deposito/) pero sin el borde y poner el titulo y descripción en el header de esa card y los botones generales de esa etapa van en el header.

3. La información general, balance de cantidades, balance de pesos y progreso se debe rediseñar, ya no se muestre como columna sino que se mueva esa información al header principal de la vista en una card propia junto con la información del header actual. En el [mockup](./detalle-deposito-v2/) se puede ver la distribución que se desea y una aproximación de los estilos, este mockup fue hecho por IA asi que puede haber datos o información que no corresponde. 

4. Etapa 1. Entradas: 
   - Con el punto 2 implementado, Tomar de modelo el diseño de la tabla interna del listado de depositos para implementarlo en esta tabla de camiones del deposito.
   - En las acciones, la opción de "Ver pesajes" lleva a una vista vacia, si esa vista no va, quitar la opción, los pesos igual se ven en la opción de editar.

5. Etapa 2. Datos principales: 
   - Con el punto 2 implementado, cada seccion de esta etapa no va en una card individual, sino que se divide en las mismas secciones en la card principal.
   - Los botones de "Descartar cambios" y "Guardar" van en el header de la card principal.

6. Etapa 3. Bodega: 
   - Con el punto 2 implementado, Tomar de modelo el diseño de la tabla interna del listado de depositos para implementarlo en las tablas de Recepciones y Inventario 
   - En el boton de "Ajustes de cantidad" quitar el texto "CE-7"

7. Etapa 4. Amparados: 
   - Con el punto 2 implementado, Tomar de modelo el diseño de la tabla interna del listado de depositos para implementarlo en la tabla de cantidades amparadas
   - Los botones de "Descartar cambios" y "Guardar" van en el header de la card principal.
   - Al agregar producto al depósito, quitar el motivo (No solicitarlo) y mejorar los estilos y ditribución de ese formulario, por ejemplo el texto "Depósito 2026BA00001. La cantidad se registra por camión; la cantidad del depósito es su suma." ponerlo en el header del modal.
   - En el modal de Corregir producto del depósito, quitar el campo "Motivo" no solicitarlo, y mejorar los estilos y ditribución de ese formulario, por ejemplo el texto "Depósito 2026BA00001. La cantidad se registra por camión; la cantidad del depósito es su suma." ponerlo en el header del modal.

8. Etapa 5. Levantes: 
   - Con el punto 2 implementado, Tomar de modelo el diseño de la tabla interna del listado de depositos para implementarlo en las tablas de levantes.
   - El flujo es poco intuitivo por que la tabla es muy sobrecargada, tomar como modelo el mockup [mockup](./tabla-levantes-detalle-deposito/) las etiquetas de "Sin nacionalizar" o "Nacionalizado" no son necesarias, el color en el saldo indica el estado.
   - Quitar el boton de "Levante total del saldo" y uyilizar botones samll en las acciones y del formulario
   - Los KPI que no ocupen tanto espacio y no sean intrusivos, no es lo principal de la vista.
   - El warning que aparece al darle guardar que sea mas pequeño y no tan intrusivo.
   - A los campos del formulario agregar un tooltip con la descripción o label del campo.

9. Etapa 6. Salidas:
   - Con el punto 2 implementado, Tomar de modelo el diseño de la tabla interna del listado de depositos para implementarlo en las tablas de salidas.

10. Si se necesita agregar un mensaje en una columna al lado de un dato como el de "Datos pendientes", usar un icono de alerta pequeño y con tooltip. Esto aplica para toda la app.

## Detalle de exportación (cinco etapas, sin Levantes)

1. Aplica los mismos cambios visuales de la vista de importación.

## Detalle de inspección (cuatro etapas, sin Levantes ni Amparados)

1. Aplica los mismos cambios visuales de la vista de importación.

## Edición del ingreso (P-CE-03)

1. Aplicar los mismos estilos y distribución que el formulario que se utiliza en bascula.

## Listados y reporte

1. Levantes (vista 2): 
   - Quitar los filtros globales (todos), y agregar los filtros en la columna de la tabla. 
   - las columnas de Ingreso y saldo aparezcan una al lado de la otra.
   - En la columna estado solo debe aparecer el estado aduanero "Sin nacionalizar" o "Nacionalizado".
   - En la columna de "Nacionalizado" no utilizar la barra para mostrar el progreso, utilizar un spinner y el porcentaje
   - En la tabla interna aplicar el mismo concepto que en el detalle de un deposito con los ajustes a las tablas sugeridos en el punto 8 de "Detalle de importación (Las seis etapas)" y quitar el boton tipo texto de "Ver detalle del depósito"

2. Abandono y prórrogas:
   - Quitar la alerta superior, con el filtro en columna es suficiente

3. Listas de empaque:
   - En el modal de "Cargar Lista de empaque" utilizar los mismos estilos y componentes que el Importador de ciudades en `admin/cities`
