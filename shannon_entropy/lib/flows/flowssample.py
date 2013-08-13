# coding=UTF-8

from __future__ import with_statement
import shutil

	
class FlowsSample:

	"""
	Representa uma amostra de fluxo, da qual podemos extrair um histograma, etc.
	"""

	def __init__(self, file):
		self.file = file



	def __records(self):
		
  		"""
		Um gerador, que provê um dicionário para cada linha processada do arquivo de amostra.
		"""
		
		for line in open(self.file, 'r'):
			if len(line.strip()) > 0:
				ip, num_packets = line.split(',')
				ip = ip.strip()
				num_packets = int( num_packets )
				yield {'ip': ip, 'num_packets': num_packets}
			else:
				yield {}



	def histogram(self):

		"""
		Calcula o histograma normalizado do arquivo de amostra 'self.file' e o retorna através de um dicionário de chaves que representam IPs e valores que representam o total de número de pacotes.
		"""
		
		h = {}

		for record in self.__records():
			if record != {}:
				if record['ip'] in h:
					h[record['ip']] += record['num_packets']
				else:
					h[record['ip']] = record['num_packets']

		total_num_packets = sum(h.values())

		for key, value in h.iteritems():
			h[key] = float( h[key] ) / total_num_packets

		return h



	def inject_anomaly(self, anomaly_file, factor, injected_file):

		"""
		Insere a anomalia descrita no arquivo "anomaly_file", utilizando-se o fator de escala "factor", e salva o resultado no arquivo "injected_file".
		"""
		shutil.copy(self.file, injected_file)

		with open(injected_file, 'a') as injected:
			for line in open(anomaly_file, 'r'):
				ip, num_packets = line.split(',')
				ip = ip.strip()
				num_packets = int( num_packets ) * factor
				num_packets = int( num_packets + 1 )
				injected.write(ip + ', ' + str(num_packets) + '\n')



