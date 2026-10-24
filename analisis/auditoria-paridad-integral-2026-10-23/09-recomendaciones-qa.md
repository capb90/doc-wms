# 09 — Recomendaciones de QA

> **Fecha:** 2026-10-23. **Ninguna de estas pruebas se ejecutó en esta auditoría.** Son las que confirmarían la paridad y cerrarían las brechas que solo tienen evidencia estática.
> **Cómo leer la columna «Origen»:**
> - **Documentada (no ejecutada):** el caso existe en `docs/qa/fase-*.md`, pero no tiene resultado, o su resultado fue «NO APLICA».
> - **Documentada (re-ejecutar):** el caso se ejecutó sobre un build anterior o sin cubrir el escenario.
> - **Propuesta:** el caso es nuevo.
>
> Ninguna fila es «Ejecutada»: las ejecuciones previas se citan en la columna «Validación mediante ejecución» de `04-matriz-global.csv`.
> **Ambiente:** local para lo que exige datos o palancas de tiempo (`docs/procesos/verificacion-local.md`). En staging no se escribe con SQL ni se recrea la base (`DEC-006`, `DEC-042`).

## 1. Prioridad 0 — confirman brechas P1 o cierran el GO

| ID | Capacidad · escenario | Resultado esperado | Datos y condiciones previas | Capa | Origen | Brecha |
| --- | --- | --- | --- | --- | --- | --- |
| QA-01 | Báscula: registro de importación cronometrado (PRF-002) | Un operario real registra un camión en ≤ 30 s, con el build desplegado que incluya el selector de conductor | Staging, datos de práctica P6 (`estado.md` §3) | E2E, UX | Documentada (no ejecutada): PRF-002, F3-REG-024, F3-PES-015 (`docs/qa/resultados/informe-final.md`) | — (condición del GO) |
| QA-02 | Facturación: confirmar un depósito cuyo convenio enlaza un servicio complementario sin tarifa | La confirmación responde 200, la factura sale con la línea complementaria al mínimo o en $0 con advertencia y aviso a Facturación (`DEC-020`); el job no reintenta cada 5 min | Convenio con almacenamiento y servicio complementario sin `ServicePrice`; local | BE, job | Documentada (no ejecutada): F6-ALM-014 «NO APLICA» (`F6-informe-2026-10-02.md:169`), más una prueba de integración nueva | BR-06-004 |
| QA-03 | Convenio «Programado» para mañana | Al día siguiente el convenio está `Active` y un cargo de ese día sale «Acuerdo (nivel 1)» | Local con reloj controlado o palanca de tiempo | BE, job | Propuesta. F1-CNV-009 solo prueba el rechazo de una fecha pasada | BR-06-001 |
| QA-04 | Báscula: corregir el pesaje 3 en un ciclo Bruto → Intermedio → Tara de dos depósitos | Cambia solo la secuencia 3 y el neto del segundo depósito; los dos netos cuadran | Camión con dos documentos (F3-MUL) | FE, BE | Documentada (no ejecutada): F3-COR-006 (riesgo R-BAS-09) | BR-02-006 |
| QA-05 | Orden de cargue: dos `POST foreign-trade/loading-orders` simultáneos por todo el nacionalizado disponible de un producto | Uno 201 y otro 400; la reserva total nunca supera lo nacionalizado | Depósito IMP con levante parcial; prueba de integración paralela (`Wms.IntegrationTests`, Testcontainers) | BE, persistencia | Propuesta. F5-OC-005 prueba el tope secuencial | BR-05-002 |
| QA-06 | Cancelar o modificar una orden `Pending` con guía vigente (de contado, pagada) | 409 «Anule primero la guía…», como en revertir (F5-OC-018) | Guía emitida antes del cargue (F5-GUI-007) | BE, FE | Propuesta (variante de F5-OC-015/016/018) | BR-05-001 |
| QA-07 | Respaldo diario con dos destinos, uno fuera del servidor; provocar un fallo | `GET administration/backups/runs` muestra los dos destinos `Succeeded`; el fallo llega por correo a Admin | Destino S3 real configurado por API (DF3) | Infraestructura, job | Documentada (re-ejecutar): FB-BAK-003/005 (`fase-11-regresion-cierre.md`) con S3 real | BR-08-001 |
| QA-08 | Migración: CSV con dos depósitos vivos de igual número de años distintos y uno con `prorroga = 1` | Los dos migran con sus levantes y conciliación `Ok`; el prorrogado queda con `HasExtension = true` y plazo de 60 días | CSV sintético sin datos reales, `dryRun` y luego real, en local | Migración | Propuesta | BR-08-005, BR-08-003 |
| QA-09 | Kardex, diario de ingresos y Excel de importaciones de un depósito con la fecha de ingreso corregida al día anterior | Aparece en el diario de ese día y con esa fecha en el kardex (pantalla y PDF) y en el Excel | Depósito con corrección de fecha (E2E-15) | BE, FE | Propuesta. Variante de E2E-15 y F7-REP-001 | BR-07-003 |
| QA-10 | Superficie de API sin consumidor: `PATCH entry-logs/{id}` con un ingreso con ciclo de báscula y otro motivo; `POST warehouse/loading-orders` con el rol Warehouse | 409/405 y 403/404 respectivamente | Usuarios por rol; prueba de superficie como `BillingControllerSurfaceTests` | Seguridad, BE | Propuesta. F9 probó la matriz de roles, no estos dos endpoints (`docs/qa/resultados/F9-anexo-matriz-api.md`) | BR-03-001, BR-03-002 |

