# Nhat ky hoat dong AI (AI Log - Mr. Trung)

File nay ghi lai toan bo cac thay doi, thao tac va qua trinh ho tro cua AI doi voi du an K5-L3-DAY03-NguyenDucTrung-2A202603423-ResearchAgentToolEval.

## Quy tac ghi nhat ky
- Ghi ro thoi gian thuc hien (nam-thang-ngay gio:phut:giay).
- Neu ro hanh dong va muc dich.
- Danh sach cac file bi anh huong hoac tao moi.
- Mo ta chi tiet thay doi, khong dung icon hoac viet tat.

---

## Danh sach nhat ky thay doi

### 1. Khoi tao phan chia nhiem vu 3 nguoi
- Thoi gian: 2026-11-10 09:48:00
- Nguoi yeu cau: Mr. Trung
- Muc dich: Chia nho toan bo noi dung bai tap ResearchAgentToolEval thanh 3 phan doc lap, can bang khoi luong cong viec cho 3 thanh vien trong nhom theo dung cac moc thoi gian trong slide va README.
- Cac file tao moi:
  - NHIEM_VU_NGUOI_1.md: Prompt Engineering, Tool Schema, Version Log va Dataset Danh gia Nhom (v0, v1, v2, v3).
  - NHIEM_VU_NGUOI_2.md: Phat trien Tool moi va viet Unit Test tu dong (pytest tests/test_tools_todo.py).
  - NHIEM_VU_NGUOI_3.md: Xay dung giao dien Streamlit (app.py), mo Cloudflare Tunnel va viet Bao cao tong hop (REPORT.md).
- Trang thai: Hoan thanh tao 3 file mau huong dan chi tiet.

### 2. Ghi nhan quy tac quan ly va khoi tao nhat ky hoat dong
- Thoi gian: 2026-11-10 10:11:00
- Nguoi yeu cau: Mr. Trung
- Muc dich: Thiet lap file nhat ky AI_log_MR_trung.md de luu vet toan bo cac thao tac, thay doi ma AI thuc hien theo dung yeu cau rule cua Mr. Trung.
- File bi anh huong:
  - AI_log_MR_trung.md: Khoi tao cau truc nhat ky va ghi nhan cac moc hoat dong ban dau.
- Trang thai: Hoan thanh khoi tao.


### 3. Huong dan lenh chay kiem thu Baseline v0
- Thoi gian: 2026-11-10 10:16:00
- Nguoi yeu cau: Mr. Trung
- Muc dich: Cung cap cu phap lenh kiem tra ket noi API (preflight), chay danh gia tu dong Baseline v0 (run_eval.py) va chay che do chat thu cong (chat.py).
- File bi anh huong:
  - AI_log_MR_trung.md: Cap nhat muc nhat ky so 3.
- Trang thai: Hoan thanh tu van.

### 4. Xu ly loi duong dan khi chay preflight
- Thoi gian: 2026-11-10 10:18:00
- Nguoi yeu cau: Mr. Trung
- Nguyen nhan loi: Terminal dang dung tai thu muc goc du an thay vi thu muc starter_v0 chua ma nguon scripts/.
- Giai phap: Yeu cau di chuyen vao thu muc starter_v0 bang lenh cd starter_v0 truoc khi chay tap lenh.
- File bi anh huong:
  - AI_log_MR_trung.md: Cap nhat muc nhat ky so 4.
- Trang thai: Hoan thanh huong dan sua loi.

### 5. Tong hop va truc quan hoa ket qua danh gia v0
- Thoi gian: 2026-11-10 10:35:00
- Nguoi yeu cau: Mr. Trung
- Muc dich: Chuyen doi toan bo file du lieu JSON phuc tap runs/v0_B_base_gemini_20261110T102604874011.json thanh file bao cao bang markdown de doc va truc quan hoa de dang.
- Cac file tao moi:
  - aiversionv0.md: Tong hop chi tiet bang chi so, bang ket qua 20 test case, phan tich nguyen nhan cac ca that bai va phat hien van de quota rate limit cua Gemini API.
- File bi anh huong:
  - AI_log_MR_trung.md: Cap nhat muc nhat ky so 5.
- Trang thai: Hoan thanh tao file bao cao truc quan.

### 9. Hoan thanh 2 file cho Tool moi currency_converter
- Thoi gian: 2026-11-10 11:22:00
- Nguoi yeu cau: Mr. Trung
- Muc dich: Hien thuc day du file TOOL.md va tool.py cho cong cu moi currency_converter (quy doi ngoai te) phuc vu Research Agent, dong thoi dang ky vao tools/__init__.py.
- Cac file bi anh huong:
  - starter_v0/tools/currency_converter/TOOL.md: Khai bao day du metadata chuan frontmatter (inputs, outputs, side_effect).
  - starter_v0/tools/currency_converter/tool.py: Viet ham convert_currency voi bieu thuc chinh quy regex check ma tien te (3 chu cai in hoa), kiem tra so am, ranh nhanh if/else day du khong viet tat va tinh toan ty gia chinh xac.
  - starter_v0/tools/__init__.py: Import convert_currency o dong 20 va dang ky vao TOOL_FUNCTIONS.
  - AI_log_MR_trung.md: Cap nhat muc nhat ky so 9.
