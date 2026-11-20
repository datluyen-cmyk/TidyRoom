# Happy Tidy Room — Game Design Document

**Bản phân tích:** APK 0.9 (versionCode 9) · **Ngày:** 20/11/2026

Tài liệu mô tả game từ dữ liệu APK và bám các mục của GDD Rotate Rings. Level Progress tạm chưa biên soạn. Đây là phân tích tĩnh: dữ liệu đóng gói, lời hướng dẫn và tài nguyên đã được đối chiếu; chưa chơi trên thiết bị. Các phần suy luận hoặc cần chơi xác nhận được ghi ngay tại nội dung liên quan.

## 1. Happy Tidy Room — Tổng quan

*Nguồn đối chiếu: S00, S01, S01–S10, S02, S03, S04, S05, S06, S07, S08, S09. Xem mục Nguồn và giới hạn xác minh.*

### Overview

Happy Tidy Room là game giải đố dọn phòng. Người chơi tìm đồ vật giữa một căn phòng bừa bộn và chạm để đưa chúng vào hộp có cùng nhóm. Mỗi hộp hoàn thành giúp căn phòng thoáng hơn, đồng thời mở ra yêu cầu thu gom tiếp theo.

### Core mechanic

Đọc nhãn hộp, tìm đồ phù hợp và chọn thứ tự thu gom. Đồ chưa có hộp nhận phải nằm trong khay chờ có giới hạn. Vì vậy, mỗi lần chạm vừa là tìm đồ, vừa là quyết định sử dụng chỗ trống.

### Ending Rewards

Có thưởng coin khi thắng và lựa chọn nhận thưởng qua quảng cáo. Giá trị cuối cùng chưa chốt: hằng số thưởng là 20/40/60 coin theo độ khó, còn prefab Win lưu 30/60 coin. Xem Economy để phân biệt hai nguồn.

### Màn hình

Chơi theo chiều dọc. Bản Android được phân tích là phiên bản 0.9, versionCode 9, package puzzle.happy.tidy.room. Yêu cầu Android tối thiểu API 24, tương ứng Android 7.0.

### Camera

Căn phòng được minh họa theo góc nhìn chéo từ trên xuống. Người chơi có thể kéo để quan sát phần khác của phòng và dùng thao tác thu phóng để tìm đồ; camera không phải một vật thể cần điều khiển trong câu đố.

### Genre / Sub-genre

Casual puzzle, tìm đồ và phân loại theo nhóm, kết hợp quản lý khay chờ. Áp lực chính đến từ không gian chứa và thứ tự lấy đồ.

### Target Audience

Phù hợp với người thích tìm đồ, sắp xếp và giải đố bằng thao tác đơn giản. Đây là nhận định từ cách chơi và hình ảnh; APK không cung cấp dữ liệu tuổi, giới tính hay chân dung người chơi thực tế.

### Art style

Đồ họa 2D với căn phòng có chiều sâu giả lập. Nội thất dùng màu dịu, còn đồ vật có đường viền và hình khối dễ nhận diện. Các biến thể cùng nhóm khác màu hoặc kiểu dáng để người chơi phân loại bằng ý nghĩa của đồ vật.

### Control

Chạm để chọn đồ. Kéo để dịch chuyển góc quan sát; pinch để thu phóng. Một số popup có hướng dẫn giữ để xem lại bản đồ, nhưng cần chơi xác nhận popup nào đang bật chức năng này.

### Monetize

Có quảng cáo nhận thưởng, quảng cáo xen kẽ, banner và IAP. Các điểm đổi quảng cáo lấy lợi ích gồm trợ giúp, hồi sinh, tim và thưởng cuối màn. IAP gồm No Ads và sáu gói coin.

### IGC

Coin là tiền mềm. Tim giới hạn khả năng tiếp tục chơi sau thất bại; số lượng booster là một tài nguyên riêng. Khay, hộp và kho là tài nguyên trong màn, không phải tiền tệ.

### USP

Sự kết hợp giữa tìm đồ trong phòng và giải quyết nhu cầu của hộp đang mở tạo ra lựa chọn có tính chiến thuật. Chọn được món nhìn thấy chưa chắc đã tốt: người chơi còn phải cân nhắc hộp nhận, đồ bị che và số ô chờ còn lại.

### Phạm vi tài liệu

Tài liệu bám 13 mục của GDD Rotate Rings, đổi Ring Object thành Đồ vật & Hộp. Level Progress được giữ chỗ nhưng chưa biên soạn. Các mục khác mô tả bản APK hiện có, không lấy cơ chế, giá hoặc thông số của Rotate Rings để điền sang.

### Cách đọc

Cấu hình APK là giá trị lưu trong gói cài đặt, chưa bảo đảm giống giá trị sau Remote Config. Tổng hợp cơ chế là mô tả rút ra từ UI, dữ liệu và tên hàm. Cần chơi xác nhận là phần chưa đủ bằng chứng để coi là hành vi thực tế. Chưa chạy game hoặc xác nhận giao dịch/quảng cáo trực tiếp.

