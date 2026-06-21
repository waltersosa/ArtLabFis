$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$source = Join-Path $root 'Ingenuis\articulo_ingenius.tex'
$target = Join-Path $PSScriptRoot 'articulo_espol.tex'
$bibSource = Join-Path $root 'Ingenuis\referencias_articulo.bib'
$bibTarget = Join-Path $PSScriptRoot 'referencias_espol.bib'

$text = Get-Content -Raw -Encoding UTF8 $source
$start = $text.IndexOf('\section{Introducci')
$end = $text.IndexOf('\bibliography{referencias_articulo.bib}')
if ($start -lt 0 -or $end -lt 0) {
    throw 'No se pudo localizar el cuerpo del manuscrito fuente.'
}

$body = $text.Substring($start, $end - $start)
$body = $body -replace '\\cite\{', '\parencite{'
$body = $body -replace '\\begin\{table\*\}\[t\]', '\begin{table}[H]'
$body = $body -replace '\\end\{table\*\}', '\end{table}'
$body = $body -replace '\\begin\{figure\}\[H\]', '\begin{figure}[htbp]'
$body = $body -replace '\\begin\{table\}\[H\]', '\begin{table}[htbp]'
$body = $body -replace '\\includegraphics\[width=\\linewidth\]', '\includegraphics[width=0.88\textwidth]'
$body = $body -replace '\\includegraphics\[width=0\.88\\textwidth\]\{figures/', '\includegraphics[width=0.88\textwidth]{../figures/'
$body = $body -replace '\\section\*\{Agradecimientos\}', "\section{Reconocimientos y declaraciones}`r`n`r`n\subsection{Agradecimientos}"

$figurePattern = '(?m)^(\s*\\includegraphics[^\r\n]+)\r?\n(\s*\\caption[^\r\n]+)\r?\n(\s*\\label[^\r\n]+)'
$body = [regex]::Replace($body, $figurePattern, {
    param($match)
    $match.Groups[2].Value + "`r`n" +
    $match.Groups[3].Value + "`r`n" +
    $match.Groups[1].Value
})

