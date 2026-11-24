# Plan cerrado — Fase 2 · Ajustes de la QA manual de F01 y F02

> **Fecha:** 24 de noviembre de 2026. **Estado:** Aprobado por el usuario el 2026-11-24 («Aprobar y ejecutar»). En ejecución.
> **Origen:** la QA manual del usuario sobre `fase-2` después de I-01, con diez hallazgos visuales: [`../qa-manual/hallazgos-f01-f02.md`](../qa-manual/hallazgos-f01-f02.md) y sus mockups (`drawel-detalle-terceros/`, `drawer-detalle-servicios/`, `drawer-detalle-usuario/`). Las respuestas del usuario del 2026-11-24 están en D1 a D4.
> **Base:** FE `fase-2` `042c4ce` · docs `main`. Rama: `f2/f02-ajustes-qa` (FE), desde `fase-2` (D4).
> **Alcance:** solo frontend. Sin cambios de backend, de contrato ni migraciones.
> **Rutas:** relativas a `code_workspace/`. Prefijos: `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`; `P02/` = `D/planes/sprint-11/f02-base/plan-cerrado-f2-f02-base-2026-11-21.md`; `QA/` = `D/planes/sprint-11/qa-manual/`.

---

## 0. Instrucciones para el ejecutor

1. **Lecturas mínimas:** `Frontend/wms/AGENTS.md`, `D/procesos/flujo-de-trabajo-agentes.md`, `P02/` D2, D9, D11 y §2.2 (`AppDetailDrawer`), este plan completo, el archivo de hallazgos y los tres mockups (`screen.png` y `code.html`). Los mockups los hizo una IA: sirven de guía de estructura y estilo, no de píxeles; donde chocan con una Dn, gana la Dn.
2. **Rama y git:** `git fetch`; crea `f2/f02-ajustes-qa` desde `fase-2`. Commit al cerrar cada fase con el mensaje de §7 y push de la rama. Al cerrar la fase 3 y pasar las compuertas, fusiona en `fase-2` con `--no-ff` y push. Sin `push --force`. El cambio local sin commit de `F/app.vue` (Devtools comentado) no es de este plan: no lo incluyas en ningún commit.
3. **Líneas citadas:** son de `042c4ce`. Confírmalas con grep; si el código no coincide, pregunta en un solo mensaje.
4. **Convenciones:** las de `Frontend/wms/AGENTS.md`. Estilos con tokens de PrimeVue (`var(--p-…)`) y utilidades de Tailwind, sin colores fijos, para que funcione en tema claro y oscuro.
5. **Verificación:** backend local y `yarn dev`; cada drawer se revisa en el navegador con un usuario Admin y uno Facturación, en ancho normal y ampliado, con captura.

---