## 2. Gameplay — Luật chơi và vòng lặp

*Nguồn đối chiếu: S02, S04, S05, S07, S08. Xem mục Nguồn và giới hạn xác minh.*

### Mục tiêu

Hoàn tất tất cả hộp thu gom của màn. Lời nhắc trong game là “COMPLETE all the boxes to win!”. Mỗi hộp yêu cầu một nhóm đồ và một số lượng cụ thể.

### Vòng lặp chính

Quan sát các hộp đang mở → tìm đồ đúng nhóm có thể lấy → chạm để thu gom → hộp nhận đủ đồ và hoàn thành → hộp tiếp theo xuất hiện → tiếp tục cho đến khi hoàn tất toàn bộ yêu cầu.

### Đồ phù hợp với hộp

Khi có hộp đang nhận nhóm đồ tương ứng và còn chỗ, món được chọn được đưa về hộp. Bộ đếm của hộp cho người chơi biết tiến độ thu gom. Đây là phân loại theo nhóm, không đòi mọi món phải giống hệt hình ảnh hay màu sắc.

### Đồ chưa có hộp nhận

Món chưa được hộp đang mở tiếp nhận sẽ chiếm một ô khay chờ. Việc lấy trước có thể giúp lộ đồ phía dưới, nhưng cũng làm giảm khoảng trống để xử lý những lượt sau.

### Giải phóng khay

Hệ thống có bước giải quyết đồ đang chờ khi hộp thay đổi, giúp chuyển đồ phù hợp về hộp. Kho tạm cũng có luồng trả đồ về hộp. Cần chơi xác nhận thứ tự ưu tiên nếu cùng lúc có nhiều nguồn đồ hợp lệ.

### Đồ bị che

Đồ vật có lớp hiển thị và quan hệ chặn. Người chơi cần lấy món phía trên để tiếp cận món phía dưới. Không nên mô tả luật là “hễ thấy một phần là lấy được”: ngưỡng chọn còn phụ thuộc kiểm tra vùng hình ảnh và mức che.

### Win

Hoàn tất toàn bộ hộp sẽ chuyển sang chuỗi kết màn, hiển thị hiệu ứng thắng, phần thưởng và nút sang màn kế tiếp. Trạng thái căn phòng sạch dần là phản hồi trực quan cho tiến độ.

### Lose

Khay chờ hết chỗ là tình huống thất bại được UI nêu rõ bằng “Waiting slots are full!” và “Out of space!”. Thời điểm kiểm tra sau khi đồ đang bay được xử lý xong cần chơi xác nhận.

### Revive

Popup đề nghị hồi sinh và dọn khay để tiếp tục màn hiện tại, bằng quảng cáo hoặc coin. Giá trị hằng số chi phí là 800 coin. Hệ thống hồi sinh được bật; chưa kết luận số lần tối đa vì maxRevives lưu 0 nhưng chưa xác nhận cách code diễn giải giá trị này.

### Replay / Quit

Có Retry, Replay và Quit. Hộp xác nhận nhắc người chơi có thể mất tim khi bỏ lượt. Không nên suy ra cứ mở màn là trừ tim ngay; thời điểm trừ tim và xử lý đóng ứng dụng cần kiểm tra trực tiếp.

### Giới hạn thời gian / lượt

Trong cấu hình gameplay và nội dung UI đã trích chưa thấy đồng hồ đếm ngược hoặc giới hạn số lần chạm cho câu đố chính. Tạm mô tả là giải đố theo sức chứa, chưa khẳng định mọi chế độ đều không có giới hạn thời gian.

### Nhịp quyết định

Người chơi nên ưu tiên hoàn thành hộp sớm để đổi yêu cầu và giải phóng khay. Lấy một món chưa có hộp nhận là đánh đổi giữa mở đường trên bàn và rủi ro hết chỗ.

## 3. Đồ vật & Hộp — Đối tượng chính

*Nguồn đối chiếu: S02, S03, S04, S05, S07, S10. Xem mục Nguồn và giới hạn xác minh.*

### Đồ vật thu gom

Đồ vật là các sprite riêng đặt rải và chồng lên nhau trong căn phòng. Mỗi món có nhóm phân loại, vị trí, góc xoay và biến thể hình ảnh. Các trạng thái được khai báo gồm trên bàn, đang bay, trong hộp, trong khay và trong kho.

### Nhóm và biến thể

Một nhóm có thể chứa nhiều hình khác nhau, chẳng hạn giày, tất, quần, áo, mũ hoặc móc áo. Nhãn hộp là căn cứ chọn món. Cùng màu không đồng nghĩa cùng nhóm; cùng nhóm cũng không cần giống hệt nhau.

### Ví dụ yêu cầu hộp

Một dữ liệu màn có hộp nhận 3 túi xách, 3 mũ, 4 móc áo và 4 quần. Các số này minh họa rằng sức chứa thay đổi theo từng yêu cầu; không có cơ sở dùng một quy tắc cố định 3 món cho mọi hộp.

