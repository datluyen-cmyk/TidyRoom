using System;
using System.Collections.Generic;
using UnityEngine;

public sealed class TidyPreviewView : MonoBehaviour
{
    static readonly Color Ink = new Color32(38, 46, 54, 255), Soft = new Color32(86, 98, 107, 255), Paper = new Color32(250, 247, 239, 255), Mint = new Color32(217, 239, 224, 255), Line = new Color32(229, 224, 212, 255), Rose = new Color32(250, 218, 208, 255);
    readonly Dictionary<string, Texture2D> art = new Dictionary<string, Texture2D>();
    TidyPack pack;
    TidyLevel level;
    TidyPreviewGame game;
    int index;
    string message;
    bool showGuide;
    int step, flying = -1, bumped = -1;
    float flightStart, bumpStart;
    TidyPreviewGame.Pick flight;
    GUIStyle text, small, center, title, pill;

    void Awake() { pack = TidyPreviewGame.LoadPack(); Load(0); }

    void Load(int i)
    {
        index = i;
        level = pack.levels[i];
        game = new TidyPreviewGame(pack, level);
        flying = bumped = -1;
        step = 0;
        showGuide = false;
        message = "Bấm vào món đồ muốn dọn. Lấy đồ phía trên trước.";
    }

    void Styles()
    {
        if (text != null) return;
        text = new GUIStyle(GUI.skin.label) { fontSize = 17, alignment = TextAnchor.MiddleLeft, clipping = TextClipping.Clip };
        text.normal.textColor = Ink;
        small = new GUIStyle(text) { fontSize = 14 };
        small.normal.textColor = Soft;
        center = new GUIStyle(text) { alignment = TextAnchor.MiddleCenter };
        title = new GUIStyle(text) { fontSize = 23, fontStyle = FontStyle.Bold };
        pill = new GUIStyle(center) { fontSize = 16, fontStyle = FontStyle.Bold };
    }

    void OnGUI()
    {
        if (game == null) return;
        Styles();
        var prior = GUI.matrix;
        float zoom = Mathf.Min(Screen.width / 650f, Screen.height / 730f, 1.9f);
        GUI.matrix = Matrix4x4.Scale(new Vector3(zoom, zoom, 1));
        try { Draw(Screen.width / zoom, Screen.height / zoom); }
        finally { GUI.matrix = prior; }
    }

