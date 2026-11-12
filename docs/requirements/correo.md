# correo

Borrador de etapa 2; pendiente de revisión independiente de criterios y Checkpoint 2.

## REQ-0037

```yaml requirement
uid: REQ-0037
level: software
kind: functional
criticality: medium
statement: Correo Corporativo admite dominios personales y corporativos.
acceptance_criteria:
- case: happy
  given: contacto confirmado
  when: se presenta correo
  then: conserva name, phone y company
- case: edge
  given: contacto confirmado
  when: se introduce persona@gmail.com
  then: no se rechaza por ser dominio personal
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: correo#INV-1
refines: REQ-0002
```

## REQ-0038

```yaml requirement
uid: REQ-0038
level: software
kind: functional
criticality: high
statement: Continuar exige correo no vacío tras trim().
acceptance_criteria:
- case: happy
  given: correo activo
  when: se continúa con cadena vacía
  then: muestra Requerido sin avanzar
- case: error
  given: correo activo
  when: se continúa con espacios
  then: muestra Requerido antes de comprobar formato
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: correo#INV-2
refines: REQ-0002
```

## REQ-0039

```yaml requirement
uid: REQ-0039
level: software
kind: functional
criticality: high
statement: Continuar rechaza correo que no cumple la expresión acordada.
acceptance_criteria:
- case: happy
  given: correo no vacío
  when: no cumple /^[^\s@]+@[^\s@]+\.[^\s@]+$/ tras trim()
  then: muestra Email inválido sin avanzar
- case: error
  given: correo no vacío
  when: se escribe usuario@localhost
  then: se rechaza sin depender de HTML5
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: correo#INV-3
refines: REQ-0002
```

## REQ-0040

```yaml requirement
uid: REQ-0040
level: software
kind: functional
criticality: medium
statement: Actualizar correo limpia su error sin avanzar.
acceptance_criteria:
- case: happy
  given: error de correo activo
  when: se edita manualmente
  then: limpia error y mantiene correo activo
- case: edge
  given: error de correo activo
  when: se aplica voz válida
  then: no confirma la pregunta automáticamente
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: correo#INV-4
refines: REQ-0002
```

## REQ-0041

```yaml requirement
uid: REQ-0041
level: software
kind: functional
criticality: high
statement: Continuar persiste el correo completo normalizado.
acceptance_criteria:
- case: happy
  given: correo válido con espacios externos
  when: se pulsa Continuar
  then: guarda email.trim() sin cambiar mayúsculas
- case: error
  given: correo válido con espacios externos
  when: el contacto ya estaba guardado
  then: conserva name, phone y company
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: correo#INV-5
refines: REQ-0002
```

## REQ-0042

```yaml requirement
uid: REQ-0042
level: software
kind: functional
criticality: medium
statement: Cada pulsación de Continuar resuelve una sola rama de correo.
acceptance_criteria:
- case: happy
  given: correo activo
  when: se continúa con correo válido
  then: abre projectType sin recorrer errores
- case: edge
  given: correo activo
  when: el correo no vacío es inválido
  then: no ejecuta la rama válida
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: correo#INV-6
refines: REQ-0002
```

## REQ-0043

```yaml requirement
uid: REQ-0043
level: software
kind: functional
criticality: high
statement: La validación de correo conserva el contacto previo.
acceptance_criteria:
- case: happy
  given: contacto guardado
  when: el correo falla validación
  then: conserva name, phone y company
- case: error
  given: contacto guardado
  when: Gemini está indisponible
  then: la corrección manual sigue disponible
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: correo#INV-7
refines: REQ-0002
```

## REQ-0044

```yaml requirement
uid: REQ-0044
level: software
kind: functional
criticality: medium
statement: La fila de correo trunca sólo su representación visual.
acceptance_criteria:
- case: happy
  given: correo largo confirmado
  when: se dibuja la fila compacta
  then: usa ellipsis con ancho del valor limitado al 55 %
- case: edge
  given: correo largo confirmado
  when: se construye el _brief_
  then: incluye el correo completo
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: correo#INV-8
refines: REQ-0002
```

