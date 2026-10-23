A continuación te presento un **ejemplo completamente concreto y operativo**, alineado con tu contexto real de **WMS para depósito aduanero DIAN**, mostrando **cómo dividir una feature entre Antigravity (diseño)** y **Cursor (ejecución)**, y **qué artefactos se generan en cada paso**.

Voy a usar como feature ejemplo:
**“Registro de levante parcial de mercancía asociado a una declaración”**, porque es típica de un depósito aduanero y tiene reglas claras.

---

## Feature objetivo (alcance controlado)

> Permitir registrar uno o varios **levantes parciales** sobre una **declaración**, afectando parcialmente las cantidades de mercancía almacenada, manteniendo trazabilidad y estados aduaneros.

---

# FASE 1 — ANTIGRAVITY (DISEÑO Y ACOTACIÓN)

**Objetivo**: salir con todo definido **sin escribir código productivo**.

### 1. Prompt en Antigravity (ejemplo real)

```
Actúa como arquitecto de software especializado en WMS para depósitos aduaneros DIAN.

Necesito diseñar la feature:
"Levante parcial de mercancía por declaración".

Entrega exclusivamente:
1. Reglas de negocio
2. Modelo de dominio (entidades y relaciones)
3. Estados posibles del levante
4. Contrato de API REST (endpoints, DTOs)
5. Validaciones críticas
6. Eventos importantes de auditoría

No generes código.
```

---

## 2. Artefactos generados por Antigravity

### 📄 A. Reglas de negocio (documento funcional)

Ejemplo de salida:

* Una **Declaración** puede tener **0..N Levantes**
* Un **Levante** puede ser:

  * TOTAL
  * PARCIAL
* Un levante parcial:

  * No puede exceder el saldo disponible
  * No cierra la declaración
* Cuando el saldo llega a 0:

  * La declaración pasa a estado `LEVANTADA_TOTAL`

📌 **Artefacto**:
`rules-levante-parcial.md`

---

### 📄 B. Modelo de dominio

```
Declaracion
- id
- numero
- estado
- peso_total
- peso_disponible

Levante
- id
- declaracion_id
- tipo (TOTAL | PARCIAL)
- fecha
- usuario

LevanteDetalle
- id
- levante_id
- producto_id
- cantidad
- peso
```

📌 **Artefacto**:
`domain-model-levante.md`

---

### 📄 C. Estados

**Declaración**

* REGISTRADA
* EN_DEPOSITO
* LEVANTADA_PARCIAL
* LEVANTADA_TOTAL

**Levante**

* REGISTRADO
* ANULADO

📌 **Artefacto**:
`state-machine-levante.md`

---

### 📄 D. Contrato de API (clave para Cursor)

```http
POST /api/declaraciones/{id}/levantes
```

**Request**

```json
{
  "tipo": "PARCIAL",
  "detalles": [
    {
      "productoId": 12,
      "cantidad": 50,
      "peso": 120.5
    }
  ]
}
```

**Response**

```json
{
  "levanteId": 45,
  "estadoDeclaracion": "LEVANTADA_PARCIAL",
  "saldoRestante": 300.0
}
```

📌 **Artefacto**:
`api-contract-levante.json`

---

### 📄 E. Validaciones

* Cantidad > 0
* Peso > 0
* Saldo suficiente
* Declaración en estado permitido
* Producto pertenece a la declaración

📌 **Artefacto**:
`validations-levante.md`

---

### 📄 F. Eventos de auditoría

* LEVANTE_REGISTRADO
* SALDO_ACTUALIZADO
* DECLARACION_CAMBIO_ESTADO

📌 **Artefacto**:
`audit-events-levante.md`

---

### ✅ Resultado de Antigravity

Sales con:

* Criterios cerrados
* Alcance acotado
* Contratos estables
* Cero tokens caros

---

# FASE 2 — CURSOR (IMPLEMENTACIÓN CONTROLADA)

**Objetivo**: implementar solo lo ya definido.

---

## PASO 1 — Base de datos (Cursor)

### Prompt Cursor

```
Basado en este modelo de dominio (adjunto),
crea las migraciones SQL para:

- levantes
- levante_detalles

No modifiques tablas existentes.
```

📌 **Artefactos generados**

* `Vxx__create_levantes.sql`
* `Vxx__create_levante_detalles.sql`

---

## PASO 2 — Backend (Cursor)

### Prompt 2.1: Entidades

```
Genera las entidades ORM para Levante y LevanteDetalle
siguiendo este contrato y relaciones.
```

📌 Artefactos:

* `LevanteEntity`
* `LevanteDetalleEntity`

---

### Prompt 2.2: Servicio de dominio

```
Implementa el servicio RegisterLevanteService que:

- Valide reglas
- Descuente saldos
- Cambie estados
- Registre eventos de auditoría
```

📌 Artefactos:

* `RegisterLevanteService`
* Tests unitarios

---

### Prompt 2.3: Controller

```
Implementa el endpoint POST /declaraciones/{id}/levantes
usando este DTO y servicio.
```

📌 Artefactos:

* `LevanteController`
* `CreateLevanteDto`

---

## PASO 3 — Frontend (Cursor)

### Prompt 3.1: UI

```
Crea un formulario para registrar levante parcial:

- Lista productos
- Campos cantidad y peso
- Validaciones básicas
- Confirmación
```

📌 Artefactos:

* `LevanteFormComponent`
* `levante.service.ts`

---

## PASO 4 — Pruebas (Cursor)

```
Agrega pruebas unitarias para:
- Levante parcial válido
- Saldo insuficiente
- Cambio de estado
```

📌 Artefactos:

* `register-levante.spec.ts`

---

# MATRIZ FINAL: ¿Quién hace qué?

| Fase     | Herramienta | Resultado                  |
| -------- | ----------- | -------------------------- |
| Diseño   | Antigravity | Reglas, dominio, contratos |
| BD       | Cursor      | Migraciones                |
| Backend  | Cursor      | Servicios, controllers     |
| Frontend | Cursor      | Componentes                |
| QA       | Cursor      | Tests                      |

---

## Beneficio real para ti

* 60–75% menos tokens
* Prompts pequeños
* Control total del alcance
* Código más limpio
* Menos re-trabajo

---

Si quieres, en el siguiente mensaje puedo:

* Convertir este ejemplo en un **template reutilizable**
* Ajustarlo exactamente a tu stack (.NET / NestJS / Angular)
* O ayudarte a definir **qué features NO deben pasar por Cursor**
