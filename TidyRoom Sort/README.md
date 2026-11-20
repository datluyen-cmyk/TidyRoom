# Tidy Room — bản test chuyển level

Project dùng target **Android**. Mở `Assets/TidyRoom/Scenes/LevelTest.unity`, bấm Play trong Unity để test. Không xuất APK theo yêu cầu hiện tại; gói Windows đã được xóa.

Bộ 139 màn RoomSort (130 màn cơ bản, 8 biến thể có đường giải, 1 tutorial) mặc định dùng nền RoomSort gốc để khớp bố cục đồ trong phòng. Đồ vật, hộp, slot và biểu tượng booster dùng art Tidy Room 57. Với những ID đồ vật không có trong gói này, game dùng ảnh RoomSort gốc. 65 màn Happy giữ nguyên dữ liệu và art để đối chiếu.

## Cách dùng

- **Levels:** chọn **RoomSort / Tidy Room** hoặc **Happy reference**. Dấu `*` là ghi chú cho bản xuất sang catalog Happy.
- **Tap:** lấy đồ chưa bị lớp trên che. Đúng nhóm hộp đang mở thì vào hộp; còn lại vào slot chờ. Hộp mới tự nhận đồ cùng nhóm trong slot chờ và kho tạm.
- Hộp và slot chờ đặt đè lên phòng. Nền và đồ vật luôn giữ cùng tỉ lệ, không kéo dài pixel ở mép ảnh. Map rộng cần kéo ngang để xem các đồ ở hai bên; camera có giới hạn để không kéo lạc khỏi phòng. Dùng `+`/`-` hoặc lăn chuột để phóng to/thu nhỏ. Khoảng ngoài ảnh nền dùng màu sàn phẳng.
- **Test options → Layers:** làm tối đồ đang bị che. **Reset view** đưa camera về vị trí ban đầu.
- **Test options → Background:** chuyển giữa nền RoomSort gốc và nền Tidy Room tương ứng ngay trên cùng màn, giữ tiến độ đang chơi. Khi vào hoặc khởi động lại màn RoomSort, game dùng nền gốc. Màn không có nền Tidy Room tương ứng chỉ hiển thị nền gốc.
- **Vacuum:** làm đầy một hộp đang mở. **Broom:** chuyển đồ trong slot chờ sang kho tạm; bấm biểu tượng kho để xem đồ đã cất. Nút `+` mở tối đa 7 slot và 3 hộp để thử phương án cứu màn.
- **Test options → Collision:** so sánh vùng che phủ RoomSort gốc với vùng che phủ theo ảnh đồ đang hiển thị. Chế độ gốc dùng polygon gốc nên vùng bấm có thể lệch viền ảnh.
- **Test options → Lose:** chọn thua ngay khi đầy slot hoặc chỉ thua khi đầy slot và không còn nước đi trực tiếp vào hộp.
- **Replay supplied solution:** tự chơi đường giải có sẵn của 8 màn `ladder_*`. Restart khôi phục trạng thái và cấu hình mặc định của màn.

## Chuyển lại dữ liệu

Chạy trong PowerShell, khi đã dừng Play:

```powershell
& ./Tools/Convert-Levels.ps1
```

Từ thư mục project, script đọc dữ liệu RoomSort, Happy và Tidy Room trong thư mục `APK` bên cạnh project. Có thể truyền `-RoomRoot`, `-HappyRoot` và `-TidyRoomApks` khi đổi vị trí nguồn. Cần Node.js, Python, Pillow và UnityPy. Để chỉ cập nhật art mà không chạy lại converter, chạy `Tools/import_tidy_room_art.py` với Python.

Chỉnh `Tools/category-map.json` để đổi nhóm nhận. Mỗi nhóm ghi `sourceName`, `happyType`, `happyName`, `status`. `mapped` là đã gán nhóm; `proxy` là nhóm thay thế cần duyệt; `unmapped` là chưa có nhóm tương ứng. Có thể thêm `items` để chọn từng ảnh cụ thể:

```json
"items": { "28-1": "HandBag_6" }
```

ID ảnh phải tồn tại trong đúng `happyType`; tool sẽ báo lỗi nếu sai. Xem danh sách ID thật trong catalog đầu vào trước khi sửa ví dụ.

Kết quả:

- `Assets/StreamingAssets/TidyRoom`: bộ dữ liệu và ảnh mà bản test đọc. Level được nén `.json.gz`; nền dùng JPEG chất lượng 95 để giảm dung lượng, ảnh đồ vật giữ nguyên PNG.
- `Converted/HappyLevels`: JSON theo cấu trúc level Happy (`bgPosX`, `bg`, `levelName`, `order`, `content`). Giữ thứ tự hộp, số lượng, vị trí, phép lật, góc và lớp chồng; điều chỉnh scale ảnh mới theo khung đồ gốc.
- `Converted/HappyLevels/CatalogCompatible`: không có cảnh báo gán nhóm. Hiện có 10 màn. Đây là tương thích catalog, **chưa phải chứng nhận độ khó hoặc đường giải sau khi đổi art**.
- `Converted/HappyLevels/NeedsReview`: có nhóm thay thế, thiếu art hoặc nhiều nhóm RoomSort cùng trỏ vào một nhóm Happy. Cần sửa mapping trước khi đưa thẳng vào game Happy.
- `Converted/conversion-report.json`: cảnh báo theo màn. `Converted/mapping-summary.json`: tổng hợp mapping.
- `Converted/tidy-room-art-report.json`: thống kê art Tidy Room và danh sách ảnh phải giữ từ RoomSort gốc. Bước đổi art chỉ cập nhật bộ level RoomSort dùng để Play trong Unity.

Bản test giữ `sourceType` riêng để không gộp hai nhóm nhận. Bản xuất Happy thuần không mang cơ chế giữ nhóm này. JSON Happy thuần dùng nền Happy tương ứng số màn làm nền xem thử, cần bố trí lại bối cảnh trước khi đưa vào sản phẩm.

## Kết quả kiểm tra

Menu **Tidy Room → Validate Conversion and Gameplay** kiểm tra số lượng, nhóm/hộp, thứ tự lớp, ảnh và chạy đường giải mẫu. Kết quả nằm trong `Evidence/validation.json`.

204 màn đã qua kiểm tra dữ liệu và không thiếu ảnh. Cả 8 đường giải mẫu thắng với vùng va chạm gốc, không có bước bấm bị từ chối. Khi dùng viền ảnh hiển thị, cả 8 đường giải cũ đều gặp bước bị che; điều này cho thấy cần kiểm tra lại đường đi, chưa kết luận các màn đó vô nghiệm. Các phép thử còn kiểm tra chặn lớp, tự chuyển slot/kho vào hộp, thắng/thua, Vacuum, Broom và giới hạn slot/hộp.

Menu **Tidy Room → Check Runtime UI** chạy khi đang Play để thử bấm đồ qua raycast, Restart, chọn level và đổi chế độ va chạm. Kết quả: `Evidence/runtime-ui.json`. Ảnh chụp màn chơi được lưu trong `Evidence`.

Menu **Tidy Room → Check Rapid Input and Maps** thử bấm liên tục theo cụm 6 lượt trong cùng một frame, kiểm tra bộ đếm hộp/slot qua từng bước, bấm trùng và đổi màn khi đồ đang bay. Đồng thời kiểm tra khả năng kéo tới mép đồ trên 204 map và giữ đúng tỉ lệ nền khi zoom/kéo. Kết quả: `Evidence/input-map-regression.json`. Hiệu ứng bay không khóa thao tác; mỗi đồ chỉ được ghi nhận một lần.

## Những điểm đang dùng quy tắc thử nghiệm

Thứ tự lớp và vùng va chạm RoomSort dùng phép tính gốc, gồm tính phần giao chính xác khi còn 1–2 đồ che và mẫu 64×64 khi nhiều đồ che. Chế độ ảnh Happy dùng alpha mask thu nhỏ tối đa 40×40 và ngưỡng che 4,5%; đây là quy tắc mô phỏng để test, chưa xác nhận đúng công thức gốc của Happy. Scale riêng theo map của Happy đã được nhập. Thời điểm thua ngay khi đầy slot của Happy và ưu tiên hộp cho Vacuum cũng cần đối chiếu thêm nếu muốn khớp hoàn toàn game gốc.

Phạm vi đã làm: vòng chơi dọn đồ và công cụ so sánh/chuyển level. UI được bố trí lại cho việc test; chưa dựng shop, quảng cáo, kinh tế, âm thanh hay các màn meta.

## Unity MCP

Đã cài CoplayDev Unity MCP `v10.3.0`, server `mcpforunityserver==10.3.0`, endpoint `http://127.0.0.1:8080/mcp`. Cấu hình Codex trên máy đã có endpoint này. Nếu server chưa chạy, dùng `Tools/Start-UnityMCP.ps1`, sau đó chọn **Tidy Room → Connect Unity MCP**. Server chỉ nghe trên localhost.

Trên Android, dữ liệu trong `StreamingAssets` được đọc qua `UnityWebRequest` và chỉ chép level/ảnh đang dùng vào cache của ứng dụng. Nhánh đọc file này đã được chuẩn bị trong code; chưa kiểm tra trên thiết bị Android vì chưa build APK. Scene mẫu ban đầu vẫn còn tại `Assets/Scenes`.
