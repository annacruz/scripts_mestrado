#!/usr/bin/env python

import sys, os, time, string, re

rrdfile1          = 'sa-hw-slammer-injetado-pe-ba-udp.rrd'
graphtitle        = "BA-PE UDP | Slammer worm | Entropia IP Origem | Estimativa: Holt-Winters"
data_inicio       = '200811260000'
data_fim          = '200811282355'

arq_imagem        = string.rsplit(rrdfile1,'.', maxsplit=1)
arq_imagem        = arq_imagem[0]+'.png'
data_inicio_epoch = time.mktime( time.strptime( data_inicio, "%Y%m%d%H%M" ))
data_fim_epoch    = time.mktime( time.strptime( data_fim, "%Y%m%d%H%M" ))
comentario1       = time.ctime(data_inicio_epoch)+' to '+time.ctime(data_fim_epoch)
comentario1       = comentario1.replace(':','\:')
comentario1       = '"'+comentario1+'\c"'
comentario2       = '"'+"\\n"+'"'
vertical          = '"'+'Grau de entropia'+'"'
data_inicio_epoch = str(data_inicio_epoch).split(".")
data_inicio_epoch = data_inicio_epoch[0]
data_fim_epoch    = str(data_fim_epoch).split(".")
data_fim_epoch    = data_fim_epoch[0]
graphtitle        = re.escape(graphtitle)

os.system('rrdtool graph %s \
--imgformat=PNG \
--start %s \
--end %s \
--title=%s \
--upper-limit=1.0 \
--lower-limit=0.0 \
COMMENT:%s \
COMMENT:%s \
--rigid \
--base=1000 \
--height=120 \
--width=500 \
--vertical-label=%s \
--slope-mode \
--font TITLE:9: \
--font AXIS:8: \
--font LEGEND:8: \
--font UNIT:8: \
DEF:entropia=%s:entropia:AVERAGE \
DEF:pred=%s:entropia:HWPREDICT \
DEF:dev=%s:entropia:DEVPREDICT \
DEF:season=%s:entropia:SEASONAL \
DEF:devseason=%s:entropia:DEVSEASONAL \
DEF:fail=%s:entropia:FAILURES \
CDEF:dev_lower=pred,dev,2,*,- \
CDEF:dev_upper=pred,dev,2,*,+ \
LINE3:pred#00FF00:"Holt-Winters" \
LINE2:dev_lower#6e6e6e:"Limiar de confianca (Holt-Winters)" \
LINE2:dev_upper#6e6e6e \
LINE1:entropia#FF0000:"Entropia"' % (arq_imagem, data_inicio_epoch, data_fim_epoch, graphtitle, comentario1, comentario2, vertical, rrdfile1, rrdfile1, rrdfile1, rrdfile1, rrdfile1, rrdfile1)) 

print ' '
print 'Arquivo RRD.........: ', rrdfile1
print 'Arquivo imagem......: ', arq_imagem
print 'Titulo..............: ', graphtitle
print 'Data inicio.........: ', data_inicio
print 'Data fim............: ', data_fim
print "Data inicio em epoch: ", data_inicio_epoch
print "Data fim............: ", data_fim
print "Data fim em epoch...: ", data_fim_epoch
print 'Comentario1.........: ', comentario1
print 'Comentario2.........: ', comentario2

