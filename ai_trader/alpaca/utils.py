from datetime import datetime
import os

def collect_creds():
  # API_KEY = os.getenv("API_KEY")
  # API_SECRET = os.getenv("API_SECRET")

  # check if file .env exists, then load it
  if os.path.exists(".env"):
    from dotenv import load_dotenv, dotenv_values
    load_dotenv()

  API_KEY = os.getenv("API_KEY")
  API_SECRET = os.getenv("API_SECRET")
    

  ALPACA_CREDS = {
    "API_KEY":API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True
  }
  return ALPACA_CREDS



# # crypto()
# btc_bars=get_stocks_data()
# # Convert to dataframe
# print(btc_bars.df)


