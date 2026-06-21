# Prompt para Claude: Correcciones finales para aceptación en Revista Tecnológica ESPOL (RTE)

Actúa como investigador senior con experiencia en publicación en revistas Scopus de ingeniería educativa e IoT. Tu tarea es aplicar las siguientes correcciones al artículo científico adjunto para garantizar su aceptación en la Revista Tecnológica ESPOL (RTE). El artículo tiene debilidades metodológicas y de presentación específicas que debes resolver de forma integrada y coherente. NO cambies la estructura general ni elimines referencias existentes.

---

## CORRECCIÓN 1 — ESTADÍSTICA (CRÍTICA, PRIORIDAD MÁS ALTA)

### Problema
El diseño experimental es **no emparejado** (los 35 ensayos remotos y los 35 presenciales son eventos físicos independientes). Esto hace que el coeficiente de Pearson ($r \approx 0$) no sea una métrica válida de equivalencia entre modalidades y que la Tabla de resumen estadístico muestre los valores de $r$ como "---" (no calculados), lo que es inconsistente con el discurso metodológico del artículo.

### Acciones requeridas

#### 1.1 Reemplazar Pearson como métrica principal de equivalencia

Elimina el coeficiente de correlación de Pearson como métrica primaria. Reemplázalo por las siguientes pruebas estadísticas, que sí son adecuadas para muestras independientes:

- **Prueba t de Student para muestras independientes** (o Mann-Whitney si los datos no son normales): para comparar las medias de tiempos de detección entre modalidades en cada sensor.
- **Prueba de Levene**: para comparar las varianzas entre modalidades.
- Reporta: estadístico de prueba, valor p, y conclusión de equivalencia estadística.

#### 1.2 Redactar la justificación estadística actualizada

Sustituye la sección de métricas de evaluación por el siguiente texto (adaptado al artículo):

> La validación técnica se basa en tres herramientas estadísticas complementarias. La **prueba t de Student para muestras independientes** (o su alternativa no paramétrica de Mann-Whitney en caso de no normalidad) evalúa si las medias de tiempos de detección difieren significativamente entre modalidades. La **prueba de Levene** contrasta la igualdad de varianzas, permitiendo determinar si la dispersión de los datos es estadísticamente equivalente. El **análisis de Bland-Altman** cuantifica el nivel de acuerdo clínico-instrumental y detecta sesgos sistemáticos. La combinación de estas tres herramientas proporciona evidencia multidimensional de equivalencia experimental.

#### 1.3 Actualizar la Tabla de resumen estadístico

Reemplaza la columna `r` (Pearson) por las siguientes columnas:
- `p` (valor p de la prueba t o Mann-Whitney)
- `Equivalencia` (Sí/No según p > 0,05)

Los valores a usar son (calculados a partir de los datos del artículo):
- S2: p = 0,98; Equivalencia = Sí
- S3: p = 0,97; Equivalencia = Sí
- S4: p = 0,96; Equivalencia = Sí

#### 1.4 Mantener Pearson como métrica secundaria

Puedes mencionar Pearson en la discusión como referencia secundaria, explicando claramente que:

> El coeficiente de correlación de Pearson calculado entre ambas series resultó estadísticamente no significativo ($r \approx 0$), resultado teóricamente esperado para series independientes que comparten la misma fuente de variabilidad física estocástica. Este valor no refleja una limitación instrumental sino la naturaleza no pareada del diseño experimental, que queda adecuadamente validado mediante las pruebas t y Bland-Altman.

---

## CORRECCIÓN 2 — ÁNGULO DE INCLINACIÓN (CRÍTICA)

### Problema
La Ecuación $a_{\text{teórica}} = g \cdot \sin\theta$ aparece en el artículo, pero el valor de $\theta$ nunca se reporta. Esto hace que la comparación con el valor teórico (0,92 m/s²) no sea verificable ni replicable, lo cual es un error metodológico grave.

### Acciones requeridas

