from fastapi import APIRouter, Depends, Header
from model.item_model import ItemModel, ItemUpdateModel, ItemDeleteModel, ItemPagingViewModel
from model.item_model import ItemViewModel, ItemSearchModel
from model.main_model import ResponseModel, Meta
from dependencies import get_session
from utils import validate_jwt, decode_jwt
from fastapi.responses import JSONResponse, Response
from db.base_class import Item
from sqlalchemy.orm import scoped_session
from sqlalchemy import desc, func, select, or_, and_
from datetime import datetime

router = APIRouter(
    prefix='/items',
    tags=['items'])


@router.post('/create', summary='아이템 생성 API')
def create_items(
        request_model: ItemModel,
        db: scoped_session = Depends(get_session),
        authorizaion: str | None = Header(default=None)):
    code, status, msg = validate_jwt(authorizaion)
    if status:
        token = authorizaion
        decode_token = decode_jwt(token)
        data_dict = request_model.dict()
        data_dict['user_id'] = int(decode_token['user_id'])
        if data_dict['expiration_date']:
            data_dict['expiration_date'] = data_dict['expiration_date'].strftime('%Y-%m-%d %H:%m')
        db.add(Item(**data_dict))
        db.commit()
        code = 201
        response = ResponseModel(
            meta=Meta(
                code=code,
                message=msg),
            data=data_dict)
    else:
        response = ResponseModel(
            meta=Meta(
                code=code,
                message=msg))
    return JSONResponse(status_code=code, content=response.dict())


@router.put('/update', summary='아이템 수정 API')
def update_items(
        request_model: ItemUpdateModel,
        db: scoped_session = Depends(get_session),
        authorizaion: str | None = Header(default=None)):
    code, status, msg = validate_jwt(authorizaion)
    if status:
        token = authorizaion
        decode_token = decode_jwt(token)
        item_row = db.query(Item).filter(Item.id == request_model.id).first()
        if item_row.user_id == decode_token['user_id']:
            update_item_dict = {}
            for k, v in request_model.dict().items():
                if v is not None and k != 'id':
                    update_item_dict[k] = v
            if update_item_dict:
                db.query(Item).filter(Item.id == request_model.id).update(update_item_dict)
                db.commit()
        else:
            code = 403
            msg = '권한이 존재하지 않습니다.'
        data_dict = request_model.dict()
        data_dict['user_id'] = int(decode_token['user_id'])
        if data_dict['expiration_date']:
            data_dict['expiration_date'] = data_dict['expiration_date'].strftime('%Y-%m-%d %H:%m')
        response = ResponseModel(
            meta=Meta(
                code=code,
                message=msg),
            data=data_dict)
    else:
        response = ResponseModel(
            meta=Meta(
                code=code,
                message=msg))
    return JSONResponse(status_code=code, content=response.dict())


@router.delete('/delete', summary='아이템 삭제 API')
def delete_items(
        request_model: ItemDeleteModel,
        db: scoped_session = Depends(get_session),
        authorizaion: str | None = Header(default=None)):
    code, status, msg = validate_jwt(authorizaion)
    if status:
        token = authorizaion
        decode_token = decode_jwt(token)
        data_dict = request_model.dict()
        data_dict['user_id'] = int(decode_token['user_id'])
        items = db.query(Item).filter(Item.id == request_model.id).first().__dict__
        if items:
            if items['user_id'] == data_dict['user_id']:
                db.query(Item).filter(Item.id == request_model.id).delete()
                db.commit()
            else:
                code = 403
                msg = '권한이 없습니다.'
        else:
            code = 204
        response = ResponseModel(
            meta=Meta(
                code=code,
                message=msg),
            data=data_dict)
    else:
        response = ResponseModel(
            meta=Meta(
                code=code,
                message=msg))
    if code != 204:
        return JSONResponse(status_code=code, content=response.dict())
    else:
        return Response(status_code=204)


