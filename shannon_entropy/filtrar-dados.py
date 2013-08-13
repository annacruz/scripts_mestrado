#!/usr/bin/env python

# $1 = Roteador | # $2 = Interface | # $3 = Workdir (ouput dir)
# $4 = Arquivo netflow | # $4 = Diretorio com arquivos netflow

import os, sys, string

#prefix = '/Volumes/Samsung/Docs/Mestrado/anomaly/samples/2wperformance/'
prefix = '/home/yui/dev/mestrado/traffic/'
#prefix = os.getcwd()

roteador   = raw_input('Nome do roteador..............: ')
interface  = raw_input('Interface.....................: ')
add_filtro = raw_input('Mais filtros p/ nfdump........: ')
workdir    = raw_input('Diretorio de saida............: ')
dir_nfcapd = raw_input('Diretorio c/ arqs. nfcapd.....: ')

dir_nfcapd = os.path.join(prefix, dir_nfcapd)

try:
    os.chdir(dir_nfcapd)
finally:
    arqs_nfcapd = os.listdir(os.getcwd())  # Lendo nomes dos arqs da amostra normal para a lista arqs_nfcapd
    arqs_nfcapd = sorted(arqs_nfcapd)

print "\nVariaveis usadas:\n"
print "Workdir...........: " + workdir

i = 0
j = 0
nfdump_fmt = [ 'fmt:%sa,%pkt', 'fmt:%da,%pkt', 'fmt:%sp,%pkt', 'fmt:%dp,%pkt' ] 
nfdump_cmd = "nfdump -q -o " + nfdump_fmt[j] + " -r " + arqs_nfcapd[i] + " \'in if" + interface + " " + add_filtro + "\'"

while i <= len(arqs_nfcapd) - 1:
   j = 0
   while j <= 3:
#     nfdump_cmd = "nfdump -q -o " + nfdump_fmt[j] + " -r " + arqs_nfcapd[i] + " \'in if" + interface + " " + add_filtro + "\'"
      timestamp = string.split(arqs_nfcapd[i], ".")[1]
      filt = string.split(string.split(nfdump_fmt[j], ":%")[1], ",")[0]
      filename = timestamp+"-"+roteador+"-"+filt+"-if"+interface+".txt"
      arq_destino = os.path.join(prefix, workdir, filename)
      filtro = nfdump_fmt[j]
      nfcapd_file = arqs_nfcapd[i]

      print "Processando arquivo: " + arqs_nfcapd[i]
      print "Roteador...........: " + roteador
      print "Interface..........: " + interface
      print "Filtro.............: " + nfdump_fmt[j]
      print "Arquivo nfcapd.....: " + arqs_nfcapd[i]
      print "Comando............: " + "nfdump -q -o %s -r %s 'in if %s %s' > %s" % (filtro, nfcapd_file, interface, add_filtro, arq_destino)
      print "Gravando arquivo...: " + arq_destino 
      print " "
      os.system("nfdump -q -o %s -r %s 'in if %s %s' > %s" % (filtro, nfcapd_file, interface, add_filtro, arq_destino))
      j = j + 1
   i = i + 1
