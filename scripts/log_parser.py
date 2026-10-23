c = 0
with open ("test.log", "r") as f:
	for riga in f :
		if "failed" in riga:
			c += 1
			print(riga, end="")
print (f"Eventi failed trovati :{c} ");