### Hộp đang mở

Mỗi hộp hiển thị loại đồ cần thu và bộ đếm. Cấu hình khởi đầu có 2 hộp mở cùng lúc. Hộp hoàn thành sẽ đóng, rời vị trí và nhường chỗ cho yêu cầu tiếp theo.

### Hộp khóa

Bàn có tối đa 3 vị trí hộp, trong đó một vị trí có thể ở trạng thái khóa. Extra Box mở thêm hộp, giúp người chơi xử lý nhiều nhóm đồ hơn cùng lúc. Chưa xác minh mở hộp có kéo dài sang màn sau hay không.

### Khay chờ

Khay mặc định có 5 ô. Mỗi món chưa được nhận chiếm một ô, tạo ra giới hạn dễ đọc cho người chơi. Scene còn có 2 ô bổ sung và hệ thống mở ô; đây là phần mở rộng, không tính vào sức chứa mặc định.

### Kho tạm

Kho là nơi nhận đồ được Broom chuyển ra khỏi khay. Mục đích của thao tác này là lấy lại chỗ trống mà vẫn giữ đồ trong luồng thu gom. Chưa xác minh giới hạn kho và thứ tự trả đồ khi nhiều hộp có thể nhận.

### Phông phòng

Phòng là nền bối cảnh cho đồ vật, có nội thất minh họa sẵn. Catalog chứa 60 mục nền. Không có bằng chứng trong phần đã đọc cho một hệ thống tự mua và đặt nội thất để trang trí phòng.

### Quy mô thư viện

Catalog chứa 2.863 mục đồ vật, 76 mục nhóm và 607 mục nhóm con; một số nhóm mang cờ removed. Đây là quy mô dữ liệu đóng gói, không phải cam kết tất cả đều xuất hiện trong bản chơi hoặc đều đang được sử dụng.

![Ví dụ tài nguyên gốc trích từ APK](D:/APK Works/HappyTidyRoom/analysis/visuals/asset-contact-sheet.png)

*Ảnh tài nguyên gốc, không phải ảnh gameplay đang chạy.*

## 4. Element — Các yếu tố tạo câu đố

*Nguồn đối chiếu: S02, S04, S05, S07, S10. Xem mục Nguồn và giới hạn xác minh.*

### Lớp đồ chồng nhau

Các món phía trên che và chặn món phía dưới, khiến người chơi phải chọn thứ tự dọn. Khi một món được lấy đi, thông tin mới lộ ra và có thể tạo cơ hội hoàn tất hộp.

### Yêu cầu hộp theo thứ tự

Danh sách hộp của màn được lưu riêng với vị trí đồ. Do chỉ mở một phần số hộp tại một thời điểm, người chơi phải cân nhắc giữa nhu cầu hiện tại và những món đang nhìn thấy.

### Cảnh báo sắp đầy

Khi còn 1 ô chờ, cấu hình có cảnh báo ô cuối và hiệu ứng cảnh báo màn hình. Cảnh báo giúp người chơi nhận ra rủi ro trước khi khay hết chỗ.

### Ô chờ bổ sung

Extra Slot có mô tả “Add empty slots to the tray.” và scene có 2 ô bổ sung. Cần chơi xác nhận một lần mua mở bao nhiêu ô, giá và hiệu lực của lần mở.

### Nhãn độ khó

HUD có biểu tượng Hard và Very Hard; màn mở đầu có animation Hard / SuperHard. Đây là cách báo độ khó cho người chơi. Chưa phân tích phân bổ độ khó theo màn trong tài liệu này.

### Cơ chế đặc biệt khác

MechanicDatabase trong APK hiện là danh sách rỗng. Có sẵn popup mở khóa cơ chế, nhưng sự tồn tại của popup không chứng minh có thêm cơ chế đang chạy. Chưa ghi nhận bom, băng, chìa khóa hay dây xích cho Happy Tidy Room.

## 5. Booster — Trợ giúp và điều kiện sử dụng

*Nguồn đối chiếu: S02, S04, S07, S08. Xem mục Nguồn và giới hạn xác minh.*

### Vacuum — Công dụng

Hoàn tất ngay 1 hộp, được mô tả bằng “Instantly complete 1 box!”. Hiệu ứng máy hút bụi thu gom đồ phục vụ hộp mục tiêu. Chưa xác nhận người chơi tự chọn hộp hay hệ thống tự ưu tiên hộp nào.

### Vacuum — Mở khóa

Mở ở level 3. Tutorial lưu phần cấp 2 lượt dùng và lời nhắc “Fill a box instantly!”. Nếu không có hộp phù hợp, UI có thông báo “No box can be filled”.

### Broom — Công dụng

Chuyển toàn bộ đồ trong khay chờ sang kho tạm để lấy lại chỗ trống. Đây là thao tác dọn khay, không phải xáo trộn bố cục hoặc xóa đồ khỏi mục tiêu màn.

### Broom — Mở khóa

