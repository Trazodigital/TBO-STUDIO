# voz-cierre

Borrador de etapa 2; pendiente de revisión independiente de criterios y Checkpoint 2.

## REQ-0109

```yaml requirement
uid: REQ-0109
level: software
kind: functional
criticality: high
statement: El cierre de voz libera los recursos locales.
acceptance_criteria:
- case: happy
  given: _sesión de voz_ o recursos parciales
  when: se apaga micrófono o se entra a _revisión_
  then: cierra WSS, detiene pistas y audio y muestra solving
- case: error
  given: _sesión de voz_ o recursos parciales
  when: no existe WSS
  then: libera igualmente los recursos presentes
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-cierre#INV-1
refines: REQ-0023
```

## REQ-0110

```yaml requirement
uid: REQ-0110
level: software
kind: functional
criticality: high
statement: El cierre conserva la edición manual frente a confirmaciones pendientes.
acceptance_criteria:
- case: happy
  given: _conflicto manual_ pendiente
  when: se cierra voz
  then: cancela confirmación conservando dato
- case: error
  given: _conflicto manual_ pendiente
  when: se acepta la propuesta después
  then: no aplica aceptación tardía
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-cierre#INV-2
refines: REQ-0023
```

## REQ-0111

```yaml requirement
uid: REQ-0111
level: software
kind: functional
criticality: high
statement: Apagar voz en _captura_ no abre _revisión_.
acceptance_criteria:
- case: happy
  given: _captura_ activa
  when: se apaga voz
  then: permanece disponible la escritura manual
- case: error
  given: _captura_ activa
  when: se entra en _revisión_ explícitamente
  then: bloquea IA sin cola
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-cierre#INV-3
refines: REQ-0023
```

## REQ-0112

```yaml requirement
uid: REQ-0112
level: software
kind: functional
criticality: high
statement: El fallo de conexión permite continuación manual.
acceptance_criteria:
- case: happy
  given: inicio o _sesión de voz_ en curso
  when: ocurre fallo de red, credencial o GoAway
  then: muestra error recuperable con datos disponibles
- case: error
  given: inicio o _sesión de voz_ en curso
  when: no se pulsa micrófono otra vez
  then: no reconecta
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-cierre#INV-4
refines: REQ-0023
```

## REQ-0113

```yaml requirement
uid: REQ-0113
level: software
kind: functional
criticality: high
statement: El cierre local no promete liberación inmediata de cuota externa.
acceptance_criteria:
- case: happy
  given: error de concurrencia
  when: se cierra conexión local
  then: no afirma disponibilidad remota inmediata
- case: error
  given: error de concurrencia
  when: el proveedor sigue rechazando
  then: permite continuar manualmente
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-cierre#INV-5
refines: REQ-0023
```

## REQ-0114

```yaml requirement
uid: REQ-0114
level: software
kind: reliability
criticality: high
statement: El fallo del receptor de telemetría no impide cerrar voz.
acceptance_criteria:
- case: happy
  given: _sesión de voz_ fallida
  when: Faro falla o no responde
  then: continúa cierre y ruta manual
- case: error
  given: _sesión de voz_ fallida
  when: la emisión técnica lanza error
  then: conserva datos
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-cierre#INV-6
refines: REQ-0023
metric: alteraciones o bloqueos funcionales por fallo del sink
threshold: == 0 alteraciones
measurement_method:
  instrument: integration
  window: one test run
  sample: every applicable acceptance criterion with failing and indefinitely pending sinks
```

## REQ-0115

```yaml requirement
uid: REQ-0115
level: software
kind: functional
criticality: high
statement: Los eventos tardíos tras cierre no producen efectos.
acceptance_criteria:
- case: happy
  given: voz cerrada
  when: llega audio o llenar_campo rezagado
  then: descarta sin reproducir, mutar ni encolar
- case: error
  given: voz cerrada
  when: ya existe nuevo canal
  then: no responde a llamada antigua por él
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-cierre#INV-7
refines: REQ-0023
```

## REQ-0116

```yaml requirement
uid: REQ-0116
level: software
kind: functional
criticality: high
statement: Volver del _brief_ a _captura_ mantiene la voz cerrada.
acceptance_criteria:
- case: happy
  given: _brief_ visible
  when: se solicita corregir
  then: conserva datos con orbe solving
- case: error
  given: _brief_ visible
  when: no se pulsa micrófono
  then: no pide token ni conecta WSS
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-cierre#INV-8
refines: REQ-0023
```

## REQ-0117

```yaml requirement
uid: REQ-0117
level: software
kind: functional
criticality: high
statement: La nueva activación repite el permiso antes de emisión.
acceptance_criteria:
- case: happy
  given: _captura_ tras cierre
  when: se pulsa de nuevo micrófono
  then: comprueba permiso antes de token
- case: error
  given: _captura_ tras cierre
  when: el inicio ya está pendiente
  then: bloquea pulsaciones adicionales
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-cierre#INV-9
refines: REQ-0023
```

## REQ-0118

```yaml requirement
uid: REQ-0118
level: software
kind: functional
criticality: high
statement: La nueva activación no reutiliza la autorización consumida.
acceptance_criteria:
- case: happy
  given: _sesión de voz_ anterior cerrada
  when: se inicia voz otra vez
  then: solicita _credencial efímera_ nueva de un uso
- case: error
  given: _sesión de voz_ anterior cerrada
  when: la nueva emisión falla
  then: no reutiliza el token anterior
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-cierre#INV-10
refines: REQ-0023
```

## REQ-0119

