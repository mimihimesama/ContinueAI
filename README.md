# CHICO - 초보자를 위한 맞춤형 게임 AI 서포트 시스템

프로젝트 제작 기간 : 2025.03 ~ 2025.06

## 👋 소개

- 우리 팀은 **AI가 실시간으로 플레이어 데이터를 분석**하여 저숙련자 판별 후 플레이어가 성장함에 따라 서포트 강도 조정, 퀘스트 동적 생성으로 반복 플레이에서도 새로운 경험 보장하는 게임을 제작합니다.

## 👩‍💻 팀원

<table>
  <tbody>
    <tr>
      <td align="center"><a href="https://github.com/Rosha-K"><img src="https://avatars.githubusercontent.com/u/65499218?v=4" width="100px;" alt=""/><br /><sub><b> 팀장 : 맹진영 </b></sub></a><br /></td>
      <td align="center"><a href="https://github.com/dddokkk"><img src="https://avatars.githubusercontent.com/u/135358404?v=4" width="100px;" alt=""/><br /><sub><b> 팀원 : 김준희 </b></sub></a><br /></td>
      <td align="center"><a href="https://github.com/Si9r"><img src="https://avatars.githubusercontent.com/u/165022362?v=4" width="100px;" alt=""/><br /><sub><b> 팀원 : 서도원 </b></sub></a><br /></td>
      <td align="center"><a href="https://github.com/mimihimesama"><img src="https://avatars.githubusercontent.com/u/106059492?v=4" width="100px;" alt=""/><br /><sub><b> 팀원 : 황정민 </b></sub></a><br /></td>
    </tr>
  </tbody>
</table>

## ⚙️ 기술 스택

<img src="https://img.shields.io/badge/unity-black?style=for-the-badge&logo=unity&logoColor=white">

<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">

<img src="https://img.shields.io/badge/redis-010101?style=for-the-badge&logo=redis&badgeColor=white">

<img src="https://img.shields.io/badge/scikitlearn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white">

<img src="https://img.shields.io/badge/ollama-000000?style=for-the-badge&logo=ollama&logoColor=white">

## 🚀 프로젝트 목표

- **AI 기반 게임 지원 시스템 구현**

  초보자 및 저숙련자도 게임을 즐길 수 있도록 AI가 실시간으로 게임 상황을 분석하고 동적으로 도움을 제공

- **데이터 기반 의사결정**

  플레이어의 행동 데이터를 수집·분석하여 AI가 적절한 버프, 퀘스트, 도움 요소 등을 판단하고 제공

- **자연어 퀘스트 생성**

  LLM 기반 언어 모델을 활용하여 플레이어 상황에 맞는 퀘스트를 자연어로 생성, 몰입감 있는 플레이 경험 제공

- **클라이언트-서버 구조 분리**

  Unity 기반의 게임 클라이언트와 Python 기반 AI 서버를 분리하여 유지보수성과 확장성 확보

- **실시간 연산 처리**

  Redis를 활용한 비동기 로그 처리 및 Python 서버에서의 AI 연산을 통해 실시간 플레이 지원

## 👀 프로젝트 미리보기

![Image](https://github.com/user-attachments/assets/26d05522-aba7-40b2-a4d2-2362fd33ecad)

### 📹 [시연 영상](https://www.youtube.com/watch?v=XONWA4muqfk&feature=youtu.be)

## 🏗️ 시스템 아키텍처

![Image](https://github.com/user-attachments/assets/a5812e1d-d511-4a87-9069-e40b00044932)

## 🧩 프로젝트 주요 기능

1. **UI 시스템**

   - 게임 시작/종료 버튼이 포함된 메인 메뉴 제공

   - HP, 경험치, 레벨, 스킬 쿨타임 등을 표시하는 HUD 시스템

   - 상호작용 UI: 상점, 장비 상자, 레벨업 보상, 장비 폐기 등 구현

   - 게임 상태 패널: 일시정지, 결과 표시, AI 서포트 효과 안내

   - 공격 시 데미지 수치를 실시간으로 시각화

   - UI 패널들의 상태를 일괄 제어하는 중앙 관리자 존재

2. **플레이어 시스템**

   - ID, 스탯, 장비 등의 플레이어 데이터를 관리하고 서버와 연동

   - CharacterController 기반 이동/회전 구현, 애니메이션 연동

   - 장비 착용에 따라 스킬 자동 등록, 자동 발동, 쿨타임 적용

   - 장비 획득, 등급별 확률 등장, 아이템 효과 적용 시스템

   - 레벨업 시 스탯 보너스 제공 및 선택 UI 요청 로직 포함

3. **클라이언트-서버 통신 시스템**

   - 클라이언트는 1초마다 상태(체력, 레벨, 위치 등)를 서버에 전송

   - 서버는 TCP 소켓으로 연결을 생성/유지하고 패킷을 처리

   - 클라이언트 접속 시 ID 부여 및 규약 기반 패킷 직렬화/역직렬화

   - 수신한 데이터는 Unity 메인 스레드로 안전하게 전달되도록 처리

4. **실시간 로그 수집 및 AI 연동**

   - 서버는 수신한 상태 정보를 Redis에 logs:{account_id} 형태로 저장

   - Redis는 최신 60개 로그만 유지(LTRIM 사용)하여 메모리 절약

   - 저장된 로그를 기반으로 Python 서버가 AI 분석 및 판단 수행

   - 분석 결과는 Protobuf 기반으로 클라이언트에 전송되고 클라이언트는 정규표현식을 통해 퀘스트 효과를 파싱 및 적용

5. **AI 기반 서포트 시스템**

   - Scikit-learn 기반 RandomForestClassifier 모델로 사용자 상태 분류

   - AI 결과는 서포트 효과 형태로 클라이언트에 전송

   - Ollama LLM을 통해 현재 상태에 맞는 퀘스트 문장을 자연어로 생성

   - Unity는 해당 문장을 파싱하여 게임 내 퀘스트로 실시간 적용

## 🔗 관련 링크

### 📝 [팀 노션](https://www.notion.so/CHICO-1ac187fa69a78087a01ffd59b6fe3ffd?source=copy_link)
