from pathlib import Path
import re

OUT = Path(r'D:/APK Works/HappyTidyRoom/outputs/happy-tidy-room-gdd/markdown')
main = OUT / 'GDD.md'
text = main.read_text(encoding='utf-8')
if '## 1. Overview' not in text:
    raise SystemExit('Already split: edit topic files directly; do not regenerate from the old builder.')

text = text.replace('Các trường hợp nhiều hộp cùng nhận một nhóm, xử lý nhiều item đang bay và hồi phục màn đang chơi được ghi cụ thể trong [quyết định cần chốt](DESIGN_DECISIONS.md). Không tự dùng luật của RoomSort để lấp các điểm này.', 'Các trường hợp nhiều hộp cùng nhận một nhóm, xử lý nhiều item đang bay và hồi phục màn đang chơi được ghi cụ thể trong [quyết định cần chốt](DESIGN_DECISIONS.md). Level theo RoomSort không tự quyết định mọi luật hoặc nhịp chuyển động của bản kết hợp.')
text = text.replace('| Mỹ thuật | Hoạt hình 2D, màu dịu mắt. Đồ vật có hình dáng và đường viền rõ để dễ nhận diện. |', '| Mỹ thuật | Dùng bộ art Tidy Room tại `D:\\APK Works\\Tidy Room`. Chi tiết phong cách và số lượng asset sẽ cập nhật sau khi trích xuất, xem hình. |')
text = text.replace('Trải nghiệm tập trung vào ba điểm:', '**Hướng kết hợp đã chốt:** Level design theo RoomSort, art từ Tidy Room, cảm giác thao tác và phản hồi theo Happy Tidy Room. Các mô tả booster và economy hiện tại giữ làm bản thảo tham chiếu, chưa tự chuyển thành cấu hình cuối chỉ từ việc chọn feeling.\n\nTrải nghiệm tập trung vào ba điểm:')
text = text.replace('Thư viện gồm **355 tên nhóm hộp nhận**', '**Danh mục dưới đây là thư viện Happy dùng đối chiếu**, chưa phải số liệu của bộ art Tidy Room được chọn cho game mới.\n\nThư viện tham chiếu gồm **355 tên nhóm hộp nhận**')
text = text.replace('Xem toàn bộ tên nhóm, bối cảnh, số asset, mã category và ảnh đại diện trong [CATEGORY_OBJECT.md](CATEGORY_OBJECT.md).', 'Xem toàn bộ tên nhóm, bối cảnh, số asset, mã category và ảnh đại diện của Happy trong [CATEGORY_OBJECT.md](CATEGORY_OBJECT.md).\n\nDanh mục chính thức phải kiểm đếm lại từ Tidy Room, chia theo bối cảnh → nhóm hộp nhận → từng mẫu đồ. Sau đó ánh xạ nhóm đồ RoomSort sang nhóm tương ứng của Tidy Room; nhóm thiếu asset phải được nêu rõ, không tự đổi ý nghĩa hộp.')
text = text.replace('Dùng Happy Tidy Room làm tham chiếu hình ảnh: đồ họa 2D giả lập chiều sâu, màu dịu, viền rõ. Các mẫu trong cùng nhóm cần dễ nhận là cùng loại dù khác màu hoặc kiểu dáng. Nhãn và icon của hộp phải giúp người chơi hiểu nhóm nhận ngay khi quan sát.', '''**Nguồn art chính: Tidy Room**, tại `D:\\APK Works\\Tidy Room\\Tidy-Room_57_apkcube.apks`.

Tidy Room quyết định hình ảnh đồ vật và bối cảnh. Phạm vi dùng lại UI, icon booster và hiệu ứng hình ảnh cần đối chiếu sau khi xem tài nguyên; không mặc định toàn bộ UI cũng lấy từ Tidy Room.

Happy Tidy Room là tham chiếu về cảm giác thao tác và phản hồi: chọn đồ, nhịp nảy / bay, nhận đồ, đóng hộp, chuyển hộp và phản hồi booster. Dùng feeling Happy không có nghĩa dùng lại art Happy.

Các mẫu trong cùng nhóm phải dễ nhận là cùng loại dù khác màu hoặc kiểu dáng. Nhãn và icon hộp cần giúp người chơi hiểu nhóm nhận. Chưa mô tả màu, nét hoặc hình khối cụ thể của Tidy Room khi chưa xem hình trích xuất.''')
text = text.replace('![Tham chiếu đồ vật và bối cảnh](references/uiux-20.png)', '![Art Happy chỉ dùng đối chiếu, không phải art đích](references/uiux-20.png)')
text = text.replace('Ảnh Object, Booster và Tutorial trong tài liệu là tài nguyên và hình ghép minh họa. Chúng xác định hình dáng, màu sắc và ý nghĩa đối tượng; không thể hiện đầy đủ chuyển động của một lượt chơi.', 'Ảnh Object, Booster và Tutorial hiện có đều từ Happy, được giữ để giải thích vai trò và trình tự. Chúng chưa phải hình đại diện của bộ art Tidy Room. Ảnh tĩnh không xác nhận đường bay hoặc nhịp chuyển động.')
text = text.replace('### Sự kiện hình ảnh', '''### Mục tiêu feeling

Giữ Happy làm mốc cho cảm giác chạm chọn, chuyển item tới đích, nhận đủ đồ và đổi hộp. Các mốc thời gian trong bảng dưới là dữ liệu tham chiếu Happy hiện có. Cần đối chiếu chuỗi chuyển động trước khi gọi là khớp feeling; chưa tự xem các timing này là thông số cuối đã duyệt.

### Sự kiện hình ảnh''')
text = text.replace('Bản này phục vụ đọc và hoàn thiện thiết kế. Chưa phải tài liệu đã duyệt để triển khai toàn bộ game. Level Progress chưa được viết, bộ level kết hợp chưa được tạo và các mẫu dữ liệu chưa được chuyển art.', 'Hướng game đã chốt: **level RoomSort + art Tidy Room + feeling Happy**. Tài liệu đang hoàn thiện chi tiết, chưa phải bản đã duyệt để triển khai toàn bộ game. Level Progress chưa viết; bộ level kết hợp và mapping art Tidy Room chưa được tạo.')
text = text.replace('Điểm cần chốt đầu tiên là tài liệu sẽ mô tả Happy Tidy Room hiện tại hay phiên bản kết hợp level RoomSort với art Happy. Các lựa chọn phụ thuộc được ghi trong [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md).', 'Hướng kết hợp không cần hỏi lại. Các điểm còn mở là luật thua áp dụng cho bộ level, quy tắc booster và các chuỗi chuyển động chưa đối chiếu; xem [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md).')
text = text.replace('Chốt hướng game, cấu trúc dữ liệu; có đủ ảnh tham chiếu.', 'Chốt cấu trúc dữ liệu; trích xuất và ánh xạ art Tidy Room.')
text = text.replace('ánh xạ nhóm nhận và mẫu đồ giữa hai thư viện; đổi nền;', 'ánh xạ nhóm nhận và mẫu đồ từ RoomSort sang thư viện Tidy Room; đổi nền;')

