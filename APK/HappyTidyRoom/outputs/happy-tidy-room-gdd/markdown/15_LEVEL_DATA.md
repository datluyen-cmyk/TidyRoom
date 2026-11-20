# Dữ liệu level

[← Mục lục GDD](GDD.md)

### Happy Tidy Room

| Phần | Nội dung |
|---|---|
| `levelName`, `bg`, `bgPosX` | Tên màn và bối cảnh. |
| `order[]` | Mỗi hộp có nhóm nhận `type`, số lượng `count`, ID `box` và trường `diff`. Chưa dùng `diff` để suy ra luật mới. |
| `content[]` | Mỗi item có `id`, `x`, `y`, `scaleX`, `scaleY`, `angle`, `box`. |
| `plan` | Dữ liệu hỗ trợ thiết kế / sinh bố trí, gồm hộp, lớp, lọc mẫu và các giới hạn xếp đồ. |
| Danh mục đồ | Liên kết ID đồ với nhóm nhận, bối cảnh và ảnh. |

### RoomSort

| Phần | Nội dung |
|---|---|
| Level | Số màn, tên, nền và thông tin màn nguồn. |
| `order[]` | Mỗi hộp có nhóm nhận `type` và số lượng `count`. |
| `content[]` | Mỗi item có `id`, vị trí, tỉ lệ và góc xoay. Thứ tự trong danh sách quyết định thứ tự chồng. |
| `items` | Kích thước và đường bao từng mẫu đồ để xét tương tác / che phủ. |
| `types` | Tên nhóm nhận. ID dạng `103-2` thuộc nhóm `103`. |
| Biến thể | Có thể thay thứ tự hộp của một level; một số biến thể còn lọc nhóm đồ. |

Quy tắc khi chuyển dữ liệu: ánh xạ nhóm nhận và mẫu đồ từ RoomSort sang thư viện Tidy Room; đổi nền; giữ quan hệ bố trí; kiểm tra lại độ che phủ theo kích thước và đường bao của art mới. Chép tọa độ giống nhau chưa bảo đảm level giữ nguyên độ khó hoặc cách giải.

Ở mỗi nhóm nhận, tổng số item trong màn phải khớp tổng số item các hộp yêu cầu. Chỉ tham chiếu những ID có trong danh mục. Không nhầm `box` liên kết thiết kế với số vị trí hộp mở đồng thời.

Các mẫu đầy đủ được giữ tại [Happy level 1](references/happy-level-1.json) và [RoomSort level 1](references/roomsort-level-1.json). Đây là hai mẫu riêng của game gốc, không phải bộ level kết hợp đã chuyển đổi. Chưa chọn cấu trúc dữ liệu cuối cho phiên bản mới.
