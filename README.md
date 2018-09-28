Initialize
---

```
docker run -p 5000:5000 -e password=super_secret -v "$(pwd)/data:/app/data" adamyordan/dumper
```


Usage
---

- Dump data at `/dump/`
    ```
    $ curl http://localhost:5000/dump?e=<your_data>
      or
    $ curl -X POST --data "<your_data>" http://localhost:5000/dump/
    ```
- View list of dumped data at `dump/result/`
    ```
    $ curl --user admin:super_secret http://localhost:5000/dump/result/
    <a href=/dump/result/2018-09-28-070726.vj73.txt> 2018-09-28-070726.vj73.txt </a><br>
    
    $ curl --user admin:super_secret http://localhost:5000/dump/result/2018-09-28-070726.vj73.txt
    <your_data>
    ```
