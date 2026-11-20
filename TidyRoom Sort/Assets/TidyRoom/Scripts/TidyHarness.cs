using System;
using System.IO;
using System.Linq;
using System.Collections;
using System.Collections.Generic;
using Newtonsoft.Json;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using UnityEngine.InputSystem.UI;

namespace TidyRoom
{
    public class BoardPointer : MonoBehaviour, IPointerDownHandler, IPointerClickHandler, IBeginDragHandler, IDragHandler, IEndDragHandler, IScrollHandler
    {
        public TidyHarness Owner;
        bool dragged;
        public void OnPointerDown(PointerEventData e){dragged=false;}
        public void OnPointerClick(PointerEventData e){if(!dragged)Owner.BoardTap(e.position);dragged=false;}
        public void OnBeginDrag(PointerEventData e){dragged=true;}
        public void OnDrag(PointerEventData e){Owner.Pan(e.delta);}
        public void OnEndDrag(PointerEventData e){}
        public void OnScroll(PointerEventData e){Owner.Zoom(e.scrollDelta.y>0?1.1f:.9f);}
    }
    public class TidyHarness : MonoBehaviour
    {
        public TidyModel Model;
        public LevelIndex Index;
        public int Selected;
        public string Root=>TidyAssetCache.Root;
        readonly Dictionary<string,Sprite> cache=new Dictionary<string,Sprite>();
        RectTransform canvas,phone,board,world,hud,modal;
        RawImage roomBackdrop;
        bool compareBackground;
        TidyRoomFraming framing;
        readonly List<RectTransform> flyingItems=new List<RectTransform>();
        readonly List<RectTransform> itemViews=new List<RectTransform>();
        Font font;
        float fit=1,zoom=1;Vector2 center,pan;
        static Vector2 BoxPosition(int box)=>new Vector2(-330+box*330,753);
        static Vector2 SlotPosition(int slot)=>new Vector2(-378+slot*126,600);
        static readonly string[] CommonUi={"GP_Box0","GP_Box_Unlock","GP_Slot","NewBooster_Icon_Vaccum","NewBooster_Icon_Clear"};
        static bool UsesTidyRoomArt(LevelData level)=>level.artTheme=="TidyRoom";
        static string UiPath(LevelData level,string name)=>"Art/"+(UsesTidyRoomArt(level)?"TidyRoomUI/":"UI/")+name+".png";
        Sprite UiArt(string name)=>Art(UiPath(Model.Level,name));
        bool TidyRoomArt=>UsesTidyRoomArt(Model.Level);
        bool busy,showAvailability;
        string filter="RoomSort";int page;
        Color ink=new Color(.24f,.18f,.32f),cream=new Color(1,.97f,.89f),purple=new Color(.46f,.31f,.68f);
        IEnumerator Start()
        {
            Application.targetFrameRate=60;
            Application.runInBackground=true;
            font=Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            var go=new GameObject("Tidy Room Canvas",typeof(Canvas),typeof(CanvasScaler),typeof(GraphicRaycaster));
            var cv=go.GetComponent<Canvas>();cv.renderMode=RenderMode.ScreenSpaceOverlay;canvas=(RectTransform)go.transform;
            var scaler=go.GetComponent<CanvasScaler>();scaler.uiScaleMode=CanvasScaler.ScaleMode.ScaleWithScreenSize;scaler.referenceResolution=new Vector2(1080,1920);scaler.screenMatchMode=CanvasScaler.ScreenMatchMode.Expand;
            var bg=Image(canvas,"Screen",null,new Vector2(0,0),new Vector2(8000,4000),new Color(.13f,.10f,.19f));
            phone=Panel(canvas,"Phone",Vector2.zero,new Vector2(1080,1920),new Color(.90f,.85f,.96f));
            if(FindAnyObjectByType<EventSystem>()==null)new GameObject("EventSystem",typeof(EventSystem),typeof(InputSystemUIInputModule));
            if(TidyAssetCache.InAndroidPlayer)
            {
                var loading=Text(phone,"Loading level data...",Vector2.zero,new Vector2(950,200),36);
                string error=null;yield return TidyAssetCache.Fetch("index.json",e=>error=e);
                if(error!=null){loading.text=error;yield break;}Destroy(loading.gameObject);
            }
            Index=JsonConvert.DeserializeObject<LevelIndex>(File.ReadAllText(Path.Combine(Root,"index.json")));
            LoadLevel(PlayerPrefs.GetInt("TidyTestLevel",0));
        }
        void OnDestroy()
        {
            foreach(var sp in cache.Values){if(sp!=null){Destroy(sp.texture);Destroy(sp);}}
            if(canvas!=null)Destroy(canvas.gameObject);
        }
        RectTransform Rect(Transform parent,string name,Vector2 pos,Vector2 size)
        {var g=new GameObject(name,typeof(RectTransform));g.transform.SetParent(parent,false);var r=(RectTransform)g.transform;r.sizeDelta=size;r.anchoredPosition=pos;return r;}
        RectTransform Panel(Transform p,string n,Vector2 xy,Vector2 size,Color color)=>Image(p,n,null,xy,size,color).rectTransform;
        Image Image(Transform parent,string name,Sprite sp,Vector2 xy,Vector2 size,Color? color=null)
        {
            var r=Rect(parent,name,xy,size);var im=r.gameObject.AddComponent<Image>();im.sprite=sp;im.color=color??Color.white;im.raycastTarget=false;return im;
        }
        Text Text(Transform p,string value,Vector2 pos,Vector2 size,int fs=28,Color? color=null,TextAnchor align=TextAnchor.MiddleCenter)
        {var r=Rect(p,"Text",pos,size);var t=r.gameObject.AddComponent<Text>();t.text=value;t.font=font;t.fontSize=fs;t.color=color??ink;t.alignment=align;t.raycastTarget=false;t.horizontalOverflow=HorizontalWrapMode.Wrap;return t;}
        Button Button(Transform p,string value,Vector2 pos,Vector2 size,Action action,Color? color=null)
        {
            var r=Panel(p,value,pos,size,color??cream);var im=r.GetComponent<Image>();im.raycastTarget=true;
            var b=r.gameObject.AddComponent<Button>();b.onClick.AddListener(()=>action());Text(r,value,Vector2.zero,size-new Vector2(12,4),25);return b;
        }
        Sprite Art(string file)
        {
            if(cache.TryGetValue(file,out var sprite))return sprite;
            string path=Path.Combine(Root,file);if(!File.Exists(path)){Debug.LogError("Missing image: "+path);return null;}
            var tex=new Texture2D(2,2,TextureFormat.RGBA32,false);if(!tex.LoadImage(File.ReadAllBytes(path)))Debug.LogError("Cannot decode image: "+path);tex.filterMode=FilterMode.Bilinear;
            sprite=Sprite.Create(tex,new Rect(0,0,tex.width,tex.height),new Vector2(.5f,.5f),100);cache[file]=sprite;return sprite;
        }
        public void LoadLevel(int index)
        {
            LoadRequested(index,false);
        }
        void LoadRequested(int index,bool replay)
        {
            StopAllCoroutines();
            foreach(var view in flyingItems)if(view!=null){view.gameObject.SetActive(false);Destroy(view.gameObject);}
            flyingItems.Clear();busy=false;index=(index+Index.levels.Count)%Index.levels.Count;
            if(TidyAssetCache.InAndroidPlayer){busy=true;StartCoroutine(LoadAndroid(index,replay));}
            else{LoadLevelNow(index);if(replay)StartCoroutine(Replay());}
        }
        IEnumerator LoadAndroid(int index,bool replay)
        {
            BeginModal("LOADING LEVEL");string error=null;
            yield return TidyAssetCache.Fetch(Index.levels[index].file,e=>error=e);
            LevelData data=null;
            if(error==null)try{data=LevelData.Load(Path.Combine(Root,Index.levels[index].file));}catch(Exception e){error=e.Message;}
            if(error==null)
            {
                var files=new HashSet<string>(data.content.Select(i=>i.art)){data.bg};
                if(data.HasBackgroundComparison)files.Add(data.DefaultBackground);
                foreach(string ui in CommonUi)files.Add(UiPath(data,ui));
                files.Add(UiPath(data,UsesTidyRoomArt(data)?"Hint":"GP_Icon_RainbowBox"));
                foreach(string file in files){yield return TidyAssetCache.Fetch(file,e=>error=e);if(error!=null)break;}
            }
            busy=false;
            if(error!=null){BeginModal("CANNOT LOAD LEVEL");Text(modal,error,Vector2.zero,new Vector2(920,500),28);Button(modal,"Choose level",new Vector2(0,-450),new Vector2(600,90),OpenPicker);yield break;}
            LoadLevelNow(index);if(replay)StartCoroutine(Replay());
        }
        void LoadLevelNow(int index)
        {
            Selected=index;PlayerPrefs.SetInt("TidyTestLevel",Selected);
            CloseModal();if(board!=null){board.gameObject.SetActive(false);Destroy(board.gameObject);}if(hud!=null){hud.gameObject.SetActive(false);Destroy(hud.gameObject);}
            Model=new TidyModel(LevelData.Load(Path.Combine(Root,Index.levels[Selected].file)));zoom=1;pan=Vector2.zero;itemViews.Clear();
            board=Panel(phone,"Room View",Vector2.zero,new Vector2(1080,1920),new Color(.97f,.94f,.88f));
            board.GetComponent<Image>().raycastTarget=true;board.gameObject.AddComponent<RectMask2D>();board.gameObject.AddComponent<BoardPointer>().Owner=this;
            world=Rect(board,"Room Coordinates",Vector2.zero,Vector2.zero);
            var l=Model.Level;
            compareBackground=false;
            var backdropRect=Rect(world,"Room background",Vector2.zero,Vector2.zero);
            roomBackdrop=backdropRect.gameObject.AddComponent<RawImage>();roomBackdrop.raycastTarget=false;
            ApplyBackground();
            foreach(var item in l.content)
            {
                var view=Image(world,$"{item.uid}: {item.id}",Art(item.art),new Vector2(item.x,item.y),new Vector2(item.width,item.height)).rectTransform;
                view.localRotation=Quaternion.Euler(0,0,item.angle);view.localScale=new Vector3(item.scaleX,item.scaleY,1);itemViews.Add(view);
            }
            Render();
            var used=new HashSet<string>(l.content.Select(i=>i.art)){l.bg,l.DefaultBackground};
            foreach(string k in cache.Keys.Where(k=>!used.Contains(k)&&!k.StartsWith("Art/UI/")&&!k.StartsWith("Art/TidyRoomUI/")).ToArray())
            {Destroy(cache[k].texture);Destroy(cache[k]);cache.Remove(k);}
        }
        void ApplyBackground()
        {
            var level=Model.Level;
            string path=compareBackground?level.bg:level.DefaultBackground;
            Sprite bg=Art(path);
            Vector2 size=level.BackgroundSize(path,bg==null?new Vector2(1080,1920):bg.rect.size);
            roomBackdrop.rectTransform.sizeDelta=size;
            roomBackdrop.texture=bg==null?null:bg.texture;
            // A flat floor colour fills only the margins outside the authored room.
            Color floor=new Color(.97f,.94f,.88f);
            if(bg!=null)
            {
                floor=Color.clear;
                for(int n=0;n<16;n++)floor+=bg.texture.GetPixel((int)((n+.5f)*bg.texture.width/16),0);
                floor/=16;floor.a=1;
            }
            board.GetComponent<Image>().color=floor;
            framing=new TidyRoomFraming(level,size);center=framing.Content.center;fit=framing.Scale;
            ApplyView();
        }
        void ApplyView()
        {
            float scale=fit*zoom;world.localScale=Vector3.one*scale;
            Vector2 origin=-center*scale+TidyRoomFraming.PlayArea.center;
            world.anchoredPosition=framing.Clamp(origin+pan,scale);
            pan=world.anchoredPosition-origin;
        }
        public void Zoom(float factor){zoom=Mathf.Clamp(zoom*factor,1,3);ApplyView();}
        public void Pan(Vector2 delta){float scale=canvas.GetComponent<Canvas>().scaleFactor;pan+=delta/scale;ApplyView();}
        public void BoardTap(Vector2 screen)
        {
            if(busy||modal!=null||Model.State!=RunState.Playing)return;
            RectTransformUtility.ScreenPointToLocalPointInRectangle(world,screen,null,out var p);
            for(int uid=Model.Places.Length-1;uid>=0;uid--)
            {
                var it=Model.Level.content[uid];if(Model.Places[uid]!=ItemPlace.Room||!(Model.SourceGeometry?it.HitSource(p):it.HitArt(p)))continue;
                Pick(uid);return;
            }
        }
        public bool Pick(int uid)
        {
            if(busy||modal!=null||Model==null||Model.State!=RunState.Playing||uid<0||uid>=Model.Places.Length)return false;
            int box=Model.FindBox(Model.TypeOf(uid));Vector3 start=itemViews[uid].position;
            if(!Model.Tap(uid)){Render();return false;}
            Render();Vector2 target=box>=0?BoxPosition(box):SlotPosition(Model.Tray.Count-1);
            StartCoroutine(Fly(uid,start,target));return true;
        }
        IEnumerator Fly(int uid,Vector3 start,Vector2 target)
        {
            // The model commits immediately. Independent visual flights must not lock input.
            var it=Model.Level.content[uid];var v=Image(phone,"Flying item",Art(it.art),Vector2.zero,new Vector2(110,110));v.preserveAspect=true;v.transform.position=start;
            flyingItems.Add(v.rectTransform);
            Vector3 from=v.rectTransform.anchoredPosition;float elapsed=0;
            while(elapsed<.28f){elapsed+=Time.unscaledDeltaTime;float t=Mathf.Clamp01(elapsed/.28f);v.rectTransform.anchoredPosition=Vector2.Lerp(from,target,t)+new Vector2(0,Mathf.Sin(t*Mathf.PI)*70);yield return null;}
            flyingItems.Remove(v.rectTransform);Destroy(v.gameObject);
        }
        void Render()
        {
            if(hud!=null){hud.gameObject.SetActive(false);Destroy(hud.gameObject);}hud=Rect(phone,"HUD",Vector2.zero,new Vector2(1080,1920));
            // Transparent input shields stop taps on UI from selecting room items underneath.
            Panel(hud,"Header input shield",new Vector2(0,755),new Vector2(1080,410),Color.clear).GetComponent<Image>().raycastTarget=true;
            Panel(hud,"Footer input shield",new Vector2(0,-885),new Vector2(1080,150),Color.clear).GetComponent<Image>().raycastTarget=true;
            for(int i=0;i<itemViews.Count;i++)
            {
                itemViews[i].gameObject.SetActive(Model.Places[i]==ItemPlace.Room);
                if(Model.Places[i]==ItemPlace.Room)itemViews[i].GetComponent<Image>().color=showAvailability&&Model.IsCovered(i)?new Color(.55f,.55f,.55f,.8f):Color.white;
            }
            Panel(hud,"Level label",new Vector2(0,909),new Vector2(570,65),new Color(1,.97f,.89f,.88f));
            Text(hud,(Model.Level.source=="Happy"?"Happy ":"Room ")+Model.Level.levelName,new Vector2(0,909),new Vector2(550,60),36,purple);
            Button(hud,"Levels",new Vector2(-425,909),new Vector2(190,65),()=>OpenPicker());
            Button(hud,"Restart",new Vector2(425,909),new Vector2(190,65),()=>LoadLevel(Selected));
            float progress=Model.Delivered/(float)Model.Places.Length;
            Panel(hud,"Progress track",new Vector2(0,861),new Vector2(960,8),new Color(.78f,.72f,.84f));
            Panel(hud,"Progress",new Vector2(-480+(960*progress)/2,861),new Vector2(Mathf.Max(1,960*progress),8),new Color(.46f,.70f,.46f));
            for(int b=0;b<3;b++)DrawBox(b);
            for(int i=0;i<7;i++)
            {
                Vector2 p=SlotPosition(i);bool open=i<Model.Capacity;
                var slot=Image(hud,"Waiting slot "+i,UiArt("GP_Slot"),p,new Vector2(100,100));slot.preserveAspect=true;
                if(!open){slot.color=new Color(1,1,1,.65f);Button(hud,"+",p,new Vector2(75,75),()=>{Model.AddSlot();Render();});}
                else if(i<Model.Tray.Count){var im=Image(hud,"Waiting item",Art(Model.Level.content[Model.Tray[i]].art),p,new Vector2(85,85));im.preserveAspect=true;}
            }
            Panel(hud,"Message backing",new Vector2(0,-831),new Vector2(1040,42),new Color(1,.97f,.89f,.88f));
            Text(hud,$"{Model.Message}  ·  {Model.Remaining} left",new Vector2(0,-831),new Vector2(1020,42),23,Model.State==RunState.Lose?new Color(.75f,.20f,.20f):ink);
            Booster("Vacuum","NewBooster_Icon_Vaccum",-210,()=>{Model.Vacuum();Render();});
            Booster("Broom","NewBooster_Icon_Clear",0,()=>{Model.Broom();Render();});
            Action hint=()=>{int uid=Model.Hint();Model.Message=uid>=0?"Highlighted a matching item":"Clear an upper layer first";Render();if(uid>=0)itemViews[uid].GetComponent<Image>().color=new Color(.6f,1,.6f);};
            if(TidyRoomArt)Booster("Hint","Hint",210,hint);
            else Button(hud,"Hint",new Vector2(210,-905),new Vector2(190,86),hint);
            Button(hud,"Next >",new Vector2(420,-905),new Vector2(190,86),()=>LoadLevel(Selected+1));
            Button(hud,"-",new Vector2(-480,600),new Vector2(80,80),()=>Zoom(.85f));
            Button(hud,"+",new Vector2(480,600),new Vector2(80,80),()=>Zoom(1.15f));
            Button(hud,"Test options",new Vector2(-420,-905),new Vector2(190,86),()=>OpenOptions());
            if(Model.Storage.Count>0)
            {
                var stored=Button(hud,"",new Vector2(165,753),new Vector2(90,100),OpenStorage);
                Image(stored.transform,"Storage",UiArt(TidyRoomArt?"GP_Box0":"GP_Icon_RainbowBox"),new Vector2(0,12),new Vector2(74,58)).preserveAspect=true;
                Text(stored.transform,$"{Model.Storage.Count}",new Vector2(0,-30),new Vector2(85,30),22);
            }
            if(Model.State!=RunState.Playing)
            {
                Panel(hud,"Result",new Vector2(0,-180),new Vector2(800,310),cream);
                Text(hud,Model.State==RunState.Win?"ALL TIDY!":"SLOTS ARE FULL",new Vector2(0,-100),new Vector2(750,90),52,purple);
                Text(hud,Model.State==RunState.Win?"Every item is in its box":"Use Broom, add a slot, or restart",new Vector2(0,-180),new Vector2(750,60),29);
                Button(hud,Model.State==RunState.Win?"Next level":"Try again",new Vector2(0,-270),new Vector2(360,75),()=>LoadLevel(Model.State==RunState.Win?Selected+1:Selected));
            }
            foreach(var view in flyingItems)if(view!=null)view.SetAsLastSibling();
        }
        void DrawBox(int b)
        {
            Vector2 pos=BoxPosition(b);
            if(b>=Model.Boxes.Count)
            {
                if(TidyRoomArt)
                {
                    var muted=new Color(.63f,.70f,.78f);
                    Image(hud,"Locked box",UiArt("GP_Box0"),pos,new Vector2(210,165),muted).preserveAspect=true;
                    Image(hud,"Box lid",UiArt("GP_Box_Unlock"),pos+new Vector2(0,55),new Vector2(216,45),muted).preserveAspect=true;
                }
                else Image(hud,"Locked box",UiArt("GP_Box_Unlock"),pos,new Vector2(210,165)).preserveAspect=true;
                Button(hud,"+ Box",pos,new Vector2(145,60),()=>{Model.AddBox();Render();});return;
            }
            var box=Model.Boxes[b];Image(hud,"Box "+b,UiArt("GP_Box0"),pos,new Vector2(220,175)).preserveAspect=true;
            if(box.order<0){Text(hud,"DONE",pos,new Vector2(200,65),29);return;}
            var order=Model.Level.order[box.order];var item=Model.Level.content.First(i=>i.sourceType==order.sourceType);
            Image(hud,"Category icon",Art(item.art),pos+new Vector2(0,TidyRoomArt?15:23),new Vector2(82,TidyRoomArt?58:70)).preserveAspect=true;
            Text(hud,order.label,pos+new Vector2(0,TidyRoomArt?-24:-39),new Vector2(TidyRoomArt?185:210,36),TidyRoomArt?21:23);
            Text(hud,$"{box.count}/{order.count}",pos+new Vector2(0,TidyRoomArt?-51:-73),new Vector2(190,34),29);
        }
        void Booster(string label,string icon,float x,Action action)
        {
            var button=Button(hud,"",new Vector2(x,-905),new Vector2(190,86),action);
            Image(button.transform,label,UiArt(icon),new Vector2(-53,0),new Vector2(58,58)).preserveAspect=true;
            Text(button.transform,label,new Vector2(32,0),new Vector2(120,65),24);
        }
        void CloseModal(){if(modal!=null){modal.gameObject.SetActive(false);Destroy(modal.gameObject);modal=null;}}
        void BeginModal(string title)
        {
            CloseModal();modal=Panel(phone,"Modal",Vector2.zero,new Vector2(1030,1850),cream);modal.GetComponent<Image>().raycastTarget=true;
            Text(modal,title,new Vector2(0,830),new Vector2(850,70),42,purple);Button(modal,"Close",new Vector2(390,830),new Vector2(170,65),CloseModal);
        }
        public void OpenPicker()
        {
            BeginModal("CHOOSE LEVEL");
            Button(modal,"RoomSort / Tidy Room",new Vector2(-225,725),new Vector2(370,70),()=>{filter="RoomSort";page=0;OpenPicker();});
            Button(modal,"Happy reference",new Vector2(180,725),new Vector2(360,70),()=>{filter="Happy";page=0;OpenPicker();});
            var entries=Index.levels.Select((e,i)=>new{e,i}).Where(x=>x.e.source==filter).ToArray();int pages=(entries.Length+15)/16;page=Mathf.Clamp(page,0,pages-1);
            foreach(var x in entries.Skip(page*16).Take(16).Select((x,n)=>new{x,n}))
            {
                int ix=x.x.i;var e=x.x.e;Button(modal,e.label+(e.review?"  *":""),new Vector2(0,615-x.n*74),new Vector2(940,65),()=>{CloseModal();LoadLevel(ix);});
            }
            Text(modal,$"{page+1}/{pages}   * category mapping needs review",new Vector2(0,-680),new Vector2(940,65),25);
            Button(modal,"< Previous",new Vector2(-250,-790),new Vector2(380,75),()=>{page--;OpenPicker();});Button(modal,"Next >",new Vector2(250,-790),new Vector2(380,75),()=>{page++;OpenPicker();});
        }
        void OpenOptions()
        {
            BeginModal("LEVEL TEST OPTIONS");
            Text(modal,Model.Level.key+"\nConverted levels keep source category IDs separate.\nA * marks categories that need an art mapping decision.",new Vector2(0,655),new Vector2(900,120),27);
            if(Model.Level.HasBackgroundComparison)
                Button(modal,compareBackground?"Background: Tidy Room":"Background: RoomSort original",new Vector2(0,540),new Vector2(900,80),()=>{compareBackground=!compareBackground;ApplyBackground();CloseModal();});
            else if(Model.Level.source=="RoomSort")
                Text(modal,"Background: RoomSort original",new Vector2(0,540),new Vector2(900,80),30);
            if(Model.Level.source=="RoomSort")Button(modal,Model.SourceGeometry?"Collision: RoomSort source":"Collision: item image",new Vector2(0,440),new Vector2(900,100),()=>{Model.SourceGeometry=!Model.SourceGeometry;Model.Recheck();OpenOptions();RenderBehind();});
            else Text(modal,"Collision: Happy image",new Vector2(0,440),new Vector2(900,100),30);
            Button(modal,Model.StrictFull?"Lose: immediately when slots are full":"Lose: full slots and no direct move",new Vector2(0,300),new Vector2(900,100),()=>{Model.StrictFull=!Model.StrictFull;Model.Recheck();OpenOptions();RenderBehind();});
            Button(modal,"Replay supplied solution",new Vector2(0,140),new Vector2(900,100),()=>{CloseModal();LoadRequested(Selected,true);});
            Text(modal,"The exact Happy coverage threshold and fail timing are provisional.\nSource collision uses RoomSort's original overlap calculations.\nImage collision uses the imported alpha silhouettes.",new Vector2(0,-60),new Vector2(900,230),28);
            string issues=Model.Level.issues==null?"":string.Join("\n",Model.Level.issues.Take(7));Text(modal,issues.Length==0?"No category conversion issues on this level":issues,new Vector2(0,-430),new Vector2(900,450),24);
            Button(modal,showAvailability?"Hide layers":"Layers",new Vector2(-310,-770),new Vector2(285,85),()=>{showAvailability=!showAvailability;OpenOptions();RenderBehind();});
            Button(modal,"Previous level",new Vector2(0,-770),new Vector2(285,85),()=>LoadLevel(Selected-1));
            Button(modal,"Reset view",new Vector2(310,-770),new Vector2(285,85),()=>{zoom=1;pan=Vector2.zero;ApplyView();CloseModal();});
        }
        void RenderBehind(){Render();modal.SetAsLastSibling();}
        void OpenStorage()
        {
            BeginModal("TEMPORARY STORAGE");
            Text(modal,"Stored items automatically move into matching boxes.",new Vector2(0,700),new Vector2(900,110),29);
            int n=0;foreach(int uid in Model.Storage.Take(36))
            {var im=Image(modal,"Stored item",Art(Model.Level.content[uid].art),new Vector2(-360+(n%5)*180,520-(n/5)*170),new Vector2(145,145));im.preserveAspect=true;n++;}
        }
        IEnumerator Replay()
        {
            if(Model.Level.proof==null||Model.Level.proof.Length==0){Model.Message="No supplied solution for this board";Render();yield break;}
            var path=Model.Level.proof;busy=true;
            foreach(int uid in path){if(!Model.Tap(uid)){Model.Message="Replay stopped at UID "+uid;break;}Render();yield return new WaitForSeconds(.035f);}
            busy=false;Render();
        }
        public object RunProof(int index,bool source=true)
        {
            var data=LevelData.Load(Path.Combine(Root,Index.levels[index].file));var m=new TidyModel(data);m.SourceGeometry=source;m.StrictFull=false;int rejected=0;
            foreach(int uid in data.proof??Array.Empty<int>())if(!m.Tap(uid))rejected++;
            return new {data.key,state=m.State.ToString(),rejected,delivered=m.Delivered,total=m.Places.Length,peakTray=m.PeakTray};
        }
    }
}
