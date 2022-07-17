#!/bin/bash
BOILERPLATE_DIR=boilerplate
TMP_COMPILE=tmp_compiledir
ROOT="$(pwd)"


mkdir -p $TMP_COMPILE
cp -R $BOILERPLATE_DIR/* $TMP_COMPILE/

#######

FOLDERS=("sets/jigs" "sets/reels")
for FOLDER in "${FOLDERS[@]}"; do
    cd $FOLDER
    ls | while read SET; do
        SETLABEL=$(echo $SET | md5)
        echo $SET
        cd "$SET"
        SETNAME_UNDERSCORE=${SET// /_}
        FILENAME=$SETNAME_UNDERSCORE.tex
        FULLTUNE_GOALPATH=$ROOT/${TMP_COMPILE}/tunes/$(basename $FOLDER)
        echo $SETNAME_UNDERSCORE
        echo $FILENAME
        echo "\subsection{$SET}" > $FILENAME
        echo "\label{$SETLABEL}" >> $FILENAME
        
        COUNTER=1
        ls *.abc | while read TUNE; do
            #echo $COUNTER
            # Full tune
            FULLTUNE_FILENAME=${TUNE}_FULL.tex
            if [ ! -f $FULLTUNE_GOALPATH/$FULLTUNE_FILENAME ]
            then
                FULLTUNE_NAME=$(sed -n 's/^T:[[:space:]]*//p' ${TUNE} | tr -d '\n')
                TUNELABEL=$(echo $FULLTUNE_NAME | md5)
                echo "\\subsection{$FULLTUNE_NAME}" > $FULLTUNE_GOALPATH/$FULLTUNE_FILENAME
                echo "\\label{$TUNELABEL}" >> $FULLTUNE_GOALPATH/$FULLTUNE_FILENAME
                echo "\\begin{abc}[name=$FULLTUNE_FILENAME]" >> $FULLTUNE_GOALPATH/$FULLTUNE_FILENAME
                cat $TUNE >> $FULLTUNE_GOALPATH/$FULLTUNE_FILENAME
                cat $FULLTUNE_GOALPATH/$FULLTUNE_FILENAME
                echo "\\end{abc}" >> $FULLTUNE_GOALPATH/$FULLTUNE_FILENAME
                echo "Tune included in set ~\nameref{$SETLABEL}" >> $FULLTUNE_GOALPATH/$FULLTUNE_FILENAME
                echo "\\input{./tunes/$(basename $FOLDER)/$FULLTUNE_FILENAME}" >> $FULLTUNE_GOALPATH/00-Index.tex
            else
                echo "Tune included in set ~\nameref{$SETLABEL}" >> $FULLTUNE_GOALPATH/$FULLTUNE_FILENAME
            fi

            # And set part
            echo "\\begin{abc}[name=${SETNAME_UNDERSCORE}_${COUNTER}]" >> $FILENAME
            sed '/|/q' $TUNE >> $FILENAME
            echo "\\end{abc}" >> $FILENAME
            echo "Full tune on page ~\pageref{$TUNELABEL}" >> $FILENAME
            ((COUNTER=$COUNTER+1))
        done
        echo "~\\" >> $FILENAME
        echo "~\\" >> $FILENAME
        echo $FOLDER/$FILENAME
        echo $TMP_COMPILE/$FOLDER/$FILENAME
        cat $FILENAME
        mv $FILENAME $ROOT/$TMP_COMPILE/$FOLDER/
        echo "\\input{./${FOLDER}/$FILENAME} " >> $ROOT/$TMP_COMPILE/$FOLDER/00-Index.tex
        echo $ROOT/$TMP_COMPILE/$FOLDER/00-Index.tex
        cat $ROOT/$TMP_COMPILE/$FOLDER/00-Index.tex
        cd ..
    done
    cd $ROOT
done

#######
#echo "Exiting"
#exit

cd $TMP_COMPILE
# Repeate pdflatex twice to build index
pdflatex  -synctex=1 -interaction=nonstopmode -file-line-error -recorder  -shell-escape "Tunestarter.tex" 
pdflatex  -synctex=1 -interaction=nonstopmode -file-line-error -recorder  -shell-escape "Tunestarter.tex" 
mv Tunestarter.pdf ../
cd ..
rm -rf $TMP_COMPILE