## 1. Decisiones

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **Acuerdos y tarifas siguen en los detalles hasta F07, con el contenedor nuevo.** La sección «Acuerdos» del tercero y la de «Tarifas» del servicio (precios, reglas, mínimos e impuestos) se muestran dentro de la tarjeta de sección nueva (D5), con los componentes de hoy sin cambios por dentro, solo para Admin y Facturación. F07 las mueve a «Tarifas y acuerdos» (P-FAC-12 y P-FAC-13) y las borra de los detalles. Responde las dos preguntas de los hallazgos 3 y 4: sí, salen en F07 | Usuario, 2026-11-24: «Mantener con estilo nuevo (Recomendada)»; `P02/` D2; `DEC-005` |
| D2 | **El formulario «Crear tarifa base» se rediseña en F07**, con el patrón de «Agregar tarifa» (P-FAC-13), en su página de Tarifas y acuerdos. Este plan no lo toca | Usuario, 2026-11-24: «En F07 (Recomendada)»; análisis funcional, tabla de modales grandes (`ServicePricingRuleFormDialog.vue` → «Mismo patrón que P-FAC-13») |
| D3 | **Acciones del registro: en el pie o en un menú, nunca en los dos.** Con una o dos acciones, todas van en el pie, con botones `small`. Con más de dos, todas pasan a un menú que abre un botón de solo icono (`pi pi-ellipsis-v`, con tooltip «Acciones») en el encabezado, junto a ampliar y cerrar, y el drawer no lleva pie. El encabezado nunca lleva un botón de acción suelto | Usuario, 2026-11-24: «Acciones en el pie (Recomendada). Pero usar botones small. Si hay más de 2 acciones entonces utilizar un botón de solo icono que abra un menú con las opciones en el header para que el footer del drawer no se sature», precisado el mismo día: «Si hay más de 2 acciones, todo pasa al botón con el menú. No se conserva el pie»; MK-07 (AF-45) |
| D4 | **Rama `f2/f02-ajustes-qa`** desde `fase-2`, fusionada en `fase-2` con `--no-ff` al pasar las compuertas | Usuario, 2026-11-24: «f2/f02-ajustes-qa (Recomendada)»; plan maestro §5.3 |
| D5 | **Anatomía única del drawer de detalle** (hallazgo 10), para estas vistas y las de F03 a F09: <br>• **Encabezado:** icono del registro en un recuadro suave de color primario; título; etiqueta de estado (punto y texto, verde Activo, gris Inactivo) junto al título; subtítulo en una línea (identificación, código o usuario, separados por «·»); a la derecha, menú menú «Acciones» (D3), ampliar y cerrar, todos de solo icono con tooltip. <br>• **Cuerpo:** fondo `--p-surface-50` (oscuro: `--p-surface-950`) y tarjetas de sección separadas. <br>• **Tarjeta de sección** (`AppDetailSection`, nuevo): encabezado con icono, título, contador opcional (`Badge`) y una acción opcional a la derecha («+ Agregar», `small`); cuerpo con pares etiqueta-valor (`app-detail-grid`), una tabla o un estado vacío. <br>• **Estado vacío:** icono en círculo gris, una frase y, si el usuario puede, el enlace o botón para agregar. <br>• **Tablas dentro de una sección:** `DataTable` `size="small"`, sin bordes externos, encabezados en versalitas pequeñas; acciones de fila de solo icono con tooltip. <br>• **Pie:** solo con una o dos acciones; fijo, alineado a la derecha, botones `small` (D3). <br>• **Anchos:** `md` 40rem y `lg` 56rem (hoy 34 y 52); ampliado, 100vw | Hallazgos 3, 4, 5, 8, 9 y 10; mockups de `QA/` |
| D6 | **Tooltips en los botones de acción** (hallazgo 1): todo botón de solo icono de las 16 páginas con `AppDataTable` y de los drawers lleva `v-tooltip.top` con el verbo de la acción («Ver detalle», «Editar», «Desactivar» o «Activar», «Eliminar», «Bloquear salidas»…). Se conserva el `aria-label` actual, que es más largo y nombra el registro. Las pantallas viejas que aún no usan el patrón nuevo reciben los tooltips cuando su feature las rediseñe | Hallazgo 1; `P02/` D8 |
| D7 | **«Ver» de solo icono** (hallazgo 2): `pi pi-eye`, sin `label`, con tooltip «Ver detalle», en Terceros, Servicios, Conductores, Usuarios y Auditoría. `F/features/warehouse/components/LoadingOrderList.vue` no se toca: pertenece a la orden de cargue que retira F06 | Hallazgo 2; plan de F01 fase 5 |
| D8 | **Terceros** (hallazgo 3), según su mockup: encabezado con icono `pi pi-building`, nombre, estado y «NIT … · rol principal»; tarjeta «Datos del tercero» con los datos de hoy, las etiquetas de Estado financiero, UAP y Salidas en el encabezado de la tarjeta, y el aviso de salidas bloqueadas debajo; tarjeta «Roles de negocio» con los roles como chips (con «×» para quitar si puede gestionarlos) y «+ Asignar roles» a la derecha; tarjetas «Cuentas bancarias» y «Contactos» con contador, «+ Agregar» y estado vacío con enlace; tarjeta «Acuerdos» (D1). Acciones en el pie: «Editar» y «Bloquear salidas» o «Permitir salidas» (si tiene `ExitBlockAccess`): dos, sin menú. Se reescriben las plantillas de `StakeholderBusinessRoles`, `BankAccountsList` y `ContactsList`, que solo usa este detalle; su lógica y sus eventos no cambian | Hallazgo 3; mockup `drawel-detalle-terceros/` |
| D9 | **Servicios** (hallazgo 4): encabezado con icono `pi pi-box`, nombre, estado y «Código: … »; tarjeta «Información del servicio» con código (en `font-mono` sobre fondo gris), nombre, descripción («Sin descripción» en cursiva si falta) y fecha de creación; tarjeta «Tarifas» con `ServiceRateSections` sin cambios por dentro (D1). Acciones en el pie: «Editar» | Hallazgo 4; mockup `drawer-detalle-servicios/` |
| D10 | **Conductores** (hallazgo 5): icono `pi pi-id-card`; tarjeta «Datos del conductor»; tarjeta «Últimos ingresos» con contador y la tabla de D5. Pie: «Editar» | Hallazgo 5 |
| D11 | **Usuarios** (hallazgo 8), según su mockup: icono `pi pi-user`; subtítulo «usuario · correo»; tarjeta «Datos del usuario»; tarjeta «Roles» con cada rol en una fila («Quitar» `small`) y, debajo, el selector y «+ Asignar». Acciones: «Editar», «Restablecer contraseña» y «Desactivar» o «Activar»: tres, así que las tres van en el menú del encabezado y el drawer no lleva pie (D3) | Hallazgo 8; mockup `drawer-detalle-usuario/`; D3 |
| D12 | **Auditoría** (hallazgo 9): icono `pi pi-history`; título «Registro de auditoría»; subtítulo «fecha · usuario»; etiqueta de la acción en lugar del estado; tarjeta «Datos del registro»; tarjeta «Cambios» con «Valor anterior» y «Valor nuevo» lado a lado (uno debajo del otro en el ancho `md` o en pantalla angosta), cada uno con su propio encabezado y el JSON con fuente monoespaciada. Sin pie: no tiene acciones | Hallazgo 9 |
| D13 | **Ciudades** (hallazgo 6): «Importar» con `size="small"`, igual que «Nueva ciudad» y «Exportar» (`F/components/app/AppDataTable.vue:300-328`). El modal «Importar ciudades del legacy» queda así: aviso de columnas; zona para soltar el archivo (`FileUpload` en modo avanzado con plantilla propia: icono, «Arrastre el archivo CSV aquí o haga clic para seleccionarlo», y al elegirlo, nombre, tamaño y «×» para quitarlo); «Filas de encabezado» debajo, a la izquierda, con ancho fijo; resultado de la simulación. El pie no cambia | Hallazgo 6 (opción «Dropzone») |
| D14 | **Prefijos** (hallazgo 7): la columna «Prefijo» muestra el prefijo en un `Tag` (`severity="info"`, `font-mono`); «Ejemplo al digitar» muestra el prefijo en color primario y en negrita, y el resto en color de texto atenuado. El mismo resaltado va en el ejemplo del modal | Hallazgo 7 |
| D15 | **La convención queda escrita** (hallazgo 10): un apartado «Drawer de detalle» en `D/contexto/convenciones-tecnicas.md` §3 con D3, D5 y D6, y la galería `F/pages/dev/components.vue` (`P02/` D20) muestra el drawer nuevo con una y con tres acciones | Hallazgo 10; `P02/` D20 |

