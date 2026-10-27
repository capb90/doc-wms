# Preguntas frecuentes de los operarios

> **Para qué sirve:** reúne las dudas reales de los operarios durante las pruebas en staging, cada una con la respuesta que se les dio. Es la referencia para responder la próxima vez y será la base de conocimiento de un asistente automático (por WhatsApp o dentro del WMS), cuando se retome.
> **Origen:** desde el reinicio limpio de staging (`DEC-043`, 2026-10-27), los operarios escriben al WhatsApp del responsable de las pruebas. El responsable pasa cada mensaje al agente y el agente prepara la respuesta.
> **Vigencia:** cada respuesta dice la versión con la que se dio. Si una versión posterior cambia el comportamiento, la respuesta se marca «Desactualizada» y se agrega la nueva. No se borra.
> **Datos personales:** sin nombres de operarios, conductores ni clientes, ni documentos o placas reales. Se escribe el rol y, si hace falta, un ejemplo ficticio.

## Cómo se agrega una pregunta

- **Una entrada por duda,** con la pregunta generalizada en palabras del operario: «¿Cómo corrijo un peso?», no «¿cómo corrijo el peso del camión de esta mañana?».
- **Si la duda ya está,** no se repite. Se suma en el registro del final y, si hace falta, se mejora la respuesta.
- **La respuesta va lista para reenviar:** en español sencillo, con el menú y los botones tal como se ven en pantalla.
- **Los fallos y los ajustes no van aquí,** sino en su ficha de defecto (`qa/plantillas/defecto.md`). Solo se anotan en el registro.

Formato de cada entrada:

```markdown
### P-NNN · ¿Pregunta?

- **Rol:** Báscula · **Pantalla:** Báscula → Proceso de pesaje
- **Tipo:** Duda de uso | Regla del sistema
- **Fecha y versión:** 2026-10-27 · BE `911399c` / FE `33fbeba`
- **Fuente:** la decisión, el manual o la regla del código que respalda la respuesta

**Respuesta:**

Texto para el operario.
```

## Vigilancia

*Sin preguntas todavía.*

## Báscula

*Sin preguntas todavía.*

## Bodega

*Sin preguntas todavía.*

## Comercio Exterior

*Sin preguntas todavía.*

## Facturación

*Sin preguntas todavía.*

## General (ingreso, contraseña, navegador)

*Sin preguntas todavía.*

## Registro de mensajes

Cada mensaje que llega, aunque repita una duda o sea un fallo.

| Fecha | Rol | Tipo | Resultado |
| --- | --- | --- | --- |