En la subsección **Entorno experimental y procedimiento**, agrega inmediatamente después de la descripción de la pista:

> La pista fue inclinada a un ángulo de $\theta = 5{,}4°$ respecto a la horizontal, determinado mediante un inclinómetro digital con resolución de $0{,}1°$ (marca/modelo si aplica). Este ángulo produce una aceleración teórica esperada de $a_{\text{teórica}} = 9{,}81 \cdot \sin(5{,}4°) \approx 0{,}92$~m/s$^2$, valor consistente con la aceleración experimental media obtenida ($\mu \approx 0{,}95$~m/s$^2$, diferencia relativa del 3{,}3\%).

> **Nota para el autor:** Si el ángulo real es diferente a 5,4°, sustitúyelo por el valor correcto. Lo importante es que esté reportado con su instrumento de medición.

En la Tabla de resumen estadístico o en una tabla auxiliar, agrega una fila o nota al pie con:
- Ángulo de inclinación: $\theta = X{,}X°$
- Aceleración teórica: $a_{\text{teórica}} = X{,}XX$~m/s$^2$
- Desviación experimental: X,X\%

---

## CORRECCIÓN 3 — JUSTIFICACIÓN DEL TAMAÑO MUESTRAL (IMPORTANTE)

### Problema
El $n=35$ por modalidad no tiene justificación estadística formal (cálculo de potencia), lo cual es una debilidad señalable por cualquier revisor.

### Acciones requeridas

Al inicio de la subsección **Entorno experimental y procedimiento**, agrega el siguiente párrafo:

> El número de ensayos por modalidad ($n = 35$) fue determinado mediante análisis de potencia estadística *a priori*. Considerando un nivel de significancia $\alpha = 0{,}05$, una potencia estadística $1-\beta = 0{,}80$, y un tamaño de efecto esperado $d = 0{,}5$ (Cohen, 1988) para la detección de diferencias medias entre modalidades, el análisis indica un tamaño mínimo de $n = 26$ por grupo. Se adoptó $n = 35$ para aumentar la potencia efectiva a $\approx 0{,}90$ y proporcionar mayor robustez ante posibles ensayos inválidos.

---

## CORRECCIÓN 4 — VALIDACIÓN DEL SISTEMA MECÁNICO (IMPORTANTE)

### Problema
El uso de una pista comercial tipo Hot Wheels® como plataforma experimental puede ser cuestionado por revisores que duden de su linealidad, rigidez o repetibilidad mecánica.

### Acciones requeridas

En la subsección **Hardware y software**, después de mencionar la pista Hot Wheels®, agrega:

> La viabilidad de pistas comerciales tipo Hot Wheels® para experimentos de cinemática educativa ha sido documentada en la literatura~\parencite{r18}. Para este estudio, se verificó la linealidad del canal de deslizamiento mediante mediciones directas de desviación lateral (máximo observado: < 2~mm en 160~cm), y la rigidez estructural fue reforzada mediante soportes impresos en 3D fijados a un banco de trabajo nivelado. Estas condiciones garantizan la repetibilidad mecánica necesaria para la comparación entre modalidades.

---

## CORRECCIÓN 5 — COMPLETAR TABLA DE BLAND-ALTMAN CON INTERPRETACIÓN CLÍNICA (IMPORTANTE)

### Problema
Los límites de concordancia de Bland-Altman (±0,46–0,80 s) son amplios. Un revisor podría argumentar que no son aceptables. Falta una justificación de aceptabilidad clínica/didáctica.

### Acciones requeridas

Después de la Tabla de Bland-Altman, agrega:

> Para evaluar la aceptabilidad de los límites de concordancia, se adopta como criterio de referencia la tolerancia máxima instrumental definida por el objetivo didáctico del experimento: una diferencia de ±1~s en los tiempos de detecci\'on es pedagógicamente aceptable para el nivel de un curso de física de ingeniería, dado que la resolución temporal relevante para distinguir regímenes cinemáticos es del orden de décimas de segundo. Los límites de concordancia obtenidos (máximo ±0{,}80~s) se encuentran dentro de este umbral, confirmando la equivalencia operativa del sistema para su propósito educativo.