    void Draw(float w, float h)
    {
        Fill(new Rect(0,0,w,h), Paper);
        bool side = w / h >= 1.20f;
        float boardWidth = side ? w - 328 : w - 28;
        var boardArea = new Rect(14, side ? 65 : 218, boardWidth, h - (side ? 105 : 258));
        Rect board = Fit(boardArea, level.w, level.h);
        float hudX = side ? w - 305 : 15, hudY = side ? 94 : 83, hudWidth = side ? 289 : w - 30;
        bool modal = game.State != TidyPreviewGame.Status.Playing && flying < 0;

        GUI.Label(new Rect(16,4,220,53), "Tidy Room · Unity test", title);
        if (Button(new Rect(w-377,13,86,32), "Màn trước", index > 0)) { Load(index-1); return; }
        if (Button(new Rect(w-284,13,76,32), "Chơi lại")) { Load(index); return; }
        if (Button(new Rect(w-201,13,82,32), "Màn sau", index + 1 < pack.levels.Length)) { Load(index+1); return; }
        if (Button(new Rect(w-112,13,96,32), showGuide ? "Ẩn lời giải" : "Xem lời giải"))
        {
            if (showGuide) showGuide = false;
            else { Load(index); showGuide = true; message = "Lời giải mẫu: bấm vào điểm đánh dấu hoặc nút Bước tiếp."; }
        }

        Fill(new Rect(14,52,w-28,1), Line);
        GUI.Label(new Rect(side ? hudX : 16,55,side ? 295 : w-132,28), $"{level.label}  ·  Còn {game.Remaining}/{level.items.Length} món", text);
        Fill(new Rect(board.x-2,board.y-2,board.width+4,board.height+4), Line);
        GUI.DrawTexture(board, Texture(level.room));
        float scale = board.width / level.w, now = Time.unscaledTime;
        GUI.BeginGroup(board);
        try
        {
            var local = new Rect(0,0,board.width,board.height);
            for (int i=0; i<level.items.Length; i++)
            {
                if (!game.present[i]) continue;
                var item = level.items[i];
                Vector2 p = CanvasPoint(local, scale, item.x, item.y);
                if (i == bumped && now-bumpStart < .22f) p.x += Mathf.Sin((now-bumpStart)*75f)*3.5f;
                DrawItem(item, p, scale);
            }
            if (showGuide && step < level.proof.Length)
            {
                var p = CanvasPoint(local, scale, level.proof[step].x, level.proof[step].y);
                Fill(new Rect(p.x-10,p.y-10,20,20), Color.white);
                Fill(new Rect(p.x-8,p.y-8,16,16), Mint);
                GUI.Label(new Rect(p.x-10,p.y-11,20,20), "·", pill);
            }
        }
        finally { GUI.EndGroup(); }

        var boxRects = new Rect[2];
        float boxWidth = (hudWidth-8)*.5f;
        for (int i=0; i<2; i++)
        {
            var box = game.boxes[i];
            var rect = boxRects[i] = new Rect(hudX+i*(boxWidth+8),hudY,boxWidth,64);
            Fill(rect, box.order != null ? Mint : Line);
            if (box.order != null)
            {
                DrawIcon(box.order.image, new Rect(rect.x+7,rect.y+10,40,42));
                GUI.Label(new Rect(rect.x+51,rect.y+5,rect.width-55,23), box.order.label, small);
                GUI.Label(new Rect(rect.x+51,rect.y+30,rect.width-55,26), $"{box.count}/{box.order.count}", text);
            }
            else GUI.Label(rect,"Xong", center);
        }

        GUI.Label(new Rect(hudX,hudY+69,hudWidth,20), $"Khay chờ · {game.Waiting}/5", small);
        var trayRects = new Rect[5];
        float trayWidth = Mathf.Min((hudWidth-24)/5,47);
        for(int i=0;i<5;i++)
        {
            var rect = trayRects[i] = new Rect(hudX+i*(trayWidth+6),hudY+94,trayWidth,36);
            Fill(rect, game.Waiting >= 4 ? Rose : Line);
            if(game.tray[i]>=0 && !(flying == game.tray[i] && now-flightStart < .19f))
                DrawIcon(level.items[game.tray[i]].image, new Rect(rect.x+3,rect.y+3,rect.width-6,30));
        }

        if (flying >= 0)
        {
            float t = (now-flightStart)/.19f;
            if (t>=1) flying = -1;
            else
            {
                var it = level.items[flying];
                var from = CanvasPoint(board, scale, it.x, it.y);
                var target = flight.move == TidyPreviewGame.Move.ToBox ? boxRects[flight.slot].center : trayRects[flight.slot].center;
                DrawItem(it, Vector2.Lerp(from,target,Mathf.SmoothStep(0,1,t)), Mathf.Lerp(scale, Mathf.Min(scale,31f/(float)Math.Max(Math.Abs(it.w),Math.Abs(it.h))), t));
            }
        }

        GUI.Label(new Rect(16,h-34,w-32,28), message, small);
        if (showGuide && game.State == TidyPreviewGame.Status.Playing && step < level.proof.Length && Button(new Rect(hudX+hudWidth-106, hudY+67,106,25), "Bước tiếp"))
            Tap(level.proof[step].x,level.proof[step].y);

        if (modal)
        {
            var r = new Rect(board.center.x-144,board.center.y-66,288,132);
            Fill(r, Ink);
            Fill(new Rect(r.x+2,r.y+2,r.width-4,r.height-4), game.State == TidyPreviewGame.Status.Won ? Mint : Rose);
            GUI.Label(new Rect(r.x,r.y+10,r.width,37), game.State == TidyPreviewGame.Status.Won ? "Đã dọn sạch!" : "Hết chỗ trong khay!", pill);
            if (Button(new Rect(r.x+29,r.y+60,111,40),"Chơi lại")) Load(index);
            if (Button(new Rect(r.x+148,r.y+60,111,40),"Màn tiếp",game.State == TidyPreviewGame.Status.Won && index+1<pack.levels.Length)) Load(index+1);
        }
        else if (Event.current.type == EventType.MouseDown && Event.current.button == 0 && board.Contains(Event.current.mousePosition))
        {
            var p = WorldPoint(board, scale, Event.current.mousePosition);
            Tap(p.x,p.y);
            Event.current.Use();
        }
    }

