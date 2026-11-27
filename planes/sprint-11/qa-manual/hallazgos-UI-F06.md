# Hallazgos UI - F06

1. `http://localhost:3006/foreign-trade/exits?roles=Admin,ForeignTrade` :
   - El botón "Nueva salida" debería estar en la parte superior derecha de la tabla, junto al botón de exportar
   - Quitar la columna "Falta" genera confusión, muestra demasiada informacion
   - Repartir automáticamente el ancho de las columnas, la columan acciones ocupa mucho espacio
   - En el Drawer del detalle -> Tabla "Mercancía" la fila de total basate en los estilos de los levantes con un color diferente y organizada.
   - Utilizar en salida una tabla con row expand, para que al abrir muestre dos tablas 1. la tabla de productos con las columnas (Depósito, Producto, Cantidad, Cargada, Peso asignado, Saldo anterior, Nuevo saldo) y la 2. la tabla con el listado de las guias relacionadas. De esta forma se puede eliminar del drawer de detalle de la salida la seccion de "Mercancia","guia" y "Guías anuladas" y el listado de guias con el tab correspondiente tambien se elimina solo queda la tabla principal sin tabs. Utilizar los estilos de la tabla interna de levantes `foreign-trade/releases`, en esa vista se muestra mas de una tabla

2. `/foreign-trade/exits/new?roles=Admin,ForeignTrade` (Formulario de nueva salida): 
   - Realizar una refactorización completa del formulario, este es el mockup que debes seguir [mockup](./rediseño-formulario-salida/)

3. Etapa Salidas del depósito, en la galería, sección «Etapa Salidas»: 
   - Utilizar en salida una tabla con row expand, para que al abrir muestre dos tablas 1. la tabla de productos con las columnas (Depósito, Producto, Cantidad, Cargada, Peso asignado, Saldo anterior, Nuevo saldo) y la 2. la tabla con el listado de las guias relacionadas. De esta forma se puede eliminar del drawer de detalle de la salida la seccion de "Mercancia","guia" y "Guías anuladas" y el listado de guias con el tab correspondiente tambien se elimina solo queda la tabla principal sin tabs. Utilizar los estilos de la tabla interna de levantes `foreign-trade/releases`, en esa vista se muestra mas de una tabla

4. `http://localhost:3006/warehouse/exits?roles=Admin,Warehouse`:
   - Quitar la columna "Falta" de la tabla.
   - Quitar el boton de "ver" al operario no le interesa toda esa información, el solo carga la mercancia.

5. `/warehouse/exits/history?roles=Admin,Warehouse`:
   - Aqui si se puede dejar el detalle de la salida con la información relevante para el operario de bodega