# Hallazgos UI - F04 Bodega

1. `/warehouse/receptions`: En acciones cuando un montacargas esta en proceso, para un registro, por ejemplo el "ABC123" el usuario tenga la opción de finalizar el uso desde esa misma pagina, se abre el modal desde aqui. 

2. `/warehouse/receptions`: En el modal de "Recepción física de mercancía", Quitar los avisos "Activo: la ubicación de todos los productos es «Sobre vehículo» y el cobro usa la tarifa por vehículo si el acuerdo la tiene." y "Una cuadrilla por recepción. Ubicación obligatoria por producto descargado. Con unidades de carga, cada unidad se marca «Recibida completa» en lugar de cantidades."

3. `/warehouse/forklift`: Poner el boton de "+ Registrar Uso" en la esquina derecha para que los tabs queden ubicados desde la esquina izquierda.

4. En el modal de "Facturación y Cobro - Montacargas" Cambiar el mensaje de "Sin IVA · pago inmediato; registro interno sin factura («No aplica»)." por "Sin IVA · pago inmediato" y "IVA del 19 % · pendiente por facturar; Facturación le pone el número." por "IVA del 19 % · pendiente por facturar".

5. Organizar mejor las secciones del mdal de "Facturación y Cobro - Montacargas" se suguiere este [mockup](./modal-facturacion-montacargas/)

6. `/warehouse/inventory`: Los tabs de "Existencias", "Movimientos" y "Ubicaciones" deberian estar en la card de la tabla principal no en una card separada.

7. `/warehouse/novelties`: El check de "Incluir anuladas" deberia estar en la card de la tabla principal a lado izquierdo del boton "Exportar".

8. En Registrar novedad en registro fotografico es un input normal, ¿deberia dejar subir fotos?