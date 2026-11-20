# TidyRoom

Chứa project Unity, bộ tạo level và dữ liệu nguồn của ba game tham chiếu.

## Tải và mở project

Cài [Git LFS](https://git-lfs.com/) trước khi clone để Git tải đầy đủ APK và tài nguyên lớn:

```sh
git lfs install
git clone https://github.com/datluyen-cmyk/TidyRoom.git
cd TidyRoom
```

- **TidyRoom Sort** — Unity **6000.0.78f1**. Thêm thư mục `TidyRoom Sort` vào Unity Hub, mở `Assets/TidyRoom/Scenes/LevelTest.unity`, rồi bấm Play. Xem [hướng dẫn project](TidyRoom%20Sort/README.md).
- **Tidy Room Level Studio** — tool sinh level và pack mẫu. Mở `Open Generator.vbs` để dùng trên trình duyệt. `Open Unity Level Test.cmd` mở bản Unity **2022.3.62f2** để chơi 12 màn sinh mẫu. Xem [hướng dẫn Level Studio](Tidy%20Room%20Level%20Studio/README.md).
- **Level Tool Html5** — editor xếp level bằng kéo thả, chơi thử và xuất hoặc thêm màn vào Unity. Mở `Open Level Tool.cmd` sau khi cài Python và Pillow. Xem [hướng dẫn Level Tool HTML5](Level%20Tool%20Html5/README.md).
- **APK** — APK/APKS và dữ liệu phân tích của Happy Tidy Room, RoomSort và Tidy Room. Các thư viện cài sẵn, cache Unity, thư viện native đã bung riêng, cấu hình Firebase của game tham chiếu và bản sao trùng của Level Studio không được track. Unity tự tải package từ manifest và lockfile; các APK/APKS nguồn dùng Git LFS.

Dữ liệu cần để nhấn Play đã có sẵn trong `Assets`; không cần chạy lại tool chuyển đổi. Để tái tạo dữ liệu của project chính, cài Node.js 20+, Python, Pillow và UnityPy rồi chạy `Tools/Convert-Levels.ps1` trong `TidyRoom Sort`. Script đọc thư mục `APK` bên cạnh project.
