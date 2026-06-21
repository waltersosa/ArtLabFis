\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{espol-rte}[2026/06/06 RTE ESPOL article format]

\LoadClass[12pt,a4paper]{article}

\RequirePackage{fontspec}
\setmainfont{Times New Roman}
\setsansfont{Arial}
\RequirePackage[spanish,es-nodecimaldot,english]{babel}
\RequirePackage{csquotes}
\RequirePackage{geometry}
\geometry{a4paper,top=0.75in,bottom=1in,left=1in,right=1in}
\RequirePackage{setspace}
\setstretch{1.0}
\RequirePackage{indentfirst}
\setlength{\parindent}{0.5in}
\setlength{\parskip}{0pt}
\RequirePackage{microtype}
\RequirePackage{graphicx}
\RequirePackage{float}
\RequirePackage{booktabs}
\RequirePackage{array}
\RequirePackage{multirow}
\RequirePackage{amsmath,amssymb,bm}
\RequirePackage{textcomp}
\RequirePackage{xcolor}
\RequirePackage{enumitem}
\setlist{nosep,leftmargin=0.5in}
\RequirePackage{caption}
\DeclareCaptionLabelFormat{espol}{\textbf{#1~#2}}
\DeclareCaptionFormat{espol}{\centering#1\par\textit{#3}}
\captionsetup{
  format=espol,
  labelformat=espol,
  labelsep=none,
  justification=centering,
  singlelinecheck=false,
  position=top,
  font={normalsize},
  skip=6pt
}
\captionsetup[figure]{name=Figura}
\captionsetup[table]{name=Tabla}
\RequirePackage{titlesec}
\titleformat{\section}
  {\normalfont\bfseries\centering\fontsize{12}{14}\selectfont}
  {}{0pt}{}
\titlespacing*{\section}{0pt}{12pt}{6pt}
\titleformat{\subsection}
  {\normalfont\bfseries\fontsize{12}{14}\selectfont}
  {}{0pt}{}
\titlespacing*{\subsection}{0pt}{10pt}{4pt}
\titleformat{\subsubsection}
  {\normalfont\itshape\fontsize{12}{14}\selectfont}
  {}{0pt}{}
\titlespacing*{\subsubsection}{0pt}{8pt}{4pt}
\titleformat{\paragraph}[runin]
  {\normalfont\itshape\fontsize{12}{14}\selectfont}
  {}{0pt}{}[.]
\RequirePackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\footnotesize Revista Tecnológica ESPOL -- RTE}
\fancyhead[R]{\footnotesize\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\setlength{\headheight}{15pt}
\RequirePackage[hidelinks]{hyperref}
\urlstyle{same}

\newcommand{\RTEdoi}{www.doi.org/10.37785/revista.vXnX.X}
\newcommand{\RTEtipo}{Artículos originales}
\newcommand{\RTEtituloES}{}
\newcommand{\RTEtituloEN}{}
\newcommand{\RTEautores}{}
\newcommand{\RTEafiliaciones}{}
\newcommand{\RTEfechas}{%
  Enviado: año/mes/día\quad
  Aceptado: año/mes/día\quad
  Publicado: año/mes/día}

\newcommand{\makertetitle}{%
  \thispagestyle{fancy}
  \begin{center}
    {\footnotesize\RTEdoi\par}
    \vspace{3pt}
    {\small\bfseries\RTEtipo\par}
    \vspace{6pt}
    {\fontsize{16}{19}\selectfont\bfseries\RTEtituloES\par}
    \vspace{4pt}
    {\fontsize{16}{19}\selectfont\bfseries\RTEtituloEN\par}
    \vspace{6pt}
    {\normalsize\bfseries\RTEautores\par}
    \vspace{4pt}
    {\normalsize\RTEafiliaciones\par}
    \vspace{4pt}
    {\footnotesize\RTEfechas\par}
  \end{center}
  \vspace{2pt}
}

\newenvironment{resumenespol}
  {\section*{Resumen}\noindent}
  {\par}

\newenvironment{abstractespol}
  {\section*{Abstract}\noindent\begin{otherlanguage}{english}}
  {\end{otherlanguage}\par}

\newcommand{\palabrasclave}[1]{%
  \par\smallskip\noindent\textbf{Palabras clave:} #1\par}
\newcommand{\keywordsespol}[1]{%
  \par\smallskip\noindent\textbf{Keywords:} #1\par}

\AtBeginDocument{%
  \selectlanguage{spanish}
  \renewcommand{\refname}{Referencias}
  \renewcommand{\figurename}{Figura}
  \renewcommand{\tablename}{Tabla}
}
