from pathlib import Path
import json
import re
import shutil
import openpyxl

ROOT = Path(r'D:/APK Works/HappyTidyRoom')
OUT = ROOT / 'outputs/happy-tidy-room-gdd/markdown'
if (OUT / '01_OVERVIEW.md').exists():
    raise SystemExit('GDD is now split into topic files. Edit those files directly; this legacy builder must not overwrite them.')
OUT.mkdir(parents=True, exist_ok=True)
WB = ROOT / 'outputs/happy-tidy-room-gdd/GDD.xlsx'
w = openpyxl.load_workbook(WB, data_only=False)

gdd = r'''---
title: "Tidy Room Sort — Game Design Document"
status: drafting
updated: 2026-11-20
revision: 0.1
scope: "Thiết kế game dựa trên Happy Tidy Room; chưa biên soạn Level Progress; hướng áp dụng level RoomSort đang chờ chốt."
---

# Tidy Room Sort

## 1. Overview

Tidy Room Sort là game giải đố dọn phòng. Người chơi tìm đồ trong căn phòng bừa bộn và thu gom vào các hộp theo đúng nhóm để hoàn thành màn chơi.

| Mục | Thiết kế |
|---|---|
| Thể loại | Casual puzzle, kết hợp tìm đồ, phân loại và quản lý slot chờ. |
| Nền tảng | Điện thoại, màn hình dọc. |
| Người chơi | Người thích tìm đồ, sắp xếp và giải đố bằng thao tác đơn giản. |
| Camera | Góc nhìn isometric giả lập bằng đồ họa 2D. Có thể kéo và thu phóng để tìm đồ. |
| Điều khiển | Chạm để chọn đồ, kéo để di chuyển góc nhìn, dùng hai ngón tay để thu phóng. |
| Mỹ thuật | Hoạt hình 2D, màu dịu mắt. Đồ vật có hình dáng và đường viền rõ để dễ nhận diện. |
| Phần thưởng | Hoàn thành màn nhận coin, có lựa chọn xem quảng cáo để nhận thêm thưởng. |
| Tài nguyên | Coin, tim và lượt sử dụng booster. |
| Kiếm tiền | Quảng cáo nhận thưởng, quảng cáo xen kẽ, banner, gói bỏ quảng cáo và gói coin. |

Trải nghiệm tập trung vào ba điểm: nhận diện đúng nhóm đồ, chọn thứ tự thu gom để mở lớp bên dưới và giữ đủ slot chờ. Căn phòng sạch dần cho thấy tiến độ của người chơi.

## 2. Gameplay

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

Các trường hợp nhiều hộp cùng nhận một nhóm, xử lý nhiều item đang bay và hồi phục màn đang chơi được ghi cụ thể trong [quyết định cần chốt](DESIGN_DECISIONS.md). Không tự dùng luật của RoomSort để lấp các điểm này.

## 3. Object

| ID | Đối tượng | Vai trò | Ảnh |
|---|---|---|---|
| O-001 | Đồ vật thu gom | Các món đặt rải và chồng lên nhau trong phòng. Mỗi món thuộc một nhóm nhận. | ![Đồ vật](references/object-2.png) |
| O-002 | Hộp đang mở | Hiển thị nhóm cần thu và bộ đếm. Ban đầu mở 2 hộp. | ![Hộp mở](references/object-3.png) |
| O-003 | Hộp khóa | Vị trí hộp bổ sung. Extra Box mở thêm hộp, tối đa 3 hộp cùng lúc. | ![Hộp khóa](references/object-4.png) |
| O-004 | Slot chờ | Ban đầu có 5 slot. Mỗi slot giữ một item chưa có hộp nhận; có 2 slot bổ sung. | ![Slot chờ](references/object-5.png) |
| O-005 | Kho tạm | Nhận item từ Broom để giải phóng khay chờ. Đồ trong kho vẫn thuộc số đồ cần thu. | ![Kho tạm](references/object-6.png) |
| O-006 | Bối cảnh | Nền phòng và nội thất giúp định hướng bộ đồ, bố cục và vùng tìm kiếm. | ![Bối cảnh](references/object-7.png) |

Hộp khóa là vị trí hỗ trợ sức chứa, không phải Element gây khó của level. Số lượng cần thu được đặt theo từng hộp, không cố định ba món cho mọi hộp.

## 4. Element

Chưa ghi nhận Element đặc biệt đang hoạt động để đưa vào thiết kế.

Element là cơ chế bổ sung làm thay đổi cách chơi hoặc tăng độ khó, như khóa hoặc bom. Layer, hộp nhận và slot chờ thuộc luật chơi cơ bản. Booster được mô tả riêng ở mục 5.

## 5. Booster

| ID | Booster | Tác dụng | Mở khóa | Ảnh |
|---|---|---|---|---|
| B-001 | Vacuum | Hoàn thành ngay một hộp. | Level 3 | ![Vacuum](references/booster-2.png) |
| B-002 | Broom | Chuyển toàn bộ item trong slot chờ sang kho tạm. | Level 6 | ![Broom](references/booster-3.png) |
| B-003 | Extra Box | Mở thêm một hộp đang khóa, tối đa 3 hộp cùng lúc. | Chưa chốt level | ![Extra Box](references/booster-4.png) |
| B-004 | Extra Slot | Tăng chỗ chứa trong khay chờ. Có 2 slot bổ sung. | Chưa chốt level | ![Extra Slot](references/booster-5.png) |

**Vacuum:** Bấm nút → dùng lượt hiện có hoặc chọn cách nhận → hút đồ để hoàn thành một hộp. Nếu không có hộp hợp lệ, báo không thể sử dụng. Quy tắc chọn hộp mục tiêu còn cần chốt.

**Broom:** Bấm nút → dùng lượt hoặc chọn cách nhận → chuyển đồ từ khay sang kho → tiếp tục thu gom. Nếu khay trống, báo không có item để dọn.

**Extra Box / Extra Slot:** Chạm vị trí khóa → mở lựa chọn nhận hỗ trợ → bổ sung sức chứa. Số slot mở mỗi lần và hiệu lực qua màn còn cần chốt.

**H-001 — Hint:** Sau 7 giây không thao tác, item phù hợp được gợi ý bằng viền vàng và nhịp phóng nhẹ. Đây là trợ giúp tự động, chưa đặt thành booster mua bằng coin.

Eagle Eye, Erase, Clear trả đồ về phòng và Undo của RoomSort chưa được đưa vào bộ booster này. Việc đổi level tham chiếu không tự thay đổi bộ booster.

## 6. Level Progress

Tạm chưa biên soạn theo yêu cầu. Các mốc tutorial ở mục 11 chỉ mô tả thời điểm giới thiệu tính năng, không thay thế bảng tiến trình level.

## 7. Category Object

Thư viện gồm **355 tên nhóm hộp nhận**, ứng với **356 mã category**, **2.863 asset đồ vật** và **44 nhóm bối cảnh**. Có 2.638 ID asset xuất hiện trong 65 file dữ liệu màn đã thống kê.

Category được chia theo tên nhóm mà hộp nhận, không chia theo các thành phần giao diện. Hai category cùng tên Gift box được cộng thành một dòng, tổng 13 asset.

**Bối cảnh** giúp chọn bộ đồ và chủ đề khi thiết kế màn. Nó không giới hạn đồ vật chỉ được xuất hiện ở một loại phòng. Số asset đếm theo ID hình riêng, không tính các bản sao đặt trong level.

Xem toàn bộ tên nhóm, bối cảnh, số asset, mã category và ảnh đại diện trong [CATEGORY_OBJECT.md](CATEGORY_OBJECT.md).

## 8. Art, Animation và VFX

### Art direction

Dùng Happy Tidy Room làm tham chiếu hình ảnh: đồ họa 2D giả lập chiều sâu, màu dịu, viền rõ. Các mẫu trong cùng nhóm cần dễ nhận là cùng loại dù khác màu hoặc kiểu dáng. Nhãn và icon của hộp phải giúp người chơi hiểu nhóm nhận ngay khi quan sát.

![Tham chiếu đồ vật và bối cảnh](references/uiux-20.png)

Ảnh Object, Booster và Tutorial trong tài liệu là tài nguyên và hình ghép minh họa. Chúng xác định hình dáng, màu sắc và ý nghĩa đối tượng; không thể hiện đầy đủ chuyển động của một lượt chơi.

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

## 9. SFX và Haptic

### Âm thanh

| ID | Sự kiện | Tên âm thanh tham chiếu |
|---|---|---|
| A-01 | Bấm nút | Button click |
| A-02 | Chọn đồ hợp lệ | Bubble tap 2 (1) |
| A-03 | Chạm không hợp lệ | tap_wrong |
| A-04 | Item vào hộp | Item Drop Into Box |
| A-05 | Hộp xuất hiện | sfx_box_in |
| A-06 | Hộp đóng | box_close |
| A-07 | Hộp rời đi | Box Disappears |
| A-08 | Bắt đầu màn | Start level |
| A-09 | Kết màn | sfx_level_end |
| A-10 | Thắng | win_sfx |
| A-11 | Thua | lose_sfx |
| A-12 | Dùng Broom | Broom booster |
| A-13 | Dùng Vacuum | Vaccum booster |
| A-14 | Gợi ý | sfx_hint |
| A-15 | Nhận coin | coin_sfx |
| A-16 | Mua thành công | purchase_sfx |

`Bubble tap 1` là âm thanh bổ sung chưa xác định trigger, chưa gán vào một hành động mới. Nhạc nền, âm hồi sinh riêng, độ lớn tương đối và cách chồng âm chưa chốt. Danh sách tên âm thanh là tham chiếu nội dung, chưa phải bộ âm thanh sản xuất được bàn giao.

### Haptic

Settings có công tắc bật / tắt rung. Cảnh báo độ khó có các mốc rung 0,2 giây và 1,3 giây, với thời lượng tham chiếu 300 ms. Rung cho chọn đồ, hoàn thành hộp và booster chưa được xác định, không tự bổ sung vào luật chơi.

## 10. Economy

Coin dùng cho các tính năng hỗ trợ. Tim giới hạn lượt chơi sau thất bại. Lượt booster được quản lý riêng với coin.

| Nội dung | Giá trị tham chiếu | Trạng thái |
|---|---:|---|
| Coin ban đầu | 600 coin | Mốc tham chiếu |
| Coin miễn phí trong Shop | 50 coin | Chưa chốt điều kiện và thời gian nhận lại |
| Revive | 800 coin hoặc quảng cáo | Chưa chốt số lần dùng tối đa |
| Nạp tim | 700 coin | Chưa chốt số tim nhận |
| Hồi một tim | 30 phút | Chưa chốt số tim tối đa |
| Thưởng Easy / Hard / Super Hard | 20 / 40 / 60 coin | Còn xung đột với mốc thưởng 30 / 60 ở popup |
| Vacuum / Broom | Coin, quảng cáo hoặc lượt hiện có | Chưa chốt giá |
| Extra Box / Extra Slot | Có luồng mở hỗ trợ | Chưa chốt giá và lượng nhận |

| Gói mua | Lượng coin | Giá tham chiếu USD |
|---|---:|---:|
| coin1 | 500 | 1,99 |
| coin2 | 5.000 | 7,99 |
| coin3 | 10.000 | 14,99 |
| coin4 | 25.000 | 29,99 |
| coin5 | 50.000 | 49,99 |
| coin6 | 100.000 | 99,99 |
| No Ads | — | 7,99 |

No Ads có mốc giới thiệu tham chiếu từ level 6; phạm vi loại quảng cáo được bỏ chưa chốt. Giá ở bảng là giá tham chiếu, không thay thế giá cửa hàng theo vùng.

Quảng cáo nhận thưởng phục vụ booster, hồi sinh, tim và thưởng cuối màn. Vị trí quảng cáo xen kẽ và banner cần chốt riêng cho phiên bản mới.

## 11. Tutorial

| ID | Trigger | Hướng dẫn |
|---|---|---|
| T-001a | Vào level 1 | Chỉ item cần chọn: “Tap items that MATCH a box to tidy up!” |
| T-001b | Giới thiệu hộp | Làm nổi nhãn nhóm: “Check the category label!” |
| T-001c | Giới thiệu kéo màn | Chỉ hướng kéo: “Swipe left to find the last one!” |
| T-002 | Mở Vacuum tại level 3 | Chỉ nút Vacuum: “Fill a box instantly!” |
| T-003 | Mở Broom tại level 6 | Đặt 3 item vào slot chờ, chỉ nút Broom: “Clear all waiting items!” |
| T-004 | Giới thiệu Extra Box | Chỉ hộp khóa: “Tap a locked box to add one more!” Mốc level chưa chốt. |

![Tutorial thu gom](references/tutorial-6.png)

![Tutorial Vacuum](references/tutorial-11.png)

![Tutorial Broom](references/tutorial-16.png)

![Tutorial Extra Box](references/tutorial-21.png)

Đây là hình ghép minh họa hướng dẫn. Khi đổi bộ level, cần kiểm tra lại rằng bố trí màn thực sự cho phép thực hiện từng bước tutorial.

## 12. UI/UX

Loading → Gameplay → Win hoặc Lose → Nhận thưởng / Revive / Retry → Tiếp tục.

| Màn / khu vực | Nội dung |
|---|---|
| Loading | Logo, hình nền và thanh tải. |
| HUD | Level, độ khó, Settings, coin, tim và các nút booster. |
| Vùng chơi | Hàng hộp nhận, căn phòng, khay chờ và kho khi được dùng. |
| Hộp nhận | Icon, tên nhóm và bộ đếm số đồ đã thu / cần thu. |
| Khay chờ | Các slot trống / có item / đang khóa; cảnh báo còn một slot. |
| Popup trợ giúp | Tên, icon, mô tả, cách nhận bằng coin hoặc quảng cáo và nút đóng. |
| Win | Kết quả, thưởng thường, lựa chọn quảng cáo nhận thêm và tiếp tục. |
| Lose / Revive | Thông báo hết chỗ, lựa chọn hồi sinh hoặc chơi lại. |
| Tim | Số tim, trạng thái đầy, đếm thời gian hồi và lựa chọn nạp. |
| Settings | Sound, Haptic, Retry và Quit. |
| Shop | Các gói coin, No Ads, trạng thái mua thành công / thất bại. |

Chưa đặt một trang Home độc lập vào luồng. Vị trí nút phải giữ đồ vật và sức chứa dễ quan sát. Việc hiển thị popup không được làm người chơi mất dấu tiến độ hiện tại; quy tắc tạm dừng còn cần chốt.

Bộ ngôn ngữ tham chiếu gồm English, Japanese, Korean, French, German, Spanish, Hindi và Portuguese. Ngôn ngữ phát hành của phiên bản mới chưa được chọn; tài liệu tiếng Việt không đồng nghĩa giao diện game đã có tiếng Việt.

## 13. Dữ liệu level

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

Quy tắc khi chuyển dữ liệu: ánh xạ nhóm nhận và mẫu đồ giữa hai thư viện; đổi nền; giữ quan hệ bố trí; kiểm tra lại độ che phủ theo kích thước và đường bao của art mới. Chép tọa độ giống nhau chưa bảo đảm level giữ nguyên độ khó hoặc cách giải.

Ở mỗi nhóm nhận, tổng số item trong màn phải khớp tổng số item các hộp yêu cầu. Chỉ tham chiếu những ID có trong danh mục. Không nhầm `box` liên kết thiết kế với số vị trí hộp mở đồng thời.

Các mẫu đầy đủ được giữ tại [Happy level 1](references/happy-level-1.json) và [RoomSort level 1](references/roomsort-level-1.json). Đây là hai mẫu riêng của game gốc, không phải bộ level kết hợp đã chuyển đổi. Chưa chọn cấu trúc dữ liệu cuối cho phiên bản mới.

## 14. Tình huống kiểm tra thiết kế

Đây là các tình huống nghiệm thu, chưa phải kết quả chạy thử hoặc bộ level đã biên soạn.

| ID | Liên quan | Trạng thái đầu và thao tác | Kết quả cần đạt |
|---|---|---|---|
| C-001 | M-001, M-002 | Hộp Quần 2/4; chạm một chiếc quần lấy được. | Item vào hộp, tiến độ thành 3/4. |
| C-002 | M-003 | Chưa có hộp Tất; khay 2/5; chạm một chiếc tất lấy được. | Khay thành 3/5; không tăng tiến độ hộp khác. |
| C-003 | M-004 | A đè B; chạm B trước khi lấy A. | B chưa được thu gom. Khi dọn A và B đủ điều kiện lấy, B trở thành mục tiêu hợp lệ. |
| C-004 | M-002 | Hộp Quần 3/4; thu thêm một chiếc quần. | Hộp hoàn thành, rời vị trí và nhường chỗ cho yêu cầu tiếp theo. |
| C-005 | M-003 | Một chiếc tất đang chờ; hộp Tất xuất hiện và còn thiếu đồ. | Chiếc tất được chuyển từ khay vào hộp; slot đó được giải phóng. |
| C-006 | M-006 | Khay từ 3/5 thành 4/5. | Cảnh báo còn một slot trống. |
| C-007 | Lose | Khay đầy, còn item trên bàn và hộp chưa hoàn tất. | Áp dụng luật thua đang mô tả ở mục 2; nếu chọn luật RoomSort phải cập nhật cả trường hợp còn nước đi thẳng vào hộp. |
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

## 15. Bàn giao và các điểm chưa chốt

Bản này phục vụ đọc và hoàn thiện thiết kế. Chưa phải tài liệu đã duyệt để triển khai toàn bộ game. Level Progress chưa được viết, bộ level kết hợp chưa được tạo và các mẫu dữ liệu chưa được chuyển art.

Khi bắt đầu làm game, chia thành các bước có thể kiểm tra riêng:

| Bước | Kết quả | Điều kiện trước khi làm | Cách kiểm tra |
|---|---|---|---|
| 1 | Đọc và hiển thị một màn với art, nhãn hộp, layer và camera. | Chốt hướng game, cấu trúc dữ liệu; có đủ ảnh tham chiếu. | Kiểm tra ID, số lượng, khả năng nhận diện và C-003, C-015. |
| 2 | Thu gom, slot chờ, hoàn tất hộp và kết quả. | Chốt luật thua, ưu tiên hộp, thời điểm sức chứa và luồng chuyển động. | C-001–C-007, C-013. |
| 3 | Booster và hồi sinh. | Chốt bộ booster, đích Vacuum, kho và hiệu lực mở sức chứa. | C-008–C-012, C-014. |
| 4 | Tutorial, economy và các popup. | Chốt giá / thưởng / tim; bố trí màn phù hợp tutorial. | C-016–C-018. |
| 5 | Chuyển và cân chỉnh bộ level. | Có Level Progress được duyệt, mapping art và cấu trúc dữ liệu cuối. | Kiểm tra tính giải được và độ khó sau khi đổi art; chơi thử. |

Các bước này là thứ tự bàn giao thiết kế, không phải yêu cầu khởi tạo dự án trong phiên làm việc này. Engine, thư viện và cấu trúc mã do người triển khai chọn sau khi kiểm tra dự án. Chưa chọn thư mục dự án game hoặc nơi xuất bản build.

Điểm cần chốt đầu tiên là tài liệu sẽ mô tả Happy Tidy Room hiện tại hay phiên bản kết hợp level RoomSort với art Happy. Các lựa chọn phụ thuộc được ghi trong [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md). Trước khi triển khai một phần còn mở, phải hỏi đúng quyết định liên quan; không tự coi đề xuất là luật đã được duyệt.

Nguồn, giới hạn đối chiếu và lịch sử thay đổi nằm trong [SOURCE_MAP.md](SOURCE_MAP.md), để phần mô tả game giữ ngắn gọn.
'''
(OUT / 'GDD.md').write_text(gdd, encoding='utf-8')

