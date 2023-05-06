from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)


def user_1_login():
    data = json.dumps({
        'phone': '010-8738-3581',
        'password': '1234'})
    response = client.post(
        '/users/login',
        content=data)
    token_user_1 = 'Bearer ' + response.json()['data']['access_token']
    return token_user_1


def user_2_login():
    data = json.dumps({
        'phone': '010-2238-3222',
        'password': '123'
        })
    response = client.post(
        '/users/login',
        content=data)
    token_user_2 = 'Bearer ' + response.json()['data']['access_token']
    return token_user_2


class TestSignUp():
    def test_회원가입_이미_가입한_핸드폰_번호일경우(self):
        data = json.dumps({
            'phone': '010-8738-3581',
            'password': '123'})
        response = client.post(
            '/users/sign_up',
            content=data)
        assert response.status_code == 400
        assert response.json()['meta'] == {
            "code": 400,
            "message": "이미 가입한 핸드폰 번호입니다"}

    def test_핸드폰_번호에_하이픈_미포함(self):
        data = json.dumps({
            'phone': '01087383581',
            'password': '123'})
        response = client.post(
            '/users/sign_up',
            content=data)
        assert response.status_code == 400
        assert response.json()['meta'] == {
            "code": 400,
            "message": '핸드폰 번호에는 - 가 포함되어 있어야 합니다'}

    def test_올바른_핸드폰_형식이_아닐경우(self):
        data = json.dumps({
            'phone': '010-873-83581',
            'password': '123'})
        response = client.post(
            '/users/sign_up',
            content=data)
        assert response.status_code == 400
        assert response.json()['meta'] == {
            "code": 400,
            "message": '올바른 핸드폰 번호가 아닙니다'}

    def test_핸드폰_혹은_비밀번호가_빈_값일_경우(self):
        data = json.dumps({
            'phone': '',
            'password': '123'})
        response = client.post(
            '/users/sign_up',
            content=data)
        assert response.status_code == 400
        assert response.json()['meta'] == {
            "code": 400,
            "message": '아이디 또는 패스워드는 빈 값일 수 없습니다.'}


class TestLogin():
    def test_존재하지_않는_핸드폰_번호(self):
        data = json.dumps({
            'phone': '010-22538-3224',
            'password': '1223'})
        response = client.post(
            '/users/login',
            content=data)
        assert response.status_code == 401
        assert response.json()['meta'] == {
            "code": 401,
            "message": '존재하지 않는 핸드폰 번호입니다. 회원가입 해주세요!'}

    def test_비밀번호_불_일치(self):
        data = json.dumps({
            'phone': '010-8738-3581',
            'password': '122'})
        response = client.post(
            '/users/login',
            content=data)
        assert response.status_code == 401
        assert response.json()['meta'] == {
            "code": 401,
            "message": '비밀번호가 일치하지 않습니다'}


class TestItems():
    token_user_1 = user_1_login()
    token_user_2 = user_2_login()

    def test_비로그인_유저_시도시(self):
        data = json.dumps({
            "category": "커피",
            "price": 330,
            "cost": 3330,
            "product_name": "맛없는 커피",
            "product_detail": "맛없음",
            "barcode": 233320,
            "expiration_date": "2023-05-06T19:00:15.660Z",
            "size": "small",
            "id": 18
            })
        response = client.put(
            '/items/update',
            content=data,
            headers={'authorization': ''})
        assert response.status_code == 401
        assert response.json()['meta'] == {
            "code": 401,
            "message": '유효하지 않은 요청입니다. 로그인 해주세요'}

    def test_권한이_없는_유저_시도시(self):
        response = client.request(
            "DELETE",
            "http://testserver/items/delete",
            json={'id': 20},
            headers={'authorizaion': self.token_user_2})
        assert response.status_code == 403
        assert response.json()['meta'] == {
            "code": 403,
            "message": '권한이 없습니다.'}

    def test_검색시_아이템이_없을_경우(self):
        response = client.request(
            "POST",
            "http://testserver/items/search_item",
            json={'title': 'ㅋㄹㅁ'},
            headers={'authorizaion': self.token_user_2})
        assert response.status_code == 204
    
    def test_검색시_아이템이_있을_경우(self):
        response = client.request(
            "POST",
            "http://testserver/items/search_item",
            json={'title': 'ㅅㅋㄹ'},
            headers={'authorizaion': self.token_user_2})
        assert response.status_code == 200
        assert response.json()['data'] == [
            {
                "category": "커피",
                "price": 5000,
                "cost": 3000,
                "product_detail": "맛있는 슈크림 라떼",
                "size": "small",
                "updated_at": None,
                "id": 21,
                "user_id": 2,
                "product_name": "슈크림 라떼",
                "barcode": 433240,
                "expiration_date": "2023-05-06 18:05:00",
                "created_at": "2023-05-07 04:05:34"
            }]