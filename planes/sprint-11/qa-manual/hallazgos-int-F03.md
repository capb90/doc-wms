# Hallazgos integración F03

1. Realizar un cambio en el menu principal de Báscula, dejar los subitems de Entradas, Salidas y Solo Bascula como principales fuera de Historial, y quitar el Historial. El menu quedaria: Dashboard, Proceso de pesaje, Entradas, Salidas, Solo Bascula.

2. Al ingresar el numero de documento y encontrar una coicidencia, lo selecciono y se muestra el deposito, al borrar el ultimo numero en el numero y volver a escribirlo y seleccionarlo se pone en el input del numero de documento la infromacion del deposito. [Imagen del error](./imagenes-hallazgos/Screenshot%202026-11-24%20at%209.58.50 PM.png)

3. En la información del depósito que se muestre, adicional a lo actual, la placa de los camiones. Este detella del deposito se puede mostrar como estaba anteriormente. Adcional hay un error al tratar de seleccionar "Es otro documento: crear depósito nuevo" no queda seleccionado, se devulve al valor anterior.

4. El campo "No de manifiesto" y "P.Manifiesto" al seleccionar un tipo de documento diferente a "Carta Porte" esos campos desaparecen, la solicitud era que esos campos no eran obligatorios y que siempre estuvieran disponibles, cambia la obligatoriedad dependiendo del tipo de documento seleccionado.

5. Estaba llenando los datos del formulario `/operations/weighbridge/process/ca83322f-57a6-40e0-bc3d-e331573e2187?duplicar=1` los tenia completados para guardar pero antes precione "Duplicar entrada" y la información que habia completado se desaparecio y no veo el duplicado en la cola. debe duplicarlo pero no abrirlo inmediatamente. Debo quedar en el registro actual para poder guardar.

6. La opción de cerrar el ciclo sin repesaje debe estar disponible tambien en `/operations/weighbridge/process/{id}`en el header para los repesajes. Actualmente debo ir hasta el historial de la entrada para cerrar el ciclo sin repesaje.

7. En el drawer de detalle de un ciclo de bascula `/operations/weighbridge/history?id=b68db780-a28b-434b-a4d2-a9244e762e8a` ¿Es posible mostrar los valores del el repesaje? 

8. Al editar un ciclo completado, cambie el "P.Indicador (Kg)" sale el siguiente error: status:400, descripcion: "Indique la tara del repesaje.", Endpoint:"http://localhost:5281/api/v1/weighbridge/entries/b68db780-a28b-434b-a4d2-a9244e762e8a".

9. En los Drawers derrogar la regla de los botones del footer, genera confusión al buscarlos. dejar todo en el menu en el boton que aparece en el header del drawer aplica para toda los drawers de la app.

10. Actualmente si tengo un ciclo con "Req. 2 pesaje" para soltarlo debo entrar nuevamente a edicion del ciclo para desmarcarlo, agregar una acción rapida en la "Acciones" de la tabla y el detalle en el drawer, al igual que repesar.

11. En el drawer del detalle de un ciclo en el historial, en la sección de "Pesaje en báscula" aparece el boton de "Editar pesajes", quitar ese boton y dejar la opción de editar en el menu del header.

12. En las tablas de historial del ciclo de pesaje, el peso del manifiesto agruparlo tambien en la columna de "Pesos (Kg)" como "P. Manifiesto" y en acciones utilizar el mismo tipo de boton que se usa en las tablas del modulo de "Configuración". Esto ultimo tambien aplica para la tabla de  `/operations/entries/history` y para todas las tablas de la aplicación. 

13. Para las operaciones de "Solo Bascula" tambien debe haber la opción de "Cerrar ciclo sin repesaje" en caso que el registro se haya ingresado con "Req. 2 pesaje" marcado