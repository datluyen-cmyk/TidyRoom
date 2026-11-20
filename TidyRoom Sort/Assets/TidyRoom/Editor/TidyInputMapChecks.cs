using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using TidyRoom;

public static class TidyInputMapChecks
{
    [MenuItem("Tidy Room/Check Rapid Input and Maps")]
    public static void Check()
    {
        var h=UnityEngine.Object.FindAnyObjectByType<TidyHarness>();
        if(!EditorApplication.isPlaying||h==null)throw new InvalidOperationException("Enter Play mode first");
        var m=h.Model;
        var saved=JObject.FromObject(new {h.Selected,m.Places,m.Tray,m.Storage,m.Boxes,m.Next,m.Capacity,m.PeakTray,m.Moves,m.State,m.SourceGeometry,m.StrictFull,m.Message});
        var failures=new List<string>();var results=new List<object>();
        Action<bool,string> expect=(ok,test)=>{results.Add(new {test,pass=ok});if(!ok)failures.Add(test);};
        int map=0,step=0,burst=0,phase=0;double ready=EditorApplication.timeSinceStartup+.3;
        TidyModel reference=null;int[] proof=null;
        h.LoadLevel(130);
        EditorApplication.CallbackFunction tick=null;
        Action finish=()=>{
            EditorApplication.update-=tick;
            Restore(h,saved);
            File.WriteAllText("Evidence/input-map-regression.json",JsonConvert.SerializeObject(new {utc=DateTime.UtcNow,maps=map,rapidTaps=step,bursts=burst,failures,results},Formatting.Indented));
            if(failures.Count>0)Debug.LogError("Input/map checks: "+string.Join("; ",failures));else Debug.Log("Input/map checks PASS: rapid pointer input, counters, duplicate rejection, flight cleanup, all map framing.");
        };
        tick=()=>{
            if(h==null||!EditorApplication.isPlaying){EditorApplication.update-=tick;return;}
            if(EditorApplication.timeSinceStartup<ready)return;
            try
            {
                if(phase==0)
                {
                    Canvas.ForceUpdateCanvases();
                    var board=GameObject.Find("Room View").GetComponent<Image>();
                    if(board.depth<0)
                    {
                        if(EditorApplication.timeSinceStartup<ready+5)return;
                        expect(false,"Game View did not render the board before pointer checks");finish();return;
                    }
                    proof=h.Model.Level.proof;reference=new TidyModel(h.Model.Level);
                    expect(proof!=null&&proof.Length>0,"Source solution exists for pointer burst regression");phase=1;
                }
                if(phase==1)
                {
                    // No frames or animation completions between these six pointer clicks.
                    int before=h.Model.Moves,n=0;
                    for(;n<6&&step<proof.Length;n++,step++)
                    {
                        int uid=proof[step];bool point=TapPointer(h,uid),accepted=reference.Tap(uid);
                        bool equal=accepted&&h.Model.Moves==reference.Moves&&h.Model.Delivered==reference.Delivered&&
                            h.Model.Tray.SequenceEqual(reference.Tray)&&h.Model.Places.SequenceEqual(reference.Places)&&
                            JsonConvert.SerializeObject(h.Model.Boxes)==JsonConvert.SerializeObject(reference.Boxes);
                        expect(point&&equal,"Rapid pointer "+step+" updates items, slots and box counters immediately");
                        int moves=h.Model.Moves;expect(!h.Pick(uid)&&h.Model.Moves==moves,"Repeated UID "+uid+" is counted once");
                    }
                    burst++;expect(h.Model.Moves==before+n,"Every pointer in burst "+burst+" is accepted before flights finish");
                    if(failures.Count>0){finish();return;}
                    if(step<proof.Length){ready=EditorApplication.timeSinceStartup+.02;return;}
                    expect(h.Model.State==RunState.Win,"Rapid pointer solution wins across box changes and slot refills");
                    h.LoadLevel(2);
                    expect(!ActiveFlights(),"Changing level immediately clears concurrent flying items");
                    ready=EditorApplication.timeSinceStartup+.4;phase=2;return;
                }
                if(phase==2)
                {
                    expect(h.Model.Moves==0&&!ActiveFlights(),"Old flights cannot change counters or survive on the next map");phase=3;
                }
                // One map per editor update: release decoded textures before testing the next.
                if(phase==3&&map<h.Index.levels.Count)
                {
                    var level=LevelData.Load(Path.Combine(h.Root,h.Index.levels[map].file));
                    var texture=new Texture2D(2,2);Vector2 size;
                    try{expect(texture.LoadImage(File.ReadAllBytes(Path.Combine(h.Root,level.DefaultBackground))),level.key+" default background decodes");size=new Vector2(texture.width,texture.height);}
                    finally{UnityEngine.Object.DestroyImmediate(texture);}
                    size=level.BackgroundSize(level.DefaultBackground,size);
                    var f=new TidyRoomFraming(level,size);Rect view=TidyRoomFraming.PlayArea;
                    var low=f.Clamp(new Vector2(-100000,-100000),f.Scale);var high=f.Clamp(new Vector2(100000,100000),f.Scale);
                    bool reachable=level.content.All(i=>{
                        var b=i.Bounds();return b.xMin*f.Scale+high.x>=view.xMin-0.1f&&b.xMax*f.Scale+low.x<=view.xMax+0.1f&&
                            b.yMin*f.Scale+high.y>=view.yMin-0.1f&&b.yMax*f.Scale+low.y<=view.yMax+0.1f;
                    });
                    expect(reachable,level.key+" all item edges reachable between HUD and footer at pan limits");
                    expect(f.Scale*size.x>=1080-.1f&&f.Scale*size.y>=1920-.1f,level.key+" room spans phone dimensions at original aspect");
                    if(new[]{0,1,2,66,129,139,203}.Contains(map))
                    {
                        h.LoadLevel(map);
                        var background=GameObject.Find("Room background").GetComponent<RawImage>();
                        var world=(RectTransform)background.transform.parent;
                        expect(background.uvRect==new Rect(0,0,1,1)&&background.rectTransform.sizeDelta==size&&
                            background.rectTransform.anchoredPosition==Vector2.zero&&Mathf.Abs(size.x/size.y-background.texture.width/(float)background.texture.height)<.001f,
                            level.key+" actual room texture retains source aspect and full UVs");
                        h.Zoom(3);h.Pan(new Vector2(100000,100000));h.Pan(new Vector2(-200000,-200000));
                        expect(background.uvRect==new Rect(0,0,1,1)&&background.rectTransform.sizeDelta==size&&
                            Mathf.Approximately(world.localScale.x,world.localScale.y),level.key+" zoom and extreme drags never stretch background");
                    }
                    map++;if(map<h.Index.levels.Count)return;
                    finish();
                }
            }
            catch(Exception e){expect(false,e.ToString());finish();}
        };
        EditorApplication.update+=tick;
    }

