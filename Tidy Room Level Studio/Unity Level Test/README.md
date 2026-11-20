# Tidy Room — chơi thử level trong Unity

Mở [Open Unity Level Test.cmd](../Open%20Unity%20Level%20Test.cmd) hoặc mở thư mục này như project **Unity 2022.3.62f2**. Trong Editor, chọn **Tidy Room → Play Level Test** (hoặc mở `Assets/Level Test.unity` rồi bấm **Play**).

Mặc định vào màn 1 của batch seed 42. **Màn trước / Màn sau** đổi giữa 12 màn. Bấm vào đồ để dọn. Đồ đang bị đè sẽ rung; đồ hợp nhóm vào hộp, đồ chưa có hộp chờ trong khay. **Xem lời giải** bắt đầu lại và đánh dấu điểm bấm tiếp theo; có thể bấm **Bước tiếp** để theo lời giải.

Muốn xem một batch khác, dừng Play rồi chạy từ thư mục này:

```powershell
node prepare-levels.mjs '..\batches\TEN_BATCH\pack.json'
```

Cần Node.js 20+ và Python có Pillow để chuyển ảnh từ Level Studio. Khi nhập xong, để Unity nạp lại `Assets`, rồi bấm Play. Mỗi lần nhập thay bộ màn trong project chơi thử; file `pack.json` nguồn vẫn giữ nguyên. Chạy lại script không truyền đường dẫn để nạp 12 màn mẫu.

`verification.txt` ghi kết quả Unity chạy lại các tọa độ bấm của 12 màn gốc ở hai tỷ lệ khung hình, kiểm tra ảnh và luật khay. Bản này phục vụ test level, với hiệu ứng chuyển đồ cơ bản.
