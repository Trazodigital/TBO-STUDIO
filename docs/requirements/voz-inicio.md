# voz-inicio

Borrador de etapa 2; pendiente de revisión independiente de criterios y Checkpoint 2.

## REQ-0083

```yaml requirement
uid: REQ-0083
level: software
kind: functional
criticality: high
statement: El inicio de voz bloquea activaciones concurrentes.
acceptance_criteria:
- case: happy
  given: _captura_ disponible
  when: se pulsa micrófono
  then: marca inicio pendiente antes de pedir permiso
- case: error
  given: _captura_ disponible
  when: se pulsa otra vez durante inicio
  then: no solicita otra _credencial efímera_
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#INV-1
refines: REQ-0003
```

## REQ-0084

```yaml requirement
uid: REQ-0084
level: software
kind: functional
criticality: high
statement: La denegación de micrófono impide solicitar autorización.
acceptance_criteria:
- case: happy
  given: inicio de voz pendiente
  when: se deniega permiso o falta micrófono
  then: libera bloqueo sin llamar al emisor
- case: error
  given: inicio de voz pendiente
  when: se continúa escribiendo
  then: el formulario manual permanece disponible
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#INV-2
refines: REQ-0003
```

## REQ-0085

```yaml requirement
uid: REQ-0085
level: software
kind: functional
criticality: high
statement: La emisión sólo ocurre después del permiso de micrófono.
acceptance_criteria:
- case: happy
  given: micrófono disponible
  when: se concede permiso
  then: pide autorización de un uso al servidor
- case: error
  given: micrófono disponible
  when: no se concede permiso
  then: no contacta token-issuer
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#INV-3
refines: REQ-0003
```

## REQ-0086

```yaml requirement
uid: REQ-0086
level: software
kind: functional
criticality: high
statement: El producto no presupone cuotas o expiraciones no verificadas.
acceptance_criteria:
- case: happy
  given: configuración de emisión
  when: se define autorización temporal
  then: usa ventana configurada sin imponer un minuto
- case: error
  given: configuración de emisión
  when: el proveedor devuelve 429
  then: no lo atribuye necesariamente a tres sesiones
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#INV-4
refines: REQ-0003
```

## REQ-0087

```yaml requirement
uid: REQ-0087
level: software
kind: reliability
criticality: high
statement: El registro de emisión no bloquea la respuesta de autorización.
acceptance_criteria:
- case: happy
  given: emisión resuelta
  when: Loki falla o no responde
  then: devuelve token o error sin esperar al sink
- case: error
  given: emisión resuelta
  when: la emisión fue exitosa
  then: no transforma éxito en error por logging
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#INV-5
refines: REQ-0003
metric: alteraciones o bloqueos funcionales por fallo del sink
threshold: == 0 alteraciones
measurement_method:
  instrument: integration
  window: one test run
  sample: every applicable acceptance criterion with failing and indefinitely pending sinks
```

## REQ-0088

```yaml requirement
uid: REQ-0088
level: software
kind: functional
criticality: high
statement: Cada activación permite como máximo un intento WSS.
acceptance_criteria:
- case: happy
  given: _credencial efímera_ válida
  when: se conecta voz
  then: abre WSS directo una sola vez
- case: error
  given: _credencial efímera_ válida
  when: falla el handshake
  then: no reintenta automáticamente ni reutiliza token
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#INV-6
refines: REQ-0003
```

## REQ-0089

```yaml requirement
uid: REQ-0089
level: software
kind: functional
criticality: high
statement: La voz sólo se habilita con sesión configurada.
acceptance_criteria:
- case: happy
  given: _sesión de voz_ lista
  when: se entrega contexto previo con herramienta habilitada
  then: muestra listening y habilita hablar
- case: error
  given: conexión de voz en configuración
  when: aún no está lista
  then: no muestra ESCUCHANDO VOZ ACTIVA
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#INV-7
refines: REQ-0003
```

## REQ-0090

```yaml requirement
uid: REQ-0090
level: software
kind: functional
criticality: high
statement: La configuración del canal precede a la conversación habilitada.
acceptance_criteria:
- case: happy
  given: canal de voz disponible
  when: se configura contexto e instrucciones
  then: habilita llenar_campo antes de hablar
- case: error
  given: canal de voz disponible
  when: falla configuración
  then: no habilita conversación sin herramienta
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#INV-8
refines: REQ-0003
```

## REQ-0091

