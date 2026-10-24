# 08 — Auditoría del análisis inicial

> **Fecha:** 2026-10-23. Auditoría estática. Consolida la sección «Contraste con el análisis anterior» de los 8 `modulos/<NN>-<modulo>/resultado-agente.md`.
> **Qué se evalúa:** la matriz `bodegas-legacy/docs/legacy_analysis/MIGRATION_MATRIX.md` (código del 2026-09-24, BE `b089d2b` / FE `26aed68`, decisiones del 2026-09-29) y las afirmaciones de los planes de paridad, las decisiones y los documentos de estado (inventario en `00-evaluacion-analisis-existente.md`).

## 1. Clasificación

- `CONFIRMADA_EN_CODIGO`: la afirmación sigue siendo cierta en el código actual.
- `OBSOLETA`: era cierta en su fecha y el código cambió después, casi siempre porque un plan de paridad la cerró. **No es un error del análisis.**
- `INCOMPLETA`: es cierta, pero omite algo relevante.
- `CONTRADICHA_POR_CODIGO`: el código la desmiente. Es un error, o una regresión posterior.
- `NO_VERIFICADA`: el código no permite concluir.

## 2. Estados de `MIGRATION_MATRIX.md` (263 capacidades)

| Módulo | N | Confirmada | Obsoleta | Incompleta | Contradicha |
| --- | ---: | ---: | ---: | ---: | ---: |
| 01 Administración y catálogos | 98 | 68 | 11 | 16 | 3 |
| 02 Báscula | 22 | 9 | 6 | 7 | 0 |
| 03 Vigilancia y Bodega | 16 | 8 | 7 | 0 | 1 |
| 04 CE: ingresos y depósitos | 24 | 12 | 8 | 4 | 0 |
| 05 CE: levantes y salidas | 28 | 14 | 11 | 3 | 0 |
| 06 Facturación | 22 | 6 | 6 | 10 | 0 |
| 07 Reportes | 15 | 4 | 8 | 2 | 1 |
| 08 Procesos y excluidas | 38 | 36 | 1 | 1 | 0 |
| **Total** | **263** | **157** | **58** | **43** | **5** |

**De las 202 evaluadas** (sin las 61 excluidas): 97 confirmadas (48 %), 58 obsoletas (29 %), 42 incompletas (21 %) y 5 contradichas (2,5 %). Ninguna quedó `NO_VERIFICADA`.

**Las 61 exclusiones** (Colmotores y acceso) están bien hechas en 60 casos: no quedan restos ni dependencias de Colmotores en V2 (módulo 08, `05-analisis-v2.md` §8). La excepción es `CF-L217`, la sesión del portal: además de Colmotores servía a las agencias de aduanas, cuya consulta de ingresos no era de Colmotores (BR-08-008, INCOMPLETA).

### 2.1 Las 5 contradicciones

| Capacidad | Decía | El código actual | Fuente |
| --- | --- | --- | --- |
| `CF-L032` Eliminar embalajes | «Borrado físico bloqueado si está en uso por productos» | Solo bloquea por productos de depósito; los del catálogo pierden el embalaje (FK `SetNull`), sin auditoría | Módulo 01, BR-01-001 |
| `CF-L101` Requisitos de modalidad | La relación documento–modalidad está sembrada | Los 6 tipos se siembran con `OperationModalityId` nulo (`SeedDataExtensions.cs:299-370`) | Módulo 01 |
| `CF-L244` Selector de productos | CUBIERTA con el selector de productos | Es el grupo de alias de vehículos de Colmotores (`mod_productos/selecciongrupo.php:7`): `NO_APLICA` | Módulo 01 |
| `CF-L230` Portería | «Vigilancia registra la salida sin comprobar guía ni ciclo completo» | La salida se bloquea con un pesaje abierto (CHG-30) y con una orden de importación sin guía (CHG-33) (`EntryLogDepartureGuard.cs:20-40`) | Módulo 03 |
| `CF-L258` Código de barras | «Code128 en etiquetas, depósito y guía» | Depósito y guía usan Code 39 (`DepositPdfService.cs:546-567`, `DispatchGuidePdfService.cs:784-805`) | Módulo 07 |

`CF-L230` es una mejora posterior (QA). Las otras cuatro son imprecisiones del análisis original.

### 2.2 Lo que el análisis anterior no miró

Las 42 `INCOMPLETA` tienen un patrón común. El análisis comparó capacidades, pero no recorrió los siguientes aspectos:

- **Campos y unicidad:** fichas de terceros, conductores y vehículos con datos sin destino ni decisión, y la placa única sin país (BR-01-004, BR-01-005).
- **Bajas con registros asociados:** el legacy las bloqueaba con el error 8 y V2 las permite (BR-01-006).
- **Casos borde de varios camiones y documentos:**
  - un solo pesaje por camión en el legacy, uno por depósito en V2 (BR-02-013);
  - el camión tardío a un depósito agotado (BR-04-001).
- **Concurrencia y transacciones:** las reservas sobre el tope de lo nacionalizado (BR-05-002).
- **Vigencia de convenios y tarifas:** los convenios programados que no se activan (BR-06-001) y la tarifa faltante de un servicio complementario (BR-06-004).
- **Integración y contratos:** la dimensión no existía. Esta auditoría encontró 9 brechas `CONTRATOS_API` en 16 capacidades, 2 pantallas `SOLO_MAQUETADO` y 5 capacidades sin integración.

Tampoco estaban en el catálogo **13 capacidades legacy** (`CF-LX`). Las más relevantes:

- el bloqueo manual de salidas por cliente (`cliente.sinsalidas`, `CF-LX05-01`);
- la guía solo con el cargue completo (`CF-LX05-02`);
- la alerta de abandono en el panel (`CF-LX04-01`);
- la alerta de TRM (`CF-LX06-01`);
- la auditoría del inicio de sesión (`CF-LX01-01`);
- la liberación de posiciones al emitir la guía (`CF-LX03-01`).

## 3. Afirmaciones de planes, decisiones y documentos (176)

| Módulo | Confirmada | Incompleta | Obsoleta | Contradicha | No verificada | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 01 | 6 | 1 | 1 | 0 | 1 | 9 |
| 02 | 29 | 2 | 4 | 0 | 5 | 40 |
| 03 | 12 | 1 | 2 | 3 | 0 | 18 |
| 04 | 17 | 2 | 0 | 1 | 3 | 23 |
| 05 | 19 | 0 | 0 | 0 | 3 | 22 |
| 06 | 14 | 2 | 1 | 0 | 1 | 18 |
| 07 | 13 | 6 | 0 | 2 | 0 | 21 |
| 08 | 14 | 6 | 2 | 2 | 1 | 25 |
| **Total** | **124** | **20** | **10** | **8** | **14** | **176** |

Los recuentos por módulo de 01 y 03 a 07 los derivó el orquestador de las tablas de cada `resultado-agente.md` §5; los de 02 y 08 son los del propio agente.

**Las 14 «no verificadas» se resuelven casi todas cruzando módulos:**

| Afirmación | Agente que no la verificó | Agente que la confirma |
| --- | --- | --- |
| F1-04 y F1-07 | 02 | 04 |
| F1-06 | 04 | 02 |
| F2-10 y P6(a) | 04 | 07 |
| F3-01 | 05 | 03 |
| F4-07 | 05 | 02 |
| F6-02 | 01 | 08 |

Quedan sin verificar de verdad, porque no se resuelven con código:

- la medición de báscula ≤ 30 s (DEC-010, DF2, PRF-002);
- la asignación del rol de Vigilancia al operario de báscula (`BASCULA_PARITY.md` §6, configuración de usuarios);
- las tarifas T1–T4 de `DEC-041` (datos de configuración);
- la prueba con S3 real de la fase 6.

### 3.1 Las 8 contradicciones

| Afirmación | Fuente | El código | Ref. |
| --- | --- | --- | --- |
| La fecha de ingreso se corrige «sin límite hacia atrás» | `DEC-012` | Solo dentro de la estadía del primer camión (`WarehouseStorage.cs:212-213`) | BR-04-002 · resuelto el 2026-10-23: el usuario mantuvo el código y DEC-051 precisa DEC-012 |
| El Excel del resumen de pólizas lleva las tres firmas | plan frontend F5-06 | `excel-export.ts:158-166` no pasa `footerLines` | BR-07-005 |
| Excel sin límite y los mismos informes que el legacy | `DECISIONES_REVISION.md` §2.E.18 | El límite se resolvió, pero los diarios de ingreso y salida no tienen Excel | BR-07-001 |
| GAP-004: un camión con mercancía puede salir sin guía | `FUNCTIONAL_GAPS.md` | `EntryLogDepartureGuard` lo impide en importación | Módulo 03 |
| `POST entry-logs` exige `WarehouseAccess` | `BASCULA_PARITY.md` §6 | Exige `GateAccess` (`EntryLogController.cs:20`) | Módulo 03 |
| La recepción actualiza el stock | `Backend/wms-api/Wms.Application/Warehouse/README.md:134`, `GUIA_USUARIO.md:224` | La recepción no mueve stock (`DEC-010`) | Módulo 03 · documentación del repo desactualizada |
| `CF-V085` es el «estado del sistema» | `01-inventario-funcional-global.md` §7 (de esta auditoría) | Es la TRM de la DIAN del día, sin consumidor | Módulo 08 · error del inventario inicial del orquestador, corregido por el agente |
| El Id «que muestra la pantalla de respaldos» | `Backend/wms-api/deploy/staging/README.md:206` | No hay pantalla (DF3); el mismo runbook lo dice en `:160` | Módulo 08 |

