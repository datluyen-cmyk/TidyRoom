# Quyết định thiết kế

Ngày cập nhật: 20/11/2026. Phiên bản tài liệu: 0.2. Trạng thái: drafting.

## Quyết định đã có

| ID | Trạng thái | Quyết định | Phần liên quan |
|---|---|---|---|
| D-001 | answered | Viết ngắn gọn, trôi chảy; Overview và Gameplay không chứa diễn giải kỹ thuật hoặc thuật ngữ trích xuất. | [01_OVERVIEW.md](01_OVERVIEW.md)–2 |
| D-002 | answered | Giữ các mục của mẫu GDD; chưa viết Level Progress. | [01_OVERVIEW.md](01_OVERVIEW.md)–12 |
| D-003 | answered | Layer thuộc Core Mechanic. Đồ bị đè chưa lấy được. | M-004 |
| D-004 | answered | Element chỉ là cơ chế đặc biệt bổ sung, không liệt kê thành phần cơ bản. | [04_ELEMENT.md](04_ELEMENT.md) |
| D-005 | answered | Bỏ Score / Combo vì game không có; dùng Category Object, chia theo tên hộp nhận và số asset. | [07_CATEGORY_OBJECT.md](07_CATEGORY_OBJECT.md), phụ lục |
| D-006 | answered | Giữ bối cảnh nếu hữu ích cho thiết kế level. Workbook nhóm tối đa 10 dòng / ô bối cảnh, màu nhạt và đầy đủ đường kẻ. Markdown lặp lại bối cảnh từng dòng để đọc độc lập. | Phụ lục; workbook không sửa |
| D-007 | answered | Object, Booster và Tutorial có ảnh; Tutorial ngắn gọn. | [03_OBJECT.md](03_OBJECT.md), 5, 11 |
| D-008 | answered | Camera mô tả là isometric giả lập bằng đồ họa 2D. | [01_OVERVIEW.md](01_OVERVIEW.md) |
| D-009 | answered | Tạm bỏ qua việc bổ sung Element / Booster từ RoomSort. | [04_ELEMENT.md](04_ELEMENT.md)–5 |
| D-010 | proposed | Dùng cấu trúc Happy để tích hợp và học cách RoomSort quản lý biến thể thứ tự hộp. Đây là đề xuất của trợ lý, chưa được người dùng chọn. | [15_LEVEL_DATA.md](15_LEVEL_DATA.md) |
| D-011 | answered | Phiên hiện tại chỉ viết bộ GDD Markdown bằng skill, không triển khai game. | Toàn bộ |
| D-012 | answered | Người dùng chốt: level RoomSort + art D:/APK Works/Tidy Room + feeling Happy. Thay hướng art Happy trước đây bằng art Tidy Room; Happy là mốc feeling. | Overview, Art, Animation, Level Data |
| D-013 | answered | GDD tách thành nhiều file nhỏ trong cùng folder; GDD.md là mục lục, mỗi chủ đề có file chuẩn riêng. | Toàn bộ |

## Quyết định đã trả lời và câu hỏi còn mở

Các mục sau giữ nguyên trạng thái chưa chốt. Không coi việc đã có trong workbook, đề xuất của trợ lý hoặc lựa chọn mặc định trên giao diện câu hỏi là sự duyệt của người dùng.