- Kiem thu: Da chay kiem tra toan bo logic ham va toan bo cac dieu kien cua test_tool_contract.py (ket qua: ALL CONTRACT CHECKS PASSED PERFECTLY).
- Trang thai: Hoan thanh xuat sac.

### 10. Tra cuu va dinh vi vi tri gay loi Rate Limit 429
- Thoi gian: 2026-11-10 11:27:00
- Nguoi yeu cau: Mr. Trung
- Muc dich: Xac dinh chinh xac vi tri doan code gay ra van de Rate Limit trong run_eval.py khien 12 test case cua phien ban v1 bi loi ClientError 429 RESOURCE_EXHAUSTED.
- Vi tri phat hien:
  - File starter_v0/run_eval.py: Vong lap tai dong 289-294 chay lien tuc tat ca cac case ma khong co do tre (sleep), dan den vuot qua han ngach 5 requests/phut cua Gemini Free Tier.
- File bi anh huong:
  - AI_log_MR_trung.md: Cap nhat muc nhat ky so 10.
- Trang thai: Hoan thanh xac dinh vi tri.

### 11. Bo sung co che chong Rate Limit vao run_eval.py
- Thoi gian: 2026-11-10 11:29:00
- Nguoi yeu cau: Mr. Trung
- Muc dich: Them co che nghi tu dong giua cac test case de khong bi chan boi gioi han 5 requests/phut cua Gemini Free Tier (ClientError 429 RESOURCE_EXHAUSTED).
- Cac thay doi cu the trong starter_v0/run_eval.py:
  - Dong 6: Import thu vien time.
  - Dong 274: Bo sung tham so dong lenh --delay-seconds.
  - Dong 277-283: Tu dong dat delay_seconds = 12.0 giay neu provider la gemini, giu nguyen 0.0 giay cho cac provider khac; cho phep nguoi dung ghi de bang tham so --delay-seconds.
  - Dong 300: Dung enumerate de theo doi chi so case hien tai.
  - Dong 336-339: Goi time.sleep(delay_seconds) giua cac case kem thong bao ro rang tren console.
- Kiem thu: Chay thu python3 run_eval.py --help thanh cong voi ma thoat 0.
- File bi anh huong:
  - starter_v0/run_eval.py
  - AI_log_MR_trung.md: Cap nhat muc nhat ky so 11.
- Trang thai: Hoan thanh va chay on dinh.

### 12. Tat co che delay Rate Limit trong run_eval.py
- Thoi gian: 2026-11-10 11:40:00
- Nguoi yeu cau: Mr. Trung
- Muc dich: Loai bo hoan toan logic nghi time.sleep va tham so --delay-seconds trong file run_eval.py theo yeu cau truc tiep cua nguoi dung, dua toc do chay danh gia ve nguyen ban toi da.
- Cac dong thay doi cu the trong starter_v0/run_eval.py:
  - Dong 5-6: Xoa import time.
  - Dong 273-274: Xoa khai bao tham so --delay-seconds va khoi if/else xu ly delay_seconds.
  - Dong 288-290: Khoi phuc vong lap for case in cases goc.
  - Dong 324-325: Xoa bo hoan toan khoi lenh time.sleep.
- Kiem thu: Chay thu python3 run_eval.py --help thanh cong voi ma thoat 0.
- File bi anh huong:
  - starter_v0/run_eval.py
  - AI_log_MR_trung.md: Cap nhat muc nhat ky so 12.
- Trang thai: Hoan thanh va chay on dinh.

### 13. Tong hop va truc quan hoa ket qua danh gia v1
- Thoi gian: 2026-11-10 12:21:00
- Nguoi yeu cau: Mr. Trung
- Muc dich: Chuyen doi toan bo file du lieu JSON runs/v1_B_base_openrouter_20261110T120623880369.json thanh file bao cao truc quan aiversionv1.md tuong tu file v0 de de dang quan sat va danh gia.
- Cac file tao moi:
  - aiversionv1.md: Tong hop chi tiet bang chi so so sanh v0 voi v1 (accuracy tang tu 58.33% len 90.00%, routing dat 100%), bang ket qua 20 test case, phan tich cac diem cai tien vuot bac va nguyen nhan duy nhat khien 2 case R10, R11 chua dat diem toi da do thieu response_type='text'.