Mở ở level 6. Tutorial lưu phần cấp 2 lượt dùng, đặt sẵn 3 món trong khay và hướng dẫn “Clear all waiting items!”. Nếu khay trống, UI báo “No items in the waiting slots”.

### Extra Box

Chạm hộp khóa để mở thêm một hộp, tối đa 3 hộp cùng lúc theo cấu hình. Tutorial có lời nhắc “Tap a locked box to add one more!” và giá trị cấp 1 lượt. BoosterDatabase chỉ có Vacuum và Broom nên chưa xác định mốc mở Extra Box.

### Extra Slot

Mở thêm chỗ chứa trong khay để giảm áp lực sắp đầy. Scene có các ô bổ sung và popup có icon riêng, nhưng không có cấu hình mở khóa/giá đầy đủ trong BoosterDatabase đã đọc.

### Luồng dùng / mua

Bấm trợ giúp đã mở khóa để kích hoạt khi có lượt dùng. Popup mua có lựa chọn quảng cáo hoặc coin và được cấu hình dùng ngay sau khi mua. Metadata có kiểm tra mở khóa, số lượng, tính khả dụng và trạng thái đang thi triển.

### Giá và quảng cáo

Cả Vacuum và Broom lưu coinCost = 0 trong database, đồng thời có hàm lấy giá riêng. Vì chưa đọc thân hàm và chưa mở popup trực tiếp, không kết luận giá bằng 0. Hằng số AdAmount lưu 1, là lượng cấp cấu hình cho luồng quảng cáo booster.

### Gợi ý tự động

Hint được bật và có delay 7 giây không thao tác. Gợi ý dùng viền vàng cùng nhịp phóng nhẹ để thu hút chú ý. Không có cơ sở tính hint là một booster phải mua trong bản này.

## 6. Level Progress

*Nguồn đối chiếu: S00. Xem mục Nguồn và giới hạn xác minh.*

### Chưa biên soạn

Tạm thời không viết bảng tiến trình, thứ tự màn hay đường cong độ khó theo yêu cầu. Các mốc mở booster vẫn nằm trong Booster và Tutorial để các mục đó có đủ thông tin.

## 7. Score / Combo Text — Tiến độ và thông báo

*Nguồn đối chiếu: S04, S07. Xem mục Nguồn và giới hạn xác minh.*

### Score

Chưa thấy bằng chứng cho hệ thống cộng điểm theo từng món hoặc bảng điểm tổng của người chơi trong gameplay đã trích. Tài liệu không tự bổ sung công thức điểm của Rotate Rings.

### Combo

Chưa thấy chuỗi combo, hệ số thưởng khi chọn liên tiếp hay bộ lời khen Sweet → Incredible trong phần dữ liệu Happy Tidy Room đã đọc. Mục này được giữ để bám mẫu, không coi combo là tính năng có sẵn.

### Phản hồi tiến độ

Tiến độ được truyền đạt bằng số đồ trong hộp, số ô khay còn lại, hộp hoàn thành và số đồ còn trên bàn. Đây là các tín hiệu có tác dụng trực tiếp lên quyết định của người chơi.

### Text mục tiêu

“COMPLETE all the boxes to win!” nhắc điều kiện thắng. “Almost there!” tạo phản hồi khích lệ gần cuối; chưa xác nhận chính xác ngưỡng xuất hiện câu này.

### Text thất bại / cứu trợ

“Out of space!” và “Waiting slots are full!” giải thích nguyên nhân thua. “Revive and clear the holding tray!” nêu lợi ích hồi sinh. Thông báo ưu tiên giải thích tình huống và hành động tiếp theo.

### Text không thể dùng

“No items in the waiting slots”, “No box can be filled”, “No more boxes to open” và “Not available right now” là các phản hồi cho trợ giúp không có mục tiêu hoặc chưa khả dụng.

## 8. VFX / Animation — Phản hồi hình ảnh

*Nguồn đối chiếu: S02, S07, S10. Xem mục Nguồn và giới hạn xác minh.*

### Chạm chọn đồ

Có hiệu ứng click, select và collect riêng. Chúng giúp xác nhận món vừa được chọn và theo dõi món rời khỏi đống đồ; hình thức cuối cùng cần đối chiếu khi chạy game.

### Đồ bay vào đích

Cấu hình lưu thời gian bay 0,5 giây. Trước khi bay, đồ có nhịp nảy lên 0,12 giây và hạ 0,10 giây, scale nảy 1,3 lần. Các giá trị này mô tả preset chuyển động, không phải số đo video.

### Hộp bắt đầu / chờ

Hộp có animation vào màn, chờ, nhận đồ và trạng thái khóa. Ba vị trí hộp được đưa vào theo nhịp lệch 0,12 giây, tạo cảm giác lần lượt mở ra.

### Hoàn thành hộp

Có animation Box_Com, Box_com_idle và âm đóng hộp. Cấu hình chờ hộp tiếp theo 0,8 giây; luồng bay về hộp lưu thời gian 0,7 giây. Cần xem runtime để chốt tổng thời gian một chuỗi hoàn thành.

