# REQUIRED VARIABLES
main.py, DatabaseHandler.py
[SECRET_KEY]
app.secret_key = SECRET_KEY

main.py [MAIL, MAIL_PASSWORD]
uses gmail message sending api
app.config['MAIL_USERNAME'] = 'MAIL'
app.config['MAIL_PASSWORD'] = 'MAIL_PASSWORD'

DatabaseHandler.py [DB_USER, DB_PASS, DB_NAME]
self.data_modifier = DatabaseControl(host='localhost', user='DB_USER', password='DB_PASS',
                                     database='DB_NAME')

![plot](README/1.png)
![plot](README/2.png)
![plot](README/3.png)
![plot](README/4.png)
![plot](README/5.png)
![plot](README/6.png)
![plot](README/7.png)
![plot](README/8.png)
[EXAMPLE PDF](README/1.pdf)
![plot](README/9.png)
![plot](README/10.png)

