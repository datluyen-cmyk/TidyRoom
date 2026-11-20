# Animation, VFX và Feeling

[← Mục lục GDD](GDD.md)

## Mục tiêu feeling

Giữ Happy làm mốc cho cảm giác chạm chọn, chuyển item tới đích, nhận đủ đồ và đổi hộp. Các mốc thời gian trong bảng dưới là dữ liệu tham chiếu Happy hiện có. Cần đối chiếu chuỗi chuyển động trước khi gọi là khớp feeling; chưa tự xem các timing này là thông số cuối đã duyệt.

### Sự kiện hình ảnh

| ID | Trigger | Chuỗi hiển thị | Thời gian đã có / điểm còn mở |
|---|---|---|---|
| V_01 | Chọn item hợp lệ — M-001 | Phản hồi chọn tại món vừa chạm, sau đó chuyển sang chuyển động thu gom. | Hình thức chi tiết của hiệu ứng chọn còn mở. |
| V_02 | Thu gom — M-002, M-003 | Item nảy nhẹ tại vị trí cũ, rồi bay đến hộp hoặc slot chờ tương ứng. | Nhịp lên 0,12 giây, xuống 0,10 giây; scale nảy 1,3; thời gian bay 0,5 giây. Đường bay và thời điểm ghi nhận sức chứa còn mở. |
| V_03 | Hộp xuất hiện / nhận đồ — M-002 | Hộp vào vị trí, chờ nhận đồ và phản hồi khi item tới. | Nhịp xuất hiện giữa các vị trí hộp 0,12 giây. |
| V_04 | Hộp đủ đồ — M-002 | Hộp đóng và rời đi, hộp tiếp theo xuất hiện ở vị trí đó. | Khoảng chờ hộp kế tiếp 0,8 giây. Tổng thời lượng chuỗi còn mở. |
| V_05 | Kho nhận / trả đồ — B-002 | Kho xuất hiện, nhận đồ từ khay; item phù hợp được chuyển về hộp. | Kho xuất hiện 0,3 giây; nhịp đồ bay từ kho 0,12 giây. Ưu tiên trả đồ còn mở. |
| V_06a | Vacuum — B-001 | Máy hút hoạt động, đồ được hút để hoàn tất hộp mục tiêu. | Đường hút và thứ tự item còn mở. |
| V_06b | Broom — B-002 | Hiệu ứng quét đi cùng chuỗi chuyển đồ từ khay sang kho. | Nhịp quét và đồng bộ sức chứa còn mở. |
| V_07 | Hint — H-001 | Viền vàng và nhịp phóng nhẹ trên item được gợi ý. | Hiện 0,4 giây, giữ 0,5 giây, ẩn 0,4 giây, nghỉ 0,2 giây. |
| V_08 | Còn một slot chờ — M-006 | Nhấp nháy slot cuối để cảnh báo. | Nhịp slot 0,45 giây. |
| V_09a | Win | Hiệu ứng thắng, sau đó hiện kết quả và phần thưởng. | Có thời gian chờ popup thắng 2 giây; chưa chốt toàn bộ chuỗi. |
| V_09b | Lose | Hiển thị tình trạng thiếu chỗ và lựa chọn hồi sinh / chơi lại. | Thời điểm so với item đang bay còn mở. |
| V_10a | Mở hộp — B-003 | Vị trí hộp khóa đổi thành hộp hoạt động. | Có hoạt ảnh thêm hộp; nhịp cụ thể còn mở. |
| V_10b | Mở slot — B-004 | Slot khóa đổi thành slot có thể chứa đồ. | Có hoạt ảnh thêm slot; nhịp cụ thể còn mở. |
| V_10c | Revive | Dọn slot chờ và trở lại trạng thái chơi. | Đích đến của đồ và đồng bộ tiếp tục lượt cần chốt. |
| V_11 | Chạm item bị đè / thao tác không hợp lệ | Không thu gom item; cần phản hồi để người chơi nhận biết. | Hiệu ứng hình cụ thể còn mở. |
| V_12 | Lấy item che phía trên — M-004 | Món phía dưới được lộ ra; chỉ nhận chọn khi đủ điều kiện lấy. | Thời điểm bỏ chặn trong chuỗi bay còn mở. |
| V_13 | Mở / đóng popup | Hiển thị hoặc đóng bảng đang chọn, giữ rõ ngữ cảnh của màn chơi. | Hiệu ứng và việc tạm dừng gameplay còn mở. |
| V_14 | Retry / khôi phục lượt | Bàn chơi trở về trạng thái bắt đầu hoặc trạng thái lưu hợp lệ. | Xử lý khi ngắt giữa chuyển động còn mở. |

Các giá trị thời gian ở trên là mốc tham chiếu hiện có, chưa phải bộ thông số đã được duyệt cho phiên bản mới. Cần chốt các chuỗi còn mở trước khi triển khai phần chuyển động phụ thuộc.
