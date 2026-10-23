# Ficha de defecto — DEF-F{N}-{nnn}

> Un archivo por defecto en `docs/qa/resultados/defectos/`, o una fila por defecto en la herramienta que el usuario indique (Linear, equipo Wms). Sin contraseñas ni datos personales reales.

| Campo | Valor |
|---|---|
| ID | DEF-F{N}-{nnn} |
| Título | Verbo + qué falla + dónde (≤ 90 caracteres) |
| Severidad | BLOCKER / CRITICAL / MAJOR / MINOR / TRIVIAL |
| Prioridad sugerida | Alta / Media / Baja |
| Módulo | Administración / Vigilancia / Báscula / Bodega / Comercio Exterior / Facturación / Transversal |
| Caso(s) | F{N}-XXX-nnn |
| Riesgo del plan (§9) | R-XXX-nn o «nuevo» |
| Ambiente y commits | Local/Staging · FE `xxxxxxx` · BE `xxxxxxx` |
| Rol / usuario | |
| Estado | Nuevo / Confirmado / En corrección / Corregido / Verificado / Reabierto / Rechazado |

## Precondiciones y datos
(IDs, números de depósito, placa, factura… del registro de datos QA)

## Pasos para reproducir
1.
2.
3.

## Resultado esperado
(cita la regla: decisión, criterio del caso o mensaje esperado)

## Resultado obtenido
(texto literal del mensaje; estado final de los datos)

## Evidencia
- Captura(s):
- Petición: `MÉTODO /api/v1/...` → código, cuerpo resumido
- Consola del navegador:
- Consulta SQL de verificación (solo local, solo lectura):

## Impacto
(dinero, stock, pesos, permisos, operación detenida, frecuencia)

## Pista técnica (opcional)
(archivo:línea si el ejecutor la conoce; no es obligatorio)

## Historial
| Fecha | Evento | Build | Por |
|---|---|---|---|
