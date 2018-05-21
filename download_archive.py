import requests
import pickle
import time

tickers = pickle.load(open("tickers.pkl"))
def get_session():
  s = requests.Session()
  res = s.get("https://finance.yahoo.com/")
  print "Initial session status:", res.status_code
  prefix = '"user":{"crumb":"'
  start_index = res.content.find(prefix) + len(prefix)
  crumb_len = res.content[start_index:].find('"')
  crumb = res.content[start_index: start_index + crumb_len]
  print "Crumb 1:", crumb
  time.sleep(1)
  res = s.get("https://finance.yahoo.com/quote/MAHLOG.NS?p=MAHLOG.NS")
  time.sleep(1)
  res = s.get("https://finance.yahoo.com/quote/MAHLOG.NS/history?p=MAHLOG.NS")
  prefix = '"user":{"crumb":"'
  start_index = res.content.find(prefix) + len(prefix)
  crumb_len = res.content[start_index:].find('"')
  crumb = res.content[start_index: start_index + crumb_len]
  print "Crumb 2:", crumb
  return s, crumb


s, crumb = get_session()

for t in tickers:
  try:
    url = "https://query1.finance.yahoo.com/v7/finance/download/%s.NS" % t
    params = {
      "period1": 820434600,
      "period2": 1526922417,
      "interval": "1d",
      "events" : "history",
      "crumb": crumb
    }
    res = s.get(url, params=params)
    print t, res.status_code, url
    if res.status_code == 200:
      f = open("raw/" + t + ".csv", "wb")
      f.write(res.content)
      f.close()
    time.sleep(2)
  except Exception as e:
    print t, e
    s, crumb = get_session()
