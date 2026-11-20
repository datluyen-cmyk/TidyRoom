# Tidy Room Level Tool · HTML5

Mở **Open Level Tool.cmd** (Windows), hoặc chạy `python server.py` và vào <http://127.0.0.1:37848>. Cần Python 3.10+ và Pillow (`python -m pip install Pillow`). App chỉ nghe trên máy này. Project mặc định là thư mục **TidyRoom Sort** nằm cạnh tool. Có thể đổi bằng biến `TIDY_UNITY_PROJECT`. Tool đọc ảnh trực tiếp từ `Assets/StreamingAssets/TidyRoom/Art` nên không cần chép ảnh sang thư mục tool.

1. Chọn **Ảnh nền**, rồi kéo thẻ trong **Đồ vật** vào phòng, hoặc bấm thẻ rồi bấm chỗ muốn đặt. **+ Đặt ở tâm** thêm đồ tại `(0,0)`. Esc để ngừng đặt và chuyển sang kéo đồ đã xếp. Có thể nhập tọa độ, góc và scale trong **Lớp đồ**; nâng/hạ làm thay đổi thứ tự vẽ và luật chặn. Chuột phải kéo khung nhìn; lăn chuột để zoom. Giữ Shift khi đặt hoặc kéo đồ để căn theo lưới 25 đơn vị.
2. Trong **Hộp & luật**, đặt thứ tự hộp và sức chứa. Có thể **Tạo hộp từ đồ đang có** rồi sửa thứ tự/sức chứa. Tổng chỗ của từng nhóm phải bằng số món cùng nhóm.
3. **Playtest** có hai hộp hoạt động và năm slot chờ. Đồ bị đè không lấy được; đồ đúng nhóm vào hộp, đồ còn lại chờ trong khay. Chọn luật thua khi đủ 5 slot, hoặc cho tiếp tục nếu còn món có thể vào thẳng hộp. Kết quả chơi thử không xóa đồ khỏi bản đang xếp.
4. **Lưu JSON** để giữ bản chỉnh; với bộ nhiều màn có nút **Lưu cả bộ**. Trình duyệt giữ bản nháp gần nhất. **Xuất Unity → Tải JSON Unity** tạo file `LevelData`. **Thêm màn vào Unity** tạo file mới và thêm vào `StreamingAssets/TidyRoom/index.json`. Khi đang Play trong Unity cần dừng và Play lại. Màn ở cuối nhóm **Happy reference** (luật đầy mất ngay) hoặc **RoomSort / Tidy Room** (luật cho vào hộp trực tiếp).

Đồ mới dùng kích thước đã đặt trong level Unity: ưu tiên cùng sprite và nền; nếu chưa có trên nền đó thì lấy cỡ điển hình của sprite theo chiều cao nền. Sprite chưa dùng ở bất kỳ màn nào dùng cỡ tham chiếu của bộ art. Với đồ đã đặt ở bản cũ, bấm **Cỡ gốc** cho một món hoặc **Cỡ gốc cả màn** rồi **Hoàn tác** nếu cần. Các nút này giữ tọa độ, góc và chiều lật.

## Nhập hàng loạt

- **Nhập level** có thể mở một màn hoặc cả thư viện đang dùng trong Unity, bộ RoomSort gốc và Happy Tidy Room gốc đã trích trên máy. Nguồn tham chiếu mặc định trong thư mục `APK` cạnh tool; có thể đổi bằng `TIDY_ANALYSIS_ROOT`.
- Hỗ trợ chọn nhiều file, chọn thư mục, thả file, hoặc ZIP chứa JSON/JSON.GZ. Mỗi JSON có thể chứa một màn, mảng màn, `levels[]`, `base.levels[]` (màn cơ sở) hoặc `records[].level` của Level Studio. ZIP được đọc tại chỗ.
- **RoomSort** dùng `content[].id, x, y, scaleX, scaleY, angle` và `order[].type, count`. **Happy** dùng thêm `content[].box` và `order[].box`, nền `HT_BG_*`. Chế độ **Tidy Room** nhập file đã trích có kiểu `content/order` và tên nền tương ứng trong Unity (có ánh xạ nền số → tên phòng). APK/APKS không phải đầu vào của tool. Nếu một game có cấu trúc khác, cần thêm bộ chuyển riêng.
- Khi import Unity/clone, giữ vị trí, scale, góc, thứ tự lớp, thứ tự hộp và nhóm nhận. Playtest dùng viền theo **ảnh đang hiển thị**, như chế độ `art` trong Unity. Màn RoomSort dùng polygon gốc có thể cần chơi lại để kiểm tra. Tool báo lỗi khi không tìm thấy ảnh/nền trong Unity, không thay bằng ảnh đoán; riêng ID số có thể dùng ảnh RoomSort cùng ID đã có trong Unity. Các màn lỗi có báo cáo riêng, các màn hợp lệ vẫn mở được.

## Hai dạng JSON

**JSON chỉnh sửa (`tidy-level-tool/1`):** `background.asset` trỏ vào art Unity kèm `width/height` theo hệ tọa độ; `items` gồm `uid`, `asset`, `group`, `targetType`, `layer`, `x/y`, `width/height`, `scaleX/scaleY`, `angle`; `boxes` sắp theo thứ tự mở. Tâm ảnh nền là `(0,0)`, `+X` sang phải, `+Y` lên trên, góc dương ngược chiều kim đồng hồ. Layer càng lớn càng nằm trên. Hệ tọa độ là đơn vị pixel ảnh nền; thay nền không tự dịch đồ. `cameraX` giữ lại thông tin gốc khi nhập.

**JSON Unity:** bộ chuyển sắp `items` theo `layer` tăng dần thành `content`, gán `uid` theo vị trí mảng, tạo `order`, ánh xạ nhóm logic sang `sourceType`, giữ `targetType` sang `type`, tạo `box` cho từng món và sinh alpha mask giống cấu trúc game. Đường dẫn ảnh giữ tương đối theo `StreamingAssets/TidyRoom`.