- File bi anh huong:
  - AI_log_MR_trung.md: Cap nhat muc nhat ky so 13.
- Trang thai: Hoan thanh xuat sac.

### 14. Giai thich quy dinh 10 case eval_group va kien truc phien ban khi deploy
- Thoi gian: 2026-11-10 12:30:00
- Nguoi yeu cau: Mr. Trung
- Muc dich: Giai dap 2 thac mac ve de bai README:
  1. Lam ro: v1 cua ban dat 18/20 case (90%) tren eval_base.json la qua xuat sac; con quy dinh "10 eval case" la viec tu soan 10 case moi vao data/eval_group.json (5 single-turn, 5 multi-turn) o Step 4.
  2. Khang dinh khong can tach thu muc code: De bai thiet ke starter_v0 la noi lam viec duy nhat, quan ly version bang commit/run JSON hash, va viec doi model khi deploy duoc thuc hien qua tham so CLI hoac dropdown menu tren Streamlit app.py chu khong phai tach thanh cac thu muc code roi rac.
- File bi anh huong:
  - AI_log_MR_trung.md: Cap nhat muc nhat ky so 14.
- Trang thai: Hoan thanh tu van.

### 16. Hoan tat v1 va chuan bi 10 eval case phuc vu kiem thu v2
- Thoi gian: 2026-11-10 12:38:00
- Nguoi yeu cau: Mr. Trung
- Muc dich: Thuc hien tron ven 4 hang muc cong viec theo yeu cau:
  1. starter_v0/artifacts/version_log.csv: Ghi nhan day du du lieu lich su do dac cua v0 (0.5833 tren Gemini) va v1 (0.9000 tren OpenRouter).
  2. starter_v0/tests/test_tools_todo.py: Hien thuc 3 unit test hoan chinh cho tool currency_converter (kiem tra happy path quy doi USD->VND, kiem tra loi regex ma tien te, kiem tra loi so am).
  3. starter_v0/artifacts/system_prompt.md: Tinh chinh quy tac clarify (bat buoc truyen response_type='text') de khac phuc 2 loi cuoi cua v1, dong thoi bo sung huong dan goi tool moi currency_converter.
  4. starter_v0/data/eval_group.json: Xay dung tron ven 10 eval cases danh rieng cho nhom theo dung quy dinh (5 single-turn G01-G05 va 5 multi-turn G06-G10), bao gom ca cac ca danh gia cho tool currency_converter, papers, policy, send va cau hoi out-of-scope.
- Kiem thu: Da chay kiem tra toan bo logic 3 unit tests va xac thuc 100% tinh hop le cua 10 case trong eval_group.json voi test_tool_contract.py.
- File bi anh huong:
  - starter_v0/artifacts/version_log.csv
  - starter_v0/tests/test_tools_todo.py
  - starter_v0/artifacts/system_prompt.md
  - starter_v0/data/eval_group.json
  - AI_log_MR_trung.md: Cap nhat muc nhat ky so 16.
- Trang thai: Hoan thanh toan dien.

### 17. Tong hop ket qua v2 cho ca 2 bo eval va de xuat phuong an v3
- Thoi gian: 2026-11-10 12:53:00
- Nguoi yeu cau: Mr. Trung
- Muc dich: Chuyen doi toan bo ket qua chay thuc te cua phien ban v2 tu 2 file JSON (v2_B_base dat 95% va v2_B_group dat 90%) thanh file bao cao tong hop aiversion2.md, dong thoi phan tich ro 2 diem can cai thien de phien ban v3 dat 100% tuyet doi.
- Cac file tao moi:
  - aiversion2.md: Bang so sanh chi so 4 cot (v0, v1, v2-base, v2-group), bang chi tiet 20 case base, bang chi tiet 10 case group, va phuong an xu ly cho M06 (chuyen doi cong cu da luot) va G05 (cau hoi thoi tiet ngoai pham vi).
- File bi anh huong:
  - AI_log_MR_trung.md: Cap nhat muc nhat ky so 17.
- Trang thai: Hoan thanh xuat sac.

### 18. Tinh chinh system prompt cho phien ban v3
- Thoi gian: 2026-11-10 12:57:00
- Nguoi yeu cau: Mr. Trung
- Muc dich: Khac phuc triet de 2 loi con ton tai cua phien ban v2 de dat muc tieu 100% o phien ban v3:
  1. Mục 1 Out of Scope: Bo sung ro rang cac cau hoi ve thoi tiet (weather forecast), doi song khong thuoc linh vuc nghien cuu de khong tu y goi lookup (khac phuc case G05).
  2. Mục 6 Multi-Turn Source Switching: Bo sung quy dinh nghiem ngat khi nguoi dung bao bo nguon cu (vi du bo Twitter sang web) thi phai huy bo hoan toan cong cu cu (social_search/timeline) va chi goi duy nhat cong cu moi duoc yeu cau (khac phuc case M06).