    void Tap(double x,double y)
    {
        var pick = game.Tap(x,y);
        if (pick.move == TidyPreviewGame.Move.Blocked)
        {
            bumped = pick.uid; bumpStart = Time.unscaledTime;
            message = "Món này bị đè. Dọn đồ phía trên trước.";
        }
        else if (pick.move == TidyPreviewGame.Move.ToBox || pick.move == TidyPreviewGame.Move.ToTray)
        {
            flying = pick.uid; flight = pick; flightStart = Time.unscaledTime;
            if (showGuide)
            {
                if (pick.uid == level.uids[step]) step++;
                else showGuide = false;
            }
            message = game.State == TidyPreviewGame.Status.Won ? "Tất cả đồ đã vào hộp."
                : game.State == TidyPreviewGame.Status.Lost ? "Khay đã đầy mà vẫn còn đồ cần dọn."
                : pick.move == TidyPreviewGame.Move.ToTray ? "Chưa có hộp phù hợp. Món đồ chuyển vào khay chờ." : "Đồ đã vào hộp.";
        }
        else if (pick.move == TidyPreviewGame.Move.TrayFull) message = "Khay đã đầy mà vẫn còn đồ cần dọn.";
    }

    Texture2D Texture(string key)
    {
        if (!art.TryGetValue(key,out var t)) art[key] = t = Resources.Load<Texture2D>("TidyPreview/Artwork/"+key);
        return t;
    }

    void DrawItem(TidyItem item, Vector2 p, float scale)
    {
        float w=(float)Math.Abs(item.w)*scale, h=(float)Math.Abs(item.h)*scale;
        var before = GUI.matrix;
        GUIUtility.RotateAroundPivot(-(float)item.angle,p);
        var r = new Rect(p.x-w*.5f,p.y-h*.5f,w,h);
        var t = Texture(item.image);
        GUI.DrawTextureWithTexCoords(r, t, new Rect(item.w<0?1:0,item.h<0?1:0,item.w<0?-1:1,item.h<0?-1:1));
        GUI.matrix=before;
    }

    void DrawIcon(string key, Rect r) { var t = Texture(key); GUI.DrawTexture(r,t,ScaleMode.ScaleToFit,true); }

    static void Fill(Rect r, Color c) { var before=GUI.color; GUI.color=c; GUI.DrawTexture(r,Texture2D.whiteTexture); GUI.color=before; }

    bool Button(Rect r, string label, bool enabled=true)
    {
        if (Event.current.type == EventType.Repaint) Fill(r, !enabled ? Line : r.Contains(Event.current.mousePosition) ? Mint : Color.white);
        bool before = GUI.enabled; GUI.enabled = enabled;
        bool click = GUI.Button(r,label,smallCentered ?? (smallCentered = new GUIStyle(small) { alignment = TextAnchor.MiddleCenter }));
        GUI.enabled = before;
        return click;
    }
    GUIStyle smallCentered;

    public static Rect Fit(Rect area, int w,int h)
    {
        float s=Mathf.Min(area.width/w,area.height/h);
        return new Rect(area.center.x-w*s*.5f,area.center.y-h*s*.5f,w*s,h*s);
    }

    public static Vector2 CanvasPoint(Rect board,float s,double x,double y) => new Vector2(board.center.x+(float)x*s,board.center.y-(float)y*s);
    public static TidyPoint WorldPoint(Rect board,float s,Vector2 p) => new TidyPoint { x=(p.x-board.center.x)/s,y=(board.center.y-p.y)/s };
}