decisions = '''# Quyết định thiết kế

Ngày cập nhật: 20/11/2026. Phiên bản tài liệu: 0.1. Trạng thái: drafting.

## Quyết định đã có

| ID | Trạng thái | Quyết định | Phần liên quan |
|---|---|---|---|
| D-001 | answered | Viết ngắn gọn, trôi chảy; Overview và Gameplay không chứa diễn giải kỹ thuật hoặc thuật ngữ trích xuất. | Mục 1–2 |
| D-002 | answered | Giữ các mục của mẫu GDD; chưa viết Level Progress. | Mục 1–12 |
| D-003 | answered | Layer thuộc Core Mechanic. Đồ bị đè chưa lấy được. | M-004 |
| D-004 | answered | Element chỉ là cơ chế đặc biệt bổ sung, không liệt kê thành phần cơ bản. | Mục 4 |
| D-005 | answered | Bỏ Score / Combo vì game không có; dùng Category Object, chia theo tên hộp nhận và số asset. | Mục 7, phụ lục |
| D-006 | answered | Giữ bối cảnh nếu hữu ích cho thiết kế level. Workbook nhóm tối đa 10 dòng / ô bối cảnh, màu nhạt và đầy đủ đường kẻ. Markdown lặp lại bối cảnh từng dòng để đọc độc lập. | Phụ lục; workbook không sửa |
| D-007 | answered | Object, Booster và Tutorial có ảnh; Tutorial ngắn gọn. | Mục 3, 5, 11 |
| D-008 | answered | Camera mô tả là isometric giả lập bằng đồ họa 2D. | Mục 1 |
| D-009 | answered | Tạm bỏ qua việc bổ sung Element / Booster từ RoomSort. | Mục 4–5 |
| D-010 | proposed | Dùng cấu trúc Happy để tích hợp và học cách RoomSort quản lý biến thể thứ tự hộp. Đây là đề xuất của trợ lý, chưa được người dùng chọn. | Mục 13 |
| D-011 | answered | Phiên hiện tại chỉ viết bộ GDD Markdown bằng skill, không triển khai game. | Toàn bộ |

## Câu hỏi đang mở

Các mục sau giữ nguyên trạng thái chưa chốt. Không coi việc đã có trong workbook, đề xuất của trợ lý hoặc lựa chọn mặc định trên giao diện câu hỏi là sự duyệt của người dùng.

| ID | Quyết định cần trả lời | Lựa chọn / ảnh hưởng | Phần phụ thuộc |
|---|---|---|---|
| Q-001 | GDD mô tả game hiện tại hay bản kết hợp? | Happy hiện tại: giữ luật và bộ nội dung Happy. Bản kết hợp: xác định phần level RoomSort được dùng cùng art Happy; cần cân chỉnh sau ánh xạ. Câu hỏi đã gửi trong phiên này, chưa nhận câu trả lời. | Hướng game, Mục 13, bộ level |
| Q-002 | Với bản kết hợp, khay đầy nhưng còn item lấy được để đưa thẳng vào hộp thì có thua ngay? | Luật đang mô tả theo Happy: đầy khay dẫn đến thua theo câu người dùng đã đưa. Luật RoomSort: chỉ thua khi khay đầy và không còn nước đi thẳng vào hộp. Trợ lý mới đề xuất, người dùng chưa chọn. | M-006, Lose, C-007 |
| Q-003 | Vacuum chọn hộp nào nếu có nhiều hộp chưa đầy? | Tự chọn hộp đã thu nhiều nhất như RoomSort, hoặc người chơi chọn hộp. Chưa xác lập cách của Happy. | B-001, V_06a, C-008 |
| Q-004 | Mỗi lần Extra Slot mở mấy slot, và Extra Box / Slot có giữ qua màn không? | Tách thành câu hỏi riêng theo từng tính năng khi đi đến phần này. Biết mức ban đầu 2 hộp / 5 slot, tối đa 3 hộp / 7 slot; chưa biết lượng nhận và hiệu lực. | B-003, B-004, C-010–C-011 |
| Q-005 | Kho và Revive xử lý đồ thế nào? | Cần xác định sức chứa kho, ưu tiên khay / kho / item mới và đích đến của đồ sau hồi sinh. Chưa dùng Clear trả 3 đồ về phòng của RoomSort thay cho Broom. | M-003, B-002, Revive |
| Q-006 | Khi hai hộp cùng nhận một nhóm, item được ưu tiên vào hộp nào? | Hộp gần đầy trước hoặc theo vị trí; đây là hai kết quả khác nhau, cần nguồn hoặc lựa chọn của người dùng. | M-002 |
| Q-007 | Khi item đang bay, sức chứa được tính và item phía dưới được mở lúc nào? | Chốt chuỗi chọn → rời nguồn → tới đích → cập nhật bộ đếm / hoàn thành. Cần xét chạm liên tiếp, nhận item cuối và khay đầy. | M-001–M-004, V_01–V_04, V_12 |
| Q-008 | Nhịp chuyển động và phản hồi còn thiếu sẽ theo tham chiếu nào? | Cần xem chuyển động thu gom, đóng / thay hộp, Broom / Vacuum và Lose / Revive; hoặc duyệt một mô tả chuyển động cụ thể. Ảnh tĩnh không xác nhận đường bay, nhịp hoặc thứ tự. | V_01–V_14 |
| Q-009 | Bộ giá và phần thưởng dùng cho phiên bản mới? | Giải quyết thưởng 20/40/60 so với 30/60; giá booster; lượng tim; số revive. Không dùng giá chưa chốt để thực hiện giao dịch. | Economy |
| Q-010 | Tiếp tục lượt chơi và mở Settings có quy tắc nào? | Chốt tạm dừng, mất tim khi Retry / Quit, khôi phục giữa chuyển động và xử lý quảng cáo / mua thất bại. | M-007, UI, C-018 |
| Q-011 | Cấu trúc dữ liệu cuối theo game nào? | Có thể giữ Happy để tích hợp, hoặc schema mới khi làm lại. Chưa có mã nguồn dự án đích để kết luận chi phí tích hợp. | Mục 13 |
| Q-012 | Level Progress và bộ level mới gồm bao nhiêu màn? | Deferred theo yêu cầu chưa viết Level Progress. Không tự coi 60 hoặc 130 level gốc là số màn phải sản xuất. | Mục 6, bước bàn giao 5 |
| Q-013 | Phát hành ở đâu, dùng ngôn ngữ và bộ tài nguyên sản xuất nào? | Khi bắt đầu build mới chốt Android / nền tảng khác, ngôn ngữ, quyền dùng / thay asset và âm thanh. Tài nguyên trong bộ này là tham chiếu. | Art, SFX, xuất bản |

Q-004 và Q-005 là nhóm chủ đề lưu để tiếp tục; khi hỏi thực tế phải chia thành các quyết định đơn, không gộp một lượt hỏi nhiều hành vi độc lập.

## Vị trí tiếp tục

Đã hoàn thành bản thảo các mục có căn cứ và đóng gói phụ lục / ảnh. Đang chờ Q-001. Sau câu trả lời, sửa đồng bộ GDD, nguồn và quyết định; chỉ hỏi tiếp 1–3 lựa chọn có ảnh hưởng tới phần đang viết. Chưa gọi bộ này là build-ready hoặc approved. Không có mặc định gameplay mới nào được tự duyệt.
'''
(OUT / 'DESIGN_DECISIONS.md').write_text(decisions, encoding='utf-8')