```yaml requirement
uid: REQ-0091
level: software
kind: functional
criticality: high
statement: El inicio fallido libera los recursos adquiridos.
acceptance_criteria:
- case: happy
  given: micrófono obtenido
  when: falla emisión o WSS
  then: detiene pistas, audio y socket parcial y libera el bloqueo de inicio
- case: error
  given: micrófono obtenido
  when: sólo existe recurso parcial
  then: lo libera y mantiene datos manuales
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#INV-9
refines: REQ-0003
```

## REQ-0092

```yaml requirement
uid: REQ-0092
level: software
kind: functional
criticality: high
statement: El fallo de inicio cancela confirmaciones pendientes.
acceptance_criteria:
- case: happy
  given: _conflicto manual_ pendiente
  when: se cierra por fallo
  then: conserva el dato manual y cancela confirmación
- case: error
  given: _conflicto manual_ pendiente
  when: llega aceptación tardía
  then: no la aplica
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#INV-10
refines: REQ-0003
```

## REQ-0093

```yaml requirement
uid: REQ-0093
level: software
kind: reliability
criticality: high
statement: La telemetría de inicio no impide recuperar la _captura_.
acceptance_criteria:
- case: happy
  given: inicio fallido
  when: Faro no responde
  then: limpia recursos y mantiene formulario manual
- case: error
  given: inicio fallido
  when: Faro devuelve error
  then: no inicia reconexión automática
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#INV-11
refines: REQ-0003
metric: alteraciones o bloqueos funcionales por fallo del sink
threshold: == 0 alteraciones
measurement_method:
  instrument: integration
  window: one test run
  sample: every applicable acceptance criterion with failing and indefinitely pending sinks
```

## REQ-0094

```yaml requirement
uid: REQ-0094
level: software
kind: functional
criticality: high
statement: Un error de emisión interrumpe la ruta de conexión.
acceptance_criteria:
- case: happy
  given: permiso concedido
  when: el emisor devuelve error
  then: no abre WSS
- case: error
  given: inicio de voz pendiente
  when: falla por ausencia de micrófono
  then: no llega siquiera a emisión
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#INV-12
refines: REQ-0003
```

## REQ-0148

```yaml requirement
uid: REQ-0148
level: software
kind: functional
criticality: high
statement: El _visitante_ inicia voz mediante una pulsación explícita.
acceptance_criteria:
- case: happy
  given: _captura_ disponible
  when: pulsa micrófono
  then: inicia comprobación de permiso
- case: error
  given: _captura_ disponible
  when: no pulsa micrófono
  then: no solicita autorización
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#visitor
refines: REQ-0001
```

## REQ-0149

```yaml requirement
uid: REQ-0149
level: software
kind: functional
criticality: high
statement: La interfaz muestra voz activa únicamente con sesión lista.
acceptance_criteria:
- case: happy
  given: conexión preparada
  when: se confirma configuración lista
  then: muestra ESCUCHANDO VOZ ACTIVA
- case: error
  given: conexión preparada
  when: falla el inicio
  then: muestra solving
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#frontend
refines: REQ-0002
```

## REQ-0150

```yaml requirement
uid: REQ-0150
level: software
kind: functional
criticality: high
statement: El emisor obtiene una autorización temporal de un uso.
acceptance_criteria:
- case: happy
  given: micrófono autorizado
  when: el proveedor acepta emisión
  then: devuelve _credencial efímera_ con uses:1
- case: error
  given: micrófono autorizado
  when: el proveedor rechaza
  then: devuelve error sin clave
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#token-issuer
refines: REQ-0003
```

## REQ-0151

```yaml requirement
uid: REQ-0151
level: software
kind: functional
criticality: high
statement: La voz se conecta sin atravesar un proxy de audio propio.
acceptance_criteria:
- case: happy
  given: token válido
  when: se abre el canal
  then: conecta navegador y Gemini directamente
- case: error
  given: token válido
  when: el canal falla
  then: conserva ruta manual
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#gemini-live
refines: REQ-0004
```

## REQ-0181

```yaml requirement
uid: REQ-0181
level: software
kind: security
criticality: high
statement: Los eventos de inicio de voz enviados a Loki excluyen contenido personal y secretos.
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
derived_from: voz-inicio#grafana-loki
refines: REQ-0018
metric: filtraciones de datos protegidos en eventos
threshold: == 0 filtraciones
measurement_method:
  instrument: security
  window: one test run
  sample: every applicable acceptance criterion with canary data
```

## REQ-0182

