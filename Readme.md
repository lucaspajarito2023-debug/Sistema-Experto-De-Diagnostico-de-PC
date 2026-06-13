# 🧠 Sistema Experto de Diagnóstico de PC

## 📋 Descripción General

Este proyecto implementa un **Sistema Experto para Diagnóstico de Computadoras** desarrollado completamente en **Python**, utilizando técnicas clásicas de Inteligencia Artificial simbólica.

El sistema es capaz de identificar posibles fallas de hardware y software a partir de síntomas proporcionados por el usuario, aplicando mecanismos de:

* **Encadenamiento hacia Adelante (Forward Chaining)**
* **Encadenamiento hacia Atrás (Backward Chaining)**
* **Resolución de Conflictos**
* **Diagnóstico Múltiple con Ranking de Resultados**
* **Explicación del Proceso de Inferencia**

Su objetivo es simular el razonamiento de un técnico especializado mediante una base de conocimiento compuesta por reglas de diagnóstico.

---

# 🏗️ Arquitectura del Sistema

El sistema está compuesto por cinco elementos fundamentales que siguen la estructura clásica de un Sistema Experto.

## 1. Base de Conocimiento (Knowledge Base)

Almacena el conocimiento especializado del dominio mediante reglas del tipo:

```text
SI condición1 Y condición2
ENTONCES diagnóstico
```

Cada regla contiene:

* Identificador único.
* Conjunto de síntomas o condiciones.
* Diagnóstico asociado.
* Factor de confianza.

La implementación utiliza una lista de diccionarios para facilitar la gestión y expansión del conocimiento.

---

## 2. Base de Hechos (Working Memory)

Representa el estado actual del problema analizado.

Contiene los síntomas confirmados por el usuario durante la sesión de diagnóstico.

Se implementa mediante una estructura `set`, permitiendo:

* Búsquedas rápidas.
* Evitar duplicados.
* Complejidad promedio de acceso O(1).

---

## 3. Motor de Inferencia

Es el componente responsable del razonamiento.

### Funciones principales

#### Equiparación (Pattern Matching)

Determina qué reglas pueden activarse según los hechos actuales.

#### Resolución de Conflictos

Cuando varias reglas coinciden, el sistema determina cuáles deben priorizarse utilizando:

1. Factor de confianza.
2. Nivel de especificidad de la regla.

---

## 4. Sistema de Explicación

Proporciona transparencia sobre el razonamiento realizado.

Por cada diagnóstico generado, el sistema muestra:

* Regla utilizada.
* Síntomas que activaron la regla.
* Nivel de confianza obtenido.

Esto permite comprender cómo se alcanzó una conclusión determinada.

---

## 5. Interfaz de Usuario

Consiste en una consola interactiva que:

* Solicita síntomas al usuario.
* Actualiza la base de hechos.
* Ejecuta el motor de inferencia.
* Presenta diagnósticos y explicaciones.

---

# ⚙️ Mejoras Implementadas

Durante el desarrollo se realizaron diversas optimizaciones para aumentar la robustez y eficiencia del sistema.

## Normalización de Entradas

Las respuestas ingresadas por el usuario son procesadas mediante:

```python
.strip().lower()
```

Beneficios:

* Evita errores por mayúsculas o minúsculas.
* Elimina espacios innecesarios.
* Mejora la consistencia de los datos.

---

## Optimización de Equiparación

Se implementó:

```python
set.issubset()
```

para verificar si las condiciones de una regla están contenidas en la base de hechos.

Ventajas:

* Menor complejidad computacional.
* Mejor rendimiento con grandes cantidades de reglas.

---

## Resolución de Conflictos Mejorada

Las reglas se ordenan utilizando dos criterios:

1. Mayor factor de confianza.
2. Mayor número de condiciones.

Esto favorece diagnósticos más específicos y reduce resultados ambiguos.

---

# 🚀 Extensiones Desarrolladas

## Nivel 1: Expansión de la Base de Conocimiento

Se añadieron tres nuevas reglas de diagnóstico:

### R08 — Falla de Disco Duro

