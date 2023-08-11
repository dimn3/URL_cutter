from flask import jsonify, request, url_for

from . import app
from .consts import SHORT_FUNCTION_NAME
from .error_handlers import (
    APIException,
    GeneratedShortException,
    ShortIsBadException,
    ShortIsExistsException
)
from .models import URLMap


@app.route('/api/id/<string:short_url>/', methods=['GET'])
def get_original_link_api(short_url):
    original_link = URLMap.get(short_url)
    if original_link is None:
        raise APIException('Указанный id не найден', 404)
    return jsonify(url=original_link.original), 200


@app.route('/api/id/', methods=['POST'])
def add_link_api():
    data = request.get_json(silent=True)
    try:
        long_url = data['url']
    except TypeError:
        raise APIException('Отсутствует тело запроса')
    except KeyError:
        raise APIException('"url" является обязательным полем!')
    short = data.get('custom_id')
    try:
        link_record = URLMap().db_writer(long_url, short, do_validate=True)
    except ShortIsExistsException:
        raise APIException('Имя "{0}" уже занято.'.format(short))
    except ShortIsBadException:
        raise APIException('Указано недопустимое имя для короткой ссылки')
    except GeneratedShortException:
        raise APIException('Ошибка генерации имени, повторите попытку')
    return jsonify(dict(
        url=long_url,
        short_link=url_for(
            SHORT_FUNCTION_NAME,
            short_url=link_record.short,
            _external=True
        ),
    )), 201
