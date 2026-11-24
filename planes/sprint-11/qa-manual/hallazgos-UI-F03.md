# Hallazgos UI - Fase 03 - Bascula

1. De acuerdo a P-TR-01 · Menú por rol (propuesta), El historial se debio dividir en 3 secciones:
   - Entradas
   - Salidas
   - Solo báscula

2. `operations/weighbridge` - Proceso de pesaje:
   - La tabla no sigue las reglas general, los filtros deben ir en la columna, en este caso se debe eliminar el filtro de búsqueda global y agregar el filtro por placa en la columna correspondiente
   - Las placas de la tabla ponerlas en tags que faciliten la lectura.
   - Los filtros de estado cambiarlos por tabs de primeVue. 
   - Los botones de acciones para esta tabla y como regla global deben ser de tamaño small
   - La etiqueta de "Duplicada" ocupa mucho espacio, poner solo un tag al lado de la placa con la inicial "D".
   - Para mejora la lectura de los pesos y el tamaño de la tabla, agrupar las columnas P.Bruto, P.Mercancía y tara en una sola columna llamada "Pesos (Kg)" y por cada registro mostrar en esa columna los valores de las tres columnas en una linea por peso, con el label en negrita y el valor mas pequeño en texto muted.

3. `/operations/weighbridge/process/` - Formulario de registro:
   - En el panel de "CAMIONES EN COLA", poner un scroll vertical par que muestre maximo 4 registros y los filtros de 
   - El apartado de camiones en cola esta saturando mucho la vista, tiene demaciados bordes y el boton de "Cargar a báscula" ocupa mucho espacio y los filtros "Todos", "Repesar" y "Por pesar" no cubre todos los estados. Propongo rediseñar este panel con las siguientes caracteristicas: 
        - Eliminación de tarjetas anidadas y botones redundantes: Se removieron los contenedores individuales con bordes pesados y todos los botones "Cargar a báscula ->", dejando una lista continua dentro de un único contenedor con divisores sutiles de 1px.
        - Filas directamente clicables: Cada camión en la cola funciona como una fila interactiva (hover suave) con dos líneas de información clara:
          - Línea 1: Placa en negrita a la izquierda y badge de estado (En atención, Por repesar, Sin iniciar, Por cobrar) a la derecha.
          - Línea 2: Resumen breve (mercancía) y tiempo de espera en texto gris tenue.
        - Resaltado del camión activo: El turno actual (ABC123) se distingue con un fondo azul suave y borde izquierdo activo (border-l-4), facilitando la lectura rápida bajo presión.
        - Para evitar el scroll de la pagina principal, se agregó un scroll vertical al panel de "CAMIONES EN COLA" con un maximo de registros tal que ocupe la altura del formulario principal.

4. Para los estados de repesaje, actualmente se abre un modal sobre el formulario, esto genera confusión, cambiar mejor el formulario del repesaje en el modal a una pagina en el espacio del formulario de registro. 

5. Para el historial
    - las placas del vehiculo mostrarlas en un tag. 
    - Los pesos (P.Bruto, P.Mercancía y tara) agruparlos en una sola columna llamada "Pesos (Kg)" y por cada registro mostrar en esa columna los valores de las tres columnas en una linea por peso, con el label en negrita y el valor mas pequeño en texto muted.
    - Conductor y ID Conductor agruparlos en una sola columna.
    - El Doc. Entrada esta agrupado el tipo y el numero, pero se muestran en una sola linea lo que dificulta la lectura, separarlos en dos lineas.
    - Los tag de "Duplicado" Mostrar solo la inicial "D" en un tag pequeño.
    - Para esta tabla y como regla general para todas las tablas, para las acciones si un registro de una tabla puede llegar a tener mas de 3 acciones, se debe usar un menu desplegable y agrupar todas las acciones en el menu (Como la regla del drawer)

    
**Dudas**

1. `/weighbridge/history` ¿En el historial los ciclos con estado "Completado" ya no se pueden editar?, si es si, agregar un campo solo para los completados que permita al oporario agregar una observación que llega a CE. 

---

**Decisiones** (plan [`plan-cerrado-f2-f03-ajustes-ui-2026-11-24.md`](../f03-bascula/plan-cerrado-f2-f03-ajustes-ui-2026-11-24.md), ejecutado el 2026-11-24, FE `7eb7cfc` y `ee3d5d9`):

1. **Historial en tres secciones:** las tres páginas ya existían desde FE-3. I-03 las enlaza como submenú «Historial ▸ Entradas, Salidas, Solo báscula» (D16).
2. **Proceso de pesaje:** hecho. Sin búsqueda global; filtros de placa y conductor en la columna; estados en pestañas con contador; placa en etiqueta con «D»; «Pesos (kg)» (D7 a D9). Los botones de acción ya eran `small`, y la regla queda en la convención (D5).
3. **Panel «Camiones en cola»:** hecho como se propuso. Los cinco estados van en un selector con contador (D4, D10 y D11).
4. **Repesaje:** hecho. Es un paso de la página de proceso y no un modal; «Repesar» del historial, del detalle y de `cycles/[id]` también lleva a él (D1, D12 a D14).
5. **Historial:** hecho. Placa en etiqueta con «D»; pesos agrupados (también en Salidas y Solo báscula); conductor y documento en una columna, con un filtro por nombre o documento; documento de entrada en dos líneas; acciones en el menú «Acciones» si la tabla puede tener más de tres, como regla general (D3, D6 y D15).

**Duda 1:** no se agrega el campo de observación para CE (D2). Los completados se corrigen con motivo: en Entradas, mientras el depósito esté en Borrador; en Salidas y Solo báscula, siempre. Con el depósito confirmado corrige CE (P-CE-03, F05).

