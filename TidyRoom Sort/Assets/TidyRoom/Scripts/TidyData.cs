using System;
using System.Collections.Generic;
using Newtonsoft.Json;
using UnityEngine;

namespace TidyRoom
{
    [Serializable] public class LevelIndex { public List<LevelEntry> levels; }
    [Serializable] public class LevelEntry { public string key,label,source,file; public bool review; }
    [Serializable] public class OrderData { public int type,sourceType,count,box; public string label; }
    [Serializable] public class CoverData { public int uid; public double ratio; public uint[] bits; }
    [Serializable] public class PairData { public int a,b; public double ratio; }
    [Serializable] public class ReferenceData { public int samples; public CoverData[] covers; public PairData[] pairs; }
    [Serializable] public class ItemData
    {
        public string id,sourceId,art;
        public int uid,type,sourceType,box,maskW,maskH;
        public float x,y,scaleX=1,scaleY=1,angle,width,height,sourceWidth,sourceHeight;
        public float[][] poly;
        public int[] alpha;
        public ReferenceData reference;
        public Vector2 World(Vector2 p)
        {
            float r=angle*Mathf.Deg2Rad,c=Mathf.Cos(r),s=Mathf.Sin(r);
            p=new Vector2(p.x*scaleX,p.y*scaleY);
            return new Vector2(x+p.x*c-p.y*s,y+p.x*s+p.y*c);
        }
        public Vector2 Local(Vector2 p)
        {
            p-=new Vector2(x,y);float r=angle*Mathf.Deg2Rad,c=Mathf.Cos(r),s=Mathf.Sin(r);
            return new Vector2((p.x*c+p.y*s)/scaleX,(-p.x*s+p.y*c)/scaleY);
        }
        public bool HitArt(Vector2 world)
        {
            Vector2 p=Local(world);int px=Mathf.FloorToInt((p.x/width+.5f)*maskW),py=Mathf.FloorToInt((.5f-p.y/height)*maskH);
            return px>=0&&py>=0&&px<maskW&&py<maskH&&alpha[py*maskW+px]!=0;
        }
        public bool HitSource(Vector2 world)
        {
            if(poly==null)return HitArt(world);
            Vector2 p=Local(world);bool inside=false;
            for(int i=0,j=poly.Length-1;i<poly.Length;j=i++)
            { var a=poly[i];var b=poly[j];if((a[1]>p.y)!=(b[1]>p.y)&&p.x<(b[0]-a[0])*(p.y-a[1])/(b[1]-a[1])+a[0])inside=!inside; }
            return inside;
        }
        public Rect Bounds()
        {
            var p=World(new Vector2(-width/2,-height/2));float x0=p.x,x1=p.x,y0=p.y,y1=p.y;
            foreach(var v in new[]{new Vector2(width/2,-height/2),new Vector2(width/2,height/2),new Vector2(-width/2,height/2)})
            {p=World(v);x0=Mathf.Min(x0,p.x);x1=Mathf.Max(x1,p.x);y0=Mathf.Min(y0,p.y);y1=Mathf.Max(y1,p.y);}
            return Rect.MinMaxRect(x0,y0,x1,y1);
        }
    }
    [Serializable] public class LevelData
    {
        public string key,levelName,name,source,bg,sourceBg,coverageMode,artTheme;
        public float[] bgSize;
        [JsonIgnore] public bool HasBackgroundComparison=>source=="RoomSort"&&!string.IsNullOrEmpty(sourceBg)&&sourceBg!=bg;
        [JsonIgnore] public string DefaultBackground=>HasBackgroundComparison?sourceBg:bg;
        public Vector2 BackgroundSize(string path,Vector2 imageSize)=>path==bg&&bgSize!=null&&bgSize.Length==2&&bgSize[0]>0&&bgSize[1]>0
            ?new Vector2(bgSize[0],bgSize[1]):imageSize;
        public float bgPosX,blockThreshold=.045f;
        public OrderData[] order;
        public ItemData[] content;
        public string[] issues;
        public int[] proof;
        public static LevelData Load(string path)
        {
            if(path.EndsWith(".gz",StringComparison.OrdinalIgnoreCase))
                using(var file=System.IO.File.OpenRead(path))
                using(var gzip=new System.IO.Compression.GZipStream(file,System.IO.Compression.CompressionMode.Decompress))
                using(var reader=new System.IO.StreamReader(gzip))return JsonConvert.DeserializeObject<LevelData>(reader.ReadToEnd());
            return JsonConvert.DeserializeObject<LevelData>(System.IO.File.ReadAllText(path));
        }
    }
}
