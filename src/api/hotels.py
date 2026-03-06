from typing import Annotated

from fastapi import Query, Body, Path, APIRouter
from fastapi.params import Depends

from src.api.dependencies import PaginationParams
from src.schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix='/hotels')
hotels = [
    {
        'id': 1,
        'name': 'Sochi',
        'rus_name': 'Сочи'
    },
    {
        'id': 2,
        'name': 'Dubai',
        'rus_name': 'Дубай'
    },
    {
        'id': 3,
        'name': 'spb',
        'rus_name': 'ПИТЕР'
    },
    {
        'id': 4,
        'name': 'Mscwod',
        'rus_name': 'Москва'
    },
    {
        'id': 5,
        'name': 'Sishkingrad',
        'rus_name': 'шишкинград'
    },
    {
        'id': 6,
        'name': 'Poni',
        'rus_name': 'Пони'
    },
    {
        'id': 7,
        'name': 'Woapa',
        'rus_name': 'Опа'
    },
    {
        'id': 8,
        'name': 'Stanicaa',
        'rus_name': 'Станица'
    },

]

@router.get('')
def get_hotels(
        pagination: Annotated[PaginationParams, Depends()],
        id: int | None = Query(None, description='ID отеля'),
        name: str | None = Query(None, description='Название отеля(на английском)'),
        rus_name: str | None = Query(None, description='Название отеля(на русском)')
):
    result = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        elif name and hotel['name'] != name:
            continue
        elif rus_name and hotel['rus_name'] != rus_name:
            continue

        result.append(hotel)
    if pagination.page and pagination.per_page:
        return result[(pagination.page-1) * pagination.per_page:][:pagination.per_page]
    return result

@router.delete('/{id}')
def delete_hotel(
        id: int = Path()
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != id]
    return {'status': 200}

@router.post('')
def create_hotel(
        hotel_data: Hotel = Body(openapi_examples= {
            '1': {'summary': 'Сочи', 'value': {
                'name': 'NESOHCI',
                'rus_name': 'НЕСОЧИ'
            }}
        })
):
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'name': hotel_data.name,
        'rus_name': hotel_data.rus_name
    })

    return {'status': 200}

@router.put('/{id}')
def change_hotel(
        id: int,
        hotel_data: Hotel
):
    global hotels
    find = False
    for hotel in hotels:
        if hotel['id'] == id:
            hotel['name'] = hotel_data.name
            hotel['rus_name'] = hotel_data.rus_name
            find = True

    if find:
        return {'status': 200}
    return {'status': 400}

@router.patch('/{id}',
           summary='описание',
           description='полное описание')
def partinallity_change_hotel(
        id: int,
        hotel_data: HotelPatch
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == id:
            if hotel_data.name:
                hotel['name'] = hotel_data.name
            if hotel_data.rus_name:
                hotel['rus_name'] = hotel_data.rus_name

    return {'status': 200}