### Kho tạm

Kho có chuỗi xuất hiện, chờ, hoạt động và kết thúc. Scene lưu thời gian xuất hiện 0,3 giây. Các món bay từ kho có nhịp lệch cấu hình 0,12 giây để người chơi dễ theo dõi.

### Broom / Vacuum

Broom có hiệu ứng quét dọn; Vacuum dùng animation máy hút bụi và luồng hút về đích. Tài liệu mô tả theo tên tài nguyên và hệ thống trợ giúp, chưa khẳng định từng khung hình chuyển động.

### Gợi ý

Viền gợi ý màu vàng, độ tăng scale 0,1. Nhịp cấu hình gồm hiện 0,4 giây, giữ 0,5 giây, ẩn 0,4 giây và nghỉ 0,2 giây. Hint được gọi sau 7 giây đứng yên.

### Cảnh báo khay

Ô cuối có nhịp nhấp nháy cấu hình 0,45 giây. Cảnh báo màn có chu kỳ 1 giây và thời gian hiển thị cấu hình 2 giây. Trigger dựa trên ngưỡng còn 1 ô chờ.

### Thắng / thua

Có bộ animation riêng cho Win, Lose và chữ kết quả. WinPopup lưu hiệu ứng ở các mốc 0,20 và 0,25 giây; config lưu thời gian chờ popup thắng 2 giây. Các mốc này không được cộng thành một tổng thời lượng chưa kiểm chứng.

### Mở hộp / thêm ô / hồi sinh

Có các clip Box_AddSlot, AnimAddSlots và Revive. Chúng phản hồi việc người chơi vừa tăng khả năng chứa hoặc tiếp tục màn sau thất bại.

## 9. SFX — Âm thanh theo hành động

*Nguồn đối chiếu: S07, S10. Xem mục Nguồn và giới hạn xác minh.*

### Nút UI

File “Button click” được gắn cho hành động button, âm lượng cấu hình 1,0. Dùng để phản hồi thao tác lên nút.

### Chọn đúng đồ

“Bubble tap 2 (1)” gắn cho Correct_Item_Pick, âm lượng 1,0. “Bubble tap 1” cũng có mapping riêng. Chưa xác minh trường hợp lựa chọn giữa hai tiếng tap.

### Chạm không hợp lệ

“tap_wrong” được gắn cho Tap_wrong, âm lượng 0,2. Là phản hồi âm thanh cho thao tác không được chấp nhận; không đồng nghĩa mọi món chưa có hộp nhận đều là thao tác sai.

### Đồ vào hộp

“Item Drop Into Box” gắn cho Item_Drop_Into_Box, âm lượng 1,0. Đây là âm xác nhận đồ đã đến hộp.

### Hộp vào / đóng / rời đi

“sfx_box_in” có âm lượng 0,3; “box_close” và “Box Disappears” có âm lượng 1,0. Ba tiếng tách phản hồi cho từng giai đoạn của hộp.

### Booster

Có hai file “Broom booster” và “Vaccum booster”, đều được gắn trong bảng âm thanh với âm lượng 1,0.

### Gợi ý

“sfx_hint” gắn cho Hint, âm lượng 0,5. Chưa xác nhận âm phát ở mọi nhịp gợi ý hay chỉ lúc bắt đầu.

### Bắt đầu / kết màn

Có “Start level”, “sfx_level_end”, “win_sfx” và “lose_sfx”. Âm lượng mapping đều là 1,0.

### Coin / mua hàng

“coin_sfx” được dùng cho coin và get_coin. “purchase_sfx” dùng cho purchase. Âm lượng mapping là 1,0.

### Nhạc nền / âm còn thiếu

Trong 17 AudioClip đã liệt kê chưa xác định được file nhạc nền Home hoặc Gameplay. Hai mapping revive và claim_reward có tham chiếu clip rỗng. Không tự thêm nhạc hoặc tiếng hồi sinh từ mẫu.

## 10. Economy — Coin, tim và thương mại

*Nguồn đối chiếu: S04, S06, S07, S08, S09. Xem mục Nguồn và giới hạn xác minh.*

### Coin ban đầu

Hằng số NEW_USER_START_COIN lưu 600 coin. Đây là preset trong code, chưa xác nhận số dư tài khoản mới sau các lần cấp thưởng hoặc cấu hình từ xa.

### Coin miễn phí

SHOP_FREE_COIN_AMOUNT lưu 50 coin. Có luồng quảng cáo và shop trong game, nhưng điều kiện nhận, cooldown và số lượt nhận khoản 50 coin chưa được xác minh.

### Thưởng thắng theo độ khó

LEVEL_WIN_REWARD_EASY / HARD / SUPER_HARD lần lượt lưu 20 / 40 / 60 coin. Có hàm GetLevelWinReward. Chưa đọc thân hàm để khẳng định màn thắng thực tế luôn nhận đúng các số này.

### Thưởng trong WinPopup

