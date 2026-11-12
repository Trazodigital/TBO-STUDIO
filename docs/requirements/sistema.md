# Requisitos de sistema

Borrador de etapa 2; pendiente de revisión independiente de criterios y Checkpoint 2.

## REQ-0001

```yaml requirement
uid: REQ-0001
level: system
kind: interface
criticality: high
statement: El _visitante_ decide cuándo confirmar su _solicitud_.
acceptance_criteria:
- case: happy
  given: _brief_ visible
  when: pulsa ENVIAR _SOLICITUD_
  then: se inicia un intento confirmado
- case: error
  given: _brief_ visible
  when: no confirma
  then: no se inicia entrega
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#visitor
```

## REQ-0002

```yaml requirement
uid: REQ-0002
level: system
kind: interface
criticality: high
statement: El formulario conserva un estado único para escritura y voz.
acceptance_criteria:
- case: happy
  given: _captura_ disponible
  when: se acepta un valor por voz
  then: el formulario muestra ese valor
- case: error
  given: _captura_ disponible
  when: la voz falla
  then: el valor aceptado permanece
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#frontend
```

## REQ-0003

```yaml requirement
uid: REQ-0003
level: system
kind: interface
criticality: high
statement: El servidor entrega únicamente una _credencial efímera_ al navegador.
acceptance_criteria:
- case: happy
  given: permiso concedido
  when: se obtiene autorización temporal
  then: se devuelve la _credencial efímera_
- case: error
  given: permiso concedido
  when: la emisión falla
  then: se devuelve error sin clave permanente
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#token-issuer
```

## REQ-0004

```yaml requirement
uid: REQ-0004
level: system
kind: interface
criticality: high
statement: La _sesión de voz_ intercambia propuestas de campos con el navegador.
acceptance_criteria:
- case: happy
  given: _sesión de voz_ activa
  when: el asistente propone un campo
  then: el navegador recibe llenar_campo
- case: error
  given: _sesión de voz_ activa
  when: el campo es desconocido
  then: el estado permanece intacto
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#gemini-live
```

## REQ-0005

```yaml requirement
uid: REQ-0005
level: system
kind: interface
criticality: high
statement: El servidor rechaza solicitudes inválidas antes de su entrega externa.
acceptance_criteria:
- case: happy
  given: _solicitud_ recibida
  when: el servidor valida datos inválidos
  then: responde 4xx sin llamar al webhook
- case: error
  given: _solicitud_ recibida
  when: el correo tiene formato inválido
  then: la _solicitud_ no cruza la integración
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#lead-submitter
```

## REQ-0006

```yaml requirement
uid: REQ-0006
level: system
kind: interface
criticality: high
statement: La integración comunica el resultado de recepción al servidor.
acceptance_criteria:
- case: happy
  given: _solicitud_ válida enviada al webhook
  when: el webhook responde HTTP 2xx, incluso sin cuerpo
  then: el servidor considera confirmada la recepción sin comprobante adicional
- case: error
  given: _solicitud_ válida
  when: el webhook devuelve 5xx
  then: el servidor recibe un fallo
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#lead-webhook
```

## REQ-0007

```yaml requirement
uid: REQ-0007
level: system
kind: interface
criticality: high
statement: El producto encamina solicitudes al _destino comercial_ configurado.
acceptance_criteria:
- case: happy
  given: _solicitud_ válida
  when: la integración la acepta
  then: se encamina al receptor configurado
- case: error
  given: _solicitud_ válida
  when: la integración rechaza
  then: no se afirma recepción comercial
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#commercial-destination
```

## REQ-0008

```yaml requirement
uid: REQ-0008
level: system
kind: interface
criticality: medium
statement: Los eventos del navegador se dirigen al receptor técnico externo.
acceptance_criteria:
- case: happy
  given: evento técnico permitido
  when: frontend lo emite
  then: usa browser-telemetry-sink
- case: edge
  given: evento técnico permitido
  when: el receptor falla
  then: no se transforma en registro comercial
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#grafana-faro
```

## REQ-0009

```yaml requirement
uid: REQ-0009
level: system
kind: interface
criticality: medium
statement: Los eventos del servidor se dirigen al receptor técnico externo.
acceptance_criteria:
- case: happy
  given: evento técnico permitido
  when: el servidor lo emite
  then: usa structured-log-sink
- case: edge
  given: evento técnico permitido
  when: el receptor falla
  then: no se transforma en registro comercial
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#grafana-loki
```

## REQ-0010