## 2. Prioridad 1 — contratos, flujos principales y procesos automáticos

| ID | Capacidad · escenario | Resultado esperado | Datos y condiciones previas | Capa | Origen | Brecha |
| --- | --- | --- | --- | --- | --- | --- |
| QA-11 | Levantes: filtrar por rango de fechas desde `/foreign-trade/releases` y exportar Excel | Solo levantes del rango (días de Colombia, inclusivos) | Levantes en tres fechas | INT, contrato | Documentada (re-ejecutar): F5-REL-001, con fechas | BR-05-007 |
| QA-12 | Recorrido de los contratos con desalineaciones conocidas: historial de báscula con filtro «ID Ciclo»; detalle de importación; tipos de facturación; detalle por agencia | Cada campo que la pantalla lee llega del API; ningún filtro se ignora | Datos de QA de F3, F5, F6, F7 | INT, contrato | Propuesta | BR-02-008, BR-04-008, BR-05-013, BR-06-013, BR-07-011 |
| QA-13 | E2E de importación completa con dos camiones, levante parcial, orden, cargue parcial, guía, renovación y factura | Stock, reservas, kardex, ubicaciones y factura cuadran en cada paso | E2E-01, E2E-02, E2E-13 | E2E | Documentada (re-ejecutar) sobre el build actual: E2E-01, 02, 11, 13 (`fase-08-e2e.md`) | Paridad de los módulos 02–06 |
| QA-14 | Notificaciones: con 20 avisos, abrir el panel | El más reciente primero; la página 1 contiene los nuevos | Usuario Facturación con avisos generados | BE, FE | Documentada (re-ejecutar): F7-NOT-006 con orden | BR-08-014 |
| QA-15 | Desactivar un cliente con convenio y depósitos con período abierto | El job de renovación y la factura se comportan según una decisión explícita (sin error silencioso) | Local, palanca de tiempo | BE, job | Propuesta | BR-01-006 (efecto en el módulo 06) |
| QA-16 | Renovación con salida a mitad del período (`PER_UOM`, 10 unidades, salida de 4 en `fin + 2`) | La factura del período siguiente cobra 10, el saldo al inicio del período (DEC-053) | Local, palanca de tiempo | BE, job | Propuesta (DEC-053) | BR-06-005 |
| QA-17 | «Depósitos pendientes» con un depósito agotado cuya factura se anuló sin refacturar | Aparece con `periodsPendingReissue > 0` | F6-REF | BE, FE | Documentada (re-ejecutar): F6-REF-006 | BR-06-003 |
| QA-18 | Camión tardío a un depósito cerrado por agotamiento, sin cierre del ingreso de camiones | Se crea otro depósito con otro número; el agotado sigue cerrado (DEC-051). Prueba de no regresión | E2E-03 sobre un depósito despachado a 0 | E2E | Documentada (re-ejecutar): E2E-03, variante; F3-MCA-009 | BR-04-001 |
| QA-19 | Diarios de ingreso y salida: columnas y exportación frente a una salida legacy de referencia | Diario de ingresos con el formato legacy (DEC-054): por depósito, una fila por camión, total de vehículos y firmas, en pantalla, PDF y Excel; diario de salidas con Excel y todas las filas | Rango con varios depósitos y camiones | FE, BE | Documentada (re-ejecutar): F7-REP-001/003, contra el formato legacy | BR-07-001, 002, 004 |
| QA-20 | Tiquete de báscula: revisar el pie del PDF | Sin la leyenda «Numeración autorizada… por la DIAN», o con decisión que la respalde | Cualquier tiquete | FE (PDF) | Documentada (re-ejecutar): F3-TIQ-002, con este criterio | BR-02-005 |
| QA-21 | Fecha de ingreso anterior al ingreso de Vigilancia | 400 «no puede ser anterior al ingreso del camión en Vigilancia»; tras corregir Vigilancia, la nueva fecha se acepta (DEC-051). Prueba de no regresión | Depósito confirmado | BE, FE | Documentada (re-ejecutar): casos de `fase-05-comercio-exterior.md:135-136` | BR-04-002 (cerrada) |