```yaml requirement
uid: REQ-0182
level: software
kind: security
criticality: high
statement: Los eventos de inicio de voz enviados a Faro excluyen contenido personal y secretos.
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
derived_from: voz-inicio#grafana-faro
refines: REQ-0017
metric: filtraciones de datos protegidos en eventos
threshold: == 0 filtraciones
measurement_method:
  instrument: security
  window: one test run
  sample: every applicable acceptance criterion with canary data
```

## REQ-0183

```yaml requirement
uid: REQ-0183
level: software
kind: observability
criticality: medium
statement: La instrumentación emite los eventos técnicos esperados del flujo de inicio de voz.
acceptance_criteria:
- case: happy
  given: intentos técnicos del flujo con receptor disponible
  when: se ejecutan todos los casos de aceptación
  then: emite tbo.voz_inicio.start y tbo.voz_inicio.end con event, requirement=REQ-0183 y correlation_id del intento
- case: edge
  given: intentos técnicos del flujo con receptor disponible
  when: el caso termina en error
  then: emite tbo.voz_inicio.error en lugar de tbo.voz_inicio.end con event, requirement=REQ-0183 y correlation_id del intento
feasibility: Viable con señales técnicas sin contenido; una prueba de integración @sdoc[REQ-0183] comprueba literalmente los eventos y sus tres campos obligatorios.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#frontend
refines: REQ-0017
metric: eventos esperados emitidos con receptor disponible
threshold: == 100 %
measurement_method:
  instrument: integration
  window: one test run
  sample: every acceptance criterion (happy, edge, error) of REQ-0083, REQ-0084, REQ-0085, REQ-0086, REQ-0088, REQ-0089, REQ-0090, REQ-0091, REQ-0092, REQ-0094, REQ-0148, REQ-0149, REQ-0150, REQ-0151, REQ-0192, REQ-0193, REQ-0198, REQ-0199, REQ-0201; receiver available
events:
- tbo.voz_inicio.start
- tbo.voz_inicio.end
- tbo.voz_inicio.error
watched_by:
- 'Comprobación de integración: cada evento esperado y sus campos event, requirement y correlation_id; ausencia detectada hace fallar la prueba.'
```

## REQ-0192

```yaml requirement
uid: REQ-0192
level: software
kind: functional
criticality: high
statement: La interfaz token-issuance-api sólo solicita autorización con permiso de micrófono concedido.
acceptance_criteria:
- case: happy
  given: micrófono disponible
  when: se concede permiso
  then: pide autorización de un uso al servidor
- case: error
  given: micrófono disponible
  when: no se concede permiso
  then: no contacta token-issuer
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#INV-3
refines: REQ-0011
```

## REQ-0193

```yaml requirement
uid: REQ-0193
level: software
kind: functional
criticality: high
statement: La emisión utiliza el proveedor mediante gemini-token-source.
acceptance_criteria:
- case: happy
  given: micrófono autorizado
  when: se solicita autorización temporal
  then: el emisor usa gemini-token-source
- case: error
  given: micrófono autorizado
  when: el proveedor rechaza
  then: devuelve error sin credencial
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#INV-3
refines: REQ-0012
```

## REQ-0198

```yaml requirement
uid: REQ-0198
level: software
kind: functional
criticality: high
statement: El servidor dirige los eventos de autorización al receptor de logs.
acceptance_criteria:
- case: happy
  given: emisión resuelta
  when: se informa resultado
  then: usa structured-log-sink hacia Loki
- case: error
  given: emisión resuelta
  when: Loki falla
  then: no convierte la autorización en error
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#INV-5
refines: REQ-0009
```

## REQ-0199

```yaml requirement
uid: REQ-0199
level: software
kind: functional
criticality: high
statement: La respuesta de autorización excluye la clave permanente.
acceptance_criteria:
- case: happy
  given: emisor configurado
  when: responde al navegador
  then: sólo incluye _credencial efímera_ o error
- case: error
  given: emisor configurado
  when: se inspecciona respuesta fallida
  then: no contiene clave permanente
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#INV-3
refines: REQ-0020
```

## REQ-0201

```yaml requirement
uid: REQ-0201
level: software
kind: functional
criticality: high
statement: La emisión usa dependencias configuradas sin salto comercial adicional.
acceptance_criteria:
- case: happy
  given: emisor y adaptador configurados
  when: se solicita autorización
  then: el puerto se conecta al adaptador configurado
- case: error
  given: emisor y adaptador configurados
  when: se inspecciona la traza de red
  then: composition-root no aparece como servicio intermedio
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-inicio#INV-3
refines: REQ-0024
```