---

## 2. Componentes compartidos

### 2.1 `AppDetailDrawer` (`F/components/app/AppDetailDrawer.vue`)

| Prop o slot | Tipo | Uso |
| --- | --- | --- |
| `title`, `subtitle`, `width`, `expandable`, `loading` | igual que hoy | `width`: anchos de D5 |
| `icon` (nuevo) | `string` | Clase de PrimeIcons del recuadro del encabezado |
| `status` (nuevo) | `{ label: string; severity: "success" \| "secondary" \| "warn" \| "danger" \| "info" }` | Etiqueta junto al título |
| `actions` (nuevo) | `{ label: string; icon: string; severity?: string; loading?: boolean; disabled?: boolean; command: () => void }[]` | Regla de D3: hasta dos, en el pie; con más, todas en el `Menu` del encabezado y sin pie |
| slot `footer` | se conserva | Para un pie que no sean acciones; si hay `actions`, no se usa |

El cierre propio del `Drawer` se reemplaza por el botón de cerrar del encabezado, para alinear los tres botones de icono. Escape y el clic fuera siguen cerrando.

### 2.2 `AppDetailSection` (nuevo, `F/components/app/AppDetailSection.vue`)

Props: `title`, `icon?`, `count?` (número del `Badge`). Slots: por defecto (cuerpo), `actions` (a la derecha del encabezado), `empty` (se muestra si `empty` es verdadero). Prop `flush?` para cuerpos con tabla sin relleno. Las clases `app-detail-section` y `app-detail-grid` de `F/assets/styles.scss:28-58` se ajustan a D5 y se conservan para no romper otros usos.

