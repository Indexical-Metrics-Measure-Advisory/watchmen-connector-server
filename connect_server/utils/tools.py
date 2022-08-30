
import socket

def get_free_port():
	sock = socket.socket()
	sock.bind(('', 0))
	return sock.getsockname()[1]




def get_most_covered_index(sum_counts,df,binned=[]):
	temp_count = 0
	for index, row in df.iterrows():
		temp_count = temp_count + row[0]
		binned.append(index)
		if temp_count / sum_counts > 0.8:
			break
	return binned

