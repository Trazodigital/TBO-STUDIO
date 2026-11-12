# recorrido-general

Borrador de etapa 2; pendiente de revisión independiente de criterios y Checkpoint 2.

## REQ-0121

```yaml requirement
uid: REQ-0121
level: software
kind: functional
criticality: high
statement: El recorrido integrado conserva las reglas de sus subflujos.
acceptance_criteria:
- case: happy
  given: secuencias funcionales aprobadas
  when: se recorre consulta completa
  then: aplica reglas detalladas sin introducir validaciones distintas
- case: error
  given: secuencias funcionales aprobadas
  when: se consulta esta vista macro
  then: no duplica los intentos de subflujo
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#INV-1
refines: REQ-0021
```

## REQ-0122

```yaml requirement
uid: REQ-0122
level: software
kind: functional
criticality: high
statement: Las rutas manual y asistida alimentan la misma _solicitud_.
acceptance_criteria:
- case: happy
  given: _captura_ disponible
  when: el _visitante_ alterna escritura y voz
  then: ambas actualizan los mismos datos aceptados
- case: error
  given: _captura_ disponible
  when: falla voz
  then: puede terminar manualmente
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#INV-2
refines: REQ-0021
```

## REQ-0123

```yaml requirement
uid: REQ-0123
level: software
kind: functional
criticality: high
statement: La ruta manual mantiene el orden de _captura_ aprobado.
acceptance_criteria:
- case: happy
  given: consulta iniciada
  when: se completa manualmente
  then: recorre contacto, correo y preguntas
- case: error
  given: consulta iniciada
  when: se omiten preguntas opcionales
  then: continúa a mensaje sin depender de Gemini
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#INV-3
refines: REQ-0021
```

## REQ-0124

```yaml requirement
uid: REQ-0124
level: software
kind: functional
criticality: high
statement: La autorización del recorrido se obtiene por el emisor.
acceptance_criteria:
- case: happy
  given: permiso concedido
  when: se solicita voz
  then: recibe _credencial efímera_ de token-issuer
- case: error
  given: permiso concedido
  when: el emisor falla
  then: no conecta usando la clave permanente
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#INV-4
refines: REQ-0021
```

## REQ-0125

```yaml requirement
uid: REQ-0125
level: software
kind: functional
criticality: high
statement: La voz no confirma automáticamente la entrega comercial.
acceptance_criteria:
- case: happy
  given: _captura_ asistida activa
  when: se incorporan datos dictados
  then: el _visitante_ conserva la decisión de enviar
- case: error
  given: _captura_ asistida activa
  when: el asistente propone envío
  then: no sustituye confirmación humana
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#INV-5
refines: REQ-0021
```

## REQ-0126

```yaml requirement
uid: REQ-0126
level: software
kind: functional
criticality: high
statement: La _revisión_ integrada utiliza un _brief_ estable.
acceptance_criteria:
- case: happy
  given: _captura_ concluida
  when: se solicita _revisión_
  then: cierra voz y bloquea IA antes del _brief_
- case: error
  given: _captura_ concluida
  when: se modifica un dato volviendo a _captura_
  then: exige nueva _revisión_
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#INV-6
refines: REQ-0021
```

## REQ-0127

```yaml requirement
uid: REQ-0127
level: software
kind: functional
criticality: high
statement: La validación integrada precede a la frontera comercial.
acceptance_criteria:
- case: happy
  given: _brief_ confirmado
  when: lead-submitter recibe la _solicitud_
  then: valida antes de llamar al webhook
- case: error
  given: _brief_ confirmado
  when: el payload es inválido
  then: no cruza esa frontera
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#INV-7
refines: REQ-0021
```

## REQ-0128

```yaml requirement
uid: REQ-0128
level: software
kind: functional
criticality: high
statement: El recorrido distingue aceptación de persistencia comercial.
acceptance_criteria:
- case: happy
  given: webhook confirma recepción
  when: se recibe HTTP 202
  then: informa _solicitud_ aceptada
- case: error
  given: webhook confirma recepción
  when: no hay evidencia de persistencia final
  then: no afirma seguimiento completado
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#INV-8
refines: REQ-0021
```

## REQ-0129

```yaml requirement
uid: REQ-0129
level: software
kind: functional
criticality: high
statement: El recorrido mantiene la recuperación de fallos de entrega.
acceptance_criteria:
- case: happy
  given: _brief_ confirmado
  when: el intento falla
  then: conserva _brief_ según la rama de envio
- case: error
  given: _brief_ confirmado
  when: se agota timeout local
  then: no afirma ausencia de entrega remota
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#INV-9
refines: REQ-0021
```

## REQ-0130

```yaml requirement
uid: REQ-0130
level: software
kind: functional
criticality: high
statement: El POST integrado termina en lead-submitter.
acceptance_criteria:
- case: happy
  given: _brief_ revisado
  when: el _visitante_ confirma envío
  then: activa pending y envía al backend propio
- case: error
  given: _brief_ revisado
  when: se pulsa otra vez durante pending
  then: no envía directamente a webhook
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#INV-10
refines: REQ-0021
```

