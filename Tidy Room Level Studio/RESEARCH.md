# Đối chiếu RoomSort và bài sinh level

Phạm vi: giữ nhịp level của RoomSort, dùng art của Tidy Room, sau này ghép feeling Happy Tidy Room. Bản studio chỉ sinh và kiểm tra câu đố.

| Nguồn | Dùng để làm gì |
|---|---|
| RoomSort · catalog `compact-v11` | 130 level cơ sở theo thứ tự đóng gói, sức chứa từng hộp và bố cục. Nhánh thử nghiệm không thay thứ tự cơ sở. |
| RoomSort · `LEVEL_ODDS` | 59 nhãn tham chiếu có sẵn. Không có log người chơi, nên không diễn giải thành tỷ lệ thắng đã quan sát. |
| RoomSort · `core/game.js`, `geometry.js`, `rules.js` | Hai hộp mở, năm slot chờ, phép thử che phủ, mở hộp kế, tự kéo đồ từ khay và điều kiện hết chỗ. |
| Tidy Room · bộ `datapack.unity3d`, sprite và `RoomItemShapes` | Ba nền, 368 mẫu đồ nhập vào tool, hình dạng và nhóm. Dáng vắt chọn riêng cho mép giường/ghế. |
| Happy Tidy Room · tài liệu thiết kế | Mốc cảm giác thao tác cho game đích. Không dùng như bằng chứng về chuyển động của tool. |

## Vì sao phải đánh dấu trên từng background?

Đối sánh ảnh thu nhỏ giữa các nền RoomSort và Tidy Room: chỉ 1/130 nền qua phép lọc sơ bộ theo cùng tỷ lệ khung hình và chênh lệch màu thấp. Xem trực tiếp mẫu đầu cho thấy phòng hoặc vị trí nội thất có thể khác hẳn. Đây là phép tìm ứng viên ảnh tương đồng, không phải phép chứng minh hai nền cùng hoặc khác hình học. Tool không mang tọa độ từ RoomSort sang. Nó chọn vị trí mới từ vùng đã vẽ trên ảnh Tidy Room và chỉ đặt sprite dáng vắt vào neo cho phép.

## Cách giữ progression

- Mốc 1: 26 đồ, 5 hộp, 5 nhóm. Mốc 2: 80 đồ, 16 hộp, 15 nhóm. Mốc 3: 209 đồ, 41 hộp, 23 nhóm. Tool giữ ba số này theo từng mốc, kể cả khi nhịp nguyên bản tăng mạnh ở đầu.
- Sức chứa của các hộp được lấy theo phân bố của từng mốc rồi đổi thứ tự. Các lần gặp lại cùng nhóm được dãn bằng một tiêu chí lấy từ dữ liệu gốc. Tỷ lệ đồ lộ, số lựa chọn vào hộp đầu và mật độ che được đo trên cả màn gốc và màn sinh.
- Tool dựng thứ tự thu gom có chủ đích trước, sau đó xếp lớp để giữ ít nhất một đường giải. Ứng viên tiếp tục qua luật nhận đồ, sức chứa và phép kiểm tra tọa độ click. Điều này đo tính giải được; không phải đường đi ngắn nhất hoặc mô hình hành vi con người.

## Bằng chứng và cách đọc

[Bộ mẫu 12 màn](batches/2026-11-20T09-39-07-460Z-seed42/levels.json) · [Bảng progression](batches/2026-11-20T09-39-07-460Z-seed42/progression.csv) · [Kiểm tra batch](batches/2026-11-20T09-39-07-460Z-seed42/validation.json) · [Lời giải bằng tọa độ](batches/2026-11-20T09-39-07-460Z-seed42/pack.json).

Chuỗi mô hình: thu thống kê từ 130 màn → đánh giá nhãn trên 59 họ nền, lần lượt giữ một họ ngoài tập học → dùng mô hình hàng xóm gần nhất để xếp hạng nhẹ, cùng kiểm tra bố cục và lời giải. Sai lệch tuyệt đối trung bình 18,166 điểm, trung vị 20,085 điểm. Đây là mức cải thiện nhỏ ở một thước đo tham chiếu; không phải chứng nhận tương đương độ khó.

**Bộ seed 42:** 12/12 màn qua cả kiểm tra bằng ID và tọa độ. Mức cao nhất trên từng đường giải nằm trong 0–4 slot chờ. Hai lượt thử tách riêng ở mốc 59 và mốc 130 cũng qua kiểm tra; chưa chạy một batch đủ cả 130 mốc trên cả ba template.

| Chiến lược kiểm tra | RoomSort (12 mốc) | Màn sinh (12 mốc) |
|---|---:|---:|
| Ưu tiên món khớp hộp, lấy món trên cùng nếu có nhiều lựa chọn | 6 thắng | 10 thắng |
| Ưu tiên hộp gần đầy và món giúp lộ mục tiêu | 3 thắng | 3 thắng |

Chiến lược thứ nhất thắng nhiều hơn trên bộ sinh, nên chưa coi độ khó ngang bản gốc dù khớp nhịp số đồ/hộp. Cả hai bot chạy cùng luật RoomSort tiêu chuẩn và biết quan hệ che phủ; kết quả chỉ dùng chẩn đoán. Ba trận thắng ở hai cột không nhất thiết là cùng ba mốc. Xem [kết quả so từng màn](batches/2026-11-20T09-39-07-460Z-seed42/pointer-audit.json).

Mẫu được kiểm tra trong Chrome: mở giao diện, chỉnh điểm vắt, khoanh vùng, khôi phục template, sinh và tải kết quả, đi từng bước lời giải, thắng một màn bằng click và dừng một lượt sinh. Các lượt thử UI nằm ngoài thư mục batch để không lẫn với bộ mẫu chính.

Điểm còn thiếu trước khi sản xuất: duyệt các nền khác; chơi đối chiếu cùng một nhóm người trên các mốc đại diện; ghi tỷ lệ thắng lần đầu, số lần hết slot, số lần thử, thời gian và phản hồi về nhận diện đồ. Các template chỉ là điểm bắt đầu để duyệt bằng mắt; bản game đích còn cần kiểm tra camera, cảm giác Happy và định dạng nhập level.