```yaml requirement
uid: REQ-0010
level: system
kind: interface
criticality: medium
statement: El _visitante_ puede aportar datos mediante la interfaz de consulta.
acceptance_criteria:
- case: happy
  given: página abierta
  when: accede a consulta
  then: encuentra los campos de contacto
- case: edge
  given: página abierta
  when: no usa micrófono
  then: los campos siguen disponibles
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#capture
```

## REQ-0011

```yaml requirement
uid: REQ-0011
level: system
kind: interface
criticality: high
statement: La interfaz solicita autorización temporal mediante token-issuance-api.
acceptance_criteria:
- case: happy
  given: permiso concedido
  when: el _visitante_ inicia voz
  then: frontend pide la _credencial efímera_ al servidor
- case: error
  given: _captura_ disponible
  when: el permiso se deniega
  then: no solicita autorización
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#token-request
```

## REQ-0012

```yaml requirement
uid: REQ-0012
level: system
kind: interface
criticality: high
statement: El emisor obtiene autorización temporal mediante gemini-token-source.
acceptance_criteria:
- case: happy
  given: petición autorizada
  when: el proveedor acepta la emisión
  then: devuelve una _credencial efímera_
- case: error
  given: petición autorizada
  when: el proveedor falla
  then: se comunica error de emisión
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#token-source
```

## REQ-0013

```yaml requirement
uid: REQ-0013
level: system
kind: interface
criticality: high
statement: La voz establece un canal directo entre navegador y proveedor.
acceptance_criteria:
- case: happy
  given: _credencial efímera_ válida
  when: se inicia conexión
  then: el canal WSS va directamente al proveedor
- case: error
  given: _credencial efímera_ válida
  when: falla WSS
  then: no exige un proxy de audio propio
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#voice-channel
```

## REQ-0014

```yaml requirement
uid: REQ-0014
level: system
kind: interface
criticality: high
statement: La interfaz entrega la _solicitud_ mediante lead-submission-api.
acceptance_criteria:
- case: happy
  given: _brief_ confirmado
  when: se inicia el intento
  then: el POST llega a lead-submitter
- case: error
  given: _brief_ confirmado
  when: el servidor rechaza
  then: la interfaz conserva el _brief_
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#lead-request
```

## REQ-0015

```yaml requirement
uid: REQ-0015
level: system
kind: interface
criticality: high
statement: La entrega externa usa lead-destination después de validar.
acceptance_criteria:
- case: happy
  given: _solicitud_ válida
  when: el servidor la procesa
  then: llama al webhook por lead-destination
- case: error
  given: _solicitud_ recibida
  when: la _solicitud_ es inválida
  then: no llama a lead-destination
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#validated-delivery
```

## REQ-0016

```yaml requirement
uid: REQ-0016
level: system
kind: interface
criticality: high
statement: La integración encamina la _solicitud_ aceptada al _destino comercial_.
acceptance_criteria:
- case: happy
  given: recepción confirmada
  when: se encamina la _solicitud_
  then: se utiliza el receptor configurado
- case: error
  given: recepción confirmada
  when: sólo consta HTTP 202
  then: no se afirma persistencia final
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#external-routing
```

## REQ-0017

```yaml requirement
uid: REQ-0017
level: system
kind: interface
criticality: high
statement: El navegador separa la telemetría del contenido comercial.
acceptance_criteria:
- case: happy
  given: consulta en _captura_
  when: ocurre un fallo técnico
  then: se emite sólo metadato técnico
- case: error
  given: consulta en _captura_
  when: el _brief_ contiene datos personales
  then: no se incorpora a la telemetría
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#browser-events
```

## REQ-0018

```yaml requirement
uid: REQ-0018
level: system
kind: interface
criticality: high
statement: El emisor registra el resultado técnico de emisión.
acceptance_criteria:
- case: happy
  given: intento de autorización
  when: termina la emisión
  then: se registra resultado técnico
- case: error
  given: intento de autorización
  when: la clave permanente está disponible
  then: no se registra la clave
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#token-logs
```

## REQ-0019

```yaml requirement
uid: REQ-0019
level: system
kind: interface
criticality: high
statement: El servidor registra el resultado técnico de validación y entrega.
acceptance_criteria:
- case: happy
  given: _solicitud_ recibida
  when: se resuelve el intento
  then: se registra resultado técnico
- case: error
  given: intento de entrega en cliente
  when: el POST nunca llega al servidor
  then: no se inventa registro de recepción
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#lead-logs
```

## REQ-0020

