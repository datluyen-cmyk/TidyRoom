---
title: "Tidy Room Sort — GDD"
status: drafting
updated: 2026-11-20
revision: 0.2
scope: "Level RoomSort + art Tidy Room + feeling Happy; chưa viết Level Progress."
---

# Tidy Room Sort — GDD

Game giải đố tìm đồ và phân loại vào hộp. Đồ xếp theo layer; người chơi chọn thứ tự lấy đồ và giữ đủ slot chờ để dọn sạch màn.

**Hướng đã chốt:** Level design theo **RoomSort**, art từ **D:\APK Works\Tidy Room**, cảm giác thao tác và phản hồi theo **Happy Tidy Room**.

## Tài liệu thiết kế

Mỗi chủ đề có một file chuẩn. Đọc Overview và Gameplay trước, sau đó mở phần cần làm; không cần đọc toàn bộ folder để tìm một luật.

| File | Nội dung |
|---|---|
| [Overview](01_OVERVIEW.md) | Ý tưởng, đối tượng chơi, nền tảng và hướng kết hợp. |
| [Gameplay](02_GAMEPLAY.md) | Core loop, layer, thu gom, Win / Lose / Revive. |
| [Object](03_OBJECT.md) | Đồ vật, hộp, slot chờ, kho và bối cảnh. |
| [Element](04_ELEMENT.md) | Cơ chế đặc biệt; chưa bổ sung Element mới. |
| [Booster](05_BOOSTER.md) | Vacuum, Broom, Extra Box, Extra Slot và Hint. |
| [Level Progress](06_LEVEL_PROGRESS.md) | Giữ chỗ theo yêu cầu chưa biên soạn. |
| [Category Object](07_CATEGORY_OBJECT.md) | Cách chia nhóm và yêu cầu kiểm kê art Tidy Room. |
| [Art direction](08_ART_DIRECTION.md) | Art Tidy Room; phân biệt với hình Happy đang dùng đối chiếu. |
| [Animation, VFX và Feeling](09_ANIMATION_VFX.md) | Feeling Happy, sự kiện chuyển động và VFX. |
| [SFX](10_SFX.md) | Trigger và âm thanh tham chiếu. |
| [Haptic](11_HAPTIC.md) | Rung và cài đặt bật / tắt. |
| [Economy](12_ECONOMY.md) | Coin, tim, thưởng, quảng cáo và IAP. |
| [Tutorial](13_TUTORIAL.md) | Các bước hướng dẫn ngắn, có ảnh minh họa. |
| [UI/UX](14_UI_UX.md) | Luồng màn hình, HUD và popup. |
| [Dữ liệu level](15_LEVEL_DATA.md) | Schema hai game, mapping và yêu cầu chuyển art. |
| [Tình huống kiểm tra thiết kế](16_ACCEPTANCE.md) | Các tình huống kiểm tra luật và tương tác. |
| [Bàn giao và điểm chưa chốt](17_HANDOFF.md) | Thứ tự bàn giao và phần còn cần chốt. |

## Hồ sơ đi kèm

- [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md): quyết định đã chốt và các điểm còn mở.
- [SOURCE_MAP.md](SOURCE_MAP.md): nguồn, độ phủ đối chiếu và giới hạn bằng chứng.
- [CATEGORY_OBJECT.md](CATEGORY_OBJECT.md): 355 nhóm và ảnh **tham chiếu Happy**, chưa phải thống kê Tidy Room.
- `references/`: hình minh họa và hai mẫu level gốc, chưa phải bộ asset / level cuối của bản kết hợp.

**Trạng thái:** Đã chốt hướng kết hợp và tổ chức tài liệu. Art Tidy Room chưa được trích xuất / kiểm kê; chuyển động Happy chưa được đối chiếu đầy đủ. Luật thua, một số quy tắc booster và economy còn mở. Không dùng bản này như tài liệu đã duyệt toàn bộ để triển khai.
