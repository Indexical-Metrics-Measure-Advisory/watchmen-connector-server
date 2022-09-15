import shlex
import subprocess
import sys

streamlit_port = sys.argv[1]
achievementId = sys.argv[2]
app_path = sys.argv[3]

cmd = "streamlit run {} --server.port {} --server.headless true -- {}".format(app_path, streamlit_port, achievementId)

print(cmd)
subprocess.run(shlex.split(cmd))
