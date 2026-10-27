# Plan cerrado — Corrección de la validación de DEC-058 (R1–R10)

> **Fecha:** 26 de octubre de 2026. **Estado:** Aprobado por el usuario el 2026-10-26. Prompt del ejecutor, por fase: `prompt-correccion-validacion-dec-058-2026-10-26.md`.
> **Origen:** los hallazgos R1–R10 de la validación de `plan-cerrado-correccion-dec-057-2026-10-26.md` (§7, «Validación»). Dos revisores independientes los encontraron, y se comprobaron en el código antes de este plan.
> **Va antes de la fase 13** del plan P1.
> **Base:** FE `develop` `e1e871a`; docs `main` `8079ae9` (la validación); BE `develop` `911399c`, que no cambia.
> **Alcance:**
> - 2 fases: báscula; páginas y documentación;
> - solo frontend y docs: sin backend, sin migración y sin cambios de permisos.
>
> **Rutas:** relativas a `code_workspace/`. Prefijos: `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`.

---

## 0. Instrucciones para el ejecutor

1. Lee `Frontend/wms/AGENTS.md`, `D/contexto/convenciones-tecnicas.md`, `DEC-058` y `DEC-005`, y este plan completo. Lee también, del plan de corrección de DEC-057, §1.3 (B1–B9) y la fila de la fase 3 del §7.
2. Trabaja en `develop` (FE) y en `main` de docs, sin ramas ni commits (`DEC-003`). Al cerrar la fase, te detienes con el resumen y los mensajes de commit.
3. Confirma con grep las líneas citadas. Si el código no coincide, detente y pregunta, con todas las dudas en un solo mensaje. Si un caso borde choca con una decisión de este plan, gana la decisión (`DEC-002`).
4. **Sin retrocesos** (`DEC-005`). Se conservan:
   - los borradores por camión (`KeepAlive`);
   - Enter, F2, Alt+N y Alt+K;
   - las flechas en la cola;
   - «Recuperar operaciones»;
   - los filtros y «Exportar» de las listas.
5. **`yarn build` reescribe `.nuxt`.** Si el usuario tiene `yarn dev` abierto, compila sobre una copia de `HEAD`:
   1. `git archive HEAD | tar -x -C <scratchpad>`;
   2. un enlace a `node_modules`;
   3. `nuxt prepare` y luego `nuxt build`.

   Vitest y lint se corren en el repo.

---

## 1. Decisiones

### 1.1 Báscula (fase 1)