## REQ-0131

```yaml requirement
uid: REQ-0131
level: software
kind: functional
criticality: high
statement: La consulta integrada muestra contacto sin selección previa de ruta.
acceptance_criteria:
- case: happy
  given: sitio abierto
  when: se accede a _captura_
  then: muestra DATOS DE CONTACTO y panel solving
- case: error
  given: sitio abierto
  when: no se elige manual o voz
  then: el formulario ya está disponible
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#INV-11
refines: REQ-0021
```

## REQ-0132

```yaml requirement
uid: REQ-0132
level: software
kind: functional
criticality: high
statement: Las propuestas de voz reciben resolución en el mismo canal vigente.
acceptance_criteria:
- case: happy
  given: _sesión de voz_ activa
  when: Gemini emite llenar_campo
  then: frontend aplica reglas y devuelve toolResponse
- case: error
  given: _sesión de voz_ activa
  when: la propuesta no es aceptada
  then: no muta formulario ni _brief_
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#INV-12
refines: REQ-0021
```

## REQ-0133

```yaml requirement
uid: REQ-0133
level: software
kind: functional
criticality: high
statement: La observabilidad del recorrido mantiene separación de receptores.
acceptance_criteria:
- case: happy
  given: recorrido instrumentado
  when: se emite un evento técnico
  then: frontend usa Faro y backend Loki
- case: error
  given: recorrido instrumentado
  when: se necesita registro comercial
  then: los eventos no lo sustituyen
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#INV-13
refines: REQ-0021
```

## REQ-0159

```yaml requirement
uid: REQ-0159
level: software
kind: functional
criticality: high
statement: El _visitante_ controla el paso de _revisión_ a entrega.
acceptance_criteria:
- case: happy
  given: _brief_ visible
  when: confirma enviar
  then: inicia una entrega explícita
- case: error
  given: _brief_ visible
  when: sólo habla al asistente
  then: no autoriza entrega
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#visitor
refines: REQ-0001
```

## REQ-0160

```yaml requirement
uid: REQ-0160
level: software
kind: functional
criticality: high
statement: El recorrido completo funciona sin iniciar voz.
acceptance_criteria:
- case: happy
  given: formulario abierto
  when: se completa manualmente
  then: alcanza respuesta de aceptación o recuperación
- case: error
  given: formulario abierto
  when: Gemini no está disponible
  then: no bloquea ruta manual
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#frontend
refines: REQ-0002
```

## REQ-0161

```yaml requirement
uid: REQ-0161
level: software
kind: functional
criticality: high
statement: La autorización integrada no expone la clave permanente.
acceptance_criteria:
- case: happy
  given: ruta de voz elegida
  when: el servidor responde al navegador
  then: devuelve sólo _credencial efímera_
- case: error
  given: ruta de voz elegida
  when: falla emisión
  then: no revela clave en error
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#token-issuer
refines: REQ-0003
```

## REQ-0162

```yaml requirement
uid: REQ-0162
level: software
kind: functional
criticality: high
statement: Las propuestas integradas se evalúan antes de actualizar datos.
acceptance_criteria:
- case: happy
  given: _sesión de voz_ vigente
  when: llega llenar_campo válido y aceptado
  then: refleja el dato en formulario y _brief_
- case: error
  given: _sesión de voz_ vigente
  when: llega código inválido
  then: conserva el dato previo
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#gemini-live
refines: REQ-0004
```

## REQ-0163

```yaml requirement
uid: REQ-0163
level: software
kind: functional
criticality: high
statement: La entrega integrada valida en el servidor propio.
acceptance_criteria:
- case: happy
  given: _brief_ confirmado
  when: llega POST
  then: valida antes de reenviar
- case: error
  given: _brief_ confirmado
  when: payload inválido
  then: no llama al webhook
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#lead-submitter
refines: REQ-0005
```

## REQ-0164

```yaml requirement
uid: REQ-0164
level: software
kind: functional
criticality: high
statement: La integración devuelve recepción al servidor propio.
acceptance_criteria:
- case: happy
  given: _solicitud_ reenviada al webhook
  when: el webhook responde HTTP 2xx, incluso sin cuerpo
  then: lead-submitter considera confirmada la recepción y devuelve 202 Accepted
- case: error
  given: _solicitud_ reenviada
  when: falla webhook
  then: no acredita aceptación
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#lead-webhook
refines: REQ-0006
```

## REQ-0165

```yaml requirement
uid: REQ-0165
level: software
kind: functional
criticality: high
statement: La aceptación integrada no promete persistencia final.
acceptance_criteria:
- case: happy
  given: HTTP 202 recibido
  when: se presenta confirmación
  then: informa aceptación sin afirmar seguimiento completado
- case: error
  given: HTTP 202 recibido
  when: no existe evidencia del receptor final
  then: no inventa persistencia
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#commercial-destination
refines: REQ-0007
```

