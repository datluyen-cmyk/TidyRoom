# Gameplay

[← Mục lục GDD](GDD.md)

### Vòng lặp chính

Quan sát hộp đang mở → tìm item đúng nhóm → chạm để thu gom → hoàn thành hộp → nhận hộp tiếp theo → dọn sạch màn chơi.

**Core mechanic:** Chạm item để dọn vào hộp chứa đúng nhóm. Item chưa có hộp nhận sẽ vào slot chờ và chuyển vào hộp khi có nhóm phù hợp. Đồ vật xếp theo layer; đồ bị đè chưa lấy được, cần dọn đồ phía trên trước.

**Win:** Khi toàn bộ item trên level được dọn sạch vào các hộp chứa.

**Lose:** Khi đầy hết slot chờ mà vẫn còn item trên màn chơi, các hộp chứa chưa được đầy hết.

**Revive:** Dùng coin hoặc xem quảng cáo để dọn slot chờ và tiếp tục chơi.

### Quy tắc tương tác

| ID | Quy tắc |
|---|---|
| M-001 | Mỗi lần chạm chọn một item có thể lấy. Item cùng nhóm có thể khác màu và kiểu dáng. |
| M-002 | Item khớp hộp đang mở được chuyển vào hộp đó. Hộp nhận đủ số lượng sẽ hoàn thành và nhường vị trí cho hộp tiếp theo. |
| M-003 | Item chưa có hộp nhận chiếm một slot chờ. Khi có hộp phù hợp, item đang chờ được chuyển vào hộp. |
| M-004 | Item phía trên có thể đè item phía dưới. Dọn món phía trên để mở đường lấy món bên dưới. |
| M-005 | Kéo hoặc thu phóng giúp quan sát phòng. Cần phân biệt thao tác kéo với chạm để tránh chọn nhầm đồ. |
| M-006 | Cảnh báo khi khay còn một slot trống. Khi đạt điều kiện thua, hiển thị lựa chọn hồi sinh hoặc chơi lại. |
| M-007 | Chơi lại bắt đầu lại màn hiện tại. Rời hoặc chơi lại có thông báo liên quan đến mất tim. |

Ví dụ: hộp Quần đang nhận 2/4 món. Chạm một chiếc quần có thể lấy sẽ đưa tiến độ lên 3/4. Chạm một chiếc tất khi chưa có hộp Tất sẽ làm item đó chiếm một slot chờ. Nếu chiếc quần bị một món khác đè lên, cần lấy món phía trên trước.

Các trường hợp nhiều hộp cùng nhận một nhóm, xử lý nhiều item đang bay và hồi phục màn đang chơi được ghi cụ thể trong [quyết định cần chốt](DESIGN_DECISIONS.md). Level theo RoomSort không tự quyết định mọi luật hoặc nhịp chuyển động của bản kết hợp.
