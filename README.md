# 84.201.152.85:8888
# LaFoodie-project

It is web app for lafoodies. For people who got awesome recipes and want to share it with other people. You can subscribe, add to favorites, add to shop list and not only this.

## Getting Started

Clone this repository. Go to root directory of this project and input command docker-compose up.

### Prerequisites

You need to install docker on your computer

### How to create super user
You need to open the console and make this command

```
docker exec -it api_yamdb_web_1 python manage.py createsuperuser
```

### How to make migrations

You need to open the console and make this command

```
docker exec -it api_yamdb_web_1 python manage.py migrate
```

## Built With

* [Django-rest-framework](http://www.django-rest-framework.org) - The web framework used

## Authors

* [Roman_Demyanov](https://github.com/RomanDamn)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
