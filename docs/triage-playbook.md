1. Identificazione
L'alert: due tentativi di login falliti consecutivi per l'utenza admin, alle 09:03:10 e 09:03:14 — distanziati di soli 4 secondi. Fonte: test.log (nel mondo reale sarebbe il log di autenticazione dell'app/sistema).

2. Raccolta contesto
Guardi cosa succede intorno a quell'orario: alle 09:01:12 l'utente gigi ha fatto login con successo, alle 09:02:45 c'è una lettura file legittima. Nessun'altra attività sospetta nelle righe precedenti o successive. Punto chiave che noterai in un log reale ma che qui manca: l'IP di origine — è lo stesso IP di sempre o uno nuovo/estero? E: dopo i 2 fallimenti, c'è un login riuscito per admin? (Nel nostro caso no, il log finisce lì.)

3. Valutazione
Due segnali la rendono sospetta, non solo "errore di battitura": il tempo tra i tentativi (4 secondi è troppo rapido per un umano che ridigita la password — tipico di uno script automatizzato), e il target (admin è l'account generico più preso di mira in assoluto, sia da attacchi reali che da bot automatici su internet). Con solo 2 tentativi però la severità resta bassa — non è ancora un pattern di brute force conclamato (di solito si parla di soglie come 5+ tentativi in pochi minuti).

4. Decisione
Non la chiudi come falso positivo, ma non la escali nemmeno come incidente critico: la segni come "da monitorare" — apri un ticket/nota, e se il conteggio di fallimenti su admin sale ulteriormente nelle prossime righe di log, quella diventa un'escalation a IR. Se invece subito dopo vedessi un login riuscito su admin nello stesso lasso di tempo, quella sarebbe escalation immediata (possibile compromissione riuscita).

5. Documentazione
Nota finale: "20/10, 09:03 — 2 tentativi di login falliti su account admin in 4 secondi, pattern compatibile con tentativo automatizzato di bruteforce/credential stuffing. Nessun login riuscito successivo osservato nel log disponibile. Severità: bassa-media per ora. Azione: monitorare ulteriori tentativi su questo account, verificare IP di origine se disponibile nei log reali, valutare policy di lockout dopo N tentativi falliti."
