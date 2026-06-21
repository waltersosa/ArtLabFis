# Prompt para Claude: Corrección integral del artículo científico

Actúa como un investigador senior y revisor experto de revistas indexadas en ingeniería, educación e IoT (Scopus Q1/Q2). Tu tarea es revisar y corregir el manuscrito completo manteniendo un estilo académico formal, coherencia entre secciones y lenguaje científico adecuado para publicación.

## Instrucciones generales

* Conserva las referencias y la estructura general del artículo.
* No elimines información relevante; mejora la redacción y el argumento científico.
* Mantén un tono objetivo y formal.
* Evita repeticiones.
* Incrementa la profundidad científica del manuscrito.
* Prioriza el rigor metodológico y la interpretación de resultados por encima de la descripción técnica.
* Todas las modificaciones deben integrarse de forma natural en el texto.

---

# 1. TÍTULO

## Problema

El término "laboratorio" puede resultar exagerado, ya que el trabajo desarrolla un experimento específico de MRUA y no un laboratorio completo.

## Acciones

### Opción preferida

Cambiar el título a:

> Implementación de un experimento de MRUA mediante retrofitting IoT en un entorno híbrido

### Si se mantiene la palabra "laboratorio"

Agregar en la introducción el siguiente párrafo:

> En este trabajo, el término "laboratorio" se refiere a una plataforma experimental modular y extensible, donde el experimento de MRUA se emplea como caso de validación inicial.

---

# 2. RESUMEN

Reescribir el resumen para incrementar:

* Impacto científico.
* Claridad del aporte.
* Uso estratégico de los resultados.

La estructura debe incluir:

1. Objetivo del estudio.
2. Diseño e implementación.
3. Número de ensayos realizados.
4. Resultados cuantitativos principales.
5. Análisis estadístico.
6. Contribución y aplicabilidad.

Debe incorporar ideas similares a:

* 70 ensayos independientes (35 remotos y 35 presenciales).
* Diferencias medias inferiores a 0.03 s.
* Aceleraciones experimentales prácticamente idénticas.
* Confirmación mediante Bland–Altman de ausencia de sesgo sistemático.
* Viabilidad del retrofitting IoT como solución escalable y de bajo costo para laboratorios híbridos.

---

# 3. INTRODUCCIÓN (PRIORIDAD ALTA)

La introducción debe seguir una estructura científica clara.

## 3.1 Contextualización

Conservar la contextualización actual, mejorando la redacción cuando sea necesario.

## 3.2 Problema

Incorporar explícitamente que:

> A pesar de los avances en laboratorios remotos, muchas implementaciones se centran en la demostración funcional, sin proporcionar validaciones cuantitativas rigurosas sobre la fidelidad experimental respecto a montajes presenciales.

## 3.3 Brecha de investigación (MUY IMPORTANTE)

Expresar claramente que:

> Existe una escasez de estudios que validen cuantitativamente si los sistemas remotos basados en IoT pueden reproducir con precisión el comportamiento físico de experimentos clásicos, como el MRUA, en comparación con mediciones presenciales.

## 3.4 Pregunta de investigación

Incorporar explícitamente:

> ¿Puede un sistema de retrofitting IoT de bajo costo reproducir con precisión y estabilidad las mediciones cinemáticas de un experimento de MRUA en comparación con un montaje presencial de referencia?

## 3.5 Objetivo

Expresar:

> El objetivo de este trabajo es diseñar, implementar y validar técnicamente un prototipo de laboratorio remoto basado en IoT para el estudio del MRUA.

## 3.6 Contribución principal (MUY IMPORTANTE)

Destacar que:

> La principal contribución de este estudio es la validación cuantitativa de la equivalencia experimental entre modalidades remota y presencial mediante análisis estadísticos como correlación de Pearson y Bland–Altman.

---

# 4. MARCO TEÓRICO

Fortalecer la relación conceptual entre:

* MRUA.
* Sensores.
* IoT.

Integrar un párrafo equivalente al siguiente:

