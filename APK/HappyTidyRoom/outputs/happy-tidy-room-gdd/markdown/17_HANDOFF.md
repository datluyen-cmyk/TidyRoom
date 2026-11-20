# Bàn giao và điểm chưa chốt

[← Mục lục GDD](GDD.md)

Hướng game đã chốt: **level RoomSort + art Tidy Room + feeling Happy**. Tài liệu đang hoàn thiện chi tiết, chưa phải bản đã duyệt để triển khai toàn bộ game. Level Progress chưa viết; bộ level kết hợp và mapping art Tidy Room chưa được tạo.

Khi bắt đầu làm game, chia thành các bước có thể kiểm tra riêng:

| Bước | Kết quả | Điều kiện trước khi làm | Cách kiểm tra |
|---|---|---|---|
| 1 | Đọc và hiển thị một màn với art, nhãn hộp, layer và camera. | Chốt cấu trúc dữ liệu; trích xuất và ánh xạ art Tidy Room. | Kiểm tra ID, số lượng, khả năng nhận diện và C-003, C-015. |
| 2 | Thu gom, slot chờ, hoàn tất hộp và kết quả. | Chốt luật thua, ưu tiên hộp, thời điểm sức chứa và luồng chuyển động. | C-001–C-007, C-013. |
| 3 | Booster và hồi sinh. | Chốt bộ booster, đích Vacuum, kho và hiệu lực mở sức chứa. | C-008–C-012, C-014. |
| 4 | Tutorial, economy và các popup. | Chốt giá / thưởng / tim; bố trí màn phù hợp tutorial. | C-016–C-018. |
| 5 | Chuyển và cân chỉnh bộ level. | Có Level Progress được duyệt, mapping art và cấu trúc dữ liệu cuối. | Kiểm tra tính giải được và độ khó sau khi đổi art; chơi thử. |

Các bước này là thứ tự bàn giao thiết kế, không phải yêu cầu khởi tạo dự án trong phiên làm việc này. Engine, thư viện và cấu trúc mã do người triển khai chọn sau khi kiểm tra dự án. Chưa chọn thư mục dự án game hoặc nơi xuất bản build.

Hướng kết hợp không cần hỏi lại. Các điểm còn mở là luật thua áp dụng cho bộ level, quy tắc booster và các chuỗi chuyển động chưa đối chiếu; xem [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md). Trước khi triển khai một phần còn mở, phải hỏi đúng quyết định liên quan; không tự coi đề xuất là luật đã được duyệt.

Nguồn, giới hạn đối chiếu và lịch sử thay đổi nằm trong [SOURCE_MAP.md](SOURCE_MAP.md), để phần mô tả game giữ ngắn gọn.