## 3. Prioridad 2 — regresión del código no desplegado y reglas secundarias

| ID | Capacidad · escenario | Resultado esperado | Datos y condiciones previas | Capa | Origen | Brecha |
| --- | --- | --- | --- | --- | --- | --- |
| QA-22 | Regresión de `83de58a`: borrar un producto declarado sin movimientos; montacargas con camión; recepción informativa con todos los camiones; migración `AddForkliftUseEntryLog` | Funcionan sin romper F4 ni E2E-09 | Build actual en local y luego en staging | E2E, migración | Propuesta (`estado.md` §7: «no se sabe si pasaron por QA») | `CF-V032`, `CF-V033`, `CF-L127`, `CF-L128` |
| QA-23 | Regresión de `2eeaaad`: producto y cantidad en el historial de guías, cambiar el modo de pago, anular un pesaje por repesar, unidad de carga al crear la orden | Ídem | Ídem | E2E | Propuesta | `CF-V055`, `CF-L163`, `CF-L105`, `CF-L154` |
| QA-24 | Embalaje en uso por un producto del catálogo: desactivar y borrar | Desactivar lo oculta; borrar responde 409 | Producto con embalaje | BE, FE | Documentada (re-ejecutar): F1-EMB-003, con un producto del catálogo | BR-01-001 |
| QA-25 | Levante con un número usado en un depósito anulado | Se permite registrarlo en otro depósito | Depósito anulado con levante | BE | Documentada (re-ejecutar): F5-LEV-004, variante | BR-05-003 |
| QA-26 | Guía emitida antes del cargue y cargue que difiere de la guía | La guía se emite; al cargar una cantidad distinta, Comercio Exterior recibe el aviso para anularla y reemitirla (DEC-052) | F5-GUI-007 | BE, FE | Documentada (re-ejecutar): F5-GUI-007, más el aviso nuevo | BR-05-006 |
| QA-27 | Pantallas `SOLO_MAQUETADO`: abrir las autorizaciones de salida, los manifiestos y la validación contra plantilla | Hay una ruta visible a cada diálogo, o se retiran | Rol Receiving y CE | FE | Propuesta | BR-03-003, BR-04-007 (`CF-V036`, `CF-V047`) |

## 4. Criterios para declarar «paridad validada»

Una capacidad pasa de `COMPLETO_CODIGO` o `DIFERENCIA_INTENCIONAL` a validada cuando:

1. un caso con resultado registrado en `docs/qa/resultados/` cubre su escenario principal sobre el build que se desplegará;
2. si tenía brechas, sus criterios de resolución de `06-brechas-priorizadas.md` pasan;
3. las capacidades en `PARCIAL` solo se validan después de corregir o aceptar, con una decisión escrita, todas sus brechas.

Con eso, el indicador de paridad validada (30,3 % hoy, `05-resumen-ejecutivo.md`) se puede recalcular desde `04-matriz-global.csv` sin repetir esta auditoría.

## 5. Lo que no se propone probar

- **Colmotores y el portal de clientes:** están excluidos por decisión, y el módulo 08 verificó que no quedan restos.
- **Datos reales del legacy:** solo se usan en el ensayo del corte, con la aprobación del usuario (`DEC-006`, `DEC-007`).
