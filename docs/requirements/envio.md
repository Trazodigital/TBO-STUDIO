# envio

Borrador de etapa 2; pendiente de revisión independiente de criterios y Checkpoint 2.

## REQ-0067

```yaml requirement
uid: REQ-0067
level: software
kind: functional
criticality: high
statement: El _envío pendiente_ bloquea nuevas confirmaciones.
acceptance_criteria:
- case: happy
  given: _brief_ revisado y voz cerrada
  when: se confirma envío
  then: activa pending antes del POST
- case: error
  given: _brief_ revisado y voz cerrada
  when: se pulsa otra vez mientras pending
  then: no genera otro POST
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#INV-1
refines: REQ-0005
```

## REQ-0068

```yaml requirement
uid: REQ-0068
level: software
kind: functional
criticality: high
statement: Cada intento resuelve una única alternativa de entrega.
acceptance_criteria:
- case: happy
  given: intento iniciado
  when: recibe 202
  then: muestra sólo aceptación
- case: error
  given: intento iniciado
  when: recibe 4xx
  then: no muestra aceptación para ese intento
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#INV-2
refines: REQ-0005
```

## REQ-0069

```yaml requirement
uid: REQ-0069
level: software
kind: functional
criticality: high
statement: El servidor rechaza payload inválido sin invocar webhook.
acceptance_criteria:
- case: happy
  given: _solicitud_ recibida
  when: la validación falla
  then: devuelve 4xx sin llamada externa
- case: error
  given: _solicitud_ recibida
  when: el payload contiene correo inválido
  then: rechaza antes de entrega
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#INV-3
refines: REQ-0005
```

## REQ-0070

```yaml requirement
uid: REQ-0070
level: software
kind: functional
criticality: high
statement: Corregir datos tras rechazo exige nueva _revisión_.
acceptance_criteria:
- case: happy
  given: _brief_ rechazado por 4xx
  when: el _visitante_ corrige en _captura_
  then: debe revisar antes de confirmar
- case: error
  given: _brief_ conservado tras fallo técnico
  when: reintenta sin cambiar datos tras fallo técnico
  then: puede reusar el _brief_ revisado
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#INV-4
refines: REQ-0005
```

## REQ-0071

```yaml requirement
uid: REQ-0071
level: software
kind: functional
criticality: high
statement: El servidor registra únicamente fallos que pudo observar.
acceptance_criteria:
- case: happy
  given: intento de entrega
  when: el backend recibe y detecta un fallo
  then: puede registrar fallo técnico
- case: error
  given: intento de entrega
  when: la red falla antes de recibir POST
  then: no inventa recepción backend
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#INV-5
refines: REQ-0005
```

## REQ-0072

```yaml requirement
uid: REQ-0072
level: software
kind: functional
criticality: high
statement: Un fallo de entrega conserva el _brief_ para reintento.
acceptance_criteria:
- case: happy
  given: _brief_ confirmado
  when: ocurre red, 5xx o timeout
  then: conserva _brief_ y libera pending
- case: error
  given: _brief_ confirmado
  when: el _visitante_ reintenta
  then: no necesita reconstruir campos
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#INV-6
refines: REQ-0005
```

## REQ-0073

```yaml requirement
uid: REQ-0073
level: software
kind: functional
criticality: high
statement: El timeout local no acredita ausencia de entrega remota.
acceptance_criteria:
- case: happy
  given: intento que agota 10 s
  when: la espera local termina
  then: no declara cancelado el procesamiento remoto
- case: error
  given: intento que agota 10 s
  when: se reintenta
  then: no garantiza deduplicación extremo a extremo
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#INV-7
refines: REQ-0005
```

## REQ-0074

```yaml requirement
uid: REQ-0074
level: software
kind: functional
criticality: high
statement: La aceptación requiere confirmación de recepción por la integración.
acceptance_criteria:
- case: happy
  given: _solicitud_ válida enviada al webhook
  when: el webhook responde HTTP 2xx, incluso sin cuerpo
  then: lead-submitter devuelve 202 Accepted sin exigir comprobante adicional
- case: error
  given: _solicitud_ válida
  when: el webhook falla
  then: no devuelve aceptación comercial por ese intento
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#INV-8
refines: REQ-0005
```

