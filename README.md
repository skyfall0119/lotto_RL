# Side Project
---
### Stable Baseline 강화학습을 통한 로또 번호 예측

---
#### training 용 Cuda 환경 설정
- https://pytorch.org/get-started/locally/
- 선택한 Cuda 버전에 맞춰서 검색 후 다운로드 및 설치
- Cuda 설치 후 pytorch 에서 나온 커맨드 실행 
  - ex) pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

---

##### Env_v1
- 주어진 회차에서 다음 회차 번호 예측.
- 예측한 번호 갯수만큼 보상


##### Env_v2
- v1 과의 차이점 : 번호 5세트를 예측
- 목적 : 5000원 한세트에서 최소한 본전을 회수할 확률이 높도록