$body = $body.Replace('Lahme \textit{et al.}~\parencite{r1}', '\textcite{r1}')
$body = $body.Replace('Guerrero-Osuna \textit{et al.}~\parencite{r4}', '\textcite{r4}')
$body = $body.Replace('Fuertes \textit{et al.}~\parencite{r3}', '\textcite{r3}')
$body = $body.Replace('Viswanadh \textit{et al.}~\parencite{r2}', '\textcite{r2}')
$body = $body.Replace('Lustig \textit{et al.}~\parencite{r5}', '\textcite{r5}')
$body = $body.Replace('Zhao~\parencite{r6}', '\textcite{r6}')
$body = $body.Replace('Dizdarevic y Jukan~\parencite{r7}', '\textcite{r7}')
$body = $body.Replace('Azad~\parencite{r8}', '\textcite{r8}')
$body = $body.Replace('Palmer \textit{et al.}~\parencite{r9}', '\textcite{r9}')
$body = $body.Replace('Lustig \textit{et al.}~\parencite{r10}', '\textcite{r10}')
$body = $body.Replace("P\'erez-Cham\'e \textit{et al.}~\parencite{r11}", '\textcite{r11}')
$body = $body.Replace('Marosan \textit{et al.}~\parencite{r12}', '\textcite{r12}')
$body = $body.Replace('Chang \textit{et al.}~\parencite{r52}', '\textcite{r52}')
$body = $body.Replace("Hern\'andez \textit{et al.}~\parencite{r51}", '\textcite{r51}')
$body = $body.Replace('Lustig~\parencite{r10}', 'Lustig et al. (2024)')
$body = $body.Replace("P\'erez-Cham\'e~\parencite{r11}", "P\'erez-Cham\'e et al. (2023)")
$body = $body.Replace('Guerrero-O.~\parencite{r4}', 'Guerrero-Osuna et al. (2024)')
$body = $body.Replace('Viswanadh~\parencite{r2}', 'Viswanadh et al. (2024)')
$body = $body.Replace('Fuertes~\parencite{r3}', 'Fuertes et al. (2011)')
$body = $body.Replace("\textbf{Pregunta de investigaci\'on:}", "Pregunta de investigaci\'on:")
$body = $body.Replace("\textbf{objetivo general}", "objetivo general")
$body = $body.Replace("\textbf{contribuciones}", "contribuciones")
$body = $body.Replace("\textbf{sistema experimental mec\'anico}", "sistema experimental mec\'anico")
$body = $body.Replace("\textbf{sistema de sensado y adquisici\'on de datos}", "sistema de sensado y adquisici\'on de datos")
$body = $body.Replace("\textbf{unidad de control y procesamiento IoT}", "unidad de control y procesamiento IoT")
$body = $body.Replace("\textbf{estructura mec\'anica}", "estructura mec\'anica")
$body = $body.Replace("\textbf{actuadores}", "actuadores")
$body = $body.Replace("\textbf{interfaz de usuario local}", "interfaz de usuario local")
$body = $body.Replace("\textbf{comunicaci\'on y conectividad}", "comunicaci\'on y conectividad")
$body = $body.Replace("\textbf{fuente de alimentaci\'on}", "fuente de alimentaci\'on")
$body = $body.Replace("\textbf{sistema de visualizaci\'on remota}", "sistema de visualizaci\'on remota")
$body = $body.Replace("\textbf{servidor}", "servidor")
$body = $body.Replace("\textbf{antes}", "antes")
$stabilityCaption = '\caption{Tasa de captura exitosa de eventos: remoto (98,5\%) vs. presencial (100,0\%).}'
$captionIndex = $body.IndexOf($stabilityCaption)
if ($captionIndex -ge 0) {
    $figureStart = $body.LastIndexOf('\begin{figure}[htbp]', $captionIndex)
    if ($figureStart -ge 0) {
        $body = $body.Remove($figureStart, '\begin{figure}[htbp]'.Length).Insert($figureStart, '\begin{figure}[H]')
    }
}
$body = $body.Replace(
    '\includegraphics[width=0.88\textwidth]{../figures/stability_success_rate.png}',
    '\includegraphics[width=0.70\textwidth]{../figures/stability_success_rate.png}'
)
$body = $body.Replace(
    '\begin{tabular}{p{2.0cm}p{1.3cm}p{1.5cm}p{1.8cm}p{0.8cm}p{0.8cm}p{0.6cm}p{0.6cm}p{3.0cm}}',
    "\setlength{\tabcolsep}{2pt}`r`n\begin{tabular}{p{2.3cm}p{1.4cm}p{1.7cm}p{1.5cm}p{0.8cm}p{1.0cm}p{0.9cm}p{1.0cm}p{2.4cm}}"
)

$preamble = @'
\documentclass{espol-rte}

\usepackage[backend=biber,style=apa,sortcites=true,sorting=nyt]{biblatex}
\DeclareLanguageMapping{spanish}{spanish-apa}
\addbibresource{referencias_espol.bib}
\graphicspath{{../figures/}}