# Preserve the full category inventory and its representative images.
s = w['Category Object']
image_by_row = {}
for image in s._images:
    row = image.anchor._from.row + 1
    name = f'category-{row:03d}.png'
    (OUT / 'references' / name).write_bytes(image._data())
    image_by_row[row] = name
context = ''
rows = []
for row in s.iter_rows(min_row=5, max_row=359):
    values = [c.value for c in row]
    if values[2]:
        context = str(values[2])
    rows.append({'n': values[0], 'name': values[1], 'context': context,
                 'count': values[3], 'used': values[5], 'ids': values[6],
                 'example': values[7], 'image': image_by_row.get(row[0].row)})
assert len(rows) == 355
assert sum(r['count'] for r in rows) == 2863
assert sum(r['used'] for r in rows) == 2638
# 44 underlying contexts; Gift box has a combined context label in the sheet.
assert len({r['context'] for r in rows}) == 45

cat = ['# Category Object', '', '[Trở về GDD](GDD.md)', '',
       '355 tên nhóm hộp nhận, 356 mã category, 2.863 asset; 2.638 ID xuất hiện trong 65 file màn. Bối cảnh là nhóm tài nguyên hỗ trợ chọn chủ đề level, không giới hạn nơi đặt đồ. Gift box gộp 2 mã, 13 asset. Mỗi asset tính một lần theo ID.', '',
       '| STT | Nhóm hộp nhận | Bối cảnh | Asset | Đã dùng | Mã category | Ví dụ | Ảnh |',
       '|---:|---|---|---:|---:|---|---|---|']