Prefab lưu coinClaim = 30 và coinClaimAd = 60, đồng thời có nút nhận thường và nhận qua quảng cáo. Giá trị này khác bộ hằng số phía trên. Không chốt hệ số x2 cho mọi độ khó trước khi kiểm tra giá trị được gán khi mở popup.

### Chi phí hồi sinh

REVIVE_COIN_COST lưu 800 coin. Popup có nút quảng cáo, nút coin và bỏ cuộc. Phần thưởng được mô tả là hồi sinh và làm trống khay để chơi tiếp.

### Chi phí nạp tim

REFILL_HEART_COST lưu 700 coin. Popup có lựa chọn coin hoặc quảng cáo và bộ đếm hồi tim. Chưa xác nhận 700 coin nạp đầy toàn bộ hay cấp số tim cụ thể.

### Hồi tim theo thời gian

TIME_HEART_COUNTDOWN lưu 1.800 giây, tương đương 30 phút. Có hệ thống đồng bộ tim và thời gian. Số tim tối đa được lấy qua hàm GetMaxHeart, chưa xác định từ cấu hình đã đọc.

### Giá booster

Popup hỗ trợ mua bằng coin hoặc quảng cáo. Database ghi coinCost = 0 cho Vacuum và Broom, nhưng có hàm tính giá riêng nên giá thực tế còn mở. Không sử dụng giá Airplane / Magic Wand của Rotate Rings.

### IAP — No Ads

SKU puzzle.happy.tidy.room.noads, loại mua một lần, giá mặc định catalog 7,99 USD. Reward catalog bật removeAds. Phạm vi loại quảng cáo được loại bỏ và việc còn cho dùng quảng cáo tự nguyện cần xác nhận trực tiếp.

### IAP — 500 coin

SKU coin1 cấp 500 coin, giá mặc định catalog 1,99 USD.

### IAP — 5.000 coin

SKU coin2 cấp 5.000 coin, giá mặc định catalog 7,99 USD.

### IAP — 10.000 coin

SKU coin3 cấp 10.000 coin, giá mặc định catalog 14,99 USD.

### IAP — 25.000 coin

SKU coin4 cấp 25.000 coin, giá mặc định catalog 29,99 USD.

### IAP — 50.000 coin

SKU coin5 cấp 50.000 coin, giá mặc định catalog 49,99 USD.

### IAP — 100.000 coin

SKU coin6 cấp 100.000 coin, giá mặc định catalog 99,99 USD. Tất cả giá IAP ở đây là giá mặc định đóng gói, có thể khác giá theo vùng và giá cửa hàng tại thời điểm chơi.

### Rewarded Ads

Có các điểm nhận lợi ích cho booster, revive, tim và cuối màn. Remote Config mặc định đặt mốc khả dụng của các luồng này ở level 1. Đây là cấu hình dự phòng, không phải bằng chứng quảng cáo sẽ luôn tải thành công.

### Interstitial / Banner

Remote Config mặc định bật quảng cáo, interval 120 giây và cờ banner gameplay bật. Có khoảng cách cấu hình 15 giây sau rewarded trước interstitial. Chưa xác minh vị trí chèn quảng cáo và cách bộ đếm được áp dụng trong một phiên.

### Giới thiệu No Ads

Giá trị lịch mặc định bắt đầu ở level 6 và lặp theo khoảng 10 level. Đây là tham số của lời mời mua, không khẳng định popup chắc chắn hiện đúng các mốc này vì còn điều kiện lịch và trạng thái quảng cáo.

## 11. Tutorial — Hướng dẫn người chơi

*Nguồn đối chiếu: S02, S04, S07, S09. Xem mục Nguồn và giới hạn xác minh.*

### Mục tiêu hướng dẫn

Dạy người chơi đọc nhóm trên hộp trước, sau đó tìm và chạm đồ phù hợp. Mỗi bước giải thích gắn với thao tác ngay trong căn phòng, dùng lời nhắc, bàn tay và vùng làm nổi bật.

### Level 1 — Mở đầu

Có hai câu giới thiệu: “Uh-oh, look at this mess...” và “Let’s tidy up together!”. Lời nhắc chính là “Tap items that MATCH a box to tidy up!”. Cấu hình đặt tutorial lõi ở level 1.

### Level 1 — Đọc hộp

Tooltip “Check the category label!” hướng sự chú ý vào nhãn hộp. Sau đó “Tap to collect matching items” hướng dẫn chọn món cùng nhóm. Người chơi được dạy mối quan hệ giữa hộp và đồ thay vì chỉ chạm theo màu.

### Level 1 — Quan sát phòng

Bước kéo có câu “Swipe left to find the last one!”, bật bàn tay chỉ dẫn và thời gian pan cấu hình 1,2 giây. Hướng dẫn cho thấy một phần đồ nằm ngoài khung nhìn ban đầu.

### Level 3 — Vacuum

Database mở Vacuum ở level 3. Tutorial có lời nhắc “Fill a box instantly!”, phần cấp 2 lượt và cờ hiển thị một lần. Cần chơi xác nhận thời điểm cấp/tiêu lượt khi hoàn tất bài hướng dẫn.