| # | Hallazgo | Corrección |
| --- | --- | --- |
| R1 | **Mientras carga un camión, el encabezado del panel actúa sobre el anterior.**<br>• `handleSelectQueueEntry` abre el panel antes de la carga (`F/pages/operations/weighbridge/index.vue:589-600`).<br>• «Soltar camión» (`:1714-1722`), «Guardar» (`:1725-1734`) y los chips «Otros camiones en proceso» (`:1696-1710`) siguen activos con `isLoadingEntry`.<br>• «Soltar» en ese momento borra el borrador del camión anterior (`releaseTruck`, `:1402`) | **Durante la carga, el encabezado muestra solo el camión que llega:**<br>• Ref nuevo `loadingTruckPlate`. `handleSelectQueueEntry` lo llena con `item.vehiclePlate` antes de la carga y lo limpia en su `finally`; en la carga de «Recuperar operaciones» (`onMounted`) queda null.<br>• Con `isLoadingEntry`, el slot `#header` muestra solo «Cargando el camión {placa}…» (sin placa: «Cargando el camión…»), sin `wb-context` ni chips.<br>• «Soltar camión» y «Guardar» no se pintan: `v-if` agrega `!isLoadingEntry`.<br>• `panelTitle` usa la placa que llega.<br>• «Volver a la cola» sigue disponible. Si se usa durante la carga:<br>  – la carga termina con ese camión elegido y el panel cerrado, como si se hubiera abierto y vuelto;<br>  – `focusCurrentStep` no actúa con el panel cerrado;<br>  – `hidePanel` pone el foco en la fila de `panelEntryLogId`, el camión del panel, en lugar de la de `selectedEntry`. |
| R2 | **La cola se come las teclas.**<br>• `TruckQueue.vue` usa `selection-mode="single"` (`:162`).<br>• Con eso, el `onRowKeyDown` del `DataTable` de PrimeVue cancela toda tecla de la fila con foco, salvo Ctrl/Cmd+C (`primevue/datatable/index.mjs:4983-4987`).<br>• Tras «Volver a la cola» o «Soltar camión», el foco queda en una fila. Ahí F5, Alt+←, Ctrl+F y AvPág no hacen nada.<br>• Las teclas de los botones de la fila no le llegan: el manejador lleva `.self` (`:1825`) | **La cola maneja su propio teclado:**<br>• Se quitan `selection-mode` y `meta-key-selection`, y se agrega `row-hover`.<br>• `@row-click` se conserva: PrimeVue lo emite sin modo de selección e ignora los clics en botones (`isClickable`, `:4829`).<br>• `:pt="{ bodyRow: … }"` le da a cada fila, según `context.index`:<br>  – `tabindex` itinerante: 0 en la fila del camión elegido o, sin él, en la primera; -1 en las demás;<br>  – `aria-current="true"` en la fila del camión elegido;<br>  – un `onKeydown` propio.<br>• El `onKeydown` actúa solo si la fila es el `target` y no hay Alt, Ctrl ni Cmd:<br>  – Enter, Intro numérico y Espacio emiten `select`;<br>  – ↑ y ↓ mueven el foco a la fila anterior o siguiente;<br>  – Inicio y Fin, a la primera o la última;<br>  – en esas teclas, `preventDefault`;<br>  – **cualquier otra tecla se deja pasar.**<br>• `focusEntry` y `focusFirstInState` no cambian: siguen con `data-p-index`. |
| R3 | **El panel no retiene el foco.**<br>• Declara `aria-modal`, pero solo la tarjeta de la cola queda `inert` (`index.vue:1654`).<br>• Tab desde el último campo sale a la barra superior, al menú y a «Recuperar operaciones»; Mayús+Tab desde el encabezado llega a «Recuperar operaciones» | **El panel atrapa el foco con la directiva `FocusTrap` de PrimeVue**, la misma que usa `Dialog`:<br>• `import FocusTrap from "primevue/focustrap"` y `const vFocustrap = FocusTrap` en `F/features/weighbridge/components/WeighbridgeProcessPanel.vue`.<br>• `v-focustrap` va en `.wb-process__panel`.<br>• Los hijos directos de `.wb-process__panel`, el encabezado y el cuerpo, no llevan `v-if`. El `MutationObserver` de la directiva solo mira los hijos directos, y moverlos movería el foco aunque esté abierto F2.<br>• Tab desde el último campo vuelve al primer control del encabezado, y Mayús+Tab desde el primero va al último.<br>• Las ventanas de PrimeVue que se abren encima (F2, crear tercero, anular) siguen con su propio foco.<br>• La tarjeta de la cola sigue `inert`. |
| R4 | **Entradas repetidas en el historial.**<br>• Al cargar con `?camion=`, `onMounted` hace `replace` a la cola y después `push` (`index.vue:1603` y `openPanel`). Con F5 en el panel, el historial queda [cola, cola, camión].<br>• «Camión fuera de la cola» hace `replace` (`:1581`) y deja [cola, cola] | **Se reutiliza la regla de `leavePanelRoute`** («la entrada anterior es la cola», `:392-403`):<br>• Pasa a una función pura nueva, `previousEntryIsQueue(back, currentPath, resolve)`, en `F/features/weighbridge/utils/panel-route.ts`. `leavePanelRoute` la usa.<br>• **Carga con `?camion=` y sin `resume`:** si la entrada anterior ya es la cola, no hay `replace`. El panel se abre sobre la entrada actual: `openPanel` ya sale sin navegar cuando `?camion=` coincide.<br>• Con `resume`, o si la entrada anterior no es la cola, no cambia.<br>• «Camión fuera de la cola» llama a `leavePanelRoute()` en lugar de `router.replace`. |
| R5 | **Una ventana abierta sobrevive al cierre del panel.**<br>• `hidePanel` solo cierra F2 (`index.vue:406-413`).<br>• Las ventanas de los formularios del panel van a `body`: `QuickCreateStakeholderDialog` y el gestor de documentos (`ServiceRecordDocumentsManager`) en `StorageServiceForm`; anular (`:2078`), su resultado (`:2088`) y las órdenes adicionales (`:2097`) en la página.<br>• «Atrás» del navegador con una de ellas abierta oculta el panel, y la ventana queda encima de la cola, actuando sobre el camión oculto | **Con una ventana abierta, «Atrás» no cierra el panel:**<br>• En el `watch` de `routeTruckId` (`:1550-1557`), si `?camion=` sale de la URL con el panel abierto y hay una ventana de PrimeVue abierta, el panel sigue abierto y `?camion=` vuelve con `router.push({ query: { ...route.query, camion: panelEntryLogId } })`.<br>• «Hay ventana abierta» = `document.querySelector(".p-dialog-mask")`, la misma prueba de `isEnterIgnored` (`:1481`) y de `useGlobalShortcuts` (`hasOpenModal`).<br>• Vale también para F2: con F2 abierto, primero se cierra F2 (Esc o su botón).<br>• Alt+N y Alt+K ya no actúan con una ventana abierta (`useGlobalShortcuts`). |
| R6 | **Las reglas de modo oscuro con `:global(…)` no aplican y pintan el `<html>`.**<br>• Vue compila `:global(.app-dark) .x` como `.app-dark { … }`: suelta el resto del selector (comprobado con `compileStyle`).<br>• Hay 7 reglas así:<br>  – `F/features/weighbridge/components/WeighbridgeProcessPanel.vue:90`;<br>  – `TruckQueue.vue:314`;<br>  – `WeightCapture.vue:646`;<br>  – `TruckGoodsLines.vue:458`;<br>  – `OutputServiceForm.vue:501`;<br>  – `F/components/base/SpinnerOverlay.vue:69`;<br>  – `F/pages/operations/weighbridge/index.vue:2187`.<br>• En modo oscuro, el panel queda con el fondo claro y el `<html>` recibe el fondo o el color de la última regla cargada | **Se corrigen las siete reglas y una guardia evita que vuelvan:**<br>• Cada una pasa de `:global(.app-dark) .x` a `.app-dark .x`. Vue la compila como `.app-dark .x[data-v-…]`, que aplica también al panel teletransportado, porque el atributo de alcance va en el elemento.<br>• Guardia nueva `FT/unit/guards/scoped-global-selector.spec.ts`, que reutiliza `source-files.ts`. Falla si un `.vue` tiene `:global(…)` seguido de más selector antes de `{` o `,` (`/:global\([^)]*\)(?!\s*[{,])/`).<br>• `:global(.a .b)`, con todo el selector adentro, sigue permitido. |

