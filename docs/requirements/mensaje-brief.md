# mensaje-brief

Borrador de etapa 2; pendiente de revisión independiente de criterios y Checkpoint 2.

## REQ-0057

```yaml requirement
uid: REQ-0057
level: software
kind: functional
criticality: medium
statement: El mensaje opcional admite saltos de línea sin submit.
acceptance_criteria:
- case: happy
  given: pregunta de mensaje activa
  when: se pulsa Enter
  then: inserta salto de línea en textarea de tres filas
- case: edge
  given: pregunta de mensaje activa
  when: el mensaje está vacío
  then: no envía ni avanza por Enter
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: mensaje-brief#INV-1
refines: REQ-0021
```

## REQ-0058

```yaml requirement
uid: REQ-0058
level: software
kind: functional
criticality: high
statement: Continuar guarda el mensaje recortado antes de _revisión_.
acceptance_criteria:
- case: happy
  given: mensaje escrito o vacío
  when: se pulsa Continuar
  then: persiste message.trim() antes del _brief_
- case: error
  given: mensaje escrito o vacío
  when: sólo contiene espacios
  then: persiste cadena vacía
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: mensaje-brief#INV-2
refines: REQ-0021
```

## REQ-0059

```yaml requirement
uid: REQ-0059
level: software
kind: functional
criticality: high
statement: El _brief_ presenta las nueve filas en el orden acordado.
acceptance_criteria:
- case: happy
  given: datos capturados
  when: se abre _revisión_
  then: muestra name, phone, company, email, projectType, budget, timeline, industry y message
- case: error
  given: datos capturados
  when: un opcional está vacío
  then: muestra Sin especificar con etiquetas humanas
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: mensaje-brief#INV-3
refines: REQ-0021
```

## REQ-0060

```yaml requirement
uid: REQ-0060
level: software
kind: functional
criticality: medium
statement: Volver a _captura_ conserva los nueve campos.
acceptance_criteria:
- case: happy
  given: _brief_ visible
  when: el _visitante_ solicita corregir
  then: restaura los nueve valores en _captura_ para editar directamente el dato deseado y solicitar _revisión_ sin reconfirmar los demás pasos
- case: edge
  given: _brief_ visible
  when: la voz estuvo activa antes
  then: no la reinicia automáticamente
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: mensaje-brief#INV-4
refines: REQ-0021
```

## REQ-0061

```yaml requirement
uid: REQ-0061
level: software
kind: functional
criticality: high
statement: La _revisión_ posterior a edición revalida los obligatorios.
acceptance_criteria:
- case: happy
  given: datos corregidos
  when: se solicita revisar
  then: exige name.trim() no vacío y email.trim() válido por la regex acordada
- case: error
  given: datos corregidos
  when: nombre o correo vacíos o correo mal formado
  then: retiene _captura_ con Requerido o Email inválido
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: mensaje-brief#INV-5
refines: REQ-0021
```

## REQ-0062

```yaml requirement
uid: REQ-0062
level: software
kind: functional
criticality: medium
statement: Editar datos no abre _revisión_ por sí solo.
acceptance_criteria:
- case: happy
  given: _captura_ restaurada
  when: el _visitante_ modifica un campo
  then: permanece en _captura_
- case: edge
  given: _captura_ restaurada
  when: se limpia un error
  then: no abre el _brief_ sin solicitar revisar
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: mensaje-brief#INV-6
refines: REQ-0021
```

## REQ-0063

```yaml requirement
uid: REQ-0063
level: software
kind: functional
criticality: high
statement: La _revisión_ posterior conserva la normalización acordada.
acceptance_criteria:
- case: happy
  given: obligatorios válidos
  when: se solicita revisar
  then: persiste name.trim(), email.trim() y message.trim()
- case: error
  given: obligatorios válidos
  when: hay respuestas opcionales previas
  then: no las pierde
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: mensaje-brief#INV-7
refines: REQ-0021
```

## REQ-0064

```yaml requirement
uid: REQ-0064
level: software
kind: functional
criticality: medium
statement: Enviar desde _revisión_ enlaza un único intento de entrega.
acceptance_criteria:
- case: happy
  given: _brief_ visible con voz cerrada
  when: se pulsa ENVIAR _SOLICITUD_
  then: entra una vez al flujo envio
- case: edge
  given: consulta en curso
  when: la _captura_ aún está activa
  then: no permite envío final desde este paso
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: mensaje-brief#INV-8
refines: REQ-0021
```

## REQ-0065

```yaml requirement
uid: REQ-0065
level: software
kind: functional
criticality: medium
statement: La corrección del _brief_ es opcional.
acceptance_criteria:
- case: happy
  given: _brief_ visible
  when: el _visitante_ confirma sin corregir
  then: puede iniciar envio sin recorrer edición
- case: edge
  given: _brief_ visible
  when: el _visitante_ vuelve repetidamente a corregir
  then: conserva campos entre recorridos
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: mensaje-brief#INV-9
refines: REQ-0021
```

## REQ-0066

```yaml requirement
uid: REQ-0066
level: software
kind: functional
criticality: high
statement: La _revisión_ bloquea las actualizaciones del asistente.
acceptance_criteria:
- case: happy
  given: _captura_ con voz activa
  when: se solicita _revisión_
  then: cierra voz y recursos antes de mostrar el _brief_
- case: error
  given: _revisión_ activa con voz cerrada
  when: llega una propuesta tardía
  then: no modifica ni encola cambios
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: mensaje-brief#INV-10
refines: REQ-0021
```