@router.post('/page_view', summary='유저 페이지 기반 view API')
def page_read_items(
        request_model: ItemPagingViewModel,
        db: scoped_session = Depends(get_session),
        authorizaion: str | None = Header(default=None)):
    code, status, msg = validate_jwt(authorizaion)
    if status:
        token = authorizaion
        decode_token = decode_jwt(token)
        data_dict = request_model.dict()
        data_dict['user_id'] = int(decode_token['user_id'])
        start = (data_dict['page'] - 1) * 10 + 1
        end = data_dict['page'] * 10 + 1
        if data_dict['page'] <= 0:
            code = 204
        else:
            items = db.query(Item).filter(
                Item.user_id == data_dict['user_id']).order_by(
                    desc(Item.created_at)).slice(start, end).all()
            item_list = []
            for item in items:
                item = item.__dict__
                item.pop('_sa_instance_state', None)
                for k, v in item.items():
                    if isinstance(v, datetime):
                        item[k] = v.strftime('%Y-%m-%d %H:%m:%S')
                item_list.append(item)
            if len(items) == 0:
                code = 204
        response = ResponseModel(
            meta=Meta(
                code=code,
                message=msg),
            data=item_list)
    else:
        response = ResponseModel(
            meta=Meta(
                code=code,
                message=msg))
    if code != 204:
        return JSONResponse(status_code=code, content=response.dict())
    else:
        return Response(status_code=204)


@router.post('/get_item', summary='아이템 상세내역 view Api')
def page_read_item(
        request_model: ItemViewModel,
        db: scoped_session = Depends(get_session),
        authorizaion: str | None = Header(default=None)):
    code, status, msg = validate_jwt(authorizaion)
    if status:
        token = authorizaion
        decode_token = decode_jwt(token)
        data_dict = request_model.dict()
        data_dict['user_id'] = int(decode_token['user_id'])
        item = db.query(Item).filter(   
            Item.id == request_model.id,
            Item.user_id == data_dict['user_id']).first().__dict__
        if item:
            code = 200
            item.pop('_sa_instance_state', None)
            for k, v in item.items():
                if isinstance(v, datetime):
                    item[k] = v.strftime('%Y-%m-%d %H:%m:%S')
        else:
            code = 204
        response = ResponseModel(
            meta=Meta(
                code=code,
                message=msg),
            data=item)
    else:
        response = ResponseModel(
            meta=Meta(
                code=code,
                message=msg))
    if code != 204:
        return JSONResponse(status_code=code, content=response.dict())
    else:
        return Response(status_code=204)


@router.post('/search_item', summary='아이템 초성 , 제목 검색 Api')
def search_items(
        request_model: ItemSearchModel,
        db: scoped_session = Depends(get_session),
        authorizaion: str | None = Header(default=None)):
    code, status, msg = validate_jwt(authorizaion)
    if status:
        token = authorizaion
        decode_token = decode_jwt(token)
        data_dict = request_model.dict()
        data_dict['user_id'] = int(decode_token['user_id'])
        title = '%' + request_model.title + '%'
        chosung = func.chosung(Item.product_name)
        stmt = select(Item, chosung).where(
            and_(
                or_(
                    Item.product_name.like(title),
                    chosung.like(title)),
                Item.user_id == data_dict['user_id']))
        items = db.execute(stmt).fetchall()
        item_list = []
        for item in items:
            item = item[0].__dict__
            item.pop('_sa_instance_state', None)
            for k, v in item.items():
                if isinstance(v, datetime):
                    item[k] = v.strftime('%Y-%m-%d %H:%m:%S')
            item_list.append(item)
        if len(items) == 0:
            code = 204
        response = ResponseModel(
            meta=Meta(
                code=code,
                message=msg),
            data=item_list)
    else:
        response = ResponseModel(
            meta=Meta(
                code=code,
                message=msg))
    if code != 204:
        return JSONResponse(status_code=code, content=response.dict())
    else:
        return Response(status_code=204)