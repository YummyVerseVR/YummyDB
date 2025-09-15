import argparse
import uvicorn
from app import App

parser = argparse.ArgumentParser()
parser.add_argument(
    "-db",
    "--database-path",
    type=str,
    required=False,
    default="./DATABASE",
    help="path to store data",
)
parser.add_argument(
    "-d",
    "--device-server-endpoint",
    type=str,
    required=False,
    default="http://localhost:9000",
    help="endpoint of device server",
)
parser.add_argument(
    "-c",
    "--control-server-endpoint",
    type=str,
    required=False,
    default="http://localhost:8000",
    help="endpoint of control server",
)
parser.add_argument(
    "-p",
    "--port",
    type=int,
    default=8001,
    help="port to run the server on (default: 8001)",
)
parser.add_argument("--debug", action="store_true", help="enable debug mode")
args = parser.parse_args()

app = App(
    args.database_path,
    args.device_server_endpoint,
    args.control_server_endpoint,
    args.debug,
).get_app()

if __name__ == "__main__":
    uvicorn.run(
        "entry:app", host="0.0.0.0", port=args.port, log_level="info", reload=args.debug
    )
