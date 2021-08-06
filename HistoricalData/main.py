from py5paisa import FivePaisaClient
import datetime 

client = FivePaisaClient(email="52119099", passwd="#bhola@1996", dob="19840101")
client.login()

# historical_data(<Exchange>,<Exchange Type>,<Scrip Code>,<Time Frame>,<From Data>,<To Date>)
end = datetime.datetime.now()
start =end - datetime.timedelta(100)

df=client.historical_data('N','C',999920000,'1d',start,end)
print(df)