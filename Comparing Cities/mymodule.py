# getdata function
def getdata(*urls):
	for i in urls:
   		return pd.read_csv(i,skiprows=4)
