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
---

## Resolución (2026-11-24)

Plan: [plan-cerrado-f2-f02-ajustes-qa-2026-11-24.md](../f02-base/plan-cerrado-f2-f02-ajustes-qa-2026-11-24.md). Fusionado en `fase-2` del frontend (`5793bc9`).

| Hallazgo | Decisión | Estado |
| --- | --- | --- |
| 1. Tooltips en los botones de acción | D6 | Corregido (fase 1) |
| 2. «Ver» de solo icono | D7 | Corregido (fase 1) |
| 3. Drawer de Terceros; ¿se eliminan los acuerdos del detalle? | D8; D1: sí, F07 los pasa a «Tarifas y acuerdos» y los quita del detalle; hasta entonces siguen en su tarjeta | Corregido (fase 2) |
| 4. Drawer de Servicios; ¿se eliminan las tarifas base del detalle?; formulario «Crear tarifa base» | D9; D1: sí, en F07; D2: el formulario se rediseña en F07 con el patrón de «Agregar tarifa» (P-FAC-13) | Corregido el drawer (fase 2); formulario en F07 |
| 5. Drawer de Conductores | D10 | Corregido (fase 3) |
| 6. Ciudades: botón «Importar» y modal de importación | D13 | Corregido (fase 1) |
| 7. Prefijos: etiqueta y resaltado del ejemplo | D14 | Corregido (fase 1) |
| 8. Drawer de Usuarios | D11 y D3 (más de dos acciones: todas en el menú del encabezado) | Corregido (fase 3) |
| 9. Drawer de Auditoría | D12 | Corregido (fase 3) |
| 10. Consistencia de los drawers | D5 y D15: anatomía única, escrita en `contexto/convenciones-tecnicas.md` §3 y en la galería `/dev/components` | Corregido |
