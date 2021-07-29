from py5paisa import FivePaisaClient
import datetime 

client = FivePaisaClient(email="52119099", passwd="#bhola@1996", dob="19840101")
client.login()

# historical_data(<Exchange>,<Exchange Type>,<Scrip Code>,<Time Frame>,<From Data>,<To Date>)
end = datetime.datetime.now()
start =end - datetime.timedelta(100)

df=client.historical_data('N','C',1660,'15m',start,end)
print(df)


# req_list=[
#             { "Exch":"N","ExchType":"C","ScripCode":1660},
            
#             ]

# dict1=client.Request_Feed('mf','s',req_list)

# client.Streming_data(dict1)
