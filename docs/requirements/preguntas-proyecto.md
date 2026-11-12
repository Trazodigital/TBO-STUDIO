# preguntas-proyecto

Borrador de etapa 2; pendiente de revisión independiente de criterios y Checkpoint 2.

## REQ-0046

```yaml requirement
uid: REQ-0046
level: software
kind: functional
criticality: medium
statement: La _captura_ presenta una sola pregunta de proyecto activa.
acceptance_criteria:
- case: happy
  given: correo confirmado
  when: se abren detalles
  then: presenta projectType con respuestas previas encima
- case: edge
  given: correo confirmado
  when: existen preguntas pendientes
  then: no las presenta como inputs libres simultáneos
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: preguntas-proyecto#INV-1
refines: REQ-0002
```

## REQ-0047

```yaml requirement
uid: REQ-0047
level: software
kind: functional
criticality: high
statement: El selector admite las interacciones de teclado acordadas.
acceptance_criteria:
- case: happy
  given: pregunta activa
  when: se pulsa clic, Enter, Espacio o ArrowDown
  then: abre la lista y permite flechas sin wrap
- case: error
  given: pregunta activa
  when: se pulsa Escape o mousedown fuera
  then: cierra sin cambiar dato ni pregunta
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: preguntas-proyecto#INV-2
refines: REQ-0002
```

## REQ-0048

```yaml requirement
uid: REQ-0048
level: software
kind: functional
criticality: high
statement: Una selección de catálogo avanza sin confirmación adicional.
acceptance_criteria:
- case: happy
  given: pregunta de proyecto activa
  when: se elige opción con clic o Enter, o se acepta y aplica por voz
  then: guarda código, apila etiqueta humana, cierra lista abierta y activa inmediatamente la siguiente pregunta
- case: error
  given: opción de catálogo seleccionada o aplicada por voz
  when: no se pulsa Continuar
  then: el avance ya está efectuado
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: preguntas-proyecto#INV-3
refines: REQ-0002
```

## REQ-0049

```yaml requirement
uid: REQ-0049
level: software
kind: functional
criticality: medium
statement: Las filas compactas conservan el valor completo.
acceptance_criteria:
- case: happy
  given: respuesta confirmada
  when: se presenta encima de la pregunta activa
  then: muestra etiqueta humana con ellipsis al 55 %
- case: edge
  given: respuesta confirmada
  when: la etiqueta es larga
  then: el código almacenado no se recorta
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: preguntas-proyecto#INV-4
refines: REQ-0002
```

## REQ-0050

```yaml requirement
uid: REQ-0050
level: software
kind: functional
criticality: high
statement: Omitir una pregunta conserva su valor vacío.
acceptance_criteria:
- case: happy
  given: pregunta opcional activa
  when: se pulsa Prefiero no decir / Siguiente
  then: guarda cadena vacía sin añadir fila compacta
- case: error
  given: pregunta opcional activa
  when: ya hay otras respuestas
  then: las conserva intactas
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: preguntas-proyecto#INV-5
refines: REQ-0002
```

## REQ-0051

```yaml requirement
uid: REQ-0051
level: software
kind: functional
criticality: medium
statement: Abrir o cerrar el selector no confirma una respuesta.
acceptance_criteria:
- case: happy
  given: pregunta activa
  when: se abre y cierra sin elegir
  then: permanece en la misma pregunta
- case: edge
  given: pregunta activa
  when: se omite explícitamente
  then: avanza por omisión, no por apertura
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: preguntas-proyecto#INV-6
refines: REQ-0002
```

## REQ-0052