> El experimento de MRUA se fundamenta en la medición de tiempos de paso del móvil entre posiciones fijas. En este sistema, los sensores infrarrojos permiten registrar estos eventos, mientras que el módulo IoT procesa las señales y genera marcas de tiempo que posteriormente son utilizadas para calcular velocidades y aceleraciones.

---

# 5. METODOLOGÍA

Justificar el uso del análisis estadístico.

Explicar que:

* La correlación de Pearson evalúa la consistencia en la captura de la variabilidad del fenómeno físico entre ambas modalidades.
* El análisis de Bland–Altman permite cuantificar el nivel de acuerdo y detectar posibles sesgos sistemáticos.

La justificación debe quedar integrada dentro de la metodología.

---

# 6. RESULTADOS

No limitarse a describir tablas y gráficos.

Añadir interpretación científica.

Ejemplo:

En lugar de expresiones como:

> Alta consistencia.

Utilizar una interpretación más profunda:

> La diferencia prácticamente nula entre las medias y la mínima variación en la desviación estándar indican que el sistema IoT reproduce con alta fidelidad las mediciones temporales del sistema presencial.

Al finalizar la sección de resultados, incorporar una síntesis general que indique que:

> En conjunto, los resultados muestran una alta concordancia entre ambas modalidades, evidenciando que el sistema IoT no introduce errores sistemáticos en las mediciones.

---

# 7. DISCUSIÓN (PRIORIDAD ALTA)

Profundizar la discusión.

No limitarse a comparar resultados.

Destacar que:

> A diferencia de estudios previos que enfatizan la implementación funcional de laboratorios remotos, este trabajo aporta una validación cuantitativa rigurosa de la equivalencia experimental.

Comparar además con soluciones comerciales indicando que:

> Las soluciones comerciales suelen implicar altos costos y sistemas propietarios, mientras que la propuesta desarrollada utiliza hardware de bajo costo y código abierto, manteniendo niveles de precisión comparables.

Resaltar continuamente el aporte científico del trabajo.

---

# 8. LIMITACIONES

Agregar una limitación adicional:

> Una limitación del estudio es la ausencia de mediciones explícitas de latencia en la cadena de comunicación.

Mantener un enfoque crítico y objetivo.

---

# 9. CONCLUSIONES

Reforzar las conclusiones para que destaquen claramente el aporte científico.

Las conclusiones deben enfatizar:

* Alta fidelidad del sistema.
* Diferencias inferiores a 0.03 s.
* Ausencia de sesgo sistemático.
* Equivalencia experimental entre modalidad remota y presencial.
* Potencial del retrofitting IoT para modernizar laboratorios educativos híbridos.

---

# 10. FIGURAS Y TABLAS

Cada figura o tabla debe explicarse utilizando una estructura similar a:

* La Figura X muestra...
* Estos resultados indican...
* Esto permite concluir que...

Evitar figuras y tablas sin interpretación científica.

---

# 11. APORTE CIENTÍFICO (MUY IMPORTANTE)

El artículo no debe percibirse únicamente como una aplicación técnica.

Debe resaltarse explícitamente que:

> El aporte de este trabajo radica en establecer un método de validación cuantitativa para sistemas IoT aplicados a experimentos físicos, contribuyendo a cerrar la brecha entre implementación tecnológica y rigor científico.

---

# PRIORIDADES DE REVISIÓN

## Críticas

1. Reescribir la introducción.
2. Explicitar la brecha de investigación.
3. Destacar claramente el aporte científico.
4. Fortalecer la discusión.
5. Interpretar adecuadamente los resultados.

## Importantes

1. Mejorar las conclusiones.
2. Integrar teoría y sistema IoT.
3. Explicar figuras y tablas.

## Menores

1. Ajustes de redacción.
2. Mejoras de estilo y presentación.

---

# Instrucción final

Reescribe el manuscrito completo aplicando todas estas observaciones de manera integrada y coherente. El resultado debe tener el nivel esperado para una revista científica indexada en Scopus, enfatizando el rigor metodológico, la validez experimental y la contribución científica del estudio.
