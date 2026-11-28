# Hallazgos de la QA manual de F06 integrada

> **Fecha:** 2026-11-27. Prueba del usuario sobre F06 integrada en `fase-2` (I-06, BE `335eb25`, FE `3069cb7`), contra el backend local.
> **Plan que los atiende:** [`../f06-salidas/plan-cerrado-f2-f06-ajustes-qa-2026-11-27.md`](../f06-salidas/plan-cerrado-f2-f06-ajustes-qa-2026-11-27.md).

1. Al generar una nueva «salida de mercancía», unificar las dos observaciones (la del formulario y la de «Confirmar y emitir guía») para que el operario no tenga que llenar dos veces ese campo. Que la guía tome la del formulario principal.
2. En el modal de confirmación de la salida, permitir que el usuario escoja el firmante de la guía: «¿Quién firma la guía de salida?» con dos opciones, «Importador» y «Conductor». Quitar el campo de observaciones del modal.
3. Rediseñar el modal «Confirmar salida» con el mockup [`modal-confirmar-salida/`](modal-confirmar-salida/) («Modal confirmar salida — rediseño@1x.png»). Para esto también se rediseña el formulario de cobro, que es un componente compartido, con el mockup [`formulario-cobro-compartido/`](formulario-cobro-compartido/) («Componente compartido — Cobro de la guía@1x.png»). El formulario rediseñado cambia en todas las vistas donde se muestra.
