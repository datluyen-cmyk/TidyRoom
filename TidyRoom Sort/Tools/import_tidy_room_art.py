"""Apply the local Tidy Room APKS art to existing RoomSort runtime levels.

Requires Pillow and UnityPy. The Happy reference levels and Happy schema exports
are kept intact. Source layers, positions, orders and overlap data are preserved.
"""
import argparse
import gzip
import io
import json
from pathlib import Path
import re
import sys
import zipfile

from PIL import Image


PROJECT = Path(__file__).resolve().parents[1]
UI = {
    'GP_Box0': 'Basket', 'GP_Box_Unlock': 'BasketLid', 'GP_Slot': 'TraySlot',
    'NewBooster_Icon_Vaccum': 'BoosterWand256',
    'NewBooster_Icon_Clear': 'BoosterBrush256', 'Hint': 'HintsIcon',
}


def read(path):
    return json.loads(path.read_bytes().decode('utf-8-sig'))


def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_bytes(data)
    temporary.replace(path)


def data(value, indent=None):
    return json.dumps(value, ensure_ascii=False, indent=indent,
                      separators=(',', ':') if indent is None else None).encode('utf-8')


def save(image, path):
    output = io.BytesIO()
    if path.suffix == '.jpg':
        image.convert('RGB').save(output, format='JPEG', quality=95, subsampling=0)
    else:
        image.convert('RGBA').save(output, format='PNG', compress_level=3)
    atomic(path, output.getvalue())


def unpack_bundle(apks, out, package, filename):
    path = out / filename
    if not path.exists():
        with zipfile.ZipFile(apks) as outer, zipfile.ZipFile(io.BytesIO(outer.read(package))) as inner:
            atomic(path, inner.read(f'assets/bin/Data/{filename}'))
    return path


def shape(path, w, h):
    with Image.open(path) as im:
        alpha = im.convert('RGBA').getchannel('A')
        # Fit the complete sprite proportionally into the source footprint.
        factor = min(w / im.width, h / im.height)
        alpha.thumbnail((40, 40))
        return dict(width=im.width * factor, height=im.height * factor,
                    maskW=alpha.width, maskH=alpha.height,
                    alpha=[int(v > 32) for v in alpha.getdata()])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apks', type=Path, default=Path('D:/APK Works/Tidy Room/Tidy-Room_57_apkcube.apks'))
    parser.add_argument('--vendor', type=Path, default=Path('D:/APK Works/HappyTidyRoom/analysis/vendor'))
    parser.add_argument('--room-root', type=Path, default=Path('D:/APK Works/RoomSort'))
    args = parser.parse_args()
    sys.path.insert(0, str(args.vendor))
    import UnityPy

    root = PROJECT/'Assets/StreamingAssets/TidyRoom'
    scratch = args.apks.parent/'analysis'/('art-' + args.apks.stem)
    env = UnityPy.load(str(unpack_bundle(args.apks, scratch, 'base.apk', 'data.unity3d')),
                       str(unpack_bundle(args.apks, scratch, 'split_UnityDataAssetPack.apk', 'datapack.unity3d')))
    names = None
    sprites = {}
    for obj in env.objects:
        if obj.type.name == 'Sprite':
            sprite = obj.read()
            sprites.setdefault(sprite.m_Name, sprite)
        elif obj.type.name == 'TextAsset':
            asset = obj.read()
            if asset.m_Name == 'RoomBackgroundLegacyNames':
                names = json.loads(asset.m_Script)
    if not names:
        raise ValueError('Missing background name mapping in Tidy Room package')
    item_names = {n for n in sprites if re.fullmatch(r'\d+-\d+', n)}
    ui_paths = {key: f'Art/TidyRoomUI/{key}.png' for key in UI}
    for key, name in UI.items():
        save(sprites[name].image, root/ui_paths[key])
    print(f'Tidy Room package: {len(item_names)} numeric sprites, {len(names)} named backgrounds', flush=True)

    index = read(root/'index.json')
    source = read(PROJECT/'Tools/Source/room.json')
    used = {}; backgrounds = {}; background_sizes = {}; missing_bg = set(); missing_items = set()
    packed_levels = {}; stats = {}; shape_cache = {}
    for entry in index['levels']:
        if entry['source'] != 'RoomSort':
            continue
        path = root/entry['file']
        raw = path.read_bytes()
        level = json.loads(gzip.decompress(raw) if path.suffix == '.gz' else raw)
        original_bg = level.get('sourceBg', level['bg'])
        bg_id = Path(original_bg).stem
        missing_on_level = set()
        for item in level['content']:
            name = item['sourceId']
            if name not in used:
                if name in item_names:
                    rel = f'Art/TidyRoom/{name}.png'
                    save(sprites[name].image, root/rel)
                else:
                    # This package omits some older categories and custom tutorial art.
                    # Retain the matching original RoomSort image instead of substituting a different object.
                    rel = f'Art/Room/{name}.png'
                    with Image.open(args.room_root/'analysis/www/assets'/source['itemFiles'][name]) as image:
                        save(image, root/rel)
                used[name] = rel
            if name not in item_names:
                missing_on_level.add(name)
            size = item['sourceWidth'], item['sourceHeight']
            cache_key = name, size
            if cache_key not in shape_cache:
                shape_cache[cache_key] = shape(root/used[name], *size)
            item.update(id=name, art=used[name], **shape_cache[cache_key])
        missing_items.update(missing_on_level)
        target = names.get(bg_id)
        if target:
            if bg_id not in backgrounds:
                dest = f'Art/TidyRoomBG/{target}.jpg'
                image = sprites[target].image
                # The same room exists at different resolutions in the two releases.
                # Keep the source coordinate scale so objects still sit on the furniture.
                with Image.open(root/original_bg) as old:
                    logical_width, logical_height = old.size
                fit = min(logical_width/image.width, logical_height/image.height)
                background_sizes[bg_id] = [image.width*fit, image.height*fit]
                save(image, root/dest)
                backgrounds[bg_id] = dest
            level.update(bg=backgrounds[bg_id], sourceBg=original_bg, bgSize=background_sizes[bg_id])
        else:
            missing_bg.add(original_bg)
        level['artTheme'] = 'TidyRoom'
        packed_levels[path] = gzip.compress(data(level), compresslevel=6, mtime=0) if path.suffix == '.gz' else data(level)
        stats[level['key']] = dict(items=len(level['content']), sourceBackground=bool(target), fallbackItems=sorted(missing_on_level))
        if len(packed_levels) % 25 == 0:
            print(f'Prepared {len(packed_levels)} RoomSort levels, {len(used)} unique item images', flush=True)

    for path, content in packed_levels.items():
        atomic(path, content)
    report = dict(package=str(args.apks), roomSortLevels=len(stats), happyReferenceLevels=len(index['levels'])-len(stats),
                  tidyRoomItems=len(used)-len(missing_items), originalRoomSortItems=sorted(missing_items),
                  tidyRoomBackgrounds=len(backgrounds), originalRoomSortBackgrounds=sorted(missing_bg),
                  ui=UI, levels=stats)
    atomic(PROJECT/'Converted/tidy-room-art-report.json', data(report, indent=2))
    print(f'Applied to {len(stats)} levels: {report["tidyRoomItems"]} Tidy Room items, {len(backgrounds)} backgrounds; '
          f'{len(missing_items)} items and {len(missing_bg)} backgrounds kept from original RoomSort.', flush=True)


if __name__ == '__main__':
    main()
