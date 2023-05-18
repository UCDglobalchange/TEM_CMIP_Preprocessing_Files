for dir in ${dirs[@]}; do
cd $dir
cvar=( $(basename $dir | cut -d '_' -f 1) )
scenario=( $(basename $dir | cut -d '_' -f 3) )
X=( $( find . -type f  | grep "$cvar"'_Amon_.*_'"$scenario"'_r1i1p1.*\.nc$' | awk '{ sub(/.*'"$cvar"'_Amon_/, ""); sub(/_'"$scenario"'_r1i1p1.*/, ""); print $0 }' | sort -u) )
export X 
echo ${X[@]}
for name in ${X[@]} ; do
file_group="$name"
/bin/ls | grep $file_group | xargs -x ncrcat -o ${file_group}_concat.nc
du -sh ${file_group}_concat.nc
done
cd ..
done