## REQ-0075

```yaml requirement
uid: REQ-0075
level: software
kind: functional
criticality: high
statement: La confirmación de aceptación permanece estable.
acceptance_criteria:
- case: happy
  given: respuesta 202 vigente
  when: frontend la recibe
  then: cierra el envío y cancela el temporizador
- case: error
  given: respuesta 202 vigente
  when: transcurren 3500 ms
  then: no reinicia automáticamente la _captura_
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#INV-9
refines: REQ-0005
```

## REQ-0076

```yaml requirement
uid: REQ-0076
level: software
kind: security
criticality: high
statement: Los eventos de entrega excluyen datos comerciales.
acceptance_criteria:
- case: happy
  given: _solicitud_ con datos señuelo
  when: se registra éxito, rechazo o fallo
  then: no incluye campos, payload ni datos personales
- case: error
  given: _solicitud_ con datos señuelo
  when: se inspecciona el evento de rechazo
  then: no contiene correo ni mensaje
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#INV-10
refines: REQ-0005
metric: filtraciones de datos protegidos en eventos
threshold: == 0 filtraciones
measurement_method:
  instrument: security
  window: one test run
  sample: every applicable acceptance criterion with canary data in one test run
```

## REQ-0077

```yaml requirement
uid: REQ-0077
level: software
kind: functional
criticality: high
statement: Una respuesta tardía no sustituye el resultado de un nuevo intento.
acceptance_criteria:
- case: happy
  given: intento anterior resuelto
  when: llega su respuesta después de iniciar otro
  then: se ignora para el nuevo intento
- case: error
  given: intento anterior resuelto
  when: el intento actual sigue pendiente
  then: conserva su estado y temporizador
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#INV-11
refines: REQ-0005
```

## REQ-0078

```yaml requirement
uid: REQ-0078
level: software
kind: reliability
criticality: high
statement: El fallo del receptor de logs no cambia la respuesta comercial.
acceptance_criteria:
- case: happy
  given: webhook confirma recepción
  when: Loki falla o permanece sin resolver
  then: se devuelve 202 sin esperarlo
- case: error
  given: webhook confirma recepción
  when: Loki devuelve error
  then: no convierte aceptación en 5xx
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#INV-12
refines: REQ-0005
metric: alteraciones o bloqueos funcionales por fallo del sink
threshold: == 0 alteraciones
measurement_method:
  instrument: integration
  window: one test run
  sample: every applicable acceptance criterion with failing and indefinitely pending sinks
```

## REQ-0079

```yaml requirement
uid: REQ-0079
level: software
kind: performance
criticality: high
statement: La espera upstream al webhook no supera diez segundos.
acceptance_criteria:
- case: happy
  given: _solicitud_ válida
  when: el webhook no responde
  then: termina su espera a más tardar a los 10 s
- case: error
  given: _solicitud_ válida
  when: el webhook sigue procesando
  then: no afirma cancelación remota
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#INV-13
refines: REQ-0005
metric: duración máxima de espera upstream
threshold: <= 10 s
measurement_method:
  instrument: integration
  window: one test run
  sample: every applicable acceptance criterion of REQ-0079
```

## REQ-0080

```yaml requirement
uid: REQ-0080
level: software
kind: functional
criticality: high
statement: La respuesta del webhook se interpreta como resultado de la llamada.
acceptance_criteria:
- case: happy
  given: llamada upstream en curso
  when: se recibe 5xx
  then: se procesa como retorno HTTP
- case: error
  given: llamada upstream en curso
  when: vence la espera upstream
  then: se procesa timeout local, no callback HTTP
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#INV-14
refines: REQ-0005
```

## REQ-0081

```yaml requirement
uid: REQ-0081
level: software
kind: functional
criticality: high
statement: El navegador informa fallos locales sin depender del backend.
acceptance_criteria:
- case: happy
  given: intento iniciado
  when: falla red o vence el plazo local
  then: emite fallo técnico por browser-telemetry-sink
- case: error
  given: intento iniciado
  when: el POST nunca llega al servidor
  then: el evento cliente sigue siendo verificable
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#INV-15
refines: REQ-0005
```

