from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)


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
