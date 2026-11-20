using System;
using UnityEngine;

[Serializable] public sealed class TidyPack { public bool strict; public double coverThreshold; public TidyLevel[] levels; }
[Serializable] public sealed class TidyLevel { public int number, w, h, peak; public string label, room; public TidyItem[] items; public TidyOrder[] order; public TidyPoint[] proof; public int[] uids; }
[Serializable] public struct TidyPoint { public double x, y; }
[Serializable] public struct TidyPair { public int x, y; }
[Serializable] public sealed class TidyItem { public int type, sampleCount; public string image; public double x, y, w, h, angle; public TidyPoint[] poly; public TidyCover[] covers; public TidyPair[] pairs; }
[Serializable] public sealed class TidyCover { public int uid; public bool alone; public string bits; [NonSerialized] public byte[] decoded; }
[Serializable] public sealed class TidyOrder { public int type, count; public string label, image; }

public sealed class TidyPreviewGame
{
    public const int BoxCount = 2, TrayCount = 5;
    public enum Status { Playing, Won, Lost }
    public enum Move { Blank, Blocked, ToBox, ToTray, TrayFull }
    public readonly struct Pick
    {
        public readonly Move move;
        public readonly int uid, slot;
        public Pick(Move move, int uid = -1, int slot = -1) { this.move = move; this.uid = uid; this.slot = slot; }
    }
    public sealed class Box { public TidyOrder order; public int count; }

    readonly TidyLevel level;
    readonly bool strict;
    readonly double threshold;
    int next;
    public readonly Box[] boxes = { new Box(), new Box() };
    public readonly int[] tray = { -1, -1, -1, -1, -1 };
    public readonly bool[] present;
    public int Remaining { get; private set; }
    public int Waiting { get { int n = 0; foreach (int uid in tray) if (uid >= 0) n++; return n; } }
    public Status State { get; private set; }

    public TidyPreviewGame(TidyPack pack, TidyLevel level)
    {
        this.level = level;
        strict = pack.strict;
        threshold = pack.coverThreshold;
        Remaining = level.items.Length;
        present = new bool[Remaining];
        for (int i = 0; i < present.Length; i++) present[i] = true;
        foreach (var box in boxes) Refill(box);
    }

    public Pick Tap(double x, double y)
    {
        if (State != Status.Playing) return new Pick(Move.Blank);
        for (int uid = present.Length - 1; uid >= 0; uid--)
            if (present[uid] && Contains(level.items[uid].poly, x, y))
                return Take(uid);
        return new Pick(Move.Blank);
    }

    Pick Take(int uid)
    {
        if (Covered(uid)) return new Pick(Move.Blocked, uid);
        int slot = FindBox(level.items[uid].type);
        if (slot >= 0)
        {
            Remove(uid);
            if (++boxes[slot].count == boxes[slot].order.count) Refill(boxes[slot]);
            CheckEnd();
            return new Pick(Move.ToBox, uid, slot);
        }
        for (int i = 0; i < tray.Length; i++)
            if (tray[i] < 0)
            {
                Remove(uid);
                tray[i] = uid;
                CheckEnd();
                return new Pick(Move.ToTray, uid, i);
            }
        State = Status.Lost;
        return new Pick(Move.TrayFull, uid);
    }

    void Remove(int uid) { present[uid] = false; Remaining--; }

    int FindBox(int type)
    {
        int best = -1;
        for (int i = 0; i < boxes.Length; i++)
            if (boxes[i].order != null && boxes[i].order.type == type && (best < 0 || boxes[i].count > boxes[best].count)) best = i;
        return best;
    }

    void Refill(Box box)
    {
        box.count = 0;
        box.order = null;
        while (next < level.order.Length)
        {
            box.order = level.order[next++];
            box.count = 0;
            for (int i = 0; i < tray.Length && box.count < box.order.count; i++)
                if (tray[i] >= 0 && level.items[tray[i]].type == box.order.type) { tray[i] = -1; box.count++; }
            if (box.count < box.order.count) return;
            box.order = null;
            box.count = 0;
        }
    }

    void CheckEnd()
    {
        if (Remaining == 0 && Waiting == 0 && boxes[0].order == null && boxes[1].order == null) { State = Status.Won; return; }
        if (Waiting < tray.Length) return;
        if (!strict)
            for (int i = 0; i < present.Length; i++)
                if (present[i] && FindBox(level.items[i].type) >= 0 && !Covered(i)) return;
        State = Status.Lost;
    }

    public bool Covered(int uid)
    {
        TidyItem it = level.items[uid];
        TidyCover first = null, second = null;
        int count = 0;
        foreach (var cover in it.covers)
            if (present[cover.uid]) { if (count == 0) first = cover; if (count == 1) second = cover; count++; }
        if (count == 0) return false;
        if (count == 1) return first.alone;
        if (count == 2)
        {
            foreach (var pair in it.pairs) if (pair.x == first.uid && pair.y == second.uid) return true;
            return false;
        }
        if (it.sampleCount <= 0) return false;
        byte[] union = new byte[(it.sampleCount + 7) / 8];
        foreach (var cover in it.covers)
        {
            if (!present[cover.uid]) continue;
            byte[] bits = cover.decoded ?? (cover.decoded = Convert.FromBase64String(cover.bits));
            for (int i = 0; i < union.Length; i++) union[i] |= bits[i];
        }
        int hit = 0;
        foreach (byte b in union) for (int a = b; a != 0; a &= a - 1) hit++;
        return (double)hit / it.sampleCount >= threshold;
    }

    static bool Contains(TidyPoint[] polygon, double x, double y)
    {
        const double eps = 0.0001;
        bool inside = false;
        for (int i = 0, j = polygon.Length - 1; i < polygon.Length; j = i++)
        {
            var a = polygon[j]; var b = polygon[i];
            double cross = (b.x-a.x)*(y-a.y)-(b.y-a.y)*(x-a.x);
            if (Math.Abs(cross) <= eps && x >= Math.Min(a.x,b.x)-eps && x <= Math.Max(a.x,b.x)+eps && y >= Math.Min(a.y,b.y)-eps && y <= Math.Max(a.y,b.y)+eps) return true;
            if ((a.y > y) != (b.y > y) && x < (b.x-a.x)*(y-a.y)/(b.y-a.y)+a.x) inside = !inside;
        }
        return inside;
    }

    public static TidyPack LoadPack()
    {
        var source = Resources.Load<TextAsset>("TidyPreview/Levels");
        if (source == null) throw new InvalidOperationException("Missing TidyPreview/Levels. Run prepare-levels.mjs first.");
        return JsonUtility.FromJson<TidyPack>(source.text);
    }
}