---

## 3. Archivos que se tocan

| Archivo | Fase | Cambio |
| --- | --- | --- |
| `F/components/app/AppDetailDrawer.vue`; `F/components/app/AppDetailSection.vue` (nuevo); `F/assets/styles.scss` | 1 | §2; D3, D5 |
| `F/pages/admin/*/index.vue` y `F/pages/settings/*.vue` con `AppDataTable` (16) | 1 | Tooltips (D6) y «Ver» de icono (D7) |
| `F/pages/admin/cities/index.vue`; `F/features/administration/components/CityImportDialog.vue` | 1 | D13 |
| `F/pages/settings/prefixes.vue` | 1 | D14 |
| `F/pages/dev/components.vue` | 1 | D15 |
| `F/pages/admin/stakeholders/index.vue`; `F/features/stakeholders/components/StakeholderDetailSections.vue`, `StakeholderBusinessRoles.vue`, `BankAccountsList.vue`, `ContactsList.vue` | 2 | D8 (`AgreementsList.vue` no cambia: D1) |
| `F/pages/admin/services/index.vue` | 2 | D9 (`F/features/services/components/*` no cambian: D1, D2) |
| `F/pages/admin/drivers/index.vue`, `users/index.vue`, `audit/index.vue` | 3 | D10, D11, D12 |
| `FT/unit/components/AppDetailDrawer.spec.ts`; `FT/unit/components/AppDetailSection.spec.ts` (nuevo) | 1 | Pruebas de §5 |
| `D/contexto/convenciones-tecnicas.md` §3 | 3 | D15 |

---

## 4. Fases

| Fase | Contenido | Criterio de salida |
| --- | --- | --- |
| 1 | Drawer y sección compartidos (§2), tooltips y «Ver» de icono en las 16 páginas, Ciudades, Prefijos y galería | Compuertas de §6; QA-AJ-001 a 005 en PASA. Los drawers de hoy siguen funcionando con el componente nuevo aunque aún no usen `icon`, `status` ni `actions` |
| 2 | Terceros y Servicios | Compuertas; QA-AJ-006 a 009 en PASA |
| 3 | Conductores, Usuarios y Auditoría; convención escrita; fusión en `fase-2` | Compuertas; QA-AJ-010 a 013 en PASA; fusión hecha y publicada |

---

## 5. Pruebas y casos QA

**Vitest:**

- `AppDetailDrawer.spec.ts`: con dos acciones, ambas en el pie y sin menú; con tres, las tres en el menú del encabezado y sin pie; el estado y el icono se pintan; ampliar cambia el ancho; cerrar emite `update:visible`.
- `AppDetailSection.spec.ts`: título, contador, slot de acciones y estado vacío.

**Casos QA** (en el navegador, contra el backend local):

