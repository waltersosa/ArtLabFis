#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_final.py — Aplica TODOS los bloques 1-4 de correcciones editoriales
"""
import re, os

SRC = 'template.tex'

with open(SRC, encoding='utf-8') as f:
    tex = f.read()

with open(SRC + '.bak4', 'w', encoding='utf-8') as f:
    f.write(tex)
print("Backup guardado.")

# ════════════════════════════════════════════════
# BLOQUE 1: CORRECCIONES DE TEXTO Y ECUACIONES
# ════════════════════════════════════════════════

# ERROR 5: Fijar label de ecuación mruateorico
tex = tex.replace(r'\label{eq:mrua_teorico}', r'\label{eq:mruateorico}')
tex = tex.replace(r'\ref{eq:mrua_teorico}', r'\ref{eq:mruateorico}')
print("OK - label eq:mruateorico")

# ERROR 5: Fijar dobles backslashes en subsección fundamento teórico
# Estas quedaron de una inyección anterior
old_block = (
    r'\subsection{Fundamento te\\' + "'" + r'orico del experimento MRUA}' + "\n\n" +
    r'El experimento implementado estudia el Movimiento Rectil\\' + "'" + r'ineo'
)
# Simplificado: limpiar directamente cualquier \\\\' residual en el texto del fundamento
# Reemplazar patrones específicos
tex = tex.replace("\\\\'orico", "\\'orico")
tex = tex.replace("\\\\'ineo", "\\'ineo")
tex = tex.replace("\\\\'on", "\\'on")
tex = tex.replace("\\\\'angulo", "\\'angulo")
tex = tex.replace("\\\\'a", "\\'a")
tex = tex.replace("\\\\theta", r"\theta")
tex = tex.replace("\\\\cdot", r"\cdot")
tex = tex.replace("\\\\sin", r"\sin")
tex = tex.replace("\\\\text{", r"\text{")
tex = tex.replace("\\\\label{", r"\label{")
tex = tex.replace("\\\\ref{", r"\ref{")
tex = tex.replace("\\\\Delta", r"\Delta")
tex = tex.replace("\\\\frac", r"\frac")
tex = tex.replace("\\\\bar", r"\bar")
print("OK - dobles backslashes en ecuaciones MRUA corregidos")

# ERROR 4: Referencia rota "Ecuación ??"
tex = re.sub(
    r'definido por la Ecuaci[oó]n\s?\?\?',
    r"definido por la Ecuaci\\'on~\\ref{eq:mruateorico}",
    tex
)
print("OK - Ecuacion ?? corregida")

# ERROR 3: Párrafo duplicado S1 (línea 347 — versión sin \ref)
dup_para = (
    r'Como se muestra en la Figura 7, los puntos de datos se concentran en el origen. '
    r"El coeficiente de correlaci\\'on es t\\'ecnicamente indefinido o nulo porque la "
    r"varianza de los datos es cero ( s= 0). Este comportamiento es f\\'isicamente "
    r"esperado y confirma que S1 funciona correctamente como punto de referencia de "
    r"sincronizaci\\'on tanto para el cron\\'ometro manual como para el m\\'odulo de "
    r"control digital. No hay fluctuaciones ni ruido experimental que afecten este estado inicial."
)
if dup_para in tex:
    tex = tex.replace(dup_para + "\n\n", "", 1)
    print("OK - Párrafo duplicado S1 eliminado")
else:
    # Regex flexible
    pat = (r'Como se muestra en la Figura 7, los puntos de datos se concentran en el origen\.'
           r'.*?No hay fluctuaciones ni ruido experimental que afecten este estado inicial\.\n\n')
    new_tex, n = re.subn(pat, '', tex, count=1, flags=re.DOTALL)
    if n:
        tex = new_tex
        print("OK - Párrafo duplicado S1 eliminado (regex)")
    else:
        print("AVISO - párrafo duplicado S1 no encontrado, quizá ya fue eliminado")

# ERROR 1: Texto incorrecto Sensor S2 — reemplazar párrafo con r<0.3
S2_NEW = (
    r"La Figura~\ref{fig:corr_s2} presenta la gr\'afica de dispersi\'on para S2, con"
    "\n"
    r"un coeficiente de correlaci\'on de Pearson moderado"
    "\n"
    r"($r = 0.61$, $R^2 = 0.37$, $N = 35$). Este valor refleja una"
    "\n"
    r"asociaci\'on lineal positiva estad\'isticamente significativa entre"
    "\n"
    r"ambas modalidades. La dispersi\'on observada es coherente con la"
    "\n"
    r"independencia f\'isica de los ensayos: dado que cada par"
    "\n"
    r"(presencial, remoto) corresponde a eventos f\'isicos distintos"
    "\n"
    r"sujetos a diferentes condiciones iniciales de fricci\'on y"
    "\n"
    r"liberaci\'on del carrito, una correlaci\'on perfecta ($r \approx 1$)"
    "\n"
    r"ser\'ia f\'isicamente imposible. El valor $r = 0.61$ con medias"
    "\n"
    r"pr\'acticamente id\'enticas ($\bar{x}_P = 1.17$~s vs.\ "
    "\n"
    r"$\bar{y}_R = 1.19$~s, $\Delta\bar{x} = 0.02$~s) confirma"
    "\n"
    r"que el sistema IoT captura la variabilidad natural del MRUA"
    "\n"
    r"sin introducir sesgo sistem\'atico."
)

pat_s2 = (r'La gr[aá]fica de la Figura.*?corr_s2.*?captura la variabilidad natural del '
          r'fen[oó]meno de MRUA\.')
new_tex, n = re.subn(pat_s2, lambda m: S2_NEW, tex, count=1, flags=re.DOTALL)
if n:
    tex = new_tex
    print("OK - Texto S2 reemplazado")
else:
    # Intentar con el texto en unicode directo
    pat_s2b = (r'La gráfica de la Figura.*?captura la variabilidad natural del '
               r'fenómeno de MRUA\.')
    new_tex, n = re.subn(pat_s2b, S2_NEW, tex, count=1, flags=re.DOTALL)
    if n:
        tex = new_tex
        print("OK - Texto S2 reemplazado (variante unicode)")
    else:
        print("AVISO - texto S2 no encontrado")

# ERROR 2: Texto incorrecto Sensor S3 — reemplazar párrafo con "baja correlación"
S3_NEW = (
    r"La Figura~\ref{fig:corr_s3} muestra la gr\'afica de dispersi\'on para S3, con"
    "\n"
    r"$r = 0.62$, $R^2 = 0.39$, $N = 35$: el coeficiente m\'as alto"
    "\n"
    r"de la serie, indicando una correlaci\'on moderada positiva."
    "\n"
    r"Este resultado es consistente con el mayor rango temporal"
    "\n"
    r"del sensor ($\bar{x}_P = 1.66$~s), que ampl\'ifica la"
    "\n"
    r"variabilidad f\'isica acumulada del MRUA y enriquece la"
    "\n"
    r"se\~nal estad\'istica. Las desviaciones est\'andar pr\'acticamente"
    "\n"
    r"id\'enticas ($\sigma_P = 0.23$~s vs.\ $\sigma_R = 0.24$~s,"
    "\n"
    r"$\Delta\sigma = 0.01$~s) demuestran que la detecci\'on"
    "\n"
    r"automatizada por interrupciones de hardware del m\'odulo de"
    "\n"
    r"control replica la dispersi\'on del cronometraje manual con"
    "\n"
    r"una fidelidad estad\'isticamente equivalente."
)

pat_s3 = (r'La Figura.*?corr_s3.*?precisi[oó]n similar\.')
new_tex, n = re.subn(pat_s3, lambda m: S3_NEW, tex, count=1, flags=re.DOTALL)
if n:
    tex = new_tex
    print("OK - Texto S3 reemplazado")
else:
    pat_s3b = r'La Figura.*?nube de puntos con baja correlaci[oó]n.*?precisi[oó]n similar\.'
    new_tex, n = re.subn(pat_s3b, lambda m: S3_NEW, tex, count=1, flags=re.DOTALL)
    if n:
        tex = new_tex
        print("OK - Texto S3 reemplazado (variante)")
    else:
        print("AVISO - texto S3 no encontrado")

# ERROR 6: Artefactos de encoding
encoding_fixes = [
    ("dise\u00b4no", "dise\\~no"),
    ("\u00edPuede", "\\textquestiondown{}Puede"),
    ("te\u00b4orico", "te\\'orico"),
    ("u\u00b4ltimo", "\\'ultimo"),
    ("\u0131\u0301ndice", "\\'indice"),
]
for bad, good in encoding_fixes:
    if bad in tex:
        tex = tex.replace(bad, good)
        print(f"OK - encoding: {repr(bad)} corregido")

# ════════════════════════════════════════════════
# BLOQUE 2: RENUMERACIÓN DE REFERENCIAS
# Mapa antiguo→nuevo (usar prefijo "ZZZ" para evitar colisiones)
# ════════════════════════════════════════════════

# Añadir cita de Chang [r52] si no existe
if r'\cite{r52}' not in tex:
    # Buscar después del párrafo de Marosan
    old_marosan = r"confirmando la idoneidad del m\'odulo de control adoptado en este estudio."
    new_marosan = (old_marosan + " Chang et al.~\\cite{r52} reportan resultados similares al "
                   "desplegar una plataforma remota IoT para pr\'acticas de mec\'anica "
                   "universitaria, confirmando la viabilidad del enfoque adoptado en este trabajo.")
    if old_marosan in tex:
        tex = tex.replace(old_marosan, new_marosan, 1)
        print("OK - Cita r52 Chang añadida")
    else:
        print("AVISO - No se encontró el punto de inserción para r52")

# Mapa de renumeración: (clave_antigua, ZZZclave_temporal)
REF_MAP = [
    ('r1',   'ZZZ1'),
    ('r2',   'ZZZ2'),
    ('r3',   'ZZZ3'),
    ('r4',   'ZZZ4'),
    ('r5',   'ZZZ5'),
    ('r6',   'ZZZ6'),
    ('r7',   'ZZZ7'),
    ('r8',   'ZZZ8'),
    ('r9',   'ZZZ9'),
    ('lustig2024_new', 'ZZZ10'),
    ('perez2023_esp32', 'ZZZ11'),
    ('marosan2024',    'ZZZ12'),
    ('idoyaga2023',    'ZZZ13'),
    ('invecom2025',    'ZZZ14'),
    ('r45',  'ZZZ15'),
    ('r11',  'ZZZ16'),
    ('r12',  'ZZZ17'),
    ('r13',  'ZZZ18'),
    ('r14',  'ZZZ19'),
    ('r15',  'ZZZ20'),
    ('r16',  'ZZZ21'),
    ('r17',  'ZZZ22'),
    ('r18',  'ZZZ23'),
    ('r19',  'ZZZ24'),
    ('r20',  'ZZZ25'),
    ('r21',  'ZZZ26'),
    ('r22',  'ZZZ27'),
    ('r23',  'ZZZ28'),
    ('r24',  'ZZZ29'),
    ('r25',  'ZZZ30'),
    ('r26',  'ZZZ31'),
    ('r27',  'ZZZ32'),
    ('r28',  'ZZZ33'),
    ('r29',  'ZZZ34'),
    ('r30',  'ZZZ35'),
    ('r31',  'ZZZ36'),
    ('r32',  'ZZZ37'),
    ('r33',  'ZZZ38'),
    ('r34',  'ZZZ39'),
    ('r35',  'ZZZ40'),
    ('r36',  'ZZZ41'),
    ('r37',  'ZZZ42'),
    ('r38',  'ZZZ43'),
    ('r39',  'ZZZ44'),
    ('r40',  'ZZZ45'),
    ('r41',  'ZZZ46'),
    ('r42',  'ZZZ47'),
    ('r10',  'ZZZ48'),
    ('r43',  'ZZZ49'),
    ('r44',  'ZZZ50'),
    ('acm2025_remote', 'ZZZ51'),
    ('chang2024_iot_physics', 'ZZZ52'),
    ('pmc2023_esp32', 'ZZZ53'),
    ('r46',  'ZZZ_DROP'),
    ('r47',  'ZZZ_DROP'),
    ('r48',  'ZZZ_DROP'),
    ('r49',  'ZZZ_DROP'),
    ('r50',  'ZZZ_DROP'),
    ('r51',  'ZZZ_DROP'),
    # r52 y r53 ya fueron añadidos a la bibliografía como chang y kaur
    ('r52',  'ZZZ52'),
    ('r53',  'ZZZ53'),
]

# Paso 1: Reemplazar claves antiguas por temporales (de más largo a más corto)
# Ordenar por longitud descendente para evitar que 'r1' afecte 'r11', 'r12', etc.
REF_MAP_sorted = sorted(REF_MAP, key=lambda x: len(x[0]), reverse=True)

for old_key, tmp_key in REF_MAP_sorted:
    # Solo reemplazar cuando el key está delimitado por {, }, ,, espacio
    pattern = r'(?<=[{,\s])' + re.escape(old_key) + r'(?=[},\s])'
    replacement = tmp_key
    tex = re.sub(pattern, replacement, tex)

print("OK - Paso 1: claves reemplazadas por temporales ZZZ")

# Paso 2: Reemplazar temporales ZZZ → r{N} final
for n in range(1, 54):
    tex = tex.replace(f'ZZZ{n}', f'r{n}')

# Eliminar referencias DROP (no deberían tener bibitem, pero limpiar citas huérfanas)
tex = re.sub(r'\\cite\{ZZZ_DROP(?:,ZZZ_DROP)*\}', '', tex)
tex = re.sub(r',\s*ZZZ_DROP', '', tex)
tex = re.sub(r'ZZZ_DROP,\s*', '', tex)
tex = re.sub(r'ZZZ_DROP', '', tex)
print("OK - Paso 2: numeración final r1-r53 aplicada")

# ════════════════════════════════════════════════
# BLOQUE 3: REEMPLAZAR SECCIÓN REFERENCES
# ════════════════════════════════════════════════

NEW_BIB = r"""\begin{thebibliography}{999}

