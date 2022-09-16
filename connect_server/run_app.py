import shlex
import subprocess
import sys

streamlit_port = sys.argv[1]
achievementId = sys.argv[2]
app_path = sys.argv[3]
watchmen_host = sys.argv[4]

cmd = "streamlit run {} --server.port {} --server.headless true -- {} {}".format(app_path, streamlit_port, achievementId,watchmen_host)

subprocess.run(shlex.split(cmd))
