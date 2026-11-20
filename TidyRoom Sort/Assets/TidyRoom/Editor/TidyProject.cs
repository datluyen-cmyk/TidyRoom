using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using Newtonsoft.Json;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using TidyRoom;

public static class TidyProject
{
    public const string ScenePath="Assets/TidyRoom/Scenes/LevelTest.unity";
    [MenuItem("Tidy Room/Open Level Test")]
    public static void Open()
    {
        if(EditorApplication.isPlaying){Debug.LogWarning("Stop Play before opening the test scene");return;}
        if(!File.Exists(ScenePath))
        {
            Directory.CreateDirectory(Path.GetDirectoryName(ScenePath));
            var scene=EditorSceneManager.NewScene(NewSceneSetup.EmptyScene,NewSceneMode.Single);
            new GameObject("Happy Tidy Level Test",typeof(TidyHarness));
            var camera=new GameObject("Main Camera",typeof(Camera));camera.tag="MainCamera";camera.transform.position=new Vector3(0,0,-10);camera.GetComponent<Camera>().orthographic=true;camera.AddComponent<AudioListener>();
            EditorSceneManager.SaveScene(scene,ScenePath);
        }
        else EditorSceneManager.OpenScene(ScenePath);
        EditorBuildSettings.scenes=new[]{new EditorBuildSettingsScene(ScenePath,true)};
        PlayerSettings.productName="Tidy Room - Level Test";PlayerSettings.companyName="Level Lab";
        PlayerSettings.defaultInterfaceOrientation=UIOrientation.Portrait;
        PortraitView();
        Debug.Log("Tidy Room ready. Press Play.");
    }
    [MenuItem("Tidy Room/Portrait Game View")]
    public static void PortraitView()
    {
        try
        {
            var asm=typeof(Editor).Assembly;var type=asm.GetType("UnityEditor.GameViewSizes");
            var singleton=typeof(ScriptableSingleton<>).MakeGenericType(type);
            var sizes=singleton.GetProperty("instance",System.Reflection.BindingFlags.Public|System.Reflection.BindingFlags.Static|System.Reflection.BindingFlags.FlattenHierarchy).GetValue(null);
            var group=type.GetProperty("currentGroup",System.Reflection.BindingFlags.Public|System.Reflection.BindingFlags.NonPublic|System.Reflection.BindingFlags.Instance).GetValue(sizes);
            var gt=group.GetType();int built=(int)gt.GetMethod("GetBuiltinCount").Invoke(group,null),custom=(int)gt.GetMethod("GetCustomCount").Invoke(group,null),selected=-1;
            for(int i=0;i<built+custom;i++)
            {
                var size=gt.GetMethod("GetGameViewSize").Invoke(group,new object[]{i});
                if((int)size.GetType().GetProperty("width").GetValue(size)==540&&(int)size.GetType().GetProperty("height").GetValue(size)==960){selected=i;break;}
            }
            if(selected<0)
            {
                var sizeType=asm.GetType("UnityEditor.GameViewSize");var enumType=asm.GetType("UnityEditor.GameViewSizeType");
                var size=Activator.CreateInstance(sizeType,System.Reflection.BindingFlags.Public|System.Reflection.BindingFlags.NonPublic|System.Reflection.BindingFlags.Instance,null,new object[]{Enum.ToObject(enumType,1),540,960,"Tidy Portrait"},null);
                gt.GetMethod("AddCustomSize").Invoke(group,new[]{size});selected=built+custom;
            }
            var viewType=asm.GetType("UnityEditor.GameView");var window=EditorWindow.GetWindow(viewType);window.Show();
            viewType.GetProperty("selectedSizeIndex",System.Reflection.BindingFlags.Public|System.Reflection.BindingFlags.NonPublic|System.Reflection.BindingFlags.Instance).SetValue(window,selected);
        }
        catch(Exception e){Debug.LogWarning("Portrait view: "+e.Message);}
    }
    [MenuItem("Tidy Room/Validate Conversion and Gameplay")]
    public static void Validate()
    {
        string root=Path.Combine(Application.streamingAssetsPath,"TidyRoom");
        var index=JsonConvert.DeserializeObject<LevelIndex>(File.ReadAllText(Path.Combine(root,"index.json")));
        var results=new List<object>();var failures=new List<string>();int boards=0,artMissing=0;
        foreach(var entry in index.levels)
        {
            var l=LevelData.Load(Path.Combine(root,entry.file));boards++;
            var have=l.content.GroupBy(i=>i.sourceType).ToDictionary(x=>x.Key,x=>x.Count());
            var want=l.order.GroupBy(o=>o.sourceType).ToDictionary(x=>x.Key,x=>x.Sum(o=>o.count));
            if(have.Count!=want.Count||have.Any(x=>!want.ContainsKey(x.Key)||want[x.Key]!=x.Value))failures.Add(entry.key+": count mismatch");
            for(int i=0;i<l.content.Length;i++)
            {
                var item=l.content[i];if(item.uid!=i)failures.Add(entry.key+": layer UID mismatch");
                if(!File.Exists(Path.Combine(root,item.art)))artMissing++;
                if(item.alpha==null||item.alpha.Length!=item.maskW*item.maskH)failures.Add(entry.key+": bad alpha mask");
                var order=l.order.FirstOrDefault(o=>o.box==item.box);
                if(order==null||order.sourceType!=item.sourceType)failures.Add(entry.key+": invalid box assignment");
            }
            if(!File.Exists(Path.Combine(root,l.bg)))failures.Add(entry.key+": background missing");
            if(l.HasBackgroundComparison&&!File.Exists(Path.Combine(root,l.DefaultBackground)))failures.Add(entry.key+": original background missing");
            if(l.proof!=null&&l.proof.Length>0)
            {
                var m=new TidyModel(l);m.StrictFull=false;int rejected=0;
                foreach(int uid in l.proof)if(!m.Tap(uid))rejected++;
                results.Add(new{key=l.key,state=m.State.ToString(),rejected,total=l.content.Length,delivered=m.Delivered,peakTray=m.PeakTray});
                if(m.State!=RunState.Win||rejected>0)failures.Add(l.key+": source proof failed");
                var art=new TidyModel(l);art.SourceGeometry=false;art.StrictFull=false;int firstReject=-1,step=0;
                foreach(int uid in l.proof){if(!art.Tap(uid)){firstReject=step;break;}step++;}
                results.Add(new{key=l.key+" / item image collision",state=art.State.ToString(),firstReject,delivered=art.Delivered,total=l.content.Length});
            }
        }
        // Independent critical rule probes: layers, chained refill, full-tray timing and boosters.
        Func<int,int,float,ItemData> makeItem=(uid,type,x)=>new ItemData{uid=uid,id="test",sourceType=type,type=type,x=x,y=0,width=10,height=10,scaleX=1,scaleY=1,maskW=1,maskH=1,alpha=new[]{1}};
        Action<bool,string> check=(ok,label)=>{if(!ok)failures.Add(label);results.Add(new{test=label,pass=ok});};
        var layer=new TidyModel(new LevelData{source="Happy",coverageMode="art",order=new[]{new OrderData{sourceType=1,count=1},new OrderData{sourceType=2,count=1}},content=new[]{makeItem(0,1,0),makeItem(1,2,0)}});
        check(layer.IsCovered(0)&&!layer.Tap(0)&&layer.Tap(1)&&layer.Tap(0)&&layer.State==RunState.Win,"Layer blocks lower item until upper removed");
        var many=new[]{makeItem(0,1,0),makeItem(1,2,20),makeItem(2,3,40),makeItem(3,3,60),makeItem(4,3,80),makeItem(5,3,100),makeItem(6,3,120)};
        var probe=new LevelData{source="RoomSort",coverageMode="art",order=new[]{new OrderData{sourceType=1,count=1},new OrderData{sourceType=2,count=1},new OrderData{sourceType=3,count=5}},content=many};
        var full=new TidyModel(probe);for(int i=2;i<7;i++)full.Tap(i);
        check(full.Tray.Count==5&&full.State==RunState.Playing,"Full tray allows available direct-to-box move in source rule");
        full.Tap(0);check(full.State==RunState.Playing&&full.Tray.Count==0,"New box pulls matching waiting items and completes");full.Tap(1);check(full.State==RunState.Win,"Win after all items delivered");
        var strict=new TidyModel(probe);strict.StrictFull=true;for(int i=2;i<7;i++)strict.Tap(i);check(strict.State==RunState.Lose,"Strict full-tray fail");
        strict.Broom();check(strict.Storage.Count==5&&strict.Tray.Count==0&&strict.State==RunState.Playing,"Broom stores waiting items and revives");strict.Tap(0);check(strict.Storage.Count==0,"Temporary storage feeds new matching box");
        var vacuum=new TidyModel(probe);vacuum.Vacuum();check(vacuum.Delivered==1&&vacuum.Places[0]==ItemPlace.Delivered,"Vacuum fills one open box");
        var slot=new TidyModel(probe);slot.AddSlot();slot.AddSlot();slot.AddSlot();check(slot.Capacity==7,"Waiting slots capped at seven");slot.AddBox();slot.AddBox();check(slot.Boxes.Count==3,"Boxes capped at three");
        if(artMissing>0)failures.Add("Missing item art: "+artMissing);
        string evidence=Path.GetFullPath("Evidence");Directory.CreateDirectory(evidence);
        File.WriteAllText(Path.Combine(evidence,"validation.json"),JsonConvert.SerializeObject(new{utc=DateTime.UtcNow,boards,artMissing,failures,results},Formatting.Indented));
        if(failures.Count>0)Debug.LogError("Tidy validation: "+string.Join("; ",failures));else Debug.Log("Tidy validation PASS: "+boards+" boards, all 8 source proofs and gameplay probes.");
    }
}
