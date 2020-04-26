# Distributed Albums Ratings

**Python REST API using flask and SQL**

### Usage:
## **Run Server:**
```python server.py```

**Available HTTP Requests:**
```
'/utilizadores', methods = ["POST"]
'/utilizadores/ALL', methods = ["GET", "DELETE"]
'/utilizadores/ALL/<int:id>', methods = ["GET","DELETE"]
'/utilizadores/<int:id>', methods = ["GET", "DELETE", "PUT"]

'/bandas', methods = ["POST"]
'/bandas/<int:id>', methods = ["GET", "DELETE"]
'/bandas/ALL', methods = ["GET", "DELETE"]
'/bandas/ALL/<int:id>', methods = ["GET"]

'/albuns', methods = ["POST"]
'/albuns/ALL', methods = ["GET", "DELETE"]
'/albuns/ALL/RATE', methods = ["GET", "DELETE"]
'/albuns/RATE/<int:id>', methods = ["PUT"]
'/albuns/<int:id>', methods = ["POST","GET", "DELETE"]
'/albuns/ALL/<int:id>', methods = ["GET", "DELETE"]
```

## **Run Client:**
```python cliente.py```

**Client Commands:**
```
ADD USER <nome> <username> <password>
ADD BANDA <nome> <ano> <genero>
ADD ALBUM <id_banda> <nome> <ano album>
ADD <id_user> <id_album> <rate>
SHOW\REMOVE USER <id_user>
SHOW\REMOVE BANDA <id_banda>
SHOW\REMOVE ALBUM <id_album>
SHOW\REMOVE ALL <USERS | BANDAS | ALBUNS>
SHOW\REMOVE ALL ALBUNS_B <id_banda>
SHOW\REMOVE ALL ALBUNS_U <id_user>
SHOW\REMOVE ALL ALBUNS <rate>
UPDATE ALBUM <id_user> <id_album> <rate>
UPDATE USER <id_user> <password>
```