### 1.2 Páginas (fase 2)

| # | Hallazgo | Corrección |
| --- | --- | --- |
| R7 | **El título de Terceros no sigue el filtro de Roles.**<br>• `pageTexts` y la miga miran solo `?rol=` (`F/pages/admin/stakeholders/index.vue:24-33,54`).<br>• El filtro de la columna cambia `businessRolCode` sin tocar la URL (`:213-216`).<br>• En «Clientes», con Roles = Empresa de transporte, el título sigue diciendo «Clientes» | **El filtro de Roles escribe `?rol=`. Así la URL es la única fuente de:**<br>• el título, el subtítulo y la miga;<br>• la entrada resaltada del menú;<br>• las columnas.<br>Cómo:<br>• `onColumnFilter`, con `businessRoles`, hace `router.replace({ query: { ...route.query, rol: valor ?? undefined } })` y retorna.<br>• El `watch` de `route.query.rol` (`:64-78`) ya reinicia la consulta. Como hoy al cambiar de rol desde el menú, los demás filtros de columna se limpian, porque las columnas cambian con el rol.<br>• Sin rol: «Terceros».<br>• Con un rol sin texto propio: título «Terceros» y subtítulo «Terceros con el rol {nombre del rol}», con el nombre de `businessRolesFilterOptions`. |
| R8 | **Enlaces que pasaron a botón** con `navigateTo` o `router.push`, y perdieron «abrir en otra pestaña» (`DEC-005`):<br>• «Recuperar operaciones» (`F/pages/operations/weighbridge/index.vue:1641-1649`);<br>• «Pendientes» y «Nueva Guía» (`F/pages/foreign-trade/dispatch-guides/index.vue:295,300`);<br>• «Historial», «Nueva Guía», el botón de la lista vacía y «Generar Guía» de la fila (`dispatch-guides/pending.vue:21,36,41,73,92`);<br>• «Nueva Orden» y «Crear Primera Orden» (`F/pages/foreign-trade/loading-orders/index.vue:146,233`).<br>Los «Volver» quedan con `navigateTo` (U1) | **Componente nuevo `F/components/app/AppLinkButton.vue`:**<br>• prop `to` (`RouteLocationRaw`), con `inheritAttrs: false`;<br>• renderiza `<NuxtLink :to custom v-slot="{ href, navigate }">` y, adentro, `<Button as="a" :href="href" v-bind="$attrs" @click="navigate" />`;<br>• el clic simple navega dentro de la app; Ctrl, Cmd o el clic con la rueda abren otra pestaña, porque `navigate` de vue-router ya deja pasar esos clics;<br>• `v-tooltip` y `aria-label` caen sobre el `<a>`.<br>Los diez botones de la lista lo usan, con sus mismas props (`label`, `icon`, `severity`, `outlined`, `text`, `rounded`, `badge`, `badge-severity`). `createGuideFor` (`pending.vue:21`) se reemplaza por el `to` del enlace. |
| R10 | **Informe de báscula: un error se ve como lista vacía.**<br>• `F/pages/operations/weighbridge/reports.vue:198` no tiene rama de error.<br>• Si la consulta falla, la página dice «No se encontraron operaciones para esta fecha» | **El `#empty` distingue el error:**<br>• `useDailyBillingReport` también entrega `isError` y `refetch`;<br>• con error: `pi pi-exclamation-triangle`, «No se pudo cargar el informe.» y un botón «Reintentar» (`refetch`);<br>• sin error: el texto de hoy. |

