\typeout{Beamer  class for talks with F4 style <2017-07-19> Frauke Sprengel}
\NeedsTeXFormat{LaTeX2e}

\ProvidesClass{f4_beamer}[2017/07/19  beamer class F4 style]

\RequirePackage{ifthen}
\RequirePackage{etex} 
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage{lmodern} 
\RequirePackage{amssymb}
\RequirePackage{amsmath}
\RequirePackage{graphicx}

%\RequirePackage{url,hyperref}

 \DeclareOption{ngerman}{%
 \PassOptionsToPackage{\CurrentOption}{babel}
 }
 
 \DeclareOption{english}{%
 \PassOptionsToPackage{\CurrentOption}{babel}
}

\ExecuteOptions{ngerman}
\ProcessOptions

\LoadClass[german,compress,hyperref={pdfpagelabels=false},unknownkeysallowed]{beamer}
\RequirePackage{babel}
\RequirePackage{geometry}
\geometry{paperwidth=16cm,paperheight=9cm}


\newcommand{\zsp}{\rule{0pt}{0pt}}  % zero space


\mode<presentation>{%
\hypersetup{pdffitwindow=true,pdfpagelayout=SinglePage,%pdfpagemode=FullScreen,
breaklinks=true,urlcolor=Blue}
\usetheme{default}
\useinnertheme[shadow=true]{rounded}
\usecolortheme{orchid}
\setbeamercovered{invisible}
\setbeamertemplate{theorems}[numbered]
\setbeamertemplate{captions}[numbered]
\setbeamertemplate{bibliography item}[book]
\usefonttheme{professionalfonts}
 \raggedright
\setbeamertemplate{items}[circle]
%\setbeamertemplate{itemize items}[ball]
\setbeamertemplate{bibliography item}[book]

\titlegraphic{\includegraphics[width=0.15\textwidth]{images/Wortmarke_WI_schwarz.pdf}}

\defbeamertemplate*{title page}{customized}[1][]
{ \inserttitlegraphic\par\vfill\vfill
  \usebeamerfont{title}{\bfseries \inserttitle}\par
  \usebeamerfont{subtitle}%\usebeamercolor[fg]{subtitle}
  {\slshape \insertsubtitle}\par  \bigskip
  \usebeamerfont{author}{\footnotesize\insertauthor\par
  \usebeamerfont{date}\insertdate\par}\vspace*{-1cm}
  %\usebeamerfont{institute}\insertinstitute\par
}

  \AtBeginDocument{%
    \setcounter{framenumber}{0}
{\setbeamertemplate{footline}{}
  \setbeamertemplate{sidebar right}{~ \vfill\par
\mbox{}\hspace{-2cm}
\includegraphics[width=3cm]{images/H_WI_Pantone1665.pdf}}

\maketitle }
  }

\AtBeginSection[]
{
  \begin{frame}<beamer>
    \tableofcontents[currentsection,hideothersubsections]
  \end{frame}
}
  
  % Frame layout
  \pgfdeclareimage[height=1.7cm]{fhh-logo}{images/H_WI_Pantone1665.pdf}
  \logo{\pgfuseimage{fhh-logo}}  
\definecolor{structureBlue}{rgb}{0.862745098, 0.235294118, 0.019607843}
\renewcommand{\alert}[1]{{\textcolor{structureBlue}{#1}}}
  \setbeamertemplate{navigation symbols}{%
    \insertslidenavigationsymbol{}
    \insertframenavigationsymbol{}
    \insertbackfindforwardnavigationsymbol{}%
  }

  \setbeamertemplate{sidebar left}{}
  \setbeamertemplate{footline}{%
 
    \zsp\hspace{0.1cm}%
	\parbox{0.95\textwidth}{{\fontsize{6}{8}
	\mbox{~}\textcolor{structureBlue}{\hrulefill}\mbox{} \\

	\mbox{~}{\bfseries Hochschule Hannover}, Fak. IV, \insertshortauthor{}, \insertshorttitle{}, 
	 \insertshortsubtitle{}, \insertdate{} \hfill \insertframenumber{}
	\vspace*{4pt}
	}}
%    \parbox{4cm}{%
      %\insertlogo{}%
%      \vskip2pt%
%    }%
%    \hfill
%    \parbox{4cm}{%
%      \centering\fontsize{6}{8}%
%      \textcolor{lightgray}{\insertshorttitle{}}\\[2pt]
%      \textcolor{lightgray}{\insertshortauthor{} -- \insertdate{}}%
%      \vspace*{2pt}%
%    }
%    \hfill
%    \parbox{4cm}{%
%      \raggedleft\fontsize{6}{8}%
%      \textcolor{lightgray}{\insertlecture{} --  \insertsectionhead{} --
%      \insertframenumber{}}\\ \usebeamertemplate***{navigation symbols}%
%      \vspace*{2pt}%
%    }
    \hspace{0.1cm}\zsp
  }

\setbeamersize{sidebar width right=1.5cm}
 \setbeamertemplate{sidebar right}{~ \vfill \insertlogo \vspace*{10pt} 

	~}

\setbeamercolor{structure}{fg=structureBlue!70!black}
}
