# Stick-Battle (Turn-Based PvC)

> Dự án bài tập nhóm xây dựng trò chơi **Stick-Battle đánh theo lượt (PvC - Người đấu với Máy)** bằng **Python FastAPI** và **HTML/CSS/JavaScript**, nhằm giúp cả nhóm thực hành quy trình làm việc chuyên nghiệp với **Scrum-Agile**, **Jira** và **GitHub**.

---

## 1. Mục tiêu dự án

- **Mục tiêu quy trình (Trọng tâm):**
  - Làm quen và vận hành quy trình **Scrum-Agile** (Sprint Planning, Daily Standup, Sprint Review, Sprint Retrospective).
  - Thành thạo quản lý công việc trên **Jira** (Epic, User Story, Task/Sub-task, Story Points, Scrum Board).
  - Thành thạo làm việc nhóm trên **GitHub** (Branching, Commit Convention, Pull Request, Code Review, xử lý Merge Conflict).
- **Mục tiêu sản phẩm:**
  - Hoàn thiện một web game **Stick-Battle Turn-Based PvC** chạy mượt mà, dễ chơi, tách biệt rõ ràng giữa **Backend (REST API)** và **Frontend (UI & Event Handling)**.

---

## 2. Mô tả Gameplay (Turn-Based PvC)

### 2.1. Luật chơi cốt lõi
- Người chơi điều khiển 1 chiến binh Stickman đấu lần lượt với các đối thủ do **Máy (Bot)** điều khiển qua nhiều màn chơi (từ Lính thường đến Boss).
- Trò chơi diễn ra **theo lượt (Turn-Based)**:
  1. **Lượt người chơi:** Chọn 1 trong 4 hành động:
     - **Đánh thường:** Gây sát thương cơ bản, hồi nhẹ Mana (+10 MP).
     - **Kỹ năng:** Tiêu tốn Mana (MP) để gây sát thương lớn hoặc hiệu ứng đặc biệt (ví dụ: Xuyên giáp, Đánh chí mạng).
     - **Phòng thủ:** Giảm 50% sát thương nhận vào ở lượt kế tiếp và hồi thêm Mana (+20 MP).
     - **Hồi máu:** Sử dụng bình máu (giới hạn số lần/trận) để hồi lại lượng HP cố định.
  2. **Lượt của Máy:**
     - Máy hành động theo **luật cố định đơn giản (`if/else` + ngẫu nhiên)** viết bằng Python:
       - Nếu `HP < 30%` và còn lượt hồi máu → Ưu tiên **Hồi máu**.
       - Nếu đủ Mana cho kỹ năng → Có tỷ lệ (ví dụ 40%) tung **Kỹ năng**.
       - Các trường hợp còn lại → Chọn ngẫu nhiên giữa **Đánh thường** (80%) hoặc **Phòng thủ** (20%).
  3. **Kết thúc trận & Tiến trình Leo tháp vô tận:** Bên nào có `HP <= 0` trước sẽ thua. Khi thắng một màn, người chơi nhận **Điểm Tiềm Năng** để tăng chỉ số cơ bản; riêng khi vượt qua **màn Boss** (mỗi 3 màn: Màn 3, 6, 9, ...), người chơi nhận thêm **Điểm Kỹ Năng** để nâng cấp Kỹ năng. Trò chơi **không có giới hạn số màn** — khi người chơi thất bại, **tổng số màn đã vượt qua** sẽ là **Kỷ lục** được ghi nhận trên Bảng xếp hạng.

### 2.2. Hệ thống nhân vật & Cấp độ kỹ năng (Classes & Skill Levels)
Mỗi nhân vật khởi đầu với **Skill Lv.1** và có thể nâng cấp liên tục (`Lv.1 → Lv.2 → Lv.3 → ...`) mỗi khi hạ gục một **Boss** (cứ sau mỗi 3 màn). Với cấp độ kỹ năng hiện tại là `L`:

| Nhân vật | HP | ATK | DEF | MP | Công thức Kỹ năng đặc biệt theo Level (`L`) |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Kiếm sĩ** | 120 | 18 | 8 | 50 | *Chém Xoáy (25 MP):* Gây `(180 + 25×(L-1))% ATK`. Từ `Lv.2` trở lên hồi thêm `min(25%, 5%×L)` Max HP |
| **Cung thủ** | 100 | 22 | 4 | 60 | *Tên Xuyên Phá (25 MP):* Gây `(150 + 25×(L-1))% ATK`, bỏ qua 100% DEF. Từ `Lv.2` có tỉ lệ chí mạng `min(100%, 20%×(L-1))` |
| **Pháp sư** | 85 | 25 | 3 | 100 | *Cầu Lửa (30 MP):* Gây `(190 + 25×(L-1))% ATK` + Thiêu đốt `10×L` sát thương mỗi lượt (trong 2 lượt) |

