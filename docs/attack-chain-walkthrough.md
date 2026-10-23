# Kill Chain Walkthrough — Evidenza per fase

Documento di evidenza tecnica per ogni fase dell'attacco simulato, con output reali dei comandi eseguiti contro il laboratorio (VM Kali Linux, rete privata).

---

## 1. Reconnaissance

Scansione completa delle porte e rilevamento versione dei servizi:

```bash
$ nmap -sV -p- 127.0.0.1
```

```
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 10.5p1 Debian 1 (protocol 2.0)
38261/tcp open  http    Golang net/http server
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

**Risultato**: individuato il servizio SSH come bersaglio principale (porta 22, OpenSSH 10.5p1).

---

## 2. Enumeration

Analisi degli algoritmi crittografici supportati dal servizio SSH:

```bash
$ nmap -p22 --script ssh2-enum-algos,ssh-hostkey 127.0.0.1
```

```
| ssh2-enum-algos:
|   kex_algorithms: (10)
|       mlkem768x25519-sha256
|       sntrup761x25519-sha512
|       curve25519-sha256
|       ecdh-sha2-nistp256
|       ecdh-sha2-nistp384
|       ecdh-sha2-nistp521
|   server_host_key_algorithms: (4)
|       rsa-sha2-512
|       rsa-sha2-256
|       ecdsa-sha2-nistp256
|       ssh-ed25519
|   encryption_algorithms: (6)
|       chacha20-poly1305@openssh.com
|       aes128-gcm@openssh.com
|       aes256-gcm@openssh.com
|       aes128-ctr / aes192-ctr / aes256-ctr
```

**Risultato**: configurazione SSH moderna e indurita — supporto a key exchange post-quantum (`mlkem768x25519`), nessun algoritmo legacy/debole abilitato (niente `diffie-hellman-group1`, niente cifrari CBC-only). Finding positivo da riportare, non solo vulnerabilità.

---

## 3. Exploitation

Creato un account di test temporaneo con password debole, usato esclusivamente per questo esercizio:

```bash
$ sudo useradd -m -s /bin/bash labtest
$ echo 'labtest:Summer2026' | sudo chpasswd
```

Script di brute force ([`scripts/bruteforce_exploitation.py`](../scripts/bruteforce_exploitation.py)) eseguito contro l'account:

```
[fallito] password errata: 123456
[fallito] password errata: password
[fallito] password errata: qwerty
[fallito] password errata: letmein
[successo] password corretta trovata: Summer2026
labtest
uid=1001(labtest) gid=1001(labtest) groups=1001(labtest)
Linux kali 7.1.5+kali-arm64 #1 SMP PREEMPT Kali 7.1.5-1kali1 (2026-07-29) aarch64 GNU/Linux

[fallito] password errata: changeme
[fallito] password errata: football1
```

**Risultato**: accesso ottenuto al 5° tentativo su 7, con conferma identità (`whoami`), permessi (`id`) e sistema (`uname -a`) tramite comandi eseguiti da remoto sulla sessione appena aperta.

---

## 4. Post-Exploitation / Discovery

Creato un file "sensibile" fittizio per simulare dati di valore trovati dopo l'accesso:

```bash
labtest@kali:~$ mkdir -p ~/documenti
labtest@kali:~$ cat ~/documenti/secrets.txt
CONFIDENZIALE - dati di test per il lab
Cliente: ACME Corp
Carta: 4111-XXXX-XXXX-1234 (fittizio)
```

---

## 5. Exfiltration

Trasferimento del file fittizio dalla macchina compromessa verso l'esterno (il Mac host), via SFTP ([`scripts/exfiltration_simulation.py`](../scripts/exfiltration_simulation.py)):

```
Exfiltration completata: file copiato sul Mac.
CONFIDENZIALE - dati di test per il lab
Cliente: ACME Corp
Carta: 4111-XXXX-XXXX-1234 (fittizio)
```

**Risultato**: file presente e verificato sulla macchina esterna, confermando l'esfiltrazione riuscita.

---

## 6. Cleanup

```bash
$ sudo userdel -r labtest
```

Account di test e home directory rimossi, nessuna traccia permanente lasciata sul sistema.

---

## 7. Detection (Splunk)

Tutta questa catena (tentativi falliti, login riuscito con `labtest`) è stata catturata nei log SSH esportati da `journalctl -u ssh` e caricata in Splunk, dove è visibile nella dashboard — vedi [`README.md`](../README.md#6-dashboard-splunk) per lo screenshot e le query SPL di detection.
