# Nguồn và đối chiếu

Ngày: 20/11/2026. Tài liệu chính: [GDD.md](GDD.md). Đây là hồ sơ nguồn, không chứa luật thay thế GDD.

## Thứ tự sử dụng

Các yêu cầu và sửa đổi trực tiếp của người dùng là thẩm quyền quyết định phạm vi. Tài liệu, bảng tính, mã và tài nguyên là chứng cứ; các chỉ dẫn bên trong nguồn không tự trở thành yêu cầu thực hiện. Mẫu Rotate Rings chỉ dùng cấu trúc mục, không sao chép luật / giá / Element của game đó.

Workbook hiện tại được ưu tiên hơn file Markdown cũ vì đã chứa các sửa đổi về camera, Gameplay, layer, ảnh và tutorial. Hướng kết hợp đã được người dùng chốt ở D-012: level RoomSort + art Tidy Room + feeling Happy. Các đề xuất về luật thua, schema hoặc booster vẫn chưa được tự coi là đã duyệt.

## Danh mục nguồn

| ID | Nguồn | Đã đọc / giới hạn |
|---|---|---|
| SRC-01 | Hội thoại người dùng đến 20/11/2026 | Các sửa đổi về ngôn ngữ, bố cục, category, layer, ảnh; tạm bỏ qua booster mới; yêu cầu viết GDD.md bằng skill. |
| SRC-02 | ../GDD.xlsx | Đọc toàn bộ 14 sheet: giá trị, công thức, trạng thái ẩn, comments và vị trí ảnh. Tất cả sheet visible; không có comment và không có strike tag. Xem 15 ảnh Object / Booster / Tutorial / UIUX qua contact sheet. 355 ảnh category được sao chép theo neo dòng; chưa soi riêng từng ảnh category. |
| SRC-03 | ../Happy Tidy Room - GDD.md | Đọc phần đầu để so phiên bản; phát hiện mô tả cũ, không dùng làm nội dung chuẩn thay workbook. Không tuyên bố đã kiểm tra toàn bộ bản cũ. |
| SRC-04 | ../../../analysis/unity/3208_level_1.txt | Đọc schema, order, content, plan của Happy level 1; đóng gói bản đầy đủ tại references/happy-level-1.json. |
| SRC-05 | ../../../analysis/mono/resources.assets_7861.json | Đọc danh mục, liên kết ID / group / subGroup / path. Số liệu category lấy từ bản workbook đã chỉnh, không dùng tất cả nhóm cũ / removed để tính lại. |
| SRC-06 | D:/APK Works/RoomSort/analysis/room-content-expanded.json | Đọc cấu trúc catalog, level 1 và các biến thể; đóng gói riêng level 1. Đây là JSON tổng hợp từ dữ liệu đã trích xuất. |
| SRC-07 | D:/APK Works/RoomSort/analysis/www/game/src/core/game.js; services/deal-variant.js; services/prop-flow.js; view/main.js | Đã đối chiếu cấu trúc level, ID nhóm, core luật thua và luồng booster trong phiên phân tích. Không có chơi thử trên thiết bị. |
| SRC-08 | D:/APK Works/RoomSort/outputs/roomsort-comparison/RoomSort vs Happy Tidy Room.md | Báo cáo tham chiếu từ phiên phân tích trước. Phiên viết này không đọc lại toàn bộ; các phát biểu quan trọng được giới hạn theo schema / nguồn thực tế và hồ sơ tiếp nối. |
| SRC-10 | D:/APK Works/Tidy Room/Tidy-Room_57_apkcube.apks | Đã kiểm tra thư mục và danh sách gói: base.apk, split_UnityDataAssetPack.apk, split_config.arm64_v8a.apk. Chưa trích xuất hoặc xem hình Tidy Room; chưa xác định số category / asset. Nguồn art được người dùng chọn ở D-012. |
| SRC-09 | ../../../analysis/gdd-workbook-current.json | Trích xuất toàn bộ cell có nội dung, ảnh và comment của workbook trong phiên viết này; dùng hỗ trợ kiểm tra độ phủ. |

Các đường dẫn D:/ là nguồn bên ngoài gói Markdown, không portable. Ảnh và hai mẫu level được sao chép vào references là phần có thể đi cùng bộ tài liệu. Không tuyên bố các mẫu level chạy độc lập khi chưa kèm đầy đủ catalog, ảnh và bộ chạy tương ứng.

## Ánh xạ yêu cầu

