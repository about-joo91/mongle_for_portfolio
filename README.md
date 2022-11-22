# 몽글 - 개인 포트폴리오

### [팀 리포지토리](https://github.com/about-joo91/mailbox_back)

## 👨🏻‍💻프로젝트 담당 작업 및 기여도

### 유저 프로필 기능 & 리뷰작성, 수정, 삭제 기능

```
DRF를 활용하여 유저 프로필을 가져와 프론트에 전달하고 수정, 삭제할 수 있는 기능을 구현하였습니다.

편지에 대한 리뷰를 작성, 수정, 삭제를 할 수 있는 기능을 구현하였고 

각각의 데이터를 더 빠르게 가져올 수 있도록 prefetch, select related 기능을 활용하여 미리 가져와 중복 쿼리가 발생하지 않도록 최적화하여 구현하였습니다.
```

[📍 편지를 가져오는 기능](https://github.com/about-joo91/mongle_for_portfolio/blob/f0ea22ff7d012e6a07ceb7925c8e5b5a58f95946/my_page/views.py#L23)[📍 리뷰작성, 수정, 삭제 기능](https://github.com/about-joo91/mongle_for_portfolio/blob/f0ea22ff7d012e6a07ceb7925c8e5b5a58f95946/my_page/views.py#L152)

### 테스트 코드 작성

```
service 레이어를 분리하여 unit test, API에 대한 E2E 테스트를 분리하여 작성하는 등
안정성 높은 코드를 위해 노력하였고 이를 통해 약 40개의 API에 대해 약 280개의 test 코드를 작성하여 
유저 피드백에서 백엔드 서버의 안정성에 대한 좋은 피드백을 얻을 수 있었습니다.
```

[📍서비스 레이어 분리](https://github.com/about-joo91/mongle_for_portfolio/blob/6efe279c5deff620d54b73e38c958e2af612c0b9/my_page/services/letter_review_service.py#L1)

[📍unit-test](https://github.com/about-joo91/mongle_for_portfolio/blob/6efe279c5deff620d54b73e38c958e2af612c0b9/my_page/tests/services/test_letter_review_service.py#L1)

[📍E2E-test](https://github.com/about-joo91/mongle_for_portfolio/blob/6efe279c5deff620d54b73e38c958e2af612c0b9/my_page/tests/api_tests/test_letter_review_api.py#L1)

### 신고 기능

```
django의 UniqueConstraint를 활용하여 유저의 중복 신고를 막았습니다.

ap스케쥴러 활용하여 상대적으로 트래픽이 적을 거라고 예상되는 매주 월요일 새벽 3시마다 신고 유저를 반영하여 is_active를 false로 만들어 제재를 가해줍니다.

주에 3번 신고당한 유저만 반영할 수 있도록  함수가 종료된 후 신고 db 테이블을 초기화해주었습니다.

기능기여도 100%

```

[📍report 모델](https://github.com/about-joo91/mongle_for_portfolio/blob/6dd01e6051a90c5317e516e43f16ab6a96dc9d75/user/models.py#L88)[📍APScheduler](https://github.com/about-joo91/mongle_for_portfolio/blob/f0ea22ff7d012e6a07ceb7925c8e5b5a58f95946/recommendation/operator.py#L20)[📍제재를 가해주는 함수](https://github.com/about-joo91/mongle_for_portfolio/blob/f0ea22ff7d012e6a07ceb7925c8e5b5a58f95946/user/services/report_service.py#L24)

### ELK 스택의 elastic search 검색기능과 logstash를 활용한 mysql데이터 옮기기

```
기존에 저장된 mysql데이터를 logstash를 활용하여 30분마다 elastic-search로 데이터를 옮겼습니다.

nori-tokenizer로 미리 스키마를 설정해두어 가장 유사한 토큰을 추천하는 검색 시스템을 만들었습니다.

python elasitc search 패키지를 활용해 :9200/_search를 이용자가 쓰게 만드는 것이 아니라 api로 이용할 수 있도록 구현하였습니다.

기여도 100%
```

[📍logstash config](https://github.com/about-joo91/mongle_for_portfolio/blob/f0ea22ff7d012e6a07ceb7925c8e5b5a58f95946/logstash/pipeline/logstash.conf#L1)

### 도커 - 도커 컴포즈 활용  CI/CD

```
몽글 프로젝트에서는 테스트 코드를 상당히 중요하게 생각했으므로 작성한 테스트 코드가 푸시 할 때 자동으로 돌아 갈 수 있도록 하자는 요구가 생겼습니다.

추가로 ec2 서버에 계속 접속해 git pull 혹은 docker pull을 받지 말고 지속적인 배포 기능도 추가하고 싶다는 욕구도 생겼습니다.

무료로 CI 기술을 시도해 볼 수 있는 github actions를 활용하여 run-test ⇒ build-image ⇒ continuos deploy 순으로 이어지는 CI / CD 파이프라인을 완성하였습니다.

도커 컴포즈를 다중 컨테이너를 제어하고 이미지를 빌드하였고 그 이미지를 도커헙에 올려 빌드한 이미지를 배포환경에 바로 pull을 받아 배포할 수 있도록 하였습니다.
```

[📍 docker-compose.yml](https://github.com/about-joo91/mongle_for_portfolio/blob/f0ea22ff7d012e6a07ceb7925c8e5b5a58f95946/docker-compose.prod.yml#L1)

[📍 ci-cd-pipline.yaml](https://github.com/about-joo91/mailbox_back/blob/6e37b99b33c69163adcef45ea029be1d1c9e3eaa/.github/workflows/mail_box_pipeline.yaml#L1)

### 그밖의 것들

AWS ec2를 활용한 배포

[📍 패키지 호환 문제를 디버그모드로 찾아내 직접 패키지를 수정했습니다.](https://github.com/about-joo91/mongle_for_portfolio/blob/f0ea22ff7d012e6a07ceb7925c8e5b5a58f95946/webpush/views.py#L12)

<br>
<br>

## 🤩 만족스러운 코드

### 계속 이어질 뻔했던 분기문을 이분탐색으로 깔끔하게!

```python
## 이전 코드
if 0 <= grade < 200:
  mongle_level = 1
elif 200 <= grade < 600:
  mongle_level = 2
elif 600 <= grade < 1200:
  mongle_level = 3
elif 1200 <= grade < 2500:
  mongle_level = 4
else:
  mongle_level = 5

## 고친 이후
from bisect import bisect_left

MONGLE_GRADE_BISECTS = [199, 599, 1199, 2499]

def update_mongle_level(cur_grade: int) -> int:
  return bisect_left(MONGLE_GRADE_BISECTS, cur_grade) + 1

```

[📍 코드 링크](https://github.com/about-joo91/mongle_for_portfolio/blob/41ccf9d6cf555351a7563d53901ddb8f734431e0/my_page/services/letter_review_service.py#L16)

### 원자성을 위한 atomic 데코레이터

리뷰를 쓸 때마다 점수가 올라가야 했고 이때 리뷰는 써졌으나 점수는 올라가지 않는 상황을 상정하여 atomic 데코레이터를 통해 이를 방지하였습니다.

```python

@transaction.atomic
def create_letter_review(user: UserModel, letter_id: int, review_data: dict[str, str]) -> None:
    target_letter = (
        LetterModel.objects.select_related("worryboard__author")
        .select_related("letter_author__monglegrade")
        .get(id=letter_id)
    )
    if target_letter.worryboard.author == user:
        letter_review_serializer = LetterReviewSerializer(data=review_data)
        letter_review_serializer.is_valid(raise_exception=True)

        letter_author = target_letter.letter_author
        update_mongle_grade(user=letter_author, grade=int(review_data["grade"]), rate_type="review")
        letter_review_serializer.save(review_author=user, letter=target_letter)
    else:
        raise PermissionError

```

[📍 코드 링크](https://github.com/about-joo91/mongle_for_portfolio/blob/f0ea22ff7d012e6a07ceb7925c8e5b5a58f95946/my_page/services/letter_review_service.py#L33)

### 기존 장고-웹푸시 패키지의 FBV를 CBV로

- 팀원이 장고 웹 푸시를 통해 알림이 오는 기능을 일부 구현하였으나 프런트에서 요청은 가는데 뭐가 문제인지 어떻게 풀어야 할지 모르겠다고 도움을 요청하였습니다.
- vscode 디버그 모드를 통해서 어떤 함수에서 문제가 발생하는지 패키지 단까지 들어가서 확인을 해보았고
- 장고 내장함수인 is_authenticate 인증 함수가 프로젝트의 JWT 토큰 인증 방식을 받아들이지 않아서 로그인 된 유저를 anonymous user로 받아들이고 있었습니다.
- 프로젝트에 적용시킨 JWT-simple 패키지는 drf에 맞게 만들어진 패키지이므로 그 인증 방식을 클래스 안에서 제어합니다.
- 따라서 기존 FBV로 구성된 패키지를 커스텀 하여 문제를 해결할 수 있었습니다.

[📍 코드 링크](https://github.com/about-joo91/mongle_for_portfolio/blob/41ccf9d6cf555351a7563d53901ddb8f734431e0/my_page/services/letter_review_service.py#L16)

### 보안을 위해서 쉘 파일을 만들어 도커 파일이 빌드될 때 logstash keystore에 저장

- 기존의 호스트 정보나 db 비밀번호 정보를 .env 파일로 만들어 정리하고 있었습니다.
- github actions로 이미지를 빌드 하기 때문에 logstash.conf파일을 깃헙에 올릴 수밖에 없는 상황에서
- 비밀번호를 지킬 수 있는 수단을 찾기 위해서 [엘라스틱 서치 공식문서](https://www.elastic.co/guide/en/logstash/current/keystore.html)에서 logstash kyestore라는 것을 찾았고
- 이를 적용시키기 위해서 도커 이미지를 빌드 할 때 shell 파일을 만들어 실행시키면 되겠다고 생각해 적용시켜 보안을 지킬 수 있었습니다.

[📍 코드 링크](https://github.com/about-joo91/mongle_for_portfolio/blob/41ccf9d6cf555351a7563d53901ddb8f734431e0/logstash/log_stash_keystore.sh#L1)

<br>
<br>

## 🏃🏻 문제와 해결책들

### ✋ 사용하지 않는 import 실수로 인해 맞지 않는 인덴트 등 휴먼오류로 인해 지속적으로 오류가 발생

→ 휴먼 오류를 줄이기 위해서는 가장 기본적인 것부터 시작해야 한다고 생각되어서

→ 첫 시도는 push가 발생하면 자동으로 black으로 코드를 변환한 다음 pr을 생성하려고 했으나 너무 많은 pr이 생성되는 부작용을 낳았고

→ pre-commit을 다운로드하고 커밋 할 때마다 black, isort로 파이썬 린트를 통일시키고 flake8을 통해 불필요한 import문이나 white space를 제거할 수 있도록 하였습니다.

### ✋ 엘라스틱 서치를 적용 및 기존 mysql데이터의 처리

→ 서비스 특성상 sql의 Like를 활용한 정확한 단어 검색보다는 유사한 단어 검색 혹은 추천 검색어 기능이 필요하다는 판단하에 Elastic Search를 서비스에 적용하기로 결정하였습니다.

→ 엘라스틱 서치를 적용하기 위해서는 기존 mysql데이터를 Elastic Search에 옮길 필요가 있었습니다.

→ 엘라스틱 서치 공식 블로그에 들러 [logstash와 JDBC를 사용해 RDBMS의 동기화를 유지하는 방법](https://www.elastic.co/kr/blog/how-to-keep-elasticsearch-synchronized-with-a-relational-database-using-logstash) 을 찾아 읽은 후 매 30분 마다 주기적으로 mysql의 데이터가 동기화될 수 있도록 설정하였습니다.

→ 또한 nori_tokenizer를 활용해 역인덱싱이 가능하게 하여 기존에 원하던 추천 검색 기능이 가능하도록 구현하였습니다.

### ✋ 빠르게 적용시켜야 했던 DRF

→ [미니 프로젝트를 만들어 팀원들이 성장할 수 있도록 도움을 제공](https://www.notion.so/b55bf70cbbca4224868b0bd3169f8742)

→ [6.16 팀원 타임어택 진행](https://www.notion.so/9c0adb338c8041e5acf3298dc5c6f88b)

→ [6월 20일 타임어택](https://www.notion.so/11b2ab4c43c94f32b67a7bbedee78dce)

→ [6/21일 CRUD_further](https://www.notion.so/f90a6ac8a0724f7a96f9d17435583834)

→ [https://github.com/about-joo91/1TA3P_timeattack](https://github.com/about-joo91/1TA3P_timeattack)

### ✋ 쿼리 최적화 도중 발견한 유독 느린 쿼리

→ 전체 쿼리 로그를 보며 최적화를 하던 도중 메인페이지에 필요한 데이터를 union으로 묶어 가져오는 부분에서 속도 저하가 발생하는 것을 발견했습니다. (평균 0.01초인 다른 쿼리들에 비해 0.3초로 매우 느린속도라고 판단이 되었습니다.)

→ 이를 해결하기 위해서 어떻게 성능을 개선할지 팀원들과 회의 끝에 쿼리를 미리 캐싱해두면 속도면에서 향상을 보이겠다는 생각을 해냈습니다.

→ 그러나 MySQL의 쿼리 캐싱기능은 5버전대 이후로 사라진 기능이라는 것을 알게 되었고 인메모리 데이터베이스인 Redis를 활용하면 개선할 수 있으리라 생각했고 Redis 적용을 통해서 쿼리 속도를 0.01초로 줄일 수 있게 되었습니다.

### ✋ 일주일간의 실 사용 피드백

→ 대부분 페이지의 가시성이나 사용성 불편에 대한 피드백이 많았으며

→ 반응형 페이지 제작, 사이트를 설명하는 튜토리얼 페이지 제작

→ 폰트 크기 반응형으로 변경 등 페이지를 조금 더 사용자 친화적이게 변경하였습니다.