| ID | Quyết định cần trả lời | Lựa chọn / ảnh hưởng | Phần phụ thuộc |
|---|---|---|---|
| Q-001 | Đã trả lời: bản kết hợp nào? | **answered:** level RoomSort + art Tidy Room tại D:/APK Works/Tidy Room + feeling Happy. Không hỏi lại hướng này. | D-012 |
| Q-002 | Với bản kết hợp, khay đầy nhưng còn item lấy được để đưa thẳng vào hộp thì có thua ngay? | Luật đang mô tả theo Happy: đầy khay dẫn đến thua theo câu người dùng đã đưa. Luật RoomSort: chỉ thua khi khay đầy và không còn nước đi thẳng vào hộp. Trợ lý mới đề xuất, người dùng chưa chọn. | M-006, Lose, C-007 |
| Q-003 | Vacuum chọn hộp nào nếu có nhiều hộp chưa đầy? | Tự chọn hộp đã thu nhiều nhất như RoomSort, hoặc người chơi chọn hộp. Chưa xác lập cách của Happy. | B-001, V_06a, C-008 |
| Q-004 | Mỗi lần Extra Slot mở mấy slot, và Extra Box / Slot có giữ qua màn không? | Tách thành câu hỏi riêng theo từng tính năng khi đi đến phần này. Biết mức ban đầu 2 hộp / 5 slot, tối đa 3 hộp / 7 slot; chưa biết lượng nhận và hiệu lực. | B-003, B-004, C-010–C-011 |
| Q-005 | Kho và Revive xử lý đồ thế nào? | Cần xác định sức chứa kho, ưu tiên khay / kho / item mới và đích đến của đồ sau hồi sinh. Chưa dùng Clear trả 3 đồ về phòng của RoomSort thay cho Broom. | M-003, B-002, Revive |
| Q-006 | Khi hai hộp cùng nhận một nhóm, item được ưu tiên vào hộp nào? | Hộp gần đầy trước hoặc theo vị trí; đây là hai kết quả khác nhau, cần nguồn hoặc lựa chọn của người dùng. | M-002 |
| Q-007 | Khi item đang bay, sức chứa được tính và item phía dưới được mở lúc nào? | Chốt chuỗi chọn → rời nguồn → tới đích → cập nhật bộ đếm / hoàn thành. Cần xét chạm liên tiếp, nhận item cuối và khay đầy. | M-001–M-004, V_01–V_04, V_12 |
| Q-008 | Những chi tiết chuyển động nào cần đối chiếu Happy? | Đã chốt Happy là mốc feeling. Còn thiếu quan sát đường bay, nhịp nhận / đổi hộp, Broom / Vacuum và Lose / Revive; cần bổ sung bằng chứng chuyển động hoặc mô tả cụ thể. Không hỏi lại game tham chiếu. | V_01–V_14 |
| Q-009 | Bộ giá và phần thưởng dùng cho phiên bản mới? | Giải quyết thưởng 20/40/60 so với 30/60; giá booster; lượng tim; số revive. Không dùng giá chưa chốt để thực hiện giao dịch. | Economy |
| Q-010 | Tiếp tục lượt chơi và mở Settings có quy tắc nào? | Chốt tạm dừng, mất tim khi Retry / Quit, khôi phục giữa chuyển động và xử lý quảng cáo / mua thất bại. | M-007, UI, C-018 |
| Q-011 | Cấu trúc dữ liệu cuối theo game nào? | Có thể giữ Happy để tích hợp, hoặc schema mới khi làm lại. Chưa có mã nguồn dự án đích để kết luận chi phí tích hợp. | [15_LEVEL_DATA.md](15_LEVEL_DATA.md) |
| Q-012 | Level Progress và bộ level mới gồm bao nhiêu màn? | Deferred theo yêu cầu chưa viết Level Progress. Không tự coi 60 hoặc 130 level gốc là số màn phải sản xuất. | [06_LEVEL_PROGRESS.md](06_LEVEL_PROGRESS.md), bước bàn giao 5 |
| Q-013 | Phát hành ở đâu, dùng ngôn ngữ và bộ tài nguyên sản xuất nào? | Khi bắt đầu build mới chốt Android / nền tảng khác, ngôn ngữ, quyền dùng / thay asset và âm thanh. Tài nguyên trong bộ này là tham chiếu. | Art, SFX, xuất bản |

Q-004 và Q-005 là nhóm chủ đề lưu để tiếp tục; khi hỏi thực tế phải chia thành các quyết định đơn, không gộp một lượt hỏi nhiều hành vi độc lập.

## Trạng thái art và danh mục

Đã kiểm tra D:/APK Works/Tidy Room có Tidy-Room_57_apkcube.apks, chứa base.apk, split_UnityDataAssetPack.apk và split_config.arm64_v8a.apk. Chưa trích ảnh / catalog hoặc xem art từ gói này. Category 355 nhóm và ảnh trong tài liệu vẫn là tham chiếu Happy, không phải số lượng hoặc hình ảnh của Tidy Room.

## Vị trí tiếp tục

Đã ghi nhận Q-001 và tách bộ GDD thành các file chủ đề. Tiếp theo cần kiểm kê art Tidy Room, ánh xạ nhóm nhận với RoomSort và đối chiếu feeling Happy. Luật Lose / booster không tự được chọn chỉ từ hướng tham chiếu; chỉ hỏi tiếp 1–3 lựa chọn có ảnh hưởng tới phần đang viết. Chưa gọi bộ này là build-ready hoặc approved. Không có mặc định gameplay mới nào được tự duyệt.