sections = {}
for match in re.finditer(r'^## (\d+)\. ([^\n]+)\n(.*?)(?=^## \d+\. |\Z)', text, re.M | re.S):
    sections[int(match[1])] = (match[2], match[3].strip())
assert len(sections) == 15
art, vfx = sections[8][1].split('### Mục tiêu feeling', 1)
sound, haptic = sections[9][1].split('### Haptic', 1)
topics = [
 ('01_OVERVIEW.md', 'Overview', sections[1][1]),
 ('02_GAMEPLAY.md', 'Gameplay', sections[2][1]),
 ('03_OBJECT.md', 'Object', 'Ảnh bên dưới là tham chiếu Happy để giải thích đối tượng; hình chính thức sẽ lấy từ Tidy Room.\n\n' + sections[3][1]),
 ('04_ELEMENT.md', 'Element', sections[4][1]),
 ('05_BOOSTER.md', 'Booster', 'Ảnh và bộ trợ giúp dưới đây giữ từ bản thảo Happy. Hướng feeling Happy chưa tự chốt giá, luật booster hoặc yêu cầu dùng lại hình icon.\n\n' + sections[5][1]),
 ('06_LEVEL_PROGRESS.md', 'Level Progress', sections[6][1] + '\n\nLevel design dùng RoomSort làm chuẩn về bố trí, layer và thứ tự hộp. Chưa chọn số lượng level cần làm; không mặc định lấy đủ toàn bộ level gốc.'),
 ('07_CATEGORY_OBJECT.md', 'Category Object', sections[7][1]),
 ('08_ART_DIRECTION.md', 'Art direction', art),
 ('09_ANIMATION_VFX.md', 'Animation, VFX và Feeling', '## Mục tiêu feeling' + vfx),
 ('10_SFX.md', 'SFX', sound),
 ('11_HAPTIC.md', 'Haptic', haptic),
 ('12_ECONOMY.md', 'Economy', sections[10][1]),
 ('13_TUTORIAL.md', 'Tutorial', sections[11][1]),
 ('14_UI_UX.md', 'UI/UX', sections[12][1]),
 ('15_LEVEL_DATA.md', 'Dữ liệu level', sections[13][1]),
 ('16_ACCEPTANCE.md', 'Tình huống kiểm tra thiết kế', sections[14][1]),
 ('17_HANDOFF.md', 'Bàn giao và điểm chưa chốt', sections[15][1]),
]
mapping = {1:'01_OVERVIEW.md',2:'02_GAMEPLAY.md',3:'03_OBJECT.md',4:'04_ELEMENT.md',5:'05_BOOSTER.md',6:'06_LEVEL_PROGRESS.md',7:'07_CATEGORY_OBJECT.md',8:'09_ANIMATION_VFX.md',9:'10_SFX.md',10:'12_ECONOMY.md',11:'13_TUTORIAL.md',12:'14_UI_UX.md',13:'15_LEVEL_DATA.md',14:'16_ACCEPTANCE.md',15:'17_HANDOFF.md'}
def fix_refs(t):
    def repl(m):
        n = int(m[1])
        return f'[{mapping[n]}]({mapping[n]})' if n in mapping else m[0]
    return re.sub(r'(?i)mục (\d+)\b', repl, t)
