using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using Newtonsoft.Json;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using TidyRoom;

public static class TidyRuntimeChecks
{
    [MenuItem("Tidy Room/Check Runtime UI")]
    public static void Check()
    {
        var h=UnityEngine.Object.FindAnyObjectByType<TidyHarness>();
        if(!EditorApplication.isPlaying||h==null)throw new InvalidOperationException("Enter Play mode first");
        h.LoadLevel(139);
        // Wait for a rendered frame: newly created uGUI graphics have depth -1 before render.
        double ready=EditorApplication.timeSinceStartup+.5;
        EditorApplication.CallbackFunction tick=null;
        tick=()=>{if(EditorApplication.timeSinceStartup<ready)return;EditorApplication.update-=tick;if(h!=null)Run(h);};
        EditorApplication.update+=tick;
    }
    static void Run(TidyHarness h)
    {
        var results=new List<object>();var failures=new List<string>();
        Action<bool,string> expect=(ok,test)=>{results.Add(new{test,pass=ok});if(!ok)failures.Add(test);};
        Action<string> submit=name=>{
            var b=UnityEngine.Object.FindObjectsByType<Button>(FindObjectsSortMode.None).First(x=>x.gameObject.activeInHierarchy&&x.name==name);
            ExecuteEvents.Execute(b.gameObject,new BaseEventData(EventSystem.current),ExecuteEvents.submitHandler);
        };
        Canvas.ForceUpdateCanvases();
        var world=GameObject.Find("Room Coordinates").transform;int moves=h.Model.Moves;bool clicked=false;int target=-1;
        for(int uid=h.Model.Places.Length-1;uid>=0&&!clicked;uid--)
        {
            if(h.Model.IsCovered(uid))continue;var it=h.Model.Level.content[uid];
            for(int y=0;y<it.maskH&&!clicked;y++)for(int x=0;x<it.maskW&&!clicked;x++)
            {
                if(it.alpha[y*it.maskW+x]==0)continue;
                var p=it.World(new Vector2(((x+.5f)/it.maskW-.5f)*it.width,(.5f-(y+.5f)/it.maskH)*it.height));
                if(h.Model.Level.content.Skip(uid+1).Any(i=>i.HitArt(p)))continue;
                var screen=RectTransformUtility.WorldToScreenPoint(null,world.TransformPoint(p));
                var evt=new PointerEventData(EventSystem.current){position=screen,button=PointerEventData.InputButton.Left};var hits=new List<RaycastResult>();EventSystem.current.RaycastAll(evt,hits);
                if(hits.Count==0||hits[0].gameObject.GetComponent<BoardPointer>()==null)continue;
                ExecuteEvents.Execute(hits[0].gameObject,evt,ExecuteEvents.pointerClickHandler);clicked=true;target=uid;
            }
        }
        expect(clicked&&h.Model.Moves==moves+1,"Pointer raycast picks visible native Happy item");
        submit("Restart");expect(h.Model.Moves==0&&h.Model.Remaining==36,"Restart restores native board");
        submit("Levels");expect(UnityEngine.Object.FindObjectsByType<Text>(FindObjectsSortMode.None).Any(t=>t.text=="CHOOSE LEVEL"),"Level picker opens through UI submit");
        submit(h.Index.levels[1].label+(h.Index.levels[1].review?"  *":""));expect(h.Selected==1&&h.Model.Level.key=="room_002","Picker loads converted Room board");
        var model=h.Model;
        var backdrop=GameObject.Find("Room background").GetComponent<RawImage>();
        var original=backdrop.texture;
        expect(model.Level.DefaultBackground=="Art/RoomBG/2.jpg"&&original!=null,"RoomSort loads its original room background by default");
        int item=Enumerable.Range(0,model.Places.Length).Last(uid=>!model.IsCovered(uid));
        expect(h.Pick(item),"Pick an item before changing background");
        var places=model.Places.ToArray();
        submit("Test options");submit("Background: RoomSort original");
        expect(backdrop.texture!=null&&backdrop.texture!=original,"Background option shows the Tidy Room texture");
        expect(h.Model==model&&h.Model.Moves==1&&places.SequenceEqual(h.Model.Places),"Background switch preserves current play state");
        submit("Test options");submit("Background: Tidy Room");
        expect(backdrop.texture==original&&h.Model.Moves==1,"Switching back restores the original texture without restarting");
        submit("Test options");submit("Collision: RoomSort source");expect(!h.Model.SourceGeometry,"Collision option switches to current item image silhouettes");submit("Close");
        submit("Restart");expect(h.Model.SourceGeometry&&h.Model.Moves==0,"Restart restores source comparison defaults");
        string path=Path.GetFullPath("Evidence/runtime-ui.json");File.WriteAllText(path,JsonConvert.SerializeObject(new{utc=DateTime.UtcNow,target,failures,results},Formatting.Indented));
        if(failures.Count>0)Debug.LogError("Runtime UI failed: "+string.Join(";",failures));else Debug.Log("Runtime UI PASS: click, restart, picker, mode switch.");
    }
}
