import requests
import datetime

# Copied from Walter.Sanders (whsmacon) in Dicord
# https://discord.com/channels/1018958699991138386/1019589796802351106/1204167779394129982

symph = '4bDYjxIpZHO4PjA4n56C'

payload = {
	'capital': 10000,
	'apply_reg_fee': True,
	'apply_taf_fee': True,
	'backtest_version': "v2",
	'slippage_percent': 0.0005,
	'start_date': "1970-01-01",
	'end_date': datetime.datetime.today().strftime('%Y-%m-%d') 
}
print(datetime.datetime.today().strftime('%Y-%m-%d'))
url = f"https://backtest-api.composer.trade/api/v2/public/symphonies/{symph}/backtest"

data = requests.post(url, json=payload)
jsond = data.json()

print(jsond)

# prev = 10000
# for day in sorted(jsond['dvm_capital'][symph].keys()):
# 	date_1 = datetime.datetime.strptime("01/01/1970", "%m/%d/%Y")
# 	dt = date_1 + datetime.timedelta(days=int(day))
# 	percent = ((jsond['dvm_capital'][symph][day] - prev) / prev) * 100
# 	print(dt.strftime('%Y-%m-%d')+','+str(percent))
# 	prev = jsond['dvm_capital'][symph][day]
