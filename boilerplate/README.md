# README för vår receptsamling

Eftersom vi fick en lysande idé att samla lite olika recept i TeX-format så tog jag på mig uppgiften att sätta upp ett TeX-projekt som vi kan använda. För en kort instruktion för hur man gör för att lägga till recept, se nedan.

## Projektets struktur
För att slippa ha en stor och lång fil som man måste ändra i har jag försökt strukturera upp projektet i kategorier (TeX-Chapters) som alla motsvarar olika kategorier av mat, exempelvis bröd eller soppor. I varje kategori finns plats för underkategorier (sections) som motsvarar t. ex. olika sorters bröd. I dessa underkategorier ligger sedan recepten, och varje recept ska sparas i en egen fil. Bilder på maträtterna ska ligga i mappen _figs_ som ska skapas då en ny underkategori skapas.

Som ett exempel så har projektet (i den andra kommitten) följande struktur

	├── Broed
	│   ├── 00-Index.tex
	│   ├── Fikabroed
	│   │   ├── 00-Index.tex
	│   │   ├── CthulhuBullar.tex
	│   │   └── figs
	│   │       └── CthulhuBullar.jpg
	│   ├── Fruktbroed
	│   │   ├── 00-Index.tex
	│   │   ├── SamisktRonnbarsbrod.tex
	│   │   └── figs
	│   ├── Okategoriserat
	│   │   ├── 00-Index.tex
	│   │   └── figs
	│   └── Surdegsbroed
	│       ├── 00-Index.tex
	│       └── figs
	├── Soppor
	│   ├── 00-Index.tex
	│   └── Cremesoppor
	│       ├── 00-Index.tex
	│       ├── Pumpasoppa.tex
	│       └── figs
	├── COOKBOOKCOMMANDS.sty
	├── HYPHENATION.sty
	├── PREAMBLE.sty
	├── ReceptTemplate.tex
	├── Receptsamling.teX
	└── Titlepage.tex

Filerna _00-Index.tex_ innehåller referenser till de filer som ska inkluderas i kategorin. Till exempel ser filen _./Broed/00-Index.tex_ som definierar kapitlet "Bröd" ut såhär:

	\chapter{Bröd}
	\input{./Broed/Fruktbroed/00-Index.tex} \clearpage
	\input{./Broed/Surdegsbroed/00-Index.tex} \clearpage
	\input{./Broed/Fikabroed/00-Index.tex} \clearpage
	\input{./Broed/Okategoriserat/00-Index.tex} \clearpage
	
och filen _./Broed/Fruktbroed/00-Index.tex_ ser ut såhär:

	\subsection{Fruktbröd}
	\input{./Broed/Fruktbroed/SamisktRonnbarsbrod.tex} \clearpage
	
Alltså, ska man lägga till ett recept så skapar man en TeX-fil (se mall nedan), sparar den i rätt kategori och underkategori och lägger till motsvarande referens i underkategorins _00-Index.tex_-fil.

## Mall för recept
En mall för receptet, som man kan kopiera in i rätt underkategori och döpa om till rätt namn kan hittas i filen _ReceptTemplate.tex_.

## Användbara kommandon
För att underlätta formateringen av texten så finns det vissa fördefinierade kommandon för vanliga mått. Dessa är definierade i filen _COOKBOOKCOMMANDS.sty_ och det är fritt fram att lägga till nya kommandon där om något saknas.

Följande kommandon är definierade:

	\gram
	\mliter
	\dliter
	\liter
	\krm
	\tsk
	\msk
	\st
	\gradC
	\minut
	\minuter
	\timme
	\timmar
	\dagar