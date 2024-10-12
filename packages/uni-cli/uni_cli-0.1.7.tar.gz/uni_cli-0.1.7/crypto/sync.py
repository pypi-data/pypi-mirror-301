import os

import pandas as pd
from sqlalchemy import Engine, text

from utils.pd import deduplicated


def grid_sync_data(
    engine: Engine, csv_path: str, query: str, update_status: int
) -> int:
    # 查询数据
    data_frame = pd.read_sql(query, engine)
    # 提取 'id' 列
    ids = data_frame["id"].tolist()
    # 删除 'id' 列
    data_frame = data_frame.drop(columns=["id"])
    # 根据 'open_at' 列降序排序
    # data_frame = data_frame.sort_values(by="open_at", ascending=False)

    # 将数据追加写入 CSV 文件
    data_frame.to_csv(
        csv_path,
        mode="a",
        header=not os.path.exists(csv_path),
        index=False,
        encoding="utf-8",
    )
    # csv去重,保留最后加入的数据
    deduplicated(csv_path, "client_order_id", "last")

    # 根据提取的 'id' 列更新数据库中 up_status 字段
    if ids:
        # 使用 text() 构建查询时，确保 :ids 是一个列表
        update_query = text(
            f"UPDATE tx SET up_status = :status WHERE id IN ({','.join(map(str, ids))});"
        )
        with engine.connect() as connection:
            with connection.begin():
                result = connection.execute(
                    update_query,
                    {"status": update_status},
                )

                return result.rowcount

    return 0


def grid_sync_open(engine: Engine, csv_path: str):
    query = "select id,created_at,name,act_name,symbol,qty,cex,status,up_status,path,level,earn,cost,buy_px,benefit,sell_px,profit,order_id,client_order_id,fx_order_id,fx_client_order_id,open_at,close_at from tx where (cost is not null or benefit is not null) and profit is null and up_status = 0;"
    row_count = grid_sync_data(engine, csv_path, query, update_status=1)
    print(f"🚀 grid open count:({row_count})")


def grid_sync_close(engine: Engine, csv_path: str):
    query = "select id,created_at,name,act_name,symbol,qty,cex,status,up_status,path,level,earn,cost,buy_px,benefit,sell_px,profit,order_id,client_order_id,fx_order_id,fx_client_order_id,open_at,close_at from tx where profit is not null and up_status in (0,1);"
    row_count = grid_sync_data(engine, csv_path, query, update_status=2)
    print(f"🎯 grid close count:({row_count})")
