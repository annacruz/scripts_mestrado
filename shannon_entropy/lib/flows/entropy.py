# coding=UTF-8

# Descrição:
# Esta classe sabe tratar arquivos de "fluxos", gerar um histograma dessas informações, aplicar um algoritmo para cálculo de entropia a este e, por fim, anexar o resultado num arquivo RRD.

import glob
import os
import time

from flowssample import FlowsSample
from algorithms import shannon
from algorithms import ewma
from algorithms import createrrd,createrrdhw,createrrdmhw,rrdgraph,rrdgraphhw,tunerrdgamma
from utils import progressbar

class Entropy:
    
    """
    Calcula entropia de arquivos de fluxos existentes num determinado diretório.
    """

    def __init__(self, input_dir, filename_wildcard):
    
        """ 
        - input_dir: diretório que contém os dados filtrados
        - filename_wildcard: expressão regular utilizada para filtrar os arquivos desejados
        """
        self.dir = input_dir
        self.wildcard = filename_wildcard

    def evaluate(self, algorithm, rrd_file):
        """
        Processa as informações contidas nos arquivos selecionados em "self.input_dir" e 'appenda' as informações no "rrd_file".
        """
        vetor_ewma = [] # EWMA
        janela = 1      # EWMA
        files = glob.glob(self.dir + '/' + self.wildcard)
	files.sort()
        first_timestamp = files[0].split('/')[-1].split('-')[0] # EWMA
        first_timestamp_epoch = time.mktime( time.strptime( first_timestamp, "%Y%m%d%H%M" ) ) # EWMA
        idx_arq = 0
        #pb = progressbar(288, "*")
        pb = progressbar(len(files), "*")

        if not os.path.isfile(rrd_file):
            createrrdhw(rrd_file, '200701010000')   # Cria o arquivo da base RRD
            tunerrdgamma(rrd_file, '0.1')           # Modifica o parametro gamma do Holt-Winters no RRD

        for f in files:
            idx_arq = idx_arq + 1
            histogram = FlowsSample(f).histogram()

            result = algorithm(histogram, to_be_normalized = True)   # Calcula entropia de shannon 

            timestamp = f.split('/')[-1].split('-')[0]
            timestamp_epoch = time.mktime( time.strptime( timestamp, "%Y%m%d%H%M" ) )
            vetor_ewma.append(result) # EWMA - Guarda as entropias calculadas no vetor
            
            rrd_line = "%s:%f" % (timestamp_epoch, result) # rrd_line = parametros para gravar entropia no RRD

            #if not os.path.isfile(rrd_file):   # Verifica se existe o arquivo RRD
#            createrrdhw(rrd_file, '200701010000')   # Cria o arquivo da base RRD
#            tunerrdgamma(rrd_file, '0.1')           # Modifica o parametro gamma do Holt-Winters no RRD

            os.system('rrdtool update %s %s' % (rrd_file, rrd_line)) # Grava o valor da entropia na base RRD
            pb.progress(idx_arq)  # Exibe barra de progresso do processamento de SHANNON
            #print "[%s] [%d] %s" % (rrd_file, idx_arq, rrd_line)
        
        # Grafico Entropia com Holt-Winters
        #graphtitle = rrd_file + " Entropia" # Titulo do grafico SHANNON c/ Holt-Winters
        #startdate = '200811270000'          # Data inicial grafico SHANNON c/ H.W.
        #enddate = '200811302355'            # Data final   grafico SHANNON c/ H.W.
        #rrdgraphhw(rrd_file, graphtitle, startdate, enddate) # Gera grafico SHANNON c/ H.W.

        resultado_ewma = []                       # EWMA - Inicializa vetor p/ EWMA
        ewma_entropias = ewma(vetor_ewma,janela)  # EWMA - Calcula EWMA dos valores normalizados

        ewma_timestamp_epoch = first_timestamp_epoch

        for item_ewma_entropias in range(len(ewma_entropias)):       # EWMA - Loop p/ calcular EWMA
            resultado_ewma.append( (ewma_timestamp_epoch, ewma_entropias[item_ewma_entropias] ) ) # EWMA - Guarda EWMA no vetor
            ewma_timestamp_epoch = ewma_timestamp_epoch + float(300) # EWMA - Preenche tuplas com timestamp
        
        rrd_file_ewma = rrd_file + '-ewma.rrd'
        # EWMA - Testa se existe o arquivo RRD para cada metrica, caso negativo o arquivo e' criado:
        #if not os.path.isfile('sa-ewma.rrd') and not os.path.isfile('da-ewma.rrd') and not os.path.isfile('sp-ewma.rrd') and not os.path.isfile('dp-ewma.rrd'): # EWMA - Se nao existir nenhum arq. RRD
        #   rrd_file_ewma = 'sa-ewma.rrd' # Arquivo RRD a ser criado
        #elif os.path.isfile('sa-ewma.rrd') and not os.path.isfile('da-ewma.rrd') and not os.path.isfile('sp-ewma.rrd') and not os.path.isfile('dp-ewma.rrd'): # EWMA - ARquivo RRD a ser criado
        #   rrd_file_ewma = 'da-ewma.rrd' 
        #elif os.path.isfile('sa-ewma.rrd') and os.path.isfile('da-ewma.rrd') and not os.path.isfile('sp-ewma.rrd') and not os.path.isfile('dp-ewma.rrd'): # EWMA - Arq. RRD a ser criado
        #   rrd_file_ewma = 'sp-ewma.rrd' 
        #elif os.path.isfile('sa-ewma.rrd') and os.path.isfile('da-ewma.rrd') and os.path.isfile('sp-ewma.rrd') and not os.path.isfile('dp-ewma.rrd'): # EWMA - Arq. RRD a ser criado
        #   rrd_file_ewma = 'dp-ewma.rrd' 

        #createrrd(rrd_file_ewma, '200801010000')  # EWMA - Comando p/ criar o arq. RRD

        createrrdhw(rrd_file_ewma, '200801010000') # EWMA - Comando p/ criar o arq. RRD 

        for item_ewma in resultado_ewma:           # EWMA - Para cada tupla do vetor EWMA
            ewma_timestamp = str(item_ewma[0])     # EWMA - armazena o timestamp da tupla
            ewma_value = str(item_ewma[1])         # EWMA - Valor do EWMA da tupla
            rrd_line_ewma = "%s:%s" % (ewma_timestamp, ewma_value) # EWMA - Tupla a ser gravada no RRD
            # rrd_line_ewma = "%s:%s" % (str(item_ewma[0], str(item_ewma[1])   # EWMA - Tupla a ser gravada no RRD
            os.system('rrdtool update %s %s' % (rrd_file_ewma, rrd_line_ewma)) # EWMA - Grava tupla no RRD

        #graphtitle_ewma = rrd_file_ewma + " EWMA" # EWMA - Titulo do grafico EWMA
        #startdate_ewma = '200811270000' # EWMA - Data inicial do grafico EWMA
        #enddate_ewma = '200811302355'   # EWMA - Data final do grafico EWMA
        #rrdgraph(rrd_file_ewma, graphtitle_ewma, startdate_ewma, enddate_ewma) # EWMA - Gera grafico EWMA

        return rrd_line