for filename, title, body in topics:
    body = fix_refs(body)
    (OUT / filename).write_text(f'# {title}\n\n[← Mục lục GDD](GDD.md)\n\n{body.strip()}\n', encoding='utf-8')

dec = (OUT / 'DESIGN_DECISIONS.md').read_text(encoding='utf-8')
dec = dec.replace('Phiên bản tài liệu: 0.1', 'Phiên bản tài liệu: 0.2')
dec = dec.replace('| D-011 | answered | Phiên hiện tại chỉ viết bộ GDD Markdown bằng skill, không triển khai game. | Toàn bộ |', '''| D-011 | answered | Phiên hiện tại chỉ viết bộ GDD Markdown bằng skill, không triển khai game. | Toàn bộ |
| D-012 | answered | Người dùng chốt: level RoomSort + art D:/APK Works/Tidy Room + feeling Happy. Thay hướng art Happy trước đây bằng art Tidy Room; Happy là mốc feeling. | Overview, Art, Animation, Level Data |
| D-013 | answered | GDD tách thành nhiều file nhỏ trong cùng folder; GDD.md là mục lục, mỗi chủ đề có file chuẩn riêng. | Toàn bộ |''')
old = next(line for line in dec.splitlines() if line.startswith('| Q-001 |'))
dec = dec.replace(old, '| Q-001 | Đã trả lời: bản kết hợp nào? | **answered:** level RoomSort + art Tidy Room tại D:/APK Works/Tidy Room + feeling Happy. Không hỏi lại hướng này. | D-012 |')
old = next(line for line in dec.splitlines() if line.startswith('| Q-008 |'))
dec = dec.replace(old, '| Q-008 | Những chi tiết chuyển động nào cần đối chiếu Happy? | Đã chốt Happy là mốc feeling. Còn thiếu quan sát đường bay, nhịp nhận / đổi hộp, Broom / Vacuum và Lose / Revive; cần bổ sung bằng chứng chuyển động hoặc mô tả cụ thể. Không hỏi lại game tham chiếu. | V_01–V_14 |')
dec = dec.replace('## Vị trí tiếp tục', '''## Trạng thái art và danh mục

Đã kiểm tra D:/APK Works/Tidy Room có Tidy-Room_57_apkcube.apks, chứa base.apk, split_UnityDataAssetPack.apk và split_config.arm64_v8a.apk. Chưa trích ảnh / catalog hoặc xem art từ gói này. Category 355 nhóm và ảnh trong tài liệu vẫn là tham chiếu Happy, không phải số lượng hoặc hình ảnh của Tidy Room.

## Vị trí tiếp tục''')
dec = dec.replace('Đã hoàn thành bản thảo các mục có căn cứ và đóng gói phụ lục / ảnh. Đang chờ Q-001. Sau câu trả lời, sửa đồng bộ GDD, nguồn và quyết định; chỉ hỏi tiếp 1–3 lựa chọn có ảnh hưởng tới phần đang viết.', 'Đã ghi nhận Q-001 và tách bộ GDD thành các file chủ đề. Tiếp theo cần kiểm kê art Tidy Room, ánh xạ nhóm nhận với RoomSort và đối chiếu feeling Happy. Luật Lose / booster không tự được chọn chỉ từ hướng tham chiếu; chỉ hỏi tiếp 1–3 lựa chọn có ảnh hưởng tới phần đang viết.')
dec = dec.replace('## Câu hỏi đang mở', '## Quyết định đã trả lời và câu hỏi còn mở')
(OUT / 'DESIGN_DECISIONS.md').write_text(fix_refs(dec), encoding='utf-8')

