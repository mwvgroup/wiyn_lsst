# These are just the Weyant14 SNe:
# To generate coordinates for more supernovae, change this list.
for sn in SN2011gy SN2012fm PSNJ07250042+2347030 LSQ12fuk SN2011hb PTF11qzq PTF11mty SN2011iu PTF11owc SN2011ho PTF11qpc; do
    echo "Name,RA,Dec" > ${sn}_ra_dec.txt;
    echo ${sn} | awk '{printf "%s,", $1}' >> ${sn}_ra_dec.txt;
# echo ${sn}, >> ${sn}_ra_dec.txt;
    grep ${sn} observed_target_info.txt | awk '{printf "skycoor -d -n 6 %s %s\n", $3, $4}' | sh | awk '{printf "%s,%s\n", $1, $2}' >> ${sn}_ra_dec.txt;
done
