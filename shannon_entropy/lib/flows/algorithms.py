# coding=UTF-8

from math import log
from scipy import array, cumsum, mean
import sys, os, time, string, re

def shannon(histogram, to_be_normalized = False):

    """
    Implementa o algoritmo de 'Shannon'.

    Parâmetros:
      - histogram: 'Dicionário' na forma 'ip': num_pacotes
        Ex: {'a.a.a.a': 43, 'b.b.b.b': 17, 'c.c.c.c': 37}

      - to_be_normalized: 'Booleano' que especifica se o devemos normalizar

    Retorno:
      O resultado (float), normalizado ou não, do algoritmo de Shannon.
    """

    shannon = 0

    for value in histogram.values():
      shannon += value * log(value, 2)   # shannon = shannon + value * log(value, 2)

    shannon *= -1 

    if to_be_normalized:
      num_of_ips = len( histogram.keys() )
      if num_of_ips > 1:
         shannon /= log(num_of_ips, 2)   # shannon = shannon/log(num_of_ips, 2)

    return shannon

def ewma(s, n):
    """
    returns an n period exponential moving average for the time series s

    s is a list ordered from oldest (index 0) to most recent (index -1)
    n is an integer

    returns a numeric array of the exponential moving average
    """
    ewma = []
    j = 1
    #get n sma first and calculate the next n period ewma
    sma = sum(s[:n]) / n
    # multiplier = 2 / float(1 + n)
    multiplier = 0.01
    ewma.append(sma)
    #EMA(current) = ( (Price(current) - EMA(prev) ) x Multiplier) + EMA(prev)
    ewma.append(( (s[n] - sma) * multiplier) + sma)
    #now calculate the rest of the values
    for i in s[n+1:]:
        tmp = ( (i - ewma[j]) * multiplier) + ewma[j]
        j = j + 1
        ewma.append(tmp)
        
    return ewma

def createrrd(rrd_filename, startdate):
    """
    Creates RRD database file
    """
    data_inicio  = time.mktime( time.strptime( startdate, "%Y%m%d%H%M" ))
    data_inicio  = str(int(data_inicio))
    step = "300"
    row_count = "2016"
    alpha = "0.01"
    beta = "0.0035"
    #gamma = "0.1"
    period = "288"
    rrdtool_cmd = "rrdtool create " + rrd_filename + " --start " + data_inicio + " --step " + step + " DS:entropia:GAUGE:600:0:1 RRA:AVERAGE:0.5:1:600 RRA:AVERAGE:0.5:6:700 RRA:AVERAGE:0.5:24:775 RRA:AVERAGE:0.5:288:797 RRA:MAX:0.5:1:600 RRA:MAX:0.5:6:700 RRA:MAX:0.5:24:775 RRA:MAX:0.5:288:797 "
    try:
        os.system(rrdtool_cmd)
    finally:
        #print "Arquivo %s criado com sucesso!" % (rrd_filename)
        print ''
    return

def createrrdhw(rrd_filename, startdate):
    """
    Creates RRD database file
    """
    data_inicio  = time.mktime( time.strptime( startdate, "%Y%m%d%H%M" ))
    data_inicio  = str(int(data_inicio))
    step = "300"
    row_count = "2016"
    alpha = "0.01"
    beta = "0.0035"
    period = "288"
    rrdtool_cmd = "rrdtool create " + rrd_filename + " --start " + data_inicio + " --step " + step + " DS:entropia:GAUGE:600:0:1 RRA:AVERAGE:0.5:1:600 RRA:AVERAGE:0.5:6:700 RRA:AVERAGE:0.5:24:775 RRA:AVERAGE:0.5:288:797 RRA:MAX:0.5:1:600 RRA:MAX:0.5:6:700 RRA:MAX:0.5:24:775 RRA:MAX:0.5:288:797 RRA:HWPREDICT:" + row_count + ":" + alpha + ":" + beta + ":" + period
    try:
        os.system(rrdtool_cmd)
    finally:
        #print "Arquivo %s criado com sucesso!" % (rrd_filename)
        print ''
    return

def createrrdmhw(rrd_filename, startdate):
    """
    Creates RRD database file
    """
    data_inicio  = time.mktime( time.strptime( startdate, "%Y%m%d%H%M" ))
    data_inicio  = str(int(data_inicio))
    step = "300"
    row_count = "2016"
    alpha = "0.01"
    beta = "0.0035"
    period = "288"
    rrdtool_cmd = "rrdtool create " + rrd_filename + " --start " + data_inicio + " --step " + step + " DS:entropia:GAUGE:600:0:1 RRA:AVERAGE:0.5:1:600 RRA:AVERAGE:0.5:6:700 RRA:AVERAGE:0.5:24:775 RRA:AVERAGE:0.5:288:797 RRA:MAX:0.5:1:600 RRA:MAX:0.5:6:700 RRA:MAX:0.5:24:775 RRA:MAX:0.5:288:797 RRA:MHWPREDICT:" + row_count + ":" + alpha + ":" + beta + ":" + period
    try:
        os.system(rrdtool_cmd)
    finally:
        #print "Arquivo %s criado com sucesso!" % (rrd_filename)
        print ''
    return

