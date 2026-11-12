# contacto

Borrador de etapa 2; pendiente de revisión independiente de criterios y Checkpoint 2.

## REQ-0030

```yaml requirement
uid: REQ-0030
level: software
kind: functional
criticality: medium
statement: La _captura_ presenta los tres campos de contacto desde el inicio.
acceptance_criteria:
- case: happy
  given: consulta abierta
  when: se muestra _captura_
  then: aparecen name, phone y company
- case: edge
  given: consulta abierta
  when: no se ha pulsado otro botón
  then: los tres campos ya son visibles
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: contacto#INV-1
refines: REQ-0002
```

## REQ-0031

```yaml requirement
uid: REQ-0031
level: software
kind: functional
criticality: high
statement: Continuar rechaza un nombre vacío tras trim().
acceptance_criteria:
- case: happy
  given: contacto visible
  when: se pulsa Continuar con name vacío
  then: muestra Requerido sin avanzar
- case: error
  given: contacto visible
  when: name contiene sólo espacios
  then: mantiene phone y company sin avanzar
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: contacto#INV-2
refines: REQ-0002
```

## REQ-0032

```yaml requirement
uid: REQ-0032
level: software
kind: functional
criticality: high
statement: Continuar persiste los datos de contacto normalizados.
acceptance_criteria:
- case: happy
  given: name con contenido
  when: se pulsa Continuar
  then: guarda name, phone y company con trim()
- case: error
  given: name con contenido
  when: phone y company contienen sólo espacios
  then: se guardan como cadenas vacías
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: contacto#INV-3
refines: REQ-0002
```

## REQ-0033

```yaml requirement
uid: REQ-0033
level: software
kind: functional
criticality: medium
statement: La edición del nombre no ejecuta Continuar.
acceptance_criteria:
- case: happy
  given: error Requerido visible
  when: el _visitante_ escribe un nombre
  then: permanece en contacto hasta Continuar
- case: edge
  given: error Requerido visible
  when: se aplica voz válida
  then: permanece en contacto sin avance automático
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: contacto#INV-4
refines: REQ-0002
```

## REQ-0034

```yaml requirement
uid: REQ-0034
level: software
kind: functional
criticality: high
statement: El contacto admite teléfono y organización vacíos.
acceptance_criteria:
- case: happy
  given: name válido
  when: se continúa sin phone ni company
  then: permite pasar al correo
- case: error
  given: name válido
  when: el servicio de voz está caído
  then: permite continuar manualmente
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: contacto#INV-5
refines: REQ-0002
```

## REQ-0035

```yaml requirement
uid: REQ-0035
level: software
kind: functional
criticality: medium
statement: Enter en contacto ejecuta únicamente Continuar de contacto.
acceptance_criteria:
- case: happy
  given: inputs de contacto activos
  when: se pulsa Enter con name válido
  then: abre correo sin enviar _solicitud_
- case: edge
  given: inputs de contacto activos
  when: se pulsa Enter con name vacío
  then: muestra Requerido sin POST
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: contacto#INV-6
refines: REQ-0002
```

## REQ-0036

```yaml requirement
uid: REQ-0036
level: software
kind: functional
criticality: high
statement: Sólo una actualización de nombre realmente aplicada limpia su error.
acceptance_criteria:
- case: happy
  given: Requerido visible
  when: se aplica voz válida sin _conflicto manual_
  then: desaparece el error
- case: error
  given: Requerido visible
  when: la propuesta no se acepta
  then: no se limpia el error por esa propuesta
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: contacto#INV-7
refines: REQ-0002
```

## REQ-0134

```yaml requirement
uid: REQ-0134
level: software
kind: functional
criticality: high
statement: El _visitante_ puede corregir un nombre rechazado.
acceptance_criteria:
- case: happy
  given: name vacío
  when: edita y ejecuta Continuar con nombre válido
  then: abre correo
- case: error
  given: name vacío
  when: sólo edita sin Continuar
  then: permanece en contacto
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: contacto#visitor
refines: REQ-0001
```

## REQ-0135

