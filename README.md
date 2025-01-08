# AI Trading
- based on YoutTube Nicholas Renotte (How to Code a AI Trading bot (so you can make $$$))
https://www.youtube.com/watch?v=c9OjEThuJjY

- code: 
https://github.com/nicknochnack/MLTradingBot

- Sentiment Analysis with BERT Neural Network and Python
https://www.youtube.com/watch?v=szczpgOEdXs

# Run
export the alpaca key and secret as env variables or 
rename the .env_template to .env and put them in there
````
export API_KEY=""
export API_SECRET=""
````
run the main.py, which creates an image file for grapht or execute via jupyter notbook, which is directly showing the image
````
python main.py
````

# Test
install pytest and run it with the test folder inside ai_trader folder
````
pytest ai_trader/test/
````

# pip upgrade requirements
to upgrade the dependencies install pur, which is iterating over the dependencies listed in the requirements.txt file
````
pip install pur
pur -r requirements.txt
pip install -r requirements.txt
````

# Trading strategies
see https://www.investopedia.com/beginner-trading-strategies-4689644

# API problems
If any problems occur to access the Alpaca API try to check via direct access, to what could be the issue
````
curl -v -X GET "https://paper-api.alpaca.markets/v2/account" -H "APCA-API-KEY-ID: ${API_KEY}" -H "APCA-API-SECRET-KEY: ${API_SECRET}"
````
