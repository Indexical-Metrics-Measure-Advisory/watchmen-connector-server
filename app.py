from uvicorn import run

if __name__ == "__main__":
	run("connect_server.main:app", host="127.0.0.1", port=5000, log_level="info", workers=1)