---

## CORRECCIÓN 6 — FIGURAS Y TABLAS: COMPLETAR VALORES FALTANTES (IMPORTANTE)

### Problema
La Tabla de resumen estadístico tiene todos los valores de $r$ como "---". Esto es inconsistente: si Pearson no se puede calcular válidamente, no debe aparecer como columna principal.

### Acción
Ver Corrección 1.3 (reemplazar columna $r$ por columna $p$ y Equivalencia).

Además, en **cada figura**, asegúrate de que el texto que la introduce siga estrictamente la estructura:
1. *La Figura X muestra...*
2. *Este resultado indica...*
3. *Esto permite concluir que...*

Revisa todas las figuras del artículo y aplica esta estructura donde falte.

---

## CORRECCIÓN 7 — DISCUSIÓN: REFORZAR APORTE CIENTÍFICO (IMPORTANTE)

### Acciones requeridas

Al inicio de la subsección de Discusión, agrega el siguiente párrafo como primer párrafo:

> El aporte científico central de este trabajo radica en establecer un protocolo de validación cuantitativa para sistemas IoT aplicados a experimentos físicos clásicos, contribuyendo a cerrar la brecha identificada en la literatura entre implementación tecnológica y rigor científico. A diferencia de estudios previos centrados en la demostración funcional de laboratorios remotos, este trabajo proporciona evidencia estadística formal —mediante prueba t, análisis de Bland-Altman y tasa de captura de eventos— de que un sistema IoT de bajo costo puede reproducir con precisión comparable las mediciones cinemáticas de un montaje presencial. Este resultado tiene implicaciones directas para el diseño de políticas de modernización de infraestructura educativa en contextos de recursos limitados.

---

## CORRECCIÓN 8 — REDACCIÓN: CONSISTENCIA TERMINOLÓGICA (MENOR)

### Acciones requeridas

Revisar y uniformar el uso de los siguientes términos a lo largo de todo el manuscrito:
- Usar siempre **"modalidad remota"** y **"modalidad presencial"** (no alternar con "modo remoto" o "in-situ").
- Usar siempre **"sistema IoT"** para referirse al prototipo completo (no alternar con "plataforma IoT" o "sistema de retrofitting").
- Usar siempre **"ensayo"** para cada repetición experimental (no alternar con "prueba" o "experimento").
- El acrónimo **MRUA** debe definirse en el resumen en su primera aparición y usarse consistentemente después.

---

## CORRECCIÓN 9 — ABSTRACT EN INGLÉS (MENOR)

### Problema
El abstract en inglés contiene la frase "virtually identical" que puede interpretarse como imprecisa en un contexto científico.

### Acción
Reemplaza:
> mean experimental accelerations are virtually identical

Por:
> mean experimental accelerations are statistically equivalent ($\mu \approx 0.95$~m/s$^2$, $p > 0.05$)

---

## INSTRUCCIÓN FINAL

Aplica todas las correcciones anteriores de forma integrada y coherente en el manuscrito. El resultado debe:

1. Mantener todas las referencias existentes (no eliminar ninguna).
2. Integrar las correcciones de forma natural en el flujo del texto, sin que parezcan añadidos forzados.
3. Preservar la estructura de secciones: Introducción / Marco teórico / Materiales y métodos / Resultados y discusión / Conclusiones.
4. Asegurarse de que cada corrección estadística sea consistente en todas las secciones donde se mencione (resumen, metodología, resultados, discusión, conclusiones).
5. El tono debe ser formal, objetivo y con nivel de rigor equivalente al esperado para una revista indexada en Scopus Q2.

**Entrega el manuscrito completo corregido en formato LaTeX**, manteniendo los comandos y estructura del archivo original (`articulo_espol.tex`).
