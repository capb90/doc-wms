Eres el implementador de la corrección de **DEF-F11-022 (MINOR)**, un defecto del menú lateral del frontend del WMS de Bodegas Asociadas que reportó el usuario el 2026-10-07. Modelo recomendado: **Sonnet 5.5**: es un cambio acotado en el componente del menú, con pruebas.

## El defecto (reportado por el usuario)
- En el menú de **Comercio Exterior**, al elegir **Reportes → Movimientos por Depósito** (`/reports/warehouse-movements`), el menú lateral **salta y resalta la misma opción del grupo Facturación**.
- Pasa igual con otras entradas compartidas. Por ejemplo, **Facturación → Clientes** salta a **Comercio Exterior → Listado de Terceros**.

## Causa (revisada en el código)
En `app/components/layout/AppMenuItem.vue`, cada entrada del menú observa `route.path`. Si su `to` coincide, llama a `setActiveMenuItem(itemKey)`, en `handleRouteChange`, en un `watch` aparte con la misma lógica, y en `onBeforeMount`. Eso falla de dos maneras:
1. **Rutas repetidas:** en `app/components/layout/AppMenu.vue` hay entradas con el mismo `to` en grupos distintos:
   - `/reports/warehouse-movements`, 2 veces;
   - `/reports/general-inventory`, 3 veces;
   - `/admin/stakeholders`, 2 veces;
   - `/admin/stakeholders/create`, 2 veces;
   - `/notifications`, 2 veces.

   Cuando cambia la ruta, **todas** las que coinciden se marcan activas y gana la última en reaccionar, que no es la que tocó el usuario.
2. **Rutas con filtro:** las entradas cuyo `to` lleva un filtro (`/admin/stakeholders?rol=CUSTOMER`, `?rol=TRANSPORT_COMPANY`, `?rol=CUSTOMS_AGENCY`) **nunca coinciden**, porque se compara contra `route.path`, que no lleva el filtro. En cambio coincide «Listado» (`/admin/stakeholders`) de otro grupo.

## Decisión (cerrada)
1. **Comparar la ruta completa.** Una entrada coincide si su `to` es igual a la ruta actual con **la ruta normalizada** (`normalizePath`, de DEF-F11-021) **y los mismos parámetros de filtro** (`route.query`).
   - Una entrada sin filtro coincide solo con la ruta sin filtro.
   - Una entrada con filtro coincide solo con ese mismo filtro.
   - Pon la comparación en una función pura (por ejemplo `menuItemMatchesRoute(to, route)` en `app/utils/`) y úsala en todos los lugares del componente que hoy comparan `to` con la ruta, incluido `checkActiveRoute`.
2. **La entrada que el usuario tocó manda.**
   - Al hacer clic en una entrada, el menú recuerda **cuál** fue: su `itemKey`, que ya se guarda en `layoutState.activeMenuItem`.
   - Cuando la ruta cambia, **una entrada solo toma el resaltado si la entrada activa actual no coincide ya con la ruta nueva.**
   - Así, con dos entradas para la misma ruta, queda resaltada la que se tocó y la otra no se la quita.
3. **Al entrar por la dirección o al recargar,** cuando no hubo clic: queda resaltada **la primera** entrada que coincida en el orden del menú, y siempre la misma. No puede depender de qué `watch` reaccionó último.
4. **Quita la lógica duplicada:** hay dos `watch` de `route.path` con el mismo cuerpo. Deja uno solo que llame a `handleRouteChange`.
5. **No cambies `AppMenu.vue`:** las entradas repetidas son a propósito, porque cada rol ve su propio grupo. Tampoco cambies las rutas, los permisos ni los modos del menú (estático, slim, horizontal). La lógica de los modos slim y horizontal debe quedar igual.

## Pruebas (Vitest)
Revisa si existe `test/components/layout/AppMenu.spec.ts` y amplíalo, o crea uno para `AppMenuItem`:
- **La función pura:**
  - `/admin/stakeholders` coincide con la ruta sin filtro y **no** con `?rol=CUSTOMER`;
  - `/admin/stakeholders?rol=CUSTOMER` coincide solo con ese filtro;
  - la «/» final no importa.
- **Dos entradas con la misma ruta** en grupos distintos:
  - al hacer clic en la del grupo B, queda activa la del grupo B y no salta a la del grupo A;
  - al volver a hacer clic en la del grupo A, queda la del A.
- **Facturación → Clientes** (`?rol=CUSTOMER`): queda activa esa entrada y no «Listado».
- **Carga directa de una ruta repetida:** queda activa la primera del menú, siempre la misma.

## Verificación
1. `yarn test` en verde, `yarn build` con código 0 y `yarn lint` con no más de 279 errores.
2. **En el navegador**, con el frontend local (`yarn dev`), un Admin y los roles Comercio Exterior y Facturación:
   - Comercio Exterior → Reportes → Movimientos por Depósito **se queda en Comercio Exterior**;
   - Facturación → Movimientos por depósito **se queda en Facturación**;
   - Facturación → Clientes **se queda en Clientes**;
   - Inventario general en cada uno de sus grupos;
   - al recargar la página, el resaltado es estable.

   Puedes usar el API local de tu ambiente de desarrollo. **No toques `wmsdb` ni staging.**

## Ficha
Crea `docs/qa/resultados/defectos/DEF-F11-022.md` con `docs/qa/plantillas/defecto.md`:
- **severidad** MINOR, **módulo** Transversal (menú);
- los pasos del usuario, la causa y la corrección;
- **Estado** «Corregido», con una fila «Detectado» (2026-10-07, reportado por el usuario) y otra «Corregido» con «commits: pendiente».

Agrégala a `INDICE.md`.

## Restricciones
- Trabaja en `develop`. **No crees ramas ni hagas commits**: entrega los mensajes.
- **No redespliegues staging:** lo decide el usuario, porque los operarios están probando. El redespliegue sería solo del frontend (`scripts/deploy-staging.sh frontend`), sin tocar la base.
- Textos y comentarios en español. Nada fuera de este alcance.

## Entrega
1. Los archivos modificados y las entradas repetidas que comprobaste.
2. Las compuertas, con números, y lo que verificaste en el navegador.
3. **Los mensajes de commit:**
   - `fix(menu): el resaltado del menú respeta la entrada elegida y los filtros de la ruta (DEF-F11-022)`;
   - `docs(qa-f11): ficha DEF-F11-022`.

   Los dos terminan con la línea de coautoría que corresponde a tu modelo.
4. El comando para redesplegar solo el frontend en staging, para que lo ejecute el usuario cuando quiera.

**Detente ahí.**
