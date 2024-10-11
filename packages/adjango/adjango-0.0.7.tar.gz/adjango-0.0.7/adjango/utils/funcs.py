from __future__ import annotations

from functools import wraps
from typing import Any, Type
from urllib.parse import urlparse

from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.db.models import QuerySet, Model, Manager
from django.shortcuts import resolve_url, redirect


async def aget(
        queryset: QuerySet,
        exception: Type[Exception] | None = None,
        *args: Any,
        **kwargs: Any,

) -> Model | None:
    """
    Асинхронно получает единственный объект из заданного QuerySet,
    соответствующий переданным параметрам.

    @param queryset: QuerySet, из которого нужно получить объект.
    @param exception: Класс исключения, которое будет выброшено, если объект не найден.
                      Если None, возвращается None.

    @return: Объект модели или None, если объект не найден и exception не задан.

    @behavior:
        - Пытается асинхронно получить объект с помощью queryset.aget().
        - Если объект не найден, выбрасывает исключение exception или возвращает None.

    @usage:
        result = await aget(MyModel.objects, MyCustomException, id=1)
    """
    try:
        return await queryset.aget(*args, **kwargs)
    except queryset.model.DoesNotExist:
        if exception is not None:
            raise exception()
    return None


async def arelated(model_object: Model, related_field_name: str) -> object | None:
    """
    Асинхронно получает связанный объект из модели по указанному имени связанного поля.

    @param model_object: Экземпляр модели, у которого нужно получить связанный объект.
    @param related_field_name: Название связанного поля, из которого нужно получить объект.

    @return: Связанный объект или None, если поле не существует.

    @usage: result = await arelated(my_model_instance, "related_field_name")
    """
    return await sync_to_async(getattr)(model_object, related_field_name, None)


async def aadd(queryset: Manager, data: Any, *args: Any, **kwargs: Any) -> None:
    """
    Асинхронно добавляет объект или данные в ManyToMany поле через метод add().

    @param queryset: Менеджер модели или поле, в которое нужно добавить данные.
    @param data: Данные или объект, который нужно добавить.
    @param args: Дополнительные аргументы для метода add().
    @param kwargs: Дополнительные именованные аргументы для метода add().

    @return: None

    @usage: await aadd(my_model_instance.related_field, related_obj)
    """
    return await sync_to_async(queryset.add)(data, *args, **kwargs)


async def aall(objects: Manager) -> list:
    """
    Асинхронно возвращает все объекты, управляемые менеджером.

    @param objects: Менеджер модели, откуда нужно получить все объекты.

    @return: Список всех объектов из менеджера.

    @usage: result = await aall(MyModel.objects)
    """
    return await sync_to_async(list)(objects.all())


async def afilter(queryset: QuerySet, *args: Any, **kwargs: Any) -> list:
    """
    Асинхронно фильтрует объекты из QuerySet по заданным параметрам.

    @param queryset: QuerySet, по которому будет произведена фильтрация.
    @param args: Дополнительные позиционные аргументы для фильтрации.
    @param kwargs: Именованные аргументы для фильтрации.

    @return: Список объектов, соответствующих фильтру.

    @usage: result = await afilter(MyModel.objects, field=value)
    """
    return await sync_to_async(list)(queryset.filter(*args, **kwargs))


def auser_passes_test(test_func: Any, login_url: str = None, redirect_field_name: str = REDIRECT_FIELD_NAME):
    """
    Декоратор для представлений, который проверяет, соответствует ли пользователь переданному тесту,
    перенаправляя на страницу входа при необходимости.

    @param test_func: Функция теста, которая принимает объект пользователя и возвращает True, если тест пройден.
    @param login_url: URL страницы входа, на которую будет произведено перенаправление при провале теста.
                      Если не указано, будет использован LOGIN_URL из настроек Django.
    @param redirect_field_name: Имя поля, используемого для передачи URL перенаправления после успешного входа.

    @return: Декоратор для представления.
    """
    if not login_url: login_url = settings.LOGIN_URL

    def decorator(view_func):
        @wraps(view_func)
        async def _wrapped_view(request, *args, **kwargs):
            if await test_func(request.user): return await view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url)
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            return redirect(login_url)

        return _wrapped_view

    return decorator
