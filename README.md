## FastAPI를 선택한 이유

일단 현재 존재하는 Python 웹 프레임 워크 중 가벼우며 swagger UI를 통한 협업이 간편하여 골랐습니다.

## ROUTER
api_router 를 이용하여 각 domain 별로 코드를 분리하여 유지 보수와 확장에 용이하게 만들었습니다.

## pytest
pytest를 이용한 유닛 테스트를 진행하였습니다.

## pydantic
리퀘스트 별 pydantic 모델을 분리하여 확장에 유연하게 대응하게 만들었으며 datatype을 강제하여 가독성을 높였습니다

## sqlalchemy
ORM을 사용하여 DB
