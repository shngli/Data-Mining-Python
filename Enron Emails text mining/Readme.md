Unzip kenneth.zip to process Kenneth Lay's (former Enron CEO) 5929 emails from the lay-k folder that were made public after the accounting fraud scandal. kenneth_json.zip contains all the lay-k emails in a single lay-k.json file. Access the complete dataset containing all the 516893 emails from the Enron scandal [here](http://www.cs.cmu.edu/~enron/).

1) **folderText.py** analyzes the email folders by the emails' text body and outputs their Term Frequency - Inverse Document Frequency (TF-IDF) scores and their cosine similarity between each pair of folders. **Output**: folderText_TFIDF.txt, folderText_Cosine.txt.

2) **senderText.py** analyzes the email senders by the emails' text body and outputs their TF-IDF scores and their cosine similarity between each pair of email senders. **Output**: senderText_TFIDF.txt, senderText_Cosine.txt (Note: this file is too big to be uploaded).

3) **folderSubj.py** analyzes the email folders by the email subject lines and outputs their TF-IDF scores and their cosine similarity between each pair of folders. **Output**: folderSubj_TFIDF.txt, folderSubj_Cosine.txt.

4) **senderSubj.py** analyzes the email senders by the email subject lines and outputs their TF-IDF scores and their cosine similarity between each pair of email senders. **Output**: senderSubj_TFIDF.txt, senderSubj_Cosine.txt (Note: this file is too big to be uploaded).

5) **mr_wc_by_sender.py** processes lay-k.json and outputs the number of every term by each email sender using MapReduce. `python mr_wc_by_sender.py -o 'wc_by_sender' --no-output 'lay-k.json'` **Output**: wc_by_sender

6) **mr_per_term_idf.py** processes lay-k.json and outputs the IDFs for every term using MapReduce. `python mr_per_term_idf.py -o 'idf_parts' --no-output 'lay-k.json'` **Output**: idf_parts

7) **mr_tfidf_per_sender.py** multiplies per-sender term frequencies by per-term IDFs from the idf_parts folder and outputs the TF-IDF score per term for every email sender. Note: you need to modify the Directory. `python mr_tfidf_per_sender.py -o 'sender_tfidf' --no-output 'lay-k.json'` **Output**: sender_tfidf
