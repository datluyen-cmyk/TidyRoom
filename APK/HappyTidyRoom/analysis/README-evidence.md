# Hồ sơ nguồn APK

Phân tích tĩnh bằng Python, ZIP/XML, UnityPy và TypeTreeGeneratorAPI. REA MCP không có trong phiên, nên đây là kết quả công cụ cục bộ, không phải REA Evidence.

Không chạy APK, không đăng nhập dịch vụ và không thay đổi dữ liệu game gốc.

- puzzle.happy.tidy.room-9-config.arm64_v8a.apk: 33,314,462 bytes; SHA-256 `e917cf13b51ea3bd62275f50a130a9633d5de9f21ebe70124f0d562537311e42`.
- puzzle.happy.tidy.room-9.apk: 311,874,989 bytes; SHA-256 `e72c9e1b6b861ecf0f5accaf6771fff510205c065250682eabfd14360cf42f45`.

## Phạm vi và các điểm chưa chốt

- Đã trích catalog, JSON màn, localization, 3.990 MonoBehaviour, sprite, mapping âm thanh và hằng số metadata. Có 5 MonoBehaviour không giải mã đầy đủ.
- Không viết level progress. Không suy ra tính năng đang hoạt động chỉ từ tên class, asset hoặc SDK có trong APK.
- Chưa xác nhận giá booster hiệu lực, số tim tối đa, lượng tim nạp, giới hạn revive, thưởng thắng hiệu lực, quy tắc No Ads và thứ tự resolve khay/kho.
- Booster coinCost=0 chưa đủ để kết luận miễn phí. maxRevives=0 chưa đủ để kết luận cấm hồi sinh hoặc hồi sinh vô hạn.
- Hằng số thưởng 20/40/60 và preset WinPopup 30/60 khác nhau, cần runtime giải quyết.
- IAP là giá mặc định catalog. Remote Config chỉ là giá trị dự phòng đóng gói.
- Công cụ không decompile thân hàm native. Những luồng suy từ metadata được ghi rõ trong GDD.
