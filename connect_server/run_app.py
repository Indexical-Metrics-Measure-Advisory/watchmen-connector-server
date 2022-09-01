import shlex
import subprocess
import sys

from connect_server.config import settings

streamlit_port = sys.argv[1]
achievementId  = sys.argv[2]
app_name = sys.argv[3]
app_path = settings.streamlit_folder+"/"+app_name



print("app_path ",app_path)

cmd ="streamlit run {}--server.port {} --server.headless true -- {}".format(app_path,streamlit_port,achievementId)

subprocess.run(shlex.split(cmd))