## REQ-0188

```yaml requirement
uid: REQ-0188
level: software
kind: observability
criticality: medium
statement: La instrumentación emite los eventos técnicos esperados del flujo de recorrido general.
acceptance_criteria:
- case: happy
  given: límites del recorrido completo con receptor disponible
  when: se ejecutan todos los casos de aceptación
  then: emite tbo.recorrido_general.start y tbo.recorrido_general.end con event, requirement=REQ-0188 y correlation_id del intento
- case: edge
  given: límites del recorrido completo con receptor disponible
  when: el caso termina en error
  then: emite tbo.recorrido_general.error en lugar de tbo.recorrido_general.end con event, requirement=REQ-0188 y correlation_id del intento
- case: edge
  given: recorrido con subflujos instrumentados
  when: una prueba de integración recorre desde entrada a resultado de entrega
  then: observa los tres nombres propios del recorrido entre los casos exitosos y fallidos sin duplicar emisiones de eventos de subflujos
feasibility: Viable con hitos propios de entrada y resultado global; una prueba de integración @sdoc[REQ-0188] comprueba literalmente los eventos del recorrido y la ausencia de emisiones duplicadas de subflujos.
size: S
environment:
- element: receptores externos de telemetría
  impact: envíos técnicos best-effort sin garantía de persistencia ni contenido personal
derived_from: recorrido-general#INV-13
refines: REQ-0017
metric: eventos esperados emitidos con receptor disponible
threshold: == 100 %
measurement_method:
  instrument: integration
  window: one test run
  sample: every acceptance criterion (happy, edge, error) of REQ-0121, REQ-0122, REQ-0123, REQ-0124, REQ-0125, REQ-0126, REQ-0127, REQ-0128, REQ-0129, REQ-0130, REQ-0131, REQ-0132, REQ-0133, REQ-0159, REQ-0160, REQ-0161, REQ-0162, REQ-0163, REQ-0164, REQ-0165; receiver available
events:
- tbo.recorrido_general.start
- tbo.recorrido_general.end
- tbo.recorrido_general.error
watched_by:
- 'Comprobación de integración: cada evento esperado y sus campos event, requirement y correlation_id; ausencia detectada hace fallar la prueba.'
```

## REQ-0189

```yaml requirement
uid: REQ-0189
level: software
kind: security
criticality: high
statement: Los eventos del flujo de recorrido general excluyen datos personales, campos, audio y credenciales.
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
derived_from: recorrido-general#frontend
refines: REQ-0017
metric: filtraciones de datos protegidos en eventos
threshold: == 0 filtraciones
measurement_method:
  instrument: security
  window: one test run
  sample: every applicable acceptance criterion with canary data
```

## REQ-0190

```yaml requirement
uid: REQ-0190
level: software
kind: reliability
criticality: high
statement: Los fallos de telemetría no alteran ni bloquean el resultado del flujo de recorrido general.
acceptance_criteria:
- case: happy
  given: mismos casos funcionales con y sin sink disponible
  when: el sink falla o permanece sin resolver
  then: el resultado coincide sin esperar al sink
- case: error
  given: mismos casos funcionales con y sin sink disponible
  when: el flujo incluye envío comercial
  then: mantiene el timeout de envío de como máximo 10 s
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: receptores externos de telemetría
  impact: envíos técnicos best-effort sin garantía de persistencia ni contenido personal
derived_from: recorrido-general#frontend
refines: REQ-0025
metric: alteraciones o bloqueos funcionales por fallo del sink
threshold: == 0 alteraciones
measurement_method:
  instrument: integration
  window: one test run
  sample: every applicable acceptance criterion with failing and indefinitely pending sinks
```

## REQ-0203

```yaml requirement
uid: REQ-0203
level: software
kind: constraint
criticality: high
statement: El recorrido termina en aceptación informativa para seguimiento externo.
acceptance_criteria:
- case: happy
  given: _solicitud_ aceptada
  when: finaliza el recorrido
  then: no genera cotización ni propuesta autónoma
- case: error
  given: _solicitud_ aceptada
  when: se solicita pago o cuenta de cliente
  then: no forma parte de este recorrido
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#INV-8
refines: REQ-0027
```

## REQ-0205

```yaml requirement
uid: REQ-0205
level: software
kind: constraint
criticality: medium
statement: El contrato del recorrido no impone un stack no aprobado.
acceptance_criteria:
- case: happy
  given: reglas funcionales aprobadas
  when: se especifica recorrido integrado
  then: no exige implementación ni alojamiento concreto
- case: edge
  given: reglas funcionales aprobadas
  when: se menciona antecedente histórico
  then: no se convierte en selección vigente
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: recorrido-general#INV-1
refines: REQ-0029
```

