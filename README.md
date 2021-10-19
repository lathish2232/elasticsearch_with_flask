# elasticsearch_with_flask

## note:- elasticsearch index app it selfe defined and created automatically

### index name = search 
### URLS:-

```
[POST] http://localhost:5000/saved 

body :- {
  "name": "ls",
  "criteria": "scan1",
  "user_id": "test_user1"
}
[GET] http://localhost:5000/saved?id=1 

[PUT]http://localhost:5000/saved?id=1 


{
  "name": "ls",
  "criteria": "scan2_22_2",
  "user_id": "test_user1"
}


[DELETE] http://localhost:5000/saved?id=1 
```

### Note :- requirement.txt file not available please check the module imported in app
