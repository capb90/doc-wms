A continuación te entrego el **template reutilizable**, diseñado para que puedas **repetir este flujo en cualquier feature de tu WMS aduanero**, controlando **costo, tokens y calidad**, y separando correctamente **Antigravity (diseño)** de **Cursor (ejecución)**.

Este template está pensado para:

* Features con **reglas DIAN**
* Backend + frontend + base de datos
* Evolución incremental (no “big bang”)

Puedes copiarlo tal cual y reutilizarlo.

---

# TEMPLATE REUTILIZABLE

## Feature WMS – Estrategia Antigravity + Cursor

---

## 🧩 FEATURE METADATA (completar manualmente)

```text
Feature name:
Contexto funcional:
Entidad principal:
Impacta inventario: (SI / NO)
Impacta estados aduaneros: (SI / NO)
Tipo de cambio: (NUEVA / EXTENSIÓN / REGLA)
```

---

# FASE 1 — ANTIGRAVITY (DISEÑO Y ACOTACIÓN)

## 🎯 Objetivo

Definir completamente la feature **sin escribir código productivo**.

---

## 1️⃣ Prompt estándar – Antigravity

```text
Actúa como arquitecto de software especializado en WMS para depósitos aduaneros habilitados por la DIAN.

Necesito diseñar la siguiente feature:

[DESCRIPCIÓN FUNCIONAL BREVE]

Entrega exclusivamente los siguientes artefactos, sin generar código:

1. Reglas de negocio
2. Modelo de dominio (entidades y relaciones)
3. Estados y transiciones
4. Contrato de API REST (endpoints y DTOs)
5. Validaciones críticas
6. Eventos de auditoría / trazabilidad

Usa terminología aduanera correcta.
No asumas implementación técnica.
```

---

## 2️⃣ Artefactos obligatorios (output Antigravity)

### 📄 A. Reglas de negocio

**Archivo:**
`rules-[feature].md`

Contiene:

* Qué se permite
* Qué se prohíbe
* Condiciones previas
* Efectos colaterales

---

### 📄 B. Modelo de dominio

**Archivo:**
`domain-[feature].md`

Incluye:

* Entidades
* Relaciones
* Cardinalidades
* Campos clave

---

### 📄 C. Estados y transiciones

**Archivo:**
`states-[feature].md`

Define:

* Estados iniciales
* Estados finales
* Cambios automáticos

---

### 📄 D. Contrato de API

**Archivo:**
`api-[feature].json`

Incluye:

* Endpoint
* Request
* Response
* Códigos de error

⚠️ Este artefacto es **la fuente de verdad para Cursor**.

---

### 📄 E. Validaciones

**Archivo:**
`validations-[feature].md`

Reglas que deben cumplirse antes de persistir.

---

### 📄 F. Auditoría

**Archivo:**
`audit-[feature].md`

Eventos que deben registrarse para DIAN / control interno.

---

### ✅ Checklist de salida Antigravity

```text
☐ Alcance cerrado
☐ Reglas claras
☐ Contratos definidos
☐ Estados explícitos
☐ Sin código generado
```

---

# FASE 2 — CURSOR (IMPLEMENTACIÓN CONTROLADA)

## 🎯 Objetivo

Implementar **únicamente lo ya definido** en Antigravity.

---

## 3️⃣ Prompt base – Cursor (regla general)

```text
Implementa exclusivamente lo descrito en los artefactos adjuntos.
No agregues lógica adicional.
No asumas reglas implícitas.
```

---

## 4️⃣ Implementación por capas (orden obligatorio)

---

### 🔹 Paso 1 – Base de datos

**Prompt Cursor**

```text
Basado en domain-[feature].md,
genera las migraciones necesarias.

No modifiques tablas existentes.
```

📌 Artefactos:

* `Vxx__create_[feature]_tables.sql`

---

### 🔹 Paso 2 – Entidades ORM

**Prompt Cursor**

```text
Genera las entidades ORM según domain-[feature].md.
Respeta relaciones y nombres.
```

📌 Artefactos:

* Entidades ORM

---

### 🔹 Paso 3 – Servicio de dominio

**Prompt Cursor**

```text
Implementa el servicio de dominio que:

- Aplica rules-[feature].md
- Ejecuta validations-[feature].md
- Emite eventos audit-[feature].md
- Cambia estados según states-[feature].md
```

📌 Artefactos:

* Servicio
* Tests unitarios

---

### 🔹 Paso 4 – API / Controller

**Prompt Cursor**

```text
Implementa el endpoint definido en api-[feature].json
usando el servicio de dominio.
```

📌 Artefactos:

* Controller
* DTOs

---

### 🔹 Paso 5 – Frontend

**Prompt Cursor**

```text
Crea la UI basada en api-[feature].json:

- Formularios
- Validaciones básicas
- Manejo de errores
```

📌 Artefactos:

* Componentes
* Servicios frontend

---

### 🔹 Paso 6 – Pruebas

**Prompt Cursor**

```text
Agrega pruebas para:
- Caso exitoso
- Validaciones fallidas
- Cambios de estado
```

📌 Artefactos:

* Tests unitarios / integración

---

## 5️⃣ Regla de oro de costos

```text
❌ Nunca pedir "feature completa"
❌ Nunca mezclar diseño con código
❌ Nunca dejar reglas implícitas

✅ Prompts pequeños
✅ Artefactos explícitos
✅ Ejecución por capas
```

---

# ESTRUCTURA SUGERIDA DE CARPETAS

```text
/docs/features/
 └── [feature]/
     ├── rules.md
     ├── domain.md
     ├── states.md
     ├── api.json
     ├── validations.md
     └── audit.md
```

---

## Resultado esperado

* Reducción drástica de tokens
* Features predecibles
* Menos re-trabajo
* Código alineado a reglas aduaneras
* Facilidad para auditoría DIAN

---

### Siguiente paso opcional

Si quieres, puedo:

* Ajustar este template **exactamente a tu stack** (.NET + Angular o NestJS)
* Convertir este template en un **checklist operativo para cada sprint**
* Diseñar un **prompt guard** para evitar sobreuso de tokens en Cursor