### 1.3 Documentación (fase 2)

| # | Hallazgo | Corrección |
| --- | --- | --- |
| R9 | **Cambios de texto que la desviación (5) de la fase 2 del plan anterior no lista.** Por eso faltan en QA, en la nota y en los videos.<br>Pasaron a botón de ícono con ayuda al pasar el mouse:<br>• «Acciones» de Facturas (`pi pi-bolt`);<br>• «Registrar prórroga» de Abandono (`pi pi-calendar-plus`);<br>• «Generar Guía» de la fila de Pendientes de guía (`pi pi-file-export`).<br>Además, el botón del encabezado de Pendientes de guía pasó de «Generar Guía» a «Nueva Guía», y la ayuda de esa página (`pending.vue:48`) todavía dice «Seleccione "Generar Guía"» | **Código:** la ayuda de `pending.vue:48` pasa a «Use el botón «Generar Guía» (ícono de documento) de cada orden y complete el formulario de la guía de salida».<br>**Docs:**<br>• `D/qa/fase-06-facturacion.md` F6-ACC-001;<br>• `D/qa/fase-05-comercio-exterior.md` F5-ABA-003 y F5-GUI-001;<br>• `D/videos/videos-desactualizados-dec-057.md` §5.1, una fila por cambio; y §5.2, si un subtítulo publicado los nombra (grep de solo lectura, como en la fase 5 anterior);<br>• `D/manuales/nota-operarios-hallazgos-2026-10-26.md`: en la fila «Pantalla de Báscula y tablero de depósitos», una frase sobre las acciones de fila con ícono y su ayuda. |