Síntoma principal:

* Ruido mecánico o clic repetitivo.

Diagnóstico:

* Posible daño físico del disco duro.

---

### R09 — Batería CMOS Agotada

Síntoma principal:

* Fecha y hora incorrectas al iniciar.

Diagnóstico:

* Batería CMOS descargada.

---

### R10 — Problema de Alimentación Eléctrica

Síntoma principal:

* Apagados inesperados bajo carga.

Diagnóstico:

* Fuente de poder insuficiente o defectuosa.

---

## Nivel 2: Diagnóstico Múltiple y Ranking

El sistema ya no devuelve una única conclusión.

Ahora genera una lista ordenada de posibles causas según:

* Nivel de confianza.
* Especificidad de la regla.

### Ejemplo

Un inicio lento podría estar relacionado con:

1. Malware.
2. Disco duro deteriorado.
3. Falta de memoria RAM.

Esto permite al usuario evaluar varias alternativas simultáneamente.

---

## Nivel 3: Encadenamiento hacia Atrás

Se implementó la función:

```python
backward_chain(meta, base_conocimiento, hechos)
```

Esta técnica permite validar hipótesis específicas.

### Ejemplo

Pregunta:

```text
¿Podría tratarse de sobrecalentamiento?
```

El sistema responde indicando:

* Qué síntomas ya respaldan la hipótesis.
* Qué síntomas faltan para confirmarla.

---

## Nivel 4: Exportación de la Red de Inferencia

Se desarrolló la función:

```python
exportar_red()
```

que genera una representación de la base de conocimiento en formato JSON.

### Beneficios

* Visualización de reglas.
* Construcción de grafos de inferencia.
* Integración con herramientas externas.
* Documentación automática de conocimiento.

---

# 📚 Reflexión sobre Sistemas Expertos

## ¿Cuál es la diferencia entre un Sistema Experto y un software tradicional?

Un software tradicional ejecuta instrucciones programadas de forma directa y determinista.

Por el contrario, un Sistema Experto:

* Se basa en conocimiento explícito.
* Razona sobre hechos.
* Puede manejar incertidumbre.
* Simula la toma de decisiones de un especialista.

Además, el comportamiento puede modificarse agregando o editando reglas sin alterar el motor de inferencia.

---

## ¿Por qué el conocimiento está separado del motor de razonamiento?

La arquitectura de los Sistemas Expertos distingue claramente:

### Base de Conocimiento

Contiene el saber especializado.

### Motor de Inferencia

Contiene los mecanismos de razonamiento.

### Ventajas

#### Mantenibilidad

Las reglas pueden modificarse sin afectar el funcionamiento interno del sistema.

#### Escalabilidad

Es posible ampliar el conocimiento agregando nuevas reglas.

#### Reutilización

El mismo motor podría utilizarse para:

* Diagnóstico médico.
* Asesoría legal.
* Soporte técnico.
* Sistemas educativos.

Simplemente cambiando la base de conocimiento.

---

## ¿Qué es la Base de Hechos y cómo se diferencia de la Base de Conocimiento?

### Base de Conocimiento

Contiene información general y permanente sobre el dominio.

Ejemplo:

```text
Si existe humo, entonces puede existir fuego.
```

---

### Base de Hechos

Contiene información específica del caso actual.

Ejemplo:

```text
Existe humo en la cocina.
```

---

### Diferencia Fundamental

| Base de Conocimiento | Base de Hechos             |
| -------------------- | -------------------------- |
| Información general  | Información específica     |
| Permanente           | Temporal                   |
| Reglas               | Observaciones              |
| Conocimiento experto | Estado actual del problema |

En términos simples:

* **Base de Conocimiento:** el manual de instrucciones.
* **Base de Hechos:** la situación que está ocurriendo en este momento.

---

# 🛠️ Tecnologías Utilizadas

* Python 3
* Programación Orientada a Objetos
* Sistemas Expertos
* Inteligencia Artificial Simbólica
* Encadenamiento hacia Adelante
* Encadenamiento hacia Atrás
* JSON

---