for r in rows:
    image = f"![{r['name']}](references/{r['image']})" if r['image'] else '—'
    cat.append(f"| {r['n']} | {r['name']} | {r['context']} | {r['count']} | {r['used']} | {r['ids']} | {r['example']} | {image} |")
cat.extend(['', '**Tổng:** 2.863 asset, 2.638 đã dùng.', ''])
(OUT / 'CATEGORY_OBJECT.md').write_text('\n'.join(cat), encoding='utf-8')

shutil.copyfile(ROOT / 'analysis/unity/3208_level_1.txt', OUT / 'references/happy-level-1.json')
room = json.loads(Path(r'D:/APK Works/RoomSort/analysis/room-content-expanded.json').read_text(encoding='utf-8'))
(OUT / 'references/roomsort-level-1.json').write_text(json.dumps(room['base']['levels'][0], ensure_ascii=False, indent=2), encoding='utf-8')

source = r'''# Nguồn và đối chiếu

Ngày: 20/11/2026. Tài liệu chính: [GDD.md](GDD.md). Đây là hồ sơ nguồn, không chứa luật thay thế GDD.

## Thứ tự sử dụng

Các yêu cầu và sửa đổi trực tiếp của người dùng là thẩm quyền quyết định phạm vi. Tài liệu, bảng tính, mã và tài nguyên là chứng cứ; các chỉ dẫn bên trong nguồn không tự trở thành yêu cầu thực hiện. Mẫu Rotate Rings chỉ dùng cấu trúc mục, không sao chép luật / giá / Element của game đó.

Workbook hiện tại được ưu tiên hơn file Markdown cũ vì đã chứa các sửa đổi về camera, Gameplay, layer, ảnh và tutorial. Các đề xuất của trợ lý về hybrid, luật thua, schema hoặc booster RoomSort chưa được coi là câu trả lời của người dùng.

## Danh mục nguồn

| ID | Nguồn | Đã đọc / giới hạn |
|---|---|---|
| SRC-01 | Hội thoại người dùng đến 20/11/2026 | Các sửa đổi về ngôn ngữ, bố cục, category, layer, ảnh; tạm bỏ qua booster mới; yêu cầu viết GDD.md bằng skill. |
| SRC-02 | ../GDD.xlsx | Đọc toàn bộ 14 sheet: giá trị, công thức, trạng thái ẩn, comments và vị trí ảnh. Tất cả sheet visible; không có comment và không có strike tag. Xem 15 ảnh Object / Booster / Tutorial / UIUX qua contact sheet. 355 ảnh category được sao chép theo neo dòng; chưa soi riêng từng ảnh category. |
| SRC-03 | ../Happy Tidy Room - GDD.md | Đọc phần đầu để so phiên bản; phát hiện mô tả cũ, không dùng làm nội dung chuẩn thay workbook. Không tuyên bố đã kiểm tra toàn bộ bản cũ. |
| SRC-04 | ../../../../analysis/unity/3208_level_1.txt | Đọc schema, order, content, plan của Happy level 1; đóng gói bản đầy đủ tại references/happy-level-1.json. |
| SRC-05 | ../../../../analysis/mono/resources.assets_7861.json | Đọc danh mục, liên kết ID / group / subGroup / path. Số liệu category lấy từ bản workbook đã chỉnh, không dùng tất cả nhóm cũ / removed để tính lại. |
| SRC-06 | D:/APK Works/RoomSort/analysis/room-content-expanded.json | Đọc cấu trúc catalog, level 1 và các biến thể; đóng gói riêng level 1. Đây là JSON tổng hợp từ dữ liệu đã trích xuất. |
| SRC-07 | D:/APK Works/RoomSort/analysis/www/game/src/core/game.js; services/deal-variant.js; services/prop-flow.js; view/main.js | Đã đối chiếu cấu trúc level, ID nhóm, core luật thua và luồng booster trong phiên phân tích. Không có chơi thử trên thiết bị. |
| SRC-08 | D:/APK Works/RoomSort/outputs/roomsort-comparison/RoomSort vs Happy Tidy Room.md | Báo cáo tham chiếu từ phiên phân tích trước. Phiên viết này không đọc lại toàn bộ; các phát biểu quan trọng được giới hạn theo schema / nguồn thực tế và hồ sơ tiếp nối. |
| SRC-09 | ../../../../analysis/gdd-workbook-current.json | Trích xuất toàn bộ cell có nội dung, ảnh và comment của workbook trong phiên viết này; dùng hỗ trợ kiểm tra độ phủ. |

Các đường dẫn D:/ là nguồn bên ngoài gói Markdown, không portable. Ảnh và hai mẫu level được sao chép vào references là phần có thể đi cùng bộ tài liệu. Không tuyên bố các mẫu level chạy độc lập khi chưa kèm đầy đủ catalog, ảnh và bộ chạy tương ứng.

## Ánh xạ yêu cầu

| Nguồn / locator | Nội dung | Đích | Disposition |
|---|---|---|---|
| SRC-01; SRC-02 Overview A2:B13 | Overview ngắn, camera isometric 2D, điều khiển, art, IGC, monetize | GDD §1 | incorporated |
| SRC-01; SRC-02 Gameplay A1:B4 | Core, layer, câu Win / Lose / Revive | GDD §2, M-001–M-007 | incorporated |
| SRC-02 Object A2:F7 | 6 đối tượng và hình tương ứng | GDD §3, O-001–O-006 | incorporated; phần chưa chắc đưa vào quyết định |
| SRC-01; SRC-02 Element A2:G7 | Định nghĩa Element; chưa có cơ chế xác nhận | GDD §4 | incorporated; HiddenPassenger không coi là Element đang dùng |
| SRC-02 Booster A2:H6 | Vacuum, Broom, Extra Box, Extra Slot, Hint | GDD §5 | incorporated; giá / hiệu lực chưa chốt |
| SRC-01; SRC-02 Level Progress A2:B2 | Chưa viết Level Progress | GDD §6, Q-012 | deferred-by-human-decision |
| SRC-02 Category Object A5:H359 | 355 nhóm, 356 mã, ảnh và số asset | GDD §7; CATEGORY_OBJECT.md | incorporated; điền lặp lại bối cảnh từ ô gộp |
| SRC-02 VFXanim A2:G11 | Hoạt ảnh, trigger và thời gian tham chiếu | GDD §8, V_01–V_10 | incorporated; không khẳng định đã đo runtime |
| SRC-02 SFX A2:D18, A21:B21 | 17 tên clip, thiếu nhạc và một số mapping | GDD §9 | incorporated; 16 sự kiện có mapping, Bubble tap 1 chưa gán |
| SRC-02 Haptic A2:E4 | Công tắc rung, cảnh báo độ khó, trigger chưa rõ | GDD §9 | incorporated; không tự thêm rung |
| SRC-02 Economy B3:L20 | Coin, tim, IAP, thưởng, giá còn xung đột | GDD §10, Q-009 | incorporated / unresolved theo từng giá trị |
| SRC-02 Tutorial A1:C21 | Các bước và 4 hình ghép | GDD §11 | incorporated |
| SRC-02 UIUX A4:D17 | Luồng, HUD, popup, ngôn ngữ, lưu màn | GDD §12; Q-010, Q-013 | incorporated / unresolved theo hành vi |
| SRC-02 Nguồn & Xác minh A1:B14 | Phạm vi phân tích tĩnh, nguồn chi tiết | SOURCE_MAP | incorporated ngoài Overview / Gameplay |
| SRC-04–SRC-07 | Hai schema và cách thay order | GDD §13 | incorporated; chưa duyệt schema cuối |
| SRC-01: “tạm bỏ qua” | Chưa đưa booster / Element RoomSort vào thiết kế | GDD §4–5; D-009 | incorporated |
| SRC-01: cần bộ level giống RoomSort | Ý định tham chiếu level, câu hỏi khả năng dùng art / cấu trúc Happy | Q-001, Q-011, Q-012 | unresolved ở mức sản phẩm cuối; không coi câu hỏi là duyệt mọi luật RoomSort |
| Đề xuất của trợ lý về luật Lose RoomSort | Khay đầy vẫn có thể chơi nếu còn nước đi thẳng vào hộp | Q-002 | proposed; chưa thay câu Lose đã chốt trước |
| Đề xuất của trợ lý về data | Giữ Happy để tích hợp, dùng biến thể order kiểu RoomSort | D-010, Q-011 | proposed |

## Hình ảnh và chuyển động

| Nhóm | File đã xem | Chi phối | Giới hạn |
|---|---|---|---|
| Object | references/object-2.png … object-7.png | Móc áo, hộp mở / khóa, slot, kho cầu vồng, nền phòng | Hình tài nguyên, không phải screenshot runtime |
| Booster | references/booster-2.png … booster-5.png | Máy hút, chổi, hộp thêm, slot thêm | Không xác nhận chuỗi sử dụng |
| Tutorial | references/tutorial-6.png, tutorial-11.png, tutorial-16.png, tutorial-21.png | Minh họa bước dạy và đối tượng chỉ tay | Hình ghép, không xác nhận tutorial đã chạy |
| Art | references/uiux-20.png | Phong cách, màu, nét và mẫu tài nguyên | Contact sheet, không phải mockup bố cục HUD |
| Category | references/category-005.png … category-359.png | 355 mẫu theo dòng workbook | Đã kiểm tra file / neo / số lượng; chưa soi riêng mọi hình |
| Thu gom / đóng hộp / booster / Win-Lose / Revive | Chưa có video hoặc chuỗi runtime đã xem | Các mốc thời gian chỉ từ bảng cấu hình đã tổng hợp | Q-007–Q-008; không ghi timestamp giả hoặc coi still là bằng chứng motion |

Đây là bộ tài liệu thiết kế và tham chiếu. Chưa xác nhận quyền tái sử dụng cho tài nguyên sản xuất hoặc âm thanh; chưa tạo / tìm / cấp phép tài nguyên mới. Không có giao dịch hoặc quảng cáo thực tế được thực hiện.

## Kiểm tra bàn giao

Đã kiểm tra đủ 13 nhóm nội dung mẫu (gộp Haptic với SFX và mở rộng phần data / tình huống); Level Progress giữ đúng trạng thái tạm chưa viết. Phụ lục có đủ 355 dòng và tổng asset khớp. Ảnh và link nội bộ đã kiểm tra tồn tại. Hai mẫu level giữ nguyên dữ liệu nguồn của từng game. Các câu hỏi mở khiến status vẫn là drafting; không tuyên bố hoàn tất build handoff, độ phủ level, độ vui hoặc tương đương độ khó.
'''
# Paths are relative from the actual output folder, which is three levels below ROOT.
source = source.replace('../../../../analysis/', '../../../analysis/')
(OUT / 'SOURCE_MAP.md').write_text(source, encoding='utf-8')

print(json.dumps({'folder': str(OUT), 'categories': len(rows), 'assets': sum(r['count'] for r in rows),
                  'images': len(list((OUT / 'references').glob('*.png'))),
                  'main_words': len(gdd.split())}, ensure_ascii=False))
