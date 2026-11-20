# Tình huống kiểm tra thiết kế

[← Mục lục GDD](GDD.md)

Đây là các tình huống nghiệm thu, chưa phải kết quả chạy thử hoặc bộ level đã biên soạn.

| ID | Liên quan | Trạng thái đầu và thao tác | Kết quả cần đạt |
|---|---|---|---|
| C-001 | M-001, M-002 | Hộp Quần 2/4; chạm một chiếc quần lấy được. | Item vào hộp, tiến độ thành 3/4. |
| C-002 | M-003 | Chưa có hộp Tất; khay 2/5; chạm một chiếc tất lấy được. | Khay thành 3/5; không tăng tiến độ hộp khác. |
| C-003 | M-004 | A đè B; chạm B trước khi lấy A. | B chưa được thu gom. Khi dọn A và B đủ điều kiện lấy, B trở thành mục tiêu hợp lệ. |
| C-004 | M-002 | Hộp Quần 3/4; thu thêm một chiếc quần. | Hộp hoàn thành, rời vị trí và nhường chỗ cho yêu cầu tiếp theo. |
| C-005 | M-003 | Một chiếc tất đang chờ; hộp Tất xuất hiện và còn thiếu đồ. | Chiếc tất được chuyển từ khay vào hộp; slot đó được giải phóng. |
| C-006 | M-006 | Khay từ 3/5 thành 4/5. | Cảnh báo còn một slot trống. |
| C-007 | Lose | Khay đầy, còn item trên bàn và hộp chưa hoàn tất. | Áp dụng luật thua đang mô tả ở [02_GAMEPLAY.md](02_GAMEPLAY.md); nếu chọn luật RoomSort phải cập nhật cả trường hợp còn nước đi thẳng vào hộp. |
| C-008 | B-001 | Có hộp chưa hoàn thành và đủ đồ tương ứng để hoàn tất. | Vacuum hoàn thành một hộp; việc chọn hộp chờ Q-003. |
| C-009 | B-002 | Khay có 3 item; dùng Broom. | Khay trống, 3 item chuyển sang kho; số đồ cần thu không mất đi. |
| C-010 | B-003 | Có 2 hộp mở và một vị trí khóa; nhận Extra Box. | Có tối đa 3 hộp mở. |
| C-011 | B-004 | Khay có slot bổ sung còn khóa; nhận Extra Slot. | Sức chứa tăng theo lượng nhận được chốt ở Q-004. |
| C-012 | H-001 | Có item phù hợp và không thao tác 7 giây. | Hiện viền vàng và nhịp gợi ý. |
| C-013 | Win | Thu gom item cuối cùng và hoàn tất mọi hộp. | Kết màn, hiện phần thưởng và lựa chọn tiếp tục. |
| C-014 | Revive | Đang thua do hết chỗ; hồi sinh thành công. | Khay được dọn và tiếp tục màn hiện tại; cách xử lý item chờ chốt Q-005. |
| C-015 | M-005 | Kéo hoặc pinch trong vùng phòng. | Góc nhìn thay đổi; không tự thu gom item do nhầm thao tác. |
| C-016 | T-001–T-004 | Vào đúng mốc hướng dẫn, có đủ đối tượng cho bước dạy. | Hiện đúng lời nhắc và mục tiêu; từng bước thực hiện được. |
| C-017 | Economy, UI | Tắt Sound hoặc Haptic trong Settings. | Tùy chọn tắt tương ứng được tôn trọng khi thực hiện hành động tiếp theo. |
| C-018 | UI, M-007 | Mua thất bại, hủy hồi sinh, Retry hoặc mở lại giữa lượt. | Không tự cấp tài nguyên hay lặp thưởng; quy tắc mất tim / khôi phục cần chốt trước triển khai. |