```yaml requirement
uid: REQ-0020
level: system
kind: functional
criticality: high
statement: La clave permanente permanece exclusivamente en servidor.
acceptance_criteria:
- case: happy
  given: emisión configurada
  when: el navegador solicita autorización
  then: sólo recibe la _credencial efímera_
- case: error
  given: emisión configurada
  when: se inspeccionan respuestas y eventos
  then: no contienen la clave permanente
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#INV-1
```

## REQ-0021

```yaml requirement
uid: REQ-0021
level: system
kind: functional
criticality: high
statement: La consulta manual funciona sin una _sesión de voz_.
acceptance_criteria:
- case: happy
  given: formulario disponible
  when: el _visitante_ completa el recorrido manual
  then: puede confirmar su _brief_
- case: error
  given: formulario disponible
  when: el proveedor de voz no responde
  then: la vía manual sigue completa
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#INV-2
```

## REQ-0022

```yaml requirement
uid: REQ-0022
level: system
kind: interface
criticality: high
statement: El navegador no entrega solicitudes directamente al webhook.
acceptance_criteria:
- case: happy
  given: _brief_ confirmado
  when: se inicia entrega
  then: el navegador contacta al servidor propio
- case: error
  given: _brief_ confirmado
  when: el servidor rechaza
  then: no hay llamada de navegador al webhook
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#INV-3
```

## REQ-0023

```yaml requirement
uid: REQ-0023
level: system
kind: functional
criticality: high
statement: La interfaz conserva el _brief_ cuando el envío falla.
acceptance_criteria:
- case: happy
  given: _brief_ confirmado
  when: el intento falla
  then: el _brief_ permanece disponible
- case: error
  given: _brief_ confirmado
  when: el cliente agota 10 s
  then: no se afirma que el servidor no recibió la _solicitud_
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#INV-4
```

## REQ-0024

```yaml requirement
uid: REQ-0024
level: system
kind: functional
criticality: high
statement: La configuración conecta las dependencias sin añadir un intermediario comercial.
acceptance_criteria:
- case: happy
  given: cuatro módulos propios
  when: se configura la integración
  then: los siete puertos están conectados a sus adaptadores
- case: error
  given: cuatro módulos propios
  when: se ejecuta una entrega
  then: composition-root no es un salto de red
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#INV-5
```

## REQ-0025

```yaml requirement
uid: REQ-0025
level: system
kind: functional
criticality: medium
statement: La observabilidad no sustituye la recepción comercial de solicitudes.
acceptance_criteria:
- case: happy
  given: evento técnico emitido
  when: el receptor técnico lo acepta
  then: sólo queda evidencia operativa
- case: edge
  given: evento técnico emitido
  when: el _destino comercial_ no confirma
  then: el evento no acredita entrega comercial
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#INV-6
```

## REQ-0026

```yaml requirement
uid: REQ-0026
level: system
kind: interface
criticality: high
statement: El navegador responde a las propuestas de campos por el canal de voz vigente.
acceptance_criteria:
- case: happy
  given: _sesión de voz_ activa
  when: recibe llenar_campo
  then: devuelve el resultado por el mismo canal
- case: error
  given: propuesta recibida tras cierre
  when: el canal está cerrado
  then: no responde por otra sesión
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: tbo-capture#INV-7
```

## REQ-0027

```yaml requirement
uid: REQ-0027
level: system
kind: constraint
criticality: high
statement: El producto limita su función comercial a captación y precalificación informativa.
acceptance_criteria:
- case: happy
  given: producto configurado
  when: se completa una consulta
  then: se entrega para evaluación por TBO
- case: error
  given: producto configurado
  when: se busca pago o cotización automática
  then: no se ofrece esa función
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: W-17
```

## REQ-0028

```yaml requirement
uid: REQ-0028
level: system
kind: constraint
criticality: high
statement: El producto opera sin almacenamiento comercial propio.
acceptance_criteria:
- case: happy
  given: _destino comercial_ configurado
  when: se acepta una _solicitud_
  then: el receptor comercial es externo
- case: error
  given: _destino comercial_ configurado
  when: la telemetría está disponible
  then: no funciona como base de prospectos
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: W-18
```

## REQ-0029

```yaml requirement
uid: REQ-0029
level: system
kind: constraint
criticality: medium
statement: La definición del producto no impone tecnología ni despliegue todavía no aprobados.
acceptance_criteria:
- case: happy
  given: contratos funcionales establecidos
  when: se revisa la especificación
  then: no impone stack ni alojamiento
- case: edge
  given: contratos funcionales establecidos
  when: se consideran alternativas históricas
  then: no se interpretan como decisión vigente
feasibility: Viable con validación y transiciones locales verificables sin una conversación real ni entrega externa.
size: S
environment: none
derived_from: W-19
```

