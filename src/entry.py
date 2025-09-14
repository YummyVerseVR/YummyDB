import argparse
import uvicorn
from app import App

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--database-path", type=str, required=True, help="path to store data"
    )
    parser.add_argument(
        "-e",
        "--control-server-endpoint",
        type=str,
        required=True,
        help="endpoint of control server",
    )
    args = parser.parse_args()

    app = App(args.database_path, args.control_server_endpoint)
    uvicorn.run(app.get_app(), host="0.0.0.0", port=8000, log_level="info")
