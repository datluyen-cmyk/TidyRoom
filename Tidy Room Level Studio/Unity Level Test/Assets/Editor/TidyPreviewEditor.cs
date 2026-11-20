using System;
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

public static class TidyPreviewEditor
{
    const string Scene = "Assets/Level Test.unity";

    [MenuItem("Tidy Room/Play Level Test")]
    public static void OpenForPlay()
    {
        EditorApplication.delayCall += () =>
        {
            if (EditorApplication.isPlayingOrWillChangePlaymode) return;
            if (!EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo()) return;
            EditorSceneManager.OpenScene(Scene);
            EditorApplication.ExecuteMenuItem("Window/General/Game");
            EditorApplication.EnterPlaymode();
        };
    }

    public static void PrepareAndVerify()
    {
        try
        {
            var pack = TidyPreviewGame.LoadPack();
            var artwork = new HashSet<string>();
            var report = new List<string> { "Unity " + Application.unityVersion + " · click replay · strict tray=" + pack.strict };
            foreach (var level in pack.levels)
            {
                artwork.Add(level.room);
                foreach (var item in level.items) artwork.Add(item.image);
                foreach (var order in level.order) artwork.Add(order.image);
                // Exercise the same fitted play area projection the Game view uses in both layouts.
                CheckReplay(pack, level, new Rect(14,65,790,680));
                int peak = CheckReplay(pack, level, new Rect(14,218,622,590));
                report.Add($"Level {level.number}: won in {level.proof.Length} clicks; peak tray {peak}/5.");
            }
            foreach (var key in artwork)
                Require(!string.IsNullOrEmpty(key) && Resources.Load<Texture2D>("TidyPreview/Artwork/"+key) != null, "Missing texture: " + key);
            CheckInteraction();
            report.Add($"{pack.levels.Length} levels; {artwork.Count} textures. Blocked click, buffer transfer and full tray verified.");
            EnsureScene();
            File.WriteAllLines("verification.txt", report);
            Debug.Log(string.Join("\n", report));
            if (Application.isBatchMode) EditorApplication.Exit(0);
        }
        catch (Exception e)
        {
            Debug.LogException(e);
            if (Application.isBatchMode) EditorApplication.Exit(1);
            else throw;
        }
    }

    static void EnsureScene()
    {
        if (File.Exists(Scene)) { EditorSceneManager.OpenScene(Scene); return; }
        var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
        var camera = new GameObject("Camera").AddComponent<Camera>();
        camera.transform.position = new Vector3(0,0,-10);
        camera.orthographic = true;
        camera.cullingMask = 0;
        camera.backgroundColor = new Color32(250,247,239,255);
        camera.clearFlags = CameraClearFlags.SolidColor;
        new GameObject("Level Test").AddComponent<TidyPreviewView>();
        EditorSceneManager.SaveScene(scene, Scene);
        EditorBuildSettings.scenes = new[] { new EditorBuildSettingsScene(Scene,true) };
    }

    static int CheckReplay(TidyPack pack,TidyLevel level,Rect area)
    {
        var game = new TidyPreviewGame(pack,level);
        var board = TidyPreviewView.Fit(area,level.w,level.h);
        float scale = board.width/level.w;
        Require(level.proof.Length == level.items.Length && level.proof.Length == level.uids.Length,"Incomplete proof");
        int peak = 0;
        for (int i=0;i<level.proof.Length;i++)
        {
            var point = level.proof[i];
            var click = TidyPreviewView.CanvasPoint(board,scale,point.x,point.y);
            Require(board.Contains(click),$"Level {level.number}, click {i+1} is offscreen");
            var world = TidyPreviewView.WorldPoint(board,scale,click);
            var pick = game.Tap(world.x,world.y);
            Require(pick.uid==level.uids[i] && (pick.move==TidyPreviewGame.Move.ToBox || pick.move==TidyPreviewGame.Move.ToTray),$"Level {level.number}, click {i+1}: {pick.move} picked {pick.uid}; expected {level.uids[i]}");
            peak = Math.Max(peak,game.Waiting);
        }
        Require(game.State==TidyPreviewGame.Status.Won && game.Remaining==0 && game.Waiting==0 && peak==level.peak,$"Level {level.number} did not finish with expected tray peak {level.peak} (was {peak}).");
        return peak;
    }

    static TidyItem Item(int type, double left, double right, params TidyCover[] covers)
    {
        return new TidyItem { type=type, covers=covers, pairs=Array.Empty<TidyPair>(), poly=new[]{new TidyPoint{x=left,y=0},new TidyPoint{x=right,y=0},new TidyPoint{x=right,y=4},new TidyPoint{x=left,y=4}} };
    }

    static void CheckInteraction()
    {
        var strict = new TidyPack { strict=true,coverThreshold=.045 };
        var layered = new TidyLevel { items=new[]{Item(1,0,5,new TidyCover {uid=1,alone=true}),Item(2,2,5),Item(3,6,7)}, order=new[]{new TidyOrder{type=1,count=1},new TidyOrder{type=2,count=1},new TidyOrder{type=3,count=1}} };
        var game = new TidyPreviewGame(strict,layered);
        Require(game.Tap(1,2).move == TidyPreviewGame.Move.Blocked && game.Remaining==3,"A covered item was collected");
        Require(game.Tap(6.5,2).move == TidyPreviewGame.Move.ToTray && game.Waiting==1,"A nonmatching item did not wait");
        Require(game.Tap(3,2).uid==1 && game.Waiting==0,"The topmost item must be picked, opening a box that pulls from the tray");
        Require(game.Tap(1,2).move == TidyPreviewGame.Move.ToBox && game.State == TidyPreviewGame.Status.Won,"Item must be available after removal of the layer above");

        var crowded = new TidyLevel {items=new[]{Item(1,0,1),Item(2,2,3),Item(3,4,5),Item(3,6,7),Item(3,8,9),Item(3,10,11),Item(3,12,13)},order=new[]{new TidyOrder{type=1,count=1},new TidyOrder{type=2,count=1},new TidyOrder{type=3,count=5}}};
        game = new TidyPreviewGame(strict,crowded);
        for (int i=0;i<5;i++) game.Tap(4.5+i*2,2);
        Require(game.State==TidyPreviewGame.Status.Lost && game.Waiting==5,"The fifth waiting item must end the strict test");
        game = new TidyPreviewGame(new TidyPack { strict=false,coverThreshold=.045 },crowded);
        for (int i=0;i<5;i++) game.Tap(4.5+i*2,2);
        Require(game.State==TidyPreviewGame.Status.Playing,"The RoomSort rule must allow a direct move at a full tray");
        game.Tap(.5,2);
        game.Tap(2.5,2);
        Require(game.State==TidyPreviewGame.Status.Won,"Direct play must open the matching box and drain the full tray");
    }

    static void Require(bool ok,string message) { if(!ok) throw new InvalidOperationException(message); }
}
