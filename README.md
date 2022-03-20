# Intall environment

```
pipenv install
pipenv shell 
```
raise the environment

# move to ecommerce

```
cd ecommerce 
```

# install migrations

```
python manage.py migrate –settings=settings.local
```

# install fixtures

```
python manage.py loaddata common/fixtures/dump.json –settings=settings.local 
```

-- This create an user: test passsword : test password
-- and product, orders, ordersdetails


# runserver

```
python manage.py runserver –settings=settings.local
```

swagger

```
http://127.0.0.1:8000/    
```

here we can see all the endpoints, to access them you must first retrieve the access token and paste it in Authorize of swagger

# Tests 

```
ecommerce$ python manage.py test --settings=settings.local
```