# voz-campos

Borrador de etapa 2; pendiente de revisión independiente de criterios y Checkpoint 2.

## REQ-0095

```yaml requirement
uid: REQ-0095
level: software
kind: functional
criticality: high
statement: La recepción de llenar_campo no acredita su aplicación.
acceptance_criteria:
- case: happy
  given: _sesión de voz_ activa
  when: Gemini envía id, campo y valor
  then: frontend evalúa la propuesta
- case: error
  given: _sesión de voz_ activa
  when: el valor es inválido
  then: no afirma que fue guardado
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-campos#INV-1
refines: REQ-0013
```

## REQ-0096

```yaml requirement
uid: REQ-0096
level: software
kind: functional
criticality: high
statement: Cada propuesta obtiene una sola resolución vigente.
acceptance_criteria:
- case: happy
  given: propuesta recibida
  when: se acepta
  then: responde ok con su id
- case: error
  given: propuesta recibida
  when: se rechaza por _conflicto manual_
  then: responde rejected, no ok y error a la vez
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-campos#INV-2
refines: REQ-0013
```

## REQ-0097

```yaml requirement
uid: REQ-0097
level: software
kind: functional
criticality: high
statement: Una propuesta válida sin _conflicto manual_ actualiza el campo.
acceptance_criteria:
- case: happy
  given: _captura_ y sesión vigentes
  when: llega campo válido sin edición previa
  then: normaliza, guarda y refleja antes de ok
- case: error
  given: _captura_ y sesión vigentes
  when: el valor textual contiene espacios externos
  then: aplica trim() antes de responder
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-campos#INV-3
refines: REQ-0013
```

## REQ-0098

```yaml requirement
uid: REQ-0098
level: software
kind: functional
criticality: high
statement: La sustitución de una edición manual requiere confirmación.
acceptance_criteria:
- case: happy
  given: _conflicto manual_ presente
  when: el _visitante_ acepta
  then: aplica propuesta normalizada y responde ok
- case: error
  given: _conflicto manual_ presente
  when: el _visitante_ rechaza
  then: conserva edición y responde rejected
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-campos#INV-4
refines: REQ-0013
```

## REQ-0099

```yaml requirement
uid: REQ-0099
level: software
kind: functional
criticality: high
statement: Una propuesta inválida no modifica datos.
acceptance_criteria:
- case: happy
  given: canal vigente abierto
  when: llega campo desconocido o valor inválido
  then: responde error con mismo id sin mutar
- case: error
  given: canal vigente abierto
  when: name es vacío, email inválido o código ajeno al catálogo
  then: conserva formulario y _brief_
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-campos#INV-5
refines: REQ-0013
```

## REQ-0100

```yaml requirement
uid: REQ-0100
level: software
kind: functional
criticality: high
statement: Las propuestas de una sesión cerrada se descartan.
acceptance_criteria:
- case: happy
  given: _sesión de voz_ cerrada
  when: llega llenar_campo antiguo
  then: no modifica ni encola
- case: error
  given: _sesión de voz_ cerrada
  when: ya existe otra _sesión de voz_
  then: no responde a la llamada antigua por la nueva
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-campos#INV-6
refines: REQ-0013
```

## REQ-0101

```yaml requirement
uid: REQ-0101
level: software
kind: functional
criticality: high
statement: La confirmación revalida la vigencia antes de aplicar.
acceptance_criteria:
- case: happy
  given: _conflicto manual_ pendiente
  when: el _visitante_ acepta con _captura_ y sesión vigentes
  then: permite aplicar propuesta
- case: error
  given: _conflicto manual_ pendiente
  when: la _revisión_ comenzó antes de aceptar
  then: no modifica el _brief_
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-campos#INV-7
refines: REQ-0013
```

## REQ-0102

```yaml requirement
uid: REQ-0102
level: software
kind: functional
criticality: high
statement: El fallo de voz conserva los datos ya aplicados.
acceptance_criteria:
- case: happy
  given: _sesión de voz_ activa
  when: se corta WSS o se apaga voz
  then: cierra recursos con datos intactos
- case: error
  given: _sesión de voz_ activa
  when: sólo se guardó parte de la conversación
  then: permite terminar manualmente
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-campos#INV-8
refines: REQ-0013
```