```yaml requirement
uid: REQ-0135
level: software
kind: functional
criticality: high
statement: La interfaz sustituye contacto por detalles tras validar.
acceptance_criteria:
- case: happy
  given: name válido
  when: se ejecuta Continuar
  then: presenta Correo Corporativo
- case: error
  given: contacto visible
  when: se ejecuta Continuar con name vacío
  then: mantiene DATOS DE CONTACTO
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: contacto#frontend
refines: REQ-0002
```

## REQ-0166

```yaml requirement
uid: REQ-0166
level: software
kind: observability
criticality: medium
statement: La instrumentación emite los eventos técnicos esperados del flujo de contacto.
acceptance_criteria:
- case: happy
  given: intentos técnicos del flujo con receptor disponible
  when: se ejecutan todos los casos de aceptación
  then: emite tbo.contacto.start y tbo.contacto.end con event, requirement=REQ-0166 y correlation_id del intento
- case: edge
  given: intentos técnicos del flujo con receptor disponible
  when: el caso termina en error
  then: emite tbo.contacto.error en lugar de tbo.contacto.end con event, requirement=REQ-0166 y correlation_id del intento
feasibility: Viable con señales técnicas sin contenido; una prueba de integración @sdoc[REQ-0166] comprueba literalmente los eventos y sus tres campos obligatorios.
size: S
environment:
- element: receptores externos de telemetría
  impact: envíos técnicos best-effort sin garantía de persistencia ni contenido personal
derived_from: contacto#frontend
refines: REQ-0017
metric: eventos esperados emitidos con receptor disponible
threshold: == 100 %
measurement_method:
  instrument: integration
  window: one test run
  sample: every acceptance criterion (happy, edge, error) of REQ-0030, REQ-0031, REQ-0032, REQ-0033, REQ-0034, REQ-0035, REQ-0036, REQ-0134, REQ-0135, REQ-0191, REQ-0206; receiver available
events:
- tbo.contacto.start
- tbo.contacto.end
- tbo.contacto.error
watched_by:
- 'Comprobación de integración: cada evento esperado y sus campos event, requirement y correlation_id; ausencia detectada hace fallar la prueba.'
```

## REQ-0167

```yaml requirement
uid: REQ-0167
level: software
kind: security
criticality: high
statement: Los eventos del flujo de contacto excluyen datos personales, campos, audio y credenciales.
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
derived_from: contacto#frontend
refines: REQ-0017
metric: filtraciones de datos protegidos en eventos
threshold: == 0 filtraciones
measurement_method:
  instrument: security
  window: one test run
  sample: every applicable acceptance criterion with canary data
```

## REQ-0168

```yaml requirement
uid: REQ-0168
level: software
kind: reliability
criticality: high
statement: Los fallos de telemetría no alteran ni bloquean el resultado del flujo de contacto.
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
derived_from: contacto#frontend
refines: REQ-0025
metric: alteraciones o bloqueos funcionales por fallo del sink
threshold: == 0 alteraciones
measurement_method:
  instrument: integration
  window: one test run
  sample: every applicable acceptance criterion with failing and indefinitely pending sinks
```

## REQ-0191

```yaml requirement
uid: REQ-0191
level: software
kind: functional
criticality: high
statement: La interfaz de consulta presenta los campos de contacto al acceder a _captura_.
acceptance_criteria:
- case: happy
  given: consulta abierta
  when: se muestra _captura_
  then: aparecen name, phone y company
- case: error
  given: consulta abierta
  when: no se ha pulsado otro botón
  then: los tres campos ya son visibles
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: contacto#INV-1
refines: REQ-0010
```

## REQ-0206

```yaml requirement
uid: REQ-0206
level: software
kind: functional
criticality: medium
statement: La edición del nombre limpia el error activo.
acceptance_criteria:
- case: happy
  given: Requerido visible
  when: se edita name manualmente
  then: desaparece Requerido sin avanzar
- case: edge
  given: Requerido visible
  when: la voz propone valor sin aplicarlo
  then: no limpia el error por esa propuesta
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: contacto#INV-2
refines: REQ-0002
```