---

## 2. Fase 1 — Báscula (frontend, R1–R6)

**Pruebas:**

| Archivo | Escenario |
| --- | --- |
| Ajustar `FT/components/weighbridge/TruckQueue.spec.ts` | Con foco en una fila, F5, Alt+←, Ctrl+F y AvPág no quedan con `defaultPrevented`. Enter y Espacio sobre la fila emiten `select`. Enter sobre «Capturar peso» emite `capture-weight` y no `select`. ↓ y ↑ mueven el foco, e Inicio y Fin van a los extremos. Una sola fila tiene `tabindex="0"`: la del camión elegido o la primera. La fila del camión elegido lleva `aria-current="true"` |
| Ajustar `FT/components/weighbridge/WeighbridgeProcessPanel.spec.ts` | El panel tiene los dos centinelas de `FocusTrap` (`[data-p-hidden-focusable="true"]`). Las pruebas de hoy (`v-show`, Escape, «Volver a la cola») siguen |
| **Nuevo** `FT/unit/weighbridge/panel-route.spec.ts` | `previousEntryIsQueue` da verdadero con la misma ruta sin `camion` y falso con `camion`, con otra ruta o sin `back` |
| **Nueva** guardia `FT/unit/guards/scoped-global-selector.spec.ts` | Sin `:global(…)` seguido de más selector en `F/`. Se prueba con un ejemplo que falla y otro que pasa |

**Verificación en pantalla** sobre `wms_qa_preprod`, con el navegador integrado y la sesión que abra el usuario, a 1366×768. Las escrituras se interceptan en la página (como en la fase 3 anterior): no se guarda nada.

| Paso | Qué se hace | Qué se espera |
| --- | --- | --- |
| R1 | Se retrasa 3 s la respuesta de la carga del camión, interceptando `fetch` en la página. Se cambia de camión con un chip | El encabezado dice «Cargando el camión {placa}…», sin «Soltar», «Guardar» ni chips. Al terminar, aparece el camión nuevo con lo suyo, y el borrador del anterior sigue |
| R2 | «Volver a la cola» | Con el foco en la fila: F5 recarga, Alt+← vuelve, Ctrl+F abre la búsqueda del navegador (comprobado con un escucha que lee `defaultPrevented`), ↓ ↑ recorren y Enter abre el panel |
| R3 | Tab desde el último campo del registro | Vuelve al encabezado del panel. Mayús+Tab desde el primer control va al último. Nunca llega a la barra superior ni al menú. F2 sigue abriendo el peso encima |
| R4 | F5 con el panel abierto | El panel reabre el camión. «Atrás» una vez vuelve a la cola; otra vez, sale del módulo. Se comprueba con `history.length` antes y después |
| R5 | Abrir «Crear tercero» y pulsar «Atrás» | El panel y la ventana siguen, y `?camion=` vuelve a la URL. Se cierra la ventana y «Atrás» cierra el panel. Lo mismo con F2 abierto |
| R6 | Modo oscuro | El panel tiene fondo oscuro. `getComputedStyle(document.documentElement).backgroundColor` es el mismo antes y después de abrir la báscula. «Espera» en ámbar desde 60 min |

Además, de la fase 3 anterior se repiten tres pasos, para asegurar que nada se rompió:
- el paso 1: lo digitado se conserva al volver a la cola y cambiar de camión;
- el paso 3: F2 sobre el panel, y Escape cierra solo F2;
- el paso 6: Alt+N y Alt+K.

**Commit sugerido (FE):** `fix(bascula): el panel no actúa sobre el camión anterior mientras carga, la cola deja pasar las teclas del navegador, el foco queda en el panel, «Atrás» respeta las ventanas abiertas y el modo oscuro aplica (validación DEC-058)`

---

## 3. Fase 2 — Páginas y documentación (frontend y docs, R7–R10)

**Pruebas:**

