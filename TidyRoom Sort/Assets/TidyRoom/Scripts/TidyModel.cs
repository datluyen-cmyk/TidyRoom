using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace TidyRoom
{
    public enum ItemPlace { Room, Tray, Storage, Delivered }
    public enum RunState { Playing, Win, Lose }
    public sealed class BoxState { public int order=-1,count; }
    public sealed class TidyModel
    {
        public readonly LevelData Level;
        public readonly ItemPlace[] Places;
        public readonly List<int> Tray=new List<int>(),Storage=new List<int>();
        public readonly List<BoxState> Boxes=new List<BoxState>();
        public int Capacity=5,Next,PeakTray,Moves;
        public RunState State=RunState.Playing;
        public bool SourceGeometry,StrictFull;
        public string Message="Tap an uncovered item";
        Dictionary<int,List<CoverData>> artCovers=new Dictionary<int,List<CoverData>>();
        Dictionary<int,int> artSamples=new Dictionary<int,int>();
        public TidyModel(LevelData level)
        {
            Level=level;Places=new ItemPlace[level.content.Length];SourceGeometry=level.coverageMode=="source";
            StrictFull=level.source=="Happy";
            AddBox();AddBox();Settle();
        }
        public int Remaining=>Places.Count(p=>p==ItemPlace.Room);
        public int Delivered=>Places.Count(p=>p==ItemPlace.Delivered);
        public int TypeOf(int uid)=>Level.content[uid].sourceType;
        public int FindBox(int type)
        {
            int best=-1;
            for(int b=0;b<Boxes.Count;b++)if(Boxes[b].order>=0&&Level.order[Boxes[b].order].sourceType==type)
                if(best<0||Boxes[b].count>Boxes[best].count)best=b;
            return best;
        }
        public bool AddBox()
        {
            if(Boxes.Count>=3)return false;
            var box=new BoxState();Boxes.Add(box);Assign(box);Settle();State=RunState.Playing;Check();return true;
        }
        public bool AddSlot()
        {
            if(Capacity>=7)return false;Capacity++;State=RunState.Playing;Check();return true;
        }
        void Assign(BoxState b) { b.order=Next<Level.order.Length?Next++:-1;b.count=0; }
        void Deliver(int uid,int slot) { Places[uid]=ItemPlace.Delivered;Tray.Remove(uid);Storage.Remove(uid);Boxes[slot].count++; }
        void Settle()
        {
            bool changed=true;int guard=0;
            while(changed&&guard++<Level.order.Length+Level.content.Length+10)
            {
                changed=false;
                for(int b=0;b<Boxes.Count;b++)
                {
                    var box=Boxes[b];if(box.order<0)continue;
                    if(box.count>=Level.order[box.order].count){Assign(box);changed=true;}
                }
                foreach(int uid in Tray.Concat(Storage).ToArray())
                {int b=FindBox(TypeOf(uid));if(b>=0&&Boxes[b].count<Level.order[Boxes[b].order].count){Deliver(uid,b);changed=true;}}
            }
        }
        public bool IsCovered(int uid)
        {
            if(Places[uid]!=ItemPlace.Room)return false;
            var it=Level.content[uid];
            if(SourceGeometry&&it.reference!=null)
            {
                var alive=it.reference.covers.Where(c=>Places[c.uid]==ItemPlace.Room).ToArray();
                if(alive.Length==0)return false;
                if(alive.Length==1)return alive[0].ratio>=.045;
                if(alive.Length==2)
                {
                    if(alive.Any(c=>c.ratio>=.045))return true;
                    var pair=it.reference.pairs.FirstOrDefault(p=>(p.a==alive[0].uid&&p.b==alive[1].uid)||(p.b==alive[0].uid&&p.a==alive[1].uid));
                    return pair!=null&&pair.ratio>=.045;
                }
                return UnionCount(alive)/(double)Math.Max(1,it.reference.samples)>=.045;
            }
            EnsureArt(uid);
            return UnionCount(artCovers[uid].Where(c=>Places[c.uid]==ItemPlace.Room))/(double)Math.Max(1,artSamples[uid])>=Level.blockThreshold;
        }
        static int Pop(uint x) {x-=(x>>1)&0x55555555;x=(x&0x33333333)+((x>>2)&0x33333333);return (int)((((x+(x>>4))&0x0F0F0F0F)*0x01010101)>>24);}
        static int UnionCount(IEnumerable<CoverData> covers)
        {
            uint[] bits=null;foreach(var c in covers){if(bits==null)bits=new uint[c.bits.Length];for(int k=0;k<bits.Length;k++)bits[k]|=c.bits[k];}
            return bits==null?0:bits.Sum(x=>Pop(x));
        }
        void EnsureArt(int uid)
        {
            if(artCovers.ContainsKey(uid))return;
            var me=Level.content[uid];var points=new List<Vector2>();
            for(int y=0;y<me.maskH;y++)for(int x=0;x<me.maskW;x++)if(me.alpha[y*me.maskW+x]!=0)
                points.Add(me.World(new Vector2(((x+.5f)/me.maskW-.5f)*me.width,(.5f-(y+.5f)/me.maskH)*me.height)));
            var covers=new List<CoverData>();Rect bounds=me.Bounds();
            for(int j=uid+1;j<Level.content.Length;j++)
            {
                var other=Level.content[j];if(!bounds.Overlaps(other.Bounds()))continue;
                uint[] bits=new uint[(points.Count+31)/32];int count=0;
                for(int k=0;k<points.Count;k++)if(other.HitArt(points[k])){bits[k>>5]|=1u<<(k&31);count++;}
                if(count>0)covers.Add(new CoverData{uid=j,bits=bits});
            }
            artCovers[uid]=covers;artSamples[uid]=points.Count;
        }
        public bool HasDirectMove()=>Enumerable.Range(0,Places.Length).Any(i=>Places[i]==ItemPlace.Room&&FindBox(TypeOf(i))>=0&&!IsCovered(i));
        void Check()
        {
            if(Delivered==Places.Length){State=RunState.Win;Message="ALL TIDY!";return;}
            if(Tray.Count>=Capacity&&(StrictFull||!HasDirectMove())){State=RunState.Lose;Message="Waiting slots are full";}
        }
        public bool Tap(int uid)
        {
            if(State!=RunState.Playing||uid<0||uid>=Places.Length||Places[uid]!=ItemPlace.Room)return false;
            if(IsCovered(uid)){Message="Covered by another item";return false;}
            int box=FindBox(TypeOf(uid));
            if(box<0&&Tray.Count>=Capacity){Message="No empty waiting slot";return false;}
            if(box>=0)Deliver(uid,box);else{Places[uid]=ItemPlace.Tray;Tray.Add(uid);}
            Moves++;PeakTray=Math.Max(PeakTray,Tray.Count);Settle();Message=box>=0?"Sorted into its box":"Moved to a waiting slot";Check();return true;
        }
        public void Broom()
        {
            if(State==RunState.Win)return;
            foreach(int uid in Tray){Places[uid]=ItemPlace.Storage;Storage.Add(uid);}Tray.Clear();State=RunState.Playing;Settle();Message="Waiting items moved to temporary storage";Check();
        }
        public void Vacuum()
        {
            if(State==RunState.Win)return;
            int b=Boxes.FindIndex(x=>x.order>=0);if(b<0)return;
            int order=Boxes[b].order,type=Level.order[order].sourceType,need=Level.order[order].count-Boxes[b].count;
            foreach(int uid in Enumerable.Range(0,Places.Length).Where(i=>Places[i]!=ItemPlace.Delivered&&TypeOf(i)==type).Take(need).ToArray())Deliver(uid,b);
            State=RunState.Playing;Settle();Message="Vacuum filled a box";Check();
        }
        public int Hint()=>Enumerable.Range(0,Places.Length).Reverse().Where(i=>Places[i]==ItemPlace.Room&&FindBox(TypeOf(i))>=0&&!IsCovered(i)).DefaultIfEmpty(-1).First();
        public void Recheck(){if(State!=RunState.Win)State=RunState.Playing;Check();}
    }
}