## REQ-0103

```yaml requirement
uid: REQ-0103
level: software
kind: functional
criticality: high
statement: La voz no reconecta sin una nueva pulsación.
acceptance_criteria:
- case: happy
  given: _sesión de voz_ interrumpida
  when: el _visitante_ sigue en _captura_
  then: mantiene voz cerrada
- case: error
  given: _sesión de voz_ interrumpida
  when: el proveedor vuelve a estar disponible
  then: no reconecta automáticamente
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-campos#INV-9
refines: REQ-0013
```

## REQ-0104

```yaml requirement
uid: REQ-0104
level: software
kind: reliability
criticality: high
statement: La telemetría de actualización no bloquea la recuperación.
acceptance_criteria:
- case: happy
  given: fallo de voz
  when: el receptor de eventos falla
  then: conserva cierre y continuación manual
- case: error
  given: fallo de voz
  when: el receptor permanece sin respuesta
  then: no espera para liberar recursos
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-campos#INV-10
refines: REQ-0013
metric: alteraciones o bloqueos funcionales por fallo del sink
threshold: == 0 alteraciones
measurement_method:
  instrument: integration
  window: one test run
  sample: every applicable acceptance criterion with failing and indefinitely pending sinks
```

## REQ-0105

```yaml requirement
uid: REQ-0105
level: software
kind: functional
criticality: high
statement: Aplicar voz válida no confirma contacto o correo.
acceptance_criteria:
- case: happy
  given: nombre o correo con error
  when: se aplica valor válido
  then: limpia error y permanece en la pregunta
- case: error
  given: nombre o correo con error
  when: el _visitante_ no ejecuta Continuar
  then: no avanza por voz solamente
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-campos#INV-11
refines: REQ-0013
```

## REQ-0106

```yaml requirement
uid: REQ-0106
level: software
kind: functional
criticality: high
statement: Las propuestas de catálogo usan los códigos aprobados.
acceptance_criteria:
- case: happy
  given: llenar_campo para opción de proyecto
  when: llega código exacto aprobado
  then: lo reconoce sin inferir otros catálogos
- case: error
  given: llenar_campo para opción de proyecto
  when: llega variante no aprobada
  then: la rechaza sin normalizarla a otra opción
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-campos#INV-12
refines: REQ-0013
```

## REQ-0107

```yaml requirement
uid: REQ-0107
level: software
kind: functional
criticality: high
statement: El cierre cancela la confirmación de _conflicto manual_.
acceptance_criteria:
- case: happy
  given: propuesta esperando decisión
  when: se apaga voz o entra en _revisión_
  then: mantiene dato manual y cancela propuesta
- case: error
  given: propuesta esperando decisión
  when: se acepta después del cierre
  then: no revive la propuesta
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-campos#INV-13
refines: REQ-0013
```

## REQ-0108

```yaml requirement
uid: REQ-0108
level: software
kind: functional
criticality: high
statement: Una opción aplicada por voz muestra su etiqueta humana.
acceptance_criteria:
- case: happy
  given: pregunta de proyecto activa en _captura_ con catálogo válido aceptado por voz
  when: se aplica la opción sin _conflicto manual_ o tras confirmarlo
  then: guarda código, apila etiqueta humana, cierra lista abierta y activa inmediatamente la siguiente pregunta
- case: error
  given: propuesta de catálogo válido recibida
  when: había _conflicto manual_ sin aceptar
  then: no aplica esa presentación como confirmada
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-campos#INV-14
refines: REQ-0013
```

## REQ-0152

```yaml requirement
uid: REQ-0152
level: software
kind: functional
criticality: high
statement: El _visitante_ puede rechazar una sustitución por voz.
acceptance_criteria:
- case: happy
  given: _conflicto manual_
  when: rechaza propuesta
  then: mantiene su dato anterior
- case: error
  given: _conflicto manual_
  when: ya se cerró voz
  then: la decisión tardía no modifica nada
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-campos#visitor
refines: REQ-0001
```