src = (OUT / 'SOURCE_MAP.md').read_text(encoding='utf-8')
src = src.replace('Các đề xuất của trợ lý về hybrid, luật thua, schema hoặc booster RoomSort chưa được coi là câu trả lời của người dùng.', 'Hướng kết hợp đã được người dùng chốt ở D-012: level RoomSort + art Tidy Room + feeling Happy. Các đề xuất về luật thua, schema hoặc booster vẫn chưa được tự coi là đã duyệt.')
src = src.replace('| SRC-09 |', '| SRC-10 | D:/APK Works/Tidy Room/Tidy-Room_57_apkcube.apks | Đã kiểm tra thư mục và danh sách gói: base.apk, split_UnityDataAssetPack.apk, split_config.arm64_v8a.apk. Chưa trích xuất hoặc xem hình Tidy Room; chưa xác định số category / asset. Nguồn art được người dùng chọn ở D-012. |\n| SRC-09 |')
src = src.replace('| SRC-01: cần bộ level giống RoomSort | Ý định tham chiếu level, câu hỏi khả năng dùng art / cấu trúc Happy | Q-001, Q-011, Q-012 | unresolved ở mức sản phẩm cuối; không coi câu hỏi là duyệt mọi luật RoomSort |', '| SRC-01: câu trả lời Q-001 | Level RoomSort + art Tidy Room + feeling Happy | D-012; Overview, Art, Animation, Level Data | incorporated; không tự duyệt mọi luật RoomSort |\n| SRC-01: yêu cầu tách file | Nhiều tài liệu nhỏ cùng folder, GDD.md là mục lục | D-013; toàn bộ gói | incorporated |')
src = src.replace('| Art | references/uiux-20.png | Phong cách, màu, nét và mẫu tài nguyên | Contact sheet, không phải mockup bố cục HUD |', '| Art Happy đối chiếu | references/uiux-20.png | Tham chiếu cũ, không còn là art đích | Contact sheet; art đích là Tidy Room, chưa xem hình |')
src = src.replace('Đã kiểm tra đủ 13 nhóm nội dung mẫu (gộp Haptic với SFX và mở rộng phần data / tình huống);', 'Đã tách đủ 17 tài liệu chủ đề, giữ đủ nhóm nội dung mẫu; Haptic, SFX, Art và Animation có file riêng;')
for n in sorted(mapping, reverse=True):
    src = re.sub(r'GDD §'+str(n)+r'\b', f'[{mapping[n]}]({mapping[n]})', src)
