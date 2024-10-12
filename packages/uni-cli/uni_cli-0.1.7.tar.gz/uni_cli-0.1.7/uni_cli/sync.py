import os

import typer
from dotenv import load_dotenv
from sqlalchemy import create_engine

from crypto.sync import grid_sync_close, grid_sync_open

app = typer.Typer()


@app.command()
def grid(
    env_path: str = "d:/.env", csv_path: str = "d:/github/txnj/data/bitget_grid_0.csv"
):
    """同步mysql数据到csv文件

    Args:
        env_path (string, optional): .env文件路径, Defaults to "d:/.env".\n
        csv_path (string, optional): 保存csv文件路径, Defaults to "d:/github/txnj/data/bitget_grid_0.csv".
    """
    # 加载 .env 文件
    load_dotenv(env_path)

    host = os.getenv("UNI_CLI_MYSQL_HOST")
    user = os.getenv("UNI_CLI_MYSQL_USER")
    password = os.getenv("UNI_CLI_MYSQL_PASSWORD")
    database = os.getenv("UNI_CLI_MYSQL_DATABASE")

    engine = create_engine(
        f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
    )

    grid_sync_close(engine, csv_path)
    grid_sync_open(engine, csv_path)
