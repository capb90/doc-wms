# Hallazgos integración F05

Para realizar este QA realice un flujo completo desde vigilancia, tomando datos del legacy.

1. En Bascula `/operations/weighbridge/process/01ff1b84-d755-4ddf-84b4-61f85da3f88e?paso=registro` el flujo de agregar un producto nuevo es confuso, escribo el nombre del producto y al perder el enfoque del input, se pierde la información ingresada. Mejor implementar un modal para agregar productos nuevos, el boton de "+" abre el modal con los campo Nombre y Embalaje se crea, se cierra el modal y se precarga la información en los select. Tambien en el listado mostrar el nombre y el embalaje del producto en el listado de opciones.

2. En detalle del deposito -> Etapa Entradas: La información de "Ver pesaje" que se muestra en `/operations/weighbridge/cycles/697a84eb-64d0-4d09-85dc-00ac85e07e44` mostrarla en un drawer como información de solo lectura, y las opciones de esa pagina de "Repesar", "Anular" mostrarlas en el menú de acciones.

3. En `/foreign-trade/entries/ea356ba8-dfb9-4743-a72f-43b2358bd6f8?volver=/foreign-trade/imports/5f3749d2-6058-4f58-91e9-45d53f832b41`: 
    - el switch de "Unidad de carga" se active solo al darle click al switch, no al hacer click en el label o fuera de él. 
    - En esta misma vista quitar el campo de "Motivo de la corrección" este campo llenarlo automaticamente por abajo para no tocar el backend.
    - En el header, la placa hacerla mas visible, puede ser en un tag.

4. En el detalle del deposito en el header el tag del estado del deposito cuando esta "Confirmado" mostrarlo en verde. En la informacion general en el header agregar el numero y tipo de documento comercial

5. En detalle del deposito -> Etapa Levantes: La cantidad acepta decimales, para este deposito `/foreign-trade/imports/5f3749d2-6058-4f58-91e9-45d53f832b41?etapa=levantes` el legacy no muestra decimales por ejemplo en la version 2 la cantidad nacionalizada y del levante muestra "640.13" pero el legacy muestra "640" y para el saldo igual, en v2 muestra "1279,87" pero el legacy muestra "1280" al parecer hay redondeo en el legacy.

6. Los estados aduaneros de importacion son solo dos: "Sin nacionalizar" y "Nacionalizado". no existe "Nacionalización parcial" quitarlo (Actualmente aparece esta etiqueta en el header del detalle del deposito). Si el deposito tiene al menos 1 levante se pone como "Nacionalizado"

7. El boton de "+ Nuevo levante" de la tabla de levantes tanto en el detalle del deposito como la vista 2 `/foreign-trade/releases` Al parecer no cumple ninguna funcion porque la fila de la tabla se agrega automaticamente, si es asi quitar ese boton. En esta misma tabla en la columna de acciones agregar un margin entre los botones para que no queden pegados.

7. Para toda la APP y PDFs: Actualmente se maneja el "punto (.)" como separador de miles y la "coma (,)" como separador de decimales, cambiar a "punto (.)" como separador de decimales y "coma (,)" como separador de miles.

8. Ajustes PDFs:
    - En las tarjetas que se generan por vehículo no aparece de DATOS DE NACIONALIZACION con los levantes. Tambien el "Manifiesto No" que debe mostrar es el Manifiesto Dian con la fecha.
    - En la tarjeta por vehiculo y por deposito la sección de "Unidad(es) de carga" se muestra solo cuando hay valor, ahora siempre se muestra con un "N/A"
    - Para las tarjetas tanto de deposito como por vehiculo propongo un rediseño del formato pdf, pero no eliminar el actual, debe ser aditivo, de tal forma que por configuración se escoga si utilizar el formato legacy o el nuevo que proponemos. [mockup](./formato-etiqueta-v2/) Es una propuesta de rediseño hecho con IA.
    - PDF del depósito: 
        - Los datos del importador no se estan mostrando, aparece "Sin cliente"
        - En la tabla de descipción del ingreso a Bodega la columna "Peso Kg" no muestra nada, debe mostrar el peso de la mercancía "P.mercancía" de las entradas
        - En la columnas de cantidades se muestran todas el mismo valor por ejemplo "1920" puedes revisarlo para este deposito `http://localhost:3000/foreign-trade/imports/5f3749d2-6058-4f58-91e9-45d53f832b41`. aqui deberia indicar como en el legacy la cantidad total de entrada, la total amparada y el saldo
        - El "TOTAL PESO (KG)" se muestra siempre en 0
        - Para este documento tambien propongo un rediseño mas moderno, Organizado y limpio [mockup](./pdf-deposito-v2/). debe ser aditivo, de tal forma que por configuración se escoga si utilizar el formato legacy o el nuevo que proponemos
    - PDF Guia de salida:
        - No se muestra la Dirección de importador - Validarlo (Falta verificar si el importador tiene dirección configurada)
        - Los "Tiquetes" no se muestran.
        - En Agencia de aduanas despues del valor entre paréntesis aparece nuevamente el texto "Agencia de aduanas"
        - En la tabla quitar la columna de "Unidad"
        - Verificar si en la columna Levante y Aceptación se listan todos los levantes y las aceptaciones.
        - El codigo QR aparece centrado, debe aparecer a la izquierda.
        -  Para este documento tambien propongo un rediseño mas moderno, Organizado y limpio [mockup](./formato-guia-v2/). debe ser aditivo, de tal forma que por configuración se escoga si utilizar el formato legacy o el nuevo que proponemos
    
    **Notas**: Estos modelos de formatos fueron hechos con IA, la idea es generar unos formatos mas modernos, organizados y limpios, pero son eliminar aun los formatos legacy, se debe seleccionar por configuracion o parametros que formatos utilizar. El formato del PDF del deposito y la guia de salida, el footer y el encabezado deben ser los mismos para mantener la consistencia. El logo puedes utilizar los que estan en el frontend y que mejor se ajusten.


9. ¿La planilla de envío que se genera desde las acciones en el detalle del deposito donde se la puede ver o que hace esta opcion?