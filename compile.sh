#!/bin/bash
BOILERPLATE_DIR=boilerplate
TMP_COMPILE=tmp_compiledir
ROOT="$(pwd)"

mkdir -p $TMP_COMPILE
cp -R $BOILERPLATE_DIR/* $TMP_COMPILE/

#######

FOLDERS=("sets/jigs")
for FOLDER in $FOLDERS; do
    cd $FOLDER
    for SET in "$(ls)"; do
        #echo $SET
        cd "$SET"
        SETNAME_UNDERSCORE=${SET// /_}
        FILENAME=$SETNAME_UNDERSCORE.tex
        echo "\subsection{$SET}" > $FILENAME
        COUNTER=1
        for TUNE in $(ls *.abc); do
            #echo $COUNTER
            echo "\\begin{abc}[name=${SETNAME_UNDERSCORE}_${COUNTER}]" >> $FILENAME
            sed '/|/q' $TUNE >> $FILENAME
            echo "\\end{abc}" >> $FILENAME
            ((COUNTER=$COUNTER+1))
        done
        #echo $FOLDER/$FILENAME
        #echo $TMP_COMPILE/$FOLDER/$FILENAME
        #cat $FILENAME
        mv $FILENAME $ROOT/$TMP_COMPILE/$FOLDER/
        echo "\\input{./sets/jigs/$FILENAME} \clearpage" >> $ROOT/$TMP_COMPILE/$FOLDER/00-Index.tex
        #echo $ROOT/$TMP_COMPILE/$FOLDER/00-Index.tex
        cat $ROOT/$TMP_COMPILE/$FOLDER/00-Index.tex
    done
    cd $ROOT
done

#######
#echo "Exiting"
#exit
#echo "This should not show"

cd $TMP_COMPILE
pdflatex  -synctex=1 -interaction=nonstopmode -file-line-error -recorder  -shell-escape "Tunestarter.tex" 
mv Tunestarter.pdf ../
cd ..
rm -rf $TMP_COMPILE