```yaml requirement
uid: REQ-0052
level: software
kind: functional
criticality: high
statement: Las preguntas aceptan exclusivamente sus catálogos aprobados.
acceptance_criteria:
- case: happy
  given: pregunta activa
  when: se selecciona un código del catálogo correspondiente
  then: acepta el código exacto
- case: error
  given: pregunta activa
  when: se propone código fuera de catálogo
  then: rechaza sin alterar formulario
- case: edge
  given: pregunta projectType activa
  when: se muestran sus opciones o la respuesta confirmada en el _brief_
  then: 'landing: Landing Page; ecommerce: E-commerce; webapp: Aplicación Web; redesign: Rediseño / Migración; automation: Automatización con IA; other: Otro'
- case: edge
  given: pregunta budget activa
  when: se muestran sus opciones o la respuesta confirmada en el _brief_
  then: 'lt10k: Menos de $10,000 MXN; 10to20k: $10,000 – $20,000 MXN; 20to30k: $20,000 – $30,000 MXN; quote: Prefiero cotizar'
- case: edge
  given: pregunta timeline activa
  when: se muestran sus opciones o la respuesta confirmada en el _brief_
  then: 'urgent: Urgente (menos de 1 mes); 1to3: 1 – 3 meses; 3to6: 3 – 6 meses; flexible: Sin fecha definida'
- case: edge
  given: pregunta industry activa
  when: se muestran sus opciones o la respuesta confirmada en el _brief_
  then: 'retail: Retail / E-commerce; health: Salud; education: Educación; realestate: Bienes Raíces; tech: Tecnología / SaaS; services: Servicios Profesionales; other: Otro'
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: preguntas-proyecto#INV-7
refines: REQ-0002
```

## REQ-0053

```yaml requirement
uid: REQ-0053
level: software
kind: functional
criticality: medium
statement: Las preguntas respetan el orden de proyecto acordado.
acceptance_criteria:
- case: happy
  given: projectType activo
  when: se confirma u omite cada pregunta
  then: recorre projectType, budget, timeline, industry y message
- case: edge
  given: projectType activo
  when: se omite industry
  then: abre message igualmente
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: preguntas-proyecto#INV-8
refines: REQ-0002
```

## REQ-0054

```yaml requirement
uid: REQ-0054
level: software
kind: functional
criticality: medium
statement: Una actualización externa fuera de catálogo no muta datos.
acceptance_criteria:
- case: happy
  given: _sesión de voz_ vigente
  when: llenar_campo trae un código ajeno al catálogo
  then: responde error correlacionado sin aplicar
- case: edge
  given: propuesta fuera de catálogo recibida tras cierre
  when: el canal está cerrado
  then: descarta sin responder por ese canal
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: preguntas-proyecto#INV-9
refines: REQ-0002
```

## REQ-0055

```yaml requirement
uid: REQ-0055
level: software
kind: functional
criticality: high
statement: Responder preguntas no envía la _solicitud_.
acceptance_criteria:
- case: happy
  given: _captura_ activa
  when: se selecciona u omite una opción
  then: no ejecuta POST comercial
- case: error
  given: _captura_ activa
  when: no existe _sesión de voz_
  then: la selección manual funciona
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: preguntas-proyecto#INV-10
refines: REQ-0002
```

## REQ-0056

```yaml requirement
uid: REQ-0056
level: software
kind: functional
criticality: medium
statement: El selector reinicia su estado al cambiar de pregunta.
acceptance_criteria:
- case: happy
  given: lista con opción resaltada
  when: se selecciona u omite y avanza
  then: cierra lista y reinicia índice activo
- case: edge
  given: lista con opción resaltada
  when: la pregunta anterior tenía otra opción activa
  then: no la hereda en la siguiente
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: preguntas-proyecto#INV-11
refines: REQ-0002
```

## REQ-0138

```yaml requirement
uid: REQ-0138
level: software
kind: functional
criticality: high
statement: El _visitante_ puede omitir las cuatro preguntas de proyecto.
acceptance_criteria:
- case: happy
  given: projectType activo
  when: omite cada pregunta
  then: alcanza message con cuatro vacíos
- case: error
  given: projectType activo
  when: hay respuestas anteriores
  then: no las elimina al omitir otra
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: preguntas-proyecto#visitor
refines: REQ-0001
```

## REQ-0139

