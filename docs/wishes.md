# Deseos del cliente — TBO Studio

## Propósito y autoridad

TBO Studio transforma el primer contacto de un visitante en una solicitud de proyecto estructurada y útil para iniciar una conversación comercial. El formulario manual y el asistente de voz alimentan la misma solicitud; no son dos productos. El éxito es una consulta revisada por el visitante, aceptada por el backend y encaminada al destino configurado para seguimiento por TBO, no sólo un mensaje visual de éxito.

Este archivo registra deseos, no requisitos aprobados ni integraciones verificadas. Está pendiente de los diagramas y del checkpoint 1. La voz real y la entrega real son objetivos, no capacidades demostradas por el prototipo.

## Fuentes

- **S1 — Cliente TBO, respuesta en esta conversación (2026-11-03):** definición de negocio, usuarios, arquitectura documentada, decisiones de envío preservadas y cuestiones pendientes; fuente principal de esta captura.
- **S2 — [tbodisenio.md](file:///home/tavobecerril/Leadwebsite/tbodisenio.md):** referencia local del prototipo, producto e interacciones; especialmente secciones 1–3 y 19. Ruta externa al repositorio: el enlace no garantiza disponibilidad fuera de esta máquina.
- **S3 — Prototipo [Leadwebsite](file:///home/tavobecerril/Leadwebsite/):** material auxiliar visual y de interacción identificado por S2; no se importa su stack ni se certifica aquí su implementación.
- Los borradores históricos de requisitos y diagramas mencionados por el cliente quedan por localizar y reconciliar; no se convierten en requisitos aprobados por referencia. El prompt visual previo es material auxiliar, no autoridad de negocio o arquitectura.

## Deseos

```yaml wish
id: W-01
statement: Conocer los servicios de TBO e iniciar una consulta de proyecto.
source: Cliente TBO — S1; contexto auxiliar S2
kind: behaviour
```

```yaml wish
id: W-02
statement: Compartir mis datos de contacto para que TBO pueda responderme.
source: Cliente TBO — S1; contexto auxiliar S2
kind: behaviour
```

```yaml wish
id: W-03
statement: Describir mi proyecto mediante preguntas sencillas, pudiendo omitir información opcional.
source: Cliente TBO — S1; contexto auxiliar S2
kind: behaviour
```

```yaml wish
id: W-04
statement: Añadir un mensaje opcional y obtener un resumen de mi consulta.
source: Cliente TBO — S1; contexto auxiliar S2
kind: behaviour
```

```yaml wish
id: W-05
statement: Completar y enviar mi consulta manualmente, sin cuenta ni asistencia de voz.
source: Cliente TBO — S1; contexto auxiliar S2
kind: behaviour
```

```yaml wish
id: W-06
statement: Alternar voz y escritura para completar una misma consulta y resumen.
source: Cliente TBO — S1; contexto auxiliar S2
kind: behaviour
```

```yaml wish
id: W-07
statement: Activar voluntariamente la asistencia de voz de forma segura y privada.
source: Cliente TBO — S1; contexto auxiliar S2
kind: behaviour
```

```yaml wish
id: W-08
statement: Ver reflejada en el formulario la información aceptada del asistente.
source: Cliente TBO — S1; contexto auxiliar S2
kind: behaviour
```

```yaml wish
id: W-09
statement: Entender los fallos de voz y poder continuar de forma controlada.
source: Cliente TBO — S1; contexto auxiliar S2
kind: behaviour
```

```yaml wish
id: W-10
statement: Revisar mi consulta y decidir personalmente cuándo enviarla a TBO.
source: Cliente TBO — S1; contexto auxiliar S2
kind: behaviour
```

```yaml wish
id: W-11
statement: Evitar envíos adicionales mientras mi solicitud está pendiente de respuesta.
source: Cliente TBO — S1; contexto auxiliar S2
kind: behaviour
```

```yaml wish
id: W-12
statement: Hacer llegar al destino comercial únicamente solicitudes validadas por TBO.
source: Cliente TBO — S1; contexto auxiliar S2
kind: behaviour
```

```yaml wish
id: W-13
statement: Recibir confirmación clara de aceptación, sin promesas de seguimiento comercial completado.
source: Cliente TBO — S1; contexto auxiliar S2
kind: behaviour
```

```yaml wish
id: W-14
statement: Conservar mi consulta ante fallos para poder corregirla o reintentar enviarla.
source: Cliente TBO — S1; contexto auxiliar S2
kind: behaviour
```

```yaml wish
id: W-15
statement: Recibir solicitudes con contacto y contexto útiles para el seguimiento comercial.
source: Cliente TBO — S1; contexto auxiliar S2
kind: behaviour
```

```yaml wish
id: W-16
statement: Detectar fallos del servicio sin exponer información personal de los visitantes.
source: Cliente TBO — S1; contexto auxiliar S2
kind: behaviour
```

```yaml wish
id: W-17
statement: Centrar el producto en captación y precalificación, sin funciones comerciales adicionales.
source: Cliente TBO — S1; contexto auxiliar S2
kind: constraint
```

```yaml wish
id: W-18
statement: Mantener responsabilidades separadas y una solución sencilla, sin almacenamiento propio.
source: Cliente TBO — S1; contexto auxiliar S2
kind: constraint
```

```yaml wish
id: W-19
statement: Definir primero el producto y decidir después su tecnología y despliegue.
source: Cliente TBO — S1; contexto auxiliar S2
kind: constraint
```

## Contexto arquitectónico proporcionado, no nueva selección de stack

Cuatro módulos propios: `frontend` (captura, formulario, brief y voz), `token-issuer` (credenciales efímeras), `lead-submitter` (validación y entrega) y `composition-root` (cableado y configuración, sin responsabilidad comercial). Frontend conecta directamente con Gemini Live usando la credencial temporal; el audio no requiere atravesar el backend propio. La clave permanente permanece del lado servidor.

Fronteras externas documentadas: Gemini Live, Lead Webhook, destino comercial configurado, Grafana Loki para logs del backend y Grafana Faro para eventos del navegador. No se exige implementar múltiples destinos simultáneamente. No se ha comprobado aquí la entrega final ni una base de datos propia.

Puertos documentados: `token-issuance-api`, `gemini-token-source`, `voice-session-channel`, `lead-submission-api`, `lead-destination`, `structured-log-sink`, `browser-telemetry-sink`. Los diagramas de etapa 1 conservarán responsabilidades y límites, sin convertir estas referencias en una aprobación de arquitectura de etapa 3.

## Política acordada durante la captura de deseos

**Conflictos IA/manual — respuesta del cliente: opción 1.** Si la IA intenta cambiar un campo que el visitante ya editó manualmente, se conserva la edición manual y se pide confirmación antes de sustituirla. La propuesta de la IA no sobrescribe por sí sola ese valor. Esta respuesta orientará los diagramas; no sustituye la aprobación del checkpoint 1.

**Fallo de voz y reconexión — respuesta del cliente: opción 1.** Mantener el formulario manual disponible; no reconectar automáticamente. Conservar los datos ya incorporados al estado compartido y al brief si la sesión se corta; el visitante puede terminar escribiendo o solicitar una nueva conexión con el micrófono.

**Intención de consumo declarada por el cliente:** una acción explícita de inicio debe habilitar como máximo una solicitud de credencial efímera de un uso (`uses: 1`) y un intento de conexión WebSocket; no gastar llamadas adicionales mediante reintentos automáticos ante saturación o denegación de micrófono. La correspondencia no garantiza que una llamada produzca un token ni que se establezca una conexión: pueden fallar. El cliente acordó obtener primero el permiso de micrófono y bloquear nuevas activaciones mientras el inicio está pendiente; no se afirma aquí soporte verificado del proveedor ni límites vigentes del Free Tier.

**Inicio de voz — respuesta del cliente: opción 1.** Comprobar primero el permiso y la disponibilidad del micrófono; solicitar la credencial sólo si se obtiene acceso. Mientras el inicio esté pendiente se bloquean nuevas activaciones. Si se deniega el permiso o no hay micrófono disponible, no se llama a `token-issuer` y el formulario manual sigue disponible. Esto no verifica cifras de cuota, tiempos de expiración ni compatibilidad específica de navegadores: esos detalles deberán contrastarse con documentación oficial y pruebas antes de la implementación.

**Actualizaciones inválidas o tardías — respuesta del cliente: opción 1.** Un campo desconocido o un valor inválido se rechaza sin mutar el estado compartido ni el brief. En una sesión activa con canal disponible se devuelve un error estructurado correlacionado con el identificador de la llamada, sin afirmar que el dato fue aplicado. Un evento de una sesión cerrada se descarta sin mutación y sin intentar responder por el socket cerrado. La recepción de un evento antiguo no autoriza a responder mediante una sesión nueva.

Historial: los ejemplos de catálogos inicialmente quedaron por reconciliar. El cliente suministró después expresamente los catálogos cerrados de projectType, budget, timeline e industry en la precisión de Preguntas de proyecto al final de este documento; esos valores ya orientan los diagramas, sin sustituir el checkpoint. La forma exacta de `toolCall`/`toolResponse` deberá verificarse con documentación oficial del proveedor al definir los contratos.

**Revisión y envío — respuesta del cliente: opción 1.** Desde el inicio de la revisión y mientras se espera el resultado del envío se bloquean las actualizaciones de IA; se rechazan sin mutar datos y sin encolarlas para aplicación posterior, incluso si el envío falla. El envío usa los datos revisados y confirmados por el visitante. Para dictar o corregir de nuevo se vuelve explícitamente a captura y después se revisa otra vez antes de enviar. Durante un envío pendiente no se habilita una nueva solicitud.

**UX solicitada expresamente:** el brief incluye una acción clara para volver a captura y corregir datos sin perder lo ya capturado; esta capacidad es deseada, no una función que se afirme existente en el prototipo.

Bloquear mutaciones del formulario no equivale a cerrar el canal de voz ni garantiza liberar cuota. El cierre explícito de sesión y recursos al entrar a revisión quedó acordado con la opción 1. Las cifras aportadas sobre latencia, consumo y sesiones del proveedor son justificación del cliente, no mediciones ni límites verificados en esta etapa.

**Cierre de voz — respuesta del cliente: opción 1.** Al entrar a revisión, apagar la voz o fallar el inicio o la sesión, cerrar la conexión que exista y detener micrófono y audio, limpiando también los recursos parcialmente adquiridos durante un inicio fallido. Conservar formulario y brief, descartar eventos de esa sesión y mostrar la voz en reposo. Volver a captura no reinicia la voz: requiere otra pulsación explícita. No se promete un plazo de liberación de cuota del proveedor ni se afirma que cualquier cierre elimine por sí solo todo posible fallo técnico.

## Decisiones pendientes, explícitamente no aprobadas

- Actualizaciones IA durante revisión/envío resueltas: bloqueo sin cola y cierre explícito de voz.
- El tratamiento de campos/valores inválidos y los catálogos de las cuatro preguntas ya están expresamente definidos; queda por precisar el contrato técnico de respuesta.
- Las llamadas de sesiones cerradas se descartan sin mutación ni respuesta por socket cerrado; el mecanismo técnico de identificación de sesión se definirá en diseño.
- Cierre de recursos al fallar acordado; el diseño deberá concretar su ejecución y pruebas sin convertirlo en una garantía infalible.
- La disponibilidad manual y reconexión sólo por acción del visitante ya están acordadas; no requieren nueva decisión.
- Reintento tras timeout: la entrega anterior puede haber ocurrido; el bloqueo local no demuestra deduplicación extremo a extremo.
- Contrato de aceptación frente a persistencia final del destino: no prometer entrega confirmada sólo por recibir 202.

## Diagramas previstos, todavía no aprobados

Arquitectura lógica de sistema con límites de confianza y cableado separado; secuencias por funcionalidad: contacto, correo, preguntas de proyecto, mensaje y brief, envío, voz y actualización de campos. Evitar duplicar cada paso detallado en la vista de arquitectura. Los participantes mantendrán los mismos IDs entre vistas y cada comportamiento tendrá trazabilidad a un deseo.

```yaml wish
id: W-20
statement: Conservar mis datos si falla la voz y poder continuar escribiendo.
source: Cliente TBO — respuesta explícita a la política de reconexión de voz
kind: behaviour
```

```yaml wish
id: W-21
statement: Controlar cada inicio de voz y evitar intentos automáticos innecesarios.
source: Cliente TBO — razón de la política de reconexión manual
kind: behaviour
```

```yaml wish
id: W-22
statement: Revisar un resumen estable y poder volver a corregirlo sin perder información.
source: Cliente TBO — opción 1 y necesidad UX explícita para revisión y envío
kind: behaviour
```

## Precisión del cliente para Contacto

Los tres campos DATOS DE CONTACTO aparecen al abrir o navegar a consulta. Continuar valida `name.trim()`; vacío o espacios muestran `Requerido` sin avanzar y conservando `phone`/`company`. Editar `name` limpia el error. Con contenido se guarda el nombre normalizado y los opcionales, y se sustituye el bloque por DETALLES DEL PROYECTO con Correo Corporativo activo. Esta precisión expresa del cliente desarrolla W-02; no aprueba automáticamente otros borradores históricos.

## Precisión del cliente para Correo

Correo Corporativo admite dominios personales y corporativos y conserva name/phone/company. Sólo Continuar valida `email.trim()`: vacío muestra `Requerido`; no vacío que no cumpla `/^[^\s@]+@[^\s@]+\.[^\s@]+$/` muestra `Email inválido`. Editar limpia el error sin avanzar. Con formato válido al pulsar Continuar se guarda email normalizado mediante trim, Correo queda como fila compacta completada encima y se activa Pregunta 1 (`projectType`). Esta precisión explícita del cliente desarrolla W-02 sin aprobar otros borradores.

### Precisión adicional de Correo

Al continuar con correo válido se persiste `email = email.trim()` y se conservan name/phone/company, no sólo se evalúa un valor temporal. Se usa la regex explícita ya indicada, no la validación HTML5. Editar manualmente o aplicar realmente un email válido por voz limpia `Requerido`/`Email inválido` sin avanzar automáticamente y sin eludir confirmación por conflicto manual. La fila compacta usa ellipsis visual al 55% para valores largos; estado, brief y payload conservan el string completo normalizado.

## Precisión del cliente para Envío

Confirmar el brief revisado con voz cerrada e IA bloqueada inicia pending, bloqueo UI y POST con timeout local de 10 segundos. Rechazo 4xx no llega al webhook y pide corregir; errores de red/timeout/upstream permiten reintentar conservando el brief y liberando pending. Los logs técnicos de rechazo, fallo observado y éxito van por structured-log-sink sin PII; el backend no puede registrar una petición que nunca recibió. Recepción confirmada por integración produce 202 y confirmación estable sin reinicio simulado de 3500 ms, sin afirmar persistencia final del destino. Bloqueo UI no garantiza deduplicación extremo a extremo.

### Precisión adicional de Envío

Las respuestas HTTP de webhook se representan como retornos síncronos. Loki es best-effort, no bloqueante y fail-open; su fallo no impide un 202 por recepción ya confirmada. La espera upstream a webhook se acota a ≤ 10 segundos, sin afirmar cancelación remota o deduplicación garantizada. Frontend registra red/timeout local en Faro por browser-telemetry-sink sin PII y sin bloquear recuperación. Reintentar el mismo brief repite el ciclo del segmento 1 con pending, bloqueo y nuevo timeout. La confirmación final es única y estable, sin reset a los 3500 ms.

## Precisión del cliente para Mensaje y brief

Mensaje opcional en textarea de 3 filas; Enter añade salto de línea, no envía. Continuar persiste message.trim(), cierra voz/micrófono/audio y bloquea llenar_campo antes de la vista de resumen previo al envío (TU BRIEF). El resumen tiene 9 filas ordenadas name, phone, company, email, projectType, budget, timeline, industry, message, con etiquetas/valores humanos y Sin especificar para opcionales vacíos. Volver a captura conserva los 9 campos y no reactiva voz; al solicitar revisar tras editar se revalidan nombre y correo con trim y regex acordada, mostrando errores sin salir de captura si fallan. Si son válidos se cierra voz nuevamente y se muestra brief actualizado. ENVIAR SOLICITUD enlaza con la secuencia envio sólo con voz cerrada e IA bloqueada.

### Precisión adicional de Contacto

Con nombre válido al ejecutar Continuar se persisten `name = name.trim()`, `phone = phone.trim()` y `company = company.trim()` antes de cambiar a DETALLES DEL PROYECTO, de modo que opcionales con sólo espacios queden vacíos y el brief muestre Sin especificar. Editar manualmente o aplicar una actualización válida por voz limpia el error sin abandonar DATOS DE CONTACTO. Enter en esos inputs evalúa Continuar de Contacto, nunca el submit final; no se confunde con avance por el mero hecho de escribir. Se mantienen las políticas de aceptación de voz previamente acordadas.

## Precisión del cliente para Preguntas de proyecto

Cuatro selectores desplegables de opciones (GlassSelect) progresivos con combobox/listbox y flechas sin wrap: Escape o mousedown fuera sólo cierra sin avanzar. Seleccionar clic/Enter guarda código interno, muestra etiqueta humana en fila compacta con ellipsis al 55% y auto-avanza sin Continuar. Prefiero no decir / Siguiente conserva string vacío, respeta previas y avanza; en brief es Sin especificar. Orden y catálogos explícitos: projectType = landing | ecommerce | webapp | redesign | automation | other; budget = lt10k | 10to20k | 20to30k | quote; timeline = urgent | 1to3 | 3to6 | flexible; industry = retail | health | education | realestate | tech | services | other. Tras P4 se presenta message. Estos catálogos ya fueron suministrados expresamente por el cliente, no son inferencia de un borrador. Una llamada externa/voz fuera de ellos se rechaza al recibirla, sin mutar estado.

### Precisión adicional de GlassSelect

El combobox abre con clic, Enter, Espacio o ArrowDown y desplaza con flechas sin wrap. Al cambiar pregunta por selección u omisión cierra listbox y reinicia highlightedIndex, sin heredar estado. Omitir conserva "" y no añade fila compacta: sólo se apilan respondidas; Sin especificar aparece en TU BRIEF.

## Precisión del cliente para voz y actualización compartida

Con WSS activo y orbe escuchando (listening), Gemini devuelve voz y/o llenar_campo(id,campo,valor). En captura vigente, un dato válido se normaliza, limpia error previo y se refleja antes de ok. Si había edición manual se pide confirmación: aceptar aplica y responde ok; rechazar conserva edición y responde rejected. Datos desconocidos o inválidos se rechazan sin mutar y responden error sólo con canal vigente abierto; sesiones cerradas, revisión o pending descartan sin mutar ni enviar por socket cerrado. Fallo, desconexión o apagado cierra voz/micrófono/audio, deja el orbe en reposo (solving) y datos/manual disponibles, sin reconexión automática. Faro recibe telemetría técnica sin PII ni audio, best-effort.

### Precisión final de actualización por voz

Cerrar voz por fallo, apagado o revisión cancela automáticamente confirmaciones de conflicto manual pendientes conservando el dato manual. Una aceptación tardía no revive la operación. Aplicar realmente un catálogo válido por voz apila su etiqueta humana y cierra GlassSelect si estaba abierto. Los toolCall tardíos se descartan sin mutar ni encolar y conservan el brief intacto.

## Precisión del cliente para cierre y recuperación manual

Apagar micrófono o entrar a TU BRIEF cierra WSS, micrófono mediante MediaStreamTrack.stop() y audio, deja el orbe en reposo (solving) y cancela confirmaciones manuales pendientes sin perder datos. Fallos de inicio/sesión/red/GoAway/cuota mantienen manual disponible y emiten Faro sin PII/audio best-effort, sin reconexión automática. Audio y toolCall tardíos se descartan sin mutar, encolar, reproducir audio ni responder en socket cerrado. Volver a captura no activa voz; una nueva pulsación recorre voz-inicio con permiso, token efímero nuevo uses:1 sin reutilizar el consumido y contexto de campos previos en la nueva sesión. El límite de 3 sesiones citado es supuesto cliente, no verificación de cuota vigente.

## Precisión del cliente para inicio de voz

Pulsar micrófono en captura bloquea activaciones mientras inicia y solicita getUserMedia antes de cualquier credencial; denegación o falta de dispositivo libera bloqueo y mantiene el orbe en reposo (solving) y la captura manual disponible sin llamar token-issuer. Con permiso, token-issuance-api pide credencial a servidor, que usa gemini-token-source con clave permanente para token efímero uses:1 y newSessionExpireTime. Loki recibe evento async sin PII/clave, best-effort y no bloquea HTTP. Sólo token válido abre WSS directo; sesión configurada con systemInstruction/llenar_campo y contexto previo antes de que el orbe indique que está escuchando (listening) y se habilite hablar. Fallo de emisión o WSS limpia micrófono inmediato mediante MediaStreamTrack.stop(), audio y socket parcial, libera bloqueo, conserva datos/manual, no reutiliza token ni reconecta automáticamente y emite Faro sin PII/audio best-effort. Cuotas, duración y setup exactos siguen pendientes de verificación de proveedor en diseño.

## Precisiones de alcance preservadas

- **W-01:** Entender qué ofrece TBO y encontrar cómo iniciar una consulta sobre landing pages, e-commerce, aplicaciones web, rediseños o migraciones, automatización con IA u otros proyectos por evaluar.
- **W-17:** Limitar el producto a captación y precalificación informativa sin CRM propio, dashboard comercial, cuentas de clientes, pagos, scoring de leads, cotizaciones automáticas ni propuestas comerciales autónomas.
- **W-18:** Conservar como referencia arquitectónica documentada la separación hexagonal de frontend, token-issuer, lead-submitter y composition-root sin tratar el formulario, panel de voz u orbe como módulos independientes ni añadir una base de datos propia.
- **W-19:** Separar la definición del producto de la futura decisión de stack y despliegue, pues Vercel es antecedente histórico y Hostinger una alternativa no decidida.
