#!/bin/bash
BOILERPLATE_DIR=boilerplate
TMP_COMPILE=tmp_compiledir
ROOT="$(pwd)"

mkdir -p $TMP_COMPILE
cp -R $BOILERPLATE_DIR/* $TMP_COMPILE/

#######

FOLDERS=("sets/jigs" "sets/reels")
for FOLDER in ${FOLDERS[@]}; do
    cd $FOLDER
    ls | while read SET; do
        #echo $SET
        cd "$SET"
        SETNAME_UNDERSCORE=${SET// /_}
        FILENAME=$SETNAME_UNDERSCORE.tex
        #echo $SETNAME_UNDERSCORE
        #echo $FILENAME
        echo "\subsection{$SET}" > $FILENAME
        COUNTER=1
        ls *.abc | while read TUNE; do
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
        echo "\\input{./${FOLDER}/$FILENAME} \clearpage" >> $ROOT/$TMP_COMPILE/$FOLDER/00-Index.tex
        #echo $ROOT/$TMP_COMPILE/$FOLDER/00-Index.tex
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