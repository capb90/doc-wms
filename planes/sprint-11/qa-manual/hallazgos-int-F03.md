# Hallazgos integración F03

1. Realizar un cambio en el menu principal de Báscula, dejar los subitems de Entradas, Salidas y Solo Bascula como principales fuera de Historial, y quitar el Historial. El menu quedaria: Dashboard, Proceso de pesaje, Entradas, Salidas, Solo Bascula.
   - **Decisión:** D18: menú de Báscula sin «Historial». Hecho (FE `f634510`). Plan: [`plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md`](../f03-bascula/plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md).

2. Al ingresar el numero de documento y encontrar una coicidencia, lo selecciono y se muestra el deposito, al borrar el ultimo numero en el numero y volver a escribirlo y seleccionarlo se pone en el input del numero de documento la infromacion del deposito. [Imagen del error](./imagenes-hallazgos/Screenshot%202026-11-24%20at%209.58.50 PM.png)
   - **Decisión:** D4: el campo muestra solo el número. Hecho (FE `c70a736`). Plan: [`plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md`](../f03-bascula/plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md).

3. En la información del depósito que se muestre, adicional a lo actual, la placa de los camiones. Este detella del deposito se puede mostrar como estaba anteriormente. Adcional hay un error al tratar de seleccionar "Es otro documento: crear depósito nuevo" no queda seleccionado, se devulve al valor anterior.
   - **Decisión:** D5: tarjetas con placas, sin preselección, y «Es otro documento» con su valor. Hecho (FE `c70a736`). Plan: [`plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md`](../f03-bascula/plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md).

4. El campo "No de manifiesto" y "P.Manifiesto" al seleccionar un tipo de documento diferente a "Carta Porte" esos campos desaparecen, la solicitud era que esos campos no eran obligatorios y que siempre estuvieran disponibles, cambia la obligatoriedad dependiendo del tipo de documento seleccionado.
   - **Decisión:** D6: manifiesto siempre visible, obligatorio solo con carta porte. Hecho (FE `c70a736`). Plan: [`plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md`](../f03-bascula/plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md).

5. Estaba llenando los datos del formulario `/operations/weighbridge/process/ca83322f-57a6-40e0-bc3d-e331573e2187?duplicar=1` los tenia completados para guardar pero antes precione "Duplicar entrada" y la información que habia completado se desaparecio y no veo el duplicado en la cola. debe duplicarlo pero no abrirlo inmediatamente. Debo quedar en el registro actual para poder guardar.
   - **Decisión:** D7, D10, D11: duplicada pendiente en el backend (C-F03-53 y C-F03-54) y en la cola; el registro no cambia de página. Hecho (BE `30c2147`, FE `c70a736`). Plan: [`plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md`](../f03-bascula/plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md).

6. La opción de cerrar el ciclo sin repesaje debe estar disponible tambien en `/operations/weighbridge/process/{id}`en el header para los repesajes. Actualmente debo ir hasta el historial de la entrada para cerrar el ciclo sin repesaje.
   - **Decisión:** D8: «Cerrar sin repesaje» en el encabezado del paso Repesaje. Hecho (FE `c70a736`). Plan: [`plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md`](../f03-bascula/plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md).

7. En el drawer de detalle de un ciclo de bascula `/operations/weighbridge/history?id=b68db780-a28b-434b-a4d2-a9244e762e8a` ¿Es posible mostrar los valores del el repesaje? 
   - **Decisión:** D14: «Pesajes del ciclo» en el detalle (respuesta del usuario: «Lista de pesajes»). Hecho (FE `f634510`). Plan: [`plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md`](../f03-bascula/plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md).

8. Al editar un ciclo completado, cambie el "P.Indicador (Kg)" sale el siguiente error: status:400, descripcion: "Indique la tara del repesaje.", Endpoint:"http://localhost:5281/api/v1/weighbridge/entries/b68db780-a28b-434b-a4d2-a9244e762e8a".
   - **Decisión:** D9: la corrección envía la tara real del repesaje. Hecho (FE `c70a736`). Plan: [`plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md`](../f03-bascula/plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md).

9. En los Drawers derrogar la regla de los botones del footer, genera confusión al buscarlos. dejar todo en el menu en el boton que aparece en el header del drawer aplica para toda los drawers de la app.
   - **Decisión:** D12: toda acción del drawer en el menú del encabezado, en toda la app; deroga `PAJ/` D3. Hecho (FE `f634510`). Plan: [`plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md`](../f03-bascula/plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md).

10. Actualmente si tengo un ciclo con "Req. 2 pesaje" para soltarlo debo entrar nuevamente a edicion del ciclo para desmarcarlo, agregar una acción rapida en la "Acciones" de la tabla y el detalle en el drawer, al igual que repesar.
   - **Decisión:** D13, D15: «Cerrar sin repesaje» en el menú de fila de los historiales y en el drawer. Hecho (FE `f634510`). Plan: [`plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md`](../f03-bascula/plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md).

11. En el drawer del detalle de un ciclo en el historial, en la sección de "Pesaje en báscula" aparece el boton de "Editar pesajes", quitar ese boton y dejar la opción de editar en el menu del header.
   - **Decisión:** D13: «Editar pesajes» sale de la sección; «Editar» va en el menú del encabezado. Hecho (FE `f634510`). Plan: [`plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md`](../f03-bascula/plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md).

12. En las tablas de historial del ciclo de pesaje, el peso del manifiesto agruparlo tambien en la columna de "Pesos (Kg)" como "P. Manifiesto" y en acciones utilizar el mismo tipo de boton que se usa en las tablas del modulo de "Configuración". Esto ultimo tambien aplica para la tabla de  `/operations/entries/history` y para todas las tablas de la aplicación. 
   - **Decisión:** D16, D17: «P. manifiesto» en «Pesos (kg)»; se conserva el menú de más de tres acciones y su botón toma el borde de Configuración (respuesta del usuario). Hecho (FE `f634510`). Plan: [`plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md`](../f03-bascula/plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md).

13. Para las operaciones de "Solo Bascula" tambien debe haber la opción de "Cerrar ciclo sin repesaje" en caso que el registro se haya ingresado con "Req. 2 pesaje" marcado
   - **Decisión:** D8: «Cerrar sin repesaje» también en solo báscula. Hecho (FE `c70a736`). Plan: [`plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md`](../f03-bascula/plan-cerrado-f2-f03-ajustes-qa-2026-11-24.md).