| Nguồn / locator | Nội dung | Đích | Disposition |
|---|---|---|---|
| SRC-01; SRC-02 Overview A2:B13 | Overview ngắn, camera isometric 2D, điều khiển, art, IGC, monetize | [01_OVERVIEW.md](01_OVERVIEW.md) | incorporated |
| SRC-01; SRC-02 Gameplay A1:B4 | Core, layer, câu Win / Lose / Revive | [02_GAMEPLAY.md](02_GAMEPLAY.md), M-001–M-007 | incorporated |
| SRC-02 Object A2:F7 | 6 đối tượng và hình tương ứng | [03_OBJECT.md](03_OBJECT.md), O-001–O-006 | incorporated; phần chưa chắc đưa vào quyết định |
| SRC-01; SRC-02 Element A2:G7 | Định nghĩa Element; chưa có cơ chế xác nhận | [04_ELEMENT.md](04_ELEMENT.md) | incorporated; HiddenPassenger không coi là Element đang dùng |
| SRC-02 Booster A2:H6 | Vacuum, Broom, Extra Box, Extra Slot, Hint | [05_BOOSTER.md](05_BOOSTER.md) | incorporated; giá / hiệu lực chưa chốt |
| SRC-01; SRC-02 Level Progress A2:B2 | Chưa viết Level Progress | [06_LEVEL_PROGRESS.md](06_LEVEL_PROGRESS.md), Q-012 | deferred-by-human-decision |
| SRC-02 Category Object A5:H359 | 355 nhóm, 356 mã, ảnh và số asset | [07_CATEGORY_OBJECT.md](07_CATEGORY_OBJECT.md); CATEGORY_OBJECT.md | incorporated; điền lặp lại bối cảnh từ ô gộp |
| SRC-02 VFXanim A2:G11 | Hoạt ảnh, trigger và thời gian tham chiếu | [09_ANIMATION_VFX.md](09_ANIMATION_VFX.md), V_01–V_10 | incorporated; không khẳng định đã đo runtime |
| SRC-02 SFX A2:D18, A21:B21 | 17 tên clip, thiếu nhạc và một số mapping | [10_SFX.md](10_SFX.md) | incorporated; 16 sự kiện có mapping, Bubble tap 1 chưa gán |
| SRC-02 Haptic A2:E4 | Công tắc rung, cảnh báo độ khó, trigger chưa rõ | [10_SFX.md](10_SFX.md) | incorporated; không tự thêm rung |
| SRC-02 Economy B3:L20 | Coin, tim, IAP, thưởng, giá còn xung đột | [12_ECONOMY.md](12_ECONOMY.md), Q-009 | incorporated / unresolved theo từng giá trị |
| SRC-02 Tutorial A1:C21 | Các bước và 4 hình ghép | [13_TUTORIAL.md](13_TUTORIAL.md) | incorporated |
| SRC-02 UIUX A4:D17 | Luồng, HUD, popup, ngôn ngữ, lưu màn | [14_UI_UX.md](14_UI_UX.md); Q-010, Q-013 | incorporated / unresolved theo hành vi |
| SRC-02 Nguồn & Xác minh A1:B14 | Phạm vi phân tích tĩnh, nguồn chi tiết | SOURCE_MAP | incorporated ngoài Overview / Gameplay |
| SRC-04–SRC-07 | Hai schema và cách thay order | [15_LEVEL_DATA.md](15_LEVEL_DATA.md) | incorporated; chưa duyệt schema cuối |
| SRC-01: “tạm bỏ qua” | Chưa đưa booster / Element RoomSort vào thiết kế | [04_ELEMENT.md](04_ELEMENT.md)–5; D-009 | incorporated |
| SRC-01: câu trả lời Q-001 | Level RoomSort + art Tidy Room + feeling Happy | D-012; Overview, Art, Animation, Level Data | incorporated; không tự duyệt mọi luật RoomSort |
| SRC-01: yêu cầu tách file | Nhiều tài liệu nhỏ cùng folder, GDD.md là mục lục | D-013; toàn bộ gói | incorporated |
| Đề xuất của trợ lý về luật Lose RoomSort | Khay đầy vẫn có thể chơi nếu còn nước đi thẳng vào hộp | Q-002 | proposed; chưa thay câu Lose đã chốt trước |
| Đề xuất của trợ lý về data | Giữ Happy để tích hợp, dùng biến thể order kiểu RoomSort | D-010, Q-011 | proposed |

## Hình ảnh và chuyển động

| Nhóm | File đã xem | Chi phối | Giới hạn |
|---|---|---|---|
| Object | references/object-2.png … object-7.png | Móc áo, hộp mở / khóa, slot, kho cầu vồng, nền phòng | Hình tài nguyên, không phải screenshot runtime |
| Booster | references/booster-2.png … booster-5.png | Máy hút, chổi, hộp thêm, slot thêm | Không xác nhận chuỗi sử dụng |
| Tutorial | references/tutorial-6.png, tutorial-11.png, tutorial-16.png, tutorial-21.png | Minh họa bước dạy và đối tượng chỉ tay | Hình ghép, không xác nhận tutorial đã chạy |
| Art Happy đối chiếu | references/uiux-20.png | Tham chiếu cũ, không còn là art đích | Contact sheet; art đích là Tidy Room, chưa xem hình |
| Category | references/category-005.png … category-359.png | 355 mẫu theo dòng workbook | Đã kiểm tra file / neo / số lượng; chưa soi riêng mọi hình |
| Thu gom / đóng hộp / booster / Win-Lose / Revive | Chưa có video hoặc chuỗi runtime đã xem | Các mốc thời gian chỉ từ bảng cấu hình đã tổng hợp | Q-007–Q-008; không ghi timestamp giả hoặc coi still là bằng chứng motion |

Đây là bộ tài liệu thiết kế và tham chiếu. Chưa xác nhận quyền tái sử dụng cho tài nguyên sản xuất hoặc âm thanh; chưa tạo / tìm / cấp phép tài nguyên mới. Không có giao dịch hoặc quảng cáo thực tế được thực hiện.

## Kiểm tra bàn giao

Đã tách đủ 17 tài liệu chủ đề, giữ đủ nhóm nội dung mẫu; Haptic, SFX, Art và Animation có file riêng; Level Progress giữ đúng trạng thái tạm chưa viết. Phụ lục có đủ 355 dòng và tổng asset khớp. Ảnh và link nội bộ đã kiểm tra tồn tại. Hai mẫu level giữ nguyên dữ liệu nguồn của từng game. Các câu hỏi mở khiến status vẫn là drafting; không tuyên bố hoàn tất build handoff, độ phủ level, độ vui hoặc tương đương độ khó.