### 3.2 «Toda la funcionalidad planeada está implementada» (`docs/contexto/estado.md` §1)

**Casi cierta.** Los ítems de los planes de paridad existen en código y casi todos se confirman. Hay cuatro excepciones:

| Ítem planeado | Estado | Brecha |
| --- | --- | --- |
| F4-04 «Reporte de mercancías» | INCOMPLETA: imprime el depósito como CPI y omite la salida y el tipo de novedad | BR-03-005 |
| `DEC-020` «la factura siempre se genera» | INCOMPLETA: una tarifa faltante de un servicio complementario la bloquea | BR-06-004 |
| GAP-017 Excel de los mismos reportes | INCOMPLETA: los diarios no tienen Excel | BR-07-001 |
| F5-06 (frontend) firmas en el Excel de pólizas | CONTRADICHA | BR-07-005 |

Además quedan pendientes de construir o de decidir **3 capacidades legacy sin implementar**:

- `CF-L139`, modificar el serial de un depósito;
- `CF-LX05-01`, bloqueo manual de salidas por cliente;
- `CF-LX05-02`, guía solo con el cargue completo.

Ninguna de las tres estaba en el plan, porque el análisis anterior no las catalogó o las daba por cubiertas.

## 4. Dictamen sobre el análisis inicial

| Criterio | Valoración |
| --- | --- |
| **Completitud del inventario legacy** | Buena: 263 capacidades con IDs estables que esta auditoría reutilizó sin cambios. Faltaron 13, la mayoría reglas o alertas escondidas en listados y en el panel. El 95 % del universo final ya estaba catalogado |
| **Precisión de los estados** | Alta en lo que miró: 2,5 % de contradicciones sobre 202. Media en la profundidad: el 21 % omitía detalles que hoy son brechas MEDIA o BAJA |
| **Vigencia** | Baja: el 29 % de los estados son obsoletos porque los planes de paridad los cerraron. La matriz anterior **no debe usarse hoy como estado de la migración**; la reemplaza `03-matriz-global.md` |
| **Dimensiones** | Insuficientes para cerrar una migración: no separaba frontend, backend e integración, ni revisaba contratos o endpoints sin consumidor |
| **Decisiones** | Bien registradas y aplicadas. `DECISIONES_REVISION.md` y los §A.3/A.4 de los planes fueron la base de 78 `DIFERENCIA_INTENCIONAL`, y el código las cumple salvo `DEC-012` (BR-04-002, resuelta el 2026-10-23 con DEC-051 a favor del código) y `DEC-020` (BR-06-004) |
| **Porcentaje anterior** | La matriz anterior no daba un porcentaje y advertía que el recuento no mide el avance. **El 90 % estimado no surge de ningún documento:** el más cercano es el 82 % de «cubiertas salvo detalles menores» de esta auditoría (`05-resumen-ejecutivo.md` §2) |

## 5. Qué conviene actualizar (decisión del usuario)

Esta auditoría no modifica documentos fuera de su directorio. Quedan como sugerencias:

- `bodegas-legacy/docs/legacy_analysis/MIGRATION_MATRIX.md`: marcarla como histórica y apuntar a esta matriz.
- `Backend/wms-api/Wms.Application/Warehouse/README.md` y `GUIA_USUARIO.md`: corregir «la recepción actualiza el stock».
- `Backend/wms-api/deploy/staging/README.md:206`: la «pantalla de respaldos» no existe.
- `docs/contexto/estado.md`: registrar esta auditoría y sus P1. Su §1 puede matizar «toda la funcionalidad planeada está implementada» con las cuatro excepciones del §3.2.
- ~~`docs/contexto/decisiones.md`: resolver el choque de `DEC-012` con el código (BR-04-002) y las 13 preguntas de `06-brechas-priorizadas.md` §3.1.~~ Hecho el 2026-10-23: DEC-050…054 y DEC-012 precisada.
