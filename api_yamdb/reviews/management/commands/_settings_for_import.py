import os

from reviews.models import (User, Genre, GenreTitle, Title,
                            Category, Comment, Review)
from api_yamdb.settings import BASE_DIR

DIR_CSV = os.path.join(BASE_DIR, 'static/data')

NEED_TO_PARSE = {
    'users.csv': User,
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Title,
    'genre_title.csv': GenreTitle,
    'review.csv': Review,
    'comments.csv': Comment,
}

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
