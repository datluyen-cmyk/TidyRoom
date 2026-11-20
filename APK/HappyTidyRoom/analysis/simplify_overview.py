import json
from pathlib import Path
p=Path(r'D:\APK Works\HappyTidyRoom\analysis\gdd-content.json')
d=json.loads(p.read_text(encoding='utf8'))
text={
'Overview':'Happy Tidy Room là game giải đố dọn phòng. Người chơi tìm đồ trong căn phòng bừa bộn và thu gom vào các hộp theo đúng nhóm để hoàn thành màn chơi.',
'Core mechanic':'Chạm item để dọn vào hộp chứa đúng nhóm; item chưa có hộp nhận sẽ vào slot chờ. Đồ vật xếp theo layer; đồ bị đè chưa lấy được, cần dọn đồ phía trên trước.',
'Ending Rewards':'Hoàn thành màn để nhận coin, kèm lựa chọn xem quảng cáo để nhận thêm thưởng.',
'Màn hình':'Màn hình dọc, chơi trên điện thoại.',
'Camera':'Góc nhìn isometric giả lập bằng đồ họa 2D, nhìn chéo từ trên xuống để bao quát căn phòng. Có thể kéo và thu phóng để tìm đồ.',
'Genre / Sub-genre':'Casual puzzle, kết hợp tìm đồ, phân loại và quản lý chỗ trống trong khay chờ.',
'Target Audience':'Người chơi yêu thích tìm đồ, sắp xếp và giải đố nhẹ nhàng với thao tác đơn giản.',
'Art style':'Đồ họa 2D phong cách hoạt hình, màu sắc dịu mắt. Căn phòng có chiều sâu giả lập; đồ vật có hình dáng và đường viền rõ để dễ nhận diện.',
'Control':'Chạm để chọn đồ, kéo để di chuyển góc nhìn và dùng hai ngón tay để thu phóng.',
'Monetize':'Quảng cáo nhận thưởng, quảng cáo xen kẽ và banner. Mua trong ứng dụng gồm gói bỏ quảng cáo và các gói coin.',
'IGC':'Coin dùng cho các tính năng hỗ trợ. Tim giới hạn lượt chơi sau thất bại; booster giúp xử lý các tình huống khó.',
'USP':'Kết hợp cảm giác dọn gọn căn phòng với bài toán chọn thứ tự thu gom: tìm đúng đồ, đưa vào đúng hộp và tránh làm đầy khay chờ.'
}
for s in d['sheets']:
 if s['name']=='Overview':
  for row in s['rows']:
   if row[0] in text: row[1]=text[row[0]]
gameplay={
'Mục tiêu':'Thu gom đủ đồ cho tất cả các hộp để hoàn thành màn. Mỗi hộp ghi nhóm đồ cần nhận và số lượng yêu cầu.',
'Vòng lặp chính':'Quan sát hộp đang mở → tìm và chọn đồ phù hợp → thu gom đủ số lượng → hoàn thành hộp → đón hộp mới. Tiếp tục cho đến khi hoàn tất tất cả các hộp.',
'Đồ phù hợp với hộp':'Đồ đúng nhóm được đưa vào hộp tương ứng nếu hộp còn chỗ. Các món có thể khác màu hoặc kiểu dáng nhưng vẫn được nhận nếu thuộc cùng nhóm. Bộ đếm trên hộp cho biết số đồ còn cần thu gom.',
'Đồ chưa có hộp nhận':'Đồ chưa có hộp phù hợp sẽ chiếm một ô khay chờ. Lấy đồ trước giúp mở đường tới những món bị che, nhưng làm giảm chỗ trống cho các lượt sau.',
'Giải phóng khay':'Khi có hộp nhận nhóm đồ đang nằm trong khay chờ, các món phù hợp được chuyển vào hộp để giải phóng chỗ trống.',
'Đồ bị che':'Các món đồ xếp chồng và che khuất nhau. Người chơi cần lấy những món phía trên để tiếp cận đồ nằm bên dưới, đồng thời cân nhắc chỗ trống trong khay.',
'Win':'Nhận đủ đồ cho tất cả các hộp để chiến thắng. Game hiển thị hiệu ứng hoàn thành, phần thưởng và lựa chọn sang màn tiếp theo.',
'Lose':'Người chơi thất bại khi khay chờ đầy và không còn chỗ nhận thêm đồ. Màn hình thất bại cho phép chọn hồi sinh, chơi lại hoặc thoát.',
'Revive':'Sau khi thất bại, người chơi có thể dùng coin hoặc xem quảng cáo để dọn khay chờ và tiếp tục màn đang chơi.',
'Replay / Quit':'Người chơi có thể chơi lại từ đầu hoặc thoát màn. Khi bỏ lượt, game hiển thị xác nhận và nhắc về việc mất tim.',
'Giới hạn thời gian / lượt':'Áp lực chính đến từ số ô khay chờ và thứ tự thu gom. Người chơi cần quan sát các hộp đang mở để chọn món phù hợp trước khi hết chỗ.',
'Nhịp quyết định':'Ưu tiên hoàn thành hộp để mở yêu cầu mới và giải phóng khay. Mỗi lần lấy món chưa có hộp nhận là một lựa chọn giữa mở đường tìm đồ và nguy cơ làm đầy khay.'
}
for s in d['sheets']:
 if s['name']=='Gameplay':
  for row in s['rows']:
   if row[0] in gameplay: row[1]=gameplay[row[0]]
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
