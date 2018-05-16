#!/bin/csh -f 
cd /home/gpsproc/test123/123/tectest

foreach site (`ls /home/gpsproc/test123/123/tectest/????????????????s.T02 | cut -c 35-38 | sort -u`)
  set USITE = `echo ${site} | tr '[:lower:]' '[:upper:]'`

  foreach DATE (`ls /home/gpsproc/test123/123/tectest/${site}????????????s.T02 | cut -c 39-48 | sort -u`)
    set YYYY = `echo ${DATE} | awk '{print substr($1,1,4)}'`
    set MM = `echo ${DATE} | awk '{print substr($1,5,2)}'`
    set DD = `echo ${DATE} | awk '{print substr($1,7,2)}'`
    set HH = `echo ${DATE} | awk '{print substr($1,9,2)}'`
    set DDD = `date --date=${YYYY}-${MM}-${DD} +%j | awk '{print $1}'`
    echo "${DDD}"

    ls /home/gpsproc/test123/123/tectest/${site}????????????s.T02 > /home/gpsproc/test123/123/tectest/t02.list
    runpkr00 -g -d @t02.list ${site}${DDD}1

    foreach dat (`ls ${site}${DDD}1.tgd`)
      set YY = `echo ${YYYY} | cut -c 3-4`
      set rn=`awk '/^\ '${USITE}'/ {if (substr($0,26,4)substr($0,31,3) <= '${YYYY}${DDD}') print $0}' ~/station.info.db | awk 'END {print substr($0,149,20)}'`
      set an=`awk '/^\ '${USITE}'/ {if (substr($0,26,4)substr($0,31,3) <= '${YYYY}${DDD}') print $0}' ~/station.info.db | awk 'END {print substr($0,195,20)}'`

      teqc +igs \
           +C2 \
           -R \
           -E \
           -week ${YYYY}/${MM}/${DD} \
           -tr d \
           -O.rt 'TRIMBLE NETR9' \
           -O.rn "${rn}" \
           -O.at 'TRM57971.00     SCIT' \
           -O.an "${an}" \
           -O.pe 0.0000 0.0000 0.0000 \
           -O.int 1 \
           -O.mo "${USITE}" -O.mn "${USITE}" \
           -O.s 'M' \
           -O.obs L1L2C1P2\
           -O.ag 'CWB/Taiwan' -O.o 'CWB/Taiwan' -O.r 'CWB/Taiwan' \
           +O.c " " \
           +O.c "Contact: justin510199@scman.cwb.gov.tw" \
           +O.c "Antenna height is vertical to base of antenna" \
           +O.c " " \
           +err "${USITE}_${YYYY}${DDD}${HH}.err" \
           +nav "${site}${DDD}${HH}.${YY}n","${site}${DDD}${HH}.${YY}g" \
           +obs "${site}${DDD}${HH}.${YY}o" \
           ${dat} 
    end
  
  end
end





rm /home/gpsproc/test123/123/tectest/*.err
rm /home/gpsproc/test123/123/tectest/*.tgd
rm /home/gpsproc/test123/123/tectest/*.17g