## REQ-0140

```yaml requirement
uid: REQ-0140
level: software
kind: functional
criticality: high
statement: El _visitante_ puede solicitar corrección desde el _brief_.
acceptance_criteria:
- case: happy
  given: _brief_ visible
  when: el _visitante_ solicita corregir un dato
  then: vuelve a _captura_ con nueve valores conservados, edición directa y nueva _revisión_ sin repetir confirmaciones de los demás pasos
- case: error
  given: _brief_ visible
  when: no solicita corregir
  then: puede confirmar sin edición
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: mensaje-brief#visitor
refines: REQ-0001
```

## REQ-0141

```yaml requirement
uid: REQ-0141
level: software
kind: functional
criticality: high
statement: La interfaz representa opcionales vacíos como Sin especificar.
acceptance_criteria:
- case: happy
  given: _brief_ listo
  when: renderiza fila opcional vacía
  then: muestra Sin especificar
- case: error
  given: _brief_ listo
  when: opcional sólo tenía espacios antes de normalizar
  then: no muestra espacios como información
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: mensaje-brief#frontend
refines: REQ-0002
```

## REQ-0142

```yaml requirement
uid: REQ-0142
level: software
kind: functional
criticality: high
statement: La _revisión_ termina el canal de voz existente.
acceptance_criteria:
- case: happy
  given: _sesión de voz_ activa
  when: se solicita revisar
  then: se cierra WSS antes de mostrar el _brief_
- case: error
  given: petición de _revisión_ sin _sesión de voz_ activa
  when: no existe conexión
  then: no requiere abrirla para cerrar
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: mensaje-brief#gemini-live
refines: REQ-0004
```

## REQ-0175

```yaml requirement
uid: REQ-0175
level: software
kind: observability
criticality: medium
statement: La instrumentación emite los eventos técnicos esperados del flujo de mensaje y _brief_.
acceptance_criteria:
- case: happy
  given: intentos técnicos del flujo con receptor disponible
  when: se ejecutan todos los casos de aceptación
  then: emite tbo.mensaje_brief.start y tbo.mensaje_brief.end con event, requirement=REQ-0175 y correlation_id del intento
- case: edge
  given: intentos técnicos del flujo con receptor disponible
  when: el caso termina en error
  then: emite tbo.mensaje_brief.error en lugar de tbo.mensaje_brief.end con event, requirement=REQ-0175 y correlation_id del intento
feasibility: Viable con señales técnicas sin contenido; una prueba de integración @sdoc[REQ-0175] comprueba literalmente los eventos y sus tres campos obligatorios.
size: S
environment:
- element: receptores externos de telemetría
  impact: envíos técnicos best-effort sin garantía de persistencia ni contenido personal
derived_from: mensaje-brief#frontend
refines: REQ-0017
metric: eventos esperados emitidos con receptor disponible
threshold: == 100 %
measurement_method:
  instrument: integration
  window: one test run
  sample: every acceptance criterion (happy, edge, error) of REQ-0057, REQ-0058, REQ-0059, REQ-0060, REQ-0061, REQ-0062, REQ-0063, REQ-0064, REQ-0065, REQ-0066, REQ-0140, REQ-0141, REQ-0142, REQ-0207; receiver available
events:
- tbo.mensaje_brief.start
- tbo.mensaje_brief.end
- tbo.mensaje_brief.error
watched_by:
- 'Comprobación de integración: cada evento esperado y sus campos event, requirement y correlation_id; ausencia detectada hace fallar la prueba.'
```

## REQ-0176

```yaml requirement
uid: REQ-0176
level: software
kind: security
criticality: high
statement: Los eventos del flujo de mensaje y _brief_ excluyen datos personales, campos, audio y credenciales.
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
derived_from: mensaje-brief#frontend
refines: REQ-0017
metric: filtraciones de datos protegidos en eventos
threshold: == 0 filtraciones
measurement_method:
  instrument: security
  window: one test run
  sample: every applicable acceptance criterion with canary data
```

## REQ-0177

```yaml requirement
uid: REQ-0177
level: software
kind: reliability
criticality: high
statement: Los fallos de telemetría no alteran ni bloquean el resultado del flujo de mensaje y _brief_.
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
derived_from: mensaje-brief#frontend
refines: REQ-0025
metric: alteraciones o bloqueos funcionales por fallo del sink
threshold: == 0 alteraciones
measurement_method:
  instrument: integration
  window: one test run
  sample: every applicable acceptance criterion with failing and indefinitely pending sinks
```

## REQ-0207

```yaml requirement
uid: REQ-0207
level: software
kind: functional
criticality: high
statement: La entrada en _revisión_ cierra la voz antes de presentar el _brief_.
acceptance_criteria:
- case: happy
  given: _sesión de voz_ activa
  when: se confirma Continuar de mensaje
  then: cierra WSS, micrófono y audio antes de renderizar _revisión_
- case: error
  given: _sesión de voz_ activa
  when: existen recursos parcialmente adquiridos
  then: también los libera
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: mensaje-brief#INV-2
refines: REQ-0021
```