\bibitem{r1}
Lahme, S.Z.; Klein, P.; Lehtinen, A.; M\"uller, A.; Pirinen, P.; Ron\v{c}evi\'c, L.; Su\v{s}ac, A.
Physics lab courses under digital transformation: A trinational survey among university lab instructors about the role of new digital technologies and learning objectives.
\textit{Phys. Rev. Phys. Educ. Res.} \textbf{2023}, \textit{19}, 020159.
\href{https://doi.org/10.1103/PhysRevPhysEducRes.19.020159}{https://doi.org/10.1103/PhysRevPhysEducRes.19.020159}.

\bibitem{r2}
Viswanadh, K.S.; Gureja, A.; Walchatwar, N.; Agrawal, R.; Sinha, S.; Chaudhari, S.; Vaidhyanathan, K.; Hussain, A.M.
Engineering End-to-End Remote Labs Using IoT-Based Retrofitting.
\textit{IEEE Access} \textbf{2024}, \textit{PP}, 1--1.
\href{https://doi.org/10.1109/ACCESS.2024.3523066}{https://doi.org/10.1109/ACCESS.2024.3523066}.

\bibitem{r3}
Fuertes, J.J.; Mart\'inez, J.M.; Dormido, S.; Vargas, H.; S\'anchez, J.; Duro, N.
Virtual and Remote Laboratory of a DC Motor for Learning Control Theory.
\textit{Int. J. Eng. Educ.} \textbf{2011}, \textit{27}, 1--12.

\bibitem{r4}
Guerrero-Osuna, H.A.; Garc\'ia-V\'azquez, F.A.; Ibarra-Delgado, S.; Sol\'is-S\'anchez, L.O.
Developing a Cloud and IoT-Integrated Remote Laboratory to Enhance Education 4.0: An Approach for FPGA-Based Motor Control.
\textit{Appl. Sci.} \textbf{2024}, \textit{14}, 10115.

\bibitem{r5}
Lustig, F.; Kuri\v{s}\v{c}\'ak, P.; Brom, P.; Dvo\v{r}\'ak, J.
Open Modular Hardware and Software Kit for Creations of Remote Experiments Accessible from PC and Mobile Devices.
\textit{Int. J. Online Eng. (iJOE)} \textbf{2016}, \textit{12}, 30--36.
\href{https://doi.org/10.3991/ijoe.v12i07.5833}{https://doi.org/10.3991/ijoe.v12i07.5833}.

\bibitem{r6}
Zhao, Y.
Smartphone-Based Undergraduate Physics Labs: A Comprehensive Review.
\textit{IEEE Access} \textbf{2024}, \textit{13}, 1106--1132.
\href{https://doi.org/10.1109/ACCESS.2024.3523066}{https://doi.org/10.1109/ACCESS.2024.3523066}.

\bibitem{r7}
Dizdarevic, J.; Jukan, A.
Engineering an IoT--Edge--Cloud Computing System Architecture: Lessons Learnt from an Undergraduate Laboratory Course.
\textit{IoT} \textbf{2022}, \textit{3}, 145--163.
\href{https://doi.org/10.3390/iot3010010}{https://doi.org/10.3390/iot3010010}.

\bibitem{r8}
Azad, A.K.M.
Use of Internet of Things for Remote Laboratory Settings.
\textit{IoT} \textbf{2021}, \textit{2}, 203--232.
\href{https://doi.org/10.3390/iot2020011}{https://doi.org/10.3390/iot2020011}.

\bibitem{r9}
Palmer, C.; Roullier, B.; Aamir, M.; McQuade, F.; Stella, L.; Anjum, A.
Digital Twinning Remote Laboratories for Online Practical Learning.
\textit{Sensors} \textbf{2022}, \textit{22}, 2351.
\href{https://doi.org/10.3390/s22062351}{https://doi.org/10.3390/s22062351}.

\bibitem{r10}
Lustig, A.; Biard, V. \textit{et al.}
Engineering End-to-End Remote Labs using IoT-based Retrofitting.
\textit{arXiv} \textbf{2024}, arXiv:2402.05466.
Available online: \url{https://arxiv.org/abs/2402.05466} (accessed on 5 December 2025).

\bibitem{r11}
P\'erez-Cham\'e, J.H. \textit{et al.}
Development of an educational low-cost and ESP32-based platform for fundamental physics experiments.
\textit{Comput. Appl. Eng. Educ.} \textbf{2023}.
\href{https://doi.org/10.1002/cae.22674}{https://doi.org/10.1002/cae.22674}.

\bibitem{r12}
Marosan, A. \textit{et al.}
Real-time data acquisition with ESP32 for IoT applications in educational environments.
\textit{Int. Conf. Appl. Math. Sci. (ICMAS)} \textbf{2024}, \textit{19}(2), 61--68.
Available online: \url{http://www.icmas.eu/Journal_archive_files/Vol_19-Issue2_2024_PDF/61-68_MAROSAN.pdf} (accessed on 5 December 2025).

\bibitem{r13}
Idoyaga, I. \textit{et al.}
The Use of Remote Laboratories in University Physics: Challenges and Opportunities in Latin America.
In \textit{Proceedings of the Symposium ICASE-MIDEC GIREP 2023}.
Available online: \url{https://indico.cern.ch/event/1175859/} (accessed on 5 December 2025).

\bibitem{r14}
Vera, M. \textit{et al.}
An\'alisis comparativo de la ense\~nanza de la f\'isica en universidades latinoamericanas durante la pandemia COVID-19.
\textit{Rev. Invecom} \textbf{2025}.
Available online: \url{https://revistainvecom.org/index.php/invecom/article/view/4234} (accessed on 5 December 2025).

\bibitem{r15}
Sosa Mej\'ia, W.S.
\textit{RemotePhysicsLab: Prototipo de laboratorio de f\'isica h\'ibrido basado en IoT}.
Repositorio GitHub.
Available online: \url{https://github.com/waltersosa/RemotePhysicsLab.git} (accessed on 5 December 2025).

\bibitem{r16}
Hevner, A.R.; March, S.T.; Park, J.; Ram, S.
Design Science in Information Systems Research.
\textit{MIS Q.} \textbf{2004}, \textit{28}, 75--105.

\bibitem{r17}
ISO/IEC.
\textit{ISO/IEC 15288:2015 Systems and Software Engineering---System Life Cycle Processes};
International Organization for Standardization: Geneva, Switzerland, 2015.

\bibitem{r18}
Mattel, Inc.
\textit{Hot Wheels Track Sets}.
Available online: \url{https://shop.mattel.com/pages/hot-wheels} (accessed on 5 December 2025).

\bibitem{r19}
Mattel, Inc.
\textit{Hot Wheels Cars}.
Available online: \url{https://shop.mattel.com/collections/hot-wheels-cars} (accessed on 5 December 2025).

\bibitem{r20}
Vishay Intertechnology, Inc.
\textit{TCRT5000 Reflective Optical Sensor}.
Available online: \url{https://www.vishay.com/docs/83751/tcrt5000.pdf} (accessed on 5 December 2025).

\bibitem{r21}
Espressif Systems.
\textit{ESP32-WROOM-32 Datasheet}.
Available online: \url{https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32_datasheet_en.pdf} (accessed on 5 December 2025).

\bibitem{r22}
Thingiverse.
\textit{Mechanical Support for Track-Based Experiments} (Thing 3630616).
Available online: \url{https://www.thingiverse.com/thing:3630616} (accessed on 5 December 2025).

\bibitem{r23}
Thingiverse.
\textit{3D Printed Modular Track Components} (Thing 3485484).
Available online: \url{https://www.thingiverse.com/thing:3485484} (accessed on 5 December 2025).

\bibitem{r24}
Thingiverse.
\textit{3D Printed Structural Reinforcement Parts} (Thing 4381935).
Available online: \url{https://www.thingiverse.com/thing:4381935} (accessed on 5 December 2025).

\bibitem{r25}
Thingiverse.
\textit{3D Printed Mechanical Pusher Mechanism} (Thing 2806324).
Available online: \url{https://www.thingiverse.com/thing:2806324} (accessed on 5 December 2025).

\bibitem{r26}
Tower Pro.
\textit{SG90 Micro Servo Motor Datasheet}.
Available online: \url{http://www.ee.ic.ac.uk/pjs99/projects/servo/sg90_datasheet.pdf} (accessed on 5 December 2025).

\bibitem{r27}
Stepperonline.
\textit{NEMA 17 Stepper Motor Bipolar Datasheet}.
Available online: \url{https://www.omc-stepperonline.com/download/17HS19-2004S1.pdf} (accessed on 5 December 2025).

\bibitem{r28}
STMicroelectronics.
\textit{L298N Dual H-Bridge Motor Driver Datasheet}.
Available online: \url{https://www.st.com/resource/en/datasheet/l298.pdf} (accessed on 5 December 2025).

\bibitem{r29}
Generic Electronics Suppliers.
\textit{LCD 20x4 Display with I2C Interface Datasheet}.
Available online: \url{https://www.sparkfun.com/datasheets/LCD/HD44780.pdf} (accessed on 5 December 2025).

\bibitem{r30}
Generic Electronics Suppliers.
\textit{Tactile Push Button Switch for Breadboard}.
Available online: \url{https://www.adafruit.com/product/367} (accessed on 5 December 2025).

\bibitem{r31}
USB Implementers Forum.
\textit{USB Type-C Cable Specification}.
Available online: \url{https://www.usb.org/sites/default/files/USB\%20Type-C\%20Spec\%20R2.0\%20-\%20August\%202019.pdf} (accessed on 5 December 2025).

\bibitem{r32}
IEEE.
\textit{IEEE Standard for Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications}.
Available online: \url{https://ieeexplore.ieee.org/document/9363693} (accessed on 5 December 2025).

\bibitem{r33}
Generic Electronics Suppliers.
\textit{Dupont Jumper Wires (Male-Female and Female-Female)}.
Available online: \url{https://www.adafruit.com/category/289} (accessed on 5 December 2025).

\bibitem{r34}
Generic Electronics Suppliers.
\textit{Plastic Project Enclosure Box (135x75x40 mm)}.
Available online: \url{https://www.digikey.com/en/products/filter/enclosures/287} (accessed on 5 December 2025).

\bibitem{r35}
Generic Electronics Suppliers.
\textit{AC-DC Power Adapter 12V/1A}.
Available online: \url{https://www.digikey.com/en/products/filter/power-supplies-external-internal-off-board/171} (accessed on 5 December 2025).

\bibitem{r36}
Insta360.
\textit{Insta360 Link---4K AI Webcam Technical Specifications}.
Available online: \url{https://onlinemanual.insta360.com/link/en-us/introduction} (accessed on 5 December 2025).

\bibitem{r37}
Raspberry Pi Ltd.
\textit{Raspberry Pi 4 Model B Product Brief}.
Available online: \url{https://datasheets.raspberrypi.com/rpi4/raspberry-pi-4-product-brief.pdf} (accessed on 5 December 2025).

\bibitem{r38}
EMQ Technologies Co., Ltd.
\textit{EMQX---MQTT Platform for IoT Data Streaming Documentation}.
Available online: \url{https://docs.emqx.com/en/emqx/v5.0/} (accessed on 5 December 2025).

\bibitem{r39}
EMQ Technologies Co., Ltd.
\textit{MQTTX: Your All-in-One MQTT Client Toolbox Documentation}.
Available online: \url{https://mqttx.app/docs} (accessed on 5 December 2025).

\bibitem{r40}
OpenJS Foundation.
\textit{Node.js API Documentation}.
Available online: \url{https://nodejs.org/api/} (accessed on 5 December 2025).

\bibitem{r41}
OpenJS Foundation.
\textit{Express API Reference}.
Available online: \url{https://expressjs.com/en/4x/api.html} (accessed on 5 December 2025).

\bibitem{r42}
MongoDB, Inc.
\textit{MongoDB Documentation}.
Available online: \url{https://www.mongodb.com/docs/manual/} (accessed on 5 December 2025).

\bibitem{r43}
Mongoose.
\textit{Mongoose ODM API Documentation}.
Available online: \url{https://mongoosejs.com/docs/api.html} (accessed on 5 December 2025).

\bibitem{r44}
Vercel, Inc.
\textit{Next.js Documentation}.
Available online: \url{https://nextjs.org/docs} (accessed on 5 December 2025).

\bibitem{r45}
Meta Platforms, Inc.
\textit{React Reference Documentation}.
Available online: \url{https://react.dev/reference/react} (accessed on 5 December 2025).

\bibitem{r46}
Arduino AG.
\textit{Arduino IDE 2.x Documentation}.
Available online: \url{https://www.arduino.cc/en/software} (accessed on 5 December 2025).

\bibitem{r47}
Python Software Foundation.
\textit{Python 3 Documentation}.
Available online: \url{https://docs.python.org/3/} (accessed on 5 December 2025).

\bibitem{r48}
Atzori, L.; Iera, A.; Morabito, G.
The Internet of Things: A survey.
\textit{Comput. Netw.} \textbf{2010}, \textit{54}, 2787--2805.
\href{https://doi.org/10.1016/j.comnet.2010.05.010}{https://doi.org/10.1016/j.comnet.2010.05.010}.

\bibitem{r49}
Eraser Labs, Inc.
\textit{Eraser---AI Co-Pilot for Technical Design and Documentation}.
Available online: \url{https://www.eraser.io} (accessed on 5 December 2025).

\bibitem{r50}
OpenAI. \textit{ChatGPT}.
Available online: \url{https://chat.openai.com} (accessed on 23 January 2026). Content generated with the assistance of ChatGPT.

\bibitem{r51}
Hern\'andez, R. \textit{et al.}
Remote Laboratory for developing IoT systems in engineering education.
In \textit{Proceedings of the ACM Technical Symposium on Computer Science Education}; ACM: New York, NY, USA, \textbf{2025}.
\href{https://doi.org/10.1145/3716554.3716602}{https://doi.org/10.1145/3716554.3716602}.

\bibitem{r52}
Chang, H.Y. \textit{et al.}
Deploying an IoT-based remote physics lab platform to support undergraduate mechanics education.
\textit{Phys. Educ.} \textbf{2024}, \textit{59}, 065012.

\bibitem{r53}
Kaur, G. \textit{et al.}
Design and Implementation of ESP32-Based IoT Devices for Real-Time Monitoring Applications.
\textit{Sensors} \textbf{2023}, \textit{23}, 6437.
\href{https://doi.org/10.3390/s23156437}{https://doi.org/10.3390/s23156437}.

\end{thebibliography}"""

bib_pat = r'\\begin\{thebibliography\}\{999\}.*?\\end\{thebibliography\}'
new_tex, n = re.subn(bib_pat, lambda m: NEW_BIB, tex, count=1, flags=re.DOTALL)
if n:
    tex = new_tex
    print("OK - Sección References reemplazada (53 entradas)")
else:
    print("AVISO - No se encontró bloque thebibliography")

# ════════════════════════════════════════════════
# GUARDAR
# ════════════════════════════════════════════════
with open(SRC, 'w', encoding='utf-8') as f:
    f.write(tex)
print("DONE - template.tex guardado correctamente.")