### 2.3. Cơ chế Leo tháp Vô tận & Tăng tiến Độ khó (Endless Scaling)
Người chơi xuất phát và chinh phục số màn **không giới hạn** (`Màn 1, 2, 3, ..., n`):
- **Nguyên tắc cân bằng (Tuyến tính vs. Cấp số nhân):**
  - Chỉ số của **Nhân vật** tăng **tuyến tính** (cộng cố định theo số Điểm Tiềm Năng nhận được sau mỗi màn).
  - Chỉ số của **Quái & Boss** tăng **theo cấp số nhân (exponential)** qua từng màn `n`, đảm bảo chỉ số trung bình của địch tăng nhanh hơn nhân vật để người chơi **không thể chơi vô hạn đến cuối**, buộc phải tối ưu chiến thuật và cách cộng điểm để lập kỷ lục cao nhất.
- **Công thức sinh Quái tự động ở Màn `n` (`stage_generator.py`):**
  - `HP_địch(n) = round(75 × 1.20^(n - 1))`
  - `ATK_địch(n) = round(12 × 1.16^(n - 1))`
  - `DEF_địch(n) = round(3 × 1.15^(n - 1))`
  - `MP_địch(n) = 40 + 10 × (n - 1)`
  - Số bình máu: `0` (Màn 1), `1` (Màn 2–5), `2` (từ Màn 6 trở đi).
  - Tỉ lệ Bot tung Skill khi đủ MP tăng dần theo màn: `min(70%, 25% + 5% × n)`.
- **Màn Boss (Mỗi 3 màn — `n % 3 == 0`: Màn 3, 6, 9, 12, ...):**
  - Chỉ số Boss được nhân thêm từ quái thường cùng màn: **`HP × 1.45`**, **`ATK × 1.20`**, **`DEF × 1.20`**, cộng thêm `+1 bình máu`.
  - Luật đặc biệt của Boss: Cứ mỗi **3 lượt** chắc chắn tung Skill nếu đủ MP (người chơi có thể canh lượt để bấm `Phòng thủ`).

#### Minh họa tốc độ tăng tiến chỉ số Quái / Boss
| Màn `n` | Loại đối thủ | HP địch | ATK địch | DEF địch | Ghi chú |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **Màn 1** | Quái thường | 75 | 12 | 3 | Khởi động, làm quen cơ chế |
| **Màn 3** | **Boss #1** | 157 | 19 | 5 | Vượt qua → mở **Skill Lv.2** |
| **Màn 6** | **Boss #2** | 271 | 30 | 7 | Đòi hỏi cộng điểm & phòng thủ hợp lý |
| **Màn 9** | **Boss #3** | 467 | 47 | 11 | Chỉ số địch bắt đầu vượt trội mạnh |
| **Màn 12** | **Boss #4** | 808 | 74 | 17 | Ngưỡng thử thách cực hạn lập kỷ lục |

### 2.4. Cơ chế Nâng cấp Nhân vật sau khi vượt màn
Sau mỗi màn thắng, nhân vật được hồi phục đầy HP/MP, làm mới bình máu và mở **Bảng Nâng Cấp**:
- **Điểm Tiềm Năng (Tăng tuyến tính):**
  - Vượt màn thường: nhận **+3 Điểm Tiềm Năng**.
  - Vượt màn Boss (`n % 3 == 0`): nhận **+5 Điểm Tiềm Năng**.
  - Thưởng thêm **+1 Điểm Tiềm Năng** nếu thắng mà còn trên `70% HP`.
  - Quy đổi mỗi điểm: `+15 Max HP` | `+3 ATK` | `+2 DEF` | `+10 Max MP`.
- **Điểm Kỹ Năng :** Chỉ nhận **+1 điểm** mỗi khi đánh bại **Boss** (Màn 3, 6, 9, ...), dùng để nâng cấp kỹ năng đặc biệt lên Level tiếp theo (`Lv.L → Lv.L+1`).

