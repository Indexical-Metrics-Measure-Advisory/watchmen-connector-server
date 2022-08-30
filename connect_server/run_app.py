import shlex
import subprocess
import sys



streamlit_port = sys.argv[1]
achievementId  = sys.argv[2]
cmd ="streamlit run app.py --server.port {} --server.headless true -- {}".format(streamlit_port,achievementId)

subprocess.run(shlex.split(cmd))