(OUT / 'SOURCE_MAP.md').write_text(src, encoding='utf-8')
cat = OUT / 'CATEGORY_OBJECT.md'
c = cat.read_text(encoding='utf-8').replace('# Category Object', '# Phụ lục Category Object — tham chiếu Happy', 1)
c = c.replace('[Trở về GDD](GDD.md)', '[Mục lục GDD](GDD.md) · [Thiết kế Category Object](07_CATEGORY_OBJECT.md)\n\nĐây là thống kê Happy Tidy Room, chưa phải danh mục art Tidy Room đã chọn cho game mới.')
cat.write_text(c, encoding='utf-8')

index = '''---
title: "Tidy Room Sort — GDD"
status: drafting
updated: 2026-11-20
revision: 0.2
scope: "Level RoomSort + art Tidy Room + feeling Happy; chưa viết Level Progress."
---

# Tidy Room Sort — GDD

Game giải đố tìm đồ và phân loại vào hộp. Đồ xếp theo layer; người chơi chọn thứ tự lấy đồ và giữ đủ slot chờ để dọn sạch màn.

**Hướng đã chốt:** Level design theo **RoomSort**, art từ **D:\\APK Works\\Tidy Room**, cảm giác thao tác và phản hồi theo **Happy Tidy Room**.

## Tài liệu thiết kế

Mỗi chủ đề có một file chuẩn. Đọc Overview và Gameplay trước, sau đó mở phần cần làm; không cần đọc toàn bộ folder để tìm một luật.

| File | Nội dung |
|---|---|
'''
descriptions = [
'Ý tưởng, đối tượng chơi, nền tảng và hướng kết hợp.',
'Core loop, layer, thu gom, Win / Lose / Revive.',
'Đồ vật, hộp, slot chờ, kho và bối cảnh.',
'Cơ chế đặc biệt; chưa bổ sung Element mới.',
'Vacuum, Broom, Extra Box, Extra Slot và Hint.',
'Giữ chỗ theo yêu cầu chưa biên soạn.',
'Cách chia nhóm và yêu cầu kiểm kê art Tidy Room.',
'Art Tidy Room; phân biệt với hình Happy đang dùng đối chiếu.',
'Feeling Happy, sự kiện chuyển động và VFX.',
'Trigger và âm thanh tham chiếu.',
'Rung và cài đặt bật / tắt.',
'Coin, tim, thưởng, quảng cáo và IAP.',
'Các bước hướng dẫn ngắn, có ảnh minh họa.',
'Luồng màn hình, HUD và popup.',
'Schema hai game, mapping và yêu cầu chuyển art.',
'Các tình huống kiểm tra luật và tương tác.',
'Thứ tự bàn giao và phần còn cần chốt.'
]
for (filename, title, _), desc in zip(topics, descriptions):
    index += f'| [{title}]({filename}) | {desc} |\n'
index += '''
## Hồ sơ đi kèm

- [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md): quyết định đã chốt và các điểm còn mở.
- [SOURCE_MAP.md](SOURCE_MAP.md): nguồn, độ phủ đối chiếu và giới hạn bằng chứng.
- [CATEGORY_OBJECT.md](CATEGORY_OBJECT.md): 355 nhóm và ảnh **tham chiếu Happy**, chưa phải thống kê Tidy Room.
- `references/`: hình minh họa và hai mẫu level gốc, chưa phải bộ asset / level cuối của bản kết hợp.

**Trạng thái:** Đã chốt hướng kết hợp và tổ chức tài liệu. Art Tidy Room chưa được trích xuất / kiểm kê; chuyển động Happy chưa được đối chiếu đầy đủ. Luật thua, một số quy tắc booster và economy còn mở. Không dùng bản này như tài liệu đã duyệt toàn bộ để triển khai.
'''
main.write_text(index, encoding='utf-8')
print(f'Split into {len(topics)} topic files; updated index, decisions, source map and category labels.')
