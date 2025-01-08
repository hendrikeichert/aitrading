

def pybroker_test():
    from ai_trader.pybroker_test import pybroker_work_in_progress
    pybroker_work_in_progress

def run_ai_trader():
    from ai_trader.ai_trader import AiTrader
    trader = AiTrader()
    trader.initialize()
    trader.stock_example()
    # trader.crypto_example()
    # trader.news_example()


if __name__ == '__main__':
    print('AI Trading!')
    # pybroker_test()
    # run_alpaca_api()
    run_ai_trader()