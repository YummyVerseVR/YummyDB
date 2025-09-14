import argparse
import uvicorn
from app import App

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-db", "--database-path", type=str, required=True, help="path to database store"
    )
    args = parser.parse_args()

    app = App(args.database_path)
    uvicorn.run(app.get_app(), host="0.0.0.0", port=8000, log_level="info")
