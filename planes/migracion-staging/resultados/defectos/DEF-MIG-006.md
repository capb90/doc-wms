# Ficha de defecto — DEF-MIG-006

| Campo | Valor |
|---|---|
| ID | DEF-MIG-006 |
| Título | El detalle del depósito muestra «Importador: Sin asignar» cuando el importador es el cliente |
| Severidad | MINOR |
| Prioridad sugerida | Baja |
| Módulo | Comercio Exterior (detalle del depósito, frontend) |
| Caso(s) | FA-MIG-009 |
| Riesgo del plan (§9) | nuevo |
| Ambiente y commits | Local (`wms_migracion`, FE en el puerto 3001) · FE `24d742d` · BE `f6f1828` |
| Rol / usuario | `mig.comext` (Comercio Exterior) |
| Estado | Verificado |

## Precondiciones y datos
- Cualquier depósito migrado; por ejemplo BA0042 (v2 `2024BA00002`).
- El legacy factura al importador (`cron.php:21`), así que en los 128 migrados el cliente y el importador son el mismo tercero.

## Pasos para reproducir
1. Con Comercio Exterior, abrir Depósitos de importación → `2024BA00002` → Ver detalle.
2. Mirar «Terceros documentales».

## Resultado esperado
- El bloque IMPORTADOR muestra el tercero.
- `GET /api/v1/foreign-trade/warehouse-storages/{id}/stakeholders` lo devuelve con `roleCode = IMPORTER` (e `isCustomer = true`).

## Resultado obtenido
- El bloque dice «IMPORTADOR · Obligatorio para confirmar · Sin asignar».
- El API sí devuelve el importador. En la base, los 128 servicios migrados tienen sus filas `CUSTOMER`, `IMPORTER` y `CUSTOMS_AGENCY`.

## Evidencia
- Página `foreign-trade/imports/3e98f57d-…` (texto capturado en el informe de la fase 1).
- Respuesta del API con el rol `IMPORTER`.

## Impacto
- Visual. Comercio Exterior puede creer que falta el importador.
- No bloquea operaciones: los migrados ya están confirmados.
- También afecta a depósitos nuevos cuyo importador sea el mismo cliente.

## Pista técnica (opcional)
`Frontend/wms/app/features/foreign-trade/components/DepositDetailDocumentStakeholdersSection.vue:61` filtra con `!s.isCustomer` y descarta al importador que también es el cliente.

## Historial
| Fecha | Evento | Build | Por |
|---|---|---|---|
| 2026-10-06 | Detectado en el recorrido por rol de la fase 1 (FA-MIG-009) | FE `24d742d` | Agente ejecutor (Opus 5.5) |
| 2026-10-06 | **Corregido.** `DepositDetailDocumentStakeholdersSection.vue` muestra en cada bloque documental (importador, agencia, exportador) al tercero con ese rol aunque sea el cliente. El filtro `!isCustomer` existía desde el commit inicial del componente (`4c9c205`) para no repetir al cliente en este bloque, pero el cliente llega con el rol `CUSTOMER`, que el bloque no lista: solo escondía al importador o al exportador que también es el cliente. No hay otra lista que dependa de él (el panel de resumen no filtra), así que se quitó. El backend (`DepositConfirmationRequirements`) ya contaba ese importador para confirmar: el bloque deja de decir «Sin asignar» y la regla «Obligatorio para confirmar» queda satisfecha también en depósitos nuevos cuyo importador es el cliente. Prueba: `test/components/foreign-trade/DepositDetailDocumentStakeholdersSection.spec.ts` (importador que es el cliente → se muestra; importador distinto → igual que antes; la fila CUSTOMER no llena un rol documental); falla con el código anterior. Commits: pendiente. | BE `f6f1828` + cambios sin commit · FE `24d742d` + cambios sin commit | Agente implementador (Opus 5.5) |
| 2026-10-06 | **Verificado** en la repetición de la fase 1 (`informe-fase-1-repeticion.md`). Con `mig.comext`, detalle de `2024BA00002`: «Terceros documentales · IMPORTADOR · Obligatorio para confirmar» muestra la razón social y el NIT del importador, el mismo tercero del cliente, y ya no «Sin asignar»; la agencia de aduanas sigue apareciendo. No se probó el caso opcional del depósito nuevo en Borrador. Informe de la repetición §10. | BE `9c5c81b` · FE `4799cc4` | Agente ejecutor (Opus 5.5) |

## Lista de verificación para la repetición de la fase 1
- [x] Con Comercio Exterior, en el detalle de un migrado (p. ej. `2024BA00002`), «Terceros documentales» → el bloque IMPORTADOR muestra el tercero (el mismo del cliente), con su documento; ya no dice «Sin asignar».
- [x] La agencia de aduanas sigue apareciendo como antes.
- [ ] Opcional, en un depósito nuevo de importación en Borrador cuyo importador es el cliente: el bloque lo muestra con «Cambiar» y la confirmación no pide el importador. — *No probado en la repetición.*