### Level 6 — Broom

Database mở Broom ở level 6. Tutorial chuẩn bị 3 món trong khay, cấp cấu hình 2 lượt và yêu cầu “Clear all waiting items!”. Tình huống này làm rõ lợi ích giải phóng khay bằng một ví dụ cụ thể.

### Extra Box

Tutorial có câu “Tap a locked box to add one more!” và lượng cấp 1. Mốc xuất hiện chưa chốt do BoosterDatabase đóng gói không có bản ghi Extra Box.

### Cách trình bày

Overlay làm nổi bật mục tiêu, bàn tay minh họa thao tác và tooltip giải thích ngắn. Cấu hình booster tutorial có showOnce = 1; cách lưu hoàn thành qua cài lại game chưa được kiểm tra.

### Gợi ý sau tutorial

Khi không thao tác 7 giây, hệ thống hint có thể hướng chú ý vào đồ phù hợp bằng viền vàng và nhịp scale. Remote Config còn có khóa điều khiển mốc đóng hint, nên cần kiểm tra trạng thái hiệu lực trong bản chạy.

## 12. Haptic — Phản hồi rung

*Nguồn đối chiếu: S04, S07, S08. Xem mục Nguồn và giới hạn xác minh.*

### Cài đặt

Settings có công tắc Haptic. Đây là lựa chọn của người chơi để bật hoặc tắt phản hồi rung.

### Điểm gọi rung

Metadata có hàm GameSfx.Haptic và hệ thống AudioAndVibrationManager. Chưa xác định đầy đủ rung gắn với chọn đúng, chọn sai, hoàn thành hộp hay booster, vì chưa theo vết thân hàm lúc chạy.

### Cảnh báo độ khó

GameplayWarningUI lưu hai mốc rung 0,2 giây và 1,3 giây. Amplitude cho Hard là 150, Very Hard là 190; duration cấu hình 300 ms. Đây là preset của cảnh báo mở màn, chưa đo trên thiết bị.

### Các tình huống khác

Chưa chốt độ dài, số nhịp hoặc cường độ rung cho những hành động khác. Các giá trị này để trạng thái cần chơi xác nhận, tránh biến một phản hồi mong muốn thành tính năng đã có.

## 13. UI / UX — Màn hình và luồng tương tác

*Nguồn đối chiếu: S02, S03, S04, S06, S06–S09, S07, S08. Xem mục Nguồn và giới hạn xác minh.*

### Luồng tổng thể

Loading → gameplay → kết quả thắng hoặc khay đầy → nhận thưởng / hồi sinh / chơi lại → tiếp tục. Có các popup Settings, Shop, mở khóa booster, No Ads, thiếu tim và đánh giá game. Chưa đủ bằng chứng để thêm một trang Home độc lập vào luồng.

### Loading

Có logo, nền, biểu tượng và thanh tải cùng transition giữa scene. Vai trò là đưa người chơi vào bàn chơi và báo trạng thái chuẩn bị nội dung.

### HUD gameplay

HUD có level, nhãn độ khó, Settings, thanh tim/coin và hai nút booster thường trực. Bàn chơi có hàng hộp, vùng căn phòng, khay chờ và kho khi được dùng. Vị trí pixel và safe area cuối cùng cần đối chiếu trên thiết bị.

### Quan sát và chọn đồ

Nhìn nhãn hộp để biết cần lấy gì, chạm đồ trên bàn để thu gom. Kéo và pinch phục vụ tìm đồ. Tài nguyên có kiểm tra tap/drag riêng để phân biệt chạm chọn với dịch chuyển camera.

### Hộp / khay

Hộp truyền đạt mục tiêu bằng icon, tên nhóm và bộ đếm. Khay truyền đạt rủi ro bằng số ô trống cùng cảnh báo sắp đầy. Nhịp đồ bay cho thấy món đang đến đâu, giảm phụ thuộc vào việc đọc text.

### Popup mua trợ giúp

Hiển thị tên, mô tả, icon và hai lựa chọn quảng cáo/coin, kèm nút đóng. Cấu hình useImmediately bật, vì vậy luồng mua được thiết kế để dùng ngay. Giá cụ thể còn cần xác nhận.

### Popup thắng

Hiển thị level, animation thắng và lựa chọn nhận thưởng thường hoặc qua quảng cáo. Sau khi nhận, người chơi chuyển tới màn tiếp. Hai số thưởng preset của prefab là 30/60 coin, cần đối chiếu cơ chế gán thưởng.

### Popup khay đầy / hồi sinh

Giải thích thiếu chỗ và đề nghị hồi sinh để dọn khay. Có quảng cáo, coin hoặc bỏ cuộc. Popup thua có Replay; một số nội dung UI hỗ trợ giữ để xem bản đồ trước khi quyết định.

### Popup tim

Có hai trạng thái “Refill your heart!” và “Out of lives!”, bộ đếm “Next life in:”, trạng thái Full và nút coin/quảng cáo. Nó giúp người chơi biết khi nào có thể tiếp tục và cách nhận thêm tim.