```yaml requirement
uid: REQ-0119
level: software
kind: functional
criticality: high
statement: La nueva sesión recibe el contexto previamente capturado.
acceptance_criteria:
- case: happy
  given: nueva _sesión de voz_ lista
  when: se aporta contexto
  then: incluye campos previos sin sobrescribirlos
- case: error
  given: nueva _sesión de voz_ lista
  when: se emite telemetría
  then: no incluye esos valores
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-cierre#INV-11
refines: REQ-0023
```

## REQ-0120

```yaml requirement
uid: REQ-0120
level: software
kind: functional
criticality: high
statement: La continuación tras cierre no exige reactivar voz.
acceptance_criteria:
- case: happy
  given: voz apagada sin fallo
  when: el _visitante_ continúa manualmente
  then: puede completar la _solicitud_
- case: error
  given: voz apagada sin fallo
  when: no se recibe ningún evento tardío
  then: no exige atravesar rama de error
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-cierre#INV-12
refines: REQ-0023
```

## REQ-0155

```yaml requirement
uid: REQ-0155
level: software
kind: functional
criticality: high
statement: El _visitante_ puede continuar sin reactivar voz.
acceptance_criteria:
- case: happy
  given: voz cerrada
  when: sigue escribiendo
  then: completa _captura_ manualmente
- case: error
  given: voz cerrada
  when: vuelve desde el _brief_
  then: la voz sigue apagada
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-cierre#visitor
refines: REQ-0001
```

## REQ-0156

```yaml requirement
uid: REQ-0156
level: software
kind: functional
criticality: high
statement: La interfaz deja de reproducir audio tras el cierre.
acceptance_criteria:
- case: happy
  given: audio en _sesión de voz_
  when: se apaga micrófono
  then: detiene reproducción
- case: error
  given: voz cerrada
  when: llega audio tardío
  then: lo descarta sin reproducir
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-cierre#frontend
refines: REQ-0002
```

## REQ-0157

```yaml requirement
uid: REQ-0157
level: software
kind: functional
criticality: high
statement: Una reconexión manual obtiene una autorización nueva.
acceptance_criteria:
- case: happy
  given: voz anterior cerrada
  when: se pulsa micrófono y se concede permiso
  then: solicita nueva _credencial efímera_
- case: error
  given: voz anterior cerrada
  when: el permiso se deniega
  then: no solicita token
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-cierre#token-issuer
refines: REQ-0003
```

## REQ-0158

```yaml requirement
uid: REQ-0158
level: software
kind: functional
criticality: high
statement: La nueva conversación recibe el contexto conservado.
acceptance_criteria:
- case: happy
  given: nueva _sesión de voz_ lista
  when: se inicia conversación
  then: recibe datos capturados como contexto
- case: error
  given: nueva _sesión de voz_ lista
  when: la nueva sesión falla
  then: no pierde los datos locales
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-cierre#gemini-live
refines: REQ-0004
```

## REQ-0186

```yaml requirement
uid: REQ-0186
level: software
kind: security
criticality: high
statement: Los eventos del flujo de cierre de voz excluyen datos personales, campos, audio y credenciales.
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
derived_from: voz-cierre#grafana-faro
refines: REQ-0017
metric: filtraciones de datos protegidos en eventos
threshold: == 0 filtraciones
measurement_method:
  instrument: security
  window: one test run
  sample: every applicable acceptance criterion with canary data
```

## REQ-0187

```yaml requirement
uid: REQ-0187
level: software
kind: observability
criticality: medium
statement: La instrumentación emite los eventos técnicos esperados del flujo de cierre de voz.
acceptance_criteria:
- case: happy
  given: intentos técnicos del flujo con receptor disponible
  when: se ejecutan todos los casos de aceptación
  then: emite tbo.voz_cierre.start y tbo.voz_cierre.end con event, requirement=REQ-0187 y correlation_id del intento
- case: edge
  given: intentos técnicos del flujo con receptor disponible
  when: el caso termina en error
  then: emite tbo.voz_cierre.error en lugar de tbo.voz_cierre.end con event, requirement=REQ-0187 y correlation_id del intento
feasibility: Viable con señales técnicas sin contenido; una prueba de integración @sdoc[REQ-0187] comprueba literalmente los eventos y sus tres campos obligatorios.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-cierre#frontend
refines: REQ-0017
metric: eventos esperados emitidos con receptor disponible
threshold: == 100 %
measurement_method:
  instrument: integration
  window: one test run
  sample: every acceptance criterion (happy, edge, error) of REQ-0109, REQ-0110, REQ-0111, REQ-0112, REQ-0113, REQ-0115, REQ-0116, REQ-0117, REQ-0118, REQ-0119, REQ-0120, REQ-0155, REQ-0156, REQ-0157, REQ-0158, REQ-0197; receiver available
events:
- tbo.voz_cierre.start
- tbo.voz_cierre.end
- tbo.voz_cierre.error
watched_by:
- 'Comprobación de integración: cada evento esperado y sus campos event, requirement y correlation_id; ausencia detectada hace fallar la prueba.'
```

## REQ-0197

```yaml requirement
uid: REQ-0197
level: software
kind: functional
criticality: high
statement: Los fallos del navegador se notifican al receptor técnico externo.
acceptance_criteria:
- case: happy
  given: fallo de voz
  when: se emite evento
  then: se usa browser-telemetry-sink hacia Faro
- case: error
  given: fallo de voz
  when: Faro falla
  then: no bloquea continuación manual
feasibility: Viable mediante el comportamiento descrito; verificar los límites externos con dobles y contratos antes de integrar.
size: S
environment:
- element: navegador y dispositivo de audio
  impact: permiso de micrófono y liberación de recursos locales
- element: proveedor de voz externo
  impact: disponibilidad y autorización temporal sujetas al contrato verificado
derived_from: voz-cierre#INV-6
refines: REQ-0008
```

