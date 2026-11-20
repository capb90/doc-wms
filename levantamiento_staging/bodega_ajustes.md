## Bodega ajustes:

## Recepcion:

1. En recepcion eliminar la pagina de ingreso, solo dejar la recepcion, todos los registros de ingresos pasan a recepcion directamente.
2. El menu cambiar el nombre de "Recepciones" a "Entradas" y los subitems serian "Recepción" e "Historial"

## Montacargas:

1. En el historial de montacargas, la facturación solo debe mostrar la cantidad pagada y si fue o no facturado. Esta información es relevante solo en facturación, aca solo es informativo.

## Recepción directa:

1. El modal de recepción directa sin bascula esta solicitando información que no se puede completar en bodega. en el mockup `docs/levantamiento_staging/mockups/recepcion_directa_bodega` se encuentra los campos que debe contener. Y se debe migrar a una pagina independiente no un modal.

## Ordenes de cargue (Salidas):

1. Debe cambiar el nombre a Ordes de salida, ya no se maneja el concepto de ordenes de cargue.
2. Aqui deben aparecer todas las salidas sin importar el tipo: "Por tiquete de entrada", "Global", "Por número de depósito" y "Consolidada"
3. para las salidas "Por tiquete de entrada" y "Global" que no realizan cargue el operario debe regitrar la salida de patio
4. para las salidas "Por número de depósito" y "Consolidada" el operario registra el cargue y llena los datos correspondientes a cantidades.
5. Aqui solo deben listar las salidas en estado "Confirmada"
6. El mockup `/Volumes/Dock/Projects/bodegas_asociadas/code_workspace/docs/levantamiento_staging/mockups/orden_de_salida_bodega` muestra como deberia verse el modal de ejecutar la salida para el caso de "Por número de depósito" y "Consolidada", para los casos de "Por tiquete de entrada" y "Global" se debe ajustar con los campos necesarios y una accion rapida para registrar la salida de patio.
7. En el menu deben estar seguidas de "Entradas" y con el nombre "Salidas" y los subitems "Ordenes de Salida" e "Historial". En "Ordenes de Salida" solo se muestran las pendientes. El historial se debe manejar con tabla
