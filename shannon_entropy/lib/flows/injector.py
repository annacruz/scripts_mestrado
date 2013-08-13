# coding=UTF-8

import re
from glob import glob
from shutil import copy

from flows.flowssample import FlowsSample


class Injector:

	def __init__(self, configuration):

		"""
		Inicializa um objeto Injector com informa��es contidas no dicion�rio 'configuration'.

		As seguintes vari�veis devem estar definidas no dicion�rio 'configuration', passado como par�metro:

		  starts_at  : O data-hora de in�cio da inje��o, no formato AAAAMMDDHHMM.
		  samples    : Diret�rio que cont�m os arquivos de 'amostras'.
		  anomalies  : Diret�rio que cont�m os arquivos de 'anomalias'.
		  injected   : Diret�rio que cont�m os arquivos 'injetados'.
		  scale      : Fator de escala a ser aplicado nos registros de anomalias. Escalas usadas no paper para o SBRC 2009: 0.02919 (para 10%), 0.14595 (50%), 0.5838 (20%) e 0.073 (25%)
		  filename_re: Express�o regular que define o padr�o de nome dos arquivos. Ela define os seguintes agrupamentos:
		    - timestamp
		    - pop
		    - type
		    - interface
		"""
    
		self.configuration = configuration


	def __get_fields(self, file):

		fields = {}

		filename_re = re.compile(self.configuration['filename_re'])
		
		filename_match = filename_re.match( file.split('/')[-1] )

		if filename_match:
			fields['timestamp'] = filename_match.group('timestamp') 
			fields['pop'] = filename_match.group('pop')
			fields['type'] = filename_match.group('type')
			fields['interface'] = filename_match.group('interface')
		
		return fields
			

	def inject(self):

		head, middle, tail = [], [], []
		fields = {}
		position = 0

		anomalies = glob( self.configuration['anomalies'] + '/*' )
		anomalies.sort()

		samples = glob(self.configuration['samples'] + '/*')
		samples.sort() 

		fs = FlowsSample(samples[0]) # somente criando um objeto para mudar o estado dentro do loop 
  
		# copying 'head' files
		for k, sample in enumerate(samples):

			fields = self.__get_fields(sample)
	
			if fields != {}:
				if fields['timestamp'] < self.configuration['starts_at']:
					copy(sample, self.configuration['injected'])
				else:
					head = samples[0:k]
					position = k
					break

		print "Escala: ", float(self.configuration['scale'])
		# applying anomalies
		if len(samples) - position < len(anomalies):
			raise RuntimeError, "Existem mais anomalias a inserir do que a quantidade de amostras."
		else:
			middle = samples[position : position + len(anomalies)]
			i = 0 # �ndice para o vetor de anomalias
			for k in range( position, position + len(anomalies) ):
				fs.file = samples[k]
				fs.inject_anomaly(anomalies[i], float(self.configuration['scale']), self.configuration['injected'] + '/' + fs.file.split('/')[-1])
				i += 1
			position += len(anomalies)


		# copying 'tail' files
		tail = samples[position : ]
		for k in range( position, len(samples) ):
			copy(samples[k], self.configuration['injected'])

		# print len(head)
		# print len(middle)
		# print len(tail)
		print " ===== Fim do Processamento ===== "