    static bool ActiveFlights()=>UnityEngine.Object.FindObjectsByType<RawImage>(FindObjectsSortMode.None).Any(i=>i.name=="Flying item"&&i.gameObject.activeInHierarchy)||
        UnityEngine.Object.FindObjectsByType<Image>(FindObjectsSortMode.None).Any(i=>i.name=="Flying item"&&i.gameObject.activeInHierarchy);

    static bool TapPointer(TidyHarness h,int uid)
    {
        var world=(RectTransform)GameObject.Find("Room Coordinates").transform;
        var canvas=world.GetComponentInParent<Canvas>();var item=h.Model.Level.content[uid];
        var phone=(RectTransform)world.parent.parent;
        Vector2 current=phone.InverseTransformPoint(world.TransformPoint(new Vector2(item.x,item.y)));
        h.Pan((TidyRoomFraming.PlayArea.center-current)*canvas.scaleFactor);
        Canvas.ForceUpdateCanvases();Rect bounds=item.Bounds();
        for(int y=0;y<35;y++)for(int x=0;x<35;x++)
        {
            Vector2 p=new Vector2(Mathf.Lerp(bounds.xMin,bounds.xMax,(x+.5f)/35),Mathf.Lerp(bounds.yMin,bounds.yMax,(y+.5f)/35));
            if(!(h.Model.SourceGeometry?item.HitSource(p):item.HitArt(p)))continue;
            if(h.Model.Level.content.Skip(uid+1).Any(i=>h.Model.Places[i.uid]==ItemPlace.Room&&(h.Model.SourceGeometry?i.HitSource(p):i.HitArt(p))))continue;
            var screen=RectTransformUtility.WorldToScreenPoint(null,world.TransformPoint(p));
            var e=new PointerEventData(EventSystem.current){position=screen,button=PointerEventData.InputButton.Left};
            var hits=new List<RaycastResult>();EventSystem.current.RaycastAll(e,hits);
            if(hits.Count==0||hits[0].gameObject.GetComponent<BoardPointer>()==null)continue;
            ExecuteEvents.Execute(hits[0].gameObject,e,ExecuteEvents.pointerDownHandler);
            ExecuteEvents.Execute(hits[0].gameObject,e,ExecuteEvents.pointerClickHandler);return true;
        }
        return false;
    }

    static void Restore(TidyHarness h,JObject s)
    {
        h.LoadLevel(s["Selected"].ToObject<int>());var m=h.Model;
        s["Places"].ToObject<ItemPlace[]>().CopyTo(m.Places,0);
        m.Tray.Clear();m.Tray.AddRange(s["Tray"].ToObject<int[]>());
        m.Storage.Clear();m.Storage.AddRange(s["Storage"].ToObject<int[]>());
        m.Boxes.Clear();m.Boxes.AddRange(s["Boxes"].ToObject<BoxState[]>());
        m.Next=s["Next"].ToObject<int>();m.Capacity=s["Capacity"].ToObject<int>();m.PeakTray=s["PeakTray"].ToObject<int>();m.Moves=s["Moves"].ToObject<int>();
        m.State=s["State"].ToObject<RunState>();m.SourceGeometry=s["SourceGeometry"].ToObject<bool>();m.StrictFull=s["StrictFull"].ToObject<bool>();m.Message=s["Message"].ToString();
        typeof(TidyHarness).GetMethod("Render",System.Reflection.BindingFlags.Instance|System.Reflection.BindingFlags.NonPublic).Invoke(h,null);
    }
}
