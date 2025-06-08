import uvicorn 
import sys

if __name__ == '__main__':
    port = 8000
    if '--port' in sys.argv:
        idx = sys.argv.index('--port')
        if idx + 1 < len(sys.argv):
            try:
                port = int(sys.argv[idx + 1])
            except ValueError:
                pass
    uvicorn.run("app_management.app:app", log_level = "info", port = port)