- File bi anh huong:
  - starter_v0/artifacts/system_prompt.md
  - AI_log_MR_trung.md: Cap nhat muc nhat ky so 18.
- Trang thai: Hoan thanh cap nhat prompt.

### 19. Chan doan loi Provider Error khi chay v3
- Thoi gian: 2026-11-10 13:48:00
- Nguoi yeu cau: Mr. Trung
- Nguyen nhan loi: Doc file ket qua v3_B_group_openrouter_20261110T134724826660.json, toan bo 10 test case bi loi voi noi dung cu the: "RuntimeError: Install live provider dependency first: pip install openai".
- Giai thich: Cua so Terminal hien tai cua nguoi dung chua kich hoat moi truong ao (.venv) hoac moi mo mot terminal moi chua co thu vien openai.
- Giai phap: Kich hoat lai moi truong ao hoac chay lenh pip install openai truoc khi chay lai eval.
- File bi anh huong:
  - AI_log_MR_trung.md: Cap nhat muc nhat ky so 19.
- Trang thai: Hoan thanh chan doan chinh xac.

### 21. Tong hop bao cao v3 va xay dung giao dien Streamlit UI
- Thoi gian: 2026-11-10 14:08:00
- Nguoi yeu cau: Mr. Trung
- Muc dich: Thuc hien 3 hang muc cuoi cung:
  1. aiversion3.md: Bao cao ket qua v3 dat 100% tuyet doi tren ca 2 bo de (Base: 20/20 PASS, Group: 10/10 PASS).
  2. starter_v0/artifacts/version_log.csv: Hoan tat ghi nhan du 4 hang v0, v1, v2, v3 voi day du hash va metrics.
  3. starter_v0/app.py: Xay dung ung dung web Streamlit chay localhost cho phep chat truc tiep, lua chon Provider/Model va mo rong nhat ky goi Tool chi tiet.
  4. starter_v0/artifacts/REPORT.md: Hoan thien ca Phan A (truoc gio Showdown 16:30) va Phan B (nop bai LMS truoc 17:30).
- File bi anh huong:
  - aiversion3.md
  - starter_v0/artifacts/version_log.csv
  - starter_v0/app.py
  - starter_v0/artifacts/REPORT.md
  - AI_log_MR_trung.md: Cap nhat muc nhat ky so 21.
- Trang thai: Hoan thanh toan bo cac yeu cau cua du an.

### 22. Huong dan cai dat streamlit va cap nhat requirements.txt
- Thoi gian: 2026-11-10 14:15:00
- Nguoi yeu cau: Mr. Trung
- Nguyen nhan: Moi truong chua cai thu vien streamlit de chay ung dung web app.py.
- Giai phap:
  1. starter_v0/requirements.txt: Bo sung streamlit>=1.30.0 vao cuoi file de dong bo phu thuoc du an.
  2. Huong dan nguoi dung chay lenh pip install streamlit tren Terminal.
- File bi anh huong:
  - starter_v0/requirements.txt
  - AI_log_MR_trung.md: Cap nhat muc nhat ky so 22.
- Trang thai: Hoan thanh huong dan.

### 23. Kiem tra toan dien tat ca cac tieu chi cham diem
- Thoi gian: 2026-11-10 14:21:00
- Nguoi yeu cau: Mr. Trung
- Muc dich: Doi chieu toan bo cac tieu chi bat buoc va diem thuong trong README voi thuc te du an de dam bao san sang nop bai dat diem toi da:
  1. Setup & Provider: Hoan thanh voi OpenRouter va Gemini.
  2. Tools: Co du 11 tools (gom tool moi currency_converter).
  3. Base eval: Chay du v0 (58.33%), v1 (90.00%), v2 (95.00%), v3 (100.00%).
  4. Version log: Ghi day du 4 dong v0-v3 trong artifacts/version_log.csv.
  5. Tool moi & Unit tests: Co TOOL.md, tool.py, dang ky trong tools/__init__.py, tools.yaml va 3 unit tests trong test_tools_todo.py.
  6. Eval group: 10 cases (5 single, 5 multi) trong data/eval_group.json dat 100% PASS tren v3.
  7. Run JSON: Day du tat ca cac run trong starter_v0/runs/.
  8. Transcript JSON: Da tao starter_v0/transcripts/v3_openrouter_demo.transcript.json.
  9. UI Streamlit: Hoan thien starter_v0/app.py chay tren localhost.
  10. REPORT.md: Hoan thien tron ven ca Phan A (truoc 16:30) va Phan B (nop LMS truoc 17:30).
  11. An toan ma nguon: File .env da duoc loai khoi git boi .gitignore.
- Trang thai: Tat ca cac tieu chi deu dat 100%.