## REQ-0153

```yaml requirement
uid: REQ-0153
level: software
kind: functional
criticality: high
statement: La interfaz normaliza texto aceptado por voz.
acceptance_criteria:
- case: happy
  given: texto válido sin _conflicto manual_
  when: se acepta llenar_campo
  then: guarda trim() antes de reflejarlo
- case: error
  given: propuesta textual sin _conflicto manual_
  when: el texto name sólo tiene espacios
  then: lo rechaza
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-campos#frontend
refines: REQ-0002
```

## REQ-0154

```yaml requirement
uid: REQ-0154
level: software
kind: functional
criticality: high
statement: El canal devuelve el identificador de resolución de la herramienta.
acceptance_criteria:
- case: happy
  given: toolCall vigente con id
  when: se aplica o rechaza propuesta
  then: responde toolResponse con ese mismo id
- case: error
  given: toolCall vigente con id
  when: el canal está cerrado
  then: no envía respuesta por otro canal
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-campos#gemini-live
refines: REQ-0004
```

## REQ-0184

```yaml requirement
uid: REQ-0184
level: software
kind: security
criticality: high
statement: Los eventos del flujo de actualización por voz excluyen datos personales, campos, audio y credenciales.
acceptance_criteria:
- case: happy
  given: datos señuelo en campos y credenciales
  when: se registran todos los casos pertinentes
  then: ningún evento contiene esos datos
- case: error
  given: datos señuelo en campos y credenciales
  when: ocurre un fallo del proveedor o de validación
  then: el evento de error tampoco los contiene
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-campos#grafana-faro
refines: REQ-0017
metric: filtraciones de datos protegidos en eventos
threshold: == 0 filtraciones
measurement_method:
  instrument: security
  window: one test run
  sample: every applicable acceptance criterion with canary data
```

## REQ-0185

```yaml requirement
uid: REQ-0185
level: software
kind: observability
criticality: medium
statement: La instrumentación emite los eventos técnicos esperados del flujo de actualización por voz.
acceptance_criteria:
- case: happy
  given: intentos técnicos del flujo con receptor disponible
  when: se ejecutan todos los casos de aceptación
  then: emite tbo.voz_campos.start y tbo.voz_campos.end con event, requirement=REQ-0185 y correlation_id del intento
- case: edge
  given: intentos técnicos del flujo con receptor disponible
  when: el caso termina en error
  then: emite tbo.voz_campos.error en lugar de tbo.voz_campos.end con event, requirement=REQ-0185 y correlation_id del intento
feasibility: Viable con señales técnicas sin contenido; una prueba de integración @sdoc[REQ-0185] comprueba literalmente los eventos y sus tres campos obligatorios.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-campos#frontend
refines: REQ-0017
metric: eventos esperados emitidos con receptor disponible
threshold: == 100 %
measurement_method:
  instrument: integration
  window: one test run
  sample: every acceptance criterion (happy, edge, error) of REQ-0095, REQ-0096, REQ-0097, REQ-0098, REQ-0099, REQ-0100, REQ-0101, REQ-0102, REQ-0103, REQ-0105, REQ-0106, REQ-0107, REQ-0108, REQ-0152, REQ-0153, REQ-0154, REQ-0202; receiver available
events:
- tbo.voz_campos.start
- tbo.voz_campos.end
- tbo.voz_campos.error
watched_by:
- 'Comprobación de integración: cada evento esperado y sus campos event, requirement y correlation_id; ausencia detectada hace fallar la prueba.'
```

## REQ-0202

```yaml requirement
uid: REQ-0202
level: software
kind: functional
criticality: high
statement: El canal voice-session-channel devuelve una sola resolución por propuesta vigente.
acceptance_criteria:
- case: happy
  given: propuesta recibida
  when: se acepta
  then: responde ok con su id
- case: error
  given: propuesta recibida
  when: se rechaza por _conflicto manual_
  then: responde rejected, no ok y error a la vez
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-campos#INV-2
refines: REQ-0026
```

