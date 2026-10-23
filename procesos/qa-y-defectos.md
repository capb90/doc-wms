# QA y defectos

> **Para qué sirve:** cómo se registra, corrige y verifica un defecto, y dónde está cada pieza de la campaña QA.
> **Fuentes:** `qa/00-plan-maestro.md`, `qa/plantillas/`, `qa/plan-correccion-defectos.md` y `qa/resultados/defectos/INDICE.md`.

## 1. Dónde está cada cosa

| Qué | Dónde |
| --- | --- |
| Plan maestro de la campaña (alcance, riesgos §9, **decisiones del negocio §10**) | `qa/00-plan-maestro.md` |
| Casos por fase (F0 humo … F11 regresión y cierre) | `qa/fase-NN-*.md` |
| Plan de corrección (CHG-01…CHG-90, reglas comunes §4.0) | `qa/plan-correccion-defectos.md` |
| Informes por fase y sesión | `qa/resultados/F*-informe-*.md`, `qa/resultados/SEL-informe-2026-10-08.md` |
| Informe final (veredicto GO / NO-GO) | `qa/resultados/informe-final.md` |
| Fichas de defecto e índice | `qa/resultados/defectos/DEF-*.md` e `INDICE.md` |
| Evidencias (capturas, respuestas del API, PDF) | `qa/resultados/evidencias/` y `qa/resultados/muestras-f*/` |
| Datos de prueba usados | `qa/resultados/registro-datos-qa.md` y `registro-datos-qa-f11.md` |
| Defectos de la migración a staging | `planes/migracion-staging/resultados/defectos/DEF-MIG-*.md` |
| Plantillas (defecto, informe de fase, registro de datos) | `qa/plantillas/` |

## 2. Identificadores

| Prefijo | Significado |
| --- | --- |
| `DEF-F{N}-{nnn}` | Defecto de producto hallado en la fase N de QA. Los nuevos de cualquier origen siguen en `DEF-F11-028` en adelante |
| `DEF-MIG-{nnn}` | Defecto de la migración del legacy. El siguiente es `DEF-MIG-009` |
| `F{N}-{ÁREA}-{nnn}` | Caso de prueba (p. ej. `F3-CAM-013`) |
| `CHG-nn` | Cambio del plan de corrección |
| `OBS-*`, `O-n` | Observación sin ficha |
| `PRF-nnn` | Prueba de rendimiento (p. ej. `PRF-002`, cronometraje de báscula) |

Antes de numerar un defecto nuevo, revisa `INDICE.md` y las fichas más recientes.

## 3. Ciclo de vida

```
Nuevo → Confirmado → En corrección → Corregido → Verificado
                                         └──→ Reabierto ──┘      (o Rechazado / Duplicado)
```

- **Quien lo encuentra** crea la ficha con `qa/plantillas/defecto.md`: pasos, resultado esperado con la regla que lo sustenta, resultado obtenido literal, evidencia, impacto, ambiente y commits FE/BE. La agrega a `INDICE.md` con una nota fechada.
- **Quien lo corrige** cambia el estado a «Corregido» e indica commit base, cambio hecho y lista de verificación.
- **Quien hace el re-test** lo pasa a «Verificado» o «Reabierto», con la evidencia del re-test.
- **Severidades:** BLOCKER, CRITICAL, MAJOR, MINOR, TRIVIAL. Si el usuario cambia una severidad, se anota en la ficha.

## 4. Reglas

- Las **decisiones del negocio** (§10 del plan maestro y `contexto/decisiones.md`) mandan sobre lo que diga una ficha.
- Sin contraseñas ni datos de personas reales en fichas e informes: usa las cuentas de prueba por su nombre de usuario, y los datos de práctica o QA por su código.
- Las consultas SQL de verificación son de solo lectura y solo en la base local.
- En staging, el agente no escribe contraseñas en el navegador: el usuario inicia sesión y el agente usa esa sesión.
- Un hallazgo de rendimiento o de entorno que no es defecto va como observación en el informe, no como ficha.
