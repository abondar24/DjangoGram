#DjangoGram

Django demo project based on [YouTube course](https://www.youtube.com/watch?v=xSUm6iMtREA&list=PLj-dJy-nCFS2r1hniPVaarBM_xJwnwFU5).

Templates are used [from this repo](https://github.com/tomitokko/django-social-media-template)

## Todo

- Implement post deletion
- Implement post editing
- Implement post sharing
- Refactor the code in views
- Fix session store clearing after logout
- Implement comments
- Implement comments disabling

## RUN
- Run server
```
python manage.py runserver
```

- Additional commands for migrations
```
python manage.py migrate

python manage.py makemigrations
```

- Create admin user(for localhost:8000/admin)
```
python manage.py createsuperuser
```
