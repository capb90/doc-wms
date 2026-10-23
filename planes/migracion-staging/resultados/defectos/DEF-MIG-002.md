# Ficha de defecto — DEF-MIG-002

| Campo | Valor |
|---|---|
| ID | DEF-MIG-002 |
| Título | La consulta de levantes de F6-03 arrastra levantes de depósitos cerrados con el mismo número |
| Severidad | CRITICAL |
| Prioridad sugerida | Alta |
| Módulo | Administración (migración legacy) |
| Caso(s) | FA-MIG-001, FA-MIG-003; E19 |
| Riesgo del plan (§9) | «La herramienta nunca se probó con datos reales (E19)» |
| Ambiente y commits | Local (`wms_migracion`) · FE `24d742d` · BE `f6f1828` |
| Rol / usuario | Admin |
| Estado | Verificado |

## Precondiciones y datos
- En el legacy, `deposito.nro_deposito` **no es único**: la serie se reinicia (BA0001 existe en varios años). Hay 9.682 depósitos y 4.755 números distintos.
- Entre los 128 depósitos vivos los números sí son únicos.
- Depósitos cargados en firme (128).

## Pasos para reproducir
1. Ejecutar la consulta de levantes del plan (`docs/planes/paridad-legacy/plan-backend-paridad-legacy.md` ≈ línea 2952) con `D.nro_deposito IN (<números del CSV de depósitos>)`.
2. `POST /api/v1/administration/legacy-import/Releases` con `dryRun=true`.

Ejemplo anonimizado: dos depósitos del legacy con el mismo número.

| id_deposito | nro_deposito | Año | Estado |
|---|---|---|---|
| 1001 | BA9001 | 2019 | cerrado |
| 2001 | BA9001 | 2024 | vivo |

La consulta por número devuelve los levantes de los dos.

## Resultado esperado
Solo los levantes de los depósitos vivos exportados: **170 filas** (118 tras el paliativo de DEF-MIG-003).

## Resultado obtenido
- La consulta devuelve **819 filas**.
- En la simulación se crean **109** levantes (frente a los 107 correctos): 2 levantes de depósitos cerrados caen en el depósito vivo con el mismo número y el mismo producto.
- 499 filas se rechazan con «el producto legacy N con embalaje N no está en el depósito BAN».

## Evidencia
- Lote `def2-Releases-sim` y CSV `db_legacy/trabajo/extractos/12_levantes_original.csv` (fuera de git).

## Impacto
- Nacionalizado inflado en depósitos vivos: permitiría despachar mercancía sin levante.
- Además, cientos de errores de ruido en el reporte de simulación.
- **Paliativo aplicado en la fase 1:** la consulta congelada (`consultas/12_levantes.sql`) filtra por `D.id_deposito` de los depósitos vivos.

## Pista técnica (opcional)
Corregir la consulta del plan para filtrar por `id_deposito`, con la misma subconsulta de depósitos vivos o con una tabla temporal de ids.

## Historial
| Fecha | Evento | Build | Por |
|---|---|---|---|
| 2026-10-06 | Detectado en la fase 1 de la migración (E19) | BE `f6f1828` | Agente ejecutor (Opus 5.5) |
| 2026-10-06 | **Corregido.** La consulta de levantes de F6-03 en `docs/planes/paridad-legacy/plan-backend-paridad-legacy.md` filtra por `id_deposito` de los depósitos vivos con la misma condición de la consulta de depósitos (`HAVING ingresan − salen > 0`, sin eliminados ni el importador 70) y ya no agrupa: exporta una fila por `producto_levante` y agrupa el importador (DEF-MIG-003). Incluye la nota de por qué no se filtra por número. Se probó en solo lectura contra `legacy-mariadb`: 170 filas, iguales a `extractos/12_levantes_sin_agrupar.csv`. Solo documentación. Commits: pendiente. | BE `f6f1828` + cambios sin commit | Agente implementador (Opus 5.5) |
| 2026-10-06 | **Verificado** en la repetición de la fase 1 (`informe-fase-1-repeticion.md`). La consulta de levantes del plan, sin editar (`consultas/v2/12_levantes.sql`), devuelve **170 filas**, todas de depósitos del CSV de depósitos; son las mismas filas de `extractos/12_levantes_sin_agrupar.csv`. Firme: 107 levantes creados (no 109). Los 18 errores de fila son «el producto legacy N con embalaje N no está en el depósito BAN»: 11 grupos de productos agotados en el legacy (no exportados en depósitos), ninguno por número de depósito repetido. Σ levantes por producto = `nacionalizados` del CSV en 133 de 133. Informe de la repetición §5.2. | BE `9c5c81b` · FE `4799cc4` | Agente ejecutor (Opus 5.5) |

## Lista de verificación para la repetición de la fase 1
- [x] La consulta de levantes del plan (F6-03, «Levantes. Corregida…», ≈ línea 2982) se ejecuta tal como está, sin lista de números ni ids pegados a mano.
- [x] Devuelve **≈ 170 filas** (no 819) y todas son de los depósitos vivos del CSV de depósitos.
- [x] La simulación de `Releases` no da errores «el producto legacy N … no está en el depósito BAN» por depósitos con el número repetido, y no crea levantes en depósitos equivocados (≈ 107 creados, no 109).
