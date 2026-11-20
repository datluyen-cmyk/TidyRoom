# Tidy Room Level Studio

Tool chạy trên máy để sinh level trên **art Tidy Room** theo các mốc **RoomSort**. Bản chơi thử trong tool kiểm tra cách chạm lấy, hộp, layer và khay chờ. Cảm giác chuyển động **Happy Tidy Room** vẫn là mục tiêu của bản game, chưa được tái tạo trong phần xem thử này.

## Mở và sinh màn

1. Mở [Open Generator.vbs](<Open Generator.vbs>). Nó mở giao diện tại `http://127.0.0.1:37846`. Cần Node.js 20 trở lên; launcher ưu tiên Node có sẵn trong Codex. Nếu máy không chạy VBS, mở PowerShell tại thư mục này và chạy `node server.js`, sau đó mở địa chỉ trên.
2. Chọn **Từ mốc**, **Số màn**, **Seed** và nền. Mặc định luân phiên giữa phòng ngủ, phòng giường tầng và phòng khách. Chọn mốc `1` để bắt đầu theo thứ tự tham chiếu; chọn `40` để bắt đầu ở đoạn giữa. Tool không suy ra mốc 131 trở đi.
3. Bấm **Sinh level**. Kết quả nằm tại `batches/`. **Dừng** lưu các màn đã qua kiểm tra, sau khi xử lý xong mốc đang chạy.
4. Chọn lượt và màn để xem bố cục, đi từng bước của lời giải, hoặc bấm **Chơi thử** để tự thu gom. Hai hộp mở và 5 slot chờ được hiển thị. Chế độ này chưa có booster, tutorial hoặc animation của game đích.

Mặc định, mỗi màn phải có một đường giải **không chạm 5 slot đang chứa đồ**. Nếu bỏ chọn, bộ kiểm tra dùng luật RoomSort: khay đầy vẫn cho chơi tiếp nếu còn món vào thẳng hộp. Đây là tùy chọn kiểm tra; không thay luật đã ghi trong GDD. Lượt chưa đủ màn lưu `partial.json`, không xuất `levels.json` như thể đã đạt đủ.

## Sửa chỗ đặt đồ

- Chọn nền cụ thể rồi bấm **Xem vùng và điểm đặt**. Ba nền có vùng sàn và các mặt đỡ được đánh dấu một lần.
- **Khoanh vùng**: click các góc trên nền theo thứ tự quanh mặt bàn, ghế hoặc sàn, rồi lưu. JSON template cho phép thêm `types` để giới hạn nhóm đồ và `weight` để chỉnh mức xuất hiện. Vùng đầu phải là vùng chung.
- **Dời điểm vắt**: click vào mép giường hoặc ghế để dời điểm đầu tiên. Trong JSON, mỗi điểm có danh sách `choices` với `id`, `angle`, `scale` và độ lệch `du`, `dv` nếu cần. Áo `24-10`, quần `1-4` và khăn `12-4` là ví dụ sprite có nếp vắt thật. Sprite dáng vắt được tách khỏi nhóm rải ngẫu nhiên trên mặt phẳng.
- Bản chỉnh lưu theo trình duyệt và chỉ áp dụng khi chọn đúng nền; **Lưu template JSON** để mang sang máy khác. Muốn chỉnh nền ngoài ba nền có sẵn cần bổ sung ảnh, vùng đặt và điểm neo vào `data/art.json`. Tool chưa tự nhận diện nội thất từ ảnh.

## Tool học gì từ RoomSort?

`data/references.json` giữ thứ tự của **130 level cơ sở RoomSort**. Không trộn các nhánh thử nghiệm vào đường progression chính. Tool giữ đúng số item, số nhóm khác tên, số hộp và phân bố sức chứa từng hộp ở mốc tham chiếu. Bố cục, nhóm đồ và thứ tự hộp sinh mới; tỷ lệ đồ lấy được lúc đầu, mật độ chồng đồ, lượng đồ vào được hộp ngay và khoảng cách giữa hộp cùng nhóm dùng để lọc/chấm ứng viên.