| Caso | Hallazgo | Pasos | Resultado esperado |
| --- | --- | --- | --- |
| QA-AJ-001 | 1 | Pasar el mouse por cada botón de acción de las 16 páginas | Cada uno muestra su tooltip |
| QA-AJ-002 | 2 | Ver las acciones de Terceros, Servicios, Conductores, Usuarios y Auditoría | «Ver» es de solo icono, del mismo tamaño que los demás |
| QA-AJ-003 | 6 | Ciudades: barra de la tabla; abrir «Importar», soltar un CSV, simular | Los tres botones del mismo tamaño; la zona acepta el archivo arrastrado y al hacer clic; nombre y «×» visibles; la simulación funciona como hoy |
| QA-AJ-004 | 7 | Prefijos: tabla y modal de edición | Prefijo en etiqueta; en el ejemplo, el prefijo resaltado en color primario |
| QA-AJ-005 | 10 | `/dev/components` | Drawer con una y con tres acciones según D3 |
| QA-AJ-006 | 3 | Terceros › Ver un cliente, como Admin | Anatomía de D5 y D8; asignar y quitar rol, agregar cuenta y contacto, bloquear y permitir salidas funcionan como hoy |
| QA-AJ-007 | 3; D1 | Igual, como Facturación | Tarjeta «Acuerdos» con los componentes de hoy funcionando |
| QA-AJ-008 | 4 | Servicios › Ver ALMACENAMIENTO y un servicio con precio, como Facturación | Anatomía de D9; tarjeta «Tarifas» con reglas, mínimos, precios e impuestos funcionando como hoy |
| QA-AJ-009 | 4; D1 | Servicios › Ver, como Comercio Exterior | Sin tarjeta «Tarifas» |
| QA-AJ-010 | 5 | Conductores › Ver | Anatomía de D10; «Últimos ingresos» con contador o estado vacío |
| QA-AJ-011 | 8 | Usuarios › Ver; abrir el menú del encabezado | Sin pie; «Editar», «Restablecer contraseña» y «Desactivar» en el menú, y funcionan; asignar y quitar rol funcionan |
| QA-AJ-012 | 9 | Auditoría › Ver un registro de actualización, en ancho normal y ampliado | Anatomía de D12; valores anterior y nuevo legibles |
| QA-AJ-013 | 10 | Abrir los cinco drawers en tema oscuro | Fondo, tarjetas y textos legibles |

---

## 6. Compuertas de cada fase

- `yarn build` con código 0.
- `yarn test` en verde; base 679 pruebas (I-01).
- `yarn lint` con 255 errores o menos (base de I-01) y cero en archivos nuevos o tocados.
- Capturas de los casos de la fase.

---

## 7. Commits

| Fase | Repo | Mensaje |
| --- | --- | --- |
| 1 | FE | `style(ui): drawer de detalle con secciones, tooltips en acciones, «Ver» de icono, importación de ciudades y prefijos (DEC-080, F02, QA manual)` |
| 2 | FE | `style(configuracion): detalle de terceros y servicios con el drawer nuevo (DEC-080, F02, QA manual)` |
| 3 | FE | `style(administracion): detalle de conductores, usuarios y auditoría con el drawer nuevo (DEC-080, F02, QA manual)`, y la fusión `merge: ajustes de la QA manual de F01 y F02 en fase-2` |
| 3 | docs | `docs(convenciones): drawer de detalle; cierre de los ajustes de la QA manual de F01 y F02` |

Al cerrar: estado de este plan y su fila en `D/planes/README.md`; una línea en `D/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md` §3 con los commits; el archivo de hallazgos marca cada punto con su decisión.

---

## 8. Riesgos

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R1 | Reescribir las plantillas de roles, cuentas y contactos rompe sus diálogos | La lógica, los props y los eventos no cambian; QA-AJ-006 recorre cada acción |
| R2 | El cierre propio del `Drawer` se pierde al reemplazarlo | Prueba de Vitest y QA de Escape y clic fuera |
| R3 | F03 a F09 crean drawers sin seguir D5 | D15: convención escrita y galería |
| R4 | Las tarjetas de Acuerdos y Tarifas se ven distintas por dentro | Aceptado por D1: duran hasta F07 |