### 2.5. Kỷ lục & Bảng xếp hạng
- Thước đo chính của người chơi là **Kỷ lục số màn đã vượt qua (`highest_stage_cleared`)**.
- Khi hai người chơi vượt qua cùng số màn, xếp hạng phụ dựa trên **Tổng sát thương gây ra** (hoặc **Tổng số lượt ít hơn**).

---

## 3. Kiến trúc & Công nghệ

- **Backend:** Python 3.10+, **FastAPI**, Uvicorn, Pydantic (validate dữ liệu), SQLite hoặc file JSON (lưu bảng xếp hạng).
- **Frontend:** **HTML5**, **CSS3** (Flexbox/Grid, CSS Keyframe Animation cho Stickman), **JavaScript (Vanilla JS)** để bắt sự kiện người dùng và gọi API bằng `fetch()`.
- **Tài liệu API:** Tự động sinh qua Swagger UI của FastAPI (`/docs`).

### Luồng giao tiếp Client – Server
```text
[Người chơi click nút trên HTML]
        │
        ▼ (JS Event Listener + fetch API)
[FastAPI Backend: POST /api/battle/action]
        │  1. Tính sát thương lượt Người chơi
        │  2. Chạy logic Bot (rule-based) cho lượt Máy
        │  3. Cập nhật HP, MP, trạng thái thắng/thua
        ▼ (Trả về JSON kết quả lượt đánh)
[JavaScript nhận JSON]
        │  - Chạy CSS Animation (chém, trúng đòn, rung màn hình)
        │  - Cập nhật thanh HP/MP và Nhật ký trận đấu (Battle Log)
```

### Danh sách REST API chính (Dự kiến)
| Method | Endpoint | Mô tả |
| :--- | :--- | :--- |
| `GET` | `/api/characters` | Lấy danh sách nhân vật, chỉ số cơ bản và công thức Skill theo Level |
| `POST` | `/api/battle/start` | Khởi tạo lượt chơi Leo tháp mới (chọn nhân vật, bắt đầu từ Màn 1) |
| `POST` | `/api/battle/action` | Gửi hành động người chơi (`attack`, `skill`, `defend`, `heal`) và nhận kết quả cả lượt |
| `POST` | `/api/battle/upgrade` | Cộng Điểm Tiềm Năng (HP/ATK/DEF/MP), nâng Level Skill (sau khi thắng Boss) và sinh Quái cho màn tiếp theo |
| `GET` | `/api/battle/{battle_id}` | Lấy trạng thái hiện tại của trận đấu |
| `GET` | `/api/leaderboard` | Lấy danh sách Top Kỷ lục (xếp theo số màn vượt qua cao nhất) |
| `POST` | `/api/leaderboard` | Lưu Kỷ lục số màn vượt qua sau khi người chơi thất bại |

---

## 4. Cấu trúc thư mục dự án (Đề xuất)

```text
stick-battle/
├── README.md                  # Tài liệu tổng quan dự án (file này)
├── backend/                   # Mã nguồn Python FastAPI
│   ├── main.py                # Điểm khởi chạy FastAPI & cấu hình CORS
│   ├── requirements.txt       # Danh sách thư viện Python
│   ├── models/                # Pydantic schemas (Request/Response)
│   │   └── battle_models.py
│   ├── routers/               # Định nghĩa các API endpoints
│   │   ├── battle.py
│   │   └── leaderboard.py
│   ├── services/              # Logic chiến đấu, sinh màn vô tận & Bot PvC
│   │   ├── battle_engine.py
│   │   ├── bot_logic.py
│   │   └── stage_generator.py # Sinh chỉ số Quái/Boss tăng theo cấp số nhân
│   └── data/                  # Dữ liệu nhân vật, lưu kỷ lục (JSON/SQLite)
│       ├── characters.json
│       └── leaderboard.json
└── frontend/                  # Giao diện HTML + CSS + JS
    ├── index.html             # Trang chính (Chọn nhân vật & Sân đấu)
    ├── css/
    │   ├── style.css          # Layout chung, thanh HP/MP, nút bấm
    │   └── animations.css     # Hiệu ứng di chuyển, tấn công của Stickman
    ├── js/
    │   ├── api.js             # Các hàm gọi fetch() lên FastAPI
    │   ├── ui.js              # Cập nhật DOM, thanh máu, Battle Log
    │   └── main.js            # Bắt sự kiện click và điều phối game
    └── assets/                # Hình ảnh / SVG nhân vật Stickman, âm thanh
```

---
