import numpy as np
from flask import Flask, request, jsonify, render_template, Response, make_response, escape, stream_with_context
import pickle, socket, subprocess, math
import webbrowser, flask, json

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('interface.html')

def pushData():
		while True:
			cmd = "/home/invoker/Documents/build-files/src/kdd99extractor"
			process = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
			loadreg_model = pickle.load(open('eye_model.pkl', 'rb'))
			load_model = pickle.load(open('save_model.pkl', 'rb'))
			for line in iter(process.stdout.readline, b""):
				line = line.strip()
				columns = str(line)
				columns = columns.replace("b'", "")
				columns = columns.replace("'", "")
				if "icmp" in columns:
					columns = columns.replace("icmp","1.0")
				if "tcp" in columns:
					columns = columns.replace("tcp","0.0")
				if "udp" in columns:
					columns = columns.replace("udp","0.0")
				if "SF" in columns:
					columns = columns.replace("SF","1.0")
				if "OTH" in columns:
					columns = columns.replace("OTH","0.0")
				if "REJ" in columns:
					columns = columns.replace("REJ","0.0")
				if "RSTO" in columns:
					columns = columns.replace("RSTO","0.0")
				if "RSTOS0" in columns:
					columns = columns.replace("RSTOS0","0.0")
				if "RSTR" in columns:
					columns = columns.replace("RSTR","0.0")
				if "S0" in columns:
					columns = columns.replace("S0","0.0")
				if "S1" in columns:
					columns = columns.replace("S1","0.0")
				if "S2" in columns:
					columns = columns.replace("S2","0.0")
				if "S3" in columns:
					columns = columns.replace("S3","0.0")
				if "SH" in columns:
					columns = columns.replace("SH","0.0")
				if "http_443," in columns:
					columns = columns.replace("http_443","0.0")
				if "other," in columns:
					columns = columns.replace("other","0.0")
				if "private," in columns:
					columns = columns.replace("private","0.0")
				if "http," in columns:
					columns = columns.replace("http","0.0")
				if "domain_u," in columns:
					columns = columns.replace("domain_u","0.0")
				if 'oth_i,' in columns:
					columns = columns.replace('oth_i',"0.0")	
				if "domain," in columns:
					columns = columns.replace("domain","0.0")
				if "ecr_i," in columns:
					columns = columns.replace("ecr_i","0.0")
				if "ftp_data," in columns:
					columns = columns.replace("ftp_data","1.0")				
				lis = columns
				#print(ip)
				#print(lis)
				test_list  = [float(x) for x in lis.split(',')]
				index_list = [4, 5, 9, 15, 16, 19, 20, 22, 3]
				indreg_list = [4, 5, 8, 9, 20, 21, 22, 2, 2]  
				resreg_list = [test_list[i] for i in indreg_list] 
				res_list = [test_list[i] for i in index_list] 
				finreg = [np.array(resreg_list)]
				fin = [np.array(res_list)]
				test = load_model.predict(fin)
				if test == 1:	
					testreg = loadreg_model.predict(finreg)
					if testreg < 1:
						tes = "normal"
					elif testreg < 2:
						tes = "dos"
					elif testreg < 3:
						tes = "port"
					elif testreg < 4:
						tes = "nep"
					else:
						tes = "work"
				else:
					tes = "Normal"
				yield 'data: %s\n\n' % '{0}'.format(tes)
				yield 'data: %s\n\n' % '{0}'.format(columns)

@app.route('/listenForPushes')
def stream():
    return Response(pushData(), mimetype="text/event-stream")

if __name__ == "__main__":
    webbrowser.open('http://localhost:8000') # show the page in browser
    app.run(host='localhost', use_reloader=False, port=8000, debug=True) # run the server
    