## REQ-0082

```yaml requirement
uid: REQ-0082
level: software
kind: functional
criticality: high
statement: El reintento confirmado inicia un ciclo independiente.
acceptance_criteria:
- case: happy
  given: _brief_ conservado tras fallo
  when: se confirma reintento
  then: activa nuevo pending, POST y temporizador de 10 s
- case: error
  given: _brief_ conservado tras fallo
  when: el temporizador anterior expiró
  then: no se reutiliza para el intento nuevo
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#INV-16
refines: REQ-0005
```

## REQ-0143

```yaml requirement
uid: REQ-0143
level: software
kind: functional
criticality: high
statement: El _visitante_ puede reintentar el _brief_ tras fallo técnico.
acceptance_criteria:
- case: happy
  given: _brief_ conservado
  when: confirma reintento
  then: inicia un nuevo intento
- case: error
  given: _brief_ conservado
  when: no pulsa enviar otra vez
  then: no reintenta automáticamente
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#visitor
refines: REQ-0001
```

## REQ-0144

```yaml requirement
uid: REQ-0144
level: software
kind: performance
criticality: high
statement: El cliente termina la espera de envío en diez segundos como máximo.
acceptance_criteria:
- case: happy
  given: POST iniciado
  when: no llega respuesta en el plazo
  then: termina espera y libera pending a más tardar a los 10 s
- case: error
  given: POST iniciado
  when: llega respuesta del intento ya vencido
  then: no altera un intento posterior
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#frontend
refines: REQ-0002
metric: duración máxima de espera de envío en cliente
threshold: <= 10 s
measurement_method:
  instrument: integration
  window: one test run
  sample: every applicable acceptance criterion of REQ-0144
```

## REQ-0145

```yaml requirement
uid: REQ-0145
level: software
kind: functional
criticality: high
statement: El servidor valida el correo antes de entrega.
acceptance_criteria:
- case: happy
  given: payload recibido
  when: email.trim() incumple la regex acordada
  then: rechaza con 4xx sin webhook
- case: error
  given: payload recibido
  when: correo con formato válido
  then: no lo rechaza por dominio personal
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#lead-submitter
refines: REQ-0005
```

## REQ-0146

```yaml requirement
uid: REQ-0146
level: software
kind: functional
criticality: high
statement: El resultado de recepción externo condiciona la respuesta del servidor.
acceptance_criteria:
- case: happy
  given: _solicitud_ válida enviada al webhook
  when: el webhook responde HTTP 2xx, incluso sin cuerpo
  then: la recepción queda confirmada y permite devolver 202 Accepted
- case: error
  given: _solicitud_ válida enviada
  when: webhook devuelve 5xx
  then: se trata como fallo de entrega
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#lead-webhook
refines: REQ-0006
```

## REQ-0147

```yaml requirement
uid: REQ-0147
level: software
kind: functional
criticality: high
statement: La _solicitud_ aceptada se encamina al receptor comercial configurado.
acceptance_criteria:
- case: happy
  given: _solicitud_ válida
  when: la integración confirma recepción
  then: utiliza el _destino comercial_ configurado
- case: error
  given: _solicitud_ válida
  when: sólo hay un log técnico
  then: no lo considera registro comercial
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#commercial-destination
refines: REQ-0007
```

## REQ-0178

```yaml requirement
uid: REQ-0178
level: software
kind: security
criticality: high
statement: Los eventos de entrega enviados a Loki excluyen contenido personal y secretos.
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
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#grafana-loki
refines: REQ-0019
metric: filtraciones de datos protegidos en eventos
threshold: == 0 filtraciones
measurement_method:
  instrument: security
  window: one test run
  sample: every applicable acceptance criterion with canary data
```

## REQ-0179

```yaml requirement
uid: REQ-0179
level: software
kind: security
criticality: high
statement: Los eventos de entrega enviados a Faro excluyen contenido personal y secretos.
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
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#grafana-faro
refines: REQ-0017
metric: filtraciones de datos protegidos en eventos
threshold: == 0 filtraciones
measurement_method:
  instrument: security
  window: one test run
  sample: every applicable acceptance criterion with canary data
```