| Archivo | Escenario |
| --- | --- |
| **Nuevo** `FT/components/app/AppLinkButton.spec.ts` | Renderiza un `<a>` con el `href` de la ruta y las props del botón (`label`, `icon`, `badge`). El clic simple navega. Ctrl+clic y el clic con la rueda no llaman `preventDefault` |
| Ajustar o crear la prueba de `admin/stakeholders` | Con `?rol=CUSTOMER`, elegir «Empresa de transporte» en Roles cambia la URL a `?rol=TRANSPORT_COMPANY` y el título a «Empresas de transporte». Limpiarlo deja «Terceros». Un rol sin texto propio da «Terceros» y el subtítulo con su nombre. Si montar la página entera es costoso, la regla del texto sale a una función pura, `stakeholderPageTexts(rol, roleName)`, con su prueba |
| `FT/unit/guards/*` | En verde: `AppLinkButton` lleva texto o `aria-label` en cada uso |

**Verificación en pantalla**, igual que la fase 1:
- **R7:** en Clientes, cambiar el filtro de Roles cambia la URL, el título, la miga y la entrada resaltada del menú, sin recargar.
- **R8:** los diez enlaces son `<a href>`. Ctrl+clic abre otra pestaña, y el clic simple navega dentro de la app. «Recuperar operaciones» conserva su contador.
- **R10:** con la consulta del informe forzada a 500 (interceptada en la página), se ve «No se pudo cargar el informe.», y «Reintentar» vuelve a consultar.

**Docs, R9 y registro:**
- **R9:** como dice el §1.3.
- **Casos QA**, con el siguiente ID libre de cada archivo:
  - `D/qa/fase-03-bascula.md`: el encabezado durante la carga (R1), las teclas en la fila de la cola (R2), el foco del panel (R3), F5 con el panel (R4), «Atrás» con una ventana abierta (R5) y el informe con error (R10);
  - `D/qa/fase-10-ux-visual-errores.md`: el modo oscuro del panel (R6);
  - `D/qa/fase-01-administracion.md`: el título de Terceros con el filtro de Roles (R7);
  - `D/qa/fase-05-comercio-exterior.md`: los enlaces de guías y órdenes en otra pestaña (R8).
- **Registro:**
  - el §4 de este plan;
  - `D/planes/README.md`;
  - el §7 del plan de corrección de DEC-057, con R1–R10 corregidos y sus commits;
  - `DEC-058`, con su línea de commits;
  - el pendiente 8b de `D/contexto/estado.md`;
  - el §16.4 del plan P1: el commit FE a desplegar y los casos QA de staging del panel.

**Commits sugeridos:**
- **FE:** `fix(paginas): el título de Terceros sigue el filtro de rol, los botones de navegación vuelven a ser enlaces y el informe de báscula distingue el error (validación DEC-058)`
- **Docs:** `docs(planes,qa): corrección de la validación de DEC-058 (R1–R10), con sus casos QA`

---

## 4. Estado de las fases

| Fase | Estado | Commits | Notas |
| --- | --- | --- | --- |
| 1 · Báscula (R1–R6) | Pendiente | — | — |
| 2 · Páginas y documentación (R7–R10) | Pendiente | — | — |

---

## 5. Riesgos

| Riesgo | Mitigación |
| --- | --- |
| Quitar `selection-mode` puede romper el resaltado, el clic o las flechas de la cola | El resaltado ya sale de `rowClass`, y `@row-click` no depende del modo. Las flechas pasan al `onKeydown` propio. Lo cubren las pruebas de `TruckQueue` y los pasos R2 y 1 de la verificación |
| `FocusTrap` mueve el foco si cambian los hijos directos del panel | Su `MutationObserver` solo mira los hijos directos, y R3 prohíbe `v-if` en ellos. La verificación repite F2 sobre el panel |
| Volver a poner `?camion=` cuando hay una ventana abierta deja una entrada nueva en el historial | Es la misma entrada que se quitó con «Atrás»; el historial queda igual que antes de pulsarlo |
| Con R7, cambiar el rol limpia los demás filtros de columna | Ya pasa hoy al cambiar de rol desde el menú, porque las columnas cambian con el rol. Lo que se ve y lo que se pide coinciden |
