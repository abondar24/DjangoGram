#DjangoGram

Django demo project based on [YouTube course](https://www.youtube.com/watch?v=xSUm6iMtREA&list=PLj-dJy-nCFS2r1hniPVaarBM_xJwnwFU5).

Templates are used [from this repo](https://github.com/tomitokko/django-social-media-template)

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


<!--                                                    <li>-->
<!--                                                        <a href="#" class="flex items-center px-3 py-2 hover:bg-gray-200 hover:text-gray-800 rounded-md ">-->
<!--                                                            <i class="uil-share-alt mr-1"></i> Share-->
<!--                                                        </a>-->
<!--                                                    </li>-->
<!--                                                    <li>-->
<!--                                                        <a href="{% url 'edit_post' post.id %}" class="flex items-center px-3 py-2 hover:bg-gray-200 hover:text-gray-800 rounded-md ">-->
<!--                                                            <i class="uil-edit-alt mr-1"></i> Edit Post-->
<!--                                                        </a>-->
<!--                                                    </li>-->
<!--                                                    <li>-->
<!--                                                        <a href="{% url 'disable_comments' post.id %}" class="flex items-center px-3 py-2 hover:bg-gray-200 hover:text-gray-800 rounded-md ">-->
<!--                                                            <i class="uil-comment-slash mr-1"></i> Disable comments-->
<!--                                                        </a>-->
<!--                                                    </li>-->
<!--                                                    <li>-->
<!--                                                        <hr class="-mx-2 my-2 ">-->
<!--                                                    </li>-->