## REQ-0180

```yaml requirement
uid: REQ-0180
level: software
kind: observability
criticality: medium
statement: La instrumentación emite los eventos técnicos esperados del flujo de envío.
acceptance_criteria:
- case: happy
  given: intentos técnicos del flujo con receptor disponible
  when: se ejecutan todos los casos de aceptación
  then: emite tbo.envio.start y tbo.envio.end con event, requirement=REQ-0180 y correlation_id del intento
- case: edge
  given: intentos técnicos del flujo con receptor disponible
  when: el caso termina en error
  then: emite tbo.envio.error en lugar de tbo.envio.end con event, requirement=REQ-0180 y correlation_id del intento
feasibility: Viable con señales técnicas sin contenido; una prueba de integración @sdoc[REQ-0180] comprueba literalmente los eventos y sus tres campos obligatorios.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#frontend
refines: REQ-0017
metric: eventos esperados emitidos con receptor disponible
threshold: == 100 %
measurement_method:
  instrument: integration
  window: one test run
  sample: every acceptance criterion (happy, edge, error) of REQ-0067, REQ-0068, REQ-0069, REQ-0070, REQ-0071, REQ-0072, REQ-0073, REQ-0074, REQ-0075, REQ-0077, REQ-0080, REQ-0081, REQ-0082, REQ-0143, REQ-0145, REQ-0146, REQ-0147, REQ-0194, REQ-0195, REQ-0196, REQ-0200; receiver available
events:
- tbo.envio.start
- tbo.envio.end
- tbo.envio.error
watched_by:
- 'Comprobación de integración: cada evento esperado y sus campos event, requirement y correlation_id; ausencia detectada hace fallar la prueba.'
```

## REQ-0194

```yaml requirement
uid: REQ-0194
level: software
kind: functional
criticality: high
statement: El cliente entrega el _brief_ al servidor propio.
acceptance_criteria:
- case: happy
  given: _brief_ confirmado
  when: se inicia intento
  then: POST usa lead-submission-api
- case: error
  given: _brief_ confirmado
  when: el servidor devuelve 4xx
  then: conserva _brief_ para corregir
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#INV-1
refines: REQ-0014
```

## REQ-0195

```yaml requirement
uid: REQ-0195
level: software
kind: functional
criticality: high
statement: La interfaz lead-destination no recibe payloads rechazados por la validación del servidor.
acceptance_criteria:
- case: happy
  given: _solicitud_ recibida
  when: la validación falla
  then: devuelve 4xx sin llamada externa
- case: error
  given: _solicitud_ recibida
  when: el payload contiene correo inválido
  then: rechaza antes de entrega
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#INV-3
refines: REQ-0015
```

## REQ-0196

```yaml requirement
uid: REQ-0196
level: software
kind: functional
criticality: high
statement: La entrega usa el destino externo configurado.
acceptance_criteria:
- case: happy
  given: _solicitud_ validada
  when: el webhook la acepta
  then: encamina al _destino comercial_
- case: error
  given: _solicitud_ validada
  when: no confirma persistencia final
  then: no la afirma
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#INV-8
refines: REQ-0016
```

## REQ-0200

```yaml requirement
uid: REQ-0200
level: software
kind: functional
criticality: high
statement: Los datos inválidos no cruzan la frontera externa.
acceptance_criteria:
- case: happy
  given: _solicitud_ inválida
  when: el servidor valida
  then: no llama al webhook
- case: error
  given: _solicitud_ inválida
  when: el navegador intenta envío
  then: sólo contacta a lead-submitter
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#INV-3
refines: REQ-0022
```

## REQ-0204

```yaml requirement
uid: REQ-0204
level: software
kind: constraint
criticality: high
statement: La recepción comercial se delega al destino externo.
acceptance_criteria:
- case: happy
  given: _solicitud_ válida
  when: se confirma integración
  then: no exige base de prospectos propia
- case: error
  given: _solicitud_ válida
  when: existen logs técnicos
  then: no sustituyen almacenamiento comercial
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: backend propio y webhook externo
  impact: validación antes de entrega y resultado remoto potencialmente incierto tras timeout
derived_from: envio#INV-8
refines: REQ-0028
```

