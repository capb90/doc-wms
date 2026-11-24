# Hallazgos F01 y F02

Estos son los hallazgos encontrados durante la QA manual de las features F01 y F02.

1. Los botones de acciones deben tener Tooltip que muestren una descripción al pasar el mouse sobre ellos.
2. El boton de "Ver" Quitar el texto, dejarlo como los otros botones, solo icono con el tooltip recomendado en 1.
3. `/admin/stakeholders`: El Drawer de detalle de un "Tercero" se ve muy mal, hay que mejorar el diseño. propongo este mockup como referencia [mockup](./drawel-detalle-terceros/). La gesition de acuerdos ya no se va a manejar desde el detalle de un tercero, ¿La gestion de acuerdos se elimina en las siguientes fases?.
4. `/admin/services`: El Drawer de detalle de un "Servicio" se ve muy mal, hay que mejorar el diseño. Propongo este mockup como referencia [mockup](./drawer-detalle-servicios/). La gestion de tarifas base ya no se va a manejar desde el detalle del servicio, ¿La gestion de tarifas base se elimina en las siguientes fases?. Y el formulario de "Crear tarifa base" se debe rediseñar de forma similar a la propuesta presentada para acuerdos de clientes. 
5. `/admin/drivers`: El drawer de detalle de un conductor tambien se debe rediseñar utilizando como base los estilos que se implementen en los drawers de tercero y servicio.
6. `/admin/cities`: El boton de importar tiene un tamaño diferente al de los demas botones, se debe ajustar para que sea consistente con el resto. Y el modal de "Importar ciudades del legacy" esta mal distribuido los campos del formulario, el boton de Seleccionar CSV cambiarlo por un tipo "Dropzone" o "InputGroup"
7. `settings/prefixes`: En la columna prefijo de la tabla poner un tag para deiferenciar de la columna de Ejemplo al digitar es confuso para el usuario nuevo, el prefijo en el ejemplo mostrarlo de otro color que resalte
8.  `/admin/users`: El drawer de detalle de un usuario se ve muy mal, hay que mejorar el diseño. Propongo este mockup como referencia [mockup](./drawer-detalle-usuario/)
9. '/admin/audit': El drawer de detalle de audit se debe mejorar, siguiendo las convenciones de los otros drawers rediseñados de los puntos anteriores
10. En general el drawer debe rediseñarse, para las vistas aqui revisadas y las futuras, manteniendo una consistencia visual. 

**Nota**: Los mockups dueron diseñados con IA, por lo que pueden no ser 100% realistas, pero dan una idea de como deberian lucir los drawers.