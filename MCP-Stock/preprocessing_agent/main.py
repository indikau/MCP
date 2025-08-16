from mcp import MCPServer, Message
from utils.preprocess import align_timeframes, calculate_returns, normalize_volume

server = MCPServer(agent_id="preprocessing_agent")

@server.on_message("price_data")
def handle_price_data(msg: Message):
    aligned_df = align_timeframes(msg.content)
    returns_df = calculate_returns(aligned_df)
    normalized_vol_df = normalize_volume(aligned_df)
    
    # Create response
    response = {
        "symbol": "NVTS",
        "date": str(aligned_df.index[-1]),
        "daily_return": returns_df["NVTS"].iloc[-1],
        "normalized_volume": normalized_vol_df["NVTS"].iloc[-1]
    }
    msg.reply(response)

server.start()