## REQ-0045

```yaml requirement
uid: REQ-0045
level: software
kind: functional
criticality: medium
statement: Una propuesta de voz no aceptada no cambia el correo.
acceptance_criteria:
- case: happy
  given: correo editado manualmente
  when: el _visitante_ rechaza la sustitución
  then: mantiene el correo y su estado de error
- case: edge
  given: correo editado manualmente
  when: la _sesión de voz_ está cerrada
  then: descarta la propuesta
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: correo#INV-9
refines: REQ-0002
```

## REQ-0136

```yaml requirement
uid: REQ-0136
level: software
kind: functional
criticality: high
statement: El _visitante_ confirma expresamente su correo.
acceptance_criteria:
- case: happy
  given: correo escrito
  when: pulsa Continuar con formato válido
  then: se activa projectType
- case: error
  given: correo escrito
  when: sólo escribe
  then: no avanza
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: correo#visitor
refines: REQ-0001
```

## REQ-0137

```yaml requirement
uid: REQ-0137
level: software
kind: functional
criticality: high
statement: La interfaz apila el correo confirmado.
acceptance_criteria:
- case: happy
  given: email válido
  when: se confirma con Continuar
  then: lo muestra como fila compacta sobre projectType
- case: error
  given: correo activo
  when: se pulsa Continuar con email inválido
  then: no lo apila como completado
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: correo#frontend
refines: REQ-0002
```

## REQ-0169

```yaml requirement
uid: REQ-0169
level: software
kind: observability
criticality: medium
statement: La instrumentación emite los eventos técnicos esperados del flujo de correo.
acceptance_criteria:
- case: happy
  given: intentos técnicos del flujo con receptor disponible
  when: se ejecutan todos los casos de aceptación
  then: emite tbo.correo.start y tbo.correo.end con event, requirement=REQ-0169 y correlation_id del intento
- case: edge
  given: intentos técnicos del flujo con receptor disponible
  when: el caso termina en error
  then: emite tbo.correo.error en lugar de tbo.correo.end con event, requirement=REQ-0169 y correlation_id del intento
feasibility: Viable con señales técnicas sin contenido; una prueba de integración @sdoc[REQ-0169] comprueba literalmente los eventos y sus tres campos obligatorios.
size: S
environment:
- element: receptores externos de telemetría
  impact: envíos técnicos best-effort sin garantía de persistencia ni contenido personal
derived_from: correo#frontend
refines: REQ-0017
metric: eventos esperados emitidos con receptor disponible
threshold: == 100 %
measurement_method:
  instrument: integration
  window: one test run
  sample: every acceptance criterion (happy, edge, error) of REQ-0037, REQ-0038, REQ-0039, REQ-0040, REQ-0041, REQ-0042, REQ-0043, REQ-0044, REQ-0045, REQ-0136, REQ-0137; receiver available
events:
- tbo.correo.start
- tbo.correo.end
- tbo.correo.error
watched_by:
- 'Comprobación de integración: cada evento esperado y sus campos event, requirement y correlation_id; ausencia detectada hace fallar la prueba.'
```

## REQ-0170

```yaml requirement
uid: REQ-0170
level: software
kind: security
criticality: high
statement: Los eventos del flujo de correo excluyen datos personales, campos, audio y credenciales.
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
derived_from: correo#frontend
refines: REQ-0017
metric: filtraciones de datos protegidos en eventos
threshold: == 0 filtraciones
measurement_method:
  instrument: security
  window: one test run
  sample: every applicable acceptance criterion with canary data
```

## REQ-0171

```yaml requirement
uid: REQ-0171
level: software
kind: reliability
criticality: high
statement: Los fallos de telemetría no alteran ni bloquean el resultado del flujo de correo.
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
derived_from: correo#frontend
refines: REQ-0025
metric: alteraciones o bloqueos funcionales por fallo del sink
threshold: == 0 alteraciones
measurement_method:
  instrument: integration
  window: one test run
  sample: every applicable acceptance criterion with failing and indefinitely pending sinks
```