```yaml requirement
uid: REQ-0139
level: software
kind: functional
criticality: high
statement: La interfaz muestra etiquetas humanas de opciones confirmadas.
acceptance_criteria:
- case: happy
  given: opción seleccionada
  when: se apila su respuesta
  then: muestra su etiqueta, no el código
- case: error
  given: pregunta opcional activa
  when: opción omitida
  then: no añade fila compacta
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: preguntas-proyecto#frontend
refines: REQ-0002
```

## REQ-0172

```yaml requirement
uid: REQ-0172
level: software
kind: observability
criticality: medium
statement: La instrumentación emite los eventos técnicos esperados del flujo de preguntas de proyecto.
acceptance_criteria:
- case: happy
  given: intentos técnicos del flujo con receptor disponible
  when: se ejecutan todos los casos de aceptación
  then: emite tbo.preguntas_proyecto.start y tbo.preguntas_proyecto.end con event, requirement=REQ-0172 y correlation_id del intento
- case: edge
  given: intentos técnicos del flujo con receptor disponible
  when: el caso termina en error
  then: emite tbo.preguntas_proyecto.error en lugar de tbo.preguntas_proyecto.end con event, requirement=REQ-0172 y correlation_id del intento
feasibility: Viable con señales técnicas sin contenido; una prueba de integración @sdoc[REQ-0172] comprueba literalmente los eventos y sus tres campos obligatorios.
size: S
environment:
- element: receptores externos de telemetría
  impact: envíos técnicos best-effort sin garantía de persistencia ni contenido personal
derived_from: preguntas-proyecto#frontend
refines: REQ-0017
metric: eventos esperados emitidos con receptor disponible
threshold: == 100 %
measurement_method:
  instrument: integration
  window: one test run
  sample: every acceptance criterion (happy, edge, error) of REQ-0046, REQ-0047, REQ-0048, REQ-0049, REQ-0050, REQ-0051, REQ-0052, REQ-0053, REQ-0054, REQ-0055, REQ-0056, REQ-0138, REQ-0139; receiver available
events:
- tbo.preguntas_proyecto.start
- tbo.preguntas_proyecto.end
- tbo.preguntas_proyecto.error
watched_by:
- 'Comprobación de integración: cada evento esperado y sus campos event, requirement y correlation_id; ausencia detectada hace fallar la prueba.'
```

## REQ-0173

```yaml requirement
uid: REQ-0173
level: software
kind: security
criticality: high
statement: Los eventos del flujo de preguntas de proyecto excluyen datos personales, campos, audio y credenciales.
acceptance_criteria:
- case: happy
  given: casos con datos señuelo
  when: se emiten eventos de todos los resultados
  then: no incluyen PII, campos, audio, tokens ni claves
- case: error
  given: casos con datos señuelo
  when: se produce un error con datos capturados
  then: el evento no filtra esos datos
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: receptores externos de telemetría
  impact: envíos técnicos best-effort sin garantía de persistencia ni contenido personal
derived_from: preguntas-proyecto#frontend
refines: REQ-0017
metric: filtraciones de datos protegidos en eventos
threshold: == 0 filtraciones
measurement_method:
  instrument: security
  window: one test run
  sample: every applicable acceptance criterion with canary data
```

## REQ-0174

```yaml requirement
uid: REQ-0174
level: software
kind: reliability
criticality: high
statement: Los fallos de telemetría no alteran ni bloquean el resultado del flujo de preguntas de proyecto.
acceptance_criteria:
- case: happy
  given: mismos casos funcionales con y sin sink disponible
  when: el sink falla o permanece sin resolver
  then: el resultado coincide sin esperar al sink
- case: error
  given: mismos casos funcionales con y sin sink disponible
  when: el sink lanza error al emitir evento del paso
  then: conserva los datos y el estado del paso sin bloqueo
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: receptores externos de telemetría
  impact: envíos técnicos best-effort sin garantía de persistencia ni contenido personal
derived_from: preguntas-proyecto#frontend
refines: REQ-0025
metric: alteraciones o bloqueos funcionales por fallo del sink
threshold: == 0 alteraciones
measurement_method:
  instrument: integration
  window: one test run
  sample: every applicable acceptance criterion with failing and indefinitely pending sinks
```