\renewcommand{\RTEtituloES}{Retrofitting IoT de un laboratorio remoto de cinem\'atica}
\renewcommand{\RTEtituloEN}{IoT Retrofitting of a Remote Kinematics Laboratory}
\renewcommand{\RTEautores}{%
  Walter Santiago Sosa Mej\'ia\textsuperscript{1}\,
  \href{https://orcid.org/0009-0003-6240-3462}{ORCID};
  Manuel Rogelio Nev\'arez Toledo\textsuperscript{1,*}\,
  \href{https://orcid.org/0000-0001-5628-3351}{ORCID}}
\renewcommand{\RTEafiliaciones}{%
  \textsuperscript{1}Pontificia Universidad Cat\'olica del Ecuador,
  Sede Esmeraldas, Esmeraldas, Ecuador\\
  wssosa@pucese.edu.ec; manuel.nevarez@pucese.edu.ec\\
  *Autor de correspondencia: manuel.nevarez@pucese.edu.ec}

\begin{document}
\makertetitle

\begin{resumenespol}
La modernizaci\'on de los laboratorios de f\'isica en contextos de recursos limitados presenta desaf\'ios significativos para la educaci\'on superior en Am\'erica Latina. Este art\'iculo presenta el dise\~no, implementaci\'on y validaci\'on t\'ecnica de un prototipo de laboratorio remoto de cinem\'atica para el estudio del Movimiento Rectil\'ineo Uniformemente Acelerado (MRUA), basado en una estrategia de \textit{retrofitting} mediante tecnolog\'ias de Internet de las Cosas (IoT) sobre equipamiento preexistente de bajo costo. La arquitectura integra un microcontrolador ESP32 como nodo Edge computing, cuatro sensores infrarrojos, un broker MQTT en Raspberry Pi~4 y una interfaz web en Next.js/React. Se realizaron 70 ensayos independientes (35 remotos y 35 presenciales). Los resultados demuestran que el prototipo remoto alcanza precisi\'on cinem\'atica comparable al montaje tradicional: diferencias medias inferiores a 0,01~s, desviaciones est\'andar que difieren en menos de 0,02~s y una aceleraci\'on experimental media id\'entica en ambas modalidades ($\mu \approx 0{,}95$~m/s$^2$). La tasa de captura exitosa alcanz\'o el 98,5\% en modo remoto. Se concluye que el \textit{retrofitting} IoT es una soluci\'on viable, escalable y de bajo costo para democratizar el acceso a educaci\'on experimental en entornos h\'ibridos.
\palabrasclave{Edge computing, instrumentaci\'on de bajo costo, Internet de las Cosas, laboratorios remotos, MRUA, retrofitting.}
\end{resumenespol}

\begin{abstractespol}
The modernization of physics laboratories in resource-limited contexts presents significant challenges for higher education in Latin America. This article presents the design, implementation, and technical validation of a remote kinematics laboratory prototype for the study of Uniformly Accelerated Rectilinear Motion (UARM), based on a \textit{retrofitting} strategy using Internet of Things (IoT) technologies on pre-existing low-cost equipment. The architecture integrates an ESP32 microcontroller as an Edge computing node, four infrared sensors, an MQTT broker on Raspberry Pi~4, and a web interface in Next.js/React. To validate the system, 70 independent trials were conducted (35 remote and 35 in-person). The results demonstrate that the remote prototype achieves kinematic precision comparable to the traditional setup: mean differences below 0.01~s, standard deviations differing by less than 0.02~s, and an identical mean experimental acceleration in both modalities ($\mu \approx 0.95$~m/s$^2$). The successful event capture rate reached 98.5\% in remote mode. The IoT \textit{retrofitting} methodology is therefore a viable, scalable, and low-cost solution for expanding access to experimental education in hybrid environments.
\keywordsespol{Edge computing, Internet of Things, low-cost instrumentation, remote laboratories, retrofitting, UARM.}
\end{abstractespol}

'@

$declarations = @'

\subsection{Contribuciones de autor\'ia}
Conceptualizaci\'on, W.S.S.M. y M.R.N.T.; metodolog\'ia, W.S.S.M. y M.R.N.T.; software, W.S.S.M.; validaci\'on, W.S.S.M. y M.R.N.T.; an\'alisis formal, W.S.S.M.; investigaci\'on, W.S.S.M.; recursos, M.R.N.T.; curaci\'on de datos, W.S.S.M.; redacci\'on del borrador original, W.S.S.M.; revisi\'on y edici\'on, W.S.S.M. y M.R.N.T.; visualizaci\'on, W.S.S.M.; supervisi\'on, M.R.N.T.; administraci\'on del proyecto, M.R.N.T. Todos los autores han le\'ido y aprobado la versi\'on final del manuscrito.

\subsection{Declaraci\'on sobre el uso de inteligencia artificial}
Los autores declaran que, durante la elaboraci\'on del art\'iculo, se utiliz\'o ChatGPT de OpenAI como apoyo para la elaboraci\'on de diagramas y la revisi\'on de redacci\'on, y Gemini de Google para la generaci\'on de im\'agenes. Los autores verificaron y asumieron la responsabilidad del contenido final.

\subsection{Conflictos de inter\'es}
Los autores declaran que no existen conflictos de inter\'es.

\printbibliography[title={Referencias}]
\end{document}
'@

$body = $body.TrimEnd()
$body = $body -replace '\\end\{multicols\}', ''
$body = $body -replace '\\end\{document\}', ''

Set-Content -Encoding UTF8 $target ($preamble + $body + $declarations)
Copy-Item -LiteralPath $bibSource -Destination $bibTarget -Force
Write-Host "Generado: $target"
Write-Host "Generado: $bibTarget"