### Settings

Có Sound, Haptic, Retry và Quit. Rời hoặc chơi lại có hộp xác nhận mất tim. Cần kiểm tra trò chơi có tạm dừng hoàn toàn khi mở Settings hay không.

### Shop / No Ads

Shop có sáu gói coin và nhóm No Ads. Có popup báo mua thành công, mua thất bại và tải giao dịch. Giá hiển thị hiệu lực phụ thuộc cửa hàng, không dùng giá catalog để giả lập kết quả mua.

### Ngôn ngữ

Bảng IngameUI có English, Japanese, Korean, French, German, Spanish, Hindi và Portuguese. Chưa thấy cột tiếng Việt trong bảng này. GDD viết tiếng Việt để phân tích, không ngụ ý game đã hỗ trợ tiếng Việt.

### Lưu tiến độ màn

Có cấu trúc lưu trạng thái board, hộp, khay, kho và hồi sinh. Hệ thống có xử lý pause và mở lại. Cần kiểm tra trực tiếp các trường hợp tắt ứng dụng giữa animation hoặc ngay sau thua trước khi kết luận mọi trạng thái đều được khôi phục.

### Điểm cần kiểm chứng tiếp

Ưu tiên chơi xác nhận: giá và lượng nhận khi mua trợ giúp; số tim tối đa và thời điểm mất tim; số lần hồi sinh; thưởng thắng thực nhận; phạm vi No Ads; thứ tự chuyển đồ từ khay/kho; khả năng lưu màn. Các điểm này chưa ngăn việc mô tả vòng lặp chính nhưng ảnh hưởng tới việc tái tạo chính xác game.

## 14. Nguồn và giới hạn xác minh

### S00

Mẫu GDD — D:\[Rotate Rings] GDD.xlsx
Đọc cấu trúc 13 sheet và các trường. Chỉ dùng làm mẫu bố cục, không dùng luật hoặc giá của Rotate Rings làm dữ liệu Happy Tidy Room.

### S01

Nhận diện bản APK — AndroidManifest.xml; manifest-attrs
Package puzzle.happy.tidy.room, versionName 0.9, versionCode 9, minSdkVersion 24, targetSdkVersion 36, activity chính portrait. Unity 6000.0.66f2.

### S02

Cấu hình gameplay — analysis/mono/resources.assets_10789.json
GameplayConfig: 5 ô, 2 hộp mở, tối đa 3 hộp; hint, cảnh báo, hoạt ảnh, cờ tim/hồi sinh. Đây là giá trị đóng gói.

### S03

Hình ảnh gốc — analysis/visuals/asset-contact-sheet.png; analysis/unity-index.json
Ảnh minh họa được trích trực tiếp từ sprite của APK. Không phải ảnh chụp game đang chạy.

### S04

Lời hướng dẫn / UI — analysis/unity/3175_IngameUI.txt
Bảng CSV ngôn ngữ: mô tả booster, mục tiêu, cảnh báo khay, hồi sinh, tim, hướng dẫn và tên cài đặt.

### S05

Đồ vật và hộp — analysis/mono/resources.assets_7861.json; analysis/unity/3208_level_1.txt
ItemCatalog và ví dụ JSON màn. Catalog có bản ghi removed; số lượng catalog không bằng số nội dung đang được dùng.

### S06

IAP / thưởng — analysis/unity/3186_IAPProductCatalog.txt; analysis/mono/sharedassets0.assets_104.json; analysis/mono/resources.assets_10888.json
Catalog giá mặc định, reward mapping từng SKU và preset thưởng của WinPopup. Chưa kiểm tra giá live hoặc giao dịch.

### S07

Scene / prefab / hệ thống — analysis/mono-index.json; analysis/game-object-index.json; analysis/mono/
Đã đọc 3.990 MonoBehaviour; 5 đối tượng không đọc được đầy đủ. Bản ghi chính: level1_531 Queue, 566 BoxController, 568 Tutorial, 575 Storage, 580 Camera; resources.assets_10788 BoosterDatabase, 10791 MechanicDatabase; các popup riêng.

### S08

Metadata và hằng số — analysis/metadata-game-classes.txt; analysis/constants.py; analysis/global-metadata.dat
Tên lớp/hàm/trạng thái và giá trị field mặc định của IL2CPP metadata v31, giải mã số nguyên nén. Chưa decompile thân hàm native, chưa gọi thực tế các hàm lấy giá/thưởng.

### S09

Remote Config mặc định — analysis/mono/resources.assets_7836.json
Chỉ là default trong APK. Không truy vấn backend và chưa xác nhận cấu hình người chơi nhận khi online.

### S10

Âm thanh / hoạt ảnh — analysis/mono/resources.assets_7829.json; analysis/unity-index.json
AudioDefaultSO, 17 AudioClip và 23 AnimationClip đã liệt kê. Sự tồn tại/mapping không chứng minh mọi clip đều phát trong phiên chơi.