def ewmaold(series, window):
    """
    returns an n period exponential moving average for the time series s

    series is a list ordered from oldest (index 0) to most recent (index -1)
    window is an integer

    returns a numeric array of the exponential moving average
    """
    series = series
    ewma = []
    window = 1

    #get window sma first and calculate the next window period ewma
    sma = sum(s[:window]) / n
    alpha = 2 / float(1 + n)
    ewma.append(sma)

    #EWMA(current) = ( (Price(current) - EWMA(prev) ) x Multiplier) + EWMA(prev)
    ewma.append(( (series[window] - sma) * alpha) + sma)

    #now calculate the rest of the values
    for i in series[window+1:]:
        tmp = ( (i - ewma[window]) * alpha) + ewma[window]
        window = window + 1
        ewma.append(tmp)

    return ewma

def movavg(s, n):
    ''' returns an n period moving average for the time series s
       
        s is a list ordered from oldest (index 0) to most recent (index -1)
        n is an integer

        returns a numeric array of the moving average
        
        This should run in near constant time with regard to n (of course, 
        O(n) to the length of s).  At least one person has said yuk because 
        of the numerical issue of losing precision in the cumsum, but for
        small n's, and values like you will see in stock prices and indices,
        I don't think this is too much of a problem.  Someone may have 
        a more numerically stable version, but then you could just implement
        the c-code version and wrap it for python.
    '''
    s = array(s)
    c = cumsum(s)
    return (c[n-1:] - c[:-n+1]) / float(n)


def sma(series, window):
    ''' returns an unweighted mean of the previous "window" values (data points) for the time series "series".
    
        series is a list ordered from oldest to most recent
        window is an integer, representing the amount of past values used to calculate the mean
        
        returns a numeric value of the mean for the provided "window"
    '''
    series = array(series)
    constant = cumsum(series)
    return (constant[window-1:] - constant[:-window+1] / float(window))
    
def sma(valores, janela):
    serie = valores[0:janela]
    return scipy.mean(serie) 

def rrdgraph(rrdfile, graphtitle, data_inicio, data_fim):
    '''
    Gerador de graficos de dados em base RRD '
    '''
    arq_imagem        = string.rsplit(rrdfile,'.', maxsplit=1)
    arq_imagem        = arq_imagem[0]+'.png'
    data_inicio_epoch = time.mktime( time.strptime( data_inicio, "%Y%m%d%H%M" ))
    data_fim_epoch    = time.mktime( time.strptime( data_fim, "%Y%m%d%H%M" ))
    comentario1       = time.ctime(data_inicio_epoch)+' to '+time.ctime(data_fim_epoch)
    #comentario1      = '"'+re.escape(comentario1)+'\c"'
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
    LINE1:entropia#FF0000:"Entropia"' % (arq_imagem, data_inicio_epoch, data_fim_epoch, graphtitle, comentario1, comentario2, vertical, rrdfile)) 
    return

def rrdgraphhw(rrdfile, graphtitle, data_inicio, data_fim):
    '''
    Gerador de graficos de dados em base RRD '
    '''
    arq_imagem        = string.rsplit(rrdfile,'.', maxsplit=1)
    arq_imagem        = arq_imagem[0]+'.png'
    data_inicio_epoch = time.mktime( time.strptime( data_inicio, "%Y%m%d%H%M" ))
    data_fim_epoch    = time.mktime( time.strptime( data_fim, "%Y%m%d%H%M" ))
    comentario1       = time.ctime(data_inicio_epoch)+' to '+time.ctime(data_fim_epoch)
    #comentario1      = '"'+re.escape(comentario1)+'\c"'
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
    TICK:fail#a4a4a4:1.0:"Anomalia" \
    LINE2:dev_lower#6e6e6e:"Limiar de confianca" \
    LINE2:dev_upper#6e6e6e \
    LINE1:entropia#FF0000:"Entropia"' % (arq_imagem, data_inicio_epoch, data_fim_epoch, graphtitle, comentario1, comentario2, vertical, rrdfile, rrdfile, rrdfile, rrdfile, rrdfile, rrdfile)) 

def rrdplothw(rrdfile, graphtitle, data_inicio, data_fim):
    '''
    Gerador de graficos de dados em base RRD
    '''
    arq_imagem        = string.rsplit(rrdfile,'.', maxsplit=1)
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
    LINE1:pred#FF0000:"Holt Winters"' % (arq_imagem, data_inicio_epoch, data_fim_epoch, graphtitle, comentario1, comentario2, vertical, rrdfile, rrdfile, rrdfile, rrdfile, rrdfile, rrdfile))
    return

def tunerrdgamma(rrd_filename, gamma):
    """
    Modifies an RRD database Holt-Winters gamma parameter:
    Alter the seasonal coefficient adaptation parameter for the SEASONAL RRA and
    alter the seasonal deviation adaptation parameter for the DEVSEASONAL RRA.
    
    This parameter must be between 0 and 1.
    """

    rrdtool_tune_cmd = "rrdtool tune " + rrd_filename + " --gamma " + gamma + " --gamma-deviation " + gamma

    os.system(rrdtool_tune_cmd)

    #try:
    #    os.system(rrdtool_tune_cmd)
    #finally:
    #    print ''
    #return

    return