Với **59 mốc có `LEVEL_ODDS`**, mô hình hàng xóm gần nhất dùng số liệu trên để xếp hạng nhẹ các ứng viên. Thử giữ nguyên từng nền nguồn ngoài tập học: MAE **18,166**, so với **20,085** của dự đoán trung vị. Đây là nhãn đóng gói, không phải tỷ lệ thắng đã đo trên người chơi. Từ mốc 60 trở đi chỉ có các mốc cấu trúc để đối chiếu. Tool học từ thống kê và dựng theo ràng buộc, không dùng mô hình sinh ảnh hoặc mô hình ngôn ngữ để đặt đồ.

### Điều được kiểm tra cho mỗi màn

- Số đồ theo từng nhóm khớp tổng số yêu cầu của các hộp. Không dùng hai mã phân loại cùng tên trong một màn.
- Tỷ lệ đồ lấy được lúc đầu và mật độ chồng đồ nằm trong khoảng quanh mốc tham chiếu. Có ít nhất một món lấy được và vào được hộp lúc đầu.
- Bố cục có đường giải qua logic RoomSort với hình dạng đồ Tidy Room, không booster. Lời giải được chạy bằng ID đồ và bằng tọa độ click thật qua bộ kiểm tra điểm chạm.
- Kiểm tra dấu vân tay bố cục/thứ tự hộp để loại trùng với 130 màn cơ sở và các batch hoàn chỉnh đã lưu. Đây là phép lọc theo quan hệ che phủ và chuỗi hộp, chưa phải phép chứng minh mọi dạng xoay, lật hay gần trùng.

Độ hay còn cần người chơi: thử cùng các mốc RoomSort và level mới, ghi số lần thua, thời gian, số lần mắc kẹt và món nào khó nhận ra. Bot trong `audit.js` hỗ trợ phát hiện chênh lệch, không thay người chơi thật. Art nền dùng các vùng đánh dấu thủ công; không thể bảo đảm mọi góc xoay hoặc lớp che bởi nội thất đều đẹp chỉ bằng số liệu.

## File đầu ra

| File | Dùng để làm gì |
|---|---|
| `levels.json` | Dữ liệu màn đã qua lọc. Hệ tọa độ lấy tâm ảnh nền làm gốc, `x` hướng phải, `y` hướng lên, góc dương ngược kim đồng hồ. `content[]` từ lớp dưới lên trên. |
| `pack.json` | Bố cục, seed, chỉ số đối chiếu, thứ tự cần lấy và tọa độ click lời giải. |
| `progression.csv` | Số đồ/hộp/nhóm, tỷ lệ đồ lộ, mật độ chồng và áp lực khay theo từng mốc. |
| `validation.json` | Trạng thái đủ/thiếu, lý do loại, dấu kiểm tra nguồn, luật, art và pack. |
| `partial.json` | Chỉ các màn đã qua kiểm tra khi hết lượt thử hoặc dừng. |

Để chơi thử 12 màn mẫu trong Unity, mở [Open Unity Level Test.cmd](<Open Unity Level Test.cmd>). [Hướng dẫn Unity](<Unity Level Test/README.md>) có cách nạp `pack.json` của lượt sinh khác. Sheet Level Progress trong GDD không bị sửa.

## Chạy lại từ dòng lệnh

```powershell
node batch.js --start=1 --count=12 --seed=42 --room=bedroom
node audit.js <tên-folder-trong-batches>
```

Bỏ `--room` để luân phiên nền. Nếu muốn lặp lại seed mà không loại các batch trước, thêm `--exclude=false`. Model lưu tại `data/model.json`. Khi đổi core RoomSort hoặc `studio.js`, chạy `node train.js` để làm lại thống kê và đồng bộ dấu kiểm tra trước khi sinh.
